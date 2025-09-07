from .country_database import Country, CountryManager
from pydantic import ValidationError
from .basic import TagIDStr

from pydantic import BaseModel

class Vic3Save(BaseModel):
    """ 
    Top high-level data model validating the info from a Vic3 save.

    Important! To avoid loading unnecessary info from 'managers' unwated keys, 'manager' data models
    can be defined with a filtering set varclass that specify which data to include at runtime.

    For example, 

    CountryManager.wanted_tags = [1,3,4] will specify to only parse data for UK, RUS and FRA,
    in the database for country_manager object in vic3 saves.

    Do this before validating the model. It is a class var. Only need to do it once at runtime.
    
    """
    date: str
    country_manager: CountryManager

    @classmethod
    def pretty_missing_fields(cls, e: ValidationError) -> ValueError:
        """
        Format missing field errors for this model in a pretty way.
        """
        messages = []
        for err in e.errors():
            if err['type'] == 'missing':
                loc = ".".join(str(x) for x in err['loc'])
                messages.append(f"{loc}\n  {err['msg']}")
        return ValueError("\n".join(messages) )

__all__ = [
        "Country", 
        "CountryManager",
        "TagIDStr",
        "TagModel",
        "ValidationError",
        "Vic3Save",
        ]