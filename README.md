# Biblioteca API

API REST segura con FastAPI, SQLAlchemy, Alembic, Argon2 y JWT.

## Puesta en marcha

1. Copia `.env.example` a `.env` y cambia `SECRET_KEY` por una clave de al menos 32 caracteres.
2. Instala dependencias: `pip install -r requirements-dev.txt`.
3. Revisa/aplica migraciones: `alembic upgrade head`.
4. Ejecuta: `fastapi dev app/main.py`.

La documentación queda disponible en `/docs` en entornos `dev` y `test`. El registro y login están bajo `/api/v1/auth`.

