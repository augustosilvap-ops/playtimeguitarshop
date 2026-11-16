"""Reels de TESTE (Instagram 'Reel de teste' — só para não seguidores), 2 pares por dia, 17–20/11.
Cada par muda UMA variável. Cada variável é testada 2 vezes com conteúdos diferentes.
Gera augusto/entregas/testes_reels/ (vídeos A/B por par, GUIA.md) e Testes_Reels.xlsx (planilha de resultados).
Rodar em augusto/: python3 editorial/testes_reels.py"""
import os, shutil, json
E = 'entregas'; AB = '/tmp/claude-0/drive/ab'
PARES = [
 # (dia, hora, par, variável, conteúdo, A (arquivo, descrição), B (arquivo, descrição), legenda (post id))
 ('17/11', '11h', 1, 'Efeito', 'ANUNCIO', (f'{E}/2026-11-19/12_reel_anuncio/reel_narrado_1080x1920_56s.mp4', 'abertura normal'), (f'{E}/2026-11-19/12_reel_anuncio/reel_teste_mundo_interface_56s.mp4', 'abertura "mundo de interface"'), ('2026-11-17', '12')),
 ('17/11', '15h', 2, 'Duração', 'DESCONTO', (f'{E}/2026-11-18/09_reel_desconto/reel_narrado_1080x1920_79s.mp4', 'completa (79 s)'), (f'{AB}/desconto_curta.mp4', 'curta'), ('2026-11-17', '09')),
 ('18/11', '11h', 3, 'Narração', 'TITULO', (f'{E}/2026-11-18/15_reel_titulo/reel_narrado_1080x1920_58s.mp4', 'com voz'), (f'{AB}/titulo_semvoz.mp4', 'sem voz (só legenda + trilha)'), ('2026-11-18', '15')),
 ('18/11', '15h', 4, 'Gancho', 'ROAS', (f'{E}/2026-11-19/23_reel_roas/reel_narrado_1080x1920_53s.mp4', 'gancho pergunta ("Gastou em anúncio")'), (f'{AB}/roas_numero.mp4', 'gancho número ("R$ 500 → R$ 248 de prejuízo")'), ('2026-11-19', '23')),
 ('19/11', '11h', 5, 'Efeito', 'PLANILHA', (f'{E}/2026-11-16/03_reel_precificar-leigo/reel_narrado_1080x1920_79s.mp4', 'abertura normal'), (f'{AB}/planilha_ui.mp4', 'abertura "mundo de interface"'), ('2026-11-18', '03')),
 ('19/11', '15h', 6, 'Duração', 'ROTINA', (f'{E}/2026-11-19/18_reel_rotina/reel_narrado_1080x1920_54s.mp4', 'completa'), (f'{AB}/rotina_curta.mp4', 'curta'), ('2026-11-19', '18')),
 ('20/11', '11h', 7, 'Narração', 'ATENDE', (f'{E}/2026-11-20/21_reel_atende/reel_narrado_1080x1920_51s.mp4', 'com voz'), (f'{AB}/atende_semvoz.mp4', 'sem voz (só legenda + trilha)'), ('2026-11-20', '21')),
 ('20/11', '15h', 8, 'Gancho', 'GARIMPO', (f'{E}/2026-11-17/06_reel_garimpo/reel_narrado_1080x1920_64s.mp4', 'gancho pergunta ("Comprou 200 peças no achismo?")'), (f'{AB}/garimpo_numero.mp4', 'gancho número ("200 compradas → 12 vendidas")'), ('2026-11-16', '06')),
]

def dur(f):
    import subprocess
    return round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout or 0))

def main():
    D = f'{E}/testes_reels'; os.makedirs(D, exist_ok=True)
    md = ['# Reels de TESTE — 2 pares por dia (17 a 20/11)\n',
          'Como postar: no app, ao publicar o Reel, ative **"Reel de teste"** (vai só para quem não te segue). Poste o **A e o B do mesmo par com até 10 minutos de diferença**, com a mesma legenda e a mesma capa. Não promova nenhum dos dois para o feed antes da leitura.\n',
          'Leitura: **72 h depois**, anote na planilha `Testes_Reels.xlsx`: visualizações, % que passou dos 3 s (retenção inicial), tempo médio assistido, salvamentos, compartilhamentos e novos seguidores. Me manda os prints ou os números que eu analiso.\n',
          'Regra de decisão: vence quem tiver **tempo médio assistido + compartilhamentos** maiores. Diferença menor que 10% = empate.\n',
          '\n| Dia | Hora | Par | Variável | Conteúdo | A | B |\n|---|---|---|---|---|---|---|\n']
    rows = []
    for dia, hora, par, var, cont, A, B, leg in PARES:
        fa, fb = f'{D}/par{par:02d}_{cont}_A.mp4', f'{D}/par{par:02d}_{cont}_B.mp4'
        shutil.copy(A[0], fa); shutil.copy(B[0], fb)
        da, db = dur(fa), dur(fb)
        md.append(f'| {dia} | {hora} | {par} | {var} | {cont} | {A[1]} ({da} s) | {B[1]} ({db} s) |\n')
        rows.append((dia, hora, par, var, cont, f'{A[1]} ({da} s)', f'{B[1]} ({db} s)', leg))
    md.append('\n## Legendas\nUse nos dois vídeos do par a mesma legenda do post do feed:\n\n')
    for dia, hora, par, var, cont, a, b, (d, pid) in rows:
        cap = json.load(open(f'publicacao/{d}/{pid}.json'))['params']['caption']
        md.append(f'### Par {par} · {cont}\n\n{cap}\n\n')
    open(f'{D}/GUIA.md', 'w').write(''.join(md))
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook(); ws = wb.active; ws.title = 'Resultados'
    H = ['Dia', 'Hora', 'Par', 'Variável', 'Conteúdo', 'Versão', 'Descrição', 'Visualizações', '% passou dos 3 s', 'Tempo médio (s)', 'Salvamentos', 'Compartilhamentos', 'Novos seguidores', 'Vencedor?']
    ws.append(H)
    for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='08090E'); c.alignment = Alignment(wrap_text=True)
    for dia, hora, par, var, cont, a, b, _ in rows:
        ws.append([dia, hora, par, var, cont, 'A', a] + [None] * 7)
        ws.append([dia, hora, par, var, cont, 'B', b] + [None] * 7)
    for i, w in enumerate([7, 6, 5, 11, 11, 7, 42, 13, 13, 13, 12, 14, 13, 10], 1): ws.column_dimensions[chr(64 + i)].width = w
    wb.save(f'{D}/Testes_Reels.xlsx'); print(len(rows), 'pares')

if __name__ == '__main__': main()
