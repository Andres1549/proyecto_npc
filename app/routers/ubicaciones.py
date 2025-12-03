from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query,Request
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import Ubicacion
from app.servicios.supabase_conexion import upload_file
from fastapi.responses import HTMLResponse
from app.utils.templates import templates
from fastapi.responses import RedirectResponse
router = APIRouter()

@router.get("/{ubicacion_id}")
def detalle_ubicacion(ubicacion_id: int, request: Request, session: Session = Depends(get_session)):
    ubicacion = session.get(Ubicacion, ubicacion_id)
    if not ubicacion:
        return {"error": "Ubicación no encontrada"}

    npc_list = ubicacion.npcs  # gracias al Relationship

    return templates.TemplateResponse(
        "detalles/ubicacion_detalle.html",
        {
            "request": request,
            "ubicacion": ubicacion,
            "npc_list": npc_list
        }
    )

@router.post("/", response_model=Ubicacion, status_code=201)
async def crear_ubicacion(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    imagen_url = None
    if imagen:
        imagen_url = await upload_file(imagen)

    u = Ubicacion(nombre=nombre, descripcion=descripcion, imagen_url=imagen_url)
    session.add(u)
    session.commit()
    session.refresh(u)
    return u

@router.put("/{id}", response_model=Ubicacion)
async def reemplazar_ubicacion(
    id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    u = session.get(Ubicacion, id)
    if not u or not u.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o inactiva")

    if imagen:
        u.imagen_url = await upload_file(imagen)
    u.nombre = nombre
    u.descripcion = descripcion
    session.add(u)
    session.commit()
    session.refresh(u)
    return u
@router.get("/{id}/editar")
def form_editar_ubicacion(
    request: Request,
    id: int,
    session: Session = Depends(get_session)
):
    u = session.get(Ubicacion, id)
    if not u or not u.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    return templates.TemplateResponse("formularios/ubicacion_editar.html", {
        "request": request,
        "ubicacion": u
    })

@router.post("/{id}/editar")
async def actualizar_ubicacion_form(
    id: int,
    nombre: str = Form(None),
    descripcion: str = Form(None),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    # Llamamos tu mismo PATCH interno
    u = session.get(Ubicacion, id)
    if not u or not u.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    if imagen:
        u.imagen_url = await upload_file(imagen)
    if nombre is not None:
        u.nombre = nombre
    if descripcion is not None:
        u.descripcion = descripcion

    session.add(u)
    session.commit()

    return RedirectResponse(url=f"/ubicaciones/{id}", status_code=303)

@router.get("/{id}/eliminar")
def confirmar_eliminar_ubicacion(
    request: Request,
    id: int,
    session: Session = Depends(get_session)
):
    u = session.get(Ubicacion, id)
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    return templates.TemplateResponse("formularios/ubicacion_eliminar.html", {
        "request": request,
        "ubicacion": u,
    })

@router.post("/{id}/eliminar")
def eliminar_ubicacion_form(
    id: int,
    session: Session = Depends(get_session)
):
    u = session.get(Ubicacion, id)
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    u.activo = False

    session.add(u)
    session.commit()

    return RedirectResponse(url="/ubicaciones", status_code=303)


@router.get("/", response_class=HTMLResponse)
def listar_ubicaciones(request: Request, db: Session = Depends(get_session)):
    ubicaciones = db.query(Ubicacion).filter(Ubicacion.activo == True).all()
    return templates.TemplateResponse("listas/ubicaciones.html", {
        "request": request,
        "ubicaciones": ubicaciones
    })
