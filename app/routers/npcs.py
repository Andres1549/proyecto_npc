from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import NPC, TipoNPC
from app.servicios.supabase_conexion import upload_file

router = APIRouter(tags=["NPCs"])

@router.get("/", response_model=List[NPC])
def listar_npcs(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    return session.exec(
        select(NPC).where(NPC.activo == True).offset(skip).limit(limit)
    ).all()


@router.post("/", response_model=NPC, status_code=201)
async def crear_npc(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo: TipoNPC = Form(...),
    id_ubicacion: int = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session),
):
    imagen_url = None
    if imagen:
        imagen_url = await upload_file(imagen)

    npc = NPC(
        nombre=nombre,
        descripcion=descripcion,
        tipo=tipo,
        id_ubicacion=id_ubicacion,
        imagen_url=imagen_url,
    )

    session.add(npc)
    session.commit()
    session.refresh(npc)
    return npc


@router.put("/{npc_id}", response_model=NPC)
async def reemplazar_npc(
    npc_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo: TipoNPC = Form(...),
    id_ubicacion: int = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session),
):
    npc_db = session.get(NPC, npc_id)
    if not npc_db:
        raise HTTPException(404, "NPC no encontrado")

    if imagen:
        npc_db.imagen_url = await upload_file(imagen)

    npc_db.nombre = nombre
    npc_db.descripcion = descripcion
    npc_db.tipo = tipo
    npc_db.id_ubicacion = id_ubicacion

    session.commit()
    session.refresh(npc_db)
    return npc_db


@router.patch("/{npc_id}", response_model=NPC)
async def actualizar_npc(
    npc_id: int,
    nombre: str = Form(None),
    descripcion: str = Form(None),
    tipo: TipoNPC = Form(None),
    id_ubicacion: int = Form(None),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session),
):
    npc_db = session.get(NPC, npc_id)
    if not npc_db:
        raise HTTPException(404, "NPC no encontrado")

    if imagen:
        npc_db.imagen_url = await upload_file(imagen)

    if nombre is not None:
        npc_db.nombre = nombre
    if descripcion is not None:
        npc_db.descripcion = descripcion
    if tipo is not None:
        npc_db.tipo = tipo
    if id_ubicacion is not None:
        npc_db.id_ubicacion = id_ubicacion

    session.commit()
    session.refresh(npc_db)
    return npc_db


@router.delete("/{npc_id}")
def eliminar_npc(npc_id: int, session: Session = Depends(get_session)):
    npc_db = session.get(NPC, npc_id)
    if not npc_db:
        raise HTTPException(404, "NPC no encontrado")
    npc_db.activo = False
    session.commit()
    return {"mensaje": "NPC marcado como inactivo"}
