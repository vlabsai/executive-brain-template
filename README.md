# Meu projeto de IA

Comece com uma dificuldade real do trabalho. O repositório guarda as fontes permitidas e o conhecimento que você conferiu.

## Começar

Com o Codex aberto, peça:

> Faça um fork de https://github.com/vlabsai/executive-brain-template na minha conta e clone minha cópia. Use-a como pasta de trabalho e leia suas instruções. Reutilize minha cópia se já existir. Aguarde meu pedido para iniciar a entrevista.

Depois:

> Use a skill start-executive-project para me entrevistar, esclarecer o que faltar e organizar meu perfil neste projeto.

A skill aproveita o que você já contou, pergunta pelo que falta e apresenta uma síntese. Depois da conferência, cria o perfil preenchido em knowledge/perfil.md e preserva sua origem em inbox/, ou referencia a fonte que você já forneceu.

## Pastas que já vêm no template

| Pasta | Conteúdo |
|---|---|
| [inbox/](inbox/README.md) | Relatos, textos e propostas que recebemos |
| [knowledge/](knowledge/README.md) | Seu perfil e notas revisadas, com origem e pendências |

As duas pastas já existem no clone, com um README curto explicando sua função. A entrevista e as próximas tarefas criam os arquivos preenchidos dentro delas.

Para incorporar uma informação, faça um pedido natural, por exemplo: **Organize esta transcrição na minha base. Quero encontrar depois as decisões, pendências e próximos passos.** Forneça o texto da reunião e sua origem. O assistente usa o roteiro de curadoria, mostra a proposta e a incorpora depois da sua conferência. Para consultar, pergunte naturalmente, por exemplo: **O que preciso acompanhar neste projeto? Mostre as fontes e o que ainda falta confirmar.**

## O que já vem no template

- [AGENTS.md](AGENTS.md): regras únicas para o assistente.
- .agents/skills/: os três fluxos de trabalho do executivo e o recurso de [teste para os autores dos fluxos](.agents/skills/brain-evaluate/SKILL.md).
- Os testes de autoria reúnem casos e script dentro da própria skill: montagem do contexto, curadoria de reunião e os casos do Projeto Alfa para curadoria e consulta. Cada caso usa poucos pontos de conferência; novos casos entram no mesmo pacote.
- scripts/ e .github/: verificações de manutenção do template.

Se a skill não aparecer no seletor, peça ao Codex que leia o SKILL.md correspondente nesta cópia. Agenda, briefing e automação entram quando houver uma necessidade concreta.

O template e seus forks públicos recebem apenas material genérico. Use dados fictícios para testar; mantenha conteúdo pessoal na cópia local ou em destino privado autorizado. Não envie dados pessoais ao fork público.

Quem mantém os fluxos pode usar brain-evaluate para reproduzir uma tarefa com dados fictícios, conferir a saída e ajustar a skill. Esse teste não é uma atividade do participante nem uma etapa automática a cada nota. Para manutenção do framework, execute python3 scripts/validate.py e python3 -m unittest discover -s scripts -p 'test_*.py'. Essa verificação não comprova acesso operacional. Atualizações do template não alteram automaticamente cópias já existentes.
