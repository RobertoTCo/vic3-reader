"""Functions to extract Victoria 3 data in a save related to government and diplomacy."""

from typing import Callable, Dict, Sequence

from vic3_reader.metrics.models import Country, TagIDStr, Vic3Save
from vic3_reader.metrics.models.basic import warning_more_than_one_channel


def get_prestige(country: Country) -> Dict:
    warning_more_than_one_channel(country.prestige)
    return {"prestige": country.prestige.channels[0].values[-1]}


def get_literacy(country: Country) -> Dict:
    warning_more_than_one_channel(country.literacy)
    return {"literacy": country.literacy.channels[0].values[-1]}


def get_infamy(country: Country) -> Dict:
    return {'infamy': country.infamy}


ADM_FN = [
        get_prestige,
        get_literacy,
        get_infamy,
    ]


def get_adm(data: 'Vic3Save', 
            tag_id: TagIDStr,
            functions: Sequence[Callable] = ADM_FN
            ) -> Dict:
    """
    Find the database data for a given country and extract the government
    and diplomacy metrics defined in the module.
    
    Args:
        data: Vic3Save - Parsed Vic3 save information.
        tag_id: TagIDStr - The tag ID for a country in the database.
        functions (Opt): each function define how to extract one or semantically grouped metrics. 
            The expected output is to be a Dict['metric name', 'value']
        
    Returns:
        Dict ['metric name', 'value'] with all metrics collected in the module.

    """
    country = data.country_manager.database[tag_id]

    merged = {}  # Warning: same keys might overriden
    
    if not country:
        return

    for func in functions:
        merged.update(func(country))

    return merged
