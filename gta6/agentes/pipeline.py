"""CAOS INSANO BR · pipeline dos agentes 2→6 para um dia (o agente 1 é o Claude pesquisando e escrevendo fila/<data>/pautas.json).
Uso: python3 pipeline.py <data> [--de a3] [--sem-push]
Cada etapa grava em fila/<data>/status.json; se uma falhar, as seguintes não rodam."""
import sys, subprocess
from nucleo import *
ETAPAS = ['a2_roteiro', 'a3_voz', 'a4_editor', 'a5_miniatura', 'a6_enviador']
def main():
    data = sys.argv[1]; de = sys.argv[sys.argv.index('--de') + 1] if '--de' in sys.argv else 'a2'
    for e in ETAPAS[[x[:2] for x in ETAPAS].index(de):]:
        cmd = [sys.executable, os.path.join(AG, e + '.py'), data] + (['--sem-push'] if e == 'a6_enviador' and '--sem-push' in sys.argv else [])
        log('pipeline', f'→ {e}'); r = subprocess.run(cmd, cwd=AG)
        if r.returncode: log('pipeline', f'✗ parou em {e}'); sys.exit(r.returncode)
    log('pipeline', '✓ concluído')
if __name__ == '__main__': main()
