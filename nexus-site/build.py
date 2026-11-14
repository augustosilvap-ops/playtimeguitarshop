"""Gera nexus-site/public/index.html a partir de nexus/index.html (fonte única).
Uso: python3 nexus-site/build.py  (rodar na raiz do repositório)"""
import shutil, os
s = open('nexus/index.html').read()
R = [
 ("O chat precisa da permissão “Perguntar ao Claude”. Abra Ajustes → Permissões.", "O chat com IA fica no Nexus dentro do Claude. Aqui no site você vê os números, aprova conteúdo e marca tarefas."),
 ("A execução direta precisa do conector Claude Code Remote liberado em Ajustes → Permissões.", "Para executar tarefas, use o Nexus dentro do Claude."),
 ("sample?'Claude · lê os dados ao vivo':'chat indisponível nesta visualização'", "sample?'Claude · lê os dados ao vivo':'chat disponível no Nexus dentro do Claude'"),
]
for a, b in R:
    assert a in s, a[:40]; s = s.replace(a, b)
diag = ('<div class="box" style="grid-column:1/-1"><h3>Diagnóstico das conexões</h3><p>Mostra se cada conexão está configurada e a resposta de cada serviço. Nenhuma chave aparece aqui.</p>'
  '<div><button class="act" onclick="this.disabled=true;this.textContent=\'Verificando…\';nexusDiag().then(j=>{document.getElementById(\'diag\').textContent=JSON.stringify(j,null,2)}).catch(e=>{document.getElementById(\'diag\').textContent=\'Erro: \'+JSON.stringify(e)}).finally(()=>{this.disabled=false;this.textContent=\'Verificar de novo\'})">Verificar agora</button></div>'
  '<pre id="diag" style="white-space:pre-wrap;font:12px var(--f-m);color:var(--fg);margin:0"></pre></div>'
  '<div class="box"><h3>Sessão</h3><p>Sair deste aparelho.</p><div><button class="act" onclick="nexusLogout()">Sair</button></div></div>')
a = '<div class="box"><h3>Voz</h3>'; assert a in s; s = s.replace(a, diag + a, 1)
css = open('nexus-site/login.css').read()
head = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="robots" content="noindex,nofollow"><script src="shim.js"></script>' + css)
i = s.index('<div class="shell">')
open('nexus-site/public/index.html', 'w').write(head + s[:i] + '</head><body>' + s[i:] + '</body></html>')
shutil.copy('nexus/holo.webp', 'nexus-site/public/holo.webp')
os.makedirs('nexus-site/public/posts', exist_ok=True)
for f in os.listdir('nexus/posts'): shutil.copy('nexus/posts/' + f, 'nexus-site/public/posts/' + f)
print('ok')
