# Live Paulinho o LOKO (GTA 6 O ÍNICIO) — plano de cortes
- Autorização: DM (informada pelo Augusto em 23/11/2026). Crédito na tela: youtube.com/@PaulinhoLOKOoficial.
- 23/11: Drive bloqueou download ("Quota exceeded") no original e na cópia. Tentar de novo em 24/11 com UM download completo (curl) para `/home/user/gta6_brutos/lives/paulinho1/live.mp4` e cortar local.
- Picos e transcrições: `/home/user/gta6_brutos/lives/paulinho1/` (picos.json, transc.json, th/) — fora do repo; se o container mudar, refazer a análise a partir do arquivo local.
- Cortes aprovados para fazer: ver lote.json. Depois, procurar +3/4 momentos entre os 40 picos conferindo a imagem.
- Ferramenta: `gta6/src/cortes/corte.py <arquivo> <ini> <fim> "<TÍTULO>" "<crédito>" <saída> <cam>`.
