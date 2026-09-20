"""Write the worlds of the Bell run with the choosers on the GameBoard
(issue #363; the register entry "A2 with the choosers on the GameBoard
(2026-09-20)" in docs/EXPERIMENTS.md; the dictionary in README.md here).

A2's bar of 21 x 1 x 1 with the pair lamp of `light` at x = 10 releasing
one ray on +X and one on -X per interval with its clock phase (content
K + 2: the release of age a carries the phase a mod 64), and four counters
of content 1 (each its own `wave` detector of threshold 1) whose windows on
`light` are not written in the file but read from the phase of a ray
arriving from a third and a fourth source (`phase_window` `{"reads":
"<family>", "offset": s}`, docs/ENGINE.md): Alice's from the free family
`sa`, released by a lamp at x = 0 toward +X, Bob's from `sb`, released by a
lamp at x = 20 toward -X. `sa` and `sb` pass through everything else (the
counters' and the lamps' tables declare `pass`) and escape through the
faces; different families never collide.

Why the counters are where they are, and why the setting lamps have the
clocks they have (derived before the run from the engine's own flight table
and `by_clock`; nothing here is tuned to a result):

- A setting is the phase of the coherent pointer of the setting rows
  present at the counter's Node. A ray of a heading dwells 1 or 2 intervals
  at a Node (the flight table: 32 Links per 55 intervals), so with one row
  per interval a Node holds a constant 1 or 2 rows: the Nodes at 4 and 7
  Links from a lamp hold one (the flight ages 7 and 12), the Nodes at 2 and
  3 Links hold two (the ages 3, 4 and 5, 6). Alice's counters are at 7
  (plus) and 4 (minus) Links from her lamp, one row each: the setting is a
  ray's phase exactly. Bob's are at 3 (plus, x = 17) and 2 (minus, x = 18)
  Links from his, two rows each of consecutive releases: the setting is the
  pointer of two phases, the bisector of the two, its nearest step.
- The two counters of a side must read the SAME setting for one pair, or
  the minus window is not the exact complement of the plus window and
  pairs are lost. The pair ray meets the plus counter first and the minus
  counter tau intervals later, when the stream at the minus Node is a
  fixed number of releases further on: 10 releases for Alice (tau = 5, the
  flight ages 7 and 12), 3 for Bob (tau = 1, the ages 5, 6 and 3, 4). So
  the phase of the stream must be periodic in the releases with a period
  that divides the shift: Alice's lamp turns 64 / 5 steps per interval on
  average (content 64 K / 5: the turns 12, 13, 13, 13, 13, the phases
  0, 12, 25, 38, 51 and again, the period 5), Bob's 64 / 3 (content
  64 K / 3: the turns 21, 21, 22, the period 3). With `offset` 32 on the
  minus counters the two windows of a side cover the circle exactly.
- The periods 5 and 3 are odd, coprime to each other and to the circle of
  64: over 15 consecutive pairs every (a, b) combination occurs once, and
  over 15 x 64 = 960 pairs every combination meets every phase of the pair
  lamp exactly once. A two-valued setting from one clock (the owner's
  0 / 16) is impossible without a period that divides 64 (a stride of 16
  has period 4; a stride of 32, half the circle, is refused): such a
  setting would share a residue of the interval with the pair's phase and
  each bin would see a quarter of the phases, a correlation built by the
  file. The odd periods are the generic choice.
- The three lamps share nothing: the pair lamp turns 1 step per interval
  from the phase 0 (content K + 2), Alice's lamp 12 or 13 from the phase 7,
  Bob's 21 or 22 from the phase 40; the setting lamps are free events (a
  release costs nothing, so their turn stays exactly periodic; a paid lamp
  spends its content and its turn drifts), released at the world's rate
  `release` [1, 2^26]: 3 rays per interval of `sa` (as one row) and 5 of
  `sb`, so the pointer's phase is the same as for one row. The counters'
  offsets (`OFFSET_A`, `OFFSET_B`) place Alice's settings at 0, 12, 25, 38,
  51 and Bob's smallest at 8; the settings are then 0/25 for Alice and
  8/29 for Bob on the CHSH quadruple, an ordered quadruple within a half
  circle on which the triangle gives S = 2 exactly.
- The pair ray of age a (released at tick a + 1) reaches x = 7 at tick
  a + 6, x = 4 at a + 11, x = 17 at a + 13 and x = 18 at a + 14 (the flight
  ages 5, 10, 12, 13). The first `sa` ray (released at tick 1) reaches x = 7
  at tick 13, so the pairs of the ages 0..6 meet no setting at Alice's plus
  counter and are the warm-up the reader excludes; from a = 7 every
  counter has a setting at every pair. 1920 pairs (two rounds of the 960)
  are analysed, the ages 7..1926, and 1940 intervals hold the last minus
  click (a + 14).

The worlds (`beam-bell-choosers-<name>-v1`):

- `read.json`: the run, the windows read from the streams.
- `written_a<a>_b<b>.json`: control 1, the same GameBoard and streams with
  the windows written in the file (A2's form) at the four settings of the
  CHSH quadruple; 128 pairs each; S = 2 exactly.
- `fixed.json`: control 2, the streams released with the settings fixed
  (the lamps' contents below K: the turn 0, one phase each, at the world's
  rate `release` [1, 1]); Alice's setting 0 and Bob's 8 throughout; E(0, 8)
  = 1/2 as in A2.
- `one_clock.json`: control 3, the three lamps fed from one clock (the
  setting lamps with the pair lamp's stride 1 and phase 0, content K at
  `release` [1, K]: one ray per interval): a correlation built in on
  purpose, to be seen.

    python examples/events/bell/make_chooser_worlds.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.events.nature_beam import (  # noqa: E402
    coherent_pointer,
    nature_beam_tables,
    pointer_phases,
)
from event_universe.events.world import parse_nature_beam_world  # noqa: E402

N = 64
# K divisible by 15 so that 64 K / 5 and 64 K / 3 are whole contents, and
# large enough that the pair lamp's turn stays exactly 1 over the run: its
# content K + 2 falls by 2 per interval, and the turn `by_clock(a, M, K)`
# loses a step once a x (K + 2 - M) reaches K (at K = 15 x 2^16 that was at
# the age 700 of 1940; here a x 2 a stays below K / 2).
K = 15 << 20
LAMP_X = 10
SHAPE = [2 * LAMP_X + 1, 1, 1]
# Alice's lamp (`sa`) at x = 0 toward +X; Bob's (`sb`) at x = 20 toward -X.
SA_X, SB_X = 0, 2 * LAMP_X
# The counters: Alice's plus at 7 Links from her lamp and minus at 4 (one
# setting row each), Bob's plus at 3 Links from his and minus at 2 (two rows).
ALICE_PLUS, ALICE_MINUS = SA_X + 7, SA_X + 4
BOB_PLUS, BOB_MINUS = SB_X - 3, SB_X - 2
# The setting lamps' periods, contents, starting phases and rate.
PERIOD_A, PERIOD_B = 5, 3
CONTENT_A, CONTENT_B = 64 * K // PERIOD_A, 64 * K // PERIOD_B
PHASE_A, PHASE_B = 7, 40
RELEASE = [1, 1 << 26]
ROWS_A, ROWS_B = CONTENT_A // RELEASE[1], CONTENT_B // RELEASE[1]
# The pair ray's flight ages at the counters (the flight table: m(5) = 3,
# m(10) = 6, m(12) = 7, m(13) = 8 Links), so its tick is the age + 1 + these.
FLIGHT = {ALICE_PLUS: 5, ALICE_MINUS: 10, BOB_PLUS: 12, BOB_MINUS: 13}
OFFSETS = {x: flight + 1 for x, flight in FLIGHT.items()}
# The first pair with a setting at every counter (the first `sa` ray, born
# at tick 1, reaches x = 7 at tick 13 = a + 6) and the pairs analysed.
FIRST = 7
PAIRS = PERIOD_A * PERIOD_B * N * 2
CONTROL_PAIRS = 2 * N
# The setting the smallest of Bob's values is placed at, and the CHSH
# quadruple (Alice's 0 and 25, Bob's 8 and the value 21 steps on).
BOB_LOWEST = 8
CHSH_ALICE = (0, 25)


def counter(x: int, window: object, extra: dict[str, object]) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": "counter",
        "amount": 1,
        "fixed": True,
        "table": {"light": {"phase_window": window}, **extra},
    }


def setting_lamp(x: int, family: str, content: int, phase: int, other: str) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": family,
        "amount": content,
        "phase": phase,
        "fixed": True,
        "directions": [[1, 0, 0]] if x == SA_X else [[-1, 0, 0]],
        "table": {"light": "pass", other: "pass"},
    }


def base(
    name: str,
    ticks: int,
    windows: dict[int, object],
    release: list[int],
    contents: tuple[int, int],
    phases: tuple[int, int],
) -> dict[str, object]:
    passes = {"sa": "pass", "sb": "pass"}
    return {
        "law": "beam",
        "model_id": f"beam-bell-choosers-{name}-v1",
        "shape": SHAPE,
        "boundary": "open",
        "ticks": ticks,
        "K": K,
        "N": N,
        "release": release,
        "suspension": 0,
        "families": [
            {"name": "light", "quantum": 1},
            {"name": "counter", "quantum": 1},
            {"name": "sa", "quantum": 0},
            {"name": "sb", "quantum": 0},
        ],
        "measured": [
            {
                "position": [LAMP_X, 0, 0],
                "family": "light",
                "amount": K + 2,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": [[1, 0, 0], [-1, 0, 0]]},
                "table": passes,
            },
            counter(ALICE_PLUS, windows[ALICE_PLUS], passes),
            counter(ALICE_MINUS, windows[ALICE_MINUS], passes),
            counter(BOB_PLUS, windows[BOB_PLUS], passes),
            counter(BOB_MINUS, windows[BOB_MINUS], passes),
            setting_lamp(SA_X, "sa", contents[0], phases[0], "sb"),
            setting_lamp(SB_X, "sb", contents[1], phases[1], "sa"),
        ],
        "detectors": [
            {"name": "alice_plus", "positions": [[ALICE_PLUS, 0, 0]], "threshold": 1},
            {"name": "alice_minus", "positions": [[ALICE_MINUS, 0, 0]], "threshold": 1},
            {"name": "bob_plus", "positions": [[BOB_PLUS, 0, 0]], "threshold": 1},
            {"name": "bob_minus", "positions": [[BOB_MINUS, 0, 0]], "threshold": 1},
        ],
    }


def reads(family: str, offset: int) -> dict[str, object]:
    return {"reads": family, "offset": offset % N}


def bisector(first: int, second: int, amount: int, cosines: np.ndarray, sines: np.ndarray) -> int:
    """The nearest step of the pointer of two rows of one amount at two
    phases, the engine's own reading (`coherent_pointer`, `pointer_phases`)."""
    x, y = coherent_pointer(
        np.array([amount, amount], dtype=np.int64),
        np.array([first % N, second % N], dtype=np.int64),
        np.zeros(1, dtype=np.int64),
        cosines,
        sines,
    )
    (step,) = pointer_phases(x, y, cosines, sines)
    assert step is not None
    return step


def raw_settings() -> tuple[list[int], list[int]]:
    """The settings the counters read before any offset, from the design:
    Alice's the phases of her lamp's releases 12, 13, 13, 13, 13 apart
    (one row at her counters), Bob's the bisectors of two consecutive
    releases 21, 21, 22 apart (two rows at his), read with the engine's
    tables at N = 64."""
    tables = nature_beam_tables(parse_nature_beam_world(read_world({x: 0 for x in FLIGHT})))
    alice = sorted({(PHASE_A + k * CONTENT_A // K) % N for k in range(PERIOD_A)})
    bob = sorted(
        {
            bisector(
                PHASE_B + k * CONTENT_B // K,
                PHASE_B + (k + 1) * CONTENT_B // K,
                ROWS_B,
                tables.cosines,
                tables.sines,
            )
            for k in range(PERIOD_B)
        }
    )
    return alice, bob


def read_world(windows: dict[int, object]) -> dict[str, object]:
    return base(
        "read",
        FIRST + PAIRS - 1 + max(OFFSETS.values()),
        windows,
        RELEASE,
        (CONTENT_A, CONTENT_B),
        (PHASE_A, PHASE_B),
    )


def offsets() -> tuple[int, int]:
    """The counters' offsets: Alice's puts her lowest raw setting at 0,
    Bob's puts his lowest at `BOB_LOWEST`."""
    alice, bob = raw_settings()
    return (-alice[0]) % N, (BOB_LOWEST - bob[0]) % N


def settings() -> tuple[list[int], list[int]]:
    """The settings of the run after the offsets, sorted: Alice's five and
    Bob's three."""
    alice, bob = raw_settings()
    offset_a, offset_b = offsets()
    return sorted((a + offset_a) % N for a in alice), sorted((b + offset_b) % N for b in bob)


def chsh_quadruple() -> tuple[tuple[int, int], tuple[int, int]]:
    """Alice's 0 and 25 with Bob's lowest two settings (8 and the one 21
    steps on): a < b < a' < b' within a half circle."""
    _, bob = settings()
    return CHSH_ALICE, (bob[0], bob[1])


def worlds() -> dict[str, dict[str, object]]:
    offset_a, offset_b = offsets()
    found: dict[str, dict[str, object]] = {}
    found["read"] = read_world(
        {
            ALICE_PLUS: reads("sa", offset_a),
            ALICE_MINUS: reads("sa", offset_a + N // 2),
            BOB_PLUS: reads("sb", offset_b),
            BOB_MINUS: reads("sb", offset_b + N // 2),
        }
    )
    (alice_a, alice_a2), (bob_b, bob_b2) = chsh_quadruple()
    control_ticks = CONTROL_PAIRS - 1 + max(OFFSETS.values())
    for a in (alice_a, alice_a2):
        for b in (bob_b, bob_b2):
            found[f"written_a{a}_b{b}"] = base(
                f"written-a{a}-b{b}",
                control_ticks,
                {
                    ALICE_PLUS: a,
                    ALICE_MINUS: (a + N // 2) % N,
                    BOB_PLUS: b,
                    BOB_MINUS: (b + N // 2) % N,
                },
                RELEASE,
                (CONTENT_A, CONTENT_B),
                (PHASE_A, PHASE_B),
            )
    # Control 2: the settings fixed. The lamps' contents are the rows per
    # interval at `release` [1, 1] (the turn 0 at K: the phase never turns);
    # Alice's rays carry the phase 0 and Bob's the phase 8, the offsets 0.
    found["fixed"] = base(
        "fixed",
        FIRST + CONTROL_PAIRS - 1 + max(OFFSETS.values()),
        {
            ALICE_PLUS: reads("sa", 0),
            ALICE_MINUS: reads("sa", N // 2),
            BOB_PLUS: reads("sb", 0),
            BOB_MINUS: reads("sb", N // 2),
        },
        [1, 1],
        (ROWS_A, ROWS_B),
        (0, BOB_LOWEST),
    )
    # Control 3: one clock. The setting lamps turn 1 step per interval from
    # the phase 0 as the pair lamp does (content K at `release` [1, K]: one
    # ray per interval), the offsets 0.
    found["one_clock"] = base(
        "one_clock",
        FIRST + PAIRS - 1 + max(OFFSETS.values()),
        {
            ALICE_PLUS: reads("sa", 0),
            ALICE_MINUS: reads("sa", N // 2),
            BOB_PLUS: reads("sb", 0),
            BOB_MINUS: reads("sb", N // 2),
        },
        [1, K],
        (K, K),
        (0, 0),
    )
    return found


def main() -> None:
    alice, bob = settings()
    offset_a, offset_b = offsets()
    print(f"offsets: Alice {offset_a}, Bob {offset_b}; settings: Alice {alice}, Bob {bob}")
    print(f"CHSH quadruple: {chsh_quadruple()}")
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
