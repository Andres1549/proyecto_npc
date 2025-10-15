from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select
from app.db import get_session
from app.models import Vendedor, Item
import csv, io

router = APIRouter()

@router.get("/vendedores_items.csv")
def reporte_vendedores_items(session: Session = Depends(get_session)):
    vendedores = session.exec(select(Vendedor)).all()
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["vendedor", "item", "precio", "tipo", "costo_metal_artesano"])
    for v in vendedores:
        for item in v.items:
            writer.writerow([v.nombre, item.nombre, item.precio, item.tipo, getattr(item, "costo_metal_artesano", "")])
    return Response(content=buffer.getvalue(), media_type="text/csv")
