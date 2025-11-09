import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from src.models.util import Address,Identification, Name, DateOfBirth
from src.models.psc import PSC
from tqdm import tqdm
from sqlmodel import Session, select

class PscIngestor:
    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def convert_datetime(obj):
        return datetime.fromisoformat(obj.replace('Z', '+00:00'))

    def parse_full_address(self, obj: dict):
            order = ['address_line_1', 'address_line_2', 'premises', 'postal_code', 'locality', 'region','country'] 
            address = obj.get('data',{}).get('address')
            if address is None:
                return None

            data = {key: address[key] for key in order if key in address}
            return ', '.join(filter(None,[*data.values()]))

    def create_object(self, obj: dict) -> PSC:
        return PSC(
                company_id=obj.get('company_number', ''),  # Default to empty string if 'company_number' is missing
                full_address=self.parse_full_address(obj),
                address_line_1=obj.get('data', {}).get('address', {}).get('address_line_1', ''),
                address_line_2=obj.get('data', {}).get('address', {}).get('address_line_2', ''),
                country=obj.get('data', {}).get('address', {}).get('country', ''),
                post_town=obj.get('data', {}).get('address', {}).get('locality', ''),
                post_code=obj.get('data', {}).get('address', {}).get('postal_code', ''),
                premises=obj.get('data', {}).get('address', {}).get('premises', ''),
                care_of=obj.get('data', {}).get('address', {}).get('care_of', ''),
                post_box=obj.get('data', {}).get('address', {}).get('post_box', ''),
                county=obj.get('data', {}).get('address', {}).get('region', ''),
                country_registered=obj.get('data', {}).get('identification', {}).get('country_registered', ''),
                legal_authority=obj.get('data', {}).get('identification', {}).get('legal_authority', ''),
                legal_form=obj.get('data', {}).get('identification', {}).get('legal_form', ''),
                place_registered=obj.get('data', {}).get('identification', {}).get('place_registered', ''),
                registration_number=obj.get('data', {}).get('identification', {}).get('registration_number', ''),
                kind=obj.get('data', {}).get('kind', ''),
                etag=obj.get('data', {}).get('etag', ''),
                full_name=obj.get('data', {}).get('name'),
                first_name=obj.get('data', {}).get('name_elements', {}).get('forename', ''),
                middle_name=obj.get('data', {}).get('name_elements', {}).get('middlename', ''),
                surname=obj.get('data', {}).get('name_elements', {}).get('surname', ''),
                title=obj.get('data', {}).get('name_elements', {}).get('title', ''),
                year=obj.get('data', {}).get('date_of_birth', {}).get('year'),
                month=obj.get('data', {} ).get('date_of_birth', {}).get('month'),
                nationality=obj.get('data', {}).get('nationality'),
                ceasedOn=None if obj.get('data', {}).get('ceased_on', '') == '' else self.convert_datetime(obj.get('data', {}).get('ceased_on', '')),
                country_of_residence=obj.get('data', {}).get('country_of_residence'),
                links=json.dumps(obj.get('data', {}).get('links', {})),  # Default to empty dict if 'links' is missing
                natures_control=obj.get('data', {}).get('natures_of_control', []),  # Default to empty list if 'natures_of_control' is missing
                notified_on=None if obj.get('data', {}).get('notified_on', '') == '' else datetime.strptime(obj.get('data', {}).get('notified_on', ''), '%Y-%m-%d')
            )

    def ingest_psc(self):
        bulk = []
        with open('psc.txt', 'r') as file:
            total_rows = sum(1 for _ in file) - 1  # minus header
            file.seek(0)  # reset to start
            for index, line in enumerate(tqdm(file, total=total_rows, desc='Ingesting PSCs')):
                obj = json.loads(line)
                psc = self.create_object(obj)
                bulk.append(psc)    
                
                if len(bulk) >= 100000:
                    try:
                        self.bulk_insert(bulk)
                        bulk = []
                    except Exception as e:
                        print(e)


        
        if bulk:
            self.bulk_insert(bulk)
            print('Loading final batch')
    
    def bulk_insert(self, psc: list):
        with Session(self.engine) as session:
            session.add_all(psc)
            session.commit()
    





  


"""                data = [(
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
                        json.dumps(psc.Links),
                        json.dumps(psc.NaturesControl),
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
"""
