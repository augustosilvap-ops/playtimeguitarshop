"""Posts de 18–20/11 (5 por dia: 10h, 12h, 16h, 18h, 20h) — SEM presente (Manychat pendente).
Gera: entregas/2026-11-18_a_20_SEM_PRESENTE.md, pacotes augusto/publicacao/<data>/<id>.json (status: aguardando aprovação)
e mídias públicas em nexus-site/public/ig/<dd>/. Rodar em augusto/: python3 editorial/semana2.py"""
import json, os, shutil
from PIL import Image
U = 'https://nexusautomatic.vercel.app/ig/'
TAGS = {'ia': '#ia #marketplace #produtos #mercadolivre #shopee', 'mkt': '#marketplace #mercadolivre #shopee #ecommerce #vendasonline',
        'prec': '#precificacao #marketplace #ecommerce #vendasonline #margem', 'black': '#blackfriday #marketplace #ecommerce #vendasonline #precificacao'}
P = [
 # (data, hora, id, tipo, pasta, titulo, legenda)
 ('2026-11-18', '10:00', '13', 'carrossel', '2026-11-18/13_carrossel_demanda', 'Validar demanda com IA sem inventar números', f"""A IA não sabe quanto um produto vende. Se você pergunta, ela chuta — e chute vira estoque parado.

O jeito certo é usar a IA para organizar os dados que VOCÊ coletou:

1. Digite o produto na busca do marketplace e anote os 10 primeiros anúncios: preço, avaliações, vendas exibidas e frete.
2. Cole na IA e peça uma tabela com média e faixa de preço. Escreva no prompt: "não invente nenhum dado".
3. Leia os sinais: avaliações recentes no topo, o termo nas sugestões da busca e vendas exibidas nos 5 primeiros.
4. Peça uma nota de 0 a 10 para demanda, concorrência e margem, explicando o motivo com base nos dados.

Notas fortes? Teste com um lote pequeno antes de comprar grande. (Notas do slide 6 são um exemplo hipotético.)

🔖 Salve para usar antes da próxima compra.
💬 Você já comprou estoque porque "parecia que vendia"?

{TAGS['ia']}"""),
 ('2026-11-18', '12:00', '14', 'estatico', '2026-11-18/14_estatico_frete', 'O custo que você esquece: o frete', f"""Frete grátis para o cliente quase nunca é grátis para você.

Antes de fechar o preço, some o que sai do seu bolso em cada pedido:

→ A parte do frete que o canal cobra de você (confira a tabela de frete do seu marketplace).
→ Caixa, fita, plástico bolha e etiqueta.
→ Reenvio quando o pacote extravia ou volta.

Exemplo hipotético: produto de R$ 89,90 com R$ 18,00 de frete pago por você e R$ 3,20 de embalagem. São R$ 21,20 por pedido — 23,6% do preço — antes de comissão, imposto e custo do produto.

Se esse valor não está na sua conta de preço, ele está saindo da sua margem.

🔖 Salve e confira o frete do seu produto mais vendido hoje.
↗ Envie para quem oferece frete grátis sem fazer conta.

{TAGS['mkt']}"""),
 ('2026-11-18', '18:00', '15', 'reel', '2026-11-18/15_reel_titulo', 'Títulos de anúncio melhores com IA', f"""Seu anúncio pode estar ótimo e mesmo assim não aparecer. O motivo costuma estar no título.

A busca compara o título com o que o cliente digita. "Barato", "promoção" e "envio rápido" ninguém pesquisa.

1. Pesquise: digite o produto na busca e anote as sugestões e as palavras que se repetem nos títulos do topo.
2. Use a fórmula: produto + marca/modelo + característica principal + variação.
3. Monte sem repetir palavras e sem símbolos. Ex.: Garrafa Térmica Inox Pro 1 Litro 24h Gelada Preta.
4. Peça 5 versões para a IA, com o limite de caracteres do seu canal, e escolha a mais clara.
5. Troque e compare a taxa de cliques depois de 7 dias.

No exemplo (hipotético), a taxa de cliques foi de 0,8% para 2,4%.

🔖 Salve e reescreva hoje o título do seu anúncio principal.
💬 Me conta: qual palavra inútil você vai tirar do seu título?

{TAGS['ia']}"""),
 ('2026-11-18', '20:00', '22', 'estatico', '2026-11-18/22_estatico_ticket', 'Ticket médio: o número que ninguém olha', f"""Todo mundo olha faturamento. Pouca gente olha o ticket médio — e ele é uma das alavancas mais rápidas de lucro.

Ticket médio = faturamento ÷ número de pedidos.

Exemplo hipotético: R$ 14.400 em 200 pedidos = R$ 72 por pedido.

Se cada pedido subir R$ 10, são R$ 2.000 a mais no mês, sem precisar de um cliente novo. E o frete e a embalagem continuam sendo de um pedido só.

Como subir sem dar desconto:
→ Kit com um complemento (produto + acessório).
→ Frete grátis a partir de um valor um pouco acima do seu ticket atual.
→ Versão maior ou pacote com mais unidades.

🔖 Salve e calcule o ticket médio da sua loja hoje.
💬 Qual é o seu ticket médio? Conta aqui.

{TAGS['mkt']}"""),
 ('2026-11-19', '10:00', '16', 'carrossel', '2026-11-19/16_carrossel_erros', '7 erros de quem começa no marketplace', f"""Quase todo mundo que começa no marketplace comete pelo menos um destes 7 erros. Confira se algum é seu:

1. Somar os % ao custo. As taxas são cobradas sobre o preço — a conta certa é dividir.
2. Escolher a categoria errada. Ela muda a comissão e onde o produto aparece.
3. Título com "promoção" e "barato". Use as palavras que o cliente digita.
4. Foto escura ou com texto por cima. A primeira foto decide o clique.
5. Esquecer o frete na conta. A parte que você paga entra no custo.
6. Comprar estoque grande sem teste. Comece com um lote pequeno.
7. Deixar pergunta sem resposta. Quem responde primeiro costuma levar a venda.

🔖 Salve e confira os 7 nos seus anúncios hoje.
↗ Envie para alguém que está começando agora.

{TAGS['mkt']}"""),
 ('2026-11-19', '12:00', '17', 'estatico', '2026-11-19/17_estatico_devolucao', 'Devolução também é custo', f"""Toda loja tem devolução. O problema é não colocar ela na conta.

Cada devolução custa o frete de volta e, muitas vezes, um produto que não pode ser vendido de novo.

Exemplo hipotético:
→ 200 vendas no mês, 6 devoluções (3%).
→ Custo médio de R$ 25 por devolução.
→ 6 × R$ 25 = R$ 150 no mês.
→ R$ 150 ÷ 200 vendas = R$ 0,75 por venda.

Esses R$ 0,75 (ou o % equivalente) entram na sua conta de preço como reserva. Assim a devolução não come o lucro quando acontece.

Para achar o seu número: veja no painel do canal quantas devoluções teve nos últimos 3 meses e quanto cada uma custou.

🔖 Salve e calcule a sua reserva para devoluções.
💬 Qual é o motivo de devolução que mais aparece na sua loja?

{TAGS['prec']}"""),
 ('2026-11-19', '16:00', '26', 'estatico', '2026-11-19/26_estatico_repor', 'Estoque mínimo: a hora certa de repor', f"""Faltar estoque derruba o anúncio. Sobrar estoque prende o seu dinheiro. O ponto de pedido resolve os dois.

Ponto de pedido = vendas por dia × prazo do fornecedor + estoque de segurança.

Exemplo hipotético:
→ Vende 4 por dia.
→ O fornecedor leva 10 dias para entregar.
→ Estoque de segurança de 12 unidades (3 dias de venda).
→ 4 × 10 + 12 = 52.

Quando o estoque chegar em 52 unidades, faça o pedido. Ele chega antes de acabar.

Onde achar os números: vendas por dia no relatório dos últimos 30 dias ÷ 30; prazo real das últimas entregas do fornecedor.

🔖 Salve e calcule o ponto de pedido dos seus 5 mais vendidos.
↗ Envie para quem vive ficando sem estoque.

{TAGS['mkt']}"""),
 ('2026-11-19', '18:00', '18', 'reel', '2026-11-19/18_reel_rotina', 'Rotina para organizar os pedidos', f"""Pedido acumulando, prazo estourando, cliente reclamando. Quase sempre o problema é a falta de rotina, não de tempo.

Uma rotina simples que dá conta:

1. Horário fixo, sempre na mesma ordem: 9h separar, 10h etiquetas, 11h embalar e conferir, 12h postar, 17h mensagens.
2. Descubra o horário de corte da transportadora (fica no painel do canal) e poste antes dele.
3. Antes de fechar a caixa, confira 4 itens: produto certo, cor e tamanho, etiqueta do pedido certo e embalagem protegida.
4. Reserve um horário só para responder mensagens.

Acompanhe toda semana a sua taxa de envio no prazo. No exemplo (hipotético), a meta é 98%.

🔖 Salve e cole na parede do estoque.
💬 Qual parte da sua rotina mais atrasa hoje?

{TAGS['mkt']}"""),
 ('2026-11-19', '20:00', '23', 'reel', '2026-11-19/23_reel_roas', 'Quanto investir em anúncios sem perder dinheiro', f"""O anúncio vendeu R$ 900 e parece ótimo. Mas deu lucro?

Exemplo hipotético: R$ 900 em vendas − R$ 405 de custo dos produtos − R$ 243 de taxas − R$ 500 de anúncio = R$ 248 de prejuízo.

Como conferir os seus:
1. ROAS = vendas geradas pelo anúncio ÷ valor gasto. Os dois estão no painel de anúncios. No exemplo: 900 ÷ 500 = 1,8.
2. Veja quanto sobra de cada venda antes do anúncio: preço − custo do produto − taxas. No exemplo, 28%.
3. ROAS mínimo = 1 ÷ essa sobra. 1 ÷ 0,28 = 3,6.
4. Abaixo do mínimo, o anúncio dá prejuízo: ajuste público, foto e título, ou anuncie um produto com margem maior.

🔖 Salve e confira o ROAS dos seus anúncios hoje.
💬 Você sabe o ROAS mínimo do seu produto principal?

{TAGS['prec']}"""),
 ('2026-11-20', '10:00', '19', 'carrossel', '2026-11-20/19_carrossel_pronto', 'Checklist antes da Black Friday (27/11)', f"""Faltam 7 dias para a Black Friday (27/11). O que você não preparar até lá, vai improvisar no dia.

Checklist:

1. Desconto máximo por produto: custo ÷ (1 − taxas − margem mínima). Acima disso, é prejuízo.
2. Estoque para a demanda: confira os 10 mais vendidos e peça reposição já.
3. Anúncios revisados: foto, título com as palavras da busca e preço comparado ao topo.
4. Frete e envio testados: horário de corte, embalagens e etiquetas em estoque.
5. Respostas prontas para as perguntas que mais chegam.
6. Oferta com limite e prazo: quantas unidades, até quando e qual a meta de lucro.

(Valores dos slides são exemplos hipotéticos.)

🔖 Salve e marque o que ainda falta.
↗ Envie para quem vai fazer Black Friday este ano.

{TAGS['black']}"""),
 ('2026-11-20', '12:00', '20', 'estatico', '2026-11-20/20_estatico_sobra', 'De cada R$ 100, o que sobra?', f"""Você vende R$ 100. Quanto disso é seu?

Exemplo hipotético de para onde vai o dinheiro:
→ Produto: R$ 45
→ Comissão: R$ 14
→ Frete e embalagem: R$ 8
→ Imposto: R$ 6
→ Anúncios: R$ 5
→ Devoluções: R$ 2
→ Sobra: R$ 20

Faça a mesma conta com o seu produto principal: pegue o preço, tire cada custo em reais e veja o que fica. Se a sobra for pequena, é ali que você mexe antes de vender mais.

Os percentuais mudam por canal, categoria e regime de imposto — confira a tabela do seu marketplace e a alíquota com o seu contador.

🔖 Salve e faça a sua conta hoje.
💬 Quanto sobra de cada R$ 100 na sua loja?

{TAGS['prec']}"""),
 ('2026-11-20', '16:00', '25', 'carrossel', '2026-11-20/25_carrossel_avalia', 'Como responder avaliação negativa', f"""Avaliação negativa não precisa afastar cliente. Bem respondida, ela vende.

Quem vai comprar lê as negativas primeiro. A sua resposta não é para quem reclamou — é para os próximos compradores.

Como responder:
1. Agradeça e cite o problema que a pessoa contou. Nada de resposta copiada.
2. Explique o que aconteceu sem culpar o cliente. Nunca discuta em público.
3. Diga o que mudou (ex.: reforçamos a embalagem).
4. Ofereça a solução pelo canal oficial: troca, devolução ou contato.

Responda no mesmo dia. Resposta rápida mostra que a loja está presente.

🔖 Salve o modelo para a próxima avaliação.
↗ Envie para quem tem medo de avaliação ruim.

{TAGS['mkt']}"""),
 ('2026-11-20', '18:00', '21', 'reel', '2026-11-20/21_reel_atende', 'Atendimento rápido com IA', f"""O cliente pergunta para várias lojas ao mesmo tempo. Quem responde primeiro costuma levar a venda.

Como montar um atendimento rápido com IA:

1. Escreva a base da loja: prazo de envio, frete, trocas, pagamento e tom de voz.
2. Liste as perguntas que mais chegam e a resposta certa de cada uma.
3. Cole a base no prompt: "Você é atendente da minha loja. Responda com simpatia, em até 3 linhas, usando só esta base. Se não souber, diga que vai confirmar."
4. A IA rascunha, você revisa e envia. Nunca deixe a IA inventar prazo ou preço.

No exemplo (hipotético), o tempo de resposta caiu de 6 horas para 5 minutos.

🔖 Salve e monte a base da sua loja hoje.
💬 Quanto tempo você leva hoje para responder um cliente?

{TAGS['ia']}"""),
 ('2026-11-20', '20:00', '24', 'carrossel', '2026-11-20/24_carrossel_combo', 'Kit e combo: venda mais sem dar desconto', f"""Desconto sai inteiro do seu lucro. Kit aumenta o pedido sem cortar o preço.

Como montar:
1. Junte o produto com um complemento que o cliente também precisa (garrafa + capa térmica).
2. Faça a conta com as taxas sobre o preço do kit.
3. Mostre a economia em relação a comprar separado.
4. Teste por 14 dias, com o kit ao lado do produto sozinho, e compare o lucro por pedido.

Exemplo hipotético (taxas de 27%):
→ Garrafa sozinha a R$ 89,90 (custo R$ 38): lucro de R$ 27,63.
→ Kit a R$ 109,90 (custo R$ 47): lucro de R$ 33,23.
→ +R$ 5,60 por pedido, e o cliente economiza R$ 9,90.

🔖 Salve e monte o seu primeiro kit.
↗ Envie para quem só pensa em desconto.

{TAGS['prec']}"""),
]
REELS = {'15': ('titulo', 'branco'), '18': ('rotina', ''), '23': ('roas', ''), '21': ('atende', '')}

def main(root='.'):
    md = ['# 18 a 20/11 — versão SEM presente (5 posts por dia)\n', 'Aprovação no Nexus. Publicação automática pelo Windsor no horário, só depois de aprovado.\n']
    for data, hora, pid, tipo, pasta, tit, leg in P:
        dd = data[-2:]; D = f'{root}/../nexus-site/public/ig/{dd}/'; os.makedirs(D, exist_ok=True)
        E = f'{root}/entregas/{pasta}/'
        if tipo == 'carrossel':
            sl = sorted(f for f in os.listdir(E + 'slides') if f.endswith('.png'))
            for f in sl: Image.open(E + 'slides/' + f).convert('RGB').save(f'{D}{pid}_{f[:2]}.jpg', quality=92)
            params = {'image_urls': [f'{U}{dd}/{pid}_{f[:2]}.jpg' for f in sl], 'caption': leg}; acao = 'create_carousel_post'; arq = f'slides/01–{len(sl):02d}.png'
        elif tipo == 'estatico':
            Image.open(E + 'arte.png').convert('RGB').save(f'{D}{pid}.jpg', quality=92)
            params = {'image_url': f'{U}{dd}/{pid}.jpg', 'caption': leg}; acao = 'create_image_post'; arq = 'arte.png'
        else:
            v = [f for f in os.listdir(E) if f.startswith('reel_narrado')][0]
            shutil.copy(E + v, f'{D}{pid}.mp4')
            capa = 'capa_aula_1080x1920.png' if os.path.exists(E + 'capa_aula_1080x1920.png') else 'capa_1080x1920.png'
            if os.path.exists(E + capa): Image.open(E + capa).convert('RGB').save(f'{D}{pid}_capa.jpg', quality=90)
            params = {'video_url': f'{U}{dd}/{pid}.mp4', 'share_to_feed': True, 'caption': leg}
            if os.path.exists(E + capa): params['cover_url'] = f'{U}{dd}/{pid}_capa.jpg'
            acao = 'create_video_post'; arq = v
        assert len(leg) <= 2200 and 'Comente' not in leg
        os.makedirs(f'{root}/publicacao/{data}', exist_ok=True)
        json.dump({'hora': hora, 'acao': acao, 'connector': 'instagram', 'account': '17841407424879500', 'perfil': '@augustosilva.p', 'data': data,
                   'status': 'aguardando aprovação no Nexus', 'params': params}, open(f'{root}/publicacao/{data}/{pid}.json', 'w'), ensure_ascii=False, indent=1)
        md.append(f'\n---\n\n## {data[8:]}/11 {hora[:2]}h · {pid} · {tit}\n**Arquivo:** `{pasta}/{arq}`\n\n**Legenda:**\n\n{leg}\n')
    open(f'{root}/entregas/2026-11-18_a_20_SEM_PRESENTE.md', 'w').write(''.join(md)); print(len(P), 'posts')

if __name__ == '__main__': main()
