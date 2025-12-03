from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form,Request
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import NPC, TipoNPC, Ubicacion
from app.servicios.supabase_conexion import upload_file
from fastapi.responses import HTMLResponse
from app.utils.templates import templates
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


templates = Jinja2Templates(directory="app/templates")

router = APIRouter()



@router.get("/{id}/editar", response_class=HTMLResponse)
def editar_npc_form(id: int, request: Request, session: Session = Depends(get_session)):
    npc = session.get(NPC, id)
    if not npc or not npc.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    ubicaciones = session.exec(select(Ubicacion).where(Ubicacion.activo == True)).all()

    return templates.TemplateResponse(
        "formularios/npc_editar.html",
        {
            "request": request,
            "npc": npc,
            "ubicaciones": ubicaciones
        }
    )

@router.get("/{npc_id}")
def detalle_npc(npc_id: int, request: Request, session: Session = Depends(get_session)):

    npc = session.get(NPC, npc_id)
    if not npc:
        return {"error": "NPC no encontrado"}

    items = []
    misiones = []

    if npc.tipo == "vendedor":
        items = npc.items

    if npc.tipo == "misiones":
        misiones = npc.misiones

    return templates.TemplateResponse(
        "detalles/npc_detalle.html",
        {
            "request": request,
            "npc": npc,
            "items": items,
            "misiones": misiones,
        }
    )
@router.post("/", response_model=NPC, status_code=201)
async def crear_npc(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo: TipoNPC = Form(...),
    id_ubicacion: int = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    ubic = session.get(Ubicacion, id_ubicacion)
    if not ubic or not ubic.activo:
        raise HTTPException(status_code=400, detail="Ubicación inválida")

    imagen_url = None
    if imagen:
        imagen_url = await upload_file(imagen)

    npc = NPC(
        nombre=nombre,
        descripcion=descripcion,
        tipo=tipo,
        id_ubicacion=id_ubicacion,
        imagen_url=imagen_url
    )
    session.add(npc)
    session.commit()
    session.refresh(npc)
    return npc

@router.post("/{id}/editar")
async def actualizar_npc_form(
    id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo: str = Form(...),
    id_ubicacion: int = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    npc = session.get(NPC, id)
    if not npc or not npc.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado")

    npc.nombre = nombre
    npc.descripcion = descripcion
    npc.tipo = TipoNPC(tipo)

    npc.id_ubicacion = id_ubicacion
    if imagen and imagen.filename:
        npc.imagen_url = await upload_file(imagen)

    session.add(npc)
    session.commit()
    session.refresh(npc)

    return RedirectResponse(url=f"/npcs/{id}", status_code=303)

@router.get("/{id}/eliminar")
def confirmar_borrar_npc(
    id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    npc = session.get(NPC, id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")

    return templates.TemplateResponse(
        "formularios/eliminar_confirmacion.html",
        {
            "request": request,
            "titulo": "Eliminar NPC",
            "nombre": npc.nombre,
            "url": f"/npcs/{id}/eliminar",
            "volver": f"/npcs/{id}"
        }
    )

@router.post("/{id}/eliminar")
def borrar_npc(id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")

    npc.activo = False
    session.add(npc)
    session.commit()

    return RedirectResponse("/", status_code=303)



@router.get("/tipo/{tipo}", response_class=HTMLResponse)
def listar_npcs_tipo(tipo: str, request: Request, db: Session = Depends(get_session)):
    tipo = tipo.lower()

    validos = ["historia", "misiones", "vendedor"]
    if tipo not in validos:
        return HTMLResponse("Tipo no válido", status_code=404)

    npcs = db.query(NPC).filter(NPC.tipo == tipo).all()

    return templates.TemplateResponse("listas/npcs.html", {
        "request": request,
        "npcs": npcs,
        "titulo": tipo.upper()
    })
