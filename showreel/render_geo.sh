#!/bin/bash
# Render reanudable de la versión de 30 s (ambos formatos en paralelo)
cd "$(dirname "$0")"
for v in h v; do
  ( until [ "$(ls framesG_$v 2>/dev/null | wc -l)" -ge 900 ]; do node capture.js geo.html $v full framesG_$v 30; done ) &
done
wait
echo RENDERG_DONE
