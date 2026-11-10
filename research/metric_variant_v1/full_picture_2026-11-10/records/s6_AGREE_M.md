# AGREE_M — Study 6 "the seed": twin agreement SEED-M1 × SEED-M2
- Skeleton and M1 column: SEED-M1, 09:42–10:0x UTC 2026-11-10 (`date -u`). Sources: s6/M1_FINDINGS.md (M1),
  s6/M2_FINDINGS.md (M2).
- Reproductions:
  - M1: s6/M1_work/M1_t1…t25.
  - M2: `cd s6/M2_work && python3 m2_verify.py`, 34/34 PASS, re-run by SEED-M1 at 09:41.
- Verdicts: AGREE / REFINE (agree after a stated change) / AGREED-OPEN (both say it is open, and why) / DISAGREE (both
  positions + a decisive check in BOTH codes).
- Labels: THEOREM / NUMERIC / DERIVED / OPEN.
- Notation map:
  - R_T (M2) = X2' (M1): matter G = J'K with the parity-preserving mirror M'.
  - R* (M2) = P_c∘X2' (M1), Π = W0 = β; M2's S* = J'Kβ = M1's W0·G (as matrices).
  - M2's "link-centred R* seed" = M1's S2*. M1's S* = M2's "twin 4-integer seed (c'')". Q = scaling of D = 6Q.
- **M2: please mark the last column of every row.**

## A. Foundations (both §0s)
| # | claim | M1 | M2 | proposed | evidence / decisive check | M2 mark |
|---|---|---|---|---|---|---|
| A1 | Seed criteria L/M/N/T/G as snapshot-checkable conditions (merged): L = C ≡ 0, Gauss ≡ 0 (+ NA, gravity), compact support, vacuum remainders reversor-symmetric and div r_A = 0; M = fewest nonzero integers (M1 also counts r ≠ r_vac); N = net charge/isospin/colour/momentum 0; T = fixed by an INVOLUTIVE exact reversor of the whole design, F^−t(s0) = R(F^t s0); G = every sector grows at the LINEAR level (fields ∝ A², slope test 2^8…2^16) | M1 §1 | M2 §0 | AGREE | wording merged | AGREE (M counts r ≠ r_vac too: accepted) |
| A2 | r mod 2 is an inert, conserved bit per gear (D even); the dynamics sees ⌊r/2⌋ with divisor 3Q | T0' THEOREM | L2 THEOREM | AGREE | M1 t1; M2 m2_verify | AGREE |
| A3 | a = b = 0 everywhere (any remainders) is a fixed point; remainder-only seeds are inert | T0 THEOREM | §1 (implicit) | AGREE | — | AGREE |
| A4 | Matter cannot be created from exact zero (no field, quartic or choice gear); also backwards. Proofs: fermion parity ψ → −ψ (M1); J'-rotation by π (−1 on matter, +1 on fields; M2), the same element | T1a THEOREM | §3.1 THEOREM + NUMERIC | AGREE | M2 m2_verify (10 fw + 10 bw); M1 T5 runs | AGREE |
| A5 | Matter and antimatter (V = JJ' = ±1) evolve independently at the linear level; an asymmetry can only be grown at O(1/A) (the "baryogenesis budget") | accept: V commutes with every block (free H, φV, (A+A)P_dJ', Wilson); M1 sees V₋ = V₊ exactly | §3.2 THEOREM | AGREE | M1 t8/t15 (V₋ = V₊ to the last digit) | AGREE |
| A6 | Every independent matter species (gauge-connected multiplet) that is to exist must be seeded | T1a | §3.1 corollary | AGREE | — | AGREE |
| A7 | Closed-board identity: Σ_x Gauss = (const)·Q exactly at every t; so legal ⇒ Q = 0 (a charged closed universe is illegal) | ΣG_int = −6dd·PM·Q', THEOREM | Σ𝒢 = κD_M·Q, THEOREM | AGREE: one identity; the residual's overall sign is a convention (𝒢_M2 ∝ −G_int,M1) | M1 t12 (0/5 failures); M2 m2_verify | AGREE (+: Σ_x δ²Φ = −Σ div(A − A_prev) = 0 identically, so the identity holds even without C ≡ 0) |
| A8 | Lorenz constant C = b_Φ − a_Φ + div a_A is exactly constant; C ≠ 0 drives Φ linearly (Study 4 C1) | §1 L2 | L4 | AGREE | both, every run | AGREE |
| A9 | Dressed Gauss: G(t+1) − G(t) = ∓κ·b(t)ᵀJ'(r(t) − r(t+1)) exactly (matter remainder only) | 0 failures in every run | 0 failures | AGREE | M1 t8/t15/t19; M2 ledger | AGREE |

## B. Reversors and fixed states
| # | claim | M1 | M2 | proposed | evidence | M2 mark |
|---|---|---|---|---|---|---|
| B1 | Per gear: time-even maps are flip (D−1−r) and M'/R' (D−2−r even, D−r odd), and no others of this form; time-odd maps are JR (r kept) and JR'. Self-mapped M-type gears are fixable only for odd Q at r ∈ {3Q−1, 3Q} (D = 6: the quiet {2,3}); paired gears are always fixable | R0 THEOREM | §2.1–2.2 THEOREM | AGREE | both | AGREE |
| B2 | Study 4's X_EM is Kramers (X F X F = −1 on matter): no state with matter is fixed by it, or by any Kramers class | THEOREM + 10/10 | THEOREM + 5/5 | AGREE | M1 t1; M2 m2_verify | AGREE |
| B3 | Non-Kramers classes. R_T: G = ±J'K, time only; needs odd Q_F (A self-mapped). R*: P_c∘X2', G = ±J'Kβ at node/edge(link)/face/cube centres; any Q with a balanced vacuum; odd Q for the uniform one | R1 table; also Π = W0J (S = J'·R_k·β, M1 t11 4/4 at all centres) | §2.4 (48 classes) | REFINE: add the R_k family; M2 to confirm it is among its 48 classes | M1 t11; M2 m2_rev | AGREE: confirmed, my 4 involutive PT reversors are ±J'R_jβ and ±J'R_kβ (m2_rev.json) |
| B4 | Fixed vacua: R_T fixes the uniform r = 3Q−1 iff Q is odd. R* fixes it for odd Q, and fixes a balanced (channel-paired) vacuum for any Q | M1 draft first said "node-centred needs odd Q"; WITHDRAWN 09:41: Γ pairs the channels of a self-mapped node, so balanced works | §2.2 | AGREE (M2's version) | M2 m2_verify ("fixed iff Q odd" for R_T) | AGREE |
| B5 | A moment is automatically neutral. Every reversor-odd two-time charge (J', both pair-isospin generators) vanishes; ρ'(x) = 0 node by node at t = 0; with vacuum fields it is Gauss-legal by construction. Momentum: forced to 0 by R_T (time-odd), NOT by R* (PT-even) | R2 THEOREM; S*: all 0 (t14) | §2.6 | AGREE | M1 t14; M2 m2_ledger | AGREE |
| B6 | Every fixed matter seed has ≥ 2 nonzero integers (S has no fixed channel); a seed fixed by BOTH R_T and R* is P-even, so ≥ 4 | lower bound in §5 | §2.7 THEOREM | AGREE | M2 m2_onenumber (9216 one-integer states × 48 classes: 0 fixed) | AGREE |
| B7 | M1's S* (b = A e0, A e1 on x0, x0+e_y; a = G·b) is fixed by R_T AND R*_link, hence P-symmetric. One node with Wilson: b = A(e0+e1), a = G·b (4 integers), same property | THEOREM + NUMERIC (t11, t21) | §5 (c'') | AGREE | both | AGREE (m2_twin4; one-node 4-integer: m2_decisive, fixed by R*_node and R_T, both bounces exact) |
| B8 | Click view: the click log before the bounce is the reversor image of the log after it (update t ↔ −t−1, node σx, channel π(i), size ×sign) | S* 60/60 steps, 142,936 clicks; S2* 80/80 steps, 227,038 clicks | node R* 40/40 (m2_arrow) | AGREE | M1 t12, t15; M2 m2_arrow | AGREE (mine: counts 40/40 + the record-level identity ell(x,i) = s_i·ell(σx, π(i))) |
| B9 | Two-headed arrow: a compact seed is a footprint minimum, and R* makes the halves exact mirrors; a dense random state has no arrow | — (not run) | §4 NUMERIC | AGREE (M1 accepts M2's runs) | M2 m2_arrow | AGREE |

## C. Growth and selection rules
| # | claim | M1 | M2 | proposed | evidence / decisive check | M2 mark |
|---|---|---|---|---|---|---|
| C1 | **T4 + Wilson qualifier.** Without Wilson, every neutral one-node seed is EM-inert at the linear level (ρ'(x,t) = κ(x−x0,t)·ρ'(x0,0); proof via h(k)² = λ²·1 and the staggered block structure). With Wilson the γW0·βP cross term sources ρ' ∝ A² | THEOREM + NUMERIC (448/448 exactly 0; 192/448 with Wilson, slope 2.00) | §3.5 table: node R* field-free without Wilson, generative with it | AGREE | M1 t5, t18, t19; M2 m2_wilson, m2_verify | AGREE (re-derived independently from h² = λ²·1, my §3.4) |
| C2 | **Sublattice / direction rule** (Wilson-free). (i) THEOREM: a node's linear propagator reaches only x0 + {≤ 1 odd coordinate}, so two seed nodes with displacement ≡ (1,1,1) mod 2 never interfere. Hence EVERY cube-centred R* pair (c − 2x ≡ (1,1,1)) is exactly inert. (ii) NUMERIC, sharper: a two-node PT pair b(x0) = A e_i, a(x0+δ) = A·Γ·e_i with Γ = β·J'·R_q generates iff δ ≡ e_y (q = j: M2's S* = J'Kβ) or δ ≡ e_z (q = k: the W0J family) mod 2. It gives 16/16 channels in that class and 0/16 in every other class, (0,0,0) and (1,1,1) included. With Wilson every class generates | THEOREM (i) + NUMERIC (ii): t24, t26 (M2's far cube pair x0 = (2,3,1), −x0−1: exactly 0 Wilson-free, 134 with Wilson), t26b (R_j: (0,1,0), (2,1,0) 16/16; all others 0/16), t26c (R_k: (0,0,1), (2,0,1) 16/16; others 0/16) | (c*) "with Wilson only"; (c) far cube pair "generative after the halves meet" (default setup has Wilson on) | REFINE: (c) is generative only through the Wilson term (M1 check done; M2 to confirm in m2_seed with wr = wn = 0) | M1 t24, t26, t26b, t26c | AGREE (re-entered 09:55:11 UTC). Both parts confirmed in MY code: (i) far cube pair and cube diagonal, Wilson OFF, L = 12, T = 40: fixed, exact bounce, fields/charges exactly 0 (m2_agree_checks.py); (ii) direction rule, Wilson OFF, linear level: R_j generates 16/16 iff δ ≡ e_y (also (2,1,0)), R_k 16/16 iff δ ≡ e_z (also (2,0,1)), every other δ 0/16, (0,0,0) and (1,1,1) included (m2_direction_rule.py). Consequence for (a): S2* with S* = J'R_jβ must sit on a y-link (or use J'R_kβ on a z-link) to be Wilson-robust |
| C3 | **Charge flicker** (ρ' = 0 at every even t, linear level) | THEOREM for R_T seeds with matter in ONE 8-block and pairwise K-orthogonal node vectors (S*, all single-channel seeds): ρ'(x,t) = −(U_{t−2}Kb0)_x·(U_t b0)_x; at even t both factors are scalar kernels because h² = λ² (with or without Wilson). Counterexample to "every": random 64-node a = G·b seeds give even-t ρ' = 5.4e−3 vs odd 4.8e−3 | "every R_T-fixed seed" (NUMERIC m2_linear_all); mechanism OPEN; chiral Γ ruled out (agrees with M1) | DISAGREE on "every" → proposed REFINE to M1's statement | decisive in BOTH codes: a random multi-node R_T seed (M1 t22: no flicker); M2 to run the same in m2_linear_all | REFINE → AGREE: I WITHDRAW 'every'. Joint THEOREM = M1 scope (one 8-block, pairwise K-orthogonal nodes) ∪ M2 scope (one node, b0ᵀP_dJ'b0 = 0 ∀d, e.g. e1+e9). Decisive (m2_agree_checks*): random 64-node 2.78 vs 2.76; (1,1,1), (1,3,1) flicker (≤ 4e-19); (1,3,5) with e5·Ke1 = 1 does not |
| C4 | Exact net Q = 0 for all t | node-centred R* seeds and S4c: Q ≡ 0 for 40 updates; link S2* and S* drift O(A) (t25) | node R* seeds exactly 0 (80 updates); link seed drifts O(A); mechanism OPEN (no exact symmetry fixes the seed, m2_symQ) | AGREED-OPEN (the phenomenon agrees in both codes; the mechanism is open) | M1 t25; M2 m2_Qexact2, m2_symQ | AGREED-OPEN (m2_Qexact2: all 16 single-channel node seeds exact 0; generic R*-fixed and the link seed drift O(A)) |
| C5 | Generativity strengths (design-relative couplings). Node R* with Wilson: ρ' ~ 0.02 A²; link S2*: ~0.1 A² (~5× stronger), with and without Wilson; S* and R_T seeds: flicker-weakened (11–46× weaker); all fields ∝ A² | slopes 2.00 (t18, t19); S2* Σ\|ρ'\| ≈ 0.3 A² at t = 2 | §3.4, §3.5 | AGREE | both | REFINE: '~5×' → 2.4–5.3× by measure (m2_decisive, Wilson on: max ρ' 5.3×, Σ|ρ'| 2.4×, |A| 3.0×, |Φ| 3.5×); rest AGREE |
| C6 | C-symmetric / one-block seeds (incl. the one-unit seed (a)) are EXACTLY EM-dead, rounding included | T5 THEOREM | (a) "nothing, ever" | AGREE | M1 t2, t6; M2 m2_seed | AGREE |
| C7 | **Dirac energy.** Every point/compact seed tested has total Dirac energy 0 (half positive, half negative branch). M1's "J-carrier" seeds have E_J ≠ 0, but E_J measures the J-sense (physical vs time-doubler), NOT the energy sign: E_H = ΣaᵀJ(Hb) = 0 at t = 0 | M1 WITHDRAWS (09:40) "S4c = energy for gravity". The branch-sensitive single-time energy E₁ = Σ bᵀHb is 0 for every point seed and +0.95·mc·A² for the P+ seeds (t28). The two-time E_H is 0 at any time-symmetric moment (J-sense balance), so E₁ is the right measure | §7.1 (⟨e_i\|P+(k)\|e_i⟩ = ½) | AGREE (M2's statement) | M1 t25, t28; M2 m2_posenergy | AGREE |
| C8 | Seeds of the full design (prepared, not run): links, gravity and detectors are created from matter bilinears; the quartic never creates; the R* rules for gravity, links and L0 are DERIVED | creation table §2 | §2.5, §3.3 | AGREED-OPEN (not built) | stage-1 package | AGREED-OPEN |

## D. The manager's items (a)–(i)
| # | item | M1 | M2 | proposed joint line | evidence | M2 mark |
|---|---|---|---|---|---|---|
| (a) | ONE recommended seed | see below | node R* (in the design), S2* "robust" | **S2*** (see below) | M1 t15, t18; M2 §3.5, §5 | AGREE: S2* (criterion 3 — Wilson-robust — above n_nodes accepted); strength per C5 |
| (b) | shared phases: who needs what | §7 | §4 (quiet vacuum) | see below | M1 t17 | AGREE (= my refined §4) |
| (c) | even-t ρ' = 0 | THEOREM (restricted) | "every R_T seed", OPEN mechanism | C3 | M1 t20, t22, t23 | AGREE via C3 (joint scope) |
| (d) | gravity on the always-closed board: sign, remedy, data-only | §4 + owner input | §1.3–1.4 | see below (rewritten after the owner input) | DERIVED | REFINE per OWNER DECISION 09:45 (closed board): see H-(d) |
| (e) | positive energy and the count | C7 | §7.1 | see below | M2 m2_posenergy | AGREE + REFINE: see H-(e) (remainder texture vs A1's div r_A = 0) |
| (f) | all-forces seed: integer count | §5 (d) | §5 (e) | see below | — | AGREE |
| (g) | L0 vs Dirac pair | T1a | §3.3, §5 (d) | see below | — | AGREE |
| (h) | vacuum convention | odd Q, r = 3Q−1 | odd Q, r = 3Q−1; random vacuum = arrow fuel but no shared phases | see below | M2 m2_arrow | REFINE wording to the package's ONE Q: see H-(h) |
| (i) | merged test spec | TS-1…10 | S1…S12 | §E | — | AGREE + API names and two additions: see H-(i) |

**(a) The recommended seed (proposed joint line).** Ranking criteria, in this order:
1. legal: exact C ≡ 0 and Gauss ≡ 0, compact support;
2. exact bounce under an involutive reversor of the whole design;
3. generative at the LINEAR level in the design (Wilson on) AND not dependent on the doubler-removal (Wilson) term, which is a
   lattice artefact that vanishes in the continuum;
4. neutral (forced anyway: A7, B5);
5. supports the choice-gear shared phases that the design uses ((b));
6. compatible with gravity (energy, (d)/(e));
7. fewest integers;
8. field strength.

Under 1–4 and 7, the node R* seed (1 node, 2 integers) and S2* (2 nodes, 2 integers) tie on integers. S2* wins on criterion 3
(Wilson-robust, 2.4–5.3× stronger by measure (C5), its charge separation comes from ordinary hopping interference). The node seed separates charge
only through the Wilson cross term. **Recommendation: S2*.**
- Definition: b(x0) = A·e_i, a(x0 + e_y) = A·(J'Kβ)·e_i (K = R_j; equivalently J'R_kβ with e_z — the C2 direction rule:
  other link directions are Wilson-free inert); everything else is the uniform odd-Q vacuum (L0 at 2Q, new layers at 3Q−1); A ≫ 1
  (2^12…2^16).
- It is fixed by R* about the link centre.
- Alternatives:
  - node R*: minimal in nodes, in the design only;
  - the both-reversor 4-integer seed: P-symmetric, so mirror-detector shared phases; flicker-weakened;
  - the P+-projected seed: the only positive-energy one; ~600 integers, ~50× weaker, needs prepared Coulomb data, see (e).
- Its two known limits (both codes): zero Dirac energy (half negative branch) and PT-only symmetry, see (b) and (e).

**(b) Shared phases: which needs what (proposed).**
- (b1) A same-link PAIRED clock (S5: both clocks read ONE input by tensor construction) needs only equal remainders at birth.
  The uniform quiet vacuum supplies them. No seed symmetry is needed. (M2's statement holds here.)
- (b2) Detectors at x and σx (each reads its own local \|ψ\|²) need equal birth remainders (uniform vacuum) AND equal drives at
  equal times. That needs a SPATIAL symmetry σ of the seed.
  - NUMERIC: S* (P-symmetric) gives identical drives 31/31; S2* (PT only) 0/31; a PT seed pairs x at t with σx at −t.
  - (M1's statement holds here.)
  - So mirror-detector phases need the P-symmetric 4-integer seed, or a P-symmetric matter configuration grown later.
- (b3) The F7 far side reads Alice's choice FRONT. Its correlation is carried by the front, not by a vacuum phase. It needs only
  causal contact and the "typicality" of its own hidden phase (Born weights). Nothing from the seed beyond a quiet vacuum,
  and the typicality is OPEN.

**(c) Even-t ρ' = 0.**
- THEOREM (M1) for R_T-fixed seeds with matter in one 8-block and pairwise K-orthogonal node vectors. This covers every
  single-channel R_T seed, including S* and M2's R_T one-node seed.
- Not true for every R_T-fixed state: a random multi-node a = G·b state is a counterexample (M1 t22).
- Proof (M1 §3, M1_FINDINGS "Charge flicker"). Write X(t) = U_t b0 and Y(t) = U_{t−1}K b0. Then
  ρ'(x,t) = −(U_{t−2}Kb0)_x·(U_t b0)_x. At even t both factors are even polynomials in h, hence scalar kernels (h² = λ²·1, with
  or without Wilson). So ρ'(x, even t) = −Σ e_{t−2}(x−y)e_t(x−z)(Kb0(y))·b0(z). This vanishes for K-orthogonal node vectors.
- Decisive check for M2: run m2_linear_all on a random multi-node R_T seed.

**(d) Gravity on the ALWAYS-CLOSED board.** OWNER DECISION 09:45 UTC: "closed board", recorded in s0/SYSTEM_DESIGN_v5.md §11.
Only closed-board-legal remedies are recommended below, both as prepare/ data.
- **Sign.** The two drafts state the same identity with opposite residual conventions (M1: ΣG_H = −κE; M2: Σ𝒢_g = +κ_g E).
  With OD2 accumulators Σh̄^{00} (and Σh̄^{0i}) are exactly constant. So, on the closed board, **strict legality (every
  constraint residual = 0) ⇒ total energy E = 0** (and total momentum = 0). THEOREM-level once OD2 is built as specified;
  DERIVED now.
- **The open board is NOT a remedy.** "L > 2cT" survives only as a numerical TEST DEVICE: a causal window in which runs on L and
  2L must agree. It is labelled that way in T13.
- **Three candidates compared:**
  1. **E = 0 seeds** (S2*, node R*, every compact 2-integer seed: E_H = 0 exactly, M1 t25 and M2 §7.1). Strictly legal,
     compact, minimal.
     - Their zero comes from **negative-branch matter**: exactly half the content has negative Dirac energy.
     - This is NOT the GR closed-universe zero, where positive matter energy is balanced by NEGATIVE GRAVITATIONAL (field/
       binding) energy.
     - With a Dirac-energy stress the negative half would gravitate repulsively (Study 4 A3), so physically doubtful.
  2. **R-a = the mean-subtracted Hamiltonian constraint** (the periodic-box cosmology convention: Poisson with the mean density
     removed).
     - Every k ≠ 0 constraint mode is satisfied EXACTLY.
     - The k = 0 component carries ONE declared number, the uniform residual −κĒ per node (Ē = E/N).
     - It is conserved exactly (dressed identity), and force-free (k = 0).
  3. **M2's "k = 0 mode read as cosmology"** is the SAME OBJECT as R-a: the k = 0 component of the gravitational source.
     - On the OD2 accumulator board this mode cannot evolve (Σh̄^{00} is exactly constant), so the "cosmology" is a STATIC
       uniform background, i.e. exactly R-a. The t² growth M2 mentions arises only if h̄^{00} is a wave gear (no exact
       Hamiltonian accumulator).
     - Outside the seed question (not proposed): an evolving (Friedmann-like) background, or a GR-like balance by negative
       field energy, would change the LAW (nonlinear gravity), not the initial data.
- **Recommended remedy (proposed joint line): R-a** for positive-energy matter, and NO remedy for the E = 0 seeds. Its points:
  - *Legality:* legal in the cosmological sense: all k ≠ 0 residuals 0, plus one declared k = 0 background. Strict legality
    with E > 0 is impossible in the linear design (THEOREM above).
  - *Integrality:* Ē = κE/N is an integer iff N | κE. Otherwise distribute the residue κE mod N as −1 on a REVERSOR-SYMMETRIC
    node set.
    - An R*-fixed seed has R*-even T^{00}. Edge/cube-centred R* has only 2-orbits of nodes, so E is even and an even residue
      set always exists.
    - The residue part is not exactly k = 0: it exerts forces at the O(1)-quantum level, a relative 1/(κE) effect.
  - *Pure prepare/ data:* the declared residual and the field data that realise it are initial data written by prepare/. The
    tensor is unchanged (AGENTS 9).
    - Realisation: integer h̄^{0i} "velocity" links w and remainders r with 6Q·div w + div r = −κ(T^{00} − Ē). This is solvable
      on the torus because Σ(T^{00} − Ē) = 0; the remainders fix the residues mod 6Q, as in the EM construction of (e).
  - *Clocks:* the uniform part is unobservable in clock ratios. The k = 0 lapse is frozen by the accumulator (prepare it as 0).
    Clocks feel only the mean-subtracted field of the seed.
  - *L0:* bit-identical to today's board. L0 is uncoupled in v5, and without a seed E = 0, so nothing is prepared.
  - *Criteria:*
    - "Vacuum outside the seed" is violated in the GRAVITY data. The mean-subtracted field fills the board (O(N) nonzero h̄^{0i}
      entries): every node must carry flux.
    - "Minimal" holds in FREE choices: the matter integers plus ONE number Ē. The board-wide field is determined by them, not
      chosen; in support it is not minimal.
    - So R-a is the price of positive energy on a closed board.

**(e) Positive energy and the integer count.**
- For EM alone, "minimal = 2 integers" stands.
- For the FULL system with gravity (positive gravitational charge for matter and antimatter), the point seeds are unphysical.
  Their single-time Dirac energy E₁ = Σ bᵀHb is 0, half of it on the negative branch, which would gravitate repulsively.
- The physical seed is the P+-projected one, which stays R*-fixed because P+ commutes with R*.
- **With gravity, therefore, the minimal physical seed is NOT 2 integers.** Hundreds to ~1700 integers, depending on A and the
  truncation: M2 has 616 (Wilson) / 124 (no Wilson) at 2^16; M1 rounds without truncation, 926–1670 for 2^12–2^16. The true
  minimum is OPEN.
- Own-code NUMERIC (M1 t27/t28, Wilson-free, odd Q): E₁ = +0.95·mc·A² in both slots; exactly R*-fixed; exact bounce 20/20.
  - The node P+ seed has ZERO ghost charge, so it is exactly legal with zero fields. But it is EM-inert Wilson-free: its data are
    f(h)·e₀, so T4 applies. With Wilson, M2 finds a small ghost (2.4e−5 A² on 38 nodes) and growth.
  - The link P+ seed is generative (slope 2.0) but carries a ghost charge of 4.6% A² on 212–412 nodes (M2 ≈ 2%). It needs
    prepared field data.
- Exactly legal P+ seed: DERIVED solvable. Net Q is exactly 0 (both codes).
  - Choose b_Φ = 0 and an integer longitudinal link field w = b_A − a_A with 6PF·div w + div δr_A = −6dd·ρ'. The torus flux
    network exists because Σρ' = 0, and remainder textures δr_A carry the residues mod 6PF.
  - R*-fixedness needs w mirror-symmetric, with a_A(x) = −b_A(σ'x). On a SELF-mapped link w = 2b is even, so an odd flux
    through the central link must be routed partly through remainder textures (each node can absorb up to about ±18PF).
  - Explicit construction OPEN: pre-registered as T14/S12.

**(f) All-forces seed.** Two integers per independent matter multiplet:
- the Dirac pair (EM + its pair isospin {J', σx⊗J, σz⊗J}, both zero at the moment): 2;
- colour-triplet matter, if a separate species: its own 2 (DERIVED, not built);
- L0, if its content is wanted: its own seed (count OPEN, see (g));
- gravity: no charge to cancel, but the energy remedy (d), plus (e) for positivity.

EM + isospin + colour therefore needs 4 integers (two species). The minimum with gravity is OPEN (e).

**(g) L0 (today's 48-channel board).**
- YES, today's board content needs its own seed in the full system. L0 enters every coupling linearly (c1/c2 links: U·b with
  source b·b), so neither L0 nor the Dirac pair can create the other.
- A mixing block (e.g. a rank-2 L0↔Dirac term) would be a new law: an OWNER decision.
- Recommendation: NO mixing block (it would change today's board). Seed L0 separately when its content is wanted. E17's
  JR-fixed s* lifts unchanged while L0 is decoupled; under a common spatial map, re-symmetrise it with R0 = JR∘Π0∘P (M2).

**(h) Vacuum convention.** The vacuum remainders are initial data, so this is an OWNER choice of the preparation. Odd Q is a
build parameter.
- Joint recommendation: odd Q for every scaled gear, with the quiet uniform central vacuum r = 3Q−1. It is the scaled form of
  today's quiet r = 2.
- Why:
  - it is fixed by R_T and R*;
  - it is Gauss-legal (div r_A = 0);
  - it keeps the vacuum-born shared phases (b1);
  - the whole history is then a function of the tensor and two integers;
  - the arrow is Boltzmann's coarse-grained footprint growth, two-headed about the bounce.
- A random hidden vacuum would fuel record entropy (M2 T13b) but destroys the shared phases and needs R-symmetry and
  div r_A = 0 to stay legal and bouncing.

## E. (i) ONE merged test spec for the seed physicists
To run against the stage-1 package API:
- seed data only in `prepare/`;
- reads only via `observe/`;
- reversor maps from `core/reversors.py`.

Common declarations: odd Q per gear; vacuum r = 3Q−1 (L0 at (0,0,2)); A = 2^12, 2^14, 2^16; L and 2L (even L); T ≥ 2L;
Wilson ON (the design) and OFF (Study 4 E1); `date -u`; pre-register.

| # | test | seeds | pass criterion | origin |
|---|---|---|---|---|
| T1 | vacuum identity | vacuum | fixed point (1 and 100 updates, bit for bit); L0 part = universe24 bit for bit; R(vac) = vac for R_T (odd Q) and R* | M1 TS-1, M2 S1 |
| T2 | legality at t = 0 | all | C ≡ 0, Gauss ≡ 0 (integer, with remainders), NA-Gauss ≡ 0, gravity harmonic and momentum ≡ 0, Hamiltonian = declared uniform background (d) | TS-2, S2 |
| T3 | closed-board identity | all + charged control | ΣGauss = (const)·Q at every t; the charged one-node control fails T2 | TS-2, S3 |
| T4 | reversors | random coupled states | R F R F = id for R_T, N∘R_T, R* (S = J'Kβ and J'R_kβ) at node/link/face/cube centres; X_EM gives −1 on matter; with and without Wilson; then with gravity, links and detectors added | TS-3, S4 |
| T5 | fixedness + exact bounce | S2*, node R*, S*, P+ seed (S12), cube-centred R* | R(s0) = s0 on ALL layers; F^−t(s0) = R(F^t s0) for t ≤ T; exact rewind | TS-4, S4, S5 |
| T6 | ledger along the run | all | r mod 2 unchanged; accumulator remainders unchanged; C ≡ 0; G(t+1) − G(t) = ∓κR_m; Q_T(−t) = −Q_T(t) for J' and both isospin generators; energy even; ΣΦ constant | TS-5, S6 |
| T7 | growth (linear level) | S2*, node R*, S*, P+, cube R*; controls: unit, C-symmetric, charged | slopes over A of max\|A\|, max\|Φ\|, max\|ρ'\|, Σ\|ρ'\| = 2 ± 0.05 for generative seeds. Wilson OFF: node R* and cube R* exactly field-free, S2* generative. Controls: unit and C-symmetric exactly 0. Report V₋ = V₊, net Q (node seeds exactly 0), transverse fraction, field front speed vs c_Q | TS-6, S7 |
| T8 | selection rules | R_T seeds; PT pairs | flicker: ρ'(even t) at rounding scale for single-block K-orthogonal R_T seeds, NOT for a random multi-node R_T seed; Wilson-free direction rule: a PT pair with Γ = βJ'R_j generates iff δ ≡ e_y, with βJ'R_k iff δ ≡ e_z (mod 2), all channels; cube-centred pairs inert | M1 C2, C3 |
| T9 | matter-vacuum invariance | ψ = 0, random fields | matter stays exactly 0 for T updates, forward and backward; unseeded species stay 0 | TS-9, S8 |
| T10 | click view | S2*, node R*, S* | record-level mirror (t, x, i) ↔ (−t−1, σx, π(i)), sizes ×sign, kinds kept/swapped per sign; 0 unpaired; footprint minimum at the bounce; dense random control: no arrow | TS-7, S9 |
| T11 | hidden-vacuum ensemble (optional) | S2* | quiet vacuum gives 1 record; random R*-symmetric r_h gives distinct records, Hamming distance growing | S10 |
| T12 | shared phases | S* and S2* with \|ψ\|² detector pairs and one same-link paired clock | same-link clock: equal remainders always; mirror detectors: equal for S* (P), not for S2*; λ histogram at decisions | TS-10, (b) |
| T13 | gravity (after OD2) | P+ seed, S2* | ΣG_H identity; strict legality possible iff E = 0 (S2*); R-a: the declared uniform residual stays uniform (dressed) and k ≠ 0 residuals stay 0; E_H vs ΣT^{00}; clock ratios unaffected by the uniform part. TEST DEVICE only (not a remedy): L vs 2L records identical inside the causal window t ≤ (L − d)/2 | TS-8, S11 |
| T14 | positive-energy seed (S12) | P+-projected S2* and node R* + compact integer flux network | exactly legal (T2), R*-fixed (T5), then T6–T7; count its integers | S12, (e) |

## F. OWNER DECISIONS (joint recommendation first)
0. **DECIDED by the owner (09:45 UTC):** the board is always the closed periodic cube. The open board is rejected and is used
   only as a numerical test device (T13).
1. **Vacuum and Q:** ONE odd Q for the whole system (the package has one divisor). The vacuum is L0 gears at (0,0,2Q) (the
   Q-scaled reference (0,0,2), kept by the L0 time-odd map "JM"/"rhoL0") and every new-layer gear at (0,0,3Q−1) (kept by
   "Mp" = R' iff Q is odd). Alternative: a random hidden vacuum, legal only with random MATTER remainders and div r_A = 0 (arrow
   fuel, no vacuum-born shared phases). [M2 H-(h), accepted by M1]
2. **The seed:** S2*, two integers on two neighbouring nodes (along y for S* = J'R_jβ; C2), fixed by the link-centred PT reversor. Alternative: node R*
   (one node, two integers; generative only through the Wilson term).
3. **Gravity's energy on the closed board** (closed board = owner DECISION 09:45, recorded in v5 §11). Only closed-board-legal
   remedies, both pure prepare/ data:
   - **(i) recommended for positive-energy matter: the uniform k = 0 background datum (R-a).** One declared number Ē; every
     k ≠ 0 constraint exact; static and force-free on the OD2 board; invisible to clock ratios; L0 untouched.
   - **(ii) E = 0 seeds** (the 2-integer seeds): strictly legal with no datum, but the zero is negative-branch matter, not GR's
     balance by gravitational energy.
   - The joint recommendation is (i) together with the positive-energy seed of item 4. (ii) is acceptable only for an EM-only
     universe.
4. **Positive energy:** for a gravitating universe, adopt the P+-projected seed with a compact integer flux network
   (pre-register S12). Alternative: accept the point seed (half negative branch: repulsive gravity for that half).
5. **Today's board (L0):** no mixing block; seed L0 separately when its content is wanted. Alternative: a mixing block (a new
   law).
6. **Wilson term:** kept in the matter block (manager's instruction to B1-EM). The recommended seed S2* works with and without
   it.

## G. Six lines for the owner
1. The whole system is the rule, the one tensor and a seed. The tensor can grow light and every force field from matter, but it
   can never create matter, so the seed must contain matter.
2. On a closed board the seed must be exactly neutral. Every exact constraint (Gauss, Lorenz) forces net charge zero, and a
   time-symmetric seed has every charge zero automatically.
3. The smallest correct seed is two integers: one value on a node and its mirror one step earlier on the neighbouring node. The
   board then runs as an exact bounce, its past the mirror of its future, as in E17.
4. From those two integers the tensor alone grows matter and antimatter in equal amounts, their separation, the Coulomb field
   and light. The observer's clicks before and after the bang are mirror images.
5. Gravity adds one condition: on the closed board total energy must balance.
   - The two-integer seed does so only through equal negative-energy content.
   - Real positive-energy matter needs one declared uniform background number: pure initial data, no force.
   - It also needs a larger seed: about 2000 integers, built exactly in M1 t29. Its true minimum is open.
6. Owner choices: odd Q with a quiet uniform vacuum, the two-integer seed, the uniform background for gravity, and a separate
   seed for today's 48-channel board.

## H. SEED-M2 marks — notes and decisive checks (SEED-M2, 09:46–09:55 UTC, `date -u`)
Decisive checks run in MY code for this table: `s6/M2_work/m2_agree_checks.py`, `m2_agree_checks2.py` (C2, C3),
`m2_decisive.py` (C5, (a)), `m2_arrow_legal.py` ((h), T11). All other evidence as cited in M2_FINDINGS.

**H-(d) Gravity on the closed board (OWNER DECISION 09:45: "closed board").** Proposed replacement text for row (d):
- Signs: one identity; Σ_x G_H = −κE (M1 convention) ≡ Σ_x 𝒢_g = +κ_g E (M2 convention). With OD2 accumulators Σ_x h̄^{00}
  is exactly constant, so legal ⇒ E_total = 0 on the closed board.
- Only closed-board-legal remedies are recommended. ONE remedy: **R-a, the declared uniform k = 0 background datum**
  (= M2's "prepared uniform background"):
  - integrality: κE/N is an integer iff N | κE; with A = 2^k, L = 2^m and an integer bilinear stress (κE ∝ A²) this is
    arranged by the choice of A and L (prepare data); otherwise the residue κE mod N goes on a σ-symmetric node set as
    unit entries (R*-even; with a cube centre the residue count must be even), leaving k ≠ 0 parts of size 1/N;
  - pure `prepare/` data: the value of an exactly conserved (dressed) constant; no tensor entry, no law;
  - clocks: k = 0 only, so no force; Σh̄^{00} stays at its initial value (set 0), so no uniform lapse offset arises, and any
    uniform offset would be invisible in clock RATIOS;
  - L0: untouched, bit-identical to today's board (the datum lives in the gravity layer's constraint data);
  - "vacuum outside the seed" / minimal: one extra uniform number; the matter/EM seed stays compact, but the prepared h̄
    data carry the flux of T^{00} − Ē over the board (the seed's own periodic Newtonian field, fully determined).
- The k = 0 "cosmology" reading: R-a IS the periodic-box cosmology convention (Poisson with ρ − ρ̄; the k = 0 part is the
  background). A GROWING k = 0 mode is NOT available with OD2 accumulators (Σh̄^{00} frozen); it would need a
  non-accumulator h̄^{00} (a law change), so it is not a seed option.
- E = 0 seeds (the only other closed-board-legal option, also prepare/ data): their zero comes ENTIRELY from negative-branch
  (time-doubler) content — half positive, half negative Dirac branch (M2) = E_H(0) = 0 (M1 t25). Unlike GR's closed
  universe, where positive matter energy is balanced by gravitational field energy. Not recommended.
- "L > 2cT" appears only as a numerical test device (causal patch), never as a remedy.
- NUMERIC support, EM analogue of R-a (SEED-M2 `m2_jellium.py`, 09:50; gravity itself is DERIVED): a CHARGED one-node seed
  (Q = −A² = −4.29e9, L = 8) made legal up to ONE uniform constant u = 48κQ/N: integer flux W with div W = f exactly,
  Lorenz C = 0, Gauss ≡ u at t = 0, prepared field on 511/1536 links (non-compact, as stated), dressed identity exact at
  every node for 30 updates (deviation from u = the matter-remainder dressing, 1.9e-5 relative), exact rewind.

**H-(e) Positive energy.** AGREE that with gravity the minimal physical seed is not 2 integers and that the true minimum is
OPEN. One refinement to the solvability derivation: it fixes the residues mod 6PF with div r_A, i.e. with an A-remainder
TEXTURE (div r_A ≠ 0), which row A1 (and M1's L3) excludes as a hidden polarisation charge. So T14 must state which holds:
(i) A1 relaxed for prepared Coulomb data (the texture is then an exactly accounted Gauss term), or (ii) the P+ seed is
built with PF | dd·ρ'(x) at every node (uniform r_A), or (iii) a non-compact integer flux in w alone. Solvability in my own
normalisation additionally needed λ_src | κD_Mρ' (true for PM ≡ 0 mod 8): normalisation-dependent; the package's should be
checked in T14.

**H-(h) One Q.** The package has ONE divisor for the whole system (README "ONE divisor, read literally"). Replace "odd Q for
every scaled gear" by: **one odd Q; vacuum = L0 gears at (0,0,2Q) (the Q-scaled reference (0,0,2), fixed by the package's
"rhoL0" map and by JR) and every new-layer gear at (0,0,3Q−1) (fixed by "Mp" = R' iff Q is odd; package T0.15).** The
hidden-vacuum alternative is legal only with random MATTER remainders (or div-free A remainders): m2_arrow_legal gives the
same result (10/10 distinct records, Hamming 7 → 2833, Gauss constant 0).

**H-(i) Test spec.** AGREE with §E. Use the package names (`core/reversors.py`, per-gear maps): "Mp" = (b, a, R'(r)) for
the new b-only layers; "rhoL0" for the L0 time mirror (fixes 2Q); for the vacuum-keeping time-odd maps (A links under
R\*, L0 under R0 = JR∘Π0∘P) use **"JM" = (−b, −a, r)** — the package's "JR" = (−b, −a, r xor 1) flips the inert bit
and fixes neither 2Q nor 3Q−1. Matter part of R\*: `SpatialMap` ∘ `GroupLinearMap(S*, neg_r="Mp")` ∘ "Mp" on the
16 matter gears (a −1 entry then keeps r: R'∘R' = id); `SpatialMap(tensor, S)` (x → S − x, links re-based; link centre S = 2x0 + e),
`inversion_about_node`, `inversion_about_cube_centre`; `GroupLinearMap` for S* = J'Kβ on the 16 matter channels;
`reversor_check`, `is_fixed`; `prepare.vacuum_state`, `prepare.em.set_matter/set_field`; `observe.em.charge_density`,
`link_currents`, `lorenz_C`, `gauss_Y`, `gauss_step_residual`, `remainder_term`, `click_sizes`. Additions:
- T1: L0 vacuum (0,0,2Q) in the scaled form;
- T11: randomise matter remainders only (div r_A = 0), else the vacuum is illegal;
- T13: the causal patch L > 2cT is a numerical test device only (owner 09:45).

**H-F (OWNER DECISIONS).** #1 → "one odd Q; L0 at 2Q, new layers at 3Q−1" (H-(h)). #2 AGREE (S2*). #3 → per the owner's
09:45 decision: "a declared uniform k = 0 background (prepared data, conserved, force-free). Closed-board alternative: E = 0
seeds (zero from negative-branch matter; not recommended). No open board." #4 AGREE with H-(e). #5, #6 AGREE.

**H-post-signature edit (09:55 UTC, SEED-M2, consistent with rows C2/C5 as accepted in I):** row (a) text now says
2.4–5.3× and fixes the S2* link direction (e_y for J'R_jβ, e_z for J'R_kβ).

**H-G (six lines).** AGREE. Suggested line 5: "Gravity adds one condition: on the closed board the total energy must
balance. The remedy is one declared uniform background number — pure initial data, no force. A truly positive-energy seed
is larger (hundreds of integers) and is the open next step."

## Signatures
- SEED-M1: column filled 09:42–09:53 UTC. All of M2's REFINEs accepted (section I). **Signed by SEED-M1 at 09:54 UTC
  (`date -u`)**, pending only M2's re-entry of the C2 mark lost in the edit collision.
- SEED-M2: all 35 rows marked 09:47 UTC; notes H added 09:47–09:50; C2 re-entered 09:55:11 UTC after the edit collision.
  SEED-M1 accepted every REFINE (section I), including S12 constructed with option (ii). No DISAGREE remains.
  **Signed by SEED-M2 at 09:55:11 UTC (`date -u`).**

## I. SEED-M1 responses to M2's marks (SEED-M1, 09:53–09:54 UTC, `date -u`)
- **A7:** ACCEPT M2's extension. Φ_next − 2b_Φ + a_Φ = −div(b_A − a_A) holds identically for the accumulator, so ΣD_ttΦ ≡ 0 and
  ΣGauss = (const)·Q holds WITHOUT assuming C ≡ 0.
- **B3:** ACCEPT: the involutive PT classes are exactly ±J'R_jβ and ±J'R_kβ (both codes).
- **C2:** M1 asks M2 to re-enter its mark (lost in the 09:47:51 rewrite). M1's evidence:
  - M2's far cube pair (2,3,1) ↔ −x0−1 is exactly 0 Wilson-free and 134 with Wilson (t26);
  - the direction rule R_j ↔ e_y and R_k ↔ e_z gives 16/16 vs 0/16 (t26b, t26c).
- **C3:** ACCEPT the joint scope, M1's (one 8-block, pairwise K-orthogonal nodes) ∪ M2's (one node, b0ᵀP_dJ'b0 = 0 ∀d). Row C3
  verdict: AGREE (REFINE resolved). The decisive checks agree in both codes: random 64-node, no flicker (M1 t22 5.4e−3/4.8e−3;
  M2 2.78/2.76).
- **C5:** ACCEPT "2.4–5.3× by measure" in place of "~5×". (a) text: "S2* is 2.4–5.3× stronger than node R* (with Wilson)".
- **(d):** ACCEPT M2's H-(d) as the joint text. It coincides with M1's (d): the same identity, R-a = the declared uniform k = 0
  background = the periodic-box cosmology convention, no growing k = 0 mode on OD2, E = 0 seeds = negative-branch zero, and
  the open board a test device only.
  - M2's integrality route (A = 2^k, L = 2^m so that N | κE) is accepted as the preferred route; the σ-symmetric residue set is
    the fallback.
  - M2's m2_jellium EM analogue (a charged node made legal up to one uniform constant; non-compact prepared field on
    511/1536 links; dressed identity exact; exact rewind) is accepted as NUMERIC support for R-a's mechanism.
- **(e):** ACCEPT M2's point that a remainder texture conflicts with A1. **T14/S12 is now CONSTRUCTED by M1 with option (ii),
  uniform r_A, which keeps A1** (M1_work/M1_t29_S12_legal_Pplus.py + .json):
  - design: Wilson on (wr = 0.2498·PM), odd Q (PM = 1025·1023, PF = 1025), normalisation dd = hn = PF, so 6PF·div w = −6dd·ρ'
    needs no residues;
  - matter: the node P+ seed (b = P+(A e0), a = Γ b∘σ, Γ = W0G), 1818 integers, ghost charge max|ρ'| = 51,058 on 128 nodes,
    Σρ' = 0, σ-odd;
  - field: a mirror-symmetric integer flux w with div w = −ρ' EXACTLY, routed for every ghost pair (x, σx) through the centre
    node along a mirror-symmetric path (a node-centred inversion has no self-mapped link, so no parity obstruction). The split
    is b_A = w on representative links and a_A = −b_A∘mirror, with b_Φ = 0, a_Φ = div a_A; 255 field integers, COMPACT;
  - checks: C ≡ 0; Gauss ≡ 0 at EVERY node; uniform remainders (div r_A = 0); R*(s0) = s0 EXACTLY; single-time energy
    E₁ = +3.41e13 > 0; exact bounce 16/16; exact rewind; dressed-Gauss identity 0 failures; the field grows from the prepared
    48,282 to 106,297 (G = 0).
  - So an exactly legal, positive-energy, R*-fixed, compact seed EXISTS in the design: 2073 integers at A = 2^12. Its MINIMUM
    stays OPEN.
  - For a link-centred P+ seed the self-mapped central link forces an even flux there. If Σ_half ρ' is odd, use M2's option
    (i) or (iii), or route through a node-centred map: OPEN detail for T14.
- **(h), (i), F#1:** ACCEPT the one-Q wording (F#1 updated above), the package map names ("Mp", "rhoL0", "JM" vs the package's
  "JR", which flips the inert bit), and the additions T1 (L0 at (0,0,2Q)), T11 (randomise matter remainders only) and T13.
- **F#3, G:** ACCEPT M2's F#3 wording (equivalent to M1's). G line 5 is merged above: it keeps M2's "one declared uniform
  number, pure initial data, no force" and adds the honest clause on the two-integer seed's negative-energy content and the
  S12 size.
