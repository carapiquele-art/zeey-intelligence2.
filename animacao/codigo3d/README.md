# Três vídeos Zeey feitos por código

Os personagens, o Z, três cenários (oficina, confeitaria, escritório), movimentos, câmera e cartões de informação são criados por `cena.py` no Blender. Não há imagens paradas usadas como cenas. `finalizar.py` transforma os quadros em MP4 e chama `../legendar.py` para voz em português, trilha e legendas sincronizadas.

## Gerar no GitHub

Abra a aba **Actions** do repositório, escolha **Animacao 3D Zeey por codigo**, clique em **Run workflow**. Quando terminar, baixe o artefato `zeey-tres-videos-3d` com três MP4. O workflow instala Blender e FFmpeg no runner, sem API de vídeo paga. A voz Edge TTS exige rede. A execução gratuita do GitHub Actions pode ter limites conforme a conta.

## Gerar no computador Linux

Instale Blender, FFmpeg e `edge-tts==7.3.1`. Na raiz do repositório:

```bash
for n in 0 1 2; do blender -b --threads 2 --python animacao/codigo3d/cena.py -- "$n"; done
python animacao/codigo3d/finalizar.py
```

Os arquivos saem em `animacao/saida/Zeey_01.mp4`, `Zeey_02.mp4`, `Zeey_03.mp4`. A renderização original é 480 × 832 a 12 fps; `legendar.py` entrega 1080 × 1920/30 fps com ampliação/interpolação, sem criar detalhe nativo 1080p. Revise visualmente os vídeos antes de publicar; a versão inicial mostra o fluxo, e a atuação dos personagens ainda pode ser refinada.

O Blender não está incluído no script Termux. Para celular, use Actions e baixe os MP4 prontos. Não há necessidade de instalar Blender no telefone.
