from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import Item

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=List[Item])
def listar_items(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    items = session.exec(select(Item).where(Item.activo == True).offset(skip).limit(limit)).all()
    return items


@router.get("/{item_id}", response_model=Item)
def obtener_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item or not item.activo:
        raise HTTPException(status_code=404, detail="Item no encontrado o inactivo")
    return item


@router.post("/", response_model=Item, status_code=201)
def crear_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{item_id}", response_model=Item)
def remplazar_item(item_id: int, datos_actualizados: Item, session: Session = Depends(get_session)):
    item_db = session.get(Item, item_id)
    if not item_db or not item_db.activo:
        raise HTTPException(status_code=404, detail="Item no encontrado o inactivo")
    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(item_db, key, value)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db


@router.patch("/{item_id}", response_model=Item)
def actualizar_item(item_id: int, datos_parciales: dict, session: Session = Depends(get_session)):
    item_db = session.get(Item, item_id)
    if not item_db or not item_db.activo:
        raise HTTPException(status_code=404, detail="Item no encontrado o inactivo")
    for key, value in datos_parciales.items():
        setattr(item_db, key, value)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db


@router.delete("/{item_id}")
def eliminar_item(item_id: int, session: Session = Depends(get_session)):
    item_db = session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    item_db.activo = False
    session.add(item_db)
    session.commit()
    return {"mensaje": f"Item '{item_db.nombre}' marcado como inactivo"}
