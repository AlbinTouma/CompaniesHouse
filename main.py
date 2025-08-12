from db import SqliteClass

sqlite_db = SqliteClass()
sqlite_db.init_sqlite()
sqlite_db.execute_query('create_companies_table.sql')