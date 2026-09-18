"""Binding as a loop (loop-binding-v1, Highlights 3.4 and 3.28): a ray never
stops, and a bound group is a periodic orbit of the ordinary meeting rule, a set
of rays on a ring of Nodes whose corner meetings, under an ordinary rule with
outputs, reproduce the rays that entered them. The unit-square electron of
`examples/nature/ring.json`, built inline: eight rays circulating both ways on
four Nodes under the Port form of the corner table hold every tick with content
8, period 8 (K 1: a ray of 1 advances one step per interval, clock-readings-v1,
2026-09-18; the rate 2 of the first pin is out of the bound content / K < N / 2
for a corner's merged output of 2 at N = 8) and their phases as the clock; under the catalog's Born table with
the senses in phase the ring disperses (`ring_open.json`); at the catalog's rate
1 the state repeats after two circuits; four rays close the smallest loop; the
Born table closes the ring in quadrature. Nothing at a Node names a group: the
snapshot lists none, no `bound_tick` is written, the world ledger keeps every
line exact with the momentum of the corner turns booked as each corner's source,
and the group is read from the record by the ray viewer's extractor (its ring,
content, period and clock). The held form of feature 8 is gone: `ray_delay` and
a `momentum_table` beside `assignments` are rejected at parsing with a message
naming the migration note.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Loop binding")
before the first run.
"""

import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import LOOP_BINDING, Ray, ray_merge_key
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
BORN = [8, 7, 4, 1, 0, 1, 4, 7]
ENERGY = {"name": "energy", "expression": {"field": "amount"}}
PORT_CORNER = {
    "name": "corner",
    "participants": [{"type": "electron"}, {"type": "electron"}],
    "outputs": [
        {
            "field": "electron",
            "amount": {"of": 0},
            "heading": "reversed",
            "input": 1,
            "phase": {"of": 0},
        },
        {
            "field": "electron",
            "amount": {"of": 1},
            "heading": "reversed",
            "input": 0,
            "phase": {"of": 1},
        },
    ],
    "invariants": [ENERGY],
}
BORN_CORNER = {
    "name": "corner",
    "participants": [{"type": "electron"}, {"type": "electron"}],
    "outputs": [
        {
            "field": "electron",
            # phase-spread-v1 (2026-09-18): the steering table is the family's, written
            # from its phase width ([8, 7, 4, 1, 0, 1, 4, 7] at eight steps), never declared.
            "amount": {"of": "sum", "index": "phase_difference"},
            "heading": "reversed",
            "input": 1,
            "phase": {"of": 0},
        },
        {
            "field": "electron",
            "amount": {"rest_of": 0},
            "heading": "reversed",
            "input": 0,
            "phase": {"of": 1},
        },
    ],
    "invariants": [ENERGY],
}


def lamps(corners=(0, 1, 2, 3), l_phase=0):
    """The corner lamps: (position, name, Port, phase), one per sense per corner."""
    result = []
    for k in corners:
        result.append((CORNERS[k], f"corner_{k}_r", R_PORTS[k], 0))
        result.append((CORNERS[k], f"corner_{k}_l", L_PORTS[k], l_phase))
    return result


def document(rule, clock=1, corners=(0, 1, 2, 3), l_phase=0, ticks=16):
    return {
        "schema_version": 1,
        "N": 8,
        "K": clock,
        "model_id": "loop-binding-test-v1",
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
                "name": "electron",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": name,
                "fields": ["electron", "momentum"],
                "defaults": {"electron": 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for _, name, _, _ in lamps(corners, l_phase)
        ],
        "spatial_fields": [
            {
                "field": "electron",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 1,
                "metric": "links",
                "pace": [1, 1],
                # The clock is the content (clock-readings-v1, 2026-09-18): a ray
                # of 1 advances one step per interval at K 1 and one step every
                # second interval at K 2; no rate is declared.
                "clock": True,
                "charge": -3,
            }
        ],
        "emissions": [
            {
                "type": name,
                "field": "electron",
                "amount": 1,
                "denominator": 1,
                "heading": HEADINGS[port],
                "kerengonen_phase": phase,
            }
            for _, name, port, phase in lamps(corners, l_phase)
        ],
        "seeds": [
            {"position": list(position), "type": name}
            for position, name, _, _ in lamps(corners, l_phase)
        ],
        "ray_interactions": [rule],
    }


def ray(heading, amount, phase, steps, mask, shares):
    return Ray(heading, ZERO, amount, phase=phase, steps=steps, event_ports=mask, event_shares=shares)


def rays_at(world, position):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`), and since charge-per-thing-v1 (the same day) a Born product
    # that took the whole content of a corner carries the other thing's identity
    # too (`owners`, point 25); this module pins lines and events, not identities
    # (test_bit_law and test_charge_per_thing do).
    rays = node.rays[0] if node is not None and node.rays else ()
    return sorted((replace(ray, owner=0, owners=()) for ray in rays), key=ray_merge_key)


def state(world):
    return {position: rays_at(world, position) for position in CORNERS}


def balanced(world):
    return all(item["balanced"] for item in world.spatial_accounting().values())


def ledger(world):
    """The world's electron, momentum and charge readouts and the ledger's balance."""
    return (
        world.totals()["electron"],
        world.totals()["momentum"],
        world.escaped_totals()["electron"],
        world.charge_totals()["electron"],
        balanced(world),
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
# The momentum the two quarter turns of a corner move, booked as that corner's
# source under the Port form and in quadrature; under the Born form in phase.
PORT_SOURCES = {P0: (2, 2, 0), P1: (-2, 2, 0), P2: (-2, -2, 0), P3: (2, -2, 0)}
BORN_SOURCES = {P0: (1, 3, 0), P1: (-1, 3, 0), P2: (-1, -3, 0), P3: (1, -3, 0)}


def lines(table, phase, phases=None, remainder=0):
    """The expected rays of every corner: (heading, mask, shares) with a phase and
    the clock's remainder (clock-readings-v1)."""
    return {
        position: [
            replace(
                ray(heading, 1, phase if phases is None else phases[position][index], 1, mask, shares),
                remainder=remainder,
            )
            for index, (heading, mask, shares) in enumerate(entries)
        ]
        for position, entries in table.items()
    }


def corner_sources(records, tick):
    """The momentum each corner booked in its cycle of `tick`, from the record."""
    found = {}
    for event in records:
        if event["event"] == "spatial_cycle" and event["tick"] == tick:
            position = tuple(event["position"])
            booked = event["source_delta"].get("momentum")
            if position in CORNERS and booked is not None:
                found[position] = tuple(booked)
    return found


def tool(name):
    spec = importlib.util.spec_from_file_location(
        "tools.ray_viewer." + name, ROOT / "tools/ray_viewer" / (name + ".py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("case", ["ring", "open", "slow", "half", "quadrature", "record", "rejected"])
def test_a_bound_group_is_a_periodic_orbit_of_the_meeting_rule(tmp_path, case):
    if case == "ring":
        # (a) The Port form at K 1 (a ray of 1 advances one step per interval,
        # clock-readings-v1; the rate 2 of the first pin needs a content of 2
        # per ray, whose merged corner outputs of 4 the bound content / K < N / 2
        # refuses at N = 8): every corner meets every interval from the cycle of
        # tick 1, the lines close in one circuit and the phases in two, content 8
        # exact.
        world = Simulation(parse_initial_state(document(PORT_CORNER)))
        seen = {}
        for tick in range(1, 17):
            world.step()
            if tick == 1:
                assert state(world) == lines(LAMP_LINES, 1)
            else:
                assert state(world) == lines(RING_LINES, tick % 8)
            seen[tick] = state(world)
            if tick >= 6:
                assert seen[tick] != seen[tick - 4]
            if tick >= 10:
                assert seen[tick] == seen[tick - 8]
            assert ledger(world) == ((8,), ZERO, (0,), -24, True)
            assert world.source_totals()["momentum"] == ZERO
            assert "bound_groups" not in world.snapshot()
        return
    if case == "open":
        # (b) The Born form with the senses in phase: d = 0 sends each corner's
        # whole content one way, the next corner holds one ray, and it crosses off
        # the square; the eight quanta leave the open board by tick 8.
        world = Simulation(parse_initial_state(document(BORN_CORNER)))
        for tick in range(1, 17):
            world.step()
            electron = 8 if tick < 8 else 0
            assert ledger(world) == ((electron,), ZERO, (8 - electron,), -3 * electron, True)
            if tick == 1:
                assert state(world) == lines(LAMP_LINES, 1)
            elif tick == 2:
                # The merged output of 2 leaves at the inputs' phase 1 and advances
                # two steps per Link at K 1: phase 3 one Link on.
                assert state(world) == {
                    P0: [ray(3, 2, 3, 1, 8, (0, 0, 0, 2, 0, 0))],
                    P1: [ray(3, 2, 3, 1, 8, (0, 0, 0, 2, 0, 0))],
                    P2: [ray(2, 2, 3, 1, 4, (0, 0, 2, 0, 0, 0))],
                    P3: [ray(2, 2, 3, 1, 4, (0, 0, 2, 0, 0, 0))],
                }
            elif tick <= 7:
                assert state(world) == {position: [] for position in CORNERS}
                phase = (2 * tick - 1) % 8
                for x in (5, 6):
                    assert rays_at(world, (x, 7 - tick, 5)) == [
                        ray(3, 2, phase, tick - 1, 8, (0, 0, 0, 2, 0, 0))
                    ]
                    assert rays_at(world, (x, 4 + tick, 5)) == [
                        ray(2, 2, phase, tick - 1, 4, (0, 0, 2, 0, 0, 0))
                    ]
            else:
                assert not any(n.rays and any(n.rays) for n in world.inventory_view().nodes)
        return
    if case == "slow":
        # (c) The Port form at K 2: a ray of 1 advances (remainder + 1) // 2
        # steps per interval, one every second interval with the remainder kept
        # on the ray (clock-readings-v1), the same lines with phase t // 2 mod 8,
        # the state repeating after four circuits, nothing dispersing.
        world = Simulation(parse_initial_state(document(PORT_CORNER, clock=2, ticks=20)))
        seen = {}
        for tick in range(1, 20):
            world.step()
            assert state(world) == lines(
                LAMP_LINES if tick == 1 else RING_LINES, (tick // 2) % 8, remainder=tick % 2
            )
            seen[tick] = state(world)
            if tick >= 6:
                assert seen[tick] != seen[tick - 4]
                assert all(
                    a.phase == (b.phase + 2) % 8
                    for position in CORNERS
                    for a, b in zip(seen[tick][position], seen[tick - 4][position], strict=True)
                )
            if tick >= 18:
                assert seen[tick] == seen[tick - 16]
            assert ledger(world) == ((8,), ZERO, (0,), -24, True)
        world.step()
        assert state(world) == seen[4]
        return
    if case == "half":
        # (d) Four rays, the two lamps at P0 and at P2: the smallest loop, two
        # corners meeting in every interval, content 4.
        world = Simulation(parse_initial_state(document(PORT_CORNER, corners=(0, 2), ticks=10)))
        seen = {}
        for tick in range(1, 11):
            world.step()
            phase = tick % 8
            if tick == 1:
                expected = {
                    P0: [],
                    P1: lines(LAMP_LINES, phase)[P1],
                    P2: [],
                    P3: lines(LAMP_LINES, phase)[P3],
                }
            elif tick % 2 == 0:
                expected = {
                    P0: lines(RING_LINES, phase)[P0],
                    P1: [],
                    P2: lines(RING_LINES, phase)[P2],
                    P3: [],
                }
            else:
                expected = {
                    P0: [],
                    P1: lines(RING_LINES, phase)[P1],
                    P2: [],
                    P3: lines(RING_LINES, phase)[P3],
                }
            assert state(world) == expected
            seen[tick] = state(world)
            if tick >= 6:
                assert seen[tick] != seen[tick - 4]
            if tick >= 10:
                assert seen[tick] == seen[tick - 8]
            assert ledger(world) == ((4,), ZERO, (0,), -12, True)
        return
    if case == "quadrature":
        # (e) The Born form with the L lamps at phase 2: d = 2 or 6 at every
        # corner, T[d] = 4, half the shared content each way, the ring closes with
        # the lines of (a), the L rays two steps ahead.
        world = Simulation(parse_initial_state(document(BORN_CORNER, l_phase=2, ticks=6)))
        l_headings = {P0: 1, P1: 3, P2: 0, P3: 2}
        seen = {}
        for tick in range(1, 7):
            world.step()
            table = LAMP_LINES if tick == 1 else RING_LINES
            phases = {
                position: [
                    (tick + (2 if heading == l_headings[position] else 0)) % 8
                    for heading, _, _ in table[position]
                ]
                for position in CORNERS
            }
            assert state(world) == lines(table, 0, phases)
            seen[tick] = state(world)
            if tick >= 6:
                assert seen[tick] != seen[tick - 4]
            assert ledger(world) == ((8,), ZERO, (0,), -24, True)
        return
    if case == "record":
        # (f) The record of (a) and of (b) through the runner, and the reading of
        # the group from it: the corner turns are booked as each corner's source
        # in its cycle record, no `bound_tick` exists, the run record carries the
        # loop identity and no motion identity, and the ray viewer's extractor
        # reads one group on the unit square, content 8, period 8, clock 1 on the
        # 8-step circle (K 1, clock-readings-v1), from tick 1 to tick 15; the
        # control reads none.
        extract = tool("extract")
        sidecar = tool("record_sidecar")
        for name, rule, sources in (
            ("ring", PORT_CORNER, PORT_SOURCES),
            ("open", BORN_CORNER, BORN_SOURCES),
        ):
            path = tmp_path / f"{name}.json"
            path.write_text(json.dumps(document(rule)), encoding="utf-8")
            record = tmp_path / name
            # 24 ticks: the extractor's window must cover two periods of 8.
            run_initialization(path, record, ticks=24)
            metadata = json.loads((record / "run.json").read_text(encoding="utf-8"))
            assert metadata["loop_binding"] == LOOP_BINDING == "loop-binding-v1"
            assert metadata["ray_meeting"] == "ray-meeting-conversion-v1"
            assert "bound_group_motion" not in metadata
            assert metadata["conserved_at_every_completed_tick"]
            records = [
                json.loads(line)
                for line in (record / "events.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            assert not any(e["event"] in ("bound_tick", "bound_group_step") for e in records)
            assert corner_sources(records, 1) == sources
            if name == "ring":
                assert all(corner_sources(records, tick) == sources for tick in range(1, 24))
                assert metadata["final_totals"] == {"electron": [8], "momentum": [0, 0, 0]}
            else:
                assert corner_sources(records, 2) == {}
                assert metadata["final_totals"] == {"electron": [0], "momentum": [0, 0, 0]}
                assert metadata["escaped_totals"]["electron"] == [8]
            # Without the phase recording the pattern of Nodes, headings and amounts
            # alone is read: on the eight-ray ring it is the same every interval,
            # period 1, and the clock is unknown; the phases make the period 8
            # (K 1, clock-readings-v1).
            plain = extract.extract_record(record)
            sidecar.write_sidecar(record)
            run = extract.extract_record(record, sidecar=record / "ray-recording.json")
            if name == "open":
                assert run["groups"] == []
                assert all(row["bound"] == {} for row in run["ticks_data"])
                continue
            (group,) = run["groups"]
            assert group == {
                "ring": [list(P0), list(P1), list(P2), list(P3)],
                "ring_size": 4,
                "content": 8,
                "families": {"electron": 8},
                "period": 8,
                "clock": {"electron": 1},
                "phase_steps": {"electron": 8},
                "from_tick": 1,
                "to_tick": 23,
                "rays": group["rays"],
            }
            assert len(group["rays"]) == 184
            assert all(run["rays"][i]["group"] == 0 for i in group["rays"])
            assert all(r["group"] is None for r in run["rays"] if r["id"] not in group["rays"])
            assert [row["bound"] for row in run["ticks_data"]] == [{}] + [{"electron": [8]}] * 23 + [{}]
            assert [(g["content"], g["period"], g["clock"]) for g in plain["groups"]] == [
                (8, 1, {"electron": None})
            ]
        return
    # (g) The held form is gone: a `ray_delay` on a rule and a `momentum_table`
    # beside `assignments` are rejected at parsing, naming the migration note.
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
    for rule in (
        held | {"ray_delay": 1},
        PORT_CORNER | {"ray_delay": 1},
        held | {"momentum_table": {"electron": -1}},
    ):
        with pytest.raises(ValueError, match="removed by loop-binding-v1.*docs/MIGRATION.md"):
            parse_initial_state(document(rule))
    # A rule without outputs that assigns `delay` is a wait, not a hold: the two
    # rays that meet at each corner in the cycle of tick 1 wait one interval at
    # their event Node, are met by nothing there, leave in the cycle of tick 2 on
    # their unchanged headings, off the square, and reach the board's edge at
    # tick 7: no group, no re-firing, every line exact.
    world = Simulation(parse_initial_state(document(held, ticks=8)))
    for tick in range(1, 8):
        world.step()
        assert balanced(world)
        if tick == 2:
            assert all(
                r.steps == 0 and r.interaction_delay == 0 for p in CORNERS for r in rays_at(world, p)
            )
        if tick >= 3:
            assert state(world) == {position: [] for position in CORNERS}
    assert ledger(world) == ((8,), ZERO, (0,), -24, True)
    assert sorted(n.position for n in world.inventory_view().nodes if n.rays and any(n.rays)) == [
        (0, 5, 5),
        (0, 6, 5),
        (5, 0, 5),
        (5, 11, 5),
        (6, 0, 5),
        (6, 11, 5),
        (11, 5, 5),
        (11, 6, 5),
    ]
