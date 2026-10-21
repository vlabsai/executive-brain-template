# IA na rotina executiva · Template do Brain

Ponto de partida para aplicar os conceitos da [mentoria executiva](https://github.com/vlabsai/executive-ai-mentorship) a um problema real: lidar com fontes de informação, agenda, compromissos e trabalho diário.

O Brain é o projeto de aplicação. Este template organiza o conhecimento curado, suas origens e as rotinas que o Dot poderá coordenar no ambiente configurado para o cliente.

## Comece pequeno

1. Com o mentor, confira os acessos e combine o destino. Na aula, a skill de início do material da mentoria pode conduzir contexto, criação da cópia privada e clonagem. Também é possível usar **Use this template → Create a new repository**.
2. Siga [START_HERE.md](START_HERE.md) com o mentor.
3. Na aula 1, abra a pasta já preparada pelo mentor, leia as fontes e salve perfil, nota e registro da conferência no mesmo projeto. Amplie a base conforme os encontros.

Este é um modelo vazio. Nenhuma fonte está conectada, nenhum agendamento está salvo e nenhuma execução foi realizada. Não contém dados de clientes nem conteúdo do My Brain pessoal de Fabricio.

## Mapa

| Lugar | Para que serve |
|---|---|
| [AGENTS.md](AGENTS.md) | Regras únicas para tarefas de IA neste repositório |
| [profile/overview.md](profile/overview.md) | Problema prioritário, responsabilidades e contexto do executivo |
| [sources/catalog.md](sources/catalog.md) | Como cadastrar e conferir as fontes |
| [config/sources.json](config/sources.json) | Registro canônico de acesso, autoridade e atualização de cada fonte |
| [inbox/](inbox/README.md) | Material recebido e ainda não consolidado |
| [knowledge/](knowledge/README.md) | Conhecimento revisado, com origem |
| [commitments/source-map.md](commitments/source-map.md) | Onde consultar agenda e tarefas |
| [routines/](routines/README.md) | Instruções para consultas, curadoria e briefing |
| [.agents/skills/](.agents/skills/) | Fluxos guiados que perguntam o que falta e produzem os documentos |
| [runs/](runs/README.md) | Evidências de execução e revisão |
| [quality/acceptance.md](quality/acceptance.md) | Critérios para aceitar a primeira versão |
| [evals/](evals/README.md) | Exercícios fictícios para avaliar instruções em outra sessão |

## Começar por uma conversa

Abra a cópia privada como projeto no aplicativo. As skills ficam junto do repositório, em `.agents/skills/`; não exigem instalar conteúdo na configuração pessoal. A descoberta local segue a [documentação oficial](https://learn.chatgpt.com/docs/build-skills). A disponibilidade no ambiente do Dot deve ser conferida pelo mentor; a existência da pasta não comprova que ele a carregou.

| Quando usar | Skill | O que fica pronto |
|---|---|---|
| “Quero organizar este contexto” | `$brain-context` | Perfil, objetivo e primeira entrada com origem |
| “Recebi este texto; atualize a base” | `$brain-curate` | Proposta ou nota revisada e registro da alteração |
| “O que sabemos sobre isto?” | `$brain-query` | Resposta com fontes e lacunas; registro quando for exercício |
| “Me ajude a preparar o dia” | `$brain-briefing` | Briefing datado com cobertura de agenda e tarefas |
| “Quero repetir esta rotina” | `$brain-automate` | Rotina, teste e estado do agendamento conforme evidência |

Por exemplo: **“Use a skill brain-context para organizar o relato abaixo. Aproveite o que ele já informa e me pergunte só o que faltar: [texto].”** O nome pode ser usado no pedido mesmo quando o seletor do aplicativo tiver outra forma de invocação. Se a skill não aparecer, o mentor verifica a descoberta no ambiente; não assume que está instalada.

O fluxo é **texto → perguntas necessárias → proposta → conferência → arquivos salvos**. As [três conferências](quality/workflow-checks.md) cuidam de origem, conteúdo e resultado sem pedir aprovação para cada edição local. Os documentos existentes orientam o formato; a conversa orienta seu preenchimento.

## Conferir a estrutura

```sh
python3 scripts/validate.py
python3 scripts/validate.py --configured
python3 -m unittest discover -s scripts -p 'test_*.py'
```

A primeira verificação confere o template. A segunda exige configuração real e falha enquanto o projeto estiver vazio. Passar na validação estrutural não prova acesso, consulta nem automação em funcionamento; registre essas evidências em `runs/`.

O mesmo validador e seus testes rodam no GitHub a cada push e pull request. Regras comuns ficam em `AGENTS.md`, procedimentos em `routines/` e perguntas de condução nas skills.

Para avaliar comportamento, use as [evals em workspace separado](evals/README.md). Elas ligam três aprendizados da primeira aula ao que foi efetivamente salvo: contexto, prazo conflitante e informação ausente. O script confere os artefatos; outra sessão ou pessoa revisa o conteúdo. Sem revisão, o resultado permanece pendente.
