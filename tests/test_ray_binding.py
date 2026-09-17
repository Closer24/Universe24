"""Binding and gravity by delay (ray-binding-v1, Highlights 3.4 and 3.28): a rule
without outputs assigning delay 1 binds its participants as a bound group that
stays at the Node, ticks every interval, advances each phase by its rest rate and
releases its field on all six headings; an earlier outputs rule that names a bound
participant and an arriving ray unbinds it; a binding rule's `ray_delay` delays
every departure from the Node; a light ray meeting a field ray is delayed by a
declared table per Port and turns toward the mass over several Nodes, the field
ray returning reversed; G_eff x N^2 is one integer over four phase widths.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Ray binding") before
the first run.
"""

import json
from fractions import Fraction

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import RAY_BINDING, Ray, bound_group, ray_merge_key
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
CENTER = (10, 10, 10)
# The two n lamps whose rays meet at the center after tick 1.
PAIR = (((9, 10, 10), "n", 8, 0), ((11, 10, 10), "n", 8, 1))
IONIZE = {
    "name": "ionize",
    "participants": [{"type": "n"}, {"type": "n"}, {"type": "x"}],
    "outputs": [
        {"field": "n", "amount": {"of": 0}, "heading": 2, "phase": {"of": 0}},
        {"field": "n", "amount": {"of": 1}, "heading": 3, "phase": {"of": 1}},
        {"field": "x", "amount": {"of": 2}, "heading": "same", "input": 2},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}
# Gravity as bending by delay: the light keeps its amount and phase and is delayed
# by the field ray's amount times the table entry of the Port the field ray came
# through; the field ray returns reversed as the recoil.
GRAVITY = {
    "name": "gravity",
    "participants": [{"type": "light"}, {"type": "G"}],
    "outputs": [
        {
            "field": "light",
            "amount": {"of": 0},
            "heading": "same",
            "phase": "same",
            "delay": {"of": 1, "table": [4, 4, 4, 4, 4, 4], "per": 1},
        },
        {"field": "G", "amount": {"of": 1}, "heading": "reversed", "input": 1},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def bind(ray_delay=None):
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
    if ray_delay is not None:
        rule["ray_delay"] = ray_delay
    return rule


def field(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, advance, bits, slots, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": bits,
        "kerengonen": {"phase_advance": advance},
    } | extra


def document(lamps, rules, bits=3, rate=1, ticks=12):
    """The board: `lamps` are (position, family, amount, heading index)."""
    families = ("n", "G", "light", "x", "p")
    return {
        "schema_version": 1,
        "model_id": "ray-binding-test-v1",
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
        "fields": [field(name) for name in families],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": [family],
                "defaults": {family: amount},
                "transport": {"mode": "hold"},
            }
            for index, (_, family, amount, _) in enumerate(lamps)
        ],
        "spatial_fields": [
            ray_field("n", rate, bits, 8),
            ray_field("G", 0, bits, 16, field_of="n", release=[1, 4]),
            ray_field("light", 0, bits, 8),
            ray_field("x", 0, bits, 8),
            ray_field("p", 0, bits, 8),
        ],
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": family,
                "amount": amount,
                "denominator": 1,
                "source": False,
                "heading": HEADINGS[heading],
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


def bundles(world, position):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return () if node is None or not node.rays else node.rays


def rays_at(world, position, family):
    """The resident rays of one family at a Node, in merge-key order."""
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = bundles(world, position)
    return sorted(node[index], key=ray_merge_key) if node else []


def positions_of(world, family):
    return {n.position for n in world.inventory_view().nodes if rays_at(world, n.position, family)}


def ray(heading, amount, phase, steps, mask, shares, lag=(0, 0, 0), delay=0):
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        interaction_delay=delay,
        steps=steps,
        event_ports=mask,
        event_shares=shares,
        lag=lag,
    )


def held(phase):
    """The bound pair after its tick: both at their event Node, one event on both Ports."""
    return [ray(0, 8, phase, 0, 3, (8, 8, 0, 0, 0, 0)), ray(1, 8, phase, 0, 3, (8, 8, 0, 0, 0, 0))]


def group_entry(phase, ray_delay=0):
    return [
        {
            "position": CENTER,
            "families": ["n", "n"],
            "amounts": [8, 8],
            "phases": [phase, phase],
            "ray_delay": ray_delay,
        }
    ]


def balanced(world):
    return all(item["balanced"] for item in world.spatial_accounting().values())


def light_ray(steps, mask=1, shares=(6, 0, 0, 0, 0, 0), lag=(0, 0, 0)):
    return ray(0, 6, 0, steps, mask, shares, lag)


RECOIL = ((10, 13, 10), (10, 12, 10), (10, 11, 10), CENTER, (10, 9, 10))
TURN = ((11, 14, 10), (11, 13, 10), (11, 12, 10), (12, 12, 10), (13, 12, 10))
LAGS = ((0, -16, 0), (0, -8, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))


@pytest.mark.parametrize("case", ["binding", "unbinding", "ray_delay", "gravity", "criterion"])
def test_a_bound_group_ticks_releases_unbinds_delays_and_bends_light_by_delay(tmp_path, case):
    if case == "binding":
        # (a) Two n rays meet and the delay-1 rule binds them: the group stays,
        # ticks every interval, each phase advances once per interval, the group
        # releases its field on all six headings every interval, totals exact.
        world = Simulation(parse_initial_state(document(PAIR, [bind()], ticks=6)))
        for tick in range(1, 7):
            world.step()
            assert world.totals()["n"] == (16,) and world.totals()["G"] == (24 * (tick - 1),)
            assert world.source_totals()["n"] == (0,)
            assert world.source_totals()["G"] == (24 * (tick - 1),)
            assert balanced(world)
            if tick == 1:
                assert rays_at(world, CENTER, "n") == [
                    ray(0, 8, 1, 1, 1, (8, 0, 0, 0, 0, 0)),
                    ray(1, 8, 1, 1, 2, (0, 8, 0, 0, 0, 0)),
                ]
                assert world.snapshot()["bound_groups"] == []
                continue
            assert rays_at(world, CENTER, "n") == held(tick)
            assert positions_of(world, "n") == {CENTER}
            assert bound_group(bundles(world, CENTER)) == tuple((0, r) for r in held(tick))
            assert world.snapshot()["bound_groups"] == group_entry(tick)
            for release in range(2, tick + 1):
                walked, phase = tick - release + 1, release - 1
                for heading, step in enumerate(HEADINGS):
                    at = tuple(c + walked * s for c, s in zip(CENTER, step, strict=True))
                    assert rays_at(world, at, "G") == [ray(heading, 4, phase, walked, 0, (0,) * 6)]
        path = tmp_path / "binding.json"
        path.write_text(json.dumps(document(PAIR, [bind()], ticks=6)), encoding="utf-8")
        run_initialization(path, tmp_path / "out", ticks=6)
        metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
        assert metadata["ray_binding"] == RAY_BINDING == "ray-binding-v1"
        assert metadata["final_totals"] == {"n": [16], "G": [120], "light": [0], "x": [0], "p": [0]}
        ticks = [
            json.loads(line)
            for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        ticks = [event for event in ticks if event["event"] == "bound_tick"]
        # A Node's cycle record carries the tick the cycle started at; the cycle of
        # tick 1 is the meeting that forms the group, the later ones its ticks.
        assert [event["tick"] for event in ticks] == [2, 3, 4, 5]
        assert all(
            event["families"] == ["n", "n"]
            and event["amounts"] == [8, 8]
            and event["phases"] == [event["tick"] + 1] * 2
            and event["ray_delay"] == 0
            and tuple(event["position"]) == CENTER
            for event in ticks
        )
        return
    if case == "unbinding":
        # (b) An arriving x ray unbinds the group through the outputs rule declared
        # before the binding rule; the outputs leave as event rays.
        lamps = PAIR + (((10, 6, 10), "x", 3, 2),)
        world = Simulation(parse_initial_state(document(lamps, [IONIZE, bind()], ticks=8)))
        for tick in range(1, 9):
            world.step()
            assert world.totals()["n"] == (16,) and world.totals()["x"] == (3,)
            assert balanced(world)
            if tick <= 4:
                assert world.totals()["G"] == (24 * (tick - 1),)
                assert rays_at(world, (10, 6 + tick, 10), "x") == [
                    ray(2, 3, 0, tick, 4, (0, 0, 3, 0, 0, 0))
                ]
                assert rays_at(world, CENTER, "n") == (
                    held(tick) if tick > 1 else rays_at(world, CENTER, "n")
                )
                assert world.snapshot()["bound_groups"] == (group_entry(tick) if tick > 1 else [])
                continue
            walked = tick - 4
            assert world.totals()["G"] == world.source_totals()["G"] == (72 + 20 * walked,)
            assert rays_at(world, CENTER, "n") == [] and world.snapshot()["bound_groups"] == []
            shares = (0, 0, 11, 8, 0, 0)
            assert rays_at(world, (10, 10 + walked, 10), "n") == [
                ray(2, 8, (4 + walked) & 7, walked, 12, shares)
            ]
            assert rays_at(world, (10, 10 - walked, 10), "n") == [
                ray(3, 8, (4 + walked) & 7, walked, 12, shares)
            ]
            assert rays_at(world, (10, 10 + walked, 10), "x") == [ray(2, 3, 0, walked, 12, shares)]
        return
    if case == "ray_delay":
        # (c) The group's declared ray_delay delays every departure from its Node by
        # the declared count: a p ray of its own layer crossing the Node waits two
        # intervals.
        lamps = PAIR + (((10, 7, 10), "p", 3, 2),)
        world = Simulation(parse_initial_state(document(lamps, [bind(2)], ticks=9)))
        for tick in range(1, 10):
            world.step()
            assert balanced(world)
            if tick > 1:
                assert world.snapshot()["bound_groups"] == group_entry(tick & 7, 2)
            if tick <= 3:
                at, steps, delay = (10, 7 + tick, 10), tick, 2 if tick == 3 else 0
            elif tick <= 5:
                at, steps, delay = CENTER, 3, 5 - tick
            else:
                at, steps, delay = (10, 5 + tick, 10), tick - 2, 0
            assert positions_of(world, "p") == {at}
            assert rays_at(world, at, "p") == [ray(2, 3, 0, steps, 4, (0, 0, 3, 0, 0, 0), delay=delay)]
        world = Simulation(parse_initial_state(document(lamps, [bind()], ticks=4)))
        for _ in range(4):
            world.step()
        assert positions_of(world, "p") == {(10, 11, 10)}
        return
    lamps = PAIR + (((4, 14, 10), "light", 6, 0),)
    if case == "gravity":
        # (d) A light ray passing the group at b = 4 is delayed 16 phase steps on
        # its -Y side by the table, two full intervals at N = 8: it turns toward
        # the group by 2 Links over the next Nodes, and the recoil returns.
        world = Simulation(parse_initial_state(document(lamps, [GRAVITY, bind()], ticks=11)))
        for tick in range(1, 12):
            world.step()
            assert world.totals()["G"] == world.source_totals()["G"] == (24 * (tick - 1),)
            assert world.totals()["light"] == (6,) and world.totals()["n"] == (16,)
            assert balanced(world)
            if tick <= 6:
                assert positions_of(world, "light") == {(4 + tick, 14, 10)}
                assert rays_at(world, (4 + tick, 14, 10), "light") == [light_ray(tick)]
                if tick == 6:
                    assert rays_at(world, (10, 14, 10), "G") == [ray(2, 4, 2, 4, 0, (0,) * 6)]
                continue
            walked = tick - 6
            assert positions_of(world, "light") == {TURN[walked - 1]}
            assert rays_at(world, TURN[walked - 1], "light") == [
                light_ray(walked, 9, (6, 0, 0, 4, 0, 0), LAGS[walked - 1])
            ]
            assert ray(3, 4, 2, walked, 9, (6, 0, 0, 4, 0, 0)) in rays_at(world, RECOIL[walked - 1], "G")
        return
    # (e) The acceptance criterion: G_eff x N^2 over N = 2^8, 2^10, 2^12, 2^16 with
    # the group's mass in phase units the same fraction N / 4 of N.
    products = []
    for bits in (8, 10, 12, 16):
        modulus = 1 << bits
        rate = modulus // 8
        world = Simulation(
            parse_initial_state(document(lamps, [GRAVITY, bind()], bits=bits, rate=rate, ticks=8))
        )
        for _ in range(8):
            world.step()
        assert balanced(world) and world.totals()["G"] == world.source_totals()["G"] == (168,)
        assert positions_of(world, "light") == {(12, 14, 10)}
        (light,) = rays_at(world, (12, 14, 10), "light")
        assert light == light_ray(2, 9, (6, 0, 0, 4, 0, 0), (0, -16, 0))
        mass = 2 * rate
        alpha = Fraction(abs(light.lag[1]), modulus)
        g_eff = alpha * 4 / (4 * mass)
        assert g_eff == Fraction(64, modulus * modulus)
        products.append(g_eff * modulus * modulus)
    assert products == [64, 64, 64, 64]
