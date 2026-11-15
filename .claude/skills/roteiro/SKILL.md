---
name: roteiro
description: Escreve roteiros de Reels (formato mini-aula aprovado), carrosséis e estáticos do @augustosilva.p, prontos para virar arte em augusto/src/motion/gen_aula.py e nos modelos v4. Use quando o Augusto pedir "roteiro", "script", "escreva o Reel", "estrutura do carrossel" ou um post novo do calendário.
---

# Roteiro — padrão aprovado (15/11/2026)

Antes de escrever: leia `CLAUDE.md`, `augusto/sistema/BRIEFING_MESTRE.md` e o calendário `augusto/editorial/CALENDARIO.md` (palavra-chave e recompensa do post). Use a skill **hooks** para o gancho e a skill **voz** para o tom.

## Reel = MINI-AULA (~36–42 s, 9–11 cenas)
Ordem fixa:
1. **Gancho** (problema + "vamos fazer a conta / resolver com um exemplo").
2. **Exemplo com números** (o cenário, marcado como exemplo).
3. **O erro comum** (o que a maioria faz).
4. **Por que dá errado** — com a conta ou o motivo na tela (ex.: taxas são cobradas sobre o PREÇO).
5. **Passos 1…4/5** — cada passo diz O QUE fazer, O QUE ENTRA e ONDE ACHAR o número (tabela da categoria, contador, busca do marketplace…).
6. **A conta em etapas** (quando houver cálculo) — uma operação por linha.
7. **Conferência / resultado** — prove que o método funciona (ex.: R$ 12,54 = 15% ✓).
8. **Resumo** em 4–5 itens para salvar.
9. **CTA**: "Comente PALAVRA e receba X no Direct" + "Leia a legenda ↓".

Saída em tabela: `cena · fundo (dark/light/accent) · texto grande (≤3 palavras por linha) · elemento animado (table, typer, gauge, liquid, slider, donut, bars, notifs, magnifier, route, calendar, phone3d, stamp/split/strike/glass) · legenda da cena (frase explicativa completa, ≤90 caracteres) · duração (2,0–2,8 s)`.
- Confira TODAS as contas antes de entregar (mostre a verificação).
- Varie o tema visual em relação ao Reel anterior (ver temas em `gen_aula.py`).
- Sem personagens e sem carrinho (reprovados).

## Carrossel (v4 aprovado)
7–8 slides: capa com hook + elemento herói grande → problema com exemplo → passos (1 por slide, com anotação) → conferência → CTA + presente com faixa "Comente PALAVRA". Fundo sólido (claro ou navy), bloco azul na palavra-chave, no máx. 1 elemento de apoio por slide.

## Legenda do post
Gancho → 3–5 linhas com o passo a passo → exemplo marcado como hipotético → CTA "Comente PALAVRA e eu te envio X no Direct" → 5 hashtags. Inclua o roteiro de Direct do Manychat (gatilho, resposta pública, mensagem, botão).
