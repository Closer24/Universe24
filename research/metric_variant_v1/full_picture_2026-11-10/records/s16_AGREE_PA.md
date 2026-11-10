# AGREE_PA — PAULI: PA-A (constructive) × PA-B (rigorous). Study 16
File opened by PA-A at Tue Nov 10 13:40:16 UTC 2026 (`date -u`; written 13:36–13:40:16 UTC).
Proposals:
- s16/PA-A_PROPOSAL.md (frozen 13:36:07);
- s16/PA-B_PROPOSAL.md (frozen 13:30:43; I read it at 13:36:13, sha256 71acd511…a1f800cc).

Each twin adds its own section and signs. Nothing in the other twin's section is edited.

## PA-A ROWS on PA-B_PROPOSAL.md — written by PA-A 13:36–13:40:16 UTC; signature at the end
- I froze PA-A_PROPOSAL.md (13:36:07) before opening any PA-B file. Then I read PA-B in full, plus the C5 code in PA-B_work/pab_checks.py (lines 204–250).
- New tiny exact checks for these rows: s16/PA-A_work/pa_agree_checks.py → pa_agree_checks.json (X1, X2; sha256 in SHA256.txt).
- Verdicts: AGREE / REFINE / DISAGREE. "A:x" points to my proposal.

| # | PA-B item | PA-A | reason |
|---|---|---|---|
| 1 | E1–E2: headroom (\|ℓ\| ≤ 1 ⇔ \|K\| ≤ D); the lock is unit counting, ℓ+ − ℓ− = m | **AGREE (THEOREM)** | Same as A:A1. A1 also gives the n-visit form: Σℓ_k = ⌊(r₀ + ΣK)/D⌋ |
| 2 | E3: two units through one lock give the Fréchet LOWER joint; in-phase units give ℓ+ = 2 | **AGREE + REFINE** | REFINE: the Fréchet-lower joint IS the QM law for two FERMIONS in \|1,1⟩ at a beam splitter, at every ratio, provided the two units do not interfere. Port + then carries T + R = 1 unit, so p = ½ and P(1, −1) = 1 = (T + R)². Checked in A:C1, 31/31 ratios. E3's comparison with the binomial law of \|2,0⟩ is the BOSON input. The lock fails vs QM for two other reasons: classical interference of same-state units (E3's in-phase case, P3) and species-blindness (P3) |
| 3 | E4: "REFUTED as an exclusion principle; a single-quantum detector property plus a sum rule" | **AGREE (substance) + REFINE (wording)** | Proposed joint wording: "the choice is the CLICK half of Pauli: ≤ 1 click per mode per readout ⇔ the mode carries ≤ 1 unit (A:A1). The STATE half, a bound on mode occupation, is absent on one board (S2)" |
| 4 | E5, E6 (clicks-as-particles is species-blind; a re-used lock gives sub-binomial noise) | **AGREE** | = GU4 rows 5–6; v6 §11 #11 |
| 5 | S1: S₂ acts trivially on board states | **AGREE (THEOREM)** | = 4B:P1, sharpened |
| 6 | S2: exclusion and exact superposition cannot share the same integer variables | **AGREE (THEOREM) + REFINE (scope)** | It bounds OCCUPATION-AS-AMPLITUDE. On a copy board (A:§5) the bounded object is the Gram of the orthonormal copies (Bessel), and superposition stays intact inside each copy. That is the very escape S2 names for QM ("superposition over occupation configurations"). S2 therefore does not obstruct A:§5 |
| 7 | S3: exchange ≠ 2π rotation on a classical field; a twisting process gives a path holonomy, not statistics | **AGREE + add A:B2** | Exact instance: the free Dirac hop's own spinor holonomy is (−1)^{ab} on an a×b rectangle (P_yᵀP_xᵀP_yP_x = −1 in all three planes; A:C3, 9/9). It depends on the path and the area: a holonomy, as S3 says |
| 8 | S4: a ±1 label on one deterministic history is unobservable or is a new dynamical bit | **AGREE (THEOREM)** | — |
| 9 | S5: spin–statistics not forced; with commuting values a spin-½ field has an indefinite Hamiltonian | **AGREE + REFINE (add the algebraic shadow)** | A:B3: on 2O, #{g² = 1} = 2 and #{g² = −1} = 18, so Σ dim·ν = +10 on V+ (dims 1,1,2,3,3) and −8 on V− (dims 2,2,4). Hence the Frobenius–Schur ν = z irrep by irrep (THEOREM + A:C4). Kᵀ = −K, so ψᵀKψ ≡ 0 for one integer field. Statistics is still DECLARED. But M2 is the unique assignment under which every species keeps a rotation-invariant on-site pair channel (DERIVED; naturalness, not a proof) |
| 10 | S6 (Grassmann not storable), S7 (univalence superselection, Kramers) | **AGREE** | — |
| 11 | §3 (a) parity / JW bookkeeping: EMPTY | **AGREE** | = S4 |
| 12 | §3 (b) Z2 link flux: AB holonomy, not statistics | **AGREE + add cost (A:§4)** | A classical string would be a definite record of where an integer, LOCALIZED parity went. Board quanta are spread waves, so the string has no well-defined path, and where it has one it is a which-path record that dephases the interference it is meant to sign |
| 13 | §3 (c) / M3: hard-core bit gears, u = 3Q(a + b) + locked pair hop; table: "Rule3 / reversible: yes, exact (C5)" | **DISAGREE (legality + reversibility)** | (i) u ∋ 3Q·a reads the gear's OWN a, which the acyclic a-read rule forbids (ONE-P2 §6.4; package AcyclicityError; the S7 row of A:§1). (ii) K = D·a makes ℓ − a = b + ⌊(K_rest + r)/D⌋ independent of a, so the map FORGETS a and is not injective on its state set. X1: one gear 72 states → 36 images (Q = 3) and 120 → 60 (Q = 5); locked pair 288 → 72 and 480 → 120. Example: (a, b, r) = (0, 0, 0) and (1, 0, 0) have the same image. PA-B's C5 checked bit invariance and number conservation, not injectivity. Under the acyclic rule, A:C6 (THEOREM: a bounded field is uncoupled) closes (c) on Rule3. Proposed status: "(c) CLOSED within Rule3; any hard-core law needs a NEW update rule, not a new tensor entry" |
| 14 | M1: antisymmetric configuration board with remainder pairing r(x2,x1) = D−1−r(x1,x2); Σ commutes with Rule3; the diagonal stays 0 | **AGREE (algebra, THEOREM)** | Re-derived: ⌊(D−1−r−K)/D⌋ = −⌊(K+r)/D⌋ and r′ ↦ D−1−r′. Parity classes are consistent (K even, D even). Note: a diagonal remainder can never be Σ-fixed (2r = D−1 has no solution for even D). PA-B handles this correctly through K(x,x) = 0 |
| 15 | §3 (d) table: "+0 rank (the same linear tensor, made swap-symmetric)", i.e. the configuration board CARRIES two quanta | **DISAGREE (dynamics) → REFINE** | Rule3 is second order in time. The product x_t⊗y_t of two free one-quantum solutions is NOT a solution of the sum-tensor leapfrog on the configuration board. X2 (exact Fractions, no rounding): (a) M = 0 clocks: the product has period 2 but the configuration gear has period 4, mismatch 6 at t = 2 and 4 at t = 3; (b) 1D ring L = 5, D = 30: mismatch 6 at t = 2, growing to ≈ 110 by t = 7. So the two-quantum frequency is cos W = cos w₁ + cos w₂, not W = w₁ + w₂: no additivity and no cluster decomposition for free quanta. The antisymmetry (row 14) is exact, but it is the antisymmetry of a different 6D wave theory. A correct (d) needs a mixed-time register (x_t⊗y_{t−1} components: 4 numbers per configuration point instead of a gear's 2). Rule3-native form: OPEN. The copies (A:§5) avoid this, since each copy is its own leapfrog |
| 16 | M2: board-native spin–statistics LAW, data = Fix(swap ∘ (z ⊗ 1)) | **AGREE (PROPOSAL / NEW LAW)** | Supported by row 9 (ν = z). On copies, the same law reads: "V− species ⇒ copies + wedge (Fermi) readers" (A:K6) |
| 17 | M4: JW / 3D bosonization relate QUANTUM models | **AGREE** | — |
| 18 | P1–P2: no shells, no degeneracy pressure, no stability bound on one board | **AGREE (one board)** + REFINE | With copies (NEW LAW), shells, Pauli blocking and degeneracy growth return in MEAN FIELD (A:§5 rows, DERIVED). The account is still signed (AGENTS 12), so "stability" stays dynamical |
| 19 | P3: HOM = 1 − \|cos φ\| (identical; mean 1 − 2/π for a uniform phase) and 1 (distinguishable, forced splitting), species-blind | **AGREE** | Same numbers as A:A3 (independently: 1 − 2√(TR) sin φ per port). On copies: identical FERMIONS → 1 at every ratio (A:§5); distinguishable still 1 with a copy-blind router (A:K5) |
| 20 | P4, P5 | **AGREE** | — |
| 21 | §5: D-PA1 "MISSING by THEOREM on one board; the choice's exclusivity is single-quantum unit counting" | **AGREE**, with row 3's wording | — |
| 22 | §5: D-PA2 "open (d) as a separate candidate variant" | **REFINE** | Offer TWO variants:<br>• (d-S) = A:§5 Slater copies: 3D-local, six neighbours, rank ≤ 4, storage 16·N·L³, correct free dynamics; exact Pauli (Bessel) to O(1/A); mean field.<br>• (d) = the full configuration board: correlations and exchange interference native, but 6D, 12 neighbours, storage ~(48L³)^N/N!, and it first needs the row-15 mixed-time fix.<br>PA-A ranks (d-S) first under the board's rules; (d) is the route if correlations beyond one Slater determinant are required |

### PA-A rows for PA-B to mark (not in PA-B's proposal)
| # | PA-A item | label | PA-B mark |
|---|---|---|---|
| Y1 | A:A2 — the three remainder couplings ARE the three two-port statistics: antitone (one circle) = fermions (T + R)² = 1, 31/31 ratios; independent = distinguishable T² + R², 31/31; comonotone (equal remainders in parallel) = \|T − R\|, equal to the boson (T − R)² only at T ∈ {0, ½, 1} | THEOREM + NUMERIC (A:C1) | |
| Y2 | A:A3 / C2 — beyond two ports one circle is order-dependent systematic sampling. In the Hadamard 4-port, 2-fermion case it selects {13}, {24} at ½ each: exactly the pairs Fermi statistics FORBIDS (fermion law: {12, 14, 23, 34} at ¼ each). The choice is not a determinantal sampler | NUMERIC (A:C2) | |
| Y3 | A:B3 / C4 — ν = z on every 2O irrep; ψᵀKψ ≡ 0 for one integer field | THEOREM + NUMERIC | |
| Y4 | A:C6 — bounded field ⇒ uncoupled under the acyclic Rule3: ℓ − B ⊂ B forces ℓ = min B + max B; X1 shows that the own-a escape (row 13) is irreversible | THEOREM + NUMERIC | |
| Y5 | A:§5 — ORBITAL COPIES (Slater board), NEW LAW, 3D-local:<br>• exact Pauli = Bessel on the conserved cross-copy Wronskians W(ψ_c, ψ_c′) = a_c·b_c′ − a_c′·b_c (odd under swap). Identity D·ΔW = b1·δ2 − b2·δ1 exact (A:C5, 0/30 failures); the remainder term is non-zero for generic hop ⇒ O(1/A);<br>• fermion HOM P(1,1) = 1 at every ratio;<br>• never two clicks in one mode;<br>• costs K1–K7 | THEOREM (Bessel, identity) + NUMERIC + NEW LAW | |
| Y6 | Relation of the two variants: at the linear level, the wedge of two copies IS an antisymmetric two-quantum amplitude, with the correct product dynamics (row 15). (d-S) is the Slater sub-manifold of a corrected (d) | DERIVED | |
| Y7 | X2 (row 15): configuration board with the sum tensor ≠ two free quanta under second-order Rule3 | NUMERIC (exact) + THEOREM (one line: the product of two leapfrog solutions satisfies a 4-term, not a 2-term, recurrence) | |

### Net state (PA-A view, before PA-B's marks)
- DISAGREE (2):
  - row 13: (c) M3 is not legal and not reversible;
  - row 15: (d) with the sum tensor does not carry two free quanta.
  Both are factual, with exact counterexamples in X1 and X2.
- Every other row is AGREE or REFINE.
- Joint recommendation, proposed:
  1. **D-PA1** (record): "Pauli, the exchange sign and spin–statistics: MISSING by THEOREM on one board (S1, S2, S4). The choice is the CLICK half (unit counting; fermion-exact at a two-port collision of non-interfering units, A2). The 2π sign is single-quantum (S3), with ν = z as its only algebraic link to exchange (B3)."
  2. **FAILS** (unchanged): shells, degeneracy pressure, fermion and boson HOM, ³He/⁴He (P1–P4).
  3. **D-PA2** (owner, NEW LAW, separate candidate variant only):
     - (d-S) orbital copies first (A:§5);
     - (d) the full configuration board second, after the mixed-time fix;
     - (c) closed within Rule3; (a) and (b) are not Pauli.
  4. **OPEN**: a determinantal reader (A:K4/K5); a Rule3-native mixed-time configuration register; the reachable-set escape of C6.

**PA-A SIGNATURE:** rows 1–22, Y1–Y7 and the net state, signed by PA-A at Tue Nov 10 13:40:16 UTC 2026 (`date -u`).

---------------------------------------------------------------------------------------------------------------------
## PA-B SECTION — marks on PA-A's rows 1–22 and Y1–Y7, PA-B corrections, rows for PA-A (I edit nothing above this line)
- I froze PA-B_PROPOSAL.md at 13:30:43 before opening any PA-A file.
- Read at 13:36:20–13:41: PA-A_PROPOSAL.md in full; PA-A_work/pa_checks.json (C1 all_ok = true; C2; C3 9/9; C4 counts
  2 / 18; C5 0/30; C6); pa_agree_checks.json (X1, X2).
- Post-freeze checks (my proposal is unchanged; these rows supersede it where they differ):
  - C6: PA-B_work/pab_c6_dirac_pairboard.{py,json}, sha256 e7ae82f3…63b07 / f3ce03b3…362f8, run 13:31:41;
  - C7: PA-B_work/pab_c7_selfaread.{py,json}, sha256 2ca76599…cacee3 / 7a3559d8…2dfd, run 13:37:53, AFTER reading
    PA-A's C6 and BEFORE reading PA-A's rows here.
- Marks: ACCEPT / ACCEPT + note / DISPUTE.

### (i) PA-B marks on PA-A's rows 1–22 (rows on my proposal)
| row | PA-A verdict | PA-B mark | reason |
|---|---|---|---|
| 1, 4, 5, 7, 8, 10, 11, 12, 14, 16, 17, 20 | AGREE (+ instances / costs) | **ACCEPT** | The A:B2 π-flux (−1)^{ab} is a good exact instance of S3. The which-path cost of a JW string (row 12) is added to option (b) |
| 2 | REFINE: for two NON-interfering units (\|1,1⟩) the Fréchet-lower joint gives P(1,1) = 1 = (T + R)² at every ratio; my \|2,0⟩ comparison is the boson input | **ACCEPT the arithmetic + note** | p = ½, so P(1,−1) = 1 for every ratio. Note: the board gives the same 1 for DISTINGUISHABLE units and for non-overlapping BOSONS, where QM gives T² + R² whatever the statistics. It is the same number at two ports, not the fermion law. Y2 (4 ports) shows that the one-circle reader picks the pairs Fermi statistics forbids |
| 3 | proposed wording "the choice is the CLICK half of Pauli" | **DISPUTE (wording only; substance ACCEPTED)** | ≤ 1 click per mode per readout ⇔ ≤ 1 unit in the mode is the quantization of DETECTION, which photon counting obeys too. Pauli is a bound on the STATE. Calling the counting "half of Pauli" credits the board with half a law it lacks. **Proposed joint wording:** "the choice supplies UNIT COUNTING at the detector (≤ 1 click per mode per readout ⇔ ≤ 1 unit in the mode; shared by every quantum, photons included). The STATE side of Pauli, a bound on occupation, is MISSING on one board (S2)" |
| 6 | REFINE (scope): S2 bounds occupation-as-amplitude; copies escape it (Gram + Bessel; superposition inside each copy) | **ACCEPT + note** | Correct: copies are the QM-type escape S2 names. Note (X1 below): Bessel needs a POSITIVE-definite Gram, which holds only within one rotation sense |
| 9 | add the algebraic shadow ν = z (FS on 2O); ψᵀKψ ≡ 0; M2 = the unique assignment that keeps a rotation-invariant on-site pair channel | **ACCEPT + REFINE (wording)** | Re-derived: #{g² = z} = 18 = 6 (±i, ±j, ±k) + 12 (±u ± v)/√2 with u ≠ v ∈ {i, j, k}; #{g² = 1} = 2; so Σ_{V±} dim·ν = 10, −8, and ν = +1 / −1 on every tensorial / spinorial irrep. Wording: this is the PSEUDOREALITY of half-integer spin (the j ⊗ j → 0 coupling has symmetry (−1)^{2j}). It holds for ANY statistics and fixes the spin-index symmetry of the singlet, not the particle exchange sign. ψᵀKψ ≡ 0 is a genuine classical-field prohibition: a Majorana mass needs anticommuting fields. I add it as S8 of my list. Naturalness of M2: ACCEPT as DERIVED (not a proof) |
| 13 | DISAGREE: my M3 / (c) reads the gear's own a (AcyclicityError) and is not injective | **ACCEPT — I WITHDRAW (c)'s "Rule3 / reversible: yes" and M3's construction** | Confirmed independently (C7): with K = D(a + b) + j EVERY image has two preimages (684/684 at Q = 3, 1860/1860 at Q = 5). The core says it too (core/tensor.py: "a self-read is a cycle"). My "free propagation C0-exact via K = D(a + b(x − e))" uses the same self-read and is withdrawn too; the legal exact transport is the d'Alembert fibre. Status, joint: "(c) CLOSED within Rule3 (A:C6 THEOREM on the full product set; reachable-subset escape OPEN); a hard-core law needs a NEW update rule". So not even CLASSICAL exclusion is available on the board |
| 15 | DISAGREE (dynamics): the sum-tensor configuration board is not two free quanta under second-order Rule3 (X2: product mismatch 6 → ~110) | **ACCEPT — I CONCEDE** | One line: x_t·y_t contains the two frequencies w1 ± w2 (a 4-term recurrence), while the lifted gear has one frequency, cos W = cos w1 + cos w2. No cluster decomposition. My own post-freeze note ("deviations add to first order around the π/2 carrier") does not rescue it, because the w1 − w2 component is missing. M1 (exact antisymmetry, exact zero diagonal, both sectors invariant) stays a THEOREM about the lifted law. New status of (d): "antisymmetric sector exact; correct two-quantum dynamics needs a mixed-time register (4 numbers per configuration point); Rule3-native form OPEN" |
| 18 | REFINE: with copies, shells / blocking / degeneracy growth return in mean field; stability stays dynamical | **ACCEPT + note** | The N^{5/3} growth is of the summed orbital frequencies. That it acts as a PRESSURE needs a stress law for the signed account (AGENTS 12): OPEN |
| 19 | AGREE; on copies identical fermions → 1; distinguishable 1 with a copy-blind router (K5) | **ACCEPT + note** | My P3 "distinguishable → 1" assumed a channel-blind router. Channel-resolved routers give the QM value T² + R², but then one quantum in a superposed internal state can give 0, 1 or 2 clicks (A:K5 (i)). The identical-quanta law 1 − \|cos φ\| on one board stands, so the FAILS stands |
| 21 | D-PA1 with row 3's wording | **ACCEPT D-PA1** with my row-3 wording | — |
| 22 | REFINE D-PA2: offer two variants, (d-S) orbital copies first, (d) after the mixed-time fix | **ACCEPT — I concede minimality to the copies** | For free / mean-field fermions the copies are the minimal construction: 3D-local, six neighbours, 16·N·L³, correct product dynamics. (d) is the route only for correlations beyond one Slater determinant, after the row-15 fix |

### (ii) PA-B marks on PA-A's rows Y1–Y7
| # | PA-A row | PA-B mark | reason |
|---|---|---|---|
| Y1 | the three remainder couplings ARE the three two-port statistics (antitone = fermions, independent = distinguishable, comonotone = \|T − R\|) | **AGREE (THEOREM + NUMERIC) + REFINE (name)** | Arithmetic checked (A:C1 all_ok; boson only at k = 0, 15, 30). On the board the antitone row occurs (a) when a persistent lock reads two SUCCESSIVE quanta (even Q, the sigma-delta lock), or (b) when a channel-blind router reads two overlapping orthogonal quanta. In both cases QM gives T² + R² for any statistics: (a) is the sub-binomial PRED [v6§11 #11], FAILS for independent sources. Name proposed: "antitone = the Fréchet-lower (one-circle) law; it equals the fermion two-port value", not "= fermions" |
| Y2 | beyond two ports one circle picks exactly the Fermi-forbidden pairs ({13}, {24} in the Hadamard 4-port) | **AGREE (NUMERIC; re-derived)** | Four reads of D/2: ports 1, 3 carry iff r ≥ D/2, else 2, 4. A strong result: the choice is anti-determinantal, not "half fermionic" |
| Y3 | ν = z on every 2O irrep; ψᵀKψ ≡ 0 | **AGREE (THEOREM)** + the row-9 wording | — |
| Y4 | bounded ⇒ uncoupled; the own-a escape is irreversible | **AGREE (THEOREM + NUMERIC)** | = my C7. Scope: the full product state set; a correlated reachable subset is OPEN |
| Y5 | ORBITAL COPIES (Slater board), NEW LAW | **AGREE as an explicitly separate candidate variant + REFINE (X1, X5)** | Exact Pauli in the state holds to O(1/A) WITHIN one rotation sense (X1). The copies' exchange sign is the frame orientation, invisible to copy-blind readers (S4 = A:K4). Fermion HOM P(1,1) = 1 at every ratio: ACCEPT. Distinguishable pairs need channel-resolved routers (K5) |
| Y6 | (d-S) = the Slater sub-manifold of a corrected (d) | **AGREE (DERIVED)** | — |
| Y7 | X2: the sum-tensor configuration board ≠ two free quanta | **AGREE (NUMERIC + THEOREM)** | = row 15 |

### (iii) PA-B rows for PA-A to mark
| # | PA-B item | label | PA-A mark |
|---|---|---|---|
| X1 | **The copies' Gram is indefinite on the full solution space.** For every real leapfrog mode, the two rotation senses b_t = v cos ωt ± Jv sin ωt give W(ψ, Jψ) = ∓D\|v\|² sin ω (C0 example: the u = 0 period-4 pair gives ±1). Bessel, i.e. n_φ ≤ 1, therefore holds only if every copy AND the probed mode lie in ONE sense (the positive-norm sector). The seed must select that sector, and the remainder mixes N_J at O(1/A) [v6§9]. A copy seeded in the other sense makes G = diag(A², −A²), and Bessel fails | THEOREM (algebra) | |
| X2 | **C6 (post-freeze): configuration board on the package's 8-channel sin-Dirac algebra** (P = L_i ⊗ s_z, W0 = 1_4 ⊗ s_x, re-derived, not imported), 1D ring L = 3, Q = 5, hop 3, mass 7, lifted U = M ⊗ 1 + 1 ⊗ M, pairing D − 1 − r. Result: 0 antisymmetry and 0 Pauli-diagonal violations in 60 updates × 2 seeds, rewind exact; control r̃ = r: 13192–13392 / 1006–1025 violations. Row-15 caveat: this is the antisymmetry of the LIFTED law, not of two free quanta | NUMERIC (C6) | |
| X3 | **Additional FAILS row.** Searches for Pauli-forbidden atomic transitions bound the violation probability for electrons to β²/2 ≲ 10⁻²⁶ (Ramberg–Snow 1990) and ≲ 10⁻²⁹ (VIP 2006), with later runs lower. Helium has no 1s² ³S state and shows the ortho/para exchange splitting. One board predicts maximal violation and no exchange energy | FAILS (lit.; orders of magnitude as cited) | |
| X4 | **Precision for S3.** The board's ψ → −ψ is the central X² of matter.py REVERSOR_MATTER: (a, b, r) → (−a, −b, R′(r)), with R′(r) = D − 2 − r (even r) or D − r (odd r) (core/reversors.py). It is exact for b-odd tensors on each r-parity class, so the 2π sign is an exact board operation on single packets | THEOREM (algebra) | |
| X5 | **Self-REFINE of my §0 line 7 and §3 (c):** "Fermi–Dirac counting" (lit.: lattice gases) is moot, since (c) is closed (row 13). My §3 answer is replaced by the joint status: (a) EMPTY; (b) AB holonomy (+ which-path cost); (c) CLOSED within Rule3; (d-S) copies FIRST (NEW LAW, separate candidate); (d) SECOND after the mixed-time fix | REFINE (own) | |

### (iv) Net state (PA-B view)
- **Substance: no DISAGREE left.**
  - I accept both of PA-A's factual DISAGREEs (row 13: (c) illegal and irreversible; row 15: the lifted (d) is not two
    free quanta) and withdraw the affected claims.
  - One WORDING dispute remains: "click half of Pauli" (row 3, and the name in Y1). My proposed joint wording is in
    row 3.
- **Joint recommendation (PA-B version; identical to PA-A's net state except the wording):**
  1. **D-PA1 (record):** "Pauli, the exchange sign and spin–statistics: MISSING by THEOREM on one board (S1, S2, S4).
     The choice supplies unit counting at the detector (photons too), fermion-valued only at a two-port collision of
     non-interfering units and anti-determinantal beyond (Y2). The 2π sign is an exact single-packet operation (S3, X4).
     Its only algebraic link to exchange is ν = z (pseudoreality, Y3). Even classical exclusion is closed under Rule3
     (row 13)."
  2. **FAILS:** shells, degeneracy pressure, fermion and boson HOM, ³He/⁴He, Pauli-violation searches (P1–P4, X3).
  3. **D-PA2 (owner, NEW LAW, separate candidate variant only):**
     - (d-S) orbital copies first (Y5 with X1);
     - (d) second, after a Rule3-native mixed-time register exists;
     - (a), (b), (c) are not Pauli.
  4. **OPEN:**
     - a determinantal reader (A:K4, K5);
     - the mixed-time configuration register (row 15);
     - the reachable-subset escape of A:C6;
     - a stress law that turns the copies' N^{5/3} into pressure (row 18).

**PA-B SIGNATURE:** sections (i)–(iv) (rows 1–22, Y1–Y7, X1–X5, net state) signed by PA-B at Tue Nov 10 13:43:07 UTC 2026 (`date -u`).

---------------------------------------------------------------------------------------------------------------------
## PA-A COMPLETION — marks on PA-B's X1–X5 and replies to PA-B's marks (written 13:43:33–13:44:43 UTC; I edit nothing above this line)
- I read the PA-B section (signed 13:43:07) in full.
- Read-only checks:
  - PA-B_work/pab_c6_dirac_pairboard.json: anti pairing 0/0 violations, seeds 1 and 2, rewind exact; same pairing 13392/1025 and 13192/1006;
  - pab_c7_selfaread.json: 684/684 and 1860/1860 two-preimage images.
  - sha256 prefixes match the ones PA-B cites.

### (i) PA-A marks on PA-B's rows X1–X5
| # | PA-B item | PA-A mark | reason |
|---|---|---|---|
| X1 | the copies' Gram W(ψ, Jψ) is INDEFINITE on the full solution space (the two rotation senses have opposite signs), so Bessel holds only if every copy AND the probed mode lie in ONE sense; the remainder mixes N_J at O(1/A) | **AGREE (THEOREM, re-derived) — it sharpens my §5** | For b_t = v cos ωt + s·Jv sin ωt: W(ψ, Jψ) = 2aᵀJb = −2s\|v\|² sin ω (in my normalization; PA-B's ∓D\|v\|² sin ω differs only by a positive factor). The sign is fixed by the sense s. My ADDENDUM 1 (13:41) restricts the click row to the same class: J-circular, one-sense (= the P+ seed class, v6 (c)). The joint row Y5 now reads "exact Pauli in the state to O(1/A) WITHIN the positive-norm sense; the seed selects it; a copy in the other sense gives G = diag(A², −A²) and breaks Bessel" |
| X2 | C6: lifted 8-channel sin-Dirac configuration board, anti pairing, 0 antisymmetry / 0 diagonal violations; control fails | **AGREE (NUMERIC, read-only check)** | With PA-B's own row-15 caveat: it is the antisymmetry of the LIFTED law, not of two free quanta |
| X3 | additional FAILS: Pauli-violation searches (Ramberg–Snow 1990; VIP); helium has no 1s² ³S and shows the ortho/para exchange splitting | **AGREE (FAILS) + REFINE (citation precision, from memory and not re-verified here)** | As I recall, Ramberg–Snow gave β²/2 ≲ 1.7·10⁻²⁶ and VIP 2006 ≲ 4.5·10⁻²⁸, with ~10⁻²⁹ only in later VIP runs. The orders of magnitude do not change the verdict. With copies (NEW LAW) the transitions into filled orbitals become blocked in mean field (Gram conserved to O(1/A)), so the variant predicts a violation of order the remainder drift, a PRED to quantify (OPEN) |
| X4 | the board's ψ → −ψ = the central X²: (a, b, r) → (−a, −b, R′(r)), R′ = D−2−r (even r) / D−r (odd r), exact for b-odd tensors on each parity class | **AGREE (THEOREM, re-derived)** | K + r = Dℓ + r′ with r′ ≡ r (mod 2); then −K + R′(r) = D(−ℓ) + R′(r′), and R′(r′) lies in [0, D) on both parity classes |
| X5 | PA-B self-REFINE: (a) EMPTY; (b) AB holonomy + which-path cost; (c) CLOSED within Rule3; (d-S) copies FIRST; (d) SECOND after the mixed-time fix | **AGREE** | Identical to my net state |

### (ii) PA-A replies to PA-B's marks
- **Row 3 (wording dispute) — I ACCEPT PA-B's wording and withdraw "the CLICK half of Pauli".** Photon counting obeys the same detection quantization, so the phrase over-credits the board. Joint wording: "the choice supplies UNIT COUNTING at the detector (≤ 1 click per mode per readout ⇔ ≤ 1 unit in the mode; shared by every quantum, photons included). The STATE side of Pauli, a bound on occupation, is MISSING on one board (S2)." My proposal §0.2, §0.6, §2 and §5 "Idea" should be read with this wording (to be applied in the merge; the frozen text stays).
- **Y1 name — ACCEPT.** "Antitone = the Fréchet-lower (one-circle) law; at two ports it equals the fermion value; it gives the same 1 for distinguishable units and for non-overlapping bosons (QM: T² + R²), and beyond two ports it is ANTI-determinantal (Y2)."
- **Rows 2, 6, 18, 19, Y5 notes — ACCEPT all.** In particular, row 18: the N^{5/3} growth is a growth of summed orbital frequencies; turning it into PRESSURE needs a stress law for the signed account (AGENTS 12): OPEN.

### (iii) Final joint state (both sections)
- **DISAGREE: none.**
  - PA-B conceded both factual rows: 13 ((c) illegal and irreversible) and 15 (the lifted (d) does not carry two free quanta).
  - PA-A conceded the wording rows: 3 and the Y1 name.
- **Joint recommendation (identical text for both twins):**
  1. **D-PA1 (record):**
     - Pauli, the exchange sign and spin–statistics are MISSING by THEOREM on one board (S1, S2, S4).
     - The choice supplies unit counting at the detector (photons too). It is fermion-valued only at a two-port collision of non-interfering units, and ANTI-determinantal beyond (Y2).
     - The 2π sign is an exact single-packet operation (S3, X4). Its only algebraic link to exchange is ν = z (pseudoreality, Y3); ψᵀKψ ≡ 0 (no classical Majorana mass).
     - Even classical exclusion is closed under Rule3 (C6 THEOREM; row 13).
  2. **FAILS:** shells and the periodic table; degeneracy pressure; fermion AND boson HOM; ³He/⁴He; the Pauli-violation searches (P1–P4, X3).
  3. **D-PA2 (owner, NEW LAW, explicitly separate candidate variant only):**
     - (d-S) ORBITAL COPIES first: 3D-local, six neighbours, rank ≤ 4, 16·N·L³, correct product dynamics. Exact Pauli in the state to O(1/A) within the positive-norm sense (X1). Fermion HOM 1 at every ratio. Mean field only; the sign is invisible to copy-blind readers.
     - (d) the full configuration board second, only after a Rule3-native mixed-time register exists (row 15).
     - (a), (b), (c) are not Pauli.
  4. **OPEN:**
     - a determinantal reader (K4, K5);
     - the mixed-time configuration register;
     - the reachable-subset escape of C6;
     - a stress law for the N^{5/3} growth;
     - the size of the copies' O(1/A) Pauli-violation PRED (X3).
- **Cross-pair note for the merge (EN):** EN-B's T1 NEW LAW (a joint amplitude on two-quantum configuration space) faces row 15 as well. Under second-order Rule3, a configuration gear with the sum tensor does not carry two free quanta (X2: product period 2 vs lifted period 4; L = 5 ring mismatch growing to ≈ 110). Any configuration board needs the mixed-time register.

**PA-A FINAL SIGNATURE:** AGREE_PA complete for PA-A (rows 1–22, Y1–Y7, X1–X5, replies, final joint state) at Tue Nov 10 13:44:43 UTC 2026 (`date -u`).
