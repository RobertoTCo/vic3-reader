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

def get_money():
    pass

def get_debt_for_tag(countries_data: Dict, tag_id: int) -> float:
    """
    Extract debt (principal) for a specific tag ID.
    
    Args:
        countries_data: Dictionary containing country data with budget information
        tag_id: The tag ID to get debt for
        
    Returns:
        Debt value (principal) for the tag
    """
    tag_key = str(tag_id)  # Keys are strings from parser
    country = countries_data[tag_key]
    budget = country.get('budget', {})
    return float(budget.get('principal') or 0)

def debt(countries_data: Dict) -> Dict[int, float]:
    """
    Extract debt (principal) for each country by tag ID.
    
    Args:
        countries_data: Dictionary containing country data with budget information
        
    Returns:
        Dictionary mapping tag ID to debt value (principal)
    """
    return {
        tag_id: get_debt_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_prestige_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    prestige_data = country.get('prestige', {})
    values = prestige_data.get('values', [])
    return float(values[-1]) if values else 0.0

def prestige(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_prestige_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_gdp_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    gdp_data = country.get('gdp', {})
    values = gdp_data.get('values', [])
    return float(values[-1]) if values else 0.0

def gdp(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_gdp_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_sol_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    sol_data = country.get('avgsoltrend', {})
    values = sol_data.get('values', [])
    return float(values[-1]) if values else 0.0

def sol(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_sol_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_pop_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    pop_data = country.get('trend_population', {})
    values = pop_data.get('values', [])
    return float(values[-1]) if values else 0.0

def pop(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_pop_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_peasants_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    pop_stats = country.get('pop_statistics', {})
    return float(pop_stats.get('population_subsisting_workforce') or 0)

def peasants(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_peasants_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_employed_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    pop_stats = country.get('pop_statistics', {})
    return float(pop_stats.get('population_salaried_workforce') or 0)

def employed(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_employed_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_literacy_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    literacy_data = country.get('literacy', {})
    values = literacy_data.get('values', [])
    return float(values[-1]) if values else 0.0

def literacy(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_literacy_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_construction_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    return float(country.get('construction') or 0)

def construction(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_construction_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_money_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    return float(country.get('money') or 0)

def money(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_money_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_national_revenue_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    budget = country.get('budget', {})
    return float(budget.get('national_revenue') or 0)

def national_revenue(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_national_revenue_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

def get_expenses_for_tag(countries_data: Dict, tag_id: int) -> float:
    tag_key = str(tag_id)
    country = countries_data[tag_key]
    budget = country.get('budget', {})
    return float(budget.get('expenses') or 0)

def expenses(countries_data: Dict) -> Dict[int, float]:
    return {
        tag_id: get_expenses_for_tag(countries_data, tag_id) 
        for tag_id in TAGS 
        if str(tag_id) in countries_data
    }

# def get_army_for_tag(countries_data: Dict, tag_id: int) -> float:
#     tag_key = str(tag_id)
#     country = countries_data[tag_key]
#     return float(country.get('army') or 0)

# def army(countries_data: Dict) -> Dict[int, float]:
#     return {
#         tag_id: get_army_for_tag(countries_data, tag_id) 
#         for tag_id in TAGS 
#         if str(tag_id) in countries_data
#     }

# def get_navy_for_tag(countries_data: Dict, tag_id: int) -> float:
#     tag_key = str(tag_id)
#     country = countries_data[tag_key]
#     return float(country.get('navy') or 0)

# def navy(countries_data: Dict) -> Dict[int, float]:
#     return {
#         tag_id: get_navy_for_tag(countries_data, tag_id) 
#         for tag_id in TAGS 
#         if str(tag_id) in countries_data
#     }

def get_budget_metrics(budget: Budget):
    get_credit()
    debt()
    get_money()
    return

def get_country_stats() -> pd.Dataframe:
    pass