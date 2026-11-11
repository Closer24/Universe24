# NOTES_gauge — B1-GAUGE, stage 1: non-abelian (weak SU(2), strong SU(3)), compact U(1) and dynamic base links

All stamps are `date -u`. Pre-registrations are written BEFORE the acceptance runs; results are appended below,
never edited into the pre-registration. Core (core/), other builders' files and `universe24/` are not touched; no git.
Scope files: `layers/gauge.py`, `layers/links.py`, `prepare/gauge.py`, `observe/gauge.py`, `tests/test_gauge.py`,
`demos/gauge/`, this file. Evidence: `results/gauge/*.json`.

## Design (written Tue Nov 10 09:34:28 UTC 2026; code drafted 09:24-09:34, only builder smoke checks run so far)
- ONE potential per layer. Each builder writes the PHYSICAL potential Phi (integer polynomial, Fraction-exact) in the
  physical variables X = X0 + X~ (X0 = vacuum value), subtracts D X0.X~ and the constant (exact deviation shift,
  B10/N5-vac), ASSERTS that no linear term remains (static vacuum) and differentiates: u = dPhi~/db. So every block
  is reciprocal by construction (field sign +1 everywhere; no designated one-way term in any gauge block).
- One divisor D = 6Q, Q ODD, new-gear vacuum remainder r0 = 3Q - 1 (fixed by R'(r) = D-2-r / D-r).
- Compact layers (`build_gauge(group=...)`, wrappers `build_su2/su3/u1`):
  matter psi (SU(2): integer quaternion doublet, 4; SU(3): Z[i]^3 triplet, 6; U(1): Z[i], 2), links U on positive
  face links stored at the base node (SU(2) quaternion 4; SU(3) integer complex 3x3, 18; U(1) Gaussian 2),
  optional 2-path gears P(x;k1,k2) (6 ordered pairs).
  Phi = kappa <psi(x), U psi(x+e)> + mass/2 |psi|^2 + (D - c_U)/2 |U|^2 - (lam/4) Tr((U^dag U - A^2)^2)
        + kappa_P <P, U(x,k1) U(x+e_k1,k2)> + c_P/2 |P|^2 + beta <P(k1,k2), P(k2,k1)>,
  vacuum U = A*1, P = P0*1, P0 = kappa_P A^2/(D - c_P - beta) (integer), c_U = 4 kappa_P P0 (static balance).
  The ONLY rank-4 term is the spring (minus sign, lam > 0). Gauge maps act on PHYSICAL values (affine in the
  stored deviations), signed permutations for the integer groups Q8 / Z4 / the 96-element monomial subgroup of SU(3)
  (entries in {+-1, +-i}, det 1; DECLARED integer subgroup in place of Delta(27), whose omega-phases are not in
  Z[i]). Integer anti-Hermitian generators: SU(2) i, j, k; U(1) i; SU(3) i lambda_1..7, i diag(1,1,-2) (lambda_8
  rescaled) and i*1 (the U(1) of U(3): Phi is U(3)-invariant).
- Exact Noether/Gauss identity checked by `observe/gauge.py`: J^X_x(t+1) - J^X_x(t) = <b(t), T^X_x (r(t) - r(t+1))>,
  J^X_x = D sum a (T^X_x b) with physical values; T acts by X on matter at x, left on links/2-paths leaving x, minus
  right on links/2-paths arriving at x.
- Canonical parameters (test regime): Q = 2^19 + 1 = 524289 (D = 3145734), A = 256, kappa = 1024 (kappa*A = (Q-1)/2),
  mass = Q + 3 (k = 0 matter frequency cos w0 = 2/3; matter stays stable for link norms up to ~1.67 A), spring
  lam = 2 (radial w^2 ~ 4 lam A^2/D = 0.17); 2-path: kappa_P = 256, c_P = 0, beta = D - 2^19 -> P0 = 32, c_U = 32768.
- c2 dynamic base links (`layers/links.py`, G9-c). The board's right-Q8 (internal) symmetry made local:
  Phi_ref + Phi_c2 = sum b(x)^T W_d rho(U(x,d)) b(x+e_d), vacuum rho(U) = Q.
  * ZQ8 form (8 gears/link): U in the group algebra Z[Q8], rho(U) = sum_q U_q R_q, U = A[1] + W, kappa A = Q.
    Bit-exact LOCAL Q8 covariance by pure permutations (labels g -> g k(x); link components q -> k q k'^-1).
    Continuous SU(2) on the odd (quaternion) part: exact Noether identity with generators R_{e_a} - R_{-e_a} on the
    48 labels and [e_a] - [-e_a] on the links. R-M2 Q-lattice rule (manager 09:23/09:28): kappa = Q (A = 1) meets it
    (q_lattice validator), giving the exact joint mirror rhoL0 (L0) + M' (links) that fixes the joint vacuum; a finer
    link (kappa < Q) is allowed only as DECLARED (no exact mirror then fixes the L0 vacuum).
  * H form (4 gears/link, the spec's integer quaternion): acts on V- only via R_{e_a} - R_{-e_a}; U_eff = Q + 2 kappa W.
    THEOREM (stated here before the runs): no 4-component integer link gives a bit-exact LOCAL Q8 covariance on the
    48 labels. Proof: a local covariance by integer maps needs signed permutations S with S W_d = W_d S; then |S|
    commutes with the (positive) port permutations, so |S| = R_q (centralizer = Q8, exhaustive), and S = Diag(s) R_q
    with s constant (the port group is transitive), i.e. S = +-R_q. The quaternion algebra needs -1 -> -Id, but R_{-1}
    is +1 on the 24-dim V+ (it swaps g and -g). With a fixed V+ coupling, local R_q (q not +-1) multiplies the V+
    coupling by sign characters, so it is not even a symmetry. What survives exactly: global Q8, local centre Z2
    (when kappa | Q), continuous local SU(2) on V- as a Noether identity. The H form needs kappa not = 0 mod Q
    (kappa = Q leaves only the values U/A in {+1, -1}): DECLARED off the Q-lattice.
  * Links frozen (kappa = lam = 0): `observe.audit.frozen_equivalence` must give 0 base mismatches and 0 link
    deviations. With kappa != 0, excited reference data evolve differently BY DESIGN (the links respond); only the
    vacuum is today's board bit for bit.
- c1 (EXPLORATORY only): minimal frame-side register = one dynamical integer weight per +++ port entry (48 gears per
  link axis), vacuum = today's curved +++ connection. Stability test of the curved vacuum; NOT adopted unless stable.

## PRE-REGISTRATION of the acceptance tests (written Tue Nov 10 09:34:28 UTC 2026, BEFORE the acceptance runs)
Exact = bit for bit; "0 failures" means every node x every generator x every update. Seeds fixed in tests/test_gauge.py.
G1 BUILD/RECIPROCITY/LOCALITY: every gauge block (u1, su2, su3; with and without 2-path gears; c2 ZQ8 and H; c1)
   composes (B3 storage locality enforced by core), passes `check_reciprocity` with 0 designated terms, has rank 4
   only through the spring (no degree-3 monomial when lam = 0, except the c2/c1 coupling terms which are degree 2
   in u, i.e. rank 3), and the physical-support violations are listed (expected: only the 2-path terms).
G2 VACUUM: (a) each compact layer alone, L = 4, vacuum state, 50 updates: unchanged bit for bit, 0 clicks;
   (b) reference (Q-scaled) + each layer + c2 (ZQ8 kappa = Q): composed vacuum = universe24's vacuum run x Q for
   50 updates and the new gears stay at (0,0,3Q-1).
G3 NOETHER/GAUSS: L = 3 (SU(3)) / L = 4 (SU(2), U(1)), random initial data (matter |a|,|b| <= 64, links = random
   integer-group units * A + noise <= 8, 2-path deviations <= 16, random remainders), 40 updates (SU(3): 20), with and
   without 2-path gears and with the spring: identity exact with 0 failures for every generator. Also reported:
   max |remainder term| / max |J_matter|, and the swing of the matter-only charge vs the total (colour flow).
G4 COVARIANCE: random integer gauge fields (Q8 / Z4 / monomial-96), F^T(Gamma s0) == Gamma F^T(s0) bit for bit
   (a, b, r of every gear), T = 30 (SU(3): 15), with 2-path gears and spring. Wilson plaquettes invariant.
G5 REWIND + MIRROR: rewind T updates returns s0 exactly; plain mirror M F^T M F^T s0 = s0; M' (parity-preserving)
   likewise for the b-only gauge tensors; joint mirror rhoL0 (L0) + M' (new gears) for ref + c2 (ZQ8, kappa = Q).
G6 SPRING-BOUNDED NORMS: SU(2) with 2-path gears and SU(3), L = 4 (SU(3) L = 3), strong drive (matter amplitude 256 =
   A, i.e. eps = (A_psi/A)^2 = 1), t = 2000: lam in {1, 2, 4}: max_t max_links | |U|/(A sqrt(dim)) - 1 | reported,
   PASS iff < 0.5 for every lam >= 1 and the Gauss identity stays exact on a sampled window (every 100th update
   pair). Control lam = 0: expected runaway (report the time |U| > 4A or the value at t = 2000).
G7 LINKS FROZEN (c2): reference (Q = 4095 and Q = 524289) + c2 with kappa = lam = 0 from dense random reference data:
   `frozen_equivalence` 0 base mismatches, 0 link deviations over 50 updates; control kappa != 0 detects a difference.
G8 c2 EXACTNESS: ZQ8 kappa = Q (q_lattice validator passes): local Q8 covariance bit-exact, Noether identity
   exact (3 isospin generators), rewind, M and joint mirror exact; H form (Q = 4095, kappa = 65, m = 63):
   reciprocity, Noether identity exact, global Q8 and local centre Z2 bit-exact, rewind, M exact.
G9 c2 stability (report): ZQ8 kappa = Q with single-quantum reference excitations, and the fine forms with small
   reference amplitudes: max |U|/A over 2000 updates; no pass threshold (excited data evolve differently by design).
DEMOS (report, with exact integers):
D1 isospin rotation via links (SU(2)): a localized doublet excitation hops across one link set to A*q (q = a 90
   degree isospin rotation, integer: (A',0,0,A') ~ A(1+k)/sqrt2) vs the vacuum link: the transported isospin vector
   is rotated (gauge-covariant transport); two packets exchange isospin through the dynamical links, total exact.
D2 colour flow matter <-> field (SU(3)): matter-only colour vs field colour vs total over the run; total changes only
   by the exact remainder term.
D3 non-abelian witness: matter injected at x0 reaches the opposite corner of a plaquette by two 2-step paths. Links
   with the SAME multiset {i, j} in swapped order on the two paths: amplitude proportional to (j i + i j)psi = 0 for
   SU(2) (anticommuting) vs 2 j i psi in the same-order configuration; the U(1) analogue with {i, i} never cancels.
   PASS iff the SU(2) swapped-order far-corner amplitude is 0 up to the rounding floor while the same-order one is
   >= 100x larger, and the U(1) control is non-zero.

## RESULTS, first acceptance runs (written Tue Nov 10 09:41:24 UTC 2026; runs 09:37:36-09:40:44 UTC, nice 10, <= 2 threads)
Raw numbers: `results/gauge/G*.json`, `demos/gauge/D3.json`. All exact-integer.
| test | verdict | numbers |
|---|---|---|
| G1 build/reciprocity/locality | PASS | u1/su2/su3, with/without 2-path, lam 0/2: all reciprocal (56-5163 monomials checked, 0 designated), b-only, constant-free; lam = 0 -> no degree-3 monomial (rank 3), lam = 2 -> rank 4 only via the spring; physical-support violations ONLY with 2-path gears (u1 120, su2 384, su3 2376: the U(x+e_k1,k2) factor spans the plaquette); P0 = 32, c_U = 32768. c2 ZQ8/H at Q = 4095 and 524289 with kappa = Q: reciprocal, q_lattice_violations(("ref.*",)) = [] (validator on), 0 support violations; c1 port-weights reciprocal. |
| G2 vacuum | PASS | each layer alone, L = 4: 0 changed updates, 0 raw clicks (50 updates; su3 20); ref + su2 + c2 (kappa = Q) composed vacuum unchanged for 30 updates. |
| G3 Noether/Gauss | PASS | 0 failures: u1 2560/2560, u1+P 2560, su2 7680, su2+P 7680, su3 and su3+P 9 generators x 27 nodes x 20 updates each (see json); matter-only isospin swings 1.53-1.88 x its scale in su2 while the total moves only by the exact remainder term (0.04-0.12 of the matter scale in this low-amplitude regime A_psi = 64: remainder floor ~ A/A_psi^2). |
| G4 covariance | PASS | random local Q8 (su2), Z4 (u1), 96-element monomial group (su3) gauge fields, 2 seeds each, with 2-path gears and spring: F^T(Gamma s0) == Gamma F^T(s0) bit for bit (T = 30 / 30 / 15); Wilson plaquettes invariant. |
| G5 rewind + mirror | PASS | rewind exact; M F^T M F^T = id and M' F^T M' F^T = id (u1, su2, su3 with 2-path + spring); M' fixes the vacuum (M does not: 3Q-1 -> 3Q); ref + c2 (kappa = Q): joint mirror rhoL0 (ref.*) + M' (links) exact over 12 + 12 and fixes the joint vacuum; rewind and M exact. |
| G7 links frozen | PASS | Q = 4095 and 524289, ZQ8 and H: kappa = lam = 0 -> 0 base mismatches, 0 link deviations over 50 updates (dense random reference, amp 20); control kappa = lam = Q detects it within 2 updates (5096-5134 base mismatches). |
| G8 c2 exactness | PASS (exactness) | ZQ8 kappa = Q: Noether 810/810, rewind, M exact, LOCAL Q8 covariance bit-exact (2 random gauge fields). H: Noether 810/810, rewind, M, global i/j/k/-1 and local centre bit-exact; a local non-central map has no integer image (as the theorem says). DYNAMICS (report): the coarse kappa = Q links blow up from sparse amp-1 reference data + +-1 link noise: max bit length 1 -> 17404 (ZQ8) / 25859 (H) in 10 updates (doubly exponential: the cubic spring and the doubled couplings). |
| G6 spring-bounded norms | **FAIL (as pre-registered)** | strong drive A_psi = 256 = A (eps = 1) is far too strong for this regime: the relative link drive is 2 kappa A_psi^2/(D A) = 0.17 per update^2 against a radial w^2 = 0.083 lam: su2+P runs away (|U| > 4A) at t = 6 / 8 / 5 for lam = 1 / 2 / 0; lam = 4 stays finite to t = 2000 but its worst deviation is 1.61 (> 0.5); su3 runs away at t = 6 / 7 / 10 / 6 for lam = 1 / 2 / 4 / 0. Gauss sampled checks 0 failures in every arm. The eps-only scaling of S4-P3R does not transfer: their matter barely hopped (kappa A/D = 4e-5); here kappa A/D = 1/12. |
| D3 non-abelian witness | PASS | far corner after 2 updates, A_psi = 2^16: SU(2) same order (k-component) -3641, swapped order exactly 0 (j i + i j = 0); U(1) same = swapped = 3641; Wilson loop +A^4 vs -A^4 (flux pi) in SU(2), +A^4 in both U(1) configurations. |

## PRE-REGISTRATION G6b (written Tue Nov 10 09:41:24 UTC 2026, BEFORE the run; G6 above stands as FAILED)
Same arms and criterion as G6 (PASS iff worst |U|/(A sqrt dim) deviation < 0.5 for every lam >= 1 to t = 2000 and
0 sampled Gauss failures; lam = 0 control reported), with the drive calibrated to S4-P3R's drive/stiffness ratio
(~0.1/lam): A_psi = 64 (eps = 1/16, relative link drive ~0.01 per update^2), arms su2+P (L = 4) and su3 (L = 3),
lam in {1, 2, 4, 0}. G6c: the fine regime Q = 2^25 + 1, A = 4096, kappa = 4096, mass = Q + 3, 2-path kappa_P = 256,
d_P = 2^25 (P0 = 128), su2+P, L = 4, A_psi = 1000 (relative drive ~0.01), lam in {1, 2, 0}, same criterion.

## PRE-REGISTRATION G9 details + C1 exploratory (written Tue Nov 10 09:42:35 UTC 2026, BEFORE these runs)
- The binding rule (manager 09:28 and the 09:34 binding rules: q_lattice_violations(("ref.*",)) == [] for every shipped composed system)
  leaves kappa in {0, Q} for c2/c1, i.e. A = 1: the link register has the board's own granularity. The fine forms
  (kappa < Q) are NOT run (not shippable).
- G9 (report, no threshold): ref (Q = 4095, L = 4) + c2 ZQ8 kappa = Q, lam = Q and 2Q; seeds: one reference
  quantum (b = 1 on R00 at one node) and three quanta; 2000 updates or until a value exceeds 4000 bits; same seeds
  with kappa = lam = 0 as the frozen comparison. Reported: bit lengths of reference and link values over time.
- C1 (exploratory): ref + c1 port-weight register, kappa = Q (A = 1), lam = Q and 2Q: (i) vacuum fixed for 200
  updates (expected exact); (ii) weight pulse V~ = +1 on 3 entries of one link, reference at vacuum (decoupled at
  linear order: expected bounded oscillation of the weights, reference untouched); (iii) one reference quantum,
  dynamic weights vs frozen weights. ADOPTION RULE: c1 is recommended only if (ii) and (iii) stay bounded (no
  value above 64 bits) for 2000 updates; otherwise NOT adopted.
- ADDED before running (09:44:08 UTC, report only): G9b/C1b stronger excitation: reference data random in [-3, 3] on 10% of
  the reference gears (r on the Q-lattice), L = 4, Q = 4095, c2 ZQ8 kappa = Q lam = Q and c1 kappa = Q lam = Q,
  500 updates or until > 4000 bits; plus a bit-identity comparison of the reference sector with the frozen run for
  the single-quantum seeds of G9.
- ADDED before running (09:45:00 UTC, EXPLORATORY, NOT SHIPPED, DECLARED off the Q-lattice): fine c2 for comparison only
  (owner information): Q = 4095, kappa = 65 (not = 0 mod Q: no exact mirror fixes the L0 vacuum), H form m = 63
  (A = 31.5) lam = 1 and ZQ8 A = 63 lam = 1; same strong reference data as G9b; 500 updates or > 4000 bits.

## RESULTS, second batch (written Tue Nov 10 09:45:47 UTC 2026; runs 09:41:38-09:45:21 UTC)
| test | verdict | numbers |
|---|---|---|
| G6b spring, calibrated drive A_psi = 64 (A = 256) | **FAIL for su2+P at lam = 1, 2 (bounded but > 0.5); PASS otherwise** | su2+P: worst |U|/A deviation 1.08 / 0.82 / 0.478 for lam = 1 / 2 / 4, all bounded to t = 2000 (no runaway); lam = 0 runs away at t = 15. su3 (L = 3): 0.41 / 0.28 / 0.19 for lam = 1 / 2 / 4 (PASS), lam = 0 runaway t = 22. Sampled Gauss checks: 0 failures in every arm (3840-4860 checks per arm). Reading: with 2-path gears the P pull (2 c_U = 65536 against the spring's 2 lam A^2 = 131072 lam) halves the effective spring, so su2+P needs lam >= 4 for the strict 0.5 band. |
| G6c spring, fine regime A = 4096 (Q = 2^25+1), su2+P, A_psi = 1000 | PASS | worst deviation 0.41 (lam = 1), 0.27 (lam = 2) to t = 2000; lam = 0 runaway t = 19; Gauss sampled 0 failures (3840 each). |
| D1 isospin rotation/exchange (SU(2), fine regime) | PASS (demo) | (a) one link set to q = (2896,0,0,2896) ~ A exp(k pi/4): the transported isospin vector at the next node is (0, +1.5014e15, 0) vs (-1.5016e15, 0, 0) through the vacuum link: cos = 0.000, rotation axis -e3 (90 degrees, gauge-covariant transport). (b) two packets with orthogonal isospin (i and j), 60 updates: matter isospin swings 92 % of its scale and flows between the left/right packets and the links; the total vector moves 0.22 % and its change equals the summed remainder terms EXACTLY; Gauss 11520/11520; max |U|/A 1.20. |
| D2 colour flow (SU(3), fine regime, L = 3, 40 updates) | PASS (demo) | 9 generators (i lambda_1..7, i diag(1,1,-2), i*1): matter-only colour swings 12-55 % of its scale (lambda_8': 55 %), the U(1) part (i*1, carried by matter only) 0.2 %; the totals move 0.4-1.2 % and every change equals the summed remainder terms exactly; Gauss 9720/9720; link unitarity deviation 0.14. |
| G9 c2 (kappa = Q) single / three quanta | report | links never leave W = 0 in 2000 updates; the reference sector is bit-identical to the frozen run (500 updates checked) and even the link remainders stay at 3Q-1. Reason (exact): the link drive is b(x) b(x+e), and data that live on one space-time checkerboard class (all three seeds did) never have both ends of a link non-zero at the same update. |
| G9b c2 / C1b c1 (kappa = Q), generic data |b| <= 3 on 10 % of the reference gears | report: UNSTABLE | c2 blows up at t = 8 (> 4000 bits), c1 at t = 9; the frozen board stays at <= 8 bits for 500 updates. |
| C1 exploratory (port-weight register) | **NOT ADOPTED** | vacuum fixed (200 updates, exact); unit weight pulse bounded at lam = Q but blows up at t = 10 for lam = 2Q (cubic-spring CFL at the board's granularity); one-quantum data trivially stable (checkerboard); generic data blow up at t = 9 (C1b). Fails the pre-registered adoption rule. |
| G9c fine c2, EXPLORATORY, DECLARED off-lattice (kappa = 65, Q = 4095; not shipped) | report | H form (V- only, A = 31.5): survives to t ~ 250 (lam = 1) / 290 (lam = 2), then blows up; ZQ8 A = 63: blows up at t = 33; Noether identity exact in all (1920/1920 on the first 10 updates). |
Mechanism (DERIVED, consistent with all the above): today's board sits exactly at the stability edge (the uniform V+
mode has |eigenvalue| 6, i.e. cos w = 1; V- has max |eigenvalue| ~ 5.01 on a 9^3 k-grid). A dynamical link whose
norm fluctuates above the unitary value pushes such modes beyond |cos w| = 1 (exponential growth); integer links at
the board's own granularity (A = 1, forced by the binding Q-lattice rule) cannot stay unitary, and the cubic spring
itself is CFL-limited at |U| ~ 2. The V- only H form with headroom lives longer (gap ~1.0) but still grows.

## CENSUS (ARCH R3/R4/R6, binding items 1-7 of the manager's 09:34 binding rules; written Tue Nov 10 09:48:33 UTC 2026)
Computed by `observe.gauge.layer_census` (results/gauge/census.json), canonical parameters, monomials TARGETING the
named gears.
| block | monomials by degree (0/1/2/3) | a-read monomials | constants | max entries per row from ONE face (OD3 placement) | rank-4 (degree-3) monomials = spring only | physical support > one link |
|---|---|---|---|---|---|---|
| u1 (lam 0 / 2) | 0/20/36/0 ; 0/20/45/12 | 0 | 0 | 3 (1 rank-2 hop + 2 rank-3 through-link) | 0 ; 12 | 0 |
| u1 + 2-path | 0/104/108/0 ; 0/104/117/12 | 0 | 0 | 8 | 0 ; 12 | 120 (2-path terms) |
| su2 | 0/40/144/0 ; 0/40/165/48 | 0 | 0 | 5 | 0 ; 48 | 0 |
| su2 + 2-path | 0/208/432/0 ; 0/208/453/48 | 0 | 0 | 14 | 0 ; 48 | 384 (2-path terms) |
| su3 | 0/96/324/0 ; 0/132/927/1404 | 0 | 0 | 7 | 0 ; 1404 | 0 |
| su3 + 2-path | 0/852/2268/0 ; 0/888/2871/1404 | 0 | 0 | 16 | 0 ; 1404 | 2376 (2-path terms) |
| c2 ZQ8 links (lam 0 / Q) | 0/24/1152/0 ; 0/24/1197/192 | 0 | 0 | 48 (link row reads 48 bilinears b(x) b(x+e)) | 0 ; 192 | 0 |
| c2 ZQ8: rows of L0 | 0/288/2304/0 | 0 | 0 | 9 (the reference's own 1 rank-2 port + 8 rank-3 through-link entries) | 0 | 0 |
| c2 H links ; L0 rows | 0/12/1152/0 (lam 0), 0/12/1173/48 (lam Q) ; 0/288/2304/0 | 0 | 0 | 96 ; 9 | 0 or 48 ; 0 | 0 |
| c1 links ; L0 rows | 0/144/288/144 ; 0/288/288/0 | 0 | 0 | 1 ; 2 | 144 (spring) ; 0 | 0 |
- OD3: the reference's rank-2 ports keep ONE entry per row per face. The new rows (matter, links) and, under the
  DYNAMIC base links (G9-c, departs from AGENTS 5), the L0 rows take several entries from the SAME face neighbour,
  all of them rank-3 through-link entries (the link gear is stored at x or at x - e, i.e. on that same face link).
- OD4: the only degree-3 monomials (rank 4) are the spring's, verified by lam = 0 -> 0 degree-3 monomials in every
  block; the spring enters Phi with a MINUS sign and lam > 0.
- Deviation form, constant-free: `deviation_terms` asserts that the shifted potential has no linear term, so no
  constant input exists (T.has_constant is False in G1 for every block).
- Two-time (a) reads: NONE in any block (all b-only); no designated one-way term; every field sign is +1 (no sign_why
  needed).
- Physical supports wider than one link: only the 2-path coupling terms (P(x;k1,k2) U(x,k1) U(x+e_k1,k2) spans the
  plaquette x, x+e_k1, x+e_k1+e_k2); storage locality (B3) holds for every term.
- Reversors as DATA (Block.params["reversor"]; `observe.gauge.joint_mirror`): new b-only gears M' (fixes 3Q-1 for ODD
  Q; for even Q no remainder is R'-fixed, so no mirror-fixed vacuum exists); ref.* rhoL0 (exact because every c2/c1
  term into L0 is = 0 mod Q, validator `q_lattice=("ref.*",)`); the plain M is exact for every block but does not fix
  the vacuum. J/JR/JM are NOT used (the rank-3 couplings make the blocks J-even in part, not J-odd).
- No timing or spacelike claim is made by these layers.

## API for reviewers (read-only access to every state component)
- Builders (layers/): `build_gauge(group="su2"|"su3"|"u1", Q, A, kappa, mass, lam, use_P, kappa_P, c_P, beta, name)`,
  `build_su2/build_su3/build_u1(...)`; `build_c2(Q, kappa in {0, Q}, lam, algebra="ZQ8"|"H", ref="ref", name="c2")`;
  `build_c1_weights(Q, kappa in {0, Q}, lam)`. Algebra data: `layers.gauge.ALGEBRAS[group]` (structure constants,
  adjoint, unit, integer generators, integer gauge group); gear names: `layers.gauge.gear_names(group, use_P)`.
  Block.params carries Q, couplings, P0, c_U, X0 (vacuum values of the physical variables), r0, reversor.
- Initial data (prepare/gauge.py): `random_gauge_state`, `set_link` (physical link value), `set_matter`, `set_gears`.
- Read-only (observe/gauge.py): `GaugeView(tensor, block.params, name)` -> `.phys`, `.link_matrix`, `.link_norm2`,
  `.link_unitarity`, `.wilson`, `.charge(state, X, parts)`, `.remainder_term`, `.gauss_check(history)`,
  `.pieces(X)` (the generator T^X_x as data), `.gauge_map` (audit map); `C2View` likewise for ref + c2
  (`gauge_map_zq8`, `gauge_map_h`); `layer_census`; `joint_mirror`.
- Tests: `OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_gauge -v` (13.8 s;
  the long spring arms G6/G6b with GAUGE_LONG=1, about 20 s). Demos: `python -m
  research.metric_variant_v1.demos.gauge.run_demos [D1 D2 D3]`, `python -m
  research.metric_variant_v1.demos.gauge.links_stability`.

## PRE-REGISTRATION G6d (written Tue Nov 10 09:48:54 UTC 2026, before the run)
SU(3) WITH 2-path gears (canonical parameters, P0 = 32), L = 3, A_psi = 64, t = 2000, lam in {1, 2, 4, 0}; same
criterion as G6b (worst deviation < 0.5 for lam >= 1, 0 sampled Gauss failures; lam = 0 reported). Afterwards the
whole evidence set (G1-G8, G6/G6b/G6d, D1-D3, G9/C1) is re-run once on the final code.

## MANAGER RULINGS (received after the 09:46 interim) and the SPRING DEFAULT RULE (written Tue Nov 10 09:50:00 UTC 2026, BEFORE the selection run)
- G6 (pre-registered, A_psi = A) stays a recorded FAIL; G6b / G6c / G6d are re-registered variants, reported separately.
- c2 ships as an exact block, DEFAULT OFF (not part of any default composed system); c1 NOT ADOPTED (exploratory).
- SU(3) integer-exact covariance = the DECLARED 96-element monomial subgroup (entries +-1, +-i; det 1), NOT Delta(27)
  (whose omega phases are not in Z[i]); the colour Gauss law is the exact Noether identity.
SPRING DEFAULT RULE (selection run S1, after this paragraph): candidates for su2 WITH 2-path gears, L = 4:
  regime C (Q = 2^19+1, A = 256, kappa = 1024, mass = Q+3, kappa_P = 256, P0 = 32) with lam in {4, 8, 16} at the
  calibrated drive A_psi = 64; regime F (Q = 2^25+1, A = 4096, kappa = 4096, mass = Q+3, kappa_P = 256, P0 = 128)
  with lam in {2, 3, 4} at A_psi = 1000; seeds 51, 52, 53; 2000 updates each.
  A candidate QUALIFIES iff (a) its worst |U|/A deviation over all three seeds is <= 0.30 (margin >= 0.20 to the 0.5
  band), (b) 0 sampled Gauss failures (every 100th update pair), (c) the radial CFL margin 2 lam A^2 / D <= 2/3
  (cos w_r >= 1/3; this also keeps the cubic spring well inside its nonlinear CFL range for |U| <= 1.5 A).
  The shipped default = the qualifying candidate with the smallest worst deviation (tie: smaller lam); its regime is
  then the default regime for every gauge layer (ONE Q). su3 and u1 (with 2-path gears) get their lam by the same
  rule inside that regime (su3: L = 3, seeds 51-53, same lam candidates). If no candidate qualifies, NO spring default
  is shipped and that is reported.

## PRE-REGISTRATION M1: c2 instability mechanism map (written Tue Nov 10 09:50:47 UTC 2026, BEFORE the run; MECHANISM test, prescribed static links, not shipped)
Mechanism claim (DERIVED, to be tested): L0's uniform V+ mode has |eigenvalue| 6 (cos w = 1, the reference light at
k = 0); a link whose coupling operator rho(U) = sum_q U_q R_q has operator norm > 1 on a sector pushes modes past
|cos w| = 1 (exponential growth); unitary links (rho(U) a signed permutation: U = +-[q]) keep the operator norm <= 6
and L0 bounded, whatever their holonomy.
Setup: Q = 4095, L = 4, reference + a PRESCRIBED STATIC ZQ8 link block (link gears with u = D W only, so W never
changes; the L0 terms of c2 kept and DESIGNATED one-way "prescribed static link, mechanism test only"; q-lattice
validator on). Generic L0 data: |a|,|b| <= 3 on 10 % of the reference gears (seed 8), r on the Q-lattice; 1000
updates or until a reference value exceeds 64 bits. Configurations at the link (1,1,1)+x (others vacuum [1]):
  unitary: [1] (= frozen board), [i], [-1], -[1], a nontrivial-holonomy set ([i] on (1,1,1)+x, [j] on (2,1,1)+y,
  [k] on (1,2,1)+x, [-1] on (1,1,2)+z), cut 0 (contraction);
  non-unitary: [1]+[i] (V+ trivial character 2, V- sqrt2), [1]+[-1] (V+ 2, V- 0), [1]-[-1] (V+ 0, V- 2), 2[1], 3[1].
Prediction: every unitary configuration and the cut stay bounded (max bits within +3 of the frozen run over 1000
updates); every configuration with a V+ norm 2 or 3 blows up (the time reported); the V--only [1]-[-1] is reported
(V- has max |eigenvalue| ~5.01 < 6, so a single norm-2 link may or may not bind a growing mode).

## RESULTS M1 (written Tue Nov 10 09:51:51 UTC 2026; run 09:51:09-09:51:37 UTC; demos/gauge/M1_mechanism.json)
Prescribed static links (MECHANISM), Q = 4095, L = 4, generic L0 data (|b| <= 3 on 10 %), 1000 updates, cap 64 bits:
| link at (1,1,1)+x | operator norm of rho(U) (V+ trivial char / V-) | outcome |
|---|---|---|
| [1] (frozen board) | 1 / 1 | bounded, final 9 bits |
| [i], [-1], -[1] | 1 / 1 (signed permutations) | bounded (7 / 9 / 6 bits) |
| holonomy set [i], [j], [k], [-1] on four links (nontrivial plaquette holonomies) | 1 / 1 | bounded (9 bits) |
| cut 0 | 0 / 0 | bounded (6 bits) |
| [1]+[i] | 2 / sqrt2 | blows up at t = 405 |
| [1]+[-1] | 2 / 0 | blows up at t = 411 |
| 2[1] | 2 / 2 | blows up at t = 406 |
| 3[1] | 3 / 3 | blows up at t = 246 (faster: growth ~0.28 bits/update vs ~0.18 at norm 2) |
| [1]-[-1] | 0 / 2 (V- only) | bounded (6 bits) over 1000 updates |
The prediction holds as registered: unitary links of any holonomy and the cut keep L0 bounded (within the frozen
run's 9 bits); every link with V+ norm > 1 blows up, faster for a larger excess; a V--only excess of 2 on a single link
does not (V- has max |eigenvalue| ~5.01 < 6 for the uniform coupling, so one strong V- link binds no growing mode in
1000 updates). The links stayed exactly static in every run (prescribed field); reciprocity: 2304 designated terms,
checker OK. This supports the DERIVED mechanism: the dynamical c2 instability comes from link norms leaving the
unitary set on the V+ sector, where L0's uniform mode sits at |eigenvalue| 6 (cos w = 1).

## RESULTS S1 + the shipped SPRING DEFAULT (written Tue Nov 10 09:53:17 UTC 2026; S1 ran 09:50:18-09:52:58 UTC; results/gauge/S1_spring_default.json)
Worst |U|/(A sqrt dim) deviation over seeds 51-53 (2000 updates each, 0 Gauss failures in every arm):
| layer (with 2-path) | regime C (A = 256, A_psi = 64): lam 4 / 8 / 16 | regime F (A = 4096, A_psi = 1000): lam 2 / 3 / 4 |
|---|---|---|
| su2 | 0.536 / 0.350 / runaway (t ~ 1440-1590) | 0.315 / **0.122** / **0.074** |
| su3 (L = 3) | **0.216** / **0.182** / runaway (t ~ 1650-1960) | **0.138** / **0.045** / **0.036** |
| u1 | 0.570 / 0.365 / 0.457 | **0.165** / **0.080** / **0.064** |
(bold = qualifies: worst <= 0.30, no runaway, 0 Gauss failures, 2 lam A^2/D <= 2/3.)
By the rule: su2 + 2-path qualifies only in regime F, lam = 3 (0.122) or lam = 4 (0.074); the smallest worst is
lam = 4, so the SHIPPED DEFAULT is regime F (Q = 2^25+1, A = 4096, kappa = 4096, mass = Q+3, kappa_P = 256, c_P = 0,
beta = D - 2^25, P0 = 128, c_U = 131072) with lam = 4 for su2; inside regime F the same rule gives lam = 4 for su3
(0.036) and u1 (0.064). WHY lam = 4 IS SAFE: (1) margin >= 0.43 to the 0.5 band in all three layers over three
seeds (vs 0.478 for the marginal G6b arm); (2) the radial CFL at the default is 2 lam A^2/D = 2/3 (cos w_r = 1/3), and
the cubic spring's own nonlinear CFL (radial stiffness lam (3x^2 - 1) A^2 <= 2D at |U| = xA) only fails beyond a
53 % radial excursion, seven times the observed worst (7 %); the coarse-regime runaways at the same ratio (C, lam = 16)
are exactly this onset, reached there because the deviations were already 0.33-0.5. (3) LIMIT: the default is
qualified for drives up to the calibrated level (relative link drive ~0.01 per update^2); the strong-drive G6 FAIL
stands. lam = 3 (worst 0.12, onset 73 %) is the fallback if more CFL headroom is wanted.

## PRE-REGISTRATION G10 + FINAL RE-RUN (written Tue Nov 10 09:53:40 UTC 2026, BEFORE the runs)
G10 DEFAULT SYSTEM: compose(ref, su2, su3, u1) with the shipped defaults (regime F, lam = 4, 2-path gears), validator
q_lattice=("ref.*",): ONE Q (2^25+1), reciprocal, no c2/c1 gear, no designated term; vacuum fixed for 20 updates;
L = 3, random data in every layer (A_psi = 1000) + dense random reference data (amp 20): 10 updates with the Noether
identity exact for all 13 generators (0 failures), rewind exact, joint mirror (rhoL0 on ref.*, M' elsewhere) exact and
vacuum-fixing, simultaneous local covariance (Q8 x Delta96-declared x Z4 gauge fields) bit-exact, and the reference
sector equal to the reference-alone run (frozen_equivalence with the default blocks as the extra layers).
FINAL RE-RUN on the final code: tests G1-G5, G7, G8, G10; GAUGE_LONG arms G6 (stays FAIL), G6b/G6c/G6d; S1 is not
re-run (its rows are the selection evidence); demos D1-D3, G9/C1 stability, M1. Verdicts must reproduce.

## c2 DESIGN FACTS for the owner (manager ruling item 2; written Tue Nov 10 09:55:03 UTC 2026). c2 ships DEFAULT OFF.
(i) MECHANISM [DERIVED]. With +++ ports, every W_d is a positive permutation matrix, so on the uniform vector
    (all 48 labels equal, in V+) sum_d W_d e^{ik.e_d} = 6 at k = 0: L0's uniform mode has |eigenvalue| 6, i.e.
    cos w = 1 exactly (the reference light at k = 0 sits ON the stability edge). With a dynamical link the coupling
    across (x, x+e_d) becomes b(x)^T W_d rho(U) b(x+e_d). If rho(U) is a signed permutation (U = +-[q]) the operator
    norm stays 6 and L0 stays bounded whatever the holonomy; any non-unitary value with norm > 1 on V+ pushes modes
    past |cos w| = 1 and they grow exponentially. Integer links cannot move between unit values without passing
    through non-unit ones, and under the binding Q-lattice rule (kappa = Q, A = 1) one unit of W is a full reference
    coupling. V- has a spectral gap (max |eigenvalue| ~5.01 on a 9^3 k-grid), which is why a V--only excess survives
    longer.
(ii) NUMERIC MAP (M1, prescribed static links; table in RESULTS M1 above): unitary links of any holonomy and the cut
    keep L0 bounded (<= the frozen run's bits for 1000 updates); one link with V+ norm 2 blows up at t ~ 405-411, norm
    3 at t = 246; a V--only norm-2 link stays bounded for 1000 updates. Dynamically (G9b): generic |b| <= 3 data blow up
    at t = 8 (c2) and t = 9 (c1); data on ONE space-time checkerboard class never drive the links at all (b(x) b(x+e) = 0
    identically), so their reference sector is bit-identical to today's board (500 updates checked).
(iii) THEOREM (ZQ8 = 8 gears). Suppose a local symmetry acts at each node by integer maps on the 48 L0 gears that
    commute with Rule3 (signed permutations of the labels, R' on negated remainders) and reduces to a symmetry of
    today's board when it is constant in space. Then the link register needs at least 8 independent integers per link,
    and Z[Q8] (8 gears) suffices.
    Proof. (1) A constant map S must commute with every port matrix: S W_d = W_d S. The underlying permutation |S| then
    commutes with the positive permutations W_d (+++), so |S| lies in the centralizer of the port group, which is
    exactly {R_q : q in Q8} (exhaustive, M2_commutant48: transitive group of order 196608, centralizer order 8). Write
    S = Diag(s) R_q. Then Diag(s) commutes with every W_d, so s(g) = s(ports[d][g]) for all d and g; the port group is
    transitive, so s is constant: S = +-R_q. (2) Locally S(x) = +-R_{q(x)}. The link (x, d) carries
    b(x)^T W_d rho(U) b(x+e_d), and the vacuum is rho = Id. Covariance needs the set of attainable rho(U) to be closed
    under rho -> S(x)^T rho S(x+e_d) = +-R_{q(x)}^{-1} rho R_{q(x+e)}. From rho = Id this generates every R_p, p in
    Q8 (p = q(x)^{-1} q(x+e)). (3) The eight R_p have pairwise disjoint supports ((R_p)_{g, gp} = 1), so they are
    linearly independent. An integer-linear link realisation rho(U) = sum_c U_c M_c therefore needs span{M_c} to
    contain 8 independent matrices: at least 8 link integers. A 4-integer quaternion link spans only 4 (on V- the
    pairs R_p, R_{-p} coincide up to sign; on V+ they do not, because R_{-1} = +1 there). (4) rho(U) = sum_q U_q R_q
    on Z[Q8] is a ring homomorphism (R_p R_q = R_pq). Local Q8 then acts by PERMUTING the 8 components
    (q -> k q k'^-1) plus an integer affine shift in deviation form: bit-exact (G8). QED.
    Consequence: the spec's 4-gear quaternion link (H form, V- only) keeps global Q8, the local centre Z2 and the
    continuous local SU(2) on V- as an exact Noether identity, but cannot carry bit-exact local Q8 on the 48 labels.

## PRE-REGISTRATION S2: the default family at other Q (written Tue Nov 10 09:56:09 UTC 2026, BEFORE the run)
Manager heads-up (after the rulings): B1-EM imports build_gauge(group="u1") read-only at Q = 2^29+1. The build_gauge API stays
unchanged. A helper default_regime(Q) states the shipped default family for Q = 2^(2n+1)+1 (odd), which keeps every
dimensionless ratio of regime F (n = 12): A = 2^n, kappa = 2^n (kappa A = (Q-1)/2), mass = Q+3, lam = 4
(2 lam A^2/D = 2/3 - O(1/Q)), 2-path kappa_P = 256, c_P = 0, beta = 6Q - 2^(2n+1) (d_P = 2^(2n+1), P0 = 128,
c_U = 131072). S2 verifies it at Q = 2^29+1 (n = 14, A = 16384): u1 and su2 with 2-path gears, L = 4, seeds 51-53,
2000 updates, drive scaled with A (A_psi = 4000, the same relative link drive ~0.01 per update^2 as S1's regime F).
Same criterion as the spring default rule: worst deviation <= 0.30, no runaway, 0 sampled Gauss failures.

## RESULTS S2 (written Tue Nov 10 09:56:39 UTC 2026; run 09:56:25-09:56:31 UTC; results/gauge/S2_default_family_Q2p29.json)
Q = 2^29+1, default family (A = kappa = 16384, mass = Q+3, lam = 4, kappa_P = 256, c_P = 0, beta = 6Q - 2^29, P0 = 128),
A_psi = 4000, 3 seeds x 2000 updates, int64 path throughout: u1 worst 0.055 / 0.063 / 0.053, su2 0.074 / 0.075 / 0.074
(regime F at 2^25+1 gave 0.064 / 0.074); 0 runaway, 0 Gauss failures (1280 / 3840 sampled checks per run). The
default family QUALIFIES at Q = 2^29+1 with the same margin: the dynamics depends only on the dimensionless ratios.
For B1-EM (u1 at Q = 2^29+1): `build_default("u1", Q=(1<<29)+1)` or build_gauge(group="u1", Q=536870913, A=16384,
kappa=16384, mass=536870916, lam=4, use_P=True, kappa_P=256, c_P=0, beta=2684354566) -> P0 = 128, c_U = 131072.

## FINAL RE-RUN on the final code (written Tue Nov 10 09:57:55 UTC 2026; runs 09:54:42-09:57:27 UTC)
- Quick suite (`python -m unittest research.metric_variant_v1.tests.test_gauge -v`): G1, G2, G3, G4, G5, G7, G8, G10
  OK (16.1 s, run twice: 09:54:42 and 09:57:11, the second after the last code edits: default_regime and the census
  in G1). G10: default system ref + su2 + su3 + u1 (Q = 2^25+1, 276 gear types, 6393 monomials), reciprocal, 0
  designated, 0 q-lattice violations, no c2/c1 gear, vacuum fixed, Noether 810 + 2430 + 270 checks with 0 failures,
  rewind, joint mirror exact and vacuum-fixing, simultaneous local covariance (Q8, the declared 96-element SU(3)
  subgroup, Z4) bit-exact, reference sector unchanged by the gauge layers (frozen_equivalence 0/0).
- GAUGE_LONG: G6 FAILS again exactly as recorded (stays a FAIL); G6b fails again at su2+P lam = 1 (1.08) and lam = 2
  (0.82), with identical numbers; G6c PASS (0.41 / 0.27); G6d (su3 WITH 2-path, regime C, A_psi = 64) PASS: worst
  0.38 / 0.28 / 0.21 for lam = 1 / 2 / 4, lam = 0 runaway at t = 17; 0 sampled Gauss failures in every arm.
- Demos D1-D3, G9, C1, G9b/C1b/G9c (now in demos/gauge/links_stability.py -> G9b_C1b_G9c_strong.json) and M1
  reproduced their numbers exactly (G9b 8, C1b 9, G9c H 250 / 291, ZQ8 33 / 33; M1 405 / 411 / bounded / 406 / 246).

## FINAL SUMMARY TABLE
| item | verdict |
|---|---|
| SU(2) layer: quaternion doublets + quaternion links (4/link) + 2-path + OD4 spring | exact: Noether/Gauss 0 failures, local Q8 bit-exact, rewind, M and M' mirrors, vacuum |
| SU(3) layer: Z[i]^3 triplets + integer complex 3x3 links (18/link) + 2-path + spring | exact: Noether for i lambda_1..7, i diag(1,1,-2), i*1 (0 failures); DECLARED 96-element monomial subgroup bit-exact (not Delta(27)); colour flow demo PASS |
| compact U(1): Gaussian links (2/link) + 2-path + spring | exact: Gauss 0 failures, local Z4 bit-exact; default stated for B1-EM at Q = 2^29+1 (S2) |
| non-abelian witness D3 | PASS (swapped order -> exactly 0; U(1) unchanged) |
| isospin rotation / exchange D1 | PASS |
| spring-bounded norms | G6 FAIL (recorded); G6b su2+P lam 1, 2 FAIL (bounded, > 0.5), others PASS; G6c, G6d PASS; shipped default regime F lam = 4 by the pre-registered rule (worst 0.036-0.075, S1 + S2) |
| c2 dynamic base links (ZQ8, 8 gears; H, 4 gears) | exact (vacuum, frozen control 0/0, reciprocity, q-lattice, Noether, local Q8 (ZQ8) / global Q8 + local centre (H), rewind, M, joint mirror); DEFAULT OFF; dynamically UNSTABLE for generic excited data (owner-level fact; mechanism DERIVED + M1 map) |
| c1 frame register (port weights, 48/link) | NOT ADOPTED (exploratory) |
Designations: NONE in any shipped block (all force terms gradients of one potential, all field signs +1, no a-reads).
Test-only designations: M1's prescribed static link block (2304 L0 terms, "prescribed static link, mechanism test
only"). Declared off-lattice exploratory runs: G9c only (kappa = 65), not shipped.
