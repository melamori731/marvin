# Planning Rules

Normative policy for **Phase 4** drafting and **Phase 5** gate criteria. Execution order is in `references/workflow.md`.

## Requirement and test mapping

- Every `REQ-NNN` must map to at least one integration test scenario
- Every `QR-NNN` must map to an integration test scenario or explicit manual validation note with a path to automation
- `integration-test-scenarios.md` is the single source of truth for Step 0 scenario definitions and `REQ-NNN` / `QR-NNN` coverage; `plan.md` should reference it, not duplicate its scenario or coverage tables
- Step 0 integration tests are test-first acceptance checks: they must be specified, implemented, and runnable, but they are not expected to pass until the planned production behavior is implemented
- Every `INV-NNN` must be encapsulated in exactly one class and covered by unit tests on that class
- Every `POL-NNN` must be encapsulated in exactly one class and covered by unit tests on that class

## Architecture and design constraints

- For a brownfield plan, the architecture style already applied in the repo is the governing constraint. Do not ask the human to supply or select a different style. A user-named style that differs is a design risk, not a replacement. Docs that disagree with the applied code do not win; record that conflict as a design risk and keep the applied style.
- For a greenfield plan, treat the provided architecture style as the governing constraint for how responsibilities are grouped and how boundaries are drawn
- Do not assume Clean Architecture, layered architecture, or any other default style unless it is the style already applied in a brownfield repo, or it was explicitly provided or strongly supported for a greenfield plan
- If a greenfield architecture style is inferred, include the evidence and confidence in the plan; if that evidence conflicts, stop instead of guessing. A brownfield plan records the applied style and does not stop to choose among alternatives.
- Prefer the smallest set of cohesive design units that satisfies the requirements and the selected architecture style
- Avoid creating thin pass-through, wrapper, delegator, or single-method classes unless they isolate a real dependency boundary, reusable concept, policy boundary, or independently changing concern
- Do not split one feature flow into multiple classes unless the split clearly reduces coupling, improves cohesion, or is required by the selected architecture style
- Interpret SRP as "one coherent reason to change", not "one tiny operation per class"
- If several responsibilities always change together and belong to the same architectural boundary, keep them together

## Naming and brownfield preservation

- Preserve existing package, module, class, file, and test naming conventions unless the user explicitly asks for renaming or the plan identifies a concrete correctness/maintainability reason
- Prefer extending or modifying existing cohesive units over introducing new names or abstractions in brownfield plans
- New names must match the repo's observed naming style, language conventions, and test naming patterns
- Do not plan broad renames, package moves, or architecture reshaping as incidental work; call them out as separate optional follow-up work unless required

## Test naming and structural boundaries

- Test names use `subject_condition_expectedOutcome`
- Unit test names use `className_condition_expectedBehavior`
- Structural boundary tests should reflect the selected architecture style; use ArchUnit or an equivalent mechanism only for structural boundaries, not business invariants or policies
- Structural boundary test names should match the chosen architecture boundaries, for example `layer_mustNotDependOn_layer`, `module_mustNotDependOn_module`, or `slice_mustNotDependOn_slice`

## Design risks and scope preservation

- If an invariant or policy is spread across multiple classes, flag it as a design risk and propose consolidation
- If a requirement is untestable or under-specified, surface it explicitly as a risk
- Every `minimumAcceptedScope` ID must map to at least one plan step and its planned verification; do not silently omit, weaken, or replace it
- Every `critical` item from `topPriorityItems` must be mapped to a plan step and the Coverage sign-off; if it cannot be mapped, mark the plan `BLOCKED`
- Carry the analyst priority and minimum-scope anchors into the plan and implementation handoff so the coding agent can preserve them

## Design decisions (`DD-NNN`)

- Record every material design decision in `design-decisions.md` using stable `DD-NNN` IDs
- Include the selected option, status, rationale, evidence, alternatives considered, consequences, and affected plan steps
- Record unresolved material choices as `REQUIRES_ACK` or `BLOCKED`; do not hide them only in plan prose or `Design risks`
- `design-decisions.md` is the single source of truth for design decisions made or carried forward during planning; `plan.md` and `solution-skeleton-spec.md` reference it instead of maintaining independent decision records
- Assign each material decision a stable `DD-NNN` ID. Material decisions include architecture style, boundaries, dependency direction, integration contracts, persistence/data shape, cross-cutting policy placement, and consequential technology or implementation choices
- Do not create decision entries for trivial mechanics or restate requirements as decisions
- Every decision must cite concrete evidence from requirements, architecture records, user answers, or code discovery. Clearly distinguish evidence from planner rationale
- Use decision status `DECIDED`, `REQUIRES_ACK`, `BLOCKED`, or `SUPERSEDED`. A `REQUIRES_ACK` decision requires `READY_FOR_IMPLEMENTATION_WITH_ACK`; a `BLOCKED` decision requires a blocked handoff
- Link every active design decision to the plan step(s) it governs and record considered alternatives plus why they were not selected
- Write `design-decisions.md` with `solution-skeleton-spec.md` before `plan.md`. Do not write `plan.md` until the human explicitly approves those artifacts when Gate 6C requires skeleton review. On a brownfield plan without an explicit Marvin prompt to review the skeleton, write `plan.md` in the same turn.
- Update the decision record when planning changes a choice; preserve superseded entries and point to the replacing `DD-NNN` rather than silently rewriting history

## Implementation readiness and handoff

Choose intended status in Phase 6 before writing the skeleton artifacts. Write `handoff.json` with the plan package: after human approval when Gate 6C requires skeleton review, and in the same turn as the skeleton on a brownfield plan without that review. Also write it at the Step 15a stop when review is required, before `plan.md` exists. Align `requiresHumanAck`, `pauseReason`, and `designRisks` in `handoff.json` consistently; the coding agent treats any inconsistency between `status` and `requiresHumanAck` as a mandatory pause. In human-facing planner artifacts, present `pauseReason` as the acknowledgement reason instead of implying the planner run itself is paused. The coding agent surfaces those implementation risks in chat when acknowledgement is required. It requires skeleton approval only when this handoff says `skeletonReviewRequired` is true and `skeletonReviewApproved` is not true. It does not re-read the original Marvin prompt from chat.

- If implementation can proceed safely without human review, mark the final plan status `READY_FOR_IMPLEMENTATION` and set `requiresHumanAck: false` and `pauseReason: null` in `handoff.json`
- If planning reveals material delivery, architecture, or dependency risk that should be acknowledged, mark the final plan status `READY_FOR_IMPLEMENTATION_WITH_ACK` and set `requiresHumanAck: true` with a non-empty `pauseReason` and at least one entry in `designRisks` in `handoff.json`; never mark this status with `requiresHumanAck: false`
- If planning reveals contradictions or missing information that make implementation unsafe, mark the final plan status `BLOCKED`
- Leave the coding agent's execution-result fields (`humanAcknowledgement`, `implementationStatus`, `completionReportPath`) as `null` in `handoff.json`; the coding agent owns and populates them after implementation. When populated, `humanAcknowledgement.decision` is always exactly `proceed_as_is` or `risk_resolved` — no other value clears the coding agent's acknowledgement gate
- Persist the Gate 6C decision on that same handoff. `skeletonReviewRequired` is `true` when review is required and `false` when it is not. `skeletonReviewApproved` is `false` until an explicit approve, proceed, or write-the-plan instruction is recorded at Step 16, `true` after that instruction, and `null` only when review is not required. `solutionSkeletonSpecUrl` is the GitHub blob URL when review is required and `null` when it is not.
- When review is required and not yet approved, write those three fields at Step 15a after publication. Set `nextAction` to `await_skeleton_approval`. Do not write `plan.md` and do not set `nextAction` to `run_coding_agent`.
- When review is not required, Step 16 writes `skeletonReviewRequired` `false`, `skeletonReviewApproved` `null`, `solutionSkeletonSpecUrl` `null`, and `nextAction` `run_coding_agent` unless status is `BLOCKED`.
- A later session reads these fields. It must not turn a missing chat prompt into `skeletonReviewRequired: false`. An explicit prompt to review or approve the skeleton sets `skeletonReviewRequired` to `true` and `skeletonReviewApproved` to `false` before the coding agent runs, including when `plan.md` already exists.

## Design simplification

- Start with the smallest viable design for each planned step, then introduce additional classes only when justified by reuse, dependency boundaries, policy boundaries, or independent change pressure
- Prefer explicit methods inside one cohesive class before introducing more classes
- If more than 2-3 classes are proposed for one feature flow within the same architectural boundary, justify why each additional class is necessary

## Plan authoring completeness (Gate 5 criteria)

Verify for each plan step:

- The step scope is explicit and limited to that step's concern
- Responsibilities are assigned to concrete classes, tests, or validation activities
- Every in-scope `REQ-NNN`, `QR-NNN`, `INV-NNN`, and `POL-NNN` is mapped
- Every `minimumAcceptedScope` and `critical` priority item is mapped to a concrete plan step and verification
- Dependencies on earlier steps are explicit
- The generated content fully fills the template structure with concrete content
- The proposed class set is minimal for the planned behavior and selected architecture style
- No class exists only as an indirection layer without clear architectural value
- Each split is justified by reuse, dependency boundary, policy boundary, or independent change pressure
- Existing code names and architecture conventions are preserved or any deviation is explicitly justified
- New names are aligned with observed repo naming patterns
- Every material design decision is recorded in `design-decisions.md`, supported by evidence, and linked to the affected plan steps
- Decision statuses are consistent with implementation readiness and acknowledgement requirements
- Gaps or assumptions are surfaced in `Design risks` rather than omitted

If a step cannot be planned to this level of completeness, surface the missing detail as a risk or missing input — do not present the plan as ready.
