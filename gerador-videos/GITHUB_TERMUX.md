# Rodar no Termux e no GitHub

O projeto gera vídeos a partir das histórias em roteiros.json. Para acrescentar histórias, adicione objetos ao final da lista, cada um com titulo e quatro textos em cenas. No modo vigiar, o agente detecta mudanças em até 30 segundos e produz itens novos. Ele não pesquisa, escreve novas histórias sozinho, publica nem roda enquanto o Termux ou o processo estiver encerrado. Mantenha a ordem dos roteiros já gerados. Pressione Ctrl+C para parar.

No Termux, execute estes comandos depois da inclusão dos arquivos no repositório:

```bash
pkg install -y git
git clone https://github.com/carapiquele-art/zeey-intelligence2..git "$HOME/zeey-intelligence2"
cd "$HOME/zeey-intelligence2/gerador-videos"
bash iniciar-termux.sh
```

A instalação de pacotes requer rede. O primeiro uso pode consumir tempo e armazenamento; o espaço disponível e a memória atuais do telefone não foram verificados. Os vídeos são guardados na pasta videos dentro do Termux. Transferir para a galeria exige acesso Android ao armazenamento compartilhado; isso ainda não foi configurado neste aparelho.

No GitHub, o arquivo .github/workflows/videos.yml deve ficar na raiz do repositório e a pasta do agente em gerador-videos/. Após integração, use Actions → Gerar vídeos Zeey → Run workflow. O resultado aparece como artefato videos-zeey, se o job e o serviço de voz concluírem com sucesso. Nada foi executado no GitHub ainda. Custos e disponibilidade de minutos do Actions dependem da conta.

Os MP4 incluídos no pacote são versões de revisão com cenas estáticas, locução gerada e texto sobreposto. É necessário avaliar o resultado criativo, a pronúncia e a legibilidade antes de publicar.
