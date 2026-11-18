# Coding-agent workflow

Canonical phase-and-gate tree for implementing from a saved plan.

Read `references/handoff-contract.md` before writing any `handoff.json` execution fields.

---

## Phase 0 - Resolve inputs

**Step 0.1 - Locate the plan set**

Accept one of these entry points:

1. An explicit `.../plan.md` path from the user message
2. A plan directory that contains `plan.md`
3. A sibling `handoff.json` path whose `planPath` points to `plan.md`

Resolve the final artifact set to one plan directory containing:

- `plan.md`
- `handoff.json`
- `design-decisions.md`
- `integration-test-scenarios.md` when referenced by Step 0

**Gate 0A - Required artifacts present?**

- [ ] `handoff.json` exists in the plan directory
- [ ] `design-decisions.md` exists in the same plan directory
- [ ] `plan.md` exists, unless `handoff.json` has `skeletonReviewRequired` `true` and `skeletonReviewApproved` is not `true`
- [ ] The repo working tree is available for edits and tests


| Result   | Action                                                       |
| -------- | ------------------------------------------------------------ |
| All pass | -> Phase 1                                                   |
| Any fail | **STOP** - report an input inventory and the missing path(s) |


---



## Phase 1 - Readiness and acknowledgement

**Step 1.1 - Validate the planner handoff**

Read `handoff.json` and verify:

- `skeletonReviewRequired`, `skeletonReviewApproved`, and `solutionSkeletonSpecUrl` agree with `references/handoff-contract.md`
- `status`, `requiresHumanAck`, `pauseReason`, and `designRisks` agree
- `humanAcknowledgement`, `implementationStatus`, and `completionReportPath` are either `null` or already follow `references/handoff-contract.md`
- `nextAction` is `run_coding_agent` when implementation may start. When `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true`, Gate 1A's review stop still applies if `nextAction` is `run_coding_agent`; that mismatch is not permission to start

The coding agent does not require approval of `solution-skeleton-spec.md` unless `handoff.json.skeletonReviewRequired` is `true` and `handoff.json.skeletonReviewApproved` is not `true`. It does not infer that gate from this conversation. A build request, a bare `/marvin`, and "carry this through implementation" do not approve a required review and do not clear `skeletonReviewApproved`.

**Gate 1A - May implementation start?**


| Handoff state                                                                         | Action                                                                        |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true` | **STOP** - skeleton review is still required by the plan handoff. Paste separate GitHub blob links for `solution-skeleton-spec.md` and `design-decisions.md` in the chat (not only the skeleton). If `solutionSkeletonSpecUrl` is missing, publish both review files using planner `references/output-contract.md` section "Skeleton review publication", store the skeleton blob URL on the handoff, and still stop. When the human also needs to acknowledge implementation risk, list the acknowledgement reason and every `designRisks` entry in that same chat. Do not edit product code. Do not set `skeletonReviewApproved` |
| `READY_FOR_IMPLEMENTATION`, `skeletonReviewRequired` is `false` or `skeletonReviewApproved` is `true`, and fields are consistent | -> Step 1.2                                                                   |
| `READY_FOR_IMPLEMENTATION_WITH_ACK` and a valid `humanAcknowledgement` already exists, and skeleton review is not pending | -> Step 1.2                                                                   |
| `READY_FOR_IMPLEMENTATION_WITH_ACK` and no valid acknowledgement exists yet, and skeleton review is not pending | **STOP** - surface the implementation risks in the chat before any code edits. Name the acknowledgement reason and every `designRisks` entry in the chat itself. Ask for `proceed_as_is` or `risk_resolved`. Do not require skeleton approval when `skeletonReviewRequired` is `false` or `skeletonReviewApproved` is `true` |
| `BLOCKED`                                                                             | **STOP** - do not implement a blocked plan                                    |
| Any inconsistency between readiness fields, including a missing skeleton-review field | **STOP** - report the mismatch and ask for a repaired handoff                 |


**Step 1.2 - Load execution constraints**

Read:

1. `plan.md`
2. `design-decisions.md`
3. `integration-test-scenarios.md` when Step 0 or Coverage sign-off references it
4. `references/rules.md`

Resolve the active decisions:

- `DECIDED` always apply
- `REQUIRES_ACK` apply only after a valid acknowledgement exists
- `BLOCKED` stops execution
- `SUPERSEDED` do not implement directly

**Gate 1B - Execution contract complete?**

- [ ] Each plan step has scope plus verification or acceptance criteria
- [ ] Every active `DD-NNN` maps to one or more plan steps
- [ ] No `BLOCKED` decision is still active
- [ ] Final acceptance and Coverage sign-off sections are present


| Result   | Action                                                 |
| -------- | ------------------------------------------------------ |
| All pass | -> Phase 2                                             |
| Any fail | **STOP** - report the specific gap in the plan package |


---



## Phase 2 - Implement the plan in order

**Step 2.1 - Execute Step 0 first**

Use Step 0 as the source of truth for integration-test coverage:

1. Create or align the Step 0 integration-test scaffolding first
2. Keep `integration-test-scenarios.md` as the canonical coverage map
3. Allow Step 0 tests to fail only because later production behavior is not implemented yet

**Gate 2A - Step 0 complete enough to continue?**

- [ ] Scenario coverage for every planned `REQ-NNN` and `QR-NNN` exists
- [ ] Step 0 tests or validation hooks are runnable
- [ ] Failures, if any, are only missing planned behavior rather than broken test setup


| Result   | Action                                                               |
| -------- | -------------------------------------------------------------------- |
| All pass | -> Step 2.2                                                          |
| Any fail | Fix the Step 0 setup once, then re-check; if still failing, **STOP** |


**Step 2.2 - Execute Steps 1..N sequentially**

For each numbered implementation step in `plan.md`, in order:

1. Restate the step scope and the active `DD-NNN` decisions it must preserve
2. Edit only the files needed for that step
3. Run the planned verification for that step and save the command output under `verification-logs/` in the plan directory (see Verification log files)
4. Check that step's acceptance criteria or Definition of Done before moving on

Do not merge unrelated steps just because the touched files overlap.

**Gate 2B - Current step done?**

- [ ] The step's planned code changes are implemented
- [ ] The step's planned verification ran
- [ ] Each command that ran has a `verification-logs/` output file with a tool-appropriate body (see Verification log files)
- [ ] The step's acceptance criteria or Definition of Done passes
- [ ] No new dependency violates the Step 1 boundary rules
- [ ] No active `DD-NNN` was silently contradicted


| Result                                                   | Action                                                                     |
| -------------------------------------------------------- | -------------------------------------------------------------------------- |
| All pass                                                 | Repeat Step 2.2 for the next plan step, or -> Phase 3 after the final step |
| Any fail that is local and fixable                       | Fix locally and re-run the gate once                                       |
| Any fail caused by a plan/codebase/runtime contradiction | **STOP** - surface the blocker instead of guessing                         |


---



## Phase 3 - Apply final acceptance

**Step 3.1 - Run the final acceptance section**

Execute the broadest required verification needed by `plan.md`, which may include:

- build or compile commands
- linters or static analysis
- structural boundary tests
- unit tests
- integration tests
- planned manual validation for `QR-NNN` items that still lack automation

Save each command's output under `verification-logs/` using the names in Verification log files. Do not rely on chat transcript as the record.

**Step 3.2 - Run the Coverage sign-off**

Verify that every mapped item in the Coverage sign-off is green and that active decisions are still reflected in the implementation.

**Gate 3A - Implementation complete before the coverage gate?**

- [ ] Build and static analysis pass or the plan explicitly recorded a manual exception
- [ ] All required structural boundary tests pass
- [ ] All required unit tests pass
- [ ] All required integration tests pass
- [ ] Each command that ran has a `verification-logs/` output file with a tool-appropriate body (see Verification log files)
- [ ] Every `REQ-NNN`, `QR-NNN`, `INV-NNN`, and `POL-NNN` mapping has matching verification
- [ ] No active `DD-NNN` was left unimplemented


| Result                                         | Action                                                              |
| ---------------------------------------------- | ------------------------------------------------------------------- |
| All pass                                       | -> Step 3.3                                                         |
| Any fail that is straightforward to fix        | Fix locally, then re-run Phase 3 once                               |
| Any fail with unresolved risk or contradiction | **STOP** - report the blocker and do not write completion artifacts |


**Step 3.3 - Evaluate requirement-test coverage**

Before writing a completion report, run the deterministic coverage gate against the input requirements and the working tree:

```bash
python3 .cursor/skills/coding-agent/scripts/requirement-test-coverage-gate.py <repo-root> <plan-dir>
```

Use the JSON output as the gate. Do not replace it with a narrative claim that tests exist.

The script must show:

- every input `REQ-NNN`, `INV-NNN`, and `POL-NNN` covered by a respective test
- every input `QR-NNN` covered by a test, or by an explicit `Manual:` mapping in the plan package
- if a contract or schema was provided, contract tests exist, each contract is referenced by those tests, and every input `REQ-NNN` is cited in a contract test

Write the JSON to `requirement-test-coverage.json` in the plan directory on every run, including failures. Do not write `completion-report.md` yet.

**Gate 3B - Requirement-test coverage passed?**

- [ ] The script exited 0 and `"passed": true`
- [ ] `uncovered` is empty
- [ ] `contractFailures` is empty


| Result                                                                                       | Action                                                                                          |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Pass                                                                                         | -> Phase 4                                                                                      |
| Fail that is missing tests or missing requirement IDs in tests                               | Add the missing tests or wiring, re-run the script once, then continue only on pass             |
| Fail after that retry, or a provided contract still has no contract tests wired to `REQ-NNN` | **STOP** - report the uncovered IDs and `contractFailures`; do not write `completion-report.md` |


---



## Phase 4 - Write completion artifacts

**Step 4.1 - Write the completion report**

Read `templates/completion-report.md` and write `completion-report.md` into the same plan directory.

Include:

- the plan path
- which steps were implemented
- verification commands or checks run
- a markdown link to each test, build, or lint command's `verification-logs/` output file (do not paste the log body into the report)
- `n/a` in Output for Manual or n/a rows (do not invent a log)
- the overall outcome after final acceptance
- the requirement-test coverage gate result copied from `requirement-test-coverage.json` (that JSON is the coverage-gate evidence; do not also require a `verification-logs/` link for the gate command)
- any remaining manual follow-up

**Step 4.2 - Update** `handoff.json`

Populate only the coding-agent-owned execution fields defined in `references/handoff-contract.md`:

- `humanAcknowledgement` when the acknowledgement branch was used
- `implementationStatus`
- `completionReportPath`

Do not silently rewrite planner-owned readiness fields.

**Gate 4A - Completion artifacts consistent?**

- [ ] `completion-report.md` exists
- [ ] every report row that names a test, build, or lint command links to an existing file under `verification-logs/`
- [ ] Manual and n/a rows use `n/a` in Output and do not invent or link a log
- [ ] the Coverage gate **Command** row is not subject to the `verification-logs/` link rule; its evidence is `requirement-test-coverage.json`
- [ ] each linked test log contains a test runner stream, not only framework logs
- [ ] each linked build or lint log contains that tool's own success/failure or findings output (do not fabricate a test runner stream)
- [ ] `requirement-test-coverage.json` exists and `"passed"` is true
- [ ] `handoff.json.completionReportPath` points to that file
- [ ] `handoff.json.implementationStatus` matches the actual outcome
- [ ] Any stored `humanAcknowledgement.decision` is exactly `proceed_as_is` or `risk_resolved`


| Result   | Action                                     |
| -------- | ------------------------------------------ |
| All pass | **STOP** - implementation is complete      |
| Any fail | Fix the artifact mismatch before returning |


---



## Verification log files

Capture stdout and stderr for every verification command that actually ran (step-level and final acceptance). Write files into `<plan-dir>/verification-logs/`.

Each captured file must start with:

```text
command: <exact command>
cwd: <working directory>
exit_code: <integer>
```

Then a tool-appropriate body:

| Command kind | Required body |
| ------------ | ------------- |
| Test (unit, integration, boundary, or any invocation whose purpose is running tests) | A test runner stream: which suite or test file ran, pass/fail/skip counts, and the overall result. Maven Surefire (`Tests run: N, Failures: 0, Errors: 0, Skipped: 0` plus `BUILD SUCCESS` / `BUILD FAILURE`) is one example, not a requirement for pytest, jest, or other runners. |
| Build / compile | The compiler or build tool's own success/failure output. For Maven compile/package, `BUILD SUCCESS` / `BUILD FAILURE` is enough; do not fabricate Surefire `Tests run:` lines. |
| Lint / static analysis | The linter's own report (findings or a clean run). Do not fabricate a test runner stream. |

Framework logs can sit around a test runner stream; they cannot replace it.

Do not pass quiet or silent flags (`-q`, `--quiet`, `--silent`) on commands cited as test or build evidence. `exit_code: 0` plus runtime noise is not a runner stream. If the tool is quiet by default, raise verbosity or append its report file (for example `target/surefire-reports/*.txt`) into the same log.

Use these names:


| Run                             | File                                                    |
| ------------------------------- | ------------------------------------------------------- |
| Plan Step 0                     | `verification-logs/step-0.txt`                          |
| Plan Step N                     | `verification-logs/step-N.txt`                          |
| Extra commands in the same step | `verification-logs/step-N-02.txt`, `step-N-03.txt`, ... |
| Final build / compile           | `verification-logs/final-build.txt`                     |
| Final lint / static analysis    | `verification-logs/final-lint.txt`                      |
| Final structural boundary tests | `verification-logs/final-boundary.txt`                  |
| Final unit tests                | `verification-logs/final-unit.txt`                      |
| Final integration tests         | `verification-logs/final-integration.txt`               |


If a planned check is `n/a` or `Manual:` and has no command, write `Manual: ...` in the report and `n/a` in the Output column. Do not invent an empty log and do not link `verification-logs/` for that row.

The coverage gate JSON at `<plan-dir>/requirement-test-coverage.json` is the output file for Gate 3B and the Coverage gate section of the report. Do not duplicate it under `verification-logs/`, and do not require a `verification-logs/` link for that command in Gate 4A.

In `completion-report.md`, attach evidence with relative markdown links from the plan directory, for example `[verification-logs/step-0.txt](verification-logs/step-0.txt)` or `[requirement-test-coverage.json](requirement-test-coverage.json)`.

---



## Do not continue when

- The only artifact is `plan.md` and no sibling `handoff.json` exists
- `READY_FOR_IMPLEMENTATION_WITH_ACK` is present but the user has not acknowledged the risk. The stop must already have listed the implementation risks in the chat
- `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true`. Do not treat a missing chat prompt, or a build request in this conversation, as approval
- A plan step contradicts an active `DD-NNN` and you are tempted to "just make it work"
- Step 0 coverage is incomplete and you are tempted to postpone it until after production code
- Final acceptance is still red and you are tempted to write completion artifacts anyway
- A test, build, or lint command ran and you are tempted to cite pass/fail in the report without a `verification-logs/` file
- A test log exists but contains only framework logs, or the command used quiet/silent flags that hid the runner stream
- A lint or compile log is padded with a fabricated test runner stream
- A Manual or n/a row is given a fake `verification-logs/` file, or the coverage-gate command is treated as a `verification-logs/` Gate 4A row
- Gate 3B is red and you are tempted to write `completion-report.md` from a prose coverage summary
- A contract or schema was provided and you are tempted to treat integration tests as a substitute for contract tests wired to `REQ-NNN`

