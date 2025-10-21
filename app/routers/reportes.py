from fastapi import APIRouter, Depends, Response
from sqlmodel import select, Session
from app.db import get_session
from app.models import NPC, Item
import csv, io

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/vendedores_items.csv")
def reporte_vendedores_items(session: Session = Depends(get_session)):
    vendedores = session.exec(
        select(NPC).where(NPC.tipo == "vendedor", NPC.activo == True)
    ).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["vendedor", "item", "precio", "tipo", "usa_metal_artesano"])

    for v in vendedores:
        for item in v.items:
            writer.writerow([
                v.nombre,
                item.nombre,
                item.precio,
                item.tipo.value,
                "Sí" if item.usa_metal_artesano else "No"
            ])

    return Response(content=buffer.getvalue(), media_type="text/csv")
