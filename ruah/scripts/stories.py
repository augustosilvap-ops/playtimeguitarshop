import sys; sys.path.insert(0,'.')
from common import *
out=[]
# 1 abertura
c=bg_dark(3); d=ImageDraw.Draw(c)
s=img(SYM,h=1500); s.putalpha(s.split()[3].point(lambda v:int(v*0.06))); c.paste(s,((W-s.width)//2,230),s)
l=img(LOGO,w=230); c.paste(l,((W-l.width)//2,300),l)
tracked(d,W/2,820,'MOSTRAMOS',F('cinzel900',96),BONE,10); tracked(d,W/2,935,'DE PERTO.',F('cinzel900',96),BONE,10)
d.line([(W/2-60,995),(W/2+60,995)],fill=MUT,width=2)
d.text((W/2,1090),'Vocês responderam.',font=F('cg400i',80),fill=BONE,anchor='ms')
for i,t in enumerate(['Perguntamos o que vocês acharam','da camiseta pelo vídeo de detalhes.']): d.text((W/2,1200+i*52),t,font=F('cg300i',40),fill=MUT,anchor='ms')
tracked(d,W/2,1560,'TOQUE PARA VER  ›',F('cinzel700',22),MUT,6)
out.append(c)
# 2 e 3: duas respostas por story, sobre a filmagem
bgs=[SP+'video/anat/last_04.png',SP+'video/anat/last_08.png']
for k in range(2):
    c=darken(Image.open(bgs[k]).convert('RGB').resize((W,H)),0.38,k)
    d=ImageDraw.Draw(c); tracked(d,W/2,330,'O QUE VOCÊS VIRAM NO VÍDEO',F('cinzel700',24),MUT,7)
    y=470
    for a in ANS[2*k:2*k+2]:
        L=card_layer(a); c.paste(L,((W-L.width)//2,y),L); y+=L.height+90
    out.append(c)
# 4 CTA com espaço para a figurinha de link
c=bg_dark(11); d=ImageDraw.Draw(c)
s=img(SYM,h=1500); s.putalpha(s.split()[3].point(lambda v:int(v*0.06))); c.paste(s,((W-s.width)//2,230),s)
l=img(LOGO,w=230); c.paste(l,((W-l.width)//2,300),l)
d.text((W/2,760),'Ver no vídeo é uma coisa.',font=F('cg400i',78),fill=BONE,anchor='ms')
tracked(d,W/2,890,'VESTIR É OUTRA.',F('cinzel900',88),BONE,8)
d.line([(W/2-60,950),(W/2+60,950)],fill=MUT,width=2)
tracked(d,W/2,1040,'COLEÇÃO 001',F('cinzel700',30),MUT,10)
d.rounded_rectangle([W/2-280,1180,W/2+280,1290],radius=55,outline=(80,78,74),width=2)
tracked(d,W/2,1420,'USERUAH.COM',F('cinzel700',36),BONE,12)
out.append(c)
for i,c in enumerate(out): c.save(f'st/RUAH_story_reacoes_{i+1}.jpg',quality=93)
S=Image.new('RGB',(4*276,480),'white'); [S.paste(c.resize((270,480)),(i*276,0)) for i,c in enumerate(out)]; S.save('st/previa_stories.jpg')
