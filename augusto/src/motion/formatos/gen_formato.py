"""Reels nos formatos CONVERSA e PLANILHA (aprovados 16/11) — tela muda a cada frase, narração do Lucas, legenda frase a frase, trilha e efeitos.
Uso: python3 gen_formato.py <nome> <saida.mp4> <trilha.mp3>   (nomes em REELS abaixo). Números = exemplos hipotéticos (contas nos comentários)."""
import sys, os, json, re, subprocess, contextlib, io
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); MOT = os.path.dirname(HERE)
sys.path.insert(0, MOT); os.chdir(MOT)
with contextlib.redirect_stdout(io.StringIO()):
    import narrar_aula as NA
os.chdir(HERE)
RD, GR, BL = '#FF6B78', '#4ADE80', '#7FA3FF'
def big(html, bgc='blue', **k): return dict(shot='big', p=dict(html=html, bg=bgc, **k))
def S(shot, **p): return dict(shot=shot, p=p)

# ---------------- DESCONTO · CONVERSA ----------------
# 83,90×0,70=58,73 · 58,73×27%=15,86 · 58,73−15,86−48,50=−5,63 · 48,50÷0,68=71,32 · 1−71,32÷83,90=15% · 71,32−19,26−48,50=3,56
M1 = [(0, 'Vou dar 30% off em tudo na Black 🔥')]
M2 = M1 + [(1, 'Calma. Faz essa conta comigo antes 👇')]
M3 = M2 + [(1, 'Com 30% off, o preço vira <b>R$ 58,73</b>')]
M4 = M3 + [(0, 'Eita 😳 qual o máximo então?')]
M5 = M4 + [(1, 'Com <b>15%</b> ainda sobram <b>R$ 3,56</b> por venda ✅')]
REELS = {
 'desconto_chat': [
  (big('<div style="font:800 150px/.95 I;letter-spacing:-.06em">VAI DAR<br><span style="background:#fff;color:#1C47C9;padding:0 20px">30% OFF</span><br>NA BLACK?</div>'), "Vai dar 30% de desconto na Black Friday? Olha essa conversa antes."),
  (S('notif', txt='Vou dar 30% off em tudo na Black 🔥'), "Imagine que um seguidor manda: vou dar 30% off em tudo."),
  (S('phone', msgs=M2), "A resposta: calma, faz essa conta antes."),
  (S('bubble', me=1, txt='Preço <b>R$ 83,90</b><br>Custo <b>R$ 48,50</b><br>Taxas <b>27%</b> do preço'), "No exemplo, o produto custa R$ 48,50, é vendido a R$ 83,90 e as taxas somam 27% do preço."),
  (S('phone', msgs=M3, dir=-1), "Com 30% de desconto, o preço cai para R$ 58,73."),
  (big('<div style="font:600 54px I;opacity:.9">Lucro por venda</div><div style="font:800 230px/1 I;letter-spacing:-.06em">−R$ 5,63</div>', 'red', shake=1, top=640), "Tirando as taxas, R$ 15,86, e o custo, sobra prejuízo de R$ 5,63 em cada venda."),
  (S('typing', txt='“Qual o máximo então?”'), "Então, qual é o desconto máximo?"),
  (S('bubble', me=1, txt='Custo ÷ (1 − taxas − margem)<br><b>48,50 ÷ 0,68 = R$ 71,32</b>'), "Divida o custo por 1 menos as taxas menos a margem mínima, aqui 5%. 48,50 dividido por 0,68 dá R$ 71,32."),
  (big('<div style="font:600 54px I;opacity:.9">Desconto máximo</div><div style="font:800 330px/1 I;letter-spacing:-.06em">15%</div>', 'green', top=600), "Esse é o menor preço da oferta. Comparando com R$ 83,90, o desconto máximo é 15%."),
  (S('phone', msgs=M5), "E com 15% de desconto, ainda sobram R$ 3,56 por venda. Números de exemplo."),
  (big('<div style="font:800 150px/.95 I;letter-spacing:-.05em">SALVE<br><span style="color:#BFD2FF">PRA BLACK</span></div><div style="display:inline-block;margin-top:50px;padding:28px 54px;border-radius:99px;background:#fff;color:#1C47C9;font:800 48px I">Envie para quem precisa ↗</div>'), "Salve e faça essa conta antes de criar qualquer cupom."),
 ],
 # ---------------- DESCONTO · PLANILHA ----------------
 'desconto_planilha': [
  (big('<div style="font:800 150px/.95 I;letter-spacing:-.06em">A PLANILHA<br><span style="background:#fff;color:#1C47C9;padding:0 20px">NÃO MENTE.</span></div>'), "Vai dar 30% off na Black? Coloca na planilha antes."),
  (S('sheet', rows=[('Preço', 'R$ 83,90'), ('Custo', 'R$ 48,50'), ('Taxas', '27%')], act=2, count=1), "No exemplo: preço de R$ 83,90, custo de R$ 48,50 e 27% de taxas sobre o preço."),
  (S('cell', l='Desconto', v='30%'), "Agora, o desconto de 30%."),
  (S('formula', f='=B1*(1-B4)', r='R$ 58,73'), "O preço com desconto é o preço vezes 1 menos o desconto. R$ 58,73."),
  (S('sheet', rows=[('Preço', 'R$ 83,90'), ('Custo', 'R$ 48,50'), ('Taxas', '27%'), ('Desconto', '30%'), ('Preço com desconto', 'R$ 58,73'), ('Lucro por venda', '− R$ 5,63', '#E5384A')], act=5, count=1, fx='=B5-B5*B3-B2', flash='#E5384A'), "O lucro é esse preço, menos as taxas, menos o custo."),
  (big('<div style="font:600 54px I;opacity:.9">Em cada venda</div><div style="font:800 230px/1 I;letter-spacing:-.06em">−R$ 5,63</div>', 'red', shake=1, top=640), "Prejuízo de R$ 5,63 em cada venda."),
  (S('chart', title='Lucro por venda', bars=[('Sem desconto', 12.75, '#2F6BFF'), ('Com 30% off', -5.63, '#E5384A')]), "Sem desconto, sobravam R$ 12,75. O desconto de 30% levou tudo, e mais um pouco."),
  (S('formula', f='=B2/(1-B3-5%)', r='R$ 71,32', col=BL), "A conta certa: custo dividido por 1 menos as taxas menos 5% de margem. R$ 71,32."),
  (S('cell', l='Desconto', v='15%', col='#22A06B'), "Isso dá um desconto máximo de 15%."),
  (S('sheet', rows=[('Preço', 'R$ 83,90'), ('Custo', 'R$ 48,50'), ('Taxas', '27%'), ('Desconto', '15%'), ('Preço com desconto', 'R$ 71,32'), ('Lucro por venda', 'R$ 3,56', '#22A06B')], act=5, count=1, fx='=B5-B5*B3-B2', confetti=1), "Com 15%, ainda sobram R$ 3,56 por venda. Números de exemplo."),
  (big('<div style="font:800 150px/.95 I;letter-spacing:-.05em">SALVE<br><span style="color:#BFD2FF">PRA BLACK</span></div><div style="display:inline-block;margin-top:50px;padding:28px 54px;border-radius:99px;background:#fff;color:#1C47C9;font:800 48px I">Envie para quem precisa ↗</div>'), "Salve e faça essa conta antes de criar qualquer cupom."),
 ],
}
SFX = {'notif': [(.25, 'pop', .8)], 'phone': [(.2, 'pop', .7)], 'bubble': [(.05, 'pop', .8)], 'typing': [(0, 'typing', .4)],
       'sheet': [(.2, 'tick', .7), (.5, 'typing', .3)], 'cell': [(.15, 'typing', .4)], 'formula': [(0, 'typing', .45), (1.2, 'impact', .55)], 'chart': [(.2, 'riser', .45)]}

def main():
    nome, out, trilha = sys.argv[1], sys.argv[2], sys.argv[3]
    beats, caps, voz, fx, t = [], [], [], [], 0.0
    for i, (b, fala) in enumerate(REELS[nome]):
        st = t; vt = t + (.25 if i == 0 else .1)
        for fr in [f for f in re.split(r'(?<=[.?!:])\s+', fala) if f.strip()]:
            a = NA.tts(NA.falar(fr)); voz.append((vt, a)); caps.append([round(vt - .05, 3), 0, fr]); vt += len(a) / NA.SR; caps[-1][1] = round(vt + .04, 3); vt += .04
        dur = max(1.6, vt - st + .2); beats.append(dict(t0=round(st, 3), t1=round(st + dur, 3), **b))
        fx.append((st, 'whoosh' if i else 'impact', .5 if i else .7))
        p = b['p']
        if b['shot'] == 'big': fx.append((st + .1, 'impact' if p.get('bg') == 'red' else 'chime' if p.get('bg') == 'green' else 'pop', .7))
        if p.get('confetti'): fx += [(st + .3, 'chime', .7), (st + .4, 'coin', .5)]
        fx += [(st + d, n, g) for d, n, g in SFX.get(b['shot'], [])]
        t = st + dur
    DUR = t + .3; beats[-1]['t1'] = DUR
    for k in range(len(caps) - 1): caps[k][1] = max(caps[k][1], caps[k + 1][0])
    caps[-1][1] = DUR
    html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"></head><body><div id="v"></div>
<script>const THEME={{}};</script><script src="../lib.js"></script><script>const BEATS={json.dumps(beats, ensure_ascii=False)};window.CAPS={json.dumps(caps, ensure_ascii=False)};const DUR={DUR:.3f};</script>
<script src="engine.js"></script><script>R(0)</script></body></html>'''
    hp = os.path.join(HERE, f'reel_{nome}.html'); open(hp, 'w').write(html)
    SR = NA.SR; N = int(DUR * SR) + SR; V = np.zeros(N, np.float32); F = np.zeros(N, np.float32)
    for st, a in voz: i = int(st * SR); V[i:i + len(a)] += a[:N - i]
    for st, n, g in fx:
        a = NA.load(n); i = int(st * SR); F[i:i + len(a)] += g * a[:N - i]
    tmp = f'/tmp/fmt_{nome}'; os.makedirs(tmp, exist_ok=True)
    sf.write(f'{tmp}/voz.wav', V[:int(DUR * SR)], SR); sf.write(f'{tmp}/fx.wav', F[:int(DUR * SR)], SR); json.dump([], open(f'{tmp}/t.json', 'w'))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/voz.wav', '-i', f'{tmp}/fx.wav', '-stream_loop', '-1', '-i', trilha, '-filter_complex',
        f"[2:a]atrim=0:{DUR:.2f},asetpts=PTS-STARTPTS,aformat=sample_rates={SR}:channel_layouts=mono,volume=0.22,afade=t=in:d=0.4,afade=t=out:st={DUR-1.5:.2f}:d=1.5[m];"
        f"[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=300[md];[1:a]volume=0.6[f];[v1][f][md]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5,aformat=channel_layouts=stereo[a]",
        '-map', '[a]', '-ar', str(SR), f'{tmp}/mix.wav'], check=True)
    print('duração', round(DUR, 2), 'telas', len(beats))
    subprocess.run(['node', os.path.join(MOT, 'render_motion.js'), hp, out, str(DUR), '30', f'{tmp}/t.json', f'{tmp}/mix.wav'], check=True, cwd=MOT)

if __name__ == '__main__': main()
