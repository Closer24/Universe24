# AGREE_EINF — STUDY 28 (full Einstein on the board, rank 4): builder EINF-A, verifier EINF-B
Created by EINF-A: Tue Nov 10 15:33:17 UTC 2026. EINF-B appends below (append-only). Pre-registration: s28/EINF-A_NOTES.md.
Rules: rank 4 FINAL; B3 (six faces); exact integers; reversible; nothing posted / forced / faked / circular; default OFF.

## A. EINF-A claims (rows written Tue Nov 10 16:04:49 UTC 2026; evidence paths relative to s28/EINF-A_work/ unless they start with pkg/ = research/metric_variant_v1/)
Package files (NEW only; sha256 in new_files_sha256_1607.txt; pkg_sha256_now.txt shows that no existing .py changed):
pkg/layers/einstein.py, pkg/observe/einstein.py, pkg/tests/test_einstein.py, pkg/demos/einstein/{bending_shapiro,source_gamma,
stability}.py, pkg/NOTES_einstein.md. Composer: einstein_system(base=None, on=False, l0_beta=True). DEFAULT OFF.
Mirror: s28/EINF-A_work/mirror (package + universe24 copy). Test command, from the mirror root:
  OMP_NUM_THREADS=1 nice -n 19 python3 -m unittest research.metric_variant_v1.tests.test_einstein -v

| # | claim | label | evidence | EINF-B mark |
|---|---|---|---|---|
| A1 | DEWITT BASIS. The Fierz–Pauli (harmonic gauge) kinetic form q(h̄) = h̄·h̄ − h̄²/2 is indefinite (6+, 4−). In the integer basis F = P·h_00 (metric.h00, unchanged), a1 = P(h̄_xx − h̄_yy)/2, a2 = P·h̄_zz, a3 = P(h̄_xx + h̄_yy + 2h̄_zz)/2, h0i = P·h̄_0i, hij = P·h̄_ij, it reads 2q = (4/P²)(F² + a1² + a2² − a3² − Σh0i² + Σhij²): equal weights, field signs −1 exactly on a3 and h0i. 0 failures in 200 random exact checks of 2q and of h = TR(h̄). | THEOREM + NUMERIC | pkg/observe/einstein.dewitt_check; test T3a | |
| A2 | The 9 idle metric gears get these roles with NO new gear: hxx, hyy, hzz are renamed a1, a2, a3 in a COPY of the metric block, with signs as metadata. The free part is u-identical: replacing only that block keeps the dynamics fingerprint 593753fa. | NUMERIC | test T1c | |
| A3 | ONE CONE + EXACT DISPERSION. All ten gears have on-site 6 and six faces Q − 1, so 1 − cos w = c²·Σ(1 − cos k_d), c² = (Q−1)/(3Q), EXACTLY (integer identity). A free board plane wave turns by the exact w(k) (|Δw| < 1e-6 per update, 40 updates). | THEOREM + NUMERIC | tests T2a, T2b, T2c | |
| A4 | TWO POLARISATIONS. In lattice momenta K_μ = 2·sin(k_μ/2) the board's exact dispersion is K_0² = c²·|K|² (null). On h̄ (10-dim): the constraint has rank 4, the gauge directions rank 4 (inside the constraint) and are killed by the linearised Riemann map, whose rank on the constraint surface is 2. Checked at K = (3,4,0), (1,2,2), (2,3,6). | THEOREM (exact sympy) | pkg/observe/einstein.polarisation_count; test T3a | |
| A5 | READER = board form of (1/2)·h_μν·T^μν (kinetic fixed, metric × one-time potential): Φ_int = h_00·E_site + Σ_d (h_00 + h_dd)·E_link,d, with P(h_00 + h_dd) = 2F + Δ_d. The 2F part is today's form-C lapseL0 (unchanged). The NEW block einL0 (4,032 terms, rank 3, reciprocal, integer k·w and k·w/2) is the Δ part. Exact checks: (i) with uniform F, a1, a2, a3, L0's input at k = π·e_d is EXACTLY D·v − (Q−1)·[(1 − F/P)·M0 + (1 − (2F + Δ_d)/P)·T_d]·v (3 axes, L = 4); (ii) a uniform L0 state sources ONLY F (the inputs of a1, a2, a3 are exactly 0). | THEOREM + NUMERIC (exact) | tests T4a, T4b | |
| A6 | γ = 1 IS DERIVED, no longer chosen. Dust (T^ij = 0) sources only F, so a1 = a2 = a3 = 0 and P·h_dd = F = P·h_00: the link factor is 1 − 2h_00 = 1 − 4U by the field equation (trace reversal). The 1911 control (link factor 1 − h_00) is a reader not of the form (1/2)·h·T. Board: in the T5 run (static dust load, field built from F = 0) a1, a2, a3 stay exactly 0 for 100 updates. | THEOREM + NUMERIC | test T3b; runs/T5_bending_shapiro.json (a123_max_abs 0) | |
| A7 | The F source (E_site + ΣĒ_d)/P is the GR source of h_00 = (h̄_00 + h̄_kk)/2, i.e. active mass ρ + Σp (Tolman). The package's lapse was already the y0-component of the DeWitt coupling. | DERIVED | NOTES_einstein §2 | |
| A8 | BENDING 2× and SHAPIRO 2× on the board (pre-registered T5). L = 56; the field is built by the board from a static dust load (MECHANISM load, designated one-way, as in the package's D2/D6); U(4) = 0.027; F ≥ 0 for the whole run; rewind of 100 exact. Two one-way test lights (full reader vs h_00-only control) plus a no-read light, which is bit-identical with and without the load. Delay ratio 2.056 / 2.060 / 2.055 / 2.025 at b = 2 / 4 / 6 / 8 (window [1.8, 2.2]: PASS). Delay-slope (bending) ratio 2.08 (b 2–6) and 2.16 (b 4–8) (window [1.7, 2.3]: PASS). Beyond b = 10 the ratio falls to 1.95 – 1.85 (b 10 – 13): OPEN. | NUMERIC | runs/T5_bending_shapiro.json; pkg/demos/einstein/bending_shapiro.py | |
| A9 | γ_eff of a REAL board source (L0 lump, reciprocal; L = 20, 60 updates): h_dd/h_00 at r = 3..7 is 1.016 / 1.005 / 1.001 (x / y / z). The naive prediction from time-integrated sources is 1.045 / 1.032 / 1.027. The control without einL0 gives exactly 1 (the encoded γ). The field at r = 3..7 is dominated by the closed-board zero-mode drift (U ≈ 0.18 – 0.19, F4), so this is NOT a clean far-field test. L0's link energy W_d·(1 − shift) is INDEFINITE (signed ports), so its stress has no fixed sign. | NUMERIC (report only, as pre-registered) | runs/T4_T9_source_gamma.json | |
| A9b | γ_eff with the uniform (k = 0) modes REMOVED (same run as A9, rerun bit-identical; runs/T4b_source_gamma_k.json): 1.002 / 0.998 / 0.991 / 0.982 / 0.971 (x, r = 3..7); y: 0.993 → 0.970; z: 0.994 → 0.972. So within 3 % of 1, slightly below 1 and roughly isotropic, the sign GR's (ρ − p)/(ρ + 3p) gives for positive effective pressure. Control exactly 1. The raw A9 values are dominated by the zero-mode drift ratio (U_mean = 0.166). Report only. (Tue Nov 10 16:17:05 UTC 2026) | NUMERIC | runs/T4b_source_gamma_k.json | |
| A10 | CONSERVATION DEFECT (E2; THEOREM: not exact, G-NOGO-a), quantified in the same run. max \|D_μ s^μν\|/max \|s\| per update: ν = 0: 0.44 – 0.82 (the one-time energy source swings at 2w; the same in the control: 0.39 – 0.80). ν = x, y, z: 0.004 – 0.019 with einL0 (diagonal stress with no T^0j to balance it); 0 in the control (no spatial source). The h0i and hij sources are exactly 0 (walls A13, A14). | NUMERIC + THEOREM | runs/T4_T9_source_gamma.json; pkg/observe/einstein.conservation_defect | |
| A11 | β = 1 for L0 (E3). Block einbeta (1,296 terms, rank 3, DESIGNATED one-way): L0 reads G = F²/(2P) (existing GRAV-FIX A gear) as +G/P on M0 and +(17/8)·(G_x + G_y)/P on T, so −g00 = 1 − 2U + 2U². A reciprocal rank-4 quartic F² × L0 would need (Q−1)/(4P²) ∈ Z: grain-blocked. | DERIVED + NUMERIC (law) | pkg/layers/einstein.build_l0_beta_read; test W_beta | |
| A11b | β read, exact check: with uniform G = G0 (F = 0), L0's input at k = π·e_d is EXACTLY D·v − (Q−1)·[(1 + G0/P)·M0 + (1 + (17/4)·G0/P)·T_d]·v (3 axes, L = 4, exact integers). With the static law G = F²/(2P), the clock factor is 1 − 2U + 2U², i.e. β = 1. (Tue Nov 10 16:17:42 UTC 2026) | NUMERIC (exact) | test T4e | |
| A12 | 3-GRAVITON VERTEX. Its static 00-part, ∇²(U²) = 2(∇U)² (field energy sourcing the second-order potential), IS the existing G source −(w_G/(2P))·Lap(F²): rank 3, one-way. Its reciprocal completion is unstable (finding F1). The one-axis one-time parts h·(Δ_d h)² are rank-3 legal, NOT built (OPEN). The mixed-direction and two-time parts are impossible (A13, A14). | DERIVED / OPEN / THEOREM | NOTES_einstein §3 | |
| A13 | WALL (B3, any rank). h_ij (i ≠ j) cannot be read or sourced by any second-order field: ∂_iφ·∂_jφ needs +e_i and +e_j in one monomial (three nodes). LocalityError from the package's own validator. | THEOREM | pkg/observe/einstein.b3_offdiagonal_wall; test W_walls | |
| A14 | WALL (two-time, any rank). h_0i for second-order matter: the momentum density φ̇·∂φ is two-time (no b-only reciprocal source), and the matter's read would close an a-read cycle (AcyclicityError: no staged inverse). So there is no gravitomagnetism and no frame dragging for L0 or the light. | THEOREM | pkg/observe/einstein.two_time_cycle_wall; test W_walls | |
| A15 | MANAGER (a): the visible Dirac doublet at rest under FIX-i can NEITHER feel NOR source the lapse at rank ≤ 4. **Coupled ONE default (593753fa):** mass entries are Θ × ψ (coefficient 422,772,736), Yukawa entries Θ × H × ψ (6,451). The SU(2)-covariant dressing F × Θ × Φ × ψψ has degree 5, so RANK 5: THEOREM WALL. The only rank-4 candidate F × Θ × (bare mass)·ψψ is not covariant (breaks SU(2) at O(U), HL-1) and is non-integral (6451/32). **ONE v1:** the covariant F × Yukawa composite is rank 4 (the approved narrow kind) but grain-blocked (412,864/(2P) = 6451/2^15 ≈ 0.197; integrality needs v \| 2·6451, i.e. v ≤ 2). The integral rank-3 bare-mass dressing (12,902) breaks SU(2). NOT built; the FIX-i EP debt stays. | THEOREM (coupled default) / grain wall (ONE v1); NUMERIC census | grain_doublet.py / .json | |
| A16 | Other walls: F-4 (spring energy as a source: degree 5); light on plaquette links (route B): rank 5; E1 photon reading the metric breaks exact Gauss (UNIV T5): owner choice, NOT built; an exactly conserved reciprocal source (G-NOGO-a) and an exact Bianchi / Hamiltonian constraint (CL2 row 5) at ANY rank. | THEOREM (cited) | s23/AGREE_R5, s11/AGREE_CL2, s10/AGREE_ST | |
| A17 | MANAGER (c), stability, exact part: no NEW monomial has degree 1 (einL0 and einbeta are degree 2 in u), so the vacuum linearisation is identical to the base (test T1d: the sets of degree-1 monomials are equal after the renaming). The edge-mode lemma is not triggered; k = 0 and the corner are as in the base (marginal). Reciprocity checker: 0 violations on 13,098 b-only monomials. Rank 4. | THEOREM + NUMERIC | tests T1b, T1d | |
| A18 | MANAGER (c), reversibility: rewind exact in every run (T1e: ONE + einstein, ONE seed, L = 3, 12 updates; T5: 100 updates, L = 56; T4/T9: 60 updates, both systems; T8: 666 updates, L = 4). | NUMERIC | runs/*.json | |
| A19 | MANAGER (c), dynamics. J-pure ONE seed: L0 stays exactly dark, so einL0 and einbeta are idle and the run is bit-identical to the base. At L = 4 the BASE (coupled ONE 593753fa) runs away at t = 666 (bits 29 → 374), with the rewind exact. The runaway is in the base, NOT in this layer (flagged 16:02; ONE-LONG is diagnosing). L = 6 (design regime), S2* (L0 excited) and J-pure: see addendum A-L6. | NUMERIC | runs/T8_stability_L4.json | |
| A20 | Uniform (k = 0) modes of a2 and a3 are driven by L0's net directional link energies, like F4 for F. In the T4 run: Σ sources a2 = −8.2e16, a3 = −1.25e17 (vs F 3.2e18), so Δ_d/(2F) ≈ 2 %. No k = 0 law exists for them (OPEN, as for F). | NUMERIC + OPEN | runs/T4_T9_source_gamma.json | |
| A21 | MANAGER (b), what of the FULL field equations holds. EXACT on the board (integer identities): the ten-component harmonic-gauge (de Donder) wave operator on the ONE cone with exact lattice dispersion (A3; NOT the gauge-invariant FP operator, A24); the DeWitt kinetic structure (A1); reciprocity, i.e. Newton III, of every new coupling (A17); the exact reader factors (A5); 2 polarisations in lattice momenta (A4); γ = 1 for dust (A6). IN THE CONTINUUM / TIME-AVERAGE LIMIT: □h̄_μν ∝ ⟨T_μν⟩ in the DIAGONAL sector (h̄_00, h̄_dd), via the virial ⟨T⟩ = 2⟨E_pot⟩; Newtonian limit, redshift, bending 2×, Shapiro 2×. TO SECOND ORDER: β = 1 for L0 (designated read) and the 00-part of the cubic vertex (one-way G source). IMPOSSIBLE (theorem): h_0i and h_ij(i ≠ j) for second-order matter (A13, A14); the covariant doublet coupling in the coupled default (rank 5, A15); a conserved reciprocal source and an exact Bianchi identity (A16). So the board has the LINEARISED Einstein equations in their diagonal sector for L0, with a non-conserved source. It does NOT have the full Einstein equations. | DERIVED summary | NOTES_einstein §0 | |

### A-addendum 1 (EINF-A, Tue Nov 10 16:07:00 UTC 2026): precisions to A4, A12, A17 (new rows; earlier rows unchanged)
| # | claim | label | evidence | EINF-B mark |
|---|---|---|---|---|
| A4b | The board does NOT enforce the harmonic constraint. Per stored gear, Box g = 2 s_g + (r − r′) EXACTLY, so any constant-coefficient combination, the constraint C^ν included, obeys Box C^ν = 2 D_μ s^μν + ledger (identity; the package's G5 shows it in the original basis). Radiation from a non-conserved board source (A10) therefore carries non-TT (scalar / vector) parts in proportion to the defect. "2 polarisations" (A4) holds on constraint-satisfying data. | THEOREM (linear identity) + DERIVED | observe/gravity.lorenz_identity_residual (G5); A10 | |
| A12b | Reason the cubic vertex's 'graviton feels gravity' part is NOT built: it is rank-3 legal (metric link energies × (h_00 + h_dd)), but the ONE headroom stencil has headroom 1/(3Q). So wherever h_00 + h_dd < 0 the metric's own corner mode leaves the band (CFL; package findings F1/F2). The live closed-board uniform lapse drifts negative (STAB R11: U_mean −0.036). Unsafe at the ONE stencil: OPEN (it needs a stencil with headroom, e.g. stencil B, an owner choice). | DERIVED | NOTES_gravity F1/F2; s18 STAB R11 | |
| A17b | Precision: the layer is IDLE on every state with L0 = 0 and a1 = a2 = a3 = 0 (exact: every new monomial has an L0 factor or an a factor that vanishes there). For a uniform L0 background the a's k = 0 mode stays decoupled (L0's link energy vanishes at k = 0). | THEOREM | tests T1d, T4a | |
| A5b | NULL BEAM (exact). A RECIPROCAL test light beam along x (k = π·e_x) sources the metric exactly as a null beam does in GR: the h̄_yy and h̄_zz sources are 0 and the h̄_00 source equals the h̄_xx source (T_00 = T_xx, traceless), exact integers, L = 4. The missing piece of the GR beam field is h̄_0x (wall A14). | THEOREM + NUMERIC (exact) | test T4d (Tue Nov 10 16:08:35 UTC 2026) | |
| A8b | Honesty note on A8. For a DUST source the a's vanish exactly, so in the bending / Shapiro run the full reader reduces to 2F/P per link: numerically the same as the package's encoded 'GR' light with a lapse-only field. What is NEW is that the 2 is now forced by the field equation (A6), not chosen. The runs that exercise the a's are A5b, A9, A10 (L0 / light sources). | DERIVED | — | |
| A23 | GAUGE FIELDS (E2 'where the grain allows'). The compact links (su2, su3, u1, wsu2) cannot gravitate at rank 4 without a wall. (i) Their norm coupling F·(\|U\|² − A²) has a bilinear at the vacuum (2A·u_1), so the edge-mode lemma applies (s18 R5 THEOREM; this is the runaway that FIX-i removed). (ii) Their wave energy sits in the OD4 springs / relays (quartic), so F × spring is degree 5 = rank 5 (F-4). (iii) The stationary balanced composite (route (c)) avoids the bilinear but is grain-blocked (κ = 2^-11; STAB R15). So: none of them gravitates, and none is built. | THEOREM (cited) + DERIVED | s18/AGREE_STAB R5, R15; s23/AGREE_R5 D5 (Tue Nov 10 16:09:51 UTC 2026) | |
| A24 | THE LAW IS THE HARMONIC-GAUGE (de Donder) OPERATOR, not the gauge-invariant Fierz–Pauli operator. Box h̄_μν on each stored gear is diagonal and identical for all ten. The gauge-invariant G⁽¹⁾_μν[h] needs mixed second differences (∂_x∂_y h_xy: edge offsets, B3-illegal) and mixed ∂_t∂_i terms (symmetric two-time reads between h_0i and h_ij: an a-read cycle). So it cannot be the board law at rank ≤ 4. The law therefore propagates all ten components; 'two polarisations' is a property of constraint-satisfying data (A4, A4b). This agrees with EINF-B's pre-registered P1/P3. | THEOREM (locality + acyclicity) | NOTES_einstein §1/§5 (Tue Nov 10 16:11:37 UTC 2026) | |
| A22 | Structural risk, stated (EINF-B's Krein lemma P5, as refined by EINF-B 16:12). The DeWitt metric is indefinite, and a3 (s = −1) is a ghost-sign wave reciprocally coupled to L0's stress. There is NO direct metric–metric bilinear (EINF-B audit: 0). The matter-mediated static mixing is semidefinite where every L0 mode lies on one side of the cone frequency (low k), so it gives no complex eigenvalues there. Krein growth would need an indefinite mixing at lattice-scale k (cone between L0 bands) or a difference resonance with the background's w0 / 2w0 oscillation. A direct test with an L0 lump is MASKED by the base's F4 drift: with A = 2^16 at L = 6, BOTH the einL0 run AND the control without einL0 blow up at t ≈ 45–60, after the uniform U passes 1/4 (U_F = 0.224 at t = 40) and L0's link factor 1 − 4U flips. EINF-A's krein.py was withdrawn (16:14). The test of record is EINF-B's krein_comp.py (uniform modes cancelled by diagnostic loads; control = the same einL0 potential with all signs +1). OPEN until it reports. (Tue Nov 10 16:13:11 UTC 2026) | DERIVED + NUMERIC (masking) + OPEN | EINF-B_NOTES §3; EINF-A smoke run (L = 6, 80 updates; console only) | |

### A-L6 addendum (EINF-A, Tue Nov 10 16:15:21 UTC 2026): L = 6, the design regime
| # | claim | label | evidence | EINF-B mark |
|---|---|---|---|---|
| A25 | ONE + Einstein (on), ONE S2* seed, L = 6, 600 updates: bounded (max 27 bits); rewind of 600 exact; bit-identical to the base OFF run (593753fa: same bits and U_mean at every sample). L0 stays EXACTLY dark under the ONE S2* bang too (max \|L0\| = 0), and a1 = a2 = a3 ≡ 0. So the layer is idle on both ONE bangs (A17b). The J-pure L = 6 run was cancelled as redundant (ONE-A T3: bounded 1200). | NUMERIC | runs/T8b_stability_L6_s2star.json | |
| A26 | To exercise einL0 / einbeta INSIDE ONE: the J-pure ONE seed plus an L0 lump (seed data, A = 2^12, sigma 1.5), L = 6, 400 updates, ON vs OFF. (Row text before the result; the result is A27.) | NUMERIC | runs/T8d_stability_L6_jpure_l0.json | |
| A27 | RESULT of A26 (Tue Nov 10 16:19:44 UTC 2026): ONE + Einstein with L0 excited (max \|L0\| 1,359 → 487 – 977) is BOUNDED for 400 updates at L = 6 (max 24 bits, the same as OFF), and the rewind of 400 is exact for both. The layer acts: max \|a\| goes 0 → 6,330, and L0 differs slightly ON vs OFF (e.g. 977 vs 958 at t = 300). The a's uniform modes drift ∝ t² as predicted (A20): U-means at t = 400 are a1 2.7e-4, a2 1.2e-3, a3 3.0e-3, against F 0.042 (the base's F4 drift, identical OFF). So Δ_z/P ≈ −0.007 against 2F/P ≈ 0.17 (≈ 4 %). Extrapolated, F reaches U = 1/4 near t ≈ 1,000 with this lump: the base's F4, not this layer. | NUMERIC | runs/T8d_stability_L6_jpure_l0.json | |

### A-addendum 3 (EINF-A, Tue Nov 10 16:23:28 UTC 2026): (i) OWNER base change, (ii) EINF-B's required edits E-a … E-g ADOPTED (wording; no law change)
(i) The owner ruled (~16:13 UTC; manager 16:25 / 16:31) that matter must NOT read the cosmic clock. AFTER THE PUSH the default is
ONE v1 (couple_doublet=False, fp 77f6d251), and the coupled build (593753fa) is an explicit opt-in. ONE-SWITCH's patch of
layers/one.py is installed only at the final delta (~17:50 UTC). So TODAY one_system() still returns 593753fa, and
einstein_system(base=None) builds on it (ON fp 3ebe7bb6); with base=one_system(couple_doublet=False) the ON fp is c6996dce.
The Einstein layer stays DEFAULT OFF on both, and every result below is stated for BOTH bases.
[CORRECTED Tue Nov 10 16:28:45 UTC 2026 after EINF-B B16 and the manager's 16:31 note; the first wording "one_system() now defaults to ONE v1" was
premature]
einstein_system(base=None) builds on whatever one_system() returns. No fingerprint is hard-coded as "the default" any more.
| # | claim | label | evidence | EINF-B mark |
|---|---|---|---|---|
| V1 | BOTH BASES (tests now use EXPLICIT bases: v1 first, coupled second; 17/17 OK, 16:23:28):<br>- on=False returns the given base: v1 77f6d251 and coupled 593753fa;<br>- base=None equals one_system();<br>- the DeWitt metric copy alone ≡ each base's dynamics;<br>- rank 4 and reciprocity 0 violations on both ON tensors;<br>- no new degree-1 monomial on both;<br>- vacuum fixed (L = 3, 4) and ONE-seed rewind exact (L = 3) on both. | NUMERIC | test_einstein_run_v1_1622.log; pkg/tests/test_einstein.py | |
| V2 | The board PASS runs T5 (bending / Shapiro) and T4 / T9 (γ_eff, conservation defect) use REDUCED systems built only from layers.gravity, gravity_l0c and einstein: no ONE block and no cosmic block. They are therefore base-INDEPENDENT and hold unchanged for v1 (EINF-B reproduced them bit for bit). | NUMERIC (by construction) | pkg/demos/einstein/bending_shapiro.py, source_gamma.py | |
| V3 | (a) FOR THE NEW DEFAULT (ONE v1), plainly:<br>- the visible Dirac doublet at rest can NEITHER feel NOR source the lapse;<br>- the SU(2)-covariant dressing F × Yukawa composite (F·Φ·ψψ) is rank 4, of the APPROVED narrow kind, but GRAIN-BLOCKED: 412,864/(2P) = 6451/2^15 ≈ 0.197 per unit Higgs, and integrality would need v \| 2·6451, i.e. a Higgs vev of 1 or 2 units;<br>- the integral rank-3 bare-mass dressing (12,902 = (m + 6w)/(2P)) breaks SU(2) at O(U);<br>- the vev-response route (L2(b)) triggers the edge-mode lemma, hence FIX-i;<br>- the doublet keeps only the FIX-i singlet-half hop read (768 degree-2 terms) and its EP debt.<br>So under v1 this is a GRAIN wall, not a rank wall. In the coupled opt-in it is a RANK wall (degree 5, A15). | NUMERIC census + DERIVED | grain_doublet.json (ONE_v1_uncoupled) | |
| V4 | Stability on the v1 base (L = 6, J-pure + L0 lump, 400 updates; and L = 4, J-pure, 700 updates): result in addendum A-V1R. | NUMERIC (pending) | runs/T8v1_*.json | |
(ii) EINF-B's edits, adopted (new wording supersedes the cited rows; the original rows stay for the record):
| # | claim (adopted wording) | label | evidence | EINF-B mark |
|---|---|---|---|---|
| E-a → A1′ | "the ONLY integer way" → "an integer way". Several exact rational bases exist; Sylvester fixes only the inertia 6+/4−. Ours keeps the lapse metric.h00 as a gear. With the lapse kept, the rest of the diagonal sector has DeWitt form 2(Σh̄_dd² − S²) of signature (2+, 1−), so z is necessarily singled out. A cubic-symmetric integer basis exists only WITHOUT the lapse as a gear: 4q\|diag = Σ_d (h̄_00 + 2h̄_dd + S)² − (h̄_00 + 3S)² (0 failures / 500, checked). My earlier "no permutation-symmetric basis exists" was too strong: CORRECTED. | THEOREM + NUMERIC | docstring + NOTES §1 | |
| E-b → A4′ | "2 polarisations" means: 2 ON constraint-satisfying data; 6 in general (E(2) class II6: Riemann rank 6 on unconstrained null data); the vacuum Ricci = sym(K·C). The law propagates all ten components (A24, A4b). | THEOREM (EINF-B riemann_rank) | EINF-B_NOTES §3 | |
| E-c → A6′ | γ = 1 for dust follows from the trace-reversed identification F = P·h_00 together with the board reader (h_00 on site, h_00 + h_dd on links), which is a CHOSEN board form of ½hT. The link factor is no longer a free parameter inside that form: the 1911 value is excluded. NEW: h_dd is a field sourced by the stress, and the DeWitt signs make STRESSED sources GR-like ((ρ − p)/(ρ + 3p)) and isotropic. With a3 at +1 the response would be anisotropic (EINF-B isotropy_sign). | DERIVED | A5b, A9b, EINF-B isotropy_sign.json | |
| E-d → A14′ | Split. FEELING h_0i (second-order matter) is impossible: an a-read cycle (THEOREM). A designated one-way two-time SOURCE of h_0i is legal and simply NOT built (CHOSEN). | THEOREM / CHOSEN | docstring + WALLS updated | |
| E-e → docstring | The docstring and WALLS line "metric × link × ψ × ψ′ = degree 4 (rank 5)" MISCOUNTED: without Θ that product is rank 4. Replaced by A15 / V3's wording: degree 5 with Θ (coupled opt-in); in v1 the narrow kind is rank 4 but grain-blocked. | CORRECTION | pkg/layers/einstein.py (16:21) | |
| E-f → A8c | The excess over 2 is the predicted O(U) term of the built factors: n_full = (1 − 4U)^−½, n_ctl = (1 − 2U)^−½. So the delay ratio ≈ 2(1 + 1.5U) and the slope ratio ≈ 2(1 + 3U). EINF-B's straight-ray eikonal on the measured profile gives 2.086 / 2.058 / 2.047 / 2.040 (b = 2 / 4 / 6 / 8), against the measured 2.058 / 2.060 / 2.055 / 2.025; and slopes 2.17 / 2.11 against 2.08 / 2.16. γ = 1 holds at first order. | DERIVED + NUMERIC | EINF-B second_order_ratio.py | |
| E-g → A11′, A12′ | β = 1 for L0 holds for STATIC fields only (G's static law G = F²/(2P)). The 3-graviton vertex is PARTIAL: only its static 00-part (the one-way G source). | DERIVED | NOTES §3 | |

### A-addendum 4 (EINF-A, Tue Nov 10 16:28:00 UTC 2026): A-V1R (V4 results on the v1 base) and replies to EINF-B's EDITs
| # | claim | label | evidence | EINF-B mark |
|---|---|---|---|---|
| A-V1R-a | v1 base (77f6d251) + Einstein (ON fp c6996dce), J-pure ONE seed + L0 lump (A = 2^12), L = 6, 400 updates:<br>- BOUNDED, max 25 bits, the same as the v1 base OFF;<br>- rewind of 400 exact for both;<br>- the layer acts: max \|a\| 0 → 6,587;<br>- a's uniform drift ∝ t² (U at t = 400: a1 2.7e-4, a2 1.18e-3, a3 2.97e-3), against F 0.0427 (OFF 0.0427).<br>All int64 steps. Numbers within 1 % of the coupled-base run A27: the L0 / metric sector is base-blind. | NUMERIC | runs/T8v1_L6_jpure_l0.json | |
| A-V1R-b | v1 base, J-pure ONE seed, L = 4, 700 updates (ON vs OFF): written before the result; the result is A-V1R-c. | NUMERIC | runs/T8v1_L4_jpure.json | |
| A-V1R-c | RESULT (Tue Nov 10 16:29:04 UTC 2026). On the v1 base (77f6d251) the J-pure seed at L = 4 is BOUNDED for 700 updates (max 29 bits, ON = OFF bit for bit) and the rewind is exact for both. L0 stays dark, so the layer is idle. The coupled build ran away at t = 666 on the same seed (A19). So the L = 4 runaway belongs to the COUPLED build (matter reading the cosmic clock, now rejected by the owner), not to v1 and not to this layer. This is a datum for ONE-LONG; their per-sector diagnosis is the record. | NUMERIC | runs/T8v1_L4_jpure.json vs runs/T8_stability_L4.json | |
| R-A1/A6/A4 | EDITs accepted. NOTES §0.1 now says "an integer way"; A6 is labelled "DERIVED given the board reader"; A4's count is "2 on the constraint surface, 6 in general". | — | NOTES_einstein.md | |
| R-A8 | EDIT accepted. Scope: one-way test lights and a MECHANISM dust load; no light of the ONE content reads the metric (E1 not coupled). The b ≥ 10 dip is plausibly wave-optics / caustic structure (OPEN). | — | NOTES §5 | |
| R-A10 | EDIT accepted. The ν = 0 number mixes (i) the G-NOGO-a 2w swing of the one-time source and (ii) the missing momentum flux of the dispersing lump (s^0i ≡ 0). A period-averaged defect would separate them (not done). | — | NOTES §5 | |
| R-A20/A21 | EDITs accepted. a2 and a3 are TWO NEW F4-type uniform modes with NO bgk-type compensation; with L0 matter they push the link factor 1 − (2F + Δ)/P toward 0, alongside F. The verdict adds: the ghost-sign gears PROPAGATE (no constraint removes them; Krein around matter tested in B5: no ghost-specific growth, OPEN at lattice k); universality = L0 only; 2 polarisations on the constraint surface, 6 in general. | — | NOTES §0, §6 | |
| R-B14 | EINF-B's new prediction is accepted as DERIVED (not run): with h̄_0x walled off, parallel light beams attract on the board (exchange 2EE′), whereas GR gives 0 for parallel beams (Tolman–Ehrenfest–Podolsky). This is a falsifiable lattice signature of the missing gravitomagnetism. | DERIVED | EINF-B B14 | |

## B. EINF-B marks (append-only)

### EINF-B block 1 — appended Tue Nov 10 16:27:17 UTC 2026 (append-only; rows by EINF-A are untouched above)

### B-1. EINF-B marks on EINF-A's rows
Appended by EINF-B; stamps in each block header.
Basis of the marks:
- my pre-registration s28/EINF-B_NOTES.md §1 (15:44:34, before layers/einstein.py existed at 15:48:17);
- my own checks in s28/EINF-B_work/;
- re-runs in my scratch mirrors (mirror1 15:53:46, mirror2 16:03:58, mirror3 16:17:04, mirror4 16:21:52, mirror5 16:25:33).
- einstein.py: 7cd82dc2… until 16:21:42, then ff6e2079… (docstring/WALLS only; the coupled ON dyn fp is 3ebe7bb6… in both).

| # | EINF-B mark | reason / evidence |
|---|---|---|
| A1 | **ACCEPT + EDIT** | 2q identity and the inverse maps hand-verified; re-run test T3a OK. EDIT: drop "the ONLY integer way" (NOTES §0.1 and the docstring). Other exact rational bases exist (gamma_dewitt.json): c = 1 (Hadamard on (00,xx,yy,zz) + pairs (3h_ij + h_0k)/2, (h_ij + 3h_0k)/2) and c = 2 (2h_ij at +1, 2h_0i at −1, trace ghost mixed). What is FORCED is the inertia 6+/4− (Sylvester), not the basis. EINF-A's basis is the cleanest (equal weights; h0i and hij untouched) |
| A2 | ACCEPT | audit_tensor.json: ON minus {einL0, einbeta} ≡ base dynamics; all 10 free stencils are headroom |
| A3 | ACCEPT | symbol m(k) = 6 + 2(Q−1)Σcos k_d is exact at every k (my P2); re-run T2a–T2c OK |
| A4 | **ACCEPT + EDIT** | The count 2 holds ON the constraint surface (A4b/A24 now say so: EDIT A4's own wording to match). EINF-B riemann_rank.json (sympy, K = (3,4,0), (1,2,2), (2,3,6), (1,0,0)): linearised Riemann rank is 6 on all 10-dim null data (2 TT + breathing + longitudinal + 2 vector) and 2 on the constraint surface; the vacuum Ricci = sym(K·C) exactly (ratio 1). So sourced board waves carry 4 non-GR polarisations ∝ C ∝ the source defect (A10) |
| A4b | ACCEPT | = my P4 identity (pre-registered): Box C = 2·div s + ledger, exact |
| A5 | ACCEPT | re-run T4a/T4b OK (exact integers) |
| A5b | ACCEPT | test T4d re-run OK (mirror3, 16/16). Note: this structure REQUIRES the ghost sign (with a3 at +1: h̄_00 = 6E_x, h̄_xx = 0, h̄_yy = −2E_x). Consequence (B14): with h̄_0x walled off, parallel beams attract on the board; GR says they do not |
| A6 | **ACCEPT + EDIT** | For DUST, γ = 1 follows from the identification F = P·h_00 = P(h̄_00 + h̄_kk)/2 plus the reader (h_00 on site, h_00 + h_dd on links). It does NOT depend on the a-signs: dust leaves a1–a3 unsourced for any signs. It equals the old c_link = 1 number (A8b says this honestly). The reader is a CHOSEN board form of ½hT (kinetic fixed), so label "DERIVED given the board reader". The signs matter for STRESS (isotropy_sign.json, exact): with a3 = −1 the response to isotropic stress is isotropic and equals GR's (ρ−p)/(ρ+3p) = (E_site+2E)/(E_site+6E); with a3 = +1 it is ANISOTROPIC: x, y (E_site+10E)/(E_site+6E), z (E_site+18E)/(E_site+6E). So the ghost sign is what makes the layer GR and cubic-symmetric |
| A7 | ACCEPT | with Ē_d = 2E_link,d: ∂Φ/∂F·P = E_site + 2ΣE_d ∝ ρ + Σp (virial ρ = 2E_pot, p_d = 2E_d) |
| A8 | **ACCEPT + EDIT** | Re-run reproduces EINF-A's JSON to every digit (reruns/T5_bending_shapiro_B.json). EDIT: the excess over 2 is the predicted second-order term of the BUILT factors. n_full = (1−4U)^−½ and n_ctl = (1−2U)^−½ give a delay ratio ≈ 2(1 + 1.5U) and a slope ratio ≈ 2(1 + 3U). The straight-ray eikonal on the measured profile gives delay 2.086/2.058/2.047/2.040 (b = 2/4/6/8) and slope 2.17/2.11 (second_order_ratio.json). Scope: one-way test lights and a MECHANISM load; no light of the ONE content reads the metric (E1 not coupled). The b ≥ 10 dip, with the ratio oscillating 1.85 (b 13) → 2.13 (b 18) → 1.95 (b 24), looks like wave-optics/caustic structure plus field build-up: OPEN, agreed |
| A8b | ACCEPT | honest and correct |
| A9 | ACCEPT (report only) | re-run identical; the T4b zero-mode-removed re-run is identical too (x 1.002 → 0.970, y 0.993 → 0.970, z 0.994 → 0.972 over r = 3 → 7; control 1): roughly isotropic, slightly below 1. γ_eff > 1 means negative effective pressure (signed-port link energy); U ≈ 0.18–0.19 is drift-dominated. Not a far-field test: agreed |
| A10 | **ACCEPT + EDIT** | re-run identical (ν0 0.44–0.82 vs 0.39–0.80 in the control; νi 0.007–0.019 vs 0). EDIT: since s^{0i} ≡ 0 (A14), the ν = 0 number is |Δ_t s^00| alone. It mixes (i) the G-NOGO-a 2w swing of the one-time source (F source total 4.18e16–7.02e16, mean 5.38e16) and (ii) the missing momentum flux of the dispersing lump. A period-averaged defect would separate them. My P9 "O(1)" is confirmed |
| A11 | **ACCEPT + EDIT** | β = 1 via G = F²/(2P) holds for STATIC fields only: stencil B is off the cone and lags any time-dependent F, and Lap kills k = 0, so the clock reads 1 − 2U + 2U² − (uniform offset), harmless for orbits. EINF-B perihelion.json (quadrature, ratio to GR at μ = 1e-7): L0 form C alone 1.3333343 (4/3); L0 + einbeta 1.0000007 (1); hands-OFF Dirac R1 1.1666673 (7/6); the live doublet has none (A15) |
| A12 | **ACCEPT + EDIT** | accept as the STATIC 00-part (the U² of −g00 = e^{−2U}), one-way, off the cone. It is NOT the dynamical cubic vertex: no GW self-interaction and no GW energy sourcing (cross-axis parts B3-illegal, time parts two-time). Label "PARTIAL" |
| A12b | ACCEPT | consistent with the exact corner margin 2/Q (krein.json Part A) |
| A13 | ACCEPT | my b3_probe P7a and its reciprocal partner P7a′ (an edge offset) |
| A14 | **ACCEPT + EDIT** | FEELING h_0i is impossible: the force needs the matter's own φ̇, a self a-read, or mutual a-reads, i.e. a cycle. A SOURCE-only h_0i (designated, sourced by φ̇·∂φ, matter not reading) is acyclic and rank-3 legal (b3_probe P1d pattern). So "no gravitomagnetism FELT by L0 or light" is a THEOREM, while "h_0i unsourced" is CHOSEN (not built) |
| A15 | **ACCEPT + EDIT** | A15's count is right: Θ × F × H × ψψ is degree 5 in Φ, i.e. rank 5. EDIT: the WALLS dict and the module docstring of layers/einstein.py still say "metric × link × ψ × ψ′ is degree 4 (rank 5)". Without Θ that product is rank 4. The rank-5 count needs Θ (theta_scale_block refuses Θ × degree-3) or the Higgs factor. Replace with A15's wording. Census reproduced (census_doublet.json): Θ×ψ 422,772,736 (16 per namespace), Θ×H×ψ 6,451 (64) and 64 (3,072); the max input degree into the doublet is already 3 |
| A16 | ACCEPT | cited theorems; F-4 rank error reproduced by the parser (b3_probe P7f) |
| A17 | ACCEPT (vacuum) | audit: 0 metric–metric bilinears, all new terms degree 2 with metric/β × L0. The vacuum spectrum is unchanged. NOT covered by A17: matter backgrounds (A22, B5) |
| A17b | ACCEPT | |
| A18 | ACCEPT | rewind exact in my re-runs of T5, T4/T9 and T8 (B-2 row B9) |
| A19 | **ACCEPT** | re-run IDENTICAL (reruns/T8_stability_L4_B.json): ON ≡ OFF, L0 exactly 0 for all 666 updates, bits 24 → 29 → 374, rewind exact. NOTE: by its own pre-registered code T8 is FALSE (374 > 60); the failure is the BASE's and the layer is idle there, so T8 does not test the layer. EINF-A's L = 6 J-pure + L0 lump (A = 2^12, 400 updates, bounded) is the first run in which the layer acts |
| A20 | **ACCEPT + EDIT** | re-run identical (Σ sources a2 −8.17e16, a3 −1.25e17, F 3.23e18). My krein_board L = 6 run also shows a3 drifting. EDIT: a2/a3 have NO bgk-type compensation. These are TWO NEW F4-type uniform modes added by the layer; with L0 matter they push the link factor 1 − (2F + Δ)/P toward 0 as well |
| A21 | **ACCEPT + EDIT** | add: (i) the ghost-sign gears PROPAGATE, because no constraint removes them (T7); Krein channel around matter: B5; (ii) two new uniform drifts (A20); (iii) universality = L0 only (visible doublet, E1, gauge fields, Higgs and cosmic block uncoupled: A15, A23); (iv) 2 polarisations on the constraint surface, 6 in general (A4) |
| A22 | ACCEPT | my refinement, correctly stated. Test of record (B5): no ghost-specific growth; the base's uniform lapse fails first |
| A23 | ACCEPT | cited theorems (s18 R5, R15; F-4) |
| A24 | ACCEPT | = my P1 (pre-registered 15:44): b3_probe P1a–P1c (edge offset, a-read cycle) |
| V1 | **ACCEPT** | my own both-base audit agrees (B15); 17/17 re-run in mirror5. But see B16: base=None is still the COUPLED build in the package |
| V2 | ACCEPT | reduced systems, no ONE/cosmic block; my re-runs are bit-identical |
| V3 | ACCEPT | correct reading. Under v1 the doublet wall is a GRAIN wall (narrow kind, rank 4, 0.197 per unit Higgs); a RANK wall only in the coupled opt-in |
| V4 | (pending at the time of this block) | marked in the signature block if available |
| A1′ | ACCEPT | cubic-symmetric identity verified EXACTLY (cubic_basis_check.json: 4q\|diag identity true; remainder eigenvalues 1, 1, −2, i.e. (2+, 1−)) |
| A4′ | ACCEPT | = B4 |
| A6′ | ACCEPT | = my E-c (B10 isotropy) |
| A14′ | ACCEPT | = my E-d |
| E-e | ACCEPT | verified as docstring/WALLS-only: the coupled ON dyn fp is 3ebe7bb6… before and after |
| A8c | ACCEPT | = B7 |
| A11′/A12′ | ACCEPT | static only; vertex PARTIAL |

### B-2. EINF-B's own rows
| # | claim | label | evidence |
|---|---|---|---|
| B1 | PRE-REGISTRATION kept (15:44:34, before layers/einstein.py appeared at 15:48:17). Outcomes: P1 harmonic gauge only ✓ (= A24); P2 exact one-cone symbol ✓ (A3); P3 10 propagate, 2 on the constraint surface ✓ (A4b; Riemann rank 6/2); P4 constraint propagation driven by div s ✓ (A4b); P5 vacuum safe ✓ (A17), Krein refined (B2) and not observed (B5); P6 γ = 0 for all-plus reciprocal designs; EINF-A chose route (b-i) ✓; P7 walls ✓ (A13–A16; A14 needs an EDIT); P8 β via U², vertex partial ✓ (A11, A12); P9 bending/Shapiro 2× ✓; defect O(1) ✓ (0.44–0.82); monopole radiation at 2w0 NOT measured (proposal M-1) | NUMERIC + DERIVED | EINF-B_NOTES §1–§4 |
| B2 | KREIN LEMMA. With field signs S the linear law is b⁺ + b⁻ = (2/D)(H + S·M)b. Two degenerate modes of OPPOSITE sign with an INDEFINITE mixing give μ = μ0 ± iε, so \|λ\| > 1 at any k. A SEMIDEFINITE mixing (M = ±RRᵀ) gives real eig(S·M) = eig(±RᵀSR), hence no growth. Exact Python-int toy (L = 6, Q = 9): normal pair bounded for 400 updates, ghost pair ×1e8 (1.053 per update; Bloch max 1.084) | THEOREM + NUMERIC | krein.py / .json; NOTES §3 refinement |
| B3 | γ FROM THE FIELD EQUATIONS NEEDS THE DeWitt SIGN. Reciprocal Φ = ½hT with all field signs +1 gives γ = 0 (h basis and h̄ basis: E(light, M)/E(M, M) = 1). Designated (h̄ ← T, matter reads h): γ = 1. Rational DeWitt bases with 4 ghosts exist and are NOT unique | DERIVED (sympy, exact) | gamma_dewitt.py / .json |
| B4 | POLARISATION CONTENT. For null lattice K = (3,4,0), (1,2,2), (2,3,6), (1,0,0): Riemann rank 6 on all 10-dim data, 2 on the constraint surface. The vacuum Ricci = sym(K·C) exactly. So the board's sourced waves carry breathing, longitudinal and vector parts ∝ C | THEOREM (sympy) | riemann_rank.py / .json |
| B5 | KREIN TEST OF RECORD (L = 6, L0 lump A = 2^14; uniform modes cancelled by DIAGNOSTIC static loads; base vs perturbed copy; per-update 60-bit guard). The perturbed copy blows up in ALL variants: OFF (no einL0) t = 180, CTL (signs +1) t = 487, ON (as built) t = 589. The difference stays 2e4–1.4e5 in CTL and ON beforehand: NO ghost-specific growth. Diagnosis (OFF re-run): the difference is 99.8 % the UNIFORM lapse mode, corner share < 1e-7, then a super-exponential nonlinear explosion (U > ¼ flip) in 5 updates. The failure mode is the base's marginal uniform lapse (F4), not Krein. Krein at lattice k / difference resonances: not isolated by this test, OPEN (proposal K-2) | NUMERIC + OPEN | krein_comp.py / krein_comp_L6_A14.json; corner_diag.py / .json |
| B6 | PERIHELION PER CLOCK FAMILY (eikonal ω² = A(U)m² + B(U)k²; ratio to GR at μ = 1e-7): GR 1.0000007; L0 form C 1.3333343 (4/3); L0 + β read 1.0000007; Dirac R1 1.1666673 (7/6); Dirac + U² read 1.0000005; 1911 control 0.6666669 (2/3). So β matters: without einbeta, L0's orbit would precess 4/3 × GR | DERIVED + NUMERIC (quadrature) | perihelion.py / .json |
| B7 | T5's EXCESS OVER 2 = the predicted U² term of the built link factors: delay ≈ 2(1 + 1.5U), slope ≈ 2(1 + 3U); eikonal on the measured profile gives 2.04–2.09 / 2.09–2.17 (measured 2.02–2.06 / 2.08–2.20) | DERIVED + NUMERIC | second_order_ratio.py / .json |
| B8 | FILE INTEGRITY. From my baseline (15:44:41) to 16:08:24 and again at 16:24:36, only the 8 new EINF-A files appeared; 0 existing files changed; the 7 ONE files are unchanged (layers/one.py 57de300d…). The final check is in the signature block | NUMERIC | baseline_sha256.txt, now_sha256.txt, now2_sha256.txt |
| B9 | RE-RUNS: tests 15/15 (mirror2), 16/16 (mirror3), 17/17 (mirror4) and 17/17 (mirror5: explicit v1 + coupled bases). T5, T4/T9, T4b and T8 reproduce EINF-A's JSON bit for bit | NUMERIC | rerun_test_einstein*.log, reruns/ |
| B10 | ISOTROPY NEEDS THE GHOST SIGN. In EINF-A's basis, an isotropic stress gives h_dd/h_00 = (E_s+2E)/(E_s+6E) on all axes with a3 = −1, which is exactly GR's (ρ−p)/(ρ+3p). With a3 = +1 it gives x, y (E_s+10E)/(E_s+6E) and z (E_s+18E)/(E_s+6E): anisotropic, non-GR | DERIVED (sympy, exact) | isotropy_sign.py / .json |
| B11 | B3/RANK PROBE (package parser, 19/19 as pre-registered): edge offset (FP mixed ∂x∂y), a-read cycle (symmetric ∂t∂i), node-scalar T^xy (three nodes), lapse × magnetic energy (three nodes), F-4 (4 factors) all rejected; Dirac-hop T^xy and diagonal T^ii legal; link-field A_x(x)A_y(x) storage-legal but strict-support-illegal; direct F²ψ read legal (rank 4); cross-axis vertex illegal | NUMERIC (parser) | b3_probe.py / .json |
| B12 | NEW UNIFORM DRIFTS. The layer adds two F4-type k = 0 modes (a2, a3) with sign-definite net sources and no compensation (my L = 6 lump run: a3 4.4k → 20.7k in 30 updates; EINF-A L = 6: U_a3 = 3e-3 at t = 400). With F's drift they set the long-run limit of any L0-matter run | NUMERIC + OPEN | krein_board.py; A20 |
| B13 | PLAIN VERDICT (E5), verifier's wording: the board carries linearised Einstein in HARMONIC GAUGE for all ten components on the one cone. It agrees with GR for constraint-satisfying data; the constraint is not imposed and the source is not conserved. The coupling is reciprocal and diagonal, for L0 only. γ = 1 for dust (same number as before, now from a 10-component field); bending/Shapiro 2× (+ the predicted U² excess); β = 1 static, via a one-way read. NOT full Einstein: conserved source, Bianchi, h_0i felt, off-diagonal stress, visible doublet, springs/plaquettes are all walls. Keep DEFAULT OFF | DERIVED summary | B1–B12 |
| B14 | NEW FALSIFIABLE PREDICTION (from A5b and A14): with h̄_0x walled off, the beam–beam exchange is 2EE′ for parallel AND antiparallel beams. GR gives EE′(k·k′)², i.e. 0 for parallel and 4EE′ for antiparallel (Tolman–Ehrenfest–Podolsky). So on the board, co-moving parallel light beams attract; in GR they do not. Not run | DERIVED | NOTES §4 |
| B15 | BOTH-BASE LAW AUDIT (mirror5, 16:25:33). v1 (77f6d251) + Einstein: 23,920 monomials, rank 4, 3 stages, strict-support 3,300 = base; OFF is the base object; ON minus new ≡ base; reciprocity ok (0 violations; +4,032 checked, +1,296 designated); signs −1 on {a3, h0i}; 0 metric–metric bilinears; 5,328 new degree-2 terms; ON fp c6996dce…. Coupled (593753fa) + Einstein: as in §3, ON fp 3ebe7bb6… | NUMERIC | audit_tensor_v1.json, audit_tensor_coupled.json, on_fingerprints.txt |
| B16 | DISCREPANCY TO FLAG. Addendum 3 (i) says "one_system() now defaults to ONE v1 (ONE-SWITCH's patch)". In the package at 16:24:36 and 16:25:33, layers/one.py is UNCHANGED (sha 57de300d…), and one_system() returns the COUPLED build (593753fa). So einstein_system(base=None) currently builds on the coupled opt-in (ON fp 3ebe7bb6). The v1 default is not in the package yet; until it lands, callers must pass base=one_system(couple_doublet=False) | NUMERIC | mirror5_sha256.txt, on_fingerprints.txt |

### EINF-A SIGNATURE BLOCK (Tue Nov 10 16:31:01 UTC 2026)
**Final files** (NEW only; sha256 in EINF-A_work/new_files_sha256_final.txt; pkg_sha256_final.txt shows 0 existing .py changed):
- layers/einstein.py 622b7f07… (docstrings/WALLS only since 7cd82dc2; dynamics unchanged: ON fp c6996dce… on v1, 3ebe7bb6… on
  the coupled build);
- observe/einstein.py cc2ecb93…;
- tests/test_einstein.py c417d6c6… (17 tests, explicit v1 + coupled bases; 17/17 OK 16:30);
- demos/einstein/bending_shapiro.py 213e4a17…, source_gamma.py 0daf6ad0…, stability.py 0849ec03…, __init__.py 7be1f4c6…;
- NOTES_einstein.md 5c23c1af….
DEFAULT OFF: einstein_system(base) returns base. After the push the base is ONE v1 (77f6d251); the coupled build (593753fa) is
opt-in.

**EINF-A final statement (E5), labelled:**
1. BUILT [THEOREM + NUMERIC]:
   - the harmonic-gauge linearised Einstein layer for all ten components on the ONE cone, dispersion exact on the lattice;
   - in the DeWitt basis (integer, field signs −1 on a3 and h0i; no new gear);
   - L0 reads and sources the full diagonal metric reciprocally;
   - β = 1 for L0 via a one-way static U² read.
2. EXACT [THEOREM + NUMERIC]: the DeWitt identity; the reader factors; dust sources only F (γ = 1 for dust, given the board
   reader); the null-beam source structure; two polarisations on constraint-satisfying data (six in general); the
   constraint-propagation identity.
3. ON THE BOARD [NUMERIC, pre-registered PASS; base-independent]: bending 2.08–2.16× and Shapiro 2.02–2.06× Newton. The excess
   is the predicted O(U) term.
4. IN THE LIMIT / REPORTED [DERIVED + NUMERIC]:
   - □h̄ = −16πG T in the diagonal sector on time average;
   - γ_eff of an L0 lump 0.97–1.00 (zero mode removed);
   - perihelion = GR for L0 + einbeta (EINF-B quadrature; 4/3 without the read);
   - Newtonian limit and redshift unchanged.
5. IMPOSSIBLE [THEOREM]:
   - the gauge-invariant FP operator as the law (B3 / a-read cycle);
   - felt h_0i and any h_ij (i ≠ j) for second-order matter, at any rank;
   - a conserved reciprocal source and an exact Bianchi identity, at any rank;
   - spring / plaquette energy as sources (rank 5);
   - gauge fields gravitating (edge-mode lemma / F-4).
   - The visible doublet at rest: GRAIN wall in v1 (narrow kind, rank 4, 0.197 per unit Higgs); RANK wall (degree 5) in the
     coupled opt-in.
6. MEASURED DEFECT [NUMERIC]: the source is not conserved. Time part 44–82 % of the source per update; space part 0.4–1.9 %.
   So sourced waves carry non-GR polarisations.
7. STABILITY [THEOREM + NUMERIC]:
   - no new degree-1 monomial: the vacuum is as the base, the edge-mode lemma is not triggered, k = 0 and the corner are
     marginal;
   - rewind exact in every run;
   - bounded where the layer acts (L = 6, v1 and coupled, J-pure + L0 lump, 400 updates);
   - two new uncompensated uniform drifts (a2, a3), OPEN like F4;
   - the ghost-sign gears propagate: no ghost-specific growth in EINF-B's Krein test; lattice-k resonances OPEN;
   - the L = 4 runaway belongs to the COUPLED base (v1 bounded 700).
8. VERDICT: the board holds Einstein's LINEARISED equations (harmonic gauge, diagonal sector, dark board L0, non-conserved
   source). It does NOT hold the FULL Einstein equations. The missing parts are theorems at rank 4 (some at any rank), plus
   one grain wall (the doublet in v1).
   - The layer is fit for the push as an OPT-IN, DEFAULT OFF option ("Einstein approximately"), subject to EINF-B's
     signature.
Signed EINF-A Tue Nov 10 16:31:01 UTC 2026

EINF-A post-signature precision (Tue Nov 10 16:33:52 UTC 2026), accepting EINF-B's 16:34 EDIT to A21: "reciprocity, i.e. Newton III, of every new
coupling" reads "of every new RECIPROCAL coupling (einL0, 4,032 terms); the β read (einbeta, 1,296 terms) is designated
one-way". My signature item 1 already makes this split. Nothing else changes.

### EINF-B block 2 — SIGNATURE (appended Tue Nov 10 16:35:57 UTC 2026; append-only)
**Marks on EINF-A's later rows**

| # | EINF-B mark | reason / evidence |
|---|---|---|
| A-add.3 (i), revised wording | **ACCEPT** | Matches the package and the manager (16:31). TODAY layers/one.py is unchanged (57de300d…), one_system() returns 593753fa, and einstein_system(base=None) builds on the coupled build (ON 3ebe7bb6). ONE-SWITCH's patch (s33/) lands at the final delta (~17:50) |
| A-V1R-a | **ACCEPT, reproduced** | my re-run (mirror5, reruns/T8v1_L6_jpure_l0_B.json, A_l0 = 2^12) is IDENTICAL. Bounded at 25 bits ON and OFF; rewind exact for both; the layer acts (max \|a\| 0 → 6,587); U at t = 400: a1 2.7e-4, a2 1.18e-3, a3 2.97e-3, against F 0.0427 (OFF 0.0427) |
| A-V1R-b | **ACCEPT, reproduced** (as A-V1R-c) | my re-run (mirror5, reruns/T8v1_L4_jpure_B.json) is IDENTICAL: v1 + Einstein (ON fp c6996dce) and v1 OFF (77f6d251) bounded at max 29 bits over 700 updates (25 → 29), ON ≡ OFF, L0 dark, rewind exact. So the L = 4 runaway at t = 666 belongs to the COUPLED build only |
| R-A1/A6/A4, R-A8, R-A10, R-A20/A21 | ACCEPT | my EDITs, correctly adopted (NOTES_einstein.md updated) |
| A9b | **ACCEPT, reproduced** | my T4b re-run is bit-identical (reruns/T4b_source_gamma_k_B.json) |
| A25 | ACCEPT (cited; coupled, not re-run by me) | consistent with my L = 4 re-runs: L0 stays exactly 0 under the ONE bangs, so the layer is idle |
| A26/A27 | ACCEPT (coupled; not re-run by me) | the v1 analogue A-V1R-a is re-run by me (above); consistent with B5: the long-run limit is the base's F4 |
| A21 precision | **EDIT, adopted** (EINF-A post-signature line, 16:34) | "Newton III of every new coupling" → "of every new RECIPROCAL coupling (einL0, 4,032 terms); the β read (einbeta, 1,296 terms) is designated one-way" |
| R-B14 | ACCEPT | labelled DERIVED, not run. It is a BOARD prediction that DIFFERS from GR (parallel beams attract) |

**Every result on BOTH bases**
After the final push the package default is ONE v1 (77f6d251); the coupled build (593753fa) is an explicit opt-in. The Einstein
layer stays DEFAULT OFF on both.

| item | v1 (77f6d251; default after the push) | coupled (593753fa; opt-in) |
|---|---|---|
| law audit (rank 4, B3, stages 3, reciprocity 0 violations, signs −1 on {a3, h0i}, 0 metric–metric bilinears, OFF ≡ base, ON minus new ≡ base) | PASS; ON fp c6996dce… (confirmed on the final einstein.py 622b7f07, mirror6 16:35) | PASS; ON fp 3ebe7bb6… (same) |
| new terms | 5,328, degree 2: 4,032 reciprocal + 1,296 designated (β read) | same |
| tests/test_einstein.py (explicit bases) | 17/17 OK (mirror5; mirror6 = the final files, 16:35) | 17/17 OK (same runs) |
| T5 bending/Shapiro 2×, T4/T9/T4b γ_eff and defect, Krein test of record | base-INDEPENDENT (reduced systems); bit-identical re-runs | same |
| stability, ONE seed | L = 4 J-pure, 700 updates: bounded 29 bits, ON ≡ OFF, rewind exact. L = 6 J-pure + L0 lump (2^12), 400 updates: bounded 25 bits = OFF, the layer acts, a-drifts ∝ t². Both re-runs are bit-identical to EINF-A's | L = 4 J-pure: the BASE runs away at t = 666 (bits 374), ON ≡ OFF, L0 dark: reproduced. L = 6: EINF-A's runs, not re-run by me |
| visible doublet | GRAIN wall: covariant F × Yukawa is rank 4 (narrow kind) but 0.197 per unit Higgs | RANK wall: Θ × F × H × ψψ is degree 5 (census reproduced) |

**Final file integrity** (Tue Nov 10 16:33:54 UTC 2026; final_sha256.txt vs my baseline 15:44:41): only the 8 NEW files, with sha256 prefixes = EINF-A's final list (einstein.py 622b7f07, observe cc2ecb93, tests c417d6c6, bending 213e4a17, source_gamma 0daf6ad0, stability 0849ec03, __init__ 7be1f4c6, NOTES 5c23c1af). 0 existing files changed; the 7 ONE files are unchanged (layers/one.py 57de300d). The 622b7f07 diff vs ff6e2079 is docstring-only

**Two findings for the final documents** (as the manager asked, 16:31):
- (i) The base's uniform lapse (k = 0, F4) and the U > ¼ flip limit ANY run with L0 matter, with or without the Einstein layer.
  In krein_comp (L = 6, A = 2^14, mean sources cancelled), the base WITHOUT the layer fails first (OFF t = 180, CTL 487, ON 589).
  The difference is 99.8 % k = 0 before a nonlinear explosion. The layer adds two more uncompensated uniform modes (a2, a3).
  [NUMERIC + OPEN]
- (ii) Board prediction, DIFFERENT from GR: with h̄_0i walled off (A14), two parallel co-moving light beams ATTRACT on the board
  (exchange 2EE′). GR gives 0 (Tolman–Ehrenfest–Podolsky); antiparallel beams get 2EE′ on the board against GR's 4EE′. [DERIVED,
  not run]

**Plain verdict (E5)**
- The board now carries linearised Einstein in HARMONIC GAUGE for all ten metric components on the one cone. It is exact as
  integer identities: dispersion, reader factors, reciprocity, constraint-propagation identity.
  - It agrees with GR for constraint-satisfying data and a conserved source.
  - Neither is guaranteed: the constraint is not imposed (T7), and the reciprocal source is not conserved (G-NOGO-a; the defect is
    O(1) per update).
  - So sourced waves carry up to 6 polarisations (2 in GR).
- Coupling: diagonal sector, dark L0 only, reciprocal.
- What holds, and how:
  - γ = 1 for dust (DERIVED given the board reader; the same number as before);
  - GR-like and isotropic response to stress, through the DeWitt ghost signs;
  - bending and Shapiro 2× on the board, with the predicted U² excess;
  - β = 1 for static fields, through a one-way read (perihelion 1 × GR with it, 4/3 without).
- Walls (THEOREM): conserved reciprocal source; exact Bianchi / Hamiltonian constraint; felt gravitomagnetism and off-diagonal
  stress for second-order fields; springs and plaquettes as sources (rank 5). The visible doublet is a rank wall (coupled) or a
  grain wall (v1).
- The ghost-sign gears propagate. No ghost-specific instability was seen; the binding long-run limit is the base's uniform lapse.
- The FULL Einstein equations do NOT hold on the board at rank 4.

**OPEN, with proposals (s28/EINF-B_PROPOSAL.md)**: K-2 (Krein at lattice k), M-1 (monopole radiation at 2w0), P-1 (polarisation
content of sourced waves), B-1 (beam–beam test), D-1/D-2 (drift law; period-averaged defect).

**SIGNED: EINF-B (independent verifier), Tue Nov 10 16:35:57 UTC 2026.**
ACCEPT EINF-A's build as a DEFAULT-OFF research layer, with all edits adopted. Every EINF-A claim row is ACCEPT or ACCEPT + EDIT;
there is no DISAGREE. Nothing faked: every number above was re-run or derived by me in my own mirrors / scripts under
s28/EINF-B_work/.
