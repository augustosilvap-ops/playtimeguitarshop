#!/usr/bin/env bash
# Monta um Reel de 7 s: filmagem real (Mixkit) + painel de vidro com desfoque + texto fixo.
# Uso: src/reel.sh <id_mixkit> <inicio_s> <crop_x> <overlay.png> <mascara.png> <saida.mp4>
# Ex.: src/reel.sh 308 2 1300 src/build/reel03_overlay.png src/build/reel03_mask.png entregas/.../reel_1080x1920_7s.mp4
set -euo pipefail
ID=$1; SS=$2; CX=$3; OV=$4; MK=$5; OUT=$6
SRC=${MIXKIT_DIR:-/tmp/mixkit}/$ID.mp4
mkdir -p "$(dirname "$SRC")"
if [ ! -f "$SRC" ]; then
  for r in 2160 1080 720; do curl -sf -o "$SRC" "https://assets.mixkit.co/videos/$ID/$ID-$r.mp4" && break; done
fi
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$SRC")
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$SRC")
if [ "$W" -gt "$H" ]; then CROP="crop=$((H*9/16)):$H:$CX:0,"; else CROP=""; fi
ffmpeg -v error -y -ss "$SS" -t 7 -i "$SRC" -i "$OV" -loop 1 -t 7 -i "$MK" -f lavfi -t 7 -i anullsrc=r=48000:cl=stereo \
  -filter_complex "[0:v]${CROP}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,split[a][b];[b]gblur=sigma=26,format=yuva420p[bl];[2:v]scale=1080:1920,format=gray,fps=30[m];[bl][m]alphamerge[blm];[a][blm]overlay=0:0[g];[g][1:v]overlay=0:0:format=auto,format=yuv420p[o]" \
  -map "[o]" -map 3:a -c:v libx264 -profile:v high -preset slow -crf 18 -r 30 -c:a aac -b:a 128k -t 7 -movflags +faststart "$OUT"
echo "ok $OUT"
