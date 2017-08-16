import yaml
import re

import pandas as pd
import pymonetdb
import pymysql.cursors
import sqlalchemy as sa
import subprocess as sp

from survey_stats import log
from survey_stats.etl.sas_import import load_sas_xport_df, process_sas_survey
from survey_stats.etl.socrata import process_socrata_url
from survey_stats import serdes


logger = log.getLogger()




def load_socrata_data(params):
    dfs = [process_socrata_url(url=url,
                              rename=params['rename'],
                              remap=params['remap'],
                              apply_fn=params['apply_fn'],
                              c_filter=params['c_filter'],
                              unstack=params['unstack'],
                              fold_stats=params['fold_stats'])
          for url in soda_api]
    dfs = pd.concat(dfs, ignore_index=True)
    return dfs


def load_survey_data(yaml_f):
    cfg = None
    with open(yaml_f) as fh:
        cfg = yaml.load(fh)
    logger.bind(dataset=cfg['id'])
    '''soda = process_socrata_url(**cfg['socrata'])
    ksoda = serdes.socrata_key4id(cfg['id'])
    serdes.save_feather(ksoda,soda)
    logger.info('saving socrata data to csv')
    serdes.save_csv(ksoda, soda)'''
    logger.info('loading survey dfs')
    svydf = process_sas_survey(meta=cfg['surveys']['meta'],
                               prefix=cfg['surveys']['s3_url_prefix'],
                               qids=cfg['surveys']['qids'],
                               facets=cfg['facets'], 
                               na_syns=cfg['surveys']['na_synonyms'])
    logger.info('loaded survey dfs', shape=svydf.shape)
    ksvy = serdes.surveys_key4id(cfg['id'])
    logger.info('saving survey data to feather', name=ksvy)
    serdes.save_feather(ksvy, svydf)
    logger.unbind('dataset')


def load_csv_mariadb_columnstore(df, tblname, engine):
    logger.info('creating schema for column store', name=tblname)
    q = pd.io.sql.get_schema(df[:0], tblname, con=engine)
    q = q.replace('TEXT', 'VARCHAR(100)').replace('BIGINT', 'INT') + \
        ' engine=columnstore default character set=utf8;'
    q = re.sub(r'FLOAT\(\d+\)', 'FLOAT', q)
    with engine.connect() as con:
        con.execute(q)
        logger.info('bulk loading data using cfimport', name=tblname)


def load_csv_monetdbr(df, csvf, engine, tbl):
    logger.info('creating schema for MonetDB', name=tbl)
    q = pd.io.sql.get_schema(df[:0], tbl, con=engine)
    q = q.replace('BIGINT', 'INT')
    with engine.connect() as con:
        con.execute('DROP TABLE IF EXISTS %s' % tbl)
        con.execute(q)
    logger.info('bulk loading csv using MonetDB.R', tbl=tbl, q=q)
    from rpy2.robjects.packages import importr
    import rpy2.robjects as ro
    read_csv_fn = ro.r('''
    function(con, file, tbl, cols, ...){
        require('MonetDB.R')
        monetdb.read.csv(con, files=file, tablename=tbl, header=FALSE, 
                         locked=TRUE, col.names=cols, na.strings='NA', 
                         nrow.check=1000000, ...)
    }
    ''')
    rmonet = importr('MonetDB.R')
    dbi = importr('DBI')
    params = {
        'host': engine.url.host,
        'dbname': engine.url.database
    }
    if engine.url.port:
        params['port'] = engine.url.port
    if engine.url.username:
        params['user'] = engine.url.username
    if engine.url.password:
        params['password'] = engine.url.password
    con = dbi.dbConnect(rmonet.MonetDBR(), **params )
    read_csv_fn(con, csvf, tbl, list(df.columns))


def bulk_load_df(tblname, engine):
    logger.info('loading data from feather', name=tblname)
    df = serdes.load_feather(tblname)
    logger.info('saving data to csv for bulk load', name=tblname)
    csvf = serdes.save_csv(tblname, df, index=False, header=False)
    if engine.name == 'mysql':
        load_csv_mariadb_columnstore(df, tblname, engine)
    elif engine.name == 'monetdb':
        load_csv_monetdbr(df, csvf, engine, tblname)



def setup_tables(yaml_f, dburl):
    cfg = None
    with open(yaml_f) as fh:
        cfg = yaml.load(fh)
    engine = sa.create_engine(dburl)
    ksvy = serdes.surveys_key4id(cfg['id'])
    bulk_load_df(ksvy, engine)
    ksoc = serdes.socrata_key4id(cfg['id'])
    bulk_load_df(ksoc, engine)


if __name__ == '__main__':
    default_sql_conn = 'mysql+pymysql://mcsuser:mcsuser@localhost:4306/survey'
    default_sql_conn = 'monetdb://localhost/survey'
    # load_survey_data('config/data/brfss.yaml')
    #load_survey_data('config/data/brfss.yaml')
    setup_tables(
        'config/data/brfss.yaml',
        default_sql_conn
    )
    '''
    setup_tables(
        'config/data/brfss_pre2011.yaml',
        'mysql+pymysql://mcsuser:mcsuser@localhost:4306/survey'
    )
    setup_tables(
        'config/data/brfss_pre2011.yaml',
        'mysql+://mcsuser:mcsuser@localhost:4306/survey'
    )'''
