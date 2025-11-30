from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import Item, TipoItem
from app.servicios.supabase_conexion import upload_file

router = APIRouter()

@router.get("/", response_model=List[Item])
def listar_items(session: Session = Depends(get_session), skip: int = Query(0), limit: int = Query(10)):
    return session.exec(select(Item).where(Item.activo == True).offset(skip).limit(limit)).all()

@router.get("/{id}", response_model=Item)
def obtener_item(id: int, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item or not item.activo:
        raise HTTPException(status_code=404, detail="Item no encontrado o inactivo")
    return item

@router.post("/", response_model=Item, status_code=201)
async def crear_item(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: int = Form(...),
    usa_metal_artesano: bool = Form(False),
    tipo: TipoItem = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    imagen_url = None
    if imagen:
        imagen_url = await upload_file(imagen)

    item = Item(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        usa_metal_artesano=usa_metal_artesano,
        tipo=tipo,
        imagen_url=imagen_url
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.put("/{id}", response_model=Item)
async def reemplazar_item(
    id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: int = Form(...),
    usa_metal_artesano: bool = Form(False),
    tipo: TipoItem = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    item_db = session.get(Item, id)
    if not item_db or not item_db.activo:
        raise HTTPException(status_code=404, detail="Item no encontrado o inactivo")

    if imagen:
        item_db.imagen_url = await upload_file(imagen)

    item_db.nombre = nombre
    item_db.descripcion = descripcion
    item_db.precio = precio
    item_db.usa_metal_artesano = usa_metal_artesano
    item_db.tipo = tipo

    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db

@router.patch("/{id}", response_model=Item)
async def actualizar_item(
    id: int,
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    precio: Optional[int] = Form(None),
    usa_metal_artesano: Optional[bool] = Form(None),
    tipo: Optional[TipoItem] = Form(None),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    item_db = session.get(Item, id)
    if not item_db or not item_db.activo:
        raise HTTPException(status_code=404, detail="Item no encontrado o inactivo")

    if imagen:
        item_db.imagen_url = await upload_file(imagen)
    if nombre is not None:
        item_db.nombre = nombre
    if descripcion is not None:
        item_db.descripcion = descripcion
    if precio is not None:
        item_db.precio = precio
    if usa_metal_artesano is not None:
        item_db.usa_metal_artesano = usa_metal_artesano
    if tipo is not None:
        item_db.tipo = tipo

    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db

@router.delete("/{id}")
def eliminar_item(id: int, session: Session = Depends(get_session)):
    item_db = session.get(Item, id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    item_db.activo = False
    session.add(item_db)
    session.commit()
    return {"mensaje": "Item marcado como inactivo"}
