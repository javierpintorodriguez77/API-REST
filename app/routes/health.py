from fastapi import APIRouter
from sqlalchemy import text
from app.core.dependencies import SessionDep

router = APIRouter(tags=["health"])


@router.get("/health", summary="Estado de la API")
def health(db: SessionDep):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except Exception:
        return {"status": "ok", "database": "error"}

