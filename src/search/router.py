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



@router.get("/company_name/{q}", response_model=CompanyRead)
def get_company(request: Request,q: str) -> CompanyRead:
    """Get firmographics by company name.
    
    :param request: FastAPI Request object
    :param q: Company name to search for
    :return: CompanyRead
    
    """

    logger.info("Query is:", q)
    with Session(engine) as session:
        sql_query  = select(CompanySQL).where(CompanySQL.name == q)
        company: CompanySQL = session.exec(sql_query).first()
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        company = CompanyRead.model_validate(company.model_dump())

        return company


@router.get("/company_id/{company_id}", response_model=CompanyRead)
def get_company_by_id(request: Request, company_id: str) -> CompanyRead:
    """Get firmographics by company name.
    :param request: FastAPI Request object
    :param company_id: Company id to search for
    :return: CompanyRead
    
    """
    logger.info(f"QUERYING -> {company_id}")
    with Session(engine) as session:
        sql_query  = select(CompanySQL).where(CompanySQL.id == company_id)
        company: CompanySQL = session.exec(sql_query).first()
        logger.info(type(company))
        logger.info(company.model_dump())
        companyRead = CompanyRead.model_validate(company.model_dump())
        return companyRead


@router.get("/company_full/{company_name}", response_model=CompanyWithPSC)
def get_company_pscs(request: Request,company_name: str) -> CompanyWithPSC:
    """Get firmographics and a list of persons with significant control by company name
    
    :param request: FastAPI Request object
    :param q: Company name to search for
    :return: CompanyWithPSC
    
    """
    
    logger.info("Query is %s:", q)
    with Session(engine) as session:
        sql_query  =  (
            select(CompanySQL)
            .where(CompanySQL.name == comppany_name)
            .options(selectinload(CompanySQL.psc))
        )

        logger.info("SQL Query: %s", sql_query)
        company: CompanySQL = session.exec(sql_query).one_or_none()
        companyWithPSC = CompanyWithPSC.model_validate(company)
        return companyWithPSC


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

    
