# Physics-rule review, second round: covariant-readings-v1 as amended (17.6)

The physics-rule reviewer of beam-v1, 2026-09-21. Read-only review of
`origin/claude/derivations-beam` at `a6c1b1cf` (a detached worktree; the
amendment commit `d56c0df7` of PR #476 over `main` `a4bc9cd8`; `origin/main`
now contains the branch head, PR #476 merged at `bbf161d9`). Nothing
edited, no run, no fit, no new physics. Read: the first round
(`covariant_review_REVIEW.md`, ADMISSIBLE WITH MUST-FIXES, M1 to M9, S1 to
S11), then docs/DERIVATIONS_BEAM.md 17.6, 17.3, 18.1's amendment, 19.5's
amendment, 21.2 rows 38, 39, 44, 21.4 rows E2 to E7 and E15, the host
script `amended_pins.py` and its output, docs/designs/light_speed/FORM.md
section 3 (form B, the base, in build on branch directional-drive),
AGENTS.md's change boundaries (the three tests, record 281), and the engine
on the branch: `events/engine.py` (`_frame_all`, `_suspend`, `_move`),
`events/nature_beam.py` (the reading `counted`, the release, `become`'s
products), `core/integer.py` (`by_drive`, `at_most`), `events/world.py`
(the keys, `MOMENTUM_BOUND`), `examples/events/hubble_stars/coasting_none.json`
and `examples/events/entities/families.json`.

Notation, once: **p** the momentum vector (label units), p its magnitude,
|**p**|_1 its Manhattan norm; **dp** the push of one interval; c the pace of
a row (1 / sqrt 3 Links per interval in the limit; 32 / 55 on a heading of
the flight table, T_D = 110 at Q = 64); beta the speed over c; gamma the
Lorentz factor; Q the label's scale (64); S the world's width; M a body's
content; E' the energy accumulator in the identity's units (E' = 3 E),
E'_0 = Q S M its rest value, W = E'_0^2 + 3 **p** . **p** its exact square;
g the identity's grain; n / d a clock's rate pair; h a paid family's
quantum; `by_drive(acc, rate, wall)` the count primitive (an accumulator
gains a rate, the whole part in units of the wall is taken, the remainder
kept); `counted` the reading a body's clock takes at its Node in one
interval (nature_beam.py:3190).

## VERDICT: BUILDABLE WITH MUST-FIXES

Readings (iii) the energy accumulator and (iv) the proper-time gate are
buildable after form B lands: the object the identity gates is now the
self-creation, its integers are whole on every register, the invariant is
exact by construction (W is a function of **p**, nothing accumulates), no
root runs at run time, and the pace per lattice interval is `p / E'`
exactly (derived below). Over M1 to M9: CLOSED 4 (M2, M4, M5, M8), PARTLY 5
(M1, M3, M6, M7, M9), OPEN 0. The five PARTLY items give six must-fixes,
N1 to N6, each one design sentence of 17.6; two of them (N2, N3) are
declarations the build itself can carry, the other four must be fixed in
the document before the two pinned worlds are written and run. The first:
N5, the load-time refusal that 17.6's M7 and S10 introduce (`3 h n = Q S
d` for every paid family) refuses `coasting_none`, the world the z pin is
on, so pin (c) is unreachable as amended.

## 1. M1 to M9, one by one

**M1, the counter the identity gates: PARTLY.** Closed by the sentence
"The proper-time accumulator gates the SELF-CREATION, not the phase turn:
after every self-creation the body owes `by_drive(acc_tau, E' - E'_0,
E'_0)` further intervals ... so self-creations come one per `E' / E'_0 =
gamma` intervals and everything counted per self-creation follows proper
time at once" (17.6 M1), with the six counts and their cadence listed.
On the engine this holds: the age advances only at a self-creation
(engine.py:490), `become` reads the age (nature_beam.py:3649), the turn,
the lamp and the release advance in the self-creation branch
(nature_beam.py:3654-3663), the drive steps only at a self-creation
(engine.py:598). The product of the two gates, in one line: per
self-creation the drive gains `|p|_1 S_1 Q / (Q S M S_1 Q) = |p|_1 / (Q S
M)` Manhattan Links on the line of D, whose Euclidean length is `p / (Q S
M)` (FORM.md section 3: `|p|_1 = k S_1`, `|p|_2 = k |D|`); the
self-creations come at the rate `E'_0 / E'` per interval (over N
self-creations the owed intervals are the whole part of `N (E' - E'_0) /
E'_0` with the remainder kept, so N self-creations take `N E' / E'_0`
intervals up to one); the pace per interval is `(p / (Q S M)) (E'_0 / E')
= p / E'` since `E'_0 = Q S M`, and `v = p c^2 / E` with `c^2 = 1 / 3`,
`E = E' / 3` is `p / E'`: exact in the mean with two bounded remainders,
as form B's own pace is. Two sentences remain wrong on the engine:

1. "the crossing count of (i), which is charged per self-creation as
   `_suspend` charges it today and is therefore `gamma (1 - n . beta)`
   per self-creation with no separate rule" is a CLAIM, not a consequence.
   `counted` is reset to 0 for every entry at the start of the law's
   reading (nature_beam.py:2590) and set to THIS interval's reading
   (nature_beam.py:3190); `_suspend` charges `by_drive(acc_owed, counted x
   n, d)` once per self-creation (engine.py:520) with that one interval's
   reading. Under the identity the body self-creates once per gamma
   intervals and the readings of the owed intervals are dropped, so the
   count charged per self-creation is `(1 - n . beta)` times the rest
   count, the factor gamma absent, and 18.1 (d)'s numbers (0.763 / 1.300
   at p = 10, 0.498 / 2.002 at p = 28) and 17.3 (i)'s Doppler with gamma
   do not follow. The gamma needs a declared sum: `counted` accumulated on
   the body's own record over the intervals since its last self-creation
   (one integer, the verb "sum", bounded by the reading bound times the
   owed count; local; generic) and charged at the self-creation. N1.
2. "the pace per lattice interval is ... `p / E'` ... exactly, with the
   cap `1 / sqrt 3` as p grows" holds only while `|p|_1 <= Q S M`. Without
   the cap term the drive's whole part per self-creation is `|p|_1 / (Q S
   M)`, and `at_most = 1` (core/integer.py:94: "caps the count gained at
   one self-creation and keeps the rest in the accumulator ... fires one
   at each following self-creation until it is spent") with the step only
   at a self-creation (engine.py:598) gives at most ONE Link per
   self-creation, i.e. `1 / gamma` Links per interval, a pace that FALLS
   with p above `|p|_1 = Q S M` (gamma 2 on a heading, `sqrt 2` on a body
   diagonal) while the accumulator's deficit grows without bound. The
   pinned muon at p = 12 856 is at 0.970 of the ceiling (13 248); the
   script's (C) at p = 40 000 (beta 0.98) is outside it, where the engine
   would give `1 / 5.3 = 0.19` Links per interval, not 0.567. The identity
   must declare its domain `|p|_1 <= Q S M` (refused at load and at the
   push under the key) or state the pace above it. N2.

**M2, the pins on declared momenta: CLOSED.** "the muon of J4 (`Q S M =
13248`) at `p = 3640` and `12 856` label units has `E'` at load 14 671 and
25 910, `gamma = E' / E'_0 = 1.1074` and `1.9558` ... the 64th
self-creation at 70.9 and 125.2" and "The pin is on the REGISTERED world:
`z = 0.369 +- 0.003`". Re-derived: `isqrt(13248^2 + 3 x 3640^2) = 14671`,
`isqrt(13248^2 + 3 x 12856^2) = 25910`; the owed accumulator from the
declared E' puts the 64th self-creation at interval 70 and 124 (64 gamma
= 70.9 and 125.2), within the one tick. `coasting_none`'s `s_mz2` at `p_z
= 51 901 289 008 505`, `E'_0 = 2^48`: `E' / E'_0 = 1.04976`, `p / E' =
0.17565` Links per interval. One should-fix: `z = 0.3691` uses the
continuum's `beta = sqrt 3 p / E'` in the Doppler factor, while the
design's own S11 says the count is per direction of the flight table
with the lattice's c: on the heading the detector's z is `gamma (1 + v T_D
/ (Q S_1)) - 1 = 0.3667`; inside the `+- 0.003` by 0.0006 of margin, so
the centre should be restated as 0.367 (S11 applied to (c)), or the
tolerance widened to cover both c's. The pin is also blocked by N5.

**M3, the integers of E: PARTLY.** Closed: "`c^2 = [1, 3]` declared by the
identity ... one pair, declared once"; "`E' = 3 E`, `E'_0 = Q S M` (whole
on every register), the invariant `E'^2 - 3 p . p = E'_0^2`"; "The state
carried is NOT an accumulator of the work but the exact square, `W =
E'_0^2 + 3 p . p` (bilinear in **p** ... no drift)"; "The initial `E'` of a
thrown body: `isqrt(E'_0^2 + 3 p . p)` at load, a declared load-time
rounding of `T_D`'s class ... a world may declare `E'` instead, refused if
below `E'_0` or off the invariant by more than 1". The load-time root is
a declared integer of the world's loading (the class of `T_D` and
**u**_d), not a run-time root: it passes. Since W is a function of the
record's **p** alone, no accumulation and no drift exist (the first
round's midpoint objection is void); M7's gain of W on a change of
content is the same function re-read with the new M. The grain: on
`coasting_none` `g = 2^18` gives `W / g^2 = 1.27 x 10^18 < 2^62 - 1`
(verified; `2^16` gives `2.0 x 10^19`, refused), the ceiling under that
grain at `p = 2.8 x 10^14`, gamma 2.000, beta 0.866, so the pinned
momentum sits at a margin of 3.6 in W; the refusal is by division before
the product, as `push_form` does: stated. What remains:

- "at most `ceil(sqrt 3 abs(dp)) + 1` comparisons per interval ... the
  script's (C): 40 000 unit pushes from rest ... at most 3 comparisons
  per step" is bounded to 3 only for a unit push (`|dp| / g <= 1`, since
  `dE' / dp < sqrt 3` and the floor can rise by 2), and the design's own
  general bound is the push's size, not a constant: counterexample, a
  push of 100 label units along **p** at `p = 40 000`, `E'_0 = 13 248`
  moves E' from 70 537 to 70 707, 171 comparisons in one interval. AGENTS
  requires fixed local work for fixed K. On J4 the push is 0 (an empty
  bar: two failing comparisons per interval); on `coasting_none` the
  push per interval in units of `g = 2^18` is not stated. State the fixed
  count: either the largest push per interval at the grain on the two
  pinned worlds (from the registered run's `pushed` lines) with a
  refusal above one unit of g per interval, or a form with fixed work
  (one Euclidean division `by_drive(W - E'^2, 2 E')` as Newton's first
  step, then the bounded comparisons; named here as an option, not
  designed). N3.

**M4, the vector potential withdrawn, (ii) as `-grad(A)` with its integer
form: CLOSED.** "The sentence 'the flow's age-weighted moment as the
vector potential' is wrong ... (ii) is restated as `-grad(A)` alone: the
push per axis is the difference of the age moments at the two
neighbouring Nodes of that axis, `pushed_a = C x (A_(-a) - A_(+a))` with
C the column's coupling as a declared pair applied by one `by_drive` with
its remainder ... a NEW reading set, keyed by the identity, with the
reading bound `reading_fits` applied per neighbour"; "**Lorentz's 1904
pair is NOT derived from (ii)**". The co-moving forces (the rest force
along, gamma across) are the first round's own computation on 12.1's
potential; `source-velocity-v1` is named and not designed, which is the
correct status. (ii) beyond `-grad(A)` is not buildable and is not
claimed to be; the build of (iii) and (iv) does not read it.

**M5, the 5b pin's geometry: CLOSED.** "the pin is withdrawn from 18.1
rather than moved"; the future geometry (12b.2's thrown orbit at beta 0.43
or above, the extents' ratio 0.903 within one Link on 26, the period
within 2 percent) is stated with its grain, under `source-velocity-v1`.

**M6, the release's E, units and owner: PARTLY.** Closed on the three
points asked: "the release's rate reads the content-equivalent of the
body's OWN energy, `E' / (Q S)` in place of M, as one
`by_drive(acc_release, E' x n, Q S x d)` with the remainder kept, whole
integers; each body reads its own `E'` and never 'the set's'". Whole:
`E' x n` and `Q S x d` are products of record integers (on
`coasting_none` `E' x n = 2.95 x 10^14 x n`, `Q S x d = 2^26 x d`, within
the bound for the registered rates; at the grain, `E' / g` over `Q S /
g`, g dividing Q S on both pinned worlds); at rest `E' = Q S M` gives `M
n / d` exactly, the law's release. Local: its own record. Generic: no
family name. What remains is the pin, which the design's own two rules
cancel: the release advances only in the self-creation branch
(nature_beam.py:3663; an owed interval `continue`s at engine.py:487), so
under M1 a moving body releases `(E' / (Q S)) (n / d)` rows per
self-creation and self-creates `E'_0 / E'` times per interval, `M n / d`
rows per lattice interval at every speed (the muon at p = 3640: 229.2
per self-creation, 207.0 per interval; at 12 856: 404.8 and 207.0). A
probe at rest reads rows per lattice interval, so the pin "the ratio 1
at rest and `gamma` in motion" (17.6 M6, 19.5's amendment, 21.2 row 44,
21.4 E15) is not the design's consequence: the probe reads 1 at every
speed, and E15's "the field of a body equal to its own rest plus kinetic
energy" is false per lattice time. The design must choose and say: the
release per self-creation (M1 as written; then the pin is 1 at every
speed and the identity adds nothing to the equivalence principle beyond
the law's) or the release per interval at the rate `E' x n` (then the
active mass per interval is `gamma M` and M1's "all per self-creation"
is amended for the release). N4.

**M7, E on a change of content: PARTLY.** Closed on the rate asked for:
"On every change of the held content by dM ... `E'_0` is read as `Q S M`
at the frame (no state), and `W` gains `Q S (2 E'_0 + Q S dM) dM` (the
identity `(E'_0 + Q S dM)^2 - E'_0^2`, bilinear, exact), so the kinetic
part `E' - E'_0` is kept and the rest part follows the content": exact,
a product of two record integers, and the same as re-reading W from the
new M. Three things remain:

1. Two c's in one identity: W uses `c^2 = 1 / 3` (`3 p . p`) while "their
   energy `3 h s c = 96 h s / 55` in `E'` units, a declared pair on the
   row" uses the heading's `c = 32 / 55`; M3 says "one pair, declared
   once". With the declared pair a row's energy in E' units is `sqrt 3 h
   s`, not a pair: no exact balance exists with `[1, 3]`.
2. "the books balance only if `3 h n = Q S d` for every paid family" is
   asserted, not derived: at the release the emitter's E' falls by about
   `Q S h s` (the rest identity with `dM = -h s`: 64 h s on J4), while the
   row carries `96 h s / 55 = 1.75 h s`; no (h, n, d) closes that gap,
   and 17.3 (iv)'s identity is another statement (the click's `E = h f`
   against the drive's `E'_0` per content at rest). State the exchange's
   accounting as integers on one c, or withdraw "the books balance" and
   E5's "its `W` falling by the rows' energy" until it is derived.
3. What the load-time check fixes and forbids. It fixes: the world's
   turn rate (n, d) (`world.turn_rate`, the clock's rate of `by_drive(acc_turn,
   content x n, d)`, engine.py) and every paid family's quantum h bound
   to `Q S` by `3 h n = Q S d`, so that the click's energy per content and
   the drive's rest energy per content are one number. It forbids, under
   the key: every world with a paid family off the identity, which the
   design itself says is every registered lamp at S = 1 (21.33), AND
   `coasting_none`: its 24 stars are paid families of quantum 1
   (families.json, `"quantum": 1`) with lamps at rate [1, 1] and `Q S =
   2^26`, so `3 n = 2^26 d` needs a turn rate `n / d = 2^26 / 3`, a turn
   of `4 194 304 x 2^26 / 3 = 9.4 x 10^13` phase steps per self-creation,
   refused at half the circle (engine.py:499, `K x N / 2 = 1.3 x 10^8`) by
   any turn rate. So S10's "the load-time check refuses" refuses the
   world pin (c) is on, and pin (c) cannot be run under the identity as
   amended. Make the check a diagnostic (a warning line at load, the
   identity's own test on E5's lamp world), or restrict the refusal to
   worlds that declare the exchange's accounting, and say which. N5.

**M8, the base and the order: CLOSED.** "The identity is built on form B
(record 186, decided, not on `main`): its drive is form B's directional
accumulator without the cap term (M1) ... Form B lands and re-registers
its 47 moving-body worlds first; the identity's OFF baseline is that
register". One should-fix for the build: the identity's drive must be
form B's one primitive with the wall's second term `|p|_1 T_D` selected
off by the key, not a second copy of the accumulator (one canonical
primitive; the OFF path byte-identical by construction).

**M9, the pins as detector readings: PARTLY.** The kind is closed: "The
muon's pin is restated as the products' face clicks on a J4 world file,
to be written before the run ... the two faces as detectors reading the
products' clicks ... the decay tick is derived back from the click by
the flight table and named as derived" (record 281's detector reading;
the `become` line stays a GameBoard diagnostic). The products are rows
(`PendingRow`, nature_beam.py:1566) at the rows' pace, so the flight at
55 / 32 intervals per Link on the heading is the engine's. The ticks
re-derived from the design's integers, at rest: the 64th self-creation
at 64, x = 10, the face at x = 200: `64 + 190 x 110 / 64 = 390.6`, the
pin's 391; at p = 3640 with the drive's whole steps (17 of 17.6, x = 27):
`70.9 + 173 x 1.71875 = 368.2` against the pin's 367 (the script uses x =
27.6), inside the two ticks; at 12 856 (62 steps, x = 72): 345.2, the
pin's 345. What remains: the world file "declares: an open bar `[220, 1,
1]`" while the script derives the clicks for a face at x = 200 (`bar =
200`); with the face at 220 the clicks are 403, 380 and 425, 34 ticks off
the pins. State the shape as `[201, 1, 1]` with the +x face at x = 200,
or restate the three ticks. N6. Two should-fixes: the products leave on
the parent's declared `directions` apportioned from `(clock age + k) mod
n` (nature_beam.py:1568), so the muon's `directions` line (`[[1, 0, 0]]`
alone, or the electron's index against the count) must be declared for
the electron to reach the +x face, at rest too; and "the products of the
catalog" names a catalog with no muon (no `muon` in examples/ or src/):
the family table (contents, quanta, charges, the `become` products) is
written in full in the world file.

## 2. The three tests on the amended (iii) and (iv)

**(iii) the energy accumulator.** Generic: one primitive with declared
integers, `W = E'_0^2 + 3 p . p` with the pair `[1, 3]` and the identity
matrix declared, `E'_0 = Q S M` read at the frame, one grain g per world;
no family name, no kind. Vector: `W` is the bilinear form `p . p` scaled
by a declared integer, `E'` is kept by the comparison verb (`E'^2 <= W <
(E' + 1)^2`), the load-time `isqrt` is a declared rounding of the world's
loading (the class of `T_D`), no root runs at run time; the invariant is
exact by construction since nothing accumulates; the test passes with
one condition, that the comparison count per interval is fixed (N3: the
design's own bound is the push's size). Local: the record's own **p**, M,
`E'`, `W / g^2`; nothing kept at a Node; the six neighbours are not read
by (iii). Passes, with N2 (the domain `|p|_1 <= Q S M`) and N3 (the fixed
count) as the two declarations the build carries.

**(iv) the proper-time gate.** Generic: `by_drive(acc_tau, E' - E'_0,
E'_0)`, one primitive, declared integers, no name. Vector: one count
with its remainder, the wall `E'_0` a constant of the record (cleaner
than the first form's growing wall `d x E`, which is withdrawn), the
rate `E' - E'_0 >= 0` by construction (`W >= E'_0^2`); at the grain
`(E' - E'_0) / g` over `E'_0 / g`, whole; no product, no overflow. Local:
its own record; what it gates is the body's own self-creation, and
every count that follows the self-creation follows it with no second
rule. Passes. The one consequence it does not deliver by itself is the
crowd's count with gamma (N1): the sum of `counted` over the owed
intervals is a local sum on the record, bounded by the reading bound
times the owed count (at most one under N2's domain), and passes the
three tests once declared.

## 3. Bit-exactness with the identity off

A claim the build must test, in three parts. (1) The register after form
B lands, every world with the key `covariant_readings` absent: the
crossing rule's VALIDATION table (the 66 rows) and every registered
`record/` byte-identical, shown in the identity's pull request. (2) A
dedicated test loading every registered world under the parser and
asserting, with the key absent, that no record carries `E'`, `W`, the
grain, `acc_tau` or a second owed count, that `state.json`, `run.json`
and the `step` line have no new field, that `read_arrivals`' group and
bound are the law's (no neighbour read; (ii) is keyed and not built),
and that the drive's wall carries form B's cap term. (3) The edge: a
world with the key and a body at rest (`E' = E'_0`, `W = E'_0^2`, the owed
count 0), every registered integer of that world unchanged (S8's test
1), which proves the key without motion is the identity map. The OFF
baseline is form B's register, not `main`'s: the identity cannot be
tested for bit-exactness until form B lands and re-registers its 47
moving-body worlds.

## 4. The world file's declarations and refusals, as amended

Declared (17.6 S3, M3, M9): the key `covariant_readings` beside `action`
and `meeting`, one object with `c2 = [1, 3]`, `grain` (a power of two),
and per measured event an optional `E'`; the load rule `isqrt(E'_0^2 + 3
p . p)` stated once for the identity. Refused: `E'` below `E'_0` or off
the invariant by more than 1; the key with `action` (S4); the key on the
per-axis drive (M8); `W / g^2` above `MOMENTUM_BOUND`, tested by division;
a paid family off `3 h n = Q S d` (S10; N5 above: this refusal refuses
the pinned world). Missing, to declare: the domain `|p|_1 <= Q S M` and
its refusal (N2); the comparison bound or the push ceiling per interval
at the grain (N3); the sum of `counted` over the owed intervals as a
component of the record (N1); the release's cadence under the identity
(N4); the composition of the two owed counts (the crowd's and the
proper-time's) as additive intervals, one sentence; J4's `directions`
and its family table in full (M9's should-fixes); ENGINE.md's readings by
type with `E'` (a scalar of the state, the `step` line) and the gradient
(a vector, when (ii) is built), at the build (S6).

## MUST-FIXES, numbered

- **N1** (17.6 M1, "charged per self-creation as `_suspend` charges it
  today and is therefore `gamma (1 - n . beta)` per self-creation with
  no separate rule"): `counted` is one interval's reading
  (nature_beam.py:2590, 3190); declare the sum over the owed intervals
  on the record and charge it at the self-creation, or withdraw the
  gamma from (i) and from 18.1 (d)'s pins.
- **N2** (17.6 M1, "the pace per lattice interval is ... `p / E'` ...
  exactly, with the cap `1 / sqrt 3` as p grows"): true for `|p|_1 <= Q S
  M` only; above it the one Link per self-creation gives `1 / gamma`
  Links per interval; declare the domain and its refusal, or the pace
  above it. A declaration the build can carry.
- **N3** (17.6 M3, "at most `ceil(sqrt 3 abs(dp)) + 1` comparisons per
  interval ... at most 3 comparisons per step"): 3 holds for a unit push
  only (171 for a push of 100 at p = 40 000); state the fixed count on
  the pinned worlds at the grain with a refusal above it, or a form with
  fixed work. A declaration the build can carry.
- **N4** (17.6 M6, "the ratio 1 at rest and `gamma` in motion under the
  identity"; 19.5's amendment; 21.2 row 44; 21.4 E15): the release per
  self-creation times the cadence gives `M n / d` per lattice interval
  at every speed; restate the pin as 1 at every speed or the release's
  cadence as per interval, and say which.
- **N5** (17.6 M7, "which the engine CHECKS AT LOAD and refuses otherwise
  under the identity key"; S10 "the load-time check refuses"): the
  refusal refuses `coasting_none` (paid stars of quantum 1 at `Q S =
  2^26`; no turn rate the engine accepts satisfies it), so pin (c) `z =
  0.369 +- 0.003` cannot be run; make the check a diagnostic or confine
  it, and derive or withdraw "the books balance" (two c's in one
  identity, M7's row energy `96 h s / 55` against the pair `[1, 3]`).
- **N6** (17.6 M9, "an open bar `[220, 1, 1]`" against "the click on the
  +x face at tick 367 ... 345 ... 391 at rest", derived for a face at x =
  200): with the face at 220 the clicks are 403, 380, 425; fix the shape
  (`[201, 1, 1]`) or the ticks.

## SHOULD-FIXES

- The z pin's centre per S11's own formula: `gamma (1 + v T_D / (Q S_1))
  - 1 = 0.3667` on the heading, against 0.3691 with the continuum's
  beta; inside the tolerance by 0.0006.
- The design's decay positions 27.6 and 72.1 are the drive's 27 and 72
  (whole steps); the two-tick tolerance covers it; say so.
- The identity's drive as form B's one primitive with the cap term
  keyed off, not a copy (M8).
- The J4 muon's `directions` line and its family table in full (M9);
  "the catalog" has no muon.
- The composition of the crowd's and the proper-time owed counts as
  additive intervals, one sentence (on `coasting_none` `suspension` is 0,
  so only the proper-time count runs there).
- The cited review file `docs/designs/derivations_beam/REVIEW_COVARIANT_READINGS.md`
  is on `main` (874a09ef) after the branch head; resolved by the merge.
- The pace product is exact in the mean with two bounded remainders (as
  form B's own); "exactly" should say so.

## What this review does not do

No run, no fit, no new physics: the counterexamples are the design's own
formulas on the register's declared integers (the comparison count at p
= 40 000; the rows per lattice interval from M1 and M6 together; the
face at 220 against 200; the identity `3 h n = Q S d` on `coasting_none`'s
declared stars); the alternatives named (a Newton step before the
comparisons, the release per interval, the check as a diagnostic) are
what the design must decide, not rules. Nothing here changes beam-v1.
