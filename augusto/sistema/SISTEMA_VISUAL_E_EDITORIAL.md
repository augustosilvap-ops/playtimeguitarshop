# @augustosilva.p — Sistema visual e editorial

> Documento mestre: `BRIEFING_MESTRE.md` (nesta pasta). Este arquivo transforma as decisões do briefing em regras de produção.
> Código-fonte das artes: `augusto/src/` (HTML + CSS renderizados em PNG pelo Chromium; vídeos montados com ffmpeg).

---

## 1. Tokens (proposta — os hexadecimais não estavam fechados no briefing)

Todos ficam em `src/base.css`, no bloco `:root`. Mudar um valor ali atualiza todas as peças na próxima renderização.

| Token | Hex | Uso |
|---|---|---|
| `--ink` | `#070A12` | Preto de marca: texto sobre fundos claros |
| `--navy-950` | `#050B1F` | Fundo escuro principal |
| `--navy-900` | `#0A1638` | Cards escuros, cabeçalhos de planilha |
| `--navy-800` / `--navy-600` | `#102257` / `#1B3A8C` | Profundidade, degradês |
| `--electric` | `#2F6BFF` | Azul elétrico: palavra-chave, botões, pontos de destaque |
| `--electric-2` / `-3` | `#5B8CFF` / `#9DBBFF` | Ênfase sobre fundo escuro, reflexos de vidro |
| `--white` | `#FFFFFF` | Texto sobre escuro, fundo branco |
| `--paper` / `--paper-2` | `#F3F5F9` / `#E7EBF2` | Fundo do editorial clean |
| `--gray-500` / `--gray-700` | `#7D879A` / `#3A4356` | Texto secundário |

Fora da paleta: laranja, roxo e dourado. O vermelho aparece apenas como alerta funcional (por exemplo, margem abaixo de 5% na planilha).

## 2. Tipografia

| Papel | Fonte | Regra |
|---|---|---|
| Títulos | **Manrope 800** | Entrelinha 0,94–1,0 e espaçamento −0,035 a −0,045em. Título com no máximo 7 palavras na capa |
| Ênfase | **Instrument Serif Itálico** | Uma expressão por título, em azul elétrico. Dá o tom editorial e evita a cara de template |
| Rótulos, números, assinatura | **JetBrains Mono** | Caixa alta com espaçamento largo nos rótulos; números tabulares |

Tamanhos de referência em 1080 px: título de capa 92–118 px; título interno 68 px; texto 34 px; nada abaixo de 24 px no feed. A única exceção são os rótulos de gráfico (16–19 px), que não carregam a mensagem principal.

Licenças: as três fontes são do Google Fonts, sob a licença OFL, e podem ser usadas comercialmente. Os arquivos estão em `src/fonts/`.

## 3. Grade e assinatura

- **Feed 4:5 (1080 × 1350):** margem segura de 84 px. O título nunca encosta nas bordas.
- **Miniatura do perfil:** o Instagram mostra o post cortado em 3:4 (1080 × 1440 a partir do centro, no caso dos Reels). O título fica sempre dentro da faixa central.
- **Reels 9:16 (1080 × 1920):** o texto fica entre y = 470 e y = 1300. As áreas de baixo (legenda e botões) e da direita (ícones) ficam livres.
- **`@augustosilva.p`:** JetBrains Mono, 22 px, opacidade de 78%, no canto inferior esquerdo, em todas as peças. Sem nome, cargo nem "Executivo".
- **Paginação do carrossel:** `02 / 08`, no canto inferior direito. A capa leva "arraste →".

## 4. Componentes de vidro (Glassmorfismo A)

| Componente | Quando usar |
|---|---|
| `.glass` (escuro) | Painel translúcido com desfoque real (`backdrop-filter`), borda de 1 px, luz na aresta superior e reflexo azul elétrico nas bordas |
| `.glass.light` | O mesmo vidro em versão leitosa, para os fundos claros |
| Recibo de vidro | Lista de custos, preços e tarifas (sem gráfico) |
| Painel com gráfico | **Só** quando o tema é análise de números. Sempre com o selo "Simulação ilustrativa" |
| Caixa de dica | Bloco "Como levar para o preço" nos slides internos |
| Botão de palavra-chave | Bloco azul elétrico com a palavra em mono, usado só no último slide e na legenda |

Nos Reels, o desfoque é feito no próprio vídeo: o painel ganha uma máscara, o trecho embaixo dele é desfocado quadro a quadro, e o texto fica por cima, parado.

## 5. As quatro direções e a regra de alternância

| Direção | Fundo | Elemento principal | Quando usar |
|---|---|---|---|
| **A · Fotográfico editorial** | Foto ou filmagem real | Título forte integrado à imagem, poucos elementos de vidro | Taxas, operação, logística, rotina |
| **B · Editorial clean** | Branco ou `paper` | Tipografia grande, muito respiro, um elemento de vidro leitoso | Conceitos, listas, validação, erros |
| **C · Glass Dashboard** | Navy profundo com brilho elétrico | Cards de vidro com números ou gráfico | Margem, simulações, comparações financeiras |
| **D · Conceitual** | Escuro ou claro | Uma metáfora comercial (etiqueta, recibo, caixa) feita em vidro | Ideias abstratas (preço no escuro, desconto, markup) |

**Regras de alternância** (valem para cada bloco de 3 × 3 da grade):
1. Cada direção aparece no mínimo 2 e no máximo 3 vezes.
2. Duas capas vizinhas (lado a lado ou uma em cima da outra) nunca têm a mesma direção nem a mesma massa de cor (clara/escura).
3. Gráficos aparecem em no máximo 2 das 9 capas.
4. A posição do título varia: em cima, embaixo ou no meio, à esquerda ou centralizado. Nunca mais de duas capas seguidas com o título na mesma posição.
5. Os fundos não se repetem: cada foto ou filmagem é usada uma vez por semana.
6. Os Reels usam filmagem real em movimento contínuo. GIF, foto com zoom ou slide animado não são aceitos.

## 6. Linha editorial

**Pilares e peso semanal (21 publicações):**

| Pilar | Peso | Exemplos |
|---|---|---|
| Precificação e lucro | 6 | Custos ocultos, margem × markup, preço mínimo, taxas |
| Marketplace e operação | 5 | Frete, anúncio, rotina de pedidos, erros de iniciante, devoluções |
| IA aplicada | 5 | Validar produto, pesquisar demanda, prompts de atendimento |
| Estratégia comercial | 4 | Black Friday com margem protegida, checklist de campanha |
| Autoridade e educação | 1 | Pergunta de engajamento e conceitos de base |

**Formatos por dia:** 1 carrossel (manhã), 1 estático (almoço) e 1 Reel de 7 s (noite). Os horários 08h30, 12h30 e 19h30 são uma hipótese e **não foram validados** com as métricas da conta.

**Tom:** direto, técnico sem jargão, didático, sem promessas. Todo número de exemplo leva o aviso "hipotético" ou "simulação ilustrativa". Nenhum post comercial fala de fé ou ministério.

**Estrutura da legenda:** gancho (1 linha) → problema → ensino em lista → aviso de exemplo hipotético, quando houver números → CTA "Comente PALAVRA e eu te envio [material] no Direct" → de 5 a 6 hashtags.

**CTA:** nunca pedir "siga para receber" na arte nem na legenda. A verificação de seguidor acontece no Direct, e só se o Manychat oferecer esse recurso.

## 7. Checklist de qualidade (QA) de cada peça

- [ ] Dimensão exata (1080 × 1350 ou 1080 × 1920) e todos os slides prometidos.
- [ ] Título legível na miniatura (prévia de 3:4 a 360 px de largura).
- [ ] Português revisado. Nenhum número apresentado como resultado real.
- [ ] `@augustosilva.p` presente e discreto.
- [ ] A palavra-chave da arte, da legenda e do Manychat é a mesma, e é única.
- [ ] A recompensa existe, abre no celular e o conteúdo foi conferido.
- [ ] Reel: MP4 em H.264, 30 fps, 7 s, com o vídeo em movimento do início ao fim.
- [ ] Licença da imagem ou do vídeo registrada em `CREDITOS.md`.
