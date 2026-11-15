"""Aplica um TEMA visual a um Reel Cinético (cores de fundo, animação das palavras, transição entre cenas e textura).
Uso: python3 tema.py arquivo.html NOME_DO_TEMA   — temas em TEMAS abaixo. Reaplicável (substitui o tema anterior)."""
import sys, re, json
TEMAS = {
 # fundo escuro/claro/destaque · anim: left|mask|zoom|flip|up · trans: wipe|zoom|flash|slide|cut · deco: grid|dots|rings|scan|none
 'preto_grade':   dict(dark='#000000', light='#FFFFFF', accent='#2F6BFF', anim='left', trans='wipe',  deco='grid', align='left'),
 'claro_pontos':  dict(dark='#0A1430', light='#EEF2FA', accent='linear-gradient(160deg,#5B8CFF,#1C47C9)', anim='mask', trans='zoom', deco='dots', align='center'),
 'azul_aneis':    dict(dark='radial-gradient(900px 1200px at 50% 30%,#13307A,#050A1C)', light='#F5F7FB', accent='#1C47C9', anim='zoom', trans='flash', deco='rings', align='right'),
 'navy_scan':     dict(dark='#08090E', light='#FFFFFF', accent='#2F6BFF', anim='flip', trans='slide', deco='scan', align='left'),
 'original':      dict(dark='#08090E', light='#F5F7FB', accent='#2F6BFF', anim='up', trans='cut', deco='none'),
}
f, nome = sys.argv[1], sys.argv[2]
T = TEMAS[nome]
s = open(f).read()
s = re.sub(r'\n?const TEMA=.*?;\n', '\n', s)
s = s.replace("const NAVY='#08090E'", "const TEMA=" + json.dumps(T) + ";\nconst NAVY='#08090E'", 1)
W = r'''function w(t,t0,txt,x,y,size,c,o={}){if(t<t0)return'';const p=cl((t-t0)/.2),q=eo(p),s=(o.s||1.35)-((o.s||1.35)-1)*eb(p);let tr,ex='';
 switch(TEMA.anim){case'left':tr=`translateX(${(1-q)*-160}px) skewX(${(1-q)*-14}deg)`;break;
  case'mask':tr=`translateY(${(1-q)*45}%)`;ex=`clip-path:inset(0 0 ${(1-q)*100}% 0);`;break;
  case'zoom':tr=`scale(${1+(1-q)*1.6})`;ex=`filter:blur(${(1-p)*16}px);`;break;
  case'flip':tr=`perspective(900px) rotateX(${(1-q)*-95}deg)`;break;
  default:tr=`translateY(${(1-q)*60}px) scale(${s})`;ex=`filter:blur(${(1-p)*12}px);`}
 const pos=TEMA.align==='center'?`left:0;right:0;text-align:center;`:TEMA.align==='right'?`right:84px;text-align:right;`:`left:${x}px;`;
 return `<div class="w" style="${pos}top:${y}px;font-size:${size}px;color:${c};transform:${tr};transform-origin:${TEMA.anim==='flip'?'50% 100%':TEMA.align==='center'?'50% 50%':TEMA.align==='right'?'100% 50%':(o.o||'0 50%')};${ex}opacity:${cl(p*3)}">${txt}</div>`}'''
a = s.index('function w(t,t0,txt'); b = s.index('}', s.index('</div>`', a)) + 1
EX = r'''
function stamp(lt,t0,word,y){const q=eo((lt-t0)/.18),sh=lt>t0&&lt<t0+.3?Math.sin(lt*120)*10*(1-(lt-t0)/.3):0;return `<div style="position:absolute;left:0;right:0;top:${y}px;text-align:center;font:800 190px/1 I;letter-spacing:-.06em;color:#fff;transform:translateX(${sh}px)">${word}</div>`+(lt<t0?'':`<div style="position:absolute;left:50%;top:${y-30}px;transform:translateX(-50%) rotate(-12deg) scale(${1+(1-q)*1.8});opacity:${q};border:12px solid #E5384A;color:#E5384A;border-radius:24px;padding:10px 40px;font:800 130px/1 I;letter-spacing:.04em;background:rgba(255,255,255,.08)">NÃO</div>`)}
function split(lt,t0,word,y){const q=eo((lt-t0)/.5),d=lt<t0?0:q*90;const base=`position:absolute;left:0;right:0;top:${y}px;text-align:center;font:800 200px/1 I;letter-spacing:-.06em;color:#fff`;return `<div style="${base};clip-path:inset(0 0 50% 0);transform:translate(${-d*.4}px,${-d}px) rotate(${-q*4}deg)">${word}</div><div style="${base};clip-path:inset(50% 0 0 0);transform:translate(${d*.4}px,${d}px) rotate(${q*4}deg)">${word}</div>`+(lt<t0?'':`<div style="position:absolute;left:-40px;right:-40px;top:${y+100}px;height:6px;background:#E5384A;transform:scaleX(${cl((lt-t0)/.15)});opacity:${1-q*.6}"></div>`)}
function strike(lt,t0,word,y){const q=eo((lt-t0)/.25),sh=lt>t0&&lt<t0+.35?Math.sin(lt*110)*12*(1-(lt-t0)/.35):0;return `<div style="position:absolute;left:84px;top:${y}px;font:800 200px/1 I;letter-spacing:-.06em;color:#fff;transform:translateX(${sh}px)">${word}<div style="position:absolute;left:-20px;top:46%;height:22px;width:calc(100% + 40px);background:#E5384A;transform-origin:0 50%;transform:scaleX(${lt<t0?0:q}) rotate(-4deg)"></div></div>`}
'''
s = s[:a] + W + EX + s[b:]
s = re.sub(r"\nfunction stamp\(.*?\nfunction strike\(.*?\n", "\n", s, flags=re.S) if s.count('function stamp(')>1 else s
R = r'''window.R=function(t){
 const i=SC.findIndex(s=>t>=s[0]&&t<s[1]),s=SC[i<0?SC.length-1:i],lt=t-s[0];
 const dark=s[2]===NAVY,blue=s[2]===BLUE,fg=dark||blue?'#fff':INK,bg=dark?TEMA.dark:blue?TEMA.accent:TEMA.light;
 const q=eo(lt/.28);let wrapT=`scale(${1+.02*lt})`,over='';
 if(TEMA.trans==='zoom')wrapT=`scale(${1+.22*(1-q)+.02*lt})`;
 if(TEMA.trans==='slide')wrapT=`translateY(${(1-q)*220}px) scale(${1+.02*lt})`;
 if(TEMA.trans==='flash'&&lt<.3)over=`<div style="position:absolute;inset:0;background:#fff;opacity:${.85*(1-lt/.3)}"></div>`;
 if(TEMA.trans==='wipe'&&lt<.35&&i>0)over=`<div style="position:absolute;top:0;bottom:0;width:1080px;left:${-1080+2160*eo(lt/.35)}px;background:${blue?'#fff':'#2F6BFF'}"></div>`;
 if(TEMA.trans==='cut')wrapT=`scale(${1+(lt<.15?.04*(1-lt/.15):0)+.02*lt})`;
 const ln=dark||blue?'rgba(255,255,255,':'rgba(10,11,16,';let deco='';
 if(TEMA.deco==='grid')deco=`<div style="position:absolute;inset:0;background-image:linear-gradient(${ln}.07) 2px,transparent 2px),linear-gradient(90deg,${ln}.07) 2px,transparent 2px);background-size:90px 90px;background-position:0 ${(t*40)%90}px"></div>`;
 if(TEMA.deco==='dots')deco=`<div style="position:absolute;inset:0;background-image:radial-gradient(${ln}.16) 2.5px,transparent 3px);background-size:44px 44px;background-position:${(t*18)%44}px 0"></div>`;
 if(TEMA.deco==='rings')deco=`<svg style="position:absolute;right:-380px;top:-300px" width="1100" height="1100" viewBox="0 0 1100 1100" fill="none">${[0,1,2,3,4].map(k=>`<circle cx="550" cy="550" r="${180+k*90}" stroke="${ln}${.16-k*.025})" stroke-width="3" stroke-dasharray="${k%2?'14 18':'none'}" transform="rotate(${t*(k%2?20:-12)} 550 550)"/>`).join('')}</svg>`;
 if(TEMA.deco==='scan')deco=`<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,${ln}.04) 0 2px,transparent 2px 6px)"></div><div style="position:absolute;left:0;right:0;height:260px;top:${((t*520)%2400)-260}px;background:linear-gradient(180deg,transparent,${ln}.07),transparent)"></div>`;
 document.getElementById('v').innerHTML=`<div style="position:absolute;inset:0;background:${bg}"></div>${deco}
  <div style="position:absolute;inset:0;transform:${wrapT};transform-origin:30% 50%">${s[3](lt/1.25)}</div>${over}
  <div class="chip" style="color:${fg}"><i style="background:${blue?'#fff':BLUE};color:${blue?BLUE:'#fff'}">↗</i>@augustosilva.p</div>
  <div class="cap" style="color:${fg};opacity:.9">${s[4]}</div>
  <div class="bar" style="width:912px;background:${dark||blue?'rgba(255,255,255,.2)':'rgba(10,11,16,.12)'}"></div>
  <div class="bar" style="width:${912*t/DUR}px;background:${blue?'#fff':BLUE}"></div>`};'''
a = s.index('window.R=function(t){'); b = s.index('R(0);', a)
s = s[:a] + R + '\n' + s[b:]
open(f, 'w').write(s); print('ok', f, nome)
