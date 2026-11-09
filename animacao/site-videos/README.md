# Três vídeos Zeey no visual do site

Três histórias animadas por código: Lia (beleza, Instagram → reserva), Beto (serviço local, busca → pedido) e Nina (projetos, dúvida → orçamento). O Z é um personagem que reúne dados e responde a objeções. Visual claro, azul #075bff, fonte Switzer e interfaces que mostram o funcionamento. Voz brasileira, balões de mensagem, legendas e música.

O workflow **Videos Zeey — visual do site** na aba Actions gera os três MP4 e os oferece como artefato. Ele usa Remotion, Chromium, FFmpeg e Edge TTS, sem API de vídeo paga. A geração foi validada neste ambiente; a execução do workflow no GitHub ainda precisa ser verificada. O repositório inclui o código e reutiliza a fonte/trilha em `animacao/`. Os vídeos locais renderizados têm 720 × 1280 a 20 fps.

Para rodar num computador Linux: instale Node 22+, Chromium e FFmpeg; em `animacao/site-videos`, rode `npm install`, `python -m pip install edge-tts==7.3.1`, `mkdir -p public out`, copie as fontes e a trilha de `../fonts` e `../assets`, rode `python gerar_voz.py` e renderize `ZeeyLia`, `ZeeyBeto`, `ZeeyNina` com Remotion. Pelo celular, use o workflow.
