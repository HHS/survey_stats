import yaml
import pandas as pd
from survey_stats import log
from survey_stats.etl.sas_import import load_sas_xport_df
from survey_stats.etl.socrata import process_socrata_url
from survey_stats import serdes


logger = log.getLogger()


def load_surveys(meta, prefix, qids, facets):
    logger.bind(p=prefix)
    undash_fn = lambda x: 'x' + x if x[0] == '_' else x
    meta_df = pd.DataFrame(meta.rows, columns=meta.columns)
    dfs = [load_sas_xport_df(r=r, p=prefix, qids=qids, facets=facets) for
           idx, r in list(meta_df.iterrows())]
    logger.info('merging SAS dfs')
    dfs = (pd.concat(dfs, ignore_index=True)
           .apply(lambda x: x.astype('category') if
                  x.dtype.name in ['O','object'] else x)
           .pipe(lambda xf: xf.rename(index=str,
                                      columns={x:undash_fn(x) for
                                               x in xf.columns})))
    logger.info('merged SAS dfs', shape=dfs.shape,
                summary=dfs.dtypes.value_counts(dropna=False).to_dict())
    logger.unbind('p')
    return dfs


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
    soda = socrata.load_socrata_data(cfg['socrata'])
    ksoda = serdes.surveys_key4id(cfg['id'])
    save_feather(ksoda,soda)
    logger.info('saving socrata data to csv')
    save_csv(ksoda, soda)
    logger.info('loading survey dfs')
    svydf = load_surveys(meta=cfg['surveys']['meta'],
                         prefix=cfg['surveys']['s3_url_prefix'],
                         qids=cfg['surveys']['qids'],
                         facets=cfg['facets'])
    logger.info('loaded survey dfs', shape=svydf.shape)
    ksvy = serdes.socrata_key4id(cfg['id'])
    logger.info('saving survey data to feather', name=ksvy)
    save_feather(ksvy, svydf)
    logger.info('saving survey data to csv', name=ksvy)
    save_csv(ksvy, svydf)
    logger.unbind('dataset')

if __name__=='__main__':
    load_survey_data('data/brfss.yaml')
