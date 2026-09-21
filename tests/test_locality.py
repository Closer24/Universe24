"""LOCALITY-1 (SIMULATOR_DEFINITIONS.md): every physical update of a Node
reads its own rows and what the six Ports delivered, and nothing else of the
GameBoard; a change travels one Link per interval at most. Two checks: (a)
the rule is documented without an exception; (b) the six-read test on a
minimal GameBoard, the executable form the scalar candidate's deletion of
2026-09-17 left out (the architecture audit of 2026-09-21, item 8). The
layer of `amplitude-v1` (the click's join and deletion over a record's
identity) is the one non-local operation the model owner decided (records
72 and 74 of 2026-09-20) and is outside this test's claim: no world here
declares a record.

The expected integers of docs/TEST_EXPECTATIONS.md ("Locality and bounded
local work"), written down first. A bar of 13 x 1 x 1, y and z periodic,
K 2^20 so that no phase moves, `suspension` 0, `release` [0, 1], the
families `m` (free, the reader's), `f` (free, another number's) and
`light` (paid); the measured events 1 (of `f`, at x = 12, fixed) and 2
(`d`, of `m`, content 4, at x = 9, fixed, measuring `light` and reading
`f`, a `beam` detector so that the window reads each ray's own phase); the
two Nodes under test X_c = 3 (free space) and X_d = 9 (the detector's):

(b) the six-read test: the world A seeds a head-on pair of `light` at x = 2
    (+X) and x = 4 (-X) meeting at X_c in interval 1, a `light` unit at
    x = 8 on +X clicking at X_d in interval 1 and an `f` unit at x = 10 on
    -X pushing d in interval 1; the world B is A with rows beyond one Link
    of both Nodes changed: a `light` pair at x = 6 (+X and -X, walking
    apart to x = 7 and x = 5), a `light` unit at x = 0 on -X (escaping on
    `face:-x`) and one at x = 11 on +X. After interval 1, A and B are byte-identical at X_c
    (the rows: the pair parked as the two rest rays), at X_d (the rows,
    the click, the push: d's record and momentum) and in the readings of
    both Nodes (arrived, flow, presence per family), while B differs from
    A elsewhere (the rows at x = 5 and x = 7, the face's click); d clicked once and
    its momentum moved, so the identity is not vacuous;
(c) the converse, the causal bound: the world D0 (the pair of (b) alone)
    and D_k, D0 with a `light` unit k Links from X_d on +X, k = 1, 2, 3:
    X_d's rows and d's record are identical for every interval before the
    flight's first arrival at k Links and differ at it, the intervals 1,
    3 and 5 (the flight table, `test_nature_beam_flight` (a)): the
    neighbour's change reaches X_d exactly one interval later and no
    sooner, a change at k Links no sooner than k intervals later.
"""

from __future__ import annotations

import json
from pathlib import Path

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

X_C = (3, 0, 0)
X_D = (9, 0, 0)
FIRST_ARRIVAL = {1: 1, 2: 3, 3: 5}


def test_locality_rule_is_documented_without_an_exception():
    """(a)."""
    root = Path(__file__).parents[1]
    definitions = (root / "SIMULATOR_DEFINITIONS.md").read_text()
    assert "LOCALITY-1" in definitions
    assert "end-to-end" in definitions
    assert "fixed K" in definitions
    assert "sole explicit model-computation exception" not in definitions
    assert "LOCALITY-1" in (root / "AGENTS.md").read_text()


def ray(x: int, sign: int, family: str = "light", phase: int = 0) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": family,
        "number": 1,
        "direction": [sign, 0, 0],
        "amount": 1,
        "phase": phase,
    }


def bar(in_transit: list[dict[str, object]]) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "locality-test",
        "shape": [13, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": 6,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [
            {"name": "m", "quantum": 0},
            {"name": "f", "quantum": 0},
            {"name": "light", "quantum": 1},
        ],
        "measured": [
            {"position": [12, 0, 0], "family": "f", "amount": 1, "fixed": True},
            {
                "position": list(X_D),
                "family": "m",
                "amount": 4,
                "fixed": True,
                "table": {"light": "measure", "f": "read"},
            },
        ],
        "detectors": [{"name": "d", "positions": [list(X_D)], "reading": "beam"}],
        "in_transit": in_transit,
    }


def at_node(simulation: NatureBeamSimulation, node: tuple[int, int, int]) -> str:
    """Everything the interval left at one Node, as JSON: its rows per
    family and its readings (the amount arrived, the net flow and the
    presence per family)."""
    vectors = simulation.tables.flight.vectors
    rows = []
    for store in simulation.stores:
        lo, hi = store.slice(store.flat(node))
        rows.append([beam.record_line(vectors) for beam in store.rows(lo, hi)])
    readings = [
        [
            int(simulation.arrived[f][node]),
            [int(c) for c in simulation.flow[f][node]],
            int(simulation.presence[f][node]),
        ]
        for f in range(len(simulation.stores))
    ]
    return json.dumps({"rows": rows, "readings": readings}, sort_keys=True)


def at_detector(simulation: NatureBeamSimulation) -> str:
    """The reader's side at X_d: d's state (its momentum after the push,
    its content and held after the click) and the detector's record."""
    detector = next(entry for entry in simulation.detectors() if entry["name"] == "d")
    return json.dumps({"measured": simulation.measured[2].state(), "detector": detector}, sort_keys=True)


def test_a_node_reads_nothing_beyond_one_link():
    """(b)."""
    near = [ray(2, 1), ray(4, -1, phase=32), ray(8, 1), ray(10, -1, family="f")]
    far = [ray(6, 1, phase=5), ray(6, -1, phase=40), ray(0, -1), ray(11, 1)]
    a = NatureBeamSimulation(parse_nature_beam_world(bar(near)))
    b = NatureBeamSimulation(parse_nature_beam_world(bar(near + far)))
    a.step()
    b.step()
    assert a.books()["balanced"] and b.books()["balanced"]
    assert at_node(a, X_C) == at_node(b, X_C)
    assert at_node(a, X_D) == at_node(b, X_D)
    assert at_detector(a) == at_detector(b)
    # Not vacuous: the pair parked at X_c as the two rest rays, d clicked
    # the unit and the push moved its momentum; and B is not A elsewhere.
    light = a.stores[2]
    lo, hi = light.slice(light.flat(X_C))
    assert sorted(int(d) for d in light.direction[lo:hi]) == [0, 1]
    detector = next(entry for entry in a.detectors() if entry["name"] == "d")
    assert detector["families"]["light"]["clicks"] == 1
    assert a.measured[2].momentum != [0, 0, 0]
    assert at_node(a, (5, 0, 0)) != at_node(b, (5, 0, 0))
    assert at_node(a, (7, 0, 0)) != at_node(b, (7, 0, 0))
    assert a.detectors() != b.detectors()


def test_a_change_reaches_a_node_no_sooner_than_the_flight_allows():
    """(c)."""
    pair = [ray(2, 1), ray(4, -1, phase=32)]
    for links, first in FIRST_ARRIVAL.items():
        d0 = NatureBeamSimulation(parse_nature_beam_world(bar(pair)))
        dk = NatureBeamSimulation(parse_nature_beam_world(bar(pair + [ray(X_D[0] - links, 1)])))
        assert at_node(d0, X_D) == at_node(dk, X_D)
        for tick in range(1, first + 1):
            d0.step()
            dk.step()
            same = at_node(d0, X_D) == at_node(dk, X_D) and at_detector(d0) == at_detector(dk)
            assert same == (tick < first), (links, tick)
        assert first >= links
