from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
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
        company = session.exec(statement).first()
        if company is None:
            return HTMLResponse(
                content="""<p>NO data</p>""",
                )
        

        
        result = {
                "company": company.model_dump(),
                "psc": company.psc.model_dump()
                }
    return templates.TemplateResponse(
        "result.html", 
        {"request": request, "bods_json": result}
        )


