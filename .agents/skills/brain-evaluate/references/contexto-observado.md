# Início pela conversa · prova local de 22/10/2026

O caso conversar-contexto cobre o trecho que o caso montar-contexto não exercitava: este último já entregava um relato conferido. Foi aberta uma conversa nova, sem histórico do autor, numa cópia limpa e sem Git. O executor recebeu somente a localização, o limite fictício e o pedido natural, sem nome de skill, critérios ou resultado esperado. A correção do fluxo está na revisão 7aa21b3.

Na referência anterior, após o relato de dificuldade e objetivo, o executor pediu contextos e papéis; mesmo deixando nomes para depois, pediu outro exemplo recente. Não havia uma condição clara para encerrar a coleta e apresentar a conferência. O teste informado pela pessoa também mostrava uma proposta provisória sem conclusão da entrevista.

Na execução corrigida, o assistente preparou o ambiente e perguntou pela dificuldade. O operador enviou o relato fictício de author_replies: agendas pessoal e de trabalho, Google Agenda, WhatsApp e Granola, com objetivo de enxergar compromissos e pendências preservando contexto e origem. O assistente apresentou uma síntese e perguntou: “Está correto? Faltou ou precisa corrigir alguma coisa?”. Só então o operador enviou o OK, sem orientar como salvar.

| Conferência | Resultado observado |
|---|---|
| Antes do OK | Os sete READMEs de inbox/ e knowledge/ mantiveram seus hashes. Não existiam perfil.md, relato-inicial.md ou perfil-proposto.md. |
| Depois do OK | Criados somente knowledge/perfil.md e inbox/relato-inicial.md como conteúdo. Perfil com id, domínios, origem relativa e revisão efetiva. |
| Fidelidade | Dificuldade, objetivo e fontes mencionadas preservados. Papel, empresas, nomes de agendas e outros detalhes não foram inventados; ficaram pendentes quando relevantes. Nenhuma fonte conectada foi consultada. |
| Encerramento | O executor abriu perfil e origem no aplicativo e atualizou o índice, com um documento e seus embeddings. Não criou arquivo temporário de proposta. |

Os 41 arquivos do template da cópia executora permaneceram idênticos à revisão testada. A integridade de ids e links passou nessa cópia; os 32 testes de manutenção passaram no template. O novo teste unitário confere que a preparação do caso começa vazia e não entrega author_replies ao executor; ele não substitui a conversa observada.

Alcance: um ensaio conversacional local com dados fictícios e preparação real do QMD. O encaminhamento pelo pedido natural foi observado pela leitura das instruções, sem comprovar um hook nativo ou execução automática em segundo plano. Não testa criação de repositório privado, acesso a conectores, cliente real ou executor remoto. As respostas do operador e os três pontos de conferência ficam no caso, dentro da avaliação dos autores.
