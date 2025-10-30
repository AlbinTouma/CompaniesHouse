from dataclasses import dataclass, field
from sqlmodel import Field, Relationship, Session, SQLModel
from typing import Optional



@dataclass
class Identification:
    CountryRegistered: str
    LegalAuthority: str
    LegalForm: str
    PlaceRegistered: str
    RegistrationNumber: str

@dataclass
class Name:
    FullName: str
    Firstname: str
    Middlename: str
    Surname: str
    Title: str

@dataclass
class DateOfBirth:
    Year: str   
    Month: str

class Address:
    care_of:  Optional[str] = Field(default=None)
    post_box:   Optional[str] = Field(default=None)
    address_line_1: Optional[str] = Field(default=None)
    address_line_2: Optional[str] = Field(default=None)
    post_town: Optional[str] = Field(default=None)
    county: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    post_code: Optional[str] = Field(default=None)
    premises: Optional[str] = Field(default=None)

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
     