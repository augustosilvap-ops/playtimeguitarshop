"""Reels de TESTE (Instagram 'Reel de teste' — só para não seguidores), 2 pares por dia, 17–20/11.
Cada par muda UMA variável. Cada variável é testada 2 vezes com conteúdos diferentes.
Gera augusto/entregas/testes_reels/ (vídeos A/B por par, GUIA.md) e Testes_Reels.xlsx (planilha de resultados).
Rodar em augusto/: python3 editorial/testes_reels.py"""
import os, shutil, json
E = 'entregas'
AB = '/tmp/claude-0/drive/ab2'
PARES = [
 # (dia, hora, par, variável, conteúdo inédito, A, B, chave da legenda) — conteúdos que NÃO estão no feed
 ('17/11', '13h', 9, 'Formato', 'DESCONTO', (f'{E}/testes/formatos/DESCONTO_conversa_narrado_43s.mp4', 'formato conversa de DM'), (f'{E}/testes/formatos/DESCONTO_planilha_narrado_38s.mp4', 'formato planilha ao vivo'), 'desc'),
 ('17/11', '11h', 1, 'Efeito', 'CLASSICO', (f'{AB}/t1_A.mp4', 'abertura normal'), (f'{AB}/t1_B.mp4', 'abertura "mundo de interface"'), 't1'),
 ('17/11', '15h', 2, 'Duração', 'ABC', (f'{AB}/t2_A.mp4', 'completa'), (f'{AB}/t2_B.mp4', 'curta'), 't2'),
 ('18/11', '11h', 3, 'Narração', 'CUBADO', (f'{AB}/t3_A.mp4', 'com voz'), (f'{AB}/t3_B.mp4', 'sem voz (só legenda + trilha)'), 't3'),
 ('18/11', '15h', 4, 'Gancho', 'CAC', (f'{AB}/t4_A.mp4', 'gancho pergunta ("Quanto custa cada venda?")'), (f'{AB}/t4_B.mp4', 'gancho número ("R$ 1.200 → sobraram R$ 200")'), 't4'),
 ('19/11', '11h', 5, 'Efeito', 'EQUILIBRIO', (f'{AB}/t5_A.mp4', 'abertura normal'), (f'{AB}/t5_B.mp4', 'abertura "mundo de interface"'), 't5'),
 ('19/11', '15h', 6, 'Duração', 'CONVERSAO', (f'{AB}/t6_A.mp4', 'completa'), (f'{AB}/t6_B.mp4', 'curta'), 't6'),
 ('20/11', '11h', 7, 'Narração', 'ANTECIPA', (f'{AB}/t7_A.mp4', 'com voz'), (f'{AB}/t7_B.mp4', 'sem voz (só legenda + trilha)'), 't7'),
 ('20/11', '15h', 8, 'Gancho', 'ESTOQUE', (f'{AB}/t8_A.mp4', 'gancho pergunta ("Dinheiro parado no estoque?")'), (f'{AB}/t8_B.mp4', 'gancho número ("R$ 10.000 → 4 meses para vender")'), 't8'),
]
H = '#marketplace #ecommerce #vendasonline #mercadolivre #shopee'
LEG = {
 'desc': 'A Black Friday é em 27/11. Antes de colocar "-30%" em tudo, faça uma conta de 1 minuto.\n\n1. Descubra o seu preço mínimo: custo por unidade ÷ (1 − soma dos % cobrados na venda).\n2. Defina a menor margem que você aceita na promoção (ex.: 5%).\n3. Calcule o preço da oferta: custo ÷ (1 − % da venda − margem mínima).\n4. Compare com o preço atual: esse é o seu desconto máximo.\n\nExemplo hipotético: custo R$ 48,50, 27% de taxas, preço R$ 83,90 e margem mínima de 5%. O desconto máximo é 15%. Um cupom de 20% deixaria a margem abaixo de 1%.\n\n🔖 Salve e faça essa conta com cada produto antes de definir o desconto.\n↗ Envie para quem vai fazer Black Friday este ano.\n\n#blackfriday #precificacao #marketplace #ecommerce #vendasonline',
 't1': f"""Clássico ou Premium? Antes de escolher, faça esta conta.\n\n1. Veja a comissão de cada tipo na tabela da sua categoria.\n2. Calcule o lucro de uma venda em cada um.\n3. Divida o lucro do Clássico pelo do Premium.\n4. O resultado diz quanto o Premium precisa vender a mais para empatar.\n\nExemplo hipotético: produto de R$ 100, custo R$ 50, imposto 6%. Clássico a 12% deixa R$ 32; Premium a 17% deixa R$ 27. 32 ÷ 27 = 1,19 → o Premium precisa vender 19% a mais.\n\n🔖 Salve antes do próximo anúncio.\n💬 Seus anúncios estão em qual tipo hoje?\n\n{H}""",
 't2': f"""Nem todo produto merece a mesma atenção. A curva ABC mostra quais pagam as suas contas.\n\n1. Exporte as vendas dos últimos 90 dias, por produto.\n2. Ordene do maior para o menor faturamento.\n3. Some o acumulado: até 80% é curva A, de 80% a 95% é B, o resto é C.\n4. A nunca falta estoque · B melhore os anúncios · C revise ou tire.\n\nExemplo hipotético: de R$ 50 mil, 20 produtos fazem R$ 40 mil (80%).\n\n🔖 Salve e faça a sua curva ABC esta semana.\n↗ Envie para quem tem loja com muitos produtos.\n\n{H}""",
 't3': f"""Seu frete pode estar caro por causa da caixa, não do produto.\n\nA transportadora cobra o MAIOR entre o peso real e o peso cubado:\nComprimento × largura × altura (cm) ÷ fator da transportadora.\n\nExemplo hipotético (fator 6.000): caixa de 40 × 30 × 20 = 24.000 ÷ 6.000 = 4 kg. O produto pesa 1,2 kg, mas você paga por 4 kg. Trocando por uma caixa de 30 × 20 × 15, o cubado cai para 1,5 kg.\n\nConfira o fator da sua transportadora.\n\n🔖 Salve e meça as caixas dos seus 5 mais vendidos.\n💬 Você já tinha ouvido falar em peso cubado?\n\n{H}""",
 't4': f"""Gastar R$ 1.200 em anúncio é caro ou barato? Depende de quantas vendas vieram.\n\n1. Pegue o total gasto no mês (painel de anúncios).\n2. Veja quantas vendas vieram do anúncio.\n3. Divida: esse é o custo por venda.\n4. Compare com o lucro de cada venda antes do anúncio.\n\nExemplo hipotético: R$ 1.200 ÷ 40 vendas = R$ 30 por venda. Se sobravam R$ 35 antes do anúncio, ficam R$ 5 por venda — R$ 200 no mês.\n\n🔖 Salve e calcule o custo por venda do seu anúncio.\n💬 Quanto custa cada venda sua hoje?\n\n{H}""",
 't5': f"""Quantas vendas por mês você precisa para não ter prejuízo? Esse é o ponto de equilíbrio.\n\n1. Some os custos fixos do mês (ferramentas, contador, internet…).\n2. Calcule quanto sobra de cada venda: preço − custo − taxas.\n3. Divida os fixos pela sobra.\n\nExemplo hipotético: R$ 3.000 de fixos. Preço R$ 80 − R$ 40 de custo − R$ 20 de taxas = R$ 20 por venda. 3.000 ÷ 20 = 150 vendas por mês.\n\nAbaixo disso, prejuízo. Acima, cada venda vira lucro.\n\n🔖 Salve e calcule o seu ponto de equilíbrio.\n↗ Envie para quem está começando a vender.\n\n{H}""",
 't6': f"""Visita não paga conta. O que paga é visita que vira pedido.\n\nTaxa de conversão = vendas ÷ visitas.\n\n1. Pegue visitas e vendas do mês nas métricas do anúncio.\n2. Divida.\n3. Compare com os seus outros anúncios.\n4. Melhore primeiro o que converte menos (foto, título, preço).\n\nExemplo hipotético: 30 vendas ÷ 2.000 visitas = 1,5%. Subindo para 2%, as mesmas visitas viram 40 vendas — 10 a mais sem pagar tráfego.\n\n🔖 Salve e calcule a conversão dos seus anúncios.\n💬 Qual é a conversão do seu melhor anúncio?\n\n{H}""",
 't7': f"""Antecipar o dinheiro das vendas parceladas tem custo. Faça a conta antes.\n\n1. Veja a taxa mensal no contrato ou no painel de pagamentos.\n2. Multiplique pelos meses que vai receber antes.\n3. Aplique sobre o valor.\n4. Compare com a sua margem.\n\nExemplo hipotético (conta aproximada): 1,5% ao mês × 4 meses = 6%. A cada R$ 1.000, R$ 60 ficam com a operadora. Com margem de 15%, a antecipação leva 6 desses 15 pontos.\n\nAntecipe quando precisar, não por hábito.\n\n🔖 Salve e confira quanto a antecipação te custa.\n\n{H}""",
 't8': f"""Estoque parado é dinheiro que não volta para o caixa.\n\nMeses de estoque = estoque a preço de custo ÷ custo do que vendeu no mês.\n\nExemplo hipotético: R$ 10.000 em estoque ÷ R$ 2.500 vendidos no mês = 4 meses. Com meta de 2 meses, são R$ 5.000 parados a mais.\n\nO que fazer: pare de recomprar esses itens e gire com kit ou promoção.\n\n🔖 Salve e calcule os meses de estoque da sua loja.\n💬 Quantos meses de estoque você tem hoje?\n\n{H}""",
}

def dur(f):
    import subprocess
    return round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout or 0))

def main():
    D = f'{E}/testes_reels'; os.makedirs(D, exist_ok=True)
    md = ['# Reels de TESTE — 2 pares por dia (17 a 20/11)\n',
          'Como postar: no app, ao publicar o Reel, ative **"Reel de teste"** (vai só para quem não te segue). Poste o **A e o B do mesmo par com até 10 minutos de diferença**, com a mesma legenda e a mesma capa. Não promova nenhum dos dois para o feed antes da leitura.\n',
          'Leitura: **72 h depois**, anote na planilha `Testes_Reels.xlsx`: visualizações, % que passou dos 3 s (retenção inicial), tempo médio assistido, salvamentos, compartilhamentos e novos seguidores. Me manda os prints ou os números que eu analiso.\n',
          'Regra de decisão: vence quem tiver **tempo médio assistido + compartilhamentos** maiores. Diferença menor que 10% = empate.\n',
          '\n| Dia | Hora | Par | Variável | Conteúdo | A | B |\n|---|---|---|---|---|---|---|\n']
    rows = []
    for dia, hora, par, var, cont, A, B, leg in PARES:
        fa, fb = f'{D}/par{par:02d}_{cont}_A.mp4', f'{D}/par{par:02d}_{cont}_B.mp4'
        shutil.copy(A[0], fa); shutil.copy(B[0], fb)
        da, db = dur(fa), dur(fb)
        md.append(f'| {dia} | {hora} | {par} | {var} | {cont} | {A[1]} ({da} s) | {B[1]} ({db} s) |\n')
        rows.append((dia, hora, par, var, cont, f'{A[1]} ({da} s)', f'{B[1]} ({db} s)', leg))
    md.append('\n## Legendas\nConteúdos INÉDITOS (não estão no feed). Use a mesma legenda nos dois vídeos do par:\n\n')
    for dia, hora, par, var, cont, a, b, k in rows:
        cap = LEG[k]
        md.append(f'### Par {par} · {cont}\n\n{cap}\n\n')
    open(f'{D}/GUIA.md', 'w').write(''.join(md))
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook(); ws = wb.active; ws.title = 'Resultados'
    H = ['Dia', 'Hora', 'Par', 'Variável', 'Conteúdo', 'Versão', 'Descrição', 'Visualizações', '% passou dos 3 s', 'Tempo médio (s)', 'Salvamentos', 'Compartilhamentos', 'Novos seguidores', 'Vencedor?']
    ws.append(H)
    for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='08090E'); c.alignment = Alignment(wrap_text=True)
    for dia, hora, par, var, cont, a, b, _ in rows:
        ws.append([dia, hora, par, var, cont, 'A', a] + [None] * 7)
        ws.append([dia, hora, par, var, cont, 'B', b] + [None] * 7)
    for i, w in enumerate([7, 6, 5, 11, 11, 7, 42, 13, 13, 13, 12, 14, 13, 10], 1): ws.column_dimensions[chr(64 + i)].width = w
    wb.save(f'{D}/Testes_Reels.xlsx'); print(len(rows), 'pares')

if __name__ == '__main__': main()
