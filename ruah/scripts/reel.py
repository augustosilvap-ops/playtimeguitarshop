import sys, os, subprocess
sys.path.insert(0,'.'); sys.path.insert(0,'/tmp/claude-0/-home-claude/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/scratchpad/video')
from common import *
import anatomia as A
FPS=30; OUT='reel/'; os.makedirs(OUT,exist_ok=True)
def eo(x): x=max(0,min(1,x)); return 1-(1-x)**3
def seg(t,a,b): return max(0,min(1,(t-a)/(b-a)))
GR=[np.random.default_rng(i).normal(0,4,(H,W,1)) for i in range(4)]
def grade(im,fi,dark=0.34):
    a=np.asarray(im).astype(np.float32); g=a.mean(2,keepdims=True); a=g+(a-g)*0.55
    a=(a-128)*1.08+122; a=a*dark+GR[fi%4]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def zoom(im,z):
    vw,vh=W/z,H/z; return im.resize((W,H),Image.BILINEAR,box=((W-vw)/2,(H-vh)/2,(W+vw)/2,(H+vh)/2))
def put(c,L,cx,cy,p):
    if p<=0: return
    s=0.86+0.14*eo(p); l=L.resize((int(L.width*s),int(L.height*s)),Image.BILINEAR)
    if p<1: l.putalpha(l.split()[3].point(lambda v:int(v*min(1,p*1.6))))
    c.paste(l,(int(cx-l.width/2),int(cy-l.height/2+(1-eo(p))*40)),l)
def text_c(d,txt,font,y,fill=BONE,track=0):
    if track: tracked(d,W/2,y,txt,font,fill,track)
    else: d.text((W/2,y),txt,font=font,fill=fill,anchor='ms')
CL=[card_layer(a) for a in ANS]
# cenas: (parte, início, dur-fonte, velocidade, dur-saída)
SC=[(7,2.6,1.4,0.7,2.0),(6,0.0,1.6,0.62,2.6),(6,19.4,1.1,0.42,2.6),(6,10.6,1.4,0.54,2.6),(6,30.0,2.0,0.77,2.6)]
def enc(name):
    return subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-',
        '-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p',OUT+name],stdin=subprocess.PIPE)
def scene(k,t,fr):
    n=len(fr); i=min(n-1,int(t*FPS)); dur=SC[k][4]
    c=grade(zoom(Image.fromarray(fr[i]),1.0+0.06*t/dur),i)
    d=ImageDraw.Draw(c)
    if t<0.12 and k>0: c=Image.blend(c,Image.new('RGB',(W,H),(255,255,255)),0.35*(1-t/0.12)); d=ImageDraw.Draw(c)
    if k==0:
        c=Image.blend(c,Image.new('RGB',(W,H),(8,8,9)),0.45*eo(seg(t,0,0.4))); d=ImageDraw.Draw(c)
        p=eo(seg(t,0.15,0.6)); q=eo(seg(t,0.9,1.3))
        if p>0: tracked(d,W/2,860,'MOSTRAMOS DE PERTO.',F('cinzel900',62),tuple(int(v*p) for v in BONE),6)
        if q>0: d.text((W/2,980),'Vocês responderam.',font=F('cg400i',84),fill=tuple(int(v*q) for v in BONE),anchor='ms')
    else:
        tracked(d,W/2,420,'O QUE VOCÊS VIRAM NO VÍDEO',F('cinzel700',24),MUT,7)
        put(c,CL[k-1],W/2,900,seg(t,0.25,0.7))
    return c
def endc(t,fi):
    c=bg_dark(fi%3+5); d=ImageDraw.Draw(c)
    s=img(SYM,h=1500); s.putalpha(s.split()[3].point(lambda v:int(v*0.06))); c.paste(s,((W-s.width)//2,230),s)
    a=eo(seg(t,0.1,0.5)); b=eo(seg(t,0.5,0.9)); e=eo(seg(t,1.2,1.6)); g=eo(seg(t,1.7,2.1))
    l=img(LOGO,w=200)
    if a:
        l2=l.copy(); l2.putalpha(l2.split()[3].point(lambda v:int(v*a))); c.paste(l2,((W-l.width)//2,520),l2)
        d.text((W/2,770),'Ver no vídeo é uma coisa.',font=F('cg400i',74),fill=tuple(int(v*a) for v in BONE),anchor='ms')
    if b: tracked(d,W/2,895,'VESTIR É OUTRA.',F('cinzel900',86),tuple(int(v*b) for v in BONE),8)
    if e:
        tracked(d,W/2,1060,'ACESSE O SITE E',F('cinzel700',40),tuple(int(v*e) for v in BONE),8)
        tracked(d,W/2,1120,'COMPRE JÁ A SUA',F('cinzel900',56),tuple(int(v*e) for v in BONE),8)
    if g:
        z=1.12-0.12*g; bw,bh=600*z,118*z; y=1250
        d.rounded_rectangle([W/2-bw/2,y-bh/2,W/2+bw/2,y+bh/2],radius=int(59*z),fill=BONE)
        f=F('cinzel900',int(44*z)); tracked(d,W/2,y+int(16*z),'USERUAH.COM',f,(12,12,12),6)
        if t>2.5:
            q=(t-2.5)%0.9/0.9; r=8+40*q
            d.rounded_rectangle([W/2-300-r,y-59-r,W/2+300+r,y+59+r],radius=int(59+r),outline=tuple(int(v*(1-q)) for v in BONE),width=3)
        tracked(d,W/2,1380,'LINK NA BIO',F('cinzel700',24),tuple(int(v*g) for v in MUT),8)
    return c
if __name__=='__main__':
    files=[]
    for k,(part,t0,dsrc,sp,dout) in enumerate(SC):
        fr=A.decode(part,t0,dsrc,sp,0.5,0.5,1.0); n=int(dout*FPS); p=enc(f's{k}.mp4')
        for i in range(n): p.stdin.write(scene(k,i/FPS,fr).tobytes())
        p.stdin.close(); p.wait(); files.append(f's{k}.mp4'); print(k,len(fr),n,flush=True)
    p=enc('s9.mp4'); n=int(4.2*FPS)
    for i in range(n): p.stdin.write(endc(i/FPS,i).tobytes())
    p.stdin.close(); p.wait(); files.append('s9.mp4')
    open(OUT+'list.txt','w').write(''.join(f"file '{f}'\n" for f in files))
    if len(sys.argv)>1 and sys.argv[1]=='frames': pass
