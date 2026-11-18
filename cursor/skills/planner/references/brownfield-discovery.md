# Brownfield Discovery

Read this reference when **Gate 2A** selects brownfield mode, before Step 6. Execution order is in `references/workflow.md`. The architecture style already applied in the repo is the style the plan uses.

For existing repos, perform a focused read-only study before planning:

- Identify the current architectural units and dependency direction from source layout, imports, package names, module manifests, tests, and docs
- Identify naming conventions for packages, modules, classes, functions, tests, fixtures, and configuration
- Identify local patterns for validation, error handling, dependency injection, persistence, external clients, and test setup when relevant to the requested change
- Prefer recent, nearby code over distant examples when conventions conflict
- Distinguish evidence from assumptions; carry uncertain findings into planning risks or the clarification list
- Keep discovery scoped to the requested change and its integration points

Discovery findings feed into:

- The architecture style the plan must use: the style already applied in the repo. This is not a candidate for the human to confirm or replace.
- Naming and extension decisions in the plan
- Evidence citations in `design-decisions.md`
- Brownfield-specific constraints in `references/planning-rules.md`
