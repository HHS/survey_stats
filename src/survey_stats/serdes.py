import os
import feather as ft
from survey_stats.const import SURVEYS_SUFFIX, SOCRATA_SUFFIX, METADATA_SUFFIX
from survey_stats.const import CACHE_DIR


cache_dir = os.path.join(os.getcwd(), CACHE_DIR)


def surveys_key4id(id):
    return id + SURVEYS_SUFFIX


def socrata_key4id(id):
    return id + SOCRATA_SUFFIX


def metadata_key4id(id):
    return id + METADATA_SUFFIX


def f4key(key):
    return os.path.join(cache_dir, key+'.feather')


def csv4key(key):
    return os.path.join(cache_dir, key+'.csv')


def has_feather(k):
    return os.path.isfile(f4key(k))


def load_feather(k):
    return ft.read_dataframe(f4key(k))


def save_feather(k, df):
    ft.write_dataframe(df, f4key(k))


def save_csv(k, df, **kwargs):
    df.to_csv(csv4key(k), **kwargs)
