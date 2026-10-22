---
name: brain-onboarding
description: Preparar ou conferir o Second Brain no executor antes de iniciar ou retomar o uso da base. Acionar também quando faltar instalação, modelo ou índice, ou houver falha na preparação da busca.
---

# Preparar o ambiente

Siga [AGENTS.md](../../../AGENTS.md). Trabalhe na cópia destinada à tarefa; confira o destino antes de operar. Esta preparação é técnica e independe da entrevista de contexto. O assistente executa os comandos; a pessoa não precisa conhecer ou nomear esta skill.

Execute na raiz da cópia:

```sh
python3 scripts/search.py setup
```

O helper confere os pré-requisitos e os recursos reais desta cópia. Se já estiverem presentes, retorna rapidamente sem reinstalar, baixar modelos ou repetir o teste. Quando faltar preparação, instala o QMD fixado, carrega o modelo de embeddings, confere as buscas vetorial e híbrida num teste fictício e prepara o índice do conhecimento aceito. O teste usa um índice temporário fora das notas reais, compartilha apenas o cache do modelo e é removido ao terminar. Instalação, cache npm, modelo e índices ficam em .local/, fora do Git.

Confira o código de saída e o resultado. Só apresente o ambiente como pronto depois de `ready: true`. Ao retomar uma conversa no mesmo executor, aproveite a preparação já conferida; antes de uma consulta, o fluxo de busca continua atualizando o conhecimento indexado. Não mantenha outro cadastro ou arquivo de aprovação para isso.

Se o ambiente mudou, houve falha de execução ou a pessoa pediu nova verificação, repita o teste com `python3 scripts/search.py setup --verify`. Uma conferência sem instalação está disponível em `python3 scripts/search.py check`. O padrão é busca híbrida com um modelo de embeddings. Se a tarefa for usar re-ranking, prepare-o com `python3 scripts/search.py setup --rerank`; esse modo verifica também o modelo adicional em um teste temporário. A [referência de busca](../brain-query/references/search.md) explica requisitos e limites.

Se faltar Python, Node, npm, espaço, rede ou permissão, informe o bloqueio concreto e resolva o que estiver ao alcance da tarefa. Solicite uma ação humana somente quando necessária; não altere políticas de rede nem instale ferramentas globais para contornar o bloqueio. Preserve notas existentes e não apresente leitura textual como busca semântica preparada. Se a preparação continuar pendente, informe a limitação antes de prosseguir com o que independe dela.

A preparação não conecta contas, coleta fontes, entrevista a pessoa, publica dados ou cria rotinas. Depois da checagem, siga o encaminhamento do AGENTS.md para atender ao pedido original. Se ele for começar ou retomar a base, a preparação técnica é seguida pela conversa de contexto; não a apresente como encerramento da solicitação. Não acrescente atividades que a pessoa não pediu. Cada executor tem sua própria preparação e seu próprio índice.
