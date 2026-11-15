"""Gera os Reels da semana a partir de lib.js (estilos aprovados). Uso: python3 gen_reels.py"""
HEAD='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
@font-face{font-family:I;font-weight:500;src:url('../fonts/InterPDF-500.ttf')}@font-face{font-family:I;font-weight:600;src:url('../fonts/InterPDF-600.ttf')}
@font-face{font-family:I;font-weight:700;src:url('../fonts/InterPDF-700.ttf')}@font-face{font-family:I;font-weight:800;src:url('../fonts/InterPDF-800.ttf')}
@font-face{font-family:M;font-weight:500;src:url('../fonts/JetBrainsMono-500.ttf')}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:I,sans-serif}
#v{position:absolute;inset:0;overflow:hidden}.ab{position:absolute}.t{position:absolute;left:0;right:0;text-align:center;font-weight:800;letter-spacing:-.05em;line-height:.95}
.w{position:absolute;white-space:nowrap;font-weight:800;letter-spacing:-.06em;line-height:.92}
.chip{position:absolute;left:84px;top:150px;display:flex;align-items:center;gap:16px;font:700 30px I}.chip i{width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:28px}
.cap{position:absolute;left:84px;right:84px;bottom:250px;text-align:center;font:700 40px I}.bar{position:absolute;left:84px;bottom:110px;height:6px;border-radius:6px}
</style></head><body><div id="v"></div><script src="lib.js"></script><script>
'''
REELS={
'titulo':('''const THEME={dark:'#0A1430',light:'#FFFFFF',accent:'#2F6BFF',anim:'right',trans:'iris',deco:'diag',align:'right'};
const SC=[
[0,1.8,'dark',lt=>W(lt,[[0,'SEU TÍTULO',130],[.2,'ESPANTA',210],[.45,'CLIENTE?',210,BL2]],520),'seu título espanta o cliente?'],
[1.8,3.9,'light',lt=>lbl('Título do anúncio · exemplo',600,'#7A7F8C',eo(lt/.2))+typer(lt,{a:'Produto ',wrong:'barato promoção',right:'térmico 1L inox',size:96,top:700,t1:.9,speed:28}),'título genérico some na busca.'],
[3.9,5.6,'accent',lt=>notifs(lt,{items:['Visita no anúncio','Visita no anúncio','Visita no anúncio','Visita no anúncio','Visita no anúncio'],icon:'↗',ic:'#0A1430',top:560,step:.2}),'muita visita, pouco clique.'],
[5.6,7.3,'dark',lt=>W(lt,[[0,'RELEVÂNCIA',120]],380)+gauge(lt,{top:620,from:.12,to:.9,t0:.2,dur:1.2,labels:[['BAIXA',RD],['MÉDIA',YE],['ALTA',GR]]}),'o título certo aumenta a relevância.'],
[7.3,9.0,'light',lt=>W(lt,[[0,'CLIQUES',120]],330)+slider(lt,{top:560,h:760,t0:.3,dur:1.1,L:{bg:'#FDECEC',k:'TÍTULO GENÉRICO · EXEMPLO',big:'0,8%',sub:'de cliques',c:RD},Rt:{bg:'#EAF0FF',k:'TÍTULO COM IA · EXEMPLO',big:'2,4%',sub:'de cliques',c:BL},bigSize:200}),'antes e depois do título (exemplo).'],
[9.0,10.9,'accent',lt=>cta(lt,'TITULO'),'e receba o prompt de títulos no Direct.']];
const DUR=10.9;'''.replace('const DUR=10.9;','let DUR=10.9;const K=1.7;SC.forEach(s=>{s[0]*=K;s[1]*=K});DUR*=K;'),'2026-11-18/15_reel_titulo'),
'rotina':('''const THEME={dark:'#000000',light:'#EEF2FA',accent:'linear-gradient(160deg,#5B8CFF,#1C47C9)',anim:'mask',trans:'wipe',deco:'glow',align:'center'};
const SC=[
[0,1.8,'accent',lt=>W(lt,[[0,'PEDIDOS',150],[.2,'ACUMULANDO?',130]],250)+notifs(lt,{items:['Novo pedido #1042','Novo pedido #1043','Novo pedido #1044','Novo pedido #1045','Novo pedido #1046'],top:640,step:.18,t0:.3}),'pedidos acumulando?'],
[1.8,3.8,'dark',lt=>W(lt,[[0,'O PRAZO',140]],330)+calendar(lt,{days:[16,17,18,19],rate:2.4,top:600,head:'PRAZO DE ENVIO',stampTxt:'ATRASO'}),'atraso vira reclamação.'],
[3.8,5.6,'light',lt=>W(lt,[[0,'ROTINA',150],[.2,'DIÁRIA.',150,BL]],300)+route(lt,{t0:.2,dur:1.3,after:'postar até 12h todo dia',afterCol:BL}),'uma rotina simples resolve.'],
[5.6,7.3,'dark',lt=>W(lt,[[0,'NO PRAZO',140]],330)+liquid(lt,{pct:98,top:600,t0:.15,dur:1.3})+lbl('Pedidos no prazo · exemplo',1360,'#8C92A3'),'pedidos saindo no prazo.'],
[7.3,9.0,'light',lt=>W(lt,[[0,'REPUTAÇÃO',130],[.2,'SUBINDO ↑',130,BL]],280)+bars(lt,{label:'Reputação · exemplo',t0:.15}),'reputação sobe junto.'],
[9.0,10.9,'accent',lt=>cta(lt,'ROTINA'),'e receba o checklist diário no Direct.']];
const DUR=10.9;'''.replace('const DUR=10.9;','let DUR=10.9;const K=1.7;SC.forEach(s=>{s[0]*=K;s[1]*=K});DUR*=K;'),'2026-11-19/18_reel_rotina'),
'roas':('''const THEME={dark:'radial-gradient(900px 1200px at 50% 30%,#13307A,#050A1C)',light:'#F5F7FB',accent:'#1C47C9',anim:'zoom',trans:'flash',deco:'grid',align:'left'};
const SC=[
[0,1.9,'light',lt=>W(lt,[[0,'GASTOU',130],[.2,'EM ANÚNCIO',130,BL]],260)+coins(lt,{n:18,count:500,y:600,top:1480}),'gastou em anúncio...'],
[1.9,3.8,'dark',lt=>W(lt,[[0,'PRA ONDE',120],[.15,'FOI?',120,BL2]],260)+donut(lt,{slices:[[45,'#fff'],[20,'#C9D6F5'],[15,'#9DBBFF'],[20,RD]],hi:3,top:640,center:'20%',centerCol:RD,sub:'foi para anúncios · exemplo'}),'...e não sabe se voltou?'],
[3.8,5.5,'accent',lt=>W(lt,[[0,'SEU ROAS',130]],330)+gauge(lt,{top:600,from:.05,to:.3,t0:.2,dur:1.1,valTxt:q=>'ROAS '+(1+q*3).toFixed(1).replace('.',',')}),'ROAS baixo = prejuízo.'],
[5.5,7.4,'light',lt=>lbl('A conta',640,'#7A7F8C',eo(lt/.2))+typer(lt,{a:'ROAS mínimo = ',wrong:'chute',right:'1 ÷ margem',size:100,top:720,t1:.75,speed:26}),'use a conta, não o chute.'],
[7.4,9.0,'dark',lt=>W(lt,[[0,'ANÚNCIO',140],[.15,'COM LUCRO.',140,BL2]],280)+bars(lt,{label:'Lucro com anúncio · exemplo',hi:GR,lo:'rgba(255,255,255,.18)',t0:.1}),'anúncio que paga a conta.'],
[9.0,10.9,'accent',lt=>cta(lt,'ROAS'),'e receba a calculadora de ROAS no Direct.']];
const DUR=10.9;'''.replace('const DUR=10.9;','let DUR=10.9;const K=1.7;SC.forEach(s=>{s[0]*=K;s[1]*=K});DUR*=K;'),'2026-11-19/23_reel_roas'),
'atende':('''const THEME={dark:'#08090E',light:'#FFFFFF',accent:'#2F6BFF',anim:'flip',trans:'slide',deco:'dots',align:'center'};
const SC=[
[0,1.9,'dark',lt=>W(lt,[[0,'CLIENTE',120],[.15,'SEM RESPOSTA?',110,BL2]],260)+notifs(lt,{items:['Tem pronta entrega?','Qual o prazo?','Aceita Pix?','Tem outra cor?','Cadê meu pedido?'],icon:'?',ic:RD,top:600,step:.22,t0:.35,dark:true}),'cliente sem resposta?'],
[1.9,3.7,'light',lt=>W(lt,[[0,'TEMPO DE',110],[.15,'RESPOSTA',110,BL]],280)+gauge(lt,{top:600,from:.08,to:.92,t0:.25,dur:1.2,labels:[['LENTO',RD],['OK',YE],['RÁPIDO',GR]]}),'resposta lenta perde a venda.'],
[3.7,5.7,'accent',lt=>lbl('Resposta escrita com IA',560,'rgba(255,255,255,.8)',eo(lt/.2))+typer(lt,{a:'Oi, Ana! Temos sim, com envio em até 24h. Posso separar o seu?',size:54,speed:34,top:650,box:true}),'a IA rascunha, você revisa.'],
[5.7,7.4,'dark',lt=>W(lt,[[0,'ANTES ×',110],[.15,'DEPOIS',110,BL2]],260)+slider(lt,{top:560,h:760,t0:.25,dur:1.1,L:{bg:'#FDECEC',k:'SEM IA · EXEMPLO',big:'6 h',sub:'para responder',c:RD},Rt:{bg:'#EAF0FF',k:'COM IA · EXEMPLO',big:'5 min',sub:'para responder',c:BL},bigSize:200}),'de horas para minutos.'],
[7.4,9.0,'light',lt=>W(lt,[[0,'AVALIAÇÃO',120],[.15,'SOBE.',120,BL]],260)+liquid(lt,{pct:4.9,dec:1,suffix:'★',top:600,t0:.15,dur:1.2,fill:BL})+lbl('Exemplo hipotético',1360,'#7A7F8C'),'e a avaliação acompanha.'],
[9.0,10.9,'accent',lt=>cta(lt,'ATENDE'),'e receba os prompts de atendimento no Direct.']];
const DUR=10.9;'''.replace('const DUR=10.9;','let DUR=10.9;const K=1.7;SC.forEach(s=>{s[0]*=K;s[1]*=K});DUR*=K;'),'2026-11-20/21_reel_atende'),
'fotos':('''const THEME={dark:'#000000',light:'#F1F3F8',accent:'radial-gradient(900px 900px at 30% 20%,#7FA3FF,#2F6BFF 50%,#1A3FB0)',anim:'left',trans:'zoom',deco:'rings',align:'left'};
const SC=[
[0,1.9,'dark',lt=>W(lt,[[0,'FOTO ESCURA',120],[.15,'VENDE MENOS.',120,BL2]],260)+magnifier(lt,{top:620,errors:[[330,770,.5],[720,900,.9],[460,1080,1.3]]}),'foto escura vende menos.'],
[1.9,3.8,'light',lt=>slider(lt,{top:420,h:900,t0:.2,dur:1.3,L:{bg:'#3A3D47',k:'ANTES',big:'Foto escura',sub:'fundo bagunçado',c:'#FF8A95'},Rt:{bg:'#FFFFFF',k:'DEPOIS',big:'Foto clara',sub:'fundo limpo',c:BL},bigSize:110}),'antes e depois, só com o celular.'],
[3.8,5.6,'accent',lt=>W(lt,[[0,'SÓ COM O',110],[.15,'CELULAR.',110]],260)+phone3d(lt,{top:520,after:'luz da janela + fundo branco',afterCol:BL,ta:1.1}),'luz da janela e fundo branco.'],
[5.6,7.3,'dark',lt=>W(lt,[[0,'ESQUEÇA O',130]],560)+strike(lt,.6,'FILTRO.',780,210),'nada de filtro pesado.'],
[7.3,9.0,'light',lt=>W(lt,[[0,'MAIS',130],[.15,'CLIQUES ↑',130,BL]],280)+bars(lt,{label:'Cliques · exemplo',t0:.1}),'foto boa traz mais cliques.'],
[9.0,10.9,'accent',lt=>cta(lt,'FOTOS'),'e receba o checklist de fotos no Direct.']];
const DUR=10.9;'''.replace('const DUR=10.9;','let DUR=10.9;const K=1.7;SC.forEach(s=>{s[0]*=K;s[1]*=K});DUR*=K;'),'2026-11-21/27_reel_fotos'),
}
import os
for k,(js,out) in REELS.items():
    open(f'reel_{k}.html','w').write(HEAD+js+'\nR(0);\n</script></body></html>\n')
    os.makedirs(f'../../entregas/{out}',exist_ok=True)
print('ok',len(REELS))
