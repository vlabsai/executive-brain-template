---
name: start-executive-project
description: Entrevistar o executivo e preencher o contexto inicial na cópia do projeto já clonada na máquina dele. Usar explicitamente no primeiro acesso ao fork ou à cópia individual, sem criar ou clonar repositórios durante a entrevista.
---

# Preparar meu projeto

Run in the executive's local working copy, after Codex has prepared or reused the client fork and clone. Resolve file and shell operations against that copy; do not assume the conversation's original folder is the intended project. Follow root `AGENTS.md` and [workflow checks](../../../quality/workflow-checks.md). Speak Portuguese. This is one explicitly invoked conversation: interview, clarify, review and save. Do not ask the client to invoke a second skill or restart the interview to advance.

## Confirm the working folder

Read the current profile, configuration and local repository identity before asking about the person. If this is the canonical `vlabsai/executive-brain-template` checkout or a common mentoring repository, do not save client context there; point to [first-use instructions](../../../START_HERE.md). If the client already has the intended copy, reuse it. Do not create forks, clone repositories, change remotes, alter visibility or grant access in this skill.

For an explicitly fictional rehearsal or eval workspace, work only with its synthetic inputs even if it has no Git metadata. Keep that limitation in the record rather than claiming a fork or clone was verified.

## Interview and disambiguate

Briefly explain: “Vou entender sua rotina, esclarecer o que faltar e salvar o contexto inicial nesta pasta.” Extract what the client already supplied. Ask the next useful question, normally one at a time:

- “Qual é seu papel e pelo que você responde no dia a dia?”
- “Qual dificuldade concreta de informação, agenda ou trabalho você quer resolver primeiro?”
- “Pode contar um caso recente e onde estavam as informações?”
- “Que resultado pequeno já faria diferença para você?”
- “Como prefere receber as respostas e que informações podemos guardar nesta cópia?”

Use these as prompts, not a fixed form. Resolve ambiguities that affect the project: who a person is, which project is meant, whether a deadline is confirmed, and which source supports a claim. Do not ask already answered questions. Ask for a time zone when recording it or interpreting dates/time; do not infer it. Unknowns outside the first goal remain explicit pending items.

Show a compact synthesis of the profile and goal. The client corrects or confirms its substance in the same conversation. Reuse acceptance already given; do not impose a second launch command or an approval ceremony for each local edit.

## Fill the project

Use [brain-context](../brain-context/SKILL.md) as the implementation guide, reusing the interview and its confirmed summary. No second interview or invocation is needed. Keep any existing knowledge and settings that the client did not change.

- `profile/overview.md`: role, responsibilities, difficulty, outcome, preferences, origin and confirmation date.
- `config/brain.json`: agreed goal and settings actually defined; unknown values remain unset. File creation does not establish runtime readiness.
- `inbox/relato-inicial.md`: only the permitted relevant excerpt, with speaker/source and original/read dates. If the task supplies an existing source file, reference/reuse it rather than duplicating the raw material. Register its actual local source in config using the catalog contract.
- `runs/preparacao-inicial.md`: actions actually performed, files, review and remaining questions. Honor an explicitly requested run-log path in an exercise or task.

If substantive review is pending, save drafts with that status and retain accepted content. Do not mark content reviewed until supported by the actual exchange or the task's delegated review.

Run `python3 scripts/validate.py`. End by showing the actual saved paths and explaining the role of each file. The template and its public forks are public. Use synthetic data for a fork rehearsal. Distinguish local writes from commits or pushes; do not commit or push personal context to a public fork, and do not synchronize personal content or configure integrations/automations as a side effect. The next activity is curating a permitted piece of work, using the profile already saved.
