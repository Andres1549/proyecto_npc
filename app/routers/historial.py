from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.db import get_session
from app.models import NPC, Ubicacion

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def ver_historial(request: Request, session: Session = Depends(get_session)):
    npcs_inactivos = session.exec(
        select(NPC).where(NPC.activo == False)
    ).all()

    ubicaciones_inactivas = session.exec(
        select(Ubicacion).where(Ubicacion.activo == False)
    ).all()

    return templates.TemplateResponse(
        "historial.html",
        {
            "request": request,
            "npcs": npcs_inactivos,
            "ubicaciones": ubicaciones_inactivas
        }
    )
