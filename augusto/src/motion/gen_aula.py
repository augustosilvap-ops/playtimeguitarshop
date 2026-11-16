"""Reels no formato MINI-AULA (aprovado 15/11): gancho → erro comum → por quê → passos com números → conferência/resultado → resumo → CTA.
Uso: python3 gen_aula.py  (gera reel_aula_<nome>.html; renderizar com render_motion.js)"""
import re,os
g=open('gen_reels.py').read();H=g[g.index("HEAD='''")+8:g.index("'''",g.index("HEAD='''")+8)]
TH={
'claro_pontos':"{dark:'#0A1430',light:'#EEF2FA',accent:'linear-gradient(160deg,#5B8CFF,#1C47C9)',anim:'mask',trans:'zoom',deco:'dots',align:'center'}",
'azul_aneis':"{dark:'radial-gradient(900px 1200px at 50% 30%,#13307A,#050A1C)',light:'#F5F7FB',accent:'#1C47C9',anim:'zoom',trans:'flash',deco:'rings',align:'right'}",
'navy_scan':"{dark:'#08090E',light:'#FFFFFF',accent:'#2F6BFF',anim:'flip',trans:'slide',deco:'scan',align:'left'}",
'branco_diag':"{dark:'#0A1430',light:'#FFFFFF',accent:'#2F6BFF',anim:'right',trans:'iris',deco:'diag',align:'right'}",
'preto_glow':"{dark:'#000000',light:'#EEF2FA',accent:'linear-gradient(160deg,#5B8CFF,#1C47C9)',anim:'mask',trans:'wipe',deco:'glow',align:'center'}",
'azul_grade':"{dark:'radial-gradient(900px 1200px at 50% 30%,#13307A,#050A1C)',light:'#F5F7FB',accent:'#1C47C9',anim:'zoom',trans:'flash',deco:'grid',align:'left'}",
'branco_pontos':"{dark:'#08090E',light:'#FFFFFF',accent:'#2F6BFF',anim:'flip',trans:'slide',deco:'dots',align:'center'}",
'preto_aneis':"{dark:'#000000',light:'#F1F3F8',accent:'radial-gradient(900px 900px at 30% 20%,#7FA3FF,#2F6BFF 50%,#1A3FB0)',anim:'left',trans:'zoom',deco:'rings',align:'left'}"}
def T(a,b,c=None): return f"['{a}','{b}'"+(f",{c}" if c else "")+"]"
def tb(rows,top=560,**k): 
    ex=''.join(f",{a}:{v}" for a,v in k.items())
    return f"table(lt,{{top:{top},t0:.3,step:.22{ex},rows:[{','.join(rows)}]}})"
def box(txt,top=640,size=46,ink=None): return f"typer(lt,{{a:'{txt}',size:{size},speed:44,top:{top},box:true}})"
def head(a,b,c=None,top=250): return f"W(lt,[[0,'{a}',150],[.15,'{b}',100{','+c if c else ''}]],{top})"
def resumo(items,dark=False): return "W(lt,[[0,'RESUMO',150]],250)+"+tb([T(str(i+1),x) for i,x in enumerate(items)],top=480,w1="'10%'",al="'left'")
ARGS={}
SAVE=None
def build(name,theme,kw,capcta,S):
    ARGS[name]=(theme,kw,capcta,S)
    rows=[];t=0
    for d,ty,js,cap in S: rows.append(f"[{t:.2f},{t+d:.2f},'{ty}',lt=>{js},'{cap}']");t+=d
    ctajs=f"ctaSave(lt,'{SAVE[0]}','{SAVE[1]}')" if SAVE else f"cta(lt,'{kw}')"
    rows.append(f"[{t:.2f},{t+2:.2f},'accent',lt=>{ctajs},'{capcta}']");t+=2
    js=f"const THEME={TH[theme]};\nconst SC=[\n"+",\n".join(rows)+f"];\nlet DUR={t:.2f};const K=1.55;SC.forEach(s=>{{s[0]*=K;s[1]*=K}});DUR*=K;"
    open(f'reel_aula_{name}.html','w').write(H+js+'\nR(0);\n</script></body></html>\n');return round(t*1.55,2)
OUT={}
OUT['garimpo']=build('garimpo','claro_pontos','GARIMPO','Comente GARIMPO e receba os 5 prompts prontos.',[
(2.0,'dark',"W(lt,[[0,'COMPROU',130],[.2,'200 PEÇAS',170],[.45,'NO ACHISMO?',130,BL2]],420)","Vamos validar um produto antes de comprar, com um exemplo."),
(2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+tb([T('Pedido ao fornecedor','200 un.'),T('Vendidas em 30 dias','12 un.'),T('Dinheiro parado','R$ 5.264','RD')],hiLast='true'),"Erro comum: comprar porque “parece que vende”."),
(2.4,'accent',"W(lt,[[0,'POR QUE',150],[.15,'DÁ ERRADO?',120]],260)+"+box('Você viu o produto em alta, mas não conferiu se alguém compra ele no seu canal.'),"Produto em alta não prova que ele vende no SEU canal."),
(2.6,'light',head('PASSO 1','DEMANDA','BL')+"+"+tb([T('Digite o produto na busca','veja as sugestões'),T('Abra os 5 primeiros','eles têm vendas?'),T('Avaliações','são recentes?')],w1="'48%'"),"Passo 1: pesquise no próprio marketplace, como o cliente faz."),
(2.8,'dark',head('PASSO 2','CONCORRÊNCIA','BL2')+"+"+tb([T('Faixa de preço','R$ 49 a R$ 79'),T('Nota média','4,3 ★'),T('Frete grátis','7 de 10'),T('Brecha','tampa que vaza')],hiLast='true'),"Passo 2: cole os 10 primeiros anúncios na IA e peça esta tabela."),
(2.6,'light',head('PASSO 3','RECLAMAÇÕES','BL')+"+notifs(lt,{items:['“Chegou amassada” · 18 vezes','“A tampa vaza” · 11 vezes','“Não mantém gelado” · 7 vezes'],icon:'×',ic:RD,top:560,step:.25,t0:.3,badge:false})","Passo 3: leia as notas de 1 a 3 estrelas. A queixa mais repetida é a sua chance."),
(2.8,'dark',head('PASSO 4','MARGEM','BL2')+"+"+tb([T('Preço médio do mercado','R$ 59,90'),T('Custo por unidade','− R$ 28,00'),T('Taxas: 27% do preço','− R$ 16,17'),T('Lucro por venda','R$ 15,73 (26%)')],hiLast='true'),"Passo 4: no preço médio do mercado, ainda sobra lucro depois das taxas?"),
(2.4,'accent',head('PASSO 5','TESTE PEQUENO')+"+"+tb([T('Lote de teste','20 un.'),T('Prazo','30 dias'),T('Vendeu 15 ou mais?','compre mais')],hiLast='true'),"Passo 5: teste com 20 peças antes de comprar 200."),
(2.6,'light',resumo(['Demanda: o topo da busca vende?','Concorrência: preço, nota e frete','Reclamações: qual a brecha?','Margem: sobra lucro?','Teste com lote pequeno'])+"+lbl('Valores do exemplo são hipotéticos',1330,'#7A7F8C')","Salve este Reel antes da próxima compra."),
])
OUT['desconto']=build('desconto','azul_aneis','DESCONTO','Comente DESCONTO e receba a calculadora.',[
(2.0,'dark',"W(lt,[[0,'VAI DAR',130],[.2,'30% OFF',200],[.45,'NA BLACK?',140,BL2]],400)","Vamos ver se o seu desconto dá lucro, com um exemplo."),
(2.6,'light',"W(lt,[[0,'COM 30% OFF',130]],260)+"+tb([T('Preço normal','R$ 83,90'),T('Com −30%','R$ 58,73'),T('Taxas: 27% do preço','− R$ 15,86'),T('Custo por unidade','− R$ 48,50'),T('Resultado','− R$ 5,63','RD')],hiLast='true'),"No exemplo, cada venda com 30% off dá R$ 5,63 de prejuízo."),
(2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('Sem desconto, sobravam R$ 12,75 por venda. Um desconto de 30% tira R$ 25,17. O desconto é maior que o lucro.'),"O desconto sai inteiro do lucro, e ele era maior que o lucro."),
(2.8,'dark',head('PASSO 1','PREÇO MÍNIMO','BL2')+"+"+tb([T('Custo por unidade','R$ 48,50'),T('Taxas sobre a venda','27%'),T('Conta','48,50 ÷ 0,73'),T('Preço mínimo','R$ 66,44')],hiLast='true'),"Passo 1: abaixo do preço mínimo, toda venda dá prejuízo."),
(2.2,'light',head('PASSO 2','MARGEM MÍNIMA','BL')+"+liquid(lt,{pct:5,top:560,t0:.3,dur:1,fill:BL})","Passo 2: decida quanto ainda precisa sobrar na promoção. No exemplo, 5%."),
(2.8,'dark',head('PASSO 3','PREÇO DA OFERTA','BL2')+"+"+tb([T('Taxas + margem mínima','27% + 5% = 32%'),T('O que sobra','1 − 0,32 = 0,68'),T('Conta','48,50 ÷ 0,68'),T('Preço da oferta','R$ 71,32')],hiLast='true',w1="'48%'"),"Passo 3: preço da oferta = custo ÷ (1 − taxas − margem mínima)."),
(2.4,'accent',head('PASSO 4','DESCONTO MÁXIMO')+"+(lt>.5?`<div class=\"t\" style=\"top:640px;font-size:320px;color:#fff;transform:scale(${eb((lt-.5)/.35)})\">15%</div>`:'')+lbl('1 − 71,32 ÷ 83,90 = 15%',1000,'rgba(255,255,255,.85)',eo((lt-.8)/.3))","Passo 4: compare com o preço atual. Esse é o seu desconto máximo."),
(2.6,'light',"W(lt,[[0,'CONFERINDO',150,BL]],260)+"+tb([T('Preço com −15%','R$ 71,32'),T('Taxas: 27% do preço','− R$ 19,26'),T('Custo','− R$ 48,50'),T('Lucro','R$ 3,56 = 5% ✓','GR')],hiLast='true'),"Com 15% off ainda sobram R$ 3,56 por venda (5%)."),
(2.6,'dark',resumo(['Calcule o preço mínimo','Defina a margem mínima','Calcule o preço da oferta','Desconto máximo = 1 − oferta ÷ preço'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#C9D6F5')","Salve antes de criar qualquer cupom."),
])
OUT['anuncio']=build('anuncio','navy_scan','ANUNCIO','Comente ANUNCIO e receba o checklist completo.',[
(2.0,'dark',"W(lt,[[0,'MUITA VISITA',130],[.2,'E NENHUMA',130],[.4,'VENDA?',220,BL2]],380)","Vamos achar o problema do anúncio, ponto por ponto."),
(2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+box('Colocar mais anúncio pago num anúncio que não convence.',top=620,size=56),"Erro comum: pagar por mais visitas antes de arrumar o anúncio."),
(2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+tb([T('Visitas','1.000'),T('Conversão','0,5%'),T('Vendas','5'),T('Dobrar as visitas','10 vendas, custo em dobro')],hiLast='true',w1="'45%'"),"Se o anúncio converte pouco, mais visitas só aumentam o gasto (exemplo)."),
(2.6,'dark',head('1.','FOTO','BL2')+"+slider(lt,{top:520,h:760,t0:.3,dur:1.1,L:{bg:'#3A3D47',k:'ANTES',big:'escura',sub:'com texto por cima',c:'#FF8A95'},Rt:{bg:'#FFFFFF',k:'DEPOIS',big:'clara',sub:'produto inteiro',c:BL},bigSize:150})","1. Primeira foto: produto inteiro, fundo limpo, sem texto por cima."),
(2.6,'light',head('2.','TÍTULO','BL')+"+typer(lt,{a:'Garrafa ',wrong:'barata promoção',right:'térmica 1L inox',size:84,top:640,t1:.8,speed:28})","2. Título com as palavras que o cliente digita na busca."),
(2.6,'dark',head('3.','PREÇO','BL2')+"+"+tb([T('Seu preço','R$ 89,90'),T('Média dos 10 primeiros','R$ 74,90'),T('Diferença','+20%','RD')],hiLast='true'),"3. Mais caro que a média? Mostre por quê: kit, garantia ou prazo."),
(2.6,'light',head('4.','FRETE','BL')+"+"+tb([T('Seu frete','calcular no checkout','RD'),T('Concorrentes','7 de 10 grátis'),T('O que fazer','avaliar frete embutido')],w1="'40%'"),"4. Se os concorrentes dão frete grátis, avalie embutir no preço."),
(2.6,'dark',head('5.','DESCRIÇÃO','BL2')+"+notifs(lt,{items:['Qual a medida?','Serve no meu modelo?','O que vem na caixa?'],icon:'?',ic:BL,top:560,step:.25,t0:.3,dark:true,badge:false})","5. Responda na descrição as perguntas que mais chegam."),
(2.4,'accent',"W(lt,[[0,'RESULTADO',140]],260)+"+tb([T('Mesmas visitas','1.000'),T('Conversão nova','1,5%'),T('Vendas','15')],hiLast='true'),"Com o anúncio arrumado, as mesmas visitas vendem mais (exemplo)."),
(2.4,'light',resumo(['Foto clara e inteira','Título com palavras da busca','Preço comparado','Frete competitivo','Descrição que responde'])+"+lbl('Valores do exemplo são hipotéticos',1330,'#7A7F8C')","Salve e revise hoje o anúncio com mais visitas."),
])
OUT['titulo']=build('titulo','branco_diag','TITULO','Comente TITULO e receba o prompt completo.',[
(2.0,'dark',"W(lt,[[0,'SEU TÍTULO',130],[.2,'ESPANTA',210],[.45,'CLIENTE?',210,BL2]],420)","Vamos reescrever um título, com um exemplo."),
(2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+typer(lt,{a:'Garrafa barata promoção envio rápido',size:70,top:620,speed:30})","Erro comum: encher o título de palavras que ninguém pesquisa."),
(2.6,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('A busca compara o título com o que o cliente digita. Promoção e barato não ajudam ninguém a te encontrar.'),"O anúncio aparece quando as palavras batem com a busca."),
(2.6,'dark',head('PASSO 1','PESQUISE','BL2')+"+"+tb([T('Digite o produto','garrafa térmica'),T('Sugestões da busca','1 litro · inox · 24h'),T('Títulos do topo','palavras repetidas')],w1="'45%'"),"Passo 1: anote as palavras das sugestões da busca."),
(2.8,'light',head('PASSO 2','A FÓRMULA','BL')+"+"+tb([T('Produto','Garrafa térmica'),T('Marca ou modelo','Inox Pro'),T('Característica','1 litro, 24h gelada'),T('Variação','preta')],w1="'45%'"),"Passo 2: produto + marca + característica + variação."),
(2.6,'dark',head('PASSO 3','MONTE','BL2')+"+typer(lt,{a:'Garrafa Térmica Inox Pro 1 Litro 24h Gelada Preta',size:64,top:640,speed:30,ink:'#fff'})","Passo 3: junte tudo, sem repetir palavras e sem símbolos."),
(2.6,'accent',"lbl('Passo 4 · prompt',540,'rgba(255,255,255,.85)',eo(lt/.2))+"+box('Escreva 5 títulos para minha garrafa térmica 1L inox, usando as palavras que o cliente pesquisa e o limite de caracteres do meu canal.',top=620,size=44),"Passo 4: peça 5 versões para a IA e escolha a mais clara."),
(2.4,'light',head('PASSO 5','TESTE 7 DIAS','BL')+"+slider(lt,{top:540,h:740,t0:.3,dur:1.1,L:{bg:'#FDECEC',k:'TÍTULO ANTIGO',big:'0,8%',sub:'de cliques',c:RD},Rt:{bg:'#EAF0FF',k:'TÍTULO NOVO',big:'2,4%',sub:'de cliques',c:BL},bigSize:200})","Passo 5: troque e compare os cliques depois de 7 dias (exemplo)."),
(2.4,'dark',resumo(['Pesquise as palavras da busca','Use a fórmula','Respeite o limite do canal','Teste e compare']),"Salve para usar no próximo anúncio."),
])
OUT['rotina']=build('rotina','preto_glow','ROTINA','Comente ROTINA e receba o checklist diário.',[
(2.0,'accent',"W(lt,[[0,'PEDIDOS',150],[.2,'ACUMULANDO?',130]],250)+notifs(lt,{items:['Novo pedido #1042','Novo pedido #1043','Novo pedido #1044','Novo pedido #1045'],top:660,step:.18,t0:.3})","Vamos montar uma rotina que dá conta dos pedidos."),
(2.2,'dark',"W(lt,[[0,'O ERRO',150]],300)+calendar(lt,{days:[16,17,18,19],rate:2.2,top:560,head:'PRAZO DE ENVIO',stampTxt:'ATRASO'})","Erro comum: enviar quando dá tempo. O prazo estoura."),
(2.4,'light',"W(lt,[[0,'POR QUE?',150]],260)+"+tb([T('Envio atrasado','vira reclamação'),T('Reclamação','derruba a reputação'),T('Reputação baixa','menos exposição')],w1="'45%'"),"Cada atraso pesa na reputação, e a reputação pesa nas vendas."),
(2.8,'dark',head('PASSO 1','HORÁRIO FIXO','BL2')+"+"+tb([T('09h','Separar os pedidos'),T('10h','Imprimir etiquetas'),T('11h','Embalar e conferir'),T('12h','Postar ou coleta'),T('17h','Responder mensagens')],w1="'20%'",al="'left'"),"Passo 1: horários fixos, sempre na mesma ordem."),
(2.4,'light',head('PASSO 2','HORÁRIO DE CORTE','BL')+"+route(lt,{t0:.3,dur:1.2})","Passo 2: descubra o horário de corte da transportadora e poste antes dele."),
(2.8,'dark',head('PASSO 3','CONFERÊNCIA','BL2')+"+"+tb([T('Produto certo','✓','GR'),T('Cor e tamanho','✓','GR'),T('Etiqueta do pedido certo','✓','GR'),T('Embalagem protegida','✓','GR')]),"Passo 3: confira 4 itens antes de fechar a caixa. Evita troca."),
(2.4,'accent',head('PASSO 4','MENSAGENS')+"+notifs(lt,{items:['Cadê meu pedido?','Pode trocar a cor?','Chegou hoje?'],icon:'?',ic:'#0A1430',top:560,step:.25,t0:.3,badge:false})","Passo 4: reserve um horário para responder todas as mensagens."),
(2.2,'light',"W(lt,[[0,'META',150]],260)+liquid(lt,{pct:98,top:520,t0:.2,dur:1.1,fill:BL})","Meta: quase todos os pedidos no prazo. Acompanhe toda semana (exemplo)."),
(2.4,'dark',resumo(['Horário fixo, mesma ordem','Postar antes do corte','Conferir 4 itens','Horário para mensagens']),"Salve e cole na parede do estoque."),
])
OUT['roas']=build('roas','azul_grade','ROAS','Comente ROAS e receba a calculadora.',[
(2.0,'light',"W(lt,[[0,'GASTOU',130],[.2,'EM ANÚNCIO',130,BL]],260)+coins(lt,{n:16,count:500,y:600,top:1480})","Vamos ver se o seu anúncio dá lucro, com um exemplo."),
(2.4,'dark',"W(lt,[[0,'O ERRO',150]],260)+"+box('O anúncio vendeu R$ 900. Está ótimo!',top=620,size=60),"Erro comum: achar que vender bem é o mesmo que dar lucro."),
(2.8,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+tb([T('Vendas geradas','R$ 900'),T('Custo dos produtos (45%)','− R$ 405'),T('Taxas (27%)','− R$ 243'),T('Anúncio','− R$ 500'),T('Resultado','− R$ 248','RD')],hiLast='true'),"Depois do custo, das taxas e do anúncio, o resultado foi negativo (exemplo)."),
(2.4,'dark',head('PASSO 1','O ROAS','BL2')+"+typer(lt,{a:'900 ÷ 500 = 1,8',size:120,top:640,speed:20,ink:'#fff'})","Passo 1: ROAS = vendas geradas ÷ valor gasto no anúncio."),
(2.6,'light',head('PASSO 2','SOBRA','BL')+"+"+tb([T('Preço','100%'),T('Custo do produto','− 45%'),T('Taxas','− 27%'),T('Sobra antes do anúncio','28%')],hiLast='true'),"Passo 2: veja quanto sobra de cada venda antes de pagar o anúncio."),
(2.6,'dark',head('PASSO 3','ROAS MÍNIMO','BL2')+"+"+tb([T('Sobra antes do anúncio','28%'),T('Conta','1 ÷ 0,28'),T('ROAS mínimo','3,6')],hiLast='true'),"Passo 3: ROAS mínimo = 1 ÷ sobra antes do anúncio."),
(2.4,'accent',"W(lt,[[0,'1,8 < 3,6',170]],260)+gauge(lt,{top:540,from:.05,to:.2,t0:.2,dur:.9,valTxt:q=>'PREJUÍZO'})","Passo 4: ROAS abaixo do mínimo = prejuízo. Ajuste ou pause."),
(2.6,'light',"W(lt,[[0,'O QUE AJUSTAR',120,BL]],260)+"+tb([T('Público','mais específico'),T('Anúncio','foto e título melhores'),T('Produto','escolha um com margem maior')],w1="'30%'"),"Ajuste público, anúncio ou produto antes de investir mais."),
(2.4,'dark',resumo(['ROAS = vendas ÷ gasto','Calcule a sobra antes do anúncio','ROAS mínimo = 1 ÷ sobra','Abaixo do mínimo: ajuste ou pause'])+"+lbl('Valores do exemplo são hipotéticos',1200,'#C9D6F5')","Salve e confira seus anúncios hoje."),
])
OUT['atende']=build('atende','branco_pontos','ATENDE','Comente ATENDE e receba os prompts de atendimento.',[
(2.0,'dark',"W(lt,[[0,'CLIENTE',120],[.15,'SEM RESPOSTA?',110,BL2]],260)+notifs(lt,{items:['Tem pronta entrega?','Qual o prazo?','Aceita Pix?','Tem outra cor?'],icon:'?',ic:RD,top:620,step:.2,t0:.35,dark:true})","Vamos montar um atendimento rápido com IA, passo a passo."),
(2.2,'light',"W(lt,[[0,'O ERRO',150]],260)+gauge(lt,{top:540,from:.9,to:.08,t0:.2,dur:1,labels:[['LENTO',RD],['OK',YE],['RÁPIDO',GR]]})","Erro comum: responder só quando sobra tempo, horas depois."),
(2.4,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('O cliente pergunta para várias lojas ao mesmo tempo. Quem responde primeiro costuma levar a venda.'),"Quem responde primeiro tem mais chance de vender."),
(2.8,'dark',head('PASSO 1','A BASE','BL2')+"+"+tb([T('Prazo de envio','sua política'),T('Frete','valores do canal'),T('Trocas','regras da loja'),T('Pagamento','formas aceitas'),T('Tom de voz','simpático e direto')],w1="'45%'"),"Passo 1: escreva sua base: prazo, frete, trocas, pagamento e tom."),
(2.6,'light',head('PASSO 2','PERGUNTAS','BL')+"+"+tb([T('Tem pronta entrega?','sim, envio em 24h'),T('Qual o prazo?','conforme o frete'),T('Aceita Pix?','sim')],w1="'48%'"),"Passo 2: liste as perguntas que mais chegam e a resposta certa de cada uma."),
(2.6,'accent',"lbl('Passo 3 · prompt',540,'rgba(255,255,255,.85)',eo(lt/.2))+"+box('Você é atendente da minha loja. Responda com simpatia, em até 3 linhas, usando só esta base. Se não souber, diga que vai confirmar.',top=620,size=44),"Passo 3: cole a base no prompt e peça respostas curtas."),
(2.4,'dark',"lbl('Passo 4 · revise antes de enviar',540,'#C9D6F5',eo(lt/.2))+"+box('Oi, Ana! Temos sim, com envio em até 24h. Posso separar o seu?',top=620,size=52),"Passo 4: a IA rascunha; você revisa e envia. Nunca invente prazo."),
(2.4,'light',"W(lt,[[0,'RESULTADO',140,BL]],260)+slider(lt,{top:500,h:780,t0:.3,dur:1.1,L:{bg:'#FDECEC',k:'ANTES',big:'6 h',sub:'para responder',c:RD},Rt:{bg:'#EAF0FF',k:'DEPOIS',big:'5 min',sub:'para responder',c:BL},bigSize:200})","Resultado: respostas em minutos, não em horas (exemplo)."),
(2.4,'dark',resumo(['Escreva a base da loja','Liste as perguntas frequentes','Use o prompt com a base','Revise antes de enviar']),"Salve e monte sua base hoje."),
])
OUT['fotos']=build('fotos','preto_aneis','FOTOS','Comente FOTOS e receba o checklist de fotos.',[
(2.0,'dark',"W(lt,[[0,'FOTO ESCURA',120],[.15,'VENDE MENOS.',120,BL2]],260)+magnifier(lt,{top:620,errors:[[330,770,.5],[720,900,.8],[460,1080,1.1]]})","Vamos melhorar a foto do produto só com o celular."),
(2.4,'light',"W(lt,[[0,'O ERRO',150]],260)+"+tb([T('Foto à noite, luz amarela','cor errada','RD'),T('Fundo da casa','distrai','RD'),T('Produto cortado','não mostra o todo','RD')],w1="'50%'"),"Erro comum: fotografar onde está, do jeito que dá."),
(2.4,'accent',"W(lt,[[0,'POR QUE?',150]],260)+"+box('Na busca, o cliente vê só a primeira foto, pequena. Se ela não for clara, ele passa direto.'),"A primeira foto decide se o cliente clica ou não."),
(2.4,'dark',head('PASSO 1','LUZ','BL2')+"+phone3d(lt,{top:470,after:'perto da janela, de dia, sem flash',afterCol:BL,ta:1})","Passo 1: luz natural de janela, de dia, sem flash."),
(2.4,'light',head('PASSO 2','FUNDO','BL')+"+slider(lt,{top:480,h:800,t0:.3,dur:1.1,L:{bg:'#3A3D47',k:'ANTES',big:'bagunçado',sub:'distrai',c:'#FF8A95'},Rt:{bg:'#FFFFFF',k:'DEPOIS',big:'liso',sub:'cartolina branca',c:BL},bigSize:130})","Passo 2: fundo liso. Uma cartolina branca atrás e embaixo resolve."),
(2.6,'dark',head('PASSO 3','4 FOTOS','BL2')+"+"+tb([T('Frente','produto inteiro'),T('Lateral','profundidade'),T('Detalhe','material e acabamento'),T('Em uso','tamanho real')],w1="'35%'"),"Passo 3: frente, lateral, detalhe e em uso."),
(2.2,'accent',head('PASSO 4','SEM FILTRO')+"+strike(lt,.5,'FILTRO.',720,210)","Passo 4: sem filtro. A cor tem que ser a que o cliente vai receber."),
(2.6,'light',head('PASSO 5','REGRAS DO CANAL','BL')+"+"+tb([T('Primeira foto','fundo branco'),T('Formato','quadrado (1:1)'),T('Produto','ocupa boa parte da foto')],w1="'40%'"),"Passo 5: confira as regras de foto do seu marketplace antes de subir."),
(2.4,'dark',resumo(['Luz de janela','Fundo liso','4 ângulos','Sem filtro','Regras do canal']),"Salve e refaça hoje a foto do seu produto principal."),
])
# Versões SEM recompensa (Manychat não configurado) — 16/11
for nm,sv,cap in [('desconto',('SALVE','PRA BLACK'),'Salve e faça essa conta antes de definir o desconto.'),
                  ('anuncio',('SALVE','E REVISE'),'Salve e revise seu anúncio com esse passo a passo.'),
                  ('garimpo',('SALVE','E TESTE'),'Salve e use esse passo a passo no próximo produto.')]:
    SAVE=sv; th,kw,_,S=ARGS[nm]; OUT[nm+'_salve']=build(nm+'_salve',th,kw,cap,S); SAVE=None
print(OUT)
