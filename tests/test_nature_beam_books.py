"""The books as running ledger lines under the law of the ray
(docs/RAY_LAW.md, section 10, note 22; the optimizations of 2026-09-19):
`books()` reports the transit line, the content line and the transit
momentum from the ledger (what was released less what left: escaped, home,
absorbed), O(families) and no pass over the store, and `recount()` counts
the same three lines from the rows of the store. The expected result of
docs/TEST_EXPECTATIONS.md ("The books"), written down first: on a world
that exercises every way a row comes or goes, the running lines equal the
recount at every one of 40 intervals, `books(recount=True)` equals
`books()`, and the books balance; on an empty world both are zero.

The world: a 12 x 1 x 3 GameBoard with y periodic (the stub: a ray on +-y lands
on its own Node and is home) and every other face open, K 2^20, N 64,
`release` [1, 4], a fan direction (2, 1, 0) declared; a lamp of the paid
family `light` (content 2^23, the turn 8) at (1, 0, 1) releasing 3 units
per self-creation on +X, on (2, 1, 0) and on +Y (the +Y unit comes home
next interval, the home of a paid family, and is created again on the
six headings, so some of it escapes through the z faces); a re-emitter
of `light` (content 1) at (5, 0, 1) with `rerelease` for `light` on +X
and -X (the -X copies click at the lamp, the +X ones at the screen); the
detector `screen` at (9, 0, 1), a measured event of `light` measuring it;
a free source `m` (content 2^19) at (10, 0, 1), beyond the screen,
releasing 2^17 per heading per self-creation (the +-Z units escape
through the z faces at once, the +-Y units come home, the +X units escape
through the +x face, the -X units are read by the screen, the re-emitter
and the lamp and escape through the -x face); two units of `light` in
transit head-on at (3, 0, 0) and (5, 0, 0) meeting at (4, 0, 0) in free
space, parked at rest by the collision in the interval they meet (the
labels +1 and -1 conserved; the table moves the pair on later).
"""

from __future__ import annotations

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

LIGHT, M = 0, 1
TICKS = 40


def world_of_every_way() -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-books-test",
        "shape": [12, 1, 3],
        "boundary": {"y": "periodic"},
        "ticks": TICKS,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 4],
        "suspension": 0,
        "directions": [[2, 1, 0]],
        "families": [{"name": "light", "quantum": 1}, {"name": "m", "quantum": 0}],
        "measured": [
            {
                "position": [1, 0, 1],
                "family": "light",
                "amount": 1 << 23,
                "fixed": True,
                "lamp": {"rate": [3, 1], "directions": [[1, 0, 0], [2, 1, 0], [0, 1, 0]]},
            },
            {
                "position": [5, 0, 1],
                "family": "light",
                "amount": 1,
                "fixed": True,
                "table": {"light": "rerelease"},
                "directions": [[1, 0, 0], [-1, 0, 0]],
            },
            {"position": [9, 0, 1], "family": "light", "amount": 1, "fixed": True},
            {"position": [10, 0, 1], "family": "m", "amount": 1 << 19, "fixed": True},
        ],
        "detectors": [{"name": "screen", "positions": [[9, 0, 1]], "threshold": 1}],
        "in_transit": [
            {
                "position": [3, 0, 0],
                "family": "light",
                "number": 1,
                "direction": [1, 0, 0],
                "amount": 1,
                "phase": 0,
            },
            {
                "position": [5, 0, 0],
                "family": "light",
                "number": 1,
                "direction": [-1, 0, 0],
                "amount": 1,
                "phase": 5,
            },
        ],
    }


def current_lines(books: dict[str, object]) -> dict[str, list[int]]:
    families = books["families"]
    assert isinstance(families, dict)
    momentum = books["momentum"]
    assert isinstance(momentum, dict)
    return {
        "transit": [int(families[name]["transit"]["current"]) for name in ("light", "m")],
        "content": [int(families[name]["content"]["current"]) for name in ("light", "m")],
        "momentum": list(momentum["transit"]),
    }


def test_the_running_lines_equal_the_recount_at_every_interval():
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world_of_every_way()), records.append)
    assert current_lines(simulation.books()) == simulation.recount()
    moved = False
    for tick in range(1, TICKS + 1):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        counted = simulation.recount()
        assert current_lines(books) == counted, tick
        assert simulation.books(recount=True) == books, tick
        moved = moved or counted["momentum"] != [0, 0, 0]
        if tick == 1:
            light = simulation.stores[LIGHT]
            at_rest = light.direction < 2
            assert int(at_rest.sum()) == 2 and (light.node[at_rest] == light.flat((4, 0, 0))).all()
    assert moved
    kinds = {(str(r["event"]), r["detector"], str(r["family"])) for r in records}
    assert ("home", None, "light") in kinds and ("home", None, "m") in kinds
    assert ("rerelease", None, "light") in kinds and ("read", None, "m") in kinds
    assert ("click", "screen", "light") in kinds and ("click", None, "light") in kinds
    assert ("click", "face:+z", "m") in kinds and ("click", "face:+x", "m") in kinds
    assert ("click", "face:-x", "m") in kinds and ("click", "face:-z", "light") in kinds


def test_an_empty_world_counts_zero_both_ways():
    world = world_of_every_way()
    world["measured"], world["in_transit"], world["detectors"] = [], [], []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world))
    simulation.step()
    zero = {"transit": [0, 0], "content": [0, 0], "momentum": [0, 0, 0]}
    assert simulation.recount() == zero == current_lines(simulation.books())
    assert simulation.books(recount=True) == simulation.books()
