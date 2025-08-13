from db import SqliteClass
from IngestFiles import CompanyIngestor

sqlite_db = SqliteClass()
sqlite_db.init_sqlite()
sqlite_db.execute_query('create_companies_table.sql')

company_ingestor = CompanyIngestor()
company_ingestor.ingest_companies(sqlite_db)

sqlite_db.close_connection()

