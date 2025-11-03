from typing import Union, Annotated
from fastapi import FastAPI, Form
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import uvicorn
from src.config import templates
from src.search.router import router

#https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")

#templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
