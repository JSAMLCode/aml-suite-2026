set -e
mkdir -p snd
# colchón armónico (La menor) 15 s
ffmpeg -loglevel error -y -f lavfi -i "sine=f=110:d=15" -f lavfi -i "sine=f=164.8:d=15" -f lavfi -i "sine=f=220:d=15" -f lavfi -i "sine=f=261.6:d=15" -f lavfi -i "sine=f=329.6:d=15" \
 -filter_complex "[0]volume=.35[a];[1]volume=.18[b];[2]volume=.16[c];[3]volume=.10[d];[4]volume=.07[e];[a][b][c][d][e]amix=inputs=5:normalize=0,tremolo=f=2:d=0.25,afade=t=in:d=1,afade=t=out:st=13.8:d=1.2,volume=.55" snd/pad.wav
# whoosh
ffmpeg -loglevel error -y -f lavfi -i "anoisesrc=d=0.7:c=pink:a=.6" -af "highpass=f=700,lowpass=f=9000,afade=t=in:d=0.4,afade=t=out:st=0.4:d=0.3" snd/whoosh.wav
# impacto grave
ffmpeg -loglevel error -y -f lavfi -i "sine=f=55:d=0.8" -af "afade=t=out:d=0.8,volume=1.6" snd/hit.wav
# blip palabras
ffmpeg -loglevel error -y -f lavfi -i "sine=f=1320:d=0.12" -af "afade=t=out:d=0.12,volume=.5" snd/blip.wav
# campanilla final
ffmpeg -loglevel error -y -f lavfi -i "sine=f=1760:d=1.6" -af "afade=t=out:d=1.6,volume=.35" snd/chime.wav
inputs=(-i snd/pad.wav); fc=""; n=1; labels="[0]"
add(){ f=$1; t=$2; inputs+=(-i snd/$f.wav); ms=$(python3 -c "print(int(($t)*1000))"); fc+="[$n]adelay=${ms}|${ms}[x$n];"; labels+="[x$n]"; n=$((n+1)); }
for b in 2.2 5.2 8.2 11.0 13.4; do add whoosh $(python3 -c "print($b-.3)"); add hit $b; done
add hit 0.3
for w in 11.05 11.55 12.05 12.55; do add blip $w; done
add chime 13.9
ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "${fc}${labels}amix=inputs=$n:normalize=0,alimiter=limit=0.9" -t 15 snd/mix.wav
