from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form,Request
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import NPC, TipoNPC, Ubicacion
from app.servicios.supabase_conexion import upload_file
from fastapi.responses import HTMLResponse
from app.utils.templates import templates
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/", response_model=List[NPC])
def listar_npcs(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    return session.exec(select(NPC).where(NPC.activo == True).offset(skip).limit(limit)).all()


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

@router.put("/{npc_id}", response_model=NPC)
async def remplazar_npc(
    npc_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo: TipoNPC = Form(...),
    id_ubicacion: int = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    npc_db = session.get(NPC, npc_id)
    if not npc_db or not npc_db.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o inactivo")

    ubic = session.get(Ubicacion, id_ubicacion)
    if not ubic or not ubic.activo:
        raise HTTPException(status_code=400, detail="Ubicación inválida")

    if imagen:
        npc_db.imagen_url = await upload_file(imagen)

    npc_db.nombre = nombre
    npc_db.descripcion = descripcion
    npc_db.tipo = tipo
    npc_db.id_ubicacion = id_ubicacion

    session.add(npc_db)
    session.commit()
    session.refresh(npc_db)
    return npc_db

@router.patch("/{npc_id}", response_model=NPC)
async def actualizar_npc(
    npc_id: int,
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    tipo: Optional[TipoNPC] = Form(None),
    id_ubicacion: Optional[int] = Form(None),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    npc_db = session.get(NPC, npc_id)
    if not npc_db or not npc_db.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o inactivo")

    if id_ubicacion is not None:
        ubic = session.get(Ubicacion, id_ubicacion)
        if not ubic or not ubic.activo:
            raise HTTPException(status_code=400, detail="Ubicación inválida")
        npc_db.id_ubicacion = id_ubicacion

    if imagen:
        npc_db.imagen_url = await upload_file(imagen)
    if nombre is not None:
        npc_db.nombre = nombre
    if descripcion is not None:
        npc_db.descripcion = descripcion
    if tipo is not None:
        npc_db.tipo = tipo

    session.add(npc_db)
    session.commit()
    session.refresh(npc_db)
    return npc_db

@router.delete("/{npc_id}")
def eliminar_npc(npc_id: int, session: Session = Depends(get_session)):
    npc_db = session.get(NPC, npc_id)
    if not npc_db:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    npc_db.activo = False
    session.add(npc_db)
    session.commit()
    return {"mensaje": f"NPC '{npc_db.nombre}' marcado como inactivo"}

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
