#!/usr/bin/env bash
set -euo pipefail
DIR="${MIROFISH_DIR:-/home/user/MiroFish}"

if [ -d "$DIR/.git" ]; then
  git -C "$DIR" pull --ff-only || echo "aviso: no se pudo actualizar, sigo con la copia actual"
else
  git clone --depth 1 https://github.com/666ghj/MiroFish.git "$DIR"
fi
cd "$DIR"

npm run setup
uv python install 3.12
(cd backend && uv sync --python 3.12)

if [ ! -f .env ]; then
  {
    echo "LLM_API_KEY=${LLM_API_KEY:-your_api_key_here}"
    echo "LLM_BASE_URL=${LLM_BASE_URL:-https://dashscope.aliyuncs.com/compatible-mode/v1}"
    echo "LLM_MODEL_NAME=${LLM_MODEL_NAME:-qwen-plus}"
    echo "ZEP_API_KEY=${ZEP_API_KEY:-your_zep_api_key_here}"
    if [ -n "${LLM_BOOST_API_KEY:-}" ]; then
      echo "LLM_BOOST_API_KEY=$LLM_BOOST_API_KEY"
      echo "LLM_BOOST_BASE_URL=${LLM_BOOST_BASE_URL:-}"
      echo "LLM_BOOST_MODEL_NAME=${LLM_BOOST_MODEL_NAME:-}"
    fi
  } > .env
  chmod 600 .env
fi

missing=$(grep -E '=(your_|$)' .env | cut -d= -f1 | tr '\n' ' ' || true)
if [ -n "$missing" ]; then
  echo "MiroFish instalado en $DIR. Faltan claves en .env: $missing"
else
  echo "MiroFish instalado en $DIR con .env completo."
fi
