import json
from dataclasses import dataclass, field, asdict
import psycopg2
from datetime import datetime
from models.company import *
from db.sqlite_db import *
from models import PSC, Identification, Name, DateOfBirth

conn = connect_db()
execute_query(conn, 'sql/create_psc.sql')

class IngestPSC:
    def convert_datetime(obj):
        return datetime.fromisoformat(obj.replace('Z', '+00:00'))

    def create_object(self, obj: dict) -> PSC:
        return PSC(
                CompanyNumber=obj.get('company_number', ''),  # Default to empty string if 'company_number' is missing
                Address=Address(
                    AddressLine1=obj.get('data', {}).get('address', {}).get('address_line_1', ''),
                    AddressLine2=obj.get('data', {}).get('address', {}).get('address_line_2', ''),
                    Country=obj.get('data', {}).get('address', {}).get('country', ''),
                    PostTown=obj.get('data', {}).get('address', {}).get('locality', ''),
                    PostCode=obj.get('data', {}).get('address', {}).get('postal_code', ''),
                    Premises=obj.get('data', {}).get('address', {}).get('premises', ''),
                    CareOf=obj.get('data', {}).get('address', {}).get('care_of', ''),
                    PostBox=obj.get('data', {}).get('address', {}).get('post_box', ''),
                    County=obj.get('data', {}).get('address', {}).get('region', '')
                ),
                Identification=Identification(
                    CountryRegistered=obj.get('data', {}).get('identification', {}).get('country_registered', ''),
                    LegalAuthority=obj.get('data', {}).get('identification', {}).get('legal_authority', ''),
                    LegalForm=obj.get('data', {}).get('identification', {}).get('legal_form', ''),
                    PlaceRegistered=obj.get('data', {}).get('identification', {}).get('place_registered', ''),
                    RegistrationNumber=obj.get('data', {}).get('identification', {}).get('registration_number', '')
                ),


                Kind=obj.get('data', {}).get('kind', ''),
                Etag=obj.get('data', {}).get('etag', ''),
                Name=Name(
                    FullName=obj.get('data', {}).get('name'),
                    Firstname=obj.get('data', {}).get('name_elements', {}).get('forename', ''),
                    Middlename=obj.get('data', {}).get('name_elements', {}).get('middlename', ''),
                    Surname=obj.get('data', {}).get('name_elements', {}).get('surname', ''),
                    Title=obj.get('data', {}).get('name_elements', {}).get('title', ''),
                    ),

                DateOfBirth=DateOfBirth(
                    Year=obj.get('data', {}).get('date_of_birth', {}).get('year'),
                    Month=obj.get('data', {} ).get('date_of_birth', {}).get('month')
                ),
                Nationality=obj.get('data', {}).get('nationality'),
                CeasedOn=None if obj.get('data', {}).get('ceased_on', '') == '' else self.convert_datetime(obj.get('data', {}).get('ceased_on', '')),
                CountryOfResidence=obj.get('data', {}).get('country_of_residence'),
                Links=json.dumps(obj.get('data', {}).get('links', {})),  # Default to empty dict if 'links' is missing
                NaturesControl=obj.get('data', {}).get('natures_of_control', []),  # Default to empty list if 'natures_of_control' is missing
                NotifiedOn=None if obj.get('data', {}).get('notified_on', '') == '' else datetime.strptime(obj.get('data', {}).get('notified_on', ''), '%Y-%m-%d')
            )

    def ingest_psc(self)
        bulk = []
        with open('psc.txt', 'r') as file:
            for index, line in enumerate(file):
                obj = json.loads(line)
                print(f"creating object for {index}")
                psc = self.create_object(obj)
                bulk.append(psc)
                
                if len(bulk) >= 500:
                    data = [(
                        psc.CompanyNumber, 
                        psc.Name.FullName,
                        psc.Kind,
                        psc.Etag,
                        psc.Name.Firstname,
                        psc.Name.Middlename,
                        psc.Name.Surname,
                        psc.Name.Title,
                        psc.DateOfBirth.Year,
                        psc.DateOfBirth.Month,
                        psc.Nationality,
                        psc.CountryOfResidence,
                        psc.Identification.CountryRegistered,
                        psc.Identification.LegalAuthority,
                        psc.Identification.LegalForm,
                        psc.Identification.PlaceRegistered,
                        psc.Identification.RegistrationNumber,
                        psc.NotifiedOn,
                        psc.CeasedOn,
                        psc.Links,
                        psc.NaturesControl,
                        psc.Address.FullAddress,
                        psc.Address.CareOf,
                        psc.Address.PostBox,
                        psc.Address.AddressLine1,
                        psc.Address.AddressLine2,
                        psc.Address.Premises,
                        psc.Address.PostTown,
                        psc.Address.County,
                        psc.Address.Country,
                        psc.Address.PostCode
                    
                    ) for psc in bulk
                    ]  
            
            
            
                    execute_bulk_insert(conn, 'sql/insert_psc.sql', data)
                    bulk = []
                    print('Loading batch')


        
        if bulk:
            data = [(
                    psc.CompanyNumber, 
                    psc.Name.FullName,
                    psc.Kind,
                    psc.Etag,
                    psc.Name.Firstname,
                    psc.Name.Middlename,
                    psc.Name.Surname,
                    psc.Name.Title,
                    psc.DateOfBirth.Year,
                    psc.DateOfBirth.Month,
                    psc.Nationality,
                    psc.CountryOfResidence,
                    psc.Identification.CountryRegistered,
                    psc.Identification.LegalAuthority,
                    psc.Identification.LegalForm,
                    psc.Identification.PlaceRegistered,
                    psc.Identification.RegistrationNumber,
                    psc.NotifiedOn,
                    psc.CeasedOn,
                    psc.Links,
                    psc.NaturesControl,
                    psc.Address.FullAddress,
                    psc.Address.CareOf,
                    psc.Address.PostBox,
                    psc.Address.AddressLine1,
                    psc.Address.AddressLine2,
                    psc.Address.Premises,
                    psc.Address.PostTown,
                    psc.Address.County,
                    psc.Address.Country,
                    psc.Address.PostCode

            ) for psc in bulk
            ]
            execute_bulk_insert(conn, 'sql/insert_psc.sql', data)
            print('Loading final batch')



                
