"""Tensor24's decoder: a record read under the schema's rules, each broken record not read with its cause named and
nothing raised; row 15's two readings; the ticks from the rate lines; each law failing on its own mutant."""

import json

import numpy as np
import pytest

from tensor24.decoder import books, clocks, records

HEADER = {"kind": "header", "record": "tensor24", "major": 1, "minor": 0}
END = {"kind": "end", "rounds": 1, "digest": "", "undone": 0, "exact": 1}


def holding(train, windings, kept=(0, 0)):
    """One train's holding at a click: its windings and its kept, before and after."""
    return {"train": train, "windings": list(windings), "kept": list(kept)}


def click(round_, site, taken=(), laid=(), ends=()):
    """A whole click with its books at the click, or at its ends."""
    return {
        "kind": "whole",
        "round": round_,
        "site": site,
        "train": 0,
        "taken": list(taken),
        "laid": list(laid),
        "ends": list(ends),
    }


def end_of(site, taken, laid):
    """One end of a whole click that takes at both, with its books."""
    return {"site": site, "spoke": 0, "taken": taken, "laid": laid, "push": [0, 0, 0]}


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
    """A record's file: one JSON object a line."""
    return "".join(json.dumps(line) + "\n" for line in lines)


BROKEN = {  # each broken record's file, and the guard without which it would be read or would raise
    "a line that is no JSON": (text([HEADER]) + "no json\n" + text([END]), "jsoned"),
    "an empty file": ("", "framed"),
    "a first line that is no header": (
        text([{"kind": "turnover", "major": 1, "round": 1, "site": 0}, END]),
        "headed",
    ),
    "no major": (text([{"kind": "header"}, END]), "majored"),
    "an unknown major": (text([{**HEADER, "major": 1 + 1}, END]), "majored"),
    "no end": (text([HEADER, TAKE]), "ended"),
    "an unknown kind": (text([HEADER, {"kind": "chime", "round": 1, "site": 0}, END]), "kinded"),
    "an event without its site": (text([HEADER, {"kind": "whole", "round": 1}, END]), "placed"),
    "the events out of order": (text([HEADER, click(1 + 1, 0), click(1, 0), END]), "ordered"),
}


def unread(path, guards):
    """The record at path is not read, with its cause named, and nothing raised."""
    try:
        record, cause = records.read(path, guards)
    except Exception:
        return False
    return record is None and bool(cause)


@pytest.mark.parametrize("name", sorted(BROKEN))
def test_a_broken_record_is_not_read_with_its_cause_and_fails_without_its_guard(tmp_path, name):
    raw, guard = BROKEN[name]
    path = tmp_path / "record.jsonl"
    path.write_text(raw, encoding="utf-8")
    assert unread(str(path), records.GUARDS)
    assert not unread(str(path), tuple(g for g in records.GUARDS if g.__name__ != guard))


def test_a_record_of_the_schema_reads(tmp_path):
    path = tmp_path / "record.jsonl"
    path.write_text(text([HEADER, TAKE, PAIR, END]), encoding="utf-8")
    record, cause = records.read(str(path))
    assert cause == "" and record is not None and record.of("whole") == [TAKE, PAIR]


def read(lines, tmp_path):
    """A record of the given lines, read."""
    path = tmp_path / "record.jsonl"
    path.write_text(text(lines), encoding="utf-8")
    return records.read(str(path))[0]


def ledger(round_, held):
    """The ledger's lines of one round: per train, its windings after the step and after the clicks."""
    return [
        {"round": round_, "at": at, "train": train, "windings": w}
        for train, pair in held.items()
        for at, w in zip(("step", "clicks"), pair, strict=True)
    ]


def ticked(seed, beats=60):
    """A Node-clock's k at each beat, and its rate lines: at its first beat and wherever k changes."""
    ks = [int(k) for k in np.random.default_rng(seed).integers(0, 1 + 1, size=beats)]
    lines = [(count, k) for count, k in enumerate(ks, start=1) if count == 1 or ks[count - 1 - 1] != k]
    return ks, lines


def law_books(tmp_path):
    broken = click(1, 0, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))])
    return books.closes(TAKE) and not books.closes(broken)


def law_ends(tmp_path):
    broken = click(1, 0, ends=[end_of(0, [holding(0, (5, 0))], [holding(1, (0, 4))])])
    return books.closes(PAIR) and not books.closes(broken)


def law_ledger(tmp_path):
    record = read([HEADER, TAKE, END], tmp_path)
    verdict = books.row_15(record, ledger(1, {0: (0, 4), 1: (10, 7)}))
    return verdict["kind"] == "SHOWN"


def law_nothing(tmp_path):
    record = read([HEADER, {"kind": "rate", "round": 1, "site": 0, "count": 1, "k": 1}, END], tmp_path)
    verdict = books.row_15(record, ledger(1, {0: (0, 0)}))
    return verdict == {"kind": "NOT READ", "cause": "no whole click", "first": verdict["first"]}


def law_ticks(tmp_path):
    held = []
    for seed in (0, 1, 1 + 1):
        ks, lines = ticked(seed)
        held += [clocks.ticks_to(lines, count) == sum(ks[:count]) for count in range(1, len(ks) + 1)]
    return all(held)


LAWS = {  # each law, and its mutant: one function of the decoder replaced
    "the books close, windings and kept together": (
        law_books,
        books,
        "gained",
        lambda hs: sum(h["windings"][1] - h["windings"][0] for h in hs),
    ),
    "a pair into light's books close at each end": (law_ends, books, "parts", lambda click: [click]),
    "the ledger's clicks less its step agree with the clicks": (
        law_ledger,
        books,
        "moved",
        lambda click: {
            h["train"]: h["windings"][1] - h["windings"][0] for p in [click] for h in p["laid"]
        },
    ),
    "a record with no whole click reads not read": (law_nothing, books, "unread", lambda first: False),
    "the ticks counted from the rate lines": (
        law_ticks,
        clocks,
        "ticks_to",
        lambda lines, count: sum(k for c, k in lines if c <= count),
    ),
}


@pytest.mark.parametrize("name", sorted(LAWS))
def test_each_law_of_the_readings_holds_and_fails_on_its_mutant(tmp_path, monkeypatch, name):
    law, module, attribute, mutant = LAWS[name]
    assert law(tmp_path)
    monkeypatch.setattr(module, attribute, mutant)
    assert not law(tmp_path)


# ---- the sixth review's additions (probes/test_decoder_strengthened.py): each kills a mutant the 15 tests let live

CAUSES = {  # each broken record's cause, as records.py names it
    "a line that is no JSON": "line 2 is no JSON object with its kind",
    "an empty file": "the record holds no header and end",
    "a first line that is no header": "the first line is no header",
    "no major": "the header holds no major version",
    "an unknown major": "the major version 2 is unknown",
    "no end": "the last line is no end",
    "an unknown kind": "the line kinds ['chime'] are unknown",
    "an event without its site": "line 2 stands at no whole round and site",
    "the events out of order": "the events stand out of the schema's order",
}


@pytest.mark.parametrize("name", sorted(BROKEN))
def test_a_broken_record_names_its_own_cause(tmp_path, name):
    path = tmp_path / "record.jsonl"
    path.write_text(BROKEN[name][0], encoding="utf-8")
    assert records.read(str(path)) == (None, CAUSES[name])


def rate(round_, site, count, k):
    return {"kind": "rate", "round": round_, "site": site, "count": count, "dial": 0, "k": k}


def test_a_line_with_no_kind_and_the_order_by_site_and_kind(tmp_path):
    kindless = text([HEADER, {"round": 1, "site": 0}, END])
    by_site = text([HEADER, rate(1, 1, 1, 1), rate(1, 0, 1, 1), END])
    by_kind = text([HEADER, {"kind": "turnover", "round": 1, "site": 0, "count": 1, "q": 1, "x": 0}, rate(1, 0, 1, 1), END])
    got = []
    for raw in (kindless, by_site, by_kind):
        path = tmp_path / "record.jsonl"
        path.write_text(raw, encoding="utf-8")
        got.append(records.read(str(path))[1])
    assert got == ["line 2 is no JSON object with its kind", "the events stand out of the schema's order", ""]


def test_the_books_close_at_each_end_and_the_verdict(tmp_path):
    one_open = click(1, 0, ends=[PAIR["ends"][0], end_of(1, [holding(0, (5, 0))], [holding(1, (0, 4))])])
    twisted = click(1, 0, ends=[end_of(0, [holding(0, (5, 0))], [holding(1, (0, 6))]), end_of(1, [holding(0, (5, 0))], [holding(1, (0, 4))])])
    assert books.closes(PAIR) and not books.closes(one_open) and not books.closes(twisted)
    opened = click(1, 0, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))])
    verdict = books.row_15(read([HEADER, opened, END], tmp_path), ledger(1, {0: (0, 4), 1: (10, 7)}))
    assert verdict["kind"] == "NOT SHOWN"
    absent = books.row_15(read([HEADER, TAKE, END], tmp_path), None)
    assert absent["kind"] == "NOT READ" and absent["cause"].startswith("the ledger is absent")


def test_the_ledger_at_the_ends_and_round_by_round(tmp_path):
    pair = books.row_15(read([HEADER, PAIR, END], tmp_path), ledger(1, {0: (10, 0), 1: (0, 9)}))
    again = {**TAKE, "round": 1 + 1}
    two = read([HEADER, TAKE, again, END], tmp_path)
    good = ledger(1, {0: (0, 4), 1: (10, 7)}) + ledger(1 + 1, {0: (4, 8), 1: (7, 4)})
    over = ledger(1, {0: (0, 5), 1: (10, 7)}) + ledger(1 + 1, {0: (4, 8), 1: (7, 4)})
    assert pair["kind"] == "SHOWN" and books.row_15(two, good)["kind"] == "SHOWN"
    assert books.row_15(two, over)["kind"] == "NOT SHOWN"


def test_the_ticks_from_a_record_whose_counts_are_not_its_rounds(tmp_path):
    lines = [rate(1, 0, 1, 1), rate(1 + 1, 1, 1, 0), rate(1 + 1 + 1, 1, 1 + 1, 1), rate(4, 0, 1 + 1, 0), rate(6, 0, 4, 1)]
    held = clocks.stretches(read([HEADER, *lines, END], tmp_path))
    assert [clocks.ticks_to(held[0], c) for c in (1, 1 + 1, 1 + 1 + 1, 4)] == [1, 1, 1, 1 + 1]
    assert [clocks.ticks_to(held[1], c) for c in (1, 1 + 1)] == [0, 1]
