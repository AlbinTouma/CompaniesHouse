from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, create_engine
import logging
import json

engine = create_engine("sqlite:///ukch.db")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


