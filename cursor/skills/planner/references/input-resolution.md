# Input Resolution

Supporting detail for **Phase 1** and **Phase 2** of `references/workflow.md`. Do not use this file as the execution path — follow the workflow gates.

## Locate requirements base path

Try in order:

1. User-provided or attached `requirements/<ticket-id>/`
2. Work item path from Requirement Analyst `handoff.json`
3. Legacy `docs/requirements/` or `requirements/` only when migrating older work
4. Any user-attached `@` paths

Used by: **Gate 1A**

## Required files

- `assumptions.md`
- `functional.md`
- `invariants.md`
- `policies.md`
- `quality.md`
- `conflicts-and-ambiguities.md`
- `handoff.json`

Optional: `constraints.md`

Used by: **Gate 1B**

## Discover repo context

Try in order:

1. AI context bank or equivalent: `ai-context-bank/`, `context-bank/`, `docs/ai-context-bank/`, `docs/context-bank/`, `.ai/`, `.cursor/rules/`
2. Repository guidance: `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `docs/architecture/`, `docs/design/`, `docs/adr/`, `adr/`
3. User-attached `@` paths for contracts, schemas, modules, packages, or services
4. Nearby source and test modules relevant to the requested change

Used by: **Step 4** (Phase 2)

## Planning mode criteria

| Mode | Condition |
|------|-----------|
| Greenfield | No existing implementation is relevant, or the user explicitly asks to plan from scratch |
| Brownfield | The request modifies, extends, or integrates with existing code |

Used by: **Gate 2A**

## Architecture style sources

Brownfield precedence:

1. The architecture style already applied in the repo, read from package/module boundaries, dependency direction, test organization, and naming
2. Trusted repo context only when it describes that same applied style

A user-named style does not replace the applied brownfield style. Record a mismatch as a design risk.

Greenfield precedence:

1. User-provided architecture style
2. Trusted repo context: AI context bank, architecture docs, ADRs, or repo rules
3. Evidence inferred from package/module boundaries, dependency direction, test organization, and naming conventions

Classification guidance for **Gate 2B**:
- **Brownfield applied**: the style already in the code. Do not stop to ask the human to choose. Stop only when no applied style can be identified.
- **Greenfield clear**: user-provided or unambiguous trusted repo context
- **Greenfield inferred**: code evidence only; record evidence and confidence
- **Greenfield ambiguous**: conflicting sources or low confidence. Stop and ask.
- **Greenfield missing**: no source found. Stop and ask.

## Input inventory template

Fill at **Step 3** (Phase 1) before continuing to Phase 2:

```md
## Input inventory

### Requirements discovery
- **Located**: yes | no
- **Work item ID**: [e.g. ECCS-123] | not found
- **Base path**: [e.g. requirements/ECCS-123/] | not found
- **Search paths checked**: requirements/<ticket-id>/, legacy docs/requirements/, legacy requirements/, [@ attachments]

| File | Status | Path |
|------|--------|------|
| assumptions.md | found | missing | [path or —] |
| functional.md | found | missing | [path or —] |
| invariants.md | found | missing | [path or —] |
| policies.md | found | missing | [path or —] |
| quality.md | found | missing | [path or —] |
| constraints.md | found | missing | [path or —] |
| conflicts-and-ambiguities.md | found | missing | [path or —] |
| handoff.json | found | missing | [path or —] |

### Other inputs
| Input | Status |
|-------|--------|
| Top priority items | [IDs from handoff.json, or None] |
| Minimum accepted scope | [IDs from handoff.json, or None] |
| Planning mode | new repo / existing repo / unclear |
| Architecture style | applied (brownfield) | provided | discovered | inferred | ambiguous | missing |
| Architecture evidence | [user message, context bank/docs/rules, source evidence, or not found] |
| AI context bank / repo guidance | [list paths found or not found] |
| Contracts / schemas | [list attached paths or not provided] |
| Existing modules | [list discovered or attached paths, or not applicable for greenfield] |
```

## Cannot proceed template

Output when any Phase 1–3 gate fails:

```md
## Cannot proceed

Provide the following before planning can start:

1. [specific missing item]
2. [specific missing item]
```

## Readiness validation detail

Used by **Phase 3** (Steps 7–9, Gate 3A):

- Read `assumptions.md` → `READY_FOR_PLANNING`, `READY_WITH_RISKS`, or `BLOCKED`
- Read `handoff.json` → preserve work item ID, requirements path, planner next-action intent, `topPriorityItems`, `minimumAcceptedScope`
- Read `conflicts-and-ambiguities.md` → carry open `CA-NNN` rows into planning risks or blockers
- Validate every `topPriorityItems[].id` and `minimumAcceptedScope` ID exists in requirement outputs
