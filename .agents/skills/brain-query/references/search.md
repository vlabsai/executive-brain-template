# Busca no executor

Procedimento técnico para o assistente. A pessoa faz um pedido natural. O mecanismo adotado é [QMD 2.8.3](https://github.com/tobi/qmd/releases/tag/v2.8.3), executado por [scripts/search.py](../../../../scripts/search.py). O helper mantém a configuração e o índice desta cópia em .local/search/, excluído do Git. Não instala serviço nem agenda execução.

## Preparação inicial e retomada

Requer Python 3.10+, Node 22+ e npm. No macOS, a documentação do QMD recomenda SQLite do Homebrew com extensões. Confira recursos e rede antes de instalar. Execute na raiz da cópia:

```sh
python3 scripts/search.py setup
```

O [onboarding](../../brain-onboarding/SKILL.md) é orientado pelo AGENTS.md antes de usar a base. O comando é idempotente: confere dependências, versão instalada, arquivo completo do modelo e índice desta cópia. Se já estiverem presentes, retorna sem reinstalação ou novo teste. Quando faltar preparação, instala o QMD fixado dentro de .local/search/, verifica as buscas vetorial e híbrida num caso fictício temporário e indexa knowledge/, sem READMEs. O teste baixa e carrega o modelo mesmo numa base vazia, sem colocar o exemplo em inbox/ ou knowledge/. O resultado só declara ready depois de recuperar o registro fictício e preparar o índice real. Embeddings usam o modelo padrão embeddinggemma-300M-Q8_0 (cerca de 300 MB), baixado na primeira preparação, inclusive sem notas. Modelos e índice ficam neste executor, não são enviados a uma API de embeddings e não entram no Git. O npm resolve as dependências transitivas durante a preparação; esta prova fixa o QMD, não toda a árvore de dependências.

Para diagnóstico sem instalação, use `python3 scripts/search.py check`. Para repetir o teste com recursos já presentes, use `python3 scripts/search.py setup --verify`. São operações do assistente. A checagem rápida não prova novamente o carregamento do modelo a cada execução; falha posterior exige nova verificação, sem uso de resultados antigos. O cache npm também fica nesta cópia, e a política de rede do ambiente é preservada.

## Consultar e atualizar

```sh
python3 scripts/search.py search "Onde estamos perdendo o histórico quando o atendimento troca de equipe?" --terms "atendimento histórico"
python3 scripts/search.py lexical "Alfa"
python3 scripts/search.py update
python3 scripts/search.py status
```

search combina BM25 e busca vetorial com a fusão nativa RRF do QMD. A pergunta segue como `vec:`; `--terms` fornece os nomes, identificadores ou poucas palavras centrais para `lex:`. Preserve esses termos como a pessoa os informou, sem inventar sinônimos de entidades. Aspas permitem expressões exatas. Sem --terms, o helper usa o mesmo texto nos dois componentes; como BM25 exige todos os termos positivos, perguntas longas se beneficiam de termos concisos escolhidos pelo assistente.

A pergunta completa também segue como contexto de intenção, preservando o objetivo ao selecionar trechos e reordenar candidatos. As consultas tipadas dispensam o modelo local de expansão: o assistente já formula a pergunta e os termos. Não use vsearch nem o query sem prefixos para obter esse caminho. lexical continua disponível como consulta exclusivamente textual. Os comandos retornam JSON com arquivos, trechos e pontuações; abra a nota atual e cite a evidência antes de responder.

Antes de buscar, o helper atualiza a coleção e só prossegue se concluir; a busca híbrida também completa os embeddings pendentes. Falha interrompe a busca, sem fallback silencioso. update serve para mudanças feitas pela curadoria, Obsidian ou Git. Repetir a atualização sem mudanças mantém os documentos.

### Re-ranking opcional

Para comparar candidatos de uma pergunta difícil ou quando a pessoa solicitar uma busca mais cuidadosa, o assistente pode usar o re-ranking nativo:

```sh
python3 scripts/search.py setup --rerank
python3 scripts/search.py search "O que ficou definido na decisão DEC-0742?" --terms "DEC-0742" --rerank
```

A preparação adicional baixa e carrega o reranker padrão Qwen3 de cerca de 640 MB em um teste fictício, sem baixar o modelo de expansão. check --rerank confere os recursos desse modo; ready no modo padrão indica prontidão da busca híbrida, sem prometer o reranker. O re-ranking reavalia os candidatos e acrescenta custo à consulta; não confirma fatos nem substitui a abertura das notas. Quando solicitado, uma falha não provoca repetição silenciosa sem re-ranking.

A coleção cobre apenas conhecimento aceito. Incluir uma entrada exige curadoria; copiar um arquivo para inbox/ não inicia processo. Domínios são conferidos na nota recuperada; QMD 2.8.3 não implementa o filtro de propriedades planas adotado pelo Brain. Acesso a públicos diferentes exige repositórios e índices separados. Não use similaridade como confirmação de fatos ou como limite de acesso.

Na busca, a pontuação ordena candidatos; no modo sem re-ranking pode dar 1 ao primeiro colocado mesmo quando ele não responde à pergunta. Não a interprete como probabilidade de acerto. Se nenhuma nota sustentar o que foi perguntado, informe a ausência; não force uma resposta a partir do primeiro resultado.

O índice é reconstruível, mas contém conteúdo privado. Após remoções, a atualização deixa de retornar os documentos removidos; ela não é uma comprovação de apagamento físico de todas as páginas do banco. Para descartar o índice ou os originais, use o procedimento de retenção do executor. Não reutilize este estado em outro cliente.

## Outro executor

Prepare ferramentas e modelos naquele ambiente e execute setup novamente. Receba as notas por Git, atualize o índice e confira os arquivos usados. Não copie bancos ou credenciais para o repositório. Persistência entre tarefas cloud, acesso aos conectores, latência e volume precisam de prova no ambiente escolhido; um teste nesta máquina não valida esses pontos.
