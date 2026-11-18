# Planner Skill

Turns validated requirements into an implementation plan with integration test scenarios, structural boundary rules, per-architecture-unit class designs, unit test descriptions, and a solution skeleton spec. Brownfield plans use the architecture style already applied in the repo and write `plan.md` in the same turn as the skeleton. Skeleton approval is required for greenfield plans, and for brownfield plans only when Marvin is explicitly prompted to review the skeleton.

## Recognition in Cursor

This planner is a **project skill** located at `.cursor/skills/planner/SKILL.md`.

Cursor recognizes it automatically when you open this repository because project skills live under `.cursor/skills/`.

The skill includes `disable-model-invocation: true`, which makes it an **explicitly invoked** skill rather than one that is auto-applied from ambient context.

## Invoke with slash command

Because the skill name is `planner` and it is explicitly invoked, you can run it from the slash menu as:

```text
/planner
```

Then provide the request details in the same message, for example:

```text
/planner
Create an implementation plan.
Architecture style: Clean Architecture — domain / application / adapter / infrastructure
```

For an existing repo, point the planner at the relevant module. It uses the architecture style already applied there and does not ask you to pick a style:

```text
/planner @requirements/PROJ-123/ @src/main/java/com/example/orders/
Create an implementation plan for this change using the existing repo architecture and names.
```

You can also attach contracts, schemas, architecture docs, or AI context bank paths explicitly:

```text
/planner @requirements/PROJ-123/ @docs/context-bank/ @openapi.yaml @src/main/java/com/example/
Create an implementation plan.
```

## Install globally (optional)

If you want the same skill in other repositories, copy this skill directory into `~/.cursor/skills/`:

```bash
mkdir -p ~/.cursor/skills
rm -rf ~/.cursor/skills/planner
cp -R "$PWD/.cursor/skills/planner" ~/.cursor/skills/planner
```

After updates in this repo, re-run the copy command to refresh the global skill.

## Prerequisites

Run the **requirement-analyst** skill first. Planner prefers ticket-scoped outputs under `requirements/<ticket-id>/` and may use legacy `docs/requirements/` only while migrating older flows.

Readiness must be `READY_FOR_PLANNING` or `READY_WITH_RISKS`. If status is `BLOCKED`, planner stops without producing a plan.

If requirements are not found, a greenfield architecture style cannot be provided or confidently discovered, or a brownfield repo has no identifiable applied style, planner responds with an **Input inventory** and a **Cannot proceed** list. No skeleton or plan files are written until the required inputs are present and the readiness gates pass. `plan.md` waits for approval of the solution skeleton spec only when that review is required.

## Inputs

| Input | Location / format |
|-------|-------------------|
| Requirement analyst docs | Canonical: `requirements/<ticket-id>/`; or attached via `@` |
| Core files (required) | `assumptions.md`, `functional.md`, `invariants.md`, `policies.md`, `quality.md`, `conflicts-and-ambiguities.md`, `handoff.json` |
| Optional | `constraints.md` |
| Architecture style | Brownfield: the style already applied in the repo. Greenfield: provided by the user, discovered from AI context bank/docs/rules, or inferred from code evidence |
| AI context bank / repo guidance | Auto-discovered from common context/doc/rules paths; or attached via `@` |
| Contracts / schemas | `@` OpenAPI, Avro, Protobuf, JSON Schema files |
| Existing modules | Auto-discovered from the requested change context; or attached via `@` path or description |

Architecture source precedence:

Brownfield:

1. The style already applied in existing modules, dependency direction, source layout, and tests.
2. Trusted repo context only when it describes that same applied style.

A user-named style that differs is recorded as a design risk and does not replace the applied style.

Greenfield:

1. User-provided architecture style.
2. Trusted repo context such as AI context bank, architecture docs, ADRs, or repo rules.
3. Evidence inferred from modules, dependency direction, source layout, and tests.
4. Clarification from the user when evidence is missing or conflicting.

## Outputs

The planner is **Agent-only**. Once validation and readiness gates pass, it writes the skeleton artifacts. Greenfield plans, and brownfield plans where Marvin was explicitly prompted to review the skeleton, stop for approval before the plan package. Other brownfield plans write the plan package in the same turn.

| File | When | Content |
|------|------|---------|
| `requirements/<ticket-id>/plan/design-decisions.md` | Immediately after gates pass | Material `DD-NNN` records with evidence, alternatives, consequences, and affected steps |
| `requirements/<ticket-id>/plan/solution-skeleton-spec.md` | Immediately after `design-decisions.md` | Solution skeleton spec generated from the applied or selected architecture and the written design decisions, titled `<ticket-id> <implemented service name or short change name>` |
| `requirements/<ticket-id>/plan/integration-test-scenarios.md` | Step 16, after approval only when skeleton review is required | Summary table, Given-When-Then scenarios, acceptance coverage matrix; single source of truth for Step 0 scenario and `REQ-NNN` / `QR-NNN` coverage |
| `requirements/<ticket-id>/plan/plan.md` | Step 16, same rule | Planning mode, architecture and naming evidence, Step 0 reference to the integration-test artifact, Step 1 (architectural structure + boundary tests), Step 2..N (per-unit classes and unit tests), coverage sign-off |
| `requirements/<ticket-id>/plan/handoff.json` | Step 15a when review is required, then Step 16 with the plan package | Implementation readiness, skeleton-review state (`skeletonReviewRequired`, `skeletonReviewApproved`, `solutionSkeletonSpecUrl`), and the coding-agent handoff contract |

When skeleton review is required, publish `solution-skeleton-spec.md` and `design-decisions.md` to GitHub and paste separate blob URLs for both in chat, along with the implementation risks when acknowledgement is required. Ask for approval to write `plan.md`. Do not paste full artifact bodies into chat. When review is not required, the close names every written path and does not ask for skeleton approval.

The planner preserves the analyst's `minimumAcceptedScope` and `topPriorityItems` from the requirements handoff. Every minimum-scope item and every `critical` priority item must map to a plan step and verification.

## Next stage

`requirements/<ticket-id>/plan/handoff.json` is the handoff contract for the **coding-agent** skill. When skeleton review is required and not approved, it is written at that stop with `nextAction` `await_skeleton_approval` and no `plan.md`. It is written or updated with `plan.md` once review is approved or was not required. The coding agent requires skeleton approval only when `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true`. When `status` is `READY_FOR_IMPLEMENTATION` and that review gate is clear, the coding agent implements the plan without pausing; `READY_FOR_IMPLEMENTATION_WITH_ACK` stops and surfaces the implementation risks in chat before any code edits; `BLOCKED` stops before any implementation.

`status` and `requiresHumanAck` must agree: `READY_FOR_IMPLEMENTATION` pairs with `requiresHumanAck: false` and `pauseReason: null`; `READY_FOR_IMPLEMENTATION_WITH_ACK` pairs with `requiresHumanAck: true`, a non-empty `pauseReason`, and at least one `designRisks` entry. The JSON field remains `pauseReason` for compatibility, but planner-produced human-facing artifacts should present it as the acknowledgement reason rather than implying the planner itself is paused. The fields `humanAcknowledgement`, `implementationStatus`, and `completionReportPath` are reserved for the coding agent to populate after execution; the planner always writes them as `null`. When the coding agent populates `humanAcknowledgement`, its `decision` field is always exactly `proceed_as_is` or `risk_resolved` — any other value is not recognized as clearing the acknowledgement gate.

## Reference

- Skill (operational): [`SKILL.md`](./SKILL.md)
- Workflow (canonical execution): [`references/workflow.md`](./references/workflow.md) — phase-and-gate decision tree
- Supporting references (on-demand): [`references/`](./references/)
  - [`input-resolution.md`](./references/input-resolution.md) — Phase 1–2 path/file checks and inventory template
  - [`planning-rules.md`](./references/planning-rules.md) — Phase 4–5 drafting policy and gate criteria
  - [`brownfield-discovery.md`](./references/brownfield-discovery.md) — brownfield branch code study
  - [`output-contract.md`](./references/output-contract.md) — Phase 6 staged artifacts, approval gate, solution skeleton spec, mode behavior
  - [`template-guide.md`](./references/template-guide.md) — concrete examples, placeholder usage, and content-quality expectations
  - [`anti-patterns.md`](./references/anti-patterns.md) — common planning and output mistakes to avoid
- Templates: [`templates/`](./templates/)
- Downstream: [`coding-agent`](../coding-agent/README.md)
- Sequenced run: [`marvin`](../marvin/README.md) keeps this planner's interactive stops. Brownfield skeleton approval runs only when Marvin is explicitly prompted to review the skeleton.
