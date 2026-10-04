"""The reading gate (the owner's word of 2026-10-04, relayed by the advisor on #1793, comments 5974878000 and 5974938542: the experimenter's readings are kept in each folder's document and a gate re-runs the gate worlds and compares bit for bit): for every folder named under examples/events/ the gate reads the block `## The gate's table` of the folder's `blind_and_reading.md`, a markdown table of five columns, `label`, `world`, `by`, `reading` and `value`, one row per number the experimenter read on the current tree, re-runs the world as the row's `by` says (`run_inputs`, the world once over its `ticks` by tools/run_inputs.py, its output file read back as the experimenter reads it; `meeting_trials`, the design's seeds by tools/meeting_trials.py; `back_in_time`, tools/back_in_time.py over the row's `intervals N`), reads the number the row names (RUN_READINGS and TRIAL_READINGS below: the NodeReader's lines, the clicks, labelled NODEREADER, the one measurement; the books, the ticks, the verdict, the line counts, the trials' count and the back-in-time verdict labelled GAMEBOARD, diagnostics) and compares it with the row's value bit for bit: one JSON line per row with both values, the label and the verdict, MATCH or DIFFERS (a row whose label is not the reading's own DIFFERS by name; a row the gate cannot read DIFFERS with the reason), then one summary line per folder. A folder whose document holds no table is UNFILLED, for the experimenter to fill; the gate invents no number. Where the document holds no gate's table but a reading table in one of two shipped shapes, the screen table (`region`, then `<world> clicks` columns, the which-way folder; the shares beside them are a GameBoard reading and not read) or the trials table (`world`, then `A only`, `B only`, `both`, `neither` and `alpha`, the anticoincidence folder), the last such table is read in its place. Exit code 0 where every row is MATCH, 1 otherwise. A host tool: it holds no number of the law and writes nothing to the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/reading_gate.py examples/events/<folder> ...
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe.game_board import GameBoard
from event_universe.world_files import load_world

sys.path.insert(0, str(Path(__file__).resolve().parent))
from back_in_time import verdict as back_in_time_verdict  # noqa: E402
from meeting_trials import reading as trials_reading  # noqa: E402
from run_inputs import run_input  # noqa: E402

DOCUMENT = "blind_and_reading.md"
TABLE = "The gate's table"  # the heading of the block the gate reads
COLUMNS = ("label", "world", "by", "reading", "value")  # the block's columns, in this order
MEASUREMENT, DIAGNOSTIC = "NODEREADER", "GAMEBOARD"  # the output's labels (reports.py)
MATCH, DIFFERS, UNFILLED = (
    "MATCH",
    "DIFFERS",
    "UNFILLED",
)  # a row's verdicts and a folder's without a table
RUN, TRIALS, BACK = (
    "run_inputs",
    "meeting_trials",
    "back_in_time",
)  # the row's `by`: the tool that re-runs
NONE = "none"  # a reading that is None, as the document writes it
EXCHANGES = {"takings": "taken", "givings": "given"}  # a record's clicks by the family exchanged
COINCIDENCE = {
    "A only": "A_only",
    "B only": "B_only",
    "both": "both",
    "neither": "neither",
    "alpha": "alpha",
}
RUN_READINGS = (
    "ticks",
    "verdict",
    "lines <event>",
    "books <family> <key>",
    "density <node_reader> <family>",
    "clicks [<node_reader>]",
    "inflow <node_reader> <family>",
    "takings <node_reader>",
    "givings <node_reader>",
    "conversions <node_reader>",
)  # the readings of one run's output file
TRIAL_READINGS = ("trials", "refused", "ends in <part> <node_reader>", *COINCIDENCE, "clicks <kind>")
SEPARATOR = re.compile(r":?-+:?")  # a cell of a markdown table's separator row
SCREEN, TRIAL_COLUMNS = "region", tuple(COINCIDENCE)  # the two shipped table shapes, by their headers
Row = dict[str, str]
Table = tuple[str | None, list[list[str]]]  # a table's heading and its rows as cells, the header first
Value = Fraction | str


def cells_of(line: str) -> list[str]:
    """The cells of a markdown table's row, stripped."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def tables_of(text: str) -> list[Table]:
    """Every markdown table of a document with the heading above it (None before the first heading), its header row first and its separator row left out."""
    found: list[Table] = []
    heading, rows = None, []
    for line in [*text.splitlines(), ""]:
        if line.lstrip().startswith("|"):
            cells = cells_of(line)
            if not all(SEPARATOR.fullmatch(cell) for cell in cells):
                rows.append(cells)
            continue
        if rows:
            found.append((heading, rows))
            rows = []
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
    return found


def gate_rows(tables: list[Table]) -> list[Row] | None:
    """The rows of the gate's table, each a dictionary over COLUMNS; None where the document holds no such block; a block with other columns or a row of another width is refused by name."""
    for heading, rows in tables:
        if heading == TABLE:
            if tuple(cell.lower() for cell in rows[0]) != COLUMNS:
                raise ValueError(f"the columns of {TABLE!r} are {rows[0]}, not {list(COLUMNS)}")
            for cells in rows[1:]:
                if len(cells) != len(COLUMNS):
                    raise ValueError(
                        f"the row {cells} of {TABLE!r} has {len(cells)} cells, not {len(COLUMNS)}"
                    )
            return [dict(zip(COLUMNS, cells, strict=True)) for cells in rows[1:]]
    return None


def numeric(cell: str) -> bool:
    """Whether a cell is a number the gate compares (a whole number, a fraction or a decimal)."""
    return isinstance(parsed(cell), Fraction)


def shipped_rows(tables: list[Table]) -> list[Row]:
    """The rows of the last reading table in a shipped shape, as gate rows labelled NODEREADER, the clicks: the screen table (`region`, then `<world> clicks` columns, every other column left out; the row `N` the clicks of every region) and the trials table (`world`, then `A only` to `alpha`; a count `n of m` read as n and alpha's fraction before its decimal)."""
    found: list[Row] = []
    for _heading, rows in tables:
        header = rows[0]
        if header[0] == SCREEN:
            found = []
            for cells in rows[1:]:
                for name, cell in zip(header[1:], cells[1:], strict=False):
                    world, _, kind = name.rpartition(" ")
                    if kind == "clicks" and numeric(cell):
                        reading = "clicks" if cells[0] == "N" else f"clicks {cells[0]}"
                        row = (MEASUREMENT, f"{world}.json", RUN, reading, cell)
                        found.append(dict(zip(COLUMNS, row, strict=True)))
        elif header[0] == "world" and tuple(header[1:]) == TRIAL_COLUMNS:
            found = []
            for cells in rows[1:]:
                for name, cell in zip(header[1:], cells[1:], strict=True):
                    value = cell.split(" of ")[0].split("=")[0].strip()
                    row = (MEASUREMENT, f"{cells[0]}.json", TRIALS, name, value)
                    found.append(dict(zip(COLUMNS, row, strict=True)))
    return found


def parsed(cell: str) -> Value:
    """A documented value: a whole number, a fraction `p / q` or a decimal as an exact fraction; any other text as written."""
    try:
        return Fraction(cell.replace(" ", ""))
    except ValueError, ZeroDivisionError:
        return cell.strip()


def as_value(found: object) -> Value:
    """A re-read value as the documented values are compared: an integer, or a [numerator, denominator] pair, as a fraction; None as `none`; other text as written."""
    if isinstance(found, int) and not isinstance(found, bool):
        return Fraction(found)
    if isinstance(found, list) and len(found) == 2 and all(isinstance(v, int) for v in found):
        return Fraction(found[0], found[1])
    return NONE if found is None else str(found)


def printed(value: Value) -> str:
    """A value as the report prints it: a whole number plain, a fraction as `p / q`, text as it is."""
    if isinstance(value, Fraction):
        return (
            str(value.numerator)
            if value.denominator == 1
            else f"{value.numerator} / {value.denominator}"
        )
    return value


def credits(output: dict[str, Any], node_reader: str | None, exchanged: str | None = None) -> int:
    """The quanta the `credit` lines labelled NODEREADER count (the null window's GAMEBOARD lines left out), every reader's or one reader's by name, and among them those exchanging a quantum with another family where `exchanged` is `taken` or `given`."""
    lines = [
        line for line in output["lines"] if line["event"] == "credit" and line["label"] == MEASUREMENT
    ]
    lines = [line for line in lines if node_reader is None or line["node_reader"] == node_reader]
    lines = [line for line in lines if exchanged is None or line[exchanged] is not None]
    return sum(int(line["count"]) for line in lines)


def run_reading(output: dict[str, Any], words: list[str]) -> tuple[str, object]:
    """One reading of a run's output by the row's words (RUN_READINGS), with the reading's own label: the clicks from the NodeReader's lines, labelled NODEREADER; the ticks, the verdict, a line count, a books entry and a region's last density labelled GAMEBOARD."""
    kind, rest, lines = words[0], words[1:], output["lines"]
    if kind in ("ticks", "verdict") and not rest:
        return DIAGNOSTIC, output[kind]
    if kind == "lines" and len(rest) == 1:
        return DIAGNOSTIC, sum(line["event"] == rest[0] for line in lines)
    if kind == "books" and len(rest) == 2:
        return DIAGNOSTIC, output["books"][rest[0]][rest[1]]
    if kind == "density" and len(rest) >= 2:
        name, family = " ".join(rest[:-1]), rest[-1]
        at = [line for line in lines if line["event"] == kind and line["node_reader"] == name]
        readings = [line["reading"] for line in at if line["family"] == family]
        return DIAGNOSTIC, readings[-1] if readings else None
    if kind == "clicks":
        return MEASUREMENT, credits(output, " ".join(rest) or None)
    if kind in EXCHANGES and rest:
        return MEASUREMENT, credits(output, " ".join(rest), EXCHANGES[kind])
    if kind == "conversions" and rest:
        name = " ".join(rest)
        return MEASUREMENT, sum(
            line["event"] == "conversion" and line["node_reader"] == name for line in lines
        )
    if kind == "inflow" and len(rest) >= 2:
        name, family = " ".join(rest[:-1]), rest[-1]
        at = [line for line in lines if line["event"] == "click" and line["node_reader"] == name]
        return MEASUREMENT, sum(int(line["inflow"]) for line in at if line["family"] == family)
    raise ValueError(f"the reading {' '.join(words)!r} is none of a run's: {', '.join(RUN_READINGS)}")


def trial_reading(found: dict[str, Any], words: list[str]) -> tuple[str, object]:
    """One reading of the trials by the row's words (TRIAL_READINGS), with the reading's own label: the parts the records end in, the coincidences and the clicks per kind labelled NODEREADER; the trials' count and the refused seeds' count labelled GAMEBOARD."""
    text = " ".join(words)
    if text == "trials":
        return DIAGNOSTIC, found["trials"]
    if text == "refused":
        return DIAGNOSTIC, len(found["refused"])
    if text in COINCIDENCE:
        value = found["coincidence"].get(COINCIDENCE[text]) if found["coincidence"] else None
        return MEASUREMENT, value[0] if text != "alpha" and isinstance(value, list) else value
    if words[:2] == ["ends", "in"] and len(words) > 3:
        ends = found["ends_in_part"].get(" ".join(words[3:]), {})
        return MEASUREMENT, ends.get(words[2], [0])[0]
    if words[0] == "clicks" and len(words) > 1:
        return MEASUREMENT, found["clicks"].get(" ".join(words[1:]), 0)
    raise ValueError(f"the reading {text!r} is none of the trials': {', '.join(TRIAL_READINGS)}")


def read(folder: Path, row: Row, cache: dict[tuple[str, str], Any], out: Path) -> tuple[str, object]:
    """The reading a row names, re-read on the current tree with its own label: the world run as the row's `by` says, once per world and tool (`cache`; the runner's output file written under `out` and read back), and the number taken by the row's words."""
    world, by, words = row["world"], row["by"], row["reading"].split()
    path = folder / world
    if not path.is_file():
        raise ValueError(f"the world {world!r} is not in {folder.as_posix()}")
    if by == RUN:
        if (RUN, world) not in cache:
            run_input(str(path), str(out))
            written = out / f"{path.stem}.output.json"
            cache[(RUN, world)] = json.loads(written.read_text(encoding="utf-8"))
        return run_reading(cache[(RUN, world)], words)
    if by == TRIALS:
        if (TRIALS, world) not in cache:
            cache[(TRIALS, world)] = trials_reading(path, folder / "design.json", None)
        return trial_reading(cache[(TRIALS, world)], words)
    if by == BACK and words[:1] == ["intervals"] and len(words) == 2:
        key = (BACK, f"{world} {words[1]}")
        if key not in cache:
            cache[key] = back_in_time_verdict(GameBoard(load_world(path)), int(words[1]))
        return DIAGNOSTIC, cache[key]["verdict"]
    raise ValueError(
        f"the row's by {by!r} with the reading {row['reading']!r} is none the gate runs: "
        f"{RUN}, {TRIALS}, or {BACK} with `intervals N`"
    )


def verdict_of(
    folder: Path, row: Row, cache: dict[tuple[str, str], Any], out: Path
) -> dict[str, object]:
    """One row's verdict: MATCH where the re-read value is the documented one bit for bit and the row's label is the reading's own, else DIFFERS, with the reason where the label or the reading itself is the cause."""
    found: dict[str, object] = {"folder": folder.as_posix(), **row}
    try:
        label, value = read(folder, row, cache, out)
    except (ValueError, KeyError, IndexError, RuntimeError, OSError) as refusal:
        return {**found, "read": None, "verdict": DIFFERS, "reason": str(refusal)}
    reread = as_value(value)
    found["read"] = printed(reread)
    if row["label"] != label:
        return {**found, "verdict": DIFFERS, "reason": f"the reading's own label is {label}"}
    return {**found, "verdict": MATCH if parsed(row["value"]) == reread else DIFFERS}


def gate(folder: Path) -> list[dict[str, object]]:
    """Every row's verdict for one folder, the row's source named under `table` (`gate` for the gate's table, `shipped` for a shipped table read in its place); one UNFILLED line where the folder's document holds neither, or a block the gate cannot read."""
    document = folder / DOCUMENT
    unfilled: dict[str, object] = {"folder": folder.as_posix(), "verdict": UNFILLED}
    if not document.is_file():
        return [{**unfilled, "reason": f"no {DOCUMENT} in the folder"}]
    tables = tables_of(document.read_text(encoding="utf-8"))
    try:
        rows, source = gate_rows(tables), "gate"
    except ValueError as refusal:
        return [{**unfilled, "reason": str(refusal)}]
    if rows is None:
        rows, source = shipped_rows(tables), "shipped"
    if not rows:
        reason = f"no block `## {TABLE}` in {DOCUMENT} and no shipped reading table; the experimenter fills it"
        return [{**unfilled, "reason": reason}]
    cache: dict[tuple[str, str], Any] = {}
    with tempfile.TemporaryDirectory() as out:
        return [{**verdict_of(folder, row, cache, Path(out)), "table": source} for row in rows]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "folders",
        nargs="+",
        type=Path,
        help=f"the folders under examples/events/, each with its {DOCUMENT}",
    )
    args = parser.parse_args(argv)
    lines = [line for folder in args.folders for line in gate(folder)]
    for line in lines:
        print(json.dumps(line))
    for folder in args.folders:
        own = [line for line in lines if line["folder"] == folder.as_posix()]
        counts = {
            kind: sum(line["verdict"] == kind for line in own) for kind in (MATCH, DIFFERS, UNFILLED)
        }
        summary = ", ".join(f"{count} {kind}" for kind, count in counts.items())
        print(f"{folder.as_posix()}: {len(own)} rows, {summary}")
    agreed = all(line["verdict"] == MATCH for line in lines)
    print(f"the reading gate: {MATCH if agreed else DIFFERS} on {len(args.folders)} folder(s)")
    sys.exit(0 if agreed else 1)


if __name__ == "__main__":
    main()
