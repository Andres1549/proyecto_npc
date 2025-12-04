from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, Session
from typing import List, Optional
from app.db import get_session
from app.models import Mision, TipoMision, NPC
from app.servicios.supabase_conexion import upload_file

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_model=List[Mision])
def listar_misiones(session: Session = Depends(get_session), skip: int = 0, limit: int = 50):
    return session.exec(select(Mision).where(Mision.activo == True).offset(skip).limit(limit)).all()


@router.get("/crear")
def form_crear_mision(request: Request, npc_id: int = None):
    return templates.TemplateResponse("formularios/mision_form.html", {"request": request, "npc_id": npc_id})


@router.post("/crear")
def crear_mision(
    request: Request,
    npc_id: int = Form(...),
    titulo: str = Form(...),
    descripcion: str = Form(...),
    recompensa: str = Form(...),
    tipo: TipoMision = Form(...),
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
    session.refresh(m)
    return RedirectResponse(url=f"/npcs/{npc_id}", status_code=303)


@router.get("/{id}", response_model=Mision)
def detalle_mision(id: int, request: Request, session: Session = Depends(get_session)):
    m = session.get(Mision, id)
    if not m:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return templates.TemplateResponse("detalles/mision_detalle.html", {"request": request, "mision": m})


@router.get("/{id}/editar")
def form_editar_mision(id: int, request: Request, session: Session = Depends(get_session)):
    m = session.get(Mision, id)
    if not m:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    npcs = session.exec(select(NPC).where(NPC.activo == True,NPC.tipo == "misiones")).all()

    return templates.TemplateResponse(
        "formularios/mision_editar.html",
        {
            "request": request,
            "mision": m,
            "npcs": npcs
        }
    )

@router.post("/{id}/editar")
def actualizar_mision_form(
    id: int,
    titulo: str = Form(...),
    descripcion: str = Form(...),
    recompensa: str = Form(...),
    tipo: TipoMision = Form(...),
    id_npc: int = Form(...),
    session: Session = Depends(get_session)
):
    m = session.get(Mision, id)
    if not m or not m.activo:
        raise HTTPException(status_code=404, detail="Misión no encontrada o inactiva")

    m.titulo = titulo
    m.descripcion = descripcion
    m.recompensa = recompensa
    m.tipo = tipo
    m.id_npc = id_npc

    session.add(m)
    session.commit()
    session.refresh(m)
    return RedirectResponse(url=f"/misiones/{id}", status_code=303)


@router.get("/{id}/eliminar")
def form_eliminar_mision(id: int, request: Request, session: Session = Depends(get_session)):
    mision = session.get(Mision, id)
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    return templates.TemplateResponse(
        "formularios/eliminar_confirmacion.html",
        {
            "request": request,
            "tipo": "mision",
            "objeto": mision
        }
    )
@router.post("/{id}/eliminar")
def eliminar_mision(id: int, session: Session = Depends(get_session)):
    m = session.get(Mision, id)
    if not m:
        raise HTTPException(status_code=404, detail="Misión no encontrada")

    m.activo = False
    session.add(m)
    session.commit()

    return RedirectResponse(url="/", status_code=303)
