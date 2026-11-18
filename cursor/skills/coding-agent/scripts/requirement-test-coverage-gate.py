#!/usr/bin/env python3
"""Gate completion until input requirements have tests.

Also requires contract tests, wired to REQ IDs, when a contract artifact is
part of the plan or requirements package.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    ".tox",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "target",
    ".cursor",
}

ID_RE = re.compile(r"\b(REQ|QR|INV|POL)-(\d{3,})\b")
SOURCE_PREFIX = {
    "functional.md": "REQ",
    "quality.md": "QR",
    "invariants.md": "INV",
    "policies.md": "POL",
}
TEST_DIR_PARTS = {"test", "tests", "spec", "specs", "__tests__", "it", "e2e"}
TEST_FILE_RE = re.compile(
    r"(^test_|_test\.|\.test\.|\.spec\.|Test\.|Tests\.|Spec\.|IT\.|Contract)",
    re.I,
)
CONTRACT_NAME_RE = re.compile(
    r"(openapi|swagger|asyncapi|json.?schema|avro|protobuf|\.proto$|\.avsc$|"
    r"\.avdl$|\.graphql$|\.wsdl$|\.xsd$|pact)",
    re.I,
)
CONTRACT_TEST_RE = re.compile(r"(contract|pact|schemathesis|consumer.?driven)", re.I)
NOT_PROVIDED_RE = re.compile(r"\b(not provided|n/?a|none|not found|not applicable)\b", re.I)
MANUAL_RE = re.compile(r"\bManual\s*:", re.I)
BACKTICK_RE = re.compile(r"`([^`]+)`")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def collect_requirement_ids(requirements_path: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for filename, prefix in SOURCE_PREFIX.items():
        path = requirements_path / filename
        if not path.is_file():
            continue
        for match in ID_RE.finditer(read_text(path)):
            if match.group(1) != prefix:
                continue
            found[f"{match.group(1)}-{match.group(2)}"] = filename
    return found


def resolve_requirements_path(repo_root: Path, plan_dir: Path, handoff: dict) -> Path:
    raw = str(handoff.get("requirementsPath") or "").strip()
    candidates = []
    if raw:
        candidates.append((repo_root / raw).resolve())
        candidates.append(Path(raw).resolve())
    candidates.append(plan_dir.parent.resolve())
    for path in candidates:
        if (path / "functional.md").is_file() or (path / "handoff.json").is_file():
            return path
    return plan_dir.parent.resolve()


def is_ignored(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def is_test_file(path: Path) -> bool:
    if is_ignored(path) or not path.is_file():
        return False
    lowered_parts = {part.lower() for part in path.parts}
    name = path.name
    return bool(TEST_DIR_PARTS & lowered_parts) or bool(TEST_FILE_RE.search(name))


def iter_test_files(repo_root: Path, plan_dir: Path, requirements_path: Path) -> list[Path]:
    skip_roots = {plan_dir.resolve(), requirements_path.resolve()}
    files = []
    for path in repo_root.rglob("*"):
        if not path.is_file() or is_ignored(path):
            continue
        resolved = path.resolve()
        if any(resolved == root or root in resolved.parents for root in skip_roots):
            continue
        if is_test_file(path):
            files.append(path)
    return files


def extract_named_tests(plan_dir: Path) -> dict[str, list[str]]:
    names: dict[str, list[str]] = {}
    texts = [
        read_text(plan_dir / "plan.md"),
        read_text(plan_dir / "integration-test-scenarios.md"),
    ]
    for text in texts:
        for line in text.splitlines():
            id_match = ID_RE.search(line)
            if not id_match:
                continue
            rid = f"{id_match.group(1)}-{id_match.group(2)}"
            for name in BACKTICK_RE.findall(line):
                cleaned = name.strip("[]() ")
                if cleaned:
                    names.setdefault(rid, []).append(cleaned)
    return names


def mapping_is_manual(plan_dir: Path, requirement_id: str) -> bool:
    for filename in ("plan.md", "integration-test-scenarios.md"):
        for line in read_text(plan_dir / filename).splitlines():
            if requirement_id in line and MANUAL_RE.search(line):
                return True
    return False


def evidence_for_id(requirement_id: str, named_tests: list[str], test_files: list[Path]) -> list[str]:
    hits = []
    needles = [requirement_id, *named_tests]
    for path in test_files:
        text = read_text(path)
        if any(needle and needle in text for needle in needles):
            hits.append(str(path))
    return hits


def looks_like_contract(path: Path) -> bool:
    if path.suffix.lower() in {".md", ".py", ".ts", ".js", ".java", ".kt", ".go"}:
        return False
    if path.name in {"handoff.json", "package.json", "package-lock.json"}:
        return False
    return bool(CONTRACT_NAME_RE.search(path.name) or CONTRACT_NAME_RE.search(str(path)))


def contracts_from_text(repo_root: Path, plan_dir: Path, text: str) -> list[Path]:
    found = []
    for match in re.finditer(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]+", text):
        raw = match.group(0)
        if NOT_PROVIDED_RE.search(raw):
            continue
        for base in (repo_root, plan_dir, plan_dir.parent):
            candidate = (base / raw).resolve()
            if candidate.is_file() and looks_like_contract(candidate):
                found.append(candidate)
                break
    return found


def detect_contracts(repo_root: Path, plan_dir: Path, requirements_path: Path) -> list[Path]:
    contracts: list[Path] = []
    search_roots = [requirements_path, plan_dir]
    for root in search_roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and looks_like_contract(path):
                contracts.append(path.resolve())

    combined = "\n".join(
        [
            read_text(plan_dir / "plan.md"),
            read_text(plan_dir / "design-decisions.md"),
            read_text(plan_dir / "integration-test-scenarios.md"),
        ]
    )
    contracts.extend(contracts_from_text(repo_root, plan_dir, combined))

    unique: list[Path] = []
    seen = set()
    for path in contracts:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def is_contract_test(path: Path) -> bool:
    return bool(CONTRACT_TEST_RE.search(str(path)))


def evaluate(
    repo_root: Path,
    plan_dir: Path,
    requirements_path: Path,
    requirement_ids: dict[str, str],
) -> dict[str, object]:
    named_tests = extract_named_tests(plan_dir)
    test_files = iter_test_files(repo_root, plan_dir, requirements_path)
    contracts = detect_contracts(repo_root, plan_dir, requirements_path)
    contract_tests = [path for path in test_files if is_contract_test(path)]

    items = []
    uncovered = []
    for rid, source in sorted(requirement_ids.items()):
        prefix = rid.split("-", 1)[0]
        hits = evidence_for_id(rid, named_tests.get(rid, []), test_files)
        manual = prefix == "QR" and mapping_is_manual(plan_dir, rid)
        if hits:
            status = "covered"
        elif manual:
            status = "manual"
        else:
            status = "uncovered"
            uncovered.append(rid)
        items.append(
            {
                "id": rid,
                "source": source,
                "status": status,
                "tests": [str(Path(hit).relative_to(repo_root)) if Path(hit).is_relative_to(repo_root) else hit for hit in hits],
                "namedTests": named_tests.get(rid, []),
            }
        )

    contract_failures = []
    req_ids = [rid for rid in requirement_ids if rid.startswith("REQ-")]
    if contracts:
        if not contract_tests:
            contract_failures.append("contract-tests-missing: a contract was provided but no contract test exists")
        else:
            contract_blob = "\n".join(read_text(path) for path in contract_tests)
            for contract in contracts:
                if contract.name not in contract_blob and str(contract) not in contract_blob:
                    rel = contract.name
                    try:
                        rel = str(contract.relative_to(repo_root))
                    except ValueError:
                        pass
                    contract_failures.append(f"contract-untested: {rel} is not referenced by a contract test")
            wired = [rid for rid in req_ids if rid in contract_blob]
            unwired = [rid for rid in req_ids if rid not in contract_blob]
            if req_ids and not wired:
                contract_failures.append(
                    "contract-unwired: contract tests do not cite any input REQ IDs"
                )
            elif unwired:
                contract_failures.append(
                    "contract-unwired: contract tests do not cite " + ", ".join(unwired)
                )

    passed = not uncovered and not contract_failures
    return {
        "passed": passed,
        "requirementsPath": str(requirements_path.relative_to(repo_root))
        if requirements_path.is_relative_to(repo_root)
        else str(requirements_path),
        "planPath": str(plan_dir.relative_to(repo_root)) if plan_dir.is_relative_to(repo_root) else str(plan_dir),
        "items": items,
        "uncovered": uncovered,
        "contracts": [
            str(path.relative_to(repo_root)) if path.is_relative_to(repo_root) else str(path)
            for path in contracts
        ],
        "contractTests": [
            str(path.relative_to(repo_root)) if path.is_relative_to(repo_root) else str(path)
            for path in contract_tests
        ],
        "contractFailures": contract_failures,
    }


def validate(repo_root: Path, plan_dir: Path) -> dict[str, object]:
    handoff_path = plan_dir / "handoff.json"
    handoff = json.loads(read_text(handoff_path) or "{}")
    requirements_path = resolve_requirements_path(repo_root, plan_dir, handoff)
    requirement_ids = collect_requirement_ids(requirements_path)
    if not requirement_ids:
        return {
            "passed": False,
            "uncovered": [],
            "contracts": [],
            "contractTests": [],
            "contractFailures": [],
            "items": [],
            "requirementsPath": str(requirements_path),
            "planPath": str(plan_dir),
            "errors": ["no-requirement-ids: functional.md/quality.md/invariants.md/policies.md contained no REQ/QR/INV/POL IDs"],
        }
    result = evaluate(repo_root, plan_dir, requirements_path, requirement_ids)
    result["errors"] = []
    return result


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        req = root / "requirements" / "T-1"
        plan = req / "plan"
        _write(
            req / "functional.md",
            "#### REQ-001\n- **Statement**: Accept orders\n#### REQ-002\n- **Statement**: Reject invalid\n",
        )
        _write(req / "quality.md", "#### QR-001\n- **Statement**: p95 under 200ms\n")
        _write(req / "invariants.md", "#### INV-001\n- **Statement**: totals match lines\n")
        _write(req / "policies.md", "#### POL-001\n- **Statement**: decline over limit\n")
        _write(plan / "handoff.json", json.dumps({"requirementsPath": "requirements/T-1/"}))
        _write(
            plan / "plan.md",
            "| Functional | REQ-001 | Integration: `accepts_valid_order` |\n"
            "| Quality | QR-001 | Manual: load check |\n"
            "| Invariant | INV-001 | Unit: `total_matches_lines` |\n"
            "| Policy | POL-001 | Unit: `declines_over_limit` |\n"
            "| Contracts / schemas | docs/openapi.yaml |\n",
        )
        _write(root / "docs" / "openapi.yaml", "openapi: 3.0.0\n")
        _write(
            root / "src" / "test" / "AcceptIT.java",
            "void accepts_valid_order() { /* REQ-001 */ }\nvoid REQ-002() {}\n",
        )
        _write(
            root / "src" / "test" / "DomainTest.java",
            "void total_matches_lines() { /* INV-001 */ }\nvoid declines_over_limit() { /* POL-001 */ }\n",
        )

        missing_tests = validate(root, plan)
        assert missing_tests["passed"] is False
        assert "REQ-001" in json.dumps(missing_tests)
        assert any("contract" in f for f in missing_tests["contractFailures"])

        _write(
            root / "src" / "test" / "OrderContractTest.java",
            "void contract_accepts_valid_order() { /* openapi.yaml REQ-001 REQ-002 */ }\n",
        )
        covered = validate(root, plan)
        assert covered["passed"] is True, covered
        assert covered["uncovered"] == []
        assert covered["contracts"]


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--self-check":
        self_check()
        print("self-check: ok")
        return
    if len(sys.argv) != 3:
        print(
            "Usage: requirement-test-coverage-gate.py <repo-root> <plan-dir>",
            file=sys.stderr,
        )
        raise SystemExit(2)

    repo_root = Path(sys.argv[1]).resolve()
    plan_dir = Path(sys.argv[2]).resolve()
    if not repo_root.is_dir() or not plan_dir.is_dir():
        print("Repository root and plan directory must exist", file=sys.stderr)
        raise SystemExit(2)

    result = validate(repo_root, plan_dir)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result.get("passed") else 1)


if __name__ == "__main__":
    main()
