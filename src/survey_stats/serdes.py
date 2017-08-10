import os
import feather

cache_dir = os.path.join(os.getcwd(),'cache')

surveys_key4id = lambda id: id + '_surveys'
socrata_key4id = lambda id: id + '_socrata'
metadata_key4id = lambda id: id + '_metadata'

f4key = lambda key: os.path.join(cache_dir,key+'.feather')
csv4key = lambda key: os.path.join(cache_dir,key+'.csv')


def has_feather(k):
    return os.path.isfile(f4key(k))


def load_feather(k):
    return feather.read_dataframe(f4key(k))


def save_feather(k, df):
    feather.write_dataframe(df, f4key(k))


def save_csv(k, df, **kwargs):
    df.to_csv(csv4key(k), **kwargs)
