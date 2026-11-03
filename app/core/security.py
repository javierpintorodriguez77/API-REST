from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

password_hash = PasswordHash.recommended()


def hashear_password(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def crear_token(usuario, tipo: str, duracion: timedelta) -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    jti = str(uuid4())
    payload = {"sub": str(usuario.id), "rol": usuario.rol.value, "type": tipo,
               "iat": now, "exp": now + duracion, "jti": jti}
    settings = get_settings()
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm), jti

