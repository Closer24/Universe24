"""A family's quantum is a declared width of the world (`families[i].quantum`;
the model owner, 2026-09-19, "put it in, without an experiment"; DERIVATIONS.md
round 8, S5 and S6: a whole q_γ assembled at a holder by the remainder rule,
per number, is the event a light table acts on, one absorption per quantum).
At a holder that absorbs a family (`keep`, the click; `rerelease`), the units
of one number wait in the holder's register until a whole quantum is there;
then one event of that whole. The push of the units enters the holder as they
are taken, as before; nothing changes in flight. The expected integers of
docs/TEST_EXPECTATIONS.md ("The quantum of a family"), written down first:

(a) the default is 1; 0, a negative, a fraction and a string are refused by name;
(b) light of quantum 3 at three marks, one interval: mark A gets 2 units of
    one lamp and 2 of another, no click, both pending, push (2, 2, 0); mark B
    gets 4 of one lamp, one click of 3, 1 pending, push (4, 0, 0); mark C
    (`rerelease`) gets 7, two events, 6 pooled and released again in the same
    interval with C's number, 1 pending, push (7, 0, 0); the books close;
(c) with the default of 1 every unit is its own event and nothing waits.
"""

from __future__ import annotations

import pytest

from event_universe.shadow import ShadowSimulation, parse_shadow_world

A, B, C = (2, 2, 2), (2, 2, 4), (4, 2, 2)
PLUS_X, PLUS_Y = (1, 0, 0), (0, 1, 0)


def world(quantum: object, shadows: list[dict[str, object]]) -> dict[str, object]:
    light: dict[str, object] = {"name": "light", "kind": "paid"}
    if quantum is not None:
        light["quantum"] = quantum
    return {
        "law": "shadow",
        "model_id": "family-quantum-test",
        "shape": [7, 5, 7],
        "boundary": "open",
        "ticks": 1,
        "K": 16,
        "N": 64,
        "release": [0, 1],
        "wait_per_quantum": 0,
        "families": [{"name": "m", "kind": "free"}, light],
        "contents": [
            {"position": list(A), "family": "m", "amount": 8, "fixed": True},
            {"position": list(B), "family": "m", "amount": 8, "fixed": True},
            {
                "position": list(C),
                "family": "m",
                "amount": 8,
                "fixed": True,
                "table": {"light": "rerelease"},
            },
            {"position": [0, 0, 0], "family": "light", "amount": 1, "fixed": True},
            {"position": [6, 4, 6], "family": "light", "amount": 1, "fixed": True},
        ],
        "initial_shadows": shadows,
    }


def arriving(position: tuple[int, int, int], amount: int, number: int = 4, heading=PLUS_X):
    return {
        "position": list(position),
        "family": "light",
        "number": number,
        "heading": list(heading),
        "amount": amount,
    }


def test_the_default_is_one_and_the_refusals_name_the_key():
    """(a)."""
    assert parse_shadow_world(world(None, [])).families[1].quantum == 1
    assert parse_shadow_world(world(3, [])).families[1].quantum == 3
    for bad in (0, -1, 2.5, "3"):
        with pytest.raises(ValueError, match=r"families\[1\]\.quantum"):
            parse_shadow_world(world(bad, []))


def test_a_click_is_one_whole_quantum_per_number_and_the_books_close():
    """(b)."""
    shadows = [
        arriving(A, 2, number=4),
        arriving(A, 2, number=5, heading=PLUS_Y),
        arriving(B, 4),
        arriving(C, 7),
    ]
    simulation = ShadowSimulation(parse_shadow_world(world(3, shadows)))
    simulation.step()
    a, b, c = simulation.holders[1], simulation.holders[2], simulation.holders[3]
    assert a.events[1] == 0 and a.absorbed[1]["keep"] == 0 and a.held[1] == 0
    assert a.pending[1] == {4: 2, 5: 2} and a.pushed == [2, 2, 0]
    assert b.events[1] == 1 and b.absorbed[1]["keep"] == 3 and b.held[1] == 3
    assert b.pending[1] == {4: 1} and b.pushed == [4, 0, 0]
    # The pool leaves again in the same interval, one unit per Port, with C's number.
    assert c.events[1] == 2 and c.absorbed[1]["rerelease"] == 6 and c.pool[1] == 0
    assert c.pending[1] == {4: 1} and c.pushed == [7, 0, 0]
    books = simulation.books()
    assert books["balanced"] is True
    light = books["families"]["light"]
    assert light["shadows"]["absorbed"] == 15 and light["shadows"]["released"] == 6
    assert light["shadows"]["current"] == 6
    assert light["held"]["absorbed"] == 3 and light["held"]["pending"] == 6
    assert a.state()["pending"] == [{}, {"4": 2, "5": 2}] and a.state()["events"] == [0, 0]


def test_the_default_of_one_makes_every_unit_its_own_event():
    """(c)."""
    simulation = ShadowSimulation(parse_shadow_world(world(None, [arriving(B, 4)])))
    simulation.step()
    b = simulation.holders[2]
    assert b.events[1] == 4 and b.absorbed[1]["keep"] == 4 and b.held[1] == 4
    assert b.pending[1] == {} and simulation.books()["families"]["light"]["held"]["pending"] == 0
