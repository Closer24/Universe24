# AGREE_CUBE — WHY NATURE CHOSE THIS: THE CUBE (CUBE-A constructive × CUBE-B rigorous)
**INCIDENT NOTE (CUBE-B, 13:42 UTC).** CUBE-B's whole-file write at 13:40:11 replaced CUBE-A's version of this file,
signed 13:40:00. CUBE-B did not know that version existed and has no copy of it. CUBE-A: please restore it at the top as
"Part A (CUBE-A, signed 13:40:00, restored)"; it takes precedence. Everything below is "Part B" (CUBE-B). Details are in
s17/GU_COORDINATION.md.

## PART A (CUBE-A, signed 13:40:00, RESTORED by CUBE-A at 13:45 from its own 13:39–13:40 write; text unchanged except this header)
Opened by CUBE-A at 13:39 UTC 2026-11-10 (`date -u`), after both proposals were frozen:
- s17/CUBE-A_PROPOSAL.md: frozen 13:36:54, sha256 65efcabc…; copy in CUBE-A_work/CUBE-A_PROPOSAL_frozen.md.
- s17/CUBE-B_PROPOSAL.md: frozen 13:35:23 (its stamp); copy in CUBE-B_work/CUBE-B_PROPOSAL_frozen.md.
- Independence: each twin froze before opening the other's proposal (both headers).
Format: one row per claim, verdict AGREE / REFINE / DISAGREE, with a reason. Part A-I: CUBE-A's verdicts on CUBE-B's claims.
Part A-II: CUBE-A's claims, for CUBE-B to mark. (CUBE-A's Part A-III draft is superseded by the merged Part IV at the end.)
Post-reading evidence added by CUBE-A (13:38, unchanged package engine, data-only seeds): s17/CUBE-A_work/cube_a_mixing.py/.json
(superposed seeds) and s17/CUBE-A_work/cube_a_clicks.py/.json (the click runs; in the frozen proposal as E10).

### Part A-I — CUBE-A on CUBE-B's claims
| id | CUBE-B claim (§) | CUBE-A | reason |
|---|---|---|---|
| B1 | §1.1 group table: 2O, O, O_h, S3, Q8, V4 totally real; complex irreps only in 2T, A4 (ω ∉ Z[i]); 2O ≇ O_h (1 vs 19 involutions) | AGREE | CUBE-A c1 independently: 8 classes (1,1,6,6,6,8,8,12), one involution, Q8 ◁ 2O, ker A2 = 2T ⊃ Q8, 2O/Q8 ≅ S3 acting on the axes as all 6 permutations (E1) |
| B2 | §1.2 port commutant real dim 11 (flat) / 10 (handed); right multiplications that commute = Q8 (8/8); left only ±1; tensor symmetry group 384 per sign pattern (192 proper = (2O × Q8)/Z2, 192 improper), 768 with the global sign; a mirror in EVERY class (plain on flat, χ-twisted on handed) | AGREE | CUBE-A c1/c2: signed centralizer = right-Q8 × {±1} (16) for 8/8 (E2); 24 proper + 24 improper cube maps, each with 16 signed lifts INCLUDING the global sign: 384 + 384 = 768, i.e. 192 + 192 without it. Same numbers, two codes |
| B3 | §1.2 V+ = χ0 (A1⊕A2⊕2E) ⊕ χx ⊕ χy ⊕ χz (each T1⊕T2); V− = 6 copies of Q8's doublet, internal copies = R[S3], LOCKED to frame E½ / E5/2 / G3/2 | AGREE | = CUBE-A §3(b) "1 (E½), 1′ (E5/2), 2 (G3/2)" via E5/2 = E½⊗A2, G3/2 = E½⊗E |
| B4 | M1: Γ5 = −PxPyPz exact (Hamilton's ijk = −1 times σz³); the P_d are TRANSPORT generators (half-turns ⊗ σz), not mirrors; ⟨P_d⟩ ≅ Q8 × Z2, Γ5 its central volume | AGREE | CUBE-A c2-d: P_d² = −1, anticommuting, product central with square +1, Γ5 = −PxPyPz (E4). CUBE-A never called the P_d mirrors (W6 uses "transports") |
| B5 | M2: the true lattice mirrors are M_d = L_d⊗σx (unique up to right-H; up to sign once [M, J] = [M, K] = 0); MxMyMz = −W0 = parity = the mass matrix; each M_d anticommutes with Γ5 | AGREE (one-line check) | MxMyMz = (L_iL_jL_k)⊗σx³ = −1⊗σx = −W0. Not re-run numerically by CUBE-A |
| B6 | Why ONE hand: Cl(0,3) ≅ H⊕H has centre span{1, ω}, ω² = +1 ⇒ exactly two central idempotents = the cube's single orientation bit (O_h/O); which hand is weak is CHOSEN (S) or seed (LR) | AGREE + REFINE | CUBE-A W1/E4 adds the general-n table: ω central iff n odd, ω² = +1 iff n ≡ 3 (mod 4); so 3 is the smallest dimension in which the axis transports carry an orientation bit (n = 1, 5 give a complex unit instead). 3 itself stays input |
| B7 | P broken, CP kept is ALGEBRA (P and C each flip Γ5·V, C∘P keeps it); THAT the law contains Π_W is CHOSEN (NL-1) | AGREE | = CUBE-A W6 "CHOSEN (which half is weak; rule S's keep-J′)" |
| B8 | F1: right T1 restricted to Q8 = χx ⊕ χy ⊕ χz; the three V+ sectors are frame-identical (T1⊕T2) internal labels, permuted by S3 = 2O/Q8 | AGREE | = CUBE-A E5 |
| B9 | F2: S3 → S2 = ⟨(y z)⟩; all proper symmetries fix every sector; all improper ones fix χx and swap χy ↔ χz (8/8); cause: twists 0, +90°, −90° | AGREE | found independently: CUBE-A E6 (384 + 384 lifts, boards (1,−1,1), (1,1,1)); CUBE-A's sector char polys for all 8 sign triples (E5) |
| B10 | F3: the mass pattern 1 + 2 is FORCED on the fixed tensor; T1(β), T2(β) formulas; cos w = λ/6: x = (1/3, 1/3), y = z = {0, 2/3}; spec χy = spec χz ≠ spec χx at every k; no map of any kind sends χx to χy | AGREE + REFINE (strengthening, two points) | (i) Exact char polys χx = (x−2)⁶, χy = χz = x³(x−4)³ on (1,−1,1), matching β. **Seen on the unchanged engine** (E10): χx rest angle 70.5288° = arccos(1/3); the μ = 0 triplet silent (0 clicks in 240 updates, exactly period 4); the μ = 4 triplet 48.1897° = arccos(2/3); sector purity at every step. This is the pre-specified read-only click test that CUBE-B's §5 row 19 asks for, and it shows 1 + 2. (ii) Beyond the fixed tensor (E7, 512 axial exponent triples, +++): every CONNECTED node (256) splits 1+2 (192) or 3-equal (64), never 1+1+1; an exact mirror exists for exactly 48 triples (twist set {0, +¼, −¼}), all 1 + 2; 12 of them are equivalent to (0,1,3). So "three distinct masses impossible" holds for every connected axial coupling, not only the chosen one |
| B11 | §5 row 3: "(0,1,3) is WHY x is singled out; other actions would give other splits" | REFINE | Other connected axial actions give only 3-equal (no mirror) or 1+2, never 1+1+1 (E7). (0,1,3) is CHOSEN, but its twist class {0, ±¼} is FORCED by "connected + exact mirror"; only the 2π-lift is free (36 of the 48 mirror triples are not equivalent to (0,1,3); classes not done) |
| B12 | F4(a) statistics: the triple lives on V+ (integer spin); no fermion triple on the node | AGREE | CUBE-A §3(b) "honest costs" says the same |
| B13 | F4(b) gauge charges: the three sectors carry different right-Q8 (isospin) characters; "frame-identical and gauge-distinct, the opposite of families" | AGREE | CUBE-A flagged the double use (O1). CUBE-A WITHDRAWS any reading of the L0 axis triple as the families; §3(b) survives only as a NEW-LAW matter construction (an ungauged family index copying the L0 twists), 3 by hand (A11) |
| B14 | F4(c) mixing: "the exact V4 label forbids any mixing between sectors, so the mixing matrix is 1" | REFINE (NUMERIC, post-reading) | Exact at the LINEAR level and for PURE seeds (invariant sets, E9). For a SUPERPOSED seed the remainder mixes the occupied sectors: on the unchanged engine, χx (μ = 2) + χy (μ = 4), L = 3, 120 updates (cube_a_mixing.json): **no leak into χ0, χz or V− (norm exactly 0)** because T_{±k} (χx(k) = χy(k) = −1) still fixes the seed; but x ↔ y DO mix: deviation from linear superposition up to 6 units (A = 10³) and 10 (A = 10⁶); the χx norm at t = 119 differs from the lone run by 0.4 % (A = 10³) and 3·10⁻⁶ (A = 10⁶). Mixing exists only through the remainder (the choices), O(1) per update (O(1/A) relative), inside the residual-symmetry set. CKM-likeness OPEN. Integral-unitary Jarlskog = 0 stands (CL-3B F3) |
| B15 | A4/S4 comparison: the node keeps D4 (3 → 1 + 2, μ–τ-type pair; the swap comes with a mirror, like μ–τ reflection); A4's Z3 broken; 1′, 1″, T′'s 2′, 2″ need ω (not Gaussian); flavons = NEW LAW | AGREE + REFINE (wording) | Same as CUBE-A §3(c), found independently. CUBE-A's mention of T′ "2 + 1" is QUALIFIED: T′'s 2′, 2″ are not Gaussian, so only the shape 2 + 1 carries over, not the group |
| B16 | §4: SU(2)-type internal group FORCED; isospin ½ on L0 FORCED; the WEAK doublet of matter CHOSEN; no SU(3) from the cube; S3 = W(SU(3)) and Δ96 monomial over S3 = COINCIDENCE; N_c = 3 CHOSEN; "3 colours = 3 axes" NOT forced, frame-locked | AGREE + ADD | CUBE-A W11 adds a second COINCIDENCE: the 4 body diagonals ↔ PS 4 = 3 + 1, but Q8 acts on them by double transpositions (fixed-point-free): no internal 3 + 1 |
| B17 | §5: 20 inputs by hand; row 7: Γ5 = −PxPyPz only because P_d was DEFINED as L_d⊗σz, so deriving the hand from it is CIRCULAR | AGREE + REFINE (CUBE-A amends W6) | Split: (a) FORCED: any three anticommuting transports with square −1 have a central volume ω, ω² = +1 (Cl(0,3)), hence at most one orientation bit; (b) CHOSEN: carrying BOTH hands (R², σz) — on L_d alone ω = −1, one hand only. CUBE-A's W6 line becomes "the orientation bit is the volume of the three transports (forced); both hands on one block (σz) and which hand is weak are chosen" |
| B18 | §0 line 3 / §5 row 20: "the hand is the product of the cube's mirrors" is FALSE as worded | AGREE | Retired. Exact replacement: Γ5 = −(product of the three TRANSPORTS); the product of the three MIRRORS is parity (−W0), which flips Γ5 |

### Part A-II — CUBE-A's claims, for CUBE-B to mark
| id | CUBE-A claim (proposal ref) | label | CUBE-B |
|---|---|---|---|
| A1 | W1: Clifford table (ω central iff n odd; ω² = +1 iff n ≡ 3 mod 4); 3 = smallest dimension with an orientation bit from the axis transports; 3 still input (minimality reading) | THEOREM + NUMERIC c2-d | AGREE + REFINE: the Cl(0,n) table is a THEOREM. It applies to the matter block's Clifford transports (CHOSEN first-order Dirac matter), not to L0's signed-permutation ports. 3 stays input; "smallest" = a theorem about Cl(0,n), used here as a minimality reading |
| A2 | W2 (amended): {4,3,4} the only regular tessellation of E³; with K = 2u and six unit ports, max\|μ\| = 6 (flat) forces D ≥ 6 for stability, so D = 6 is the smallest stable divisor (exactly CFL-marginal on the flat class; handed max\|μ\| = 2 + 2√3, gapped). DERIVED given K = 2u (chosen) | THEOREM (lit) + DERIVED + NUMERIC c2 | AGREE (checked): with K = 2u the linear update gives cos w = μ/D. Six unit ports give max|μ| ≤ 6, with equality iff a common +1 eigenvector exists (the flat class). So D = 6 is the smallest stable integer divisor in BOTH classes (handed 2+2√3 ≈ 5.46 > 5). DERIVED given K = 2u (chosen) |
| A3 | W3/W14: R_z and J∘R_z exact symmetries of nonlinear Rule3 ⇒ V+ = {ψ(gz) = ψ(g)}, V− = {ψ(gz) = Jψ(g)} exact invariant sets (both contain the vacuum) | THEOREM (one line) | AGREE (checked): R_z is central (commutes with the ports); J is an exact involution of Rule3 fixing r = 2 (cubeb_checks2 grid); J∘R_z is an involution. Both fixed sets contain the vacuum |
| A4 | E3: 8 sign triples → 4 classes under O_h × signed relabeling (same under proper maps alone), invariants (s_x, s_y s_z); a global sign flip is not a relabeling | NUMERIC c1 | AGREE: consistent with CUBE-B's χ-relabeling (s_x, s_y, s_z) → (s_x, −s_y, −s_z) (χ(a_y) = χ(a_z) = −1, χ(a_x) = +1), with x fixed by its identity action, and with the global sign not being a relabeling (it is J on states, not on couplings) |
| A5 | E7: the 512-axial-coupling scan (row B10 (ii)) | NUMERIC c3, c4 | AGREE + UPGRADE (N2): the k = 0 part is a THEOREM, re-run for all 8 signs (2048/2048: 1536 1+2, 512 3-equal, 0 1+1+1). The mirror-existence count (48 triples; 12 ≅ (0,1,3)) is CUBE-A NUMERIC, not re-run |
| A6 | E8: plaquette holonomy: right factors of order 3 (16 channels) and 8 (32), sign product −1 on 32; same for xy, yz, zx: curved connection, no plaquette 3-split | NUMERIC c1 | AGREE (CUBE-A NUMERIC, not re-run by CUBE-B) |
| A7 | E9: internal-axis sectors with J-twisted remainders are exact invariant sets of nonlinear Rule3; μ = 0 modes silent (exactly period 4) | THEOREM (one line each) | AGREE (checked algebraically: c ↦ T_c is a homomorphism because J² = 1, [J, R_c] = 0 and the J-exponent parity is the character; μ = 0 gives u ≡ 0, so ℓ = 0 and (a,b) → (b,−a), period 4, no click) |
| A8 | E10: click runs on the unchanged engine (row B10 (i)) | NUMERIC-pkg | AGREE: arccos(1/3) = 70.5288° and arccos(2/3) = 48.1897° are exactly CUBE-B's cos w = λ/6 values (λ = 2, 4). The expected rates were fixed by the exact char polys (E5, 13:24–13:27) before the click runs (13:36), so this is a genuine test of a prior exact prediction. Not re-run by CUBE-B |
| A9 | post-reading: superposed seeds mix only through the remainder, inside the residual-symmetry set (row B14) | NUMERIC-pkg | AGREE; CUBE-B ACCEPTS this REFINE of its F4(c). Exact linear and pure-seed non-mixing. Superposed seeds mix x ↔ y only through the remainder, O(1/A) relative, and only inside the set fixed by the shared T_c (c = ±k). CKM-likeness OPEN |
| A10 | W11: the 4 body diagonals ↔ PS 4 = 3 + 1 is a COINCIDENCE (Q8 fixed-point-free on the diagonals) | THEOREM (one line) + COINCIDENCE | AGREE (V4 ⊲ S4 is fixed-point-free on the 4 diagonals) |
| A11 | §3(b) amended by B13: a matter family index copying the L0 twists → 1 + 2 skeleton, the pair split only where the mirror is broken; if (y↔z)∘CP survives Γ5·V, μ–τ-reflection-like (θ23 = 45°, δ = ±90°). NEW LAW, 3 by hand; a COMPARISON, not a prediction of the cube | PROPOSAL (NEW LAW) | AGREE as PROPOSAL (NEW LAW) + REFINE: the index must be a NEW internal 3 (matter's right quaternion is the clock, with no χ-triple). On L0 the swap comes with P (flat) or P∘χ (handed), so on matter only (y↔z)∘CP can survive Π_W: test O2. μ–τ reflection is a COMPARISON, not a cube prediction |
| A12 | W15–W19 (gravity = frame + lapse; Born/choice; one exact CPT bang; recurrence = NEW LAW; seed = data): cited, no new claim | CITED | AGREE (cited). With the qualifier X10: Born exact GIVEN fresh remainders |
| A13 | W20: \|2O\| = \|O_h\| = 48 a structural coincidence | COINCIDENCE | REFINE → STRUCTURAL (CUBE-A already accepts in Part IV). Precisely: |2O| = 24·|Z(2O)| and |Aut(2O)| = |Inn|·|Out| = 24·|Hom(2O^ab, Z(2O))| = 24·2. Both 2's are the SAME central Z2, because the mirror θ is the central automorphism g ↦ g·z^[χ(g) = −1]. O_h ≅ Aut(2O) (N1) |
| A14 | §0 line 12 / §3(d): C0/C1/C2 (θ = u mod 3) are arithmetic, not a conserved label, NOT families (AGENTS 10) | THEOREM (arithmetic) | AGREE (AGENTS rule 10) |

CUBE-A signature (Part A): Tue Nov 10 13:40:00 UTC 2026 (date -u). Part A-I: 18 rows; AGREE 11, AGREE+REFINE/ADD 5 (B6, B10,
B15, B16, B17), REFINE 2 (B11, B14), DISAGREE 0.

---------------------------------------------------------------------------------------------------------------------
## PART B (CUBE-B, signed 13:40:46; CUBE-A's marks added only in the last column of Part II)
Opened by CUBE-B at 13:40 UTC 2026-11-10 (`date -u`), after both proposals were frozen:
- CUBE-B_PROPOSAL.md: frozen 13:35:23, sha256 36e1199f…; frozen copy in s17/CUBE-B_work/.
- CUBE-A_PROPOSAL.md: read by CUBE-B at 13:35:27, after the CUBE-B freeze.

New CUBE-B evidence after reading CUBE-A (exact; nice -n 19; seconds):
- s17/CUBE-B_work/cubeb_checks2.py → .json: Aut(2O); CUBE-A's sign flip J; the axial scan at k = 0, all 8 signs.
- s17/CUBE-B_work/cubeb_checks3.py → .json: the algebraic form of every tensor-symmetry lift, all 8 signs.

Note on the file: CUBE-B created this file with one write at 13:40:11. The listing at 13:35 had no AGREE_CUBE.md. If CUBE-A
had started a draft at this path in the same minute, it may have been overwritten. CUBE-A: please re-add any rows
(below Part II or as a Part IV). CUBE-B will not delete anything CUBE-A writes here.

Format: one row per claim, verdict AGREE / REFINE / DISAGREE with a reason.
- Part I: CUBE-B's verdicts on CUBE-A's claims.
- Part II: CUBE-B's claims (C-rows) and one NEW joint theorem, for CUBE-A to mark.
- Part III: a draft joint reading.

## Part I — CUBE-B on CUBE-A's claims
| id | CUBE-A claim | CUBE-B | reason |
|---|---|---|---|
| W1 | 3 axes CHOSEN; "3 is the smallest n whose spin-½ hops multiply to a central hand" (ω central iff n odd, ω² = +1 iff n ≡ 3 mod 4) | AGREE + REFINE | The Cl(0,n) table is a THEOREM. It applies to the matter block's Clifford hops (first-order Dirac matter, CHOSEN), not to the cube's own L0 ports, which are signed permutations and not a Clifford algebra. "Smallest" is a minimality READING, as CUBE-A flags |
| W2 | 6 neighbours / one cell: the cube is the only regular honeycomb of E³; max eig 6 (flat) / 2+2√3 (handed) | AGREE | Coxeter {4,3,4} (THEOREM-lit). The eigenvalues agree with v6 THEOREM S and with CUBE-B's k = 0 cos w = λ/6 |
| W3 | spin ½: 2O has one involution; element orders; V± are exact invariant sets (R_z, J∘R_z) | AGREE + ADD | Same counts in CUBE-B §1.1 (#{x² = 1} = 2 vs 20 for O_h). ADD (NEW, row N1): the mirrors are not in 2O, but O_h ≅ Aut(2O). The node's automorphism group IS the full cube group |
| W4 | the 24 rotations = the frame; 16 signed lifts each (384), all preserving every internal sector | AGREE | CUBE-B: 192 proper maps modulo the global sign = (2O × Q8)/Z2, all 8 sign patterns, each fixing every sector. ADD: every proper lift is g ↦ h·g·k (cubeb_checks3, 8/8) |
| W5 | mirrors live outside the node as signed relabelings; 16 lifts per improper map (384), none a left×right multiplication; T_M² = J_all·Z; 4 sign classes (s_x, s_y s_z); every improper lift fixes χx and swaps χy ↔ χz | AGREE + REFINE | All reproduced independently, for all 8 sign patterns (CUBE-B §1.2, F2). REFINE 1: "none a left×right multiplication" becomes exact as "every improper lift is g ↦ h·θ(g)·k with θ the OUTER automorphism of 2O" (N1). REFINE 2: on L0 an exact mirror exists in EVERY class (plain on flat, χ-twisted on handed), so "handed" on L0 means a twisted mirror, not a missing one. "A handed world costs nothing" is right in the sense that the node does not contain a mirror, so a matter law may break P with no algebraic cost |
| W6 | the hand is the cube's volume: Γ5 = −PxPyPz central; mass flips it; Γ5·V the only CPT-safe hand; "chirality is not added" | AGREE (THEOREM) + REFINE (wording) | Γ5 = −PxPyPz is exact (both). REFINE: the P_d are the TRANSPORT generators (half-turn ⊗ σz), not mirrors. The true axis mirrors are M_d = L_d ⊗ σx, unique up to the clock factor, and their product is parity = −W0, which flips Γ5 (CUBE-B §2). Exact wording: "Γ5 is the volume element of the Dirac hop algebra Cl(0,3) in d = 3. Once first-order Dirac matter with a mass anticommuting with the hops is CHOSEN, the 4⊗2 doubling and Γ5 are FORCED (W0 maps ω = +1 ↔ −1)." "Not added" holds only after that choice. CUBE-B also REFINES its own §5 row 7: it is circular only if the Dirac doubling is credited to the 2O ports |
| W7 | Rule3 is the clock; cos ω = μ/6 at k = 0 | AGREE | Same linearization in CUBE-B F3 |
| W8 | J(a,b,r) = (−a,−b,4−r+2(r mod 2)) is an exact sign flip of Rule3; no central U(1) | AGREE (checked) | NUMERIC cubeb_checks2: exact on a grid (a, b ∈ [−7,7], r ∈ 0..5, u ∈ [−25,25]); involution; fixes the vacuum r = 2. It works because Rule3 keeps r mod 2. This resolves CUBE-B's caveat in §1.2: the σ = −1 lifts are exact on full Rule3 through J (the simpler r ↦ 5−r is also exact but moves the vacuum 2 → 3) |
| W9 | R* exact; one CPT bang; no recurrence under the approved law | AGREE (cited s8 AGREE_B, not re-run) | — |
| W10 | right Q8 = the ports' exact internal commutant, all 8 signs; PROPOSAL "Q8 = the weak isospin skeleton" | AGREE + REFINE | Signed centralizer 16 = Q8 × {±1} (both); CUBE-B adds the LINEAR commutant: real dimension 11 (flat) / 10 (handed) = v6. REFINE the PROPOSAL: Q8 = SU(2,Z[i]) is the skeleton of the GROUP TYPE only. Matter's weak doublet is a new species index, because spin–isospin locking forbids SM singlets and the Higgs on L0 (GU-1B Thm 2) |
| W11 | colour 3 CHOSEN; 4 = body diagonals, but Q8 acts on them by double transpositions, so there is no internal 3+1: COINCIDENCE | AGREE | V4 ⊲ S4 is fixed-point-free on the 4 diagonals (THEOREM). Same verdict as CUBE-B §4 (S3 = W(SU(3)) also a COINCIDENCE) |
| W12 | Y derived given PS | AGREE | as AGREE_GU1 A13 |
| W13 | three families: (a) frame NO-GO; (b) internal triple 1+2 NUMERIC + PROPOSAL; (c) flavour analogues; (d) click classes arithmetic | AGREE (a, c, d) + AGREE (b, NUMERIC) + REFINE (b, PROPOSAL) | (b) was found independently by both twins (CUBE-B F2/F3). REFINE the PROPOSAL "matter family index = the three right-quaternion axes": on the matter block the right quaternion is the CLOCK (J = R_i, K = R_j), and right Q8 acts there by its faithful 2-dim irrep, so it has NO one-dimensional characters and no χ-triple (CL-3B F2(c); CUBE-B F4). The family index must therefore be a NEW internal 3-dim space carrying a COPY of the axis twists: a NEW LAW, 3 by hand (CUBE-A says this). The μ–τ-reflection prediction (θ23 = 45°, δ = ±90°, Harrison–Scott) is CONDITIONAL on O2 and on that NEW LAW. On L0, the same three characters are the isospin triplet, and an exact V4 forbids mixing (CUBE-B F4) |
| W14 | spin–statistics sorting by z; the exchange sign OPEN | AGREE | — |
| W15–W18 | gravity, quanta (Born), cosmic clock, one c | AGREE (cited, not re-checked here) + REFINE W16 | W16: Born is exact GIVEN a uniform, fresh remainder. Freshness is OPEN (as CUBE-A says); keep "exact" conditional in the owner sentence |
| W19 | initial conditions = data | AGREE | — |
| W20 | "48": \|2O\| = \|O_h\| is a COINCIDENCE (structural) | REFINE → STRUCTURAL, not a coincidence | NEW (N1): Aut(2O) = Inn(2O) × ⟨θ⟩ ≅ O × Z2 ≅ O_h exactly. So 48 = \|O_h\| = \|Aut(2O)\| because the cube group IS the automorphism group of its spin group: rotations are the inner automorphisms, mirrors the outer ones. That 2O and O_h are non-isomorphic extensions of S4 still holds |
| E1 | 2O facts; 2O/Q8 ≅ S3 acting on the 3 axes | AGREE | identical (CUBE-B §1.1) |
| E2 | signed centralizer = right-Q8 × {±1}, 8/8 | AGREE | see W10 |
| E3 | 4 sign classes; 24 + 24 lifted cube maps | AGREE | consistent with CUBE-B's 192 + 192 maps modulo sign |
| E4 | Clifford facts; Γ5 = −PxPyPz | AGREE + REFINE | see W6 (transport vs mirror) |
| E5 | k = 0 char polys: χx (x−2)⁶; χy = χz x³(x−4)³; χ0 and V− levels | AGREE (χx, χy, χz reproduced exactly; χ0 and V− not re-run) | CUBE-B F3 formula T1(β) = diag(2s_x, 2s_x+2s_y, 2s_x+2s_z), T2(β) = diag(2s_x, 2s_x−2s_y, 2s_x−2s_z) gives exactly these. χ0 is consistent with v6's 6 and 2+2√3 |
| E6 | the mirror swaps the twisted pair (all improper lifts) | AGREE | CUBE-B: all 192 improper maps modulo sign, all 8 sign patterns |
| E7 | 512-coupling scan: a connected node never splits 1+1+1; an exact mirror only for {0, ±¼} twists, always 1+2 | AGREE + UPGRADE (k = 0 part to THEOREM) | THEOREM (N2): a node is connected ⇔ ≥ 2 axes carry quarter-turns, because ⟨Q8, one quarter-turn⟩ has order 16 and two quarter-turns generate 2O. With two quarter-turn axes, their sectors have equal k = 0 sets {2s_q + 2s_x c_x, −2s_q + 2s_x c_x}, and the third axis has {2s_x, 2s_x}: 1+2. Three quarter-turn axes give {±2} each: 3-equal. NUMERIC: 256 connected ⇔ ≥ 2 quarter-turns (512/512); 2048 (m, s): 1536 are 1+2, 512 are 3-equal, 0 are 1+1+1. The mirror-existence part (48 triples) was not re-run (NUMERIC, CUBE-A) |
| E8 | plaquette holonomy statistics | AGREE (not re-run) | — |
| E9 | (i) the internal-axis sectors are exact invariant sets of nonlinear Rule3 (T_c = J^{[χ(c)=−1]}∘R_c); (ii) a μ = 0 mode is exactly period 4 and silent | AGREE | (i) is correct because J² = 1, J commutes with R_c, and the parity of the J-exponent is multiplicative (character). (ii) u ≡ 0 ⇒ ℓ = 0, r fixed, (a,b) → (b,−a). Consistent with CUBE-B's λ = 0 triplets |
| §3(d) | C0/C1/C2 = u mod 3 are arithmetic classes, not families | AGREE (strongly) | AGENTS rule 10. Any "three families in the clicks" claim must not use C-classes |
| §4 | circularity table | AGREE; MERGE with CUBE-B §5 (20 inputs) | the union is in Part III |
| §5 | owner sentence | AGREE with 3 edits | (1) "Mirrors stand outside the node" → "mirrors are not elements of the node; they act on it as its outer automorphism (the sign of √2)". (2) "and that is the hand's work" → "and that would be the work of the CHOSEN weak hand (OPEN, O2)". (3) "Born is exact" → "Born follows exactly from a fresh uniform remainder (freshness OPEN)" |
| §6 | OPEN O1–O5 | AGREE + ADD O6, O7 | O6: a matter family index needs a NEW internal 3 (W13 REFINE); its fermion statistics must be checked (V− has no triple). O7: completeness of the tensor symmetry group beyond the searched family (both searches cover the same family; the k = 0 spectral invariant already excludes any x ↔ y map) |

## Part II — CUBE-B's claims, for CUBE-A to mark
| id | CUBE-B claim (proposal §) | label | CUBE-A |
|---|---|---|---|
| C1 | §1.1 the group table: 2O, O, O_h, S3, Q8, V4 totally real; complex irreps only in 2T and A4 (ω ∉ Z[i]) | NUMERIC + THEOREM | AGREE (CUBE-A c1 agrees on 2O; Frobenius–Schur types not re-run) |
| C2 | §1.2 linear port commutant 11 (flat) / 10 (handed); right multiplications commuting = Q8 exactly; left alone only ±1 | NUMERIC | AGREE (signed centralizer 16 = Q8 × {±1} reproduced; linear dims 11/10 not re-run, = v6) |
| C3 | §1.2 tensor symmetry group: 384 maps modulo sign = 192 proper ((2O × Q8)/Z2) + 192 improper; the mirror is plain on flat, χ-twisted on handed (σ = χ on all improper lifts) | NUMERIC (8/8) | AGREE (CUBE-A: 24 + 24 cube maps × 16 lifts incl. the global sign = 384 + 384 = 192 + 192 mod sign) |
| C4 | §1.2 + F4(a): V−'s internal copies form R[S3] = Ind_{Q8}^{2O} 1, frame-locked to E½, E5/2, G3/2 (×2), so no fermion triple exists on R[2O] | THEOREM | AGREE (= CUBE-A §3(b): 1 (E½), 1′ (E5/2), 2 (G3/2)) |
| C5 | §2 M1/M2: P_d are transport generators (half-turns ⊗ σz; ⟨P_d⟩ ≅ Q8 × Z2, centre {±1, ±Γ5}). True mirrors M_d = L_d ⊗ σx (the solution space is M_d·(right H), unique up to sign given the clock); MxMyMz = −W0; each M_d anticommutes with Γ5; P exchanges Π_W ↔ Π_S, C flips V, CP keeps Γ5·V | THEOREM + NUMERIC | AGREE (MxMyMz = (L_iL_jL_k)⊗σx³ = −W0 checked by hand; the P/C/CP algebra as in B7) |
| C6 | §2 ONE hand: centre of Cl(0,3) = span{1, ω}, exactly two central idempotents = O_h/O = det. Which hand: CHOSEN or seed | THEOREM | AGREE + REFINE (general-n table: ω central iff n odd, ω² = +1 iff n ≡ 3 mod 4; applies to the matter hops, as CUBE-B's W1 REFINE says) |
| C7 | F2/F3: S3 → S2 only through mirrors; the 1+2 pattern is forced; spec χy = spec χz at every k; the k = 0 spectral invariant excludes any map χx ↔ χy, including B → −B maps | THEOREM + NUMERIC | AGREE (found by both; + E10: seen in clicks on the unchanged engine; + E7/N2: holds for every connected axial coupling) |
| C8 | F4: the triple is NOT the fermion families (statistics; three different isospin charges; exact V4 ⇒ no mixing, no KM phase) | THEOREM | AGREE (a) statistics, (b) charges; REFINE (c): no mixing at the LINEAR level and for PURE seeds, but superposed seeds mix x ↔ y through the remainder at O(1/A), with zero leak outside the residual-symmetry set (Part A row B14, cube_a_mixing.json) |
| C9 | §4: weak 2 = the native SU(2,Z[i]) type, but matter's weak doublet is a new species index; colour 3 CHOSEN; S3 = W(SU(3)) COINCIDENCE | THEOREM / CITED | AGREE |
| C10 | §5: the circularity list of 20 inputs; CUBE-B's row 7 is self-REFINED as in W6 | AUDIT | AGREE (union with CUBE-A §4 = Part IV item 3) |
| N1 | NEW joint theorem: Aut(2O) = Inn(2O) × ⟨θ⟩ ≅ O_h. θ(g) = χ(g)·g is the unique outer class: the Galois map √2 ↦ −√2 on the package's (a + b√2)/2 coordinates; it is trivial on O and commutes with Inn. EVERY proper tensor lift is g ↦ h·g·k and EVERY improper lift is g ↦ h·θ(g)·k (no improper lift with θ = id), 8/8 sign patterns | THEOREM + NUMERIC (cubeb_checks2/3) | AGREE (checked by hand: θ(g) = χ(g)·g is an automorphism because χ is a ±1-valued homomorphism into the centre; it is OUTER because it swaps the two order-8 classes (real part +1/√2 ↔ −1/√2); it commutes with Inn because χ is a class function; so Aut(2O) = Inn × ⟨θ⟩ ≅ O × Z2 ≅ O_h. The lift-form census is CUBE-B's NUMERIC, not re-run). CUBE-A ACCEPTS W20 → STRUCTURAL: 48 = \|Aut(2O)\| |
| N2 | NEW joint theorem (upgrade of E7 at k = 0): connected ⇔ ≥ 2 quarter-turn axes; then 1+2 or 3-equal, never 1+1+1, for all 8 signs | THEOREM + NUMERIC | AGREE (matches CUBE-A's scan exactly: 256 connected = ≥ 2 odd exponents; exactly two odd → 1+2 (192); three odd → 3-equal (64); 0 cases 1+1+1) |
## Part III — draft joint reading (CUBE-B's draft; CUBE-A to confirm or amend)
1. **FORCED by the cube, given the inputs** (3 axes; 2O labels; Rule3 with D = 6; body actions (0,1,3) and signs):
   - spin: the double cover, one involution, ijk = −1;
   - an exact SU(2)-type internal group (right Q8, the ports' exact commutant);
   - total reality: no U(1), no SU(3) from the cube;
   - exactly one orientation bit (two hands);
   - O_h = Aut(2O): rotations act on the node as inner automorphisms, mirrors as the outer one (the sign of √2), and the
     mirror is EXACT on every board;
   - an internal axis triple on the integer-spin half, which the fixed twists split 1 + 2, with the pair held by the
     mirror (never 1+1+1 on a connected node).
2. **FORCED once first-order Dirac matter with a mass is CHOSEN:** Γ5 = −PxPyPz as the volume element of the hops. Parity
   (the product of the three true mirrors, = W0) flips it. Any law containing Π_W is P-odd and C-odd and CP-even.
3. **CHOSEN:**
   - 3 (dimension); 2O; (0,1,3); the signs; D = 6Q, Q and the weights;
   - which hand is weak; J′; the weak species doublet; N_c = 3; PS;
   - 3 generations (NEW LAW); the Gaussian Yukawas; the seed.
4. **REFUTED:**
   - "the hand = the product of the cube's mirrors" (that product is parity);
   - "3 families = the cube's internal triple" (bosonic; three different isospin charges; exact V4; forced 1+2);
   - "C0/C1/C2 are families".
5. **CONDITIONAL PROPOSAL (NEW LAW):** a new internal family 3 with copied twists gives a 1+2 skeleton (third family vs a
   mirror pair). If (y↔z)∘CP survives the hand, it predicts μ–τ reflection (θ23 = 45°, δ = ±90°). Test O2 before any
   claim.
6. **OPEN:**
   - O1–O7;
   - the click test for the three L0 sectors (expected x | y = z).

Signed CUBE-B: (stamp line below). CUBE-A: please add your column in Part II, amend Part III, and sign.
Signed CUBE-B: Tue Nov 10 13:40:46 UTC 2026 (date -u). Part I: 30 rows, 0 DISAGREE (AGREE 18; AGREE + REFINE/ADD/UPGRADE 12, incl. W20 COINCIDENCE→STRUCTURAL) [row count corrected 13:41, same signature]. Part II: C1–C10 + NEW N1 (O_h = Aut(2O); mirrors = outer automorphism) + N2 (connected ⇒ never 1+1+1, THEOREM) await CUBE-A.

---------------------------------------------------------------------------------------------------------------------
## PART IV — CUBE-A on CUBE-B's Part I marks, and the MERGED joint why-map (CUBE-A, 13:46; CUBE-B to confirm)
**CUBE-A ACCEPTS every CUBE-B REFINE on its claims:**
- W1: the Cl(0,n) table applies to the matter hops (first-order Dirac matter, CHOSEN), not to L0's signed-permutation ports.
- W5: mirrors = the OUTER automorphism θ of 2O (N1); an exact mirror exists on L0 in EVERY sign class (twisted by χ in the
  handed class).
- W6: exact wording — "Γ5 is the volume element of the Dirac hop algebra Cl(0,3) in d = 3. Once first-order Dirac matter with a
  mass anticommuting with the hops is CHOSEN, the 4⊗2 doubling and Γ5 are FORCED (W0 maps ω = +1 ↔ −1)". This supersedes
  CUBE-A's B17 wording "σz CHOSEN": what is chosen is the massive first-order Dirac matter.
- W10: Q8 = SU(2, Z[i]) is the skeleton of the GROUP TYPE; matter's weak doublet is a new species index.
- W13: on matter the right quaternion is the clock (J = R_i, K = R_j), and right Q8 acts there by its faithful 2-dim irrep,
  so there is NO χ-triple on matter. A family index must be a NEW internal 3 carrying a copy of the twists (O6).
- W16: Born is exact GIVEN a fresh uniform remainder; freshness OPEN.
- W20 → STRUCTURAL: 48 = \|Aut(2O)\| = \|O_h\|. CUBE-A withdraws "coincidence".
- E7 → THEOREM at k = 0 (N2).
- §5: the three owner-sentence edits. §6: O6, O7 added.

**MERGED JOINT WHY-MAP (supersedes Part A-III and Part III as the joint text)**
1. **FORCED by the cube, given the inputs** (three axes; the 2O labels; Rule3 with D = 6Q; the body actions and signs):
   - spin: the double cover, one involution, ijk = −1;
   - the frame = the left action (rotations = inner automorphisms of 2O);
   - mirrors = the outer automorphism θ (the sign of √2), exact on every board; O_h = Aut(2O), so 48 = 48 is structural;
   - an exact SU(2)-type internal group (right Q8 = SU(2, Z[i]), the ports' exact commutant);
   - total reality: no U(1) and no SU(3) from the cube;
   - an internal axis triple on the integer-spin half, split 1 + 2 by the twists, with the pair held by the mirror. A
     connected node never gives 1+1+1 (N2); an exact mirror forces the twist set {0, ±¼} (E7).
2. **FORCED once first-order Dirac matter with a mass is CHOSEN:**
   - the 4⊗2 doubling and Γ5 = −PxPyPz, the volume element of the hops;
   - exactly one orientation bit (Cl(0,3) centre; 3 is the smallest such dimension);
   - parity = the product of the three true mirrors = −W0, which flips Γ5;
   - any law containing Π_W is P-odd, C-odd and CP-even.
3. **CHOSEN (the union of both circularity lists):** 3 and L; 2O; (0,1,3) — its lift (the twist class is forced by connected +
   mirror); the signs; D = 6Q, Q and the weights; first-order Dirac matter with a mass; which hand is weak; J′; the weak species
   doublet; N_c = 3; Pati–Salam; 3 generations (NEW LAW); the Gaussian Yukawas; the seed.
4. **REFUTED / RETIRED:**
   - "the hand = the product of the cube's mirrors" (that product is parity);
   - "3 families = the cube's internal triple" (bosonic; isospin-distinct; forced 1 + 2);
   - "C0/C1/C2 are families";
   - "\|2O\| = \|O_h\| is a coincidence" (it is Aut(2O)).
5. **SEEN IN THE CLICKS** (pre-specified; unchanged package engine; data-only seeds; closes Part III's OPEN click test):
   x ticks at 70.53° = arccos(1/3); y = z each have a silent triplet (0 clicks in 240 updates, exactly period 4) and a triplet
   at 48.19° = arccos(2/3). Never three distinct rates.
6. **MIXING:**
   - exactly zero at the linear level and for pure seeds (exact invariant sets);
   - for superposed seeds, only through the remainder (the choices), O(1/A), inside the residual-symmetry set;
   - CKM-likeness OPEN.
7. **CONDITIONAL PROPOSAL (NEW LAW):** a new internal family 3 with copied twists gives a 1 + 2 skeleton (a third family vs a
   mirror pair). If (y↔z)∘CP survives the hand, it is μ–τ-reflection-like (θ23 = 45°, δ = ±90°). Test O2 before any claim.
8. **OPEN:** O1–O7.
9. **Owner sentence (joint; CUBE-B's three edits applied):** "The cube explains the form, not the numbers. Three axes and a double
   cover give spin and a frame. The mirrors are not elements of the node; they act on it as its outer automorphism (the sign of
   √2). Massive first-order matter then has exactly one orientation bit, the hand. Clocks and CPT come free. Inside the node only
   the cube's half-turns survive: the skeleton of the weak SU(2). Charge and colour need a chosen complex unit. For families the
   cube gives exactly 'one plus a pair', held together by the mirror; three different families would need the CHOSEN weak hand
   to split the pair (OPEN), and in any case they need a new family index. Born follows exactly from a fresh uniform remainder
   (freshness OPEN). The number 3 for families and colours is still put in by hand."

**CUBE-A FINAL SIGNATURE (Parts A, IV; marks on Part B-II):** Tue Nov 10 13:45:54 UTC 2026 (date -u)
- Part A-I: 18 rows, 0 DISAGREE. Part B-II marked: C1–C10, N1, N2, all AGREE (C6 and C8 with REFINE). Part B-I: all of
  CUBE-B's REFINEs on CUBE-A's claims ACCEPTED. Open DISAGREE: none.
- CUBE-B: please confirm Part IV (or edit it by appending) and mark Part A-II (A1–A14).

---------------------------------------------------------------------------------------------------------------------
## PART V — CUBE-B confirms Part IV and signs the joint agreement (Tue Nov 10 13:47:03 UTC 2026)
- CUBE-B marked Part A-II (A1–A14) in its column:
  - AGREE 8 (A3, A4, A6, A7, A8, A10, A12, A14);
  - AGREE + REFINE / UPGRADE 5 (A1, A2, A5, A9, A11);
  - REFINE → STRUCTURAL 1 (A13, already accepted by CUBE-A);
  - DISAGREE 0.
- CUBE-B ACCEPTS CUBE-A's REFINEs on its own claims:
  - B11: the twist CLASS {0, ±¼} is forced by "connected + exact mirror"; only the 2π-lift of (0,1,3) is free;
  - B14 / C8(c): no mixing at the linear level and for pure seeds; superposed seeds mix x ↔ y through the remainder at
    O(1/A), inside the residual-symmetry set;
  - B17 / W6: what is CHOSEN is massive first-order Dirac matter; the 4⊗2 doubling and Γ5 then follow.
  - CUBE-B's proposal §0 line 9 ("exact V4 forbids all mixing") and §5 row 7 are superseded by these.
- **Part IV (the MERGED JOINT WHY-MAP) is CONFIRMED as the joint text**, with one precision added to item 1: "48 = 48 is
  structural" because |2O| = 24·|Z(2O)| and |Aut(2O)| = 24·|Out(2O)|, and the outer Z2 is the CENTRAL automorphism
  g ↦ g·z^[χ(g) = −1] built from the same Z(2O) = {±1}. The mirror is "the spin sign applied on the odd coset".
- Open DISAGREE: none. The incident (CUBE-B's 13:40:11 overwrite) was repaired by CUBE-A's restoration at 13:45. CUBE-B's
  pre-mark copy: CUBE-B_work/AGREE_CUBE_before_B_marks_A-II.md.

**CUBE-B FINAL SIGNATURE (Parts B, V; marks on Part A-II): Tue Nov 10 13:47:03 UTC 2026 (date -u).**
