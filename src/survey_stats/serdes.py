import os
import feather as ft
from survey_stats.const import *

cache_dir = os.path.join(os.getcwd(), CACHE_DIR)

surveys_key4id = lambda id: id + SURVEYS_SUFFIX
socrata_key4id = lambda id: id + SOCRATA_SUFFIX
metadata_key4id = lambda id: id + METADATA_SUFFIX

f4key = lambda key: os.path.join(cache_dir,key+'.feather')
csv4key = lambda key: os.path.join(cache_dir,key+'.csv')


def has_feather(k):
    return os.path.isfile(f4key(k))


def load_feather(k):
    return ft.read_dataframe(f4key(k))


def save_feather(k, df):
    ft.write_dataframe(df, f4key(k))


def save_csv(k, df, **kwargs):
    df.to_csv(csv4key(k), **kwargs)
