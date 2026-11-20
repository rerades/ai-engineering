from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.config import get_settings
from app.services.llm_service import generate_estimation

router = APIRouter(prefix="/api/v1", tags=["estimations"])


class EstimationRequest(BaseModel):
    transcription: str = Field(min_length=1, description="Transcripción de la reunión con el cliente")


class EstimationResponse(BaseModel):
    estimation: str
    model: str
    provider: str


@router.post("/estimate", response_model=EstimationResponse)
async def estimate(request: EstimationRequest) -> EstimationResponse:
    settings = get_settings()
    try:
        estimation = await generate_estimation(request.transcription)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Error llamando al LLM: {exc}") from exc
    return EstimationResponse(estimation=estimation, model=settings.llm_model, provider=settings.llm_provider)
