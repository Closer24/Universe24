"""Tensor24's whole system once, on a test's lay (frame.strengthless): laid by one formula, a round the naive round,
the trains' order and the 24's turns nothing to the act, a uniform drift's orbit with no period, run to a record and a
ledger the decoder reads, the run back exact, a departure named with nothing written; the edge teeth on a pair world."""

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
from tensor24.algebra.carry import carry
from tensor24.decoder import records
from tensor24.engine import state, step
from tensor24.record import schema
from tensor24.runner import load as loading
from tensor24.runner import run
from tensor24.runner.files import NAMES, sites_of, whole
from tensor24.runner.rewind import rewind
from tests import frame

ROOT = Path(__file__).resolve().parents[1]
TOOTH = 1 << 127  # a tooth within the files' width and past the first train's dial
FIELDS = ("round", "at", "site", "train", "count")  # a Count line's fields, schema.Count's
REACH = 1 << 40  # the clock's counts are drawn below it
ALONE = 40  # the pair world's rounds for the split alone's no, past its first open place, round 26 on this head
HOW = {"capture_output": True, "text": True}  # a tool run, its output read


def read(path):
    """A file of JSON, or a record's lines, each a JSON object."""
    text = path.read_text(encoding="utf-8")
    return [json.loads(x) for x in text.splitlines()] if path.suffix == ".jsonl" else json.loads(text)


def ordered(order=None):
    """The test's lay's three files, its trains in the order given and the setting's gears renumbered with them."""
    universe, piece, setting = (frame.strengthless()[name] for name in NAMES)
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
    """Every row's rest, stretch, kick and grips alike, the drive's teeth senses on the square's 00 and ii rows and 1 elsewhere, the
    clock's read the square's 00 slot at k0 = Spokes x senses into every other row (the 00 row reads none); no term of J laid."""
    rows, (zero,) = len(laid.gearing.rest), [t.first for t in held.trains if t.square]
    alike = all(len(set(np.broadcast_to(x, (rows, 1))[:, 0].tolist())) == 1 for x in laid.gearing[:3])
    senses, unit = len(laid.spokes) // len(laid.spokes[0]), np.eye(rows, dtype=int)[zero]  # the 00 row's
    dial = [senses if r in (zero, *range(zero + 4, zero + 7)) else 1 for r in range(rows)]  # 00 and ii
    read, ones = frame.dense(laid.clock, rows, rows), np.ones(rows, dtype=int)
    grips, plan = len(set(laid.grip.ravel().tolist())) == 1, not laid.plan.factor.any()  # no notch
    clock = (read == senses * len(laid.spokes) * np.outer(ones - unit, unit)).all()
    return alike and grips and plan and clock and laid.gearing.drive[:, 0].tolist() == dial


def drawn(held, laid, seed):
    """A state on the layout: every gear across 2**256, the square's 00 slot moving below REACH, each tooth in its dial."""
    rng, (rows, n) = np.random.default_rng(seed), (len(laid.gearing.rest), laid.nb.shape[1])
    a, b = frame.wide(rng, (rows, n)), frame.wide(rng, (rows, n))
    (clock,) = [t.first for t in held.trains if t.square]
    a[clock], b[clock] = (rng.integers(0, REACH, n).astype(object) for _ in "ab")
    d = step.weight(laid.gearing, laid.clock, a) + step.weight(laid.gearing, laid.clock, b)
    r = frame.wide(rng, (rows, n)) % (d + d) - d
    return state.State(a, b, r, 0 * a, 0 * laid.click.key + 0 * a[:1])  # every edge side's tooth


def naive(laid, held, s, shape):
    """One round site by site with loops: W the rest and the square's 00 slot at k0 = Spokes x senses at both slots (the 00 row's own
    at rest), each grip its rest and the square's ii slot of its axis at both ends of its Mesh, by name; the split on the edge."""
    a, b, r = (x.tolist() for x in s[:3])
    (zero,), d, rows = [x.first for x in held.trains if x.square], len(shape), len(s.a)
    rest, grip, k0 = int(laid.gearing.rest[0, 0]), int(laid.grip[0, 0]), 2 * d * 2  # k0, Spokes x senses
    out = [np.zeros_like(s.a) for _ in "abr"]
    for i, x in enumerate(itertools.product(*map(range, shape))):
        around = [np.ravel_multi_index(y, shape) for y in frame.near(x, shape)]  # +x, -x, +y, -y, +z, -z
        wa, wb = ([rest + k0 * c[zero][i] * (g != zero) for g in range(rows)] for c in (a, b))
        grips = [grip + sum(a[zero + 1 + d + k // 2][y] for y in (i, j)) for k, j in enumerate(around)]
        moment, first = [0] * rows, [0] * rows
        for g in range(rows):
            push = sum(k * (a[g][j] - a[g][i]) for k, j in zip(grips, around, strict=True))
            moment[g] = 2 * ((wa[g] + wb[g]) * (a[g][i] - b[g][i]) + 2 * push) + r[g][i]
            first[g] = frame.split(moment[g], wa[g] + wb[g])[0]  # the count at the edge's own dial
        for g in range(rows):
            wa1 = rest + k0 * (a[zero][i] + first[zero]) * (g != zero)  # the teeth at the next slot
            q, kept = frame.split(moment[g], wa[g] + wa1)
            out[0][g, i], out[1][g, i], out[2][g, i] = a[g][i] + q, a[g][i], kept
    return out


def orders_alike():
    """The test's lay in every order of its trains, run its ticks: each train's rows in the layout and in the run alike."""
    runs, (universe, _, setting) = [], ordered()
    for order in itertools.permutations(range(len(universe["trains"]))):
        held, laid, s = lay(*ordered(order))
        for _ in range(setting["ticks"]):
            s = step.tick(laid, s)
        trains = [order.index(t) for t in range(len(order))]  # each file train's place in this order
        place = [held.trains[n] for n in trains]
        rows = np.concatenate([np.arange(t.first, t.first + t.rows()) for t in place])
        gears = [np.broadcast_to(x, s.a.shape)[rows] for x in laid.gearing]
        sides = [t * len(order) + u for t, u in itertools.product(trains, trains)]  # the file's sides
        runs.append([*gears, *(x[rows] for x in s[:-1]), s.k[sides]])
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
        for x, (n, t) in itertools.product(range(sites), enumerate(held.trains)):
            count = s.a[t.first : t.first + t.rows(), x].tolist()
            wanted.append(dict(zip(FIELDS, (at, "step", x, n, count), strict=True)))
    return wanted


def test_the_lay_is_laid_by_one_formula_steps_alike_in_every_order_and_turn_and_runs_to_a_record_and_back(
    tmp_path, monkeypatch
):
    (universe, piece, setting), paths = ordered(), frame.written(tmp_path / "lay", frame.strengthless())
    held, laid, start = lay(universe, piece, setting)
    assert geared_alike(held, laid)
    # D1, the drift's infinite order (MATH4 1.5), on a test's lay that differs at a whole row, lawful as the check of a
    # DERIVED fact (09:5x): the wave's first row a uniform drift, a = c + 1 and b = c at every site, feels no pull, so
    # every round carries it one count on, each round's promise met: an orbit with no period
    c, (a, b, r) = start.a[0, 0], (x.copy() for x in start[:3])
    a[0], b[0], r[0] = c + 1, c, 0
    s = state.State(a, b, r, *start[3:])
    for n in range(1, setting["ticks"] + 1):
        assert run.promised(main.ENGINE, laid, s, universe["integers"]["width"]) == []
        s = step.tick(laid, s)
        assert (s.a[0] == c + n + 1).all()
    for seed in range(3):  # a round is the naive round, and departs from it with the grips' read ignored
        s = drawn(held, laid, seed)
        unread = laid._replace(stretch=frame.unread())
        (*stepped, _, _), (*blind, _, _) = step.tick(laid, s), step.tick(unread, s)
        model, out = naive(laid, held, s, piece["shape"]), step.tick(laid, s)
        assert frame.same(stepped, model) and not frame.same(blind, model)
        assert not step.act(laid, s)[1].any() and not out.k.any()  # no vertex: no passing, no click
        for m in frame.turns():
            moved = frame.turned_by(m, laid, held, out, piece["shape"])
            assert frame.same(
                step.tick(laid, frame.turned_by(m, laid, held, s, piece["shape"])), moved
            ), m.tolist()
    # the run: the files verbatim with their digests, every Node-clock in every round, the end's digest the rounds'
    # state, and 0 where the run back misses
    record, missed, reached = tmp_path / "run.jsonl", tmp_path / "missed.jsonl", {}
    assert main.ran(paths, record) == []
    got, cause = records.read(str(record))
    assert cause == "" and got is not None
    texts = [path.read_text(encoding="utf-8") for path in paths]
    assert [(f["name"], f["text"], f["digest"]) for f in got.header["files"]] == [
        (path.name, text, hashlib.sha256(text.encode("utf-8")).hexdigest())
        for path, text in zip(paths, texts, strict=True)
    ]
    assert got.header["sides"] == piece["shape"] and got.header["runner"] == "synchronous"
    ticks = setting["ticks"]
    end = dict(kind="end", rounds=ticks, digest=got.end["digest"], undone=ticks, exact=1, across=[])
    assert got.end == end and got.events == []  # no edge, so no click and no Mesh edge; no tooth written
    card = {k: [t[k] for t in got.header["trains"]] for k in ("label", "winding", "key", "square")}
    assert card["label"] == [t["name"] for t in universe["trains"]] and card["square"] == [0, 1]
    assert card["winding"] == [1, len(laid.spokes) // len(piece["shape"])]  # the 00 row's dial, senses
    assert set(card["key"]) == {universe["chosen"]["key"]} and card["square"] == list(held.trains.square)
    traced, turns = [k["characters"] for k in got.header["kinds"]], len(list(frame.turns()))
    assert {len(c) for c in traced} == {turns} and len(set(map(tuple, traced))) == len(traced)

    def kept(layout, s):
        reached.setdefault("end", s)  # the first state the run back reads is the rounds' last
        return s  # a run back that undoes nothing

    assert run.run(main.ENGINE._replace(untick=kept), paths, missed) == []
    assert read(record)[-1]["digest"] == run.digest(run.stated(reached["end"]))
    assert read(missed)[-1]["exact"] == 0 and read(missed)[-1]["digest"] == read(record)[-1]["digest"]
    # the ledger: every train's counts as the rounds reach them, the metric family at rest, the schema's fields
    lines, fields = read(run.ledger_of(record)), [f.name for f in dataclasses.fields(schema.Count)]
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
    # a departing file, an even key, a broken promise or a lay outside the wave's window (the 00 slot at site 0 laid so
    # deep that the teeth there, the rest and k0 times it, are within 1 and k0, every row's but the 00 row's own) is
    # named, and nothing is written, by the run and its tool
    even = {**universe, "chosen": {**universe["chosen"], "key": universe["chosen"]["key"] + 1}}
    universe["version"], k0 = 1 + 1, int(laid.clock.factor.max())  # the clock's read factor
    deep, low = json.loads(json.dumps(setting)), (k0 - int(laid.gearing.rest[0, 0])) // k0
    deep["gears"].append([[n for n, t in enumerate(held.trains) if t.square][0], 0, 0, low, low, 0])
    setting["gears"][0][-1] = TOOTH
    edits = (
        ("universe", universe, "universe.version: 1, not 2", 1),
        ("universe", even, "universe.chosen.key: an odd whole number", 1),
        ("setting", setting, "round 1: row 0, site 0: the tooth", 1),
        ("setting", deep, "round 1: row 0, site 0: the Spokes' grips", len(laid.gearing.rest) - 1),
    )
    for name, held_, named, lines in edits:
        edited = list(paths)
        edited[NAMES.index(name)] = tmp_path / f"{name}.json"
        edited[NAMES.index(name)].write_text(json.dumps(held_), encoding="utf-8")
        out, found = tmp_path / f"{name}.jsonl", main.ran(edited, tmp_path / f"{name}.jsonl")
        assert len(found) == lines and found[0].startswith(named), found
        assert not out.exists() and not run.ledger_of(out).exists()
    tool = str(ROOT / "tools" / "tensor24_run.py")
    args, written = [sys.executable, "-I", tool], tmp_path / "tool.jsonl"
    done = subprocess.run([*args, *map(str, paths), str(written)], **HOW)
    assert done.returncode == 0 and done.stdout == f"{written}: written\n"
    assert not records.read(str(written))[1]  # the tool's record reads
    missing, none = tmp_path / "missing.json", tmp_path / "none.jsonl"
    done = subprocess.run([*args, str(missing), *map(str, paths[1:]), str(none)], **HOW)
    assert done.returncode == 1 and "missing.json: not read" in done.stdout and not none.exists()
    # every order of the trains runs alike, and not with the clock found by its place (the B2 mutant)
    assert orders_alike()
    by_place(monkeypatch)
    assert not orders_alike()
    # the pair world, kept as NOT_CLOSED 37's record: whichever way it falls, a departure is the width's own, named with nothing
    # written, or the run writes its record and ledger
    files = frame.pair_world()
    for name, held_ in files.items():
        (tmp_path / f"{name}.json").write_text(json.dumps(held_), encoding="utf-8")
    pair_record = tmp_path / "pair.jsonl"
    found = main.ran([tmp_path / f"{name}.json" for name in NAMES], pair_record)
    wide = f"takes more bits than the width, {files['universe']['integers']['width']}"
    assert all(x.startswith("round ") and wide in x for x in found), found  # a departure the width's own
    assert (
        pair_record.exists() == run.ledger_of(pair_record).exists() == (not found)
    )  # named, nothing written


def test_the_edge_teeth_close_every_edges_books_run_back_and_turn_with_the_24_and_the_split_alone_does_not():
    """Yes: on the pair world, three trains at one Node-clock, every edge's two sides click opposite quotients with teeth summing to
    key - 1 in every round, run back exact; the click world's cube turned by each of the 24 steps to the round turned, clicks and teeth.
    No: the split alone, each train's sum of its sides carried on one tooth of its own (NC29's form), opens the books there (C5's no)."""
    held, laid, start = lay(*frame.pair_world().values())
    trains, key = len(held.trains), laid.click.key[0, 0]
    s, alone, opened = start, (key - 1) // step.halves(laid) + 0 * start.a[:trains], False
    for _ in range(ALONE):
        out, q = step.act(laid, s)
        assert frame.opposed(q, out.k, key, trains)
        passed = step.passing(
            laid.click, laid.plan, s.b, s.a, out.a
        )  # each train's sum of its sides, alone
        given, alone = carry(passed.reshape(trains, trains, -1).sum(axis=1), key, alone)
        s, opened = out, opened or given.sum(axis=0).any()
    assert opened and frame.same(rewind(step.untick, laid, s, ALONE), start)
    click = [read(ROOT / "examples" / "tensor24-click" / f"{name}.json") for name in NAMES]
    (held, laid, s), shape = lay(*click), click[NAMES.index("piece")]["shape"]
    out, q = step.act(laid, s)
    for m in frame.turns():
        moved, p = step.act(laid, frame.turned_by(m, laid, held, s, shape))
        sited = frame.turned_by(m, laid, held, s._replace(k=q), shape).k  # the clicks moved too
        assert frame.same(moved, frame.turned_by(m, laid, held, out, shape)) and frame.same([p], [sited])


def test_the_widths_promise_names_a_count_past_the_width_in_either_slot_and_none_at_its_edge(tmp_path):
    """Yes: counts of 2^w - 1 and -(2^w - 1) in both slots, w the universe file's width, are within it and named by none.
    No: a count of 2^w or -2^w in either slot is named where it stands; a free gear at 2^w - 1, before 2^w - 2, crosses
    by inertia in round 1, named at round 2, nothing written (1 tick the end state's read, 2 ticks the round-2 promise)."""
    universe = read(ROOT / "examples" / "tensor24-click" / "universe.json")  # a held train, Mesh-less
    width = universe["integers"]["width"]  # the width of the universe the case runs
    edge, past, zero = (1 << width) - 1, 1 << width, np.zeros((1, 1), dtype=object)
    held = lambda a, b: state.State(zero + a, zero + b, zero, zero, zero)  # noqa: E731
    assert run.wide(held(edge, -edge), width) == run.wide(held(-edge, edge), width) == []
    for n in (past, -past):
        named = [f"row 0, site 0: the count {n} takes more bits than the width, {width}"]
        assert run.wide(held(n, 0), width) == run.wide(held(0, n), width) == named
    universe["chosen"].update(spring=0, hold=0, tie=0)  # no strength on it: free
    (hand,) = [n for n, t in enumerate(universe["trains"]) if t["kinds"] == ["A1", "A2"]]
    for ticks in (1, 1 + 1):  # the end state's read, then the round-2 promise
        setting = {"version": 1, "ticks": ticks, "gears": [[hand, 0, 0, edge, edge - 1, 0]]}
        files = {"universe": universe, "piece": {"version": 1, "shape": [1, 1, 1]}, "setting": setting}
        for name, held_ in files.items():
            (tmp_path / f"{name}.json").write_text(json.dumps(held_), encoding="utf-8")
        free = tmp_path / "free.jsonl"
        found = main.ran([tmp_path / f"{name}.json" for name in NAMES], free)
        named = f"site 0: the count {past} takes more bits than the width, {width}"  # the held train's first row
        assert len(found) == 1, found  # one departure
        assert found[0].startswith("round 2: row ") and found[0].endswith(named), found
        assert not free.exists() and not run.ledger_of(free).exists()  # round 1's ledger unlinked
