# Policies

Software architecture policies: business or operational rules expressed in terms of what the system chooses to do. A policy captures system decision logic, not external process metadata.

Keep each policy atomic: one condition and one resulting system behavior. If a policy overlaps a requirement, constraint, or invariant, keep the strongest canonical item and reference its ID instead of restating it.

```markdown
### POL-NNN
- **Statement**: [Single policy rule: condition and resulting system behavior]
- **Source**: [Source artifact and reference]
- **Verification**: [One way to verify the system applies this rule]
- **Related requirements**: [Related item IDs only, or None]
```

---

## Business decision policies

## Operational decision policies

## Routing and classification policies

## Data handling policies

## Security behavior policies

## Fallback and exception policies

## User experience policies

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Business decision        | 0     |
| Operational decision     | 0     |
| Routing / classification | 0     |
| Data handling            | 0     |
| Security behavior        | 0     |
| Fallback / exception     | 0     |
| User experience          | 0     |
| **Total**                | **0** |

## Notes

[Omit this section unless it adds non-duplicative policy context. Put conflict and ambiguity details in `conflicts-and-ambiguities.md`; do not duplicate them here.]