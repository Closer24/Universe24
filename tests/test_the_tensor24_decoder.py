"""Tensor24's decoder: a record and its ledger read under the schema's rules, each broken one not read with its own cause
and nothing raised; the click lines read, listed and counted, and read in the click world."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.decoder import clicks, records, shadow
from tensor24.record import schema

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"
DIGITS = (
    sys.int_info.default_max_str_digits
)  # the interpreter's bound on a whole number's digits, the tool lifts it
KIND = {"index": 0, "label": "A1", "dimension": 1, "characters": [1] * 24}  # its trace on each of the 24
CARD = {"kinds": [0], "part": 1, "winding": 1, "key": 7, "square": 0}  # every edge side's key 7
CARDS = [{"index": t, "label": f"train {t}", **CARD} for t in (0, 1)]
H = {
    "kind": "header",
    "record": "tensor24",
    "version": schema.VERSION,
    "kinds": [KIND],
    "trains": CARDS,
}
B = {**H, "sides": [1 + 1, 1, 1]}  # a board of two sites on its x axis
E = {"kind": "end", "rounds": 6, "undone": 0, "exact": 1}


def met(round_=1, site=0):
    """A meeting at a round and a Node-clock: train 0 gives one quantum to train 1 on their edge, the teeth born at 3."""
    give = {
        "kind": "click",
        "round": round_,
        "site": site,
        "train": 0,
        "q": -1,
        "sides": [[1, -1, 3, 6]],
    }
    return [give, {**give, "train": 1, "q": 1, "sides": [[0, 1, 3, 0]]}]


def without(line, key):
    return {name: value for name, value in line.items() if name != key}


def text(lines):
    """A file of JSON Lines: one JSON object a line."""
    return "".join((line if isinstance(line, str) else json.dumps(line)) + "\n" for line in lines)


GIVE, TOOK = met()
BARE = {
    "kind": "click",
    "round": 1,
    "site": 0,
    "train": 0,
    "q": 1,
}  # a line of no side, which no guard pairs
SENT = {
    **GIVE,
    "sides": [],
    "across": [[0, 1, -1, 3, 6]],
}  # train 0 gives across a Mesh, site 0 to site 1
CROSS = [SENT, {**SENT, "site": 1, "q": 1, "across": [[0, 0, 1, 3, 0]]}]
ENDED = {
    **E,
    "across": [[0, 0, [1, 0], [3, 3]]],
}  # the end's across: the side (0, 0), its places and teeth
NO_JSON, ORDER = "line 2 is no JSON object with its kind", "the events stand out of the schema's order"
SHAPE, LINE1 = (
    "line 2's {} has not its shape in the schema",
    "line 1's {} has not its shape in the schema",
)
UNPLACED, SITE = (
    "line 2 stands at no whole round and site",
    "line 2 names site {}, off the board of sides [2, 1, 1]",
)
KEYED = '{"kind": "click", "round": 1, "round": 1, "site": 0}'
NAN = '{"kind": "click", "round": 1, "site": 0, "train": 0, "q": NaN}'
# ten million deep, past any stack: 3.14.9 on CI reads a hundred thousand, 3.14.6 about forty thousand
DEEP, NESTS = "[" * 10**7 + "]" * 10**7, "line 2 nests past the interpreter's depth"
OFF = "line 1's sides {} make no board, a side below 1"
BROKEN = {  # each broken record's lines, the guard without which it would be read or would raise, and its cause
    "a line that is no JSON": ([H, "no json", E], "jsoned", NO_JSON),
    "a line with no kind": ([H, {"round": 1, "site": 0}, E], "jsoned", NO_JSON),
    "a key twice": ([H, KEYED, E], "jsoned", NO_JSON),
    "a line nested past the interpreter's depth": ([H, DEEP, E], "jsoned", NESTS),
    "an empty file": ([], "framed", "the record holds no header and end"),
    "a first line that is no header": (
        [{**GIVE, "version": schema.VERSION}, E],
        "headed",
        "the first line is no header",
    ),
    "no version": ([{"kind": "header"}, E], "versioned", "the header holds no version"),
    "a version of another major": (
        [{**H, "version": "1.4"}, E],
        "versioned",
        f"the version 1.4 is of another major than the schema's {schema.VERSION}",
    ),
    "no end": ([H, BARE], "ended", "the last line is no end"),
    "an unknown kind": (
        [H, {"kind": "chime", "round": 1, "site": 0}, E],
        "kinded",
        "the line kinds ['chime'] are unknown",
    ),
    "a kind past ASCII": (
        [H, {"kind": "\xe9", "round": 1, "site": 0}, E],
        "kinded",
        "the line kinds ['\\xe9'] are unknown",
    ),
    "the old engine's whole click": (
        [H, {**GIVE, "kind": "whole"}, E],
        "kinded",
        "the line kinds ['whole'] are unknown",
    ),
    "an event without its site": ([H, without(BARE, "site"), E], "placed", UNPLACED),
    "an event without its round": ([H, without(BARE, "round"), E], "placed", UNPLACED),
    "a float for a whole number": ([H, {**BARE, "q": 1.5}, E], "shaped", SHAPE.format("q")),
    "a truth value for a whole number": (
        [H, {**BARE, "train": True}, E],
        "shaped",
        SHAPE.format("train"),
    ),
    "NaN for a whole number": ([H, NAN, E], "shaped", SHAPE.format("q")),
    "a float in the header": ([{**H, "width": 0.5}, E], "shaped", LINE1.format("width")),
    "a label that is no label": ([{**H, "engine": [1]}, E], "shaped", LINE1.format("engine")),
    "a kind card's characters off its shape": (
        [{**H, "kinds": [{**KIND, "characters": [0.5]}]}, E],
        "shaped",
        LINE1.format("kinds"),
    ),
    "a train card's key off its shape": (
        [{**H, "trains": [{**CARDS[0], "key": 0.5}]}, E],
        "shaped",
        LINE1.format("trains"),
    ),
    "an end's digest that is no label": ([H, {**E, "digest": 1}], "shaped", SHAPE.format("digest")),
    "null in an unnamed field": ([H, {**BARE, "note": None}, E], "shaped", SHAPE.format("note")),
    "a float in an unnamed row": ([H, {**BARE, "note": [1, [0.5]]}, E], "shaped", SHAPE.format("note")),
    "a float in an unnamed mapping": (
        [H, {**BARE, "note": {"a": 0.5}}, E],
        "shaped",
        SHAPE.format("note"),
    ),
    "a field named with a line feed": ([H, {**BARE, "a\nb": 0.5}, E], "shaped", SHAPE.format("a\\nb")),
    "a field named with a lone surrogate": (
        [H, {**BARE, "\ud800": 0.5}, E],
        "shaped",
        SHAPE.format("\\ud800"),
    ),
    "a round past the end's rounds": (
        [H, *met(7), E],
        "valued",
        "line 2 stands at round 7, off the record's rounds 1 to 6",
    ),
    "a round before the first": (
        [H, *met(0), E],
        "valued",
        "line 2 stands at round 0, off the record's rounds 1 to 6",
    ),
    "a site off the board": ([B, *met(1, 1 + 1), E], "valued", SITE.format(1 + 1)),
    "a site below 0": ([B, *met(1, -1), E], "valued", SITE.format(-1)),
    "a side below 1": (
        [{**B, "sides": [1 + 1, -1, -1]}, *met(), E],
        "valued",
        OFF.format([1 + 1, -1, -1]),
    ),
    "a side of 0": ([{**B, "sides": [1 + 1, 0, 1]}, *met(), E], "valued", OFF.format([1 + 1, 0, 1])),
    "a train card's winding 0": (
        [{**H, "trains": [CARDS[0], {**CARDS[1], "winding": 0}]}, *met(), E],
        "valued",
        "line 1's train card 2 holds the winding 0, below 1",
    ),
    "a train on two cards": (
        [{**H, "trains": [*CARDS, CARDS[0]]}, *met(), E],
        "valued",
        "line 1's train cards name the train 0 twice",
    ),
    "a train no card names": (
        [H, {**BARE, "train": 5}, E],
        "clicked",
        "line 2 names train 5, which no train card names",
    ),
    "q 0 on a line of no side": (
        [H, {**GIVE, "q": 0, "sides": []}, E],
        "paired",
        "line 2 holds a tooth beside its sides, or no sides",
    ),
    "a line at an earlier line's place": (
        [H, GIVE, GIVE, TOOK, E],
        "clicked",
        "line 3 stands at the round, the site and the train of an earlier click line",
    ),
    "the end's across dropped": (
        [B, *CROSS, {**E, "across": []}],
        "crossed",
        "line 2's side across a Mesh to train 0 stands in no entry of the end's across",
    ),
    "the end's across off the board": (
        [B, *CROSS, {**E, "across": [[0, 0, [5, 0], [3, 3]]]}],
        "crossed",
        "the end's across names place 5, off the board of sides [2, 1, 1]",
    ),
    "a side across a Mesh on a line of no train": (
        [B, without(SENT, "train"), CROSS[1], ENDED],
        "paired",
        "line 2 names no train whose card holds a whole key",
    ),
    "the events out of order": ([H, *met(1 + 1), *met(), E], "ordered", ORDER),
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


def read(lines, tmp_path):
    """A record of the given lines, read."""
    path = tmp_path / "record.jsonl"
    path.write_text(text(lines), encoding="utf-8")
    return records.read(str(path))[0]


def test_the_record_is_read_by_its_schema_and_each_guard_refuses_its_own_broken_record(tmp_path):
    """Yes: a record of the schema reads in order, its unnamed and absent fields among it, a label holding any
    character. No: each broken one is refused by its own guard, named in ASCII, and read without that guard."""
    for name in sorted(BROKEN):
        lines, guard, cause = BROKEN[name]
        assert cause_of(lines, tmp_path) == cause, name
        kept = tuple(g for g in records.GUARDS if g.__name__ != guard)
        assert not unread(str(tmp_path / "record.jsonl"), kept), name
    assert cause_of([H], tmp_path) == "the record holds no header and end"
    assert cause_of([{**H, "version": 1 + 1}, E], tmp_path) == "the header holds no version"
    assert cause_of([H, {"kind": 1, "round": 1, "site": 0}, E], tmp_path) == NO_JSON  # a kind no label
    absent, nul = records.read(str(tmp_path / "absent.jsonl")), records.read(str(tmp_path) + "/a\x00b")
    assert absent == (None, "the record's file is absent") and nul == (
        None,
        "the record's file cannot be read",
    )
    label = "a b\u0085c d"
    lines = [B, GIVE, TOOK, {**met(1, 1)[0], "note": label}, met(1, 1)[1], E]
    # each line ends in a return and a line feed, and holds returns as white space between its tokens
    texts = [json.dumps(line, ensure_ascii=False).replace(", ", ",\r ") + "\r\n" for line in lines]
    path = tmp_path / "record.jsonl"
    path.write_text("".join(texts), encoding="utf-8")
    record, cause = records.read(str(path))
    assert cause == "" and record is not None and record.of("click")[: 1 + 1] == [GIVE, TOOK]
    assert record.of("click")[-1 - 1]["note"] == label
    reads = [[B, {**BARE, "ends": [1]}, E], [{**B, "ends": [5]}, BARE, E], [B, BARE, {"kind": "end"}]]
    reads += [[B, *CROSS, ENDED]]  # the end's across holding the side across a Mesh the lines name
    assert [cause_of(lines, tmp_path) for lines in reads] == ["", "", "", ""]
    sides = [10**4000, 10**4000, 1]
    cause = cause_of([{**B, "sides": sides}, *met(1, -1), E], tmp_path)
    assert cause == f"line 2 names site -1, off the board of sides {sides}"


def counts(round_, site):
    """The ledger's Count lines of one round and Node-clock, after the step: each train's now counts there."""
    return [{"round": round_, "at": "step", "site": site, "train": t, "count": [t, 0]} for t in (0, 1)]


GOOD = counts(1, 0) + counts(1, 1)
STANDS = "the ledger's line 5 stands at no whole round and train, after the step"
OBJECT, FITTED = (
    "the ledger's line 5 is no JSON object",
    "the ledger's line 5 holds a field that has not its shape in the schema",
)
LEDGER_BROKEN = {  # each broken ledger's line after GOOD's four, the guard without which it would be read or raise
    "a blank line": ("", "objects", OBJECT),
    "a line that is no JSON": ("no json", "objects", OBJECT),
    "a line that is a list": ([1, "step", 0, 4], "objects", OBJECT),
    "a line without its at": (without(GOOD[0], "at") | {"round": 1 + 1}, "standing", STANDS),
    "a line without its round": (without(GOOD[0], "round"), "standing", STANDS),
    "a line without its train": (without(GOOD[0], "train") | {"round": 1 + 1}, "standing", STANDS),
    "a line after the clicks, which no run writes": ({**GOOD[0], "at": "clicks"}, "standing", STANDS),
    "a count that is no whole number": ({**GOOD[0], "round": 1 + 1, "count": [4.5]}, "fitted", FITTED),
    "a count that is a label": ({**GOOD[0], "round": 1 + 1, "count": "x"}, "fitted", FITTED),
    "a line at the place of an earlier one": (
        GOOD[0],
        "once",
        "the ledger's line 5 stands at the round, the at, the site and the train of an earlier line",
    ),
}


def test_a_broken_ledger_is_not_read_with_its_own_cause_and_fails_without_its_guard(tmp_path):
    """Yes: the ledger's Count lines read. No: each broken ledger refused by its own guard and read without it."""
    path = tmp_path / "ledger.jsonl"
    path.write_text(text(GOOD), encoding="utf-8")
    assert records.read_ledger(str(path)) == (GOOD, "")
    for name in sorted(LEDGER_BROKEN):
        line, guard, cause = LEDGER_BROKEN[name]
        path.write_text(text([*GOOD, line]), encoding="utf-8")
        assert records.read_ledger(str(path)) == (None, cause), name
        kept = tuple(g for g in records.LEDGER_GUARDS if g.__name__ != guard)
        assert not unread(str(path), kept, records.read_ledger), name
    assert records.read_ledger(str(tmp_path / "absent.jsonl")) == (None, "the ledger's file is absent")


def tool(*args):
    return subprocess.run(
        [sys.executable, "-I", str(TOOL), *map(str, args)], capture_output=True, text=True
    )


def test_the_tool_reads_names_and_raises_nothing_and_lifts_the_digits(tmp_path):
    """Yes: a record and its ledger read and printed, a whole number past the interpreter's digits read by the tool,
    which lifts them. No: a usage error, a broken record and an absent ledger, each named, nothing raised, a cause in
    ASCII however its field is named."""
    names = ("record", "ledger", "broken", "wide")
    record, good, broken, wide = (tmp_path / f"{name}.jsonl" for name in names)
    number = '{"kind": "click", "round": 1, "site": 0, "train": 0, "q": ' + "9" * (DIGITS + 1) + "}"
    for path, lines in zip(
        (record, good, broken, wide),
        ([H, GIVE, TOOK, E], GOOD, [H, "no json", E], [H, number, E]),
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
    assert f"the ledger: read, {len(GOOD)} lines" in shown.stdout
    assert "the ledger's file is absent" in absent.stdout
    assert lifted.stdout.startswith("the ledger: the ledger is absent")
    assert unread_run.stdout == f"not read: {NO_JSON}\n"
    for key, name in (("\ud800", "\\ud800"), ("a\nnot read: forged", "a\\nnot read: forged")):
        broken.write_text(text([H, {**BARE, key: 0.5}, E]), encoding="utf-8")
        assert tool(broken).stdout == f"not read: line 2's {name} has not its shape in the schema\n"


def test_the_click_lines_are_listed_and_counted_per_train_and_site_with_no_verdict_and_the_tool_prints_them(
    tmp_path,
):
    """Yes: the lines list in the schema's order; per train and per Node-clock the lines, the given, the taken and the
    net; the places whose across net is not 0 counted; the tool prints the list, each line's sides and across, and
    the counts. Yes too: a quantum across a Mesh, between two places, counts each of them as passing a net across."""
    held = clicks.counted(read([B, GIVE, TOOK, E], tmp_path))
    assert held.lines == [GIVE, TOOK] and held.sites == {0: clicks.Tally(len(held.lines), 1, 1, 0)}
    assert held.trains == {0: clicks.Tally(1, 1, 0, -1), 1: clicks.Tally(1, 0, 1, 1)}
    assert (held.places, held.crossed) == (1, 0)
    give = {**GIVE, "round": 6, "sides": [], "across": [[0, 1, -1, 3, 6]]}
    across = [give, {**give, "site": 1, "q": 1, "across": [[0, 0, 1, 3, 0]]}]
    more = clicks.counted(read([B, GIVE, TOOK, *across, E], tmp_path))
    assert (more.places, more.crossed) == (len({(e["round"], e["site"]) for e in more.lines}), 1 + 1)
    run = tool(tmp_path / "record.jsonl")  # the record read last, as read() wrote it
    assert run.returncode == 0 and run.stderr == "" and run.stdout.startswith("the ledger: ")
    lines = run.stdout.splitlines()
    assert (
        "the click lines: 4" in lines
        and "  round 6, site 0, train 0: q -1, sides [], across [[0, 1, -1, 3, 6]]" in lines
    )
    assert "  round 1, site 0, train 0: q -1, sides [[1, -1, 3, 6]], across []" in lines
    assert "train 0: 3 lines, given 2, taken 1, net -1" in lines
    assert "site 0: 3 lines, given 2, taken 1, net -1" in lines
    net = "each place's across net, its sum of q over the trains (its own site's sides cancel there): 2 of 3 places"
    assert f"{net} pass a net across a Mesh" in lines


def test_the_click_world_reads_the_books_no_own_count_and_no_cone_where_none_could_be_outside(tmp_path):
    """Yes: q summing to 0 at every place, the edges' consistency check holding by construction, never SHOWN; at round 2,
    the lay's reach, no line could stand outside the cone, not read. No: a quantum across a Mesh two Meshes from the lay at
    round 1, the cone NOT SHOWN, its books closed at both places; a line with no q, not read; no click line: NO CLICK, refusal last."""
    # a ring of five sites, its setting laying one gear, at site 0
    lay = json.dumps({"version": 1, "ticks": 6, "gears": [[0, 0, 0, 1, 0, 0]]})
    ring = {**H, "sides": [5, 1, 1], "files": [{"name": "setting.json", "text": lay}]}
    world = shadow.shadow(read([ring, *met(1 + 1, 1 + 1), E], tmp_path))  # two Meshes from the lay
    assert [v["kind"] for v in world.values()] == [shadow.HOLDS, "NOT READ"]
    give = {**TOOK, "sides": [], "across": [[0, 1 + 1, 1, 3, 0]]}
    apart = [
        give,
        {**GIVE, "site": 1 + 1, "sides": [], "across": [[1, 0, -1, 3, 6]]},
    ]  # two sites of one round
    world = shadow.shadow(read([ring, *apart, E], tmp_path))
    held, far = world[shadow.CONSISTENCY], world[shadow.CONE]["cause"]
    assert held["kind"] == shadow.HOLDS and far.startswith(
        "the click line at round 1, site 2 stands outside the lay's cone"
    )
    assert shadow.books(read([ring, without(BARE, "q"), E], tmp_path))["kind"] == "NOT READ"
    assert {v["kind"] for v in shadow.shadow(read([ring, E], tmp_path)).values()} == {shadow.ABSENT}
    run = tool(tmp_path / "record.jsonl")  # the record of no click line, read last
    last = run.stdout.splitlines()[-1]
    assert run.returncode == 0 and "the click world (the owner's law of 23:4x UTC):" in run.stdout
    assert last.startswith("  the record holds no click line, so no claim") and "light's speed" in last
