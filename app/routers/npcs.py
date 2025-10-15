from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import NPC, Mision

router = APIRouter()

@router.get("/", response_model=List[NPC])
def listar_npcs(skip: int = 0, limit: int = Query(10, le=100), session: Session = Depends(get_session)):
    return session.exec(select(NPC).offset(skip).limit(limit)).all()

@router.get("/{npc_id}", response_model=NPC)
def obtener_npc(npc_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    return npc

@router.post("/", response_model=NPC)
def crear_npc(npc: NPC, session: Session = Depends(get_session)):
    session.add(npc)
    session.commit()
    session.refresh(npc)
    return npc

@router.patch("/{npc_id}", response_model=NPC)
def actualizar_npc(npc_id: int, data: NPC, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(npc, key, value)
    session.add(npc)
    session.commit()
    session.refresh(npc)
    return npc

@router.delete("/{npc_id}")
def eliminar_npc(npc_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    npc.activo = False
    session.add(npc)
    session.commit()
    return {"ok": True}

@router.post("/{npc_id}/misiones/{mision_id}")
def asignar_mision(npc_id: int, mision_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    mision = session.get(Mision, mision_id)
    if not npc or not mision:
        raise HTTPException(status_code=404, detail="NPC o Misión no encontrada")
    mision.npc_id = npc.id
    session.add(mision)
    session.commit()
    return {"ok": True, "mensaje": f"Misión '{mision.titulo}' asignada a {npc.nombre}"}

@router.delete("/{npc_id}/misiones/{mision_id}")
def remover_mision(npc_id: int, mision_id: int, session: Session = Depends(get_session)):
    mision = session.get(Mision, mision_id)
    if not mision or mision.npc_id != npc_id:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    mision.npc_id = None
    session.add(mision)
    session.commit()
    return {"ok": True, "mensaje": "Misión desvinculada del NPC"}
