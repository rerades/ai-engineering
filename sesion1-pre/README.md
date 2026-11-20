# Sesión 1: modelos de IA vía API

Ejercicios previos a la sesión. Consisten en llamar a un LLM por API desde un notebook y ver los conceptos base: system prompt, metadatos de la respuesta y coste por tokens.

| Notebook | Qué hace |
|---|---|
| `01_llamadas_api.ipynb` | Primera llamada a `gpt-4o-mini` a través de OpenRouter, con el SDK de OpenAI. |
| `02_system_prompt.ipynb` | Envía el mismo mensaje con y sin system prompt (experto en estimación) y compara tono, detalle y estructura. |
| `03_metadatos_coste.ipynb` | Lee de la respuesta el modelo y los tokens de entrada y salida, estima el coste y lo compara con el `usage.cost` real de OpenRouter. |

## Puesta en marcha

```bash
pip install openai python-dotenv jupyter
echo 'OPENROUTER_API_KEY=sk-or-...' > .env   # git lo ignora
```

Abre los notebooks en VS Code (extensión Jupyter) o en Colab.

## Ideas clave de la sesión

- Las llamadas son **atómicas y sin memoria**: en una conversación se reenvía el historial completo en cada turno.
- El **system prompt** lo define la aplicación y tiene más prioridad que el del usuario. Conviene estructurarlo así: rol, audiencia, formato, restricciones y reglas.
- `temperature` baja da respuestas casi deterministas. `max_tokens` es un techo de seguridad, no una forma de controlar la longitud.
- El **output cuesta mucho más que el input**, y el system prompt se paga en cada llamada.
- Los agregadores (**LiteLLM**, **OpenRouter**) dan una sola interfaz para todos los proveedores y permiten tener un modelo de respaldo si falla el principal.
