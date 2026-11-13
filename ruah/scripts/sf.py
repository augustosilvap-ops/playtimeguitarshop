from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
SP='/tmp/claude-0/-home-claude/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/scratchpad/'
BONE=(238,234,225); MUT=(150,145,137); DIM=(110,106,100); BG=(11,11,12)
def F(n,s): return ImageFont.truetype(SP+'ttf/'+n+'.ttf',int(s))
def tracked(d,cx,y,t,f,fill,tr):
    ws=[d.textlength(ch,font=f) for ch in t]; tw=sum(ws)+tr*(len(t)-1); x=cx-tw/2
    for ch,w in zip(t,ws): d.text((x,y),ch,font=f,fill=fill,anchor='ls'); x+=w+tr
def img(p,**k):
    im=Image.open(p).convert('RGBA'); im=im.crop(im.getbbox())
    if 'h' in k: return im.resize((int(im.width*k['h']/im.height),k['h']),Image.LANCZOS)
    return im.resize((k['w'],int(im.height*k['w']/im.width)),Image.LANCZOS)
def story(n):
    W,H=1080,1920
    y,x=np.mgrid[0:H,0:W]; r=np.hypot((x-W/2)/W,(y-H*.44)/W)
    a=np.full((H,W,3),BG,float)+(np.clip(1-r/0.65,0,1)**2*16)[...,None]+np.random.default_rng(n).normal(0,3.5,(H,W,1))
    c=Image.fromarray(np.clip(a,0,255).astype('uint8')); d=ImageDraw.Draw(c)
    s=img(SP+'kit/marca/simbolo-bone.png',h=1250); s.putalpha(s.split()[3].point(lambda v:int(v*0.07))); c.paste(s,((W-s.width)//2,330),s)
    l=img(SP+'kit/marca/logo-bone.png',w=240); c.paste(l,((W-l.width)//2,260),l)
    tracked(d,W/2,420,'FOUNDERS · PRIMEIRA GERAÇÃO',F('cinzel700',24),MUT,7)
    tracked(d,W/2,640,'FOUNDER',F('cinzel700',44),MUT,24)
    d.text((W/2,1010),f'Nº {n:02d}',font=F('corm700',360),fill=BONE,anchor='ms',features=['lnum'])
    d.line([(W/2-70,1080),(W/2+70,1080)],fill=MUT,width=2)
    ORD={1:'primeiro',2:'segundo',3:'terceiro',4:'quarto',5:'quinto',6:'sexto',7:'sétimo',8:'oitavo',9:'nono',10:'décimo'}; first=f'O {ORD[n]} Founder da RUAH.' if n in ORD else f'O {n}º Founder da RUAH.'
    d.text((W/2,1170),first,font=F('cg300i',58),fill=BONE,anchor='ms')
    d.text((W/2,1240),'Obrigado por acreditar desde o primeiro dia.',font=F('cg300i',40),fill=MUT,anchor='ms')
    # espaço reservado para a marcação (@)
    x0,x1,y0,y1=W/2-300,W/2+300,1300,1410
    d.rounded_rectangle([x0,y0,x1,y1],radius=55,outline=(70,68,64),width=2)
    left=30-n
    tracked(d,W/2,1560,f'RESTAM {left} VAGAS',F('cinzel700',40),BONE,12)
    tracked(d,W/2,1615,'COLEÇÃO 001 DISPONÍVEL · USERUAH.COM',F('cinzel700',22),DIM,6)
    c.save(SP+f'stories_founders/RUAH_stories_Founder_{n:02d}.jpg',quality=93)
for n in map(int,sys.argv[1:]): story(n)
