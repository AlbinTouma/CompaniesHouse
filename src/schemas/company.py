from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Any
from src.schemas.address import AddressRead
from src.schemas.psc import PscRead
from pydantic import model_validator
from pydantic import ConfigDict

class Accounts(BaseModel):
    id: int | None 
    account_ref_day: str | None
    account_ref_month: str | None
    next_due_date: str | None
    last_made_update: str | None
    account_category: str | None
    returns_next_due_date: str | None
    returns_last_madeup_date: str | None

class Mortgages(BaseModel):
    id: int | None 
    num_mort_charges: int | None
    num_mort_outstanding: int | None
    num_mort_part_satisfied: int | None
    num_mort_satisfied: int | None
   
class Industry(BaseModel):
    id: int | None 
    company_id: str | None 
    sic_text_1: str | None
    sic_text_2: str | None
    sic_text_3: str | None
    sic_text_4: str | None
    num_gen_partners: str | None
    num_lim_partners: str | None

class PreviousName(BaseModel):
    id: int | None 
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

class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str | None
    category: str | None
    status: str | None
    country_origin: str | None
    dissolution_date: str | None
    incorporation_date: str | None
    address: Optional[AddressRead] = None
    psc: Optional[List[PscRead]] = []

    @model_validator(mode="before")
    @classmethod
    def wrap_address_fields(cls, data: Any) -> Any:
        # If we are validating an ORM object (like CompanySQL)
        if not isinstance(data, dict):
            # 1. Convert the flat SQL object to a dict
            # (SQLModel objects have a built-in .model_dump())
            payload = data.model_dump()
            if hasattr(data, "psc"):
                payload["psc"] = data.psc
            
            # 2. Assign the same flat payload to the 'Address' key.
            # AddressRead (with from_attributes=True) will pick only
            # the address-specific fields it needs from this flat dict.
            payload["address"] = payload
            return payload
            
        return data
