# NOTES_em — stage 1, MATTER + ELECTROMAGNETISM layers (builder B1-EM)

All stamps are `date -u`. Pre-registrations are written BEFORE the corresponding run; results are appended below them,
never edited into them. Exact integers everywhere in the dynamics; floats only in initial-data preparation and derived
observables. No git. Nothing under `universe24/` or `core/` is touched. Files of this builder:
`layers/matter.py`, `layers/em.py`, `prepare/em.py`, `observe/em.py`, `tests/test_em.py`, `demos/em/`, this file.

## 0. Design as built (written Tue Nov 10 09:31:50 UTC 2026; code written 09:24–09:31, smoke-built only: tensor
construction, census and the reciprocity checker were called once at 09:29 to see that the blocks compose; no
dynamics run yet)

ONE divisor D = 6Q for every gear; ODD Q; every new gear's vacuum is (0, 0, 3Q − 1) (fixed by the parity-preserving
negation remainder map R'(r) = D − 2 − r (even r) / D − r (odd r), which the C map uses). Deviation form: every term
targeting a new gear contains a factor of a new gear, so the vacuum is a fixed point and the reference sector is
untouched (no term of mine targets a reference gear).

MATTER (`layers/matter.py`), 16 gears X0..X7, Y0..Y7 (the pair) or X0..X7 (one 8-block), label official:
  u(x) = hop Σ_d [P_d b(x − e_d) + P_dᵀ b(x + e_d)] + (mass + 6 wilson) W0 b(x) − wilson Σ_d W0 [b(x + e_d) + b(x − e_d)]
  P_d = 1₂ ⊗ L_d ⊗ σ_z, W0 = 1₂ ⊗ 1₄ ⊗ σ_x, J = 1₂ ⊗ R_i ⊗ 1₂, J' = ε ⊗ 1₈, V = JJ', K = 1₂ ⊗ R_j ⊗ 1₂, C = diag(1₈, −1₈).
  Reciprocal: u = ∂Ψ/∂b, Ψ = Σ_x Σ_d b(x+e_d)ᵀ H_d b(x) + (mass/2 + 3 wilson) Σ bᵀW0 b, H_d = hop P_d − wilson W0.
  OD3: a matter row reads ≤ 2 gears from one face neighbour (P_dᵀ entry + Wilson W0 entry).
EM (`layers/em.py`), gears A_x, A_y, A_z (link gears, Yee axes 0, 1, 2) and Phi (node), label audit (OD1):
  u_{A_d} = (Q − 1) Σ_6 A_d.b + 6 A_d.b + σ b(x+e_d)ᵀ J'(hs P_d − ws W0) b(x)      [(hs, ws) = (hop, wilson)/g, g = gcd]
  u_Phi   = 3Q [2 Phi.b − div A.b + div A.a]        (K_Phi ≡ 0 mod D: rounding-free; remainder constant)
  u_matter += g_phi (3 Phi.b − Phi.a − div A.b + div A.a) V b + g_A Σ_d (A_d.b(x) + A_d.b(x − e_d)) P_d J' b
  a-read graph A → Phi → matter (acyclic; staged inverse A, Phi, matter).
  Gauge-covariant ratio g_A/g_phi = hop/Q; physical φ = Phi/3 (c² = 1/3; with the headroom stencil strictly
  Phi·(Q−1)/(3Q)). Coupling per unit Phi: δλ = ±2 g_phi Phi (static), δE = 2 g_phi Phi/(D cos E); per unit A_d:
  δk_d = g_A A_d / hop (small k).
MECHANISM blocks (labelled, designated one-way, never evidence): `build_static_lapse_mechanism` (a static marginal gear
N read by the matter's mass entries), `build_current_driver` (a static or oscillating driver gear S feeding one A_d
source; prescribed line/dipole currents).

### Derivation of the exact identities (THEOREM-level algebra; checked numerically below)
Step: D(X(t+1) + X(t−1)) = 2u(t) + r(t) − r(t+1) for every gear.
* Continuity. ρ_x(t) := D b_x(t−1)ᵀJ' b_x(t). ρ(t+1) − ρ(t) = b(t)ᵀJ' D(b(t+1) + b(t−1)) = 2 bᵀJ'u + R(t),
  R(t) := b(t)ᵀJ'(r(t) − r(t+1)). Every on-site coupling matrix S (W0, V, P_dJ', 1) is symmetric and commutes with J',
  so bᵀJ'S b = 0. The link part gives 2 b_xᵀJ'u_x = −Σ_d [j_d(x) − j_d(x − e_d)], j_d(y) := 2 b(y+e_d)ᵀ J' H_d b(y).
  Hence ρ(t+1) − ρ(t) + div j(t) = R(t) EXACTLY, with the A-free hopping current (no diamagnetic term).
* Lorenz. Phi(t+1) + Phi(t−1) = 2Phi(t) − div A(t) + div A(t−1) exactly (K ≡ 0 mod D, 0 ≤ r < D), so
  C(t) := Phi(t+1) − Phi(t) + div A(t) is constant at every node. As a state function: C(S_t) = Phi.b − Phi.a + div A.a.
* Dressed Gauss. From the A equation, D·D_t²A = 2(Q−1)ΔA + 2σ s + r_A(t) − r_A(t+1) (s_d = j_d/(2g)); with
  div A(t) = C − (Phi(t+1) − Phi(t)): define
  Y_g(t) := g D [Phi(t+1) − 2Phi(t) + Phi(t−1)] − 2g(Q−1) ΔPhi(t) − σ ρ(t) − g div r_A(t). Then
  Y_g(t+1) − Y_g(t) = −σ R(t) − 2g(Q−1) ΔC   EXACTLY (any data; ΔC = 0 for legal data with C ≡ 0).
  With C ≡ 0: Y_g = g[6Q div E + 2ΔPhi] − σρ − g div r_A, E := −∇⁺(Phi/3) − (A(t) − A(t−1)): Gauss's law with the
  field remainders r_A (dressed) and the matter remainders R (accumulated); static: −ΔPhi = σρ/(2g(Q−1)).
* Charge Noether: summing continuity over the torus, Σρ(t+1) − Σρ(t) = ΣR(t).

### §R Reciprocity: why every E1 cross entry is designated one-way (finding; written 09:31 before any run)
`check_reciprocity` demands u_t = s_t ∂Ψ/∂b_t for ONE potential. In E1 this is impossible at ANY finite rank while
keeping exact continuity:
1. The source must be the matter's exactly conserved current (else Lorenz + accumulator give a drifting Gauss law).
   For matter whose A-coupling is on-site and J'-commuting, that current is the A-free LINK bilinear j_d (above).
2. The literal ∂Ψ/∂b partner of a link source σ A_d(x) b(x+e)ᵀM_d b(x) is the linear PEIERLS action. With it, the
   matter's exact current gains σ A_d b(x+e)ᵀJ'M_d b(x) (degree 3 = rank 4) — the diamagnetic term (Study 4 D4:
   57,718/58,000 failures without it). Adding it to the source requires an A² term in Ψ, which changes the current at
   O(A²), etc.: the expansion of e^{iθ} never closes at finite rank (only compact link gears close it).
3. The literal partner of the on-site α·A action is an on-site current Σ bᵀP_dJ'b at the two link ends, which is not
   conserved by the matter dynamics.
4. Phi is a slaved accumulator: the partner of the matter's φ_c·V read would be a direct ρ-source of Phi, which breaks
   C ≡ 0; the accumulator's own A reads are a first-order-in-time relation (partner: ∇Phi in the A equation).
So E1's source/action pairs are transposes only in the CONTINUUM (b(x+e)ᵀJ'P_d b(x) → bᵀP_dJ'b). Newton III needs
only a species-independent source/action ratio (S4-M CF-1), which E1 has (C is an exact symmetry). The cross entries
are therefore DESIGNATED with this justification, and two CONTROLS are offered: vector="peierls" (the literal transpose
of the source: reciprocal, exactness lost) and blind=c (a charge-blind action without source: Newton III broken).

## 1. PRE-REGISTRATION of the tests (tests/test_em.py), written Tue Nov 10 09:31:50 UTC 2026, BEFORE any run
Parameters unless stated: Q = 2²⁹ + 1 = 536870913 (odd, ≡ 1 mod 4), hop = (Q − 1)/4 = 2²⁷ (hop/D = 1/24 − O(1/Q)),
mass = 3Q (mass/D = 1/2), wilson = 0; (g_phi, g_A, σ) = (4, 1, 2¹¹) ≙ Study-4 G = 1 (S4: PM = 2³⁷, PF = 2¹⁰, dd = 4,
hn = 1), (4, 1, 2¹⁴) ≙ G = 8. Every verdict is EXACT (integer equality, 0 failures) unless a tolerance is given.
- EM-T1 algebra: every entry of `check_algebra()` True (J, J' commuting complex structures, V and P_dJ' symmetric
  signed permutations commuting with J and J', K anticommutes with J, K² = −1, C flips J').
- EM-T2 structure: rank 3; stages exactly (A_x, A_y, A_z) → (Phi) → (16 matter); every Phi coefficient ≡ 0 mod 3Q
  (rounding-free); every matter row reads ≤ 2 distinct matter gears per face neighbour (OD3; checked with wilson = 1
  too); deviation form (every term targeting a new gear has a new-gear factor); support_violations() = exactly the
  3 × 6 neighbour entries of the A stencil (design fact: the link-field light stencil couples parallel links).
- EM-T3 reciprocity: check_reciprocity(compose(matter, em)) ok; the designated monomials are exactly the A sources,
  the matter ← Phi.b and matter ← A.b reads, and the Phi ← A.b accumulator reads; free matter alone passes with 0
  designations. Controls: (a) the same tensor with designations stripped FAILS and lists those monomials; (b) the
  Peierls control's vector block is reciprocal (no violation among its matter ← A.b·b(x±e) entries and A sources);
  (c) the blind control's term is flagged when its designation is stripped.
- EM-T4 vacuum: (i) F(vac) = vac for matter + em (+ the lapse and driver mechanism blocks), L = 4, 20 updates;
  (ii) frozen_equivalence(reference(Q), matter + em) from a random reference state (L = 4, 20 updates): 0 base
  mismatches, 0 new-gear deviations.
- EM-T5 exact identities, dynamical matter: (a) L = 6, moving pair (particle kc = +0.4 x̂ at (1,3,3) and antiparticle
  kc = −0.4 x̂ at (4,3,3), width 1.3), prepared Poisson Phi (static dressed Gauss), A = 0, T = 60, amplitudes 2¹², 2¹⁶,
  2²⁰, σ = 2¹⁴: continuity, Lorenz C ≡ 0, dressed Gauss step identity, global Noether: 0 failures at every node and
  update. Reported (no pass mark, expected ~1/A): the undressed drift max|Y_g(t) − Y_g(0)| / max|σρ|.
  (b) ANY data: L = 4, random a, b ∈ [−2²⁰, 2²⁰] on every new gear, random remainders, wilson = 3, T = 30: continuity
  and the Gauss step identity (with its ΔC term) 0 failures; C(S_{t+1}) = C(S_t) at every node.
  (c) negative controls: the Peierls control board (same data as (a), 2¹⁶) FAILS continuity with the free current;
  dropping R or r_A from the identities makes them fail.
- EM-T6 rewind: every run of EM-T5 rewound T steps returns the initial state exactly.
- EM-T7 reversor X (3-D): L = 8, pair kc = ±0.4 x̂, width 1.3, amp 2¹⁶, random matter and field remainders, prepared
  Phi, σ = 2¹¹ (G = 1), T = 30: X F X F (S_t) ∈ {S_t, N(S_t)} (N = global matter negation, the Kramers sign) at the
  10 states t = 0, 3, …, 27; X F³⁰ X F³⁰ (S_0) ∈ {S_0, N(S_0)}; the mirrored run's matter clicks (official rule) equal
  the reversed original's under the K channel map: identical click flags, |ell| equal, 0 mismatches; my X equals the
  X built from core/reversors.py on every state used. Negative controls: the plain per-gear M, and X with the
  un-staggered Phi map (a, b, r) ↦ (−b, −a, r) both FAIL.
- EM-T8 C symmetry: F∘C = C∘F bit-exactly on 10 random states (L = 3 and 4; random values up to 2²⁰, random
  remainders); ρ ↦ −ρ and j ↦ −j exactly; C(vac) = vac (odd Q, r0 = 3Q − 1).
- EM-T9 Bloch (exact algebra + float eigenvalues): in the sector J = +i a uniform Phi shifts the two charge sectors
  by opposite equal amounts (|sum| ≤ 1e-9 relative); the identity coupling shifts them equally; the k-shift of a
  uniform A_x equals ±g_A A/hop to 1e-3 at small k; antimatter: the C-image's shifts are φ-opposite, lapse-equal.

## 2. PRE-REGISTRATION of the demos (demos/em/), written Tue Nov 10 09:31:50 UTC 2026, BEFORE any run
Every demo rewinds EXACTLY (T forward + T inverse = the initial state); prepared states satisfy C = 0.
- EM-D1 Coulomb, fully dynamical two-body (both packets source and feel), L = 32, amp 2¹⁴, width 2, σ = 2¹⁴ (G = 8),
  prepared static Phi of the total ρ, T = 150: (+,−) at r = 8 and 12 (species projection Π±); (+,+) at r = 8 and
  (−,−) at r = 8 (spin-separated packets, as S4-P run6). Prediction: a1 = ⟨E''⟩·F1, F1 = −s1·(2 g_phi/(D⟨cos E⟩))·
  ⟨|ρ1| ∂_x Phi_2⟩ (Phi_2 the torus potential of packet 2 in the E1 normalisation). PASS: signs exact (unlike attract,
  like repel); meas/pred ∈ [0.90, 1.05]; Newton III a2/a1 ∈ [−1.025, −0.975].
- EM-D2 1/r² with a PREPARED STATIC field and a SHORT window: L = 40, a ball (radius 2) of charge with its prepared
  torus Phi (A = 0, σ = 0: probes are TEST charges, so Phi is bit-static, checked at every update), ONE probe per board
  (amp 2¹⁴, width 2.5) at r = 8, 10, 12, 14 on +x, both charges; T = 40 (spreading σ(T)/σ0 reported). PASS: signs
  exact; |a(−)/a(+) + 1| ≤ 0.03; a/a_pred ∈ [0.85, 1.15]; slope of log|a| over the stations within ±0.15 of the slope of
  log|⟨∂_x Phi_torus⟩_ρ|; Phi bit-static.
- EM-D3 NON-CIRCULAR: L = 32, T = 60, hop = Q (hop/D = 1/6), mass = (3Q+1)/2, (g_phi, g_A, σ) = (1, 1, 2¹³) (≙ S4 G = 4,
  dd = 1), neutral seed: particle (kc = +0.6 x̂) and antiparticle (kc = −0.6 x̂) at the same place, Phi = A = 0; control
  with g_phi = g_A = σ = 0. PASS: relative L2 of φ_c/2 to the torus Poisson potential of ρ(t) (r < 6) ≤ 0.15 at
  t = 50–60; separation(coupled) < separation(control) at t = 60; C ≡ 0.
- EM-D4 dipole radiation (MECHANISM: oscillating driver S on the link (c, c + e_z), κ = round(D cos 0.4)), pure field
  (no matter), Q = 1025, L = 48, T = 70: Lorenz C ≡ 0 (0 failures); |E_z| ∝ r^p on the x axis, p ∈ [−1.05, −0.95]
  (r = 10–18, amplitude over the last 20 updates); other transverse ≤ 5 %; longitudinal/transverse decreasing with
  r = 6 → 10, ≤ 0.12 at r = 6 and ≤ 0.08 at r = 10 (φ = Phi/3), the φ = Phi control ≥ 2× larger; fronts (half-peak
  arrival, interpolated): [111] within 1.5 % of c_Q, [100] in [0.56, 0.61]; 1/10-peak fronts reported (S4 style).
  y-dipole: the second polarization (|E_y| on the x axis equals |E_z| of the z-dipole to 2 %). Q = 5 board (L = 32):
  [111] front within 3 % of c_5 = 0.5164.
- EM-D5 magnetism (MECHANISM: static antiparallel line currents along y at x = 8 and 24, z = 16, by static drivers),
  L = 32, T = 60, hop = Q, mass = 3Q, probe at x = 14 moving ±y (k = ±0.4), particle and antiparticle, g_A coupling on
  and a g = 0 control (subtracted). PASS: a(anti)/a(part) ∈ [−1.10, −0.90]; a(−v)/a(+v) ∈ [−1.10, −0.90]; parallel
  currents attract; a/(E''_xx q_A v_y ⟨∂_x A_y⟩) ∈ [0.85, 1.15]; Phi ≡ 0 exactly.
- EM-D6 click-space charge: L = 10, T = 60, pair (+ at (2,5,5), − at (7,5,5)), amp 2¹⁶, width 1.5, σ = 2¹¹:
  q_click/Q' per species = Σ ell(t)ᵀJ'ell(t+1) / Σρ' over the species projection. PASS: each ∈ [0.95, 1.10] with the
  species sign (flips with C); relative std ≤ 1e-3. (S4: 1.0176, std 3e-5.)
- EM-D7 ONE BOARD, TWO FORCES (MECHANISM, prescribed static fields, as S4-P PR-21): L = 24, T = 200, amp 2¹⁴, width 2;
  particle and C-image antiparticle at rest at (0, L/4, L/2) and (0, 3L/4, L/2). Gravity: static lapse gear N(x) =
  rint(0.002 D sin(2πx/L)) on the mass (coupling 1). EM: static Phi(x) = rint(D/8000 · sin(2πx/L)) with σ = 0
  (g_phi = 4). PASS: gravity a_anti/a_part ∈ [0.999, 1.001]; EM ∈ [−1.01, −0.99]; click/event (species-projected
  size-Wronskian centroid acceleration / event) ∈ [0.995, 1.005] for all four readings.
- EM-D8 Newton-III control (S4-P R17): EM-D1 (+,−) r = 8 with blind = 2 (a charge-blind action c·Phi.b·b = 25 % of
  the E1 scalar coupling 2 g_phi Phi V, as S4-P PR-30; no source): reported a2/a1 (expected to depart from −1 by
  ≫ 2.5 %; S4: −1.586). [blind value corrected from 64 to 2 at 09:33 UTC, before any run]

### AMENDMENT A1 (written Tue Nov 10 09:34:10 UTC 2026, BEFORE any run) — keep the coupling physical in EM-T5
Reason: σ·amp² sets the coupling strength; at amp = 2²⁰ with σ = 2¹⁴ the field would exceed D/g_phi and the matter
would turn unstable (doubly exponential growth, as the T0.10 control), which an identity test does not need.
- EM-T5(a): σ = 2¹⁴·(2¹⁴/amp)² (constant σ·amp², ≙ G = 8 at every amplitude): σ = 2¹⁸, 2¹⁰, 2² for amp = 2¹², 2¹⁶, 2²⁰.
- EM-T5(b): random a, b ∈ [−2¹⁰, 2¹⁰] (was 2²⁰), wilson = 3, σ = 2¹¹, T = 30; every other item unchanged.

### AMENDMENT A2 (written Tue Nov 10 09:37:09 UTC 2026, BEFORE any run) — manager's binding conditions (reversor as data, fixed vacuum)
- The DECLARED reversor is X = (K∘M′ on matter, M′ on A_d, Phi ↦ (−Phi_next, −Phi.b, r)), M′ = (b, a, R′(r)): it
  fixes the joint vacuum (0, 0, 3Q − 1) for ODD Q (even Q has no R′-fixed remainder). Declared as data in
  build_matter(...).params["reversor"] and build_em(...).params["reversor"]; central element X² = Jp on the matter.
- EM-T7 now runs three cases (each with every EM-T7 criterion): (wilson 0, M′), (wilson 0, M = S4-P's D − 1 − r
  convention; central J; the vacuum-fixed criterion does not apply), (wilson 2, M′); plus X(vac) = vac for M′; plus the
  FREE matter (wilson 2) Kramers reversor K∘M′: reversor_check (core) X F⁴⁰ X F⁴⁰ = id or Jp on a random L = 4 state
  (|values| < 2³⁰), and K∘M′(vac) = vac.

## RESULTS so far and AMENDMENT A3
(written Tue Nov 10 09:42:36 UTC 2026)
- First test run started 09:37:09: EM-T8 PASS, EM-T5a/EM-T6 PASS (numbers in §3 below, final run), EM-T9 FAIL:
  the PRE-REGISTERED k-shift criterion (±g_A A/hop to 1e-3 at k = 0.15) omitted the lattice factor 1/cos k that S4-P R1
  documents: measured 0.00198 (grid step 1e-5) vs 0.001953 (1.4 % off); 0.001953/cos 0.15 = 0.001975. Charge-odd,
  identity-blind and lapse-blind parts passed. The pre-registered verdict stays FAIL.
- EM-T5b was STOPPED by hand at 09:42:16: with wilson = 3 the source coefficient is σ·hop/g with g = gcd(hop, 3) = 1, i.e.
  2²⁷× the Wilson-free normalisation: the coupling is absurdly strong and the random-data board grows doubly
  exponentially (max|value| 1.7e17 after 6 updates, Python-int path). The identities were exact in those 6 updates
  (continuity, Lorenz, Gauss step, Noether: 0 failures, checked by hand), but the run cannot finish. DESIGN NOTE: the
  source normalisation depends on g = gcd(hop, wilson); use Wilson weights hop/2^k (g large) and σ ∝ g.
- The (+,−) Coulomb run EM-D1 r = 8 (09:39–09:40) gave Newton III = −1.0000 EXACTLY: with the R′-fixed vacuum the
  antiparticle is the EXACT C-image (remainders included), so the prepared (+,−) state is exactly C∘P-symmetric and the
  exact dynamics keep it so. a2/a1 = −1 there is a symmetry, not a test (S4's runs were not exact C-images: N3 −1.004).

AMENDMENT A3 (before the runs it governs):
- Wilson weight in every test that uses one: wilson = hop/8 = 2²⁴ (g = 2²⁴, hs = 8, ws = 1) with σ scaled by g/hop
  (σ = 2⁸ where the Wilson-free value is 2¹¹): EM-T5b (T = 30, values ∈ [−2¹⁰, 2¹⁰]), EM-T7 Wilson case, EM-T8, EM-T2
  OD3 check (any wilson works there), EM-T7 free-matter check.
- EM-T9b (POST-HOC, labelled): the k-shift of a uniform A_x, found by bisection, equals g_A A/(hop cos k) to 1e-3 at
  k = 0.15 and k = 0.02 (both charges, opposite signs).
- EM-D1b (new, NON-SYMMETRIC Newton III): (+,−) at r = 8, L = 32, T = 150, particle width 2.0, antiparticle width 2.4
  (different ⟨E''⟩): force ratio F2/F1 = (a2/⟨E''⟩₂)/(a1/⟨E''⟩₁) ∈ [−1.025, −0.975]; each meas/pred ∈ [0.90, 1.05].
  The like-charge runs (spin 0 vs spin 1 packets) are not symmetric: their a2/a1 is a genuine Newton-III test.

### AMENDMENT A4 (written Tue Nov 10 09:51:56 UTC 2026) — POST-HOC follow-ups, labelled, registered BEFORE they run
- EM-D2b (POST-HOC): the registered EM-D2 (T = 40) is noise-dominated (displacements ~ 1e-3 sites; ratios 0.55–1.25).
  The spreading guard allows far more: measured σ(40)/σ0 = 1.003, spreading time 2σ0²/⟨E''⟩ ≈ 500 updates. Re-run the
  SAME protocol with T = 120 (σ(T)/σ0 ≈ 1.03 ≤ 1.3, still a short window in the P-a sense); same pass marks as EM-D2.
- EM-D4b (POST-HOC readout): the registered half-peak [100] front took each station's peak over a window containing
  the wrapped image wave (L = 48, T = 70). Re-read with the peak restricted to t < d_image/c_Q − 2 (d_image = distance
  to the nearest periodic image of the source) and the fit over stations r ≤ 0.8 c_Q T; same pass marks ([111] within
  1.5 % of c_Q, [100] in [0.56, 0.61]). The Q = 5 board is re-run at L = 48, T = 60 (the registered L = 32 fit used
  stations the front never reached): [111] within 3 % of c_5 = 0.5164.
- EM-D1c (diagnostic, no pass mark): the (+,−) r = 8 run with S4-P's remainders (matter r = 3Q, field r = 3Q,
  i.e. D/2 as S4 used) to see whether the 3 % excess over S4's measured value (S4 a1 = 6.43e-7, a2 = −6.27e-7,
  pred 6.36e-7; mine ±6.62e-7, pred 6.355e-7) comes from the exact-C symmetric preparation.

### PRE-REGISTRATION EM-T10 (written Tue Nov 10 09:54:21 UTC 2026, BEFORE it runs) — the single 8-channel sin-Dirac gear
build_matter(species="single", wilson = hop/8), L = 4, random a, b ∈ [−2¹⁰, 2¹⁰], random remainders, T = 40:
(i) check_reciprocity passes with 0 designations; (ii) the exact carrier Noether identity (X = J8) at every node and
update: ρ_J(t+1) − ρ_J(t) + div j_J = R_J, 0 failures (the pair's charge identity with J8 in place of J'); (iii) the
Kramers reversor K8∘M′ (K8 = R_j ⊗ 1₂, K8² = −1): X F⁴⁰ X F⁴⁰ = id or the central negation Jp, and X(vac) = vac;
(iv) rewind exact; (v) OD3: ≤ 2 distinct gears per face neighbour.

## 3. RESULTS (written Tue Nov 10 09:55:48 UTC 2026; raw numbers in results/EM-T*.json and demos/em/results/*.json)
Test suite run 09:43:00–09:44:34 (10 tests OK) + EM-T10 09:54:31 (OK). Every run below is exact-integer, int64 path
(guard never tripped), and rewinds exactly.

| id | verdict | numbers |
|---|---|---|
| EM-T1 algebra | PASS | all 17 integer checks true (J, J′ commuting complex structures; V, P_dJ′ symmetric signed permutations commuting with J, J′; K anticommutes with J, K² = −1; C flips J′) |
| EM-T2 structure | PASS | G = 20, 482 monomials, rank 3, stages (A_x, A_y, A_z) → (Phi) → (16 matter); every Phi coefficient ≡ 0 mod 3Q; OD3 max 1 (wilson 0) / 2 (wilson ≠ 0); deviation form; support_violations = exactly the 18 A-stencil neighbour entries |
| EM-T3 reciprocity | PASS (with designations) | 134 b-only monomials checked, 230 designated = 48 A sources + 16 matter←Phi.b + 160 matter←A.b + 6 Phi←A.b, 0 other, 0 undesignated cross b-only; 118 two-time monomials skipped; free matter reciprocal with 0 designations; stripped designations → FAIL with 230 violations; Peierls control: its 96 vector entries + sources reciprocal UNdesignated (checker ok); blind control flagged (16 violations) |
| EM-T4 vacuum | PASS | matter + em + lapse + driver: F(vac) = vac for 20 updates; frozen_equivalence(ref(Q), matter + em) from a random reference state: 0 base mismatches, 0 new-gear deviations (G 48 → 68, 288 → 770 monomials) |
| EM-T5a identities | PASS | L = 6, T = 60, moving pair, amp 2¹²/2¹⁶/2²⁰ (σ = 2¹⁸/2¹⁰/2²): continuity, Lorenz constant, C ≡ 0, dressed-Gauss step, global Noether: 0 failures in 3 × 12,960 node-updates; undressed Gauss drift max\|Y_g(60) − Y_g(0)\|/max\|σρ\| = 5.2e-4 / 4.3e-5 / 2.8e-6 (~1/A; S4: 1.0e-3 / 5.5e-5 / 4.2e-6) |
| EM-T5b any data | PASS | random data on every gear, wilson = hop/8, T = 30: 0 failures of continuity, Lorenz constancy, Gauss step (with its ΔC term), Noether (1,920 node-updates); rewind exact |
| EM-T5c controls | PASS | Peierls control board: continuity 4,092/4,320 and Gauss 4,092/4,320 node-updates FAIL (S4 D4: 57,718/58,000); dropping R: 4,264/4,320 fail; dropping r_A: 4,264/4,320 fail |
| EM-T6 rewind | PASS | every EM-T5 run rewinds exactly |
| EM-T7 reversor | PASS | (wilson 0, M′): X F X F = N (central Kramers sign) at 10/10 states; X F³⁰ X F³⁰ = N; 0 click-size mismatches, identical click flags under K, 233,642 mirrored matter clicks (S4: 0/233,911); X(vac) = vac; my X ≡ the X built from core/reversors; controls: plain M′ fails 3/3, un-staggered Phi fails 3/3; C ≡ 0. Same with M (S4 convention; vacuum moved 3Q−1 → 3Q, as stated) and with wilson = hop/8 (234,164 clicks). Free matter (wilson hop/8): core reversor_check X F⁴⁰ X F⁴⁰ = Jp, K∘M′(vac) = vac |
| EM-T8 C symmetry | PASS | F∘C = C∘F 10/10 (L = 3, 4, values to 2²⁰, wilson hop/8); ρ ↦ −ρ, j ↦ −j 10/10; C(vac) = vac |
| EM-T9 Bloch | PASS for charge-odd / blind / lapse; k-shift FAIL as registered | δλ(J′ = ±) = −8000 / +8000 at 2 g_phi Phi = 8000 (charge-odd, exactly the documented normalisation); identity +8000 both (blind); lapse W0 −7997.52 both (blind). k-shift: registered prediction (no 1/cos k) FAIL (0.00198 vs 0.001953); POST-HOC with 1/cos k (S4-P R1's factor): 0.99985 / 1.00015 (k = 0.15), 0.99998 / 1.00002 (k = 0.02) |
| EM-T10 8-block | PASS | single sin-Dirac gear (wilson hop/8): reciprocal, 0 designations; carrier (J8) Noether 0 failures / 2,560; Kramers K8∘M′ X F⁴⁰ X F⁴⁰ = Jp; vacuum fixed; rewind exact; OD3 max 2 |

| demo | verdict | numbers |
|---|---|---|
| EM-D1 Coulomb (+,−) r = 8 | PASS | attract; a1 = 6.623e-7 vs pred 6.355e-7: 1.042; a2/a1 = −1.0000 EXACTLY = the exact C∘P symmetry of the prepared state (not a Newton-III test) |
| EM-D1 Coulomb (+,−) r = 12 | FAIL (magnitude) | attract; 1.0500080 vs the registered ≤ 1.05 (miss by 8e-6); N3 −1.0006 |
| EM-D1 (+,+) r = 8 / (−,−) r = 8 | PASS | repel; 0.918 both (S4 final design 0.926); a2/a1 = −1.0000 exactly (symmetric preparation again) |
| EM-D1b unequal widths 2.0/2.4 | PASS a/pred; N3 FAIL as registered (mis-specified) | a1/pred 1.016, a2/pred 1.001; registered per-particle force ratio −0.570 (it omits the charge weight: Q2/Q1 = 1.726); POST-HOC momentum ratio (Q-weighted) −0.984 (pred −0.9996), within 2.5 % |
| EM-D1c diagnostic (remainders 3Q+1) | reported | 1.032 / 1.027, N3 −0.9956: rounding-level changes of the preparation move the ratio by 1–2 % |
| EM-D8 blind control | reported | a2/a1 = −1.614 (S4 −1.586): a non-reciprocal action breaks Newton III |
| EM-D2 1/r² T = 40 | FAIL | signs right; ratios 0.99/1.17, 1.01/1.25, 0.65/0.55, 0.69/0.69 (r = 8, 10, 12, 14; +/−); slope −3.51 vs torus gradient −2.45; Phi bit-static; spreading 1.004: noise-dominated short window (displacements ~1e-3 site) |
| EM-D3 non-circular | PASS | rel L2 (r < 6) 0.058–0.101 at t = 50–60 (S4 0.07–0.09); separation(coupled) − separation(G=0) = −0.0060 at t = 60 (S4 −0.006); C ≡ 0; rewind exact |
| EM-D4 dipole z, Q = 1025, L = 48 | PASS except [100] half-peak | C ≡ 0 in 7,741,440 node-updates; strict taxicab causality 0 violations; \|E_∥\| ∝ r^−1.002 (r = 10–18); other transverse 3.9 %; long/trans 0.153 / 0.089 / 0.062 / 0.065 / 0.053 (r = 4, 6, 8, 10, 12) (S4 0.089 / 0.064); φ = Phi control 0.277 / 0.220 / … (≥ 2×); fronts half-peak [111] 0.5767 (c_Q 0.57707, −0.06 %), [100] 0.425 FAIL; 1/10-peak [111] 0.5772, [100] 0.5703 |
| EM-D4 y-dipole | PASS | the second polarisation: E_y amplitudes on the x axis bit-identical to E_z of the z-dipole |
| EM-D4 Q = 5, L = 32 | FAIL (readout) | [111] fit used stations the front never reached (v = 0.02) |
| EM-D4b POST-HOC pre-image readout | [111] PASS, [100] FAIL | Q = 1025: half-peak [111] 0.5774, [100] 0.493; 1/10 [111] 0.5774, [100] 0.592. Q = 5 (L = 48, T = 60): half-peak [111] 0.507 (c_5 0.5164, −1.7 %), 1/10 0.519. The axis fronts are slow because the light-gear stencil disperses along [100] at Ω = 0.4 (group velocity sin k/(3 sin Ω) ≈ 0.55), while [111] is dispersion-free (front exactly on the cone) |
| EM-D5 magnetism | PASS | charge-odd −1.017, velocity-odd −1.017, a/(E''_xx q_A v_y⟨∂_xA_y⟩) = 1.080 / 1.098 / 1.098 / 1.080 (with the documented 1/cos k_y = 1.0857: 0.994 / 1.011); parallel currents attract; Phi ≡ 0 exactly; G = 0 drift −1.0835e-6 (S4 −1.083e-6) subtracted |
| EM-D6 click charge | PASS | q_click/Q′ = 1.017588 for both species (S4 1.0176), rel std 3.0e-5, sign + / − (flips with C); matter official clicks 932,248 = 97.1 % of gear-updates, kinds C0/C1/C2 = 4 / 466,122 / 466,122; Phi clicks 56,402 all C0 (pure carries) |
| EM-D7 two forces | PASS | gravity a_anti/a_part = +1.0000 (exact: C is an exact symmetry and the lapse is C-even; S4 +0.99987); EM −1.0025 (S4 −0.9978); click/event 0.99893 / 0.99893 / 0.99886 / 0.99893 (S4 0.999); both fields: superposition 0.995 (gravity part) / 0.982 (EM part) (reported, not registered) |

## 4. COMPACT-U(1) EM CANDIDATE (manager ruling 09:5x) — design and PRE-REGISTRATION (written Tue Nov 10 09:59:08 UTC 2026, BEFORE any code runs)
Design (reciprocal by construction, ONE potential, b-only):
- matter: my 16-ch pair (build_matter), hop = A·κ_D, wilson = A·κ_W (vacuum hopping supplied by the matter block);
- links: B1-GAUGE's u1 block imported READ-ONLY: build_gauge(group="u1", Q, A, kappa = 0, mass = 0, lam, use_P = True,
  kappa_P, c_P, beta) with its Gaussian-integer matter gears (psi_*) and their on-site terms removed (kappa = 0 leaves
  them decoupled); link gears U<axis>_re/_im (deviation W = U − A·1), 2-path gears P<k1><k2>_re/_im, OD4 spring;
- coupling (new block, layers/em_compact.py): Ψ_c = Σ_x Σ_d b(x)ᵀ [W_re(x,d) + W_im(x,d) J′] N_d b(x + e_d),
  N_d = κ_D P_dᵀ − κ_W W0; in physical variables Ψ_matter-link = Σ b(x)ᵀ M(U) N_d b(x+e), M(U) = U_re + U_im J′,
  exactly invariant under b(x) → M(g_x) b(x), U(x,d) → g_x U ḡ_{x+e} (with B1-GAUGE's P → g_x P ḡ_{x+e1+e2}).
  Every term = ∂Ψ/∂b: the checker must pass with 0 designations.
- Parameters: Q = 2²⁹ + 1; B1-GAUGE's default family at this Q (their NOTES S2): A = 2¹⁴, κ_P = 256, c_P = 0,
  β = 6Q − 2²⁹ (P0 = 128, c_U = 131072), λ = 4; my matter hop = 2²⁷ (κ_D = 2¹³), mass = 3Q, wilson 0 (and κ_W = 2¹⁰,
  wilson = 2²⁴ in the identity tests).
- Exact Gauss/Noether (local generator i at node y; physical variables X = W + X0): G_y(t) = ρ_y(t) + D Σ [ε of links
  based at y] − D Σ [ε of links ending at y] + D Σ [ε of P based at y] − D Σ [ε of P ending at y (based at y − e1 − e2)],
  ε(u) = X(t−1)·(i X(t)) for a complex gear pair; G_y(t+1) − G_y(t) = Σ_{supp} X(t)·T(r(t) − r(t+1)) EXACTLY.
Pre-registered checks (EM-C1 … EM-C7):
- EM-C1 (i) dressed Gauss at every node: 0 failures, (a) random data on every gear (|a|, |b| ≤ 2¹⁰ for matter, links
  and 2-paths), L = 4, T = 30, with and without the Wilson term; (b) a moving pair (amp 2⁹) with Gauss-prepared links,
  L = 6, T = 40. Plus the global charge Σρ + (link parts sum to 0 on the torus): Σ_y G_y conserved up to the remainders.
- EM-C2 (ii) check_reciprocity(compose(matter, u1-links, coupling)) PASS with 0 designations.
- EM-C3 (iii) exact rewind (the EM-C1 runs) and the plain mirror M′ (b-only): M′ F³⁰ M′ F³⁰ = id on the EM-C1(a) state;
  M′(vac) = vac; F(vac) = vac.
- EM-C4 (iv) Coulomb sign, dynamical two-body, L = 24, amp 2⁹, width 2.0, T = 120, links prepared Gauss-consistent
  (θ advance per update on each link = −∇⁺φ, −Δφ = ρ/(D A²), torus): (+,−) at r = 8 attract (species projection);
  (+,+) at r = 10 repel (half-space centroids). PASS: the signs of a1 and a2 (both packets), each exact.
- EM-C5 (v) Newton III, NON-symmetric (+,−) r = 8, widths 2.0 / 2.4: charge-weighted momentum ratio
  (Q2 a2/⟨E''⟩₂)/(Q1 a1/⟨E''⟩₁), Q_i = |Σρ| of packet i alone: PASS iff ∈ [−1.025, −0.975].
- EM-C6 (vi) link-wave front: a transverse link pulse (W_im of A_z-links on a 3×3 patch around the centre, amplitude 2⁸,
  W(t−1) = W(t)), no matter, L = 40, T = 30: half-peak and 1/10-peak arrival speeds of |W_im| along [100] (x axis) and
  [111], compared with c_Q = 0.57735: PASS iff [111] half-peak within 3 % of c_Q (the value is reported either way).
- EM-C7 (vii, if time) magnetism sign: skipped unless time remains; then registered separately.

### RESULTS EM-C1–C3 (test run 10:00:59–10:01:00) and AMENDMENT A5 (written Tue Nov 10 10:01:31 UTC 2026, BEFORE EM-C4–C6 run)
- EM-C2 PASS: check_reciprocity ok with 0 designations (583 monomials at κ_W = 0, 967 with κ_W = 2¹⁰), b-only, no
  constants, rank 4 only through B1-GAUGE's OD4 spring (12 degree-3 monomials); 120 physical supports wider than a
  link = the 2-path entries (B1-GAUGE's design fact).
- EM-C1 PASS: dressed Gauss/Noether step identity 0 failures at every node and update (random data, L = 4, T = 30,
  κ_W = 0 and 2¹⁰: 1,920 node-updates each; prepared moving pair amp 2⁹, L = 6, T = 40: 8,640), global sums exact.
- EM-C3 PASS: rewind exact (all three runs); M′ F³⁰ M′ F³⁰ = id (both random runs); F(vac) = vac; M′(vac) = vac.
- Resolution finding: with A = 2¹⁴ the Gauss-prepared link angle at r = 8 from an amp-2⁹ packet is A·δθ ≈ 2 integer
  units (initial Gauss residual 4 % of max ρ on L = 6): too coarse for a force readout.
AMENDMENT A5: EM-C4 and EM-C5 use amp = 2¹¹ (field ∝ amp²: A·δθ(r = 8) ≈ 30 units) and T = 60 (expected
displacements ~0.03 sites); everything else as registered. EM-C6 unchanged.

## 5. CENSUS (manager's binding conditions 3–6; written Tue Nov 10 10:02:40 UTC 2026; demos/em/census.py → demos/em/results/EM-census.json)
E1 system compose(matter, em, lapse-mechanism, driver-mechanism), Q = 2²⁹ + 1:
- G = 22, 501 monomials (645 with wilson = hop/8), rank 3 (no rank-4 term: no OD4 spring is needed by E1), 0 constants
  (deviation form; every term targeting a new gear has a new-gear factor), 0 terms into ref.* (q_lattice trivially []).
- OD3 placement: only the matter rows read two distinct gears from one face neighbour (P_dᵀ entry + Wilson W0 entry),
  max 2; without Wilson max 1. The 48 reference channels are untouched.
- Two-time (a-read) monomials — 118, all of the design's named kinds (P-i: accumulator ← fields; matter ← centred
  potential), staged inverse A → Phi → matter:
  * 6 × Phi ← A_d.a (at x and x − e_d): the Lorenz accumulator's +div A(t−1);
  * 16 × matter ← (Phi.a · b), and 6 × 16 × matter ← (A_d.a · b) (A_d at x and x − e_d): the −Phi(t−1) and
    +div A(t−1) parts of the time-centred read Phi(t) + Phi(t+1).
- Physical supports wider than one link (Tensor.support_violations): exactly 18 = the six neighbour entries of each
  A_d headroom stencil (the link-field light stencil couples parallel links: a plaquette or three collinear nodes).
  Storage rule (B3) holds everywhere.
- Designations: 230 (E1 cross terms; §R) + the MECHANISM blocks' one-way reads (16 lapse, 1 driver); 0 designated reads
  coincide with a force term (checked on the raw block terms before merging).
- Field signs: every gear s = +1 (no sign_why needed).
- Reversors as data: build_matter(...).params["reversor"] (K∘M′, central Jp), build_em(...).params["reversor"]
  (X = (K∘M′, M′ on A_d, Phi ↦ (−Phi_next, −b, r)), X(vac) = vac for odd Q; even Q has no mirror-fixed remainder).
  J/JR/JM are not used: the A source is quadratic in the matter (even under negation), so E1 is not J-odd.
Compact candidate compose(matter, u1-links, coupling): G = 34, 583 monomials (967 with κ_W = 2¹⁰), rank 4 only via
B1-GAUGE's spring (12 degree-3 monomials, minus sign), b-only (0 a-reads), 0 constants, 0 designations, 120 supports
wider than a link = B1-GAUGE's 2-path entries; reversor M′ on every gear (b-only), vacuum fixed.

### RESULT EM-C6 (run 10:02:14) and PRE-REGISTRATION EM-C6b (written Tue Nov 10 10:03:19 UTC 2026, BEFORE it runs)
- EM-C6 FAIL (as registered): in B1-GAUGE's default u1 regime (κ_P = 256, P0 = 128) a transverse link pulse (W_im = 256
  on a 3×3×3 patch) produced NO integer change at any station |x − c| ≥ 3 in 30 updates: the 2-path transfer per update
  (~κ_P P0 W / D ≈ 2.6e-3 units) stays below integer resolution (held in the remainders). Taxicab causality exact,
  rewind exact. So in this regime the compact photon does not propagate on the shared cone (electric/strong-coupling
  limit: flux is carried by Gauss-prepared links, not re-radiated).
- EM-C6b (EXPLORATORY, no pass mark; parameters outside B1-GAUGE's verified regime): the same pulse with a stiff
  plaquette, κ_P = 2¹⁵ (P0 = 2¹⁴, c_U = 4κ_P P0 = 2³¹ < D), A = 2¹⁴, λ = 4, β = 6Q − 2²⁹; report the half/tenth-peak
  fronts along x and [111], the link-norm deviation, taxicab causality and rewind.

### RESULTS EM-C4/C5 (runs 10:02:25–10:03:02) and POST-HOC diagnostics EM-C4b/C5b (registered Tue Nov 10 10:05:37 UTC 2026, before they run)
- EM-C4 signs PASS: (+,−) r = 8 attract (a1 = +1.006e-5, a2 = −1.007e-5; the equal-width state stays exactly C∘P
  symmetric: o1 + o2 = 0 at every update); (+,+) r = 10 repel (a1 = −9.23e-6, a2 = +1.44e-6). Gauss step 0 failures
  (sampled), rewind exact, link norms within 5.7e-4 of A.
- EM-C5 FAIL: unequal widths, charge-weighted momentum ratio −0.502 (registered band [−1.025, −0.975]).
- Diagnosis (from the stored trajectories): the compact field is NOT static in this regime — the link phase advance
  (E) at the midpoint decays 0.0299 → 0.0278 (−7 %) in 60 updates and both packets decelerate after t ≈ 30–40, so a
  quadratic fit over T = 60 is not a constant-force reading; the (+,+) half-space readout is also biased (the centre
  plane dx = 0 belongs to packet 2's half: initial centroid 4.987 instead of 5).
- EM-C4b (POST-HOC): (+,+) r = 10 with symmetric half-spaces (dx ∈ [−11, −1] and [1, 11]); report a1, a2, a2/a1.
- EM-C5b (POST-HOC): the same three runs fitted over the EARLY window t = 0–20 (before the field decay); report the
  charge-weighted momentum ratio of the unequal-width run (no pass mark: post-hoc).

## 6. RESULTS of the post-hoc runs and the compact route (written Tue Nov 10 10:07:20 UTC 2026)
| id | label | numbers |
|---|---|---|
| EM-D1c | diagnostic | (+,−) r = 8 with matter remainders 3Q+1 (C-image no longer exact): a/pred 1.032 / 1.027, N3 −0.9956. A rounding-level change of the preparation moves the ratio by 1–2 %; the remaining ~2–3 % gap to S4-P's own final-design file (a1 6.43e-7, a2 −6.27e-7, pred 6.36e-7, mean 0.998; mine ±6.62e-7, pred 6.355e-7) is OPEN. A structural difference: S4 ran the field gears with their own divisor 6·2¹⁰ (coarser field rounding), the package uses ONE divisor 6Q for every gear. |
| EM-D2b | POST-HOC, FAIL | T = 120 (σ(T)/σ0 = 1.034): signs right; a/pred (+/−) 0.987/1.015 (r = 8), 1.022/1.095 (10), 1.116/1.154 (12), 1.119/1.299 (14); charge symmetry 0.028/0.071/0.033/0.161; slope of \|a\| −2.107 vs torus gradient −2.446 (Δ = 0.34 > 0.15); κ max/min 1.21; Phi bit-static; rewind exact. The short-window 1/r² of the twin (−2.02 vs −2.15) is NOT reproduced; the test-charge response grows relative to the prediction with r. The dynamical two-body runs (EM-D1, r = 8, 12) remain the magnitude evidence. |
| EM-D4b | POST-HOC | see §3 (pre-image readout): [111] 0.5774 (Q = 1025), 0.507 (Q = 5, −1.7 %); [100] half-peak 0.493 FAIL |
| EM-C4 | registered, PASS (signs) | (+,−) r = 8 attract, (+,+) r = 10 repel (amp 2¹¹, T = 60); Gauss 0 failures; rewind exact |
| EM-C4b | POST-HOC | (+,+) with symmetric half-spaces: a1 = −9.109e-6, a2 = +9.109e-6 (exact mirror symmetry; the registered readout's asymmetry was the mask) |
| EM-C5 | registered, FAIL | unequal widths: momentum ratio −0.502 (T = 60 fit over a decelerating trajectory) |
| EM-C5b | POST-HOC | early window t ≤ 20: momentum ratio −0.962 (unequal widths), −0.9999 (equal widths) |
| EM-C6 | registered, FAIL | no link wave reaches \|x − c\| ≥ 3 in 30 updates (B1-GAUGE default regime: transfer ≈ 2.6e-3 units/update, below integer resolution) |
| EM-C6b | EXPLORATORY | κ_P = 2¹⁵ (c_U = 2³¹ < D): link waves propagate, half-peak [111] 0.495 (0.86 c_Q), [100] 0.256; taxicab exact; rewind exact. Off the shared cone and anisotropic. |
CONCLUSION on the compact route (for the manager's choice, not decided here): it is exactly reciprocal (0
designations), has the exact Noether Gauss law with the remainder dressing, the exact plain mirror and rewind, and the
correct Coulomb SIGNS from Gauss-prepared fields. In B1-GAUGE's verified regime it is the electric (strong-coupling)
limit: no light (EM-C6), the prepared Coulomb field is not stationary (E at the midpoint −7 % in 60 updates) and
dynamical Newton III fails over T = 60 (−0.50; −0.96 in the first 20 updates). A stiffer plaquette propagates links but
off the shared cone (0.86 c_Q on [111]). E1 keeps the cone, the static Coulomb field and Newton III to ≈ 1.6 %, at the
price of 230 designated (continuum-reciprocal) entries.

## 7. API and how to run (written Tue Nov 10 10:07:20 UTC 2026)
- Blocks: layers.matter.build_matter(Q, hop, mass, wilson, species="pair"|"single"); layers.em.build_em(Q, matter,
  g_phi, g_A, sigma, stencil, vector, blind); layers.em.build_current_driver (MECHANISM line/dipole currents);
  layers.matter.build_static_lapse_mechanism (MECHANISM lapse); layers.em_compact.build_u1_links /
  build_compact_coupling / default_compact. MATTER INTERFACE: layers.matter.rest_clock_terms, transport_terms,
  link_hamiltonian, bloch_matrix, algebra, REVERSOR_MATTER; observe.em.density(X="Jp" charge | "J" C-even number),
  link_currents(X), continuity_residual.
- Initial data: prepare.em.dirac_packet (particle; c_image for the antiparticle), set_matter, set_field,
  static_phi_for, torus_poisson; prepare.em_compact.gauss_links, link_pulse. Audit maps: prepare.em.c_map,
  x_reversor (M′ default, M option), x_reversor_core (built from core/reversors), matter_negation.
- Observables: observe.em (charge density, currents, remainder term, Lorenz C, Gauss Y_g and its step residual,
  E field with phi_norm, species projectors, click sizes and click charge); observe.em_compact (gauss_G, dressing,
  step residual, link phase advance, link norm deviation). Clicks: core Engine.clicks.
- Commands (repository root): OMP_NUM_THREADS=2 nice -n 10 python -m unittest
  research.metric_variant_v1.tests.test_em research.metric_variant_v1.tests.test_em_compact -v;
  demos: cd research/metric_variant_v1/demos/em && python coulomb.py +- 8 150 | slope.py [T] | noncircular.py |
  dipole.py z 1025 48 70 | magnet.py | qclick.py | twoforces.py | compact_coulomb.py +- 8 [w2] [sym] |
  compact_wave.py [kappa_P] | census.py | n3_charge_weighted.py.

### PRE-REGISTRATION EM-D2c (POST-HOC #2, labelled; written Tue Nov 10 10:08:04 UTC 2026, BEFORE it runs)
Hypothesis from EM-D2b: on L = 40 the stations approach the torus midpoint (r = 20), where Phi turns over (gradient
-> 0, curvature finite), so a/pred grows with r (1.00, 1.06, 1.14, 1.21). Re-run the SAME protocol on L = 56 (midpoint
28; stations 8, 10, 12, 14 at >= 14 sites from it), T = 100. Pass marks as EM-D2. Reported with EM-D2 and EM-D2b
(three attempts in total; only EM-D2 was pre-registered as the protocol).

### §R addendum — the finite-rank no-go in one recursion (for the board's verification)
(written Tue Nov 10 10:08:52 UTC 2026) Let the A-dependent link part of the potential on the link (x, x+e) be Ψ_A = Σ_{n=1..N} A^n
b(x+e)ᵀ L_n b(x) (any finite order N; on-site A-terms contribute nothing to the J′ current because their matrices are
symmetric and commute with J′). The exactly conserved J′-current through the link is the response to rotating b(x+e)
alone: c(A) = b(x+e)ᵀ J′ᵀ (L_0 + Σ_n A^n L_n) b(x) (L_0 = the free hopping H_dᵀ-block). The Lorenz accumulator gives an
exact (dressed) Gauss law iff the A source is a fixed multiple κ of that current, and reciprocity demands the source
be ∂Ψ_A/∂A = Σ_n n A^{n−1} L_n. Equating the coefficients of A^{n−1} for every A: n L_n = κ J′ᵀ L_{n−1}, so
L_n = κⁿ (J′ᵀ)ⁿ L_0 / n!, which is never 0 (J′ is invertible and L_0 ≠ 0): Ψ_A = b′ᵀ (e^{κ A J′ᵀ} − 1) L_0 b, the compact
(Peierls-exponential) link. Any finite N violates it at order A^N, i.e. exactness and reciprocity are incompatible at
finite rank unless the link variable is itself compact (stored as the group element, as in layers/em_compact.py).
A two-time (a-read) source would escape the checker but is excluded: the matter reads A.a (centred read), so an A source
reading matter.a would close an a-read cycle (no staged inverse).

### PRE-REGISTRATION EM-D1d (written Tue Nov 10 10:09:19 UTC 2026, BEFORE it runs) — the remaining Study-4 separations
EM-D1 protocol unchanged (L = 32, amp 2¹⁴, width 2, σ = 2¹⁴, T = 150): (+,−) at r = 6 and 10, (+,+) at r = 12. PASS:
signs exact; meas/pred ∈ [0.90, 1.05]. (Symmetric preparations: a2/a1 = −1 by symmetry, not reported as a test.)

### RESULTS EM-D1d (runs 10:09:19–10:12:19; written Tue Nov 10 10:12:42 UTC 2026)
| run | verdict | numbers |
|---|---|---|
| (+,−) r = 6 | PASS | attract, a/pred 1.031, rewind exact, C ≡ 0 |
| (+,−) r = 10 | PASS | attract, a/pred 0.977, rewind exact |
| (+,+) r = 12 | PASS | repel, a/pred 0.963 (S4 1.014 at T = 300, early 0.985), rewind exact |
Derived from the registered (+,−) runs r = 6, 8, 10, 12 (no separate pass mark): log-log slope of \|a\| = −2.461 vs the
torus-Poisson prediction −2.452 on the same L = 32 torus (S4-P: −2.41 vs −2.48). Over all E1 dynamical Coulomb runs
a/pred ∈ [0.918, 1.050] (agreed band 0.92–1.01; S4 final design 0.926–1.011).

### PRE-REGISTRATION EM-C8 (POST-HOC diagnostic, labelled; written Tue Nov 10 10:13:20 UTC 2026, BEFORE it runs)
Compact route, (+,−) equal widths 2.0, amp 2¹¹, L = 24, r = 6, 8, 10, window t = 0–20 (before the field decay seen in
EM-C5): ratio a1 / (⟨E''⟩ · ⟨δθ_x⟩_{|ρ1|}), δθ_x = the prepared link phase advance (temporal-gauge E) averaged to
nodes ((δθ(x) + δθ(x − e_x))/2) and weighted by packet 1's |ρ| at t = 0; and the log-log slope of |a1| over r.
No pass mark (diagnostic of whether the compact field's initial force follows the Gauss-prepared Coulomb field).
RESULT EM-C8 (run 10:13, written Tue Nov 10 10:13:40 UTC 2026; POST-HOC diagnostic): a1/(⟨E''⟩⟨δθ_x⟩) = 0.861 (r = 6), 0.982 (r = 8),
1.078 (r = 10); signs consistent (attraction); |a1| log-slope −2.59 vs the prepared-field prediction −3.03 on this
L = 24 torus. So the compact field's INITIAL force follows the Gauss-prepared Coulomb field to ±14 %; the failure of
EM-C5 is the subsequent non-stationarity of the field in B1-GAUGE's regime, not the coupling.

## 8. FREEZE-READY EM (declared to the manager Tue Nov 10 10:36:32 UTC 2026)
Frozen (no edits after this point; new work goes into new files; this NOTES file keeps changing as documentation):
| file | sha256 |
|---|---|
| layers/matter.py | 078f38405fa67d1d0b2cb22d229d8ff725b9dfbb89bdf7ce320d0f6e9e25e1a2 |
| layers/em.py | 9c13b9b87ca4563741e5bb70a93d976659185aaf3247645b159a9abfdea94b6b |
| prepare/em.py | 5aff316e01aeb43ddfd4c16cb24ef13d37c690c23fe9e4be9c50e2efdb379b48 |
| observe/em.py | fc2c1932b8f377fa8a5adee1946fdea917d691a11f7c7c95a4732b6cdbb04c29 |
| tests/test_em.py | 2ea623ab9d9fe19d43dd1c39708dcfdaed2da836f6c1ea4b991fc9f7765f042f |
| layers/em_compact.py | c7ce8d5db79672bd235edc0b07a598961c21f1bc23ad67d8870fb1111f7ff0f2 |
| prepare/em_compact.py | f5ca257ad0b0000328f10a044fe247f6f8b39eeaacb15f989c113d8303b33331 |
| observe/em_compact.py | c51b1b86317ad92f4df6755f1d0f4b50a54e807a1aa8b57813fc8ca325a2f104 |
| tests/test_em_compact.py | 3210834d261898350ee5e614b81747b721cbac7f6820d21a2f76b8b18626a2f3 |
Final test run on exactly these files: 10:06:45–10:06:50 UTC, 13 tests OK (EM-T1–T10, EM-C1–C3). The (+,−) r = 8
Coulomb demo was re-run on the final code at 10:15 and reproduced its 09:39 trajectories bit for bit.
Integrator parameters (both routes, Wilson ON): build_matter(Q = 2²⁹+1, hop = 2²⁷, mass = 3Q, wilson = 2²⁴); compact:
default_compact(Q, kd = 2¹³, kw = 2¹⁰); E1: build_em(Q, matter, g_phi = 4, g_A = 1, sigma = 2⁸ (≙ G = 1) … 2¹¹ (≙ G = 8)).

### RESULT EM-D2c (POST-HOC #2, run 10:08:05–10:38:45; written Tue Nov 10 10:39:04 UTC 2026)
L = 56, T = 100 (σ(T)/σ0 = 1.023), stations 8, 10, 12, 14 on +x, one test-charge probe per board, prepared bit-static
Phi: signs exact; a/pred (+/−) 1.042/0.950, 1.000/1.055, 1.031/1.048, 0.967/1.140 (all ∈ [0.85, 1.15]); log-slope of the
charge-averaged |a| −2.040 vs the torus gradient −2.137 (Δ = 0.098 ≤ 0.15; the twin: −2.02 vs −2.15); κ max/min 1.058
(≤ 1.10); Phi bit-static; rewind exact. Charge symmetry |a(−)/a(+) + 1| = 0.089, 0.054, 0.016, 0.179: FAIL (≤ 0.03).
So the L = 40 trend was the torus midpoint (hypothesis confirmed), and the 1/r² slope with a short window and a prepared
field is reproduced in this third, post-hoc attempt; the pre-registered EM-D2 (T = 40, L = 40) stays FAIL, and the
particle/antiparticle asymmetry of single short-window probes (an even-in-charge offset of a few % of the signal,
sign-changing between stations) is OPEN.

## 9. FINAL VERDICT LIST (written Tue Nov 10 10:39:04 UTC 2026)
REGISTERED PASS: EM-T1–T8, T10; EM-T9 (charge-odd, blind, lapse parts); EM-D1 (+,−) r = 6, 8, 10 and (+,+) r = 8, 12,
(−,−) r = 8; EM-D1b a/pred; EM-D3; EM-D4 (C, causality, 1/r, transverse, longitudinal, φ control, [111] fronts, y-dipole);
EM-D5; EM-D6; EM-D7; EM-C1, C2, C3; EM-C4 signs.
REGISTERED FAIL (kept): EM-T9 k-shift (1/cos k omitted); EM-D1 (+,−) r = 12 magnitude 1.0500080 > 1.05; EM-D1b Newton III
observable (mis-specified, −0.570); EM-D2 (T = 40); EM-D4 [100] half-peak (0.425); EM-D4 Q = 5 readout; EM-C5 (−0.502);
EM-C6 (no link wave).
POST-HOC (labelled): EM-T9 k-shift with 1/cos k 0.99985–1.00015; EM-D1b charge-weighted −0.984; EM-D2b (T = 120) FAIL;
EM-D2c (L = 56) slope/magnitude PASS, charge symmetry FAIL; EM-D4b [111] 0.5774 / Q = 5 0.507, [100] 0.493;
EM-C4b mirror-exact (+,+); EM-C5b early −0.962; EM-C6b exploratory 0.86 c_Q; EM-C8 early force 0.86–1.08.

## 10. COMPACT ROUTE, next step: the 2-path photon speed (DERIVED) and EM-C9 (PRE-REGISTERED Tue Nov 10 10:40:56 UTC 2026, before it runs)
DERIVATION (stiff 2-path limit, small phases U = A e^{iθ}, P = P0 e^{iψ}): the effective static potential
W = (D/2)Σ|X|² − Φ contains (K/2)[(s1 − ψ12)² + (s2 − ψ21)²] + (B/2)(ψ12 − ψ21)², s1 = θ_k1(x) + θ_k2(x+e_k1),
s2 = θ_k2(x) + θ_k1(x+e_k2), K = κ_P P0 A², B = β P0². Minimising over the 2-path phases leaves the plaquette energy
(K_eff/2)(s1 − s2)², s1 − s2 = lattice curl θ, K_eff = K B/(K + 2B). With the link inertia D A² θ̈ = −2∂W/∂θ the
transverse waves obey θ̈ = −(2K_eff/(D A²)) curl curl θ: c² = 2K_eff/(D A²) < K/(D A²) = κ_P P0/D = c_U/(4D).
Predictions: B1-GAUGE default (κ_P = 256, P0 = 128): c = 0.00304 (explains EM-C6: 0.09 sites in 30 updates);
κ_P = 2¹⁵ (P0 = 2¹⁴): c = 0.389. The shared cone c_Q ≈ 0.5774 therefore needs K_eff = D A²/6, i.e. c_U > 4D/3 —
outside the regime B1-GAUGE verified (c_U ≪ D): a design constraint to hand over, not a fix I can make in their block.
EM-C9 (exploratory check of the formula; new file demos/em/compact_dispersion.py): pure u1 links, L = 32, a transverse
plane wave θ_z(x) = ε sin(2πx/L) on every z-link (W_im = rint(A ε sin), ε = 0.01, at rest), T = 300; measure ω from the
projection of W_im onto sin(2πx/L) (zero crossings / fitted cosine) and v = ω/k (k = 2π/L), for κ_P = 2¹⁵ and
κ_P = 2¹³; compare with the stiff-limit formula including the lattice factor (2 sin(k/2))² for curl curl:
cos-free check v_lattice = sqrt(2K_eff/(D A²)) · 2 sin(k/2)/k. No pass mark (exploratory); agreement within 10 % would
support the bound.
RESULT EM-C9 (runs 10:40–10:42; written Tue Nov 10 10:43:00 UTC 2026; EXPLORATORY, INCONCLUSIVE):
- κ_P = 2¹⁵ (c_U = 0.667 D): the plane-wave start excites a fast mode (projected amplitude oscillating at ω ≈ 1.22, not
  the photon) that RUNS AWAY: max|value| > 2⁴⁰ at t = 136 (guard stop; rewind of the 136 updates exact). This stiff-
  plaquette regime is unstable for this initial data (the pulse test EM-C6b ran only 30 updates).
- κ_P = 2¹³ (c_U = 0.042 D): bounded; projected oscillation ω = 0.0845 (v = 0.430) vs the stiff-limit prediction
  v = 0.097 (ratio 4.4). With εA ≈ 164 integer units the run is dominated by rounding and by the transient of the 2-path
  gears (started at P0, not at their slaved phases); this does not test the formula.
So the derived bound c² < c_U/(4D) (§10) is NOT verified numerically; it remains DERIVED. Next step (OPEN, for
B1-GAUGE and me): a larger amplitude, 2-path gears prepared at their slaved phases, and a stability map in c_U/D; the
shared cone needs c_U > 4D/3 by the bound, where the stiff-plaquette runs already show a runaway at 0.67 D.

## 11. Integrator note on the mass (manager 10:3x; written Tue Nov 10 10:43:07 UTC 2026)
Nothing in the matter or EM layers depends on mass = 3Q exactly. The mass is only the rest-clock entry (mass + 6·wilson)
W0 on site. The carrier J (π/2) is a matrix (1₂ ⊗ R_i ⊗ 1₂) and commutes with W0 for any mass. Every exact identity
(continuity, Lorenz, dressed Gauss, Noether), the reversor X = K∘M′, the C map and the vacuum 3Q − 1 hold for any
integer mass with |λ| < D. Demos and predictions read the mass from Block.params. mass = 3·2²⁹ gives mass/D =
1/2 − 1/(2Q), the same physics to 1e-9. All entries are in 2²²·Z for hop = 2²⁷, wilson = 2²⁴, mass = 3·2²⁹; the E1
source normalisation g = gcd(hop, wilson) = 2²⁴ is unchanged by the mass.

## 12. LINK WAVES ON THE SHARED CONE (manager 10:4x) — PRE-REGISTRATION (written Tue Nov 10 10:46:24 UTC 2026, BEFORE any code runs)
New files only: demos/em/link_cone.py (analysis + runs), results in demos/em/results/LC-*.json. B1-GAUGE's
build_gauge / build_default are imported read-only with my own parameters; frozen files are not touched.
METHOD (exact, linear): in deviation form the degree-1 monomials of the link + 2-path gears ARE the Hessian H of the
potential, and the gear dynamics linearised about the vacuum is D(ξ(t+1) + ξ(t−1)) = 2H(k)ξ with the Bloch matrix
H(k)[t, f] = Σ coeff·e^{ik·offset}; hence cos ω = h/D for every eigenvalue h of H(k). Transverse photon = the branch
with h → D as k → 0 that is not a pure-gauge mode (h = D exactly); c = lim ω/k. Linear stability ⇔ |h| ≤ D for all k.
LC1 (dispersion): compute c along [100], [110], [111] (k = 0.05, 0.1, 0.2) and the stiff-limit formula
  c² = 2K_eff/(D A²), K_eff = K B/(K + 2B), K = κ_P P0 A², B = β P0², for u1 at Q = 2²⁹+1, A = 2¹⁴, κ_P = 256, 2¹³, 2¹⁵
  (β = 6Q − 2²⁹, c_P = 0, λ = 4) and for B1-GAUGE's build_default("u1"|"su2"|"su3") at Q = 2²⁵+1 and 2²⁹+1.
  PASS (formula): Bloch c(k → 0) within 1 % of the formula for every u1 case. Also report max|h|/D over a 16³ k-grid.
LC2 (cone regime): search (κ_P, d_P = D − c_P − β, β, λ) at Q = 2²⁹+1, A = 2¹⁴ (P0 = κ_P A²/d_P an integer, c_U = 4κ_P P0)
  for: (i) c within 0.5 % of c_Q = sqrt((Q−1)/(3Q)) along [100], [110], [111] at k = 0.05; (ii) max|h|/D ≤ 1 on a
  24³ grid including the zone boundary (links re/im and 2-paths). Report the best regime, or why none exists.
LC3 (only if LC2 finds a regime): (a) EXACT: reciprocity 0 designations, Noether/Gauss 0 failures, rewind exact
  (u1 links + my pair, L = 4, T = 30, small random data); (b) NONLINEAR STABILITY: random link/2-path perturbations of
  amplitude A/64 on L = 8, T = 1000: max | |U|/A − 1 | ≤ 0.1, no runaway (max|value| < 2⁴⁰); (c) LINK WAVE: a transverse
  pulse (≥ 2¹⁰ units), L = 40, T = 30: half-peak fronts along [100] and [111] within 3 % of c_Q.

### LC1 RESULTS (run 10:46:56–10:47:24; written Tue Nov 10 10:49:19 UTC 2026) and the LC2 argument (written before the LC2 scan runs)
- Formula check (PASS for B1-GAUGE's regime): u1 κ_P = 256 at Q = 2²⁹+1: Bloch c = 0.0030401 vs stiff formula 0.0030410
  (ratio 0.9997); default u1 at Q = 2²⁵+1: 0.012127 vs 0.012164 (0.997). κ_P = 2¹³: Bloch 0.0917 ([111]) and the two
  [100] polarisations 0.0838 / 0.0917 vs formula 0.0973 → FAIL of the 1 % mark: the 2-path gears add inertia
  ((P0/A)² participation; P0/A = 1/4 here), which lowers c and is polarisation-dependent (birefringence at O(k²)).
  κ_P = 2¹⁵: LINEARLY UNSTABLE, max h/D = 1.117 (an extra soft mode; explains the EM-C9 runaway).
- Measured link-wave speed of B1-GAUGE's DEFAULTS (Bloch, k → 0): u1 = su2 = 0.00304 at Q = 2²⁹+1 and 0.0121 at
  Q = 2²⁵+1, i.e. 1/190 and 1/47 of c_Q (su3: its U(3) block has 9 gauge zero modes; re-read below).
- LC2 ARGUMENT (DERIVED; the scan below checks it): (1) the photon has c² = 2K_eff/(D A²(1 + μ)) ≤ 2K_eff/(D A²) <
  c_U/(4D) (μ ≥ 0 = 2-path participation); so c_Q² = (Q−1)/(3Q) needs c_U > (4/3)(Q−1)/Q·D ≈ 4D/3. (2) The uniform k = 0
  radial (re) mode of links + 2-paths has the Hessian [[2λA², −2√2 κ_P A], [−2√2 κ_P A, d_P]] (W-form, per normalised
  mode): static stability needs det ≥ 0 ⇔ λA² ≥ 4κ_P²A²/d_P = c_U; the CFL bound needs its largest eigenvalue ≤ 2D, and
  that eigenvalue is ≥ 2λA² ≥ 2c_U. Hence c_U ≤ D (exactly: c_U ≤ D − d_P/2 at the stability edge), c² < 1/4, c < 1/2 <
  c_Q (odd Q ≥ 5). So NO parameters of this 2-path + spring design reach the shared cone. LC2 scan (pre-registered now,
  before it runs): κ_P ∈ {2¹⁰…2¹⁶}, d_P ∈ {2²⁶…2²⁹}, λ from the static edge c_U/A² upward, c_P = 0 (β = D − d_P), A = 2¹⁴,
  Q = 2²⁹+1: report the largest Bloch c (min over polarisations and directions at k = 0.05) among linearly stable
  configurations (|h|/D ≤ 1 on an 8³ grid plus the k-points used); expected < 0.5.

### LC2 RESULT and CONCLUSION (scan 10:49:30–10:49:44; written Tue Nov 10 10:52:22 UTC 2026)
- su3 re-read with its 9 gauge zero modes (U(3) links): c = 0.01213–0.01215 (Q = 2²⁵+1), 0.003040 (Q = 2²⁹+1): the same
  as u1 and su2. EVERY default compact link layer propagates at ≈ c_Q/190 (Q = 2²⁹+1) or c_Q/47 (Q = 2²⁵+1).
- Scan (112 configurations, κ_P = 2¹⁰…2¹⁶, d_P = 2²⁶…2²⁹, λ = 1.05–3 × the static edge c_U/A², c_P = 0): 70 linearly
  stable. Largest stable c_U/D = 0.333; at c_U/D = 0.667 EVERY configuration with λA² ≥ c_U violates the CFL bound
  (min h/D = −1.67 … −4.3), and those with λA² < c_U are statically unstable (max h/D > 1: the EM-C9 runaway).
  Fastest stable photon: c = 0.163 (fastest polarisation) / 0.130 (slowest), κ_P = 2¹⁴, d_P = 2²⁹, P0 = 2¹³, λ = 3.
- BIREFRINGENCE: the u1 tensor is exactly symmetric under every axis permutation (checked: invariant under y↔z, x↔y,
  x↔z), yet along [100] the two transverse photons differ (0.0838 vs 0.0917 at κ_P = 2¹³; equal along [111]). The
  eigenvectors are the y ± z combinations: the 2-path gears sit only on the "++" diagonal of each plaquette, which breaks
  single-axis reflections and 90° rotations, so nothing maps y+z onto y−z. With non-negligible 2-path inertia
  (P0/A not ≪ 1) the compact photon is birefringent at O(k²). In B1-GAUGE's default (P0/A = 1/128) this is invisible.
- CONCLUSION (task 2): the shared cone is IMPOSSIBLE in the 2-path + spring link design, for every (κ_P, P0, β, c_P, λ,
  A): c² ≤ 2K_eff/(D A²) < c_U/(4D) (the 2-path stiffness comes with the radial pull c_U = 4κ_P P0); radial stability
  needs λA² ≥ c_U; the uniform radial eigenvalue is then ≥ 2λA² ≥ 2c_U, and Rule3's CFL bound (every |h| ≤ D, i.e.
  W-eigenvalue ≤ 2D for ONE divisor) forces c_U ≤ D − d_P/2, so c < 1/2 < c_Q for every odd Q ≥ 5. Numerically the
  fastest stable link wave found is 0.163. This holds for u1, su2 and su3 alike (same 2-path structure).
  Therefore LC3 (tests in a cone regime) does not apply as registered.
- What it means for unification (for the manager/owner, not decided here): with ONE divisor and Rule3 leapfrog, exact
  compact (reciprocal, Noether-exact) links cannot carry waves on the shared cone c_Q in this design; E1 (non-compact
  Lorenz-gauge gears with the headroom stencil) carries EM exactly on c_Q but is reciprocal only in the continuum.
  A different plaquette mechanism, one whose stiffness is not tied to a radial pull (or a different radial
  stabilisation outside the CFL budget), would be needed; I found none within B3 locality, rank ≤ 4 and one divisor.

## 13. E1 coupling under the integrator's dressing constraint (manager 10:5x) — analysis and PRE-REGISTRATION (written Tue Nov 10 10:59:06 UTC 2026)
Normalisation (DERIVED from the static dressed Gauss law −2g(Q−1)ΔPhi = σρ, ρ = D·ρ′, and δλ = 2 g_phi Phi):
the dimensionless clock shift is δλ/D = α ρ′ G(r) with α = g_phi σ/(g (Q − 1)), g = gcd(hop, wilson); Study-4
equivalence G = 2¹⁵ α A_ψ² (checks: σ = 2¹⁴, g = 2²⁷ → G = 8 and σ = 2⁸, g = 2²⁴ → G = 1, both at A_ψ = 2¹⁴).
Dressing integrality (P a power of 2, ws = wilson/g odd when hop is a power of 2): σ·ws ∈ 16P·ℤ ⇒
α ≥ 16 g_phi P/(wilson (Q − 1)) and G ≥ 2¹⁹ g_phi P A_ψ²/(wilson (Q − 1)).
Integrator's σ = 2²⁴ with wilson = 2²⁴ (g = 2²⁴): α = 2⁻²⁷, i.e. G = 65,536 at A_ψ = 2¹⁴ (G = 1 needs A_ψ = 64).
Recommended at Q = 2²⁹+1, P = 2²⁰: hop = 2²⁷, wilson = 2²⁶ (Wilson r = 1/2; mass + 12·wilson = 4.5·2²⁹ < D: stable),
mass = 3·2²⁹ (all ∈ 2²²ℤ), g = 2²⁶, hs = 2, ws = 1, σ = 2²⁴ (σ ws/(2P) = 8, 9σ ws/(16P) = 9), g_phi = 4, g_A = 1:
α = 2⁻²⁹, G = A_ψ²/2¹⁴ → A_ψ = 128 (G = 1), 256 (G = 4), 362 (G = 8).
EM-D9 (pre-registered now, new file demos/em/coulomb_dressing_regime.py; UNDRESSED E1 with these integers, gravity
off): (+,−) r = 8, L = 32, T = 150, width 2.0, A_ψ = 256 and 128; prediction as EM-D1 but with the Wilson term in the
band (E(k) from B(k) with wilson). PASS: attract, meas/pred ∈ [0.85, 1.15], rewind exact, C ≡ 0; reported: the
species-charge drift and max|value| (int64 path).
RESULT EM-D9 (runs 11:01–11:05; written Tue Nov 10 11:05:34 UTC 2026): FAIL as registered. A_ψ = 256 (G = 4): attract, meas/pred 1.80;
A_ψ = 128 (G = 1): meas/pred 26.7; species-charge drift −0.29 % / −1.7 % over 150 updates; rewind exact, C ≡ 0, int64
path. Note: with wilson = 2²⁶ the Wilson term dominates the band curvature (⟨E''⟩ = 0.0576 vs 0.0124 at wilson 0).
EM-D9c (pre-registered now, before it runs): the same A_ψ = 256 state with every EM coupling off (g_phi = g_A = σ = 0):
reported a1, a2 (the rounding-artefact baseline); no pass mark.
RESULT EM-D9c (11:06): coupling OFF at A_ψ = 256: a1 = −3.60e-6, a2 = +3.60e-6 (apparent repulsion), max|b| 256 → 102:
with wilson = 2²⁶ the packets spread within ~70 updates (⟨E''⟩ = 0.0576), so T = 150 breaks the spreading guard and the
EM-D9 readout is artefact-dominated (control-subtracted ratio at A_ψ = 256 is still 4.2).
EM-D9b (pre-registered now, before it runs; option "raise Q"): Q = 2³³+1, hop = 2³¹, wilson = 2³⁰, mass = 3·2³³ (all in
2²²ℤ), g = 2³⁰, ws = 1, σ = 2²⁴ (dressing-integral at P = 2²⁰), g_phi = 4, g_A = 1 → α = 2⁻³⁷, A_ψ = 4096 (G = 4);
(+,−) r = 8, L = 32, width 2.5, T = 60 (σ(T)/σ0 ≈ 1.14), with its coupling-off control. PASS: attract and
(a1 − a1_off)/pred ∈ [0.85, 1.15]; rewind exact; C ≡ 0; int64 path.
RESULT EM-D9b (11:07; written Tue Nov 10 11:08:13 UTC 2026): Q = 2³³+1, σ = 2²⁴, A_ψ = 4096 (G = 4), T = 60: attract; a1 = 3.425e-6 vs pred
2.910e-6 (raw 1.177); coupling-off control a1 = 7.6e-8; control-subtracted ratio 1.151 → FAIL by 0.001 of the
registered [0.85, 1.15]; species-charge drift −3.5e-5; rewind exact; C ≡ 0; int64 path (max|value| 5.0e6).
Conclusion for the integrator: the dressing-integral σ is usable only with a large matter amplitude (A_ψ ≳ 2¹²), i.e.
Q = 2³³+1 at P = 2²⁰ or P ≤ 2¹² at Q = 2²⁹+1. At Q = 2²⁹+1 with P = 2²⁰ a physical coupling (G ≤ 8) forces A_ψ ≤ 362,
where spreading and rounding dominate (EM-D9/D9c).
