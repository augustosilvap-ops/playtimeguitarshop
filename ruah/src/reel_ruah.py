"""Reel RUAH "Fora das quatro paredes" — 10 s, 4 cenas + assinatura, sobre filmagem real (Mixkit Free License).
Uso: MIXKIT_DIR=/caminho python3 reel_ruah.py   (rodar dentro de ruah/src)"""
import subprocess, os
DUR = 10.0
OUT = '../entregas/2026-11-16/R02_reel_quatro_paredes'
MIX = os.environ.get('MIXKIT_DIR', '/tmp/mixkit')
BEATS = [('Por que aquilo', 'em que você acredita'), ('precisa ficar', 'entre quatro paredes?'),
         ('Somos uma geração', 'que não se esconde.'), ('Que não tem vergonha de', 'carregar o Espírito.')]
T = [(0, 2.3), (2.3, 4.6), (4.6, 6.6), (6.6, 8.4)]
END = 8.4
css = ('<style>.art{height:1920px}.bt{position:absolute;left:84px;right:84px;top:760px;color:var(--bone)}'
       '.bt .it{font-size:64px;color:var(--bone2)}.bt .cz{font-size:76px;margin-top:14px}'
       '.sc{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,8,8,.55),rgba(8,8,8,.72) 45%,rgba(8,8,8,.5) 80%,rgba(8,8,8,.3))}</style>')
h = ['<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="ruah.css">' + css + '</head><body>']
B = '../ruah/src/build/'
h.append(f'<section class="art" data-out="{B}scrim.png" data-transparent="1"><div class="sc"></div></section>')
h.append(f'<section class="art" data-out="{B}top.png" data-transparent="1"><img src="../marca/logos/logo-bone.png" style="position:absolute;left:84px;top:260px;height:48px">'
         '<div class="lab" style="position:absolute;right:84px;top:276px;color:var(--taupe)">@ruahwear_</div></section>')
for i, (a, b) in enumerate(BEATS):
    h.append(f'<section class="art" data-out="{B}b{i}.png" data-transparent="1"><div class="bt"><p class="it">{a}</p><p class="cz">{b}</p></div></section>')
end = ('<div style="position:absolute;inset:0;background:var(--preto);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--bone)">'
       '<img src="../marca/logos/simbolo-bone.png" style="height:120px">'
       '<p class="cz" style="font-size:72px;margin-top:60px">We carry<br>the spirit.</p>'
       '<p class="it" style="font-size:46px;margin-top:40px;color:var(--bone2)">Coleção 001 disponível</p>'
       '<p class="lab" style="margin-top:70px;color:var(--taupe)">useruah.com · link na bio</p></div>')
h.append(f'<section class="art" data-out="{B}end.png">{end}</section>')
# capa (frame estático do smoke + cena 1)
h.append(f'<section class="art" data-out="../ruah/entregas/2026-11-16/R02_reel_quatro_paredes/capa_1080x1920.png" style="background:url(\'build/capa_bg.jpg\') center/cover">'
         '<div class="sc"></div><img src="../marca/logos/logo-bone.png" style="position:absolute;left:84px;top:260px;height:48px">'
         '<div class="bt"><p class="it">Por que aquilo em que você acredita</p><p class="cz">precisa ficar entre quatro paredes?</p></div></section>')
h.append('</body></html>')
os.makedirs('build', exist_ok=True); os.makedirs(OUT, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '2', '-i', f'{MIX}/1960.mp4', '-frames:v', '1', '-vf', 'crop=1215:2160:1312:0,scale=1080:1920', 'build/capa_bg.jpg'], check=True)
open('reel_layers.html', 'w').write('\n'.join(h))
subprocess.run(['node', 'render.js', '../../ruah/src/reel_layers.html'], cwd='../../augusto/src', check=True, stdout=subprocess.DEVNULL)

ins = ['-ss', '1', '-t', '4.8', '-i', f'{MIX}/1960.mp4', '-ss', '2', '-t', '4.2', '-i', f'{MIX}/40746.mp4']
L = ['scrim', 'top', 'b0', 'b1', 'b2', 'b3', 'end']
for x in L: ins += ['-loop', '1', '-t', str(DUR), '-framerate', '30', '-i', f'build/{x}.png']
ins += ['-f', 'lavfi', '-t', str(DUR), '-i', 'color=c=0xB9A88C:s=912x4:r=30', '-t', str(DUR), '-i', '../videos/RUAH_trilha_lancamento.mp3']
f = ['[0:v]crop=1215:2160:1312:0,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setpts=PTS-STARTPTS[a]',
     '[1:v]scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setpts=PTS-STARTPTS[b]',
     '[a][b]xfade=transition=fade:duration=0.5:offset=4.3,tpad=stop_mode=clone:stop_duration=2[v0]',
     '[2:v]format=rgba[sc]', '[v0][sc]overlay[v1]',
     '[3:v]format=rgba,fade=in:st=0:d=0.5:alpha=1[tp]', '[v1][tp]overlay[v2]']
prev = 'v2'
for i, (s, e) in enumerate(T):
    f.append(f'[{4+i}:v]format=rgba,fade=in:st={s}:d=0.4:alpha=1,fade=out:st={e-0.3}:d=0.3:alpha=1[b{i}]')
    f.append(f"[{prev}][b{i}]overlay=x=0:y='if(lt(t,{s}),40,if(lt(t,{s+0.5}),40*pow(1-(t-{s})/0.5,2),0))'[v{3+i}]"); prev = f'v{3+i}'
f.append(f'[8:v]format=rgba,fade=in:st={END}:d=0.5:alpha=1[en]'); f.append(f'[{prev}][en]overlay[v8]')
f.append(f"[9:v]format=rgba[bar];[v8][bar]overlay=x='84-912+912*t/{DUR}':y=1830:shortest=1,format=yuv420p[o]")
f.append(f'[10:a]afade=in:st=0:d=0.6,afade=out:st={DUR-1.2}:d=1.2,aresample=48000[au]')
cmd = ['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(f), '-map', '[o]', '-map', '[au]', '-c:v', 'libx264', '-profile:v', 'high',
       '-preset', 'slow', '-crf', '18', '-r', '30', '-c:a', 'aac', '-b:a', '128k', '-t', str(DUR), '-movflags', '+faststart', f'{OUT}/reel_1080x1920_10s.mp4']
subprocess.run(cmd, check=True); print('ok', OUT)
