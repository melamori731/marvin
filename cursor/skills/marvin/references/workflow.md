# Marvin workflow

Run the three child skills in order. Follow each child skill's own workflow while its phase is active. This file only decides which child runs, when the pipeline may advance, and when it must return to the human.

Do not write `plan.md` from this skill. Do not edit product code from this skill. Do not invent answers, approvals, or acknowledgements. The git writes this skill performs itself are Step 1b (create the story branch when it is missing, then switch onto it) and Step 9 (commit/push as needed and open a PR for that branch when coding is complete and no PR exists yet). Marvin does not leave the previous branch checked out. Child skills still follow their own git rules while that story branch is current.

---

## Phase 0 — Resolve the run

### Step 0: Confirm Agent mode when the next stage must write files

**Gate 0A — Can this turn write the next stage's artifacts?**

| Result | Action |
|--------|--------|
| Agent mode, or Plan mode and the only honest action is a report | → Step 1 |
| The next stage must write files and this context cannot write them | **STOP** — tell the user to rerun `/marvin` in Agent mode |

### Step 1: Resolve the work item and stage

Require one ticket ID. If none is present and no `requirements/<ticket-id>/handoff.json` is in scope, ask for the ID and **STOP**.

Read the artifacts that exist:

1. `requirements/<ticket-id>/handoff.json`
2. `requirements/<ticket-id>/plan/design-decisions.md`
3. `requirements/<ticket-id>/plan/solution-skeleton-spec.md`
4. `requirements/<ticket-id>/plan/plan.md`
5. `requirements/<ticket-id>/plan/handoff.json`
6. `requirements/<ticket-id>/plan/completion-report.md`

**Gate 0B — Which stage is active?**

Match `status`, `requiresHumanInput`, `blockingIssues`, and `nextAction` only on the file the row names. The Phase 1 stop row reads `requirements/<ticket-id>/handoff.json` and does not read `requirements/<ticket-id>/plan/handoff.json`. A plan `nextAction` of `run_coding_agent`, and a plan `status` of `BLOCKED`, are Phase 3 facts (Step 7), not this stop. If `requirements/<ticket-id>/handoff.json` is absent, skip the Phase 1 stop row.

| Artifact state | Action |
|----------------|--------|
| `requirements/<ticket-id>/handoff.json` is missing and `plan.md` is not present, or that requirements handoff still has unanswered analyst questions | → Phase 1 |
| On `requirements/<ticket-id>/handoff.json` only: `status` is `BLOCKED`, `requiresHumanInput` is true, `blockingIssues` is non-empty, or `nextAction` is not `run_planner` | **STOP** — Phase 1 human gate. `plan.md` will not be written |
| Requirements handoff may advance, and either review artifact is missing | → Phase 2. Brownfield without an explicit skeleton-review prompt runs the planner through Step 16. Otherwise stop at planner Step 15a |
| Both review artifacts exist, `plan.md` is missing, and plan `handoff.json` has `skeletonReviewRequired` true with `skeletonReviewApproved` not true | → Phase 2 Step 5 |
| Both review artifacts exist, `plan.md` is missing, and plan `handoff.json` has `skeletonReviewRequired` false | → Phase 2 planner Step 16, then Phase 3 when the plan handoff can advance |
| Both review artifacts exist, `plan.md` is missing, and plan `handoff.json` does not record `skeletonReviewRequired` | **STOP** — do not infer the review decision from this conversation and do not write `plan.md` |
| `plan.md` and plan `handoff.json` exist, coding handoff is not clear to implement | → Phase 3 Step 7 |
| Coding handoff is clear to implement and completion artifacts are absent | → Phase 3 Step 8 |
| `completion-report.md` exists and plan `handoff.json.implementationStatus` records completion | → Step 9 (create-pr if the story branch has no PR yet), then **STOP** — pipeline complete |

A later `/marvin` with no new human decision does not change this gate.

### Step 1b: Create the user-story branch, switch onto it, and stay there

Run this step only in Agent mode, and only when this turn will write or commit repository files. A Gate 0B **STOP** that does not write skips it. Entering Phase 1, Phase 2, or Phase 3 Step 8 in order to write or commit runs it first. A later turn that writes runs it again before that write.

The branch name is the ticket key plus a slug of the user story, as in `ECCS-4521-implement-this-or-that` when the ticket is `ECCS-4521` and the story title is "Implement this or that". `ECCS-XXXX-emplement-tis-or-that` is a picture of that pattern, not a literal branch. Do not create that name unless those exact strings are the real ticket key and the real story slug.

**Gate 0C — Story branch is current before this turn writes, and it stays current?**

1. Resolve one user-story title. Use a one-line title the user supplied for this work item. If they did not, use the Jira issue summary for the ticket id, retrieved the same way the requirement analyst retrieves Jira. Do not slug a requirement sentence, a plan step, a skeleton heading, or a placeholder.
2. If no title is available, **STOP** and ask for the one-line user story title. Do not invent a title. Do not create a branch yet.
3. Print the branch name with `python3 .cursor/skills/marvin/scripts/story-branch.py --ticket <ticket-id> --title "<title>"`. The script prints `<ticket-id>-<slug>` and exits non-zero when the ticket key or the slug is unusable. The slug is the title in lowercase kebab-case, ASCII letters and digits, at most 48 characters, cut on a hyphen. A title that repeats the ticket key keeps the key only once.
4. Read the previous branch with `git branch --show-current`. If that output is already `<name>`, Marvin is on the story branch. Do not create a second branch. Continue at step 8.
5. If `refs/heads/<name>` exists, `git switch <name>`. When the switch would overwrite or drop local changes, **STOP** and report the git error. Do not stash, reset, clean, or discard uncommitted work. Do not write on the previous branch.
6. Otherwise create the branch and switch onto it in the same command: `git switch -c <name>` from the current HEAD, including a detached HEAD. Do not use `git branch <name>` by itself. That creates the ref and leaves Marvin on the previous branch. Uncommitted files stay in the working tree. Do not commit, push, force-push, or change git config in this step.
7. `git branch --show-current` must print `<name>`. If it still prints the previous branch, **STOP**. Do not write or commit on the previous branch.
8. The rest of this turn runs on `<name>`. Requirement analysis, planning, and implementation all happen on that branch. Do not switch back to the previous branch. Child skills commit and push only while this branch is current.

The branch is git state. Do not store it in either `handoff.json`.

---

## Phase 1 — Requirement analyst

### Step 2: Run the analyst

Read and follow `.cursor/skills/requirement-analyst/SKILL.md` for this work item. Analyst writes in this turn happen on the Step 1b branch. Do not switch back to the previous branch.

When that skill must ask the human (missing sources, missing work item ID, or a blocking / high-impact ambiguity round), put those questions in the final reply using `templates/human-pause.md` and **STOP** until the human answers. This applies in Slack, IDE, and CLI alike. Do not use IDE-only AskQuestion. Do not self-answer skipped or unanswered questions and continue. Do not write a final readiness claim in that turn. Do not start the planner.

### Step 3: Decide whether planning may start

Read `requirements/<ticket-id>/handoff.json` and `references/human-gates.md`.

**Gate 1A — Analyst handoff may advance?**

- [ ] `status` is `READY_FOR_PLANNING` or `READY_WITH_RISKS`
- [ ] `requiresHumanInput` is `false`
- [ ] `blockingIssues` is empty
- [ ] `nextAction` is `run_planner`
- [ ] No critical ambiguity is still waiting on the human

| Result | Action |
|--------|--------|
| All pass | → Phase 2 in this same turn |
| `BLOCKED`, `requiresHumanInput: true`, or unresolved critical questions | **STOP** — surface the blocking issues / questions with `templates/human-pause.md` in the final reply and wait for human resolution. Do not self-answer |
| Any other shape | **STOP** — report the mismatch with `templates/human-pause.md`; do not start the planner |

---

## Phase 2 — Planner

### Step 4: Run the planner until its interactive stop

Read and follow `.cursor/skills/planner/SKILL.md` and `references/workflow.md`. Planner writes and the skeleton publish in this turn happen on the Step 1b branch. Do not switch back to the previous branch.

The planner stays interactive at every stop that skill already uses. For brownfield, using the architecture style already applied in the repo is required and is not one of those stops. Greenfield still stops on architecture conflict, low confidence, or a missing style. Both modes stop for unclear greenfield vs brownfield, blocked or malformed requirements, quality-gate stops, and a failed skeleton write. Skeleton review stops only when the planner's Gate 6C requires it. See `references/human-gates.md`.

**Gate 2A — Planner is waiting on the human?**

| Result | Action |
|--------|--------|
| Planner workflow says **STOP** and the human has not answered yet | **STOP** — return the planner's question unchanged |
| Human answered an interactive planner question | Resume the planner with that answer. Re-check this gate |
| Gate 6C requires skeleton review and approval has not been given | → Step 5 |
| Gate 6C does not require review and the planner wrote the plan package | → Phase 3 |
| `plan.md` already written | → Phase 3 |

Do not pick greenfield vs brownfield, a greenfield architecture, or a design alternative on the user's behalf. On brownfield, do use the architecture style already applied in the repo.

### Step 5: Solution skeleton spec review and steering

Run this step when Gate 6C requires review: the plan is greenfield, the user explicitly prompted Marvin to review or approve the solution skeleton spec, or plan `handoff.json` already has `skeletonReviewRequired` `true` and `skeletonReviewApproved` is not `true`.

Explicit prompts include "review the skeleton", "review the solution skeleton spec", "approve the skeleton before the plan", and "ask me to approve the skeleton". These are not that prompt: a bare `/marvin`, "carry this through implementation", "finish the pipeline", and "implement it". An explicit approve / proceed / write-the-plan reply is the approval, not the prompt that creates the gate. The planner records that approval as `skeletonReviewApproved: true`.

Skip this step on brownfield only when the plan handoff does not already say review is required and Marvin was not explicitly prompted. The planner then writes `skeletonReviewRequired: false`. Do not skip it because this message omitted the original prompt.

When this step runs, the gate is mandatory. The message that started the pipeline is not approval. Silence, `/marvin`, `/planner`, and an intended status of `READY_FOR_IMPLEMENTATION` are not approval.

Treat as approval only an explicit instruction to approve, proceed, or write the plan, and only when both review files already exist.

Treat a requested change to scope, design, or the skeleton as steering.

**Gate 2B — What did the human do at the solution skeleton spec?**

| Human input | Action |
|-------------|--------|
| Explicit approve / proceed / write the plan | Resume planner Step 16. Write `integration-test-scenarios.md`, `plan.md`, and plan `handoff.json` only through the planner skill. Then → Phase 3 if Gate 2C passes |
| Steering (requested changes) | Update `design-decisions.md` and `solution-skeleton-spec.md` through the planner skill, publish both again with separate GitHub blob links for each, then **STOP**. Do not write `plan.md` in that turn |
| Intended readiness is `BLOCKED` | **STOP** — do not offer to write `plan.md` until the human resolves the blockers and the review artifacts are updated |
| Anything else, including the original pipeline request | **STOP** — publish per the planner's skeleton review publication. The planner writes or refreshes plan `handoff.json` with `skeletonReviewRequired` `true`, `skeletonReviewApproved` `false`, `solutionSkeletonSpecUrl` set to the skeleton GitHub blob URL, and `nextAction` `await_skeleton_approval`. The chat pastes separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` (not only the skeleton), states the intended readiness, and asks for approval or steering. When acknowledgement is required, the same chat lists the implementation risks. `plan.md` stays unwritten |

If writing `plan.md` would change a material decision, return to the steering row instead of writing the plan.

**Gate 2C — Plan package is ready for the coding agent?**

- [ ] `plan.md`, `integration-test-scenarios.md`, and plan `handoff.json` exist
- [ ] When skeleton review was required, `plan.md` was written only after Gate 2B approval and `skeletonReviewApproved` is `true`
- [ ] When the brownfield skip applied, `skeletonReviewRequired` is `false` and `skeletonReviewApproved` is `null`
- [ ] `nextAction` is `run_coding_agent`
- [ ] Readiness fields match `references/handoff-contract.md`

| Result | Action |
|--------|--------|
| All pass | → Phase 3 in this same turn |
| Any fail | **STOP** — stay in the planner skill and report the gap |

---

## Phase 3 — Coding agent

### Step 6: Read the plan handoff

Read `requirements/<ticket-id>/plan/handoff.json`. Do not rewrite planner-owned readiness fields.

### Step 7: Human acknowledgement or resolution

**Gate 3A — May coding start?**

| Plan handoff | Action |
|---------------|--------|
| `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true` | **STOP** — skeleton review before coding. Paste separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` in the chat (not only the skeleton). If `solutionSkeletonSpecUrl` is missing, publish both review files per the planner output contract and store the skeleton blob URL on the handoff. List the acknowledgement reason and each implementation risk in that chat when acknowledgement is required. Do not edit product code. Do not treat this conversation as the approval record |
| `READY_FOR_IMPLEMENTATION`, `requiresHumanAck` false, fields consistent, `nextAction` `run_coding_agent` | → Step 8 |
| `READY_FOR_IMPLEMENTATION_WITH_ACK` and `humanAcknowledgement.decision` is `proceed_as_is` or `risk_resolved` | → Step 8 |
| `READY_FOR_IMPLEMENTATION_WITH_ACK` without that decision, and skeleton review is not pending | **STOP** — surface the implementation risks in the chat: the acknowledgement reason and every `designRisks` entry. Accepted decisions are only `proceed_as_is` and `risk_resolved`. Do not edit product code. Do not require skeleton approval when `skeletonReviewRequired` is `false` or `skeletonReviewApproved` is `true` |
| `BLOCKED` | **STOP** — report the acknowledgement reason and design risks in the chat. Do not implement |
| Inconsistent readiness fields, or any other status | **STOP** — ask the human to resolve or repair the handoff |

The pipeline does not write `humanAcknowledgement`. After the human chooses one of the two decisions, resume `.cursor/skills/coding-agent/SKILL.md` so that skill records it, then re-check Gate 3A.

### Step 8: Run the coding agent

If Step 1b has not run this turn, run it before any coding write. The story branch is the current branch before this step edits the tree. Do not switch back to the previous branch. Follow `.cursor/skills/coding-agent/SKILL.md` until it completes or until its workflow says **STOP**.

**Gate 3B — Coding agent finished or needs a human?**

| Result | Action |
|--------|--------|
| Completion artifacts written and Gate 4A of the coding-agent workflow passes | → Step 9 |
| Coding-agent workflow **STOP** for acknowledgement, a blocked decision, a contradiction, a missing artifact, or a coverage-gate failure it cannot fix inside its own retry | **STOP** — involve the human with that blocker via `templates/human-pause.md`. Do not declare the pipeline complete |
| Coding-agent workflow allows a local fix and retry | Stay inside the coding-agent skill. Do not skip its gates |

### Step 9: Open a PR for the story branch when missing

Run this only after Gate 3B says coding completed. Stay on the Step 1b story branch.

**Gate 3C — Does the story branch already have a PR?**

1. Check with `gh pr view --json url,title,state` on the current branch (or the equivalent create-pr preflight). If an open PR already exists for this branch, skip creation, report that PR URL with the completion report path, and **STOP** — pipeline complete.
2. Otherwise follow the create-pr skill (`.cursor/skills/create-pr/SKILL.md` when present, else skill-home `create-pr`). Commit and push story-branch work as needed so create-pr can open the PR. The PR title must start with the Jira user story id (`<ticket-id>`), then a short description, for example `ECCS-13592 Deploy muse permission rule`. Do not force-push. Do not change git config. Do not open a second PR when one already exists.
3. Report the new PR URL with the completion report path, then **STOP** — pipeline complete.

---

## Do not continue when

- A child skill is waiting on the human and the pipeline is tempted to answer for them, use AskQuestion instead of the final-reply pause, or self-answer skipped questions
- Skeleton review is required by plan `handoff.json` (`skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true`). A brownfield handoff with `skeletonReviewRequired` `false` is not this case. Do not replace a missing handoff field with a guess from chat
- Steering was just applied at a required skeleton review and `plan.md` is about to be written in the same turn
- `READY_FOR_IMPLEMENTATION_WITH_ACK` has no valid acknowledgement
- Any handoff in the active stage is `BLOCKED`
- This turn will write or commit and the current branch is not the Step 1b story branch
- Step 1b created or switched to the story branch, and a later step would switch back to the previous branch or keep writing there
