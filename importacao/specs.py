"""Lê a descrição (HTML) de um produto do site atual e separa a ficha técnica.

Aceita os três formatos usados no site:
  "Chave: valor" na mesma linha · chave numa linha e valor na seguinte · "– Tampo em Flamed Maple".
Devolve um dicionário com as chaves dos metafields custom.* do tema.
"""
import html
import re
import unicodedata

# rótulo encontrado na descrição -> chave do metafield
ROTULOS = {
    "tamanho da escala": "escala", "comprimento da escala": "escala", "escala (comprimento)": "escala",
    "escala": "escala_madeira", "material da escala": "escala_madeira",
    "braco": "braco_madeira", "material do braco": "braco_madeira",
    "perfil do braco": "braco_perfil", "formato do braco": "braco_perfil",
    "corpo": "corpo", "corpo (laterais e fundo)": "corpo", "laterais e fundo": "corpo", "fundo e laterais": "corpo",
    "tampo": "tampo",
    "trastes": "trastes", "tipo de trastes": "trastes_tipo",
    "captacao": "captadores", "captadores": "captadores",
    "controles": "eletrica", "eletrica": "eletrica", "eletronica": "eletrica",
    "ponte": "ponte", "tarraxas": "tarraxas", "acabamento": "acabamento",
    "largura do nut": "nut_largura", "raio": "raio", "raio da escala": "raio",
}
CAMPOS = ["escala", "nut_largura", "raio", "braco_perfil", "braco_madeira", "escala_madeira", "trastes",
          "corpo", "tampo", "captadores", "eletrica", "ponte", "tarraxas", "acabamento"]


def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip(" :–-*•")


def _linhas(desc):
    t = re.sub(r"<(br|/p|/tr|/li|/h\d|/div)[^>]*>", "\n", desc or "", flags=re.I)
    t = re.sub(r"</td>\s*<td[^>]*>", ": ", t, flags=re.I)  # tabelas: célula | célula
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return [re.sub(r"\s+", " ", x).strip() for x in t.splitlines() if x.strip()]


def extrair(desc):
    out = {}
    linhas = _linhas(desc)
    i = 0
    while i < len(linhas):
        ln = linhas[i].strip(" –-•*")
        chave = valor = None
        if ":" in ln:
            a, b = ln.split(":", 1)
            if _norm(a) in ROTULOS and b.strip():
                chave, valor = ROTULOS[_norm(a)], b.strip()
        if chave is None and _norm(ln) in ROTULOS and i + 1 < len(linhas) and ":" not in linhas[i + 1]:
            chave, valor = ROTULOS[_norm(ln)], linhas[i + 1].strip()
            i += 1
        if chave is None:
            m = re.match(r"^(tampo|braco|escala|corpo|ponte|tarraxas|captadores|eletrica)\s+(em|de)?\s*(.+)$", _norm(ln))
            if m:
                original = re.sub(r"^\S+\s+(em|de)?\s*", "", ln, flags=re.I)
                chave = ROTULOS[m.group(1)]
                valor = original.strip()
        if chave and valor and chave not in out:
            out[chave] = valor[:250]
        i += 1
    if "trastes_tipo" in out:
        t = out.pop("trastes_tipo")
        out["trastes"] = (out.get("trastes", "") + " · " + t).strip(" ·")[:250]
    # raio escrito junto com a escala: "Rosewood (Raio de 430mmR)" / "raio composto (228mm a 305mm)"
    if "raio" not in out:
        for k in ("escala_madeira", "escala"):
            m = re.search(r"raio[^()\d]*\(?([^)]*\d[^)]*)\)?", out.get(k, ""), flags=re.I)
            if m:
                out["raio"] = m.group(1).strip(" ,.")
                break
    return {k: out[k] for k in CAMPOS if out.get(k)}


if __name__ == "__main__":
    exemplo = "<p>Tamanho da escala</p><p>25.5″ (648 mm)</p><p>Escala: Rosewood (Raio de 430mmR)</p><p>– Tampo em Flamed Maple 5A</p>"
    print(extrair(exemplo))
