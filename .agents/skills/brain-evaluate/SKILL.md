---
name: brain-evaluate
description: Experimentar um fluxo do projeto com um caso fictício, observar o resultado e conduzir sua conferência. Usar para avaliar skills com exemplos leves, extensíveis a novas tarefas.
---

# Avaliar um fluxo

Siga [AGENTS.md](../../../AGENTS.md). Esta skill conduz a avaliação; a skill indicada no caso executa a tarefa. Os casos e o preparador pertencem a este pacote, sem cadastro de casos na raiz.

Liste os casos com `python3 .agents/skills/brain-evaluate/scripts/preparar_caso.py --list`. Escolha pelo pedido da pessoa; com apenas um caso disponível, use-o. Pergunte qual deseja somente se houver ambiguidade entre os casos existentes.

Prepare o caso com o mesmo script, passando seu nome. Ele devolve uma pasta nova em .local/ensaios/, com as fontes fictícias, os pontos de conferência e a skill avaliada. Trabalhe nessa pasta e siga TASK.md. Não use o perfil ou as notas reais como entradas do ensaio.

Execute a tarefa indicada, sem substituir a skill avaliada por uma resposta de referência. Mostre a fonte e o resultado que realmente foi produzido; se a tarefa cria um arquivo, abra o arquivo salvo. Use os critérios do caso para conduzir a conferência com a pessoa. Critérios sobre perguntas ou interação precisam da conversa observada; sem ela, deixe esse ponto pendente.

Se houver uma divergência, preserve a versão anterior no ensaio, corrija o ponto autorizado e compare novamente. Se não houver, encerre após a conferência. Não invente defeitos, conferências ou novas execuções. Outra sessão é opcional; não é necessário pontuar, criar manifesto ou relatório. Ao terminar, indique o caminho do ensaio e retome a cópia real.

Para acrescentar uma avaliação, adicione um JSON em [assets](assets/) com title, skill, prompt, files e checks. A entrada deve ser fictícia, a skill deve existir no projeto e os critérios devem descrever resultados observáveis. O script descobre os casos disponíveis; não é preciso editar listas no código. A quantidade de critérios depende da tarefa; os exemplos da aula usam poucos pontos.
