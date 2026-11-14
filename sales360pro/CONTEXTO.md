# Sales360Pro — contexto do projeto

> Recebido do Augusto em 14/11/2026 (resumo de outro chat). Os arquivos do CRM e da landing page **não estão neste repositório**: ficam em `/mnt/user-data/outputs/` do outro ambiente. Peça ao Augusto para enviar o zip quando for mexer no código.

## Quem e o que
- Augusto, Gerente de Pós-Venda na Evolua (Curitiba). Comunicação direta; quer ferramentas executáveis. **Revisar a estrutura inteira antes de dizer "corrigi"**.
- **Sales360Pro**: CRM de WhatsApp. Meta: vender como **SaaS com mensalidade (não white-label)**, para vários segmentos (não só operadoras).

## Stack e endereços
- Frontend: Vite JS (`crm-atendimento/`: `src/main.js` ~4700 linhas, `src/style.css`, `src/logo.js`, `favicon.svg`, `logo.svg`) → `crm-atendimento.zip` para o Netlify.
- Landing page final: `landing-page-v2/index.html` (v1 rejeitada). Formulário de teste posta no webhook `lp-lead-demo`. Planos: Essencial R$ 197, Operação R$ 397, Escala sob consulta.
- Backend: Supabase (projeto `crexvdhogmvjabomubex`, RLS, função `is_admin()`).
- Automação: n8n em https://n8n.sales360pro.com (VPS Hostinger, docker compose em `/opt/atendimento-whatsapp`).
- WhatsApp: Evolution API em https://evolution.sales360pro.com (não oficial/Baileys). Nginx Proxy Manager na frente (encaminha para `evolution-api:8080`, websockets ligado).
- Cobrança: Asaas. IA: Anthropic API, só texto (sem ElevenLabs).
- Visual do CRM: Space Grotesk + Inter, gradiente esmeralda→azul (`#14b98a` → `#4f86f5`), tokens em `style.css`. **Não mexer na sidebar nem nas cores.**

## Arquitetura
- Multi-tenant em fases. Fase 1 pronta (`empresas`, `asaas_eventos`). **Fase 2 (isolar tabelas por empresa) não iniciada.**
- Até lá: uma instância por cliente; `configuracoes.plano_ativo` controla limites (`window._planoAtivo`), marca branca via `window._marcaBranca`, bloqueio por assinatura em `configuracoes.assinatura`.
- Limites já informados: conta demo isolada automática e liberação automática de recursos por plano dependem da Fase 2. O webhook do Asaas atualiza o status e reconhece o plano pelo valor, mas os recursos ainda são aplicados por instância. O "Painel do dono" é controle comercial manual.

## Já construído
Funil Kanban, painel do contato, comentários internos com menções, fila priorizada por valor, alerta de vencimento, análise de sentimento, roteamento por especialidade, SLA, widget, relatórios; campanhas com variações de áudio e ritmo; importação de planilha com detecção de coluna de telefone (aviso se >15% inválidos); menu recolhível, login redesenhado, tour guiado, aba Treinamentos (Metas, Tarefas e Modelos removidas); chatbot de IA (texto), upload de documentos para a IA, modelos por operadora, leads de demonstração, clientes comerciais, backup, primeira tela de acesso, tela de assinatura suspensa, verificação de plano ao criar agente/número; **modo monitoramento** (`whatsapp_sessions.modo`); prévia navegável `previa.html`.

## Workflows n8n
| Workflow | ID |
|---|---|
| Inbound | `pq31KdMVQZiJESE1` |
| Disparo de Campanha | `7txdpEu4MpYUHHe5` |
| Atribuição | `ARTCf13jKVy9KTYp` |
| Gerenciar Sessão | `LIrayn4CsHtatDKc` |
| Maturador de Grupo | `7dpItjxCIIK8uSfI` |
| Maturador par fixo | `vAj4bA0bWyHT1Yn0` |
| Agente IA | `ya7k8h1vm8E0GKFN` |
| IA Assistente | `E5uADGyqawbfyXEm` |
| Processar Documento IA | `mSWSdnTeuEoToahY` |
| Alerta Vencimento | `6SNrnda6P5s7a25d` |
| Backup | `uHP7yXSsN1A0RRZ1` |
| Asaas eventos | `YMuo6dMRCOJbsCl7` |
| Asaas criar assinatura | `iWSp0ISqLAnOkMpv` |
| LP lead | `YfF1ygIDsxDDRUWi` |
| TEMP (pode apagar) | `S9ARdY1IDgvOQks4` |

## Supabase — tabelas adicionadas
`pipeline_etapas`, `comentarios_internos`, `agente_ia_documentos`, `modelos_operadora`, `meus_clientes_comerciais`, `empresas`, `asaas_eventos`, `backups_historico`, `leads_demo`, `planos_catalogo`, `numero_maturacao_conversas_ativas`. Colunas novas em conversations, contacts, agents, campaigns, campaign_variants, notificacoes, `whatsapp_sessions.modo`, `numero_maturacao_grupos.travado_ate`.

## Maturador de grupo
- Turnos alternados (tabela `numero_maturacao_conversas_ativas`: `proximo_remetente_id`, `proximo_turno_em`, `total_turnos` 4–8), rajadas de 1–2 mensagens, ~78 frases por fase (abertura/meio/despedida), cron a cada 45 s.
- Um número não pode estar em par fixo e em grupo ao mesmo tempo.
- Armadilhas do n8n: `$json` é sobrescrito após nós HTTP (usar nó âncora nomeado); nó com N itens roda N vezes (colapsar com Code); nós após saída vazia não rodam (`alwaysOutputData`); crons sobrepostos precisam de trava (`travado_ate`).
- Testado ao vivo: turno 0→1 e alternância corretos. Grupo reativado.

## Pendências
1. Confirmar que a VPS foi regularizada e que o n8n voltou (timeout na última sessão).
2. Modo monitoramento no n8n: o inbound `pq31KdMVQZiJESE1` não deve enfileirar conversas de sessões com `modo='monitoramento'`.
3. Confirmar o maturador com os números da Nicolle reconectados (estavam FAILED).
4. Confirmar que respostas de campanha chegam em Conversas (webhook da Evolution faltava nas instâncias novas).
5. Subir o `crm-atendimento.zip` mais recente no Netlify e hospedar a `landing-page-v2`.
6. Evolution: v2.1.1 ligando/desligando em loop na instância "WhatsappAugusto"; certificado do NPM falhou com "Evolution" como domínio (usar `evolution.sales360pro.com`).
7. Opcional: trava no CRM contra número em par fixo e grupo; Fase 2 multi-tenant; gravação de tela real na LP; apagar o workflow TEMP.

## Segurança (prioridade)
- Chaves reais (Asaas produção, Anthropic, Evolution global) foram coladas em chat e estão escritas nos nós HTTP do n8n. **Rotacionar todas e mover para credenciais do n8n.** Nunca pedir chaves no chat; usar o formulário seguro de credenciais ou as credenciais do n8n.

## Erros que não podem se repetir
- Mexer em layout e quebrar tela (login, widget removido sem querer): revisar o resultado inteiro.
- Campanha "concluída" na hora com 1094 falhas: coluna de telefone mal detectada.
- Evolution sem webhook em instância nova: configurar e conferir a URL (espaço no nome = `%20`).
