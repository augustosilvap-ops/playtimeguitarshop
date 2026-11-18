"""CAOS INSANO BR — Shorts de curiosidades narrados (voz Lucas, legenda palavra a palavra, trilha Mixkit + SFX).
Uso: python3 gen_caos.py <nome> <saida.mp4> [trilha.mp3]
FATOS: só informação pública e confirmada (Rockstar/imprensa). Sem spoiler da história. Sem arte/logo da Rockstar."""
import sys, os, json, re, subprocess, contextlib, io
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); MOT = os.path.abspath(os.path.join(HERE, '../../augusto/src/motion'))
sys.path.insert(0, MOT); _cwd = os.getcwd(); os.chdir(MOT)
with contextlib.redirect_stdout(io.StringIO()):
    import narrar_aula as NA
os.chdir(HERE)
def S(shot, **p): return dict(shot=shot, p=p)

# Fontes: GTA V lançado em 17/09/2013; GTA VI 19/11/2026 (Rockstar, adiado de "outono 2025" → 26/05/2026 → 19/11/2026).
# Trailer 1 (05/12/2023, liberado na véspera, 04/12, após vazamento): 90+ milhões de views em 24 h no YouTube (recorde de vídeo não musical).
# Trailer 2 (06/05/2025): 475 milhões de views em 24 h somando plataformas (Rockstar). Músicas: Tom Petty "Love Is a Long Road" (T1), The Pointer Sisters "Hot Together" (T2).
# Parte 2: dev confirmado 04/02/2022; vazamento 18/09/2022 (90+ vídeos, hacker de 17 anos); Rockstar fundada 12/1998 → trailer 1 em 12/2023 (25 anos);
# trailer 2 "capturado inteiramente no jogo no PS5" (Rockstar); lançamento PS5/Xbox Series, sem PC anunciado; GTA V 200+ mi cópias (Take-Two); nomes Jason Duval/Lucia Caminos (site Rockstar, 05/2025).
# Leonida = estado inspirado na Flórida (regiões divulgadas pela Rockstar em 05/2025: Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga); Vice City = inspirada em Miami. Lucia: primeira protagonista mulher da era 3D da série.
REELS = {
 'curiosidades1': [
  (S('title', html='7 COISAS<br><span class="cy">QUE VOCÊ</span><br>PRECISA SABER<br><span class="yl">ANTES DE JOGAR</span>', size=150), "Sete coisas sobre o GTA 6 que você precisa saber antes de jogar."),
  (S('years', a=2013, b=2026, big='13 ANOS'), "Um: foram treze anos de espera. O GTA 5 saiu em 2013, e o 6 chega agora, em 19 de novembro de 2026."),
  (S('delay', lbl='ADIADO 2 VEZES', steps=['2025', 'MAIO 2026', '19 NOV 2026']), "Dois: ele foi adiado duas vezes. Era para 2025, passou para maio de 2026 e só então ficou para 19 de novembro."),
  (S('rank', n=3, html='LUCIA<br><span class="cy">FAZ HISTÓRIA</span>', sub='Primeira protagonista mulher da era 3D da série.', sky=1), "Três: Lucia é a primeira protagonista mulher da era 3D da série. Ela divide a história com o Jason."),
  (S('num', lbl='Trailer 1 · em 24 horas', v=90, pre='+', suf='', unit='MILHÕES DE VIEWS', sub='Recorde de vídeo não musical no YouTube'), "Quatro: o primeiro trailer passou de 90 milhões de visualizações no YouTube em 24 horas. Recorde para um vídeo que não é clipe de música."),
  (S('rank', n=5, html='VAZOU,<br><span class="yl">SAIU ANTES</span>', sub='O trailer 1 foi liberado um dia antes do previsto, depois de vazar na internet.', top=540), "Cinco: esse trailer saiu um dia antes do previsto, porque vazou na internet e a Rockstar decidiu liberar na hora."),
  (S('num', lbl='Trailer 2 · em 24 horas', v=475, unit='MILHÕES DE VIEWS', sub='Somando todas as plataformas', size=280), "Seis: o segundo trailer foi ainda maior. 475 milhões de visualizações em 24 horas, somando todas as plataformas."),
  (S('map', lbl='LEONIDA = FLÓRIDA', pins=['Vice City', 'Leonida Keys', 'Grassrivers', 'Port Gellhorn', 'Ambrosia', 'Mount Kalaga']), "Sete: o mapa se passa em Leonida, um estado inspirado na Flórida. E Vice City é a versão do jogo para Miami."),
  (S('song', lbl='BÔNUS · TRILHA DOS TRAILERS', t='LOVE IS A LONG ROAD', a='Tom Petty · trailer 1'), "Bônus: a música do primeiro trailer é Love Is a Long Road, de Tom Petty."),
  (S('cta', html='QUAL VOCÊ<br><span class="yl">NÃO SABIA?</span>', btn='SEGUE PRA PARTE 2 →'), "Qual dessas você não sabia? Segue o Caos Insano que amanhã tem parte dois."),
 ],
}
REELS['curiosidades2'] = [
  (S('title', html='MAIS 7<br><span class="cy">COISAS</span><br>DO <span class="yl">GTA 6</span><br>QUE POUCA GENTE SABE', size=140), "Mais sete coisas do GTA 6 que pouca gente sabe. Parte dois."),
  (S('delay', lbl='LINHA DO TEMPO', steps=['FEV 2022', 'SET 2022', 'DEZ 2023'], nocut=1), "Um: a Rockstar só confirmou que o jogo estava em produção em fevereiro de 2022. Sete meses depois veio um dos maiores vazamentos da história dos games."),
  (S('num', lbl='Vazamento · set 2022', v=90, pre='+', unit='VÍDEOS VAZADOS', sub='De uma versão inicial do jogo, ainda em desenvolvimento'), "Dois: mais de 90 vídeos de uma versão inicial do jogo vazaram na internet. E quem vazou foi um hacker de 17 anos."),
  (S('rank', n=3, html='TRAILER DE<br><span class="yl">ANIVERSÁRIO</span>', sub='O trailer 1 saiu em dezembro de 2023, mês dos 25 anos da Rockstar.'), "Três: o primeiro trailer foi lançado em dezembro de 2023, no mês em que a Rockstar completou 25 anos."),
  (S('rank', n=4, html='TUDO<br><span class="cy">NO PS5</span>', sub='A Rockstar disse que o trailer 2 foi capturado inteiro dentro do jogo, no PS5.'), "Quatro: segundo a Rockstar, o trailer dois foi capturado inteiro dentro do jogo, rodando no PS5. Uma parte é gameplay e outra parte é cena."),
  (S('check', lbl='NO LANÇAMENTO', items=[('PS5', 1), ('XBOX SERIES', 1), ('PC', 0)]), "Cinco: no lançamento, o jogo sai só para PS5 e Xbox Series. Para PC ainda não tem data."),
  (S('num', lbl='A régua: GTA 5 vendeu', v=200, pre='+', unit='MILHÕES DE CÓPIAS', sub='Um dos jogos mais vendidos da história'), "Seis: a régua está alta. O GTA 5 passou de 200 milhões de cópias vendidas, um dos jogos mais vendidos da história."),
  (S('rank', n=7, html='JASON <span class="cy">DUVAL</span><br>&amp; LUCIA<br><span class="yl">CAMINOS</span>', top=520, size=130, sub='Os nomes completos dos protagonistas, revelados pela Rockstar.', subTop=1000), "Sete: os protagonistas têm nome completo. Jason Duval e Lucia Caminos."),
  (S('song', lbl='BÔNUS · TRILHA DO TRAILER 2', t='HOT TOGETHER', a='The Pointer Sisters · trailer 2'), "Bônus: a música do trailer dois é Hot Together, das Pointer Sisters."),
  (S('cta', html='AMANHÃ<br><span class="yl">É O DIA</span>', btn='SEGUE O CAOS INSANO →'), "Amanhã é o dia. Segue o Caos Insano pra não perder nada do lançamento."),
]
SFX = {'num': [(.15, 'riser', .5), (1.45, 'impact', .7)], 'years': [(.3, 'tick', .6), (1.6, 'impact', .7)], 'delay': [(.3, 'stamp', .6), (1.2, 'stamp', .6), (2.1, 'chime', .7)],
       'rank': [(.05, 'impact', .7)], 'map': [(.3, 'pop', .6), (.65, 'pop', .6), (1.0, 'pop', .6), (1.35, 'pop', .6)], 'song': [(.2, 'swipe', .6)], 'cta': [(.1, 'chime', .8)], 'check': [(.35, 'chime', .6), (.85, 'chime', .6), (1.35, 'impact', .6)], 'title': [(.1, 'impact', .8)]}

def main():
    nome, out = sys.argv[1], sys.argv[2]; trilha = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '../trilhas/mk_173.mp3')
    beats, caps, voz, fx, t = [], [], [], [], 0.0
    for i, (b, fala) in enumerate(REELS[nome]):
        st = t; vt = t + (.2 if i == 0 else .08)
        for fr in [f for f in re.split(r'(?<=[.?!:])\s+', fala) if f.strip()]:
            a = NA.tts(NA.falar(fr)); voz.append((vt, a)); d = len(a) / NA.SR
            ws = fr.split(); ch = [ws[k:k + 4] for k in range(0, len(ws), 4)]; tt = vt
            for c in ch:
                cd = d * len(c) / len(ws); caps.append([round(tt, 3), round(tt + cd, 3), ' '.join(c)]); tt += cd
            vt += d + .03
        dur = max(1.8, vt - st + .15); beats.append(dict(t0=round(st, 3), t1=round(st + dur, 3), **b))
        fx.append((st, 'whoosh' if i else 'impact', .5 if i else .7)); fx += [(st + d_, n, g) for d_, n, g in SFX.get(b['shot'], [])]
        t = st + dur
    DUR = t + .3; beats[-1]['t1'] = DUR
    for k in range(len(caps) - 1): caps[k][1] = max(caps[k][1], min(caps[k + 1][0], caps[k][1] + .3))
    html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="caos.css"></head><body><div id="v"></div>
<script>const BEATS={json.dumps(beats, ensure_ascii=False)};window.CAPS={json.dumps(caps, ensure_ascii=False)};const DUR={DUR:.3f};function setTimes(){{}}</script>
<script src="caos_engine.js"></script><script>R(0)</script></body></html>'''
    hp = os.path.join(HERE, f'short_{nome}.html'); open(hp, 'w').write(html)
    SR = NA.SR; N = int(DUR * SR) + SR; V = np.zeros(N, np.float32); F = np.zeros(N, np.float32)
    for st, a in voz: i = int(st * SR); V[i:i + len(a)] += a[:N - i]
    for st, n, g in fx: a = NA.load(n); i = int(st * SR); F[i:i + len(a)] += g * a[:N - i]
    tmp = f'/tmp/caos_{nome}'; os.makedirs(tmp, exist_ok=True)
    sf.write(f'{tmp}/voz.wav', V[:int(DUR * SR)], SR); sf.write(f'{tmp}/fx.wav', F[:int(DUR * SR)], SR); json.dump([], open(f'{tmp}/t.json', 'w'))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/voz.wav', '-i', f'{tmp}/fx.wav', '-stream_loop', '-1', '-i', trilha, '-filter_complex',
        f"[2:a]atrim=0:{DUR:.2f},asetpts=PTS-STARTPTS,aformat=sample_rates={SR}:channel_layouts=mono,volume=0.3,afade=t=in:d=0.3,afade=t=out:st={DUR-1.5:.2f}:d=1.5[m];"
        f"[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=300[md];[1:a]volume=0.6[f];[v1][f][md]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5,aformat=channel_layouts=stereo[a]",
        '-map', '[a]', '-ar', str(SR), f'{tmp}/mix.wav'], check=True)
    print('duração', round(DUR, 2), 'telas', len(beats))
    subprocess.run(['node', os.path.join(MOT, 'render_motion.js'), hp, os.path.abspath(os.path.join(_cwd, out)), f'{DUR:.2f}', '30', f'{tmp}/t.json', f'{tmp}/mix.wav'], check=True, cwd=MOT)
if __name__ == '__main__': main()
