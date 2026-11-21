"""CAOS INSANO BR — Shorts com TAKES OFICIAIS do jogo (trailers e screenshots baixados da área de downloads oficial da Rockstar).
Overlay (neon + legenda) renderizado com fundo transparente e composto sobre os takes. Áudio original dos trailers NUNCA é usado.
Uso: python3 gen_takes.py <nome> <saida.mp4>"""
import sys, os, json, re, subprocess, shutil
import numpy as np, soundfile as sf
import gen_caos as G
NA = G.NA; HERE = G.HERE; MOT = G.MOT
BR = '/home/user/gta6_brutos'
V = {'T1': f'{BR}/GTAVI_Trailer_1_1080.mp4', 'T2': f'{BR}/GTAVI_Trailer_2_1080.mp4', 'L': f'{BR}/GTAVI_Launch_Trailer_1080.mp4', 'EL': f'{BR}/GTAVI_Extended_Look_1080.mp4'}
P = lambda reg, n: f'{BR}/shots/Places/{reg}/{reg.replace(" ", "_")}_{n:02d}.jpg'
# (fonte, início em s, posição horizontal do recorte 0–1)
BG = {
 'curiosidades1': [('T1', 3, .5), ('T1', 12, .5), ('L', 54, .55), ('T1', 9, .45), ('T1', 27, .5), ('T1', 30, .5), ('T2', 99, .5), ('T2', 6, .5), ('T1', 60, .4), ('L', 66, .5)],
 'curiosidades2': [('L', 69, .5), ('T2', 36, .5), ('L', 30, .5), ('T1', 3, .5), ('T2', 117, .6), ('T2', 141, .45), ('T1', 63, .5), ('T2', 66, .45), ('T2', 96, .45), ('T2', 153, .5)],
 'personagens': [('L', 39, .5), ('T1', 9, .45), ('L', 72, .45), ('T2', 18, .5), ('L', 12, .55), ('T2', 117, .6), ('L', 66, .5)],
 'mapa': [('T2', 6, .5), ('img', P('Vice City', 1), .5), ('img', P('Leonida Keys', 1), .5), ('img', P('Grassrivers', 1), .5), ('img', P('Port Gellhorn', 1), .5), ('img', P('Ambrosia', 1), .5), ('img', P('Mount Kalaga National Park', 1), .5), ('L', 66, .5)],
 'linha_do_tempo': [('T1', 3, .5), ('T1', 21, .5), ('T1', 27, .5), ('L', 18, .5), ('T2', 45, .5), ('L', 48, .5), ('T2', 6, .5), ('L', 66, .5)],
 'quiz': [('T1', 24, .5), ('T2', 6, .5), ('T2', 6, .5), ('T1', 9, .45), ('T1', 6, .45), ('T1', 12, .5), ('T2', 153, .5), ('L', 66, .5)],
}
E = lambda n: f'{BR}/ed/{n}'
import glob as _g
def ED(prefix): return sorted(_g.glob(f'{BR}/ed/{prefix}*'))[0]
BG.update({
 'vercetti': [('T2', 99, .5), ('img', ED('ULTIMATE_EDITION_HAWK_AND_LITTLE_MORGAN_REVOLVERS_01'), .5), ('img', ED('ULTIMATE_EDITION_WEAPON_VARIANTS_01'), .5), ('img', ED('VINTAGE_VICE_CITY_PACK_EXCLUSIVE_LOOKS_01'), .5), ('img', ED('VINTAGE_VICE_CITY_PACK_EXCLUSIVE_LOOKS_02'), .5), ('T2', 153, .5)],
 'ultimate': [('img', ED('ULTIMATE_EDITION_01'), .5), ('img', ED('ULTIMATE_EDITION_GROTTI_CHEETAH_01'), .5), ('img', ED('ULTIMATE_EDITION_VAPID_BUGGY_01'), .5), ('img', ED('ULTIMATE_EDITION_SQUALO_01'), .5), ('img', ED('ULTIMATE_EDITION_ELECTRIC_FANG_01'), .5), ('img', ED('ULTIMATE_EDITION_ONE_EYED_WILLIE_02'), .5), ('img', ED('ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_01'), .5), ('L', 66, .5), ('T2', 153, .5)],
 'bairros': [('T1', 12, .5), ('T1', 21, .5), ('img', ED('VINTAGE_VICE_CITY_PACK_VAPID_STANIER_01'), .5), ('img', ED('ULTIMATE_EDITION_STOCK_305_01'), .5), ('img', ED('ULTIMATE_EDITION_PTT_STORE_01'), .5), ('L', 69, .5), ('T2', 153, .5)],
 'macca': [('T2', 6, .5), ('img', ED('ULTIMATE_EDITION_GOODTIME_GEAR_01'), .5), ('T1', 18, .5), ('T1', 3, .5), ('img', P('Leonida Keys', 2), .5), ('L', 66, .5), ('T2', 153, .5)],
 'trilha': [('L', 54, .5), ('L', 48, .5), ('L', 60, .5), ('T2', 96, .45), ('T2', 153, .5), ('L', 66, .5), ('T2', 153, .5)],
 'preview': [('L', 69, .5), ('T2', 36, .5), ('L', 39, .5), ('L', 33, .5), ('T1', 30, .5), ('T2', 141, .45), ('L', 66, .5), ('T2', 153, .5)],
})
BG.update({
 'g_real': [('EL', 510, .5), ('EL', 524, .5), ('EL', 924, .5), ('EL', 964, .5), ('EL', 748, .5), ('EL', 988, .5)],
 'g_coisas': [('EL', 1032, .5), ('EL', 1028, .5), ('EL', 1044, .5), ('EL', 1116, .5), ('EL', 1228, .5), ('EL', 1172, .5), ('EL', 604, .5), ('EL', 1004, .5)],
 'g_tv': [('EL', 452, .5), ('EL', 452, .5), ('EL', 468, .5), ('EL', 476, .5), ('EL', 388, .5)],
 'g_loja': [('EL', 708, .5), ('EL', 704, .5), ('EL', 716, .5), ('EL', 909, .5), ('EL', 939, .5)],
 'g_aeroporto': [('EL', 1132, .5), ('EL', 1132, .5), ('EL', 1148, .5), ('EL', 1170, .5), ('EL', 1172, .5)],
 'g_volante': [('EL', 508, .5), ('EL', 516, .5), ('EL', 528, .5), ('EL', 756, .5), ('EL', 774, .5)],
})
BG.update({
 'd_ovo': [('EL', 1132, .5), ('EL', 1136, .5), ('T2', 6, .5), ('EL', 1172, .5), ('T2', 153, .5)],
 'd_capotado': [('EL', 964, .5), ('EL', 924, .5), ('EL', 1032, .5), ('EL', 508, .5), ('EL', 774, .5)],
 'd_gato': [('EL', 804, .5), ('EL', 808, .5), ('EL', 812, .5), ('EL', 820, .5), ('EL', 528, .5)],
 'd_animais': [('EL', 1044, .5), ('EL', 1032, .5), ('EL', 468, .5), ('img', P('Grassrivers', 2), .5), ('EL', 1116, .5)],
 'd_dicas': [('EL', 516, .5), ('EL', 744, .5), ('EL', 528, .5), ('EL', 1132, .5), ('EL', 756, .5)],
 'd_casa': [('EL', 1132, .5), ('img', P('Vice City', 1), .5), ('T1', 21, .5), ('T1', 3, .5), ('L', 66, .5)],
})
def main(trilha=None):
    nome, out = sys.argv[1], os.path.abspath(sys.argv[2]); trilha = trilha or os.path.join(HERE, '../trilhas/mk_173.mp3')
    beats, caps, voz, fx, t = [], [], [], [], 0.0
    for i, (b, fala) in enumerate(G.REELS[nome]):
        st = t; vt = t + (.2 if i == 0 else .08)
        for fr in [f for f in re.split(r'(?<=[.?!:])\s+', fala) if f.strip()]:
            a = NA.tts(NA.falar(fr)); voz.append((vt, a)); d = len(a) / NA.SR
            ws = fr.split(); tt = vt
            for k in range(0, len(ws), 4):
                c = ws[k:k + 4]; cd = d * len(c) / len(ws); caps.append([round(tt, 3), round(tt + cd, 3), ' '.join(c)]); tt += cd
            vt += d + .03
        dur = max(1.8, vt - st + .15); beats.append(dict(t0=round(st, 3), t1=round(st + dur, 3), **b))
        fx.append((st, 'whoosh' if i else 'impact', .5 if i else .7)); fx += [(st + d_, n, g) for d_, n, g in G.SFX.get(b['shot'], [])]
        t = st + dur
    DUR = t + .3; beats[-1]['t1'] = round(DUR, 3)
    for k in range(len(caps) - 1): caps[k][1] = max(caps[k][1], min(caps[k + 1][0], caps[k][1] + .3))
    tmp = f'/tmp/takes_{nome}'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="caos.css"><style>html,body,#v{{background:transparent!important}}</style></head><body><div id="v"></div>
<script>window.TAKES=1;const BEATS={json.dumps(beats, ensure_ascii=False)};window.CAPS={json.dumps(caps, ensure_ascii=False)};const DUR={DUR:.3f};function setTimes(){{}}</script>
<script src="caos_engine.js"></script><script>R(0)</script></body></html>'''
    hp = os.path.join(HERE, f'takes_{nome}.html'); open(hp, 'w').write(html)
    # fundo: um take por tela, recortado em 9:16 com leve aproximação
    segs = []
    for k, (b, (src, s0, x)) in enumerate(zip(beats, BG[nome])):
        d = b['t1'] - b['t0']; o = f'{tmp}/bg{k:02d}.mp4'
        z = f"scale=-2:2112,crop=1188:2112:(iw-1188)*{x}:0,zoompan=z='1+0.0009*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        if src == 'img':
            cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-loop', '1', '-t', f'{d:.3f}', '-i', s0, '-vf', z + ',eq=saturation=1.1', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', o]
        else:
            cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(s0), '-t', f'{d:.3f}', '-i', V[src], '-vf', z + ',eq=saturation=1.1', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', o]
        subprocess.run(cmd, check=True); segs.append(o)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'{tmp}/bg.mp4'], check=True)
    # áudio: voz + SFX + trilha (sem áudio dos trailers)
    SR = NA.SR; N = int(DUR * SR) + SR; Vv = np.zeros(N, np.float32); F = np.zeros(N, np.float32)
    for st, a in voz: i = int(st * SR); Vv[i:i + len(a)] += a[:N - i]
    for st, n, g in fx: a = NA.load(n); i = int(st * SR); F[i:i + len(a)] += g * a[:N - i]
    sf.write(f'{tmp}/voz.wav', Vv[:int(DUR * SR)], SR); sf.write(f'{tmp}/fx.wav', F[:int(DUR * SR)], SR)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/voz.wav', '-i', f'{tmp}/fx.wav', '-stream_loop', '-1', '-i', trilha, '-filter_complex',
        f"[2:a]atrim=0:{DUR:.2f},asetpts=PTS-STARTPTS,aformat=sample_rates={SR}:channel_layouts=mono,volume=0.3,afade=t=in:d=0.3,afade=t=out:st={DUR-1.5:.2f}:d=1.5[m];"
        f"[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=300[md];[1:a]volume=0.6[f];[v1][f][md]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5,aformat=channel_layouts=stereo[a]",
        '-map', '[a]', '-ar', str(SR), f'{tmp}/mix.wav'], check=True)
    subprocess.run(['node', os.path.join(MOT, 'formatos/render_alpha.js'), hp, f'{tmp}/ov', f'{DUR:.3f}', '30'], check=True, cwd=MOT)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/bg.mp4', '-framerate', '30', '-i', f'{tmp}/ov/%04d.png', '-i', f'{tmp}/mix.wav',
        '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]', '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    shutil.rmtree(tmp, ignore_errors=True); print('ok', out, round(DUR, 2))
if __name__ == '__main__': main()
