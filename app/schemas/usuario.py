from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.usuario import RolUsuario


class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    nombre: str
    rol: RolUsuario
    activo: bool
    socio_id: int | None
    creado_en: datetime

