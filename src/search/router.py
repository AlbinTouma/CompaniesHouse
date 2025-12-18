from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from src.config import engine, templates
from sqlmodel import Session, select, create_engine
from sqlalchemy.orm import selectinload
from src.models.company import CompanySQL
from src.schemas.company import CompanyRead
from src.models.psc import PSC
from src.schemas.psc import PscRead
from src.config import logger

router = APIRouter(
    prefix='/search'
)



@router.get("/company", response_model=CompanyRead)
def get_company(request: Request,q: str) -> CompanyRead:
    logger.info("Query is:", q)
    with Session(engine) as session:
        sql_query  = select(CompanySQL).where(CompanySQL.name == q)
        company: CompanySQL = session.exec(sql_query).first()
        if company is None:
            return {"data": "Not found"}

        return company

@router.get("/company-pscs", response_model=CompanyRead)
def get_company_pscs(request: Request,q: str) -> CompanyRead:
    logger.info("Query is %s:", q)
    with Session(engine) as session:
        sql_query  =  (
            select(CompanySQL)
            .where(CompanySQL.name == q)
            .options(selectinload(CompanySQL.psc))
        )

        logger.info("SQL Query: %s", sql_query)
        company: CompanySQL = session.exec(sql_query).one_or_none()
        logger.info("Company fetched: %s", company)
        pscs_in_db = session.exec(select(PSC).where(PSC.company_id == "08209948")).all()
        print(f"DEBUG: Found {len(pscs_in_db)} PSCs directly in DB for this ID")
        print(company.psc)
        if company:
            _ = company.psc
            return company
        return company



@router.get("/psc", response_model=PscRead)
def get_psc_by_company_number(request: Request, company_number: int) -> PscRead:
    with Session(engine) as session:
        sql_query  = select(PSC).where(PSC.id == company_number)
        psc: PSC = session.exec(sql_query).first()
        if psc is None:
            return {"data": "Not found"}

        return psc


"""
@router.post("/", response_class=HTMLResponse) 
def get_item(request: Request, query: str = Form(...)):
    with Session(engine) as session:
        statement = select(Company).where(Company.name == query)
        company = session.exec(statement).first()
        if company is None:
            return HTMLResponse(
                content=<p>NO data</p>,
                status_code=404
                )
        psc: list = session.exec(select(PSC).where(PSC.company_id == company.id)).all()
        print(type(psc[0]))
        row = {"company": company, "psc_list": psc}
       
    return templates.TemplateResponse(
        "result.html", 
        {"request": request, "bods_json": jsonable_encoder(row)}
        )

"""
