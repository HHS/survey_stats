import os
import feather as ft
from survey_stats.dbi import DatasetPart
from survey_stats.const import DEFAULT_CACHE_DIR, DBTBL_FMT 

cache_dir = os.path.join(os.getcwd(), DEFAULT_CACHE_DIR)


def surveys_key4id(id):
    return DBTBL_FMT.format(dsid=id, part=DatasetPart.SURVEYS.value)


def socrata_key4id(id):
    return DBTBL_FMT.format(dsid=id, part=DatasetPart.SOCRATA.value)


def metadata_key4id(id):
    return DBTBL_FMT.format(dsid=id, part=DatasetPart.SCHEMA.value)


def f4key(key):
    return os.path.join(cache_dir, key+'.feather')


def csv4key(key):
    return os.path.join(cache_dir, key+'.csv')


def has_feather(k):
    return os.path.isfile(f4key(k))


def load_feather(k):
    return ft.read_dataframe(f4key(k))


def save_feather(k, df):
    of = f4key(k)
    ft.write_dataframe(df, of)
    return of


def save_csv(k, df, **kwargs):
    of = csv4key(k)
    df.to_csv(of, **kwargs)
    return of
