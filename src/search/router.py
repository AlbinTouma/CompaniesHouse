from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from src.config import engine, templates
from sqlmodel import Session, select, create_engine
from sqlalchemy.orm import selectinload
from src.models.company import CompanySQL
from src.schemas.company import CompanyRead, CompanyWithPSC
from src.models.psc import PSC
from src.schemas.psc import PscRead, PscWithCompany
from src.config import logger
from fastapi import HTTPException


router = APIRouter(
    prefix='/search'
)


@router.get("/company", response_model=CompanyRead | CompanyWithPSC)
def search_company(
        request: Request,
        company_name: str = None, 
        company_id: str = None,
        include_psc: bool = None
        ):
    with Session(engine) as session:
        statement = select(CompanySQL)

        if company_id:
            statement = statement.where(CompanySQL.id == company_id)
        elif company_name:
            statement = statement.where(CompanySQL.name == company_name)
        else:
            raise HTTPException(status_code=400, detail="Must provide either company_id or company_name")

        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")

        if include_psc:
            return CompanyWithPSC.model_validate(result)
        return CompanyRead.model_validate(result)


@router.get("/psc", response_model=PscRead | PscWithCompany)
def search_psc(
        request: Request,
        name: str = None, 
        person_id: str = None,
        include_company: bool = None
        ):
    with Session(engine) as session:
        statement = select(PSC)

        if person_id:
            statement = statement.where(PSC.person_id == person_id)
        elif name:
            statement = statement.where(PSC.name == name)
        else:
            raise HTTPException(status_code=400, detail="Must provide either person_id or name of psc")

        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")

        if include_company:
            return PscWithCompany.model_validate(result)

        return PscRead.model_validate(result)







@router.get("/psc", response_model=PscRead)
def get_psc_by_company_number(request: Request, company_number: str) -> PscRead:
    """Get the first person with significant control by company number.

    :param request: FastAPI Request object
    :param company_number: Company number to search for
    :return: PscRead
    
    """

    with Session(engine) as session:
        sql_query  = select(PSC).where(PSC.company_id == company_number)
        psc: PSC = session.exec(sql_query).first()

        if psc is None:
            return {"data": "Not found"}

        return psc

@router.get("/psc-company", response_model=PscWithCompany)
def get_psc_with_company(request: Request, company_number: str) -> PscWithCompany:
    with Session(engine) as session:
        sql_query  = (
            select(PSC)
            .where(PSC.company_id == company_number)
            .options(selectinload(PSC.company))
        )
        psc: PSC = session.scalar(sql_query)
        psc = PscWithCompany.model_validate(psc)
        print(type(psc))
        print(psc.model_dump_json())

        if psc is None:
            return {"data": "Not found"}

        return psc

    
