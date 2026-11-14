"""Reels-roteiro (motion): cenas de pergunta que levam ao ponto final, sobre filmagem real.
Uso: python3 reel_story.py   (gera as camadas em pecas/reel_story_layers.html, renderiza e monta os MP4)"""
import subprocess, os, json
DUR=10.0
REELS={
 '03':dict(src=308,ss=1,cx=1300,out='../entregas/2026-11-16/03_reel_precificar-leigo/reel_1080x1920_10s.mp4',beats=[
   ('Você quer','vender online?'),('Mas não sabe','precificar seu produto…'),('…e está tomando','prejuízo sem perceber?'),('Vou te ensinar a precificar','mesmo sendo leigo.')]),
 '06':dict(src=4938,ss=0,cx=1500,out='../entregas/2026-11-17/06_reel_garimpo/reel_1080x1920_10s.mp4',beats=[
   ('Você vive procurando','produto pra vender?'),('Compra no','achismo…'),('…e o estoque','fica parado?'),('Use a IA para achar produtos','com potencial.')]),
 '09':dict(src=42137,ss=1,cx=0,out='../entregas/2026-11-18/09_reel_desconto/reel_1080x1920_10s.mp4',beats=[
   ('Vai entrar na','Black Friday?'),('Vai dar desconto','em tudo…'),('…sem saber o seu','preço mínimo?'),('Faça promoção sem','destruir sua margem.')]),
}
T=[(0,2.3),(2.3,4.6),(4.6,6.9),(6.9,DUR)]
h=['<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="../v2.css"><style>.bt{position:absolute;left:84px;right:84px;top:640px;font-weight:700;letter-spacing:-.05em;line-height:1;color:#fff;font-size:118px}.bt span{color:var(--blue2)}.fin{font-size:104px}.sc{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,9,14,.55),rgba(8,9,14,.78) 40%,rgba(8,9,14,.55) 75%,rgba(8,9,14,.2))}</style></head><body>']
for k,r in REELS.items():
    h.append(f'<section class="art s" data-out="src/build/s{k}_scrim.png" data-transparent="1" style="height:1920px"><div class="sc"></div></section>')
    h.append(f'<section class="art s" data-out="src/build/s{k}_chip.png" data-transparent="1" style="height:1920px;color:#fff"><div class="chip" style="top:300px"><i>↗</i>@augustosilva.p</div></section>')
    for i,(a,b) in enumerate(r['beats']):
        h.append(f'<section class="art s" data-out="src/build/s{k}_b{i}.png" data-transparent="1" style="height:1920px"><div class="bt{" fin" if i==3 else ""}">{a} <span>{b}</span></div></section>')
    h.append(f'<section class="art s" data-out="src/build/s{k}_pill.png" data-transparent="1" style="height:1920px;color:#fff"><div class="pill" style="position:absolute;left:84px;top:1080px">Leia a legenda ↓</div></section>')
h.append('</body></html>')
open('pecas/reel_story_layers.html','w').write('\n'.join(h))
subprocess.run(['node','render.js','pecas/reel_story_layers.html'],check=True,stdout=subprocess.DEVNULL)
MIX=os.environ.get('MIXKIT_DIR','/tmp/mixkit')
for k,r in REELS.items():
    src=f"{MIX}/{r['src']}.mp4"
    w,hh=map(int,subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',src]).decode().strip().split(','))
    crop=f"crop={hh*9//16}:{hh}:{r['cx']}:0," if w>hh else ''
    ins=['-ss',str(r['ss']),'-t',str(DUR),'-i',src]
    layers=['scrim','chip','b0','b1','b2','b3','pill']
    for L in layers: ins+=['-loop','1','-t',str(DUR),'-framerate','30','-i',f'build/s{k}_{L}.png']
    ins+=['-f','lavfi','-t',str(DUR),'-i','color=c=0x5B8CFF:s=912x6:r=30','-f','lavfi','-t',str(DUR),'-i','anullsrc=r=48000:cl=stereo']
    f=[f'[0:v]{crop}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v0]',
       '[1:v]format=rgba,fade=in:st=0:d=0.4:alpha=1[l1]','[2:v]format=rgba,fade=in:st=0.1:d=0.4:alpha=1[l2]']
    prev='v0';f.append(f'[{prev}][l1]overlay=0:0[v1]');f.append("[v1][l2]overlay=x='if(lt(t,0.1),-40,if(lt(t,0.5),-40+40*(t-0.1)/0.4,0))':y=0[v2]");prev='v2'
    for i,(s,e) in enumerate(T):
        fo='' if i==3 else f',fade=out:st={e-0.25}:d=0.25:alpha=1'
        f.append(f'[{3+i}:v]format=rgba,fade=in:st={s}:d=0.35:alpha=1{fo}[b{i}]')
        f.append(f"[{prev}][b{i}]overlay=x=0:y='if(lt(t,{s}),50,if(lt(t,{s+0.4}),50*pow(1-(t-{s})/0.4,2),0))'[v{3+i}]");prev=f'v{3+i}'
    f.append('[7:v]format=rgba,fade=in:st=7.4:d=0.4:alpha=1[pl]')
    f.append(f"[{prev}][pl]overlay=x=0:y='if(lt(t,7.4),40,if(lt(t,7.8),40*pow(1-(t-7.4)/0.4,2),-6*abs(sin(PI*(t-7.8)/1.1))))'[v8]")
    f.append(f"[8:v]format=rgba[bar];[v8][bar]overlay=x='84-912+912*t/{DUR}':y=1830:shortest=1,format=yuv420p[o]")
    cmd=['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(f),'-map','[o]','-map','9:a','-c:v','libx264','-profile:v','high','-preset','slow','-crf','18','-r','30','-c:a','aac','-b:a','128k','-t',str(DUR),'-movflags','+faststart',r['out']]
    subprocess.run(cmd,check=True);print('ok',r['out'])
