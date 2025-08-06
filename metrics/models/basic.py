"""Defines the basic schemes that are used to identify data in a Victoria 3 save."""

from pydantic import BaseModel , ConfigDict, RootModel, field_validator
from typing import Dict, List, NewType
from datetime import datetime, date

from warnings import warn


TagIDStr = NewType("TagIDStr", str)
"""
TagIDStr

Numeric IDs for a specific country throughout its lifespan in Vic3 game.
These are stored as strings with numeric digits.
"""


class TagModel(RootModel[List[TagIDStr]]):
    """ 
     List[TagID]
     
     List defining for what countries should metrics be extracted
     """
    pass


class Channel(BaseModel):
    """
    A recorded array of a saved game measure, plus date and index of last element.
    """
    date: date
    index: int
    values: List[int|float]

    @field_validator('date', mode='before')
    @classmethod
    def parse_custom_date(cls, v):
        """ Ensure that str dates are parsed """
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y.%m.%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format: {v}. Expected format: yyyy.mm.dd")
        return v


class TrendObject(BaseModel):
    """ 
    A object recording a metric with one or more channels. 
    
    Used in-game to plot trend line charts.
    """
    sample_rate: int
    count: int
    channels: Dict[int, Channel]


class ProcessingWarning(Warning):
     pass


def warning_more_than_one_channel(trend_object: TrendObject):
    """ 
    Raise a warning when only one channel is expected to get a metric 
    but do not stop the execution.
    """
    if len( trend_object.channels.keys() ) > 1:
        warn("This is a custom warning!", ProcessingWarning)