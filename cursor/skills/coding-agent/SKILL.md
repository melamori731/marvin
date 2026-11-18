---
name: coding-agent
description: Build planned code changes from a `plan.md` plus sibling `handoff.json` and `design-decisions.md`. Do not require solution skeleton spec approval unless `handoff.json` has `skeletonReviewRequired` true and `skeletonReviewApproved` is not true. When human acknowledgement is required, list the implementation risks in chat. Use when the user says `Build requirements/<ticket-id>/plan/plan.md` or `Build <plan-directory>/plan.md`, asks to execute a saved implementation plan step by step, or wants each step acceptance criteria applied in the agent loop. Do NOT use when requirements are still ambiguous, when a plan has not been written, or for reviewer-only work; use `critique-and-revise-reviewer` or another dedicated review workflow instead.
disable-model-invocation: true
---
# Coding Agent

## Use this skill when

- The user asks to build from an existing `plan.md`
- Planner outputs already exist and `handoff.json` says `nextAction: run_coding_agent`
- The work should follow plan steps in order, apply each step's acceptance criteria, and preserve planned verification

## Required inputs

- A target `plan.md` path
- Sibling `handoff.json`
- Sibling `design-decisions.md`
- The implementation repo and its runnable tests or validation commands
- Optional contract or schema files when the plan or requirements package provides them
- Optional `integration-test-scenarios.md` when the plan references Step 0 coverage

## Execution

Read `references/workflow.md` first. Do not edit product code before Phase 1 says implementation may start.

Supporting references:

| Reference | When |
|-----------|------|
| `references/workflow.md` | Always; canonical phase-and-gate execution |
| `references/handoff-contract.md` | Before interpreting planner outputs or writing coding-agent-owned handoff fields |
| `references/rules.md` | Before implementing steps or deciding how to apply tests and `DD-NNN` decisions |
| `references/anti-patterns.md` | When tempted to skip steps, merge steps, skip the coverage gate, or declare completion before final acceptance |
| `references/mode-behavior.md` | When pausing for acknowledgement or resuming after a prior stop |
| `templates/completion-report.md` | Before writing the final implementation report; test/build/lint command rows link to `verification-logs/` (test logs need a runner stream; build/lint logs need tool-appropriate output). Coverage-gate evidence is `requirement-test-coverage.json`. Manual and n/a rows stay n/a. |
| `templates/human-acknowledgement.json` | When persisting a required acknowledgement into `handoff.json` |
| `templates/implementation-status.json` | Before populating `handoff.json.implementationStatus` |
| `scripts/requirement-test-coverage-gate.py` | After Final acceptance, before writing `completion-report.md` |

## Mode behavior

- **Plan mode**: resolve the target artifact set, report readiness, and stop without editing files
- **Agent mode**: implement the plan step by step, run the planned verification (saving each test, build, or lint command's output under `verification-logs/`), apply final acceptance, run the requirement-test coverage gate, then write the completion artifacts only if that gate passes. The completion report must link to those log files instead of pasting command output. Each test log must include a runner stream a reviewer can read (which suite or test file ran, pass/fail/skip counts, overall result; Maven `Tests run:` / `BUILD SUCCESS` is an example). Build and lint logs use that tool's own output; do not invent a runner stream for lint, compile, n/a, or Manual rows. Coverage-gate evidence is `requirement-test-coverage.json`, not a `verification-logs/` file. Do not use quiet flags on test or build commands cited as evidence.
