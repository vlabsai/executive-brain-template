# Primeiro uso com o mentor

## Comece com um pedido no Codex

Com o Codex aberto, cole este pedido na conversa:

> Faça um fork de https://github.com/vlabsai/executive-brain-template na minha conta e clone minha cópia. Use-a como pasta de trabalho e leia suas instruções. Reutilize minha cópia se já existir. Aguarde meu pedido para iniciar a entrevista.

O Codex prepara a cópia e informa onde ela ficou. Se precisar de login ou de uma escolha sobre o destino, ele orienta apenas essa parte. O executivo acompanha a preparação pela conversa.

A entrevista começa depois, com a cópia preparada.

## Uma chamada · entrevista e preenchimento

Acione explicitamente **Preparar meu projeto**:

> Use a skill start-executive-project para me entrevistar e preencher o contexto deste projeto.

A skill lê o que já existe, pergunta o que faltar e esclarece ambiguidades. Você corrige ou confirma a síntese. Na mesma conversa ela preenche:

| Arquivo | Resultado |
|---|---|
| `profile/overview.md` | Seu papel, dificuldade, objetivo e preferências |
| `config/brain.json` | Objetivo e configurações já definidas |
| `inbox/relato-inicial.md` | Trecho permitido que fundamenta o perfil, com origem e data |
| `runs/preparacao-inicial.md` | O que foi salvo, conferido e ficou pendente |

Abra os arquivos ao concluir. A skill não pede outro acionamento para passar da entrevista ao preenchimento. Ela também não cria ou clona o repositório: essa preparação já aconteceu.

## Continuar a primeira aula

Escolha uma informação pequena e permitida do trabalho, use brain-curate para montar e revisar a nota e brain-query para fazer uma consulta conferida. No ensaio, o laboratório contém o relato fictício e a anotação da reunião em inbox/fontes-do-encontro.md, a nota em knowledge/projects/alfa.md e o registro da consulta em runs/conferencia-do-encontro.md.

O estado permanece template até a configuração real. Catálogo completo, acesso operacional do Dot e automações avançam nos encontros próprios. Salvar os arquivos localmente não comprova essas conexões nem autoriza sincronização automática.

## 1 · Escolher uma dificuldade real

Registre em [profile/overview.md](profile/overview.md) onde a informação se perde e qual situação vamos melhorar: preparar uma reunião, localizar uma decisão ou acompanhar pendências. Uma necessidade pequena basta.

## 2 · Configurar a cópia

Preencha `config/brain.json`: nome do projeto, objetivo e fuso confirmado. Troque o estado de `template` para `configured` depois de preparar as fontes. Configure o acesso real no aplicativo e ambiente disponíveis; este arquivo apenas registra a decisão.

Em `config/sources.json`, cadastre uma fonte inicial com ID, tipo, finalidade, localizador, autoridade, permissão confirmada, acesso verificado e data. Use a referência em `sources/catalog.md`. Dados de conta e credenciais permanecem fora do Git.

## 3 · Construir e conferir uma peça

Preencha o perfil. Leia uma entrada permitida e crie uma nota com `templates/source-note.md`. Marque como revisada somente depois de conferir os fatos. Faça uma pergunta respondível e uma pergunta cuja resposta falta. Registre o que aconteceu em `runs/`, com `templates/run-log.md`.

## 4 · Ampliar durante a mentoria

| Encontro | Conceito e aplicação |
|---|---|
| 1 | Contexto e verificação: perfil, nota e primeira resposta |
| 2 | Fontes e organização: repositório e catálogo |
| 3 | Curadoria: entrada, revisão e atualização |
| 4 | Orquestração: Dot e consultas com evidência |
| 5 | Trabalho diário: fontes de agenda/tarefas e briefing manual |
| 6 | Automação: uma rotina testada e sua operação |

Mantenha o escopo nas fontes que realmente ajudam o problema prioritário. A agenda inteira e todas as conexões não são pré-requisitos para começar.

## 5 · Aceitar a primeira versão

Execute o validador estrutural, revise `quality/acceptance.md` e demonstre os usos com fontes acessíveis. Defina com o mentor o que foi comprovado e o que continua pendente. Não marque o projeto pronto só porque os arquivos existem.

Para testar o fork público, use o caso fictício. Mantenha conteúdo real na cópia local ou em um destino privado autorizado; não o publique no fork.
