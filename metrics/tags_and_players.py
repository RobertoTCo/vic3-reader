from typing import Callable, Dict, List, Sequence
from pydantic import BaseModel

from .models.country_database import Country
from .models.basic import TagIDStr

TAGS = [
    "1",      # GBR
    "3",      # RUS
    "4",      # FRA
    "5",      # PRU, NGF, GER
    "8",      # AUS, HAB
    "9",      # USA
    "17",     # JAP
    "23",     # SWE
    "29",     # NET
    "36",     # SPA
    "62",     # SAR (ITA?)
    "94",     # TUR
    "199",    # BRZ
]

class PlayerItem(BaseModel):
    """Model for Player dicts relating tag ids and player names
    
    PlayerItem: Dict[idtype] = name
    """
    idtype: str
    name: str

class PreviousPlayed(BaseModel):
    """Model for previous_played array
    
    PreviousPlayed[PlayerItem: Dict]
    """
    items: List[PlayerItem]

def get_players(previous_played: PreviousPlayed) -> Dict:
    """
    Array of dicts that contain "idtype": int and "name": str

    Returns: flattened version "idtype":"name"
    """
    return {item['name']: item['idtype'] for item in previous_played.items}


def get_tag_definition(country: Country) -> Dict:
    return country.definition


TAG_FN = [
        get_tag_definition,
    ]


def get_tag_data(data: 'Vic3Save', 
                tag_id: TagIDStr,
                functions: Sequence[Callable] = TAG_FN
                ) -> Dict:
    """
    Find the database data for a given country and extract the economy metrics
    defined in the module.
    
    Args:
        data: Vic3Save - Parsed Vic3 save information.
        tag_id: TagIDStr - The tag ID for a country in the database.
        
    Returns:
        Dict with all metrics collected in the module.

    """
    country = data.country_manager.database[tag_id]

    merged = {}  # Warning: same keys are overriden
    
    if not country:
        return

    for func in functions:
        merged.update(func(country))

    return merged