"""The one-clock tests (the owner's word of 2026-10-25: every property tested on one clock fed through its six meshes): the horizon (a clock whose x meshes stand disengaged holds on that axis, is read by no mesh striking and fits nothing; a bob wound at it by a neighbour's shared half chimes, PM-S1), the stopped load (a clock at the mesh rate 0 is not read and never strikes), the turnover (the turned-over clock ends the tick at its pre-state reversed and complemented, the reverse an involution), the rewind exact through all of it; the step's reach of one mesh forward and none back; the files' refusals by name. The horizon's fed clock fits once on its own z mesh at 6 under EX-S1 (listed as its own and as its + end; nothing under the former unwind)."""

from __future__ import annotations

import copy
from typing import Any

import numpy as np

from event_universe import hands, readings
from event_universe import run as record
from event_universe.assembly.piece import check_piece
from event_universe.clock import Clock
from event_universe.core import rates
from event_universe.core.rule3 import carries
from event_universe.core.spokes import SPOKES
from event_universe.meshes import coupling_of, factors
from event_universe.tick import Tick
from event_universe.trains import HAND, OFFSET, REGULATOR, ratchet_of, rows_of, zeros
from event_universe.unspring import fall_of, unwinds
from event_universe.unwind import advance, move, window_clocks
from tests.laws import level_at, node_of, refused, run_back_exact, state_of, world_of, wronskian

CENTRE, INTERVALS = (1, 1, 1), 20  # the fed clock, the 3-cube's centre; the run's ticks
RAISED = [dict(x, quanta=7) if x["lay"] == "at" else x for x in world_of("world_nature.json")[1]["seed"]]


def clicks_at(node: Clock, at: tuple[int, ...]) -> list[dict[str, Any]]:
    own = [e for e in node.log if tuple(e["node"]) == at and e["event"] in ("birth", "credit")]
    ends = [e for e in node.log if e["event"] == "birth" and at in (tuple(e["minus"]), tuple(e["plus"]))]
    return own + ends


def fed_horizon(clock: Clock, at: tuple[int, ...]) -> Clock:
    """The clock's x axis gear of the regulator fed to 2 Gamma, so the tension of its two x meshes stands at Gamma and their factor is 0; its unsprung gear far above two windings, so an engagement would be read were the clock read."""
    axis = clock.train(REGULATOR).gears[1]
    axis.now[at] = 2 * clock.full_rate
    axis.before[at] = 2 * clock.full_rate
    unsprung = clock.unsprung().gears[0]
    unsprung.now[at] = 4 * int(unsprung.now[at])
    clock.driven_teeth()
    return clock


def test_the_horizon_holds_the_links_at_the_wall_and_the_node_births_nothing() -> None:
    """The horizon: the fed clock's two x meshes disengaged (the factor 0), its other four above; no mesh striking reads the clock (no fitting at it, none with it as an end); a bob of the near-massless hand laid at the fed clock, two quanta over the half-width 2, chimes there under the light the feed raised: three in 20 ticks under the great clock's bounds, at 8, 13 and 18 on the beat 5, the first at W = 0 paying one notch of the fed light and the next two from its slack (the one-clock bob of one quantum, wound at every tick, chimes none by 40, its dot with its reference crossing zero once in 20 ticks; seven in 20 ticks under the wave's honest books, where the neighbours' fittings that once shared a half into the clock under PM-S1 are jammed by the stop), so the near-massless hand's chimes are read there (twelve in 20 ticks under PL-S1, five at W = 0 (none by 20 under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting)); under the former drive of 2 W after the step twelve with nine at W = 0, the first beat 4 and the rest 1, under MS-S1's advance at T div 2 and CK-S1's beat of the half period with the crossing read even; eleven with eight at W = 0 and every beat 1 under the crossing odd at a touch of zero; named: the bobs' striking is not the mesh striking); the rewind exact."""
    _, piece = world_of("world_node.json")
    bob = {"lay": "at", "row": 1, "centre": list(CENTRE), "width": 2, "quanta": 2, "sense": 1}
    clock = fed_horizon(node_of("world_node.json", seed=[*piece["seed"], bob]), CENTRE)
    read = factors(clock)
    assert [int(f[CENTRE]) for f in read[:2]] == [0, 0]
    assert all(int(f[CENTRE]) > 0 for f in read[2:])
    fed = copy.deepcopy(clock)
    for _ in range(INTERVALS):
        clock.tick()
    strikes = clicks_at(clock, CENTRE)
    # no fitting at the fed clock under CL-S2 (the unspringing's two ends tallied from the start at 6, the course following; (11, 1) and (12, 519) before it, two fittings of 270 notches at 10 before LT-S1, (6, 18) at 54)
    assert [(e["i"], e["levels"]) for e in strikes if e["event"] == "birth"] == []
    # the laid bob's three chimes under the great clock's bounds (seven at the wave, one quantum at the one clock; the head's six under CL-S2 from the neighbours' shared halves; (-1, 0), (0, 0), (1, 0), (0, 0), (0, 0) before CL-S2; two under BH-S1's mask, six with the stopped clock released, FR-S1)
    chimes = [(e["sense"], e["line"]) for e in strikes if e["event"] == "credit"]
    assert chimes == [(0, 0), (1, 0), (1, 0)]
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def test_the_frozen_node_is_not_read_and_never_clicks() -> None:
    clock = node_of("world_node.json")
    stopped = rates.stopped_load(clock.full_rate)
    regulator = clock.train(REGULATOR).gears[0]
    regulator.now[CENTRE] = level_at(clock, stopped)
    regulator.before[CENTRE] = regulator.now[CENTRE]
    clock.driven_teeth()
    unsprung = clock.unsprung().gears[0]
    unsprung.now[CENTRE] = 4 * int(unsprung.now[CENTRE])
    fed = copy.deepcopy(clock)
    for _ in range(INTERVALS):
        clock.tick()
    assert clicks_at(clock, CENTRE) == []
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def exchanged(clock: Clock, held: list[list[Any]], at: tuple[int, ...]) -> bool:
    flat, pawl = [gear for train in held for gear in train], ratchet_of(clock.trains_).gears[0]
    twelves = [hands.signs(r.size)[k] < 0 for r in clock.trains_ for k in range(r.size)]
    for gear, h, twelve in zip(clock.all_gears(), flat, twelves, strict=True):
        sign = -1 if twelve else 1
        teeth = int(np.asarray(gear.teeth)[at]) if np.ndim(gear.teeth) else int(gear.teeth)
        mirrored = (
            teeth - 1 - int(h.fine[at]) if gear is pawl else (teeth // 2 * 2 - int(h.fine[at])) % teeth
        )
        if int(gear.now[at]) != sign * int(h.before[at]) or int(gear.before[at]) != sign * int(
            h.now[at]
        ):
            return False
        if int(gear.fine[at]) != (int(h.fine[at]) if twelve else mirrored):
            return False
        if (
            gear.dfine is not None
            and int(gear.dfine[at]) != (gear.dteeth // 2 * 2 - int(h.dfine[at])) % gear.dteeth
        ):
            return False
    return True


def bumped(clock: Clock) -> Clock:
    """The regulator's time gear at the centre fed a bump with before = now above its neighbours, so the clock turns over alone at the first tick."""
    bump = level_at(clock, 40)
    regulator = clock.train(REGULATOR).gears[0]
    regulator.now[CENTRE] = bump
    regulator.before[CENTRE] = bump
    clock.driven_teeth()
    return clock


def sea_only(name: str) -> Clock:
    return node_of(name, seed=[x for x in world_of(name)[1]["seed"] if x.get("lay") == "sea"])


def test_the_turn_is_the_pre_state_exchanged_and_complemented_and_runs_back_exact() -> None:
    clock = bumped(sea_only("world_node.json"))
    fed = copy.deepcopy(clock)
    held = [[gear.copy() for gear in train] for train in clock.trains()]
    clock.tick()
    turned_over = [tuple(int(x) for x in q) for q in zip(*np.nonzero(clock.turned_over), strict=True)]
    assert turned_over == [CENTRE]
    assert exchanged(clock, held, CENTRE)
    twice = copy.deepcopy(clock)
    before = state_of(twice)
    for _ in range(2):
        twice.reverse(clock.turned_over, [[gear.copy() for gear in train] for train in twice.trains()])
    assert state_of(twice) == before
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def test_the_turn_at_the_horizon_runs_back_exact() -> None:
    clock = fed_horizon(bumped(sea_only("world_node.json")), CENTRE)
    fed = copy.deepcopy(clock)
    clock.tick()
    turned_over = [tuple(int(x) for x in q) for q in zip(*np.nonzero(clock.turned_over), strict=True)]
    assert turned_over == [
        (0, 1, 1),
        CENTRE,
        (2, 1, 1),
    ]  # the centre alone at the trace 54; its x neighbours with it at 6
    assert run_back_exact(fed, INTERVALS) == INTERVALS


def differences(a: Clock, b: Clock, origin: tuple[int, ...]) -> set[int]:
    """The torus distances from the origin of every clock where the two great clocks' gears differ."""
    found = set()
    for ta, tb in zip(a.trains(), b.trains(), strict=True):
        for ga, gb in zip(ta, tb, strict=True):
            for slot in ("now", "before", "fine", "dfine"):
                xa, xb = getattr(ga, slot), getattr(gb, slot)
                if xa is None:
                    continue
                for where in zip(*np.nonzero(np.asarray(xa != xb)), strict=True):
                    clock = tuple(int(x) for x in where)
                    found.add(
                        sum(
                            min(abs(clock[k] - origin[k]), a.cube - abs(clock[k] - origin[k]))
                            for k in range(3)
                        )
                    )
    return found


def test_the_step_reaches_one_link_forward_and_none_back() -> None:
    at = (2, 2, 2)
    a = sea_only("world_hole.json")
    for _ in range(2):
        a.tick()
    b = copy.deepcopy(a)
    unsprung = b.unsprung().gears[0]
    unsprung.now[at] = unsprung.now[at] + 1
    assert differences(a, b, at) == {0}
    a.tick()
    b.tick()
    assert a.counts["births"] == b.counts["births"] == 0
    assert differences(a, b, at) <= {0, 1}
    a2, b2 = copy.deepcopy(a), copy.deepcopy(a)
    unsprung = b2.unsprung().gears[0]
    unsprung.now[at] = unsprung.now[at] + 1
    a2.tick(-1)
    b2.tick(-1)
    assert differences(a2, b2, at) <= {0}


def test_the_files_are_refused_by_name() -> None:
    universe, piece = world_of("world_node.json")
    rim, rows = universe["integers"]["den"], universe["rows"]
    refused("keys of no law: control", check_piece, dict(piece, control={"ride": "symmetric"}), universe)
    refused("keys of no law: detectors", check_piece, dict(piece, detectors=[[0, 0, 0]]), universe)
    ints = {**universe["integers"], "link_unit": 16}
    refused("keys of no law: link_unit", check_piece, piece, dict(universe, integers=ints))
    assert node_of("world_node.json").G == 16  # derived from Gamma 1,000 (K-S1), no key of the file
    # the file holds the matter alone: a row the clock builds (trains.rows_of: the light at the rim, the regulator, the offset at the rim), a shape of no gapped row (the former gap-0 plane, shape 1 with a pair, among them) and a row with no pair each refused by name as no gapped row; the ratchet's wall a key of no law; a file of none refused
    light, *_, regulator, offset, ratchet = rows_of(universe)
    shapes = [{"shape": 1}, {"shape": 1, "pair": [1, 2]}, {"shape": 8}, {"shape": 2}]
    for row in (light, regulator, offset, *shapes):
        refused("is no gapped row", check_piece, piece, dict(universe, rows=[*rows, row]))
    refused("keys of no law: wall", check_piece, piece, dict(universe, rows=[*rows, ratchet]))
    refused("names no gapped row", check_piece, piece, dict(universe, rows=[]))
    off = [dict(r, pair=[r["pair"][0] - 1, rim]) for r in rows]  # every row of the file gapped
    refused("off den's circle", Clock, dict(universe, rows=off), piece)
    for match, change in (
        ("a cube", {"shape": [3, 3, 4]}),
        ("off the board", {"seed": [{"lay": "hole", "at": [3, 0, 0]}]}),
        ("no form of the law", {"seed": [{"lay": "cycle", "row": 0}]}),
        ("at its quanta", {"seed": [{"lay": "wave", "row": 0}]}),  # no form of the law before CS5-S2
        ("the plane at the gap 0 alone", {"seed": [{"lay": "sea", "row": 1}]}),
        (
            "half-width 1 .the one Node., 2 or 3",
            {"seed": [{"lay": "at", "row": 1, "centre": [1, 1, 1], "quanta": 1, "width": 4}]},
        ),
    ):
        refused(match, Clock, universe, dict(piece, **change))
    # the trains the clock builds beside the file's three gapped hands: the ratchet, the light, the offset and the regulator
    assert [r.size for r in node_of("world_node.json").trains_] == [1, 2, 2, 2, 2, 4, 10]


def test_the_frozen_node_rests_and_its_links_stand_at_the_wall_bh_s1() -> None:
    """BH-S1 (the owner's word of 2026-10-25 through the Boss, 6398593790; The-Frozen-Node-Black-Hole_COMPARISON.md section 6): a clock whose mesh rate reads 0 at the tick's start is stopped: no act changes any integer of its state and its dial rests, no strike reads it, every mesh with a stopped end is disengaged from both ends; the stopped mask kept in the rewind note for the rewind. The 3-cube centre fed to the stopped load 3,793 at Gamma 1,000 (X 4,268,834,097), 100 ticks: the centre's gears equal to the fed values at every tick, dial[centre] unchanged, the twelve factors 0, 0 strikes at it, the stopped count 1 at every tick, the transient within 128, the rewind exact 100 of 100."""
    clock = node_of("world_node.json")
    stopped = rates.stopped_load(clock.full_rate)
    regulator = clock.train(REGULATOR).gears[0]
    regulator.now[CENTRE] = level_at(clock, stopped)
    regulator.before[CENTRE] = regulator.now[CENTRE]
    clock.driven_teeth()
    assert int(regulator.now[CENTRE]) == 4_268_834_097
    fed = [[int(a[CENTRE]) for a in (gear.now, gear.before, gear.fine)] for gear in clock.all_gears()]
    dial = int(clock.dial[CENTRE])
    kept = copy.deepcopy(clock)
    for _ in range(100):
        clock.tick()
        gears = clock.all_gears()
        assert [[int(a[CENTRE]) for a in (gear.now, gear.before, gear.fine)] for gear in gears] == fed
        assert int(clock.dial[CENTRE]) == dial and not clock.turned_over[CENTRE]
        stopped_now = (
            np.asarray(rates.mesh_rate_of(clock.full_rate, readings.load(clock)), dtype=object) == 0
        )
        assert int(stopped_now.sum()) == 1 and stopped_now[CENTRE]
        assert all(int(f[CENTRE]) == 0 for f in factors(clock, None, stopped_now))
        assert all(
            int(factors(clock, None, stopped_now)[spoke ^ 1][n]) == 0
            for spoke, n in enumerate(window_clocks(clock, CENTRE)[1:])
        )
    assert clicks_at(clock, CENTRE) == []  # the width's bound struck (the ruling of 2026-10-26)
    assert run_back_exact(kept, 100) == 100


def shares_of(node: Clock) -> tuple[Any, Any, Any]:
    """The unsprung gear's wind in the regulator's unit, and by hand at the frame's weight (X set to Gamma^3 div p_i^2) and at the vacuum's (X set to Gamma)."""
    unsprung = node.unsprung()
    gearing = readings.gearing(node, unsprung.ratio, node.start_load, factors(node))
    pace = np.asarray(rates.mesh_rate_of(node.full_rate, node.start_load), dtype=object)
    x, regulator = node.start_stretch, hands.wind(node, unsprung.gears, gearing)
    node.start_stretch = np.vectorize(lambda p: carries(node.full_rate**3, p * p), otypes=[object])(pace)
    frame = hands.wind(node, unsprung.gears, gearing)
    node.start_stretch = zeros(node.size) + node.full_rate
    vacuum, node.start_stretch = hands.wind(node, unsprung.gears, gearing), x
    return regulator, frame, vacuum


def test_every_count_is_read_in_the_carriers_unit_pm_s1() -> None:
    """PM-S1 (the owner's word of 2026-10-25, 15:18 UTC, through the Boss, 6399410929; The-Count-In-The-Carriers-Unit_COMPARISON.md section 5): the identity Gamma^2 div p_i^2 = X(c) div Gamma at c = 0 to 1,000 by 100 (pm1); on the 3-cube hole the regulator's wind within one unit of the frame's at 27 of 27 clocks at the tick 1 (X / Gamma below 2) and equal to the vacuum's there (X = Gamma); at 20 the vacuum's below the regulator's by X / Gamma (429 thousandths at X / Gamma between 1.915 and 2.781 under the great clock's bounds; 407 between 1.979 and 2.995 at the wave, 390 between 2.36 and 2.94 at 54) and the frame's within four per mille; the chiral 5-cube at 40: fittings 2, bob chimes 1,543 and 107 integers of at most 112 bits under the great clock's bounds (5, 1,873 and 107 under the wave's honest books, the light raised to two quanta a packet (David's DAVID-WORLDS-AFTER-THE-WAVE.md) and the beats' references counted; 16, 1,973 and 99 before the wave; 16, 2,075 and 99 under EX-S1; 17, 1,690 and 98 under GP-S1, 19 and 2,477 under MG-S1, 17 and 1,999 under PL-S1; 19 and 2,038 under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting); 17 and 1,996 under the former drive of 2 W after the step), the rewind 10 of 10, 98 integers, 115 bits (at 60 under the crossing odd at a touch of zero and the wound unsprung hand chimed as a bob: fittings 16 and 2,336 chimes, pm2's 15 and 24 under the advance by the winding; the fittings and the chimes re-cut by MS-S1's advance at T div 2; the chimes 533 under the upward crossing alone, re-cut by CK-S1's beat of the half period; 40 ticks so the test stands under 10 s alone, the Boss's 6402497841)."""
    clock = node_of("world_node.json")
    full = clock.full_rate
    for c in range(0, 1_001, 100):
        mesh_rate = rates.mesh_rate(full, c)
        assert carries(full * full, mesh_rate * mesh_rate) == carries(level_at(clock, c), full)
    clock.tick()
    clock.tick(-1)
    carrier, frame, vacuum = shares_of(clock)
    assert bool((clock.start_stretch < 2 * full).all()) and int((abs(carrier - frame) <= 1).sum()) == 27
    assert carrier.tolist() == vacuum.tolist()
    for _ in range(20):
        clock.tick()
    clock.start_load, clock.start_stretch = readings.load(clock), clock.train(REGULATOR).gears[0].now
    carrier, frame, vacuum = shares_of(clock)
    totals = [sum(int(v) for v in a.reshape(-1)) for a in (carrier, frame, vacuum)]
    # 429 under the great clock's bounds (407 at the wave, 390 at 54)
    assert totals[2] * 1000 // totals[0] == 429 and abs(totals[1] - totals[0]) * 1000 <= 4 * totals[0]
    assert (
        1_915  # under the great clock's bounds (1_979 at the wave, 2_356 at the trace 54)
        <= int(clock.start_stretch.min()) * 1000 // clock.full_rate
        <= int(clock.start_stretch.max()) * 1000 // clock.full_rate
        <= 2_781  # (2_995 at the wave, 2_938 at 54)
    )
    chiral = node_of("world_nature.json")
    kept = copy.deepcopy(chiral)
    for _ in range(40):
        chiral.tick()
    counts = (chiral.counts["births"], chiral.counts["body_clicks"], record.census(chiral))
    assert counts == (3, 1384, (107, 112))  # the one mirror (2, 1,543 before it; 5, 1,873 at the wave)
    assert run_back_exact(kept, 10) == 10


def test_the_charge_is_one_e_for_every_row_at_the_lay_ms_s1() -> None:
    """MS-S1 (the owner's word of 2026-10-25, 15:18 UTC, through the Boss, 6399410929; The-Masses-From-The-Clicks_COMPARISON.md section 5, ms2's exact form): the advance's two notches (A, B) with A B = T div 2 from T alone (125 and 144 at T 36,000), the same for every train; the chiral 5-cube at 12 ticks, its light raised to seven quanta a packet (six fittings on the three sprung rows under the great clock's bounds, where the file's two quanta a packet fit twice in 40 ticks; four under the wave's honest books with the light at two quanta a packet, eight and more before the wave): every fitted hand's sweep is +-(T div 2) where its hand stood at nothing at its clock (the residue logged), every fitting's fitted hands at opposite signs with the senses' sum 0, unwound at or above tallied on every fitting, the rewind exact."""
    clock = node_of("world_nature.json", seed=RAISED)
    assert (clock.A, clock.B, clock.A * clock.B) == (125, 144, clock.key // 2)
    kept = copy.deepcopy(clock)
    for _ in range(12):
        clock.tick()
    fittings = [e for e in clock.log if e["event"] == "birth" and "exact_lay" not in e]
    assert len(fittings) >= 4 and all(b["amplitude"] == [125, 144] for b in fittings)
    for b in fittings:
        for w, stood in zip(b["W_children"], b["stood"], strict=True):
            assert abs(w) == clock.key // 2 or any(stood), (w, stood)
        assert (b["W_children"][0] > 0) != (b["W_children"][1] > 0) and 0 not in b["W_children"]
        assert b["taken"] + b["remainder_was"] - b["remainder"] == b["booked"] > 0  # EX-S1
    assert sum((w > 0) - (w < 0) for b in fittings for w in b["W_children"]) == 0
    assert sum(1 for b in fittings for w in b["W_children"] if abs(w) == clock.key // 2) >= len(fittings)
    assert run_back_exact(kept, 12) == 12


def test_the_born_pair_meets_at_the_next_close_with_no_current_and_is_refused_by_the_orientation_sl_s1() -> (
    None
):
    """SL-S1 (the Boss's 6399718139, The-Merger-As-The-Birth-Reversed_COMPARISON.md section 4: the generic striking, every hand's engagement by its own list): the chiral setting at 14 ticks, its light raised to seven quanta a packet under the great clock's bounds, where the file's two fit twice in 14 ticks (the 5-cube as written at the wave: under the wave's honest books its 3-cube cut, with two packets of two quanta, fits nothing, so the test reads the whole setting; the 3-cube at 30 ticks before the wave): every fitted pair's mesh engages at the next striking (the two ends holding a whole winding of the fitted hands) and reads no lead, F = 0 exactly: under MG-S1 the pair at rest reaches the unspringing's premise by its sweeps and the stop jams the undoing at an end by name, the pair's fall below the unsprung fitted hand's own quantum (7 of 7 fitted pairs under the great clock's bounds, 2 of 2 with the file's light; 5 of 5 under the wave, 4 of 4 before it; before MG-S1 the orientation jammed the same meshes with no name, 4 of 4 under PL-S1; 8 of 8 pairs of matter with a ninth fitting, an unspringing of the lightest pair at rest whose unsprung fitted hands the advance jams, under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting); 5 of 5 under the former drive of 2 W after the step); the engagements counted as `met`; the rewind exact."""
    clock = node_of("world_nature.json", intervals=14, seed=RAISED)
    kept = copy.deepcopy(clock)
    for _ in range(14):
        clock.tick()
    fittings = [e for e in clock.log if e["event"] == "birth"]
    pairs = [b for b in fittings if b["line_pair"] != clock.hands().index(clock.unsprung())]
    # 4 fittings, every one a pair, under the one mirror (6 with the lead at the kick, 7 under the great clock's bounds, 5 and 5 at the wave); 6 fittings and 5 pairs on the 3-cube before the wave and before LT-S1 as at -dP; 6 pairs at 54
    assert len(fittings) == 4 and len(pairs) == 4 and clock.counts["met"] > len(fittings)
    for b in pairs:
        mesh = {tuple(b["minus"]), tuple(b["plus"])}
        # the advance's or the orientation's jam under 4ad484eb9's bound; the stop again, MG-S1's own
        assert any(
            e["event"] == "refused"
            and e["i"] == b["i"] + 1
            and e["cause"] == "stop"
            and e.get("row") == b["line_pair"]
            and tuple(e["node"]) in mesh
            and e["fall"] < e["walls"]
            for e in clock.log
        ), b
    assert run_back_exact(kept, 14) == 14


def test_the_merger_takes_one_light_quantum_at_each_end_of_the_pair_and_lays_the_light_sl_s2() -> None:
    """SL-S2 (the Boss's ledger item 10, The-Merger-As-The-Birth-Reversed_COMPARISON.md section 3: the unspringing is the fitting read at -1): the heaviest hand's reflected pair fed at two adjacent clocks of the bare 5-cube (the + hand at M and the - hand at P at three times the advance's notches (A, B), one notch pair on P's three-o'clock gear for a lead across the mesh and on two transverse neighbours for a twist) engages as the reflected pair (the ends' sweeps opposite) and strikes into light: one fitting whose unwound train is the heaviest hand and whose fitted hands are the unsprung train, each fitted hand's windings one light quantum to the rounding (its own quantum, MG-S1, 1,654,009,903,854,256,729,287 at both ends) paid at its own end by the unwound hand's four notches unwound whole by the one advance act at -1 (MG-S1; before it by one exact unwind from the unwound train's gear), the unsprung train wound at a whole winding at each end where nothing stood (the unsprung hand advanced as the fitted hand's advance, the gear having no going there), the fitted hands' sweeps -+(T div 2) summing to 0 and the unsprung train's sweep 0 over the great clock, unwound at or above tallied, the unspringing at the first striking with no stop before it (the former unwinds by gear, CS4-S2, logged `taken_line` [1, 1] on the heavy train's second gear, 3 B against 0 the farthest; at the second striking on the first gear, [0, 0], under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting); under the former first gear's unwind the stop jammed both ends by name before the unspringing paid); the rewind exact."""
    clock = node_of("world_node.json", shape=[5, 5, 5], seed=[])
    a, b, k = clock.A, clock.B, 3
    heavy = max(range(len(clock.hands())), key=lambda r: clock.hands()[r].spring or 0)
    unsprung = clock.unsprung()
    unsprung_index = clock.hands().index(unsprung)
    unit = clock.windings[unsprung_index]
    m, p = (1, 1, 1), (2, 1, 1)
    feed = (
        (m, (k * a, 0, 0, k * b)),
        (p, (k * a, b, 0, -k * b)),
        ((1, 2, 1), (a, b, 0, 0)),
        ((2, 1, 2), (b, a, 0, 0)),
    )
    for at, notches in feed:
        advance(clock, heavy, at, notches)
    kept = copy.deepcopy(clock)
    for _ in range(INTERVALS):
        clock.tick()
    fittings = [e for e in clock.log if e["event"] == "birth"]
    mergers = [e for e in fittings if e["taken_row"] == heavy]
    assert len(mergers) == 1 and mergers[0]["line_pair"] == unsprung_index and fittings[0] is mergers[0]
    (merger,) = mergers
    assert {tuple(merger["minus"]), tuple(merger["plus"])} == {m, p}
    assert [tuple(t["node"]) for t in merger["takes"]] == [tuple(merger["minus"]), tuple(merger["plus"])]
    assert [t["booked"] for t in merger["takes"]] == [1_654_009_903_854_256_729_287] * 2
    assert all(unit <= t["booked"] <= t["taken"] and t["booked"] < 2 * unit for t in merger["takes"])
    assert [t["taken_levels"][1::2] for t in merger["takes"]] == [[k * a, 0], [k * a, 0]]
    assert merger["taken"] >= merger["booked"] == sum(t["booked"] for t in merger["takes"])
    # the unsprung hand at both ends, cc1
    assert merger["W_children"] == [0, 0] and merger["stood"] == [[0] * 4] * 2
    jam_events = [
        e
        for e in clock.log
        if e["event"] == "refused" and e.get("row") == heavy and e["i"] <= merger["i"]
    ]
    # cc1: both ends exact ([None, None] before)
    assert (
        merger["i"] == 1 and jam_events == [] and [x[:2] for x in merger["exact_lay"]] == [[0, -191]] * 2
    )
    probe = copy.deepcopy(kept)
    for _ in range(merger["i"]):
        probe.tick()
    re, im = probe.unsprung().gears
    assert int((re.now * im.before - im.now * re.before).sum()) == 0  # its sweep at the unspringing
    assert run_back_exact(kept, INTERVALS) == INTERVALS


def test_the_swap_keeps_the_charge_of_every_plane_at_every_turned_node_ws() -> None:
    """WS (the Boss's 6400357538, The-Swap-Keeps-The-Charge_VERDICT.md section 4, ws1's exchange_read as a test under 15 s): the turnover at the top is the reflection composed with the reverse of the two notches, and W = three_now twelve_before - twelve_now three_before, odd under each, is even under the two: at every turned-over clock and every hand (the unsprung hand with the sprung), W after the turnover equals W of the held pre-state exactly (read by a clock whose strike reads before it advances; the acts untouched), kept = sites, negated 0, changed 0; on the Boss's 3-cube (the sea and one winding of train 1 at the centre) 148 of 148 sites by 60 under the great clock's bounds as under the wave's honest books (37 turned-over clocks, the first at the tick 1, 9 sites with W not 0, every one kept; the centre's bob chimed 18 times, none laid back, 57 at the wave) and before the wave (the first turnover at 42 under EQ-S1, the centre's bob returning 12 of its 39 chimes where nothing arrives; 35 with the unwind standing under CK-S1's crossing read even, 37 under the crossing odd at a touch of zero, 42 before CK-S1's chimes) 296 of 296 sites (74 turned-over clocks; 324 and 81 with the unwind standing), every W 0 there; on the chiral 5-cube at 20 ticks 2,624 of 2,624 sites by 656 turned-over clocks, 224 of them with W not 0, under the great clock's bounds (2,668 by 667 and 440 under the wave; 2,112 and 533 before it; 2,152 of 2,152 sites, 664 of them with W not 0 under EX-S1 (2,124 and 632 under GP-S1; 2,172 of 2,172 by 543 turned-over clocks, 686 with W not 0 under MG-S1; 2,156 sites by 539 turned-over clocks and 625 under PL-S1; 2,180 sites by 545 turned-over clocks and 722 under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting); 2,160 sites by 540 turned-over clocks and 695 under the former drive of 2 W after the step; 2,124 and 672 under the odd crossing; 2,120 and 668 under the upward crossing alone; at 60 the probe read 2,500 of 2,500, 908 not 0, against ws1's 1,863 on the former head))."""

    class Reading(Clock):
        wronskians: dict[str, int] = {}

        def strike(self, *args: Any, **keys: Any) -> Any:
            where = list(zip(*np.nonzero(self.turned_over), strict=True))
            for r, train, htrain in zip(self.trains_, self.trains(), args[1], strict=True):
                if r.size == HAND:
                    pre, after = wronskian(*htrain), wronskian(*train)
                    for at in where:
                        wp, wa = int(pre[at]), int(after[at])
                        key = "kept" if wa == wp else "negated" if wa == -wp else "changed"
                        for k in ("sites", key, "nonzero" if wp else "zero"):
                            self.wronskians[k] = self.wronskians.get(k, 0) + 1
            return super().strike(*args, **keys)

    calibre, piece = world_of("world_node.json")
    one = {"lay": "at", "row": 1, "centre": [1, 1, 1], "quanta": 1, "width": 2, "sense": 1}
    found = []
    for clock, n in (
        (Reading(calibre, dict(piece, seed=[piece["seed"][0], one])), 60),
        (Reading(*world_of("world_nature.json")), 20),
    ):
        clock.wronskians = {}
        for _ in range(n):
            clock.tick()
        assert clock.wronskians["kept"] == clock.wronskians["sites"] > 0
        assert not {"negated", "changed"} & clock.wronskians.keys()
        found.append(clock.wronskians)
        # 2,668 and 277 under the one mirror (2,624 and 224 before it; 2,668 and 440 at the wave; 2,152 sites and 708 with W not 0 at the trace 54, 664 before cc1)
    assert [(f["sites"], f.get("nonzero", 0)) for f in found] == [(148, 9), (2668, 277)]


def test_the_bodies_closing_clicks_on_the_zero_crossing_in_either_direction_ck_s1() -> None:
    """CK-S1 (the owner's word of 2026-10-25, 17:57 UTC, through the Boss, 6401141446; ck1's REPORT.md section 4): a hand wound at a whole quantum of its own winding through one period of its three-o'clock gear's zero crossings, in either direction, strikes, the beat the half period, the crossing read even under the negation of the gear (the two notches' product below 0 or exactly one of them 0, a touch of zero a crossing from either side alike; the Boss's 6402516165), read on the hand's own beat (the owner's word of 2026-10-27, 15:5x UTC, DAVID-OWN-BEAT.md: the dot of the hand's notch with its reference, the notch where its winding began, the crossings' timer restarted there): at one clock a hand's three-o'clock gear fed at rest, its reference set along the three gear, over the period 8 touching zero (2, 1, 0, -1, -2, -1, 0, 1) and over the period 6 (2, 1, -1, -2, -1, 1), each with its negation, gives the counters crossed and beats equal step for step, the period 6 the beat 3; on the chiral 5-cube at 20 ticks every hand chime's beat is the tick count between the two latest zero crossings of that dot at its clock in either direction after its winding began, read by hand from the gears and the references by the even form, 275 chimes with 138 of them on an upward crossing under the great clock's bounds, every one a take, at the beats 1 to 5 (453 and 281 under the wave's honest books; 1,037 and 481 on the three gear before the wave; 1,036 chimes with 671 of them on a downward crossing under EX-S1 (762 and 512 under GP-S1, 910 and 106 under MG-S1, 825 and 128 under PL-S1; 834 and 79 under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting); 819 and 177 under the former drive of 2 W after the step; 536 and 50 under the form `b < 0 <= n or n < 0 <= b`, odd where exactly one notch is 0; 115 chimes under the upward crossing alone)); the rewind exact."""
    from event_universe.bobs import bobs

    clock = node_of("world_node.json")
    rec, count = 1, len(clock.hands())
    three = clock.hands()[rec].gears[0]
    nothing, still = [zeros(clock.size) for _ in range(count)], np.zeros(clock.size, dtype=bool)
    gearing = readings.gearing_of(clock, clock.unsprung(), readings.load(clock), factors(clock))
    for period in ((2, 1, 0, -1, -2, -1, 0, 1), (2, 1, -1, -2, -1, 1)):
        counters = []
        for sign in (1, -1):
            clock.wound, clock.crossed, clock.beats, clock.reference = [
                [zeros(clock.size) for _ in range(count)] for _ in range(3)
            ] + [[[zeros(clock.size) + 1, zeros(clock.size)] for _ in range(count)]]
            notches = [sign * v for v in period * 3]
            for before, now in zip(notches, notches[1:], strict=False):
                three.before[CENTRE], three.now[CENTRE] = before, now
                bobs(clock, [r.gears for r in clock.hands()], nothing, set(), still, gearing)
                counters.append((sign, int(clock.crossed[rec][CENTRE]), int(clock.beats[rec][CENTRE])))
        assert [c[1:] for c in counters if c[0] == 1] == [c[1:] for c in counters if c[0] == -1]
    assert counters[-1][2] == 3 and clock.counts["body_clicks"] == 0
    clock = node_of("world_nature.json")
    kept, hands_of = copy.deepcopy(clock), {r for r, h in enumerate(clock.hands()) if h.size == HAND}
    beat: dict[tuple[int, tuple[int, ...]], tuple[int, bool]] = {}
    last: dict[tuple[int, tuple[int, ...]], int] = {}
    chimes: list[tuple[int, tuple[int, bool] | None]] = []
    for t in range(1, INTERVALS + 1):
        was_refs, read_from = [[a.copy() for a in pair] for pair in clock.reference], len(clock.log)
        clock.tick()
        for r in sorted(hands_of):
            (r3, r12), (three, twelve) = clock.reference[r], clock.hands()[r].gears
            was, read = r3 * three.before + r12 * twelve.before, r3 * three.now + r12 * twelve.now
            crossed = (was * read < 0) | ((was == 0) != (read == 0))
            started = (clock.wound[r] == 1) | (r3 != was_refs[r][0]) | (r12 != was_refs[r][1])
            for where in zip(*np.nonzero(started | crossed), strict=True):
                key = (r, tuple(int(x) for x in where))
                if started[where]:
                    last.pop(key, None)
                if crossed[where]:
                    beat.update({key: (t - last[key], bool(read[where] >= 0))} if key in last else {})
                    last[key] = t
        new = [e for e in clock.log[read_from:] if e["event"] == "credit" and e["line"] in hands_of]
        chimes += [(e["beat"], beat.get((e["line"], tuple(e["node"])))) for e in new]
    assert all(by_hand is not None and b == by_hand[0] for b, by_hand in chimes)
    assert (len(chimes), sum(1 for _b, h in chimes if h and h[1])) == (201, 101)  # 275, 138; 453, 281
    assert run_back_exact(kept, INTERVALS) == INTERVALS


def test_the_take_moves_the_line_farthest_from_its_before_and_logs_it_per_take_cs4_s2() -> None:
    """CS4-S2 (the owner's word of 2026-10-25, 22:50 UTC, "all of them", through the Boss; cs4's REPORT.md sections 1.2, 1.5 and 4, The-Handed-Seed-And-Births_COMPARISON.md's finding (a) and cs5's mend, the gear logged PER UNWIND; the test under 20 s): the exact unwind moves the unwound hand's gear whose notch now stands farthest from its before (the largest now^2 - before^2, the first where equal), the gear logged as `taken_line` on every fitting, chime and unspringing unwind, the strike undone restoring that gear. The pair's 3-cube at 20 ticks (81 chimes at 4, 6 and 12 under the great clock's bounds where nothing arrives, each taking nothing and logged on the gear a take would move, bobs.still_chime; 27, the first at 336, under the wave's honest books, the run then 336 ticks; 81 in 20 before the wave) beside its image with the unsprung hand turned a quarter at the setting ((three, twelve) -> (-twelve, three): the unsprung hand on its second gear, the first at 0): the two great clocks' X equal at every clock at 20 of 20 ticks and the 81 chimes equal chime for chime in their numbers, every one logged on the first gear on the great clock and on the second on the image, where the former act (the first gear's unwind) is the stop by name (fall_of (None, 0) on a gear at 0), the rewind exact 20 of 20 through the chimes on the second gear (the numbers equal at an even count of turnovers: run to 336, every clock turns over at 84 and 252 and the image's chimes at 168 to 172 read the logged notch negated, the turnover conjugating the quarter turn); SL-S2's unspringing great clock (the heaviest hand's reflected pair at two adjacent clocks of the bare 5-cube) at 20: under MG-S1 the unspringing at the first striking with no stop before it, its two ends' notches unwound whole (no gear), six unsprung fittings after it at 9 and 17 on the unsprung hand's second gear under GP-S1 (the fitted hands advanced with the sweep's sign), each of the 11 unwinds' gears re-derived by hand from the clock's notches after the striking (the other gear untouched by the unwind, the unwound gear as the unwind found it), 11 of 11 on a gear other than the first, 5 chimes (under MG-S1 with Y-S3's six gears three unsprung fittings at 9, 19 and 20, 344 unwinds with 233 on another gear and 341 chimes, one unsprung fitting at 9 and 343 chimes before Y-S3; before MG-S1 the unspringing's two unwinds on the heavy train's second gear, 3 B against 0, the farthest at both ends, where under the former act the first gear's fall came short and the stop jammed both ends, ten unsprung fittings after it unwinding the unsprung hand's second gear but one at 19 where the first gear's gap is the larger, 87 unwinds with 66 on another gear, 0 under the former act, 74 chimes (the unspringing at the second striking on the first gear with 2 fittings, 4 unwinds and 1 chime under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting)); under the sign train's former drive of 2 W after the step, before PL-S1, 9 fittings every one on the second gear, 318 unwinds with 219 on it and 308 chimes; the rewind exact."""
    pair, image = node_of("world_pair_3.json"), node_of("world_pair_3.json")
    re, im = image.unsprung().gears
    im.now[...], im.before[...], re.now[...], re.before[...] = re.now.copy(), re.before.copy(), 0, 0
    kept = copy.deepcopy(image)
    for _ in range(INTERVALS):
        pair.tick()
        image.tick()
        assert (pair.train(REGULATOR).gears[0].now == image.train(REGULATOR).gears[0].now).all()
    keys = ("i", "node", "taken", "levels", "taker", "taken_line")
    chimes = [
        [tuple(e[k] for k in keys) for e in n.log if e["event"] == "credit"] for n in (pair, image)
    ]
    assert len(chimes[0]) == 81 and [c[:5] for c in chimes[0]] == [c[:5] for c in chimes[1]]
    assert {c[5] for c in chimes[0]} == {0} and {c[5] for c in chimes[1]} == {1}
    three = image.unsprung().gears[0]  # the live three gear, at rest at the image's chime clocks
    assert all(int(three.now[tuple(c[1])]) == int(three.before[tuple(c[1])]) for c in chimes[1])
    assert run_back_exact(kept, INTERVALS) == INTERVALS
    clock = node_of("world_node.json", shape=[5, 5, 5], seed=[])
    a, b, k = clock.A, clock.B, 3
    heavy = max(range(len(clock.hands())), key=lambda r: clock.hands()[r].spring or 0)
    for at, notches in (
        ((1, 1, 1), (k * a, 0, 0, k * b)),
        ((2, 1, 1), (k * a, b, 0, -k * b)),
        ((1, 2, 1), (a, b, 0, 0)),
        ((2, 1, 2), (b, a, 0, 0)),
    ):
        advance(clock, heavy, at, notches)
    kept, gears_unwound = copy.deepcopy(clock), []
    for _ in range(INTERVALS):
        seen = len(clock.log)
        clock.tick()
        for e in clock.log[seen:]:
            if e["event"] not in ("birth", "credit"):
                continue
            gears = clock.hands()[e.get("taken_row", clock.hands().index(clock.unsprung()))].gears
            for t in e.get("takes", [e]):
                if "taken_levels" in t:
                    continue
                at, k = tuple(t["node"]), t["taken_line"]
                gaps = [int(gear.now[at]) ** 2 - int(gear.before[at]) ** 2 for gear in gears]
                gaps[k] = t["taken_now_was"] ** 2 - t["taker"][1] ** 2
                assert gaps.index(max(gaps)) == k and t["taker"][0] == t["taken_now_was"]
                gears_unwound.append(k)
    fittings = [e for e in clock.log if e["event"] == "birth"]
    assert fittings[0]["taken_row"] == heavy and fittings[0]["taken_line"] == [None, None]
    on_first = [(e["i"], e["taken_line"]) for e in fittings if "takes" not in e and not e["taken_line"]]
    # cc1: the unspringing's unsprung hand exact at both ends, no fitted hand with a sweep, no fitting and no chime after it (7 fittings, 11 unwinds and 5 chimes before)
    assert on_first == [] and len(fittings) == 1
    assert (len(gears_unwound), sum(gears_unwound), clock.counts["body_clicks"]) == (0, 0, 0)
    assert run_back_exact(kept, INTERVALS) == INTERVALS


def test_the_unit_the_emitter_and_the_identity_turn_are_values_of_the_pair_un() -> None:
    """UN (The-Unit-And-The-Coupling_COMPARISON.md section 4, un2's table): every hand's winding of universe_toy.json is 3 T (sine_rim(pinion, rim) + rim (pinion div rim)), the one formula giving 3 T rim at the unsprung hand and 3 T s at a sprung ratio; the unsprung hand is the hand of the offset's ratio (rim, rim), the last hand; the 3-cube hole at 20 ticks gives the state hash of the former finders bit for bit; then, with pawls of -1 standing after the turnovers, the meshes at the coupling 0 turn an arbitrary pair of arrays into itself at every spoke; the rewind exact. The state hash at 20: 0b429dc0 under the great clock's bounds, moved by the first two, a tension and a load below 0 read at 0 (b4c97c7c under the wave's honest books and the own beat; 16c88d4b before the wave; ddfeb210 under EX-S1, c608a485 before it, d7f2c713 before Y-S3)."""
    clock = node_of("world_node.json")
    rim, t, all_hands = clock.rim, clock.key, clock.hands()
    assert clock.windings == [
        3 * t * (rates.sine_rim(r.ratio[0], rim) + rim * (r.ratio[0] // rim)) for r in all_hands
    ]
    assert clock.windings[-1] == clock.windings[all_hands.index(clock.unsprung())] == 3 * t * rim
    assert (
        (clock.unsprung().size, clock.unsprung().ratio)
        == (HAND, clock.train(OFFSET).ratio)
        == (2, (rim, rim))
    )
    assert clock.unsprung() is all_hands[-1]
    assert [r for r in all_hands if coupling_of(r)] == all_hands[:-1]
    kept = copy.deepcopy(clock)
    for _ in range(INTERVALS):
        clock.tick()
    # under the one mirror (0b429dc0 before it, b4c97c7c at the wave, ddfeb210 at 54); over the whole state since 2026-10-26, ff82a0da over the gears and the unwind's slack alone
    assert record.state_hash(clock) == "fba1dd44d34fe56e83947040dd6bff488d75a15431f5f82a7d96e688c5f469f4"
    tick = Tick(copy.deepcopy(clock), 1)
    tick.readings()
    assert sorted(tick.meshes_at) == [0, 1] and any(
        int(x) == -1 for f in tick.pawls for x in f.reshape(-1)
    )
    drawn = np.random.default_rng(0).integers(-(2**40), 2**40, size=(2, *clock.size)).tolist()
    pair = [np.array(a, dtype=object) for a in drawn]
    for spoke in range(SPOKES):
        assert [a.tolist() for a in clock.offset_pull(pair, spoke, tick.meshes_at[0])] == drawn
    assert run_back_exact(kept, INTERVALS) == INTERVALS


def test_the_take_keeps_its_remainder_at_the_node_and_pays_exactly_ex_s1() -> None:
    """EX-S1 (the Boss's order of 2026-10-26, 03:3x UTC, 6407630119, under the owner's delegation; H-Exact-Take-Remainder-1's REPORT.md sections 2 and 4, the one-clock test one_node_take.py re-read on the engine): the exact unwind is one carry of the clock: what the striking tallies less the unwind's slack standing at the clock is the unwind's due, the unwound gear moved by the least count of notches whose fall pays what is due (by none where the slack alone pays), the fall above what is due the new slack, one integer of the clock's state, starting at 0; on the 3-cube hole piece the unsprung gear at (1, 0, 0) fed 3,000 notches above its before and unwound twenty times for two unsprung windings by take_at alone: fall + slack before - slack after = tallied at 20 of 20 (the former unwind paid above tallied at every one), every slack below the one-notch step at its unwind, the clock's count one integer more (99 on the toy's calibre, 107 with the beats' references, two a hand), the unwind's push read at the gears of the tick's start (CL-S2's one moment, here the gears as set), the twenty unwinds undone by the advance back and the slack's restore to the state's hash before them."""
    clock = node_of("world_node.json")
    at, clock.start_gears = (1, 0, 0), [r.gears for r in clock.hands()]
    unsprung = clock.unsprung()
    rec0, z = clock.hands().index(unsprung), unsprung.gears[0]
    z.now[at] = int(z.before[at]) + 3_000
    c = readings.load(clock)
    clock.start_load, clock.start_stretch = c, clock.train(REGULATOR).gears[0].now
    gearing = readings.gearing_of(clock, unsprung, c, factors(clock))
    windings = clock.windings[rec0] + clock.windings[rec0]
    hash_before, undo, paid, below = record.state_hash(clock), [], 0, 0
    for _ in range(20):
        got = unwinds(clock, [(at, windings)], gearing, 1)  # the one unwind act at one end (CR-S2)
        assert got is not None
        (unwind,) = got
        fall, now, k = unwind["taken"], unwind["taken_now_was"], unwind["taken_line"]
        slack_was, slack = unwind["remainder_was"], unwind["remainder"]
        paid += fall + slack_was - slack == windings
        below += 0 <= slack < fall_of(clock, at, 1, gearing, unsprung)[1]
        undo.append((now, k, slack_was))
    assert (paid, below) == (20, 20) and record.census(clock)[0] == 107
    for now, k, slack_was in reversed(undo):
        move(clock, rec0, k, at, now - int(unsprung.gears[k].now[at]))
        clock.strikes[at] -= 1
        clock.slack[at] = slack_was
    assert record.state_hash(clock) == hash_before
