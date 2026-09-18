"""A click is an absorption (detector-absorb-v1; Highlights 5.4, model owner,
2026-09-18; issue #169, feature 2c) under the law of the bit (bit-law-v1): a
thing a marked Node catches (its counter table, `setting`) is absorbed into the
mark's counter with its momentum, on the marks' line of the ledger, unless the
mark declares `on_click: "pass"` for its family, when it walks on with the bit
1; a shadow is returned and never counted (test_bit_law.py).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A click is an
absorption") before the first run. Re-pinned on 2026-09-18 under bit-law-v1:
the field family `G` (`field_of` quanta) and its per-tick release went with the
law, so the marks off the lamp's line (A, B, E) see nothing and the reading is
C's: absorb is the default for every family, the matter ray of the old world
is a thing and C catches it at tick 4 with its momentum; a click names the
thing's owner.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    BIT_THING,
    CLICK_ABSORB,
    CLICK_DEFAULT,
    CLICK_PASS,
    DetectorMark,
    Ray,
    Resident,
    click_coupling,
    detector_absorb,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
LAMP = (5, 7, 7)
A, B, C, E = (6, 8, 7), (6, 6, 7), (9, 7, 7), (6, 7, 6)
AMOUNT = 4
CHARGE = -2
TICKS = 6
ZERO = (0, 0, 0)


def mark(position, setting=(1, 1), **keys):
    return {"position": list(position), "setting": list(setting)} | keys


def marks(matter="absorb"):
    """The four marks: A on the defaults, B passing quanta, C absorbing quanta (or
    on the defaults), E absorbing every family; only C is on the lamp's line."""
    return [
        mark(A),
        mark(B, on_click={"quanta": "pass"}),
        mark(C, **({} if matter == "default" else {"on_click": {"quanta": matter}})),
        mark(E, on_click="absorb"),
    ]


def document(detectors, ticks=TICKS):
    return {
        "schema_version": 1,
        "K": AMOUNT,
        "model_id": "detector-absorb-test-v1",
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
                "name": "lamp",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": AMOUNT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 1,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "charge": CHARGE,
                "kerengonen": {"phase_steps": 8},
                # The clock is the content (clock-readings-v1): one step per interval at K.
                "clock": True,
            }
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "quanta",
                "amount": AMOUNT,
                "denominator": 1,
                "heading": HEADINGS[0],
                "kerengonen_phase": 0,
            }
        ],
        "seeds": [{"position": list(LAMP), "type": "lamp"}],
        "detectors": [dict(item) for item in detectors],
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


def rays_at(world, position, index):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return () if node is None or not node.rays else node.rays[index]


def mark_at(world, position):
    node = world._spatial.nodes.get(position)
    if node is None:
        return next(m for m in world.initial.detectors if m.position == position)
    return node.detector


def event(kind, tick, position, **detail):
    return {"event": kind, "tick": tick, "position": position} | detail


def line(readout, name, ledger):
    return {
        key: ledger[readout][name][key]
        for key in (
            "initial",
            "sourced",
            "current",
            "escaped",
            "absorbed",
            "absorbed_by_marks",
        )
    }


def test_a_click_absorbs_a_thing_by_default(tmp_path):
    raw = document(marks())
    initial = parse_initial_state(raw)
    (quanta,) = initial.spatial_fields
    declared = {m.position: m for m in initial.detectors}
    assert declared[A].on_click == () and declared[A].click_keys == 0
    assert declared[B].on_click == (CLICK_PASS,) and declared[B].click_keys == 1
    assert declared[C].on_click == (CLICK_ABSORB,)
    assert declared[E].on_click == (CLICK_ABSORB,)
    assert declared[A].resident.things == () and declared[A].resident.momentum == ZERO
    events = []
    world = Simulation(
        initial,
        observer=lambda item: (
            events.append(item)
            if item["event"] in ("detector_click", "detector_return", "inverse_split")
            else None
        ),
    )
    for tick in range(1, TICKS + 1):
        world.step()
        taken = AMOUNT if tick >= 4 else 0
        ledger = world.audit()
        assert ledger["balanced"] and world.conservation_report()["status"] == "passed"
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        # (a) The world ledger, exact at every tick with the marks' line: the thing
        # absorbed at C at tick 4 with its momentum, leaving the lamp's recoil as
        # the world's momentum.
        assert line("fields", "quanta", ledger) == {
            "initial": (AMOUNT,),
            "sourced": (0,),
            "current": (AMOUNT - taken,),
            "escaped": (0,),
            "absorbed": (0,),
            "absorbed_by_marks": (taken,),
        }
        assert ledger["real"]["quanta"]["absorbed"] == (taken,)
        assert line("fields", "momentum", ledger)["current"] == (-taken, 0, 0)
        assert line("fields", "momentum", ledger)["absorbed_by_marks"] == (taken, 0, 0)
        assert world.real_content() == AMOUNT - taken and world.shadow_content() == 0
    # (b) One click, C's, naming the thing and what it absorbed; C's counter and
    # momentum; A, B and E untouched.
    assert events == [
        event("detector_click", 4, C, port=1, family="quanta", amount=AMOUNT, bit=1, owner=1, absorbed=4)
    ]
    # The resident thing of C (node-is-ports-v1): the thing absorbed, its momentum
    # and its owner; the marks A, B and E hold nothing.
    resident = mark_at(world, C).resident
    assert (resident.things, resident.shadows, resident.momentum) == ((AMOUNT,), (0,), (AMOUNT, 0, 0))
    assert resident.owners == (1,)
    for position in (A, B, E):
        assert mark_at(world, position).resident.things == ()
        assert mark_at(world, position).resident.momentum == ZERO
    assert not any(node.rays and any(node.rays) for node in world.inventory_view().nodes)
    # (c) The runner: the marks' totals and momentum, the marks with their counters.
    path = tmp_path / "absorb.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "absorb", ticks=TICKS)
    metadata = json.loads((tmp_path / "absorb" / "run.json").read_text(encoding="utf-8"))
    assert metadata["detector_mark_totals"] == {"quanta": [AMOUNT], "momentum": [AMOUNT, 0, 0]}
    assert metadata["detector_mark_momentum"] == [AMOUNT, 0, 0]
    assert [item["resident"]["real"] for item in metadata["detector_marks"]] == [
        {},
        {},
        {"quanta": AMOUNT},
        {},
    ]
    assert metadata["detector_marks"][2]["resident"]["owners"] == [1]
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["local_conservation"]["status"] == "passed"


def test_a_thing_passes_with_the_bit_when_the_mark_says_so(tmp_path):
    # (d) Under `on_click: {"quanta": "pass"}` at C the thing passes with the bit
    # 1: the click has no `absorbed` entry, C's counter stays empty, the ray
    # walks on.
    raw = document(marks("pass"))
    events = []
    world = Simulation(
        parse_initial_state(raw),
        observer=lambda item: events.append(item) if item["event"] == "detector_click" else None,
    )
    for _ in range(4):
        world.step()
    assert events == [
        event("detector_click", 4, C, port=1, family="quanta", amount=AMOUNT, bit=1, owner=1)
    ]
    assert mark_at(world, C).resident.things == () and mark_at(world, C).resident.momentum == ZERO
    (walking,) = [
        ray for node in world.inventory_view().nodes for ray in (node.rays[0] if node.rays else ())
    ]
    assert (walking.amount, walking.detector, walking.outbound) == (AMOUNT, BIT_THING, 1)
    assert mark_at(world, C).click_keys == 1
    ledger = world.audit()
    assert line("fields", "quanta", ledger)["absorbed_by_marks"] == (0,)
    assert line("fields", "momentum", ledger)["current"] == ZERO
    assert ledger["marks"]["momentum"] == ZERO
    # (e) A world whose marks pass every click: no `absorbed` entry on any click,
    # no `absorbed_by_mark` reading, the marks' line zero and every counter empty.
    passing = document([mark(A, on_click="pass"), mark(C, on_click="pass"), mark(E, on_click="pass")])
    path = tmp_path / "passing.json"
    path.write_text(json.dumps(passing), encoding="utf-8")
    run_initialization(path, tmp_path / "passing", ticks=TICKS)
    recorded = [
        json.loads(text)
        for text in (tmp_path / "passing" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    clicks = [item for item in recorded if item["event"] == "detector_click"]
    assert len(clicks) == 1 and not any("absorbed" in item for item in clicks)
    assert not any(
        "absorbed_by_mark" in item for item in recorded if item["event"] == "spatial_received"
    )
    metadata = json.loads((tmp_path / "passing" / "run.json").read_text(encoding="utf-8"))
    assert metadata["detector_mark_totals"] == {"quanta": [0], "momentum": [0, 0, 0]}
    assert metadata["detector_mark_momentum"] == [0, 0, 0]
    assert all(
        item["resident"]["real"] == {} and item["resident"]["momentum"] == [0, 0, 0]
        for item in metadata["detector_marks"]
    )
    assert all(ledger["fields"]["quanta"]["absorbed_by_marks"] == [0] for ledger in metadata["audit"])
    assert (
        metadata["conserved_at_every_completed_tick"]
        and metadata["local_conservation"]["status"] == "passed"
    )


def test_the_click_keys_are_validated_and_the_helpers_are_exact():
    # (f) `on_click` takes absorb, pass or a mapping of ray family to one of them;
    # anything else, an unknown family or a family that is no ray field is refused
    # before a world exists; the helpers read the declared value or the default.
    for value, message in (
        ("maybe", "on_click must be absorb, pass or a mapping"),
        (5, "on_click must be absorb, pass or a mapping"),
        ({"quanta": "draw"}, "on_click.quanta must be absorb or pass"),
        ({"photon": "absorb"}, "unknown ray family: photon"),
        ({"momentum": "absorb"}, "unknown ray family: momentum"),
    ):
        raw = document([mark(A, on_click=value)])
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
        assert not validate_configuration(json.dumps(raw)).valid
    with pytest.raises(ValueError, match="absorb or pass"):
        DetectorMark(A, 1, 1, on_click=(5,))
    with pytest.raises(ValueError, match="nonnegative"):
        Resident(things=(-1,), shadows=(0,))
    with pytest.raises(ValueError, match="resident thing"):
        DetectorMark(A, 1, 1, resident=())
    assert DetectorMark(A, 1, 1) == DetectorMark(A, 1, 1, (), 0, Resident())
    initial = parse_initial_state(document(marks()))
    (quanta,) = initial.spatial_fields
    plain = DetectorMark(A, 1, 1)
    assert click_coupling(plain, 0, quanta) == CLICK_ABSORB
    declared = DetectorMark(A, 1, 1, on_click=(CLICK_PASS,), click_keys=1)
    assert click_coupling(declared, 0, quanta) == CLICK_PASS
    assert CLICK_DEFAULT == -1
    # The absorption into the resident thing (node-is-ports-v1): its things line
    # sized on the first take, the momentum amount x heading plus the pushes the
    # thing carries (clock-readings-v1), added exactly; a shadow home to it goes
    # on its shadows line with the momentum it carries.
    taken = detector_absorb(plain, 0, (Ray(2, ZERO, 3), Ray(5, ZERO, 1, momentum=(1, -1, 0))), quanta, 1)
    assert (taken.resident.things, taken.resident.momentum) == ((4,), (1, 2, -1))
    again = detector_absorb(taken, 0, (Ray(0, ZERO, 4, detector=BIT_THING),), quanta, 1)
    assert (again.resident.things, again.resident.momentum) == ((8,), (5, 2, -1))
    home = detector_absorb(
        again, 0, (Ray(1, ZERO, 2, detector=BIT_SHADOW, outbound=0, momentum=(-1, 0, 0)),), quanta, 1
    )
    assert (home.resident.things, home.resident.shadows, home.resident.momentum) == (
        (8,),
        (2,),
        (4, 2, -1),
    )
    assert again.position == A and again.on_click == () and again.resident.owners == (0,)
