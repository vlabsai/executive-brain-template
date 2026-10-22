---
name: brain-evaluate
description: Testar skills com casos fictícios durante a autoria ou manutenção dos fluxos. Usar quando os responsáveis pelo fluxo quiserem reproduzir uma tarefa, conferir o resultado e ajustar suas instruções.
---

# Avaliar um fluxo

Siga [AGENTS.md](../../../AGENTS.md). Este recurso atende à autoria e manutenção dos fluxos e é independente das tarefas cotidianas da base. Acione-o quando houver um pedido de teste dos responsáveis pelo fluxo. A skill indicada no caso executa a tarefa. Os casos e o preparador pertencem a este pacote, sem cadastro de casos na raiz.

Liste os casos com `python3 .agents/skills/brain-evaluate/scripts/preparar_caso.py --list`. Escolha pelo pedido da pessoa; com apenas um caso disponível, use-o. Pergunte qual deseja somente se houver ambiguidade entre os casos existentes.

Prepare o caso com o mesmo script, passando seu nome. Ele devolve uma pasta nova em .local/ensaios/, com as fontes fictícias, os pontos de conferência, as três skills de trabalho e os recursos comuns de leitura/busca. Modelos, índices, notas e preferências pessoais da cópia de origem não são copiados. Trabalhe nessa pasta e siga TASK.md. Não use o perfil ou as notas reais como entradas do ensaio.

Execute a tarefa indicada, sem substituir a skill avaliada por uma resposta de referência. Mostre a fonte e o resultado que realmente foi produzido; se a tarefa cria um arquivo, abra o arquivo salvo. Use os critérios do caso para conduzir a conferência com a pessoa. Critérios sobre perguntas ou interação precisam da conversa observada; sem ela, deixe esse ponto pendente.

Se houver uma divergência, preserve a versão anterior no ensaio, corrija o ponto autorizado e compare novamente. Se não houver, encerre após a conferência. Não invente defeitos, conferências ou novas execuções. Outra sessão é opcional; não é necessário pontuar, criar manifesto ou relatório. Ao terminar, indique o caminho do ensaio e retome a cópia real.

Nos casos do Alfa, curar-ata-alfa acompanha a proposta e sua incorporação após aceitação; consultar-alfa exercita a consulta com uma nota já revisada como entrada. Para testar curadoria e consulta em sequência, consulte também a nota que a curadoria acabou de produzir. Em uma sessão independente, forneça apenas o pedido, as regras, as skills de trabalho e as fontes; mantenha TASK.md, critérios e respostas de referência fora da pasta executora. Confira o resultado depois, sem antecipar o conteúdo esperado ao executor.

Para acrescentar uma avaliação, adicione um JSON em [assets](assets/) com title, skill, prompt, files e checks. A entrada deve ser fictícia, a skill deve existir no projeto e os critérios devem descrever resultados observáveis. O script descobre os casos disponíveis; não é preciso editar listas no código. A quantidade de critérios depende da tarefa; os casos fornecidos usam poucos pontos.

No caso conversar-contexto, files está vazio porque a fonte nasce da conversa. Use author_replies apenas como apoio do operador, fora da sessão executora: envie o relato em resposta à abertura e o OK somente depois de ver a síntese. Não antecipe a confirmação nem acrescente instruções para corrigir o comportamento durante o ensaio. Observe a conversa e os arquivos antes e depois do OK. O caso montar-contexto continua cobrindo o aproveitamento de um relato previamente conferido.

Para comparar somente a recuperação, prepare navegar-e-buscar e execute `python3 .agents/skills/brain-evaluate/scripts/comparar_busca.py CAMINHO_DO_ENSAIO`. O script aceita apenas as notas fictícias originais desse caso, prepara o índice e compara vetor, híbrida e híbrida com re-ranking nas mesmas perguntas. O JSON mostra posições e tempos observados, sem aprovar respostas ou acionar a skill avaliada. A primeira passagem pode baixar o reranker. São poucos exemplos de manutenção, não uma prova de escala ou uma etapa da pessoa usuária.

A [comparação local observada](references/busca-observada.md) registra o alcance da prova e a decisão sobre o modo padrão.
