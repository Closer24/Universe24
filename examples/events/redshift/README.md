# The redshift series E under the Beam Law, in space, under the age reading

Two worlds of one base, written by `make_worlds.py`; the register entry is
[E, the clock's redshift in space under the age reading (2026-09-20)](../../../docs/EXPERIMENTS.md#e-the-clocks-redshift-in-space-under-the-age-reading-2026-09-20)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
question: with the ray's age kept whole on the record and read by the
measured event as the age moment of the one reading (the model owner,
2026-09-19, "the clock beside a mass must read M / r, not M / r^2, and the
reading is in the detector"; [BEAM_LAW section 10](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
note 24), does a clock beside a mass in space slow as M / r under
`reads: "age"` while the presence, what the push reads, falls as M / r^2,
Einstein's pair from two readings of the same rays? A research run, made
once, never a test; the derivation and the expectations below were written
before the runs; a reading outside its expectation is reported with its
numbers, never moved.

**The kinds of the readings (the model owner, 2026-09-22, records 562, 564
and 569).** Two kinds. Each probe's own owed count (age, waited, owed in
the run's `run.json`) is a DETECTOR reading at its Node within its limits
(record 569: an emitter behaves like a detector at its own Node). The
shell means k_s and k_a, the fractions counting and the rate ratios of the
age clocks are read by the tool from the world replayed through the API
(the probes' (age, waited) at the window's two ends): GAMEBOARD readings,
the host's view of the state, a diagnostic and never a measurement (record
281; record 562: nobody measures the board), and every pinned reading of
this series rests on them (the audit of record 567: a shell mean from a
replay is the board; from the probes' own records it would be a detector's,
to be verified by the Replicator's re-read). The detector reading of a
clock's rate at two distances is a lamp's births read by a detector, as
series T reads them (NATURE row 12); the detector reading of Poisson's
equation (record 564) is not made in this series.

## The base

An open cube of 31^3 Nodes, the centre c = (15, 15, 15), `"law": "beam"`,
K 2^22, N 64, one free family `m` of charge 0 without a phase circle
(`"phase": false`). The source is a fixed measured event of content
M = 2^12 at c releasing on the full fan of primitive directions (a, b, c)
with 0 < |a| + |b| + |c| <= 6: 290 directions (284 declared beyond the six
headings), every direction of the GameBoard within that bound. At `release`
[1, M] its clock gives `by_clock(age, M, M)` = 1 ray per direction per
self-creation: q = 290 units per interval, one shell of the fan every
interval, exact. The probes are fixed measured events of content 1 at every
Node of the shells of radius r = 4, 6, 8, 10, 12, 14 (the Nodes at
Euclidean distance within a half Link of r: 210, 450, 762, 1250, 1814 and
2498 Nodes, 6984 probes) whose table entry for `m` is `pass` (no push, no
record; the clock's count is read all the same, over every ray of another
number at the Node, rest and moving alike). In the `scalar` world the
probes count the presence at `suspension` [1, 1] (the default reading, as
series C read it); in the `age` world their entry reads `age`
(`{"rule": "pass", "reads": "age"}`) so their clocks count the age moment,
`sum amount x age` over the rays at the Node, at `suspension` [1, 2] (a
few units at r = 12). The probes' own release, one ray per heading at the
age M = 4096, never comes within the 300 intervals of a run; the source
reads no other number at its Node and owes nothing. No collision acts (one
number, one content, every ray outgoing).

## The derivation, before the runs

A ray of the fan flies straight at 1 / sqrt 3 (the flight table) and every
ray crosses every shell once, so the rays crossing the shell of radius r
per interval are q whatever r, spread over the shell's 4 pi r^2 Nodes; a
ray dwells `dwell` intervals at a Node it crosses (T_d / (S_1 Q) per Link:
110 / 64 = 1.72 on a heading, 1 on (1, 1, 1)). The shell mean of the
presence is therefore

    presence(r) = q x dwell / (4 pi r^2),

and the scalar probes, which owe `by_clock(age, presence, 1)`, have a mean
owed count per self-creation k_s(r) with **k_s x r^2 constant** (q x
dwell / (4 pi) = 290 x 1.72 / 12.57 = 40 with the heading's dwell, less
with the fan's). A ray at r has the age r x sqrt 3 (plus its dwell), so the
age moment at a Node is presence x r sqrt 3 and the age probes, which owe
`by_clock(age, presence x age, 2)`, have **k_a x r constant**, q x dwell x
sqrt 3 / (8 pi): the ratio of the two constants is (k_a x r) / (k_s x r^2)
= sqrt 3 / 2 = 0.866, the age of a ray per Link of radius over the width 2.
This is M / r beside M / r^2 read from the same rays: the presence is
what the push reads (M / r^2), the age moment what the clock counts (M / r).

The rate of a clock is its self-creations per interval, age / (age +
waited) = 1 / (1 + k). Two age clocks at r1 and r2 therefore run at the
ratio

    rate(r1) / rate(r2) = (1 + k_a(r2)) / (1 + k_a(r1)),  k_a(r) = C / r,

which for k << 1 is 1 - C (1 / r1 - 1 / r2), the weak-field redshift
between two heights. Here k_a is 2 to 9 (a strong count, chosen so that the
clocks count a few units per self-creation and the run resolves them): the
exact ratio is the model's statement, and the first-order line is printed
for the reader and expected to fail (it goes negative).

**The granularity of the fan.** A single probe on a line of the fan reads
that line's beam: a heading's beam dwells 2 intervals per Node so its
presence is about 2 whatever r (series C: "on the axis the presence does
not fall with r"), and a Node on no line reads 0. The 1 / r^2 and 1 / r
laws live in the shell means, which is why the probes cover the whole
shells; the single probes on the +x axis and nearest the (1, 1, 0) and
(1, 1, 1) diagonals are read beside them to show the grain: k_s x r^2 on
the axis is expected to grow as 2 r^2 and k_a x r as r^2 sqrt 3, and a
diagonal Node off every line reads nothing. From r of about 7 on, the 290
lines hit fewer Nodes than the shell holds (290 x dwell against 4 pi r^2):
the fraction of a shell's probes that count anything is expected to fall
from 1 at r = 4 to about 0.2 at r = 14, and the shell mean still reads the
law as the mean over hit and unhit Nodes.

## The criteria, pinned before the runs

- A record check (fails the tool): every run completed, the books balanced
  at every tick.
- **The window**: the front reaches r = 14 near tick 25 (14 x sqrt 3); the
  readings are the mean owed count per self-creation per probe over the
  intervals 100 to 300 (the world replayed through the API, the probes'
  (age, waited) at both ends), averaged over the shell; the whole-run mean
  (`waited / age` from `run.json`) is printed beside it.
- **k_s x r^2 constant** (the `scalar` world): within +- 15 % of its mean
  over r = 6 to 14 at every r >= 6 (r = 4, where many lines cross one
  Node, is reported and not held).
- **k_a x r constant** (the `age` world): within +- 15 % of its mean over
  r = 6 to 14 at every r >= 6.
- **The redshift ratio**: rate(r) / rate(14) measured, (1 + k_a(14)) /
  (1 + k_a(r)), against the 1 / r law fitted at the reference radius,
  (1 + k_ref) / (1 + C / r) with C = k_a(14) x 14, within 15 % of the law's
  shift 1 - law at every r >= 6; the same law with C the shell mean is
  printed for the reader; the first-order line is printed and expected to
  fail at these k.

## The worlds

| World | `suspension` | The probes' entry for `m` | What the clock counts | Expected |
| --- | --- | --- | --- | --- |
| `scalar` | [1, 1] | `pass` | the presence | k x r^2 constant |
| `age` | [1, 2] | `{"rule": "pass", "reads": "age"}` | the age moment `sum amount x age` | k x r constant |

Run them in parallel and read the records:

```bash
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/redshift examples/events/redshift/scalar.json examples/events/redshift/age.json
PYTHONPATH=src python tools/redshift_readings.py artifacts/redshift
```

`tools/redshift_readings.py` prints the record checks, the shell means per
radius with k x r^2 and k x r against their expectation, the single probes
on the axis and the diagonals, and the redshift ratios of the age clocks.

## The readings (2026-09-20, measured against expected)

Source fingerprint
`cd90313373651164e7f1a1e5f2d0f5019356cd5fb4bc9d3f909511b4f783be52` (the
worktree of `claude/universe24-new-3ytqde` on the age commit), Python
3.14.0rc2, numpy 2.5.3, headless, four cores, `--jobs 2`; every run
completed in 16 s with the books balanced at every tick; the tool: 0
record checks failed, 11 readings inside, 3 outside, registered, none
moved (the kinds as above).

The shell means of the owed count per self-creation (the window 100 to
300; "counting" the fraction of the shell's probes that owed anything):

| r | probes | counting | k scalar | k scalar x r^2 (expected 41.48 +- 15 %) | k age | k age x r (expected 36.07 +- 15 %) |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 210 | 1.00 | 2.521 | 40.34 (reported) | 8.748 | 34.99 (reported) |
| 6 | 450 | 0.63 | 1.092 | 39.30 inside | 5.711 | 34.27 inside |
| 8 | 762 | 0.42 | 0.700 | 44.82 inside | 4.904 | 39.23 inside |
| 10 | 1250 | 0.32 | 0.416 | 41.56 inside | 3.657 | 36.57 inside |
| 12 | 1814 | 0.20 | 0.297 | 42.74 inside | 3.097 | 37.17 inside |
| 14 | 2498 | 0.17 | 0.199 | 38.99 inside | 2.366 | 33.12 inside |

- k_s x r^2 (expected constant, q x dwell / (4 pi) = 40 with the heading's
  dwell): measured 39.0 to 44.8 over r = 6 to 14, the mean 41.5, the ripple
  +- 7 %; inside at every r >= 6 (r = 4: 40.3). The fan dilutes as the
  shell's Nodes: Gauss in space.
- k_a x r (expected constant): measured 33.1 to 39.2 over r = 6 to 14, the
  mean 36.1, the ripple +- 9 %; inside at every r >= 6 (r = 4: 35.0). The
  ratio of the two constants 36.07 / 41.48 = 0.870 against sqrt 3 / 2 =
  0.866: the age of a ray at r is r sqrt 3, the flight's 1 / sqrt 3. The
  pair holds: the same rays read M / r^2 as the presence and M / r as the
  age moment.
- The whole-run means (0.165 to 2.295 scalar, 0.988 to 6.719 age) are
  below the window's by the empty intervals before the front and by the
  start-up of the fan (the source's first shells), as expected.
- The granularity (the fraction counting 1.00, 0.63, 0.42, 0.32, 0.20,
  0.17 at r = 4 to 14; expected about 0.2 at r = 14): the single probes
  read the beam of their line, k scalar 2.03, 2.03, 1.99, 1.99 on the +x
  axis at r = 6 to 12 (the heading's dwell of 2; 1.00 at r = 4 and 14,
  where the line dwells one interval at that Link) so k scalar x r^2 grows
  73, 130, 199, 286 and k age x r 65, 106, 172, 255 with r; the (1, 1, 0)
  line 1.00 at r = 4 to 10 and 14 (its dwell 1 at those Links) and the
  Node nearest the diagonal at r = 12 off every line, 0; the (1, 1, 1)
  line 1.00 at r = 4, 10, 12, 14 and the nearest shell Nodes at r = 6 and
  8 off every line, 0. As predicted: the laws are shell means, and no
  radius up to 14 leaves a shell reading nothing.

The redshift of the age clocks (the window), rate = 1 / (1 + k),
rate(r) / rate(14) measured against the 1 / r law fitted at r = 14 (C =
2.366 x 14 = 33.12) and, for the reader, with C the shell mean 36.07:

| r | k age | rate | rate(r) / rate(14) measured | the 1 / r law (fit at 14) | the law, shell C | first order | expected: within 15 % of the shift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 8.748 | 0.1026 | 0.3453 | 0.3627 | 0.3570 | -4.91 | reported |
| 6 | 5.711 | 0.1490 | 0.5015 | 0.5162 | 0.5101 | -2.15 | inside |
| 8 | 4.904 | 0.1694 | 0.5701 | 0.6548 | 0.6492 | -0.77 | outside |
| 10 | 3.657 | 0.2147 | 0.7227 | 0.7805 | 0.7763 | 0.05 | outside |
| 12 | 3.097 | 0.2441 | 0.8215 | 0.8951 | 0.8928 | 0.61 | outside |
| 14 | 2.366 | 0.2971 | 1.0000 | 1.0000 | 1.0000 | 1.00 | inside |

- The ratio of two clocks' rates follows the 1 / r law in form (a clock
  nearer the mass runs slower: 0.35, 0.50, 0.57, 0.72, 0.82 of the clock at
  r = 14 at r = 4 to 12) and is outside the 15 % criterion at r = 8, 10 and
  12: the deviation from the fitted law is 0.085, 0.058, 0.074 on shifts
  of 0.345, 0.220, 0.105, the ripple of k_a x r (33.1 at the reference
  radius against 39.2 at r = 8, +- 9 % of the mean) entering the ratio
  (1 + k_ref) / (1 + k_r) whole while the shift it is compared with
  shrinks as 1 / r - 1 / 14. With C the shell mean the law moves by less
  than 0.01. The first-order line fails as expected: k of 2 to 9 is not a
  weak field. A weak-field run (k << 1, a larger `suspension` denominator
  or a smaller q) is the follow-up for the model owner; nothing was
  changed here.
- Host cost: 16 s per run (300 intervals, about 8000 rows in flight, 6985
  measured events), the `age` run 15.5 s against the `scalar` run 16.0 s:
  the age reading costs nothing measurable.

## Verdict

The pair of nature holds in space, on the GameBoard, by two readings of the
same rays: the
presence read by the shell falls as M / r^2 (k_s x r^2 = 41.5 +- 7 %) and
the age moment as M / r (k_a x r = 36.1 +- 9 %), their ratio sqrt 3 / 2 to
half a percent, the age of a ray being its distance over the flight's
speed. The clocks' ratio follows the 1 / r law in form and misses the
pinned 15 %-of-shift criterion at three radii by the ripple of the shell
means; the weak-field line needs a weak field. The grain of the fan is as
predicted: a single probe reads its line's beam, and the laws are the
shell means. Every number of this verdict is a shell mean by the replay,
GAMEBOARD; the detector reading is not made.

## Re-read under clock-age-v1 (2026-09-21)

The model owner's word of record 394: a clock counts the age moment by
default, so the `scalar` world's probes (`read` entries without a word,
their records still the presence) now count the age moment at
`suspension` [1, 1], twice the `age` world's count at [1, 2] for the same
rays; the `age` world is byte-identical (record 409). Both run again on the
head of branch `clock-age-v1` (`tools/run_series.py --jobs 2`, 300
intervals) and read by `tools/redshift_readings.py`, whose power of r is
now 1 for both worlds (k x r the expected constant; k x r^2 for the
`scalar` world until the word). GameBoard readings, the shell means of the
owed count per self-creation in the window 100 to 300, the registered
value beside the new:

| r | probes | k, `scalar` world (was, the presence) | k x r (was k x r^2) | k, `age` world | k x r |
| --- | --- | --- | --- | --- | --- |
| 4 | 210 | 17.268 (2.521) | 69.07 (40.34) | 8.629 | 34.52 |
| 6 | 450 | 11.366 (1.092) | 68.20 (39.30) | 5.711 | 34.27 |
| 8 | 762 | 10.166 (0.700) | 81.33 (44.82) | 4.904 | 39.23 |
| 10 | 1250 | 7.123 (0.416) | 71.23 (41.56) | 3.657 | 36.57 |
| 12 | 1814 | 6.065 (0.297) | 72.78 (42.74) | 3.141 | 37.69 |
| 14 | 2498 | 4.815 (0.199) | 67.41 (38.99) | 2.366 | 33.12 |

- The `scalar` world's k x r is constant within the ripple, 67.4 to 81.3
  over r = 6 to 14, the mean 72.19, inside at every r >= 6: the same rays
  read M / r under both worlds now, and 72.19 / 36.18 = 2.00 is the ratio
  of the two widths ([1, 1] against [1, 2]). The pair of readings of
  section 8 (k_s x r^2 = 41.5 and k_a x r = 36.1 from one run, Einstein's
  pair from the presence and the age moment) is now read by the record's
  components, the presence on the `scalar` world's `read` records and the
  age moment on the `age` world's, not by the two clocks; a clock reading
  the presence declares `reads: "presence"` since the word.
- The redshift ratio of the age clocks (the `age` world, unchanged): 11
  readings inside and 3 outside as registered (the tool's exit 1 is that
  count); the `age` world's numbers here are the head's, equal to `main`'s
  by the digests of record 409.
