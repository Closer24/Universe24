"""The width of a window, `phase_width` (docs/BEAM_LAW.md, section 2 and
section 10 note 36; the model owner, 2026-09-20, "go on everything": the
weak force in the recommended order, the neutrino first with the
table-entry key `phase_width` and no change of law; the physicist's design,
WEAK.md 1.2): a window is its setting s and its width w, the w consecutive
steps of the circle [s - floor(w / 2), s - floor(w / 2) + w), a phase at the
distance d = (phase - s) mod N inside when (d + floor(w / 2)) mod N < w
(`nature_beam.window_admits`, the one floor of the window and its width),
N / 2 by default: the half circle as it was. The expected integers of
docs/TEST_EXPECTATIONS.md ("The width of a window"), written down before
the first run:

(a) the one floor at the default width N / 2 is the half circle on every
    (phase, setting) pair, d < N / 4 or d >= 3 N / 4, at N = 2, 4, 64 and
    4096 (for N = 2 the one step d = 0); at N = 64 the width 1 centred on s
    admits {s}, 2 admits {s - 1, s}, 3 admits {s - 1, s, s + 1}, 4 admits
    {s - 2, s - 1, s, s + 1} (the arc starts at s - floor(w / 2)), and the
    width 64 admits every step;
(b) the admitted fraction w / N against the source's stride: a bar of
    9 x 1 x 1, K 4096, N 64, `release` [1, 4096], `suspension` 0; a fixed
    source of the free family `nu` (a phase circle) of content 4096 at x = 0
    releasing one ray per self-creation on +x (the release 4096 x 1 / 4096,
    the turn 4096 / 4096 = 1 phase step per self-creation: the stride 1),
    the ray born at tick t carrying the phase (t - 1) mod 64, arriving at
    the fixed reader `r` (free, no phase circle, content 1) at x = 5 at tick
    t + 8 (`m(8) = 5`); over 648 intervals 640 arrivals (ticks 9 .. 648).
    The reader's entry `nu: {rule measure, phase_window 0}`: with the width
    absent 320 click and 320 pass (the phases 0 .. 15 and 48 .. 63, the
    engine as it was); with `phase_width` 1: 10 clicks, at the phase 0
    alone, at the ticks 9, 73, ..., 585 (9 + 64 k); 2: 20 (the phases 63
    and 0); 4: 40 (62, 63, 0, 1); 32: 320, the `click` and `pass` records
    identical line by line to the width absent. With K 2048 (the turn 2:
    the stride 2, the phases 0, 2, 4, ...), the width 1 centred on 0 admits
    20 of 640 (the even coset, 1 / 32) and centred on 1 admits 0 (the coset
    missed, 640 passes). The reader declared as a `beam` detector reads the
    same counts (one ray per interval, nothing to pair). Each click of a
    free family's ray takes the columns' push, gravity -M_A x V = -64 on a
    reader of content 1 (toward the source; a free ray's label never joins,
    only a paid ray's does), so the reader's momentum after c clicks is
    (-64 c, 0, 0). The reader's state carries `widths` [w, None] (None
    where no width is declared); a world without the key is unchanged, the
    state's `widths` all None;
(c) `beam`'s pairing arc is the entry's width: two rays of `light` at
    x = 5 with the phases 0 and 30 (and 0 and 10) arriving together at a
    `beam` counter at x = 6 whose entry has the window 16 (both phases
    inside it at every width below): with the width 40 the pair (0, 30) is
    paired (d = (30 - 0 - 32) mod 64 = 62, (62 + 20) mod 64 = 18 < 40: two
    `pass` records with `cancelled`, no click) and the pair (0, 10) clicks
    twice (d = 42, (42 + 20) mod 64 = 62 < 40 false); with the width 64
    every pair is paired, (0, 10) among them; with the default width (0,
    30) pairs ((62 + 16) mod 64 = 14 < 32) and (0, 10) clicks (58 < 32
    false), as until 2026-09-20;
(d) a lamp's window has the same width: the lamp of
    `tests/test_nature_beam_window.py` (c) (K 2^14, content K + 2, the turn
    1, one ray per self-creation on +x) with `phase_window` 8 and
    `phase_width` 4 releases at the self-creations whose clock phase falls
    in [6, 10): over the first 64 intervals 4 rays, at the phases 6, 7, 8
    and 9, against 31 with the width absent (the lamp's exact clock, the
    count of its turn accumulator since the fraction-free law of
    2026-09-20, stalls once at tick 6: 63 phases walked in 64 intervals;
    32 under the whole part off the clock until then);
(e) the refusals, naming the key: `phase_width` 0, 65 (at N = 64), 1.5 and
    "4" (an integer from 1 through N); on `pass`; for a family without a
    phase circle; without `phase_window` (a width is the width of a
    window); on a lamp without its window and at 0; `phase_width` alone
    with `phase_window` on a paid family takes the default rule `measure`.
"""

from __future__ import annotations

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import window_admits
from event_universe.events.world import default_width

NU, R = 0, 1
TICKS = 648
ARRIVALS = 640
FIRST_ARRIVAL = 9


def half_circle(distance: int, modulus: int) -> bool:
    """The window as it was until 2026-09-20: a table over the distances."""
    return 4 * distance < modulus or 4 * distance >= 3 * modulus


# -- (a) ---------------------------------------------------------------------------


def test_the_default_width_is_the_half_circle_on_every_pair_and_a_width_is_an_arc():
    """(a)."""
    for modulus in (2, 4, 64, 4096):
        width = default_width(modulus)
        for setting in range(0, modulus, max(1, modulus // 64)):
            for phase in range(modulus):
                distance = (phase - setting) % modulus
                assert bool(window_admits(distance, width, modulus)) == half_circle(distance, modulus)
    for setting in (0, 7, 63):
        for width, offsets in ((1, [0]), (2, [-1, 0]), (3, [-1, 0, 1]), (4, [-2, -1, 0, 1])):
            admitted = sorted(
                phase for phase in range(64) if window_admits((phase - setting) % 64, width, 64)
            )
            assert admitted == sorted((setting + k) % 64 for k in offsets), (setting, width)
        assert all(window_admits((phase - setting) % 64, 64, 64) for phase in range(64))


# -- (b) ---------------------------------------------------------------------------


def bar(width: int | None, clock: int = 4096, setting: int = 0, beam: bool = False) -> dict[str, object]:
    entry: dict[str, object] = {"rule": "measure", "phase_window": setting}
    if width is not None:
        entry["phase_width"] = width
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "window-width-test",
        "shape": [9, 1, 1],
        "boundary": "open",
        "ticks": TICKS,
        "K": clock,
        "N": 64,
        "release": [1, 4096],
        "suspension": 0,
        "families": [{"name": "nu", "quantum": 0}, {"name": "r", "quantum": 0, "phase": False}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "nu",
                "amount": 4096,
                "phase": 0,
                "fixed": True,
                "directions": [[1, 0, 0]],
            },
            {"position": [5, 0, 0], "family": "r", "amount": 1, "fixed": True, "table": {"nu": entry}},
        ],
    }
    if beam:
        document["detectors"] = [{"name": "gate", "positions": [[5, 0, 0]], "reading": "beam"}]
    return document


def arrivals(document: dict[str, object]) -> tuple[NatureBeamSimulation, list[tuple[int, int, str]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(document), records.append)
    for _ in range(TICKS):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    found = [
        (int(str(r["tick"])), int(str(r["phase"])), str(r["event"]))
        for r in records
        if r["event"] in ("click", "pass") and r.get("measured") == 2
    ]
    return simulation, found


def test_the_admitted_fraction_is_the_width_over_the_circle_against_the_stride():
    """(b)."""
    simulation, found = arrivals(bar(None))
    assert len(found) == ARRIVALS and found[0][0] == FIRST_ARRIVAL and found[-1][0] == TICKS
    assert [t for t, _, _ in found] == list(range(FIRST_ARRIVAL, TICKS + 1))
    assert [p for _, p, _ in found] == [(t - FIRST_ARRIVAL) % 64 for t, _, _ in found]
    assert sum(1 for _, _, e in found if e == "click") == 320
    assert sorted({p for _, p, e in found if e == "click"}) == [*range(16), *range(48, 64)]
    assert simulation.measured[2].widths == [None, None] and simulation.measured[2].state()[
        "widths"
    ] == [
        None,
        None,
    ]
    for width, clicks, phases in ((1, 10, [0]), (2, 20, [63, 0]), (4, 40, [62, 63, 0, 1])):
        simulation, narrow = arrivals(bar(width))
        clicked = [(t, p) for t, p, e in narrow if e == "click"]
        assert len(clicked) == clicks and len(narrow) == ARRIVALS, width
        assert sorted({p for _, p in clicked}) == sorted(phases), width
        assert simulation.measured[2].widths == [width, None]
        assert simulation.measured[2].clicks == [clicks, 0] and simulation.measured[2].momentum == [
            -64 * clicks,
            0,
            0,
        ]
    _, one = arrivals(bar(1))
    assert [t for t, _, e in one if e == "click"] == [FIRST_ARRIVAL + 64 * k for k in range(10)]
    _, half = arrivals(bar(32))
    assert half == found
    # The stride 2: the even coset at the centre 0, nothing at the centre 1.
    _, even = arrivals(bar(1, clock=2048))
    assert [p for _, p, _ in even][:4] == [0, 2, 4, 6]
    assert sum(1 for _, _, e in even if e == "click") == 20
    _, odd = arrivals(bar(1, clock=2048, setting=1))
    assert sum(1 for _, _, e in odd if e == "click") == 0 and len(odd) == ARRIVALS
    # Under `beam` the same counts.
    _, beam_one = arrivals(bar(1, beam=True))
    assert sum(1 for _, _, e in beam_one if e == "click") == 10
    _, beam_half = arrivals(bar(None, beam=True))
    assert sum(1 for _, _, e in beam_half if e == "click") == 320


# -- (c) ---------------------------------------------------------------------------


def pair_world(width: int | None, phases: tuple[int, int]) -> dict[str, object]:
    entry: dict[str, object] = {"rule": "measure", "phase_window": 16}
    if width is not None:
        entry["phase_width"] = width
    return {
        "law": "beam",
        "model_id": "window-width-pairing-test",
        "shape": [7, 1, 1],
        "boundary": "open",
        "ticks": 2,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}],
        "measured": [
            {"position": [0, 0, 0], "family": "light", "amount": 8, "fixed": True},
            {
                "position": [6, 0, 0],
                "family": "counter",
                "amount": 1,
                "fixed": True,
                "table": {"light": entry},
            },
        ],
        "in_transit": [
            {
                "position": [5, 0, 0],
                "family": "light",
                "number": 1,
                "direction": [1, 0, 0],
                "amount": 1,
                "phase": phase,
            }
            for phase in phases
        ],
        "detectors": [{"name": "gate", "positions": [[6, 0, 0]], "reading": "beam"}],
    }


def outcome(width: int | None, phases: tuple[int, int]) -> tuple[int, int]:
    """(the clicks, the cancelled passes) of the two rays at the counter."""
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(pair_world(width, phases)), records.append)
    simulation.step()
    assert simulation.books()["balanced"]
    clicks = sum(1 for r in records if r["event"] == "click" and r["measured"] == 2)
    cancelled = sum(1 for r in records if r["event"] == "pass" and r.get("cancelled"))
    return clicks, cancelled


def test_the_pairing_arc_under_beam_is_the_entrys_width():
    """(c)."""
    assert outcome(40, (0, 30)) == (0, 2) and outcome(40, (0, 10)) == (2, 0)
    assert outcome(64, (0, 10)) == (0, 2)
    assert outcome(None, (0, 30)) == (0, 2) and outcome(None, (0, 10)) == (2, 0)


# -- (d), (e) -----------------------------------------------------------------------

K_B = 1 << 14


def lamp_world(lamp: dict[str, object]) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "window-width-lamp-test",
        "shape": [12, 1, 1],
        "boundary": "open",
        "ticks": 64,
        "K": K_B,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": K_B + 2,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": [[1, 0, 0]], **lamp},
            },
            {"position": [10, 0, 0], "family": "counter", "amount": 1, "fixed": True},
        ],
    }


def test_a_lamps_window_has_the_same_width():
    """(d)."""
    parsed = parse_nature_beam_world(lamp_world({"phase_window": 8, "phase_width": 4}))
    assert parsed.measured[0].lamp is not None and parsed.measured[0].lamp.width == 4
    simulation = NatureBeamSimulation(parsed)
    source, light = simulation.measured[1], simulation.stores[0]
    assert source.lamp_width == 4
    released: list[int] = []
    for tick in range(1, 65):
        simulation.step()
        assert simulation.books()["balanced"], tick
        fresh = light.age == 0
        if fresh.any():
            released.append(int(light.phase[fresh][0]))
    # The four releases at the clock's phases 6 .. 9 are records born at
    # u = 0 .. 3 (re-run under the one click (stage (vii) step 4); the verdict to be re-read; until stage (vii) step 4 the rows carried 6 .. 9).
    assert released == [0, 1, 2, 3] and simulation.ledger.transit_released == [4, 0]
    assert source.held == [K_B + 2 - 4, 0] and source.momentum == [-256, 0, 0]
    # Without the width the half circle admits 32 phases of 64; the lamp
    # (content K + 2 paying 1 per release) stalls its exact clock once, at
    # the self-creation of tick 6 (the fraction-free law, 2026-09-20), so
    # 63 phases are walked in 64 intervals and 31 releases fall in the
    # window (32 until then, the whole part off the clock at the current
    # content never stalling within 64 intervals).
    wide = NatureBeamSimulation(parse_nature_beam_world(lamp_world({"phase_window": 8})))
    stalls = []
    for tick in range(1, 65):
        wide.step()
        if wide.measured[1].turn == 0:
            stalls.append(tick)
    assert stalls == [6] and wide.measured[1].turned == 63
    assert wide.ledger.transit_released == [31, 0] and wide.measured[1].lamp_width is None


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_nature_beam_world(document)


def test_the_refusals_name_the_key():
    """(e)."""
    for bad in (0, 65, 1.5, "4"):
        refused(bar(bad), r"table\['nu'\]\.phase_width must be an integer from 1 through 64")  # type: ignore[arg-type]
    document = bar(1)
    document["measured"][1]["table"] = {"nu": {"rule": "pass", "phase_width": 1}}  # type: ignore[index]
    refused(document, r"table\['nu'\]\.phase_width is refused on pass")
    document = bar(1)
    document["measured"][0]["table"] = {"r": {"rule": "measure", "phase_width": 1}}  # type: ignore[index]
    refused(document, r"table\['r'\]\.phase_width is refused for a family without a phase circle")
    document = bar(1)
    document["measured"][1]["table"] = {"nu": {"rule": "measure", "phase_width": 1}}  # type: ignore[index]
    refused(document, r"table\['nu'\]\.phase_width needs the window's setting `phase_window`")
    refused(lamp_world({"phase_width": 4}), r"lamp\.phase_width needs the window's setting")
    refused(
        lamp_world({"phase_window": 8, "phase_width": 0}),
        r"lamp\.phase_width must be an integer from 1 through 64",
    )
    alone = lamp_world({})
    alone["measured"][1]["table"] = {"light": {"phase_window": 8, "phase_width": 2}}  # type: ignore[index]
    parsed = parse_nature_beam_world(alone)
    assert parsed.measured[1].table[0] == "measure" and parsed.measured[1].widths == (2, None)
