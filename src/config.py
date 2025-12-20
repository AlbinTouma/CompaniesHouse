from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, create_engine
import logging
import json

engine = create_engine("sqlite:///ukch_2.db") #json_serializer=lambda obj: json.dumps(obj), json_deserializer=lambda s: json.loads(s))
SQLModel.metadata.create_all(engine)

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


