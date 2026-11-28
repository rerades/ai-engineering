"""Chat Streamlit para el estimador CAG.

Lanzar desde estimador-cag/:  uv run streamlit run streamlit_app.py
La API key se lee de .env (o del entorno) igual que la API FastAPI.
"""

import asyncio
import threading
from collections.abc import Iterator

import streamlit as st

from app.services.llm_service import stream_estimation


@st.cache_resource
def _event_loop() -> asyncio.AbstractEventLoop:
    # Un único loop vivo para toda la app: el cliente AsyncOpenAI cacheado guarda
    # conexiones atadas a su loop, y asyncio.run() crearía uno nuevo en cada mensaje.
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    return loop


def estimate_stream(transcript: str) -> Iterator[str]:
    """Puente síncrono para st.write_stream: saca cada trozo del generador async en el loop de fondo."""
    loop = _event_loop()
    chunks = stream_estimation(transcript)
    try:
        while True:
            try:
                yield asyncio.run_coroutine_threadsafe(anext(chunks), loop).result()
            except StopAsyncIteration:
                return
    finally:
        asyncio.run_coroutine_threadsafe(chunks.aclose(), loop).result()


st.set_page_config(page_title="Estimador CAG", page_icon="📋")
st.title("📋 Estimador de proyectos de software")
st.caption("Pega la transcripción de una reunión con el cliente y recibe una estimación de esfuerzo.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if transcript := st.chat_input("Escribe o pega la transcripción de la reunión…", submit_mode="disable"):
    st.session_state.messages.append({"role": "user", "content": transcript})
    with st.chat_message("user"):
        st.markdown(transcript)

    with st.chat_message("assistant"):
        try:
            estimation = st.write_stream(estimate_stream(transcript))
        except Exception as exc:
            st.error(f"Error llamando al LLM: {exc}")
        else:
            st.session_state.messages.append({"role": "assistant", "content": estimation})
