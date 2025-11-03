from dataclasses import dataclass, field
from data_models.util import Address, Identification, DateOfBirth
from data_models.company import Company
from sqlmodel import Field, Relationship, Session, SQLModel
from typing import Optional, List
from sqlalchemy import Column, JSON


class PSC(SQLModel, Address, Identification, DateOfBirth,  table=True):
    id: int | None  = Field(default=None, primary_key=True)
    etag: Optional[str] = Field(default=None) 
    kind: Optional[str] = Field(default=None) 
    name: Optional[str] = Field(default=None) 
    nationality: Optional[str] = Field(default=None) 
    notified_on: Optional[str] = Field(default=None) 
    ceased_on: Optional[str] = Field(default=None) 
    country_of_residence: Optional[str] = Field(default=None) 
    natures_control: Optional[List[str]] = Field(default_factory=list,sa_column=Column(JSON))
    links: dict[str, str] = Field(default_factory=dict, sa_column=Column(JSON))
    company_id: str | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="psc")


@dataclass
class PSCClass:
    CompanyNumber: str
    Address: Address
    Etag: str
    Identification: Identification
    Kind: str
    Name: str
    DateOfBirth:  DateOfBirth
    Nationality: str
    NotifiedOn: str
    CeasedOn: str
    CountryOfResidence: str
    NaturesControl: list[str] = field(default_factory=list)
    Links: dict[str, str] = field(default_factory=dict)
