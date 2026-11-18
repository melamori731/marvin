# Anti-patterns

## 1. Treating the pipeline request as skeleton approval

**Red flag:** Skeleton review is required, and `plan.md` appears in the same turn as the first write of `solution-skeleton-spec.md`. The matching brownfield miss is stopping for skeleton approval when the user did not explicitly prompt Marvin to review the skeleton.

**Why it happens:** "Run the pipeline" is misread as "approve every gate in advance," or the greenfield approval gate is applied to every brownfield plan.

**Fix:** When review is required, stop at planner Step 15a, publish both review files, paste separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` in chat, and wait for an explicit approve, proceed, or write-the-plan message. When the plan is brownfield and Marvin was not explicitly prompted, write the plan package in the same turn.

**Example (bad):** User says `/marvin` on a greenfield ticket and the agent writes `plan.md` immediately after the skeleton. Or the user says `/marvin` on a brownfield repo and the agent waits for skeleton approval. Or the pause links only the skeleton and omits `design-decisions.md`.

**Example (good):** On greenfield, the agent pastes separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md`, states the intended readiness, and asks for approval or steering. On brownfield without that prompt, it does not ask for skeleton approval.

## 2. Answering planner questions

**Red flag:** The pipeline picks greenfield vs brownfield, or a greenfield architecture alternative, without a user reply. On brownfield, inventing a style instead of using the one already applied is the same mistake.

**Why it happens:** The sequencer treats planner stops as inconveniences, or treats "use the applied style" as a license to guess.

**Fix:** Return the planner's question unchanged and stop. When the repo already applies a style, use that style and do not ask the human to choose a different one.

**Example (bad):** "No architecture style was found, so I used layered modules."

**Example (good):** "Gate 2A stopped. I did not pick greenfield vs brownfield or an architecture style."

## 3. Folding steering into plan write

**Red flag:** Skeleton review is required, the user asks to change a design decision, and the same turn writes `plan.md`.

**Why it happens:** Steering is treated as a comment on an already approved plan.

**Fix:** Update `design-decisions.md` and `solution-skeleton-spec.md`, publish both again, paste separate GitHub blob links for each, then stop.

**Example (bad):** "I applied your note and wrote `plan.md`."

**Example (good):** "I updated the two review files and put separate GitHub blob links for each in chat. `plan.md` is not written. Approve again, or send another change."

## 4. Starting coding on an unacknowledged or blocked plan

**Red flag:** Product edits begin while `status` is `READY_FOR_IMPLEMENTATION_WITH_ACK` and `humanAcknowledgement` is null, or while `status` is `BLOCKED`.

**Why it happens:** The pipeline's job is confused with "always reach code."

**Fix:** Stop for `proceed_as_is` or `risk_resolved`, or for resolution of the block. List the acknowledgement reason and each implementation risk in the chat. Do not invent the acknowledgement JSON. Do not add a skeleton-approval stop unless plan `handoff.json` has `skeletonReviewRequired` `true` and `skeletonReviewApproved` is not `true`.

**Example (bad):** "The risks look acceptable, so I set `proceed_as_is` and started coding."

**Example (good):** "Status is `READY_FOR_IMPLEMENTATION_WITH_ACK`. The chat lists the implementation risks. Choose `proceed_as_is` or `risk_resolved`. No code has been edited."

## 5. Skipping analyst resolution

**Red flag:** Planner starts while `requiresHumanInput` is true, `blockingIssues` is non-empty, or critical questions are unanswered. Or the agent uses IDE-only AskQuestion, or invents answers for skipped questions and continues.

**Why it happens:** The pipeline wants sequential progress more than a planner-safe requirement set, or assumes AskQuestion works outside the IDE.

**Fix:** Put the analyst's questions in the final reply with `templates/human-pause.md` and **STOP** in Slack, IDE, and CLI. Do not use AskQuestion. Do not self-answer. Finalize readiness only after the human answers or explicitly accepts a non-material risk the analyst skill allows.

**Example (bad):** "One ownership question is open; I marked the handoff `READY_FOR_PLANNING`." Or: "AskQuestion was skipped, so I assumed the refund owner is Billing."

**Example (good):** "Ownership of the refund record is unresolved. The final reply has the human-pause questions. I did not start the planner."

## 5b. Declaring coding done without a story-branch PR

**Red flag:** Coding-agent completion artifacts exist, the story branch has no open PR, and Marvin stops without running create-pr.

**Why it happens:** Pipeline "done" is treated as completion-report only.

**Fix:** After Gate 3B completion, run Step 9. Create the PR (commit/push as needed per create-pr). The title must start with the Jira user story id. Skip only when a PR already exists for that branch.

**Example (bad):** "Implementation complete. See `completion-report.md`." (no PR check)

**Example (good):** "Implementation complete. No PR existed for the story branch, so create-pr opened `<url>` with title `ECCS-13592 Deploy muse permission rule`."

## 6. Reimplementing a child skill

**Red flag:** The pipeline writes plan steps or product code without following the child `SKILL.md`.

**Why it happens:** The orchestrator copies a short summary and drops the child gates.

**Fix:** Read and follow the child skill for the active phase. This skill only sequences and enforces human stops.

**Example (bad):** A homemade `plan.md` is written from the requirements summary.

**Example (good):** Phase 2 follows `.cursor/skills/planner/SKILL.md` until its approval stop.

## 7. Creating the placeholder branch, or leaving Marvin on the previous branch

**Red flag:** The pipeline creates `ECCS-XXXX-emplement-tis-or-that`, writes files while the current branch is still the branch Marvin started on, creates the story branch with `git branch <name>` and does not switch, or switches back to the previous branch before the analyst, planner, or coding agent finishes.

**Why it happens:** The pattern example is copied as a literal name, or branch setup is treated as optional git hygiene. `git branch <name>` creates a ref and leaves the previous branch checked out.

**Fix:** Resolve the real ticket key and the real user-story title, print the name with `scripts/story-branch.py`, then create the missing branch and switch onto it with `git switch -c <name>`. The example `ECCS-4521-implement-this-or-that` is what ticket `ECCS-4521` and title "Implement this or that" produce. The rest of the turn runs on that current branch. Do not switch back to the previous branch. Do not invent a title. Do not discard uncommitted work to switch branches.

**Example (bad):** "I created `ECCS-XXXX-emplement-tis-or-that` and started the analyst there." Or: "I ran `git branch ECCS-4521-implement-this-or-that`, stayed on `main`, and wrote the requirements there."

**Example (good):** "Ticket `ECCS-4521` and story title Implement this or that. `git switch -c` left the current branch as `ECCS-4521-implement-this-or-that`. The analyst ran there. Uncommitted files stayed in the working tree. I did not switch back."
