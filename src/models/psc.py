from dataclasses import dataclass, field
from src.models.util import Address, Identification, DateOfBirth
#from src.models.company import CompanySQL
from sqlmodel import Field, Relationship, Session, SQLModel
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from src.models.company import CompanySQL

class PSC(Address, Identification, DateOfBirth, SQLModel,table=True):

    person_id: str  = Field(primary_key=True)
    etag: Optional[str] = Field(default=None) 
    kind: Optional[str] = Field(default=None) 
    name: Optional[str] = Field(default=None) 
    nationality: Optional[str] = Field(default=None) 
    notified_on: Optional[str] = Field(default=None) 
    ceased_on: Optional[str] = Field(default=None) 
    country_of_residence: Optional[str] = Field(default=None) 
    natures_of_control: Optional[list[str]] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )

    links: dict[str, str] = Field(
        default_factory=dict,
        sa_column=Column(JSON)
    )
    company_number: str | None = Field(default=None, foreign_key="company.id")
    company: Optional[List["CompanySQL"]] = Relationship(back_populates="psc")


