from dataclasses import dataclass, field
from pydantic import JsonValue, BaseModel, BeforeValidator, ConfigDict, model_validator, Json, field_serializer, field_validator
from typing import Optional, List, Any, Dict, Annotated
from src.schemas.utils import Identification, DateOfBirth
from src.schemas.address import AddressRead
import json

def parse_json_string(v):
    if isinstance(v, str):
        return json.loads(v)
    return v

class PscRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    etag: Optional[str] 
    address: AddressRead
    identification: Identification
    date_of_birth: DateOfBirth
    
    kind: str | None = None 
    name: str | None = None
    nationality: str | None = None 
    notified_on: str | None = None 
    ceased_on: str | None = None 
    country_of_residence: str | None = None 
    natures_control: List[str] | None = None
    links: Optional[dict[str, str]] = None
    company_id: str | None = None
    
    @model_validator(mode="before")
    @classmethod
    def wrap_address_fields(cls, data: Any) -> Any:
            # If we are validating an ORM object (like CompanySQL)
            if not isinstance(data, dict):
                # 1. Convert the flat SQL object to a dict
                # (SQLModel objects have a built-in .model_dump())
                payload = data.model_dump()
                
                # 2. Assign the same flat payload to the 'Address' key.
                # AddressRead (with from_attributes=True) will pick only
                # the address-specific fields it needs from this flat dict.
                payload["address"] = payload
                payload["date_of_birth"] = payload
                payload["identification"] = payload
                return payload
                
            return data
        
    @field_validator("links", mode="before")
    @classmethod
    def parse_links(cls, v: Any) -> Any:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v
