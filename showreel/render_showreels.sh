#!/bin/bash
# Re-render reanudable de los showreels del Acuerdo 01-2026 (15 s y 30 s, 16:9 y 9:16)
cd "$(dirname "$0")"
while pgrep -f "render_plazo.sh" >/dev/null; do sleep 15; done   # espera a que termine la pieza del art. 25
for dur in 15 30; do
  pre=$([ $dur = 15 ] && echo frames || echo frames30); n=$((dur*30))
  for v in h v; do
    ( until [ "$(ls ${pre}_$v 2>/dev/null | wc -l)" -ge $n ]; do node capture.js cinematic.html $v full ${pre}_$v $dur; done ) &
  done
  wait
done
echo SHOWREELS_DONE
