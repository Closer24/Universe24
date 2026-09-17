"""Inverse split (inverse-split-v1): a returned ray at its event Node, by return_mode.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Inverse split")
before the first run: a pair lamp at X sending 4 quanta each way on one line,
arm A returned at a marked Node three Links out (seed 3, setting 1/2, one draw,
bit 0), arm B free, and the exact tick table from the return through the
inverse split in each of the three modes.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    DETECTOR_BIT_0,
    DETECTOR_NONE,
    INVERSE_SPLIT,
    RETURN_MODES,
    Ray,
    ray_momentum,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

X = (7, 7, 7)
MARK = (10, 7, 7)
SEED = 3
AMOUNT = 8
SHARE = 4
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
PAIR_PORTS, PAIR_SHARES = 3, (SHARE, SHARE, 0, 0, 0, 0)


def document(mode, ticks=10):
    return {
        "schema_version": 1,
        "model_id": "inverse-split-test-v1",
        "shape": [15, 15, 15],
        "boundary": "periodic",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
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
        # The pair lamp holds exactly the amount it emits, so it fires once at tick 0.
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": AMOUNT, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        # A sweep of two headings from cursor 0: +X and -X, one ray each way.
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 2,
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
                "kerengonen_phase": 0,
            }
        ],
        "seeds": [{"position": list(X), "type": "lamp"}],
        "detectors": [{"position": list(MARK), "setting": [1, 2], "seed": SEED}],
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


def ray(heading, amount, steps, outbound, phase, bit, ports, shares):
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        advance=-1,
        wait=0,
        interaction_delay=0,
        steps=steps,
        outbound=outbound,
        event_ports=ports,
        event_shares=shares,
        detector=bit,
    )


def arm_a(tick):
    """Arm A's ray after tick t: out to the mark, returned there, back at X at tick 6."""
    if tick <= 2:
        return ((7 + tick, 7, 7), ray(0, SHARE, tick, 1, tick, DETECTOR_NONE, PAIR_PORTS, PAIR_SHARES))
    if tick <= 6:
        back = 6 - tick
        return ((7 + back, 7, 7), ray(1, SHARE, back, 0, back, DETECTOR_BIT_0, PAIR_PORTS, PAIR_SHARES))
    return None


def arm_b(tick):
    """Arm B's ray after tick t: one Link per tick along -X, free, around the torus."""
    return (
        ((7 - tick) % 15, 7, 7),
        ray(1, SHARE, tick, 1, tick % 8, DETECTOR_NONE, PAIR_PORTS, PAIR_SHARES),
    )


def transmission(tick):
    """The transmission after tick t >= 7: a new event ray on arm B's line with arm A's
    phase at X (0), its bit and the one Port transmitted to."""
    steps = tick - 6
    return (
        (7 - steps, 7, 7),
        ray(1, SHARE, steps, 1, steps, DETECTOR_BIT_0, 1 << 1, (0, SHARE, 0, 0, 0, 0)),
    )


def expected_rays(mode, tick):
    rays = [arm_b(tick)]
    if tick <= 6:
        rays.append(arm_a(tick))
    elif mode != "annul":
        rays.append(transmission(tick))
    return sorted(rays)


def rays_in(world):
    return sorted(
        (node.position, r) for node in world.inventory_view().nodes for rays in node.rays for r in rays
    )


def lamp(world):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == 0
    )


@pytest.mark.parametrize("mode", RETURN_MODES)
def test_a_returned_ray_performs_the_inverse_split_by_the_return_mode(mode, tmp_path):
    initial = parse_initial_state(document(mode))
    assert initial.return_mode == mode
    definition = initial.spatial_fields[0]
    events = []
    world = Simulation(
        initial,
        observer=lambda event: (
            events.append(event)
            if event["event"] in ("inverse_split", "detector_return", "detector_click")
            else None
        ),
    )
    annul = mode == "annul"
    for tick in range(1, 11):
        world.step()
        split = tick >= 7
        # (a), (b) The rays of the world follow the pinned table: arm A out, returned
        # and back at X at tick 6; arm B free; from tick 7 the transmission on arm
        # B's line in siblings and straight, six Links behind B, nothing in annul.
        assert rays_in(world) == expected_rays(mode, tick)
        # (c) The lamp keeps nothing of the returned share: the restore and the
        # funding of the transmission in one interval leave it 0 quanta, with the
        # recoil of the transmission in siblings and straight and none in annul.
        assert lamp(world) == {
            "quanta": (0,),
            "momentum": (8, 0, 0) if split and not annul else (0, 0, 0),
        }
        # (d) Totals, the annulled sink, the spatial accounting and the conservation
        # report are exact at every tick: initial = current + escaped + annulled.
        gone = SHARE if split and annul else 0
        assert world.totals() == {"quanta": (AMOUNT - gone,), "momentum": (-gone, 0, 0)}
        assert world.annulled_totals() == {"quanta": (gone,), "momentum": (gone, 0, 0)}
        assert world.escaped_totals() == {"quanta": (0,), "momentum": (0, 0, 0)}
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert report["annulled"] == {"energy": gone, "momentum": (gone, 0, 0)}
        accounting = world.spatial_accounting()
        assert all(item["balanced"] for item in accounting.values())
        assert accounting["quanta"]["annulled"] == (gone,)
        in_flight = [0, 0, 0]
        for node in world.inventory_view().nodes:
            for rays in node.rays:
                for axis, value in enumerate(ray_momentum(rays, definition)):
                    in_flight[axis] += value
        assert tuple(in_flight) == (
            (-8, 0, 0) if split and not annul else (-4, 0, 0) if split else (0, 0, 0)
        )
    # (e) One return, no click, and exactly one inverse split at X, in the cycle
    # labelled 6 (the cycle whose packets arrive at tick 7, as the lamp's emission
    # cycle is labelled 0).
    assert [event["event"] for event in events] == ["detector_return", "inverse_split"]
    assert events[0] == {
        "event": "detector_return",
        "tick": 3,
        "position": MARK,
        "port": 1,
        "family": "quanta",
        "amount": SHARE,
    }
    assert events[1] == {
        "event": "inverse_split",
        "tick": 6,
        "position": X,
        "family": "quanta",
        "mode": mode,
        "ports": () if annul else (1,),
        "amounts": () if annul else (SHARE,),
        "amount": SHARE,
        "bit": 0,
        "restored": True,
        "annulled": {"quanta": (SHARE,), "momentum": (SHARE, 0, 0)} if annul else {},
    }
    # (f) The runner records the identity and the mode, the sink and the conservation
    # line, and replays byte for byte.
    path = tmp_path / "split.json"
    path.write_text(json.dumps(document(mode)), encoding="utf-8")
    records = []
    for name in ("first", "second"):
        run_initialization(path, tmp_path / name, ticks=10)
        events_text = (tmp_path / name / "events.jsonl").read_text(encoding="utf-8")
        metadata = json.loads((tmp_path / name / "run.json").read_text(encoding="utf-8"))
        metadata.pop("elapsed_seconds")
        records.append((events_text, metadata))
    (first_events, first_run), (second_events, second_run) = records
    assert first_events == second_events and first_run == second_run
    recorded = [json.loads(line) for line in first_events.splitlines()]
    assert [event for event in recorded if event["event"] == "inverse_split"] == [
        json.loads(json.dumps(events[1]))
    ]
    assert first_run["inverse_split"] == INVERSE_SPLIT == "inverse-split-v1"
    assert first_run["return_mode"] == mode
    assert first_run["detector_return"] == "detector-return-v1"
    assert first_run["annulled_totals"] == {
        "quanta": [SHARE if annul else 0],
        "momentum": [SHARE if annul else 0, 0, 0],
    }
    assert first_run["accounting_balanced_at_every_completed_tick"]
    assert first_run["conserved_at_every_completed_tick"] == (not annul)
    assert first_run["final_totals"] == {
        "quanta": [SHARE if annul else AMOUNT],
        "momentum": [-SHARE if annul else 0, 0, 0],
    }
    # An unknown mode is rejected before a world exists.
    with pytest.raises(ValueError, match="return_mode"):
        parse_initial_state(document("none"))
