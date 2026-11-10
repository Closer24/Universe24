# metric_variant_v1 — Stage 0 (core engine) notes, B0-BUILD

All stamps are `date -u` at the moment of writing. Each acceptance test is pre-registered here BEFORE it is run;
results are appended below the pre-registration, never edited into it. Nothing under `universe24/`, `tests/`, `docs/`,
`examples/` or any existing file is touched; the package imports `universe24` read-only. No git.

## Design summary (written Tue Nov 10 08:45:24 UTC 2026, before any code was run)
- WHOLE SYSTEM = Rule3 + ONE divisor D = 6Q + ONE tensor T + the initial state.
- Every gear: `K = 2u`, `ell, r' = divmod(K + r, D)`, `a' = b`, `b' = ell - a`; u is read from the SAME previous
  complete snapshot. The tensor coefficients are coefficients of u (not of K), so K is even by construction.
- Tensor = unit-cell template: gear types (name, readout label `official`/`audit`, optional Yee link axis as metadata)
  and monomials `(target, integer coefficient, <= 3 factors)`, factor = `(gear, offset in {0, +-e_x, +-e_y, +-e_z},
  field in {a, b})`. Degree <= 3 = rank <= 4 on v = (1, b, a). A monomial with no factor is a constant.
- Locality (B3), enforced at construction: the target's node (offset 0) and every factor offset lie in {0, e} for ONE
  face direction e. Edge/diagonal/longer offsets and monomials touching three nodes raise.
- a-reads: the graph "gear g's a is read by gear t" must be acyclic (self-reads included); it gives the staged inverse
  order (stage 0 = gears whose input reads no a, ...). Cyclic a-reads raise at construction.
- Reference block: built from `universe24.core.coupling.Coupling` ports/weights in the SENDER form of
  `Engine.input_sums` (receiver `ports[d][g]` at x + e_d reads `Q*weights[d][g] * b(gear g at x)`), entries x Q.
- Engine: dense arrays (G, L^3) per field; vectorised numpy int64 with an exact Python-int overflow guard
  (bound on |K + r| from per-gear maxima, limit 2^62); if the guard trips the step runs on Python ints (object arrays).
- Clicks (passive readout, never fed back): OFFICIAL click iff `quotient = after.b + before.a != 0` AND the triple
  changed (exactly universe24's `classify`); kind = handedness of delta = (r' - r) mod D in (-D/2, D/2]:
  C0 if delta in {0, D/2}, C1 if 0 < delta < D/2, C2 if D/2 < delta < D (CLICK_TAXONOMY §1; = today's kind for D = 6).
  Gear label `official`/`audit` (OD1) is copied into the click rows only. A raw `ell != 0` stream (with the
  `changed` flag) is exposed separately and labelled NON-OFFICIAL.
- Mirror M(a, b, r) = (b, a, D - 1 - r) per gear.

## PRE-REGISTRATION of the Stage-0 acceptance tests (written Tue Nov 10 08:45:24 UTC 2026, BEFORE any run)
Pass criteria are EXACT (bit for bit) unless stated otherwise. Seeds are fixed in `tests/test_core.py`.

T0.1 REFERENCE IDENTITY. Tensor = `reference_block(Q=1)` (+++), D = 6, L = 5. Initial states (universe24 `State`):
  (i) three dense random states, every channel a, b uniform in [-50, 50], r uniform in 0..5; (ii) one dense state with
  |a|, |b| up to 2^80 (forces the Python-int path); (iii) two sparse states: vacuum (0,0,2) + 20 random non-vacuum
  cells; (iv) one sparse state on the non-default background (0,0,5). 25 updates each. PASS iff after EVERY update
  every (a, b, r) of every channel at every node equals `universe24.core.engine.Engine.advance`, AND the official
  click log (address, kind, quotient) equals `universe24.observation.clicks.clicks` row for row. Also reported (not a
  pass condition): the number of raw `ell != 0` rows dropped as unchanged; my staged inverse equals
  `Engine.rewind` on every update; a constructed state with a = b = 1 and six +1 inputs (ell = 2, unchanged) is dropped
  from the official log and present in the raw stream.

T0.2 Q-SCALING. Same initial states (i)-(iii), `reference_block(Q)` with Q = 7 and Q = 50 (entries x Q, D = 6Q,
  initial r x Q), 25 updates. PASS iff after every update a, b equal the Q = 1 run and r_Q = Q * r_1 for every channel,
  and the official click logs (address, kind, quotient) are identical to the Q = 1 logs.

T0.3 EXACT REWIND. Random translation-invariant B3-local tensors, rank <= 4 (degree <= 3), G = 6 gear types,
  Q = 10^6, symmetric Q-weighted linear part + small nonlinear terms + constants; family A b-only, family B with an
  acyclic a-read layer (a-reads of strictly earlier gears in a random order, linear and nonlinear); seeds 10..15,
  L = 4, 5, 6; random a, b in [-20, 20], r uniform in 0..D-1. 50 forward then 50 staged-inverse updates. PASS iff
  the final state equals the initial state bit for bit AND every inverse step equals the stored forward history.
  Non-triviality also required: >= 1 update with ell != 0, and nonlinear monomials evaluate non-zero somewhere.
  Extra cases: (a) big ints |a|, |b| ~ 2^70 with a degree-3 tensor, 6 forward + 6 back (Python-int path);
  (b) small Q = 1 with cubic terms that cross the int64 limit mid-run, 8 forward + 8 back (guard switch mid-run).

T0.4 MIRROR. Random b-only tensors as in T0.3 (seeds 20..24, L = 4, 5, 6), n = 30. PASS iff
  M F^30 M F^30 (s0) = s0 bit for bit for every seed, and F M F (s) = M (s) on every visited state.

T0.5 LOCALITY AUDIT. The builder must RAISE on: edge offset (1,1,0); diagonal offset (1,1,1); offset (2,0,0); factors
  at +e_x and +e_y (three nodes); factors at +e_x and -e_x (three nodes); more than 3 factors; unknown gear; field not
  in {a, b}; non-integer coefficient; a-read self-loop; a-read 2-cycle. It must ACCEPT: on-site monomials (all offsets
  0, degree 0..3), single-link monomials (offsets subset of {0, e} for each of the six e, degree 1..3, including all
  factors on the neighbour). PASS iff every case behaves as stated.

T0.6 VACUUM. Q = 7, L = 5: `reference_block(7)` + 32 new gears with a random B3-local tensor (degree 1..3, no
  constants) including back-coupling monomials into the reference gears.
  (a) Reference sector in its vacuum (0,0,2Q); new gears at (0,0,r0), r0 random in 0..D-1. PASS iff after each of 100
  updates the full state is unchanged, there are zero clicks (official and raw) from new gears, and the reference
  sector equals the universe24 run from the empty vacuum State (x Q).
  (b) (stronger, deviation form) every monomial targeting a new gear and every back-coupling monomial contains >= 1
  new-gear factor; the reference sector starts in a dense random state (a, b in [-20, 20]). PASS iff for 100 updates
  the new gears stay exactly (0,0,r0), they produce no click (raw or official), and the reference sector equals the
  universe24 Engine.advance run (r x Q) bit for bit.

T0.7 PERFORMANCE (report only, no pass threshold). L = 16, 48 reference gears (Q = 7) + 32 new gears, random rank-3
  tensor (degree <= 2) for the new gears incl. couplings to the reference; int64 path (must be confirmed: the guard
  never trips); `nice`, <= 2 threads. Report updates/s and gear-updates/s over >= 30 timed updates after a warm-up,
  and confirm exactness of the timed run by rewinding it to the initial state.

## RESULTS, first full run (written Tue Nov 10 08:55:06 UTC 2026; runs 08:52:50-08:54:58 UTC, `nice -n 10`, <= 2 threads)
Raw numbers: `results/T0.*.json` (each with its own `date -u` stamp). All runs exact-integer.

| test | verdict | numbers |
|---|---|---|
| T0.1 reference identity | PASS | 7 initial states x 25 updates, L = 5: 7 x 450,000 = 3,150,000 component comparisons with universe24 `Engine.advance`, 0 mismatches; official click logs equal to `universe24.observation.clicks` on 175/175 updates (939,043 click rows); staged inverse == `Engine.rewind` == previous state on 175/175 updates; the 2^80 state ran on the Python-int path (25 py-int steps, 150 int64 steps). Raw rows with ell != 0 but unchanged triple (dropped from the official log, as universe24 does): 1, 4, 2, 0, 414, 372, 792 per state. Constructed fixed point a = b = 1, six +1 inputs: state stays (1,1,2), ell = 2, absent from the official log and from universe24, present (changed = False) in the raw stream. |
| T0.1 extra | PASS | `reference_block` (sender form of `input_sums`) == receiver form of `update_node` (canonical tensors equal); census 288 link entries, 0 node entries. |
| T0.2 Q-scaling | PASS | Q = 7 and Q = 50, 6 states x 25 updates each: a, b equal, r_Q = Q*r_1, click logs (address, kind, quotient) equal: 0 mismatches in 12 runs. |
| T0.3 exact rewind | PASS | 12 runs (seeds 10..15 x families A b-only / B acyclic a-reads, L = 4, 5, 6, Q = 10^6, rank 4, 34-54 monomials, B: 4-6 inverse stages): 50 forward + 50 inverse returns the initial state bit for bit in 12/12; every inverse step equals the stored history (0 mismatches); ell != 0 in 18,197-61,583 gear-updates per run; nonlinear monomials non-zero (2,264-7,768 values); max |value| 49-57. Extra (a) |a|,|b| ~ 2^70, degree 3, a-reads: 6 + 6 exact on the Python-int path (values reach 43,290 bits; 0 int64 steps). Extra (b) Q = 1 cubic: 8 + 8 exact, bit length 2 -> 12,058; the guard switched from int64 to Python ints mid-run. |
| T0.4 mirror | PASS | 5 b-only tensors (seeds 20..24, L = 4, 5, 6): M F^30 M F^30 (s0) = s0 in 5/5; F M F (s) = M (s) on 155/155 visited states. |
| T0.5 locality | PASS | rejected: (1,1,0) edge, (1,1,1) diagonal, (2,0,0), three nodes (+ex,+ey), (+ex,-ex), degree-3 three-node, 4 factors, unknown gear, bad field, float and bool coefficients, a-read self-loop (on-site and on a link), a-read 2-cycle. Accepted: constant, on-site degree 1 and 3, single-link degree 1/2/3 in all six directions (incl. all factors on the neighbour), an a-read chain staged as ((p),(q),(s)). |
| T0.6a vacuum | PASS | Q = 7, L = 5, 48 + 32 gears, 467 monomials (degree 1-3, no constants, a-reads, back-coupling): 100 updates, 0 updates with any change, 0 clicks (official and raw) from new gears, reference sector == universe24 run from the empty vacuum (0 mismatches). |
| T0.6b deviation form | PASS | same size, 451 monomials, reference sector dense random (a, b in [-20, 20]): 100 updates, new gears stay exactly (0,0,r0) (0 deviations), 0 clicks (official and raw) from new gears, reference sector == universe24 `Engine.advance` x Q (0 mismatches; 582,892 official reference clicks). |
| T0.7 performance | REPORTED | L = 16, 48 (Q = 7) + 32 gears/node, 628 monomials, rank 3: 18.7 updates/s = 6.1e6 gear-updates/s (40 timed updates after 3 warm-up, 2 threads, nice 10); int64 path for all 43 updates (0 Python-int steps); rewinding the 40 timed updates returns the start state exactly. Note: the T0.7 random tensor was built so that values stay in int64 (symmetric Q-weighted new-new linear part, quadratic terms read reference b's and at most one earlier new gear); its new gears still grow, to max |value| 1.45e10 by update 43, so it is a throughput probe, not a stable model. |

Fixtures for the independent verifier: `tools/export_fixtures.py` -> `results/fixtures/*.json` (tensor, Q, initial and
final state, per-update state sha256 and official click rows; 6 systems incl. the reference at Q = 1 and Q = 7).

## Manager items of 08:56 (layer API, reciprocity tool, links-frozen hook, manifest) — PRE-REGISTRATION
(written Tue Nov 10 08:59:05 UTC 2026, BEFORE the code below exists or runs)
Also changed before the freeze, with T0.1-T0.7 to be re-run on the final code: the int64 segment sums use per-target
`ndarray.sum` instead of `np.add.reduceat` (speed only; same exact integers).

T0.8 RECIPROCITY CHECKER. `check_reciprocity(tensor)` groups the b-only monomials (degree >= 1, all factors b) by
  their potential monomial P = {target at 0} + factors (translation class) and requires u_t = s_t dPhi/db_t (s_t =
  documented gear field sign, default +1): every partner monomial of P present with coefficient s_g * n_g * phi_P.
  Monomials designated `designated_one_way: <justification>` are excluded; every other monomial of an inconsistent
  class is listed and the check FAILS. Expected: (a) the +++ reference block (Q = 1 and 7) PASSES; (b) the symmetric
  random linear part of tests/randgen PASSES; (c) a gradient of a random integer cubic+quartic potential PASSES;
  (d) the same with one partner deleted FAILS and lists exactly the orphaned monomials; (e) a one-way detector term
  (u_det = c b_m b_m) FAILS undesignated and PASSES designated; (f) the body-sign choices (-1,+1,+1) etc. of the
  reference coupling PASS (universe24 validates reciprocity for all 8); (g) field signs: u_1 = -dPhi/db_1 passes only
  with s_1 = -1 declared.
T0.9 COMPOSE / NAMESPACES. `compose(*blocks)` prefixes local gear names with the block namespace ("em.A_x"); qualified
  names ("ref.R00") cross layers; a dotted local name or an unknown qualified name raises; the composed reference
  (namespace "ref") gives the same dynamics (bit for bit, L = 4, 10 updates, random state) as `build(reference_block)`.
T0.10 LINKS-FROZEN HOOK. `observe.audit.frozen_equivalence(base, extra, ...)`: reference block + a test STUB link block
  (3 link gears per node, Yee links, coupling kappa through rank-3 monomials into the reference gears and back).
  kappa = 0: the reference sector equals the plain reference run bit for bit for 30 updates (L = 4, random reference
  state) and the link gears stay at their vacuum -> PASS expected. Control kappa = 1: a difference must be detected.

## RESULTS, final stage-0 run on the frozen code (written Tue Nov 10 09:05:42 UTC 2026; suite run 09:04:53-09:05:17 UTC, 14 tests, 23.8 s, OK)
Command: `OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_core research.metric_variant_v1.tests.test_layers -v`
- T0.1-T0.6 re-run on the final code: identical verdicts and identical numbers to the first run (T0.1: 0 mismatches in
  3,150,000 components, 939,043 official click rows equal to universe24, unchanged-row counts 1/4/2/0/414/372/792;
  T0.2 0 mismatches; T0.3 12/12 exact, 0 inverse mismatches, extras exact; T0.4 5/5; T0.5 all cases as registered;
  T0.6a/b 0 deviations, 582,892 reference clicks in T0.6b).
- Speed-only change (per-target ndarray.sum instead of np.add.reduceat) preserves exact state traces: all six fixture
  systems (tools/export_fixtures.py) give byte-identical per-update state sha256 lists before (08:54:58) and after
  (09:05:26) the change, e.g. ref_Q1_L4 final 9e89568b..., cubic_Q1_bigint final a2899adf..., ref7+32 final caba7dc6....
- T0.7 (report): L = 16, 80 gears/node, 628 monomials, rank 3: 34.7 updates/s = 1.14e7 gear-updates/s (40 timed
  updates, 2 threads, nice 10; first run before the change: 18.7 updates/s); int64 path 43/43 updates; rewind exact.
- T0.8 RECIPROCITY: PASS. (a) +++ reference Q = 1 and 7: reciprocal, 288 monomials checked; (f) all 8 body-sign
  choices reciprocal; (b) symmetric random linear parts (5 seeds) pass; (c) gradients of random cubic+quartic
  potentials (5 seeds, rank 4, 51-69 monomials) pass; (d) deleting one monomial that has a partner fails in 5/5 and
  lists exactly the surviving members of its class (1-3) plus the missing partner; (e) one-way detector
  u_det = 3 b_m^2 fails undesignated, passes designated (and round-trips through JSON); (g) u1 = -dPhi/db1 fails with
  default signs, passes with sign -1 declared.
  DEVIATION, recorded honestly: the first T0.8 run (09:03:55) FAILED at (d) because the randomly chosen victim was a
  self-partnered term (d/db of b^3: its potential monomial has a single distinct variable), whose deletion leaves an
  exact gradient, so the checker correctly accepted it. The test was corrected to pick a monomial that HAS a partner,
  as (d) was registered ("one partner deleted"), and a case (d') now asserts that deleting a self-term stays
  reciprocal. No checker code was changed for this.
- T0.9 COMPOSE: PASS. Namespaced names A.x, A.y, B.z; cross-layer reference "A.x" resolved; dotted local name,
  unknown qualified name, duplicate namespace raise; compose(build_reference(name="ref")) has the same
  dynamics_fingerprint as build(reference_block(1)) and 0 run mismatches over 10 updates.
- T0.10 LINKS FROZEN: PASS. Reference (Q = 7, L = 4, random state) + test-stub link block (3 Yee link gears, rank-3
  reciprocal hopping, kappa): kappa = 0 -> 0 base mismatches, 0 link-gear deviations over 30 updates (monomial count
  unchanged, 288); control kappa = 1 -> 637 base mismatches and 828 link deviations within 2 updates (detected).
  Both stubs pass the reciprocity checker. (The first T0.10 attempt ran the kappa = 1 control for 30 updates: a
  rank-3 coupling without a spring grows doubly exponentially, so it was stopped by hand at 09:03:48 and the control
  now runs 2 updates; the kappa = 0 run is unchanged.)

## STAGE 0.1 — PRE-REGISTRATION (written Tue Nov 10 09:09:00 UTC 2026, before the 0.1 code exists or runs)
Reasons: (1) B0-VERIFY X7 found a REAL BUG: np.abs(int64(-2^63)) = -2^63, so exact_array/_maxabs_rows/_fits under-
estimate a state entry equal to -2^63 (given by the user as an int64 array or a plain list), the step stays on int64
and wraps silently. Not reachable from the engine's own evolution (its int64 outputs stay below ~1.17*2^62), only from
user-given initial data. Fix: exact max-abs = max(int(max), -int(min)) everywhere; plain lists are read as Python-int
object arrays (never float-inferred). (2) Manager ruling 09:08 on X11: the storage rule stays binding; add the strict
physical-support rule as an OPT-IN flag (), default unchanged.
T0.11 INT64 EXTREMES. One gear, u = b(x + e_x) (and a cubic variant), D = 6: states containing b = -2^63, a = -2^63,
  b = 2^63 - 1, given as int64 arrays and as plain lists, and a plain list mixing 2^63 with negative values. PASS iff
  forward and inverse equal an exact pure-Python per-gear oracle written in the test (and the official clicks equal
  the oracle's), in every input form; the mixed list is accepted (no TypeError).
T0.12 STRICT SUPPORT (opt-in). Link gear Lx (Yee axis 0) and node gear n: u_Lx(x) = b_n(x - e_x) and the link-field
  stencil u_Ax(x) = b_Ax(x + e_y): default construction ACCEPTS both and support_violations() lists both;
  strict_support=True RAISES LocalityError for each; hopping through the link u_n(x) = b_Ux(x) b_n(x + e_x) (and its
  partner terms) is accepted in both modes; the reference block and every T0.3 random tensor (node gears only) are
  accepted in strict mode. compose(..., strict_support=True) and Tensor.from_dict(..., strict_support=True) pass the flag.
Regression: the full suite T0.1-T0.10 must pass unchanged on the 0.1 code, and the six fixtures must reproduce their
recorded per-update state hashes exactly.

## STAGE 0.1 — RESULTS (written Tue Nov 10 09:11:30 UTC 2026)
- T0.11 INT64 EXTREMES: PASS. 22 checks (2 tensors: linear and cubic x 4 states: b = -2^63, a = -2^63, b = 2^63 - 1,
  a list mixing 2^63 with negatives x the input forms that exist: plain lists, int64 arrays, object arrays): forward,
  staged inverse and official clicks equal the pure-Python oracle in 22/22; the mixed list is accepted.
  Sensitivity: the same test with the stage-0.0 max-abs functions monkeypatched back in (scratchpad script
  t11_on_old_guard.py) FAILS at linear/b=-2^63/plain_lists, i.e. it reproduces B0-VERIFY's X7 bug; with the fix it
  passes.
- T0.12 STRICT SUPPORT (opt-in): PASS. X11 probe u_Lx(x) = b_n(x - e_x) and the link-field stencil u_Ax(x) = b_Ax(x+e_y):
  default ACCEPTED and reported by support_violations() (1 each); strict_support=True REJECTED (LocalityError), also
  through from_dict and compose; hopping through the link (3 monomials) ACCEPTED in strict mode; reference block
  (Q = 1, 7) and the twelve T0.3 tensors ACCEPTED in strict mode.
- Regression on the 0.1 code: 16 tests OK in 23.1 s (09:10:42-09:11:05 UTC): T0.1-T0.10 identical verdicts and
  numbers (T0.1: 0 mismatches, 939,043 click rows, unchanged rows 1/4/2/0/414/372/792); T0.7 42.3 updates/s, int64
  43/43, rewind exact. The six fixtures reproduce their stage-0.0 per-update state sha256 lists exactly (6/6
  identical, 82 hashes), so the fix changed no trace of the engine's own evolution.

## STAGE 0.2 — generic reversor building blocks — PRE-REGISTRATION (written Tue Nov 10 09:16:44 UTC 2026, before the 0.2 code exists)
Request (manager 09:14): core/reversors.py with (a) per-gear maps M = (b, a, D-1-r), M' = (b, a, R'(r)) with
R'(r) = D-2-r (r even) / D-r (r odd), J = (-a, -b, D-1-r), JR := J o M' = (-b, -a, r xor 1), plus a per-gear choice
given as data (also provided, documented: JM := J o M = (-b, -a, r), the "JR" of CLICK_TAXONOMY, and the
parity-preserving negation Jp = (-a, -b, R'(r)), the J_D of CLICK_TAXONOMY); (b) linear maps on a gear group at every
node (signed permutation, or integer matrix with an explicit remainder rule), exact; (c) spatial maps: identity,
inversion x -> S - x about a node (S = 2 x0) or a cube centre (S = 2 x0 + (1,1,1)); link gears of axis k re-based
x -> S - x - e_k; (d) reversor_check(X, F, states, n, central) for X F^n X F^n = id or = a declared central map Z;
(e) is_fixed(X, state). Composition X @ Y = X o Y.
T0.13 (all exact, bit for bit):
 (1) involutions: M, M', J, JR, JM, Jp, random per-gear choices, node and cube-centre inversions (L = 4, 5, with link
     gears), an involutive signed permutation: X X = id on random states, Q = 1, 7, 50; a unimodular integer matrix
     map followed by its inverse matrix = id; a K with K^2 = -1 gives K K = J on its block.
 (2) M' with D = 6 equals universe24 observation.diagnostics.time_reverse on random reference states (L = 5).
 (3) reference sector (Q = 1 and 7, L = 4, random states, n = 10): M, M', JR and JM are reversors (X F^n X F^n = id);
     the mirrored history's official clicks are the original's reversed in time with the same addresses: kinds kept
     and quotients kept for M and M'; kinds C1 <-> C2 swapped and quotients negated for JR and JM.
 (4) spatial inversion of the reference board: the channel relabelings sigma with sigma(ports[d][h]) =
     ports[d^1][sigma(h)] and equal weights are found by search from universe24's Coupling (prediction from a
     search run at 09:14: 8 for +++; 0 for (1,1,-1)); for each sigma, inversion about a node (L = 4, 5) and about a
     cube centre (L = 4, 5) composed with sigma COMMUTES with F on random states (F X s = X F s); control: plain
     inversion (sigma = identity) does not commute.
 (5) link re-basing: a random inversion-symmetrised gradient tensor with node and link gears commutes with inversion
     (node and cube centre, L = 4, 5); control: the same map without link re-basing does not commute.
 (6) central detection: for a complex-linear tensor on a gear pair (X, Y) and K(X, Y) = (-Y, X) (sign rows use
     r -> D-1-r), reversor_check(K o M) reports the central element J (global sign on the pair) for every state and
     no failure; M alone reports identity; for a real-linear tensor that is not complex-linear K o M reports failures.
 (7) is_fixed: the vacuum (0, 0, r0) is fixed by inversions and permutations; M fixes no generic vacuum unless
     r0 = D-1-r0 is impossible (D even) -> not fixed; reported.
Regression: T0.1-T0.12 must still pass; fixtures must reproduce their per-update hashes.
Clarification of T0.13 (7) (written Tue Nov 10 09:17:45 UTC 2026, still before any T0.13 run): is_fixed must be TRUE for the vacuum
(0, 0, r0) under node and cube-centre inversions and under a gear permutation among gears with equal r0, and FALSE
under M (r0 -> D-1-r0 differs from r0 because D is even).

## STAGE 0.2 — RESULTS (written Tue Nov 10 09:20:32 UTC 2026; T0.13 first run 09:19:06-09:19:07 UTC, 7/7 OK on the first run)
- (1) involutions: 67 checks (Q = 1, 7, 50; L = 4, 5; M, M', J, JR, JM, Jp, random per-gear choices, node / cube-centre
  / box-centre inversions with link gears, an involutive signed permutation): X X = id 67/67; unimodular [[2,1],[1,1]]
  then its inverse = id and the values equal the matrix product; K = [[0,-1],[1,0]]: K K = J on the block.
- (2) M' (D = 6) == universe24 observation.diagnostics.time_reverse on 3 random reference states (L = 5).
- (3) reference sector, Q = 1 and 7, 2 states each, n = 10: M, M', JR, JM are reversors (16/16 identity); the mirrored
  histories' official clicks (30,186-30,190 per run) are the originals reversed in time at the same addresses: kinds
  and quotients kept for M, M'; C1 <-> C2 swapped and quotients negated for JR, JM.
- (4) channel relabelings sigma making inversion a symmetry, by search over universe24's ports: 8 for (1,1,1), 0 for
  (1,1,-1) (both as predicted), 8 for (1,-1,-1) and (-1,-1,-1) (reported); for +++ all 8 sigma x {node, cube-centre}
  inversion x L = 4, 5: F X s == X F s in 32/32; plain inversion does not commute (control).
- (5) inversion-symmetrised random gradient tensor with node gears and Yee link gears (49 monomials, physically
  link-local entries): commutes with node and cube-centre inversions at L = 4, 5 (4/4); the control without link
  re-basing does not commute (2/2 detected). Recorded design fact: a storage-legal entry whose physical support exceeds
  one link does not stay storage-legal under inversion (link gears are re-based by -e_k).
- (6) complex-linear tensor on (X, Y), K(X, Y) = (-Y, X): reversor_check(K o M) = central J in 4/4, 0 failures;
  M alone identity 4/4; K o M without the declared central element: 4/4 failures; real-linear control: 4/4 failures.
- (7) is_fixed on the vacuum (0, 0, 2Q): node inversion True, cube-centre inversion True, a 48-cycle gear permutation
  True, M False (as clarified at 09:17:45).
- Regression on the 0.2 code: 23 tests OK in 27.0 s (09:19:38-09:20:05 UTC); T0.1 0 mismatches / 939,043 clicks;
  T0.7 36.6 updates/s int64; T0.11 22/22; fixtures 6/6 reproduce their per-update hashes (82 hashes).

## STAGE 0.2 addendum (architect review items R1, R2; manager 09:21) — PRE-REGISTRATION (written Tue Nov 10 09:21:34 UTC 2026, before code)
Note: a 0.2 section was frozen at 09:20:32 (reversors only, not yet announced); it is kept in the manifest as "0.2a"
and superseded by the final 0.2 = reversors + R1 + R2.
R1 ONE Q: Block.Q records the Q a block was built with (None = Q-independent block); compose raises if two blocks
  declare different Q and the Tensor records the common Q; Engine(tensor, Q) raises if tensor.Q is declared and differs;
  prepare.vacuum_state raises if the tensor or any block declares a different Q. build_reference / reference_block /
  the test generators that take Q record it.
R2 FIELD SIGNS: GearType(sign = -1) requires a non-empty justification (GearType.sign_why), else ValueError at
  construction (and in from_dict); check_reciprocity's report lists every gear with s = -1 and its justification.
T0.14: (a) a Q = 7 reference block under Engine(Q = 5) raises; compose(Q=7 block, Q=5 block) raises;
  vacuum_state(tensor(Q=7), Q=5, ...) raises; matching Q works; a Q-independent block (Q=None) composes with a Q=7
  block and the tensor records Q = 7; a tensor without a declared Q runs under any Q (back-compatible).
  (b) GearType("p", sign=-1) without justification raises (also via Tensor dict input / from_dict); with a
  justification the reciprocity report lists exactly the s = -1 gears with their justifications; sign +1 gears are
  not listed. Regression: the whole suite T0.1-T0.13 passes; fixtures reproduce their per-update hashes.
T0.15 (rho_L0, R-M2 theorem; manager 09:23) — PRE-REGISTRATION (written Tue Nov 10 09:23:10 UTC 2026, before code):
  rho_L0(r) = 4Q + 2 (r mod 2Q) - r as a named remainder/per-gear map "rhoL0" = (b, a, rho_L0(r)); validator
  Tensor/compose(..., q_lattice=<gear-name patterns>) raising if a term targeting a listed gear has u-coefficient
  not = 0 mod Q (also Tensor.q_lattice_violations(patterns)). Predictions: (a) rho_L0 is an involution on 0..6Q-1 and
  equals Q * universe24 time_reverse(r_ref) on r = Q r_ref for all r_ref in 0..5 (Q = 1, 3, 7); (b) for Q = 1, 3, 7:
  reference block (Q-scaled) + a new b-only layer (node gears, couplings both ways, back-coupling coefficients x Q):
  X = rhoL0 on L0 gears and Mp (R') on new gears gives X F^n X F^n = id (n = 12, random states, also with L0
  remainders off the Q-lattice) and X fixes the joint vacuum (L0 at (0,0,2Q), new at (0,0,3Q-1)); L0 remainders that
  start on the Q-lattice stay on it for every update; (c) controls: Mp on L0 does not fix the vacuum for Q = 3, 7;
  a back-coupling coefficient not = 0 mod Q is flagged by the validator and breaks the rho_L0 reversor (detected).

## STAGE 0.2 (final) — RESULTS for R1, R2, rho_L0 (written Tue Nov 10 09:25:17 UTC 2026; first runs 09:23:57-09:23:58 UTC, 4/4 OK)
- T0.14a ONE Q: PASS. A Q = 7 block under Engine(Q = 5) raises; compose(Q = 7 block, Q = 5 block) raises;
  vacuum_state with a mismatched tensor or block Q raises; matching Q runs; a Q-independent block (Q = None) composes
  with a Q = 7 block and the tensor records Q = 7 (also after to_dict/from_dict); an undeclared tensor runs under any Q.
- T0.14b FIELD SIGNS: PASS. sign = -1 without a justification raises (GearType, dict input, from_dict); with
  justifications the reciprocity report lists exactly [("a1", ...), ("a3", ...)]; the reference block lists none.
- T0.15a rho_L0: PASS. Involution of 0..6Q-1 and equal to Q x universe24 time_reverse on all six Q-lattice remainders
  for Q = 1, 3, 7; fixes 2Q; for comparison R'(2Q) = 2, 10, 26 for Q = 1, 3, 7 (i.e. R' fixes 2Q only for Q = 1).
- T0.15b joint mirror: PASS. Q = 1, 3, 7, L = 4, reference + 4 new node gears (324-326 monomials, couplings both ways,
  back-coupling coefficients x Q; validator q_lattice=("ref.*",) passes): X = rhoL0 on L0 and Mp on the new layer:
  X F^12 X F^12 = id in 3/3 states per Q (including one with L0 remainders off the Q-lattice); X fixes the joint vacuum
  (L0 (0,0,2Q), new (0,0,3Q-1)); L0 remainders starting on the Q-lattice stay on it for all 12 updates. Controls:
  Mp on L0 fixes the vacuum only for Q = 1 (not for 3, 7); back-coupling coefficients not = 0 mod Q (Q = 3, 7) are
  rejected by the validator and break the rho_L0 reversor (3/3 failures each).
- Regression on the final 0.2 code: 27 tests OK in 25.7 s (09:24:21-09:24:47 UTC): T0.1 0 mismatches / 939,043 clicks,
  T0.7 51.7 updates/s int64, all T0.2-T0.13 as before; the six fixtures reproduce their per-update state hashes
  (6/6, 82 hashes; their tensor JSON now carries "Q" and "sign_why", the dynamics are unchanged).
