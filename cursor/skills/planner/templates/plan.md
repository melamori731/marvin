# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | [e.g. ECCS-123] |
| **Requirements base path** | [e.g. requirements/ECCS-123/] |
| **Plan base path** | [e.g. requirements/ECCS-123/plan/] |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | New repo / Existing repo |
| **Architecture style** | [e.g. Clean Architecture: domain / application / adapter / infrastructure, or inferred existing repo style] |
| **Architecture source** | User-provided / Context bank / Architecture docs / Repo rules / Inferred from code |
| **Architecture confidence** | High / Medium / Low; low confidence must be carried as a design risk or blocker |
| **Input readiness** | READY_FOR_PLANNING \| READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION \| READY_FOR_IMPLEMENTATION_WITH_ACK \| BLOCKED |
| **Human acknowledgement required** | yes \| no |
| **Risks carried forward** | [From assumptions.md in discovered requirements path, or None] |

### Analyst planning anchors

These fields come from `requirements/<ticket-id>/handoff.json`. The plan must preserve every minimum-scope item and map every critical item to a step and verification.

| ID | Priority | Minimum accepted scope | Why it matters | Plan step(s) | Verification |
|----|----------|------------------------|----------------|--------------|--------------|
| REQ-NNN | critical | yes | [Analyst-provided reason] | Step N | [Test or validation] |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | [path or not found] | [Relevant architecture, naming, or boundary rule] |
| Existing modules | [path or not applicable] | [Module/package/class naming and responsibility pattern to preserve] |
| Existing tests | [path or not applicable] | [Test naming, fixture, and coverage pattern to preserve] |
| Contracts / schemas | [path or not provided] | [API/event/data shape constraint] |

---

## Step 0 — Integration tests

- [Integration test scenarios](./integration-test-scenarios.md)
- `integration-test-scenarios.md` is the single source of truth for Step 0 scenarios and `REQ-NNN` / `QR-NNN` coverage.

### Definition of Done

- [ ] Integration test scenarios covering every `REQ-NNN` are specified and corresponding test code is implemented
- [ ] Every `QR-NNN` has a specified integration test or manual validation with a path to automation
- [ ] Step 0 tests are runnable and may fail only because the planned production behavior is not implemented yet
- [ ] Acceptance coverage matrix in `integration-test-scenarios.md` shows zero uncovered items and matches the planned verification

---

## Step 1 — Architectural structure and boundaries

### Structure map

| Architectural unit | Responsibility | Allowed dependencies |
|--------------------|----------------|----------------------|
| [layer / module / slice / component] | [Single-sentence purpose] | [Allowed dependencies for the selected architecture style] |
| [layer / module / slice / component] | [Single-sentence purpose] | [Allowed dependencies for the selected architecture style] |
| [layer / module / slice / component] | [Single-sentence purpose] | [Allowed dependencies for the selected architecture style] |

### Structural boundary test descriptions

Use ArchUnit or an equivalent mechanism for the implementation language and architecture style. Structural boundary tests are only for architectural boundaries, not business invariants or policies.

| Test name | Rule |
|-----------|------|
| `[boundary]_mustNotDependOn_[boundary]` | [Boundary A must not depend on boundary B according to the selected architecture style] |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — [Architectural unit name]

Use a concrete step name that matches the repo's architecture and naming evidence. Do not leave this as a vague feature summary such as "Add business logic" or "Set up persistence".

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `[ClassName]` | [Single reason to change] | INV-NNN, POL-NNN (if any) |

### Invariants and policies

Each invariant and policy must be fully encapsulated in exactly one class.

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-NNN | `[ClassName]` | [How the class enforces it] |
| POL-NNN | `[ClassName]` | [How the class enforces it] |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `[className_condition_expectedBehavior]` | `[ClassName]` | [What the test verifies] |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step N — [Next architectural unit name]

[Repeat Step 2 structure for each remaining architectural unit]

---

## Final acceptance

Overall acceptance criteria for the planned code changes. All items must pass before the implementation is considered complete.

### Build and static analysis

- [ ] Project compiles without errors
- [ ] No linter or static analysis errors introduced

### Test suite

- [ ] All structural boundary tests pass
- [ ] All unit tests pass (including invariant and policy encapsulation tests)
- [ ] All integration tests pass (all scenarios in `integration-test-scenarios.md`)

### Traceability

- [ ] All items in the Coverage sign-off below are green
- [ ] Every active `DD-NNN` in `design-decisions.md` is reflected in the affected implementation steps

---

## Coverage sign-off

Final traceability check before implementation.

| ID type | ID | Verification |
|---------|-----|--------------|
| Functional | REQ-NNN | Integration: `[testName]` |
| Quality | QR-NNN | Integration: `[testName]` or Manual: [approach] |
| Invariant | INV-NNN | Unit: `[className_condition_expectedBehavior]` on `[ClassName]` |
| Policy | POL-NNN | Unit: `[className_condition_expectedBehavior]` on `[ClassName]` |

### Sign-off checklist

- [ ] Every `REQ-NNN` → integration test(s)
- [ ] Every `INV-NNN` → unit test(s) on encapsulating class
- [ ] Every `POL-NNN` → unit test(s) on encapsulating class
- [ ] Every `QR-NNN` → integration test(s) or manual validation note
- [ ] No invariant or policy split across multiple classes
- [ ] Every `minimumAcceptedScope` ID is mapped to a plan step and verification
- [ ] Every `critical` priority item is mapped to a plan step and verification
- [ ] All mapped verifications are implemented and passing

---

## Coding agent handoff

- **Automatic start**: yes | no
- **Acknowledgement reason**: [Design risk, dependency risk, human acknowledgement required, or `None`]
- **Handoff artifact**: `requirements/<ticket-id>/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/<ticket-id>/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/<ticket-id>/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

[SRP violations, split encapsulation, untestable requirements, or architectural concerns surfaced during planning]
