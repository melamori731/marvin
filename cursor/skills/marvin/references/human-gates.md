# Human gates

The child skill is the source of truth. This index is the pipeline's checklist so a sequencer does not treat those stops as automatic.

When a row matches, stop the pipeline, put `templates/human-pause.md` in the final reply, and wait. That pause text is the channel-agnostic surface for Slack, IDE, and CLI. Do not use IDE-only AskQuestion. Do not self-answer skipped questions and continue. Resume only the child skill that raised the gate.

## Story branch

Source: `references/workflow.md` Step 1b

| State | Human involvement |
|-------|-------------------|
| This turn will write or commit, and no one-line user story title or Jira summary is available | Ask for the user story title. Stop. Do not invent a slug or create a placeholder branch |
| `git switch` onto an existing story branch would overwrite or drop local changes | Stop and report the git error. Do not discard uncommitted work |
| After create or switch, `git branch --show-current` is still the previous branch | Stop. Do not write on the previous branch |
| A later stage would switch back to the previous branch | Stop. The rest of the work stays on the story branch |

## Requirement analyst

Source: `.cursor/skills/requirement-analyst/SKILL.md`

| State | Human involvement |
|-------|-------------------|
| No source artifacts | Ask what to analyze. Stop |
| No stable work item ID | Ask for one. Stop |
| Blocking or high-impact ambiguity (scope, acceptance, data ownership, external behavior, architecture assumptions, readiness) | Put at most 3–5 prioritized questions in the human-pause final reply and **STOP**. Do not finalize outputs in that round. Do not use AskQuestion. Do not invent answers |
| `handoff.json.status` is `BLOCKED` | Human resolves contradictions, critical ambiguity, or missing information before planning |
| `requiresHumanInput` is `true` | Human supplies the missing decision before planning. Surface it in the pause text and wait |
| `blockingIssues` is non-empty | Same as blocked. Do not start the planner |

`READY_WITH_RISKS` may advance only when Gate 1A in `workflow.md` passes. Manageable tracked risks are not a silent skip of `requiresHumanInput`.

## Planner

Source: `.cursor/skills/planner/references/workflow.md` and `references/output-contract.md`

The planner stays interactive at every row below. The pipeline must not choose greenfield vs brownfield, a greenfield architecture, or a design alternative for the user. Brownfield uses the architecture style already applied in the repo without asking the human to pick one.

| State | Human involvement |
|-------|-------------------|
| Execution context cannot write planner artifacts | Ask the user to rerun in Agent mode |
| Requirements path or required analyst files missing | Human points at the package or returns to the analyst |
| Greenfield vs brownfield unclear | Human chooses the planning mode |
| Greenfield: user architecture style contradicts trusted repo context | Human chooses which architecture governs |
| Greenfield: validator confidence is low, `conflicts[]` is non-empty, or recommendation is stop | Human clarifies among the stated alternatives |
| Greenfield: no architecture candidate | Human provides a style or repo guidance |
| Brownfield: no applied style can be identified | Human points at the modules that already show the style. Do not offer a menu of new styles |
| Analyst readiness `BLOCKED` or handoff metadata malformed | Human resolves the requirements handoff. Do not draft |
| Quality gate cannot map scope or minimum accepted scope | Human resolves the missing input. Do not downgrade it to a design risk |
| `solution-skeleton-spec.md` failed to write | Report the exact error. Retry only after the user confirms |
| Skeleton review required and review artifacts written (`design-decisions.md`, `solution-skeleton-spec.md`) | Human approves writing `plan.md`, or steers changes. Publish both review files and paste separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` in the chat (not only the skeleton). List implementation risks in that chat when acknowledgement is required |
| Plan handoff `skeletonReviewRequired` is `false`, or there is no plan handoff yet and this brownfield run was not explicitly prompted to review the skeleton | Do not stop for skeleton approval. The planner records `skeletonReviewRequired: false` when it writes the handoff |
| Steering during a required skeleton review | Update the two review artifacts, publish both again with separate GitHub blob links for each, then wait |
| Intended implementation status `BLOCKED` | Human resolves blockers before any `plan.md` write |

Skeleton approval is only an explicit approve, proceed, or write-the-plan instruction after both review files exist, and only when review is required. The pipeline start message is not that instruction and is not a prompt to require brownfield skeleton review. Explicit prompts are "review the skeleton", "review the solution skeleton spec", "approve the skeleton before the plan", and "ask me to approve the skeleton".

## Coding agent

Source: `.cursor/skills/coding-agent/references/workflow.md` and `references/mode-behavior.md`

| State | Human involvement |
|-------|-------------------|
| Plan mode | Report readiness only. Ask for Agent mode before edits |
| Required plan artifacts missing | Human points at a complete plan package |
| `READY_FOR_IMPLEMENTATION_WITH_ACK` and no valid acknowledgement | Surface the implementation risks in the chat (acknowledgement reason and every design risk). Human decides `proceed_as_is` or `risk_resolved` before any code edit |
| Plan handoff `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true` | Do not start coding. The chat pastes separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` (including `solutionSkeletonSpecUrl` for the skeleton) and, when acknowledgement is required, the implementation risks |
| Coding completed and no open PR exists for the story branch | Follow create-pr (commit/push as needed). PR title must start with the Jira user story id. Skip only when a PR already exists for that branch |
| `BLOCKED` plan or an active `BLOCKED` design decision | Human resolves the plan. Do not implement |
| Readiness fields disagree | Human repairs the handoff before coding |
| Plan package fails the execution-contract gate | Human or a resumed planner repairs the package |
| Step, acceptance, or coverage failure the coding-agent workflow says to stop on | Human resolves the contradiction or uncovered requirement. Do not write a completion report |

A valid acknowledgement is `humanAcknowledgement.decision` of exactly `proceed_as_is` or `risk_resolved`, written by the coding-agent skill after the human chooses it.
