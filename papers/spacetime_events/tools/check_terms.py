"""The paper's defined terms: each term in TERMS (maintained by hand: the term, how it is used, the words that define it) is defined in the body, and its first use in the body comes no earlier than the line that defines it. The Abstract is excepted, since it may use a term with its gloss; the figure's and the table's captions are excepted too, since they are read with the figure. Fails when a term is never defined or is used before its definition. Usage: python3 -I check_terms.py."""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import read_tex, strip_comments

# (term, the regex of its use, the regex of its definition)
TERMS = [
    ("Node", r"\bNodes?\b", r"a grid of sites called Nodes"),
    ("tick", r"\bticks?\b", r"what every Node does at each tick, the board's one beat"),
    ("board", r"\bboards?\b", r"on a board, a grid of sites called Nodes"),
    ("neighbour", r"\bneighbours?\b", r"six neighbours \(front and back, left and right, up and down\)"),
    ("step", r"\bsteps?\b", r"adds three things beside the step, what every Node does at each tick"),
    ("now", r"\bnow\b", r"three whole numbers for each of light and matter: now, before, and the remainder"),
    ("before", r"\bbefore\b", r"three whole numbers for each of light and matter: now, before, and the remainder"),
    ("next", r"next (number|plus)|\\mathrm\{next\}", r"keeping the quotient as its next number"),
    ("remainder", r"\bremainders?\b", r"the remainder \(what is left over from the division\)"),
    ("piece", r"\bpieces?\b(?! of particle decay)", r"one whole piece, the smallest amount a detector can take"),  # "one small piece of particle decay aside" in the opening is the everyday word, not the term
    ("detector", r"\bdetectors?\b", r"a detector we place, one Node or a few with a record"),
    ("record", r"(?<!runs back with its )\brecords?\b", r"one Node or a few with a record, clicks \(takes something from the numbers and records it\)"),  # "the toss runs back with its record" in the opening is the toss's own record of its draws, the everyday word, not the detector's
    ("books", r"\bbooks\b", r"the detector's books, the count it keeps of pieces"),
    ("click", r"\bclick(s|ed)?\b", r"clicks \(takes something from the numbers and records it\)"),
    ("toss", r"\btoss(es)?\b", r"a toss, which is a weighted draw"),
    ("weight", r"\bweights?\b", r"reads the six numbers its neighbours hold now, each with a fixed weight"),
    ("chance", r"\bchances?\b", r"chance \$P_i\$ is its weight over the sum"),
    ("wiping", r"\bwip(ing|es|ed)\b", r"a wiping, which overwrites numbers"),
    ("ball", r"\bball\b", r"a ball counted in steps"),
    ("tube", r"\btube\b", r"a tube, a board whose sides hold zero"),
    ("swing", r"\bswings?\b", r"a swing being the numbers' going up, down and back"),
    ("clock", r"\bclocks?\b", r"A body's clock is how many swings it completes in so many ticks"),
    ("the Node's rate", r"\brate\b(?! and a length)", r"that sets the Node's rate"),
    ("turn", r"\b(a|the|its|that|of) turn\b|\bturn rate", r"is the detector's turn, an angle measured as a part of one full swing"),
    ("pair", r"\bpairs?\b", r"A kind of pattern is chosen by two whole numbers, a top and a bottom number"),
    ("content", r"\bcontents?\b", r"has a content at the Node, a count of units held there"),
    ("symmetry", r"\bsymmetr(y|ies)\b", r"turnings and mirror images that leave the cube as it was form the cube's symmetry group"),
    # the algebra's standard terms, allowed since the owner's rule of round 5c, each explained at its first use; absent from the paper, they are skipped
    ("Wronskian", r"\bWronskians?\b", r"a cross-difference of the kind called a Wronskian", True),
    ("group", r"\bgroups?\b", r"form the cube's symmetry group, of order 48, the order being how many it holds", True),
    ("scalar", r"\bscalars?\b", r"are scalars, unchanged by every symmetry", True),
    ("vector", r"\bvectors?\b", r"are vectors, turning with the axes", True),
    ("invariant", r"\binvariants?\b", r"invariant of second degree, a number every symmetry leaves as it is", True),
    ("commutes", r"\bcommutes?\b", r"the step commutes with the group, remainders included: a symmetry then a step is a step then that symmetry", True),
    ("tie", r"\bties?\b", r"we say they are tied; on the board nothing carries the tie\. The tie is the count's conservation"),
    ("crest", r"\bcrests?\b", r"many Nodes from one highest number to the next \(crest to crest\)"),
]


def main() -> int:
    lines = strip_comments(read_tex()).splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("\\section{"))
    end = next(i for i, l in enumerate(lines) if l.startswith("\\section*{Statements"))
    t0 = next((i for i in range(start, end) if "\\label{tab:symbols}" in lines[i]), None)
    t1 = next((i for i in range(t0, end) if lines[i].startswith("\\end{table}")), None) if t0 is not None else None
    body = [(i + 1, re.sub(r"\\caption\{.*\}", "", lines[i])) for i in range(start, end) if t0 is None or not (t0 <= i <= t1)]  # the table of symbols collects the terms; it is skipped
    problems = []
    print(f"{'term':16} {'defined':>8} {'first use':>10}")
    for entry in TERMS:
        term, use, definition = entry[:3]
        optional = len(entry) > 3 and entry[3]
        defs = [n for n, l in body if re.search(definition, l)]
        uses = [n for n, l in body if re.search(use, l, flags=re.I)]
        d = defs[0] if defs else None
        u = uses[0] if uses else None
        if optional and u is None and d is None:
            print(f"{term:16} {'absent':>8} {'skipped':>10}")
            continue
        print(f"{term:16} {str(d):>8} {str(u):>10}")
        if d is None:
            problems.append(f"'{term}' is never defined")
        elif u is not None and u < d:
            problems.append(f"'{term}' is used on line {u} before its definition on line {d}")
    if problems:
        print("the terms FAIL: " + "; ".join(problems))
        return 1
    print("the terms pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
