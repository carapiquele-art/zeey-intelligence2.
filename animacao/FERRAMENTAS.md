# Ferramentas de vídeo conectadas ao projeto Zeey

Este projeto usa código e executáveis instalados, sem copiar o código-fonte inteiro de projetos externos para dentro do repositório. Isso mantém o clone viável no Termux. Os links abaixo foram verificados em 2026-11-09.

| Projeto | Função real na produção | Uso agora |
|---|---|---|
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Montagem, áudio, legendas e codificação MP4 | Instalado pelo `iniciar-termux.sh`; usado por `legendar.py` |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Animação programática a partir de HTML/CSS | Candidato para cenas gráficas futuras; requer Node 22+ e protótipo visual |
| [Remotion](https://github.com/remotion-dev/remotion) | Vídeo programático em React | Alternativa de composição, dependente de Node/Chromium; ainda não integrada ao render atual |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Transcrição de voz gravada | Útil quando houver diálogos gravados; legendas atuais usam os tempos da voz sintetizada |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Baixar referências permitidas | Pesquisa e revisão; não é gerador de cenas |
| [VoiceStudio](https://github.com/debpalash/VoiceStudio) | Interface de produção de voz | Alternativa de locução; não é requisito dos filmes atuais |

## Pipeline atual

`historias.json` define as cenas e falas. `gerar.py` solicita cenas animadas ao Space gratuito, preserva cada trecho concluído e interrompe ao encontrar erro ou cota. `legendar.py` cria voz, música, legendas e MP4 usando FFmpeg. `iniciar-termux.sh` instala o que o Termux precisa e solicita autenticação gratuita no Hugging Face.

Os repositórios acima são ferramentas, não bancos de vídeos prontos. Cloná-los não gera automaticamente personagens nem três filmes. A geração das cenas depende do serviço de vídeo e de sua disponibilidade; o projeto também pode receber cenas 3D renderizadas localmente. Nunca coloque token, senha ou arquivos de referência sem direitos de uso no GitHub.
