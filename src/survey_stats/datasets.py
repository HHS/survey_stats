import blaze as bz
import yaml
import feather
from collections import namedtuple

from survey_stats import log
from survey_stats.serdes import has_feather, load_feather
from survey_stats.survey import des_from_feather, des_from_survey_db

STATS_COLUMNS = ['count', 'mean', 'ci_u', 'ci_l', 'se']

logger = log.getLogger()


def resolve_db_url(url):
    return (feather.read_dataframe(url) if
            url.endswith('.feather') else
            bz.data(url))



class SurveyDataset(namedtuple('SurveyDataset',
                               ['svy','meta', 'cfg'])):


    @classmethod
    def load_dataset(cls, cfg_f):
        cfg = None
        with open(cfg_f) as fh:
            cfg = yaml.load(fh)


    @classmethod
    def from_db_urls(cls, svy_url, meta_url, cfg):
        return cls(svy=resolve_db_url(svy_url),
                   meta=resolve_db_url(meta_url), cfg=cfg)


    @classmethod
    def from_feather_files(cls, svy_f, meta_f, cfg):
        return cls(svy=des_from_feather(svy_f), meta=load_feather(metaf))



    def fetch_socrata(self, qn, vars, filt = {}):
        sel = df.qid == qn
        if 'sitecode' in filt.keys():
            sel = sel & df.sitecode.isin(filt['sitecode'])
        if 'year' in filt.keys():
            sel = sel & df.year.isin(map( int, filt['year']))
        for v in self.facets.keys():
            if v in filt.keys():
                sel = sel & df[v].isin(filt[v])
            if not v in vars:
                sel = sel & (df[v] == 'Total')
        cols = ['qid','response','sitecode','year'] + \
                self.facets + STATS_COLUMNS
        return df.to_dict(orient='records')


    def facets(self):
        return self.cfg['facets']


    def facet_levels(self):
        return {k: list(self.meta_db[k]
                        .cat.categories) for k in self.facets}


