from dataclasses import dataclass, field
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from pydantic import Field, field_serializer, model_validator

class AddressRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    care_of: str | None = None
    post_box:  str | None  = None
    address_line_1: str | None = None
    address_line_2: str | None = None 
    post_town: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None
    post_code: Optional[str] = None
    premises: Optional[str] = None
    full_address: Optional[str] = None

    @model_validator(mode="after")
    def assemble_full_address(self) -> str:
        parts = [
            self.premises,
            self.address_line_1,
            self.address_line_2,
            self.post_town,
            self.county,
            self.post_code,
            self.country
        ]
        self.full_address = ', '.join(filter(None, parts))
        return self
