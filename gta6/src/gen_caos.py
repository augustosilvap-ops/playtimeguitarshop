"""CAOS INSANO BR — Shorts de curiosidades narrados (voz Lucas, legenda palavra a palavra, trilha Mixkit + SFX).
Uso: python3 gen_caos.py <nome> <saida.mp4> [trilha.mp3]
FATOS: só informação pública e confirmada (Rockstar/imprensa). Sem spoiler da história. Sem arte/logo da Rockstar."""
import sys, os, json, re, subprocess, contextlib, io
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); MOT = os.path.abspath(os.path.join(HERE, '../../augusto/src/motion'))
sys.path.insert(0, MOT); _cwd = os.getcwd(); os.chdir(MOT)
with contextlib.redirect_stdout(io.StringIO()):
    import narrar_aula as NA
os.chdir(HERE)
def S(shot, **p): return dict(shot=shot, p=p)

# Fontes: GTA V lançado em 17/09/2013; GTA VI 19/11/2026 (Rockstar, adiado de "outono 2025" → 26/05/2026 → 19/11/2026).
# Trailer 1 (05/12/2023, liberado na véspera, 04/12, após vazamento): 90+ milhões de views em 24 h no YouTube (recorde de vídeo não musical).
# Trailer 2 (06/05/2025): 475 milhões de views em 24 h somando plataformas (Rockstar). Músicas: Tom Petty "Love Is a Long Road" (T1), The Pointer Sisters "Hot Together" (T2).
# Parte 2: dev confirmado 04/02/2022; vazamento 18/09/2022 (90+ vídeos, hacker de 17 anos); Rockstar fundada 12/1998 → trailer 1 em 12/2023 (25 anos);
# trailer 2 "capturado inteiramente no jogo no PS5" (Rockstar); lançamento PS5/Xbox Series, sem PC anunciado; GTA V 200+ mi cópias (Take-Two); nomes Jason Duval/Lucia Caminos (site Rockstar, 05/2025).
# Leonida = estado inspirado na Flórida (regiões divulgadas pela Rockstar em 05/2025: Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga); Vice City = inspirada em Miami. Lucia: primeira protagonista mulher da era 3D da série.
REELS = {
 'curiosidades1': [
  (S('title', html='7 COISAS<br><span class="cy">QUE VOCÊ</span><br>PRECISA SABER<br><span class="yl">ANTES DE JOGAR</span>', size=150), "Sete coisas sobre o GTA 6 que você precisa saber antes de jogar."),
  (S('years', a=2013, b=2026, big='13 ANOS'), "Um: foram treze anos de espera. O GTA 5 saiu em 2013, e o 6 chega agora, em 19 de novembro de 2026."),
  (S('delay', lbl='ADIADO 2 VEZES', steps=['2025', 'MAIO 2026', '19 NOV 2026']), "Dois: ele foi adiado duas vezes. Era para 2025, passou para maio de 2026 e só então ficou para 19 de novembro."),
  (S('rank', n=3, html='LUCIA<br><span class="cy">FAZ HISTÓRIA</span>', sub='Primeira protagonista mulher da era 3D da série.', sky=1), "Três: Lucia é a primeira protagonista mulher da era 3D da série. Ela divide a história com o Jason."),
  (S('num', lbl='Trailer 1 · em 24 horas', v=90, pre='+', suf='', unit='MILHÕES DE VIEWS', sub='Recorde de vídeo não musical no YouTube'), "Quatro: o primeiro trailer passou de 90 milhões de visualizações no YouTube em 24 horas. Recorde para um vídeo que não é clipe de música."),
  (S('rank', n=5, html='VAZOU,<br><span class="yl">SAIU ANTES</span>', sub='O trailer 1 foi liberado um dia antes do previsto, depois de vazar na internet.', top=540), "Cinco: esse trailer saiu um dia antes do previsto, porque vazou na internet e a Rockstar decidiu liberar na hora."),
  (S('num', lbl='Trailer 2 · em 24 horas', v=475, unit='MILHÕES DE VIEWS', sub='Somando todas as plataformas', size=280), "Seis: o segundo trailer foi ainda maior. 475 milhões de visualizações em 24 horas, somando todas as plataformas."),
  (S('map', lbl='LEONIDA = FLÓRIDA', pins=['Vice City', 'Leonida Keys', 'Grassrivers', 'Port Gellhorn', 'Ambrosia', 'Mount Kalaga']), "Sete: o mapa se passa em Leonida, um estado inspirado na Flórida. E Vice City é a versão do jogo para Miami."),
  (S('song', lbl='BÔNUS · TRILHA DOS TRAILERS', t='LOVE IS A LONG ROAD', a='Tom Petty · trailer 1'), "Bônus: a música do primeiro trailer é Love Is a Long Road, de Tom Petty."),
  (S('cta', html='QUAL VOCÊ<br><span class="yl">NÃO SABIA?</span>', btn='SEGUE PRA PARTE 2 →'), "Qual dessas você não sabia? Segue o Caos Insano que amanhã tem parte dois."),
 ],
}
REELS['curiosidades2'] = [
  (S('title', html='MAIS 7<br><span class="cy">COISAS</span><br>DO <span class="yl">GTA 6</span><br>QUE POUCA GENTE SABE', size=140), "Mais sete coisas do GTA 6 que pouca gente sabe. Parte dois."),
  (S('delay', lbl='LINHA DO TEMPO', steps=['FEV 2022', 'SET 2022', 'DEZ 2023'], nocut=1), "Um: a Rockstar só confirmou que o jogo estava em produção em fevereiro de 2022. Sete meses depois veio um dos maiores vazamentos da história dos games."),
  (S('num', lbl='Vazamento · set 2022', v=90, pre='+', unit='VÍDEOS VAZADOS', sub='De uma versão inicial do jogo, ainda em desenvolvimento'), "Dois: mais de 90 vídeos de uma versão inicial do jogo vazaram na internet. E quem vazou foi um hacker de 17 anos."),
  (S('rank', n=3, html='TRAILER DE<br><span class="yl">ANIVERSÁRIO</span>', sub='O trailer 1 saiu em dezembro de 2023, mês dos 25 anos da Rockstar.'), "Três: o primeiro trailer foi lançado em dezembro de 2023, no mês em que a Rockstar completou 25 anos."),
  (S('rank', n=4, html='TUDO<br><span class="cy">NO PS5</span>', sub='A Rockstar disse que o trailer 2 foi capturado inteiro dentro do jogo, no PS5.'), "Quatro: segundo a Rockstar, o trailer dois foi capturado inteiro dentro do jogo, rodando no PS5. Uma parte é gameplay e outra parte é cena."),
  (S('check', lbl='NO LANÇAMENTO', items=[('PS5', 1), ('XBOX SERIES', 1), ('PC', 0)]), "Cinco: no lançamento, o jogo sai só para PS5 e Xbox Series. Para PC ainda não tem data."),
  (S('num', lbl='A régua: GTA 5 vendeu', v=200, pre='+', unit='MILHÕES DE CÓPIAS', sub='Um dos jogos mais vendidos da história'), "Seis: a régua está alta. O GTA 5 passou de 200 milhões de cópias vendidas, um dos jogos mais vendidos da história."),
  (S('rank', n=7, html='JASON <span class="cy">DUVAL</span><br>&amp; LUCIA<br><span class="yl">CAMINOS</span>', top=520, size=130, sub='Os nomes completos dos protagonistas, revelados pela Rockstar.', subTop=1000), "Sete: os protagonistas têm nome completo. Jason Duval e Lucia Caminos."),
  (S('song', lbl='BÔNUS · TRILHA DO TRAILER 2', t='HOT TOGETHER', a='The Pointer Sisters · trailer 2'), "Bônus: a música do trailer dois é Hot Together, das Pointer Sisters."),
  (S('cta', html='AMANHÃ<br><span class="yl">É O DIA</span>', btn='SEGUE O CAOS INSANO →'), "Amanhã é o dia. Segue o Caos Insano pra não perder nada do lançamento."),
]
# ---- BATERIA 1 (semana de lançamento) — fatos: site oficial da Rockstar (personagens/regiões, 05/2025) e datas de lançamento da série.
# Jason: cresceu cercado de golpistas; passou pelo Exército tentando deixar a adolescência problemática para trás (site Rockstar).
# Lucia: o pai a ensinou a lutar assim que aprendeu a andar; aparece presa no trailer 1 (site Rockstar / trailer).
# Regiões (site Rockstar): Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia, Mount Kalaga National Park.
# Série: GTA III 2001, Vice City 2002, San Andreas 2004, GTA IV 2008, GTA V 2013, GTA VI 2026.
REELS['personagens'] = [
  (S('title', html='QUEM SÃO<br><span class="cy">JASON</span> E<br><span class="yl">LUCIA?</span>', size=170), "Quem são Jason e Lucia, os protagonistas do GTA 6? Sem spoiler, só o que a Rockstar mostrou."),
  (S('rank', n=1, html='LUCIA<br><span class="cy">CAMINOS</span>', sub='Começa a história atrás das grades.', sky=1), "Lucia Caminos. No primeiro trailer, ela aparece presa, e é assim que a história dela começa."),
  (S('rank', n=2, html='CRIADA<br><span class="yl">PRA LUTAR</span>', sub='Segundo a Rockstar, o pai dela a ensinou a lutar assim que ela aprendeu a andar.'), "Segundo a Rockstar, o pai dela a ensinou a lutar assim que ela aprendeu a andar."),
  (S('rank', n=3, html='JASON<br><span class="cy">DUVAL</span>', sub='Cresceu cercado de golpistas e criminosos.', sky=1), "Jason Duval cresceu cercado de golpistas e criminosos."),
  (S('rank', n=4, html='EX-<span class="yl">EXÉRCITO</span>', sub='Passou pelo Exército tentando deixar a adolescência problemática para trás.'), "Ele passou pelo Exército tentando deixar a adolescência problemática para trás. Não deu muito certo."),
  (S('title', html='DOIS CONTRA<br><span class="cy">LEONIDA</span>', size=170), "Juntos, eles viram uma dupla tentando sobreviver em Leonida. E o resto você descobre jogando."),
  (S('cta', html='TIME<br><span class="cy">JASON</span> OU<br><span class="yl">LUCIA?</span>', btn='COMENTA AQUI 👇'), "E aí, você é time Jason ou time Lucia? Comenta aqui e segue o Caos Insano."),
]
REELS['mapa'] = [
  (S('title', html='O MAPA DE<br><span class="cy">LEONIDA</span><br>EM 30 SEGUNDOS', size=160), "O mapa do GTA 6 em 30 segundos. São seis regiões, todas inspiradas na Flórida."),
  (S('rank', n=1, html='VICE<br><span class="yl">CITY</span>', sub='A cidade grande, versão do jogo para Miami.', sky=1), "Um: Vice City. A cidade grande do mapa, a versão do jogo para Miami."),
  (S('rank', n=2, html='LEONIDA<br><span class="cy">KEYS</span>', sub='Ilhas e praias, inspiradas nas Florida Keys.'), "Dois: Leonida Keys. As ilhas e praias inspiradas nas Florida Keys."),
  (S('rank', n=3, html='GRASS<br><span class="cy">RIVERS</span>', sub='Pântanos, inspirados nos Everglades.', sky=1), "Três: Grassrivers. Os pântanos, inspirados nos Everglades."),
  (S('rank', n=4, html='PORT<br><span class="yl">GELLHORN</span>', sub='Cidade portuária no litoral.'), "Quatro: Port Gellhorn, uma cidade portuária no litoral."),
  (S('rank', n=5, html='AMBROSIA', sub='Cidade do interior de Leonida.', sky=1), "Cinco: Ambrosia, uma cidade do interior de Leonida."),
  (S('rank', n=6, html='MOUNT<br><span class="cy">KALAGA</span>', sub='Parque nacional, com trilhas e natureza.'), "Seis: Mount Kalaga, um parque nacional com trilhas e muita natureza."),
  (S('cta', html='QUAL VOCÊ<br><span class="yl">EXPLORA</span><br>PRIMEIRO?', btn='SEGUE O CAOS INSANO →'), "Qual região você vai explorar primeiro? Comenta e segue o Caos Insano."),
]
REELS['linha_do_tempo'] = [
  (S('title', html='25 ANOS<br><span class="cy">DE CAOS</span><br>EM <span class="yl">30 SEG</span>', size=170), "A história do GTA em 3D até o 6, em 30 segundos."),
  (S('years', a=2001, b=2001, big='GTA III'), "2001: GTA 3 leva a série para o 3D e muda os jogos de mundo aberto."),
  (S('years', a=2001, b=2002, big='VICE CITY'), "2002: Vice City. Anos 80, neon e a primeira visita à versão do jogo para Miami."),
  (S('years', a=2002, b=2004, big='SAN ANDREAS'), "2004: San Andreas, com um estado inteiro para explorar."),
  (S('years', a=2004, b=2008, big='GTA IV'), "2008: GTA 4, mais realista e mais sério."),
  (S('years', a=2008, b=2013, big='GTA V'), "2013: GTA 5, com três protagonistas. Ele ficou 13 anos no topo."),
  (S('years', a=2013, b=2026, big='GTA VI'), "2026: GTA 6. A volta para Vice City, agora no estado de Leonida."),
  (S('cta', html='QUAL FOI O<br><span class="yl">SEU PRIMEIRO?</span>', btn='COMENTA AQUI 👇'), "Qual foi o seu primeiro GTA? Comenta aqui e segue o Caos Insano."),
]
REELS['quiz'] = [
  (S('title', html='SÓ FÃ<br><span class="cy">DE VERDADE</span><br>ACERTA <span class="yl">3/3</span>', size=170), "Só fã de verdade de GTA 6 acerta as três. Valendo!"),
  (S('check', lbl='PERGUNTA 1', items=[('A) FLÓRIDA', 1), ('B) CALIFÓRNIA', 0), ('C) TEXAS', 0)], ask=1), "Pergunta um: Leonida é inspirada em qual estado americano? Flórida, Califórnia ou Texas?"),
  (S('check', lbl='PERGUNTA 1', items=[('A) FLÓRIDA', 1), ('B) CALIFÓRNIA', 0), ('C) TEXAS', 0)], fast=1), "Resposta: Flórida."),
  (S('check', lbl='PERGUNTA 2', items=[('A) SANTOS', 0), ('B) CAMINOS', 1), ('C) DUVAL', 0)], ask=1), "Pergunta dois: qual o nome completo da protagonista? Santos, Caminos ou Duval?"),
  (S('check', lbl='PERGUNTA 2', items=[('A) SANTOS', 0), ('B) CAMINOS', 1), ('C) DUVAL', 0)], fast=1), "Resposta: Lucia Caminos."),
  (S('check', lbl='PERGUNTA 3', items=[('A) 7 ANOS', 0), ('B) 10 ANOS', 0), ('C) 13 ANOS', 1)], ask=1), "Pergunta três: quantos anos separam o GTA 5 do GTA 6? Sete, dez ou treze?"),
  (S('check', lbl='PERGUNTA 3', items=[('A) 7 ANOS', 0), ('B) 10 ANOS', 0), ('C) 13 ANOS', 1)], fast=1), "Resposta: treze anos."),
  (S('cta', html='QUANTAS<br><span class="yl">VOCÊ ACERTOU?</span>', btn='COMENTA AQUI 👇'), "Quantas você acertou? Comenta aqui e segue o Caos Insano."),
]
# ---- BATERIA 2 (18/11) — fatos do site oficial da Rockstar (Ultimate Edition, Vintage Vice City Pack, loja, vídeos) e cobertura da prévia para criadores.
REELS['vercetti'] = [
  (S('title', html='O NOME<br><span class="yl">VERCETTI</span><br><span class="cy">VOLTOU</span>', size=180), "O nome Vercetti voltou no GTA 6. E foi a própria Rockstar que colocou."),
  (S('rank', n=1, html='VERCETTI<br><span class="yl">ESTATE</span>', sub='Os revólveres Hawk e Little Morgan da Ultimate Edition vêm "da Vercetti Estate", segundo a Rockstar.', sky=1), "Na Ultimate Edition, os revólveres Hawk e Little Morgan vêm da Vercetti Estate, a mansão Vercetti, segundo a descrição oficial."),
  (S('rank', n=2, html='A CAMISA DE<br><span class="cy">PALMEIRAS</span>', sub='Um padrão de arma inspirado na camisa do Tommy Vercetti.'), "Tem até um padrão de arma inspirado na camisa de palmeiras do Tommy Vercetti, o protagonista de Vice City."),
  (S('rank', n=3, html='ANOS 80<br><span class="yl">DE VOLTA</span>', sub='Pacote Vintage Vice City: terno de linho pastel para o Jason e vestido vermelho de paetê para a Lucia.', sky=1), "E o pacote Vintage Vice City traz terno de linho pastel para o Jason e vestido vermelho de paetê para a Lucia."),
  (S('cta', html='O TOMMY<br><span class="yl">APARECE?</span>', btn='COMENTA AQUI 👇'), "Isso não confirma que o Tommy aparece no jogo. Mas o nome dele já está lá. O que você acha? Comenta aqui."),
  (S('subs'), "Se inscreve no canal e segue a gente no TikTok: arroba caos insano br."),
]
REELS['ultimate'] = [
  (S('title', html='O QUE VEM NA<br><span class="yl">ULTIMATE</span><br><span class="cy">EDITION</span>', size=170), "O que vem na Ultimate Edition do GTA 6? Seis coisas, direto do site da Rockstar."),
  (S('rank', n=1, html='GROTTI<br><span class="yl">CHEETAH 95</span>', sub='O esportivo clássico dos anos 90, com pintura retrô.', sky=1), "Um: o Grotti Cheetah 95, o esportivo clássico dos anos 90."),
  (S('rank', n=2, html='BUGGY<br><span class="cy">OFF-ROAD</span>', sub="Dominator 67 para as trilhas de Mount Kalaga, com garagem em Watson Bay."), "Dois: um buggy off-road para as trilhas de Mount Kalaga, com garagem própria em Watson Bay."),
  (S('rank', n=3, html='LANCHA<br><span class="yl">SQUALO</span>', sub='Rosa e azul, em Washington Beach, com caixa de explosivos.', sky=1), "Três: a lancha Squalo, rosa e azul, em Washington Beach. E vem com uma caixa de explosivos."),
  (S('rank', n=4, html='50+<br><span class="cy">TATUAGENS</span>', sub='Estúdio Electric Fang, com tatuagens criadas pelo coletivo FAILE.'), "Quatro: o estúdio Electric Fang, com mais de 50 tatuagens criadas pelo coletivo de artistas FAILE."),
  (S('rank', n=5, html='OFICINA<br><span class="yl">OFF-ROAD</span>', sub="One-Eyed Willie's, em Lake Leonida: modificações e pintura à mão.", sky=1), "Cinco: a oficina One-Eyed Willie's, em Lake Leonida, com modificações off-road e pintura feita à mão."),
  (S('rank', n=6, html='CARROS<br><span class="cy">ABANDONADOS</span>', sub='Missões do colecionador Wyman para restaurar clássicos.'), "Seis: missões do colecionador Wyman para achar carros abandonados e restaurar."),
  (S('cta', html='VALE A<br><span class="yl">PENA?</span>', btn='COMENTA AQUI 👇'), "Vale a pena pegar a Ultimate? Comenta aqui e segue o Caos Insano."),
  (S('subs'), "Se inscreve no canal e segue a gente no TikTok: arroba caos insano br."),
]
REELS['bairros'] = [
  (S('title', html='8 LUGARES<br><span class="cy">QUE A ROCKSTAR</span><br><span class="yl">JÁ CITOU</span>', size=150), "Oito lugares de Leonida que a Rockstar já citou no material oficial."),
  (S('map', lbl='VICE CITY E ARREDORES', pins=['Ocean Beach', 'Shore Drive', 'Washington Beach', 'Watson Bay', 'Stockyard', 'Gambit Bay', 'Lake Leonida', 'Southside']), "Ocean Beach, Shore Drive, Washington Beach, Watson Bay, Stockyard, Gambit Bay, Lake Leonida e Southside Vice City."),
  (S('rank', n=1, html='OCEAN<br><span class="yl">BEACH</span>', sub='Onde fica uma das garagens da edição especial.', sky=1), "Ocean Beach é onde fica uma das garagens da edição especial, pertinho da areia."),
  (S('rank', n=2, html='STOCK<br><span class="cy">YARD</span>', sub='Bairro de loja de streetwear e de estúdio de tatuagem.'), "Stockyard tem loja de streetwear e o estúdio de tatuagem mais famoso da região."),
  (S('rank', n=3, html='SOUTH<br><span class="yl">SIDE</span>', sub='Área de uma das gangues mais barulhentas de Vice City.', sky=1), "E Southside Vice City é a área de uma das gangues mais barulhentas da cidade, segundo a Rockstar."),
  (S('cta', html='QUAL VOCÊ<br><span class="cy">VISITA</span><br>PRIMEIRO?', btn='COMENTA AQUI 👇'), "Qual você visita primeiro? Comenta e segue o Caos Insano."),
  (S('subs'), "Se inscreve no canal e segue a gente no TikTok: arroba caos insano br."),
]
REELS['macca'] = [
  (S('title', html='LEONIDA TEM<br><span class="yl">PROGRAMA</span><br><span class="cy">DE TV</span>', size=170), "Leonida tem até programa de TV famoso. E a Rockstar fez produto de verdade dele."),
  (S('rank', n=1, html='MACCA<br><span class="yl">THE GATOR</span>', sub='Um jacaré, personagem do programa de TV de sucesso em Leonida.', sky=1), "Macca the Gator é um jacaré, personagem de um programa de TV de sucesso dentro do jogo."),
  (S('rank', n=2, html='CHUNKEE<br><span class="cy">THE MANATEE</span>', sub='Um peixe-boi, outro personagem da TV de Leonida.'), "Chunkee the Manatee é um peixe-boi, outro personagem da TV de Leonida."),
  (S('rank', n=3, html='GOODTIME<br><span class="yl">STATE</span>', sub='É o apelido de Leonida no material oficial.', sky=1), "E Leonida tem apelido: Goodtime State, o estado da diversão."),
  (S('rank', n=4, html='VIROU<br><span class="cy">PRODUTO REAL</span>', sub='A loja da Rockstar tem uma caixa de colecionador inspirada no Macca.'), "Na vida real, a loja da Rockstar lançou uma caixa de colecionador inspirada no Macca, com estatueta, pôster com o mapa de Leonida e mais."),
  (S('cta', html='TIME<br><span class="yl">MACCA</span> OU<br><span class="cy">CHUNKEE?</span>', btn='COMENTA AQUI 👇'), "Time Macca ou time Chunkee? Comenta aqui."),
  (S('subs'), "Se inscreve no canal e segue a gente no TikTok: arroba caos insano br."),
]
REELS['trilha'] = [
  (S('title', html='A MÚSICA<br><span class="cy">DO TRAILER</span><br><span class="yl">FINAL</span>', size=170), "Qual é a música do trailer de lançamento do GTA 6?"),
  (S('song', lbl='TRAILER DE LANÇAMENTO', t='FLOWER IN A HURRICANE', a='Justice feat. Tame Impala, SZA e King Gizzard'), "Flower in a Hurricane, do Justice, com Tame Impala, SZA e King Gizzard and The Lizard Wizard."),
  (S('rank', n=1, html='JUSTICE<br><span class="cy">FEZ A TRILHA</span>', sub='A dupla francesa compõe a trilha original do jogo.', sky=1), "E o Justice, a dupla francesa de música eletrônica, é quem compõe a trilha original do jogo."),
  (S('song', lbl='TRAILER 1 · TRAILER 2', t='TOM PETTY · POINTER SISTERS', a='Love Is a Long Road · Hot Together'), "Os outros trailers usaram Love Is a Long Road, do Tom Petty, e Hot Together, das Pointer Sisters."),
  (S('rank', n=2, html='DÁ PRA<br><span class="yl">OUVIR JÁ</span>', sub='O site oficial tem a trilha e algumas rádios do jogo para ouvir.'), "E o site oficial já tem a trilha e algumas rádios do jogo para ouvir antes de jogar."),
  (S('cta', html='QUAL A<br><span class="cy">MELHOR?</span>', btn='COMENTA AQUI 👇'), "Qual dessas é a melhor? Comenta aqui e segue o Caos Insano."),
  (S('subs'), "Se inscreve no canal e segue a gente no TikTok: arroba caos insano br."),
]
REELS['preview'] = [
  (S('title', html='O QUE OS<br><span class="cy">CRIADORES</span><br><span class="yl">VIRAM</span>', size=170), "O que os criadores de conteúdo viram dentro da Rockstar antes de todo mundo?"),
  (S('rank', n=1, html='ROCKSTAR<br><span class="cy">NORTH</span>', sub='Em julho, criadores foram ao estúdio em Edimburgo, na Escócia.', sky=1), "Em julho, criadores foram ao estúdio Rockstar North, em Edimburgo, na Escócia."),
  (S('rank', n=2, html='TEVE<br><span class="yl">BRASILEIRO</span>', sub='Entre eles, segundo a imprensa: TGG, Davy Jones, El Rubius e Mike ShowSha.'), "Segundo a imprensa, estavam lá TGG, o brasileiro Davy Jones, El Rubius e Mike ShowSha."),
  (S('rank', n=3, html='SEM<br><span class="cy">JOGAR</span>', sub='A prévia foi só para assistir, e os celulares ficaram recolhidos.', sky=1), "Mas ninguém jogou. A prévia foi só para assistir, e os celulares ficaram recolhidos."),
  (S('rank', n=4, html='ESTREIA<br><span class="yl">NA NETFLIX</span>', sub='As reações só saíram depois do especial "An Extended Look", em 27 de agosto.'), "As reações só puderam sair depois do especial An Extended Look, que estreou em 27 de agosto."),
  (S('rank', n=5, html='TUDO<br><span class="cy">NO PS5</span>', sub='Segundo a Rockstar, o especial foi capturado inteiro dentro do jogo, no PS5.', sky=1), "E segundo a Rockstar, esse especial foi capturado inteiro dentro do jogo, no PS5."),
  (S('cta', html='AMANHÃ<br><span class="yl">É A NOSSA VEZ</span>', btn='SEGUE O CAOS INSANO →'), "Agora é a nossa vez. Segue o Caos Insano que a gente traz tudo do lançamento."),
  (S('subs'), "Se inscreve no canal e segue a gente no TikTok: arroba caos insano br."),
]
SFX = {'num': [(.15, 'riser', .5), (1.45, 'impact', .7)], 'years': [(.3, 'tick', .6), (1.6, 'impact', .7)], 'delay': [(.3, 'stamp', .6), (1.2, 'stamp', .6), (2.1, 'chime', .7)],
       'rank': [(.05, 'impact', .7)], 'map': [(.3, 'pop', .6), (.65, 'pop', .6), (1.0, 'pop', .6), (1.35, 'pop', .6)], 'song': [(.2, 'swipe', .6)], 'cta': [(.1, 'chime', .8)], 'subs': [(.5, 'pop', .7), (1.5, 'chime', .7), (2.3, 'pop', .7), (2.45, 'chime', .6)], 'check': [(.35, 'pop', .6), (.85, 'pop', .6), (1.35, 'pop', .6)], 'title': [(.1, 'impact', .8)]}

def main():
    nome, out = sys.argv[1], sys.argv[2]; trilha = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '../trilhas/mk_173.mp3')
    beats, caps, voz, fx, t = [], [], [], [], 0.0
    for i, (b, fala) in enumerate(REELS[nome]):
        st = t; vt = t + (.2 if i == 0 else .08)
        for fr in [f for f in re.split(r'(?<=[.?!:])\s+', fala) if f.strip()]:
            a = NA.tts(NA.falar(fr)); voz.append((vt, a)); d = len(a) / NA.SR
            ws = fr.split(); ch = [ws[k:k + 4] for k in range(0, len(ws), 4)]; tt = vt
            for c in ch:
                cd = d * len(c) / len(ws); caps.append([round(tt, 3), round(tt + cd, 3), ' '.join(c)]); tt += cd
            vt += d + .03
        dur = max(1.8, vt - st + .15); beats.append(dict(t0=round(st, 3), t1=round(st + dur, 3), **b))
        fx.append((st, 'whoosh' if i else 'impact', .5 if i else .7)); fx += [(st + d_, n, g) for d_, n, g in SFX.get(b['shot'], [])]
        t = st + dur
    DUR = t + .3; beats[-1]['t1'] = DUR
    for k in range(len(caps) - 1): caps[k][1] = max(caps[k][1], min(caps[k + 1][0], caps[k][1] + .3))
    html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="caos.css"></head><body><div id="v"></div>
<script>const BEATS={json.dumps(beats, ensure_ascii=False)};window.CAPS={json.dumps(caps, ensure_ascii=False)};const DUR={DUR:.3f};function setTimes(){{}}</script>
<script src="caos_engine.js"></script><script>R(0)</script></body></html>'''
    hp = os.path.join(HERE, f'short_{nome}.html'); open(hp, 'w').write(html)
    SR = NA.SR; N = int(DUR * SR) + SR; V = np.zeros(N, np.float32); F = np.zeros(N, np.float32)
    for st, a in voz: i = int(st * SR); V[i:i + len(a)] += a[:N - i]
    for st, n, g in fx: a = NA.load(n); i = int(st * SR); F[i:i + len(a)] += g * a[:N - i]
    tmp = f'/tmp/caos_{nome}'; os.makedirs(tmp, exist_ok=True)
    sf.write(f'{tmp}/voz.wav', V[:int(DUR * SR)], SR); sf.write(f'{tmp}/fx.wav', F[:int(DUR * SR)], SR); json.dump([], open(f'{tmp}/t.json', 'w'))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/voz.wav', '-i', f'{tmp}/fx.wav', '-stream_loop', '-1', '-i', trilha, '-filter_complex',
        f"[2:a]atrim=0:{DUR:.2f},asetpts=PTS-STARTPTS,aformat=sample_rates={SR}:channel_layouts=mono,volume=0.3,afade=t=in:d=0.3,afade=t=out:st={DUR-1.5:.2f}:d=1.5[m];"
        f"[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=300[md];[1:a]volume=0.6[f];[v1][f][md]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5,aformat=channel_layouts=stereo[a]",
        '-map', '[a]', '-ar', str(SR), f'{tmp}/mix.wav'], check=True)
    print('duração', round(DUR, 2), 'telas', len(beats))
    subprocess.run(['node', os.path.join(MOT, 'render_motion.js'), hp, os.path.abspath(os.path.join(_cwd, out)), f'{DUR:.2f}', '30', f'{tmp}/t.json', f'{tmp}/mix.wav'], check=True, cwd=MOT)
if __name__ == '__main__': main()
