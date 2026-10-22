---
name: brain-query
description: Responder sobre as notas do projeto com fontes e lacunas, e conferir uma afirmação na origem quando solicitado. Usar para consultas sem alterar a base implicitamente.
---

# Consultar e conferir

Siga [AGENTS.md](../../../AGENTS.md). Leia knowledge/perfil.md quando existir, as notas relevantes e suas referências. Use somente fontes autorizadas e disponíveis. Não exija perfil completo ou agenda conectada para responder sobre um arquivo local.

Esclareça assunto, período ou objetivo somente quando a ambiguidade mudar a resposta. Quando a pergunta exigir recuperar conteúdo da base, use a [busca local](references/search.md): o helper atualiza o índice antes da consulta. A busca padrão combina significado e termos exatos. Formule a pergunta e forneça poucas palavras centrais, nomes ou identificadores em --terms, conforme a referência, para que o componente textual não dependa de todas as palavras da pergunta. Para uma pergunta difícil, o re-ranking opcional reordena os candidatos; prepare esse modo antes de usá-lo. Abra as notas atuais e suas relações, confira domínios e a origem relevante. Um resultado aproximado ou de outro contexto não sustenta a resposta. As propriedades de domínio não são um filtro nativo nesta versão do mecanismo.

Uma pergunta sobre uma nota já indicada pode ser respondida pela leitura direta. Se a busca estiver indisponível, explique e use leitura/busca textual quando suficientes, sem afirmar que houve recuperação semântica. Nunca use resultados antigos depois de uma falha de atualização.

Responda de forma curta com os fatos sustentados e suas fontes. Separe interpretação, proposta e informação ausente. Se houver conflito, preserve as versões e suas origens; não escolha uma confirmação que não existe.

Quando a pergunta pedir o estado atual, compare os registros datados e siga o acompanhamento mais recente disponível. Identifique a data de referência e o que não foi confirmado depois; uma reunião histórica continua válida para explicar o que se combinou naquele momento. Não trate uma síntese como se tivesse lido todas as fontes citadas nela.

Quando for solicitada uma conferência, escolha com a pessoa uma afirmação e encontre seu suporte na origem. Se houver diferença, corrija esse ponto e releia a resposta. Se for pedido guardar o resultado, proponha uma nota com nome descritivo no local pertinente de knowledge/, seguindo as [convenções das notas](../../../knowledge/README.md). Registre a pergunta, as fontes realmente lidas e a conferência ou correção observada; reutilize uma nota existente quando for uma atualização do mesmo assunto. Não declare revisão que não aconteceu.

Uma consulta comum não cria arquivo nem altera notas. Para incorporar fatos à base, use a skill de curadoria. Termine com o que foi encontrado e a informação que falta, sem presumir que houve ação externa.
