from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.config import get_settings
from app.services.llm_service import generate_estimation

MIN_TRANSCRIPTION_LENGTH = 1

router = APIRouter(tags=["estimations"])


class EstimationRequest(BaseModel):
    transcription: str = Field(min_length=MIN_TRANSCRIPTION_LENGTH, description="Transcripción de la reunión con el cliente")


class EstimationResponse(BaseModel):
    estimation: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    cost_usd: float | None = Field(description="Coste real cobrado por OpenRouter (usage.cost)")
    created_at: datetime


@router.post("/estimate", response_model=EstimationResponse)
async def estimate(request: EstimationRequest) -> EstimationResponse:
    try:
        completion = await generate_estimation(request.transcription)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Error llamando al LLM: {exc}") from exc
    return EstimationResponse(
        estimation=completion.choices[0].message.content,
        model=completion.model,  # el modelo que realmente sirvió la respuesta
        provider=get_settings().llm_provider,
        input_tokens=completion.usage.prompt_tokens,
        output_tokens=completion.usage.completion_tokens,
        cost_usd=getattr(completion.usage, "cost", None),
        created_at=datetime.now(timezone.utc),
    )
