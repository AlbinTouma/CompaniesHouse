from dataclasses import dataclass, field
from pydantic import JsonValue, BaseModel, BeforeValidator, ConfigDict, model_validator, Json, field_serializer, field_validator
from typing import Optional, List, Any, Dict, Annotated, TYPE_CHECKING
from src.schemas.utils import Identification, DateOfBirth
from src.schemas.address import AddressRead
import json

if TYPE_CHECKING:
    from src.schemas.company import CompanyRead

class PscRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    person_id: str | None = None
    etag: str | None = None 
    address: AddressRead | None = None
    identification: Identification | None = None
    date_of_birth: DateOfBirth | None = None
    kind: str | None = None 
    name: str | None = None
    nationality: str | None = None 
    notified_on: str | None = None 
    ceased_on: str | None = None 
    country_of_residence: str | None = None 
    natures_of_control: List[str] | None = []
    links: Optional[dict[str, str]] = None
    company_id: str | None = None
    notified_on: str | None = None
    
    @model_validator(mode="before")
    @classmethod
    def reshape_flat_orm_to_nested(cls, orm_data: Any) -> Any:
            if not isinstance(orm_data, dict):
                payload = orm_data.model_dump()

                if hasattr(orm_data, 'company'):
                    payload['company'] = orm_data.company

                wrapped_fields = ['address', 'date_of_birth', 'identification']
                for f in wrapped_fields:
                    payload[f] = payload 

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

class PscWithCompany(PscRead):
    model_config = ConfigDict(from_attributes=True)
    company: Optional["CompanyRead"] = None

