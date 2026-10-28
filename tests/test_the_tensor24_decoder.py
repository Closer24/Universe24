"""Tensor24's decoder: a record and its ledger read under the schema's rules, each broken one not read with its own cause
and nothing raised; row 15's two readings; the ticks from the rate lines; each law failing on its own mutant."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from tensor24.decoder import books, clocks, records

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"
HEADER = {"kind": "header", "record": "tensor24", "major": 1, "minor": 0}
END = {"kind": "end", "rounds": 1, "digest": "", "undone": 0, "exact": 1}
DIGITS = (
    sys.int_info.default_max_str_digits
)  # the interpreter's bound on a whole number's digits, which the tool lifts


def holding(train, windings, kept=(0, 0)):
    """One train's holding at a click: its windings and its kept, before and after."""
    return {"train": train, "windings": list(windings), "kept": list(kept)}


def click(round_, site, taken=(), laid=(), ends=()):
    """A whole click at the count of its round, with its books at the click, or at its two ends."""
    return {
        "kind": "whole",
        "round": round_,
        "site": site,
        "count": round_,
        "train": 0,
        "taken": list(taken),
        "laid": list(laid),
        "ends": list(ends),
    }


def end_of(site, taken, laid):
    """One end of a whole click that takes at both, with its books."""
    return {"site": site, "spoke": 0, "taken": taken, "laid": laid, "push": [0, 0, 0]}


def rate(round_, site, count, k):
    return {"kind": "rate", "round": round_, "site": site, "count": count, "dial": 0, "k": k}


def without(line, key):
    return {name: value for name, value in line.items() if name != key}


# three windings of train 1 and one kept laid as four of train 0; a pair of train 0 taken at both ends into train 1
TAKE = click(1, 0, [holding(1, (7, 4), (3, 2))], [holding(0, (0, 4))])
PAIR = click(
    1,
    0,
    ends=[
        end_of(0, [holding(0, (5, 0), (0, 1))], [holding(1, (0, 4))]),
        end_of(1, [holding(0, (5, 0))], [holding(1, (0, 5))]),
    ],
)


def text(lines):
    """A file of JSON Lines: one JSON object a line."""
    return "".join((line if isinstance(line, str) else json.dumps(line)) + "\n" for line in lines)


NO_JSON = "line 2 is no JSON object with its kind"
BROKEN = {  # each broken record's file, the guard without which it would be read or would raise, and its cause
    "a line that is no JSON": (text([HEADER, "no json", END]), "jsoned", NO_JSON),
    "a line with no kind": (text([HEADER, {"round": 1, "site": 0}, END]), "jsoned", NO_JSON),
    "a key twice": (
        text([HEADER, '{"kind": "rate", "round": 1, "round": 1, "site": 0}', END]),
        "jsoned",
        NO_JSON,
    ),
    "a line nested past the interpreter's depth": (
        text([HEADER, "[" * 100_000 + "]" * 100_000, END]),
        "jsoned",
        NO_JSON,
    ),
    "an empty file": ("", "framed", "the record holds no header and end"),
    "a first line that is no header": (
        text([{"kind": "turnover", "major": 1, "round": 1, "site": 0}, END]),
        "headed",
        "the first line is no header",
    ),
    "no major": (text([{"kind": "header"}, END]), "majored", "the header holds no major version"),
    "an unknown major": (
        text([{**HEADER, "major": 1 + 1}, END]),
        "majored",
        "the major version 2 is unknown",
    ),
    "no end": (text([HEADER, TAKE]), "ended", "the last line is no end"),
    "an unknown kind": (
        text([HEADER, {"kind": "chime", "round": 1, "site": 0}, END]),
        "kinded",
        "the line kinds ['chime'] are unknown",
    ),
    "an event without its site": (
        text([HEADER, {"kind": "whole", "round": 1}, END]),
        "placed",
        "line 2 stands at no whole round and site",
    ),
    "a float where a whole number stands": (
        text([HEADER, click(1, 0, [holding(1, (7.5, 4.5))]), END]),
        "shaped",
        "line 2's taken has not its shape in the schema",
    ),
    "a truth value where a whole number stands": (
        text([HEADER, rate(1, 0, True, 1), END]),
        "shaped",
        "line 2's count has not its shape in the schema",
    ),
    "NaN where a whole number stands": (
        text([HEADER, '{"kind": "rate", "round": 1, "site": 0, "count": 1, "k": NaN}', END]),
        "shaped",
        "line 2's k has not its shape in the schema",
    ),
    "a row of another length": (
        text([HEADER, click(1, 0, [{"train": 1, "windings": [7], "kept": [0, 0]}]), END]),
        "shaped",
        "line 2's taken has not its shape in the schema",
    ),
    "a float in the header": (
        text([{**HEADER, "minor": 0.5}, END]),
        "shaped",
        "line 1's minor has not its shape in the schema",
    ),
    "a click booked at the click and again at its ends": (
        text([HEADER, {**PAIR, "taken": TAKE["taken"]}, END]),
        "booked",
        "line 2's whole click books at the click and again at its ends",
    ),
    "a click with one end": (
        text([HEADER, click(1, 0, ends=PAIR["ends"][:1]), END]),
        "booked",
        "line 2's whole click's ends number 1, where the schema holds both or none",
    ),
    "the events out of order": (
        text([HEADER, click(1 + 1, 0), click(1, 0), END]),
        "ordered",
        "the events stand out of the schema's order",
    ),
}


def unread(path, guards, reader=records.read):
    """The file at path is not read, with its cause named, and nothing raised."""
    try:
        held, cause = reader(path, guards)
    except Exception:
        return False
    return held is None and bool(cause)


@pytest.mark.parametrize("name", sorted(BROKEN))
def test_a_broken_record_is_not_read_with_its_own_cause_and_fails_without_its_guard(tmp_path, name):
    raw, guard, cause = BROKEN[name]
    path = tmp_path / "record.jsonl"
    path.write_text(raw, encoding="utf-8")
    assert records.read(str(path)) == (None, cause)
    assert not unread(str(path), tuple(g for g in records.GUARDS if g.__name__ != guard))


def test_a_record_of_the_schema_reads_its_lines_split_at_the_line_feed_alone(tmp_path):
    label = "a\u2028b\u0085c\u2029d"
    lines = [HEADER, TAKE, PAIR, {**rate(1, 0, 1, 1), "note": label}, END]
    # each line ends in a return and a line feed, and holds returns as white space between its tokens
    texts = [json.dumps(line, ensure_ascii=False).replace(", ", ",\r ") + "\r\n" for line in lines]
    path, alone = tmp_path / "record.jsonl", tmp_path / "alone.jsonl"
    path.write_text("".join(texts), encoding="utf-8")
    alone.write_text(text([HEADER]), encoding="utf-8")
    record, cause = records.read(str(path))
    assert cause == "" and record is not None and record.of("whole") == [TAKE, PAIR]
    assert record.of("rate")[0]["note"] == label
    assert records.read(str(alone)) == (None, "the record holds no header and end")
    assert records.read(str(tmp_path / "absent.jsonl")) == (None, "the record's file is absent")


def test_a_line_with_no_kind_and_the_order_by_site_and_kind(tmp_path):
    kindless = text([HEADER, {"round": 1, "site": 0}, END])
    by_site = text([HEADER, rate(1, 1, 1, 1), rate(1, 0, 1, 1), END])
    turnover = {"kind": "turnover", "round": 1, "site": 0, "count": 1, "q": 1, "x": 0}
    by_kind = text([HEADER, turnover, rate(1, 0, 1, 1), END])
    got = []
    for raw in (kindless, by_site, by_kind):
        path = tmp_path / "record.jsonl"
        path.write_text(raw, encoding="utf-8")
        got.append(records.read(str(path))[1])
    assert got == [NO_JSON, "the events stand out of the schema's order", ""]


def ledger(round_, held):
    """The ledger's lines of one round: per train, its wind after the step and after the clicks."""
    return [
        {"round": round_, "at": at, "train": train, "wind": wind}
        for train, pair in held.items()
        for at, wind in zip(records.AT, pair, strict=True)
    ]


GOOD = ledger(
    1, {0: (0, 4), 1: (10, 6)}
)  # TAKE's round: the wind over every train 10 after the step and the clicks
LEDGER_BROKEN = {  # each broken ledger's lines after GOOD's four, the guard without which it would be read or raise
    "a blank line": ("", "objects", "the ledger's line 5 is no JSON object"),
    "a line that is no JSON": ("no json", "objects", "the ledger's line 5 is no JSON object"),
    "a line that is a list": ([1, "step", 0, 4], "objects", "the ledger's line 5 is no JSON object"),
    "a line without its at": (
        {"round": 1, "train": 0, "wind": 4},
        "standing",
        "the ledger's line 5 stands at no whole round and train, after the step or the clicks",
    ),
    "a line after neither the step nor the clicks": (
        {"round": 1, "at": "lay", "train": 0, "wind": 4},
        "standing",
        "the ledger's line 5 stands at no whole round and train, after the step or the clicks",
    ),
    "a wind that is no whole number": (
        {"round": 1 + 1, "at": "step", "train": 0, "wind": 4.5},
        "fitted",
        "the ledger's line 5 holds a field that has not its shape in the schema",
    ),
    "a line at the place of an earlier one": (
        GOOD[0],
        "once",
        "the ledger's line 5 stands at the round, the at and the train of an earlier line",
    ),
}


@pytest.mark.parametrize("name", sorted(LEDGER_BROKEN))
def test_a_broken_ledger_is_not_read_with_its_own_cause_and_fails_without_its_guard(tmp_path, name):
    line, guard, cause = LEDGER_BROKEN[name]
    path = tmp_path / "ledger.jsonl"
    path.write_text(text([*GOOD, line]), encoding="utf-8")
    assert records.read_ledger(str(path)) == (None, cause)
    kept = tuple(g for g in records.LEDGER_GUARDS if g.__name__ != guard)
    assert not unread(str(path), kept, records.read_ledger)
    assert records.read_ledger(str(tmp_path / "absent.jsonl")) == (None, "the ledger's file is absent")


def read(lines, tmp_path):
    """A record of the given lines, read."""
    path = tmp_path / "record.jsonl"
    path.write_text(text(lines), encoding="utf-8")
    return records.read(str(path))[0]


def test_the_books_close_at_each_end_and_the_verdict(tmp_path):
    one_open = click(1, 0, ends=[PAIR["ends"][0], end_of(1, [holding(0, (5, 0))], [holding(1, (0, 4))])])
    twisted = click(
        1,
        0,
        ends=[
            end_of(0, [holding(0, (5, 0))], [holding(1, (0, 6))]),
            end_of(1, [holding(0, (5, 0))], [holding(1, (0, 4))]),
        ],
    )
    assert books.closes(PAIR) and not books.closes(one_open) and not books.closes(twisted)
    opened = click(1, 0, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))])
    assert books.row_15(read([HEADER, opened, END], tmp_path), GOOD)["kind"] == "NOT SHOWN"
    absent = books.row_15(read([HEADER, TAKE, END], tmp_path), None)
    assert absent["kind"] == "NOT READ" and absent["cause"].startswith("the ledger is absent")


def test_the_wind_over_every_train_round_by_round(tmp_path):
    pair = books.row_15(read([HEADER, PAIR, END], tmp_path), ledger(1, {0: (10, 1), 1: (0, 9)}))
    two = read([HEADER, TAKE, {**TAKE, "round": 1 + 1, "count": 1 + 1}, END], tmp_path)
    second = ledger(1 + 1, {0: (4, 8), 1: (6, 2)})
    over = ledger(1, {0: (0, 5), 1: (10, 6)})
    under = ledger(1, {0: (0, 3), 1: (10, 6)})
    swapped = [
        *over,
        *ledger(1 + 1, {0: (4, 7), 1: (6, 2)}),
    ]  # one more at the first round, one less at the second
    assert pair["kind"] == "SHOWN" and books.row_15(two, [*GOOD, *second])["kind"] == "SHOWN"
    assert all(
        books.row_15(two, held)["kind"] == "NOT SHOWN"
        for held in ([*over, *second], [*under, *second], swapped)
    )


def test_a_split_click_moves_wind_between_trains_and_the_ledger_reads_at_every_round_with_a_click(
    tmp_path,
):
    split = {"kind": "split", "round": 1 + 1, "site": 0, "count": 1 + 1}
    record = read([HEADER, TAKE, split, END], tmp_path)
    moved = [*GOOD, *ledger(1 + 1, {0: (4, 1), 1: (6, 9)})]
    some = books.row_15(record, GOOD)
    clicks_alone = books.row_15(record, [line for line in moved if line["at"] == "clicks"])
    windless = books.row_15(record, [without(line, "wind") for line in moved])
    parted = books.row_15(record, [line for line in moved if line["at"] == "step" or line["train"] == 0])
    assert books.row_15(record, moved)["kind"] == "SHOWN" and some["kind"] == "NOT READ"
    assert some["cause"].endswith("the ledger's lines are read at 1 of 2 rounds with a click")
    assert clicks_alone["kind"] == windless["kind"] == parted["kind"] == "NOT READ"


LACKING = {  # a whole click that lacks a field its books are read from (Sofer's G1)
    "its ends": without(TAKE, "ends"),
    "its taken": without(TAKE, "taken"),
    "an end's laid": click(1, 0, ends=[PAIR["ends"][0], without(PAIR["ends"][1], "laid")]),
    "a holding's kept": click(1, 0, [without(holding(1, (7, 4)), "kept")], [holding(0, (0, 4))]),
}


@pytest.mark.parametrize("name", sorted(LACKING))
def test_a_whole_click_that_lacks_a_field_of_its_books_reads_the_row_not_read(tmp_path, name):
    verdict = books.row_15(read([HEADER, LACKING[name], END], tmp_path), GOOD)
    cause = "the whole click at round 1, site 0 lacks a field its books are read from"
    assert verdict["kind"] == "NOT READ" and verdict["cause"] == cause


def ticked(seed, beats=60):
    """A Node-clock's k at each beat, and its rate lines: at its first beat and wherever k changes."""
    ks = [int(k) for k in np.random.default_rng(seed).integers(0, 1 + 1, size=beats)]
    lines = [(count, k) for count, k in enumerate(ks, start=1) if count == 1 or ks[count - 1 - 1] != k]
    return ks, lines


def test_the_ticks_from_a_record_whose_counts_are_not_its_rounds(tmp_path):
    lines = [
        rate(1, 0, 1, 1),
        rate(1 + 1, 1, 1, 0),
        rate(1 + 1 + 1, 1, 1 + 1, 1),
        rate(4, 0, 1 + 1, 0),
        rate(6, 0, 4, 1),
    ]
    held, counts = clocks.stretches(read([HEADER, *lines, END], tmp_path)), (0, 1, 1 + 1, 1 + 1 + 1, 4)
    assert [clocks.ticks_to(held[0], c) for c in counts] == [0, 1, 1, 1, 1 + 1]
    assert [clocks.ticks_to(held[1], c) for c in (1, 1 + 1)] == [0, 1]


def test_the_ticks_are_not_read_where_the_rate_lines_stand_from_no_first_beat():
    unread_lines = {
        "the count is no whole number from 0": [([(1, 1)], -1), ([(1, 1)], True), ([(1, 1)], None)],
        "its Node-clock holds no rate line": [([], 1)],
        "a rate line of its Node-clock holds no whole count and k": [([(1, None)], 1), ([(1.0, 1)], 1)],
        "its Node-clock's first rate line stands at no first beat": [([(1 + 1, 1)], 1 + 1)],
        "its Node-clock's rate lines do not rise in count": [([(1, 1), (1, 0)], 1 + 1)],
    }
    for cause, cases in unread_lines.items():
        assert all(
            clocks.unread(lines, c) == cause and clocks.ticks_to(lines, c) is None for lines, c in cases
        )


def law_books(tmp_path):
    broken = click(1, 0, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))])
    return books.closes(TAKE) and not books.closes(broken)


def law_ends(tmp_path):
    broken = click(1, 0, ends=[end_of(0, [holding(0, (5, 0))], [holding(1, (0, 4))])])
    return books.closes(PAIR) and not books.closes(broken)


def law_ledger(tmp_path):
    record = read([HEADER, TAKE, END], tmp_path)
    over = ledger(1, {0: (0, 5), 1: (10, 6)})
    return (
        books.row_15(record, GOOD)["kind"] == "SHOWN"
        and books.row_15(record, over)["kind"] == "NOT SHOWN"
    )


def law_nothing(tmp_path):
    record = read([HEADER, rate(1, 0, 1, 1), END], tmp_path)
    verdict = books.row_15(record, ledger(1, {0: (0, 0)}))
    return verdict == {"kind": "NOT READ", "cause": "no whole click", "first": verdict["first"]}


def law_lacking(tmp_path):
    """A whole click that lacks its taken reads the row not read, and nothing is raised."""
    try:
        verdict = books.row_15(read([HEADER, LACKING["its taken"], END], tmp_path), GOOD)
    except KeyError:
        return False
    return verdict["kind"] == "NOT READ"


def law_ticks(tmp_path):
    held = []
    for seed in (0, 1, 1 + 1):
        ks, lines = ticked(seed)
        held += [clocks.ticks_to(lines, count) == sum(ks[:count]) for count in range(1, len(ks) + 1)]
    return all(held)


def law_first_beat(tmp_path):
    return clocks.ticks_to([(1 + 1, 1)], 1 + 1) is None


def law_line_feed(tmp_path):
    path = tmp_path / "record.jsonl"
    path.write_text(
        text([HEADER, json.dumps({**rate(1, 0, 1, 1), "note": "a\u2028b"}, ensure_ascii=False), END])
    )
    return records.read(str(path))[1] == ""


LAWS = {  # each law, and its mutant: one function of the decoder replaced
    "the books close, windings and kept together": (
        law_books,
        books,
        "gained",
        lambda hs: sum(h["windings"][1] - h["windings"][0] for h in hs),
    ),
    "a pair into light's books close at each end": (law_ends, books, "parts", lambda click: [click]),
    "the wind over every train agrees after the clicks and after the step": (
        law_ledger,
        books,
        "second_reading",
        lambda record, ledger: {"rounds with a click": 1, "read": 1, "agree": 1},
    ),
    "a record with no whole click reads not read": (law_nothing, books, "unread", lambda first: False),
    "a click that lacks a field of its books reads not read": (
        law_lacking,
        books,
        "legible",
        lambda click: True,
    ),
    "the ticks counted from the rate lines": (
        law_ticks,
        clocks,
        "ticks_to",
        lambda lines, count: sum(k for c, k in lines if c <= count),
    ),
    "the ticks read from the first beat alone": (
        law_first_beat,
        clocks,
        "unread",
        lambda lines, count: "",
    ),
    "the lines split at the line feed alone": (
        law_line_feed,
        records,
        "lines_of",
        lambda path: (
            [records.parsed(t) for t in Path(path).read_text(encoding="utf-8").splitlines()],
            "",
        ),
    ),
}


@pytest.mark.parametrize("name", sorted(LAWS))
def test_each_law_of_the_readings_holds_and_fails_on_its_mutant(tmp_path, monkeypatch, name):
    law, module, attribute, mutant = LAWS[name]
    assert law(tmp_path)
    monkeypatch.setattr(module, attribute, mutant)
    assert not law(tmp_path)


def tool(*args):
    return subprocess.run(
        [sys.executable, "-I", str(TOOL), *map(str, args)], capture_output=True, text=True
    )


def test_the_tool_reads_names_and_raises_nothing_and_lifts_the_digits(tmp_path):
    record, good = tmp_path / "record.jsonl", tmp_path / "ledger.jsonl"
    record.write_text(text([HEADER, TAKE, rate(1, 0, 1, 1), END]), encoding="utf-8")
    good.write_text(text(GOOD), encoding="utf-8")
    wide = tmp_path / "wide.jsonl"
    number = (
        '{"kind": "rate", "round": 1, "site": 0, "count": 1, "dial": ' + "9" * (DIGITS + 1) + ', "k": 1}'
    )
    wide.write_text(text([HEADER, number, END]), encoding="utf-8")
    bound = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(DIGITS)
    try:
        assert records.read(str(wide)) == (None, NO_JSON)
    finally:
        sys.set_int_max_str_digits(bound)
    runs = [tool(), tool(record, good), tool(record, tmp_path / "absent.jsonl"), tool(wide)]
    assert runs[0].returncode == 1 + 1 and runs[0].stderr.startswith("usage:") and runs[0].stdout == ""
    assert all(run.returncode == 0 and run.stderr == "" for run in runs[1:])
    assert "'kind': 'SHOWN'" in runs[1].stdout and "1 read, 0 not read" in runs[1].stdout
    assert "the ledger's file is absent" in runs[1 + 1].stdout and runs[-1].stdout.startswith("row 15")
