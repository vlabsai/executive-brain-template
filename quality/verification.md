# Verificação do template · 21/10/2026

- `python3 scripts/validate.py`: estrutura, links e configuração vazia válidos.
- `python3 scripts/validate.py --configured`: falhou como esperado, pois nome, objetivo, fuso e fonte ainda não estão configurados.
- Configuração inicial: `state=template`, fontes vazias, agenda e tarefas sem origem operacional escolhida, automação não configurada.
- Nenhum dado de cliente ou conteúdo do My Brain pessoal foi importado.
- Cinco skills locais em `.agents/skills/`: contexto, curadoria, consulta, briefing e automação. Todas passaram pelo `quick_validate.py` do criador de skills; links e metadados também foram conferidos pelo validador do repositório.
- Cinco testes com cópias sintéticas isoladas passaram: template vazio sem prontidão, fonte habilitada sem permissão/leitura, calendário apontando para fonte errada, configuração sintética estruturalmente válida e referência de skill saindo do repositório.
- Workflow do GitHub escrito para repetir validação e testes em pushes e pull requests. A execução remota deve ser conferida no GitHub.
- Os cenários de interação estão em `quality/workflow-checks.md`. Ainda não houve ensaio independente das conversas nem confirmação da descoberta das skills no ambiente do Dot de um cliente.

Este registro comprova a estrutura do ponto de partida. Acesso do Dot, consultas reais, briefing e automação serão validados na cópia do cliente, com evidência de execução.

## Atualização · aula em ciclos e evals

- Contexto inicial reaproveitado após a criação/clonagem da cópia privada, sem repetir a entrevista. Fontes são apresentadas ao operador com nomes descritivos.
- Três cenários sintéticos de avaliação: contexto, prazo conflitante e orçamento ausente. A preparação separa workspace, gabarito e revisão. O resultado sem revisão permanece pending_review.
- Dez testes passaram: cinco de estrutura/prontidão e cinco de isolamento, integridade e estados da avaliação. Esses testes validam o mecanismo; os três cenários ainda não foram executados como conversas independentes neste registro.

## Entrada pelo fork e clone

A skill inicial agora pertence ao template e é explícita. O cliente abre sua cópia local antes da entrevista; a mesma conversa esclarece o contexto e preenche os arquivos. O template continua privado. A eval de contexto foi alinhada à skill inicial; a execução comportamental independente segue pendente.

O GitHub confirmou private=true e allow_forking=false. A tentativa de habilitar fork neste repositório retornou: This organization does not allow private repository forking. A política da organização não foi alterada; a preparação de acesso/fork para o cliente continua pendente.
