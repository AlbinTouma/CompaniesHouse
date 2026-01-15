from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List



class Identification(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Must be here
    country_registered: str | None = None
    legal_authority: str | None = None 
    legal_form: str | None = None 
    place_registered: str | None = None  
    registration_number: str | None = None 

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

