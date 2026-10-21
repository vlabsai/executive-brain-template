# IA na rotina executiva

Um projeto pequeno para aprender IA organizando uma dificuldade real do trabalho. O Brain é a aplicação prática da [mentoria executiva](https://github.com/vlabsai/executive-ai-mentorship).

## Começar pela conversa

Com o Codex aberto, peça:

> Faça um fork de https://github.com/vlabsai/executive-brain-template na minha conta e clone minha cópia. Use-a como pasta de trabalho e leia suas instruções. Reutilize minha cópia se já existir. Aguarde meu pedido para iniciar a entrevista.

Depois da preparação:

> Use a skill start-executive-project para me entrevistar, esclarecer o que faltar e preencher meu contexto neste projeto.

Você responde ao que faltar e confere a síntese. A skill preenche contexto.md e preserva o relato permitido em inbox/, ou usa a fonte que você já forneceu.

## Três lugares para o trabalho

| Lugar | Para que serve |
|---|---|
| [contexto.md](contexto.md) | Quem você é, o que quer resolver e suas preferências |
| [inbox/](inbox/README.md) | Relatos, textos e propostas que recebemos |
| [knowledge/](knowledge/README.md) | Notas revisadas, com origem e pendências |

As notas começam diretamente nessas pastas; crie subdivisões apenas quando ajudarem a encontrar algo.

## Começar por uma conversa

| Quero… | Pedido |
|---|---|
| Organizar uma informação | Use a skill brain-curate para propor uma nota com origem e lacunas a partir deste texto. |
| Consultar minha base | Use a skill brain-query para responder esta pergunta com as fontes disponíveis. |
| Experimentar uma conferência | Leia evals/README.md e faça comigo o ensaio rápido de contexto inicial, usando apenas dados fictícios. |

As três skills vêm em .agents/skills/. Se o seletor não as mostrar, peça ao Codex que leia o arquivo SKILL.md correspondente nesta cópia; não presuma que a descoberta automática ocorreu. As [regras](AGENTS.md) ficam em um único arquivo. Os [exemplos](evals/README.md) são provas de conceito de poucos minutos.

## Crescer com o uso

Fontes de agenda, briefing e automação entram nos encontros em que forem necessárias. Não há configuração de integrações no ponto de partida. O Dot poderá consultar a base e apoiar rotinas depois de configurar e conferir os acessos no ambiente da pessoa.

O template e seus forks públicos contêm material genérico. Use dados fictícios para testar o fork. Contexto real pode ficar na cópia local ou em um destino privado autorizado; não o envie ao fork público. Não contém dados de cliente ou conteúdo do My Brain pessoal de Fabricio.

## Manutenção do template

Os scripts e o CI são para quem mantém o framework. O validador confere as três skills, exemplos e referências das instruções; não percorre fontes brutas e notas do executivo nem exige infraestrutura de encontros futuros.

Execute python3 scripts/validate.py e python3 -m unittest discover -s scripts -p 'test_*.py' após mudanças no framework.

Uma alteração no template não atualiza automaticamente as cópias já existentes. Atualize as instruções da cópia desejada preservando suas notas e seu contexto.
