"""The gates of the phenomena (the owner's word of 2026-10-26, 00:24 UTC, through the Boss, #2187 comments 6405405057 and 6405481357: the table of gates managed in one place, named so that it reads so that everyone understands): the one table of docs/UNIVERSE24.md's section 2, rendered by this tool from the readings of the records run from the seed, one row per gate, the phenomenon in plain words first, the gate's number, the verdict per record (SHOWN with the records that show it, NOT SHOWN or NOT READ with the cause), the change since the table before; the table replaced whole in the document on every read, the verdict of every row the decoder's and nobody's hand. Usage: `python tools/phenomena.py <sha> <name=reading.jsonl>... [--document docs/UNIVERSE24.md]`; with no document the table is printed."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

HEADING = "### The gates of the phenomena"
ROWS = 60  # the rows of the table, the phenomena of nature the run must show
GATE_COLUMN, VERDICT_COLUMN = (
    1,
    2,
)  # the table's cells after the phenomenon: the gate's number, the verdict
OPTION_WORDS = 2  # a --document option and its path, two words of the command line
NOT = "NOT"  # the word a verdict begins with where the gate is not shown, read or reached
KINDS = ("SHOWN", "SHOWN in part", f"{NOT} SHOWN", f"{NOT} REACHED", f"{NOT} READ")
PHENOMENA = {
    1: "the recurring bang",
    2: "the lengthening of the Links",
    3: "the Links shortening, then lengthening",
    4: "the era of matter",
    5: "the acceleration of the expansion",
    6: "the contraction",
    7: "light present and absorbed",
    8: "the families forming",
    9: "the collision of two bodies",
    10: "gravitational time dilation",
    11: "gravitational redshift",
    12: "the delay and the bending of light",
    13: "free fall",
    14: "the horizon, a black hole",
    15: "conservation at the click",
    16: "the uncertainty floor",
    17: "charge conservation",
    18: "the arrow of time and its reversal",
    19: "the mass ratios",
    20: "the twist, P and C violated, CP kept",
    21: "the handedness of the birth",
    22: "Coulomb's sign",
    23: "the momentum across the click",
    24: "the merger of a pair into light",
    25: "the entropy rising",
    26: "the three lifts and their masses",
    27: "confinement, no third alone",
    28: "the neutron's conversion",
    29: "the redshift of light",
    30: "the dilation of a body's clock",
    31: "the deflection and the Shapiro delay",
    32: "the perihelion's advance",
    33: "free fall by the tail",
    34: "the stopped clock at the horizon",
    35: "frame dragging",
    36: "gravitational waves, the shears",
    37: "Maxwell's one Link per interval",
    38: "the Aharonov-Bohm phase",
    39: "the Zeeman and Stark shifts",
    40: "the photoelectric click",
    41: "the spinor's two beats",
    42: "Stern-Gerlach, the split along the gradient",
    43: "the exclusion",
    44: "the moving packet's velocity",
    45: "the bound body in its well",
    46: "the bang recurring with its gates",
    47: "the exact take",
    48: "the black body",
    49: "the exponential decay",
    50: "light on light",
    51: "the Casimir force and the running alpha",
    52: "the neutrino",
    53: "a fast packet binding",
    54: "scattering, two packets through each other",
    55: "the two slits",
    56: "Bell's correlation",
    57: "the GHZ correlation",
    58: "the fast expansion after the bang, in the clicks",
    59: "the deceleration, in the clicks",
    60: "the acceleration, in the clicks",
}


def reading_of(path: str | Path) -> dict[int, dict[str, Any]]:
    """A reading file's numbered rows: the gate's number to its row (its verdict among the numbers)."""
    rows: dict[int, dict[str, Any]] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        for key, row in json.loads(line).items():
            found = re.match(r"(\d+) ", key)
            if found and isinstance(row, dict) and "verdict" in row:
                rows[int(found.group(1))] = row | {"key": key}
    return rows


def kind_of(verdict: str) -> str:
    """A verdict's kind: SHOWN or SHOWN in part, else NOT with SHOWN, with REACHED or with READ; a restated row's by the gate it restates."""
    words = verdict.split(": ", 1)[1] if verdict.startswith("as gate") else verdict
    return next((kind for kind in reversed(KINDS) if words.startswith(kind)), "NOT READ")


def cause_of(verdict: str) -> str:
    """The verdict's own words after its kind, the cause where not SHOWN, one clause."""
    words = verdict.split(": ", 1)[1] if verdict.startswith("as gate") else verdict
    for kind in reversed(KINDS):
        if words.startswith(kind):
            words = words[len(kind) :]
            break
    return words.strip(" :;").split(";")[0].strip()


def rows_of(readings: dict[str, dict[int, dict[str, Any]]], before: dict[int, set[str]]) -> list[str]:
    """The table's rows from the named readings and the SHOWN sets of the table before."""
    found = []
    for gate in range(1, ROWS + 1):
        kinds = {name: kind_of(rows[gate]["verdict"]) for name, rows in readings.items() if gate in rows}
        shown = {name for name, kind in kinds.items() if kind == "SHOWN"}
        if not kinds:
            verdict = "NOT READ by the decoder: no row (the predicate in the hands' file, the row owed)"
            cause = ""
        else:
            verdict = "; ".join(
                f"{kind} on {', '.join(n for n in readings if kinds.get(n) == kind)}"
                for kind in KINDS
                if any(kinds.get(n) == kind for n in readings)
            )
            worst = next((n for n in readings if kinds.get(n) not in ("SHOWN", None)), None)
            cause = cause_of(readings[worst][gate]["verdict"]) if worst else ""
        was = before.get(gate)
        change = (
            "the first table"
            if was is None
            else "unchanged"
            if was == shown
            else "SHOWN now on " + ", ".join(sorted(shown - was))
            if shown > was
            else "REGRESSED on " + ", ".join(sorted(was - shown))
            if shown < was
            else "SHOWN now on "
            + ", ".join(sorted(shown - was))
            + "; REGRESSED on "
            + ", ".join(sorted(was - shown))
        )
        found.append(f"| {PHENOMENA[gate]} | {gate} | {verdict} | {cause} | {change} |")
    return found


def before_of(document: str) -> dict[int, set[str]]:
    """The SHOWN sets of the table standing in the document, by gate, read from its own rows."""
    found: dict[int, set[str]] = {}
    for line in section_of(document).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) > VERDICT_COLUMN and cells[GATE_COLUMN].isdigit():
            shown = re.match(r"SHOWN on ([^;]+)", cells[VERDICT_COLUMN])
            found[int(cells[GATE_COLUMN])] = set(shown.group(1).split(", ")) if shown else set()
    return found


def section_of(document: str) -> str:
    """The tool's own section of the document, from its heading to the next heading."""
    start = document.find(HEADING)
    if start < 0:
        return ""
    end = document.find("\n### ", start + len(HEADING))
    return document[start : end if end > 0 else len(document)]


def table_of(
    sha: str, readings: dict[str, dict[int, dict[str, Any]]], before: dict[int, set[str]]
) -> str:
    """The section: its heading, one line on the head and the records, the table."""
    shown = sum(
        1
        for gate in range(1, ROWS + 1)
        if any(gate in rows and kind_of(rows[gate]["verdict"]) == "SHOWN" for rows in readings.values())
    )
    head = f"SHOWN in Universe24: {shown} of {ROWS} on {sha}"
    records = ", ".join(readings)
    return "\n".join(
        [
            f"{HEADING} (the head {sha}; written by tools/phenomena.py from the readings, the verdict of every row the decoder's)",
            "",
            f"{head}. The records read from the seed alone: {records}. A row is SHOWN in Universe24 where the decoder's verdict reads SHOWN on at least one record; SHOWN in part is not counted; a row with no line in the decoder is NOT READ by the decoder.",
            "",
            "| the phenomenon | gate | the verdict per record | the cause where not SHOWN | since the table before |",
            "| --- | --- | --- | --- | --- |",
            *rows_of(readings, before),
            "",
        ]
    )


def write(document_path: Path, sha: str, readings: dict[str, dict[int, dict[str, Any]]]) -> str:
    """The document with its section replaced whole (or the section added at the end of section 2 where none stands)."""
    document = document_path.read_text(encoding="utf-8")
    old = section_of(document)
    new = table_of(sha, readings, before_of(document))
    if old:
        document = document.replace(old, new, 1)
    else:
        marker = "### The gates widened to everything derived"
        at = document.find(marker)
        document = document[:at] + new + "\n" + document[at:] if at > 0 else document + "\n" + new
    document_path.write_text(document, encoding="utf-8")
    return new


def main(argv: list[str]) -> None:
    """The table from the arguments: the head's sha, name=reading pairs, and the document to write."""
    document = None
    if "--document" in argv:
        at = argv.index("--document")
        document = Path(argv[at + OPTION_WORDS - 1])
        argv = argv[:at] + argv[at + OPTION_WORDS :]
    sha = argv[1]
    readings = {pair.split("=", 1)[0]: reading_of(pair.split("=", 1)[1]) for pair in argv[2:]}
    if document is None:
        print(table_of(sha, readings, {}))
    else:
        print(write(document, sha, readings))


if __name__ == "__main__":
    main(sys.argv)
