"""CAOS INSANO · corte de live (formato 'react'): streamer em cima, gameplay embaixo, caixa de título neon, legenda
palavra a palavra (Whisper), crédito do criador na tela, @caosinsano.br. Áudio original da live (voz do streamer).
Uso: python3 corte.py <url_ou_arquivo> <inicio_s> <fim_s> "<TÍTULO>" "<crédito>" <saida.mp4> [cam=x,y,w,h]"""
import sys, os, json, subprocess, shutil, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); MOT = os.path.abspath(os.path.join(HERE, '../../../augusto/src/motion'))
def run(c): subprocess.run(c, check=True)
def main():
    src, ini, fim, titulo, cred, out = sys.argv[1:7]; ini, fim = float(ini), float(fim); dur = fim - ini
    cam = [int(v) for v in (sys.argv[7] if len(sys.argv) > 7 else '16,10,224,222').split(',')]
    tmp = tempfile.mkdtemp(prefix='corte_')
    run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(ini), '-t', f'{dur:.2f}', '-i', src, '-r', '30', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '192k', f'{tmp}/clip.mp4'])
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/clip.mp4', '-ac', '1', '-ar', '16000', f'{tmp}/a.wav'])
    from faster_whisper import WhisperModel
    m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
    import soundfile as sf
    aud, _sr = sf.read(f'{tmp}/a.wav', dtype='float32')
    segs, _ = m.transcribe(aud, language='pt', word_timestamps=True, vad_filter=True)
    words = [(w.start, w.end, w.word.strip()) for s in segs for w in s.words if w.word.strip()]
    caps = []
    for k in range(0, len(words), 3):
        g = words[k:k + 3]; caps.append([round(g[0][0], 2), round(g[-1][1] + .15, 2), ' '.join(x[2] for x in g).upper()])
    for k in range(len(caps) - 1): caps[k][1] = min(caps[k][1], caps[k + 1][0])
    html = open(os.path.join(HERE, 'overlay.html')).read().replace('__CAPS__', json.dumps(caps, ensure_ascii=False)) \
        .replace('__TITULO__', json.dumps(titulo, ensure_ascii=False)).replace('__CRED__', json.dumps(cred, ensure_ascii=False)).replace('__DUR__', f'{dur:.2f}')
    hp = os.path.join(HERE, f'_ov_{os.getpid()}.html'); open(hp, 'w').write(html)
    try: run(['node', os.path.join(MOT, 'formatos/render_alpha.js'), hp, f'{tmp}/ov', f'{dur:.2f}', '30'])
    finally: os.remove(hp)
    x, y, w, h = cam
    fc = (f"[0:v]split=3[a][b][c];"
          f"[a]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.25:saturation=1.2[bg];"
          f"[b]crop={w}:{h}:{x}:{y},scale=600:590,format=rgba[cam0];[cam0][2:v]alphamerge[cam];"
          f"[c]scale=-2:1000,crop=1080:1000[gp];"
          f"[bg][cam]overlay=240:70[t1];[t1][gp]overlay=0:820[t2];[t2][1:v]overlay=0:0:format=auto,format=yuv420p[v];"
          f"[0:a]loudnorm=I=-14:TP=-1.5,aresample=48000[au]")
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/clip.mp4', '-framerate', '30', '-i', f'{tmp}/ov/%04d.png', '-loop', '1', '-i', os.path.join(HERE, 'mask_cam.png'),
         '-filter_complex', fc, '-map', '[v]', '-map', '[au]', '-t', f'{dur:.2f}', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out])
    shutil.rmtree(tmp, ignore_errors=True); print('ok', out, round(dur, 1))
if __name__ == '__main__': main()
