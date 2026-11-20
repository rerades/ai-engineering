from fastapi import FastAPI

from app.config import get_settings
from app.routers import estimations

API_PREFIX = "/api/v1"

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
