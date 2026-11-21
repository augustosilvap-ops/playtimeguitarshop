"""CAOS INSANO BR · publicador automático de YouTube Shorts e TikTok (roda no GitHub Actions, sem servidor).

Lê a fila gta6/publicacao/<data>/<id>.json (campos "yt", "tt", "publicar_em", "arquivo") e, quando chega o horário,
envia o vídeo. O estado (o que já foi enviado) fica em status.json, guardado na branch "caos-status" pelo workflow.

Chaves (GitHub → Settings → Secrets and variables → Actions), nunca no código:
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN      → YouTube Data API v3 (escopo youtube.upload)
  TT_CLIENT_KEY, TT_CLIENT_SECRET, TT_REFRESH_TOKEN     → TikTok Content Posting API (escopo video.upload)
Sem as chaves de uma rede, ela é ignorada. Vídeos com horário vencido há mais de JANELA_H horas não são enviados.

YouTube: projeto ainda sem auditoria → o YouTube deixa o vídeo PRIVADO (é só trocar para Público no app).
         Defina a variável YT_PRIVACIDADE=public no repositório quando a auditoria for aprovada.
TikTok : sem auditoria, o vídeo vai para a caixa de RASCUNHOS do app (você toca em publicar).

Uso: python3 gta6/publicar/yt_tt.py status.json [--simular]"""
import os, sys, json, glob, datetime, math
import urllib.request, urllib.parse

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
JANELA_H = float(os.environ.get('JANELA_H', '6'))
SIMULAR = '--simular' in sys.argv


def http(url, data=None, headers=None, method=None):
    if isinstance(data, dict):
        data = json.dumps(data).encode(); headers = {**(headers or {}), 'Content-Type': 'application/json; charset=UTF-8'}
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=300) as r:
        corpo = r.read()
        return r.status, dict(r.headers), (json.loads(corpo) if corpo[:1] in (b'{', b'[') else corpo)


def form(url, campos):
    return http(url, urllib.parse.urlencode(campos).encode(), {'Content-Type': 'application/x-www-form-urlencoded'}, 'POST')[2]


# ---------- YouTube ----------
def yt_token():
    e = os.environ
    if not all(e.get(k) for k in ('YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN')): return None
    return form('https://oauth2.googleapis.com/token', {'client_id': e['YT_CLIENT_ID'], 'client_secret': e['YT_CLIENT_SECRET'],
                                                        'refresh_token': e['YT_REFRESH_TOKEN'], 'grant_type': 'refresh_token'})['access_token']


def yt_enviar(tok, arquivo, yt):
    meta = {'snippet': {'title': yt['titulo'][:100], 'description': yt.get('descricao', ''), 'tags': yt.get('tags', [])[:15],
                        'categoryId': '20', 'defaultLanguage': 'pt-BR', 'defaultAudioLanguage': 'pt-BR'},
            'status': {'privacyStatus': os.environ.get('YT_PRIVACIDADE', 'private'), 'selfDeclaredMadeForKids': False}}
    tam = os.path.getsize(arquivo)
    _, h, _ = http('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status', meta,
                   {'Authorization': f'Bearer {tok}', 'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(tam)}, 'POST')
    destino = h.get('Location') or h.get('location')
    _, _, r = http(destino, open(arquivo, 'rb').read(), {'Authorization': f'Bearer {tok}', 'Content-Type': 'video/mp4'}, 'PUT')
    return {'video_id': r['id'], 'url': f"https://youtube.com/shorts/{r['id']}", 'privacidade': meta['status']['privacyStatus']}


# ---------- TikTok ----------
def tt_token():
    e = os.environ
    if not all(e.get(k) for k in ('TT_CLIENT_KEY', 'TT_CLIENT_SECRET', 'TT_REFRESH_TOKEN')): return None
    return form('https://open.tiktokapis.com/v2/oauth/token/', {'client_key': e['TT_CLIENT_KEY'], 'client_secret': e['TT_CLIENT_SECRET'],
                                                                'grant_type': 'refresh_token', 'refresh_token': e['TT_REFRESH_TOKEN']})['access_token']


def tt_enviar(tok, arquivo):
    tam = os.path.getsize(arquivo); bloco = min(tam, 10_000_000); n = max(1, tam // bloco)
    _, _, r = http('https://open.tiktokapis.com/v2/post/publish/inbox/video/init/',
                   {'source_info': {'source': 'FILE_UPLOAD', 'video_size': tam, 'chunk_size': bloco, 'total_chunk_count': n}},
                   {'Authorization': f'Bearer {tok}'}, 'POST')
    url, pid = r['data']['upload_url'], r['data']['publish_id']; dados = open(arquivo, 'rb').read()
    for i in range(n):
        ini = i * bloco; fim = tam - 1 if i == n - 1 else ini + bloco - 1
        http(url, dados[ini:fim + 1], {'Content-Type': 'video/mp4', 'Content-Range': f'bytes {ini}-{fim}/{tam}'}, 'PUT')
    return {'publish_id': pid, 'destino': 'rascunhos do app'}


# ---------- fila ----------
def main():
    st_path = sys.argv[1]; st = json.load(open(st_path)) if os.path.exists(st_path) else {}
    agora = datetime.datetime.now(datetime.timezone.utc)
    yt = yt_token() if not SIMULAR else 'simulado'; tt = tt_token() if not SIMULAR else 'simulado'
    print(f'YouTube {"pronto" if yt else "sem chaves"} · TikTok {"pronto" if tt else "sem chaves"}')
    for f in sorted(glob.glob(os.path.join(RAIZ, 'gta6/publicacao/*/*.json'))):
        j = json.load(open(f))
        if 'publicar_em' not in j or 'arquivo' not in j: continue
        quando = datetime.datetime.fromisoformat(j['publicar_em'])
        chave = os.path.relpath(f, RAIZ); feito = st.setdefault(chave, {})
        if quando > agora: continue
        atraso = (agora - quando).total_seconds() / 3600
        arq = os.path.join(RAIZ, j['arquivo'])
        for rede, chv, tok, fn in (('youtube', 'yt', yt, lambda t: yt_enviar(t, arq, j['yt'])), ('tiktok', 'tt', tt, lambda t: tt_enviar(t, arq))):
            if not tok or rede in feito or chv not in j: continue
            if atraso > JANELA_H: feito[rede] = {'pulado': f'{atraso:.1f} h de atraso'}; continue
            if SIMULAR: print(f'[simulação] {rede} ← {chave}'); continue
            try:
                feito[rede] = {**fn(tok), 'em': agora.isoformat(timespec='seconds')}; print(f'✓ {rede} ← {chave}: {feito[rede]}')
            except Exception as e:  # não tenta de novo sozinho: o envio pode ter entrado (evita vídeo duplicado)
                feito[rede] = {'falhou': str(e)[:300], 'em': agora.isoformat(timespec='seconds')}; print(f'✗ {rede} ← {chave}: {e}')
    json.dump(st, open(st_path, 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
