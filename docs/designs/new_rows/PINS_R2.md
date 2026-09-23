# R2, the Sagnac ratio, in one world of two numbers: the cart's +x pulse and a co-moving body's -x pulse, the pins before any run (the New Rows Scout, 2026-09-23; docs only, no run)

The Boss's GO of 2026-09-23 (about 03:09Z, by Routine) on the physics-rule
reviewer's ruling over [RUNS.md](RUNS.md) section 4 (PR #996 merged to
main at `688a93d`, the Boss's record 1210): the rule that turned the
first arrangement's rows off the loop is THE COLLISION, item 3 of the
interval (`nature_beam.py` :35-40 the header's item 3; `_collide` :3464,
applied at :3436 every interval; `collision_table` :1293; `class_key`
:1279): at every Node of free space, per (number, content) class, the
single units in the eight slots are permuted by the cyclic shift inside
their class, the class being the crowd mask, the number of singles and
the vector sum of their headings; two single rows of one class with
opposite headings sum to zero, so (+x, -x), (+y, -y) and (+z, -z) are one
orbit and the shift carries a head-on pair off the x axis onto ±y or ±z.
Two pulses of one number and one content that meet at a free Node are
scattered off their line; two pulses of different numbers pass through
each other; a single stream never meets itself. Hence the reviewer's
arrangement, taken here as he gave it: the two pulses of one birth need
TWO NUMBERS, one body each, and no second post.

This file: the chain click to click by kind with its code lines, the
closed forms per end, the pins as exact fractions, the band, the
falsifiers, the four worlds validated at load and NEVER run, the HOST
cost. Written by [new_rows_r2_worlds.py](new_rows_r2_worlds.py) into
[worlds/](worlds/) (`sagnac2_k3`, `k5`, `k9`, `k17`), the pins in
[new_rows_r2_pins.out](new_rows_r2_pins.out) and
[new_rows_r2_pins.json](new_rows_r2_pins.json). The reviewer gates these
pins before any run. Notation and kinds as in [PINS.md](PINS.md).

## 1. The arrangement, under existing keys

The cart of RUN_4AB (series O's numbers: N = 64, K = 4 202 496, S = 2^20,
the held mass 4 194 304 and the amount 8192, the momentum p = Q S M / (k -
1) on +x, k = 3, 5, 9, 17) on the bar 240 x 3 x 3 with the x axis periodic
(`boundary: {"x": "periodic"}`), `age_bound` 1500 declared (the run's
length; the default 840 refused k = 3, RUNS.md finding 3), `clock_stamp`
true, `suspension` 0, 1500 intervals. Two bodies of the family `cart`:

- **The cart D at x = 20**: its lamp on +x alone (`lamp.directions`
  `[[1, 0, 0]]`, the rate [1, 1], the wheel [1, 64]); its `directions` +x
  (the mass release); its table `cart: measure` (`reads: age`), `mass:
  pass`. It clicks every cart row of another number: E's -x pulse
  directly, and its own +x pulse when it comes back re-stamped with E's
  number.
- **The body E at x = 19**, one Node behind, of the cart's family,
  momentum and content (the same accumulators: it hops in step with the
  cart; its own lamp costs its amount 1 per birth as the cart's does, so
  the two M fall alike): its lamp on -x alone; its `directions` +x; its
  table `cart: rerelease`, `mass: pass`. It re-emits the cart's +x pulse
  on its declared direction +x, one Link to the cart, stamped with its own
  number (the transponding rule RUN_4AB 1.2 steps 9 to 11 read).

The held mass is kept as registered (the cart's M = 4 194 304 + 8192
under the drive's wall, as in every cart world), the choice the Boss left
to the scout: the mass rows (content 0, amount 64 per row, released on +x
by each body) are a crowd slot and never a single, so they enter no
collision class of content 1 and collide with nothing that is read; both
bodies' tables pass them.

Why two numbers suffice and nothing meets: the cart's +x stream (number
D, content 1) and E's -x stream (number E, content 1) are two classes, so
they pass through each other at every free Node; each stream is single in
its direction, so it never meets itself; E's re-emissions (number E,
content 1, +x) travel one Link between the two bodies' Nodes and meet
nothing (E's own -x rows leave E the other way; the cart consumes the
re-emission at its Node, a measured event, where no collision acts).
Neither body ever meets a row of its own number: E's -x pulse arrives from
the +x side and meets the cart first; the cart's +x pulse arrives from the
-x side and meets E first. No `home` line of the cart's family can occur;
that is a falsifier below.

## 2. The chain click to click, by kind

1. Declaration (the arrangement, not the number): section 1.
2. GAMEBOARD: at the cart's self-creation of count n_0(j) the cart births
   the record j with one row on +x, and E, at the same tick, its record j
   with one row on -x (`nature_beam.py` :6066, the `birth` lines, each
   stamped with its body's own count; both lamps hold K exactly, so both
   skip the same self-creation when the count's remainder does, RUN_8BC
   5: the pairing is by ordinal and reads nothing of it).
3. COMPUTATION, the law's pace: both bodies step one Link per k intervals
   on +x (`engine.py` :759, the per-axis drive p / (Q S M + p) = 1 / k), v
   = 1 / k; the rows fly at the heading's pace c = 32 / 55 (`direction_flight`,
   `nature_beam.py` :909; ALGEBRA.md 4.2); beta = 55 / (32 k).
4. GAMEBOARD: E's -x row goes round the loop (the wrap, `nature_beam.py`
   :1411 and :1426) and closes on the cart from the +x side at c + v after
   L - 1 Links; the cart's +x row goes round and closes on E from the -x
   side at c - v after L - 1 Links.
5. DETECTOR: the cart's `measure` clicks E's row (another number) at its
   arrival, the click line stamped with the cart's count n_-(j) and
   carrying E's record j (`nature_beam.py` :5536 the click line, :5179 the
   stamp).
6. GAMEBOARD, then DETECTOR: E's `rerelease` takes the cart's row into
   its pending rows (`nature_beam.py` :2488) and re-emits it at its next
   self-creation on +x with its own number, the record kept (:5812-5815);
   the row closes the one Link on the receding cart at c - v; the cart's
   `measure` clicks it, the line stamped n_+(j) and carrying the cart's
   record j (the record's owner D, `record >> 32`, tells it from E's own
   row of step 5, both with `number` E).
7. CONVERSION: per ordinal j, (n_+ - n_-) / (n_+ + n_- - 2 n_0), n_0 the
   cart's birth line's clock; the mean over the window from the cart's
   count 60. Every term is a count of the cart's one clock (its own age,
   one per interval; `suspension` 0, no count owed, `count_owed` at a
   zero numerator, `engine.py` :157), so the ratio is r-free at r = 1 by
   declaration.
8. COMPUTATION, the closed forms per end (ALGEBRA.md 4.1, the
   accumulators' carries, exact in the mean): t_- = (L - 1) / (c + v); t_+
   = (L - 1) / (c - v) + 1 + 1 / (c - v) = L / (c - v) + 1 (E's next
   self-creation the one count added, then the last Link); the ratio's
   pin (t_+ - t_-) / (t_+ + t_-) = beta plus the one asymmetric constant
   of E's dwell.

The law as built makes it: yes; no key of a hypothesis.

## 3. The pins, before any run (COMPUTATION; c = 32 / 55 from the engine's flight table on the loaded worlds; L = 240)

| World | k | beta = 55 / (32 k) | t_- = (L - 1) / (c + v) (GAMEBOARD, intervals) | t_+ = L / (c - v) + 1 | ordinals with both returns inside 1500 | the ratio's pin, exact (DETECTOR the stamps, CONVERSION the ratio) | the pin less beta | the band on the ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `sagnac2_k3` | 3 | 55/96 = 0.57292 | 39435/151 = 261.16 | 39641/41 = 966.85 | 533 | 2184478/3801313 = 0.57466 | +0.00175 | 0.0123 (the remainders 4.72 and 10.44 counts) |
| `sagnac2_k5` | 5 | 11/32 = 0.34375 | 13145/43 = 305.70 | 4407/7 = 629.57 | 870 | 48743/140758 = 0.34629 | +0.00254 | 0.0226 (6.72 and 14.44) |
| `sagnac2_k9` | 9 | 55/288 = 0.19097 | 118305/343 = 344.91 | 119033/233 = 510.87 | 989 | 6631627/34196692 = 0.19393 | +0.00295 | 0.0387 (10.72 and 22.44) |
| `sagnac2_k17` | 17 | 55/544 = 0.10110 | 223465/599 = 373.06 | 74963/163 = 459.90 | 1040 | 4239021/40663816 = 0.10425 | +0.00314 | 0.0686 (18.72 and 38.44) |

The band: the lattice's meeting remainder of RUN_4AB 6.3 per end, in the
cart's counts: at the direct click one hop (k intervals) plus one dwell
(55 / 32); at the re-emitted return twice that plus E's one count (the
meeting with E, E's next self-creation, the last Link's landing); the two
over the sum of the two returns. It is the per-ordinal band; the mean
over the window's hundreds of ordinals scatters far less, and a run
reports both the mean and its scatter. The pin is the exact fraction; the
comparison with nature (Michelson-Gale 1925, PINS.md section 2) is on the
form v / c, the constant of E's dwell being the arrangement's own,
stated here before the run and never subtracted after it.

## 4. The falsifiers, checked by the reader before any verdict

- E's step lines are the cart's shifted by one Node: at every tick of a
  cart `step` line E writes a `step` line from x - 1 to x (GAMEBOARD; the
  two bodies' accumulators identical); a step of one without the other
  refutes the co-motion and stops the reading.
- No face click of either number's rows (DETECTOR): the two streams pass
  through each other; a face click carrying a cart-family row is a
  collision the classes should not allow.
- No `home` line of the cart's family at either body (GAMEBOARD): neither
  body ever meets a row of its own number.
- Every return stamped: per ordinal j in the window, exactly two click
  lines at the cart with `clock`, one of E's record j (n_-) and one of the
  cart's record j (n_+, via E); a missing return, or one without a stamp,
  stops the ratio for that ordinal and is counted.
- The spacing: n_- - n_0 within the remainder of t_-, n_+ - n_0 within the
  remainder of t_+ (COMPUTATION against the closed forms).
- The books balanced at every tick (GAMEBOARD).
- The verdict: the mean ratio within the band of its pin PASS, outside it
  FAIL as written; no pin moved after the run.

## 5. The worlds, validated at load and never run; HOST

`worlds/sagnac2_k3.json`, `sagnac2_k5.json`, `sagnac2_k9.json`,
`sagnac2_k17.json`, written by `new_rows_r2_worlds.py` and each loaded by
the shipped loader (`load_world`; the model ids
`beam-new-rows-sagnac2-k<k>-v1`; `age_bound` 1500 read back from the
parsed world). HOST: about 12 s per world on the runner's timings of the
first arrangement (1500 intervals, two bodies, two streams), under a
minute for the four; the reader seconds. The run is the Boss's GO after
the reviewer's gate on these pins.

## 6. What a FAIL would and would not show

The chain, not the number: a mean ratio off its pin beyond the band would
show a rule the chain forgot at the wrap (step 4), at E's re-emission
(step 6: the record not kept, or the next self-creation not one count) or
in the pairing by ordinal (step 2: the two lamps not skipping the same
self-creation); a face click or a `home` line would show a class the
arrangement did not foresee; never a rate r, which cancels in step 7
under every value. It would not touch rows 4a, 4b or 5b (the same family
and not the same observable, r-free by construction, PINS.md section 2),
nor R3, R1 or R4. A PASS says the two counter-propagating arrivals at one
moving detector on a closed loop differ as v / c to the lattice's
remainder, the form Michelson and Gale read; it says nothing of the
second order in v.

## 7. The three tests, on the arrangement

Nothing enters the law: no identity, no key, no verb. Generic: no family
name read by any step (the tables select by family as every world's do).
Vector: the translation of the accumulators (the flight, the drive, the
lamps' counts), the re-release a permutation of pending rows, the click's
comparison; no root, no float. Local: each click reads its own Node's
arrivals; E's re-emission its own pending rows; nothing kept at a Node.

## 8. Links

- [RUNS.md](RUNS.md) section 4 (the first arrangement's three findings
  and the reviewer's rule); [PINS.md](PINS.md) section 2 (the row, nature's
  number, the claim it stands beside); [new_rows_r2_worlds.py](new_rows_r2_worlds.py),
  [new_rows_r2_pins.out](new_rows_r2_pins.out), [new_rows_r2_pins.json](new_rows_r2_pins.json),
  [worlds/](worlds/).
- [RUN_4AB.md](../fail_rows/RUN_4AB.md) 1.2 and 6.3 (the transponder's
  return, the meeting remainder); [ALGEBRA.md](../../ALGEBRA.md) 4.1, 4.2 and
  [5.1](../../ALGEBRA.md#51-the-click-theorem-lorentzs-factors-from-the-clicks);
  [ENGINE.md](../../ENGINE.md), what comes home.
