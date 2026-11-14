"""Scorecard de produto (SINAIS) e Calculadora de desconto (DESCONTO)."""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import FormulaRule
F="Arial";INK="0A0B10";BLK="08090E";BLU="2F6BFF";IN="E8EFFF";PA="F5F7FB";G="7A7F8C";thin=Side(style="thin",color="E6EAF3")
def head(ws,t,s):
    ws.sheet_view.showGridLines=False;ws["B2"]=t;ws["B2"].font=Font(name=F,size=18,bold=True,color=INK);ws["B3"]=s;ws["B3"].font=Font(name=F,size=10,color=G)
def cell(c,v,fmt=None,inp=False,bold=False):
    c.value=v;c.font=Font(name=F,size=10,bold=bold,color=INK);c.fill=PatternFill("solid",fgColor=IN if inp else PA);c.border=Border(bottom=thin)
    if fmt:c.number_format=fmt
# --- SINAIS
wb=Workbook();ws=wb.active;ws.title="Scorecard"
head(ws,"Scorecard de produto · 3 sinais","@augustosilva.p · dê nota de 0 a 10 em cada sinal, com base nos dados que você coletou")
H=["Produto","Demanda (0–10)","Concorrência com brecha (0–10)","Margem (0–10)","Nota final","Decisão"]
for i,h in enumerate(H):
    c=ws.cell(row=5,column=2+i,value=h);c.font=Font(name=F,size=9,bold=True,color="FFFFFF");c.fill=PatternFill("solid",fgColor=BLU if i<4 else BLK);c.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center")
ws.row_dimensions[5].height=40
ex=[("EXEMPLO HIPOTÉTICO · Garrafa térmica 1L",8,6,7),("EXEMPLO HIPOTÉTICO · Capa de celular",9,3,4)]
for r in range(6,36):
    v=ex[r-6] if r-6<len(ex) else (None,None,None,None)
    for j,x in enumerate(v): cell(ws.cell(row=r,column=2+j),x,"0" if j else "@",True)
    cell(ws.cell(row=r,column=6),f'=IF(B{r}="","",ROUND((C{r}+D{r}+E{r})/3,1))',"0.0",bold=True)
    cell(ws.cell(row=r,column=7),f'=IF(B{r}="","",IF(MIN(C{r},D{r},E{r})<5,"Não comprar: sinal fraco",IF(F{r}>=7,"Testar com lote pequeno","Pesquisar mais")))',bold=True)
ws.conditional_formatting.add("G6:G35",FormulaRule(formula=['LEFT(G6,3)="Não"'],font=Font(color="C62828",bold=True)))
ws.conditional_formatting.add("G6:G35",FormulaRule(formula=['LEFT(G6,3)="Tes"'],font=Font(color="1B7F3B",bold=True)))
for col,w in zip("ABCDEFG",[3,38,16,22,14,12,26]): ws.column_dimensions[col].width=w
g=wb.create_sheet("Como dar nota",0);head(g,"Como dar nota","Notas baseadas em evidências que você coletou, nunca em achismo")
for i,t in enumerate(["Demanda: 0 = nenhum concorrente com vendas · 5 = poucos com vendas · 10 = vários anúncios com vendas e avaliações recentes",
 "Concorrência com brecha: 0 = mercado saturado e bem atendido · 5 = algumas reclamações · 10 = reclamações claras que você consegue resolver",
 "Margem: 0 = prejuízo no preço do mercado · 5 = margem baixa · 10 = margem confortável depois de todas as taxas",
 "Regra: qualquer sinal abaixo de 5 = não comprar. Média 7 ou mais = testar com lote pequeno."]):
    c=g.cell(row=5+i,column=2,value=t);c.font=Font(name=F,size=11,color=INK);c.alignment=Alignment(wrap_text=True)
g.column_dimensions["B"].width=110
wb.save(sys.argv[1])
# --- DESCONTO
wb=Workbook();d=wb.active;d.title="Desconto máximo"
head(d,"Calculadora de desconto máximo","@augustosilva.p · Black Friday sem destruir a margem · troque os valores azuis pelos seus")
rows=[("Custo por unidade (produto + embalagem + tarifa fixa)",48.5,'"R$" #,##0.00',True),("Soma dos % sobre a venda (comissão, imposto, anúncios, devoluções)",.27,"0.0%",True),
 ("Preço atual",83.9,'"R$" #,##0.00',True),("Menor margem que aceito na promoção",.05,"0.0%",True),
 ("Preço mínimo (lucro zero)",'=IF(C6>=1,"Revise",C5/(1-C6))','"R$" #,##0.00',False),("Preço da oferta com margem protegida",'=IF(C6+C8>=1,"Revise",C5/(1-C6-C8))','"R$" #,##0.00',False),
 ("DESCONTO MÁXIMO",'=IF(ISNUMBER(C10),MAX(0,1-C10/C7),"")',"0.0%",False),("Desconto que estou pensando em dar",.2,"0.0%",True),
 ("Margem com esse desconto",'=IF(C7*(1-C12)=0,"",(C7*(1-C12)*(1-C6)-C5)/(C7*(1-C12)))',"0.0%",False),
 ("Veredito",'=IF(NOT(ISNUMBER(C13)),"",IF(C13<0,"PREJUÍZO: não faça",IF(C13<C8,"Abaixo da margem mínima","Dentro do limite")))',"@",False)]
for i,(l,v,f,inp) in enumerate(rows):
    r=5+i;d.cell(row=r,column=2,value=l).font=Font(name=F,size=10,bold=l.isupper(),color=INK);cell(d.cell(row=r,column=3),v,f,inp,bold=not inp)
d["B16"]="Valores iniciais = exemplo hipotético. Comissões e impostos: use os valores oficiais do seu canal e do seu contador.";d["B16"].font=Font(name=F,size=9,italic=True,color=G)
d.conditional_formatting.add("C14",FormulaRule(formula=['LEFT(C14,4)="PREJ"'],font=Font(color="C62828",bold=True)))
d.conditional_formatting.add("C14",FormulaRule(formula=['LEFT(C14,5)="Dentr"'],font=Font(color="1B7F3B",bold=True)))
d.column_dimensions["A"].width=3;d.column_dimensions["B"].width=62;d.column_dimensions["C"].width=20
wb.save(sys.argv[2]);print("ok")
