import blaze as bz
from odo import odo
import feather
import json
import pandas as pd
from cytoolz.itertoolz import mapcat
from collections import namedtuple
from survey_stats import log
from survey_stats.types import load_config_from_yaml
from survey_stats.survey import fetch_stats, des_from_survey_db
from dask import delayed


TMPL_METAF = 'cache/{id}.schema.json'
TMPL_SOCTBL = '{id}_socrata'
TMPL_SVYTBL = '{id}_surveys'
TMPL_SVYFTH = 'cache/{id}_surveys.feather'
TMPL_SOCFTH = 'cache/{id}_socrata.feather'


STATS_COLUMNS = ['count', 'mean', 'ci_u', 'ci_l', 'std_err']

logger = log.getLogger()


def resolve_db_url(url):
    return (feather.read_dataframe(url) if
            url.endswith('.feather') else
            bz.data(url))


class SurveyDataset(namedtuple('SurveyDataset',
                               ['cfg', 'meta', 'soc', 'svy', 'des'])):
    __slots__ = ()

    @classmethod
    def load_dataset(cls, cfg_f, dbc):
        # given a config file and blaze data handle,
        # work some magic
        cfg = load_config_from_yaml(cfg_f)
        id = cfg.id
        meta_f = TMPL_METAF.format(id=id)
        with open(meta_f, 'r+') as mh:
            meta = json.load(mh)
        meta = pd.DataFrame(meta)
        meta.index = meta.qid
        svytbl = dbc[TMPL_SVYTBL.format(id=id)]
        soctbl = resolve_db_url(TMPL_SOCFTH.format(id=id))
        logger.info('set up urls for svytbl, soctbl', id)
        des = des_from_survey_db(id+'_surveys', db='survey', host='127.0.0.1', port=50000, denovo=True)
        # des = des_from_survey_df(id+'_surveys', db='survey', host='127.0.0.1', port=50000, denovo=True)
        # des = des_from_feather('cache/'+id+'_surveys.feather', denovo=True)
        return cls(cfg=cfg, meta=meta, svy=svytbl, soc=soctbl, des=des)

    def fetch_socrata(self, qn, vars, filt={}):
        sel = None
        df = self.soc
        sel = df['qid'] == qn
        if 'sitecode' in filt.keys():
            sel = sel & df.sitecode.isin(filt['sitecode'])
        if 'year' in filt.keys():
            sel = sel & df.year.isin(filt['year'])
        for v in self.cfg.facets:
            if v in filt.keys():
                sel = sel & df[v].isin(filt[v])
        for v in self.cfg.facets:
            if v not in vars:
                sel = sel & (df[v] == 'Total')
        cols = ['qid', 'response', 'sitecode', 'year'] + \
            self.cfg.facets + STATS_COLUMNS
        dfz = df[sel][cols]
        dfz[STATS_COLUMNS] = dfz[STATS_COLUMNS].apply(
            lambda xf: xf.astype(float).fillna(-1))
        return dfz


    def facets(self):
        return self.cfg.facets

    def facet_levels(self):
        return {k: list(self.meta_db[k]
                        .cat.categories) for k in self.facets}

    def fetch_stats(self, qn, vars=[], filt={}):
        lvls = self.meta.ix[qn]['response'].iloc[0]
        res = mapcat(lambda r: fetch_stats(self.des, qn, r, vars, filt), lvls)
        return pd.concat(res)
