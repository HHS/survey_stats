import yaml
import pandas as pd

from survey_stats import log

logger = log.getLogger(__name__)

def get_qids_by_year(soda_api, qnkey):
    url = '?$limit=999999999&' + \
            '$select=year,{qnkey}' + \
            '&$group=year,{qnkey}'
    url = url.format(qnkey=qnkey)
    pass


def get_questions_socrata(soda_api, mapcols):
    revmap = {v: k for k, v in mapcols.items()}
    url = '?$limit=999999999&' + \
            '$select={columns},count(year)' + \
            '&$group={columns}'
    url = url.format(columns=','.join([revmap[k] for k in QNCOLS]))
    sl_res =[]
    sl_res = res[['facet', 'facet_description',
        'facet_level', 'facet_level_value']].drop_duplicates()
    sl_res = {f[0]: {
        'facet':f[0],
        'facet_description': f[1]['facet_description'].get_values()[0],
        'levels': dict(list(f[1][['facet_level','facet_level_value']].to_records(index=False)))
        } for f in sl_res.groupby('facet')}

    qn_res = res[['questionid', 'topic', 'subtopic', 'question', 'response']].groupby('questionid').agg({
        'topic': lambda x: x.head(1).get_values()[0],
        'subtopic': lambda x: x.get_values()[0],
        'question': lambda x: x.get_values()[0],
        'response': lambda x: list(x.drop_duplicates())
    })
    qn_res['class'] = qn_res['topic']
    qn_res['topic'] = qn_res['subtopic']
    del qn_res['subtopic']
    qn_res = qn_res.to_dict(orient='index')
