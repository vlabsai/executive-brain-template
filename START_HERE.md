# Primeiro uso com o mentor

## Antes do encontro 1 · Preparação pelo mentor

O mentor cria a cópia privada deste template, abre o checkout no computador de trabalho e confirma com o executivo o caminho local da pasta. A pasta do cliente fica separada do repositório comum da mentoria. Verifique que é possível ler e salvar um arquivo.

Na aula 1, use somente quatro arquivos:

| Arquivo | Papel na primeira construção |
|---|---|
| `inbox/session-01-sources.md` | Duas fontes pequenas e permitidas para a aula |
| `profile/overview.md` | Contexto validado do executivo |
| `knowledge/projects/<projeto>.md` | Nota com fatos, origem e lacunas |
| `runs/session-01-check.md` | Pergunta, fontes usadas e revisão observada |

O mentor prepara e apoia a edição; o executivo confere o conteúdo e aprende a encontrá-lo. O salvamento e o versionamento da cópia privada são conferidos ao encerrar. O laboratório fictício da mentoria usa `knowledge/projects/alfa.md`; não trate o caso Alfa como dado do cliente.

Para conduzir essa construção por conversa, use **brain-context → brain-curate → brain-query**. O mentor confere antes se as skills aparecem no ambiente. Comece com o relato ou as fontes preparadas: a skill aproveita o texto, pergunta o que falta e salva nos caminhos acima. Mostre os arquivos ao executivo após cada construção. Veja [os nomes e exemplos de uso](README.md#começar-por-uma-conversa).

Começar essa construção acompanhada não exige configurar toda a base. O catálogo de fontes será trabalhado no encontro 2; o acesso operacional do Dot será verificado antes do encontro 4. O estado permanece `template` até a configuração real. Se o ambiente não estiver disponível, use o laboratório fictício e registre o preparo do cliente como pendente.

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
