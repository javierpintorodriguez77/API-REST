import logging
import time
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routes import auth, health, libros

settings = get_settings()
app = FastAPI(title="Biblioteca API", version="1.0.0", docs_url=None if settings.environment == "prod" else "/docs", redoc_url=None if settings.environment == "prod" else "/redoc")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.middleware("http")
async def request_log(request: Request, call_next):
    request_id = str(uuid4()); start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logging.getLogger("biblioteca").info("%s %s %s %.2fms", request.method, request.url.path, response.status_code, (time.perf_counter() - start) * 1000)
    return response


app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(libros.router, prefix="/api/v1")

