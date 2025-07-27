from typing import Dict, Optional
from pydantic import BaseModel

from .tags_and_players import TAGS

import pandas as pd


RESOURCES = {
    0: 'iron',
    1: 'wood'
}

class Budget(BaseModel):
    """Model for minimal information for budget and spending"""
    credit: float
    money: float
    principal: Optional[float] = 0


class Country(BaseModel):
    """Model for minimal information in country dictionaries"""
    definition: str
    infamy: float

    market_capital: int
    market: int

    budget: Budget

  
def get_credit(country: Dict) -> Dict:
    return country['budget']['credit']

def get_debt():
    pass

def get_money():
    pass

def get_budget_metrics(budget: Budget):
    get_credit()
    get_debt()
    get_money()
    return

def get_country_stats() -> pd.Dataframe:
    pass