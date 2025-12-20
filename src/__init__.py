from src.schemas.company import CompanyRead, CompanyWithPSC
from src.schemas.psc import PscRead, PscWithCompany

CompanyRead.model_rebuild()
CompanyWithPSC.model_rebuild()
PscRead.model_rebuild()
PscWithCompany.model_rebuild()
