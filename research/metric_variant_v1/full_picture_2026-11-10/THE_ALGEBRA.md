# THE ALGEBRA OF EVERYTHING — Universe24 as one law, derived step by step (Study 24)
Writer: ALG-A (§1–§4, §6–§10); EIN-A (§5, merged verbatim). Verifiers: ALG-B / EIN-B (s24/AGREE_ALG.md).
Draft opened Tue Nov 10 14:59 UTC 2026 (`date -u`). Base text: s17/GRAND_UNIFICATION.md (GU; merged and signed by CUBE-A and CUBE-B;
§00–§11, AGREE table, circularity rows X1–X36). This document adds step-by-step derivations, small exact worked examples, and
one label on every line. It makes NO new physical claim: anything not in a signed file or an exact check below is marked OPEN.

**The owner's demand (14:50 UTC, verbatim brief s24/README_STUDY.md):** no circularity, no fakes; only the tensor plus a start
from the seed; all the algebra clear; why the physics converges to Einstein; how the clocks work; why everything fits; how to
build the rank-4 (or rank-5) tensor.

**Labels (exactly one per line).**
| label | meaning |
|---|---|
| THEOREM | proved from the law (proof here, or in the signed file cited) |
| NUMERIC | an exact integer computation (package or ALG-A's own scripts; file named) |
| DERIVED | a short derivation from theorems/numbers above it, not separately signed |
| CHOSEN | an input, a convention or data (it could have been otherwise) |
| NEW LAW | an extension the owner approved or that is proposed; changes the law's content |
| OPEN | not established; no signed source or exact check |
| POSTED | put in by hand (a schedule, a hold); EXCLUDED from the picture by the binding owner rule of 14:43 |
| TUNED | a coefficient fitted to make something work; NOT adopted (binding owner rule 14:43) |

**Evidence of ALG-A (all exact integers; read-only on the package; `nice -n 19`, one core), in s24/ALG-A_work/:**
gear_demo.py/.out/.json (a Rule3 gear by hand), flip_check.py/.out (remainder flip, Q odd), energy_check.py/.out (two-time
energy identity), block_u1_listing.py/.out (one block built by the package builder), block_example.py/.out/.json (recount of
the package default as it stands now), h00_readers.py/.out (who reads the lapse), remerge_s5.py (merges EIN-A's §5 verbatim).

**OWNER DECISIONS relayed by the manager (message stamped 15:40 UTC; received by ALG-A at 15:25 UTC by `date -u`; binding here).**
| # | decision | where | label |
|---|---|---|---|
| O1 | RANK 4 IS FINAL ("solve everything with it"); rank 5 was considered and rejected per s23/AGREE_R5.md | §3 (recipe), §3.11 | CHOSEN |
| O2 | "The bangs are not supposed to return — information is not lost — a bang starts with a new seed": one exact CPT bang; each later turn of the cosmic clock starts a NEW seed (the state at the turn, with all its records); echoes are data, not the goal | §9.3–§9.4 | CHOSEN |
| O3 | "There is no freeze on the board: light is the executor of the clicks, and when a path is chosen only it produces the click"; the zero-time hold is dropped from the picture | §8 | CHOSEN |

---------------------------------------------------------------------------------------------------------------------
## §0 THE WHOLE THING IN TEN LINES
1. [CHOSEN] Space is the periodic cube (Z/LZ)³, L ≥ 3; every site holds the same list of gears; a gear holds (a, b, r).
2. [CHOSEN] One divisor D = 6Q; one integer tensor u (rank ≤ 4: at most three factors from v = (1, b, a), node + one face).
3. [THEOREM] One update, Rule3: ℓ, r′ = divmod(2u + r, D); a′ = b; b′ = ℓ − a — an exact bijection (§1.3).
4. [CHOSEN] One seed: the vacuum (0, 0, 3Q−1) everywhere plus a few non-vacuum integers; each later turn of the cosmic clock
   starts a new seed, the full state at the turn (owner O2; §9).
5. [THEOREM] Every gear is a clock: b(t+1) + b(t−1) = 2u/D + ε exactly, |ε| < 1, i.e. M b(t) + ε for the linear part; a mode
   with eigenvalue μ of M ticks at cos w = μ/2 (§4).
6. [THEOREM] A click is a carry of the remainder: ℓ(t) = b(t+1) + b(t−1), and D·Σℓ = ΣK + r(0) − r(T) exactly (§4).
7. [THEOREM] For the reciprocal part of the tensor (17,729 of the 18,553 live monomials) Rule3 is the discrete Euler–Lagrange
   equation of L(x, y) = Φ(x) + Φ(y) − D x·y, and there rank = degree of Φ; reciprocity itself is a CHOSEN design rule, checked by
   the package; the 706 designated and 118 two-time monomials are not gradients (§1.7, §3.2, §3.5).
8. [THEOREM] The node is 2O (48 channels) over Z[i]: left = frame/spin, right = internal; mirrors = the outer automorphism (§2).
9. [DERIVED] Einstein's kinematics (one cone, given the one chosen stencil; an exact EP FACTOR in the tensor for every clock that
   reads the lapse — in the live FIX-i default only the dark board L0 reads it at rest, while the visible Dirac pair's rest clock
   neither feels nor sources it: a declared first-order EP debt; a γ = 1 weak-field metric via the CHOSEN link factor 1 − 4U, the
   1911 control giving γ = 0; local rotations) is in the tensor as the continuum limit of exact integer identities; the dynamics
   is a NEWTONIAN-LEVEL sourced scalar lapse + designated one-way parts; the full Einstein equations are NOT reproduced, because
   Rule3 forbids by theorem an exact Bianchi identity and an exactly conserved reciprocal source (§5, EIN-A).
10. [CHOSEN] What the cube fixes are FORMS (groups, sectors, hands, splits, cones); 3, L, Q, the weights and the seed are inputs (§10).

---------------------------------------------------------------------------------------------------------------------
## §1 THE LAW
### 1.1 The three ingredients
- [CHOSEN] Space: Λ = (Z/LZ)³, L ≥ 3, six face neighbours x ± e_d (d = x, y, z). — GU §0 A1.
- [CHOSEN] Gears: a finite list 𝒢 of gear types, the same at every site; each gear holds (a, b, r) ∈ Z × Z × {0, …, D−1}. — GU §0 A2.
- [CHOSEN] Divisor: D = 6Q for every gear; the package value is Q = 2^33 + 1 (odd: forced GIVEN a mirror-fixed vacuum, §1.6, X30). — GU §0 A2; layers/system.py.
- [CHOSEN] Tensor: for the gear of type g at node x,
  u_g(x) = Σ_{monomials m with target g} c_m · Π_{f ∈ m} v_f(x + o_f),  v_f ∈ {b, a} of some gear type, at most 3 factors,
  offsets o_f ∈ {0, ±e_x, ±e_y, ±e_z}, all offsets of one monomial on ONE node or ONE face link (B3); c_m ∈ Z. — core/tensor.py docstring.
- [CHOSEN] Rank: rank = 1 + (max number of factors) ≤ 4 ("v = (1, b, a)" counts the constant slot). — GU §5.1.
- [CHOSEN] The input of Rule3 is K = 2u (so K is always EVEN; this is used in §1.6). — core/engine.py l.5.

### 1.2 The update (Rule3), from ONE complete snapshot
- [CHOSEN] For every gear of every node at once:  (ℓ, r′) = divmod(K + r, D),  a′ = b,  b′ = ℓ − a. — GU §0 A4; AGENTS rule 6–7.
- [CHOSEN] divmod is floor division: K + r = D·ℓ + r′ with 0 ≤ r′ < D (Python semantics, also for negative K). — core/engine.py.
- [THEOREM] Two-line consequence (used everywhere below): since a(t+1) = b(t), b(t+1) = ℓ(t) − a(t) = ℓ(t) − b(t−1), i.e.
  **ℓ(t) = b(t+1) + b(t−1)**, and D·ℓ(t) = K(t) + r(t) − r(t+1). — AGREE_CC A2(a) (s13).

### 1.3 Why Rule3 is a bijection (the exact inverse)
- [THEOREM] Given the NEW snapshot (a′, b′, r′) everywhere, the OLD one is recovered uniquely, stage by stage: — s8 AGREE_B A1; engine.inverse_step.
  - (i) old b = a′ for every gear (Rule3 copies b into a).
  - (ii) for a gear whose u reads only b's (stage 0), K = 2u(old b) is now known;
  - (iii) K + r = D·ℓ + r′ with 0 ≤ r < D fixes r = (r′ − K) mod D uniquely, then ℓ = (K + r − r′)/D;
  - (iv) old a = ℓ − b′.
  - (v) a gear whose u reads the a of other gears (a "two-time read") is done after those gears (stage s reads a only of
    stages < s); this needs the a-read graph to be ACYCLIC (§3.6).
- [THEOREM] Nothing in (i)–(v) uses the sign or the time-independence of the coefficients, so the bijection holds for every
  coefficient sign, for time-dependent and even gear-valued coefficients. — s8 AGREE_B A1 ("rewind exact even through a runaway to > 2^87").
- [NUMERIC] The package default (375 gear types) was run 4 updates forward and 4 back from random ±2^10 data on L = 3: the start
  state returns exactly. — GU §5.4 (CUBE-B gu_rewind.json).
- [NUMERIC] The live FIX-i default (375 gear types, 18,553 monomials) rewinds exactly too (L = 3, ±2^10, staged inverse step by
  step). — s24/ALG-B_work k1237_rule3.json (K1).
- [NUMERIC] ALG-A's gears (§1.4, §4): inverse exact in every run (1-gear and 2-gear boards, 20,000 updates). — ALG-A_work/gear_demo.out.

### 1.4 A Rule3 gear run by hand (exact; the smallest example)
- [CHOSEN] One gear, u = 12·b (a pure "mass" term), Q = 5, D = 30, so cos w = 12/30 = 0.4; start at (a, b, r) = (0, 1, 14),
  i.e. the vacuum remainder 3Q−1 = 14 and one unit of b. — ALG-A_work/gear_demo.py.
- [NUMERIC] The run (K = 2u = 24b):

| t | a | b | r | K | ℓ = carry | check ℓ = b(t+1) + b(t−1) |
|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 14 | 24 | 1 (14+24 = 38 = 30 + 8) | 1 = 1 + 0 |
| 1 | 1 | 1 | 8 | 24 | 1 (8+24 = 32 = 30 + 2) | 1 = 0 + 1 |
| 2 | 1 | 0 | 2 | 0 | 0 | 0 = −1 + 1 |
| 3 | 0 | −1 | 2 | −24 | −1 (2−24 = −22 = −30 + 8) | −1 = −1 + 0 |
| 4 | −1 | −1 | 8 | −24 | −1 (8−24 = −16 = −30 + 14) | −1 = 0 + (−1) |
| 5 | −1 | 0 | 14 | 0 | 0 | 0 = 1 + (−1) |
| 6 | 0 | 1 | 14 | | (the start again: period 6) | |

- [NUMERIC] Checks on this run: the click identity holds at every t, the ledger D·Σℓ = ΣK + r(0) − r(T) holds, the inverse
  returns the start, and |ε| = |r(t) − r(t+1)|/D ≤ 1/5. — gear_demo.out.
- [DERIVED] Reading: the remainder r walks 14 → 8 → 2 → 2 → 8 → 14 on the circle Z_30; every time it wraps, ℓ = ±1 is emitted
  (a "click"), and that ℓ becomes the next b (b′ = ℓ − a). The gear is a clock whose ticks ARE its carries (§4).

### 1.5 The vacuum
- [THEOREM] At a = b = 0 every monomial with ≥ 1 factor vanishes; the default tensor has NO degree-0 monomial (census: 0
  constants), so K = 0, ℓ = 0, r′ = r: (0, 0, r) is a fixed point for every r. — GU §0 A5; census gu_census2.json; ALG-A recount §3.9.
- [CHOSEN] The package puts EVERY gear at r = 3Q−1 ("one vacuum"). Why this value: §1.6. — layers/system.py (l0_offset = Q−1).
- [DERIVED] At r = 3Q−1 and even K the first carry is symmetric: up-click iff K ≥ 3Q+1; down-click iff K + 3Q−1 < 0, i.e.
  (K even, 3Q odd) K ≤ −(3Q+1). The vacuum remainder is the centre of the phase circle.

### 1.6 Why Q is odd (the remainder flip)
- [CHOSEN] The package's remainder flip: R′(r) = D−2−r for even r, D−r for odd r (an involution of {0, …, D−1}). — core/reversors.py.
- [THEOREM] Lemma (the primitive commutes with the flip): for EVEN K, if (ℓ, r′) = divmod(K + r, D) then
  divmod(−K + R′(r), D) = (−ℓ, R′(r′)). Proof: K even ⇒ r′ ≡ r (mod 2); even r: −K + D−2−r = D(−ℓ) + (D−2−r′) with
  0 ≤ D−2−r′ < D; odd r: −K + D−r = D(−ℓ) + (D−r′) with 1 ≤ D−r′ < D. ∎ — GU §3.3; ALG-A flip_check (all even K ∈ [−4D, 4D], Q = 1…12).
- [THEOREM] By the same one-line computation, the time mirror M′(a, b, r) = (b, a, R′(r)) is an exact reversor (M′FM′F = id) of
  every b-only tensor with even K; by the lemma, the sign flip Jp(a, b, r) = (−a, −b, R′(r)) is a symmetry of every tensor ODD in v (it is a building block of the CPT reversor R*,
  not a symmetry of the default, which has degree-2 terms). — s8 AGREE_B A1; core/reversors.py; flip_check (2000/2000).
- [THEOREM] Fixed points: R′(r) = r ⇔ (r even and r = 3Q−1) or (r odd and r = 3Q). 3Q−1 is even and 3Q is odd exactly when Q
  is odd. So: **a vacuum remainder fixed by the exact mirror exists ⇔ Q is odd**, and then the fixed set is {3Q−1, 3Q}. — GU §3.3, X30; CUBE-B gu_flip.json.
- [THEOREM] The plain mirror r ↦ D−1−r has no fixed remainder at all (D even). — flip_check.out.
- [NUMERIC] Q = 1, 3, 5, 7, 9, 11: fixed sets {2,3}, {8,9}, {14,15}, {20,21}, {26,27}, {32,33}; Q = 2, 4, …, 12: empty. — flip_check.out.
- [CHOSEN] Asking for a mirror-fixed vacuum is the input that forces "Q odd" (the CPT reversor R* needs it); the VALUE 2^33+1 is chosen. — GU X30.

### 1.7 Why forces are gradients: Rule3 as a discrete Euler–Lagrange equation
- [THEOREM] Take L(x, y) = Φ(x) + Φ(y) − D·x·y and the action S = Σ_t L(b(t), b(t+1)). Then
  ∂S/∂b(t) = [∇Φ(b(t)) − D b(t−1)] + [∇Φ(b(t)) − D b(t+1)] = 0  ⇔  D·(b(t+1) + b(t−1)) = 2∇Φ(b(t)) = 2u = K.
  Rule3 is exactly this equation with the integer rounding carried by the remainder: D·(b(t+1) + b(t−1)) = K + r − r′.
  — s11 AGREE_CL2 row 1 (found independently by CL-2A and CL-2B; converse ∂x∂yL ≡ −D·1).
- [THEOREM] The kinetic coefficient is the ONE number D for every gear; a-reads and one-way (designated) terms are never
  variational. — AGREE_CL2 row 1.
- [CHOSEN] Rule3 runs with ANY integer u (§1.3), so reciprocity is NOT forced by Rule3: it is a design rule. A reciprocal block is
  ONE integer potential Φ with u = ∂Φ/∂b (action = reaction); §3 is the recipe for writing Φ; anything not of that form must be
  declared one-way (§3.5). — ALG-B mark A5/A31.
- [NUMERIC] In the live default 17,729 b-only undesignated monomials pass the reciprocity checker (0 violations, 0 missing
  partners); 706 designated and 118 two-time (a-read) monomials are outside it (17,729 + 706 + 118 = 18,553). — s24/ALG-B_work k9_reciprocity.json, k9b_two_time.json.

### 1.8 What never writes to the state (readings)
- [CHOSEN] CLICK = ℓ ≠ 0 with a state change; CLOCK = an eigenmode of the linear part; inverse/rewind = audit only. — GU §0; AGENTS 9–11.
- [CHOSEN] No monomial reads r (v = (1, b, a) only); r enters only its own gear's divmod. — GU §0 (CUBE-B R2).

---------------------------------------------------------------------------------------------------------------------
## §2 THE NODE
### 2.1 The groups of the cube
| object | order | role | label |
|---|---|---|---|
| O ≅ S4 (cube rotations) | 24 | spatial symmetry of (Z/LZ)³; = Inn(2O) | THEOREM |
| O_h = O × {±1} | 48 | = Aut(2O): mirrors act on the node as its OUTER automorphism θ (Galois √2 ↦ −√2) | THEOREM |
| 2O (binary octahedral, unit quaternions of the cube) | 48 | the 48 channel labels of the dark board; one involution z = −1 (2π turn) | CHOSEN (labels) |
| 2T ⊃ Q8 ◁ 2O; 2O/Q8 ≅ S3 | 24, 8, 6 | Q8 = lifts of the three half-turns | THEOREM |
- [THEOREM] Sources: s17 AGREE_CUBE B1, E1, N1; GU §1.1.
- [THEOREM] All characters of 2O, O, O_h, S3 are real, so no U(1) and no complex 3 come from the cube. — GU §1.1; GU-1B Thm 1.
- [THEOREM] As a real algebra R[2O] = R² ⊕ M2(R) ⊕ M3(R)² ⊕ H² ⊕ M2(H): real and quaternionic blocks only (dimension check
  1+1+4+9+9 = 24 integer spin, 4+4+16 = 24 half-integer spin). The node natively makes SU(2)s, never U(1) or SU(3). — GU §1.1; AGREE_CL3 row 3.
- [THEOREM] |2O| = 24·|Z| and |Aut(2O)| = 24·|Out| with the same central Z2: "48 = 48" is structural. — GU §1.7.

### 2.2 The dark board L0 = R[2O]: ports
- [CHOSEN] Channel g at x reads the channel g·B_u at x + d with sign s_u, u = R(g)⁻¹d; B_{±x} = 1, B_{±y} = q_y^{±1},
  B_{±z} = q_z^{±3}: the body actions (0, 1, 3); signs s = (1, −1, 1) (the "handed class"). — GU §1.3; AGENTS item 5.
- [THEOREM] The twist class {0, ±¼} is forced by "connected + exact mirror"; the lift (0, 1, 3) inside it is chosen. — GU §11.5; AGREE_CUBE.
- [THEOREM] Φ_L0 = Q Σ b(x)ᵀP b(x+e) = 3QΣ|b|² − (Q/2)Σ_links |b(x) − P b(x+e)|²; at k = 0 the hop is right multiplication by
  β = Σ_u s_u[B_u] ∈ Z[2O]. — GU §1.3.
- [THEOREM] LEFT action = frame/spin (exact only with the spatial rotation); RIGHT = internal: the ports' exact commutant is
  right Q8 × {±1} (an exact internal SU(2) skeleton). 384 proper lifts h·g·k and 384 improper lifts h·θ(g)·k, for all 8 sign
  triples. — GU §1.3; AGREE_CUBE C2, C3, E2, N1 (two codes).

### 2.3 Why D = 6 (reference) and why the handed board is massive
- [DERIVED] With K = 2u and u = Σ (six ports, unit weights) b, the k-space operator M = 2W/D has eigenvalues μ = 2λ/D, so
  cos w = λ/D (§4.2). Stability needs |λ| ≤ D for every mode; the flat class reaches λ = 6 (all six ports in phase at k = 0),
  so D = 6 is the smallest stable divisor. — GU §1.7, X30 (given K = 2u); AGREE_CUBE A2.
- [THEOREM] In the handed class max|λ| = 2 + 2√3 ≈ 5.464 < 6, so every L0 mode is massive: cos w ≤ 0.911, w ≥ 0.4255
  (THEOREM S). — GU §1.3; v6 THEOREM S.
- [DERIVED] On the package's L0 (D = 6Q, ports ±(Q−1), on-site 6): cos w = ((Q−1)λ + 6)/(6Q) at U = 0. — GU §1.3 (CUBE-B gu_ref.json).

### 2.4 The matter block and the one orientation bit
- [CHOSEN] Massive first-order Dirac matter: real structure H ⊗ R² ⊗ (internal Cⁿ, i = J′); transports P_d = L_d ⊗ σz. — GU §1.4.
- [THEOREM] P_d² = −1 and the P_d anticommute; ω = PxPyPz commutes with every P_d and ω² = Px²·(PyPzPyPz) = (−1)(−1) = +1.
  So ω is central with square 1: Cl(0,3) = H ⊕ H has exactly two central idempotents ½(1 ± ω). **Γ5 = −PxPyPz**. — GU §1.4, §6.1; AGREE_CUBE Part IV.
- [THEOREM] Γ5 is NOT the product of the mirrors: the true mirrors M_d = L_d ⊗ σx multiply to −W0 (parity = the mass matrix),
  which anticommutes with Γ5. — GU §6.1, X1.
- [THEOREM] Four commuting i's: J (right i: the clock carrier), J′ (the charge ring), Γ5J, V = JJ′. Weak hand Π_W = ½(1 − Γ5V). — GU §1.4.

### 2.5 The node in one line, and what it does NOT give
- [THEOREM] Z[i][2O] acted on from both sides: LEFT = frame/spin (Einstein's local rotations), RIGHT = internal (isospin Q8 on
  L0; the clock J and Kramers K on matter); z = −1 = (−1)^F glues them; one algebra from two sides, never one connection. — GU §1.6; AGREE_GU1 B9.
- [THEOREM] The internal axis triple splits 1 + 2 (cos w = {1/3} vs {0, 2/3} on the reference engine); a connected node never
  gives 1+1+1. It is bosonic and isospin-distinct, so it is NOT the families. — GU §1.3 (1+2 law); AGREE_CUBE N2.
- [THEOREM] Integer gauge cores from Z[i]: U(n, Z[i]) = Z4 ≀ S_n; Z4 (U(1)), Q8 = SU(2, Z[i]), Δ96 (SU(3)). — GU §1.2; GU-1B Thm 4.
- [THEOREM] Q odd (given a mirror-fixed vacuum) and the one vacuum (0, 0, 3Q−1) belong to the node's arithmetic: proofs in §1.5–§1.6. — GU §3.3, X30.

---------------------------------------------------------------------------------------------------------------------
## §3 HOW TO BUILD THE TENSOR — a recipe someone could follow
### 3.0 What the tensor is, as data
- [CHOSEN] A tensor = an ordered list of gear TYPES + a list of MONOMIALS. A monomial = (target, integer coeff, ≤ 3 factors);
  a factor = (gear type, offset ∈ {0, ±e_x, ±e_y, ±e_z}, field ∈ {a, b}). — core/tensor.py (module docstring).
- [CHOSEN] Gear metadata (name, readout label official/audit, Yee link axis, documented field sign) never enters the
  dynamics; the engine sees only integer arrays. — core/tensor.py GearType; core/engine.py docstring.
- [THEOREM] The builder REJECTS: > 3 factors (rank > 4), a non-integer coefficient, a B3-illegal offset set (LocalityError),
  a cycle of a-reads (AcyclicityError), a one-way entry without a written reason, two different Q. — core/tensor.py (_parse,
  check_locality, inverse_stages, _designation, compose).

### 3.1 Step 1 — blocks
- [CHOSEN] A block = gear types (local names) + terms + vacuum remainders + parameters + the Q it was built with.
  `compose(*blocks)` qualifies names "<block>.<gear>", allows cross-block references by qualified name, merges equal
  monomials (coefficients added) and enforces ONE Q. — core/tensor.py Block, compose.
- [NUMERIC] The package default composes 21 blocks: ref 48/336, su2 40/709, su3 168/5,163, u1 20/233, matter 16/208,
  em 4/834, metric 10/70, lapse 0/0, beta 1/14, bgk 1/2, lapseL0 0/1,728, arm1 3/3, arm2 3/3, router 2/18, gate 1/2,
  exit 2/18, matter2 16/208, wsu2 36/537, chiral 4/7,131, ehop 0/232, gwb 0/1,152 (gear types / terms). — ALG-A_work/block_example.out.
- [THEOREM] Every block is a TENSOR block: no detector, `if`, clock or erased remainder is in the law (AGENTS 6–8); the
  readers act only through monomials. — GU §5.3.

### 3.2 Step 2 — write ONE integer potential Φ per reciprocal block; rank = degree of Φ
- [THEOREM] For a reciprocal block: if Φ is a polynomial of degree n in the b's, each force u_t = ∂Φ/∂b_t has degree n − 1, so
  rank = 1 + max deg u = n (designated and two-time entries carry their degree directly). **Rank 2 = quadratic Φ (linear force); rank 3 = cubic Φ; rank 4 = quartic Φ (cubic force).** — GU §6.6 criterion; §1.7 above.
- [DERIVED] What each rank buys (all from the package):
  - rank 2 (Φ quadratic): inertia, masses, ports, hops through a fixed vacuum — ref (L0), matter, metric, bgk, arm1/2, gate;
  - rank 3 (Φ cubic = one field × a bilinear): a matter hop THROUGH a dynamic link κ⟨ψ, Uψ′⟩, a lapse dressing F·|ψ|²,
    the Higgs hop — lapseL0, ehop, gwb, beta, router;
  - rank 4 (Φ quartic): the OD4 link spring −(λ/4)(|U|² − A²)² — su2, su3, u1, wsu2, chiral; plus designated rank-4 entries
    in em and exit. — GU §5.3b (per-block rank table, gu_census3.json).
- [THEOREM] Three separate link factors on one hop would be degree 5 > 4, so the rank bound forces ONE unified link per face per
  multiplet (Burnside at rank 3). — GU §2.2; AGREE_CL3 row 17; AGREE_GU1 A8/B5.

### 3.3 Step 3 — deviation form about the vacuum (static vacuum, integer coefficients)
- [CHOSEN] Store the deviation X̃ = X − X0 (so the vacuum gear holds b = 0) and use
  Φ̃(X̃) = Φ(X0 + X̃) − D·X0·X̃ − const. — layers/gauge.py deviation_terms.
- [THEOREM] Why the −D·X0·X̃: the constant history X(t) = X0 solves Rule3 iff D·2X0 = 2∂Φ/∂X at X0; subtracting D·X0·X̃
  removes exactly that linear term, so u(vacuum) = 0 and the vacuum is a fixed point (§1.5). — layers/gauge.py (asserted: "no linear term").
- [THEOREM] The builder raises if a linear term survives (vacuum not static) or if any u-coefficient is not an integer
  ("integer grain": the binding constraint behind several walls, e.g. route (c), GU §5.6b). — deviation_terms.

### 3.4 Step 4 — B3 locality (node + six faces)
- [CHOSEN] Every monomial lives on ONE node or ONE face link: its offsets (target at 0) lie in {0, e} for a single face
  direction e. Edge (1,1,0), diagonal (1,1,1), long (2,0,0) offsets and a monomial touching both +e and −e are rejected. — core/tensor.py check_locality.
- [CHOSEN] The gear of the link (x, x + e_k) is stored at its base node x (Yee metadata; the engine ignores it). — core/tensor.py.
- [THEOREM] Cone theorem: one update moves influence by at most one face, so the state at x after t updates depends only on
  the seed inside the L1 ball of radius t (this hard taxicab cone is wider than the wave cone c_Q ≈ 0.577). Board-causal
  no-signalling is therefore a THEOREM of the law. — GU X36; s20 AGREE_ZT ("connected" in the cone sense).
- [NUMERIC] The stricter "physical support" diagnostic (a link gear spans its link) flagged 3,300 monomials in the 13:43
  composition; it is NOT the binding rule and is NOT claimed. — GU §5.2.

### 3.5 Step 5 — reciprocal versus designated (one-way) terms
- [THEOREM] Reciprocal: the b-only part satisfies u_t = s_t·∂Φ/∂b_t for ONE translation-invariant Φ, i.e. the Jacobian is
  symmetric (action = reaction). The checker is exact (Fractions): every potential class implies one coefficient φ_P and every
  partner monomial must be present with exactly s_g·n_g·φ_P. — core/reciprocity.py.
- [CHOSEN] Designated: an entry flagged {"designated_one_way": "<reason>"}; it is excluded from the check and must carry a
  non-empty written reason. Price: Newton III fails for that coupling, and it is never variational. — core/tensor.py; AGREE_CL2 row 1.
- [NUMERIC] The smallest designated entry of the default (block bgk, 2 terms): u[metric.h00] += −1·b[bgk.B], reason "R-a: the
  declared uniform k = 0 background … B holds its value and does not feel F (data, one-way)". — layers/system.py l.272–277.
- [NUMERIC] Default census: 706 designations, by degree 1/2/3 = 7/297/402. The 1,930 degree-3 monomials = 1,528 reciprocal
  (all inside OD4-spring blocks: 48 + 1,404 + 12 + 48 + 16) + 402 designated (em 384 + exit 18, AUDIT C-6's two allowed
  places). — GU §5.3b; ALG-A recount (degree-3 and designation counts unchanged by FIX-i).
- [OPEN] Which of the 706 designations sit in the "allowed places" row by row is not census-verified. — GU §5.4.

### 3.6 Step 6 — staging of the a-reads (two-time reads)
- [THEOREM] A factor "a" reads b(t−1). The inverse (§1.3) recovers a gear's old a only after its K is known, so a gear may
  read the a of gears in EARLIER stages only: the a-read graph must be acyclic; a self-a-read is a cycle and is rejected. — core/tensor.py inverse_stages.
- [NUMERIC] The default has 3 inverse stages: stage 0 = 358 gear types (read no a); stage 1 = em.Phi (the Lorenz accumulator,
  which reads the a of the A links); stage 2 = the 16 matter gears X0–X7, Y0–Y7 (which read the a of Phi and of A). — ALG-A_work/block_example.out; layers/em.py l.143–185.
- [THEOREM] An oscillator cannot be paused by its own input: the pause would need ℓ = a + b of the gear itself, a self-a-read. — AGREE_INTEGRATED IB7 (s13).

### 3.7 Step 7 — compose, then run the ten checks
- [CHOSEN] Checklist, each with its package tool: (1) one Q; (2) rank ≤ 4; (3) B3; (4) acyclic a-reads; (5) reciprocity
  report (0 violations on undesignated b-only terms); (6) no degree-0 monomial and no linear term (vacuum fixed); (7) rewind
  exact; (8) the reversor R* exact on a seed; (9) an all-k Bloch scan of the linear part (|λ| ≤ 1 for the companion matrix);
  (10) integrality at the chosen Q and amplitudes. — core/tensor.py, core/reciprocity.py, core/engine.py, core/reversors.py; GU X27, X27b.
- [THEOREM] Checks 1–8 are kinematic: they do NOT imply a bounded history. — GU §5.6, X22.
- [NUMERIC] Check 9 is the test that separates exactly the configurations that ran away (found first in bang runs) from those
  that stayed bounded: with gwb's norm bilinears the k = 0 companion eigenvalue was λ = 1.1381 (cos w = (λ + 1/λ)/2 = 1.0084 > 1), the corner (π,π,π) λ = −1.026; FIX-i (λ_H = λ_L = 0) is marginal at k = 0 and at every L = 6 k checked, corner included. — GU §5.6b; s18 AGREE_STAB R9.

### 3.8 The kinds of rank-4 (degree-3) terms
| kind | form | status today | label |
|---|---|---|---|
| OD4 spring | −(λ/4)(\|U\|² − A²)² on one link (route B adds the \|det V\|² matrix spring) | the ONLY reciprocal rank-4 kind in the default (1,528 monomials) | NUMERIC |
| narrow kind (decision 4) | "uncharged singlet × gauge-covariant rank-3 composite"; excludes link × composite | approved design rule; not used in the default | NEW LAW |
| plaquette kind (v8 item 3) | "the product of the FOUR links around one elementary plaquette, NO matter factor", + a det-shadow link Re(d̄·det V) (rank 3) | APPROVED 14:37 for route B (ONE v2); not built | NEW LAW |
| designated rank-4 | the E1 dressed source (em, 384) + the gated one-shot exit (18) | the two allowed places | NUMERIC |
- [THEOREM] Wording guard: "link × staple" WITHOUT "no matter factor" would make two links per hop legal again and undo
  Burnside's one-link forcing. — GU §6.2b; AGREE_GU1 A8.
- [THEOREM] Why the plaquette kind is needed for one light: every gauge-invariant product of group-valued links closes a loop
  of ≥ 4 links (link × staple), which the narrow kind excludes; so compact links have no curvature stiffness and run at
  0.13–0.21 (the mixed route-B photon at ≈ 0.88 c_Q). — GU §2.5, §6.2b; s19 ONE_LIGHT_FINALS T3.
- [OPEN] B3 for the plaquette: its four links reach the diagonal node, so it must be built through 2-path relay gears (s19
  "plaquette relays"; O1 open), and whether its corner counter-term is structural or TUNED must be declared when it is built. — s19 l.20–39.

### 3.9 The census of the default, counted
| quantity | GU census 13:43 (before FIX-i) | ALG-A recount 14:55 (package now: FIX-i since 14:45) | label |
|---|---|---|---|
| gear types G | 375 | 375 | NUMERIC |
| monomials | **18,623** | **18,553** (gwb 1,222 → 1,152 terms) | NUMERIC |
| rank | 4 | 4 | NUMERIC |
| by degree 0 / 1 / 2 / 3 | 0 / 2,343 / 14,350 / 1,930 | 0 / 2,329 / 14,294 / 1,930 | NUMERIC |
| node / link monomials | 3,487 / 15,136 | 3,447 / 15,106 | NUMERIC |
| designations (one-way) | **706** | **706** (7 / 297 / 402 by degree 1/2/3) | NUMERIC |
| inverse stages | 3 | 3 (358 / 1 / 16 gear types) | NUMERIC |
| Q | 2^33 + 1 | 2^33 + 1 | CHOSEN |
- [NUMERIC] Sums: 2,329 + 14,294 + 1,930 = 18,553; 3,447 + 15,106 = 18,553; 2,343 + 14,350 + 1,930 = 18,623. — block_example.out; GU §5.2.
- [NUMERIC] The recount's dynamics fingerprint b51d3f2c…cbfc8e8 equals the one ONE-A recorded when applying FIX-i (14:45:16),
  where ONE-A also records "monomials 18,623 → 18,553, designations 706 → 706". — research/metric_variant_v1/NOTES_system.md l.745–751.
- [DERIVED] So "375 / 18,623 / 706" is the census of the hands-ON default as composed at 13:43; the package default with FIX-i
  is 375 / 18,553 / 706. Rank, B3, stages, Q and the 706 designations are unchanged.
- [NUMERIC] ONE v1 (layers/one.py: the FIX-i package + the 7-gear WIND cosmic block) = 382 gear types per node, 18,592
  monomials, 736 designations, rank 4 (18,592 − 39 cosmic terms = 18,553); route-B ONE v2 would be 444 gear types. Counted
  independently by both Study 26 twins. — s26/AGREE_CH.md A1, A2 (signed, closed 15:20).
- [NUMERIC] Coupling graph of ONE v1, at gear level: the connected physical core has 127 gear types (ref 48, matter 16,
  matter2 16, wsu2 36, em 4, chiral 4, metric.h00, beta, bgk); 255 of 382 lie outside it = su2, su3, u1 (228; they read nothing
  and are read by nothing) + 9 uncoupled metric gears + the 11 reader gears + the 7 cosmic gears (separate components). — s26/AGREE_CH.md A4 (REFINE, CH-B B1); CHANNELS.md v2 §0 item 4.
- [THEOREM] Block SIZES are forced as the minimal real module of each sector's algebra (+ B3 relays): Dirac pair 16 (R⁸ × C(J′)),
  links V⊗V* (SU(2) 4, SU(3) 18, U(1) 2, U(2) 8), metric 10 = Sym²R⁴, L0 48 = the regular module of 2O; the CONTENT and the
  TOTAL are chosen (no principle forces the total). — s26/CHANNELS.md v2; AGREE_CH.

### 3.10 Worked example: one block, from Φ to its monomials (package builder, tiny integers)
- [CHOSEN] Compact U(1) layer, Q = 5 (D = 30), link vacuum A = 2, hop κ = 1, mass m = 4, spring λ = 1, no 2-path gears.
  Gear types per node: ψ_re, ψ_im (a Gaussian-integer matter field) and U_k,re, U_k,im for k = x, y, z (links at the base node).
  — ALG-A_work/block_u1_listing.py (calls layers/gauge.py build_gauge read-only).
- [CHOSEN] The potential (⟨z, w⟩ = Re(z̄w); U = A + W in deviation form):
  Φ = κ Σ_k ⟨ψ(x), U(x,k) ψ(x+e_k)⟩ + (m/2)|ψ|² + (D/2) Σ_k |U_k|² − (λ/4) Σ_k (|U_k|² − A²)².
- [NUMERIC] Result: 8 gear types, 77 monomials, rank 4, degrees 0/20/45/12, node/link 29/48, 1 stage (b-only), vacuum
  remainder 14 = 3Q−1, reciprocity checker: 77 checked, 0 violations, 0 missing partners. — block_u1_listing.out.
- [NUMERIC] The 7 monomials of the radial link gear U_x,re (verbatim from the builder):
  - 22·W_re
  - 1·ψ_re(0)·ψ_re(+e_x)   and   1·ψ_im(0)·ψ_im(+e_x)
  - −6·W_re²   and   −2·W_im²
  - −1·W_re³   and   −1·W_re·W_im²
- [DERIVED] Each coefficient by hand. |U|² − A² = 2A·W_re + W_re² + W_im², so the spring is
  −(λ/4)(2A W_re + W_re² + W_im²)² and its W_re-derivative is −2λA²W_re − λA(3W_re² + W_im²) − λ(W_re³ + W_re W_im²):
  - degree 1: D − 2λA² = 30 − 8 = **22** (inertia minus the spring's stiffness);
  - degree 2: −3λA = **−6** and −λA = **−2**; the hop gives ∂/∂W_re Re(ψ̄ W ψ′) = ψ_re ψ′_re + ψ_im ψ′_im, times κ = **1**;
  - degree 3: −λ = **−1**, twice (this is the rank-4 part: a quartic Φ gives a cubic force).
- [NUMERIC] The angular link gear U_x,im has 6 monomials: 30·W_im, −1·ψ_re(0)ψ_im(+e_x), +1·ψ_re(+e_x)ψ_im(0), −4·W_re W_im,
  −1·W_re² W_im, −1·W_im³ (degree-1 coefficient D = 30: no spring stiffness along the angle). — block_u1_listing.out.
- [NUMERIC] The matter gear ψ_re has 19 monomials: 4·ψ_re(0) (the mass), 2·ψ_re(±e) for the six faces (κA = 2: the hop through
  the vacuum link) and 12 degree-2 hop-through-W terms such as 1·ψ_re(+e_x)·W_re(0) and −1·ψ_im(+e_x)·W_im(0). — block_u1_listing.out.
- [THEOREM] Reciprocity visible by eye: U_x,re reads 1·ψ_re(0)ψ_re(+e_x), and ψ_re reads 1·ψ_re(+e_x)·W_re(0) (and, from the link
  at x − e_x, 1·ψ_re(−e_x)·W_re(−e_x)): both are derivatives of the ONE potential term κ ψ_re(x) W_re(x) ψ_re(x+e_x). — reciprocity.py; listing.
- [DERIVED] What the block DOES, read off as clocks (§4.2): the radial link ticks at cos w = 22/30, i.e. 4 sin²(w/2) = 16/30 =
  4λA²/D exactly (w = 0.7476; the GU's "radial ω² = 4λA²/D" is this law); the angular link has cos w = 30/30 = 1, a massless
  zero mode (the holonomy direction); matter ticks at cos w(k) = (4 + 4Σ_d cos k_d)/30 ∈ [−8/30, 16/30]: a massive, stable clock. — GU §2.1.

### 3.11 Rank 5 — considered and rejected (owner decision O1 in the box above: RANK 4 IS FINAL)
- [CHOSEN] The owner fixed the rank at 4 ("solve everything with it"); §3.0–§3.10 is therefore the complete recipe. — O1 (box).
- [NUMERIC] Why rank 5 was rejected (s23/AGREE_R5.md): the candidate "Θ × any approved covariant rank-4 term" lifts only ONE
  wall, the lapse × link × matter hop, and only to an approximate echo (0.0033, against no echo at rank 4); THEOREM O is a
  parity law, not a rank law, so every cubic coupling stays non-folding at any rank; and the zero-time hold cannot emerge at
  ANY rank (no b-only rule of any degree, 16/16 conflicts). Its costs: an unbounded-below two-way term (quintic potential) and
  a ~19× smaller usable amplitude at the package's Q (6,553 → 350). — AGREE_R5 A1, A2, B1, C2, C3 (signed by both twins; R5-B final 15:22:48).

---------------------------------------------------------------------------------------------------------------------
## §4 HOW THE CLOCKS WORK
### 4.1 The leapfrog (forced, not chosen)
- [THEOREM] From §1.2: b(t+1) + b(t−1) = ℓ(t) = (K(t) + r(t) − r(t+1))/D = 2u(t)/D + ε(t), with ε(t) = (r(t) − r(t+1))/D and
  |ε| ≤ (D−1)/D < 1. — GU §3.1; v6 A.4.
- [THEOREM] Write u = H b + (higher order) about the vacuum; then **b(t+1) + b(t−1) = M b(t) + ε(t) + O(b²)**, M = 2H/D. This is a
  leapfrog (Störmer–Verlet) step of length 1 with the ONE kinetic coefficient D (§1.7). With a-reads the linear map is the
  companion [[2H_b/D, 2H_a/D − I], [I, 0]]. — GU §3.1, §4.3.
- [NUMERIC] max|ε| in ALG-A's runs: 1/5 (unit orbit), 4/5 (D = 30, A ≥ 10), 998/1001 and 142/143 (D = 6006): always < 1. — gear_demo.out.

### 4.2 Eigenmodes: cos w = μ/2
- [THEOREM] If M e = μ e, then b(t) = A cos(wt + φ) e solves the linear part iff 2cos w = μ, i.e. **cos w = μ/2**. — GU §3.1.
- [THEOREM] |μ| < 2: a clock; μ = 2: w = 0 (massless; a zero mode drifts linearly); μ = −2: w = π (the doubler); |μ| > 2: growth
  (companion eigenvalue λ with λ + 1/λ = μ). — GU §3.1, §5.6b.
- [THEOREM] Translation invariance makes M block-diagonal in k (Bloch): every block has a dispersion cos w(k) = μ(k)/2. On L0:
  cos w = λ/6 (reference), ((Q−1)λ + 6)/(6Q) (package). — GU §1.3.
- [NUMERIC] Two gears, D = 6006, u1 = 2400 b1 + 600 b2 (and symmetric): predicted rates arccos(3000/6006)/2π = 0.16676 and
  arccos(1800/6006)/2π = 0.20156; measured (zero crossings, 20,000 updates, A = 10⁷) 0.16675 and 0.20155. — gear_demo.out.

### 4.3 Mass = the rest rate
- [THEOREM] A mode's mass is its k = 0 rate w0 (radians per update), cos w0 = μ(0)/2; a lone gear u = m·b has cos w0 = m/D. — GU §3.1; s21 AGREE_MASS ("mass = the rest click rate").
- [NUMERIC] The package's Dirac pair: mass coefficient m = 4915·2^22 at D = 6(2^33+1), m/D = 0.39998. Its BOARD rate is
  arccos(m/D) = 1.159 rad (0.18451 per update), which includes the π/2 carrier of a first-order clock; its OWN-FRAME (R2) rest rate,
  the continuum mass, is arcsin(m/D) = 0.4115 rad (0.0655 per update). For a second-order clock (carrier 0, e.g. L0 form C or the
  lone gear below) the board rate is the rest rate. — layers/system.py docstring (MASS_DEFAULT); ALG-B mark T2; GU §3.5.
- [NUMERIC] ALG-A, u = 12b at D = 30 (cos w = 0.4, w/2π = 0.18451): measured rate 0.18460 at amplitude 10, 0.18450 at 10³ and
  10⁶; at amplitude 1 the orbit is exactly period 6 (rate 1/6): small amplitudes LOCK to rationals, so a gear shows its rest
  rate only with amplitude ≫ 1. — gear_demo.out; system.py (R-P1/R-P2 rounding lock).
- [THEOREM] The NUMBERS of the masses are data (Yukawa integers); the cube forces only multiplets and pairings. — s21 AGREE_MASS; GU §10.

### 4.4 Click = carry; remainder = phase
- [THEOREM] r′ = (r + K) mod D: the remainder is a phase register on the circle Z_D, advanced by K every update; ℓ counts how
  many times it passes through 0 (a carry). A CLICK is ℓ ≠ 0 together with a change of the gear's triple (the engine's
  official click stream, §1.8). — §1.2; GU §0 readings; core/engine.py.
- [THEOREM] **ℓ(t) = b(t+1) + b(t−1)**: a detector's own b is the zero-lag record of its clicks; for amplitude A ≫ 1,
  ℓ(t) = 2cos w · A cos(wt + φ) + O(1). — AGREE_CC A2(a); SYSTEM_DESIGN_v8 l.2359.
- [THEOREM] ε = (r − r′)/D is exactly what the integers cannot hold; the remainder carries this sub-integer phase to the next
  update, so nothing is rounded away (this is WHY Rule3 is a bijection, §1.3). — §1.3.
- [NUMERIC] §1.4's table: r walks 14 → 8 → 2 → 2 → 8 → 14 and the carries are 1, 1, 0, −1, −1, 0. — gear_demo.out.

### 4.5 The ledger
- [THEOREM] Summing D·ℓ = K + r − r′ over t < T telescopes: **D·Σ_{t<T} ℓ(t) = Σ_{t<T} K(t) + r(0) − r(T)** for every gear. — GU §3.2; AGREE_COSMIC E4.
- [NUMERIC] Exact in every ALG-A run (1- and 2-gear boards, up to 20,000 updates). — gear_demo.out.

### 4.6 Born from fresh remainders
- [THEOREM] For 0 ≤ K < D: #{r ∈ Z_D : K + r ≥ D} = K, so with a uniform remainder P(carry) = K/D exactly; collapse = the
  remainder falls in one arc (r′ < K exactly when the carry fires). — s12 AGREE_GU4 row 2.
- [NUMERIC] D = 30: the count equals K for all 30 values of K; one shared remainder on a circle split into arcs (6, 10, 14)
  exits exactly once, 6 / 10 / 14 times over the 30 remainders. — gear_demo.out.
- [THEOREM] With inputs proportional to |ψ|² the click probability is |ψ|²/Σ|ψ|² (Born); the LINK chooses (one shared
  remainder, one overflow, P(both) = 0). — GU §10.
- [DERIVED] P(none) = 1/Q at odd Q (a falsifiable prediction, not measured). — GU §10.
- [OPEN] Freshness: Born is exact only for a FRESH uniform remainder; re-reading one circle gives the Fréchet joint
  P11 = max(0, 2p − 1) and Sturmian (not √n) noise. Freshness is OPEN. — AGREE_GU4 rows 5, 6; GU X10.
- [THEOREM] Odd-Q parity: K even and D/2 = 3Q odd, so no event has probability exactly 1/2, 1/4 or 3/4. — AGREE_INTEGRATED IB6; s23 R5-B P3 (0 half-events at Q = 1, 3, 5).

### 4.7 Board time versus click time; the own-frame tick rule (R2)
- [THEOREM] Board time t = the number of Rule3 updates, the same for every gear (one snapshot). — §1.2.
- [CHOSEN] R2 (read-only observation rule, ruling 11:43): one tick = one sign cycle of the click sizes in the clock's OWN rotating
  frame (carrier removed: θ = π/2 for the Dirac pair, θ = 0 for L0 form C). — GU §3.5; SYSTEM_DESIGN_v8 l.2359.
- [THEOREM] Under a lapse a clock's rate obeys the half-angle law sin(w/2) = √(1 − 2U)·sin(w0/2) (L0 form C, exact symbol; N ≈ 1 − U);
  first-order matter in the R1 form (hands OFF) obeys cos w = (1 − U)·cos w0 on the board, i.e. sin w_R2 = (1 − U)·sin w0,R2 for
  the own-frame rate w_R2 = π/2 − w. A clock in a deeper potential ticks
  slower per board update: time dilation is a rate change (details §5.1b, §5.2). — GU §3.4 (THEOREM M2-7); AGREE_M_final rows 5a/5b.
- [NUMERIC] In the live FIX-i default the Dirac rest clock carries NO lapse factor (Δu_matter = 0 exactly under a uniform lapse),
  and the Dirac rest energy sources h00 by exactly 0; its on-site entry is the BARE m + 6w = 27,057,455,104 on all 16 matter
  gears: the declared EP debt is first order. — s24/ALG-B_NOTES.md K5d, K5e; EIN-A row EIN-26; s18 AGREE_STAB.
- [THEOREM] A confirmation gate would make click time differ from board time; an enable-only gate changes WHEN clicks happen,
  not WHAT they are (S = 5/4 exactly). It is NOT part of the law. — AGREE_BELL C1–C2; GU §3.6.

### 4.8 Charges and energy as clocks see them
- [THEOREM] Board charge J_X = Σ D b(t−1)·X b(t); Ĵ_X = J_X/D is an integer changed only by remainder kicks; the click charge is
  the board charge × 4cos²w (= μ²). — GU §3.7 (THEOREM M2-2).
- [THEOREM] For a linear symmetric part H, the two-time energy E = D|b|² + D|a|² − 2aᵀHb changes ONLY by remainder kicks:
  E(t+1) − E(t) = Σ_x (r_x − r′_x)(b′_x − a_x). Proof: insert 2Hb = D(b′ + a) − (r − r′) into E′ − E; all D-terms cancel. — s12 AGREE_GU2 B3.
- [NUMERIC] ALG-A: 0 failures in 12,000 updates on 40 random symmetric boards (n ≤ 5 gears, Q ∈ {1, 3, 5, 1001}). — energy_check.out.

### 4.9 The universe as one clock
- [THEOREM] A bounded orbit of the bijection is exactly periodic; if it contains a state fixed by a reversor it has exactly one
  more symmetric moment, at half the period (THEOREM P). — s8 AGREE_B C1.
- [THEOREM] Two exact symmetric moments make a history exactly periodic, so a growing history has at most ONE exact bang
  (THEOREM D). — s12 AGREE_GU2 C5.

---------------------------------------------------------------------------------------------------------------------
<!-- BEGIN §5 (EIN-A, merged verbatim from s24/EIN_SECTION5.md by ALG-A) -->
## §5 WHY IT CONVERGES TO EINSTEIN (exactly what, in what limit, and what not)
Writer: EIN-A (Study 24). Draft opened Tue Nov 10 14:51:10 UTC 2026; written 15:00–15:05; EIN-B's 10 EDITs applied 15:26 UTC (`date -u`). Verifier: EIN-B
(rows EIN-1 … EIN-26 in s24/AGREE_ALG.md). One label per line: THEOREM / NUMERIC / DERIVED / CHOSEN / NEW LAW / OPEN /
POSTED / TUNED. "NUMERIC (EIN-A)" = my own check this hour, under s24/EIN-A_work/ (scripts + JSON). The package was only read.
Source abbreviations:
- GU = s17/GRAND_UNIFICATION.md (merged, signed).
- SD7 / SD8 = s0/SYSTEM_DESIGN_v7.md / v8.md.
- MF / PF / P1 = research/metric_variant_v1/review/AGREE_M_final.md / AGREE_P_final.md / AGREE_P_stage1.md (all signed).
- ST = s10/AGREE_ST.md; CL2 = s11/AGREE_CL2.md; AUD = s12/AUDIT.md; STAB = s18/AGREE_STAB.md; M7 = s7/AGREE_M.md.
- GRAV / UNIV / HYB = research/metric_variant_v1/NOTES_gravity.md / NOTES_universality.md / NOTES_gravity_hybrid.md
  (builder notes; their numbers count as signed only where a row of P1/PF/MF/ST cites them).
- Clock notation (leapfrog b(t+1) + b(t−1) = M b(t) + ε, cos w = μ/2, mass = rest rate, half-angle law) is §4.2/§4.3/§4.7.

**The answer in four lines.**
1. Kinematics: in the continuum limit the tensor reproduces Einstein's weak-field kinematics, as the limit of exact
   integer identities. This covers:
   - the metric g00 = −(1 − 2U), g_ij = (1 + 2U)δ_ij, with PPN γ = 1 following from the CHOSEN link factor c_link = 1;
   - one cone c_Q² = (Q−1)/(3Q) (given the CHOSEN common stencil);
   - the EP for every clock that reads the lapse (live default: at rest only the dark L0; the visible Dirac pair neither feels nor sources it);
   - local Lorentz symmetry at O(k²).
2. Dynamics: the lapse is a NEWTONIAN-LEVEL sourced scalar wave, obeying a discrete Poisson law.
   - γ is kinematic (a chosen reader factor), not lapse dynamics.
   - β = 1 needs the hands-OFF β read.
   - In the live default the lapse is sourced by L0, the singlet-half hop and bgk, not by the visible Dirac rest mass.
   - One-way (designated) terms come on top.
3. Theorems of Rule3 itself FORBID the two pillars of Einstein's field equations: an exactly conserved reciprocal source,
   and an exact Bianchi identity.
4. So the full Einstein equations are NOT reproduced, and "converges EXACTLY to Einstein" is not a true statement. §5.6
   gives the true one.

### 5.0 The objects (what "gravity" is on the board)
- The lapse field F is the b-counter of the gear metric.h00, and U := F/(2P) with P = 2^20. A clock that reads it gets the
  factor (1 − 2U) on its mass (on-site) entries and the factor (1 − 4U) on its link (transport) entries. A first-order
  clock takes half of each: 1 − U and 1 − 2U. Both factors come from one potential:
  Φ_int = −(F/P)·Φ_site − ((F(x) + F(x+e))/P)·Φ_link. [CHOSEN (approved law); GRAV design item 3; GU §4.0]
- The action (metric → matter) and the source (matter → metric) are the two derivatives of the SAME Φ_int. So
  "feels gravity" ⇔ "sources gravity", and Newton III is exact. This holds for every UNDESIGNATED lapse term (lapseL0,
  gwb). [THEOREM; CL2 row 13; live reciprocity checker 17,729 checked, 0 violations: NUMERIC (EIN-B k9_reciprocity.json)]
  - Designated exceptions: em's 192 h00 reads feel without sourcing; bgk sources without feeling. [NUMERIC (EIN-B k8)]
- Source = ∂Φ_int/∂F = the reading clocks' one-time (b-only) mass + gradient energy. [THEOREM (by construction); CL2 row 13; ST S7]
- Who reads metric.h00 in the LIVE default (hands ON + FIX-i, owner decision v8-1 14:37)? [NUMERIC (EIN-A), pkg_cone_check.json]
  - readers: ref (L0, form C) 1,104 terms; matter 384 and matter2 384 (the FIX-i singlet-half hop); em 192 (degree-3,
    designated source dressing only); beta 7 monomials (14 h00 factors: G's source ∝ Lap(F²) has two), designated;
    lapseL0 and gwb reads are reciprocal (degree 2) [NUMERIC (EIN-A), pkg_h00_terms.json];
  - sources: lapseL0 624, gwb 384, bgk 1.
  - Comparison with the signed hands-OFF census (ref 1,104; Dirac 992; em 384):
    - ref 1,104 is unchanged;
    - em 384 = 192 reading h00 + 192 reading β;
    - the Dirac pair's hands-OFF reads (mlapse/mbeta) are replaced by the FIX-i hop reads (matter 384 + matter2 384).
    [PF A1; MF row 1a; GU §4.3; NUMERIC (EIN-A)]
- The other nine metric gears (h0x, h0y, h0z, hxx, hyy, hzz, hxy, hxz, hyz) have 0 readers and 0 sources outside the metric
  block. They are free waves only (§5.5f). [NUMERIC (EIN-A), pkg_cone_check.json]
- The β gear (beta.G) is read only by em (192, source dressing) and by itself (7). So in the live default NO clock reads β.
  [NUMERIC (EIN-A), pkg_cone_check2.json]

### 5.1 The lapse on the board → the weak-field metric (continuum limit), γ = 1, one cone
**(a) One cone: the exact stencil.**
- Every metric gear and E1's A_d have the ONE headroom stencil u = (Q−1)·Σ_6 b(x+e) + 6·b(x): the 10 metric gears and
  A_x, A_y, A_z. [NUMERIC (EIN-A), pkg_cone_check.json: on-site 6, six neighbours at exactly Q − 1 = 8,589,934,592, for all 13 gears]
- Exceptions:
  - beta.G uses stencil B (on-site 3Q + 3, faces (Q−1)/2, c² = (Q−1)/(6Q): the GRAV-FIX A detuning), so β is off the cone.
  - em.Phi is an accumulator (on-site D, faces 3Q).
  [NUMERIC (EIN-B k8); GU §4.3]
- All 48 L0 channels have the same magnitudes: on-site 6, six ports of |weight| Q − 1 (signed by the 2O ports).
  [NUMERIC (EIN-A), pkg_cone_check2.json: 48/48 channels, 288/288 ports]
- Plane-wave symbol: m(k) = 6 + 2(Q−1)·Σ_d cos k_d, and cos w = m/D with D = 6Q (§4.2). Hence, EXACTLY:
  cos w = 1 − c_Q²·Σ_d (1 − cos k_d), with c_Q² = (Q−1)/(3Q). At k = 0, m = D, so cos w = 1: massless.
  [THEOREM (exact algebra); EIN-A ein_limits.json C1 (sympy identity True)]
- Continuum (k → 0): w² = c_Q² k² − (c_Q²/12)·Σ_d k_d⁴ + (c_Q⁴/12)·(k²)² + O(k⁶).
  The k⁴ term contains Σ k_d⁴, which is cubic but not rotation-invariant. So isotropy, and hence the light cone, holds at
  O(k²) only. [DERIVED; EIN-A ein_limits.json C1]
- At the default Q = 2^33 + 1: c_Q² = 8589934592/25769803779 and c_Q = 0.5773502691560 (1/√3 − O(1/Q)). [NUMERIC (EIN-A)]
- c_Q is the supremum of this band's group velocity, approached as k → 0 from below. Along [100], [110] and [111]
  (k ≤ 2, 60-digit mpmath) the max of v_g − c_Q is −1.2e-6, −3.0e-7 and −7e-17. In 1-D, v_g falls monotonically
  (0.447 at k = π/2). It is the wave front, not a hard bound.
  - Near k = 0 in EVERY direction n: the k⁴ coefficient is (c²/12)(c² − Σn_d⁴) ≤ (c²/12)(c² − 1/3) = −(Q−1)/(108Q²) < 0,
    so v_g < c_Q.
  [DERIVED (all directions, O(k⁴)) + NUMERIC (3 directions; EIN-A vg_check_mp.json; EIN-B k45_fast.json)]
- The hard causal bound of any B3 update is one face per update (taxicab speed 1 along an axis). [THEOREM (locality); GRAV D4 note]
- That hard B3 cone is WIDER than c_Q ≈ 0.577. So the law alone does not exclude influence outside the c_Q cone
  (precursors, other gears). Law-level no-signalling is board-causal (B3 cone), not c_Q-causal. [THEOREM (locality); EIN-B EIN-6]
- Measured: [111] front 0.57735 at Q = 1025 (the same as the EM front), 0 hard-cone violations; metric/light/EM evolution
  bit-identical in R-P2's code. [NUMERIC; P1 D9 AGREE]
- One cone, shared by the metric gears, the E1 photon and L0 form C. [THEOREM given the CHOSEN common stencil (GU X16) + NUMERIC-pkg; GU §4.1 E-1; SD7 §4.1]
  - For L0 this means the same symbol coefficient c_Q² in 4sin²(w/2) = c_Q²·eig(M0 + T(k)), not an L0 light.
  - The handed default L0 has NO massless band: M0 is positive definite, with minimum eigenvalue 4 − 2√3 = 0.536.
  [NUMERIC; PF A2; EIN-B k4d_m0_spectrum.json]
- NOT on the cone:
  - Compact-link waves are slower by theorem: c < 1/2 < c_Q. [THEOREM; GU §2.5]
  - One light on c_Q with exact Gauss is impossible under the current rules. [THEOREM; GU §2.5, s19 ONE_LIGHT finals]
  - Putting all field gears on stencil B keeps one cone but lowers it to c² = (Q−1)/(6Q). [DERIVED; OPEN design; ST S21]

**(b) The lapse-dressed Rule3 dispersion (exact symbol).** Take a static uniform U and a second-order clock (KG-type,
carrier D) whose transport sits on the headroom weights:
- 1 − cos w = (1 − 2U)·σ + (1 − 4U)·c_Q²·Σ_d (1 − cos k_d), where σ = 1 − cos w0 is its rest term.
  [THEOREM (the tensor's factors); GRAV item 3]
- Form C for L0, exact symbol at k = 0 on all 9 distinct bands: u = Dv − (Q−1)(1 − 2U)·M0·v. Hence the half-angle law
  sin(w/2) = √(1 − 2U)·sin(w0/2), with M0 and 8 − M0 positive definite. [THEOREM (exact LDLᵀ, symbol); MF row 5a AGREE]
- Form C on the LIVE default (hands ON + FIX-i), at every k:
  - Write the symbol as u = A(k)v + F0·B(k)v, where A comes from the 336 ref terms and B from the 1,104 F×L0 lapseL0 terms.
  - The exact Gaussian-integer identity P·B(k) = D·1 + A(0) − 2A(k) holds.
  - This is u = Dv − (Q−1)[(1 − 2U)·M0 + (1 − 4U)·T(k)]v: clock factor 1 − 2U on the mass M0 and link factor 1 − 4U on
    the difference transport T(k), exactly.
  - Checked at 64 k-points (quarter turns per axis): 147,456 entries, 0 failures. No other term targets L0.
  [NUMERIC (EIN-A), pkg_formC_check.py/.json, 15:05:11]
- First-order (Dirac pair, R1, Wilson difference form): u = (1 − U)·m·W0·v + (1 − 2U)·T(v), where T = hops + Wilson.
  At k = 0: cos w = (1 − U)·cos w0. In the own frame: sin w = (1 − U)·sin w0. [THEOREM; MF row 5b AGREE (432/432 rows)]

**(c) Continuum limit → metric.**
- Limit taken: w0 ≪ 1, |k| ≪ 1 (scales ≫ one node), U ≪ 1, and U slowly varying (eikonal: |∇U| ≪ |k|·U).
- Expanding (b): w² = (1 − 2U)·m² + (1 − 4U)·c_Q²·k² + O(w⁴, k⁴, U²), with m² = 2σ.
- Compare with the eikonal of a field of mass m in g00 = −(1 + 2Φ), g_ij = (1 − 2γΦ)δ_ij/c_Q², i.e.
  g^{μν}k_μk_ν + m² = 0: w² = (1 + 2Φ)·m² + (1 + 2(1 + γ)Φ)·c_Q²·k² + O(Φ²).
- Matching at first order gives Φ = −U and γ = 1. With the 1911 control (link factor 1 − 2U) the same match gives γ = 0.
  [DERIVED; EIN-A ein_limits.json C2: sympy solve → {γ: 1}; control → {γ: 0}]
- So, in the continuum and weak-field limit: g00 = −(1 − 2U), g_ij = (1 + 2U)δ_ij. This is the weak-field GR metric with
  Newtonian potential Φ = −U and PPN γ = 1, at first order in U. γ = 1 is the output of the CHOSEN c_link = 1.
  [CHOSEN ⇒ DERIVED]
- **Why γ = 1 comes out, in one line.** The site term reads the lapse at its one node: 1 − F(x)/P = 1 − 2U. The link term
  reads it at BOTH end nodes: 1 − (F(x) + F(x+e))/P = (1 − F(x)/P)(1 − F(x+e)/P) + O(U²).
  - So link factor = (clock factor)² at first order.
  - In metric language, −g00/g_ii = (−g00)² is exactly isotropic γ = 1 (g_ii = 1/(−g00) at O(U)).
  - The 1911 control reads only the average of the two ends (c_link = ½), so it gives γ = 0.
  - So γ = 1 follows from the CHOSEN reading "a link carries the FULL lapse of both its ends" (c_link = 1). B3 equally
    permits the average.
  [CHOSEN ⇒ DERIVED (first order in U); GRAV item 3; EIN-A C2]
- In this reading "clock 1 − 2U / link 1 − 4U" are the metric components (−g00) and (−g00/g_ii). In lapse form:
  N = √(1 − 2U) ≈ 1 − U, and the light speed factor is √(1 − 4U) ≈ 1 − 2U. [DERIVED; SD8 ch.2 §3]
- First-order (Dirac) R1 gives the same metric: H = (1 − U)βm + (1 − 2U)c_Q α·k, so H² = (1 − 2U)m² + (1 − 4U)c_Q²k² + O(U²).
  [DERIVED; EIN-A C3: difference 0 at O(U)]
- PPN β (second order in g00):
  - The β gear relaxes to G = F²/(2P) (static). The matter clock read 1 − F/P + G/P = 1 − 2U + 2U² then gives β = 1.
    [DERIVED; EIN-A C4 → β = 1; GRAV item 4]
  - That read is DESIGNATED one-way. [CHOSEN (designated); P1 D6]
  - It exists only with hands OFF (mbeta). In the live hands-ON default no clock reads β (§5.0), so β = 1 is lost for
    matter. [NUMERIC (EIN-A) + GU E-2; AUD O-8]
- Measured: E1-type light under a uniform lapse: (1 − cos w) ratio 0.9599990983 against the law 1 − 4U0 = 0.9599990845.
  Speed factor 0.97980 = √(1 − 4U0), so γ = 1 at first order.
  [NUMERIC (one builder; UNIV U2 photon, candidate, default OFF); SD8 ch.2 §3]
- L0 form C: massless speed ratio √(1 − 4U); massive bands sin(w/2)/sin(w0/2) = √(1 − 2U).
  [DERIVED + NUMERIC two codes; SD7 row "FORM C in the official reading"]
- Scope: the uniform-U symbol is exact; the metric reading is a continuum, first-order statement. [DERIVED]
- The strong field does NOT follow GR:
  - Where the clocks stop depends on the species.
    - The Dirac clock's linear lapse 1 − U vanishes at U = 1, while GR's √(1 − 2U) vanishes at U = ½.
    - L0's exact factor √(1 − 2U) vanishes at U = ½, like −g00.
    [DERIVED; AUD C-7: MECHANISM; EIN-B EIN-12]
  - L0's link factor 1 − 4U flips sign at U = ¼ and the board blows up. [NUMERIC; GU §4.3]

### 5.2 The equivalence principle
- **EP in the tensor (exact).** Every lapse-reading mass entry of a given order gets the same factor, as an integer
  identity. Example, a first-order rest clock: 2P·u(F0) = (2P − F0)·u(0), i.e. the factor 1 − U.
  - L0 form C: all 9 bands obey sin(w/2) = √(1 − 2U)·sin(w0/2). [THEOREM; MF 5a]
  - The live tensor carries the form-C factors at every k (§5.1b). [NUMERIC (EIN-A), pkg_formC_check.json]
  - Dirac pair (R1, hands OFF): cos-ratio N_rest = 1 − U, with the link factor exact on every entry. [THEOREM; MF 5b]
  - Gauge-layer "site" form (default OFF): exact, T1 0 mismatches. [NUMERIC; UNIV T1]
- **EP of observed clock rates (from clicks):**
  - D2 universality 4.79e-5 (builder); R-P2 G5(i) 6e-11 (frozen MECHANISM lapse). [NUMERIC; P1 D2 AGREE]
  - L0 − Dirac gap −5.05e-5 at U = 0.01, as predicted. [NUMERIC-pkg; SD7 §4.1; GU E-2]
- **What "exact" means here.** The FACTOR is exact. The observed tick ratios differ between species at O(U·w0²): the
  lattice-scale redshift of §5.3e, which is a PREDICTION.
  - As w0 → 0 every species reads the same N, but at FIRST order in U only.
  - At O(U²) they differ. L0 gives √(1 − 2U) = 1 − U − U²/2; Dirac gives 1 − U, and 1 − U + U²/2 with the hands-OFF β read.
  - So the EP of observed rates is a continuum, first-order statement.
  [DERIVED; EIN-A C5; EIN-B EIN-13]
- **Hands ON (default since 13:22), with FIX-i (owner decision v8-1, 14:37, applied in the package 14:45:16):**
  - compose_electroweak removes the matter lapse blocks mlapse/mbeta (744 + 496 terms). [NUMERIC census; GU E-2; STAB R8]
  - FIX-i builds gwb with lam_H = lam_L = 0 and keeps only the singlet-half hop. [CHOSEN (coefficient level, not a new law); STAB R9; NOTES_system v8-1]
  - Then (EP debt, DECLARED):
    - the doublet's rest clock has no lapse factor. The BARE on-site m + 6w = 27,057,455,104 is still on all 16 Dirac
      gears, undressed, and so are the Yukawa × Higgs terms. Under a uniform U = ±1/128 the live Dirac rest input changes
      by exactly 0 (hands OFF: −U·m·W0·b). The debt is FIRST order in U; GU E-2's "adiabatic O(U²)" predates FIX-i.
      [NUMERIC (EIN-B k5d_dirac_rest_clock.json)]
    - the visible Dirac rest mass does not source the lapse: its rest-energy source into h00 is exactly 0 (hands OFF
      7,308,428,060). [NUMERIC (EIN-B k5e_sources.json)]
    - the doublet half of the transport has no lapse factor;
    - only the singlet-half hop keeps one;
    - the doublet's mass and the W/Higgs energies do not source the lapse.
    [OPEN (declared debt); STAB side-by-side "EP for the doublet" + joint result; EW-BUILDER recommendation]
  - Checked on the live tensor:
    - all 768 lapse reads into the doublet (matter 384 + matter2 384) are gwb hop (link-type) terms of degree 2;
    - there are 0 on-site (mass-type) lapse reads;
    - the doublet's on-site terms carry no lapse factor: its own 16 + 16, Yukawa × Higgs 128 (chiral), em 176.
    [NUMERIC (EIN-A), pkg_fixi_ep_check.py/.json, 15:06:22]
  - Restoring form C on the doublet ("Bc + L3 hop") makes EP R1-exact, but it breaks SU(2) at O(U) through the bare-mass
    dressing. [DERIVED; STAB R17]
  - In the live default the EP is therefore exact only for L0 (form C).
- **Other permanent EP defects:**
  - Gauge-layer matter does not read the lapse in the default (η = 1). [NUMERIC-pkg; PF A1; CL2 row 12]
  - The OD4 spring energy can never gravitate at rank ≤ 4 (degree count): spring-bound states carry a small permanent EP
    defect. [THEOREM (degree count); the defect itself is DERIVED, not measured; CL2 row 16]

### 5.3 Observable tests, with the package's numbers
**(a) Gravitational redshift.**
- Derivation: a STATIC lapse makes the update time-translation invariant, so each normal mode keeps its board frequency.
  Clocks at x tick at N(x) in their own frame (§5.1c). So the received frequency ratio is N(x_e)/N(x_r), and
  z = U_e − U_r + O(U²). [DERIVED; CL2 row 19 (static offset invisible; changing U visible as N(t_e)/N(t_r))]
- Clock slowing read from clicks:
  - builder D1: |N_click/N_lapse − 1| ≤ 2.92e-5 (MECHANISM load, sourced field);
  - R-P2 G1: law 3.8e-11, click = event 3e-12 (frozen lapse).
  [NUMERIC; P1 D1 AGREE]
- Redshift via light:
  - With a static MECHANISM field it is exact: Z_click = Z_event to 2e-7. That PASS is POST-HOC geometry (L = 18). The
    registered L = 16 run FAILED by 0.25 % (a torus resonance) and is kept as a FAIL. [NUMERIC; P1 D3 REFINE (agreed), G-x]
  - With the package's own sourced field it FAILS (z off by 34 %), because that field is not static (§5.5e).
    [NUMERIC; P1 D3; builder D8d]

**(b) Light bending (2× the Newtonian/1911 value).**
- Derivation: for light, n = c_Q/c_local = (1 − 4U)^{−1/2}, so n − 1 = 2U + 6U². With the 1911 control,
  n − 1 = U + (3/2)U². [DERIVED; EIN-A C6]
- For U = u0/r and impact parameter b: α_GR = ∫∂_b(n − 1)dz = 4u0/b and α_1911 = 2u0/b. Ratio exactly 2 at first order.
  [DERIVED; EIN-A C6 (sympy integral)]
- Package status:
  - No deflection run exists. [OPEN; P1 D5 "NOT RUN" AGREE; SD7 §4.2]
  - In the live default no massless field reads the lapse (E1 reads gravity only through its source dressing; L0 has 0
    massless bands), so bending has no carrier. [NUMERIC-pkg; PF A2/J4 AGREE]
  - The U2 photon lapse (candidate, OFF) gives the local factor √(1 − 4U) (§5.1c), but Gauss stays exact only for a
    uniform lapse. [NUMERIC; UNIV T4b–T4d]
  - Exact Gauss + bending at E1's stencil is impossible. [THEOREM, exact over Q; UNIV T5]
  - The 2-path route bends nothing (trajectory bit-identical). [NUMERIC; UNIV T7c]
  - So bending is an owner choice: bending with a Gauss ledger, or exact Gauss with flat light. [OPEN; SD8 ch.2 §5]

**(c) Shapiro delay.**
- Derivation: the excess delay is ∫(n − 1)dz. The GR/1911 ratio is 2 at first order, and 2 + 3U for a uniform slab at
  second order. [DERIVED; EIN-A C6]
- Measured with test light (MECHANISM for the default, PF J4):
  - weak field (U = 0.02, D2c): GR/1911 = 2.087–2.109, PASS;
  - R-P2 G3 (L = 96): 2.054 / 2.067 against R-P2's 2.0645 including second order;
  - the registered strong-field D2 FAILED (2.61 / 2.57), likely a readout artefact (a wrapped slab reflection).
  [NUMERIC; P1 D4 AGREE]

**(d) The Newtonian limit: Poisson for the lapse.**
- Static field: b(t±1) = b(t), r static ⇒ u = D·b ⇒ (Q − 1)·ΔF = −s(x), where Δ is the 6-neighbour lattice Laplacian.
  With Φ = −U = −F/(2P): ΔΦ = s/(2P(Q − 1)) ≡ 4πGρ (the board's Poisson law).
  [DERIVED (exact for remainder-static data); EIN-A]
- In general the per-update flux identity holds exactly with the remainder ledger:
  D·Σ_B(b⁺ + b⁻ − 2b) = 2(Q − 1)·flux_B + 2·S_B + Σ_B(r − r′).
  [THEOREM (identity); P1 D7 "exact Gauss identity (G6)"; EIN-A ein_k0_gauss.json: 0 failures in 360 box checks]
- Field built by the board from F = 0:
  - slope −1.0018 (r = 3…11);
  - F·r·4π(Q − 1)/S = 1.001–1.007;
  - Gauss −(Q − 1)·flux/S = 1.0002–1.0008 (box half-widths 4, 6, 8).
  [NUMERIC; P1 D7 SINGLE (R-P1)]
- Slow-particle limit of §5.1c: ω ≈ m + c_Q²k²/(2m) − m·U. So the potential energy is V = −m·U, independent of species
  among the lapse readers, and bodies fall toward larger U, i.e. toward the load. [DERIVED]
- Measured free fall:
  - direction: inward (sign PASS);
  - magnitude: click vs event FAIL (12 %); R-P2 0.52 / 0.69 of the lattice prediction.
  [NUMERIC; P1 D8: OPEN in both codes; ST S18 OPEN]
- β = 1 (hands OFF): β_click = 1.0059, control −0.0009. Marginal FAIL on |β_click − β_event| ≤ 0.005 (measured 0.0065).
  [NUMERIC; P1 D6 SINGLE]

**(e) The own-frame tick rule R2 and the lattice-scale redshift (a PREDICTION).**
- R2: one tick = one sign cycle of the click sizes in the clock's OWN rotating frame. The carrier θ is fixed by the law:
  π/2 for the Dirac pair, 0 for L0 form C. Board eigenvalue = click sign cycles to 4.3e-7 (27 lapse values × 2 species).
  [THEOREM (identities) + NUMERIC two codes; SD7 CLICK→CLOCK; read-only rule]
- From the exact laws of §5.1b:
  - form C: δ/U = −w0²/12 + O(w0⁴), from w = 2·arcsin(√(1 − 2U)·sin(w0/2));
  - Dirac: δ/U = −w0²/3 + O(w0⁴), from w = arcsin((1 − U)·sin w0);
  - here δ := (w/w0)/√(1 − 2U) − 1.
  [DERIVED; EIN-A ein_limits.json C5]
- Hence δ/(U·w0²) → −1/12 (L0) and −1/3 (Dirac), matching the signed prediction. [NUMERIC (verified in two codes, GU E-11); SD7 §4.1]
- Exact tick ratios at U = 0.01, against GR's √(1 − 2U) = 0.98995:
  - handed default L0 bands μ = 4 − 2√3 = 0.536 / 2 / 4 + 2√3 = 7.464 (the top band): 0.98980 / 0.98932 / 0.98593;
  - μ = 8 is the +++ top band, not a handed band: 0.98527 (the SD8 value).
  [NUMERIC (EIN-A; EIN-B EIN-19); SD8 ch.2 §4]
- Default Dirac: δ = −6.0e-4 at U = 0.01 (reads 1 − 1.06U). [NUMERIC; SD7 §4.1]
- Meaning: GR's redshift is recovered for slow clocks (w0 → 0). The w0² term is a falsifiable lattice-scale departure.
  [DERIVED (a falsifiable prediction)]

### 5.4 Local Lorentz symmetry
- **Rotations = the frame.** Local rotations are the LEFT action of 2O, combined with the spatial rotation. This is
  exact and discrete. Spin ½ is exact (Kramers T² = −1), and the 2O labels are exact superselection labels.
  [THEOREM; GU §4.4, E-10]
- On the chiral half the frame acts through SL(2, C_{J′}), and the weak hand is its J′-self-dual half. There is no
  graviweak single connection. [THEOREM; GU §4.4; AGREE_CL3 row 22]
- **Boosts and SO(3).** These are not node symmetries (2O contains rotations only, and the lattice is cubic). Exact SO(3)
  and exact boosts are FORBIDDEN. [THEOREM; GU F-3]
- They EMERGE at O(k²): the dispersions of §5.1 are Lorentz-invariant at second order. Lattice corrections are O(k⁴)
  (the anisotropic Σk_d⁴ term) and O(w0²) (§5.3e). [DERIVED; EIN-A C1]
- **The frame connection.** c1 (dynamic frame links, Z[2O] per link) is NOT adopted. In Einstein–Cartan the spin
  connection is slaved, and its integer 2O image rounds to the vacuum below about 45° per link. So L0's frame links stay
  FIXED, which is the EC-consistent remnant. [DERIVED; M7 U6-3, M2-12 AGREED; SD8 row c1; GU §2.3]
- **Frame dragging.**
  - The shift gears h0i exist but are neither sourced nor read (§5.0). [NUMERIC (EIN-A)]
  - A reciprocal h0i ↔ current coupling meets an E1-type (Peierls) no-go. [DERIVED warning; CL2 row 23 OPEN; ST-1]
  - Not run. [OPEN; P1 D10]

### 5.5 The THEOREMS that forbid more
**(a) G-NOGO-a = ST-1 G1 = CL-2 row 2.**
- No reciprocal (b-only, one-potential) gravity coupling of ANY rank has an exactly conserved source.
  [THEOREM, four independent proofs; ST S1; CL2 row 2; GU F-1]
- Why:
  - Reciprocity makes the source ∂Φ/∂F, a function of b alone (one-time).
  - Rule3's map a → b′ is onto, stage by stage, so no function of b alone is conserved on all orbits.
  - Equivalently (G1, scaling proof): take b(t) = 0 and a(t) = λv.
- So "Newton III exact" and "source conserved" exclude each other.
- Package: the source swings by 0.50 (default), against 9.4e-4 for a two-time source. [NUMERIC; ST S7, S11; CL2 row 2]
- Corollaries:
  - Under a changing lapse the only exact quadratic two-time invariants are Wronskian charges; energy is destroyed by
    dF/dt (work). [THEOREM + NUMERIC; ST S3]
  - A source exact under a changing lapse is a Wronskian D·aᵀXb, which is ODD under the time mirror (a ↔ b). So no source
    can be exact AND weigh a state and its time-doubler alike. [THEOREM; ST S19; GU F-7]
  - Sourcing cannot be made exactly conserved for field energy. [DERIVED; ST S17 AGREED]

**(b) No exact Bianchi identity.**
- Rule3's fixed kinetic coefficient D·1 admits no time-dependent gauge symmetry (no Noether II). Hence there is no exact
  Bianchi identity and no exact Hamiltonian constraint. Momentum-type (time-independent) constraints CAN be exact (OD2).
  [THEOREM; CL2 row 5; GU F-2]
- The finite-rank Deser conjecture says exact harmonic constraint + reciprocity need all orders in U; at rank ≤ 4
  consistency holds only to O(U²). [OPEN; CL2 row 22]
- An Einstein-conserved source together with a turnover trigger is impossible at rank ≤ 4. [DERIVED (scoped); GU F-6]

**(c) Only the Newtonian Bianchi is exact.**
- The time component of the contracted Bianchi identity at Newtonian order is the local continuity of the carrier number
  N_J, exact with the integer remainder ledger: N_J 24/24, J′ 24/24, Σ bᵀJu = 0, in two codes; 240/240 in the work form.
  [THEOREM + NUMERIC two codes; ST S2; GU E-5]
- Only its GLOBAL (k = 0) part is buildable as a source at today's integers. The local form would make gravity about
  6·10⁶ × too strong. [DERIVED; ST amendment (a); SD8 ch.2 §8]
- Also exact, as identities:
  - the exchange identity X (a sector's two-time energy changes by exactly the centred lapse work + ledger);
  - the shift law 𝒫(t+1) = 𝒫(t) + 2S(t).
  [THEOREM; CL2 rows 6, 7; GU E-6]

**(d) The source choices with prices (NEW LAW; none is in the default).**
- The HYBRID (ρ_J for Dirac + two-time Tolman energy for L0), owner-approved 13:09, default OFF:
  - H1 PASS: an exact tensor (B3, rank ≤ 4, vacuum and rewind bit-exact).
  - H2 reversor test FAILED as pre-registered: R* bounce mismatches 0, 2, 12, 36, 52, 54 at t = 1…6 (S2*). There is no
    time-shift reversor, because the two-time source is centred at t − ½ and the action at t.
  - H3: runaway at t = 500 (L = 4, strong dark seed).
  - COSMIC-N1: the Tolman part gives NO linear spring for k = 0 (a Hellmann–Feynman cancellation).
  - The decision-2 condition failed, so the owner must re-decide.
  [NEW LAW; NUMERIC + DERIVED; HYB; GU §4.3; SD8 ch.2 §8]
- The rest-mass lapse R: exact for any lapse history. But only Dirac rest mass gravitates, J− anti-gravitates, and
  binding energy would not gravitate. [NEW LAW; ST S9, S10, S19, S20; AUD §3b]

**(e) The uniform (k = 0) mode: exactly marginal, drift OPEN.**
- Summing Rule3 over the closed board gives the exact identity
  D·Σ_x[F(t+1) − 2F(t) + F(t−1)] = 2·Σ_x s + Σ_x(r − r′).
- This is the zero-mode shift law of CL2 row 6, 𝒫(t+1) = 𝒫(t) + 2S, with v uniform: 𝒫(t) = D·Σ(b(t) − b(t−1)) + Σr(t).
  (Pointed out by ALG-A.)
- Since Σ_x ΔF ≡ 0 on (Z/LZ)³, a static field needs Σ_x s = 0. Any net source drives F̄ ∝ (Σs/(D·L³))·t².
  [THEOREM (identity; CL2 row 6); EIN-A ein_k0_gauss.json: 0/120 failures]
- My run: mean F = 16.9 / 67.3 / 151.6 / 268.5 at t = 30 / 60 / 90 / 120, against the t² law 266.7 at t = 120 (ratio 1.007).
  [NUMERIC (EIN-A, L = 12, Q = 8193, MECHANISM source)]
- This is builder finding F4 (U grows ∝ t²; GR light dies at U = ¼). [NUMERIC; P1 D12 AGREE (OPEN)]
- It is the root of "the sourced field is not static" (§5.3a) and of the Eddington k = 0 drift. [DERIVED; CL2 r.9]
- Live default (FIX-i):
  - marginal at every k checked; [DERIVED; STAB R9]
  - bang seeds bounded ≥ 1196 updates (L = 6), but U_mean drifts (−0.036 at 1196, slowly accelerating);
  - behaviour beyond about 1,200 updates is OPEN.
  [NUMERIC; STAB R11, A1; joint result "OPEN: the uniform-lapse drift"]
- The earlier hands-ON gwb made k = 0 linearly unstable (λ = 1.138). FIX-i removed that. [DERIVED + NUMERIC; STAB R2, R4, R5]
- The fate of the uniform mode (spring, saturation or runaway) is OPEN. [OPEN; STAB; GU §9]

**(f) Gravitational waves: what exists exactly.**
- All 10 metric components exist as gears on the one cone (the headroom stencil, §5.1a). In the default, 9 of them (h0i,
  hij) are FREE: no matter reads them and none sources them. [NUMERIC (EIN-A)]
- So the default holds nine uncoupled scalar waves plus the sourced lapse h00, not GR's two constrained polarizations.
  The harmonic-gauge constraints
  C^μ are exact only in the OD2 accumulator option (G7), which is not in the default. [NUMERIC-pkg; GRAV G5/G7]
- Driven by a prescribed (MECHANISM) quadrupole:
  - front 0.583 against c_Q = 0.577 (+1.0 %);
  - 1/R amplitude within 10 % with the fixed-duration estimator (D4b PASS; D4 max-estimator marginal FAIL);
  - two polarizations: h× = 0 exactly for a linear quadrupole, h×/h+ = 0.86–0.99 for a rotating one.
  [NUMERIC; GRAV D4/D4b; P1 D9 AGREE (own estimator: [111] front 0.57735, 1/R exponent −1.025 rms; h×/h+ FAIL of the ±5 % band)]
- Reciprocal coupling of all ten components to matter needs the DeWitt metric. An integer basis exists
  (y0 = h00 + Σhii = 2h_00, …), but it is NOT built. [DERIVED; GRAV "DeWitt" note]
- So emission by the board's own matter, the quadrupole formula, the energy carried away and the back-reaction are NOT
  reproduced. [OPEN]

### 5.6 "Converges exactly to Einstein": the precise statement
**(i) EXACT identities on the board (any lattice spacing; integer arithmetic).**
- One stencil (on-site 6, ports Q − 1) for all metric gears, E1's A_d and (in magnitude) the L0 channels, giving
  c_Q² = (Q−1)/(3Q), given the CHOSEN common stencil. The β gear (stencil B) and em.Phi (accumulator) are the exceptions.
  [THEOREM; §5.1a]
- Exact lapse factors in the tensor:
  - clock (1 − 2U) and link (1 − 4U) for second-order clocks;
  - (1 − U) and (1 − 2U) for first-order clocks;
  - the half-angle law on every L0 band.
  [THEOREM; MF 5a/5b; live form C at every k: NUMERIC (EIN-A) pkg_formC_check.json]
- EP of the factor for every clock that reads the lapse (live default: at rest only the dark L0; the visible Dirac pair neither feels nor sources it): L0 in the live default; Dirac hands OFF.
  [THEOREM; §5.2]
- Reciprocity (Newton III) of the lapse coupling. [THEOREM; CL2 row 13]
- Per-update Gauss/flux identity for the lapse. [THEOREM; §5.3d]
- k = 0 identity. [THEOREM; §5.5e]
- Newtonian Bianchi (N_J continuity) with ledger. [THEOREM; §5.5c]
- Exchange identity X; shift law 𝒫. [THEOREM; §5.5c]

**(ii) True only IN THE LIMIT.** The limit is: w0 → 0, |k| → 0, U → 0 with U slowly varying.
- Q stays fixed: c_Q² = (Q−1)/(3Q) is exact at every odd Q. Q → ∞ only sends c_Q → 1/√3.
- Weak-field metric g00 = −(1 − 2U), g_ij = (1 + 2U)δ_ij, i.e. PPN γ = 1 via the chosen link factor, first order in U.
  [CHOSEN ⇒ DERIVED; §5.1c]
- PPN β = 1, only through the hands-OFF designated β read. [DERIVED + NUMERIC; §5.1c]
- Lorentz invariance at O(k²). [DERIVED; §5.4]
- EP of the observed rates: first order in U, with the predicted O(U·w0²) lattice departure. Live default: L0 only.
  [DERIVED + NUMERIC (two codes); §5.2, §5.3e]
- Redshift z = ΔU. [DERIVED; NUMERIC static field; §5.3a]
- Bending ×2. [DERIVED; NOT RUN; §5.3b]
- Shapiro ×2. [DERIVED + NUMERIC (test light); §5.3c]
- Poisson and the Newtonian potential V = −mU, for the k ≠ 0 field on top of the drifting uniform mode. [DERIVED + NUMERIC; §5.3d]

**(iii) ABSENT or FORBIDDEN.**
- Einstein's field equations G_μν = 8πG·T_μν are NOT reproduced. [§5.5]
  - An exactly conserved reciprocal source is FORBIDDEN. [THEOREM; §5.5a]
  - An exact Bianchi identity is FORBIDDEN. [THEOREM; §5.5b]
  - The default source is a one-time, b-only energy that oscillates at 2w. [NUMERIC; ST S7]
- The strong field departs from GR. [DERIVED/NUMERIC; §5.1c]
  - The Dirac clock stops at U = 1, not ½.
  - L0's √(1 − 2U) stops at U = ½, but L0's link factor flips at U = ¼ and the board blows up first.
- Frame dragging: OPEN, with a likely no-go. [§5.4]
- Radiative GR (generation, back-reaction, two-polarization constraint): OPEN. [§5.5f]
- Universality in the live default: OPEN debts. [§5.2]
  - The lapse is read by L0 (form C) and by the FIX-i singlet-half hop.
  - Gauge-layer matter and E1 light do not read it.
  - The doublet's clock carries the FIX-i EP debt.
- Free-fall magnitude read from clicks: OPEN. [§5.3d]
- Cosmological deceleration FAILS in the approved law. [NUMERIC; AGREE_B B8; GU §4.3]

**One sentence for the owner.**
- Universe24 reproduces Einstein's KINEMATICS in the continuum limit, as the limit of exact integer identities of one
  tensor:
  - one cone (given the chosen common stencil);
  - a weak-field metric, with γ = 1 via the CHOSEN link factor;
  - the EP for every clock that reads the lapse (live default: at rest only the dark L0; the visible Dirac pair neither feels nor sources it);
  - local Lorentz symmetry at O(k²).
- Its DYNAMICS is a NEWTONIAN-LEVEL sourced scalar lapse plus designated one-way parts.
  - In the live default the lapse is sourced by L0, the singlet-half hop and bgk, not by the visible Dirac rest mass.
- The full Einstein equations are NOT reproduced. Rule3 itself forbids, by theorem, the exactly conserved reciprocal
  source and the exact Bianchi identity that they would need.
- [DERIVED summary of §5.1–§5.5; no new law; nothing posted]

**EIN-A exact checks (s24/EIN-A_work/; ≤ 1 core, nice 19; the package was read, never written).**
- pkg_cone_check.py / .json (14:56:06): metric + E1 stencils, h00 readers and sources, 9 free metric gears.
- pkg_cone_check2.py / .json (14:56:23): β readers; L0 ports and on-site terms.
- ein_limits.py / .json (sympy 1.14): C1 cone identity and the O(k⁴) term; C2 γ = 1 (and the 1911 control γ = 0); C3 Dirac
  metric; C4 β = 1; C5 −1/12 and −1/3 with the U = 0.01 tick ratios; C6 bending ×2 and Shapiro 2 + 3U.
- ein_k0_gauss.py / .json (14:57:41): exact Python-int Rule3 run, L = 12, Q = 8193. The k = 0 identity holds 120/120 and
  the box flux identity 360/360. The uniform mode drifts as t².
- vg_check.py / vg_check_mp.py (+ .json, 15:02): group velocity ≤ c_Q along [100], [110] and [111].
- pkg_formC_check.py / .json (15:05:11): form C exact on the live tensor, P·B(k) = D·1 + A(0) − 2A(k) at 64 k-points
  (147,456 entries, 0 failures).
- pkg_fixi_ep_check.py / .json (15:06:22): lapse reads into the doublet are hop-only (768, all gwb); 0 mass-type reads.
- pkg_h00_terms.py / .json (15:07:53): h00-reading TERMS per block, with degree and designation (beta 7 designated, em 192
  designated degree 3, gwb 384 + 384 and lapseL0 1,104 reciprocal degree 2).
<!-- END §5 (EIN-A) -->

---------------------------------------------------------------------------------------------------------------------
## §6 CONSERVATION AS EINSTEIN FOUND IT — what is exact on the board, what in the clicks, what only in a limit
- [THEOREM] In GR, ∇_μT^{μν} = 0 follows from the Bianchi identity plus the field equations. Rule3 has a fixed kinetic
  coefficient D, so it admits no time-dependent gauge symmetry: no Noether II, hence no exact Bianchi identity and no exact
  Hamiltonian constraint (F-2). The board therefore has its OWN exact laws, listed here. — s11 AGREE_CL2 row 5; GU §4.2.
### 6.1 Exact on the board (every update, every amplitude, no limit)
| # | law | exact form | label | source |
|---|---|---|---|---|
| B1 | information | Rule3 is a bijection; rewind exact on the full default | THEOREM | AGREE_B A1; GU §5.4 (numeric check) |
| B2 | click ledger, per gear | D·ℓ = K + r − r′; D·Σℓ = ΣK + r(0) − r(T) | THEOREM | §4.5 |
| B3 | discrete Noether | every exact law is a discrete Noether theorem of L = Φ(x) + Φ(y) − D x·y plus the remainder step | THEOREM | AGREE_CL2 row 1; GU E-3 |
| B4 | charges | J′, local Gauss for SU(2)/SU(3)/U(1) (0/32,400; 0/92,160; 0/1,280), L0 isospin, X4, N_J, matter number, each with an integer remainder ledger | THEOREM | GU E-4, §2.1; AGREE_CL2 rows 4, 6 (package counts) |
| B5 | N_J local continuity (time part of the contracted Bianchi at Newtonian order) | N_J(t+1) − N_J(t) = b(t)ᵀJ(r(t) − r(t+1)) | THEOREM | AGREE_ST S2; AGREE_B A5 (two codes) |
| B6 | zero-mode charge (cosmic law) | 𝒫_v = D v·(b − a) + v·r, 𝒫(t+1) = 𝒫(t) + 2v·s for ANY source, ledger-free | THEOREM | AGREE_CL2 row 6 (zm_check 0/120) |
| B6′ | its uniform-lapse form | D·Σ_x[F(t+1) − 2F(t) + F(t−1)] = 2Σ_x s + Σ_x(r − r′): a net source drives the uniform lapse ∝ t² | THEOREM | §5.5e (EIN-A ein_k0_gauss 0/120); = B6 with v uniform, since 𝒫(t) = D Σ(b(t) − b(t−1)) + Σ r(t) |
| B7 | exchange identity X | matter's two-time energy changes by exactly the centred lapse work + ledger | THEOREM | AGREE_CL2 row 7; GU E-6 |
| B8 | two-time energy (linear symmetric part) | E(t+1) − E(t) = Σ (r − r′)(b′ − a): only remainder kicks change it | THEOREM | AGREE_GU2 B3; ALG-A energy_check.out (0/12,000) |
| B9 | CPT | R* exact reversor along the bang seed: v2 default (hands OFF) t ≤ 200; hands ON t = 1…6 (batch 4) / 1…10; FIX-i t = 1…10 | NUMERIC | AGREE_B B1; GU E-9, §6.6 |
### 6.2 Exact in the clicks
- [THEOREM] The click charge equals the board charge × 4cos²w (= μ²). — GU §3.7 (M2-2).
- [THEOREM] For an exactly matched shared-remainder pair the record Δ obeys Δ(t+1) + Δ(t−1) = ℓ+ − ℓ− (the number of events
  equals the load). — AGREE_CC A2(c).
- [CHOSEN] Energy in clicks = own-frame tick rate × number: a redshifted Killing energy, conserved only in a static field, as in GR. — SYSTEM_DESIGN_v8 l.1682 (a reading, not a new law).
### 6.3 Only in a limit, or not at all
- [THEOREM] No exact TOTAL energy at rank ≥ 3 (matter + lapse + E1): the T⁰⁰ identities are balances with a work term. — AGREE_CL2 row 4.
- [THEOREM] No exactly conserved AND reciprocal gravity source: a reciprocal coupling reads one time (b only), and no nonzero
  one-time quadratic is conserved on all free orbits (G-NOGO-a; F-1). — AGREE_ST S1; AGREE_CL2 row 2.
- [NUMERIC] Local energy continuity with an explicit link flux, ∂_tT⁰⁰ + ∇·T⁰ⁱ = (one-way inputs + remainder kicks): 4617/4617
  on a toy; lattice momentum exact only in remainder-free sectors (79/79). — GU E-7 (AGREE_CC, CC-B final).
- [THEOREM] Newton III fails for one-way (designated) parts by definition; momentum beyond rank 2 is not conserved. — AGREE_COSMIC E4; GU §9.4.
- [DERIVED] So Einstein's conservation law holds on the board only through exact SUBSTITUTES (B4–B8) and in the continuum,
  Newtonian-limit sense of §5; never as ∇_μT^{μν} = 0 with a reciprocal source. — GU X15.

---------------------------------------------------------------------------------------------------------------------
## §7 HANDS, FORCES, PATI–SALAM, ROUTE B, FAMILIES, PAULI, ENTANGLEMENT — the algebra in brief
### 7.1 The hand (chirality)
- [THEOREM] The cube has exactly one orientation bit: O_h/O = {±1} = det; in Cl(0,3) the centre is span{1, ω}, ω² = +1 (§2.4),
  so there are exactly two hands ½(1 ± Γ5), Γ5 = −PxPyPz. — GU §6.1.
- [THEOREM] Γ5·V (V = JJ′) is the only chiral, CPT-even, clock- and charge-keeping split (unique up to the P sign): Einstein's
  J′-self-dual Lorentz half, "one hand, two groups". — AGREE_HL; AGREE_CL3 rows 1, 22; AGREE_GU1 A3.
- [THEOREM] P exchanges Π_W ↔ Π_S, C flips V, CP keeps Γ5·V: P and C broken, CP exact. — GU §6.1.
- [NUMERIC] Package demo: the CP-image run has 0 unpaired clicks of 60,237; the P-image run has 104,381 unpaired. — NOTES_chiral DEMO; GU §6.1.
- [THEOREM] Nielsen–Ninomiya: an exactly chiral LAW but never an exactly chiral SPECTRUM; mirror doublers carry Wilson–Yukawa
  masses; light-sector anomaly freedom (N_c odd; N_c = 3 with standard charges) is the condition for the doublers to decouple. — AGREE_GU1 B7, A14; AGREE_CL3 row 9.
- [CHOSEN] That the weak force couples to one hand (NL-1) and which hand (the P sign). — GU §6.1.
### 7.2 Forces = links
- [THEOREM] At rank 3 one link per face per irreducible multiplet spans End(R): U(2) for a hypercharged doublet, M6(C) for (3,2),
  M8(C) per hand for (4,2) (Burnside). — GU §2.2; AGREE_GU1 A8/B5.
- [NUMERIC] Local Z4 / Q8 / Δ96 covariance bit-exact; Gauss = Noether + remainder: SU(3) 0/92,160, SU(2) 0/32,400, U(1) 0/1,280. — GU §2.1 (v6 A.2).
- [THEOREM] Wilson loops are view-invariants (board = clock = click). A link is a clock: radial 4 sin²(w/2) = 4λA²/D (§3.10),
  angular part = holonomy. — GU §2.1, §2.3.
### 7.3 The unification ceiling: Pati–Salam
- [THEOREM] Under V and the charge ring, exactly 21 of the 45 so(10) generators commute with both: SU(4) × SU(2)_L × SU(2)_R is
  the largest unification keeping J′ and V inside SO(10). — AGREE_CL3 row 12; GU §6.3.
- [DERIVED] Once PS is chosen: Y = T3_R + (B−L)/2 and 6Y ∈ Z; no gauge-mediated proton decay (a prediction). — AGREE_CL3 row 14; AGREE_GU1 A13.
- [CHOSEN] Keeping J′ and V, and stopping at SO(10), are choices (PS is CONDITIONAL, X29). — AGREE_GU1 joint 2.
### 7.4 Route B (exact local SU(2) × U(1)_Y; ONE v2)
- [NEW LAW] U(2) = M2(C) unified link for a lepton doublet, M6(C) for a quark doublet; the |det V|² matrix spring (forced for
  M2(C), not a composition algebra); e_R via a charge-2 link locked to det V (rank 3). — GU §6.2; GU-1B Thm 5, Cor 5a/5c.
- [THEOREM] Exactly one light on c_Q with exact Gauss is IMPOSSIBLE under the current rules (T3 rank obstruction; T4: a
  non-compact B cannot gauge a charged Higgs); exactly-c_Q compact links melt (T5). — s19 ONE_LIGHT_FINALS; GU §6.2b.
- [NEW LAW] APPROVED 14:37: the plaquette rank-4 kind (§3.8) + a det-shadow link (one U(2) Frobenius norm alone forces
  sin²θ_W = 1/2, falsified at 1066σ). Expected c = c_Q(1 − η), η ~ 10⁻⁴. Not built. — GU §00 line 7; s21 AGREE_MASS.
### 7.5 The hands-ON dynamics and FIX-i
- [NUMERIC] Hands ON (before FIX-i), the default ran away after a bang (t* ≈ 120–420 at L = 6); the seed is a linear k = 0
  instability from gwb's lapse–radial bilinears (λ = 1.1381; corner −1.026). — GU §5.6b; s18 AGREE_STAB.
- [THEOREM] R5: any nonzero bilinear coupling of an exactly marginal mode in a symmetric linear Rule3 system pushes it past the
  band edge (Rayleigh quotient slope 2eᵀEw ≠ 0). The uniform lapse is exactly marginal (k = 0 row sum = D). — AGREE_STAB R5; GU §6.6.
- [CHOSEN] FIX-i (λ_H = λ_L = 0): existing coefficients set to 0, no new law; marginal at k = 0 and at every L = 6 k checked
  (corner included); bounded on three L = 6 bang seeds
  to ≥ 1196 updates; in the package default since 14:45:16 (ONE-A). Debt: the doublet's EP (its mass and doublet-half transport
  are not lapse-dressed). — s18 AGREE_STAB; NOTES_system.md l.745–751; GU §6.6, X34.
- [DERIVED] Owner trilemma at today's integers: an untuned stable lapse, EP at O(U) for Higgs-generated masses, exact local SU(2)
  with gravity on — pick two (FIX-i: first and third). — GU §5.6b (DERIVED from R5 + linear response; signed in AGREE_STAB R9–R17).
- [TUNED] FIX-C+ (counter-terms computed from the couplings): NOT adopted (binding owner rule 14:43). — GU X35(b).
### 7.6 Families, Pauli, entanglement
- [THEOREM] No natural family 3: every 3 on the node is the cube's axis triple; the frame triple gives (m1, m2, m2) and no mixing;
  the frame-free triple is bosonic and split 1 + 2. — s16 AGREE_FA; GU §7.1.
- [THEOREM] Why three is the minimum for CP: Im det[H_u, H_d] is an exact even integer, ≡ 0 for two families, generically ≠ 0 for three. — AGREE_FA III.
- [NEW LAW] Three families = three copies (384 = 128 × 3 channels) + a complex bidoublet; links family-blind, rank unchanged;
  APPROVED build target (ONE v3). 384 = 8 × 48 is a coincidence. — GU §7.1; AGREE_FA B6.
- [THEOREM] Pauli, the exchange sign and spin–statistics are missing on one board (S₂ acts trivially on board states); the
  board has unit counting at the detector and the single-quantum 2π sign (z = −1). — s16 AGREE_PA; GU §7.2.
- [NEW LAW] Pauli by orbital copies with wedge readers: APPROVED, separate variant first (ONE v3). — GU §00 line 9.
- [THEOREM] "Entanglement from the path choice" = a confirmed joint read of two setting clocks = classical communication
  inside the cone; true entanglement needs configuration space (×1.26·10⁷ per added quantum at L = 64), a NEW LAW recorded for
  after Pauli. — s16 AGREE_EN; GU §7.3.

---------------------------------------------------------------------------------------------------------------------
## §8 QUANTA
- [THEOREM] Click = carry (§4.4); the click map is many-to-one, so collapse = conditioning on records; nothing is erased; the
  record is the arrow. — AGREE_GU4; GU §10.
- [THEOREM] Born is exact from a uniform FRESH remainder (§4.6). — AGREE_GU4 row 2.
- [OPEN] Freshness of the remainder (and one quantum ↔ one click). — GU X10; §11.3 (5).
- [THEOREM] Bell: |S| ≤ 2 under measurement independence; the cos law holds exactly inside the first click's cone. — s14 AGREE_BELL D-final.
- [NUMERIC] Measured on the board: S = 1.18–1.26 with and without Θ (exact 5/4), against 2.07–2.42 in loophole-free experiments. — AGREE_BELL D.
- [NEW LAW] The only door to spacelike S > 2 is superdeterminism (a law on seed data); floor δ ≥ 0.138 for any readers; over ALL
  seeds S = 4 (rewind any record), so such a law predicts nothing (X25). — AGREE_BELL B4, D.
- [THEOREM] Tsirelson's 2√2 follows from four declared READER laws (one-way, amplitude-only, fresh Born, setting-free average);
  breaking one gives a PR box or signalling. The reader laws are inputs, not board theorems. — s20 AGREE_ZT T4; GU X26.
- [CHOSEN] OWNER'S READING (O3, box): "There is no freeze on the board: light is the executor of the clicks, and when a path is
  chosen only it produces the click." — manager relay (stamped 15:40, received 15:25 by date -u).
- [THEOREM] No freeze, by the law itself: an oscillator cannot be paused by any input (a pause needs ℓ = a + b of the gear itself,
  a self-a-read, which breaks the bijection), and no b-only rule of ANY degree generates a hold (16/16 conflicts at every rank). — AGREE_INTEGRATED IB7; s23 AGREE_R5 B1, C4.
- [THEOREM] Only the chosen path clicks: one shared remainder, exactly one overflow, P(both) = 0 (§4.6). — AGREE_GU4; GU §10.
- [DERIVED] Every click is caused by inputs that arrive through B3 links, i.e. inside the B3 cone (§3.4); "light executes the
  clicks" is the owner's reading of this (O3, CHOSEN, not derived). On the integrated board the choices happen only where light
  is. — §3.4; GU §9.5.
- [POSTED] The zero-time hold (Study 20, case (c)) is DROPPED from the picture: its schedule was put in by hand, and no tensor
  generates it at any rank. — s20 AGREE_ZT; GU X35(a); s23 AGREE_R5 B1.
- [THEOREM] No-signalling is a theorem of the law: B3 gives the B3 cone theorem (§3.4), and with no hold and no gate in the law
  there is no click-time non-local mechanism, so spacelike S ≤ 2 under measurement independence (over ALL seeds S = 4, X25). — GU X36; s23 AGREE_R5 N1; s14 AGREE_BELL.
- [THEOREM] Odd-Q parity: no carry event has probability exactly 1/2 (multiples of 1/(3Q)^m), so the gate designs' F7 leak
  (≈ 0.0023 at Q = 101) is never exactly 0 — one more reason those designs are not in the law. — AGREE_INTEGRATED IB5–IB6; AGREE_R5 N1.

---------------------------------------------------------------------------------------------------------------------
## §9 SEED, THE ONE EXACT CPT BANG, NEW SEEDS, THE COSMIC CLOCK, ECHOES AS DATA, THEOREM K
### 9.1 The seed (data only)
- [CHOSEN] The vacuum (0, 0, 3Q−1) everywhere + seed amplitudes; prepare/ writes data only. — GU §8; AGENTS 9.
- [CHOSEN] S2*, the minimal bang seed, has exactly TWO non-vacuum integers: b(x0) = A e_i and a(x0 + e_y) = A Γ e_i, Γ = J′KW0;
  it is R*-fixed about the link midpoint and legal at t = 0 (Lorenz C = 0, Gauss Y = 0 everywhere). — NOTES_system SEED; prepare/seed.py; GU §8.
- [CHOSEN] The J-pure seed: A_J = 2^12, 6,912 nonzero integers on 216 nodes, J− fraction 8.6·10⁻⁸; the background datum, the R-a
  gear and the k = 0 lapse offset are declared data. — GU §8.
### 9.2 The one exact CPT bang
- [NUMERIC] R* (= CPT) is an exact reversor of the WHOLE v2 default (hands OFF) along S2*: the past is the CPT image of the
  future, the bang is two-headed, and the click record is mirrored about it (two codes; t ≤ 200 at A = 2^18). — s8 AGREE_B B1.
- [NUMERIC] Hands ON: R*_on exact for t = 1…6 (NOTES_system batch 4) and t = 1…10 (EMERGE-N ARM B); with FIX-i, R* has 0
  mismatches for t = 1…10 on S2* and J-pure (STAB-B 14:09). — GU §00 line 6, §6.6.
- [THEOREM] At most ONE exact bang in a growing history (THEOREM D); under the approved gravity law WITHOUT the WIND layer (the
  package default) there is no recurrence at all: the uniform mode is symmetric about the bang and rises on both sides, so the
  bang is the minimum of U. — AGREE_GU2 C5; AGREE_B B2.
- [THEOREM] The other side is the CPT anti-aeon; with Γ5·V, CP is an exact forward symmetry, so it is one-handed in its own clicks;
  no J+ → J− transfer through any crossing. — AGREE_B A5; GU §8.
### 9.3 Later bangs start from a NEW seed (owner decision O2, box)
- [CHOSEN] OWNER (O2): "the bangs are not supposed to return — information is not lost — a bang starts with a new seed." — manager relay (stamped 15:40, received 15:25 by date -u).
- [THEOREM] There is ONE exact CPT bang (§9.2); a growing history has at most one (THEOREM D), so no later bang is a return of
  the first. — AGREE_GU2 C5; AGREE_B B1–B2.
- [CHOSEN] Reading adopted: each later turn of the cosmic clock starts a NEW seed, namely the complete state at the turn,
  with all its records; nothing is reset, posted or tuned. — O2 (box).
- [THEOREM] Information is never lost: Rule3 is a bijection on the full (a, b, r), the click record is a redundant copy, and the
  board's information is law + seed + ⌈log2 t⌉ (THEOREM K). — AGREE_B A1; s20 AGREE_ZT ("not lost"); AGREE_GU2 C3.
- [DERIVED] The cosmic hand of the approved law is gravity's k = 0 mode, and it has no restoring force (no datum gives one);
  a spring ON the uniform lapse would screen gravity beyond ~5 sites (order of magnitude). So the cosmic clock needs a
  SEPARATE γ = 0 hand. — AGREE_B B3 (DERIVED + NUMERIC T10f); GU §9.1 (CUBE-B REFINE).
- [NEW LAW] WIND (approved, ONE v1): a per-node hand Θ, no bare spring, stiffness from the matched-pair choice record Δ
  (Δ(t+1) + Δ(t−1) = ℓ+ − ℓ−), a rigid clock field, R-keep; the turn comes when ∫Ω_eff dt = π/2 (a choosing budget). — AGREE_COSMIC E2; AGREE_CC; GU §9.2–9.3.
- [THEOREM] It reads b-values (Δ), never r, so it is legal and not circular; the choices TIME the turn and never CAUSE a bang
  (THEOREM N); a fold returns to the mirror of the SATURATED state, not to the seed (THEOREM X). — GU X20; AGREE_CC C1, C4.
### 9.4 Echoes are data, not the goal
- [THEOREM] THEOREM O (fold classes): an exact fold needs (A) first-order fields with every input = Θ × odd in (A), (Θ) every
  term odd in Θ, (C) slow fields not reading Θ with zero velocity at every zero; an interacting composition never folds exactly. — AGREE_COSMIC A1, C2.
- [NUMERIC] Recorded as DATA: CC-A's integrated board turned 20 times in 20 aeons over 5,400 updates with approximate echoes
  (distance 0.0043 → 0.042, ∝ √n); 99.99 % of the choices were new each aeon; the cosmic history was bit-identical across token
  seeds (driven by choice EVENTS, not outcomes). — GU §9.5; s13 AGREE_INTEGRATED.
- [CHOSEN] Under the owner's decision an echo is a measured property of a new seed, not a target: no coefficient is tuned to
  improve it (X35). — O2 (box); GU X35.
- [NUMERIC] ONE v1 (Study 22; s22/AGREE_ONE.md signed by ONE-A 15:30:26 and ONE-B 15:30:15; read by ALG-A at 15:31:37): on L = 6
  from the J-pure seed, 1200 updates bounded (package max 25 bits); rewind of all 1200 updates exact, across six turns; cosmic
  and Rule3 click ledgers 0 failures; turns at t ≈ 96, 289, 481, 672, 863, 1054 (the ~192-update period is an INPUT, set by g_w);
  per aeon ≥ 99.4 % new pair-outcome entries and ~80 kB of new incompressible record, flat per aeon; echo distances kept as DATA. — AGREE_ONE R8–R12, R18–R19, OB10.
- [NUMERIC] Honesty rows there: the pre-registered "every update int64" FAILED (858/1200), and the owner framing of R18–R21 is
  POST HOC (written after the runs). — AGREE_ONE R8 correction; label note.
- [OPEN] Behaviour beyond 1,200 updates. — AGREE_ONE; s18 AGREE_STAB (uniform-lapse drift).
### 9.5 THEOREM K (information) and emergence
- [THEOREM] |K(X_t) − K(X_0)| ≤ 2 log2 t + O(1): the board's information is law + seed + ⌈log2 t⌉; all growth beyond log t is
  apparent (coarse-grained). — s12 AGREE_GU2 C3.
- [NUMERIC] EMERGE-N (hands OFF): complexity saturates by t ≈ 10–100; structure rises and falls once while the bang shell wraps
  the torus; only the click record grows (+14.5–15.6 kB/update); 0 persistent localized structures at L = 6. — GU §9.6.

---------------------------------------------------------------------------------------------------------------------
## §10 CIRCULARITY AUDIT and the FORCED / CHOSEN / NEW LAW / OPEN table
### 10.0 The derivation chain: every step uses only steps above it (this is why there is no circle)
1. [CHOSEN] Inputs: d = 3 and L; the 2O labels; the body actions (0,1,3) and signs (1,−1,1); D = 6Q and the value of Q; the
   gear list and its integer weights (the tensor); the seed. Nothing else enters. — GU §11.2 (I-1…I-6).
2. [THEOREM] Rule3 alone ⇒ exact bijection and staged inverse (§1.3).
3. [THEOREM] Rule3 alone ⇒ click identity ℓ = b(t+1) + b(t−1) and the ledger D·Σℓ = ΣK + r(0) − r(T) (§1.2, §4.5).
4. [THEOREM] Rule3 + the CHOSEN reciprocity of a block ⇒ discrete Euler–Lagrange: its forces = ∇Φ, rank = degree of Φ (§1.7, §3.2).
5. [THEOREM] Step 3 + the tensor's linear part ⇒ eigenmodes cos w = μ/2, mass = rest rate, Born count K/D (§4.2–§4.6).
6. [THEOREM] Rule3 + the demand "vacuum fixed by the exact mirror" (CHOSEN) ⇒ Q odd, vacuum pair {3Q−1, 3Q} (§1.6).
7. [THEOREM] 2O labels + ports ⇒ left frame / right internal Q8, mirrors = Out(2O), the 1+2 split (§2).
8. [THEOREM] Chosen massive Dirac matter ⇒ Γ5 = −PxPyPz and the uniqueness of Γ5·V (§2.4, §7.1).
9. [DERIVED] Steps 4–5 + the CHOSEN common stencil (⇒ one cone) + the CHOSEN universal lapse dressing with c_link = 1 (clock
   1 − 2U, link 1 − 4U ⇒ EP factor, γ = 1; c_link = ½ would give γ = 0) + the continuum limit ⇒ Einstein's kinematics (§5).
10. [THEOREM] Step 4 (fixed kinetic D) ⇒ no exact Bianchi, no exactly conserved reciprocal source (§5.5, §6.3).
11. [DERIVED] No step 2–10 uses a click, a reader, a run result or a later step as an input; runs only CHECK steps (NUMERIC).
### 10.1 The test
- [CHOSEN] A claim is CIRCULAR if it uses its own conclusion, or relabels an input as an output; it is a FAKE if a number is not
  produced by the law + seed (posted, tuned, fitted). Rows X1–X36 are the signed audit of GU §11.4–11.5 (condensed; X22 and X33–X34 updated for FIX-i, 14:37). — GU §11.4.
### 10.2 The audit rows (condensed; each verdict is signed in GU)
| # | tempting claim | verdict | label |
|---|---|---|---|
| X1 | the hand is the product of the cube's mirrors | FALSE: that product is parity (−W0); Γ5 is the volume of the transports | THEOREM |
| X2 | chirality is the cube's volume, not added | CIRCULAR as worded: forced only once Dirac matter with a mass is chosen | CHOSEN |
| X3 | 3 families because the cube has 3 axes | CIRCULAR/REFUTED: 3 = d is input; the triple is bosonic, split 1 + 2 | THEOREM |
| X4 | 3 families seen in the clicks | NOT EVIDENCE: C0/C1/C2 = u mod 3 are arithmetic classes | THEOREM |
| X5 | x is singled out by nature | INPUT: x has the trivial body action because (0,1,3) was chosen | CHOSEN |
| X6–X8 | colour 3 = axes; 48 = 3 × 16; 1/6 hypercharge = D = 6Q | COINCIDENCES (AGREE_CUBE C9; AGREE_CL3 row 30) | DERIVED |
| X9 | Y is derived | CONDITIONAL on the PS choice | CHOSEN |
| X10 | Born is exact | CONDITIONAL on a fresh remainder (OPEN) | OPEN |
| X11 | the choices drive the cosmic clock | QUALIFIED: they TIME the turn, never CAUSE it (THEOREM N) | THEOREM |
| X12, X24 | complexity rises bang to bang / emergence | QUALIFIED: only the record grows; board information ≤ 2 log2 t | THEOREM |
| X13, X21 | the confirmation gate solves Bell | FALSE as settings-only (S = 5/4); outcome-carrying = NEW LAW, contradicted by controls | THEOREM |
| X14 | gravity + gauge are one connection | FALSE: one algebra from two sides | THEOREM |
| X15 | Einstein's conservation law holds | FALSE in exact form (F-1, F-2); exact substitutes §6 | THEOREM |
| X16 | 1/3, 2/3, 0.88 c_Q, c² = (Q−1)/(3Q) are predictions of nature | INPUT-DEPENDENT (D = 6Q, stencils) | CHOSEN |
| X17 | the cube fixes the constants | FALSE: it fixes FORMS; 3, Q, weights, N_c are inputs | CHOSEN |
| X18, X28 | the 1+2 split is nature's flavour pattern / clicks confirm it | COMPARISON / ENGINE CHECK only | DERIVED |
| X19 | mirror symmetry is broken by the handed board | FALSE on L0 (an exact χ-twisted mirror exists); P broken only by Γ5·V | THEOREM |
| X20 | the cosmic clock reads the choices | LEGAL as TIMING: reads Δ (b-values), not r | THEOREM |
| X22 | the hands-ON default is verified | TRUE kinematically, FALSE dynamically before FIX-i ("exact" ≠ "bounded") | NUMERIC |
| X23 | one cone / one light for everything | FALSE for route B under current rules (needs the plaquette NEW LAW) | THEOREM |
| X25 | superdeterminism explains Bell | NOT A PREDICTION (fit; over all seeds S = 4) | THEOREM |
| X26 | the integrated board derives Tsirelson | FALSE: same machinery gives 2.832 or a PR box; 2√2 follows from declared reader laws | THEOREM |
| X27, X27b | the runaway is fixed by a counter-term | must be pre-registered; FIX-C / FIX-C+ are fitted to the couplings | TUNED |
| X33, X34 | route (c) / FIX-i is the fix | route (c) fails the integer grain; FIX-i is a TRADE (stable, EP debt), adopted | CHOSEN |
| X29 | Pati–Salam is forced | CONDITIONAL (keep J′ and V, stop at SO(10)) | CHOSEN |
| X30 | Q odd and D = 6 are derived | CONDITIONAL: Q odd given a mirror-fixed vacuum; D = 6 given K = 2u and six unit ports; Q's value chosen | CHOSEN |
| X31 | the cube predicts Koide's 2/3 | READING + COINCIDENCE (representable in Z[i], not forced) | DERIVED |
| X35 | anything posted/forced/faked counts as law | NO (binding owner rule 14:43): hold DROPPED (owner O3), FIX-C+ not adopted, ARM C = mechanism, seeds not tuned | POSTED |
| X36 | no-signalling holds | only as a THEOREM: board-causal yes (cone); click-time must be derived per law | THEOREM |
### 10.3 New rows from this study (ALG-A; for the verifiers)
| # | tempting claim | verdict | label |
|---|---|---|---|
| X37 | "the census is 375 / 18,623 / 706" | TRUE for the 13:43 composition; the FIX-i default (14:45) is 375 / 18,553 / 706 (§3.9) | NUMERIC |
| X38 | "a gear always ticks at its eigen-rate" | only for amplitude ≫ 1; at amplitude 1 the rate locks to a rational (period 6 vs 5.42) (§4.3) | NUMERIC |
| X39 | "the vacuum remainder 3Q−1 is forced" | the PAIR {3Q−1, 3Q} is forced by a mirror-fixed vacuum (odd Q); picking 3Q−1 is a convention (§1.5–1.6) | CHOSEN |
| X40 | "Jp (sign flip) is a symmetry of the default" | FALSE: Jp commutes with Rule3 only for tensors odd in v; the default has degree-2 terms; Jp is a building block of R* (§1.6) | THEOREM |
| X41 | "rank 5 solves the zero-time hold" | NO: no b-only hold rule of ANY degree exists on the invisible band; the hold fails the EMERGENT rule at every rank (AGREE_R5 B1) (§3.11) | NUMERIC |
### 10.4 FORCED / CHOSEN / NEW LAW / OPEN
| item | status | label | where |
|---|---|---|---|
| exact reversibility (bijection), the staged inverse | forced by Rule3 | THEOREM | §1.3 |
| every gear a clock (cos w = μ/2); click = carry; the ledger | forced by Rule3 | THEOREM | §4 |
| for the reciprocal part: Rule3 = discrete Euler–Lagrange, rank = degree of Φ | theorem; reciprocity itself is a CHOSEN design rule (checked) | THEOREM | §1.7, §3.2 |
| Q odd (given a mirror-fixed vacuum); one vacuum pair {3Q−1, 3Q} | forced | THEOREM | §1.6 |
| spin ½, frame = left 2O, internal SU(2) = right Q8, mirrors = Out(2O), one orientation bit | forced by the 2O labels | THEOREM | §2 |
| Γ5 and the uniqueness of Γ5·V (given massive Dirac matter) | forced | THEOREM | §2.4, §7.1 |
| one link per multiplet; link unification; |det V|² for U(2) | forced at rank ≤ 4 | THEOREM | §3.2, §7.2 |
| no-gos F-1…F-7 (no conserved reciprocal source, no exact Bianchi, …); Nielsen–Ninomiya | forced | THEOREM | §5, §6.3 |
| d = 3, L, the 2O labels, (0,1,3), signs (1,−1,1), Q = 2^33+1, all weights, the seed | inputs | CHOSEN | §1, §2, §9 |
| massive Dirac matter, the weak doublet, J′, N_c = 3, Pati–Salam ceiling, Gaussian Yukawas | content inputs | CHOSEN | §7 |
| FIX-i (λ_H = λ_L = 0) | coefficient choice, not a new law; EP debt | CHOSEN | §7.5 |
| the hand Γ5·V; narrow rank-4 kind; route B; plaquette + det-shadow link; WIND; families (copies); Pauli copies | approved | NEW LAW | §3.8, §7, §9 |
| zero-time hold | schedule put in by hand; cannot emerge at any rank; DROPPED from the picture (owner O3) | POSTED | §8 |
| rank 4 final; later turns start new seeds; no freeze (light executes the clicks) | owner decisions O1–O3 (box at the top) | CHOSEN | §3.11, §8, §9 |
| FIX-C / FIX-C+ counter-terms | fitted to the couplings | TUNED | §7.5 |
| freshness of remainders; doublet EP; uniform-lapse drift; gravity source re-decision; universality; route B build; ONE v1 run | not established | OPEN | §4.6, §5, §9.4 |
### 10.5 Why everything fits (and what does not)
- [THEOREM] Everything that fits, fits because it is ONE bijection with ONE divisor: clocks, clicks, ledgers, Born counts,
  charges and the energy identity are identities of the same update (§1, §4, §6); forces are derivatives of ONE potential per
  reciprocal block (a CHOSEN, checked design rule) plus declared one-way entries (§1.7, §3.5); symmetries are automorphisms of ONE node (§2). — this document, sources per line.
- [CHOSEN] The numbers that make it look like our world (3, Q, weights, Yukawas, N_c, the seed) are inputs, not outputs. — GU X16–X17.
- [THEOREM] What does not fit, by theorem: exact Einstein dynamics (no conserved reciprocal source, no Bianchi), exactly one light
  for route B under the current rules, Pauli and true entanglement on one board, spacelike Bell beyond 2 without a seed law. — §5–§8.
- [OPEN] What does not fit yet: freshness, the doublet's EP, the uniform-lapse drift, universality, the integrated ONE v1 run. — §10.4.

---------------------------------------------------------------------------------------------------------------------
## Evidence index (ALG-A, s24/ALG-A_work/; all read-only on the package)
- [NUMERIC] gear_demo.py → gear_demo.out / gear_demo.json: §1.4, §4.1–4.6.
- [NUMERIC] flip_check.py → flip_check.out: §1.6.
- [NUMERIC] energy_check.py → energy_check.out: §4.8, §6.1 B8.
- [NUMERIC] block_u1_listing.py → block_u1_listing.out: §3.10.
- [NUMERIC] block_example.py → block_example.out / block_example.json: §3.1, §3.5, §3.6, §3.9 (dynamics fingerprint b51d3f2c…cbfc8e8).
- [NUMERIC] Reference audit (15:16 UTC): every AGREE file (21 names) and every package / scratchpad file named in §1–§4 and
  §6–§10 exists on disk; the one exception is s23/AGREE_R5.md, which is cited only as pending.
