# Handoff contract

The pipeline does not own a third handoff file. It reads the two contracts the child skills already write.

## Upstream

| From | Input | Required shape |
|------|--------|----------------|
| User | Work item ID, source artifacts or an existing `requirements/<ticket-id>/`, and the implementation repo | One ticket per run |
| User at a pause | An answer, steering notes, an approval, or an acknowledgement decision | Only the decision the active gate asked for |
| Requirement analyst | `requirements/<ticket-id>/handoff.json` | `nextAction` `run_planner` before Phase 2 |
| Planner | `requirements/<ticket-id>/plan/handoff.json` plus sibling plan artifacts | `nextAction` `run_coding_agent` before Phase 3 |

### Analyst handoff, to leave Phase 1

| Field | Advance only when |
|-------|-------------------|
| `status` | `READY_FOR_PLANNING` or `READY_WITH_RISKS` |
| `requiresHumanInput` | `false` |
| `blockingIssues` | `[]` |
| `nextAction` | `run_planner` |
| `plannerInputPath` | `requirements/<ticket-id>/` |

`READY_WITH_RISKS` still carries `trackedRisks` into the planner. It does not clear a human gate by itself.

### Plan handoff, to leave Phase 2

Written with `plan.md`, and also written earlier when skeleton review is required and not yet approved. On greenfield, and on brownfield when Marvin was explicitly prompted to review the solution skeleton spec, `plan.md` is written only after human approval. That approval is `skeletonReviewApproved: true` on this handoff. On other brownfield plans the plan package is written in the same turn as the skeleton, with `skeletonReviewRequired: false`. A later session reads these fields and does not infer them from chat.

| Field | `READY_FOR_IMPLEMENTATION` | `READY_FOR_IMPLEMENTATION_WITH_ACK` | `BLOCKED` |
|-------|----------------------------|--------------------------------------|-----------|
| `requiresHumanAck` | `false` | `true` | `true` |
| `pauseReason` | `null` | Non-empty acknowledgement reason | Non-empty |
| `designRisks` | May be empty | At least one entry | At least one entry when risks caused the block |
| `humanAcknowledgement` | `null` until coding agent, if ever | `null` until the human chooses and the coding agent records it | `null` |
| `nextAction` | `run_coding_agent` | `run_coding_agent` | Do not implement |
| `skeletonReviewRequired` | `false`, or `true` with `skeletonReviewApproved` `true` | same | same |
| `skeletonReviewApproved` | `null` when review was not required; `true` when it was required and approved | same | same |
| `solutionSkeletonSpecUrl` | `null` when review was not required; otherwise the GitHub blob URL | same | same |

`status` and `requiresHumanAck` must agree. A mismatch is a human-resolution stop, not a license to code.

An unapproved required review does not leave Phase 2. That handoff has `skeletonReviewRequired` `true`, `skeletonReviewApproved` `false`, a GitHub blob URL in `solutionSkeletonSpecUrl`, and `nextAction` `await_skeleton_approval`, whatever the intended `status` is.

Accepted `humanAcknowledgement.decision` values are only `proceed_as_is` and `risk_resolved`.

## Downstream

| To | Output | Contract |
|----|--------|----------|
| Planner | Analyst package under `requirements/<ticket-id>/` | Unchanged analyst skill outputs |
| Coding agent | `requirements/<ticket-id>/plan/` | Planner package. Skeleton approval blocks coding only when `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true` |
| User | Stage summary plus `templates/human-pause.md` in the final reply when a gate hits | Names the artifact paths and the decision needed. Channel-agnostic (Slack / IDE / CLI); not AskQuestion |
| User, on skeleton review | Separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` | Skeleton URL also stored in `solutionSkeletonSpecUrl` |
| User, on completion | Coding-agent `completion-report.md` path, plan `implementationStatus`, and the story-branch PR URL | Coding agent remains the writer of completion fields. Marvin opens the PR in Step 9 when missing |

The pipeline must not rewrite planner-owned readiness fields and must not write `humanAcknowledgement`, `implementationStatus`, or `completionReportPath` itself. The planner may set `solutionSkeletonSpecUrl` when it publishes a required review whose URL was null.

## Re-invocation

Yes. Resume `/marvin` after any human gate. Re-resolve Phase 0 from artifacts and the new user message. A resume that writes runs workflow Step 1b again so the story branch is current before that write. Do not write the resume on the previous branch.

Re-invocation is not approval and not acknowledgement. A resume with no new decision repeats the current **STOP**.
