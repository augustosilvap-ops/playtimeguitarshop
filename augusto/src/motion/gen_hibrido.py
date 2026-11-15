"""Reels HÍBRIDOS: mini-aula em motion + colagem como destaque (papel nas cenas claras, recortes, traços à mão, carimbos).
Uso: python3 gen_hibrido.py"""
g=open('gen_reels.py').read();H=g[g.index("HEAD='''")+8:g.index("'''",g.index("HEAD='''")+8)]
def T(a,b,c=None): return f"['{a}','{b}'"+(f",{c}" if c else "")+"]"
def tb(rows,top=560,**k): return f"table(lt,{{top:{top},t0:.3,step:.22"+''.join(f",{a}:{v}" for a,v in k.items())+f",rows:[{','.join(rows)}]}})"
def build(name,theme,kw,capcta,S):
    rows=[];t=0
    for d,ty,js,cap in S: rows.append(f"[{t:.2f},{t+d:.2f},'{ty}',lt=>{js},'{cap}']");t+=d
    rows.append(f"[{t:.2f},{t+2:.2f},'accent',lt=>cta(lt,'{kw}'),'{capcta}']");t+=2
    js=f"const THEME={theme};\nconst SC=[\n"+",\n".join(rows)+f"];\nlet DUR={t:.2f};const K=1.55;SC.forEach(s=>{{s[0]*=K;s[1]*=K}});DUR*=K;"
    open(f'reel_hib_{name}.html','w').write(H+js+'\nR(0);\n</script></body></html>\n');return round(t*1.55,2)
IMG='../img/'
th="{dark:'#0A1430',light:'#F4ECDD',accent:'#2F6BFF',anim:'left',trans:'zoom',deco:'grid',align:'left',paper:true}"
print('frete',build('frete',th,'FRETE','Comente FRETE e receba o checklist de frete.',[
(2.2,'dark',"W(lt,[[0,'FRETE',190],[.2,'GRÁTIS',190,BL2],[.45,'TEM DONO?',120]],330)+cclip(lt,.5,{x:560,y:900,w:440,h:520,img:'"+IMG+"ph_frete.jpg',rot:5,seed:2,from:[400,0]})+cstamp(lt,1.1,{x:80,y:1000,txt:'VOCÊ',size:110})","Frete grátis para o cliente não é grátis para você."),
(2.6,'light',"W(lt,[[0,'QUEM PAGA?',130,NV]],280)+"+tb([T('Frete do pedido','R$ 22,90'),T('Cliente paga','R$ 0,00'),T('Você paga','R$ 22,90','RD')],hiLast='true')+"+ccircle(lt,1.3,{cx:830,cy:842,rx:170,ry:62})+lbl('Pedido de exemplo',1000,'#6B6152')","No frete grátis, o valor do frete sai do seu bolso."),
(2.6,'accent',"W(lt,[[0,'POR QUE',140],[.15,'PESA TANTO?',110]],260)+typer(lt,{a:'22,90 ÷ 59,90 = 38%',size:84,top:640,speed:24,ink:'#fff'})+cclip(lt,.9,{x:600,y:880,w:380,h:440,img:'"+IMG+"ph_comissao.jpg',rot:-4,seed:5,from:[0,400]})+carrow(lt,1.4,{x1:420,y1:1120,x2:600,y2:1050,col:'#fff'})","Num produto de R$ 59,90, o frete é 38% do preço (exemplo)."),
(2.8,'dark',"W(lt,[[0,'PASSO 1',150],[.15,'PESE E MEÇA',100,BL2]],250)+"+tb([T('Peso real','balança'),T('Peso cúbico','C × L × A ÷ fator do canal'),T('O frete cobra','o MAIOR dos dois')],hiLast='true',w1="'38%'")+"+ccircle(lt,1.5,{cx:790,cy:800,rx:210,ry:58,col:YE})","Passo 1: o frete cobra o maior entre peso real e peso cúbico."),
(2.6,'light',"W(lt,[[0,'PASSO 2',150,NV],[.15,'CAIXA MENOR',100,BL]],250)+`<div class=\"ab\" style=\"left:110px;top:620px;width:440px;height:440px;background:#C8955A;border:6px solid #9A6A36;transform:rotate(-3deg);opacity:${cstep(lt,.3)}\"></div><div class=\"ab\" style=\"left:640px;top:780px;width:260px;height:260px;background:#C8955A;border:6px solid #9A6A36;transform:rotate(4deg);opacity:${cstep(lt,.6)}\"></div>`+cstamp(lt,.9,{x:120,y:740,txt:'R$ 32',size:80,rot:-8})+cstamp(lt,1.2,{x:640,y:860,txt:'R$ 19',size:70,rot:6,col:BL})+carrow(lt,1.0,{x1:520,y1:1120,x2:700,y2:1080,col:NV})+lbl('Valores ilustrativos',1150,'#6B6152')","Passo 2: a menor caixa que protege bem o produto paga menos frete."),
(2.8,'dark',"W(lt,[[0,'PASSO 3',150],[.15,'FRETE NO PREÇO',90,BL2]],250)+"+tb([T('Custo do produto','R$ 28,00'),T('+ Frete grátis','R$ 22,90'),T('Custo total','R$ 50,90'),T('÷ (1 − 27% − 15%)','÷ 0,58'),T('Preço','R$ 87,76')],hiLast='true',w1="'52%'"),"Passo 3: se o frete é grátis, ele entra no custo antes de precificar."),
(2.6,'light',"W(lt,[[0,'CONFERINDO',140,NV]],270)+"+tb([T('Preço','R$ 87,76'),T('Taxas: 27% do preço','− R$ 23,70'),T('Produto','− R$ 28,00'),T('Frete','− R$ 22,90'),T('Lucro','R$ 13,16 = 15% ✓','GR')],hiLast='true')+"+chl(lt,1.4,{x:580,y:1006,w:360,h:56})","Sobram R$ 13,16: os 15% de margem, mesmo pagando o frete."),
(2.4,'accent',"W(lt,[[0,'RESUMO',150]],250)+"+tb([T('1','Frete grátis tem dono: você'),T('2','O frete cobra o maior peso'),T('3','Use a menor caixa segura'),T('4','Frete grátis entra no custo')],w1="'10%'",al="'left'")+"+cstamp(lt,1.4,{x:620,y:1080,txt:'SALVE',col:'#fff',rot:-10,size:84})","Salve e revise o frete dos seus produtos hoje."),
]))
