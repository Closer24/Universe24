"""Bound groups that move (bound-group-motion-v1, Highlights 3.4, 3.14, 3.16, 3.19
and 3.28): a bound group carries a momentum register and three per-axis
accumulators, set at its formation as the sum of amount x heading of its rays;
each interval it is bound the accumulators add the momentum and the whole group
departs one Link through the Port of the first axis whose accumulator has reached
its content, as the external body steps, carrying its rays with their phases,
its register and its clock; a field ray of a family the binding rule's
`momentum_table` names pushes the group by sign x amount x heading and returns
reversed; the world ledger reads a group by its register; a group leaving an
open boundary is booked as escaped with its content and momentum; a head-on
pair at rest never moves and runs byte-identically to ray-binding-v1.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Bound group motion")
before the first run.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import BOUND_GROUP_MOTION, Ray, ray_merge_key
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
CENTER = (10, 10, 10)
ZERO = (0, 0, 0)


def bind(table=None):
    rule = {
        "name": "bind",
        "participants": [{"type": "n"}, {"type": "n"}],
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
    if table is not None:
        rule["momentum_table"] = table
    return rule


def field(name, components=1, signed=False):
    return {
        "name": name,
        "components": components,
        "units": "quantum" if components == 1 else "quantum times heading",
        "signed": signed,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, advance, slots, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": 3,
        "kerengonen": {"phase_advance": advance},
    } | extra


def document(lamps, rules, released=True, ticks=12):
    """The board: `lamps` are (position, family, amount, heading index); every
    emission keeps its recoil on the lamp's `momentum` vector."""
    families = ("n",) + (("G",) if released else ()) + ("f",)
    return {
        "schema_version": 1,
        "model_id": "bound-group-motion-test-v1",
        "shape": [21, 21, 21],
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
        "fields": [field(name) for name in families] + [field("momentum", 3, True)],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": [family, "momentum"],
                "defaults": {family: amount, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for index, (_, family, amount, _) in enumerate(lamps)
        ],
        "spatial_fields": [ray_field("n", 1, 8)]
        + ([ray_field("G", 0, 16, field_of="n", release=[1, 4])] if released else [])
        + [ray_field("f", 0, 8)],
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": family,
                "amount": amount,
                "denominator": 1,
                "source": False,
                "heading": HEADINGS[heading],
                "recoil_field": "momentum",
                "kerengonen_phase": 0,
            }
            for index, (_, family, amount, heading) in enumerate(lamps)
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _, _) in enumerate(lamps)
        ],
        "ray_interactions": list(rules),
    }


def rays_at(world, position, family):
    """The resident rays of one family at a Node, in merge-key order."""
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return sorted(node.rays[index], key=ray_merge_key) if node is not None and node.rays else []


def positions_of(world, family):
    return {n.position for n in world.inventory_view().nodes if rays_at(world, n.position, family)}


def ray(heading, amount, phase, steps, mask, shares):
    return Ray(
        heading, (0, 0, 0), amount, phase=phase, steps=steps, event_ports=mask, event_shares=shares
    )


def held(amounts, phase):
    """The bound pair after its tick: at its Node, one event on both Ports."""
    shares = (amounts[0], amounts[1], 0, 0, 0, 0)
    return [ray(0, amounts[0], phase, 0, 3, shares), ray(1, amounts[1], phase, 0, 3, shares)]


def group_entry(position, amounts, phase, momentum, accumulators):
    return [
        {
            "position": position,
            "families": ["n", "n"],
            "amounts": list(amounts),
            "phases": [phase, phase],
            "ray_delay": 0,
            "momentum": momentum,
            "accumulators": accumulators,
        }
    ]


def momentum_line(world):
    return world.audit()["fields"]["momentum"]


def balanced(world):
    ledger = world.audit()
    return ledger["balanced"] and all(item["balanced"] for item in world.spatial_accounting().values())


def steps_of(events):
    return [
        (
            e["tick"],
            tuple(e["position"]),
            e["port"],
            e["arrival_tick"],
            tuple(e["momentum"]),
            tuple(e["accumulators"]),
            e["content"],
        )
        for e in events
        if e["event"] == "bound_group_step"
    ]


def run(tmp_path, raw, ticks):
    path = tmp_path / "world.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=ticks)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    lines = (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    state = json.loads((tmp_path / "out" / "state.json").read_text(encoding="utf-8"))
    return metadata, [json.loads(line) for line in lines], state


@pytest.mark.parametrize("case", ["uniform", "push", "escape", "rest", "rejected"])
def test_a_bound_group_moves_by_its_register_is_pushed_by_a_field_ray_and_escapes(tmp_path, case):
    events = []
    if case == "uniform":
        # (a) A group of content 8 with register (4, 0, 0) steps one Link every
        # two intervals for 12 intervals: positions, accumulators and phases
        # pinned tick by tick, bound_tick continuing, the ledger exact.
        lamps = (((9, 10, 10), "n", 6, 0), ((11, 10, 10), "n", 2, 1))
        raw = document(lamps, [bind()])
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 13):
            world.step()
            assert world.totals()["n"] == (8,) and world.escaped_totals()["n"] == (0,)
            sourced = 6 * (t - 1) - max(0, (t - 2) // 2)
            assert world.source_totals()["G"] == (sourced,)
            assert world.escaped_totals()["G"] == ((6,) if t == 12 else (0,))
            assert world.totals()["G"] == (sourced - (6 if t == 12 else 0),)
            line = momentum_line(world)
            assert (line["initial"], line["sourced"], line["current"]) == (ZERO, ZERO, ZERO)
            assert balanced(world)
            if t == 1:
                assert rays_at(world, CENTER, "n") == [
                    ray(0, 6, 1, 1, 1, (6, 0, 0, 0, 0, 0)),
                    ray(1, 2, 1, 1, 2, (0, 2, 0, 0, 0, 0)),
                ]
                assert world.snapshot()["bound_groups"] == []
                continue
            at = (10 + (t - 2) // 2, 10, 10)
            accumulators = (4 * ((t - 2) % 2), 0, 0)
            assert positions_of(world, "n") == {at}
            assert rays_at(world, at, "n") == held((6, 2), t & 7)
            assert world.snapshot()["bound_groups"] == group_entry(
                at, (6, 2), t & 7, (4, 0, 0), accumulators
            )
        assert steps_of(events) == [
            (tick, (10 + (tick - 3) // 2, 10, 10), 0, tick + 1, (4, 0, 0), ZERO, 8)
            for tick in (3, 5, 7, 9, 11)
        ]
        ticks = [e for e in events if e["event"] == "bound_tick"]
        assert [(e["tick"], tuple(e["position"])) for e in ticks] == [
            (tick, (10 + (tick - 2) // 2, 10, 10)) for tick in range(2, 12)
        ]
        assert all(
            e["families"] == ["n", "n"]
            and e["amounts"] == [6, 2]
            and e["phases"] == [(e["tick"] + 1) & 7] * 2
            and e["ray_delay"] == 0
            for e in ticks
        )
        metadata, records, state = run(tmp_path, raw, 12)
        assert metadata["bound_group_motion"] == BOUND_GROUP_MOTION == "bound-group-motion-v1"
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["accounting_balanced_at_every_completed_tick"]
        assert steps_of(records) == steps_of(events)
        assert state["bound_groups"][0]["momentum"] == [4, 0, 0]
        return
    if case == "push":
        # (b) A group at rest met by a G ray of amount 2 from -x with table sign -1
        # gains (-2, 0, 0) and moves toward the source one Link every four
        # intervals; the field ray's return pinned.
        lamps = (((9, 10, 10), "n", 4, 0), ((11, 10, 10), "n", 4, 1), ((5, 10, 10), "G", 2, 0))
        raw = document(lamps, [bind({"G": -1})], ticks=14)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 15):
            world.step()
            assert world.totals()["n"] == (8,)
            expected_g = (
                2 + 12 * (t - 1) - (2 if t >= 10 else 0) - (2 if t >= 14 else 0) - 12 * max(0, t - 11)
            )
            assert world.totals()["G"] == (expected_g,)
            line = momentum_line(world)
            sourced = (0 if t <= 5 else -6 if t <= 9 else -4 if t <= 13 else -2, 0, 0)
            assert line["sourced"] == sourced and line["current"] == sourced
            assert line["escaped"] == ZERO and line["initial"] == ZERO
            assert balanced(world)
            if t <= 5:
                # The lamp's ray crosses the group's own released G rays on its way.
                assert ray(0, 2, 0, t, 1, (2, 0, 0, 0, 0, 0)) in rays_at(world, (5 + t, 10, 10), "G")
                if t > 1:
                    assert world.snapshot()["bound_groups"] == group_entry(CENTER, (4, 4), t, ZERO, ZERO)
                continue
            at = (10 - (t - 6) // 4, 10, 10)
            accumulators = (-2 * ((t - 6) % 4), 0, 0)
            assert positions_of(world, "n") == {at}
            assert rays_at(world, at, "n") == held((4, 4), t & 7)
            assert world.snapshot()["bound_groups"] == group_entry(
                at, (4, 4), t & 7, (-2, 0, 0), accumulators
            )
            # The recoil walks -X beside the release of the cycle it left in.
            assert ray(1, 2, 0, t - 5, 2, (0, 2, 0, 0, 0, 0)) in rays_at(world, (15 - t, 10, 10), "G")
        assert steps_of(events) == [
            (9, CENTER, 1, 10, (-2, 0, 0), ZERO, 8),
            (13, (9, 10, 10), 1, 14, (-2, 0, 0), ZERO, 8),
        ]
        metadata, records, _ = run(tmp_path, raw, 14)
        assert metadata["bound_group_motion"] == BOUND_GROUP_MOTION
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["final_totals"]["G"] == [118]
        assert steps_of(records) == steps_of(events)
        return
    if case == "escape":
        # (c) A group pushed to (3, 0, 0) with content 8 reaches the open boundary
        # and escapes as a group: escaped totals and momentum pinned.
        lamps = (((17, 10, 10), "n", 4, 0), ((19, 10, 10), "n", 4, 1), ((20, 10, 10), "f", 3, 1))
        raw = document(lamps, [bind({"f": -1})], released=False, ticks=11)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        positions = {2: 18, 3: 18, 4: 18, 5: 18, 6: 19, 7: 19, 8: 19, 9: 20, 10: 20}
        # After tick t: the step decision of the push cycle reads the register
        # before the push, so the accumulator starts adding 3 from the cycle of tick 3.
        accumulators = {2: 0, 3: 0, 4: 3, 5: 6, 6: 1, 7: 4, 8: 7, 9: 2, 10: 5}
        for t in range(1, 12):
            world.step()
            line = momentum_line(world)
            assert line["sourced"] == ((9, 0, 0) if t >= 3 else ZERO)
            assert balanced(world)
            if t == 1:
                assert rays_at(world, (19, 10, 10), "f") == [ray(1, 3, 0, 1, 2, (0, 3, 0, 0, 0, 0))]
                continue
            if t == 2:
                assert rays_at(world, (18, 10, 10), "f") == [ray(1, 3, 0, 2, 2, (0, 3, 0, 0, 0, 0))]
            elif t <= 4:
                assert rays_at(world, (16 + t, 10, 10), "f") == [
                    ray(0, 3, 0, t - 2, 1, (3, 0, 0, 0, 0, 0))
                ]
            else:
                assert positions_of(world, "f") == set()
                assert world.escaped_totals()["f"] == (3,)
            if t <= 10:
                at = (positions[t], 10, 10)
                assert positions_of(world, "n") == {at}
                assert world.snapshot()["bound_groups"] == group_entry(
                    at, (4, 4), t & 7, (3, 0, 0) if t >= 3 else ZERO, (accumulators[t], 0, 0)
                )
                assert world.totals()["n"] == (8,) and world.escaped_totals()["n"] == (0,)
                assert line["escaped"] == ((3, 0, 0) if t >= 5 else ZERO)
            else:
                assert positions_of(world, "n") == set()
                assert world.snapshot()["bound_groups"] == []
                assert world.totals()["n"] == (0,) and world.escaped_totals()["n"] == (8,)
                assert line["escaped"] == (6, 0, 0) and line["current"] == (3, 0, 0)
        assert steps_of(events) == [
            (5, (18, 10, 10), 0, 6, (3, 0, 0), (1, 0, 0), 8),
            (8, (19, 10, 10), 0, 9, (3, 0, 0), (2, 0, 0), 8),
            (10, (20, 10, 10), 0, 11, (3, 0, 0), ZERO, 8),
        ]
        escaped = [e for e in events if e["event"] == "spatial_escaped" and "bound_group" in e]
        assert len(escaped) == 1
        assert (escaped[0]["tick"], tuple(escaped[0]["position"]), escaped[0]["port"]) == (
            11,
            (20, 10, 10),
            0,
        )
        assert escaped[0]["escaped"] == {"n": (8,), "momentum": (3, 0, 0)}
        assert escaped[0]["bound_group"] == {
            "families": ["n", "n"],
            "amounts": [4, 4],
            "content": 8,
            "momentum": (3, 0, 0),
        }
        metadata, _, _ = run(tmp_path, raw, 11)
        assert metadata["bound_group_motion"] == BOUND_GROUP_MOTION
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["escaped_totals"] == {"n": [8], "f": [3], "momentum": [6, 0, 0]}
        assert metadata["final_totals"] == {"n": [0], "f": [0], "momentum": [3, 0, 0]}
        return
    if case == "rest":
        # (d) The head-on pair of ray-binding-v1 keeps (0, 0, 0) and never moves:
        # the events and the run record are those of feature 8.
        lamps = (((9, 10, 10), "n", 8, 0), ((11, 10, 10), "n", 8, 1))
        raw = document(lamps, [bind()], ticks=6)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 7):
            world.step()
            assert balanced(world)
            if t > 1:
                assert world.snapshot()["bound_groups"] == group_entry(CENTER, (8, 8), t, ZERO, ZERO)
                assert rays_at(world, CENTER, "n") == held((8, 8), t)
        assert steps_of(events) == []
        ticks = [e for e in events if e["event"] == "bound_tick"]
        assert [e["tick"] for e in ticks] == [2, 3, 4, 5]
        assert all(
            set(e) == {"event", "tick", "position", "families", "amounts", "phases", "ray_delay"}
            for e in ticks
        )
        metadata, records, state = run(tmp_path, raw, 6)
        assert "bound_group_motion" not in metadata
        assert metadata["conserved_at_every_completed_tick"]
        assert [e["event"] for e in records if e["event"].startswith("bound")] == ["bound_tick"] * 4
        assert state["bound_groups"] == [
            {
                "position": list(CENTER),
                "families": ["n", "n"],
                "amounts": [8, 8],
                "phases": [6, 6],
                "ray_delay": 0,
                "momentum": [0, 0, 0],
                "accumulators": [0, 0, 0],
            }
        ]
        return
    # (e) Malformed momentum tables are rejected at initialization.
    lamps = (((9, 10, 10), "n", 4, 0), ((11, 10, 10), "n", 4, 1))
    outputs = {
        "name": "bounce",
        "participants": [{"type": "n"}, {"type": "f"}],
        "outputs": [
            {"field": "n", "amount": {"of": 0}, "heading": "reversed"},
            {"field": "f", "amount": {"of": 1}, "heading": "reversed", "input": 1},
        ],
        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
        "momentum_table": {"G": -1},
    }
    for rules, message in (
        ([outputs], "declared by a binding rule"),
        ([bind({"n": -1})], "families it does not bind"),
        ([bind({"light": -1})], "momentum_table"),
        ([bind({"G": 2})], "attraction"),
        (
            [bind({"G": -1}) | {"assignments": [{"participant": 0, "field": "phase", "expression": 0}]}],
            "families it does not bind",
        ),
    ):
        with pytest.raises(ValueError, match=message):
            parse_initial_state(document(lamps, rules))
