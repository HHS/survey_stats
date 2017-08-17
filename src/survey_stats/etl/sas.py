import os
import os.path
import io
import re

from survey_stats import log

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
    df = (load_sas_from_zip(fh, format) if url[-3:].lower() == 'zip'
            else pd.read_sas(fh, format=format))
    logger.info("loaded SAS XPORT file", shape=df.shape)
    return df


def load_sas_xport_df(r, p, facets, qids, lbls, na_syns):
    logger.bind(year=r.year)
    df = load_sas_from_url(p+r.xpt, 'xport')
    df.columns = [x.lower() for x in df.columns]
    lbls = {k:v for k,v in lbls.items() if k in df.columns}
    facets = {r[k]:k for k in facets}
    logger.unbind('year')
    return munge_df(df, lbls, facets,
                    year=r.year, sitecode=r.sitecode,
                    weight=r.weight, strata=r.strata, psu=r.psu)



def process_sas_survey(meta, facets, prefix, qids, na_syns):
    logger.bind(p=prefix)
    flist = pd.DataFrame(meta['rows'], columns=meta['cols'])
    lbls = {r.year: load_variable_labels(prefix + r.formas,
                                         prefix + r.format) for
            idx, r in list(flist.iterrows())}
    dfs = [load_sas_xport_df(r, prefix, facets, qids, lbls[r.year], na_syns) for
        idx, r in list(flist.iterrows())]
    dfs = merge_multiyear_surveys(dfs, na_syns)
    logger.unbind('p')
    return dfs


