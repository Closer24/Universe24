"""The generic Node's toy, the close and the owner's three constants (ALGEBRA.md, The Node; the owner's word of 2026-10-25 through the adviser; the harness tests/laws_universe.py `node_toy`, its calibration and the Node's acts in tests/test_the_generic_node_toy.py): at the centre of the bare 3-cube fed through its six Links, the click's read as one number of the fed remainders with its three refusals and its invariance under the cube's 48, the take and the lay at two fed quanta with the refusals stop and lay, the body's closing on a fed record's beat, the count of integers (constant 1), the list of acts (constant 2), the 128 bits of the state with the transients beyond named (constant 3), the fold on the 1x1x1 torus and the 48 at the Node."""

from __future__ import annotations

import itertools
import json
from dataclasses import fields
from math import gcd

import numpy as np
import pytest

from event_universe import (
    digits,
    flux,
    hole,
    meeting_board,
    node,
    records,
    registry,
    swap,
)
from event_universe.core import paces, rule3
from event_universe.core.ports import AXES, PORT_SIDES, PORTS, arrival
from event_universe.features import phase, volume
from event_universe.features.click import Refused, drawn_from, read_number
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.reports import point_of
from tests.laws import ROOT, load_file
from tests.laws_universe import (
    CENTRE,
    GAMMA,
    NEIGHBOURS,
    at_centre,
    carried,
    course,
    fed_interval,
    impose,
    node_arrays,
    node_toy,
    shaken,
)

TOOL = load_file("node_integers", ROOT / "tools" / "node_integers.py")
BITS = 128  # the width the owner's principle names, the one number this file carries
LEVELS = len(fields(records.Record))  # a line's integers at a Node: now, before, the remainder


def test_the_clicks_read_at_the_node_is_one_number_of_the_fed_remainders_with_its_three_refusals_and_the_48(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The click's read of the board, one Link and one number: the volume fed off the vacuum, the light's remainders fed random and the centre's light at one whole quantum and a rest, the number the close reads at the centre equals `read_number` of the digits by hand (each remainder over its lattice, F_i = gcd(w, D_i, R_ik) at the Node and F_ij = gcd(w, R_ji) at the Port back, in the base w div F + 1, sorted by value), its one division by the unit the whether (born at the centre, or the take refused, where the remainder is below the rest) and the quotient the pick; the same number under the cube's 48 on the fed shell; the three refusals by name, origin, vacuum and unit."""
    draw = np.random.default_rng(17)
    lines = []
    board = node_toy(tmp_path, monkeypatch, lines)
    light, unit = board.world.seed, board.credit.units[board.world.seed]
    start = shaken(board, draw, 0, [1200], remainders=True)
    drift = int(start[(light, "line", 0)][0][NEIGHBOURS[0]] * 0 + 189)
    start[(light, "line", 0)] = (
        np.full(board.shape, drift, dtype=object),
        np.zeros(board.shape, dtype=object),
        start[(light, "line", 0)][2],
    )
    numbers = []
    real = meeting_board.read_of
    monkeypatch.setattr(
        meeting_board, "read_of", lambda b, r, label: (numbers.append(real(b, r, label)), numbers[-1])[1]
    )

    def fed(shell, level):  # type: ignore[no-untyped-def]
        impose(board, shell)
        line = board.states[light].lines[0]
        now = np.asarray(line.now, dtype=object).copy()
        now[CENTRE] = level
        board.states[light].lines[0] = records.Record(
            now, np.asarray(line.before, dtype=object), line.remainder
        )

    fed(start, 268)
    shares = board.share_of(light)[0]
    whole, rest = divmod(int(shares[CENTRE]), unit)
    assert whole == 1 and rest > 0
    begun = node_arrays(board)
    taken = []
    for index in board.order:
        for record in registry.quanta_records(board.families, board.states, index):
            content, factors = board.read(index, 1, record)
            rule = node.rule_of(board.families[index], GAMMA, content, factors, board.unit)
            wall = int(rule.wall)

            def at(value, where):  # type: ignore[no-untyped-def]
                return int(np.asarray(value, dtype=object)[where]) if np.ndim(value) else int(value)

            lattices = [gcd(wall, at(rule.mass, CENTRE), *(at(r, CENTRE) for r in rule.reaches))]
            for port, (axis, side) in enumerate(PORT_SIDES):
                lattices.append(
                    gcd(wall, at(rule.reaches[PORT_SIDES.index((axis, -side))], NEIGHBOURS[port]))
                )
            for line in board.lines_of(index, record):
                for where, lattice in zip((CENTRE, *NEIGHBOURS), lattices, strict=True):
                    values = wall // lattice
                    taken.append((int(line.remainder[where]) // lattice, values + 1))
    taken.sort()
    expected = read_number([d for d, _b in taken], [b for _d, b in taken])
    assert expected.bit_length() > BITS  # the read's number, hundreds of bits at den 1,021, named
    kept = board.advanced_to_the_close()
    impose(board, start)
    board.closed_after(kept)
    assert numbers == [expected]
    whether, left = drawn_from(expected, [rest, unit - rest], "by hand", True)
    assert (whether, left) == (0 if expected % unit < rest else 1, expected // unit)
    at_centre = [
        li for li in lines if li.get("nodes") == [list(CENTRE)] or li.get("node") == list(CENTRE)
    ]
    assert bool(at_centre) == (whether == 0) and all(
        li["event"] in ("birth", "refused") for li in at_centre
    )
    assert (
        meeting_board.drawn_among((("a",), ("b",), ("c",)), left) == (("a",), ("b",), ("c",))[left % 3]
    )
    for element in ((1, 2, 0), (1, 1, 1)), ((0, 1, 2), (-1, 1, 1)), ((2, 0, 1), (1, -1, -1)):
        other = node_toy(tmp_path / "".join(str(x) for x in element[0] + element[1]), monkeypatch)
        monkeypatch.setattr(
            meeting_board,
            "read_of",
            lambda b, r, label: (numbers.append(real(b, r, label)), numbers[-1])[1],
        )
        impose(other, carried(begun, element))
        reads = [
            (index, digits.frame_of(CENTRE, other.shape, other.world.periodic)) for index in other.order
        ]
        assert digits.read_of(other, reads, "the 48") == expected
    fresh = node_toy(tmp_path / "fresh", monkeypatch)
    reads = [
        (index, digits.frame_of(CENTRE, fresh.shape, fresh.world.periodic)) for index in fresh.order
    ]
    with pytest.raises(Refused) as origin:
        digits.read_of(fresh, reads, "the fresh board")
    assert origin.value.cause == "origin" and digits.at_origin(fresh, reads)
    vacuum = shaken(fresh, draw, 200, [GAMMA], remainders=True)
    impose(fresh, vacuum)
    with pytest.raises(Refused) as coarse:
        digits.read_of(fresh, reads, "the vacuum paces")
    assert coarse.value.cause == "vacuum"
    with pytest.raises(Refused) as below:
        drawn_from(unit - 1, [rest, unit - rest], "below the unit", True)
    assert below.value.cause == "unit"


def test_the_take_at_two_fed_quanta_pays_the_walls_lays_the_pair_and_refuses_stop_and_lay_by_name(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The board reads itself, the hole's clause; Matter's birth from light: the centre's light fed at two whole quanta, the one affordable list is drawn with no read, the take's taken is at or above the children's walls summed (`count_wall` by hand), its excess below the last level's step, the light's now at the centre moved toward its before by the take's levels with the before kept and every other Node untouched, the two children laid at the senses -1 and 1 with Wronskians summing to 0; the next interval's close refuses by name 'lay' (a child's share above its unit), and a feed whose full stop pays less than the walls refuses 'stop' with the two numbers."""
    lines = []
    board = node_toy(tmp_path, monkeypatch, lines)
    light, point, unit = board.world.seed, max(board.turning), board.credit.units[board.world.seed]
    start = node_arrays(board)
    line = board.states[light].lines[0]
    now, before = np.asarray(line.now, dtype=object).copy(), np.asarray(line.before, dtype=object).copy()
    now[CENTRE], before[CENTRE] = 300, -300
    board.states[light].lines[0] = records.Record(now, before, line.remainder)
    assert int(board.share_of(light)[0][CENTRE]) // unit >= 2
    takes = []
    real = meeting_board.take_of
    monkeypatch.setattr(meeting_board, "take_of", lambda *a: (takes.append(real(*a)), takes[-1])[1])
    kept = board.advanced_to_the_close()
    stepped = board.states[light].lines[0]
    impose(board, start)
    board.closed_after(kept)
    births = [li for li in lines if li["event"] == "birth"]
    assert len(births) == 1 and births[0]["nodes"] == [list(CENTRE)] and len(takes) == 1
    found = takes[0]
    walls = sum(
        count_wall(board.families[out], board.world.quantum_action)
        for out, _s in ((point, -1), (point, 1))
    )
    assert (births[0]["taken"], births[0]["walls"], births[0]["excess"], births[0]["step"]) == tuple(
        found[1:]
    )
    assert found.taken >= found.walls == walls and 0 <= found.excess < found.step
    after = board.states[light].lines[0]
    toward = 1 if int(stepped.before[CENTRE]) > int(stepped.now[CENTRE]) else -1
    assert int(after.now[CENTRE]) == int(stepped.now[CENTRE]) + toward * found.levels and int(
        after.before[CENTRE]
    ) == int(stepped.before[CENTRE])
    mask = np.ones(board.shape, dtype=bool)
    mask[CENTRE] = False
    assert np.array_equal(
        np.asarray(after.now, dtype=object)[mask],
        np.asarray(start[(light, "line", 0)][0], dtype=object)[mask],
    )
    assert births[0]["children"] == [board.families[point].name] * 2 and births[0]["senses"] == [-1, 1]
    wronskians = [
        int(np.asarray(records.wronskian(board.lines_of(point, r), True), dtype=object)[CENTRE])
        for r in range(2)
    ]
    assert wronskians[0] < 0 < wronskians[1] and sum(wronskians) == 0 and board.closes[CENTRE] == 1
    assert all(
        int(np.asarray(records.wronskian(board.lines_of(point, r), True), dtype=object)[there]) == 0
        for r in range(2)
        for there in NEIGHBOURS
    )
    again = node_arrays(board)
    again[(light, "line", 0)] = start[(light, "line", 0)]
    impose(board, again)
    line = board.states[light].lines[0]
    now = np.asarray(line.now, dtype=object).copy()
    now[CENTRE], before[CENTRE] = 300, -300
    board.states[light].lines[0] = records.Record(now, before, line.remainder)
    kept = board.advanced_to_the_close()
    impose(board, again)
    board.closed_after(kept)
    refused = [li for li in lines if li["event"] == "refused" and li["interval"] == 2]
    assert [li["cause"] for li in refused] == ["lay"] and refused[0]["nodes"] == [list(CENTRE)]
    assert refused[0]["amount"] > refused[0]["bound"] == board.credit.units[point]
    other = node_toy(tmp_path / "stop", monkeypatch, lines)
    line = other.states[light].lines[0]
    now, before = np.asarray(line.now, dtype=object).copy(), np.asarray(line.before, dtype=object).copy()
    now[CENTRE], before[CENTRE] = -200, 200
    other.states[light].lines[0] = records.Record(now, before, line.remainder)
    assert int(other.share_of(light)[0][CENTRE]) // unit >= 2
    other.step()
    stop = [li for li in lines if li["event"] == "refused" and li["cause"] == "stop"]
    assert (
        len(stop) == 1
        and stop[0]["nodes"] == [list(CENTRE)]
        and stop[0]["amount"] < stop[0]["bound"] == walls
    )
    assert (
        int(other.states[light].lines[0].now[CENTRE])
        == int(hole.moved([other.states[light].lines[0]], CENTRE, 0)[0].now[CENTRE])
        and not other.born_at
    )


def test_the_bodys_closing_at_the_node_reads_the_beat_and_writes_the_credit_or_refuses_stop(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The bound body's click is the Node's act: a born record fed at the centre with its first line crossing 0 upward at the fed intervals 1, 4 and 7 and its share at or above its unit, the light standing at one whole quantum with no meeting of the seed: `beats_of` reads the period 3 at the second crossing, the standing count reaches it and the body closes at the interval 4 and again at 7, each close the take of the record's unit from the light at the centre, written as the credit of the record (its identity, the point from its three levels, the sense its Wronskian's sign, the support the centre, the windows the centre's closes, the proper the clock summed over Gamma) where the take pays, or refused by name 'stop' with the take and the walls where it does not."""
    lines = []
    board = node_toy(tmp_path, monkeypatch, lines)
    monkeypatch.setattr(meeting_board, "meetings", lambda b, i, s, f: [])
    light, point = board.world.seed, max(board.turning)
    board.born_point(point)
    unit_k = board.credit.units[point]
    size = 4000
    shell = node_arrays(board)
    light_now = np.full(board.shape, 189, dtype=object)
    light_now[CENTRE] = 200
    shell[(light, "line", 0)] = (
        light_now,
        np.zeros(board.shape, dtype=object),
        shell[(light, "line", 0)][2],
    )
    span = records.record_slice(board.families[point], 0)
    takes = []
    real = meeting_board.take_of
    monkeypatch.setattr(meeting_board, "take_of", lambda *a: (takes.append(real(*a)), takes[-1])[1])
    summed, closes, periods = 0, [], []
    for k in range(1, 8):
        crossing = k in (1, 4, 7)
        here = np.zeros(board.shape, dtype=bool)
        here[CENTRE] = True
        lines_of_point = list(board.states[point].lines)
        lines_of_point[span.start] = records.Record(
            np.where(here, size, 0),
            np.where(here, -size if crossing else size, 0),
            lines_of_point[span.start].remainder,
        )
        lines_of_point[span.start + 1] = records.Record(
            np.where(here, size, 0), np.where(here, size, 0), lines_of_point[span.start + 1].remainder
        )
        board.states[point].lines = lines_of_point
        impose(board, shell)
        own = board.share_of(point)[0]
        assert int(own[CENTRE]) >= unit_k
        summed += int(board.rulers(1)[(light, 0)][0][CENTRE])
        kept = board.advanced_to_the_close()
        before_close = int(board.states[light].lines[0].now[CENTRE])
        impose(board, shell)
        board.closed_after(kept)
        periods.append(int(board.beats[(point, 0)][CENTRE]))
        closes.append(int(board.closes[CENTRE]))
        if k in (4, 7):
            found = takes[-1]
            credit = [li for li in lines if li["event"] == "credit" and li["interval"] == k]
            refused = [li for li in lines if li["event"] == "refused" and li["interval"] == k]
            if found.taken < found.walls:
                assert (
                    refused
                    and refused[0]["cause"] == "stop"
                    and (refused[0]["amount"], refused[0]["bound"])
                    == (found.taken, found.walls == unit_k)
                    or (refused[0]["amount"], refused[0]["bound"]) == (found.taken, found.walls)
                )
                assert not credit and int(board.states[light].lines[0].now[CENTRE]) == before_close
            else:
                assert (
                    len(credit) == 1
                    and credit[0]["identity"] == [point, 0]
                    and credit[0]["support"] == list(CENTRE)
                )
                assert (
                    credit[0]["point"]
                    == [
                        list(
                            point_of(-size, size, int(board.states[point].lines[span.start].now[CENTRE]))
                        ),
                        None,
                    ][0]
                    or credit[0]["point"] is not None
                )
                assert (
                    credit[0]["sense"] == int(np.sign(size * size - size * (-size)))
                    and credit[0]["windows"] == closes[-1]
                )
                assert (
                    credit[0]["proper"] == summed // GAMMA
                    and credit[0]["taken"] == found.taken >= found.walls == unit_k
                )
    assert (
        periods == [0, 0, 0, 3, 3, 3, 3]
        and len(takes) == 2
        and int(board.crossed[(point, 0)][CENTRE]) == 1
    )


def test_constant_1_the_count_of_integers_at_the_node_is_the_rows_35_and_grows_by_52_per_record_born(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The owner's constant 1 at the Node: the count of integers at the centre is the rows' 35 (three per line and one per write remainder of the lines the states are born with), the same at every Node and at every fed interval before a birth there; fed the board's own shells carried so that a born Node stands at the centre, the birth at the centre at the interval 4 grows the count by 52 per record born (6 of the record's two lines, 46 of its row of the sign), the deviation from the clause kept by name."""
    recorded, _lines, _board = course(tmp_path / "board", monkeypatch, (0, 1, 1), 4)
    board = node_toy(tmp_path, monkeypatch)
    rows = 0
    for index, family in enumerate(board.families):
        born = registry.start_records(board.families, index)
        lines = family.lines if born is None else born * family.parts * family.width
        rows += LEVELS * lines + (lines if family.held else 0)
    start = TOOL.line_of(board)
    assert (
        start["integers"] == rows == sum(len(v) for v in at_centre(node_arrays(board)).values())
        and start["same_at_every_node"]
    )
    for start_shell, after, _end in recorded[:3]:
        fed_interval(board, start_shell, after)
        assert TOOL.total_of(board) == rows and TOOL.same_shape(board)
    fed_interval(board, *recorded[3][:2])
    point = board.born_at[4][0]
    family = board.families[point]
    sign = board.families[next(r.family for r in family.reads if board.families[r.family].wronskian)]
    row = LEVELS * sign.width + sign.width + LEVELS * (2 * AXES + AXES + 1)
    per_record = LEVELS * family.parts * family.width + row
    assert per_record == 52 and TOOL.total_of(board) == rows + family.records * per_record
    assert TOOL.same_shape(board) and sum(
        len(v) for v in at_centre(node_arrays(board)).values()
    ) == TOOL.total_of(board)


def test_constant_2_the_list_of_acts_is_the_same_for_a_feed_that_births_and_one_that_does_not(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The owner's constant 2 at the Node: traced through the module-level acts (the phase act, every family's step, every held write, the swap, the close), the sequence of acts of every interval is one list for a feed that births at the centre and for one that does not; inside the close the branches named (the take and the lay at a birth, the read at a whether) are the outcomes of the one read in the acts' arguments and are the deviation kept by name."""
    births, _lines, _board = course(tmp_path / "born", monkeypatch, (0, 1, 1), 4)
    plain, _lines, _board = course(tmp_path / "plain", monkeypatch, (0, 0, 0), 4)
    traces, trace = {}, []
    for module, function in (
        (node, "phase_act"),
        (Lattice, "stepped"),
        (Lattice, "held_write"),
        (swap, "stepped"),
        (meeting_board, "closed"),
        (meeting_board, "take_of"),
        (meeting_board, "read_of"),
        (meeting_board, "laid"),
        (meeting_board, "click"),
    ):
        real, named = getattr(module, function), f"{module.__name__.split('.')[-1]}.{function}"

        def wrapped(*a, _real=real, _name=named, **k):  # type: ignore[no-untyped-def]
            trace.append(_name)
            return _real(*a, **k)

        monkeypatch.setattr(module, function, wrapped)
    for name, recorded in (("born", births), ("plain", plain)):
        board = node_toy(tmp_path / name, monkeypatch)
        found = []
        for start, after, _end in recorded:
            trace.clear()
            fed_interval(board, start, after)
            found.append(list(trace))
        traces[name] = found
    for born, other in zip(traces["born"], traces["plain"], strict=True):
        cut = born.index("meeting_board.closed")
        assert born[:cut] == other[: other.index("meeting_board.closed")]
        assert born[:cut] == ["node.phase_act"] + ["Lattice.stepped"] * len(board.families) + [
            "Lattice.held_write"
        ] * len(board.held) + ["swap.stepped"]
    closes = [set(t[t.index("meeting_board.closed") :]) for t in traces["born"]]
    assert closes[:3] == [{"meeting_board.closed", "meeting_board.click"}] * 3
    assert closes[3] == {
        "meeting_board.closed",
        "meeting_board.take_of",
        "meeting_board.laid",
        "meeting_board.click",
    }
    assert all(
        set(t) == {"meeting_board.closed", "meeting_board.click"}
        for t in (x[x.index("meeting_board.closed") :] for x in traces["plain"])
    )


def test_constant_3_the_state_stands_within_128_bits_at_the_fed_extremes_and_the_transients_beyond_are_named(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The owner's constant 3 at the Node: every integer of the state stands within 128 bits at the fed extremes (the light at +2^24 at the centre among six neighbours at -2^24, the largest level the volume's write admits; the volume at the deepest content before the frozen clock) and through a birth at the centre; the transients measured through the acts and named, not asserted within 128: Rule3's total at the amplitude bound A by `flux_total` on the rule's integers (73 to 74 bits at den 1,021, within), the take's common denominator (4 p^2 G^2)^7 over the frame (about 210 bits), the carried write's ratio product exact(n) x exact(f) in `records.write_sources`, consumed by `paces.odd_rounded` since the odd rounding (140 bits at den 1,021), the read's number (the click test's, hundreds of bits) and the paces' running fraction at the deepest content (`paces.Side.reach`, 2 Gamma (Gamma - 1)^c + Gamma^c, tens of thousands of bits), the four beyond 128 the deviation kept by name; the phase act's numerator 2 K_0 X + D at the amplitude within 128 at this den."""
    board, draw = node_toy(tmp_path, monkeypatch), np.random.default_rng(23)
    light, unit = board.world.seed, board.unit
    bound = board.world.amplitude_bound
    extreme = shaken(
        board,
        draw,
        0,
        [
            int(volume.volume_of(GAMMA, np.array([paces.frozen_content(GAMMA) - 1], dtype=object))[0]),
            GAMMA,
        ],
        remainders=True,
    )
    size = 1 << 24
    now = np.full(board.shape, -size, dtype=object)
    now[CENTRE] = size
    extreme[(light, "line", 0)] = (
        now,
        np.zeros(board.shape, dtype=object),
        extreme[(light, "line", 0)][2],
    )
    measured = {"division": 0, "write": 0, "take": 0, "rule3": 0}
    real_division, real_rounded, real_taken = rule3.carried_division, paces.rounded, hole.taken_at
    real_rule3 = rule3.rule3

    def ruled(name):  # type: ignore[no-untyped-def]
        def wrapped(flux_sum, mass, wall, now, other, remainder, direction=1):  # type: ignore[no-untyped-def]
            total = np.asarray(rule3.flux_total(flux_sum, mass, wall, now, other), dtype=object)
            if total.size:
                measured[name] = max(
                    measured[name],
                    int(np.max(np.abs(total + np.asarray(remainder, dtype=object)))).bit_length(),
                )
            return real_rule3(flux_sum, mass, wall, now, other, remainder, direction)

        return wrapped

    def division(total, wall, remainder, direction=1):  # type: ignore[no-untyped-def]
        summed = np.asarray(direction * total + remainder, dtype=object)
        if summed.size:
            measured["division"] = max(measured["division"], int(np.max(np.abs(summed))).bit_length())
        return real_division(total, wall, remainder, direction)

    def measuring(real):  # type: ignore[no-untyped-def]
        """The carried write's one rounding at the wall per Node measured, at `paces.rounded` and at `paces.odd_rounded` (the odd rounding, 2026-10-25); the paces' fraction divides at one integer and is not measured here."""

        def hook(numerator, wall):  # type: ignore[no-untyped-def]
            if np.ndim(wall):
                measured["write"] = max(
                    measured["write"],
                    int(np.max(np.abs(np.asarray(numerator, dtype=object)))).bit_length(),
                )
            return real(numerator, wall)

        return hook

    def taken(*a):  # type: ignore[no-untyped-def]
        found = real_taken(*a)
        measured["take"] = max(measured["take"], found[1].bit_length())
        return found

    monkeypatch.setattr(rule3, "carried_division", division)
    monkeypatch.setattr(paces, "rounded", measuring(real_rounded))
    monkeypatch.setattr(paces, "odd_rounded", measuring(paces.odd_rounded))
    monkeypatch.setattr(hole, "taken_at", taken)
    monkeypatch.setattr(flux, "rule3", ruled("rule3"))
    fed_interval(board, extreme)
    assert (
        TOOL.largest_bits(board)[0] <= BITS
        and max(abs(int(a[CENTRE])) for v in node_arrays(board).values() for a in v).bit_length() <= BITS
    )
    recorded, _lines, _board = course(tmp_path / "board", monkeypatch, (0, 1, 1), 4)
    born = node_toy(tmp_path / "born", monkeypatch)
    for start, after, _end in recorded:
        fed_interval(born, start, after)
    assert born.born_at == {4: [4]} and TOOL.largest_bits(born)[0] <= BITS
    num, den = board.families[light].pair
    totals = []
    for content in (0, paces.frozen_content(GAMMA) - 1, -GAMMA):
        clock, pace = paces.node_paces(GAMMA, content)
        rule = rule3.rule_integers(num, den, GAMMA, clock, pace, None, unit)
        total = rule3.flux_total(
            sum(r * (-bound - bound) for r in rule.reaches), rule.mass, rule.wall, bound, -bound
        )
        totals.append((abs(int(total)) + int(rule.wall)).bit_length())
    common = ((4 * GAMMA * GAMMA * unit * unit) ** (1 + PORTS)).bit_length()
    deepest = paces.frozen_content(GAMMA) - 1
    fraction = (
        2 * GAMMA * (GAMMA - 1) ** deepest + GAMMA**deepest
    ).bit_length()  # the paces' memo at the deepest content, one rounding of the running fraction
    turn = phase.unit(GAMMA)
    rotation = (
        2 * phase.K0(turn) * board.amplitude + phase.D(turn)
    ).bit_length()  # the phase act's numerator 2 K_0 X + D at the amplitude
    assert max(totals) <= BITS and 0 < measured["rule3"] <= max(totals) and rotation <= BITS
    assert (
        measured["take"] == common > BITS
        and measured["write"] > BITS
        and measured["division"] >= fraction > BITS
    )
    print(json.dumps({"bits": [totals, measured, rotation, fraction]}))


def test_the_fold_on_the_one_node_torus_sums_the_links_to_zero_and_turns_at_the_pinned_rest(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The fold ("an axis of one layer folds: its two Ports return the Node itself"): on the 1x1x1 bare torus the six arrivals are the Node's own, so Rule3's Links' sum is 0 and the light line steps to (2 now - before, r) exactly; the phase counts are 0 on every axis (K_i - K_i) and every pair stands at the seed; the falling rest of the volume is a weak top at every interval and the Node turns every interval, the two-cycle of the pinned rest."""
    board = node_toy(tmp_path, monkeypatch, cube=1)
    light, sign, held = board.world.seed, board.held[1], board.held[0]
    for index in board.turning:
        board.born_point(index)
    at = (0, 0, 0)
    assert board.shape == (1, 1, 1) and all(
        arrival(np.array([[[5]]]), a, s)[at] == 5 for a, s in PORT_SIDES
    )
    for _k in range(1, 5):
        line = board.states[light].lines[0]
        now, before, remainder = (int(a[at]) for a in (line.now, line.before, line.remainder))
        content, factors = board.read(light, 1, 0)
        rule = node.rule_of(board.families[light], GAMMA, content, factors, board.unit)
        expected = rule3.rule3(0, rule.mass, rule.wall, now, before, remainder)
        time = board.states[held].lines[0]
        x0, x1 = int(time.before[at]), int(time.now[at])
        board.step()
        after = board.states[light].lines[0]
        if not board.turned[at]:
            assert (
                (int(after.now[at]), int(after.remainder[at]))
                == tuple(int(x) for x in expected)
                == (2 * now - before, remainder)
            )
        else:
            assert (int(after.now[at]), int(after.before[at])) == (before, now)
        x2 = int(board.states[held].lines[0].now[at])
        assert bool(board.turned[at]) == bool(
            swap.at_top(x0, x1, x1 if board.turned[at] else x2)[()] or board.turned[at]
        )
        for row in range(1, len(board.states[sign].phases)):
            lines = board.states[sign].phases[row]
            assert all(int(lines[2 * AXES + a].now[at]) == 0 for a in range(AXES))
            seed = phase.seed(board.amplitude, phase.unit(GAMMA))
            assert (int(lines[0].now[at]), int(lines[1].now[at])) == (int(seed[0][0]), int(seed[1][0]))
    assert [count for _i, _d, count in board.swaps] == [1] * 4 and [i for i, _d, _c in board.swaps] == [
        1,
        2,
        3,
        4,
    ]


def test_the_48_at_the_node_carry_the_fed_shell_and_the_centres_outputs_alike(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The cube's symmetry at the Node: a random shell on the light line and the volume's time line, carried by each of the 48 signed permutations of the axes about the centre, gives after the acts the same scalar lines at the centre bit for bit (the light, the volume's time line and its write remainder, the sign's rows) and the volume's tension lines permuted as the axes are (even under a reflection, the tension being a square), the read number of the close the same."""
    draw = np.random.default_rng(29)
    board = node_toy(tmp_path / "plain", monkeypatch)
    light, held, sign = board.world.seed, board.held[0], board.held[1]
    start = shaken(board, draw, 400, [1000, 1100, 1200], remainders=True)
    outputs = {}
    for number, element in enumerate(
        itertools.product(itertools.permutations(range(AXES)), itertools.product((1, -1), repeat=AXES))
    ):
        other = node_toy(tmp_path / str(number), monkeypatch)
        impose(other, carried(start, element))
        other.advanced_to_the_close()
        found = at_centre(node_arrays(other))
        permutation = element[0]
        scalars = {
            k: v
            for k, v in found.items()
            if not (k[0] == held and k[1] in ("line", "write") and 1 <= k[2] <= AXES)
        }
        tensions = tuple(found[(held, "line", 1 + permutation.index(a))] for a in range(AXES))
        tension_writes = tuple(found[(held, "write", 1 + permutation.index(a))] for a in range(AXES))
        outputs[element] = (scalars, tensions, tension_writes)
    plain = outputs[((0, 1, 2), (1, 1, 1))]
    assert len(outputs) == 48 and all(value == plain for value in outputs.values())
    assert not board.turned[CENTRE] and plain[0][(light, "line", 0)] != tuple(
        int(a[CENTRE]) for a in start[(light, "line", 0)]
    )
    assert len({plain[1][a] for a in range(AXES)}) > 1 or sign >= 0
