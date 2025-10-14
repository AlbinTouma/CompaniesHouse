from typing import Union, Annotated
from fastapi import FastAPI, Form
from db.sqlite_db import SqliteClass
from data_models.bods import BODS_MAPPER  
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/search", response_class=HTMLResponse)
def get_item(request: Request, query: str = Form(...)):
    db = SqliteClass()
    company: list[dict] = db.execute_query('get_company.sql', params={'company_name': query,})
    psc: list[dict] = db.execute_query('get_psc.sql', params={"company_number": company[0]["company_number"],})


    bods = BODS_MAPPER(company,psc, officers=[]).map()
    print(psc)


    return templates.TemplateResponse("result.html", {"request": request, "bods_json": bods})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
