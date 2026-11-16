"""Mini-aula NARRADA (ElevenLabs) + trilha + efeitos sonoros sincronizados com o motion.
Uso: python3 narrar_aula.py <nome> <saida.mp4> [trilha.mp3]
  <nome> = chave de gen_aula.ARGS (ex.: desconto_salve). A fala de cada cena é a legenda da cena.
A chave da ElevenLabs é injetada pelo proxy do ambiente (nunca no código). Áudios ficam em cache por texto."""
import sys, os, re, json, hashlib, subprocess, contextlib, io
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE); sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import gen_aula as G
VOZ = '7lu3ze7orhWaNeSPowWx'  # Lucas (aprovado 16/11)
SFX = os.path.join(HERE, '../sfx'); CACHE = '/tmp/narr_cache'; os.makedirs(CACHE, exist_ok=True)
SR = 44100; LEAD = .25; PAD = .2; GAPF = .04; ASPD = 1.0  # animações no tempo normal (antes 1.25)
from narr_textos import NARR

def falar(txt):
    t = txt
    t = re.sub(r'R\$\s?(\d+),(\d\d)', lambda m: f"{m.group(1)} reais e {int(m.group(2))} centavos" if m.group(2) != '00' else f"{m.group(1)} reais", t)
    t = re.sub(r'R\$\s?([\d.]+)', lambda m: m.group(1) + ' reais', t)
    t = t.replace('÷', ' dividido por ').replace('−', ' menos ').replace(' - ', ' menos ').replace('×', ' vezes ')
    t = t.replace(' = ', ' é igual a ').replace(' (', ', ').replace('(', '').replace(')', '').replace('↓', '').replace('↗', '').replace('✓', '')
    t = re.sub(r'^(\d)\. ', r'\1: ', t)
    return re.sub(r'\s+', ' ', t).strip()

def tts(txt):
    h = hashlib.md5((VOZ + txt).encode()).hexdigest()[:12]; mp = f'{CACHE}/{h}.mp3'; wav = f'{CACHE}/{h}.wav'
    if not os.path.exists(wav):
        body = json.dumps({'text': txt, 'model_id': 'eleven_multilingual_v2',
                           'voice_settings': {'stability': .45, 'similarity_boost': .8, 'style': .25, 'use_speaker_boost': True, 'speed': 1.2}})
        code = subprocess.run(['curl', '-sS', '-m', '120', '-o', mp, '-w', '%{http_code}', '-X', 'POST',
                               f'https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128',
                               '-H', 'Content-Type: application/json', '-d', body], capture_output=True, text=True).stdout
        if code != '200': raise SystemExit(f'ElevenLabs {code}: {open(mp).read()[:300]}')
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', mp, '-ac', '1', '-ar', str(SR), wav], check=True)
    a, _ = sf.read(wav); a = a.astype(np.float32)
    nz = np.where(np.abs(a) > .01)[0]
    return a[max(0, nz[0] - 200):nz[-1] + 2000] if len(nz) else a

def load(n):
    w = f'{CACHE}/sfx_{n}.wav'
    if not os.path.exists(w): subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{SFX}/{n}.mp3', '-ac', '1', '-ar', str(SR), w], check=True)
    return sf.read(w)[0].astype(np.float32)

def eventos(js, real):
    """Efeitos dentro da cena: u = tempo da animação (lt/1.25) → segundos reais = u*1.25."""
    ev = []; U = lambda u: u * ASPD
    for m in re.finditer(r"W\(lt,\[(.*?)\]\],", js):
        for t0 in re.findall(r"\[\s*([\d.]+)\s*,\s*'", m.group(1) + ']'): ev.append((U(float(t0)), 'pop', .35))
    for m in re.finditer(r"head\(", js): pass
    if 'table(' in js or "tb(" in js or 'step:.22' in js:
        for m in re.finditer(r"t0:([\d.]+),step:([\d.]+).*?rows:\[(.*?)\]\}\)", js):
            t0, st = float(m.group(1)), float(m.group(2)); n = m.group(3).count("['")
            for i in range(n): ev.append((U(t0 + st * i), 'tick', .5))
            if 'hiLast' in js: ev.append((U(t0 + st * (n - 1)), 'pop', .5))
    if 'typer(' in js:
        m = re.search(r"typer\(lt,\{a:'([^']*)'(?:,wrong:'([^']*)')?.*?speed:(\d+)", js)
        sp = float(m.group(3)) if m else 30; n = len(m.group(1)) + len(m.group(2) or '') if m else 30
        ev.append((U(.05), 'typing', .45, U(n / sp)))
    if 'slider(' in js: ev.append((U(.3), 'swipe', .7))
    if 'liquid(' in js: ev.append((U(.3), 'riser', .45))
    if 'phone3d(' in js or 'notifs(' in js: ev.append((U(.4), 'pop', .5))
    if 'coins(' in js: ev.append((U(.1), 'coin', .6))
    for f, s in (('strike', 'impact'), ('stamp', 'stamp'), ('split', 'impact'), ('glass', 'glass')):
        for m in re.finditer(f + r"\(lt,([\d.]+)", js): ev.append((U(float(m.group(1))), s, .7))
    if 'font-size:320px' in js: ev.append((U(.5), 'impact', .8))
    if 'cta(' in js or 'ctaSave(' in js: ev.append((U(.6), 'chime', .6))
    return [e for e in ev if e[0] < real - .1]

def main():
    nome, out = sys.argv[1], sys.argv[2]
    trilha = sys.argv[3] if len(sys.argv) > 3 else '/tmp/claude-0/drive/mus/759.mp3'
    if nome in G.ARGS:
        th, kw, capcta, S = G.ARGS[nome]
        salve = nome.endswith('_salve')
        cenas = [(d, js, cap) for d, ty, js, cap in S] + [(2.0, "ctaSave(lt" if salve else "cta(lt", capcta)]
    else:  # Reel montado à mão (ex.: reel_aula_planilha_salve.html): lê as cenas do próprio HTML
        h = open(f'reel_aula_{nome}.html').read(); body = h[h.index('const SC=[') + 10:h.index('];', h.index('const SC=['))]
        cenas = [(float(b) - float(a), js, cap) for a, b, js, cap in re.findall(r"^\[([\d.]+),([\d.]+),'\w+',lt=>(.*),'([^']*)'\],?$", body, re.M)]
    falas = NARR.get(nome, [c for _, _, c in cenas])
    assert len(falas) == len(cenas), (len(falas), len(cenas))
    voz_parts, times, caps, sfx_ev, t = [], [], [], [], 0.0
    for i, ((d, js, cap), fala) in enumerate(zip(cenas, falas)):
        st = t; vt = t + (LEAD if i == 0 else .08)
        for fr in [f for f in re.split(r'(?<=[.?!])\s+', fala) if f.strip()]:
            a = tts(falar(fr)); voz_parts.append((vt, a)); caps.append([round(vt - .05, 3), 0, fr])
            vt += len(a) / SR; caps[-1][1] = round(vt + GAPF, 3); vt += GAPF
        dur = max(d * .9, (vt - st) + PAD)
        times.append([round(st, 3), round(st + dur, 3)])
        sfx_ev.append((st, 'impact' if i == 0 else 'whoosh', .55 if i else .7))
        for e in eventos(js, dur): sfx_ev.append((st + e[0],) + e[1:])
        t = st + dur
    for k in range(len(caps) - 1): caps[k][1] = max(caps[k][1], caps[k + 1][0])
    DUR = t + .3; times[-1][1] = round(DUR, 3); N = int(DUR * SR) + SR
    voz = np.zeros(N, np.float32); fx = np.zeros(N, np.float32)
    for st, a in voz_parts: i = int(st * SR); voz[i:i + len(a)] += a[:N - i]
    for e in sfx_ev:
        st, n, g = e[0], e[1], e[2]; a = load(n)
        if len(e) > 3: a = a[:int(e[3] * SR)]; a[-int(.08 * SR):] *= np.linspace(1, 0, int(.08 * SR))
        i = int(st * SR); fx[i:i + len(a)] += g * a[:N - i]
    tmp = f'/tmp/narr_{nome}'; os.makedirs(tmp, exist_ok=True)
    sf.write(f'{tmp}/voz.wav', voz[:int(DUR * SR)], SR); sf.write(f'{tmp}/fx.wav', fx[:int(DUR * SR)], SR)
    caps[-1][1] = round(DUR, 3)
    json.dump({'times': times, 'caps': caps, 'aspd': ASPD}, open(f'{tmp}/t.json', 'w'))
    # mix: voz em destaque, efeitos abaixo, trilha abafada sob a voz (sidechain) com fade
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/voz.wav', '-i', f'{tmp}/fx.wav', '-stream_loop', '-1', '-i', trilha, '-filter_complex',
        f"[2:a]atrim=0:{DUR:.2f},asetpts=PTS-STARTPTS,aformat=sample_rates={SR}:channel_layouts=mono,volume=0.22,afade=t=in:d=0.4,afade=t=out:st={DUR-1.5:.2f}:d=1.5[m];"
        f"[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=300[md];"
        f"[1:a]volume=0.55[f];[v1]volume=1.0[v];[v][f][md]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5,aformat=channel_layouts=stereo[a]",
        '-map', '[a]', '-ar', str(SR), f'{tmp}/mix.wav'], check=True)
    print('duração', round(DUR, 2), 'cenas', len(times))
    subprocess.run(['node', 'render_motion.js', f'reel_aula_{nome}.html', out, str(DUR), '30', f'{tmp}/t.json', f'{tmp}/mix.wav'], check=True)

if __name__ == '__main__': main()
