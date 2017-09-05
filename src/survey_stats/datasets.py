import blaze as bz
from odo import odo
import feather
import json
import pandas as pd
from cytoolz.itertoolz import mapcat
from cytoolz.curried import map, curry
from cytoolz.functoolz import identity
from cytoolz.dicttoolz import keymap
from collections import namedtuple
from survey_stats import log
from survey_stats.types import load_config_from_yaml
from survey_stats.survey import fetch_stats, des_from_survey_db, subset_survey
from survey_stats.survey import fetch_stats_by, fetch_stats_totals, des_from_feather
from dask import delayed
from rpy2.robjects import Formula

TMPL_METAF = 'cache/{id}.schema.json'
TMPL_SOCTBL = '{id}_socrata'
TMPL_SVYTBL = '{id}_surveys'
TMPL_SVYFTH = 'cache/{id}_surveys.feather'
TMPL_SOCFTH = 'cache/{id}_socrata.feather'


STATS_COLUMNS = ['mean', 'ci_u', 'ci_l', 'std_err']

logger = log.getLogger()


def resolve_db_url(url):
    return (feather.read_dataframe(url) if
            url.endswith('.feather') else
            bz.data(url))


def map_with_dict(d, val):
    repl_f = lambda x: d[x] if x in d else x
    typ = type(val)
    if typ == str:
        return repl_f(val)
    if typ == list or typ == set:
        return typ(map(repl_f, val))
    if typ == dict:
        return keymap(repl_f, val)
        

class SurveyDataset(namedtuple('SurveyDataset',
                               ['cfg', 'meta', 'soc', 'svy', 'des', 'mapper'])):
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
        # des = des_from_survey_db(id+'_surveys', db='survey', host='127.0.0.1', port=50000, denovo=True)
        # year is a reserved keyword in monetdb so work around
        # mapper = curry(map_with_dict)({'year':'yr'})
        # des = des_from_survey_df(id+'_surveys', db='survey', host='127.0.0.1', port=50000, denovo=True)
        des = des_from_feather('cache/'+id+'_surveys.feather', denovo=True)
        mapper = identity
        return cls(cfg=cfg, meta=meta, svy=svytbl, soc=soctbl, des=des, mapper=mapper)

    def fetch_socrata(self, qn, vars, filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        if self.mapper:
            vars = map_vars(vars)
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
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        lvls = self.meta.ix[qn]['response'].iloc[0]
        res = map(lambda r: fetch_stats(self.des, qn, r, vars, filt), lvls)
        dfz = pd.concat(res)
        return dfz # .compute()
    
    def fetch_stats_for_slice(self, qn, r, vars=[], filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        qn_f = Formula('~I(%s=="%s")' % (qn, r))
        logger.info('subsetting des with filter', filt=filt)
        des = subset_survey(self.des, filt)
        if len(vars) > 0:
            logger.info('fetching stats with var levels', vs=vars, qn=qn, r=r)
            return fetch_stats_by(des, qn_f, r, vars)
        else:
            logger.info('fetching top level stats', qn=qn, r=r)
            return fetch_stats_totals(des, qn_f, r)

    def generate_slices(self, qn, vars=[], filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        resps = self.meta.ix[qn]['response'].iloc[0]
        vlvls = [vars[:k+1] for k in range(len(vars))]
        res = []
        d = self.cfg.id
        for r in resps:
            top = [{'d': d, 'q': qn,'r': r, 'f':filt, 'vs':[]}]
            rs = [{'d': d, 'q': qn, 'r':r, 'f': filt, 'vs': vs} for vs in vlvls]
            res = res + top + rs
        logger.info(res)
        return res
