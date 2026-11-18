#!/usr/bin/env python3
"""Print the git branch for a ticket and a user-story title.

Pattern: <ticket-id>-<slug>. The slug comes from the title argument.
A placeholder such as ECCS-XXXX-emplement-tis-or-that is not a default.
"""

from __future__ import annotations

import argparse
import re
import sys

# ponytail: non-ASCII letters become hyphens. Transliterate if a title becomes unreadable.
SLUG_LIMIT = 48
TICKET = re.compile(r"^[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$")


def slugify(title: str, limit: int = SLUG_LIMIT) -> str:
    chars: list[str] = []
    hyphen = False
    for ch in title.strip().lower():
        if ch.isascii() and ch.isalnum():
            chars.append(ch)
            hyphen = False
        elif chars and not hyphen:
            chars.append("-")
            hyphen = True
    slug = "".join(chars).strip("-")
    if len(slug) <= limit:
        return slug
    cut = slug.rfind("-", 0, limit + 1)
    if cut <= 0:
        return slug[:limit]
    return slug[:cut]


def story_branch(ticket_id: str, title: str) -> str:
    ticket = ticket_id.strip()
    if not TICKET.fullmatch(ticket):
        raise ValueError(f"ticket key is not usable in a branch name: {ticket_id!r}")
    text = title.strip()
    if not text:
        raise ValueError("user story title is empty")
    if text.lower().startswith(ticket.lower()):
        rest = text[len(ticket) :].lstrip(" \t:-_")
        if rest:
            text = rest
        else:
            raise ValueError("user story title is only the ticket key")
    slug = slugify(text)
    if not slug:
        raise ValueError("user story title has no slug")
    return f"{ticket}-{slug}"


def self_check() -> int:
    expect = {
        ("ECCS-4521", "Implement this or that"): "ECCS-4521-implement-this-or-that",
        ("ECCS-4521", "ECCS-4521: Implement this or that"): "ECCS-4521-implement-this-or-that",
        ("PROJ-200", "Add login!"): "PROJ-200-add-login",
        ("LOCAL-auth-flow", "Reset expired sessions"): "LOCAL-auth-flow-reset-expired-sessions",
        ("ECCS-1", "this / that"): "ECCS-1-this-that",
        (
            "ECCS-4521",
            "Implement the billing export for quarterly finance review and archive",
        ): "ECCS-4521-implement-the-billing-export-for-quarterly",
    }
    for (ticket, title), branch in expect.items():
        got = story_branch(ticket, title)
        if got != branch:
            print(f"{ticket!r} {title!r} -> {got!r}, want {branch!r}", file=sys.stderr)
            return 1
    if story_branch("ECCS-4521", "Implement this or that") == "ECCS-XXXX-emplement-tis-or-that":
        print("example title mapped to the placeholder branch", file=sys.stderr)
        return 1
    for ticket, title in (("", "Implement this"), ("ECCS-4521", "   "), ("ECCS-4521", "ECCS-4521"), ("NOT A KEY", "Implement this")):
        try:
            story_branch(ticket, title)
        except ValueError:
            continue
        print(f"accepted bad input {ticket!r} {title!r}", file=sys.stderr)
        return 1
    print("story-branch ok")
    return 0


def main(argv: list[str]) -> int:
    if "--self-check" in argv[1:]:
        return self_check()
    parser = argparse.ArgumentParser(description="Print <ticket-id>-<user-story-slug>.")
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args(argv[1:])
    try:
        print(story_branch(args.ticket, args.title))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
