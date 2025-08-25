"""Functions to extract Victoria 3 data in a save related to economy."""

from typing import Callable, Dict, Sequence

from .models import Country, TagIDStr, Vic3Save
from .models.country_database import ConstructionElement
from .models.basic import warning_more_than_one_channel

# principal, credit, money
# gpd
# pop, peasants, low, middle, upper
# construction
# avgsol

def get_budget(country: Country) -> Dict:
    return country.budget.model_dump()


def get_gdp(country: Country) -> Dict:
    warning_more_than_one_channel(country.gdp)
    return {"gpd": country.gdp.channels[0].values[-1]}


def get_pop(country: Country) -> Dict:
    return country.pop_statistics.model_dump()


def get_avgsol(country: Country) -> Dict:
    warning_more_than_one_channel(country.avgsoltrend)
    return {"avgsoltrend": country.avgsoltrend.channels[0].values[-1]}


def get_construction(construction_queue: Sequence[ConstructionElement]) -> Dict:
    # Construction is not a metric number, we need to check those buildings
    # currently being active in construction and sum the speed of all
    total_base_speed = 0
    total_speed = 0

    for elem in construction_queue:
        total_base_speed += elem.base_construction_speed
        total_speed += elem.construction_speed

    return (total_speed, total_base_speed)
        
def get_total_construction(country: Country) -> Dict:
    # Construction can be split between government and private queues. 
    # The total base_contruction of both will be what the player see in the right top corner in the game
    # But the real applied construction (final) is the one after speed modifiers are applied
    
    # government construction
    public_output, public_base = get_construction(country.government_queue.construction_elements)
    # private construction
    private_output, private_base = get_construction(country.private_queue.construction_elements)

    return {
        "gov_base_construction": public_base ,
        "gov_final_construction": public_output, 
        "priv_base_construction": private_base,
        "priv_final_construction": private_output,
    }


ECONOMY_FN = [
        get_budget,
        get_gdp,
        get_pop,
        get_avgsol,
        get_total_construction
    ]


def get_economy(data: 'Vic3Save', 
                tag_id: TagIDStr,
                functions: Sequence[Callable] = ECONOMY_FN
                ) -> Dict:
    """
    Find the database data for a given country and extract the economy metrics
    defined in the module.
    
    Args:
        data: Vic3Save - Parsed Vic3 save information.
        tag_id: TagIDStr - The tag ID for a country in the database.
        functions (Opt): each function define how to extract one or semantically grouped metrics. 
            The expected output is to be a Dict['metric name', 'value']
        
    Returns:
        Dict ['metric name', 'value'] with all metrics collected in the module.

    """
    country = data.country_manager.database[tag_id]

    merged = {}  # Warning: same keys are overriden
    
    if not country:
        return

    for func in functions:
        merged.update(func(country))

    return merged