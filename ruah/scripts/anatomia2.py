"""ANATOMIA DA PEÇA v2 — moderno: barras segmentadas, rótulos em vidro, ponto pulsando, foco no detalhe.
Sem o som da filmagem (só trilha + efeitos sintetizados)."""
import sys, os, subprocess, math, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import anatomia as A
from anatomia import W, H, FPS, F, INTER_B, INTER_M, MONO, CG, clamp, eo, eio, seg, scaled, LOGO, SYM, grade, decode
OUT = A.SP + 'video/anat2/'; os.makedirs(OUT, exist_ok=True)
INK = (17, 17, 18); GRAY = (105, 101, 95); CREAM = (242, 238, 230)

def T(d, xy, t, font, fill, anchor='la', track=0): A.text(d, xy, t, font, fill, anchor, track)

# ---------- HUD moderno
def hud(c, idx, total, prog):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    m, gap, y = 40, 8, 54
    sw = (W - 2 * m - gap * (total - 1)) / total
    for k in range(total):
        x0 = m + k * (sw + gap)
        d.rounded_rectangle([x0, y, x0 + sw, y + 6], 3, fill=(0, 0, 0, 55))
        f = 1.0 if k < idx - 1 else (prog if k == idx - 1 else 0)
        if f > 0: d.rounded_rectangle([x0, y, x0 + max(6, sw * f), y + 6], 3, fill=(17, 17, 18, 235))
    c.paste(ov, (0, 0), ov); d = ImageDraw.Draw(c)
    lg = scaled(LOGO, h=34); c.paste(lg, (m, 92), lg)
    T(d, (m + lg.width + 18, 109), 'Anatomia da peça', F(INTER_M, 28), INK, 'lm')
    T(d, (W - m, 109), f'{idx:02d}/{total:02d}', F(MONO, 26), INK, 'rm', 2)

# ---------- rótulo em vidro
def glass(c, box, radius=34, tint=(255, 255, 255), a=0.62):
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, x1), min(H, y1)
    if x1 - x0 < 4 or y1 - y0 < 4: return
    reg = c.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(18))
    reg = Image.blend(reg, Image.new('RGB', reg.size, tint), a)
    mk = Image.new('L', reg.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1], radius, fill=255)
    c.paste(reg, (x0, y0), mk)
    ImageDraw.Draw(c).rounded_rectangle([x0, y0, x1 - 1, y1 - 1], radius, outline=(255, 255, 255), width=2)

def callout(c, t, pt, lab, num, title, sub):
    """t = segundos desde que este rótulo começou."""
    if t <= 0: return
    d = ImageDraw.Draw(c); x, y = pt
    # anel pulsando
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for ph in (0.0, 0.45):
        q = ((t + ph) % 0.9) / 0.9
        r = 16 + 54 * q; al = int(200 * (1 - q) * min(1, t / 0.2))
        od.ellipse([x - r, y - r, x + r, y + r], outline=(17, 17, 18, al), width=3)
    c.paste(ov, (0, 0), ov); d = ImageDraw.Draw(c)
    s = eo(seg(t, 0, 0.25)); r0 = 14 * s
    d.ellipse([x - r0 - 4, y - r0 - 4, x + r0 + 4, y + r0 + 4], fill=INK)
    if r0 > 4: d.ellipse([x - r0 + 3, y - r0 + 3, x + r0 - 3, y + r0 - 3], fill=(255, 255, 255))
    # rótulo
    ft, fs, fn = F(INTER_B, 42), F(INTER_M, 27), F(INTER_B, 26)
    tw = max(d.textlength(title, font=ft), d.textlength(sub, font=fs))
    bw, bh = tw + 140, 132
    lx, ly = lab
    # linha do ponto até a borda do rótulo
    ax = lx + (0 if x < lx else bw); ay = ly + bh / 2
    if x >= lx and x <= lx + bw: ax = x; ay = ly if y < ly else ly + bh
    q = eo(seg(t, 0.12, 0.42))
    if q > 0:
        ex, ey = x + (ax - x) * q, y + (ay - y) * q
        d.line([(x, y), (ex, ey)], fill=INK, width=3)
    p = eo(seg(t, 0.32, 0.62))
    if p > 0:
        dx = (1 - p) * 40 * (1 if lx > x else -1)
        bx, by = lx + dx, ly
        glass(c, (bx, by, bx + bw, by + bh), 34, a=0.55 + 0.1 * p)
        d = ImageDraw.Draw(c)
        cx0, cy0 = bx + 30, by + bh / 2
        d.ellipse([cx0, cy0 - 30, cx0 + 60, cy0 + 30], fill=INK)
        T(d, (cx0 + 30, cy0 + 1), f'{num:02d}', fn, (255, 255, 255), 'mm')
        al = seg(p, 0.3, 1)
        col = tuple(int(255 - (255 - v) * al) for v in INK); col2 = tuple(int(255 - (255 - v) * al) for v in GRAY)
        T(d, (cx0 + 84, by + 30), title, ft, col)
        T(d, (cx0 + 86, by + 84), sub, fs, col2)

# ---------- plano: (id, parte, início, dur-fonte, vel, cx, cy, larg, congela, zoom, [ (ponto, rótulo(x,y), título, sub) ])
SHOTS = [
    ('01', 7, 0.2, 2.2, 1.0, .50, .45, 1.00, 0.0, 1.0, []),
    ('02', 7, 2.6, 1.4, 0.8, .50, .50, 1.00, 3.2, 1.06, [((700, 70), (90, 1330), 'Embalagem zip', 'Fecha e reutiliza'),
                                                        ((850, 850), (90, 1490), 'Não é lixo. É bolsa.', 'Leve o que importa'),
                                                        ((230, 795), (90, 1650), 'O que você carrega?', '[X] O Espírito')]),
    ('03', 7, 18.3, 1.1, 0.5, .50, .50, 1.00, 0.0, 1.0, []),
    ('04', 6, 0.0, 1.6, 0.8, .50, .50, 1.00, 1.9, 1.08, [((900, 880), (90, 1500), 'Estampa costas', 'We carry the spirit.')]),
    ('05', 6, 10.6, 1.4, 0.8, .55, .38, .78, 1.9, 1.10, [((400, 830), (90, 1250), 'Frente', 'RUAH + sopro no peito')]),
    ('06', 6, 12.6, 1.4, 0.8, .62, .48, .70, 1.9, 1.10, [((465, 985), (90, 1380), 'Etiqueta na barra', 'Símbolo | RUAH')]),
    ('07', 6, 15.8, 1.4, 0.8, .51, .42, .75, 1.9, 1.08, [((390, 780), (430, 1250), 'Tag RUAH', 'We carry the spirit.')]),
    ('08', 6, 19.4, 1.1, 0.5, .42, .40, .70, 2.8, 1.06, [((350, 640), (300, 250), 'Gola canelada', 'Acabamento em ribana'),
                                                        ((200, 880), (330, 1450), 'Etiqueta estampada', 'Nada costurado no pescoço')]),
    ('09', 6, 30.0, 2.0, 0.85, .46, .55, .85, 2.0, 1.08, [((520, 1020), (90, 1620), 'Por dentro', '1 Coríntios 6:19 — só você vê')]),
]
TOTAL = len(SHOTS) + 1
NUMS = {}; k = 1
for sh in SHOTS:
    for j in range(len(sh[10])): NUMS[(sh[0], j)] = k; k += 1

def zoom_box(z, fx, fy):
    vw, vh = W / z, H / z
    x0 = min(max(fx - vw / 2, 0), W - vw); y0 = min(max(fy - vh / 2, 0), H - vh)
    return (x0, y0, x0 + vw, y0 + vh)

SFX = []   # (tempo, tipo)

def build(sh, fr, i, n_live, n_frz, tglob):
    sid, cos, zf = sh[0], sh[10], sh[9]; idx = int(sid)
    if i < n_live:
        t = i / FPS
        z = 1.0 + 0.03 * eio(i / max(1, n_live))
        base = Image.fromarray(fr[i]).resize((W, H), Image.BILINEAR, box=zoom_box(z, W / 2, H / 2))
        c = grade(base, i)
        prog = (i + 1) / (n_live + n_frz)
    else:
        k = i - n_live; t = k / FPS
        fx = np.mean([p[0][0] for p in cos]); fy = np.mean([p[0][1] for p in cos])
        z = 1.0 + (zf - 1.0) * eio(seg(t, 0, 0.5))
        box = zoom_box(z, fx, fy)
        base = Image.fromarray(fr[n_live - 1]).resize((W, H), Image.BILINEAR, box=box)
        c = grade(base, 0)
        # foco: desfoca e clareia o que está longe dos pontos
        f = eo(seg(t, 0.1, 0.5))
        if f > 0:
            bl = Image.blend(c.filter(ImageFilter.GaussianBlur(10)), Image.new('RGB', (W, H), CREAM), 0.18)
            mk = Image.new('L', (W, H), 255); md = ImageDraw.Draw(mk)
            for (pt, lab, ti, su) in cos:
                px, py = (pt[0] - box[0]) * z, (pt[1] - box[1]) * z
                md.ellipse([px - 300, py - 300, px + 300, py + 300], fill=0)
            mk = mk.filter(ImageFilter.GaussianBlur(90)).point(lambda v: int(v * f * 0.85))
            c.paste(bl, (0, 0), mk)
        if k < 3: c = Image.blend(c, Image.new('RGB', (W, H), (255, 255, 255)), 0.55 * (1 - k / 3))
        step = 0.9
        for j, (pt, lab, ti, su) in enumerate(cos):
            px, py = (pt[0] - box[0]) * z, (pt[1] - box[1]) * z
            callout(c, t - 0.35 - j * step, (px, py), lab, NUMS[(sid, j)], ti, su)
        prog = (i + 1) / (n_live + n_frz)
    # corte: leve deslize/blur de entrada
    if i < 4 and idx > 1:
        a = 1 - i / 4
        c = c.transform(c.size, Image.AFFINE, (1, 0, int(-60 * a * a), 0, 1, 0)).filter(ImageFilter.GaussianBlur(6 * a))
    hud(c, idx, TOTAL, prog)
    return c

def intro(c, t):
    p = seg(t, 0.15, 0.7)
    if p <= 0: return
    glass(c, (70, 1180, W - 70, 1180 + 420 * eo(p)), 44, a=0.6)
    d = ImageDraw.Draw(c)
    for k2, (w, y) in enumerate([('ANATOMIA', 1290), ('DA PEÇA', 1410)]):
        q = eo(seg(t, 0.3 + k2 * 0.15, 0.75 + k2 * 0.15))
        if q > 0:
            im = Image.new('RGBA', (W, 140), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
            T(dd, (W / 2, 70 + (1 - q) * 60), w, F(INTER_B, 118), INK, 'mm', 2)
            c.paste(im, (0, int(y - 70)), im)
    q = eo(seg(t, 0.9, 1.3))
    if q > 0:
        d = ImageDraw.Draw(c); chips = ['Drop 001', 'Off-white', 'Oversized']
        fx = F(INTER_M, 28); ws = [d.textlength(s, font=fx) + 44 for s in chips]; x = W / 2 - (sum(ws) + 16 * 2) / 2
        for s, w in zip(chips, ws):
            d.rounded_rectangle([x, 1500, x + w, 1552], 26, outline=INK, width=2)
            T(d, (x + w / 2, 1527), s, fx, INK, 'mm'); x += w + 16

def endcard(t, fi):
    c = grade(Image.new('RGB', (W, H), CREAM), fi); d = ImageDraw.Draw(c)
    s = scaled(SYM, h=int(230 * (1.08 - 0.08 * eo(seg(t, 0, 0.5))))); c.paste(s, (int(W / 2 - s.width / 2), 470), s)
    al = eo(seg(t, 0.15, 0.6))
    if al > 0:
        lg = scaled(LOGO, w=480); l2 = lg.copy(); l2.putalpha(l2.split()[3].point(lambda v: int(v * al)))
        c.paste(l2, (int(W / 2 - lg.width / 2), 760), l2)
    d = ImageDraw.Draw(c)
    for k2, (w, y) in enumerate([('Pré-venda', 1010), ('aberta.', 1115)]):
        q = eo(seg(t, 0.55 + k2 * 0.15, 0.95 + k2 * 0.15))
        if q > 0:
            im = Image.new('RGBA', (W, 130), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
            T(dd, (W / 2, 65 + (1 - q) * 55), w, F(INTER_B, 104), INK, 'mm')
            c.paste(im, (0, int(y - 65)), im)
    d = ImageDraw.Draw(c)
    if t > 1.2: T(d, (W / 2, 1225), 'Os 30 primeiros viram Founders.', F(CG, 58), GRAY, 'mm')
    p = seg(t, 1.6, 2.0)
    if p > 0:
        bw, bh = 470, 100; z = 1.1 - 0.1 * eo(p)
        d.rounded_rectangle([W / 2 - bw * z / 2, 1370 - bh * z / 2, W / 2 + bw * z / 2, 1370 + bh * z / 2], int(50 * z), fill=INK)
        T(d, (W / 2, 1370), 'Link na bio', F(INTER_B, int(40 * z)), (255, 255, 255), 'mm')
    if t > 2.0: T(d, (W / 2, 1475), 'useruah.com', F(INTER_M, 32), GRAY, 'mm')
    hud(c, TOTAL, TOTAL, min(1, t / 3.4))
    return c

# ---------- efeitos sonoros sintetizados (sem a voz da filmagem)
SR = 48000
def whoosh(d=0.32):
    n = int(SR * d); x = np.random.default_rng(1).normal(0, 1, n)
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    # filtro passa-faixa que sobe (aprox.: média móvel variável)
    out = np.zeros(n); acc = 0
    for i in range(n):
        a = 0.02 + 0.25 * i / n; acc += a * (x[i] - acc); out[i] = acc
    out = out - np.convolve(out, np.ones(40) / 40, 'same')
    return out * env * 0.9
def shutter():
    n = int(SR * 0.09); x = np.random.default_rng(2).normal(0, 1, n)
    env = np.exp(-np.linspace(0, 9, n)); click = x * env
    n2 = int(SR * 0.05); click2 = np.random.default_rng(3).normal(0, 1, n2) * np.exp(-np.linspace(0, 12, n2))
    out = np.zeros(int(SR * 0.16)); out[:n] += click * 0.5; out[int(SR * 0.07):int(SR * 0.07) + n2] += click2 * 0.4
    return out
def pop():
    n = int(SR * 0.12); tt = np.arange(n) / SR
    f = 900 + 500 * np.exp(-tt * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38) * 0.45

if __name__ == '__main__':
    mode = sys.argv[1]
    lens = [(int(round(sh[3] / sh[4] * FPS)), int(round(sh[8] * FPS))) for sh in SHOTS]
    END = int(3.6 * FPS)
    starts = np.cumsum([0] + [a + b for a, b in lens]).tolist()
    for k, sh in enumerate(SHOTS):
        if mode not in ('all', 'frames', sh[0]): continue
        fr = decode(sh[1], sh[2], sh[3], sh[4], sh[5], sh[6], sh[7])
        n_live = min(len(fr), lens[k][0]); n_frz = lens[k][1]
        if mode == 'frames':
            i = n_live + n_frz - 1 if n_frz else n_live - 1
            c = build(sh, fr, i, n_live, n_frz, 0)
            if sh[0] == '01': intro(c, 1.8)
            c.save(OUT + f'f_{sh[0]}.jpg', quality=84); continue
        tmp = OUT + f'_{sh[0]}.tmp.mp4'
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', tmp], stdin=subprocess.PIPE)
        # se faltar quadro na decodificação, completa congelando
        L = lens[k][0]
        for i in range(L + n_frz):
            ii = min(i, n_live - 1) if i < L else n_live + (i - L)
            c = build(sh, fr, ii, n_live, n_frz, 0)
            if sh[0] == '01': intro(c, i / FPS)
            p.stdin.write(c.tobytes())
        p.stdin.close(); p.wait(); os.replace(tmp, OUT + f'{sh[0]}.mp4'); print(sh[0], flush=True)
    if mode in ('all', 'frames', '10'):
        if mode == 'frames': endcard(2.8, 0).save(OUT + 'f_10.jpg', quality=84)
        else:
            p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                                  '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', OUT + '_10.tmp.mp4'], stdin=subprocess.PIPE)
            for i in range(END): p.stdin.write(endcard(i / FPS, i).tobytes())
            p.stdin.close(); p.wait(); os.replace(OUT + '_10.tmp.mp4', OUT + '10.mp4')
    if mode in ('all', 'sfx'):
        total = (starts[-1] + END) / FPS
        buf = np.zeros(int(SR * (total + 1)))
        def add(t, s):
            a = int(t * SR); buf[a:a + len(s)] += s[:len(buf) - a]
        wh, sh_, pp = whoosh(), shutter(), pop()
        for k, sh in enumerate(SHOTS):
            t0 = starts[k] / FPS
            if k > 0: add(max(0, t0 - 0.12), wh)
            if lens[k][1]:
                tf = (starts[k] + lens[k][0]) / FPS
                add(tf, sh_)
                for j in range(len(sh[10])): add(tf + 0.35 + j * 0.9 + 0.32, pp)
        add(starts[-1] / FPS - 0.12, wh)
        buf = np.clip(buf * 0.8, -1, 1)
        st = np.stack([buf, buf], 1)
        with wave.open(OUT + 'sfx.wav', 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
        print('sfx', total)
