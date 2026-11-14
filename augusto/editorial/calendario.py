"""Calendário 16–22/11/2026 — fonte única. Gera CALENDARIO.md e Calendario_16-22nov.xlsx."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
C=[
# id, data, hora, formato, pilar, direção, tema/gancho, palavra, recompensa, mídia, status
("01","Seg 16/11","08h30","Estático","Precificação","A · Fotográfico","Você perde lucro nas taxas?","TAXAS","Raio-X das Taxas (PDF 2 p.)","Mixkit #242","Pronto p/ revisão"),
("02","Seg 16/11","12h30","Carrossel 8","Precificação","C · Glass Dashboard","5 custos que comem seu lucro","CUSTOS","Guia de Precificação para Leigos com IA (PDF 12 p.)","—","Pronto p/ revisão"),
("03","Seg 16/11","19h30","Reel 7s","Precificação","A · Filmagem real","Quer aprender a precificar mesmo sendo leigo? Leia a legenda.","PLANILHA","Planilha de Precificação (XLSX)","Mixkit #308","Pronto p/ revisão"),
("04","Ter 17/11","08h30","Carrossel 7","Precificação","B · Editorial clean","Faturamento não é lucro: entenda sua margem antes de vender","MARGEM","Mini-guia Faturamento × Lucro × Margem (PDF)","—","Capa p/ revisão"),
("05","Ter 17/11","12h30","Estático","Precificação","D · Conceitual","Margem não é markup","MARKUP","Tabela de conversão markup → margem (PDF 1 p.)","—","Capa p/ revisão"),
("06","Ter 17/11","19h30","Reel 7s","IA aplicada","B · Editorial clean (capa) + filmagem real","Quer usar IA para encontrar produtos com potencial? Leia a legenda.","GARIMPO","Pack de prompts de pesquisa de produto (PDF)","Mixkit #4938","Capa p/ revisão"),
("07","Qua 18/11","08h30","Carrossel 7","IA aplicada","D · Conceitual (claro)","Produto certo com IA: valide antes de comprar","VALIDAR","Checklist de validação de produto (PDF)","—","Capa p/ revisão"),
("08","Qua 18/11","12h30","Estático","Estratégia comercial","A · Fotográfico","3 sinais de um produto com potencial","SINAIS","Scorecard de produto (XLSX)","Mixkit #4705","Capa p/ revisão"),
("09","Qua 18/11","19h30","Reel 7s","Estratégia comercial","C · Glass Dashboard (capa) + filmagem real","Quer fazer Black Friday sem destruir sua margem? Leia a legenda.","DESCONTO","Calculadora de desconto máximo (XLSX)","Mixkit #42137","Capa p/ revisão"),
("10","Qui 19/11","08h30","Carrossel 8","Estratégia comercial","C · Glass Dashboard","Black Friday: oferta com margem protegida","BLACK","Planejador de ofertas da Black Friday (XLSX)","—","Planejado"),
("11","Qui 19/11","12h30","Estático","Precificação","D · Conceitual","Pare de precificar no escuro","ESCURO","Prompt de preço mínimo (PDF 1 p.)","—","Planejado"),
("12","Qui 19/11","19h30","Reel 7s","Marketplace e operação","A · Filmagem real","Quer saber se seu anúncio está perdendo vendas? Leia a legenda.","ANUNCIO","Checklist de anúncio (PDF)","Mixkit #1781","Planejado"),
("13","Sex 20/11","08h30","Carrossel 7","IA aplicada","C · Glass (interface de IA)","Como validar a demanda com IA sem inventar números","DEMANDA","Prompts de pesquisa de demanda (PDF)","—","Planejado"),
("14","Sex 20/11","12h30","Estático","Marketplace e operação","A · Fotográfico","Frete: o custo que você esquece","FRETE","Checklist de embalagem e frete (PDF)","Mixkit #42131","Planejado"),
("15","Sex 20/11","19h30","Reel 7s","IA aplicada","A · Filmagem real","Quer usar IA para escrever títulos de anúncio melhores? Leia a legenda.","TITULO","Prompt de títulos de anúncio (PDF)","Mixkit #4907","Planejado"),
("16","Sáb 21/11","08h30","Carrossel 8","Marketplace e operação","B · Editorial clean","7 erros de quem começa no marketplace","ERROS","Checklist dos 7 erros (PDF)","—","Planejado"),
("17","Sáb 21/11","12h30","Estático","Marketplace e operação","D · Conceitual","Devolução também é custo","DEVOLUCAO","Calculadora de reserva para devoluções (XLSX)","—","Planejado"),
("18","Sáb 21/11","19h30","Reel 7s","Marketplace e operação","A · Filmagem real","Quer organizar seus pedidos sem se perder? Leia a legenda.","ROTINA","Checklist diário da operação (PDF)","Mixkit #42135","Planejado"),
("19","Dom 22/11","08h30","Carrossel 8","Estratégia comercial","B · Editorial clean","Checklist antes da Black Friday (27/11)","PRONTO","Checklist pré-Black Friday (PDF)","—","Planejado"),
("20","Dom 22/11","12h30","Estático","Autoridade e educação","D · Conceitual","Quanto sobra de cada R$ 100 que você vende?","SOBRA","Calculadora \"quanto sobra\" (XLSX)","—","Planejado"),
("21","Dom 22/11","19h30","Reel 7s","IA aplicada","A · Filmagem real","Quer usar IA para responder clientes mais rápido? Leia a legenda.","ATENDE","Prompts de atendimento ao cliente (PDF)","Mixkit #4915","Planejado"),
]
kws=[c[7] for c in C]; assert len(set(kws))==len(kws), "palavra-chave duplicada"
for a in kws:
    for b in kws:
        assert a==b or a not in b, f"{a} contido em {b}"
H=["ID","Data","Hora*","Formato","Pilar","Direção visual","Tema / gancho","Palavra-chave","Recompensa no Direct","Mídia real","Status"]
md=["# Calendário editorial — 16 a 22/11/2026 · @augustosilva.p","",
"*Horários são hipótese (manhã/almoço/noite) e ainda **não foram validados** com as métricas da conta. Nenhuma publicação está agendada ou publicada.*",
"*Black Friday 2026 = sexta, 27/11. O conteúdo de 11.11 foi convertido para a Black Friday.*","",
"| "+" | ".join(H)+" |","|"+"---|"*len(H)]
for c in C: md.append("| "+" | ".join(c)+" |")
md+=["","## Palavras-chave Manychat","","Uma por publicação, todas diferentes e sem acento (configurar também as variações com acento e minúsculas). Nenhuma é parte de outra, para não disparar o fluxo errado.","",
"Não usar: `CHAT`, `IA`, `PROMO`, `PROMO11`, `PREÇO`, `LUCRO`, `OFERTA`, `PESQUISA`, `PRODUTO`, `VALIDAÇÃO` (genéricas ou de planos antigos).","",
"**Status de todas as automações: NÃO CONFIGURADO.** Nada dispara até a conta do Manychat estar conectada e cada fluxo ser testado (ver `post.md` de cada entrega)."]
open("editorial/CALENDARIO.md","w").write("\n".join(md)+"\n")
wb=Workbook();ws=wb.active;ws.title="Semana 16-22 nov"
ws.append(H)
for c in C: ws.append(list(c))
for cell in ws[1]: cell.font=Font(bold=True,color="FFFFFF",name="Arial");cell.fill=PatternFill("solid",fgColor="0A1638");cell.alignment=Alignment(wrap_text=True,vertical="center")
for row in ws.iter_rows(min_row=2):
    for cell in row: cell.font=Font(name="Arial",size=10);cell.alignment=Alignment(wrap_text=True,vertical="top");cell.border=Border(bottom=Side(style="thin",color="E7EBF2"))
    row[7].font=Font(name="Arial",size=10,bold=True,color="2F6BFF")
for i,w in enumerate([5,10,7,12,20,22,46,14,40,14,16]): ws.column_dimensions[chr(65+i)].width=w
ws.freeze_panes="A2"
wb.save("editorial/Calendario_16-22nov.xlsx");print("ok",len(C))
