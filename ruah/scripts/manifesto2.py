"""Manifesto v2 — cinético + cinematográfico. 9:16, ~33 s. Texto dentro da área segura dos Reels (≈260–1500)."""
import sys, os, math
SRC2 = open('/tmp/claude-0/-home-claude/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/scratchpad/video/cine2.py').read()
exec(SRC2.split("# ---------- cenas")[0])
OUT = SP + 'video/manif2/'; os.makedirs(OUT, exist_ok=True)
BAR = 110

# ---------- recursos cinéticos
def reveal_up(c, im, cx, cy, p, dist=None):
    """palavra sobe de dentro de uma máscara"""
    if p <= 0: return
    dist = dist or im.height
    e = eo(p); dy = (1 - e) * dist
    vis = Image.new('RGBA', im.size, (0, 0, 0, 0)); vis.paste(im, (0, int(dy)), im)
    c.paste(vis, (int(cx - im.width / 2), int(cy - im.height / 2)), vis)

def slam(c, im, cx, cy, p, z0=1.45, blur=16):
    """entra grande e desfocada e 'bate' no lugar"""
    if p <= 0: return
    e = eo(p); z = z0 - (z0 - 1) * e
    ii = im.resize((max(1, int(im.width * z)), max(1, int(im.height * z))), Image.BILINEAR)
    if p < 0.7 and blur: ii = ii.filter(ImageFilter.GaussianBlur(blur * (1 - p / 0.7)))
    paste_c(c, ii, cx, cy, min(1, p * 2.5))

def chroma(c, amt):
    """aberração cromática (separa R e B)"""
    if amt <= 0.02: return c
    k = int(14 * amt); r, g, b = c.split()
    r = r.transform(c.size, Image.AFFINE, (1, 0, -k, 0, 1, 0)); b = b.transform(c.size, Image.AFFINE, (1, 0, k, 0, 1, 0))
    return Image.merge('RGB', (r, g, b))

def zoom(c, z):
    if abs(z - 1) < 0.002: return c
    w, h = W / z, H / z
    return c.resize((W, H), Image.BILINEAR, box=((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2))

def punch(t, beats, amp=0.05, d=0.35):
    """zoom de impacto em cada batida"""
    z = 1.0
    for b in beats:
        if b <= t < b + d: z += amp * (1 - eo((t - b) / d))
    return z

def whip_in(c, t, d=0.16, dirn=1):
    if t < d:
        a = 1 - t / d; c = smear(c, a); c = c.transform(c.size, Image.AFFINE, (1, 0, int(dirn * W * 0.35 * a * a), 0, 1, 0))
        c = chroma(c, a)
    return c

def whip_out(c, t, dur, d=0.18):
    if t > dur - d:
        p = seg(t, dur - d, dur); c = smear(c, p); c = c.transform(c.size, Image.AFFINE, (1, 0, -int(W * 0.5 * p * p), 0, 1, 0))
        c = chroma(c, p)
    return c

def dark(c, a=0.32):
    return Image.blend(Image.new('RGB', (W, H), (8, 8, 9)), c, a)

def T(txt, font, fill=BONE, track=0, maxw=W - 110):
    return fit(text_img(txt, font, fill, track), maxw)

def shadow(c, im, cx, cy, a=1.0):
    sh = Image.new('RGBA', (im.width + 120, im.height + 120), (0, 0, 0, 0))
    blk = Image.new('RGBA', im.size, (0, 0, 0, 255)); blk.putalpha(im.split()[3]); sh.paste(blk, (60, 60), blk)
    sh = sh.filter(ImageFilter.GaussianBlur(20)); sh.putalpha(sh.split()[3].point(lambda v: min(255, int(v * 1.8 * a))))
    paste_c(c, sh, cx, cy + 6)

def post(c, fi, t, beats=(), dur=None, shade=0.0, hh=0.5, seed=0):
    c = zoom(c, punch(t, beats))
    c = handheld(c, t + seed, hh)
    c = finish(c, fi, shade=shade)
    return bars(c, 1.0)

# ---------- cenas
# A) ANTES DA ROUPA, existe o Espírito. (3.8 s)
def a(t, fi):
    c = blackbg(fi); c = fog(c, t, 0.18, 90)
    s = sc(SYM, h=1150); paste_c(c, s, W / 2, 900, 0.05 * eo(seg(t, 0, 1.5)))
    if t < 1.55:
        slam(c, T('ANTES', F('cinzel900', 200), BONE, 10), W / 2, 820, seg(t, 0.1, 0.45))
        slam(c, T('DA ROUPA,', F('cinzel900', 150), BONE, 8), W / 2, 1010, seg(t, 0.55, 0.9))
        if t > 1.35: c = Image.blend(c, blackbg(fi), seg(t, 1.35, 1.55))
    else:
        reveal_up(c, T('existe o', F('cg300i', 110)), W / 2, 780, seg(t, 1.6, 2.0))
        p = seg(t, 1.95, 2.7)
        slam(c, T('Espírito.', F('cg400i', 230), BONE, 0, W - 90), W / 2, 980, p, z0=1.25, blur=22)
        c = leak(c, seg(t, 2.0, 3.6), strength=0.38)
    c = whip_out(c, t, 3.8)
    return post(c, fi, t, beats=(0.1, 0.55, 1.95), seed=0)

# B) TUDO COMEÇOU COM UMA PALAVRA. -> רוח (4.2 s)
def b(t, fi):
    c = blackbg(fi); c = fog(c, t + 3, 0.22, 100)
    if t < 1.5:
        reveal_up(c, T('TUDO COMEÇOU', F('cinzel900', 110), BONE, 6), W / 2, 840, seg(t, 0.05, 0.4))
        reveal_up(c, T('COM UMA PALAVRA.', F('cinzel700', 76), MUT, 6), W / 2, 980, seg(t, 0.35, 0.7))
        if t > 1.25: c = Image.blend(c, blackbg(fi), seg(t, 1.25, 1.5))
    else:
        p = seg(t, 1.5, 2.4)
        heb = text_img('חור', F('heb500', 420), BONE)  # רוח
        z = 1.6 - 0.6 * eo(p); hb = heb.resize((int(heb.width * z), int(heb.height * z)), Image.BILINEAR)
        if p < 0.75: hb = hb.filter(ImageFilter.GaussianBlur(26 * (1 - p / 0.75)))
        paste_c(c, hb, W / 2, 880, min(1, p * 1.8))
        track_in(c, 'R U A C H', F('cinzel900', 70), W / 2, 1180, seg(t, 2.4, 3.0))
        track_in(c, 'SPIRIT  ·  BREATH  ·  WIND', F('cinzel700', 34), W / 2, 1275, seg(t, 2.8, 3.4), MUT)
        c = leak(c, seg(t, 1.6, 3.4), warm=(235, 225, 210), strength=0.3)
        c = chroma(c, 1 - seg(t, 1.5, 1.75))
    c = whip_out(c, t, 4.2)
    return post(c, fi, t, beats=(0.05, 0.35, 1.5), seed=3)

# C) SPIRIT / BREATH / WIND sobre o detalhe da RUACH (3.3 s, 3 batidas)
WORDS = [('SPIRIT', 'Espírito.'), ('BREATH', 'Sopro.'), ('WIND', 'Vento.')]
CD = 1.1
def cc(t, fi):
    i = min(2, int(t / CD)); lt = t - i * CD
    c = kb(AT + 'c7adeb74-image.png', t / (CD * 3), 1.22, 1.02, fy=0.5); c = dark(c, 0.26); c = fog(c, t, 0.14, 70)
    en, pt = WORDS[i]
    im = text_img(en, F('cinzel900', 230), BONE, int(40 - 30 * eo(lt / CD)))
    im = fit(im, W - 90)
    slam(c, im, W / 2, 860, seg(lt, 0, 0.3), z0=1.3, blur=12)
    reveal_up(c, T(pt, F('cg400i', 110)), W / 2, 1070, seg(lt, 0.2, 0.55))
    tag = T(' / '.join(w for w, _ in WORDS[:i + 1]), F('cinzel700', 30), MUT, 8)
    paste_c(c, tag, W / 2, 1380)
    c = whip_in(c, lt, 0.12, (-1) ** i) if i else c
    c = whip_out(c, t, CD * 3)
    return post(c, fi, t, beats=(0, CD, 2 * CD), seed=6)

# D) Propósito (4.4 s)
def d(t, fi):
    c = kb(AT + '80a353c2-image.png', t / 4.4, 1.0, 1.14, fy=0.55); c = dark(c, 0.34); c = fog(c, t, 0.1, 50)
    reveal_up(c, T('A RUAH NASCEU', F('cinzel900', 96), BONE, 6), W / 2, 620, seg(t, 0.1, 0.45))
    reveal_up(c, T('PARA LEVAR', F('cinzel700', 72), MUT, 8), W / 2, 740, seg(t, 0.45, 0.8))
    slam(c, T('uma mensagem', F('cg400i', 140)), W / 2, 880, seg(t, 0.8, 1.15))
    reveal_up(c, T('E ENCONTRAR', F('cinzel700', 72), MUT, 8), W / 2, 1030, seg(t, 1.4, 1.75))
    slam(c, T('pessoas.', F('cg400i', 170)), W / 2, 1170, seg(t, 1.75, 2.1))
    p = seg(t, 2.7, 3.2)
    if p > 0:
        ln = int(110 * eo(p)); ImageDraw.Draw(c).line([(W / 2 - ln, 1310), (W / 2 + ln, 1310)], fill=MUT, width=2)
        reveal_up(c, T('Até pelo que vestimos.', F('cg300i', 72)), W / 2, 1400, p)
    c = whip_in(c, t, 0.14)
    c = whip_out(c, t, 4.4)
    return post(c, fi, t, beats=(0.1, 0.8, 1.75), seed=9)

# E) Ezequiel 37:9 (4.0 s)
def e(t, fi):
    c = blackbg(fi); c = fog(c, t + 8, 0.28, 130)
    lines = [('Vem dos', 'cg300i', 96), ('QUATRO VENTOS,', 'cinzel900', 104), ('ó espírito,', 'cg400i', 120), ('e assopra', 'cg300i', 96), ('PARA QUE VIVAM.', 'cinzel900', 100)]
    y = 560
    for k, (ln, fn, sz) in enumerate(lines):
        im = T(ln, F(fn, sz), BONE, 6 if fn.startswith('cinzel') else 0)
        t0 = 0.1 + k * 0.38
        if fn.startswith('cinzel'): slam(c, im, W / 2, y, seg(t, t0, t0 + 0.3), z0=1.3, blur=10)
        else: reveal_up(c, im, W / 2, y, seg(t, t0, t0 + 0.35))
        y += im.height + 40
    track_in(c, 'EZEQUIEL 37:9', F('cinzel700', 32), W / 2, 1360, seg(t, 2.3, 2.9), MUT)
    c = leak(c, seg(t, 2.0, 3.9), strength=0.36)
    c = whip_out(c, t, 4.0)
    return post(c, fi, t, beats=(0.48, 1.62), seed=12)

# F) cortes nas costas: NÃO É / SOBRE O QUE / VESTIMOS. (4 x 0.62 s)
BACKS = [AT + 'e272e518-image.png', AT + '50b28577-image.png', AT + 'dbd14915-image.png', AT + '1e86452b-image.png']
FW = ['NÃO É', 'SOBRE', 'O QUE', 'VESTIMOS.']
SD = 0.62
def f_(t, fi):
    i = min(3, int(t / SD)); lt = t - i * SD
    ramp = 0.65 * eo(min(1, (lt / SD) / 0.25)) + 0.35 * (lt / SD)
    c = kb(BACKS[i], ramp, z0=1.16, z1=1.02, fy=0.42)
    c = whip_in(c, lt, 0.12, (-1) ** i)
    c = zoom(c, punch(lt, (0,), 0.06, 0.3)); c = handheld(c, t + 2, 0.9); c = finish(c, fi, shade=0.9)
    im = T(FW[i], F('cinzel900', 150 if i < 3 else 130), BONE, 8)
    shadow(c, im, W / 2, 1360); slam(c, im, W / 2, 1360, seg(lt, 0, 0.18), z0=1.35, blur=8)
    if lt < 0.05: c = Image.blend(c, Image.new('RGB', (W, H), (255, 255, 255)), 0.4 * (1 - lt / 0.05))
    return bars(c, 1.0)

# G) detalhes: É SOBRE O QUE CARREGAMOS. (3 x 0.85 s)
DETS = [AT + '8e3caba6-image.png', AT + '8e16ace4-image.png', AT + '2a89c5b5-image.png']
DD = 0.85
def g(t, fi):
    i = min(2, int(t / DD)); lt = t - i * DD
    c = kb(DETS[i], lt / DD, 1.18, 1.04, fy=0.5)
    c = whip_in(c, lt, 0.12, (-1) ** i) if i else c
    c = zoom(c, punch(lt, (0,), 0.05, 0.3)); c = handheld(c, t + 5, 0.9); c = finish(c, fi, shade=0.9)
    a1 = T('É SOBRE O QUE', F('cinzel700', 70), BONE, 10); shadow(c, a1, W / 2, 1250); paste_c(c, a1, W / 2, 1250)
    b1 = T('CARREGAMOS.', F('cinzel900', 140), BONE, 6); shadow(c, b1, W / 2, 1380)
    slam(c, b1, W / 2, 1380, seg(t, 0.05, 0.4) if i == 0 else 1)
    c = whip_out(c, t, DD * 3)
    return bars(c, 1.0)

# H) geração (3.6 s)
def h(t, fi):
    c = blackbg(fi); c = fog(c, t + 15, 0.18, 80)
    reveal_up(c, T('NÃO QUEREMOS UMA GERAÇÃO', F('cinzel700', 48), MUT, 6), W / 2, 560, seg(t, 0.05, 0.4))
    reveal_up(c, T('conhecida pela marca que usa.', F('cg300i', 76), MUT), W / 2, 660, seg(t, 0.3, 0.65))
    if t > 1.2:
        ImageDraw.Draw(c).line([(W / 2 - int(80 * eo(seg(t, 1.1, 1.4))), 780), (W / 2 + int(80 * eo(seg(t, 1.1, 1.4))), 780)], fill=MUT, width=2)
    slam(c, T('QUEREMOS UMA', F('cinzel900', 92), BONE, 6), W / 2, 900, seg(t, 1.3, 1.6))
    slam(c, T('GERAÇÃO', F('cinzel900', 190), BONE, 10), W / 2, 1060, seg(t, 1.6, 1.9), z0=1.5)
    reveal_up(c, T('conhecida pelo Espírito que carrega.', F('cg400i', 78)), W / 2, 1240, seg(t, 2.1, 2.5))
    c = leak(c, seg(t, 1.6, 3.4), strength=0.28)
    c = whip_out(c, t, 3.6)
    return post(c, fi, t, beats=(1.3, 1.6), seed=18)

# I) convite (5.0 s)
def i_(t, fi):
    c = blackbg(fi); c = fog(c, t, 0.17, 70)
    s = sc(SYM, h=1250); paste_c(c, s, W / 2, 900, 0.07 * eo(seg(t, 0, 1)))
    lg = sc(LOGO, w=int(420 * (1.15 - 0.15 * eo(seg(t, 0, 0.7))))); paste_c(c, lg, W / 2, 470, eo(seg(t, 0, 0.5)))
    track_in(c, 'UMA MARCA. UM MOVIMENTO.', F('cinzel700', 36), W / 2, 600, seg(t, 0.3, 0.9), MUT)
    slam(c, T('FAÇA', F('cinzel900', 200), BONE, 12), W / 2, 790, seg(t, 0.8, 1.1), z0=1.5)
    slam(c, T('PARTE.', F('cinzel900', 200), BONE, 12), W / 2, 980, seg(t, 1.1, 1.4), z0=1.5)
    p = seg(t, 1.7, 2.1)
    if p > 0:
        dd = ImageDraw.Draw(c); bw, bh = 600, 116; z = 1.15 - 0.15 * eo(p)
        x0, y0 = W / 2 - bw * z / 2, 1190 - bh * z / 2
        dd.rounded_rectangle([x0, y0, x0 + bw * z, y0 + bh * z], radius=int(58 * z), fill=BONE)
        paste_c(c, text_img('SIGA @RUAHWEAR_', F('cinzel900', int(42 * z)), (12, 12, 12), 4), W / 2, 1190)
    if t > 2.4:
        q = (t - 2.4) % 0.9 / 0.9; dd = ImageDraw.Draw(c); r = 8 + 40 * q
        dd.rounded_rectangle([W / 2 - 300 - r, 1132 - r, W / 2 + 300 + r, 1248 + r], radius=int(58 + r), outline=tuple(int(v * (1 - q)) for v in BONE), width=3)
    track_in(c, 'WE CARRY THE SPIRIT.', F('cinzel700', 30), W / 2, 1370, seg(t, 2.2, 2.8), MUT)
    c = leak(c, seg(t, 0.8, 2.6), strength=0.3)
    c = chroma(c, 1 - seg(t, 0, 0.2))
    return post(c, fi, t, beats=(0.8, 1.1), seed=11, hh=0.4)

SCENES = [('a', a, 3.8), ('b', b, 4.2), ('c', cc, CD * 3), ('d', d, 4.4), ('e', e, 4.0), ('f', f_, SD * 4), ('g', g, DD * 3), ('h', h, 3.6), ('i', i_, 5.0)]

if __name__ == '__main__':
    if sys.argv[1] == 'frames':
        S = dict((n, f) for n, f, dd in SCENES)
        for n, t in [('a', 0.8), ('a', 3.0), ('b', 3.2), ('c', 1.6), ('d', 3.4), ('e', 3.0), ('f', 2.2), ('g', 1.0), ('h', 2.8), ('i', 3.0)]:
            S[n](t, 0).save(OUT + f'f_{n}_{t}.jpg', quality=85)
    else:
        for n, f, dd in SCENES:
            if sys.argv[1] in ('all', n): render(n, f, dd)
