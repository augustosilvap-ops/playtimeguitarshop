# Playtime Guitar Shop — loja na Shopify

| Pasta / arquivo | O que é |
|---|---|
| `tema-playtime.zip` | Tema pronto para enviar à Shopify |
| `tema/` | Código do tema (o mesmo conteúdo do .zip) |
| `importacao/produtos-shopify.csv` | Os 185 produtos do site atual, com as 927 fotos |
| `importacao/gerar_csv.py` | Gera a planilha de novo a partir do site atual |
| `previa/` | Prévia navegável (cópia do artefato no claude.ai) |
| `previa/videos/` | Vídeos da Clínica e do Passaporte, para enviar à Shopify |

## Passo a passo na Shopify

1. **Importar os produtos** — *Produtos › Importar* › escolha `importacao/produtos-shopify.csv`.
   As fotos são baixadas direto de playtimeguitarshop.com, então o site atual precisa estar no ar durante a importação.
   Instrumentos em estoque entram com quantidade 1; confira o estoque de cordas, cabos e outros itens com mais de uma unidade.
2. **Enviar o tema** — *Loja virtual › Temas › Adicionar tema › Fazer upload de arquivo zip* › `tema-playtime.zip`.
3. **Criar as coleções automáticas** — *Produtos › Coleções › Criar coleção*, tipo "Automatizada", condição "Tag do produto é igual a":

   | Coleção | Identificador (handle) | Tag |
   |---|---|---|
   | Guitarras | `guitarras` | `guitarras` |
   | Violões | `violoes` | `violoes` |
   | Baixos | `baixos` | `baixos` |
   | Pedais e amps | `pedais` | `pedais-e-amps` |
   | Acessórios | `acessorios` | `acessorios` |
   | Garimpo | `garimpo` | `garimpo` |
   | Destaques | `destaques` | `destaques` |
   | Com passaporte | `passaporte` | `passaporte` |

   A tag `destaques` foi colocada nos 12 instrumentos mais caros em estoque. Troque à vontade.
4. **Criar as páginas** — *Loja virtual › Páginas*. Em cada uma, escolha o modelo indicado:

   | Página | Identificador | Modelo |
   |---|---|---|
   | Clínica Playtime | `clinica` | `page.clinica` |
   | Afinador online | `afinador` | `page.afinador` |
   | Troca | `troca` | `page.troca` |
   | Passaporte do Instrumento | `passaporte` | `page.passaporte` |

5. **Menus** — *Loja virtual › Navegação*:
   - `main-menu`: Início, Guitarras, Violões, Baixos, Pedais e amps, Garimpo, Clínica, Troca
   - `footer` (Loja): Guitarras, Violões, Baixos, Garimpo
   - `servicos` (Serviços): Clínica Playtime, Afinador online, Avalie sua troca, Passaporte do Instrumento
6. **Passaporte e áudio** — *Configurações › Dados personalizados › Produtos › Adicionar definição*, com namespace `custom`:

   | Nome | Chave | Tipo |
   |---|---|---|
   | Nº de série | `custom.passaporte_serie` | Texto de linha única |
   | Ano | `custom.passaporte_ano` | Texto de linha única |
   | Fabricação | `custom.passaporte_origem` | Texto de linha única |
   | Condição | `custom.passaporte_condicao` | Texto de linha única |
   | Peso desta peça | `custom.passaporte_peso` | Texto de linha única |
   | Altura das cordas | `custom.passaporte_altura_cordas` | Texto de linha única |
   | Trastes | `custom.passaporte_trastes` | Texto de linha única |
   | Encordoamento | `custom.passaporte_encordoamento` | Texto de linha única |
   | Regulagem | `custom.passaporte_regulagem` | Texto com várias linhas |
   | Áudio limpo | `custom.audio_limpo` | Arquivo |
   | Áudio com drive | `custom.audio_drive` | Arquivo |

   O quadro do Passaporte e o player "Ouça esta peça" só aparecem nos produtos que tiverem esses campos preenchidos.
   Para o selo dourado "Passaporte" aparecer no cartão do produto, adicione a tag `passaporte`.
7. **Vídeos** — *Conteúdo › Arquivos* › envie `previa/videos/passaporte-loop.mp4` e `clinica-loop.mp4`.
   No editor do tema, escolha cada vídeo na seção "Vídeo com lista" (página inicial, Clínica e Passaporte).
   Até lá, a seção mostra a imagem de capa.
8. **Conferir** — *Configurações do tema*: WhatsApp (já vem com 55 41 3501-4977), parcelas e desconto no Pix.
   No rodapé, confira o horário de atendimento.
