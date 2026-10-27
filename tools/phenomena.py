"""The gates of the phenomena (the owner's word of 2026-10-26, 00:24 UTC, through the Boss, #2187 comments 6405405057 and 6405481357: the table of gates managed in one place, named so that it reads so that everyone understands): the one table of docs/UNIVERSE24.md's section 2, rendered by this tool from the readings of the records run from the seed, one row per gate, the phenomenon in plain words first (the decoder's own field, as its kind and its cause), the gate's number, the verdict per record (SHOWN with the records that show it, NOT SHOWN or NOT READ with the cause), the change since the table before; the table replaced whole in the document on every read, the verdict of every row the decoder's and nobody's hand. Usage: `python tools/phenomena.py <sha> <name=reading.jsonl>... [--document docs/UNIVERSE24.md]`; with no document the table is printed."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

HEADING = "### The gates of the phenomena"
GATE_COLUMN, VERDICT_COLUMN = (
    1,
    2,
)  # the table's cells after the phenomenon: the gate's number, the verdict
OPTION_WORDS = 2  # a --document option and its path, two words of the command line
DERIVATIONS = "tools/derivations/open_items/READER-THE-GATES-DERIVED.md"
DERIVED = {  # each row's derivation from the algebra alone (the owner's word of 2026-10-27, 15:12 UTC), by the page above
    "an identity": "7 14 15 17 18 25 27 34 40 43 47 62 65 67 68 70 71 72",
    "under a condition": "1 2 3 4 5 6 10 19 20 24 29 30 37 44 45 46 55 63 73",
}
NOT = "NOT"  # the word a verdict begins with where the gate is not shown, read or reached
KINDS = (
    "SHOWN",
    "SHOWN in part",
    f"{NOT} SHOWN",
    f"{NOT} REACHED",
    f"{NOT} READ",
)  # the kinds the decoder writes, in the table's order


def reading_lines(path: str | Path) -> list[dict[str, Any]]:
    """A reading file's lines (one JSON object per line, the gates' output), the one loader of a reading for the table and the page."""
    return [
        json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def reading_of(path: str | Path) -> dict[int, dict[str, Any]]:
    """A reading file's numbered rows: the gate's number to its row (its verdict among the numbers)."""
    rows: dict[int, dict[str, Any]] = {}
    for line in reading_lines(path):
        for key, row in line.items():
            found = re.match(r"(\d+) ", key)
            if found and isinstance(row, dict) and "verdict" in row:
                rows[int(found.group(1))] = row | {"key": key}
    return rows


def rows_in(readings: dict[str, dict[int, dict[str, Any]]]) -> int:
    """The rows of the table, the phenomena of nature the run must show: the largest numbered row the readings carry (the decoder's table names them, one function per row, so a new row enters the table with its reading alone)."""
    return max((gate for rows in readings.values() for gate in rows), default=0)


def rows_of(readings: dict[str, dict[int, dict[str, Any]]], before: dict[int, set[str]]) -> list[str]:
    """The table's rows from the named readings and the SHOWN sets of the table before."""
    found = []
    for gate in range(1, rows_in(readings) + 1):
        kinds = {name: rows[gate]["kind"] for name, rows in readings.items() if gate in rows}
        phenomenon = next(
            (rows[gate]["phenomenon"] for rows in readings.values() if gate in rows), f"row {gate}"
        )
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
            cause = readings[worst][gate]["cause"] if worst else ""
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
        found.append(f"| {phenomenon} | {gate} | {verdict} | {cause} | {change} | {derived_of(gate)} |")
    return found


def derived_of(gate: int) -> str:
    """A row's status from the algebra alone: an identity, under a condition, or not derived (DERIVATIONS)."""
    return next((status for status, rows in DERIVED.items() if str(gate) in rows.split()), "not derived")


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
        for gate in range(1, rows_in(readings) + 1)
        if any(gate in rows and rows[gate]["kind"] == "SHOWN" for rows in readings.values())
    )
    head = f"SHOWN in Universe24: {shown} of {rows_in(readings)} on {sha}"
    seen = [
        gate
        for gate in range(1, rows_in(readings) + 1)
        if any(gate in rows and rows[gate]["kind"] == "SHOWN" for rows in readings.values())
    ]
    weighed = sum(1 for gate in seen if derived_of(gate) != "not derived")
    tally = {status: len(rows.split()) for status, rows in DERIVED.items()}
    derived = f"Derived from the algebra alone ({DERIVATIONS}): {tally['an identity']} rows as identities, {tally['under a condition']} under a condition, {rows_in(readings) - sum(tally.values())} not derived; SHOWN and derived, the rows that weigh: {weighed} of {rows_in(readings)}."
    records = ", ".join(readings)
    return "\n".join(
        [
            f"{HEADING} (the head {sha}; written by tools/phenomena.py from the readings, the verdict of every row the decoder's)",
            "",
            f"{head}. The records read from the seed alone: {records}. A row is SHOWN in Universe24 where the decoder's verdict reads SHOWN on at least one record; SHOWN in part is not counted; a row with no line in the decoder is NOT READ by the decoder. {derived}",
            "",
            "| the phenomenon | gate | the verdict per record | the cause where not SHOWN | since the table before | derived from the algebra |",
            "| --- | --- | --- | --- | --- | --- |",
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
    """The table from the arguments: the head's sha, name=reading pairs, and the document to write; a reading's integers read whole however long."""
    sys.set_int_max_str_digits(0)
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
