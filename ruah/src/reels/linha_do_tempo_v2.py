"""RUAH · Reel "Linha do tempo das camisetas" — v2 (27/11: v1 reprovada: "visual amador, texto ruim, áudio/trilha").
v2: tratamento de cor de filme + vinheta + grão, zoom lento em cada trecho, cartão grande por capítulo (Nº + nome),
linha do tempo com pontos embaixo, legenda maior (Cormorant 700) na parte de baixo, closes OFICIAIS das 4 estampas
no Drop 01, cortes de fala só nas pausas longas (com fade de 25 ms), trilha própria de 3 min (ElevenLabs, sem loop).
Base original (vídeo gravado pelo Augusto em 26/11, IMG_2863).
O bruto veio ESPELHADO (câmera frontal): o vídeo é desespelhado (hflip) para as estampas lerem certo.
Trechos escolhidos por frase; pausas longas cortadas; legenda frase a frase (corrigida à mão — o Whisper errou nomes
como RUAH/Faith/Isaías 54:10/Jeremias 29:11); etiqueta de cada fase no topo; trilha RUAH baixa com ducking; cartão final.
Fora do corte (afirmação NOVA, precisa de aprovação): "a qualidade é infinitamente superior" (225–246 s) e
"tecido de gramatura alta" (128–133 s). Uso: python3 linha_do_tempo.py <IMG_2863.MOV> <IMG_2863_tr.json> <saida.mp4>"""
import sys, os, json, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(HERE, '../../..'))
REND = os.path.join(RAIZ, 'augusto/src/motion/formatos/render_alpha.js'); TRILHA = os.path.join(RAIZ, 'ruah/videos/RUAH_trilha_linha_do_tempo.mp3')
FOTOS = [os.path.join(RAIZ, 'ruah/fotos_produtos', f) for f in ('01_RUACH/01_5_detalhe.jpg', '02_WE_CARRY_THE_SPIRIT/02_5_detalhe.jpg', '03_INVISIVEL_MOVE/03_5_detalhe.jpg', '04_WHAT_DO_YOU_CARRY/04_5_detalhe.jpg')]
# (início, fim, (rótulo, nome) da fase ou None, [(ini, fim, legenda)] em tempo do bruto)
EDL = [
 (7.3, 17.4, None, [(7.3, 9.4, 'Hoje eu quero contar um pouquinho da história.'), (10.0, 13.0, 'Separei a linha do tempo das camisetas que eu já fiz…'), (13.0, 17.4, '…e quero explicar um pouquinho de cada uma.')]),
 (18.0, 27.0, ('2021 · 2022', 'Nº 02', 'Faith'), [(18.0, 22.6, 'Essa foi a segunda camiseta que eu fiz.'), (23.1, 27.0, 'A primeira tinha uma rosa na frente.')]),
 (28.3, 35.4, ('2021 · 2022', 'Nº 02', 'Faith'), [(28.3, 30.8, 'Já está bem velhinha.'), (31.7, 35.4, 'Fiz lá por 2021, 2022.')]),
 (37.9, 43.8, ('2021 · 2022', 'Nº 02', 'Faith'), [(37.9, 41.8, 'Como vocês podem ver, o nome ainda não era RUAH.'), (41.9, 43.8, 'O nome era Faith.')]),
 (55.2, 64.0, ('2021 · 2022', 'Nº 02', 'Faith'), [(55.2, 60.9, 'Ela ainda era longline, com esse arco embaixo…'), (60.9, 64.0, '…que na época eu achava feio, mas eu estava testando.')]),
 (67.9, 82.7, ('Ainda Faith', 'Nº 03', 'Passion'), [(67.9, 75.6, 'Depois eu fiz essa, ainda da Faith, com os corações de chamas.'), (76.5, 82.7, 'E tinha essa frase: “Passion ignites our purpose”.')]),
 (89.2, 94.1, ('Ainda Faith', 'Nº 03', 'Passion'), [(89.2, 94.1, 'Essa foi a terceira camiseta que eu fiz, ainda como Faith.')]),
 (98.0, 112.3, ('O nome muda', 'Nº 04', 'RUAH'), [(98.0, 101.8, 'E aqui já como RUAH. Já é uma oversized.'), (102.3, 106.3, 'Eu ainda fazia como private label:'), (107.0, 112.3, 'a camiseta já vinha pronta, num saquinho de TNT.')]),
 (118.7, 124.1, ('O nome muda', 'Nº 04', 'RUAH'), [(118.7, 124.1, 'Aqui já vinha com o meu logo. Esse era o logo antigo.')]),
 (133.7, 144.9, ('O nome muda', 'Nº 04', 'RUAH'), [(133.7, 137.9, 'Mas eu não gostei muito da estampa. Era DTG,'), (138.8, 144.9, 'impressa direto na camiseta, e ficou meio falhadinha.')]),
 (156.6, 165.0, ('O nome muda', 'Nº 04', 'RUAH'), [(156.6, 160.3, 'E aqui nas costas: “Inabalável”.'), (161.4, 165.0, 'Isaías 54:10, que eu desenhei nas costas.')]),
 (167.8, 173.4, ('Jeremias 29:11', 'Nº 05', 'Peace Plan'), [(167.8, 173.4, 'E essa eu fiz no mesmo lugar, já como RUAH.')]),
 (180.0, 195.5, ('Jeremias 29:11', 'Nº 05', 'Peace Plan'), [(180.0, 185.9, 'Peace Plan. Jeremias 29:11:'), (186.0, 188.6, '“Só eu sei os pensamentos que tenho a vosso respeito.”'), (189.5, 195.5, 'Foi uma das últimas que eu fiz como RUAH. Ficou bonita também.')]),
 (201.5, 209.9, ('Jeremias 29:11', 'Nº 05', 'Peace Plan'), [(201.5, 203.6, 'Essa estampa ficou bem bonita.'), (204.0, 209.9, 'Fiz até uma enquete no meu Instagram, e ela ganhou até das novas.')]),
 (209.9, 224.0, ('Hoje', 'Drop 01', 'A coleção'), [(209.9, 215.8, 'Até a gente chegar na coleção nova…'), (215.9, 220.6, '…já com o logo novo da RUAH: o sopro.'), (221.2, 224.0, 'E as estampas do Drop 01.')]),
 (247.9, 249.1, ('Hoje', 'Drop 01', 'A coleção'), [(247.9, 249.1, 'Dá para ver pela gola canelada,')]),
 (251.9, 261.8, ('Hoje', 'Drop 01', 'A coleção'), [(251.9, 257.3, 'pelas etiquetas, o versículo aqui dentro…'), (257.8, 259.0, '…e aqui na barra.'), (259.2, 261.8, 'Essa é a coleção nova.')]),
 (262.1, 284.2, None, [(262.1, 267.2, 'Essa é um pouco da história da RUAH.'), (267.3, 273.8, 'Com o tempo, eu vou fazendo outros vídeos…'), (273.8, 279.0, '…para contar quando e por que eu decidi mudar de Faith para RUAH…'), (279.0, 284.2, '…e como aconteceu essa transição.')]),
]
GAP, PAD, FIM = 0.8, 0.18, 3.4
def run(c): subprocess.run(c, check=True)
def cortar(src, s0, s1, p, z0=1.0, z1=1.0):
    n = max(1, round((s1 - s0) * 30)); D = n / 30  # nº exato de quadros; áudio cortado na mesma medida
    run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{s0:.3f}', '-i', src, '-vf', f"hflip,fps=30,scale=w='trunc(1080*({z0}+({z1}-{z0})*t/{D:.3f})/2)*2':h=-2:eval=frame:flags=bicubic,crop=1080:1920,format=yuv420p",
         '-af', f'aresample=48000,loudnorm=I=-15:TP=-1.5,apad,atrim=0:{D:.4f},afade=t=in:d=0.025,afade=t=out:st={max(0, D - .025):.4f}:d=0.025', '-frames:v', str(n), '-ac', '2', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-c:a', 'pcm_s16le', p])
    return n / 30
def main():
    src, trj, out = sys.argv[1:4]; tmp = tempfile.mkdtemp(prefix='ruah_lt_')
    words = [w for s in json.load(open(trj)) for w in s['w']]
    partes, chips, caps, t, ins = [], [], [], 0.0, None
    for a, b, fase, cl in EDL:
        ws = [w for w in words if w[0] >= a - .05 and w[0] < b]
        sub, ini = [], a
        for k in range(len(ws) - 1):
            if ws[k + 1][0] - ws[k][1] > GAP: sub.append((ini, ws[k][1] + PAD)); ini = ws[k + 1][0] - PAD
        sub.append((ini, b))
        c0 = t; mapa = []; seg = len(chips) % 2; L = b - a
        for s0, s1 in sub:
            s0, s1 = max(s0, a), min(s1, b)
            if s1 - s0 < .2: continue
            za, zb = [1.0 + .06 * ((x - a) / L if seg == 0 else 1 - (x - a) / L) for x in (max(s0, a), min(s1, b))]
            d = cortar(src, s0, s1, f'{tmp}/p{len(partes):03d}.mov', za, zb)  # duração REAL do pedaço (evita a legenda atrasar)
            mapa.append((s0, s1, t, d)); partes.append(f'{tmp}/p{len(partes):03d}.mov'); t += d
        def conv(x):  # tempo do bruto → tempo de saída
            for s0, s1, o, d in mapa:
                if x < s1: return o + min(d, max(0, x - s0))
            return mapa[-1][2] + mapa[-1][3]
        for ca, cb, txt in cl: caps.append([round(conv(ca), 2), round(conv(cb), 2), txt])
        if fase and chips and chips[-1][2:] == list(fase): chips[-1][1] = round(t, 2)
        else: chips.append([round(c0, 2), round(t, 2), *(fase or ('', '', ''))])
        if fase and fase[1] == 'Drop 01' and cl[1][2].startswith('…já com'): ins = (conv(215.9), conv(224.0))
    total = t
    for k in range(len(caps) - 1): caps[k][1] = min(caps[k][1], caps[k + 1][0])
    lst = open(f'{tmp}/l.txt', 'w')
    for p in partes: lst.write(f"file '{p}'\n")
    lst.close()
    run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'{tmp}/base.mov'])
    dur = total + FIM
    html = open(os.path.join(HERE, 'linha_overlay_v2.html')).read().replace('__CAPS__', json.dumps(caps, ensure_ascii=False)) \
        .replace('__CHIPS__', json.dumps(chips, ensure_ascii=False)).replace('__END__', f'{total:.2f}')
    hp = os.path.join(HERE, '_lt_ov.html'); open(hp, 'w').write(html)
    try: run(['node', REND, hp, f'{tmp}/ov', f'{dur:.2f}', '30'])
    finally: os.remove(hp)
    a0, a1 = ins; q = (a1 - a0) / len(FOTOS)
    for k, f in enumerate(FOTOS):  # close oficial: fundo desfocado da própria foto + foto inteira com zoom lento
        run(['ffmpeg', '-loglevel', 'error', '-y', '-loop', '1', '-t', f'{q:.3f}', '-i', f, '-filter_complex',
             f"[0:v]split[a][b];[a]scale=1536:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.2[bg];[b]scale=w='trunc(900*(1+0.05*t/{q:.3f})/2)*2':h=-2:eval=frame[fg];[bg][fg]overlay=(W-w)/2:790-h/2,fps=30,format=yuv420p",
             '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', f'{tmp}/f{k}.mp4'])
    open(f'{tmp}/fl.txt', 'w').write(''.join(f"file '{tmp}/f{k}.mp4'\n" for k in range(len(FOTOS))))
    run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/fl.txt', '-c', 'copy', f'{tmp}/ins.mp4'])
    GRADE = 'eq=contrast=1.08:saturation=0.86:gamma=0.97,colorbalance=rs=0.03:gs=0.01:bs=-0.03:rh=0.02:bh=-0.02,vignette=PI/4.5,noise=alls=5:allf=t'
    fc = (f"[3:v]setpts=PTS-STARTPTS+{a0:.3f}/TB,format=yuva420p,fade=t=in:st={a0:.3f}:d=0.25:alpha=1,fade=t=out:st={a1 - .25:.3f}:d=0.25:alpha=1[ins];"
          f"[0:v]tpad=stop_mode=add:color=black:stop_duration={FIM}[v0];[v0][ins]overlay=0:0:eof_action=pass[v1];[v1]{GRADE}[v2];[v2][1:v]overlay=0:0:format=auto,format=yuv420p[v];"
          f"[0:a]apad=pad_dur={FIM}[voz];[voz]asplit[voz1][sc];"
          f"[2:a]volume=0.32,afade=t=in:d=1.5,afade=t=out:st={dur - 2.0:.2f}:d=2.0[mus];[mus][sc]sidechaincompress=threshold=0.04:ratio=4:attack=60:release=900:makeup=1[duck];"
          f"[voz1][duck]amix=inputs=2:normalize=0,alimiter=limit=0.95[au]")
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/base.mov', '-framerate', '30', '-i', f'{tmp}/ov/%04d.png', '-i', TRILHA, '-i', f'{tmp}/ins.mp4',
         '-filter_complex', fc, '-map', '[v]', '-map', '[au]', '-t', f'{dur:.2f}', '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-maxrate', '5M', '-bufsize', '10M',
         '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out])
    json.dump({'caps': caps, 'chips': chips, 'total': total}, open(out.rsplit('.', 1)[0] + '_edl.json', 'w'), ensure_ascii=False, indent=1)
    shutil.rmtree(tmp, ignore_errors=True); print('ok', out, round(dur, 1))
if __name__ == '__main__': main()
