"""Gravity by delay (ray-binding-v1, Highlights 3.28): a light ray meeting a field
ray is delayed by a declared table per Port and turns toward the mass over several
Nodes, the field ray returning reversed; G_eff x N^2 is one integer over four phase
widths. The mass is resident content, a record holding stock of the family whose
field `G` is, releasing on all six headings every interval (released-field-v1).

The held form of this identity (a rule without outputs holding its participants,
its `ray_delay` wait, `bound_group` and `bound_groups`) was removed on 2026-09-17
by loop-binding-v1: binding is a periodic orbit of the ordinary meeting rule
(`test_loop_binding.py`), and the cases `binding`, `unbinding` and `ray_delay`
went with it.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Ray binding") before
the first run.
"""

from fractions import Fraction

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import RAY_BINDING, Ray, ray_merge_key
from event_universe.initialization import parse_initial_state

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
CENTER = (10, 10, 10)
# The mass: a record holding 16 of `n` at the center, never emitting, whose stock
# releases floor(16 / 4) = 4 of G on every heading every interval.
MASS = 16
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
    """The board: `lamps` are (position, family, amount, heading index); the mass
    record holds `MASS` of `n` at the center and emits nothing."""
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
            {"name": "mass", "fields": ["n"], "defaults": {"n": MASS}, "transport": {"mode": "hold"}}
        ]
        + [
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
        "seeds": [{"position": list(CENTER), "type": "mass"}]
        + [
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


def balanced(world):
    return all(item["balanced"] for item in world.spatial_accounting().values())


def light_ray(steps, mask=1, shares=(6, 0, 0, 0, 0, 0), lag=(0, 0, 0)):
    return ray(0, 6, 0, steps, mask, shares, lag)


LAMPS = (((4, 14, 10), "light", 6, 0),)
RECOIL = ((10, 13, 10), (10, 12, 10), (10, 11, 10), CENTER, (10, 9, 10))
TURN = ((11, 14, 10), (11, 13, 10), (11, 12, 10), (12, 12, 10), (13, 12, 10))
LAGS = ((0, -16, 0), (0, -8, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))


@pytest.mark.parametrize("case", ["gravity", "criterion"])
def test_light_bends_by_delay_at_the_field_of_a_mass(case):
    if case == "gravity":
        # (d) A light ray passing the mass at b = 4 is delayed 16 phase steps on
        # its -Y side by the table, two full intervals at N = 8: it turns toward
        # the mass by 2 Links over the next Nodes, and the recoil returns through
        # the mass's Node, which absorbs nothing.
        world = Simulation(parse_initial_state(document(LAMPS, [GRAVITY], ticks=11)))
        assert RAY_BINDING == "ray-binding-v1"
        for tick in range(1, 12):
            world.step()
            # The mass releases 24 of G every interval from the cycle of tick 0;
            # the first releases reach the open boundary at tick 11.
            assert world.source_totals()["G"] == (24 * tick,)
            assert world.totals()["G"][0] + world.escaped_totals()["G"][0] == 24 * tick
            assert world.totals()["light"] == (6,) and world.totals()["n"] == (MASS,)
            assert balanced(world)
            if tick <= 6:
                assert positions_of(world, "light") == {(4 + tick, 14, 10)}
                assert rays_at(world, (4 + tick, 14, 10), "light") == [light_ray(tick)]
                if tick == 6:
                    assert rays_at(world, (10, 14, 10), "G") == [ray(2, 4, 0, 4, 0, (0,) * 6)]
                continue
            walked = tick - 6
            assert positions_of(world, "light") == {TURN[walked - 1]}
            assert rays_at(world, TURN[walked - 1], "light") == [
                light_ray(walked, 9, (6, 0, 0, 4, 0, 0), LAGS[walked - 1])
            ]
            assert ray(3, 4, 0, walked, 9, (6, 0, 0, 4, 0, 0)) in rays_at(world, RECOIL[walked - 1], "G")
        return
    # (e) The acceptance criterion: G_eff x N^2 over N = 2^8, 2^10, 2^12, 2^16 with
    # the mass in phase units the same fraction N / 4 of N (hypothesis 14).
    products = []
    for bits in (8, 10, 12, 16):
        modulus = 1 << bits
        world = Simulation(parse_initial_state(document(LAMPS, [GRAVITY], bits=bits, ticks=8)))
        for _ in range(8):
            world.step()
        assert balanced(world) and world.totals()["G"] == world.source_totals()["G"] == (192,)
        assert positions_of(world, "light") == {(12, 14, 10)}
        (light,) = rays_at(world, (12, 14, 10), "light")
        assert light == light_ray(2, 9, (6, 0, 0, 4, 0, 0), (0, -16, 0))
        mass = modulus // 4
        alpha = Fraction(abs(light.lag[1]), modulus)
        g_eff = alpha * 4 / (4 * mass)
        assert g_eff == Fraction(64, modulus * modulus)
        products.append(g_eff * modulus * modulus)
    assert products == [64, 64, 64, 64]
