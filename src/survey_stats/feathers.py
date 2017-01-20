import os
import feather


cache_dir = os.path.join(os.getcwd(),'cache')


def has_feather(key):
    f = os.path.join(cache_dir, key+'.feather')
    return os.path.isfile(f)


def load_feather(key):
    f = os.path.join(cache_dir, key+'.feather')
    return feather.read_dataframe(f)


def save_feather(key, df):
    f = os.path.join(cache_dir, key+'.feather')
    feather.write_dataframe(df, f)
