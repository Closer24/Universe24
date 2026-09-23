"""The pins of RUN_8BC.md section 6 before the run (the FAIL Runner B,
2026-09-23, STEP 3a): the re-emitter world `j2_reemit.json` and its control
`j2_reemit_control.json`, loaded and never run; every number a COMPUTATION
from the engine's own tables (`nature_beam_tables`), its count primitive
(`by_drive_rows`) and its window (`window_admits`), printed with its kind.
The chain (section 6): the lamp's record (u = j, the wheel [1, 64]) turns
floor(55 x / 4) to the re-emitter at x = R, completes there (a `rerelease`
entry on a `sum` set: the record's one offer, its gather after step 4) and
is reborn in step 5 of the same interval at age 0 with the running phase
kept and a new u = 2 k from the re-emitter's wheel [2, 64] (k its ordinal,
k = j); behind it the path phase at y Links is shift(R) + shift(y) - j mod
64, so a reader with the window [0, 1) takes the one class j = shift(R) +
shift(y) mod 64. The control keeps the re-emitter's wheel [1, 64] (no lamp
block: u the count of births, as built), so the path phase behind it is
shift(R) + shift(y) for every row: the plane wave of section 3 again.

    PYTHONPATH=src .venv/bin/python docs/designs/fail_rows/run_8bc_reemit_pins.py
"""

from __future__ import annotations

import collections
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import by_drive_rows, nature_beam_tables, window_admits
from event_universe.world_loading import load_world

HERE = Path(__file__).resolve().parent
WORLD = HERE / "j2_reemit.json"
CONTROL = HERE / "j2_reemit_control.json"
R, FIRST, SECOND, FAR = 4, 8, 9, 190


def births_by_the_count_row(held: int, wall: int, ticks: int) -> list[int]:
    """The intervals with no birth of a lamp holding `held` at the clock's
    wall K (the count row `Count("turn", "content", ...)` replayed by the
    one primitive; one unit spent per birth, the lamp's turn 1 otherwise)."""
    acc = np.zeros(1, dtype=np.int64)
    skipped = []
    for tick in range(1, ticks + 1):
        count, acc = by_drive_rows(acc, held, wall)
        if int(count[0]) == 0:
            skipped.append(tick)
        held -= int(count[0])
    return skipped


def main() -> None:
    world = load_world(WORLD.read_text(encoding="utf-8")).world
    control = load_world(CONTROL.read_text(encoding="utf-8")).world
    tables = nature_beam_tables(world)
    modulus = world.phase_steps
    ticks = world.ticks
    heading = [i for i, v in enumerate(tables.flight.vectors) if tuple(v) == (1, 0, 0)][0]
    nu = [i for i, f in enumerate(world.families) if f.name == "nu"][0]
    ff = tables.family_flights[nu]
    lamp = world.measured[0].lamp
    reemitter = world.measured[1]
    assert lamp is not None and reemitter.lamp is not None
    numerator, denominator = int(ff.turn[heading][0]), int(ff.turn_denominator)
    print("THE WORLDS, as loaded (COMPUTATION, the engine's tables at load, no run)")
    print(
        f"  {world.model_id}: ticks {ticks}; K {world.K}; the lamp at x = 0 holds {world.measured[0].amount} = K + 1024, "
        f"wheel {list(lamp.wheel)}, p {world.families[nu].momentum_magnitude}; the re-emitter at x = {R} (family d, a `rerelease` "
        f"entry on the `sum` set 'reemit', weights [1], directions [[1, 0, 0]]) with the wheel {list(reemitter.lamp.wheel)} "
        f"on a lamp block of rate {list(reemitter.lamp.rate)} at held 1 (its turn 0 at every interval: it births nothing of its own); "
        f"the readers at x = {FIRST} and {SECOND} (window 0, width 1), the far detector at x = {FAR} (no window)"
    )
    assert control.measured[1].lamp is None
    print(
        f"  {control.model_id}: the same world, the re-emitter without a lamp block (its rebirths' u the count of births less one mod N, "
        f"the wheel [1, N] as built)"
    )
    print(
        f"  the nu tables on the heading: flight triple ({int(ff.rate[heading])}, {int(ff.wall[heading])}, {int(ff.start[heading])}), "
        f"the turn {numerator} over {denominator} = 55 / 4 steps per Link; the same as section 3"
    )

    # The lamp's births by the count row (COMPUTATION).
    for held, name in ((world.K, "K"), (world.K + 1, "K + 1"), (world.measured[0].amount, "K + 1024")):
        skipped = births_by_the_count_row(held, world.K, ticks)
        print(
            f"  the lamp's count row at held {name}: the intervals with no birth over {ticks}: {skipped or 'none'}"
            + (
                " (the remainder after t births is 1024 t - t (t - 1) / 2, above 0 through t = 2049; "
                "the count never 2, the gain below 2 K: every birth at the turn 1)"
                if name == "K + 1024"
                else ""
            )
        )
    assert not births_by_the_count_row(world.measured[0].amount, world.K, ticks)
    births = ticks  # one record per interval, at the ticks 1 .. T; the j-th birth (j from 0) at the tick j + 1

    # The flight by the family's accumulator (GAMEBOARD): the age at which a row has made d Links from a fresh start.
    ages = np.arange(0, 4 * FAR + 64, dtype=np.int64)
    made = np.asarray(ff.accumulator(np.full(ages.shape, heading, dtype=np.int64), ages)[0])

    def age_for(distance: int) -> int:
        return int(ages[np.flatnonzero(made >= distance)[0]])

    t_r = age_for(R)
    legs = {x: age_for(x - R) for x in (FIRST, SECOND, FAR)}
    print("THE FLIGHT (GAMEBOARD, the flight table): the row born at the tick t (age 0) reaches")
    print(
        f"  the re-emitter x = {R} at the tick t + {t_r} (step 4), is reborn there in step 5 of that interval at age 0,"
    )
    for x, leg in legs.items():
        print(f"  x = {x} at the tick t + {t_r} + {leg} = t + {t_r + leg}")

    # The turn (COMPUTATION): shift(d) = floor(14080 d / 1024) by by_drive_rows from a fresh accumulator.
    def shift(distance: int) -> int:
        acc = np.zeros(1, dtype=np.int64)
        total = 0
        for _ in range(distance):
            count, acc = by_drive_rows(acc, numerator, denominator)
            total += int(count[0])
        assert total == (numerator * distance) // denominator
        return total

    s_r = shift(R)
    path = {x: (s_r + shift(x - R)) % modulus for x in (FIRST, SECOND, FAR)}
    print(
        f"THE TURN (COMPUTATION): shift({R}) = {s_r} to the re-emitter (the remainder 0, and the rebirth starts a fresh accumulator); "
        f"behind it shift(y) = {shift(FIRST - R)}, {shift(SECOND - R)}, {shift(FAR - R)} at y = {FIRST - R}, {SECOND - R}, {FAR - R}; "
        f"the path phase of the j-th birth at x is (shift({R}) + shift(x - {R}) - j) mod 64: "
        f"{path[FIRST]} - j at x = {FIRST}, {path[SECOND]} - j at x = {SECOND}, {path[FAR]} - j at x = {FAR}"
    )
    classes = {x: path[x] for x in (FIRST, SECOND)}
    assert classes[FIRST] != classes[SECOND]
    for x in (FIRST, SECOND):
        assert bool(window_admits((path[x] - classes[x]) % modulus, 1, modulus))

    # The arrivals and the clicks (the pins).
    n_r = births - t_r  # the births that reach the re-emitter: t + t_r <= T
    n = {x: births - t_r - legs[x] for x in (FIRST, SECOND, FAR)}  # if nothing were taken before
    taken = {}
    taken[FIRST] = [j for j in range(n[FIRST]) if j % modulus == classes[FIRST]]
    arrivals_second = n[SECOND] - len([j for j in taken[FIRST] if j < n[SECOND]])
    taken[SECOND] = [j for j in range(n[SECOND]) if j % modulus == classes[SECOND]]
    far_taken_before = [j for j in taken[FIRST] + taken[SECOND] if j < n[FAR]]
    far_clicks = n[FAR] - len(far_taken_before)
    print("THE PINS OF THE RE-EMITTER WORLD (DETECTOR at the run; the arithmetic COMPUTATION)")
    print(
        f"  B0 the re-emitter: {n_r} records complete there (the births 1 .. {n_r}: one `gather` line each, chosen 'reemit') "
        f"and {n_r} are reborn (one `split` line with rebirth each, the new u = 2 k mod 64, k = 0 .. {n_r - 1}: the 32 even values)"
    )
    print(
        f"  B1 the first reader (x = {FIRST}): {len(taken[FIRST])} clicks of {n[FIRST]} arrivals, the one class j = {classes[FIRST]} mod 64 "
        f"(j = {taken[FIRST][0]}, {taken[FIRST][1]}, ..., {taken[FIRST][-1]}); {n[FIRST]} = 16 x 64 arrivals, 16 per class"
    )
    print(
        f"  B2 the second reader (x = {SECOND}): {len(taken[SECOND])} clicks of {arrivals_second} arrivals "
        f"({n[SECOND]} would reach it, less the {len([j for j in taken[FIRST] if j < n[SECOND]])} the first reader took), "
        f"the fresh class j = {classes[SECOND]} mod 64 (j = {taken[SECOND][0]}, ..., {taken[SECOND][-1]}); "
        f"the ratio second / first = {len(taken[SECOND])} / {len(taken[FIRST])} = {len(taken[SECOND]) / len(taken[FIRST]):.3f} (nature about 1)"
    )
    print(
        f"  B3 the far detector (x = {FAR}): {far_clicks} clicks of {n[FAR]} that reach it within the run "
        f"({n[FAR]} births, less the {len([j for j in taken[FIRST] if j < n[FAR]])} of the class {classes[FIRST]} and the "
        f"{len([j for j in taken[SECOND] if j < n[FAR]])} of the class {classes[SECOND]} among the births 1 .. {n[FAR]}); "
        f"the fraction {far_clicks / n[FAR]:.4f} (62 / 64 = {62 / 64:.4f} in the limit; nature's near-total passage)"
    )
    dist = collections.Counter((path[FIRST] - j) % modulus for j in range(n[FIRST]))
    print(
        f"  B4 the `pass` lines at x = {FIRST}: `phase - u` = ({path[FIRST]} - j) mod 64 over the {n[FIRST]} arrivals, "
        f"the {len(dist)} values with {min(dist.values())} to {max(dist.values())} rows each; the admitted rows those with `phase - u` = 0 "
        f"(GAMEBOARD, the row's columns on the reader's line; the class filter visible)"
    )
    # The control.
    c_far = n[FAR]
    print(
        "THE PINS OF THE CONTROL (the re-emitter's wheel [1, 64]: u_new = k = j, the path phase shift(R) + shift(y) for every row)"
    )
    print(
        f"  C1 the first reader (x = {FIRST}): the path phase {path[FIRST]} for every row, not 0: 0 clicks of {n[FIRST]}; "
        f"C2 the second reader (x = {SECOND}): {path[SECOND]}, not 0: 0 of {n[SECOND]}; "
        f"C3 the far detector: {c_far} of {c_far}, every row that reaches it; the re-emitter {n_r} completions and rebirths as B0"
    )
    print(
        "THE EDGE CASES (COMPUTATION): the same wheel at both, the control above (the plane wave of section 3); "
        "the shift per Link 0 mod N (p = 2^12 at h = 2^10): the path phase behind the re-emitter is -j mod 64 with no turn, "
        "the readers still class filters (the classes come from the two wheels, the turn only fixes which class each reader takes)"
    )


if __name__ == "__main__":
    main()
