# Busca no executor

Procedimento técnico para o assistente. A pessoa faz um pedido natural. O mecanismo adotado é [QMD 2.8.3](https://github.com/tobi/qmd/releases/tag/v2.8.3), executado por [scripts/search.py](../../../../scripts/search.py). O helper mantém a configuração e o índice desta cópia em .local/search/, excluído do Git. Não instala serviço nem agenda execução.

## Preparação inicial e retomada

Requer Python 3.10+, Node 22+ e npm. No macOS, a documentação do QMD recomenda SQLite do Homebrew com extensões. Confira recursos e rede antes de instalar. Execute na raiz da cópia:

```sh
python3 scripts/search.py setup
```

O [onboarding](../../brain-onboarding/SKILL.md) é orientado pelo AGENTS.md antes de usar a base. O comando é idempotente: confere dependências, versão instalada, arquivo completo do modelo e índice desta cópia. Se já estiverem presentes, retorna sem reinstalação ou novo teste. Quando faltar preparação, instala o QMD fixado dentro de .local/search/, executa um teste vetorial fictício temporário e indexa knowledge/, sem READMEs. O teste baixa e carrega o modelo mesmo numa base vazia, sem colocar o exemplo em inbox/ ou knowledge/. O resultado só declara ready depois de recuperar o registro fictício e preparar o índice real. Embeddings usam o modelo padrão embeddinggemma-300M-Q8_0 (cerca de 300 MB), baixado na primeira preparação, inclusive sem notas. Modelos e índice ficam neste executor, não são enviados a uma API de embeddings e não entram no Git. O npm resolve as dependências transitivas durante a preparação; esta prova fixa o QMD, não toda a árvore de dependências.

Para diagnóstico sem instalação, use `python3 scripts/search.py check`. Para repetir o teste com recursos já presentes, use `python3 scripts/search.py setup --verify`. São operações do assistente. A checagem rápida não prova novamente o carregamento do modelo a cada execução; falha posterior exige nova verificação, sem uso de resultados antigos. O cache npm também fica nesta cópia, e a política de rede do ambiente é preservada.

## Consultar e atualizar

```sh
python3 scripts/search.py search "Onde estamos perdendo o histórico quando o atendimento troca de equipe?"
python3 scripts/search.py lexical "Alfa"
python3 scripts/search.py update
python3 scripts/search.py status
```

search usa uma consulta vetorial tipada (`qmd query 'vec: …' --no-rerank`); lexical usa BM25. O comando vsearch desta versão também carrega expansão por LLM, por isso não é usado pelo helper. A consulta tipada dispensa esse modelo e o reranker. Ambas retornam JSON com arquivos, trechos e pontuações. Não são respostas finais: abra o arquivo atual e cite a evidência. O helper faz uma varredura de atualização antes de buscar e só prossegue se ela concluir. A consulta semântica também completa os embeddings pendentes. Falha interrompe a busca, sem fallback silencioso. update serve para mudanças feitas pela curadoria, Obsidian ou Git. Repetir a atualização sem mudanças deve manter os mesmos documentos.

A coleção cobre apenas conhecimento aceito. Incluir uma entrada exige curadoria; copiar um arquivo para inbox/ não inicia processo. Domínios são conferidos na nota recuperada; QMD 2.8.3 não implementa o filtro de propriedades planas adotado pelo Brain. Acesso a públicos diferentes exige repositórios e índices separados. Não use similaridade como confirmação de fatos ou como limite de acesso.

Na consulta tipada, a pontuação ordena candidatos e pode dar 1 ao primeiro colocado mesmo quando ele não responde à pergunta. Não a interprete como probabilidade de acerto. Se nenhuma nota sustentar o que foi perguntado, informe a ausência; não force uma resposta a partir do primeiro resultado.

O índice é reconstruível, mas contém conteúdo privado. Após remoções, a atualização deixa de retornar os documentos removidos; ela não é uma comprovação de apagamento físico de todas as páginas do banco. Para descartar o índice ou os originais, use o procedimento de retenção do executor. Não reutilize este estado em outro cliente.

## Outro executor

Prepare ferramentas e modelos naquele ambiente e execute setup novamente. Receba as notas por Git, atualize o índice e confira os arquivos usados. Não copie bancos ou credenciais para o repositório. Persistência entre tarefas cloud, acesso aos conectores, latência e volume precisam de prova no ambiente escolhido; um teste nesta máquina não valida esses pontos.
