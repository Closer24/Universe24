# metric_variant_v1 — Stage 1, CHOICE-CLICK layer (quantum measurement gears), builder B1-CHOICE

All stamps are `date -u` at the moment of writing. Append-only: results are appended below the pre-registration,
never edited into it. Core (stage 0.2) is used read-only; `universe24/` and other builders' files are untouched. No git.
Sources ported (read-only): Study 5 (s5/AGREE_M.md, AGREE_P.md, P2R_INTERIM.md, M2_work/*.py, P_*.py).
Design: SYSTEM_DESIGN_v5 §1b, §7, §8 (S5-O1…O4).

## Design summary (written Tue Nov 10 09:33:04 UTC 2026, BEFORE any code of this layer exists or runs)

Every gear runs Rule3 with K = 2u (u = integer polynomial of the previous snapshot), ONE divisor D = 6Q per composed
experiment (Block.Q set by every builder; compose asserts one Q). Gears of other designs (divisor 6, 8A², 30 …) enter
by the Q-scaling theorem: a gear designed with divisor D_g | 6Q runs with input ×(6Q/D_g) and remainder ×(6Q/D_g).

ENSEMBLES ON THE LATTICE (declared hidden data, exhaustive). Every node holds every gear type. A construction whose
terms are all on-site is an independent copy at every node; a construction along x (fibres) is an independent copy on
every (y, z) line. Each copy carries its own declared hidden data (token remainder λ, phases) written by prepare/.
Counting is exhaustive over the declared hidden data unless stated (M2-2 N ≥ 3: P2R's seed-1 sample, declared).

GEARS / BUILDERS (layers/choice.py; every builder returns a Block with Q):
- `build_clock_ring` — C0 carrier: n = 3 gears, u = 3Q·b (period 6) or n = 2 gears, u = 0 (period 4); remainder 0.
  Reciprocal (self terms).
- `build_fibre` — C0 carrier: exact d'Alembert fibre along an axis, u = 3Q·(b(x−e) + b(x+e)); reciprocal.
- `build_born_router` — the rank-3 |ψ|² DETECTOR pair reading two rings: u_d± = ±κ·Σ_j (b_X1j ± b_X2j)²
  ("opposite" form: equal remainders, the PAIRED LINK CLOCK) or u_d± = +κ·Σ_j(…)² ("mirror" form: tokens λ, D−1−λ).
  One-way OBSERVER: DESIGNATED `observer detector: records without back-action (Study 5 D3)`.
- `build_common_drive` — a DC source gear S (u = 6Q·b; seed (c, c) stays) feeding both detectors of a pair equally
  (u_d± += w·b_S): the board-made token (equal remainders born from the vacuum). Designated one-way (drive).
- `build_sequential_router` — ONE link gear with a fixed divisor reading an intensity stream that arrives along a
  C0 fibre: visits k = 1..n at successive updates; exit k = first overflow at visit k (arcs of one remainder circle).
  Parallel control `build_parallel_router`: n exit gears reading n simultaneous intensities with one shared token.
- `build_f7` — the light-cone choice: Alice's photon flash (3 ring components + 1 marker, C0 fibres), Alice's setting
  ring C, Alice's photon-gated rank-3 router dA±, Alice's front clock F (3 gears) set up Rule3-natively by P2R's
  two-update kick k0 = q·(b_C − a_C), k1 = −q·a_C, here GATED by the photon marker passing the neighbour node
  (rank 4, b·b·b and a·a·a monomials on one face link; DESIGNATED one-way imprint), the front fibres P (C0) driven
  one-way by F through an exact two-node source u_P(x) += 3Q(b_F(x) − a_F(x+e)) (emits an exact right-moving copy of F;
  DESIGNATED), Bob's setting ring B and Bob's setting-gated rank-3 Born pair dB± (u = ±κΣ b_B(b_B ± b_P); designated
  observer). Designed bit-gate reader = a read-only observer function (observe/choice.py), not a gear.
- `build_which_path_W` — Study-5 M2-2 nonlinear which-path gears (S5-P2R): W reads arm-1 gear j%3 (u_W = 3·(Q/Q_W)…),
  kicks it by one unit. Under ONE divisor its 3:3 multi-divisor symmetry becomes 3:(3Q_W) → not a gradient →
  DESIGNATED (kept for exact reproduction).
- `build_gated_pair` — exit detectors read once, at the arrival of a gate flash (rank 4: g·|ψ±|²), mirror tokens;
  designated observer. Used for M2-2's one-shot readout at τ (P2R's definition).
- `build_dec_toy` — S5-M2's D12b toy as gears (P_dec): period-4 arms, W1/W2 (u = 6Σ X²), exit pair with the rank-4
  gated readout of the arm rotated by c × 90° (designated).
- `build_backaction_router` — (ii) BACK-ACTING reciprocal detectors from ONE potential:
  Φ = κ b_d+ |X1+X2|² + κ b_d− |X1−X2|² − (g/2)(b_d+² |X1+X2|² + b_d−² |X1−X2|²), field sign s(d−) = −1;
  g = 0: rank 3; g = 2κ: rank 4, sign-definite (the arm modulation 2(κ b − (g/2) b²)ψ has one sign for every integer b).
  Passes the reciprocity checker with NO designation.

Q per experiment (ODD where free): router/token D = 48A² (Q = 8A², κ = 3; matched quantization forces even Q);
sequential router D_I ∈ {9, 15} with ODD Q = 3, 5 (κ = 1) and D_I ∈ {8, 12} (Q = 8, 4) for P2R's sizes; F7 Q = 4
(D = 24, κ = 3, A = 1); all-or-nothing Q = 5 (odd; D_W = 30 native); M2-2 Q = 40 (D = 240 = lcm of 6, 30, 16·15);
D12b toy Q = 4A² (D = 24A²); back-action router Q = 8.

## PRE-REGISTRATION of the acceptance tests (written Tue Nov 10 09:33:04 UTC 2026, BEFORE any run)
Exact integers everywhere; probabilities are exact Fractions (Visibilities of M2-2 are floats, compared at 3 decimals,
as P2R reported them). Every run is rewound with the staged inverse and must return the initial state bit for bit.
Ring phase convention: ring of phase φ at time t has b_j = p[(2j + φ + t) mod 6], p = (A, A, 0, −A, −A, 0).

TC.1 C0 CARRIERS. (a) ring (period 6) at Q = 1, 3, 8, A = 1, 2, 5: exact period 6, remainder stays 0, every official
  click is C0, Σ_j b_j² = 2A² at every update; period-4 pair (u = 0): period 4. (b) fibre along x, Q = 1, 3: an
  exact right-moving profile g(x − t) (random integers, length 7) is transported exactly for 2L updates (wraps),
  remainder 0, all clicks C0. Both blocks pass check_reciprocity with no designation. Rewind exact.
TC.2 BORN ROUTER (M2-1), both forms, A = 1, 2, 3, 10 (D = 48A²), s = 0..5, token over ALL D remainders (laid on
  nodes): P(d+) = 1, 3/4, 1/4, 0, 1/4, 3/4 EXACTLY; P(both) = P(none) = 0. I± static (= (8,6,2,0,2,6)A²,
  (0,2,6,8,6,2)A²) over 12 updates. Opposite form (paired link clock): r+ = r− at every update and exactly one click
  per update for 12 updates (continuous exposure). Mirror check (A = 1, 2): M F^7 M F^7 = id and the mirrored official
  log of the detectors = the reversed forward log with the SAME kinds. Rewind exact.
TC.3 GRANGIER α. A = 1, 2: independent tokens (all D² pairs (λ+, λ−)): α = P(both)/(P+·P−) = 1 EXACTLY for s = 1, 2,
  4, 5; shared token (both forms): P(both) = 0, α = 0.
TC.4 MISMATCH S ≠ D. A = 1, D = 48, κ ∈ {1, 2, 3, 4} (S = 16κ), opposite form, every s with max(K+, K−) ≤ D:
  P(both) = max(0, S − D)/D and P(none) = max(0, D − S)/D EXACTLY on every row; P(+ | exactly one) = I+/(I+ + I−)
  iff S ≤ D (reported for S > D).
TC.5 BOARD-MADE TOKEN (paired link clock born from the vacuum). (a) common drive, light off: both detectors at the
  vacuum (0, 0, 0), DC seed S = (1, 1) with w = 5 (K = 10 per update), D = 48: r+ = r− at every update for 48 updates
  and the visited remainders over birth times = the 24 even residues (the conserved parity class), each once.
  (b) unstaged exposure: detectors born at the vacuum with equal remainder r0, rings exposed from t = 0 (A = 1, s =
  0..5, r0 over all 48): r+ = r− at every update for 2D updates, exactly one click per update, and over ANY D
  consecutive updates N+ = K+ = 6·I+ exactly (sigma-delta Born: P(+) = I+/8 over readout times). Rewind exact.
TC.6 SEQUENTIAL n-EXIT ROUTER. n = 3, 4; D_I ∈ {8, 9, 12, 15} (Q = 8, 3, 4, 5); ALL compositions (I1..In ≥ 0,
  Σ = D_I: n = 3: 45, 55, 91, 136; n = 4: 165, 220, 455, 816), token over ALL 6Q remainders: P(exit k) = I_k/D_I
  EXACTLY for every composition, exactly one overflow per (composition, token) over the n visits; rewind exact.
  PARALLEL CONTROL (same intensities, read in ONE update, one shared token: exit 1 input −κI1, exits 2..n input +κI_k)
  must FAIL (non-exclusive or non-Born) on at least one composition for n = 3 and for n = 4 (also with the best fixed
  per-exit offset searched exhaustively over the remainder circle for each composition, n = 3, D_I = 9).
TC.7 F7 LIGHT-CONE CHOICE. Q = 4 (D = 24), A = 1, d = 5 (Bob at x_A + 5), Alice's photon at x_A at t_A = 1.
  EXHAUSTIVE over φ ∈ Z6, λ_A, λ_B ∈ 0..23, all 36 setting pairs (a, b).
  (a) TIMELIKE (Bob reads snapshot t_B ≥ t_A + 3 + d = 9): E(a, b) = cos(60°(a − b)) EXACTLY (1, 1/2, −1/2, −1, −1/2,
  1/2); max S over all quadruples = 5/2; Alice's and Bob's marginals 0 for every (a, b) (no-signalling).
  (b) SPACELIKE in the taxicab cone (Bob's update reads snapshot t_B ≤ t_A + d = 6, so no path |x|₁ ≤ t from Alice's
  click (update t_A → t_A+1) reaches it): E = 0 for every (a, b), max |S| = 0 ≤ 2. t_B = 7, 8 (inside the cone, front
  not yet arrived because of the two-update set-up): E = 0 as well.
  (c) Bob's wait = 8 updates from t_A (1 click + 1 + 1 set-up/emission + 5 transit), reported in Bob's own clock ticks
  (sign cycles of his gear's click sizes).
  (d) bit gate (designed observer, decodes (o_A, a) from the front at Bob within a pair 60° apart): S = 4.
  (e) Alice: no detector click before t_A, exactly one click at t_A (every φ, λ_A, a); the front fibres are identically
  0 before Alice's click and all C0; every run rewinds exactly.
TC.8 ALL-OR-NOTHING on exact light (Q = 5): rings (u = 15b) + ONE nonlinear W (D_W = 30 native, u_W = 3 b_X1,0,
  kick 15 b_W), s = 0..5, r_W = 0..29, τ = 6: expected 72/180 configurations with a W click (P2R); every silent one
  leaves both arms BIT-IDENTICAL to the free clocks; every clicking one changes them by ≥ 2 units (Σ|Δa| + |Δb|).
TC.9 DECOHERENCE M2-2 with P2R's definitions (Q = 40): A = 1, Q_W = 5, τ = 6, W_j on arm-1 gear j mod 3, arm 2
  lagged by s; '+' = d+ with ℓ = 1 and d− without ℓ = 1, mirror token λ ∈ 0..7 (×30); V = 2|c1|/c0 over s.
  Expected V_ens = 0.808 / 0.833 / 0.650 / 0.262 for N = 1 / 2 / 3 / 6 (N = 1, 2 exhaustive over r_W; N = 3, 6 P2R's
  numpy default_rng(1) sample of 2000 configurations); N = 1: V_single = 0.915 = V_eraser. Extra (reported): N = 3
  exhaustive (27,000 configurations).
TC.10 QM-DEVIATION (D12b toy, P_dec), A = 1, 2, 3 (Q = 4A²): kick c = 1 (90° on period-4 arms):
  P(+|s) = 1/2 for s = 0..3; P(+|s, W1 record) = 1, 1, 1, 0; P(+|s, W2) = 0, 0, 0, 1; I(s; exit) = 0, I(s; exit,
  record) = 0.8113 bits; c = 0: P(+|s) = 1, 1/2, 0, 1/2; c = 2: 0, 1/2, 1, 1/2. Exactly one W click (update 1) and one
  exit click (update 2) per (s, λ), no exit click at update 1; rewind exact; M F² M F² = id.
TC.11 BACK-ACTING RECIPROCAL DETECTORS (ii), opposite form, A = 1, D = 48, κ = 3, g ∈ {0 (rank 3), 6 (rank 4,
  sign-definite)}; s = 0..5, λ = 0..47, 24 updates. Expected: check_reciprocity PASSES with NO designation; the first
  update is Born exactly (back-action enters after the click); rewind exact. OPEN, reported as found: exclusivity at
  later updates (counts of exactly-one / both / none), r+ = r−, max|b| of the arms (stability). Study 5 (D3) predicts
  broken exclusivity for rank 3.
TC.12 RECIPROCITY CENSUS: every experiment tensor passes check_reciprocity (all undesignated b-only terms are
  gradients); every one-way term carries a justification; the designated list is printed per experiment.

## AMENDMENTS (written Tue Nov 10 09:47:29 UTC 2026, BEFORE the acceptance suite tests/test_choice.py is run)
Development runs of the harness (scratchpad drivers, 09:38-09:47) found and fixed two HARNESS bugs (no layer/gear
change); recorded honestly:
1. TC.6 first draft placed tokens on nodes that the stream profile initially occupies (x = L-n..L-1), so those link
   gears read part of the stream at t = 0 (49/55 compositions "non-Born"). Fix: tokens on x = 0..D-1 only, L >= D+n+1
   (the profile starts outside the token nodes). Same fix for the parallel control (L >= D+2).
2. TC.6 control: my first "best offset" search chose the offset PER composition, which uses the intensities
   themselves (non-local, S5-P's c2 = I3) and therefore always succeeds. The pre-registered control is ONE fixed
   offset for all compositions (a local rule); both numbers are now reported, the assertion is on the fixed offset.
3. TC.11 reports max|b| of the arms as a BIT LENGTH (the reciprocal back-action blows up to > 4300 digits, beyond
   Python's int->str limit in JSON); 12 updates instead of 24 (pre-registered 24; the blow-up makes later updates
   meaningless and slow).
4. Manager's binding stage-1 conditions (09:4x) added to TC.12: the declared mirror maps (layers/choice.py MIRROR):
   M' F^8 M' F^8 = id on the router (Q = 8) and all-or-nothing (Q = 5) initial data; the M'-fixed remainders exist
   only for ODD Q ([8, 9] for Q = 3, [14, 15] for Q = 5, none for Q = 4, 8); the odd-Q joint vacuum (0, 0, 3Q-1) is
   M'-fixed and stationary; F7 (a-read gears) has NO per-gear mirror (expected M' failure, declared OPEN).
Development runs already seen (not the acceptance record): F7 full (09:45-09:46), M2-2 N = 1, 2, 3, 6 (09:45),
router/token/mismatch/Grangier/all-or-nothing/D12b/back-action (09:38-09:44); their numbers agree with the
pre-registration except TC.11 (OPEN item, see results). The acceptance record is the unittest run below.

## RESULTS of the acceptance suite (written Tue Nov 10 09:50:10 UTC 2026; run 09:47:42-09:49:56 UTC, 12 tests, OK, 134.4 s)
Command: `OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_choice -v`
Raw numbers: `results/choice/TC.*.json` (each with `date -u` start/finish stamps). Exact integers, exact Fractions.

| test | verdict | numbers |
|---|---|---|
| TC.1 C0 carriers | PASS | rings Q = 1, 3, 8 x A = 1, 2, 5: exact period 6, r = 0 throughout, every official click C0, sum b^2 = 2A^2 every update, rewind exact; period-4 pairs exact; fibre Q = 1, 3, L = 8: random right-moving profiles transported exactly for 2L updates (wraps), r = 0, clicks C0, rewind exact; all reciprocal, 0 designations |
| TC.2 Born router | PASS | A = 1, 2, 3, 10 (D = 48, 192, 432, 4800), both forms, every token: P(d+) = 1, 3/4, 1/4, 0, 1/4, 3/4; both = none = 0; I+ = (8,6,2,0,2,6)A^2 static for 12 updates; exactly one click per update for 12 updates; opposite form r+ = r- at every update; M F^7 M F^7 = id and mirrored detector log = reversed log with the same quotients and kinds (A = 1, 2); kinds: opposite form (C2, C2) for I+ > D/2, (C1, C1) for I+ < D/2, C0 at certainty; mirror form (C2, C1)/(C1, C2) (S5-P's PR-6 finding reproduced) |
| TC.3 Grangier | PASS | independent tokens (all D^2 pairs, A = 1, 2, both forms): alpha = 1 exactly for s = 1, 2, 4, 5 (P(both) = P(none) = 3/16 at A = 1); shared token: P(both) = 0, alpha = 0 |
| TC.4 mismatch | PASS | kappa = 1..4 (S = 16, 32, 48, 64), every row with K+-, <= D: P(both) = max(0, S-D)/D, P(none) = max(0, D-S)/D exactly; P(+ | one) = I+/(I+ + I-) for S <= D (e.g. kappa = 4, s = 1: both 1/3, P(+|one) = 1/2 != 3/4 -> not Born for S > D) |
| TC.5 board-made token | PASS | (a) DC drive (w = 5, K = 10/update), light off, born at the vacuum: r+ = r- every update; the 24 birth times visit the 24 even residues once each; the two detectors stay identical; (b) unstaged: every r0 in 0..47 x s: r+ = r- at every update for 96 updates, exactly one click EVERY update, and over ANY 48 consecutive updates N+ = 6 I+ exactly -> P(+) = 1, 3/4, 1/4, 0, 1/4, 3/4 over readout times |
| TC.6 sequential n-exit router | PASS | D_I = 8 (Q 8), 9 (Q 3, odd), 12 (Q 4), 15 (Q 5, odd); n = 3: 45/55/91/136 compositions, n = 4: 165/220/455/816; every token: exactly one overflow, P(exit k) = I_k/D_I exactly for EVERY composition (0 failures); rewind exact. PARALLEL control (D_I = 9): FAILS as required: n = 3: 36/55 compositions (280 non-exclusive token cases), the best ONE fixed offset still 36/55; n = 4: 192/220 (1770 cases). A per-composition offset (it needs the intensities, non-local) succeeds 55/55 |
| TC.7 F7 light-cone choice | PASS | 216 runs (a, b, phi) x 576 lines (lam_A, lam_B all 24 x 24), Bob at d = 5: Alice clicks exactly once (update t_A = 1), never before/after; the front is identically 0 through snapshot 3 and all fibres stay C0; the front reaches Bob at snapshot 9 = t_A + 3 + d; TIMELIKE t_B >= 9: E(a - b) = 1, 1/2, -1/2, -1, -1/2, 1/2 = cos(a - b) EXACTLY, max S = 5/2 (60-degree grid maximum); t_B <= 6 SPACELIKE (taxicab: snapshot t_B cannot depend on the click iff t_B < t_A + 1 + d): E = 0, S = 0; t_B = 7, 8 (inside the cone, front not yet there): E = 0; Alice's and Bob's marginals 0 for every (a, b, t_B) (no-signalling); bit gate (designed observer, pair 60 degrees apart): E = (1, 1, 1, -1), S = 4; every run rewinds exactly. Bob's wait = 8 updates from t_A = 4/3 of his clock period (his gear's click sizes 1, 1, 0, -1, -1, 0, 1, 1, ...: one sign cycle = 6 updates) |
| TC.8 all-or-nothing | PASS | Q = 5 (odd), 180 configs (s, r_W): 72 with a W click; all 108 silent ones leave both arms BIT-IDENTICAL to the free clocks at every update; all 72 clicking ones change them, minimum final disturbance 2 units |
| TC.9 M2-2 decoherence | PASS | V_ens = 0.808 / 0.833 / 0.650 / 0.262 (N = 1 / 2 exhaustive, 3 / 6 P2R's seed-1 sample); N = 1: V_single = V_eraser = 0.915; also N = 2: V_single 0.975, V_eraser 0.975, V_1 0.944; N = 3: 0.917 / 0.917 / 0.816; N = 6: 0.986 / 0.986 / 0.570 (all equal to P_m22_p2r.log); P_ens(N = 1) = 9/10, 3/4, 7/20, 1/10, 1/4, 13/20 (= S5-P2R's M2-2c unconditioned row). EXTRA (dev run 09:47, not asserted): N = 3 EXHAUSTIVE (27,000 configurations): V_ens 0.656, V_single 0.923, V_eraser 0.930, V_1 0.822 -- the 0.650 is the sample's value |
| TC.10 QM deviation (D12b) | PASS | A = 1, 2, 3 identical: c = 1 (90 degrees): P(+|s) = 1/2 x 4, P(+|s, W1) = 1, 1, 1, 0, P(+|s, W2) = 0, 0, 0, 1, I(s; exit) = 0.0000, I(s; exit, record) = 0.8113 bits; c = 0: 1, 1/2, 0, 1/2 (W1: 1, 1, 0, 1); c = 2: 0, 1/2, 1, 1/2; exactly one W click (update 1), one exit click (update 2), none early; rewind exact; M F^2 M F^2 = id |
| TC.11 back-acting reciprocal detectors (OPEN) | asserted parts PASS; exclusivity NOT kept | both forms are exact gradients (0 designations, s(dM) = -1 with sign_why); the first update is Born exactly (1, 3/4, 1/4, 0, 1/4, 3/4; both = none = 0); rewind exact (the engine switched to Python ints). AFTER the first click exclusivity BREAKS and the coupled system is UNSTABLE: g = 0 (rank 3): exactly-one 288, 288, 228, 180, 162, 168, 162, 156, 198, 108, 114, 186 of 288 for updates 0..11, max|arm b| 82 bits by update 12; g = 6 (rank 4, sign-definite for |b_d| <= 1): exactly-one 288, 216, 168, ... 168, max|arm b| 47,836 bits by update 12. Study 5 D3 reproduced: reciprocal coupling breaks exclusivity |
| TC.12 reversors | PASS | M' F^8 M' F^8 = id on the router (Q = 8) and all-or-nothing (Q = 5) initial data; M'-fixed remainders: Q = 3: {8, 9}, Q = 5: {14, 15}, Q = 4, 8: none; the odd-Q joint vacuum (0, 0, 3Q-1) is M'-fixed and stationary; F7: M' is NOT a reversor (declared, a-read gears) |

### Designations (one-way terms, with the justification string carried by every monomial)
- `observer detector: records without back-action (Study 5 D3)`: router dP/dM (18 monomials), F7 dA+-/dB+- (12), D12b W1/W2.
- `... read once, gated by a flash (rank 4)`: M2-2 exit pair (18). `... D12b gated readout ... (P_dec, rank 4)`: D12b exits.
- `common drive ...`: token drive (2). `sequential router link gear ...` (1). `parallel-read control exit gear ...` (n).
- `choice-front imprint (F7) ...`: 18 rank-4 kick monomials (6 per front gear; 6 b-only checked-and-designated, 12 with a).
- `choice-front emission (F7) ...`: 6 (3 b-only, 3 a-read).
- `which-path gear (Study 5 M2-2, S5-P2R) ...`: 2N (W read 3Q/Q_W, arm kick 3Q): NON-reciprocal under one divisor.
No designated monomial coincides with a force term (designated terms target detector/link/front/W gears, or the arm
gear with a factor b_W that no force term uses).

### Census (binding stage-1 condition 4)
| experiment | Q | G | monomials | rank | node/link | by degree [0,1,2,3] | designated | checked gradient | a-read | support viol. | reciprocity | s = -1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ring | 8 | 3 | 3 | 2 | 3/0 | [0, 3, 0, 0] | 0 | 3 | 0 | 0 | ok | — |
| fibre | 3 | 1 | 2 | 2 | 0/2 | [0, 2, 0, 0] | 0 | 2 | 0 | 0 | ok | — |
| router (either form) A = 1 | 8 | 8 | 24 | 3 | 24/0 | [0, 6, 18, 0] | 18 | 6 | 0 | 0 | ok | — |
| token + drive | 8 | 9 | 27 | 3 | 27/0 | [0, 9, 18, 0] | 20 | 7 | 0 | 0 | ok | — |
| sequential | 3 | 2 | 3 | 2 | 1/2 | [0, 3, 0, 0] | 1 | 2 | 0 | 0 | ok | — |
| parallel n = 3 | 3 | 6 | 9 | 2 | 3/6 | [0, 9, 0, 0] | 3 | 6 | 0 | 0 | ok | — |
| F7 | 4 | 20 | 71 | 4 | 36/35 | [0, 29, 24, 18] | 33 | 23 | 15 | 0 | ok | — |
| all-or-nothing | 5 | 7 | 8 | 2 | 8/0 | [0, 8, 0, 0] | 2 | 6 | 0 | 0 | ok | — |
| M2-2 N = 6 | 40 | 15 | 38 | 4 | 36/2 | [0, 20, 0, 18] | 30 | 8 | 0 | 0 | ok | — |
| D12b c = 1 | 4 | 8 | 28 | 4 | 28/0 | [0, 0, 4, 24] | 28 | 0 | 0 | 0 | ok | — |
| back-action g = 0 | 8 | 8 | 48 | 3 | 48/0 | [0, 6, 42, 0] | 0 | 48 | 0 | 0 | ok | ba.dM |
| back-action g = 6 | 8 | 8 | 90 | 4 | 90/0 | [0, 6, 42, 42] | 0 | 90 | 0 | 0 | ok | ba.dM |
- Constant-free deviation form: no degree-0 monomial anywhere; vacuum = all gears (0, 0, r0) is a fixed point.
- No reference channels (ref.*) are composed in any choice experiment, so q_lattice is not engaged; no link gears
  (all gears are node gears), so physical support = storage support (0 support violations, strict_support would pass).
- a-read (two-time) monomials: ONLY in F7 (15): u[F_j] += -12 b[PG](-e) a[C_j] b[dA+-] (6), u[F_j] += -12 a[PG](-e)
  a[C_j] a[dA+-] (6), u[P_j] += -12 a[F_j](+e) (3). Acyclic: F reads a of PG, dA+-, C; P reads a of F; stages = 3.
- OD3-type placements (two entries of one row from the same face neighbour, new channels only): F_j reads b[PG] and
  a[PG] at -e; P_j reads b[P_j] and a[F_j] at +e.
- Rank-4 (degree-3) monomials: NOT OD4 springs. They are (i) designated one-way: F7 gated kick (18), M2-2 gated exit
  pair (18), D12b gated readout (24); (ii) reciprocal: the back-action term -(g/2) b_d^2 |psi|^2 (minus sign, the cross
  term of an OD4 spring (lambda/4)(b_d^2 + |psi|^2)^2 WITHOUT its self-quartics). Flagged for the design board.

### Reversors (binding condition 3)
Declared in `layers/choice.MIRROR`: M' per gear for every b-only block (exact; TC.12 and the M checks in TC.2/TC.10);
F7 has a-read gears and NO known per-gear reversor (TC.12 shows M' fails) -- its exactness is the staged inverse
(every F7 run rewinds exactly); a staggered map for these gears is OPEN. Joint mirror-fixed vacuum: only for ODD Q
(r0 = 3Q-1 or 3Q). The Born routers (D = 16 kappa A^2), F7 (D = 24) and M2-2 (D = 240) need EVEN Q by matched
quantization, so they have NO mirror-fixed vacuum; the odd-Q experiments (sequential router Q = 3, 5; all-or-nothing
Q = 5) do. JR/JM are not used: every choice tensor has even-degree terms (|psi|^2), so J is not a symmetry.

## PRE-REGISTRATION 2 (written Tue Nov 10 09:54:36 UTC 2026, BEFORE the code exists or runs): manager rulings (09:5x)
The text below was written before any of TC.13/TC.14 or the complete-spring scan was coded or run.
TC.13 ODD-Q ROUTERS (ruling 3). (a) Parity theorem (no run needed; checked symbolically): a matched two-exit
  polarization router has K+ - K- = 2 kappa (|X1+X2|^2 + |X1-X2|^2) = 4 kappa (|X1|^2 + |X2|^2) = 0 mod 4, while
  D = 6Q = 2 mod 4 for odd Q: so matched (exhaustive AND exclusive AND Born) two-exit polarization routers need EVEN Q;
  the single-gear form needs the same D = 4 kappa S. Verified by enumeration: no (kappa, A) with 16 kappa A^2 = 6Q for
  odd Q = 1..999. (b) n = 2 SEQUENTIAL router at odd Q (abstract intensities with an ODD total D_I = 9, 15; Q = 3, 5):
  exact on all compositions (10, 16) and all tokens. (c) Near-matched polarization pair at odd Q (A = 1, ring arms,
  opposite form, kappa = floor(6Q/16)): exclusive (P(both) = 0), P(none) = (D - 16 kappa)/D exactly, and
  P(+ | detected) = I+/(I+ + I-) EXACTLY (1, 3/4, 1/4, 0, 1/4, 3/4): Q = 3 (P(none) = 1/9), Q = 11 (A = 1: kappa = 4,
  P(none) = 1/33), and the gauge layer's Q = 2^19 + 1 (kappa = 196608, P(none) = 6/D = 1/524289), exhaustive over the
  conserved token class r = 0 mod 6 (K = 0 mod 6), run in chunks; rewind exact.
TC.14 DESIGNATION AUDIT (ruling 1, 5): for every experiment's blocks: (i) no designated term shares its canonical
  (target, factor multiset) with an undesignated (force) term; (ii) for every designated b-only monomial, none of its
  reciprocal partner monomials is present in the tensor -- EXCEPT the M2-2 W coupling, whose partner shapes are both
  present with unequal weights (3Q/Q_W vs 3Q) and both designated (listed); (iii) the list of rank-4 (degree-3)
  designated monomials with their purpose.
EXPLORATORY (not acceptance, ruling 2): complete OD4 spring back-action Phi = kappa b_dP|U|^2 + kappa b_dM|V|^2
  - (lam/4)[(b_dP^2 + |U|^2)^2 + (b_dM^2 + |V|^2)^2] (minus sign, self-quartics included, X0 = 0: deviation form), A = 1,
  2, 3, lam = 1, 2, 3, 6: report first-click Born, exclusivity after it, growth (bits), rewind, reciprocity.

## PRE-REGISTRATION 3 (written Tue Nov 10 10:12:01 UTC 2026, BEFORE the code exists or runs): F7 at ODD Q
TC.15 F7 AT ODD Q (ruling 3: does the light-cone choice survive at an odd system Q?). The same F7 block and geometry
  with Q = 11 (D = 66), kappa = 8 (near-matched: S = 8 kappa = 64 < D for both parties), tokens over the conserved
  class r = 0, 2, ..., 64 (K = 0 mod 16, gcd(16, 66) = 2; 33 x 33 = 1089 lines, L = 33), phi in Z6, all 36 (a, b).
  Predictions: P(Alice clicks at t_A) = 32/33 exactly (never two clicks); Bob's pair: P(no click) = 1/33 at every
  update, never two; CONDITIONAL on both clicks: E(a - b) = cos(60 (a - b)) exactly for t_B >= 9 (max S = 5/2) and
  E = 0 for t_B <= 8 (spacelike t_B <= 6: |S| <= 2); unconditional E = (32/33)^2 cos for t_B >= 9; rewind exact.

## RESULTS 2 (written Tue Nov 10 10:12:31 UTC 2026): final suite run 10:07:58-10:10:20 UTC, 15 tests, OK, 141.9 s
Same command; TC.1-TC.12 re-ran with identical verdicts and numbers (results/choice/TC.*.json re-stamped).
| test | verdict | numbers |
|---|---|---|
| TC.11b complete OD4 spring (exploratory) | asserted parts PASS; exclusivity NOT kept; blow-up NOT stopped | Phi = kappa b_dP|U|^2 + kappa b_dM|V|^2 - (lam/4)[(b_dP^2+|U|^2)^2 + (b_dM^2+|V|^2)^2]: exact gradient (140 monomials checked, 0 designated); first click Born and exclusive in all 12 cases (A = 1, 2, 3 x lam = 1, 2, 3, 6); after it exactly-one drops to 45-80 % (e.g. A = 3, lam = 1: 2592, 1934, 1870, 1666, ... of 2592); EVERY case exceeds 256 bits within 6-12 updates (A = 1: 6-8 updates; A = 3, lam = 1: 12); rewind exact over the updates run. Compare the g-form (cross term only, TC.11 + dev scan): A = 2, 3 with g <= 3 stayed bounded (max|b| <= 8) for 12 updates but still lost exclusivity; A = 1 always blew up |
| TC.13 odd-Q routers | PASS | (a) parity: no odd Q <= 999 admits a matched two-exit polarization router (even Q = 8, 16, 24, ... do); (b) n = 2 sequential router, ODD total D_I = 9 (Q = 3) and 15 (Q = 5): all 10 / 16 compositions x all tokens exact, rewind exact; (c) near-matched polarization pair at odd Q: Q = 3: P(none) = 1/9; Q = 11 (A = 1, kappa = 4 and A = 2, kappa = 1): P(none) = 1/33; GAUGE Q = 2^19 + 1 (D = 3,145,734, kappa = 196,608, exhaustive over the conserved class r = 0 mod 6: 524,289 tokens x 6 phases, 12 chunks of 64^3 nodes, 13 s): P(both) = 0, P(none) = 1/524289 exactly, P(+ | detected) = 1, 3/4, 1/4, 0, 1/4, 3/4 EXACTLY; rewind exact |
| TC.14 designation audit | PASS | no designated monomial coincides with a force monomial (all 12 experiments); no reciprocal partner of any designated b-only monomial is present, EXCEPT the declared M2-2 W pair (u_W += 3Q/Q_W b_X and u_X += 3Q b_W, both designated); rank-4 designated monomials: F7 imprint 18, M2-2 gated exit pair 18, D12b gated readout 24 (purposes = their designation strings) |

### ONE Q (ruling 3), answer
- THEOREM (parity): a matched two-exit polarization router needs D = K+ - K- = 2 kappa(|X1+X2|^2 + |X1-X2|^2) =
  4 kappa (|X1|^2 + |X2|^2) = 0 mod 4, but D = 6Q = 2 mod 4 for odd Q. So exact (exhaustive + exclusive + Born) Born
  routers built on the polarization identity force EVEN Q (D = 48A^2 for kappa = 3 is one instance). The same holds for
  the single-gear form (D = 4 kappa S) and for the F7 photon/setting-gated pairs (D = 8 kappa A^2).
- What works at ODD Q: (i) routers whose exit intensities have an odd total (sequential router, TC.6/TC.13: exact);
  (ii) polarization pairs NEAR-MATCHED: exclusive, Born-exact conditional on a click, with a non-detection probability
  (D - S)/D >= 2/D per readout -- 1/524289 at the gauge layer's Q = 2^19 + 1 (TC.13). TC.15 tests F7 in this regime.
- Recommendation for stage 3: an odd system Q is compatible with the choice layer if a per-readout non-detection
  (D - S)/D is accepted (it can be made 2/D or 6/D); exact detection efficiency 1 needs even Q.

### Reversor census (rulings 3, 4)
- b-only blocks: M' per gear, exact (TC.12; M checks in TC.2, TC.10). Odd Q: the vacuum (0, 0, 3Q-1) is M'-fixed;
  even Q (routers, F7, M2-2 as built) has no mirror-fixed vacuum.
- F7: no reversor known. Per-gear M/M' fail (a-read gears). A P-T combination also fails structurally: the emission
  source F(x,t) - F(x+e,t-1) maps under x -> -x, t -> -t to F(y,t) - F(y-e,t+1), which is not of the same form (the
  block is chiral: right-moving emission, left-moving gate). OPEN; exactness is the staged inverse (every run rewinds).

### Files (B1-CHOICE)
layers/choice.py (builders + MIRROR + VACUUM_NOTE), prepare/choice.py (ring/pair states, Prep, yz_lines),
observe/choice.py (quotient, click_flags, official, kinds, values, harmonic_V, mutual_info, bit_gate),
tests/test_choice.py (TC.1-TC.14, TC.11b), demos/choice/experiments.py (exp_* runners, audits), demos/choice/run_demos.py,
results/choice/TC.*.json, NOTES_choice.md. Nothing else created or changed. Note: a regression run of the stage-0
suites at 10:10 (27 tests OK) re-stamped results/T0.*.json, as every stage-0 run does; all 23 stage-0.2 code/doc
hashes verified unchanged (10:11).

## PRE-REGISTRATION 4 (written Tue Nov 10 10:13:00 UTC 2026, BEFORE the code exists or runs)
TC.16 F7 SPACELIKE PHOTON-COPY READER (S5-M2's R2; LHV control). Same F7 block (Q = 4, D = 24, A = 1). The source's
  common past gives TWO flashes with the same ring sample c(phi): Alice's (left-moving, at x_A at t = 1) and Bob's
  (right-moving, prepared at x_B - 1, at x_B at t = 1). Bob's setting ring is written into the C gears at x_B, so
  the Alice-type photon-gated router at x_B is Bob's photon-copy reader; both clicks happen at update 1 -> 2
  (|dt| = 0 < |dx|_1 = 5: SPACELIKE). Exhaustive over phi in Z6, lam_A, lam_B in 0..23, all 36 (a, b).
  Predictions: exactly one click each; E(a - b) = cos(60 (a - b))/2 = 1/2, 1/4, -1/4, -1/2, -1/4, 1/4; max S = 5/4;
  no front is emitted at x_B (Bob's marker is right-moving, so the gated kick reads zeros there); marginals 0;
  rewind exact.

## TC.15 DEVIATION, recorded honestly (written Tue Nov 10 10:17:35 UTC 2026; dev run 10:12:01-10:16:34, 272.6 s)
The pre-registered TC.15 prediction FAILED (my error in the prediction, not a code bug): at odd Q = 11 Bob's
CONTINUOUSLY exposed pair is only near-matched (K+ - K- = S = 64 != D = 66), so the equal-remainder lock is lost after
the first update (r+ - r- drifts by S - D every update). Observed: Alice detects 32/33 (as predicted); Bob's
per-update no-click rate varies with the update (1/66 ... 17/198) and both detectors click together at some updates;
conditioned on coincidences, E(a - b) = 1, 1, -1, -1, -1, 1 and max S = 4 at t_B >= 9 (E = 0 before), i.e. a
detection-loophole artefact of history-dependent non-detection; unconditional E(a = b) = 1024/1089 = (32/33)^2;
rewind exact. Lesson: the sigma-delta (continuously exposed) paired clock NEEDS matched quantization (even Q); at odd
Q a reader must be exposed ONCE, from fresh equal remainders. tests/test_choice.py keeps TC.15 as an
expectedFailure record.

## PRE-REGISTRATION 5 (written Tue Nov 10 10:17:35 UTC 2026, BEFORE the code exists or runs)
TC.15b F7 AT ODD Q WITH A ONE-SHOT (GATED) BOB. build_f7(..., bob_gate=True) adds Bob's gate fibre BG (audit) and gates
  Bob's pair: u_dB+- = +-kappa sum_j b_BG b_B (b_B +- b_P) (rank 4, designated observer). Bob's gate flash reaches x_B
  at snapshot t_B only, so his pair is exposed once from its fresh equal remainders. Q = 3 (D = 18), kappa = 2
  (S = 16), tokens over the conserved class r = 0, 2, ..., 16 (9 x 9 lines), phi in Z6, all 36 (a, b), t_B = 9
  (timelike, front present) and t_B = 6 (spacelike: snapshot 6 at x_B is outside the taxicab future of the click,
  whose output is snapshot 2 at x_A and reaches x_B at snapshot 7 at the earliest). Predictions: Alice detects
  8/9, Bob detects 8/9 at t_B (no click before or after), never two clicks; conditional on both clicks E = cos(60
  (a - b)) exactly and max S = 5/2 at t_B = 9; E = 0 and S = 0 at t_B = 6; rewind exact.

## TC.15b / TC.16 dev runs (written Tue Nov 10 10:19:31 UTC 2026)
- TC.15b first attempt (10:18:3x) crashed on a HARNESS bug: Bob's gate flash had its a-value on the wrong side (a
  right-moving flash that never reached x_B, so 0 coincidences and a 0/0 fraction). Fixed (a at x_B + t_B + 1 for a
  left-moving flash, as for Alice's photon). Rerun 10:18:47-10:19:31: AS PREDICTED -- Q = 3 (odd), D = 18, kappa = 2:
  Alice detects 8/9, Bob detects 8/9 at t_B, no Bob click outside his gate, never two clicks in a pair; conditional on
  both clicks: t_B = 9 (timelike) E = cos(a - b) exactly, max S = 5/2; t_B = 6 (taxicab-spacelike) E = 0, S = 0;
  every run rewinds exactly.
- TC.16 (10:13:23-10:14:06): AS PREDICTED -- spacelike photon-copy reader E = 1/2, 1/4, -1/4, -1/2, -1/4, 1/4
  = cos/2, max S = 5/4, Bob's marginals 0, exactly one click each at update 1, no front emitted at x_B, rewind exact.

## Caveats and open items (written Tue Nov 10 10:20:30 UTC 2026)
1. TC.11 / TC.11b: back-acting reciprocal detectors (rank 3; spring cross term alone; COMPLETE OD4 spring) are exact
   gradients and keep the FIRST click Born and exclusive, but none keeps exclusivity after it, and none is stable on
   these exact rings (bounded only for the cross-term form at A = 2, 3, g <= 3 within 12 updates). OPEN.
2. F7 has no known reversor (a-read gears; chiral emission). Exactness = staged inverse (every run rewinds). OPEN.
3. Exact Born routers on the polarization identity force EVEN Q (parity theorem, TC.13); at odd Q: near-matched pairs
   with a per-readout non-detection (D - S)/D >= 2/D, exposed ONCE from fresh equal remainders (TC.15b). The
   continuously exposed paired clock (sigma-delta token, F7's Bob in TC.7) is EVEN-Q only (TC.15 deviation).
4. M2-2's W coupling is non-reciprocal under one divisor (designated, kept for exact reproduction of P2R's numbers);
   a reciprocal W variant was not built.
5. Every node holds every gear type: observer gears at other nodes also record passing flashes (e.g. Alice-type
   detectors left of x_A click when her flash passes them). They are one-way, so the board is unchanged, and their
   records are not read; only the declared nodes are read.
6. The F7 photon is a prepared exact travelling FLASH (one ring sample in 3 fibre components + a unit marker fibre)
   from the common past, not a long clock train; Alice's exposure is one update by construction (photon-gated).
7. The F7 bit gate is a read-only observer function (a designed reader), not a gear.
8. The D12b toy's 90-degree kick is in the gated readout (P_dec's declared equivalence), not a kick of the arms.
9. Rank-4 terms of this layer are designated one-way gates/readouts only (manager ruling 1): F7 imprint (18), F7
   one-shot Bob (12, odd-Q variant), M2-2 gated exit pair (18), D12b readout (24); the reciprocal rank-4 forms appear
   only in the exploratory TC.11/TC.11b and are not shipped as force terms.

## RESULTS 3 (written Tue Nov 10 10:30:05 UTC 2026): suite run 10:20:03-10:28:18 UTC, 18 tests, OK (expected failures = 1), 495 s
TC.1-TC.14, TC.11b, TC.15b, TC.16 PASS (numbers as recorded above); TC.15 is the expectedFailure record of the failed
odd-Q continuous-reader prediction (S = 4 on coincidences).

## MANAGER RULING 10:2x (Study 7, ONE-P2) -- STATEMENTS (written Tue Nov 10 10:30:05 UTC 2026)
(1) THE C0-FIBRE F7 (TC.7, TC.15b, TC.16) RUNS ON THE TAXICAB CONE AND IS NOT THE APPROVED FORM. Its front moves on
    exact d'Alembert fibres at 1 site/update along x = sqrt(3) c (the cone gap the owner did NOT adopt, v5 §8). With
    d = 5, E = cos and S = 5/2 already appear at t_B = 9, 10, where Bob is SPACELIKE for the round cone c = 1/sqrt(3)
    (round-timelike needs t_B >= t_A + 1 + 5 sqrt(3), i.e. t_B >= 11). TC.7/TC.15b/TC.16 are kept as MECHANISM TESTS
    ONLY (labelled so in layers/choice.build_f7). ONE-P2's theorem: exact (rounding-free) single-quantum transport is
    only taxicab; the round cone needs rounding light gears, exact only to O(1/A).
(3) ODD Q PREDICTION: at the system's ONE odd Q, an exact efficiency-1 two-exit Born router is impossible (TC.13
    parity theorem); routers built at odd Q are exclusive and Born-exact CONDITIONAL on a click, with a per-readout
    non-detection (D - S)/D >= 2/D (1/9 at Q = 3, 1/33 at Q = 11, 1/524289 at Q = 2^19 + 1). This tiny inefficiency
    is the board's PREDICTION.
(4) READERS MUST BE ONE-SHOT. A continuously exposed reader at odd Q loses its equal-remainder lock and, conditioned
    on coincidences, gave S = 4 (TC.15): a detection-loophole artefact, not physics. Odd-Q readers are exposed once
    from fresh equal remainders (TC.15b: S = 5/2 on coincidences with 8/9 efficiency per party).

## PRE-REGISTRATION 6 (written Tue Nov 10 10:30:05 UTC 2026, BEFORE the code exists or runs): STATUS PROBE for ruling (2)
TC.17 PROBE -- F7 with the front carried by the HEADROOM LIGHT gear u = (Q-1) Sum_6 b + 6b (round cone c_Q =
  sqrt((Q-1)/(3Q))), emitted one-way by u_P += gamma b_F at Alice's plane; plane-wave geometry (all (y, z) identical;
  Alice's q uniform per run: one representative token per arc, weighted by the exact arc lengths), odd Q, exact
  period-6 clocks (60 degrees), Bob at d = 5. Observable: Bob's one-shot reader input at every readout time t_B
  (P_B(+|q) = K+/(K+ + |K-|) on detection, the verified arc law), E(a, b, t_B) for all 36 settings.
  Predictions: (i) t_B <= t_A + 1 + d = 7 (taxicab-spacelike): E = 0 EXACTLY (no light can arrive); (ii) gap region
  t_B = 8..10 (round-spacelike, inside the taxicab cone): max |S| <= 2; (iii) later: E approaches rho cos(60 (a - b) +
  theta0) with rho, theta0 from the lattice dispersion (60-degree light has k ~ 120 degrees, group speed ~1/3, so a
  slow, dispersive build-up with algebraic transients is expected; the full "E = cos + O(1/A)" acceptance and its 1/A
  scaling over 3 A values are NOT claimed by this probe); (iv) every run rewinds exactly.

## TC.17 PROBE RESULTS (written Tue Nov 10 10:34:03 UTC 2026; dev runs 10:31:27-10:33:27 UTC, A = 30, 100, 300)
Light-carried front, odd Q = 1201 / 13335 / 120001 (gamma = 2077 / 23093 / 207844), d = 5, plane-wave geometry,
12 runs per A ((a, q) x the 6 b on six lines), 22-27 s per A. Round cone: first round-timelike snapshot
t_A + 1 + d sqrt(3Q/(Q-1)) = 10.66; taxicab: 7.
- (i) t_B <= 8 (all taxicab-spacelike snapshots and the first gap snapshot): E = 0 EXACTLY for every setting, all A.
  PASS.
- (ii) GAP region (round-spacelike, inside the taxicab cone) t_B = 9, 10: max |S| = 0.042, 0.092 (A = 30); 0.013,
  0.040 (A = 100); 0.004, 0.049 (A = 300) -- tiny evanescent precursors, far below 2. PASS.
- (iii) NOT MET. After the round-cone arrival E(a, b) is an exact cosine in (a - b) at every t_B (fit residual 0
  while the reader is unclipped), but its amplitude rho(t_B) and phase theta(t_B) BEAT and do not settle within
  30 updates (rho = 0.94 at t = 15, 0.14 at t = 19, 1.07 at t = 21, 1.18 at t = 28), because 60-degree light is
  lattice-scale (k ~ 120 degrees, group speed ~ 1/3) and the click switches the source on abruptly. Where rho > 1 the
  front exceeds Bob's clock amplitude, his Born reader CLIPS, and max S reaches 3.35-3.40 > 2 sqrt 2 (t = 27-28):
  Tsirelson for Born readers needs |front| <= |clock| (|c_a| <= 1), which this probe does not enforce.
- The curves for A = 30, 100, 300 agree to a few 1e-2 and converge (e.g. max S at t = 14: 1.992, 2.018, 2.034): the
  remaining structure is linear lattice physics, not rounding; rounding effects shrink with A.
- (iv) every run rewinds exactly; reciprocity: the light stencil is a gradient, the emission u_P += gamma b_F is
  designated (EMIT_LIGHT).
STATUS of ruling (2): the round-cone carrier removes the cone-gap correlations (E = 0 through the gap), but the
approved form is NOT finished: E = cos(a - b) + O(1/A) needs (a) slow clocks (omega0 << 1, continuum light),
(b) an amplitude-limited one-shot reader (|front| <= |clock|) or a normalised one, (c) a smooth front envelope or a
steady-state readout window, (d) a lattice long enough for d / c_Q >> the clock period. Not done by 11:45.

## OWNER PRINCIPLE (manager 10:3x) "the detector acts on the board ... that IS the choice -- BEFORE the click":
## DESIGN NOTE + PRE-REGISTRATION 7 (written Tue Nov 10 10:34:03 UTC 2026; NOT run in stage 1)
Analysis. In one potential, a Born read u_d = kappa |psi|^2 comes from Phi = kappa b_d |psi|^2, whose arm partner is
2 kappa b_d psi: it vanishes while the detector is at rest (b_d = 0), so the reciprocal detectors of TC.11 act only
AFTER their first overflow (and then break exclusivity and run away). A pre-click action therefore needs detectors
whose b is non-zero before any click: RUNNING detector clocks (u_d += 3Q b_d) of small amplitude a_d, so that the
same potential modulates the arms continuously (which-way imprint) and the arms drive the detectors' remainders and
phases (the race) before either overflows. Exclusivity must then come from a conservation law of the reciprocal
system (the board-Noether two-time charge of the coupled clocks): the winner's growth must exhaust the quantum's
amplitude so that the loser's drive vanishes -- this is NOT guaranteed by any construction built here.
Constraints: one potential; rank <= 3, or rank 4 only as a COMPLETE OD4 spring; six neighbours; integers.
Candidate C1: Phi = kappa (b_d+ |U|^2 + b_d- |V|^2) + (3Q/2)(b_d+^2 + b_d-^2) with running detector clocks,
s(d-) = -1; candidate C2: C1 + a complete OD4 spring on each detector (b_d^2 + |psi|^2 - X0^2)^2 with X0 chosen so the
unclicked rings are its minimum (vacuum-neutral only for one intensity split; to be studied).
Pre-registered criteria for the first runs (to be run after stage 1): (i) Born frequencies |psi+-|^2/(sum)
(exact or O(1/A)); (ii) exactly one click per quantum; (iii) interference visibility drops when the detector is
coupled, BEFORE any click (which-way); (iv) no runaway after the click (bounded max|b|); (v) exact rewind.
Known risks from stage 1: rank-3 parametric coupling of running clocks is unstable at zero headroom (Study 5 PR-5);
the complete spring's self-quartic destabilises the exact rings (TC.11b). STATUS: design only, no run.

### Census addendum (written Tue Nov 10 10:34:25 UTC 2026): the F7 variants (strict_support compose passes)
| experiment | Q | G | monomials | rank | node/link | by degree [0,1,2,3] | designated | checked gradient | a-read | support viol. | reciprocity | rank-4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F7 gated Bob (odd Q = 3) | 3 | 21 | 73 | 4 | 36/37 | [0, 31, 12, 30] | 33 | 25 | 15 | 0 | ok | 30 (18 kick + 12 one-shot Bob, designated) |
| F7 light carrier (Q = 1201) | 1201 | 20 | 83 | 4 | 39/44 | [0, 41, 24, 18] | 33 | 38 | 12 | 0 | ok | 18 (kick, designated) |
Rank-4 terms anywhere in this layer: designated one-way gates/readouts only (F7 kick, one-shot Bob, M2-2 exit pair,
D12b readout) plus the exploratory reciprocal forms of TC.11/TC.11b (not shipped as force terms).

## PRE-REGISTRATION 8 (written Tue Nov 10 10:38:03 UTC 2026, BEFORE the code exists or runs)
NEW FILES ONLY (rolling freeze): layers/choice_oddq.py, tests/test_choice_oddq.py.
TC.18 ROUTER AT THE INTEGRATOR'S ODD Q = 2^29 + 1 (manager 10:3x). Helper near_matched_kappa(Q, A) = floor(6Q / 16A^2)
  for two 3-gear rings of amplitude A (S = 16 kappa A^2 <= D). Predictions for A = 1: kappa = 201326592 = 3 * 2^26,
  S = 3 * 2^30, D - S = 6, P(none) = 1/(2^29 + 1) per readout (the board's prediction, >= 2/D). Gear check (the arc law
  cannot be enumerated over ~5.4e8 class tokens): every token within 8 of each arc boundary (0, K-, D - K+, D - 1) for
  every phase s, plus a declared numpy default_rng(29) sample of 20,000 tokens per s: each outcome equals the arc law,
  never two clicks, and the none-tokens are exactly [K-, D - K+); rewind exact.
## Study 7 hint (ONE-M2, 10:36), recorded for the pre-click detector (design only, not built in stage 1)
"The quantum" = the integer Noether charge J = sum b(t-1)^T X b(t); the exclusivity invariant = the remainder lock (for
inputs K1 = -K2 the sum r1 + r2 is conserved mod D for ANY K(t), so it survives a reciprocal rank-3 back-action);
OD4 springs are U(2)-flat or convex and cannot give winner-takes-all; proposal: detectors read the FLUX of the U(1)
charge, whose time integral is J by Noether, independent of the back-action. My note: with an integer charge of one
unit, integrality may itself force a single winner (no fractional transfer); to be verified. Pre-registered criteria
(i)-(v) of PRE-REGISTRATION 7 apply. STATUS: not built in stage 1.

## TC.18 RESULT (written Tue Nov 10 10:38:41 UTC 2026; run 10:38:32-10:38:33 UTC): PASS, as pre-registered
Q = 2^29 + 1 = 536870913 (D = 3221225478): kappa = 201326592 = 3 * 2^26, S = 3 * 2^30, D - S = 6, P(none) =
1/536870913 per one-shot readout (the board's prediction); for every phase s the gear outcomes equal the arc law on all
~20,000 checked tokens (boundary neighbourhoods +-8 of 0, K-, D - K+, D - 1, plus the rng(29) sample): 0 mismatches,
never two clicks, the 6 none-tokens are exactly [K-, D - K+); P(+ | detected) = 1, 3/4, 1/4, 0, 1/4, 3/4 exactly; rewind
exact. API for the integrator (new file, frozen core untouched): layers/choice_oddq.near_matched_kappa(Q, A),
predicted_non_detection(Q, A), build_odd_q_router(*, Q, A, arm1, arm2, form, name).

## RESULTS 4 (written Tue Nov 10 10:44:39 UTC 2026): FINAL suite on the frozen choice core
`tests/test_choice.py`: 19 tests, OK (expected failures = 1: TC.15), 607.2 s (10:34:17-10:44:24 UTC); TC.17 PASS on
its asserted parts (E = 0 through t_B = 8; gap max|S| <= 0.092; rewind) with the dev-run numbers above.
`tests/test_choice_oddq.py` (new file): TC.18 OK.
ROLLING FREEZE (manager 10:4x): the frozen choice core = layers/choice.py, prepare/choice.py, observe/choice.py,
tests/test_choice.py, demos/choice/__init__.py, demos/choice/experiments.py, demos/choice/run_demos.py (sha256 below).
Post-freeze work goes to NEW files only (layers/choice_oddq.py, tests/test_choice_oddq.py so far).
| file | sha256 |
|---|---|
| layers/choice.py | 6e28fe434ab1f53fa6adde238eccf8d0b492f614db9ee7e914f8122914c0bf3b |
| prepare/choice.py | bf36d3b1915086d749a6abe7660ed2852fcfc91b9ad919ec7133e1d2615d4c9c |
| observe/choice.py | 6b565d126e2b84cecc81b8be265ab264b69d6451b23f0fdbd5e34d6e7dcf7b7f |
| tests/test_choice.py | 25a822b264fbe58f9dcda43d23de3652bd32ee3e16ec6734c26d118e8f0146cc |
| demos/choice/__init__.py | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| demos/choice/experiments.py | e22e989e9be1a3f739e109e47c9661801796d82ae121c54820d21ac4e4f8084f |
| demos/choice/run_demos.py | 20c858bcc35a1eea3eed5f1ccc02ad1fb1cf756b55c65473219a476eaeebacdb |

## PRE-REGISTRATION 9 (written Tue Nov 10 10:45 UTC 2026, BEFORE the run): long-time status probe (no new code)
TC.17-long: exp_f7_light(A = 30, steps = 80, L = 48) (frozen function, larger box so wrap-around arrives later).
Question (report only, no pass/fail): does the received front settle to a CW state (rho(t), theta(t) -> constants
rho_CW ~ 1, theta_CW ~ 29.6 deg from the dispersion) or keep beating; E = 0 through t_B = 8 and max|S| <= 2 in the
gap are re-checked; rewind exact.

## TC.17-long RESULT (written Tue Nov 10 10:53:40 UTC 2026; run 10:47:04-10:52:19, A = 30, L = 48, 80 updates)
(A first background attempt at 10:45 was killed by the kernel for lack of memory: the run kept the full history of
81 states x 110,592 nodes x 20 gears. Rerun in the foreground.) The front keeps BEATING to t = 80: rho(t) swings
between ~0.3-0.6 and ~1.2 with period ~6 updates, theta(t) wanders around 30-60 deg (theta_CW = 29.6); max S keeps
exceeding 2 sqrt 2 where rho > 1 (clipping). Diagnosis: in the plane-wave (1-D) geometry the lattice Green's function
is a STEP (no Huygens principle), so the abrupt switch-on of the 60-degree source leaves a PERSISTENT zero-frequency
plateau at Bob, which beats with the 60-degree front (period 6). Fix to try: a source with no DC content -- the time
difference gamma (b_F - a_F) (same |response| at 60 degrees: |1 - e^{-i w}| = 1; phase +60 deg), plus gamma scaled so
that |front| <= |clock| (no clipping), a one-shot reader, and no full history in memory.
## PRE-REGISTRATION 10 (written Tue Nov 10 10:53:40 UTC 2026, BEFORE the code exists or runs) -- NEW FILES ONLY
TC.19 ROUND-CONE F7, fixed source. layers/choice_round.py: build_f7(..., carrier="light", bob_gate=True) of the frozen
layer PLUS one extra designated term per front component, u_P += -gamma a_F (so the source is gamma (b_F - a_F)).
gamma = round(rho0 * 2(Q-1) sin k) with rho0 = 0.9 (CW amplitude 0.9 x Bob's clock, leaving room for overshoot).
A = 30, 100, 300 (odd Q = 1201, 13335, 120001), d = 5, L = 32, 50 updates, plane-wave geometry and Bob's one-shot
reader via the verified arc law as in TC.17. Predictions: (i) E = 0 exactly for t_B <= 8; (ii) gap t_B = 9, 10:
max |S| <= 2; (iii) after the arrival the beats are strongly reduced: for t_B in 25..45, rho within 0.9 +- 0.15 and
theta within theta_CW + 60 deg +- 20 deg, and no clipping (max S <= 2 sqrt 2); (iv) the differences between A = 100
and A = 300 are smaller than between A = 30 and A = 100 (rounding effects ~ 1/A); (v) rewind exact.

## TC.19 A = 30 RESULT (written Tue Nov 10 10:57:13 UTC 2026; run 10:54:11-10:56:21) and AMENDMENT (before further runs)
A = 30, Q = 1201, gamma = 1869 (rho0 = 0.9), 50 updates, rewind exact, reciprocity ok. (i) E = 0 for t_B <= 8: YES.
(ii) gap t_B = 9, 10: max S = 0.04, 0.09: YES. The BEATS ARE GONE: rho rises smoothly 0.02 (t = 9) -> 0.43 (t = 19)
-> 0.84 (t = 26) -> 0.99-1.12 (t = 31-50); theta settles from ~150 deg (t = 13) to 63-100 deg (theta_CW = 89.6),
drifting slowly. (iii) FAILS as pre-registered: rho reaches 1.05-1.12 (> 0.9 + 0.15), theta 63-69 at t = 25-30
(outside 89.6 +- 20), and max S = 2.92-3.06 > 2 sqrt 2 at t = 37-45 where rho > 1 (clipping). The CW amplitude is
~20 % above my estimate |G| = 0.9 |F| (not understood yet; the slow transient may still be settling).
AMENDMENT (written before the runs it governs): TC.19b = the same with rho0 = 0.75 (to keep |front| < |clock|),
A = 30, 100, 300; predictions: (i), (ii), (v) as TC.19; (iii') max S <= 2 sqrt 2 at every t_B (no clipping), rho in
[0.7, 1.0] for t_B = 30..50; (iv) the A = 100 vs 300 curves closer than A = 30 vs 100.

## TC.19 RESULTS, rho0 = 0.9 (written Tue Nov 10 11:03:18 UTC 2026; runs 10:57:13-11:02:56, A = 100, 300)
A = 100 (Q = 13335, gamma = 20784) and A = 300 (Q = 120001, gamma = 187060): rewind exact, reciprocity ok.
(i) E = 0 for t_B <= 8: YES. (ii) gap t_B = 9, 10: max S = 0.01, 0.04 (A = 100); 0.00, 0.04 (A = 300): YES.
(iii) FAILS as for A = 30: rho = 1.04-1.14 for t_B = 32-50, max S up to 3.00-3.03 (clipping); theta 66-107 deg.
(iv) YES: the curves are nearly A-independent and the A = 100 vs 300 differences (<= 0.01-0.02 in rho, <= 0.05 in
S) are smaller than A = 30 vs 100 (<= 0.03-0.06): the remaining deviations from the ideal law are linear lattice
physics (dispersion of 60-degree light, slow transient), NOT rounding; rounding effects shrink with A.
Measured late CW amplitude ~1.2 x my estimate |G| = rho0 |F| (factor not yet explained).

## TC.19b RESULTS, rho0 = 0.75 (written Tue Nov 10 11:05:21 UTC 2026; runs 10:57:20-11:04:55, A = 30, 100, 300)
All as amended-pre-registered: (i) E = 0 exactly through t_B = 8; (ii) gap t_B = 9, 10: max S = 0.042/0.092,
0.013/0.028, 0.004/0.033 (A = 30/100/300); (iii') NO clipping: max S over all t_B = 2.684, 2.675, 2.668 <= 2 sqrt 2;
rho(t_B = 30..50) in [0.74, 1.00], [0.78, 0.98], [0.78, 0.98]; (iv) A = 100 and 300 nearly identical (rounding
effects shrink with A); (v) every run rewinds exactly; reciprocity ok (light stencil = gradient; the source halves
gamma b_F and -gamma a_F designated).
WHAT THIS SHOWS. Carried by the round-cone light, the F7 correlations are EXACT COSINES in (a - b) at every readout
(E = rho(t) cos(60 (a - b) + theta(t)), fit residual 0 while the reader is unclipped), ZERO outside the round cone
(taxicab-spacelike: exactly 0; gap: S <= 0.09), and below Tsirelson (S <= 2.68 < 2 sqrt 2). NOT achieved: the ideal
fixed law E = cos(a - b - theta0) + O(1/A): rho(t) and theta(t) still drift (rho 0.74-1.00, theta 70-107 deg over
t_B = 30..50), an A-INDEPENDENT slow transient of lattice-scale (60-degree) light. The remedy is slow clocks
(omega0 << 1, dispersion-free light) with d / c_Q >> the period, i.e. a much longer box than the L^3 cube allows here.
Files (new, post-freeze): layers/choice_round.py (build_f7_round, round_gamma; 3 extra designated a-read monomials
u[f7.P_j] += -gamma a[f7.F_j], so the round F7 has 15 a-read monomials), demos/choice/round_cone.py (exp_f7_round),
results/choice/TC.19*.json(l). Not yet in a unittest (run by scratch drivers; JSON evidence copied to results/choice).

## PRE-CLICK BACK-ACTION DETECTOR (owner principle; manager priority 1 of 10:45) -- STATUS (written Tue Nov 10 11:05:45 UTC 2026)
NOT BUILT in stage 1 (honest status). What the stage-1 work establishes for its design (algebra + TC.11/TC.11b runs):
1. A reciprocal detector AT REST cannot act before its click: Phi = kappa b_d |psi|^2 gives the arms 2 kappa b_d psi,
   which is zero while b_d = 0 (TC.11: the first update is untouched Born; all action is post-click).
2. A RUNNING detector clock does not disturb its Born remainder law: with u_d = 3Q b_d + kappa |psi|^2 the clock part
   adds K = 6Q b_d = D b_d, a multiple of D, so the remainder still advances by 2 kappa |psi|^2 per update and the
   arcs (Born weights) are unchanged, while the same potential lets b_d(t) != 0 act on the arms continuously BEFORE
   the first extra overflow (the pre-click which-way imprint the owner asks for). This is the proposed construction.
3. ONE-M2's remainder lock (antitone inputs K1 = -K2) survives ANY back-action (r1 + r2 conserved mod D), but it makes
   l1 = -l2 identically (one signed event): the Born split must then come from the SIGN of the first crossing, which
   needs a signed drive whose race depends on the hidden phase -- the open step.
4. The lock of the opposite-sign pair (r+ = r-) breaks under back-action because the arms' norm (the matched total
   2 kappa (I+ + I-)) changes (TC.11); a detector input whose time integral is a Noether charge fixed by conservation
   (ONE-M2's charge flux) would keep the arcs matched in spite of back-action -- the reason to read the flux.
Next step (after stage 1): C1 of PRE-REGISTRATION 7 (running detector clocks, rank 3, one potential) with the antitone
lock and a flux-type input, tested against criteria (i)-(v).

## FINAL STATE (written Tue Nov 10 11:06:44 UTC 2026)
- Frozen choice core (7 files, hashes in RESULTS 4): unchanged since the freeze (sha256 re-checked 11:06).
- New files after the freeze: layers/choice_oddq.py (46d56f03...), layers/choice_round.py (58b3c47a...),
  demos/choice/round_cone.py (b993831c...), tests/test_choice_oddq.py (31ded1d6...), tests/test_choice_round.py
  (71716e76...). tests/test_choice_round.py: TC.19b OK (11:05:36-11:06:36, 60.3 s, A = 30).
- No tracked repository file changed; universe24/ and core/ untouched; no git.
