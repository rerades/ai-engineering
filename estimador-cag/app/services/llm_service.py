from functools import lru_cache

from openai import AsyncOpenAI

from app.config import get_settings
from app.context.examples import ESTIMATION_EXAMPLES

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
        f"### Ejemplo {i}\n**Reunión:** {ex['meeting_summary']}\n\n{ex['estimation']}"
        for i, ex in enumerate(ESTIMATION_EXAMPLES, 1)
    )
    return f"{SYSTEM_INSTRUCTIONS}\n\n## Estimaciones previas de referencia\n\n{examples}"


@lru_cache
def _client() -> AsyncOpenAI:
    s = get_settings()
    return AsyncOpenAI(api_key=s.openai_api_key, base_url=s.openai_base_url)


async def generate_estimation(transcript: str) -> str:
    settings = get_settings()
    if settings.llm_provider != "openai":
        raise NotImplementedError(f"Proveedor no implementado: {settings.llm_provider}")

    response = await _client().chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": transcript},
        ],
        temperature=0.2,  # estimar es casi determinista
        max_tokens=1500,  # techo de seguridad, no control de longitud
    )
    return response.choices[0].message.content
