import os
import pandas as pd
import feather
import logging

metacols = ['questioncode','shortquestiontext','description',
			 'greater_risk_question','lesser_risk_question','topic','subtopic']
facets = ['grade','sex','race','sitecode','stratificationtype']
true_stats = ['greater_risk_data_value','greater_risk_high_confidence_limit',.
              'greater_risk_low_confidence_limit', 'lesser_risk_data_value',
              'lesser_risk_high_confident_limit',
              'lesser_risk_low_confidence_limit','sample_size','questioncode']

#META_URL = 'https://chronicdata.cdc.gov/resource/6ay3-nik2.csv'
#META_URL += '?$select={0},count(1)&$group={0}'.format(','.join(META_COLS))
metaurl = 'data/yrbss_dash.csv.gz'

dashdf = None

def fetch_yrbss_meta():
	global dashdf
	cache_url = '{cache_dir}/{fname}.feather'.format(
		cache_dir = os.path.join(os.getcwd(),'cache'),
		fname = os.path.basename(metaurl).split('.')[0]
	)
	logging.info('cache_url: %s' % cache_url)
	dashdf = feather.read_dataframe(cache_url) if \
			os.path.exists(cache_url) else pd.read_csv(metaurl)
	dashdf.columns = dashdf.columns.map(lambda x: x.lower())
	dashdf['questioncode'] = dashdf.questioncode.apply(
		lambda k: k.replace('H','qn') if k[0]=='H' else k.lower()
    dashdf = dashdf.rename(colnames={'locationabbr':'sitecode'})
	m = dashdf[metacols].drop_duplicates().set_index('questioncode')
    dashdf[set(facets).union(true_sats)]
	return m.to_dict(orient='index')

