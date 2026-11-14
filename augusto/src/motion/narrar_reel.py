"""Gera narração por cena, monta o áudio e os tempos das cenas, e renderiza o Motion sincronizado.
Uso: python3 narrar_reel.py <motion.html> <saida.mp4> <voz> "fala 1" "fala 2" "fala 3" "fala 4" """
import sys, os, json, subprocess, numpy as np, soundfile as sf
html, out, voz, *falas = sys.argv[1:]
tmp = '/tmp/narr'; os.makedirs(tmp, exist_ok=True)
NAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../voz/narrar.py')
GAP, LEAD, TAIL = 0.12, 0.25, 0.9
parts, times, t = [], [], 0.0
for i, f in enumerate(falas):
    w = f'{tmp}/b{i}.wav'; subprocess.run(['python3', NAR, f, w, voz, '1.18'], check=True, stdout=subprocess.DEVNULL)
    a, sr = sf.read(w); a = np.trim_zeros(a, 'fb') if a.ndim == 1 else a
    start = t; t += (LEAD if i == 0 else 0)
    parts.append((t, a)); t += len(a) / sr + GAP
    times.append([round(start, 3), round(t if i < len(falas) - 1 else t + TAIL, 3)])
dur = times[-1][1]; mix = np.zeros(int(dur * sr) + sr)
for st, a in parts: mix[int(st * sr):int(st * sr) + len(a)] += a
sf.write(f'{tmp}/voz.wav', mix[:int(dur * sr)], sr); json.dump(times, open(f'{tmp}/t.json', 'w'))
print('tempos', times)
subprocess.run(['node', 'render_motion.js', html, out, str(dur), '30', f'{tmp}/t.json', f'{tmp}/voz.wav'], check=True)
