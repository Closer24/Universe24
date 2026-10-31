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

The same PAIRS table reads the live documents with --docs (README.md, llms.txt and docs/ARCHITECTURE.md), each pair against the law's governing line, a hit above the document's ceiling
(scribe_law_check_docs_known.json) refusing; the table grows with every contradiction a reader finds (the four readers of 2026-10-30, 08:3x UTC, added P14 to P17).

With --arch ROOT it reads the architecture document against the tree at ROOT (the Boss's head) in both directions: every path of a part's Home line and every test of its Test line must be there (the older form, a trace table under the heading "The trace table", is read as before), every module of src/tensor24, every file of tests/, every script directly under tools/ and every file of examples/tensor24 must be named by some part's Home or Test line (the owner's word of 2026-10-30, 12:1x UTC: the main reflects the architecture document exactly), and every part carries the four layers and its status.
--arch ROOT also reads the live documents' links: a file that README.md, llms.txt, CONTRIBUTING.md, CHANGELOG.md or the architecture document links or names under docs/, and a file the law links, must stand in the tree (the law's bare citations of a departed document are history and spared).
Usage: python -I scribe_law_check.py [--law PATH] [--all] [--selftest] [--write-known] [--docs] [--arch ROOT]
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
DOCS_KNOWN = HERE / "scribe_law_check_docs_known.json"
ROOT = HERE.parent.parent.parent
ARCH = ROOT / "docs" / "ARCHITECTURE.md"
DOCS = ("README.md", "llms.txt", "docs/ARCHITECTURE.md")
EXPECTED_LINES = 1962  # the law's fixed length (the keeper's tamper check: an edit holds its new text in its own line; 1,960 until the owner's law of the choice, 2026-10-31, 03:37 UTC, its own line at the end, the blank before it and the line)
POSTULATES = 7  # the law has Postulates 1 to 7
CORE = 110  # the law's new core: the preface, the postulates and the decisions of Tensor24 stand in lines 1 to 110
GENERIC_HEADS = frozenset({"Proof", "Theorem", "Status", "Alignment", "Note", "Remark"})  # clause names that may stand more than once (and "Alignment, <date>")
HISTORY = re.compile(
    r"cancel|struck|strike|withdrawn|superseded|retire|former|no longer|old engine|out of the law|kept by name|replaced by|renamed|is not interesting|stand as its record|G1b|settled|gone|went with|left the|out of the engine|bind no Node-clock|binds no Node-clock|departs from it|code departs",
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
    spare: bool = True  # a sentence marked as history is spared; False for a clause that still stands and waits on the owner's rule
    window: int = 260  # the characters each side of a match that are read for a history word


PAIRS: tuple[Pair, ...] = (
    Pair("P01", "an integer root named as a code primitive", r"largest_below|one integer root|\bisqrt\b",
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
    Pair("P09", "a parity rule on Gamma or den", r"Gamma odd|\bden even",
         "K-S2: Gamma of either parity; decision 40 (h): no rule on den's parity", (110, r"Gamma of either parity")),
    Pair("P10", "real arithmetic in a reading", r"in real arithmetic|rounded once",
         "line 100: no float anywhere, the probes too", (100, r"Only whole numbers are allowed")),
    Pair("P11", "a special rule for a horizon or a frozen clock", r"BH-S1|\*\*The horizon\*\*|the frozen load|hold and restore|ends in a frozen clock",
         "the owner's word of 07:1x at line 90: no specific law for when a link lengthens, shortens or decouples; decision 40 (a): horizons included", (90, r"No special code and no specific law for a clock or a link")),
    Pair("P12", "a bound read as a clamp", r"read at 0 for the rate|read within its hold|the typed floor|a tension at or past Gamma read at the teeth",
         "line 106: every bound is a clock's carry; decision 40 (e)", (106, r"Every bound is a clock's carry|each bound it still holds"), True, 420),
    Pair("P13", "the old spring D / W = 2 / Gamma", r"D / W = 2 / Gamma",
         "decisions 40 (e) and 41: the head's notch has its own slot form", (35, r"decision 41"), False),
    Pair("P14", "the width derived", r"The width is derived",
         "line 100: the width is a key of the universe file and the engine holds no bound", (100, r"The width is a key of the universe file")),
    Pair("P15", "a dial, a beat count or a time in the Node-clock's state", r"a rate dial and a count|5 G \+ 3\b|5 G \+ 2 T \+ 3|its dial turns|State\(a, b, r, go, rd",
         "line 92 (4): the Node-clock's act holds no round and no time; line 80: no counter of its history; the state is 4 G since G1b", (92, r"its act holds no round and no time")),
    Pair("P16", "the ruler's table", r"one table the load walks once|the ruler's tables?\b|the ruler table|Y\(c\) = rate",
         "decisions 40 (e) and 41: no table and no refusal past a range; the slot form", (35, r"decision 41")),
    Pair("P17", "the log's fire as a mask", r"log's fire as (?:its|the backward clock's) mask|fire from the log as its mask|forward log's fire",
         "Postulate 5 (no mask) and the law's clause of decisions 33 and 34: the forward carry's bit where counts are staggered", (35, r"with the forward carry's bit")),
)


def sentences_around(line: str, m: re.Match[str], width: int = 260) -> str:
    return line[max(0, m.start() - width) : m.end() + width]


def check_pairs(lines: list[str], report: Report, law: list[str] | None = None) -> dict[str, list[int]]:
    law = lines if law is None else law
    found: dict[str, list[int]] = {}
    for pair in PAIRS:
        gline, gre = pair.governed
        if not (1 <= gline <= len(law) and re.search(gre, law[gline - 1])):
            report.informational.append(f"{pair.code} moot: the governing text of line {gline} no longer stands")
            continue
        hits: list[int] = []
        for n, line in enumerate(lines, 1):
            for m in re.finditer(pair.stale, line):
                if pair.spare and HISTORY.search(sentences_around(line, m, pair.window)):
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


def scan_docs(law: list[str], paths: list[Path]) -> dict[str, dict[str, list[int]]]:
    """Per document, per pair, the lines that hold a stale statement against the law's governing line (a sentence marked as history spared)."""
    out: dict[str, dict[str, list[int]]] = {}
    for path in paths:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        rep = Report()
        found = check_pairs(lines, rep, law)
        hits = {code: ln for code, ln in found.items() if ln}
        if hits:
            out[path.name] = hits
    return out


def docs_main(law_lines: list[str], argv: list[str]) -> int:
    hits = scan_docs(law_lines, [ROOT / d for d in DOCS])
    counts = {doc: {code: len(ln) for code, ln in by.items()} for doc, by in hits.items()}
    if "--write-known" in argv:
        DOCS_KNOWN.write_text(json.dumps(counts, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"documents' ceilings written: {sum(sum(c.values()) for c in counts.values())} hits in {len(counts)} documents")
        return 0
    ceil = json.loads(DOCS_KNOWN.read_text(encoding="utf-8")) if DOCS_KNOWN.exists() else {}
    refused = 0
    for doc in sorted(counts):
        for code, n in sorted(counts[doc].items()):
            over = n > ceil.get(doc, {}).get(code, 0)
            refused += over
            title = next((p.title for p in PAIRS if p.code == code), code)
            print(f"  {doc}: {code} {n} line(s) (ceiling {ceil.get(doc, {}).get(code, 0)}): {title}{' REFUSED' if over else ''}")
            if "--all" in argv or over:
                print("      lines", ", ".join(str(x) for x in hits[doc][code]))
    print(f"the documents: {sum(sum(c.values()) for c in counts.values())} stale line(s) in {len(counts)} of {len(DOCS)} documents; {'REFUSED: above a ceiling' if refused else 'none above its ceiling'}")
    return 1 if refused else 0


def trace_rows(text: str) -> list[list[str]]:
    """The rows of the architecture document's trace table (the table under the heading "The trace table"): the cells of each row, the header and the rule left out."""
    rows: list[list[str]] = []
    inside = False
    for line in text.split("\n"):
        if line.startswith("## "):
            inside = line.strip() == "## The trace table"
            continue
        if inside and line.startswith("|") and not line.startswith("|---"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:]


def home_rows(text: str) -> list[tuple[str, str, str]]:
    """The parts of the architecture document that carry a Home line: (the part's heading, the paths of its Home, the tests of its Test), the line's other words left out."""
    rows: list[tuple[str, str, str]] = []
    part = ""
    for line in text.split("\n"):
        if line.startswith("### "):
            part = line[4:].strip()
        if "**Home:**" in line:
            home = line.split("**Home:**", 1)[1].split("**Status:**")[0]
            test = ""
            if "**Test:**" in home:
                home, test = home.split("**Test:**", 1)
            rows.append((part, home.strip().rstrip("."), test.strip().rstrip(".")))
    return rows


def home_paths(home: str) -> list[str]:
    """The paths a Home line names, relative to the repository: tools/, tests/, docs/ and examples/ stand as written, any other path in src/tensor24; a parenthesis and a word that is no path (term 6) are left out."""
    found: list[str] = []
    for token in re.split(r"[,;]| and ", re.sub(r"\([^)]*\)", "", home)):
        token = token.strip().strip("`")
        if not token or " " in token or not ("/" in token or token.endswith(".py")):
            continue
        found.append(token if token.startswith(("tools/", "tests/", "docs/", "examples/")) else "src/tensor24/" + token)
    return found


def trace_paths(code: str) -> list[str]:
    """The paths a trace row's code cell names, relative to the repository: a bare file name stands in the folder of the path before it, src/tensor24 holds the rest."""
    found: list[str] = []
    folder = ""
    for token in re.split(r",| and ", code):
        token = token.strip()
        if not token or token.startswith("("):
            continue
        if token.startswith("examples/"):
            found.append(token)
            continue
        if "/" in token and not token.endswith("/"):
            folder = token.rsplit("/", 1)[0]
        found.append("src/tensor24/" + (token if "/" in token else f"{folder}/{token}" if folder else token))
    return found


def check_trace(text: str, root: Path) -> list[str]:
    """The trace table against a tree: every path of a code cell and every test of a test cell exists under the root; the departures named."""
    out: list[str] = []
    rows = trace_rows(text)
    if not rows:
        homes = home_rows(text)
        if not homes:
            return ["docs/ARCHITECTURE.md: no Home line and no trace table"]
        for part, home, test in homes:
            for path in home_paths(home):
                if not (root / path).exists():
                    out.append(f"{part}: the code {path} is not in the tree")
            for name in re.split(r"[,;]| and ", re.sub(r"\([^)]*\)", "", test)):
                name = name.strip().strip("`")
                if name.endswith(".py") and not (root / "tests" / name).is_file():
                    out.append(f"{part}: the test {name} is not in the tree")
        return out
    for cells in rows:
        if len(cells) != 5:
            out.append(f"trace row of {len(cells)} cells, not 5: {cells[0][:40]}")
            continue
        part, _law, code, test, _status = cells
        for path in trace_paths(code):
            if not (root / path).exists():
                out.append(f"{part}: the code {path} is not in the tree")
        for name in re.split(r",| and ", test):
            name = name.strip()
            if name and not name.startswith("(") and not (root / "tests" / name).is_file():
                out.append(f"{part}: the test {name} is not in the tree")
    return out


LAYERS = ("Clock", "Board", "Clicks", "Algebra")
SYSTEM_SCOPE = (("src/tensor24", "*.py", True), ("tests", "*.py", True), ("examples/tensor24", "*", True), ("tools", "*.py", False))


def named_files(text: str) -> tuple[set[str], set[str]]:
    """The files and the folders the Home and Test lines of the architecture document name: (files, folders); only a folder of src/tensor24 or examples/tensor24 names the files below it, a bare tests/ or tools/ names none."""
    files: set[str] = set()
    folders: set[str] = set()
    for _part, home, test in home_rows(text):
        for path in home_paths(home):
            if path.endswith("/"):
                if path.startswith(("src/tensor24/", "examples/tensor24/")):
                    folders.add(path)
            else:
                files.add(path)
        for name in re.split(r"[,;]| and ", re.sub(r"\([^)]*\)", "", test)):
            name = name.strip().strip("`")
            if name.endswith(".py"):
                files.add("tests/" + name)
    return files, folders


def system_files(root: Path) -> list[str]:
    """The files of the tree at ROOT that belong to the system: the modules of src/tensor24, the files of tests/ and examples/tensor24, the scripts directly under tools/; no __init__.py and no cache."""
    found: list[str] = []
    for base, pattern, deep in SYSTEM_SCOPE:
        folder = root / base
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob(pattern) if deep else folder.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and "__pycache__" not in rel and path.name != "__init__.py":
                found.append(rel)
    return found


def check_mirror(text: str, root: Path) -> list[str]:
    """The tree against the document: every file of the system is named by some part's Home or Test line (the main reflects the document exactly); the departures named."""
    files, folders = named_files(text)
    return [
        f"{rel}: the tree holds it and no part's Home or Test names it"
        for rel in system_files(root)
        if rel not in files and not any(rel.startswith(folder) for folder in folders)
    ]


def part_sections(text: str) -> list[tuple[str, str]]:
    """The parts of the architecture document: each heading of three hashes, with the text up to the next heading of two or three."""
    parts: list[tuple[str, str]] = []
    name, body = "", []
    for line in text.split("\n"):
        if line.startswith("## ") or line.startswith("### "):
            if name:
                parts.append((name, "\n".join(body)))
            name, body = (line[4:].strip(), []) if line.startswith("### ") else ("", [])
        elif name:
            body.append(line)
    if name:
        parts.append((name, "\n".join(body)))
    return parts


def check_layers(text: str) -> list[str]:
    """Every part carries a Clock, a Board, a Clicks and an Algebra line with text after the label (n/a is text) and a Status: the owner's four layers with one general flag; the departures named."""
    out: list[str] = []
    for name, body in part_sections(text):
        missing = [k for k in (*LAYERS, "Status") if not re.search(r"\*\*" + k + r":\*\*[ \t]*\S", body)]
        if missing:
            out.append(f"{name}: no {', '.join(missing)} line (every part tells the four layers and its status; n/a is a text)")
    return out


LINK_FILES = ("README.md", "llms.txt", "CONTRIBUTING.md", "CHANGELOG.md", "docs/ARCHITECTURE.md", "docs/ALGEBRA.md")
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)\s]*)?\)|\b(docs/[A-Za-z0-9_.-]+\.md)\b")


def check_links(root: Path) -> list[str]:
    """Every file a live document links to (a markdown link, read from the document's own folder) or names under docs/ (read from the root) stands in the tree at ROOT; a link outside the tree, an anchor alone and the law's bare names, which cite departed documents as history, are not read."""
    out: list[str] = []
    for name in LINK_FILES:
        path = root / name
        if not path.exists():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), start=1):
            for m in LINK.finditer(line):
                target = m.group(1) or m.group(2)
                if m.group(2) and name == "docs/ALGEBRA.md":
                    continue
                if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("/"):
                    continue
                where = path.parent / target if m.group(1) else root / target
                if not where.exists():
                    out.append(f"{name}:{number}: {target} is not in the tree")
    return sorted(set(out))


def check_arch(text: str, root: Path) -> list[str]:
    """The three readings of the architecture document: its paths and tests against the tree, the tree against its Home and Test lines, its parts against the four layers."""
    return check_trace(text, root) + check_mirror(text, root) + check_layers(text)


def arch_main(argv: list[str]) -> int:
    """`--arch ROOT`: the architecture document against the tree at ROOT (the Boss's head) in both directions and against the four layers; exit 1 on a path or a test that is not there, a file of the system no part names, or a part without its layers."""
    root = Path(argv[argv.index("--arch") + 1])
    found = check_arch(ARCH.read_text(encoding="utf-8"), root) + check_links(root)
    for line in found:
        print("  " + line)
    print(f"docs/ARCHITECTURE.md against {root}: {len(trace_rows(ARCH.read_text(encoding='utf-8'))) or len(home_rows(ARCH.read_text(encoding='utf-8')))} rows; " + (f"{len(found)} departure(s)" if found else "every path and test stands"))
    return 1 if found else 0


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
    if "--arch" in argv:
        return arch_main(argv)
    law = Path(argv[argv.index("--law") + 1]) if "--law" in argv else DEFAULT_LAW
    raw = law.read_bytes().decode("utf-8")
    lines = raw.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if "--docs" in argv:
        return docs_main(lines, argv)
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
        ("the width derived against line 100", long_law({51: "**Clause 51** The width is derived", 100: "**No float anywhere** never a logarithm, an exponential, a root or a float. The width is a key of the universe file"}), 100, {"P14"}),
        ("a beat count dial against line 92 (4)", long_law({51: "**Clause 51** a rate dial and a count", 92: "**Clause 92** its act holds no round and no time"}), 100, {"P15"}),
        ("a state of 5 G + 3 marked as history is spared", long_law({51: "**Clause 51** the former state 5 G + 3", 92: "**Clause 92** its act holds no round and no time"}), 100, set()),
        ("the log's fire as a mask against the law's clause", long_law({51: "**Clause 51** the log's fire as its mask", 35: "**Clause 35** with the forward carry's bit"}), 100, {"P17"}),
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
    import tempfile

    table = (
        "## The trace table\n\n| Part | Law line | Code | Test | Status |\n|---|---|---|---|---|\n"
        "| The loader | 92 | runner/files.py, board.py | test_a.py | BUILT |\n"
        "| The act | 90 | engine/ and algebra/ | test_a.py, test_b.py | BUILT |\n"
        "| The click | 35 | (none yet) | (none yet) | OPEN |\n"
        "| The world | 35 | examples/tensor24/ | test_a.py | BUILT |\n\n## Next\n"
    )
    home_doc = (
        "### The loader\n\n- **Home:** runner/files.py, runner/board.py; tools/x.py. **Test:** test_a.py. **Status:** BUILT.\n\n"
        "### The act\n\n- **Home:** engine/step.py (the act), algebra/carry.py and main.py. **Test:** test_a.py, test_b.py. **Status:** by term.\n"
    )
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        for folder in ("src/tensor24/runner", "src/tensor24/engine", "src/tensor24/algebra", "examples/tensor24", "tests", "tools"):
            (root / folder).mkdir(parents=True)
        for name in ("src/tensor24/runner/files.py", "src/tensor24/runner/board.py", "src/tensor24/engine/step.py", "src/tensor24/algebra/carry.py", "src/tensor24/main.py", "tools/x.py", "tests/test_a.py", "tests/test_b.py"):
            (root / name).write_text("", encoding="utf-8")
        trace_cases = (
            ("a trace table whose every path and test stands", table, set()),
            ("a code path that is not in the tree", table.replace("board.py", "gone.py"), {"The loader: the code src/tensor24/runner/gone.py is not in the tree"}),
            ("a test that is not in the tree", table.replace("test_b.py", "test_gone.py"), {"The act: the test test_gone.py is not in the tree"}),
            ("a document with no trace table", "# Title\n", {"docs/ARCHITECTURE.md: no Home line and no trace table"}),
            ("Home lines whose every path and test stands", home_doc, set()),
            ("a Home path that is not in the tree", home_doc.replace("runner/board.py", "runner/gone.py"), {"The loader: the code src/tensor24/runner/gone.py is not in the tree"}),
            ("a Test that is not in the tree", home_doc.replace("test_b.py", "test_gone.py"), {"The act: the test test_gone.py is not in the tree"}),
            ("a Home with a word that is no path", home_doc.replace("main.py.", "main.py, term 6."), set()),
        )
        for name, text, want in trace_cases:
            got = set(check_trace(text, root))
            if got != want:
                failed += 1
                print(f"PARTED  {name}: wanted {sorted(want)}, got {sorted(got)}")
            else:
                print(f"ok      {name}")
    layer_part = (
        "### The act\n\n- **Clock:** a dial turns.\n- **Board:** n/a\n- **Clicks:** none of its own.\n- **Algebra:** the carry.\n"
        "- **Home:** engine/step.py. **Test:** test_a.py. **Status:** BUILT.\n"
    )
    mirror_cases = (
        ("every file of the system is named", layer_part, ("src/tensor24/engine/step.py", "tests/test_a.py"), set()),
        ("a module no part names", layer_part, ("src/tensor24/engine/step.py", "tests/test_a.py", "src/tensor24/engine/extra.py"), {"src/tensor24/engine/extra.py: the tree holds it and no part's Home or Test names it"}),
        ("a folder named in a Home line names the files below it", layer_part.replace("engine/step.py", "decoder/ (it imports the record alone)"), ("src/tensor24/decoder/a.py", "src/tensor24/decoder/b/c.py", "tests/test_a.py"), set()),
        ("a bare tests/ folder names no test", layer_part.replace("engine/step.py.", "engine/step.py, tests/."), ("src/tensor24/engine/step.py", "tests/test_a.py", "tests/test_extra.py"), {"tests/test_extra.py: the tree holds it and no part's Home or Test names it"}),
        ("an __init__.py and a cache are no file of the system", layer_part, ("src/tensor24/engine/step.py", "tests/test_a.py", "src/tensor24/engine/__init__.py", "src/tensor24/engine/__pycache__/x.py", "tests/__init__.py"), set()),
        ("a script under tools/ no part names", layer_part, ("src/tensor24/engine/step.py", "tests/test_a.py", "tools/foo.py"), {"tools/foo.py: the tree holds it and no part's Home or Test names it"}),
        ("a file of the records under tools/derivations is outside the system", layer_part, ("src/tensor24/engine/step.py", "tests/test_a.py", "tools/derivations/x.py"), set()),
        ("an example file no part names", layer_part, ("src/tensor24/engine/step.py", "tests/test_a.py", "examples/tensor24/universe.json"), {"examples/tensor24/universe.json: the tree holds it and no part's Home or Test names it"}),
        ("a helper of tests/ named in a Test line", layer_part.replace("test_a.py.", "test_a.py, frame.py."), ("src/tensor24/engine/step.py", "tests/test_a.py", "tests/frame.py"), set()),
    )
    for name, text, files, want in mirror_cases:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for rel in files:
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text("", encoding="utf-8")
            got = set(check_mirror(text, root))
        if got != want:
            failed += 1
            print(f"PARTED  {name}: wanted {sorted(want)}, got {sorted(got)}")
        else:
            print(f"ok      {name}")
    layer_cases = (
        ("a part with the four layers and its status", layer_part, set()),
        ("a part with no Board line", layer_part.replace("- **Board:** n/a\n", ""), {"The act: no Board line (every part tells the four layers and its status; n/a is a text)"}),
        ("a Clicks label with no text after it", layer_part.replace("**Clicks:** none of its own.", "**Clicks:**"), {"The act: no Clicks line (every part tells the four layers and its status; n/a is a text)"}),
        ("a part with no Status and no Algebra", layer_part.replace("**Status:** BUILT.", "").replace("- **Algebra:** the carry.\n", ""), {"The act: no Algebra, Status line (every part tells the four layers and its status; n/a is a text)"}),
        ("a heading of two hashes closes the part", layer_part + "\n## 4. Who may import whom\n\n- **Clock:** words after the part.\n", set()),
        ("two parts, the second without layers", layer_part + "\n### The loader\n\nOnly words.\n", {"The loader: no Clock, Board, Clicks, Algebra, Status line (every part tells the four layers and its status; n/a is a text)"}),
    )
    for name, text, want in layer_cases:
        got = set(check_layers(text))
        if got != want:
            failed += 1
            print(f"PARTED  {name}: wanted {sorted(want)}, got {sorted(got)}")
        else:
            print(f"ok      {name}")
    link_cases = (
        ("a markdown link to a file that stands", {"README.md": "See [the law](docs/ALGEBRA.md).", "docs/ALGEBRA.md": ""}, set()),
        ("a markdown link to a file that is gone", {"README.md": "See [it](docs/ENGINE.md#x).", "docs/ALGEBRA.md": ""}, {"README.md:1: docs/ENGINE.md is not in the tree"}),
        ("an anchor alone and an address outside the tree", {"README.md": "[a](#top) [b](https://example.org/x) [c](mailto:a@b.c)"}, set()),
        ("a bare name under docs/ that is gone, in llms.txt", {"llms.txt": "named (docs/FURTHER_RESEARCH.md, first)."}, {"llms.txt:1: docs/FURTHER_RESEARCH.md is not in the tree"}),
        ("a link in the architecture document is read from its own folder", {"docs/ARCHITECTURE.md": "[law](ALGEBRA.md) [door](../README.md)", "docs/ALGEBRA.md": "", "README.md": ""}, set()),
        ("a link in the architecture document to a file that is gone", {"docs/ARCHITECTURE.md": "[x](GONE.md)"}, {"docs/ARCHITECTURE.md:1: GONE.md is not in the tree"}),
        ("the law's bare citation of a departed document is history", {"docs/ALGEBRA.md": "built per docs/ENGINE.md, since departed"}, set()),
        ("the law's markdown link to a departed document is read", {"docs/ALGEBRA.md": "see [the engine](ENGINE.md)"}, {"docs/ALGEBRA.md:1: ENGINE.md is not in the tree"}),
    )
    for name, files, want in link_cases:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for rel, body in files.items():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(body, encoding="utf-8")
            got = set(check_links(root))
        if got != want:
            failed += 1
            print(f"PARTED  {name}: wanted {sorted(want)}, got {sorted(got)}")
        else:
            print(f"ok      {name}")
    print(f"selftest: {len(cases) + len(trace_cases) + len(mirror_cases) + len(layer_cases) + len(link_cases)} cases, {failed} parted")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
