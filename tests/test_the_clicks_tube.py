"""The fifth kind by itself: a bound body's click at its own window's close, no rate, in the shipped tube beside the clicks chain, examples/events/clicks/clicks_tube.json (2026-10-22; the blind in examples/events/clicks/blind_tube.md, written before the run). The body is a region detector of its own light (the reader's build sentence of 01:05 and ruling of 02:37 on the light's front): the electron laid beating in the equal superposition of its two lowest levels in the frozen proton's well, the frame tool typing the two levels and the resonance alone, the window the beat's period, the light's front the Chebyshev shell about the body's Node at the radius den div (den sin k) + 1 with den cos k = 3 num - 2 den from the resonance pair; at each close the outflow in the quantum W_c sin Omega is credited by the floor and the remainder's draw, the quantum passing to the lower level over the body's region and light's whole quantum laid at the shell Node the outflow drew. The pinned numbers are the run's own, with their causes in the blind: the derived window, the shell's radius, the first window's booked outflow below one quantum (no click at the first close), and the run's empty click log: no click fell inside the 256 intervals, the first click's interval OPEN as the draw's (the body's own-light book per window in the blind's outcome)."""

import json

from event_universe.lattice import Lattice
from tests.laws import EVENTS
from tests.laws_read import load_shipped

FOLDER = EVENTS / "clicks"
WORLD = FOLDER / "clicks_tube.json"
RESONANCE = (5879, 6000)  # the frame's pair, den cos(Omega_upper - Omega_lower)
WINDOW = 32  # the beat's period, the count of turns of the resonance pair closing the circle
SHELL = (
    3  # den cos k = 3 x 5879 - 2 x 6000 = 5637, den sin k = 2055 by the one search, 6000 div 2055 + 1
)
CENTRE = (
    6,
    15,
    5,
)  # the body's declared Node, the shell's centre (the electron beside the proton at (5, 15, 5))
SHELL_NODES = 218  # the Chebyshev shell r = 3 about the proton's Node: 7^3 - 5^3
REGION = 3209  # the write's region, the laid part's whole support
LINES = 0  # the run's output lines: none, no click fell inside the 256 intervals (the blind's expectation about 0.2)
FIRST_WINDOW_QUANTA = (
    None  # the first close's booked outflow in quanta, from the run (0.0486 by the probe)
)


def test_the_declaration_is_the_frames_and_nothing_of_the_mechanism():
    world = load_shipped(WORLD)
    mode = json.loads(WORLD.with_suffix(".mode.json").read_text(encoding="utf-8"))
    instrument = mode["bodies"][1]["instrument"]
    assert [p["name"] for p in instrument["parts"]][0].startswith(
        "level [4736, 6000]"
    )  # the lower level, count 0
    assert [p["count"] for p in instrument["parts"]] == [0, 1]  # the record stands in the upper level
    assert tuple(instrument["transitions"][0]["resonance"]) == RESONANCE
    assert (
        "weight" not in instrument["transitions"][0]
    )  # the holder's read weight by reciprocity, not typed
    assert not instrument.get("rates")  # no rate: the body credits its own light
    assert "window" not in instrument["node_detector"]  # the window the beat's own period, derived
    electron = [f for f in world.families if f.name == "electron"]
    assert len(world.bodies) == 2 and len(electron) == 1 and electron[0].pair == (4000, 6000)
    body = world.bodies[1]
    assert body.radius == SHELL and len(body.shell) == SHELL_NODES and len(body.region) == REGION
    assert max(abs(a - b) for at in body.shell for a, b in zip(at, CENTRE, strict=True)) == SHELL


def test_the_bound_body_books_its_own_light_and_the_run_drew_no_click():
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_shipped(WORLD), lines.append)
    (books,) = [b for b in board.credit.bodies if board.families[b.index].name == "electron"]
    assert books.declared.draw.window == WINDOW
    for _ in range(2):
        board.step()
    assert tuple(int(v) for v in board.shape) == (11, 47, 11)  # the y faces recede at the first interval
    assert len(books.light) == SHELL_NODES and any(
        int(v) for v in books.light
    )  # the book per shell Node, written
    assert lines == []
    log = json.loads(WORLD.with_suffix(".clicks.json").read_text(encoding="utf-8"))
    assert (
        log == [] and len(log) == LINES
    )  # the run's record, a JSON array as the chain's log: no click inside 256 intervals
