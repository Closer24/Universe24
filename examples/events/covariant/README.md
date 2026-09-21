# Series S: the covariant readings (`covariant-readings-v1`)

The four worlds of series S, written by `make_worlds.py` with their
expectations before the runs (`expectations.json`); the register entry is
[S, the covariant readings (2026-09-21)](../../../docs/EXPERIMENTS.md#s-the-covariant-readings-2026-09-21)
and the evidence is in [validation](../../../docs/VALIDATION.md). The model
owner's decision (2026-09-21, record 270 of the log of 2026-09-20, on the
derivation mathematician's [section 17](../../../docs/DERIVATIONS_BEAM.md#17-the-law-above-newton-and-einstein-the-theorem-of-covariant-readings-built-on-newton-and-tried-on-lorentz):
"Yes, that is what comes out right, no?"): `covariant-readings-v1` is built
beside the law under its own identity in place of lorentz-v1, after a
physics-rule review of the four readings (records 297 and 314; the design
as amended in [17.6](../../../docs/DERIVATIONS_BEAM.md#176-amended-per-the-physics-rule-review-of-covariant-readings-v1-record-297-the-nine-must-fixes-the-integer-forms-the-should-fixes)),
run against the pins of 18.1 (a) and (c) as restated there; and today's
order (2026-09-21, about 11:52Z, translated: "you said covariant-readings-v1
is needed to confirm the formula or to run it; have them do it, urgently"):
the formula at the top of the owner's page, W = E_0^2 + 3 **p** . **p** (the
exact square of a body's energy, compared and never rooted; E_0 = Q S M;
c^2 = 1 / 3), must stand on a run and not on paper alone. A research run,
made once, never a test; every expectation below was written before the
run; a reading outside its expectation is reported with its numbers, never
moved. Every number is one of two kinds ([the register](../../../docs/EXPERIMENTS.md),
"Two kinds of readings"): a DETECTOR reading (the products' clicks on the
+x face; the centre's pointer) or a GAMEBOARD reading (the `become` line's
tick, the `energy` lines, the intervals owed to proper time: the host's
view, a diagnostic). The readings tool is `tools/covariant_readings.py`,
every line labelled by its kind.

## What was built (the engine, under the world key alone)

The world key `covariant_readings` (`{"c2": [1, 3], "grain": g}`, optional
`"books"`; absent by default; refused with `action`), the identity
`covariant-readings-v1` under the record's `hypotheses`. Under it, for
every body that is not `fixed` (a fixed measured event is an apparatus held
in place: its momentum line is the push it took and never a motion, so it
carries no readings and keeps the lattice's clock; the design speaks of
bodies with a drive), the four readings of section 17 in the integer forms
of 17.6:

- **(iii) the energy as the exact square** (17.6 M3, M7): at every frame
  E'_0 = Q S M is read from the content (a change of content re-reads it,
  the kinetic part kept), W = E'_0^2 + 3 **p** . **p** is formed from the
  record's own momentum (bilinear, nothing accumulated, no drift), and E'
  is kept as the largest integer with E'^2 <= W by the comparison verb
  alone: the load-time root `isqrt` once (a declared rounding of T_D's
  class; a world may declare `E` instead, within one of the root), then a
  rise by one while (E' + 1)^2 <= W and a fall by one while E'^2 > W, the
  invariant E'^2 <= W < (E' + 1)^2 checked after and the run refused
  otherwise. At the identity's grain g (a power of two dividing Q S):
  E'_0 / g, the momentum's whole part over g and W / g^2, every product
  tested by division before it is formed (2^18 on the coasting world, 1 on
  J4).
- **(iv) the proper-time gate** (17.6 M1): after every self-creation the
  body owes `by_drive(acc_tau, E' - E'_0, E'_0)` further intervals, a
  second owed count on its record beside the crowd's (additive in
  intervals), so its self-creations come one per E' / E'_0 = gamma
  intervals in the mean and the age, `become`, the turn, the lamp and the
  drive's gain follow its proper time; the drive's wall loses its cap term
  (`step_divisor` with `cap` false: Q S M alone, the one primitive with one
  term selected off), so the pace per lattice interval is p / E' = p c^2 / E
  in the mean, the covariant dispersion.
- **(i) the count per turn** (17.6 M1, N1): the crowd's count is charged
  per self-creation with the sum of the clock's readings since the last
  one (the owed intervals' readings summed on the record).
- **the release** (17.6 M6, N4): the free release runs per lattice
  interval at the rate held x E' over E'_0 x d (the content-equivalent of
  the body's own energy; at rest the law's count exactly).
- **the declarations** (17.6 N2, N3, N5): the domain |**p**|_1 <= Q S M
  (refused at load and at the frame); the push ceiling of one grain per
  interval on the push the record took (refused at the frame: under it
  the root's comparisons are at most three per frame; a change of content
  by dM moves E' by about Q S |dM| / g in that frame, counted and reported
  as the host cost, the design's loop as written); the identity 3 h n =
  Q S d per paid family a diagnostic line of the record (`off_identity`),
  a refusal only under `books`.
- **the record**: the `energy` line per body per interval (`energy`,
  `rest`, `square`, `creating`, `owed`, `comparisons`), `energy` on the
  `step` line, the `covariant` block and `acc.tau` of a body's state, the
  run's `covariant_readings` block ([ENGINE.md](../../../docs/ENGINE.md#the-detectors-readings-by-type)).

Not built, per 17.6 and record 314: reading **(ii)** the push as the
gradient of the age moment (`-grad(A)` alone is not Lorentz's 1904 pair;
the magnetic part waits for `source-velocity-v1`), and with it the
contraction and the pair's round trips (pin (b) of 18.1, withdrawn there).
The base is `main`'s per-axis drive (form B, record 342, is BLOCKED in its
review, record 348, and not on `main`): on the two pinned worlds every
momentum lies on one axis, where the per-axis drive without its cap term
and form B's directional accumulator without its cap term are the same
count, so the pinned runs are as 17.6 derives them; the OFF baseline is
`main`'s register, replayed byte for byte (below), not form B's.

## The worlds

| World | What | The key |
| --- | --- | --- |
| `j4_muon_rest` | an open bar of 201 x 1 x 1 (the +x face at x = 200), K 2^20, N 64, `release` [1, 2^20], `suspension` 0, `width` 1; one muon of the catalog's `mu` (content 207, the electron's whole charge -7344 over its 207 units) at x = 10, `directions` [[1, 0, 0]] alone, `become` at 64 into the catalog's `e` (the body left of no content) with the products `beta` (1, 207: the catalog's electron born by `become`, a paid row of the muon's whole content and its charge) and `nu` (1, 0); the two faces the detectors; 420 intervals | `c2` [1, 3], `grain` 1 |
| `j4_muon_3640` | the same muon at p = 3640 label units (E' at load 14 671, gamma 1.1074, beta 0.4297, the pace 0.2481 Links per interval) | the same |
| `j4_muon_12856` | at p = 12 856 (E' 25 910, gamma 1.9558, beta 0.8594, the pace 0.4962; the Manhattan momentum at 0.970 of Q S M = 13 248, inside the domain) | the same |
| `coasting_none_covariant` | series G2's `coasting_none` as registered (the 24 stars thrown at their declared momenta, the centre's `wave` set, the families by reference), the model id naming the record rule so that the tool reads z from the gather lines (the register's `source` rule, record 124: since the one click every unit of a star's light is a record and the `wave` set's own pointer no longer turns); 400 intervals | `c2` [1, 3], `grain` 2^18 (2^16 is refused: W / g^2 beyond the bound) |

```bash
python examples/events/covariant/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/covariant examples/events/covariant/*.json
PYTHONPATH=src python tools/covariant_readings.py artifacts/covariant
```

The J4 runs take about 0.3 s each, the coasting run about 43 s.

## The expectations, pinned before the runs (`expectations.json`)

Derived by the generator from the engine's own rules (the load-time root,
the proper-time count from an empty accumulator, the drive's whole steps,
the flight table's steps of a heading row) beside the design's numbers
(17.6 M2, M9, N6; 18.1 (a) and (c)):

| World | Reading | Kind | The design's pin | The derived integer |
| --- | --- | --- | --- | --- |
| `j4_muon_rest` | the `become` line (the 64th self-creation) | GAMEBOARD | 64 +- 1 | 64 at x = 10 |
| | the product `beta`'s click on face:+x | DETECTOR | 391 +- 2 (N6: 390.6) | 392 (191 steps of a heading row from x = 10) |
| `j4_muon_3640` | the `become` line | GAMEBOARD | 70.9 +- 1 | 70 at x = 27 (64 + floor(63 x 1423 / 13248)) |
| | the `beta` click | DETECTOR | 367 +- 2 (N6: 368.2) | 369 (174 steps) |
| `j4_muon_12856` | the `become` line | GAMEBOARD | 125.2 +- 1 | 124 at x = 72 (64 + floor(63 x 12662 / 13248)) |
| | the `beta` click | DETECTOR | 345 +- 2 (N6: 345.2) | 345 (129 steps) |
| every J4 world | E' at load | GAMEBOARD | isqrt(13248^2 + 3 p^2) | 13 248, 14 671, 25 910 |
| `coasting_none_covariant` | `s_mz2`'s z, the late window [300, 400) | DETECTOR | 0.369 +- 0.003 (the centres 0.3687 with the continuum's beta, 0.3663 on the heading; the register's 0.2636 without the key) | gamma 1.04967 (E' / g 1 128 171 883 over E'_0 / g 1 074 790 400), the pace p / E' 0.1755 |
| every run | E'^2 <= W < (E' + 1)^2 on every `energy` line | GAMEBOARD | holds | holds (the engine refuses otherwise) |

The derived tick of the k-th self-creation, k + floor((k - 1) (E' - E'_0) /
E'_0), is 64 gamma less (gamma - 1) to within one: the count is charged
after each of the first k - 1 self-creations from an empty accumulator, so
the discrete cadence lies one (gamma - 1) below the continuum's k gamma
that the design's 70.9 and 125.2 state; both are pinned, the design's with
its tolerance and the derived integer exactly.

## What was measured (2026-09-21)

`tools/covariant_readings.py` on the four runs (the head `24e0c1ba...` of
`run.json`'s `source_sha256`; Python 3.14.0rc2, numpy 2.5.3, headless; the
J4 runs 0.3 s each, the coasting run 42.9 s; every run completed with the
books balanced at every tick): 0 record checks failed, 24 readings inside,
1 outside, nothing moved.

| World | Reading | Kind | Measured | Verdict |
| --- | --- | --- | --- | --- |
| `j4_muon_rest` | E' at load | GAMEBOARD | 13 248 (E'_0 13 248) | inside |
| | the `become` line | GAMEBOARD | tick 64 at x = 10 | inside (the design's 64; the derived 64) |
| | the `beta` click on face:+x | DETECTOR | tick 392, content 207; the decay derived back 64 | inside (the design's 391 +- 2; the derived 392) |
| | the invariant | GAMEBOARD | 420 lines, 0 failures; 0 intervals owed | inside |
| `j4_muon_3640` | E' at load | GAMEBOARD | 14 671 | inside |
| | the `become` line | GAMEBOARD | tick 70 at x = 27 | inside (the design's 70.9 +- 1; the derived 70) |
| | the `beta` click | DETECTOR | tick 369; the decay derived back 70 | inside (the design's 367 +- 2, at the edge; the derived 369) |
| | the invariant | GAMEBOARD | 420 lines, 0 failures; 6 intervals owed to proper time (gamma 1.1074: 64 self-creations in 70 intervals) | inside |
| `j4_muon_12856` | E' at load | GAMEBOARD | 25 910 | inside |
| | the `become` line | GAMEBOARD | tick 124 at x = 72 | **OUTSIDE** the design's 125.2 +- 1 by 0.2; inside the derived 124 |
| | the `beta` click | DETECTOR | tick 345; the decay derived back 124 | inside (the design's 345 +- 2; the derived 345) |
| | the invariant | GAMEBOARD | 420 lines, 0 failures; 61 intervals owed (64 self-creations in 124 intervals, gamma 1.9558) | inside |
| `coasting_none_covariant` | `s_mz2`'s z | DETECTOR | 0.3674 | inside (0.366 .. 0.372; the design's 0.369) |
| | `s_mz2`'s E' / g at load | GAMEBOARD | 1 128 171 883 over 1 074 790 400, gamma 1.04967 | inside |
| | `s_mz2`'s pace over the late window | GAMEBOARD | 18 steps in 100 intervals, 0.180 | inside (p / E' 0.1755 within 0.01) |
| | the invariant | GAMEBOARD | 9567 lines, 0 failures; `s_mz2` owed 18 intervals of 400 (the outer stars up to 55) | inside |
| | the load-time diagnostic | GAMEBOARD | 25 paid families off 3 h n = Q S d by 3 - 2^48 x 4 198 400 / 2^22 each (quantum 1 at Q S = 2^26); `books` false, no refusal | reported |

**The one reading outside.** The muon at p = 12 856 fires its 64th
self-creation at tick 124, where the design pins 125.2 +- 1 (0.2 beyond
the tolerance). The cause is the discrete count itself, not a defect: from
an empty accumulator the k-th self-creation falls at k + floor((k - 1)
(E' - E'_0) / E'_0) = 64 + floor(63 x 12662 / 13248) = 124, one (gamma - 1)
= 0.96 below the continuum's 64 gamma = 125.2 (the same count gives 70
against 70.9 at 3640, inside by the smaller gamma - 1 = 0.11); the
reviewer's own re-derivation of record 314 (M2) gives 124 too. The
detector's reading, the electron product's click at 345, is inside the
design's pin exactly. Nothing was moved.

**The host cost apart from the model's.** Per body per interval one frame
of the readings: two or three multiplications, three comparisons under the
push ceiling; where a body's content changes (a lamp's cost of one unit per
self-creation on the coasting world, the muon's `become`) the root walks by
comparisons to the new value: at most 258 comparisons in one frame on the
coasting world (E'_0 / g moves by 256 per unit of light spent), 2083, 9811
and 25 123 at the muon's `become` (the whole content left as products, E'
walked to the empty body's sqrt 3 |p|). The J4 runs 0.3 s; the coasting run
42.9 s against 41.0 s without the key on the same head (the OFF replay
below), the `energy` lines 9567 of the record.

**The OFF replay (byte for byte).** `hubble_stars/coasting_none` without
the key, run on the base (origin/main `f5417ab3`, the engine before this
branch) and on the head: the state `1a385429...`, the books `33cf0ac7...` and
the events `f75ca182...` equal on both (`expectations.json`, `off_replay`);
the gate set's digests of `gate_set.json` unchanged
(`tests/test_amplitude_click.py` (d), `tests/test_covariant_readings.py`
(a)).

**What the run says for the owner's formula.** W = E_0^2 + 3 **p** . **p**
stands on the run: on every one of the 10 827 `energy` lines of the four
runs E'^2 <= W < (E' + 1)^2 held with E' kept by comparisons alone, never
rooted after the load; the muon's clock slowed by E'_0 / E' = 1 / gamma
(64 self-creations in 70 and 124 intervals), its products reached the face
at the ticks the flight table derives from that clock, and the moving
star's light read z = 0.3674 where the law without the key read 0.2636 and
nature's gamma (1 + beta) gives 0.369 at the identity's beta 0.3040. What
the run does not give: the contraction (reading (ii), not built), and the
first-order departure of the drive that the law keeps without the key.
