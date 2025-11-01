import pandas as pd
import csv
from dataclasses import asdict
from data_models import Address, Company
from tqdm import tqdm
from sqlmodel import Session, select
#CompanyName, CompanyNumber,
# RegAddress.CareOf,RegAddress.POBox,RegAddress.AddressLine1, RegAddress.AddressLine2,RegAddress.PostTown,RegAddress.County,RegAddress.Country,RegAddress.PostCode,
# CompanyCategory,CompanyStatus,CountryOfOrigin,DissolutionDate,
# IncorporationDate,Accounts.AccountRefDay,Accounts.AccountRefMonth,Accounts.NextDueDate,
# Accounts.LastMadeUpDate,Accounts.AccountCategory,Returns.NextDueDate,Returns.LastMadeUpDate,Mortgages.NumMortCharges,
# Mortgages.NumMortOutstanding,Mortgages.NumMortPartSatisfied,Mortgages.NumMortSatisfied,
# SICCode.SicText_1,SICCode.SicText_2,SICCode.SicText_3,SICCode.SicText_4,LimitedPartnerships.NumGenPartners,LimitedPartnerships.NumLimPartners,URI,PreviousName_1.CONDATE, PreviousName_1.CompanyName, PreviousName_2.CONDATE, PreviousName_2.CompanyName,PreviousName_3.CONDATE, PreviousName_3.CompanyName,PreviousName_4.CONDATE, PreviousName_4.CompanyName,PreviousName_5.CONDATE, PreviousName_5.CompanyName,PreviousName_6.CONDATE, PreviousName_6.CompanyName,PreviousName_7.CONDATE, PreviousName_7.CompanyName,PreviousName_8.CONDATE, PreviousName_8.CompanyName,PreviousName_9.CONDATE, PreviousName_9.CompanyName,PreviousName_10.CONDATE, PreviousName_10.CompanyName,ConfStmtNextDueDate, ConfStmtLastMadeUpDate


class CompanyIngestor:

    def __init__(self, engine):
        self.engine  = engine

    def ingest_companies(self):
        with open('companies.csv', 'r') as file:
            total_rows = sum(1 for _ in file) - 1  # skip header
            file.seek(0)  # reset to start
            csvReader = csv.reader(file)
            next(csvReader)  # skip header
          
            company_objects = []

            for _, item in enumerate(tqdm(csvReader, total=total_rows, desc="Ingesting companies")):
              
                    
                
                company = Company(
                    name=item[0],
                    id=item[1],
                    category=item[10],
                    company_status=item[11],
                    country_of_origin=item[12],
                    dissolution_date=item[13],
                    incorporation_date=item[14],
                    address_line_1=item[4],
                    address_line_2=item[5],
                    post_town=item[6],
                    post_code=item[9],
                    post_box=item[3],
                    care_of=item[2],
                    country=item[8],
                    county=item[7],
                    premises=None

                    )
                
                #company.compute_full_address()
                
                
                company_objects.append(company)

                if len(company_objects) >= 100:
                    self.bulk_insert(company_objects)
                    company_objects = []
            
            if company_objects:
                self.bulk_insert(company_objects)

    
    def bulk_insert(self, companies):
        with Session(self.engine) as session:
            session.add_all(companies)
            session.commit()
        
        print('JOB DONE')