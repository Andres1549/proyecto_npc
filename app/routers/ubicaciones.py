from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import Ubicacion
from app.servicios.supabase_conexion import upload_file

router = APIRouter()

@router.get("/", response_model=List[Ubicacion])
def listar_ubicaciones(session: Session = Depends(get_session), skip: int = Query(0), limit: int = Query(50)):
    return session.exec(select(Ubicacion).where(Ubicacion.activo == True).offset(skip).limit(limit)).all()

@router.get("/{id}", response_model=Ubicacion)
def obtener_ubicacion(id: int, session: Session = Depends(get_session)):
    u = session.get(Ubicacion, id)
    if not u or not u.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o inactiva")
    return u

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

@router.patch("/{id}", response_model=Ubicacion)
async def actualizar_ubicacion(
    id: int,
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    u = session.get(Ubicacion, id)
    if not u or not u.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o inactiva")

    if imagen:
        u.imagen_url = await upload_file(imagen)
    if nombre is not None:
        u.nombre = nombre
    if descripcion is not None:
        u.descripcion = descripcion

    session.add(u)
    session.commit()
    session.refresh(u)
    return u

@router.delete("/{id}")
def eliminar_ubicacion(id: int, session: Session = Depends(get_session)):
    u = session.get(Ubicacion, id)
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    u.activo = False
    session.add(u)
    session.commit()
    return {"mensaje": "Ubicación marcada como inactiva"}
