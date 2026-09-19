"""How a family's quanta turn their phase in flight is a declared width of the
world (`families[i].phase_turn`; the model owner, 2026-09-19: light turns by
its message, the same everywhere, "the default for light, that is, per
family"; DERIVATIONS.md round 8, S5). Per Link walked: `"quantum"`, by the
family's quantum over K, the same turn for every quantum of the family
wherever it is and however diluted, the remainder carried per family, so a
paid family keeps the frequency it was born with; `"amount"`, by the amount in
the cell over K, the old rule, which slows as the field thins; `"none"`. The
default is `"quantum"` for a paid family and `"none"` for a free one. The
expected integers of docs/TEST_EXPECTATIONS.md ("The phase turn in flight"),
written down first:

(a) the default by kind, a declared value kept, and a value outside the three
    refused by name; the engine gives each family's layer its rule and quantum;
(b) one Link of the walk at K = 16 and N = 64: 128 quanta at phase 5 arrive at
    phase 13 under "amount" (128 / 16 = 8 steps) and 5 quanta at phase 5 arrive
    at phase 5 (5 / 16 = 0); under "quantum" with quantum 16 both arrive one
    step on, at 6, whatever the amount; under "none" both arrive at 5; the
    amount and the momentum are the same either way;
(c) the remainder of the uniform rule: quantum 8 at K = 16 turns nothing on the
    first Link and one step on the second, whether or not anything was in
    flight on the first, since the family's clock advances every interval.
"""

from __future__ import annotations

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


def test_the_default_is_by_kind_and_the_engine_wires_the_rule():
    """(a)."""
    parsed = parse_shadow_world(
        world(
            [
                {"name": "m", "kind": "free"},
                {"name": "light", "kind": "paid", "quantum": 16},
                {"name": "m_amount", "kind": "free", "phase_turn": "amount"},
                {"name": "light_still", "kind": "paid", "phase_turn": "none"},
            ]
        )
    )
    assert [family.turn for family in parsed.families] == ["none", "quantum", "amount", "none"]
    with pytest.raises(ValueError, match=r"families\[0\]\.phase_turn must be one of"):
        parse_shadow_world(world([{"name": "m", "kind": "free", "phase_turn": True}]))
    simulation = ShadowSimulation(parsed)
    assert [layer.turn for layer in simulation.layers] == ["none", "quantum", "amount", "none"]
    assert [layer.quantum for layer in simulation.layers] == [1, 16, 1, 1]


def walked(turn: str, quantum: int, amount: int, walks: int = 1) -> tuple[int, int, list[int]]:
    """A departure of `amount` at phase 5 carrying (3, 0, 0) on +X, walked once
    (or `walks` times, re-placed as a departure between walks): the arrival's
    amount, phase and momentum at the neighbour."""
    layer = ShadowLayer(0, (3, 1, 1), (1,), 64, 16, turn=turn, quantum=quantum)
    for _ in range(walks - 1):
        layer.walk()
    layer.fly_amt[0, 0, 0, 0, PLUS_X, 0] = amount
    layer.fly_ph[0, 0, 0, 0, PLUS_X, 0] = 5
    layer.fly_mom[0, 0, 0, 0, PLUS_X, 0] = (3, 0, 0)
    layer.walk()
    assert int(layer.arr_amt.sum()) == amount and not layer.fly_amt.any()
    return (
        int(layer.arr_amt[1, 0, 0, 0, PLUS_X, 0]),
        int(layer.arr_ph[1, 0, 0, 0, PLUS_X, 0]),
        layer.arr_mom[1, 0, 0, 0, PLUS_X, 0].tolist(),
    )


@pytest.mark.parametrize(
    "turn, quantum, amount, phase",
    [
        ("amount", 1, 128, 13),
        ("amount", 1, 5, 5),
        ("quantum", 16, 128, 6),
        ("quantum", 16, 5, 6),
        ("none", 16, 128, 5),
        ("none", 16, 5, 5),
    ],
)
def test_one_link_turns_by_the_familys_rule(turn, quantum, amount, phase):
    """(b)."""
    assert walked(turn, quantum, amount) == (amount, phase, [3, 0, 0])


def test_the_uniform_rule_carries_its_remainder_per_family():
    """(c): quantum 8 at K = 16 is a step every second interval."""
    assert walked("quantum", 8, 5, walks=1)[1] == 5
    assert walked("quantum", 8, 5, walks=2)[1] == 6
    assert walked("quantum", 8, 5, walks=3)[1] == 5
