import pandas as pd
import csv
from classes import *
from dataclasses import asdict
import json
import psycopg2
from db import *
from secretdb import PASSWORD


def connect_db():
    try:
        return psycopg2.connect(
            dbname="company", 
            user="postgres", 
            password=PASSWORD,
            host="localhost"
            )
    except Exception as e:
        print("Failure to connect to database because of {e}")
        quit()

def load_query(filename):
    with open(filename, 'r') as file:
        return file.read()
    
def execute_query(conn, filename, params=None):
    query = load_query(filename)
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        conn.commit()

def execute_bulk_insert(conn, filename, data: list):
    query = load_query(filename)
    try:
        with conn.cursor() as cur:
            cur.executemany(query, data)
            conn.commit()
    except Exception as e:
        print(f"Exception {e}")
