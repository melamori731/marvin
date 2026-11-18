# Marvin paused

Put this block in the final reply for every human gate. It is the pause surface for Slack, IDE, and CLI. Do not use AskQuestion. Do not self-answer and continue.

- **Work item:** `requirements/<ticket-id>/`
- **Stage:** requirement-analyst | planner | coding-agent
- **Gate:** <gate id and one-line reason>
- **Artifacts:** <written paths, or "none yet">
- **Links:** <when skeleton review is required: separate GitHub blob URLs for `solution-skeleton-spec.md` and `design-decisions.md`; otherwise omit>
- **Need from you:** <the analyst/planner questions, the approval-or-steering choice, or the acknowledgement decision — verbatim, unanswered>
- **Not done yet:** <the next artifact or stage that will not start until you answer>

Approval of the solution skeleton spec, when that review is required, means an explicit approve, proceed, or write-the-plan reply. The planner records that reply as `skeletonReviewApproved: true`. The chat pastes separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` (not only the skeleton; `solutionSkeletonSpecUrl` is the skeleton link). A change request is steering: the review artifacts will be updated, both files will be published again, and this pause will repeat. This pause is required when plan `handoff.json` has `skeletonReviewRequired` `true` and `skeletonReviewApproved` is not `true`, including a later session whose chat no longer contains the original prompt. Brownfield does not use this pause when that handoff says `skeletonReviewRequired` is `false`.

Acknowledgement, when the plan asks for it, is exactly `proceed_as_is` or `risk_resolved`. The pause lists the implementation risks in the chat.
