from sqlmodel import Session, select, SQLModel
from app.db import engine
from app.models import Ubicacion, NPC, Mision, Vendedor, Item, VendedorItemLink
sample_ubicaciones = [
    {"nombre": "Tierras Musgosas", "descripcion": "Región inicial y llena de vida musgosa."},
    {"nombre": "Muelles Profundos", "descripcion": "Zona industrial bajo las colinas."},
    {"nombre": "Valle Óseo", "descripcion": "Caverna profunda con ecos y comerciantes."},
]
sample_npcs = [
    {"nombre": "Shakra la Navegante", "descripcion": "Cartógrafa que vende mapas y accesorios.", "tipo": "vendedor"},
    {"nombre": "Pebb el Mercader", "descripcion": "Mercader con mercancías variadas.", "tipo": "vendedor"},
    {"nombre": "Hija del Herrero", "descripcion": "Artesana que vende mejoras y materiales.", "tipo": "vendedor"},
]
sample_misiones = [
    {"titulo": "Recolección de bayas", "descripcion": "Recolecta bayas musgosas para el druida.", "tipo": "secundaria"},
    {"titulo": "Púas maleables", "descripcion": "Recolecta núcleos de púa para la costurera.", "tipo": "secundaria"},
    {"titulo": "Las pulgas perdidas", "descripcion": "Recupera las pulgas perdidas para Mooshka.", "tipo": "secundaria"},
]
sample_items = [
    {"nombre": "Mapa de las Tierras Musgosas", "descripcion": "Mapa de la región de las Tierras Musgosas.", "precio": 40.0, "tipo":"mapa"},
    {"nombre": "Mapa de los Muelles Profundos", "descripcion": "Mapa de la región de los Muelles Profundos.", "precio": 50.0, "tipo":"mapa"},
    {"nombre": "Brújula", "descripcion": "Muestra la posición en el mapa.", "precio":70.0, "tipo":"herramienta"},
    {"nombre": "Metal artesano", "descripcion": "Material para forja.", "precio":60.0, "tipo":"material"},
    {"nombre": "Bolsa de fragmentos", "descripcion": "Da fragmentos para fabricar herramientas.", "precio":50.0, "tipo":"material"},
    {"nombre": "Kit de forja", "descripcion": "Permite crear herramientas más fuertes desde un banco.", "precio":180.0, "tipo":"mejora"},
    {"nombre": "Campana magmática", "descripcion": "Herramienta para templar armas.", "precio":110.0, "tipo":"herramienta"},
    {"nombre": "Aguijón cortante", "descripcion": "Herramienta encontrada/compra en el mundo del juego.", "precio":140.0, "tipo":"herramienta"},
]
vendedor_items = {
    "Shakra la Navegante": ["Mapa de las Tierras Musgosas", "Mapa de los Muelles Profundos", "Brújula"],
    "Pebb el Mercader": ["Metal artesano", "Bolsa de fragmentos"],
    "Hija del Herrero": ["Kit de forja", "Campana magmática", "Aguijón cortante"],
}
def seed_all():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for u in sample_ubicaciones:
            session.add(Ubicacion(**u))
        session.commit()
        ubicaciones = session.exec(select(Ubicacion)).all()
        for i, n in enumerate(sample_npcs):
            npc = NPC(**n)
            if i < len(ubicaciones):
                npc.id_ubicacion = ubicaciones[i].id
            session.add(npc)
        session.commit()
        for m in sample_misiones:
            session.add(Mision(**m))
        session.commit()
        for v in sample_npcs:
            session.add(Vendedor(nombre=v["nombre"], descripcion=v["descripcion"]))
        session.commit()
        for it in sample_items:
            session.add(Item(**it))
        session.commit()
        for vendedor_nombre, item_nombres in vendedor_items.items():
            vendedor = session.exec(select(Vendedor).where(Vendedor.nombre==vendedor_nombre)).first()
            for item_nombre in item_nombres:
                item = session.exec(select(Item).where(Item.nombre==item_nombre)).first()
                if vendedor and item:
                    session.add(VendedorItemLink(vendedor_id=vendedor.id, item_id=item.id))
        session.commit()
if __name__ == "__main__":
    seed_all()
    print("Seed completado con datos reales.")
