from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///ukch.db")
templates = Jinja2Templates(directory="templates")
