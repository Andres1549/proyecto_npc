from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import Mision

router = APIRouter()

@router.get("/", response_model=List[Mision])
def listar_misiones(skip: int = 0, limit: int = Query(10, le=100), session: Session = Depends(get_session)):
    return session.exec(select(Mision).offset(skip).limit(limit)).all()

@router.get("/{mision_id}", response_model=Mision)
def obtener_mision(mision_id: int, session: Session = Depends(get_session)):
    mision = session.get(Mision, mision_id)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return mision

@router.post("/", response_model=Mision)
def crear_mision(mision: Mision, session: Session = Depends(get_session)):
    session.add(mision)
    session.commit()
    session.refresh(mision)
    return mision

@router.patch("/{mision_id}", response_model=Mision)
def actualizar_mision(mision_id: int, data: Mision, session: Session = Depends(get_session)):
    mision = session.get(Mision, mision_id)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(mision, key, value)
    session.add(mision)
    session.commit()
    session.refresh(mision)
    return mision

@router.delete("/{mision_id}")
def eliminar_mision(mision_id: int, session: Session = Depends(get_session)):
    mision = session.get(Mision, mision_id)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    mision.activo = False
    session.add(mision)
    session.commit()
    return {"ok": True}
