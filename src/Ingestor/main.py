from src.Ingestor.company import CompanyIngestor 
from src.Ingestor.psc import PscIngestor
from sqlmodel import SQLModel, create_engine


engine = create_engine("sqlite:///ukch.db")
SQLModel.metadata.create_all(engine)

#ingestor = PscIngestor(engine=engine)
#ingestor.ingest_psc()

company  = CompanyIngestor(engine=engine)
company.ingest_companies()

