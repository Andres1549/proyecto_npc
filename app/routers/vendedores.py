from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import Vendedor, Item, VendedorItemLink

router = APIRouter()

@router.get("/", response_model=List[Vendedor])
def listar_vendedores(session: Session = Depends(get_session)):
    return session.exec(select(Vendedor)).all()

@router.get("/{vendedor_id}", response_model=Vendedor)
def obtener_vendedor(vendedor_id: int, session: Session = Depends(get_session)):
    v = session.get(Vendedor, vendedor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    return v

@router.post("/", response_model=Vendedor)
def crear_vendedor(v: Vendedor, session: Session = Depends(get_session)):
    session.add(v)
    session.commit()
    session.refresh(v)
    return v

@router.patch("/{vendedor_id}", response_model=Vendedor)
def actualizar_vendedor(vendedor_id: int, data: Vendedor, session: Session = Depends(get_session)):
    v = session.get(Vendedor, vendedor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(v, key, value)
    session.add(v)
    session.commit()
    session.refresh(v)
    return v

@router.delete("/{vendedor_id}")
def eliminar_vendedor(vendedor_id: int, session: Session = Depends(get_session)):
    v = session.get(Vendedor, vendedor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    v.activo = False
    session.add(v)
    session.commit()
    return {"ok": True}

@router.post("/{vendedor_id}/items/{item_id}")
def vincular_item(vendedor_id: int, item_id: int, session: Session = Depends(get_session)):
    v = session.get(Vendedor, vendedor_id)
    item = session.get(Item, item_id)
    if not v or not item:
        raise HTTPException(status_code=404, detail="Vendedor o item no encontrado")
    session.add(VendedorItemLink(vendedor_id=v.id, item_id=item.id))
    session.commit()
    return {"ok": True}

@router.delete("/{vendedor_id}/items/{item_id}")
def desvincular_item(vendedor_id: int, item_id: int, session: Session = Depends(get_session)):
    link = session.exec(select(VendedorItemLink).where(VendedorItemLink.vendedor_id==vendedor_id, VendedorItemLink.item_id==item_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    session.delete(link)
    session.commit()
    return {"ok": True}
