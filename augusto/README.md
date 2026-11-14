# @augustosilva.p — sistema de conteúdo

**Documento mestre:** `sistema/BRIEFING_MESTRE.md` · **Regras de produção:** `sistema/SISTEMA_VISUAL_E_EDITORIAL.md`

| Pasta | O que tem |
|---|---|
| `sistema/` | Briefing mestre, tokens, tipografia, as 4 direções, regras de alternância, linha editorial e checklist de QA |
| `editorial/` | `CALENDARIO.md` + `Calendario_16-22nov.xlsx` (21 publicações, 3 por dia, palavra-chave única por post). Fonte: `calendario.py`, que trava palavra-chave duplicada |
| `previa/` | Capas 01–09 e prévia da grade do perfil (`grade_3x3.png`, `grade_3x3_rotulada.png`) |
| `entregas/2026-11-16/` | Dia 1 completo: artes finais, legenda, roteiro de Direct, testes e material gratuito de cada post |
| `src/` | Fonte editável: `base.css` (tokens e componentes), `pecas/*.html` (artes), `materiais/` (PDFs e planilha), `render.js`, `pdf.js`, `reel.sh`, `grade.py` |

## Status (14/11/2026)

| ID | Peça | Arte | Legenda | Recompensa | Manychat | Agendado |
|---|---|---|---|---|---|---|
| 01 | Estático · Taxas | ✅ | ✅ | ✅ PDF | não configurado | não |
| 02 | Carrossel · 5 custos (8 slides) | ✅ | ✅ | ✅ PDF 12 p. | não configurado | não |
| 03 | Reel 7s · Precificar mesmo sendo leigo | ✅ MP4 + capa | ✅ | ✅ XLSX | não configurado | não |
| 04–09 | Capas para validar a grade | ✅ capa | — | — | — | não |
| 10–21 | Planejados no calendário | — | — | — | — | não |

## Como regenerar
```bash
cd augusto/src
node render.js pecas/02_custos.html pecas/01_03_taxas_reel.html pecas/capas_04_09.html   # PNGs
node pdf.js materiais/guia_precificacao.html <saida.pdf>                                  # PDFs
python3 materiais/planilha_precificacao.py <saida.xlsx>                                     # planilha
./reel.sh 308 2 1300 build/reel03_overlay.png build/reel03_mask.png <saida.mp4>             # Reel
cd .. && python3 src/grade.py                                                               # grade 3x3
```
