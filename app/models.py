from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
class Ubicacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    npcs: List["NPC"] = Relationship(back_populates="ubicacion")
class NPC(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    tipo: str
    id_ubicacion: Optional[int] = Field(default=None, foreign_key="ubicacion.id")
    activo: bool = Field(default=True)
    ubicacion: Optional[Ubicacion] = Relationship(back_populates="npcs")
    misiones: List["Mision"] = Relationship(back_populates="npc")
class Mision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    tipo: str
    activo: bool = Field(default=True)
    npc_id: Optional[int] = Field(default=None, foreign_key="npc.id")
    npc: Optional[NPC] = Relationship(back_populates="misiones")
class VendedorItemLink(SQLModel, table=True):
    vendedor_id: Optional[int] = Field(default=None, foreign_key="vendedor.id", primary_key=True)
    item_id: Optional[int] = Field(default=None, foreign_key="item.id", primary_key=True)
class Vendedor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = Field(default=True)
    items: List["Item"] = Relationship(back_populates="vendedores", link_model=VendedorItemLink)
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(default=0, ge=0)
    costo_metal_artesano: Optional[int] = Field(default=None, ge=0)
    tipo: str
    activo: bool = Field(default=True)
    vendedores: List[Vendedor] = Relationship(back_populates="items", link_model=VendedorItemLink)
