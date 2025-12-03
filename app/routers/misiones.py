from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query,Request
from sqlmodel import Session, select
from typing import List, Optional
from app.db import get_session
from app.models import Mision, TipoMision, NPC
from app.servicios.supabase_conexion import upload_file
from app.utils.templates import templates

router = APIRouter()
@router.get("/crear")
def form_crear_mision(request: Request, npc_id: int):
    return templates.TemplateResponse("formularios/mision_form.html", {
        "request": request,
        "npc_id": npc_id
    })

@router.post("/crear")
def crear_mision(
    request: Request,
    npc_id: int = Form(...),
    titulo: str = Form(...),
    descripcion: str = Form(...),
    recompensa: str = Form(...),
    tipo: str = Form(...),
    session: Session = Depends(get_session)
):
    m = Mision(
        titulo=titulo,
        descripcion=descripcion,
        recompensa=recompensa,
        tipo=tipo,
        id_npc=npc_id
    )

    session.add(m)
    session.commit()

    return {"mensaje": "Misión creada"}

@router.get("/", response_model=List[Mision])
def listar_misiones(session: Session = Depends(get_session), skip: int = Query(0), limit: int = Query(50)):
    return session.exec(select(Mision).where(Mision.activo == True).offset(skip).limit(limit)).all()

@router.get("/{id}", response_model=Mision)
def obtener_mision(id: int, session: Session = Depends(get_session)):
    m = session.get(Mision, id)
    if not m or not m.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o inactiva")
    return m


@router.put("/{id}", response_model=Mision)
async def reemplazar_mision(
    id: int,
    titulo: str = Form(...),
    descripcion: str = Form(...),
    recompensa: str = Form(...),
    tipo: TipoMision = Form(...),
    id_npc: int = Form(...),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    m = session.get(Mision, id)
    if not m or not m.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o inactiva")

    npc = session.get(NPC, id_npc)
    if not npc or not npc.activo:
        raise HTTPException(status_code=400, detail="NPC que entrega la misión no existe o está inactivo")

    if imagen:
        m.imagen_url = await upload_file(imagen)

    m.titulo = titulo
    m.descripcion = descripcion
    m.recompensa = recompensa
    m.tipo = tipo
    m.id_npc = id_npc

    session.add(m)
    session.commit()
    session.refresh(m)
    return m

@router.patch("/{id}", response_model=Mision)
async def actualizar_mision(
    id: int,
    titulo: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    recompensa: Optional[str] = Form(None),
    tipo: Optional[TipoMision] = Form(None),
    id_npc: Optional[int] = Form(None),
    imagen: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    m = session.get(Mision, id)
    if not m or not m.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o inactiva")

    if id_npc is not None:
        npc = session.get(NPC, id_npc)
        if not npc or not npc.activo:
            raise HTTPException(status_code=400, detail="NPC que entrega la misión no existe o está inactivo")
        m.id_npc = id_npc

    if imagen:
        m.imagen_url = await upload_file(imagen)
    if titulo is not None:
        m.titulo = titulo
    if descripcion is not None:
        m.descripcion = descripcion
    if recompensa is not None:
        m.recompensa = recompensa
    if tipo is not None:
        m.tipo = tipo

    session.add(m)
    session.commit()
    session.refresh(m)
    return m

@router.delete("/{id}")
def eliminar_mision(id: int, session: Session = Depends(get_session)):
    m = session.get(Mision, id)
    if not m:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    m.activo = False
    session.add(m)
    session.commit()
    return {"mensaje": "Misión marcada como inactiva"}
