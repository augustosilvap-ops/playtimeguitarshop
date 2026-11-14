#!/usr/bin/env bash
# Reel de 7 s com motion sobre filmagem real: escurecimento entra, selo desliza, título entra em duas partes,
# botão "Leia a legenda" sobe e pulsa, linha de progresso no rodapé. Texto fica parado depois de entrar.
# Uso: src/reel_motion.sh <id_mixkit> <inicio_s> <crop_x> <prefixo build/mXX> <saida.mp4>
set -euo pipefail
ID=$1; SS=$2; CX=$3; P=$4; OUT=$5
SRC=${MIXKIT_DIR:-/tmp/mixkit}/$ID.mp4
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$SRC")
H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$SRC")
if [ "$W" -gt "$H" ]; then CROP="crop=$((H*9/16)):$H:$CX:0,"; else CROP=""; fi
L="-loop 1 -t 7 -framerate 30 -i"
ffmpeg -v error -y -ss "$SS" -t 7 -i "$SRC" $L ${P}_scrim.png $L ${P}_chip.png $L ${P}_t1.png $L ${P}_t2.png $L ${P}_pill.png \
  -f lavfi -t 7 -i "color=c=0x5B8CFF:s=912x6:r=30" -f lavfi -t 7 -i anullsrc=r=48000:cl=stereo -filter_complex "
[0:v]${CROP}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v];
[1:v]format=rgba,fade=in:st=0:d=0.5:alpha=1[s];
[2:v]format=rgba,fade=in:st=0.2:d=0.4:alpha=1[c];
[3:v]format=rgba,fade=in:st=0.35:d=0.5:alpha=1[t1];
[4:v]format=rgba,fade=in:st=0.75:d=0.5:alpha=1[t2];
[5:v]format=rgba,fade=in:st=1.3:d=0.4:alpha=1[p];
[6:v]format=rgba[bar];
[v][s]overlay=0:0[a];
[a][c]overlay=x='if(lt(t,0.2),-40,if(lt(t,0.6),-40+40*(t-0.2)/0.4,0))':y=0[b];
[b][t1]overlay=x=0:y='if(lt(t,0.35),60,if(lt(t,0.85),60*pow(1-(t-0.35)/0.5,2),0))'[d];
[d][t2]overlay=x=0:y='if(lt(t,0.75),60,if(lt(t,1.25),60*pow(1-(t-0.75)/0.5,2),0))'[e];
[e][p]overlay=x=0:y='if(lt(t,1.3),40,if(lt(t,1.7),40*pow(1-(t-1.3)/0.4,2),-6*abs(sin(PI*(t-1.7)/1.2))))'[f];
[f][bar]overlay=x='84-912+912*t/7':y=1830:shortest=1,format=yuv420p[o]" \
  -map "[o]" -map 7:a -c:v libx264 -profile:v high -preset slow -crf 18 -r 30 -c:a aac -b:a 128k -t 7 -movflags +faststart "$OUT"
echo "ok $OUT"
