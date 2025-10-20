from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlmodel import select, Session
from app.db import get_session
from app.models import Item
router = APIRouter()
@router.get('/', response_model=List[Item])
def listar_items(skip: int = 0, limit: int = Query(20, le=200), session: Session = Depends(get_session)):
    return session.exec(select(Item).offset(skip).limit(limit)).all()
@router.get('/{item_id}', response_model=Item)
def obtener_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item: raise HTTPException(status_code=404, detail="No encontrado")
    return item
@router.post('/', response_model=Item)
def crear_item(item: Item, session: Session = Depends(get_session)):
    session.add(item); session.commit(); session.refresh(item); return item
@router.put('/{item_id}', response_model=Item)
def reemplazar_item(item_id: int, nuevo: Item, session: Session = Depends(get_session)):
    item = session.get(Item, item_id); 
    if not item: raise HTTPException(status_code=404, detail="No encontrado")
    for k, v in nuevo.dict().items(): setattr(item, k, v)
    session.add(item); session.commit(); session.refresh(item); return item
@router.patch('/{item_id}', response_model=Item)
def actualizar_item(item_id: int, data: Item, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item: raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in data.dict(exclude_unset=True).items(): setattr(item, key, value)
    session.add(item); session.commit(); session.refresh(item); return item
@router.delete('/{item_id}')
def eliminar_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item: raise HTTPException(status_code=404, detail="No encontrado")
    item.activo = False; session.add(item); session.commit(); return {'ok': True}
@router.post('/{item_id}/restore')
def restore_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id); 
    if not item: raise HTTPException(status_code=404, detail="No encontrado")
    item.activo = True; session.add(item); session.commit(); return {'ok': True}
