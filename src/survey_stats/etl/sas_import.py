import os
import os.path
import io
import re
import us
import zipfile
import numpy as np
import pandas as pd
import urllib.request
import multiprocessing
from retry import retry
from cytoolz.itertoolz import mapcat
from cytoolz.functoolz import thread_last
from cytoolz.curried import map, filter
import boto3
from botocore import UNSIGNED
from botocore.client import Config


from survey_stats import log
from survey_stats import pdutil

US_STATES_FIPS_INTS = thread_last(
    us.STATES_AND_TERRITORIES,
    map(lambda x: x.fips),
    filter(lambda x: x is not None),
    map(lambda x: int(x)),
    list
)

SITECODE_TRANSLATORS = {
    'fips': lambda x: (us.states.lookup('%.2d' % x).abbr if int(x) in US_STATES_FIPS_INTS else 'NA')
}

SVYDESIGN_COLS = ['sitecode', 'strata', 'psu', 'weight']

logger = log.getLogger()


s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))


def number_of_workers():
    return multiprocessing.cpu_count()-2


def fetch_s3_bytes(url):
    bucket, key = url[5:].split('/', 1)
    logger.info('fetching s3 url', url=url, bucket=bucket, key=key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj['Body']


@retry(tries=5, delay=2, backoff=2, logger=logger)
def fetch_data_from_url(url):
    if os.path.isfile(url):
        return open(url,'r',errors='ignore')
    elif url.startswith('s3://'):
        return fetch_s3_bytes(url)
    else:
        return urllib.request.urlopen(url)


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
        fetch_data_from_url,
        lambda x: x.read(),
        lambda t: (t.decode('utf-8', errors='ignore')
                   if type(t) is bytes else t),
        parse_variable_labels
    )
    logger.info("loading format assignments", file=formas_f)
    assignments = thread_last(
        formas_f,
        fetch_data_from_url,
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
    fh = fetch_data_from_url(url)
    return (load_sas_from_zip(fh, format) if url[-3:].lower() == 'zip'
            else pd.read_sas(fh, format=format))


def force_convert_categorical(s, lbls):
    c = (pd.to_numeric(s.fillna(-1), downcast='integer')
         .replace(to_replace=lbls[s.name])
         .astype('category'))
    #logger.info('forced cat conversion', c=str(c.value_counts(dropna=False)),
    #            c_desc=str(c.describe()))
    return c


def eager_convert_categorical(s, lbls):
    if not s.name in lbls.keys():
        return s
    try:
        c = (pd.to_numeric(s.fillna(-1), downcast='integer')
             .astype('category'))
        #logger.info('eager conv - 1', summ=c.value_counts(dropna=False).to_dict(),
        #            labels=lbls[s.name])
        c = c.cat.rename_categories(
            [lbls[s.name][k] for k in sorted(c.unique())])
        #logger.info('eager conv - 2', summ=c.value_counts(dropna=False).to_dict(),
        #            keys=sorted(lbls[s.name].keys()))
        c = (c.cat.set_categories(
            [lbls[s.name][k] for k in sorted(lbls[s.name].keys())])
            .astype('category'))
        #logger.info('eager conv - 3', summ=c.value_counts(dropna=False).to_dict(),
        #            desc = str(c.describe()))
        return c
    except KeyError:
        return s
    except ValueError as e:
        logger.info('found value err', err=e, c=str(c.value_counts(dropna=False)),
                    c_desc=c.describe())
        return force_convert_categorical(s, lbls)


def find_na_synonyms(df, na_syns):
    df = df.applymap(
        lambda x: np.nan if 
        (x.lower() in na_syns if 
            type(x) == str else 
            False) 
        else x)
    return df
    


def filter_columns(df, r, facets, qids):
    set_union = lambda x,y: y.union(x)
    cols = thread_last(set(qids),
                       (set_union, map(lambda x: r[x], SVYDESIGN_COLS)),
                       (set_union, facets.keys()),
                       lambda x: x.intersection(df.columns),
                       list,
                       sorted)
    ndf = df[cols]
    logger.info("filtered df columns", qids=','.join(qids),
                facets=','.join(facets.keys()),
                fixed=','.join(map(lambda x: r[x], SVYDESIGN_COLS)),
                filtered=','.join(cols),
                missing=set(cols).difference(df.columns),
                ncols=len(cols), old_shape=df.shape, new_shape=ndf.shape)
    return ndf


def load_sas_xport_df(r, p, facets, qids, lbls, na_syns):
    logger.bind(year=r.year)
    df = load_sas_from_url(p+r.xpt, 'xport')
    df.columns = [x.lower() for x in df.columns]
    logger.info("loaded SAS XPORT file", shape=df.shape)
    lbls = {k:v for k,v in lbls.items() if k in df.columns}
    facets = {r[k]:k for k in facets}
    logger.info("loaded SAS XPORT file", shape=df.shape)
    logger.info('filtering, applying varlabels, munging')
    ndf = (filter_columns(df, r, facets, qids)
           .apply(lambda x: eager_convert_categorical(x, lbls))
           .select_dtypes(include=['category'])
           .rename(index=str, columns=facets)
           .assign(year = int(r.year),
                   sitecode = df[r.sitecode].apply(
                        SITECODE_TRANSLATORS['fips']).astype('category'),
                   weight = df[r.weight].astype(float),
                   strata = df[r.strata].astype(int),
                   psu = df[r.psu].astype(int))
    )
    logger.info('completed SAS df munging',
                summary=ndf.dtypes.value_counts(dropna=False).to_dict(),
                shape=ndf.shape, dups=pdutil.duplicated_varnames(df))
    logger.unbind('year')
    return ndf



def process_sas_survey(meta, facets, prefix, qids, na_syns):
    undash_fn = lambda x: 'x' + x if x[0] == '_' else x
    logger.bind(p=prefix)
    flist = pd.DataFrame(meta['rows'], columns=meta['cols'])
    lbls = {r.year: load_variable_labels(prefix + r.formas,
                                         prefix + r.format) for
            idx, r in list(flist.iterrows())}
    dfs = [load_sas_xport_df(r, prefix, facets, qids, lbls[r.year], na_syns) for
        idx, r in list(flist.iterrows())]
    logger.info('merging SAS dfs')
    dfs = (pd.concat(dfs, ignore_index=True)
           .pipe(lambda xf: find_na_synonyms(xf, na_syns))
           .apply(lambda x: x.astype('category') if
                 x.dtype.name in ['O','object'] else x)
           .pipe(lambda xf: xf.rename(index=str, columns={x:undash_fn(x) for x
                                                          in xf.columns})))
    logger.info('merged SAS dfs', shape=dfs.shape,
                 summary=dfs.dtypes.value_counts(dropna=False).to_dict())
    logger.unbind('p')

    return dfs


