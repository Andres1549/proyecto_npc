from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select
from app.db import get_session
from app.models import Vendedor

router = APIRouter()

@router.get("/", response_model=List[Vendedor])
def list_vendedor(skip: int = 0, limit: int = Query(10, le=100), session: Session = Depends(get_session)):
    q = select(Vendedor).offset(skip).limit(limit)
    return session.exec(q).all()

@router.post("/", response_model=Vendedor)
def create_vendedor(obj: Vendedor, session: Session = Depends(get_session)):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/{obj_id}", response_model=Vendedor)
def get_vendedor(obj_id: int, session: Session = Depends(get_session)):
    obj = session.get(Vendedor, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    return obj

@router.patch("/{obj_id}", response_model=Vendedor)
def update_vendedor(obj_id: int, obj_update: Vendedor, session: Session = Depends(get_session)):
    obj = session.get(Vendedor, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    obj_data = obj_update.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(obj, key, value)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.delete("/{obj_id}")
def delete_vendedor(obj_id: int, session: Session = Depends(get_session)):
    obj = session.get(Vendedor, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    session.delete(obj)
    session.commit()
    return {"ok": True}