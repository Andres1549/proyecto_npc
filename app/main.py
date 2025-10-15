from fastapi import FastAPI
from app.db import init_db
from app.routers import npcs, items, vendedores, misiones, ubicaciones, reportes, busqueda

app = FastAPI(title="Proyecto NPC")

@app.on_event("startup")
def on_startup():
    init_db()
app.include_router(npcs, prefix="/npcs", tags=["NPCs"])
app.include_router(items, prefix="/items", tags=["Items"])
app.include_router(vendedores, prefix="/vendedores", tags=["Vendedores"])
app.include_router(misiones, prefix="/misiones", tags=["Misiones"])
app.include_router(ubicaciones, prefix="/ubicaciones", tags=["Ubicaciones"])
app.include_router(reportes, prefix="/reportes", tags=["Reportes"])
app.include_router(busqueda, prefix="/global", tags=["Búsqueda Global"])
