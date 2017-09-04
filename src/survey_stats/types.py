import cattr
import attr
import yaml
import numpy as np
import pandas as pd
from cytoolz.dicttoolz import assoc
from cytoolz.functoolz import thread_first
from cattr import typed
from typing import Optional, Sequence, Callable, TypeVar, Mapping

T = TypeVar('T', np.number,
            np.character, np.bool_,
            str, int, complex, float, bool)

cattr.register_structure_hook(
    pd.DataFrame,
    lambda d, t: pd.DataFrame(d['rows'], columns=d['cols'])
)


@attr.s(slots=True, frozen=True)
class SurveyConfig(object):
    source_url_prefix = typed(str)
    s3_url_prefix = typed(str)
    qids = typed(Sequence[str])
    meta = typed(pd.DataFrame)
    patch_format = typed(Mapping[str, Mapping[T, T]])
    na_synonyms = typed(Sequence[str])
    replace_labels = typed(Mapping[T, T])
    rename_cols = typed(Optional[Callable[[T], T]])


@attr.s(slots=True, frozen=True)
class SocrataConfig(object):
    soda_api = typed(Sequence[str])
    mapcols = typed(Optional[Mapping[str, str]])
    apply_fn = typed(Optional[Mapping[str, Callable[[T], T]]])
    mapvals = typed(Optional[Mapping[str, Mapping[T, Callable[[T], T]]]])
    unstack = typed(Optional[Mapping[str, str]])
    fold_stats = typed(Optional[Mapping[str, Sequence[str]]])
    qn_meta = typed(Sequence[str])
    c_filter = typed(Sequence[str])


@attr.s(slots=True, frozen=True)
class DatasetConfig(object):
    id = typed(str)
    description = typed(str)
    facets = typed(Sequence[str])
    surveys = typed(SurveyConfig)
    socrata = typed(SocrataConfig)


def load_config_from_yaml(yaml_f):
    with open(yaml_f) as fh:
        y = yaml.load(fh)
        y['surveys']['meta'] = pd.DataFrame(
            y['surveys']['meta']['rows'],
            columns=y['surveys']['meta']['cols']
        )
    cfg = thread_first(
        y,
        (assoc, 'socrata', SocrataConfig(**y['socrata'])),
        (assoc, 'surveys', SurveyConfig(**y['surveys']))
    )
    return DatasetConfig(**cfg)
