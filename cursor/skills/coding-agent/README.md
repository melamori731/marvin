# Coding Agent Skill

Implements a saved plan package step by step, preserves planner design decisions, and runs planned verification plus the requirement-test coverage gate before writing completion artifacts.

## Recognition in Cursor

This is a project skill at `.cursor/skills/coding-agent/SKILL.md`.

It includes `disable-model-invocation: true`, so agents should invoke it explicitly when a plan package is ready to build.

## Invoke with slash command

Because the skill name is `coding-agent`, you can invoke it as:

```text
/coding-agent
Build requirements/<ticket-id>/plan/plan.md
Go through it step by step and apply each step acceptance criteria in the agent loop.
```

If the planner used a non-canonical sibling artifact directory, that alternative also works:

```text
/coding-agent
Build planning/<ticket-id>/plan.md
```

## Prerequisites

The plan directory must contain:

- `plan.md`
- `handoff.json`
- `design-decisions.md`

Prefer the planner's canonical path `requirements/<ticket-id>/plan/` when it exists. Alternative plan directories are acceptable only when the same sibling artifact set exists.

If `handoff.json.status` is:

- `READY_FOR_IMPLEMENTATION` - coding can start immediately
- `READY_FOR_IMPLEMENTATION_WITH_ACK` - coding stops until the user explicitly acknowledges the carried risk. The chat lists the implementation risks
- `BLOCKED` - coding does not start

The coding agent does not require approval of the solution skeleton spec. That review stops implementation only when `handoff.json` has `skeletonReviewRequired` true and `skeletonReviewApproved` is not true. The review chat pastes separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md`. A build request does not set `skeletonReviewApproved`. Acknowledgement and blocked plans still stop for the human.

## What the skill does

1. Validates the plan package and acknowledgement state
2. Executes Step 0 and the remaining plan steps in order
3. Applies each step's planned verification and acceptance criteria before moving on, capturing command output under `verification-logs/` without quiet flags on test/build evidence; test logs include a readable runner stream, while build and lint logs keep the tool's own output
4. Applies Final acceptance and Coverage sign-off, capturing those command outputs the same way
5. Runs `scripts/requirement-test-coverage-gate.py` and stops if any input requirement lacks a respective test, or if a provided contract lacks contract tests wired to `REQ-NNN`
6. Writes `completion-report.md` only after that gate passes, with markdown links to the log files, and updates the coding-agent-owned execution fields in `handoff.json`

## Outputs

After success, the skill writes:

- product code and tests in the repo working tree
- `verification-logs/` in the plan directory (captured stdout/stderr for each test, build, or lint command; test logs must include the runner stream — suite or test file, counts, overall result — not only framework logs; build/lint logs keep the tool's output)
- `requirement-test-coverage.json` in the plan directory
- `completion-report.md` in the plan directory, with relative links to those log files
- `handoff.json.humanAcknowledgement` when an acknowledgement branch was required
- `handoff.json.implementationStatus`
- `handoff.json.completionReportPath`

## References

- Operational entry point: [`SKILL.md`](./SKILL.md)
- Canonical workflow: [`references/workflow.md`](./references/workflow.md)
- Planner/coding contract: [`references/handoff-contract.md`](./references/handoff-contract.md)
- Implementation rules: [`references/rules.md`](./references/rules.md)
- Pause and transition behavior: [`references/mode-behavior.md`](./references/mode-behavior.md)
- Common mistakes: [`references/anti-patterns.md`](./references/anti-patterns.md)
- Starter artifacts: [`templates/`](./templates/)
- Coverage gate: [`scripts/requirement-test-coverage-gate.py`](./scripts/requirement-test-coverage-gate.py)
- Evaluation scenarios: [`evals/`](./evals/)
