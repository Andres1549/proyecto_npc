
# Wiki Silksong NPC

**Autor:** Andres Basto  
**Proyecto:** Wiki Silksong NPC  
**Descripción:** Backend desarrollado con FastAPI + SQLModel que gestiona NPCs, Items, Misiones y Ubicaciones del mundo de Silksong. Incluye vistas HTML, búsquedas, subida de imágenes a Supabase y despiegue en render en el link:https://wiki-silksong.onrender.com/.

---

## Mapa completo de endpoints

| Método | Ruta                         | Descripción                                   |
|--------|------------------------------|-----------------------------------------------|
| GET    | /                            | Página principal                              |
| GET    | /npcs                        | Listar NPCs                                   |
| GET    | /npcs/nuevo                  | Formulario crear NPC                          |
| POST   | /npcs/nuevo                  | Crear NPC                                     |
| GET    | /npcs/{id}                   | Ver detalle de NPC                            |
| GET    | /npcs/{id}/editar            | Form editar NPC                               |
| POST   | /npcs/{id}/editar            | Actualizar NPC                                 |
| POST   | /npcs/{id}/eliminar          | Eliminar NPC (marcar como inactivo)           |
| GET    | /items                       | Listar Items                                  |
| GET    | /items/crear                 | Formulario crear Item                         |
| POST   | /items/crear                 | Crear Item                                    |
| GET    | /items/{id}                  | Ver detalle de Item                           |
| GET    | /items/{id}/editar           | Form editar Item                              |
| POST   | /items/{id}/editar           | Actualizar Item                               |
| POST   | /items/{id}/eliminar         | Eliminar Item (marcar como inactivo)          |
| GET    | /misiones                    | Listar Misiones                               |
| GET    | /misiones/crear              | Formulario crear Misión                       |
| POST   | /misiones/crear              | Crear Misión                                  |
| GET    | /misiones/{id}               | Ver detalle de Misión                         |
| GET    | /misiones/{id}/editar        | Form editar Misión                            |
| POST   | /misiones/{id}/editar        | Actualizar Misión                             |
| POST   | /misiones/{id}/eliminar      | Eliminar Misión (marcar como inactivo)        |
| GET    | /ubicaciones                 | Listar Ubicaciones                            |
| GET    | /ubicaciones/crear           | Formulario crear Ubicación                    |
| POST   | /ubicaciones/crear           | Crear Ubicación                               |
| GET    | /ubicaciones/{id}            | Ver detalle de Ubicación                      |
| GET    | /ubicaciones/{id}/editar     | Form editar Ubicación                         |
| POST   | /ubicaciones/{id}/editar     | Actualizar Ubicación                          |
| POST   | /ubicaciones/{id}/eliminar   | Eliminar Ubicación (marcar como inactivo)     |
| GET    | /busqueda                    | Búsqueda general                              |
| GET    | /reportes                    | Reportes                                       |
| GET    | /historial                   | Elementos inactivos                           |
---

##  Diagrama de Clases

```
NPC 1---N Mision
NPC N---M Item
NPC N---1 Ubicacion
```

---

## Estructura del Proyecto

```
app/
├─ main.py
├─ db.py
├─ models.py
├─ routers/
├─ servicios/
├─ templates/
└─ static/
```

---
## Tecnologías utilizadas

| Tecnología   | Descripción |
|--------------|-------------|
| FastAPI      | Framework backend |
| SQLModel     | ORM / modelos (Pydantic + SQLAlchemy) |
| PostgreSQL*  | Base de datos (conectada por `DATABASE_URL` en `.env`) |
| Supabase     | Almacenamiento de imágenes (keys en `.env`) |
| Jinja2       | Plantillas HTML (templates) |
| Python 3.11+ | Lenguaje |

