"""Audits (ray-event-audit-v1): the world ledger per completed tick, exact for
amount, momentum and charge through a return, an inverse split, a release, an
escape and an external body's sink; the runner's conservation flag; a
charge-changing rule rejected at validation; a hand-altered record reported by
tick and line.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Ray-event audit")
before the first run: a charged pair lamp (+1 and -1 quanta), a marked Node
that returns the plus arm (0), an electron lamp whose field family releases as
a source, and an open boundary, one world per return mode (annul, siblings) and
one with an external body (a sink) on the minus arm.
"""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.ray_event_audit import RAY_EVENT_AUDIT, audit_failure, line_balanced
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

SHAPE = (9, 5, 5)
X = (4, 2, 2)
MARK = (7, 2, 2)
E = (0, 4, 0)
B = (1, 2, 2)
BODY = {"position": list(B), "family": "star", "amount": 100, "charge": 3, "coupling": "sink"}
SEED = 3
TICKS = 9
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# G released per tick and escaped per tick (cumulative), from the electron's four
# crossings at (0,4,1..4): two field rays leave the world at once at every crossing,
# the one behind it walks back to z = 0 and the one on -Y walks to y = 0.
G_SOURCED = {0: 0, 1: 0, 2: 5, 3: 10, 4: 15, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20}
G_ESCAPED = {0: 0, 1: 0, 2: 2, 3: 5, 4: 7, 5: 10, 6: 11, 7: 13, 8: 14, 9: 16}
# A rule whose outputs change the total charge: the minus quantum leaves as plus.
CHARGE_BREAKING = {
    "name": "flip",
    "participants": [{"type": "plus"}, {"type": "minus"}],
    "outputs": [
        {"field": "plus", "amount": {"of": 0}, "heading": "same"},
        {"field": "plus", "amount": {"of": 1}, "heading": "same", "input": 1},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def field(name, components=1, signed=False):
    return {
        "name": name,
        "components": components,
        "units": "quantum" if components == 1 else "quantum times heading",
        "signed": signed,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, slots=8, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "kerengonen": {"phase_steps": 8, "phase_advance": 0},
    } | extra


def emission(kind, name, amount, heading):
    return {
        "type": kind,
        "field": name,
        "amount": amount,
        "denominator": 1,
        "source": False,
        "heading": HEADINGS[heading],
        "recoil_field": "momentum",
        "kerengonen_phase": 0,
    }


def document(mode, source=True, conservation=False, rules=(), body=False):
    """The board: the pair lamp at X, the mark three Links out on the plus arm,
    (with `source`) the electron lamp at the corner E whose field G releases, and
    (with `body`) an external body at B on the minus arm, a sink of family star."""
    raw = {
        "schema_version": 1,
        "model_id": "ray-event-audit-test-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": TICKS,
        "return_mode": mode,
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
        "fields": [field("plus"), field("minus"), field("momentum", 3, True)],
        "disturbance_types": [
            {
                "name": "pair",
                "fields": ["plus", "minus", "momentum"],
                "defaults": {"plus": 1, "minus": 1, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [ray_field("plus", charge=1), ray_field("minus", charge=-1)],
        "emissions": [emission("pair", "plus", 1, 0), emission("pair", "minus", 1, 1)],
        "seeds": [{"position": list(X), "type": "pair"}],
        "detectors": [{"position": list(MARK), "setting": [1, 2], "seed": SEED}],
        "ray_interactions": list(rules),
    }
    if source:
        raw["fields"] += [field("electron"), field("G")]
        raw["disturbance_types"].append(
            {
                "name": "source",
                "fields": ["electron", "momentum"],
                "defaults": {"electron": 4, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        )
        raw["spatial_fields"] += [
            ray_field("electron"),
            ray_field("G", 16, field_of="electron", release=[1, 4]),
        ]
        raw["emissions"].append(emission("source", "electron", 4, 4))
        raw["seeds"].append({"position": list(E), "type": "source"})
    if body:
        raw["fields"].append(field("star"))
        raw["spatial_fields"].append(ray_field("star"))
        raw["external_bodies"] = [BODY]
    if conservation:
        both = {"op": "add", "args": [{"field": "plus"}, {"field": "minus"}]}
        names = ["plus", "minus"] + (["electron", "G"] if source else [])
        energy = {"field": names[0], "side": "right"}
        for name in names[1:]:
            energy = {"op": "add", "args": [energy, {"field": name, "side": "right"}]}
        raw["conservation"] = {
            "name": "pair",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["plus", "minus", "momentum"],
                    "energy": both,
                    "momentum": {"field": "momentum"},
                }
            ]
            + (
                [
                    {
                        "requires": ["electron", "momentum"],
                        "energy": {"field": "electron"},
                        "momentum": {"field": "momentum"},
                    }
                ]
                if source
                else []
            ),
            "spatial": {"energy": energy, "momentum": {"op": "vector", "args": [0, 0, 0]}},
        }
    return raw


def line(initial, current, escaped=None, annulled=None, sourced=None, absorbed=None):
    """A ledger line; a line not given is zero of the readout's width. Since
    detector-absorb-v1 (2026-09-18) every line also reads `absorbed_by_marks`, what
    the Detector marks absorbed on their clicks: zero here, since the mark of this
    board returns the one ray that reaches it and no field ray clicks."""
    zero = 0 if isinstance(initial, int) else (0,) * len(initial)
    return {
        "initial": initial,
        "sourced": zero if sourced is None else sourced,
        "current": current,
        "escaped": zero if escaped is None else escaped,
        "annulled": zero if annulled is None else annulled,
        "absorbed": zero if absorbed is None else absorbed,
        "absorbed_by_marks": zero,
        "balanced": True,
    }


def expected_ledger(mode, tick, source=True, body=False):
    """The pinned ledger after tick t: the plus arm returned at tick 3, at X after
    tick 6, annulled or restored in the cycle labelled 6; the minus arm escapes at
    tick 5, or ends in the body's sink at tick 3; the electron escapes at tick 5;
    the electron's field released and escaping."""
    gone = mode == "annul" and tick >= 7
    out = tick >= 5
    sunk = body and tick >= 3
    minus_gone = sunk or (out and not body)
    fields = {
        "plus": line((1,), (0,) if gone else (1,), annulled=(1,) if gone else (0,)),
        "minus": line(
            (1,),
            (0,) if minus_gone else (1,),
            escaped=(1,) if out and not body else (0,),
            absorbed=(1,) if sunk else (0,),
        ),
        "momentum": line(
            (0, 0, 0),
            (
                (0, 0, -4 if source else 0)
                if gone
                else (1, 0, -4 if source else 0)
                if out
                else (1, 0, 0)
                if sunk
                else (0, 0, 0)
            ),
            escaped=(-1 if not body else 0, 0, 4 if source else 0) if out else (0, 0, 0),
            annulled=(1, 0, 0) if gone else (0, 0, 0),
            absorbed=(-1, 0, 0) if sunk else (0, 0, 0),
        ),
    }
    charge = {
        "plus": line(1, 0 if gone else 1, annulled=1 if gone else 0),
        "minus": line(
            -1,
            0 if minus_gone else -1,
            escaped=-1 if out and not body else 0,
            absorbed=-1 if sunk else 0,
        ),
    }
    if source:
        fields["electron"] = line((4,), (0,) if out else (4,), escaped=(4,) if out else (0,))
        fields["G"] = line(
            (0,),
            (G_SOURCED[tick] - G_ESCAPED[tick],),
            escaped=(G_ESCAPED[tick],),
            sourced=(G_SOURCED[tick],),
        )
        charge["electron"] = line(0, 0)
        charge["G"] = line(0, 0)
    if body:
        fields["star"] = line((0,), (0,))
        charge["star"] = line(0, 0)
    bodies = {
        "count": 1 if body else 0,
        "momentum": (0, 0, 0),
        "charge": 3 if body else 0,
        "sink": {name: item["absorbed"] for name, item in fields.items()},
    }
    # The marks' own lines (detector-absorb-v1, 2026-09-18): the one mark at MARK,
    # which absorbed nothing (it returns the plus arm, and nothing else reaches it).
    marks = {
        "count": 1,
        "momentum": (0, 0, 0),
        "counter": {name: item["absorbed_by_marks"] for name, item in fields.items()},
    }
    return {
        "tick": tick,
        "balanced": True,
        "fields": fields,
        "charge": charge,
        "bodies": bodies,
        "marks": marks,
    }


def as_json(value):
    return json.loads(json.dumps(value))


@pytest.mark.parametrize(
    "mode,body",
    [("annul", False), ("siblings", False), ("annul", True)],
    ids=["annul", "siblings", "body"],
)
def test_the_world_ledger_is_exact_for_amount_momentum_and_charge(mode, body, tmp_path):
    initial = parse_initial_state(document(mode, body=body))
    definitions = {initial.fields[d.field].name: d for d in initial.spatial_fields}
    assert (definitions["plus"].charge, definitions["minus"].charge) == (1, -1)
    assert (definitions["G"].field_of, definitions["G"].release_numerator) == (2, 1)
    events = []
    world = Simulation(
        initial,
        observer=lambda event: (
            events.append(event)
            if event["event"] in ("inverse_split", "detector_return", "detector_click")
            else None
        ),
    )
    # (a) Before the first tick the lamps hold everything: the charge readout counts
    # the stock a record holds of a charged family, like totals() counts its amount.
    star = {"star": 0} if body else {}
    assert world.charge_totals() == {"plus": 1, "minus": -1, "electron": 0, "G": 0} | star
    assert world.escaped_charge_totals() == {"plus": 0, "minus": 0, "electron": 0, "G": 0} | star
    assert world.audit() == expected_ledger(mode, 0, body=body)
    ledgers = []
    for tick in range(1, TICKS + 1):
        world.step()
        ledger = world.audit()
        ledgers.append(ledger)
        # (b) The ledger after every tick, every line balanced: initial + sourced =
        # current + escaped + annulled + absorbed for amount, momentum and charge,
        # through the return (tick 3), the inverse split (cycle 6), the release
        # (from tick 2) and the escapes (from tick 2, the minus arm at tick 5).
        assert ledger == expected_ledger(mode, tick, body=body)
        assert all(line_balanced(item) for item in ledger["fields"].values())
        assert all(line_balanced(item) for item in ledger["charge"].values())
        assert (
            world.escaped_charge_totals()
            == {
                "plus": 0,
                "minus": -1 if tick >= 5 and not body else 0,
                "electron": 0,
                "G": 0,
            }
            | star
        )
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        if body:
            # The body at B took the minus arm into its sink at tick 3 and is unmoved.
            assert world.external_bodies() == [
                {
                    "index": 0,
                    "position": list(B),
                    "stepping": False,
                    "momentum": [0, 0, 0],
                    "accumulators": [0, 0, 0],
                    "sink": {"minus": 1} if tick >= 3 else {},
                }
            ]
    # (c) One return, no click, one inverse split by the mode: the plus arm annulled
    # into the sink, or restored to the lamp (a one-line event has no sibling line).
    assert [event["event"] for event in events] == ["detector_return", "inverse_split"]
    assert (events[0]["tick"], events[0]["position"], events[0]["family"]) == (3, MARK, "plus")
    assert (events[1]["tick"], events[1]["position"], events[1]["mode"]) == (6, X, mode)
    assert events[1]["annulled"] == ({"plus": (1,), "momentum": (1, 0, 0)} if mode == "annul" else {})
    # (d) The runner records the ledger per completed tick under `audit`, the
    # identity, and the conservation flag true (escaped and annulled are ledger
    # lines, not losses); a second run replays byte for byte.
    path = tmp_path / "audit.json"
    path.write_text(json.dumps(document(mode, body=body)), encoding="utf-8")
    records = []
    for name in ("first", "second"):
        run_initialization(path, tmp_path / name, ticks=TICKS)
        events_text = (tmp_path / name / "events.jsonl").read_text(encoding="utf-8")
        metadata = json.loads((tmp_path / name / "run.json").read_text(encoding="utf-8"))
        metadata.pop("elapsed_seconds")
        records.append((events_text, metadata))
    (first_events, first_run), (second_events, second_run) = records
    assert first_events == second_events and first_run == second_run
    assert first_run["ray_event_audit"] == RAY_EVENT_AUDIT == "ray-event-audit-v1"
    assert first_run["audit"] == as_json(ledgers)
    assert first_run["conserved_at_every_completed_tick"]
    assert first_run["accounting_balanced_at_every_completed_tick"]
    assert first_run["completed_ticks"] == TICKS and audit_failure(first_run["audit"]) is None
    assert first_run["external_body_totals"] == as_json(ledgers[-1]["bodies"]["sink"])
    assert first_run["detector_mark_totals"] == as_json(ledgers[-1]["marks"]["counter"])
    assert first_run["detector_absorb"] == "detector-absorb-v1"
    # (e) A record altered by hand after the run, one ray's charge at the tick of
    # the return, is reported by tick and line from the integers alone.
    corrupted = deepcopy(first_run["audit"])
    corrupted[2]["charge"]["plus"]["current"] += 1
    assert audit_failure(corrupted) == {"tick": 3, "readout": "charge", "line": "plus"}
    corrupted = deepcopy(first_run["audit"])
    corrupted[8]["fields"]["G"]["escaped"] = [15]
    assert audit_failure(corrupted) == {"tick": 9, "readout": "fields", "line": "G"}
    # (f) A rule whose outputs change the total charge is rejected at validation.
    with pytest.raises(ValueError, match="would change the total charge"):
        parse_initial_state(document(mode, rules=[CHARGE_BREAKING]))
    # (g) The local conservation audit reads the same charge: on the pair alone
    # (the local audit has no source term for a release) its report agrees with
    # the world ledger summed over the two families at the last tick.
    pair = Simulation(parse_initial_state(document(mode, source=False, conservation=True)))
    for _ in range(TICKS):
        pair.step()
    report = pair.conservation_report()
    ledger = pair.audit()
    assert ledger == expected_ledger(mode, TICKS, source=False)
    assert report["status"] == "passed"
    for key in ("initial", "sourced", "current", "escaped", "annulled"):
        assert report[key]["charge"] == sum(item[key] for item in ledger["charge"].values())
        assert report[key]["energy"] == sum(ledger["fields"][n][key][0] for n in ("plus", "minus"))
        assert report[key]["momentum"] == ledger["fields"]["momentum"][key]
    # (i) The local audit reads every release as a source at its Node, so the whole
    # world (releases, escapes, the return and the inverse split) declares it and
    # passes; the energy sums the four families, the momentum counts every ray.
    if mode == "annul" and not body:
        whole = Simulation(parse_initial_state(document(mode, conservation=True)))
        for _ in range(TICKS):
            whole.step()
        report = whole.conservation_report()
        assert report["status"] == "passed"
        assert report["initial"] == {"energy": 6, "momentum": (0, 0, 0), "charge": 0}
        assert report["sourced"] == {"energy": 20, "momentum": (0, 0, -4), "charge": 0}
        assert report["current"] == {"energy": 4, "momentum": (4, 0, -4), "charge": 0}
        assert report["escaped"] == {"energy": 21, "momentum": (-5, 0, 0), "charge": -1}
        assert report["annulled"] == {"energy": 1, "momentum": (1, 0, 0), "charge": 1}
