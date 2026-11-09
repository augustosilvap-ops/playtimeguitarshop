# Playtime Guitar Shop — loja na Shopify

| Pasta / arquivo | O que é |
|---|---|
| `tema-playtime.zip` | Tema pronto para enviar à Shopify |
| `tema/` | Código do tema (o mesmo conteúdo do .zip) |
| `importacao/produtos-shopify.csv` | Os 185 produtos do site atual, com as 927 fotos |
| `importacao/gerar_csv.py` | Gera a planilha de novo a partir do site atual |
| `importacao/criar_metacampos.py` | Cria na Shopify, pela API, todos os campos de produto que o tema usa |
| `previa/` | Prévia navegável (cópia do artefato no claude.ai) |
| `previa/videos/` | Vídeos da Clínica e do Passaporte, para enviar à Shopify |

## Passo a passo na Shopify

1. **Criar os campos de produto (antes de importar)**: o jeito rápido é o script `importacao/criar_metacampos.py`, que cria os 34 campos de uma vez pela API (instruções no topo do arquivo). Se preferir fazer à mão, veja o passo 6 e crie as definições de *Ficha técnica* e *Procedência*. A planilha já preenche a ficha técnica de 151 produtos, lida das descrições do site atual, mas a Shopify só aceita essas colunas se os campos já existirem.
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
   | Compra segura | `compra-segura` | `page.compra-segura` |
   | Consultoria por vídeo | `consultoria` | `page.consultoria` |
   | Comparar | `comparar` | `page.comparar` |

5. **Menus** — *Loja virtual › Navegação*:
   - `main-menu`: Início, Guitarras, Violões, Baixos, Pedais e amps, Garimpo, Clínica, Troca
   - `footer` (Loja): Guitarras, Violões, Baixos, Garimpo
   - `servicos` (Serviços): Clínica Playtime, Afinador online, Avalie sua troca, Passaporte do Instrumento, Consultoria por vídeo, Compra segura
6. **Passaporte e áudio** — crie as definições de metacampo de **Produtos**, todas com namespace `custom`.
   O nome do menu muda conforme a versão do painel: procure em *Configurações* por **Metacampos e metaobjetos** (ou **Dados personalizados**) › **Produtos** › **Adicionar definição**.
   Atalho que não depende do menu: abra qualquer produto, role até o quadro **Metacampos** no fim da página e clique em **Gerenciar** (ou ⋯ › **Gerenciar definições**).
   Ou cole na barra do navegador: `https://admin.shopify.com/store/SUA-LOJA/settings/custom_data/product/metafields` (troque SUA-LOJA pelo nome da loja que aparece no endereço do painel).

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

   | Regulado por | `custom.regulagem_tecnico` | Texto de linha única |
   | Data da regulagem | `custom.regulagem_data` | Data |

   **Procedência**

   | Nome | Chave | Tipo |
   |---|---|---|
   | Foto do número de série | `custom.serial_foto` | Arquivo (imagem) |
   | Link de conferência do fabricante | `custom.serial_link` | URL |
   | Nota fiscal | `custom.nota_fiscal` | Texto de linha única (ex.: "Acompanha nota fiscal") |
   | Garantia | `custom.garantia` | Texto de linha única (ex.: "1 ano pela Playtime") |
   | Histórico | `custom.historico` | Texto com várias linhas |

   O número exibido é o mesmo de `custom.passaporte_serie`. Em *Configurações do tema › Procedência* dá para cadastrar uma vez a página oficial de cada marca (`Marca | link`), e ela vale para todos os produtos daquela marca.
   Use só páginas do próprio fabricante. Não consegui confirmar daqui quais marcas têm consulta oficial: a Fender costuma indicar a sua, mas confira no site dela antes de cadastrar.

   **Ficha técnica** (todos *Texto de linha única*): `custom.escala`, `custom.nut_largura`, `custom.raio`, `custom.braco_perfil`, `custom.braco_espessura_1`, `custom.braco_espessura_12`, `custom.braco_madeira`, `custom.escala_madeira`, `custom.trastes`, `custom.corpo`, `custom.tampo`, `custom.captadores`, `custom.eletrica`, `custom.ponte`, `custom.tarraxas`, `custom.acabamento`.
   As espessuras do braço (1ª e 12ª casa, em mm, ex.: `20,6`) ativam o "Compare o braço com o do seu instrumento". A planilha não traz essas medidas: a oficina mede com paquímetro.

   O quadro do Passaporte, a Procedência, a Ficha técnica e o player "Ouça esta peça" só aparecem nos produtos que tiverem esses campos preenchidos.
   Para o selo dourado "Passaporte" aparecer no cartão do produto, adicione a tag `passaporte`.
7. **Vídeos** — *Conteúdo › Arquivos* › envie `previa/videos/passaporte-loop.mp4` e `clinica-loop.mp4`.
   No editor do tema, escolha cada vídeo na seção "Vídeo com lista" (página inicial, Clínica e Passaporte).
   Até lá, a seção mostra a imagem de capa.
8. **Logos das marcas** — no editor do tema, seção "Logos das marcas": em cada marca, envie o logo oficial (PNG ou SVG com fundo transparente; os distribuidores costumam fornecer). Sem logo, a seção mostra o nome da marca.
9. **Conferir** — *Configurações do tema*: WhatsApp (já vem com 55 41 3501-4977), parcelas e desconto no Pix.
   No rodapé, confira o horário de atendimento.

## Recursos da página do produto

- **Regulagem do seu jeito**: o cliente escolhe cordas, afinação e altura das cordas, sem custo. As escolhas aparecem no pedido (*Pedidos › detalhes do item*), para a oficina. Só aparece em guitarras, violões e baixos (pelo *Tipo* do produto).
- **Frete pelo CEP**: usa as tarifas reais configuradas em *Configurações › Frete e entrega*. A cidade vem do ViaCEP. Para calcular, a Shopify precisa da peça no carrinho: se ela ainda não estiver lá, o tema coloca e tira em seguida, sem o cliente perceber.
- **Comparar**: até 3 peças lado a lado na página `/pages/comparar`, com as diferenças destacadas.
- **Consultoria por vídeo** (`/pages/consultoria`): o formulário abre o WhatsApp com a mensagem pronta. Nada fica salvo no site.
