from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import Ubicacion

router = APIRouter(tags=["Ubicaciones"])


@router.get("/", response_model=List[Ubicacion])
def listar_ubicaciones(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    ubicaciones = session.exec(select(Ubicacion).where(Ubicacion.activo == True).offset(skip).limit(limit)).all()
    return ubicaciones


@router.get("/{ubicacion_id}", response_model=Ubicacion)
def obtener_ubicacion(ubicacion_id: int, session: Session = Depends(get_session)):
    ubicacion = session.get(Ubicacion, ubicacion_id)
    if not ubicacion or not ubicacion.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o inactiva")
    return ubicacion


@router.post("/", response_model=Ubicacion, status_code=201)
def crear_ubicacion(ubicacion: Ubicacion, session: Session = Depends(get_session)):
    session.add(ubicacion)
    session.commit()
    session.refresh(ubicacion)
    return ubicacion


@router.put("/{ubicacion_id}", response_model=Ubicacion)
def remplazar_ubicacion(ubicacion_id: int, datos_actualizados: Ubicacion, session: Session = Depends(get_session)):
    ubicacion_db = session.get(Ubicacion, ubicacion_id)
    if not ubicacion_db or not ubicacion_db.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o inactiva")
    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(ubicacion_db, key, value)
    session.add(ubicacion_db)
    session.commit()
    session.refresh(ubicacion_db)
    return ubicacion_db


@router.patch("/{ubicacion_id}", response_model=Ubicacion)
def actualizar_ubicacion(ubicacion_id: int, datos_parciales: dict, session: Session = Depends(get_session)):
    ubicacion_db = session.get(Ubicacion, ubicacion_id)
    if not ubicacion_db or not ubicacion_db.activo:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada o inactiva")
    for key, value in datos_parciales.items():
        setattr(ubicacion_db, key, value)
    session.add(ubicacion_db)
    session.commit()
    session.refresh(ubicacion_db)
    return ubicacion_db


@router.delete("/{ubicacion_id}")
def eliminar_ubicacion(ubicacion_id: int, session: Session = Depends(get_session)):
    ubicacion_db = session.get(Ubicacion, ubicacion_id)
    if not ubicacion_db:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    ubicacion_db.activo = False
    session.add(ubicacion_db)
    session.commit()
    return {"mensaje": f"Ubicación '{ubicacion_db.nombre}' marcada como inactiva"}
