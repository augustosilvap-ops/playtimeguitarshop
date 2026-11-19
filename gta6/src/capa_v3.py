"""Capas v3: recorte BiRefNet em alta + fundo = a própria cena desfocada (luz igual, sem cara de colado).
Texto metálico atrás do personagem, faixa amarela na frente."""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from capa_v2 import chrome_text, yellow_bar, F, P
OUT='/home/user/playtimeguitarshop/gta6/entregas/capas_v3/'; os.makedirs(OUT,exist_ok=True)
CACHE='/home/user/playtimeguitarshop/gta6/src/capas_v3/'; os.makedirs(CACHE,exist_ok=True)
W,H=1080,1920
sess=None
def mask(path):
    """Máscara alfa (L) no tamanho original, só com as figuras principais (remove sobras)."""
    global sess
    c=CACHE+os.path.basename(path).replace('.jpg','_m.png')
    if os.path.exists(c): return Image.open(c)
    from rembg import remove, new_session
    if sess is None: sess=new_session('birefnet-portrait')
    im=Image.open(path).convert('RGB'); sm=im.copy(); sm.thumbnail((1920,1920),Image.LANCZOS)
    m=remove(sm,session=sess,only_mask=True).resize(im.size,Image.LANCZOS)
    a=np.array(m); lab,n=ndimage.label(a>128)
    if n>1:
        sizes=ndimage.sum(np.ones_like(a),lab,range(1,n+1)); keep=[i+1 for i,s in enumerate(sizes) if s>=sizes.max()*.15]
        a=np.where(np.isin(lab,keep)|(a<=128)&(ndimage.binary_dilation(np.isin(lab,keep),iterations=6)),a,0).astype(np.uint8)
    m=Image.fromarray(a); m.save(c); return m
def make(n,src,top,bar,cx=.5,ty=200,tsize=300,bsize=100,by=1240,tag="GTA 6",head=.86,minh=1350,**_):
    im=Image.open(P+src).convert('RGB'); m=mask(P+src); IW,IH=im.size
    t=chrome_text(top,tsize)
    if t.width>W-20: t=t.resize((W-20,int(t.height*(W-20)/t.width)),Image.LANCZOS)
    top_y=ty+int(t.height*head)                            # onde a cabeça deve ficar na capa
    if np.array(m)[:6].max()>128:                          # figura cortada no topo da foto: suaviza a borda
        ma=np.array(m).astype(float); r=IH//9; ma[:r]*=np.linspace(0,1,r)[:,None]; m=Image.fromarray(ma.astype(np.uint8))
    a=np.array(m)>128; ys,xs=np.nonzero(a); bt=ys.min()
    hx=xs[ys<bt+(ys.max()-bt)*.25].mean()                  # centro da parte de cima (cabeça)
    Hs=int(max(minh,min(IH*1.38,(IH-bt)/(1-top_y/H))))     # janela 9:16 da própria foto
    pad=max(0,Hs-IH+0)                                     # se a janela passa do topo, estende a foto para cima
    if pad:
        strip=im.crop((0,0,IW,max(8,IH//12))).resize((IW,pad),Image.BICUBIC)
        nim=Image.new('RGB',(IW,IH+pad)); nim.paste(strip,(0,0)); nim.paste(im,(0,pad)); im=nim
        nm=Image.new('L',(IW,IH+pad),0); nm.paste(m,(0,pad)); m=nm; bt+=pad; IH+=pad
    Ws=int(Hs*W/H); wy=int(min(IH-Hs,max(0,bt-top_y*Hs/H)))
    wx=int(min(IW-Ws,max(0,hx-Ws*cx)))
    box=(wx,wy,wx+Ws,wy+Hs)
    fg=im.crop(box).resize((W,H),Image.LANCZOS); al=m.crop(box).resize((W,H),Image.LANCZOS)
    fg=ImageEnhance.Contrast(fg).enhance(1.08); fg=fg.filter(ImageFilter.UnsharpMask(2,60,2))
    bg=im.crop(box).resize((W,H),Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
    bg=ImageEnhance.Brightness(bg).enhance(.5); bg=ImageEnhance.Color(bg).enhance(1.15)
    c=bg.convert('RGBA')
    v=Image.new('RGBA',(W,H),(0,0,0,0)); vd=ImageDraw.Draw(v)
    for y in range(H): vd.line((0,y,W,y),fill=(5,3,12,int(170*max(0,(y-H*.6)/(H*.4)))))
    c.alpha_composite(v)
    c.alpha_composite(t,((W-t.width)//2,ty))               # texto atrás
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.paste((0,0,0,190),(0,0),al); sh=sh.filter(ImageFilter.GaussianBlur(22))
    c.alpha_composite(sh,(0,12))
    p=fg.convert('RGBA'); p.putalpha(al); c.alpha_composite(p)   # personagem
    b=yellow_bar(bar,bsize)
    if b.width>W-40: b=b.resize((W-40,int(b.height*(W-40)/b.width)),Image.LANCZOS)
    c.alpha_composite(b,((W-b.width)//2,by))               # faixa na frente
    f=ImageFont.truetype(F+'ARN.ttf',54); d=ImageDraw.Draw(c); tw=d.textlength(tag,font=f)
    d.rounded_rectangle((40,70,40+tw+44,154),18,fill=(225,40,150,255)); d.text((62,80),tag,font=f,fill=(255,255,255,255))
    c.convert('RGB').save(OUT+f'capa_{n}.jpg',quality=95,subsampling=0)
if __name__=='__main__':
    jobs=json.load(open(sys.argv[1])); only=sys.argv[2:]
    for j in jobs:
        if not only or j['n'] in only: make(**j); print(j['n'],flush=True)
