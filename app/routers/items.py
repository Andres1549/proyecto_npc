from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select
from app.db import get_session
from app.models import Item

router = APIRouter()

@router.get("/", response_model=List[Item])
def list_item(skip: int = 0, limit: int = Query(10, le=100), session: Session = Depends(get_session)):
    q = select(Item).offset(skip).limit(limit)
    return session.exec(q).all()

@router.post("/", response_model=Item)
def create_item(obj: Item, session: Session = Depends(get_session)):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/{obj_id}", response_model=Item)
def get_item(obj_id: int, session: Session = Depends(get_session)):
    obj = session.get(Item, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return obj

@router.patch("/{obj_id}", response_model=Item)
def update_item(obj_id: int, obj_update: Item, session: Session = Depends(get_session)):
    obj = session.get(Item, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    obj_data = obj_update.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(obj, key, value)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.delete("/{obj_id}")
def delete_item(obj_id: int, session: Session = Depends(get_session)):
    obj = session.get(Item, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    session.delete(obj)
    session.commit()
    return {"ok": True}