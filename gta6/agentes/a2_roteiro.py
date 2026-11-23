"""AGENTE 2 · ESCRITOR DE ROTEIRO — confere o roteiro de cada pauta contra as regras de retenção e de fatos.
Estrutura obrigatória: GANCHO (cena 1, ≤ 12 palavras ≈ 3 s) → DESENVOLVIMENTO (2–5 cenas) → CTA final (cena 'subs': inscreva-se + TikTok).
Fatos: 'confirmado' = 'oficial' (Rockstar/imprensa) ou 'jogadores' (descoberta da comunidade → a fala precisa dizer "segundo jogadores").
Uso: python3 a2_roteiro.py <data>   (sai com erro e lista os problemas se algo não passar)"""
import sys
from nucleo import *
TIPOS = {'title', 'rank', 'num', 'years', 'song', 'delay', 'map', 'check', 'subs', 'cta'}
PROIBIDO = ['spoiler', 'final da história', 'morre no final', 'vazou o final']
def checar(p):
    R = CFG['roteiro']; e = []; c = p.get('cenas', [])
    if not (R['cenas_min'] <= len(c) <= R['cenas_max']): e.append(f"{len(c)} cenas (use {R['cenas_min']}–{R['cenas_max']})")
    if c and palavras(c[0]['fala']) > R['gancho_max_palavras']: e.append(f"gancho com {palavras(c[0]['fala'])} palavras (máx. {R['gancho_max_palavras']})")
    if c and c[0]['tipo'] != 'title': e.append("cena 1 precisa ser 'title' (gancho na tela)")
    if c and c[-1]['tipo'] != 'subs': e.append("última cena precisa ser 'subs' (inscreva-se + TikTok)")
    tot = sum(palavras(x['fala']) for x in c)
    if not (R['palavras_min'] <= tot <= R['palavras_max']): e.append(f"{tot} palavras no total (use {R['palavras_min']}–{R['palavras_max']} ≈ 12–20 s)")
    for i, x in enumerate(c):
        if x['tipo'] not in TIPOS: e.append(f"cena {i+1}: tipo '{x['tipo']}' não existe")
        if 'take' not in x: e.append(f"cena {i+1}: sem take de fundo")
    txt = ' '.join(x['fala'].lower() for x in c)
    if p.get('confirmado') not in ('oficial', 'jogadores'): e.append("campo 'confirmado' deve ser 'oficial' ou 'jogadores'")
    if p.get('confirmado') == 'jogadores' and 'segundo jogadores' not in txt: e.append("descoberta da comunidade: a fala precisa dizer 'segundo jogadores'")
    if not p.get('evidencia'): e.append('sem evidência (fontes) da pauta')
    for w in PROIBIDO:
        if w in txt: e.append(f"possível spoiler: '{w}'")
    T = CFG['titulos']; ti = p.get('titulos', {})
    for k in ('yt', 'tt', 'ig'):
        if not ti.get(k): e.append(f'sem título {k}')
    if len(ti.get('yt', '')) > T['yt_max']: e.append(f"título YT com {len(ti['yt'])} caracteres (máx. {T['yt_max']})")
    if '#shorts' not in ti.get('yt', '').lower(): e.append('título YT sem #shorts')
    if len(p.get('tags', [])) > T['tags_max']: e.append('tags demais')
    cp = p.get('capa', {})
    if not ((cp.get('a') and cp.get('b')) or (cp.get('top') and cp.get('bar'))): e.append('capa incompleta (a, b, c)')
    if len(cp.get('b', '')) > 11: e.append("capa: palavra-chave (b) longa demais — até ~10 letras")
    if cp.get('arte') and not os.path.exists(os.path.join(SRC, 'thumb_v5/art', cp['arte'])): e.append(f"arte não existe: {cp['arte']}")
    return e, tot
def main(data):
    ok = True
    for p in pautas(data):
        e, tot = checar(p)
        if e: ok = False; log('roteiro', f"{p['id']} ✗ " + ' | '.join(e))
        else: log('roteiro', f"{p['id']} ✓ {len(p['cenas'])} cenas, {tot} palavras"); marcar(data, p['id'], 'roteiro', palavras=tot)
    if not ok: sys.exit(1)
if __name__ == '__main__': main(sys.argv[1])
