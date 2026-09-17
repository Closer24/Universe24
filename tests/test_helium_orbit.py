"""The helium orbit of E8 in isolation on the smallest board: a body of the proton
family releasing its light, which spreads by the catalog's table with the Node-owned
remainder (field-spreading-v1, field-remainder-v1), an electron held at a launcher
body by an output delay and released into that field, turned at every Node by the
momentum-table coupling of ray-momentum-turn-v2 (a push per field ray met, the
recoil returned, the DDA's walk kept through the push), the nucleus transparent to it (phase_plate) and sinking its own
field; the world ledger exact at every tick.

The board is the E8 world's declarations (examples/nature/helium_orbit.json) on a
7^3 lattice at radius 2 with a hold of four intervals, twelve ticks, so that the
launch, the first pushes, the fall and the cage all happen within a few seconds.
The structural expectations are written before the first run and the record's
integers (the pushes, the registers, the sink, the totals) were read from the
first run of this board and pinned then, as docs/TEST_EXPECTATIONS.md ("The
helium orbit") says; re-read under ray-momentum-turn-v2 (the DDA's walk kept
through a push) and unchanged, since at both pushed Nodes the register's -X
component exceeds the banked progress and the same -X Links are taken.
"""

import json

from event_universe.runner import run_initialization

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
SHAPE = 7
CENTER = 3
R = 2
M = 256
D = 749
HOLD = 4
TICKS = 12
NUCLEUS = [CENTER, CENTER, CENTER]
LAUNCHER = [CENTER + R, CENTER - 1, CENTER]
LAMP = [CENTER + R, CENTER - 2, CENTER]
SLOTS = {"electron": 4, "light_of_nucleus": 24, "proton": 2, "launcher": 2}
ENERGY = {"name": "energy", "expression": {"field": "amount"}}


def field(name, components=1, signed=False):
    return {
        "name": name,
        "components": components,
        "units": "quantum" if components == 1 else "quantum times heading",
        "signed": signed,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, advance, charge, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": SLOTS[name],
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": 8,
        "kerengonen": {"phase_advance": advance},
        "charge": charge,
    } | extra


def document():
    """The E8 world on the small board: the same families, rules and bodies."""
    light = ray_field(
        "light_of_nucleus", 0, 0, field_of="proton", release=[1, D], spread=[6, 1, 1, 1, 1, 1]
    )
    return {
        "schema_version": 1,
        "model_id": "helium-orbit-test-v1",
        "shape": [SHAPE, SHAPE, SHAPE],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": TICKS,
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
            field("electron"),
            field("light_of_nucleus"),
            field("proton"),
            field("launcher"),
            field("momentum", 3, True),
        ],
        "disturbance_types": [
            {
                "name": "electron_source",
                "fields": ["electron", "momentum"],
                "defaults": {"electron": M, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            ray_field("electron", 1, -3),
            light,
            ray_field("proton", 0, 3),
            ray_field("launcher", 0, 0),
        ],
        "emissions": [
            {
                "type": "electron_source",
                "field": "electron",
                "amount": M,
                "denominator": 1,
                "source": False,
                "heading": [0, 1, 0],
                "kerengonen_phase": 0,
                "recoil_field": "momentum",
            }
        ],
        "seeds": [{"position": LAMP, "type": "electron_source"}],
        "ray_interactions": [
            {
                "name": "launch",
                "participants": [{"type": "electron"}, {"type": "launcher"}],
                "when": {"op": "eq", "args": [{"field": "phase", "participant": 0}, 1]},
                "outputs": [
                    {
                        "field": "electron",
                        "amount": {"of": 0},
                        "heading": "same",
                        "input": 0,
                        "phase": {"of": 0},
                        "delay": HOLD,
                    },
                    {
                        "field": "launcher",
                        "amount": {"of": 1},
                        "heading": "same",
                        "input": 1,
                        "phase": {"of": 1},
                    },
                ],
                "invariants": [ENERGY],
            },
            {
                "name": "nucleus_turn",
                "participants": [{"type": "electron"}, {"type": "light_of_nucleus"}],
                "momentum_table": {"light_of_nucleus": -1},
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
            },
            {
                "name": "phase_plate",
                "participants": [{"type": "electron"}, {"type": "proton"}],
                "outputs": [
                    {
                        "field": "electron",
                        "amount": {"of": 0},
                        "heading": "same",
                        "input": 0,
                        "phase": {"of": 0, "offset": 0},
                    },
                    {
                        "field": "proton",
                        "amount": {"of": 1},
                        "heading": "same",
                        "input": 1,
                        "phase": {"of": 1},
                    },
                ],
                "invariants": [ENERGY],
            },
        ],
        "external_bodies": [
            {
                "position": NUCLEUS,
                "family": "proton",
                "amount": 1048576,
                "charge": 6,
                "coupling": "phase_plate",
                "momentum_table": {"light_of_nucleus": -1},
            },
            {"position": LAUNCHER, "family": "launcher", "amount": 1, "coupling": "launch"},
        ],
    }


# The Node the electron arrives at, per tick with an arrival: the launcher at tick
# 1, where it is held through tick 5 (no arrival is recorded while it waits), the
# tangent point at tick 6, the fall to the nucleus at tick 8, the cage after.
POSITIONS = {
    1: LAUNCHER,
    6: [5, 3, 3],
    7: [4, 3, 3],
    8: NUCLEUS,
    9: [3, 4, 3],
    10: NUCLEUS,
    11: [3, 4, 3],
    12: NUCLEUS,
}
# The pushes of the first two Nodes, in slot order: (before, after, field amount,
# field heading); the register starts at amount x heading, (0, 256, 0).
PUSHES_6 = [
    ([0, 256, 0], [-785, 256, 0], 785, [1, 0, 0]),
    ([-785, 256, 0], [-743, 256, 0], 42, [-1, 0, 0]),
    ([-743, 256, 0], [-743, 277, 0], 21, [0, -1, 0]),
    ([-743, 277, 0], [-743, 277, -22], 22, [0, 0, 1]),
    ([-743, 277, -22], [-743, 277, 0], 22, [0, 0, -1]),
]
PUSHES_7 = [
    ([-743, 277, 0], [-2142, 277, 0], 1399, [1, 0, 0]),
    ([-2142, 277, 0], [-1357, 277, 0], 785, [-1, 0, 0]),
    ([-1357, 277, 0], [-1357, 233, 0], 44, [0, 1, 0]),
    ([-1357, 233, 0], [-1357, 280, 0], 47, [0, -1, 0]),
    ([-1357, 280, 0], [-1357, 280, -47], 47, [0, 0, 1]),
    ([-1357, 280, -47], [-1357, 280, 0], 47, [0, 0, -1]),
]
# The cage: the nucleus resets the register to (0, 256, 0) (phase_plate assigns
# the heading), the +Y line's whole ray pushes it back; the register after the
# pushes of ticks 9 and 11 and their counts.
CAGE = {9: (7, [-17, -1036, 0]), 11: (11, [-8, -1099, 0])}
# The world ledger's light and momentum lines and the bodies' momentum after
# ticks 5, 6, 8 and 12: sourced, current, escaped, absorbed; every line balanced.
LIGHT = {
    5: (41970, 34466, 3411, 4093),
    6: (50364, 38801, 6116, 5447),
    8: (67152, 44680, 13109, 9363),
    12: (100728, 51215, 31967, 17546),
}
MOMENTUM = {5: [0, 0, 0], 6: [0, 0, 0], 8: [-1357, 24, 0], 12: [-8, -1355, 0]}
BODY_MOMENTUM = {5: [0, 0, 0], 6: [0, 0, 0], 8: [1197, 3, 0], 12: [1169, 2398, 0]}


def test_the_electron_is_launched_into_the_spreading_field_turned_and_caged(tmp_path):
    path = tmp_path / "world.json"
    path.write_text(json.dumps(document()), encoding="utf-8")
    run_initialization(path, tmp_path / "out")
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    events = [
        json.loads(line)
        for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert metadata["status"] == "completed" and metadata["completed_ticks"] == TICKS
    assert metadata["ray_momentum_turn"] == "ray-momentum-turn-v2"
    assert metadata["field_spreading"] == "field-spreading-v1"
    assert metadata["field_remainder"] == "field-remainder-v1"
    assert metadata["external_body"] == "external-body-v1"
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["accounting_balanced_at_every_completed_tick"]
    # The electron's Node after each tick, from the arrivals of the record.
    positions = {}
    for event in events:
        if event["event"] == "spatial_received":
            for readings in event["received_fields"]:
                if readings and readings.get("electron", [0])[0]:
                    positions[event["tick"]] = event["position"]
    assert positions == POSITIONS
    # The pushes: every field ray met at the Node in slot order, the register
    # before and after, no push while held, none at the nucleus (its sink takes
    # the field before the meeting).
    pushes = {}
    for event in events:
        if event["event"] == "ray_push":
            assert event["family"] == "electron" and event["amount"] == M
            assert event["field"] == "light_of_nucleus"
            assert event["position"] == POSITIONS[event["tick"]]
            pushes.setdefault(event["tick"], []).append(
                (event["before"], event["after"], event["field_amount"], event["field_heading"])
            )
    assert sorted(pushes) == [6, 7, 9, 11]
    assert pushes[6] == PUSHES_6
    assert pushes[7] == PUSHES_7
    for tick, (count, register) in CAGE.items():
        assert len(pushes[tick]) == count
        assert pushes[tick][0][0] == [0, 256, 0]
        assert pushes[tick][-1][1] == register
    # The ledger: light released, held (the registers included), escaped and sunk
    # add up; the momentum line carries the pushes and the reversals; the bodies'
    # line the nucleus's recoils; every line balanced at every tick.
    audit = {line["tick"]: line for line in metadata["audit"]}
    assert all(line["balanced"] for line in audit.values()) and len(audit) == TICKS
    for tick, (sourced, current, escaped, absorbed) in LIGHT.items():
        light = audit[tick]["fields"]["light_of_nucleus"]
        assert (light["sourced"], light["current"], light["escaped"], light["absorbed"]) == (
            [sourced],
            [current],
            [escaped],
            [absorbed],
        )
        assert sourced == current + escaped + absorbed
        momentum = audit[tick]["fields"]["momentum"]
        assert momentum["sourced"] == momentum["current"] == MOMENTUM[tick]
        assert audit[tick]["bodies"]["momentum"] == BODY_MOMENTUM[tick]
        assert audit[tick]["fields"]["electron"]["current"] == [M]
    assert metadata["external_body_totals"]["light_of_nucleus"] == [LIGHT[12][3]]
    assert metadata["external_bodies"][0]["final"]["momentum"] == BODY_MOMENTUM[12]
    assert metadata["external_bodies"][0]["positions"][-1] == [TICKS, *NUCLEUS]
    assert metadata["final_totals"]["electron"] == [M]
    assert metadata["escaped_totals"]["electron"] == [0]
