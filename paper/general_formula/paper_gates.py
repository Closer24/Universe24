"""The paper's mechanical gates (the advisor's proposal of 2026-10-04, #1793 comment 5974878000; the owner's word
"examine it and see how it can enter now"): run on main.tex and supplement.tex, each gate prints its misses and the
script exits non-zero on any.

1. The marks: every \\claimmark carries one of the key's words of Section 1 (theorem, derived, computed, assumption,
   hypothesis, experiment, fitted, inspiration) and every \\fence one of its two fences (clicks, GameBoard); a derived
   or theorem mark stands beside a fence inside its own parenthesis (R191 (g)).
2. The stale phrases: the words tonight's prints struck (R162 to R196, W1 to W29) stand nowhere; a hand adds a phrase
   to the list when a print strikes it, and the gate keeps it struck.
3. The second places: a number or a word that one print changed in one place and not in its twin (R180's column,
   R61's convention, W4's count, W1's intervals): each pair asserted equal where both documents print it.

    python paper/general_formula/paper_gates.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = {"main.tex": HERE / "main.tex", "supplement.tex": HERE / "supplement.tex"}

MARKS = {
    "theorem",
    "derived",
    "computed",
    "assumption",
    "hypothesis",
    "experiment",
    "fitted",
    "inspiration",
}
FENCES = {"clicks", "gameboard"}

# the phrases the prints struck, with the finding that struck each (the hands add a line with its finding)
STALE = [
    ("not yet built", "W2"),
    ("not yet implemented", "W3"),
    ("the next version", "W6"),
    ("this version of the implementation", "R174 (d)"),
    ("is being checked", "R173 (e)"),
    ("MISS at a lay", "W2"),
    ("by design, since", "W2"),
    ("four declarations", "W24"),
    ("three declarations", "W24"),
    ("never one Node", "W26 (the reader with Nodes alone excepted below)"),
    ("three named findings", "W4"),
    ("three findings of the conversion", "W4"),
    ("the nine declarations", "R173 (k)"),
    ("the two slits $128$", "W1"),
    ("integer slopes", "R145"),
    ("three-point mean", "R166"),
    ("no click names a Node to us", "R173 (s)"),
    ("positronium $56$ percent", "R61"),
    ("the singlet's known form", "S.10's word"),
    ("Table 5", "R171 (c)"),
    ("the automated reviewer", "R171 (i)"),
    ("with the reason, with the reason", "R190"),
    ("nature's $10^{-15}$", "R77"),
    ("short by $5.9$", "R184"),
    ("the top velocity of its mode", "R179"),
    ("1:1", "the README's figures clause"),
]
# a struck phrase allowed in one named sentence, by a fragment of that sentence
STALE_ALLOWED = {
    "never one Node": [
        "A NodeReader with Nodes alone is one connected region of two Nodes or more declared in the file, never one Node"
    ],
}

# a number or a word printed in two places: every fragment must be found in the named file
TWINS = [
    ("the Zeno column", [("supplement.tex", "$1.000$, $0.508$, $0.367$, $0.233$ and $0.133$")]),
    (
        "the gate's intervals",
        [
            (
                "main.tex",
                "the two slits over $130$ intervals, Bell's four over $100$, the GHZ's four over $60$",
            )
        ],
    ),
    (
        "the conversion's two findings",
        [
            ("main.tex", "two named findings"),
            ("supplement.tex", "two named findings"),
            ("supplement.tex", "the two findings of the conversion"),
        ],
    ),
    (
        "positronium's convention",
        [
            ("main.tex", "positronium $44$ percent of nature's"),
            ("supplement.tex", "positronium $44$ percent of nature's"),
            ("supplement.tex", "$44$ percent of nature's, the line at $38$"),
        ],
    ),
    (
        "the real line's numbers",
        [
            ("main.tex", "$277.8$ ($278.0$ in the physical labels)"),
            ("main.tex", "$N = 277.85$ in the engine's labels"),
        ],
    ),
    (
        "the subluminal chain",
        [("main.tex", "2.0 \\times 10^{-28}"), ("supplement.tex", "2.0 \\times 10^{-28}")],
    ),
    (
        "the neutron's lifetime",
        [("main.tex", "$878.4 \\pm 0.5$"), ("supplement.tex", "$878.4 \\pm 0.5$")],
    ),
    (
        "alpha_law at 1/28",
        [
            ("main.tex", "$\\alpha_{\\mathrm{law}} = 1 / 28$ (the design's $T = 0.259\\,\\Gamma^2$"),
            (
                "supplement.tex",
                "$\\alpha_{\\mathrm{law}} = 1 / 28$ (the design's $T = 0.259\\,\\Gamma^2$",
            ),
        ],
    ),
    ("the draw's bound", [("main.tex", "$2 \\times 10^{-8}$ at the width $63$")]),
    (
        "the wall of a massless family",
        [
            ("main.tex", "$3\\,\\den\\,T$ for a massless family"),
            ("supplement.tex", "$3\\,\\den\\,T$ for a massless family"),
        ],
    ),
    ("Delta = 1/m*", [("main.tex", "$\\Delta = 1 / m^*$"), ("supplement.tex", "$\\Delta = 1 / m^*$")]),
]


def enclosing_parenthesis(text: str, at: int) -> str:
    """The text inside the innermost parenthesis around the position, or the sentence around it."""
    depth = 0
    start = None
    for i in range(at, -1, -1):
        c = text[i]
        if c == ")":
            depth += 1
        elif c == "(":
            if depth == 0:
                start = i
                break
            depth -= 1
    if start is None:
        return text[max(0, at - 200) : at + 200]
    depth = 0
    for j in range(start, len(text)):
        c = text[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start : j + 1]
    return text[start : at + 200]


def line_of(text: str, at: int) -> int:
    return text.count("\n", 0, at) + 1


def gate_marks(texts: dict[str, str]) -> list[str]:
    misses = []
    for name, text in texts.items():
        for m in re.finditer(r"\\claimmark\{([A-Za-z]+)\}", text):
            if m.group(1).lower() not in MARKS:
                misses.append(f"{name}:{line_of(text, m.start())}: a mark outside the key: {m.group(0)}")
        for m in re.finditer(r"\\fence\{([A-Za-z]+)\}", text):
            if m.group(1).lower() not in FENCES:
                misses.append(
                    f"{name}:{line_of(text, m.start())}: a fence outside the key: {m.group(0)}"
                )
        if name == "main.tex":
            for m in re.finditer(r"\\claimmark\{(derived|theorem)\}", text):
                around = enclosing_parenthesis(text, m.start())
                if "\\fence{" not in around:
                    misses.append(
                        f"{name}:{line_of(text, m.start())}: {m.group(0)} with no fence beside it: {around[:90]!r}"
                    )
    return misses


def gate_stale(texts: dict[str, str]) -> list[str]:
    misses = []
    for name, text in texts.items():
        for phrase, finding in STALE:
            for m in re.finditer(re.escape(phrase), text):
                line_start = text.rfind("\n", 0, m.start()) + 1
                line_end = text.find("\n", m.end())
                line = text[line_start : line_end if line_end > 0 else len(text)]
                if any(allowed in line for allowed in STALE_ALLOWED.get(phrase, [])):
                    continue
                misses.append(
                    f"{name}:{line_of(text, m.start())}: the struck phrase {phrase!r} ({finding})"
                )
    return misses


def gate_twins(texts: dict[str, str]) -> list[str]:
    misses = []
    for label, places in TWINS:
        for name, fragment in places:
            if fragment not in texts[name]:
                misses.append(f"{name}: {label}: the fragment is not printed: {fragment!r}")
    return misses


def gate_scripts(texts: dict[str, str]) -> list[str]:
    """The derived and computed marks of the main text that name no derivation script (the Boss's rule of 2026-10-04,
    #1793 comment 5975147735): a ratchet, the count may only fall; it reaches 0 with part 4's map of marks to scripts."""
    misses = []
    text = texts["main.tex"]
    for m in re.finditer(r"\\claimmark\{(derived|computed)\}", text):
        around = enclosing_parenthesis(text, m.start())
        if not re.search(r"\\texttt\{[a-z_]+\\?_?[a-z_]*\.py\}", around):
            misses.append(f"main.tex:{line_of(text, m.start())}: {m.group(0)} names no script")
    return misses


def main() -> int:
    texts = {name: path.read_text(encoding="utf-8") for name, path in FILES.items()}
    report = []
    for gate, run in (
        ("the marks", gate_marks),
        ("the stale phrases", gate_stale),
        ("the twins", gate_twins),
    ):
        misses = run(texts)
        print(f"{gate}: {len(misses)} miss{'es' if len(misses) != 1 else ''}")
        for miss in misses:
            print("  " + miss)
        report.extend(misses)
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(main())
