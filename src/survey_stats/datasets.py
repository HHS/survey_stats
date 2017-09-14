import blaze as bz
import feather
import pandas as pd
import numpy as np
import rpy2
from cytoolz.itertoolz import remove
from cytoolz.curried import map
from cytoolz.functoolz import identity
from cytoolz.dicttoolz import keymap
from collections import namedtuple
from survey_stats import log
from survey_stats.survey import fetch_stats, des_from_survey_db, subset_survey
from survey_stats.survey import fetch_stats_by, fetch_stats_totals, des_from_feather
from survey_stats import pdutil as u
from survey_stats.const import DSFILE_FMT
from survey_stats.types import DatasetConfig
from survey_stats.dbi import DatabaseConfig, DatasetPart, DatasetFileType
from rpy2.robjects import Formula
import attr
import cattr
import datashape
from cattr import typed
from pathlib import Path
from typing import Union, Optional

STATS_COLUMNS = ['mean', 'ci_u', 'ci_l', 'se', 'count', 'sample_size']

logger = log.getLogger()


def resolve_database_table(tbl, dbc):
    ngin = sa.create_engine(dbc.uri)
    db = bz.data(ngin)
    t = db[tbl]
    nrow = t.count()
    shp = datashape.dshape(str(t.dshape).replace('var', str(nrow)))
    return bz.data(t, dshape=shp)


def get_datafile_path(dsid, part, cdir):
    return os.path.join(cdir,
                        DSFILE_FMT.format(dsid=dsid, part=part, 
                                          type=DatasetFileType.FEATHER))


def map_with_dict(d, val):
    repl_f = lambda x: d[x] if x in d else x
    typ = type(val)
    if typ == str:
        return repl_f(val)
    if typ == list or typ == set:
        return typ(map(repl_f, val))
    if typ == dict:
        return keymap(repl_f, val)


@attr.s(slots=True, frozen=True)
class SurveyMeta(object):
    
    qns = typed(pd.DataFrame)
    facets = typed(pd.DataFrame)

    @classmethod
    def load_metadata(cls, cfg):
        dsid = cfg.id
        qn_f = get_datafile_path(dsid, DatasetPart.SCHEMA)
        qns = feather.read_dataframe(qn_f)
        qns.index = qns.qid
        facets_f = dbc.get_filepath(dsid, DatasetPart.FACETS)
        facets = feather.read_dataframe(facets_f)
        return cls(qns=qns, facets=facets)


@attr.s(slots=True, frozen=True)
class SurveyDataset(object):

    cfg = typed(DatasetConfig)
    dbc = typed(Optional[DatabaseConfig])
    cdir = typed(Path)
    meta = typed(SurveyMeta)
    soc = typed(Optional[bz.interactive._Data])
    svy = typed(Optional[bz.interactive._Data])
    des = typed(Optional[rpy2.robjects.vectors.ListVector])

    @classmethod
    def load_dataset(cls, cfg_f, dbc, cdir):
        # given a config file and blaze data handle,
        # work some magic
        cfg = DatabaseConfig.from_yaml(cfg_f) 
        id = cfg.id
        meta = SurveyMeta.load_metadata(cfg)
        svytbl = dbc[TMPL_SVYTBL.format(id=id)]
        soctbl = resolve_db_url(TMPL_SOCFTH.format(id=id))
        logger.info('set up urls for svytbl, soctbl', id)
        # des = des_from_survey_db(id+'_surveys', db='survey', host='127.0.0.1', port=50000, denovo=True)
        # year is a reserved keyword in monetdb so work around
        # mapper = curry(map_with_dict)({'year':'yr'})
        # des = des_from_survey_df(id+'_surveys', db='survey', host='127.0.0.1', port=50000, denovo=True)
        des = des_from_feather('cache/'+id+'_surveys.feather', denovo=cfg.surveys.denovo_strata)
        mapper = identity
        return cls(cfg=cfg, dbc=dbc, cdir=cdir, meta=meta, svy=svytbl, soc=soctbl, des=des, mapper=mapper)

    def fetch_socrata(self, qn, vars, filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        sel = None
        df = self.soc
        fcts = list(set(self.cfg.facets).intersection(df.columns))
        sel = df['qid'] == qn
        if 'sitecode' in filt.keys():
            sel = sel & df.sitecode.isin(filt['sitecode'])
        elif 'sitecode' not in vars:
            sel = sel & (df['sitecode'] == 'XX')
        if 'year' in filt.keys():
            sel = sel & df.year.isin(filt['year'])
        elif 'year' not in vars:
            sel = sel & (df['year'] == 'Total')
        for v in fcts:
            if v in filt.keys():
                sel = sel & df[v].isin(filt[v])
            elif v not in vars:
                sel = sel & (df[v] == 'Total')
        cols = set(['qid', 'response', 'sitecode', 'year']).union(vars).union(STATS_COLUMNS).intersection(df.columns)
        cols = list(cols)
        dfz = df[sel][cols]
        stats_sub = list(set(STATS_COLUMNS).intersection(dfz.columns))
        dfz[stats_sub] = dfz[stats_sub].apply(
            lambda xf: xf.astype(float).replace(-1.0, np.nan))
        # logger.info('done filtering, replacing NaNs', dfz=dfz)
        return u.fill_none(dfz.reset_index(drop=True))

    def facets(self):
        return self.cfg.facets

    def facet_levels(self):
        return {k: list(self.meta_db[k]
                        .cat.categories) for k in self.facets}

    def responses_for_qn(self, qn):
        return remove(lambda x: x[0] is None,
                      self.svy[qn].distinct())

    def fetch_stats(self, qn, vars=[], filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        lvls = self.responses_for_qn(qn)
        res = map(lambda r: fetch_stats(self.des, qn, r, vars, filt), lvls)
        dfz = pd.concat(res, ignore_index=True)
        return dfz

    def fetch_stats_for_slice(self, qn, r, vars=[], filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        qn_f = Formula('~I(%s=="%s")' % (qn, r))
        logger.info('subsetting des with filter', filt=filt)
        des = subset_survey(self.des, filt)
        ret = None
        if len(vars) > 0:
            logger.info('fetching stats with var levels', vs=vars, qn=qn, r=r)
            ret = fetch_stats_by(des, qn_f, r, vars)
        else:
            logger.info('fetching top level stats', qn=qn, r=r)
            ret = fetch_stats_totals(des, qn_f, r)
        ret = ret.assign(sample_size=None, count=None)
        return ret

    def generate_slices(self, qn, vars=[], filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        resps = self.responses_for_qn(qn)
        vlvls = [vars[:k+1] for k in range(len(vars))]
        res = []
        d = self.cfg.id
        for r in resps:
            top = [{'d': d, 'q': qn, 'r': r[0], 'f': filt, 'vs': []}]
            rs = [{'d': d, 'q': qn, 'r': r[0], 'f': filt, 'vs': vs} for vs in vlvls]
            res = res + rs + top
        logger.info(res)
        return res
