from functools import lru_cache

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from app.config import get_settings
from app.context.examples import ESTIMATION_EXAMPLES

TEMPERATURE = 0.2  # estimar es casi determinista
MAX_OUTPUT_TOKENS = 1500  # techo de seguridad, no control de longitud

SYSTEM_INSTRUCTIONS = """\
Eres un estimador de proyectos de software con más de 15 años de experiencia.
Recibes la transcripción de una reunión con un cliente y generas una estimación de esfuerzo.

Reglas:
- Básate en las estimaciones previas de referencia: imita su formato y mantén horas coherentes con ellas.
- Desglosa en tareas con horas y coste (tarifa 50 €/h). El total debe ser la suma exacta de las tareas.
- Indica equipo recomendado y duración estimada.
- Si la transcripción no da información suficiente, indica qué supuestos has hecho.
- Responde solo con la estimación, en Markdown y en español."""


def build_system_prompt() -> str:
    examples = "\n\n".join(
        f"### Ejemplo {position}\n**Reunión:** {example['meeting_summary']}\n\n{example['estimation']}"
        for position, example in enumerate(ESTIMATION_EXAMPLES, start=1)
    )
    return f"{SYSTEM_INSTRUCTIONS}\n\n## Estimaciones previas de referencia\n\n{examples}"


@lru_cache
def _client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)


async def generate_estimation(transcript: str) -> ChatCompletion:
    settings = get_settings()
    if settings.llm_provider != "openai":
        raise NotImplementedError(f"Proveedor no implementado: {settings.llm_provider}")

    return await _client().chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": transcript},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_OUTPUT_TOKENS,
    )
