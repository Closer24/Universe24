# R2, the Sagnac ratio, in one world of two numbers: the cart's +x pulse and a co-moving body's -x pulse, each clicked directly at the other body; the pins before any run (the New Rows Scout, 2026-09-23; docs only, no run)

The Boss's GO of 2026-09-23 (about 03:09Z, by Routine) on the physics-rule
reviewer's ruling over [RUNS.md](RUNS.md) section 4 (PR #996 merged to
main at `688a93d`, the Boss's record 1210), and the reviewer's gate on
this file's first version (PR #1001 at `45c9ca43`, 04:10Z and 04:18Z: NOT
AGREED as written, two must-fix lines, folded here). The rule that turned
the first arrangement's rows off the loop is THE COLLISION, item 3 of the
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
each other; a single stream never meets itself. Hence two numbers, one
body each, and no post.

This file: the chain click to click by kind with its code lines, the
closed forms per end, the pins as exact fractions, the band, the
falsifiers, the four worlds validated at load and NEVER run, the HOST
cost. Written by new_rows_r2_worlds.py (`docs/designs/new_rows/new_rows_r2_worlds.py`, deleted 2026-09-26) into
[worlds/](worlds/) (`sagnac2_k3`, `k5`, `k9`, `k17`), the pins in
[new_rows_r2_pins.out](new_rows_r2_pins.out) and
[new_rows_r2_pins.json](new_rows_r2_pins.json). Notation and kinds as in
[PINS.md](PINS.md). The run waits for the Boss's GO after the birth stamp
merges (section 4).

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
  pass`. It clicks E's -x pulse directly on its arrival from the +x side,
  the line stamped with its own count and carrying E's record.
- **The body E at x = 19**, one Node behind, of the cart's family,
  momentum and content (the same accumulators: it hops in step with the
  cart): its lamp on -x alone; its `directions` +x; its table `cart:
  measure` (`reads: age`), `mass: pass`. It clicks the cart's +x pulse
  directly on its arrival from the -x side, the line stamped with its own
  count and carrying the cart's record.

Why both bodies must measure (the reviewer's must-fix (i)): a `measure`
click deposits the clicked rows' content into the detector body
(`nature_beam.py` :5496-5500, `entry.held[family] += group_content -
waiting_content`), a `read` and a `rerelease` deposit nothing (:5359,
:5413), the body's content M is the sum of its held (`measured.py` :706)
and the drive's divisor is Q S M + |p| (`step_axis`, `engine.py`
:122-154); so with a re-emitting E the cart would gain one unit per
return and E none, both losing one per birth, the two step ticks would
diverge (E at 1449 where the cart steps at 1450 at k = 9; 1411 against
1412 at k = 17; a drift of 0.2 to 0.3 interval by the end at k = 3 and
5), E's step onto the cart's Node would be refused as a contact and the
co-motion falsifier would trip. With both measuring, the deposits are
symmetric, one per return at each body, the difference of the two
contents bounded by t_+ - t_- and not growing: no divergent step inside
1500 intervals at any k.

The held mass is kept as registered (the cart's M = 4 194 304 + 8192
under the drive's wall, as in every cart world): the mass rows (content
0, amount 64 per row, released on +x by each body) are a crowd slot and
never a single, so they enter no collision class of content 1 and
collide with nothing that is read; both bodies' tables pass them.

Why nothing meets: the cart's +x stream (number D, content 1) and E's -x
stream (number E, content 1) are two classes, so they pass through each
other at every free Node; each stream is single in its direction, so it
never meets itself; nothing is re-emitted. Neither body ever meets a row
of its own number: E's -x pulse arrives from the +x side and meets the
cart first; the cart's +x pulse arrives from the -x side and meets E
first. No `home` line of the cart's family can occur; that is a falsifier
below.

## 2. The chain click to click, by kind

1. Declaration (the arrangement, not the number): section 1.
2. GAMEBOARD: at the tick t_j the cart births the record j with one row
   on +x, and E its record j with one row on -x (`nature_beam.py` :6066,
   the `birth` lines; both lamps hold K exactly, so both skip the same
   self-creation when the count's remainder does, RUN_8BC 5: the pairing
   is by ordinal). The birth line carries no clock on `main` today
   (:6064-6078: the stamp is on the click, become, rerelease, read and
   pass lines only); n_0(j) is read from the birth stamp once the branch
   `birth-stamp` (the Birth Stamp Implementer, Reviewer 3's MUST 1 for the
   light clock) lands, the one-line engine change the Boss chose to wait
   for; the run waits for its merge SHA.
3. COMPUTATION, the law's pace: both bodies step one Link per k intervals
   on +x (`step_axis`, `engine.py` :122-154, the per-axis drive p / (Q S
   M + p) = 1 / k), v = 1 / k; the rows fly at the heading's pace c = 32 /
   55 (`direction_flight`, `nature_beam.py` :909; ALGEBRA.md 4.2); beta =
   v / c = 55 / (32 k).
4. GAMEBOARD: E's -x row goes round the loop (the row's wrap on the
   periodic axis, `_walk_rows` :1402-1427, `after %= extents[axis]`; a
   body's :3597-3598) and closes on the cart from the +x side at c + v
   after L - 1 Links; the cart's +x row goes round and closes on E from
   the -x side at c - v after L - 1 Links.
5. DETECTOR: the cart's `measure` clicks E's row (another number) at its
   arrival, the click line stamped with the cart's count n_-(j) and
   carrying E's record j (`nature_beam.py` :5533 the click line, :5179 the
   stamp).
6. DETECTOR: E's `measure` clicks the cart's row (another number) at its
   arrival, the click line stamped with E's count n_+(j) and carrying the
   cart's record j (the same lines). Each body clicks the other's rows
   only, so no owner bit is needed to tell the returns apart.
7. CONVERSION: per ordinal j, (n_+ - n_-) / (n_+ + n_- - 2 n_0), n_+ from
   E's clock, n_- from the cart's, n_0 the common birth count; the mean
   over the window from the count 60. The two clocks are one by
   construction (both counts the age, one per interval; `suspension` 0,
   no count owed, `count_owed` at a zero numerator, `engine.py` :157), so
   the ratio is r-free at r = 1 by declaration; the equality of the two
   clocks is checked on the stamps (section 4).
8. COMPUTATION, the closed forms per end (ALGEBRA.md 4.1, the
   accumulators' carries, exact in the mean; the tables and the releases
   run in one interval, `nature_beam.py` :3450-3455, so no dwell is
   added at either end): t_- = (L - 1) / (c + v); t_+ = (L - 1) / (c - v);
   the ratio (t_+ - t_-) / (t_+ + t_-) = v / c = beta EXACTLY, no
   arrangement constant.

The law as built makes it: yes; no key of a hypothesis.

## 3. The pins, before any run (COMPUTATION; c = 32 / 55 from the engine's flight table on the loaded worlds; L = 240)

| World | k | t_- = (L - 1) / (c + v) (GAMEBOARD, intervals) | t_+ = (L - 1) / (c - v) | ordinals with both returns inside 1500 | the ratio's pin = beta = 55 / (32 k), exact (DETECTOR the stamps, CONVERSION the ratio) | the band on the ratio (the remainders per end) | the band over beta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sagnac2_k3` | 3 | 39435/151 = 261.16 | 39435/41 = 961.83 | 538 | 55/96 = 0.57292 | 0.0077 (4.72 and 4.72 counts) | 0.013 |
| `sagnac2_k5` | 5 | 13145/43 = 305.70 | 13145/21 = 625.95 | 874 | 11/32 = 0.34375 | 0.0144 (6.72 and 6.72) | 0.042 |
| `sagnac2_k9` | 9 | 118305/343 = 344.91 | 118305/233 = 507.75 | 992 | 55/288 = 0.19097 | 0.0251 (10.72 and 10.72) | 0.132 |
| `sagnac2_k17` | 17 | 223465/599 = 373.06 | 223465/489 = 456.98 | 1043 | 55/544 = 0.10110 | 0.0451 (18.72 and 18.72) | 0.446 |

The band: the lattice's meeting remainder of RUN_4AB 6.3 per end, one hop
(k intervals) plus one dwell (55 / 32), in the clicking body's counts, at
each direct click; the two over the sum of the two returns. It is the
per-ordinal band; the mean over the window's hundreds of ordinals
scatters far less, and a run reports both the mean and its scatter.

**Nature's number, with its uncertainty** (NATURE; also in PINS.md
section 2): Michelson, Gale and Pearson 1925, ApJ 61, 140, read 0.230 +-
0.005 fringe against the computed 0.236 for the Earth's rotation, the
coefficient of v / c 0.975 +- 0.021 (to verify against the source); Sagnac
1913, C. R. Acad. Sci. 157, 708 and 1410 (to verify). **The law's
number**: the mean ratio over beta, pinned 1 exactly, the tolerance the
band over beta (0.013 at k = 3, the tightest rung). So R2 enters the
register as agrees or disagrees on the coefficient, not as a form row.

## 4. The falsifiers, checked by the reader before any verdict

- The two bodies' clocks equal at equal ticks: E's `clock` on its click
  lines equals the cart's `clock` on its click lines at equal ticks
  (DETECTOR, the stamps alone); beside it E's `step` lines the cart's
  shifted by one Node at the same ticks (GAMEBOARD; the two bodies'
  accumulators identical). Either apart refutes the co-motion and stops
  the reading.
- No face click of either number's rows (DETECTOR): the two streams pass
  through each other; a face click carrying a cart-family row is a
  collision the classes should not allow.
- No `home` line of the cart's family at either body (GAMEBOARD): neither
  body ever meets a row of its own number.
- Every return stamped: per ordinal j in the window, one click line at
  the cart of E's record j (n_-) and one click line at E of the cart's
  record j (n_+), each with `clock`; n_0(j) from the birth stamp (once
  `birth-stamp` lands; the falsifier off the stamps alone); a missing
  return, or one without a stamp, stops the ratio for that ordinal and
  is counted.
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
parsed world; both bodies' tables `measure`). HOST: about 12 s per world
on the runner's timings of the first arrangement (1500 intervals, two
bodies, two streams), under a minute for the four; the reader seconds.
The run is the Boss's GO after `birth-stamp` merges, with its merge SHA.

## 6. What a FAIL would and would not show

The chain, not the number: a mean ratio off its pin beyond the band would
show a rule the chain forgot at the wrap (step 4) or in the pairing by
ordinal (step 2: the two lamps not skipping the same self-creation); a
face click or a `home` line would show a class the arrangement did not
foresee; the two clocks apart would show the deposits not symmetric
(section 1); never a rate r, which cancels in step 7 under every value.
It would not touch rows 4a, 4b or 5b (the same family and not the same
observable, r-free by construction, PINS.md section 2), nor R3, R1 or R4.
A PASS says the two counter-propagating arrivals of one birth at the two
co-moving bodies differ as v / c to the lattice's remainder, the form and
the coefficient Michelson and Gale read; it says nothing of the second
order in v.

## 7. The three tests, on the arrangement

Nothing enters the law: no identity, no key, no verb. Generic: no family
name read by any step (the tables select by family as every world's do).
Vector: the translation of the accumulators (the flight, the drive, the
lamps' counts), the click's comparison; no root, no float. Local: each
click reads its own Node's arrivals; nothing kept at a Node.

## 8. Links

- [RUNS.md](RUNS.md) section 4 (the first arrangement's three findings
  and the reviewer's rule); [PINS.md](PINS.md) section 2 (the row, nature's
  number, the claim it stands beside); new_rows_r2_worlds.py (`docs/designs/new_rows/new_rows_r2_worlds.py`, deleted 2026-09-26),
  [new_rows_r2_pins.out](new_rows_r2_pins.out), [new_rows_r2_pins.json](new_rows_r2_pins.json),
  [worlds/](worlds/).
- [RUN_4AB.md](../fail_rows/RUN_4AB.md) 6.3 (the meeting remainder);
  [ALGEBRA.md](../../ALGEBRA.md) 4.1, 4.2 and
  [5.1](../../ALGEBRA.md);
  [ENGINE.md](../../ENGINE.md), what comes home.
