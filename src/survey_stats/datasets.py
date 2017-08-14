import blaze as bz
import feather
from collections import namedtuple

from survey_stats import log
from survey_stats.survey import AnnotatedSurvey
from survey_stats.serdes import has_feather, load_feather

STATS_COLUMNS = ['count','mean','ci_u','ci_l','se']

logger = log.getLogger()

def resolve_db_url(url):
    return (feather.read_dataframe(url) if
            url.endswith('.feather') else
            bz.data(url))



class SurveyDataset(namedtuple('SurveyDataset',
                               ['svy_db','meta_db', 'cfg'])):

    @classmethod
    def from_db_urls(cls, svy_url, meta_url, cfg):
        return cls(svy_db=resolve_db_url(svy_url),
                   meta_db=resolve_db_url(meta_url), cfg=cfg)


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


