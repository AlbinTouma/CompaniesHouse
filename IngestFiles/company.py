import pandas as pd
import csv
from dataclasses import asdict
import json
import psycopg2
from db import *
from models import Company, Address
import db

#CompanyName, CompanyNumber,
# RegAddress.CareOf,RegAddress.POBox,RegAddress.AddressLine1, RegAddress.AddressLine2,RegAddress.PostTown,RegAddress.County,RegAddress.Country,RegAddress.PostCode,
# CompanyCategory,CompanyStatus,CountryOfOrigin,DissolutionDate,
# IncorporationDate,Accounts.AccountRefDay,Accounts.AccountRefMonth,Accounts.NextDueDate,
# Accounts.LastMadeUpDate,Accounts.AccountCategory,Returns.NextDueDate,Returns.LastMadeUpDate,Mortgages.NumMortCharges,
# Mortgages.NumMortOutstanding,Mortgages.NumMortPartSatisfied,Mortgages.NumMortSatisfied,
# SICCode.SicText_1,SICCode.SicText_2,SICCode.SicText_3,SICCode.SicText_4,LimitedPartnerships.NumGenPartners,LimitedPartnerships.NumLimPartners,URI,PreviousName_1.CONDATE, PreviousName_1.CompanyName, PreviousName_2.CONDATE, PreviousName_2.CompanyName,PreviousName_3.CONDATE, PreviousName_3.CompanyName,PreviousName_4.CONDATE, PreviousName_4.CompanyName,PreviousName_5.CONDATE, PreviousName_5.CompanyName,PreviousName_6.CONDATE, PreviousName_6.CompanyName,PreviousName_7.CONDATE, PreviousName_7.CompanyName,PreviousName_8.CONDATE, PreviousName_8.CompanyName,PreviousName_9.CONDATE, PreviousName_9.CompanyName,PreviousName_10.CONDATE, PreviousName_10.CompanyName,ConfStmtNextDueDate, ConfStmtLastMadeUpDate


class IngestCompany:
    
    
    def ingest_company(self):

        with open('ukch.csv', 'r') as file:
            csvReader = csv.reader(file)
            companies = []
            for index, item in enumerate(csvReader):
                if index == 0:
                    continue

                company = Company(
                    CompanyName=item[0],
                    CompanyNumber=item[1],
                    CompanyCategory=item[10],
                    CompanyStatus=item[11],
                    CountryOfOrigin=item[12],
                    DissolutionDate=item[13],
                    IncorporationDate=item[14],
                    Address=Address(
                        AddressLine1=item[4],
                        AddressLine2=item[5],
                        PostTown=item[6],
                        PostCode=item[9],
                        PostBox=item[3],
                        CareOf=item[2],
                        Country=item[8],
                        County=item[7],
                        Premises='',
                    )
                )

                companies.append(company)

                if len(companies) >= 100:
                    db.insert_company(conn, companies)
                    companies = []
        
        conn.close()
        print('JOB DONE')



"""
with conn.cursor() as cur:
        data = [
        (
            company.CompanyNumber,
            company.CompanyName,
            company.CompanyCategory, 
            company.CompanyStatus,
            company.DissolutionDate, 
            company.IncorporationDate, 
            company.Address.FullAddress, 
            company.Address.CareOf, 
            company.Address.PostBox,
            company.Address.AddressLine1,
            company.Address.AddressLine2, 
            company.Address.PostTown, 
            company.Address.County,
            company.Address.Country, 
            company.Address.PostCode
        )   
        for company in companies
        ]
        try:
            cur.executemany(query, data)
            conn.commit()
        except Exception as e:
            print(f"Failed to insert company into table: {e}")
            quit()
    

"""