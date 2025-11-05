from dataclasses import dataclass, field
from datetime import datetime
from src.models.util import Address
from sqlmodel import Field, Relationship, Session, SQLModel
from typing import Optional, List


class Accounts(SQLModel, table=True):
    id: int | None  = Field(default=None, primary_key=True)
    account_ref_day: str | None
    account_ref_month: str | None
    next_due_date: str | None
    last_made_update: str | None
    account_category: str | None
    returns_next_due_date: str | None
    returns_last_madeup_date: str | None
    company_id: str | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"] = Relationship(back_populates="accounts")

class Mortgages(SQLModel, table=True):
    id: int | None  = Field(default=None, primary_key=True)
    num_mort_charges: int | None
    num_mort_outstanding: int | None
    num_mort_part_satisfied: int | None
    num_mort_satisfied: int | None
    company_id: str | None = Field(default=None, foreign_key="company.id") 
    company: Optional["Company"] = Relationship(back_populates="mortgages")
   
class Industry(SQLModel, table=True):
    id: int | None  = Field(default=None, primary_key=True)
    company_id: str | None = Field(default=None, foreign_key="company.id")
    sic_text_1: str | None
    sic_text_2: str | None
    sic_text_3: str | None
    sic_text_4: str | None
    num_gen_partners: str | None
    num_lim_partners: str | None
    uri: str | None
    company: Optional["Company"]  = Relationship(back_populates="industry")

class PreviousName(SQLModel, table=True):
    id: int | None  = Field(default=None, primary_key=True)
    PreviousName_1CONDATE: str | None
    PreviousName_1CompanyName: str | None
    PreviousName_2CONDATE: str | None
    PreviousName_2CompanyName: str | None
    PreviousName_3CONDATE: str | None
    PreviousName_3CompanyName: str | None
    PreviousName_4CONDATE: str | None
    PreviousName_4CompanyName: str | None
    PreviousName_5CONDATE: str | None
    PreviousName_5CompanyName: str | None
    PreviousName_6CONDATE: str | None
    PreviousName_6CompanyName: str | None
    PreviousName_7CONDATE: str | None
    PreviousName_7CompanyName: str | None
    PreviousName_8CONDATE: str | None
    PreviousName_8CompanyName: str | None
    PreviousName_9CONDATE: str | None
    PreviousName_9CompanyName: str | None
    PreviousName_10CONDATE: str | None
    PreviousName_10CompanyName: str | None
    ConfStmtNextDueDate: str | None
    ConfStmtLastMadeUpDate: str | None
    company_id: str | None = Field(default=None, foreign_key="company.id")
    company: Optional["Company"]  = Relationship(back_populates="previous_names")

class Company(SQLModel, Address, table=True):
    id: str = Field(primary_key=True, index=True)
    name: str
    category: str | None
    status: str | None
    country_origin: str | None
    dissolution_date: str | None
    incorporation_date: str | None
    accounts: List["Accounts"] = Relationship(back_populates="company")
    mortgages: List["Mortgages"] =  Relationship(back_populates="company")
    previous_names: List["PreviousName"] = Relationship(back_populates="company")
    industry: Optional[Industry] = Relationship(back_populates="company")
    psc: Optional["PSC"] = Relationship(back_populates="company")

