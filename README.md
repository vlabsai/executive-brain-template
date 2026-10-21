# IA na rotina executiva · Template do Brain

Ponto de partida para aplicar os conceitos da [mentoria executiva](https://github.com/vlabsai/executive-ai-mentorship) a um problema real: lidar com fontes de informação, agenda, compromissos e trabalho diário.

O Brain é o projeto de aplicação. Este template organiza o conhecimento curado, suas origens e as rotinas que o Dot poderá coordenar no ambiente configurado para o cliente.

## Comece pequeno

1. Use **Use this template → Create a new repository** e crie uma cópia privada para o cliente.
2. Siga [START_HERE.md](START_HERE.md) com o mentor.
3. Comece pelo perfil, uma fonte e uma nota revisada. Amplie a base conforme os encontros.

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
| [runs/](runs/README.md) | Evidências de execução e revisão |
| [quality/acceptance.md](quality/acceptance.md) | Critérios para aceitar a primeira versão |

## Conferir a estrutura

```sh
python3 scripts/validate.py
python3 scripts/validate.py --configured
```

A primeira verificação confere o template. A segunda exige configuração real e falha enquanto o projeto estiver vazio. Passar na validação estrutural não prova acesso, consulta nem automação em funcionamento; registre essas evidências em `runs/`.
