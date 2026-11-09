"""Catálogo único dos campos de ficha técnica (metacampos custom.* de produto).

Usado para gerar: a planilha da Shopify, as definições de metacampo (GraphQL) e a lista
que o tema exibe (tema/snippets/spec-fields.liquid). Mudou aqui, rode `python3 enriquecer.py --tema`.
"""

# (chave, rótulo na loja, tipo de metacampo)
T, TL = "single_line_text_field", "multi_line_text_field"
FICHA = [
    # identificação
    ("modelo", "Modelo", T),
    ("serie", "Série / linha", T),
    ("fabricacao", "Fabricação", T),
    # instrumentos
    ("construcao", "Construção", T),
    ("formato_corpo", "Formato do corpo", T),
    ("corpo", "Corpo", T),
    ("tampo", "Tampo", T),
    ("braco_madeira", "Braço", T),
    ("braco_perfil", "Perfil do braço", T),
    ("braco_espessura_1", "Espessura do braço na 1ª casa", T),
    ("braco_espessura_12", "Espessura do braço na 12ª casa", T),
    ("escala_madeira", "Madeira da escala", T),
    ("escala", "Escala (comprimento)", T),
    ("raio", "Raio da escala", T),
    ("trastes", "Trastes", T),
    ("nut_material", "Nut", T),
    ("nut_largura", "Largura do nut", T),
    ("marcadores", "Marcadores", T),
    ("captadores", "Captadores", T),
    ("eletrica", "Elétrica", T),
    ("ponte", "Ponte", T),
    ("tarraxas", "Tarraxas", T),
    ("hardware", "Hardware", T),
    ("acabamento", "Acabamento", T),
    ("cor", "Cor", T),
    ("cordas_qtd", "Número de cordas", T),
    ("mao", "Mão", T),
    ("cordas_fabrica", "Cordas de fábrica", T),
    # pedais
    ("tipo_efeito", "Tipo de efeito", T),
    ("chaves", "Chaves e modos", T),
    ("alimentacao", "Alimentação", T),
    ("consumo_ma", "Consumo", T),
    ("bypass", "Bypass", T),
    # amplificadores
    ("tipo_amp", "Tipo", T),
    ("formato", "Formato", T),
    ("potencia", "Potência", T),
    ("alto_falantes", "Alto-falantes", T),
    ("valvulas", "Válvulas", T),
    ("canais", "Canais", T),
    ("efeitos", "Efeitos", T),
    ("impedancia", "Impedância", T),
    # comuns
    ("controles", "Controles", T),
    ("conexoes", "Conexões", T),
    ("material", "Material", T),
    ("compatibilidade", "Compatibilidade", T),
    ("dimensoes", "Dimensões", T),
    ("peso_produto", "Peso do produto", T),
    ("acessorios", "Acompanha", TL),
]
CHAVES = [k for k, _, _ in FICHA]
ROTULO = {k: r for k, r, _ in FICHA}
TIPO = {k: t for k, _, t in FICHA}
