# Invariants

Stable truths the system must never violate. Requirements and designs must not contradict these.

Keep each invariant atomic. If an invariant overlaps a requirement, policy, or constraint, keep the strongest canonical item and reference its ID instead of restating it.

```markdown
### INV-NNN
- **Statement**: [One sentence describing what must always remain true]
- **Source**: [Source artifact and reference]
- **Verification**: [One way to verify this remains true]
- **If violated**: [Concrete failure or impact]
```

---

## Data invariants

## Integrity invariants

## Business logic invariants

## Security invariants

## Consistency invariants

---

## Summary

- **Total invariants**: [N]

## Notes

[Omit this section unless it adds non-duplicative invariant context. Put conflict and ambiguity details in `conflicts-and-ambiguities.md` and reference `CA-NNN` IDs here only when useful.]
