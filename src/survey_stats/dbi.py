import os
import sqlalchemy as sa
import blaze as bz
import attr
import yaml
from enum import unique, Enum
from cattr import typed
from survey_stats.const import DBURI_FMT, DSFILE_FMT
from datashape import datashape


@unique
class DatasetPart(Enum):
    SCHEMA = 'schema'
    FACETS = 'facets'
    SURVEYS = 'surveys'
    SOCRATA = 'socrata'
    SURVEYS_META = 'surveys_meta'


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

    def resolve_table(self, tbl):
        ngin = sa.create_engine(self.uri)
        db = bz.data(ngin)
        t = db[tbl]
        nrow = t.count()
        shp = datashape.dshape(str(t.dshape).replace('var', str(int(nrow))))
        return bz.data(t, dshape=shp)


def get_datafile_path(part, dsid, cdir):
    return os.path.join(cdir,
                        DSFILE_FMT.format(
                            dsid=dsid,
                            part=part,
                            type=DatasetFileType.FEATHER.value
                        ))
