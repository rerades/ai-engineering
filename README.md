# Estimador CAG

Sesión 2: API de FastAPI que genera estimaciones de proyectos de software a partir de la transcripción de una reunión con el cliente.

Usa **CAG** (Cache-Augmented Generation): las estimaciones previas de `app/context/examples.py` se inyectan en el system prompt de cada llamada y sirven al modelo de referencia, como ejemplos *few-shot*.

```
[system]    → instrucciones + estimaciones previas de referencia
[user]      → transcripción de la reunión
[assistant] → estimación generada
```

## Estructura

| Ruta | Qué contiene |
|---|---|
| `app/main.py` | La app de FastAPI, `GET /health` y el router montado en `/api/v1` |
| `app/config.py` | `Settings` (Pydantic): lee la configuración de `.env` |
| `app/routers/estimations.py` | `POST /api/v1/estimate` y los schemas de entrada y salida |
| `app/services/llm_service.py` | Monta el system prompt con los ejemplos y llama al LLM |
| `app/context/examples.py` | Tres estimaciones históricas (ficticias) |
| `streamlit_app.py` | Chat Streamlit que reutiliza `generate_estimation` (mismo system prompt) |

## Puesta en marcha

```bash
cp .env.example .env    # pon tu clave de OpenRouter en OPENAI_API_KEY
uv run uvicorn app.main:app --reload
```

La API se llama con el SDK de OpenAI, pero a través de **OpenRouter** (`OPENAI_BASE_URL`). Por eso el modelo lleva el prefijo del proveedor: `openai/gpt-4o-mini`.

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{"transcription": "El cliente necesita una landing page con formulario..."}'
```

La respuesta incluye `estimation`, `model`, `provider`, `input_tokens`, `output_tokens`, `cost_usd` (lo que cobra OpenRouter de verdad) y `created_at`. Swagger está en `/docs`.

### Chat Streamlit

```bash
uv run streamlit run streamlit_app.py    # http://localhost:8501, lee la misma .env
```

Pega la transcripción en el chat: la estimación se va escribiendo en streaming (`st.write_stream` sobre `stream_estimation`) como mensaje del asistente, y el historial se mantiene mientras dure la sesión (`st.session_state`).

El panel lateral enseña el contexto CAG: el system prompt (solo lectura), las estimaciones de ejemplo que se inyectan, el prompt completo tal como se envía y las métricas de la última llamada (modelo, tokens de entrada y salida, tiempo de respuesta y del primer token). Los tokens llegan en el último chunk del stream gracias a `stream_options={"include_usage": True}`.

Con `.streamlit/config.toml` (`runOnSave`) y `watchdog`, la app se recarga sola al guardar, también los cambios en `app/`. Los cambios en `.env` sí requieren reiniciar.

| ✓ | Verificación (sesión 03) | Resultado |
|---|---|---|
| ✅ | `streamlit run streamlit_app.py` abre una interfaz de chat | http://localhost:8501 |
| ✅ | Pegar una transcripción devuelve una estimación | Probado con `fixtures/transcripcion-01.md` y `-02.md` |
| ✅ | La conversación persiste (varias preguntas seguidas) | Historial `user, assistant, user, assistant` |
| ✅ | La respuesta llega en streaming | Primer token en ~1 s, respuesta completa en 5–7 s |
| ✅ | La API key sale de `.env`, no del código | `Settings` (pydantic-settings) lee `OPENAI_API_KEY` |

## Checklist de verificación

| | Comprobación | Cómo se ha verificado |
|---|---|---|
| ✅ | El servidor arranca con `uv run uvicorn app.main:app --reload` | El log dice `Application startup complete`, sin errores |
| ✅ | Las API keys salen de `.env` y nunca aparecen en el código | `git grep` y `git log -p` no encuentran ninguna clave. El código solo lee `settings.openai_api_key` |
| ✅ | `GET /health` responde 200 | `{"status": "ok", "environment": "development", "provider": "openai"}` |
| ✅ | `POST /api/v1/estimate` recibe una transcripción y devuelve una estimación | 200 con la transcripción del enunciado (abajo). Si la transcripción va vacía, 422 |
| ✅ | La estimación se inspira en los ejemplos inyectados | Comparación con y sin ejemplos (abajo) |
| ✅ | Swagger accesible en `/docs` | 200 |
| ✅ | `.env` está en `.gitignore` | `git check-ignore` lo confirma y no aparece en ningún commit |

## Resultado con la transcripción del enunciado

> En la reunión con el equipo de marketing, el cliente explicó que necesita una landing page con formulario de contacto, integración con su CRM actual (HubSpot), y una sección de blog con editor WYSIWYG. El plazo ideal sería tenerlo listo en 4 semanas. El diseño ya existe en Figma.

```json
{
  "model": "openai/gpt-4o-mini",
  "provider": "openai",
  "input_tokens": 944,
  "output_tokens": 193,
  "cost_usd": 0.0002574
}
```

## Comparación: con y sin ejemplos

Misma transcripción, mismas instrucciones, mismo modelo y misma temperatura. La única diferencia es si el system prompt lleva los ejemplos del paso 3.

### Con ejemplos (CAG)

```markdown
## Estimación: Landing Page con Formulario de Contacto e Integración CRM

### Desglose de tareas:
1. Revisión y adaptación del diseño de Figma: 15 horas (750 €)
2. Desarrollo de la landing page (HTML/CSS/JavaScript): 30 horas (1.500 €)
3. Implementación del formulario de contacto y validaciones: 20 horas (1.000 €)
4. Integración con HubSpot (API): 25 horas (1.250 €)
5. Desarrollo de la sección de blog con editor WYSIWYG: 40 horas (2.000 €)
6. Testing y QA: 20 horas (1.000 €)

**Total estimado: 150 horas (7.500 €)**
**Equipo recomendado: 1 desarrollador frontend + 1 desarrollador backend + 1 diseñador UX (part-time)**
**Duración estimada: 4 semanas**
```

### Sin ejemplos

```markdown
# Estimación de Esfuerzo para Landing Page

## Desglose de Tareas
1. Revisión del diseño en Figma — 4 h (200 €)
2. Desarrollo de la Landing Page — 16 h (800 €)
3. Implementación del formulario de contacto — 8 h (400 €)
4. Integración con HubSpot (CRM) — 12 h (600 €)
5. Desarrollo de la sección de blog con editor WYSIWYG — 20 h (1000 €)
6. Pruebas y ajustes finales — 8 h (400 €)
7. Documentación y entrega — 4 h (200 €)

## Resumen de Costes
- Total Horas: 72
- Total Coste: 3600 €
```

*(La salida sin ejemplos está condensada: el modelo puso horas y coste en líneas separadas.)*

| | Con ejemplos | Sin ejemplos |
|---|---|---|
| Formato de los ejemplos | Igual, con los 5 encabezados | Distinto, con 0 de los 5 encabezados |
| Total | **150 h (7.500 €)** | **72 h (3.600 €)** |
| Equipo y duración | Sí | No, aunque las instrucciones lo piden |
| Testing | 20 h (los ejemplos tienen 25 h) | 8 h |

**Conclusión:** los ejemplos no solo dan el formato, también la **escala**. Sin ellos, el modelo estima menos de la mitad de horas. Con ellos, el total se mueve en el mismo rango que las estimaciones históricas.

**Limitaciones observadas:**
- Recomienda un diseñador UX aunque el diseño ya existe en Figma.
- Construye el editor del blog desde cero en lugar de integrar uno existente.

Se podría corregir añadiendo ejemplos con diseño previo o afinando las reglas del system prompt.
