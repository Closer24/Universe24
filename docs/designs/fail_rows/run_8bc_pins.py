"""The pins of RUN_8BC.md before the run (the FAIL Runner B, 2026-09-23;
docs/designs/fail_rows/RUN_8BC.md section 3): every number here is a
COMPUTATION from the engine's own tables of the declared world
`j2_massive.json` (loaded, never run) and the algebra of WHAT_IS_MISSING.md
section 1.9, printed with its kind. Two readings are computed side by
side: what the code reads at a reader (the path phase, the row's phase
less the record's birth coordinate u, `nature_beam.py` `_family_plan`)
and what section 1.9 pinned (the raw phase, u plus the turn), so that the
run's PASS / FAIL is judged against the first and the difference from the
second is on record before the run.

    PYTHONPATH=src .venv/bin/python docs/designs/fail_rows/run_8bc_pins.py
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import by_drive_rows, nature_beam_tables, window_admits
from event_universe.world_loading import load_world

HERE = Path(__file__).resolve().parent
WORLD = HERE / "j2_massive.json"
READERS = range(8, 136)
FAR = 190
FIRST, SECOND = 8, 9
# Nature's lower bound on the heaviest neutrino mass state over the
# electron's mass (the paper's Table 2 row 8c, PDG 2024 and KATRIN 2022).
NATURE_MASS_RATIO = 9.8e-8


def main() -> None:
    loaded = load_world(WORLD.read_text(encoding="utf-8"))
    world = loaded.world
    tables = nature_beam_tables(world)
    modulus = world.phase_steps
    heading = [i for i, v in enumerate(tables.flight.vectors) if tuple(v) == (1, 0, 0)][0]
    nu = [i for i, f in enumerate(world.families) if f.name == "nu"][0]
    ff = tables.family_flights[nu]
    lamp = world.measured[0].lamp
    assert lamp is not None
    rate, wall, start = int(ff.rate[heading]), int(ff.wall[heading]), int(ff.start[heading])
    numerator, denominator = int(ff.turn[heading][0]), int(ff.turn_denominator)
    print("THE WORLD, as loaded (COMPUTATION, the engine's tables at load, no run)")
    print(
        f"  model {world.model_id}; shape {list(world.shape)}; ticks {world.ticks}; N {modulus}; "
        f"K {world.K}; width {world.width}; action h {world.action}; massive_rows {world.massive_rows}"
    )
    print(
        f"  nu: quantum M {world.families[nu].quantum}, massive, p {world.families[nu].momentum_magnitude}; "
        f"the lamp's wheel {list(lamp.wheel)}, rate {list(lamp.rate)}, turns {list(lamp.turns)}"
    )
    print(
        f"  the heading (1, 0, 0): label p_D {ff.labels[heading].tolist()}, rest energy E'_0 {ff.rest}, "
        f"flight triple (rate {rate}, wall {wall}, start {start}): E'_D = isqrt(E'_0^2 + 3 p . p) = {wall // 2}"
    )
    print(
        f"  the turn table on the heading: numerator |p_x| N = {numerator} over the denominator h = {denominator}: "
        f"{numerator} / {denominator} = {numerator / denominator} steps per Link; "
        f"mod N the shift per Link is {numerator / denominator % modulus} (not 0: the edge case avoided)"
    )
    pace = rate / wall
    c_heading = 64 / 110
    print(
        f"  the pace on the heading |p_D|_1 / E'_D = {rate // 2} / {wall // 2} = {pace:.5f} Links per interval "
        f"(the photon's 64 / 110 = {c_heading:.5f}; the massive row is {100 * (1 - pace / c_heading):.2f} percent slower)"
    )

    # The arrival ages by the accumulator rule of the family's own table.
    ages = np.arange(0, 4 * FAR + 64, dtype=np.int64)
    made, _ = ff.accumulator(np.full(ages.shape, heading, dtype=np.int64), ages)
    made = np.asarray(made)

    def arrival_age(distance: int) -> int:
        return int(ages[np.flatnonzero(made >= distance)[0]])

    age_first, age_second, age_far = arrival_age(FIRST), arrival_age(SECOND), arrival_age(FAR)
    print("THE ARRIVALS (GAMEBOARD, the flight table: which births reach which Node within the run)")
    print(
        f"  the age at {FIRST} Links {age_first} (the photon's 13), at {SECOND} Links {age_second}, at {FAR} Links {age_far} (the photon's 326)"
    )
    births_first = world.ticks - age_first
    births_far = world.ticks - age_far
    print(
        f"  births at the ticks 1 .. {world.ticks} (one record per interval, the lamp's turn 1 at held K); "
        f"the rows born at the ticks 1 .. {births_first} reach x = {FIRST} within the run: {births_first} arrivals "
        f"= {births_first // modulus} turns of the wheel [1, 64] exactly; the rows born at the ticks 1 .. {births_far} "
        f"reach x = {FAR}: {births_far} (the registered photon world's 711)"
    )
    assert births_first == 1024 and births_first % modulus == 0

    # The turn along the path: ONE accumulator per row, by_drive_rows at every Link crossed on the x axis.
    shift = {}
    acc = np.zeros(1, dtype=np.int64)
    total = 0
    for x in range(1, FAR + 1):
        count, acc = by_drive_rows(acc, numerator, denominator)
        total += int(count[0])
        assert total == (numerator * x) // denominator
        shift[x] = total
    print(
        "THE TURN (COMPUTATION, `by_drive_rows(acc_turn, 14080, 1024)` per Link crossed; the count after x Links floor(55 x / 4))"
    )
    print(
        "  x: shift floor(55 x / 4), shift mod 64, the path phase the reader at x reads (lamp turn 0, so the path at birth is 0)"
    )
    for x in (8, 9, 10, 13, 14, 15, 72, 135, 190):
        print(f"  x = {x:3d}: {shift[x]:5d}  {shift[x] % modulus:2d}")

    # Reading A: what the code reads. The window at reader x reads the path phase (phase - u) mod N = shift(x) mod N.
    admits_all = [x for x in READERS if bool(window_admits((shift[x] - 0) % modulus, 1, modulus))]
    print(
        "READING A, what the run reads (COMPUTATION from `_family_plan`: path = (phase - birth) mod N; window centre 0, width 1)"
    )
    print(
        f"  every row of the beam carries the same path phase at a Node; the reader at x admits the whole beam that reaches it "
        f"if shift(x) mod 64 is in its window [0, 1), else nothing: the readers admitting everything among x = 8 .. 135: {admits_all}"
    )
    first_x = admits_all[0] if admits_all else None
    pins_a = {}
    for x in READERS:
        if x == first_x:
            # all its arrivals within the run: no reader before it took anything
            pins_a[x] = world.ticks - arrival_age(x)
        else:
            pins_a[x] = 0
    far_a = 0 if admits_all else births_far
    print(
        f"  PIN A1 the first reader (x = {FIRST}): {pins_a[FIRST]} of {births_first} arrivals (DETECTOR at the run)"
    )
    print(
        f"  PIN A2 the second reader (x = {SECOND}): {pins_a[SECOND]} of {world.ticks - age_second}; the ratio second / first: 0 / 0, undefined (COMPUTATION)"
    )
    if first_x is not None:
        print(
            f"  PIN A3 the reader at x = {first_x}: {pins_a[first_x]} of {pins_a[first_x]} arrivals (the age at {first_x} Links {arrival_age(first_x)}: "
            f"the births 1 .. {pins_a[first_x]} reach it; the whole beam that reaches it, the beat of the plane wave, {shift[first_x]} = {shift[first_x] // modulus} x 64 steps)"
        )
    print(
        f"  PIN A4 every other reader 0 (the reader at x = 135 reads a path phase 0 too, but nothing reaches it); "
        f"the far detector at x = {FAR}: {far_a} of {births_far} that would reach it"
    )

    # Reading B: the class filter of section 1.9 (if the window read u + shift): the reader at x takes the class u = -shift(x) mod N.
    classes = {}
    taken: set[int] = set()
    per_class = births_first // modulus
    pins_b = {}
    for x in READERS:
        c = (-shift[x]) % modulus
        classes[x] = c
        pins_b[x] = per_class if c not in taken else 0
        taken.add(c)
    covered = len(taken)
    print(
        "READING B, section 1.9's class filter (COMPUTATION; what the run would read if the window read the raw phase u + shift, which it does not)"
    )
    print(
        f"  {births_first} births over the wheel [1, 64]: {per_class} rows per class; the reader at x takes the class -shift(x) mod 64 if no reader before it took that class"
    )
    print(f"  PIN B1 the first reader (x = 8, the class {classes[8]}): {pins_b[8]} of {births_first}")
    print(
        f"  PIN B2 the second reader (x = 9, the class {classes[9]}): {pins_b[9]}; the ratio second / first {pins_b[9] / pins_b[8]:.3f} exactly (nature about 1 the thing compared with)"
    )
    print(
        f"  distinct classes among the 128 readers' shifts: {covered} of 64; the far detector by the algebra of 1.9: "
        f"1024 - 16 x {covered} = {births_first - per_class * covered}; within the run's {births_far} arrivals at x = {FAR}: "
        f"{max(0, births_far - per_class * covered) if covered < modulus else 0}"
    )
    first_full = next(x for x in READERS if len({classes[y] for y in range(8, x + 1)}) == modulus)
    print(
        f"  the classes are all covered by the reader at x = {first_full}; the readers behind it take 0 under reading B as well"
    )

    # 8c: the comparison side.
    m_e = math.ceil(1 / NATURE_MASS_RATIO)
    rest_e = 64 * world.width * m_e
    print(
        "ROW 8c (COMPUTATION, no run): the nu quantum 1 is the minimal mass; nature's bound on m_nu / m_e >= 9.8 x 10^-8 puts the electron's content at"
    )
    print(
        f"  M_e >= 1 / 9.8e-8 = {m_e} units ({m_e:.3e}); E'_0 = Q S_w M_e = 64 x {world.width} x {m_e} = {rest_e} ({rest_e:.3e}); "
        f"its square {rest_e * rest_e:.3e} against the working bound 2^63 - 1 = {(1 << 63) - 1:.3e} and the label bound 2^62 - 1 = {(1 << 62) - 1:.3e}: inside"
    )
    print(
        "  the register's electron today: the free family `e`, quantum 0, its measured event's amount its content (ENTITY_CATALOG.md, the electron's row): "
        "the quantum 1 for nu is a declaration on the nu family alone; the electron's content is not moved by this file"
    )


if __name__ == "__main__":
    main()
