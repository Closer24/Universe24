"""The Detector's bit as a property of the ray (detector-bit-property-v1).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Detector bit as a
property") before the first run, from the published ticket rule: (a) a ray
realized at mark A (setting 1/1) reaches mark B (setting 1/2, seed 3), which by
default passes it without a draw and records a `detector_pass`, and under
`on_bit_1: "draw"` draws it (bit 0, the ray returned); (b) on a pair line, the
ray returned by mark A (setting 0/1) walks back through its source's mark C
undrawn, and the transmission of its inverse split, carrying bit 0, passes mark
D (setting 1/1) without a draw, or is drawn under `on_bit_0: "draw"`; (c) a
realized ray meets an unmarked ray in a declared outputs rule and both outputs
carry the bit, none under `bit: "none"`, an input's under `bit: {"of": i}`;
(d) a `when` guard on `detector` equal to 2 fires a rule for a realized ray
only; (e) the keys are validated and the helpers are exact.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.spatial_state import (
    BIT_HIGHEST,
    BIT_NONE,
    DETECTOR_BIT_0,
    DETECTOR_BIT_1,
    DETECTOR_BIT_PROPERTY,
    DETECTOR_NONE,
    DetectorMark,
    inherited_bit,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# Ticket states after one draw from seed 3 (setting 1/2 draws 0, as in the mark test),
# from seed 0 (setting 1/1 draws 1) and from seed 5 (setting 1/1 draws 1), and after a
# second draw from seed 5.
SEED_3_ONCE = 144814
SEED_0_ONCE = 1
SEED_5_ONCE = 241356
SEED_5_TWICE = 913077587


def ray_field(participant, name):
    return {"field": name, "participant": participant}


def document(lamps, detectors, rules=(), ticks=6, rays_per_tick=1):
    """A board under the shared Detector admission: lamps holding exactly what they emit
    once at tick 0 (a directed emission per heading, or a sweep of `rays_per_tick`
    headings when the heading is None), the marks, and the declared couplings."""
    return {
        "schema_version": 1,
        "model_id": "detector-bit-property-test-v1",
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
        "disturbance_types": [
            {
                "name": name,
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": amount, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for name, _, amount, _ in lamps
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": rays_per_tick,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8, "phase_advance": 1},
            }
        ],
        "emissions": [
            {
                "type": name,
                "field": "quanta",
                "amount": amount,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": 0,
            }
            | ({} if heading is None else {"heading": HEADINGS[heading]})
            for name, _, amount, heading in lamps
        ],
        "seeds": [{"position": list(position), "type": name} for name, position, _, _ in lamps],
        "detectors": [dict(mark) for mark in detectors],
        "ray_interactions": list(rules),
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


def mark(position, setting, seed, **couplings):
    return {"position": list(position), "setting": list(setting), "seed": seed} | couplings


def meeting(outputs, when=None, **keys):
    """Two quanta rays meet; the outputs leave on +Y and -Y with the inputs' amounts."""
    rule = {
        "name": "meeting",
        "participants": [{"type": "quanta"}, {"type": "quanta"}],
        "outputs": outputs,
        "invariants": [
            {"name": "energy", "expression": {"field": "amount"}},
            {
                "name": "momentum",
                "expression": {"op": "mul", "args": [{"field": "amount"}, {"field": "heading"}]},
            },
        ],
    }
    if when is not None:
        rule["when"] = when
    return rule | keys


TO_Y = [
    {"field": "quanta", "amount": {"of": 0}, "heading": 2},
    {"field": "quanta", "amount": {"of": 1}, "heading": 3, "input": 1},
]


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


def ticket(world, position):
    """The mark's ticket state: its seed until a ray first reaches its Node, which is
    when the engine creates the Node."""
    node = world._spatial.nodes.get(position)
    if node is None:
        return next(m.seed for m in world.initial.detectors if m.position == position)
    return node.detector_ticket


def observe(initial):
    """A world with the Detector and inverse-split events collected in stream order."""
    events = []
    world = Simulation(
        initial,
        observer=lambda event: (
            events.append(event)
            if event["event"] in ("detector_click", "detector_pass", "detector_return", "inverse_split")
            else None
        ),
    )
    return world, events


def event(kind, tick, position, **detail):
    return {"event": kind, "tick": tick, "position": position} | detail


def recorded(tmp_path, raw, ticks):
    path = tmp_path / "world.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=ticks)
    lines = (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    return [json.loads(line) for line in lines], metadata


@pytest.mark.parametrize("second", ["default", "pass", "draw"])
def test_a_marked_node_reads_the_bit_of_a_realized_ray(tmp_path, second):
    # (a) A lamp at (4,7,7) sends 8 quanta along +X: mark A at (5,7,7), setting 1/1,
    # realizes the ray at tick 1 (one draw from seed 0, a click, bit 1); mark B at
    # (9,7,7), setting 1/2 and seed 3, receives it at tick 5 carrying that bit.
    A, B = (5, 7, 7), (9, 7, 7)
    couplings = {} if second == "default" else {"on_bit_1": second}
    raw = document(
        [("lamp", (4, 7, 7), 8, 0)],
        [mark(A, (1, 1), 0), mark(B, (1, 2), 3, **couplings)],
    )
    initial = parse_initial_state(raw)
    assert initial.detectors[1].bit_keys == int(second != "default")
    world, events = observe(initial)
    for tick in range(1, 7):
        world.step()
        assert world.totals() == {"quanta": (8,), "momentum": (0, 0, 0)}
        assert world.conservation_report()["status"] == "passed"
        assert ticket(world, A) == SEED_0_ONCE
        if second == "draw" and tick >= 5:
            # B draws the realized ray again, seed 3 at 1/2 drawing 0: the ray is
            # returned with bit 0 and walks back from B, one Link per tick.
            assert ticket(world, B) == SEED_3_ONCE
            assert ray_inventory(world) == [
                ((14 - tick, 7, 7), 1, 8, 10 - tick, 10 - tick, 0, DETECTOR_BIT_0)
            ]
        else:
            # The ray continues realized; B's stream stands at its seed: no draw.
            assert ticket(world, B) == 3
            assert ray_inventory(world) == [((4 + tick, 7, 7), 0, 8, tick, tick, 1, DETECTOR_BIT_1)]
    click = event("detector_click", 1, A, port=1, family="quanta", amount=8, bit=1)
    if second == "draw":
        second_event = event("detector_return", 5, B, port=1, family="quanta", amount=8)
    else:
        second_event = event("detector_pass", 5, B, port=1, family="quanta", amount=8, bit=1)
    assert events == [click, second_event]
    # The runner writes the same events and records the identity only where the
    # world declares a key of the rule; a world on the defaults is recorded as before.
    lines, metadata = recorded(tmp_path, raw, 6)
    assert [line for line in lines if line["event"].startswith("detector_")] == [
        {**click, "position": list(A)},
        {**second_event, "position": list(B)},
    ]
    assert metadata.get("detector_bit_property") == (
        None if second == "default" else DETECTOR_BIT_PROPERTY
    )
    assert DETECTOR_BIT_PROPERTY == "detector-bit-property-v1"
    assert metadata["conserved_at_every_completed_tick"] and metadata["final_totals"]["quanta"] == [8]


@pytest.mark.parametrize("fourth", ["default", "draw"])
def test_a_returning_ray_and_a_transmission_are_never_drawn_by_default(fourth):
    # (b) A pair lamp at X = (7,7,7), itself mark C (setting 1/1, seed 7: a source is
    # a Detector), sends 4 quanta each way on the X line. Mark A at (10,7,7), setting
    # 0/1 and seed 3, returns arm A at tick 3; mark D at (4,7,7), setting 1/1 and
    # seed 5, realizes arm B at tick 3. Arm A walks back through C undrawn, its
    # inverse split in the cycle labelled 6 transmits 4 on arm B's line with bit 0,
    # and the transmission reaches D at tick 9 carrying that bit.
    X, A, D = (7, 7, 7), (10, 7, 7), (4, 7, 7)
    couplings = {} if fourth == "default" else {"on_bit_0": fourth}
    raw = document(
        [("lamp", X, 8, None)],
        [mark(X, (1, 1), 7), mark(A, (0, 1), 3), mark(D, (1, 1), 5, **couplings)],
        ticks=10,
        rays_per_tick=2,
    )
    world, events = observe(parse_initial_state(raw))
    for tick in range(1, 11):
        world.step()
        assert world.totals() == {"quanta": (8,), "momentum": (0, 0, 0)}
        assert world.conservation_report()["status"] == "passed"
        # C draws nothing: not what its lamp emits, not the ray returning to its event
        # Node, not the transmission that leaves it.
        assert ticket(world, X) == 7
        assert ticket(world, A) == (SEED_3_ONCE if tick >= 3 else 3)
        drawn_twice = fourth == "draw" and tick >= 9
        assert ticket(world, D) == (SEED_5_TWICE if drawn_twice else SEED_5_ONCE if tick >= 3 else 5)
        arm_b = ((7 - tick) % 15, 7, 7), 1, 4, tick, tick % 8, 1, (DETECTOR_BIT_1 if tick >= 3 else 0)
        if tick <= 2:
            arm_a = ((7 + tick, 7, 7), 0, 4, tick, tick, 1, DETECTOR_NONE)
        elif tick <= 6:
            arm_a = ((13 - tick, 7, 7), 1, 4, 6 - tick, 6 - tick, 0, DETECTOR_BIT_0)
        else:
            bit = DETECTOR_BIT_1 if drawn_twice else DETECTOR_BIT_0
            arm_a = ((13 - tick, 7, 7), 1, 4, tick - 6, tick - 6, 1, bit)
        assert ray_inventory(world) == sorted([arm_a, arm_b])
    at_d = (
        event("detector_click", 9, D, port=0, family="quanta", amount=4, bit=1)
        if fourth == "draw"
        else event("detector_pass", 9, D, port=0, family="quanta", amount=4, bit=0)
    )
    assert events == [
        event("detector_click", 3, D, port=0, family="quanta", amount=4, bit=1),
        event("detector_return", 3, A, port=1, family="quanta", amount=4),
        event(
            "inverse_split",
            6,
            X,
            family="quanta",
            mode="siblings",
            ports=(1,),
            amounts=(4,),
            amount=4,
            bit=0,
            restored=True,
            annulled={},
        ),
        at_d,
    ]


@pytest.mark.parametrize("bit", ["default", "highest", "none", {"of": 0}, {"of": 1}])
def test_the_outputs_of_a_meeting_inherit_the_bit(tmp_path, bit):
    # (c) Lamp 0 at (5,7,7) sends 5 quanta along +X through mark M at (6,7,7), setting
    # 1/1 (realized at tick 1, bit 1); lamp 1 at (9,7,7) sends 5 along -X, unmarked.
    # They meet at (7,7,7) in the cycle labelled 2 and leave as two outputs on +Y and
    # -Y, both carrying the bit the rule says: the highest of the inputs by default.
    M, X = (6, 7, 7), (7, 7, 7)
    keys = {} if bit == "default" else {"bit": bit}
    raw = document(
        [("lamp_0", (5, 7, 7), 5, 0), ("lamp_1", (9, 7, 7), 5, 1)],
        [mark(M, (1, 1), 0)],
        [meeting(TO_Y, **keys)],
        ticks=4,
    )
    initial = parse_initial_state(raw)
    rule = initial.ray_interactions[0]
    assert (rule.bit, rule.bit_declared) == {
        "default": (BIT_HIGHEST, False),
        "highest": (BIT_HIGHEST, True),
        "none": (BIT_NONE, True),
        0: (0, True),
        1: (1, True),
    }[bit["of"] if isinstance(bit, dict) else bit]
    expected = DETECTOR_NONE if bit in ("none", {"of": 1}) else DETECTOR_BIT_1
    world, events = observe(initial)
    for tick in range(1, 5):
        world.step()
        assert world.totals() == {"quanta": (10,), "momentum": (0, 0, 0)}
        assert world.conservation_report()["status"] == "passed"
        if tick == 1:
            assert ray_inventory(world) == [
                (M, 0, 5, 1, 1, 1, DETECTOR_BIT_1),
                ((8, 7, 7), 1, 5, 1, 1, 1, DETECTOR_NONE),
            ]
        elif tick == 2:
            assert ray_inventory(world) == [
                (X, 0, 5, 2, 2, 1, DETECTOR_BIT_1),
                (X, 1, 5, 2, 2, 1, DETECTOR_NONE),
            ]
        else:
            # The outputs: new event rays with steps from the meeting, the source
            # input's phase plus the Links walked, and the inherited bit.
            assert ray_inventory(world) == sorted(
                [
                    ((7, 5 + tick, 7), 2, 5, tick - 2, tick, 1, expected),
                    ((7, 9 - tick, 7), 3, 5, tick - 2, tick, 1, expected),
                ]
            )
            for node in world.inventory_view().nodes:
                for ray in (ray for rays in node.rays for ray in rays):
                    assert ray.event_ports == 12 and ray.event_shares == (0, 0, 5, 5, 0, 0)
    assert events == [event("detector_click", 1, M, port=1, family="quanta", amount=5, bit=1)]
    _, metadata = recorded(tmp_path, raw, 4)
    assert metadata.get("detector_bit_property") == (None if bit == "default" else DETECTOR_BIT_PROPERTY)


@pytest.mark.parametrize("marked", [True, False])
def test_a_guard_on_the_bit_fires_a_rule_for_a_realized_ray_only(marked):
    # (d) The meeting of (c) guarded by the bit: the rule fires when the highest bit
    # among the two rays is 2 (a draw of 1). Without the mark neither ray carries a
    # bit, the guard is false and the rays cross.
    realized = {
        "op": "eq",
        "args": [
            {"op": "max", "args": [ray_field(0, "detector"), ray_field(1, "detector")]},
            DETECTOR_BIT_1,
        ],
    }
    raw = document(
        [("lamp_0", (5, 7, 7), 5, 0), ("lamp_1", (9, 7, 7), 5, 1)],
        [mark((6, 7, 7), (1, 1), 0)] if marked else [],
        [meeting(TO_Y, when=realized)],
        ticks=3,
    )
    world, events = observe(parse_initial_state(raw))
    for _ in range(3):
        world.step()
    if marked:
        assert ray_inventory(world) == [
            ((7, 6, 7), 3, 5, 1, 3, 1, DETECTOR_BIT_1),
            ((7, 8, 7), 2, 5, 1, 3, 1, DETECTOR_BIT_1),
        ]
        assert len(events) == 1
    else:
        assert ray_inventory(world) == [
            ((6, 7, 7), 1, 5, 3, 3, 1, DETECTOR_NONE),
            ((8, 7, 7), 0, 5, 3, 3, 1, DETECTOR_NONE),
        ]
        assert events == []
    assert world.totals() == {"quanta": (10,), "momentum": (0, 0, 0)}


def test_the_keys_are_validated_and_the_helpers_are_exact():
    # (e) The mark's couplings, the rule's bit and the read-only view are checked
    # before a world exists; the inheritance order is 1 over 0 over none.
    lamps = [("lamp_0", (5, 7, 7), 5, 0), ("lamp_1", (9, 7, 7), 5, 1)]
    swap = {
        "name": "swap",
        "participants": [{"type": "quanta"}, {"type": "quanta"}],
        "assignments": [
            {"participant": 0, "field": "detector", "expression": 2},
        ],
        "invariants": [
            {
                "name": "energy",
                "expression": {"op": "add", "args": [ray_field(0, "amount"), ray_field(1, "amount")]},
            }
        ],
    }
    for edit, message in (
        (lambda raw: raw["detectors"][0].update(on_bit_1="maybe"), "on_bit_1 must be pass or draw"),
        (lambda raw: raw["detectors"][0].update(on_bit_0=1), "on_bit_0 must be pass or draw"),
        (lambda raw: raw["ray_interactions"][0].update(bit="sometimes"), "highest, none or"),
        (lambda raw: raw["ray_interactions"][0].update(bit={"of": 2}), "exceeds the declared roles"),
        (lambda raw: raw["ray_interactions"][0].update(bit={"of": -1}), "bit.of"),
        (lambda raw: raw["ray_interactions"].__setitem__(0, swap), "detector are read-only"),
    ):
        raw = document(lamps, [mark((6, 7, 7), (1, 1), 0)], [meeting(TO_Y)])
        edit(raw)
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
        assert not validate_configuration(json.dumps(raw)).valid
    with pytest.raises(ValueError, match="pass or draw"):
        DetectorMark((6, 7, 7), 1, 1, 0, on_bit_1=5)
    assert DetectorMark((6, 7, 7), 1, 1, 0) == DetectorMark((6, 7, 7), 1, 1, 0, 0, 0, 0)
    assert inherited_bit((DETECTOR_NONE, DETECTOR_BIT_1)) == DETECTOR_BIT_1
    assert inherited_bit((DETECTOR_BIT_0, DETECTOR_NONE)) == DETECTOR_BIT_0
    assert inherited_bit((DETECTOR_BIT_1, DETECTOR_BIT_0), BIT_HIGHEST) == DETECTOR_BIT_1
    assert inherited_bit((DETECTOR_BIT_1, DETECTOR_BIT_0), BIT_NONE) == DETECTOR_NONE
    assert inherited_bit((DETECTOR_BIT_1, DETECTOR_BIT_0), 1) == DETECTOR_BIT_0
    assert inherited_bit(()) == DETECTOR_NONE
    with pytest.raises(ValueError, match="role index"):
        inherited_bit((DETECTOR_BIT_1,), 1)
    with pytest.raises(ValueError, match="Detector bits"):
        inherited_bit((3,))
