"""Split the Supplementary Material out of the manuscript (the owner's word of
2026-09-23, "48 pages", the form he approved on 01:40Z: the paper as one
document, the records that a reader needs only to reproduce or to audit in a
supplement generated from the same source).

`split(s)` takes the reordered manuscript text (before the references are
filtered) and returns `(paper, supplement_body)`: the six blocks below are
cut whole from the paper, each replaced by a one-line pointer, and the
paper's references to them are rewritten to the supplement's numbers, S1 to
S6 for its sections and S1 to S3 for its tables. The supplement resolves
its own references to the paper's labels through the `xr` package, so it is
compiled after the paper in the same directory. Nothing is rewritten beyond
the pointers; every block stands verbatim in the supplement.
"""

import re

from reorder import REGISTER_HEADING, ROADS_HEADING

BIB_START = "\\begin{thebibliography}"
PROOFS_HEADING = "\\section{Auxiliary proofs}\\label{app:proofs}"
TECHNICAL_HEADING = "\\section{Technical details}\\label{app:technical}"
SYMBOLS_START = "\\paragraph{The symbols.} {\\footnotesize"
LONGTABLE_END = "\\end{longtable}}"
CONFIRMATIONS_START = "\\paragraph{The seven confirmations.}"
HANDWORKED_START = "\\paragraph{A hand-worked update.}"
CODE_HEADING = "\\paragraph{The code implements the law.}"

SUPPLEMENT = "the Supplementary Material"

# The pointers left in the paper where a block stood.
POINTERS = {
    "confirmations": (
        "\\paragraph{The seven confirmations.} Each a run's clicks against the formula shown Inside, "
        "listed with its numbers in S3 of " + SUPPLEMENT + ".\n\n"
    ),
    "symbols": (
        "\\paragraph{The symbols.} The symbol table, every letter with its kind and its name, is Table~S3 of "
        + SUPPLEMENT
        + ".\n\n"
    ),
    "handworked": (
        "\\paragraph{A hand-worked update, and the code.} One row's update worked by hand, interval by "
        "interval, and the engine's realisation of Eq.~\\eqref{eq:map} as one pass per interval are S6 of "
        + SUPPLEMENT
        + ".\n\n"
    ),
}

# The paper's references to what moved, rewritten to the supplement's numbers.
REFERENCES = [
    ("Tables~\\ref{tab:conversion} and~\\ref{tab:nature}", "Table~\\ref{tab:conversion} and Table~S1"),
    ("Table~\\ref{tab:nature}", "Table~S1"),
    ("Table~\\ref{tab:roads}", "Table~S2"),
    ("Appendix~\\ref{app:register}", SUPPLEMENT + ", S1"),
    ("Appendix~\\ref{app:families}", SUPPLEMENT + ", S2"),
    ("Appendix~\\ref{app:reproduction}", SUPPLEMENT + ", S3"),
    ("Appendix~\\ref{app:proofs}", SUPPLEMENT + ", S5"),
    (
        "the symbol table is\nAppendix~\\ref{app:technical},",
        "the symbol table is\nTable~S3 of " + SUPPLEMENT + ",",
    ),
]


def _once(s: str, marker: str, name: str) -> int:
    n = s.count(marker)
    if n != 1:
        raise ValueError(f"supplement: the marker of {name} occurs {n} times, not once: {marker[:60]!r}")
    return s.index(marker)


def _cut_between(s: str, start: str, end: str, name: str) -> tuple[str, str]:
    """Cut from the start marker (inclusive) to the end marker (exclusive), the end the first after the start."""
    i = _once(s, start, name)
    j = s.index(end, i)
    return s[i:j], s[:i] + s[j:]


def split(s: str) -> tuple[str, str]:
    """(the paper without the six blocks, the supplement's body of six sections)."""
    # S1 the full record and S2 the check of the roads: the two last appendices.
    register, s = _cut_between(s, REGISTER_HEADING, ROADS_HEADING, "S1, the register")
    roads, s = _cut_between(s, ROADS_HEADING, BIB_START, "S2, the roads")
    # S3 the seven confirmations: the reproduction appendix's last paragraph,
    # which stood before the register's heading (cut above), so before the references now.
    confirmations, s = _cut_between(s, CONFIRMATIONS_START, BIB_START, "S3, the confirmations")
    s = s.replace(BIB_START, POINTERS["confirmations"] + BIB_START, 1)
    # S4 the symbols table.
    i = _once(s, SYMBOLS_START, "S4, the symbols")
    j = s.index(LONGTABLE_END, i) + len(LONGTABLE_END)
    symbols, s = s[i:j], s[:i] + POINTERS["symbols"] + s[j:]
    # S5 the proofs: the whole appendix, its heading included; the references
    # to it point at the supplement.
    proofs, s = _cut_between(s, PROOFS_HEADING, TECHNICAL_HEADING, "S5, the proofs")
    # S6 the hand-worked update and the code.
    handworked, s = _cut_between(s, HANDWORKED_START, CODE_HEADING, "S6, the hand-worked update")
    s = s.replace(CODE_HEADING, POINTERS["handworked"] + CODE_HEADING, 1)
    for old, new in REFERENCES:
        if old not in s:
            raise ValueError(f"supplement: the paper's reference {old!r} is not there to rewrite")
        s = s.replace(old, new)
    proofs_body = proofs[len(PROOFS_HEADING) :]
    supplement = (
        register
        + "\n\n"
        + roads
        + "\n\n\\section{Reproduction: the seven confirmations}\\label{supp:reproduction}\n\n"
        + confirmations
        + "\n\n\\section{The symbols}\\label{supp:symbols}\n\n"
        + symbols
        + "\n\n\\section{Auxiliary proofs}\\label{supp:proofs}\n"
        + proofs_body
        + "\n\\section{A hand-worked update, and the code}\\label{supp:handworked}\n\n"
        + handworked
    )
    # The supplement's references to the paper's labels carry the prefix that
    # xr-hyper imports them under (main-), so that the paper's citation labels
    # never collide with the supplement's own reference list.
    own = set(re.findall(r"\\label\{([^}]*)\}", supplement))
    supplement = re.sub(
        r"\\(eqref|ref)\{([^}]*)\}",
        lambda m: m.group(0) if m.group(2) in own else f"\\{m.group(1)}{{main-{m.group(2)}}}",
        supplement,
    )
    return s, supplement


SUPPLEMENT_HEADER = """% The Supplementary Material of the paper on the general formula: generated by
% cut30/assemble.py from the same source as main.tex (the owner's word of
% 2026-09-23, the paper at 48 pages as one document, the records in a
% supplement); edit the parts, not this file. Its cross-references to the
% paper resolve through the xr package, so it is compiled after main.tex in
% the same directory.
"""


def preamble(main_preamble: str) -> str:
    """The supplement's preamble: the paper's, with xr and the S numbering."""
    marker = "\\begin{document}"
    head = main_preamble.split(marker)[0]
    # xr-hyper, not xr, since the paper loads hyperref (loaded before it).
    head = head.replace("\\usepackage{hyperref}", "\\usepackage{xr-hyper}\n\\usepackage{hyperref}", 1)
    head = head.replace(
        "\\title{",
        "\\externaldocument[main-]{main}\n"
        "\\renewcommand{\\thesection}{S\\arabic{section}}\n"
        "\\renewcommand{\\thetable}{S\\arabic{table}}\n"
        "\\renewcommand{\\thefigure}{S\\arabic{figure}}\n"
        "\\title{Supplementary Material to: ",
        1,
    )
    return head
