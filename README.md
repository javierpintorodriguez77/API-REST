# Biblioteca API

## Frontend Vue 3

El panel web vive en `frontend/` y consume la API mediante `VITE_API_URL`.

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Por defecto, el frontend espera la API en `http://127.0.0.1:8000/api/v1`. Para desarrollo local, agrega `http://localhost:5173` a `CORS_ORIGINS` en el `.env` del backend.

API REST segura con FastAPI, SQLAlchemy, Alembic, Argon2 y JWT.

## Puesta en marcha

Para crear o actualizar las tablas de la base de datos en Windows, ejecuta:

```powershell
.\migrate.ps1
```

El script usa el ejecutable de Alembic del entorno virtual. No uses `python -m alembic`, porque la carpeta local `alembic/` entra en conflicto con el paquete instalado.

1. Copia `.env.example` a `.env` y cambia `SECRET_KEY` por una clave de al menos 32 caracteres.
2. Instala dependencias: `pip install -r requirements-dev.txt`.
3. Revisa/aplica migraciones: `alembic upgrade head`.
4. Ejecuta: `fastapi dev app/main.py`.

La documentación queda disponible en `/docs` en entornos `dev` y `test`. El registro y login están bajo `/api/v1/auth`.

