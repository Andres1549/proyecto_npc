from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, Session
from typing import List, Optional

from app.db import get_session
from app.models import Item, TipoItem, NPC
from app.servicios.supabase_conexion import upload_file

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@router.get("/crear")
def form_crear_item(request: Request, npc_id: Optional[int] = None):
    return templates.TemplateResponse("formularios/item_form.html", {"request": request, "npc_id": npc_id})

@router.post("/crear")
async def crear_item(
    request: Request,
    npc_id: Optional[int] = Form(None),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: int = Form(...),
    tipo: TipoItem = Form(...),
    usa_metal_artesano: bool = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    imagen_url = None
    if imagen and imagen.filename:
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

    if npc_id:
        npc = session.get(NPC, npc_id)
        if npc:
            npc.items.append(item)
            session.add(npc)
            session.commit()

    return RedirectResponse(url=f"/npcs/{npc_id}" if npc_id else "/items", status_code=303)




@router.get("/{id}/editar")
def form_editar_item(id: int, request: Request, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return templates.TemplateResponse("formularios/item_editar.html", {"request": request, "item": item})


@router.post("/{id}/editar")
async def actualizar_item_form(
    id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: int = Form(...),
    usa_metal_artesano: bool = Form(False),
    tipo: TipoItem = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    item = session.get(Item, id)
    if not item or not item.activo:
        raise HTTPException(status_code=404, detail="Item no encontrado o inactivo")

    if imagen and imagen.filename:
        item.imagen_url = await upload_file(imagen)

    item.nombre = nombre
    item.descripcion = descripcion
    item.precio = precio
    item.usa_metal_artesano = usa_metal_artesano
    item.tipo = tipo

    session.add(item)
    session.commit()
    session.refresh(item)
    return RedirectResponse(url=f"/items/{id}", status_code=303)


@router.get("/{id}/eliminar")
def form_eliminar_item(id: int, request: Request, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return templates.TemplateResponse(
        "formularios/eliminar_confirmacion.html",
        {"request": request, "item": item}
    )
@router.post("/{id}/eliminar")
def eliminar_item_confirmado(id: int, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    item.activo = False
    session.add(item)
    session.commit()

    return RedirectResponse(url="/", status_code=303)
@router.get("/{id}", response_model=Item)
def detalle_item(id: int, request: Request, session: Session = Depends(get_session)):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return templates.TemplateResponse("detalles/item_detalle.html", {"request": request, "item": item})
