---
name: brain-query
description: Responder perguntas sobre a base de um Brain executivo com fontes, datas e lacunas explícitas, ou conduzir uma conferência da resposta na mentoria. Usar para consulta, sem curadoria implícita.
---

# Consultar e conferir a base

Follow root `AGENTS.md`, [query routine](../../../routines/answer-from-base.md) and [workflow checks](../../../quality/workflow-checks.md). Use Portuguese with the operator.

Search relevant repository notes and their source references. Clarify the project, period or intended decision only when ambiguity changes the answer:

- “Sobre qual projeto ou período você quer saber?”
- “Você precisa localizar um fato ou preparar uma decisão?”

Do not require a completed onboarding or a connected calendar for a question answerable from local files. Read authorized sources actually available in this task; do not silently expand to other accounts or repositories.

Answer briefly with: supported facts and links/dates; interpretation or proposed next action when useful; missing/conflicting information and coverage limits. Cite the actual supporting note and source location. If evidence is absent, say what is missing and the smallest source/question that could resolve it. Tentative information does not erase a confirmed fact.

For a lesson or requested verification, ask “Qual afirmação vamos conferir na origem?” Compare the response with that source and correct it. Record the question, sources actually read, answer, correction and reviewer in a dated `runs/` file using [run-log](../../../templates/run-log.md); use `runs/conferencia-do-encontro.md` when that exercise is prepared. Update [query checks](../../../quality/query-checks.md) only for cases actually performed.

An ordinary consultation need not create a file. Do not modify canonical knowledge as a side effect; if the operator asks to incorporate a correction, switch to the curation workflow. Close by identifying what was found and what remains unknown.

Refer to sources by descriptive names with the operator.
