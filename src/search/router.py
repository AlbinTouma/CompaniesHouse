from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from src.config import engine, templates
from sqlmodel import Session, select, create_engine
from src.models.company import Company
from src.models.psc import PSC

router = APIRouter(
    prefix='/search'
)


@router.post("/", response_class=HTMLResponse) 
def get_item(request: Request, query: str = Form(...)):
    with Session(engine) as session:
        statement = select(Company).where(Company.name == query)
        row = session.exec(statement).first()
        if row is None:
            return HTMLResponse(
                content="""<p>NO data</p>""",
                status_code=404
                )
        row: list = session.exec(select(PSC).where(PSC.company_id == row.id)).all()
       
        row = row[0]
        print(row)
        print(f"Found data for query {row.model_dump()}")
        
       
    return templates.TemplateResponse(
        "result.html", 
        {"request": request, "bods_json": jsonable_encoder(row.model_dump())}
        )


