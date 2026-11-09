# Histórias Zeey geradas por código

Três vídeos verticais com oficina (38 s), confeitaria (35 s) e serviços (36 s). Cada um mostra um problema concreto, a consequência, o fluxo de solução, uma objeção e o papel da pessoa na decisão. `cena.py` cria os cenários, personagens e Z em 3D no Blender; `filmes_v2.py` compõe cenas 3D com interfaces animadas, locução brasileira, trilha e legendas. Os arquivos finais são MP4 de 540 × 960 a 15 fps.

No celular, abra **Actions → Animacao 3D Zeey por codigo → Run workflow**. Baixe o artefato `zeey-tres-historias-v2` quando terminar. Não há API paga de geração. O workflow requer rede para a voz Edge TTS; GitHub Actions pode impor limites. A execução do workflow ainda não foi validada no GitHub, embora a geração local e a decodificação integral dos três MP4 tenham sido concluídas.

Num computador Linux com Blender, FFmpeg, Pillow e edge-tts:

```bash
for n in 0 1 2; do blender -b --threads 2 --python animacao/codigo3d/cena.py -- "$n"; done
python animacao/codigo3d/filmes_v2.py
```

Saída: `animacao/codigo3d/v2/01_oficina.mp4`, `02_confeitaria.mp4`, `03_servicos.mp4`. Arquivos `_sem_audio.mp4` são intermediários.

Esta é uma primeira versão narrativa. A atuação 3D e o desenho dos três ambientes ainda podem ganhar mais variedade. Revise o resultado antes de publicar; nenhuma taxa de retenção é garantida.
