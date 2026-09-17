"""Node Detector bit (detector-mark-v1): one unsalted draw per arriving ray at a marked Node.

Expected bits are pinned in docs/TEST_EXPECTATIONS.md ("Node Detector bit")
before the first run: six lamps one Link from one marked Node with setting 1/2
and seed 3, six arrivals in one interval, bits (0, 0, 0, 1, 1, 0) in Port
order, clicks on 1 only, and the unmarked control world equal at every tick.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.spatial_state import (
    DETECTOR_BIT_0,
    DETECTOR_BIT_1,
    DETECTOR_MARK,
    DETECTOR_NONE,
    TICKET_MODULUS,
    DetectorMark,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

CENTER = (7, 7, 7)
SEED = 3
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# Pinned from the published ticket rule for seed 3 at setting 1/2, in the order of
# the marked Node's Ports the six rays come in through.
PINNED_BITS = (0, 0, 0, 1, 1, 0)
FINAL_TICKET = 71969709


def unit(port):
    return tuple(HEADINGS[port])


def lamp_position(port):
    """The lamp one Link out on the side of Port p, aimed back at the marked Node."""
    return tuple(c + u for c, u in zip(CENTER, unit(port), strict=True))


def document(marked=True, ticks=4):
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
                "kerengonen": {"phase_steps": 8, "phase_advance": 1},
            }
        ],
        "emissions": [
            {
                "type": f"lamp_{port}",
                "field": "quanta",
                "amount": port + 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
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
        raw["detectors"] = [{"position": list(CENTER), "setting": [1, 2], "seed": SEED}]
    return raw


def rays_at(world, position):
    node = next(n for n in world.inventory_view().nodes if n.position == position)
    return node.rays[0] if node.rays else ()


def ray_inventory(world):
    """Every ray in the world: Node, heading, amount, steps, phase and Detector bit."""
    return sorted(
        (node.position, ray.heading, ray.amount, ray.steps, ray.phase, ray.detector)
        for node in world.inventory_view().nodes
        for rays in node.rays
        for ray in rays
    )


def lamp(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


def observed(world):
    """What the marked and the control world must agree on: totals, audit, lamps, rays."""
    report = world.conservation_report()
    assert report["status"] == "passed"
    assert all(item["balanced"] for item in world.spatial_accounting().values())
    return (
        world.totals(),
        report["current"]["energy"],
        tuple(report["current"]["momentum"]),
        [lamp(world, port) for port in range(6)],
        [ray[:5] for ray in ray_inventory(world)],
    )


def without_ray_field(raw):
    for key in ("spatial_fields", "emissions", "conservation"):
        del raw[key]


def test_a_marked_node_draws_one_bit_per_arriving_ray(tmp_path, monkeypatch):
    initial = parse_initial_state(document())
    assert initial.detectors == (DetectorMark(CENTER, 1, 2, SEED),)
    # (c) The control world has no mark and calls the ticket rule nowhere.
    control_clicks = []
    control_trace = []
    with monkeypatch.context() as patched:

        def forbidden(*args):
            pytest.fail("an unmarked Node consumed a ticket")

        patched.setattr("event_universe.core.spatial_state.next_ticket", forbidden)
        control = Simulation(
            parse_initial_state(document(marked=False)),
            observer=lambda event: (
                control_clicks.append(event) if event["event"] == "detector_click" else None
            ),
        )
        for _ in range(4):
            control.step()
            control_trace.append(observed(control))
            assert all(ray[5] == DETECTOR_NONE for ray in ray_inventory(control))
        assert all(node.detector is None for node in control._spatial.nodes.values())
    assert control_clicks == []
    clicks = []
    world = Simulation(
        initial,
        observer=lambda event: clicks.append(event) if event["event"] == "detector_click" else None,
    )
    for tick in range(1, 5):
        world.step()
        # (c) Totals, audited energy and momentum, the lamps and every ray's position,
        # heading, amount, steps and phase equal the control's at every tick.
        assert observed(world) == control_trace[tick - 1]
        assert world.totals() == {"quanta": (21,), "momentum": (0, 0, 0)}
        for port in range(6):
            assert lamp(world, port) == {
                "quanta": (0,),
                "momentum": tuple(u * (port + 1) for u in unit(port)),
            }
        # (a), (b) The ray that came in through Port p leaves through the opposite
        # side with its bit and is t - 1 Links beyond the marked Node after tick t.
        assert ray_inventory(world) == sorted(
            (
                tuple(c - (tick - 1) * u for c, u in zip(CENTER, unit(port), strict=True)),
                port ^ 1,
                port + 1,
                tick,
                tick,
                DETECTOR_BIT_1 if bit else DETECTOR_BIT_0,
            )
            for port, bit in enumerate(PINNED_BITS)
        )
        if tick == 1:
            assert world.spatial_values(CENTER)["quanta"]["ray_count"] == 6
            for ray in rays_at(world, CENTER):
                assert ray.outbound == 1 and ray.event_ports == 1 << ray.heading
                assert ray.event_shares == tuple(ray.amount if p == ray.heading else 0 for p in range(6))
    # (a) Exactly the arrivals that drew 1 clicked, at tick 1, in Port order, and the
    # mark's stream stands where the published rule leaves it after six draws.
    assert clicks == [
        {
            "event": "detector_click",
            "tick": 1,
            "position": CENTER,
            "port": port,
            "family": "quanta",
            "amount": port + 1,
            "bit": 1,
        }
        for port, bit in enumerate(PINNED_BITS)
        if bit
    ]
    node = world._spatial.nodes[CENTER]
    assert node.detector == initial.detectors[0] and node.detector_ticket == FINAL_TICKET
    # (d) A replay writes the same events and the same run record, and redraws nothing.
    path = tmp_path / "marked.json"
    path.write_text(json.dumps(document()), encoding="utf-8")
    records = []
    for name in ("first", "second"):
        run_initialization(path, tmp_path / name, ticks=4)
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
    assert first_run["detector_mark"] == DETECTOR_MARK == "detector-mark-v1"
    assert first_run["sampling_profile"] == "detector-only-v1"
    assert first_run["ray_state"] == "ray-event-state-v1"
    assert first_run["conserved_at_every_completed_tick"] and first_run["final_totals"]["quanta"] == [21]
    # (e) A mark without a setting, a setting outside 0 through 1, a seed at the
    # modulus, a duplicate or outside position and a world without an admitted ray
    # field are rejected before any world exists.
    for edit, message in (
        (lambda raw: raw["detectors"][0].pop("setting"), "missing keys: setting"),
        (lambda raw: raw["detectors"][0].update(setting=[3, 2]), "from 0 through 1"),
        (lambda raw: raw["detectors"][0].update(setting=[1, 0]), "denominator"),
        (lambda raw: raw["detectors"][0].update(setting=[-1, 2]), "numerator"),
        (lambda raw: raw["detectors"][0].update(seed=TICKET_MODULUS), "ticket modulus"),
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
