from typing import Union, Annotated
from fastapi import FastAPI, Form
from db.sqlite_db import SqliteClass
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
        )


@app.get("/search/")
def read_root(request: Request, name: str):
    db = SqliteClass()
    entity: list[dict] = db.execute_query('get_company.sql', params={'entity_name': name})
    return templates.TemplateResponse('index.html',{
        "request": request,
        'name': f"Results for {name}",
        'data': entity})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
