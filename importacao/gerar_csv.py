"""Gera a planilha de importação da Shopify a partir dos produtos do site atual (WooCommerce).

Uso:  python3 gerar_csv.py            (baixa os produtos de playtimeguitarshop.com)
      python3 gerar_csv.py all.json   (usa um arquivo já baixado)
Saída: produtos-shopify.csv na mesma pasta.
"""
import csv, html, json, re, sys, unicodedata, urllib.request
from pathlib import Path

SITE = "https://playtimeguitarshop.com/wp-json/wc/store/v1/products?per_page=100&page={}"
OUT = Path(__file__).with_name("produtos-shopify.csv")

def baixar():
    itens, page = [], 1
    while True:
        req = urllib.request.Request(SITE.format(page), headers={"User-Agent": "playtime-export"})
        with urllib.request.urlopen(req, timeout=60) as r:
            lote = json.load(r)
            total = int(r.headers.get("X-WP-TotalPages", "1"))
        itens += lote
        if page >= total or not lote:
            return itens
        page += 1

def slug(s):
    s = unicodedata.normalize("NFKD", html.unescape(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def limpar_html(h):
    h = re.sub(r'\s+data-[a-z-]+="[^"]*"', "", h or "")
    h = re.sub(r"<span>(.*?)</span>", r"\1", h, flags=re.S)
    return h.strip()

TIPOS = [("Guitarras", "Guitarras"), ("Violões", "Violões"), ("Baixos", "Baixos"),
         ("Amplificadores", "Amplificadores"), ("Pedaleira", "Pedais"), ("Pedais", "Pedais"),
         ("Case", "Cases e bags"), ("Acessórios", "Acessórios")]
MARCAS_CAT = {"Hertom Guitars": "Hertom", "Martin Guitars": "Martin", "Ibanez Premium": "Ibanez",
              "Ibanez Prestige": "Ibanez", "Ibanez": "Ibanez", "Takamine": "Takamine", "Squier": "Squier",
              "Jet Guitars": "Jet Guitars", "Schecter Guitar Research": "Schecter", "Schecter": "Schecter",
              "Fender": "Fender", "G&amp;l": "G&L", "PRS": "PRS", "Cort": "Cort", "D'Agelico": "D'Angelico",
              "Tagima": "Tagima", "Stagg": "Stagg", "Ltd": "LTD"}
INSTRUMENTOS = {"Guitarras", "Violões", "Baixos"}

def converter(p):
    cats = [html.unescape(c["name"]) for c in p["categories"]]
    cats_raw = [c["name"] for c in p["categories"]]
    tipo = next((t for c, t in TIPOS if c in cats), "Acessórios")
    marca = html.unescape(p["brands"][0]["name"]) if p.get("brands") else ""
    if not marca:
        marca = next((MARCAS_CAT[c] for c in cats_raw if c in MARCAS_CAT), "")
    if not marca:
        palavras = html.unescape(p["name"]).replace("–", " ").split()
        marca = palavras[1].title() if len(palavras) > 1 else "Playtime"
    tags = {slug(c) for c in cats}
    tags.add(slug(tipo))
    if tipo in ("Pedais", "Amplificadores"):
        tags.add("pedais-e-amps")
    if "Garimpo" in cats:
        tags.update({"garimpo", "peca-unica"})
    if "PROMO" in cats:
        tags.add("promocao")
    preco = int(p["prices"]["price"]) / 100
    regular = int(p["prices"]["regular_price"] or p["prices"]["price"]) / 100
    corpo = limpar_html(p["description"]) or limpar_html(p["short_description"])
    resumo = re.sub(r"<[^>]+>", " ", p["short_description"] or p["description"] or "")
    resumo = " ".join(html.unescape(resumo).split())[:300]
    return {
        "handle": p["slug"], "title": html.unescape(p["name"]), "body": corpo, "vendor": marca,
        "type": tipo, "tags": sorted(tags), "price": preco, "compare": regular if regular > preco else "",
        "qty": p["low_stock_remaining"] or (1 if p["is_in_stock"] else 0),
        "images": [i["src"] for i in p["images"]], "seo": resumo, "instrumento": tipo in INSTRUMENTOS,
    }

COLS = ["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published",
        "Option1 Name", "Option1 Value", "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
        "Variant Inventory Qty", "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price",
        "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Image Src",
        "Image Position", "Image Alt Text", "SEO Title", "SEO Description", "Status"]

def main():
    dados = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else baixar()
    produtos = [converter(p) for p in dados]
    # "destaques": os 12 instrumentos mais caros em estoque (dá para trocar depois na Shopify)
    top = sorted((x for x in produtos if x["instrumento"] and x["qty"] > 0), key=lambda x: -x["price"])[:12]
    for x in top:
        x["tags"].append("destaques")
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        for x in produtos:
            imgs = x["images"] or [""]
            for n, src in enumerate(imgs, 1):
                row = {"Handle": x["handle"], "Image Src": src, "Image Position": n if src else "",
                       "Image Alt Text": x["title"] if src else ""}
                if n == 1:
                    row.update({
                        "Title": x["title"], "Body (HTML)": x["body"], "Vendor": x["vendor"], "Type": x["type"],
                        "Tags": ", ".join(x["tags"]), "Published": "TRUE", "Option1 Name": "Title",
                        "Option1 Value": "Default Title", "Variant Grams": "", "Variant Inventory Tracker": "shopify",
                        "Variant Inventory Qty": x["qty"], "Variant Inventory Policy": "deny",
                        "Variant Fulfillment Service": "manual", "Variant Price": f'{x["price"]:.2f}',
                        "Variant Compare At Price": f'{x["compare"]:.2f}' if x["compare"] else "",
                        "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE",
                        "SEO Title": x["title"], "SEO Description": x["seo"], "Status": "active"})
                w.writerow(row)
    print(f"{len(produtos)} produtos, {sum(len(x['images']) for x in produtos)} fotos -> {OUT}")

if __name__ == "__main__":
    main()
