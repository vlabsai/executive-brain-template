# Comparação local de recuperação · 22/10/2026

O caso fictício navegar-e-buscar contém 15 notas aceitas e oito perguntas em português: paráfrase, orçamento, responsáveis, decisão, contrato e contexto pessoal. Há projetos com valores iguais, identificadores parecidos e uma entrada não aceita em inbox/. As notas são entradas sintéticas, não saídas de uma skill executada.

QMD 2.8.3, embeddings embeddinggemma-300M-Q8_0 e reranker Qwen3-0.6b-Q8_0, no mesmo computador. A passagem final usou uma cópia fictícia nova, com índice próprio e instalação/modelos públicos reutilizados. Cada consulta abriu o CLI; os tempos excluem a atualização prévia do índice e downloads. A fusão e o re-ranking são do QMD. A pergunta completa também segue como intent, preservando o sentido quando os termos textuais são curtos.

| Modo | Nota pertinente em primeiro | Entre os três primeiros | Mediana por consulta |
|---|---|---|---|
| Só vetor, referência anterior | 6 de 8 | 8 de 8 | 1,21 s |
| Híbrida: BM25 + vetor + RRF | 7 de 8 | 8 de 8 | 1,21 s |
| Híbrida com re-ranking | 7 de 8 | 8 de 8 | 2,72 s |

Duas passagens anteriores com a mesma amostra reproduziram as posições observadas; a passagem final preserva a pergunta completa como intent. Os tempos variam com inicialização e cache. O reranker obtido tem 639.153.184 bytes; o modelo de embeddings tem 333.590.944 bytes. Nenhum modelo de expansão foi necessário.

Na pergunta sobre a passagem de atendimentos, a híbrida trouxe a reunião pertinente para primeiro lugar. Na pergunta sobre aprovação do orçamento do Alfa, todos os modos deixaram a nota pertinente em segundo: vetor priorizou o Beta, e a híbrida e o reranker priorizaram o hotel pessoal, que menciona o orçamento do Alfa para negar a relação. Esse caso continua exigindo abrir as notas, conferir domínio e preservar a ausência de aprovação. O re-ranking não demonstrou ganho adicional nesse recorte.

Decisão: híbrida como padrão e re-ranking disponível sob demanda. A preparação padrão verifica separadamente o vetor e a híbrida; setup --rerank prepara e testa também o modelo adicional. O custo adicional não entra em toda consulta sem um ganho observado que o justifique.

Para reproduzir, siga a seção de comparação no [fluxo de avaliação](../SKILL.md). O script devolve posições, tempos e candidatos reais. O ensaio mede recuperação num recorte pequeno; não comprova resposta final, decisão do assistente, escala representativa ou execução cloud. Índice e resultados transitórios ficam em .local/ensaios/ e não entram no template.
