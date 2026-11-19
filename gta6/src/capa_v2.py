"""Capas v2 (padrão thumbnail): personagem recortado em alta + texto metálico por trás e faixa amarela na frente."""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
from rembg import remove, new_session
F='/home/user/playtimeguitarshop/gta6/fonts/'; P='/home/user/gta6_brutos/shots/People/'
OUT='/home/user/playtimeguitarshop/gta6/entregas/capas_v2/'; os.makedirs(OUT,exist_ok=True)
CACHE='/home/user/playtimeguitarshop/gta6/src/capas_v2/'
W,H=1080,1920
sess=None
def cutout(path):
    global sess
    c=CACHE+os.path.basename(path).replace('.jpg','.png')
    if os.path.exists(c): return Image.open(c)
    if sess is None: sess=new_session('u2net_human_seg')
    im=Image.open(path).convert('RGB'); o=remove(im,session=sess,post_process_mask=True); o.save(c); return o
def chrome_text(txt,size,font='ARN.ttf',stroke=10):
    f=ImageFont.truetype(F+font,size); d=ImageDraw.Draw(Image.new('L',(1,1)))
    l,t,r,b=d.textbbox((0,0),txt,font=f,stroke_width=stroke); w,h=r-l+40,b-t+40
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).text((20-l,20-t),txt,font=f,fill=255)
    ms=Image.new('L',(w,h),0); ImageDraw.Draw(ms).text((20-l,20-t),txt,font=f,fill=255,stroke_width=stroke,stroke_fill=255)
    g=Image.new('RGB',(w,h));gd=ImageDraw.Draw(g)
    for y in range(h):
        k=y/h; v=int(255-60*abs(k-.45)*2.2) if k<.55 else int(205-70*(k-.55)/0.45)
        gd.line((0,y,w,y),fill=(v,v,min(255,v+6)))
    out=Image.new('RGBA',(w,h),(0,0,0,0))
    out.paste((14,10,22,255),(0,0),ms)                       # contorno escuro
    out.paste(g,(0,0),m)                                     # preenchimento cromado
    sh=Image.new('RGBA',(w+60,h+60),(0,0,0,0)); sh.paste((0,0,0,200),(30,42),ms); sh=sh.filter(ImageFilter.GaussianBlur(14))
    sh.alpha_composite(out,(30,30)); return sh
def yellow_bar(txt,size,angle=-4):
    f=ImageFont.truetype(F+'AR.ttf',size); d=ImageDraw.Draw(Image.new('L',(1,1)))
    l,t,r,b=d.textbbox((0,0),txt,font=f); w,h=r-l+90,b-t+50
    bar=Image.new('RGBA',(w,h),(0,0,0,0)); bd=ImageDraw.Draw(bar)
    bd.polygon([(14,8),(w-4,0),(w-16,h-6),(0,h)],fill=(255,214,30,255))
    bd.text((45-l,25-t),txt,font=f,fill=(10,10,10,255))
    bar=bar.rotate(-angle*-1,expand=True,resample=Image.BICUBIC)
    sh=Image.new('RGBA',(bar.width+40,bar.height+40),(0,0,0,0)); sh.paste((0,0,0,170),(20,30),bar); sh=sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(bar,(20,20)); return sh
def arrow(c,x,y,flip=False):
    a=Image.new('RGBA',(260,260),(0,0,0,0)); d=ImageDraw.Draw(a)
    d.arc((20,-120,330,190),95,170,fill=(255,214,30,255),width=18)
    d.polygon([(30,120),(5,175),(70,160)],fill=(255,214,30,255))
    if flip: a=ImageOps.mirror(a)
    c.alpha_composite(a,(x,y))
def make(n,src,top,bar,cx=.5,scale=1.0,py=0,ty=330,tsize=300,bsize=100,tag='GTA 6',arrow_x=None,by=1240,hfrac=.80,bg='/home/user/gta6_brutos/shots/Places/Vice City/Vice_City_01.jpg',bgx=.5):
    cut=cutout(P+src); im=Image.open(bg).convert('RGB'); cx_bg=bgx
    s=H/im.height; bg=im.resize((int(im.width*s),H),Image.LANCZOS); x0=int((bg.width-W)*cx_bg); bg=bg.crop((x0,0,x0+W,H))
    bg=bg.filter(ImageFilter.GaussianBlur(10)); bg=ImageEnhance.Brightness(bg).enhance(.55); bg=ImageEnhance.Color(bg).enhance(1.2)
    c=bg.convert('RGBA')
    v=Image.new('RGBA',(W,H),(0,0,0,0)); vd=ImageDraw.Draw(v)
    for y in range(H): vd.line((0,y,W,y),fill=(5,3,12,int(150*max(0,(y-H*.55)/(H*.45)))))
    c.alpha_composite(v)
    # texto de trás
    t=chrome_text(top,tsize); 
    if t.width>W-20: t=t.resize((W-20,int(t.height*(W-20)/t.width)),Image.LANCZOS)
    c.alpha_composite(t,((W-t.width)//2,ty))
    # personagem: bbox do recorte, escala para ~78% da altura
    bb=cut.getbbox(); pc=cut.crop(bb)
    top_y=ty+int(t.height*.60)                      # cabeça entra só na parte de baixo das letras
    ss=(H-top_y+40)/pc.height
    if pc.width*ss>W*1.25: ss=W*1.25/pc.width; top_y=H+40-int(pc.height*ss)
    pc=pc.resize((int(pc.width*ss),int(pc.height*ss)),Image.LANCZOS)
    px=int(W*cx-pc.width/2)
    glow=Image.new('RGBA',pc.size,(0,0,0,0)); glow.paste((0,0,0,170),(0,0),pc.split()[3]); glow=glow.filter(ImageFilter.GaussianBlur(25))
    c.alpha_composite(glow,(px,top_y+10)); c.alpha_composite(pc,(px,top_y))
    # faixa amarela na frente
    b=yellow_bar(bar,bsize)
    if b.width>W-40: b=b.resize((W-40,int(b.height*(W-40)/b.width)),Image.LANCZOS)
    c.alpha_composite(b,((W-b.width)//2,by))
    if arrow_x is not None: arrow(c,arrow_x,by+b.height-30)
    # selo GTA 6
    f=ImageFont.truetype(F+'ARN.ttf',54); d=ImageDraw.Draw(c); tw=d.textlength(tag,font=f)
    d.rounded_rectangle((40,70,40+tw+44,70+84),18,fill=(225,40,150,255)); d.text((62,80),tag,font=f,fill=(255,255,255,255))
    c.convert('RGB').save(OUT+f'capa_{n}.jpg',quality=93)
if __name__=='__main__':
    for job in json.load(open(sys.argv[1])): make(**job)
