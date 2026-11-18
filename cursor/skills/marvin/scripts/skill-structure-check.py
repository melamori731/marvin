#!/usr/bin/env python3
"""Smallest check that the marvin skill still encodes its human gates."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md",
    "references/workflow.md",
    "references/human-gates.md",
    "references/handoff-contract.md",
    "references/mode-behavior.md",
    "references/anti-patterns.md",
    "templates/human-pause.md",
    "evals/scenario-1-stop-for-planning-approval.json",
    "evals/scenario-2-steering-rewaits.json",
    "evals/scenario-3-analyst-blocked.json",
    "evals/scenario-4-ack-before-coding.json",
    "evals/scenario-5-approval-then-code-when-ready.json",
    "evals/scenario-6-story-branch.json",
    "evals/scenario-7-create-pr-after-coding.json",
]

MARKERS = {
    "SKILL.md": [
        "Use when",
        "Do NOT use",
        "requirement-analyst",
        "planner",
        "coding-agent",
        "AskQuestion",
        "create-pr",
    ],
    "references/workflow.md": [
        "Phase 1",
        "Phase 2",
        "Phase 3",
        "steering",
        "proceed_as_is",
        "risk_resolved",
        "BLOCKED",
        "solution-skeleton-spec",
        "design-decisions.md",
        "Step 1b",
        "Step 9",
        "create-pr",
        "AskQuestion",
        "self-answer",
        "story-branch.py",
        "not a literal branch",
        "ECCS-XXXX-emplement-tis-or-that",
        "git switch -c",
        "Do not stash",
        "Do not switch back to the previous branch",
        "git branch --show-current",
        "git branch <name>",
        "separate GitHub blob links",
    ],
    "references/human-gates.md": [
        "brownfield",
        "READY_FOR_IMPLEMENTATION_WITH_ACK",
        "requiresHumanInput",
        "AskQuestion",
        "create-pr",
        "separate GitHub blob links",
    ],
    "templates/human-pause.md": [
        "AskQuestion",
        "Slack, IDE, and CLI",
        "design-decisions.md",
        "solution-skeleton-spec.md",
    ],
}


def main() -> None:
    missing = [rel for rel in REQUIRED if not (ROOT / rel).is_file()]
    assert not missing, f"missing files: {missing}"
    for rel, needles in MARKERS.items():
        text = (ROOT / rel).read_text()
        absent = [needle for needle in needles if needle not in text]
        assert not absent, f"{rel} missing {absent}"
    description = (ROOT / "SKILL.md").read_text().split("---", 2)[1]
    assert len(description) < 1024, "frontmatter too long"
    gate = (ROOT / "references/workflow.md").read_text().split("**Gate 0B", 1)[1].split("## Phase 1", 1)[0]
    phase1_stop = [line for line in gate.splitlines() if "plan.md` will not be written" in line]
    assert len(phase1_stop) == 1, phase1_stop
    stop = phase1_stop[0]
    assert "requirements/<ticket-id>/handoff.json" in stop, stop
    assert "only" in stop, stop
    assert "not `run_planner`" in stop, stop
    assert "plan/handoff.json" not in stop, stop
    assert "run_coding_agent" not in stop, stop
    arch = [
        line
        for line in (ROOT / "references/anti-patterns.md").read_text().splitlines()
        if line.startswith("**Example (good):**") and "architecture style" in line
    ]
    assert len(arch) == 1 and "Gate 2A" in arch[0] and "Gate 2B" not in arch[0], arch
    workflow = (ROOT / "references/workflow.md").read_text()
    for needle in (
        "explicitly prompted",
        "GitHub",
        "already applied",
        "implementation risk",
        "Slack, IDE, and CLI",
        "Do not use IDE-only AskQuestion",
        "Do not self-answer",
        "Gate 3C",
        "Jira user story id",
    ):
        assert needle in workflow, needle
    planner = (ROOT.parent / "planner" / "references" / "workflow.md").read_text()
    for needle in (
        "already applied",
        "Gate 6C",
        "solution-skeleton-spec.md",
        "separate GitHub blob links",
    ):
        assert needle in planner, needle
    publication = (ROOT.parent / "planner" / "references" / "output-contract.md").read_text()
    pub_body = publication.split("## Skeleton review publication", 1)[1]
    assert "design-decisions.md" in pub_body
    assert "separate" in pub_body
    mode_body = publication.split("## Mode behavior", 1)[1]
    assert "separate GitHub blob links" in mode_body
    assert "Name the written `design-decisions.md` path and the GitHub blob URL of `solution-skeleton-spec.md`" not in mode_body
    assert "Then publish the skeleton spec and stop" not in mode_body
    steering = workflow.split("**Gate 2B", 1)[1].split("**Gate 2C", 1)[0]
    assert "publish the spec again" not in steering
    assert "separate GitHub blob links" in steering
    human_gates = (ROOT / "references/human-gates.md").read_text()
    assert "publish the spec again" not in human_gates
    assert "separate GitHub blob links for each" in human_gates.split("Steering during a required skeleton review", 1)[1].split("\n", 1)[0]
    evals = (ROOT.parent / "planner" / "evals" / "README.md").read_text()
    assert "publish the spec with a GitHub link" not in evals
    assert "separate GitHub blob links" in evals.split("Greenfield happy path", 1)[1].split("\n", 1)[0]
    coding = (ROOT.parent / "coding-agent" / "references" / "workflow.md").read_text()
    assert "does not require approval of `solution-skeleton-spec.md`" in coding
    assert "designRisks" in coding
    assert "GitHub" in coding
    assert "separate GitHub blob links" in coding
    gate1a = coding.split("**Gate 1A", 1)[1].split("**Step 1.2", 1)[0]
    assert "skeletonReviewRequired" in gate1a and "skeletonReviewApproved" in gate1a, gate1a
    handoff = (ROOT.parent / "planner" / "templates" / "handoff.json").read_text()
    for needle in ("skeletonReviewRequired", "skeletonReviewApproved", "solutionSkeletonSpecUrl"):
        assert needle in handoff, needle
    template = ROOT.parent / "planner" / "templates" / "solution-skeleton-spec.md"
    assert template.is_file(), template
    assert not (ROOT.parent / "planner" / "templates" / "planning-evidence.md").exists()
    branch = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "story-branch.py"), "--self-check"],
        capture_output=True,
        text=True,
    )
    assert branch.returncode == 0, branch.stderr + branch.stdout
    print("marvin structure ok")


if __name__ == "__main__":
    main()
