from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
SP='/tmp/claude-0/-home-claude/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/scratchpad/'
W,H=1080,1920; BONE=(238,234,225); MUT=(160,154,145); BG=(11,11,12)
IR='/usr/share/fonts/opentype/inter/Inter-Regular.otf'; IM='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
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
_av=Image.open('/mnt/user-data/attachments/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/08109b0b-image.jpg').convert('RGB').crop((368,35,482,149))
def card_layer(answer,width=860,k=1.05):
    """caixinha de perguntas (RGBA recortada)"""
    L=Image.new('RGBA',(W,1000),(0,0,0,0)); d=ImageDraw.Draw(L); q='O que achou da qualidade?'
    fq=ImageFont.truetype(IR,int(46*k)); fa=ImageFont.truetype(IM,int(40*k)); pad=int(44*k); inner=width-2*pad
    qlines=wrap(d,q,fq,inner); alines=wrap(d,answer,fa,inner-int(60*k))
    av=int(118*k); qh=len(qlines)*int(56*k); ah=len(alines)*int(52*k)+int(56*k)
    h=int(av*0.55)+int(30*k)+qh+int(24*k)+ah+pad
    cx=W/2; x0=int(cx-width/2); y0=int(av/2)+30
    sh=Image.new('RGBA',L.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([x0,y0+8,x0+width,y0+h+8],radius=int(44*k),fill=(0,0,0,130))
    L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18))); d=ImageDraw.Draw(L)
    d.rounded_rectangle([x0,y0,x0+width,y0+h],radius=int(44*k),fill=(255,255,255,255))
    a=_av.resize((av,av),Image.LANCZOS); m=Image.new('L',(av,av),0); ImageDraw.Draw(m).ellipse([0,0,av-1,av-1],fill=255)
    ring=int(6*k); d.ellipse([cx-av/2-ring,y0-av/2-ring,cx+av/2+ring,y0+av/2+ring],fill=(255,255,255,255))
    L.paste(a,(int(cx-av/2),int(y0-av/2)),m)
    y=y0+int(av*0.55)+int(30*k)
    for l in qlines: d.text((cx,y),l,font=fq,fill=(0,0,0,255),anchor='mt'); y+=int(56*k)
    y+=int(24*k)
    d.rounded_rectangle([x0+pad,y,x0+width-pad,y+ah],radius=int(26*k),fill=(239,239,239,255))
    yy=y+int(28*k)
    for l in alines: d.text((cx,yy),l,font=fa,fill=(38,38,38,255),anchor='mt'); yy+=int(52*k)
    return L.crop(L.getbbox())
def bg_dark(seed):
    y,x=np.mgrid[0:H,0:W]; r=np.hypot((x-W/2)/W,(y-H*.45)/W)
    a=np.full((H,W,3),BG,float)+(np.clip(1-r/0.7,0,1)**2*14)[...,None]+np.random.default_rng(seed).normal(0,3.2,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))
def darken(im,dark=0.4,seed=1):
    g=im.convert('L').convert('RGB'); im=Image.blend(im,g,0.5)
    a=np.asarray(im).astype(float)*dark+np.random.default_rng(seed).normal(0,3,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))
ANS=['Cara um absurdo de linda, logo garanto as minhas','Incrível!! Meu pastor sempre fazendo tudo com excelência','Absurdoo pastor tá muito massa','Sensacional!']
