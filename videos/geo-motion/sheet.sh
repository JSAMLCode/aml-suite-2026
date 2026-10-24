#!/bin/bash
# Hoja de contactos: fotogramas indicados, en rejilla de 4 columnas a 480 px
# Uso: ./sheet.sh video.mp4 salida.png 30 60 90 ...
v=$1; o=$2; shift 2
tmp=$(mktemp -d)
i=0
for f in "$@"; do
  ffmpeg -nostdin -loglevel error -y -i "$v" -vf "select=eq(n\,$f),scale=480:-1,drawtext=text='f$f':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6" -frames:v 1 "$tmp/$(printf %03d $i).png"
  i=$((i+1))
done
ffmpeg -nostdin -loglevel error -y -pattern_type glob -i "$tmp/*.png" -vf "tile=4x$(( (i+3)/4 ))" -frames:v 1 "$o"
rm -rf "$tmp"
