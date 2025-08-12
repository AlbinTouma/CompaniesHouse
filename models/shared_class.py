from dataclasses import dataclass, field



@dataclass
class Identification:
    CountryRegistered: str
    LegalAuthority: str
    LegalForm: str
    PlaceRegistered: str
    RegistrationNumber: str

@dataclass
class Name:
    FullName: str
    Firstname: str
    Middlename: str
    Surname: str
    Title: str

@dataclass
class DateOfBirth:
    Year: str   
    Month: str

@dataclass
class Address:
    CareOf:  str
    PostBox:   str
    AddressLine1: str
    AddressLine2: str 
    PostTown: str
    County: str 
    Country: str
    PostCode: str
    Premises: str
    FullAddress: str = field(init=False)  # Excluded from __init__
       
    def __post_init__(self):
        # Construct full address with non-empty fields
        parts = [self.AddressLine1, self.AddressLine2, self.PostTown, self.County, self.PostCode, self.Country]
        self.FullAddress = ", ".join(filter(None, parts))  # Remove empty values

