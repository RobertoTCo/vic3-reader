from typing import Dict, TypeAlias

DateStr: TypeAlias = str

def get_game_date(metadata: Dict[DateStr]) -> Dict:
    from datetime import datetime

    parts = metadata['game_date'].split(".")

    if len(parts) < 3 or not all(part.isdigit() for part in parts[:3]):
        raise ValueError("Date string must have at least three numeric parts separated by dots.")
    
    date_obj = datetime.strptime(
        ".".join(parts[:3]), 
        "%Y.%m.%d"
        )

    return {
        'game_date' : date_obj
    }

