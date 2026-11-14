"""Narração automática PT-BR com Kokoro (voz neural aberta, Apache 2.0).
Uso: python3 narrar.py "texto" saida.wav [voz=pm_alex] [velocidade=1.1]
Modelo/vozes em KOKORO_DIR (padrão /home/user/kokoro): model.onnx + <voz>.bin (onnx-community/Kokoro-82M-v1.0-ONNX)."""
import sys, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
D = os.environ.get('KOKORO_DIR', '/home/user/kokoro')
txt, out = sys.argv[1], sys.argv[2]
voz = sys.argv[3] if len(sys.argv) > 3 else 'pm_alex'
vel = float(sys.argv[4]) if len(sys.argv) > 4 else 1.1
# kokoro-onnx espera um arquivo de vozes; montamos um .npz com as vozes baixadas
npz = f'{D}/voices.npz'
if not os.path.exists(npz):
    np.savez(npz, **{v[:-4]: np.fromfile(f'{D}/{v}', dtype=np.float32).reshape(-1, 1, 256) for v in os.listdir(D) if v.endswith('.bin')})
k = Kokoro(f'{D}/model.onnx', npz)
audio, sr = k.create(txt, voice=voz, speed=vel, lang='pt-br')
sf.write(out, audio, sr); print('ok', out, round(len(audio) / sr, 2), 's')
