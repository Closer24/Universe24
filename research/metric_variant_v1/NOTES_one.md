# NOTES_one — ONE (Study 22): one tensor, one Q, one seed, one run, with the cosmic clock
Builder ONE-A, Tue Nov 10 2026 (UTC). Verifier ONE-B (append-only marks in scratchpad s22/AGREE_ONE.md).
Pre-registration: scratchpad s22/ONE-A_NOTES.md §2 (14:49:43 UTC), amendments A1 (pair load scale, before any run of T1-T4) and
A2 (coupling option, 15:10:24, before its bang). Evidence: scratchpad s22/ONE-A_work/runs/. All runs in a scratch mirror.
Labels: THEOREM / DERIVED / NUMERIC / POST HOC / OPEN / NEW LAW (owner decision).
Time-stamp note (manager, doc only, 2026-11-10): the stamps "manager 15:40", "manager 15:45" and "owner 15:4x UTC" in this
package are the manager's relay stamps, which ran ahead of the clock. By `date -u` the owner's decisions arrived at 15:24:47 UTC
(rank 4 final; each bang starts a new seed; no freeze) and at 15:26:41 UTC (couple the clock to the doublet; light route A; git
via a branch and a PR). The decisions themselves are as stated.

**OWNER RULE (binding, manager 14:47 UTC): no forcing, no faking, no hand-placed schedules. ONE is only the fixed tensor + the
seed (initial data) + Rule3. There is no prescribed f(t), no posted hold, no run-time intervention and no comparison or branch in
the law. Every measurement is read-only. tests/test_one.py O7 checks that the run loop (demos/one/run_one.forward) does nothing
but call Engine.step on the composed tensor.**

**OWNER DECISIONS (manager 15:40 UTC), folded in (POST HOC: owner decision after the T3/A2 results; the pre-registered criteria and their outcomes stay in §6 and AGREE_ONE):** (1) RANK 4 is final: ONE is rank 4 and solves everything with it.
(2) Bangs are NOT supposed to return to the seed: each bang STARTS WITH A NEW SEED, the state at the turn with all its records;
information is never lost because Rule3 on one tensor is an exact bijection. Success is therefore reported as: exact rewind
across every bang; the turn times; how each new seed differs from the previous one (record growth, new choices); complexity per
aeon. Echo distances are kept as DATA only; a non-return is not a failure (the pre-registered echo criteria of T3 / A2 are
superseded as criteria). (3) There is NO freeze on the board: light executes the clicks and only the chosen path produces a
click. ONE contains no hold and no freeze (the zero-time hold is excluded, §7).
**ONE results in the owner's terms (POST HOC framing of NUMERIC data; T3, L = 6, J-pure, 1200 updates; runs/T3_main_turn_seeds.json):**
- Exact rewind across EVERY bang: the rewind of all 1200 updates (6 turns) returns the initial state bit for bit (also C1 and
  C2, both coupled).
- Turn times (hand zeros, nearest integer): 96, 289, 481, 672, 863, 1054 (period ~192 by design, declaration 1 below).
- Each new seed (the full state at a turn) differs from the previous one by ~2.28e8 new choices (pair "+" outcomes per interval)
  and ~80.4 - 81.1 kB of new incompressible outcome record; 99.6 - 99.8 % of the outcome entries differ from the previous
  interval; the cumulative record grows linearly: 39.6, 118.9, 198.3, 278.0, 357.9, 437.9 kB; all turn states are distinct.
- Complexity per aeon is flat (~80 kB new record per ~192 updates), while the coarse state passes near its earlier forms
  (data: cosmic-matter distances 0.016 - 0.047 near 2 t_z).
- Same picture with the package coupled (C1, Theta0 = 64): turns 96, 289, 481, 673, 864, 1054; ~80.1 - 80.8 kB new record per
  interval; cumulative 39.5 to 437.8 kB.

**Three declarations (REV-ARCH 15:17, so that nothing reads as circular):**
1. **The time scale is an INPUT.** g_w = 1310 was chosen by CC-A's rule for a target quarter period Tq = 100 at L = 6,
   A_c = 2^10. So the hand's turning (zeros at 96.3, 289.2, ...; period ~385 updates) and the aeon length (~192 updates) are
   set by design. T3 checks them; it does not predict them. Likewise h is matched to Theta0 (24 h Theta0 = D - 6), and
   c = 1809 is an int64 convenience (exactness does not need it: c = 3 is exact too, on Python ints).
2. **No-signalling holds in the matched seed sector: law-preserved, seed-initiated.** Outcome independence (T4, test O8) is
   exact because the seed sets b_Lp + b_Lm = S_L and r_dp = r_dm, and the law preserves both: the loads are static, and
   r+ - r- is invariant since K+ - K- = D I. A seed outside this sector would let outcomes (tokens) enter Delta, and hence
   Theta.
3. **Born weights are seed data.** p/S_L is put in by the loads; the Born ledger (max deviation 3.2e-7) verifies the
   mechanism. It does not derive the probabilities.
- Scale of the coupling (§4; opt-in only, REJECTED by the owner): 27,040 monomials and 17,856 designations, against 18,592 and 736 in ONE v1. That is how
  far reciprocity is given up there (every Theta-scaled entry is one-way).

**THE DEFAULT (owner decision received about 16:13 UTC, `date -u`: matter must NOT read the cosmic clock; Study 33 switch):**
one_system() is ONE v1 (couple_doublet=False), the block-diagonal version on which T1 - T4 were pre-registered and run (dynamics
fingerprint 77f6d251...). Bangs start NEW seeds, information is never lost (exact bijection), there is no freeze. The coupled
build C1 (one-way first-order doublet x hand; E1 not scaled; approximate echoes; dynamics fingerprint 593753fa...) is an explicit
opt-in only, couple_doublet=True: **NEW LAW candidate, REJECTED by the owner (matter must not read the clock); measured
runaway at L = 6 t ≈ 1,547–1,554 and L = 4 t ≈ 662 (Study 30); kept for the record** (§4). It had been approved at 15:26:41 UTC
("owner 15:4x UTC" in earlier text). Option C2 (Theta0 = 256 with the package mass 4916 * 2^22) is a coupled doublet too and
stays unapproved.

## 1. What ONE is (layers/one.py: one_system)
ONE v1 = default_system(Q) + block "cosmic", at ONE odd Q = 2^33 + 1 (D = 6Q), on ONE periodic L^3 cube with six faces.
- Package part: hands ON (chiral + electroweak, OWNER decision 5), **FIX-i** (OWNER decision v8-1: build_graviweak_b(lam_H = 0,
  lam_L = 0), singlet-half hop kept; applied to the package default by the single authorised edit of layers/electroweak.py), and
  GRAV-FIX A (beta detuned; already the default). Its tensor is bit-identical to default_system() (dynamics fingerprint
  b51d3f2c...).
- Cosmic block (NEW LAW, OWNER decision 8 "WIND"), 7 gears per node:

| gear | input u (K = 2u) | rank | role |
|---|---|---|---|
| Th | (D - 6 kTh) b_Th + kTh Sum_6 b_Th(y) - g_w (b_dp - b_dm) b_Th | 3 | the hand: WIND law, no bare spring, rigid face coupling |
| M1, M2 | h Sum_{y~x} (b_Th(x) + b_Th(y)) b_Mj(y) | 3 | CC-A's complex first-order matter, the ONLY Theta readers (L-Theta) |
| Lp, Lm | D b_L | 2 | static Born loads (initial data p, S_L - p) |
| dp, dm | +-c (b_M1^2 + b_M2^2) b_L+- | 4 | matched shared-remainder choice pair (narrow kind: singlet x abs(psi)^2) |

  K+ - K- = 2c I (b_Lp + b_Lm) = D I with b_Lp + b_Lm = S_L = 3Q/c: exactly I unit choices per update and node; r+ - r- invariant;
  N+ = floor((tok + Sum K+)/D). c = 1809, S_L = 14,245,331 (smallest divisor of 3Q with D S_L < 2^60: int64; CC-A used c = 3).
  Theta0 = 2^24 (seed scale), h = 2^7 (24 h Theta0 = D - 6: inside the band), kTh = 2^32 (2 kTh/D = 1/6), g_w = 1310 (CC-A's
  pre-registered rule at L = 6, quarter period 100). 30 designated one-way entries (the hand reads Delta; readers read the hand;
  the pair reads readers and loads), each one-way BY THEOREM O (no source on the hand; pair load only from readers).
- Seed (prepare/one.py, data only): J-pure (norm-matched as in s17E emerge_run) or S2* package bang; the hand at rest at Theta0
  INCLUDING the remainder 3Q - 1; CC-A's neutral packet A_c = 2^10; static loads; tokens. All R*-fixed about the bang centre.
- Hooks: route_b (ONE v2: EW-BUILDER's compose_electroweak_b on the hands-OFF base; EW-BUILDER verified one_system(route_b=True)
  composes exactly, G 444), families (ONE v3: raises), couple_doublet (§4: opt-in only, a NEW LAW candidate REJECTED by
  the owner; the default couple_doublet=False is ONE v1).

## 2. Rank census
- Package: rank 4 (OD4 springs, E1's dressed source, chiral entries, 706 designations). Cosmic: hand 3, readers 3, pair 4 (the
  approved NARROW kind: uncharged singlet b_L x covariant composite abs(psi)^2), loads 2. ONE: G 382, 18,592 monomials, rank 4.
- Theta x lapse x link x matter = rank 5: FORBIDDEN, and never built.

## 3. Who reads Theta (theta_reading_census; exact integers)
A THEOREM-O (A)-class reader needs EVERY input = Theta x (odd in the readers), with the package's own coefficients recovered at
Theta = Theta0: on-site coefficients divisible by Theta0 and link ones by 2 Theta0 (link-averaged factor).

| package sector | max Theta0 | other obstruction | reads Theta? |
|---|---|---|---|
| L0 (ref) | 2 | - | no (grain) |
| matter (E1-charged Dirac pair) | 0 | E1 link coefficient g_A = 1; exact E1 source of a Theta-dressed current = rank 5 | no, at ANY Q while E1 is its photon |
| matter2 + chiral couplings | 64 (Yukawa on-site 2^6 * 6451) | SU(2) ties it to matter | no (grain) |
| gauge links, Higgs, 2-paths, E1 fields, lapse, beta, background, choice rings | 2 or second-order | THEOREM O class (C) | no |
| router, exit | - | load-driven (AGREE_COSMIC C5); exit rank 5 | no |

So ONE v1 uses CC-A's own Theta-reading species (M1, M2) in the same tensor, stated plainly. **ONE v1 is BLOCK-DIAGONAL**: 0
monomials cross the package/cosmic boundary; the package evolves bit-identically to default_system() alone. **The sectors that
do NOT read Theta (and do not fold): every package sector** — L0, both Dirac pairs, weak links, Higgs, gauge sectors (su2, su3,
u1), E1, gravity (metric, beta, background), the choice observers.

## 4. The coupling: NEW LAW candidate, REJECTED by the owner; opt-in only, DEFAULT OFF (Study 33)
**Status:** NEW LAW candidate, REJECTED by the owner (matter must not read the clock); measured runaway at L = 6
t ≈ 1,547–1,554 and L = 4 t ≈ 662 (Study 30); kept for the record. Times by `date -u`: the owner decisions were received at
15:24:47 and 15:26:41 UTC (the coupling was approved in the second; "owner 15:4x UTC" in earlier text was a relay stamp) and
the rejection at about 16:13 UTC. one_system() is ONE v1 (couple_doublet=False, 77f6d251...). couple_doublet=True
(run_one --couple) still builds C1 bit for bit: dynamics fingerprint 593753fa... (pinned by tests/test_one.py O12) and
canonical fingerprint 1a3f998e..., both unchanged.
one_system(couple_doublet=True) (opt-in only; not designed for route B): the doublet's FIRST-ORDER potential (blocks matter, matter2, the chiral entries touching
matter, gwb) is multiplied by the hand as ONE common factor (theta_scale_block; link-averaged on link entries; designated
one-way, no hand source); E1 is NOT scaled; second-order self terms (Higgs inertia/spring, links) are NOT scaled (no inverted
oscillator at Theta < 0). Only Theta0 <= 64 is integral at today's constants. Law checks: rank 4, 27,040 monomials, vacuum,
rewind, R* exact (L = 3/4). Larger Theta0 needs a re-parametrised package: mass m 2^22 with 4 | m gives Theta0 = 2^8 (FIX-i's
gwb caps it there); a larger Q only helps if every matter constant is re-derived with it (not done).
**Result C1 (L = 6, J-pure, Theta0 = 64; pre-registered A2): the PACKAGE bang recurs approximately** — the package matter's seed
distance is 0.038 at t = 192 and 0.037 at t = 386 (uncoupled T3 at the same times: 0.21 and 1.64), then 0.20, 0.16, 0.52;
cosmic echoes 0.0097, 0.0090, 0.042, 0.0175, 0.043; bounded 24 bits, rewind of 1200 exact, all ledgers 0 failures. The echoes
are approximate and degrade: E1 (on "matter") and the (C) fields are not time-reversed, and the 64-level hand splits by
0.2 - 0.9 Theta0 at its zeros. The coupled build is exact as a map, but it is NOT the default (status above); ONE v1
(couple_doublet=False) is the default and block-diagonal.

**Measured runaway (Study 30; NUMERIC, ONE-LONG, signed 16:10 UTC; research record s30/runs/, a scratchpad path, not a
repository file):** C1 with the J-pure seed is bounded for 1,200 updates at L = 6 (rng 1, 2, 3: max 24 bits), then runs away at
t ≈ 1,547–1,554 (rng 13: 433 bits at t = 1,554, where run_one's 200-bit guard stops the driver); at L = 4 it runs away at
t ≈ 662. The chiral/Higgs sector grows first. The rewind stays exact (all 1,554 updates at L = 6, all 667 at L = 4) and the
cosmic ledgers report 0 failures at L = 6: the map is still a bijection, and the runaway is growth of the integers, not a loss of
information. ONE v1 does not run away in the same tests: L = 4 to t = 720; L = 6 to t = 2,600+ with 27 bits (the run continues),
though its uniform lapse drifts as t^2 (OPEN).
- OPEN (Study 34, s34/): a generic replacement through the clocks only.

- **Cost of the coupling (ONE-B OB5, measured; manager doc edit 2026-11-10, post-freeze, doc only):** E1 is not scaled and sources
  from the unscaled hopping current, so its dressed-continuity residual grows up to ~475x the hands-ON baseline (L = 4, 200 updates),
  tracking (1 − Θ̄); the map stays exact (bijection, rewind), but E1 is not physically coherent with the Θ-scaled doublet (OPEN).
  The hand grain Θ0 = 64 is below the 2^8 bar (ONE-B OB6); C2 (mass 4916·2^22, Θ0 = 256) is an option needing an owner decision.

## 5. NEW LAW list (owner decisions)
1. WIND hand (decision 8). 2. L-Theta readers = CC-A's species. 3. Matched pairs loaded by the readers' abs(psi)^2 (narrow kind,
decision 4). 4. The Theta-coupled doublet (§4): approved 15:26:41 UTC, then REJECTED by the owner (about 16:13 UTC, `date -u`);
not a law of ONE, opt-in only, kept for the record. FIX-i is a coefficient choice, not a new law.

## 6. Results (pre-registered T1-T4; NUMERIC unless stated)
- T1 PASS: rank 4, B3, Q odd, designations 706 + 30, vacuum fixed (L = 3, 4, 6), rewind exact, decoupling bit-exact.
- T2 PASS: r_star_hands_on (unmodified) extends by its default Mp + inversion; 0 mismatches t = 1..10, L = 4 and 6, J-pure and S2*.
- T3 PASS (L = 6, J-pure, 1200 updates, rewind exact, max 25 bits): cosmic ledgers 0/1200; Rule3 click ledger 0/4.95e6;
  Lorenz 0; hand zeros 96.3, 289.2, 481.2, 672.1, 862.8, 1054.0; 6/6 cosmic echoes < 0.05 at ~2 t_z (0.016 - 0.047). THEOREM O
  (a) holds; (b) 1.2e6 at all nodes; (c) <= 5.3e-3 Theta0; (d) split 0.03 - 0.11 Theta0: echoes approximate. Package matter: not
  timed (distance 0.21 at the first bang by coincidence, 1.3 - 1.95 later).
- T4 PASS: Born max deviation 3.2e-7; 99.5 % new outcomes per aeon; flat records; history bit-identical across token/load seeds
  (1200/1200 updates) while 98.2 % of outcomes differ.
- Coupling option (A2/A3): C1 in §4. C1b (rng 7): with the package COUPLED, the hand, the cosmic matter, Delta and every package
  gear are still bit-identical across token/load seeds (1200/1200 updates) while 98.1 % of outcomes differ. Local SU(2) Noether
  with a random non-uniform hand (L = 3): t3 exact (0/81) coupled and uncoupled; t1, t2 broken equally (the E1 limitation).
  Pre-registered "every update int64" FAILED (T3 858/1200, C1 1160/1200, C2 438/1200; exactness unaffected).
  C2 (Theta0 = 256, made integral by the package mass 4916 * 2^22 instead of 4915 * 2^22; pre-registered A3): 1200 updates bounded
  (26 bits), rewind of 1200 exact, all ledgers 0; turns 96, 290, 483, 677, 869, 1061; copy split 0.06 - 0.24 Theta0 (C1: 0.19 -
  0.94); data: package-matter distance 0.025 @200, 0.047 @388, 0.059 @578, then 0.18 - 0.25; cosmic 0.011 - 0.042; ~80.5 - 81.3 kB
  new record per interval. The mass change (cos w0 0.39998 -> 0.40006) is a package re-parametrisation for the owner, not done in
  the default.

## 7. NOT in ONE, and why
- Zero-time hold: a posted schedule (forbidden by the owner rule); its tensor generation is OPEN.
- Confirmation gate composed with folding: light-gated pairs read by the hand break THEOREM O (a); OPEN.
- Pauli copies / three families / configuration space: NEW LAWs not approved (families hook raises).
- Route B: EW-BUILDER's build (frozen 15:06:51), reachable by route_b=True, OFF by default.
- FIX-C+: two tuned lapse counter-terms; tuned counter-terms are not solutions (owner rule).
- Cosmic matter <-> lapse (universality for the readers): legal at rank 4 (Theta x F x b' is narrow) but a (C)-field defect; OPEN.
- The Theta-coupled doublet (matter reads the clock): NEW LAW candidate, REJECTED by the owner (matter must not read the
  clock); measured runaway at L = 6 t ≈ 1,547–1,554 and L = 4 t ≈ 662 (Study 30); kept for the record, as the opt-in
  couple_doublet=True (§4).
