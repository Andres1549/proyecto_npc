from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import NPC, TipoNPC

router = APIRouter(tags=["NPCs"])


@router.get("/", response_model=List[NPC])
def listar_npcs(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    npcs = session.exec(select(NPC).where(NPC.activo == True).offset(skip).limit(limit)).all()
    return npcs


@router.get("/{npc_id}", response_model=NPC)
def obtener_npc(npc_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc or not npc.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o inactivo")
    return npc


@router.post("/", response_model=NPC, status_code=201)
def crear_npc(npc: NPC, session: Session = Depends(get_session)):
    session.add(npc)
    session.commit()
    session.refresh(npc)
    return npc


@router.put("/{npc_id}", response_model=NPC)
def remplazar_npc(npc_id: int, datos_actualizados: NPC, session: Session = Depends(get_session)):
    npc_db = session.get(NPC, npc_id)
    if not npc_db or not npc_db.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o inactivo")
    for key, value in datos_actualizados.dict(exclude_unset=True).items():
        setattr(npc_db, key, value)
    session.add(npc_db)
    session.commit()
    session.refresh(npc_db)
    return npc_db


@router.patch("/{npc_id}", response_model=NPC)
def actualizar_npc(npc_id: int, datos_parciales: dict, session: Session = Depends(get_session)):
    npc_db = session.get(NPC, npc_id)
    if not npc_db or not npc_db.activo:
        raise HTTPException(status_code=404, detail="NPC no encontrado o inactivo")
    for key, value in datos_parciales.items():
        setattr(npc_db, key, value)
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
