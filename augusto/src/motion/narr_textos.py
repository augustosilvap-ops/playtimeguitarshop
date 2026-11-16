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
