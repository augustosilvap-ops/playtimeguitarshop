"""Injeta no nexus/index.html: Storytelling (dos .md), Ideias de conteúdo e calendário de Conteúdo.
Rodar na raiz: python3 nexus/gerar_conteudo.py"""
import re, json, markdown
IDEIAS={
 'RUAH · @ruahwear_':[
  ('Reel','Invisível move','“Você não vê o vento. Vê o que ele move.” Tecido em movimento na rua, sem texto explicativo; termina no símbolo.'),
  ('Carrossel','Anatomia','“O que ninguém vê na sua camiseta”: gola canelada, etiqueta estampada que não coça, tag WE CARRY THE SPIRIT, versículo por dentro.'),
  ('Reel','O que você carrega?','Três pessoas (autorizadas) respondem “o que você carrega?” vestindo a peça. Não são avaliações de compra.'),
  ('Carrossel','As 4 estampas','RUACH, WE CARRY THE SPIRIT, INVISÍVEL MOVE e WHAT DO YOU CARRY?: o que cada uma carrega.'),
  ('Estático','Manifesto','“Não é sobre o que vestimos. É sobre o que carregamos.” Fundo preto, símbolo, muito respiro.'),
  ('Carrossel','Não é lixo. É bolsa.','A embalagem zip reutilizada no dia a dia: escola, academia, viagem.'),
  ('Story','Founder Nº','Cada novo Founder ganha o seu número; contador de vagas restantes.'),
  ('Carrossel','Black Friday · Leve 2','“Um para você, um para quem você quer alcançar.” Combo Leve 2 por R$ 269,90 (18 a 24/11).'),
  ('Reel','Drop de Natal','Contagem regressiva e bastidores do próximo drop (se for confirmado).'),
  ('Reel','Fora das quatro paredes','4 cenas: “Por que aquilo em que você acredita fica só dentro da igreja?” → “Uma geração que não tem vergonha de carregar o Espírito.” → WE CARRY THE SPIRIT.'),
  ('Carrossel','O arco das 4 estampas','Origem (RUACH) → identidade (WE CARRY THE SPIRIT) → convicção (INVISÍVEL MOVE) → convite (WHAT DO YOU CARRY?).'),
 ],
 '@augustosilva.p':[
  ('Reel','Faturei, mas não lucrei','Gancho: “Você vendeu muito e o dinheiro sumiu?” → onde o lucro escapou (exemplo hipotético).'),
  ('Carrossel','Premium × Clássico no Mercado Livre','Quando cada tipo de anúncio compensa, com a conta de margem (taxas oficiais).'),
  ('Estático','R$ 79 mudou o jogo','Notícia do frete do Mercado Livre perto de R$ 79 e o que revisar nos anúncios.'),
  ('Reel','3 prompts que eu uso toda semana','Gancho: “Você usa IA só pra escrever legenda?” → 3 usos práticos.'),
  ('Carrossel','Agentes de IA no WhatsApp','Como preparar o atendimento para a Black Friday com IA (com cuidados).'),
  ('Estático','Copiar preço do concorrente','“O custo dele não é o seu.” Erro de iniciante em uma imagem.'),
  ('Carrossel','Checklist antes de anunciar','Foto, título, ficha técnica, preço, frete, prazo: 8 itens.'),
  ('Reel','Bastidor: meu painel de vendas','Mostrando o Nexus: “Eu acompanho tudo num painel só.” (sem dados sensíveis).'),
  ('Carrossel','Quanto sobra de R$ 100','A cascata da venda até o lucro, com simulação marcada.'),
  ('Reel','Prazo de entrega vende','Gancho: “Seu produto é bom, mas não vende?” → prazo, frete e reputação.'),
 ],
}
p='nexus/index.html';s=open(p).read()
def md(f): return markdown.markdown(open(f).read(),extensions=['tables'])
STORY={'RUAH':md('storytelling/RUAH_storytelling.md'),'@augustosilva.p':md('storytelling/AUGUSTO_storytelling.md')}
blob='const STORY='+json.dumps(STORY,ensure_ascii=False)+';\nconst IDEIAS='+json.dumps(IDEIAS,ensure_ascii=False)+';\n'
s=re.sub(r'const STORY=.*?;\nconst IDEIAS=.*?;\n','',s,flags=re.S)
s=s.replace('const POSTS=',blob+'const POSTS=',1)
if 'data-v="storytelling"' not in s:
    s=s.replace('    <a href="#negocios" data-v="negocios">','''    <a href="#storytelling" data-v="storytelling"><svg viewBox="0 0 24 24"><path d="M4 4h12a4 4 0 0 1 4 4v12H8a4 4 0 0 1-4-4z"/><path d="M8 9h8M8 13h6"/></svg>Storytelling</a>
    <a href="#ideias" data-v="ideias"><svg viewBox="0 0 24 24"><path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg>Ideias</a>
    <a href="#negocios" data-v="negocios">''',1)
    s=s.replace(' negocios:()=>{',''' storytelling:()=>`<div class="hd"><h2>Storytelling</h2><span class="src">base de todo conteúdo</span></div>
  <div class="tabs">${Object.keys(STORY).map(k=>`<button class="tab" data-st="${esc(k)}" aria-selected="${k===stTab}">${esc(k)}</button>`).join('')}</div>
  <div class="story box">${STORY[stTab]}</div>`,
 ideias:()=>`<div class="hd"><h2>Ideias de conteúdo</h2><span class="src">baseadas no storytelling · 3 posts por dia: estático, carrossel e Reel</span></div>
  ${Object.entries(IDEIAS).map(([k,L])=>`<h3 style="font:600 17px var(--f-ui);margin-top:6px">${esc(k)}</h3><div class="g2">${L.map(([f,t,d])=>`<div class="box"><span class="k">${esc(f)}</span><h3>${esc(t)}</h3><p>${esc(d)}</p><div class="sugs"><button class="act" data-run="${esc('Produza completo o post “'+t+'” ('+f+') para '+k+', seguindo o storytelling em storytelling/ e o sistema visual v2. Ideia: '+d)}">▶ Produzir</button></div></div>`).join('')}</div>`).join('')}`,
 negocios:()=>{''',1)
    s=s.replace("  const t=e.target.closest('[data-tab]');","  const stb=e.target.closest('[data-st]');if(stb){stTab=stb.dataset.st;renderView();return}\n  const dy=e.target.closest('[data-dia]');if(dy){diaSel=dy.dataset.dia;renderView();return}\n  const t=e.target.closest('[data-tab]');",1)
    s=s.replace("let cur='inicio',tab='moda';","let cur='inicio',tab='moda',stTab='RUAH',diaSel='todos';",1)
    s=s.replace('/* órbita do cérebro */','''.story{font-size:14.5px;line-height:1.65;color:var(--fg)}
.story h1{font:700 26px var(--f-ui);margin:0 0 10px}.story h2{font:600 19px var(--f-ui);color:var(--cy);margin:22px 0 8px}
.story p,.story li{color:var(--fg)}.story blockquote{margin:0;border-left:3px solid var(--cy);padding:6px 14px;color:var(--dim);background:rgba(56,214,255,.06);border-radius:8px}
.story table{margin:8px 0}.story td,.story th{border-top:1px solid var(--line);vertical-align:top}
.cal{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:8px}
@media (max-width:760px){.cal{grid-template-columns:repeat(4,minmax(0,1fr))}}
.cal button{border:1px solid var(--line);background:rgba(2,10,18,.5);border-radius:12px;padding:10px 6px;cursor:pointer;color:var(--fg);display:grid;gap:2px;justify-items:center}
.cal button small{font:500 11px var(--f-ui);color:var(--dim);text-transform:uppercase;letter-spacing:.08em}
.cal button b{font:700 22px var(--f-ui)}
.cal button i{font-style:normal;font-size:11px;color:var(--cy)}
.cal button[aria-pressed=true]{background:var(--cy);color:#02131F;border-color:var(--cy)}.cal button[aria-pressed=true] small,.cal button[aria-pressed=true] i{color:#02131F}
.cal button:disabled{opacity:.35;cursor:default}
/* órbita do cérebro */''',1)
    # calendário no Conteúdo
    a="""<span class="src">${POSTS.filter(p=>(S.ap||{})[p.id]?.status==='aprovado').length}/${POSTS.length} aprovados · nada é publicado sem você</span></div>
  <div class="g2">${POSTS.map(p=>{"""
    assert a in s
    s=s.replace(a,"""<span class="src">${POSTS.filter(p=>(S.ap||{})[p.id]?.status==='aprovado').length}/${POSTS.length} aprovados · nada é publicado sem você</span></div>
  <div class="cal"><button data-dia="todos" aria-pressed="${diaSel==='todos'}"><small>semana</small><b>Todos</b><i>${POSTS.length} posts</i></button>${['16','17','18','19','20','21','22'].map((d,i)=>{const n=POSTS.filter(p=>(p.data||'').includes(d+'/11')).length;return `<button data-dia="${d}" aria-pressed="${diaSel===d}" ${n?'':'disabled'}><small>${['seg','ter','qua','qui','sex','sáb','dom'][i]}</small><b>${d}</b><i>${n?n+' posts':'—'}</i></button>`}).join('')}</div>
  <div class="g2">${POSTS.filter(p=>diaSel==='todos'||(p.data||'').includes(diaSel+'/11')).map(p=>{""",1)
open(p,'w').write(s)
open('storytelling/IDEIAS_DE_CONTEUDO.md','w').write('# Ideias de conteúdo\n\n'+'\n\n'.join(f'## {k}\n\n| Formato | Ideia | Como fazer |\n|---|---|---|\n'+'\n'.join(f'| {f} | {t} | {d} |' for f,t,d in L) for k,L in IDEIAS.items())+'\n')
print('ok')
