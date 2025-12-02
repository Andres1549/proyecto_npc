from app.db import init_db
from app.routers import npcs, items, misiones, ubicaciones, busqueda, reportes
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
load_dotenv()
app = FastAPI(title="Proyecto NPC")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    init_db()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
app.include_router(npcs, prefix="/npcs", tags=["NPCs"])
app.include_router(items, prefix="/items", tags=["Items"])
app.include_router(misiones, prefix="/misiones", tags=["Misiones"])
app.include_router(ubicaciones, prefix="/ubicaciones", tags=["Ubicaciones"])
app.include_router(reportes, prefix="/reportes", tags=["Reportes"])
app.include_router(busqueda, prefix="/global", tags=["Búsqueda Global"])
