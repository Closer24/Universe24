"""Detector return (detector-return-v1): a draw of 0 returns the ray on its own line.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Detector return")
before the first run: one world per unit-axial heading, a lamp three Links
before a marked Node with setting 1/2 and seed 3 (one draw, bit 0), a sail one
Link before it absorbing half of what passes outbound, and the exact tick table
of the one ray from emission through the return to steps 0 at its event Node,
where the inverse split of a one-line event restores it to the lamp
(inverse-split-v1).
"""

import json

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import pack
from event_universe.core.spatial_state import (
    DETECTOR_BIT_0,
    DETECTOR_NONE,
    DETECTOR_RETURN,
    Ray,
    SpatialPacket,
    ray_momentum,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

MARK = (7, 7, 7)
SEED = 3
AMOUNT = 8
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# The one draw of the world, seed 3 at setting 1/2: the first draw of the mark test.
TICKET_AFTER_DRAW = 144814
# After tick t: Links from the lamp, heading index offset (0 the emitted heading, 1 its
# negation), amount, steps, outbound, phase, Detector bit, the share of the ray's event.
TICK_TABLE = {
    1: (1, 0, 8, 1, 1, 1, DETECTOR_NONE, 8),
    2: (2, 0, 8, 2, 1, 2, DETECTOR_NONE, 8),
    3: (3, 1, 4, 3, 0, 3, DETECTOR_BIT_0, 8),
    4: (2, 1, 4, 2, 0, 2, DETECTOR_BIT_0, 8),
    5: (1, 1, 4, 1, 0, 1, DETECTOR_BIT_0, 8),
    6: (0, 1, 4, 0, 0, 0, DETECTOR_BIT_0, 8),
    # The inverse split of a one-line event: no sibling line, the share restored to
    # the lamp in the cycle after its arrival (inverse-split-v1); the lamp, a source
    # that emits what it holds, then emits the 4 again as a new one-line event on
    # the cycle after the restored record reaches the field plan.
    7: None,
    8: (1, 0, 4, 1, 1, 1, DETECTOR_NONE, 4),
}


def unit(port):
    return tuple(HEADINGS[port])


def along(port, links):
    """The Node `links` Links from the lamp toward the marked Node, on the line of Port p."""
    return tuple(m + (links - 3) * u for m, u in zip(MARK, unit(port), strict=True))


def scaled(port, factor):
    return tuple(factor * u for u in unit(port))


def document(port, marked=True, boundary="periodic", ticks=8):
    raw = {
        "schema_version": 1,
        "model_id": "detector-return-test-v1",
        "shape": [15, 15, 15],
        "boundary": boundary,
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
                "name": "quanta",
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
        # The lamp holds exactly the amount it emits, so it fires once at tick 0.
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": AMOUNT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "sail",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 6,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8, "phase_advance": 1},
            }
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "quanta",
                "amount": AMOUNT,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": HEADINGS[port],
                "kerengonen_phase": 0,
            }
        ],
        # The coupling partner one Link before the mark: half of every outbound ray.
        "spatial_couplings": [
            {
                "name": "sail_absorbs",
                "type": "sail",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "fraction": 1,
                "fraction_denominator": 2,
            }
        ],
        "seeds": [
            {"position": list(along(port, 0)), "type": "lamp"},
            {"position": list(along(port, 2)), "type": "sail"},
        ],
        "conservation": {
            "name": "quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["quanta", "momentum"],
                    "energy": {"field": "quanta"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "quanta", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }
    if marked:
        raw["detectors"] = [{"position": list(MARK), "setting": [1, 2], "seed": SEED}]
    return raw


def rays_in(world):
    """Every ray in the world with its Node."""
    return [
        (node.position, ray)
        for node in world.inventory_view().nodes
        for rays in node.rays
        for ray in rays
    ]


def record(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


@pytest.mark.parametrize("port", range(6))
def test_a_draw_of_zero_returns_the_ray_to_its_event_node(port, tmp_path):
    initial = parse_initial_state(document(port))
    definition = initial.spatial_fields[0]
    events = []
    world = Simulation(
        initial,
        observer=lambda event: (
            events.append(event)
            if event["event"].startswith("detector_") or event["event"] == "inverse_split"
            else None
        ),
    )
    for tick in range(1, 9):
        world.step()
        # (a) The one ray of the world follows the pinned tick table: out to the mark,
        # reversed there on its line in the arrival interval, back one Link per tick
        # with steps and phase counting down, at its event Node at tick 6, restored
        # to the lamp by the inverse split and emitted again as a new event from
        # tick 7.
        entry = TICK_TABLE[tick]
        links, reversed_, amount, steps, outbound, phase, bit, share = entry or (0,) * 8
        assert rays_in(world) == (
            []
            if entry is None
            else [
                (
                    along(port, links),
                    Ray(
                        port ^ reversed_,
                        (0, 0, 0),
                        amount,
                        phase=phase,
                        advance=-1,
                        wait=0,
                        interaction_delay=0,
                        steps=steps,
                        outbound=outbound,
                        event_ports=1 << port,
                        event_shares=tuple(share if p == port else 0 for p in range(6)),
                        detector=bit,
                    ),
                )
            ]
        )
        # (b) The sail took half of the outbound ray and nothing of the returning one;
        # the lamp recoiled once; totals and the audits are exact at every tick, the
        # returning ray's momentum reading as its share on the event's heading.
        absorbed = 4 if tick >= 3 else 0
        assert record(world, 1) == {"quanta": (absorbed,), "momentum": scaled(port, absorbed)}
        # The lamp recoiled once for 8, holds the 4 back with its recoil undone after
        # tick 7 and recoiled again for the 4 it emitted anew from tick 8.
        held = 4 if tick == 7 else 0
        assert record(world, 0) == {"quanta": (held,), "momentum": scaled(port, -AMOUNT + held)}
        assert world.totals() == {"quanta": (AMOUNT,), "momentum": (0, 0, 0)}
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        in_flight = [0, 0, 0]
        for node in world.inventory_view().nodes:
            for rays in node.rays:
                for axis, value in enumerate(ray_momentum(rays, definition)):
                    in_flight[axis] += value
        assert tuple(in_flight) == scaled(port, AMOUNT - absorbed - held)
        if tick == 3:
            assert world.spatial_values(MARK)["quanta"]["ray_count"] == 1
        if tick == 4:
            assert world.spatial_values(along(port, 2))["quanta"]["ray_count"] == 1
    # (c) No click, one return: at tick 3, through the Port the ray came in by; one
    # inverse split at the lamp in the cycle labelled 6, to no sibling line.
    assert events == [
        {
            "event": "detector_return",
            "tick": 3,
            "position": MARK,
            "port": port ^ 1,
            "family": "quanta",
            "amount": 4,
        },
        {
            "event": "inverse_split",
            "tick": 6,
            "position": along(port, 0),
            "family": "quanta",
            "mode": "siblings",
            "ports": (),
            "amounts": (),
            "amount": 4,
            "bit": 0,
            "restored": True,
            "annulled": {},
        },
    ]
    assert world._spatial.nodes[MARK].detector_ticket == TICKET_AFTER_DRAW
    # (d) The runner records the identity and replays byte for byte.
    path = tmp_path / "return.json"
    path.write_text(json.dumps(document(port)), encoding="utf-8")
    records = []
    for name in ("first", "second"):
        run_initialization(path, tmp_path / name, ticks=8)
        events_text = (tmp_path / name / "events.jsonl").read_text(encoding="utf-8")
        metadata = json.loads((tmp_path / name / "run.json").read_text(encoding="utf-8"))
        metadata.pop("elapsed_seconds")
        records.append((events_text, metadata))
    (first_events, first_run), (second_events, second_run) = records
    assert first_events == second_events and first_run == second_run
    recorded = [json.loads(line) for line in first_events.splitlines()]
    assert [event for event in recorded if event["event"] == "detector_click"] == []
    assert [event for event in recorded if event["event"] == "detector_return"] == [
        {**events[0], "position": list(MARK)}
    ]
    assert first_run["detector_return"] == DETECTOR_RETURN == "detector-return-v1"
    assert first_run["inverse_split"] == "inverse-split-v1"
    assert first_run["detector_mark"] == "detector-mark-v1"
    assert first_run["sampling_profile"] == "detector-only-v1"
    assert first_run["ray_state"] == "ray-event-state-v1"
    assert first_run["conserved_at_every_completed_tick"]
    assert first_run["final_totals"] == {"quanta": [AMOUNT], "momentum": [0, 0, 0]}
    # (e) On an open boundary a returning ray that would escape has no event Node
    # in the world: the engine fails closed instead of recording an escape.
    open_world = Simulation(parse_initial_state(document(port, boundary="open")))
    edge = tuple(14 if u > 0 else 0 if u < 0 else 7 for u in unit(port))
    returning = Ray(port, (0, 0, 0), 4, steps=1, outbound=0, event_ports=1 << port)
    packet = SpatialPacket(1, edge, port, ((pack((0,)),) * 8,), rays=((returning,),))
    with pytest.raises(ValueError, match="event Node"):
        open_world._spatial._escape(packet, 1)
    assert open_world.escaped_totals() == {"quanta": (0,), "momentum": (0, 0, 0)}
