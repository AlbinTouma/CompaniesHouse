from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Optional, List


class AddressRead(BaseModel):
    care_of: str | None = None
    post_box:  str | None  = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    post_town: Optional[str] = str | None 
    county: Optional[str] = str | None
    country: Optional[str] = str | None
    post_code: Optional[str] = str | None 
    premises: Optional[str] = str | None
    full_address: Optional[str] = str | None
