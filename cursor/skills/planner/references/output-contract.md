# Output Contract

Read this reference at **Phase 6** (write the solution skeleton spec, then the plan package). Execution order is in `references/workflow.md`. Gate 6C decides whether the plan package waits for skeleton approval.

## Template source of truth

Use these files as the single source of truth for structure:

- `.cursor/skills/planner/templates/integration-test-scenarios.md`
- `.cursor/skills/planner/templates/plan.md`
- `.cursor/skills/planner/templates/design-decisions.md`
- `.cursor/skills/planner/templates/handoff.json`
- `.cursor/skills/planner/templates/solution-skeleton-spec.md`

Follow their headings, section order, and checklist structure exactly. Do not invent a different structure.

Before drafting the first artifact, read `references/template-guide.md` for concrete examples, placeholder usage, and content-quality expectations.

If output starts to drift, read `references/anti-patterns.md` and correct the draft before presenting or writing anything.

Read the relevant template file before authoring each artifact.

## Artifact timeline

Draft content during Phases 4-5. Write `design-decisions.md` and `solution-skeleton-spec.md` as soon as the gates pass. Write the plan package in the same turn on a brownfield plan when Marvin was not explicitly prompted to review the skeleton. Otherwise write the plan package only after explicit human approval.

| Artifact | When it is written | Delivery expectation |
|----------|--------------------|----------------------|
| `design-decisions.md` | Phase 6 Step 14 after intended readiness is consistent | Write to `requirements/<ticket-id>/plan/design-decisions.md` |
| `solution-skeleton-spec.md` | Phase 6 Step 14 immediately after `design-decisions.md` | Write to `requirements/<ticket-id>/plan/solution-skeleton-spec.md` |
| `integration-test-scenarios.md` | Phase 6 Step 16 | Write to `requirements/<ticket-id>/plan/integration-test-scenarios.md` |
| `plan.md` | Phase 6 Step 16 | Write to `requirements/<ticket-id>/plan/plan.md` |
| `handoff.json` | Phase 6 Step 15a when review is required, then Step 16 with the plan package | Write to `requirements/<ticket-id>/plan/handoff.json` |

Do not create extra summary, overview, canvas, or scratch output files. The planner's outputs are limited to the template artifacts above. A chat summary or CreatePlan card is not delivery.

## Artifact authoring order

Author outputs in this order:

1. `design-decisions.md`
2. `solution-skeleton-spec.md`
3. Gate 6C: stop for skeleton review, or continue
4. On the review stop, `handoff.json` with `skeletonReviewRequired` `true`, `skeletonReviewApproved` `false`, `solutionSkeletonSpecUrl` set, and `nextAction` `await_skeleton_approval`
5. `integration-test-scenarios.md`
6. `plan.md`
7. `handoff.json` with `skeletonReviewApproved` `true` when review was required, or `skeletonReviewRequired` `false` when it was not, and `nextAction` `run_coding_agent` unless status is `BLOCKED`
8. Refresh `solution-skeleton-spec.md` only to name the written plan path

Each later artifact must agree with the earlier ones. If writing `plan.md` would change scope or a material decision, update `design-decisions.md` and `solution-skeleton-spec.md` first. Stop again only when Gate 6C required review.

## Mandatory solution-skeleton-spec markdown

For every completed review pass:

1. Use `templates/solution-skeleton-spec.md` as a scaffold, not as evidence. Replace every `__PLACEHOLDER__`, adapt the diagram to the discovered architecture, and omit sections without real data.
2. Write the generated file to `requirements/<ticket-id>/plan/solution-skeleton-spec.md` together with `design-decisions.md`. On a review-required path this is before `plan.md` exists. On a brownfield skip path, Step 16 may follow in the same turn.
3. Title it as `<ticket-id> <implemented service name or short change name>`. Keep "Solution skeleton spec" as supporting text, not in the main title.
4. Show only unlabeled runtime-flow arrows in the mermaid diagram. Do not add compile-time dependency arrows or arrow labels.
5. Keep building-block descriptions concise and state each block's scope, boundary, and allowed dependencies.
6. Include every `DD-NNN` entry from `requirements/<ticket-id>/plan/design-decisions.md`, including superseded decisions, while preserving its ID, decision, status, rationale, evidence, alternatives, consequences, and affected plan steps. Do not create evidence-only decisions or IDs. Affected plan steps may be proposed step IDs before `plan.md` is written.
7. Carry all `CA-*` rows, design risks, intended readiness status, acknowledgement requirement, and the intended `handoff.json.pauseReason` into the risk section, but present that field to humans as the acknowledgement reason rather than as a planner pause state.
8. Keep requirement/test traceability in the canonical `integration-test-scenarios.md` once that file is written; do not duplicate coverage tables in `solution-skeleton-spec.md`.

### Evidence write fallback

If writing `solution-skeleton-spec.md` fails:

1. Report the exact error and which write step failed.
2. Treat the written `design-decisions.md` as the source of truth for decisions. Do not write `plan.md`, `integration-test-scenarios.md`, or `handoff.json`.
3. Do not invent an extra overview, summary, canvas, or substitute artifact file.
4. Retry `solution-skeleton-spec.md` only after the user confirms they want another write attempt.

## Skeleton review gate

`solution-skeleton-spec.md` plus `design-decisions.md` are the human review surface when Gate 6C requires review.

Gate 6C requires review for greenfield, and for brownfield only when the user explicitly prompted Marvin to review or approve the solution skeleton spec. A brownfield `/planner` run, a bare `/marvin`, and "carry this through implementation" do not require review. Record the decision in `handoff.json` (`skeletonReviewRequired`, `skeletonReviewApproved`, `solutionSkeletonSpecUrl`) in that same turn. The coding agent does not add its own skeleton-approval requirement and does not infer one from chat.

When review is required:

- Publish both review files per Skeleton review publication (separate GitHub blob links), then **STOP** and ask the human to approve writing `plan.md`.
- Write `plan.md` only after an explicit approve / proceed / write-the-plan instruction, and set `skeletonReviewApproved` to `true` on the plan handoff in that same write.
- If the human requests changes, update `design-decisions.md` and `solution-skeleton-spec.md`, publish both again with separate GitHub blob links, then **STOP**.
- If intended status is `BLOCKED`, do not write `plan.md` until blockers are resolved and the review artifacts are updated.
- A `/planner` or `/marvin` rerun, intended `READY_FOR_IMPLEMENTATION`, or a chat summary that mentions the future `plan.md` path is not approval.

When review is not required, write the plan package in the same turn. Do not ask for skeleton approval.

## Skeleton review publication

Use this when a human must review the solution skeleton spec (planner Step 15a, Marvin's skeleton-review stop, or the coding agent's stop when plan `handoff.json` has `skeletonReviewRequired` `true` and `skeletonReviewApproved` is not `true`). Store the skeleton blob URL in `solutionSkeletonSpecUrl`. The chat always pastes **separate** GitHub blob links for both `solution-skeleton-spec.md` and `design-decisions.md` (not only the skeleton).

1. If both `requirements/<ticket-id>/plan/solution-skeleton-spec.md` and `requirements/<ticket-id>/plan/design-decisions.md` are already on the GitHub remote at the current branch tip and the working tree copies match them, reuse those blob URLs.
2. Otherwise commit those two review files on the current branch (only those files). Do not commit unrelated files. Do not force-push. Do not change git config.
3. Push that commit to the branch's GitHub upstream. If the branch has no upstream, push to `origin` and set the upstream to the current branch name.
4. Put both GitHub blob URLs in the chat as separate links:
   - `https://github.com/<owner>/<repo>/blob/<branch>/requirements/<ticket-id>/plan/solution-skeleton-spec.md`
   - `https://github.com/<owner>/<repo>/blob/<branch>/requirements/<ticket-id>/plan/design-decisions.md`
   A local path does not replace either link.
5. If the remote is not GitHub or the push fails, **STOP** and report the exact error. Do not invent a URL. Do not write `plan.md` or edit product code in that turn.
6. When the human also needs to acknowledge implementation risk (`READY_FOR_IMPLEMENTATION_WITH_ACK`, a non-empty acknowledgement reason, or any `designRisks` entry), list the acknowledgement reason and each implementation risk in that same chat.

## Mode behavior

### Agent mode only

On a review-required path, before approval, write only:

- `requirements/<ticket-id>/plan/design-decisions.md`
- `requirements/<ticket-id>/plan/solution-skeleton-spec.md`
- `requirements/<ticket-id>/plan/handoff.json` with `skeletonReviewRequired` `true`, `skeletonReviewApproved` `false`, `solutionSkeletonSpecUrl` set to the published blob URL, and `nextAction` `await_skeleton_approval`

Then publish both review files per Skeleton review publication (separate GitHub blob links for each) and stop. That handoff must not tell the coding agent it can start.

On a brownfield path that skips review, write those two files and then, in the same turn:

- `requirements/<ticket-id>/plan/integration-test-scenarios.md`
- `requirements/<ticket-id>/plan/plan.md`
- `requirements/<ticket-id>/plan/handoff.json`

Before writing the skeleton artifacts, make one consistency pass:

- Every material choice in the drafted plan has a `DD-NNN` entry in `design-decisions.md`
- Intended handoff readiness fields match the design-risk state
- `solution-skeleton-spec.md` reflects the written design decisions and the applied or selected architecture and does not introduce decisions or requirements that exist only in the skeleton spec
- Brownfield architecture style is the style already applied in the repo

Before writing the plan package, make one additional consistency pass:

- Step 0 coverage in `integration-test-scenarios.md` matches `plan.md`
- `plan.md` follows the written `DD-NNN` records
- `handoff.json` readiness fields match those records

After a skeleton-review stop:

- Return a concise summary instead of pasting full artifact bodies into chat
- Paste separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` (a local path does not replace either link)
- State the intended readiness status
- List implementation risks in the chat when acknowledgement is required
- Ask for explicit approval to write `plan.md`

After writing the plan package:

- Name every written artifact path
- State the final readiness status and whether the downstream `coding-agent` can start from `handoff.json`
- On the brownfield skip path, do not ask for skeleton approval
