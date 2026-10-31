"""Tensor24's decoder: a record and its ledger read under the schema's rules, each broken one not read with its own cause
and nothing raised; row 15's two readings; each law failing on its own mutant; schema 1.3's click lines read, listed and counted."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.decoder import books, clicks, records, shadow
from tensor24.record import schema

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"
DIGITS = (
    sys.int_info.default_max_str_digits
)  # the interpreter's bound on a whole number's digits, the tool lifts it
TRAINS = [{"index": t, "label": f"train {t}", "kinds": [0], "part": 1, "winding": 1} for t in (0, 1)]
WOUND = dict.fromkeys(range(3), 1)  # each train's winding by its index: TRAINS', and train 2's at 1
HEADER = {"kind": "header", "record": "tensor24", "major": 1, "minor": 1, "trains": TRAINS}
THIRD = {
    **HEADER,
    "trains": [*TRAINS, {**TRAINS[1], "index": 2, "label": "train 2"}],
}  # train 2's card added
BOARD = {**HEADER, "sides": [1 + 1, 1, 1]}  # a board of two sites on its x axis, and six Spokes
END = {"kind": "end", "rounds": 6, "undone": 0, "exact": 1}
H, B, E = HEADER, BOARD, END  # short names for the tables below


def holding(train, windings, kept=(0, 0)):
    """One train's holding at a click: its windings and its kept, before and after."""
    return {"train": train, "windings": list(windings), "kept": list(kept)}


def click(round_, site, taken=(), laid=(), ends=(), train=0):
    """A whole click of a train at the count of its round, with its books at the click, or at its two ends."""
    place = {"kind": "whole", "round": round_, "site": site, "count": round_, "train": train}
    return place | {"taken": list(taken), "laid": list(laid), "ends": list(ends)}


def end_of(site, taken, laid):
    """One end of a whole click that takes at both, with its books."""
    return {"site": site, "spoke": 0, "taken": taken, "laid": laid, "push": [0, 0, 0]}


def rate(round_, site, count, k):
    return {"kind": "rate", "round": round_, "site": site, "count": count, "dial": 0, "k": k}


def without(line, key):
    return {name: value for name, value in line.items() if name != key}


# three windings and one kept of train 1 laid as four of train 0; a pair of train 0 taken at both ends into train 1
TAKE = click(1, 0, [holding(1, (7, 4), (3, 2))], [holding(0, (0, 4))], train=1)
ENDED = [
    end_of(0, [holding(0, (5, 0), (0, 1))], [holding(1, (0, 4))]),
    end_of(1, [holding(0, (5, 0))], [holding(1, (0, 5))]),
]
PAIR = click(1, 0, ends=ENDED)


def text(lines):
    """A file of JSON Lines: one JSON object a line."""
    return "".join((line if isinstance(line, str) else json.dumps(line)) + "\n" for line in lines)


NO_JSON = "line 2 is no JSON object with its kind"
SHAPE, LINE1 = (
    "line 2's {} has not its shape in the schema",
    "line 1's {} has not its shape in the schema",
)
UNPLACED, ORDER = (
    "line 2 stands at no whole round and site",
    "the events stand out of the schema's order",
)
TWICE = "line 2's whole click books at the click and again at its ends"
ENDS = "line 2's whole click's ends number {}, where the schema holds both or none"
KEYED = '{"kind": "rate", "round": 1, "round": 1, "site": 0}'
NAN = '{"kind": "rate", "round": 1, "site": 0, "count": 1, "k": NaN}'
# ten million deep, past any stack: 3.14.9 on CI reads a hundred thousand, 3.14.6 about forty thousand
DEEP, NESTS = "[" * 10**7 + "]" * 10**7, "line 2 nests past the interpreter's depth"
OFF_ROUND, OFF_SITE = (
    "line 2 stands at round 7, off the record's rounds 1 to 6",
    "line 2 names site 2, off the board of sides [2, 1, 1]",
)
OFF_END = "line 2 names site 5, off the board of sides [2, 1, 1]"
OFF_SPOKE, EARLY = (
    "line 2 names Spoke 6, off the board's Spokes 0 to 5",
    "line 2 holds the count 0, before the first beat",
)
SPOKED = {**PAIR, "ends": [ENDED[0], {**ENDED[1], "spoke": 6}]}
EDGED = {**PAIR, "ends": [ENDED[0], {**ENDED[1], "spoke": 5}]}  # the board's last site and last Spoke
BROKEN = {  # each broken record's lines, the guard without which it would be read or would raise, and its cause
    "a line that is no JSON": ([H, "no json", E], "jsoned", NO_JSON),
    "a line with no kind": ([H, {"round": 1, "site": 0}, E], "jsoned", NO_JSON),
    "a key twice": ([H, KEYED, E], "jsoned", NO_JSON),
    "a line nested past the interpreter's depth": ([H, DEEP, E], "jsoned", NESTS),
    "an empty file": ([], "framed", "the record holds no header and end"),
    "a first line that is no header": (
        [{**rate(1, 0, 1, 1), "major": 1}, E],
        "headed",
        "the first line is no header",
    ),
    "no major": ([{"kind": "header"}, E], "majored", "the header holds no major version"),
    "an unknown major": ([{**H, "major": 1 + 1}, E], "majored", "the major version 2 is unknown"),
    "no end": ([H, TAKE], "ended", "the last line is no end"),
    "an unknown kind": (
        [H, {"kind": "chime", "round": 1, "site": 0}, E],
        "kinded",
        "the line kinds ['chime'] are unknown",
    ),
    "an event without its site": ([H, {"kind": "whole", "round": 1}, E], "placed", UNPLACED),
    "an event without its round": ([H, without(rate(1, 0, 1, 1), "round"), E], "placed", UNPLACED),
    "a float for a whole number": (
        [H, click(1, 0, [holding(1, (7.5, 4.5))]), E],
        "shaped",
        SHAPE.format("taken"),
    ),
    "a truth value for a whole number": ([H, rate(1, 0, True, 1), E], "shaped", SHAPE.format("count")),
    "NaN for a whole number": ([H, NAN, E], "shaped", SHAPE.format("k")),
    "a row of another length": (
        [H, click(1, 0, [holding(1, (7,))]), E],
        "shaped",
        SHAPE.format("taken"),
    ),
    "a float in the header": ([{**H, "minor": 0.5}, E], "shaped", LINE1.format("minor")),
    "a label that is no label": ([{**H, "engine": [1]}, E], "shaped", LINE1.format("engine")),
    "an end's digest that is no label": ([H, {**E, "digest": 1}], "shaped", SHAPE.format("digest")),
    "null in an unnamed field": ([H, {**TAKE, "note": None}, E], "shaped", SHAPE.format("note")),
    "a float in an unnamed field": ([H, {**TAKE, "note": 0.5}, E], "shaped", SHAPE.format("note")),
    "a float in an unnamed row": ([H, {**TAKE, "note": [1, [0.5]]}, E], "shaped", SHAPE.format("note")),
    "a round past the end's rounds": ([H, rate(7, 0, 1, 1), E], "valued", OFF_ROUND),
    "a round before the first": (
        [H, rate(0, 0, 1, 1), E],
        "valued",
        "line 2 stands at round 0, off the record's rounds 1 to 6",
    ),
    "an end at a site off the board": (
        [B, {**PAIR, "ends": [ENDED[0], {**ENDED[1], "site": 5}]}, E],
        "valued",
        OFF_END,
    ),
    "a site off the board": ([B, rate(1, 1 + 1, 1, 1), E], "valued", OFF_SITE),
    "an end at a Spoke off the board": ([B, SPOKED, E], "valued", OFF_SPOKE),
    "a count before the first beat": ([H, rate(1, 0, 0, 1), E], "valued", EARLY),
    "a click booked at the click and its ends": (
        [H, {**PAIR, "taken": TAKE["taken"]}, E],
        "booked",
        TWICE,
    ),
    "a pair booked again in its laid": ([H, {**PAIR, "laid": [holding(1, (0, 9))]}, E], "booked", TWICE),
    "a click with one end": ([H, click(1, 0, ends=ENDED[:1]), E], "booked", ENDS.format(1)),
    "a click with three ends": ([H, click(1, 0, ends=[*ENDED, ENDED[1]]), E], "booked", ENDS.format(3)),
    "the events out of order": ([H, click(1 + 1, 0), click(1, 0), E], "ordered", ORDER),
}


def unread(path, guards, reader=records.read):
    """The file at path is not read, with its cause named, and nothing raised."""
    try:
        held, cause = reader(path, guards)
    except Exception:
        return False
    return held is None and bool(cause)


def cause_of(lines, tmp_path):
    """The cause a record of the given lines is not read, or nothing."""
    path = tmp_path / "record.jsonl"
    path.write_text(text(lines), encoding="utf-8")
    return records.read(str(path))[1]


def test_the_record_is_read_by_its_schema_and_each_guard_refuses_its_own_broken_record(tmp_path):
    """The reader's one law: a record of the schema reads; each broken one is refused by its own guard, named, and read without that guard."""
    for name in sorted(BROKEN):
        lines, guard, cause = BROKEN[name]
        assert cause_of(lines, tmp_path) == cause
        kept = tuple(g for g in records.GUARDS if g.__name__ != guard)
        assert not unread(str(tmp_path / "record.jsonl"), kept)
    assert cause_of([H], tmp_path) == "the record holds no header and end"
    assert cause_of([{**H, "major": True}, E], tmp_path) == "the header holds no major version"
    halves = {**rate(1, 0, 1, 1), "count": 0.5, "k": 0.5}
    assert cause_of([H, halves, E], tmp_path) == SHAPE.format("count")
    absent, nul = records.read(str(tmp_path / "absent.jsonl")), records.read(str(tmp_path) + "/a\x00b")
    assert absent == (None, "the record's file is absent") and nul == (
        None,
        "the record's file cannot be read",
    )
    label = "a\u2028b\u0085c\u2029d"
    lines = [H, PAIR, TAKE, {**rate(1, 0, 1, 1), "note": label}, E]
    # each line ends in a return and a line feed, and holds returns as white space between its tokens
    texts = [json.dumps(line, ensure_ascii=False).replace(", ", ",\r ") + "\r\n" for line in lines]
    path = tmp_path / "record.jsonl"
    path.write_text("".join(texts), encoding="utf-8")
    record, cause = records.read(str(path))
    assert cause == "" and record is not None and record.of("whole") == [PAIR, TAKE]
    assert record.of("rate")[0]["note"] == label
    assert cause_of([B, EDGED, E], tmp_path) == ""
    one, zero = {**TAKE, "train": 1}, {**TAKE, "train": 0}
    cases = [
        [{"round": 1, "site": 0}],
        [rate(1, 1, 1, 1), rate(1, 0, 1, 1)],
        [zero, rate(1, 0, 1, 1)],
        [rate(1, 0, 1, 1), zero],
    ]
    got = [cause_of([H, *lines, E], tmp_path) for lines in [*cases, [one, zero], [zero, one]]]
    assert got == [NO_JSON, ORDER, "", ORDER, ORDER, ""]
    # Schema 1.2 retires the turnover line: the reader names it among the kinds it holds not, as any such line.
    turnover = {"kind": "turnover", "round": 1, "site": 0, "count": 1, "q": 1, "x": 0}
    assert cause_of([H, turnover, E], tmp_path) == "the line kinds ['turnover'] are unknown"


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
STANDS = "the ledger's line 5 stands at no whole round and train, after the step or the clicks"
OBJECT = "the ledger's line 5 is no JSON object"
LEDGER_BROKEN = {  # each broken ledger's line after GOOD's four, the guard without which it would be read or raise
    "a blank line": ("", "objects", OBJECT),
    "a line that is no JSON": ("no json", "objects", OBJECT),
    "a line that is a list": ([1, "step", 0, 4], "objects", OBJECT),
    "a line without its at": ({"round": 1, "train": 0, "wind": 4}, "standing", STANDS),
    "a line without its round": ({"at": "step", "train": 0, "wind": 4}, "standing", STANDS),
    "a line without its train": ({"round": 1, "at": "step", "wind": 4}, "standing", STANDS),
    "a line after neither the step nor the clicks": (
        {"round": 1, "at": "lay", "train": 0, "wind": 4},
        "standing",
        STANDS,
    ),
    "a wind that is no whole number": (
        {"round": 1 + 1, "at": "step", "train": 0, "wind": 4.5},
        "fitted",
        "the ledger's line 5 holds a field that has not its shape in the schema",
    ),
    "a line at the place of an earlier one": (
        GOOD[0],
        "once",
        "the ledger's line 5 stands at the round, the at, the site and the train of an earlier line",
    ),
}


def test_a_broken_ledger_is_not_read_with_its_own_cause_and_fails_without_its_guard(tmp_path):
    for name in sorted(LEDGER_BROKEN):
        line, guard, cause = LEDGER_BROKEN[name]
        path = tmp_path / "ledger.jsonl"
        path.write_text(text([*GOOD, line]), encoding="utf-8")
        assert records.read_ledger(str(path)) == (None, cause)
        kept = tuple(g for g in records.LEDGER_GUARDS if g.__name__ != guard)
        assert not unread(str(path), kept, records.read_ledger)
        assert records.read_ledger(str(tmp_path / "absent.jsonl")) == (
            None,
            "the ledger's file is absent",
        )


def read(lines, tmp_path):
    """A record of the given lines, read."""
    path = tmp_path / "record.jsonl"
    path.write_text(text(lines), encoding="utf-8")
    return records.read(str(path))[0]


def kind(lines, held, tmp_path):
    """Row 15's verdict's kind on a record of the given lines and a ledger."""
    return books.row_15(read(lines, tmp_path), held)["kind"]


OPEN = {  # a whole click whose holdings sum to nothing and whose books still do not hold the click (the seventh review)
    "no books, q 5": {**click(1, 0, train=1), "q": 5},
    "a take that gains": {**click(1, 0, [holding(1, (4, 8))], [holding(0, (4, 0))], train=1), "q": 4},
    "its own train not taken": {
        **click(1, 0, [holding(0, (4, 0))], [holding(1, (0, 4))], train=1),
        "q": 4,
    },
    "a laid holding that loses": click(
        1, 0, [holding(1, (7, 4))], [holding(0, (0, 5)), holding(2, (2, 0))], train=1
    ),
    "a q that did not leave": {**TAKE, "q": 4},
    "a taken holding that gains": click(
        1, 0, [holding(1, (7, 4)), holding(2, (0, 1))], [holding(0, (0, 1 + 1))], train=1
    ),
    "an end that takes nothing": click(1, 0, ends=[ENDED[0], end_of(1, [], [])]),
}


def test_the_wind_is_read_over_every_train_at_every_round_with_a_click(tmp_path):
    """The ledger's wind, read over every train of the header, round by round, a split click moving it between trains."""
    two = read([H, TAKE, {**TAKE, "round": 1 + 1, "count": 1 + 1}, E], tmp_path)
    second = ledger(1 + 1, {0: (4, 8), 1: (6, 2)})
    over, under = ledger(1, {0: (0, 5), 1: (10, 6)}), ledger(1, {0: (0, 3), 1: (10, 6)})
    swapped = [
        *over,
        *ledger(1 + 1, {0: (4, 7), 1: (6, 2)}),
    ]  # one more at the first round, one less at the second
    paired = ledger(1, {0: (10, 1), 1: (0, 9)})
    assert kind([H, PAIR, E], paired, tmp_path) == "SHOWN"
    assert books.row_15(two, [*GOOD, *second])["kind"] == "SHOWN"
    assert all(
        books.row_15(two, held)["kind"] == "NOT SHOWN"
        for held in ([*over, *second], [*under, *second], swapped)
    )
    no_train = books.row_15(read([{**H, "trains": []}, TAKE, E], tmp_path), GOOD)
    held = [
        ledger(1, {7: (5, 5)}),
        ledger(1, {0: (0, 4)}),
        ledger(1, {1: (10, 10)}),
        [*GOOD, *ledger(1, {7: (5, 5)})],
    ]
    assert kind([H, TAKE, E], GOOD, tmp_path) == "SHOWN"
    assert all(kind([H, TAKE, E], lines, tmp_path) == "NOT READ" for lines in held)
    assert no_train["kind"] == "NOT READ" and no_train["cause"].startswith("the header names no train")
    assert books.second_reading(read([{**H, "trains": []}, TAKE, E], tmp_path), [])["read"] == 0
    record = read([H, TAKE, {"kind": "split", "round": 1 + 1, "site": 0, "count": 1 + 1}, E], tmp_path)
    moved = [*GOOD, *ledger(1 + 1, {0: (4, 1), 1: (6, 9)})]
    some = books.row_15(record, GOOD)
    clicks_alone = books.row_15(record, [line for line in moved if line["at"] == "clicks"])
    windless = books.row_15(record, [*moved[:-1], without(moved[-1], "wind")])
    parted = books.row_15(record, [line for line in moved if line["at"] == "step" or line["train"] == 0])
    assert books.row_15(record, moved)["kind"] == "SHOWN" and some["kind"] == "NOT READ"
    assert (
        some["cause"]
        == "the books close at every whole click; the ledger's lines are read at 1 of 2 rounds with a click"
    )
    assert clicks_alone["kind"] == windless["kind"] == parted["kind"] == "NOT READ"


def lacking(key, at="taken"):
    """TAKE with one holding that lacks a field, or with no field of its own at all."""
    if at == "click":
        return without(TAKE, key)
    return {**TAKE, at: [without(TAKE[at][0], key)]}


LACKING = {  # a whole click that lacks a field its books are read from (Sofer's G1)
    "its ends": lacking("ends", "click"),
    "its taken": lacking("taken", "click"),
    "an end's laid": click(1, 0, ends=[ENDED[0], without(ENDED[1], "laid")]),
    "a holding's kept": lacking("kept"),
    "a holding's windings": lacking("windings"),
    "a holding's train": lacking("train"),
    "a laid holding's kept": lacking("kept", "laid"),
}


def test_the_books_close_where_they_hold_the_click_and_read_not_shown_or_not_read_otherwise(tmp_path):
    """Row 15's one law: the books close at each end where they hold the click they book; else not shown, or not read with the cause."""
    one_open = click(1, 0, ends=[ENDED[0], end_of(1, [holding(0, (5, 0))], [holding(1, (0, 4))])])
    twisted = [
        end_of(0, [holding(0, (5, 0))], [holding(1, (0, 6))]),
        end_of(1, [holding(0, (5, 0))], [holding(1, (0, 4))]),
    ]
    assert books.closes(PAIR, WOUND) and not books.closes(one_open, WOUND)
    assert not books.closes(click(1, 0, ends=twisted), WOUND)
    opened = click(1, 0, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))], train=1)
    assert kind([H, opened, E], GOOD, tmp_path) == "NOT SHOWN"
    absent = books.row_15(read([H, TAKE, E], tmp_path), None)
    assert absent["kind"] == "NOT READ" and absent["cause"].startswith("the ledger is absent")
    for name in sorted(OPEN):
        from_kept = click(1, 0, [holding(1, (0, 0), (5, 1))], [holding(0, (0, 4))], train=1)
        assert books.closes({**TAKE, "q": 1 + 1 + 1}, WOUND) and books.closes(from_kept, WOUND)
        assert books.closes(PAIR, WOUND) and not books.closes(OPEN[name], WOUND)
        held = ledger(1, {0: (4, 4), 1: (6, 6)})
        assert kind([THIRD, OPEN[name], E], held, tmp_path) == "NOT SHOWN"
    for name in sorted(LACKING):
        cause = "the whole click at round 1, site 0 lacks a field its books are read from"
        beside = [
            LACKING[name],
            {**TAKE, "site": 1},
        ]  # beside a click whose books close, the books unnamed
        for some in ([LACKING[name]], beside):
            verdict = books.row_15(read([H, *some, E], tmp_path), GOOD)
            assert verdict["kind"] == "NOT READ" and verdict["cause"] == cause
    opened = click(1, 1, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))], train=1)
    held = ledger(1, {0: (0, 8), 1: (10, 2)})
    both = books.row_15(read([H, LACKING["its taken"], opened, E], tmp_path), held)
    assert both["kind"] == "NOT SHOWN" and "lacks a field its books are read from" in both["cause"]
    one = books.row_15(read([H, TAKE, opened, E], tmp_path), held)
    assert one["kind"] == "NOT SHOWN" and one["cause"].startswith(
        "the books open at 1 of 2 whole clicks read"
    )


def law_books(tmp_path):
    broken = click(1, 0, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))], train=1)
    return books.closes(TAKE, WOUND) and not books.closes(broken, WOUND)


def law_ends(tmp_path):
    return books.closes(PAIR, WOUND) and not books.closes(
        click(1, 0, ends=[end_of(0, [holding(0, (5, 0))], [holding(1, (0, 4))])]), WOUND
    )


def law_ledger(tmp_path):
    over, seven = ledger(1, {0: (0, 5), 1: (10, 6)}), ledger(1, {7: (5, 5)})
    kinds = [kind([H, TAKE, E], held, tmp_path) for held in (GOOD, over, seven)]
    return kinds == ["SHOWN", "NOT SHOWN", "NOT READ"]


def law_nothing(tmp_path):
    verdict = books.row_15(read([H, rate(1, 0, 1, 1), E], tmp_path), ledger(1, {0: (0, 0)}))
    return verdict == {"kind": "NOT READ", "cause": "no whole click", "first": verdict["first"]}


def law_lacking(tmp_path):
    """A whole click that lacks its taken reads the row not read, and nothing is raised."""
    try:
        return kind([H, LACKING["its taken"], E], GOOD, tmp_path) == "NOT READ"
    except KeyError:
        return False


def law_line_feed(tmp_path):
    path = tmp_path / "record.jsonl"
    path.write_text(
        text([H, json.dumps({**rate(1, 0, 1, 1), "note": "a\u2028b"}, ensure_ascii=False), E])
    )
    return records.read(str(path))[1] == ""


LAWS = {  # each law, and its mutant: one function of the decoder replaced
    "the books close, each train's windings at its winding and its kept together": (
        law_books,
        books,
        "gained",
        lambda hs, winding: sum(h["windings"][1] - h["windings"][0] for h in hs),
    ),
    "a pair into light's books close at each end": (law_ends, books, "parts", lambda click: [click]),
    "the wind over every train of the header agrees after the clicks and after the step": (
        law_ledger,
        books,
        "second_reading",
        lambda record, ledger: {"trains": 1, "rounds with a click": 1, "read": 1, "agree": 1},
    ),
    "a record with no whole click reads not read": (law_nothing, books, "unread", lambda first: False),
    "a click that lacks a field of its books reads not read": (
        law_lacking,
        books,
        "unread_books",
        lambda click, winding: "",
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


def test_each_law_of_the_readings_holds_and_fails_on_its_mutant(tmp_path, monkeypatch):
    for name in sorted(LAWS):
        with monkeypatch.context() as patch:
            law, module, attribute, mutant = LAWS[name]
            assert law(tmp_path)
            patch.setattr(module, attribute, mutant)
            assert not law(tmp_path)


def tool(*args):
    return subprocess.run(
        [sys.executable, "-I", str(TOOL), *map(str, args)], capture_output=True, text=True
    )


def test_the_tool_reads_names_and_raises_nothing_and_lifts_the_digits(tmp_path):
    names = ("record", "ledger", "broken", "wide")
    record, good, broken, wide = (tmp_path / f"{name}.jsonl" for name in names)
    number = (
        '{"kind": "rate", "round": 1, "site": 0, "count": 1, "dial": ' + "9" * (DIGITS + 1) + ', "k": 1}'
    )
    for path, lines in zip(
        (record, good, broken, wide),
        ([H, TAKE, rate(1, 0, 1, 1), E], GOOD, [H, "no json", E], [H, number, E]),
        strict=True,
    ):
        path.write_text(text(lines), encoding="utf-8")
    bound = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(DIGITS)
    try:
        assert records.read(str(wide)) == (
            None,
            "line 2 holds a whole number past the interpreter's digits",
        )
    finally:
        sys.set_int_max_str_digits(bound)
    usages = [tool(), tool(broken, broken, broken)]
    shown, absent, lifted, unread_run = (
        tool(*args) for args in ((record, good), (record, tmp_path / "absent.jsonl"), (wide,), (broken,))
    )
    assert all(
        run.returncode == 1 + 1 and run.stdout == "" and run.stderr.startswith("usage:")
        for run in usages
    )
    assert all(run.returncode == 0 and run.stderr == "" for run in (shown, absent, lifted, unread_run))
    assert "'kind': 'SHOWN'" in shown.stdout
    assert "the ledger's file is absent" in absent.stdout and lifted.stdout.startswith("row 15")
    assert unread_run.stdout == f"not read: {NO_JSON}\n"


KIND = {"index": 0, "label": "A1", "dimension": 1, "characters": [1] * 24}  # its trace on each of the 24
CARDS = [{**train, "key": 7, "square": 0} for train in TRAINS]  # the 1.3 cards: key and square flag
THIRTEEN = {**B, "minor": schema.MINOR, "kinds": [KIND], "trains": CARDS}


def clicked(round_, site, train, q, tooth):
    """A click line: at a round and a Node-clock, a train's q, the click tooth's carry signed, and its tooth before and after."""
    return {"kind": "click", "round": round_, "site": site, "train": train, "q": q, "tooth": list(tooth)}


# a pair at the key 7, both teeth born at 3: the giver's tooth carried down one key, the taker's up one
GIVE, TOOK = clicked(1, 0, 0, -1, (3, 6)), clicked(1, 0, 1, 1, (3, 0))
# lines after a 1.3 header, each refused by name: off the order, the schema, the board or its train's card, or twice
REFUSED = [
    ([TOOK, GIVE], ORDER),
    ([{**GIVE, "tooth": [*GIVE["tooth"], 0]}], SHAPE.format("tooth")),
    ([{**GIVE, "site": B["sides"][0]}], OFF_SITE),
    ([{**GIVE, "train": len(CARDS)}], "line 2 names train 2, which no train card names"),
    ([{**GIVE, "q": 0}], "line 2 holds the click's q 0, a tooth that carried no key"),
    ([{**GIVE, "tooth": [-1, 0]}], "line 2 holds the tooth -1, below 0"),
    ([{**GIVE, "tooth": [0, CARDS[0]["key"]]}], "line 2 holds the tooth 7, not below train 0's key 7"),
    ([GIVE, GIVE], "line 3 stands at the round, the site and the train of an earlier click line"),
    ([{**GIVE, "kind": "whole"}], "line 2 holds the whole click's q -1, below 1"),
]


def test_a_record_of_schema_1_3_reads_its_click_lines_and_refuses_a_click_or_a_card_off_the_schema_or_the_board(
    tmp_path,
):
    """Yes: a 1.3 record with a give below 0 and a take, two trains at one place at the teeth 0 and key - 1, reads in
    order. No: each line of REFUSED, and a kind card's characters or a train card's key off its shape, by name."""
    record = read([THIRTEEN, GIVE, TOOK, E], tmp_path)
    assert record is not None and record.of("click") == [GIVE, TOOK] and record.of("whole") == []
    for lines, cause in REFUSED:
        assert cause_of([THIRTEEN, *lines, E], tmp_path) == cause
    halved = {**KIND, "characters": [1, 0.5]}, {**CARDS[0], "key": 0.5}
    assert cause_of([{**THIRTEEN, "kinds": [halved[0]]}, E], tmp_path) == LINE1.format("kinds")
    assert cause_of([{**THIRTEEN, "trains": [halved[1]]}, E], tmp_path) == LINE1.format("trains")


def test_the_click_lines_are_listed_and_counted_per_train_and_site_with_no_verdict_and_the_tool_prints_them(
    tmp_path,
):
    """Yes: on the 1.3 record the lines list in the schema's order; per train and per Node-clock the lines, the given,
    the taken and the net; the places where the sum of q over the trains is not 0 counted; the tool prints the list
    and the counts after the rows and raises nothing. No: a give with no take at its round counts its place as not 0."""
    held = clicks.counted(read([THIRTEEN, GIVE, TOOK, E], tmp_path))
    assert held.lines == [GIVE, TOOK] and held.sites == {0: clicks.Tally(len(held.lines), 1, 1, 0)}
    assert held.trains == {0: clicks.Tally(1, 1, 0, -1), 1: clicks.Tally(1, 0, 1, 1)}
    assert (held.places, held.nonzero) == (1, 0)
    more = clicks.counted(read([THIRTEEN, GIVE, TOOK, {**GIVE, "round": E["rounds"]}, E], tmp_path))
    assert (more.places, more.nonzero) == (len({(e["round"], e["site"]) for e in more.lines}), 1)
    run = tool(tmp_path / "record.jsonl")  # the record read last, as read() wrote it
    assert run.returncode == 0 and run.stderr == "" and run.stdout.startswith("row 15")
    lines = run.stdout.splitlines()
    assert "the click lines: 3" in lines and "  round 6, site 0, train 0: q -1, tooth [3, 6]" in lines
    assert "train 0: 2 lines, given 2, taken 0, net -2" in lines
    assert "site 0: 3 lines, given 2, taken 1, net -1" in lines
    assert "the sum of q over the trains at a round and site: not 0 at 1 of 2 places" in lines


def test_the_click_world_reads_the_books_no_own_count_and_no_cone_where_none_could_be_outside(tmp_path):
    """Yes: q summing to 0 at every place, the books SHOWN; D6 and D7 not read, the act holding no clock's own count and
    every 1.3 clock at its Node-clock; at round 2, the ring's diameter, no line could stand outside the cone, not read.
    No: a round's two places cancelling, books NOT SHOWN; no q, not read; cone NOT SHOWN; no click line: NO CLICK, refusal last."""
    # a ring of five sites, its setting laying one gear, at site 0
    lay = json.dumps({"version": 1, "ticks": 6, "gears": [[0, 0, 0, 1, 0, 0]]})
    ring = {**THIRTEEN, "sides": [5, 1, 1], "files": [{"name": "setting.json", "text": lay}]}
    edge = [clicked(2, 2, 0, -1, (3, 6)), clicked(2, 2, 1, 1, (3, 0))]  # t Meshes from the lay
    world = shadow.shadow(read([ring, *edge, E], tmp_path))
    d6, d7 = world[shadow.DURATION]["cause"], world[shadow.TWINS]["cause"]
    assert [v["kind"] for v in world.values()] == ["SHOWN", "NOT READ", "NOT READ", "NOT READ"]
    assert d6 == shadow.NO_COUNT and d7 == shadow.AT_NODE
    apart = [clicked(1, 0, 1, 1, (3, 0)), clicked(1, 2, 0, -1, (3, 6))]  # two sites of one round
    world = shadow.shadow(read([ring, *apart, E], tmp_path))
    held, far = world[shadow.BOOKS]["cause"], world[shadow.CONE]["cause"]
    assert held.startswith("the sum of q over the trains is 1 at round 1, site 0:")
    assert far.startswith("the click line at round 1, site 2 stands outside the lay's cone")
    assert shadow.books(read([ring, without(edge[0], "q"), E], tmp_path))["kind"] == "NOT READ"
    assert {v["kind"] for v in shadow.shadow(read([ring, E], tmp_path)).values()} == {shadow.ABSENT}
    run = tool(tmp_path / "record.jsonl")  # the record of no click line, read last
    last = run.stdout.splitlines()[-1]
    assert run.returncode == 0 and "the click world (the owner's law of 23:4x UTC):" in run.stdout
    assert last.startswith("  the record holds no click line, so no claim") and "light's speed" in last
