# Animate's toys for the clocks' roots (the owner's word of 2026-10-28, 15:2x UTC)

**Record:** these probes run the old engine (src/event_universe) or read its records, which the owner's word of
2026-10-30, 09:2x UTC, takes out ("only the new engine matters"). They stand for their findings, cited by the
pages that name them, and are not run on the new engine.

The page is ANIMATE-CLOCK-ROOTS.md. These are toys that check whether a law would work in an engine. Nothing here is engine code, and nothing was pushed to an engine branch. Both run with no engine: `python -I local_tick.py` and `python -I kind_kept.py` (the second reads ANIMATE-PROBES-2/kinds_ladder.py and ANIMATE-PROBES-3/ladder_pauli.py).

## local_tick.py: law A, a clock's time is the carry of its own dial

- **The board:** a ring of 60 clocks in exact rationals, each a hand of two slots stepped by the one formula with the coupling c d^2, d its own tick. A patch of 20 clocks asks for c = 27/25, past the light cone at c = 1.
- **The reads:** every clock reads its neighbours where they stand at its own moment.
- **Four runs of one pulse:** one tick for all; the clamp; the local tick (the patch's clocks tick twice per great tick); every clock at half a tick (the reference).
- **The output (local_tick.txt):**
  - one tick for all grows past 10^6 by tick 48;
  - the clamp holds, with the patch's light held to the full rate;
  - the local tick holds, its front reaches the probe a tick sooner, and the rewind is exact over 9,600 events.

## kind_kept.py: law C, every carry keeps the kind, and the ladder by the light's family

- **The lays under the 24's lifts** (24 classes closed from three generators): the head's (the up twin at one end, the down at the other), the singlet and the vector lay along the Mesh.
- **The children's own states.**
- **The ladder per bang** from four calibres: the light A1 or T1, each with and without the twin hands.
- **The output (kind_kept.txt):**
  - the head's lay keeps the 24 at 12 of 72 cases, the singlet and the vector at 72 of 72;
  - a child is S = (0, 0, 1) under the head's lay and S = 0 under the other two;
  - the light A1 alone stays at A1, and the light T1 alone reaches the 24's five kinds by bang 3;
  - with the twin hands all eight kinds stand at bang 4 (A1 light) or 3 (T1 light).

## twin_flip.py: the choice carried into the next bang

- **Beside many_bangs.py,** on draft C's tree at 33d9ecaa (copied here at its version for this run): the twin calibre, the dial variant read at the step, T = J K.
- **It prints** which twin holds more at four clocks at every top and bottom.
- **The output (twin_flip.txt):** up, down, up, down at clock (0, 0, 0) through the 7th to the 10th bangs, the opposite at its neighbours, and the flip overwritten by the new births of the 11th bang.

## chosen_path.py: the chosen path carried into the next bang

- **Pure integers, no engine:** `python -I chosen_path.py`. One Node-clock over 4,096 bangs:
  - the record of each click stands as the next click's detector, with no act at the top (decision 27, the owner's word to the Boss of 2026-10-29, 06:3x UTC);
  - `--former` runs the former turnover, which reversed the record (S to -S), for comparison (chosen_path_former.txt);
  - four rules for what crosses into the next bang: nothing, the record as the detector, and the record also bending the next child fully or halfway.
- **The output (chosen_path.txt):**
  - with nothing crossing, the next choice is on the last choice's line a third of the time;
  - with the record, always;
  - the last choice repeated a half, all and three quarters of the time.
- **Under the former turnover** the same counts read reversed: the line is carried either way, and its sense is the act at the top's alone.
- **The 24** (the owner's word of 15:48 UTC: a generic law, a tensor one): the same draws with every frame turned by each of the 24 turns.
  - Every rule, built from the A1 contraction, turns its choices with the frame under 24 of 24 turns.
  - A mutant that reads the z parts alone keeps it under 16 of 24, parting at the 8 turns that carry its run's line onto the z line.

## composite_climb.py: does the chosen path build ever more complex clocks?

- **Exact fractions and complex doubles, no engine:** `python -I composite_climb.py` (a few minutes). The owner's word of 15:57 UTC.
  - No act at the top (decision 27); `--former` runs the former turnover, T on every gear, for comparison (composite_climb_former.txt).
  - `--seed N` sets the stream: SHA-256 of the seed and a counter, each rule on its own stream.
- **Part 1 (exact):** T, each kind's time reversal, keeps a kind where every turn is conjugate to its own reverse. No act applies T; the count reads it. The 24 keep all 5 kinds (all 8 with the twins' lifts); the mutant, the tetrahedron's 12 turns, keeps 2 of 4 (3 of 7).
- **Part 2:** the eight kinds built from the twins by meeting one more twin, checked against the characters: their rungs, T T (+1 on the five integer kinds, -1 on the three spinor kinds), and which hold a direction (all but A1, A2 and E).
- **Part 3:** one composite meets one new twin per bang (the plan's item (t)), 2,048 runs per rule over 24 bangs.
  - The mean rung at bang 24: 2.00 with nothing crossing, 2.54 with the twin laid against the composite, 3.28 on its line, 3.75 half along, 4.06 wholly along.
  - The top kind A2 reached by 0, 0, 24, 51 and 68 percent of the runs.
  - Wholly along, no run holds a direction at bang 4: along a cube axis four twins click into E or T2 with none.
- **The act at the top does not move the climb.** Over the seeds 2026, 11, 23, 37 and 59, with no act and with the former turnover alike:
  - wholly along: 4.06 to 4.13, and A2 reached by 66 to 69 percent;
  - half along: 3.71 to 3.79, and 49 to 53 percent;
  - on its line: 3.19 to 3.28, and 22 to 26 percent;
  - against: 2.51 to 2.57, and 0.
- **The former stream:** a linear congruential walk's bit 16, which repeats every 2^17 bits, so a rule's 2,048 runs replayed part of it: 1,190 to 1,520 distinct paths of 2,048, against 2,040 to 2,048 on the new stream. Its numbers (4.13, 3.72, 3.24 and 2.53; 68, 50, 23 and 0 percent) lie inside the spread above.

---
Animate, reader-5.
