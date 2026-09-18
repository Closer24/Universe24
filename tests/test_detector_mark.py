"""Node Detector bit (detector-mark-v1): one bit per arriving thing at a marked Node.

Expected bits are pinned in docs/TEST_EXPECTATIONS.md ("Node Detector bit")
before the first run: six lamps one Link from one marked Node with setting 1/2,
six arrivals in one interval, clicks on 1 only, the rays that drew 0 returned
to their lamps (detector-return-v1) and restored to them by the inverse split of
a one-line event (inverse-split-v1), and the unmarked control world equal on
totals and momentum at every tick and on the lamps until the restore.

Re-pinned on 2026-09-18 under the law of the bit (bit-law-v1, point 14: there
is no lottery): the mark's setting is its counter table, the k-th arrival
catching the bit 1 when k mod 2 < 1, so the bits are (1, 0, 1, 0, 1, 0) in
Port order and the counter stands at 6; the seed is retired; the mark declares
`on_click: "pass"` so that a thing that draws 1 walks on as before (absorb is
the default for every family); a click and a return name the thing's owner.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.spatial_state import (
    BIT_THING,
    CLICK_PASS,
    DETECTOR_MARK,
    DetectorMark,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

CENTER = (7, 7, 7)
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# The counter at setting 1/2 (bit-law-v1, point 14), in the order of the marked
# Node's Ports the six rays come in through: the k-th arrival draws 1 when k mod 2 < 1.
PINNED_BITS = (1, 0, 1, 0, 1, 0)
# Nine arrivals by tick 3: the six of tick 1 and the three merged pairs that turn
# back to the mark (lanes-v1, 2026-09-18).
FINAL_TICKET = 9
# Re-pinned on 2026-09-18 with feature 18 (lanes-v1, Highlights 5.4 point 25, the
# model owner's decision on its open case): a returned ray and the passing ray of
# the opposite lamp are given one lane at the mark, so they are one real ray with
# the passing ray's record, the amounts added and the momentum added exactly as the
# ledger reads it (a returned ray reads its event's momentum), which reaches the
# content: after tick 2 the pairs of 3 (-X), 7 (-Y) and 11 (-Z) sit one Link from
# C carrying (4, 0, 0), (0, 8, 0) and (0, 0, 12), and at their departure of tick 3
# each turns back to C, spending 3, 7 and 11 on the momentum field's line: after
# tick 3 the pair of 3 passed C on +X (the seventh arrival), the pair of 7 was
# returned on -Y (the eighth) and the pair of 11 passed on +Z (the ninth).
MERGED_AFTER_2 = sorted(
    [((6, 7, 7), 1, 3, 2, 0, 1, 1), ((7, 6, 7), 3, 7, 2, 0, 1, 1), ((7, 7, 6), 5, 11, 2, 0, 1, 1)]
)
MERGED_AFTER_3 = sorted(
    [((7, 7, 7), 0, 3, 3, 0, 1, 1), ((7, 7, 7), 3, 7, 3, 0, 0, 1), ((7, 7, 7), 4, 11, 3, 0, 1, 1)]
)


def unit(port):
    return tuple(HEADINGS[port])


def lamp_position(port):
    """The lamp one Link out on the side of Port p, aimed back at the marked Node."""
    return tuple(c + u for c, u in zip(CENTER, unit(port), strict=True))


def document(marked=True, ticks=3):
    raw = {
        "schema_version": 1,
        "model_id": "detector-mark-test-v1",
        "shape": [15, 15, 15],
        "boundary": "periodic",
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
        # Lamp p holds exactly the amount it emits, p + 1, so it fires once at tick 0.
        "disturbance_types": [
            {
                "name": f"lamp_{port}",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": port + 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for port in range(6)
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
                "kerengonen": {"phase_steps": 8},
            }
        ],
        "emissions": [
            {
                "type": f"lamp_{port}",
                "field": "quanta",
                "amount": port + 1,
                "denominator": 1,
                "heading": HEADINGS[port ^ 1],
                "kerengonen_phase": 0,
            }
            for port in range(6)
        ],
        "seeds": [{"position": list(lamp_position(port)), "type": f"lamp_{port}"} for port in range(6)],
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
        raw["detectors"] = [{"position": list(CENTER), "setting": [1, 2], "on_click": "pass"}]
    return raw


def rays_at(world, position):
    node = next(n for n in world.inventory_view().nodes if n.position == position)
    return node.rays[0] if node.rays else ()


def ray_inventory(world):
    """Every ray in the world: Node, heading, amount, steps, phase, outbound and bit."""
    return sorted(
        (
            node.position,
            ray.heading,
            ray.amount,
            ray.steps,
            ray.phase,
            ray.outbound,
            ray.detector,
        )
        for node in world.inventory_view().nodes
        for rays in node.rays
        for ray in rays
    )


def continuing(port, tick, bit):
    """The ray of Port p that continues: t - 1 Links beyond C after tick t. Its
    phase stays 0: the family declares no clock (clock-readings-v1, 2026-09-18;
    the rate 1 of the family was retired with the per-family rest rate)."""
    return (
        tuple(c - (tick - 1) * u for c, u in zip(CENTER, unit(port), strict=True)),
        port ^ 1,
        port + 1,
        tick,
        0,
        1,
        bit,
    )


def returned(port, tick):
    """The ray of Port p that drew 0: reversed at C at tick 1, at its lamp at tick 2 and
    restored to it by the inverse split of its one-line event from tick 3."""
    if tick == 1:
        return (CENTER, port, port + 1, 1, 0, 0, BIT_THING)
    if tick == 2:
        return (lamp_position(port), port, port + 1, 0, 0, 0, BIT_THING)
    return None


def lamp(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


def observed(world):
    """What the marked and the control world must agree on: totals, audit and lamps."""
    report = world.conservation_report()
    assert report["status"] == "passed"
    assert all(item["balanced"] for item in world.spatial_accounting().values())
    return (
        world.totals(),
        report["current"]["energy"],
        tuple(report["current"]["momentum"]),
        [lamp(world, port) for port in range(6)],
    )


def without_ray_field(raw):
    for key in ("spatial_fields", "emissions", "conservation"):
        del raw[key]


def test_a_marked_node_draws_one_bit_per_arriving_ray(tmp_path, monkeypatch):
    initial = parse_initial_state(document())
    assert initial.detectors == (DetectorMark(CENTER, 1, 2, on_click=(CLICK_PASS,), click_keys=1),)
    # (c) The control world has no mark and steps a counter nowhere.
    control_clicks = []
    control_trace = []
    with monkeypatch.context() as patched:

        def forbidden(*args):
            pytest.fail("an unmarked Node stepped a counter")

        patched.setattr("event_universe.core.spatial_state.ticket_bit", forbidden)
        control = Simulation(
            parse_initial_state(document(marked=False)),
            observer=lambda event: (
                control_clicks.append(event) if event["event"] == "detector_click" else None
            ),
        )
        for tick in range(1, 4):
            control.step()
            control_trace.append(observed(control))
            # The control's six rays all continue, unmarked.
            assert ray_inventory(control) == sorted(
                continuing(port, tick, BIT_THING) for port in range(6)
            )
        assert all(node.detector is None for node in control._spatial.nodes.values())
    assert control_clicks == []
    clicks = []
    returns = []
    splits = []
    world = Simulation(
        initial,
        observer=lambda event: (
            clicks.append(event)
            if event["event"] == "detector_click"
            else returns.append(event)
            if event["event"] == "detector_return"
            else splits.append(event)
            if event["event"] == "inverse_split"
            else None
        ),
    )
    # Three ticks: at the fourth the restored lamps would emit again into the mark.
    for tick in range(1, 4):
        world.step()
        # (c) Totals and audited energy and momentum equal the control's at every
        # tick, and the lamps until the restore; a returned ray's momentum reads as
        # its share on the event's heading, and from tick 3 the lamps of the rays
        # that drew 0 hold their share again with its recoil undone (inverse-split-v1).
        totals, energy, momentum, lamps = observed(world)
        # lanes-v1 (2026-09-18): the merged pairs turn back at tick 3, spending
        # (3, 7, 11) on the momentum field's line, so the rays' momentum differs
        # from the control's by that; nothing is ever restored to a lamp.
        assert (tick < 3) == ((totals, energy, momentum) == control_trace[tick - 1][:3])
        assert world.totals() == {"quanta": (21,), "momentum": (0, 0, 0) if tick < 3 else (3, 7, 11)}
        for port in range(6):
            assert lamp(world, port) == {
                "quanta": (0,),
                "momentum": tuple(u * (port + 1) for u in unit(port)),
            }
        assert lamps == ([lamp(world, port) for port in range(6)]) == control_trace[tick - 1][3]
        # (a), (b) The ray that came in through Port p and drew 1 leaves through the
        # opposite side with its bit and is t - 1 Links beyond the marked Node after
        # tick t; the ray that drew 0 is reversed at the marked Node in its arrival
        # interval, is at its lamp's Node at tick 2 (detector-return-v1) and is
        # restored to the lamp from tick 3 (inverse-split-v1).
        if tick == 1:
            assert ray_inventory(world) == sorted(
                continuing(port, tick, BIT_THING) if bit else returned(port, tick)
                for port, bit in enumerate(PINNED_BITS)
            )
        else:
            assert ray_inventory(world) == (MERGED_AFTER_2 if tick == 2 else MERGED_AFTER_3)
        if tick == 1:
            assert world.spatial_values(CENTER)["quanta"]["ray_count"] == 6
            for ray in rays_at(world, CENTER):
                origin = ray.heading if ray.outbound else ray.heading ^ 1
                assert ray.event_ports == 1 << origin and ray.accumulators == (0, 0, 0)
                assert ray.event_shares == tuple(ray.amount if p == origin else 0 for p in range(6))
        if tick == 2:
            # A passing ray and the returned ray given its lane are one real ray
            # (lanes-v1, 2026-09-18), with both owners.
            assert world.spatial_values((7, 6, 7))["quanta"]["ray_count"] == 1
            assert world.spatial_values((7, 7, 6))["quanta"]["ray_count"] == 1
            merged = [ray for ray in rays_at(world, (7, 6, 7)) if ray.owners]
            assert [(ray.amount, ray.owner, ray.owners, ray.momentum) for ray in merged] == [
                (7, 3, (4,), (0, 8, 0))
            ]
    # (a) Exactly the arrivals that drew 1 clicked, at tick 1, in Port order, the
    # arrivals that drew 0 were returned, in Port order, and the mark's counter
    # stands at six after six arrivals; lamp p is thing p + 1.
    assert clicks == [
        {
            "event": "detector_click",
            "tick": 1,
            "position": CENTER,
            "port": port,
            "family": "quanta",
            "amount": port + 1,
            "bit": 1,
            "owner": port + 1,
        }
        for port, bit in enumerate(PINNED_BITS)
        if bit
    ] + [
        # The merged pairs of 3 and 11 back at C after tick 3 (lanes-v1).
        {
            "event": "detector_click",
            "tick": 3,
            "position": CENTER,
            "port": port,
            "family": "quanta",
            "amount": amount,
            "bit": 1,
            "owner": owner,
        }
        for port, amount, owner in ((1, 3, 1), (5, 11, 5))
    ]
    assert returns == [
        {
            "event": "detector_return",
            "tick": 1,
            "position": CENTER,
            "port": port,
            "family": "quanta",
            "amount": port + 1,
            "owner": port + 1,
        }
        for port, bit in enumerate(PINNED_BITS)
        if not bit
    ] + [
        # The merged pair of 7 back at C after tick 3, the eighth arrival (lanes-v1).
        {
            "event": "detector_return",
            "tick": 3,
            "position": CENTER,
            "port": 3,
            "family": "quanta",
            "amount": 7,
            "owner": 3,
        }
    ]
    # No returned ray reaches its lamp: each joined the passing ray of the opposite
    # lamp on its lane (lanes-v1, 2026-09-18), so no inverse split happens.
    assert splits == []
    node = world._spatial.nodes[CENTER]
    assert node.detector == initial.detectors[0] and node.detector_ticket == FINAL_TICKET
    # (d) A replay writes the same events and the same run record, and redraws nothing.
    path = tmp_path / "marked.json"
    path.write_text(json.dumps(document()), encoding="utf-8")
    records = []
    for name in ("first", "second"):
        run_initialization(path, tmp_path / name, ticks=3)
        events = (tmp_path / name / "events.jsonl").read_text(encoding="utf-8")
        metadata = json.loads((tmp_path / name / "run.json").read_text(encoding="utf-8"))
        metadata.pop("elapsed_seconds")
        records.append((events, metadata))
    (first_events, first_run), (second_events, second_run) = records
    assert first_events == second_events and first_run == second_run
    recorded = [json.loads(line) for line in first_events.splitlines()]
    assert [event for event in recorded if event["event"] == "detector_click"] == [
        {**click, "position": list(CENTER)} for click in clicks
    ]
    assert [event for event in recorded if event["event"] == "detector_return"] == [
        {**event, "position": list(CENTER)} for event in returns
    ]
    assert first_run["detector_mark"] == DETECTOR_MARK == "detector-mark-v1"
    assert first_run["detector_return"] == "detector-return-v1"
    assert first_run["ray_state"] == "ray-event-state-v1"
    assert first_run["conserved_at_every_completed_tick"] and first_run["final_totals"]["quanta"] == [21]
    # (e) A mark without a setting, a setting outside 0 through 1, a negative seed
    # (the key is accepted, never read), a duplicate or outside position and a
    # world without an admitted ray field are rejected before any world exists.
    for edit, message in (
        (lambda raw: raw["detectors"][0].pop("setting"), "missing keys: setting"),
        (lambda raw: raw["detectors"][0].update(setting=[3, 2]), "from 0 through 1"),
        (lambda raw: raw["detectors"][0].update(setting=[1, 0]), "denominator"),
        (lambda raw: raw["detectors"][0].update(setting=[-1, 2]), "numerator"),
        (lambda raw: raw["detectors"][0].update(seed=-1), "detector.seed"),
        (lambda raw: raw["detectors"][0].update(rate=1), "unknown keys: rate"),
        (lambda raw: raw["detectors"].append(dict(raw["detectors"][0])), "one Detector mark"),
        (lambda raw: raw["detectors"][0].update(position=[15, 7, 7]), "within shape"),
        (lambda raw: raw["spatial_fields"][0].update(metric="euclidean"), "unit-axial"),
        (without_ray_field, "a ray field"),
    ):
        raw = document()
        edit(raw)
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
        assert not validate_configuration(json.dumps(raw)).valid
