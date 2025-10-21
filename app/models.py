from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TipoNPC(str, Enum):
    historia = "historia"
    vendedor = "vendedor"
    misiones = "misiones"


class TipoItem(str, Enum):
    herramienta = "herramienta"
    material = "material"
    mejora = "mejora"


class TipoMision(str, Enum):
    principal = "principal"
    secundaria = "secundaria"


class NPCItemLink(SQLModel, table=True):
    npc_id: Optional[int] = Field(default=None, foreign_key="npc.id", primary_key=True)
    item_id: Optional[int] = Field(default=None, foreign_key="item.id", primary_key=True)


class Ubicacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    activo: bool = Field(default=True)

    npcs: List["NPC"] = Relationship(back_populates="ubicacion")


class NPC(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    tipo: TipoNPC
    id_ubicacion: int = Field(foreign_key="ubicacion.id")
    activo: bool = Field(default=True)

    ubicacion: Optional[Ubicacion] = Relationship(back_populates="npcs")
    misiones: List["Mision"] = Relationship(back_populates="npc")
    items: List["Item"] = Relationship(back_populates="npcs", link_model=NPCItemLink)


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio: int
    usa_metal_artesano: bool
    tipo: TipoItem
    activo: bool = Field(default=True)

    npcs: List[NPC] = Relationship(back_populates="items", link_model=NPCItemLink)


class Mision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    recompensa: str
    tipo: TipoMision
    id_npc: int = Field(foreign_key="npc.id")
    activo: bool = Field(default=True)

    npc: Optional[NPC] = Relationship(back_populates="misiones")
