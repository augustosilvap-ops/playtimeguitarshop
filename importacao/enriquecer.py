"""Junta o CSV de estoque do WooCommerce com a pesquisa de especificações e gera:

  saida/produtos-shopify-enriquecido.csv   planilha para importar (ou atualizar) na Shopify
  saida/woocommerce-enriquecido.csv        o mesmo estoque no formato do WooCommerce, com ficha e dimensões
  saida/revisao-enriquecimento.xlsx        para a equipe revisar: confiança, correções, o que conferir e fontes
  criar_metacampos_novos.graphql           os campos de ficha que ainda não existem na loja

Uso:
  python3 enriquecer.py ESTOQUE.csv PASTA_DOS_RESULTADOS
  python3 enriquecer.py --tema            (só atualiza a lista de campos do tema)
"""
import csv
import html
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI))
from campos import CHAVES, FICHA, ROTULO, TIPO  # noqa: E402
from specs import extrair  # noqa: E402

SAIDA = AQUI / "saida"
TEMA = AQUI.parent / "tema"
JA_CRIADOS = {"escala", "nut_largura", "raio", "braco_perfil", "braco_espessura_1", "braco_espessura_12", "braco_madeira",
              "escala_madeira", "trastes", "corpo", "tampo", "captadores", "eletrica", "ponte", "tarraxas", "acabamento"}

TIPOS = [("Guitarras", "Guitarras"), ("Violões", "Violões"), ("Baixos", "Baixos"), ("Amplificadores", "Amplificadores"),
         ("Pedaleira", "Pedais"), ("Pedais", "Pedais"), ("Case", "Cases e bags"), ("Acessórios", "Acessórios")]
INSTRUMENTOS = {"Guitarras", "Violões", "Baixos"}


def slug(s):
    s = unicodedata.normalize("NFKD", html.unescape(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def limpar(v):
    v = re.sub(r"\s+", " ", str(v or "")).strip()
    return v[:250]


def preco(v):
    v = (v or "0").strip().replace(".", "").replace(",", ".")
    return float(v or 0)


def carregar_resultados(pasta):
    res = {}
    for f in sorted(Path(pasta).glob("resultado_*.json")):
        for r in json.load(open(f, encoding="utf-8")):
            res[int(r["id"])] = r
    return res


def tema():
    linhas = [f"{k}|{ROTULO[k]}" for k in CHAVES] + ["passaporte_peso|Peso desta peça"]
    txt = ("{%- comment -%}\n  Lista única dos campos da ficha técnica: chave do metafield (custom.*) e rótulo.\n"
           "  Gerada por importacao/enriquecer.py --tema a partir de importacao/campos.py.\n{%- endcomment -%}\n"
           "{%- capture spec_fields -%}\n" + "\n".join(linhas) + "\n{%- endcapture -%}\n{{- spec_fields | strip -}}\n")
    (TEMA / "snippets" / "spec-fields.liquid").write_text(txt, encoding="utf-8")
    print(f"tema: {len(linhas)} campos na ficha")


def graphql_novos():
    partes = []
    for i, (k, rot, tipo) in enumerate([f for f in FICHA if f[0] not in JA_CRIADOS], 1):
        d = (f'{{name: {json.dumps("Ficha · " + rot, ensure_ascii=False)}, namespace: "custom", key: "{k}", '
             f'type: "{tipo}", ownerType: PRODUCT}}')
        partes.append(f"  n{i:02d}_{k}: metafieldDefinitionCreate(definition: {d}) {{\n"
                      f"    createdDefinition {{ key }}\n    userErrors {{ code message }}\n  }}")
    q = ("# Campos novos da ficha técnica. Cole no app GraphiQL da Shopify e execute (▶).\n"
         "# Pode rodar de novo: os que já existem voltam com o código TAKEN.\n"
         "mutation CamposFichaNovos {\n" + "\n".join(partes) + "\n}\n")
    (AQUI / "criar_metacampos_novos.graphql").write_text(q, encoding="utf-8")
    return len(partes)


def main():
    if "--tema" in sys.argv:
        tema()
        return
    estoque, pasta = sys.argv[1], sys.argv[2]
    linhas = list(csv.DictReader(open(estoque, encoding="utf-8-sig")))
    cab = list(linhas[0].keys())
    res = carregar_resultados(pasta)
    handles = json.load(open(AQUI / "handles.json"))
    SAIDA.mkdir(exist_ok=True)

    produtos = []
    for r in linhas:
        pid = int(r["ID"])
        cats = [c.split(">")[-1].strip() for c in r["Categorias"].split(",") if c.strip()]
        tipo = next((t for c, t in TIPOS if c in cats), "Acessórios")
        desc = r["Descrição"].replace("\\n", "\n")
        e = res.get(pid, {})
        base = extrair(desc)
        campos = {k: limpar(v) for k, v in {**base, **(e.get("campos") or {})}.items() if k in CHAVES and limpar(v)}
        for k in ("braco_espessura_1", "braco_espessura_12"):
            if k in campos:
                m = re.search(r"\d+(?:[.,]\d+)?", campos[k])
                campos[k] = m.group(0).replace(".", ",") if m else campos.pop(k)
        tags = {slug(t) for t in r["Tags"].split(",") if t.strip()}
        tags |= {slug(c) for c in cats} | {slug(tipo)}
        tags |= {slug(t) for t in (e.get("tags") or []) if t}
        if tipo in ("Pedais", "Amplificadores"):
            tags.add("pedais-e-amps")
        if "Garimpo" in cats:
            tags |= {"garimpo", "peca-unica"}
        if "PROMO" in cats:
            tags.add("promocao")
        tags.discard("")
        imgs = [u.strip() for u in r["Imagens"].split(",") if u.strip()]
        estoque_qtd = int(float(r["Estoque"])) if r["Estoque"].strip() else (1 if r["Em estoque?"].strip() == "1" else 0)
        envio = e.get("envio") or {}
        curta = limpar(e.get("descricao_curta") or "")
        produtos.append({"id": pid, "linha": r, "handle": handles.get(str(pid)) or slug(r["Nome"]), "nome": html.unescape(r["Nome"]),
                         "marca": html.unescape(r["Marcas"]) or "", "tipo": tipo, "cats": cats, "corpo": desc, "campos": campos,
                         "tags": sorted(tags), "imgs": imgs, "qtd": estoque_qtd, "preco": preco(r["Preço"]),
                         "promo": preco(r["Preço promocional"]) if r["Preço promocional"].strip() else 0,
                         "envio": envio, "curta": curta, "e": e})

    top = sorted((p for p in produtos if p["tipo"] in INSTRUMENTOS and p["qtd"] > 0), key=lambda p: -p["preco"])[:12]
    for p in top:
        p["tags"].append("destaques")

    # ---------- Shopify
    col_ficha = {k: f"{ROTULO[k]} (product.metafields.custom.{k})" for k in CHAVES}
    cols = ["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published", "Option1 Name",
            "Option1 Value", "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Qty",
            "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
            "Variant Requires Shipping", "Variant Taxable", "Variant Weight Unit", "Image Src", "Image Position",
            "Image Alt Text", "SEO Title", "SEO Description", "Status"] + list(col_ficha.values())
    with open(SAIDA / "produtos-shopify-enriquecido.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        for p in produtos:
            preco_venda = p["promo"] or p["preco"]
            seo = p["curta"] or " ".join(html.unescape(re.sub(r"<[^>]+>", " ", p["linha"]["Descrição curta"])).split())[:300]
            peso = p["envio"].get("peso_kg")
            for n, src in enumerate(p["imgs"] or [""], 1):
                row = {"Handle": p["handle"], "Image Src": src, "Image Position": n if src else "",
                       "Image Alt Text": f'{p["nome"]} — foto {n}' if src else ""}
                if n == 1:
                    row.update({
                        "Title": p["nome"], "Body (HTML)": p["corpo"], "Vendor": p["marca"] or "Playtime", "Type": p["tipo"],
                        "Tags": ", ".join(p["tags"]), "Published": "TRUE", "Option1 Name": "Title", "Option1 Value": "Default Title",
                        "Variant Grams": int(round(float(peso) * 1000)) if peso else "", "Variant Weight Unit": "kg",
                        "Variant Inventory Tracker": "shopify", "Variant Inventory Qty": p["qtd"], "Variant Inventory Policy": "deny",
                        "Variant Fulfillment Service": "manual", "Variant Price": f"{preco_venda:.2f}",
                        "Variant Compare At Price": f'{p["preco"]:.2f}' if p["promo"] and p["promo"] < p["preco"] else "",
                        "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE", "SEO Title": p["nome"][:70],
                        "SEO Description": seo[:320], "Status": "active"})
                    row.update({col_ficha[k]: v for k, v in p["campos"].items()})
                w.writerow(row)

    # ---------- WooCommerce (mesmo formato do arquivo recebido)
    with open(SAIDA / "woocommerce-enriquecido.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, cab)
        w.writeheader()
        for p in produtos:
            r = dict(p["linha"])
            env = p["envio"]
            for k, c in (("peso_kg", "Peso (kg)"), ("comprimento_cm", "Comprimento (cm)"), ("largura_cm", "Largura (cm)"), ("altura_cm", "Altura (cm)")):
                if env.get(k) and not r[c].strip():
                    r[c] = str(env[k]).replace(".", ",")
            if p["curta"] and not r["Descrição curta"].strip():
                r["Descrição curta"] = p["curta"]
            r["Tags"] = ", ".join(t for t in p["tags"] if t != "destaques")
            if p["campos"] and "Ficha técnica" not in r["Descrição"]:
                tabela = "".join(f"<tr><td><strong>{html.escape(ROTULO[k])}</strong></td><td>{html.escape(v)}</td></tr>"
                                 for k, v in sorted(p["campos"].items(), key=lambda kv: CHAVES.index(kv[0])))
                r["Descrição"] = r["Descrição"] + f"\\n<h3>Ficha técnica</h3>\\n<table><tbody>{tabela}</tbody></table>"
            w.writerow(r)

    # ---------- planilha de revisão
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws = wb.active
    ws.title = "Revisão"
    hdr = ["ID", "Produto", "Tipo", "Confiança", "Campos preenchidos", "Correções na descrição", "Conferir na peça", "Fontes"]
    ws.append(hdr)
    cor = {"alta": "D9F2E3", "media": "FFF1CC", "baixa": "F9D6D5"}
    for p in produtos:
        e = p["e"]
        conf = (e.get("confianca") or "sem pesquisa").replace("é", "e").lower()
        ws.append([p["id"], p["nome"], p["tipo"], conf, len(p["campos"]), "\n".join(e.get("correcoes") or []),
                   "\n".join(e.get("conferir") or []), "\n".join(e.get("fontes") or [])])
        if conf in cor:
            ws.cell(ws.max_row, 4).fill = PatternFill("solid", fgColor=cor[conf])
    ws2 = wb.create_sheet("Ficha técnica")
    usados = [k for k in CHAVES if any(k in p["campos"] for p in produtos)]
    ws2.append(["ID", "Produto", "Tipo", "Peso envio (kg)", "Dimensões envio (cm)"] + [ROTULO[k] for k in usados])
    for p in produtos:
        env = p["envio"]
        dims = "×".join(str(env[k]) for k in ("comprimento_cm", "largura_cm", "altura_cm") if env.get(k))
        ws2.append([p["id"], p["nome"], p["tipo"], env.get("peso_kg", ""), dims] + [p["campos"].get(k, "") for k in usados])
    for sh in (ws, ws2):
        for c in sh[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="4A0000")
        sh.freeze_panes = "C2"
        for i in range(1, sh.max_column + 1):
            sh.column_dimensions[get_column_letter(i)].width = 14 if i in (1, 3, 4, 5) else 38
        for row in sh.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        sh.auto_filter.ref = sh.dimensions
    wb.save(SAIDA / "revisao-enriquecimento.xlsx")

    novos = graphql_novos()
    tema()
    conf = Counter((p["e"].get("confianca") or "sem pesquisa") for p in produtos)
    uso = Counter(k for p in produtos for k in p["campos"])
    print(f"{len(produtos)} produtos | pesquisa: {dict(conf)}")
    print(f"com ficha: {sum(1 for p in produtos if p['campos'])} | média de campos: {sum(len(p['campos']) for p in produtos) / len(produtos):.1f}")
    print(f"com peso de envio: {sum(1 for p in produtos if p['envio'].get('peso_kg'))} | correções: {sum(len(p['e'].get('correcoes') or []) for p in produtos)}")
    print(f"campos mais preenchidos: {uso.most_common(12)}")
    print(f"campos novos para criar na loja: {novos}")


if __name__ == "__main__":
    main()
