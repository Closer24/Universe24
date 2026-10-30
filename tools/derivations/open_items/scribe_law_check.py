"""The keeper's check of the law (docs/ALGEBRA.md) for contradictions among its own lines, as far as a script can read them
(the owner's word of 2026-10-30, 07:5x UTC, in Hebrew, in translation: "check the laws with a script that there is no contradiction among them").

Four checks, each by a table the script holds:
  STRUCTURE   the law's form: the fixed line count, the final newline, ASCII, no tab and no trailing space; every clause (a paragraph that opens with a bold name)
              closes its bold marks, its parentheses (an interval [0, w) spared), its brackets and its double quotes; no clause name stands twice (but the generic ones);
              a heading stands alone;
  REFERENCES  every line it cites exists, a line cited beside a clause name is that clause, every anchor it links is a heading, Postulates 1 to 6 are each defined once and no Postulate 7 is cited;
  IDENTITIES  the numbers of the cube and of Rule3 that the law repeats agree (the 24 and the 48 with their mirror images, the five kinds and the squares of their sizes summing to 24, the ten slots, the six Spokes);
  PAIRS       a table of contradicting statements: a stale row of the old engine against the law of the new core that forbids it (the audit's list, SCRIBE-LAW-AUDIT-1.md, and its sequel).

A script cannot prove that no two sentences of prose disagree: it reads what its tables name. Each contradiction a reader finds enters a table and is then found at every later run.
The known list (scribe_law_check_known.json) holds the old engine's rows that stand until the re-cut (the owner's answer of 2026-10-30, 04:5x UTC); a finding beyond it refuses.

Usage: python -I scribe_law_check.py [--law PATH] [--all] [--selftest] [--write-known]
Exit 0: no finding beyond the known list; exit 1: a new finding (printed with its line); the known rows print as counts, and by line with --all."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_LAW = HERE.parent.parent.parent / "docs" / "ALGEBRA.md"
KNOWN = HERE / "scribe_law_check_known.json"
EXPECTED_LINES = 1960  # the law's fixed length (the keeper's tamper check: an edit holds its new text in its own line)
POSTULATES = 7  # the law has Postulates 1 to 7
CORE = 110  # the law's new core: the preface, the postulates and the decisions of Tensor24 stand in lines 1 to 110
GENERIC_HEADS = frozenset({"Proof", "Theorem", "Status", "Alignment", "Note", "Remark"})  # clause names that may stand more than once (and "Alignment, <date>")
HISTORY = re.compile(
    r"cancel|struck|strike|withdrawn|superseded|retired|former|no longer|old engine|out of the law|kept by name|replaced by|renamed|is not interesting|stand as its record",
    re.I,
)  # words that mark a sentence as the record of what stood, not a claim of what stands


@dataclass
class Finding:
    check: str  # the check's code, a letter and a number
    line: int  # 1-based
    text: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    informational: list[str] = field(default_factory=list)

    def add(self, check: str, line: int, text: str) -> None:
        self.findings.append(Finding(check, line, text))


# ------------------------------------------------------------------------------------------------ STRUCTURE


def head_of(line: str) -> str:
    m = re.match(r"\*\*(.+?)\*\*", line)
    return m.group(1) if m else ""


def slug(heading: str) -> str:
    """GitHub's anchor of a heading: lowercase, punctuation out but hyphens and spaces, spaces to hyphens."""
    text = heading.lstrip("#").strip().lower()
    text = re.sub(r"[^a-z0-9 _-]", "", text)
    return text.replace(" ", "-")


HALF_OPEN = re.compile(r"\[[^\[\]()]{1,50}\)|\([^\[\]()]{1,50}\]")  # an interval [0, w) or (0, w]: its bracket is no unbalanced mark


def clause_blocks(lines: list[str]) -> list[tuple[int, str]]:
    """The clauses as paragraphs: from a line that opens with a bold name to the next blank line, as (first line, joined text)."""
    blocks: list[tuple[int, str]] = []
    n = 0
    while n < len(lines):
        if lines[n].startswith("**") and head_of(lines[n]):
            m = n
            while m + 1 < len(lines) and lines[m + 1].strip():
                m += 1
            blocks.append((n + 1, "\n".join(lines[n : m + 1])))
            n = m + 1
        else:
            n += 1
    return blocks


def check_structure(lines: list[str], raw: str, report: Report, expected: int) -> None:
    if not raw.endswith("\n"):
        report.add("S1", len(lines), "the law does not end with a newline")
    if len(lines) != expected:
        report.add("S2", len(lines), f"the law has {len(lines)} lines, the fixed length is {expected}")
    for n, line in enumerate(lines, 1):
        if not line.isascii():
            report.add("S3", n, "a non-ASCII character")
        if "\t" in line or "\r" in line or line != line.rstrip():
            report.add("S4", n, "a tab, a carriage return or a trailing space")
    for n, line in enumerate(lines, 1):
        if line.startswith("#") and (len(line) > 140 or "**" in line):
            report.add("S7", n, "a heading line that carries a clause (bold marks, or longer than 140 characters): the heading stands alone")
    for n, block in clause_blocks(lines):
        flat = HALF_OPEN.sub("", block)
        if block.count("**") % 2:
            report.add("S5", n, "an odd number of bold marks in a clause")
        if flat.count("(") != flat.count(")"):
            report.add("S5", n, f"parentheses unbalanced in a clause ({flat.count('(')} against {flat.count(')')})")
        if flat.count("[") != flat.count("]"):
            report.add("S5", n, "brackets unbalanced in a clause")
        if block.count('"') % 2:
            report.add("S5", n, "an odd number of double quotes in a clause")
    seen: dict[str, int] = {}
    for n, line in enumerate(lines, 1):
        head = head_of(line)
        if not head or head.split(",")[0] in GENERIC_HEADS:
            continue
        if head in seen:
            report.add("S6", n, f"the clause name {head!r} stands again (first at line {seen[head]})")
        else:
            seen[head] = n


# ------------------------------------------------------------------------------------------------ REFERENCES

LINE_CITE = re.compile(r"\blines? (\d+(?:(?:,\s*|\s+and\s+|\s+to\s+)\d+)*)")
NAMED_CITE = re.compile(r'(?:\*\*([^*]{3,90})\*\*|"([^"]{3,90})")(?:,)?\s*\((?:the )?line (\d+)\)')


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def check_references(lines: list[str], report: Report) -> None:
    total = len(lines)
    anchors = {slug(line) for line in lines if line.startswith("#")}
    heads = {n: norm(head_of(line) or line[:90]) for n, line in enumerate(lines, 1)}
    whole = {n: norm(line) for n, line in enumerate(lines, 1)}
    for n, line in enumerate(lines, 1):
        for m in LINE_CITE.finditer(line):
            for num in re.findall(r"\d+", m.group(1)):
                if total < int(num) < 100000:  # a number of five digits or more is an id of the thread, and line 0 a line of a table
                    report.add("R1", n, f"cites line {num}, and the law has {total} lines")
        for m in NAMED_CITE.finditer(line):
            name = norm(m.group(1) or m.group(2))
            target = int(m.group(3))
            if 1 <= target <= total and name and name not in whole[target] and heads[target] not in name:
                report.add("R2", n, f"cites {name!r} at line {target}, which opens {heads[target][:60]!r}")
        for m in re.finditer(r"\]\(#([^)\s]+)\)", line):
            if m.group(1) not in anchors:
                report.add("R3", n, f"links the anchor #{m.group(1)}, which no heading gives")
        for m in re.finditer(r"\bPostulate (\d+)\b", line):
            if not 1 <= int(m.group(1)) <= POSTULATES:
                report.add("R4", n, f"cites Postulate {m.group(1)}, and the law has Postulates 1 to {POSTULATES}")
        for m in re.finditer(r"\bdecisions? (\d+)\b", line):
            if int(m.group(1)) > 43:
                report.add("R5", n, f"cites decision {m.group(1)}, and the plan's last is 43")
    for k in range(1, POSTULATES + 1):
        where = [n for n, line in enumerate(lines, 1) for _ in re.finditer(rf"\*\*Postulate {k},", line)]
        if len(where) != 1:
            report.add("R6", where[0] if where else 1, f"Postulate {k} is defined {len(where)} times, once is owed")


# ------------------------------------------------------------------------------------------------ IDENTITIES


def check_identities(lines: list[str], report: Report) -> None:
    for n, line in enumerate(lines, 1):
        for m in re.finditer(r"\bthe (\d+) are those and their (\d+) mirror images", line):
            if (m.group(1), m.group(2)) != ("48", "24"):
                report.add("I1", n, f"the 48 are those and their 24 mirror images, read as {m.group(1)} and {m.group(2)}")
        for m in re.finditer(r"\b(\d+) mirror images\b", line):
            if m.group(1) != "24":
                report.add("I1", n, f"{m.group(1)} mirror images of the cube's rotations, the law says 24")
        for m in re.finditer(r"\b(?:the )?48 (?:rotations|turns)\b", line):
            report.add("I2", n, "the 48 spoken of as rotations or turns: the 24 are the rotations, the 48 those and their mirror images")
        for m in re.finditer(r"\b(?:the )?(\d+) (?:rotations|turns) of the cube\b", line):
            if m.group(1) not in ("24", "3", "2", "4", "6", "8", "12", "1"):
                report.add("I1", n, f"{m.group(1)} rotations of the cube")
        for m in re.finditer(r"\b(\d+), (\d+), (\d+), (\d+) and (\d+) (?:hands|dials|gears|components)", line):
            dims = [int(x) for x in m.groups()]
            if sorted(dims) == [1, 1, 2, 3, 3] and sum(d * d for d in dims) != 24:
                report.add("I3", n, "the sizes of the five kinds do not square to 24")
            if len(set(dims)) > 1 and "kinds" in line[max(0, m.start() - 120) : m.start()] and sum(d * d for d in dims) != 24:
                report.add("I3", n, f"sizes {dims} of the five kinds square to {sum(d * d for d in dims)}, the law says 24")
        for m in re.finditer(r"\b(four|eight|twelve|five|seven) Spokes\b", line):
            if "Node-clock" in line[max(0, m.start() - 160) : m.end() + 160] and "six" not in line[max(0, m.start() - 60) : m.end() + 60]:
                report.add("I4", n, f"{m.group(0)!r} beside the Node-clock, whose star has six")
        for m in re.finditer(r"\b(\d+|nine|eleven|twelve) slots\b", line):
            if "metric" in line[max(0, m.start() - 160) : m.end() + 60] and m.group(1) not in ("10", "ten"):
                report.add("I5", n, f"{m.group(0)!r} of the metric: its symmetric square has ten")


# ------------------------------------------------------------------------------------------------ PAIRS


@dataclass(frozen=True)
class Pair:
    code: str
    title: str
    stale: str  # a regex: the stale statement
    law: str  # what forbids it, in words, with its place
    governed: tuple[int, str]  # (a line of the law, a regex it must still hold): the rule is live while the governing text stands


PAIRS: tuple[Pair, ...] = (
    Pair("P01", "an integer root named as a code primitive", r"largest_below|one integer root|each is one primitive named by its clause|\bisqrt\b",
         "line 100 (never a root), line 102 and decision 41: no root in the code", (100, r"never a logarithm, an exponential, a root or a float")),
    Pair("P02", "the couplings as a file's declaration", r"the pair, the couplings|a `couplings` key|couplings key",
         "decision 35: no particle, mass or coupling is declared in any file", (35, r"no particle, no mass and no coupling is declared in any file")),
    Pair("P03", "an act from outside the Node-clock", r"one act from outside the Node-clock|an act from outside the Node-clock",
         "line 92 (3) and Postulate 1: every tick the Node-clock does the operations on its six neighbours alone", (92, r"every tick after, it does the operations on its six neighbours alone")),
    Pair("P04", "the click as an act outside the reversal", r"not injective|the one act outside the reversal",
         "Postulates 2 and 4: every act a bijection with its remainder kept, the clicks included", (35, r"Postulate 4, nature is cyclic")),
    Pair("P05", "the time gear's exponential memo", r"\(1 - 1 / Gamma\)\^c|the rate's memo|p0 = Gamma \(1 -",
         "decision 41: the slot form W = the rest + c, no table and no exponential", (35, r"decision 41")),
    Pair("P06", "a refusal past a range", r"refused by name at a tension above|the singular point",
         "decision 40 (e): no table and no refusal past a range", (35, r"no refusal past a range")),
    Pair("P07", "a declaration as a status", r"Status: (?:a )?declar",
         "line 35: declared by the file is no status; declared stands for a scale or a seed alone", (35, r"declared-by-the-file is no status|no status")),
    Pair("P08", "the swap at the top", r"swap at a (?:fed )?weak maximum|the turn is the swap|trigger at the weak maximum|the swap's trigger",
         "decision 27: cancelled, there is no act at the top and the tick has four acts", (1602, r"there is no act at the top")),
    Pair("P09", "a parity rule on Gamma, T or den", r"Gamma odd|\bT even|den even",
         "K-S2: Gamma of either parity; decision 40 (h): no rule on den's parity", (110, r"Gamma of either parity")),
    Pair("P10", "real arithmetic in a reading", r"in real arithmetic|rounded once",
         "line 100: no float anywhere, the probes too", (100, r"Only whole numbers are allowed")),
    Pair("P11", "a special rule for a horizon or a frozen clock", r"BH-S1|\*\*The horizon\*\*|the frozen load|hold and restore|ends in a frozen clock",
         "the owner's word of 07:1x at line 90: no specific law for when a link lengthens, shortens or decouples; decision 40 (a): horizons included", (90, r"No special code and no specific law for a clock or a link")),
    Pair("P12", "a bound read as a clamp", r"read at 0 for the rate|read within its hold|the typed floor|a tension at or past Gamma read at the teeth",
         "line 106: every bound is a clock's carry; decision 40 (e)", (106, r"Every bound is a clock's carry|each bound it still holds")),
    Pair("P13", "the old spring D / W = 2 / Gamma", r"D / W = 2 / Gamma",
         "decisions 40 (e) and 41: the head's notch has its own slot form", (35, r"decision 41")),
)


def sentences_around(line: str, m: re.Match[str], width: int = 260) -> str:
    return line[max(0, m.start() - width) : m.end() + width]


def check_pairs(lines: list[str], report: Report) -> dict[str, list[int]]:
    found: dict[str, list[int]] = {}
    for pair in PAIRS:
        gline, gre = pair.governed
        if not (1 <= gline <= len(lines) and re.search(gre, lines[gline - 1])):
            report.informational.append(f"{pair.code} moot: the governing text of line {gline} no longer stands")
            continue
        hits: list[int] = []
        for n, line in enumerate(lines, 1):
            for m in re.finditer(pair.stale, line):
                if HISTORY.search(sentences_around(line, m)):
                    continue
                hits.append(n)
                break
        found[pair.code] = hits
        for n in hits:
            report.add(pair.code, n, f"{pair.title}, against {pair.law}")
    return found


# ------------------------------------------------------------------------------------------------ RUN


def run(lines: list[str], raw: str, expected: int = EXPECTED_LINES) -> Report:
    report = Report()
    check_structure(lines, raw, report, expected)
    check_references(lines, report)
    check_identities(lines, report)
    check_pairs(lines, report)
    return report


def load_known(path: Path = KNOWN) -> dict[str, list[int]]:
    if not path.exists():
        return {}
    return {k: sorted(v) for k, v in json.loads(path.read_text(encoding="utf-8")).items()}


def split(report: Report, known: dict[str, list[int]]) -> tuple[list[Finding], list[Finding]]:
    new, old = [], []
    for f in report.findings:
        (old if f.line in known.get(f.check, []) else new).append(f)
    return new, old


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    law = Path(argv[argv.index("--law") + 1]) if "--law" in argv else DEFAULT_LAW
    raw = law.read_bytes().decode("utf-8")
    lines = raw.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    report = run(lines, raw)
    if "--write-known" in argv:
        out: dict[str, list[int]] = {}
        for f in report.findings:
            out.setdefault(f.check, []).append(f.line)
        KNOWN.write_text(json.dumps({k: sorted(set(v)) for k, v in sorted(out.items())}, indent=1) + "\n", encoding="utf-8")
        print(f"known list written: {sum(len(set(v)) for v in out.values())} entries in {len(out)} checks")
        return 0
    known = load_known()
    new, old = split(report, known)
    by = Counter(f.check for f in old)
    core_old = Counter(f.check for f in old if f.line <= CORE)
    print(f"the law: {len(lines)} lines; the known rows (the old engine's, standing until the re-cut): {len(old)} in {len(by)} checks, of them {sum(core_old.values())} in the core (lines 1 to {CORE})")
    for code in sorted(by):
        title = next((p.title for p in PAIRS if p.code == code), code)
        print(f"  {code}: {by[code]} lines ({core_old.get(code, 0)} in the core): {title}")
        if "--all" in argv:
            print("      lines", ", ".join(str(f.line) for f in old if f.check == code))
    for text in report.informational:
        print("  note:", text)
    if new:
        print(f"NEW findings: {len(new)}")
        for f in new:
            print(f"  {f.check} line {f.line}: {f.text}")
        return 1
    print("no new finding")
    return 0


# ------------------------------------------------------------------------------------------------ SELF-TEST


def selftest() -> int:
    """Cases on small laws: a clean one, then one defect at a time; each check must fire on its defect and spare the clean law."""
    posts = [f"**Postulate {k}, x** text" for k in range(1, POSTULATES + 1)]

    def law(*extra: str, last: str | None = None) -> tuple[list[str], str]:
        body = posts[:-1] + [last if last is not None else posts[-1]] + list(extra)
        return body, "\n".join(body) + "\n"

    def long_law(replace: dict[int, str]) -> tuple[list[str], str]:
        body = [f"**Clause {n}** filler" for n in range(1, 101)]
        for k in range(1, POSTULATES + 1):
            body[k - 1] = f"**Postulate {k}, x** text"
        body[99] = "**No float anywhere** never a logarithm, an exponential, a root or a float"
        for n, text in replace.items():
            body[n - 1] = text
        return body, "\n".join(body) + "\n"

    n7 = POSTULATES
    cases: list[tuple[str, tuple[list[str], str], int, set[str]]] = [
        ("a clean small law: no finding", law(), n7, set()),
        ("a wrong line count", law(), n7 + 1, {"S2"}),
        ("no final newline", (law()[0], law()[1].rstrip("\n")), n7, {"S1"}),
        ("a non-ASCII character", law(last="**Postulate 7, x** caf\u00e9"), n7, {"S3"}),
        ("a trailing space", law(last="**Postulate 7, x** text "), n7, {"S4"}),
        ("an odd bold mark", law(last="**Postulate 7, x** a **b"), n7, {"S5"}),
        ("unbalanced parentheses", law(last="**Postulate 7, x** a (b"), n7, {"S5"}),
        ("unbalanced brackets", law(last="**Postulate 7, x** a [b"), n7, {"S5"}),
        ("an odd double quote", law(last='**Postulate 7, x** a "b'), n7, {"S5"}),
        ("a half-open interval is no unbalanced mark", law(last="**Postulate 7, x** r in [0, w) and (0, w]"), n7, set()),
        ("a clause wrapped over two lines is read whole", law(last="**Postulate 7, x** a (b\nc) d"), n7, set()),
        ("a heading that carries a clause", law("### A heading **Alignment** of text"), n7 + 1, {"S7"}),
        ("a plain heading", law("### A heading"), n7 + 1, set()),
        ("a clause name twice", law("**Postulate 1, x** again"), n7 + 1, {"S6", "R6"}),
        ("a generic name may stand twice", law("**Proof** a", "**Proof** b"), n7 + 2, set()),
        ("a cited line past the end", law(last="**Postulate 7, x** see line 99"), n7, {"R1"}),
        ("a cited line inside the law", law(last="**Postulate 7, x** see line 2"), n7, set()),
        ("a thread id after the word line is no citation", law(last="**Postulate 7, x** line 6085442608"), n7, set()),
        ("a named citation that matches", law(last='**Postulate 7, x** see "Postulate 1, x" (line 1)'), n7, set()),
        ("a named citation of a sub-clause inside the line", law(last='**Postulate 7, x** see "x" (line 1)'), n7, set()),
        ("a named citation that does not match", law(last='**Postulate 7, x** see "Postulate 9, y" (line 1)'), n7, {"R2", "R4"}),
        ("a dangling anchor", law(last="**Postulate 7, x** see [it](#nowhere)"), n7, {"R3"}),
        ("an anchor a heading gives", law("## The postulates", "see [it](#the-postulates)"), n7 + 2, set()),
        ("a Postulate 8 cited", law(last="**Postulate 7, x** and Postulate 8"), n7, {"R4"}),
        ("a decision past the plan", law(last="**Postulate 7, x** decision 44"), n7, {"R5"}),
        ("a postulate defined twice", law("a **Postulate 3, x** again"), n7 + 1, {"R6"}),
        ("the 48 and 24 right", law(last="**Postulate 7, x** the 48 are those and their 24 mirror images"), n7, set()),
        ("the 48 spoken of as rotations", law(last="**Postulate 7, x** the 48 rotations"), n7, {"I2"}),
        ("a wrong count of mirror images", law(last="**Postulate 7, x** and 48 mirror images"), n7, {"I1"}),
        ("a stale root while line 100 is absent: moot, no finding", law(last="**Postulate 7, x** largest_below(9)"), n7, set()),
        ("the clean 100-line law", long_law({}), 100, set()),
        ("a stale root against line 100", long_law({51: "**Clause 51** the unit is largest_below(9 T^2) in the code"}), 100, {"P01"}),
        ("a stale root marked as history is spared", long_law({51: "**Clause 51** the former unit largest_below(9 T^2) is struck"}), 100, set()),
        ("a stale swap at the top against decision 27", long_law({51: "**Clause 51** the swap at a weak maximum", 1602 - 1560: "**Clause 42** x"}), 100, set()),
    ]
    failed = 0
    for name, (lines, raw), expected, want in cases:
        rep = run(lines, raw, expected)
        got = {f.check for f in rep.findings}
        if got != want:
            failed += 1
            print(f"PARTED  {name}: wanted {sorted(want)}, got {sorted(got)}")
        else:
            print(f"ok      {name}")
    print(f"selftest: {len(cases)} cases, {failed} parted")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
