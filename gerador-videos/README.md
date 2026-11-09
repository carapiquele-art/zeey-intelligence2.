# Fila automática de vídeos Zeey

O agente percorre 20 roteiros preparados, gera locução por cena com edge-tts, monta legendas visíveis e compõe vídeos verticais com prévias demonstrativas da Zeey. Salva MP4 em `videos/`, valida a decodificação e retoma sem sobrescrever os arquivos já concluídos. Os exemplos de interface são marcas fictícias. A geração é uma fila de produção baseada em roteiros, não criação autônoma ilimitada nem publicação automática.

No workspace atual, executar com o Python já preparado:

```bash
/workspace/zeey-criativo/.venv/bin/python /workspace/zeey-agente/agente.py --inicio 1 --limite 20
```

Para produzir apenas um: `--inicio 1 --limite 1`. O serviço de voz precisa de internet. FFmpeg e ffprobe devem estar instalados; instale as bibliotecas Python com `pip install -r requirements.txt`. Os arquivos da marca e das demonstrações estão em `assets/`. As peças usam imagens estáticas e cortes entre cenas; ainda não reproduzem toda a animação Remotion do primeiro vídeo. Revise narração, legibilidade e conteúdo antes de publicar. Esta versão é para o workspace atual; não configura Termux nem salva na galeria do telefone.

Para instalar em outro computador Linux, dentro da pasta extraída:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python agente.py --inicio 1 --limite 20
```

As fontes DejaVu estão incluídas na pasta `assets/`, acompanhadas da respectiva licença. Para gerar novamente um vídeo, mova ou remova previamente o MP4 correspondente.

Leia `GITHUB_TERMUX.md` para acompanhar a pasta, usar o Termux e configurar o disparo manual do GitHub Actions.
