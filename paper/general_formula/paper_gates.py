"""The paper's mechanical gates (the advisor's proposal of 2026-10-04, #1793 comment 5974878000; the owner's word
"examine it and see how it can enter now"): run on main.tex and supplement.tex, each gate prints its misses and the
script exits non-zero on any.

1. The marks: every \\claimmark carries one of the key's words of Section 1 (theorem, derived, computed, assumption,
   hypothesis, experiment, fitted, inspiration) and every \\fence one of its two fences (clicks, lattice); a derived
   or theorem mark stands beside a fence inside its own parenthesis (R191 (g)).
2. The stale phrases: the words tonight's prints struck (R162 to R196, W1 to W29) stand nowhere; a hand adds a phrase
   to the list when a print strikes it, and the gate keeps it struck.
3. The second places: a number or a word that one print changed in one place and not in its twin (R180's column,
   R61's convention, W4's count, W1's intervals): each pair asserted equal where both documents print it.

4. The derivations' Inputs graph: no cycle among the supplement's Inputs lines beyond the ones named in
   claims_table.KNOWN_CYCLES, a set that may only shrink (the owner's question of 2026-10-04 on circularity).
5. The bare board: the lattice is named by its one noun; a bare "board" or the implementation's old "GameBoard"
   stands only inside a cited document's title (the owner's question of 2026-10-04 on two names for one thing).
6. The nomenclature: every letter that stands in math mode in either document has its row in the paper's
   Nomenclature table (the rows written \nom{symbols}{senses}), the table naming each of its senses; a letter the
   table does not hold is a miss (the owner's word of 2026-10-05: the symbols' cleanliness made mechanical).
7. The units and the abbreviations: a bare number in a parenthesis after a named quantity (the swing, the floor, a
   width) carries its unit word, and every abbreviation of ABBREVIATIONS is expanded in the same document at or
   before its first use (the venue's rule; the organisations' and the missions' names are not abbreviations).
9. The pointers: every \\ref has its \\label, an equation label is cited by \\eqref and no other;
   every literal pointer of the supplement, the captions and the README (Section n.m, Eq. (n), Fig. n, Table n,
   Theorem n, S.n) names a number the paper has, counted from main.tex's source order; every \\cite key has its
   \\bibitem in the same document, every \\bibitem is cited, none is doubled and the list stands in the order of first citation (the venue's numbered style).
10. The captions and the names: no caption ends with punctuation (the venue's rule), and no reference stands as an
    author-year parenthesis outside \\cite (the supplement self-contained with its own list).
8. The team's idioms: the words of the team's own work (the reference asides, the archive's gate documentation, the
   hands' names, the ledger's row numbers, the comment ids) stand nowhere in the paper (STALE, the fourth sweep).

    python paper/general_formula/paper_gates.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = {"main.tex": HERE / "main.tex", "supplement.tex": HERE / "supplement.tex"}
sys.path.insert(0, str(HERE))
# the derivations' Inputs graph (check 7 of 2026-10-04) lives beside the claims table
from claims_table import gate_inputs_graph  # noqa: E402

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
FENCES = {"clicks", "lattice"}

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
    ("No body stands within rounding", "(16), the hands' 5975194901 and 5975225540"),
    ("no body stands within rounding", "(16), the hands' 5975194901 and 5975225540"),
    ("the hole raising the light's share", "the re-pin at d00aa9e2 (the Boss's 5975843075)"),
    ("suspended until its fix", "the re-pin at d00aa9e2"),
    ("the paper's reference", "the fourth sweep's editor"),
    ("gate documentation", "the fourth sweep's editor"),
    ("claims S.", "the fourth sweep's editor"),
    ("is history", "the fourth sweep's editor"),
    ("round item", "the team's idiom"),
    ("the Boss", "the team's idiom"),
    ("the advisor", "the team's idiom"),
    ("the mathematician", "the team's idiom"),
    ("the experimenter", "the team's idiom"),
]
# the history forms the paper may not carry undated (R228): each dated to the pinned commit or struck; the engine's
# "level at now" stands, so "now" is listed in its verb-led forms alone
STALE_PATTERNS = [
    (r"\bpending\b", "R228"),
    (r"\bnot yet\b", "R228"),
    (r"\byet\b", "R228"),
    (r"\bearlier versions?\b", "R228"),
    (r"\buntil then\b", "R228"),
    (r"\bnow (refuses|stands|reads|holds|carries|gives|writes|lays|runs)\b|\blaid now\b", "R228"),
    (r"\bearlier (review|reading|finding|lay|version)\b", "R228, the supplement's side"),
    (
        r"\bno longer\b|\bsince replaced\b|\buntil read\b|\bas before\b|\bnot settled\b|\bstood open\b",
        "R228, the supplement's side",
    ),
    (r"on \\texttt\{main\}", "R228, the supplement's side (the pinned commit, not the branch)"),
    (r"\bcomment \d{6,}\b", "the team's idiom (a comment id)"),
    (r"\bR\d{3}\b", "the team's idiom (a ledger row)"),
]
# a struck phrase allowed in one named sentence, by a fragment of that sentence
STALE_ALLOWED = {
    r"\bR\d{3}\b": ["Physical Review A 47, R747"],
    "never one Node": [
        "A NodeDetector with Nodes alone is one connected region of two Nodes or more declared in the file, never one Node"
    ],
}

# a number or a word printed in two places: every fragment must be found in the named file
TWINS = [
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
            (
                "main.tex",
                "$284.7$ units of $\\Wc$ through the screen in the physical labels ($284.5$ in the implementation's labels",
            ),
            ("main.tex", "$N = 284.50$ in the implementation's labels"),
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
    ("the draw's bound", [("main.tex", "$1.1 \\times 10^{-19}$ at the width $63$")]),
    (
        "Compton's factor at the computed pair",
        [
            ("main.tex", "$0.752$ at $[2, 3]$ exactly and $1$ at nature's gap"),
            ("supplement.tex", "$0.752$ at $[2, 3]$ and $1$ at nature's gap"),
        ],
    ),
    (
        "the wall of a massless family",
        [
            ("main.tex", "a massless field's quantum $\\Wc$ itself"),
            ("supplement.tex", "$3\\,\\den\\,T$ for a massless family"),
        ],
    ),
    ("Delta = 1/m*", [("main.tex", "$\\Delta = 1 / m^*$")]),
    (
        "the two slits at the fixed lay",
        [
            (
                "main.tex",
                "$N = 285$ in the region's unit $\\Wc$ at both seeds ($674$ photons of energy $T\\sin\\omega$ at $\\omega = 0.4366$",
            ),
            ("supplement.tex", "the run $N = 285$ at both seeds within the integer step's walk"),
            ("main.tex", "The run gives $N = 285$ at both seeds"),
        ],
    ),
    ("the one run", [("main.tex", "The one run this paper reports is the two slits'")]),
    (
        "the pins",
        [
            (
                "main.tex",
                "the commit 1fe3790a of 2026-10-05, the commit the two slits ran at",
            ),
            (
                "supplement.tex",
                "the commit 1fe3790a of 2026-10-05, the commit the two slits ran at",
            ),
        ],
    ),
    ("the gate on the one file", [("main.tex", "returns every array bit for bit over $40$ intervals")]),
    (
        "the walk and not a bound",
        [
            ("main.tex", "stands within that walk of the line's $284.7$"),
            ("supplement.tex", "the run $N = 285$ at both seeds within the integer step's walk"),
        ],
    ),
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
        struck = [(re.escape(p), p, f) for p, f in STALE] + [(p, p, f) for p, f in STALE_PATTERNS]
        for pattern, phrase, finding in struck:
            for m in re.finditer(pattern, text):
                line_start = text.rfind("\n", 0, m.start()) + 1
                line_end = text.find("\n", m.end())
                line = text[line_start : line_end if line_end > 0 else len(text)]
                if any(allowed in line for allowed in STALE_ALLOWED.get(phrase, [])):
                    continue
                misses.append(
                    f"{name}:{line_of(text, m.start())}: the struck phrase {m.group(0)!r} ({finding})"
                )
    return misses


def gate_twins(texts: dict[str, str]) -> list[str]:
    misses = []
    for label, places in TWINS:
        for name, fragment in places:
            if fragment not in texts[name]:
                misses.append(f"{name}: {label}: the fragment is not printed: {fragment!r}")
    return misses


BOARD = re.compile(r"\b(?:Game)?[Bb]oard('s)?\b")


def gate_board(texts: dict[str, str]) -> list[str]:
    """The misses: a bare "board" or "GameBoard" for the lattice outside a cited document title (the paper's one noun)."""
    misses = []
    for name, text in texts.items():
        for match in BOARD.finditer(text):
            before = text[: match.start()]
            opened = before.rfind("\\cite[")
            if opened >= 0 and "]" not in before[opened:]:
                continue
            misses.append(
                f"{name}: a bare 'board' or 'GameBoard' at line {line_of(text, match.start())}: {text[max(0, match.start() - 40) : match.end() + 20]!r}"
            )
    return misses


# 6. the nomenclature: the letters of math mode against the table's rows
GREEK = (
    r"alpha|beta|gamma|Gamma|delta|Delta|epsilon|varepsilon|zeta|eta|theta|Theta|vartheta|iota|kappa|lambda|Lambda|mu"
    r"|nu|xi|Xi|pi|Pi|rho|sigma|Sigma|tau|upsilon|phi|Phi|varphi|chi|psi|Psi|omega|Omega|ell|hbar|nabla"
)
MATH_WORDS = (
    r"sin|cos|tan|cot|ln|log|exp|sqrt|sum|int|prod|frac|tfrac|dfrac|left|right|bigl|bigr|Bigl|Bigr|biggl|biggr|big|Big"
    r"|cdot|cdots|ldots|dots|times|pm|mp|le|ge|ne|approx|propto|to|infty|partial|quad|qquad|ddiv|dmod|num|den|Wc|bM|bD|bK"
    r"|operatorname|mathrm|text|textsc|textit|mathit|arccos|arcsin|arctan|asinh|max|min|langle|rangle|lfloor|rfloor"
    r"|lceil|rceil|prime|boxed|displaystyle|scriptstyle|textstyle|limits|nolimits|setminus|cup|cap|in|notin|subset"
    r"|forall|exists|equiv|sim|simeq|cong|ll|gg|neq|leq|geq|mapsto|rightarrow|leftarrow|Rightarrow|Leftarrow"
    r"|leftrightarrow|circ|star|ast|dagger|vert|Vert|lvert|rvert|mid|colon|mathbf|mathcal|boldsymbol|bar|hat|tilde"
    r"|vec|dot|ddot|overline|underline|label|ref|eqref|cite|texttt|mbox|hspace|vspace|nonumber|tag|phantom"
)
MATH_ENVIRONMENTS = (
    r"\\\[(.*?)\\\]|\\begin\{(equation\*?|align\*?|aligned|gather\*?|multline\*?)\}(.*?)\\end\{\2\}"
)


def math_segments(text: str) -> list[tuple[int, str]]:
    """Every piece of math mode with the offset of its start: the displayed environments, then the inline $...$."""
    text = re.sub(r"(?<!\\)%.*", "", text)
    body_end = text.find("\\begin{thebibliography}")
    if body_end > 0:
        text = text[:body_end]
    segments = [
        (m.start(), m.group(1) or m.group(3)) for m in re.finditer(MATH_ENVIRONMENTS, text, re.S)
    ]
    inline = re.sub(MATH_ENVIRONMENTS, " ", text, flags=re.S)
    segments.extend((m.start(), m.group(1)) for m in re.finditer(r"(?<!\\)\$([^$]+)\$", inline))
    return segments


def math_letters(segment: str) -> list[str]:
    """The letters of one piece of math: a Latin letter standing alone, or a Greek macro; words, operators and
    the text macros' arguments are not letters."""
    s = re.sub(
        r"\\(text|mathrm|textsc|textsf|textit|mathit|operatorname|texttt|mbox|label|ref|eqref|cite)\{[^{}]*\}",
        " ",
        segment,
    )
    s = re.sub(r"\\(" + MATH_WORDS + r")\b", " ", s)
    letters = []
    for m in re.finditer(r"\\(" + GREEK + r")\b|(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", s):
        letters.append("\\" + m.group(1) if m.group(1) else m.group(2))
    return letters


def nomenclature_letters(text: str) -> set[str]:
    """The letters the Nomenclature table's rows name, each row \\nom{symbols}{senses}."""
    named: set[str] = set()
    for m in re.finditer(r"\\nom\{((?:[^{}]|\{[^{}]*\})*)\}\{", text):
        for _, segment in math_segments(m.group(1) + " "):
            named.update(math_letters(segment))
    return named


def gate_nomenclature(texts: dict[str, str]) -> list[str]:
    """The misses: a letter in math mode, in either document, with no row in the Nomenclature table of either document."""
    named = set()
    for text in texts.values():
        named |= set(nomenclature_letters(text))
    if not named:
        return [
            "main.tex, supplement.tex: no Nomenclature row (\\nom{symbols}{senses}) found in either document"
        ]
    misses = []
    for name, text in texts.items():
        seen: dict[str, int] = {}
        for offset, segment in math_segments(text):
            for letter in math_letters(segment):
                if letter not in named:
                    seen.setdefault(letter, line_of(text, offset))
        for letter, line in sorted(seen.items(), key=lambda kv: kv[1]):
            misses.append(f"{name}:{line}: the letter {letter} has no row in the Nomenclature table")
    return misses


# 7. the units and the abbreviations
QUANTITY_WORDS = (
    r"swing|floor|kick|content|defect|depth|width|range|reach|span|lifetime|period|duration|wavelength|spacing|margin"
    r"|ceiling|dip|gap|binding|well|rest"
)
BARE_NUMBER = re.compile(
    r"\b("
    + QUANTITY_WORDS
    + r")\b([^.;()\n]{0,60})\((\$?[-+]?\d[\d,.{}]*\$?(?:\s*(?:to|and|or|,)\s*\$?[\d,.{}]+\$?)*)\)"
)
NOT_A_QUANTITY = re.compile(r"postulate|item|row|step|line|Table|Fig|Section|S\.|Eq|column|part|\(\w\)")
# (the abbreviation as it is printed, the words that expand it); each expanded in the same document at or before
# its first use, within the sentence allowed; the organisations' and missions' names (LIGO, MAGIC, LHAASO, SLAC, HERA,
# CODATA, MICROSCOPE, INTEGRAL, ORCID, MIT, DOI) are names and not listed
ABBREVIATIONS = [
    (r"\\Lambda\$CDM|\\Lambda\\mathrm\{CDM\}", r"cold dark matter"),
    (r"\brms\b|\\mathrm\{rms\}", r"root-mean-square"),
    (r"\bGRB\b", r"gamma-ray burst"),
    (r"\ba\.u\.", r"atomic units"),
    (r"\bHa\b", r"hartree"),
    (r"Fermi-LAT", r"Large Area Telescope"),
    (r"\bEHT\b", r"Event Horizon Telescope"),
    (r"\bGHZ\b", r"Greenberger-Horne-Zeilinger"),
    (r"\bCHSH\b", r"Clauser"),
    (r"\bPPN\b", r"parametri[sz]ed post-Newtonian"),
    (r"G_F\b", r"Fermi constant"),
    (r"E_\{\\mathrm\{QG\}", r"quantum-gravity \(QG\) scale|Lorentz-violation scale"),
    (r"_\{\\mathrm\{GW\}\}|\bGW\b(?!\d)", r"gravitational wave"),
    (r"_\{\\mathrm\{EM\}\}|\bEM\b", r"electromagnetic"),
    (r"\bGR\b", r"general relativity"),
    (r"\bQED\b", r"quantum electrodynamics"),
]
SENTENCE_REACH = 300


def gate_units(texts: dict[str, str]) -> list[str]:
    misses = []
    for name, text in texts.items():
        body_end = text.find("\\begin{thebibliography}")
        body = text[:body_end] if body_end > 0 else text
        for m in BARE_NUMBER.finditer(body):
            if NOT_A_QUANTITY.search(m.group(2)):
                continue
            misses.append(
                f"{name}:{line_of(body, m.start())}: a bare number with no unit word after '{m.group(1)}': {m.group(0)[-80:]!r}"
            )
        for abbreviation, expansion in ABBREVIATIONS:
            first = re.search(abbreviation, body)
            if not first:
                continue
            expanded = re.search(expansion, body, re.I)
            if expanded is None or expanded.start() > first.start() + SENTENCE_REACH:
                misses.append(
                    f"{name}:{line_of(body, first.start())}: the abbreviation {first.group(0)!r} is not expanded at or before its first use"
                )
    return misses


# 9. the pointers
def numbering(main: str) -> dict[str, int]:
    """The counts the paper's numbering reaches, from main.tex's source order: sections with their subsections,
    numbered equations, figures, tables, theorems, propositions."""
    body_end = main.find("\\begin{thebibliography}")
    body = main[:body_end] if body_end > 0 else main
    body = re.sub(r"(?<!\\)%.*", "", body)
    counts: dict[str, int] = {
        "equation": 0,
        "figure": 0,
        "table": 0,
        "theorem": 0,
        "proposition": 0,
        "section": 0,
    }
    subsections: dict[int, int] = {}
    for m in re.finditer(
        r"\\(section|subsection)\{|\\begin\{(equation|figure|table|theorem|proposition)\}", body
    ):
        if m.group(1) == "section":
            counts["section"] += 1
            subsections[counts["section"]] = 0
        elif m.group(1) == "subsection":
            subsections[counts["section"]] = subsections.get(counts["section"], 0) + 1
        else:
            counts[m.group(2)] += 1
    counts["subsections"] = subsections  # type: ignore[assignment]
    return counts


LITERAL_POINTERS = [
    (r"Section~?(\d+)\.(\d+)", "subsection"),
    (r"Section~?(\d+)(?![.\d])", "section"),
    (r"Eq\.~?\((\d+)\)", "equation"),
    (r"Eqs\.~?\((\d+)\)", "equation"),
    (r"Fig\.~?(\d+)", "figure"),
    (r"Figs\.~?(\d+)", "figure"),
    (r"Table~?(\d+)", "table"),
    (r"Tables~?(\d+)", "table"),
    (r"Theorem~?(\d+)", "theorem"),
    (r"Proposition~?(\d+)", "proposition"),
]


# the long version of the paper at the tag paper-long-v1.1 numbers its derivations S.1 to S.65; a pointer the text cites
# "of the long version" (or after "the long version's", or before "at its tag") names that document, not the supplement
LONG_VERSION_DERIVATIONS = 65


def cited_of_the_long_version(text: str, m: re.Match) -> bool:
    before = text[max(0, m.start() - 70) : m.start()]
    after = text[m.end() : m.end() + 45]
    return "long version" in before or "long version" in after or "at its tag" in after


def gate_pointers(texts: dict[str, str]) -> list[str]:
    misses = []
    counts = numbering(texts["main.tex"])
    derivations = len(re.findall(r"\\begin\{derivation\}", texts["supplement.tex"]))
    for name, text in texts.items():
        body_end = text.find("\\begin{thebibliography}")
        body = text[:body_end] if body_end > 0 else text
        labels = re.findall(r"\\label\{([^}]*)\}", text)
        for label in sorted({label for label in labels if labels.count(label) > 1}):
            misses.append(f"{name}: the label {label!r} is defined twice")
        refs = re.findall(r"\\(eqref|ref)\{([^}]*)\}", text)
        for kind, label in refs:
            if label not in labels:
                misses.append(f"{name}: \\{kind}{{{label}}} has no label")
            elif (kind == "eqref") != label.startswith("eq:"):
                misses.append(f"{name}: \\{kind}{{{label}}} cites a label of the other kind")
        # the literal pointers (the supplement's, the captions' and the README's words; main's own \ref are above)
        literal_text = body if name != "main.tex" else "\n".join(re.findall(r"\\caption\{.*", body))
        for pattern, kind in LITERAL_POINTERS:
            for m in re.finditer(pattern, literal_text):
                if cited_of_the_long_version(literal_text, m):
                    continue
                if kind == "subsection":
                    section, sub = int(m.group(1)), int(m.group(2))
                    if (
                        section not in counts["subsections"]
                        or sub > counts["subsections"][section]
                        or sub == 0
                    ):
                        misses.append(
                            f"{name}: the pointer {m.group(0)!r} names a subsection the paper has not"
                        )
                else:
                    n = int(m.group(1))
                    if n == 0 or n > counts[kind]:
                        misses.append(
                            f"{name}: the pointer {m.group(0)!r} names a {kind} the paper has not"
                        )
        for m in re.finditer(r"\bS\.(\d+)\b", body):
            n = int(m.group(1))
            if cited_of_the_long_version(body, m):
                if n == 0 or n > LONG_VERSION_DERIVATIONS:
                    misses.append(
                        f"{name}:{line_of(body, m.start())}: the pointer {m.group(0)!r} of the long version names a "
                        f"derivation the tag has not (S.1 to S.{LONG_VERSION_DERIVATIONS})"
                    )
                continue
            if n == 0 or n > derivations:
                misses.append(
                    f"{name}:{line_of(body, m.start())}: the pointer {m.group(0)!r} names a derivation the supplement has not"
                )
        # the citations against the document's own bibliography
        cites = set()
        for m in re.finditer(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}", text):
            cites.update(k.strip() for k in m.group(1).split(","))
        bibitems = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", text)
        for key in sorted(cites - set(bibitems)):
            misses.append(f"{name}: \\cite{{{key}}} has no bibitem in this document")
        for key in sorted(set(bibitems) - cites):
            misses.append(f"{name}: the bibitem {key!r} is never cited")
        for key in sorted({b for b in bibitems if bibitems.count(b) > 1}):
            misses.append(f"{name}: the bibitem {key!r} is doubled")
        first_cited: list[str] = []
        for m in re.finditer(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}", body):
            for key in (k.strip() for k in m.group(1).split(",")):
                if key not in first_cited:
                    first_cited.append(key)
        if [b for b in bibitems if b in first_cited] != first_cited:
            misses.append(
                f"{name}: the bibliography is not in the order of first citation (the venue's numbered style)"
            )
    return misses


# 10. the captions and the names: a caption ends with no punctuation (the venue's rule); a reference is a \cite,
# never an author-year parenthesis
CAPTION = re.compile(r"\\caption\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}")
AUTHOR_YEAR = re.compile(
    r"\((?:[A-Z][A-Za-z'\-]+(?:,? (?:and )?[A-Z][A-Za-z'\-]+)*,? (?:19|20)\d\d[^)]{0,60})\)"
)


def gate_captions(texts: dict[str, str]) -> list[str]:
    misses = []
    for name, text in texts.items():
        body_end = text.find("\\begin{thebibliography}")
        body = text[:body_end] if body_end > 0 else text
        for m in CAPTION.finditer(body):
            if m.group(1).rstrip().endswith((".", ",", ";", ":")):
                misses.append(
                    f"{name}:{line_of(body, m.start())}: a caption ending with punctuation: {m.group(1)[-60:]!r}"
                )
        for m in AUTHOR_YEAR.finditer(body):
            misses.append(
                f"{name}:{line_of(body, m.start())}: an author-year reference outside \\cite: {m.group(0)!r}"
            )
    return misses


def gate_scripts(texts: dict[str, str]) -> list[str]:
    """The derived and computed marks of the main text that name no derivation script (the Boss's rule of 2026-10-04,
    #1793 comment 5975147735): a ratchet, the count may only fall; it reaches 0 with part 4's map of marks to scripts."""
    misses = []
    text = texts["main.tex"]
    for m in re.finditer(r"\\claimmark\{(derived|computed)\}", text):
        around = enclosing_parenthesis(text, m.start())
        if not re.search(r"\\texttt\{(?:[a-z0-9]+(?:\\_)?)+\.py\}", around):
            misses.append(f"main.tex:{line_of(text, m.start())}: {m.group(0)} names no script")
    return misses


def main() -> int:
    texts = {name: path.read_text(encoding="utf-8") for name, path in FILES.items()}
    report = []
    for gate, run in (
        ("the marks", gate_marks),
        ("the stale phrases", gate_stale),
        ("the twins", gate_twins),
        ("the derivations' Inputs graph", lambda texts: gate_inputs_graph(texts["supplement.tex"])),
        ("the bare board", gate_board),
        ("the nomenclature", gate_nomenclature),
        ("the units and the abbreviations", gate_units),
        ("the pointers", gate_pointers),
        ("the captions and the names", gate_captions),
    ):
        misses = run(texts)
        print(f"{gate}: {len(misses)} miss{'es' if len(misses) != 1 else ''}")
        for miss in misses:
            print("  " + miss)
        report.extend(misses)
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(main())
