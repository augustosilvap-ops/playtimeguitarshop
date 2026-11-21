"""AGENTE 6 · ENVIADOR — prepara a publicação de cada vídeo:
- Instagram (@caosinsano.br): sobe vídeo + capa para o site de mídias e grava o pacote gta6/publicacao/<data>/<id>.json
  (a publicação é feita pelo Claude via Windsor no horário, com lembrete agendado; em timeout NUNCA reenviar).
- YouTube e TikTok: a Windsor não publica lá → gera PACOTE_UPLOAD.md (título, descrição, tags, horário) + zip para postar no app.
Uso: python3 a6_enviador.py <data> [--sem-push]"""
import sys, shutil, subprocess, zipfile
from nucleo import *
def main(data, push=True):
    P = pautas(data); st = status(data); H = CFG['instagram']['horarios']; site = os.path.join(REPO, CFG['pasta_site']); os.makedirs(site, exist_ok=True)
    pub = os.path.join(GTA, 'publicacao', data); os.makedirs(pub, exist_ok=True); md = [f"# Caos Insano BR · pacote de upload {data}\n",
          "Instagram: automático (horários abaixo). YouTube Shorts e TikTok: postar no app com estes textos, 1–2 h de intervalo entre vídeos.\n"]
    agenda = []
    for i, p in enumerate(P):
        if 'editor' not in st.get(p['id'], {}) or 'miniatura' not in st.get(p['id'], {}): log('enviador', f"{p['id']} ✗ falta vídeo ou capa"); continue
        vid = os.path.join(REPO, st[p['id']]['editor']['video']); cap = os.path.join(REPO, st[p['id']]['miniatura']['capa'])
        nome = f"a{data.replace('-', '')[4:]}_{p['id']}"; shutil.copy(vid, f'{site}/{nome}.mp4'); shutil.copy(cap, f'{site}/{nome}_capa.jpg')
        hora = p.get('horario') or H[i % len(H)]; cred = st[p['id']]['editor'].get('creditos', [])
        leg = p['titulos']['ig'] + ('\n\n' + ' · '.join('Gameplay: ' + c for c in cred) if cred else '') + '\n\n' + CFG['rodape_ig'] + '\n\n' + ' '.join('#' + t.lstrip('#') for t in p['tags'][:5])
        j = {"hora": hora, "acao": "create_video_post", "connector": "instagram", "account": CFG['instagram']['account'], "perfil": CFG['instagram']['perfil'], "data": data, "status": "agendado",
             "params": {"video_url": CFG['site_midias'] + nome + '.mp4', "cover_url": CFG['site_midias'] + nome + '_capa.jpg', "share_to_feed": True, "caption": leg}}
        json.dump(j, open(f"{pub}/{p['id']}.json", 'w'), ensure_ascii=False, indent=1); agenda.append((hora, p['id']))
        md += [f"\n## {p['id']} · {p['tema']} — IG {hora}\n", f"- Arquivo: `{os.path.basename(vid)}` · capa `{os.path.basename(cap)}`\n",
               f"- **YouTube** título: {p['titulos']['yt']}\n- **YouTube** descrição: {p.get('descricao_yt', '')} " + ' '.join('#' + t.lstrip('#') for t in p['tags']) + "\n",
               f"- **YouTube** tags: {', '.join(t.lstrip('#') for t in p['tags'])}\n", f"- **TikTok** legenda: {p['titulos']['tt']}\n",
               f"- Fontes: " + '; '.join(e.get('fonte', '') for e in p.get('evidencia', [])) + "\n"]
        marcar(data, p['id'], 'enviador', ig=hora, pacote=f"gta6/publicacao/{data}/{p['id']}.json")
    out = saida(data); open(f'{out}/PACOTE_UPLOAD.md', 'w').write(''.join(md))
    with zipfile.ZipFile(f'{out}/CaosInsano_{data}.zip', 'w') as z:
        for f in sorted(os.listdir(out)):
            if f.endswith(('.mp4', '.jpg', '.md')): z.write(f'{out}/{f}', f)
    log('enviador', f"pacote {out}/CaosInsano_{data}.zip")
    if push:
        g = lambda *a: subprocess.run(['git', '-C', REPO, *a], check=True)
        g('add', CFG['pasta_site'], f'gta6/publicacao/{data}', f'gta6/entregas/auto/{data}', f'gta6/agentes/fila/{data}', 'gta6/agentes/uso_takes.json', 'gta6/src/capas_v3')
        g('commit', '-q', '-m', f"Caos Insano: pipeline {data} ({len(agenda)} vídeos)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01KxZ3QMQc7vQukPgiLarXU4")
        br = subprocess.run(['git', '-C', REPO, 'branch', '--show-current'], capture_output=True, text=True).stdout.strip()
        g('push', '-q', 'origin', br); g('push', '-q', 'origin', 'HEAD:main')
    print('AGENDA_IG', json.dumps(agenda))
if __name__ == '__main__': main(sys.argv[1], '--sem-push' not in sys.argv)
