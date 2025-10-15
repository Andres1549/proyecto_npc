from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_, func
from app.db import get_session
from app.models import NPC, Item, Mision, Vendedor

router = APIRouter()

@router.get("/buscar")
def busqueda_global(
    termino: str = Query(..., description="Término a buscar"),
    session: Session = Depends(get_session)
):
    termino_like = f"%{termino.lower()}%"

    npcs = session.exec(
        select(NPC).where(
            or_(
                func.lower(NPC.nombre).like(termino_like),
                func.lower(NPC.descripcion).like(termino_like)
            )
        )
    ).all()

    items = session.exec(
        select(Item).where(
            or_(
                func.lower(Item.nombre).like(termino_like),
                func.lower(Item.descripcion).like(termino_like)
            )
        )
    ).all()

    misiones = session.exec(
        select(Mision).where(
            or_(
                func.lower(Mision.titulo).like(termino_like),
                func.lower(Mision.descripcion).like(termino_like)
            )
        )
    ).all()

    vendedores = session.exec(
        select(Vendedor).where(
            or_(
                func.lower(Vendedor.nombre).like(termino_like),
                func.lower(Vendedor.descripcion).like(termino_like)
            )
        )
    ).all()

    return {
        "termino": termino,
        "resultados": {
            "npcs": npcs,
            "items": items,
            "misiones": misiones,
            "vendedores": vendedores,
        },
    }
