"""The statement apart from its provenance (the owner's word of 2026-10-04: a perfect algebra; the advisor's proposal, #1793 comment 5974878000, item on the split): docs/ALGEBRA.md keeps each rule's statement, its numbers with their inputs, its status and its fence, and `docs/PROVENANCE.md` keeps what says who, when and where: the hands' comment ids, the owner's words with their dates, the pull requests and squashes, the HIGHLIGHTS lines and the dated history. A provenance clause leaves its parenthesis and a tag `[p<n>]` stands in its place; the tag heads the clause under the line's anchor in PROVENANCE.md, so nothing is lost and every statement can be read, checked against the engine and cited without the record in the way.

What moves: inside a parenthetical group of a line, each clause (split at semicolons) that carries a comment id (ten digits), a pull request or squash, a HIGHLIGHTS line, the owner's dated word, or a hand's numbered item; a clause with none of them stays where it is, so the physics inside a mixed group is untouched. A group left empty by the move leaves with its tag.

Usage: `python tools/split_provenance.py --report [path]` prints what would move (the counts, the longest lines before and after, three samples) and changes nothing; `python tools/split_provenance.py --apply` rewrites docs/ALGEBRA.md and writes docs/PROVENANCE.md, for a pull request read by two hands.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAW, PROVENANCE = ROOT / "docs" / "ALGEBRA.md", ROOT / "docs" / "PROVENANCE.md"
MARKERS = re.compile(
    r"\b\d{10}\b|#\d{4} comments?|pull request #\d+|\bsquash [0-9a-f]{7,}|HIGHLIGHTS\.md|"
    r"the owner's (?:word|words|decision)s? of 20\d\d-\d\d-\d\d|verbatim in translation|"
    r"\bthe (?:mathematician|advisor|reviewer|writer|experimenter)'s \d{2,3}\b|\b20\d\d-\d\d-\d\d\b"
)
HEADING = re.compile(r"^\s*(?:\|\s*)?(?:\(\w+\d?\)\s*|\d+\.\s*|[a-z]\.\s*)?\*\*([^*]{3,120})\*\*")


def groups(line: str) -> list[tuple[int, int]]:
    """The spans of the balanced parenthetical groups of a line, outermost only."""
    spans, depth, start = [], 0, 0
    for i, c in enumerate(line):
        if c == "(":
            if depth == 0:
                start = i
            depth += 1
        elif c == ")" and depth:
            depth -= 1
            if depth == 0:
                spans.append((start, i + 1))
    return spans


def split(line: str, tag: int) -> tuple[str, list[tuple[int, str]], int]:
    """One line with its provenance clauses moved out: the new line, the moved clauses with their tags, the next tag."""
    out, at, moved = [], 0, []
    for start, end in groups(line):
        inner = line[start + 1 : end - 1]
        clauses = [c.strip() for c in inner.split("; ")]
        if not any(MARKERS.search(c) for c in clauses):
            continue
        kept = [c for c in clauses if not MARKERS.search(c)]
        gone = [c for c in clauses if MARKERS.search(c)]
        tags = []
        for clause in gone:
            moved.append((tag, clause))
            tags.append(f"[p{tag}]")
            tag += 1
        replacement = "(" + "; ".join(kept + tags) + ")" if kept else " ".join(tags)
        out.append(line[at:start] + replacement)
        at = end
    out.append(line[at:])
    return "".join(out), moved, tag


def anchor(line: str, number: int) -> str:
    """The line's name in PROVENANCE.md: its bold heading, else its number and first words."""
    match = HEADING.match(line)
    return match.group(1).strip() if match else f"line {number}: {' '.join(line.split()[:6])}"


def run(text: str) -> tuple[str, str, dict[str, int | str]]:
    """The law's text split: the new law, the provenance document, the report's counts."""
    law, record, tag, longest = (
        [],
        [
            "# The provenance of the law\n",
            "What says who, when and where for each line of [ALGEBRA.md](ALGEBRA.md): the hands' comments, the owner's dated words, the pull requests, the HIGHLIGHTS lines and the dated history, each under its line's name and headed by the tag that stands in the line. The law states; this document records.\n",
        ],
        1,
        (0, 0),
    )
    for number, line in enumerate(text.split("\n"), 1):
        new, moved, tag = split(line, tag)
        law.append(new)
        longest = (max(longest[0], len(line)), max(longest[1], len(new)))
        if moved:
            record.append(f"\n## {anchor(line, number)}\n")
            record += [f"- [p{t}] {clause}" for t, clause in moved]
    counts: dict[str, int | str] = {
        "clauses moved": tag - 1,
        "characters before": len(text),
        "characters after": len("\n".join(law)),
        "longest line before": longest[0],
        "longest line after": longest[1],
    }
    return "\n".join(law), "\n".join(record) + "\n", counts


def main() -> int:
    path = Path(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--report" else LAW
    law, record, counts = run(path.read_text(encoding="utf-8"))
    if "--apply" in sys.argv:
        LAW.write_text(law, encoding="utf-8")
        PROVENANCE.write_text(record, encoding="utf-8")
    for key, value in counts.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
