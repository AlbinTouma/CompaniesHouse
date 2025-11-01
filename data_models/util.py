from dataclasses import dataclass, field
from sqlmodel import Field, Relationship, Session, SQLModel
from typing import Optional
from pydantic import computed_field

class Identification:
    country_registered: Optional[str] = Field(default=None) 
    legal_authority: Optional[str] = Field(default=None) 
    legal_form: Optional[str] = Field(default=None) 
    place_registered: Optional[str] = Field(default=None) 
    registration_number: Optional[str] = Field(default=None) 

class Name:
    full_name: Optional[str] = Field(default=None) 
    first_name: Optional[str] = Field(default=None) 
    middle_name: Optional[str] = Field(default=None) 
    sur_name: Optional[str] = Field(default=None) 
    title: Optional[str] = Field(default=None) 

class DateOfBirth:
    year: Optional[str] = Field(default=None) 
    month: Optional[str] = Field(default=None)

class Address():
    care_of:  Optional[str] = Field(default=None)
    post_box:   Optional[str] = Field(default=None)
    address_line_1: Optional[str] = Field(default=None)
    address_line_2: Optional[str] = Field(default=None)
    post_town: Optional[str] = Field(default=None)
    county: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    post_code: Optional[str] = Field(default=None)
    premises: Optional[str] = Field(default=None)

    @computed_field
    @property
    def build_full_address(self) -> str:
        parts = [
            self.address_line_1, 
            self.address_line_2, 
            self.post_town, 
            self.county, 
            self.post_code, 
            self.country
            ]
        return ", ".join(filter(None, parts))
     