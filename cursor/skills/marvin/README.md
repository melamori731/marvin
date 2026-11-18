# Marvin

Runs requirement analysis, planning, and implementation in that order for one work item. Before the first write of a turn, Marvin creates a branch named `<ticket-id>-<slug-of-the-user-story>` when that local branch does not exist, switches onto it, and does the rest of the turn's work there, for example `ECCS-4521-implement-this-or-that`. It does not stay on the previous branch. `ECCS-XXXX-emplement-tis-or-that` is that pattern, not a branch to create. Planner stays interactive. Human gates go in the final reply via the human-pause template in Slack, IDE, and CLI — not AskQuestion, and not self-answered. Greenfield skeleton review still needs an explicit human approval, and steering at that point updates the review artifacts, publishes both again, and waits. Brownfield plans use the repo's applied architecture and do not wait for skeleton approval unless Marvin is explicitly prompted to review the skeleton. That review chat pastes separate GitHub links for `solution-skeleton-spec.md` and `design-decisions.md`. When implementation risks need acknowledgement, the chat lists them. After coding completes, Marvin opens a PR for the story branch when one does not already exist. Blocked handoffs stay with the human.

## Invoke

```text
/marvin
Ticket: PROJ-123
Sources: @spec.md
```

Resume the same command after you answer a pause. A bare rerun is not approval and not acknowledgement.

## Stages

1. `requirement-analyst` until `requirements/<ticket-id>/handoff.json` may advance, or until you must resolve a question or a block
2. `planner` through design decisions and the solution skeleton spec. Greenfield, and brownfield only when Marvin is explicitly prompted to review the skeleton, stop for approval or steering. Other brownfield plans write the plan package in the same turn.
3. `coding-agent` when the plan is `READY_FOR_IMPLEMENTATION` and the plan handoff does not have an unapproved required skeleton review (`skeletonReviewRequired` true with `skeletonReviewApproved` not true). `READY_FOR_IMPLEMENTATION_WITH_ACK` stops and lists the implementation risks in chat. `BLOCKED` stops before coding. After coding completion, create-pr runs unless a PR already exists for the story branch.

## References

- Skill: [`SKILL.md`](./SKILL.md)
- Workflow: [`references/workflow.md`](./references/workflow.md)
- Human gates: [`references/human-gates.md`](./references/human-gates.md)
- Child skills: [`requirement-analyst`](../requirement-analyst/SKILL.md), [`planner`](../planner/SKILL.md), [`coding-agent`](../coding-agent/SKILL.md)
- Story branch: [`scripts/story-branch.py`](./scripts/story-branch.py)
