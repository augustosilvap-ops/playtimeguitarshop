"""Capas v6 (identidade oficial, aprovada 23/11): arte oficial ilustrada da Rockstar de fundo, logo circular do Caos Insano
no canto esquerdo, logo oficial do GTA VI no direito, título em 3 linhas: bloco branco (AR) + palavra-chave em pincel rosa
(Knewave) + complemento branco, traço ciano e seta vermelha opcional.
Uso (biblioteca): make(n, a, b, c, arte, out_dir, seta=None)
  arte = nome do arquivo em src/thumb_v5/art/ (ex.: 'Cal_Hampton_portrait.jpg'); seta = (x, y, 'esq'|'dir') ou None."""
import os, subprocess, json, tempfile, html
HERE = os.path.dirname(os.path.abspath(__file__)); T5 = os.path.join(HERE, 'thumb_v5')
MOT = os.path.abspath(os.path.join(HERE, '../../augusto/src/motion'))
ARTES = sorted(f for f in os.listdir(os.path.join(T5, 'art')) if f.endswith('_portrait.jpg'))
JS = r"""const {chromium}=require('playwright');(async()=>{const [f,o]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);
await p.waitForTimeout(400);await (await p.$('.t')).screenshot({path:o,type:'jpeg',quality:93});await b.close()})();"""

def _html(a, b, c, arte, seta):
    base = open(os.path.join(T5, 'thumb_v6.html')).read()
    head = base[:base.index('<div class="t" id="c1">')]
    tail = base[base.index('<script>'):]
    arr = ''
    if seta:
        x, y, lado = seta
        flip = 'transform:scaleX(-1);' if lado == 'dir' else ''
        arr = (f'<svg class="arr" style="left:{x}px;top:{y}px;{flip}" width="280" height="280" viewBox="0 0 300 300">'
               '<path d="M260 40 C 120 30, 60 120, 90 230" stroke="#ff2b2b" stroke-width="36" fill="none" stroke-linecap="round"/>'
               '<path d="M30 190 L90 265 L160 200" stroke="#ff2b2b" stroke-width="36" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    e = html.escape
    body = (f'<div class="t" id="c1"><div class="bg" style="background-image:url(\'art/{arte}\')"></div><div class="shade"></div>'
            '<img class="badge" src="CaosInsano_logo_circular.png"><img class="gta" src="GTA_VI_logo_oficial.png">'
            f'{arr}<div class="tt" style="top:1250px"><span class="a">{e(a)}</span><span class="b">{e(b)}</span><span class="c">{e(c)}</span></div>'
            '<div class="swh" style="top:1745px"></div><div class="hand">@caosinsano.br</div></div>')
    return head + body + tail

def make(n, a, b, c, arte, out_dir, seta=None):
    os.makedirs(out_dir, exist_ok=True)
    hp = os.path.join(T5, f'_capa_{n}.html'); open(hp, 'w').write(_html(a, b, c, arte, seta))
    js = os.path.join(tempfile.gettempdir(), 'capa_v6_shot.js'); open(js, 'w').write(JS)
    out = os.path.join(out_dir, f'capa_{n}.jpg')
    try: subprocess.run(['node', js, hp, out], check=True, cwd=MOT)
    finally: os.remove(hp)
    return out
