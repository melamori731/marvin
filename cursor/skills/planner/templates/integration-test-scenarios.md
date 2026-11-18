# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

Keep Step 0 coverage in this file. Do not create separate coverage, summary, or overview markdown files for the same requirement mappings.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `[subject_condition_expectedOutcome]` | REQ-NNN, QR-NNN | [Concise outcome description] |

---

## Scenarios (Given-When-Then)

### `[subject_condition_expectedOutcome]`

- **Requirements**: REQ-NNN[, QR-NNN]
- **Given**: [Initial system state, fixtures, and preconditions]
- **When**: [Action or trigger]
- **Then**: [Expected observable outcome]
- **Notes**: [Optional: data setup, mocks, edge cases]

---

## Acceptance coverage matrix

Confirm every functional and quality requirement is covered by at least one scenario or explicit manual validation.

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `[testName]` | |
| QR-001 | `[testName]` or Manual: [validation approach] | |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 0 | 0 | 0 | 0 |
| QR | 0 | 0 | 0 | 0 |

## Risks and gaps

[Untestable requirements, missing contracts, or scenarios that need follow-up before implementation]
