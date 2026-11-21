"""AGENTE 3 · GERADOR DE VOZ — narra cada frase com a voz aprovada (Lucas, ElevenLabs; chave injetada pelo proxy) e guarda em cache.
Gera também uma prévia da narração completa (<id>_voz.wav) para conferência.
Uso: python3 a3_voz.py <data>"""
import sys, re
import numpy as np, soundfile as sf
from nucleo import *
import gen_caos as G
NA = G.NA
def main(data):
    for p in pautas(data):
        partes = []
        for c in p['cenas']:
            for fr in [f for f in re.split(r'(?<=[.?!:])\s+', c['fala']) if f.strip()]:
                partes.append(NA.tts(NA.falar(fr))); partes.append(np.zeros(int(.08 * NA.SR), np.float32))
        a = np.concatenate(partes); sf.write(os.path.join(saida(data), f"{p['id']}_voz.wav"), a, NA.SR)
        d = round(len(a) / NA.SR, 1); log('voz', f"{p['id']} ✓ narração {d}s"); marcar(data, p['id'], 'voz', segundos=d)
if __name__ == '__main__': main(sys.argv[1])
