"""Defines the scheme that compose a country data in the country_manager database in a Victoria 3 save."""

from typing import Any, ClassVar, Dict, List, Optional, Set
from pydantic import BaseModel, Field, field_validator

from.basic import TagIDStr, TrendObject


class Budget(BaseModel):
    """Model for expected information related to budget and spending"""
    credit: float
    money: float
    principal: Optional[float] = 0.0


class PopStats(BaseModel):
    """Model for expected information related to population"""
    population_lower_strata: int
    population_middle_strata: int
    population_upper_strata: int
    population_radicals: int
    population_loyalists: int
    population_political_participants: int
    population_salaried_workforce: int              # employees
    population_subsisting_workforce: int            # peasants
    population_unemployed_workforce: int            # not employeed
    population_government_workforce: int            # burocrats and clerks in gov buildings
    population_military_workforce: int              # army
    population_laborer_workforce: int               
    #...
    primary_cultures_population: int


class ConstructionElement(BaseModel):
    """Model for expected information about a building in the construction queue"""
    type: str
    state: int
    identity: Any
    construction_left: float
    construction_speed: Optional[float] = 0.0
    base_construction_speed: Optional[float] = 0.0


class ConstructionQueue(BaseModel):
    """Model holding a set of buildings in qeue for contruction."""
    # If it is not present in tag, list initialises empty.
    construction_elements: List[ConstructionElement] = Field(default_factory=list)

    
class Country(BaseModel):
    """
    Model for minimal information in per country instance 
    in the country_manager database
    """
    definition: str
    infamy: Optional[float] = 0.0

    market_capital: int
    market: int

    budget: Budget

    gdp: TrendObject
    prestige: TrendObject
    literacy: TrendObject
    avgsoltrend: TrendObject

    pop_statistics: PopStats

    government_queue: Optional[ConstructionQueue] = Field(default_factory=ConstructionQueue)
    private_queue: Optional[ConstructionQueue] = Field(default_factory=ConstructionQueue)


class CountryManager(BaseModel):
    database: Dict[TagIDStr, Optional[Country]]

    # This classvar will define which Tags from the database are used
    # Not defined tags are excluded in the model.
    wanted_tags: ClassVar[Set[TagIDStr]] = set() 

    @field_validator('database', mode='before')
    @classmethod
    def parse_none_string_to_null(cls, v):

        # First: filter unwanted keys
        if isinstance(v, dict):
            v = {k: v[k] for k in v if k in cls.wanted_tags}

        # Finally: parse "none" -> None
        if isinstance(v, dict):
            return {
                key: None if value == "none" else value
                for key, value in v.items()
            }
        return v