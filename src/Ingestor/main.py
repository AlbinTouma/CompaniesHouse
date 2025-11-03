from db import SqliteClass
from IngestFiles import CompanyIngestor, PscIngestor
from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///ukch.db")
SQLModel.metadata.create_all(engine)

ingestor = PscIngestor(engine=engine)
ingestor.ingest_psc()
#company  = CompanyIngestor(engine=engine)
#company.ingest_companies()

#ingestor = CompanyIngestor(engine=engine)
#ingestor.ingest_companies()


#sqlite_db = SqliteClass()
#sqlite_db.init_sqlite()
#sqlite_db.execute_query('create_companies_table.sql')
#sqlite_db.execute_query('create_psc_table.sql')

#company_ingestor = CompanyIngestor()
#company_ingestor.ingest_companies(sqlite_db)

#psc_ingestor = PscIngestor()
#psc_ingestor.ingest_psc(sqlite_db)
#sqlite_db.close_connection()

