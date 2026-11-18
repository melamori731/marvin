# Planner evals

Behavioral fixtures for the planner workflow after the evidence-first, approve-then-write-plan rewrite.

## What "pass" means

A scenario passes when the planner follows the expected branch, writes `design-decisions.md` and `solution-skeleton-spec.md` only after validation succeeds, and avoids the old Plan-mode preview workflow. Greenfield plans stop for skeleton approval and do not write `plan.md` until that approval. Brownfield plans use the architecture style already applied in the repo and write `plan.md` in the same turn unless Marvin was explicitly prompted to review the skeleton.

## Minimum coverage

1. Greenfield happy path: ready requirements plus explicit architecture produce `design-decisions.md` and `solution-skeleton-spec.md`, publish both with separate GitHub blob links, then stop for approval without writing `plan.md`
2. Brownfield path: the plan uses the architecture style already applied in the repo, writes the skeleton and the plan package in the same turn, and does not ask for skeleton approval
3. Blocked path: missing planning inputs stop the run before any artifact or solution-skeleton-spec write
4. Skeleton write fallback path: `solution-skeleton-spec.md` write failure reports the exact error, preserves written `design-decisions.md`, does not write `plan.md`, and avoids substitute outputs until the user asks for another retry
5. Approved plan-write path: after explicit human approval when skeleton review was required, write `integration-test-scenarios.md`, `plan.md`, and `handoff.json`

## Regression markers

- Do not require `SwitchMode`
- Do not paste full artifact bodies into chat
- Do not wait to save `design-decisions.md` or `solution-skeleton-spec.md` after readiness gates pass
- Do wait for explicit human approval before writing `plan.md` when skeleton review is required
- Do not wait for skeleton approval on a brownfield plan unless Marvin was explicitly prompted to review the skeleton
- Do not ask a brownfield plan to choose an architecture style when the repo already applies one
- When a human must review the skeleton, push both review files and paste separate GitHub blob URLs for `solution-skeleton-spec.md` and `design-decisions.md` in chat
- Do not write a solution-skeleton-spec canvas
- Do report the exact write error when the fallback branch is exercised
- Do not create substitute artifact files when `solution-skeleton-spec.md` write fails
- Do not retry `solution-skeleton-spec.md` without user confirmation
- Do not write a handoff with `nextAction` `run_coding_agent`, and do not tell `coding-agent` it can start, until `plan.md` is written after approval. A review-pending handoff at the skeleton stop is allowed only with `skeletonReviewApproved` false and `nextAction` `await_skeleton_approval`
