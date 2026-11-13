"""ANATOMIA DA PEÇA — estilo ficha técnica, claro. Congela em cada detalhe e aponta com marcador numerado.
Som original da filmagem (zíper, saco, tecido) + trilha baixa."""
import sys, os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SP = '/tmp/claude-0/-home-claude/73b1cb2e-93fc-5da2-a2e0-61df8ac8c3ef/scratchpad/'
OUT = SP + 'video/anat/'; os.makedirs(OUT, exist_ok=True)
U = '/mnt/user-data/uploads/IMG_1860_'
W, H, FPS = 1080, 1920, 30
SW, SH = 2160, 3840
INK = (18, 18, 19); CREAM = (240, 236, 228); MID = (120, 115, 108)
def F(p, s): return ImageFont.truetype(p, int(s))
INTER_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
INTER_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
INTER_L = '/usr/share/fonts/opentype/inter/Inter-Light.otf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
CIN = SP + 'ttf/cinzel900.ttf'; CG = SP + 'ttf/cg400i.ttf'
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def seg(t, a, b): return clamp((t - a) / (b - a))
def load_rgba(p):
    im = Image.open(p).convert('RGBA'); return im.crop(im.getbbox())
LOGO = load_rgba(SP + 'kit/marca/logo-preto.png'); SYM = load_rgba(SP + 'kit/marca/simbolo-preto.png')
def scaled(im, w=None, h=None):
    if h: return im.resize((max(1, int(im.width * h / im.height)), int(h)), Image.LANCZOS)
    return im.resize((int(w), max(1, int(im.height * w / im.width))), Image.LANCZOS)

# grade clara (high-key, levemente dessaturado) + grão fino
GRN = [np.random.default_rng(i).normal(0, 3.2, (H, W, 1)) for i in range(4)]
def grade(im, fi):
    a = np.asarray(im).astype(np.float32)
    g = a.mean(2, keepdims=True); a = g + (a - g) * 0.82          # dessatura
    a = a * 1.04 + 6                                                # levanta
    a = a * np.array([1.0, 0.995, 0.975])                           # creme
    a = a + GRN[fi % 4]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def text(d, xy, t, font, fill=INK, anchor='la', track=0):
    if not track: d.text(xy, t, font=font, fill=fill, anchor=anchor); return
    x, y = xy; ws = [d.textlength(ch, font=font) for ch in t]; tw = sum(ws) + track * (len(t) - 1)
    if anchor[0] == 'm': x -= tw / 2
    elif anchor[0] == 'r': x -= tw
    for ch, w in zip(t, ws): d.text((x, y), ch, font=font, fill=fill, anchor='l' + anchor[1]); x += w + track

# HUD de ficha técnica: moldura fina, cantos, cabeçalho, contador
def hud(c, idx, total, t_glob):
    d = ImageDraw.Draw(c)
    m = 46
    d.rectangle([m, m, W - m, H - m], outline=(255, 255, 255), width=2)
    for (x, y, sx, sy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line([(x, y), (x + 40 * sx, y)], fill=INK, width=4); d.line([(x, y), (x, y + 40 * sy)], fill=INK, width=4)
    # faixas do cabeçalho e rodapé (fundo creme translúcido)
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rectangle([m + 2, m + 2, W - m - 2, m + 92], fill=CREAM + (225,))
    od.rectangle([m + 2, H - m - 92, W - m - 2, H - m - 2], fill=CREAM + (225,))
    c.paste(ov, (0, 0), ov); d = ImageDraw.Draw(c)
    text(d, (m + 28, m + 47), 'RUAH — ANATOMIA DA PEÇA', F(MONO, 24), INK, 'lm', 2)
    text(d, (W - m - 28, m + 47), 'DROP 001', F(MONO, 24), INK, 'rm', 2)
    text(d, (m + 28, H - m - 47), 'WE CARRY THE SPIRIT.', F(MONO, 22), MID, 'lm', 2)
    text(d, (W - m - 28, H - m - 47), f'{idx:02d} / {total:02d}', F(MONO, 26), INK, 'rm', 2)
    # barra de progresso
    d.line([(m + 2, H - m - 93), (m + 2 + (W - 2 * m - 4) * t_glob, H - m - 93)], fill=INK, width=3)

def callout(c, p, pt, lab, num, title, sub=None, side='r'):
    """círculo desenha em volta do ponto, linha em cotovelo até a etiqueta, texto revela."""
    if p <= 0: return
    d = ImageDraw.Draw(c)
    x, y = pt; r = 46
    a = eo(seg(p, 0, 0.35)) * 360
    d.arc([x - r, y - r, x + r, y + r], -90, -90 + a, fill=INK, width=5)
    d.arc([x - r - 1, y - r - 1, x + r + 1, y + r + 1], -90, -90 + a, fill=(255, 255, 255), width=1)
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=INK)
    lx, ly = lab
    q = eo(seg(p, 0.25, 0.6))
    if q > 0:
        sx = x + (r if lx > x else -r) * 0.0
        sy = y
        ex = sx + (lx - sx) * q; mid = (lx, ly)
        # cotovelo: horizontal até lx depois vertical até ly
        p1 = (sx + (lx - sx) * min(1, q * 2), sy)
        d.line([(x + (r if lx > x else -r), y), p1], fill=INK, width=3)
        if q > 0.5:
            yy = sy + (ly - sy) * ((q - 0.5) * 2)
            d.line([(lx, sy), (lx, yy)], fill=INK, width=3)
    s = eo(seg(p, 0.55, 0.9))
    if s > 0:
        # etiqueta: caixa creme com número em preto
        ft = F(INTER_B, 44); fs = F(INTER_M, 28); fn = F(MONO, 26)
        tw = max(d.textlength(title, font=ft), d.textlength(sub or '', font=fs)) + 60
        bh = 150 if sub else 104
        bx = lx - tw / 2 if side == 'c' else (lx if side == 'r' else lx - tw)
        by = ly
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rectangle([bx, by, bx + tw * s, by + bh], fill=CREAM + (245,))
        c.paste(ov, (0, 0), ov); d = ImageDraw.Draw(c)
        d.rectangle([bx, by, bx + tw * s, by + bh], outline=INK, width=3)
        if s > 0.6:
            al = seg(s, 0.6, 1)
            col = tuple(int(240 - (240 - v) * al) for v in INK)
            text(d, (bx + 30, by + 26), f'{num:02d}', fn, MID if al > 0.5 else CREAM, 'la', 2)
            text(d, (bx + 30, by + 56), title, ft, col, 'la')
            if sub: text(d, (bx + 30, by + 112), sub, fs, tuple(int(240 - (240 - v) * al) for v in MID), 'la')

def decode(part, t0, dur, speed, cx, cy, w):
    bw, bh = int(SW * w) // 2 * 2, int(SH * w) // 2 * 2
    x = int(min(max(cx * SW - bw / 2, 0), SW - bw)); y = int(min(max(cy * SH - bh / 2, 0), SH - bh))
    vf = f'crop={bw}:{bh}:{x}:{y},scale={W}:{H}:flags=lanczos,setpts={1 / speed:.4f}*PTS,fps=30'
    pr = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(t0), '-t', str(dur), '-i', U + f'{part}.mov', '-an', '-vf', vf,
                         '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(pr.stdout, np.uint8).reshape(-1, H, W, 3)

def audio(part, t0, dur, speed, outwav):
    af = f'atempo={speed}' if speed >= 0.5 else f'atempo=0.5,atempo={speed / 0.5}'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t0), '-t', str(dur), '-i', U + f'{part}.mov', '-vn', '-af', af + ',aresample=48000',
                    '-ac', '2', outwav], check=True)

# ---------- plano: (id, parte, início, duração-fonte, velocidade, cx, cy, largura, congela(s), [callouts])
# callout: (ponto, etiqueta, título, sub, lado)
SHOTS = [
    ('01', 7, 0.2, 2.2, 1.0, 0.50, 0.45, 1.00, 0.0, []),
    ('02', 7, 2.6, 1.4, 0.8, 0.50, 0.42, 0.92, 2.2, [((560, 430), (560, 1150), 'Embalagem zip', 'Reutilizável. Não é lixo, é bolsa.', 'c'),
                                                     ((300, 880), (120, 1380), 'O que você carrega?', '[X] O Espírito.', 'r')]),
    ('03', 7, 18.3, 1.1, 0.5, 0.50, 0.50, 1.00, 0.0, []),
    ('04', 6, 0.0, 1.6, 0.8, 0.50, 0.50, 1.00, 1.8, [((560, 820), (140, 1300), 'Estampa costas', 'We carry the spirit. · DTF', 'r')]),
    ('05', 6, 10.6, 1.4, 0.8, 0.55, 0.38, 0.78, 1.8, [((560, 830), (140, 1150), 'Frente', 'RUAH + sopro no peito', 'r')]),
    ('06', 6, 12.6, 1.4, 0.8, 0.62, 0.48, 0.70, 1.8, [((470, 890), (140, 1250), 'Etiqueta na barra', 'Símbolo | RUAH', 'r')]),
    ('07', 6, 15.8, 1.4, 0.8, 0.51, 0.42, 0.75, 1.8, [((560, 820), (140, 1350), 'Tag RUAH', 'We carry the spirit.', 'r')]),
    ('08', 6, 19.4, 1.1, 0.5, 0.42, 0.40, 0.70, 2.4, [((680, 620), (140, 1180), 'Gola canelada', 'Ribana encorpada', 'r'),
                                                     ((330, 960), (140, 1400), 'Etiqueta estampada', 'Sem etiqueta costurada no pescoço', 'r')]),
    ('09', 6, 30.0, 2.0, 0.85, 0.46, 0.55, 0.85, 2.2, [((650, 920), (140, 1330), 'Por dentro', '1 Coríntios 6:19 — só você vê.', 'r')]),
]
TOTAL = len(SHOTS)

def shot_frames(sh):
    sid, part, t0, dsrc, sp, cx, cy, w, frz, cos = sh
    fr = decode(part, t0, dsrc, sp, cx, cy, w)
    return fr

def build_frame(sh, fr, i, n_live, n_frz, gstart, gtot):
    sid = sh[0]; cos = sh[9]; idx = int(sid)
    t_glob = clamp((gstart + i) / gtot)
    if i < n_live:
        t = i / FPS
        z = 1.0 + 0.04 * eio(i / max(1, n_live))
        base = Image.fromarray(fr[i])
        if z > 1:
            vw, vh = W / z, H / z
            base = base.resize((W, H), Image.BILINEAR, box=((W - vw) / 2, (H - vh) / 2, (W + vw) / 2, (H + vh) / 2))
        c = grade(base, i)
        # entrada: corte seco com leve flash branco
        if i < 2 and idx > 1: c = Image.blend(c, Image.new('RGB', (W, H), (255, 255, 255)), 0.5 - 0.25 * i)
    else:
        k = i - n_live; t = k / FPS
        base = Image.fromarray(fr[n_live - 1])
        vw, vh = W / 1.04, H / 1.04
        base = base.resize((W, H), Image.BILINEAR, box=((W - vw) / 2, (H - vh) / 2, (W + vw) / 2, (H + vh) / 2))
        c = grade(base, 0)
        if k < 3: c = Image.blend(c, Image.new('RGB', (W, H), (255, 255, 255)), 0.6 * (1 - k / 3))   # "foto"
        # véu leve para destacar as marcações
        c = Image.blend(c, Image.new('RGB', (W, H), CREAM), 0.12 * eo(seg(t, 0, 0.3)))
        step = (n_frz / FPS - 0.4) / max(1, len(cos))
        for j, (pt, lab, ti, su, side) in enumerate(cos):
            callout(c, seg(t, 0.15 + j * step * 0.85, 0.15 + j * step * 0.85 + 1.0), pt, lab, sum(len(s[9]) for s in SHOTS[:idx - 1]) + j + 1, ti, su, side)
    hud(c, idx, TOTAL, t_glob)
    return c

def intro_overlay(c, t):
    d = ImageDraw.Draw(c)
    p = seg(t, 0.2, 0.8)
    if p > 0:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rectangle([90, 1240, W - 90, 1560], fill=CREAM + (int(235 * eo(p)),)); c.paste(ov, (0, 0), ov); d = ImageDraw.Draw(c)
        text(d, (W / 2, 1310), 'ANATOMIA', F(INTER_B, 120), INK, 'mm', int(4 + 26 * (1 - eo(p))))
        text(d, (W / 2, 1420), 'DA PEÇA', F(INTER_B, 120), INK, 'mm', int(4 + 26 * (1 - eo(seg(t, 0.4, 1.0)))))
        q = seg(t, 0.9, 1.3)
        if q > 0: text(d, (W / 2, 1515), 'RUAH 001 — CARRY · OFF-WHITE', F(MONO, 26), MID, 'mm', 3)

def endcard(t, fi):
    c = Image.new('RGB', (W, H), CREAM); c = grade(c, fi); d = ImageDraw.Draw(c)
    # grade de ficha técnica
    for gx in range(90, W, 90): d.line([(gx, 0), (gx, H)], fill=(228, 223, 214), width=1)
    for gy in range(90, H, 90): d.line([(0, gy), (W, gy)], fill=(228, 223, 214), width=1)
    s = scaled(SYM, h=int(260 * (1.1 - 0.1 * eo(seg(t, 0, 0.6))))); c.paste(s, (int(W / 2 - s.width / 2), 430), s)
    lg = scaled(LOGO, w=520); al = eo(seg(t, 0.2, 0.7))
    if al > 0:
        l2 = lg.copy(); l2.putalpha(l2.split()[3].point(lambda v: int(v * al))); c.paste(l2, (int(W / 2 - lg.width / 2), 760), l2)
    d = ImageDraw.Draw(c)
    if t > 0.7: text(d, (W / 2, 1020), 'PRÉ-VENDA ABERTA', F(INTER_B, 78), INK, 'mm', int(2 + 20 * (1 - eo(seg(t, 0.7, 1.2)))))
    if t > 1.2: text(d, (W / 2, 1110), 'Os 30 primeiros viram Founders.', F(CG, 62), MID, 'mm')
    p = seg(t, 1.6, 2.0)
    if p > 0:
        bw, bh = 560, 104; z = 1.12 - 0.12 * eo(p)
        d.rectangle([W / 2 - bw * z / 2, 1260 - bh * z / 2, W / 2 + bw * z / 2, 1260 + bh * z / 2], fill=INK)
        text(d, (W / 2, 1260), 'LINK NA BIO', F(INTER_B, int(42 * z)), CREAM, 'mm', 6)
    if t > 2.0: text(d, (W / 2, 1360), 'USERUAH.COM', F(MONO, 30), MID, 'mm', 6)
    hud(c, TOTAL, TOTAL, 1.0)
    return c

def enc(name):
    tmp = OUT + f'_{name}.tmp.mp4'
    return tmp, subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                                  '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', tmp], stdin=subprocess.PIPE)

if __name__ == '__main__':
    mode = sys.argv[1]
    # duração global para a barra de progresso
    lens = []
    for sh in SHOTS:
        n_live = int(round(sh[3] / sh[4] * FPS)); lens.append((n_live, int(round(sh[8] * FPS))))
    END = int(3.4 * FPS)
    gtot = sum(a + b for a, b in lens) + END
    starts = np.cumsum([0] + [a + b for a, b in lens]).tolist()
    for k, sh in enumerate(SHOTS):
        if mode not in ('all', 'frames', sh[0]): continue
        fr = shot_frames(sh); n_live = min(len(fr), lens[k][0]); n_frz = lens[k][1]
        if mode == 'frames':
            i = n_live + n_frz - 1 if n_frz else n_live // 2
            c = build_frame(sh, fr, i, n_live, n_frz, starts[k], gtot)
            if sh[0] == '01': intro_overlay(c, 1.6)
            c.save(OUT + f'f_{sh[0]}.jpg', quality=82); continue
        tmp, p = enc(sh[0])
        for i in range(n_live + n_frz):
            c = build_frame(sh, fr, i, n_live, n_frz, starts[k], gtot)
            if sh[0] == '01': intro_overlay(c, i / FPS)
            p.stdin.write(c.tobytes())
        p.stdin.close(); p.wait(); os.replace(tmp, OUT + f'{sh[0]}.mp4')
        # som: original na parte viva + silêncio no congelado
        audio(sh[6 - 5] if False else sh[1], sh[2], sh[3], sh[4], OUT + f'{sh[0]}_live.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', OUT + f'{sh[0]}_live.wav', '-af', f'apad=whole_dur={(n_live + n_frz) / FPS:.3f},atrim=0:{(n_live + n_frz) / FPS:.3f}',
                        OUT + f'{sh[0]}.wav'], check=True)
        print(sh[0], (n_live + n_frz) / FPS, flush=True)
    if mode in ('all', 'frames', '10'):
        if mode == 'frames': endcard(2.6, 0).save(OUT + 'f_10.jpg', quality=82)
        else:
            tmp, p = enc('10')
            for i in range(END): p.stdin.write(endcard(i / FPS, i).tobytes())
            p.stdin.close(); p.wait(); os.replace(tmp, OUT + '10.mp4')
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=stereo', '-t', f'{END / FPS:.3f}', OUT + '10.wav'], check=True)
