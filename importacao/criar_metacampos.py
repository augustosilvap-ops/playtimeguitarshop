"""Cria na Shopify todos os campos de produto (metacampos custom.*) que o tema Playtime usa.

Rode UMA vez, antes de importar a planilha. Pode rodar de novo sem problema: campos que já
existem são pulados.

Uso com o app do Dev Dashboard (Client ID e Client secret):
    SHOPIFY_LOJA=minha-loja SHOPIFY_CLIENT_ID=... SHOPIFY_CLIENT_SECRET=... python3 criar_metacampos.py

Uso com um token pronto (shpat_...), se você já tiver um:
    SHOPIFY_LOJA=minha-loja SHOPIFY_TOKEN=shpat_... python3 criar_metacampos.py

Só para ver a lista, sem enviar nada:
    python3 criar_metacampos.py --teste

SHOPIFY_LOJA é o nome que aparece em minha-loja.myshopify.com.
O app precisa das permissões read_products e write_products e estar instalado na loja.
"""
import json
import os
import sys
import urllib.error
import urllib.request

API = "2026-10"
TEXTO, TEXTO_LONGO = "single_line_text_field", "multi_line_text_field"

# (chave, nome no painel, tipo, descrição)
CAMPOS = [
    # Passaporte do Instrumento
    ("passaporte_serie", "Passaporte · Nº de série", TEXTO, "Número de série desta unidade. Também aparece na Procedência."),
    ("passaporte_ano", "Passaporte · Ano", TEXTO, "Ano de fabricação. Ex.: 1998"),
    ("passaporte_origem", "Passaporte · Fabricação", TEXTO, "País ou fábrica. Ex.: EUA, Japão (Fujigen)"),
    ("passaporte_condicao", "Passaporte · Condição", TEXTO, "Ex.: Original, ótimo estado"),
    ("passaporte_peso", "Passaporte · Peso desta peça", TEXTO, "Peso na balança. Ex.: 3,62 kg"),
    ("passaporte_altura_cordas", "Passaporte · Altura das cordas (12ª casa)", TEXTO, "Grave / aguda. Ex.: 1,6 / 1,4 mm"),
    ("passaporte_trastes", "Passaporte · Trastes", TEXTO, "Estado dos trastes. Ex.: 90%, sem desgaste"),
    ("passaporte_encordoamento", "Passaporte · Encordoamento", TEXTO, "Ex.: .010–.046"),
    ("passaporte_regulagem", "Passaporte · Regulagem", TEXTO_LONGO, "O que a oficina ajustou."),
    ("regulagem_tecnico", "Passaporte · Regulado por", TEXTO, "Nome do técnico que assinou a ficha."),
    ("regulagem_data", "Passaporte · Data da regulagem", "date", ""),
    ("audio_limpo", "Áudio · Som limpo", "file_reference", "Arquivo de áudio (MP3) gravado com esta peça."),
    ("audio_drive", "Áudio · Com drive", "file_reference", "Arquivo de áudio (MP3) gravado com esta peça."),
    # Procedência
    ("serial_foto", "Procedência · Foto do número de série", "file_reference", "Foto nítida do número de série desta peça."),
    ("serial_link", "Procedência · Link de conferência do fabricante", "url", "Página oficial do fabricante para conferir o número."),
    ("nota_fiscal", "Procedência · Nota fiscal", TEXTO, "Ex.: Acompanha nota fiscal"),
    ("garantia", "Procedência · Garantia", TEXTO, "Ex.: 1 ano pela Playtime"),
    ("historico", "Procedência · Histórico", TEXTO_LONGO, "Para usados: dono anterior, peças trocadas, revisões."),
    # Ficha técnica
    ("escala", "Ficha · Escala (comprimento)", TEXTO, "Ex.: 25.5″ (648 mm)"),
    ("nut_largura", "Ficha · Largura do nut", TEXTO, "Em mm. Ex.: 43"),
    ("raio", "Ficha · Raio da escala", TEXTO, "Ex.: 430 mm / 16.9″"),
    ("braco_perfil", "Ficha · Perfil do braço", TEXTO, "Ex.: Modern C, Wizard, AZ Oval C"),
    ("braco_espessura_1", "Ficha · Espessura do braço na 1ª casa", TEXTO, "Só o número, em mm. Ex.: 20,6"),
    ("braco_espessura_12", "Ficha · Espessura do braço na 12ª casa", TEXTO, "Só o número, em mm. Ex.: 22,4"),
    ("braco_madeira", "Ficha · Braço", TEXTO, "Madeira e construção do braço."),
    ("escala_madeira", "Ficha · Madeira da escala", TEXTO, "Ex.: Rosewood, Ébano, Maple"),
    ("trastes", "Ficha · Trastes", TEXTO, "Quantidade e tipo. Ex.: 22 Jumbo em aço inoxidável"),
    ("corpo", "Ficha · Corpo", TEXTO, ""),
    ("tampo", "Ficha · Tampo", TEXTO, ""),
    ("captadores", "Ficha · Captadores", TEXTO, ""),
    ("eletrica", "Ficha · Elétrica", TEXTO, "Controles e chaves."),
    ("ponte", "Ficha · Ponte", TEXTO, ""),
    ("tarraxas", "Ficha · Tarraxas", TEXTO, ""),
    ("acabamento", "Ficha · Acabamento", TEXTO, ""),
]
SO_IMAGEM = {"serial_foto"}
SO_ARQUIVO = {"audio_limpo", "audio_drive"}

MUTATION = """
mutation criar($d: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $d) {
    createdDefinition { id namespace key }
    userErrors { field message code }
  }
}"""


def definicao(chave, nome, tipo, descricao):
    d = {"name": nome, "namespace": "custom", "key": chave, "type": tipo, "ownerType": "PRODUCT"}
    if descricao:
        d["description"] = descricao
    if chave in SO_IMAGEM:
        d["validations"] = [{"name": "file_type_options", "value": json.dumps(["Image"])}]
    elif chave in SO_ARQUIVO:
        d["validations"] = [{"name": "file_type_options", "value": json.dumps(["File"])}]
    return d


def post(url, corpo, headers):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Accept": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Erro {e.code} da Shopify: {e.read().decode(errors='replace')[:500]}")


def obter_token(loja):
    token = os.environ.get("SHOPIFY_TOKEN")
    if token:
        return token
    cid, secret = os.environ.get("SHOPIFY_CLIENT_ID"), os.environ.get("SHOPIFY_CLIENT_SECRET")
    if not (cid and secret):
        raise SystemExit("Informe SHOPIFY_CLIENT_ID e SHOPIFY_CLIENT_SECRET (ou SHOPIFY_TOKEN). Veja as instruções no topo do arquivo.")
    r = post(f"https://{loja}.myshopify.com/admin/oauth/access_token",
             {"client_id": cid, "client_secret": secret, "grant_type": "client_credentials"}, {})
    if "access_token" not in r:
        raise SystemExit(f"A Shopify não devolveu o token: {r}")
    return r["access_token"]


def main():
    defs = [definicao(*c) for c in CAMPOS]
    if "--teste" in sys.argv:
        for d in defs:
            print(f'custom.{d["key"]:<26} {d["type"]:<24} {d["name"]}')
        print(f"\n{len(defs)} campos. Nada foi enviado (modo --teste).")
        return
    loja = (os.environ.get("SHOPIFY_LOJA") or "").replace(".myshopify.com", "").strip()
    if not loja:
        raise SystemExit("Informe SHOPIFY_LOJA (o nome em minha-loja.myshopify.com).")
    token = obter_token(loja)
    url = f"https://{loja}.myshopify.com/admin/api/{API}/graphql.json"
    criados = existentes = 0
    falhas = []
    for d in defs:
        r = post(url, {"query": MUTATION, "variables": {"d": d}}, {"X-Shopify-Access-Token": token})
        if r.get("errors"):
            raise SystemExit(f"Erro da API: {r['errors']}")
        res = r["data"]["metafieldDefinitionCreate"]
        erros = res["userErrors"]
        if res["createdDefinition"]:
            criados += 1
            print(f"  criado    custom.{d['key']}")
        elif any(e.get("code") == "TAKEN" for e in erros):
            existentes += 1
            print(f"  já existe custom.{d['key']}")
        else:
            falhas.append((d["key"], erros))
            print(f"  ERRO      custom.{d['key']}: {'; '.join(e['message'] for e in erros)}")
    print(f"\n{criados} criados, {existentes} já existiam, {len(falhas)} com erro.")
    if falhas:
        sys.exit(1)
    print("Pronto. Agora importe a planilha produtos-shopify.csv.")


if __name__ == "__main__":
    main()
