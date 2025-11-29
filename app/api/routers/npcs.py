from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlmodel import Session, select
from typing import List, Optional
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


@router.get("/{npc_id}", response_model=NPC)
def obtener_npc(npc_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc or not npc.activo:
        raise HTTPException(404, "NPC no encontrado o inactivo")
    return npc


@router.post("/", response_model=NPC, status_code=201)
def crear_npc(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo: TipoNPC = Form(...),
    id_ubicacion: int = Form(...),
    file: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    imagen_url = None
    if file:
        filename = f"npcs/{nombre.replace(' ', '_')}_{file.filename}"
        imagen_url = upload_file(file.file, filename)

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
def remplazar_npc(
    npc_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo: TipoNPC = Form(...),
    id_ubicacion: int = Form(...),
    file: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    npc = session.get(NPC, npc_id)
    if not npc or not npc.activo:
        raise HTTPException(404, "NPC no encontrado o inactivo")

    npc.nombre = nombre
    npc.descripcion = descripcion
    npc.tipo = tipo
    npc.id_ubicacion = id_ubicacion

    if file:
        filename = f"npcs/{npc_id}_{file.filename}"
        npc.imagen_url = upload_file(file.file, filename)

    session.commit()
    session.refresh(npc)
    return npc


@router.patch("/{npc_id}", response_model=NPC)
def actualizar_npc(
    npc_id: int,
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    tipo: Optional[TipoNPC] = Form(None),
    id_ubicacion: Optional[int] = Form(None),
    file: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    npc = session.get(NPC, npc_id)
    if not npc or not npc.activo:
        raise HTTPException(404, "NPC no encontrado o inactivo")

    if nombre is not None:
        npc.nombre = nombre
    if descripcion is not None:
        npc.descripcion = descripcion
    if tipo is not None:
        npc.tipo = tipo
    if id_ubicacion is not None:
        npc.id_ubicacion = id_ubicacion

    if file:
        filename = f"npcs/{npc_id}_{file.filename}"
        npc.imagen_url = upload_file(file.file, filename)

    session.commit()
    session.refresh(npc)
    return npc


@router.delete("/{npc_id}")
def eliminar_npc(npc_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(404, "NPC no encontrado")

    npc.activo = False
    session.commit()

    return {"mensaje": f"NPC '{npc.nombre}' marcado como inactivo"}
