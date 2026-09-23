# The runs of step 2: R3 read (three PASS, the integers met exactly), R2 not read by its arrangement (the cart's own rows come home, never click; the loop's rows leave through the y and z faces; k = 3 refused by the age bound), R1 and R4 no run (the New Rows Scout, 2026-09-23)

The Boss's GO of 2026-09-23 (about 02:30Z, by Routine: PR #988 merged to
main at `d6f601d0`, the pins of [PINS.md](PINS.md) on main before any
run): the branch `new-rows-runs` off `main` at `d6f601d0`; the four Sagnac
worlds (k = 3, 5, 9, 17) and the three Malus worlds (s = 16, 40, 48)
through the shipped runner exactly as PINS.md declares them, no world file
changed after the pins; R2's ratio per ordinal from the cart's stamped
click lines and R3's cells over the records 1 to 256; the readings by
kind against the pins as printed, PASS or FAIL as written, no pin moved,
the falsifiers checked; R1 and R4 need no run and say so. Nothing here
edits `docs/NATURE.md`.

Notation and kinds as in PINS.md: DETECTOR (a click line, a gather line's
chosen cell, a stamped count), GAMEBOARD (a tick, a `home` line, the
books, the runner's record), COMPUTATION (the pins, the closed forms),
CONVERSION (a ratio or a fraction formed from readings), HOST (the
machine's cost), NATURE (the thing compared with).

## 1. The runs (HOST), the command, the records

```bash
PYTHONPATH=src .venv/bin/python tools/run_series.py --jobs 4 \
    --out artifacts/new_rows docs/designs/new_rows/worlds/*.json
PYTHONPATH=src .venv/bin/python docs/designs/new_rows/new_rows_readings.py artifacts/new_rows
```

The seven worlds as committed at `d6f601d0` (byte-identical to
`a4d2164`'s), the source fingerprint `5166dbe90169655d...` in every
`run.json` (the same as RUN_4AB's and RUN_8BC's runs), the project's
Python 3.14 and numpy 2.5.3. HOST: 17.6 s wall for the seven, four at a
time; per world (the runner's own seconds) `malus_s16` 0.91, `malus_s40`
0.94, `malus_s48` 0.92, `sagnac_k5` 12.4, `sagnac_k9` 12.9, `sagnac_k17`
11.8, `sagnac_k3` 5.4 to its refusal at the tick 841. The runner's table
(`summary.md`): every completed run `conserved` true; the run folders
under `artifacts/` expire by the retention policy, the readings are kept
here in [new_rows_readings.out](new_rows_readings.out) and
[new_rows_readings.json](new_rows_readings.json) with the digests of
every `state.json` and `events.jsonl`, written by
[new_rows_readings.py](new_rows_readings.py) against
[new_rows_pins.json](new_rows_pins.json), untouched.

## 2. R1, the no-signalling marginals: no run

The reading is registered (series L's `pair.marginal` = 32 of 64 at every
setting, DETECTOR, replayed at head by the tests); nothing to run, nothing
changes. The row stands in PINS.md section 5 as the PROPOSAL 1d with the
reviewer's status (a theorem of the click's form, a consistency check
outside the count).

## 3. R3, Malus at three new settings: three PASS, the integers met exactly

The reading (DETECTOR): the cells 0+ and 0- over the records 1 to 256,
read from the gather lines (the click's record of the one cell the ladder
chose per record: `chosen` names the read's label at `first` and the
channel at `second`; one gather per record, 289 in all over the 300
intervals as in the registered 22.5-degree run, the records 1 to 256
read as row 9 reads them); the falsifiers from the same lines; the books
from the runner's record.

| World | s, angle | the cells 0+, 0- read (DETECTOR) | the pin (COMPUTATION) | the pass fraction (CONVERSION) | cos^2 (NATURE) | the departure | a cell on label 1 | the wheel's coverage | the books | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `malus_s16` | 16, 11.250 degrees | 246, 10 | 246, 10 | 246 / 256 = 0.96094 | 0.96194 | -0.00100 (the pin's -0.00100) | none | 256 of 256 residues | balanced at every tick | PASS |
| `malus_s40` | 40, 28.125 degrees | 199, 57 | 199, 57 | 199 / 256 = 0.77734 | 0.77779 | -0.00044 (the pin's -0.00044) | none | 256 of 256 | balanced | PASS |
| `malus_s48` | 48, 33.750 degrees | 177, 79 | 177, 79 | 177 / 256 = 0.69141 | 0.69134 | +0.00006 (the pin's +0.00006) | none | 256 of 256 | balanced | PASS |

Every integer met exactly; every falsifier of PINS.md section 3 checked
and none tripped (no cell on label 1: the read at x = 4 kept the label;
the wheel [159, 256] covered every residue once over the records 1 to
256; 256 of 256 records gathered; the books balanced at every tick). The
departures from cos^2 are the tables' rounding at the scale 256 as
pinned, each below 1 / 256. For the register (the status of record
1166): agrees, with the number, beside row 9: 246, 199 and 177 of 256
against cos^2 times 256 = 246.26, 199.11 and 176.98 at 11.25, 28.125 and
33.75 degrees, the tolerance the tables' grain 1 / 256; a re-reading of
row 9's identity, outside the referee's count of independent
predictions, as PINS.md says.

## 4. R2, the Sagnac ratio: NOT READ by the arrangement; no number; the pin stands unread

The four worlds ran exactly as declared (no world file changed). The
result, by kind, from [new_rows_readings.out](new_rows_readings.out):

| World | the record (GAMEBOARD) | the cart's own click lines, stamped (DETECTOR) | `home` lines of the cart's rows (GAMEBOARD) | the cart's rows' face clicks (DETECTOR) | the ratio (CONVERSION) |
| --- | --- | --- | --- | --- | --- |
| `sagnac_k3` | FAILED at the tick 841: "a ray carries the age 841 beyond the world's age_bound 840"; the books balanced to there | 0 | 572 | 10 (the ages 195 to 269) | NOT READ |
| `sagnac_k5` | completed, 1500 intervals, the books balanced at every tick | 0 | 691 | 1714 of the 2998 rows born (±y 56 each, ±z 801 each; the ages 11 to 614 at the escape) | NOT READ |
| `sagnac_k9` | completed, balanced | 0 | 365 | 2139 (±y 116 each, ±z 953 and 954; the ages 11 to 346) | NOT READ |
| `sagnac_k17` | completed, balanced | 0 | 119 | 2412 (±y 107 each, ±z 1099 each; the ages 162 to 250) | NOT READ |

**What the record says, three findings, each read from the lines and not
from the pin.**

1. **A row of the cart's own number that returns to the cart is `home`,
   not a click.** The chain of PINS.md section 2, step 5, assumed the
   cart's `measure` on its own family reads its own returning pulses. The
   engine's rule (ENGINE.md :370-374; `nature_beam.py` :5215-5250): "what
   comes home (the own number's arrivals) is taken whole and created again
   at the next self-creation on the declared directions"; a detector reads
   the arrivals of every number but its own. So no stamped return exists:
   the `home` line carries no `clock` and no `record` (GAMEBOARD), and the
   cart's own click lines are 0 in every world. The ratio cannot be
   formed. This is PINS.md's falsifier "the cart's `measure` not reading
   its own family" tripped at its root, the number rule, before any Port
   question; the reviewer's item (i) on the gate named the Ports, not the
   number.
2. **The loop does not keep the pulses: the cart's rows leave through the
   y and z faces.** The escaping rows are the cart's own records (their
   `record` set, the family `cart`, the content 1), with the momentum
   labels ±64 on y or z, one Link off the axis at the escape ((y, z) =
   (0, 1), (2, 1), (1, 0), (1, 2)), at every age from 11 to 614 intervals
   and at no one displacement from the birth Node (128 distinct values of
   240 at k = 5): not the loop's antipode. The rule, named by the physics-rule
   reviewer on this record (2026-09-23): THE COLLISION, item 3 of the
   interval (`nature_beam.py` :35-40; `_collide` :3464, applied at :3436
   every interval; `collision_table` :1293; `class_key` :1279): at every
   Node of free space, per (number, content) class, the single units in
   the eight slots are permuted by the cyclic shift inside their class,
   and two single rows of one class with opposite headings sum to zero,
   so the class (+x, -x) is turned onto (+y, -y) or (+z, -z); the cart's
   +x pulse of one ordinal meets its -x pulse of another at a free Node at
   almost every interval, which is why the escapes carry [0, ±64, 0] and
   [0, 0, ±64], leave one Link off the axis, at every age and 128
   displacements, and why the turned share falls as k rises. Not the
   `home` re-creation (re-created on ±x only) and not a meeting of one
   record's rows (ALGEBRA.md 4.7 is the injectivity theorem, no turning
   rule). What it means for R2: two
   rows of one record on one loop, born at one Node in opposite
   directions, is not an arrangement the law as built carries around the
   loop.
3. **k = 3 is refused by the default age bound.** `age_bound` defaults to
   twice the flight bound of the GameBoard (`world.py` :1772-1789, 840
   here); the co-moving return at k = 3 needs 966 intervals (PINS.md's
   t_+ = 39600 / 41), so the engine refused the world at the tick 841
   ("declare a larger age_bound or a smaller GameBoard"). The key exists;
   declaring it is a change of the world file, which the GO forbade
   without a report: reported here, not done.

**The verdict.** R2: NOT READ, by the arrangement and not by the law; no
number; the pin 55 / (32 k) stands as written and unread; nothing moved.
It is not a FAIL of the law against nature (no click was read that
disagrees with the pin) and not a PASS; the row does not enter the
register from these runs. The Boss's rule for a world that must change
applies: stop and report before running.

**The arrangement that would read it, as first proposed (superseded by the
reviewer's ruling: two records of the cart's number are ONE class, so the
two pulses need two numbers; the arrangement that stands is
[PINS_R2.md](PINS_R2.md), one world of two bodies, its pins written and
its worlds validated at load, not run).** Every part
under existing keys: (a) `age_bound` declared 1500 (the run's length);
(b) the returns through transponders, as RUN_4AB reads the round trip: a
post P_b one Node behind the cart and a post P_a one Node ahead, bodies of
the cart's momentum and content (hopping in step: the same accumulators),
each with `rerelease` on the cart's rows; the cart's +x pulse wraps and
meets P_b first, its -x pulse meets P_a first, each is re-emitted toward
the cart stamped with the post's number and clicked by the cart's
`measure` (the mechanism RUN_4AB 1.2 steps 9 to 11 read); each end then
adds the same constant (one count of the post and one dwell), so the
closed form gains a correction of order 3 / (t_+ + t_-), to be pinned
exactly before any run; (c) if the reviewer names the meeting of one
record's two rows as what turns them, the two pulses must be two records:
the cart's lamp on +x alone and a co-moving lamp body E on -x alone at
the same ordinals (both holding K exactly, so both stall at the same
self-creations), the pairing by ordinal; if he names the `home`
re-creation, (b) alone suffices since no cart row then comes home. HOST
seconds per world. The pins are recomputed by the closed forms and
written before any run, as the rule requires.

## 5. R4, the round-trip Doppler: no run

The reading is registered (RUN_4AB 6.3, DETECTOR: 3.708 for 151 / 41 and
2.054 for 43 / 21); nothing to run, nothing changes. The row stands in
PINS.md section 5 as the PROPOSAL 4c with the reviewer's status (a form
row outside the count until a nature source with a number is named).

## 6. The tally of step 2, and what did not move

- R3: three PASS, the integers 246, 199, 177 of 256 met exactly (DETECTOR);
  the status for the register agrees, beside row 9, a re-reading.
- R2: NOT READ by the arrangement (three findings above, each from the
  record); no number; the pin unread; the world that would read it is a
  proposal for the Boss's word.
- R1 and R4: no run; the registered readings stand.
- No pin moved; no world file changed; no engine line; NATURE.md
  untouched.

## 7. Links

- [PINS.md](PINS.md) (the pins, the chains, the falsifiers; sections 2
  and 3 for R2 and R3); [new_rows_pins.out](new_rows_pins.out);
  [new_rows_readings.out](new_rows_readings.out) and
  [new_rows_readings.json](new_rows_readings.json);
  [new_rows_readings.py](new_rows_readings.py); [worlds/](worlds/).
- [RUN_4AB.md](../fail_rows/RUN_4AB.md) 1.2 and 6.3 (the transponder's
  returns and the meeting remainder); [ENGINE.md](../../ENGINE.md), the
  self-creation and what comes home; [ALGEBRA.md](../../ALGEBRA.md) 4.7
  (the interval's merge) and 5.1 (the r-free lines).
