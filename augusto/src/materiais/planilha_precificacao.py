"""Gera a Planilha de Precificação (recompensa da palavra PLANILHA).
Uso: python3 planilha_precificacao.py <saida.xlsx>"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation

NAVY, ELEC, ICE, PAPER, INK, GRAY = "0A1638", "2F6BFF", "DDE7FF", "F3F5F9", "070A12", "7D879A"
F = "Arial"
thin = Side(style="thin", color="E7EBF2")

def title(ws, text, sub):
    ws["B2"] = text; ws["B2"].font = Font(name=F, size=18, bold=True, color=NAVY)
    ws["B3"] = sub;  ws["B3"].font = Font(name=F, size=10, color=GRAY)
    ws.sheet_view.showGridLines = False

wb = Workbook()

# ---------------- Precificação ----------------
ws = wb.active; ws.title = "Precificação"
title(ws, "Planilha de Precificação", "@augustosilva.p  ·  preencha só as colunas azuis-claras; as escuras calculam sozinhas")
heads = ["Produto", "Custo do produto (R$)", "Embalagem (R$)", "Tarifa fixa (R$)", "Frete pago por mim (R$)",
         "Comissão (%)", "Imposto (%)", "Taxa financeira (%)", "Anúncios (%)", "Devoluções (%)", "Margem desejada (%)",
         "Custo por unidade (R$)", "Soma dos % sobre a venda", "Preço sugerido (R$)", "Preço mínimo — lucro zero (R$)",
         "Lucro no preço sugerido (R$)", "Margem real", "Markup sobre o produto"]
HR = 5
for i, h in enumerate(heads):
    c = ws.cell(row=HR, column=2 + i, value=h)
    calc = i >= 11
    c.font = Font(name=F, size=9, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=NAVY if calc else ELEC)
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
ws.row_dimensions[HR].height = 46

ex = [("EXEMPLO HIPOTÉTICO · Produto A", 40, 2.5, 6, 0, .14, .06, 0, .05, .02, .15),
      ("EXEMPLO HIPOTÉTICO · Produto B", 18, 1.5, 6, 0, .12, .06, 0, .03, .02, .12),
      ("EXEMPLO HIPOTÉTICO · Produto C", 95, 4, 0, 12, .16, .06, 0, .06, .03, .15)]
FIRST, LAST = HR + 1, HR + 40
for r in range(FIRST, LAST + 1):
    vals = ex[r - FIRST] if r - FIRST < len(ex) else (None,) * 11
    for j, v in enumerate(vals):
        c = ws.cell(row=r, column=2 + j, value=v)
        c.fill = PatternFill("solid", fgColor="FFFFFF" if j == 0 else "EEF3FF")
        c.number_format = "0.0%" if j >= 5 else ('"R$" #,##0.00' if j >= 1 else "@")
        c.font = Font(name=F, size=10, color=INK)
        c.border = Border(bottom=thin)
    # B..L = 2..12 ; cálculos em M..S (13..19)
    blank = f'$B{r}=""'
    f = {
        13: f'=IF({blank},"",C{r}+D{r}+E{r}+F{r})',
        14: f'=IF({blank},"",G{r}+H{r}+I{r}+J{r}+K{r})',
        15: f'=IF({blank},"",IF(N{r}+L{r}>=1,"Revise os percentuais",M{r}/(1-N{r}-L{r})))',
        16: f'=IF({blank},"",IF(N{r}>=1,"Revise os percentuais",M{r}/(1-N{r})))',
        17: f'=IF(OR({blank},NOT(ISNUMBER(O{r}))),"",O{r}-M{r}-O{r}*N{r})',
        18: f'=IF(OR({blank},NOT(ISNUMBER(O{r}))),"",Q{r}/O{r})',
        19: f'=IF(OR({blank},NOT(ISNUMBER(O{r})),C{r}=0),"",(O{r}-C{r})/C{r})',
    }
    fmt = {13: '"R$" #,##0.00', 14: "0.0%", 15: '"R$" #,##0.00', 16: '"R$" #,##0.00', 17: '"R$" #,##0.00', 18: "0.0%", 19: "0.0%"}
    for col, formula in f.items():
        c = ws.cell(row=r, column=col, value=formula)
        c.number_format = fmt[col]; c.font = Font(name=F, size=10, bold=col in (15, 18), color=INK)
        c.fill = PatternFill("solid", fgColor=PAPER); c.border = Border(bottom=thin)
ws.conditional_formatting.add(f"R{FIRST}:R{LAST}",
    FormulaRule(formula=[f'AND(ISNUMBER(R{FIRST}),R{FIRST}<0.05)'], font=Font(color="C62828", bold=True), fill=PatternFill("solid", fgColor="FDECEC")))
dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="0.99", allow_blank=True,
                    error="Digite um percentual entre 0% e 99%.", errorTitle="Percentual inválido")
ws.add_data_validation(dv); dv.add(f"G{FIRST}:L{LAST}")
widths = [3, 34] + [14] * 10 + [15, 14, 15, 17, 16, 12, 13]
for i, w in enumerate(widths):
    ws.column_dimensions[chr(65 + i)].width = w
ws.freeze_panes = ws.cell(row=FIRST, column=3)

# ---------------- Simulador de desconto ----------------
d = wb.create_sheet("Simulador de desconto")
title(d, "Simulador de desconto", "Descubra até onde dá para baixar o preço sem passar da margem mínima")
rows = [("Custo por unidade (R$)", 48.5, '"R$" #,##0.00', True),
        ("Soma dos % sobre a venda (sem margem)", .27, "0.0%", True),
        ("Preço atual (R$)", 83.9, '"R$" #,##0.00', True),
        ("Menor margem que aceito na promoção", .05, "0.0%", True),
        ("Preço mínimo — lucro zero (R$)", "=IF(C6>=1,\"Revise\",C5/(1-C6))", '"R$" #,##0.00', False),
        ("Preço da oferta com margem protegida (R$)", "=IF(C6+C8>=1,\"Revise\",C5/(1-C6-C8))", '"R$" #,##0.00', False),
        ("Desconto máximo sobre o preço atual", "=IF(ISNUMBER(C10),MAX(0,1-C10/C7),\"\")", "0.0%", False),
        ("Desconto que estou pensando em dar", .20, "0.0%", True),
        ("Margem resultante com esse desconto", "=IF(C7*(1-C12)=0,\"\",(C7*(1-C12)*(1-C6)-C5)/(C7*(1-C12)))", "0.0%", False),
        ("Veredito", "=IF(NOT(ISNUMBER(C13)),\"\",IF(C13<0,\"PREJUÍZO: não faça\",IF(C13<C8,\"Abaixo da margem mínima\",\"Dentro do limite\")))", "@", False)]
for i, (lab, val, fmt, inp) in enumerate(rows):
    r = 5 + i
    d.cell(row=r, column=2, value=lab).font = Font(name=F, size=10, color=INK)
    c = d.cell(row=r, column=3, value=val); c.number_format = fmt
    c.font = Font(name=F, size=11, bold=not inp, color=INK)
    c.fill = PatternFill("solid", fgColor="EEF3FF" if inp else PAPER)
    for col in (2, 3): d.cell(row=r, column=col).border = Border(bottom=thin)
d["B16"] = "Valores iniciais = exemplo hipotético do guia. Troque pelos seus."
d["B16"].font = Font(name=F, size=9, italic=True, color=GRAY)
d.column_dimensions["A"].width = 3; d.column_dimensions["B"].width = 46; d.column_dimensions["C"].width = 22
d.conditional_formatting.add("C14", FormulaRule(formula=['LEFT(C14,4)="PREJ"'], font=Font(color="C62828", bold=True)))
d.conditional_formatting.add("C14", FormulaRule(formula=['LEFT(C14,5)="Abaix"'], font=Font(color="B26A00", bold=True)))
d.conditional_formatting.add("C14", FormulaRule(formula=['LEFT(C14,5)="Dentr"'], font=Font(color="1B7F3B", bold=True)))

# ---------------- Como usar ----------------
h = wb.create_sheet("Como usar", 0)
title(h, "Como usar esta planilha", "@augustosilva.p  ·  Planilha de Precificação para leigos")
txt = [
 ("1. Abra a aba Precificação.", True),
 ("Apague as 3 linhas de EXEMPLO HIPOTÉTICO ou escreva por cima.", False),
 ("2. Preencha as colunas azuis-claras de cada produto.", True),
 ("Custo do produto, embalagem e tarifa fixa em reais. Comissão, imposto, taxa, anúncios e devoluções em %.", False),
 ("Use a tabela oficial do seu marketplace e a alíquota do seu contador. Não chute.", False),
 ("3. Escolha a margem desejada.", True),
 ("É quanto você quer que sobre de cada venda, em % do preço.", False),
 ("4. Leia as colunas escuras.", True),
 ("Preço sugerido: o preço que entrega a margem escolhida.", False),
 ("Preço mínimo: abaixo dele, cada venda dá prejuízo.", False),
 ("Margem real: fica vermelha quando passa abaixo de 5%.", False),
 ("Markup: quanto o preço está acima do custo do produto (não confunda com margem).", False),
 ("5. Antes de uma promoção, use a aba Simulador de desconto.", True),
 ("A conta usada: Preço = custo por unidade ÷ (1 − soma dos % − margem).", True),
 ("Confira: no Produto A, o preço sugerido deve dar R$ 83,62 e o preço mínimo R$ 66,44.", False),
 ("Conteúdo educativo. Os exemplos são hipotéticos; taxas e impostos variam por canal, categoria e regime tributário.", False),
]
for i, (t, b) in enumerate(txt):
    c = h.cell(row=5 + i, column=2, value=t); c.font = Font(name=F, size=11 if b else 10, bold=b, color=NAVY if b else INK)
h.column_dimensions["A"].width = 3; h.column_dimensions["B"].width = 110

# ---------------- Prompt ----------------
p = wb.create_sheet("Prompt para IA")
title(p, "Prompt para adaptar esta planilha com IA", "Cole no ChatGPT, Claude ou Gemini junto com esta planilha")
prompt = ("Anexei minha planilha de precificação. Revise as fórmulas das colunas M a S da aba Precificação e "
          "explique cada uma em linguagem simples. Depois, me ajude a preencher os percentuais do meu canal: "
          "vou colar a tabela oficial de tarifas. Use apenas os números que eu fornecer e escreva 'não informado' "
          "quando faltar algum dado. Por fim, sugira em quais produtos a margem real ficou abaixo de 10% e o que posso revisar "
          "(custo, canal, embalagem ou preço).")
c = p["B5"]; c.value = prompt; c.alignment = Alignment(wrap_text=True, vertical="top"); c.font = Font(name="Consolas", size=10, color=INK)
c.fill = PatternFill("solid", fgColor=ICE); p.row_dimensions[5].height = 120; p.column_dimensions["A"].width = 3; p.column_dimensions["B"].width = 100

wb.active = 0
wb.save(sys.argv[1]); print("ok", sys.argv[1])
