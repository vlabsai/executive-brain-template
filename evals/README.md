# Evals da mentoria

Estes são ensaios leves para provar um conceito: fornecer uma entrada conhecida, observar o que a skill produziu e conferir alguns pontos. Um exemplo curto e uma conversa bastam para a aula. Não são uma certificação do assistente nem uma exigência para cada tarefa.

## Ensaio rápido na aula

Com o Codex aberto na cópia do projeto, peça:

> Leia evals/README.md e faça comigo o ensaio rápido de contexto inicial, usando apenas dados fictícios.

O Codex conduz três passos, sem exigir comandos de terminal do participante:

1. **Produzir:** prepare `contexto-inicial` com `scripts/evaluate.py prepare`, escolhendo uma pasta nova em `.local/evals/`. Use somente o `workspace/` criado e seu `TASK.md` para executar a skill inicial. Não copie o perfil real nem leia o gabarito para montar a resposta. O relato de Marina já contém o necessário para esse pequeno ensaio.
2. **Conferir juntos:** mostre o relato e o perfil realmente salvo, lado a lado na resposta. Pergunte ao participante se o resultado preservou **papel e responsabilidades**, **dificuldade e objetivo** e **origem e informações ausentes**. Não dê uma aprovação automática ao próprio texto.
3. **Corrigir, se preciso:** peça um ajuste específico. Preserve uma cópia do resultado anterior fora do workspace, aplique a correção e compare novamente com o relato. Registre apenas a diferença observada e a conferência efetivamente realizada. Não marque uma nova execução da skill se houve apenas edição do arquivo.

Marina é uma executiva fictícia usada somente no ensaio. Ao terminar, volte ao perfil real e use a mesma conferência. Se não houver erro, não é preciso inventar um defeito nem repetir a execução. Essa demonstração cabe em poucos minutos; não exige outra sessão, `review.json` ou relatório de avaliação.

## Outros exemplos disponíveis

Os mesmos três passos podem ser usados com estes casos:

| Cenário | Aprendizado | Resultado que precisa de conferência |
|---|---|---|
| contexto-inicial | Usar contexto e perguntar apenas o necessário | Perfil fiel ao relato e origem identificada |
| prazo-em-conflito | Separar fato de sugestão | Nota confirmada preservada; mudança pendente fora da base revisada |
| consulta-sem-orcamento | Reconhecer lacunas | Resposta com evidência, sem valor inventado |

## Opcional: repetir em outra sessão

Para investigar uma falha recorrente ou comparar uma mudança nas instruções, o mecanismo abaixo separa execução e revisão. O script confere arquivos; outra sessão ou pessoa julga o conteúdo. Esta parte não precisa ser feita durante a aula.

1. Prepare uma execução nova, fora da cópia do cliente. Por exemplo, a partir da raiz do projeto:

```sh
python3 scripts/evaluate.py prepare prazo-em-conflito --destination ../ensaio-prazo-01
```

2. Abra **somente `../ensaio-prazo-01/workspace/`** como projeto em outra sessão do Codex. Peça: **“Leia TASK.md e execute o exercício usando a skill indicada.”** O diretório contém instruções e dados sintéticos; perfil, fontes, notas e configurações reais do cliente não são copiados. O gabarito permanece fora da pasta de execução.
3. Ao terminar, preserve os arquivos e a conversa real. Na sessão de revisão, abra `../ensaio-prazo-01/`, leia `REVIEW.md`, confira as fontes e preencha `review.json`. Para avaliar como a interação ocorreu, forneça a conversa da execução; sem essa evidência, marque o critério como pendente.
4. Confira os artefatos e a revisão:

```sh
python3 scripts/evaluate.py check ../ensaio-prazo-01 --review ../ensaio-prazo-01/review.json
```

Sem `--review`, o script já confere os arquivos, mas mantém o resultado como `pending_review`. Arquivo existente ou JSON válido não basta para aprovar a resposta. O código de saída só é zero quando as verificações automáticas e todos os critérios revisados passam.

## O que fica registrado

- `workspace/`: instruções, fontes fictícias e resultado da execução.
- `manifest.json`: cenário, ligação com a aula, hashes iniciais e critérios; fora da pasta do executor.
- `REVIEW.md` e `review.json`: pedido e resultado da revisão.
- `report.json`: verificações automáticas, revisão e estado final.

Não reutilize a mesma pasta para outra tentativa. Uma nova execução preserva a anterior e permite comparar mudanças nas instruções. A separação de pastas organiza um ensaio; o mentor escolhe uma sessão independente para evitar que quem executou também produza seu próprio gabarito.

Se a revisão apontar erro, corrija a instrução responsável e prepare uma nova execução com o mesmo caso. Mantenha a tentativa anterior. O conserto pontual de uma saída demonstra uma correção; repetir o caso com a instrução ajustada permite observar se ela melhorou.

Os cenários validam o comportamento no recorte proposto. Não provam acesso do Dot, integração com calendário nem operação com dados reais. A criação/clonagem do repositório tem preparo técnico próprio no material do mentor; estas três evals não criam recursos externos.

Referência de autoria: [avaliação de skills na documentação oficial OpenAI](https://developers.openai.com/blog/eval-skills/). O mecanismo local usa casos curtos e conferência humana; não depende da plataforma de Evals ou de uma chave de API.
