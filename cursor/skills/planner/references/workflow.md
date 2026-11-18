# Workflow (Decision Tree)

Canonical execution path for the planner skill. Follow phases in order. Do not skip gates. Do not draft plan content before Phase 4. Skeleton review is required for greenfield plans, and for brownfield plans only when the user explicitly prompted Marvin to review or approve the solution skeleton spec. On those paths, do not write `plan.md` until the human approves the written solution skeleton spec and design decisions. On a brownfield plan without that Marvin prompt, write the plan package in the same turn as the skeleton and do not ask for skeleton approval. This workflow is agent-only.

Supporting detail:
- Phase 1–2 checks: `references/input-resolution.md`
- Brownfield branch: `references/brownfield-discovery.md`
- Drafting policy: `references/planning-rules.md`
- Artifact authoring examples: `references/template-guide.md`
- Common mistakes: `references/anti-patterns.md`
- Output, approval gate, and mode behavior: `references/output-contract.md`

## Anti-rationalization

Do not continue when:
- a greenfield architecture is only weakly guessed from naming while repo guidance conflicts
- a brownfield plan asks the human to pick an architecture style when the repo already applies one
- a missing `minimumAcceptedScope` mapping is downgraded into a mere design risk
- required-input gates have not passed but plan prose is drafted anyway
- `plan.md` is written before skeleton approval when review is required (greenfield, or Marvin was explicitly prompted to review or approve the solution skeleton spec)
- a brownfield plan without that Marvin prompt stops to wait for skeleton approval
- a `critical` priority item is omitted because it seems hard to implement

---

## Phase 0: Confirm Agent write capability

### Step 0: Verify writable execution context

Confirm the current execution context can write the planner's required artifacts under `requirements/<ticket-id>/plan/`.

**Gate 0A — Running in Agent mode with write access?**

| Result | Action |
|--------|--------|
| Yes | → Phase 1 |
| No | **STOP** — tell the user to rerun `/planner` in Agent mode because this skill must write the solution skeleton spec, design decisions, and the plan artifacts |

---

## Phase 1: Resolve Requirements Inputs

### Step 1: Locate requirements base path

Try in order (see `input-resolution.md` for detail):

1. User-provided or attached `requirements/<ticket-id>/`
2. Work item path from Requirement Analyst `handoff.json`
3. Legacy `docs/requirements/` or `requirements/` (migration only)
4. User-attached `@` paths

**Gate 1A — Base path found?**

| Result | Action |
|--------|--------|
| Yes | → Step 2 |
| No | **STOP** — output `## Cannot proceed` with missing-path message |

### Step 2: Validate required files

Required files: `assumptions.md`, `functional.md`, `invariants.md`, `policies.md`, `quality.md`, `conflicts-and-ambiguities.md`, `handoff.json`

**Gate 1B — All required files present?**

| Result | Action |
|--------|--------|
| Yes | → Step 3 |
| No | **STOP** — output `## Cannot proceed` listing each missing file |

### Step 3: Output Input inventory

Fill the inventory template from `input-resolution.md` before continuing.

→ Phase 2

---

## Phase 2: Resolve Planning Context

### Step 4: Discover repo context

Try in order (see `input-resolution.md`):

1. AI context bank / equivalent directories
2. Repository guidance files
3. User-attached `@` paths
4. Nearby source and test modules

Record findings in the Input inventory.

### Step 5: Determine planning mode

| Mode | Condition |
|------|-----------|
| Greenfield | No relevant existing implementation, or user asks to plan from scratch |
| Brownfield | Request modifies, extends, or integrates with existing code |
| Unclear | Cannot determine from inputs |

**Gate 2A — Planning mode determined?**

| Result | Action |
|--------|--------|
| Greenfield or Brownfield | → Step 6 |
| Unclear | **STOP** — ask user to clarify greenfield vs brownfield |

If **Brownfield** → read `references/brownfield-discovery.md` before Step 6. The applied architecture style comes from that study.

### Step 6: Determine architecture style

**Brownfield.** The architecture style is the one already applied in the repository. Read it from the code in use: package and module boundaries, dependency direction, test layout, and naming. Use trusted repo docs only when they describe that same applied style.

Do not ask the human to provide or choose a style. A user-named style that differs from the applied style does not govern the plan. Record that difference as a design risk and continue with the applied style.

Run the validator on the applied style:

```bash
python3 .cursor/skills/planner/scripts/architecture-discovery-validator.py <repo-root> "<applied-style>"
```

Keep the JSON as evidence in the plan header. `confidence: low`, a non-empty `conflicts[]`, or `recommendation: stop` does not stop the plan when the applied style was identified. Do not replace the validator result with free-form confidence prose.

**Gate 2B — Brownfield architecture**

| Result | Action |
|--------|--------|
| Applied style identified from the repo | → Phase 3 |
| No applied style can be identified | **STOP** — ask the human to point at the modules that already show the style. Do not offer a menu of new styles. Do not draft the plan. |

**Greenfield.** Check in order:

1. User-provided architecture style
2. Trusted repo context (AI context bank, architecture docs, ADRs, repo rules)
3. Code evidence (package boundaries, dependency direction, test layout)

If steps 2-3 produce a candidate architecture style, run the same validator command with that candidate. Use the JSON output as the gate input.

**Gate 2B — Greenfield architecture classification**

| Result | Action |
|--------|--------|
| **User-provided** and trusted repo context does not contradict it | → Phase 3 |
| **User-provided** but trusted repo context conflicts with it | **STOP** — list the contradiction and ask the user which architecture should govern the plan. Do not draft the plan. |
| Validator returns `confidence: high`, empty `conflicts[]`, `recommendation: proceed` | → Phase 3 |
| Validator returns `confidence: medium`, empty `conflicts[]`, `recommendation: document` | Record validator evidence in the plan header and carry architecture uncertainty into Design risks → Phase 3 |
| Validator returns `confidence: low`, any non-empty `conflicts[]`, or `recommendation: stop` | **STOP** — list the candidate architecture, validator conflicts, and 2-3 plausible alternatives; ask the user to clarify. Do not draft the plan. |
| No candidate style found from Steps 1-3 | **STOP** — ask user to provide architecture style or point to repo guidance |

→ Phase 3

---

## Phase 3: Validate Planning Readiness

### Step 7: Check assumptions readiness

Read `assumptions.md` and determine: `READY_FOR_PLANNING`, `READY_WITH_RISKS`, or `BLOCKED`

### Step 8: Validate handoff metadata

Read `handoff.json`. Preserve work item ID, requirements path, planner next-action intent, `topPriorityItems`, and `minimumAcceptedScope`.

Validate every `topPriorityItems[].id` and `minimumAcceptedScope` ID exists in requirement outputs.

### Step 9: Carry conflicts and ambiguities

Read `conflicts-and-ambiguities.md`. Carry open `CA-NNN` rows into planning risks or blockers.

**Gate 3A — Readiness status**

| Status | Action |
|--------|--------|
| `READY_FOR_PLANNING` | → Phase 4 |
| `READY_WITH_RISKS` | Carry risks into plan → Phase 4 |
| `BLOCKED` | **STOP** — report blocking issues. Do not draft the plan. |
| Malformed handoff (missing IDs) | **STOP** — report malformed handoff metadata |

→ Phase 4

---

## Phase 4: Draft Plan Artifacts

### Step 10: Read planning policy

Read `references/planning-rules.md` before drafting.

### Step 11: Read templates

Read `references/template-guide.md` once before drafting the first artifact, then read the relevant files from `templates/` before authoring each artifact.

If the draft starts to drift from the template structure or invent extra output files, read `references/anti-patterns.md` before continuing.

### Step 12: Build plan content

Produce:
- Integration test scenarios (`REQ-NNN` / `QR-NNN` coverage)
- Plan steps with class assignments, invariants, policies, and tests
- `design-decisions.md` content with stable `DD-NNN` IDs for every material decision

Apply all constraints from `planning-rules.md` while drafting.

→ Phase 5

---

## Phase 5: Final Quality Gate

Run every gate before presenting or writing outputs. Use checklist items from `planning-rules.md` (Plan authoring completeness).

**Gate 5A — Scope mapped?**

- [ ] Every in-scope `REQ-NNN`, `QR-NNN`, `INV-NNN`, and `POL-NNN` mapped
- [ ] Every plan step has explicit scope and dependencies

| Result | Action |
|--------|--------|
| Pass | → Gate 5B |
| Fail | **STOP** — surface missing mappings as risks or missing inputs |

**Gate 5B — Critical and minimum scope preserved?**

- [ ] Every `minimumAcceptedScope` ID maps to a plan step and verification
- [ ] Every `critical` item from `topPriorityItems` maps to a plan step and Coverage sign-off

| Result | Action |
|--------|--------|
| Pass | → Gate 5C |
| Fail (unmapped critical item) | Mark plan `BLOCKED` — do not present as ready |
| Fail (unmapped minimum scope) | **STOP** — do not downgrade to design risk |

**Gate 5C — Decisions recorded and statuses aligned?**

- [ ] Every material decision has a `DD-NNN` entry with evidence
- [ ] Decision statuses consistent with implementation readiness
- [ ] No unresolved material choices hidden only in plan prose

| Result | Action |
|--------|--------|
| Pass | → Gate 5D |
| Fail | Record as `REQUIRES_ACK` or `BLOCKED` in decision record; align handoff status |

**Gate 5D — Class structure justified and minimal?**

- [ ] Class set is minimal for planned behavior and architecture style
- [ ] No indirection-only classes without architectural value
- [ ] Each split justified by reuse, boundary, or independent change pressure
- [ ] Template structure fully filled with concrete content

| Result | Action |
|--------|--------|
| Pass | → Phase 6 |
| Fail | Surface gaps in Design risks; do not present as `READY_FOR_IMPLEMENTATION` |

→ Phase 6

---

## Phase 6: Write the Solution Skeleton Spec, Then the Plan

### Step 13: Choose intended readiness status

Record the intended implementation readiness that will go into `handoff.json` when the plan package is written:

| Status | When |
|--------|------|
| `READY_FOR_IMPLEMENTATION` | Safe to implement without human review |
| `READY_FOR_IMPLEMENTATION_WITH_ACK` | Material risks require acknowledgement |
| `BLOCKED` | Contradictions or missing information make implementation unsafe |

Align the intended `handoff.json` fields per `planning-rules.md` (Implementation readiness and handoff). Do not write `handoff.json` in this step.

**Gate 6A — Intended handoff consistency**

- [ ] Intended `status` and `requiresHumanAck` agree
- [ ] `READY_FOR_IMPLEMENTATION_WITH_ACK` has a non-empty acknowledgement reason and at least one `designRisks` entry
- [ ] Coding-agent execution fields will be left as `null` when `handoff.json` is later written

| Result | Action |
|--------|--------|
| Pass | → Step 14 |
| Fail | Fix inconsistency before writing review artifacts |

### Step 14: Write solution skeleton spec and design decisions

Follow `references/output-contract.md`.

If this turn is a **resume after explicit human approval** of already-written review artifacts, skip to Step 16.

Otherwise write, in order:

1. `design-decisions.md`
2. `solution-skeleton-spec.md`, generated from architecture discovery plus the written design decisions, titled `<ticket-id> <implemented service name or short change name>`

Do not write `plan.md`, `integration-test-scenarios.md`, or `handoff.json` in this step.

**Gate 6B — Review artifacts written?**

| Result | Action |
|--------|--------|
| Both files written | → Step 15 |
| `design-decisions.md` write failed | **STOP** — report the exact error; write nothing else |
| `solution-skeleton-spec.md` write failed | Follow the write fallback in `output-contract.md`; do not write `plan.md` |

### Step 15: Decide whether the skeleton needs review

**Gate 6C — Is solution skeleton spec review required?**

If `requirements/<ticket-id>/plan/handoff.json` already has `skeletonReviewRequired: true` and `skeletonReviewApproved` is not `true`, review stays required. Do not clear it because this message omitted the original prompt.

Otherwise, review is required only when planning mode is greenfield, or the user explicitly prompted Marvin to review or approve the solution skeleton spec. Record that decision on the handoff in this same turn. Do not leave it only in chat.

Explicit prompts include "review the skeleton", "review the solution skeleton spec", "approve the skeleton before the plan", and "ask me to approve the skeleton". These are not that prompt: `/planner`, a bare `/marvin`, "plan this", "carry this through implementation", "finish the pipeline", and "implement it". An explicit prompt in this turn sets `skeletonReviewRequired` to `true` and `skeletonReviewApproved` to `false` before the coding agent runs, including when `plan.md` already exists.

| Result | Action |
|--------|--------|
| Greenfield, Marvin was explicitly prompted, or the handoff already says review is required and not approved | → Step 15a |
| Brownfield, Marvin was not explicitly prompted, and no handoff says review is still required | → Step 16 in this same turn. Do not ask for skeleton approval. Write `skeletonReviewRequired: false`. The coding agent does not require approval unless a later handoff says it is required and not approved. |

### Step 15a: Stop for skeleton review

Publish the spec using **Skeleton review publication** in `references/output-contract.md`. Then write `requirements/<ticket-id>/plan/handoff.json` from `templates/handoff.json` with the intended readiness fields and:

- `skeletonReviewRequired`: `true`
- `skeletonReviewApproved`: `false`
- `solutionSkeletonSpecUrl`: the GitHub blob URL just published
- `nextAction`: `await_skeleton_approval`

Leave `humanAcknowledgement`, `implementationStatus`, and `completionReportPath` as `null`. Do not write `plan.md` or `integration-test-scenarios.md`. If `plan.md` already exists, leave it in place and still set `skeletonReviewApproved` to `false`. Then **STOP**.

The chat pastes separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` (not only the skeleton; `solutionSkeletonSpecUrl` holds the skeleton link) and states the intended readiness status. When the intended status is `READY_FOR_IMPLEMENTATION_WITH_ACK`, the same chat lists the acknowledgement reason and each implementation risk. Say that `plan.md` will be written only after explicit approval, and that the coding agent reads this handoff rather than chat history.

Treat as approval only an explicit user instruction to approve, proceed, or write the plan. Treat requested changes as a revise-and-rewait loop: update `design-decisions.md` and `solution-skeleton-spec.md`, publish both again, store the new skeleton blob URL in `solutionSkeletonSpecUrl`, paste separate links for both files, keep `skeletonReviewApproved` `false`, then **STOP**. Do not treat silence, a later `/planner` or `/marvin` rerun, or `READY_FOR_IMPLEMENTATION` as approval.

If intended status is `BLOCKED`, do not offer to write `plan.md` until the blockers are resolved and review artifacts are updated.

### Step 16: Write the plan package

Write this step after Step 15a approval when Gate 6C required review. Write it in the same turn as Step 14 when Gate 6C skipped review.

Write, in order:

1. `integration-test-scenarios.md`
2. `plan.md`
3. `handoff.json`

On the handoff, set `skeletonReviewRequired` from Gate 6C. When review was required, set `skeletonReviewApproved` to `true` and keep `solutionSkeletonSpecUrl`. When review was not required, set `skeletonReviewApproved` to `null` and `solutionSkeletonSpecUrl` to `null`. Set `nextAction` to `run_coding_agent` unless status is `BLOCKED`. Do not set `skeletonReviewApproved` from a missing chat prompt.

The written `plan.md` must follow the written decisions. If writing it would add or change a material decision, update `design-decisions.md` and `solution-skeleton-spec.md` first. Return to Step 15a when Gate 6C required review. When review was skipped, continue this step after those updates and publish the spec only if a later turn makes review required.

After the three files are written, refresh `solution-skeleton-spec.md` only to point at the written plan path. Do not add decisions that exist only in the skeleton spec.

Return a concise completion summary that names every written path, the final readiness status, and whether downstream implementation can start. On the brownfield skip path, do not ask for skeleton approval in that summary.
