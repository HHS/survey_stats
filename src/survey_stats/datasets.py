import os
import blaze as bz
from odo import odo
import feather
import pandas as pd
import numpy as np
import rpy2
import sqlalchemy as sa
from rpy2.robjects import Formula
import types
import attr
import datashape
from cattr import typed
from pathlib import Path
from typing import Union, Optional
from cytoolz.itertoolz import remove
from cytoolz.curried import map, curry
from cytoolz.functoolz import identity
from cytoolz.dicttoolz import keymap
from survey_stats import log
from survey_stats.survey import fetch_stats, des_from_survey_db, subset_survey
from survey_stats.survey import fetch_stats_by, fetch_stats_totals, des_from_feather
from survey_stats import pdutil as u
from survey_stats.const import DSFILE_FMT, DBTBL_FMT
from survey_stats.types import DatasetConfig
from survey_stats.dbi import DatabaseConfig, DatasetPart, DatasetFileType
from survey_stats.const import DECIMALS

STATS_COLUMNS = ['mean', 'ci_u', 'ci_l', 'se', 'count', 'sample_size']

logger = log.getLogger()


def resolve_database_table(dsid, part, dbc):
    tbl = DBTBL_FMT.format(dsid=dsid, part=part.value)
    ngin = sa.create_engine(dbc.uri)
    db = bz.data(ngin)
    t = db[tbl]
    nrow = t.count()
    shp = datashape.dshape(str(t.dshape).replace('var', str(int(nrow))))
    return t  #bz.data(t, dshape=shp)


def get_datafile_path(dsid, part, cdir):
    return os.path.join(cdir,
                        DSFILE_FMT.format(dsid=dsid, part=part.value, 
                                          type=DatasetFileType.FEATHER.value))


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
    def load_metadata(cls, cfg, cdir):
        dsid = cfg.id
        qn_f = get_datafile_path(dsid, DatasetPart.SCHEMA, cdir)
        qns = feather.read_dataframe(qn_f)
        qns.index = qns.qid
        facets_f = get_datafile_path(dsid, DatasetPart.FACETS, cdir)
        facets = feather.read_dataframe(facets_f)
        return cls(qns=qns, facets=facets)


@attr.s(slots=True, frozen=True)
class SurveyDataset(object):

    dsid = typed(str)
    cfg = typed(DatasetConfig)
    dbc = typed(Optional[DatabaseConfig])
    cdir = typed(Path)
    meta = typed(SurveyMeta)
    soc = typed(Optional[bz.interactive._Data])
    svy = typed(Optional[bz.interactive._Data])
    des = typed(Optional[rpy2.robjects.vectors.ListVector])
    mapper = typed(Optional[Union[types.FunctionType,types.LambdaType]])

    @classmethod
    def load_dataset(cls, cfg_f, dbc, cdir, init_des=False):
        # given a config file and blaze data handle,
        # work some magic
        cfg = DatasetConfig.from_yaml(cfg_f)
        dsid = cfg.id
        meta = SurveyMeta.load_metadata(cfg, cdir)
        use_db = False  # True if dbc is not None else False 
        if use_db:
            svytbl = resolve_database_table(dsid, DatasetPart.SURVEYS, dbc) 
            soctbl = resolve_database_table(dsid, DatasetPart.SOCRATA, dbc) 
            # year is a reserved keyword in monetdb so work around
            mapper = curry(map_with_dict)({'year':'yr'})
            tbl = DBTBL_FMT.format(dsid=dsid, part=DatasetPart.SURVEYS.value)
            des = des_from_survey_db(tbl, db=dbc.name, host=dbc.host, port=dbc.port, denovo=cfg.surveys.denovo_strata) if init_des else None
        else:
            svytbl = bz.data(feather.read_dataframe(get_datafile_path(dsid, DatasetPart.SURVEYS, cdir)))
            soctbl = bz.data(feather.read_dataframe(get_datafile_path(dsid, DatasetPart.SOCRATA, cdir)))
            mapper = identity
            des = des_from_feather(get_datafile_path(dsid, DatasetPart.SURVEYS, cdir), denovo=True) if init_des else None
        return cls(dsid=dsid, cfg=cfg, dbc=dbc, cdir=cdir, meta=meta, svy=svytbl, soc=soctbl, des=des, mapper=mapper)

    def fetch_socrata(self, qn, vars, filt={}):
        vars = self.mapper(vars)
        filt = self.mapper(filt)
        sel = None
        df = self.soc
        fcts = list(set(self.cfg.facets).intersection(df.fields))
        sel = df['qid'] == qn
        site_col = self.mapper('sitecode')
        year_col = self.mapper('year')
        if site_col in filt.keys():
            sel = sel & df[site_col].isin(filt[site_col])
        elif site_col not in vars:
            sel = sel & (df[site_col] == 'XX')
        if year_col in filt.keys():
            sel = sel & df[year_col].isin(filt[year_col])
        elif year_col not in vars:
            sel = sel & (df[year_col] == 'Total')
        for v in fcts:
            if v in filt.keys():
                sel = sel & df[v].isin(filt[v])
            elif v not in vars:
                sel = sel & (df[v] == 'Total')
        cols = set(['qid', 'response', 'sitecode', 'year']).union(vars).union(STATS_COLUMNS).intersection(df.fields)
        cols = list(cols)
        dfz = odo(df[sel][cols], pd.DataFrame)
        stats_sub = list(set(STATS_COLUMNS).intersection(dfz.columns))
        dfz[stats_sub] = dfz[stats_sub].apply(
            lambda xf: xf.astype(float).replace(-1.0, np.nan)
        )
        # logger.info('done filtering, replacing NaNs', dfz=dfz)
        return u.fill_none(dfz.round(DECIMALS).reset_index(drop=True))

    def facets(self):
        return self.cfg.facets

    def facet_levels(self):
        return {k: list(self.meta_db[k]
                        .cat.categories) for k in self.facets}

    def responses_for_qn(self, qn):
        r = odo(self.svy[qn].distinct(), pd.DataFrame)
        return list(r.dropna()[qn])

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
        logger.info('mapping slices over resps', r=resps)
        for r in resps:
            top = [{'d': d, 'q': qn, 'r': r, 'f': filt, 'vs': []}]
            rs = [{'d': d, 'q': qn, 'r': r, 'f': filt, 'vs': vs} for vs in vlvls]
            res = res + rs + top
        logger.info(res)
        return res
