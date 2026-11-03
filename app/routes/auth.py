from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, update

from app.core.config import get_settings
from app.core.dependencies import CurrentUser, SessionDep
from app.core.exceptions import CuentaBloqueada, NoAutenticado
from app.core.security import crear_token, hashear_password, verificar_password
from app.models.refresh_token import RefreshToken
from app.models.socio import Socio
from app.models.usuario import RolUsuario, Usuario
from app.schemas.auth import CambioPassword, RefreshRequest, TokenRespuesta, UsuarioRegistro
from app.schemas.usuario import UsuarioRespuesta

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registro", response_model=UsuarioRespuesta, status_code=201, summary="Registrar socio")
def registro(datos: UsuarioRegistro, db: SessionDep):
    email = str(datos.email).lower()
    if db.scalar(select(Usuario).where(Usuario.email == email)):
        raise HTTPException(409, "El email ya está registrado")
    socio = Socio(nombre=datos.nombre.title(), telefono=datos.telefono)
    db.add(socio); db.flush()
    user = Usuario(email=email, nombre=datos.nombre.title(), password_hash=hashear_password(datos.password), socio_id=socio.id)
    db.add(user); db.commit(); db.refresh(user)
    return user


@router.post("/login", response_model=TokenRespuesta, summary="Iniciar sesión")
def login(db: SessionDep, form: OAuth2PasswordRequestForm = Depends()):
    user = db.scalar(select(Usuario).where(Usuario.email == form.username.lower()))
    now = datetime.now(timezone.utc)
    if user and user.bloqueado_hasta and user.bloqueado_hasta > now:
        raise CuentaBloqueada()
    valid = user is not None and verificar_password(form.password, user.password_hash)
    if not valid:
        if user:
            user.intentos_fallidos += 1
            if user.intentos_fallidos >= 5:
                user.bloqueado_hasta = now + timedelta(minutes=15)
            db.commit()
        raise NoAutenticado("Credenciales inválidas")
    if not user.activo:
        raise HTTPException(403, "Usuario inactivo")
    user.intentos_fallidos = 0; user.bloqueado_hasta = None
    settings = get_settings()
    access, _ = crear_token(user, "access", timedelta(minutes=settings.access_token_expire_minutes))
    refresh, jti = crear_token(user, "refresh", timedelta(days=settings.refresh_token_expire_days))
    db.add(RefreshToken(jti=jti, usuario_id=user.id, expira_en=now + timedelta(days=settings.refresh_token_expire_days)))
    db.commit()
    return TokenRespuesta(access_token=access, refresh_token=refresh, expires_in=settings.access_token_expire_minutes * 60)


def _refresh(request: RefreshRequest, db):
    try:
        payload = __import__("jwt").decode(request.refresh_token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        if payload.get("type") != "refresh": raise ValueError()
    except Exception:
        raise NoAutenticado("Refresh token inválido")
    row = db.scalar(select(RefreshToken).where(RefreshToken.jti == payload.get("jti")))
    if not row or row.revocado or row.expira_en < datetime.now(timezone.utc):
        db.execute(update(RefreshToken).where(RefreshToken.usuario_id == row.usuario_id if row else False).values(revocado=True)); db.commit()
        raise NoAutenticado("Refresh token inválido")
    user = db.get(Usuario, row.usuario_id)
    row.revocado = True
    settings = get_settings(); now = datetime.now(timezone.utc)
    access, _ = crear_token(user, "access", timedelta(minutes=settings.access_token_expire_minutes))
    refresh, jti = crear_token(user, "refresh", timedelta(days=settings.refresh_token_expire_days))
    db.add(RefreshToken(jti=jti, usuario_id=user.id, expira_en=now + timedelta(days=settings.refresh_token_expire_days))); db.commit()
    return TokenRespuesta(access_token=access, refresh_token=refresh, expires_in=settings.access_token_expire_minutes * 60)


@router.post("/refresh", response_model=TokenRespuesta)
def refresh(request: RefreshRequest, db: SessionDep): return _refresh(request, db)


@router.post("/logout", status_code=204)
def logout(request: RefreshRequest, db: SessionDep):
    db.execute(update(RefreshToken).where(RefreshToken.jti == request.refresh_token).values(revocado=True)); db.commit()
    return Response(status_code=204)


@router.get("/me", response_model=UsuarioRespuesta)
def me(user: CurrentUser): return user


@router.patch("/me/password", status_code=204)
def password(data: CambioPassword, user: CurrentUser, db: SessionDep):
    if not verificar_password(data.password_actual, user.password_hash): raise NoAutenticado("Contraseña actual inválida")
    user.password_hash = hashear_password(data.password_nueva)
    db.execute(update(RefreshToken).where(RefreshToken.usuario_id == user.id).values(revocado=True)); db.commit()
    return Response(status_code=204)

