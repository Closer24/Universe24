"""A family's phase turn in flight is a declared width of the world
(`families[i].turns_in_flight`; the model owner, 2026-09-19, "what can be a
parameter, make a parameter"; the open question of DERIVATIONS.md round 8
section 52 (iv), what a matter shadow rotates by). A quantum in flight turns
its phase by its amount over K on every Link when its family turns, and not at
all otherwise; the default is the law's reading so far: a paid family (light)
turns, a free family (matter) does not. Isolated on the parser, the engine's
wiring and one Link of the layer's walk, the expected integers of
docs/TEST_EXPECTATIONS.md ("The phase turn in flight") written down first:

(a) the default by kind, a declared value either way, and the refusal of a
    value that is not a boolean;
(b) the engine gives each family's layer its declared turn;
(c) on one Link, a departure of 128 quanta at phase 5 with K = 16 and N = 64
    arrives at phase 13 when the family turns and at phase 5 when it does not,
    the amount and the momentum the same either way.
"""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.shadow import ShadowSimulation, parse_shadow_world
from event_universe.shadow.layer import ShadowLayer

PLUS_X = 0


def world(families: list[dict[str, object]]) -> dict[str, object]:
    return {
        "law": "shadow",
        "model_id": "family-turns-test",
        "shape": [5, 5, 5],
        "boundary": "open",
        "ticks": 1,
        "K": 16,
        "N": 64,
        "release": [1, 2],
        "families": families,
        "contents": [{"position": [2, 2, 2], "family": families[0]["name"], "amount": 256}],
    }


def test_the_default_is_by_kind_and_a_declared_value_is_kept():
    """(a)."""
    parsed = parse_shadow_world(
        world(
            [
                {"name": "m", "kind": "free"},
                {"name": "light", "kind": "paid"},
                {"name": "m_turning", "kind": "free", "turns_in_flight": True},
                {"name": "light_still", "kind": "paid", "turns_in_flight": False},
            ]
        )
    )
    assert [family.turns for family in parsed.families] == [False, True, True, False]
    with pytest.raises(ValueError, match=r"families\[0\]\.turns_in_flight must be true or false"):
        parse_shadow_world(world([{"name": "m", "kind": "free", "turns_in_flight": 1}]))


def test_the_engine_gives_each_layer_its_familys_turn():
    """(b)."""
    parsed = parse_shadow_world(
        world(
            [
                {"name": "m", "kind": "free"},
                {"name": "m_turning", "kind": "free", "turns_in_flight": True},
                {"name": "light", "kind": "paid"},
            ]
        )
    )
    simulation = ShadowSimulation(parsed)
    assert [layer.rotates for layer in simulation.layers] == [False, True, True]


@pytest.mark.parametrize("turns, arrival_phase", [(True, 13), (False, 5)])
def test_one_link_turns_the_phase_by_the_amount_over_k_or_not_at_all(turns, arrival_phase):
    """(c): 128 quanta over K = 16 are 8 steps of the circle of 64."""
    layer = ShadowLayer(0, (3, 1, 1), (1,), 64, 16, rotates=turns)
    layer.fly_amt[0, 0, 0, 0, PLUS_X, 0] = 128
    layer.fly_ph[0, 0, 0, 0, PLUS_X, 0] = 5
    layer.fly_mom[0, 0, 0, 0, PLUS_X, 0] = (3, 0, 0)
    layer.walk()
    assert int(layer.arr_amt[1, 0, 0, 0, PLUS_X, 0]) == 128
    assert int(layer.arr_ph[1, 0, 0, 0, PLUS_X, 0]) == arrival_phase
    assert layer.arr_mom[1, 0, 0, 0, PLUS_X, 0].tolist() == [3, 0, 0]
    assert int(layer.arr_amt.sum()) == 128 and not layer.fly_amt.any()
    assert np.array_equal(layer.carried(), np.array([3, 0, 0]))
