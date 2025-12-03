from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.db import get_session
from app.models import NPC, Ubicacion
from fastapi.responses import RedirectResponse

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
        "listas/historial.html",
        {
            "request": request,
            "npcs": npcs_inactivos,
            "ubicaciones": ubicaciones_inactivas
        }
    )

@router.get("/npc/{id}/restaurar")
def confirmar_restaurar_npc(
    request: Request,
    id: int,
    session: Session = Depends(get_session)
):
    npc = session.get(NPC, id)
    if not npc or npc.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o ya está activo")

    return templates.TemplateResponse("formularios/restaurar_confirmacion.html", {
        "request": request,
        "nombre": npc.nombre,
        "url_post": f"/historial/npc/{id}/restaurar",
        "url_volver": "/historial",
    })

@router.post("/npc/{id}/restaurar")
def restaurar_npc(id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, id)
    if not npc or npc.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o ya está activo")

    npc.activo = True
    session.add(npc)
    session.commit()
    session.refresh(npc)

    # Redirige a la página de detalle del NPC
    return RedirectResponse(url=f"/npcs/{id}", status_code=303)

@router.get("/ubicacion/{id}/restaurar")
def confirmar_restaurar_ubicacion(
    request: Request,
    id: int,
    session: Session = Depends(get_session)
):
    u = session.get(Ubicacion, id)
    if not u or u.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o ya está activa")

    return templates.TemplateResponse("formularios/restaurar_confirmacion.html", {
        "request": request,
        "nombre": u.nombre,
        "url_post": f"/historial/ubicacion/{id}/restaurar",
        "url_volver": "/historial",
    })

@router.post("/ubicacion/{id}/restaurar")
def restaurar_ubicacion(id: int, session: Session = Depends(get_session)):
    u = session.get(Ubicacion, id)
    if not u or u.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o ya está activa")

    u.activo = True
    session.add(u)
    session.commit()
    session.refresh(u)
    return RedirectResponse(url=f"/ubicaciones/{id}", status_code=303)