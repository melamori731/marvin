# Mode behavior

## Plan mode

- Resolve the work item and Gate 0B stage from artifacts
- Report which child skill would run next
- Name the next human gate from `human-gates.md` when one is already due
- Do not write requirements, review artifacts, `plan.md`, product code, tests, or either `handoff.json`
- Do not create or switch git branches. When the story title is already known, the report may name the branch Step 1b would check out
- Ask the user to switch to Agent mode to execute the next stage

## Agent mode

- Follow `workflow.md`
- Before the first write or commit of the turn, create the user-story branch when it does not exist and switch onto it in Step 1b. Requirement analysis, planning, and implementation in that turn stay on that branch. Do not switch back to the previous branch.
- Stay inside the active child skill until that skill stops for a human or finishes its stage
- On a human gate, put `templates/human-pause.md` in the final reply and stop the turn. Same rule in Slack, IDE, and CLI. Do not use AskQuestion. Do not self-answer skipped questions
- After an explicit solution-skeleton-spec approval, continue into planner Step 16 and then Phase 3 in the same turn when Gate 3A allows coding
- On a brownfield plan whose handoff records `skeletonReviewRequired` `false`, continue from the written plan package into Phase 3 when Gate 3A allows coding
- After steering at a required skeleton review, publish both review files again and stop
- After a valid acknowledgement decision, resume the coding agent and let that skill persist `humanAcknowledgement`
- An acknowledgement pause lists the implementation risks in the chat. A skeleton-review pause pastes separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md`
- After coding completion, open a PR for the story branch when none exists yet (Step 9). Skip only when a PR already exists for that branch

## Transitions

```text
Plan mode
  -> Agent mode only after the user asks to execute

Agent mode
  -> Human pause on analyst questions, blocked analyst handoff, any planner interactive stop,
     a required solution-skeleton-spec review or its steering, blocked plan, or missing acknowledgement
  -> Coding agent after plan.md when Gate 3A passes. Gate 3A reads skeletonReviewRequired and skeletonReviewApproved from the plan handoff
  -> After coding completion, create-pr when the story branch has no PR yet (Step 9)
  -> Done when completion artifacts exist and Step 9 has run (PR created or already present)

Human pause
  -> Same stage after the user answers (answers come from the human reply, not from AskQuestion or inventing skipped answers)
  -> Next stage only when the matching gate in workflow.md passes
```

The original pipeline request stays in effect as the goal. It never counts as a later gate's answer.
