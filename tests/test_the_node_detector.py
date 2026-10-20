"""The NodeDetector (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment; the owner's words of 2026-10-03, a NodeDetector with Nodes alone is never on one Node and a NodeDetector with a record of its own may stand on one; src/event_universe/meeting.py, loader/node_detector_declaration.py, loader/world.py): a record declared a NodeDetector over a connected region, laid in the weights' proportion, its outer Links cut and its inner Links open, absorption and emission at one drawn Node of the region, every click a click line naming the reader and never a Node, the write's Node in the LATTICE lay and face lines beside it."""

import json
import math
from fractions import Fraction

import numpy as np

from event_universe import credit, reports, world_files
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features.click import amplitude, squared
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world
from tests.laws import (
    EVENTS,
    PACKET,
    TOOL,
    TOP,
    chain_body_world,
    load_file,
    own_lines,
    shares_of,
    slit_world,
)

TOP_PAIR = (TOP[0], TOP[1])  # the band's top as a resonance, cos Omega = 0


def test_a_count_is_one_quantum_of_the_invariant_in_the_familys_own_wall(tmp_path, monkeypatch):
    """A count is one quantum of the invariant, the form T sin omega_0 of the family's gap (the two hands' word on #1793's R8): the taker's lay carries 2 A^2 sin omega = T per quantum per line to the unit, the family's wall is W_c sin omega_0 by one root on the whole product and 3 den T for a massless family, the [1, 1299] amplitude is unchanged, and the generator lays a body's declared count in that unit (the books' count of a bound body at the lay is the share at the Nodes' paces under its own well, a reading above the declaration on main before this branch, 13 for 6 on the tests' chain, and no part of this change)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(
        tmp_path, TOOL, 8
    )  # a body of 8: at the declared rest 60 the lay of 7 cycles
    board = Lattice(load_world(world))
    names, action = [family.name for family in board.families], board.world.quantum_action
    matter, light = board.families[names.index("matter")], board.families[names.index("charge")]
    num, den = matter.pair
    gap, laid = den * den - num * num, squared(1, action, matter.pair)
    assert (
        laid == squared(1, action, (2, 3)) == 21981 and action == 32768
    )  # T / (2 sin omega_0) to the unit
    assert (
        action - 2 <= 2 * laid * math.isqrt(gap) // den <= action
    )  # 2 A^2 sin omega = T, two roots' units
    assert (
        squared(1, action, (1, 1299)) == 16384 and amplitude(1, action, (1, 1299)) == 128
    )  # bit for bit
    assert count_wall(light, action) == 3 * 6000 * action  # the bolometer's W_c for a massless family
    assert (
        count_wall(matter, action) == math.isqrt(9 * action**2 * gap) == 439628852
    )  # W_c sin omega_0 to the unit
    laid_body = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert (
        laid_body["count"] == laid_body["carried"] == 8
    )  # the generator lays the declaration in that unit


def test_the_node_detector_books_the_conserved_forms_own_current_through_its_front(
    tmp_path, monkeypatch
):
    """The credit's booking (ALGEBRA.md #the-click-is-the-meeting; the owner's word of 2026-10-04, 11:54 UTC, the mathematician's derivation with the advisor's second, two hands): a NodeDetector books through each front Port the conserved form's own current, num (q_ij / Gamma)^2 (now_i before_j - before_i now_j), the Link's factor squared the one weight, summed in the unit G^2 and divided once at the close by W_rec G^2, equal to the plain current where no tension stands. A light packet crosses a declared region of two Nodes on the tests' chain whose front Links carry a tension written into the content holder's x axis line (300 behind the region, 200 and 100 across it at the start: the tension 250 on the Link entered, Q - G^2 = -21, and 50 on the Link left, -4, the line then moving under Rule3); at every step the region's weighted share changes by the booked inflow over G^2 plus Rule3's remainder term within the division act's unit per Node, the derived tolerance, two units here, while the plain inflow misses it by far more; the twin without the tension books the plain current times G^2 exactly and `quanta_through` reads the count the plain formula read."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    region, draw = [[13, 0, 0], [14, 0, 0]], {"window": 400}
    packet = {**PACKET, "top": {"x": [8, 8], "y": [0, 0], "z": [0, 0]}, "edge": {"x": 4, "y": 0, "z": 0}}
    chain = dict(shape=[24, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), faces=[])
    readers = [{"name": "near", "positions": region}]
    world = slit_world(
        tmp_path, TOOL, "chain", packets=[packet], node_detectors=readers, draw=draw, **chain
    )
    boards = [Lattice(load_world(world)) for _ in (0, 1)]  # the tension's board and its twin without
    names, square = [f.name for f in boards[0].families], boards[0].unit ** 2
    light, gravity = names.index("charge"), names.index("gravity")
    axis = boards[0].states[gravity].lines[1]  # the content holder's x axis line, the tension's read
    for x, level in ((slice(0, 13), 300), (13, 200), (14, 100)):
        axis.now[x], axis.before[x] = level, level
    at, gamma = boards[0].mask(region), boards[0].world.node_clock
    facing = reports.front(at, boards[0].wrap, at, boards[0].declared_board())
    misses, totals = [], [[0, 0], [0, 0]]
    for _interval in range(8):
        for k, b in enumerate(boards):
            read, flow = b.read(light), [np.asarray(c, dtype=object) for c in b.currents()[light]]
            factors = [np.broadcast_to(np.asarray(q, dtype=object), b.shape) for q in read[1]]
            weighed = [q * c for q, c in zip(factors, flow, strict=True)]
            plain, weighted = (
                int(reports.entering(facing, f).sum(dtype=object)) for f in (flow, weighed)
            )
            fronts = [
                int(q[tuple(n)]) - square
                for q, f in zip(factors, facing, strict=True)
                for n in np.argwhere(f)
            ]
            assert (min(fronts) < 0) == (k == 0) and len(fronts) == 2  # tension on the front Links
            was, lines = (
                sum(map(sum, b.credit.intake.get((light, "near"), {}).values())),
                own_lines(b, light),
            )
            start = int(shares_of(b, light, read, lines)[at].sum())
            squares = np.broadcast_to(np.asarray(paces.link_pace_of(gamma, read[0])) ** 2, b.shape)[at]
            b.step()
            moved, remainder = own_lines(b, light), Fraction(0)
            booked_now = sum(map(sum, b.credit.intake.get((light, "near"), {}).values())) - was
            for a, z in zip(lines, moved, strict=True):  # Rule3's remainder term per Node of the region
                step = (z.now.astype(object) - a.before.astype(object))[at]  # next - before
                carried = (z.remainder.astype(object) - a.remainder.astype(object))[at]  # r' - r
                remainder -= sum(
                    Fraction(int(n), 2 * int(d) * square)
                    for n, d in zip(step * carried, squares, strict=True)
                )
            change = int(shares_of(b, light, read, moved)[at].sum()) - start - remainder
            print(
                f"interval {b.interval}, Q - G^2 on the front Links {fronts}: plain {plain}, weighted {weighted} (plain x G^2 {plain * square}), booked {booked_now}, the region's share change less the remainder term {float(change):.3f}, the identity's residual {float(change - Fraction(weighted, square)):.3f}"
            )
            assert (
                booked_now == weighted and abs(change - Fraction(weighted, square)) < 2
            )  # one unit per Node
            misses.append((k, abs(change - plain)))
            totals[k][0], totals[k][1] = totals[k][0] + plain, totals[k][1] + weighted
    assert max(m for k, m in misses if k == 0) > 2 and all(m < 2 for k, m in misses if k == 1)
    assert totals[1][1] == totals[1][0] * square  # the twin: the plain current times G^2 exactly
    twin, unit = boards[1], boards[1].credit.units[light]
    plain_count = int(division_forward(totals[1][0], unit, division_forward(unit, 2, 0)[0])[0])
    assert credit.quanta_through(twin.credit, light, totals[1][1], twin.unit) == plain_count > 0


def test_the_packet_readers_clicks_column_counts_the_regions_click_lines_and_not_the_givers():
    """The folder's reader's `clicks` column (the experimenter's tool note, #1827 comment 5984864554; examples/events/packet_emission/build_world.py `counted`): on a minimal output of the giver's two credit lines (its emission at the emission's interval and its null window's re-lay, `body 0`), the region `reach`'s click line at the draw's window's close, one beyond the window and the region's per-interval `click` report, the column counts the region's one line within the window of 168 and the giver's two stand in their own column with their intervals."""
    reader = load_file("packet_build_world", EVENTS / "packet_emission" / "build_world.py")
    emitted = {
        "event": "credit",
        "node_detector": "body 0",
        "interval": 2,
    }  # the emission; its null window at 48
    hit = {
        "event": "credit",
        "node_detector": "reach",
        "interval": 168,
    }  # the region's click at the close
    lines = [
        emitted,
        {**emitted, "interval": 48},
        hit,
        {**hit, "interval": 169},
        {**hit, "event": "click"},
    ]
    found = reader.counted(lines, "reach", 168)
    assert (found["clicks"], found["click_intervals"]) == (1, [168])  # the region's, inside the window
    assert (found["giver_credits"], found["giver_credit_intervals"]) == (2, [2, 48])
