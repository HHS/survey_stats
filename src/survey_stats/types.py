import cattr
import attr
import yaml
import numpy as np
import pandas as pd
from cytoolz.dicttoolz import assoc
from cytoolz.functoolz import thread_first
from typing import Optional, Sequence, Callable, TypeVar, Mapping
from survey_stats import log

logger = log.getLogger(__name__)

T = TypeVar('T', np.number,
            np.character, np.bool_,
            str, int, complex, float, bool)

cattr.register_structure_hook(
    pd.DataFrame,
    lambda d, t: pd.DataFrame(d['rows'], columns=d['cols'])
)


@attr.s(slots=True, frozen=True)
class ColumnFilter(object):
    incl: bool = attr.ib()
    vals: Sequence[str] = attr.ib()


@attr.s(slots=True, frozen=True)
class SurveyConfig(object):
    parse_mode: str = attr.ib()
    denovo_strata: bool = attr.ib()
    fpc: Optional[bool] = attr.ib()
    design: str = attr.ib()
    source_url_prefix: str = attr.ib()
    s3_url_prefix: str = attr.ib()
    qids: Sequence[str] = attr.ib()
    meta: pd.DataFrame = attr.ib()
    patch_format: Mapping[str, Mapping[T, T]] = attr.ib()
    na_synonyms: Sequence[str] = attr.ib()
    replace_labels: Mapping[T, T] = attr.ib()
    rename_cols: Optional[Callable[[T], T]] = attr.ib()


@attr.s(slots=True, frozen=True)
class SocrataConfig(object):
    soda_api: Sequence[str] = attr.ib()
    mapcols: Optional[Mapping[str, str]] = attr.ib()
    apply_fn: Optional[Mapping[str, Callable[[T], T]]] = attr.ib()
    mapvals: Optional[Mapping[str, Mapping[T, Callable[[T], T]]]] = attr.ib()
    unstack: Optional[Mapping[str, str]] = attr.ib()
    fold_stats: Optional[Mapping[str, Sequence[str]]] = attr.ib()
    qn_meta: Sequence[str] = attr.ib()
    c_filter: Sequence[str] = attr.ib()


@attr.s(slots=True, frozen=True)
class DatasetConfig(object):
    id: str = attr.ib()
    description: str = attr.ib()
    strata: Sequence[str] = attr.ib()
    facets: Sequence[str] = attr.ib()
    facet_levels: Optional[Mapping[str, Sequence[str]]] = attr.ib()
    questions: Optional[Mapping[str, str]] = attr.ib()
    national: Sequence[ColumnFilter] = attr.ib()
    surveys: Optional[SurveyConfig] = attr.ib()
    socrata: Optional[SocrataConfig] = attr.ib()

    @classmethod
    def from_yaml(cls, yaml_f):
        with open(yaml_f) as fh:
            y = yaml.load(fh)
            if y['surveys']:
                y['surveys']['meta'] = pd.DataFrame(
                    y['surveys']['meta']['rows'],
                    columns=y['surveys']['meta']['cols']
                )
        logger.info('loading cfg')
        cfg = thread_first(
            y,
            (assoc, 'facet_levels', None if 'facet_levels' not in y else y['facet_levels']),
            (assoc, 'questions', None if 'questions' not in y else y['questions']),
            (assoc, 'national', None if not y['national'] else ColumnFilter(**y['national'])),
            (assoc, 'socrata', None if not y['socrata'] else SocrataConfig(**y['socrata'])),
            (assoc, 'surveys', None if not y['surveys'] else SurveyConfig(**y['surveys']))
        )
        return cls(**cfg)
