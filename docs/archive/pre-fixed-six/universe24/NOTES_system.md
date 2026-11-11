# NOTES_system — INTEGRATOR (ex B1-GAUGE): the composed DEFAULT SYSTEM at ONE odd Q

All stamps are `date -u`. Pre-registrations come BEFORE the runs; results are appended, never edited into them. Every
layer is imported READ-ONLY; nothing in another builder's file (or in core/, universe24/) is edited. New files only:
`layers/system.py`, `observe/system.py`, `tests/test_system.py`, this file; evidence `results/system/*.json`.

## Composition (written Tue Nov 10 10:40:50 UTC 2026; layers.system.default_system)
Q = 2^29 + 1 (odd; D = 6Q). Blocks (composition order) and their sources:
| namespace | builder (read-only) | parameters |
|---|---|---|
| ref | layers.reference.build_reference | Q-scaled +++ (option body_signs (1,-1,1)); vacuum 2Q (option l0_offset = Q-1: 3Q-1) |
| su2, su3, u1 | layers.gauge.build_default(g, Q) (STAGE 1-GAUGE) | A = kappa = 2^14, mass Q+3, lam 4, 2-path kappa_P 256, beta 6Q - 2^29 (P0 128) |
| matter | layers.matter.build_matter (STAGE 1-EM) | 16-ch Dirac pair, hop 2^27, wilson 2^24, mass 3*2^29 (PROPOSED, see conflicts) |
| em | layers.em.build_em (DEFAULT EM = E1, manager 10:4x) | g_phi 4, g_A 1, sigma 2^8 |
| (variant em="compact") matter / emu1 / cem | layers.em_compact.default_compact | kd 2^13, kw 2^10 (namespaces renamed to avoid the u1 clash) |
| metric, lapse, beta, od2 | layers.gravity (STAGE 1-GRAV) | P = 2^20, k = 2^8 (Q - 1 = 2Pk); beta one-way (default); od2 stress = Dirac hop stress kappa 1; od2_reads OFF |
| arm1, arm2, router, drive, seq | layers.choice | period-6 rings, near-matched opposite Born pair kappa = floor(6Q/16) (P(none) = 1/Q), drive w = 1, sequential router kappa 1; all at vacuum 3Q - 1 |
Build-time result (10:40:27): every variant composes ONE tensor: G = 327 gear types, 8513 monomials, rank 4, 3
inverse stages (E1 default); compact variant G = 341, 8854 monomials; q_lattice validator on.

Integration decisions / conflicts found at build time (to be confirmed by the owners of the layers):
- C1 MASS PARITY: B1-EM's mass 3Q is odd; gravity's first-order lapse needs mass, Wilson and hop in 2^22 Z. The system
  uses mass = 3*2^29 = 3Q - 3 (manager proposal). hop 2^27 and Wilson 2^24 already comply.
- C2 TWO U(1)s: the compact EM route uses B1-GAUGE's u1 links under the namespace "u1", which collides with the
  standalone u1 gauge layer: the compact variant is composed as matter / emu1 / cem (renamed via default_compact's
  names argument). In the E1 default both U(1) sectors coexist (independent: different matter).
- C3 TWO LAPSES: with od2_reads=True the matter would read od2.h00 at centred times AND get the universal lapse from
  metric.h00 (two lapses on one rest clock). Default od2_reads=False (OD2 = constraint sector sourced one-way by
  the b-only Dirac hop stress). B1-GRAV to decide which h00 is THE lapse.
- C4 OD2 stress normalisation: od2_hop_stress multiplies the matter's hop entries (2^27) by an integer kappa >= 1:
  the stress coupling cannot be scaled below 2^27 per unit bilinear (no divisor API). Reported as a missing API.
- C5 E1 + gravity: E1's exact Lorenz/Gauss identities use the FREE hopping current as the source; the lapse rescales
  the matter's transport, so the conserved current of the coupled system differs from the E1 source. Expected:
  E1's identities FAIL in the gravity-coupled composition (to be measured, X6), while they hold with gravity off.

## PRE-REGISTRATION: exactness suite X1-X10 (written Tue Nov 10 10:40:50 UTC 2026, BEFORE any run)
Run for every MODE in {body_signs (1,1,1), (1,-1,1)} x {l0_offset 0, Q-1}, EM = E1 (default); the compact variant at
(+++, 0). L = 3 (CPU is saturated: OMP 1 thread, nice 10). Random data: reference a, b in [-20, 20] (r on the
Q-lattice + offset), gauge layers as in their tests (matter |psi| <= 4000, link noise 8, 2-path 16), Dirac matter
|a|,|b| <= 2^10, field gears (metric, beta, od2, em) |v| <= 2^10 except od2's accumulators prepared at C = 0 by
construction only where stated, choice rings amplitude <= 3, every new-gear remainder uniform in 0..D-1.
X1 ONE Q: tensor.Q == every block.Q == Q.
X2 Q-LATTICE: q_lattice_violations(("ref.*",)) == [] (validator on at compose).
X3 VACUUM + FROZEN: (a) the joint vacuum is fixed for 20 updates (0 changed gears); (b) frozen_equivalence((ref,),
   all other blocks, Q, dense random ref state, 20 updates): 0 base mismatches, 0 extra deviations; (c) offset mode:
   the ref-alone run from r = Q r1 + (Q-1) equals the run from r = Q r1 in a and b, and every r differs by exactly Q-1
   (the embedding theorem), 20 updates.
X4 REWIND: staged inverse returns the random initial state exactly after 8 updates.
X5 JOINT MIRROR (declared as data in observe/system.py): rhoL0 on ref.* (offset 0) or M' (offset Q-1); M' on every
   b-only new gear (gauge, choice, metric, beta, A_d of E1); K o M' on the Dirac matter (Kramers; with E1 the
   staggered Phi map of prepare.em.x_reversor_core); the OD2 staggered map (hij M', h0i (a,b) -> (-h0i_next, -b),
   h00 (a,b) -> (h00(t+2), h00(t+1))). PASS iff X F^n X F^n (s) = N(s) for n = 6 on 2 random states, N = Jp on the
   matter gears (the Kramers central element; identity elsewhere), and X(vac) = vac. Also reported: the plain M' on
   every gear (expected to FAIL with E1's a-read accumulator and OD2).
X6 LAYER IDENTITIES INSIDE THE COMPOSITION (6 updates): gauge Noether (su2 3, su3 9, u1 1 generators) 0 failures;
   OD2 constants C^i, C^0 exactly constant; E1: continuity, Lorenz constancy, Gauss step, global Noether (observe.em)
   -- reported with gravity ON (expected FAIL, C5) and with gravity OFF (expected 0 failures).
X7 RECIPROCITY: check_reciprocity passes; every designation listed with its count (designation string -> count).
X8 B3: composition succeeds (storage locality enforced); support_violations counted per block.
X9 CENSUS: undesignated degree-3 (rank-4) monomials only in the gauge springs (targets in su2/su3/u1 link gears);
   designated degree-3 monomials only in choice (expected: none in this composition); constants 0; a-read monomials
   listed per block (E1 Phi accumulator, matter's Phi read, OD2 chain).
X10 COLLISIONS: namespaces unique; no canonical monomial is both designated and undesignated (a designated read
   coinciding with a force monomial); monomials written by two different blocks counted.

## CHANGES BEFORE THE RECORDED RUN (written Tue Nov 10 10:46:50 UTC 2026)
- CHOICE frozen 10:45:19: the default now uses the odd-Q router (layers.choice_oddq.build_odd_q_router, A = 1,
  kappa = 3*2^26, P(none) = 1/Q per readout) and the ONE-SHOT gated exit pair (layers.choice.build_gated_pair, rank 4
  designated observer) with its gate fibre (build_fibre); no F7, no drive, no sequential router. All choice vacua set
  to 3Q - 1 by a data-level copy (B1-CHOICE note (a)).
- body_signs option added (Study 7 frustrated class; manager 10:4x), l0_offset option (ONE-VACUUM; manager 10:4x).
- EM final (B1-EM): matter hop 2^27, wilson 2^24, mass 3*2^29; E1 sigma 2^8 (default); compact = variant.

## RESULTS X1-X10 (written Tue Nov 10 10:46:50 UTC 2026; runs 10:46:27-10:46:38 UTC, L = 3, n = 6; results/system/*.json)
| mode | X1 one Q | X2 q-lattice | X3 vacuum / frozen / embedding | X4 rewind | X5 joint mirror (2 states) / fixes vac / control M' | X6 gauge Noether / OD2 C / E1 (with gravity) | X7 reciprocity (designated, two-time) | X8 supports | X10 collisions |
|---|---|---|---|---|---|---|---|---|---|
| default (+++, off 0, E1) | PASS | 0 | 0 changes / 0-0 / n.a. | exact | 2/2 / yes / FAILS (as expected) | 0 / 0 / continuity 162, Gauss-step 162 failures, Lorenz 0, global Noether 0 | OK (1033, 142) | 2928 | 0 / 0 |
| +++, off Q-1 | PASS | 0 | 0 / 0-0 / exact (r differs by Q-1, a, b equal) | exact | 2/2 / yes / FAILS | same | OK (1033, 142) | 2928 | 0 / 0 |
| +-+, off 0 | PASS | 0 | 0 / 0-0 / n.a. | exact | 2/2 / yes / FAILS | same | OK | 2928 | 0 / 0 |
| +-+, off Q-1 | PASS | 0 | 0 / 0-0 / exact | exact | 2/2 / yes / FAILS | same | OK | 2928 | 0 / 0 |
| compact EM variant (+++, off 0) | PASS | 0 | 0 / 0-0 / n.a. | exact | 2/2 / yes / also exact | 0 / 0 / n.a. | OK (755, 24) | 3030 | 0 / 0 |
- Default tensor: G = 328 gear types, 8529 monomials, rank 4, 3 inverse stages. E1 WITHOUT gravity: continuity,
  Lorenz, Gauss step and global Noether all 0 failures (162 node-updates).
- X9 census: rank-4 FORCE terms only in the gauge springs (su2 48, su3 1404, u1 12; emu1 12 in the compact variant),
  rank-4 DESIGNATED terms only in choice (exit pair: 18); constants 0; a-read monomials: matter 112 (E1 centred Phi
  read), em 6 (Lorenz accumulator), od2 24 (accumulator chain).
- X7 designations (11 strings): beta G read 400, E1 alpha.A 160, E1 centred Phi read 16, E1 source 96, Lorenz
  accumulator 6, beta source 7, OD2 stress 288, OD2 accumulator 24, gated observer 18, router observer 18, (compact
  variant: no E1 strings).
- X5: the declared joint mirror (rhoL0 or M' on ref, K o M' + E1's staggered Phi map on matter/em, the OD2 staggered
  map with hij M', M' elsewhere) satisfies X F^6 X F^6 = N (N = Jp on the 16 matter gears: the Kramers sign) and
  fixes the joint vacuum in all modes. The control (plain M' on the matter) fails whenever E1 is present (as
  registered); with the compact EM it is exact too (b-only).
CONFLICT C5 CONFIRMED: inside the gravity-coupled system E1's LOCAL continuity and dressed Gauss step fail at every
node (162/162) while Lorenz constancy and the GLOBAL Noether charge stay exact: the lapse/beta rescale the matter's
transport, so the exact local current is no longer E1's free-current source. Needs a design decision (B1-EM/B1-GRAV):
source E1 with the lapse-dressed link current (it is b-only and link-local), or accept a global-only charge law.

## PRE-REGISTRATION ONE-MATTER (ARCH item 1; written Tue Nov 10 10:48:34 UTC 2026, BEFORE the code exists or runs)
THEOREM (rank, elementary): a matter hop through k independent link fields is a monomial of degree 2 + k in the
potential (degree 1 + k in u), i.e. rank 2 + k on v = (1, b, a)... counted as in the core: u-degree 1 + k <= 3 needs
k <= 2 for the potential's degree 2 + k <= 4, but the rank-4 slot is reserved for OD4 springs, so a FORCE hop may
carry exactly ONE link field (rank 3). Hence ONE matter content with several gauge groups needs ONE link algebra per
hop. Options (design decision for the owner):
 (A) ONE unified link algebra M6(C) (72 integers per link) acting on ONE multiplet Psi = colour 3 (x) Dirac pair 16
     (48 channels; the complex structure is the Dirac carrier J = 1_2 (x) J8; the pair index carries C^2 with the
     standard matrix units E_00 = diag(1,0), E_01 = [[0,1],[0,0]], ... as REAL matrices). Exact local U(6) covariance
     (bit-exact for monomial unit matrices with entries +-1/+-i), which contains SU(3)_colour x SU(2)_pair x U(1)'s;
     EM = J' = 1_3 (x) eps (x) 1_8 = 1_3 (x) i sigma_y (Georgi-Glashow: EM inside the pair SU(2)); 36 gauge
     generators (incl. colour-isospin "leptoquark" ones). BUILT HERE.
 (B) (A) plus an auxiliary product link V slaved to U_colour (x) U_weak by kappa_V <V, U_c (x) U_w> (2-path-like,
     rank 3): exact covariance under the PRODUCT group only, V ~ U_c (x) U_w only adiabatically. Not built.
 (C) midpoint matter gears (two half-hops, each through one link): exact product-group covariance, extra matter
     modes. Not built.
 (E) SU(2)_pair (x) U(1)_EM on one Dirac pair (quaternion link via {1, J', sigma_x(x)J, sigma_z(x)J}; the compact
     route with SU(2)): exact, but E1 (on-site J' couplings) is NOT SU(2)_pair invariant. Not built.
TESTS O1-O5 (option A; Q = 2^29+1; matter = three B1-EM build_matter pairs q0, q1, q2 (hop 2^27, wilson 2^24, mass
3*2^29) + link block "u6" (72 gears per axis, zero mode, optional Frobenius spring lam) + coupling block "cu6";
A = 2^14, kd = 2^13, kw = 2^10 so the vacuum hopping A*N_d is the matter blocks' own):
 O1 build: ONE Q, reciprocal with 0 designations, B3, rank 3 (lam = 0) / rank 4 only via the link spring (lam = 4).
 O2 vacuum fixed (20 updates); frozen_equivalence(base = (q0, q1, q2), extra = (u6, cu6)): 0 / 0 (20 updates).
 O3 Noether/Gauss with the remainder, 0 failures: colour su(3) (i lambda_1..7, i diag(1,1,-2)) (x) 1_2, pair su(2)
    1_3 (x) {i sigma_x, i sigma_y (= EM J'), i sigma_z}, u(1) i 1_6, and two colour-isospin mixing u(6) generators;
    L = 3, random data (matter |b| <= 2^10, link deviations <= 8, random remainders), 8 updates.
 O4 local covariance bit-exact: random monomial unit U(6) gauge fields (entries +-1, +-i) and product SU(3) x SU(2)
    unit fields; 8 updates.
 O5 rewind exact; plain M' on every gear: X F^8 X F^8 = id; Kramers (K o M' on the 48 matter gears, M' on Re W,
    JM = (-b, -a, r) on Im W): X F^8 X F^8 = N (Jp on matter); both fix the vacuum.

## PRE-REGISTRATION C5-FIX: E1 sourced by the LAPSE-DRESSED link current (manager ruling 10:5x; written Tue Nov 10 10:51:54 UTC 2026, BEFORE the code exists or runs)
DERIVATION. In the composed system the matter's link potential is f_d(x) b(x)^T N_d b(x+e_d) with the scalar link
factor f_d(x) = 1 - (F(x) + F(x+e_d))/(2P) + (9/16)(G(x) + G(x+e_d))/P (B1-GRAV: first-order lapse link factor
c_link = 1/2 per endpoint; beta read 9/16 per endpoint; F = metric.h00, G = beta.G). All on-site couplings (clock
factor, beta site read, E1's phi V and alpha.A) are symmetric and commute with J', so the exact Board-Noether current
of J' is j^eff_d = f_d j_d (j_d = 2 b(x+e)^T J' H_d b(x)), and rho(t+1) - rho(t) + div j^eff(t) = R exactly.
E1's source must therefore be sigma * f_d * s_d (s_d = j_d / (2g)): the extra terms sigma M_d (-1/(2P)) (F_x + F_y) b b'
and sigma M_d (9/(16P)) (G_x + G_y) b b' are b-only and link-local but RANK 4 (designated one-way, like E1's source):
a census exception (rank-4 designated terms outside choice) to be ruled on.
INTEGER CONFLICT (found by the derivation): with hs = hop/g = 8, ws = wilson/g = 1, the dressing coefficients are
sigma ws/(2P) and 9 sigma ws/(16P): integers only for sigma in 2^24 Z (P = 2^20). B1-EM's sigma = 2^8 is impossible;
the alternative is P <= 2^4 (k = 2^24), far too coarse for gravity. The fix is therefore built with sigma = 2^24
(DECLARED: 2^16 x B1-EM's coupling; a design decision for B1-EM / the owner).
TEST (all 4 modes, gravity ON, L = 3, n = 6): with em="e1d" (layers/em_dressed.py: build_em(sigma = 2^24) + the
dressing terms): dressed local continuity residual (new observer) 0 failures, E1's Gauss step (frozen observer
observe.em.gauss_step_residual) 0 failures, Lorenz constancy 0, global Noether 0; plus X1-X5 and X7 as before.
- ADDED before running (10:55:47 UTC): O6 U(6) link-norm stability (report): lam = 4 Frobenius spring, A = 2^14, matter
  |b| <= 4000 (the gauge family's calibrated drive at this A), L = 3, 500 updates: max | |U|_F / (sqrt6 A) - 1 | and
  the unitarity defect max |U^dag U - A^2|_F / A^2 (the Frobenius spring does not pin the non-unitary modes); also at
  2x the calibrated amplitude (R-P2's window edge).

## B1-GRAV ANSWERS APPLIED (10:51) and RESULTS of the re-run (written Tue Nov 10 10:56:05 UTC 2026; runs 10:54:20-10:55:08 UTC; results/system/*.json)
Code changes (my files only): gravity = layers.gravity_select.gravity_blocks (ONE lapse): lapse="od2" DEFAULT (OD2 +
build_lapse_oneway on od2.h00 + beta on od2.h00, no metric, OD2 stress OFF), lapse="wave" variant (metric + reciprocal
lapse + beta, no OD2); em DEFAULT = "e1d" (layers/em_dressed.py, sigma = 2^24); option l0_lapse None | "R" | "W"
(layers.gravity_l0; needs l0_offset = Q - 1; q-lattice validator off for it). Default tensor: G = 318, 8355 monomials.
| mode | X1 | X2 | X3 vac / frozen / emb | X4 | X5 declared mirror | X6 gauge / OD2 C | E1 identities with gravity ON | X7 (designated, two-time) | X10 |
|---|---|---|---|---|---|---|---|---|---|
| default (od2 lapse, e1d, +++, off 0) | PASS | 0 | 0 / 0-0 / n.a. | exact | **FAILS 2/2** (fixes vacuum) | 0 / 0 | DRESSED continuity 0, Gauss step 0, Lorenz 0, global Noether 0 (free-current continuity 162/162 for contrast) | OK (1529, 142) | 0 / 0 |
| +++ off Q-1; +-+ off 0; +-+ off Q-1 (od2, e1d) | PASS | 0 | 0 / 0-0 / exact | exact | **FAILS** | 0 / 0 | all 0 | OK (1529, 142) | 0 / 0 |
| wave lapse, e1d, +++ off 0 | PASS | 0 | 0 / 0-0 | exact | **PASS 2/2**, fixes vacuum | 0 / n.a. | all 0 | OK (1105, 118) | 0 / 0 |
| e1 undressed (sigma 2^8), od2 | PASS | 0 | 0 / 0-0 | exact | FAILS | 0 / 0 | continuity 162, Gauss step 162 failures; Lorenz 0, global 0 | OK | 0 / 0 |
| compact EM, od2 | PASS | 0 | 0 / 0-0 | exact | FAILS | 0 / 0 | n.a. | OK (867, 24) | 0 / 0 |
| l0_lapse R (off Q-1) | PASS | 1056 (declared) | 0 / 0-0 / exact | exact | FAILS | 0 / 0 | all 0 | OK (2585) | 0 / 0 |
| l0_lapse W (off Q-1) | PASS | 1344 (declared) | 0 / 0-0 / NOT today's board (as stated by B1-GRAV) | exact | FAILS | 0 / 0 | all 0 | OK (2585) | 0 / 0 |
- C5 RESOLVED by the dressed source: local continuity, Gauss step, Lorenz and the global charge are EXACT with gravity
  ON in every mode (0 failures), at the price sigma = 2^24 (declared) and 384 rank-4 designated source terms in em.
- NEW CONFLICT C8 (found by X5): the DEFAULT one-way lapse reads the OD2 accumulator h00 at a SINGLE time; the
  declared staggered OD2 reversor needs the matter to read h00 at the CENTRED time (B1-GRAV's G10 used
  od2_centred_lapse_read). With build_lapse_oneway the joint mirror fails (2/2 states, every od2 mode) while the
  "wave" variant passes. Fix needed from B1-GRAV: a centred (look-ahead, two-time) one-way lapse read with BOTH the
  clock and the link factor; until then the default has no exact time mirror (rewind stays exact).
- RESULT O6 (10:56:25): at the gauge family's matter amplitude 4000 (and 8000) the U(6) links with the Frobenius
  spring RUN AWAY at t = 5 (4): the coupling drives all 72 link components (relative drive ~0.04 per update^2) and the
  Frobenius spring pins only |U|_F, not the 71 other (non-unitary) directions. ADDED before running (10:56:52 UTC): the
  same run at matter amplitude 64 and 256 (500 updates), to locate the bounded window.
- RESULT O6 scan (10:57:20): amplitude 64 and 256 ALSO run away at t = 6: the cause is NOT the matter drive but the
  Frobenius spring's CFL: its radial stiffness is 2 lam |U0|^2 = 12 lam A^2 (six diagonal entries), i.e.
  12 lam A^2 / D = 4.0 at lam = 4, A = 2^14 (> 2: unstable by construction; the single-algebra springs have
  2 lam A^2 / D = 2/3). My parameter error, recorded. ADDED before running (10:57:43 UTC): O6b with A = 2^13,
  kd = 2^14, kw = 2^11 (hop and wilson unchanged), lam = 2 (12 lam A^2 / D = 0.5), matter amplitude 64, 256, 1024,
  500 updates.
- RESULT O6b (10:58:32): A = 2^13, Frobenius lam = 2: |U|_F held to 0.001-0.0025 for 500 updates at amplitude 64 and
  256, BUT the unitarity defect |U^dag U - A^2|_F / A^2 grows to 3.1 / 4.1 (the non-unitary directions are free).
  ADDED before running (10:58:43 UTC): spring="matrix" (-(lam/4) Tr((U^dag U - A^2)^2), 26,352 rank-4 monomials per
  link block) at A = 2^14, lam = 4 (radial 2 lam A^2 / D = 2/3, as the gauge default), amplitudes 64, 256, 1024, 4000,
  500 updates: report the Frobenius deviation and the unitarity defect (bounded window), and the exact identities
  (Noether for the 14 generators, rewind, M' and Kramers mirrors) on 8 updates with this spring.
- DEVIATION from the O1-O5 pre-registration (recorded 10:59:17 UTC, before the re-run): the first O1-O5 run (lam = 4
  Frobenius at A = 2^14, CFL 4.0) blew up into big integers and was stopped at 10:59:02; the re-run uses the MATRIX
  spring (lam = 4, CFL 2/3) for O2-O5, O1 checks (lam 0, Frobenius) and (lam 4, matrix), and the random matter
  amplitude is 64 (was 2^10) to keep the int64 path; the U(6) gauge map gained a numpy two-sided product (speed only).

## ONE-MATTER (option A) DESIGN FACTS (written Tue Nov 10 10:59:17 UTC 2026)
- U(6) IS LARGER THAN SU(3) x SU(2) x U(1): the link algebra M6(C) gives 36 gauge generators acting on the 6 = colour 3
  (x) pair-isospin 2, including colour-isospin mixing ("leptoquark") ones; the matter couples to all of them. How U(6)
  breaks to the standard group (springs with different targets per block, a Higgs-like link background, or a
  product-link auxiliary as in option B) is an OPEN design question: written down, NOT decided here.
- EM = J' = 1_3 (x) i sigma_y sits INSIDE the pair SU(2) (Georgi-Glashow); there is NO C-odd hypercharge in one
  Dirac pair (the only commuting extra U(1) is the carrier number J, which is C-even). Chirality: OPEN (vector-like;
  the HAND pair, Study 7, is working on chirality from the sign class).
- ONE CONE: the U(6) link block has no 2-path (plaquette) gears, so its links carry NO transverse waves at all
  (electric-only, strong-coupling limit); with 2-path gears the systemic gap reported by B1-EM (link waves at
  c ~ 0.003 in the gauge default regime) applies. The one-cone property for gauge links is OPEN.
- Spring: the Frobenius spring pins only |U|_F (its radial stiffness 12 lam A^2 also needs lam <= 2 at A = 2^14 /
  A = 2^13); the MATRIX spring Tr((U^dag U - A^2)^2) (26,352 rank-4 monomials per link block) is the one that pins
  every Hermitian mode; results O6c below.

## RESULTS ONE-MATTER O1-O5 (written Tue Nov 10 11:00:28 UTC 2026; run 10:59:03-10:59:36 UTC; results/system/O1-O5_onematter.json)
| test | verdict | numbers |
|---|---|---|
| O1 build | PASS | ONE Q = 2^29+1; lam 0: G = 264, 11,208 monomials, rank 3; matrix spring lam 4: 43,914 monomials, rank 4 (26,352 degree-3 = the spring only); reciprocal with 0 designations; b-only; constant-free; 0 physical-support violations |
| O2 vacuum | PASS | the joint vacuum is fixed for 20 updates |
| O2 frozen_equivalence (base = the three free pairs) | FAIL as pre-registered (MY pre-registration error) | 65,250 base mismatches: the U(6) links are DYNAMICAL and respond to excited matter by design (u_W = Psi^T rho(E) N Psi'); the coupling has no kappa = 0 "frozen" setting (the vacuum hopping A kd IS the matter's hop). Only the vacuum statement applies |
| O3 Noether/Gauss with the remainder | PASS: 0 failures / 3,024 | 14 generators: colour i lambda_1..7, i diag(1,1,-2); pair i sigma_x, i sigma_y (= EM J'), i sigma_z; u(1) i 1_6; two colour-isospin mixing u(6) generators; matter amplitude 64 (remainder-floor regime: the total moves as much as the summed remainder terms, exactly) |
| O4 local covariance | PASS bit-exact | random monomial U(6) units (entries +-1, +-i) and random product units (colour monomial (x) pair monomial), 8 updates |
| O5 reversors | PASS | rewind exact; plain M' X F^8 X F^8 = id; Kramers (K o M' on the 48 matter gears, M' on Re W, JM on Im W) X F^8 X F^8 = N (Jp on matter); both fix the vacuum |

## RESULTS O6 (U(6) link stability; written Tue Nov 10 11:01:05 UTC 2026; results/system/O6_*.json)
| spring | A | matter amplitude | worst |U|_F deviation | unitarity defect max |U^dag U - A^2|_F / A^2 | runaway |
|---|---|---|---|---|---|
| Frobenius lam 4 | 2^14 | 4000 / 8000 / 64 / 256 | - | - | t = 5 / 4 / 6 / 6 (spring CFL 12 lam A^2/D = 4.0: my parameter error) |
| Frobenius lam 2 | 2^13 | 64 / 256 | 0.0012 / 0.0025 | 3.1 / 4.2 (drifting up) | none in 500 (but non-unitary) |
| MATRIX lam 4 | 2^14 | 64 / 256 / 1024 | 0.0006 / 0.0006 / 0.006 | 0.008 / 0.008 / 0.067 | none in 500 |
| MATRIX lam 4 | 2^14 | 4000 | 13.7 | 1.06 at t = 50 | t = 65 |
Reading: the full matrix spring is REQUIRED for U(6) links (the Frobenius spring leaves 71 directions free). With it the
links stay unitary to < 1 % up to matter amplitude 1024 (500 updates); the window closes between 1024 and 4000 (the
single-algebra gauge layers were calibrated at 4000 at this A: the U(6) coupling drives all 72 components). Consistent
with R-P2's finding that the stable window ends at a small multiple of the calibrated amplitude; a longer (t >= 2000)
run at amplitude <= 1024 is OPEN.

## FINAL RE-RUN AND STATUS (written Tue Nov 10 11:02:56 UTC 2026; suites run 11:01:10-11:02:37 UTC on the final code)
Command: `OMP_NUM_THREADS=1 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_system research.metric_variant_v1.tests.test_onematter`
-> 3 tests OK (87.1 s): X1-X10 in 13 modes (assertions: one Q, q-lattice where applicable, vacuum, frozen, rewind,
reciprocity, vacuum-fixing mirror, gauge Noether, dressed E1 identities; the declared mirror asserted for the wave
lapse only, C8 recorded for od2), E1 without gravity, and O1-O5. Frozen STAGE 1-GAUGE files verified unchanged
(sha256 = manifest); universe24/ untouched; no git.
Status of the integration items:
| item | status |
|---|---|
| ONE Q = 2^29+1 across all layers | DONE (P a parameter: P = 2^20 default, k = (Q-1)/(2P); sigma_dressed = 16P) |
| C1 mass parity | applied: mass 3*2^29 (E1 exact at it with gravity off) |
| C2 namespace | compact variant renamed emu1/cem |
| C3 one lapse | B1-GRAV gravity_blocks: od2 (current default) / wave (variant; planned default after B1-GRAV's F4d) |
| C4 OD2 stress | OFF in the default (B1-GRAV: b-only first-order stress is not conserved) |
| C5 local charge with gravity | FIXED: dressed E1 source (em="e1d" default), 0 failures in every mode; sigma = 16P DECLARED; 384 rank-4 designated source terms in em |
| C6 L0 gravity-blind | options l0_lapse "R" (exact today's board, EP violated by U/Q) and "W" (exact EP, today's board only in vacuum), both exact otherwise; default None |
| C7 one cone | systemic gap: gauge link waves ~0.003 (B1-EM) and none at all for U(6) without 2-path gears |
| C8 od2 one-way lapse vs mirror | the declared joint mirror FAILS with the od2 lapse (single-time accumulator read); B1-GRAV: an exact centred LINK read is impossible under B3 -> planned default = wave lapse (+ R-a background, k = 0 offset) |
| ONE matter content | option (A) built: U(6) on colour 3 (x) Dirac pair, exact Noether (14 generators incl. EM J'), bit-exact covariance for the declared monomial U(6) units and product units, rewind, M' and Kramers mirrors; matrix spring required; stable to amplitude 1024 (500 updates); U(6) > SM, breaking OPEN; no C-odd hypercharge; chirality OPEN; no link waves without 2-path gears |
Files (new, integrator):
| file | sha256 |
|---|---|
| `layers/system.py` | `c9b0ba9c3fbb4c09039e39ea63bd05402b4bbac3db65f98bdeca9e1b7f2685a6` |
| `layers/onematter.py` | `bba03756d947a1f28e9a73c3d4927941682ebd534bf94cac5c8ec144097366b0` |
| `layers/em_dressed.py` | `ef8457514737c2437214f37886f78ee5cb8943b9eafa56a12f4cfa1aac6dc3aa` |
| `observe/system.py` | `79f6db20cda4c0d274172be37d5463e32e9f7542590d505b65cc55594cbb2cc3` |
| `observe/onematter.py` | `1fc9e9a4fd6f4f91e5412bf19f9268a782515144adf7cd9be4040a198c8d76d4` |
| `prepare/system.py` | `2497c88720737f94158d216cd8343395aa7537372ca18939dda023431936b5ac` |
| `tests/test_system.py` | `bf8a0c46571934df3ed57b24495a4607ceff6b773473a610a0a7dc4afa756154` |
| `tests/test_onematter.py` | `e87df121cdd668b7949f1361199d6caeaeb0b9184ad19dc60d290227ed128d95` |
| `demos/system/o6_u6_stability.py` | `ad03599b698eebc1f9e81d05de3d80229f8a122bd6b7398ac67b15a7e5cf94f5` |
- ADDED before running (11:03:06 UTC): O6d long run: MATRIX spring lam 4, A = 2^14, matter amplitude 1024, 2000 updates
  (report the worst Frobenius deviation and unitarity defect; bounded iff no runaway and defect < 0.5).

## DEFAULT SWITCH (B1-GRAV final 11:02, manager ruling) and RESULTS (written Tue Nov 10 11:04:30 UTC 2026; runs 11:03:47-11:04:21 UTC)
- Default gravity = lapse "wave" (metric + reciprocal lapse + beta) + the R-a background gear B (B1-GRAV F4d: u_B = 6Q b,
  -b_B into metric.h00, designated one-way, data) + the k = 0 offset (initial data). OD2 = variant flag (exact
  constraints and exact freezing of the uniform mode, but its one-way read has no exact time mirror: C8 no-go under B3).
- OPEN (B1-GRAV): uniform-mode drift O(U^2 t^2) (+0.08 at U3 = 0.02, t = 700; passes at 4x weaker load, F4e); root cause
  the non-conserved b-only stress; an exactly conserved first-order stress is OPEN.
| mode | X2 | vacuum / frozen / embedding | rewind | JOINT MIRROR (declared, 2 states) / fixes vacuum | gauge Noether / OD2 C | dressed E1 (gravity ON) | X7 designated | X10 |
|---|---|---|---|---|---|---|---|---|
| DEFAULT wave + background (+++, off 0) | 0 | 0 / 0-0 / n.a. | exact | PASS 2/2 / yes | 0 / n.a. | continuity 0, Gauss step 0, Lorenz 0, global 0 | 1106 | 0 / 0 |
| wave +++ off Q-1; +-+ off 0; +-+ off Q-1 | 0 | 0 / 0-0 / exact where applicable | exact | PASS 2/2 / yes | 0 | all 0 | 1106 | 0 / 0 |
| od2 variant (+++ 0; +-+ Q-1) | 0 | 0 / 0-0 | exact | FAILS (C8) / yes | 0 / 0 | all 0 | 1529 | 0 / 0 |
| compact EM | 0 | 0 / 0-0 | exact | PASS / yes | 0 | n.a. | 444 | 0 / 0 |
| e1 undressed (sigma 2^8) | 0 | 0 / 0-0 | exact | PASS / yes | 0 | continuity 162, Gauss step 162 FAIL; Lorenz 0, global 0 | 722 | 0 / 0 |
| l0_lapse R / W (off Q-1) | 1056 / 1344 (declared) | 0 / frozen NOT expected (L0 now SOURCES the wave lapse) / R exact, W not today's board | exact | PASS / yes | 0 | all 0 | 1106 | 0 / 0 |
| P = 2^16 (sigma 2^20) | 0 | 0 / 0-0 | exact | PASS / yes | 0 | all 0 | 1106 | 0 / 0 |
- RESULT O6d (11:04:38): MATRIX spring lam 4, A = 2^14, matter amplitude 1024, 2000 updates: worst |U|_F deviation
  0.0084, unitarity defect <= 0.087 (slow creep 0.066 -> 0.083 between t = 50 and t = 2000), no runaway: BOUNDED by the
  pre-registered criterion (defect < 0.5). results/system/O6_u6_stability_A16384_lam4_matrix_1024_T2000.json.

## FINAL (written Tue Nov 10 11:05:28 UTC 2026)
Final suite run on the final code 11:04:44-11:05:22 UTC: `OMP_NUM_THREADS=1 nice -n 10 python -m unittest
research.metric_variant_v1.tests.test_system research.metric_variant_v1.tests.test_onematter` -> 3 tests OK (37.9 s;
11 system modes incl. the new default, E1 without gravity, O1-O5). Frozen STAGE 1-GAUGE files unchanged; universe24/
untouched; no git. Final hashes of the integrator files (supersede the table above):
| file | sha256 |
|---|---|
| `layers/system.py` | `eac215e3be4c2f9cfd9b73528383570ba51a03941431435f460f049b1bcb6bb5` | (docstring updated 11:05:38, after the final run; code unchanged) |
| `layers/onematter.py` | `bba03756d947a1f28e9a73c3d4927941682ebd534bf94cac5c8ec144097366b0` |
| `layers/em_dressed.py` | `ef8457514737c2437214f37886f78ee5cb8943b9eafa56a12f4cfa1aac6dc3aa` |
| `observe/system.py` | `79f6db20cda4c0d274172be37d5463e32e9f7542590d505b65cc55594cbb2cc3` |
| `observe/onematter.py` | `1fc9e9a4fd6f4f91e5412bf19f9268a782515144adf7cd9be4040a198c8d76d4` |
| `prepare/system.py` | `2497c88720737f94158d216cd8343395aa7537372ca18939dda023431936b5ac` |
| `tests/test_system.py` | `b403e9d281e147d70136538155fe2861853fc95c4a7a9b9105493abbe95ecdbe` |
| `tests/test_onematter.py` | `e87df121cdd668b7949f1361199d6caeaeb0b9184ad19dc60d290227ed128d95` |
| `demos/system/o6_u6_stability.py` | `7a91ebbc628c0b16846981a0d95febcc7605012389b7f36561482ff2938b8eb6` |

## PRE-REGISTRATION SEED (manager tasks 11:0x; written Tue Nov 10 11:08:22 UTC 2026, BEFORE the code exists or runs)
prepare/seed.py (DATA ONLY): s2_star (S2*, s6/AGREE_M (a)/F2: b(x0) = A e_i, a(x0 + e_y) = A Gamma e_i, Gamma = J'K W0
(= W0 G, G = J'K), everything else the joint vacuum), node_rstar (b(x0) = A e_i, a(x0) = A Gamma e_i), ra_background
(the R-a datum: bgk.B held at the declared uniform value, a = b), k0_offset (adds the declared constant to the lapse
field's a and b: the k = 0 offset), and a documented P+ hook (TODO: port s6/M1_work/M1_t29; not ported in this hour).
observe/seed.py (AUDIT MAP): R* = spatial inversion about the seed centre (link midpoint x0 + e_y/2 for S2*, the node
for node R*) with: matter (a, b) -> (Gamma b, Gamma a) at the mirrored node (R' on negated channels, M' on positive ones),
E1: A_d (a, b) -> (-b, -a) at the re-based mirrored link (R'), Phi staggered (-Phi_next, -b); every other gear: (a, b)
swapped at the mirrored storage node with its vacuum-fixing remainder map (rhoL0 on ref at offset 0, R' elsewhere).
DECLARED SCOPE: R* is an exact reversor of the matter + E1 sector (Study 6 design); on the other layers only its
vacuum-fixing part is declared (their parity signs are OPEN), which is what R*(seed) = seed needs.
TEST (tests/test_seed.py), default system (wave + background, e1d, all layers), L = 6, A = 2^12, i = 0:
 SD1 legal at t = 0: E1 Lorenz C = 0 and Gauss Y = 0 at every node; exactly 2 non-vacuum integers (S2*, node R*).
 SD2 R*(s0) = s0 for S2* (link-centred) and node R* (node-centred).
 SD3 exact rewind of the full composed system from each seed (10 updates).
 SD4 (report) the bounce F^-t(s0) = R*(F^t s0), t <= 6, on the matter + E1 subsystem (gravity, gauge, choice off).
 SD5 R-a datum and k = 0 offset: setting bgk.B = (v, v) and the offset keep the state stationary in the bgk gear (u_B = 6Q b)
     and the offset is visible only in metric.h00 (data check).

## PRE-REGISTRATION v2 DEFAULT (manager 11:1x-11:20 + OWNER decisions 1, 2, 3, 4-as-prediction, 6, 7, 8; written Tue Nov 10 11:21:03 UTC 2026, BEFORE any edit or run)
PARAMETERS (ONE Q): Q = 2^33 + 1 (D = 6Q); P = 2^20 (k = (Q-1)/(2P) = 2^12, k = 0 mod 4); hop = 2^31; wilson = 2^30
(g = 2^30, hs = 2, ws = 1); MASS = 4915 * 2^22 = 20615004160 (the multiple of 2^22 nearest 2.4 Q; R-P1/R-P2 weak-field
lock: a rational rest frequency locks weak potential shifts). Rest clock cos w0 = mass/D = 0.3999837, w0 = 1.1592972,
period 5.4198 updates, rotation number 0.1845079; nearest rationals (q <= 40): 7/38 (2.97e-4), 5/27 (6.8e-4), 2/11
(2.7e-3), 3/16 (3.0e-3) (the earlier candidate 5*2^32 sat 2.2e-4 from 2/11; 3Q sits ON 1/6). mass + 12 wilson =
2.31e10 <= D = 5.15e10; the full spectrum bound max_k |eig M(k)| <= D is computed and reported. g_phi = 4, g_A = 1,
sigma = 2^24 (e1 and e1d); dressing coefficients sigma ws/(2P) = 8 and 9 sigma ws/(16P) = 9 checked on the built block.
Weak-field rule (R-P1/R-P2): matter amplitude x field >= D/(8 g_phi) = 1.61e9 in demos and seeds (recorded in info).
Gauge default_regime(2^33+1): A = kappa = 2^16; odd-Q router P(none) = 1/(2^33+1).
DEFAULTS: (1) l0_offset = Q - 1: vacuum (0,0,3Q-1) for every gear, R' = THE mirror; the q-lattice validator is not
applied to the default composition (X2 reported, not asserted). (2) body_signs = (1,-1,1) (handed class; L0 = dark
sector; L0 clicks AUDIT-ONLY: passive OD1-type readout label in observe/, not a law). (3) l0_lapse = "W" = FORM C (new
file layers/gravity_l0c.py; template layers/gravity_l0.py): L0 ports at Q - 1 plus the on-site carrier remainder
6 b (u = D b - (Q-1)(M0 + T) b), clock factor (1 - 2U) on M0 = 6*1 - Sum_d W_d (on-site, F(x)), link factor (1 - 4U) on
the difference transport (F(x) + F(x+e)), U = F/(2P); reciprocal (L0 sources the wave lapse). (4) em = "e1d" (dressed
E1; its lattice-scale departure from exact action = reaction is a PREDICTION). (6) odd-Q one-shot routers. (7) no F7.
(8) lapse = "wave" + R-a background + offset; OD2 variant. (5) chirality: PENDING OWNER. c2: OFF unless run Z below is
bounded on (1,-1,1) (then ON in the handed default, with the late rounding-heating note).
X1-X10 (tests/test_system.py at the new Q): modes default (+-+, off Q-1, form C, e1d, wave+bgk, choice, gauge),
default+++ (same, +++), noW (l0_lapse None), od2 variant, compact, e1 undressed, P = 2^16, legacy (+++ off 0, no L0
lapse, q-lattice validator on). Expected in every wave mode: X1 one Q; X3 vacuum 0 changes in 20 updates; X4 rewind
exact; X5 joint mirror (R' everywhere; rhoL0 on ref only in legacy) PASS 2/2 and fixes the vacuum; X6 gauge Noether 0
failures, dressed E1 identities (continuity, Gauss step, Lorenz, global) 0; X7 reciprocity ok; X8 0; X10 0. X3 frozen
equivalence asserted only without an L0 lapse (with it, L0 sources gravity). X2: 0 asserted only in legacy.
Int64 headroom: Engine.stats (int64_steps / pyint_steps) reported for the vacuum run and the random-state run per mode.
One-matter O1-O5 re-run at the new Q (A = 2^16, kd = hop/A = 2^15, kw = wilson/A = 2^14; ratios as at 2^29+1), same
criteria as before (O2 frozen equivalence known not to apply: dynamical links).
FORM C TEST (tests/test_l0c.py; L = 4; U0 = 0.01, i.e. a uniform static prescribed lapse gear F = 2P U0 read ONE-WAY
for the clock test, designated, as B1-GRAV's L0-EP; the reciprocal block checked separately):
 C1 reciprocity (0 designations), integer coefficients, vacuum fixed, rewind exact, R' mirror exact on L0c + reciprocal
    lapse + metric + background (and in X5 of the default).
 C2 half-angle law from L0 CLICKS (sign cycles of one L0 gear over T = 4000 updates, zero crossings interpolated) on
    EVERY massive band at k = 0 (all distinct eigenvalues mu > 0 of M0; +-+ and +++): N_click = sin(w/2)/sin(w0/2) with
    w0 from the F = 0 twin; PASS iff |N_click/sqrt(1 - 2U0) - 1| <= 1e-4 for every band and class. Contrast reported:
    B1-GRAV's split (build_l0_weight + build_l0_lapse) on the same modes. +++ light: the massless band at the smallest k
    (k = pi/2): w/w0 vs sqrt(1 - 4U0) (report).
 C3 universality with Dirac matter: the default matter's rest clock (k = 0, mass only) under B1-GRAV's matter lapse
    reading the same F: N_dirac = cos w / cos w0 (demodulated pi/2-carrier law) vs N_L0: PASS iff
    |N_L0 - N_dirac| <= U0^2/2 + 1e-4 (predicted gap sqrt(1 - 2U0) - (1 - U0) = -5.0e-5); the matter's official
    sign-cycle half-angle reading reported.
RUN Z (ZQ8 c2 on the package; condition (c) of the sign-class decision; new files layers/c2_zq8.py,
demos/system/zq8_c2.py): 8 gears per link (Z[Q8]), bit-exact local Q8 (permutations; R_q commutes with the ports of
BOTH classes: checked 0/48 non-commuting pairs at 11:19), ONE OD4 spring per simple component of R[Q8] = 4 sign
characters (eps, V+) + H: Phi -= (lam/4) [Sum_chi (chi(U)^2 - A^2)^2 + (|h(U)|^2 - A^2)^2], lam = 4; FINE links;
l0_offset = Q - 1 (vacuum 3Q - 1, R'). Arm A (Study 7 comparable): L0 at weight Q, kappa A = Q, A = 20857
(kappa = 411849); Arm B (default-composable): form-C L0 (ports Q - 1 + on-site 6), kappa A = Q - 1, A = 2^14. Data:
generic L0 excitation, every L0 gear b, a uniform in [-amp, amp], amp = floor(A/128) (amp/A < 0.01), links at vacuum;
L = 4; 3 seeds; T = 10,000 updates; body_signs (1,-1,1) and the +++ control. RUNAWAY := any |b| > 2^40 or
max |W|/A > 4 (run stopped, time reported). BOUNDED := no runaway in 10,000 updates. Reported every 500 updates:
max |W|/A, max |chi(U)/A| - 1 per component, max L0 |b|/amp. Prediction (Study 7 ONE-M1/M2): (1,-1,1) bounded, +++ runs
away at t ~ 91-204. Exactness side checks: rewind 20 exact, R' mirror exact, local Q8 covariance bit-exact (one random
gauge field, 10 updates).
SEED additions: prepare/seed.py gets the L0 (dark) seed (a = b = A v at x0 on L0 gears; R*-fixed node datum).
- ADDENDUM RUN Z (written Tue Nov 10 11:28:52 UTC 2026, BEFORE running; after seeing A pmp 3/3 bounded, A ppp runaway 440/470, B pmp runaway
  2000/6330 + 1 bounded, and B ppp crashed in the OLD readout at its runaway, fixed 11:26:47: the runaway check now
  precedes the readout; readout ratios overflow-safe; added eps unitarity defect ||chi(U)| - A|/A): re-run B ppp (same
  registration). EXPLORATORY arm B2 (form-C L0, A = 2^15, kappa = 2^18, lam = 4: stiffness 16 lam A^2/D = 1.33; amp =
  A/128 = 256), (1,-1,1) only, 3 seeds, 10,000 updates, same RUNAWAY/BOUNDED definitions. B2 is NOT the registered
  default-composable arm; it is reported as exploratory evidence only.
- ADDENDUM SEED (written Tue Nov 10 11:33:17 UTC 2026, before running tests/test_seed.py): SD1-SD5 run on the v2 default (handed class,
  form C, l0_offset = Q - 1, Q = 2^33 + 1; L = 6, A = 2^12, x0 = (2,2,2)); SD1 adds charge density = 0 at every node
  and gauss_Y = 0 (observe.em.gauss_Y); SD2/SD3 also on the new L0 (dark) seed (one channel, and a rounded M0 band-0
  vector); SD4 on the matter + E1 subsystem (em = "e1", gravity/gauge/choice off, no L0 lapse).
- PRE-REGISTRATION LOCK (written Tue Nov 10 11:36:34 UTC 2026, before running demos/system/mass_lock_check.py; method of R-P1's
  p1e_weakfield_lock.py, own script): default matter (hop 2^31, wilson 2^30) + E1 with sigma = 0, uniform static
  Phi0, uniform k = 0 joint eigenvector of W0 and V (A_m = 2^20), L = 3, T = 3000; cos w from the projection recurrence
  estimator; response ratio = dcos_meas / (2 g_phi Phi0 s_V / D). Masses: MASS_DEFAULT = 4915*2^22 and the control 3Q.
  Phi0 in {256, 3072, 6144} (0.08, 1.0, 2.0 shift quanta per update). PASS (lock absent): ratio in [0.9, 1.1] at 1 and
  2 quanta for MASS_DEFAULT; the 3Q control is expected to lock (ratio far from 1 at 0.08 and 1 quanta).

## RESULTS v2 DEFAULT (written Tue Nov 10 11:38:24 UTC 2026; runs 11:24-11:37 UTC; final suite on the final code 11:37:09-11:37:49:
test_system + test_seed + test_onematter -> 4 tests OK, 39.9 s)
PARAMETERS: dressing coefficients on the built e1d block 8 / 9 (ws) and 16 / 18 (hs = 2): as predicted. Matter cos w0 =
10307502080/25769803779 = 0.3999837; mass + 12 wilson <= D: True.
X1-X10 at Q = 2^33 + 1, L = 3 (results/system/<mode>.json):
| mode | X2 q-lattice (validator) | vacuum / frozen / embedding | rewind | joint mirror 2/2, fixes vacuum | gauge Noether | E1 identities | X7 | X8 | X10 |
|---|---|---|---|---|---|---|---|---|---|
| v2_default (+-+, off Q-1, form C, e1d, wave+bgk, choice) | 1440 (off) | 0 / not expected / n.a. | exact | PASS / yes | 0 | dressed 0/0/0/0 | 1202 (with R1; this run, pre-R1, gave 1106: corrected 12:4x, M-N1) | 2916 (= stage 1) | 0/0 |
| v2_ppp | 1440 (off) | 0 / n.e. | exact | PASS / yes | 0 | 0 | 1106 | 2916 | 0/0 |
| v2_noL0lapse | 0 (off) | 0 / FROZEN / exact | exact | PASS / yes | 0 | 0 | 1106 | 2916 | 0/0 |
| v2_W_split_contrast | 1344 (off) | 0 / n.e. | exact | PASS / yes | 0 | 0 | 1106 | 2916 | 0/0 |
| v2_od2_variant | 1440 (off) | 0 / FROZEN | exact | FAILS (C8) / yes | 0; OD2 C 0 | 0 | 2633 | 2910 | 0/0 |
| v2_compact | 1440 (off) | 0 / n.e. | exact | PASS / yes | 0 | n.a. | 444 | 3018 | 0/0 |
| v2_e1_undressed | 1440 (off) | 0 / n.e. | exact | PASS / yes | 0 | continuity 162, Gauss 162 FAIL (known) | 722 | 2916 | 0/0 |
| v2_P2p16 | 1440 (off) | 0 / n.e. | exact | PASS / yes | 0 | 0 | 1106 | 2916 | 0/0 |
| v2_c2_on (c2 exactness only) | 3744 (off) | 0 / n.e. | exact | PASS / yes | 0 | 0 | 1106 | 2916 | 0/0 |
| legacy_ppp_off0 | 0 (validator ON) | 0 / FROZEN | exact | PASS / yes | 0 | 0 | 1106 | 2916 | 0/0 |
INT64 HEADROOM: every mode ran int64 only: vacuum 20/20 steps, random-state 42 forward + 6 inverse steps, pyint 0
(random_system_state default amplitudes). Python ints appear only past the bound (RUN Z run-aways).
ONE MATTER (A) at Q = 2^33 + 1 (A = 2^16, kd = 2^15, kw = 2^14, MASS_DEFAULT; O1-O5_onematter_Q2p33.json): O1
reciprocal, 0 designated, rank 3 / 4; O3 Noether 0/3024 failures (14 generators); O4 covariance u6 and product PASS; O5
rewind, plain M', Kramers X F X F = N, vacuum fixed PASS; O2 frozen False (known criterion error: dynamical links).
FORM C (L0C_clock.json; U0 = 0.0100002, L = 3, T = 2000, amp 2^20):
- C2 half-angle law from L0 CLICKS: PASS on 13 of 15 massive bands (both classes): |N_click/sqrt(1 - 2U0) - 1| <= 2.8e-6
  (max at +-+ mu = 1.17; all others <= 6e-7). The mu = 6 band (both classes): the F = 0 twin is a period-4 clock whose
  click sizes land on 0, so the registered twin reading is UNDEFINED (nan); with the analytic w0 =
  2 arcsin sqrt((Q-1) mu/(12Q)) (equal to the twin-measured w0 within 2.6e-7 on every other band) the deviation is
  1.3e-7 (declared deviation from the registration).
- Contrast B1-GRAV split (W_split): half-angle reading off by 0.9 % (mu = 8) to 6.0 % (mu = 0.54): low-w0 bands tick
  fastest; its demodulated cos-ratio reading gives 0.99000 = 1 - U0 (EP-correct only demodulated), as Study 7 said.
- C3 universality with Dirac matter: FAIL as registered on every band: N_dirac(demod) = 0.993125 vs N_L0 = 0.98995
  (gap -3.18e-3; tolerance 1.5e-4). DIAGNOSED: B1-GRAV's matter lapse puts the clock factor on the whole on-site entry
  (mass + 6 wilson) W0 and the link factor on the Wilson hops, so the Wilson rest clock gets m (1 - U) + 6 w U:
  N_rest = 1 - U (1 - 6w/m) = 1 - 0.6875 U (6w/m = 1536/4915), exactly the measured 0.993125. The official half-angle
  reading of the Dirac clock gives 1.0023 (> 1). REMEDY (proposed, not built): the matter's Wilson term in the
  DIFFERENCE form (mass m alone with the clock factor; the Wilson Laplacian w W0 (6b - Sum b(x+-e)) with the link
  factor), predicted gap -5e-5 (= sqrt(1 - 2U0) - (1 - U0)). tests/test_l0c.py fails (15 subtests) for these reasons.
RUN Z (Z_*.json): exactness side checks PASS in every arm/class (vacuum 20, rewind 20, M' mirror n = 6, LOCAL Q8
covariance 10 updates).
| arm | (1,-1,1) | +++ |
|---|---|---|
| A: today's L0 weight Q, A = 20857, kappa = 411849, lam 4 (16 lam A^2/D = 0.54) | BOUNDED 3/3 to 10^4 (max W/A ~1.0 = free H-sphere rotation; eps components ~0.01 A; L0 |b| <= 3.1 amp) | RUNAWAY t = 440, 470, 471 |
| B: form-C L0, A = 2^14, kappa = 2^19 (0.33) | RUNAWAY t = 2000, 6330; seed 3 BOUNDED | RUNAWAY t = 420, 790, 60 |
| B2 (exploratory): form-C L0, A = 2^15 (1.33) | RUNAWAY t = 510, 840, 870 | - |
Reading: on today's L0 the sign-class contrast of Study 7 is reproduced on the package (handed bounded, +++ runs
away). On the form-C L0 of the v2 default the handed class is NOT bounded. So c2 stays OFF in the v2 default
(C2_DEFAULT False); c2 ON needs either l0_lapse None/"R" (weight-Q L0, conflicts with decision 3) or a re-tuned c2:
OWNER/manager item. Run log note: B ppp first ran on the old readout and crashed at its runaway (re-run, same
registration); A ppp seed 3 first hung in bigints between 10-step checks (re-run with a check every update).
LOCK (mass_lock.json): MASS_DEFAULT response ratio 1.103 / 0.9985 / 0.9991 at 0.08 / 1 / 2 quanta per update: lock
ABSENT at 1-2 quanta (PASS). 3Q control: 0.000 at 0.08 (LOCKED), 1.000 at 1 and 2 quanta (my expectation of a lock at
1 quantum was wrong at this Q).
SEED (SEED.json, v2 default, L = 6): SD1 legal (Lorenz 0, charge density 0, gauss_Y 0, E1 at vacuum after one update;
2 integers for S2* and node R*); SD2 R*-fixed (S2*, node R*, L0 dark e0, L0 dark band-0); SD3 rewind 10 exact; SD4 bounce
F^-t = R* F^t exact for t = 1..6 (S2*, node R*); SD5 bgk static, offset only in metric.h00: ALL PASS.
PATCH DRAFT (not applied): patches/core_tensor_qlattice_docstring.patch ("iff" -> "if (sufficient; exact condition
K = 0 mod 2Q)"); core/tensor.py unchanged (sha256 ebb01379...).
FROZEN: 142/142 STAGE1_MANIFEST files unchanged; universe24/ untouched; no git.
Integrator files (sha256):
| file | sha256 |
|---|---|
| `layers/system.py` | `790e90e05d91e494cf395fe2b318fe2c40c59166def7545cefcdf79ec3285e69` |
| `layers/gravity_l0c.py` | `eadfeca90b3454a5f58ed6eedd99e132ae93428cd1c0f738a2b819a320f93ab9` |
| `layers/c2_zq8.py` | `a5644947857821cdf888b5ffe7842727644d913402adb1960f01079f374bdcab` |
| `layers/em_dressed.py` | `ef8457514737c2437214f37886f78ee5cb8943b9eafa56a12f4cfa1aac6dc3aa` |
| `layers/onematter.py` | `bba03756d947a1f28e9a73c3d4927941682ebd534bf94cac5c8ec144097366b0` |
| `observe/system.py` | `79f6db20cda4c0d274172be37d5463e32e9f7542590d505b65cc55594cbb2cc3` |
| `observe/readout.py` | `75f582b784a01b0767ddc4e588bd9ae50045246ba3d84797e0984b536a1b0362` |
| `observe/seed.py` | `57e8da8770365a2ed3211faa610d045609ff09e38331171904b1f0451fee82df` |
| `prepare/seed.py` | `8357ea4eef764ac6beedfc647154fa9d8dee0ef91002980eeda7362f5ce7e93b` |
| `prepare/system.py` | `2497c88720737f94158d216cd8343395aa7537372ca18939dda023431936b5ac` |
| `tests/test_system.py` | `929173313b0e656b66b6ce1af25e62cd899ecc221f7f3809d0753d9f01aee675` |
| `tests/test_l0c.py` | `3e5f169530d7aaa1b611207d92d2158c6a416dd3e9c04925c1585399fa38cb00` |
| `tests/test_seed.py` | `812de158a1ae7f73c41356f589ba3224cb6432c769edc6a83b170c87b0a11809` |
| `tests/test_onematter.py` | `431ce1fa96f4d2c41e35852792ceb91c95c08e42b5404afa20f7bc0332b7aefe` |
| `demos/system/zq8_c2.py` | `424ef617c4d45890c36ee2f9e7248d5063fcd3d071787e17958394eacdd5766a` |
| `demos/system/mass_lock_check.py` | `7573f3455e473f0830c3da8eb203108d028c1bde78dbd8ff47fb7f2e52928a60` |
| `README_v1_draft.md` | `1c2b6220566fc703b85477f260f1068d94069e3675e4a54e163435d7afd704ab` |
| `patches/core_tensor_qlattice_docstring.patch` | `243675e45a0a624e9549fa54f044144dbf2e58593615044eb29d8c61657b82d7` |
- PRE-REGISTRATION DIRAC-C (EXPLORATORY proposal, written Tue Nov 10 11:38:57 UTC 2026, before the code exists or runs): new file
  layers/matter_lapse_c.py: the Dirac matter's lapse with the Wilson term in the DIFFERENCE form (mass m W0 on site:
  clock factor 1 - U(x); Wilson Laplacian (w/2) Sum_links (b(x) - b(y))^T W0 (b(x) - b(y)) and the hops: link factor
  1 - (F(x) + F(y))/(2P)); U = F/(2P). Demo demos/system/dirac_formc_check.py: the C3 setup (L = 3, U0 = 0.01, one-way
  read of a static F, T = 2000, amp 2^20, rest clock on the W0 = +1 eigenvector) with this block; PASS iff
  |N_dirac(demod) - (1 - U0)| <= 1e-4 and |N_L0(form C, mu = 2) - N_dirac| <= U0^2/2 + 1e-4; also its reciprocal
  version passes check_reciprocity with 0 designations. NOT part of the default (owner/manager item).
- RESULT DIRAC-C (written Tue Nov 10 11:39:55 UTC 2026; run 11:39:27-11:39:35; results/system/DIRAC_C.json): with the Wilson term in the
  difference form the Dirac rest clock reads N_dirac(demod) = 0.98999980 vs 1 - U0 = 0.98999977 (dev 2.4e-8); gap to
  L0 form C (mu = 2, both classes) = -5.06e-5 (predicted -5.05e-5): PASS. Reciprocal version: check_reciprocity ok,
  953 monomials, 0 designations. CAVEAT (finding): in the OFFICIAL sign-cycle half-angle reading the pi/2-carrier Dirac
  clock reads 1.0033 (> 1, ticks faster) with either matter lapse; L0 (carrier-type, form C) and Dirac agree only when
  each is read in its own reading (L0: official half-angle; Dirac: demodulated). layers/matter_lapse_c.py sha256
  f32dfceeb4838eac34025bd3d320347abac7515e34da6786ac28c4a117463062; demos/system/dirac_formc_check.py sha256
  065825081a87a79df473bf455b01225b8fba27585ed26727b3c30de2e58c3be6. NOT in the default (owner/manager item).
- FINAL HASH (written Tue Nov 10 11:40:02 UTC 2026): README_v1_draft.md d9c473864104893daca6a99719ca27187c81564511c6d7a9640c7c8ecc538f69 (supersedes the table entry; evidence index and section 8 updated after DIRAC-C).
- README E1 wording (written Tue Nov 10 11:40:44 UTC 2026): section 8 E1 entry replaced by the manager's 11:40 wording (labels [DERIVED], [NUMERIC], OPEN kept); README_v1_draft.md sha256 6a8a36a224d502058d0c776abf124872454006ab0bbcba5a7bc269f6f656199d (supersedes the 11:40:02 hash).

## PRE-REGISTRATION R1 + R2 (manager rulings 11:43-11:45; written Tue Nov 10 11:48:59 UTC 2026, BEFORE any edit or run)
R1 (ADOPT): the v2 DEFAULT matter lapse = layers/matter_lapse_c.py, RECIPROCAL, Wilson term in the difference form:
site potential = mass only (m/2) b^T W0 b (clock factor 1 - U, c_site = 1/2 per F/P), link potentials = hops + Wilson
difference (w/2)(b_x - b_y)^T W0 (b_x - b_y) (link factor 1 - (F_x + F_y)/(2P)); the beta = 1 read of the matter uses the
SAME split (clock +G/(4P) on the mass term, link +(9/16)(G_x + G_y)/P on hops + Wilson difference; one-way designated
as in B1-GRAV) so that EVERY clock factor sits on the mass term only. B1-GRAV's split is kept as the contrast mode
"v2_matter_split_contrast" (matter_lapse="split"). Implementation: gravity_blocks(matters=[]) (metric + empty lapse +
beta without matter read) + the two C blocks. Re-run: X1-X10 in every mode (+ the contrast mode), same assertions;
test_l0c C3 with the default's own matter lapse: PASS iff |N_dirac(demod) - (1 - U0)| <= 1e-4 and
|N_L0 - N_dirac| <= U0^2/2 + 1e-4 on every band (mu = 6: analytic w0 as declared); test_seed, test_onematter.
Gravity source check (report): the lapse field's source from the reciprocal C block is b-only:
S(x) = -(1/(2P)) [ (m/2) b^T W0 b + Sum_links-at-x (hop + Wilson gradient energy) ]; reported for a free random matter
state (F = 0, 200 updates, L = 4): (i) the exact two-time Noether energy E = D(|a|^2 + |b|^2) - 2 a^T H b obeys
E(t+1) - E(t) = (b' - a).(r - r') (0 failures expected); (ii) Sum_x S(t) is NOT conserved (relative oscillation
reported) for both splits; (iii) at k = 0 the C source is the mass energy only (no 6w |psi|^2 term), checked on a uniform
state.
R2 (OBSERVATION RULE, read-only, observe/readout.py): proper-time tick = one sign cycle of the click sizes in the
clock's OWN ROTATING FRAME. Carrier identified FROM THE LAW (no species label): for the clock gears, fit the free k = 0
operator H0 = c 1 + kappa L0 where L0 = the k = 0 lapse-touched operator per unit F (from the tensor's F b monomials);
theta = arccos(c/D) rounded to {0, pi/2, pi} (fit residual reported), and checked against the click pattern (raw rate
on the expected side). J = rotation by theta acting on the consecutive click pair (l(t), l(t+1)) (= Rule3's zero-input
map for theta = pi/2: (x, y) -> (y, -x)); own-frame series s(t) = [J^-t (l(t), l(t+1))]_0; tick rate from its sign
cycles. Raw sign-cycle reading kept as contrast. TEST (tests/test_l0c.py, same runs): PASS iff the own-frame tick ratio
w/w0 matches each species' dispersion prediction within 1e-4 (relative): Dirac: sin w_d = (1 - U0) sin w_d0;
L0: sin(w/2) = sqrt(1 - 2U0) sin(w0/2); identified carriers must be pi/2 (Dirac) and 0 (L0) with fit residual < 1e-9.
Manager's estimates to check (U = 0.01): Dirac own-frame 0.98940; L0 mu = 0.54 / 2 / 8: 0.98980 / 0.98932 / 0.98527;
raw Dirac 1.0038.

## RESULTS R1 + R2 (written Tue Nov 10 11:56:02 UTC 2026; runs 11:51:09-11:55:42 UTC, one core, nice)
R1 (matter lapse C adopted in the v2 default; B1-GRAV split = contrast "v2_matter_split_contrast"):
- X1-X10, 11 modes (final run 11:53:21-11:54:01 + test_system re-run 11:55:23-11:55:42 after a docstring edit): every
  wave mode: one Q, vacuum 0 changes, rewind exact, joint mirror PASS 2/2 + fixes vacuum, gauge Noether 0, dressed E1
  continuity / Gauss / Lorenz / global 0, X7 ok (1202 designations; split contrast 1106), X10 0; od2 variant mirror FAILS
  (C8, as before); e1 undressed 162/162 (as before); int64 only (pyint 0) in every mode. test_seed OK, test_onematter OK.
- test_l0c (R1 + R2, 122.8 s): PASS on all 15 massive bands of both classes: C2 |N_click/sqrt(1-2U0) - 1| <= 2.8e-6
  (mu = 6: analytic w0, declared); C3 with the default's own matter lapse: N_dirac(demod) = 0.98999980 vs 1 - U0 =
  0.98999977 (|dev| <= 2e-7 every run), N_L0 - N_dirac = -5.04e-5 .. -5.11e-5 (predicted -5.05e-5; tolerance 1.5e-4).
  Contrast (split): N_dirac(demod) 0.993125 (31 % EP violation of the U-coefficient).
- Gravity source (demos/system/gravity_source_check.py -> results/system/gravity_source.json, free matter L = 4, 200
  updates): (i) exact two-time Noether energy E = D(|a|^2+|b|^2) - 2 a^T H b: E(t+1) - E(t) = (b' - a).(r - r') with
  0/200 failures; (ii) the b-only source total oscillates by 1.74 x its mean (split 1.79): NOT conserved (pi/2-carrier
  doubled frequency); (iii) uniform state: C source = -(m/(4P)) b^T W0 b per node EXACTLY (mass energy only); split
  source = -((m - 6w)/(4P)) b^T W0 b. An exactly conserved first-order stress stays OPEN.
R2 (own-frame proper-time ticks, observe/readout.py): carriers identified from the law: Dirac c = 0 -> pi/2 (fit
residual 1.9e-16), L0 form C c = D -> 0 (1.6e-15). Own-frame tick ratios vs predictions (U0 = 0.0100002): Dirac
0.989391 vs 0.989404 (-1.3e-5); L0 all bands |dev| <= 2.6e-6 (mu = 0.536: 0.989797; mu = 2: 0.989322; mu = 8 (+++):
0.985267): PASS (<= 1e-4). Raw Dirac contrast 1.00376 (ticks faster). Manager's estimates confirmed (0.98940;
0.98980 / 0.98932 / 0.98527; 1.0038).
E1 [NUMERIC] (manager 11:55): ONE-P2 N15 NOT DETERMINABLE (|delta| <= 6e-3 at 2 sigma vs delta_pred 8.6e-4): README keeps
"consistent, NOT demonstrated"; the exponent -1.8 DERIVED only.
README_v1_draft.md updated (sections 2, 3, 6, 8, 9, 10). Final-freeze candidate list: FINAL_FREEZE_CANDIDATES.md.

## PRE-REGISTRATION RC2 BATCH 1 (manager 12:18; written Tue Nov 10 12:19:14 UTC 2026, BEFORE any edit or run; RC1 reviewers use pins)
Default behaviour unchanged except where stated.
1 F-R (ARCH): observe/readout.py readout_class follows the TENSOR labels (GearType.label); check: 0 mismatches between
  the declared class and the tensor label on the v2 default (+-+ and +++); the official click stream is unchanged
  (it already filtered on tensor labels).
2/3 README: departed-AGENTS items 2 and 6 as a separate candidate variant; R2 estimator named exactly
  (own_frame_series + tick_rate), image tone ~0.21 (naive sign count bias ~+1.8e-4, R-P2), redshift law
  delta/(U w0^2) -> -1/3 (Dirac), -1/12 (L0), default Dirac delta = -6.0e-4 (R-P2 verified; our L0C_clock numbers give
  -5.96e-4 and the ratios -0.352 / -0.084 at finite w0).
4 R* for L0-exciting seeds (BANG-1, Study 8 T10d(ii)): find L0's signed relabelling S = chi o P (P a permutation of the
  48 labels, chi signs) with S M_opp(d) S^-1 = M_d for all six directions (M_d = L0's port matrix of direction d, from
  universe24's coupling of the system's body signs), compose S o T (T: chi = +1 -> (b, a, R'(r)); chi = -1 ->
  (-b, -a, r)) into observe/seed.py r_star (package level; core/ untouched). TEST (tests/test_seed.py SD6):
  F^-t(s0) = R*(F^t s0), t = 1..6, on the FULL v2 default for the L0 dark seed (e0 and band-0) AND S2*; also R*(s0) = s0.
  PASS iff all exact. The OLD declared R* (no relabelling) is reported for the L0 dark seed (expected to fail at t = 1).
5 Chiral switch: default_system(chiral=False) keyword (HAND-M1's line); default OFF; "[PENDING OWNER: decision 5]".
  TEST (tests/test_system.py): default_system(chiral=True) builds and composes; its vacuum is fixed for 3 updates and
  a random state rewinds exactly over 3 updates. README section "Chirality (declared candidate, default OFF)".
Re-run: test_system, test_seed, test_l0c, test_chiral.
- ADDENDUM RC2-4 (written Tue Nov 10 12:21:18 UTC 2026, before the code/test exists): L0's signed relabellings found (exhaustive BFS over
  P(0), parity 2-colouring for chi; each verified S M_opp(d) S^-1 = M_d for all six d): 8 per class (the right-Q8
  coset). +++: 4 involutions (S^2 = 1, 24-dim fixed space) + 4 of order 8; handed (1,-1,1): the 4 involutive P give
  S^2 = -1 (Kramers: NO R*-fixed L0 datum) and 4 of order 8 with a 6-dim fixed space. RULE: take the solution of
  minimal order that has a +1 eigenspace, tie -> smallest P(0) (+++: order 2; handed: order 8). P has no fixed label,
  so the one-channel L0 seed is not R*-fixed under ANY valid S: SD6 uses the S-SYMMETRISED L0 dark seeds
  v = Sum_j S^j e_0 and Sum_j S^j v_band0 (prepare/seed.py l0_rstar_vector; data), which satisfy S v = v. The OLD
  declared R* (no relabelling) is reported on these seeds at t = 1. L0 relabelling is applied only with the R' vacuum
  (l0_offset = Q - 1); the legacy offset 0 keeps the old map.
- ADDENDUM RC2-4b (written Tue Nov 10 12:23:08 UTC 2026, before re-running): the S-symmetrised band-0 vector vanishes (S commutes with M0; band 0 = mu 0.536 has no S-invariant vector on the handed class), so SD6's second L0 seed uses the LOWEST M0 band with a nonzero S-invariant vector (recorded in SEED.json).

## RESULTS RC2 BATCH 1 (written Tue Nov 10 12:27:28 UTC 2026; runs 12:22:18-12:27:00 UTC, one core, nice)
Suites on the final code: test_system 3 tests OK (11 modes X1-X10 unchanged results + RC2 checks + E1 without gravity),
test_seed 1 test OK (32.3 s), test_l0c + test_chiral 11 tests OK (190.4 s).
1 F-R: readout_class = the tensor's GearType label. v2 default (+-+): 280 audit / 39 official, L0 all audit,
  dark_l0_violations = []; +++: 232 audit / 87 official (L0 official). The official click stream is unchanged (it
  already used the tensor labels).
2/3 README: departed-AGENTS items 1, 2, 4, 5, 6, 8 as a separate candidate variant; R2 estimator named
  (own_frame_series + tick_rate), image tone ~0.21 and naive-count bias ~+1.8e-4 (R-P2), redshift law -1/3 (Dirac),
  -1/12 (L0), default Dirac delta = -6.0e-4 (ours -5.96e-4).
4 R* with L0's signed relabelling (observe/seed.py l0_relabelling + r_star(body_signs=...); prepare/seed.py
  l0_rstar_vector): handed class: order-8 solution, 6-dim fixed space, 8 solutions; SD6 on the FULL v2 default:
  F^-t = R* F^t exact for t = 1..6 for S2*, the S-symmetrised L0 dark seed from e0 (16 integers) and from M0 band 2
  (96 integers); the OLD declared R* fails at t = 1 on both L0 seeds (as BANG-1 found) and holds for S2*. The one-channel
  L0 seed is not R*-fixed under any valid S (P fixes no label; Kramers involutions have S^2 = -1).
5 chiral switch: default_system(chiral: bool = False) with HAND-M1's line; info["pending_owner"] carries
  "[PENDING OWNER: decision 5]". default_system(chiral=True): blocks + matter2, wsu2, chiral, mlapse2, mbeta2; G = 375,
  19665 monomials; vacuum fixed 3 updates; rewind exact over 3 updates (results/system/rc2_batch1_checks.json).
Changed files (sha256):
| file | sha256 |
|---|---|
| `observe/readout.py` | `d38f431248f739cc8b988178a88864b2641204a083c522b3fac51f7ca9713b0e` |
| `observe/seed.py` | `e989b691ea42f1efa17cfe7d9be2b8b31d61f282ed38cb4a6388f59ed376cb7d` |
| `prepare/seed.py` | `07937ac01b8253adefb147241710994d81fb094f3e6d07e5e5d6bc423534f316` |
| `layers/system.py` | `dba6f46e09332a8615e1f693ce6161934a5c78630a1d1c2de0be8b9c93dccd70` |
| `tests/test_seed.py` | `06550eb38f66b0265ba2adfbcbf28567ff64392612f972963c837298d97f3946` |
| `tests/test_system.py` | `c5d8de7168e3266fdb04214f05bc3b2c0d559f3d7b42c1d5296075a496e7f66d` |
| `README_v1_draft.md` | `6775e6a9837e2e8804f43fefe249cde935be904b8c5ae4c3bf268b9e1a447864` |

## PRE-REGISTRATION RC2 BATCH 2a (manager 12:41; written Tue Nov 10 12:40:37 UTC 2026, BEFORE any edit or run)
Wording/metadata only, plus one switch; dynamics unchanged (the designation why-text of the beta read changes, its
count does not).
1e matter beta read C: own designation text "+G/(4P) clock, +(9/16)(G_x+G_y)/P link" (first-order factors actually
   used) instead of B1-GRAV's second-order G_READ_WHY. 3c info["mirror"]["em"]: the implemented map (x_reversor_core):
   M' on A_d (b, a, R'(r)), Phi (a, b, r) -> (-Phi_next, -b, r), matter K o M'. 5b/5c/6d README wording. M-N1: the X7
   cell of the v2_default row in "RESULTS v2 DEFAULT" is corrected in place to 1202 (R1) with the pre-R1 1106 noted;
   erratum: mass + 12 wilson = 3.35e10 (not 2.31e10).
2  README physics corrections (R-P1): A1 universality limit (EP exact in the tensor for the Dirac pair and L0 only;
   su2/su3/u1 matter and the E1 photon do not read the lapse; E1 field energy does not gravitate: MISSING; gamma = 1 /
   Shapiro for L0 light in the +++ option only); stability sum 3.35e10; BANG-2 uniform-mode drift; N15 delta =
   (1.5 +- 3.2)e-3; u1 matter at 2^20 runs away at t = 3; HORIZON ~1500 updates (beta corner mode at even L, t ~ 1880;
   L = 5 passed U = 0.43 at t = 6100).
3  default_system(electroweak: bool = False) with EW-BUILDER's line; requires chiral=True (ValueError otherwise; the
   composer builds the chiral candidate itself). TEST (tests/test_system.py RC2 checks): electroweak without chiral
   raises; default_system(chiral=True, electroweak=True) builds, its vacuum is fixed for 3 updates and a random state
   rewinds exactly over 3 updates; the default (both OFF) is unchanged (X1-X10 results identical).
Re-run: test_system, test_seed, test_chiral, test_electroweak.
- ERRATUM (written Tue Nov 10 12:41:16 UTC 2026): the PRE-REGISTRATION v2 DEFAULT line 'mass + 12 wilson = 2.31e10' is an arithmetic slip: mass + 12 wilson = 20615004160 + 12884901888 = 3.35e10 <= D = 5.15e10 (the bound holds; System.info computes it exactly). M-N1: the v2_default X7 cell now reads 1202 (R1).

## RESULTS RC2 BATCH 2a (written Tue Nov 10 12:41:45 UTC 2026; run 12:40:37-12:41:33 UTC)
test_system + test_seed + test_chiral + test_electroweak: 22 tests OK (47.1 s). X1-X10 unchanged (v2_default X7 ok,
1202 designations; the beta read C now carries G_READ_C_WHY "+G/(4P) clock, +(9/16)(G_x+G_y)/P link", 496 entries).
info["mirror"]["em"] describes the implemented x_reversor_core map (M' on A_d; Phi staggered). Electroweak switch:
electroweak=True without chiral raises ValueError; default_system(chiral=True, electroweak=True) builds, vacuum fixed
3 updates, rewind exact over 3 (results/system/rc2_batch1_checks.json). README: 5b, 5c, 6d, A1 universality limit,
stability sum 3.35e10, BANG-2 drift, N15 delta = (1.5 +- 3.2)e-3, u1 amplitude regime, HORIZON, section 7c
"Electroweak completion (declared candidate, default OFF)". NOTES: M-N1 cell corrected in place; erratum 3.35e10.
Changed files (sha256): layers/matter_lapse_c.py 0e70977a4e014caf178b74743b3370b78b45bbf166359391e357b96bcf7fb607; layers/system.py 32d74837b2f51eaffd2de3a26a1e6e95ec8e0889aedb398f6e2940617f9803e4;
tests/test_system.py 5eb9bed0e9bd604fa035b20c05d5dc1c356f8402234e511b233dab96b4f07191; README_v1_draft.md b189cee0926e476f949601060d6796b12715c9f8cf2ed98f46ee84d5c31e78a3.

## PRE-REGISTRATION RC2 BATCH 2b part 1 (manager 12:58; written Tue Nov 10 12:54:22 UTC 2026, BEFORE any edit or run)
1 ADOPT GRAV-FIX candidate A (B1-GRAV, layers/gravity_beta_fix.py): after the gravity blocks, the beta block is replaced
  by build_beta_detuned(Q, P, k, field = lapse field, num = 1, den = 2): w_G = (Q-1)/2, source -(k/2) Lap(F^2) (one-way,
  designated as before), static law G = F^2/(2P) unchanged. New keyword beta_form = "detuned" (default) | "marginal"
  (contrast mode "v2_beta_marginal_contrast"). The split matter-lapse contrast keeps the marginal beta (its B1-GRAV
  block carries the split matter's G read). prepare/seed.py gains ra_free_mean (wraps B1-GRAV's prepare/gravity_ra.py:
  exact first-order time mean of the lapse source per Fourier mode; data only); for S2* the first-order mean is 0 and
  its positive mean source is NONLINEAR: no cancellation is claimed.
2 Re-run X1-X10 (all modes + the new contrast), test_seed, test_l0c, test_chiral, test_electroweak: same assertions.
3 HORIZON CHECK (demos/system/horizon_s2star.py): v2 default (detuned beta), S2* (A = 2^16, i = 0, x0 = (2,2,2)), L = 6,
  2,000 updates; samples every 200: max |G_pi| (the beta.G corner Fourier amplitude |Sum_x (-1)^(x+y+z) G(x)|/N),
  U_mean = mean(metric.h00)/(2P), max bits. Report at t = 2000; PASS (bounded) iff no gear exceeds 2^60 in magnitude.
4 README HORIZON note per the manager's wording (B1-GRAV 12,000 bounded; U_mean 0.63 at 12,000, ~1.5e-4/update, nonlinear
  mean source; U = 1 (clock reversal, Study 8) projected near t ~ 14,500).

## PRE-REGISTRATION RC2 BATCH 2b part 2 (manager 13:01; written Tue Nov 10 12:57:18 UTC 2026, BEFORE the edit/run)
C2-TUNE final (the c2 runaway = a 1:2 parametric resonance of the spring choice, not form C): C2_PARAMS = {"A": 2^14,
"lam": 2} (T2), demos/system/zq8_c2.py LAM = 2; no other code change; C2_DEFAULT stays OFF (full default: c2 ON (T2)
horizon ~1825 vs 2843-3688 for c2 OFF; fails at U_mean ~ 0.065: c2's hop modulation is not lapse-dressed, L0's is).
The v2_c2_on X-mode (exactness only) now runs T2. QUICK CHECK (if time): v2 default + GRAV-FIX A + c2 ON (T2), S2*
(A = 2^16), L = 5, 2,000 updates (demos/system/horizon_s2star.py with L/c2 arguments): BOUNDED iff no gear exceeds
2^60; U_mean and max |G_pi| reported.
- ADDENDUM (written Tue Nov 10 13:02:47 UTC 2026, before running): c2-OFF CONTROL for the quick check: same run (v2 default + GRAV-FIX A, S2* A = 2^16, L = 5, 2,000 updates) with c2 OFF, for a like-for-like U_mean comparison (report only).
- FINDING + ADDENDUM (written Tue Nov 10 13:04:49 UTC 2026, before running): the c2 quick check with S2* is BIT-IDENTICAL to its c2-OFF control (U_mean 0.0298615 at t = 2000 in both; same engine stats): S2* never excites L0 (L0's lapse terms and c2's couplings are quadratic in L0's b, so b_L0 = 0 stays 0), hence that check cannot test c2. Re-test with an L0-EXCITING datum: S2* + the S-symmetrised L0 dark seed (l0_rstar_vector, a = b = 2^16 v at x0), L = 5, 2,000 updates, c2 ON (T2) vs OFF (report: bounded, U_mean, max bits).
- NOTE (written Tue Nov 10 13:11:05 UTC 2026): the first c2 + L0-seed run hung in bigints between 200-update samples (RSS 4.4 GB, killed): the horizon script now checks max bits EVERY update and records the runaway time; both L0-seed runs are re-run with it (same registration).
- RESULT + ADDENDUM (written Tue Nov 10 13:11:33 UTC 2026): with the L0 dark seed at a = b = 2^16 v BOTH runs run away (c2 ON at t = 5, c2 OFF at t = 58): that datum is far outside the weak-field regime (L0's form-C source ~ (Q-1)/P |b|^2 drives U to O(1) within ~10^2 updates), so it does not test c2. Re-run (report only) with the L0 seed at a = b = 2^10 v (+ S2* at 2^16), L = 5, 2,000 updates, c2 ON vs OFF.

## RESULTS RC2 BATCH 2b part 1 (written Tue Nov 10 13:11:45 UTC 2026; runs 12:54:32-13:04:24 UTC)
- GRAV-FIX A adopted: default beta = build_beta_detuned(num 1, den 2) via replace_beta (B1-GRAV files, read-only);
  beta_form = "marginal" = contrast "v2_beta_marginal_contrast"; the split matter-lapse contrast keeps the marginal
  beta (its block carries the split G read). prepare/seed.py: ra_free_mean (wraps prepare/gravity_ra.py).
- Suites (12:57:57-13:00:25): test_system (13 modes incl. the new contrast) + test_seed + test_chiral + test_electroweak
  + test_l0c: 23 tests OK (147.7 s). v2_default with the detuned beta: rewind exact, joint mirror 2/2, gauge 0,
  dressed E1 0, X7 ok 1202.
- HORIZON CHECK (results/system/horizon_s2star_detuned.json): S2* A = 2^16, L = 6, 2,000 updates: BOUNDED (max 31
  bits). At t = 2000: max |G_pi| = 3.55 (0 until t = 1400; 0.35 / 1.66 / 3.55 at 1600 / 1800 / 2000), U_mean = 0.0020
  (2e-5 at 200, 2.4e-4 at 1400). Engine: 144 int64 + 1856 Python-int steps (the exact int64 bound fails early with
  A = 2^16 data; values stay <= 31 bits).
- part 2: C2_PARAMS lam = 2 (T2), zq8_c2.py LAM = 2; C2_DEFAULT OFF. The v2_c2_on X-mode (T2) passes the exactness
  assertions. Quick check as specified (GRAV-FIX A + c2 ON, S2*, L = 5, 2,000): BOUNDED, U_mean 0.0299 at t = 2000,
  BUT bit-identical to the c2-OFF control (S2* never excites L0; c2 and L0's lapse are quadratic in L0's b): it cannot
  test c2. L0-exciting data at a = b = 2^16 v: both run away (c2 ON t = 5, OFF t = 58: outside the weak-field regime).
- TIME BOX (written Tue Nov 10 13:14:52 UTC 2026, before re-running): the 2^10 L0-seed c2-ON run was still bounded after 3 min (~72 MB) but too slow for the time box (Python-int steps); both 2^10 runs are re-run with T = 600 (c2 ON, then OFF), report only.
- RESULT part 2 re-test (written Tue Nov 10 13:16:02 UTC 2026; results/system/horizon_s2star_detuned_L5_{c2_,}l0seed10.json): S2* + L0 seed
  a = b = 2^10 v, L = 5, 600 updates: c2 ON (T2) BOUNDED, U_mean 0.01304 at t = 600; c2 OFF BOUNDED, U_mean 0.01356; both
  all-int64. No horizon shortening by c2 at 600 updates after GRAV-FIX A (short test; a long re-test is OPEN). README
  updated (sections 2, 8, 9, HORIZON, evidence).

## PRE-REGISTRATION RC2 BATCH 3 (manager 13:16; OWNER approved all decisions 13:09; written Tue Nov 10 13:17:06 UTC 2026, BEFORE any edit/run)
1 DECISION 5 CLOSED, "hands ON": default_system defaults chiral=True, electroweak=True (flags kept; both OFF =
  chiral=False, electroweak=False; electroweak without chiral raises). EW removes "matter"'s mlapse/mbeta (lapse x |Phi|^2
  handles the doublet). X1-X10 on the new default and every mode, with the SAME assertions where they still apply:
  X1, X3 vacuum, X4 rewind, X7 reciprocity, X2 (legacy), X3 frozen (no L0 lapse): asserted in every mode. X5 (the
  integrator's joint mirror K o M' on "matter" only) and X6 dressed-E1 identities: asserted in hands-OFF modes only
  ("v2_handsOFF" = the R1 default; "v2_matter_split_contrast" is run hands-OFF since EW would double-dress the split
  lapse); in hands-ON modes they are REPORTED (the chiral layer's own T_phys = C K o M' is its declared mirror,
  test_chiral CH6), not forced. Gear / monomial / designation counts and Engine int64/pyint steps reported.
  test_seed: assertions on the hands-OFF system (R* knows L0's relabelling but not the chiral maps); the hands-ON
  default's S2* bounce with the integrator's R* is REPORTED. test_chiral, test_electroweak, test_l0c re-run unchanged.
2 README: "Owner decisions (13:09, approved)" items 1-9 (one line each); the narrow rank-4 kind added to the design rules
  next to the OD4 springs; defaults table updated.
3 No final manifest.

## RESULTS RC2 BATCH 3 (written Tue Nov 10 13:21:45 UTC 2026; runs 13:17:06-13:21:15 UTC)
- Defaults: chiral=True, electroweak=True (info["chiral"/"electroweak"]["status"] = ON BY DEFAULT, decision 5 CLOSED).
- test_system (14 modes incl. v2_handsOFF) 3 tests OK (36.0 s, final code); test_seed OK; test_l0c OK; test_chiral and
  test_electroweak: 6 of their tests ERROR/FAIL ("duplicate namespace 'matter2'") because their helpers call
  default_system() expecting hands OFF and compose the chiral layer again; with a hands-OFF base (scratchpad harness,
  default_system patched to chiral=False, electroweak=False by default, no file edited) all 18 pass (11.4 s). Fix =
  one line in their helpers (HAND-M1 / EW-BUILDER files: not edited by the integrator).
- Hands-ON default (v2_default): G = 375, 18623 monomials, rank 4, designations 706 (hands OFF: 319 / 10549 / 1202;
  EW removes mlapse/mbeta = 496 G reads); X1 ok, X3 vacuum 0, X4 rewind exact, X7 ok, gauge Noether 0, int64 only
  (pyint 0); X5 integrator joint mirror FAILS 2/2 (fixes vacuum; the chiral layer's mirror is T_phys, CH6);
  X6 dressed E1: Lorenz 0, continuity 162/162, Gauss 162/162, global charge 6/6 FAIL (charged W moves charge to matter2;
  E1 sources pair 1 only: hypercharge limitation, decision 5(A)); X10 several-writer gears 16, designated-and-force 0.
- Seeds (hands-ON report): S2* legal, R*-fixed, rewind exact; bounce with the integrator's R* True at t = 1, False at
  t = 2, 3 (no chiral maps). Hands-OFF SD1-SD6 PASS.
- README: section 0 "Owner decisions (13:09, approved)" items 1-9; rank-4 kind in the design rules; defaults table;
  section 7b' (hands ON in the composed default); 7b/7c status.
Changed files: layers/system.py c944c7f34d7eecff8b6849a8659d044486b036aaa3ab8c6f4e7876ce820a6e02; tests/test_system.py 1ada0bc0662e9f5f9111bc17ded8c98be19caa7c4e52b41a6e6316f3f9ea1e00;
tests/test_seed.py f8b9d2fef61a5bd3f25e707b1bc901d2197ae6793010e7427428fb80ffdb4c9b; README_v1_draft.md 4b6031a197b89054d6c29adb408a190f717b9ebb62a56f9b518419ba10c9c883.

## PRE-REGISTRATION RC2 BATCH 4 (manager 13:25; written Tue Nov 10 13:24:34 UTC 2026, BEFORE any edit or run)
1 AUTHORISED one-line fixes (integrator, manager-authorised 13:25, hands-ON default): tests/test_chiral.py lines 55, 290,
  296 and tests/test_electroweak.py lines 343, 380 -> default_system(Q, chiral=False, electroweak=False, ...) (the base
  their helpers assume). sha256 before: test_chiral.py c078cbf019bdfd9583e76af6598aea1035e1d0c6d8dae345b48923172f276eaa, test_electroweak.py 4ed6e1efe8dd54647ae3c02083a7ae4af46fa7eb86af9cdb303b9c5f05d94dae. Re-run both (expected 18/18 OK, as
  the scratchpad harness showed).
2 MIRRORS WITH HANDS ON (observe/system.py, observe/seed.py; prepare/chiral.py's building blocks read-only):
  X_on = T_phys extended to the full system: Phi -> (+Phi_next, +b, R'(r)) (E1 staggered map composed with the C-flip of
  the E1 fields), M' on every other gear, A_d negated after M' (net (-b, -a, r)), then the chiral linear maps (matter and
  matter2: kron(1_2, C K); Higgs: sig; W links and 2-paths: sig). Check X F^n X F^n = X^2 (Kramers central element) on 2
  random states (n = 6) and that X fixes the vacuum (X5 on the hands-ON default).
  R*_on = the integrator's r_star (Gamma on matter, E1 inversion maps, L0 relabelling, (b, a, R') elsewhere) EXTENDED by
  the chiral layer's inversion maps about the same centre: matter2 Gamma, Higgs sig, W links sigL = sig conj (re-based),
  2-paths sigL + reversal (prepare/chiral._two_path_shift rule). Target: S2* bounce F^-t = R*_on F^t exact for
  t = 1..6 on the hands-ON default (L = 6, A = 2^12). If a composition fails, the obstruction is reported.
3 README X6 wording with hands ON, checked against NOTES_electroweak.md EW4.
- AUTHORISED EDIT applied (integrator, manager-authorised 13:25, hands-ON default; written Tue Nov 10 13:24:34 UTC 2026): tests/test_chiral.py lines 55, 290, 296 and tests/test_electroweak.py lines 343, 380 now call default_system(Q, ..., chiral=False, electroweak=False). sha256 after: test_chiral.py 6ed81aafa7ab0ddf69048e285e03f0952a5227a3a259e53dc645208a2ebc1903, test_electroweak.py fb1869ba5fc534cc7071c5bb749f4e131e5c04144d1a52b673e9d298972b73cc.

## RESULTS RC2 BATCH 4 (written Tue Nov 10 13:29:30 UTC 2026; runs 13:24:34-13:28:57 UTC)
1 Authorised fixes applied (see above); test_chiral + test_electroweak: 18 tests OK (12.0 s).
2 MIRRORS WITH HANDS ON: joint_mirror_hands_on (observe/system.py): X F^n X F^n = X^2 exact for n = 1, 2, 6 on 2 random
  states and X fixes the vacuum on the hands-ON default (L = 3); X5 PASS in every hands-ON wave mode (default, +++,
  no L0 lapse, W_split, e1 undressed, P = 2^16, c2 on, beta marginal, legacy off 0 with rhoL0); FAILS for the OD2 variant
  (C8, as before) and for compact EM (OBSTRUCTION: under C the compact U(1) links emu1 need U -> U* conjugation, not
  composed in; reported, not asserted). r_star_hands_on (observe/seed.py): SD7 on the hands-ON default (L = 6,
  A = 2^12): S2* R*-fixed and F^-t = R*_on F^t exact for t = 1..6; the S-symmetrised L0 dark seed also exact (report).
  Gamma = J'K W0 = W0 J'K (checked). test_system 3 tests OK (49.6 s, final code); test_seed OK (in the 13:26:44 run).
3 README X6 wording per the manager, checked against NOTES_electroweak.md: EW4/EW4b (Q = L3 + R3 + BL/2 incl. the W
  links' adjoint action: exact GLOBAL Noether, 0/6), EW4 (photon = J' on pair 1 only), EW5b (t1, t2 54/81 from the
  charged W), NOT BUILT local U(1)_Y (route B: one U(2) link per face). No contradiction found.
Changed files: tests/test_chiral.py 6ed81aafa7ab0ddf69048e285e03f0952a5227a3a259e53dc645208a2ebc1903; tests/test_electroweak.py fb1869ba5fc534cc7071c5bb749f4e131e5c04144d1a52b673e9d298972b73cc;
observe/system.py a151e5f0d670bac4be49b801c27e1f8982d7ba0874cb6fdd3f579096b916aee0; observe/seed.py a1cc8afd39bba34db3d2a08288f5670e46d0b258dbbfeeb82ca4f0e257c79b85; tests/test_system.py
36bdb8eeca86be91afb95469eaa12d3132626abc7a7379251543db8d356e9f41; tests/test_seed.py bde1cf410a852756be21a41f9d5c13119c65cd317a782aef746d2b50d64964b3; README_v1_draft.md 7373db0af56015c8abceb10fad5e3df8844bbb1a3a0f3e498b443268ffc27f78.
STOP: no further edits until the RC2 freeze announcement.

## owner decision v8-1, 14:37 UTC, FIX-i per s18/AGREE_STAB.md (applied by ONE-A, Tue Nov 10 14:45:16 UTC 2026)
Owner approval (manager 14:39 UTC): FIX-i is THE hands-ON default. Edit (authorised exception, smallest form): layers/electroweak.py
compose_electroweak now builds gwb with build_graviweak_b(lam_H = 0, lam_L = 0) (keyword defaults gwb_lam_H = 0, gwb_lam_L = 0;
gwb_lam_H = None, gwb_lam_L = 4 rebuild the earlier L2(b) default as a contrast); the singlet-half hop is kept; info["electroweak_fix_i"]
records it. No other package source file edited. layers/electroweak.py sha256 58ffc050...295491 -> 9faee4a7...47b5c3.
default_system() tensor: dynamics_fingerprint 473b7b9f...346446 (ARM B) -> b51d3f2c...cbfc8e8 (= STAB-B FIX_S_built, R9/R10);
full fingerprint 1d279f1b...68fe -> 81ce08d5...ae4c; G 375 -> 375, monomials 18,623 -> 18,553 (gwb 1222 -> 1152 terms), rank 4,
designations 706 -> 706. Evidence: scratchpad s22/ONE-A_work/fixi_*.
