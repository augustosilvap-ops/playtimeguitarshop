"""Gera os PDFs: python3 build.py  (troca [[i:nome]] pelos ícones Lucide e imprime com Playwright)."""
import re, pathlib, subprocess, json
D = pathlib.Path(__file__).resolve().parent
def icon(m):
    svg = (D/'icons'/f'{m.group(1)}.svg').read_text()
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S).strip()
    svg = re.sub(r'class="[^"]*"', 'class="ic"', svg, count=1)
    svg = re.sub(r'\s(width|height)="24"', '', svg)
    return re.sub(r'\s+', ' ', svg)
jobs = [('aula_cap1.html', 'Aula_Cap1_Desenvolvendo_meu_talento.pdf', 'A4'),
        ('aluno_cap1.html', 'Material_do_Aluno_Cap1.pdf', 'A5')]
for src, pdf, fmt in jobs:
    out = D/('.build_'+src)
    out.write_text(re.sub(r'\[\[i:([a-z-]+)\]\]', icon, (D/src).read_text()))
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const [f,o,fmt] of %s){await p.goto('file://'+f,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:o,format:fmt,printBackground:true,preferCSSPageSize:true});}await b.close();})();""" % json.dumps(
    [[str(D/('.build_'+s)), str(D/p), f] for s, p, f in jobs])
subprocess.run(['node', '-e', js], check=True)
for s, _, _ in jobs: (D/('.build_'+s)).unlink()
print('ok')
