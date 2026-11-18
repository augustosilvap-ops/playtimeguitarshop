import numpy as np, math
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='/root/.claude/skills/synced/97738154-5bc6-4990-9da4-4914b5a7c854_99862642-420e-426c-b741-75a800036523/canvas-design/canvas-fonts/'
INK=(10,10,12); BONE=(236,230,218); HEAT=(255,59,48); DIM=(236,230,218)
def font(n,s): return ImageFont.truetype(F+n,s)
def terrain(w,h,seed=7):
    rng=np.random.default_rng(seed); z=sum(gaussian_filter(rng.standard_normal((h,w)),s)*s**1.1 for s in (60,30,14))
    yy,xx=np.mgrid[0:h,0:w]/max(w,h)
    # península ao sul (sutil) + costa
    pen=np.exp(-((xx-.66*w/max(w,h))**2)/.012)*np.clip((yy*max(w,h)/h),0,1)
    z=z/np.abs(z).max()+1.6*pen-.4; return z
def contours(w,h,ss,seed,levels=26,alpha=.16,lw=1.1):
    z=terrain(w//4,h//4,seed)
    fig=plt.figure(figsize=(w*ss/100,h*ss/100),dpi=100); ax=fig.add_axes([0,0,1,1]); ax.axis('off')
    ax.contour(z,levels=levels,colors=[tuple(c/255 for c in BONE)],linewidths=lw*ss,alpha=alpha); ax.set_xlim(0,z.shape[1]-1); ax.set_ylim(z.shape[0]-1,0)
    fig.patch.set_alpha(0); fig.canvas.draw(); im=Image.frombuffer('RGBA',fig.canvas.get_width_height(),fig.canvas.buffer_rgba()).copy(); plt.close(fig); return im
def ctext(d,xy,t,f,fill,anchor='mm',sp=0):
    if sp: # letter-spacing manual
        ws=[d.textlength(c,font=f) for c in t]; W=sum(ws)+sp*(len(t)-1); x=xy[0]-(W/2 if anchor[0]=='m' else 0 if anchor[0]=='l' else W)
        for c,wc in zip(t,ws): d.text((x,xy[1]),c,font=f,fill=fill,anchor='l'+anchor[1]); x+=wc+sp
    else: d.text(xy,t,font=f,fill=fill,anchor=anchor)
def rings(d,cx,cy,rs,col,w):
    for r in rs: d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=col,width=w)
def ticks(d,cx,cy,r,n,l,col,w,major=6):
    for k in range(n):
        a=2*math.pi*k/n; L=l*(2.2 if k%major==0 else 1)
        d.line((cx+math.cos(a)*r,cy+math.sin(a)*r,cx+math.cos(a)*(r-L),cy+math.sin(a)*(r-L)),fill=col,width=w)
def blip(img,x,y,r,ss):
    g=Image.new('RGBA',img.size,(0,0,0,0)); gd=ImageDraw.Draw(g)
    for k,a in ((6,40),(3.2,70),(1.8,120)): gd.ellipse((x-r*k,y-r*k,x+r*k,y+r*k),fill=HEAT+(a,))
    g=g.filter(ImageFilter.GaussianBlur(r*1.6)); img.alpha_composite(g); d=ImageDraw.Draw(img)
    d.ellipse((x-r,y-r,x+r,y+r),fill=HEAT); d.ellipse((x-r*2.6,y-r*2.6,x+r*2.6,y+r*2.6),outline=HEAT+(200,),width=max(1,ss*2))

def perfil(S=800,ss=3):
    W=S*ss; img=Image.new('RGBA',(W,W),INK+(255,)); c=W/2
    img.alpha_composite(contours(S,S,ss,11,levels=18,alpha=.14).resize((W,W)))
    d=ImageDraw.Draw(img,'RGBA')
    rings(d,c,c,[W*.47,W*.405],BONE+(46,),ss*2); ticks(d,c,c,W*.47,72,W*.012,BONE+(110,),ss*2,major=6)
    d.line((c,W*.03,c,W*.12),fill=BONE+(90,),width=ss*2); d.line((c,W*.88,c,W*.97),fill=BONE+(90,),width=ss*2)
    d.line((W*.03,c,W*.12,c),fill=BONE+(90,),width=ss*2); d.line((W*.88,c,W*.97,c),fill=BONE+(90,),width=ss*2)
    f=font('Boldonse-Regular.ttf',int(W*.255)); ctext(d,(c,c+W*.012),'CI',f,BONE)
    blip(img,c+W*.205,c-W*.175,W*.017,ss)
    fm=font('GeistMono-Regular.ttf',int(W*.026)); ctext(ImageDraw.Draw(img),(c,c+W*.215),'BR',fm,BONE+(170,),sp=W*.02)
    return img.convert('RGB').resize((S,S),Image.LANCZOS)

def banner(Wd=2560,Ht=1440,ss=2):
    W,H=Wd*ss,Ht*ss; img=Image.new('RGBA',(W,H),INK+(255,))
    img.alpha_composite(contours(Wd,Ht,ss,5,levels=30,alpha=.2).resize((W,H)))
    d=ImageDraw.Draw(img,'RGBA')
    # grade de coordenadas fina
    for x in range(0,W,320*ss): d.line((x,0,x,H),fill=BONE+(7,),width=ss)
    for y in range(0,H,320*ss): d.line((0,y,W,y),fill=BONE+(7,),width=ss)
    fm=font('GeistMono-Regular.ttf',15*ss)
    for i,x in enumerate(range(320*ss,W,320*ss)): d.text((x+6*ss,40*ss),f'{80.64-i*0.16:05.2f}°W'.replace('.',','),font=fm,fill=BONE+(70,))
    for i,y in enumerate(range(320*ss,H,320*ss)): d.text((40*ss,y+6*ss),f'{26.08-i*0.16:05.2f}°N'.replace('.',','),font=fm,fill=BONE+(70,))
    # radar à direita (fora da área segura central)
    cx,cy,R=2210*ss,980*ss,300*ss
    rings(d,cx,cy,[R,R*.75,R*.5,R*.25],BONE+(40,),ss); ticks(d,cx,cy,R,120,7*ss,BONE+(90,),ss,major=10)
    sw=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sw)
    for k in range(40): sd.pieslice((cx-R,cy-R,cx+R,cy+R),-60-k*1.2,-60-(k-1)*1.2,fill=BONE+(int(26*(1-k/40)),))
    img.alpha_composite(sw); d=ImageDraw.Draw(img,'RGBA')
    d.line((cx,cy,cx+math.cos(math.radians(-60))*R,cy+math.sin(math.radians(-60))*R),fill=BONE+(150,),width=ss*2)
    blip(img,cx+R*.42,cy-R*.52,7*ss,ss); blip(img,cx-R*.55,cy+R*.2,4*ss,ss)
    d=ImageDraw.Draw(img,'RGBA')
    # wordmark — área segura 1546x423 centrada (x 507–2053, y 508–932)
    f=font('Boldonse-Regular.ttf',150*ss); mx=W/2
    ctext(d,(mx,700*ss),'CAOS INSANO',f,BONE)
    fl=font('GeistMono-Regular.ttf',26*ss)
    ctext(d,(mx,575*ss),'SINAL AO VIVO  ·  BR',fl,BONE+(150,),sp=7*ss)
    d.line((mx-610*ss,830*ss,mx+610*ss,830*ss),fill=BONE+(60,),width=ss)
    ctext(d,(mx,875*ss),'GTA 6  —  CURIOSIDADES  ·  NOTÍCIAS  ·  MELHORES MOMENTOS',fl,BONE+(200,),sp=4*ss)
    # ponto de calor junto ao nome
    blip(img,mx+690*ss,612*ss,8*ss,ss)
    # marcas de canto
    d=ImageDraw.Draw(img,'RGBA')
    for (x,y,sx,sy) in ((90,90,1,1),(Wd-90,90,-1,1),(90,Ht-90,1,-1),(Wd-90,Ht-90,-1,-1)):
        d.line((x*ss,y*ss,(x+40*sx)*ss,y*ss),fill=BONE+(120,),width=ss*2); d.line((x*ss,y*ss,x*ss,(y+40*sy)*ss),fill=BONE+(120,),width=ss*2)
    fs=font('GeistMono-Regular.ttf',15*ss); d.text(((Wd-90)*ss,(Ht-60)*ss),'25°46′N  80°11′W  ·  REF. 0619',font=fs,fill=BONE+(80,),anchor='rs')
    return img.convert('RGB').resize((Wd,Ht),Image.LANCZOS)
perfil().save('CaosInsano_perfil_800.png'); banner().save('CaosInsano_banner_2560x1440.png')
