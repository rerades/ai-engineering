"""Chat Streamlit para el estimador CAG.

Lanzar desde estimador-cag/:  uv run streamlit run streamlit_app.py
La API key se lee de .env (o del entorno) igual que la API FastAPI.
"""

import asyncio
import threading
import time
from collections.abc import Iterator

import streamlit as st

from app.context.examples import ESTIMATION_EXAMPLES
from app.services.llm_service import SYSTEM_INSTRUCTIONS, build_system_prompt, stream_estimation


@st.cache_resource
def _event_loop() -> asyncio.AbstractEventLoop:
    # Un único loop vivo para toda la app: el cliente AsyncOpenAI cacheado guarda
    # conexiones atadas a su loop, y asyncio.run() crearía uno nuevo en cada mensaje.
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    return loop


def estimate_stream(transcript: str, metrics: dict) -> Iterator[str]:
    """Puente síncrono para st.write_stream: saca cada chunk del generador async en el loop
    de fondo, emite el texto y va rellenando `metrics` (modelo, tokens, tiempos)."""
    loop = _event_loop()
    chunks = stream_estimation(transcript)
    started = time.perf_counter()
    try:
        while True:
            try:
                chunk = asyncio.run_coroutine_threadsafe(anext(chunks), loop).result()
            except StopAsyncIteration:
                break
            metrics["model"] = chunk.model or metrics.get("model")
            if chunk.usage:
                metrics["input_tokens"] = chunk.usage.prompt_tokens
                metrics["output_tokens"] = chunk.usage.completion_tokens
            if chunk.choices and chunk.choices[0].delta.content:
                metrics.setdefault("first_token_seconds", time.perf_counter() - started)
                yield chunk.choices[0].delta.content
        metrics["total_seconds"] = time.perf_counter() - started
    finally:
        asyncio.run_coroutine_threadsafe(chunks.aclose(), loop).result()


def render_metrics(metrics: dict | None) -> None:
    st.subheader(":material/monitoring: Última llamada")
    if not metrics:
        st.caption("Aún no hay llamadas en esta sesión.")
        return
    st.metric("Modelo", metrics.get("model", "—"))
    input_column, output_column = st.columns(2)
    input_column.metric("Tokens de entrada", metrics.get("input_tokens", "—"))
    output_column.metric("Tokens de salida", metrics.get("output_tokens", "—"))
    total_column, first_token_column = st.columns(2)
    total_column.metric("Tiempo de respuesta", f"{metrics['total_seconds']:.1f} s")
    first_token_column.metric("Primer token", f"{metrics['first_token_seconds']:.1f} s")


st.set_page_config(page_title="Estimador CAG", page_icon="📋")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.last_metrics = None

with st.sidebar:
    st.header("Contexto CAG")
    st.caption("Lo que recibe el modelo en cada llamada, además de tu transcripción.")

    st.subheader(":material/description: System prompt")
    st.code(SYSTEM_INSTRUCTIONS, language=None, wrap_lines=True)

    st.subheader(f":material/library_books: Estimaciones de ejemplo ({len(ESTIMATION_EXAMPLES)})")
    for position, example in enumerate(ESTIMATION_EXAMPLES, start=1):
        with st.expander(f"Ejemplo {position}"):
            st.markdown(f"**Reunión:** {example['meeting_summary']}")
            st.markdown(example["estimation"])

    with st.expander("Prompt completo enviado al modelo"):
        st.code(build_system_prompt(), language="markdown", wrap_lines=True)

    st.divider()
    # Hueco reservado: se rellena al final del script, después de la llamada al LLM,
    # para que muestre la llamada recién hecha y no la anterior.
    metrics_slot = st.container()

st.title("📋 Estimador de proyectos de software")
st.caption("Pega la transcripción de una reunión con el cliente y recibe una estimación de esfuerzo.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if transcript := st.chat_input("Escribe o pega la transcripción de la reunión…", submit_mode="disable"):
    st.session_state.messages.append({"role": "user", "content": transcript})
    with st.chat_message("user"):
        st.markdown(transcript)

    with st.chat_message("assistant"):
        metrics: dict = {}
        try:
            estimation = st.write_stream(estimate_stream(transcript, metrics))
        except Exception as exc:
            st.error(f"Error llamando al LLM: {exc}")
        else:
            st.session_state.messages.append({"role": "assistant", "content": estimation})
            st.session_state.last_metrics = metrics

with metrics_slot:
    render_metrics(st.session_state.last_metrics)
