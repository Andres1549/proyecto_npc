from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import Ubicacion

router = APIRouter()

@router.get("/", response_model=List[Ubicacion])
def listar_ubicaciones(skip: int = 0, limit: int = Query(20, le=200), session: Session = Depends(get_session)):
    return session.exec(select(Ubicacion).offset(skip).limit(limit)).all()

@router.get("/{ubicacion_id}", response_model=Ubicacion)
def obtener_ubicacion(ubicacion_id: int, session: Session = Depends(get_session)):
    u = session.get(Ubicacion, ubicacion_id)
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return u

@router.post("/", response_model=Ubicacion)
def crear_ubicacion(u: Ubicacion, session: Session = Depends(get_session)):
    session.add(u)
    session.commit()
    session.refresh(u)
    return u

@router.patch("/{ubicacion_id}", response_model=Ubicacion)
def actualizar_ubicacion(ubicacion_id: int, data: Ubicacion, session: Session = Depends(get_session)):
    u = session.get(Ubicacion, ubicacion_id)
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(u, key, value)
    session.add(u)
    session.commit()
    session.refresh(u)
    return u

@router.delete("/{ubicacion_id}")
def eliminar_ubicacion(ubicacion_id: int, session: Session = Depends(get_session)):
    u = session.get(Ubicacion, ubicacion_id)
    if not u:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    session.delete(u)
    session.commit()
    return {"ok": True}
