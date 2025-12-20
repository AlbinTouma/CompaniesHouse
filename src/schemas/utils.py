from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List



class Identification(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Must be here

    country_registered: str = None
    legal_authority: str = None 
    legal_form: str = None 
    place_registered: str = None  
    registration_number: str = None 

class Name(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Must be here

    full_name:  str = None 
    first_name:  str = None 
    middle_name:  str = None 
    sur_name: str = None  
    title:  str = None 

class DateOfBirth(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Must be here
    year: int | None  = None
    month: int | None  = None

