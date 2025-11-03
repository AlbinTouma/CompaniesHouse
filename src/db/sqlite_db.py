"""
CompaniesHouse allows users to ingest UKCH active companies, officers, and owners into a sqlite database on disk. 

"""


import pandas as pd
import csv
from dataclasses import asdict
import json
import sqlite3
from pathlib import Path
import logging


class SqliteClass:
    BASE_DIR = Path(__file__).resolve().parent.parent

    def __init__(self, db_name='data.db'):

        print(SqliteClass.BASE_DIR)
        self.db_name = db_name
        self.conn =  sqlite3.connect(f'{SqliteClass.BASE_DIR}/{db_name}')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
                
    def load_query(self, filename):
        print(SqliteClass.BASE_DIR)
        with open(f'{SqliteClass.BASE_DIR}/sql/{filename}', 'r') as file:
            return file.read()
        
    def execute_query(self, filename, params={}) -> list[dict]:
        query = self.load_query(filename)
        self.cursor.execute(query, params)
        self.conn.commit()
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def execute_bulk_insert(self, filename, data: list):
        try:
            query = self.load_query(filename)
            cur = self.conn.cursor()
            cur.executemany(query, data)
            self.conn.commit()
        except Exception as e:
            print(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print('Closed connection to database')
            
