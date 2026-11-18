---
name: marvin
description: Run requirement-analyst, then planner, then coding-agent for one work item, stopping wherever a human must answer, approve, acknowledge, or resolve a blocker. Brownfield skeleton approval waits until Marvin is explicitly prompted to review the skeleton. Use when the user asks to run marvin, take a ticket from sources through implementation, or resume a paused pipeline run. Do NOT use to approve the solution skeleton spec, answer planner questions, or implement a blocked or unacknowledged plan. Do NOT use for a single stage; use requirement-analyst, planner, or coding-agent directly.
disable-model-invocation: true
---
# Marvin

## Use this skill when

- The user asks to run the requirements → planning → implementation pipeline
- The user wants one work item carried from source artifacts through code
- The user is resuming after a human gate (answers, steering, approval, or acknowledgement)

## Required inputs

- One stable work item ID (`requirements/<ticket-id>/`)
- Source artifacts for the requirement analyst, or an existing requirements package
- The repo working tree the coding agent will edit
- A one-line user story title, or a Jira issue whose summary can supply it, before the first write
- Optional architecture style or module pointers for the planner

## Execution

Read **`references/workflow.md`** and follow it. It is the only stage sequencer. Each stage is still the child skill; do not reimplement that skill here.

Load a reference only at the step that needs it:

| Reference | When |
|-----------|------|
| `references/workflow.md` | Always |
| `references/human-gates.md` | Before leaving a child skill's stop, and before starting the next stage |
| `references/handoff-contract.md` | Before reading or trusting either `handoff.json` |
| `references/mode-behavior.md` | At Phase 0, and whenever the run pauses or resumes |
| `references/anti-patterns.md` | When tempted to skip a human gate or auto-approve |
| `templates/human-pause.md` | Whenever the workflow says **STOP** for a human — put it in the final reply (Slack / IDE / CLI). Do not use AskQuestion |

Child skills, read and follow in full when their phase starts:

| Stage | Skill |
|-------|--------|
| 1 | `.cursor/skills/requirement-analyst/SKILL.md` |
| 2 | `.cursor/skills/planner/SKILL.md` |
| 3 | `.cursor/skills/coding-agent/SKILL.md` |
| 9 (after coding) | create-pr (`.cursor/skills/create-pr/SKILL.md` when present) |

## Mode behavior

- **Plan mode**: resolve the current stage from artifacts and report the next human gate. Do not write requirements, plan files, or product code. Do not create or switch git branches.
- **Agent mode**: run the next stage until a human gate or until implementation is complete. Before the first write or commit of the turn, create the user-story branch when it does not exist, switch onto it, and do the rest of the turn's work there (workflow Step 1b). Do not leave the previous branch checked out. After coding completion, create a PR for that branch when none exists (workflow Step 9). Human gates always use the human-pause final reply — never AskQuestion, never self-answered skipped questions. Skeleton-review pauses paste separate links for `solution-skeleton-spec.md` and `design-decisions.md`.

The request that starts the pipeline is not approval of the solution skeleton spec and not acknowledgement of implementation risk. It also does not prompt Marvin to require brownfield skeleton approval. That requirement starts only when the user explicitly asks Marvin to review or approve the skeleton.
