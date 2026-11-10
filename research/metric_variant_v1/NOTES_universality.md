# NOTES_universality — UNIV-BUILDER: universal lapse for the gauge-layer matter and the E1 photon (DECLARED CANDIDATE, DEFAULT OFF)

Gap (R-P1 row A1 / J4, review/AGREE_P_final.md 12:29 UTC): in the v2 default only the Dirac pair (matter_lapse_c, R1) and
L0 (form C) read/source the lapse. su2/su3/u1 psi clocks (cos w = 2/3) are bit-identical with and without gravity; E1
reads gravity only through its source dressing; E1 field energy does not gravitate.

NEW FILES ONLY: layers/universality.py, tests/test_universality.py, this file, results/universality/. No existing file is
edited. Switch (for the integrator, NOT applied): `universality: bool = False` in default_system.

## PRE-REGISTRATION (written Tue Nov 10 12:57:11 UTC 2026, before any test of this file was run)

### Constructions (declared before testing)
U1 GAUGE-MATTER LAPSE (layers/universality.py build_gauge_lapse). For each compact gauge layer (psi matter, links
U = A 1 + W), the matter potential is split into GAUGE-INVARIANT composites
  S(x)    = (M/2) |psi(x)|^2,                         M = mass + 6 kappa A   (the k = 0 rest coefficient: cos w0 = M/D)
  H_k(x)  = kappa <psi(x), U(x,k) psi(x+e_k)> - (kappa A/2)(|psi(x)|^2 + |psi(x+e_k)|^2)   (vanishes at k = 0 in vacuum)
  (S + Sum H = the layer's own (mass/2)|psi|^2 + kappa <psi, U psi>, identically.)
  Phi_L = - Sum_x (F(x)/(2P)) S(x) - Sum_{x,k} ((F(x) + F(x+e_k))/(2P)) H_k(x)      (R1 pattern: clock 1-U, link 1-2U)
  forms: "site" = clock term only (H not lapsed); "cov" = clock + full covariant H (rank 4: F psi W psi);
         "vac" = clock + H with U -> A 1 (the matter_lapse_c pattern applied literally; NOT locally gauge invariant).
  Integrality: u-coefficients need M in 4P Z ("site"), plus kappa A in 4P Z ("vac"), plus kappa in 2P Z ("cov").
  PREDICTION (arithmetic, to be confirmed by the builder raising/not raising): at the default (Q = 2^33+1, P = 2^20,
  A = kappa = 2^16, mass = Q+3) M = 4Q is NOT in 2P Z, and "cov" has kappa/(2P) = 1/32: both non-integral. The
  variant therefore uses the DATA-LEVEL gauge mass Q - 1 (M = 2^35 = 4(Q-1); cos w0 = 2/3 - 2/(3Q)); "cov" is tested at a
  DECLARED test regime A = 2^11, kappa = 2^21 (kappa A = 2^32 as in the default family).
U2 PHOTON LINK LAPSE (build_photon_lapse). E1 transport u_A = D A + (Q-1) Lap A (component-wise) gets the second-order
  (gamma = 1) link factor (1 - (F_x + F_y)/P) = 1 - 4U on every dual link (A_d(x), A_d(x+e_j)):
  Phi_gamma = + k Sum_{x,d,j} (F(x) + F(x+e_j)) (A_d(x+e_j) - A_d(x))^2,   k = (Q-1)/(2P) = 2^12 (integral), rank 3,
  reciprocal (E1 gradient energy sources F: u_F += k Sum (dA)^2). The lapse sits on the storage link (x, x+e_j), half a
  link off the dual link's centre (the centred read needs F at x+e_d: edge offset, C8-type).
U3 SOURCING = the reciprocal partners of U1 ("site": -(M/(4P))|psi|^2) and U2 (+k (dA)^2). Both b-only single-time.

### Tests (tests/test_universality.py; results/universality/*.json; L <= 4; nice -n 19, 1 core)
T1 rest clock, exact tensor reading: uniform psi eigenmode, uniform static prescribed F0 = 20972 (U0 = 0.0100002),
   vacuum links: 2P u_psi(F0) == (2P - F0) u_psi(0) at EVERY psi gear and node (exact integers), each of su2/su3/u1,
   forms site and cov. PASS = 0 mismatches.
T2 rest clock, dynamic cos-ratio reading: same mode, amplitude 2^10, L = 3, T = 1200, cos estimator
   c = Sum (b_{t+1} + b_{t-1}) b_t / (2 Sum b_t^2) at F0 vs F = 0. PASS: |c(F0)/c(0) - (1 - U0)| <= 1e-5 per species.
T3 Gauss/Noether with the lapse ON (prescribed RANDOM static F, |F| <= 2^14; random gauge state, random unit links):
   observe.gauge.GaugeView.gauss_check over T updates. PASS: "site" (default regime) and "cov" (test regime) 0 failures.
   "vac" EXPECTED to FAIL (count reported; it is the broken-covariance contrast).
T4 photon: (a) exact link factor: u_A of a single-node A excitation under uniform F0: neighbour coefficient ==
   (Q-1) - 2^14 F0 exactly; (b) dynamic: k = 2pi/4 standing-wave cos-ratio at L = 4 against the law
   1 - cos w = (1 - 4U0)(1 - cos w_0) (speed^2 factor), tolerance 1e-5;
   (c) Lorenz C exact (0 failures) and continuity exact (0 failures) with the photon lapse ON (e1 + matter, random
   non-uniform static F, random state); (d) dressed Gauss: uniform F0 -> exact with (Q-1) -> (Q-1)(1 - 2F0/P)
   (0 failures); non-uniform F -> the flat Gauss step residual equals -2 g div l(t) EXACTLY (l = the photon-lapse part
   of u_A) and is NONZERO (count reported): an exact defect accounting, not exact Gauss.
T5 photon obstruction (linear algebra, exact): the most general translation-invariant, B3-local, F-linear, A-linear
   term l_d(x) = Sum c F(x+o_F) A_k(x+o_A) in u_A that (i) equals lambda Lap at uniform F (lambda != 0) and (ii) maps
   every divergence-free A to a divergence-free l for a single-node F (necessary for any exact Gauss law with the
   rounding-free flat Lorenz accumulator) — PREDICTION: infeasible (rank argument), with a minimal counterexample.
T6 exactness: rank <= 4; B3 (Tensor builds); reciprocity report (designations counted) for U1 site/cov reciprocal and
   U2; vacuum bit-exact (U-blocks alone, 30 updates; composed with default_system() via compose_universality, L = 3,
   12 updates); rewind exact (random state, 20 updates forward + 20 back) on U1 and U2 subsystems; int64 headroom
   (engine dtype choice and plan bound vs 2^62 for the test states; Python ints where the guard demands).

### ADDENDUM PRE-REGISTRATION T7 (manager 13:13 request; written Tue Nov 10 13:18:57 UTC 2026, before T7 was run)
Question: does the CL-2A/CL-2B "U3" route — E1 dressed in FIELD-STRENGTH form through 2-path (plaquette) gears — keep the
dressed Gauss law exact with a non-uniform lapse, and does it bend light? T5 covers direct F(x+o) A_k(x+o') maps in u_A
only (b- and a-reads); it does NOT cover auxiliary gears.
Construction (tests/test_universality.py plaquette_block; candidate only): node gears B_xy, B_xz, B_yz (2-path, stored at
the base node), ONE potential Phi_B = Sum_x Sum_{i<j} [ (cB/2) B_ij^2 + (gam/2) F(x) B_ij^2 + beta B_ij (curl A)_ij ],
(curl A)_ij(x) = A_i(x) + A_j(x+e_i) - A_i(x+e_j) - A_j(x) (every monomial on one node or one link: B3), reciprocal,
rank 3. A reads B only through the lattice co-curl, so div(u_A) gains div curl^T(beta B) == 0 IDENTICALLY.
PREDICTIONS (DERIVED before running):
 (a) flat E1 Gauss step identity, Lorenz C and continuity: 0 failures with a random NON-uniform static lapse, for any beta.
 (b) stability at E1's headroom stencil: the transverse corner mode k = (pi,pi,pi) has u = -D + 12 (margin 12); the 2x2
     block [[D - (Q-1) lam, beta sqrt(lam)], [beta sqrt(lam), cB]] at lam = 12 is inside [-D, D] iff beta^2 <= cB + D.
     So a strong channel (beta = 2^34, cB = 6 - 2^34) RUNS AWAY; a stable channel (beta^2 <= cB + D) softens the low-k
     transverse stiffness by w0 = beta^2/(D - cB) <= (cB + D)/(D - cB) = O(1) against Q - 1 = 2^33: no measurable bending.
 (c) measured light factor with the stable channel (beta = 2^17, cB = 6, gam = 2(D - cB)/P = 12 2^13 integral): (1 - cos) ratio under F0
     equals 1 to < 1e-6 (i.e. NOT 1 - 4U0 = 0.96).

## RESULTS (written Tue Nov 10 13:32:29 UTC 2026; JSON in results/universality/, each with its own UTC stamp)
Labels: EXACT = integer identity checked at every node/update; PASS/FAIL against the pre-registered criterion;
POST-HOC = changed or added after a run.

U1 gauge-layer matter
- Integrality (prediction CONFIRMED by the builder): default mass Q+3 -> M = 4Q, not in 2P Z (every form raises);
  universality mass Q-1 -> M = 2^35: "site" and "vac" integral; "cov" raises at kappa = 2^16 (kappa/(2P) = 1/32).
  OWNER NOTE (13:13 approval of the rank-4 kind "uncharged singlet field x gauge-covariant rank-3 composite"): "cov" IS that
  kind, but it is NOT INTEGRAL in the v2 gauge regime. It needs kappa in 2P Z, i.e. A <= 2^11 at kappa A = 2^32 (or P <= 2^15).
- T1 PASS (EXACT): 2P u_psi(F0) == (2P - F0) u_psi(0) and u_psi(0) == M psi, 0 mismatches, su2/su3/u1 x site/cov/vac
  (54/108/162 gear-node checks each). Rest clock N = 1 - U exactly in the cos-ratio reading (cos w = (1 - U) M/D).
- T2: pre-registered raw estimator FAILS (rounding-limited at amplitude 2^10): deviations 3.35e-4 (u1), 3.35e-4 (su2),
  -5.0e-4 (su3). POST-HOC exact-input estimator (2u_t = D(b_{t+1}+b_{t-1}) - r_t + r_{t+1}, read from consecutive states):
  4.8e-7, 3.0e-6, 4.8e-6 (< 1e-5; the residual is the link response to psi). "cov" dynamic run removed POST-HOC: at its
  test regime a 2^10 psi is far beyond the A9 rule, and the run did not finish in 600 s. int64 throughout.
- T3 PASS (EXACT): Gauss/Noether with a random static lapse (|F| <= 2^14) ON.
  - site 0/540 (u1), 0/1620 (su2), 0/2916 (su3) failures; cov 0/540, 0/1620, 0/2916.
  - Local covariance bit-exact (2 random gauge fields x 8 updates) for site and cov.
  - vac: 540/540, 1620/1620, 2916/2916 failures, not covariant (the contrast, as registered). int64.
  - POST-HOC preparation: U = A1 + noise plus a random local gauge map. Random per-link units (flux) at the default regime
    RUN AWAY in 6 updates (18 -> 272 bits) WITH OR WITHOUT the lapse (side finding on the v2 gauge regime, like A9).
- T6 PASS: U1 site/cov reciprocal (0 designations, 0 violations), rank 4 (the layer's own spring), vacuum 30 updates
  bit-exact, rewind 20 exact (gauge-generic random state, random lapse), int64.
- Gauge-matter TRANSPORT keeps the flat factor in "site" (moving gauge matter falls like 1911, CL-2A's U2 wording): OPEN
  until "cov" is integral (owner: gauge regime or P).

U2 photon (scalar-stencil link lapse)
- T4a PASS (EXACT): neighbour coefficient (Q-1) - 2^14 F0 = 8246329344 and on-site 6 + 6*2^14 F0, exactly.
- T4b PASS: k = pi/2 transverse mode at L = 4, 1500 updates: (1 - cos) ratio 0.9599990983 vs law 1 - 4U0 = 0.9599990845
  (1.4e-8). Speed factor 0.97980 = sqrt(1 - 4U0) = 1 - 2U0 + O(U0^2): gamma = 1 at first order. int64.
- T4c PASS (EXACT): Lorenz C 0/216 and continuity 0/216 failures, for both a uniform and a random non-uniform lapse.
- T4d:
  - Uniform lapse: the modified Gauss functional (Laplacian weight (Q-1)(1 - 2F0/P)) is EXACT (0/216).
  - Non-uniform lapse: the flat Gauss residual is nonzero at 216/216 checks and equals -2g div l EXACTLY (0/216
    accounting failures). So it is an exact LEDGER, not an exact Gauss law.
- Minimal counterexample: F = 1 at (1,1,1) and ONE transverse xy plaquette loop based there give div l != 0 at 10 nodes
  (+-8192 = +-2k, +-49152 = +-12k); a uniform F gives 0.
- DERIVED consequence: near a steady current in a lapse gradient the static A has div A = -(Q-1)^-1 Lap^-1 div l != 0, so the
  slaved Phi DRIFTS linearly (Phi(t+1) - Phi(t) = -div A).
- T5 (EXACT over Q; GF(p) for two primes agrees): the B3-local, translation-invariant, F-linear maps F(x+oF) A_k(x+oA) -> u_A
  that keep div A = 0 for a single-node F form a 12-dim space.
  - It consists of 3 maps "-F div A" (zero on transverse fields) and 9 first-order maps "curl of F A_k".
  - Their uniform transverse actions span rank 9; adding lambda Lap gives rank 10, so lambda Lap is UNREACHABLE.
  - Covers b- and a-reads, reciprocal or one-way. NOT auxiliary gears (see T7).
  - The rounding-free accumulator cannot read F at the physical scale (its coefficients must lie in 3Q Z; a lapse weight
    needs 3Q/(2P)).
- T6 PASS: U2 reciprocal (designations 278 = E1's own), rank 3, vacuum 30 bit-exact, rewind 20 exact. 10 updates ran on
  Python ints: the engine's overflow guard.

T7 2-path (plaquette) route, manager 13:13 (pre-registered 13:18:57)
- (a) PASS (EXACT): with B_ij gears read by A only through the lattice co-curl, Lorenz, continuity and the FLAT Gauss step
  identity show 0/216 failures under a random NON-uniform lapse, for both parameter sets. d o d = 0 survives with 2-path
  gears (AGREE_CL2 row 15 caveat: confirmed).
- (b) PASS (prediction confirmed):
  - The strong channel (beta = 2^34, beta^2 > cB + D) RUNS AWAY at L = 4: 45 bits at t = 25, 202 at t = 113.
  - The stable channel (beta^2 <= cB + D) stays bounded. Its slow bit growth (11 -> 15 in 300 updates) is E1's linear Phi
    drift from random C != 0 data.
- (c) PASS (prediction confirmed): with the stable channel the A trajectory under F0 is BIT-IDENTICAL to F = 0 (ratio 1.0
  exactly; the law would be 0.96). NO BENDING.
- Reason (DERIVED, 2x2 corner algebra): E1's headroom stencil leaves margin 12 at the transverse corner k = (pi,pi,pi).
  - A dynamical plaquette channel needs beta^2 <= cB + D, so its low-k weight w0 = beta^2/(D - cB) <= (cB + D)/(D - cB) is
    O(1) against Q - 1 = 2^33 for any B that follows the light.
  - A slaved (rounding-free) plaquette accumulator needs K_L + |K_B| <= 2, i.e. |beta| f <= 1.
  - Stiffening channels (cB > D) are unstable by themselves.
- VERDICT: the 2-path route keeps Gauss exact but cannot bend light at E1's flat stencil. It becomes the photon fix ONLY with
  an owner-level E1 redesign: lower the scalar stencil to open corner headroom (e.g. weight ~3Q/4) and let a plaquette
  channel |beta| ~ Q/4 carry the lapse. Then transverse c^2 is halved, c_T != c_L, and the plaquette reads are one-way
  (accumulator class). NOT built.

U3 sourcing (reciprocal partners)
- site: u_F += -(M/(4P)) |psi|^2 = -2^13 |psi|^2 per component (the rest energy). U2: u_F += k (dA)^2 (E1 gradient energy).
- Both are b-only single-time quadratics, so NOT exactly conserved (v3 §2 theorem; they ripple at 2w like the Dirac source).
- The gauge-LINK (W/gluon) and spring energies are not dressed: the |x|^4 part can never gravitate at rank <= 4 (CL-2A §3.4).

Composed default (T6_composed_default)
- compose_universality(default_system(), on=True): G 319 -> 319; monomials 10549 -> 10669 (+120: ulapse_su2 8,
  ulapse_su3 12, ulapse_u1 4, ulight 96); rank 4.
- Designations 1202 -> 1202 (0 new); reciprocity report OK, 0 violations; vacuum 12 updates bit-exact at L = 3; int64.
- on=False returns the system object unchanged.

SWITCH LINES for the integrator (layers/system.py; NOT applied by UNIV-BUILDER)
  signature:  ..., chiral: bool = False, electroweak: bool = False, universality: bool = False) -> System:
  info:       add "universality": universality to the info dict
  before "if electroweak and not chiral:":
    if universality:  # UNIV-BUILDER (R-P1 A1): gauge-matter rest clocks + E1 photon link lapse, DEFAULT OFF
        from .universality import universality_blocks; blocks, info = universality_blocks(Q, blocks, info)  # noqa: E702
  LAYER_FILES: add "layers/universality.py".
  Options: universality_blocks(..., gauge_form="site"|"vac"|"cov", photon=True|False). "cov" raises at the default
  regime (integrality); photon=False gives "Gauss exact, no bending".
