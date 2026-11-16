"""Reels de TESTE com conteúdo INÉDITO (16/11: 'não quero que seja o mesmo conteúdo do feed').
8 mini-aulas novas; cada uma vira um par A/B mudando UMA variável. Números = exemplos hipotéticos (contas nos comentários).
Uso: python3 gen_testes.py  → reel_aula_t<n>_*.html ; narração em narr_textos.NARR"""
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import gen_aula as G
from gen_aula import T, tb, box, head, resumo, build
import narr_textos as N

def B(name, theme, save, S, cap):
    G.SAVE = save; r = build(name, theme, 'X', cap, S); G.SAVE = None; return r
def uiw(hero, words):
    h = hero.replace("'", "\\'")
    return f"uiworld(lt,{{dur:3.2,heroTop:1060,hero:'{h}'}})+W(lt,[{words}],300)"
def card(lab, big, a, b, bc='#E5384A'):
    return f"<div style='padding:34px'><div style='font:700 28px I;opacity:.7'>{lab}</div><div style='font:800 58px I;margin-top:8px'>{big}</div><div style='display:flex;justify-content:space-between;margin-top:18px;font:700 34px I'><span>{a}</span><span style='color:{bc}'>{b}</span></div></div>"
OUT = {}

# ---------- T1 · CLÁSSICO × PREMIUM (Efeito) — 100−12−6−50=32 · 100−17−6−50=27 · 32÷27=1,185 → +19% ----------
t1 = [
 (2.2,'dark',"W(lt,[[0,'CLÁSSICO',150],[.2,'OU',110,BL2],[.4,'PREMIUM?',170]],380)","Clássico ou Premium? Vamos fazer a conta, com um exemplo."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Colocar tudo no Premium porque parece que vende mais.',top=620,size=56),"Erro comum: escolher o tipo de anúncio no achismo."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+tb([T('Produto','R$ 100'),T('Custo','R$ 50'),T('Imposto','6%'),T('Comissão Clássico','12%'),T('Comissão Premium','17%')],w1="'55%'"),"A comissão do Premium é maior, e sai do seu lucro."),
 (2.6,'dark',head('PASSO 1','AS COMISSÕES','BL2')+"+"+tb([T('Clássico','12% (exemplo)'),T('Premium','17% (exemplo)'),T('Onde achar','tabela da sua categoria')],w1="'40%'"),"Passo 1: veja a comissão de cada tipo na tabela da sua categoria."),
 (2.6,'light',head('PASSO 2','LUCRO POR VENDA','BL')+"+"+tb([T('Clássico','100 − 12 − 6 − 50 = R$ 32'),T('Premium','100 − 17 − 6 − 50 = R$ 27')],w1="'30%'"),"Passo 2: calcule o lucro de uma venda em cada tipo."),
 (2.4,'accent',head('PASSO 3','A DIFERENÇA')+"+(lt>.5?`<div class=\"t\" style=\"top:640px;font-size:300px;color:#fff;transform:scale(${eb((lt-.5)/.35)})\">+19%</div>`:'')","Passo 3: 32 dividido por 27 dá 1,19. O Premium precisa vender 19% a mais."),
 (2.6,'dark',head('PASSO 4','TESTE','BL2')+"+"+tb([T('Vendeu menos de +19%','fique no Clássico'),T('Vendeu mais de +19%','Premium compensa','GR')],hiLast='true',w1="'50%'"),"Passo 4: teste os dois e compare o lucro, não só as vendas."),
 (2.4,'light',resumo(['Veja as comissões','Calcule o lucro em cada','Divida um pelo outro','Teste e compare o lucro'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve antes de escolher o tipo do próximo anúncio."),
]
N.NARR['t1_classico'] = [
 "Clássico ou Premium no marketplace? Vamos fazer a conta, com um exemplo.",
 "O erro comum é colocar tudo no Premium porque parece que vende mais, sem olhar quanto sobra.",
 "Por quê? No exemplo, um produto de R$ 100, com custo de R$ 50 e 6% de imposto. A comissão do Clássico é 12% e a do Premium, 17%.",
 "Passo 1: veja a comissão de cada tipo de anúncio na tabela de tarifas da sua categoria. Os números aqui são só exemplo.",
 "Passo 2: calcule o lucro de uma venda. No Clássico, sobram R$ 32. No Premium, R$ 27.",
 "Passo 3: divida um pelo outro. 32 dividido por 27 dá 1,19. O Premium precisa vender 19% a mais só para empatar.",
 "Passo 4: teste os dois tipos e compare o lucro total, não só o número de vendas.",
 "Resumo: veja as comissões, calcule o lucro em cada tipo, divida e teste. Números de exemplo.",
 "Salve antes de escolher o tipo do próximo anúncio.",
]
OUT['t1_classico'] = B('t1_classico', 'azul_aneis', ('SALVE', 'E CALCULE'), t1, 'Salve antes de escolher o tipo do próximo anúncio.')
t1b = list(t1); t1b[0] = (3.4, 'dark', uiw(card('Seu anúncio', 'Clássico ou Premium?', 'Lucro por venda', 'R$ 32 × R$ 27', '#FFC94D'), "[1.0,'CLÁSSICO',150],[1.2,'OU',110,BL2],[1.45,'PREMIUM?',170]"), t1[0][3])
N.NARR['t1_classico_ui'] = N.NARR['t1_classico']
OUT['t1_classico_ui'] = B('t1_classico_ui', 'azul_aneis', ('SALVE', 'E CALCULE'), t1b, 'Salve antes de escolher o tipo do próximo anúncio.')

# ---------- T2 · CURVA ABC (Duração) — 40.000 + 7.500 + 2.500 = 50.000 ----------
t2 = [
 (2.2,'dark',"W(lt,[[0,'QUAIS PRODUTOS',120],[.2,'PAGAM',150,BL2],[.4,'SUAS CONTAS?',130]],380)","Quais produtos pagam as suas contas? Vamos descobrir, com um exemplo."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Dar a mesma atenção para os 100 produtos da loja.',top=620,size=56),"Erro comum: tratar todos os produtos igual."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+tb([T('20 produtos','R$ 40.000 (80%)'),T('30 produtos','R$ 7.500 (15%)'),T('50 produtos','R$ 2.500 (5%)')],w1="'40%'"),"Poucos produtos fazem quase todo o faturamento (exemplo)."),
 (2.4,'dark',head('PASSO 1','EXPORTE','BL2')+"+"+box('Relatório de vendas dos últimos 90 dias, por produto.',top=640,size=52),"Passo 1: exporte as vendas dos últimos 90 dias, por produto."),
 (2.4,'light',head('PASSO 2','ORDENE','BL')+"+"+tb([T('1º','R$ 6.200'),T('2º','R$ 5.100'),T('3º','R$ 4.300'),T('…','…')],w1="'20%'"),"Passo 2: ordene do maior para o menor faturamento."),
 (2.6,'dark',head('PASSO 3','CORTE','BL2')+"+"+tb([T('Até 80% acumulado','curva A'),T('De 80% a 95%','curva B'),T('Resto','curva C')],w1="'50%'"),"Passo 3: some o acumulado e corte em 80% e 95%."),
 (2.6,'accent',head('PASSO 4','AÇÃO')+"+"+tb([T('A','nunca falta estoque'),T('B','melhore os anúncios'),T('C','revise ou tire')],w1="'20%'"),"Passo 4: cada curva tem uma ação diferente."),
 (2.4,'light',resumo(['Exporte 90 dias','Ordene por faturamento','Corte em 80% e 95%','Uma ação por curva'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve e faça a sua curva ABC esta semana."),
]
N.NARR['t2_abc'] = [
 "Quais produtos realmente pagam as suas contas? Vamos descobrir, com um exemplo.",
 "O erro comum é dar a mesma atenção para os 100 produtos da loja.",
 "Por quê? No exemplo, a loja fatura R$ 50 mil. Só 20 produtos fazem R$ 40 mil, 80% do total. Os 50 últimos fazem só R$ 2.500.",
 "Passo 1: exporte o relatório de vendas dos últimos 90 dias, por produto, no painel do seu canal.",
 "Passo 2: numa planilha, ordene do produto que mais faturou para o que menos faturou.",
 "Passo 3: some o faturamento acumulado. Até 80% é a curva A. De 80 a 95% é a curva B. O resto é a curva C.",
 "Passo 4: curva A nunca pode faltar estoque. Na curva B, melhore os anúncios. A curva C, revise ou tire da loja.",
 "Resumo: exporte, ordene, corte em 80 e 95% e dê uma ação para cada curva. Números de exemplo.",
 "Salve e faça a sua curva ABC esta semana.",
]
OUT['t2_abc'] = B('t2_abc', 'claro_pontos', ('SALVE', 'E ORGANIZE'), t2, 'Salve e faça a sua curva ABC esta semana.')
N.NARR['t2_abc_curta'] = [
 "Quais produtos realmente pagam as suas contas? Descubra em 3 passos.",
 "No exemplo, 20 de 100 produtos fazem 80% do faturamento.",
 "Ordene as vendas dos últimos 90 dias do maior para o menor faturamento e some o acumulado: até 80% é a curva A.",
 "Curva A nunca falta estoque. Curva C, revise ou tire. Números de exemplo.",
 "Salve e faça a sua curva ABC esta semana.",
]
OUT['t2_abc_curta'] = B('t2_abc_curta', 'claro_pontos', ('SALVE', 'E ORGANIZE'), [t2[i] for i in (0, 2, 5, 6)], 'Salve e faça a sua curva ABC esta semana.')

# ---------- T3 · PESO CUBADO (Narração) — 40×30×20 = 24.000 ÷ 6.000 = 4 kg · 30×20×15 = 9.000 ÷ 6.000 = 1,5 kg ----------
t3 = [
 (2.2,'dark',"W(lt,[[0,'FRETE CARO',150],[.2,'POR CAUSA',120,BL2],[.4,'DA CAIXA?',160]],380)","O seu frete pode estar caro por causa da caixa. Veja, com um exemplo."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Achar que o frete é cobrado só pelo peso do produto.',top=620,size=56),"Erro comum: olhar só o peso na balança."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('A transportadora cobra o MAIOR entre o peso real e o peso cubado (o tamanho da caixa).',top=620,size=52),"A transportadora cobra o maior: peso real ou peso pelo tamanho da caixa."),
 (2.6,'dark',head('PASSO 1','MEÇA A CAIXA','BL2')+"+"+tb([T('Comprimento','40 cm'),T('Largura','30 cm'),T('Altura','20 cm')],w1="'45%'"),"Passo 1: meça a caixa em centímetros."),
 (2.6,'light',head('PASSO 2','A CONTA','BL')+"+"+tb([T('Multiplique','40 × 30 × 20 = 24.000'),T('Divida pelo fator','24.000 ÷ 6.000'),T('Peso cubado','4 kg')],hiLast='true',w1="'40%'"),"Passo 2: multiplique as medidas e divida pelo fator da transportadora."),
 (2.4,'accent',head('PASSO 3','COMPARE')+"+"+tb([T('Peso real','1,2 kg'),T('Peso cubado','4 kg'),T('Você paga por','4 kg')],hiLast='true',w1="'45%'"),"Passo 3: compare. Você paga pelo maior dos dois."),
 (2.6,'dark',head('PASSO 4','TROQUE A CAIXA','BL2')+"+slider(lt,{top:480,h:760,t0:.3,dur:1.1,L:{bg:'#3A3D47',k:'ANTES',big:'4 kg',sub:'40×30×20',c:'#FF8A95'},Rt:{bg:'#FFFFFF',k:'DEPOIS',big:'1,5 kg',sub:'30×20×15',c:BL},bigSize:150})","Passo 4: uma caixa menor derruba o peso cobrado."),
 (2.4,'light',resumo(['Meça a caixa','Multiplique e divida pelo fator','Compare com o peso real','Use a menor caixa possível'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve e meça as caixas dos seus 5 mais vendidos."),
]
N.NARR['t3_cubado'] = [
 "O seu frete pode estar caro por causa da caixa, não do produto. Veja, com um exemplo.",
 "O erro comum é achar que o frete é cobrado só pelo peso que aparece na balança.",
 "Por quê? A transportadora cobra o maior entre o peso real e o peso cubado, que é calculado pelo tamanho da caixa.",
 "Passo 1: meça a caixa em centímetros. No exemplo, 40 de comprimento, 30 de largura e 20 de altura.",
 "Passo 2: multiplique as três medidas, 24 mil, e divida pelo fator da sua transportadora. Aqui usamos 6 mil. O peso cubado é 4 quilos.",
 "Passo 3: compare. O produto pesa 1,2 quilo, mas você paga por 4.",
 "Passo 4: troque a caixa. Uma caixa de 30 por 20 por 15 dá 1,5 quilo cubado.",
 "Resumo: meça, multiplique, divida pelo fator e use a menor caixa possível. Confira o fator da sua transportadora.",
 "Salve e meça as caixas dos seus 5 produtos mais vendidos.",
]
OUT['t3_cubado'] = B('t3_cubado', 'navy_scan', ('SALVE', 'E MEÇA'), t3, 'Salve e meça as caixas dos seus 5 mais vendidos.')

# ---------- T4 · CAC (Gancho) — 1.200 ÷ 40 = 30 · 35 − 30 = 5 · 40 × 5 = 200 ----------
t4 = [
 (2.2,'dark',"W(lt,[[0,'QUANTO CUSTA',130],[.2,'CADA VENDA',150,BL2],[.4,'DO ANÚNCIO?',130]],380)","Quanto custa cada venda que vem do anúncio? Vamos calcular, com um exemplo."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Olhar só o total gasto no mês, sem dividir pelas vendas.',top=620,size=56),"Erro comum: olhar só o valor total gasto."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('R$ 1.200 pode ser barato ou caro. Depende de quantas vendas ele trouxe.',top=620,size=54),"O valor gasto sozinho não diz se o anúncio está bom."),
 (2.4,'dark',head('PASSO 1','O GASTO','BL2')+"+"+tb([T('Gasto no mês','R$ 1.200'),T('Onde achar','painel de anúncios')],w1="'45%'"),"Passo 1: pegue o total gasto no mês, no painel de anúncios."),
 (2.4,'light',head('PASSO 2','AS VENDAS','BL')+"+"+tb([T('Vendas do anúncio','40'),T('Onde achar','mesmo painel')],w1="'45%'"),"Passo 2: veja quantas vendas vieram do anúncio."),
 (2.4,'accent',head('PASSO 3','O CUSTO POR VENDA')+"+(lt>.5?`<div class=\"t\" style=\"top:640px;font-size:280px;color:#fff;transform:scale(${eb((lt-.5)/.35)})\">R$ 30</div>`:'')+lbl('1.200 ÷ 40 = R$ 30',1000,'rgba(255,255,255,.85)',eo((lt-.8)/.3))","Passo 3: divida o gasto pelas vendas. R$ 30 por venda."),
 (2.6,'dark',head('PASSO 4','COMPARE','BL2')+"+"+tb([T('Lucro antes do anúncio','R$ 35'),T('Custo por venda','− R$ 30'),T('Sobra por venda','R$ 5'),T('No mês (40 vendas)','R$ 200','GR')],hiLast='true',w1="'50%'"),"Passo 4: compare com o lucro por venda antes do anúncio."),
 (2.4,'light',resumo(['Total gasto no mês','Vendas do anúncio','Divida um pelo outro','Compare com o lucro'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve e calcule o custo por venda do seu anúncio."),
]
N.NARR['t4_cac'] = [
 "Quanto custa cada venda que vem do seu anúncio? Vamos calcular, com um exemplo.",
 "O erro comum é olhar só o total gasto no mês, sem dividir pelas vendas.",
 "Por quê? Gastar R$ 1.200 pode ser barato ou caro. Depende de quantas vendas esse dinheiro trouxe.",
 "Passo 1: pegue o total gasto no mês, no painel de anúncios. No exemplo, R$ 1.200.",
 "Passo 2: veja quantas vendas vieram do anúncio, no mesmo painel. Aqui, 40.",
 "Passo 3: divida o gasto pelas vendas. 1.200 dividido por 40 dá R$ 30 por venda.",
 "Passo 4: compare com o lucro de cada venda antes do anúncio. Se sobram R$ 35, ficam R$ 5 por venda. No mês, R$ 200.",
 "Resumo: gasto do mês, vendas do anúncio, divida e compare com o lucro. Números de exemplo.",
 "Salve e calcule o custo por venda do seu anúncio.",
]
OUT['t4_cac'] = B('t4_cac', 'branco_diag', ('SALVE', 'E CALCULE'), t4, 'Salve e calcule o custo por venda do seu anúncio.')
t4b = list(t4); t4b[0] = (2.2, 'dark', "W(lt,[[0,'R$ 1.200',200],[.25,'EM ANÚNCIO',120,BL2],[.55,'SOBRARAM',120],[.8,'R$ 200',200,'#FF6B78']],300)", t4[0][3])
N.NARR['t4_cac_numero'] = ["R$ 1.200 em anúncio. Sobraram R$ 200. Veja a conta, com um exemplo."] + N.NARR['t4_cac'][1:]
OUT['t4_cac_numero'] = B('t4_cac_numero', 'branco_diag', ('SALVE', 'E CALCULE'), t4b, 'Salve e calcule o custo por venda do seu anúncio.')

# ---------- T5 · PONTO DE EQUILÍBRIO (Efeito) — 80 × 25% = 20 · 80 − 40 − 20 = 20 · 3.000 ÷ 20 = 150 ----------
t5 = [
 (2.2,'dark',"W(lt,[[0,'QUANTAS VENDAS',120],[.2,'PARA',110,BL2],[.4,'NÃO PERDER?',150]],380)","Quantas vendas por mês você precisa para não ter prejuízo? Vamos calcular."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Esquecer os custos fixos: ferramentas, contador, internet.',top=620,size=56),"Erro comum: esquecer os custos fixos do mês."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('Os custos fixos chegam todo mês, vendendo ou não.',top=620,size=56),"Eles chegam todo mês, vendendo ou não."),
 (2.6,'dark',head('PASSO 1','CUSTOS FIXOS','BL2')+"+"+tb([T('Ferramentas e apps','R$ 900'),T('Contador','R$ 600'),T('Internet, luz, outros','R$ 1.500'),T('Total no mês','R$ 3.000')],hiLast='true',w1="'55%'"),"Passo 1: some todos os custos fixos do mês."),
 (2.6,'light',head('PASSO 2','SOBRA POR VENDA','BL')+"+"+tb([T('Preço','R$ 80'),T('Custo do produto','− R$ 40'),T('Taxas (25%)','− R$ 20'),T('Sobra por venda','R$ 20')],hiLast='true',w1="'55%'"),"Passo 2: calcule quanto sobra de cada venda para pagar os fixos."),
 (2.4,'accent',head('PASSO 3','A CONTA')+"+(lt>.5?`<div class=\"t\" style=\"top:640px;font-size:300px;color:#fff;transform:scale(${eb((lt-.5)/.35)})\">150</div>`:'')+lbl('3.000 ÷ 20 = 150 vendas',1000,'rgba(255,255,255,.85)',eo((lt-.8)/.3))","Passo 3: divida os fixos pela sobra. 150 vendas por mês."),
 (2.4,'dark',head('PASSO 4','ACOMPANHE','BL2')+"+liquid(lt,{pct:60,top:560,t0:.3,dur:1,fill:BL2})","Passo 4: acompanhe o mês. Abaixo de 150, prejuízo; acima, lucro."),
 (2.4,'light',resumo(['Some os custos fixos','Calcule a sobra por venda','Divida um pelo outro','Acompanhe o mês'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve e calcule o seu ponto de equilíbrio."),
]
N.NARR['t5_equilibrio'] = [
 "Quantas vendas por mês você precisa para não ter prejuízo? Vamos calcular, com um exemplo.",
 "O erro comum é esquecer os custos fixos: ferramentas, contador, internet.",
 "Por quê? Eles chegam todo mês, vendendo ou não, e saem do lucro das vendas.",
 "Passo 1: some todos os custos fixos do mês. No exemplo, R$ 3 mil.",
 "Passo 2: calcule quanto sobra de cada venda. Preço de R$ 80, menos R$ 40 de custo e R$ 20 de taxas. Sobram R$ 20.",
 "Passo 3: divida os custos fixos pela sobra. 3 mil dividido por 20 dá 150 vendas por mês.",
 "Passo 4: acompanhe o mês. Abaixo de 150 vendas, prejuízo. Acima, cada venda vira lucro.",
 "Resumo: some os fixos, calcule a sobra por venda e divida. Números de exemplo.",
 "Salve e calcule o seu ponto de equilíbrio.",
]
OUT['t5_equilibrio'] = B('t5_equilibrio', 'preto_glow', ('SALVE', 'E CALCULE'), t5, 'Salve e calcule o seu ponto de equilíbrio.')
t5b = list(t5); t5b[0] = (3.4, 'dark', uiw(card('Este mês', 'Custos fixos: R$ 3.000', 'Vendas para empatar', '?', '#FFC94D'), "[1.0,'QUANTAS VENDAS',120],[1.2,'PARA',110,BL2],[1.45,'NÃO PERDER?',150]"), t5[0][3])
N.NARR['t5_equilibrio_ui'] = N.NARR['t5_equilibrio']
OUT['t5_equilibrio_ui'] = B('t5_equilibrio_ui', 'preto_glow', ('SALVE', 'E CALCULE'), t5b, 'Salve e calcule o seu ponto de equilíbrio.')

# ---------- T6 · TAXA DE CONVERSÃO (Duração) — 30 ÷ 2.000 = 1,5% · 2.000 × 2% = 40 ----------
t6 = [
 (2.2,'dark',"W(lt,[[0,'SEU ANÚNCIO',130],[.2,'CONVERTE',160,BL2],[.4,'BEM?',180]],380)","O seu anúncio converte bem? Vamos medir, com um exemplo."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Comemorar visitas sem saber quantas viram venda.',top=620,size=56),"Erro comum: comemorar visitas sem olhar as vendas."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('Visita não paga conta. O que importa é quantas viram pedido.',top=620,size=56),"Visita não paga conta. Pedido paga."),
 (2.4,'dark',head('PASSO 1','OS NÚMEROS','BL2')+"+"+tb([T('Visitas no mês','2.000'),T('Vendas','30'),T('Onde achar','métricas do anúncio')],w1="'45%'"),"Passo 1: pegue visitas e vendas do mês, nas métricas do anúncio."),
 (2.4,'light',head('PASSO 2','A CONTA','BL')+"+(lt>.5?`<div class=\"t\" style=\"top:640px;font-size:300px;color:#0A0B10;transform:scale(${eb((lt-.5)/.35)})\">1,5%</div>`:'')+lbl('30 ÷ 2.000 = 1,5%',1000,'#7A7F8C',eo((lt-.8)/.3))","Passo 2: divida vendas por visitas. 1,5%."),
 (2.6,'dark',head('PASSO 3','COMPARE','BL2')+"+"+tb([T('Anúncio A','2,4%'),T('Anúncio B','1,5%'),T('Anúncio C','0,6%','RD')],hiLast='true',w1="'45%'"),"Passo 3: compare com os seus outros anúncios e ataque o pior."),
 (2.6,'accent',head('PASSO 4','O GANHO')+"+"+tb([T('Mesmas 2.000 visitas',''),T('Conversão de 2%','40 vendas'),T('Ganho','+10 vendas','GR')],hiLast='true',w1="'55%'"),"Passo 4: subir para 2% dá 10 vendas a mais, sem pagar mais tráfego."),
 (2.4,'light',resumo(['Visitas e vendas do mês','Vendas ÷ visitas','Compare os anúncios','Melhore o pior primeiro'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve e calcule a conversão dos seus anúncios."),
]
N.NARR['t6_conversao'] = [
 "O seu anúncio converte bem? Vamos medir, com um exemplo.",
 "O erro comum é comemorar visitas sem saber quantas viram venda.",
 "Por quê? Visita não paga conta. O que importa é quantas pessoas compraram.",
 "Passo 1: pegue as visitas e as vendas do mês, nas métricas do anúncio. No exemplo, 2 mil visitas e 30 vendas.",
 "Passo 2: divida as vendas pelas visitas. 30 dividido por 2 mil dá 1,5%.",
 "Passo 3: compare com os seus outros anúncios. O que converte menos é o primeiro a melhorar: foto, título e preço.",
 "Passo 4: se subir de 1,5 para 2%, as mesmas 2 mil visitas viram 40 vendas. 10 a mais, sem pagar mais tráfego.",
 "Resumo: visitas e vendas, divida, compare e melhore o pior. Números de exemplo.",
 "Salve e calcule a conversão dos seus anúncios.",
]
OUT['t6_conversao'] = B('t6_conversao', 'azul_grade', ('SALVE', 'E MEÇA'), t6, 'Salve e calcule a conversão dos seus anúncios.')
N.NARR['t6_conversao_curta'] = [
 "O seu anúncio converte bem? Meça em 1 conta.",
 "Divida as vendas pelas visitas do mês. No exemplo, 30 dividido por 2 mil dá 1,5%.",
 "Compare com os seus outros anúncios e melhore o que converte menos.",
 "Subindo para 2%, as mesmas visitas viram 10 vendas a mais. Números de exemplo.",
 "Salve e calcule a conversão dos seus anúncios.",
]
OUT['t6_conversao_curta'] = B('t6_conversao_curta', 'azul_grade', ('SALVE', 'E MEÇA'), [t6[i] for i in (0, 4, 5, 6)], 'Salve e calcule a conversão dos seus anúncios.')

# ---------- T7 · ANTECIPAÇÃO (Narração) — 1,5% × 4 = 6% · 1.000 × 6% = 60 (aproximação simples) ----------
t7 = [
 (2.2,'dark',"W(lt,[[0,'ANTECIPAR',160],[.2,'O DINHEIRO',130,BL2],[.4,'COMPENSA?',150]],380)","Antecipar o dinheiro das vendas compensa? Vamos fazer a conta."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Antecipar tudo, todo mês, sem olhar a taxa.',top=620,size=56),"Erro comum: antecipar tudo sem olhar a taxa."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('A antecipação cobra uma taxa por mês que você recebe antes. Ela sai da margem.',top=620,size=52),"A taxa da antecipação sai direto da sua margem."),
 (2.4,'dark',head('PASSO 1','A TAXA','BL2')+"+"+tb([T('Taxa ao mês','1,5% (exemplo)'),T('Onde achar','contrato ou painel de pagamentos')],w1="'40%'"),"Passo 1: veja a taxa mensal no contrato ou no painel de pagamentos."),
 (2.4,'light',head('PASSO 2','OS MESES','BL')+"+"+tb([T('Recebe antes','4 meses'),T('Taxa total','1,5% × 4 = 6%')],hiLast='true',w1="'45%'"),"Passo 2: multiplique pela quantidade de meses que vai receber antes."),
 (2.4,'accent',head('PASSO 3','EM REAIS')+"+(lt>.5?`<div class=\"t\" style=\"top:640px;font-size:280px;color:#fff;transform:scale(${eb((lt-.5)/.35)})\">R$ 60</div>`:'')+lbl('6% de R$ 1.000 = R$ 60',1000,'rgba(255,255,255,.85)',eo((lt-.8)/.3))","Passo 3: aplique sobre o valor. R$ 60 a cada R$ 1.000."),
 (2.6,'dark',head('PASSO 4','COMPARE','BL2')+"+"+tb([T('Sua margem','15%'),T('Antecipação','− 6%'),T('Sobra','9%','RD')],hiLast='true',w1="'45%'"),"Passo 4: compare com a sua margem. Aqui, a antecipação leva 6 de 15 pontos."),
 (2.4,'light',resumo(['Veja a taxa mensal','Multiplique pelos meses','Calcule em reais','Compare com a margem'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve e confira quanto a antecipação te custa."),
]
N.NARR['t7_antecipa'] = [
 "Antecipar o dinheiro das vendas parceladas compensa? Vamos fazer a conta, com um exemplo.",
 "O erro comum é antecipar tudo, todo mês, sem olhar a taxa.",
 "Por quê? A antecipação cobra uma taxa por mês que você recebe antes. E essa taxa sai direto da sua margem.",
 "Passo 1: veja a taxa mensal no contrato ou no painel de pagamentos. No exemplo, 1,5% ao mês.",
 "Passo 2: multiplique pelos meses que vai receber antes. 4 meses vezes 1,5% dá 6%, numa conta aproximada.",
 "Passo 3: aplique sobre o valor. A cada R$ 1.000 antecipados, R$ 60 ficam com a operadora.",
 "Passo 4: compare com a sua margem. Se ela é 15%, a antecipação leva 6 desses 15 pontos.",
 "Resumo: taxa mensal, vezes os meses, em reais, comparado com a margem. Antecipe só quando precisar. Números de exemplo.",
 "Salve e confira quanto a antecipação está te custando.",
]
OUT['t7_antecipa'] = B('t7_antecipa', 'branco_pontos', ('SALVE', 'E CONFIRA'), t7, 'Salve e confira quanto a antecipação te custa.')

# ---------- T8 · ESTOQUE PARADO (Gancho) — 10.000 ÷ 2.500 = 4 meses · 2 meses = 5.000 · 10.000 − 5.000 = 5.000 ----------
t8 = [
 (2.2,'dark',"W(lt,[[0,'SEU DINHEIRO',140],[.2,'ESTÁ PARADO',140,BL2],[.4,'NO ESTOQUE?',140]],380)","Quanto do seu dinheiro está parado no estoque? Vamos calcular."),
 (2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Recomprar tudo sem saber quantos meses de estoque você já tem.',top=620,size=54),"Erro comum: recomprar sem saber quanto já tem parado."),
 (2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('Estoque parado é dinheiro que não volta para o caixa.',top=620,size=56),"Estoque parado é dinheiro que não volta para o caixa."),
 (2.4,'dark',head('PASSO 1','O ESTOQUE','BL2')+"+"+tb([T('Estoque a preço de custo','R$ 10.000')],w1="'60%'"),"Passo 1: some o estoque pelo preço de custo."),
 (2.4,'light',head('PASSO 2','O GIRO','BL')+"+"+tb([T('Custo do que vendeu no mês','R$ 2.500')],w1="'60%'"),"Passo 2: veja o custo do que você vendeu no mês."),
 (2.4,'accent',head('PASSO 3','A COBERTURA')+"+(lt>.5?`<div class=\"t\" style=\"top:640px;font-size:260px;color:#fff;transform:scale(${eb((lt-.5)/.35)})\">4 MESES</div>`:'')+lbl('10.000 ÷ 2.500 = 4 meses',1000,'rgba(255,255,255,.85)',eo((lt-.8)/.3))","Passo 3: divida um pelo outro. 4 meses de estoque."),
 (2.6,'dark',head('PASSO 4','AJUSTE','BL2')+"+"+tb([T('Meta (exemplo)','2 meses = R$ 5.000'),T('Parado a mais','R$ 5.000','RD'),T('O que fazer','kit, promoção, pausar recompra')],hiLast='true',w1="'40%'"),"Passo 4: acima da meta, pare de recomprar e gire o que está parado."),
 (2.4,'light',resumo(['Estoque a custo','Custo das vendas do mês','Divida = meses de estoque','Acima da meta, gire'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#7A7F8C')","Salve e calcule os meses de estoque da sua loja."),
]
N.NARR['t8_estoque'] = [
 "Quanto do seu dinheiro está parado no estoque? Vamos calcular, com um exemplo.",
 "O erro comum é recomprar tudo sem saber quantos meses de estoque você já tem.",
 "Por quê? Estoque parado é dinheiro que não volta para o caixa, e falta para recomprar o que vende.",
 "Passo 1: some o estoque pelo preço de custo. No exemplo, R$ 10 mil.",
 "Passo 2: veja o custo do que você vendeu no último mês. Aqui, R$ 2.500.",
 "Passo 3: divida um pelo outro. 10 mil dividido por 2.500 dá 4 meses de estoque.",
 "Passo 4: se a sua meta é 2 meses, são R$ 5 mil parados a mais. Pare de recomprar esses itens e gire com kit ou promoção.",
 "Resumo: estoque a custo, dividido pelo custo das vendas do mês, igual a meses de estoque. Números de exemplo.",
 "Salve e calcule os meses de estoque da sua loja.",
]
OUT['t8_estoque'] = B('t8_estoque', 'preto_aneis', ('SALVE', 'E GIRE'), t8, 'Salve e calcule os meses de estoque da sua loja.')
t8b = list(t8); t8b[0] = (2.2, 'dark', "W(lt,[[0,'R$ 10.000',190],[.25,'NO ESTOQUE',120,BL2],[.55,'4 MESES',190,'#FF6B78'],[.8,'PARA VENDER',120]],300)", t8[0][3])
N.NARR['t8_estoque_numero'] = ["R$ 10 mil no estoque. 4 meses para vender. Veja a conta, com um exemplo."] + N.NARR['t8_estoque'][1:]
OUT['t8_estoque_numero'] = B('t8_estoque_numero', 'preto_aneis', ('SALVE', 'E GIRE'), t8b, 'Salve e calcule os meses de estoque da sua loja.')
import json
json.dump({k: v for k, v in N.NARR.items() if k.startswith('t')}, open('narr_testes.json', 'w'), ensure_ascii=False, indent=1)
print(OUT)
