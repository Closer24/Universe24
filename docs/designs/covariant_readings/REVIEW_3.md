# Physics-rule review, third round: covariant-readings-v1 as built (PR #582)

The open-problems physicist acting as the physics-rule reviewer, 2026-09-21,
on the Boss's bounded order under record 396 (the owner's word of 14:23Z:
the Boss chooses the checks; anything substantive is the owner's question).
Read-only review of branch `covariant-readings` at
`5fb49ab04e9da920e07aa08379b548486b1d10a6` (main `7a93efe1` merged into it;
CI green; 27 files, 2888 insertions), against the design as amended:
DERIVATIONS_BEAM 17.6 (M1 to M9 per record 297, N1 to N6 per record 314),
the owner's decision of record 270 (the covariant readings built beside the
law in place of lorentz-v1, after a physics-rule review, run against 18.1's
pins), skills/physics-rule-validation/SKILL.md and docs/HIGHLIGHTS.md 5.4
(read in full first, the decisions of 2026-09-21 one line each). Nothing
edited on the branch, no engine change, no run of mine; the registered
integers were recomputed on the host from the flight rule's closed form
and the identity's own formulas (below). The Lorentz note's theorem is an
input (the open-problems note on Lorentz, PR #603: the only bilinear form
invariant under the cube's 48 signed permutations is a multiple of the
identity, so the exact square `Xi = m^2 + 3 p . p` is forced once c^2 is
one number; the coupling of the counter to it is declared, not derived).

Notation, once (record 369; the design's letters kept where the code
carries them): **p** the momentum vector in label units and p its
magnitude, |**p**|_1 its Manhattan norm; Q = 64 the label's scale, S the
world's width, M a body's content; m = Q S M the rest energy in mass units
(the code's `E'_0`), E' the energy in the same units (the code's `E'`,
`E / c^2` of the design, 3 E at c^2 = 1 / 3), Xi = m^2 + 3 **p** . **p** the
exact square (the code's `W`); gamma (the Lorentz factor) = E' / m; beta
(the speed over c); g the identity's grain; c = 32 / 55 Links per interval
on a heading of the flight table (T_D = 110 at Q = 64); `by_drive(acc,
rate, wall)` the one count primitive (an accumulator gains a rate, the
whole part in units of the wall is taken, the remainder kept); a
DETECTOR reading a detector's record, a GAMEBOARD reading the host's view
(record 281: a diagnostic, never a measurement).

## VERDICT: ADMISSIBLE WITH CORRECTIONS

The engine as built under the key does what 17.6 says for readings (iii)
the exact square and (iv) the proper-time gate, the count sum of N1, the
release of N4 and the declarations of N2, N3 and N5; with the key absent
the code paths are the old ones line by line and the replays are byte for
byte; every registered integer follows from its stated derivation (I
recomputed each); the pinned detector readings are met. The corrections
are three, all in documents and none in the engine: the design's base
sentence (17.6 M8) and the build disagree, and the build's one-axis domain
must be written into 17.6 (must-fix 1); NATURE rows 4a and 4b cite GameBoard
readings in a comparison with nature and do not state that the identity's
declared domain ends at gamma 2 (must-fix 2); the register's one "outside"
is a reading inside the design's own integer pin (must-fix 3, a label).
Four should-fixes follow. The Boss's rule stands as stated: the pull
request may merge as the hypothesis `covariant-readings-v1` beside the law
once the three lines are carried (two of them in files this branch does
not touch, DERIVATIONS_BEAM by the mathematician and the register's text),
or with them routed as one docs pull request behind it; nothing of it
enters the law.

## 1. The three tests, one line each per rule built

Every rule below is under the world key alone (a hypothesis beside the
law); the tests are applied as record 202 states them.

1. **The exact square and its root by comparisons** (`covariant_square`,
   `energy_root`, `covariant_frame`; 17.6 M3, M7).
   Generic: PASS, one primitive on every measured event that is not
   `fixed`, the declared integers c^2 = [1, d] and g, no family name (the
   branch on `fixed` is a declared key of the event, an apparatus held in
   place, not a family). Vector: PASS, the bilinear form **p** . **p** with
   the identity matrix times d on the record's own momentum, the rest part
   (Q S M / g)^2, and the comparison verb the design admits (at most three
   comparisons per frame under the push ceiling; the root `isqrt` once at
   load, the declared rounding of T_D's class, `integer_root`
   engine.py:337 and world.py `_covariant`); the walk at a change of content
   is should-fix S1. Local: PASS, the record's content, momentum and
   `pushed` alone, nothing kept at a Node.
2. **The proper-time gate** (`_suspend`, the count row `tau`; 17.6 M1).
   Generic: PASS, one `by_drive(acc_tau, E' - m, m)` at the grain, added to
   the crowd's owed count (the two compose as intervals, N1's sentence).
   Vector: PASS, the translation of an accumulator by a rate linear in the
   state (E' and m are state integers) over a wall read from the state, the
   form 15.2 the first round admitted; no root. Local: PASS, its own record.
3. **The drive without its cap term** (`step_divisor(cap=False)`,
   `_move`; 17.6 M1, M8). Generic: PASS, the one primitive with one term
   selected off, not a copy. Vector: PASS, `by_drive(drive_a, p_a, Q S M)`
   per axis. Local: PASS. The base is `main`'s per-axis drive with the
   one-axis domain declared (refused at load and at the frame otherwise):
   on one axis the count is form B's count exactly (form B's
   `by_drive(drive, |p|_1 S_1 Q, Q S M S_1 Q)` on a heading has S_1 = 1 and
   both terms scaled by Q, the same whole parts), so the pace per lattice
   interval is p / E' in the mean as 17.6 derives it; the design's sentence
   says otherwise (must-fix 1).
4. **The crowd's count as the sum since the last self-creation**
   (`counted_sum`, `_suspend`; 17.6 N1). Generic, vector (the sum verb, one
   integer added per interval, reset at the self-creation), local: PASS,
   PASS, PASS; test (e) replays the host's `by_drive(acc, sum, d)` after
   every self-creation.
5. **The free release per lattice interval at the body's own energy**
   (`covariant_release`, `_release` with `release_only`; 17.6 M6, N4).
   Generic: PASS, per family `by_drive(acc_release_f, held_f x E' x n, m x
   d)` with the rate n applied by the table's own numerator
   (measured.py:280) and the wall handed per row; a paid family's row keeps
   its rate 0; a body of no content takes the law's rows. Vector: PASS, the
   rate bilinear in the state (held x E'), every product tested by division
   before it is formed. Local: PASS, its own record and its own E' (never
   "the set's", M6's local test). On an owed interval the body visits the
   release alone: no lamp, no pending row, no `become`, the rows born with
   the phase of the last self-creation (the turn is per self-creation, N4's
   list), which is consistent.
6. **The declarations** (world.py `_covariant`, `covariant_frame`; 17.6
   N2, N3, N5, S3, S4). The domain |**p**|_1 <= Q S M refused at load and at
   the frame naming the record; the push ceiling |**dp**|_1 <= g per
   interval on the rows' push (`pushed`) refused at the frame; c^2 only as
   [1, d]; g a power of two dividing Q S; the key with `action` refused
   (S4); `E` refused without the key, on a `fixed` event, below m or off the
   load-time root by more than one (M3); the identity d h n = Q S d_K per
   paid family a diagnostic line (`off_identity`), a refusal only under
   `books` (N5). All three tests PASS (declarations read at load from the
   world's own data; at the frame from the record).

## 2. LOCALITY-1

Every input of every rule above has a local owner: the content, the
momentum and the push taken are the record's own; the six neighbours are
read by no new reading (reading (ii), the six-Port gradient, is NOT built,
per 17.6 M4 and record 314); the load-time diagnostic reads the world's
family table (data, not a Node). Nothing is kept at a Node; the record
grows by one `CovariantReadings` block per body (eleven integers) and one
count row `tau`. Fixed work per body per interval except at a change of
content (S1). The order of the frame is as the design lists it: the frame
reads m and Xi and walks E' (`_frame_all`, engine.py:650-663) before the
owed count is paid, so every interval has its `energy` line; the step at
the self-creation (`_move`, engine.py:805, `not entry.creating` returns);
the law's reading; then the turn and `_suspend` at the self-creation, or
the sum on an owed interval (engine.py:586-592). No event relays
information across more than one Link per interval by this key: the step is
at most one Link per self-creation (`at_most` 1 kept), the release's rows
walk the flight table as they did.

## 3. The measurement rule

The pins of 17.6 M9 are DETECTOR readings and the runs read them so: the
electron product's click on `face:+x` of the J4 bar at ticks 392, 369 and
345 against the design's 391, 367 and 345 with two ticks' tolerance (the
decay's tick derived back from the click by the flight table, named as
derived), and `s_mz2`'s z from the centre's pointer over the late window
[300, 400), 0.3674 against 0.369 +- 0.003 (the register's `source` rule of
record 124, the same rule that gave the register's 0.2636 without the key:
like for like). The `become` line's tick, the `energy` lines, the intervals
owed, the comparisons and the pace over the window are labelled GAMEBOARD
in the tool (`tools/covariant_readings.py`), in the README's tables and in
ENGINE.md's readings-by-type row ("GameBoard (a diagnostic ...)"), as
record 281 requires. Two places break the rule and are must-fix 2: NATURE
rows 4a and 4b lead their "re-read under covariant-readings-v1" with the
64th self-creation at 70 and 124 (a GameBoard reading) before the clicks,
in the table whose columns are the comparison with nature. The pinning
before the numbers (record 205) is documented: `expectations.json` carries
a `derivations` block per reading and was written by the generator before
the runs; the register entry S carries the derivation beside each number.

## 4. Bit-exactness with the key off

Read line by line on the diff: `counts_table` adds the `tau` row only with
`covariant=True` (measured.py:371); `_suspend` with the key absent is the
old two lines (`if suspension[0]: advance("owed", [counted])`, the second
block gated on `readings is not None`); `_move` passes `cap = world.covariant
is None`, so `step_divisor` returns Q S M + |p_a| as before; `_release`'s
`release_only` is False without the key and the old condition follows
unchanged; `covariant_release` is reached under the key alone; the `step`
line, the state, `run.json` and the `energy` line are added under `entry.
covariant is not None` or `world.covariant is None` guards; `hypotheses`
appends the identity under the key alone; `_covariant` returns None for an
absent key and refuses a stray `E`. Tested: test (a) parses every registered
world outside `covariant/` with `covariant` None, replays the gate world
`detector/grouped_12_nodes` to its `gate_set.json` digests with no `energy`
line, no `covariant` block and no `tau` accumulator, and asserts the wall's
cap term; the OFF replay of `hubble_stars/coasting_none` on the base
(`f5417ab3`) and the head is equal in state, books and events
(`expectations.json`, `off_replay`); the gate set's digests are unchanged
(CI green on the head). The design's S8 test 5 as restated (the OFF
baseline form B's register of 47 moving-body worlds) cannot be run because
form B is not on `main` (BLOCKED, record 348); the baseline tested is
`main`'s register, which is the register in force. Verdict: bit-exact with
the key absent, by code and by replay.

## 5. The world-file declarations

- `j4_muon_rest`, `j4_muon_3640`, `j4_muon_12856`: an open bar [201, 1, 1]
  (the +x face at x = 200, N6), K 2^20, N 64, `release` [1, 2^20] (no row
  within 420 intervals), `suspension` 0, `width` 1, `covariant_readings`
  {c2 [1, 3], grain 1}; the families by reference to the catalog (`mu` new:
  content 207 per measured event, quantum 0, `charge` [-7344, 207], phase
  true; `e`, `beta`, `nu` as registered); one muon at x = 10, `momentum`
  [p, 0, 0] with p = 0, 3640, 12 856, `directions` [[1, 0, 0]] alone (N6),
  `become` at 64 into `e` with the products [beta, 1, 207] and [nu, 1, 0].
  Checked: the charge balances (-7344 on the muon's 207 units; -7344 on the
  beta row of content 207 under D-1; the body left of content 0); |p|_1 =
  12 856 is at 0.970 of Q S M = 13 248, inside N2's domain; the momentum on
  one axis. As M9 and N6 state them.
- `coasting_none_covariant`: series G2's `coasting_none` as registered
  (the 24 stars at their declared momenta, the centre's `wave` set, the
  families by reference), the model id naming the record rule so that the
  readings tool reads z from the gather lines, `covariant_readings` {c2
  [1, 3], grain 2^18}; g = 2^16 refused at load (Xi / g^2 = 2.04 x 10^19
  above MOMENTUM_BOUND = 2^62 - 1, recomputed); 25 paid families off the
  identity reported, `books` absent (N5). As M2 and N5 state it.
- The catalog: `entities/families.json` gains the definition `muon` (`mu`)
  and `make_definitions.py` its line; ENTITY_CATALOG's muon row now names
  the world file; ENTITY_DEFINITIONS counts 49 names. Consistent.

## 6. Every registered integer against its derivation

Recomputed on the host (integers; the flight rule's closed form for the
heading row, `age_of(made) = ceil((2 made - 1) T_D / (2 Q))` with T_D = 110):

| Reading | Derivation (expectations.json `derivations`) | Recomputed | Registered |
| --- | --- | --- | --- |
| E' at load, J4 | isqrt(m^2 + 3 p^2), m = 13 248 | 13 248, 14 671, 25 910 | the same |
| gamma, beta | E' / m; sqrt 3 p / E' | 1, 1.1074, 1.9558; 0, 0.4297, 0.8594 | the same |
| the 64th self-creation | k + floor((k - 1)(E' - m) / m) at k = 64 | 64, 70, 124 | 64, 70, 124 (the `become` line) |
| the decay's Node | 10 + floor(64 p / m) | 10, 27, 72 | the same |
| the `beta` click on face:+x | the decay's tick + the least age at which the heading row has made 201 - x steps | 64 + 328 = 392; 70 + 299 = 369; 124 + 221 = 345 | 392, 369, 345 |
| the design's continuum | 64 gamma; the flight 55 / 32 per Link | 64.0, 70.9, 125.2; 391, 367, 345 (N6: 390.6, 368.2, 345.2) | the pins with tolerances 1 and 2 |
| `s_mz2` at the grain | (m / g, isqrt((m / g)^2 + 3 (p / g)^2)), m = 281 749 854 617 600, g = 2^18 | 1 074 790 400, 1 128 171 883; gamma 1.04967 | the same |
| the pace | p / (E' g) | 0.1755 Links per interval | 0.1755; 0.180 over the window (18 steps in 100) |
| z's centres | gamma (1 + beta) - 1 with beta = sqrt 3 p / E'; with beta = (p / E') / c on the heading | 0.3687; 0.3663 | 0.3687, 0.3663; measured 0.3674, inside 0.366 .. 0.372 |
| the invariant | E'^2 <= Xi < (E' + 1)^2 on every `energy` line | the engine refuses otherwise (`energy_root`) | 10 827 lines, 0 failures |

Every registered number follows from its derivation as written. The
"outside" reading (124 against 125.2 +- 1) is the continuum's number
against the integer cadence; 17.6 M2 itself pins "the integers 70 and 124
by the primitive's own count", which the run meets exactly (must-fix 3).

## 7. Must-fixes (numbered)

1. **The base sentence of 17.6 M8 and the build disagree; the one-axis
   domain is not in the design.** 17.6 M8: "The identity is built on form
   B ... Form B lands and re-registers its 47 moving-body worlds first; the
   identity's OFF baseline is that register." The build (the owner's order
   of about 11:52Z, "have them do it, urgently"; form B BLOCKED in review,
   record 348, not on `main`) is on `main`'s per-axis drive `step_axis`
   with the cap term keyed off and a declared domain: a body's momentum on
   ONE axis, refused at load and at the frame otherwise (world.py
   `_covariant`; engine.py `covariant_frame`). On one axis the two drives
   are one count (section 1, rule 3), so the pinned runs are as 17.6
   derives them; on a fan direction the per-axis drive would give the
   Manhattan pace, which is why the domain is right. The fix is one
   sentence in 17.6 M8 by the derivation mathematician: "Until form B
   lands the identity is built on `main`'s per-axis drive with its cap term
   keyed off, on the domain of a momentum on one axis (refused otherwise),
   where the count equals form B's; the OFF baseline is `main`'s register;
   form B's landing re-registers the identity's worlds with the domain
   lifted." The identity line (BEAM_LAW's added paragraph, HYPOTHESES 25,
   MIGRATION) already carries the domain; the design must too.
2. **NATURE rows 4a and 4b: the measurement rule and the domain.** (a) The
   re-read lines lead with GameBoard readings (the 64th self-creation at
   70 and 124) in the comparison table; the rows must lead with the
   detector's readings (the clicks 369 and 345 with their derivation, z =
   0.3674) and label the self-creation ticks GAMEBOARD, per record 281.
   (b) Row 4a's nature is gamma = 29.33; the identity's declared domain
   |**p**|_1 <= Q S M ends at gamma 2 on a heading (beta 0.866; N2), so
   the CERN regime is outside what this identity can run: the row must
   say "gamma's form reached at gamma <= 2 under the identity; row 4a's
   29.33 is outside its declared domain until form B lifts the cap", not
   leave the reader to infer that 29.33 is covered. One line each, in
   NATURE.md (a file the branch touches).
3. **The register's "1 outside" is inside the design's integer pin.**
   EXPERIMENTS S, the README's table and VALIDATION say the muon at 12 856
   fired its 64th self-creation "OUTSIDE the design's pin by 0.2". The
   design's pin for the integer is 124 (17.6 M2: "at the integers 70 and
   124 by the primitive's own count ... the build reads 70 and 124"; the
   second round's M2 re-derivation: 124); 125.2 +- 1 is the continuum's
   number, which 17.6 gives as the limit. The line is restated: "124,
   inside the design's integer pin exactly; the continuum's 64 gamma =
   125.2 is the limit, one (gamma - 1) above the cadence from an empty
   accumulator." The number is not moved; the label is. (EXPERIMENTS,
   VALIDATION and the README are files the branch touches.)

## 8. Should-fixes

- **S1, the comparison walk at a change of content.** N3's fixed count
  (three comparisons) holds for the rows' push; a change of content by dM
  moves m by Q S dM / g and E' walks by comparisons to the new root: 258
  in one frame on the coasting world, 2083, 9811 and 25 123 at the muon's
  `become` (the whole content leaves as products and E' walks down to
  sqrt 3 p of the empty body), bounded by the host's `ROOT_COMPARISONS` =
  2^24 and reported on the record. A recoil, a hand-over or a click's
  label also move **p** without passing the `pushed` ceiling. The physics
  is unchanged (E' lands on isqrt(Xi) either way), the host cost is not
  fixed work. The correction the design already names (N3): one Euclidean
  division `by_drive(Xi - E'^2, 2 E')` as Newton's first step before the
  bounded comparisons, or the ceiling stated on the momentum's change per
  frame rather than on the push alone. To state in 17.6 M7 and N3.
- **S2, the register's entry S "Features".** It says "no rule of the six
  verbs changed" and cites form B BLOCKED; add the one-axis domain in the
  same sentence as the base (as MIGRATION and HYPOTHESES 25 do).
- **S3, the massless body after `become`.** A body of content 0 with a
  momentum (the muon's shell after its decay) has m = 0, Xi = 3 p . p, E'
  = sqrt 3 p, its clock ungated and no step: consistent, and worth one
  line in HYPOTHESES 25's "what it does not give" (it carries momentum it
  cannot spend; the recoil's owner after a `become` under the identity is
  a question for the weak design, not this one).
- **S4, the two identical README rows.** docs/README.md lists the first
  and second reviews twice (two pairs of identical rows); one pair to go
  in the next docs pull request (not this branch's).

## 9. What stands, in one paragraph for the Boss

The owner's formula stands on the run as the build says: Xi = m^2 + 3 **p**
. **p** compared and never rooted after the load, E'^2 <= Xi < (E' + 1)^2 on
every one of 10 827 lines, the muon's clock at m / E' (64 self-creations
in 70 and 124 intervals), its products at the face where the flight table
puts them from that clock, the moving star's z at gamma (1 + beta) - 1 on
the heading's c (0.3674 against the centre 0.3663, the register's 0.2636
without the key); nothing of the six verbs changed, every registered world
byte for byte with the key absent. What the identity does not give stays
as 17.6 says: the contraction and the magnetic push (M4, M5), the arms'
anisotropy (the open-problems note on the anisotropy, PR #606), and any
speed beyond gamma 2 until form B lands. The verdict is ADMISSIBLE WITH
CORRECTIONS; the corrections are documents only, none touches the engine.

> The scripts of this folder (`root_free_gate.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/covariant_readings/<script>`).
