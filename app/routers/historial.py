from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, Session

from app.db import get_session
from app.models import NPC, Ubicacion, Item, Mision

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def ver_historial(request: Request, session: Session = Depends(get_session)):
    npcs_inactivos = session.exec(select(NPC).where(NPC.activo == False)).all()
    ubicaciones_inactivas = session.exec(select(Ubicacion).where(Ubicacion.activo == False)).all()
    items_inactivos = session.exec(select(Item).where(Item.activo == False)).all()
    misiones_inactivas = session.exec(select(Mision).where(Mision.activo == False)).all()

    return templates.TemplateResponse("listas/historial.html", {
        "request": request,
        "npcs": npcs_inactivos,
        "ubicaciones": ubicaciones_inactivas,
        "items": items_inactivos,
        "misiones": misiones_inactivas
    })

@router.get("/npc/{id}/restaurar")
def confirmar_restaurar_npc(request: Request, id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, id)
    if not npc or npc.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o ya está activo")

    return templates.TemplateResponse("formularios/restaurar_confirmacion.html", {
        "request": request,
        "nombre": npc.nombre,
        "url_post": f"/historial/recuperar/npc/{id}",
        "url_volver": "/historial",
    })


@router.get("/ubicacion/{id}/restaurar")
def confirmar_restaurar_ubicacion(request: Request, id: int, session: Session = Depends(get_session)):
    ubicacion = session.get(Ubicacion, id)
    if not ubicacion or ubicacion.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o ya está activa")

    return templates.TemplateResponse("formularios/restaurar_confirmacion.html", {
        "request": request,
        "nombre": ubicacion.nombre,
        "url_post": f"/historial/recuperar/ubicacion/{id}",
        "url_volver": "/historial",
    })


@router.get("/item/{id}/restaurar")
def confirmar_restaurar_item(request: Request, id: int, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item or item.activo:
        raise HTTPException(status_code=404, detail="Objeto no encontrado o ya está activo")

    return templates.TemplateResponse("formularios/restaurar_confirmacion.html", {
        "request": request,
        "nombre": item.nombre,
        "url_post": f"/historial/recuperar/item/{id}",
        "url_volver": "/historial",
    })


@router.get("/mision/{id}/restaurar")
def confirmar_restaurar_mision(request: Request, id: int, session: Session = Depends(get_session)):
    mision = session.get(Mision, id)
    if not mision or mision.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o ya está activa")

    return templates.TemplateResponse("formularios/restaurar_confirmacion.html", {
        "request": request,
        "nombre": mision.titulo,
        "url_post": f"/historial/recuperar/mision/{id}",
        "url_volver": "/historial",
    })

@router.post("/recuperar/{modelo}/{id}")
def recuperar(request: Request, modelo: str, id: int, session: Session = Depends(get_session)):
    modelo = modelo.lower()
    target = None

    if modelo == "npc":
        target = session.get(NPC, id)
    elif modelo == "ubicacion":
        target = session.get(Ubicacion, id)
    elif modelo == "item":
        target = session.get(Item, id)
    elif modelo == "mision":
        target = session.get(Mision, id)
    else:
        raise HTTPException(status_code=400, detail="Modelo desconocido")

    if not target:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    target.activo = True
    session.add(target)
    session.commit()
    return RedirectResponse(url="/historial", status_code=303)