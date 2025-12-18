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



@router.get("/company", response_model=CompanyRead)
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

        return company



@router.get("/company-pscs", response_model=CompanyWithPSC)
def get_company_pscs(request: Request,q: str) -> CompanyWithPSC:
    """Get firmographics and a list of persons with significant control by company name
    
    :param request: FastAPI Request object
    :param q: Company name to search for
    :return: CompanyWithPSC
    
    """
    
    logger.info("Query is %s:", q)
    with Session(engine) as session:
        sql_query  =  (
            select(CompanySQL)
            .where(CompanySQL.name == q)
            .options(selectinload(CompanySQL.psc))
        )

        logger.info("SQL Query: %s", sql_query)
        company: CompanySQL = session.exec(sql_query).one_or_none()
        return company


@router.get("/psc", response_model=PscRead)
def get_psc_by_company_number(request: Request, company_number: int) -> PscRead:
    """Get the first person with significant control by company number.

    :param request: FastAPI Request object
    :param company_number: Company number to search for
    :return: PscRead
    
    """

    with Session(engine) as session:
        sql_query  = select(PSC).where(PSC.id == company_number)
        psc: PSC = session.exec(sql_query).first()
        if psc is None:
            return {"data": "Not found"}

        return psc

@router.get("/psc-company", response_model=PscWithCompany)
def get_psc_with_company(request: Request, company_number: int) -> PscWithCompany:
    with Session(engine) as session:
        sql_query  = select(PSC).where(PSC.id == company_number)
        psc: PSC = session.exec(sql_query).first()
        if psc is None:
            return {"data": "Not found"}

        return psc

