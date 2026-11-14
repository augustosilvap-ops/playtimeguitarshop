"""Prévia da grade do perfil (miniaturas 3:4, mais recente no canto superior esquerdo)."""
from PIL import Image, ImageDraw, ImageFont
import sys
order=[["09","08","07"],["06","05","04"],["03","02","01"]]
W=360;H=480;G=4
def thumb(p):
    im=Image.open(p).convert("RGB"); w,h=im.size; tw=int(h*3/4) if w/h>0.75 else w; th=int(tw*4/3)
    x=(w-tw)//2; y=(h-th)//2; return im.crop((x,y,x+tw,y+th)).resize((W,H),Image.LANCZOS)
S=Image.new("RGB",(3*W+2*G,3*H+2*G),"white")
for r,row in enumerate(order):
    for c,i in enumerate(row): S.paste(thumb(f"previa/capas/{i}.png"),(c*(W+G),r*(H+G)))
S.save("previa/grade_3x3.png")
L=S.copy(); d=ImageDraw.Draw(L); f=ImageFont.truetype("src/fonts/JetBrainsMono-600.ttf",22)
lab={"01":"A foto","02":"C dashboard","03":"A reel","04":"B clean","05":"D conceito","06":"B reel","07":"D conceito","08":"A foto","09":"C reel"}
for r,row in enumerate(order):
    for c,i in enumerate(row):
        x,y=c*(W+G)+10,r*(H+G)+10; t=f"{i} · {lab[i]}"; d.rectangle([x,y,x+d.textlength(t,font=f)+16,y+34],fill="#2F6BFF"); d.text((x+8,y+5),t,font=f,fill="white")
L.save("previa/grade_3x3_rotulada.png"); print("ok")
