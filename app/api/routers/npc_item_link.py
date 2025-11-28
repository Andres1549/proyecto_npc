from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.models import NPCItemLink, NPC, Item

router = APIRouter(prefix="/npc-items", tags=["Relación NPC-Item"])


@router.get("/", response_model=List[NPCItemLink])
def listar_relaciones(session: Session = Depends(get_session)):
    return session.exec(select(NPCItemLink)).all()


@router.post("/", response_model=NPCItemLink, status_code=201)
def crear_relacion(link: NPCItemLink, session: Session = Depends(get_session)):
    npc = session.get(NPC, link.npc_id)
    item = session.get(Item, link.item_id)
    if not npc or not item:
        raise HTTPException(status_code=404, detail="NPC o Item no encontrado")
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


@router.delete("/{npc_id}/{item_id}")
def eliminar_relacion(npc_id: int, item_id: int, session: Session = Depends(get_session)):
    link = session.exec(
        select(NPCItemLink).where(
            (NPCItemLink.npc_id == npc_id) & (NPCItemLink.item_id == item_id)
        )
    ).first()
    if not link:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    session.delete(link)
    session.commit()
    return {"mensaje": f"Relación NPC {npc_id} - Item {item_id} eliminada"}
