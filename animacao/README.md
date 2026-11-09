# Zeey — animação e legenda V2

Mantém o modelo visual do teste com personagens 3D e Z. O novo acabamento usa a fonte da marca, blocos de legenda curtos com pontuação e palavra falada azul, faixa de contraste e margens para celular. A exportação é 1080 × 1920 / 30 fps por ampliação Lanczos e interpolação de movimento. Os trechos gerados originalmente têm 480 × 832 / 16 fps: a exportação não os transforma em detalhe nativo 1080p.

## Estado comprovado

O teste do ateliê de 7 segundos tem duas cenas animadas geradas, narração, trilha e legenda V2. A exportação e decodificação foram executadas. As outras cenas e os três filmes completos ainda dependem de geração. O Space gratuito bloqueou as novas tentativas por cota anônima esgotada; a mensagem foi confirmada na interface. Não se comprovou geração autenticada em conta do usuário nesta sessão.

## Termux

Atualize o repositório, entre em `animacao` e rode `bash iniciar-termux.sh`.

O script solicita um token **de leitura** da sua conta gratuita de Hugging Face. Crie-o em https://huggingface.co/settings/tokens e cole apenas quando o terminal pedir; o texto fica oculto. O token é verificado e salvo em `~/.config/zeey/hf_token`, com permissão restrita, fora do repositório. Não publique nem envie o token na conversa. Autenticar pode liberar mais cota gratuita, mas não garante disponibilidade para concluir todas as cenas. Nenhuma API de geração paga é configurada.

O processo gera uma cena por vez, preserva as concluídas e para quando o serviço falha. Para retomar: `.venv/bin/python gerar.py`. Para uma história: `.venv/bin/python gerar.py --historia 1` (1 oficina, 2 confeitaria, 3 ateliê). Para remover a credencial local, apague `~/.config/zeey/hf_token`.

Os resultados ficam em `saida/`; quando o acesso Android a Movies estiver disponível, uma cópia é feita em `Movies/Zeey`. A cópia não comprova indexação imediata pela Galeria. A geração requer internet e o serviço gratuito está sujeito a fila e cota. Fechar o Termux pode interromper o processo; ele não fica executando continuamente em servidor.

## Produção

`gerar.py` usa o Space cbensimon/wan2-2-fp8da-aoti-preview2 no Hugging Face, com autenticação padrão de Spaces. `legendar.py` prepara voz por edge-tts, legenda ASS sincronizada com tempos de palavra e exportação FFmpeg. As duas primeiras cenas do ateliê já estão incluídas para evitar gerá-las novamente. Não há sincronização labial validada; a voz funciona como narração sobre a ação.
