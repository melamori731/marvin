# Coding-agent evals

Behavioral fixtures for the coding-agent workflow.

Minimum coverage:

1. Happy path: ready plan package executes step by step, passes final acceptance, passes the requirement-test coverage gate, writes `verification-logs/` with `command:` / `cwd:` / `exit_code:` headers and relative report links, and writes completion artifacts that link to those files (stack-agnostic; do not require Maven `Tests run:` / `BUILD SUCCESS`)
2. Acknowledgement gate: `READY_FOR_IMPLEMENTATION_WITH_ACK` stops until the user explicitly clears the risk, and the chat lists the implementation risks. Skeleton approval is not required unless `skeletonReviewRequired` is true and `skeletonReviewApproved` is not true
3. Blocked or invalid handoff: coding does not start when required artifacts or readiness fields are not usable
4. Coverage gate: an uncovered input requirement blocks `completion-report.md`
5. Contract tests: a provided contract without contract tests wired to `REQ-NNN` blocks completion
6. Quiet-flag test logs: a captured test command whose `command:` line used `-q` / `--quiet` / `--silent`, or whose body has no runner stream, is not valid completion evidence. Do not assert this by banning teaching substrings such as `mvn -q` from the whole happy-path transcript.
