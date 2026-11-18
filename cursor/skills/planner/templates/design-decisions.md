# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

Record consequential choices here instead of hiding them only in `plan.md` prose. Keep trivial naming or formatting preferences out of this file.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | [e.g. ECCS-123] |
| **Requirements base path** | [e.g. requirements/ECCS-123/] |
| **Plan base path** | [e.g. requirements/ECCS-123/plan/] |
| **Plan** | [plan.md](./plan.md) (written after human approval) |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION \| READY_FOR_IMPLEMENTATION_WITH_ACK \| BLOCKED |

## Status definitions

- `DECIDED`: selected for implementation and supported by sufficient evidence.
- `REQUIRES_ACK`: selected provisionally, but material risk requires human acknowledgement before implementation.
- `BLOCKED`: unresolved choice prevents safe implementation.
- `SUPERSEDED`: replaced by another decision; preserve the entry and link its replacement.

---

## Decision index

| ID | Decision | Status | Affected plan step(s) |
|----|----------|--------|-----------------------|
| DD-001 | [Concise statement of the selected option] | DECIDED | Step N |

---

## DD-001 — [Decision title]

- **Status**: DECIDED | REQUIRES_ACK | BLOCKED | SUPERSEDED
- **Decision**: [State the selected option or unresolved choice precisely.]
- **Scope**: [Boundary, component, contract, data, technology, or implementation concern governed by this decision.]
- **Rationale**: [Why this option best satisfies the requirements and architecture constraints.]
- **Evidence**:
  - [Requirement IDs, architecture record, user answer, or code path]
- **Alternatives considered**:
  - **[Alternative]** — [Why it was not selected]
- **Consequences**:
  - [Trade-off, constraint, migration effect, operational impact, or follow-up]
- **Affected plan steps**: [Step N, Step M]
- **Supersedes**: [DD-NNN or None]
- **Superseded by**: [DD-NNN or None]

---

## Decision completeness

- [ ] Every material architecture, boundary, dependency, contract, persistence, policy-placement, and consequential technology choice has a `DD-NNN` entry
- [ ] Every active decision cites concrete evidence
- [ ] Every active decision records alternatives and consequences
- [ ] Every active decision maps to the plan step(s) it governs
- [ ] Every `REQUIRES_ACK` decision is reflected in a `READY_FOR_IMPLEMENTATION_WITH_ACK` handoff
- [ ] Every `BLOCKED` decision is reflected in a blocked handoff
- [ ] Superseded decisions are preserved and linked to their replacements
