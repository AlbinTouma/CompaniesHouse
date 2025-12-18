from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Optional, List
from pydantic import Field

class AddressRead(BaseModel):
    care_of: str | None = Field(validation_alias="care_of")
    post_box:  str | None  = Field(validation_alias="post_box")
    address_line_1: str | None = Field(validation_alias="address_line_1")
    address_line_2: str | None = Field(validation_alias="address_line_2")
    post_town: Optional[str] = Field(validation_alias="post_town")
    county: Optional[str] = Field(validation_alias="county")
    country: Optional[str] = Field(validation_alias="country")
    post_code: Optional[str] = Field(validation_alias="post_code")
    premises: Optional[str] = Field(validation_alias="premises")
    full_address: Optional[str] = Field(validation_alias="full_address")