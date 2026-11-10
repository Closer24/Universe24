# AGREE_ONE — Study 22 "ONE VERSION": ONE-A (builder) x ONE-B (independent verifier)
Created by ONE-A Tue Nov 10 15:11:37 UTC 2026 (date -u). PROTOCOL: ONE-A writes the rows; ONE-B only APPENDS, in a section "ONE-B marks" at the
end, one line per row: R# | AGREE / DISAGREE / CAN'T-CHECK | note | evidence. Then ONE-B signs with a date -u stamp.
Evidence paths are relative to s22/ONE-A_work/ unless stated. Pre-registration: s22/ONE-A_NOTES.md §2 (14:49:43 UTC), plus A1
(load scale, before any T run) and A2 (coupling option, 15:10:24, before its bang run). Code (NEW files): research/metric_variant_v1/
layers/one.py, observe/one.py, prepare/one.py, demos/one/run_one.py (+ __init__.py), tests/test_one.py, NOTES_one.md. ALL runs
were in the scratch mirror s22/ONE-A_work/mirror (manager 14:57). Labels: THEOREM / DERIVED / NUMERIC / POST HOC / OPEN / NEW LAW.
Binding owner rule (14:47): only the fixed tensor + the seed + Rule3; no f(t), no posted holds, no intervention, no ifs in the law.

## Rows
| R# | claim (ONE-A) | label | evidence | ONE-B mark |
|----|---------------|-------|----------|------------|
| R1 | ONE v1 = one_system(): default_system() [hands ON + FIX-i + GRAV-FIX A] + block "cosmic" (WIND hand Th, CC-A L-Theta matter M1/M2, static Born loads Lp/Lm, matched shared-remainder pair dp/dm). ONE tensor: G 382, 18,592 monomials, rank 4, ONE odd Q = 2^33 + 1, every monomial B3-local, b-only cosmic block, 736 designations (706 package + 30 cosmic, each with a reason). Package part = default_system() exactly (dynamics fingerprint b51d3f2c...). | THEOREM (construction) + NUMERIC | runs/T1T2.json (T1a, T1b); layers/one.py | |
| R2 | ONE v1 is BLOCK-DIAGONAL: 0 monomials read across the package/cosmic boundary. The clock times NOTHING in the package; the package's gears evolve bit-identically to default_system() alone (20/20 updates, L = 4). | THEOREM + NUMERIC | runs/T1T2.json (T1g); tests O1 | |
| R3 | Theta-reading census (exact integers): NO package sector can be a THEOREM-O (A)-class Theta reader. Max admissible Theta0 if a block's entries are all Theta-scaled: ref (L0) 2, gauge/links/Higgs 2, free Dirac pairs 2^22, chiral W transport 2^13, Wilson-Yukawa 2^12, gwb 2^8, Yukawa on-site 2^6 * 6451 (=> doublet 64), E1 on matter 0 (odd link coefficient g_A = 1); router/exit are load-driven (AGREE_COSMIC C5) and exit would be rank 5. Hence CC-A's own Theta-reading species was added. | THEOREM (exact census) | runs/T1T2.json (T1c), runs/grain_blocks.json, runs/grain_chiral_em.json | |
| R4 | The E1-charged member "matter" cannot be an exact Theta reader at ANY odd Q while E1 is its photon: g_A = 1 on links (g_A/g_phi = hop/Q is fixed), and the exact E1 source of a Theta-dressed current needs Theta x lapse x link x matter = rank 5 (FORBIDDEN). | THEOREM (integer + rank) | runs/grain_chiral_em.json; layers/one.py docstring | |
| R5 | T1 law: vacuum fixed 10 updates (L = 3, 4, 6); rewind exact (random full state L = 3, 4, 5 updates; ONE seed L = 4, 20 updates); stages 3 (acyclic a-reads); Q odd; reciprocity check passes (non-reciprocal entries all designated). | NUMERIC | runs/T1T2.json | |
| R6 | T2: observe.seed.r_star_hands_on (unmodified) already acts on the cosmic gears by its default Mp + inversion; the ONE seed is R*-fixed (hand at rest with r = 3Q - 1, packet b(x) = a(c2 - x), loads p(c2 - x) = p(x), tokens tok(c2 - x) = R'(tok(x))). X(s0) = s0 and X F^t s0 = F^-t s0 for t = 1..10, 0 mismatches, L = 4 and 6, J-pure (c2 = 0) and S2* (c2 = (0,1,0)). | NUMERIC + DERIVED (Mp is a reversor of every b-only block) | runs/T1T2.json (T2) | |
| R7 | Amendment A1 (pre-run): pair u = c I b_L with b_Lp + b_Lm = 3Q/c, c = 1809 (smallest divisor of 3Q with D * 3Q/c < 2^60): K+ - K- = D I exactly; Born probability p/S_L, S_L = 14,245,331. CC-A/CC-B is c = 3. | THEOREM (identity) | ONE-A_NOTES.md A1; tests O2 | |
| R8 | T3 (L = 6, J-pure norm-matched A_J = 2^12, rng 13): 1200 updates bounded (package max 25 bits), rewind of all 1200 exact; cosmic ledgers 0 failures in 1200 updates (events ell+ - ell- = I, lock r+ = r-, Born N+ = floor((tok + Sum K+)/D), local N_J continuity with link current); Rule3 click ledger D ell = K + r - r' 0 failures / 4,950,720 (every 20th update, all gears); E1 Lorenz 0 failures; E1 dressed local continuity NONZERO (12,744/12,960 nodes: the declared decision-5(A) limitation, not counted). 858 int64 + 342 Python-int steps (exact either way). | NUMERIC | runs/T3_main.json | |
| R9 | T3: the hand turns: board-mean zeros at t = 96.33, 289.17, 481.19, 672.05, 862.75, 1053.99 (pre-registered first zero in [80, 250]: PASS). Bangs RECUR for the Theta readers: 6/6 local minima of the cosmic matter's relative squared seed distance < 0.05 at t = 192, 386, 576, 768, 958, 1150 (0.031, 0.016, 0.047, 0.042, 0.019, 0.022), i.e. at ~2 t_z, as APPROXIMATE echoes. | NUMERIC | runs/T3_main.json | |
| R10 | THEOREM O defects, each separately, at every zero: (a) HOLDS (structural: pair entries read only Theta readers + loads; reader entries = Theta x one reader factor; hand entries odd in Theta, no source); (b) max abs(Delta(t+1) - Delta(t-1)) = 1.16e6 - 1.25e6 at all 216 nodes; (c) abs(board-mean hand at nearest integer)/Theta0 = 2e-4 ... 5.3e-3; (d) copy split/Theta0 = 0.032 ... 0.105. So every later bang is an echo, never exact. | NUMERIC | runs/T3_main.json (zeros) | |
| R11 | The package matter is NOT timed by the hand (R2): its seed distance at the bang times is 0.21, 1.64, 1.32, 1.95, 1.90, 1.63; its run minimum 0.055 at t = 214 is its own dynamics. Pre-registered "> 0.5 at 2 t_z" FAILED at bang 1 only (0.21: a coincidence; decoupling is bit-exact). | NUMERIC | runs/T3_main.json | |
| R12 | T4 records: Born ledger exact per pair; max abs(N+/(N+ + N-) - p/S_L) = 3.2e-7 over all 216 nodes (each >= 1e4 events; 2.66e9 events in total); aeons (between echoes) ~190 updates; pair-outcome entries differing from the previous aeon 99.5 - 99.6 %; outcome zlib per aeon 79 - 81 kB (flat); click rates per 50-update window flat (cosmic matter ~2.0e4, package official ~1.727e5). | NUMERIC | runs/T3_main.json (aeon_stats, windows, born) | |
| R13 | T4 outcome independence: re-run with rng 7 (tokens AND loads): the hand + cosmic matter, Delta and EVERY package gear are bit-identical at 1200/1200 updates; same zeros and bangs; the pair outcomes differ in 98.2 % of entries (98.65 % of lit entries). Cause: Delta(t+1) + Delta(t-1) = ell+ - ell- = I. | NUMERIC + DERIVED | runs/T4_compare.json, runs/T4_rng7.json | |
| R14 | Owner rule: demos/one/run_one.forward is the whole run loop and contains only engine.step (AST test); its states equal Engine.run; measurement functions leave every state unchanged (hash test). | NUMERIC (test O7) | tests/test_one.py; runs/test_one.log (9/9 OK, 7.2 s) | |
| R15 | FIX-i applied to the package default (owner decision v8-1, authorised single edit): layers/electroweak.py sha 58ffc050... -> 9faee4a7...; default dynamics fingerprint 473b7b9f... -> b51d3f2c... (= STAB-B FIX_S_built); package tests: in place 81 ran, 0 FAIL, 1 expected failure, 9 import errors (relative imports under discover without -t); those 9 modules run in the mirror: 46 OK, 2 skipped. | NUMERIC | fixi_sha_*.txt, fixi_fp_*.json, pkg_tests.log, pkg_tests_rel9_mirror.log | |
| R16 | COUPLING OPTION (NEW LAW candidate, default OFF; manager 15:06): one_system(couple_doublet=True) multiplies the doublet's FIRST-ORDER potential (matter, matter2, chiral entries touching matter, gwb) by the hand as ONE common factor (link-averaged), E1 not scaled; Theta0 = 64 (exact grain), h = 2^25. Law: rank 4, 27,040 monomials, 17,856 designations, vacuum fixed, rewind exact, R* 0 mismatches t = 1..10 (L = 4, both seeds). Bang result C1: see addendum. | THEOREM (grain) + NUMERIC | runs/coupled_check.json; ONE-A_NOTES.md A2 | |
| R17 | NOT in ONE (reasons in NOTES_one.md): zero-time hold (posted schedule: forbidden by the owner rule; tensor generation OPEN); gate composed with folding (breaks THEOREM O (a)); Pauli copies / three families (families hook raises); route B (hook route_b: EW-BUILDER verified one_system(route_b=True) composes exactly, G 444); FIX-C+ (tuned counter-terms); cosmic matter <-> lapse (legal at rank 4, OPEN). | DERIVED | NOTES_one.md; layers/one.py | |

## ONE-A addenda (appended as results arrive)

### ONE-A addendum A-1 (Tue Nov 10 15:18:54 UTC 2026): corrections accepted from ONE-B's advance notice (15:16), and new evidence
- R8 CORRECTION (accepted): the pre-registered "every update int64" FAILED: T3 858/1200 int64 steps (342 on Python ints), C1 1160/1200
  (ONE-B's own c = 3 build: 0/1500). Exactness is unaffected (the engine switches to Python ints by an exact bound).
- R11 NOTE (accepted): the package's own near-recurrences (ONE-A 0.055 at t = 214; ONE-B 0.073 at t = 420) are its own dynamics.
- R15 NOTE: relative to ONE-A's backup taken 14:45:30 (just before the in-place run 14:45:52 - 14:55:49), results/ now differs only in
  system/L0C_clock.json and system/e1_without_gravity.json, both rewritten at 15:03:59 by ANOTHER process (stamp_utc back to
  11:53:12: older RC1 versions; the only non-time diff is NaN != NaN), plus 11 NEW electroweak_b/*.json (EW-BUILDER). ONE-A does not
  write results/ (manager whitelist); any restore is the manager's / REV-VERIFY's call. Evidence: results_diff_after_inplace_tests.json.
- R16 QUALIFIERS (accepted): Theta0 = 64 is below the manager's 2^8 bar; the quantized hand's copy split (d) is 0.19 - 0.94 Theta0 in
  C1; "matter" is NOT (A)-class (E1 unscaled); E1's source still reads the UNSCALED exact hopping current while matter's transport is
  Theta-bar-scaled, so E1's current matching gets an extra (1 - Theta-bar) div(f j) residual, O(1) near the turns (ONE-B measuring).
- R16 C1 RESULT (pre-registered A2; runs/C1_coupled.json): bounded 1200 updates (24 bits), rewind of 1200 exact, cosmic ledgers 0,
  click ledger 0/4.95e6, Lorenz 0; hand zeros 95.90, 289.20, 480.75, 672.74, 864.50, 1054.24; cosmic echoes 0.0097 @192, 0.0090 @386,
  0.042 @576, 0.0175 @770, 0.043 @1150; PACKAGE MATTER echoes 0.038 @192 and 0.037 @386 (uncoupled T3 at those times: 0.21, 1.64),
  then 0.20 @576, 0.16 @770, 0.52 @1150 (approximate, decaying). Pre-registered P1 - P5: PASS.
- R16 C1b (pre-registered A3; runs/C1_vs_C1b_compare.json): coupled run with rng 7 (tokens + loads): hand + cosmic matter, Delta and
  EVERY package gear (now Theta-coupled) bit-identical at 1200/1200 updates; outcomes differ 98.1 % (98.6 % of lit). PASS.
- NEW R16b: local SU(2) Noether with a random NON-uniform hand (L = 3, 3 updates, ChiralView as in EW5b): t3 0/81 failures both
  uncoupled and coupled; t1, t2 54/81 in both (the known E1 limitation). The coupling keeps the exact t3 Gauss law. runs/noether_coupled.json.
- REV-ARCH declarations (15:17) added to NOTES_one.md: the time scale is an INPUT (g_w by CC-A's rule: period and aeon length are
  checked, not predicted); no-signalling is law-preserved and seed-initiated (matched seed sector b_Lp + b_Lm = S_L, r_dp = r_dm);
  Born weights are seed data (the ledger verifies the mechanism).

### ONE-A addendum A-2 (Tue Nov 10 15:26:03 UTC 2026): OWNER DECISIONS (manager 15:40) folded in; success re-stated in the owner's terms
- (1) RANK 4 final: ONE v1 and the coupling option are rank 4 (R1, R16). (3) No freeze: ONE has no hold/freeze (R17).
- (2) Bangs do NOT return to the seed; each bang starts with a NEW seed (the state at the turn with all its records); information
  is never lost (exact bijection). Echo distances (R9, R16 C1) are kept as DATA; the pre-registered echo criteria are SUPERSEDED as
  criteria (not counted as passes or failures).
| R# | claim (ONE-A) | label | evidence | ONE-B mark |
|----|---------------|-------|----------|------------|
| R18 | EXACT REWIND ACROSS EVERY BANG: T3's 1200-update rewind (6 turns) returns the initial state bit for bit; C1 (coupled) the same. | NUMERIC | runs/T3_main.json, runs/C1_coupled.json | |
| R19 | TURN TIMES (hand zeros, nearest integer): T3 96, 289, 481, 672, 863, 1054; C1 96, 289, 481, 673, 864, 1054. The ~192-update period is an INPUT (g_w by CC-A's rule), checked not predicted. | NUMERIC | runs/T3_main_turn_seeds.json, runs/C1_coupled_turn_seeds.json | |
| R20 | NEW SEED PER BANG: each turn state differs from the previous one by ~2.28e8 new choices and ~80.4 - 81.1 kB of new incompressible outcome record; 99.6 - 99.8 % of outcome entries differ from the previous interval; the cumulative record grows linearly (39.6, 118.9, 198.3, 278.0, 357.9, 437.9 kB); all turn states are distinct (full-state hashes). C1: same within 1 %. | NUMERIC | runs/*_turn_seeds.json | |
| R21 | COMPLEXITY PER AEON is flat (~80 kB new per ~192 updates; click rates flat per window), and the history (hand, matter, package) is independent of the outcomes (R13, C1b). | NUMERIC | R12, R13, A-1 | |

### ONE-A addendum A-3 (Tue Nov 10 15:26:40 UTC 2026): C2 (pre-registered A3, 15:13:58)
| R# | claim (ONE-A) | label | evidence | ONE-B mark |
|----|---------------|-------|----------|------------|
| R22 | C2 = coupling option with Theta0 = 256, made integral by the package mass 4916 * 2^22 (Yukawa grain 2^8 * 1613; gwb 2^8): 1200 updates bounded (26 bits), rewind of all 1200 exact, cosmic ledgers 0, click ledger 0/4.95e6, Lorenz 0, Born max dev 2.5e-7; int64 438/1200. Turns 96.33, 290.47, 483.24, 676.57, 868.82, 1061.11; copy split (d) 0.059 - 0.24 Theta0 (C1: 0.19 - 0.94): A3 "smaller split" PASS. Data: package-matter distance 0.025 @200, 0.047 @388, 0.059 @578, 0.18 @776, 0.19 @962, 0.25 @1160; cosmic 0.019, 0.011, 0.011, 0.042, 0.025, 0.026. New record ~80.5 - 81.3 kB per interval, all turn states distinct. The mass change is a package re-parametrisation (owner decision), not the default. | NUMERIC | runs/C2_coupled256.json, runs/C2_coupled256_turn_seeds.json | |
- R15 record note (ONE-B 15:20): my in-place run re-stamped 25 results/*.json (time-only; ONE-B saw them 14:47 - 14:51 against its
  14:36:14 snapshot); a third process restored them byte-equal at 15:03:58. Net now: 2 older-RC1-stamp files + 11 new electroweak_b.
- Label note (REV-ARCH 15:27): rows R18 - R21 and the owner framing of A-2 are POST HOC (owner decision 15:40, after the T3/A2
  results); the pre-registered criteria and their outcomes stay in R8 - R13, R16 and A-1 (including the FAILED int64 prediction).

### ONE-A addendum A-4 (Tue Nov 10 15:29:27 UTC 2026): OWNER APPROVAL of the coupling ("1 yes", manager 15:45) — the DEFAULT is now the COUPLED ONE
| R# | claim (ONE-A) | label | evidence | ONE-B mark |
|----|---------------|-------|----------|------------|
| R23 | one_system() now defaults to couple_doublet ON (route A), Theta0 = 64 at TODAY's mass: its tensor IS C1's (dynamics fingerprint 593753fa..., checked). one_system(couple_doublet=False) IS ONE v1 = T3/T4's tensor (77f6d251..., checked). C2 (Theta0 = 256, mass 4916 * 2^22) stays an OPTION only (mass change not approved). Coupling with route B is not designed (explicit couple_doublet=True with route_b raises; route_b alone gives the uncoupled cosmic block). NOTES_one.md labels it "APPROVED NEW LAW (owner 15:4x UTC): one-way first-order doublet x hand; E1 not scaled; approximate echoes", with the owner framing (new seeds, no information lost, no freeze). | THEOREM (construction) + NUMERIC | layers/one.py; NOTES_one.md | |
| R24 | tests/test_one.py now covers the coupled default: 11/11 OK in 4.5 s (mirror): O1 law (both versions; v1 block-diagonal), O2 params (24 h Theta0 = D - 6), O3 census (v1), O4 vacuum + rewind, O5 cosmic ledgers, O6 R* (J-pure and S2*), O7 run loop = Rule3 only, O8 history independent of outcomes, O9 hooks, O10 coupling (only package -> hand reads, E1 untouched, Theta0 = 128 raises), O11 t3 Noether exact with a random non-uniform hand. | NUMERIC | runs/test_one_coupled_default.log | |

## ONE-B marks (APPENDED by ONE-B; nothing above this line was edited)
**Protocol.** My brief asks for ACCEPT / EDIT / DISAGREE + reason.
- ACCEPT ≡ AGREE.
- EDIT = AGREE + a correction or qualifier.
- CAN'T-CHECK = no independent ONE-B evidence.

**Independence.**
- My pre-registration (s22/ONE-B_NOTES.md §0–§2) closed at 14:45:42 UTC (sha256 5b38ee0e…), before I opened any ONE-A file.
- I rebuilt every ONE tensor from the verbal spec on a private PRE-EDIT pin, with FIX-i applied by me: ONE-B_work/pin, oneb.py,
  coupled_oneb.py.
- My drivers were my own.
- I never wrote into the package: bytecode off; tests ran in private copies.

**Framing.** Marked in the OWNER's framing (manager 15:40):
- Bangs are NEW seeds, not returns. Echo distances are DATA, not criteria.
- The criteria are: exact rewind across bangs, turn times, a new seed per aeon, complexity per aeon, and no freeze.

Evidence paths are relative to s22/ONE-B_work/.

| R# | ONE-B mark | note | ONE-B evidence |
|----|-----------|------|----------------|
| R1 | ACCEPT | v1 f3a6a0aa… and v2 77f6d251… equal MY spec composition (39 cosmic monomials identical). My clock block equals CC-A ib.py bit for bit (L = 5, 300 updates, rewind exact). So WIND = s15 E2; the pairs give K+ − K− = D·I with one shared remainder; the loads read b only | fp_onea*.json, fp_oneb*.json, t_vs_ib.py |
| R2 | ACCEPT (v1/v2) | 0 cross monomials. The package is bit-identical to the package alone (L = 4, 20 updates). SUPERSEDED as the default by the owner's coupling decision (15:45): see OB9 | oneb_t1_*.json |
| R3 | ACCEPT | My own grain code gives the same maxima: matter 0 (E1 ±1 on links), matter2 64, L0 2, links/2-paths/Higgs 2, em 0. Per source into the doublet: own 2^22, gwb 2^8, chiral 2^6 | grain_census.json, route_census.json |
| R4 | ACCEPT + EDIT | The rank-5 part is parameter-free. ADD: Q-scaling (s odd) keeps odd entries odd, and rescaling E1's A by 2^k to make g_A even breaks E1's beta-dressed source coefficient 9 (odd). The wall is robust within e1d | ONE-B_NOTES.md §4.3 |
| R5 | ACCEPT | Mine: vacuum (+Θ0, loads, tokens; no packets) fixed at L = 3, 4 (v1 build, and C1 = new default) and L = 6 (v3, 0 changes in 10 updates). Rewind exact (random L = 3, 4; seed L = 4, 20 updates; v1 and C1). Stages 3. Reciprocity ok (17,738 checked, 118 two-time skipped; non-reciprocal entries all designated) | oneb_t1_*.json, verify_C1.json |
| R6 | ACCEPT | Reproduced, 0 mismatches for t = 1..10: L = 4 (v1 and v2, J-pure and S2*), L = 6 (v2, J-pure and S2*), and C1 (L = 4, both seeds) | onea_t2_*.json, verify_C1.json |
| R7 | ACCEPT | 3Q mod 1809 = 0, S_L = 14,245,331, D·S_L = 2^59.35. Events = I and lock: 0 failures. My v1 (c = 3) run and your v2 (c = 1809) run have IDENTICAL hand/matter histories to every printed digit | T3_L6_r13.json |
| R8 | ACCEPT (with A-1 correction) | Reproduced with MY driver (v1, L = 6, 1500 updates): bounded; 0 ledger failures (events, lock, Δ identity, Rule3 click ledger on all gears every 20th update); Born exact 2.4e-7. "Every update int64" FAILED (A-1). E1 Lorenz: CAN'T-CHECK | T3_L6_r13.json |
| R9 | ACCEPT as DATA | My run reproduces the zeros and echo values exactly. Over 1500 updates: zeros +1245.67, +1437.88 and echo +1342 (0.036). Per the owner, echoes are not criteria | T3_L6_r13.json |
| R10 | ACCEPT (a), (c), (d); CAN'T-CHECK (b) | (a) verified on the monomials; (c), (d) identical in my run. (b) not computed by me (my Δ-identity check: 0 failures) | T3_L6_r13.json |
| R11 | ACCEPT as DATA | Bit-exact decoupling in v1/v2 ⇒ coincidence | — |
| R12 | ACCEPT | Mine (v1): Born exact 2.4e-7 at 216 nodes; 7 aeons, zlib 79.0–81.2 kB each; 99.46–99.7 % of outcome entries new versus the previous aeon | T3_L6_r13.json |
| R13 | ACCEPT | Mine: 0 non-pair mismatches at L = 4 over 150 updates (v1 tokens; v2 tokens + loads); outcomes differ 34 % (tokens only) / 99.3 % (tokens + loads). Plus cross-version v1/v2 identity | oneb_t4_*.json, onea_t4_4_150.json |
| R14 | ACCEPT | Code read (pinned shas): the loop is engine.step only; observers read `.astype` copies; prepare/one never steps. test_one: 11/11 OK in MY private copy (layers/one.py 57de300d…, tests 54f9095e…) | test_one_oneb.log, onea_v*/ |
| R15 | ACCEPT + record | Diff verified against my byte copies (only the gwb kwargs + info record; one NOTES paragraph). b51d3f2c… reproduced from my pre-edit pin. results/ history: OB8 | orig/, census_default.json |
| R16 | ACCEPT + EDIT | Tensor = my rebuild (593753fa…). Grain 64. ADD the E1 mismatch measured: OB5. ADD: Θ0 = 64 < 2^8 bar (owner approved it anyway, 15:45) | coupled_oneb_64.json, e1_mismatch.json |
| R16b | ACCEPT | Reproduced with rng 7: t3 0/81; t1, t2 54/81 (the pre-existing E1 limitation, unchanged by the coupling) | verify_C1.json |
| R17 | ACCEPT | No freeze or hold in the law (owner decision 3) | — |
| R18 | ACCEPT | Mine: the full 1500-update rewind across 8 turns / 7 bangs (v1) is exact | T3_L6_r13.json |
| R19 | ACCEPT (T3); CAN'T-CHECK (C1 run) | My T3 turn times are identical. The period is an INPUT (g_w by CC-A's rule): agreed | T3_L6_r13.json |
| R20 | ACCEPT + EDIT | EDIT the label: "~2.28e8" is the number of '+' outcomes per aeon (N+). The CHOICES per aeon (unit events, ℓ+ − ℓ− = I) number ~4.25e8 (mine 4.17–4.29e8; yours 2.656e9 per 1200 updates). Record growth and % new: reproduced. Turn-state hashes: CAN'T-CHECK | T3_L6_r13.json |
| R21 | ACCEPT | — | T3_L6_r13.json |
| R22 | ACCEPT (tensor, grain); CAN'T-CHECK (run numbers) | C2 tensor = my independent rebuild (3d86d22b…). Doublet non-E1 grain at mass 4916·2^22 = 2^8 (412928 = 2^8·1613; links 512). The mass change needs an owner decision | coupled_oneb_256.json |

### ONE-B rows (APPENDED by ONE-B; ONE-A please mark the last column)
| # | claim (ONE-B) | label | ONE-B evidence | ONE-A mark |
|---|---|---|---|---|
| OB1 | **Owner rule (14:47): PASS.** (i) The loop is Engine.step only, on one fixed tensor. (ii) No f(t), posted hold or run-time write (observers read copies; the driver only stops). (iii) No if/comparison in the law: integer tensor data; `if`s only at construction or in observation. (iv) The seed is data only. (v) No tuned counter-term: FIX-i is lam = 0; g_w is CC-A's design rule; c_pair is a unit choice; Θ-scaling is exact division | DERIVED (code read, pinned shas) + NUMERIC (test_one O7, my run) | onea_v*/, test_one_oneb.log | |
| OB2 | **ONE v1/v2 (uncoupled) is BLOCK-DIAGONAL**: package ⊕ clock, 0 cross monomials. This was the honest verdict before the owner's 15:45 coupling decision | NUMERIC | oneb_t1_*.json | |
| OB3 | **The coupling wall is E1** (not rank, not Q). The E1-charged "matter" can never be an EXACT (A)-class Θ reader with the e1d photon, for three reasons: (1) rank 5 for the lapse-dressed source; (2) g_A·PJp = ±1 on links; (3) A-rescaling breaks the dressed coefficient 9. Coupling the doublet with E1 untouched is the only legal route | THEOREM (integers + rank) + NUMERIC | route_census.json | |
| OB4 | **Mass lever (derived by ONE-B, independently of A3):** y = mass // (2v), so mass 4916·2^22 gives doublet Θ0 = 2^8 at Q = 2^33 + 1. Verified: grain 2^8·1613 on-site, 512 on links; C2 tensor rebuilt = 3d86d22b…. It needs an OWNER decision (changes the approved mass; cos w0 0.39998 → 0.40007) | DERIVED + NUMERIC | coupled_oneb_256.json, quick checks log | |
| OB5 | **E1-source mismatch (manager 15:45), measured.** With the coupling, E1 still sources from the UNSCALED hopping current while the doublet transports with Θ̄. Setup: L = 4, same package seed, 200 updates. Measure: Σ\|dressed-continuity residual\| (the package's observable), coupled ÷ uncoupled. Ratio: 1.00 at t = 2; 12.5 (t = 3); 28 (10); 53 (20); 148 (40); 183 (50); 434 (60); 475 (100, hand −0.98 Θ0); 230 (120); 58 (150); 8.2 (190); 2.6 (200, hand +0.93). The coupling therefore breaks E1's current matching by up to ~475× the hands-ON baseline, tracking (1 − Θ̄/Θ0). It is exact as a map (bijection, rewind exact) but NOT physically coherent for E1 | NUMERIC + DERIVED | e1_mismatch.json, e1_mismatch.py | |
| OB6 | **Coherent ONE at Q = 2^33 + 1 (manager 15:08).** Today's mass, C1 (the owner's choice 15:45): **PASS as a legal, exact ONE** (rank 4, B3, integral, designated, int64 mostly, rewind exact) with a coarse hand (Θ0 = 64 < 2^8 bar: **FAIL on the bar**). Mass 4916·2^22, C2: meets the bar (Θ0 = 2^8), owner decision pending. EXACT coherence (E1 included): **FAIL at any Q** (OB3, OB5) | DERIVED + NUMERIC | OB3–OB5, verify_C1.json | |
| OB7 | **Package tests (ONE-B rerun, fresh private copy, `discover -t .`):** 90 OK, 1 expected failure (TC15, by design), 0 FAIL/ERROR. Modules: chiral, choice (+ oddq, round), core, electroweak, electroweak_b, em, em_compact, gauge, gravity, gravity_hybrid. I STOPPED it in test_l0c to free the core for the 15:45 verification (1-core rule). Not rerun by me: l0c, layers, onematter, seed, stage01/02, stage02_review, system, universality (ONE-A: 46 OK in its mirror). test_one 11/11 OK (separate run) | NUMERIC | pkg_tests_oneb2.log, test_one_oneb.log | |
| OB8 | **results/ history (record, not ONE-A's error).** 25 time-only rewrites at 14:46–14:55 (ONE-A's in-place tests). They were restored byte-equal at 15:03:58 by a third process, which also wrote 2 system files with older RC1 stamps (time/NaN-only diffs). Net now: those 2 + 11 new electroweak_b files | NUMERIC | audit_files_*.json | |
| OB9 | **Default switch (manager 15:45) VERIFIED.** one_system() → dyn_fp 593753fa… = MY independent rebuild of C1. Rank 4; 27,040 monomials; 17,856 designations. Degree-3: 18,254, of which the 1,528 NON-designated are exactly the pre-existing OD4 springs (su2 48, su3 1404, u1 12, wsu2 48, chiral 16); all others are designated (rank-4 kind rule holds). 17,120 package terms read Θ, all designated (the only undesignated Θ reads are the hand's own 7); E1 reads Θ nowhere. Vacuum L = 3/4 fixed; rewind exact; R* L = 4 J-pure/S2* 0 mismatches; t3 Noether 0/81 | NUMERIC | verify_C1.json | |
| OB10 | **The owner's criteria (15:40) are met**, by ONE v1/v2 (my own runs) and by C1 (my tensor checks + ONE-A's run): exact rewind across bangs, turn times, a new seed per aeon (≈4.25e8 new choices, ≈80 kB of new incompressible record, ≥ 99.4 % new entries), flat complexity per aeon, and no freeze (no hold term; the clicks are the pair events EXECUTED by the Θ-reading light's intensity, the outcome chosen by the shared remainder). These criteria are POST HOC (owner 15:40), not pre-registered | NUMERIC (POST HOC framing) | T3_L6_r13.json | |

**ONE-B SIGNS** all marks above (ACCEPT on R1–R3, R5–R7, R11–R14, R16b, R17, R18, R21; ACCEPT with EDIT/record on R4, R8, R15, R16, R20; partial CAN'T-CHECK on R10 (b), R19 (C1), R22 (run numbers); **no DISAGREE**) and rows OB1–OB10: Tue Nov 10 15:29:47 UTC 2026 (date -u). Appended to a file whose first 15877 bytes (sha256 prefix 93df0eeb71e79605) are unchanged.

### ONE-B marks on ONE-A addendum A-4 (appended Tue Nov 10 15:30:15 UTC 2026; A-4 was appended at 15:29:27, between my 15:28:17 read and my 15:29:47 append)
| R# | ONE-B mark | note | ONE-B evidence |
|----|-----------|------|----------------|
| R23 | ACCEPT + EDIT | Verified independently (OB9): one_system() = 593753fa… = my rebuild of C1; couple_doublet=False = 77f6d251… = my composition with c_pair = 1809. EDIT (naming): 77f6d251… is the A1 build (c = 1809, used by T3/T4); the 14:54 c = 3 build was f3a6a0aa… (R1). Their hand, matter and package histories are identical (R7) | verify_C1.json, fp_onea_v2.json, fp_oneb_v2.json |
| R24 | ACCEPT | test_one 11/11 OK in MY private copy of the live package (layers/one.py 57de300d…, tests/test_one.py 54f9095e…), 3.96 s | test_one_oneb.log |

**ONE-B RE-SIGNS** every mark (R1–R24, no DISAGREE) and rows OB1–OB10: Tue Nov 10 15:30:15 UTC 2026 (date -u). Append-only: the first 26912 bytes (sha256 prefix c2175fa4277e9fbd) are unchanged.

### ONE-A marks on OB1 - OB10 (APPENDED by ONE-A Tue Nov 10 15:30:26 UTC 2026; nothing above this line edited)
| # | ONE-A mark | note |
|---|---|---|
| OB1 | ACCEPT | Owner rule PASS: the loop is Engine.step only; ifs only at construction/observation; seed = data; no tuned counter-term. |
| OB2 | ACCEPT | v1/v2 block-diagonal was the verdict before the owner's 15:45 coupling decision; it remains the couple_doublet=False version. |
| OB3 | ACCEPT | The wall is E1 (rank 5 for the dressed source; g_A = +-1 on links; the A-rescaling breaks the odd dressed coefficient 9). Coupling the doublet with E1 untouched is the only legal route. |
| OB4 | ACCEPT | Independent derivation of the mass lever (= A3). The mass change needs an owner decision; C2 stays an OPTION. |
| OB5 | ACCEPT (important) | The coupled default breaks E1's current matching by up to ~475x the hands-ON baseline, tracking (1 - Theta-bar). The map stays exact (bijection, rewind), but E1 is NOT physically coherent with the Theta-scaled doublet. This is the main physical cost of the approved coupling; it must go to the owner with the default. |
| OB6 | ACCEPT | C1: legal and exact, FAILS the 2^8 bar (Theta0 = 64); C2 meets the bar (owner decision on the mass pending); exact coherence including E1: impossible at any Q. |
| OB7 | ACCEPT | ONE-B's private rerun (90 OK, 1 expected failure, 0 FAIL/ERROR, stopped in test_l0c) plus my mirror run of the 9 relative-import modules (46 OK, 2 skipped) plus the in-place run (81, 0 FAIL, 9 import errors) together cover the suite after FIX-i with 0 failures. |
| OB8 | ACCEPT | Record as stated (25 time-only rewrites by my in-place run 14:46 - 14:55, restored byte-equal 15:03:58 by a third process). |
| OB9 | ACCEPT | Default switch verified independently (593753fa...; the 1,528 undesignated degree-3 entries are exactly the pre-existing OD4 springs). |
| OB10 | ACCEPT + EDIT | With ONE-B's R20 correction: per aeon ~4.25e8 unit CHOICES (events, ell+ - ell- = I) and ~2.28e8 "+" outcomes; NOTES_one.md (frozen 15:29:27) calls the latter "new choices (pair '+' outcomes per interval)": read "choices" there as "+" outcomes. POST HOC framing, as labelled. |
- ONE-A ACCEPTS ONE-B's EDITs on R4 (E1 wall robust within e1d), R8 (int64 FAILED), R15 (record), R16 (E1 mismatch OB5; bar), R20 (choices vs '+' outcomes) and the CAN'T-CHECK notes on R10 (b), R19 (C1), R22 (run numbers: runs/C2_coupled256.json).
- **ONE-A SIGNS rows R1 - R24 (as amended by A-1 - A-4) and its marks on OB1 - OB10: Tue Nov 10 15:30:26 UTC 2026 (date -u). No DISAGREE on either side.**
- ONE-A ACCEPTS ONE-B's R23 naming EDIT (appended 15:30:15, seen after my 15:30:26 signature): 77f6d251... is the A1 build (c_pair = 1809, uncoupled, = T3/T4); f3a6a0aa... was the c = 3 build. 'ONE v1' in my rows means the uncoupled version as built after A1. Signature unchanged: Tue Nov 10 15:31:37 UTC 2026 (date -u).
