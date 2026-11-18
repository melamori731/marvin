# Coding-agent rules

Operational rules for interpreting planner outputs and implementing them safely.

## Skeleton and acknowledgement rules

- Do not require approval of `solution-skeleton-spec.md` before implementation.
- Require that approval only when `handoff.json` has `skeletonReviewRequired` `true` and `skeletonReviewApproved` is not `true`. Then stop. The chat must paste separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` (including `solutionSkeletonSpecUrl` for the skeleton). Do not decide this gate from conversation history, and do not set `skeletonReviewApproved`.
- When `status` is `READY_FOR_IMPLEMENTATION_WITH_ACK` and acknowledgement is missing, the chat must list the acknowledgement reason and every `designRisks` entry before asking for `proceed_as_is` or `risk_resolved`.

## Input and path rules

- Prefer the planner's canonical directory `requirements/<ticket-id>/plan/` when it exists.
- Support alternative plan directories only when `plan.md`, `handoff.json`, and `design-decisions.md` are siblings.
- Treat `integration-test-scenarios.md` as required whenever Step 0 or Coverage sign-off references it.
- If the plan directory contains stale or partially written artifacts that disagree with each other, stop and ask for a repaired plan package.

## Execution order rules

- Implement Step 0 first.
- Execute the remaining numbered plan steps in order.
- Do not merge, skip, or reorder steps unless the plan itself marks a step as already satisfied by existing code and you can cite evidence.
- Run the smallest covering verification and acceptance criteria for each step before moving on; save the broader final suite for Phase 3.
- Capture each test, build, or lint command's stdout and stderr into `<plan-dir>/verification-logs/` using the names in `references/workflow.md`. Do not treat the chat transcript as the log. Do not use quiet or silent flags on test or build commands cited as evidence. Test log bodies must be a runner stream a reviewer can read (suite or test file, pass/fail/skip counts, overall result). Build and lint logs must be tool-appropriate; do not fabricate a test runner stream. Manual and n/a checks do not get invented logs. The coverage-gate command writes `requirement-test-coverage.json`, not a `verification-logs/` file.

## Design decision rules

- Apply every active `DECIDED` decision.
- Apply `REQUIRES_ACK` decisions only after a valid `humanAcknowledgement` is present.
- Stop on any still-active `BLOCKED` decision.
- Preserve `SUPERSEDED` entries as history; do not implement them as current guidance.
- If the codebase proves an active decision unsafe or impossible, stop and surface the contradiction instead of silently drifting.

## Verification rules

- `integration-test-scenarios.md` is the single source of truth for Step 0 coverage of `REQ-NNN` and `QR-NNN`.
- Structural boundary tests are only for architecture boundaries; business invariants and policies belong in unit tests on their encapsulating classes.
- Every input `REQ-NNN`, `INV-NNN`, and `POL-NNN` must be covered by a respective automated test before completion. Every input `QR-NNN` must be covered by a test or by an explicit `Manual:` mapping in the plan package.
- If a contract or schema is provided in the requirements package, plan evidence, or attached plan inputs, implement contract tests and wire them to the input `REQ-NNN` IDs. Integration tests do not replace that wiring.
- Run `scripts/requirement-test-coverage-gate.py` after Final acceptance and before writing `completion-report.md`. Treat `"passed": false` as a stop, not as a reportable complete outcome.
- Final acceptance plus a passing coverage gate must be green before completion artifacts are written. Do not treat `completion-report.md` or `handoff.json` updates as substitutes for real verification.
- Manual validation is allowed only when the plan explicitly permits it and points to a path for later automation.

## Completion artifact rules

- Write `completion-report.md` into the same plan directory.
- In that report, attach each test, build, or lint command as a relative markdown link to its `verification-logs/` file. Do not paste command output into the report. Do not link a test log that lacks a runner stream. Do not require a runner stream in lint or compile logs. Use `n/a` for Manual and n/a rows. Link the coverage gate to `requirement-test-coverage.json`, not `verification-logs/`.
- Update only the coding-agent-owned `handoff.json` fields from `references/handoff-contract.md`.
- `implementationStatus.latestTouchedPaths` should list product paths changed during the coding-agent run, not the entire repo diff.
