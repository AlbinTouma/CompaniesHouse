from src.models.psc import PSC
from src.schemas.psc import PscRead
from sqlmodel import Session
from src.config import engine
import json
from tqdm import tqdm


with open('psc.txt', 'r') as file:
    total_rows = sum(1 for _ in file)
    file.seek(0)  # reset to start
        
    with Session(engine) as session:
           
        pscsql_list: list[PSC] = []
        for line in tqdm(file, total=total_rows, desc="Ingest PSC"):

            psc_dict = json.loads(line)
            psc = PscRead.model_validate(psc_dict['data'])
            psc.company_number = psc_dict['company_number']

            # Create person id from the links url.
            person_id = psc_dict.get('data', {}).get('links', {}).get('self', '').rsplit('/', 1)[-1]
            psc.person_id = person_id
            
            psc_sql = PSC.model_validate(psc)            
            pscsql_list.append(psc_sql)

            if len(pscsql_list) > 100:
                for psc in pscsql_list:
                    session.merge(psc)
                session.commit()
                pscsql_list.clear()
                break
        
        if pscsql_list:
            for psc in pscsql_list:
                session.merge(psc)
            session.commit()
            pscsql_list.clear()

        print("INGESTION PROCESS COMPLETE")    