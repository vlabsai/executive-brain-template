# Evals da mentoria

Três exercícios fictícios ligam a experiência da aula aos arquivos realmente produzidos. A avaliação tem duas partes: o script confere integridade e resultados observáveis; outra sessão ou pessoa julga a resposta e a conversa com critérios curtos.

| Cenário | Aprendizado | Resultado que precisa de conferência |
|---|---|---|
| contexto-inicial | Usar contexto e perguntar apenas o necessário | Perfil fiel ao relato e origem identificada |
| prazo-em-conflito | Separar fato de sugestão | Nota confirmada preservada; mudança pendente fora da base revisada |
| consulta-sem-orcamento | Reconhecer lacunas | Resposta com evidência, sem valor inventado |

## Rodar em outra sessão

1. Prepare uma execução nova, fora da cópia do cliente. Por exemplo, a partir da raiz do projeto:

```sh
python3 scripts/evaluate.py prepare prazo-em-conflito --destination ../ensaio-prazo-01
```

2. Abra **somente `../ensaio-prazo-01/workspace/`** como projeto em outra sessão do Codex. Peça: **“Leia TASK.md e execute o exercício usando a skill indicada.”** O diretório contém instruções e dados sintéticos; perfil, fontes, notas e configurações reais do cliente não são copiados. O gabarito permanece fora da pasta de execução.
3. Ao terminar, preserve os arquivos e a conversa real. Na sessão de revisão, abra `../ensaio-prazo-01/`, leia `REVIEW.md`, confira as fontes e preencha `review.json`. Para avaliar como a interação ocorreu, forneça a conversa da execução; sem essa evidência, marque o critério como pendente.
4. Confira os artefatos e a revisão:

```sh
python3 scripts/evaluate.py check ../ensaio-prazo-01 --review ../ensaio-prazo-01/review.json
```

Sem `--review`, o script já confere os arquivos, mas mantém o resultado como `pending_review`. Arquivo existente ou JSON válido não basta para aprovar a resposta. O código de saída só é zero quando as verificações automáticas e todos os critérios revisados passam.

## O que fica registrado

- `workspace/`: instruções, fontes fictícias e resultado da execução.
- `manifest.json`: cenário, ligação com a aula, hashes iniciais e critérios; fora da pasta do executor.
- `REVIEW.md` e `review.json`: pedido e resultado da revisão.
- `report.json`: verificações automáticas, revisão e estado final.

Não reutilize a mesma pasta para outra tentativa. Uma nova execução preserva a anterior e permite comparar mudanças nas instruções. A separação de pastas organiza um ensaio; o mentor escolhe uma sessão independente para evitar que quem executou também produza seu próprio gabarito.

Os cenários validam o comportamento no recorte proposto. Não provam acesso do Dot, integração com calendário nem operação com dados reais. A criação/clonagem do repositório tem preparo técnico próprio no material do mentor; estas três evals não criam recursos externos.
