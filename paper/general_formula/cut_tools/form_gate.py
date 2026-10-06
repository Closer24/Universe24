"""The form gate of the main's body: the reviewer's measure (the owner's word of 2026-10-06, "go for it").

The body is every line from \\section{Introduction} to the end of Section 9 (the line before the
Statements' \\section), lines that begin with a backslash left out; a formula $...$ counts as one
word; a sentence ends at '.', '!' or '?' followed by a space and a capital, a backslash or an
opening parenthesis; words are whitespace tokens; a paragraph is one source line. A status
parenthesis is one whose first word is a key word (derived, theorem, assumption, computed,
declaration, hypothesis, comparison, definition, fitted, calibration, experiment, inspiration,
prediction, or "a theorem"); it is mid-sentence when the character after its closing parenthesis is
not a period; it is fenceless when it holds neither "lattice" nor "clicks". The register counts:
semicolons per sentence and in all, commas per sentence (the mean and the most).

The targets: the longest sentence <= 80 words, the mean < 40, the longest paragraph <= 300 words,
mid-sentence status parentheses 0, fenceless 0, semicolons under 100 in all and at most one per
sentence, commas under three per sentence on average and none over eight.

Usage: python form_gate.py [main.tex] [--list] [--quiet]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KEY_WORDS = (
    "derived",
    "theorem",
    "assumption",
    "computed",
    "declaration",
    "hypothesis",
    "comparison",
    "definition",
    "fitted",
    "calibration",
    "experiment",
    "inspiration",
    "prediction",
)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z\\(])")
FORMULA = re.compile(r"\$[^$]*\$")
STATEMENTS = re.compile(r"\\section\*?\{(Statements|Declarations|Acknowledg)")


def body_lines(text: str) -> list[tuple[int, str]]:
    """The body's source lines with their numbers: from the Introduction to the end of Section 9."""
    lines = text.split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("\\section{Introduction}"))
    end = next(
        (
            i
            for i, line in enumerate(lines)
            if i > start and (STATEMENTS.match(line) or line.startswith("\\begin{thebibliography}"))
        ),
        len(lines),
    )
    return [
        (i + 1, line)
        for i, line in enumerate(lines[start:end], start)
        if line.strip() and not line.startswith("\\")
    ]


def words_of(sentence: str) -> int:
    return len(FORMULA.sub("F", sentence).split())


def sentences_of(line: str) -> list[str]:
    return [s for s in SENTENCE_END.split(line) if s.strip()]


def parentheses_of(line: str) -> list[tuple[int, str, bool, bool]]:
    """Every status parenthesis of the line: its offset, text, mid-sentence and fenceless."""
    found = []
    depth = 0
    start = -1
    for i, ch in enumerate(line):
        if ch == "(":
            if depth == 0:
                start = i
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
            if depth == 0:
                inner = line[start + 1 : i]
                first = inner.split()[0].lower().strip(",;:") if inner.split() else ""
                if first == "a" and inner.lower().startswith("a theorem"):
                    first = "theorem"
                if first in KEY_WORDS:
                    after = line[i + 1 : i + 2]
                    mid = after != "."
                    fenceless = "lattice" not in inner and "clicks" not in inner
                    found.append((start, inner, mid, fenceless))
    return found


def measure(text: str) -> dict:
    lines = body_lines(text)
    sentences: list[tuple[int, str, int]] = []
    paragraphs: list[tuple[int, int]] = []
    marks: list[tuple[int, str, bool, bool]] = []
    for number, line in lines:
        paragraphs.append((number, words_of(line)))
        for s in sentences_of(line):
            sentences.append((number, s, words_of(s)))
        for _offset, inner, mid, fenceless in parentheses_of(line):
            if mid or fenceless:
                marks.append((number, inner, mid, fenceless))
    counts = [n for _, _, n in sentences]
    semis = [s.count(";") for _, s, _ in sentences]
    commas = [s.count(",") for _, s, _ in sentences]
    return {
        "sentences": len(sentences),
        "mean": sum(counts) / len(counts),
        "over 40": sum(n > 40 for n in counts),
        "over 80": sum(n > 80 for n in counts),
        "over 100": sum(n > 100 for n in counts),
        "over 200": sum(n > 200 for n in counts),
        "longest": max(counts),
        "paragraphs": len(paragraphs),
        "paragraphs over 300": sum(n > 300 for _, n in paragraphs),
        "longest paragraph": max(n for _, n in paragraphs),
        "mid-sentence status parentheses": sum(mid for _, _, mid, _ in marks),
        "fenceless status parentheses": sum(f for _, _, _, f in marks),
        "semicolons": sum(semis),
        "sentences with two semicolons or more": sum(n >= 2 for n in semis),
        "commas per sentence": sum(commas) / len(commas),
        "sentences with more than eight commas": sum(n > 8 for n in commas),
        "_marks": marks,
        "_long": sorted(((n, number, s) for number, s, n in sentences if n > 80), reverse=True),
        "_paragraphs": sorted(((n, number) for number, n in paragraphs if n > 300), reverse=True),
    }


TARGETS = {
    "longest": 80,
    "mean": 40,
    "longest paragraph": 300,
    "mid-sentence status parentheses": 0,
    "fenceless status parentheses": 0,
    "semicolons": 99,
    "sentences with two semicolons or more": 0,
    "commas per sentence": 3,
    "sentences with more than eight commas": 0,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "main", nargs="?", default=str(Path(__file__).resolve().parent.parent / "main.tex")
    )
    parser.add_argument(
        "--list", action="store_true", help="print the parentheses and the long sentences"
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    m = measure(Path(args.main).read_text(encoding="utf-8"))
    failed = 0
    for key, value in m.items():
        if key.startswith("_"):
            continue
        target = TARGETS.get(key)
        ok = target is None or (
            value < target if key in ("mean", "commas per sentence") else value <= target
        )
        failed += not ok
        shown = f"{value:.1f}" if isinstance(value, float) else str(value)
        if not args.quiet or target is not None:
            print(
                f"{'ok  ' if ok else 'FAIL'} {key}: {shown}"
                + (
                    f" (target {'<' if key in ('mean', 'commas per sentence') else '<='} {target})"
                    if target is not None
                    else ""
                )
            )
    if args.list:
        print("\nthe status parentheses mid-sentence (M) or without a fence (F):")
        for number, inner, mid, fenceless in m["_marks"]:
            print(f"  L{number} {'M' if mid else ' '}{'F' if fenceless else ' '} ({inner[:110]})")
        print("\nthe sentences over 80 words:")
        for n, number, s in m["_long"]:
            print(f"  L{number} {n}: {s[:100]}")
        print("\nthe paragraphs over 300 words:")
        for n, number in m["_paragraphs"]:
            print(f"  L{number} {n}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
