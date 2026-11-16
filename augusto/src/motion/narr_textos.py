"""Narração DETALHADA por cena (16/11: "aumente a velocidade, mas deixe a explicação mais detalhada").
Uma entrada por cena + a do CTA no fim. Cada frase vira legenda na tela no momento em que é falada.
Contas conferidas: ver comentários."""
NARR = {
'garimpo_salve': [
 "Comprou 200 peças porque o produto parecia bombar? Vou te mostrar como validar antes, com um exemplo.",
 # 200 − 12 = 188 peças · 188 × R$ 28 = R$ 5.264
 "O erro comum: pedir 200 unidades ao fornecedor e vender só 12 em 30 dias. São 188 peças paradas e R$ 5.264 presos no estoque.",
 "Por que dá errado? Ver o produto em alta num vídeo ou num grupo não prova que alguém compra ele no seu canal, pelo seu preço.",
 "Passo 1, demanda. Digite o produto na busca do marketplace, como o cliente faz. Abra os 5 primeiros anúncios e confira se eles têm vendas e avaliações recentes.",
 "Passo 2, concorrência. Copie preço, nota e frete dos 10 primeiros anúncios, cole na IA e peça uma tabela. No exemplo: preços de R$ 49 a R$ 79, nota 4,3 e 7 de 10 com frete grátis.",
 "Passo 3, reclamações. Leia as avaliações de 1 a 3 estrelas dos concorrentes. Aqui, 18 pessoas dizem que chegou amassada e 11 que a tampa vaza. Se o seu fornecedor resolve isso, essa é a sua brecha.",
 # 59,90 × 27% = 16,17 · 59,90 − 28,00 − 16,17 = 15,73 · 15,73 ÷ 59,90 = 26%
 "Passo 4, margem. Pegue o preço médio do mercado, R$ 59,90. Tire o custo, R$ 28, e as taxas de 27%, R$ 16,17. Sobram R$ 15,73 por venda, 26% do preço.",
 "Passo 5, teste pequeno. Compre 20 peças, não 200, e dê 30 dias. Vendeu 15 ou mais? Aí sim, aumente o pedido.",
 "Resumindo: demanda, concorrência, reclamações, margem e teste pequeno. Os valores são de exemplo; use os números do seu produto.",
 "Salve este Reel e use o passo a passo antes da próxima compra.",
],
'desconto_salve': [
 "Vai dar 30% de desconto na Black Friday? Antes, faça a conta comigo, com um exemplo.",
 # 83,90 × 0,70 = 58,73 · 58,73 × 27% = 15,86 · 58,73 − 15,86 − 48,50 = −5,63
 "Produto de R$ 83,90. Com 30% off, cai para R$ 58,73. As taxas de 27% levam R$ 15,86 e o custo é R$ 48,50. Cada venda dá R$ 5,63 de prejuízo.",
 # sem desconto: 83,90 − 22,65 − 48,50 = 12,75 · desconto 83,90 − 58,73 = 25,17
 "Por quê? Sem desconto, sobravam só R$ 12,75 por venda. O desconto de 30% tira R$ 25,17. Ele é maior que o seu lucro inteiro.",
 # 48,50 ÷ 0,73 = 66,44
 "Passo 1, preço mínimo. Some os percentuais cobrados na venda: comissão, imposto e taxa de pagamento. Aqui, 27%. Divida o custo por 0,73. O preço mínimo é R$ 66,44.",
 "Passo 2, margem mínima. Decida quanto ainda precisa sobrar em cada venda da promoção. No exemplo, 5% do preço.",
 # 27% + 5% = 32% · 48,50 ÷ 0,68 = 71,32
 "Passo 3, preço da oferta. Some taxas e margem mínima: 27 mais 5 dá 32%. Divida o custo por 0,68. A oferta pode ir até R$ 71,32.",
 # 71,32 ÷ 83,90 = 0,85 · 1 − 0,85 = 15%
 "Passo 4, desconto máximo. Divida a oferta pelo preço atual: 71,32 dividido por 83,90 dá 0,85. Tire de 1. Seu desconto máximo é 15%.",
 # 71,32 × 27% = 19,26 · 71,32 − 19,26 − 48,50 = 3,56 · 3,56 ÷ 71,32 = 5%
 "Conferindo: com 15% off, o preço fica R$ 71,32. Taxas de R$ 19,26 e custo de R$ 48,50. Sobram R$ 3,56 por venda, os 5% que você definiu.",
 "Resumo: preço mínimo, margem mínima, preço da oferta e desconto máximo. Números de exemplo; faça com os seus.",
 "Salve e faça essa conta com cada produto antes de criar qualquer cupom.",
],
'anuncio_salve': [
 "Seu anúncio tem visita e não vende? Vamos achar o problema ponto por ponto.",
 "O erro comum é pagar por mais visitas, com anúncio pago, antes de arrumar o anúncio que não está convencendo.",
 # 1.000 × 0,5% = 5 · 2.000 × 0,5% = 10
 "Veja o exemplo: mil visitas com conversão de 0,5% dão 5 vendas. Dobrando as visitas, você paga o dobro para vender 10. O problema continua lá.",
 "Ponto 1, a foto. A primeira foto precisa mostrar o produto inteiro, com luz clara e fundo limpo. Texto por cima esconde o produto.",
 "Ponto 2, o título. Use as palavras que o cliente digita na busca, como garrafa térmica 1 litro inox. Barato e promoção ninguém pesquisa.",
 # 89,90 ÷ 74,90 = 1,20 → +20%
 "Ponto 3, o preço. Compare com a média dos 10 primeiros da busca. Se você está 20% mais caro, mostre o porquê: kit, garantia ou prazo menor.",
 "Ponto 4, o frete. Se 7 de cada 10 concorrentes dão frete grátis, avalie embutir o frete no preço para não perder a venda no último clique.",
 "Ponto 5, a descrição. Pegue as perguntas que mais chegam, como medida, compatibilidade e o que vem na caixa, e responda tudo na descrição.",
 # 1.000 × 1,5% = 15
 "Resultado no exemplo: as mesmas mil visitas, com conversão de 1,5%, viram 15 vendas. Três vezes mais, sem gastar mais com tráfego.",
 "Resumo: foto, título, preço, frete e descrição. Os números são de exemplo.",
 "Salve e revise hoje o anúncio que mais recebe visitas.",
],
}

NARR['planilha_salve'] = [
 "Você vende um produto por 100 reais. Quanto sobra de verdade? Vamos fazer a conta com um exemplo.",
 "Desses 100 reais, a maior parte vai para o produto, a comissão, o imposto e os anúncios. No exemplo, só R$ 17 viram lucro.",
 "O erro mais comum: somar 42% em cima do custo. R$ 48,50 mais 42% dá R$ 68,87. Parece certo, mas não é.",
 # 68,87 × 27% = 18,59 · 68,87 − 18,59 − 48,50 = 1,78 (2,6%)
 "Por quê? As taxas são cobradas sobre o preço, não sobre o custo. Com R$ 68,87, as taxas levam R$ 18,59 e sobra só R$ 1,78. Isso é 2,6%, não 15%.",
 # 40 + 2,50 + 6 = 48,50
 "Passo 1, custo por unidade. Some tudo o que você paga em reais por peça: produto R$ 40, embalagem R$ 2,50 e a tarifa fixa do canal, R$ 6. Total: R$ 48,50.",
 # 14 + 6 + 5 + 2 = 27
 "Passo 2, o que é cobrado em porcentagem sobre a venda. Comissão da categoria, 14%. Imposto, 6%, confirme com o contador. Anúncios, 5%. Reserva para devoluções, 2%. Total: 27%.",
 "Passo 3, a sua margem. Decida quanto quer que sobre de cada venda. No exemplo, 15%.",
 # 27 + 15 = 42 · 1 − 0,42 = 0,58 · 48,50 ÷ 0,58 = 83,62
 "Passo 4, a conta. Some 27 mais 15: 42%. Tire de 1: sobra 0,58. Divida o custo por 0,58. R$ 48,50 dividido por 0,58 dá R$ 83,62.",
 # 83,62 × 27% = 22,58 · 83,62 − 22,58 − 48,50 = 12,54 = 15%
 "Conferindo: com preço de R$ 83,62, as taxas levam R$ 22,58 e o custo é R$ 48,50. Sobram R$ 12,54, exatamente os 15% que você queria.",
 "Resumo: some o custo em reais, some os percentuais da venda, escolha a margem e divida o custo por 1 menos tudo isso. Números de exemplo.",
 "Salve e calcule hoje o preço do seu produto principal.",
]

NARR['titulo_salve'] = [
 "Seu título está espantando cliente? Vamos reescrever um, com um exemplo, passo a passo.",
 "O erro comum: encher o título de palavras que ninguém pesquisa, como garrafa barata, promoção, envio rápido.",
 "Por quê? A busca do marketplace compara o seu título com o que o cliente digita. Ninguém digita promoção ou barato para achar uma garrafa.",
 "Passo 1, pesquise. Digite o produto na busca e anote as sugestões que aparecem, como 1 litro, inox e 24 horas. Depois veja quais palavras se repetem nos títulos do topo.",
 "Passo 2, a fórmula: produto, marca ou modelo, característica principal e variação. No exemplo: garrafa térmica, Inox Pro, 1 litro, 24 horas gelada, preta.",
 "Passo 3, monte o título juntando tudo, sem repetir palavras e sem símbolos: Garrafa Térmica Inox Pro 1 Litro 24h Gelada Preta.",
 "Passo 4, use a IA. Peça 5 versões com as palavras que o cliente pesquisa e o limite de caracteres do seu canal. Escolha a mais clara, não a mais criativa.",
 # 0,8% → 2,4% = 3×
 "Passo 5, teste. Troque o título e compare a taxa de cliques depois de 7 dias. No exemplo, foi de 0,8% para 2,4%: três vezes mais cliques.",
 "Resumo: pesquise as palavras da busca, use a fórmula, respeite o limite do canal e teste. Números de exemplo.",
 "Salve e reescreva hoje o título do seu anúncio principal.",
]
NARR['rotina_salve'] = [
 "Os pedidos estão acumulando e você não sabe por onde começar? Vamos montar uma rotina que dá conta.",
 "O erro comum é enviar quando dá tempo. Um dia vira dois, e o prazo de envio estoura.",
 "Por quê isso pesa? Envio atrasado vira reclamação. Reclamação derruba a reputação. E reputação baixa significa menos exposição e menos vendas.",
 "Passo 1, horário fixo, sempre na mesma ordem. Às 9, separe os pedidos. Às 10, imprima as etiquetas. Às 11, embale e confira. Ao meio-dia, poste ou entregue para a coleta. Às 17, responda as mensagens.",
 "Passo 2, descubra o horário de corte da transportadora ou da agência, que fica no painel do seu canal. Poste sempre antes dele, para o pedido sair no mesmo dia.",
 "Passo 3, antes de fechar a caixa, confira 4 itens: produto certo, cor e tamanho, etiqueta do pedido certo e embalagem protegida. Isso evita troca e devolução.",
 "Passo 4, reserve um horário só para mensagens. Responda tudo de uma vez: onde está meu pedido, troca de cor, previsão de entrega.",
 "A meta, no exemplo, é 98% dos pedidos no prazo. Acompanhe a sua taxa de envio no prazo toda semana, no painel do canal.",
 "Resumo: horário fixo, postar antes do corte, conferir 4 itens e um horário para mensagens.",
 "Salve e monte sua rotina de envio a partir de amanhã.",
]
NARR['roas_salve'] = [
 "Gastou 500 reais em anúncio. Será que deu lucro? Vamos ver com um exemplo.",
 "O erro comum é olhar só as vendas. O anúncio vendeu R$ 900, e parece ótimo.",
 # 900 − 405 − 243 − 500 = −248
 "Agora a conta inteira: das vendas de R$ 900, saem R$ 405 de custo dos produtos, R$ 243 de taxas e R$ 500 do anúncio. O resultado é R$ 248 de prejuízo.",
 "Passo 1, calcule o ROAS: vendas geradas pelo anúncio divididas pelo valor gasto. Os dois números estão no painel de anúncios. Aqui, 900 dividido por 500 dá 1,8.",
 # 100 − 45 − 27 = 28
 "Passo 2, veja quanto sobra de cada venda antes de pagar o anúncio. Do preço, tire o custo do produto, 45%, e as taxas, 27%. Sobram 28%.",
 # 1 ÷ 0,28 = 3,57
 "Passo 3, o ROAS mínimo é 1 dividido por essa sobra. 1 dividido por 0,28 dá 3,6. Abaixo disso, o anúncio dá prejuízo.",
 "Passo 4, compare: 1,8 é menor que 3,6. Esse anúncio está dando prejuízo. Ajuste ou pause antes de colocar mais dinheiro.",
 "O que ajustar: um público mais específico, foto e título melhores no anúncio, ou anunciar um produto com margem maior.",
 "Resumo: ROAS é vendas dividido pelo gasto. Calcule a sobra antes do anúncio. O mínimo é 1 dividido pela sobra. Números de exemplo.",
 "Salve e confira o ROAS dos seus anúncios hoje.",
]
NARR['atende_salve'] = [
 "Cliente perguntando e ficando sem resposta? Vamos montar um atendimento rápido com IA, passo a passo.",
 "O erro comum é responder só quando sobra tempo, horas depois da pergunta.",
 "Por quê isso custa vendas? O cliente pergunta para várias lojas ao mesmo tempo, e quem responde primeiro costuma levar a venda.",
 "Passo 1, escreva a base da sua loja num documento: prazo de envio, frete, regras de troca, formas de pagamento e o tom de voz, simpático e direto.",
 "Passo 2, liste as perguntas que mais chegam, olhando as últimas mensagens, e escreva a resposta certa de cada uma. Tem pronta entrega? Qual o prazo? Aceita Pix?",
 "Passo 3, cole a base no prompt: você é atendente da minha loja, responda com simpatia, em até 3 linhas, usando só esta base. Se não souber, diga que vai confirmar.",
 "Passo 4, a IA escreve o rascunho, e você revisa antes de enviar. Nunca deixe a IA inventar prazo ou preço.",
 "Resultado no exemplo: o tempo de resposta caiu de 6 horas para 5 minutos.",
 "Resumo: escreva a base, liste as perguntas frequentes, use o prompt com a base e revise antes de enviar.",
 "Salve e monte a base de atendimento da sua loja hoje.",
]
