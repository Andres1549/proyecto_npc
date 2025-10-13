from fastapi import FastAPI
from app.db import init_db
from app.routers import npcs, ubicaciones, items, misiones, vendedores

app = FastAPI(title="Proyecto NPC")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(npcs, prefix="/npcs", tags=["npcs"])
app.include_router(ubicaciones, prefix="/ubicaciones", tags=["ubicaciones"])
app.include_router(items, prefix="/items", tags=["items"])
app.include_router(misiones, prefix="/misiones", tags=["misiones"])
app.include_router(vendedores, prefix="/vendedores", tags=["vendedores"])
