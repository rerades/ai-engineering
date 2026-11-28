"""Chat Streamlit para el estimador CAG.

Lanzar desde estimador-cag/:  uv run streamlit run streamlit_app.py
La API key se lee de .env (o del entorno) igual que la API FastAPI.
"""

import asyncio
import threading

import streamlit as st

from app.services.llm_service import generate_estimation


@st.cache_resource
def _event_loop() -> asyncio.AbstractEventLoop:
    # Un único loop vivo para toda la app: el cliente AsyncOpenAI cacheado guarda
    # conexiones atadas a su loop, y asyncio.run() crearía uno nuevo en cada mensaje.
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    return loop


def estimate(transcript: str) -> str:
    future = asyncio.run_coroutine_threadsafe(generate_estimation(transcript), _event_loop())
    return future.result().choices[0].message.content


st.set_page_config(page_title="Estimador CAG", page_icon="📋")
st.title("📋 Estimador de proyectos de software")
st.caption("Pega la transcripción de una reunión con el cliente y recibe una estimación de esfuerzo.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if transcript := st.chat_input("Escribe o pega la transcripción de la reunión…"):
    st.session_state.messages.append({"role": "user", "content": transcript})
    with st.chat_message("user"):
        st.markdown(transcript)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Estimando…"):
                estimation = estimate(transcript)
        except Exception as exc:
            st.error(f"Error llamando al LLM: {exc}")
        else:
            st.markdown(estimation)
            st.session_state.messages.append({"role": "assistant", "content": estimation})
