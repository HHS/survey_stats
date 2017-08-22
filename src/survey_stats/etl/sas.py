import os
import os.path
import io
import re
from collections import namedtuple
import pandas as pd
import numpy as np
from cytoolz.itertoolz import concat, concatv, mapcat
from cytoolz.curried import map, filter, curry
from cytoolz.functoolz import pipe, thread_first, thread_last
import dask
from dask import distributed as dd
from dask import delayed
from dask import bag
from dask.distributed import Client


from survey_stats import log
from survey_stats.etl import survey_df as sdf
from survey_stats.etl import download as dl

logger = log.getLogger(__name__)

def parse_format_assignments(txt):
    format_lines = ''
    append = False
    for line in txt.split('\n'):
        # lowercase, trim off comments and whitespace
        l = re.split('\/?\*', line.lower())[0].strip()
        if line.strip().endswith(';'):
            # make sure we don't lose terminating semicolons
            l += ';'
        elif not append and l.startswith('format'):
            # begin collecting format lines
            append = True
            format_lines += l.replace('format','',1) + ' '
            continue
        elif append and l.endswith(';'):
            # stop collecting format lines
            format_lines += l.replace(';','')
            append = False
            break
        elif append:
            # add format info line
            format_lines += l + ' '
            continue
        else:
            pass

    assignments = thread_last(
        format_lines.split('.'),  # assignment set ends with fmt + dot
        map(lambda x: x.split()),  # break out vars and format
        (mapcat, lambda y: [(k, y[-1]) for k in y]), # tuple of var, fmt
        dict
    )
    return assignments

def block2dict(lines):
    rqt = re.compile(r'[\"]')  # match quote chars
    rws = re.compile(r'\s')        # match whitespace
    # keep only alnum and a few unreserved symbols
    ruri = re.compile(r'(?![\w\s\-\_\.\'\-\+\(\)\/]|\.).')
    d = thread_last(
        lines,
        map(lambda x: x.replace('\x92',"'")),
        map(lambda x: rqt.sub('',x.strip()).split('=')),
        map(lambda x: (rws.sub('', x[0].strip()), ruri.sub('', x[1].strip()))),
        filter(lambda x: x[0].find('-') == -1), # no support for ranges
        (mapcat, lambda x: map(lambda y: (y, x[1]), x[0].split(','))),
        filter(lambda x: x[0].isnumeric()), # remox[1]e non-numeric codes
        map(lambda x: (int(x[0]), x[1])), # cat codes will be ints
        dict
    )
    d[-1] = 'NA' #use NA as a marker for unmapped vals
    return d


def parse_variable_labels(txt):
    labels = thread_last(
        txt.split(';'),
        filter(lambda x: x.strip().lower().startswith('value')),
        map(lambda x: x.strip().split('\n')),
        map(lambda x: (x[0].split()[1].lower(), block2dict(x[1:]))),
        dict
    )
    logger.info('parsed varlabels from format txt',
                nlabeled=len(labels.keys()))
    return labels


def load_variable_labels(formas_f, format_f, year=None):
    logger.info("loading format labels", file=format_f)
    labels = thread_last(
        format_f,
        dl.fetch_data_from_url,
        lambda x: x.read(),
        lambda t: (t.decode('utf-8', errors='ignore')
                   if type(t) is bytes else t),
        parse_variable_labels
    )
    logger.info("loading format assignments", file=formas_f)
    assignments = thread_last(
        formas_f,
        dl.fetch_data_from_url,
        lambda x: x.read(),
        lambda t: (t.decode('utf-8', errors='ignore')
                   if type(t) is bytes else t),
        parse_format_assignments
    )
    return {k: labels[v] for k, v in assignments.items() if v in labels}


def varlabels2df(vlbls, yr=None):
    return thread_last(
        vlbls.items(),
        map(lambda k,v: pd.DataFrame({'code': list(v.keys()),
                                      'label': list(v.values()),
                                      'var': k})),
        map(lambda df: df.assign(year=yr) if yr else df),
        pd.concat,
        lambda df: (df.set_index(['var','year','code'])
                    if yr else df.set_index(['var','code']))
    )


def load_sas_from_zip(fh, format):
    with zipfile.ZipFile( io.BytesIO(fh.read())) as zipf:
        with zipf.open(zipf.namelist()[0]) as fh:
            return pd.read_sas(fh, format=format)


def load_sas_from_url(url, format):
    fh = dl.fetch_data_from_url(url)
    df = (load_sas_from_zip(fh, format) if url[-3:].lower() == 'zip'
            else pd.read_sas(fh, format=format))
    logger.info("loaded SAS XPORT file", shape=df.shape)
    return df

def load_sas_xport_df(url):
    df = load_sas_from_url(url, 'xport')
    df.columns = [x.lower() for x in df.columns]
    return df

IndexedRow = namedtuple('IndexedRow', ['i','r'])

def process_sas_survey(meta, facets, prefix, qids, na_syns, client=None):
    logger.bind(p=prefix)
    flist = pd.DataFrame(meta['rows'], columns=meta['cols'])
    fz = [IndexedRow(idx,r) for idx, r in list(flist.iterrows())]
    lbls = {ir.r.year: load_variable_labels(prefix + ir.r.formas,
                                            prefix + ir.r.format) for ir in fz}
    df_munger = curry(sdf.munge_df)(facets=facets,qids=qids,na_syns=na_syns)
    dfs = [delayed(load_sas_xport_df)(url=prefix+ir.r.xpt) for ir in fz]
    rdfs = dask.persist(dfs)
    munge_fns = [df_munger(r=ir.r, lbls=load_variable_labels(prefix + ir.r.formas,
                                                             prefix + ir.r.format)) for ir in fz]
    logger.info('pulling out columns', qids=qids, facets=facets, cols=dfs[0].columns.compute())
    mdfs = [delayed(munge_fn)(df=df) for df, munge_fn in zip(dfs, munge_fns)]
    logger.info('merging SAS dfs')
    mdfs = delayed(pd.concat)(mdfs, ignore_index=True)
    rdfs = dask.persist(mdfs)
    scols = dfs.columns.intersection(qids+facets).compute()
    logger.info('pulling out columns', qids=qids, facets=facets, cols=dfs.columns.compute())
    scols = list(scols)
    logger.info('re-filtering question and facet columns to cast to category dtype', cols=scols)
    dfz = (mdfs[scols].astype('category')
           .reset_index(drop=True)
           .assign(year = dfs['year'].astype(int),
                   sitecode = dfs['sitecode'].astype('category'),
                   weight = dfs['weight'].astype(float),
                   strata = dfs['strata'].astype(int, errors='ignore'),
                   psu = dfs['psu'].astype(int, errors='ignore')))
    dfz.visualize()
    logger.info('merged SAS dfs')
    logger.unbind('p')
    # TODO: expand parallelism to include writing to feather and db
    return dfz.compute()


