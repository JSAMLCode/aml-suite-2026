#!/usr/bin/env bash
set -euo pipefail
DIR="${MIROFISH_DIR:-/home/user/MiroFish}"
[ -d "$DIR/backend/.venv" ] || bash "$(dirname "$0")/install.sh"
mkdir -p "$DIR/logs"

cd "$DIR/backend"
setsid nohup uv run python run.py > "$DIR/logs/backend.log" 2>&1 &
echo $! > "$DIR/logs/backend.pid"

cd "$DIR/frontend"
setsid nohup npx vite --host --open false > "$DIR/logs/frontend.log" 2>&1 &
echo $! > "$DIR/logs/frontend.pid"

for _ in $(seq 1 60); do
  b=$(curl -s -o /dev/null -w '%{http_code}' localhost:5001/health || true)
  f=$(curl -s -o /dev/null -w '%{http_code}' localhost:3000 || true)
  [ "$b" = 200 ] && [ "$f" = 200 ] && break
  sleep 1
done
echo "backend :5001 -> $b | frontend :3000 -> $f (logs en $DIR/logs)"
