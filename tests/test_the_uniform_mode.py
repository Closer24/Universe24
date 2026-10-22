"""The uniform mode on the board wrapped on every axis (ALGEBRA.md, The board's interval is no observable, a hypothesis under its own name, 2026-10-22; The closed lattice has no rest; item 6 of what is open, the closed board's double root; No write from outside Rule3 wakes either double root of the massless row): on a board periodic on every axis a massless held row's rest needs a sink, and the world's key `interval: unobservable` (loader/interval.py `interval_of`), or the law's `uniform: carried` of 2026-10-21 kept admitted beside it (loader/uniform.py `uniform_of`, the carried mean with no hill, the reader's line L2 on the design), admits the board by resting every massless row on the zero-mean part of its sources (features/start `rest`, `without_uniform`, `settled_free`) and leaving the k = 0 component to Rule3's own line, the double root carried at every Node by the step and the one write, no act added. (1) The declaration: the sink's refusal without either key names the hypothesis's key as the way; `interval` refused by name at any value but `unobservable`, where a face is open and where a face is closed (a board with a sink has no free uniform mode and its rest fixes the clock's unit beyond the face), the two keys together refused by name, and a kick, a packet laid on a holder of the content, refused by name under the key (the mean's velocity the content's, nobody's declaration). (2) The uniform line bit for bit: a matter record laid uniform over a 3-cube torus at the band's rest rotation sources a uniform write, so gravity's level is one number at every Node at every interval, and over 20 intervals its second difference is the one write's increment (numerator + r) div (E_s T), the numerator the form D = now^2 - next x before scaled by the write's factor at the record's own content, computed beside from the engine's own functions, bit for bit, the remainder the write's; the tensions 0 (a uniform record has none); the record's rotation slows as the content rises, (next + before) / now read against the band's own line 1 - (den - num) p_0^2 / (den Gamma^2) at the content; the uniform reading one division with one remainder; and the inverse returns the start bit for bit. (3) The rest: a point source on a 7-cube torus at [1, 1] rests on the zero-mean part, the read-weighted mean taken out exactly to under a millionth of a line unit, the fine levels within two fine units of the pace-weighted Poisson solution solved sparse (floats, the test's oracle), the floor at 0 and the levels within one level."""

import json
import re
from fractions import Fraction

import numpy as np
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import spsolve

from event_universe import board_readings, world_files
from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap
from event_universe.features.held_write import held_write
from event_universe.features.start import arrivals, rest, scaled_source, without_uniform
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import UNIVERSE, refused

GAMMA, ACTION, CUBE, AMPLITUDE = 6000, 32768, 3, 435  # the rule's clock and quantum, a 3-cube torus
TORUS = {"x": "periodic", "y": "periodic", "z": "periodic"}


def universe_at_weight_one(folder):  # type: ignore[no-untyped-def]
    """The rule's own universe beside the world with gravity's level weight 1, so that the content moves within a test's intervals, and without the binding holder: a row with a gap rests on a torus through its gap alone, and at the pair [2400, 2401] the division act's iteration contracts the uniform mode by 1 - 1 / 2,400 per act and cycles under the floors (the shipped tests' 170,000 passes at [24, 25]), a limit of the rest's iteration and nothing of the carried mode, left open by name."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [f for f in universe["families"] if f["name"] != "binding"]
    for family in universe["families"]:
        family["reads"] = {name: w for name, w in family["reads"].items() if name != "binding"}
        if family["name"] == "gravity":
            family["held"]["level_weight"] = 1
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")


def uniform_world(folder, name, counts=1, **changes):  # type: ignore[no-untyped-def]
    """A matter record laid uniform over the 3-cube at the band's rest rotation in the vacuum's content (the gravity rest 60): now A at every Node, before A cos omega with cos omega = 1 - (den - num) p_0^2 / (den Gamma^2), the k = 0 line's own; the body declared on every Node at `counts` each; the mode file beside at the world's digest."""
    nodes = CUBE**3
    world = {"shape": [CUBE] * 3, "boundary": dict(TORUS), "intervals": 20, "universe": "u.json"}
    world["bodies"] = [
        {
            "family": "matter",
            "nodes": [
                {
                    "node": [x, y, z],
                    "count": counts[(x * CUBE + y) * CUBE + z] if isinstance(counts, list) else counts,
                }
                for x in range(CUBE)
                for y in range(CUBE)
                for z in range(CUBE)
            ],
        }
    ]
    world.update(node_detectors=[], **changes)
    clock = paces.clock(GAMMA, 60)
    before = (2 * (6000 * GAMMA * GAMMA - 2000 * clock * clock) * AMPLITUDE + 6000 * GAMMA * GAMMA) // (
        2 * 6000 * GAMMA * GAMMA
    )  # A cos omega rounded half up, the test's own arithmetic
    path = folder / f"{name}.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    entry = {
        "family": "matter",
        "pair": [4000, 6000],
        "moving": {"now": [AMPLITUDE] * nodes, "before": [before] * nodes},
    }
    mode = {"world_digest": input_digest(world), "bodies": [entry], "packets": []}
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def laid_torus(folder, name, **changes):  # type: ignore[no-untyped-def]
    """The uniform world with its counts redeclared at the share the gate reads (the count is the record's share, a reading: the first load names it), spread over the Nodes."""
    first = refused("share reads", Lattice, load_world(uniform_world(folder, name, 1, **changes)))
    read = int(re.search(r"share reads (\d+) quanta", str(first)).group(1))
    nodes = CUBE**3
    counts = [read // nodes + (1 if i < read % nodes else 0) for i in range(nodes)]
    return uniform_world(folder, name, counts, **changes)


def test_the_board_declares_its_interval_unobservable_and_refuses_it_by_name_where_a_face_sinks_it(
    tmp_path, monkeypatch
):
    """(1) The declaration (loader/interval.py `interval_of`, `one_key`, `kicks_refused`; loader/uniform.py `uniform_of` beside it): a massless row's rest on a torus is refused by name without either key, the refusal naming `interval: unobservable` as the way and the law's `uniform: carried` beside it; `interval` at a value other than `unobservable` is refused by name; `unobservable` with the x face open or the z face closed is refused by name, a board with a sink having no free uniform mode; the two keys on one world are refused by name together; a `packets` entry on gravity, a kick on the holder of the content, is refused by name under the key; `unobservable` on the torus loads, the world holding the declaration, and so does the law's `carried` (the old key kept admitted, the reader's line L2 on the design)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path)
    sunk = refused("needs a sink", Lattice, load_world(uniform_world(tmp_path, "sunk")))
    assert "interval: unobservable" in str(sunk) and "Rule3's own line at k = 0" in str(sunk)
    assert "uniform: carried" in str(sunk) and "The board's interval is no observable" in str(sunk)
    kept = refused("is 'unobservable'", load_world, uniform_world(tmp_path, "kept", interval="kept"))
    assert "'kept'" in str(kept) and "a count no act reads" in str(kept)
    opened = {**TORUS, "x": "open"}
    key = {"interval": "unobservable"}
    ajar = refused(
        "no free uniform mode",
        load_world,
        uniform_world(tmp_path, "ajar", boundary=opened, face_depth=1, **key),
    )
    assert "x face is 'open'" in str(ajar) and "fixes the clock's unit" in str(ajar)
    closed = {**TORUS, "z": "closed"}
    shut = refused(
        "no free uniform mode", load_world, uniform_world(tmp_path, "shut", boundary=closed, **key)
    )
    assert "z face is 'closed'" in str(shut)
    both = refused("together", load_world, uniform_world(tmp_path, "both", uniform="carried", **key))
    assert "2026-10-21" in str(both) and "2026-10-22" in str(both) and "declare one" in str(both)
    kick = [{"family": "gravity", "along": "x", "wave": [1, 3], "phase": [0, 1], "amplitude": 1}]
    kicked = refused(
        "lays a kick on 'gravity'", load_world, uniform_world(tmp_path, "kick", packets=kick, **key)
    )
    assert "nobody's declaration" in str(kicked) and "the clause of 2026-10-22" in str(kicked)
    board = Lattice(load_world(laid_torus(tmp_path, "torus", **key)))
    assert (
        board.world.unobservable
        and not board.world.uniform
        and board.world.periodic == (True, True, True)
    )
    law = Lattice(load_world(laid_torus(tmp_path, "law", uniform="carried")))
    assert law.world.uniform and not law.world.unobservable  # the law as written, kept and runnable


def test_rule3_carries_the_uniform_line_bit_for_bit_on_a_torus_and_the_inverse_returns(
    tmp_path, monkeypatch
):
    """(2) The uniform line is Rule3's own at every Node: on the 3-cube torus under `uniform: carried` with the uniform matter record, over 20 intervals gravity's time line is one number at every Node (the write uniform, the Links' sum 0), its write remainder one number, its three tension lines 0, and a(t + 1) - 2 a(t) + a(t - 1) is exactly the one write's increment (w D' + r) div (E_s T) with D' the record's form scaled per proper volume and per proper interval at the paces of the content it reads (gravity's level), computed beside from `paces.write_factor` and features/held_write, the remainder after it the engine's too; the content rises and the record's rotation (next + before) / now at the centre falls along the band's line 2 - 2 (den - num) p_0^2 / (den Gamma^2) within the roundings; `Lattice.uniform_mode` reads the level with the remainder 0 (a NamedTuple, no string key in the engine); the 20 intervals run back return the start bit for bit."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path)
    board = Lattice(load_world(laid_torus(tmp_path, "torus", uniform="carried")))
    names = [f.name for f in board.families]
    g, m = names.index("gravity"), names.index("matter")
    wall = board.walls(g)[0]
    assert wall == ACTION  # E_s T at the level weight 1
    start = [(x.now.copy(), x.before.copy(), x.remainder.copy()) for s in board.states for x in s.lines]
    levels, rotations = [], []

    def one_number(array):  # type: ignore[no-untyped-def]
        assert int(array.max()) == int(array.min()), array
        return int(array.max())

    for _ in range(20):
        gravity, record = board.states[g].lines, board.states[m].lines[0]
        a_now, a_before = one_number(gravity[0].now), one_number(gravity[0].before)
        remainder = one_number(board.states[g].write_remainders[0])
        content = a_now  # matter reads gravity at 1, the one holder of the content here
        now, before = int(record.now[1, 1, 1]), int(record.before[1, 1, 1])
        assert all(not line.now.any() for line in gravity[1:])  # the tensions of a uniform record are 0
        board.step()
        after = board.states[m].lines[0].now
        nxt = one_number(after)
        form = now * now - nxt * before  # the record's form about the step, one number
        clock, pace = paces.node_paces(GAMMA, content)
        numerator = int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, 2))
        level, carried = held_write(2 * a_now - a_before, numerator, wall, remainder)
        a_next = one_number(board.states[g].lines[0].now)
        assert a_next == int(level) and one_number(board.states[g].write_remainders[0]) == int(carried)
        assert one_number(board.states[g].lines[0].before) == a_now
        read = board_readings.uniform_mode(board, g)
        assert tuple(read) == (a_next, 0, a_now, 0, 27)
        levels.append(a_next)
        rotations.append(((nxt + before) * 6000 * GAMMA * GAMMA, now, clock))
    assert levels[-1] - 60 > 300 and all(b >= a for a, b in zip(levels[:-1], levels[1:], strict=True))
    seconds = [c - 2 * b + a for a, b, c in zip(levels[:-2], levels[1:-1], levels[2:], strict=True)]
    assert min(seconds) >= 0 and max(seconds) >= 2  # the write's increments, several levels per interval
    for (
        pair_sum,
        now,
        clock,
    ) in rotations:  # 2 cos omega = 2 - 2 (den - num) p_0^2 / (den Gamma^2), the band's line
        line = 2 * 6000 * GAMMA * GAMMA - 2 * 2000 * clock * clock
        assert abs(pair_sum - line * now) <= 3 * 6000 * GAMMA * GAMMA, (
            pair_sum,
            line,
            now,
        )  # the roundings
    first, last = rotations[0], rotations[-1]  # the record's level of either sign: signed fractions
    assert Fraction(last[0], last[1]) > Fraction(first[0], first[1])  # cos omega rose: the beat slowed
    for _ in range(20):
        board.step_inverse()
    back = [(x.now, x.before, x.remainder) for s in board.states for x in s.lines]
    assert all(
        np.array_equal(x, y)
        for was, is_ in zip(start, back, strict=True)
        for x, y in zip(was, is_, strict=True)
    )


def test_a_massless_rest_on_a_torus_is_the_poisson_solution_of_the_zero_mean_part():
    """(3) The rest (features/start `rest` with `free`, the flag of either key): a point source of 3,000 at the centre of a 7-cube torus at [1, 1], the level weight 1, Gamma 6,000: refused by name without the flag; with it the source less its read-weighted mean sums to under a millionth of one Node's line unit (`without_uniform`), the re-centred iteration's levels stand within two fine units of the exact zero-mean solution of the pace-weighted line, diag(num p_i^2) (6 I - S_6) b = the scaled source, solved sparse with one Node pinned and the mean restored (the test's floats, the oracle), the levels within one level of it, the floor at 0 at the Node farthest from the source and the centre above it; the line's residual within one act's floor at every Node but the roundings'."""
    counts, torus = np.zeros((7, 7, 7), dtype=np.int64), Wrap(True, True, True)
    counts[3, 3, 3] = 3000
    keys = {"own_weight": 1, "intervals": paces.COUNT_POWER}
    refused("needs a sink", rest, counts, (6000, 6000), torus, 1, MAX_WORK_INT, 3 * 6000, GAMMA, **keys)
    found = rest(counts, (6000, 6000), torus, 1, MAX_WORK_INT, 3 * 6000, GAMMA, free=True, **keys)
    clock, pace = paces.node_paces(GAMMA, found.content)
    reads = (6000 * pace.astype(object) * pace.astype(object)).ravel()
    scaled = scaled_source(counts * 3 * 6000 * found.unit * GAMMA**2, clock, pace, GAMMA, 2)
    zero_mean = without_uniform(np.asarray(scaled, dtype=np.int64), np.asarray(6000 * pace * pace))
    weighted = sum(
        int(s) / int(r) for s, r in zip(zero_mean.ravel().tolist(), reads.tolist(), strict=True)
    )
    assert abs(weighted) < 1e-6 and int(zero_mean.sum(dtype=object)) != 0  # the read-weighted mean out
    paths = [diags([1.0, 1.0], [-1, 1], shape=(7, 7)) + diags([1.0, 1.0], [-6, 6], shape=(7, 7))] * 3
    links = kronsum(kronsum(paths[0], paths[1]), paths[2])
    operator = (6.0 * diags(np.ones(343)) - links).tolil()
    source = (zero_mean.ravel() / np.array([float(r) for r in reads.tolist()])).astype(float)
    operator[0, :], source[0] = 0.0, 0.0
    operator[0, 0] = 1.0  # one Node pinned: the zero-mean line's solution up to its constant
    exact = spsolve(operator.tocsr(), source).reshape(counts.shape)
    exact -= exact.min()
    fine = found.fine.astype(object) - int(found.fine.min())
    assert int(found.fine.min()) == 0 and found.levels.min() == 0 and found.levels[3, 3, 3] > 0
    assert np.abs(fine.astype(float) - exact).max() <= 2.0, np.abs(fine.astype(float) - exact).max()
    assert (np.abs(found.levels - exact / found.unit) <= 1).all()
    assert found.levels[0, 0, 0] == 0  # the floor at the Node farthest from the source
    divisor = (6 * 6000 * pace * pace).astype(object)
    residual = (
        divisor * found.fine.astype(object)
        - 6000 * pace.astype(object) ** 2 * sum(arrivals(found.fine.astype(object), torus))
        - zero_mean.astype(object)
    )
    assert (np.abs(residual) < 2 * divisor).all()
