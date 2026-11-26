"""Reel @augustosilva.p · sistema do espetáculo (vídeos gravados pelo Augusto, 26/11).
Gancho (IMG_2859) → demonstração na tela (IMG_2860, só os trechos que mostram o que é falado) → fechamento (IMG_2862).
Corta as pausas longas entre palavras (jump cut), legenda palavra a palavra, etiqueta de cada parte, trilha baixa com
ducking sob a voz, cartão final "Salve e envie". Uso: python3 reel_seduca.py <pasta_brutos> <saida.mp4>"""
import sys, os, json, subprocess, tempfile, shutil, re
HERE = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(HERE, '../../..'))
MOT = os.path.join(RAIZ, 'augusto/src/motion')
TRILHA = os.path.join(RAIZ, 'gta6/trilhas/mk_131.mp3'); WHOOSH = os.path.join(RAIZ, 'augusto/src/sfx/whoosh.mp3')
# (arquivo, início, fim, etiqueta) — trechos conferidos na tela com a fala
EDL = [
    ('IMG_2859', 1.25, 8.95, ''),
    ('IMG_2860', 1.85, 13.8, '<b>01</b>O roteiro inteiro'),
    ('IMG_2860', 15.1, 24.4, '<b>02</b>Um botão: espaço'),
    ('IMG_2860', 31.0, 44.3, '<b>03</b>3 telões'),
    ('IMG_2860', 44.5, 57.3, '<b>04</b>TVs do auditório e do palco'),
    ('IMG_2860', 69.4, 80.4, '<b>05</b>Ao vivo: 1º take'),
    ('IMG_2860', 82.1, 93.9, '<b>06</b>Letra nos telões'),
    ('IMG_2860', 114.7, 123.2, '<b>07</b>Próxima música'),
    ('IMG_2862', 1.1, 31.2, ''),
]
FIX = {'Nutelão.': 'no telão.', 'prômpitos': 'prompts', 'certo,': 'certos,', 'por': 'pro'}
GAP, PAD, FIM = 0.45, 0.12, 2.8   # pausa máxima mantida, folga em volta das palavras, duração do cartão final
def run(c): subprocess.run(c, check=True)
def main():
    src, out = sys.argv[1], sys.argv[2]; tmp = tempfile.mkdtemp(prefix='seduca_')
    tr = {n: [w for s in json.load(open(f'{src}/{n}_tr.json')) for w in s['w']] for n in {e[0] for e in EDL}}
    partes, caps, chips, words_out, t = [], [], [], [], 0.0
    for n, a, b, chip in EDL:
        ws = [w for w in tr[n] if w[0] >= a - .05 and w[1] <= b + .3]
        # sub-trechos: quebra nas pausas maiores que GAP
        sub = []; ini = a
        for k in range(len(ws) - 1):
            if ws[k + 1][0] - ws[k][1] > GAP:
                sub.append((ini, ws[k][1] + PAD, )); ini = ws[k + 1][0] - PAD
        sub.append((ini, b))
        c0 = t
        for s0, s1 in sub:
            s0 = max(s0, a); s1 = min(s1, b)
            if s1 - s0 < .2: continue
            for w in ws:
                if w[0] >= s0 - .01 and w[0] < s1:
                    txt = w[2].strip(); txt = FIX.get(txt, txt) if not (n == 'IMG_2862' and txt == 'por') else txt
                    words_out.append((t + w[0] - s0, t + min(w[1], s1) - s0, txt))
            partes.append((n, s0, s1)); t += s1 - s0
        chips.append([round(c0, 2), round(t, 2), chip])
    total = t
    # legendas: até 3 palavras, quebra na pontuação
    g = []
    for w in words_out:
        g.append(w)
        if len(g) == 3 or re.search(r'[.,?!]$', w[2]):
            caps.append([round(g[0][0], 2), round(g[-1][1] + .1, 2), [x[2].rstrip(',.').upper() for x in g], [round(x[0], 2) for x in g]]); g = []
    if g: caps.append([round(g[0][0], 2), round(g[-1][1] + .1, 2), [x[2].rstrip(',.').upper() for x in g], [round(x[0], 2) for x in g]])
    for k in range(len(caps) - 1): caps[k][1] = min(caps[k][1], caps[k + 1][0])
    # vídeo: cada sub-trecho em 1080x1920/30 fps
    lst = open(f'{tmp}/l.txt', 'w')
    for i, (n, s0, s1) in enumerate(partes):
        p = f'{tmp}/p{i:03d}.mp4'
        run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{s0:.3f}', '-t', f'{s1 - s0:.3f}', '-i', f'{src}/{n}.MOV', '-vf', 'scale=1080:1920:flags=lanczos,fps=30,format=yuv420p',
             '-af', 'aresample=48000,loudnorm=I=-15:TP=-1.5', '-ac', '2', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-c:a', 'pcm_s16le', p.replace('.mp4', '.mov')])
        lst.write(f"file '{p.replace('.mp4', '.mov')}'\n")
    lst.close()
    run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'{tmp}/base.mov'])
    dur = total + FIM
    html = open(os.path.join(HERE, 'overlay.html')).read().replace('__CAPS__', json.dumps(caps, ensure_ascii=False)) \
        .replace('__CHIPS__', json.dumps(chips, ensure_ascii=False)).replace('__END__', f'{total:.2f}')
    hp = os.path.join(HERE, '_ov.html'); open(hp, 'w').write(html)
    try: run(['node', os.path.join(MOT, 'formatos/render_alpha.js'), hp, f'{tmp}/ov', f'{dur:.2f}', '30'])
    finally: os.remove(hp)
    # whoosh na entrada de cada etiqueta
    delays = [c[0] for c in chips[1:] if c[2]]
    fx = ''.join(f'[3:a]adelay={int(d*1000)}|{int(d*1000)},volume=0.35[w{i}];' for i, d in enumerate(delays))
    fc = (f"[0:v]tpad=stop_mode=clone:stop_duration={FIM}[v0];[v0][1:v]overlay=0:0:format=auto,format=yuv420p[v];"
          f"[0:a]apad=pad_dur={FIM}[voz];[voz]asplit[voz1][sc];"
          f"[2:a]volume=0.22,afade=t=out:st={dur - 1.5:.2f}:d=1.5[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];"
          f"{fx}[voz1][duck]{''.join(f'[w{i}]' for i in range(len(delays)))}amix=inputs={2 + len(delays)}:normalize=0,alimiter=limit=0.95[au]")
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/base.mov', '-framerate', '30', '-i', f'{tmp}/ov/%04d.png', '-stream_loop', '-1', '-i', TRILHA, '-i', WHOOSH,
         '-filter_complex', fc, '-map', '[v]', '-map', '[au]', '-t', f'{dur:.2f}', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-maxrate', '8M', '-bufsize', '16M',
         '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out])
    json.dump({'caps': caps, 'chips': chips, 'total': total}, open(out.replace('.mp4', '_edl.json'), 'w'), ensure_ascii=False, indent=1)
    shutil.rmtree(tmp, ignore_errors=True); print('ok', out, round(dur, 1))
if __name__ == '__main__': main()
