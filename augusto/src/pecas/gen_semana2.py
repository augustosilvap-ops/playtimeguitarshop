"""Carrosséis e estáticos v4 de 18–20/11 (sem presente: CTA salvar/enviar). Gera pecas/v4_semana2.html.
Uso: python3 pecas/gen_semana2.py && node render.js pecas/v4_semana2.html   (rodar em augusto/src)
Todos os números são exemplos hipotéticos — contas conferidas nos comentários."""
OUT = []
def top(n=None):
    return f'<div class="top"><div class="c"><i>↗</i>@augustosilva.p</div>{f"<div class=n>{n}</div>" if n else "<div></div>"}</div>'
def rows(items, hi_last=False, size=36):
    h = ''
    for i, r in enumerate(items):
        a, b = r[0], r[1]; col = r[2] if len(r) > 2 else ''
        last = hi_last and i == len(items) - 1
        st = f'font:{800 if last else 600} {size+(6 if last else 0)}px I;letter-spacing:-.02em'
        h += f'<div style="display:flex;justify-content:space-between;gap:20px;padding:20px 0;{"border-top:3px solid #0A0B10;margin-top:6px" if last else "border-bottom:2px solid #EEF1F7"};{st}"><span>{a}</span><span style="color:{col or ("#2F6BFF" if last else "#0A0B10")};white-space:nowrap">{b}</span></div>'
    return h
def chk(items):
    return ''.join(f'<div class="chk"><b>✓</b><span>{t}</span></div>' for t in items)
def sec(cls, out, body):
    OUT.append(f'<section class="art {cls}" data-out="{out}">{body}</section>')

def carrossel(base, slides):
    n = len(slides)
    for i, (cls, body) in enumerate(slides, 1):
        sec(cls, f'{base}/slides/{i:02d}.png', top(f'{i}/{n}') + body + ('<div class="swipe">arraste pro lado →</div>' if i == 1 else ''))

def capa(l1, blk, l3, hero, s1=104, s2=170, s3=130):
    return f'''<div style="position:absolute;left:70px;right:70px;top:150px;z-index:7"><div class="hv" style="font-size:{s1}px">{l1}</div>
<div class="cn" style="font-size:{s2}px;margin-top:10px;white-space:nowrap"><span class="blk" style="padding:.16em 26px 4px">{blk}</span></div>
<div class="hv" style="font-size:{s3}px;margin-top:10px">{l3}</div></div>{hero}<div class="foot">@augustosilva.p</div>'''
def passo(num, titulo, texto, card, numcol='#2F6BFF', top_card=720):
    return f'''<div class="num" style="top:150px;color:{numcol}">{num}</div>
<div style="position:absolute;left:70px;right:70px;top:320px"><div class="hv" style="font-size:92px">{titulo}</div>
<p class="lt" style="font-size:40px;margin-top:24px;opacity:.85">{texto}</p></div>
<div class="card" style="left:70px;right:70px;top:{top_card}px">{card}</div>'''
def salvar(l1, blk, itens, faixa):
    return f'''<div style="position:absolute;left:70px;right:70px;top:150px;z-index:3"><div class="hv" style="font-size:96px">{l1}</div>
<div class="cn" style="font-size:160px;margin-top:8px;white-space:nowrap"><span class="blk" style="padding:.16em 26px 4px">{blk}</span></div></div>
<div class="card" style="left:70px;right:70px;top:560px;padding:26px 44px">{chk(itens)}</div>
<div class="ctaband"><span style="white-space:nowrap;font-size:{38 if len(faixa)>42 else 44}px">{faixa}</span></div>'''
def estatico(out, cls, l1, blk, hero, nota='Exemplo hipotético'):
    sec(cls, out, top() + f'''<div style="position:absolute;left:70px;right:70px;top:150px;z-index:3"><div class="hv" style="font-size:104px">{l1}</div>
<div class="cn" style="font-size:170px;margin-top:10px;white-space:nowrap"><span class="blk" style="padding:.16em 26px 4px">{blk}</span></div></div>{hero}
<div class="mono" style="position:absolute;left:70px;bottom:130px;color:inherit;opacity:.6">{nota}</div><div class="foot">Leia a legenda ↓</div>''')
def tile(icon, x, y, s=200, cls='tb', col='#fff', rot=-10):
    return f'<div class="tile {cls}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({rot}deg)"><script>document.write(ic("{icon}","{col}"))</script></div>'
def tag(txt, x, y, size=52, rot=0, extra=''):
    return f'<div class="tag" style="left:{x}px;top:{y}px;font-size:{size}px;transform:rotate({rot}deg);{extra}">{txt}</div>'

E18, E19, E20 = 'entregas/2026-11-18', 'entregas/2026-11-19', 'entregas/2026-11-20'

# ===== 13 · DEMANDA (Qua 18/11 10h) =====
carrossel(f'{E18}/13_carrossel_demanda', [
 ('navy', capa('Validar demanda com IA', 'sem inventar', 'números.', tile('ai', 640, 700, 260) + tag('Fonte: seus dados ✓', 120, 1010, 50, -4))),
 ('light', '<div style="position:absolute;left:70px;right:70px;top:170px"><div class="hv" style="font-size:96px">A IA <span style="color:#2F6BFF">não sabe</span> quanto um produto vende.</div><p class="lt" style="font-size:40px;margin-top:28px;opacity:.8">Se você pergunta, ela chuta. O trabalho dela é organizar os dados que <b>você</b> coletou.</p></div>'
   '<div class="card" style="left:70px;right:70px;top:700px"><div class="mono">Pergunta ruim</div><div style="font:700 40px I;margin:14px 0 30px;color:#E5384A">“Quanto vende garrafa térmica?”</div><div class="mono">Pergunta boa</div><div style="font:700 40px I;margin-top:14px;color:#22A06B">“Organize estes dados que eu coletei.”</div></div>'),
 ('navy', passo('01', 'Colete na <span style="color:#7FA3FF">busca.</span>', 'Digite o produto na busca do marketplace e anote os 10 primeiros anúncios.',
   chk(['Preço', 'Número de avaliações', 'Vendas exibidas', 'Frete grátis ou não']))),
 ('light', passo('02', 'Cole na IA e peça <span style="color:#2F6BFF">a tabela.</span>', 'Use os dados, não a opinião dela.',
   '<div class="mono">Prompt</div><div style="font:600 36px/1.45 I;margin-top:18px">“Organize estes 10 anúncios em tabela: preço, avaliações, vendas e frete. Calcule a média e a faixa de preço. <b style="color:#2F6BFF">Não invente nenhum dado.</b>”</div>')),
 ('navy', passo('03', 'Leia os <span style="color:#7FA3FF">sinais.</span>', 'Demanda real deixa rastro.',
   chk(['Avaliações recentes no topo', 'O termo aparece nas sugestões da busca', 'Vendas exibidas nos 5 primeiros']))),
 ('light', passo('04', 'Peça a nota — <span style="color:#2F6BFF">com base nos dados.</span>', 'De 0 a 10 para cada sinal, explicando o motivo.',
   rows([('Demanda', '8/10'), ('Concorrência', '6/10'), ('Margem', '7/10'), ('Decisão', 'testar lote pequeno')], True) + '<div class="mono" style="margin-top:18px">Exemplo hipotético</div>')),
 ('navy', salvar('Salve para validar', 'o próximo.', ['Colete os 10 primeiros anúncios', 'Peça a tabela, sem inventar dados', 'Confira os sinais de demanda', 'Nota de 0 a 10 com motivo'], 'Salve 🔖 e envie para quem compra no achismo ↗')),
])

# ===== 14 · FRETE (Qua 18/11 12h) — 18 + 3,20 = 21,20 · 21,20 ÷ 89,90 = 23,6% =====
estatico(f'{E18}/14_estatico_frete/arte.png', 'light', 'O custo que', 'você esquece:',
  '<div class="hv" style="position:absolute;left:70px;top:470px;font-size:104px;color:#2F6BFF">o frete.</div><div class="card" style="left:70px;right:70px;top:640px">' + rows([('Preço de venda', 'R$ 89,90'), ('Parte do frete que você paga', '− R$ 18,00', '#E5384A'), ('Caixa, fita e etiqueta', '− R$ 3,20', '#E5384A'), ('Logística por pedido', 'R$ 21,20 = 23,6%', '#E5384A')], True) + '</div>'
  + tile('truck', 800, 450, 190, 'tb', '#fff', 8), 'Exemplo hipotético · confira a tabela do seu canal')

# ===== 22 · TICKET (Qua 18/11 20h) — 14.400 ÷ 200 = 72 · 200 × 10 = 2.000 =====
estatico(f'{E18}/22_estatico_ticket/arte.png', 'navy', 'Ticket médio:', 'ninguém olha.',
  '<div style="position:absolute;left:0;right:0;top:540px;text-align:center"><div class="mono" style="color:#9DBBFF">Faturamento ÷ número de pedidos</div><div class="cn" style="font-size:290px;margin-top:6px">R$ 72</div><div style="font:600 40px I;opacity:.85;margin-top:-6px">R$ 14.400 ÷ 200 pedidos</div></div>'
  + tag('<span style="color:#2F6BFF">+R$ 10</span> por pedido = +R$ 2.000/mês', 110, 1040, 44, -3), 'Exemplo hipotético')

# ===== 16 · ERROS (Qui 19/11 10h) =====
def erro(n, t, como, card): return passo(n, t, como, card)
carrossel(f'{E19}/16_carrossel_erros', [
 ('navy', capa('Erros de quem', 'começa no', 'marketplace.', '<div class="cn" style="position:absolute;right:40px;top:640px;font-size:560px;color:#2F6BFF;line-height:.8;z-index:4">7</div>', 104, 170, 120)),
 ('light', erro('01', 'Somar os % <span style="color:#2F6BFF">ao custo.</span>', 'As taxas são cobradas sobre o preço. A conta certa é dividir.',
   rows([('Errado', 'custo × 1,42', '#E5384A'), ('Certo', 'custo ÷ 0,58', '#22A06B')]))),
 ('navy', erro('02', 'Categoria <span style="color:#7FA3FF">errada.</span>', 'A categoria muda a comissão e onde o produto aparece.',
   chk(['Busque o produto e veja a categoria do topo', 'Use a mais específica possível']))),
 ('light', erro('03', 'Título com <span style="color:#2F6BFF">“promoção”.</span>', 'Ninguém pesquisa “barato”. Use as palavras da busca.',
   rows([('Antes', 'Garrafa barata promoção', '#E5384A'), ('Depois', 'Garrafa Térmica Inox 1L', '#22A06B')], size=32))),
 ('navy', erro('04', 'Foto escura ou <span style="color:#7FA3FF">com texto.</span>', 'A primeira foto decide o clique.',
   chk(['Produto inteiro', 'Fundo limpo', 'Luz de janela, sem texto por cima']))),
 ('light', erro('05', 'Esquecer <span style="color:#2F6BFF">o frete.</span>', 'A parte do frete que você paga entra no custo.',
   rows([('Preço', 'R$ 89,90'), ('Frete que você paga', '− R$ 18,00', '#E5384A')]) + '<div class="mono" style="margin-top:16px">Exemplo hipotético</div>')),
 ('navy', '<div class="num" style="top:150px;color:#7FA3FF">06 · 07</div><div style="position:absolute;left:70px;right:70px;top:340px"><div class="hv" style="font-size:84px">Estoque grande sem teste.</div><p class="lt" style="font-size:38px;margin-top:18px;opacity:.85">Comece com um lote pequeno e compre mais quando vender.</p>'
   '<div class="hv" style="font-size:84px;margin-top:70px">Pergunta sem resposta.</div><p class="lt" style="font-size:38px;margin-top:18px;opacity:.85">Quem responde primeiro costuma levar a venda. Responda no mesmo dia.</p></div>'),
 ('navy', salvar('Salve e confira', 'os 7 hoje.', ['Dividir, não somar os %', 'Categoria e título certos', 'Foto clara e frete na conta', 'Lote pequeno e resposta rápida'], 'Salve 🔖 e envie para quem está começando ↗')),
])

# ===== 17 · DEVOLUCAO (Qui 19/11 12h) — 6 × 25 = 150 · 150 ÷ 200 = 0,75 · 6 ÷ 200 = 3% =====
estatico(f'{E19}/17_estatico_devolucao/arte.png', 'bluebg', 'Devolução também', 'é custo.',
  '<div class="card" style="left:70px;right:70px;top:600px">' + rows([('Vendas no mês', '200'), ('Devoluções (3%)', '6'), ('Custo por devolução', 'R$ 25,00'), ('Reserve por venda', 'R$ 0,75')], True) + '<div style="font:600 30px I;color:#3B3F4C;margin-top:18px">6 × R$ 25 = R$ 150 ÷ 200 vendas</div></div>',
  'Exemplo hipotético')

# ===== 26 · REPOR (Qui 19/11 16h) — 4 × 10 = 40 + 12 = 52 =====
estatico(f'{E19}/26_estatico_repor/arte.png', 'light', 'A hora certa', 'de repor.',
  '<div class="card" style="left:70px;right:70px;top:600px"><div class="mono">Ponto de pedido</div><div style="font:800 40px I;margin:14px 0 10px;letter-spacing:-.02em">vendas por dia × prazo do fornecedor + segurança</div>'
  + rows([('Vendas por dia', '4'), ('Prazo do fornecedor', '10 dias'), ('Estoque de segurança', '12'), ('Recompre quando tiver', '52 un.')], True) + '</div>' + tile('box', 830, 470, 180, 'tb', '#fff', 10),
  'Exemplo hipotético')

# ===== 19 · PRONTO (Sex 20/11 10h) =====
carrossel(f'{E20}/19_carrossel_pronto', [
 ('navy', capa('Antes da', 'Black Friday,', 'confira isto.', '<div class="card" style="left:620px;top:640px;width:360px;text-align:center;padding:0;overflow:hidden;transform:rotate(6deg)"><div style="background:#2F6BFF;color:#fff;font:800 34px I;padding:16px">NOVEMBRO</div><div class="cn" style="font-size:260px;color:#0A0B10;padding:10px 0 0">27</div><div style="font:700 28px I;color:#3B3F4C;padding-bottom:24px">Black Friday</div></div>', 110, 160, 120)),
 ('light', passo('01', 'Desconto máximo <span style="color:#2F6BFF">por produto.</span>', 'Custo ÷ (1 − taxas − margem mínima). Acima disso, é prejuízo.', rows([('Preço atual', 'R$ 83,90'), ('Preço da oferta', 'R$ 71,32'), ('Desconto máximo', '15%')], True) + '<div class="mono" style="margin-top:16px">Exemplo hipotético</div>')),
 ('navy', passo('02', 'Estoque para <span style="color:#7FA3FF">a demanda.</span>', 'Ruptura na Black derruba a posição do anúncio.', chk(['Liste os 10 mais vendidos', 'Confira o estoque de cada um', 'Peça reposição até 20/11']))),
 ('light', passo('03', 'Anúncios <span style="color:#2F6BFF">revisados.</span>', 'Mais visitas em anúncio fraco só aumentam o gasto.', chk(['Foto: produto inteiro, fundo limpo', 'Título com as palavras da busca', 'Preço comparado ao topo']))),
 ('navy', passo('04', 'Frete e <span style="color:#7FA3FF">envio testados.</span>', 'Pedido atrasado vira reclamação.', chk(['Horário de corte da transportadora', 'Embalagens e etiquetas em estoque', 'Rotina de envio no papel']))),
 ('light', passo('05', 'Respostas <span style="color:#2F6BFF">prontas.</span>', 'Pergunta sem resposta é venda perdida.', chk(['Tem pronta entrega?', 'Qual o prazo?', 'Como funciona a troca?']))),
 ('navy', passo('06', 'Oferta com <span style="color:#7FA3FF">limite e prazo.</span>', 'Quantas unidades, até quando e qual a meta de lucro.', rows([('Unidades na oferta', '100'), ('Período', '24 a 30/11'), ('Meta de lucro', 'R$ 3,56/venda')], True) + '<div class="mono" style="margin-top:16px">Exemplo hipotético</div>')),
 ('navy', salvar('Salve e marque', 'o que falta.', ['Desconto máximo calculado', 'Estoque conferido', 'Anúncios revisados', 'Envio e respostas prontos', 'Oferta com limite e prazo'], 'Salve 🔖 e envie para quem vai fazer Black ↗')),
])

# ===== 20 · SOBRA (Sex 20/11 12h) — 45+14+6+5+8+2 = 80 → sobra 20 =====
barras = [('Produto', 45, '#0A1430'), ('Comissão', 14, '#2F6BFF'), ('Frete e embalagem', 8, '#7FA3FF'), ('Imposto', 6, '#9DBBFF'), ('Anúncios', 5, '#C9D6F5'), ('Devoluções', 2, '#DCE5F7'), ('Sobra', 20, '#22A06B')]
bh = ''.join(f'<div style="display:flex;align-items:center;gap:20px;margin:10px 0"><div style="width:300px;font:700 30px I">{a}</div><div style="flex:1;height:38px;background:#F1F3F8;border-radius:10px;overflow:hidden"><div style="width:{v/45*100:.0f}%;height:100%;background:{c}"></div></div><div style="width:120px;text-align:right;font:800 32px I;color:{"#22A06B" if a=="Sobra" else "#0A0B10"}">R$ {v}</div></div>' for a, v, c in barras)
estatico(f'{E20}/20_estatico_sobra/arte.png', 'navy', 'De cada R$ 100,', 'o que sobra?', f'<div class="card" style="left:70px;right:70px;top:560px;padding:34px 40px">{bh}</div>', 'Exemplo hipotético · faça com os seus números')

# ===== 25 · AVALIA (Sex 20/11 16h) =====
carrossel(f'{E20}/25_carrossel_avalia', [
 ('navy', capa('Avaliação negativa', 'pode vender', 'mais.', '<div class="card" style="left:120px;right:120px;top:700px;transform:rotate(-3deg)"><div style="font:800 60px I;color:#F5B400">★<span style="color:#D6DAE3">★★★★</span></div><div style="font:600 36px/1.35 I;margin-top:16px">“Chegou amassada. Fiquei chateada.”</div><div style="margin-top:22px;padding:20px 24px;border-radius:18px;background:#EAF0FF;font:600 30px/1.35 I;color:#1C47C9">Resposta da loja ↓</div></div>', 104, 170, 130)),
 ('light', '<div style="position:absolute;left:70px;right:70px;top:170px"><div class="hv" style="font-size:96px">Quem compra <span style="color:#2F6BFF">lê as negativas</span> primeiro.</div><p class="lt" style="font-size:40px;margin-top:28px;opacity:.8">A sua resposta não é para quem reclamou. É para os próximos 100 compradores que vão ler.</p></div>'),
 ('navy', passo('01', 'Agradeça e <span style="color:#7FA3FF">seja específico.</span>', 'Nada de resposta copiada. Cite o problema que a pessoa contou.', '<div style="font:600 36px/1.45 I">“Oi, Ana! Obrigado por avisar sobre a caixa amassada.”</div>')),
 ('light', passo('02', 'Explique <span style="color:#2F6BFF">sem culpar.</span>', 'Nunca discuta com o cliente em público.', '<div style="font:600 36px/1.45 I">“A embalagem não protegeu bem o produto no transporte.”</div>')),
 ('navy', passo('03', 'Diga o que <span style="color:#7FA3FF">mudou.</span>', 'É isso que convence quem está lendo.', '<div style="font:600 36px/1.45 I">“Reforçamos a caixa com proteção extra em todos os envios.”</div>')),
 ('light', passo('04', 'Ofereça <span style="color:#2F6BFF">a solução.</span>', 'Troca, devolução ou contato — pelo canal oficial.', '<div style="font:600 36px/1.45 I">“Já te chamamos pelo chat para resolver a troca.”</div>')),
 ('navy', salvar('Salve o modelo', 'de resposta.', ['Agradeça e cite o problema', 'Explique sem culpar', 'Diga o que mudou', 'Ofereça a solução'], 'Salve 🔖 e envie para quem tem medo de avaliação ↗')),
])

# ===== 24 · COMBO (Sex 20/11 20h) — kit 109,90: 109,90 − 29,67 − 47 = 33,23 · sozinho 89,90 − 24,27 − 38 = 27,63 · +5,60 · separado 119,80 − 109,90 = 9,90 =====
carrossel(f'{E20}/24_carrossel_combo', [
 ('navy', capa('Venda mais', 'sem desconto:', 'monte um kit.', '<div style="position:absolute;left:0;right:0;top:620px;height:420px"><script>document.write(box(170,40,300,"Garrafa")+box(560,120,240,"Capa"))</script></div>' + tag('+ R$ 5,60 de lucro por pedido', 150, 1080, 46, -3), 104, 148, 120)),
 ('light', passo('01', 'O desconto sai <span style="color:#2F6BFF">do lucro.</span>', '10% de desconto num produto de R$ 89,90 tira R$ 8,99 de cada venda.', rows([('Preço', 'R$ 89,90'), ('Desconto de 10%', '− R$ 8,99', '#E5384A')]) + '<div class="mono" style="margin-top:16px">Exemplo hipotético</div>')),
 ('navy', passo('02', 'Junte um <span style="color:#7FA3FF">complemento.</span>', 'Algo que quem compra o produto principal também precisa.', chk(['Garrafa + capa térmica', 'Camiseta + boné', 'Panela + espátula']))),
 ('light', passo('03', 'Faça <span style="color:#2F6BFF">a conta.</span>', 'Taxas de 27% sobre o preço, custos somados.', rows([('Garrafa sozinha: lucro', 'R$ 27,63'), ('Kit R$ 109,90: lucro', 'R$ 33,23'), ('Diferença por pedido', '+ R$ 5,60', '#22A06B')], True, 34) + '<div class="mono" style="margin-top:16px">Exemplo hipotético</div>')),
 ('navy', passo('04', 'Mostre <span style="color:#7FA3FF">a economia.</span>', 'O cliente percebe vantagem sem você cortar o preço.', rows([('Comprando separado', 'R$ 119,80'), ('No kit', 'R$ 109,90'), ('Cliente economiza', 'R$ 9,90', '#22A06B')], True))),
 ('light', passo('05', 'Teste <span style="color:#2F6BFF">14 dias.</span>', 'Anuncie o kit ao lado do produto sozinho e compare o lucro por pedido.', chk(['Mesmo preço do produto sozinho', 'Kit em anúncio próprio', 'Compare lucro, não só vendas']))),
 ('navy', salvar('Salve e monte', 'seu 1º kit.', ['Escolha um complemento', 'Calcule o lucro do kit', 'Mostre a economia', 'Teste por 14 dias'], 'Salve 🔖 e envie para quem só pensa em desconto ↗')),
])

html = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="../v4.css"><script src="../v4.js"></script></head><body>\n' + '\n'.join(OUT) + '\n</body></html>\n'
import os; open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4_semana2.html'), 'w').write(html); print(len(OUT), 'artes')
