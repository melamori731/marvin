#!/usr/bin/env python3
"""Validate a candidate architecture style against repository evidence."""

from __future__ import annotations

import json
import math
import os
import re
import sys
from dataclasses import dataclass
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
    ".critique-and-revise",
}
TRUSTED_FILE_NAMES = {"AGENTS.md", "CLAUDE.md", "README.md", "CONTRIBUTING.md"}
TRUSTED_DIRS = (
    "ai-context-bank",
    "context-bank",
    "docs/ai-context-bank",
    "docs/context-bank",
    ".ai",
    ".cursor/rules",
    "docs/architecture",
    "docs/design",
    "docs/adr",
    "adr",
)
TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".adoc", ".yaml", ".yml", ".json"}
MAX_TEXT_BYTES = 250_000
MAX_EVIDENCE_ITEMS = 8
MAX_CONFLICT_ITEMS = 8


@dataclass(frozen=True)
class StyleDefinition:
    canonical_name: str
    aliases: tuple[str, ...]
    layout_groups: tuple[tuple[str, ...], ...]


STYLE_DEFINITIONS = (
    StyleDefinition(
        canonical_name="clean architecture",
        aliases=("clean architecture", "clean-architecture", "onion architecture", "onion"),
        layout_groups=(
            ("domain", "entity", "entities"),
            ("application", "usecase", "usecases", "use_case", "use_cases", "interactor"),
            ("adapter", "adapters", "interface", "interfaces", "port", "ports"),
            ("infrastructure", "infra", "framework", "frameworks"),
        ),
    ),
    StyleDefinition(
        canonical_name="hexagonal architecture",
        aliases=(
            "hexagonal architecture",
            "hexagonal",
            "ports and adapters",
            "ports-and-adapters",
            "ports & adapters",
        ),
        layout_groups=(
            ("domain", "entity", "entities"),
            ("application", "service", "services", "usecase", "usecases"),
            ("port", "ports"),
            ("adapter", "adapters"),
        ),
    ),
    StyleDefinition(
        canonical_name="layered architecture",
        aliases=("layered architecture", "layered", "n-tier", "tiered", "three-tier", "3-tier"),
        layout_groups=(
            ("controller", "controllers", "api", "web"),
            ("service", "services", "application"),
            ("repository", "repositories", "dao", "persistence", "data"),
            ("model", "models", "domain", "entity", "entities"),
        ),
    ),
    StyleDefinition(
        canonical_name="mvc",
        aliases=("model-view-controller", "model view controller", "mvc"),
        layout_groups=(
            ("model", "models"),
            ("view", "views", "template", "templates"),
            ("controller", "controllers"),
        ),
    ),
    StyleDefinition(
        canonical_name="package-by-feature",
        aliases=(
            "package-by-feature",
            "package by feature",
            "feature-first",
            "feature first",
            "feature-based",
            "module-first",
            "modular monolith",
        ),
        layout_groups=(
            ("feature", "features", "module", "modules"),
            ("shared", "common", "core"),
        ),
    ),
)


def normalize(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def split_tokens(text: str) -> set[str]:
    return set(token for token in re.split(r"[^a-z0-9]+", text.lower()) if token)


def recognize_style(candidate_style: str) -> tuple[StyleDefinition | None, str]:
    normalized = normalize(candidate_style)
    matches: list[tuple[int, StyleDefinition, str]] = []
    for definition in STYLE_DEFINITIONS:
        for alias in definition.aliases:
            normalized_alias = normalize(alias)
            if normalized_alias == normalized or normalized_alias in normalized:
                matches.append((len(normalized_alias), definition, alias))
    if not matches:
        return None, normalized
    _, definition, alias = max(matches, key=lambda item: item[0])
    return definition, normalize(alias)


def iter_trusted_files(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()

    def add_if_file(path: Path) -> None:
        if path.is_file() and path not in seen:
            seen.add(path)
            paths.append(path)

    for name in sorted(TRUSTED_FILE_NAMES):
        add_if_file(repo_root / name)

    for relative_dir in TRUSTED_DIRS:
        base = repo_root / relative_dir
        if not base.exists():
            continue
        if base.is_file():
            add_if_file(base)
            continue
        for path in sorted(base.rglob("*")):
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
                add_if_file(path)

    return paths


def read_text(path: Path) -> str:
    data = path.read_text(encoding="utf-8", errors="ignore")
    if len(data) > MAX_TEXT_BYTES:
        return data[:MAX_TEXT_BYTES]
    return data


def collect_repo_tokens(repo_root: Path) -> set[str]:
    tokens: set[str] = set()
    for current_root, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in IGNORE_DIRS and not dirname.startswith(".")
        ]
        root_path = Path(current_root)
        if any(part in IGNORE_DIRS for part in root_path.parts):
            continue

        for part in root_path.relative_to(repo_root).parts:
            tokens.update(split_tokens(part))

        for filename in filenames:
            if filename.startswith("."):
                continue
            stem = Path(filename).stem
            tokens.update(split_tokens(stem))

    return tokens


def find_trusted_mentions(
    repo_root: Path,
    trusted_files: list[Path],
    candidate_alias: str,
    candidate_definition: StyleDefinition | None,
) -> tuple[list[str], list[str]]:
    evidence: list[str] = []
    conflicts: list[str] = []
    candidate_phrase = candidate_alias

    for path in trusted_files:
        text = normalize(read_text(path))
        display_path = relative_display(repo_root, path)
        if candidate_phrase and candidate_phrase in text:
            evidence.append(f"trusted-context: {display_path} mentions '{candidate_phrase}'")

        for definition in STYLE_DEFINITIONS:
            if candidate_definition and definition.canonical_name == candidate_definition.canonical_name:
                continue
            matched_alias = next(
                (alias for alias in definition.aliases if normalize(alias) in text),
                None,
            )
            if matched_alias:
                conflicts.append(
                    f"trusted-context-conflict: {display_path} mentions '{matched_alias}'"
                )

    return evidence, conflicts


def score_layout(
    definition: StyleDefinition,
    repo_tokens: set[str],
) -> tuple[int, int, list[str]]:
    hits: list[str] = []
    for group in definition.layout_groups:
        matched = next((token for token in group if token in repo_tokens), None)
        if matched:
            hits.append(matched)
    return len(hits), len(definition.layout_groups), hits


def relative_display(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def validate(repo_root: Path, candidate_style: str) -> dict[str, object]:
    candidate_definition, candidate_alias = recognize_style(candidate_style)
    trusted_files = iter_trusted_files(repo_root)
    repo_tokens = collect_repo_tokens(repo_root)

    evidence: list[str] = []
    conflicts: list[str] = []

    if candidate_definition is None:
        normalized_candidate = normalize(candidate_style)
        doc_hits = 0
        for path in trusted_files:
            text = normalize(read_text(path))
            if normalized_candidate and normalized_candidate in text:
                evidence.append(
                    f"trusted-context: {relative_display(repo_root, path)} mentions '{normalized_candidate}'"
                )
                doc_hits += 1
        confidence = "high" if doc_hits else "low"
        recommendation = "proceed" if confidence == "high" else "stop"
        if not doc_hits:
            conflicts.append(
                "validator-config: no deterministic checks are configured for this architecture label"
            )
        return {
            "confidence": confidence,
            "evidence": evidence[:MAX_EVIDENCE_ITEMS],
            "conflicts": conflicts[:MAX_CONFLICT_ITEMS],
            "recommendation": recommendation,
        }

    trusted_evidence, trusted_conflicts = find_trusted_mentions(
        repo_root, trusted_files, candidate_alias, candidate_definition
    )
    evidence.extend(trusted_evidence)
    conflicts.extend(trusted_conflicts)

    hit_count, group_count, hit_tokens = score_layout(candidate_definition, repo_tokens)
    if hit_count:
        evidence.append(
            f"source-layout: matched {hit_count}/{group_count} cue groups for {candidate_definition.canonical_name} ({', '.join(hit_tokens)})"
        )

    strongest_other: tuple[StyleDefinition, int, int, list[str]] | None = None
    for definition in STYLE_DEFINITIONS:
        if definition.canonical_name == candidate_definition.canonical_name:
            continue
        other_hits, other_groups, other_tokens = score_layout(definition, repo_tokens)
        if strongest_other is None or other_hits > strongest_other[1]:
            strongest_other = (definition, other_hits, other_groups, other_tokens)

    if strongest_other is not None:
        definition, other_hits, other_groups, other_tokens = strongest_other
        candidate_threshold = max(1, math.ceil(group_count / 2))
        if other_hits >= max(2, candidate_threshold + 1) and other_hits > hit_count:
            conflicts.append(
                f"source-layout-conflict: matched {other_hits}/{other_groups} cue groups for {definition.canonical_name} ({', '.join(other_tokens)})"
            )

    trusted_hit_count = len(trusted_evidence)
    if conflicts:
        confidence = "low"
    elif trusted_hit_count:
        confidence = "high"
    elif hit_count >= max(3, math.ceil(group_count * 0.75)):
        confidence = "high"
    elif hit_count >= max(1, math.ceil(group_count / 2)):
        confidence = "medium"
    else:
        confidence = "low"

    if confidence == "high":
        recommendation = "proceed"
    elif confidence == "medium":
        recommendation = "document"
    else:
        recommendation = "stop"

    if not evidence:
        evidence.append("source-layout: no matching architecture cues found in trusted context or repository layout")

    return {
        "confidence": confidence,
        "evidence": evidence[:MAX_EVIDENCE_ITEMS],
        "conflicts": conflicts[:MAX_CONFLICT_ITEMS],
        "recommendation": recommendation,
    }


def main() -> None:
    if len(sys.argv) != 3:
        print(
            "Usage: architecture-discovery-validator.py <repo-root> <candidate-style>",
            file=sys.stderr,
        )
        raise SystemExit(2)

    repo_root = Path(sys.argv[1]).resolve()
    candidate_style = sys.argv[2].strip()
    if not repo_root.is_dir():
        print(f"Repository root does not exist: {repo_root}", file=sys.stderr)
        raise SystemExit(2)
    if not candidate_style:
        print("Candidate style must be non-empty", file=sys.stderr)
        raise SystemExit(2)

    result = validate(repo_root, candidate_style)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
