# Ensaios rápidos

Uma prova de conceito leva poucos minutos: uma entrada fictícia, o resultado que a skill produziu e três pontos para a pessoa conferir. Se houver erro, corrija e compare novamente. Não há pontuação ou relatório obrigatório.

## Pedir na conversa

> Leia evals/README.md e faça comigo o ensaio rápido de contexto inicial, usando apenas dados fictícios.

O Codex prepara uma pasta nova com `python3 scripts/ensaio.py contexto-inicial`. O script informa o caminho; o participante não precisa usar o terminal. A pasta fica em `.local/ensaios/`, separada do contexto e das notas reais. Recebe apenas as instruções, skills e fontes fictícias necessárias.

Trabalhe nessa pasta e siga seu TASK.md. Depois mostre o relato e o contexto realmente produzido. Confiram juntos:

1. Papel e responsabilidades correspondem ao relato?
2. Dificuldade e objetivo foram preservados?
3. A origem está indicada, sem inventar o que falta?

Aguarde a conferência da pessoa. Se aparecer uma diferença, preserve a versão anterior no ensaio, peça ou aplique o ajuste autorizado e mostre o que mudou. Não declare uma nova execução da skill se houve apenas edição da saída. Volte ao contexto real e use a mesma conferência.

Marina é a executiva fictícia deste caso. Uma pasta nova permite repetir a experiência sem apagar a anterior. Outra sessão é uma opção para uma conferência independente, quando útil; não é exigida na aula.

## Exemplos disponíveis

| Exemplo | Conceito | Conferência |
|---|---|---|
| [contexto-inicial](contexto-inicial.json) | Orientar a IA com contexto | Papel, objetivo e fidelidade ao relato |
| [prazo-em-conflito](prazo-em-conflito.json) | Distinguir fato de sugestão | Prazo confirmado, mudança pendente e origem |
| [consulta-sem-orcamento](consulta-sem-orcamento.json) | Reconhecer uma lacuna | Ausência explícita, fonte e nenhuma invenção |

Cada exemplo contém a fonte, um pedido e três pontos de conferência. O script só prepara a pasta; ele não executa o modelo nem aprova seu resultado. Um ensaio não comprova acesso do Dot, integração ou funcionamento com dados reais.
