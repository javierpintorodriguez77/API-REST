from typing import Annotated
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import get_db
from app.core.exceptions import NoAutenticado, Prohibido
from app.models.usuario import RolUsuario, Usuario

SessionDep = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(db: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> Usuario:
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        if payload.get("type") != "access" or not payload.get("sub"):
            raise NoAutenticado("Tipo de token inválido")
    except (jwt.InvalidTokenError, ValueError):
        raise NoAutenticado("Token inválido o vencido")
    user = db.scalar(select(Usuario).where(Usuario.id == int(payload["sub"])))
    if user is None:
        raise NoAutenticado("Usuario no encontrado")
    if not user.activo:
        raise Prohibido("Usuario inactivo")
    return user


CurrentUser = Annotated[Usuario, Depends(get_current_user)]


def requiere_rol(*roles: RolUsuario):
    def verificar(usuario: CurrentUser) -> Usuario:
        if usuario.rol not in roles:
            raise Prohibido()
        return usuario
    return Depends(verificar)

