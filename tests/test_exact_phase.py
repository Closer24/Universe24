"""The exact phase at the click (2026-09-21; the model owner's decision,
record 163 (2) of docs/LOG_2026-09-20.md; the mathematician's
docs/designs/fraction_free/TWO_SLITS.md section 2; BEAM_LAW note 45): a
row's phase is read at its click at the exact time of its last Link,
phi = (n / d) x made x T_d / (S_1 Q) from the row's two counts (the phase
per interval of age, the pair form, and the flight table's count of Links),
one floor at the click, a Euclidean division with the remainder kept on the
click line (`exact`, `remainder`), no float. The expected integers of
docs/TEST_EXPECTATIONS.md ("The exact phase at the click"), written down
before the first run:

(a) the axis: a lamp of the pair form [8, 1] (8 steps per interval) on +x
    to a counter 17 Links away (T_d = 110, S_1 = 1, Q = 64): every record's
    row clicks at the age 29 with the phase u + 40 as the walk turned it
    (8 x 29 mod 64), and the exact phase u + 41 with the remainder [48, 64]
    (8 x 17 x 110 = 14960 = 233 x 64 + 48, 233 = 41 mod 64: the 41.75 of
    the design's cone), on the click line and read by the layer;
(b) the diagonal (1, 1, 0) to a counter 24 Links along the staircase
    (T_d = 156, S_1 = 2): the age 29, the walk's phase u + 40, the exact
    phase u + 42 with the remainder [0, 128] (8 x 24 x 156 = 29952 = 234 x
    128 exactly, the edge of a whole exact phase);
(c) the integer form (3 per Link crossed, no pair form): the click line
    carries no `exact` and no `remainder`, the phase being exact per Link;
(d) a face: a lamp of [8, 1] on +x five Links from the open face +x: the
    row leaves through the face at the walk of the age 7 (m(8) = 5), read
    before that walk's turn with the phase u + 56 (seven intervals), and
    its exact phase is u + 4 with the remainder [48, 64] (8 x 5 x 110 =
    4400 = 68 x 64 + 48, 68 = 4 mod 64), on the face's click line;
(e) the bound: the pair form [2^55, 1] loads on a bar of age bound 100
    ((age_bound + 1) x n within 2^62 - 1) and the click 17 Links away is
    refused naming the exact phase, the measured event (the counter, 1)
    and the numerator 2^55 x 17 x 110 beyond the working bound 2^63 - 1;
(f) the primitive itself: `exact_phase` on the flight of +x and
    (1, 1, 0) gives (a), (b) and (d) from the phase, the terms and the age
    of the last Link; a rest slot and a family without the pair form return
    the phase with the remainder 0 over 1.
"""

from __future__ import annotations

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import REST_DIRECTIONS, direction_flight, exact_phase

N = 64
K = 1 << 20
RATE = [8, 1]


def world(
    lamp_directions: list[list[int]],
    shape: list[int],
    counters: list[list[int]],
    phase_per_link: object = RATE,
    ticks: int = 40,
    **keys: object,
) -> dict[str, object]:
    found: dict[str, object] = {
        "law": "beam",
        "model_id": "beam-exact-phase-test",
        "shape": shape,
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": K,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1, "phase_per_link": phase_per_link}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "light",
                "amount": K,
                "fixed": True,
                "lamp": {"wheel": [1, N], "rate": [1, 1], "directions": lamp_directions},
            },
            *(
                {"position": position, "family": "light", "amount": 1, "fixed": True}
                for position in counters
            ),
        ],
        "detectors": [
            {"name": f"counter_{k}", "positions": [position], "reading": "sum"}
            for k, position in enumerate(counters)
        ],
    }
    found.update(keys)
    return found


def lines_of(declared: dict[str, object]) -> list[dict[str, object]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(declared), observer=lines.append)
    for _ in range(int(declared["ticks"])):  # type: ignore[call-overload]
        simulation.step()
    return lines


def clicks_of(lines: list[dict[str, object]], detector: str) -> list[dict[str, object]]:
    births = {line["record"]: line for line in lines if line["event"] == "birth"}
    found = []
    for line in lines:
        if line["event"] == "click" and line["detector"] == detector and "record" in line:
            found.append({**line, "birth_u": births[line["record"]]["u"]})
    return found


def test_the_axis_and_the_diagonal_read_the_exact_phase():
    """(a) and (b)."""
    lines = lines_of(
        world([[1, 0, 0]], [19, 1, 1], [[17, 0, 0]], boundary={"y": "periodic", "z": "periodic"})
    )
    clicks = clicks_of(lines, "counter_0")
    assert len(clicks) >= 8
    for click in clicks:
        u = click["birth_u"]
        assert click["age"] == 29
        assert (click["phase"] - u) % N == 40
        assert (click["exact"] - u) % N == 41
        assert click["remainder"] == [48, 64]
    lines = lines_of(
        world(
            [[1, 1, 0]], [14, 14, 1], [[12, 12, 0]], boundary={"z": "periodic"}, directions=[[1, 1, 0]]
        )
    )
    clicks = clicks_of(lines, "counter_0")
    assert len(clicks) >= 8
    for click in clicks:
        u = click["birth_u"]
        assert click["age"] == 29
        assert (click["phase"] - u) % N == 40
        assert (click["exact"] - u) % N == 42
        assert click["remainder"] == [0, 128]


def test_the_layer_reads_the_exact_phase():
    """(a): the gather's pointer is at the exact phase, one cell per record."""
    lines = lines_of(world([[1, 0, 0]], [19, 1, 1], [[17, 0, 0]]))
    records = [line for line in lines if line["event"] == "record"]
    assert records
    from event_universe.core.phase import phase_cosines, phase_sines

    births = {line["record"]: line for line in lines if line["event"] == "birth"}
    for line in records:
        u = births[line["of"]]["u"]
        phase = (u + 41) % N
        assert line["pointer"] == [32 * phase_cosines(N)[phase], 32 * phase_sines(N)[phase]]


def test_the_integer_form_carries_no_exact_phase():
    """(c)."""
    lines = lines_of(world([[1, 0, 0]], [19, 1, 1], [[17, 0, 0]], phase_per_link=3))
    clicks = clicks_of(lines, "counter_0")
    assert len(clicks) >= 8
    for click in clicks:
        assert "exact" not in click and "remainder" not in click
        assert (click["phase"] - click["birth_u"]) % N == 51


def test_a_face_reads_the_exact_phase_of_the_link_it_leaves_through():
    """(d)."""
    declared = world([[1, 0, 0]], [5, 1, 1], [], ticks=30)
    declared["boundary"] = {"y": "periodic", "z": "periodic"}
    lines = lines_of(declared)
    births = {line["record"]: line for line in lines if line["event"] == "birth"}
    clicks = [line for line in lines if line["event"] == "click" and line["detector"] == "face:+x"]
    assert len(clicks) >= 8
    for click in clicks:
        u = births[click["record"]]["u"]
        assert (click["phase"] - u) % N == 56
        assert (click["exact"] - u) % N == 4
        assert click["remainder"] == [48, 64]


def test_the_numerator_beyond_the_register_is_refused():
    """(e)."""
    declared = world([[1, 0, 0]], [19, 1, 1], [[17, 0, 0]], phase_per_link=[1 << 55, 1], age_bound=100)
    # Since the generic entry of the bending (2026-09-22) the engine hands the
    # one form of the last Link's time, n x (age r - s + T d) with r = 2 S_1 Q
    # (here 17 x 220 = 3740, the same time as the count's 17 x 110 over
    # S_1 Q); before it the refusal named n x made x T_d, "... x 17 x 110".
    with pytest.raises(
        OverflowError, match=r"the exact phase at measured event 1: .*36028797018963968 x 3740"
    ):
        lines_of(declared)


def test_the_primitive():
    """(f)."""
    flight = direction_flight(((1, 0, 0), (1, 1, 0), (0, 0, 0)))
    assert exact_phase(40, 29, 29, 0, flight, (8, 1), N, "a") == (41, 48, 64)
    assert exact_phase(40, 29, 29, 1, flight, (8, 1), N, "a") == (42, 0, 128)
    assert exact_phase(56, 7, 8, 0, flight, (8, 1), N, "a") == (4, 48, 64)
    assert exact_phase(51, 29, 29, 0, flight, None, N, "a") == (51, 0, 1)
    assert exact_phase(9, 5, 5, 2, flight, (8, 1), N, "a") == (9, 0, 1)
    assert REST_DIRECTIONS >= 1
    with pytest.raises(OverflowError, match="the exact phase at here"):
        exact_phase(0, 29, 29, 0, flight, (1 << 55, 1), N, "here")
