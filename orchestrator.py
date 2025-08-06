from typing import ClassVar, Callable, Dict, List, Sequence, Set
from pydantic import BaseModel

import pandas as pd

from metrics.models.country_database import Country, CountryManager
from metrics.models.basic import TagIDStr

from metrics.economy import get_economy
from metrics.administrative import get_adm
from metrics.tags_and_players import TAGS


METRICS = [
    get_economy,
    get_adm,
]


class FilteredCountryManager(CountryManager):
    wanted_tags:  ClassVar[Set[str]] = set(TAGS)


class Vic3Save(BaseModel):
    """High-level of a parsed Victoria 3 save. Only expected information is defined."""
    date: str
    country_manager: FilteredCountryManager


class Orchestrator():

    def __init__(
            self, 
            data: Vic3Save, 
            metrics_fn: Sequence[Callable[[Country], Dict]] = METRICS
            ):
        self.data = data if isinstance(data, Vic3Save) else Vic3Save(**data)
        self.metrics_fn = metrics_fn

    def _get_tag_metrics(self,
                        tag: TagIDStr,
                        ) -> Dict:

        merged = {}     # Warning: make sure there are not repeated keys

        for func in self.metrics_fn:
            merged.update(func(self.data, tag))

        return merged

    def _iterate_tags(self,
                     tags: List[TagIDStr]
                     ) -> Dict:
        
        tags_metrics = {}

        for tag in tags:
            tags_metrics[tag] = self._get_tag_metrics(tag)
        
        return tags_metrics
    

    def to_dataframe(self, 
                     tags: List[TagIDStr]
                     ) -> pd.DataFrame:
        """ 
        Construct Pandas DataFrame based on a dictionary of metrics
            where Dict is {tag id: metrics}
            and metrics is a Dict {metric name: value}

        Returns:
            pd.DataFrame with constructed stats for a given year.
        
        """
        tags_metrics = self._iterate_tags(tags)
        
        return pd.DataFrame.from_dict(tags_metrics, orient='index')
