from dataclasses import dataclass, field
from shared_class import Address, Identification, DateOfBirth

@dataclass
class PSC:
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