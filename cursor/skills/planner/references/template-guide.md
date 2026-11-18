# Template Authoring Guide

Read this guide before drafting the first planner artifact. `references/output-contract.md` is the single source of truth for when artifacts exist, when Gate 6C requires skeleton review before `plan.md`, and the required authoring order. This guide focuses on what strong artifact content looks like once drafting begins.

## Output boundaries

- Do not create extra files such as `overview.md`, `summary.md`, `notes.md`, or `scratch-plan.md`.
- Use the template headings and section order exactly.
- Keep traceability in the canonical artifacts instead of duplicating it across ad hoc outputs.
- If a later artifact changes readiness, scope, or decisions, update earlier artifacts before delivery so the set stays consistent.

## Placeholder discipline

- Replace every bracketed placeholder with concrete content or remove the row/line if it does not apply.
- Keep placeholder shapes aligned with the existing template conventions, such as `REQ-NNN`, `QR-NNN`, `DD-NNN`, `INV-NNN`, `POL-NNN`, and `<ticket-id>`.
- Do not leave example values like `ECCS-123`, `Step N`, or `[ClassName]` in completed outputs.
- If a section would stay empty, explain the absence concretely or omit the optional subsection instead of leaving placeholder-only content behind.

## What "good" looks like

Good planner output is concrete, traceable, and scoped to a single artifact's job.

### `integration-test-scenarios.md`

- Every scenario maps to at least one `REQ-NNN` or `QR-NNN`.
- The acceptance coverage matrix has no silent gaps.
- Manual validation is used only when automation is not yet possible and the path to automation is stated.

### `plan.md`

- Step titles name a real architectural unit, boundary, class group, or implementation milestone.
- Each step states responsibilities, mapped invariants/policies, tests, and dependencies.
- The Definition of Done is specific enough that a coding agent can tell whether the step is complete.

### `design-decisions.md`

- Record only material decisions with trade-offs.
- Each active `DD-NNN` has evidence, alternatives, consequences, and affected steps.
- Do not hide consequential decisions only inside `plan.md`.

### `handoff.json`

- `status`, `requiresHumanAck`, `pauseReason`, and `designRisks` must agree.
- `skeletonReviewRequired`, `skeletonReviewApproved`, and `solutionSkeletonSpecUrl` must agree with Gate 6C. Required and not approved uses `nextAction` `await_skeleton_approval` and a GitHub blob URL. Not required uses `false`, `null`, and `null`.
- Preserve `minimumAcceptedScope`, `topPriorityItems`, and `nextAction`.
- Leave coding-agent execution fields as `null`.
- Keep the JSON field name `pauseReason` for contract compatibility, but describe it in human-facing plan and solution-skeleton-spec text as the acknowledgement reason.

### `solution-skeleton-spec.md`

- Reflect the written `design-decisions.md` and the architecture style. Brownfield uses the style already applied in the repo. Do not wait for `plan.md` before writing this file.
- Show only unlabeled runtime-flow arrows in the architecture diagram. Do not add compile-time dependency arrows or arrow labels.
- Do not invent new `DD-NNN`, risk items, or coverage rows that are not in `design-decisions.md` or the carried requirements risks.
- Title the file as `<ticket-id> <implemented service name or short change name>` and keep any "solution skeleton spec" wording in supporting text only.

## Example: strong vs weak plan step

### Good

```md
## Step 2 — Order application service and repository port

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `CreateOrderService` | Coordinate order creation workflow and persist the aggregate through a port | POL-002 |
| `OrderRepository` | Define the persistence contract for storing and loading orders | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| POL-002 | `CreateOrderService` | Reject duplicate create requests before calling the repository |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `createOrderService_duplicateRequest_rejected` | `CreateOrderService` | Confirms duplicate create requests fail before persistence |

### Definition of Done

- [ ] `CreateOrderService` and `OrderRepository` are implemented in the planned boundary
- [ ] `POL-002` is enforced only by `CreateOrderService`
- [ ] Unit tests for the step are implemented and passing
- [ ] Dependencies stay within the allowed architectural boundaries
```

### Weak

```md
## Step 2 — Add order logic

Create the order classes and make sure they are wired up correctly.

- [ ] Add repository
- [ ] Add service
- [ ] Test it
```

The strong version names the concrete units, maps policy coverage, gives a real test name, and defines completion criteria the coding agent can execute against.
