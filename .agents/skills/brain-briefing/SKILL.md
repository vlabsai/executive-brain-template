---
name: brain-briefing
description: Preparar um briefing manual do dia de um executivo com agenda, tarefas e contexto da base, fazendo perguntas sobre data, fontes e prioridades que faltam. Usar para organizar o dia, sem alterar compromissos.
---

# Preparar o dia

Follow root `AGENTS.md`, [daily briefing routine](../../../routines/daily-briefing.md) and [workflow checks](../../../quality/workflow-checks.md). Use Portuguese with the operator.

Read the profile, configuration and `commitments/source-map.md`. Confirm the actual date and configured time zone. Ask only what is unresolved:

- “Para qual dia e fuso vamos preparar o briefing?”
- “Qual calendário e lista de tarefas representam seus compromissos?”
- “Há alguma prioridade que precisa orientar esse dia?”

Use the registered, authorized sources. Do not interpret an empty or inaccessible calendar as a free day. If access is missing, offer a briefing explicitly based on an operator-provided dated excerpt, or stop the dependent part and record the gap; do not claim full calendar coverage.

Produce a scannable briefing: schedule with time zones; commitments and deadlines; context to prepare; dependencies/conflicts; suggested priorities. Keep source facts distinct from suggestions. Link each commitment to its operational source or identify the excerpt and its observation time.

Ask for a focused correction if a priority or conflict needs a decision. Save a dated `runs/` record with briefing, actual coverage, read time and limitations. Preserve previous runs. This skill does not send messages or create/move events or tasks; use task-specific authorization if the operator subsequently requests those actions.
