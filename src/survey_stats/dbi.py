import sqlalchemy as sa
import pymonetdb as pmb
import sqlalchemy_monetdb as smb
import blaze as bz
import cattr
import attr
import yaml
import numpy as np
import pandas as pd
from enum import unique, Enum
from cytoolz.dicttoolz import assoc
from cytoolz.functoolz import thread_first
from cattr import typed
from survey_stats.const import DBURI_FMT


@unique
class DatasetPart(Enum):
    SCHEMA = 'schema'
    FACETS = 'facets'
    SURVEYS = 'surveys'
    SOCRATA = 'socrata'


@unique
class DatabaseType(Enum):
    MONETDB = 'monetdb'
    MARIADB = 'mariadb'
    MAPD = 'mapd'


@unique
class DatasetFileType(Enum):
    FEATHER = 'feather'
    PYTABLE = 'pytable'


@attr.s(slots=True, frozen=True)
class DatabaseConfig(object):
    host = typed(str)
    port = typed(int)
    type = typed(DatabaseType)
    user = typed(str)
    password = typed(str)
    name = typed(str)

    @property
    def uri(self):
        ret = DBURI_FMT.format(dbtype=self.type.value, user=self.user,
                               password=self.password, host=self.host,
                               port=self.port, dbname=self.name)
        return ret

    @classmethod
    def from_yaml(cls, yaml_f):
        with open(yaml_f) as fh:
            y = yaml.load(fh)
            return cls(**y)
