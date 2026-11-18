# Coding-agent mode behavior

## Plan mode

- Resolve the candidate plan directory and list the required sibling artifacts
- Read `handoff.json` and report whether the package is `READY_FOR_IMPLEMENTATION`, `READY_FOR_IMPLEMENTATION_WITH_ACK`, or `BLOCKED`
- Summarize the numbered implementation steps and the acknowledgement state
- Do not edit product code, tests, `handoff.json`, or create `completion-report.md`
- End by asking the user to switch to Agent mode if they want the plan executed

## Agent mode

- Follow `references/workflow.md` exactly
- Edit product code and tests only after Gate 1A passes
- Run step-level verification and acceptance criteria as you finish each step, writing command output under `verification-logs/` (test logs need a runner stream; build/lint logs need tool-appropriate output; no quiet flags on test/build evidence)
- Apply Final acceptance, then run the requirement-test coverage gate, before writing completion artifacts
- After the coverage gate passes, write `completion-report.md` with relative links to those log files and update the coding-agent-owned fields in `handoff.json`

## Acknowledgement pause

Use this branch when `handoff.json.status` is `READY_FOR_IMPLEMENTATION_WITH_ACK` and `humanAcknowledgement` is still `null` or invalid.

- Do not edit product code before the user clears the risk
- Surface the implementation risks in the chat: the acknowledgement reason (`pauseReason`) and every `designRisks` entry. Do not leave the risks only in a file
- Ask for an explicit acknowledgement decision that the skill can persist as:
  - `proceed_as_is`
  - `risk_resolved`
- When the user gives one of those decisions, record it in `handoff.json.humanAcknowledgement` and resume from Gate 1A
- Do not require approval of `solution-skeleton-spec.md` in this pause

## Skeleton review pause

Use this branch only when `handoff.json.skeletonReviewRequired` is `true` and `handoff.json.skeletonReviewApproved` is not `true`.

- Do not edit product code
- Paste separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` in the chat. If `solutionSkeletonSpecUrl` is missing, publish both review files per planner `references/output-contract.md` "Skeleton review publication" and store the skeleton GitHub blob URL on the handoff
- When acknowledgement is also required, the same chat lists the implementation risks
- A direct "Build plan.md" request does not set `skeletonReviewApproved` and does not leave this pause

## Transition summary

```text
Plan mode
  -> Agent mode after user confirmation

Agent mode
  -> Acknowledgement pause when status is READY_FOR_IMPLEMENTATION_WITH_ACK
     The chat lists the implementation risks
  -> Skeleton review pause when skeletonReviewRequired is true and skeletonReviewApproved is not true
     The chat pastes separate GitHub blob links for solution-skeleton-spec.md and design-decisions.md
  -> Done after completion-report.md and handoff execution fields are written
```
