# NOTES_einstein — Study 28: the full linearised Einstein layer on the board (rank 4), builder EINF-A
Builder EINF-A, Tue Nov 10 2026 (UTC). Verifier EINF-B (append-only marks in scratchpad s28/AGREE_EINF.md).
Pre-registration: scratchpad s28/EINF-A_NOTES.md §1–§2 (15:46:07 UTC, before any code). Evidence: s28/EINF-A_work/
(runs/*.json, grain_doublet.json). All runs in a scratch mirror, nice 19, one core.
BASE (owner decision ~16:13 UTC, manager 16:25 / 16:31): matter must NOT read the cosmic clock. AFTER THE PUSH the default is
ONE v1 (couple_doublet=False, fp 77f6d251), and the coupled build (593753fa) is an explicit opt-in. ONE-SWITCH's patch of
layers/one.py is installed at the final delta (~17:50 UTC). Until then one_system() returns 593753fa.
- einstein_system(base=None) builds on whatever one_system() returns. ON fingerprints: c6996dce… on v1, 3ebe7bb6… on the coupled
  build.
- The layer is DEFAULT OFF on both bases, and every result here is stated for both. The tests use EXPLICIT bases (v1 first, coupled second). The board runs T5 / T4 / T9 use reduced
systems with no ONE block, so they are base-independent. Labels: THEOREM / DERIVED / NUMERIC /
CHOSEN / NEW LAW / OPEN / IMPOSSIBLE (= a theorem wall). NEW files only: layers/einstein.py, observe/einstein.py,
tests/test_einstein.py, demos/einstein/, this file. DEFAULT OFF: `einstein_system(base)` returns `base` unchanged.

## 0. The answer in six lines
1. The board law is the HARMONIC-GAUGE (de Donder) form of linearised Einstein: ten waves on the ONE cone with the board's
   exact lattice dispersion. The gauge-invariant Fierz–Pauli operator is not buildable: it needs edge offsets (B3) and a-read
   cycles.
   Its kinetic form is the indefinite DeWitt metric (6+, 4−). Rule3's kinetic term is D·1, so an integer way to carry it is
   an integer basis with equal weights plus the documented field signs (several such bases exist; Sylvester fixes only the
   inertia). The 9 idle metric gears get these jobs, with
   no new gear. [THEOREM (exact algebra) + NUMERIC]
2. With that basis and the board form of (1/2)·h_μν·T^μν (metric × one-time potential; the board form is CHOSEN), γ = 1 for dust
   follows: dust (T^ij = 0) sources only metric.h00, so h_dd = h_00. Inside that form the link factor is no longer a free
   parameter (the 1911 value is excluded). What is NEW is that h_dd is a field sourced by the stress, and the DeWitt signs make
   stressed sources GR-like ((ρ − p)/(ρ + 3p)) and isotropic. [THEOREM + NUMERIC]
3. Built and reciprocal (Newton III): L0 (the dark board) now feels and sources the full diagonal metric (h_00, h_xx, h_yy,
   h_zz). On the board, light (test light) bends 2× Newton and its Shapiro delay is 2× the lapse-only control.
   [NUMERIC, pre-registered PASS]
4. Not buildable at rank 4, by theorem (any rank where marked):
   - h_ij (i ≠ j) and h_0i for second-order matter: B3 (any rank), and two-time / a-read cycle (any rank);
   - the visible Dirac doublet's covariant lapse dressing: in the default ONE v1 it is rank 4 (narrow kind) but below the
     integer grain (0.197 per unit Higgs); in the coupled opt-in it is rank 5;
   - the OD4 spring energy as a source: rank 5;
   - an exactly conserved reciprocal source and an exact Bianchi identity: G-NOGO-a, any rank.
   [THEOREM]
5. Second order: β = 1 for L0 via the existing G = F²/(2P) gear (rank 3, designated). The 00-part of the 3-graviton vertex is
   the existing G source −k·Lap(F²) (one-way). Perihelion: DERIVED (2 + 2γ − β)/3 = 1, NOT a board orbit. [DERIVED]
6. So the board holds the linearised Einstein equations:
   - in their diagonal sector, for L0, reciprocally;
   - with the source not conserved (quantified);
   - with γ = 1 for dust derived (given the board reader), β via a designated read.
   It does NOT hold them fully: no gravitomagnetism for second-order matter, no off-diagonal stress, and the visible doublet
   is not coupled. [summary]

## 1. The DeWitt basis (layers/einstein.py)
Stored gears (scale P = 2^20, U = F/(2P)), each on THE ONE headroom stencil u = (Q−1)·Σ6 b + 6b, documented field sign s:

| gear | stores | s | role |
|---|---|---|---|
| metric.h00 (= F) | P·h_00 = P·(h̄_00 + h̄_kk)/2 | +1 | THE lapse; unchanged; it already was this combination |
| metric.a1 (was hxx) | P·(h̄_xx − h̄_yy)/2 | +1 | anisotropic stress |
| metric.a2 (was hyy) | P·h̄_zz | +1 | |
| metric.a3 (was hzz) | P·(h̄_xx + h̄_yy + 2h̄_zz)/2 | −1 | conformal-type combination (DeWitt −) |
| metric.h0i | P·h̄_0i | −1 | shift (DeWitt −); unsourced (wall) |
| metric.hij | P·h̄_ij | +1 | off-diagonal; unsourced (wall) |

- 2q(h̄) = (4/P²)·(F² + a1² + a2² − a3² − Σh0i² + Σhij²), with q = h̄·h̄ − h̄²/2 (η = diag(−1, 1, 1, 1)). Exact on
  200 random integer points; signature (6, 4). [THEOREM; NUMERIC observe.einstein.dewitt_check]
- Back-map: P·h_00 = F, P·h_xx = F + a1 − a3, P·h_yy = F − a1 − a3, P·h_zz = F + 2a2 − 2a3, P·h_0i = h0i, P·h_ij = hij.
  h = TR(h̄) holds exactly. [THEOREM]
- The free part is u-identical to the package's metric block: replacing only that block keeps each base's dynamics fingerprint
  (v1 77f6d251; coupled 593753fa). [NUMERIC test T1c]
- Several exact rational bases exist; Sylvester fixes only the inertia (6+, 4−). This one keeps the package's lapse metric.h00 as a
  gear.
- z is singled out. With the lapse kept as a gear, the rest of the diagonal sector has DeWitt form 2(Σh̄_dd² − S²), S = Σh̄_kk,
  of signature (2+, 1−), so no permuted trio of equal-sign gears completes it.
- A cubic-symmetric integer basis exists only if the lapse is NOT a gear: 4q|diag = Σ_d (h̄_00 + 2h̄_dd + S)² − (h̄_00 + 3S)²
  (0 failures in 500 exact checks). It would re-express every existing lapse block.
- The field equations are cubic-symmetric; only the rounding pattern is not. [THEOREM + NUMERIC; corrected 16:23 after
  EINF-B's E-a]

## 2. The reader and the source (E2)
- Board form of (1/2)·h_μν·T^μν: the kinetic term is fixed (D·1), so the metric multiplies the one-time potential:
  Φ_int = h_00·E_site + Σ_d (h_00 + h_dd)|link · E_link,d.
- P·(h_00 + h_dd) = 2F + Δ_d, with Δ_x = a1 − a3, Δ_y = −a1 − a3, Δ_z = 2a2 − 2a3.
- The 2F part IS today's form-C lapse on L0. Its source ∂Φ/∂F = (E_site + Σ_d Ē_d)/P is the GR source of
  h_00 = (h̄_00 + h̄_kk)/2, i.e. the active mass ρ + Σp (Tolman). [DERIVED]
- NEW block einL0 = the Δ part: 4,032 terms, rank 3, reciprocal, coefficients k·w and k·w/2 with k = 2^12. [NUMERIC]
- Exact checks (tests/test_einstein.py):
  - T4b: with uniform F, a1, a2, a3, L0's input at k = π·e_d is EXACTLY D·v − (Q−1)·[(1 − F/P)·M0 + (1 − (2F + Δ_d)/P)·T_d]·v.
  - T4a: a uniform (k = 0) L0 state sources only F; the inputs of a1, a2, a3 are exactly 0.
  - T4c: the test light's link factor is 1 − (2F + Δ_d)/P (full) or 1 − F/P (control), exactly.
  [NUMERIC, exact integers]
- Static field equations, from these sources [DERIVED]:
  - h̄_dd ∝ Ē_d (diagonal stress);
  - h̄_00 ∝ 2E_site + ΣĒ_d, i.e. 2·E_pot, which equals ⟨T^00⟩ by the virial average;
  - so □h̄_μν ∝ ⟨T_μν⟩ in the diagonal sector, with one normalisation.
- γ_eff = h_dd/h_00 = 1 + Δ_d/F = (E_site + Ē)/(E_site + 3Ē) for an isotropic source. This is GR's (ρ − p)/(ρ + 3p) under
  ρ ↔ 2E_site + 3Ē, p ↔ Ē. [DERIVED]
  - Board run (T4): see §5.
- Universality (who feels and sources what):

| reader | h_00 | h_dd (a1, a2, a3) | h_0i | h_ij (i ≠ j) |
|---|---|---|---|---|
| L0 | built (form C, today) | **built (einL0)** | IMPOSSIBLE (two-time) | IMPOSSIBLE (B3) |
| test light (demos only) | built | built | IMPOSSIBLE | IMPOSSIBLE |
| E1 photon | not built | not built | — | — |
| visible Dirac doublet | singlet-half hop only (FIX-i) | wall | wall | wall |
| gauge layers su2/su3/u1, cosmic block | no | no | no | no |

  - E1 photon: possible like the test light, but exact E1 Gauss is then lost (UNIV T5 THEOREM). This is an owner choice.
  - Doublet: see §4(a).

## 3. Second order (E3)
- β for L0 (block einbeta, 1,296 designated terms, rank 3; STATIC fields only, because G = F²/(2P) is a static law):
  - L0 reads beta.G (G = F²/(2P), GRAV-FIX A) as +G/P on M0 and +(17/8)·(G_x + G_y)/P on T.
  - −g00 = 1 − 2U + 2U², so PPN β = 1. [DERIVED]
  - Why designated: a reciprocal partner would source G with matter energy at first order.
  - The reciprocal rank-4 quartic F² × L0 needs (Q−1)/(4P²) ∈ Z, which is grain-blocked at P = 2^20. [DERIVED]
- The 3-graviton vertex is PARTIAL:
  - Its static 00-part, the gravitational field energy sourcing the second-order potential (∇²(U²) = 2(∇U)² outside matter),
    is exactly the existing G source −(w_G/(2P))·Lap(F²): rank 3, one-way. [DERIVED]
  - Its reciprocal completion (F back-reaction) is exact but dynamically unstable with the ONE stencil (finding F1). [NUMERIC, GRAV]
  - The one-time, one-axis parts h × (Δ_d h)² for the other components ("the graviton feels gravity") are rank-3 legal but
    NOT built. The reason: the ONE headroom stencil has headroom 1/(3Q), so wherever h_00 + h_dd < 0 the metric's own corner
    mode would leave the band (CFL; package findings F1/F2), and the closed board's uniform lapse drifts negative in the live
    default (STAB R11). It would need a stencil with headroom (an owner choice). [DERIVED + OPEN]
  - The mixed-direction parts (∂_i h ∂_j h, i ≠ j) are IMPOSSIBLE (B3). The time-derivative parts are IMPOSSIBLE as reciprocal
    terms (two-time). [THEOREM]
- Perihelion: (2 + 2γ − β)/3 = 1 with γ = 1 (dust, exact) and β = 1 (L0 read). [DERIVED]
  - No board orbit was run: an L0 packet has lattice-scale dispersion and no bound orbit is feasible this hour. [OPEN]

## 4. Walls (each with its reason)
(a) **Visible Dirac doublet at rest (FIX-i): it can neither feel nor source the lapse at rank ≤ 4.**
   [GRAIN wall in ONE v1 (the default after the push); RANK wall (degree 5) in the coupled opt-in. NUMERIC census:
   s28/EINF-A_work/grain_doublet.json]
   - ONE v1, the default after the push:
     - the SU(2)-covariant dressing F × (Yukawa composite) = F·Φ·ψψ is rank 4 and of the APPROVED narrow kind (uncharged
       singlet × covariant rank-3 composite);
     - but it is grain-blocked: 412,864/(2P) = 6451/2^15 ≈ 0.197 per unit Higgs, and integrality would need v | 2·6451
       (a Higgs vev of 1 or 2 units);
     - the integral rank-3 bare-mass dressing ((m + 6w)/(2P) = 12,902) breaks SU(2) at O(U);
     - the doublet keeps only the FIX-i singlet-half hop read (768 terms).
   - Coupled opt-in (593753fa): the doublet's whole first-order potential carries the hand Θ (mass entries Θ × ψ, coefficient
     422,772,736; Yukawa entries Θ × H × ψ, coefficient 6,451; the mass is the Higgs imprint, mass = 2yv).
     - So the SU(2)-covariant lapse dressing F × Θ × Φ × ψψ has degree 5 = rank 5: FORBIDDEN (O1).
     - The only rank-4 candidate, F × Θ × (bare mass)·ψψ, is not SU(2)-covariant: it breaks SU(2) at O(U) (HL-1, the reason
       compose_electroweak removes mlapse). It is also non-integral (422,772,736/(2P) = 6451/32).
   - Both bases: the vev-response route (L2(b)) triggers the edge-mode lemma (s18). Hence FIX-i, and the EP debt stays.
(b) h_ij (i ≠ j) for any second-order field: ∂_iφ∂_jφ needs offsets +e_i and +e_j in one monomial, i.e. three nodes. B3
    rejects it (observe.einstein.b3_offdiagonal_wall). [THEOREM, any rank]
(c) h_0i for second-order matter:
    - FEELING it is impossible: the matter's read of h_0i × φ̇ would close a cycle of a-reads, and Rule3 has no staged inverse
      then (observe.einstein.two_time_cycle_wall). [THEOREM, any rank]
    - No b-only (reciprocal) source exists: the momentum density φ̇∂_iφ is two-time. [THEOREM]
    - A DESIGNATED one-way two-time source of h_0i is legal and simply NOT built. [CHOSEN]
    So no gravitomagnetism is felt and there is no frame dragging for second-order matter.
(d) F-4: the OD4 spring energy as a source is F × |x|⁴, degree 5. Light on plaquette links (route B): rank 5. [THEOREM, s23 AGREE_R5]
(e) No exactly conserved reciprocal source (G-NOGO-a), no exact Bianchi identity, no exact Hamiltonian constraint (CL2 row 5).
    [THEOREM, any rank]

## 5. Results (pre-registered T1–T9; NUMERIC unless stated)
- T1 LAW PASS (tests/test_einstein.py, 17/17 OK; T4d null beam and T4e exact beta read added 16:08 / 16:17):
  - rank 4; reciprocity 0 violations (13,098 b-only monomials checked);
  - the field signs −1 sit exactly on a3, h0x, h0y, h0z;
  - OFF ≡ the GIVEN base (v1 77f6d251; coupled 593753fa); the metric copy alone ≡ each base's dynamics; both ON tensors have
    rank 4 and 0 reciprocity violations (ON fp c6996dce… on v1, 3ebe7bb6… on the coupled build);
  - vacuum fixed 10 updates (L = 3, 4); ONE seed rewind exact (L = 3, 12 updates): on both bases.
- T2 ONE CONE PASS: all ten gears have on-site 6 and faces Q − 1. The symbol identity is exact. A board plane wave turns by
  the exact w(k) (|Δw| < 1e-6 per update). [NUMERIC + THEOREM]
- T3 POLARISATIONS PASS (exact algebra, sympy):
  - in lattice momenta K = 2·sin(k/2), the board's exact dispersion is K_0² = c²·|K|² (null);
  - the constraint has rank 4 and the gauge directions rank 4; the Riemann rank on the constraint surface is 2;
  - this holds at K = (3,4,0), (1,2,2), (2,3,6).
  So two polarisations, on the ONE cone. [THEOREM + NUMERIC]
  - The board does NOT enforce the harmonic constraint. Each stored gear obeys Box g = 2 s_g + (r − r′) EXACTLY, so
    Box C^ν = 2 D_μ s^μν + ledger. Radiation from the non-conserved board source (T9) therefore carries non-TT parts in
    proportion to the defect. The two-polarisation count holds on constraint-satisfying data. [THEOREM (linear identity) + DERIVED]
  - SOURCED: L0 couples only to the diagonal sector. Along a lattice axis it radiates h+ (a1 = P·(h̄_xx − h̄_yy)/2) and never h×
    (h_xy is unsourced, wall (b)). [THEOREM, tensor census T2a]
- T5 BENDING + SHAPIRO PASS (demos/einstein/bending_shapiro.py; runs/T5_bending_shapiro.json; L = 56; the field is built by
  the board from a static dust load, F_min ≥ 0; a1 = a2 = a3 = 0 exactly; rewind 100 exact):
  - delay ratio full/control 2.056, 2.060, 2.055, 2.025 at b = 2, 4, 6, 8 (window [1.8, 2.2]);
  - delay-slope (bending) ratio 2.08 (b 2–6), 2.16 (b 4–8) (window [1.7, 2.3]);
  - the no-read light is bit-identical;
  - U(4) = 0.027.
  - The excess over 2 is the predicted O(U) term of the built factors (n_full = (1 − 4U)^−½, n_ctl = (1 − 2U)^−½): delay ratio
    ≈ 2(1 + 1.5U), slope ratio ≈ 2(1 + 3U). EINF-B's straight-ray eikonal on the measured profile gives 2.086 / 2.058 /
    2.047 / 2.040. [DERIVED + NUMERIC]
  - Beyond b = 10 the ratio falls to 1.95 – 1.85 (b = 10 – 13), then oscillates (EINF-B: 2.13 at b = 18, 1.95 at b = 24).
    This is plausibly wave-optics / caustic structure. [OPEN]
  - Scope: one-way test lights and a MECHANISM dust load. No light of the ONE content reads the metric (E1 not coupled).
- T6 REDSHIFT: rest clocks read h_00 only, and einL0 has no on-site term (T4b exact). So the redshift is the package's (P1 D1
  PASS). [DERIVED]
- T4 γ_eff of a real board source (L0 lump, reciprocal; L = 20, 60 updates; runs/T4_T9_source_gamma.json and
  T4b_source_gamma_k.json):
  - raw h_dd/h_00 at r = 3..7: 1.016 / 1.005 / 1.001 (x / y / z). This is dominated by the closed-board zero-mode drift
    (U_mean = 0.17, F4).
  - with the uniform modes removed: 0.97 – 1.00, roughly isotropic, slightly below 1 (the GR sign for positive effective
    pressure).
  - control without einL0: exactly 1.
  - L0's link energy is indefinite (signed ports), so its stress has no fixed sign. [NUMERIC, report only]
- T9 conservation defect (same run): max |D_μ s^μν| / max |s| per update [NUMERIC + THEOREM]:
  - time part 0.44 – 0.82; the control gives the same, 0.39 – 0.80. Since s^0i ≡ 0 this is |Δ_t s^00| alone. It mixes the
    G-NOGO-a 2w swing of the one-time source with the missing momentum flux of the dispersing lump. A period-averaged defect
    would separate them (not done);
  - space part 0.004 – 0.019 with einL0 (diagonal stress, no T^0j to balance it); 0 in the control;
  - the h0i and hij sources are exactly 0.
- T8 STABILITY:
  - exact: no new monomial of degree 1, so the vacuum linearisation is unchanged (test T1d) and the edge-mode lemma is not
    triggered; k = 0 and the corner are as in the base (marginal). [THEOREM + NUMERIC]
  - J-pure ONE seed: L0 stays exactly dark, so the layer is idle and the run is bit-identical to the base.
  - At L = 4 the COUPLED base (593753fa) runs away at t = 666 (bits 29 → 374); the rewind is exact. On the v1 base (77f6d251)
    the same seed is BOUNDED for 700 updates (29 bits; ON = OFF) with an exact rewind. So the runaway belongs to the coupled
    build (now rejected by the owner), not to v1 and not to this layer. Manager informed 16:02 and 16:29; ONE-LONG is
    diagnosing. [NUMERIC, runs/T8_stability_L4.json, T8v1_L4_jpure.json]
  - L = 6 (design regime) [NUMERIC]:
    - ONE S2* seed, 600 updates: bounded (27 bits), rewind exact, bit-identical to OFF. L0 stays exactly dark under BOTH ONE
      bangs, so the layer is idle there.
    - J-pure ONE seed + an L0 lump (seed data, A = 2^12), 400 updates, ON vs OFF: bounded (24 bits, as OFF), rewind exact.
      The layer acts (max |a| → 6,330).
    - The a's uniform modes drift ∝ t² (a3: U = 3e-3 at t = 400, against F's 0.042 F4 drift, identical OFF): about 4 % of the
      link reading. Long-run fate: OPEN, as for F (F reaches U = 1/4 near t ~ 1,000 with this lump: the base's F4).
  - Base v1 (77f6d251), same J-pure + L0 lump run: bounded 400 (25 bits, as OFF), rewind exact, max |a| → 6,587. The a's
    drift as above (within 1 % of the coupled-base run). [NUMERIC, runs/T8v1_L6_jpure_l0.json]
  - Two NEW F4-type uniform modes (a2, a3) with NO bgk-type compensation. With L0 matter they push the link factor
    1 − (2F + Δ)/P toward 0, alongside F. [NUMERIC + OPEN]
  - The ghost-sign gears PROPAGATE: no constraint removes them on the board.
  - Structural risk (EINF-B's Krein lemma, refined): the DeWitt metric is indefinite, and a3 (s = −1) is a ghost-sign wave
    reciprocally coupled to L0's stress.
    - There is no direct metric–metric bilinear.
    - The matter-mediated static mixing is semidefinite at low k (all L0 bands above the cone), so it gives no complex
      eigenvalues there.
    - Growth would need an indefinite mixing at lattice-scale k, or a difference resonance with the background oscillation.
    - A direct test with an L0 lump is masked by the base's F4 drift: einL0 and the plain control both blow up at L = 6
      (A = 2^16, t ≈ 45–60) after the uniform U passes 1/4.
    - The test of record is EINF-B's krein_comp.py (uniform modes cancelled; sign-flipped control). Its result (EINF-B B5): NO
      ghost-specific growth. The perturbed copy blows up first through the base's uniform lapse (F4) in all variants: OFF at
      t = 180, sign-flipped control at 487, ON as built at 589. Krein at lattice k and difference resonances: OPEN.
  - The layer is IDLE (exactly) on every state with L0 = 0 and a1 = a2 = a3 = 0. [THEOREM]

## 6. E5 — the plain owner verdict (each claim labelled)
**What the owner asked:** the FULL Einstein equations on the board, rank 4 final, nothing faked, posted or circular.

**What is now on the board** (built, exact integers, reciprocal unless marked, DEFAULT OFF until EINF-B signs):
1. All ten metric components carry Einstein's linearised equations in harmonic gauge, in an integer form Rule3 allows: the
   indefinite DeWitt metric with field signs. No new channel was added: the nine idle metric gears got their jobs.
   [THEOREM + NUMERIC]
2. Gravitational waves: all ten components run on the ONE cone, with the dispersion EXACT on the lattice. On data that satisfy
   the harmonic constraint there are exactly two polarisations. In general there are six: the board does not impose the
   constraint. [THEOREM]
3. The dark board L0 feels and sources the whole diagonal metric (time part and the three space parts). Action = reaction
   exactly. [NUMERIC]
4. γ = 1 for dust follows from the field equation, given the board form of the reader (a chosen form of ½hT):
   - matter without stress sources only the lapse, so the space part equals the time part;
   - the link factor is no longer a free parameter;
   - the DeWitt signs make stressed sources GR-like and isotropic.
   [DERIVED given the board reader]
5. On the board, with the field built by the board itself:
   - light bends twice the Newtonian value (2.08 – 2.16);
   - light is delayed twice the Newtonian value (Shapiro 2.02 – 2.06).
   [NUMERIC, pre-registered PASS; a test light on the ONE cone; the E1 photon itself does not read the metric (owner choice:
   exact Gauss)]
6. Second order: β = 1 for L0 clocks through the existing U² gear (one-way). The perihelion advance then has the GR value as
   a derived consequence; it was not run as a board orbit. [DERIVED]

**Only in the limit:**
7. The field equation □h̄ = −16πG T holds in its diagonal sector on time average (virial). The Newtonian limit and the
   redshift are the package's (unchanged). [DERIVED]

**Impossible, by theorem:**
8. The visible matter (the Dirac doublet) at rest cannot feel or source the lapse at rank ≤ 4.
   - In the default ONE v1 the covariant term is rank 4, of the approved narrow kind, but its coefficient is below the integer
     grain (0.197 per unit Higgs).
   - In the coupled opt-in it is rank 5.
   [grain wall (v1) / THEOREM (coupled)]
9. For any second-order field (L0, light), at ANY rank:
   - no gravitomagnetism can be FELT (h_0i: a-read cycle); a one-way source-only h_0i is legal but not built (CHOSEN);
   - no off-diagonal stress (h_ij: B3).
   [THEOREM]
10. No exactly conserved source and no exact Bianchi identity, at ANY rank. So the harmonic constraint is not kept, and the
    radiation carries extra polarisations in proportion to the source's non-conservation (measured: ~50 % of the source per
    update for the time part, ~1 % for the space part). [THEOREM + NUMERIC]

**A falsifiable lattice signature (EINF-B B14, DERIVED, not run):** with h̄_0x walled off, parallel light beams ATTRACT on the
board (exchange 2EE′). In GR they do not (0 for parallel, 4EE′ for antiparallel beams: Tolman–Ehrenfest–Podolsky).

**Also stated:**
- Universality is L0 only: the visible doublet, E1, the gauge fields, the Higgs and the cosmic block are uncoupled to the new
  components.
- The layer adds two uncompensated uniform drifts (a2, a3).
- The ghost-sign gears propagate. EINF-B's Krein test found no ghost-specific growth; lattice-k resonances stay OPEN.
- The layer is DEFAULT OFF. It is tested on both bases (v1 after the push; the coupled opt-in).

**One sentence.** The board now holds Einstein's LINEARISED equations in harmonic gauge, in their diagonal sector, for the dark
board: γ = 1 for dust follows from the field equation (given the board reader), light bends and is delayed 2×, two
polarisations on constraint-satisfying data on the one cone, and β = 1 via a one-way U² read. It does NOT hold the FULL Einstein
equations, and at rank 4 it cannot:
- felt gravitomagnetism, off-diagonal stress, a conserved source and an exact Bianchi identity are impossible at any rank;
- the visible matter's coupling is below the integer grain in v1 and needs rank 5 in the coupled opt-in.
[DERIVED summary]
