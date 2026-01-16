import csv
from src.schemas.company import CompanyRead
from src.schemas.address import AddressRead
from src.models.company import CompanySQL
import json
from sqlmodel import Session
from src.config import engine
from tqdm import tqdm

print("RUNNING PSC INGESTOR")
BATCH = 100

with open('companies.csv', 'r') as file:
    total_rows = sum(1 for _ in file)
    file.seek(0)  # reset to start
    csvReader = csv.reader(file, quotechar='"', delimiter=',', skipinitialspace=True)

    next(csvReader)
    with Session(engine) as session:
        companies_list = []
        for item in tqdm(csvReader, total=total_rows, desc="Ingesting companies"):
            address=AddressRead(
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


            companyRead = CompanyRead(
                name=item[0],
                id=item[1],
                category=item[10],
                status=item[11],
                country_origin=item[12],
                dissolution_date=item[13],
                incorporation_date=item[14],
                address=address
                )


            try:
                sqlModel = CompanySQL.model_validate(companyRead.model_dump())
                companies_list.append(sqlModel)
            except Exception as e:
                print("Error is", e)



            if len(companies_list) > BATCH:
                for company in companies_list:
                    session.merge(company)
                session.commit()
                companies_list.clear()


        if companies_list:
            for company in companies_list:
                session.merge(company)
            session.commit()
            companies_list.clear()

        print("COMPANIES INGESTED")


