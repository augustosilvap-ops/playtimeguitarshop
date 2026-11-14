"""Planejador de ofertas da Black Friday (recompensa BLACK). Uso: python3 planilha_black.py saida.xlsx"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
NAVY, ELEC, PAPER, INK, GRAY = "08090E", "2F6BFF", "F5F7FB", "0A0B10", "7A7F8C"; F = "Arial"; thin = Side(style="thin", color="E7EBF2")
wb = Workbook(); h = wb.active; h.title = "Como usar"; h.sheet_view.showGridLines = False
h["B2"] = "Planejador de ofertas da Black Friday"; h["B2"].font = Font(name=F, size=18, bold=True, color=NAVY)
h["B3"] = "@augustosilva.p  ·  descubra o desconto máximo de cada produto antes de anunciar"; h["B3"].font = Font(name=F, size=10, color=GRAY)
txt = [("1. Na aba Ofertas, liste só os produtos candidatos à promoção.", True), ("Preencha as colunas azuis-claras: custo por unidade (produto + embalagem + tarifa fixa + frete que você paga), % cobrados na venda, preço atual, margem mínima, desconto que pretende dar, estoque e meta de unidades.", False),
 ("2. Leia as colunas escuras.", True), ("Preço mínimo da oferta: o menor preço que ainda entrega a margem mínima.", False), ("Desconto máximo: o maior desconto possível sobre o preço atual.", False),
 ("Margem com o desconto planejado e o veredito: OK, abaixo da mínima ou prejuízo.", False), ("Lucro previsto: lucro por unidade × meta de unidades.", False),
 ("3. Considere kit, brinde ou frete em vez de desconto quando o veredito não for OK.", True),
 ("Conta usada: preço da oferta = custo ÷ (1 − % da venda − margem mínima).", True),
 ("Conteúdo educativo. Os exemplos são hipotéticos; taxas variam por canal, categoria e regime tributário.", False)]
for i, (t, b) in enumerate(txt):
    c = h.cell(row=5 + i, column=2, value=t); c.font = Font(name=F, size=11 if b else 10, bold=b, color=NAVY if b else INK); c.alignment = Alignment(wrap_text=True)
h.column_dimensions["A"].width = 3; h.column_dimensions["B"].width = 110
ws = wb.create_sheet("Ofertas"); ws.sheet_view.showGridLines = False
ws["B2"] = "Ofertas da Black Friday"; ws["B2"].font = Font(name=F, size=16, bold=True, color=NAVY)
heads = ["Produto", "Custo por unidade (R$)", "% cobrados na venda", "Preço atual (R$)", "Margem mínima", "Desconto planejado", "Estoque (un.)", "Meta (un.)",
         "Preço mínimo da oferta (R$)", "Desconto máximo", "Preço com desconto (R$)", "Margem com desconto", "Veredito", "Lucro por unidade (R$)", "Lucro previsto (R$)"]
HR = 4
for i, t in enumerate(heads):
    c = ws.cell(row=HR, column=2 + i, value=t); c.font = Font(name=F, size=9, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=NAVY if i >= 8 else ELEC); c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
ws.row_dimensions[HR].height = 44
ex = [("EXEMPLO HIPOTÉTICO · Produto A", 48.5, .27, 83.9, .05, .20, 120, 80), ("EXEMPLO HIPOTÉTICO · Produto B", 22, .25, 59.9, .08, .10, 300, 150), ("EXEMPLO HIPOTÉTICO · Produto C", 60, .30, 99.9, .05, .30, 40, 30)]
for r in range(HR + 1, HR + 41):
    v = ex[r - HR - 1] if r - HR - 1 < len(ex) else (None,) * 8
    for j, x in enumerate(v):
        c = ws.cell(row=r, column=2 + j, value=x); c.fill = PatternFill("solid", fgColor="FFFFFF" if j == 0 else "EEF3FF"); c.border = Border(bottom=thin); c.font = Font(name=F, size=10, color=INK)
        c.number_format = "@" if j == 0 else ('"R$" #,##0.00' if j in (1, 3) else ("0%" if j in (2, 4, 5) else "0"))
    b = f'$B{r}=""'
    f = {10: f'=IF({b},"",IF(D{r}+F{r}>=1,"Revise",C{r}/(1-D{r}-F{r})))', 11: f'=IF(OR({b},NOT(ISNUMBER(J{r}))),"",MAX(0,1-J{r}/E{r}))',
         12: f'=IF({b},"",E{r}*(1-G{r}))', 13: f'=IF(OR({b},L{r}=0),"",(L{r}*(1-D{r})-C{r})/L{r})',
         14: f'=IF(NOT(ISNUMBER(M{r})),"",IF(M{r}<0,"PREJUÍZO",IF(M{r}<F{r},"Abaixo da mínima","OK")))', 15: f'=IF({b},"",L{r}*(1-D{r})-C{r})', 16: f'=IF({b},"",O{r}*MIN(I{r},H{r}))'}
    fm = {10: '"R$" #,##0.00', 11: "0.0%", 12: '"R$" #,##0.00', 13: "0.0%", 14: "@", 15: '"R$" #,##0.00', 16: '"R$" #,##0.00'}
    for col, fo in f.items():
        c = ws.cell(row=r, column=col, value=fo); c.number_format = fm[col]; c.fill = PatternFill("solid", fgColor=PAPER); c.border = Border(bottom=thin); c.font = Font(name=F, size=10, bold=col in (11, 14), color=INK)
rng = f"N{HR+1}:N{HR+40}"
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'N{HR+1}="PREJUÍZO"'], font=Font(color="C62828", bold=True), fill=PatternFill("solid", fgColor="FDECEC")))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'N{HR+1}="Abaixo da mínima"'], font=Font(color="B26A00", bold=True)))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'N{HR+1}="OK"'], font=Font(color="1B7F3B", bold=True)))
for i, wdt in enumerate([3, 34] + [14] * 7 + [16, 13, 15, 14, 16, 15, 15]):
    ws.column_dimensions[chr(65 + i)].width = wdt
ws.freeze_panes = ws.cell(row=HR + 1, column=3)
wb.active = 0; wb.save(sys.argv[1]); print("ok", sys.argv[1])
