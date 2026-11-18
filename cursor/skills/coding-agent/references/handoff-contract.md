# Coding-agent handoff contract

The coding agent consumes planner outputs and owns only the execution-result fields in `handoff.json`.

## Upstream expectations

| From | Input | Format |
|------|-------|--------|
| User | A `plan.md` path or equivalent plan directory | Chat + repo path |
| Planner | `plan.md`, `handoff.json`, `design-decisions.md` | Markdown + JSON |
| Planner | `integration-test-scenarios.md` when Step 0 or Coverage sign-off references it | Markdown |
| Workspace | Existing codebase plus runnable verification commands | Working tree |
Canonical planner output path is `requirements/<ticket-id>/plan/`, but the coding agent may use another plan directory when the same sibling artifact set exists there.

## Downstream expectations

| To | Output | Contract |
|----|--------|----------|
| Working tree | Product source + test updates | Must follow `plan.md` in order, preserve active `DD-NNN` decisions, cover every input requirement with a respective test, and add contract tests wired to `REQ-NNN` when a contract is provided |
| Plan directory | `verification-logs/` plus `completion-report.md` plus `requirement-test-coverage.json` | Each test, build, or lint command has a captured `verification-logs/` file (test logs: runner stream with suite/file, counts, overall result; build/lint logs: tool-appropriate output). Manual/n/a rows do not invent logs. Coverage-gate evidence is `requirement-test-coverage.json`, not a `verification-logs/` file. The report links those files instead of pasting logs |
| Planner handoff | Updated `handoff.json` execution fields | Only coding-agent-owned fields may change |
| User | Completion summary or pause reason | Must name the blocking step, uncovered requirement IDs, or finished verification |

## `handoff.json` ownership

### Planner-owned fields

The coding agent reads but does not silently rewrite these fields:

- `ticketId`
- `requirementsPath`
- `planPath`
- `designDecisionsPath`
- `status`
- `requiresHumanAck`
- `pauseReason`
- `designRisks`
- `skeletonReviewRequired`
- `skeletonReviewApproved`
- `solutionSkeletonSpecUrl`
- `topPriorityItems`
- `minimumAcceptedScope`
- `nextAction`
- `codingAgentInstruction`

If these fields are inconsistent, the coding agent stops and asks for a repaired handoff.

The coding agent may write `solutionSkeletonSpecUrl` only when skeleton review is required, not approved, and that field is null, after a successful skeleton review publication. It does not set `skeletonReviewApproved` or change `nextAction`.

Skeleton-review fields agree only in these shapes:

| `skeletonReviewRequired` | `skeletonReviewApproved` | `solutionSkeletonSpecUrl` | `nextAction` while review is the gate |
|--------------------------|--------------------------|---------------------------|----------------------------------------|
| `true` | `false` | GitHub blob URL | `await_skeleton_approval` |
| `true` | `true` | GitHub blob URL, or `null` if the URL was not retained | `run_coding_agent` unless `status` is `BLOCKED` |
| `false` | `null` | `null` | `run_coding_agent` unless `status` is `BLOCKED` |

Any other combination, or a missing field, is an inconsistent handoff. The coding agent does not treat chat history as a substitute for these fields and does not set `skeletonReviewApproved`.

### Coding-agent-owned fields

The coding agent may populate or refresh only these fields after or during execution:

#### `humanAcknowledgement`

Use only when `status` is `READY_FOR_IMPLEMENTATION_WITH_ACK` and the user explicitly clears the risk.

```json
{
  "decision": "proceed_as_is",
  "acknowledgedAt": "2026-08-27T17:30:00Z",
  "rationale": "User accepted the carried design risk after review."
}
```

Allowed `decision` values are exactly:

- `proceed_as_is`
- `risk_resolved`

#### `implementationStatus`

Use this object as the execution summary stored in `handoff.json`:

```json
{
  "status": "COMPLETE",
  "updatedAt": "2026-08-27T18:05:00Z",
  "summary": "Implemented all planned steps and passed final acceptance.",
  "latestTouchedPaths": [
    "src/example.ts",
    "test/example.test.ts"
  ]
}
```

Allowed `status` values are:

- `IN_PROGRESS`
- `AWAITING_HUMAN`
- `BLOCKED`
- `COMPLETE`

#### `completionReportPath`

Relative repo path to the final report, normally:

`requirements/<ticket-id>/plan/completion-report.md`

or the equivalent sibling path for a non-canonical plan directory.

## Re-invocation

The coding agent may be re-invoked when:

1. The user provides a missing acknowledgement for `READY_FOR_IMPLEMENTATION_WITH_ACK`
2. The planner updated the plan package and wants implementation retried
3. A prior coding-agent run stopped on an implementation blocker and the user wants to retry with updated inputs

On re-invocation, keep the same plan directory and preserve prior execution-result fields unless they are being updated by the current run.
