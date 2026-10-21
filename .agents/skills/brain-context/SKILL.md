---
name: brain-context
description: Transformar um relato inicial em perfil, objetivo e primeira fonte de um Brain executivo, conduzindo perguntas sobre o contexto que falta. Usar na preparação ou revisão do contexto do cliente.
---

# Organizar o contexto inicial

Work in the client's active repository, following its root `AGENTS.md` and [workflow checks](../../../quality/workflow-checks.md). Read the current profile and configuration before asking questions. Operator-facing language is Portuguese.

Extract what the supplied text already establishes. When the initial skill collected a reviewed summary in this working copy, reuse it; do not restart the interview. Show a short summary of the difficulty and expected result. Ask the next unresolved question, using these prompts as a guide rather than a mandatory questionnaire:

- “Qual situação da sua rotina mais precisa melhorar? Pode contar um caso recente?”
- “Que resultado pequeno já faria diferença: encontrar uma decisão, preparar uma reunião ou acompanhar um prazo?”
- “Qual é seu papel nesse trabalho e como prefere receber ajuda?”
- “De qual fonte veio esse relato e o que podemos guardar nesta cópia local?”
- “Qual fonte pequena podemos usar primeiro? Onde ela está e quem confirmou seu uso?”

Ask about time zone only when configuring it or when dates/time matter. Do not demand every source, calendar connection or technical setting to begin. The mentor handles the local checkout; do not ask the executive to learn Git.

Build incrementally:

- Update `profile/overview.md`, preserving known context and recording the speaker/source and confirmation date. Mark unresolved material as pending.
- Record the agreed objective in `config/brain.json`; leave unknown settings empty. Keep `state=template` until configured readiness is established.
- Save only the permitted, relevant source excerpt in a dated file under `inbox/`, with origin and original/read dates. For the initial interview, use `inbox/relato-inicial.md`; reuse `inbox/fontes-do-encontro.md` or another permitted source file when the task already provides it.
- Register the source in `config/sources.json` using [the catalog contract](../../../sources/catalog.md). A pasted excerpt is a local source; it does not prove access to its original mailbox or calendar. Register it disabled until authorization and actual local reading are established. Unknown dates stay explicitly unknown in the note.

Present the profile and proposed changes for substantive review. Within already authorized local editing, save a draft without a separate permission ceremony. Only label a statement confirmed/reviewed when the operator or authorized review actually supports it. End with links to saved files, remaining questions and the next small task. Record the application in `runs/` when files change.

Use descriptive source names with the operator; registry IDs are internal references, not teaching labels.
