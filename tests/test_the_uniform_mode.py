"""The uniform mode on the board wrapped on every axis (ALGEBRA.md, The board's interval is no observable, a hypothesis under its own name, 2026-10-22; The closed lattice has no rest; item 6 of what is open, the closed board's double root; No write from outside Rule3 wakes either double root of the massless row): on a board periodic on every axis a massless held row's rest needs a sink, and the world's key `interval: unobservable` (loader/interval.py `interval_of`), or the law's `uniform: carried` of 2026-10-21 kept admitted beside it (loader/uniform.py `uniform_of`, the carried mean with no hill, the reader's line L2 on the design), admits the board by resting every massless row on the zero-mean part of its sources (features/start `rest`, `without_uniform`, `settled_free`) and leaving the k = 0 component to Rule3's own line, the double root carried at every Node by the step and the one write, no act added. (1) The declaration: the sink's refusal without either key names the hypothesis's key as the way; `interval` refused by name at any value but `unobservable`, where a face is open and where a face is closed (a board with a sink has no free uniform mode and its rest fixes the clock's unit beyond the face), the two keys together refused by name, and a kick, a packet laid on a holder of the content, refused by name under the key (the mean's velocity the content's, nobody's declaration). (2) The hill's write bit for bit and the attractor from rest: a matter record laid uniform over a 3-cube torus at the band's rest rotation sources a uniform write, so gravity's level is one number at every Node at every interval, and over 40 intervals its second difference is the one write's increment (k_w D' - K v^2 + r) div (E_s T), the numerator the form scaled by the write's factor at the record's own content less the row's own kinetic form at the symmetry's weight K, computed beside from the engine's own functions, bit for bit, the remainder the write's; the tensions 0 (a uniform record has none); the velocity relaxing to the constraint from rest as the test's own integration of the law's line has it, the constraint's residual from -1 toward 0; the uniform reading one division with one remainder; the run back refused by name (T5). (3) The rest: a point source on a 7-cube torus at [1, 1] rests on the zero-mean part, the read-weighted mean taken out exactly to under a millionth of a line unit, the fine levels within two fine units of the pace-weighted Poisson solution solved sparse (floats, the test's oracle), the floor at 0 and the levels within one level."""

import math

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
from event_universe.world_files import load_world
from tests.laws import refused
from tests.laws_interval import (
    ACTION,
    GAMMA,
    TORUS,
    laid_torus,
    lockstep,
    uniform_world,
    universe_at_weight_one,
)


def test_the_board_declares_its_interval_unobservable_and_refuses_it_by_name_where_a_face_sinks_it(
    tmp_path, monkeypatch
):
    """(1) The declaration (loader/interval.py `interval_of`, `one_key`, `kicks_refused`; loader/uniform.py `uniform_of` beside it): a massless row's rest on a torus is refused by name without either key, the refusal naming `interval: unobservable` as the way and the law's `uniform: carried` beside it; `interval` at a value other than `unobservable` is refused by name; `unobservable` with the x face open or the z face closed is refused by name, a board with a sink having no free uniform mode; the two keys on one world are refused by name together; a `packets` entry on gravity, a kick on the holder of the content, is refused by name under the key; `unobservable` on the torus loads, the world holding the declaration, and so does the law's `carried` (the old key kept admitted, the reader's line L2 on the design); a held row's `booking` at a word other than `count` or `form`, and `form` on the holder of the sign, are refused by name (loader/universe.booking_of), and its `weight` at a word other than `mix` or `gap` (loader/universe.hill_weight_of)."""
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
    universe_at_weight_one(tmp_path, gravity={"booking": "clock"})
    worded = refused("held.booking is one of", load_world, uniform_world(tmp_path, "worded", **key))
    assert "'clock'" in str(worded) and "'count', 'form'" in str(worded)
    universe_at_weight_one(tmp_path, charge={"booking": "form"})
    signed = refused(
        "holder of the sign books its Wronskian", load_world, uniform_world(tmp_path, "sign", **key)
    )
    assert "The form's own clock" in str(signed)
    universe_at_weight_one(tmp_path, gravity={"weight": "dust"})
    weighed = refused("held.weight is one of", load_world, uniform_world(tmp_path, "weighed", **key))
    assert "'dust'" in str(weighed) and "'mix', 'gap'" in str(weighed)


def test_the_hill_at_the_symmetrys_weight_writes_bit_for_bit_and_the_velocity_relaxes_to_the_constraint(
    tmp_path, monkeypatch
):
    """(2) T2, the hill's write bit for bit and the attractor from rest (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line, the clause of 2026-10-22; The motion of gravity's row is a hill at the symmetry's weight; The mean's velocity is the content's; the reader's line L4: gravity declares `booking: form`): on the 3-cube torus under `interval: unobservable` with the uniform matter record, at T 32,768 and at T 36,000, over 40 intervals gravity's time line is one number at every Node, its write remainder one number, its three tension lines 0, and a(t + 1) - 2 a(t) + a(t - 1) is exactly (k_w D' - K v^2 + r) div (E_s T + K v), the symmetric hill (the derivation M11j: the drag -K v_in v_out implicit in a(t + 1) by the one carried division at the wall E_s T + K v_in), with D' the record's form scaled by `paces.write_factor` at the paces of the content it reads (one power, the form's own clock), K = `paces.motion_weight([D'], [5], E_s T, Gamma, 6)` (27 at T 32,768, 30 at 36,000, the symmetry's integers), v = a(t) - a(t - 1) the row's own velocity at the interval's start and the division the held write's own (features/held_write; `paces.motion_term` the one function of the hill's write, the term and the divisor), the remainder after it the engine's; the velocity in levels per interval never above the constraint's bound sqrt(2 Gamma s_0 / 5) (the test's floats, s_0 the first write), its maximum within one level of the test's own integration of the model at the law's own interval, v(t + 1) = v(t) + (s(U) - c v^2 / Gamma) / (1 + c v / Gamma) and U(t + 1) = U(t) + v(t + 1) / Gamma with c = K Gamma / (E_s T) (the symmetric map's line, Gamma U'' (1 + c U') = s - c Gamma U'^2) and s(U) the write at U from the record's own form (A^2 sin omega' kept, cos omega' = 1 - N^2 / 3) and factor (N^4), the model's interval of the maximum within two intervals of the engine's plateau, U at the intervals 10, 20 and 40 within 2 percent of the model (0.25 percent measured; the symmetry hand's 9-cube within 1.3 percent); the constraint's residual from `board_readings.eras` -1 at the start and rising toward 0 at every tenth interval, the hill's weight one number at every Node (the mix of one form); `uniform_mode` reads the level with the remainder 0 on the lockstep board; the run back refused by name (T5, tests/test_the_interval.py)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    for action, weight in ((ACTION, 27), (36000, 30)):
        universe_at_weight_one(tmp_path, action=action, gravity={"booking": "form"})
        board = Lattice(load_world(laid_torus(tmp_path, f"hill_{action}", interval="unobservable")))
        names = [family.name for family in board.families]
        g, m = names.index("gravity"), names.index("matter")
        wall, course = board.walls(g)[0], lockstep(board, g, m, 40)
        assert wall == action  # E_s T at the level weight 1
        for step in course:
            form = step["now"] * step["now"] - step["next"] * step["before_record"]
            clock, pace = paces.node_paces(
                GAMMA, step["level"]
            )  # matter reads gravity at 1, the content
            scaled = int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, 1))
            hill = paces.motion_weight([np.array(scaled)], [5], wall, GAMMA, 6)
            assert int(hill) == weight and step["eras"].weight_low == step["eras"].weight_high == weight
            term, divisor = paces.motion_term(step["level"], step["before"], int(hill), wall)
            numerator = scaled + int(term)
            level, carried = held_write(
                2 * step["level"] - step["before"], numerator, divisor, step["remainder"]
            )
            assert (step["after"], step["remainder_after"]) == (int(level), int(carried))
            step["write"] = scaled / wall
        first, velocity = course[0], [step["after"] - step["level"] for step in course]
        bound = math.sqrt(2 * GAMMA * first["write"] / 5)
        assert 0 < max(velocity) < bound and velocity[0] > 0
        model = integrated(first["write"], first["level"] / GAMMA, weight * GAMMA / wall, 40)
        top = max(range(len(model)), key=lambda t: model[t][1])
        plateau = [t + 1 for t, v in enumerate(velocity) if v == max(velocity)]
        assert abs(max(velocity) - model[top][1]) <= 1 and min(abs(top - t) for t in plateau) <= 2
        for t in (10, 20, 40):
            assert abs(course[t - 1]["after"] / GAMMA / model[t][0] - 1) < 0.02, (action, t)
        residual = [step["eras"].residual[0] / step["eras"].residual[1] - 1 for step in course]
        assert -1 <= residual[0] < -0.95 and residual[-1] < 0
        assert all(b > a for a, b in zip(residual[::10], residual[10::10], strict=False))
        read, mode = course[-1]["eras"], board_readings.uniform_mode(board, g)
        assert tuple(mode) == (course[-1]["after"], 0, course[-1]["level"], 0, 27)
        assert (read.level, read.level_remainder, read.before, read.nodes) == (
            mode.level,
            0,
            mode.before,
            27,
        )
        assert dict(read.writes)["matter"] > 0 and read.seed == (0, 0, 0)


def integrated(s0, U0, c, steps):  # type: ignore[no-untyped-def]
    """The model at the law's own interval, the test's floats: v(t + 1) = v(t) + (s(U(t)) - c v(t)^2 / Gamma) / (1 + c v(t) / Gamma), the symmetric hill's map (the derivation M11j), and U(t + 1) = U(t) + v(t + 1) / Gamma from rest, s(U) = s0 (sin omega'(U) / sin omega'(U0)) (N(U) / N(U0))^4 the record's own form at the write's factor under the form's own clock, cos omega' = 1 - N^2 / 3 the band's rest rotation of [4000, 6000] at the pace N = (1 - 1 / Gamma)^(Gamma U); the pairs (U, v) from 0 through `steps`."""

    def sine(U):  # type: ignore[no-untyped-def]
        cosine = 1 - (1 - 1 / GAMMA) ** (2 * GAMMA * U) / 3
        return math.sqrt(1 - cosine * cosine)

    U, v, course = U0, 0.0, [(U0, 0.0)]
    for _ in range(steps):
        write = s0 * sine(U) / sine(U0) * (1 - 1 / GAMMA) ** (4 * GAMMA * (U - U0))
        v = v + (write - c * v * v / GAMMA) / (1 + c * v / GAMMA)
        U = U + v / GAMMA
        course.append((U, v))
    return course


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
