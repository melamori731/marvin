# Coding-agent anti-patterns

## Anti-Pattern 1: Building from `plan.md` alone

**Red flag:** The agent starts coding after reading only `plan.md`, without the sibling `handoff.json` or `design-decisions.md`.

**Why it happens:** The plan looks detailed enough, so the acknowledgement and decision files feel optional.

**Fix:** Resolve the full sibling artifact set first and stop if `handoff.json` or `design-decisions.md` is missing.

**Example (BAD):**
Start implementing from `planning/ECCS-12837/plan.md` because the step list is visible.

**Example (GOOD):**
Resolve `planning/ECCS-12837/plan.md`, `planning/ECCS-12837/handoff.json`, and `planning/ECCS-12837/design-decisions.md` before any edits.

**Related:** `references/workflow.md` Gate 0A, `references/rules.md` Input and path rules

## Anti-Pattern 2: Skipping Step 0 coverage

**Red flag:** The agent postpones integration-test scaffolding until the end because production code feels more urgent.

**Why it happens:** Step 0 can look like setup rather than implementation.

**Fix:** Treat Step 0 as the first implementation gate and keep `integration-test-scenarios.md` as the coverage source of truth.

**Example (BAD):**
"I'll add the integration cases after the feature works."

**Example (GOOD):**
"I set up the Step 0 scenario coverage first, confirmed the tests run, and only then moved to Step 1."

**Related:** `references/workflow.md` Step 2.1, `references/rules.md` Verification rules

## Anti-Pattern 3: Collapsing multiple plan steps into one blob

**Red flag:** Several numbered steps are implemented together because they touch the same module.

**Why it happens:** Shared files create pressure to "just do it all now."

**Fix:** Execute the plan step by step and run each step's verification before moving on, even when file overlap exists.

**Example (BAD):**
Implement Step 1 boundary changes, Step 2 domain logic, and Step 3 adapters in one unverified patch.

**Example (GOOD):**
Finish Step 1, run its boundary checks and acceptance criteria, then continue to Step 2 with a fresh scope.

**Related:** `references/workflow.md` Step 2.2, `references/rules.md` Execution order rules

## Anti-Pattern 4: Silently overriding an active `DD-NNN`

**Red flag:** The codebase makes a planned decision awkward, so the agent chooses a different design without surfacing it.

**Why it happens:** Local implementation pressure makes deviation feel faster than pausing.

**Fix:** Stop and report the contradiction whenever an active `DECIDED` or acknowledged `REQUIRES_ACK` decision becomes unsafe or impossible.

**Example (BAD):**
"The decision says add a boundary test, but I used a package-private shortcut instead because it was easier."

**Example (GOOD):**
"Step 3 conflicts with `DD-004`; I stopped and surfaced the mismatch instead of silently changing the design."

**Related:** `references/workflow.md` Gate 2B, `references/rules.md` Design decision rules

## Anti-Pattern 5: Treating `READY_FOR_IMPLEMENTATION_WITH_ACK` as implied consent

**Red flag:** The handoff carries risks, but the agent proceeds because the user asked to build the plan.

**Why it happens:** The build request is mistaken for acceptance of planning risk.

**Fix:** Stop until the user explicitly clears the risk with `proceed_as_is` or `risk_resolved`. The stop chat lists the acknowledgement reason and every implementation risk. Then persist that acknowledgement. Do not also demand skeleton approval unless `skeletonReviewRequired` is `true` and `skeletonReviewApproved` is not `true`.

**Example (BAD):**
Start coding immediately because the chat said "Build it." Or hide the risks and only say "please acknowledge."

**Example (GOOD):**
List each `designRisks` entry and the acknowledgement reason in the chat, ask for explicit acknowledgement, record it in `handoff.json.humanAcknowledgement`, then resume implementation.

**Related:** `references/workflow.md` Gate 1A, `references/mode-behavior.md` Acknowledgement pause

## Anti-Pattern 6: Declaring completion before final acceptance

**Red flag:** The agent writes `completion-report.md` or updates `handoff.json` before the planned final acceptance and coverage sign-off are actually green.

**Why it happens:** Step-level verification passed, so the broader finish gate feels optional.

**Fix:** Treat Final acceptance plus Coverage sign-off as the terminal gate, and only write completion artifacts after that verification succeeds or the plan explicitly records a manual exception.

**Example (BAD):**
"The step checks passed, so I already marked `implementationStatus` COMPLETE."

**Example (GOOD):**
"I finished the step work, ran Final acceptance and Coverage sign-off, confirmed they matched the plan, and only then wrote the completion artifacts."

**Related:** `references/workflow.md` Phase 3 and Phase 4, `references/rules.md` Verification rules

## Anti-Pattern 7: Writing a completion report before the coverage gate

**Red flag:** The agent writes `completion-report.md` after tests look green, without running `requirement-test-coverage-gate.py` against the input requirement IDs.

**Why it happens:** Final acceptance ran, so a separate requirement-to-test check feels redundant.

**Fix:** Gate 3B is mandatory. Every input `REQ-NNN`, `INV-NNN`, and `POL-NNN` needs a respective test, and `QR-NNN` needs a test or an explicit `Manual:` mapping. Do not write the completion report while `uncovered` is non-empty.

**Example (BAD):**
"The suite passed, so I wrote `completion-report.md` and listed coverage from memory."

**Example (GOOD):**
"I ran the coverage gate, it showed `REQ-003` uncovered, I added the missing test, re-ran the gate to `"passed": true`, and only then wrote the completion report."

**Related:** `references/workflow.md` Gate 3B, `references/rules.md` Verification rules

## Anti-Pattern 8: Shipping a provided contract without contract tests

**Red flag:** An OpenAPI, Avro, proto, or similar contract is in the inputs, but the agent only adds unit or integration tests and never adds contract tests that cite the `REQ-NNN` IDs.

**Why it happens:** Ordinary tests already exercise the happy path, so a dedicated contract suite feels optional.

**Fix:** When a contract is provided, add contract tests that reference the contract artifact and wire every input `REQ-NNN` into those tests. Stop if the coverage gate reports `contractFailures`.

**Example (BAD):**
"The API integration tests pass, so I skipped contract tests for `openapi.yaml`."

**Example (GOOD):**
"A contract was provided, so I added contract tests that load that artifact and cite `REQ-001` and `REQ-002` before writing completion artifacts."

**Related:** `references/workflow.md` Gate 3B, `references/rules.md` Verification rules

## Anti-Pattern 9: Claiming tests passed without a log file

**Red flag:** The completion report says a command passed, but there is no file under `verification-logs/`, or the report pastes a summary instead of linking the captured output.

**Why it happens:** The agent saw the command succeed in the session and treats the chat as evidence.

**Fix:** Redirect or copy each verification command's stdout and stderr into `verification-logs/`, then link that file from `completion-report.md`.

**Example (BAD):**
"Unit tests passed" with no `verification-logs/final-unit.txt`.

**Example (GOOD):**
`[verification-logs/final-unit.txt](verification-logs/final-unit.txt)` exists, starts with `command:` / `exit_code:`, and matches the claimed result.

**Related:** `references/workflow.md` Verification log files and Gate 4A, `references/rules.md` Completion artifact rules

## Anti-Pattern 10: Capturing framework logs instead of a test runner stream

**Red flag:** The linked `verification-logs/` file exists and has `exit_code: 0`, but the body is only SLF4J, Jersey, Grizzly, or similar runtime noise. There is no suite name, no `Tests run: N, Failures: 0, Errors: 0, Skipped: 0`, and no `BUILD SUCCESS` / `BUILD FAILURE` (or the tool's equivalent). Common cause: `mvn -q ... test`.

**Why it happens:** Quiet flags hide Surefire (or the equivalent runner). The agent treats any captured stdout plus a zero exit as proof.

**Fix:** Re-run without quiet or silent flags. Keep the header, then the test runner stream, enough that a reviewer can see which suite ran, the counts, and the build/test result. Framework logs can sit around that; they cannot replace it. If the runner is still quiet, append its report file into the same log.

**Example (BAD):**
`command: mvn -q -Dtest=DeviceTrustSignalIT test` followed only by Jersey provider warnings and Grizzly start/stop lines.

**Example (GOOD):**
`command: mvn -Dtest=DeviceTrustSignalIT test` followed by the suite name `DeviceTrustSignalIT`, `Tests run: N, Failures: 0, Errors: 0, Skipped: 0`, and `BUILD SUCCESS`.

**Related:** `references/workflow.md` Verification log files, Gate 3A, and Gate 4A, `references/rules.md` Execution order rules
