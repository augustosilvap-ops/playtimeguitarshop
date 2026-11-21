"""Núcleo compartilhado dos agentes do Caos Insano BR (caminhos, fila, status)."""
import os, sys, json, re, datetime
AG = os.path.dirname(os.path.abspath(__file__)); GTA = os.path.dirname(AG); REPO = os.path.dirname(GTA)
SRC = os.path.join(GTA, 'src'); sys.path.insert(0, SRC)
CFG = json.load(open(os.path.join(AG, 'config.json')))
BR = CFG['brutos']
def fila(data): d = os.path.join(AG, 'fila', data); os.makedirs(d, exist_ok=True); return d
def saida(data): d = os.path.join(GTA, 'entregas', 'auto', data); os.makedirs(d, exist_ok=True); return d
def pautas(data): return json.load(open(os.path.join(fila(data), 'pautas.json')))
def salvar_pautas(data, P): json.dump(P, open(os.path.join(fila(data), 'pautas.json'), 'w'), ensure_ascii=False, indent=1)
def status(data):
    f = os.path.join(fila(data), 'status.json'); return json.load(open(f)) if os.path.exists(f) else {}
def marcar(data, pid, etapa, **info):
    f = os.path.join(fila(data), 'status.json'); s = status(data); s.setdefault(pid, {})[etapa] = dict(ok=True, em=datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z', **info)
    json.dump(s, open(f, 'w'), ensure_ascii=False, indent=1)
def palavras(t): return len(re.findall(r"\w+", t))
def log(ag, msg): print(f'[{ag}] {msg}', flush=True)
