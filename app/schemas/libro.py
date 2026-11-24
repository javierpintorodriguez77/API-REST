from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LibroCrear(BaseModel):
    titulo: str
    autor: str
    isbn: str | None = None


class LibroRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    autor: str
    isbn: str | None
    portada_url: str | None
    creado_en: datetime
