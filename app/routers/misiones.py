from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import Mision

router = APIRouter(prefix="/misiones", tags=["Misiones"])


@router.get("/", response_model=List[Mision])
def listar_misiones(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    misiones = session.exec(select(Mision).where(Mision.activo == True).offset(skip).limit(limit)).all()
    return misiones


@router.get("/{mision_id}", response_model=Mision)
def obtener_mision(mision_id: int, session: Session = Depends(get_session)):
    mision = session.get(Mision, mision_id)
    if not mision or not mision.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o inactiva")
    return mision


@router.post("/", response_model=Mision, status_code=201)
def crear_mision(mision: Mision, session: Session = Depends(get_session)):
    session.add(mision)
    session.commit()
    session.refresh(mision)
    return mision


@router.put("/{mision_id}", response_model=Mision)
def remplazar_mision(mision_id: int, datos_actualizados: Mision, session: Session = Depends(get_session)):
    mision_db = session.get(Mision, mision_id)
    if not mision_db or not mision_db.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o inactiva")
    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(mision_db, key, value)
    session.add(mision_db)
    session.commit()
    session.refresh(mision_db)
    return mision_db


@router.patch("/{mision_id}", response_model=Mision)
def actualizar_mision(mision_id: int, datos_parciales: dict, session: Session = Depends(get_session)):
    mision_db = session.get(Mision, mision_id)
    if not mision_db or not mision_db.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o inactiva")
    for key, value in datos_parciales.items():
        setattr(mision_db, key, value)
    session.add(mision_db)
    session.commit()
    session.refresh(mision_db)
    return mision_db


@router.delete("/{mision_id}")
def eliminar_mision(mision_id: int, session: Session = Depends(get_session)):
    mision_db = session.get(Mision, mision_id)
    if not mision_db:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    mision_db.activo = False
    session.add(mision_db)
    session.commit()
    return {"mensaje": f"Misión '{mision_db.titulo}' marcada como inactiva"}
