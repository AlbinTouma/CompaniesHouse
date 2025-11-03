from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from src.config import templates

router = APIRouter(
    prefix='/search'
)



@router.post("/", response_class=HTMLResponse) #response_class=HTMLResponse)
def get_item(request: Request, query: str = Form(...)):
    result = jsonable_encoder({"company": "test"})
    return templates.TemplateResponse(
        "result.html", 
        {"request": request, "bods_json": result}
        )


