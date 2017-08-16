import yaml
import re

import pandas as pd
import mysql.connector
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
                               na_syns=cfg['na_synonyms'])
    logger.info('loaded survey dfs', shape=svydf.shape)
    ksvy = serdes.surveys_key4id(cfg['id'])
    logger.info('saving survey data to feather', name=ksvy)
    serdes.save_feather(ksvy, svydf)
    logger.unbind('dataset')


def setup_table(df, tblname, engine):
    logger.info('creating schema for column store', name=tblname)
    q = pd.io.sql.get_schema(df[:0], tblname, con=engine)
    q = q.replace('TEXT', 'VARCHAR(100)').replace('BIGINT', 'INT') + \
        ' engine=columnstore default character set=utf8;'
    q = re.sub(r'FLOAT\(\d+\)', 'FLOAT', q)
    with engine.connect() as con:
        con.execute(q)


def bulk_load_df(tblname, engine):
    logger.info('loading data from feather', name=tblname)
    df = serdes.load_feather(tblname)
    logger.info('saving data to csv for bulk load', name=tblname)
    serdes.save_csv(tblname, df, index=False, header=False)
    setup_table(df, tblname, engine)
    logger.info('bulk loading data using cfimport', name=tblname)

def bulk_load_df(tblname, engine)

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
    load_survey_data('config/data/brfss_pre2011.yaml')
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
