# Coding Agent Completion Report

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | [e.g. ECCS-123] |
| **Plan path** | [e.g. requirements/ECCS-123/plan/plan.md] |
| **Handoff path** | [e.g. requirements/ECCS-123/plan/handoff.json] |
| **Design decisions path** | [e.g. requirements/ECCS-123/plan/design-decisions.md] |
| **Outcome** | COMPLETE \| AWAITING_HUMAN \| BLOCKED |

## Implemented steps

| Step | Summary of implementation | Command | Result | Output |
|------|---------------------------|---------|--------|--------|
| Step 0 | [What changed for coverage and test scaffolding] | `<command>` | pass \| blocked | [verification-logs/step-0.txt](verification-logs/step-0.txt) |
| Step N | [What changed] | `<command>` or Manual: [note] | pass \| blocked | [verification-logs/step-N.txt](verification-logs/step-N.txt) or n/a |

If Command is a real test, build, or lint command, Output is a relative markdown link to that captured file. Every captured file starts with `command:` / `cwd:` / `exit_code:`. Test logs then need a runner stream (suite or test file, pass/fail/skip counts, overall result; Maven `Tests run:` / `BUILD SUCCESS` is one example). Build and lint logs keep that tool's own output; do not invent Surefire lines. If Command is `n/a` or `Manual: ...`, Output is `n/a` — do not invent a log. Do not cite logs captured with quiet flags (`-q`, `--quiet`, `--silent`).

## Design decision conformance

| Decision | Status | Evidence in implementation |
|----------|--------|----------------------------|
| DD-001 | applied | [Touched files, tests, or rationale] |

## Final acceptance

| Check | Result | Output |
|-------|--------|--------|
| Project compiles or builds cleanly | pass \| blocked \| n/a | [verification-logs/final-build.txt](verification-logs/final-build.txt) or n/a |
| No new linter or static-analysis failures remain | pass \| blocked \| n/a | [verification-logs/final-lint.txt](verification-logs/final-lint.txt) or n/a |
| Required structural boundary tests pass | pass \| blocked \| n/a | [verification-logs/final-boundary.txt](verification-logs/final-boundary.txt) or n/a |
| Required unit tests pass | pass \| blocked \| n/a | [verification-logs/final-unit.txt](verification-logs/final-unit.txt) or n/a |
| Required integration tests pass | pass \| blocked \| n/a | [verification-logs/final-integration.txt](verification-logs/final-integration.txt) or n/a |

## Coverage sign-off

| ID | Planned verification | Result | Output |
|----|----------------------|--------|--------|
| REQ-001 | [Integration test or validation] | pass \| blocked | [verification-logs/final-integration.txt](verification-logs/final-integration.txt) |
| QR-001 | [Integration test or manual validation] | pass \| blocked \| manual | [verification-logs/...](verification-logs/...) or n/a |
| INV-001 | [Unit test] | pass \| blocked | [verification-logs/final-unit.txt](verification-logs/final-unit.txt) |
| POL-001 | [Unit test] | pass \| blocked | [verification-logs/final-unit.txt](verification-logs/final-unit.txt) |

## Requirement-test coverage gate

Run `scripts/requirement-test-coverage-gate.py` before this report exists. Do not fill this section from memory. This command is not a Gate 4A `verification-logs/` row; link **Result JSON** only.

| Field | Value |
|-------|-------|
| **Command** | `python3 .cursor/skills/coding-agent/scripts/requirement-test-coverage-gate.py <repo-root> <plan-dir>` |
| **Result JSON** | [requirement-test-coverage.json](requirement-test-coverage.json) |
| **Passed** | true \| false |
| **Uncovered IDs** | none \| [REQ-003, ...] |
| **Contracts detected** | none \| [openapi.yaml, ...] |
| **Contract tests** | none \| [path, ...] |
| **Contract failures** | none \| [gate messages] |

## Latest touched paths

- `path/to/file`

## Remaining follow-up

- [Only include real manual follow-up, acknowledgement, or blocker details]
