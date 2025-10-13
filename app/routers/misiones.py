from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select
from app.db import get_session
from app.models import Mision

router = APIRouter()

@router.get("/", response_model=List[Mision])
def list_mision(skip: int = 0, limit: int = Query(10, le=100), session: Session = Depends(get_session)):
    q = select(Mision).offset(skip).limit(limit)
    return session.exec(q).all()

@router.post("/", response_model=Mision)
def create_mision(obj: Mision, session: Session = Depends(get_session)):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/{obj_id}", response_model=Mision)
def get_mision(obj_id: int, session: Session = Depends(get_session)):
    obj = session.get(Mision, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Mision no encontrado")
    return obj

@router.patch("/{obj_id}", response_model=Mision)
def update_mision(obj_id: int, obj_update: Mision, session: Session = Depends(get_session)):
    obj = session.get(Mision, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Mision no encontrado")
    obj_data = obj_update.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(obj, key, value)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.delete("/{obj_id}")
def delete_mision(obj_id: int, session: Session = Depends(get_session)):
    obj = session.get(Mision, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Mision no encontrado")
    session.delete(obj)
    session.commit()
    return {"ok": True}