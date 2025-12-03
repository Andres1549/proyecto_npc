from fastapi import APIRouter, Depends, Query
from sqlmodel import select, Session
from app.db import get_session
from app.models import NPC, Item, Mision, Ubicacion
import unicodedata
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Búsqueda Global"])

def normalizar(texto: str) -> str:
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.lower()


@router.get("/buscar")
def busqueda_html(
    request: Request,
    termino: str = Query(...),
    session: Session = Depends(get_session)
):
    termino_norm = normalizar(termino)

    npcs = [
        npc for npc in session.exec(select(NPC).where(NPC.activo == True)).all()
        if termino_norm in normalizar(npc.nombre) or termino_norm in normalizar(npc.descripcion)
    ]
    items = [
        item for item in session.exec(select(Item).where(Item.activo == True)).all()
        if termino_norm in normalizar(item.nombre) or termino_norm in normalizar(item.descripcion)
    ]
    misiones = [
        m for m in session.exec(select(Mision).where(Mision.activo == True)).all()
        if termino_norm in normalizar(m.titulo) or termino_norm in normalizar(m.descripcion)
    ]
    ubicaciones = [
        u for u in session.exec(select(Ubicacion).where(Ubicacion.activo == True)).all()
        if termino_norm in normalizar(u.nombre) or termino_norm in normalizar(u.descripcion)
    ]

    return templates.TemplateResponse(
        "listas/busqueda.html",
        {
            "request": request,
            "termino": termino,
            "npcs": npcs,
            "items": items,
            "misiones": misiones,
            "ubicaciones": ubicaciones
        }
    )
