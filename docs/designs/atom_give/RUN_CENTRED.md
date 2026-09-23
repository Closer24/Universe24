# The one run of hydrogen at r = 12 under the centred step (centred-step-v1), read by kind against the pins of CENTRED_STEP.md section 4

The Atom Give Designer 2, 2026-09-22, step 3 of the Boss's order of
12:10Z (record 953) under the owner's word of record 958 (the atom is out
of the paper; the key's build and the one run closed within about 45
minutes of host time if the fix is as small as it looks). The world:
`examples/events/atoms/hydrogen_r12_centred.json`, the registered
`hydrogen_r12.json` plus the world key `centred_step: true` and its own
model id, nothing else (the test `test_centred_step.py` (e) asserts it
integer for integer). The pins are those of
[CENTRED_STEP.md](CENTRED_STEP.md) section 4, declared before the run
from the kick map; NO PIN WAS MOVED AFTER THE RUN. The reading is the
Atom Baseline Runner's method ([baseline_readings.py](../atom_baseline/baseline_readings.py),
imported by [centred_readings.py](centred_readings.py), nothing copied),
its printout [centred_readings.out](centred_readings.out); every number
DETECTOR (the faces' clicks, the arrival Nodes, the crossings) or
GAMEBOARD (the step lines, the host's tick) as the runner labels them.
Bohr's whole number and Kepler's period appear only on the comparison
side (record 817).

**The verdict in one line.** THE LOOP STAYS: 7500 intervals on the
board, 23 axis crossings, five returns to the +x axis, no escape
(DETECTOR), against the baseline's one crossing of the +x axis and the
escape through `face:+y` at 3407 on the same world without the key
(RUN.md section 4): the cause read in CAUSE.md (the drive's step lagging
the Node half a Link per axis behind the accumulated motion, the push
read there turned along the motion) is confirmed on the lattice with the
fan's grain, C1 PASS. The loop does not stay where the map put it: it
tightens, slowly, from 12 to 7 Links at the -y and +x crossings over
five turns with the period falling from 1431 to 1040, so C2 and C3 FAIL
as declared (the map's residual was a slow widening under the pulse and
the lost fires; the lattice's residual is a slow tightening of about one
Link per turn): a finding, not moved. The circles per return read on
the faces, 4.125, 4.094, 3.750, 3.500, the first two within 0.125 of
the whole 4 (C5, reported, not pinned).

## 1. The run

The build: this branch's commit 6b958b9552afff427bb696e36af08972d538ffec (the `centred` parameter on
`by_drive` and `by_line`, the counts table, the world key, the engine's
two calls, the record's key line, `tests/test_centred_step.py`, the world
file); the run was made on that commit's tree, byte for byte, before its
push, while `tools/check.py --base origin/main` ran on it (28 passed on
the docs' scope earlier; the build's scope, the core modules' consumers,
passed before the commit).

    PYTHONPATH=src python tools/run_series.py --jobs 1 --out artifacts/atom_centred examples/events/atoms/hydrogen_r12_centred.json

under Python 3.14.0rc2 (`uv`-installed), headless, no render, no frames:
completed, 7500 ticks, the books balanced at every tick, 77.1 s of the
runner (77.7 wall), 123.5 MB peak (host), 369 683 482 bytes of
`events.jsonl` (the baseline's 70.8 s, 124 MB and 369 MB); the
fingerprints `state.json` sha256
d7444b5ece791de2ac745c3101fdc476ffc28e662d54860780cc3d96ea2e3d7d,
`events.jsonl` sha256
7669fc8754bfe1cdb7c3f30a1d8f8fd79ec32fc61718eb08b20f7c4d8e874966, the
audit 67586909f6d6 (the runner's summary). The record's `hypotheses`:
`bohr-v1`, `centred-step-v1`; `centred_step: true` in `run.json`. The
run's records follow the 24-hour retention policy and are not
committed; the printout is.

## 2. What the clicks read (DETECTOR unless labelled)

| The reading | The number | Kind |
| --- | --- | --- |
| the clicks per detector, family `e` | `face:+x` 762, `face:-x` 726, `face:+y` 756, `face:-y` 735, `face:+z` 0, `face:-z` 0, `at_proton` 0 (read, not measured); 738 releases paired, 56 clicks unpaired at the end; NO escape line of the electron: it is on the board at 7500 (the baseline: 342, 337, 342, 339 and the escape at 3407) | DETECTOR |
| the clicks per detector, family `p` | `face:+x` and `face:-x` 328 045 each, `face:+y` and `face:-y` 325 073 each, `face:+z` and `face:-z` 322 101 each (the baseline's numbers exactly: the proton is fixed and its fan untouched by the key) | DETECTOR |
| the axis crossings, first turn | +y at 402 at (26, 38), 12.00 Links; -x at 721 at (16, 26), 10.00; -y at 992 at (26, 15), 11.00; +x at 1341 at (38, 26), 12.00 (the baseline: 13, 13, 17, 26) | DETECTOR |
| the axis crossings, turns two to five | +y 1742 at 12; -x 2111 at 13; -y 2492 at 11; +x 2772 at 10; +y 3092 at 13; -x 3652 at 16; -y 4072 at 9; +x 4272 at 9; +y 4632 at 14; -x 5071 at 10; -y 5282 at 7; +x 5422 at 7; +y 5692 at 11; -x 6102 at 11; -y 6342 at 7; +x 6462 at 7; +y 6692 at 11; -x 7141 at 10; -y 7352 at 7 (Links from the proton's Node) | DETECTOR |
| the returns to the +x axis and the periods | 5 at 1341, 2772, 4272, 5422, 6462; the periods 1431, 1500, 1150, 1040 (the baseline: one crossing, no period) | DETECTOR |
| the circles per return (C5, reported) | 4.125, 4.094, 3.750, 3.500 from the rows' phase increments unwrapped over each return over N (the pinned circle's 4.001, ALGEBRA.md section 2 (c) reading 1, on the comparison side: the first two returns whole within 0.125) | DETECTOR |
| the proton's reads of the electron's rows | 8 `read` lines (the baseline's 5 over its shorter stay) | DETECTOR |
| the electron's reads of the proton's rows | 1215 (the baseline's 305: four times the bunches, the loop four times longer on the board) | DETECTOR (its own record) |
| the momentum's length at the step lines nearest the crossings | 289, 344, 330, 295, 299, 288, 327, 343, 288, 226, 380, 393, 241, 322, 441, 398, 271, 301, 446, 437, 281, 302, 438 million label units (the start's 294; C4's 200 to 350 left from the fourth turn) | GAMEBOARD (a diagnostic, not counted) |
| the escaped rows of `e` | 2979 units of the electron's rows left through the faces with the momentum (2304, 1344, 0) in label units, the electron's own rows' labels (the baseline's 1360 over its shorter stay) | DETECTOR (`run.json` `escaped`) |

## 3. The verdicts against the pins of CENTRED_STEP.md section 4 (no pin moved)

| Pin | Declared | Read | Verdict |
| --- | --- | --- | --- |
| C1 the loop stays | no escape face click of the electron in 7500 ticks; at least 12 quarter crossings | no escape; 23 crossings | PASS |
| C2 the crossings' radii | every crossing within 9 to 20 Links; the first four within 10 to 15 | the first four 12, 10, 11, 12 (inside); then 12, 13, 11, 10, 13, 16, 9, 9, 14, 10, 7, 7, 11, 11, 7, 7, 11, 10, 7: four crossings at 7 from the fourth turn on, below 9 | FAIL as declared (the loop tightens where the map had it wandering wider) |
| C3 the returns and the period | 3 to 4 returns in 7500; every period 1400 to 2000 | 5 returns; the periods 1431, 1500, 1150, 1040: the last two below 1400 | FAIL as declared (the period falls with the tightening, 1431 to 1040) |
| C4 the momentum's length at the crossings | 200 to 350 million (GAMEBOARD, not counted) | 226 to 446 million: inside for the first three turns, above from the fourth (the tightening's higher momentum) | (not counted) |
| C5 the closure fraction | reported, not pinned | 4.125, 4.094, 3.750, 3.500 | (reported) |
| C6 the control | the same world without the key replays the baseline byte for byte | the build's test (a): the gate world's digests unchanged with the key absent; every registered world parses with the key false | PASS (the build's test) |

1 PASS, 2 FAIL of the three counted pins (DETECTOR); C4 and C5 diagnostics
and reports; C6 the build's.

## 4. What the run adds to the algebra (CAUSE.md, CENTRED_STEP.md section 3)

1. **The cause is confirmed on the lattice.** With the one declaration
   (the body's step at half the wall, nothing else moved) the electron
   that left the board at 3407 stays for 7500 intervals through five
   returns, its first turn at 12, 10, 11, 12 Links against 13, 13, 17, 26
   without the key. The lag of the Node behind the accumulated motion,
   and the push read at the lagging Node, was what widened the loop; the
   fan's grain and the pulse, absent from the map, did not undo it.
2. **The residual is a slow tightening, not the map's slow widening.**
   The map (cases T and U) under the pulse and the lost fires wandered
   between 10 and 19 Links with the loop's constant rising slowly; the
   lattice reads the -y and +x crossings falling from 12 to 7 over five
   turns, the +y and -x crossings staying at 10 to 16, the period from
   1431 to 1040, the momentum's length rising to 440 million: a loop
   drawn inward by about one Link per turn on two of its four
   crossings, eccentric, its near side at the -y and +x crossings. The
   cause of this residual is not read here and not claimed: the map
   has no fan's grain (the crossed fraction 0.87, the comb, PINS.md
   section 2) and the register's `r8` on the same drive fell inward too
   (the radius 3.0 to 27.8, EXPERIMENTS.md); the lost fires' `v x p`
   (CAUSE.md section 2 (iv) 2) alternates in sign by quarter and could
   net either way on an eccentric loop; `drive_b` lifts the lost fires
   and the two keys compose (CENTRED_STEP.md section 6), a run the
   owner decides with form B (record 955).
3. **The closure fraction is readable now.** At the first two returns
   the rows' phase per return reads 4.125 and 4.094 circles, whole
   within 0.125 (the declared circle's 4.001 is the comparison, not a
   pin of this run); at the pair [16, 1] of atom-give-momentum-v1 the
   give would read `g = floor(16 x 0.125) = 2` and `floor(16 x 0.094) =
   1` per row at those returns, and 0.750 and 0.500 later as the loop
   tightens (12 and 8 per row): the momentum give's staircase now has a
   returning loop to act on, and its own pins (DESIGN_MOMENTUM.md
   section 6) would be declared against THIS world's readings, the
   periods and the fractions as read here, if the owner orders it after
   the paper.
4. **What is and is not claimed.** Claimed: the loop stays under the
   key (C1), the byte identity without it (C6), the cause of the
   baseline's escape. Not claimed: a closed circle at r = 12 (C2 and C3
   FAIL), any comparison with nature, the residual's cause. Nothing
   moved.

## Links

[CENTRED_STEP.md](CENTRED_STEP.md) (the pins, section 4); [CAUSE.md](CAUSE.md);
[centred_readings.py](centred_readings.py) and [centred_readings.out](centred_readings.out);
[the baseline run](../atom_baseline/RUN.md) and [its readings](../atom_baseline/baseline_readings.out);
[the world](../../../examples/events/atoms/hydrogen_r12_centred.json) and
[the atoms README](../../../examples/events/atoms/README.md);
[tests/test_centred_step.py](../../../tests/test_centred_step.py);
[the retention policy](../../RETENTION.md); records 953, 955 and 958 of
[the log](../../LOG_2026-09-20.md).
