"""AGENTE 4 · EDITOR DE GAMEPLAY — monta o Short 9:16: take de gameplay por cena (catálogo oficial ou clipe autorizado),
overlay neon + legenda frase a frase, narração, trilha com ducking e SFX. Nunca usa o áudio dos trailers/clipes.
Escolha de take: {"src":"EL","t":1132} fixo, ou {"tag":"aeroporto"} → pega do catálogo o take dessa tag menos usado recentemente.
Clipe autorizado: {"clipe":"<id em autorizados.json>","t":12} → crédito na tela.
Uso: python3 a4_editor.py <data> [id ...]"""
import sys, glob, subprocess, shutil
from nucleo import *
import gen_caos as G, gen_takes as GT
CAT = json.load(open(os.path.join(AG, 'catalogo_takes.json')))['takes']
AUT = json.load(open(os.path.join(AG, 'autorizados.json')))
USO = os.path.join(AG, 'uso_takes.json')
def usados(): return json.load(open(USO)) if os.path.exists(USO) else {}
def escolher(tk, ja):
    if 'src' in tk: return (tk['src'], tk['t'], tk.get('x', .5)), None
    if 'clipe' in tk:
        c = next(c for c in AUT['clipes'] if c['id'] == tk['clipe']); GT.V['clip_' + c['id']] = os.path.join(BR, 'autorizados', c['arquivo'])
        return ('clip_' + c['id'], tk.get('t', 0), tk.get('x', .5)), AUT['criadores'][c['criador']]['credito']
    U = usados(); op = [c for c in CAT if tk['tag'] in c['tags'] and (c['src'], c['t']) not in ja]
    if not op: raise SystemExit(f"nenhum take com a tag '{tk['tag']}'")
    op.sort(key=lambda c: U.get(f"{c['src']}:{c['t']}", 0)); c = op[0]
    U[f"{c['src']}:{c['t']}"] = U.get(f"{c['src']}:{c['t']}", 0) + 1; json.dump(U, open(USO, 'w'))
    return (c['src'], c['t'], tk.get('x', .5)), None
def render(data, p, i):
    ja, bg, cred = set(), [], set()
    for c in p['cenas']:
        b, cr = escolher(c['take'], ja); ja.add(b[:2]); bg.append(b)
        if cr: cred.add(cr)
    G.REELS[p['id']] = [(G.S(c['tipo'], **c.get('params', {})), c['fala']) for c in p['cenas']]; GT.BG[p['id']] = bg
    out = os.path.join(saida(data), f"{p['id']}.mp4"); trilha = CFG['trilhas'][i % len(CFG['trilhas'])]
    sys.argv = ['gen_takes.py', p['id'], out]; cwd = os.getcwd(); os.chdir(SRC)
    try: GT.main(trilha=os.path.join(GTA, 'trilhas', trilha))
    finally:
        os.chdir(cwd)
        try: os.remove(os.path.join(SRC, f"takes_{p['id']}.html"))
        except OSError: pass
    if cred:  # crédito do criador na tela, o vídeo inteiro
        txt = 'Gameplay: ' + ' · '.join(sorted(cred)); tmp = out + '.tmp.mp4'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', out, '-vf', f"drawtext=fontfile={GTA}/fonts/ARN.ttf:text='{txt}':x=(w-tw)/2:y=170:fontsize=38:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=14",
                        '-c:a', 'copy', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', tmp], check=True); os.replace(tmp, out)
    return out, bg, sorted(cred)
def main(data, ids=None):
    for i, p in enumerate(pautas(data)):
        if ids and p['id'] not in ids: continue
        out, bg, cred = render(data, p, i)
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
        log('editor', f"{p['id']} ✓ {os.path.basename(out)} {d:.1f}s"); marcar(data, p['id'], 'editor', video=os.path.relpath(out, REPO), segundos=round(d, 1), takes=bg, creditos=cred)
if __name__ == '__main__': main(sys.argv[1], sys.argv[2:])
