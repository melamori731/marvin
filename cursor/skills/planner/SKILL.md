---
name: planner
description: Write a solution skeleton spec and design decisions from requirement analyst outputs and the repo, then the implementation plan. Brownfield plans use the architecture style already applied in the repo and do not wait for skeleton approval unless Marvin is explicitly prompted to review the skeleton. Greenfield plans stop for that approval. Use when the user asks to plan implementation, map requirements to design, review architecture fit, or prepare a handoff to coding. Do NOT use for early requirements gathering, brainstorming, or when requirements are still ambiguous; use `requirement-analyst` first.
disable-model-invocation: true
---
# Planner

## Use this skill when

- The user asks for an implementation plan
- The user wants integration test scenarios in Given-When-Then form
- The user wants a layered implementation breakdown with classes, invariants, policies, and tests
- Requirement Analyst outputs exist or are expected to exist in the repo
- The user wants to plan changes for either a new repo or an existing codebase

## Required inputs

- Requirement Analyst outputs under `requirements/<ticket-id>/` (canonical). Legacy `docs/requirements/` or `requirements/` without a ticket subdirectory may be used only for backward compatibility during migration.
- Core files: `assumptions.md`, `functional.md`, `invariants.md`, `policies.md`, `quality.md`, `conflicts-and-ambiguities.md`, `handoff.json`
- Architecture style. Brownfield: the style already applied in the repo. Greenfield: user message, AI context bank / architecture docs / repo rules / existing code evidence, or explicit user confirmation when discovery is ambiguous.

## Execution

Read and follow **`references/workflow.md`** — the canonical phase-and-gate decision tree. Do not draft plan content before Phase 4. Do not write `plan.md` before skeleton approval when Gate 6C requires review. On a brownfield plan without an explicit Marvin prompt to review the skeleton, write the plan package in the same turn.

This skill is **Agent-only**. If the current execution context cannot write the required artifacts, stop and tell the user to rerun `/planner` in Agent mode.

Supporting references (load at the workflow branch that needs them):

| Reference | When |
|-----------|------|
| `references/input-resolution.md` | Phase 1–2 path/file checks and inventory template |
| `references/brownfield-discovery.md` | Gate 2A selects brownfield mode |
| `references/planning-rules.md` | Phase 4 drafting policy and Phase 5 gate criteria |
| `references/output-contract.md` | Phase 6 staged delivery, approval gate, and mode behavior |
| `references/template-guide.md` | Before drafting the first artifact; strong examples, placeholder usage, and content-quality expectations |
| `references/anti-patterns.md` | When drafting starts to drift; common planning and output mistakes |
| `templates/` | Before authoring each artifact |

## Mode behavior

- **Agent mode only**: validate inputs, draft artifacts, and write `design-decisions.md` and `solution-skeleton-spec.md` titled `<ticket-id> <implemented service name or short change name>`. Brownfield uses the applied repo architecture. Stop for skeleton approval only when Gate 6C requires it (greenfield, or Marvin was explicitly prompted to review the skeleton); that stop publishes both review files to GitHub and pastes separate blob URLs for each in chat, and lists implementation risks when acknowledgement is required. Otherwise write `integration-test-scenarios.md`, `plan.md`, and `handoff.json` in the same turn. Return a concise summary with the written paths and final readiness status.
