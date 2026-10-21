---
name: brain-automate
description: Conduzir a definição e o teste de uma rotina de Brain executivo e, quando solicitado e disponível, configurar seu agendamento com evidência. Usar para automatizar uma rotina delimitada, após combinar fontes e saída.
---

# Preparar e operar uma automação

Follow root `AGENTS.md`, [automation routine](../../../routines/setup-automation.md) and [workflow checks](../../../quality/workflow-checks.md). Use Portuguese with the operator.

Read existing routines and runs first. Reuse a matching routine/schedule instead of creating duplicates. Collect missing decisions in short steps:

- “Qual tarefa repetitiva e resultado queremos automatizar?”
- “Quais fontes podemos consultar e onde o resultado deve aparecer?”
- “Qual frequência, horário e fuso você quer?”
- “O que pode ser feito sozinho e o que precisa da sua revisão?”
- “Como vamos perceber uma falha e como você quer interromper ou corrigir?”

Save the bounded routine in `routines/<name>.md` and retain the setup document as a reusable guide. A request to design a routine does not itself request a live schedule. Mark the routine written while access, test or scheduling is pending.

Perform one manual run against authorized sources when available. Use the relevant query/briefing workflow, inspect the output, and record evidence in `runs/`. A failed or incomplete critical source read blocks scheduling; resolve access or narrow the agreed scope. Do not repeatedly retry side effects after an unknown outcome: inspect the schedule state before retrying.

If the user has requested scheduling, the manual result is reviewed and parameters/destination are known, use the application's available scheduling tool. Do not invent CLI commands or simulate a schedule by writing Markdown. If a tool or access is unavailable, leave a complete written plan and record the specific missing capability. Ask only for missing authorization or critical settings, never to repeat authorization already given.

Record schedule identity and saved state from the tool result. Declare scheduled operation observed only after an actual scheduled run is inspected. Update `config/brain.json` consistently using `not_configured`, `scheduled` or `observed`; do not change to `scheduled` on an ambiguous result. End with the routine/run links, observed state and correction/stop path.
