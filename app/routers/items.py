from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, Request
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import Item, TipoItem, NPC
from app.servicios.supabase_conexion import upload_file
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/crear")
def form_crear_item(request: Request, npc_id: int = Query(...)):
    # La URL llama a /items/crear?npc_id=X, y aquí lo pasamos al HTML
    return templates.TemplateResponse(
        "formularios/item_form.html",
        {"request": request, "npc_id": npc_id}
    )


@router.post("/crear")
async def crear_item(
        request: Request,
        npc_id: int = Form(...),
        nombre: str = Form(...),
        descripcion: str = Form(...),
        precio: int = Form(...),
        tipo: str = Form(...),
        usa_metal_artesano: bool = Form(False),
        imagen: UploadFile = File(None),
        session: Session = Depends(get_session)
):
    img_url = None
    if imagen and imagen.filename:
        img_url = await upload_file(imagen)

    item = Item(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        tipo=tipo,
        imagen_url=img_url,
        usa_metal_artesano=usa_metal_artesano  # Asignación
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC asociado no encontrado")

    if npc.items is None:
        npc.items = []

    npc.items.append(item)
    session.add(npc)
    session.commit()

    return RedirectResponse(url=f"/npcs/{npc_id}", status_code=303)

@router.get("/", response_model=List[Item])
def listar_items(session: Session = Depends(get_session), skip: int = Query(0), limit: int = Query(10)):
    return session.exec(
        select(Item).where(Item.activo == True).offset(skip).limit(limit)
    ).all()



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

    if imagen and imagen.filename:
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
