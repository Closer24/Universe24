"""The uniform mode on the board wrapped on every axis (ALGEBRA.md, The board's interval is no observable, a hypothesis under its own name, 2026-10-22; The closed lattice has no rest; item 6 of what is open, the closed board's double root; No write from outside Rule3 wakes either double root of the massless row): on a board periodic on every axis a massless held row's rest needs a sink, and the world's key `interval: unobservable` (loader/interval.py `interval_of`), or the law's `uniform: carried` of 2026-10-21 kept admitted beside it (loader/uniform.py `uniform_of`, the carried mean, the reader's line L2 on the design), admits the board by resting every massless row on the zero-mean part of its sources (features/start `rest`, `without_uniform`, `settled_free`) and leaving the k = 0 component to Rule3's own line, the double root carried at every Node by the step and the one write, no act added. (1) The declaration: the sink's refusal without either key names the hypothesis's key as the way; `interval` refused by name at any value but `unobservable`, where a face is open and where a face is closed (a board with a sink has no free uniform mode and its rest fixes the clock's unit beyond the face), the two keys together refused by name, a kick, a packet laid on a holder of the content, refused by name under the key (the mean's velocity the content's, nobody's declaration), and a massless row under the key without `pressure: trace` refused by name. (2) The volume form's write bit for bit and the attractor from rest (the momentum hand's derivation M12a, read cold by the reader, 2026-10-22): under the key the massless row carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1) (features/volume), its one write ((d + 1) X c + r) div (Gamma E_s T) at a wall that never moves, the level a reading of the record; a matter record laid uniform over a 3-cube torus at the band's rest rotation sources a uniform write, so X is one number at every Node at every interval, and over 40 intervals its second difference is the one write's increment computed beside from the engine's own functions, bit for bit, under the rounded factor and under the carried factor at the wall fixed per Node, the remainder the write's; the level reading relaxes to the constraint from rest, the residual from -1 toward 0, the velocity under the volume form's bound, U within 2 percent of the test's own integration of X'' = (d + 1) X s / Gamma at the law's own interval. (2b) The law's key as written: Rule3 carries the uniform line bit for bit on the torus under `uniform: carried`, the time line the level itself, the write (w D' + r) div (E_s T), and the 20 intervals run back return the start bit for bit. (3) The rest: a point source on a 7-cube torus at [1, 1] rests on the zero-mean part, the read-weighted mean taken out exactly to under a millionth of a line unit, the fine levels within two fine units of the pace-weighted Poisson solution solved sparse (floats, the test's oracle), the floor at 0 and the levels within one level."""

import math
from fractions import Fraction

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
from tests.laws import BACK, refused
from tests.laws_interval import (
    ACTION,
    GAMMA,
    TORUS,
    laid_torus,
    lockstep,
    one_number,
    uniform_world,
    universe_at_weight_one,
    volume_universe,
)


def test_the_board_declares_its_interval_unobservable_and_refuses_it_by_name_where_a_face_sinks_it(
    tmp_path, monkeypatch
):
    """(1) The declaration (loader/interval.py `interval_of`, `one_key`, `kicks_refused`, `volume_rows`; loader/uniform.py `uniform_of` beside it): a massless row's rest on a torus is refused by name without either key, the refusal naming `interval: unobservable` as the way and the law's `uniform: carried` beside it; `interval` at a value other than `unobservable` is refused by name; `unobservable` with the x face open or the z face closed is refused by name, a board with a sink having no free uniform mode; the two keys on one world are refused by name together; a `packets` entry on gravity, a kick on the holder of the content, is refused by name under the key; a held massless row under the key without `pressure: trace` is refused by name (the volume's exponent is the trace's one weight); `unobservable` on the torus loads at the volume form's integers under `factor: rounded` and under `factor: carried` alike, the world holding the declaration and gravity carrying its volume (`motion_volume`; the start's one conversion, both levels the volume of the rest 60; the wall fixed per Node kept by the lattice under the carry alone), and so does the law's `carried` (the old key kept admitted, the reader's line L2 on the design: the time line the level itself, no volume); a held row's `booking` at a word other than `count` or `form`, and `form` on the holder of the sign, are refused by name (loader/universe.booking_of)."""
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
    untraced = refused(
        "declares no `pressure: trace`", load_world, uniform_world(tmp_path, "flat", **key)
    )
    assert "'gravity'" in str(untraced) and "d + 1" in str(untraced) and "drop the key" in str(untraced)
    rest_volume = int(volume.volume_of(GAMMA, np.array(60)))
    for factor in ("rounded", "carried"):
        volume_universe(tmp_path, factor)
        board = Lattice(load_world(laid_torus(tmp_path, f"torus_{factor}", **key)))
        g = [family.name for family in board.families].index("gravity")
        assert board.world.unobservable and not board.world.uniform
        assert board.world.periodic == (True, True, True) and board.families[g].motion_volume
        assert board.families[g].factor_carried == (factor == "carried") == (g in board.fixed_walls)
        line = board.states[g].lines[0]
        assert one_number(line.now) == one_number(line.before) == rest_volume
    law = Lattice(load_world(laid_torus(tmp_path, "law", uniform="carried")))
    assert law.world.uniform and not law.world.unobservable  # the law as written, kept and runnable
    assert not law.families[g].motion_volume and one_number(law.states[g].lines[0].now) == 60
    universe_at_weight_one(tmp_path, gravity={"booking": "clock"})
    worded = refused("held.booking is one of", load_world, uniform_world(tmp_path, "worded", **key))
    assert "'clock'" in str(worded) and "'count', 'form'" in str(worded)
    universe_at_weight_one(tmp_path, charge={"booking": "form"})
    signed = refused(
        "holder of the sign books its Wronskian", load_world, uniform_world(tmp_path, "sign", **key)
    )
    assert "The form's own clock" in str(signed)


def test_the_volumes_write_is_bit_for_bit_at_either_factor_and_the_level_reading_relaxes_to_the_constraint(
    tmp_path, monkeypatch
):
    """(2) T2, the volume form's write bit for bit and the attractor from rest (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; the momentum hand's derivation M12a read cold by the reader, 2026-10-22; features/volume, records.write_sources, Lattice.fixed_walls; the reader's line L4: gravity declares `booking: form`): on the 3-cube torus under `interval: unobservable` at the volume form's integers (T 36,000, the width 92) with the uniform matter record, under `factor: rounded` and under `factor: carried` in turn, over 40 intervals gravity's time line is one number X at every Node, its write remainder one number, its three tension lines 0, X at the start the volume of the rest 60, and X(t + 1) - 2 X(t) + X(t - 1) is exactly ((d + 1) X(t) c + r) div (Gamma E_s T) under the rounding, c = k_w D' the record's form scaled by `paces.write_factor` at the paces of the level reading a(t) = `volume.level_of(X(t))` (the content matter reads; one power, the form's own clock; the uniform record's stress parts 0, so the trace's pressure term is 0 and the write the form's alone), and under the carry exactly ((d + 1) X(t) c' + r) div (Gamma W) with W = E_s T Gamma p_0(60)^2 the Node's wall at the rest's paces kept for the run and c' = rounded(k_w D p^3 W, E_s T Gamma p_0(a)^2) the carried product at the ratio of the walls, rounded once as a coefficient, the division the held write's own (features/held_write) and the remainder after it the engine's in both; the level reading a(t) is what the board reads (`board_readings.eras` with the remainder 0, `uniform_mode` a NamedTuple), rising by several levels per interval; the velocity in levels per interval never above the volume form's bound sqrt(Gamma s_0 / (d + 1)) (the test's floats, s_0 the first write c / (E_s T) in levels: Gamma U'' = s - (d + 1) Gamma U'^2 has its terminal velocity there), the level at the intervals 10, 20 and 40 within 2 percent of the test's own integration of the volume's map X(t + 1) = 2 X(t) - X(t - 1) + (d + 1) X(t) s(U(t)) / Gamma at the law's own interval, U = ln(X / Gamma) / (d + 1) and s(U) the write at U from the record's own form (A^2 sin omega' kept, cos omega' = 1 - N^2 / 3) and factor (N^4); the constraint's residual from `board_readings.eras` -1 at the start and rising toward 0 at every tenth interval (the attractor reached from rest, the chain rule's own); the writes' reading matter's alone and no seed Node; the two factors' levels within one level of each other over the 40 intervals (the ratio's one rounding on a product of forty bits)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    levels = {}
    for factor in ("rounded", "carried"):
        volume_universe(tmp_path, factor)
        board = Lattice(load_world(laid_torus(tmp_path, f"volume_{factor}", interval="unobservable")))
        names = [family.name for family in board.families]
        g, m = names.index("gravity"), names.index("matter")
        wall, course = board.walls(g)[0], lockstep(board, g, m, 40)
        fixed = one_number(board.fixed_walls[g][0]) if factor == "carried" else None
        assert wall == 36000 and course[0]["level"] == int(volume.volume_of(GAMMA, np.array(60)))
        for step in course:
            form = step["now"] * step["now"] - step["next"] * step["before_record"]
            a = int(volume.level_of(GAMMA, np.array(step["level"])))
            clock, pace = paces.node_paces(GAMMA, a)  # matter reads gravity at 1, the level reading
            if fixed is None:
                scaled = int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, 1))
                divisor = GAMMA * wall
            else:
                assert fixed == wall * GAMMA * paces.clock(GAMMA, 60) ** 2  # the rest's wall, kept
                scaled = int(paces.rounded(form * pace**3 * fixed, wall * GAMMA * clock * clock))
                divisor = GAMMA * fixed
            numerator = volume.EXPONENT * step["level"] * scaled
            level, carried = held_write(
                2 * step["level"] - step["before"], numerator, divisor, step["remainder"]
            )
            assert (step["after"], step["remainder_after"]) == (int(level), int(carried))
            step["write"], step["a"] = form * pace**3 / (GAMMA * clock * clock) / wall, a
            step["a_after"] = int(volume.level_of(GAMMA, np.array(step["after"])))
            read = step["eras"]
            assert (read.level, read.level_remainder, read.before, read.nodes) == (
                step["a_after"],
                0,
                a,
                27,
            )
        first = course[0]
        velocity = [step["a_after"] - step["a"] for step in course]
        bound = math.sqrt(GAMMA * first["write"] / volume.EXPONENT)
        assert 0 < max(velocity) <= bound + 1 and velocity[0] > 0 and min(velocity) > 0
        model = integrated(first["write"], first["level"], 40)
        for t in (10, 20, 40):
            assert abs(course[t - 1]["a_after"] / GAMMA / model[t] - 1) < 0.02, (factor, t)
        residual = [step["eras"].nature[0] / step["eras"].nature[1] - 1 for step in course]
        assert -1 <= residual[0] < -0.95 and residual[-1] < 0
        assert all(b > a for a, b in zip(residual[::10], residual[10::10], strict=False))
        read, mode = course[-1]["eras"], board_readings.uniform_mode(board, g)
        assert tuple(mode) == (course[-1]["a_after"], 0, course[-1]["a"], 0, 27)
        assert dict(read.writes)["matter"] > 0 and read.seed == (0, 0, 0)
        levels[factor] = [step["a_after"] for step in course]
    assert max(abs(c - r) for c, r in zip(levels["carried"], levels["rounded"], strict=True)) <= 1


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


def test_rule3_carries_the_uniform_line_bit_for_bit_on_a_torus_and_the_inverse_returns(
    tmp_path, monkeypatch
):
    """(2b) The law's key as written (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line, the clause of 2026-10-21 kept by name; the reader's line L1 on the engine half): on the 3-cube torus under `uniform: carried` with the uniform matter record at the rule's own integers, over 20 intervals gravity's time line is the level itself, one number at every Node (the write uniform, the Links' sum 0), its write remainder one number, its three tension lines 0, and a(t + 1) - 2 a(t) + a(t - 1) is exactly the one write's increment (w D' + r) div (E_s T) with D' the record's form scaled per proper volume and per proper interval at the paces of the content it reads (gravity's level; the law's two powers on a count), computed beside from `paces.write_factor` and features/held_write, the remainder after it the engine's too, no hill and no volume; the content rises and the record's rotation (next + before) / now at the centre falls along the band's line 2 - 2 (den - num) p_0^2 / (den Gamma^2) within the roundings; `board_readings.uniform_mode` reads the level with the remainder 0 (a NamedTuple, no string key in the engine); the 20 intervals run back return the start bit for bit (`Lattice.step_inverse`, the gate's snapshot)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path)
    board = Lattice(load_world(laid_torus(tmp_path, "law", uniform="carried")))
    names = [family.name for family in board.families]
    g, m = names.index("gravity"), names.index("matter")
    wall, start = board.walls(g)[0], BACK.snapshot(board)
    assert wall == ACTION and not board.families[g].motion_volume  # E_s T at the level weight 1
    course, rotations = lockstep(board, g, m, 20), []
    for step in course:
        form = step["now"] * step["now"] - step["next"] * step["before_record"]
        clock, pace = paces.node_paces(GAMMA, step["level"])  # matter reads gravity at 1, the content
        numerator = int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, 2))
        level, carried = held_write(
            2 * step["level"] - step["before"], numerator, wall, step["remainder"]
        )
        assert (step["after"], step["remainder_after"]) == (int(level), int(carried))
        assert (step["eras"].level, step["eras"].before) == (step["after"], step["level"])
        rotations.append(
            ((step["next"] + step["before_record"]) * 6000 * GAMMA * GAMMA, step["now"], clock)
        )
    assert tuple(board_readings.uniform_mode(board, g)) == (
        course[-1]["after"],
        0,
        course[-1]["level"],
        0,
        27,
    )
    levels = [step["after"] for step in course]
    assert levels[-1] - 60 > 300 and all(b >= a for a, b in zip(levels[:-1], levels[1:], strict=True))
    seconds = [c - 2 * b + a for a, b, c in zip(levels[:-2], levels[1:-1], levels[2:], strict=True)]
    assert min(seconds) >= 0 and max(seconds) >= 2  # the write's increments, several levels per interval
    for pair_sum, now, clock in rotations:  # 2 cos omega = 2 - 2 (den - num) p_0^2 / (den Gamma^2)
        line = 2 * 6000 * GAMMA * GAMMA - 2 * 2000 * clock * clock
        assert abs(pair_sum - line * now) <= 3 * 6000 * GAMMA * GAMMA, (pair_sum, line, now)
    first, last = rotations[0], rotations[-1]  # the record's level of either sign: signed fractions
    assert Fraction(last[0], last[1]) > Fraction(first[0], first[1])  # cos omega rose: the beat slowed
    for _ in range(20):
        board.step_inverse()
    assert BACK.first_difference(start, BACK.snapshot(board)) is None


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
