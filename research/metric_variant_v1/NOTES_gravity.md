# NOTES_gravity — stage-1 GRAVITY layer (builder B1-GRAV)

All stamps are `date -u` at the moment of writing. Every test and demo is pre-registered here BEFORE it is run;
results are appended below their pre-registration, never edited into it. Files of this layer: `layers/gravity.py`,
`prepare/gravity.py`, `observe/gravity.py`, `tests/test_gravity.py`, `demos/gravity/`, this file. Nothing in `core/`,
in other builders' files or in `universe24/` is touched. No git.

## Design summary (written Tue Nov 10 09:24:25 UTC 2026, before any gravity code exists or runs)
Sources ported: s0/SYSTEM_DESIGN_v5 (§0-§3, §5, §6, §8 OD2/OD4, §1b, §11), s0/SYSTEM_DESIGN_v3 §1-§5, s1/AGREE_M
(X1-X13, Y1-Y15), s1/M_CONVERGENCE_SPEC, s2/AGREE_M (W1-W9, W5b), s2/M2_WSB*, s3/AGREE_M (A10-1..A10-10),
s3/M_tmunu_local.py, s4/AGREE_M (A8, B8, C1, P-vi, P-vii(c)), s4/M_work/M_grav_acc.py, M_grav_mirror_bounded.py.

Conventions. ONE divisor D = 6Q, Q ODD. Every new gear starts at (0, 0, r0) with r0 = 3Q - 1 (mid-range: no Y10
zero-mode kick; fixed by the parity-preserving reversor R'(r) = D - 2 - r on even r, which needs odd Q). Deviation
form: every term targeting a new gear vanishes when the layer's own gears are 0. The potential scale P (a power of
two) and an integer k fix Q = 2Pk + 1, so that every coupling coefficient below is an integer.
Rule3 identity used everywhere: 6Q (b' + a) = 2u + r - r'.

1. METRIC block `build_metric`: 10 gears h00, h0x, h0y, h0z, hxx, hyy, hzz, hxy, hxz, hyz (trace-reversed hbar^{mu nu}
   in board units, WS-B W1), each the ONE headroom stencil u = (Q-1) Sum_6 b + 6b (= gradient of
   Phi_wave = Sum_x [(Q-1) Sum_{+axes} b(x) b(x+e) + 3 b(x)^2]); c_Q^2 = (Q-1)/(3Q). Yee: h00, hii node gears; h0i
   link gears (axis i); hij node-stored plaquette composites (physical position x + (e_i+e_j)/2). Readout label
   "audit" (OD1). Sources are added by the coupling blocks.
2. MATTER INTERFACE `MatterSpec`: gears + order (2 = second-order/KG-type, carrier 6Q; 1 = first-order, carrier 0)
   + carrier per gear + on-site (mass/clock) entries H_ts + transport entries (Laplacian weights w_t and generic
   link entries c b_t(x) b_s(x+e)). The matter block is the gradient of Phi_m = Sum_x [carrier/2 b^2 + Phi_site +
   Sum_links Phi_link], so every matter block built from a spec is reciprocal by construction. Test matter (minimal,
   stage-1 only): on-site atoms, circulating load pairs (and the pi-carrier anti-load), headroom light, KG.
3. UNIVERSAL LAPSE block `build_lapse` (equivalence principle), ONE potential
   Phi_int = - c_site (F/P) Phi_site - c_link ((F(x) + F(x+e))/P) Phi_link,  U := F/(2P),
   c_site = 1, c_link = 1 for second-order matter (clock factor 1 - 2U on the mass entries, link factor 1 - 4U on the
   transport entries: gamma = 1); c_link = 1/2 is the 1911 lapse-only CONTROL (link factor 1 - 2U); first-order matter
   takes half of each (N, N/psi^2). Action (metric x matter -> matter) and source (matter x matter -> metric: the
   on-site mass energy -Phi_site/P plus the link gradient energy) are the two derivatives of the SAME Phi_int, so
   Newton III is exact and the checker passes without designations.
4. BETA = 1 block `build_beta` (G auxiliary, S1 X1): G gear with the headroom stencil and source -k Lap(F^2) (exact
   discrete Leibniz; Q - 1 = 2Pk gives G = F^2/(2P) static). RECIPROCAL ATTEMPT: Phi_G = -k Sum_x G(x) Lap(F^2)(x)
   is a potential; its F-derivative is the back-reaction -2k F Lap G on F (O(U^3) in the static exterior, beta
   unchanged); option reciprocal_source=True adds it, False keeps the agreed one-way source (designated). The matter
   read of G (clock factor + G/P, light link factor + (17/8)(G_x + G_y)/P) CANNOT be reciprocal at rank 3: its
   partner would source G with the matter energy, giving G = F^2/(2P) - F at FIRST order (the lapse is destroyed);
   it is designated one-way. Reciprocal alternative = OD4 `build_beta_rank4`: on-site quartic
   Phi += (F^2/(2P^2)) Phi_site (minus sign: Phi_site < 0 for matter) and on-link (17/8)(F_x F_y/P^2) Phi_link.
5. N-DESIGN `build_ndesign` (static all orders, S1 X5/X10/X11/Y15, split + detuned remainders): nu = P(N - 1) with
   u = 6Q nu + (Q-1) Lap nu + k[nu Lap nu - Sum_e (delta_e nu)^2] - sigma n C (York weight), remainder gears a2
   (= P eps^2), crem, lamrem in Laplacian form with detuned weights; density gear n (static). Clock factor
   A = 1 + 2 eps + a2/P, light weight lambda = 1 + 4 eps + lamrem/P. OD4 option: light weight = A*C instantaneous
   (on-link quartic, no lamrem gear). Its self-law and auxiliaries are designated one-way (non-polynomial potential;
   feed-forward Leibniz chain; prescribed density = MECHANISM).
6. OD2 `build_od2`: hij F-gears sourced by b-only link-local stress bilinears; h0i, h00 ACCUMULATORS
   u = D b - (D/2)[Div(b) - Div(a)] (K = 2u = 0 mod D: rounding-free, r constant), so the harmonic constants
   C^i = h0i(t+1) - h0i(t) + D_j h^{ji}(t), C^0 = h00(t+1) - h00(t) + D_i h^{0i}(t) are EXACTLY conserved; matter reads
   the accumulators at centred times (look-ahead via the accumulator formula: two-time reads, acyclic). No remainder
   reads.

## PRE-REGISTRATION of the exact acceptance tests (written Tue Nov 10 09:24:25 UTC 2026, before any run)
Pass criteria EXACT (bit for bit) unless stated. Standard composition S = reference (+++, Q) + metric + test matter
(atoms of two species, circulating load pair, light) + lapse (+ beta where stated). P = 2^10 and k = 4 (Q = 8193)
unless stated; L = 6 or 8; seeds fixed in tests/test_gravity.py.
G1 VACUUM. Every composed system (S; S + beta (both options); S + beta_rank4; N-design + test light/atoms; OD2 chain):
   the vacuum (reference (0,0,2Q), new gears (0,0,3Q-1)) is unchanged for 20 updates and emits no click (official
   or raw) from new gears; with a random reference state and new gears at vacuum, the new gears stay at vacuum and the
   reference sector equals the plain reference run (deviation form) for 20 updates.
G2 REWIND. Random non-vacuum states (|values| <= 2^20 in the new gears; field gears up to P) of every composed system
   above, 30 forward + 30 staged-inverse updates return the initial state bit for bit (int64 or Python-int path).
G3 PLAIN MIRROR. For every b-only composition (S, S + beta, N-design, beta_rank4): M F^n M F^n (s) = s, n = 20.
G4 RECIPROCITY. check_reciprocity: metric + test matter + lapse PASSES with ZERO designations; lapse with gamma = 1911
   control also passes; beta with reciprocal_source=True: only the matter's G-read monomials are designated, all
   designations listed; reciprocal_source=False: G-source monomials designated in addition; beta_rank4: PASSES with
   zero designations; N-design: PASSES with its designations listed; OD2: b-only part passes with the centred-read
   designations listed. A CONTROL: deleting the lapse SOURCE terms (action without its reaction) FAILS the checker.
G5 DRESSED LORENZ / HARMONIC IDENTITY (10-gear metric, any sources): with s^{mu nu} the input of gear mu nu minus its
   stencil, C^nu(t) = [h^{0 nu}(t+1) - h^{0 nu}(t)] + Sum_i [h^{i nu}(t) - h^{i nu}(x - e_i, t)] satisfies
   6Q(C(t+1) - 2C(t) + C(t-1)) - 2(Q-1) Lap C(t) = 2 D_mu s^{mu nu}(t) - D_mu (r^{mu nu}(t+1) - r^{mu nu}(t))
   at every node, nu = 0..3, every update of a 40-update run with random matter driving all ten gears (exact).
   Also: with an exactly conserved prescribed source realised by ON-SITE OSCILLATOR gears (diagonal W-superpotential,
   W^{0i0i} = b of an oscillator gear, T = D D W, B3-legal) and C = 0 initial data, the LINEAR identity has zero
   source term (D_mu s = 0 exactly at every node and update), so C is driven only by the remainders (reported).
G6 STATIC GAUSS LAW (exact flux identity): for the lapse field F (= h00) with the lapse source, summed over any box R:
   6Q Sum_R [F(t+1) - 2F(t) + F(t-1)] - 2(Q-1) Flux_dR F(t) = 2 Sum_R src(t) + Sum_R (r(t) - r(t+1)), exact for boxes
   of half-width 1, 2, 3 around the load at every update; and the time-summed (period-mean) form over a window.
G7 OD2 MOMENTUM CONSTRAINTS. With the accumulator chain and arbitrary sources (random matter): (a) the accumulators'
   remainders never change (rounding-free); (b) C^i(t) and C^0(t) are constant at every node for all t (exact);
   (c) with prepared C^i = C^0 = 0 initial data they are 0 forever; (d) the Hamiltonian-constraint dressed identity:
   the h00 analogue of G5's identity with its remainder terms holds exactly (bit for bit).
G8 T^{mu nu} TWO-TIME IDENTITIES (s3 A10-1) on the engine: a KG test-matter block (u = (Q-1) Sum_6 b + (6 - mu) b) run
   by the Engine, read from three consecutive snapshots: the energy identity
   D[e(t+1) - e(t)] + Sum_i D[J^i_x(t) - J^i_{x-e_i}(t)] = (b(t+1) - b(t-1))(r(t) - r(t+1)) (with the mass term) and
   the momentum identity with the symmetric plaquette stress hold at every node (exact).
G9 SUPPORT FACTS: Tensor.support_violations() lists, for the composed system, exactly the expected families: the
   link-gear light stencil of h0i (parallel links), the lapse link terms on link-gear-free matter are support-legal;
   the list is reported (design facts, not failures).
G10 OD2 STAGGERED REVERSOR (CONJECTURE test, P-vii(c')): a candidate staggered map X built like S4-M's
   M_grav_mirror (matter K o M, field gears M, h0i (a, b) -> (-h0i_next, -b), h00 (a, b) -> (h00_nn, h00_next));
   report X F X F = id (up to declared central elements) on 10 random states. Outcome reported either way.

## Amendment to the pre-registration (written Tue Nov 10 09:35:58 UTC 2026, still BEFORE any test run; manager rulings 09:28 and ~09:35)
- G1-G4: every composed system containing ref.* is built with compose(..., q_lattice=("ref.*",)) (must not raise:
  no gravity term writes into an L0 gear) and every block declares Q.
- G3 uses the DECLARED reversor as data (Block.params["reversor"]): X = rhoL0 on ref.* and M' (Mp: (b, a, R'(r)),
  R'(r) = D-2-r even / D-r odd) on every new b-only gear; PASS iff X F^20 X F^20 (s) = s for 2 random states per
  b-only system AND is_fixed(X, joint vacuum) (ref (0,0,2Q), new gears (0,0,3Q-1); Q odd; for even Q no remainder is
  R'-fixed, stated, not tested). The plain M (uniform) is reported as a second check.
- G10 (OD2, a-read gears): the declared staggered map (hij: Mp instead of M is also tried) is reported; joint vacuum
  fixedness of the staggered map is reported.
- Test-data source blocks (G5) declare Q.

## DEVIATION recorded honestly (written Tue Nov 10 09:47:04 UTC 2026)
First run 09:36:13: G1 PASSED for all 8 systems (results/gravity/G1.json, 09:36:14). G2 did not finish: the registered
random-state amplitudes (matter |b| <= 2^20, field gears up to P/8) are lattice-scale "hot" states whose rank-3 couplings
grow doubly exponentially (diagnostic, max bit length per update over 8 updates, L = 5: S_GR 12 -> 334 bits;
S_beta_rank4 18 -> 23,573 bits; OD2 14 -> 149), so the exact Python-int rewind became too slow; the run was stopped by
hand at 09:46 (no G2 verdict was produced). AMENDED G2/G3 (before re-running them): random states with matter
|v| <= 16 and field/auxiliary |v| <= 4 (reference |v| <= 20), 20 forward + 20 inverse (G2) and n = 20 (G3); plus an
extra G2 regime with the original amplitudes but only 5 updates forward + 5 back (Python-int path exercised). The
exactness claims are unchanged; only the amplitudes/lengths of the random data change.
Second amendment (written Tue Nov 10 09:52:39 UTC 2026, before re-running G2/G3): even with matter |v| <= 16 / field |v| <= 4 the
small-P systems used for the exactness tests (S_beta_rank4 P = 16, ND P = 16, OD2 P = 64) grow on lattice-scale random
data (bits 6 -> 300 within 6-18 updates; a random field of 4 units is U ~ 0.1 at P = 16). Exactness is still
testable on growing states; to keep the integers below ~10^3 bits: G2 n = 20 for the S systems, n = 8 for
S_beta_rank4 (matter |v| <= 4) and the ND systems, n = 12 for OD2; the registered-amplitude regime keeps n = 5; G3 n = 20
for the S systems, n = 8 for S_beta_rank4 and ND; G10 n = 12. Pass criteria unchanged (bit-exact).

## G-suite first full run (09:52:39-): results and one FAILURE (written Tue Nov 10 09:54:34 UTC 2026)
- G1 PASS, G2 PASS, G3 PASS, G5 PASS, G6 PASS (numbers in results/gravity/*.json; summarized at the end).
- G4 FAILED on the first run: the OD2 system's accumulator b-reads (u_h0i += -(D/2) Div_i hbar(b), u_h00 += -(D/2)
  Div_0 h0(b)) are b-only couplings without partners and were not designated (my omission in build_od2, not a checker
  issue). Fix (code, not test): these monomials now carry designated_one_way = OD2_ACC_WHY (slaved accumulator =
  integration of the harmonic condition, not a force). G4 is re-run unchanged after the fix.

## PRE-REGISTRATION demo D1: clocks, universality, beta = 1, field profile (written Tue Nov 10 09:54:47 UTC 2026, before the script exists)
Script demos/gravity/d1_clocks.py. P = 2^20, k = 24, Q = 2Pk + 1 = 50,331,649 (odd). L = 32. Blocks: metric (h00 only),
load (circulating clock pairs, mu = 2P*3, smooth ball radius 2.5 at c = (16,16,16), amplitude chosen for U(3) ~ 0.08),
anti-load (pi-carrier pairs, same amplitude) at the antipode (0,0,0) (net source ~0: no closed-board zero mode;
MECHANISM, as the studies' anti-lump), atoms A (mu = 2P*1), B (mu = 2P*4) [lapse only], C (mu = 2P*1) [lapse + beta G
read], beta block (G, reciprocal_source=True). Atoms (amplitude 2^12, self-field U < 1e-7) at x-axis distances r = 3, 4,
5, 6, 8, 10, 12 and diagonal (2,2,2), (3,3,3), (4,4,4) from c, A/B/C co-located. 1300 updates; readout window
t = 300..1300 (after the field settles; images included: the torus field is the reference since predictions are LOCAL).
Readouts: CLICK space: per atom, official click quotients -> interpolated sign changes -> w_click; N_click =
sin(w_click/2)/sin(w0/2) (half-angle law; w0 from cos w0 = 1 - mu/(6Q)); EVENT space (labelled): window means of F and G
at the atom node.
Pass/report criteria:
 (a) lapse-only atoms (A, B): |N_click / sqrt(1 - Fbar/P) - 1| <= 3e-4 at every atom (agreed number: probes follow
     sqrt(1-2U) to 3.4e-4);
 (b) universality: |N_click(A)/N_click(B) - 1| <= 1e-4 at every co-located pair (also the raw w_A/w_B / (w0A/w0B) ratio,
     whose O(w0^2) lattice deficit is reported, not a criterion);
 (c) beta atoms C: |N_click^2 - (1 - Fbar/P + Gbar/P)| <= 5e-4 (reading their own G), G vs F^2/(2P): Gbar/(Fbar^2/2P)
     reported per atom; beta_click := (N_click^2(C) - 1 + 2U)/(2U^2) with U = Fbar/(2P), its mean over atoms with
     U > 0.03 reported (expected 1 within ~1e-2 at these U); control beta from A atoms (expected 0);
 (d) field: Fbar along the axis vs the exact static lattice solution of the time-mean source on the torus (float FFT,
     labelled diagnostic): ratio within 2 % for r = 2..10; log-slope of Fbar vs r reported;
 (e) exactness: the run rewinds exactly from t = 1300 to 0 (Python ints if needed).
Third amendment (written Tue Nov 10 09:55:02 UTC 2026): G7's random OD2 data (P = 64) also grow (bits ~ 336 by update 18), so the
44-update run was stopped by hand; G7 now uses 14 updates (identity windows t = 2..10); criteria unchanged (exact).

## PRE-REGISTRATION demo D2: Shapiro delay (GR vs 1911 lapse-only CONTROL) and redshift via light (written Tue Nov 10 09:57:22 UTC 2026)
Script demos/gravity/d2_light.py. P = 2^20, k = 24 (Q as D1), L = 40, centre c = (20,20,20). Load and anti-load as in
D1 (U(3) ~ 0.08), the field h00 PREPARED as the rounded static lattice solution of the load source (MECHANISM
preparation of a settled field: a = b = F_static), so the light crosses a settled field. Two light gears in the SAME
run: lightGR (lapse block gamma = GR: link factor 1 - 4U) and light1911 (separate lapse block gamma = 1911: link factor
1 - 2U = the clock factor), both started with the same plane-front pulse along +x (carrier k = 0.8, sigma = 8,
amplitude 2^12, no transverse envelope) centred at x = c - 15; a TWIN run (no load, no anti-load, F = 0) with the same
light. Atoms (mu = 2P) at the near detector N = (c, c+b, c) and the far detector F = (c+15, c+b, c), b = 4 and 6.
Readouts (click space: light quotient sizes): arrival time at a detector = centroid of quotient^2 over the passage;
delay = loaded - twin. Criteria: (a) Shapiro ratio delay_GR/delay_1911 at the far detectors (b = 4, 6) in [1.8, 2.2]
(agreed 2.00-2.11; 1.987 own ticks); (b) frequency conservation: light click frequency at N and F equal within 1e-2;
(c) redshift via light: (w_light/w_atom)_N / (w_light/w_atom)_F vs the GR first-order prediction
sqrt((1 - F_F/P)/(1 - F_N/P)) within 3e-3. Also reported: delay vs the line integral of 2U (GR) and U (1911).

## RESULTS G1-G10 (written Tue Nov 10 09:58:55 UTC 2026; runs 09:52:39-09:52:43 (G1-G3, G5, G6) and 09:55:02 (G4 re-run after the
## OD2 designation fix, G7 with 14 updates, G8-G10); raw numbers in results/gravity/G*.json)
| test | verdict | numbers |
|---|---|---|
| G1 vacuum | PASS | 8 systems (S_GR, S_1911, S_beta_recip, S_beta_oneway, S_beta_rank4 (rank 4), ND_rank3, ND_rank4 (rank 4), OD2), L = 5, all with ref.* and q_lattice=("ref.*",): vacuum unchanged 20/20 updates, 0 raw clicks from new gears; random reference + new gears at vacuum: 0 reference mismatches vs the plain reference run, 0 new-gear deviations (deviation form). |
| G2 rewind | PASS | 16/16 runs (8 systems x 2 regimes) return bit for bit, 0 inverse mismatches; registered-amplitude regime ran on the Python-int path (up to 2,089 bits, rank-4 beta); OD2 has 4 inverse stages (hij -> h0i -> h00 -> matter). |
| G3 mirror | PASS | declared reversor (rhoL0 on 48 ref gears, M' on 6-18 new gears): X F^n X F^n = id on 2/2 states for all 7 b-only systems (n = 20, rank-4/ND n = 8); joint vacuum fixed by X in 7/7; plain M also 2/2 everywhere. |
| G4 reciprocity | PASS (after one fix, see above) | S_GR, S_1911: 415 b-only monomials checked, 0 designations; S_beta_recip: 436 checked, 25 designated (all = G_READ_WHY); S_beta_oneway: 32 designated (G_READ + G_SOURCE); S_beta_rank4: 447 checked, 0 designations (fully reciprocal rank 4); ND_rank3/4: 133/194 designated (self law, auxiliaries, York source, reads); OD2: 348 checked, 56 designated (accumulator, stress, centred reads), 38 two-time monomials skipped. CONTROL: lapse action without its source -> FAIL (19 missing partners). |
| G5 Lorenz | PASS | random b-only sources into all 10 gears, 40 updates, L = 5: dressed identity residual 0 at every node (max |C| = 41: sources not conserved). Rotor superpotential source (exactly conserved): max |D_mu s^{mu nu}| = 0 over 60 updates, identity residual 0; BUT C was not 0 (max |C| = 8,671 / 14,983 / 17,231 at t = 10/30/60 for |h| ~ 1e5-2e5): a free rotor cannot be switched on from W = 0, so the initial data violated C(0) = 0 (W(0) != 0); the registered "C driven only by remainders" is therefore NOT shown (initial-data constraint not met), only the exact identity. |
| G6 Gauss | PASS | per-update flux identity exact (residual 0) for boxes of half-width 1, 2, 3 around the load at every update t = 1..30; the time-summed form exact (0); window means: (Q-1) x mean outward-flux sum = -4.06e7 vs mean source 4.47e7 (period-mean Gauss law within 9 % in a 30-update window of a non-static switch-on). |
| G7 OD2 | PASS | accumulator remainders never change; C^0, C^i constant at every node for 14 updates (random data, max |C| = 23); prepared data C = 0 exactly for all 14 updates; dressed Hamiltonian identity D_t^2 Box h00 = Div_0 Div(2s + dr) residual 0; stages [hij], [h0i], [h00], [matter]. |
| G8 T^{mu nu} | PASS | KG gear (Q = 51, mu = 3, L = 6, |a|,|b| < 1e5): energy and momentum two-time identities (with remainders, symmetric plaquette stress) exact in 10/10 windows. |
| G9 support | REPORT | metric block: 18 physical-support facts (h0i headroom stencil couples parallel links: 6 per axis); OD2: 12 (h0i reads plaquette gears hij(x - e_j)); lapse, beta, beta_rank4, N-design: 0 by the core diagnostic. NOT visible to the core diagnostic (GearType has no plaquette metadata): the 3 hij plaquette gears' stencils couple parallel plaquettes (18 monomials). |
| G10 OD2 staggered reversor | PASS (CONJECTURE now NUMERIC, structural 3-D) | X = (hij: M or M'; h0i: (a,b) -> (-h0i(t+1), -b); h00: (a,b) -> (h00(t+2), h00(t+1)); matter M or M'): X F^n X F^n = id on 10/10 random states for n = 1 and n = 12, for both M and M' (no central element needed), with the minimal first-order test matter reading h00 at the centred time and sourcing hij with b-only link stress. Caveat: no shift (h0i) coupling of the matter and no physical Dirac spinor (OPEN, stage 3). |

## PRE-REGISTRATION demos D3 (N-design field level) and D4 (gravitational waves) (written Tue Nov 10 10:00:16 UTC 2026, before running)
D3 (demos/gravity/d3_ndesign.py): P = 2^12, k = 80, Q = 655,361; N-design rank 3 (split; detuned remainder weights
Q-1, 0.7(Q-1), 0.5(Q-1)); prescribed static Gaussian density gear n (R = 2, weak-field mass estimate M = 1;
MECHANISM), L = 48, T = 60 (no-image window for r <= 13). Readout (event, labelled): N(r) = 1 + nu/P on the +x axis,
mean of the last 10 updates; fit M with the exact isotropic lapse (1 - M/2r)/(1 + M/2r) over r = 6..10 (min-max fit) and
with the linear 1 - M/r. Expected (S1 Y11: 3e-3 vs 1.5e-2 at L = 96, P = 4096): max deviation isotropic < linear,
isotropic <= 5e-3. Clocks reading A at r = 6, 10: N_click (half-angle) vs N_event within 2e-2 (agreed <= 2 %).
D4 (demos/gravity/d4_gw.py): 6 spatial metric gears (headroom stencil), Q = 8193, L = 64, T = 96; source: on-site
oscillator gears O1, O2 (w0 = 0.35) at the centre feeding s^xx = +kappa b(O1), s^yy = -kappa b(O1) (linear
quadrupole) and, in the rotating case, s^xy = kappa b(O2) (O2 in quadrature) (MECHANISM, 0mu omitted). Readouts
(event, labelled): on the z axis h+ = (hxx - hyy)/2, hx = hxy; on the x axis h+ = (hyy - hzz)/2, hx = hyz.
Criteria/report: (a) front speed from 10 %-of-peak arrivals on the z axis vs c_Q (within 10 %; strict causal bound:
taxicab, speed 1 along an axis); (b) R x amplitude constant within 15 % for R = 9..24 (1/R); (c) linear source:
hx/h+ = 0 exactly on the z axis; rotating source: hx/h+ ~ 1 on the z axis (two polarizations).

## D1/D2 first attempts FAILED dynamically — finding F1/F2 (written Tue Nov 10 10:03:55 UTC 2026)
- D1 (started 09:56:30) EXPLODED: diagnostic re-run (same system, 120 updates): F/P at the load centre 0.055 (t = 0),
  0.46 (t = 10), -2.9e6 (t = 20). Cause (DERIVED): with reciprocal_source=True the G back-reaction couples F and G as
  f_tt = c^2 (Lap f - f Lap g), g_tt = c^2 (Lap g - (1/2) Lap f^2): about a background f0 the eigen-speeds are
  c^2 (1 +- f0). The ONE headroom stencil u = (Q-1) Sum_6 b + 6b has c^2 = 1/3 - 1/(3Q), i.e. headroom 1/(3Q) only
  (Q ~ 5e7 here), so the fast mode exceeds the CFL bound for ANY f0 > 1/(Q-1): the staggered mode grows by ~3.5 per
  update at f0 = 0.46 (observed ~ x2.8e5 in 10 updates). FINDING F1: the reciprocal (one-potential) completion of the
  beta = 1 G source is exact (G2-G4 PASS) but DYNAMICALLY UNSTABLE with the ONE headroom stencil at gravity's Q; the
  agreed one-way form (reciprocal_source=False, designated) is used for dynamics.
- D2 (started 09:58:11) stopped by hand at 10:03:55: its design is unsafe for the same reason. FINDING F2: the
  lapse link factor 1 - 4U exceeds 1 wherever U < 0 (anti-load region; the zero-mean prepared static field is negative
  far away; rounding noise of F, S1 Y6), and with headroom 1/(3Q) any link factor > 1 + 1/Q violates CFL for light.
  Integer gravity with fine U resolution forces Q - 1 = 2Pk (P ~ 2^20), so the headroom of the ONE stencil vanishes.
  DESIGN ISSUE for main (owner decision): either all field gears use a common reduced face weight (e.g. (Q-1)/2:
  c^2 ~ 1/6 = S1's stencil B, headroom x2, still ONE cone), or every light demo must keep U >= 0 everywhere.
AMENDED D1 (before re-running): beta block with reciprocal_source=False; everything else as registered.
AMENDED D2 (before re-running): NO anti-load; prepared field F = F_static - min(F_static) >= 0 everywhere (a constant
is a static solution; U >= 0 so every light link factor <= 1); the closed-board zero mode then drifts upward (uniform
U drift, same for both light species and both atom sites; the redshift prediction uses the window-mean F at each
atom); atoms mu = 2P*24 (w0 ~ 0.6) and T = 120 (light window t < 110); criteria unchanged.

## PRE-REGISTRATION demo D5: free fall read from clicks vs events (written Tue Nov 10 10:04:49 UTC 2026, before running)
demos/gravity/d5_freefall.py: P = 2^20, k = 24, L = 32, T = 60. Load as D2 (no anti-load; prepared settled field
F_static - min >= 0); KG test packet (u = 6Q b + (Q-1) Lap b - mu b, mu = 2P*6, lapse GR), Gaussian sigma = 2.5,
amplitude 2^14, at rest at r0 = 8 on the +x axis. Readouts per update: EVENT centroid x_E = Sum x b^2 / Sum b^2;
CLICK centroid x_C = Sum x q^2 / Sum q^2 with q the official click quotients (0 where unchanged). Fit x(t) quadratic.
Criteria: the packet falls toward the load (x_E decreases, accel < 0); |a_C/a_E - 1| reported (agreed reading: the click
reading reproduces the fall to ~1e-6; here the target is <= 1e-3, the 1e-6 of the studies used the two-size click energy,
not reproduced in this hour), max |x_C - x_E| reported.

## FINDING F3 and amendment of D1, D2, D5 (written Tue Nov 10 10:16:46 UTC 2026, before re-running)
The relaunched D1 (one-way G) was again far too slow; diagnosis (same system, no clicks): stable to t ~ 200 but the
self-gravitating reciprocal load COLLAPSES: bits of h00 19 -> 21, load amplitude 20 -> 22, G 15 -> 20 bits by t = 200,
explosion at t ~ 222 (U(0) ~ 0.2-0.3). Mechanism (DERIVED): a reciprocal clock-pair load keeps its adiabatic invariant
(omega A^2), so as its own lapse slows it, A^2 and hence its source grow: positive feedback (the Lane-Emden-type
runaway of S1-M2 Y4 with a bare source). FINDING F3: with the reciprocal lapse, self-gravity is real and a compact
load (U(0) ~ 0.3) is not static; a York-type weighting would be needed (as in the N-design). For the demos the load is
the studies' PRESCRIBED static load (MECHANISM, designated one-way): build_static_load (density gear holding its
value, source coeff*n^2, does not feel F). D1: static load (coeff +1) at c and anti-load (coeff -1) at the antipode,
U(3) ~ 0.08; D2 and D5: static load only, prepared settled field F_static - min >= 0. All other registered items and
criteria unchanged. (The test matter keeps the reciprocal lapse: atoms, light, KG.)
D1 refinement (written Tue Nov 10 10:17:31 UTC 2026, before re-running): the smoke check (no clicks) of the static-load system is stable
(22 bits to t = 400) but the field sloshes (F/P at r = 3 between 0.07 and 0.17: switch-on monopole waves never damp
on the reversible torus). So D1 also PREPARES settled fields (F = static lattice solution of the zero-net load source,
G = F^2/(2P); MECHANISM) and compares clicks with the EVENT time-mean <sqrt(1 - F(t)/P)> (and
<sqrt(1 - F/P + G/P)> for C); beta_eff := (N_C - N_A)/(<sqrt(1-F/P+F^2/2P^2)> - <sqrt(1-F/P)>) from co-located C and A
clicks (expected 1; control 0 by construction of A). Criteria (a)-(e) otherwise unchanged.

## RESULTS D1 and D2 (written Tue Nov 10 10:18:38 UTC 2026; D1 run 10:17:31-10:18:16, D2 run 10:17:31-10:17:55; results/gravity/D1.json, D2.json)
D1 (L = 32, T = 1300, window 300-1300, prepared settled fields, static load + anti-load, MECHANISM):
- (a) PASS: lapse-only atoms A, B from CLICKS (half-angle reading) vs event <sqrt(1 - F/P)>: max |N_click/N_pred - 1| =
  2.9e-5 over 10 sites (U = 0.009-0.10) (criterion 3e-4).
- (b) PASS: universality, co-located species A (mu = 2P) and B (mu = 8P): max |N_A/N_B - 1| = 4.8e-5 (criterion 1e-4);
  the raw frequency ratio shows the O(w0^2) lattice deficit (reported in D1.json).
- (c) PASS: beta atoms C read their own 1 - F/P + G/P to 3.0e-5; beta_eff from co-located C and A clicks = 0.997,
  0.999, 1.006, 0.999, 1.029 at the 5 sites with U > 0.03 (mean 1.006); control (A) beta = -0.0009 (mean).
- (d) field: the window-mean F equals the static lattice solution to 1e-6 at r = 2..10 - NOT an independent 1/r test,
  because the field was PREPARED as that solution (it shows stationarity only); log-slope of the torus solution with
  the antipodal anti-load at r = 2..6: -1.26 (not the 0.99-1.01 of the studies' open-window build-up). 1/r build-up
  OPEN in this package.
- (e) PASS: rewind of all 1300 updates exact.
D2 (L = 40, prepared settled field >= 0, static load):
- (a) FAIL vs the pre-registered window [1.8, 2.2]: Shapiro delay ratio GR/1911 = 2.61 (b = 4: delays 5.71 vs 2.19
  updates) and 2.57 (b = 6: 4.08 vs 1.59). Reading: the 1911 control works (GR delay ~2x), but the ratio exceeds 2 by
  ~30 %: second-order index terms at U ~ 0.05-0.1 (ratio ~ 2(1 + 1.5U)), lattice dispersion of the k = 0.8 carrier, and
  the closed-board zero-mode drift of U during the run (both species); not separated in this hour.
- (b), (c) FAIL (measurement): the light-frequency readout from a 2-period pulse (selected samples non-contiguous) is
  not usable (N/F frequencies differ by -40 %, an artefact of the readout), so redshift VIA LIGHT is not shown. The
  clock comparison itself (half-angle atoms) gives N_F/N_N = 1.05024 vs the lapse prediction 1.05090 (b = 4, dev
  -6.3e-4) and 1.02876 vs 1.02683 (b = 6, dev +1.9e-3).

## PRE-REGISTRATION D6 (field build-up, 1/r, Gauss) and D2b (weak-field Shapiro) (written Tue Nov 10 10:19:46 UTC 2026, before running)
D6 (demos/gravity/d6_field.py): static load only, F built FROM ZERO (no preparation), L = 64, T = 64, window
t = 48..64 (no image reaches r <= 11 before t ~ 92). Criteria: log-slope of F on the axis, r = 3..11, in [-1.05, -0.95]
(agreed 0.99-1.01); F r 4 pi (Q-1)/S reported; Gauss: -(Q-1) x flux(box)/S within 3 % of 1 for box half-widths 4, 6, 8.
D2b: D2 with a 4x weaker load (U(3) ~ 0.02), carrier k = 0.5, sigma = 10 (smaller second-order and dispersion terms);
criterion: Shapiro ratio GR/1911 in [1.8, 2.2] at b = 4 and 6 (frequency/redshift readouts reported, not criteria).
Note on D3 (finished 10:19:08, results/gravity/D3.json): isotropic fit M = 0.969, max deviation 2.8e-3 (r = 6..10),
linear fit max deviation 4.5e-3 -> PASS (criterion: isotropic <= 5e-3 and better than linear); clocks reading A:
N_click/N_event - 1 = -2.3e-3 (r = 6), -1.2e-3 (r = 10) -> PASS (<= 2e-2); N_min on the axis 0.764.
Note on D4 (finished 10:19:40, results/gravity/D4.json): (a) PASS front speed 0.583 vs c_Q = 0.5773 (+1.0 %; the strict
causal bound along an axis is the taxicab speed 1); (b) R x |h+| on the z axis = 2817, 3156, 3075, 3168, 3654, 3048 for
R = 9..24 (mean 3153): five within 11 %, R = 21 at +15.9 % -> marginal FAIL of the registered 15 % (amplitude read as a
max over a short late window; noisy); (c) PASS: linear quadrupole hx = 0 exactly at every z-axis probe; rotating
quadrupole hx/h+ = 0.86-0.99 (two polarizations). (written Tue Nov 10 10:20:01 UTC 2026)

## DERIVED (for stage 3): reciprocal coupling of ALL TEN components needs the DeWitt metric; an integer basis exists
(written Tue Nov 10 10:20:25 UTC 2026; algebra checked numerically: A^T diag(1,1,1,-1) A = H4 exactly, det A = -4, and
hbar.K(hbar) = (1/2) hbar^T H4 hbar on the diagonal sector for random hbar)
- Matter couples to h_{mu nu} = K(hbar) (trace reversal) via Phi_int = (1/2) h_{mu nu} T^{mu nu}; with ten
  independent scalar headroom gears storing hbar, the reciprocal source of hbar would be the trace-reversed Tbar, not T
  (static dust would source hbar^{ii}: wrong). Reciprocity with GR's Box hbar ~ T needs the field potential to carry the
  DeWitt metric K (indefinite, non-diagonal in the 00/ii sector), which the checker supports only through diagonal
  field signs.
- Diagonal sector: q(hbar) = hbar^T H4 hbar = y0^2 + y1^2 + y2^2 - y3^2 with the INTEGER basis
  y0 = h00 + hxx + hyy + hzz (= 2 h_00: exactly the lapse combination the clock reads), y1 = hxx - hyy, y2 = 2 hzz,
  y3 = hxx + hyy + 2 hzz; field signs (+, +, +, -) (the -1 gear needs sign_why); h0i sign -1, hij sign +1 (eta factors).
  Storing y instead of hbar (every y is a combination of same-placed node gears, so the Yee placement is unchanged)
  would make the full linear coupling reciprocal with ONE potential. Not built in stage 1 (the lapse block couples the
  static lapse combination only); z is singled out by this basis (no permutation-symmetric integer basis was found).

## Manager rulings 10:2x received; PRE-REGISTRATIONS G5b, D7, D2c, D8 and code changes (written Tue Nov 10 10:23:15 UTC 2026, before any run)
Code changes (before re-running the suite): (i) build_beta default reciprocal_source=False (the agreed one-way,
designated form is the DEFAULT beta; the rank-4 form build_beta_rank4 is the reciprocal alternative; the reciprocal G
back-reaction is kept only as an audit option: F1). (ii) OD4 rule: build_beta_rank4's link quartic now uses
Fbar^2 = ((F_x + F_y)/2)^2 so every rank-4 term is -lambda q^2 on one node / one link (site: q = F b; link:
q = Fbar (b_y - b_x)); the system S_beta_rank4 now needs Q - 1 = 64 P^2 k (Q4 = 16385). The full G1-G10 suite is re-run
unchanged on the new code (pass criteria unchanged).
G5b (C = 0 initial data, exact conserved source): drive gears V_i (rotors, no input) and O_i with u = 3Q b(V_i)
(K = 6Q b_V: remainder-free, O(t+1) + O(t-1) = V(t)); W^{0i0i} = O_i: s^00 = kappa Sum_i D_i^2 a(O_i),
s^{0i} = -kappa D_i^fwd (b - a)(O_i), s^{ii} = kappa (b(V_i) - 2 b(O_i)) (exactly conserved for any V history).
Start V = (0, A), O = (0, 0), fields at rest: C(-1) = 0 and C(0) = remainder only. Pass: D_mu s^{mu nu} = 0 and identity
residual 0 every update (exact); report max |C| over 60 updates (expected O(remainder): <= 200, vs 17,231 in G5).
D7 ("gravity only slows", dynamic, demos/gravity/d7_slows.py): L = 32, P = 2^20, k = 24; SELF-CONSISTENT load =
reciprocal clock pairs (U(3) ~ 0.02, below the F3 collapse) + headroom light filled with random lattice noise
(|b| <= 2^8) + reciprocal lapse for both. Offset bound (DERIVED): with total source S > 0 the zero mode only grows,
F_mean(t) = F_mean(0) + S t^2 / (6 Q L^3) + O(1), so U >= 0 for all t if the initial field is the settled zero-mean
solution F_s plus a constant C0 >= -min F_s = g_L S / ((Q-1) L) (g_L = -L min G_L, G_L the zero-mean lattice Green
function, computed) plus a wave margin. Runs: (i) F(0) = F_s + 1.5 C_min; (ii) control F(0) = F_s (C0 = 0). Readouts every
10 updates (event, labelled): min_x F/P, max |light|. Pass: (i) min F >= 0 at every sample for T = 600 and max |light|
<= 10x its initial value; (ii) reported (expected min F < 0; light growth reported).
D2c (Shapiro diagnostic, separating causes; demos/gravity/d2c_shapiro.py): L = 40, static load, prepared F_s - min F_s;
centroid window restricted to +-3 sigma_t around the expected arrival (excludes spurious left-movers); for each
config three runs: loaded, ZERO-MODE CONTROL (uniform source with the same total S and the same offset: same drift, no
localized field), twin (no source). Configs: (k, U3) = (0.8, 0.08), (0.4, 0.08), (0.4, 0.04), (0.4, 0.02). Report
delay_GR, delay_1911 (loaded - control) and (loaded - twin), and the ratios. Expectation: (loaded - control) ratio ->
2 as k -> 0 and U -> 0; pass criterion for the best config (k = 0.4, U3 = 0.02): ratio in [1.8, 2.2].
D8 (redshift VIA LIGHT, emitter design; demos/gravity/d8_redshift.py): L = 48, static load (U3 = 0.04), prepared F >= 0;
an emitter atom E (mu = 2P*24) at N = (c, c+4, c) coupled to the light by the reciprocal on-site bilinear
Phi_e = -g b_E b_L (g = 2^16, designated none: reciprocal); a receiver atom (same species) at F = (c+15, c+4, c) and at N.
Readouts (CLICK space): crossing rates over t = 80..300 of the light at F (w_LF), of the atoms at F and N.
Criteria: light frequency conservation |w_LF / w_E - 1| <= 2e-3; redshift via light (w_atF / w_LF) vs the event
prediction <N_F>/<N_N> within 3e-3.

## RESULTS G5b, D5, D6 (written Tue Nov 10 10:24:51 UTC 2026)
- G5b PASS (results/gravity/G5b.json, 10:23:30): driven remainder-free source with W(-1) = W(0) = 0 and fields at rest:
  D_mu s^{mu nu} = 0 and identity residual 0 at every update; C(0) = 0; max |C| over 60 updates = 135 (C every 10
  updates: 0, 5, 15, 39, 73, 113, 135) for |h| up to 5.3e6 (relative 2.6e-5): C is driven ONLY by the remainders
  (against 17,231 in G5 with unconstrained data). The G5 claim is now shown with constrained initial data.
- D6 PASS (results/gravity/D6.json, 10:20:01): field BUILT from F = 0 by the board (static load, L = 64, window
  t = 48-64): log-slope on the axis r = 3..11 = -1.0018 (criterion [-1.05, -0.95]); F r 4 pi (Q-1)/S = 1.001-1.007;
  Gauss -(Q-1) flux/S = 1.0002, 1.0005, 1.0008 for box half-widths 4, 6, 8 (criterion 3 %).
- D5 FAIL / inconclusive (results/gravity/D5.json): the KG packet moves toward the load (event centroid -10.1 nodes in
  60 updates) but the motion is dominated by a linear drift (dispersion of the sigma = 2.5 packet in the gradient and
  the vacuum-frequency initial data), the quadratic fits give a_event = -1.7e-4, a_click = -9.2e-4, and the click and
  event centroids differ by up to 1.09 nodes. The agreed "click = event to ~1e-6" free fall is NOT reproduced: OPEN.

## RESULTS D2c (Shapiro diagnostic; written Tue Nov 10 10:27:25 UTC 2026; results/gravity/D2c.json)
Delay ratio GR/1911 (loaded minus ZERO-MODE CONTROL | loaded minus twin), far detectors b = 4 / b = 6:
- k = 0.8, U3 = 0.08: 2.43 / 2.17 | 2.31 / 2.15
- k = 0.4, U3 = 0.08: 2.40 / 2.40 | 2.33 / 2.32
- k = 0.4, U3 = 0.04: 2.157 / 2.154 | 2.156 / 2.154
- k = 0.4, U3 = 0.02: 2.109 / 2.104 | 2.087 / 2.083   (delays GR 0.478 / 0.435 vs 1911 0.227 / 0.207 updates)
Reading: the excess over 2 falls with the load strength (0.40 -> 0.155 -> 0.106 at fixed k): SECOND ORDER in U is the
main cause; the carrier k matters little at U3 = 0.08; the zero-mode drift changes the ratio by <= 0.07. The earlier
D2 values (2.61/2.57) also included spurious early left-mover arrivals (fixed here by the +-3 sigma window).
PASS for the registered best configuration (k = 0.4, U3 = 0.02): 2.109 and 2.104 in [1.8, 2.2] (agreed 2.00-2.11).
The D2 FAIL (2.61/2.57 against the same window) stays recorded.

## RESULTS D7 ("gravity only slows", dynamic; written Tue Nov 10 10:27:55 UTC 2026; results/gravity/D7.json)
- Offset bound (DERIVED, checked): U_offset >= g_L S / (2P (Q-1) L), g_L = -L min G_L = 0.0640 (L = 32, zero-mean
  lattice Green function); formula 0.001512 vs the measured -min F_s/(2P) = 0.001495 (S = 7.98e13).
- (i) offset 1.5 x bound: min_x F >= 0 at EVERY sample (min over the run 0.0023 P) -> U >= 0 / N <= 1 everywhere: PASS
  for the U >= 0 part. Light (random noise 2^8, headroom stencil, link factor 1 - 4U <= 1) stayed bounded (704-925,
  x2.7-3.6 of the initial maximum, from noise redistribution) up to t = 210.
- BUT both runs EXPLODE at t = 250: the closed-board zero mode grows as S t^2/(6 Q L^3) (gravity only slows - and keeps
  slowing): U_min reaches 0.24 at t = 240, the GR light weight 1 - 4U turns negative near the load, light grows x1e3 and
  the state blows up. DERIVED lifetime t* = sqrt(3 Q L^3 P / S) = 255 (measured 250). So the registered "light bounded
  for T = 600" FAILS; t* scales as L^{3/2} S^{-1/2} (a closed positive-energy board is not static: S1 B10 / Z1).
- (ii) control (no offset): min F < 0 at t = 10 (-0.0021 P), lifted above 0 by the drift by t ~ 30; no visible light
  growth from that brief negative-U window; same explosion at t = 250.
FINDING F4 (for main / Study 7): with positive energy only and the ONE stencil, "gravity only slows" keeps U >= 0 (CFL
safe for link factors) but the uniform mode makes U grow without bound; GR light dies at U = 1/4 at t*. Remedies
outside this layer: larger L (t* ~ L^{3/2}), an open board, or a screened/KG-form lapse (S1).

## RESULT D8 (written Tue Nov 10 10:28:36 UTC 2026; results/gravity/D8.json) and PRE-REGISTRATION D8b
- D8 FAIL (readout): the light at the far detector oscillates at w = 0.857 vs the emitter's 0.549 (+56 %): with
  g = 2^16 the emitted wave at r = 15 has an amplitude below one integer unit (estimate ~0.5), so the light's own
  rounding noise dominates the crossings. Redshift via light NOT shown by D8.
- D8b (before running): same script with g = 2^24 (wave amplitude at F ~ 1e2). Because a strong emitter coupling pulls
  the emitter's own frequency, the redshift via light is defined against the emitter it carries:
  R_light := (w_atF / w_LF) x (w_E / w_atN) (the second factor compares the emitter with the clean co-located atom at N,
  both local), predicted <N_F>/<N_N>; criteria: |w_LF / w_E,retarded - 1| <= 2e-3 and |R_light / pred - 1| <= 3e-3.

## PRE-REGISTRATION F3T: self-gravitating collapse threshold data (written Tue Nov 10 10:29:04 UTC 2026, before running)
demos/gravity/f3_collapse.py: reciprocal clock-pair load (as F3) at U3 = 0.02, 0.04, 0.08 (continuum estimate of U at
r = 3), L = 32, T = 600, with a PRESCRIBED static anti-load (MECHANISM) of equal total source at the antipode only to
cancel the closed-board zero mode. Report per strength: runaway time (first sample with > 60-bit values) or none, and
the centre U history. Expectation from F3: runaway at U3 = 0.08 (t ~ 200-250); weaker loads later or not within 600.

## RESULTS F3T and D8b (written Tue Nov 10 10:35:11 UTC 2026)
- F3T (results/gravity/F3.json, run 10:29:04-~10:33): self-gravitating reciprocal clock-pair load, zero mode cancelled
  by a prescribed anti-load: U3 = 0.02: NO runaway in 600 updates (centre U <= 0.10); U3 = 0.04: runaway at t = 600
  (centre U reached 1.5 before); U3 = 0.08: runaway at t = 230 (centre U 2.5). Threshold data for F3: the reciprocal
  self-gravitating load is stable over 600 updates only for U(0) ~< 0.1 at this resolution (R = 2.5, L = 32).
- D8b FAIL/OPEN: with g = 2^24 the emitter-light pair is not well behaved: the light at the emitter grows from 2^12 to
  2^16 in 60 updates without saturating (diagnostic at 10:34; g = 2^16 and 2^20 stay at 2^5 / 2^9), and the D8b run
  did not finish within ~5 min (stopped by hand). Redshift VIA LIGHT remains OPEN; the clock redshift (D2: 6.3e-4 and
  1.9e-3; D2b: 2.0e-4 and 5.6e-5 with the half-angle reading) stands.

## CENSUS (manager rule 4; results/gravity/census.json, refreshed 10:28 on the final code)
- Constants: 0 in every gravity block (deviation form, constant-free).
- OD3 placement: the lapse and beta blocks add, for NEW matter channels only, up to two monomials per row per face from
  the SAME neighbour (F(x) b(x+e) and F(x+e) b(x+e)); no gravity term targets ref.* (q_lattice clean).
- OD4 (rank-4) terms and their decomposition:
  * build_beta_rank4: site  -(mu/(4P^2)) (F b)^2 = -lambda q^2, q = F b (general -H >= 0: -(1/2) Sum_k h_k (F v_k.b)^2);
    link -(17 w/(16 P^2)) (Fbar (b_y - b_x))^2, Fbar = (F_x + F_y)/2; one node / one link, minus sign, negative
    semi-definite -> within OD4 (first-order matter: 1/8 and 9/16). [10:22 change from F_x F_y, an indefinite
    cross-quartic.]
  * build_ndesign(rank4=True): the A*C light-weight quartics (nu_x nu_y, nu crem, a2 crem, a2 nu times (delta b)^2) are
    INDEFINITE cross-quartics, NOT OD4 springs; they exist only as designated one-way test-light reads (ND_READ_WHY).
- Two-time (a-read) monomials: ONLY in build_od2 (+ the G5/G5b test sources): 38 per OD2 system = h0i accumulators
  read hij.a (18: Div_i at the link), h00 reads h0i.a (6), matter centred reads of h00.a and h0i.a (7 per matter gear,
  2 gears = 14); full list in census.json["OD2"]["od2"]["a_read_monomials"]. Stages: [hij] -> [h0i] -> [h00] ->
  [matter] (acyclic). No remainder-reading input anywhere.
- Field signs: all +1 (no sign_why needed).
- Physical support wider than one link: metric h0i stencils (18 per system: parallel links), hij plaquette stencils
  (18, invisible to the core diagnostic: no plaquette metadata), OD2 h0i reading plaquette gears (12).
- Designations (one-way, justified in layers/gravity.py): G_READ_WHY, G_SOURCE_WHY (beta), ND_SELF/AUX/SRC/READ_WHY
  (N-design), OD2_ACC/STRESS/READ_WHY (OD2), STATIC_LOAD_WHY (prescribed loads); all sit on monomials no force term
  uses (G4 passes; the lapse block itself has ZERO designations).

## API for reviewers (stage 1)
- layers.gravity: gravity_Q(P, k); build_metric; MatterSpec, build_matter / build_test_matter, spec_from_block;
  atom_spec, load_pair_spec, light_spec, kg_spec, weyl_spec; build_lapse(gamma="GR" | "1911" (lapse-only light
  CONTROL)); build_beta (default one-way), build_beta_rank4; build_ndesign(rank4=...); build_od2 +
  od2_hop_stress, od2_centred_lapse_read; build_static_load (MECHANISM).
- prepare.gravity: with_static_load, with_load (clock pairs), with_clocks (atom clocks), with_light_pulse,
  static_field + with_field (settled fields, offset), od2_prepare_constraints (C = 0), load_source / static_load_source.
- observe.gravity: arr (any gear's a, b, r as an (L,L,L) array), sources, lorenz_C / lorenz_identity_residual,
  source_divergence, gauss_residual / flux, od2_constants, tmunu_residuals, click_series / crossing_times /
  rate_from_crossings (click readout), od2_staggered_reversor (AUDIT map), support_report. Click logs: core
  Engine.clicks / extract_clicks (official stream).

## PRE-REGISTRATION D8c and D4b (written Tue Nov 10 10:35:36 UTC 2026, before running)
- D8c: D8 with g = 2^20 (the diagnostic at 10:34 showed g = 2^20 bounded at the emitter, light ~2^9), R_light defined as
  in D8b; same criteria (|w_LF/w_E,ret - 1| <= 2e-3; |R_light/pred - 1| <= 3e-3).
- D4b: D4 re-analysed with a fixed-duration amplitude estimator: sqrt(2) x RMS of h+ over [t_arr + 10, t_arr + 46]
  (two source periods) at each probe; criterion: R x amplitude constant within 15 % for R = 9..24 on the z axis; the
  front speed and polarization criteria as in D4.

## RESULTS D4b, D8c (written Tue Nov 10 10:37:08 UTC 2026)
- D4b PASS (results/gravity/D4b.json): fixed-duration RMS amplitude (2 source periods after arrival): R x |h+| on the
  z axis = 2636, 2649, 2683, 2664, 2685, 2364 for R = 9, 12, 15, 18, 21, 24 (mean 2614): all within 10 % (R = 24 at
  -9.6 %, the others within +2.7 %) -> 1/R within the registered 15 %. Front speed 0.583 vs c_Q 0.577; hx = 0 exactly
  (linear source), hx/h+ = 0.86-0.99 (rotating source). (The max-based D4 estimator's marginal FAIL stays recorded.)
- D8c FAIL: g = 2^20 bounded, but the light at F oscillates 5.0 % slower than the (retarded) emitter (32 crossings);
  R_light deviates +5.2 % from the prediction (1.0044). Diagnosis: during the run the closed-board zero mode drifts
  (positive static load only) and the light at F is not yet a clean steady wave; redshift via light still OPEN.

## PRE-REGISTRATION D8d: redshift via light WITHOUT zero-mode drift (written Tue Nov 10 10:37:08 UTC 2026, before running)
New file demos/gravity/d8d_redshift.py. Prescribed static load (+) at c AND prescribed static anti-load (-, equal
total) at the antipode (both MECHANISM; zero net source -> no closed-board drift), prepared settled field
F = F_s + C0 with C0 = -min F_s (k = 0 constant: U >= 0, N <= 1 everywhere, light CFL-safe), L = 48, T = 420, emitter
g = 2^20, readout window t = 180..420 (steady state). Criteria as D8b: |w_LF/w_E,ret - 1| <= 2e-3 and
|R_light/pred - 1| <= 3e-3 (R_light = (w_atF/w_LF)(w_E/w_atN), prediction <N_F>/<N_N>).

## PRE-REGISTRATION D5b: free fall, drift-free settled field (written Tue Nov 10 10:37:41 UTC 2026, before running)
New file demos/gravity/d5b_freefall.py: L = 32, prescribed load (+) and anti-load (-) (MECHANISM, zero net source: no
drift), field F_s + C0 >= 0 (k = 0 constant), KG packet (mu = 2P*6, sigma = 3, amplitude 2^14) at rest at r0 = 7 on
the +x axis, prepared with the LOCAL k = 0 frequency (a = b cos w(x), clock factor N^2(x)); T = 70. Centroids weighted
by the two-time EVENT energy b(t)^2 + b(t-1)^2 - 2 cos w0 b(t) b(t-1) and by the two-size CLICK energy
q(t)^2 + q(t-1)^2 - 2 cos w0 q(t) q(t-1) (official click sizes). Fit t = 5..69. Criteria: the event centroid falls
(accel < 0); |a_click/a_event - 1| <= 1e-2 and max |x_click - x_event| <= 0.05 node (the studies' 1e-6 used a different
click-energy definition; reported against it).

## RESULTS D8d and D5b (written Tue Nov 10 10:38:43 UTC 2026)
- D8d FAIL (results/gravity/D8d.json): drift-free field (load + anti-load + offset), steady-state window 180-420,
  63 light crossings at F: w_LF/w_E,ret - 1 = -0.84 % (criterion 0.2 %), R_light/pred - 1 = +0.92 % (half-angle
  +0.84 %; criterion 0.3 %); prediction 1.0278, measured 1.0373. Clock side: w_E vs the clean co-located atom at N
  agree to 1.2e-4 (0.52099 vs 0.52106). Diagnosis (not tested): in a closed reversible box the switch-on excites free
  light modes that never damp and beat with the driven wave at w_E, biasing crossing-based frequencies at the 1 %
  level. Redshift VIA LIGHT stays OPEN; best value +0.9 % from the GR first-order prediction.
- D5b ABORTED by an explosion (OverflowError at the click readout): with the anti-load, the offset C0 = -min F_s ~ the
  anti-load's depth, so U_max ~ 2 U_peak; at U3 = 0.08 the KG transport weight 1 - 4U turns negative in the load core
  when the falling packet arrives (tachyonic). Same F1/F4 limit: transport fields need U < 1/4 everywhere.
## PRE-REGISTRATION D5c (written Tue Nov 10 10:38:43 UTC 2026, before running): D5b with U3 = 0.03 (U_max ~ 0.08 + offset < 1/4) and
r0 = 6; criteria as D5b.
- D5c FAIL (results/gravity/D5c.json, 10:38:46): the packet falls toward the load (event centroid -5.97 nodes in 70
  updates; quadratic fit a_event = -6.9e-4 with an early velocity -0.099/update from the packet's asymmetric spreading
  in the gradient), a_click = -7.7e-4 (ratio dev +12 %, criterion 1 %), max |x_click - x_event| = 0.105 node
  (criterion 0.05). The agreed free-fall agreement (click = event to ~1e-6) is NOT reproduced: OPEN.

## PRE-REGISTRATION IQ: default blocks at the integrator's Q (written Tue Nov 10 10:39:23 UTC 2026, before running)
New file demos/gravity/integrator_check.py: Q = 2^29 + 1, P = 2^20, k = 2^8. System: ref + metric (10 gears) + test
matter (atoms mu = 2P*31, light, first-order weyl matter with entries in 4P*Z) + build_lapse (GR, all matter) +
build_beta (default one-way, atoms) + build_od2 (stress kappa = 2 and centred reads from the weyl matter), composed
with q_lattice=("ref.*",). L = 4. Criteria: compose succeeds (one Q, q_lattice clean); vacuum fixed for 10 updates;
a small random state (matter |v| <= 16, fields <= 4) rewinds exactly after 10 + 10 updates on the int64 path;
check_reciprocity PASSES (designations listed).
- IQ PASS (results/gravity/IQ.json, 10:39:24): default blocks at Q = 2^29 + 1, P = 2^20, k = 2^8 (73 gears, 681
  monomials, rank 3, 4 inverse stages): compose with q_lattice clean, vacuum fixed 10/10, 10 + 10 rewind exact on the
  int64 path, reciprocity PASS (579 checked, 64 designated, 38 two-time skipped).

## FINAL SUMMARY (written Tue Nov 10 10:39:41 UTC 2026)
Frozen exact core (FREEZE-READY GRAV sent 10:36:24; unchanged since): layers/gravity.py d75f4802...,
prepare/gravity.py 3dc98696..., observe/gravity.py dd18de66..., tests/test_gravity.py 097c8205...; suite 11/11 OK
(10:35:15). Demos and new work: demos/gravity/*.py (not frozen), results/gravity/*.json.
| item | verdict | key number |
|---|---|---|
| G1 vacuum / deviation form | PASS | 8/8 systems, 0 deviations, 0 new-gear clicks |
| G2 exact rewind | PASS | 16/16 runs incl. Python-int path (to 2,089 bits) |
| G3 declared reversor rhoL0 + M', joint vacuum fixed | PASS | 7/7 b-only systems |
| G4 reciprocity (+ control) | PASS (1st run failed: OD2 designation omitted, fixed) | lapse 0 designations; rank-4 beta 0; control FAILS |
| G5 dressed Lorenz identity | PASS | residual 0 (40 updates, random sources); rotor source divergence 0 |
| G5b C = 0 initial data | PASS | C(0) = 0, max abs C = 135 for abs h ~ 5e6 (remainders only) |
| G6 Gauss flux identity | PASS | residual 0, boxes h = 1, 2, 3 |
| G7 OD2 momentum constraints, dressed Hamiltonian identity | PASS | C exactly constant; prepared C = 0; residual 0 |
| G8 T^{mu nu} two-time identities | PASS | energy and momentum residual 0 |
| G9 support facts | REPORT | 18 (h0i) + 18 hidden (hij plaquettes) + 12 (OD2) |
| G10 OD2 staggered reversor (3-D, structural) | PASS | 10/10 states, n = 1 and 12, M and M' |
| D1 clocks from clicks vs lapse | PASS | 2.9e-5 (criterion 3e-4) |
| D1 universality two species | PASS | 4.8e-5 (criterion 1e-4) |
| D1 beta = 1 from clicks | PASS | beta_eff 1.006 (0.997-1.029); control -0.0009 |
| D6 1/r built by the board + Gauss | PASS | slope -1.0018; Gauss 1.0002-1.0008 |
| D2 Shapiro GR/1911 | FAIL (recorded) | 2.61 / 2.57 |
| D2c Shapiro diagnostic | PASS (k = 0.4, U3 = 0.02) | 2.109 / 2.104; excess ~ second order in U |
| D2/D2b clock redshift (atoms) | PASS | 6.3e-4, 1.9e-3 (D2); 2.0e-4, 5.6e-5 (D2b) |
| D8/D8c/D8d redshift VIA LIGHT | FAIL / OPEN | best +0.9 % (D8d), light frequency -0.84 % |
| D3 N-design nonlinear lapse | PASS | isotropic fit 2.8e-3 (linear 4.5e-3); clocks 2.3e-3 |
| D4/D4b gravitational waves | PASS (D4 max-estimator 1/R marginal FAIL, D4b PASS) | front 0.583 vs c_Q 0.577; 1/R within 10 %; hx = 0 / hx/h+ 0.86-0.99 |
| D5/D5c free fall | FAIL / OPEN | falls; click vs event accel +12 %, 0.1 node |
| D7 gravity only slows (offset) | U >= 0 PASS; light bounded FAIL | t* = sqrt(3QL^3P/S) = 255 (measured 250) |
| F3T collapse threshold | REPORT | U3 0.02 stable 600; 0.04 runaway 600; 0.08 runaway 230 |
| IQ integrator Q | PASS | Q = 2^29 + 1 |
Findings: F1 (headroom 1/(3Q): reciprocal G back-reaction explodes; link factors > 1 violate CFL), F2 (light demos
need U >= 0), F3 (self-gravitating reciprocal load collapses; thresholds above), F4 (positive-energy closed board:
U grows ~ t^2, GR light dies at U = 1/4 at t*), DeWitt basis for full ten-component reciprocity (stage 3).

## Manager tasks 10:4x (after the final): PRE-REGISTRATIONS F4b and L0-EP (written Tue Nov 10 10:46:09 UTC 2026, before any code/run)
All new work in NEW files: layers/gravity_l0.py (L0 lapse builders), demos/gravity/f4b_background.py,
demos/gravity/l0_ep.py. The frozen core (layers/prepare/observe/tests gravity.py) is not edited.
F4b (F4 re-run with BOTH data: R-a + k = 0 offset). System on the OD2 board, where h00 is the rounding-free
accumulator (Sum_x h00 exactly frozen): build_od2 (hij F-gears; h0i, h00 accumulators) + first-order weyl test matter
(noise |b| <= 16; stress source kappa = 2 into hij; centred on-site lapse read of h00) + headroom light (noise
|b| <= 2^8) reading b(h00) on its links with the GR link factor (one-way, designated; a centred link read is not
B3-local) + a static clock-pair load (mu = 2P*3, U(3) ~ 0.02) reading b(h00) on-site (one-way). PREPARED data:
h00 = F_s + C0 where F_s = static lattice solution of the MEAN-SUBTRACTED load source (R-a: the k = 0 part is the
declared uniform background -kappa E/N) and C0 = -min F_s (k = 0 constant: U >= 0, N <= 1); h0i = hij = 0, a = b
(C^i = C^0 = 0). P = 2^20, k = 24, L = 32, T = 700. Readouts every 10 updates (event, labelled): Sum_x h00 (must be
EXACTLY constant), min/max U, max |light|, max |weyl|. Pass: Sum h00 constant at every sample; min U >= 0 and
max U < 1/4 at every sample; max |light| <= 10 x initial and max |weyl| <= 10 x initial for 700 updates.
L0-EP (L0 under the ONE-VACUUM embedding, offset s = Q - 1, vacuum 3Q - 1, R' mirror):
- THEOREM check (exact, algebra in the builder): with L0's ports at weight Q (odd) the universal lapse needs the
  coefficients c Q w / P (c = 1/2 for L0, a pi/2-carrier first-order network) - never integers for P = 2^m, m >= 1
  (ONE-P1: gcd(Q, Q-1) = 1). So no EXACT universal lapse on today's weights.
- Minimal changes built in layers/gravity_l0.py, both with L0's port operator SPLIT into an on-site mass part
  M(0) = Sum_d W_d (clock factor N = 1 - U) and a symmetric difference-form transport part (link factor 1 - 2U,
  gamma = 1), reciprocal from one potential:
  (R) "rounded": L0 keeps weight Q (today's board bit for bit when F = 0); the lapse uses (Q - 1) w in place of Q w:
      EP violated by the relative factor (Q-1)/Q (1.9e-9 at Q = 2^29 + 1).
  (W) "weight": L0's ports take weight Q - 1 = 2Pk (the ONE headroom weight: one cone c_Q for L0 and the fields); the
      lapse is exactly universal; cost: L0 is not today's board bit for bit (except its vacuum).
- TEST (demos/gravity/l0_ep.py): Q = gravity_Q(2^10, 4) = 8193, L = 4, uniform static lapse gear F = 2P U0
  (U0 = 0.05, prepared, held; the reads are differentiated one-way for this clock test, the reciprocal blocks are
  checked by check_reciprocity separately); an L0 k = 0 eigenmode of Sum_d W_d with the integer eigenvalue mu = 4
  (rational eigenvector, amplitude 2^20) as the L0 clock; a first-order matter clock (weyl, mass only, k = 0) and a
  second-order atom. Readout (CLICK space): crossing rates -> N_click = cos w / cos w0 (first order, exact relation
  2 cos w = N mu/3) and the half-angle reading for the atom. Pass: (W): |N_click(L0)/(1 - U0) - 1| <= 1e-4 and
  |N_click(L0)/N_click(weyl) - 1| <= 1e-4; (R): the same within 1e-4 + U0/Q; the atom vs (1 - 2U0)^{1/2} reported
  (first vs second order differ at U0^2/2 without the beta block). Also: vacuum fixed, rewind exact, reciprocity of
  the reciprocal (R) and (W) blocks.

## RESULT F4b (written Tue Nov 10 10:49:28 UTC 2026; results/gravity/F4b.json) and PRE-REGISTRATION F4c
- F4b: Sum_x h00 EXACTLY constant at every sample (102,727,245): the k = 0 mode is frozen (R-a works, no t^2 growth).
  BUT the local U swung to -0.29 / +0.28 and the light exploded at t = 100: the minimal first-order test matter's
  b-only stress is NOT conserved (A10-2), and the accumulator chain integrates its non-conservation (S4 row C1: "the
  residual h00 drift tracks the non-conserved stress proxy"); with lattice noise (|b| <= 16, hop 2^25) this local drift
  dwarfs the offset C0 (U 0.0015). FAIL as registered (U >= 0 and light bounded both fail; Sum frozen passes).
- F4c (before running; new file demos/gravity/f4c_background.py = F4b with arguments): (i) kappa = 0 (no stress
  source: R-a + offset with the load, light noise and weyl noise reading h00): pass criteria of F4b; (ii) kappa = 2 with
  weyl noise |b| <= 2 (64x weaker non-conservation): report min/max U, growth and the explosion time if any.

## RESULTS L0-EP, F4c; integration answers C3/C4/E1 (written Tue Nov 10 10:51:41 UTC 2026)
L0-EP (results/gravity/L0_EP.json, run 10:49:02-10:49:06; layers/gravity_l0.py, demos/gravity/l0_ep.py):
- THEOREM confirmed: build_lapse on today's L0 (weight Q w) REFUSES (non-integer coefficient -8193/2048 at Q = 8193,
  P = 1024): no exact universal lapse on today's weights (ONE-P1).
- The reciprocal L0 lapse (split: N on the k = 0 mass part Sum_d W_d, N/psi^2 on the symmetric difference transport;
  effective weight (Q-1) w) passes check_reciprocity with ZERO designations (1,927 monomials checked).
- Clock test (L0 k = 0 eigenmode of Sum_d W_d with mu = 4 as the L0 clock, read from L0 CLICKS; U0 = 0.0498):
  * mode R (today's weights, rounded lapse): N_click(L0) = 0.9502022 vs predicted 1 - U0 (Q-1)/Q: dev 8.7e-7 (PASS);
    first-order matter clock N_click(weyl) = 0.9501963 vs 1 - U0: dev 1.0e-6; universality L0/weyl - 1 = 6.27e-6 =
    the predicted EP violation U0/Q = 6.08e-6 (PASS within 1e-4 + U0/Q).
  * mode W (L0 ports at weight Q - 1): N_click(L0) dev 9.9e-7; universality L0/weyl - 1 = -5.2e-9 (EXACT up to
    rounding) (PASS).
  * second-order atom: half-angle N vs sqrt(1 - 2U0): -1.3e-7; atom vs L0: -1.38e-3 (the O(U^2) difference between
    first- and second-order clock factors without the beta block, as registered).
  * vacuum fixed 10/10, rewind 20 + 20 exact.
- ANSWER: an EXACT universal lapse on L0 requires the minimal change (W): L0's ports at the ONE headroom weight Q - 1
  (= 2Pk), with L0's port operator split into the k = 0 mass part (clock factor) and the difference transport (link
  factor). Cost: L0 is today's board only in its vacuum (its cone becomes c_Q, the same as every field: one cone). The
  in-rules alternative (R) keeps today's board bit for bit when F = 0 and violates the EP by exactly the relative 1/Q
  (1.9e-9 at Q = 2^29 + 1). Both need the ONE-VACUUM embedding (fine couplings into L0).
F4c (results/gravity/F4c_i.json, F4c_ii.json):
- (i) kappa = 0 (OD2 accumulator lapse with R-a + offset, load, light noise 2^8, weyl noise 16): Sum h00 EXACTLY
  constant; min U = 0.000, max U = 0.037 at every sample; light x3.4, weyl x3.9, no explosion in 700 updates: PASS
  (no t^2 growth, N <= 1, light bounded 700 updates).
- (ii) kappa = 2, weyl noise 2: Sum h00 constant, but the NON-conserved b-only test stress drives local h00 to
  U in [-0.11, 0.12] and light explodes at t = 260 (was t = 100 at noise 16): the stress-chain drift (S4 C1) is the
  remaining obstruction; it needs an exactly conserved first-order stress (OPEN).
C3 (one lapse): layers/gravity_select.py: gravity_blocks(lapse="od2" | "wave"): od2 -> OD2 + build_lapse_oneway(field
"od2.h00") + beta on od2.h00, NO metric block; wave -> metric + reciprocal build_lapse(metric.h00) + beta, NO OD2.
Checked at Q = 2^29 + 1 with integrator-like first-order matter (hop 2^27, mass 3*2^29, Wilson 2^24) and atoms:
reciprocity PASS (70 / 175 designations), vacuum fixed.
C4: od2_hop_stress_scaled(ns, spec, kappa, divisor) (coefficient kappa c / divisor exact, else ValueError); at hop 2^27
the smallest unit is divisor 2^27 (diagonal) / 2^26 (off-diagonal).
E1: dressed_link_potential(spec, field, P, gamma) exposes lambda_link * c b_t(x) b_s(x+e), lambda_link = 1 -
c_link (F_x + F_y)/P (the factor build_lapse applies); its F-dependent part is degree 3, i.e. a rank-4 entry when used
as a current SOURCE (OD4 ruling applies; with the OD2 one-way lapse it can be a designated one-way source).

## PRE-REGISTRATION D8e: redshift via light, echo-free window (written Tue Nov 10 10:52:25 UTC 2026, before running)
New file demos/gravity/d8e_redshift.py = D8d with L = 96, T = 160, readout window t = 45..150 (after the direct wave
reaches F at ~29 + transient, before the first box echo at ~(96 - 15)/0.52 ~ 155). Same criteria as D8b
(|w_LF/w_E,ret - 1| <= 2e-3; |R_light/pred - 1| <= 3e-3).

## RESULT D8e (written Tue Nov 10 10:57:08 UTC 2026; results/gravity/D8e.json, run 10:52:25-10:56:55)
Echo-free window (L = 96, t = 45..150, 21 light crossings at F), drift-free field: light frequency at F vs the
retarded emitter -0.24 % (criterion 0.2 %: marginal FAIL); redshift via light R_light = 1.03165 vs the GR first-order
prediction 1.02834: +0.32 % (registered criterion 0.3 %: marginal FAIL; the half-angle-corrected reading +0.25 %).
Improved from +0.92 % (D8d, box modes) to +0.32 %: the box-mode beat was the main bias; the remaining 0.2-0.3 % is the
short window (21 crossings). Redshift VIA LIGHT: within 0.3 % of GR first order, not within the registered 0.3 %.

## Post-final summary of the new files (written Tue Nov 10 10:57:08 UTC 2026)
New files after the freeze (none of the frozen core touched): layers/gravity_l0.py (L0 lapse: build_l0_lapse,
build_l0_weight, l0_hops), layers/gravity_select.py (gravity_blocks one-lapse flag, build_lapse_oneway,
od2_hop_stress_scaled, dressed_link_potential), demos/gravity/{f4b_background, f4c_background, l0_ep, d8d_redshift,
d8e_redshift, d5b_freefall, d5c_freefall, integrator_check, f3_collapse, d2c_shapiro, d7_slows}.py. Census of the new
blocks: rank 3 (F b b), no constants, no a-reads; build_l0_lapse(oneway=False) reciprocal with 0 designations;
one-way variants designated (L0_READ_WHY, ONEWAY_LAPSE_WHY).

## C8 answer and PRE-REGISTRATION F4d (written Tue Nov 10 10:59:38 UTC 2026, before running)
C8 (centred one-way LINK lapse read for the OD2 lapse): NOT B3-local (DERIVED): the centred value h00(t+1) contains
h0i(x - e_i) for all i, so with the link's b(x + e) every endpoint choice gives three-node or edge offsets; only the
on-site clock factor is local. Options sent to main (~11:00): (a) OD2 lapse with the centred clock factor and no h00
link factor (gamma = 0 for transport); (b) the WAVE lapse (b-only, M' exact, reciprocal) + R-a as a background gear
(this test); (c) a matter time shift in X (not pursued).
F4d (new file demos/gravity/f4d_background.py): D7's system (wave lapse metric.h00, reciprocal clock-pair load
U3 = 0.02, headroom light noise 2^8, reciprocal build_lapse) PLUS a prescribed background gear B (u = 6Q b, holds
a = b = Ebar) with the one-way linear source u_F += -b_B (designated: R-a, the declared uniform k = 0 background;
deviation form: B = 0 in the vacuum); Ebar = floor(S/N) and the residue S - N Ebar as +1 on the first nodes; F prepared
F_s + C0 (C0 = -min F_s). L = 32, T = 700. Pass: the uniform mode does not grow (|mean U(t) - mean U(0)| <= 0.01 at every
sample), min U >= 0 and max U < 1/4 at every sample, max |light| <= 10 x initial; plus the declared reversor (M' on
every gear) X F^10 X F^10 = id on the prepared state.

## RESULT F4d (written Tue Nov 10 11:01:24 UTC 2026; results/gravity/F4d.json, run 10:59:39-11:00:38) and PRE-REGISTRATION F4e
F4d (option (b): wave lapse + R-a background gear + k = 0 offset; self-consistent reciprocal load U3 = 0.02, light
noise 2^8; L = 32, T = 700):
- PASS: N <= 1 at every sample (min U = 1.4e-6 >= 0), max U = 0.122 < 1/4, light bounded (x4.7, no explosion in 700),
  declared reversor M' X F^10 X F^10 = id (exact), Newton III exact by construction (reciprocal lapse; the background is
  designated one-way data).
- FAIL (registered |mean U drift| <= 0.01): the uniform mode still drifts upward, mean U +0.0012 / 0.0047 / 0.011 /
  0.021 / 0.034 / 0.053 / 0.080 at t = 100..700 (~t^2, slightly faster). The static background cancels S(0) exactly,
  but the self-consistent b-only source is not conserved (A10-2): the load's (X^2 + Y^2) grows in its own potential
  (adiabatic invariant, F3 mechanism at a weaker level), and the k = 0 mode of the WAVE lapse integrates S(t) - S(0).
  Relative to F4/D7 (no background: mean U +0.24 by t = 240) the drift is ~25x smaller.
- What (b) LOSES relative to OD2: (1) exact freezing of the k = 0 mode (OD2: Sum h00 exactly constant for ANY source);
  (2) the exact momentum constraints and harmonic constants (OD2: C^i, C^0 exactly constant; wave metric: Lorenz C only
  as a dressed identity driven by source non-conservation + remainders, G5/G5b); (3) OD2's dressed Hamiltonian identity.
  What (b) KEEPS: one reciprocal potential (Newton III exact), gamma = 1 (link factor), M' mirror exact, B3 locality.
F4e (before running): F4d with a 4x weaker load (U3 = 0.005), same criteria; if the drift scales as U3^2 it should
stay below 0.01 over 700 updates.
- F4e PASS (results/gravity/F4e.json, 11:01:25-11:02:08): U3 = 0.005: max |mean U drift| = 0.0058 (<= 0.01), min U = 0
  (N <= 1 at every sample), max U = 0.015, light x4.8, no explosion in 700, M' mirror exact. The drift scales ~U3^2
  (0.0795 -> 0.0058 for a 4x weaker load, ratio 13.7 vs 16): option (b) holds the uniform mode to O(U^2 t^2) - fine
  in weak field / moderate T, not exact (OD2 is exact for any source).
(written Tue Nov 10 11:02:16 UTC 2026)

## GRAV-FIX (manager 12:12): PRE-REGISTRATION (written Tue Nov 10 12:12:38 UTC 2026, before any code/run; 1 core, nice 19)
Context: BANG-2 (Study 8) - the v2 default (Q = 2^33 + 1, P = 2^20, k = 2^12) with the S2* seed (A = 2^16, L = 6, R-a
background 0) blows up at t ~ 1880: U_mean ~ t^2, and beta.G grows in the corner mode k = (pi,pi,pi).
Frozen files are not edited; new files: layers/gravity_beta_fix.py, prepare/gravity_ra.py, demos/gravity/gfix_*.py.
T1 MECHANISM. Linear theory (DERIVED, checked numerically below): metric.h00 (F) and beta.G (G) share the ONE headroom
stencil, whose corner mode has cos w = -1 + 2/Q (marginal, w ~ pi - 2/sqrt(Q)) for BOTH; G's source -k Lap(F^2) contains
-2k Fbar Lap f (Fbar = the uniform part of F, f the deviation), so F's corner component drives G's corner at the SAME
frequency: resonance (linear growth x Fbar). Run gfix_mech.py: the v2 default + S2* (A = 2^16, L = 6, background 0) for
700 updates (as BANG-2), printing every 50 updates the corner projections |G_pi| = |Sum (-1)^(x+y+z) G|/N,
|F_pi|, Fbar/2P and max|G|. CONFIRM iff |G_pi| dominates max|G| and grows faster than |F_pi| x Fbar-scaled static
expectation; REFUTE otherwise.
T2 FIX candidates (exact: integers, rewind, vacuum, B3, rank <= 3), in layers/gravity_beta_fix.py, block name "beta",
gear "G" (drop-in for the default's beta block; the matter's G read and e1d stay unchanged):
 (A) G with the reduced (stencil-B) face weight w_G = (Q-1)/2 and source -(k/2) Lap(F^2): static law G = F^2/(2P)
     exactly (beta = 1 kept), G's corner at cos w = 1/Q (w ~ pi/2), every G mode slower than F's (c_G^2 = c_F^2/2):
     no resonance with F at any k != 0 (S1-M2 Y15 rule: auxiliaries need different speeds).
 (B) w_G = 3(Q-1)/4, source -(3k/8) Lap(F^2): corner at cos w = -1/2.
 Test (gfix_mech.py with the replaced block, same 700 updates): |G_pi| stays <= 1e3 x (its value at t = 50) and max|G|
 stays <= 2 x the static scale max(F)^2/(2P) + 10; plus: vacuum fixed 10 updates, rewind 20 exact, reciprocity (only
 designated one-way G terms), static law check G = F^2/(2P) on a prescribed static F (beta = 1) within 2 units.
T3 DATA: prepare/gravity_ra.py ra_two_time(...): Ebar from the TWO-TIME mean of the lapse source on the initial snapshot,
 S = (S(b) + S(a))/2 with S the sum of (u_F - stencil(F) + b_B) evaluated on the state and on its a<->b swapped copy
 (exact for pi/2-carrier matter and L0 at first order: <b^2> = (b^2 + a^2)/2); integer Ebar = floor(S/N) plus the residue as
 +1 on the first nodes. Test: the t^2 coefficient of U_mean over 700 updates with Ebar vs with 0 (S2* and the L0 dark
 seed): expected reduction >= 10x.
T4 HORIZON: v2 default + fix (A) + T3 datum, S2* (A = 2^16, L = 6): run as long as time allows (target >= 1e4 updates),
 report max bit length per namespace every 100 updates, U_mean, |G_pi|; the horizon = first update with > 60 bits.

## GRAV-FIX T1 RESULT (written Tue Nov 10 12:19:21 UTC 2026; results/gravity/GFIX_T1_default_1700.json, run 12:15-12:19)
CONFIRMED (own run, current RC1 default + S2* A = 2^16, L = 6, background 0; my run differs in detail from BANG-2's pin:
U_mean 1.36e-4 at t = 600, then ~0.9-1.0e-4 to t = 1200): beta.G is EXACTLY 0 until t ~ 1300 (the source K ~ 1e9 << D/2
keeps it in the remainders), then grows only in the corner mode: |G_pi| = 1,049 / 12,840 / 44,362 / 110,355 at
t = 1400 / 1500 / 1600 / 1700 with max|G| = 1,057 / 12,854 / 44,383 / 110,397 (corner = everything). The driver
is there: F's own corner component grows steadily, |F_pi| = 1 (t = 150) -> 147 (700) -> 414 (1200) -> 875 (1700),
and Fbar = 2P U_mean ~ 200-1700; the source -k Lap(F^2) contains 24 k Fbar F_pi (24 = 2 x 12, the corner Laplacian),
which sits at F's corner frequency, cos w = -1 + 2/Q, exactly G's corner frequency (same stencil): resonance. U_mean
then rises again (2.4e-4 at 1400 -> 8.2e-4 at 1700) as the matter reads the alternating G.
Linear theory (DERIVED): headroom stencil b' + a = 2b + ((Q-1)/(3Q)) Lap b: corner (Lap = -12): 2 cos w = -2 + 4/Q,
identical for F and the default G; detuned G (A): 2 cos w = 2 - 12 w_G/(3Q) = 2/Q (w ~ pi/2); (B): 2 cos w = -1.

## GRAV-FIX T2 RESULT, fix (A) (written Tue Nov 10 12:23:04 UTC 2026; results/gravity/GFIX_T2_A_1700.json, run 12:19-12:22)
Same system and data with the detuned beta (A) (w_G = (Q-1)/2, source -(k/2) Lap(F^2)): the corner resonance is GONE:
|G_pi| = 0 to t = 1500, 0.35 at 1600, 0.79 at 1700; max|G| = 6 / 10 at 1600 / 1700 against the static scale
max(F)^2/(2P) = 1.5 / 2.6 (criterion: <= 2 x static + 10: PASS); default at the same times: 44,362 / 110,355.
NOT removed by (A): U_mean still rises after t ~ 1200 (1.0e-4 -> 7.95e-4 at 1700, ~x1.5 per 100 updates, identical
to the default to 3 digits: it is not caused by G) and |F_pi| grows sublinearly (414 -> 650). The U_mean rise is the
k = 0 obstruction (T3) and, being faster than t^2 here, a k = 0 self-gravity feedback (F3-type: the reciprocal lapse
slows the seed's clocks, its b-only source grows) - see T3/T4.
T4 launched 12:23:04: fix (A) + the two-time R-a datum, T up to 12,000, every 200 (stop at > 60 bits).

## GRAV-FIX T2 static/exactness and T3 data (written Tue Nov 10 12:25:22 UTC 2026)
T2 static/exactness (results/gravity/GFIX_static.json, 12:23:15): for the default, (A) and (B): G prepared at F^2/(2P)
(F in multiples of 2^11) is an EXACT fixed point (change 0 after one update): the static law G = F^2/(2P), i.e.
beta = 1, holds exactly for the detuned blocks; vacuum fixed, rewind 20 + 20 exact, reciprocity PASS (7 designated
G-source terms, as the default), rank 3; (A): w_G = 2^32, k_G = 2^11; (B): w_G = 3 x 2^31, k_G = 3 x 2^10.
T3 data: prepare/gravity_ra.py: ra_two_time (first draft) and ra_free_mean (the time mean of the lapse source over
the FREE linear evolution of the sourcing gears, exact per Fourier mode from the initial (b, a); one float computation
of one initial number). Values (A = 2^16, L = 6, default + fix (A)):
- L0 dark seed: free mean S = 2.305e14 per board (instantaneous S(0) = 1.407e14, reproduced exactly by the k-space
  sum), Ebar = 1,067,076,579,528 per node (+1 on 97 nodes). The two-time shortcut (b^2 + a^2)/2 is NOT enough for L0
  (its bands are not at the pi/2 carrier): use ra_free_mean.
- S2*: free mean S = 0 exactly (and S(0) = 0): the first-order datum is Ebar = 0. The positive mean source BANG-2
  sees (my run: U_mean / t^2 ~ 5.2e-10 for t <= 400, i.e. S ~ 1.2e10) is NOT in the free linear evolution of the
  matter/L0 gears: it comes from the NONLINEAR couplings the seed excites (the e1d lapse/beta dressing sources F with
  degree-3 terms A J(b, b); gauge/choice), so it cannot be computed from the initial snapshot at first order; it can
  only be declared from a calibration measurement (prepare.seed.ra_background(state, T, value)).
T4 note (written Tue Nov 10 12:25:41 UTC 2026): for S2* the first-order R-a datum is EXACTLY 0 (ra_free_mean and ra_two_time both give
S = 0), so the running T4 (fix (A) + ra_two_time) IS "fix + correct first-order datum" for S2*; it is kept running.

## GRAV-FIX T4 RESULT and the change for the integrator (written Tue Nov 10 12:51:51 UTC 2026; results/gravity/GFIX_T4_A_twotime.json,
## run 12:23-12:51, 1 core nice 19, 11,856 Python-int steps, exact)
v2 default + fix (A) + the first-order R-a datum (0 for S2*), S2* A = 2^16, L = 6: BOUNDED for all 12,000 updates
(target 1e4 reached; BANG-2's default blew up at ~1880, my default run had |G_pi| 110k by 1700). Max bit length at
t = 12,000: em 36, metric 21, beta 17, matter 16. Trends (every 200 updates in the JSON):
- beta.G: |G_pi| = 3.6 (2000), 279 (5400), 26,097 (10,000), 65,462 (12,000) - EXACTLY the static (non-resonant)
  response of G = F^2/(2P) to F's own corner component: 2 Fbar F_pi/(2P) = 26.1k at 10,000 and 65.4k at 12,000.
  No resonant growth.
- The remaining growth is NOT in beta: U_mean = 2.0e-3 (2000), 0.040 (6000), 0.36 (10,000), 0.63 (12,000), rising
  ~1.5e-4 per update at the end; |F_pi| (the lapse field's own marginal corner mode) = 828 / 9,431 / 36,147 / 52,011.
- NEW HORIZON (projected): U_mean reaches 1 near t ~ 14,500 (linear extrapolation of the last 1,000 updates), where the
  first-order clock factor 1 - U vanishes and the transport factor 1 - 2U reaches -1 (CFL edge of the first-order
  species). Cause: the k = 0 mode (closed-board "collapse") driven by the positive mean source that S2*'s NONLINEAR
  evolution develops (its free first-order source mean is exactly 0, so no initial datum cancels it), plus F's own
  marginal corner mode (headroom stencil, one-cone principle: not changed).
CHANGE FOR THE INTEGRATOR (one line + import; frozen files untouched):
- layers/system.py, default_system(): after the gravity blocks are appended (beta=True), replace the "beta" block:
    from .gravity_beta_fix import build_beta_detuned, replace_beta
    blocks = list(replace_beta(tuple(blocks), build_beta_detuned(Q=Q, P=P, k=K, field=lapse_field, num=1, den=2)))
  (P = 2^20, k = 2^12, Q = 2^33 + 1 -> w_G = 2^32, k_G = 2^11; block name "beta", gear "G", vacuum 3Q - 1: mbeta and
  e1d unchanged). Candidate (B) (num=3, den=4: w_G = 3 x 2^31, k_G = 3 x 2^10) is statically verified only.
- prepare/seed.py (data): after placing a seed, set the R-a datum with
    from .gravity_ra import ra_free_mean;  state, info = ra_free_mean(Engine(tensor, Q), state)
  (first-order exact time mean of the lapse source of the free sourcing gears; S2*: 0; L0 dark seed A = 2^16, L = 6:
  Ebar = 1,067,076,579,528 per node, +1 on 97 nodes). Seeds whose mean source is generated nonlinearly (S2*) need a
  declared measured value instead (prepare.seed.ra_background).
