from fastapi import APIRouter, Depends, Query
from sqlmodel import select, Session
from app.db import get_session
from app.models import NPC, Item, Mision, Vendedor
import unicodedata
router = APIRouter()
def normalizar(texto: str) -> str:
    if not texto: return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.lower()
@router.get('/buscar')
def busqueda_global(termino: str = Query(..., description="Término a buscar"), session: Session = Depends(get_session)):
    termino_norm = normalizar(termino)
    npcs = [npc for npc in session.exec(select(NPC)).all() if termino_norm in normalizar(npc.nombre) or termino_norm in normalizar(npc.descripcion)]
    items = [item for item in session.exec(select(Item)).all() if termino_norm in normalizar(item.nombre) or termino_norm in normalizar(item.descripcion)]
    misiones = [m for m in session.exec(select(Mision)).all() if termino_norm in normalizar(m.titulo) or termino_norm in normalizar(m.descripcion)]
    vendedores = [v for v in session.exec(select(Vendedor)).all() if termino_norm in normalizar(v.nombre) or termino_norm in normalizar(v.descripcion)]
    return {'termino': termino, 'resultados': {'npcs': npcs, 'items': items, 'misiones': misiones, 'vendedores': vendedores}}
