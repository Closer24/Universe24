"""A click is an absorption (detector-absorb-v1; Highlights 5.4, model owner, 2026-09-18).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A click is an
absorption") before the first run: a lamp at (5,7,7) sends 4 quanta (charge -2,
rest rate 1) along +X, recoiling into `momentum`; the ray releases its field `G`
(`field_of` quanta, release 1/4) on the five other headings at (6,7,7) in the
cycle of tick 1, so G 1 reaches five Nodes at tick 2, three of them marked with
setting 1/1: A (6,8,7) on the defaults absorbs the field quantum (its counter G
1, momentum (0, 1, 0), the click recording `absorbed` 1, the Node holding no
ray); B (6,6,7) under `on_click: {"G": "pass"}` passes it with bit 1; E (6,7,6)
under `on_click: "absorb"` absorbs it (the draw of 0, the return, is untouched
and is the return test's). C (9,7,7) under `on_click: {"quanta": "absorb"}` absorbs the matter ray
at tick 4 (counter quanta 4, momentum (4, 0, 0)), a screen that stops
electrons; on the defaults the same ray passes with the bit 1 as before. The
world ledger reads initial + sourced = current + escaped + annulled + absorbed +
absorbed_by_marks exactly at every tick for amount, momentum and charge, the
marks' own lines beside it; the local audit passes with its `absorbed_by_marks`
line; the runner records the identity, the marks and their totals; the keys are
validated; a world whose marks pass every click has no `absorbed` entry and no
`absorbed_by_mark` reading, its clicks recorded as before.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.spatial_state import (
    CLICK_ABSORB,
    CLICK_DEFAULT,
    CLICK_PASS,
    DETECTOR_ABSORB,
    DETECTOR_BIT_1,
    DETECTOR_NONE,
    DetectorMark,
    Ray,
    click_coupling,
    detector_absorb,
    field_family,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
LAMP = (5, 7, 7)
RELEASE_NODE = (6, 7, 7)
A, B, C, E = (6, 8, 7), (6, 6, 7), (9, 7, 7), (6, 7, 6)
AMOUNT = 4
CHARGE = -2
TICKS = 6
ZERO = (0, 0, 0)
# The ticket state after one draw from seed 0 (setting 1/1 draws 1), as in the
# bit-property test.
SEED_0_ONCE = 1


def mark(position, setting=(1, 1), seed=0, **keys):
    return {"position": list(position), "setting": list(setting), "seed": seed} | keys


def marks(matter="absorb"):
    """The four marks: A on the defaults, B passing G, C absorbing quanta (or on the
    defaults), E absorbing every family."""
    return [
        mark(A),
        mark(B, on_click={"G": "pass"}),
        mark(C, **({} if matter == "default" else {"on_click": {"quanta": matter}})),
        mark(E, on_click="absorb"),
    ]


def document(detectors, ticks=TICKS):
    return {
        "schema_version": 1,
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
                "name": "G",
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
                "kerengonen": {"phase_steps": 8, "phase_advance": 1},
            },
            {
                "field": "G",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 1,
                "ray_slots": 16,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8, "phase_advance": 0},
                "field_of": "quanta",
                "release": [1, 4],
            },
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "quanta",
                "amount": AMOUNT,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
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
                "energy": {
                    "op": "add",
                    "args": [{"field": "quanta", "side": "right"}, {"field": "G", "side": "right"}],
                },
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
            "annulled",
            "absorbed",
            "absorbed_by_marks",
        )
    }


def test_a_click_absorbs_a_field_quantum_and_passes_matter_by_default(tmp_path):
    raw = document(marks())
    initial = parse_initial_state(raw)
    quanta, g = initial.spatial_fields
    # The engine's notion of a field family: the one declared field_of another.
    assert not field_family(quanta) and field_family(g)
    declared = {m.position: m for m in initial.detectors}
    assert declared[A].on_click == () and declared[A].click_keys == 0
    assert declared[B].on_click == (CLICK_DEFAULT, CLICK_PASS) and declared[B].click_keys == 1
    assert declared[C].on_click == (CLICK_ABSORB, CLICK_DEFAULT)
    assert declared[E].on_click == (CLICK_ABSORB, CLICK_ABSORB)
    assert declared[A].counter == () and declared[A].momentum == ZERO
    events = []
    world = Simulation(
        initial,
        observer=lambda item: (
            events.append(item)
            if item["event"] in ("detector_click", "detector_pass", "detector_return", "inverse_split")
            else None
        ),
    )
    for tick in range(1, TICKS + 1):
        world.step()
        sourced_g = 5 * min(max(tick - 1, 0), 3)
        taken_g = 2 if tick >= 2 else 0
        taken_quanta = AMOUNT if tick >= 4 else 0
        ledger = world.audit()
        assert ledger["balanced"] and world.conservation_report()["status"] == "passed"
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        # (a) The world ledger, exact at every tick with the marks' line: the field
        # quanta absorbed at A and E at tick 2, the matter ray absorbed at C at tick
        # 4 with its momentum, leaving the lamp's recoil as the world's momentum.
        assert line("fields", "G", ledger) == {
            "initial": (0,),
            "sourced": (sourced_g,),
            "current": (sourced_g - taken_g,),
            "escaped": (0,),
            "annulled": (0,),
            "absorbed": (0,),
            "absorbed_by_marks": (taken_g,),
        }
        assert line("fields", "quanta", ledger) == {
            "initial": (AMOUNT,),
            "sourced": (0,),
            "current": (AMOUNT - taken_quanta,),
            "escaped": (0,),
            "annulled": (0,),
            "absorbed": (0,),
            "absorbed_by_marks": (taken_quanta,),
        }
        assert line("fields", "momentum", ledger) == {
            "initial": ZERO,
            "sourced": ZERO,
            "current": (-taken_quanta, 0, 0),
            "escaped": ZERO,
            "annulled": ZERO,
            "absorbed": ZERO,
            "absorbed_by_marks": (taken_quanta, 0, 0),
        }
        assert line("charge", "quanta", ledger) == {
            "initial": CHARGE * AMOUNT,
            "sourced": 0,
            "current": CHARGE * (AMOUNT - taken_quanta),
            "escaped": 0,
            "annulled": 0,
            "absorbed": 0,
            "absorbed_by_marks": CHARGE * taken_quanta,
        }
        assert ledger["marks"] == {
            "count": 4,
            "momentum": (taken_quanta, taken_g // 2, -(taken_g // 2)),
            "counter": {"quanta": (taken_quanta,), "G": (taken_g,), "momentum": (taken_quanta, 0, 0)},
        }
        assert world.detector_mark_totals() == ledger["marks"]["counter"]
        assert world.detector_mark_momentum() == ledger["marks"]["momentum"]
        assert world.spatial_accounting()["G"]["absorbed_by_marks"] == (taken_g,)
        assert world.spatial_accounting()["quanta"]["absorbed_by_marks"] == (taken_quanta,)
        # (b) The marks: their counters and momentum, bounded metadata on the Node.
        assert mark_at(world, A).counter == ((0, 1) if tick >= 2 else ())
        assert mark_at(world, A).momentum == ((0, 1, 0) if tick >= 2 else ZERO)
        assert mark_at(world, E).counter == ((0, 1) if tick >= 2 else ())
        assert mark_at(world, E).momentum == ((0, 0, -1) if tick >= 2 else ZERO)
        assert mark_at(world, C).counter == ((AMOUNT, 0) if tick >= 4 else ())
        assert mark_at(world, C).momentum == ((AMOUNT, 0, 0) if tick >= 4 else ZERO)
        assert mark_at(world, B).counter == ()
        if tick >= 2:
            assert world._spatial.nodes[A].detector_ticket == SEED_0_ONCE
            # (c) Nothing of an absorbed quantum is delivered: A and E hold no G ray,
            # B holds the passing G ray with its bit 1 at tick 2.
            assert rays_at(world, A, 1) == () and rays_at(world, E, 1) == ()
        if tick == 2:
            (passed,) = rays_at(world, B, 1)
            assert (passed.heading, passed.amount, passed.outbound, passed.detector) == (
                3,
                1,
                1,
                DETECTOR_BIT_1,
            )
        if tick >= 4:
            assert not any(
                ray
                for node in world.inventory_view().nodes
                for ray in (node.rays[0] if node.rays else ())
            )
    assert world.detector_marks() == [
        {"position": list(A), "momentum": [0, 1, 0], "counter": {"G": 1}},
        {"position": list(B), "momentum": [0, 0, 0], "counter": {}},
        {"position": list(C), "momentum": [AMOUNT, 0, 0], "counter": {"quanta": AMOUNT}},
        {"position": list(E), "momentum": [0, 0, -1], "counter": {"G": 1}},
    ]
    # (d) The events: the clicks of tick 2 in Node order, the absorbing ones with
    # the absorbed amount, and the matter click at C at tick 4.
    assert events == [
        event("detector_click", 2, B, port=2, family="G", amount=1, bit=1),
        event("detector_click", 2, E, port=4, family="G", amount=1, bit=1, absorbed=1),
        event("detector_click", 2, A, port=3, family="G", amount=1, bit=1, absorbed=1),
        event("detector_click", 4, C, port=1, family="quanta", amount=AMOUNT, bit=1, absorbed=AMOUNT),
    ]
    # (e) The local audit reads the marks' line: what the marks absorbed, energy
    # through the declared expression (both families), momentum and charge.
    report = world.conservation_report()
    assert report["absorbed_by_marks"] == {
        "energy": 6,
        "momentum": (AMOUNT, 1, -1),
        "charge": CHARGE * AMOUNT,
    }
    for key in ("energy", "charge"):
        assert report["initial"][key] + report["sourced"][key] == (
            report["current"][key]
            + report["escaped"][key]
            + report["annulled"][key]
            + report["absorbed_by_marks"][key]
        )
    # (f) The runner records the identity, the marks and their lines, the reception
    # record carrying what the mark absorbed; a second run replays byte for byte.
    path = tmp_path / "absorb.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    records = []
    for name in ("first", "second"):
        run_initialization(path, tmp_path / name, ticks=TICKS)
        lines = (tmp_path / name / "events.jsonl").read_text(encoding="utf-8")
        metadata = json.loads((tmp_path / name / "run.json").read_text(encoding="utf-8"))
        metadata.pop("elapsed_seconds")
        records.append((lines, metadata))
    (first_events, first_run), (second_events, second_run) = records
    assert first_events == second_events and first_run == second_run
    assert first_run["detector_absorb"] == DETECTOR_ABSORB == "detector-absorb-v1"
    assert first_run["detector_marks"] == world.detector_marks()
    assert first_run["detector_mark_totals"] == {
        "quanta": [AMOUNT],
        "G": [2],
        "momentum": [AMOUNT, 0, 0],
    }
    assert first_run["detector_mark_momentum"] == [AMOUNT, 1, -1]
    assert (
        first_run["conserved_at_every_completed_tick"]
        and first_run["accounting_balanced_at_every_completed_tick"]
    )
    assert first_run["local_conservation"]["status"] == "passed"
    assert first_run["local_conservation"]["absorbed_by_marks"] == {
        "energy": 6,
        "momentum": [AMOUNT, 1, -1],
        "charge": CHARGE * AMOUNT,
    }
    assert first_run["final_totals"] == {"quanta": [0], "G": [13], "momentum": [-AMOUNT, 0, 0]}
    recorded = [json.loads(text) for text in first_events.splitlines()]
    assert [item for item in recorded if item["event"].startswith("detector_")] == [
        {**item, "position": list(item["position"])} for item in events
    ]
    received = {
        (tuple(item["position"]), item["tick"]): item.get("absorbed_by_mark")
        for item in recorded
        if item["event"] == "spatial_received" and item.get("absorbed_by_mark")
    }
    assert received == {
        (A, 2): {"G": {"amount": 1, "momentum": [0, 1, 0]}},
        (E, 2): {"G": {"amount": 1, "momentum": [0, 0, -1]}},
        (C, 4): {"quanta": {"amount": AMOUNT, "momentum": [AMOUNT, 0, 0]}},
    }


def test_matter_passes_with_the_bit_by_default_and_a_passing_world_records_no_absorption(tmp_path):
    # (g) On the defaults the matter ray passes C with the bit 1 exactly as before:
    # the click has no `absorbed` entry, C's counter stays empty after tick 4, the
    # ray walks on (and the field it releases beyond C reaches C at tick 6, a
    # field click that absorbs, so the reading stops at tick 4).
    raw = document(marks("default"))
    events = []
    world = Simulation(
        parse_initial_state(raw),
        observer=lambda item: events.append(item) if item["event"] == "detector_click" else None,
    )
    for _ in range(4):
        world.step()
    assert events[-1] == event("detector_click", 4, C, port=1, family="quanta", amount=AMOUNT, bit=1)
    assert mark_at(world, C).counter == () and mark_at(world, C).momentum == ZERO
    (walking,) = [
        ray for node in world.inventory_view().nodes for ray in (node.rays[0] if node.rays else ())
    ]
    assert (walking.amount, walking.detector, walking.outbound) == (AMOUNT, DETECTOR_BIT_1, 1)
    assert mark_at(world, C).click_keys == 0
    ledger = world.audit()
    assert line("fields", "quanta", ledger)["absorbed_by_marks"] == (0,)
    assert line("fields", "momentum", ledger)["current"] == ZERO
    assert ledger["marks"]["momentum"] == (0, 1, -1)
    # (h) A world whose marks pass every click: no `absorbed` entry on any click,
    # no `absorbed_by_mark` reading, the marks' line zero and every counter empty.
    passing = document([mark(A, on_click="pass"), mark(B, on_click="pass"), mark(E, on_click="pass")])
    path = tmp_path / "passing.json"
    path.write_text(json.dumps(passing), encoding="utf-8")
    run_initialization(path, tmp_path / "passing", ticks=TICKS)
    recorded = [
        json.loads(text)
        for text in (tmp_path / "passing" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    clicks = [item for item in recorded if item["event"] == "detector_click"]
    assert len(clicks) == 3 and not any("absorbed" in item for item in clicks)
    assert not any(
        "absorbed_by_mark" in item for item in recorded if item["event"] == "spatial_received"
    )
    metadata = json.loads((tmp_path / "passing" / "run.json").read_text(encoding="utf-8"))
    assert metadata["detector_mark_totals"] == {"quanta": [0], "G": [0], "momentum": [0, 0, 0]}
    assert metadata["detector_mark_momentum"] == [0, 0, 0]
    assert all(
        item["counter"] == {} and item["momentum"] == [0, 0, 0] for item in metadata["detector_marks"]
    )
    assert all(ledger["fields"]["G"]["absorbed_by_marks"] == [0] for ledger in metadata["audit"])
    assert (
        metadata["conserved_at_every_completed_tick"]
        and metadata["local_conservation"]["status"] == "passed"
    )


def test_the_click_keys_are_validated_and_the_helpers_are_exact():
    # (i) `on_click` takes absorb, pass or a mapping of ray family to one of them;
    # anything else, an unknown family or a family that is no ray field is refused
    # before a world exists; the helpers read the declared value or the default.
    for value, message in (
        ("maybe", "on_click must be absorb, pass or a mapping"),
        (5, "on_click must be absorb, pass or a mapping"),
        ({"G": "draw"}, "on_click.G must be absorb or pass"),
        ({"photon": "absorb"}, "unknown ray family: photon"),
        ({"momentum": "absorb"}, "unknown ray family: momentum"),
    ):
        raw = document([mark(A, on_click=value)])
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
        assert not validate_configuration(json.dumps(raw)).valid
    with pytest.raises(ValueError, match="absorb or pass"):
        DetectorMark(A, 1, 1, 0, on_click=(5,))
    with pytest.raises(ValueError, match="nonnegative"):
        DetectorMark(A, 1, 1, 0, counter=(-1,))
    assert DetectorMark(A, 1, 1, 0) == DetectorMark(A, 1, 1, 0, 0, 0, 0, (), 0, (), ZERO)
    initial = parse_initial_state(document(marks()))
    quanta, g = initial.spatial_fields
    plain = DetectorMark(A, 1, 1, 0)
    assert click_coupling(plain, 0, quanta) == CLICK_PASS and click_coupling(plain, 1, g) == CLICK_ABSORB
    declared = DetectorMark(A, 1, 1, 0, on_click=(CLICK_ABSORB, CLICK_PASS), click_keys=1)
    assert (
        click_coupling(declared, 0, quanta) == CLICK_ABSORB
        and click_coupling(declared, 1, g) == CLICK_PASS
    )
    # The absorption: the counter sized on the first take, the momentum amount x
    # heading, or the register where a push set one, added exactly.
    taken = detector_absorb(plain, 1, (Ray(2, ZERO, 3), Ray(5, ZERO, 1, momentum=(1, -1, 0))), g, 2)
    assert (taken.counter, taken.momentum) == ((0, 4), (1, 2, 0))
    again = detector_absorb(taken, 0, (Ray(0, ZERO, 4, detector=DETECTOR_NONE),), quanta, 2)
    assert (again.counter, again.momentum) == ((4, 4), (5, 2, 0))
    assert again.position == A and again.on_click == () and again.seed == 0
