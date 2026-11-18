# Assumptions

## Readiness

**Status**: [READY_FOR_PLANNING | READY_WITH_RISKS | BLOCKED]

**Work item ID**: [e.g. ECCS-123]

**Base path**: [e.g. requirements/ECCS-123/]

**Generated**: [Date and timestamp]

**Analysis scope**: [Brief description of source artifacts analyzed]

### Summary

[One concise paragraph: readiness, blocking issues if any, and tracked risks if READY_WITH_RISKS. Do not repeat detailed items below.]

### Blocking issues

[Issues that prevent planning - empty if READY_FOR_PLANNING]

### Tracked risks

[Risks to monitor during planning - empty if READY_FOR_PLANNING]

---

## Product and requirements assumptions

Classify each assumption: **safe**, **risky**, or **blocking**. Keep assumptions atomic and avoid restating requirements, constraints, policies, or open questions.

```markdown
### ASS-NNN
- **Statement**: [One clear assumption sentence]
- **Source**: [Source artifact and reference, or "inferred"]
- **Verification**: [How to verify]
- **Risk Level**: safe | risky | blocking
- **Mitigation**: [For risky/blocking only]
```

---

## Architecture assumptions

Foundational beliefs about system structure inferred from diagrams and design docs.
Keep architecture assumptions atomic and reference related item IDs instead of restating them.

```markdown
### ASS-ARCH-NNN
- **Statement**: [One sentence describing what is assumed about architecture]
- **Source**: [Diagram, design doc, or note]
- **Scope**: [Components or systems affected]
- **Risk Level**: safe | risky | blocking
- **Impact if false**: [What breaks if wrong]
```

---

## Open questions

Questions that need human answers before or during planning.

```markdown
### Q-NNN
- **Question**: [One specific question]
- **Why it matters**: [Concise context and impact]
- **Affected decisions**: [Related item IDs or areas impacted]
- **Source gap**: [What was missing or ambiguous in sources]
- **Suggested answerer**: [Role or team, if known]
```

### Critical (blocking planning)

### Important (should resolve early)

### Minor (can defer)

---

## Summary

| Category | Safe | Risky | Blocking | Total |
|----------|------|-------|----------|-------|
| Product assumptions | 0 | 0 | 0 | 0 |
| Architecture assumptions | 0 | 0 | 0 | 0 |
| Open questions | - | - | - | 0 |

---

## Top priorities

Highlight the small set of canonical items that most strongly constrain planning. Reference IDs and brief reasons only; do not restate full requirement text.

| ID | Priority | Why it matters |
|----|----------|----------------|
| REQ-001 | critical | [One sentence explaining why this item must not drift] |

---

## Autonomous handoff

- **Next stage**: planner | human
- **Proceed automatically**: yes | no
- **Planner input path**: [e.g. requirements/ECCS-123/]
- **Reason if paused**: [Blocking issue, critical question, or `None`]
