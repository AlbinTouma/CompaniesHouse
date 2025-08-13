from dataclasses import dataclass, field
from datetime import datetime
from data_models.util import Address

@dataclass
class Company:
    CompanyName: str
    CompanyNumber: str
    CompanyCategory: str
    CompanyStatus: str
    CountryOfOrigin: str 
    DissolutionDate: str
    IncorporationDate: str
    Address: Address

    def __post_init__(self):
        self.DissolutionDate = (
            datetime.strptime(self.DissolutionDate, "%d/%m/%Y") if self.DissolutionDate else None

        )
        self.IncorporationDate = (
            datetime.strptime(self.IncorporationDate, "%d/%m/%Y") if self.IncorporationDate else None
        )

@dataclass
class Accounts:
    AccountRefDay: str 
    AccountRefMonth: str
    NextDueDate: str
    LastMadeUpDate: str 
    AccountCategory: str
    ReturnsNextDueDate: str
    ReturnsLastMadeUpDate: str

@dataclass
class Mortgages:
    NumMortCharges: int
    NumMortOutstanding: int 
    NumMortPartSatisfied: int
    NumMortSatisfied: int 
   
@dataclass
class Industry:
    SicText_1: str
    SicText_2: str
    SicText_3: str
    SicText_4: str
    NumGenPartners: str
    NumLimPartners: str
    URI: str

@dataclass
class PreviousName:
    PreviousName_1CONDATE: str
    PreviousName_1CompanyName: str
    PreviousName_2CONDATE: str
    PreviousName_2CompanyName: str
    PreviousName_3CONDATE: str
    PreviousName_3CompanyName: str
    PreviousName_4CONDATE: str
    PreviousName_4CompanyName: str
    PreviousName_5CONDATE: str
    PreviousName_5CompanyName: str
    PreviousName_6CONDATE: str
    PreviousName_6CompanyName: str
    PreviousName_7CONDATE: str
    PreviousName_7CompanyName: str
    PreviousName_8CONDATE: str
    PreviousName_8CompanyName: str
    PreviousName_9CONDATE: str
    PreviousName_9CompanyName: str
    PreviousName_10CONDATE: str
    PreviousName_10CompanyName: str
    ConfStmtNextDueDate: str
    ConfStmtLastMadeUpDate: str

