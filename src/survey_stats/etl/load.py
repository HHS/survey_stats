import re
import os
import yaml
import pandas as pd
import sqlalchemy as sa
import dask
import dask.multiprocessing
import dask.cache
from cytoolz.curried import map
from multiprocessing.pool import ThreadPool
from timeit import default_timer as timer

from survey_stats import log
from survey_stats import serdes
from survey_stats.types import DatasetConfig
from survey_stats.dbi import DatabaseConfig, DatasetPart, get_datafile_path
from survey_stats.etl.sas import process_sas_survey
from survey_stats.etl.spss import process_fwf_w_spss_loader
from survey_stats.etl.socrata import load_socrata_data, get_metadata_socrata

logger = log.getLogger(__name__)


def undash(col):
    return 'x' + col if col[0] == '_' else col


def load_survey_data(cfg, client=None):
    logger.info('loading survey dfs')
    svydf = None
    if cfg.surveys.parse_mode == 'sas':
        svydf = process_sas_survey(cfg.surveys,
                                   facets=cfg.facets,
                                   client=client, lgr=logger)
    elif cfg.surveys.parse_mode == 'spss':
        svydf = process_fwf_w_spss_loader(cfg.surveys,
                                          facets=cfg.facets,
                                          client=client, lgr=logger)
    else:
        raise NotImplementedError('Config parse_mode must be spss or sas!')

    logger.info('loaded survey dfs', shape=svydf.shape)
    svydf = svydf.compute()
    svydf = svydf.reset_index(drop=True)
    mx = (svydf.select_dtypes(include=['object', 'category'])
               .apply(lambda xf: xf.value_counts().to_dict())
               .to_dict())
    #                   )[svydf.apply(lambda yf: yf.dropna().apply(lambda q: type(q) != str))
    #                          .dropna().any(0)])
    # mx = (svydf.select_dtypes(include=['object', 'category'])
    #            .apply(lambda xf: xf.value_counts().to_dict()
    #                   )[svydf.apply(lambda yf: yf.dropna().apply(lambda q: type(q) != str))
    #                          .dropna().any(0)])
    # mx2 = (svydf.applymap(lambda yf: type(yf).__name__)[list(mx.keys())]).apply(lambda xf: xf.value_counts())
    # mx = mx.to_dict()
    # if len(mx) > 0:
    #     logger.error('Found category columns with non-str labels!', mx=mx, mx2=mx2)
    #     # TODO: check formats list in advance to see if expected fmts missing
    #     raise LookupError('Found categoricals with non-string labels!', mx.keys())
    return (svydf, mx)


def load_csv_mariadb_columnstore(df, tblname, engine):
    logger.info('creating schema for column store', name=tblname)
    start = timer()
    q = pd.io.sql.get_schema(df[:0], tblname, con=engine)
    q = q.replace('TEXT', 'VARCHAR(100)').replace('BIGINT', 'INT') + \
        ' engine=columnstore default character set=utf8;'
    q = re.sub(r'FLOAT\(\d+\)', 'FLOAT', q)
    with engine.connect() as con:
        con.execute(q)
    logger.info('bulk loaded data using cfimport', name=tblname, rows=df.shape[0], elapsed=timer()-start)


def load_csv_monetdb(df, tblname, engine):
    copy_tmpl = "COPY {nrows} OFFSET 2 RECORDS INTO {tbl} from '{csvf}'" + \
                " USING DELIMITERS ',','\n','\"' NULL AS ''"
    logger.info('creating schema for column store', name=tblname)
    start = timer()
    q = pd.io.sql.get_schema(df[:0], tblname, con=engine)
    q = q.replace('\n', ' ').replace('\t', ' ').replace('year', 'yr')
    logger.info('dumping to csv for bulk load', q=q)
    csvf = serdes.save_csv(tblname, df, index=False, header=True)
    csvf = os.path.abspath(csvf)
    copy_cmd = copy_tmpl.format(nrows=df.shape[0]+1000,
                                 tbl=tblname, csvf=csvf)
    sql_instrs = q + ';\n\n'
    sql_instrs += copy_cmd + ';\n\n'
    with open('cache/'+tblname+'.sql', 'w') as fh:
        fh.write(sql_instrs)
    csvtime = timer()
    logger.info('bulk loading csv into monetdb', csvf=csvf, elapsed=csvtime-start)
    with engine.begin() as con:
        try:
            con.execute("DROP TABLE %s" % tblname)
        except Exception as e:
            # continue if table non-existent,
            # else, what happened?!
            if str(e).find('no such table') == -1:
                raise
        con.execute(q)
        con.execute(copy_cmd)

    logger.info('bulk loaded data using cfimport', name=tblname,
                rows=df.shape[0], elapsed_copy=timer()-csvtime,
                elapsed=timer()-start)


def load_sqlalchemy(df, engine, tbl):
    logger.info('loading df into monetdb table', name=tbl)
    start = timer()
    with engine.begin() as con:
        df.to_sql(tbl, con, chunksize=10000, if_exists='replace', index=False)
    logger.info('loaded dataframe into monetdb', tbl=tbl, rows=df.shape[0], elapsed_step=timer()-start)


def bulk_load_df(tblname, engine):
    logger.info('loading data from feather', name=tblname)
    df = serdes.load_feather(tblname)
    if engine.name == 'mysql':
        load_csv_mariadb_columnstore(df, tblname, engine)
    elif engine.name == 'monetdb':
        load_csv_monetdb(df, tblname, engine)


def setup_tables(cfg, dburl):
    engine = sa.create_engine(dburl)
    if cfg.surveys:
        ksvy = serdes.surveys_key4id(cfg.id)
        bulk_load_df(ksvy, engine)
    if cfg.socrata:
        ksoc = serdes.socrata_key4id(cfg.id)
        bulk_load_df(ksoc, engine)


def process_dataset(cfg, dbc, cache_dir, resume=True):
    logger.bind(dataset=cfg.id)
    logger.info('checking for socrata, processing', s=cfg.socrata)
    if cfg.socrata:
        ksoc = get_datafile_path(DatasetPart.SOCRATA.value, cfg.id, cache_dir)
        if os.path.isfile(ksoc) and resume:
            logger.warn('found socrata artifact, moving on', resume=resume)
        else:
            logger.info('generating socrata data', resume=resume, overwriting=os.path.isfile(ksoc))
            dsoc = load_socrata_data(cfg.socrata, cfg.facets)
            logger.info('saving socrata data to feather', f=ksoc)
            dsoc.to_feather(ksoc)
            logger.info('saved socrata data to feather', f=ksoc)
            # short process, can be run regardless
            (qns, facs) = get_metadata_socrata(cfg.socrata, dsoc, cfg.facets)
            logger.info('created schema for socrata')
            qns.to_feather(get_datafile_path(DatasetPart.SCHEMA.value, cfg.id, cache_dir))
            facs.to_feather(get_datafile_path(DatasetPart.FACETS.value, cfg.id, cache_dir))
    logger.info('checking for surveys, processing', s=cfg.surveys)
    if cfg.surveys:
        svyf = get_datafile_path(DatasetPart.SURVEYS.value, cfg.id, cache_dir)
        svy_descf = svyf+'.yaml' 
        if os.path.isfile(svyf) and resume:
            logger.warn('found surveys artifact, moving on', resume=resume)
        else:
            logger.info('generating surveys data', resume=resume, overwriting=os.path.isfile(svyf))
            (svydf, svymeta) = load_survey_data(cfg)
            logger.info('saving survey data to feather', svyf)
            svydf.to_feather(svyf)
            logger.info('saving survey desc data to feather', svy_descf)
            with open(svy_descf, 'w') as fh:
                yaml.dump(svymeta, fh)
            logger.info('saved survey data to feather', name=svy_descf)
    if dbc is not None:
        setup_tables(cfg, dbc.uri)
    logger.unbind('dataset')


def restore_data(sql_conn):
    configs = map(lambda x: os.path.join('config/data', x),
                  os.listdir('config/data'))
    logger.info('restoring tables to survey database')
    for yaml_f in configs:
        cfg = DatabaseConfig.from_yaml(yaml_f)
        logger.bind(dataset=cfg.id)
        setup_tables(cfg, sql_conn)
        logger.unbind('dataset')


def load_datasets(cache_dir, dbc, dsets, parse_all=False, resume=True):
    import cytoolz.dicttoolz as dz
    cache = dask.cache.Cache(8e9)
    cache.register()
    dask.set_options(get=dask.threaded.get, pool=ThreadPool())
    configs = list(
        map(lambda x: os.path.join('config/data', x), 
            os.listdir('config/data')))
    cmap = {k: DatasetConfig.from_yaml(k) for k in configs}
    dsids = dz.valmap(lambda ds: ds.id, cmap)
    cmap = dz.merge(cmap, {d.id: d for d in cmap.values()})
    if parse_all:
        dsets = dsids
    for d in dsets:
        process_dataset(cmap[d], dbc, cache_dir)

