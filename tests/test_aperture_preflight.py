"""The aperture's multiplicity, refused at load (issue #714; the amplitude
law's rule of the design's section 2.5 unchanged: two paths of one record
add exactly at a set only when their multiplicities differ by a square
factor). A minimal aperture on a 5 x 5 x 1 GameBoard: a lamp at (0, 2) on
+x, an opening A at (2, 2) and, two Nodes wide, an opening B at (2, 3),
each a plain `rerelease` on the fan F (every weight 1: the norm is the
fan's count), a screen of five `sum` sets `screen_<y>` at x = 4. The
expected integers, written down first:

A row walks its direction's digital line one Link at a time, the lowest
axis first ([1, 1, 0] from (2, 2): (3, 2), (3, 3), (4, 3)).

(a) the fan of three directions [0, 1, 0], [1, 1, 0], [1, 0, 0] (the norm
    3): the row A sends on [1, 1, 0] reaches screen_3 with the multiplicity
    1 x 3; the row A sends on [0, 1, 0] is re-released at B, and B's row on
    [1, 0, 0] reaches screen_3 with 3 x 3 = 9; the ratio 1:3 is not a
    square, and the world is refused at load naming the rule, the two
    multiplicities, the openings of both paths, the ratio and the width 2
    (the same world with the loader's check off is refused by the run at
    tick 8, "the multiplicities 3 and 9", the bug of issue #714); the same
    fan on the opening A alone (the width 1) is accepted: every path of
    the record carries 3;
(b) the fan of four directions (the norm 4, a square; [1, -1, 0] added):
    screen_2 is reached with 4 (A on [1, 0, 0]) and 16 (B on [1, -1, 0]),
    a square ratio; accepted at load and the run takes 20 intervals
    without a refusal;
(c) the edge: the norm 2 is the smallest non-square norm a fan can have
    (two directions), and an aperture of that fan ([0, 1, 0] and [1, 1, 0])
    is accepted: A's row reaches screen_3 with 2, B's screen_4 with 4, no
    set is reached twice, so no offer ever holds two multiplicities, and
    the run takes 20 intervals; 3 is the smallest non-square multiplicity
    an aperture brings to one set; the aperture of width 3 (an opening at
    (2, 1) added) with the fan of (a) is refused naming the width 3.
"""

from __future__ import annotations

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

N = 64
NORM_3 = [[0, 1, 0], [1, 1, 0], [1, 0, 0]]
NORM_4 = [*NORM_3, [1, -1, 0]]
NORM_2 = [[0, 1, 0], [1, 1, 0]]


def opening(position: list[int], fan: list[list[int]]) -> dict[str, object]:
    return {
        "position": position,
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"light": "rerelease"},
        "directions": fan,
    }


def aperture_world(openings: list[list[int]], fan: list[list[int]]) -> dict[str, object]:
    """The lamp on +x into the openings, the screen's five sets at x = 4."""
    measured: list[dict[str, object]] = [
        {
            "position": [0, 2, 0],
            "family": "light",
            "amount": 1 << 20,
            "fixed": True,
            "lamp": {"wheel": [1, N], "rate": [1, 1], "directions": [[1, 0, 0]]},
        }
    ]
    measured.extend(opening(position, fan) for position in openings)
    measured.extend(
        {"position": [4, y, 0], "family": "counter", "amount": 1, "fixed": True} for y in range(5)
    )
    return {
        "law": "beam",
        "model_id": "aperture-preflight-test",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": 30,
        "K": 1 << 20,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "directions": [[1, 1, 0], [1, -1, 0]],
        "families": [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}],
        "measured": measured,
        "detectors": [
            {"name": f"screen_{y}", "positions": [[4, y, 0]], "reading": "sum"} for y in range(5)
        ],
    }


def run(world: dict[str, object], ticks: int) -> NatureBeamSimulation:
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    for _ in range(ticks):
        simulation.step()
    return simulation


def test_an_aperture_of_non_square_multiplicity_is_refused_at_load() -> None:
    """(a), (b) and (c)."""
    # (a) the width 2 with the norm 3: refused at load, the message whole.
    with pytest.raises(ValueError) as refused:
        parse_nature_beam_world(aperture_world([[2, 2, 0], [2, 3, 0]], NORM_3))
    message = str(refused.value)
    assert message.startswith("beam-v1: two paths of one record of 'light' from the lamp measured[0]")
    assert "reach screen_3 with the multiplicities 3 (through the openings at [[2, 2, 0]])" in message
    assert "and 9 (through [[2, 2, 0], [2, 3, 0]]), whose ratio 1:3 is not a square" in message
    assert (
        "(an aperture 2 Nodes wide: the openings at [[2, 2, 0], [2, 3, 0]] feed one another)" in message
    )
    assert "only when their multiplicities differ by a square factor (amplitude-v1" in message
    assert message.endswith("or open the aperture one Node wide")
    # The width 1: every path carries the norm 3 once; accepted and run.
    assert run(aperture_world([[2, 2, 0]], NORM_3), 20).tick == 20
    # (b) the norm 4: 4 against 16 at screen_2, a square ratio; accepted and run.
    assert run(aperture_world([[2, 2, 0], [2, 3, 0]], NORM_4), 20).tick == 20
    # (c) the smallest non-square norm, 2, whose rays reach no set together:
    # accepted and run.
    assert run(aperture_world([[2, 2, 0], [2, 3, 0]], NORM_2), 20).tick == 20
    # The width 3 with the norm 3: refused naming the width.
    with pytest.raises(ValueError, match=r"an aperture 3 Nodes wide"):
        parse_nature_beam_world(aperture_world([[2, 1, 0], [2, 2, 0], [2, 3, 0]], NORM_3))
