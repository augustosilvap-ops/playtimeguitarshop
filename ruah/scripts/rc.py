from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
SP='/tmp/claude-0/-home-claude/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/scratchpad/'
W,H=1080,1350; BONE=(238,234,225); MUT=(160,154,145); BG=(11,11,12)
def F(n,s): return ImageFont.truetype(SP+'ttf/'+n+'.ttf',int(s))
def tracked(d,cx,y,t,f,fill,tr):
    ws=[d.textlength(ch,font=f) for ch in t]; tw=sum(ws)+tr*(len(t)-1); x=cx-tw/2
    for ch,w in zip(t,ws): d.text((x,y),ch,font=f,fill=fill,anchor='ls'); x+=w+tr
def wrap(d,text,font,maxw):
    out,cur=[], ''
    for w in text.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur); cur=w
    out.append(cur); return out
def img(p,**k):
    im=Image.open(p).convert('RGBA'); im=im.crop(im.getbbox())
    if 'h' in k: return im.resize((int(im.width*k['h']/im.height),k['h']),Image.LANCZOS)
    return im.resize((k['w'],int(im.height*k['w']/im.width)),Image.LANCZOS)
LOGO=SP+'kit/marca/logo-bone.png'; SYM=SP+'kit/marca/simbolo-bone.png'
def bg_dark(seed):
    y,x=np.mgrid[0:H,0:W]; r=np.hypot((x-W/2)/W,(y-H*.45)/W)
    a=np.full((H,W,3),BG,float)+(np.clip(1-r/0.7,0,1)**2*14)[...,None]+np.random.default_rng(seed).normal(0,3.2,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))
def bg_photo(path,cy=0.5,dark=0.30,blur=0):
    im=Image.open(path).convert('RGB'); w,h=im.size; ch=int(w*H/W); y0=int(min(max(cy*h-ch/2,0),h-ch))
    im=im.crop((0,y0,w,y0+ch)).resize((W,H),Image.LANCZOS)
    g=im.convert('L').convert('RGB'); im=Image.blend(im,g,0.5)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur))
    a=np.asarray(im).astype(float)*dark
    y=np.arange(H)[:,None,None]; a=a*(1-0.5*np.clip((y-H*0.35)/(H*0.5),0,1))
    a+=np.random.default_rng(1).normal(0,3,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))
def head(d,n):
    tracked(d,W/2,118,'O QUE VOCÊS VIRAM NO VÍDEO',F('cinzel700',22),MUT,7)
    tracked(d,W/2,1262,f'{n:02d} / 06',F('cinzel700',20),MUT,6)
def quote(c,d,text,y,size=74,maxw=860):
    f=F('cg400i',size); lines=wrap(d,'“'+text+'”',f,maxw); lh=size*1.18
    for i,l in enumerate(lines): d.text((W/2,y+i*lh),l,font=f,fill=BONE,anchor='ms')
    yb=y+(len(lines)-1)*lh
    tracked(d,W/2,yb+58,'RESPOSTA NA CAIXINHA',F('cinzel700',18),MUT,6)
    return yb+58

IR='/usr/share/fonts/opentype/inter/Inter-Regular.otf'; IM='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
_av=Image.open('/mnt/user-data/attachments/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/08109b0b-image.jpg').convert('RGB').crop((368,35,482,149))
def card(c,cx,top,width,answer,k=1.0):
    """caixinha de perguntas do Instagram com a resposta preenchida"""
    q='O que achou da qualidade?'
    d=ImageDraw.Draw(c)
    fq=ImageFont.truetype(IR,int(46*k)); fa=ImageFont.truetype(IM,int(40*k))
    pad=int(44*k); inner=width-2*pad
    qlines=wrap(d,q,fq,inner); alines=wrap(d,answer,fa,inner-int(60*k))
    av=int(118*k); qh=len(qlines)*int(56*k); ah=len(alines)*int(52*k)+int(56*k)
    h=int(av*0.55)+int(30*k)+qh+int(34*k)+ah+pad
    x0=int(cx-width/2); y0=int(top)
    sh=Image.new('RGBA',c.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle([x0,y0+8,x0+width,y0+h+8],radius=int(44*k),fill=(0,0,0,120))
    sh=sh.filter(ImageFilter.GaussianBlur(18)); c.paste(sh,(0,0),sh)
    d=ImageDraw.Draw(c)
    d.rounded_rectangle([x0,y0,x0+width,y0+h],radius=int(44*k),fill=(255,255,255))
    # avatar
    a=_av.resize((av,av),Image.LANCZOS); m=Image.new('L',(av,av),0); ImageDraw.Draw(m).ellipse([0,0,av-1,av-1],fill=255)
    ring=int(6*k); d.ellipse([cx-av/2-ring,y0-av/2-ring,cx+av/2+ring,y0+av/2+ring],fill=(255,255,255))
    c.paste(a,(int(cx-av/2),int(y0-av/2)),m)
    y=y0+int(av*0.55)+int(30*k)
    for l in qlines: d.text((cx,y),l,font=fq,fill=(0,0,0),anchor='mt'); y+=int(56*k)
    y+=int(34*k-10*k)
    d.rounded_rectangle([x0+pad,y,x0+width-pad,y+ah],radius=int(26*k),fill=(239,239,239))
    yy=y+int(28*k)
    for l in alines: d.text((cx,yy),l,font=fa,fill=(38,38,38),anchor='mt'); yy+=int(52*k)
    return y0+h
def arrow(d,label=True):
    x1,y=W-90,1252; d.line([(x1-70,y-8),(x1,y-8)],fill=BONE,width=3); d.line([(x1-16,y-22),(x1,y-8),(x1-16,y+6)],fill=BONE,width=3,joint='curve')
    if label: tracked(d,x1-150,y,'ARRASTE',F('cinzel700',18),MUT,5)
out=[]
# 1 capa
c=bg_dark(3); d=ImageDraw.Draw(c)
s=img(SYM,h=1150); s.putalpha(s.split()[3].point(lambda v:int(v*0.06))); c.paste(s,((W-s.width)//2,110),s)
l=img(LOGO,w=230); c.paste(l,((W-l.width)//2,170),l)
tracked(d,W/2,560,'MOSTRAMOS',F('cinzel900',92),BONE,10)
tracked(d,W/2,670,'DE PERTO.',F('cinzel900',92),BONE,10)
d.line([(W/2-60,730),(W/2+60,730)],fill=MUT,width=2)
d.text((W/2,820),'Vocês responderam.',font=F('cg400i',78),fill=BONE,anchor='ms')
for i,t in enumerate(['Perguntamos nos stories o que vocês','acharam da camiseta pelo vídeo de detalhes.']):
    d.text((W/2,930+i*50),t,font=F('cg300i',38),fill=MUT,anchor='ms')
tracked(d,W/2,1262,'01 / 06',F('cinzel700',20),MUT,6); arrow(d)
out.append(c)
# 2-5: uma resposta por slide
for n,(bgp,cy,ans) in enumerate([
    ('video/anat/last_04.png',0.42,'Cara um absurdo de linda, logo garanto as minhas'),
    ('video/anat/last_08.png',0.45,'Incrível!! Meu pastor sempre fazendo tudo com excelência'),
    ('video/anat/last_05.png',0.40,'Absurdoo pastor tá muito massa'),
    ('video/anat/last_09.png',0.55,'Sensacional!')],start=2):
    c=bg_photo(SP+bgp,cy,0.36); d=ImageDraw.Draw(c); head(d,n)
    card(c,W/2,560,820,ans); arrow(ImageDraw.Draw(c))
    out.append(c)
# 5 CTA
c=bg_dark(11); d=ImageDraw.Draw(c); s=img(SYM,h=1150); s.putalpha(s.split()[3].point(lambda v:int(v*0.06))); c.paste(s,((W-s.width)//2,110),s)
d.text((W/2,520),'Ver no vídeo é uma coisa.',font=F('cg400i',76),fill=BONE,anchor='ms')
tracked(d,W/2,650,'VESTIR É OUTRA.',F('cinzel900',84),BONE,8)
d.line([(W/2-60,712),(W/2+60,712)],fill=MUT,width=2)
tracked(d,W/2,800,'COLEÇÃO 001',F('cinzel700',30),MUT,10)
tracked(d,W/2,1060,'USERUAH.COM',F('cinzel700',40),BONE,12)
tracked(d,W/2,1112,'LINK NA BIO',F('cinzel700',22),MUT,8)
l=img(LOGO,w=200); c.paste(l,((W-l.width)//2,140),l)
tracked(d,W/2,1262,'06 / 06',F('cinzel700',20),MUT,6)
out.append(c)
for i,c in enumerate(out): c.save(f'RUAH_reacoes_{i+1:02d}.jpg',quality=94)
S=Image.new('RGB',(6*216,270)); [S.paste(c.resize((216,270)),(i*216,0)) for i,c in enumerate(out)]; S.save('prev.jpg')
