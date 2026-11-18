# Planning And Output Anti-Patterns

Read this file when a draft starts to drift from the planner templates or when the output set begins to grow beyond the canonical artifacts.

## Anti-Pattern 1: Skipping Step 0

**Red flag:** The plan starts with implementation steps but `integration-test-scenarios.md` is missing, thin, or disconnected from `REQ-NNN` and `QR-NNN`.

**Why it happens:** The planner treats integration coverage as obvious or postpones it until after design.

**Fix:**

1. Draft `integration-test-scenarios.md` first.
2. Map every `REQ-NNN` to at least one scenario.
3. Map every `QR-NNN` to an integration test or an explicit manual validation note.
4. Do not continue to `plan.md` until Step 0 coverage is concrete.

**Bad example:**

```md
## Step 1 - Add order workflow

Implement the order feature and test it later.
```

**Good example:**

```md
## Step 0 - Integration tests

### `createOrder_validRequest_persistsOrder`

- **Requirements**: REQ-001, QR-002
- **Given**: A valid order request and a reachable persistence boundary
- **When**: The create-order endpoint is called
- **Then**: The order is persisted and a success response is returned
```

## Anti-Pattern 2: Too Many Classes For One Feature

**Red flag:** One small feature step introduces a cluster of thin coordinator, mapper, helper, processor, facade, and wrapper classes in the same boundary without a clear dependency or lifecycle reason.

**Why it happens:** The planner equates decomposition with quality and splits responsibilities before checking whether the pieces will really change independently.

**Fix:**

1. Prefer the smallest class set that preserves the architecture boundary and testability.
2. Split only when the new class isolates a dependency boundary, a distinct policy, or independent change pressure.
3. If a split is justified, say why in the step or a `DD-NNN` record instead of assuming it is obvious.

**Bad example:**

```md
## Step 2 - Order write path

Classes:
- `CreateOrderCoordinator`
- `CreateOrderWorkflow`
- `OrderPersistenceHelper`
- `OrderSaveFacade`
```

**Good example:**

```md
## Step 2 - Order application service and repository port

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `CreateOrderService` | Coordinate order creation and persistence | POL-002 |
| `OrderRepository` | Define the persistence contract for orders | None |
```

## Anti-Pattern 3: Naming Without Convention

**Red flag:** Planned class, package, or test names do not match the surrounding repo's naming patterns.

**Why it happens:** The planner invents names before studying nearby modules, tests, and architecture evidence.

**Fix:**

1. Read existing source and test names near the change before choosing new names.
2. Record naming evidence in the `Architecture and naming evidence` section of `plan.md`.
3. If you intentionally deviate from an established pattern, capture that as a `DD-NNN` with rationale.

**Bad example:**

```md
## Step 2 - Persistence

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `OrderStorageThing` | Save orders | None |
```

**Good example:**

```md
### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| Existing modules | `src/orders/` | Persisted collaborators use the `*Repository` suffix |
| Existing tests | `test/orders/` | Tests follow `className_condition_expectedBehavior` |
```

## Anti-Pattern 4: Vague Plan Steps

**Red flag:** Step titles say things like "Set up persistence", "Add business logic", or "Wire everything together".

**Why it happens:** The planner summarizes intent instead of planning executable work.

**Fix:**

1. Name the actual boundary, architectural unit, or class group being introduced or changed.
2. Fill the Classes, Invariants and policies, Unit test descriptions, and Definition of Done sections with concrete content.
3. Include explicit dependencies on earlier steps when they exist.

**Bad example:**

```md
## Step 3 - Add business logic

- [ ] Update services
- [ ] Add tests
```

**Good example:**

```md
## Step 3 - Order validation policy in application service

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `createOrderService_invalidQuantity_rejected` | `CreateOrderService` | Confirms invalid quantity requests fail before persistence |
```

## Anti-Pattern 5: Design Decisions Hidden In Plan Prose

**Red flag:** `plan.md` contains consequential choices about boundaries, persistence, async behavior, error handling, or policy placement, but `design-decisions.md` has no matching `DD-NNN`.

**Why it happens:** The decision felt too small to document or emerged while writing a step.

**Fix:**

1. Extract every material choice into `design-decisions.md`.
2. Give it a stable `DD-NNN`, evidence, alternatives, consequences, and affected steps.
3. Update the relevant plan step to cite or align with that decision.

**Bad example:**

```md
## Step 4 - Persistence strategy

Use asynchronous writes so the API stays responsive.
```

**Good example:**

```md
## DD-003 - Order persistence interaction style

- **Decision**: Use synchronous repository writes inside `CreateOrderService`
- **Alternatives considered**:
  - **Async queue handoff** - adds operational complexity that the requirements do not need
- **Affected plan steps**: Step 3, Step 4
```

## Anti-Pattern 6: Extra Output Files

**Red flag:** The planner creates `overview.md`, `summary.md`, `notes.md`, `scratch-plan.md`, or other convenience outputs.

**Why it happens:** The planner tries to separate summaries, notes, or evidence into new files instead of using the existing templates.

**Fix:**

1. Keep output limited to `integration-test-scenarios.md`, `plan.md`, `design-decisions.md`, `handoff.json`, and `solution-skeleton-spec.md`.
2. Write `design-decisions.md` and `solution-skeleton-spec.md` first. Write `plan.md` immediately after them on a brownfield plan that does not need skeleton review. When Gate 6C requires review, write `plan.md` only after explicit human approval.
3. Put summaries in the conversation, not in extra files.
4. Put structural evidence in the existing template sections, not in ad hoc artifacts.

**Bad example:**

```text
requirements/ECCS-123/plan/summary.md
requirements/ECCS-123/plan/notes.md
requirements/ECCS-123/plan/implementation-outline.md
```

**Good example:**

```text
requirements/ECCS-123/plan/integration-test-scenarios.md
requirements/ECCS-123/plan/plan.md
requirements/ECCS-123/plan/design-decisions.md
requirements/ECCS-123/plan/handoff.json
requirements/ECCS-123/plan/solution-skeleton-spec.md
```

## Anti-Pattern 7: Preview-First Delivery

**Red flag:** The planner finishes drafting, then waits for a save-confirmation checkpoint or pastes full artifact bodies into chat instead of writing `design-decisions.md` and `solution-skeleton-spec.md`.

**Why it happens:** The old preview-first contract lingers after the skill became Agent-only.

**Fix:**

1. Treat passing the readiness gates as authorization to write the review artifacts immediately.
2. Write `design-decisions.md`, then `solution-skeleton-spec.md`.
3. Use those two files plus a concise chat summary as the human review surface when Gate 6C requires review. Do not paste artifact bodies into chat.
4. When review is required, publish both review files to GitHub, paste separate blob URLs for `solution-skeleton-spec.md` and `design-decisions.md` in chat, and wait for explicit approval before writing `plan.md`. That wait is the review gate. On a brownfield plan without an explicit Marvin prompt, continue to the plan package in the same turn.

**Bad example:**

```text
Planner complete:
- here is the full `design-decisions.md` body
- here is the full `solution-skeleton-spec.md` body
- tell me if you want me to save them
```

**Good example:**

```text
Greenfield, or Marvin was explicitly prompted to review the skeleton:
- wrote `requirements/ECCS-123/plan/design-decisions.md`
- wrote `requirements/ECCS-123/plan/solution-skeleton-spec.md`
- pushed both review files and put separate GitHub blob URLs for each in chat
- asked for explicit approval before writing `plan.md`

Brownfield without that prompt:
- wrote the skeleton files and the plan package in the same turn
- did not ask for skeleton approval
```

## Anti-Pattern 8: Solution Skeleton Spec As A Second Source Of Truth

**Red flag:** `solution-skeleton-spec.md` introduces new decisions, risk rows, or coverage statements that are not present in `design-decisions.md` or the carried requirements risks.

**Why it happens:** The solution skeleton spec is treated like a brainstorming surface instead of a view of the written decisions.

**Fix:**

1. Write `design-decisions.md` first.
2. Generate `solution-skeleton-spec.md` from those decisions plus architecture discovery.
3. If the evidence file reveals a missing decision or risk, update `design-decisions.md` first, then regenerate `solution-skeleton-spec.md`.
4. Title it as `<ticket-id> <implemented service name or short change name>` and describe any intended `handoff.json.pauseReason` in human-facing evidence text as the acknowledgement reason.

**Bad example:**

```md
Solution-skeleton-spec title:
- `ECCS-123 — design evidence`

Solution-skeleton-spec risk section:
- "Pause reason: Human acknowledgement required"
- "DD-007: Migrate to event sourcing"
```

**Good example:**

```md
1. Add `DD-007` to `design-decisions.md`
2. Regenerate `solution-skeleton-spec.md` so it reflects the written decisions
3. Use the title `ECCS-123 Device trust signal ingestion`
4. Present the carried risk as `Acknowledgement reason: Confirm the downstream service contract before implementation`
5. Wait for human approval before writing `plan.md` only when Gate 6C requires skeleton review
```

## Anti-Pattern 9: Writing `plan.md` Before a Required Skeleton Review

**Red flag:** Gate 6C requires skeleton review (greenfield, or Marvin was explicitly prompted to review or approve the solution skeleton spec), and the same turn writes `plan.md`. The matching brownfield miss is the opposite: stopping to ask for skeleton approval when Marvin was not explicitly prompted.

**Why it happens:** The approval rule is applied to every plan, or dropped for every plan.

**Fix:**

1. Write `design-decisions.md` and `solution-skeleton-spec.md` first.
2. When Gate 6C requires review, publish both review files, paste separate GitHub blob URLs for each in chat, write `handoff.json` with `skeletonReviewRequired` true, `skeletonReviewApproved` false, and `nextAction` `await_skeleton_approval`, list implementation risks when acknowledgement is required, and stop before `plan.md`.
3. When the plan is brownfield and Marvin was not explicitly prompted, write the plan package in that same turn and do not ask for skeleton approval.
4. Keep `plan.md` aligned with the written decisions.

**Bad example:**

```text
Greenfield first turn:
- wrote `requirements/ECCS-123/plan/solution-skeleton-spec.md`
- wrote `requirements/ECCS-123/plan/plan.md`

Brownfield first turn, Marvin was not prompted to review the skeleton:
- asked the human to approve the skeleton before planning could continue
```

**Good example:**

```text
Greenfield, or Marvin was explicitly prompted:
- wrote `requirements/ECCS-123/plan/design-decisions.md`
- wrote `requirements/ECCS-123/plan/solution-skeleton-spec.md`
- wrote `requirements/ECCS-123/plan/handoff.json` with `skeletonReviewApproved` false and `nextAction` `await_skeleton_approval`
- chat includes separate GitHub blob URLs for `solution-skeleton-spec.md` and `design-decisions.md`
- asked for approval to write `plan.md`

Brownfield without that prompt:
- wrote the skeleton files, `integration-test-scenarios.md`, `plan.md`, and `handoff.json`
- did not ask for skeleton approval
```
