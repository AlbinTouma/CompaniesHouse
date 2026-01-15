from dataclasses import dataclass, field
from sqlmodel import Field, Relationship, Session, SQLModel
from typing import Optional
from pydantic import Field as pydanticField, AliasPath, computed_field

class Identification(SQLModel, table=False):
    country_registered: Optional[str] = Field(default=None) 
    legal_authority: Optional[str] = Field(default=None) 
    legal_form: Optional[str] = Field(default=None) 
    place_registered: Optional[str] = Field(default=None) 
    registration_number: Optional[str] = Field(default=None) 

class Name(SQLModel, table=False):
    full_name: Optional[str] = Field(default=None) 
    first_name: Optional[str] = Field(default=None) 
    middle_name: Optional[str] = Field(default=None) 
    sur_name: Optional[str] = Field(default=None) 
    title: Optional[str] = Field(default=None) 

class DateOfBirth(SQLModel, table=False):
    year: Optional[str] = Field(default=None) 
    month: Optional[str] = Field(default=None)

class Address(SQLModel, table=False):
    care_of:  Optional[str] = pydanticField(validation_alias=AliasPath("address","care_of"), default=None)
    post_box:   Optional[str] = pydanticField(validation_alias=AliasPath("address","post_box"),default=None)
    address_line_1: Optional[str] = pydanticField(validation_alias=AliasPath('address', 'address_line_1'), default=None)
    address_line_2: Optional[str] = pydanticField(validation_alias=AliasPath("address","address_line_2"),default=None)
    post_town: Optional[str] = pydanticField(validation_alias=AliasPath("address","post_town"),default=None)
    county: Optional[str] = pydanticField(validation_alias=AliasPath("address","county"),default=None)
    country: Optional[str] = pydanticField(validation_alias=AliasPath("address","country"), default=None) 
    post_code: Optional[str] = pydanticField(validation_alias=AliasPath("address", "post_code"), default=None)
    premises: Optional[str] = pydanticField(validation_alias=AliasPath("address", "premises"), default=None)
    full_address: Optional[str] = pydanticField(validation_alias=AliasPath("address", "full_address"), default=None)

