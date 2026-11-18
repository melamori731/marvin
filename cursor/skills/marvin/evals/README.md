# Marvin evals

Behavioral fixtures. A scenario passes when the pipeline follows the expected stage, stops at the expected human gate, and does not produce the artifacts that gate forbids.

## Minimum coverage

1. Greenfield happy path reaches the solution skeleton spec, pastes separate GitHub links for the skeleton and design-decisions, and stops for approval without writing `plan.md`
2. Steering at a required skeleton review updates the review artifacts and stops again
3. Analyst block or open critical question does not start the planner; questions use the human-pause final reply (not AskQuestion, not self-answered)
4. `READY_FOR_IMPLEMENTATION_WITH_ACK` does not start coding, and the pause lists the implementation risks in chat
5. Explicit approval of a required skeleton review is what allows `plan.md`, and a clear `READY_FOR_IMPLEMENTATION` handoff is what allows coding. A brownfield pipeline start does not itself require skeleton approval
6. Before writing, the pipeline creates `<ticket-id>-<user-story-slug>` when it does not exist, switches onto it, and does the rest of the work on that branch. It does not stay on the previous branch and does not create the placeholder branch `ECCS-XXXX-emplement-tis-or-that`
7. After coding completion, create-pr runs unless a PR already exists for the story branch
