from typing import Dict

def get_game_date(date: str) -> Dict:
    """ Returns as date type the date saved in a Vic3 save. """
    from datetime import datetime

    parts = date.split(".")

    if len(parts) < 3 or not all(part.isdigit() for part in parts[:3]):
        raise ValueError("Date string must have at least three numeric parts separated by dots.")
    
    date_obj = datetime.strptime(
        ".".join(parts[:3]), 
        "%Y.%m.%d"
        ).date()

    return {
        'game_date' : date_obj
    }