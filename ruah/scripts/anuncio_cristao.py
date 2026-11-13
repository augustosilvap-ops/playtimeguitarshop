"""Anúncio: 'Você é cristão...' — filmagem real + legenda cinética."""
import sys, os, subprocess
SPD = '/tmp/claude-0/-home-claude/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/scratchpad/'
sys.path.insert(0, SPD + 'reacoes'); sys.path.insert(0, SPD + 'video')
from common import *
import anatomia as A
FPS = 30; OUT = SPD + 'adcrist/out/'; os.makedirs(OUT, exist_ok=True)
def eo(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def seg(t, a, b): return max(0, min(1, (t - a) / (b - a)))
GR = [np.random.default_rng(i).normal(0, 4, (H, W, 1)) for i in range(4)]
yy, xx = np.mgrid[0:H, 0:W]
GRADB = np.ones((H,1,1)); GRADB[:,0,0] = 1 - 0.80*np.clip((np.arange(H)-950)/380,0,1)
VIG = (1 - 0.45 * np.clip(np.hypot((xx - W / 2) / (W * 0.7), (yy - H / 2) / (H * 0.6)), 0, 1) ** 2)[..., None]

def grade(im, fi, dark, sat):
    a = np.asarray(im).astype(np.float32); g = a.mean(2, keepdims=True); a = g + (a - g) * sat
    a = (a - 128) * 1.12 + 122; a = a * dark * VIG
    if dark > 0.35: a = a * GRADB
    a = a + GR[fi % 4]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def zoom(im, z, dx=0):
    vw, vh = W / z, H / z
    return im.resize((W, H), Image.BILINEAR, box=((W - vw) / 2 + dx, (H - vh) / 2, (W + vw) / 2 + dx, (H + vh) / 2))

def layer(txt, font, fill=BONE, track=0):
    d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    ws = [d0.textlength(ch, font=font) for ch in txt]; tw = int(sum(ws) + track * (len(txt) - 1)) + 40
    asc, desc = font.getmetrics(); L = Image.new('RGBA', (tw, asc + desc + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x = 20
    for ch, w in zip(txt, ws): d.text((x, 20 + asc), ch, font=font, fill=fill + (255,), anchor='ls'); x += w + track
    return L

def put(c, L, cx, cy, p, mode='slam'):
    """slam: cai de 1.5x com desfoque; rise: sobe e aparece"""
    if p <= 0: return
    e = eo(p)
    if mode == 'slam':
        s = 1.5 - 0.5 * e; l = L.resize((max(1, int(L.width * s)), max(1, int(L.height * s))), Image.BILINEAR)
        if p < 1: l = l.filter(ImageFilter.GaussianBlur(10 * (1 - e)))
        oy = 0
    else:
        l = L.copy(); oy = (1 - e) * 46
    if p < 1: l.putalpha(l.split()[3].point(lambda v: int(v * min(1, p * 1.8))))
    # sombra
    sh = Image.new('RGBA', l.size, (0, 0, 0, 0)); sh.putalpha(l.split()[3].point(lambda v: int(v * 0.6)))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    c.paste(sh, (int(cx - l.width / 2), int(cy - l.height / 2 + oy + 6)), sh)
    c.paste(l, (int(cx - l.width / 2), int(cy - l.height / 2 + oy)), l)

def underline(c, cx, y, w, p):
    if p <= 0: return
    ln = int(w * eo(p)); ImageDraw.Draw(c).rectangle([cx - w / 2, y, cx - w / 2 + ln, y + 6], fill=BONE)

def progress(c, t, total):
    d = ImageDraw.Draw(c); d.rectangle([0, 0, int(W * t / total), 6], fill=BONE)

CG = lambda s: F('cg400i', s); CZ = lambda s: F('cinzel900', s); CZ7 = lambda s: F('cinzel700', s)
L = {
 'cr':   layer('VOCÊ É CRISTÃO', CZ(92), track=6),
 'q1':   layer('e já se pegou', CG(84)),
 'q2':   layer('vestindo marcas', CG(84)),
 'est':  layer('para ter estilo', CG(92)),
 'mas':  layer('MAS SEM TER', CZ7(60), track=8),
 'prop': layer('PROPÓSITO?', CZ(124), track=6),
 'a1':   layer('A RUAH FOI CRIADA', CZ(76), track=6),
 'a2':   layer('pensando em você.', CG(100)),
 'ag':   layer('AGORA VOCÊ PODE SE VESTIR COM', CZ7(36), BONE, 6),
 'w1':   layer('ESTILO,', CZ(150), track=8),
 'w2':   layer('QUALIDADE', CZ(132), track=6),
 'ea':   layer('E AINDA CARREGAR', CZ7(46), track=8),
 'w3':   layer('UMA MENSAGEM.', CZ(100), track=6),
}

# cenas: (parte, início, dur-fonte, velocidade, cx, cy, largura, dur-saída, escuro, saturação)
SC = [
 (7, 11.4, 1.6, 0.52, 0.50, 0.45, 1.00, 3.1, 0.30, 0.35),   # costas — gancho
 (6, 0.0, 1.5, 0.48, 0.50, 0.50, 1.00, 3.1, 0.30, 0.35),    # estampa costas
 (7, 2.4, 1.6, 0.58, 0.50, 0.42, 0.98, 2.8, 0.42, 0.60),    # unboxing
 (6, 10.6, 1.2, 0.55, 0.55, 0.36, 0.62, 2.2, 0.55, 0.85),   # frente
 (6, 19.4, 1.0, 0.45, 0.42, 0.40, 0.58, 2.2, 0.55, 0.85),   # gola
 (6, 30.0, 1.6, 0.58, 0.46, 0.55, 0.80, 2.8, 0.50, 0.80),   # versículo por dentro
]
END = 4.6
TOTAL = sum(s[7] for s in SC) + END

def scene(k, t, fr, T0):
    n = len(fr); i = min(n - 1, int(t * FPS)); dur = SC[k][7]
    z = 1.0 + 0.07 * t / dur
    if t < 0.18: z += 0.05 * (1 - t / 0.18)                       # punch no corte
    c = grade(zoom(Image.fromarray(fr[i]), z), i, SC[k][8], SC[k][9])
    if t < 0.1 and k > 0: c = Image.blend(c, Image.new('RGB', (W, H), (255, 255, 255)), 0.45 * (1 - t / 0.1))
    y0 = 860 if k < 2 else 1400
    if k == 0:
        put(c, L['cr'], W / 2, y0 - 70, seg(t, 0.10, 0.42))
        put(c, L['q1'], W / 2, y0 + 50, seg(t, 0.9, 1.3), 'rise')
        put(c, L['q2'], W / 2, y0 + 150, seg(t, 1.35, 1.75), 'rise')
    elif k == 1:
        put(c, L['est'], W / 2, y0 - 90, seg(t, 0.05, 0.45), 'rise')
        put(c, L['mas'], W / 2, y0 + 40, seg(t, 1.0, 1.3))
        put(c, L['prop'], W / 2, y0 + 160, seg(t, 1.35, 1.65))
        underline(c, W / 2, y0 + 245, 560, seg(t, 1.8, 2.3))
    elif k == 2:
        put(c, L['a1'], W / 2, y0 - 40, seg(t, 0.15, 0.45))
        put(c, L['a2'], W / 2, y0 + 80, seg(t, 0.75, 1.15), 'rise')
    elif k in (3, 4):
        put(c, L['ag'], W / 2, y0 - 120, 1.0 if k == 4 else seg(t, 0.05, 0.4), 'rise')
        put(c, L['w1' if k == 3 else 'w2'], W / 2, y0 + 10, seg(t, 0.25, 0.55))
    elif k == 5:
        put(c, L['ea'], W / 2, y0 - 70, seg(t, 0.1, 0.45), 'rise')
        put(c, L['w3'], W / 2, y0 + 50, seg(t, 0.6, 0.9))
    progress(c, T0 + t, TOTAL)
    return c

LG = img(LOGO, w=230)
E1 = layer('SIGA NOSSO INSTAGRAM', CZ(60), track=6)
E2 = layer('e faça parte do movimento.', CG(80))
def endc(t, fi, T0):
    c = bg_dark(fi % 3 + 5); d = ImageDraw.Draw(c)
    s = img(SYM, h=1500); s.putalpha(s.split()[3].point(lambda v: int(v * 0.06 * eo(seg(t, 0, 1))))); c.paste(s, ((W - s.width) // 2, 230), s)
    a = eo(seg(t, 0.05, 0.5))
    if a:
        l2 = LG.copy(); l2.putalpha(l2.split()[3].point(lambda v: int(v * a))); c.paste(l2, ((W - LG.width) // 2, 500 - int(20 * (1 - a))), l2)
    put(c, E1, W / 2, 820, seg(t, 0.5, 0.8))
    put(c, E2, W / 2, 930, seg(t, 1.0, 1.4), 'rise')
    g = eo(seg(t, 1.6, 2.0))
    if g:
        d = ImageDraw.Draw(c); zz = 1.12 - 0.12 * g; bw, bh = 620 * zz, 120 * zz; y = 1110
        d.rounded_rectangle([W / 2 - bw / 2, y - bh / 2, W / 2 + bw / 2, y + bh / 2], radius=int(60 * zz), fill=BONE)
        tracked(d, W / 2, y + int(16 * zz), '@RUAHWEAR_', F('cinzel900', int(46 * zz)), (12, 12, 12), 6)
        if t > 2.1:
            q = (t - 2.1) % 0.9 / 0.9; r = 8 + 40 * q
            d.rounded_rectangle([W / 2 - 310 - r, y - 60 - r, W / 2 + 310 + r, y + 60 + r], radius=int(60 + r), outline=tuple(int(v * (1 - q)) for v in BONE), width=3)
        tracked(d, W / 2, 1250, 'WE CARRY THE SPIRIT.', F('cinzel700', 26), tuple(int(v * g) for v in MUT), 8)
    progress(c, T0 + t, TOTAL)
    return c

def enc(name):
    return subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                             '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', OUT + name], stdin=subprocess.PIPE)

if __name__ == '__main__':
    mode = sys.argv[1]
    T0 = 0; files = []
    for k, (part, t0, dsrc, sp, cx, cy, w, dout, *_ ) in enumerate(SC):
        fr = A.decode(part, t0, dsrc, sp, cx, cy, w)
        if mode == 'frames':
            for tt in (dout * 0.85,):
                scene(k, tt, fr, T0).save(OUT + f'f{k}.jpg', quality=85)
        else:
            n = int(dout * FPS); p = enc(f'_s{k}.mp4')
            for i in range(n): p.stdin.write(scene(k, i / FPS, fr, T0).tobytes())
            p.stdin.close()
            if p.wait() == 0: os.replace(OUT + f'_s{k}.mp4', OUT + f's{k}.mp4')
            files.append(f's{k}.mp4'); print(k, len(fr), n, flush=True)
        T0 += dout
    if mode == 'frames':
        endc(3.0, 0, T0).save(OUT + 'f9.jpg', quality=85)
    else:
        n = int(END * FPS); p = enc('_s9.mp4')
        for i in range(n): p.stdin.write(endc(i / FPS, i, T0).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.replace(OUT + '_s9.mp4', OUT + 's9.mp4')
        files.append('s9.mp4')
        open(OUT + 'list.txt', 'w').write(''.join(f"file '{f}'\n" for f in files))
