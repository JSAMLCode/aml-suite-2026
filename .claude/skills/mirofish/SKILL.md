---
name: mirofish
description: Instala, configura y arranca MiroFish (motor de inteligencia de enjambre que simula agentes sociales con OASIS + Zep para predecir escenarios). Úsala cuando pidan instalar MiroFish, levantarlo, simular reacción de un público o mercado, o retomar una simulación en una sesión nueva.
---

# mirofish

Repo: https://github.com/666ghj/MiroFish (AGPL-3.0). Se instala fuera del repo
de trabajo, en `$MIROFISH_DIR` (por defecto `/home/user/MiroFish`), para no
mezclar código AGPL con el SaaS propietario.

## Flujo

1. **Instalar** (idempotente, ~2 min): `bash .claude/skills/mirofish/scripts/install.sh`
   - Clona el repo si falta; si existe, hace `git pull --ff-only`.
   - Fuerza Python 3.12 con uv (el backend exige ≥3.11,<3.13; el contenedor trae 3.13).
   - `npm run setup` + `uv sync`.
   - Genera `.env` desde variables de entorno si existen; nunca sobrescribe un `.env` ya editado.
2. **Claves.** Necesita `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL_NAME` (cualquier API
   compatible con OpenAI) y `ZEP_API_KEY`. Lo correcto es definirlas como secretos del
   entorno cloud para que lleguen solas a cada sesión. Si faltan, pídelas al usuario y
   escríbelas solo en `$MIROFISH_DIR/.env`. Nunca las comitees ni las imprimas.
   Las variables `LLM_BOOST_*` se omiten salvo que el usuario las aporte: si aparecen
   con valores de ejemplo, el backend intenta usarlas.
3. **Arrancar:** `bash .claude/skills/mirofish/scripts/start.sh`
   - Backend Flask en `:5001`, frontend Vite en `:3000`, en segundo plano.
   - No uses `npm run dev`: Vite intenta abrir navegador (`xdg-open` no existe) y
     `concurrently --kill-others` tumba también el backend.
   - Logs en `$MIROFISH_DIR/logs/`. Parar: `bash .claude/skills/mirofish/scripts/stop.sh`.
4. **Verificar:** `curl -s localhost:5001/health` y `curl -sI localhost:3000` deben dar 200.

## Advertencias

- Cada simulación hace muchas llamadas al LLM; empezar con menos de 40 rondas.
- Los `SyntaxWarning` de `zep_cloud` al arrancar son ruido, no errores.
- El contenedor cloud es efímero: la instalación se pierde al cerrar la sesión.
  Para uso continuo, recomendar instalación local o `docker compose up -d`.
