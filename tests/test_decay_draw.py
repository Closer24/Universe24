"""A decaying group draws at its corner meetings (decay-draw-v1, Highlights 3.26 and
3.19): a bound group that can decay is a source, a source is a Detector, and in
the loop form its ticks are its corner meetings, so a `ray_interactions` rule with
outputs that declares `draw: [n, d]` and its `seed` draws once at every meeting of
its participants, from the Node's ticket stream, the unsalted draw of
detector-mark-v1; on 1 the conversion fires, on 0 the rule does not fire and the
meeting continues to the next rule in declared order, the corner table, which
reproduces the ring. The world is the unit-square electron of E5
(`examples/nature/ring.json`, built inline as `test_loop_binding.py` does) with
a second family `p` and the rule `decay` over `[electron, electron]` declared
before `corner`, setting 1/64 and seed 6, converting the two electrons into two
rays of `p` on the same headings, charge and energy exact. The ring survives
while every corner draws 0, the first 1 converts one pair and its orbit
disperses (a corner with one electron fires nothing), the other four-ray orbit
keeps drawing until its own 1, the ledger is exact at every tick, the tickets
consumed equal the meetings that drew, a replay is identical, a world without
`draw` never calls the ticket rule, and the malformed declarations are rejected.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Decay draw") before
the first run: the draw sequence per corner by the published ticket rule from
the rule's seed salted by the corner's position, the first draw of 1 at P1 in
the cycle of tick 11, the second at P1 in the cycle of tick 26, 74 draws in all.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.spatial_state import (
    DECAY_DRAW,
    TICKET_MODULUS,
    Ray,
    decay_ticket_seed,
    ray_merge_key,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
P0, P1, P2, P3 = (5, 5, 5), (6, 5, 5), (6, 6, 5), (5, 6, 5)
CORNERS = (P0, P1, P2, P3)
# The R sense P0 -> P1 -> P2 -> P3 -> P0 and the L sense P0 -> P3 -> P2 -> P1 -> P0:
# the Port each sense leaves each corner through.
R_PORTS = (0, 2, 1, 3)
L_PORTS = (2, 1, 3, 0)
ZERO = (0, 0, 0)
SEED = 6
SETTING = (1, 64)
TICKS = 36
ENERGY = {"name": "energy", "expression": {"field": "amount"}}
CORNER = {
    "name": "corner",
    "participants": [{"type": "electron"}, {"type": "electron"}],
    "outputs": [
        {"field": "electron", "amount": {"of": 0}, "heading": "reversed", "input": 1, "phase": {"of": 0}},
        {"field": "electron", "amount": {"of": 1}, "heading": "reversed", "input": 0, "phase": {"of": 1}},
    ],
    "invariants": [ENERGY],
}
# The decaying conversion: the two electrons of a corner meeting become two rays of
# `p` leaving on the same headings, each with its input's amount and phase.
DECAY = {
    "name": "decay",
    "participants": [{"type": "electron"}, {"type": "electron"}],
    "draw": list(SETTING),
    "seed": SEED,
    "outputs": [
        {"field": "p", "amount": {"of": 0}, "heading": "same", "input": 0, "phase": {"of": 0}},
        {"field": "p", "amount": {"of": 1}, "heading": "same", "input": 1, "phase": {"of": 1}},
    ],
    "invariants": [ENERGY],
}


def lamps():
    """The corner lamps: (position, name, Port), one per sense per corner."""
    result = []
    for k in range(4):
        result.append((CORNERS[k], f"corner_{k}_r", R_PORTS[k]))
        result.append((CORNERS[k], f"corner_{k}_l", L_PORTS[k]))
    return result


def ray_family(name):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 8,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": 3,
        "kerengonen": {"phase_advance": 2},
        "charge": -3,
    }


def document(rules=(DECAY, CORNER), ticks=TICKS):
    """The E5 ring with a second family `p` (charge -3 like the electron, so the
    conversion keeps the charge; its momentum bound through an emission of a lamp
    type that is never seeded) and the declared rules in order."""
    return {
        "schema_version": 1,
        "model_id": "decay-draw-test-v1",
        "shape": [12, 12, 11],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": name,
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            }
            for name in ("electron", "p")
        ]
        + [
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            }
        ],
        "disturbance_types": [
            {
                "name": name,
                "fields": ["electron", "momentum"],
                "defaults": {"electron": 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for _, name, _ in lamps()
        ]
        + [
            {
                "name": "p_lamp",
                "fields": ["p", "momentum"],
                "defaults": {"p": 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [ray_family("electron"), ray_family("p")],
        "emissions": [
            {
                "type": name,
                "field": "electron",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": HEADINGS[port],
                "kerengonen_phase": 0,
            }
            for _, name, port in lamps()
        ]
        + [
            {
                "type": "p_lamp",
                "field": "p",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": HEADINGS[0],
                "kerengonen_phase": 0,
            }
        ],
        "seeds": [{"position": list(position), "type": name} for position, name, _ in lamps()],
        "ray_interactions": [dict(rule) for rule in rules],
    }


def ray(heading, amount, phase, steps, mask, shares):
    return Ray(heading, ZERO, amount, phase=phase, steps=steps, event_ports=mask, event_shares=shares)


def rays_at(world, position, family=0):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return sorted(node.rays[family], key=ray_merge_key) if node is not None and node.rays else []


def state(world):
    return {position: rays_at(world, position) for position in CORNERS}


def ledger(world):
    """Electron, p, momentum, escaped electron and p, the charge lines, balance."""
    totals, escaped, charge = world.totals(), world.escaped_totals(), world.charge_totals()
    balanced = all(item["balanced"] for item in world.spatial_accounting().values())
    return (
        totals["electron"],
        totals["p"],
        totals["momentum"],
        escaped["electron"],
        escaped["p"],
        charge["electron"],
        charge["p"],
        balanced,
    )


# After tick 1: each corner holds its lamps' two rays, stamped by their emission.
LAMP_LINES = {
    P0: [(1, 2, (0, 1, 0, 0, 0, 0)), (3, 8, (0, 0, 0, 1, 0, 0))],
    P1: [(0, 1, (1, 0, 0, 0, 0, 0)), (3, 8, (0, 0, 0, 1, 0, 0))],
    P2: [(0, 1, (1, 0, 0, 0, 0, 0)), (2, 4, (0, 0, 1, 0, 0, 0))],
    P3: [(1, 2, (0, 1, 0, 0, 0, 0)), (2, 4, (0, 0, 1, 0, 0, 0))],
}
# From tick 2: the same eight lines, each ray stamped by the corner it last left.
RING_LINES = {
    P0: [(1, 6, (0, 1, 1, 0, 0, 0)), (3, 9, (1, 0, 0, 1, 0, 0))],
    P1: [(0, 5, (1, 0, 1, 0, 0, 0)), (3, 10, (0, 1, 0, 1, 0, 0))],
    P2: [(0, 9, (1, 0, 0, 1, 0, 0)), (2, 6, (0, 1, 1, 0, 0, 0))],
    P3: [(1, 10, (0, 1, 0, 1, 0, 0)), (2, 5, (1, 0, 1, 0, 0, 0))],
}
# The momentum the two quarter turns of a corner move, booked as that corner's source.
CORNER_SOURCES = {P0: (2, 2, 0), P1: (-2, 2, 0), P2: (-2, -2, 0), P3: (2, -2, 0)}
# The orbit whose pair meets at a corner in the cycle of a tick: orbit A (the lamps
# of P0 and P2) meets at P1 and P3 on odd ticks and at P0 and P2 on even ticks,
# orbit B (the lamps of P1 and P3) the other way round.
ORBIT_A_CORNERS = {1: (P1, P3), 0: (P0, P2)}
# Pinned by the published ticket rule from seed 6 salted by each corner's position
# (docs/TEST_EXPECTATIONS.md, "Decay draw"): the stream's start per corner, the
# ticket state and bit of the first draw (tick 1), of the draws in the cycle of
# tick 11 (the first 1, at P1), and the last draw and its tick per corner.
START_TICKETS = {P0: 276043064, P1: 458648927, P2: 458697198, P3: 276091335}
TICK_1_TICKETS = {P0: 812882644, P1: 1034149616, P2: 143013690, P3: 995488507}
TICK_11_DRAWS = {P0: (724645537, 0), P1: (470793086, 1), P2: (866042076, 0), P3: (46152738, 0)}
FIRST_ONE = (11, P1)
SECOND_ONE = (26, P1)
LAST_DRAWS = {
    P0: (25, 334272102),
    P1: (26, 549671329),
    P2: (25, 758871333),
    P3: (26, 758084520),
}
DRAWS_PER_CORNER = {P0: 18, P1: 19, P2: 18, P3: 19}


def lines(table, phase, corners=CORNERS):
    return {
        position: [ray(heading, 1, phase, 1, mask, shares) for heading, mask, shares in table[position]]
        if position in corners
        else []
        for position in CORNERS
    }


def meeting_corners(tick):
    """The corners that meet two electrons in the cycle of `tick`: all four through
    the first conversion (tick 11), then orbit B's two until its own (tick 26)."""
    if tick <= FIRST_ONE[0]:
        return CORNERS
    if tick <= SECOND_ONE[0]:
        return tuple(c for c in CORNERS if c not in ORBIT_A_CORNERS[tick % 2])
    return ()


def expected_state(tick):
    """The corner lines after tick t (the state the cycle of tick t meets)."""
    phase = (2 * tick) % 8
    if tick == 1:
        return lines(LAMP_LINES, phase)
    if tick <= 11:
        return lines(RING_LINES, phase)
    # The cycle of tick 11 converted orbit A's pair at P1; orbit A's other pair
    # left P3 for P0 and P2, where each ray is alone after tick 12 and crosses off.
    corners = meeting_corners(tick)
    expected = lines(RING_LINES, phase, corners)
    if tick == 12:
        expected[P0] = [ray(3, 1, phase, 1, 9, (1, 0, 0, 1, 0, 0))]
        expected[P2] = [ray(0, 1, phase, 1, 9, (1, 0, 0, 1, 0, 0))]
    if tick == 27:
        expected[P0] = [ray(3, 1, phase, 1, 9, (1, 0, 0, 1, 0, 0))]
        expected[P2] = [ray(0, 1, phase, 1, 9, (1, 0, 0, 1, 0, 0))]
    return expected


def loose_rays(tick):
    """The p rays and the lone electrons off the ring after tick t: (position,
    family, heading, steps) for each; escaped once past the open boundary."""
    result = []
    for conversion in (FIRST_ONE[0], SECOND_ONE[0]):
        since = tick - conversion
        # The two p rays leave P1 on +X and -Y in the cycle of the conversion.
        if 1 <= since <= 5:
            result.append(((6 + since, 5, 5), 1, 0, since))
            result.append(((6, 5 - since, 5), 1, 3, since))
        # The other pair of the orbit leaves P3 for P0 (-Y) and P2 (+X) the same
        # cycle, is alone there after the next tick (a corner, not loose), and
        # crosses off the ring.
        if 2 <= since <= 6:
            result.append(((5, 5 - (since - 1), 5), 0, 3, since))
            result.append(((6 + (since - 1), 6, 5), 0, 0, since))
    return sorted(result)


def expected_ledger(tick):
    """The world after tick t: the p rays of a conversion escape the open board
    six ticks after it, the two lone electrons seven; each pair off the ring
    carries momentum (1, -1, 0) while it is in the world, the ring's rays and
    the lamps' recoils summing to zero."""
    conversions = (FIRST_ONE[0], SECOND_ONE[0])
    electron = 8 - 2 * sum(1 for t in conversions if tick > t)
    escaped_p = 2 * sum(1 for t in conversions if tick > t + 5)
    escaped_e = 2 * sum(1 for t in conversions if tick > t + 6)
    p = (8 - electron) - escaped_p
    electron -= escaped_e
    pairs = sum(1 for t in conversions if t < tick <= t + 5) + sum(
        1 for t in conversions if t < tick <= t + 6
    )
    return (
        (electron,),
        (p,),
        (pairs, -pairs, 0),
        (escaped_e,),
        (escaped_p,),
        -3 * electron,
        -3 * p,
        True,
    )


def tool(name):
    spec = importlib.util.spec_from_file_location(
        "tools.ray_viewer." + name, ROOT / "tools/ray_viewer" / (name + ".py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_a_decaying_group_draws_at_its_corner_meetings(tmp_path, monkeypatch):
    initial = parse_initial_state(document())
    assert initial.ray_interactions[0].draw == SETTING
    assert initial.ray_interactions[0].seed == SEED
    assert initial.ray_interactions[1].draw is None
    assert {c: decay_ticket_seed(SEED, c) for c in CORNERS} == START_TICKETS
    # (a) Tick by tick: the ring's lines while every corner draws 0, the first 1 at
    # P1 in the cycle of tick 11 converting orbit A's pair into two p rays on the
    # same headings, orbit A's other pair dispersing (a corner with one electron
    # fires nothing), orbit B circulating as the four-ray ring and drawing until
    # its own 1 at P1 in the cycle of tick 26, then nothing left; the ledger exact
    # and every family's charge with it at every tick.
    world = Simulation(initial)
    for tick in range(1, TICKS + 1):
        world.step()
        assert state(world) == expected_state(tick), tick
        loose = sorted(
            (node.position, family, r.heading, r.steps)
            for node in world.inventory_view().nodes
            if node.rays and node.position not in CORNERS
            for family, bundle in enumerate(node.rays)
            for r in bundle
        )
        assert loose == loose_rays(tick), tick
        assert ledger(world) == expected_ledger(tick), tick
    assert world.totals()["momentum"] == ZERO
    assert world.source_totals() == {"electron": (-4,), "p": (4,), "momentum": (4, -4, 0)}
    assert world.escaped_totals()["momentum"] == (4, -4, 0)
    # The tickets consumed: one per meeting of the decaying rule at each corner,
    # the Node's stream ending exactly where the last draw left it.
    for corner in CORNERS:
        node = world._spatial.nodes[corner]
        assert node.detector is None
        assert node.detector_ticket == LAST_DRAWS[corner][1], corner
    assert all(
        node.detector_ticket == decay_ticket_seed(SEED, node.position)
        for node in world._spatial.nodes.values()
        if node.position not in CORNERS
    )
    # (b) The record: one `decay_draw` line per meeting of the rule, the pinned
    # tickets and bits, the corner bookings, the conversions' family sources, the
    # identity, the group read from the record, and an identical replay.
    path = tmp_path / "decay.json"
    path.write_text(json.dumps(document()), encoding="utf-8")
    records = []
    for name in ("first", "second"):
        run_initialization(path, tmp_path / name, ticks=TICKS)
        events = (tmp_path / name / "events.jsonl").read_text(encoding="utf-8")
        metadata = json.loads((tmp_path / name / "run.json").read_text(encoding="utf-8"))
        metadata.pop("elapsed_seconds")
        records.append((events, metadata))
    (first_events, first_run), (second_events, second_run) = records
    assert first_events == second_events and first_run == second_run
    assert first_run["decay_draw"] == DECAY_DRAW == "decay-draw-v1"
    assert first_run["loop_binding"] == "loop-binding-v1"
    assert first_run["ray_meeting"] == "ray-meeting-conversion-v1"
    assert first_run["conserved_at_every_completed_tick"]
    assert first_run["final_totals"] == {"electron": [0], "p": [0], "momentum": [0, 0, 0]}
    assert first_run["escaped_totals"] == {"electron": [4], "p": [4], "momentum": [4, -4, 0]}
    assert first_run["source_totals"] == {"electron": [-4], "p": [4], "momentum": [4, -4, 0]}
    recorded = [json.loads(line) for line in first_events.splitlines()]
    draws = [e for e in recorded if e["event"] == "decay_draw"]
    assert len(draws) == 74
    assert all(e["rule"] == "decay" and e["setting"] == list(SETTING) for e in draws)
    for tick in range(1, TICKS + 1):
        here = [e for e in draws if e["tick"] == tick]
        assert [tuple(e["position"]) for e in here] == list(meeting_corners(tick)), tick
    assert [(e["tick"], tuple(e["position"])) for e in draws if e["bit"]] == [FIRST_ONE, SECOND_ONE]
    assert {tuple(e["position"]): e["ticket"] for e in draws if e["tick"] == 1} == TICK_1_TICKETS
    assert {tuple(e["position"]): (e["ticket"], e["bit"]) for e in draws if e["tick"] == 11} == (
        TICK_11_DRAWS
    )
    for corner in CORNERS:
        own = [e for e in draws if tuple(e["position"]) == corner]
        assert len(own) == DRAWS_PER_CORNER[corner]
        assert (own[-1]["tick"], own[-1]["ticket"]) == LAST_DRAWS[corner]
    cycles = {
        (e["tick"], tuple(e["position"])): e["source_delta"]
        for e in recorded
        if e["event"] == "spatial_cycle" and tuple(e["position"]) in CORNERS
    }
    for tick in range(1, TICKS + 1):
        for corner in meeting_corners(tick):
            if (tick, corner) in (FIRST_ONE, SECOND_ONE):
                assert cycles[(tick, corner)] == {"electron": [-2], "p": [2]}, (tick, corner)
            else:
                assert cycles[(tick, corner)].get("momentum") == list(CORNER_SOURCES[corner])
                assert "p" not in cycles[(tick, corner)]
        for corner in CORNERS:
            if corner not in meeting_corners(tick) and (tick, corner) in cycles:
                assert "momentum" not in cycles[(tick, corner)], (tick, corner)
    extract = tool("extract")
    sidecar = tool("record_sidecar")
    sidecar.write_sidecar(tmp_path / "first")
    run = extract.extract_record(tmp_path / "first", sidecar=tmp_path / "first" / "ray-recording.json")
    (group,) = run["groups"]
    assert (group["ring"], group["content"], group["families"], group["period"], group["clock"]) == (
        [list(P0), list(P1), list(P2), list(P3)],
        8,
        {"electron": 8},
        4,
        {"electron": 2},
    )
    assert group["from_tick"] == 1
    assert group["to_tick"] == 11
    assert [row["bound"] for row in run["ticks_data"]][:12] == [{}] + [{"electron": [8]}] * 11
    # (c) A world without `draw` runs the ring as before: no draw line, no
    # identity, every unmarked Node's stream at 0 and the ticket rule never called.
    control = parse_initial_state(document(rules=(CORNER,)))
    assert all(rule.draw is None for rule in control.ray_interactions)

    def forbidden(state, salt):
        pytest.fail("a world without draw consumed a ticket")

    with monkeypatch.context() as patched:
        patched.setattr("event_universe.core.spatial_state.next_ticket", forbidden)
        ring = Simulation(control)
        for tick in range(1, 17):
            ring.step()
            assert state(ring) == lines(LAMP_LINES if tick == 1 else RING_LINES, (2 * tick) % 8)
            assert ledger(ring) == ((8,), (0,), ZERO, (0,), (0,), -24, 0, True)
        assert all(node.detector_ticket == 0 for node in ring._spatial.nodes.values())
    control_path = tmp_path / "ring.json"
    control_path.write_text(json.dumps(document(rules=(CORNER,), ticks=16)), encoding="utf-8")
    run_initialization(control_path, tmp_path / "ring", ticks=16)
    control_run = json.loads((tmp_path / "ring" / "run.json").read_text(encoding="utf-8"))
    assert "decay_draw" not in control_run
    control_events = (tmp_path / "ring" / "events.jsonl").read_text(encoding="utf-8")
    assert "decay_draw" not in control_events
    # (d) The rejections, before any world exists.
    held = {
        "name": "bind",
        "participants": [{"type": "electron"}, {"type": "electron"}],
        "assignments": [
            {"participant": 0, "field": "delay", "expression": 1},
            {"participant": 1, "field": "delay", "expression": 1},
        ],
        "invariants": [
            {
                "name": "energy",
                "expression": {
                    "op": "add",
                    "args": [
                        {"field": "amount", "participant": 0},
                        {"field": "amount", "participant": 1},
                    ],
                },
            }
        ],
    }
    for rule, message in (
        (held | {"draw": [1, 64], "seed": SEED}, "requires a ray interaction with outputs"),
        (DECAY | {"draw": [3, 2]}, "n at most d"),
        (DECAY | {"draw": [1, 0]}, "draw denominator must be an integer from 1"),
        (DECAY | {"draw": [-1, 2]}, "draw numerator must be an integer from 0"),
        (DECAY | {"draw": [1, 2.5]}, "draw denominator must be an integer"),
        (DECAY | {"draw": [1]}, "array of length 2 through 2"),
        ({k: v for k, v in DECAY.items() if k != "seed"}, "requires its seed"),
        ({k: v for k, v in DECAY.items() if k != "draw"}, "requires draw"),
        (DECAY | {"seed": TICKET_MODULUS}, "below the ticket modulus"),
        (DECAY | {"seed": -1}, "ray interaction seed must be an integer from 0"),
    ):
        raw = document(rules=(rule, CORNER))
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
        assert not validate_configuration(json.dumps(raw)).valid
