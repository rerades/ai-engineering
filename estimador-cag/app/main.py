from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.config import get_settings
from app.routers import estimations

API_PREFIX = "/api/v1"
INDEX_HTML = Path(__file__).parent / "static" / "index.html"

app = FastAPI(
    title="Estimador CAG",
    description=(
        "Genera estimaciones de proyectos de software a partir de la transcripción de una "
        "reunión con el cliente. Arquitectura CAG: estimaciones previas inyectadas en el prompt."
    ),
    version="0.1.0",
)
app.include_router(estimations.router, prefix=API_PREFIX)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "environment": settings.app_env, "provider": settings.llm_provider}


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(INDEX_HTML)
