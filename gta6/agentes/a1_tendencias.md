# AGENTE 1 · CAÇADOR DE TENDÊNCIAS (executado pelo Claude)

Objetivo: escolher os **3 assuntos do dia** sobre GTA 6 que mais têm gente procurando e que ainda não usamos.

## Passo a passo
1. **Pesquisar** (WebSearch `extended`, 2–4 buscas no mesmo turno):
   - "GTA 6 players discover / hidden features / easter eggs" + mês atual;
   - "GTA 6 tips / things the game doesn't tell you";
   - o que os streamers estão mostrando (Kotaku, TechRadar, PC Gamer, GamingBible, IGN, VGC; Reddit r/GTA6 via imprensa).
   - YouTube: skill `tubealfred-youtube:youtube-shorts` / `youtube-keyword-ideas` para ver os Shorts de GTA 6 com mais views nas últimas 48 h.
2. **Filtrar**
   - Descartar o que já foi feito: ver `historico.md` (temas publicados) e as pastas `fila/*/pautas.json`.
   - Sem spoiler da história. Sem afirmação que só uma fonte duvidosa sustenta.
   - Classificar: `oficial` (Rockstar/imprensa confirmou) ou `jogadores` (descoberta da comunidade → a fala diz "segundo jogadores").
3. **Ranquear** por: (a) quantas fontes falam do assunto nas últimas 48 h, (b) se é útil ("salva essa dica") ou surpreendente ("não acredito"), (c) se temos take de gameplay que mostra (ver `catalogo_takes.json` → tags).
4. **Escrever** `fila/<data>/pautas.json` (formato abaixo) e rodar `python3 a2_roteiro.py <data>`; corrigir até passar.

## Formato de cada pauta
```json
{"id": "e28", "slug": "ufo", "tema": "...", "confirmado": "jogadores", "horario": "18:00",
 "evidencia": [{"fonte": "URL", "nota": "o que a fonte diz"}],
 "cenas": [
  {"tipo": "title", "params": {"html": "...", "size": 170, "top": 300}, "fala": "GANCHO ≤ 12 palavras", "take": {"tag": "aeroporto"}},
  {"tipo": "rank", "params": {"n": 1, "html": "...", "sub": "...", "sky": 1}, "fala": "...", "take": {"src": "EL", "t": 1132}},
  {"tipo": "subs", "fala": "... Se inscreve e segue no TikTok.", "take": {"tag": "final"}}],
 "capa": {"top": "PALAVRA", "bar": "COMPLEMENTO", "personagem": "Jason Duval/Jason_Duval_05.jpg"},
 "titulos": {"yt": "... #shorts (≤ 70)", "tt": "... #gta6 #fyp", "ig": "..."},
 "descricao_yt": "...", "tags": ["gta6", "gtavi", "..."]}
```
Tipos de cena: `title`, `rank`, `num`, `years`, `delay`, `map`, `check`, `song`, `cta`, `subs` (ver exemplos em `../src/gen_caos.py`).
Tags de take: ver `catalogo_takes.json` (carro, direcao, perseguicao, policia, tiroteio, assalto, casa, tv, animais, praia, mar, aeroporto, aviao, boate, festa, cidade, aereo, mapa, vista, terraco, por_do_sol, moto, natureza, final…).
Personagens da capa: pastas em `<brutos>/shots/People/` (evitar repetir o da véspera).
