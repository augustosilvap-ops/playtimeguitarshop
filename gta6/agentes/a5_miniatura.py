"""AGENTE 5 · CRIADOR DE MINIATURAS — capa 1080×1920 no padrão v6 (identidade oficial, aprovada 23/11):
arte oficial ilustrada da Rockstar + logo Caos Insano + logo GTA VI + título branco / pincel rosa / branco + traço ciano.
Campos em pauta["capa"]: a, b, c, arte (opcional; senão gira entre as artes) e seta [x, y, "esq"|"dir"] (opcional).
Compatível com o formato antigo (top/bar): vira a=top, b=bar, c="NO GTA 6".
Uso: python3 a5_miniatura.py <data>"""
import sys, subprocess
from nucleo import *
def uma(data, pid):
    import capa_v6 as C
    P = pautas(data); k = [p['id'] for p in P].index(pid); cp = P[k]['capa']
    arte = cp.get('arte') or C.ARTES[(abs(hash(data)) + k) % len(C.ARTES)]
    C.make(pid, cp.get('a', cp.get('top', '')), cp.get('b', cp.get('bar', '')), cp.get('c', 'NO GTA 6'), arte, saida(data), cp.get('seta'))
def main(data):
    for p in pautas(data):
        subprocess.run([sys.executable, __file__, data, '--uma', p['id']], check=True, cwd=AG)
        f = os.path.join(saida(data), f"capa_{p['id']}.jpg"); log('miniatura', f"{p['id']} ✓ {os.path.basename(f)}")
        marcar(data, p['id'], 'miniatura', capa=os.path.relpath(f, REPO))
if __name__ == '__main__':
    if '--uma' in sys.argv: uma(sys.argv[1], sys.argv[sys.argv.index('--uma') + 1])
    else: main(sys.argv[1])
