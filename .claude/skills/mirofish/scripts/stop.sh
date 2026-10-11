#!/usr/bin/env bash
DIR="${MIROFISH_DIR:-/home/user/MiroFish}"
for s in backend frontend; do
  f="$DIR/logs/$s.pid"
  [ -f "$f" ] || continue
  kill -- -"$(cat "$f")" 2>/dev/null   # start.sh usa setsid: el PID es el líder del grupo
  rm -f "$f"
done
echo "MiroFish detenido."
