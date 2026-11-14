# Projetos do Augusto — base de trabalho

Antes de qualquer tarefa da marca RUAH, leia **ruah/LEIA_PRIMEIRO_RUAH.md** inteiro.
As regras da seção 1 ("Regras que não podem ser quebradas") valem sempre. Em resumo:
- Não alterar estampas; nunca escrever "nosso lema" nem "nascida na rua".
- Toda alteração precisa de prévia (celular + desktop) antes de ir ao ar.
- Temas da Shopify sempre sobem como NÃO publicados (`--unpublished`); nunca `--live`/`--allow-live`.
- O prazo de produção de 72h é interno e não aparece em lugar nenhum.
- Só usar as afirmações de produto aprovadas; qualquer afirmação nova precisa ser marcada para aprovação.
- Respostas da caixinha não são avaliações de compradores.
- Ações de escrita na Windsor (anúncios/Instagram) só depois de o Augusto confirmar a mudança específica.
- Português do Brasil, tom premium de grife.

## Estrutura
- `ruah/` — pacote da marca (logos, fontes, fotos de produto, conteúdo, vídeos, textos, scripts).
  - `ruah/scripts/` usa caminhos da sessão antiga; ajuste `SP` e os caminhos de fontes/logos antes de rodar.

## Outras frentes
- **Mercado Livre:** conta ativa com ~300 anúncios, só dropshipping, produtos variados. Fornecedor: B2Drop. Todos os anúncios em Premium (avaliar Clássico). Zero vendas até 13/11/2026; termômetro ainda não ativo; avaliando o programa Decola. Ainda sem acesso à API.
- **Canal infantil — Pequeninos do Reino:** briefing em `pequeninos/BRIEFING_MESTRE.txt` (original .docx ao lado). Universo Reino Feliz; Davi e Rafaella co-protagonistas; Theo (leão, sempre 4 patas) e Jasmin (cordeirinha). YouTube/TikTok @pequeninosdoreinoofc. EP01 não aprovado. Arquivos no Google Drive (pasta compartilhada pelo Augusto).

## Nexus (pasta `nexus/`)
- Central de comando: `nexus/index.html`, publicada em https://claude.ai/artifact/6SYuGnMN62uD1UMRiFaZrm (republique o mesmo arquivo para manter o link).
- Dados ao vivo pela capacidade `mcp` (Shopify list-orders; Windsor_ai get_data para Meta Ads e Instagram @ruahwear_ 17841452465952355 e @augustosilva.p 17841407424879500). Chat via `sample`, voz via `tts`/`dictation`, execução via Claude Code Remote `create_session`.
- Banco do artifact: `estado/tarefas` (tarefas por projeto: ruah, aug, ml, pq) e `briefing/hoje` (gravado todo dia às 6h38 pela tarefa agendada "Nexus briefing diário").

## Nexus site próprio (sem login no Claude)
- https://nexusautomatic.vercel.app · Vercel publica a branch `main` · código em `nexus-site/` (front em `public/`, funções em `api/` reexportadas na raiz `api/`).
- Login por senha (`NEXUS_PASSWORD`, token HMAC com `NEXUS_SECRET`). Dados: `/api/shopify` (SHOPIFY_STORE/SHOPIFY_TOKEN), `/api/windsor` (WINDSOR_API_KEY), `/api/state` (Upstash Redis). `public/shim.js` emula `window.claude.use` para reaproveitar o Nexus.
- Versão celular (≤760px) no próprio `nexus/index.html`: cabeçalho compacto, abas fixas embaixo (Início, Conteúdo, Negócios, Agenda, Tendências…), cérebro como banner só no Início, microfone flutuante. Conteúdo separado por página do Instagram (abas @augustosilva.p e @ruahwear_; posts da RUAH têm `marca:"ruah"`).
- Sem chat (exige créditos da API da Anthropic). Ao mudar `nexus/index.html`, regenere `nexus-site/public/index.html`.

## Instagram pessoal @augustosilva.p (pasta `augusto/`)
- Documento mestre: `augusto/sistema/BRIEFING_MESTRE.md`. Regras de produção: `augusto/sistema/SISTEMA_VISUAL_E_EDITORIAL.md`. Leia os dois antes de qualquer peça.
- Foco: marketplace, e-commerce, gestão e IA. **Sem fé/ministério nas peças comerciais.** Não recriar o rosto do Augusto. Assinatura apenas `@augustosilva.p`.
- Paleta navy/azul elétrico/branco/preto; Glassmorfismo A alternando 4 direções (foto, clean, glass dashboard, conceitual). Gráfico só quando há análise; números sempre marcados como hipotéticos.
- CTA: "Comente PALAVRA e eu te envio X no Direct" — nunca "siga para receber". Palavra-chave única por post (`augusto/editorial/calendario.py` valida).
- Reels: MESCLAR 3 formatos — (1) motion gráfico "Smooth" (APROVADO 14/11, ~7,5 s, ritmo rápido), (2) motion sobre vídeo real (reel_story.py), (3) vídeos gravados pelo Augusto (estúdio em preparação). Narração automática: Kokoro REPROVADO (robótico, 14/11) — aguardando escolha de voz premium (ElevenLabs ou Azure). Ferramentas existentes — `augusto/src/voz/narrar.py` e `augusto/src/motion/narrar_reel.py` (fala por cena → tempos das cenas → render sincronizado). Instalar: `pip install kokoro-onnx soundfile`; baixar `onnx/model_quantized.onnx` → /home/user/kokoro/model.onnx e `voices/pm_alex.bin`, `pf_dora.bin`, `pm_santa.bin` de huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX. CTA final do Reel: pílula grande "Leia a legenda ↓" + "Comente PALAVRA e receba no Direct".
- Formato "Cinético" APROVADO 14/11 ("vamos seguir esse padrão"): tipografia em tela cheia no ritmo da fala, cortes rápidos navy/branco/azul, elementos animados (vidro estilhaçando, preço caindo, margem subindo, notificações, gráficos), CTA "Leia a legenda ↓". `augusto/src/motion/cinetico_planilha.html`. Referências enviadas pelo Augusto são INSPIRAÇÃO — nunca copiar cenário, efeitos ou layout.
- Carrossel v4 APROVADO 14/11 (substitui o v2): fundo SÓLIDO (claro #F1F3F8 ou navy #08090E com brilho azul sutil) + letras gigantes com pesos misturados (Inter 800/400 + Anton) + bloco azul na palavra-chave + no máx. 1 elemento de apoio (ícone 3D, mockup de celular/planilha/PDF ou etiquetas de preço); miolo limpo em passo a passo com anotações; último slide CTA + presente com faixa "Comente PALAVRA". Base: `augusto/src/pecas/v4_final.html`. Capas com DESTAQUE APROVADAS 14/11 ("é isso!"): 1 elemento herói grande ocupando ~45% da arte (celular com chat, número gigante, caixas 3D) e contraste forte — ver `augusto/src/pecas/v4_destaque.html`. REPROVADO: foto de fundo nas capas e pessoa recortada com quadros de vídeo de banco. Ícones genéricos (sem logos de marcas).
- Motion "Smooth" — interface em vidro, ícone em mostrador animado, número que conta, texto palavra por palavra, câmera que aproxima. Protótipo: `augusto/src/motion/smooth_planilha.html` + `render_motion.js`. Se aprovado, substitui o modelo antigo abaixo.
- Reels (modelo antigo): filmagem real (Mixkit Free License, conferir licença por vídeo), 1080×1920, 30 fps, 10 s, roteiro em 4 cenas (gancho → dor → agravamento → solução + "Leia a legenda"), gerado por `augusto/src/reel_story.py`. Nada de GIF ou foto com zoom.
- Carrosséis: usar o v4 aprovado (acima). Testes v3/editorial e capas com foto de fundo foram REJEITADOS em 14/11.
- Storytelling: `storytelling/RUAH_storytelling.md` e `storytelling/AUGUSTO_storytelling.md`.
- Manychat: configurado pelo Augusto em 14/11 (links em `augusto/editorial/MANYCHAT_LINKS.md`). Agendamento: NÃO configurado. Nunca marcar como publicado/agendado sem confirmação.

## Skills de vídeo instaladas (14/11/2026)
- `remotion:*` (vídeos em código), `video-shotcraft` (vídeo de produto cinematográfico), `watch-video` (analisar vídeos: quadros + transcrição). Usar nos Reels do @augustosilva.p, anúncios da RUAH e revisão do EP01 do Pequeninos.
