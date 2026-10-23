"""The uniform mode on the board wrapped on every axis (ALGEBRA.md, The board's interval is no observable; The closed lattice has no rest; item 6 of what is open, the closed board's double root; No write from outside Rule3 wakes either double root of the massless row; the owner's law of one Node, 2026-10-22, and his rule of 2026-10-23, no more keys in the code): on a board periodic on every axis a massless held row rests on the zero-mean part of its sources (features/start `rest`, `without_uniform`, `settled_free`) and leaves the k = 0 component to Rule3's own line, the double root carried at every Node by the step and the one write, no act added and no key of the world. (1) The declaration: the torus loads with no key, the row carrying its time line as the volume's level; the former keys `interval`, `uniform`, `booking`, `factor` and `pressure` meet the ordinary refusal of an unknown key; a kick, a packet laid on a holder of the content, is refused by name (the mean's velocity the content's, nobody's declaration). (2) The volume form's write bit for bit and the attractor from rest (the momentum hand's derivation M12a, read cold by the reader, 2026-10-22): the massless row carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1) (features/volume), its one write ((d + 1) X c + r) div (Gamma E_s T) at the wall fixed per Node, the level a reading of the record; a matter record laid uniform over a 3-cube torus at the band's rest rotation sources a uniform write, so X is one number at every Node at every interval, and over 40 intervals its second difference is the one write's increment computed beside from the engine's own functions, bit for bit, the remainder the write's; the level reading relaxes to the constraint from rest, the residual from -1 toward 0, the velocity under the volume form's bound, U within 2 percent of the test's own integration of X'' = (d + 1) X s / Gamma at the law's own interval. (3) The rest: a point source on a 7-cube torus at [1, 1] rests on the zero-mean part, the read-weighted mean taken out exactly to under a millionth of a line unit, the fine levels within two fine units of the pace-weighted Poisson solution solved sparse (floats, the test's oracle), the floor at 0 and the levels within one level."""

import math

import numpy as np
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import spsolve

from event_universe import board_readings, world_files
from event_universe.core import paces
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.ports import Wrap
from event_universe.features import volume
from event_universe.features.held_write import held_write
from event_universe.features.start import arrivals, rest, scaled_source, without_uniform
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import refused
from tests.laws_interval import (
    GAMMA,
    laid_torus,
    lockstep,
    one_number,
    uniform_world,
    universe_at_weight_one,
    volume_universe,
)


def test_every_wrapped_boards_interval_is_unobservable_and_the_former_keys_are_refused_by_name(
    tmp_path, monkeypatch
):
    """(1) The declaration under the law of one Node (loader/interval.py `volume_rows`, `kicks_refused`; the owner's law of 2026-10-22 and his rule of 2026-10-23, no more keys in the code): a massless row's rest on a torus needs no key, the board loads and the row carries its time line as the volume's level, the vacuum's volume X(60) at rest, its write at the wall fixed per Node; the world's former keys `interval` and `uniform` and the held row's former keys `booking`, `factor` and `pressure` each meet the loader's ordinary refusal of an unknown key; a kick, a packet laid on a holder of the content, is refused by name (ALGEBRA.md, No write from outside Rule3 wakes either double root of the massless row)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    rest_volume = int(volume.volume_of(GAMMA, np.array(60)))
    board = Lattice(load_world(laid_torus(tmp_path, "torus")))
    g = [family.name for family in board.families].index("gravity")
    assert board.world.periodic == (True, True, True) and board.families[g].motion_volume
    assert g in board.fixed_walls  # the carried factor, the wall fixed per Node for the run
    line = board.states[g].lines[0]
    assert one_number(line.now) == one_number(line.before) == rest_volume
    for key, word in (("interval", "unobservable"), ("uniform", "carried"), ("interval", "kept")):
        refused(f"unknown key '{key}'", load_world, uniform_world(tmp_path, key, **{key: word}))
    kick = [{"family": "gravity", "along": "x", "wave": [1, 3], "phase": [0, 1], "amplitude": 1}]
    kicked = refused(
        "lays a kick on 'gravity'", load_world, uniform_world(tmp_path, "kick", packets=kick)
    )
    assert "nobody's declaration" in str(kicked) and "the clause of 2026-10-22" in str(kicked)
    for key, word in (("booking", "form"), ("factor", "carried"), ("pressure", "trace")):
        universe_at_weight_one(tmp_path, gravity={key: word})
        refused(f"unknown key '{key}'", load_world, uniform_world(tmp_path, key))


def test_the_volumes_write_is_bit_for_bit_at_the_fixed_wall_and_the_level_reading_relaxes_to_the_constraint(
    tmp_path, monkeypatch
):
    """(2) T2, the volume form's write bit for bit and the attractor from rest (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; the momentum hand's derivation M12a read cold by the reader, 2026-10-22; features/volume, records.write_sources, Lattice.held_write): on the 3-cube torus at T 36,000 with the uniform matter record, forty intervals in lockstep, the engine's own numbers at every interval: the volume's write (d + 1) X_now c with c the record's form scaled to the wall fixed per Node (the rest's wall, Gamma E_s T times the rest's paces' Gamma p_0^2) over Gamma times the fixed wall by `held_write`, the carried remainder bit for bit; the level reading a = level_of(X) rising from 60 at a velocity within the bound sqrt(Gamma s / (d + 1)) + 1 per interval and never falling; the integrated map in floats within 2 percent of the level at 10, 20 and 40; the nature residual from -1 toward 0 and rising; the board's uniform mode reading the same numbers (board_readings.uniform_mode)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    board = Lattice(load_world(laid_torus(tmp_path, "volume")))
    names = [family.name for family in board.families]
    g, m = names.index("gravity"), names.index("matter")
    wall, course = board.walls(g)[0], lockstep(board, g, m, 40)
    fixed = one_number(board.fixed_walls[g][0])
    assert wall == 36000 and course[0]["level"] == int(volume.volume_of(GAMMA, np.array(60)))
    assert fixed == wall * GAMMA * paces.clock(GAMMA, 60) ** 2  # the rest's wall, kept for the run
    for step in course:
        form = step["now"] * step["now"] - step["next"] * step["before_record"]
        a = int(volume.level_of(GAMMA, np.array(step["level"])))
        clock, pace = paces.node_paces(GAMMA, a)  # matter reads gravity at 1, the level reading
        scaled = int(paces.rounded(form * pace**3 * fixed, wall * GAMMA * clock * clock))
        numerator = volume.EXPONENT * step["level"] * scaled
        level, carried = held_write(
            2 * step["level"] - step["before"], numerator, GAMMA * fixed, step["remainder"]
        )
        assert (step["after"], step["remainder_after"]) == (int(level), int(carried))
        step["write"], step["a"] = form * pace**3 / (GAMMA * clock * clock) / wall, a
        step["a_after"] = int(volume.level_of(GAMMA, np.array(step["after"])))
        read = step["eras"]
        assert (read.level, read.level_remainder, read.before, read.nodes) == (step["a_after"], 0, a, 27)
    first = course[0]
    velocity = [step["a_after"] - step["a"] for step in course]
    bound = math.sqrt(GAMMA * first["write"] / volume.EXPONENT)
    assert 0 < max(velocity) <= bound + 1 and velocity[0] > 0 and min(velocity) > 0
    model = integrated(first["write"], first["level"], 40)
    for t in (10, 20, 40):
        assert abs(course[t - 1]["a_after"] / GAMMA / model[t] - 1) < 0.02, t
    residual = [step["eras"].nature[0] / step["eras"].nature[1] - 1 for step in course]
    assert -1 <= residual[0] < -0.95 and residual[-1] < 0
    assert all(b > a for a, b in zip(residual[::10], residual[10::10], strict=False))
    read, mode = course[-1]["eras"], board_readings.uniform_mode(board, g)
    assert tuple(mode) == (course[-1]["a_after"], 0, course[-1]["a"], 0, 27)
    assert dict(read.writes)["matter"] > 0 and read.seed == (0, 0, 0)


def integrated(s0, X0, steps):  # type: ignore[no-untyped-def]
    """The volume's map at the law's own interval, the test's floats: X(t + 1) = 2 X(t) - X(t - 1) + (d + 1) X(t) s(U(t)) / Gamma from rest, U = ln(X / Gamma) / (d + 1), s(U) = s0 (sin omega'(U) / sin omega'(U0)) (N(U) / N(U0))^4 the record's own form at the write's factor under the form's own clock, cos omega' = 1 - N^2 / 3 the band's rest rotation of [4000, 6000] at the pace N = (1 - 1 / Gamma)^(Gamma U); the levels U from 0 through `steps`."""

    def sine(U):  # type: ignore[no-untyped-def]
        cosine = 1 - (1 - 1 / GAMMA) ** (2 * GAMMA * U) / 3
        return math.sqrt(1 - cosine * cosine)

    def level(X):  # type: ignore[no-untyped-def]
        return math.log(X / GAMMA) / volume.EXPONENT

    before, now, U0 = X0, X0, level(X0)
    course = [U0]
    for _ in range(steps):
        U = level(now)
        write = s0 * sine(U) / sine(U0) * (1 - 1 / GAMMA) ** (4 * GAMMA * (U - U0))
        before, now = now, 2 * now - before + volume.EXPONENT * now * write / GAMMA
        course.append(level(now))
    return course


def test_a_massless_rest_on_a_torus_is_the_poisson_solution_of_the_zero_mean_part():
    """(3) The rest (features/start `rest`; every wrapped board's massless row rests free under the law of one Node): a point source of 3,000 at the centre of a 7-cube torus at [1, 1], the level weight 1, Gamma 6,000: the source less its read-weighted mean sums to under a millionth of one Node's line unit (`without_uniform`), the re-centred iteration's levels stand within two fine units of the exact zero-mean solution of the pace-weighted line, diag(num p_i^2) (6 I - S_6) b = the scaled source, solved sparse with one Node pinned and the mean restored (the test's floats, the oracle), the levels within one level of it, the floor at 0 at the Node farthest from the source and the centre above it; the line's residual within one act's floor at every Node but the roundings'."""
    counts, torus = np.zeros((7, 7, 7), dtype=np.int64), Wrap(True, True, True)
    counts[3, 3, 3] = 3000
    keys = {"own_weight": 1, "intervals": paces.COUNT_POWER}
    found = rest(counts, (6000, 6000), torus, 1, MAX_WORK_INT, 3 * 6000, GAMMA, **keys)
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
