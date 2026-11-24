from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.dependencies import SessionDep, requiere_rol
from app.models.usuario import RolUsuario, Usuario
from app.schemas.libro import LibroCrear, LibroRespuesta
from app.services import libros as libros_service

router = APIRouter(prefix="/libros", tags=["libros"])
personal_biblioteca = requiere_rol(RolUsuario.admin, RolUsuario.bibliotecario)


@router.post("", response_model=LibroRespuesta, status_code=status.HTTP_201_CREATED)
def crear_libro(datos: LibroCrear, db: SessionDep, _: Usuario = personal_biblioteca):
    try:
        return libros_service.crear_libro(db, datos)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/{libro_id}/portada", response_model=LibroRespuesta)
async def subir_portada_libro(
    libro_id: int,
    db: SessionDep,
    _: Usuario = personal_biblioteca,
    archivo: UploadFile = File(...),
):
    if archivo.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=415, detail="La portada debe ser JPG, PNG o WEBP")
    try:
        return libros_service.guardar_portada(db, libro_id, await archivo.read())
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.get("/{libro_id}", response_model=LibroRespuesta)
def obtener_libro(libro_id: int, db: SessionDep):
    try:
        return libros_service.obtener_libro(db, libro_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
