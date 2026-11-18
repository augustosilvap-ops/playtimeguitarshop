# Canal de cortes de GTA 6 (YouTube Shorts + TikTok) — estudo (18/11/2026)

## 1. Situação
- GTA 6 sai em 19/11/2026 (PS5/Xbox). Já há centenas de lives BR (alanzoka, Cellbit, Skorpion, PaulinhoLOKO, kosky…) e o YouTube fará live oficial de 24 h com a Rockstar.
- Janela de oportunidade: as primeiras 2–3 semanas concentram a busca por "GTA 6".

## 2. Regras que mandam no projeto
| Quem | Regra | O que significa para nós |
|---|---|---|
| Streamers | A live é deles (direito autoral) | Cortar sem autorização = reivindicação/strike (3 strikes = canal cai). Precisa de OK por escrito. |
| YouTube | Política de conteúdo reutilizado / "inautêntico" (vale para o canal inteiro) | Corte cru, sem nada nosso, não monetiza e o Shorts entrega menos. Autorização NÃO resolve isso — precisa de edição/comentário/contexto. |
| YouTube | Violência gráfica: novas regras de anúncio para games (set/2026) | Nada de violência pesada nos primeiros segundos; compilação só de violência = restrita. Título e thumb revisados à parte. |
| Rockstar/Take-Two | Uso de vídeo do jogo é tolerado para fãs, uso "não comercial", e sem spoilers da história | Spoiler de história = derrubada. Monetizar gameplay fica numa zona cinzenta (é prática comum, mas não é garantido pela política). |
| TikTok | Conteúdo não original perde alcance | Mesma lógica: precisa de algo nosso. |

## 3. Três caminhos (do mais seguro ao mais arriscado)
1. **Gameplay própria (recomendado):** você joga e grava (PS5/Xbox gravam direto), sobe na pasta do Drive e eu corto. Zero problema com streamer.
2. **Streamers que autorizam:** streamers pequenos/médios (1–20 mil seguidores) querem crescer e costumam aceitar clipador. Mandar DM pedindo autorização (modelo abaixo) e guardar o print.
3. **Notícias e curiosidades com narração:** "5 coisas que ninguém viu no mapa", "segredos escondidos" — usando trechos curtos do trailer/gameplay + narração do Lucas (ElevenLabs) + legenda. É conteúdo transformado (original). SEM spoiler de história.

Evitar: cortar lives grandes (alanzoka, Cellbit etc.) sem autorização — o risco de derrubada é alto e os canais oficiais deles já cortam.

## 4. O que vira "conteúdo nosso" em cada corte
- Gancho escrito nos 2 primeiros segundos ("ELE NÃO ESPERAVA ISSO").
- Legenda grande palavra por palavra (já temos o motor dos Reels).
- Contexto/narração curta no início ou no fim (voz Lucas).
- Crédito do streamer na tela e na descrição.
- Série com nome fixo ("Plantão do Caos #12") — cria hábito.

## 5. Automação — o que dá e o que falta
| Etapa | Status |
|---|---|
| Achar melhores momentos (transcrição + picos de áudio/reação) | ✅ consigo (whisper + ffmpeg, já instalados) |
| Cortar 9:16, 20–50 s, câmera do streamer + gameplay | ✅ consigo |
| Legenda grande + gancho + narração Lucas + SFX | ✅ consigo (mesmo motor dos Reels) |
| Baixar vídeos da Twitch/YouTube/Kick | ❌ bloqueado neste ambiente → entrada pela pasta do Google Drive (já conectado) |
| Postar no YouTube | ⚠️ Windsor não faz upload. Opções: API do YouTube (precisa criar projeto no Google Cloud) ou um agendador com API (ex.: Upload-Post/Ayrshare — 1 chave para YouTube + TikTok + Instagram, pago) |
| Postar no TikTok | ⚠️ API oficial exige aprovação do app (semanas). Via agendador com API é imediato. |
| Fila de aprovação | ✅ no Nexus, igual ao Instagram |

Fluxo proposto: vídeo na pasta do Drive → eu gero 3–5 cortes/dia → aparecem no Nexus → você aprova → publica no horário (YouTube + TikTok).

## 6. Nome do canal (sugestões — não usar "GTA", "Rockstar", "Vice City" ou "Leonida" no nome: são marcas deles)
- Plantão do Caos
- Modo Caos BR
- Rolê Insano
- Fuga Total
Conferir disponibilidade do @ no YouTube e no TikTok antes de criar.

## 7. Modelo de DM para streamer
> Fala, [nome]! Curto muito suas lives de GTA 6. Tenho um canal de cortes e queria pedir autorização para postar cortes das suas lives no YouTube Shorts e no TikTok, sempre com seu @ na tela e o link do seu canal na descrição. Se em algum momento não quiser, eu tiro na hora. Posso?

## 8. O que o Augusto precisa fazer
1. Criar uma conta Google nova (ou canal de marca) e o perfil no TikTok com o nome escolhido.
2. Decidir o caminho (1, 2 ou 3 — dá para combinar 1 + 3).
3. Criar uma pasta no Google Drive "GTA6 — brutos" e me passar.
4. Escolher como postar automático: API do YouTube (grátis, mais configuração) ou agendador com API (pago, simples).

Fontes: Rockstar Support (política de material com direitos), páginas de ajuda do YouTube (conteúdo reutilizado), Dexerto/GTABoom (regras de violência para o GTA 6), O Tempo/Adrenaline/O Liberal (lançamento e lives BR).
