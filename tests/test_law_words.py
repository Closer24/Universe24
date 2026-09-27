"""The law document's words and links: no other noun for the GameBoard or a Node, and every internal link names a heading (the gate of #1198, gate 5)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAW = ROOT / "docs" / "ALGEBRA.md"
# the GameBoard is the only noun for the lattice of Nodes, and a Node the only noun for a location
FORBIDDEN = re.compile(r"\b(?:board|lattice|grid|site)s?\b", re.IGNORECASE)
LINK = re.compile(r"\]\(#([^)\s]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def slug(heading: str) -> str:
    """GitHub's anchor of a heading: lower case, punctuation dropped but hyphens, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def findings(text: str) -> list[str]:
    """Every forbidden noun (by line) and every internal link with no heading of its name."""
    found: list[str] = []
    anchors: set[str] = set()
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            fenced = not fenced
            continue
        heading = None if fenced else HEADING.match(line)
        if heading:
            anchors.add(slug(heading.group(2)))
        for word in FORBIDDEN.findall(line.replace("GameBoard", "")):
            found.append(f"line {number}: {word!r}; the GameBoard and the Node are the only nouns")
    for anchor in sorted(set(LINK.findall(text)) - anchors):
        found.append(f"the link #{anchor} names no heading")
    return found


def test_the_law_uses_the_canonical_nouns_and_its_links_resolve():
    assert findings(LAW.read_text(encoding="utf-8")) == []


def test_a_forbidden_noun_and_a_dangling_link_fail():
    text = "# The law\n\n## Rule3\n\nThe GameBoard is a lattice of Nodes; see [Rule3](#rule3) and [x](#gone).\n"
    assert findings(text) == [
        "line 5: 'lattice'; the GameBoard and the Node are the only nouns",
        "the link #gone names no heading",
    ]
    assert findings("# A\n\n```\nboard\n```\n[a](#a)\n") == [
        "line 4: 'board'; the GameBoard and the Node are the only nouns"
    ]
