from typing import Dict, List
from pydantic import BaseModel

TAGS = [
    1,      # GBR
    3,      # RUS
    4,      # FRA
    5,      # PRU, NGF, GER
    8,      # AUS, HAB
    9,      # USA
    17,     # JAP
    23,     # SWE
    29,     # NET
    36,     # SPA
    62,     # SAR (ITA?)
    94,     # TUR
    199,    # BRZ
]

TAGS_ID_NAME = {}


class PlayerItem(BaseModel):
    """Model for Player dicts relating tag ids and player names
    
    PlayerItem: Dict[idtype] = name
    """
    idtype: int
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
    return {item['name']: item['age'] for item in previous_played}

