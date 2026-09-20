# Physics-rule review 2: `doppler-v1` at c72ca30d (worktree `.claude/worktrees/doppler`; branch base f3a41f28; current origin/main d768f831)

Read-only. Read: the full diff origin/main...doppler-v1 (11 files, +1245/-17);
`nature_beam.py` (`quantised_speed`, `flux_pair`, `weighted_flow`, `push_form`,
the call site, the plan's `t_arrival`/`t_label`/`g_moment`, `flight_table`,
`manhattan_steps`), `world.py` (`SPEED_GRAIN`, `step_divisor`,
`weighted_flow_factor`, `_column_budget`, the parser), `engine.py` (`step`,
`_frame_all`, `_move`, `step_axis`), `measured.py`, `run.py`, `core/integer.py`
(`by_clock`, `by_drive`, `checked_work`); BEAM_LAW step 4 and note 38, ENGINE,
MIGRATION, TEST_EXPECTATIONS; `tests/test_doppler.py`; the owner's records 127
to 130 (origin/main `docs/LOG_2026-09-20.md`); the mathematician's GRAIN.md
(origin/claude/series-m-masses); the first review; the local integer operation
contract (ARCHITECTURE.md lines 41-76). Run from the worktree, nothing written
in it: `tests/test_doppler.py` (19 passed, 13 s); arithmetic probes through the
branch's own functions (the bounds on the registered G2 world and the fifteen
gate worlds, the rest identity, the reduced/unreduced floors, the register
intermediate of `quantised_speed`, a rest-direction row); `git merge-tree` of
origin/main and doppler-v1. `tools/check.py` and the full suite were not run.

## Verdict

**NOT MERGEABLE AS IS; MERGEABLE AFTER B1 and S1, S2.** (1) The built form is
the mathematician's GRAIN.md section 2 form exactly, integer for integer, and
the owner's decisions of records 129 and 130 (G = 2^12 a constant beside Q,
the flux one scalar per direction on the arrivals' flow before the columns,
the absolute value, the stars as registered, no load-time bound) are all in
the code and the documents; the physics, the locality and the bounds pass.
(2) The branch does not merge onto current main: PR #377 (the signed drive)
changed `step_axis` and `by_drive` after the branch's base, and the branch
carries the pre-#377 unsigned step with `step_divisor` (conflict in
`engine.py` and an adjacent-row conflict in TEST_EXPECTATIONS.md); the
resolution is one line but the pinned integers must be re-run after it.
(3) Two small defects to fix before the merge: an unchecked register
intermediate `G x |p_a|` (up to 2^74) in `quantised_speed`, and the noun
"board" twice; two more (S3, S4) before or at series G2's merge.

## Blocking

**B1. The branch conflicts with current main (d768f831).** `git merge-tree
origin/main doppler-v1`: CONFLICT in `src/event_universe/events/engine.py`
(the `step_axis` body: origin/main after PR #377 is `by_drive(drive, momentum,
LABEL_SCALE * width * content + abs(momentum))` with the SIGNED rate and
`return (fired or None), drive`; the branch at engine.py:105-110 is the older
unsigned form `by_drive(drive, magnitude, step_divisor(momentum, content,
width))` with the sign restored at the fire) and in `docs/TEST_EXPECTATIONS.md`
(the `test_step_drive.py` row was rewritten on main; the branch adds the
`test_doppler.py` row under it, TEST_EXPECTATIONS.md:45). Resolution: main's
signed body with `step_divisor(momentum, content, width)` as the denominator
and the branch's one docstring sentence ("The divisor D is `world.step_divisor`
..."), and main's row plus the new row; nothing physical changes (D = Q S M +
|p| is the same on both sides, and the weight reads `step_divisor` only). Then
re-run `tests/test_doppler.py` and `tests/test_step_drive.py`: every pinned
momentum of (b), (f) and (g) keeps one sign within an interval, so I expect
the same integers, but the pins are evidence only after the run. Not a
physics defect; a merge cannot happen as the branch stands.

## Should-fix

**S1. `quantised_speed` forms `G x |p_a|` unchecked** (nature_beam.py:1930:
`SPEED_GRAIN * abs(p) // step_divisor(...)`). At the register's momentum
2^62 - 1 the product is 2^74 (verified: `quantised_speed([2^62 - 1, 0, 0], 1,
1)` runs and returns (4095, 1)); for |p_a| > 2^50 it leaves the 62-bit bound
silently in Python integers. The contract (ARCHITECTURE.md lines 71-75:
"Python's arbitrary-precision integers do not remove the model's
working-register bounds: check intermediates before cancellation, scaling or
assignment") and the branch's own R1 discipline on every other product ask for
a test by division before it is formed: refuse `abs(p) > MOMENTUM_BOUND //
SPEED_GRAIN` naming the body, its Node and the axis (the same form as
`flux_bound_error`), and state it in note 38 beside R1. The registered G2 stars
(|p| = 2^46.7, the product 2^58.7) and every gate world are far inside it;
nothing registered is affected.

**S2. The noun "board".** "a 9 x 12 x 9 open board" in
docs/TEST_EXPECTATIONS.md:1536 and tests/test_doppler.py:68. AGENTS.md: "do
not introduce board, lattice, grid or another noun" for the GameBoard. No gate
catches it (`test_repository_language.py` checks scripts only). Replace by
"GameBoard".

**S3. `tests/data/g2_gravity_scalar.json` is a byte-identical copy of
`examples/events/hubble_stars/gravity_scalar.json` on
`origin/claude/series-g2-stars` (b684c997; `cmp` identical, 21 053 bytes).**
On main today there is no other copy (main holds only documentary references
to `hubble_stars`), so the hygiene gate passes; when series G2 lands (record
128 (4): registered after its second run) `tests/test_repository_hygiene.py::
test_json_configurations_have_one_canonical_copy_independent_of_formatting`
fails on the pair. The test (h) that uses it is necessary: the owner's line
"the stars fit as registered" (record 130) is a claim on a registered world,
and (h) (test_doppler.py:660-673: parse under the key, 20 intervals, the books
balanced, a star pushed) is its only evidence in the suite. Fix now, in this
change: MIGRATION and TEST_EXPECTATIONS name the file as a temporary copy that
G2's merge replaces by the example's path (or (h) loads the example when it
exists and the copy otherwise), so the one-canonical-copy rule is met at G2's
merge without a second review. Note also that this world's table is the eight
headings (each star releases on two headings; `directions` per star 2, table
size 8), so (h) exercises the flux where it equals the pair, and the fan's
integers rest on (f)'s synthetic fan alone; say so where (h) is described
(note 38 "The stars fit as registered", TEST_EXPECTATIONS (h)), so nobody reads
(h) as a fan run.

**S4. The age product inside `by_clock` is still unstated** (the first
review's S3, unanswered). `weighted_flow` tests |V_d| x num_d by division
(nature_beam.py:2008) and then `by_clock(age, |V_d| x num_d, G Q |v|^2)`
(nature_beam.py:2010) forms `(age + 1) x |V_d| x num_d` with no `checked_work`
(core/integer.py:58-67): a Python integer beyond the register at a large age
(for the star at age 10^6: 2^51.4, inside; at age 2^40 with a product of 2^45,
2^85, outside, and the function returns). It is the same convention as the
columns' `by_clock` in `push_form` (nature_beam.py:2087), and ENGINE.md line
318 states it for the pointer, but note 38's "The bounds" paragraph
(BEAM_LAW.md:2727-2740) states R1 on |V_d| x num_d and nothing about the
product with the age. One line there: the age product inside `by_clock` is a
Python integer beyond the register, as for every column, or bound it.

## Notes

**N1. The form is GRAIN.md section 2, exactly; no deviation, no changed
integer.** `flux_pair` (nature_beam.py:1934-1960): numerator `abs(G Q |v|^2 -
T_d x sum_a s_a w_a v_a)`, denominator `G Q |v|^2`, `s_a = sign(p_a)` (0 at
rest), `w_a = G |p_a| // D_a` with `D_a = step_divisor = Q S M + |p_a|`
(world.py:449-458; M = `frame_content`, S = `world.width`, the same function
`step_axis` reads), `T_d = flight.resolution[d] = isqrt(3 |v|^2 Q^2)`
(nature_beam.py:575-579), the row's velocity `(Q / T_d) v` per axis verified
from `manhattan_steps` m(tau) = (2 tau S_1 Q + T_d) // (2 T_d)
(nature_beam.py:519-524: S_1 Links per T_d / Q intervals, apportioned per axis
as |v_a| / S_1). The floor sits where GRAIN.md puts it: on the flow, per
(direction, component), `by_clock(entry.clock_age, |V_d| x num_d, den)`
(nature_beam.py:2010) with `clock_age` the age before this interval's
self-creation (engine.py:417), the same age the columns read; then `push_form`
untouched on the sum (nature_beam.py:3031-3049). The pair is the unreduced
(Q = 64, T_d = 110) against section 1's heading pair (32, 55): identical
floors, since (2a) // (2b) = a // b (2000 random (age, V, w, s) checked). The
sign convention checked on the bar: receding on +x rows at v = 1/3 gives
111994 / 262144 = 0.427 = 1 - v / c with c = 32 / 55; approaching 412294 /
262144 = 1.573; transverse (0, 1, 0) exactly (262144, 262144); co-moving at c
(14, 262144), the grain (G x 32 / 55 = 2383.1 floored); outrunning at 0.75
(75776, 262144) = 0.289 = (v - c) / c. On the fan at v = 0.75 on x: (1, 1, 0)
reads 45056 / 524288 = 0.086 and (1, 3, 2) 0.653, the absolute value never
reached on those (v . c_d / |c_d|^2 < 1 there): the flux, not the per-axis
form, as decided.

**N2. LOCALITY-1 end-to-end: pass.** The weight's inputs (nature_beam.py:
1963-2012): `entry.frame_momentum` and `entry.frame_content` (the reader's own
record, snapshotted by `_frame_all`, engine.py:407-410), `world.width`, G and
Q (constants of the law), `flight.vectors[d]` and `flight.resolution[d]`
(table constants), `plan.t_arrival[k0:k1]` (the taken row's own
`store.direction` where it moved this interval, nature_beam.py:2277 and 2834:
the last hop, a table index, no source) and `plan.t_label[k0:k1]` (the row's
own label), `entry.clock_age`. No history, nothing at a Node, no global
estimator. Work per group: (directions present) x 3 products and floors,
storage a dict of at most the table's size: fixed for fixed K. A row that did
not step (arrival `NO_ARRIVAL` = 0, the vector (0, 0, 0)) gives numerator 0
and denominator 0 and is skipped at nature_beam.py:2002 before any division;
its label is zero anyway (checked: `[0, 2]` arrivals with a zero label give
[27, 0, 0]). `quantised_speed` is recomputed per group rather than once per
interval (the docs say "once per interval"): the same value, a host cost only.
**The snapshot:** `step()` runs `_frame_all` first (engine.py:349), then
`nature_beam` (the pushes), then the turns and `_move` last (engine.py:368);
so `frame_momentum` is the momentum after the previous interval's pushes and
hand-overs, the one the previous `_move` stepped by, read BEFORE this
interval's pushes, and every group of the interval reads it (test (g),
test_doppler.py:592-657: two groups at -27 each where the live momentum would
give 56 for the second). Stated: MIGRATION.md:39-42 ("at the start of the
interval ... one speed for every group"), engine.py:388-393, measured.py:
327-331. A body owing a count is snapshotted too (harmless; record 128 (1)'s
waiting rule is a later change).

**N3. Integer discipline.** Bounds: the numerator <= G (Q |v|^2 + T_d S_1):
2^19.4 on headings, 2^24.3 on the 292-direction tables, 2^28.7 on lensing's
296, 2^30.0 on bohr/r2's 2624 directions, 2^33.6 at the default P = 64 as
note 38 says, and 2^45.2 at the parser's maximum P = 4096 (world.py:2676): the
numerator alone always fits. `|V_d| x num_d` on the registered G2 world (the
per-direction release 65 of content 2^22 + 4096 at release 1 / 65536, one
heading): 2^31.5; today's columns on it 2^35.6 (against the pair's 2^87). The
gate set under the key, hypothetically: the largest flux product 2^42.4
(coupling/1b_m16, release 131072), the deuteron worlds 2^41.1, bohr/r2 2^36.0;
none near 2^62. R1: flux_bound_error names the body's number, its Node and the
direction index (nature_beam.py:1904-1912, tested (d)); R2: `bounded(...,
"weighted flow")` on the sum per component names the body and its Node
(nature_beam.py:2011). The two remainders are stated in note 38 (the speed's
`(G |p_a|) mod D_a` with its bias below 1 / G toward the weight 1; the flow's
`(|V_d| x num_d) mod (G Q |v|^2)` off the clock). Not checked: `G x |p_a|`
(S1) and the age product in `by_clock` (S4). The static budget's factor
(world.py:460-476, 2442): the ceiling of the strict bound 1 + T_d S_1 /
(Q |v|^2) (2.72 -> 3 on a heading, exactly 4 on (1, 1, 1)); it bounds
floor-ish terms that can each exceed |V_d| x num_d / den by one unit, which
the budget's "+ 1" per column absorbs only approximately: the budget is
declared "static and conservative" and R1 at the push is the guard, so a
note, not a defect. GRAIN.md's "4.75 on a heading" was section 1's pair; note
38's 2.72 is the flux form's, right.

**N4. Physics.** The rule reads the arrivals' flow at the relative speed in
the owner's frame (record 119: a body TAKES a message at the rate at which it
and the message meet): receding reads less, approaching more (N1), transverse
exactly 1 (the sum is 0, the division exact), co-moving 0 to the grain. The
absolute value at v > c: a body faster than the stream sweeps its rows from
behind at (v - c) per interval, (v - c) / c of the stream's rate; a count is
nonnegative, so |1 - v / c| is the take, and "the same as receding" would be
the negative count (c - v) / c, which is no count. The push keeps the flow's
sign (the rows' label still points from the source), so under gravity the
outrunning body is still pulled toward the source: right in the owner's
frame, and the owner took it (record 127, 130). Where it enters: the group's
flow of every FREE family, before the columns, for every column (gravity,
charge, a declared strong column alike: `push_form` sees only the weighted
`moment`, nature_beam.py:3031-3049) and for every rule that pushes (the
`read` test at 3066 only affects the record); a paid family's click is
unweighted (`free` false: GRAIN.md's scope, as in the first review's N5). A
fixed body is guarded out (weight 1 whatever it books). **The free body at
rest reads today's integers exactly:** with p_a = 0 on every axis, w_a = 0,
num_d = G Q |v|^2 = den, and `by_clock(age, |V_d| den, den) = ((age + 1) |V_d|
den) // den - (age |V_d| den) // den = (age + 1) |V_d| - age |V_d| = |V_d|`
for every age (checked at ages 0, 7, 123456); the sum over directions of the
per-direction label sums is `g_moment` (integers commute), so `push_form`
gets the same `moment` as without the key. "At rest" here is the grain's:
any body with |p_a| < D_a / G on every axis (test (f), the fan reader at rest
with rows of 1: 273, 459, 102 below 16384). A body whose momentum crosses
D_a / G on one axis reads there at w_a = 1 (the fan reader with rows of 64:
5821 against 5824 on the third read): the declared grain, stated.

**N5. The observable on the bar (counts -> label units): legitimate.** The
probe column [1, 2^20] on a body of content 2^20 (test_doppler.py:151-155)
makes E n / (D d) = 2^20 x 1 / (2^20 x 1) = 1, so the recorded push IS the
weighted flow in label units (64 per row of amount 1) with no second floor:
a cleaner observable of the same rule, not a rule change (12800 / 64 = 200
rows at rest, 6204 / 64 = 96.94 receding at 0.30, against the map's 96.9).
TEST_EXPECTATIONS carries no old pins: relative to main the section
(TEST_EXPECTATIONS.md:1463-1574) is entirely new; the first build's count pins
(97, 45, 303, 0, 57/58) appear only as FORM.md's map for comparison, and no
name of the first build (`relative_speed_bound`, `axis_pace`,
`FlightTable.pace`, `_doppler_load_checks`) survives outside MIGRATION.md:
49-52, which names them as removed.

**N6. Docs.** BEAM_LAW step 4 (BEAM_LAW.md:446-452) and note 38
(BEAM_LAW.md:2651-2787): consistent with the code (the pair, G, D_a, T_d, the
floor's place, R1/R2, the factor 2.72 / 4, the fixed body, the rest identity,
the scope: clock, size, threshold, meeting, emitter, paid clicks untouched;
the bar's and the fan's integers match the tests). ENGINE.md:396-410
consistent. MIGRATION.md:9-60 names every removed piece of the first build
(`_doppler_load_checks`, `relative_speed_bound`, `axis_pace`,
`FlightTable.pace`, the "only on an axis where the reader moves" rule, the
(N + T) x D budget) and says they never reached main; "Nothing deleted" is
right against main. English throughout; no HIGHLIGHTS edit (no diff); no
`Site`, `lattice` or `grid`; "board" twice (S2); the identity `doppler-v1`
under `hypotheses` (world.py:445, 1011-1012; run.py:114; test (e)). Note 38's
"the gate set's fifteen worlds replayed identical on 2026-09-20" is the
implementer's claim: I did not replay them; byte-identity without the key is
structural (the guard `world.doppler and free and not entry.fixed` at
nature_beam.py:3031; `frame_momentum` is read nowhere else; `step_axis`'s
divisor is the same expression through `step_divisor`), and test (e) parses
all fifteen with `doppler` false.

**N7. Tests.** 19 passed. Covered and right: (a) the fixed body and the free
body at rest byte-identical over 200 intervals; (b) the six bar lines and the
bar with rows of 64 (the first build's refusal gone); (c) the third law (both
fixed: the guard only, as in the first review); (d) the refusals, R1 naming
body and direction, the budget's factor and its refusal text; (e) the grain,
the pairs on the headings and the three fan directions against GRAIN.md's
numbers, the record, the gate set's parse; (f) the fan over three intervals
per direction, the three together in one group, the fan reader at rest with
rows of 1 (byte-identical) and of 64 (the grain crossed on y); (g) the set
body's two groups from one snapshot; (h) the registered star world under the
key. The first review's S5 gaps (a set body, two groups in one interval, a
fan reader with d_c > 1, the rest identity by a direct call) are closed
except a moving reader with a column denominator > 1 and a body moving on
two axes at once; both are covered by the form (one scalar per direction from
all three w_a; the columns untouched) and (f)'s fan reads use two nonzero
components of v with one w_a, so the sum's sign bookkeeping is exercised. A
two-axis momentum test would cost one line; not required for the merge.

**N8. Beyond this change, one line each.** The weight reads the frame's
content M for D_a while `_move` reads the live content after the interval's
clicks (engine.py:527 with `entry.content`): the speed the weight quantises
and the speed the step fires at differ by the clicks of the interval,
declared each on its own read; the frame's is the stated convention. The
second G2 run under the key (record 119 (6)) is the G2 session's, on the
signed drive and this form after B1; nothing here registers it.

## The eight questions, one line each

1. GRAIN.md section 2 exactly: numerator, denominator, s_a = sign(p_a), the
   absolute value, T_d the flight table's resolution (the velocity (Q / T_d)
   v), the floor on the flow per (direction, component) by `by_clock` at the
   reader's `clock_age`; the unreduced heading pair floors identically to
   section 1's; zero deviation.
2. Local end-to-end (N2): the reader's snapshot and record, the row's own
   direction and label, table constants, G and Q; fixed work and storage per
   group; one snapshot per interval read before the pushes, stated.
3. Every intermediate bounded and refused by name except `G x |p_a|` (S1,
   2^74 at the register's momentum) and `by_clock`'s age product (S4, the
   columns' convention, unstated); the two remainders stated; the star's
   products 2^31.5 and 2^35.6, the gate set's largest 2^42.4.
4. The sign, the transverse 1, the co-moving 0, the outrunning |c - v| / c
   are the owner's count (a reading from behind is a take, not a negative
   receding); the weight on every free family's flow before every column, a
   paid click unweighted; the free body at rest reads today's integers by
   the exact division, proved.
5. The bar's observable is now the weighted flow itself through an exact
   column (E n / D d = 1): legitimate, no rule change; no old pin survives.
6. `tests/data/g2_gravity_scalar.json` is byte-identical to the G2 branch's
   example (not on main yet): the copy rule fails at G2's merge unless named
   now (S3); the test (h) is necessary; the world is headings-only.
7. Docs consistent, English, no HIGHLIGHTS edit, no `Site`; "board" twice
   (S2); `doppler-v1` in `run.json`; MIGRATION names every removed piece.
8. NOT MERGEABLE AS IS (the conflict with main after PR #377, B1);
   MERGEABLE AFTER B1 (main's signed `step_axis` with `step_divisor`, the
   doppler and step-drive tests re-run) and S1, S2; S3 and S4 before or at
   G2's merge. The physics, the locality and the bounds of the form pass.

## Not checked

The gate set was not replayed and `tools/check.py` was not run; no G2 world
was run beyond test (h)'s 20 intervals; the inverse interval was not
considered (no measured events there); the mathematician's `grain_map.out`
was not re-derived beyond the pairs the tests pin; the branch after the
rebase of B1 does not exist yet, so its integers are expected, not shown.
