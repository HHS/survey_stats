import os
import io
import re
import us
import sys
import tempfile
import feather
import logging
import requests
import zipfile
import traceback
import dask
import dask.dataframe as dd
import dask.delayed
from dask.delayed import delayed
import numpy as np
import pandas as pd
import urllib.request
import multiprocessing
from retry import retry
from cytoolz import curry
from cytoolz.itertoolz import concat, concatv, mapcat
from cytoolz.functoolz import thread_last, thread_first, flip, do, compose
from cytoolz.curried import map, filter, reduce

from survey_stats import log

US_STATES_FIPS_INTS = thread_last(
    us.STATES_AND_TERRITORIES,
    map(lambda x: x.fips),
    filter(lambda x: x is not None),
    map(lambda x: int(x)),
    list
)

WEIGHTING_COLS = {
    'weight': 'weight_col',
    'psu': 'psu_col',
    'strata': 'strata_col'
}

SAMPLING_COLS = {
    'year': 'year_col',
    'sitecode': 'sitecode_col'
}

logger = log.getLogger()

def number_of_workers():
    return multiprocessing.cpu_count()-2

def parse_format_assignments(formas_f, remote_url=True):
    fh = formas_f
    if remote_url:
        r = requests.get(formas_f)
        fh = r.iter_lines(decode_unicode=True)
    format_lines = ''
    append = False
    for line in fh:
        # lowercase, trim off comments and whitespace
        l = re.split('\/?\*', line.lower())[0].strip()
        if line.strip().endswith(';'):
            # make sure we don't lose terminating semicolons
            l += ';'
        if not append and l.startswith('format'):
            # begin collecting format lines
            append = True
            format_lines += l.replace('format','',1) + ' '
            continue
        if append and l.endswith(';'):
            # stop collecting format lines
            format_lines += l.replace(';','')
            append = False
            break
        if append:
            # add format info line
            format_lines += l + ' '
            continue
    assignments = thread_last(
        format_lines.split('.'), # assignment set ends with fmt + dot
        map(lambda x: x.split()), # break out vars and format
        (mapcat, lambda y: [(k, y[-1]) for k in y]), # tuple of var, fmt
        dict
    )
    return assignments

def block2dict(lines):
    d = thread_last(
        lines,
        map(lambda x: x.strip().replace('"','').replace("'","").split('=')),
        map(lambda x: (x[0].strip().replace(' ',''),
                       x[1].strip().replace('\x92',"'").replace(',',''))),
        filter(lambda x: x[0].find('-') == -1),
        (mapcat, lambda x: map(lambda y: (y, x[1]), x[0].split(','))),
        filter(lambda x: x[0].isnumeric()),
        map(lambda x: (int(x[0]), x[1])),
        dict
    )
    d[-1] = "NA"
    return d


def parse_variable_labels(labels_f, remote_url = True):
    fh = labels_f
    if remote_url:
        r = requests.get(labels_f)
        fh = r.text
    labels = thread_last(
        fh.split(';'),
        map(lambda x: re.split('\/?\*', x)[0].strip()),
        filter(lambda x: x.lower().startswith('value')),
        map(lambda x: x.split('\n')),
        map(lambda x: (x[0].split()[1].lower(), block2dict(x[1:]))),
        dict
    )
    return labels

def load_variable_labels( formas_f, format_f, as_dataframe=False):
    logger.info("loading format labels", file=format_f)
    labels = parse_variable_labels(format_f)
    logger.info("loading format assignments", file=formas_f)
    assignments = parse_format_assignments(formas_f)
    if as_dataframe:
        df = pd.concat([
            (pd.DataFrame(
                list(labels[v].items()),
                columns=['code','label'])
            .assign(var=k, year=int(row['year']))
            ) for
            k, v in assignments.items() if v in labels
        ])
        return (df.assign(code = df['code'].astype(int),
                          var = df['var'].astype('str'),
                          label = df['label'].astype('category'))
                .set_index(['var','year','code']))
    else:
        return {k: labels[v] for k, v in assignments.items() if v in labels}

def get_sitecode(src, type):
    if type == 'fips':
        return src.apply(lambda x: us.states.lookup( '%.2d' % x ).abbr if
                        int(x) in US_STATES_FIPS_INTS else None).astype(str)
    else:
        raise KeyError('Only fips is supported for sitecode type.')

@retry(tries=3, delay=5, backoff=2)
def load_sas_from_remote_zip(url, format):
    with zipfile.ZipFile( io.BytesIO(
        urllib.request.urlopen(url).read() )) as zipf:
        with zipf.open(zipf.namelist()[0]) as fh:
            return pd.read_sas(fh, format=format)

def eager_convert_categorical(s, lbls):
    if not (s.name in lbls.keys() and
            set(s).issubset(lbls[s.name].keys())):
        return s
    try:
        s = (pd.to_numeric(s.fillna(-1), downcast='integer')
             .astype('category')
             .cat.rename_categories(
                  [lbls[s.name][k] for k in sorted(s.unique())])
             .cat.set_categories(
                 [lbls[s.name][k] for k in sorted(lbls[s.name].keys())])
             )
    except:
        return s

def load_sas_xport_df( row ):
    logger.info("loading SAS annotation files")
    logger.bind(year=row['year'])
    lbls = load_variable_labels( row['formas'], row['format'] )
    logger.info("loading SAS XPORT file", file=row['xpt'])
    df = load_sas_from_remote_zip(row['xpt'], 'xport')
    df = df.rename(columns={ x:x.lower() for x in df.columns})
    logger.info("%s: loaded SAS export file with %d rows, %d cols" %
                (row['year'], df.shape[0], df.shape[1]))
    lbls = {k:v for k,v in lbls.items() if k in df.columns}
    logger.info('summarized column values',
                summary=df.dtypes.value_counts().to_dict())
    logger.info('translating codes to labels')
    df = (df.head(1000).select_dtypes(include=[int,float])
            .apply(lambda x: eager_convert_categorical(x, lbls))
            .select_dtypes(include=['category'])
            .assign(year = int(row['year']),
                  sitecode = (get_sitecode(df[row['sitecode_col']],
                                           'fips')).astype('category'),
                  weight = df[row['weight_col']].astype(float),
                  strata = df[row['strata_col']].astype(int),
                  psu = df[row['psu_col']].astype(int)))
    logger.unbind('year')
    return df


def process_dataset(f):
    flist = pd.read_csv(f, comment='#')
    dfs = [load_sas_xport_df(r) for idx, r in list(flist.iterrows())]
    logger.info('merging dataframes')
    dfs = (pd.concat(dfs, ignore_index=True)
           .apply(lambda x: (x.fillna(np.nan)
                             .astype('category')) if
                  x.dtype.name in ['category','object'] else x))
    dfs.columns = [ re.sub(r'^_','',x) for x in dfs.columns ]
    logger.info('finished merging dataframes', shape=dfs.shape, summary=dfs.dtypes.value_counts())
    feather.write_dataframe(dfs, 'test.feather')

if __name__ == '__main__':
    from dask.distributed import Executor, Client
    f = '~/dev/semanticbits/survey_stats/data/brfss/annual_survey_files.csv'
    #client = Client('127.0.0.1:8786')
    process_dataset(f)



