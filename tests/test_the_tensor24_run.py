"""Tensor24's whole system once, on our bang, the three example files: laid by one formula, a round the naive round,
the trains' order and the 24's turns nothing to the act, run to a record and a ledger the decoder reads with the run
back exact, and a departure named with nothing written, by the run and by its tool."""

import dataclasses
import hashlib
import itertools
import json
import subprocess
import sys
import typing
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.decoder import records
from tensor24.engine import kinds, state, step
from tensor24.record import schema
from tensor24.runner import load as loading
from tensor24.runner import run
from tensor24.runner.files import NAMES, sites_of, whole
from tests import frame

ROOT = Path(__file__).resolve().parents[1]
PATHS = [ROOT / "examples" / "tensor24" / f"{name}.json" for name in NAMES]
TOOTH = 1 << 127  # a tooth within the files' width and past light's dial
FIELDS = ("round", "at", "site", "train", "count")  # a Count line's fields, schema.Count's
REACH = 1 << 40  # the clock's counts are drawn below it


def read(path):
    """A file of JSON, or a record's lines, each a JSON object."""
    text = path.read_text(encoding="utf-8")
    return (
        [json.loads(line) for line in text.splitlines()] if path.suffix == ".jsonl" else json.loads(text)
    )


def bang(order=None):
    """Our bang's three files read, its trains in the order given and the setting's gears renumbered with them."""
    universe, piece, setting = (read(path) for path in PATHS)
    order = order or range(len(universe["trains"]))
    universe["trains"] = [universe["trains"][t] for t in order]
    setting["gears"] = [[list(order).index(t), *rest] for t, *rest in setting["gears"]]
    return universe, piece, setting


def lay(universe, piece, setting):
    """The files loaded as the run loads them: the trains' rows, the layout and the state laid."""
    shape = piece["shape"]
    held, found = loading.load(universe, setting, sites_of(shape), *main.made(loading.star(len(shape))))
    assert found == [] and held is not None
    return held, main.layout(universe, shape, held), state.State(*held.state)


def leaves(hint):
    """The types a field's hint is built of, through rows and the schema's own records; any other form as itself."""
    if dataclasses.is_dataclass(hint):
        hints = typing.get_type_hints(hint)
        return set().union(*(leaves(hints[field.name]) for field in dataclasses.fields(hint)))
    origin, inner = (
        typing.get_origin(hint),
        [arg for arg in typing.get_args(hint) if arg is not Ellipsis],
    )
    if origin is not None and origin is not tuple:
        return {origin}
    return set().union(*map(leaves, inner)) if inner else {hint}


def geared_alike(held, laid):
    """Every row's coefficients, grips and read of the clock alike (the parity apart), the read the square's 00 slot
    into every other row (the 00 row reads none); no term of J laid."""
    rows = len(laid.gearing.rest)
    alike = all(len(set(np.broadcast_to(x, (rows, 1))[:, 0].tolist())) == 1 for x in laid.gearing[:-1])
    unit = np.eye(rows, dtype=int)[[t.first for t in held.trains if t.square][0]]  # the 00 slot's row
    read, ones = frame.dense(laid.clock, rows, rows), np.ones(rows, dtype=int)
    grips, plan = len(set(laid.grip.ravel().tolist())) == 1, all(len(x) == 0 for x in laid.plan)
    return alike and grips and plan and (read == np.outer(ones - unit, unit)).all()


def drawn(held, laid, seed):
    """A state on the layout: every gear across 2**256, the square's 00 slot moving below REACH, each tooth in its dial."""
    rng, (rows, n) = np.random.default_rng(seed), (len(laid.gearing.rest), laid.nb.shape[1])
    a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
    (clock,) = [t.first for t in held.trains if t.square]
    a[clock], b[clock] = (rng.integers(0, REACH, n).astype(object) for _ in "ab")
    d = step.weight(laid.gearing, laid.clock, a) + step.weight(laid.gearing, laid.clock, b)
    r = frame.wide(rng, (rows, n)) % (d + d - 1) - (d - 1)
    return state.State(a, b, r, 0 * a, 0 * a[: len(held.trains)])


def naive(laid, held, s, shape):
    """One round site by site with loops: W the rest and the square's 00 slot at both slots (the 00 row's own at rest),
    each grip its rest and the square's ii slot of its axis at both ends of its Mesh, by name; the split on the edge."""
    a, b, r = (x.tolist() for x in s[:3])
    squares, d, rows = [x.first for x in held.trains if x.square], len(shape), len(s.a)
    rest, grip = int(laid.gearing.rest[0, 0]), int(laid.grip[0, 0])
    out = [np.zeros_like(s.a) for _ in "abr"]
    for i, x in enumerate(itertools.product(*map(range, shape))):
        around = [np.ravel_multi_index(y, shape) for y in frame.near(x, shape)]  # +x, -x, +y, -y, +z, -z
        wa, wb = ([rest + sum(c[f][i] for f in squares if f != g) for g in range(rows)] for c in (a, b))
        grips = [
            grip + sum(a[f + 1 + d + k // 2][i] + a[f + 1 + d + k // 2][j] for f in squares)
            for k, j in enumerate(around)
        ]
        moment, first = [0] * rows, [0] * rows
        for g in range(rows):
            push = sum(k * (a[g][j] - a[g][i]) for k, j in zip(grips, around, strict=True))
            moment[g] = 2 * ((wa[g] + wb[g]) * (a[g][i] - b[g][i]) + 2 * push) + r[g][i]
            first[g] = frame.split(moment[g], wa[g] + wb[g])[0]  # the count at the edge's own dial
        for g in range(rows):
            wa1 = rest + sum(a[f][i] + first[f] for f in squares if f != g)  # the teeth at the next slot
            q, kept = frame.split(moment[g], wa[g] + wa1)
            out[0][g, i], out[1][g, i], out[2][g, i] = a[g][i] + q, a[g][i], kept
    return out


def turned(m, laid, held, s, shape):
    """The state turned by m: sites moved, each train's rows by its kind's matrix, a negated row's tooth negated."""
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    site = np.ravel_multi_index(tuple((m @ xyz) % sides), shape)
    acting = kinds.kinds(m[None, :, :])
    turn = np.eye(len(laid.gearing.rest), dtype=object)
    for train in held.trains:
        matrix = kinds.square(acting)[0] if train.square else acting[train.kinds[0]][0]
        at = train.first + np.arange(len(matrix)) * train.part
        for part in range(train.part):
            turn[np.ix_(at + part, at + part)] = matrix
    there = state.State(*(np.empty_like(x) for x in s))
    for x, y in zip(there, s, strict=True):
        x[:, site] = y
    there.a[:, site], there.b[:, site], there.r[:, site] = turn @ s.a, turn @ s.b, turn @ s.r
    return there


def orders_alike():
    """Our bang in every order of its trains, run its ticks: each train's rows in the layout and in the run alike."""
    runs, (universe, _, setting) = [], bang()
    for order in itertools.permutations(range(len(universe["trains"]))):
        held, laid, s = lay(*bang(order))
        for _ in range(setting["ticks"]):
            s = step.tick(laid, s)
        trains = [order.index(t) for t in range(len(order))]  # each file train's place in this order
        place = [held.trains[n] for n in trains]
        rows = np.concatenate([np.arange(t.first, t.first + t.rows()) for t in place])
        gears = [np.broadcast_to(x, s.a.shape)[rows] for x in laid.gearing]
        runs.append([*gears, *(x[rows] for x in s[:-1]), s.k[trains]])
    return all(frame.same(each, runs[0]) for each in runs[1:]) and (runs[0][-len(s)] != 0).any()


def by_place(monkeypatch):
    """The B2 mutant: the clock read at the last train's first row, its place."""
    geared = loading.geared

    def placed(universe, trains, spokes):
        gearing, (first, factor, target), stretch, grip = geared(universe, trains, spokes)
        return gearing, (0 * first + trains[-1].first, factor, target), stretch, grip

    monkeypatch.setattr(loading, "geared", placed)


def ledger(held, laid, s, setting, sites):
    """The Count lines the engine's own rounds give: every train's now counts at every Node-clock after every round."""
    wanted = []
    for at in range(1, setting["ticks"] + 1):
        s = step.tick(laid, s)
        wanted += [
            dict(
                zip(
                    FIELDS,
                    (at, "step", x, n, s.a[t.first : t.first + t.rows(), x].tolist()),
                    strict=True,
                )
            )
            for x in range(sites)
            for n, t in enumerate(held.trains)
        ]
    return wanted


def test_our_bang_is_laid_by_one_formula_steps_alike_in_every_order_and_turn_and_runs_to_a_record_and_back(
    tmp_path, monkeypatch
):
    universe, piece, setting = bang()
    held, laid, start = lay(universe, piece, setting)
    assert geared_alike(held, laid)
    assert not {"Ruler", "LAID"} & set(dir(state)) and not {"ruled", "reading", "at"} & set(dir(step))
    for seed in range(3):  # a round is the naive round, and departs from it with the grips' read ignored
        s = drawn(held, laid, seed)
        unread = laid._replace(stretch=frame.unread())
        (*stepped, _, _), (*blind, _, _) = step.tick(laid, s), step.tick(unread, s)
        model, out = naive(laid, held, s, piece["shape"]), step.tick(laid, s)
        assert frame.same(stepped, model) and not frame.same(blind, model)
        assert not step.act(laid, s)[1].any() and not out.k.any()  # no vertex: no area, no click
        for m in frame.turns():
            moved = turned(m, laid, held, out, piece["shape"])
            assert frame.same(step.tick(laid, turned(m, laid, held, s, piece["shape"])), moved), (
                m.tolist()
            )
    # the run: the files verbatim with their digests, every Node-clock in every round, the end's digest the rounds'
    # state, and 0 where the run back misses
    record, missed, reached = tmp_path / "run.jsonl", tmp_path / "missed.jsonl", {}
    assert main.ran(PATHS, record) == []
    got, cause = records.read(str(record))
    assert cause == "" and got is not None
    texts = [path.read_text(encoding="utf-8") for path in PATHS]
    assert [(f["name"], f["text"], f["digest"]) for f in got.header["files"]] == [
        (path.name, text, hashlib.sha256(text.encode("utf-8")).hexdigest())
        for path, text in zip(PATHS, texts, strict=True)
    ]
    assert got.header["sides"] == piece["shape"] and got.header["runner"] == "synchronous"
    ticks = setting["ticks"]
    end = dict(kind="end", rounds=ticks, digest=got.end["digest"], undone=ticks, exact=1)
    assert got.end == end and got.events == []  # no rate line, and light alone never clicks
    cards = got.header["trains"]  # the file's trains alone, each winding 1 until G3
    assert [t["label"] for t in cards] == [t["name"] for t in universe["trains"]]
    assert {t["winding"] for t in cards} == {1}

    def kept(layout, s):
        reached.setdefault("end", s)  # the first state the run back reads is the rounds' last
        return s  # a run back that undoes nothing

    assert run.run(main.ENGINE._replace(untick=kept), PATHS, missed) == []
    assert read(record)[-1]["digest"] == run.digest(run.stated(reached["end"]))
    assert read(missed)[-1]["exact"] == 0 and read(missed)[-1]["digest"] == read(record)[-1]["digest"]
    # the ledger: every train's counts as the rounds reach them, the metric family at rest, the schema's fields
    lines, fields = (
        read(run.ledger_of(record)),
        [field.name for field in dataclasses.fields(schema.Count)],
    )
    shaped = [
        list(x) == fields and all(map(whole, (x["round"], x["site"], x["train"], *x["count"])))
        for x in lines
    ]
    assert lines == ledger(held, laid, start, setting, sites_of(piece["shape"])) and all(shaped)
    assert records.read_ledger(str(run.ledger_of(record))) == (lines, "")
    rest = {x["train"]: x["count"] for x in lines if held.trains[x["train"]].square}
    assert set(rest) and all(not any(count) for count in rest.values())
    typed = [record for record in vars(schema).values() if dataclasses.is_dataclass(record)]
    assert set().union(*map(leaves, typed)) == {int, str}
    broken = [tuple[int, float], bool, int | None, dict[str, int]]
    assert all(
        leaves(dataclasses.make_dataclass("Broken", [("x", hint)])) - {int, str} for hint in broken
    )
    # a departing file, a broken promise or a lay outside the wave's window (the 00 slot at site 0 laid so deep that
    # the teeth there are 1, every row's but the 00 row's own) is named, and nothing is written, by the run and its tool
    universe["version"] = 1 + 1
    deep, low = json.loads(json.dumps(setting)), 1 - int(laid.gearing.rest[0, 0])
    deep["gears"].append([[n for n, t in enumerate(held.trains) if t.square][0], 0, 0, low, low, 0])
    setting["gears"][0][-1] = TOOTH
    edits = (
        ("universe", universe, "universe.version: 1, not 2", 1),
        ("setting", setting, "round 1: row 0, site 0: the tooth", 1),
        ("setting", deep, "round 1: row 0, site 0: the Spokes' grips", len(laid.gearing.rest) - 1),
    )
    for name, held_, named, lines in edits:
        paths = list(PATHS)
        paths[NAMES.index(name)] = tmp_path / f"{name}.json"
        paths[NAMES.index(name)].write_text(json.dumps(held_), encoding="utf-8")
        out, found = tmp_path / f"{name}.jsonl", main.ran(paths, tmp_path / f"{name}.jsonl")
        assert len(found) == lines and found[0].startswith(named), found
        assert not out.exists() and not run.ledger_of(out).exists()
    tool, written = ROOT / "tools" / "tensor24_run.py", tmp_path / "tool.jsonl"
    done = subprocess.run(
        [sys.executable, "-I", str(tool), *map(str, PATHS), str(written)], capture_output=True, text=True
    )
    assert (
        done.returncode == 0
        and done.stdout == f"{written}: written\n"
        and records.read(str(written))[1] == ""
    )
    missing, none = tmp_path / "missing.json", tmp_path / "none.jsonl"
    done = subprocess.run(
        [sys.executable, "-I", str(tool), str(missing), *map(str, PATHS[1:]), str(none)],
        capture_output=True,
        text=True,
    )
    assert done.returncode == 1 and "missing.json: not read" in done.stdout and not none.exists()
    # every order of the trains runs alike, and not with the clock found by its place (the B2 mutant)
    assert orders_alike()
    by_place(monkeypatch)
    assert not orders_alike()
