#!/bin/bash
# Render reanudable de la versión de 30 s (ambos formatos en paralelo)
cd "$(dirname "$0")"
for v in h v; do
  ( until [ "$(ls frames30_$v 2>/dev/null | wc -l)" -ge 900 ]; do node capture.js cinematic.html $v full frames30_$v 30; done ) &
done
wait
echo RENDER30_DONE
