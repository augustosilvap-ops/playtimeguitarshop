"""AGENTE 5 · CRIADOR DE MINIATURAS — capa 1080×1920 no padrão aprovado (v3): personagem oficial recortado em alta (BiRefNet),
fundo da própria cena desfocado, palavra metálica ATRÁS do personagem e faixa amarela NA FRENTE.
Uso: python3 a5_miniatura.py <data>"""
import sys, subprocess
from nucleo import *
def uma(data, pid):  # roda numa chamada separada: o recorte BiRefNet usa muita memória
    import capa_v3 as C
    C.OUT = saida(data) + '/'; p = next(p for p in pautas(data) if p['id'] == pid); cp = p['capa']
    C.make(n=p['id'], src=cp['personagem'], top=cp['top'], bar=cp['bar'], **cp.get('ajustes', {}))
def main(data):
    for p in pautas(data):
        subprocess.run([sys.executable, __file__, data, '--uma', p['id']], check=True, cwd=AG)
        f = os.path.join(saida(data), f"capa_{p['id']}.jpg"); log('miniatura', f"{p['id']} ✓ {os.path.basename(f)}")
        marcar(data, p['id'], 'miniatura', capa=os.path.relpath(f, REPO))
if __name__ == '__main__':
    if '--uma' in sys.argv: uma(sys.argv[1], sys.argv[sys.argv.index('--uma') + 1])
    else: main(sys.argv[1])
