from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.cloudinary import subir_portada
from app.models.libro import Libro
from app.schemas.libro import LibroCrear


def crear_libro(db: Session, datos: LibroCrear) -> Libro:
    if datos.isbn and db.scalar(select(Libro).where(Libro.isbn == datos.isbn)):
        raise ValueError("El ISBN ya está registrado")

    libro = Libro(**datos.model_dump())
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


def obtener_libro(db: Session, libro_id: int) -> Libro:
    libro = db.get(Libro, libro_id)
    if libro is None:
        raise LookupError("Libro no encontrado")
    return libro


def guardar_portada(db: Session, libro_id: int, contenido: bytes) -> Libro:
    libro = obtener_libro(db, libro_id)
    libro.portada_url = subir_portada(contenido, libro.id)
    db.commit()
    db.refresh(libro)
    return libro
