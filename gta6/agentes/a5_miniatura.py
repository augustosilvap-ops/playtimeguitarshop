"""AGENTE 5 · CRIADOR DE MINIATURAS — capa 1080×1920 no padrão aprovado (v3): personagem oficial recortado em alta (BiRefNet),
fundo da própria cena desfocado, palavra metálica ATRÁS do personagem e faixa amarela NA FRENTE.
Uso: python3 a5_miniatura.py <data>"""
import sys, shutil
from nucleo import *
import capa_v3 as C
def main(data):
    C.OUT = saida(data) + '/'
    for p in pautas(data):
        cp = p['capa']; C.make(n=p['id'], src=cp['personagem'], top=cp['top'], bar=cp['bar'], **cp.get('ajustes', {}))
        f = os.path.join(saida(data), f"capa_{p['id']}.jpg"); log('miniatura', f"{p['id']} ✓ {os.path.basename(f)}")
        marcar(data, p['id'], 'miniatura', capa=os.path.relpath(f, REPO))
if __name__ == '__main__': main(sys.argv[1])
