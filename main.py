import logging
import databases
import sqlalchemy
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from model import metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILENAME = 'my_database.db'
DATABASE_URL = f"sqlite:///{DB_FILENAME}"
database = databases.Database(DATABASE_URL) #, connect_args={"check_same_thread": False}

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return RedirectResponse("/tasks")

# Запуск:
# uvicorn main:app --reload
