"""
CompaniesHouse allows users to ingest UKCH active companies, officers, and owners into a sqlite database on disk. 

"""


import pandas as pd
import csv
from dataclasses import asdict
import json
import sqlite3


class SqliteClass:
    def __init__(self, db_name='data.db'):
        self.conn = None
        self.db_name = db_name

    def init_sqlite(self):
        self.conn = sqlite3.connect(self.db_name)

    def load_query(self, filename):
        with open(f'sql/{filename}', 'r') as file:
            return file.read()
        
    def execute_query(self, filename, params=None):
        try:
            query = self.load_query(filename)
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)

    def execute_bulk_insert(self, filename, data: list):
        try:
            query = self.load_query(filename)
            cur = self.conn.cursor()
            cur.executemany(query, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            



