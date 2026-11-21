# Caos Insano BR · sistema de 6 agentes

```
 1 CAÇADOR DE TENDÊNCIAS ─► 2 ROTEIRISTA ─► 3 VOZ ─► 4 EDITOR ─► 5 MINIATURAS ─► 6 ENVIADOR
   (Claude pesquisa)        a2_roteiro.py   a3_voz.py  a4_editor.py  a5_miniatura.py  a6_enviador.py
   fila/<data>/pautas.json  regras         ElevenLabs  takes + neon   capa v3          IG automático
                                           (Lucas)     + legenda       + títulos        YT/TikTok: pacote
```

| # | Agente | O que faz | Automático? |
|---|---|---|---|
| 1 | Caçador de tendências | Pesquisa o que está em alta sobre GTA 6 (imprensa, streamers, Shorts mais vistos), descarta o que já foi feito e escreve as 3 pautas do dia com fontes. Procedimento: `a1_tendencias.md` | Sim (Claude) |
| 2 | Escritor de roteiro | Gancho ≤ 12 palavras (≈ 3 s) → desenvolvimento → CTA "se inscreve e segue no TikTok". Confere total de palavras (20–35 s), fontes, "segundo jogadores", spoiler, títulos e tags. | Sim |
| 3 | Gerador de voz | Narração com a voz aprovada (Lucas, ElevenLabs), frase a frase, com cache. Prévia em `<id>_voz.wav`. | Sim |
| 4 | Editor de gameplay | Escolhe um take por cena no catálogo de gameplay oficial (`catalogo_takes.json`, por tag, girando para não repetir) ou clipe autorizado (`autorizados.json`, com crédito na tela). 9:16, overlay neon, legenda, trilha com ducking, SFX. Nunca usa áudio dos trailers/clipes. | Sim |
| 5 | Criador de miniaturas | Capa v3: personagem oficial recortado (BiRefNet), palavra atrás, faixa amarela na frente. | Sim |
| 6 | Enviador | Instagram: sobe mídia para o site e cria o pacote de publicação; o Claude publica no horário pela Windsor. YouTube/TikTok: `PACOTE_UPLOAD.md` + zip (a Windsor não publica nessas redes). | IG sim · YT/TT manual |

## Rodar
```bash
# depois que o agente 1 escreveu fila/2026-11-21/pautas.json
python3 pipeline.py 2026-11-21            # agentes 2→6 + commit/push
python3 pipeline.py 2026-11-21 --de a4    # recomeça de uma etapa
```
Saída: `gta6/entregas/auto/<data>/` (vídeos, capas, prévias de voz, `PACOTE_UPLOAD.md`, zip) · status em `fila/<data>/status.json`.

## Regras fixas
- Fatos: só imprensa/Rockstar ou "segundo jogadores". Sem spoiler.
- Gameplay de terceiros só com autorização (`autorizados.json`). Gaules: 24 h após o fim da VOD, com crédito.
- Instagram: uma chamada por post; em timeout **nunca** reenviar — conferir na Windsor.
- Os brutos (`/home/user/gta6_brutos`) ficam fora do repositório; se o container for recriado, é preciso baixar de novo (trailers e "An Extended Look" da página de downloads da Rockstar).
