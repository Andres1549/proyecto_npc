from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select
from app.db import get_session
from app.models import NPC, Mision, NPC_MisionLink

router = APIRouter()

@router.get("/", response_model=List[NPC])
def list_npcs(skip: int = 0, limit: int = Query(10, le=100), tipo: Optional[str] = None, ubicacion_id: Optional[int] = None, session: Session = Depends(get_session)):
    q = select(NPC)
    if tipo:
        q = q.where(NPC.tipo == tipo)
    if ubicacion_id:
        q = q.where(NPC.id_ubicacion == ubicacion_id)
    q = q.offset(skip).limit(limit)
    return session.exec(q).all()

@router.post("/", response_model=NPC)
def create_npc(npc: NPC, session: Session = Depends(get_session)):
    session.add(npc)
    session.commit()
    session.refresh(npc)
    return npc

@router.get("/{npc_id}", response_model=NPC)
def get_npc(npc_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    return npc

@router.patch("/{npc_id}", response_model=NPC)
def update_npc(npc_id: int, npc_update: NPC, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    npc_data = npc_update.dict(exclude_unset=True)
    for key, value in npc_data.items():
        setattr(npc, key, value)
    session.add(npc)
    session.commit()
    session.refresh(npc)
    return npc

@router.delete("/{npc_id}")
def delete_npc(npc_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC no encontrado")
    npc.activo = False
    session.add(npc)
    session.commit()
    return {"ok": True}

@router.post("/{npc_id}/misiones/{mision_id}")
def vincular_mision(npc_id: int, mision_id: int, session: Session = Depends(get_session)):
    npc = session.get(NPC, npc_id)
    mision = session.get(Mision, mision_id)
    if not npc or not mision:
        raise HTTPException(status_code=404, detail="NPC o Misión no encontrada")
    link = NPC_MisionLink(npc_id=npc_id, mision_id=mision_id)
    session.add(link)
    session.commit()
    return {"ok": True}

@router.delete("/{npc_id}/misiones/{mision_id}")
def desvincular_mision(npc_id: int, mision_id: int, session: Session = Depends(get_session)):
    q = select(NPC_MisionLink).where(NPC_MisionLink.npc_id == npc_id, NPC_MisionLink.mision_id == mision_id)
    link = session.exec(q).first()
    if not link:
        raise HTTPException(status_code=404, detail="Vinculo no encontrado")
    session.delete(link)
    session.commit()
    return {"ok": True}