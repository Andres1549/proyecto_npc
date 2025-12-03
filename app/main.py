from app.db import init_db,get_session
from app.routers import npcs, items, misiones, ubicaciones, busqueda, reportes, historial
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from sqlmodel import select,Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.models import *
load_dotenv()
app = FastAPI(title="Proyecto NPC")

@app.on_event("startup")
def on_startup():
    init_db()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    ubicaciones = session.exec(select(Ubicacion).where(Ubicacion.activo == True)).all()
    historia = session.exec(select(NPC).where(NPC.tipo == "historia")).all()
    misiones = session.exec(select(NPC).where(NPC.tipo == "misiones")).all()
    vendedores = session.exec(select(NPC).where(NPC.tipo == "vendedor")).all()

    return templates.TemplateResponse("home.html", {
        "request": request,
        "ubicaciones": ubicaciones,
        "historia": historia,
        "misiones": misiones,
        "vendedor": vendedores
    })

app.include_router(npcs, prefix="/npcs", tags=["NPCs"])
app.include_router(items, prefix="/items", tags=["Items"])
app.include_router(misiones, prefix="/misiones", tags=["Misiones"])
app.include_router(ubicaciones, prefix="/ubicaciones", tags=["Ubicaciones"])
app.include_router(reportes, prefix="/reportes", tags=["Reportes"])
app.include_router(busqueda, prefix="/global", tags=["Búsqueda Global"])
app.include_router(historial, prefix="/historial", tags=["Historial"])
