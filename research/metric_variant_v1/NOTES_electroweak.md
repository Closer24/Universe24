# NOTES_electroweak — EW-BUILDER (HAND-M1): L1–L3 as extensions of the chiral block (written DEFAULT-OFF; L2b/L3 now ON in the package default)

All stamps `date -u`. NEW FILES ONLY: layers/electroweak.py, tests/test_electroweak.py, results/electroweak/, this file.
No existing package file is modified (layers/chiral.py included); core/, universe24/ untouched; no git. Every piece
is active only with the chiral block (itself DEFAULT OFF when written). Input claims: HL-1 Study 9 interim (12:22; not
yet agreed).
STATUS UPDATE (DOC-UPDATER, Tue Nov 10 15:41 UTC 2026, doc only):
- Since owner decision 5 (13:09 UTC; RC2 batch 3, 13:17 UTC), `layers.system.default_system()` composes L3 (Higgs hop)
  and L2(b) (graviweak, gwb) by default (`chiral=True, electroweak=True`).
- L2(b) is built at FIX-i (owner decision v8-1, 14:37 UTC): `gwb_lam_H = gwb_lam_L = 0`, so only the singlet-half hop
  is kept. The lam_H = lam_L = 4 form described below was linearly unstable (s18/AGREE_STAB.md). It is now a contrast
  only (`gwb_lam_H=None, gwb_lam_L=4`), and its "lapse x |Phi|^2" EP results are not the default's: EP for the doublet
  is OPEN.
- The module constant `EW_DEFAULT_ON = False` is unchanged. It is only the default of `compose_electroweak(on=...)`,
  which the package default calls with `on=True`.
- L1 (local hypercharge) is not built here. Route B (NOTES_electroweak_b.md) is opt-in, OFF.
- Current defaults: README_v1_draft.md sections 0 and 7c. The text below is the 12:3x-12:4x record.

## Design (Tue Nov 10 12:31:48 UTC 2026, before any run): see the docstring of layers/electroweak.py
- L3 Higgs hop: kH <Φ(x), U Φ(x+e)> − (cΦ/2)|Φ|² − (cW/2)|U|², cΦ = 6 kH A, cW = kH v²/A; default kH = 2^10
  (cW = 2^26, predicted d(cos w_W) = −cW/D = −1.30e−3 at the v2 Q, v = A = 2^16).
- L2(b) graviweak: (cF/2) F (|Φ|² − v²), cF = −lam_H v²/P; (cL/2)(F_x + F_y)(|U|² − A²), cL = −lam_L A²/P;
  −(F_x + F_y)/(2P) × (hop/2) b′ᵀ P_d Π_S b (singlet half). P = 2^20 → cF = cL = −2^14. Replaces mlapse/mbeta for the
  doublet in compose_electroweak (the default lapse dresses the bare mass = SU(2)-breaking).
- L1 hypercharge: analysis + exact algebra (generators L3, R3, BL, Q in hypercharge_generators()).

## PRE-REGISTRATION (Tue Nov 10 12:31:48 UTC 2026; tests/test_electroweak.py implements them; L = 3 unless stated)
Systems: EW-ALONE = compose(matter, matter2, wsu2, chiral, ehop); GW-ALONE = EW-ALONE + test lapse field F (marginal
node gear) + gwb (reciprocal); EP = EW-ALONE + F + gwb(oneway, MECHANISM) with a prescribed static uniform F0.
- EW1 (L3 exactness): reciprocity ok, 0 designated; rank ≤ 4 with rank-4 = OD4 springs only; B3 (compose); vacuum fixed
  20/20; rewind T = 6 exact; local SU(2) Noether/Gauss 0 failures (T = 6, random state incl. excited links/2-paths).
- EW2 (W gap, L3): uniform small W_i on the x-links (δ = 64), T = 512 exact updates, dominant frequency of the mean
  W_i(t) by FFT, for kH ∈ {0, 2^10, 2^12} at v = 2^16 and kH = 2^12 at v = 2^15. PREDICTION: (1 − cos w)(kH) −
  (1 − cos w)(0) = kH v²/(A D) within 10 %; scaling w ∝ v sqrt(kH) (continuum m_W ∝ g v).
- EW3 (L2b exactness): GW-ALONE reciprocity ok with 0 designated; rank ≤ 4; vacuum fixed 20/20; rewind T = 6; local SU(2)
  Noether 0 failures with F excited (random F, |F| ≤ 2^10).
- EW3b (EP, MECHANISM): static uniform F0 with U = F0/(2P) ∈ {2^−8, 2^−6}; Higgs prepared at its shifted equilibrium
  (integer |Φ| = isqrt(v² + cF F0/lam_H)), links at isqrt(A² + 2 cL F0/lam_L). Measure the effective mass entry m_eff of
  a uniform W0-eigen matter state (engine input, exact) and compare with m(1 − U): PREDICTION m_eff/m = sqrt(1 − 2U) =
  1 − U − U²/2 + … (EP to O(U²); rounding of |Φ| adds O(1/v)). Dynamic: Higgs started at v (not relaxed): report the
  oscillation amplitude of |Φ| − v_eff over T = 64 (non-adiabatic clock modulation; no damping in a reversible law).
- EW4 (L1 algebra, exact): on EW-ALONE with a random state: ⟨∇Ψ_phys, X B⟩ = 0 for L3 at every node (local) and for
  R3, BL, Q summed over the board (global); X_Q annihilates the vev. EXPECTED (THEOREM-level, Study 4 A1): Y = R3 + BL/2
  acts on the second-order Higgs and Q on the W links, so E1 (A0 coupling needs a first-order carrier) cannot gauge Y
  exactly: E1 → hypercharge is NOT built; compact U(1)_Y is the exact route (spec).
- EW5 (composed): compose_electroweak(default_system(), on=True): compose OK; designations counted (mlapse/mbeta removed,
  added blocks reciprocal); vacuum fixed 3/3; rewind T = 2 exact; int64 headroom (Engine.stats).

## RESULTS (written Tue Nov 10 12:37:41 UTC 2026; runs 12:34:11–12:37:18 UTC; FINAL SUITE on the final code 12:37:03–12:37:18: 8 tests OK, 15.1 s)
Post-registration additions (declared): EW4b (global Noether of R3, BL, Q with the W excited) and EW5b (composed per-
generator local Noether); EW2's frequency estimator got a zero-variance guard (ω = 0 for an exactly static series) after
the first run returned NaN for kH = 0; EW4's photon check expected 2J′ but the ×2×2 normalisation gives X_Q = 4Q = 4J′
(corrected; the physics claim is unchanged); EW4b's JSON key "Q" collided with the global Q and was renamed Q_photon.
| test | result | file |
|---|---|---|
| EW1 L3 exactness (EW-ALONE) | reciprocal, 0 designated; rank 4 = 64 OD4-spring monomials only; b-only; vacuum 20/20; rewind T = 6 exact; local SU(2) Noether 0/486 with links/2-paths excited; int64 only | EW1_higgs_hop_exactness.json |
| EW2 W gap (L3) | kH = 0: the uniform transverse W stays EXACTLY static for 512 updates (massless). With the Higgs hop: 1 − cos w = 1.291e−3 (kH 2^10, v 2^16), 5.150e−3 (kH 2^12, v 2^16), 1.291e−3 (kH 2^12, v 2^15) vs predicted kH v²/(A D) = 1.302e−3 / 5.208e−3 / 1.302e−3: ratios 0.991 / 0.989 / 0.991. Scaling: w(kH ×4) / w = 1.998, w(v ×2) / w = 1.998, i.e. m_W ∝ v √kH (continuum m_W ∝ g v) | EW2_w_gap.json |
| EW3 L2(b) exactness (GW-ALONE, F excited ≤ 2^10) | reciprocal, 0 designated; rank 4 = springs only; vacuum 20/20; rewind T = 6; local SU(2) Noether 0/486 WITH THE LAPSE ON | EW3_graviweak_exactness.json |
| EW3b EP (MECHANISM static F) | m_eff/m = 0.9960785 (U = 2^−8) and 0.9842377 (U = 2^−6) vs 1 − U = 0.9960938 / 0.9843750: deviation −1.5e−5 / −1.4e−4 = −U²/2 (sqrt(1 − 2U) law) + |Φ| integer rounding; EP to O(U²) when the Higgs is relaxed. Unrelaxed Higgs (started at v): |Φ| oscillates around v_eff, clock modulation 0.49 % / 1.97 % (≈ 1.25 U): EP only ADIABATIC (no damping in a reversible law; prepare the Higgs relaxed) | EW3b_equivalence_principle.json |
| EW4 L1 algebra (exact) | ⟨∇Ψ_phys, X B⟩ = 0: global R3 (custodial T3_R, Higgs right-multiplied), BL, Q; local L3 at every node; X_Q annihilates the vev; Y (R3 part) acts on the Higgs; photon on matter = J′ on pair 1, 0 on pair 2 (= the default E1 coupling) | EW4_hypercharge_algebra.json |
| EW4b global Noether (W excited) | R3, BL, Q (incl. adjoint on links/2-paths): 0/6 failures each | EW4b_global_noether.json |
| EW5 composed | compose_electroweak(v2 default): +matter2, wsu2, chiral, ehop, gwb; −mlapse, −mbeta; designations 1202 → 706 (= −496 of mbeta; added blocks add 0); vacuum 3/3; rewind T = 2; int64 only | EW5_composed.json |
| EW5b composed local Noether | t3 0/81 failures (E1, Higgs hop, graviweak lapse all t3-invariant); t1, t2 54/81 failures each: E1 couples only pair 1's charge (charged W) = HL-1's L1 claim confirmed | EW5b_composed_local_noether.json |
NOT BUILT (priority 1 of the manager, honest status): an exact LOCAL U(1)_Y Gauss law. E1 cannot gauge Y: Y acts on the
second-order Higgs (EW4) and Q on the charged W links, and Study 4 A1 says a second-order gear cannot feel A0 (no carrier).
Exact rank-3 route (spec, DERIVED): (i) ONE U(2) link per face (complex 2×2, 8 gears) for the doublet hop (separate U·B
links make the doublet hop rank 4); (ii) the Higgs as a complex doublet φ hopping through V (Y_H = the doublet unit),
with Yukawas through φ and φ̃ = iσ2φ* (real-linear); (iii) e_R has twice the doublet charge, so its hop needs det V
(quadratic): an auxiliary charge-2 U(1) link B locked to det V by the rank-3 gauge-invariant term ⟨B, det V⟩;
(iv) U(2) plaquette dynamics (2-path gears in the M2C algebra, as for su3) + OD4 springs. Then SU(2)_L × U(1)_Y is exact
locally and the photon is the unbroken Q (vector-like, = E1's coupling on matter). Estimated 2–3 h build + tests.
Option (a) of L2 (a new rank-4 kind "singlet field × gauge-invariant rank-3 monomial"): cost = a new rank-4 element type
beyond OD4 (owner decision), on every dressed monomial (doublet hops, Yukawa, Wilson–Yukawa); not built.

## THE SWITCHES (integrator; no existing file edited)
In layers/system.default_system add `chiral: bool = False, electroweak: bool = False` and, just before the final return:
`if electroweak: from .electroweak import compose_electroweak; return compose_electroweak(System(Q, tuple(blocks), info), on=True)`
`if chiral: from .chiral import compose_with_default; return compose_with_default(System(Q, tuple(blocks), info), on=True)`
(electroweak implies chiral; DEFAULT OFF when written: layers/electroweak.EW_DEFAULT_ON = False,
layers/chiral.CHIRAL_DEFAULT_ON = False. Since 13:17 UTC `default_system()` has `chiral=True, electroweak=True` by
default (owner decision 5), with gwb at FIX-i (v8-1): see README_v1_draft.md sections 0 and 7c.)

## FILES (sha256, Tue Nov 10 12:37:41 UTC 2026)
| file | sha256 |
|---|---|
| layers/electroweak.py | 58ffc05023d26ae02d62daf80014ef8a3a2c6bed94c97e130dae0b4929295491 |
| tests/test_electroweak.py | 4ed6e1efe8dd54647ae3c02083a7ae4af46fa7eb86af9cdb303b9c5f05d94dae |
| results/electroweak/EW1_higgs_hop_exactness.json | 57896ed61bf7d0eb35fb335be7f26d2db95661537ba3d5275245e9cbc5246561 |
| results/electroweak/EW2_w_gap.json | 49836ad567bfdfd7839c40d5617a2642ea2b440e621cfb4d07233d198b0e4c05 |
| results/electroweak/EW3_graviweak_exactness.json | 2401171aa85afac20ed53b41138678bc758d070473c2da9a18becc5a23eee71c |
| results/electroweak/EW3b_equivalence_principle.json | 53a1407fc7fe993d934335d94fd377462225f22c5989aa29d97402cb19f60bf5 |
| results/electroweak/EW4_hypercharge_algebra.json | 849eda17593d9e633795875b478f4d47105363963978ed7aa611c5ce5ae9e452 |
| results/electroweak/EW4b_global_noether.json | 0a0df1ac4c3847d2d28ed6cd6c4910afc4268c1ac7591139035a8e4fc8f4a466 |
| results/electroweak/EW5_composed.json | e5d3a42b87eee2a1feb156cc64555fcb602b9c425434aef471c64c440a2b9858 |
| results/electroweak/EW5b_composed_local_noether.json | 002dc22dc56bfb4e5c352fcbfccb7a4de7da83d3d6b78d089b7398ed88702c9d |
Package files modified: NONE (new files only); core/, universe24/ untouched; no git.

## ADDENDUM (Tue Nov 10 12:39:45 UTC 2026): the exact local U(1)_Y route has one more subtlety (DERIVED; not built)
With ONE U(2) link V per face, the Higgs hop can be U(1)_Y-covariant only through the charge-+1 column of the quaternion
Higgs, φ̃ = (Φ1 + iΦ2, Φ0 − iΦ3) (Φ = (φ̃, φ) columns; U(1)_Y acts on Φ by right multiplication e^{−θk}, EW4): the hop
κH Re(φ̃(x)† V φ̃(x+e)) is rank 3 and exactly SU(2)_L × U(1)_Y covariant. But at the vev φ̃ = (0, v) it pulls ONLY the
vev-direction entry V₁₁ (κH v² V₁₁ᵣₑ), not the identity: no gauge-invariant quadratic balances it, so the static link
vacuum is diag(A, A₁) with A₁(A₁² − A²) = κH v²/λ (spring λ) — the Higgs vev distinguishes the Z/photon directions on
the links themselves. An exact integer vacuum needs (κH, v, λ, A, A₁) tuned to satisfy this cubic (e.g. A₁ = A + 1 needs
κH v² = λ (A+1)(2A+1)): OPEN design work, together with the det-V-locked charge-2 link for e_R and the U(2) 2-path gears.

## ADDENDUM 2 (Tue Nov 10 12:46:57 UTC 2026): a third rank obstruction on the exact local U(1)_Y route, and one tuning example (DERIVED; not built)
(1) The charged Wilson–Yukawa link term breaks local U(1)_Y. The chiral block's off-site Wilson–Yukawa
−(w/2) b(x+e)ᵀ[ρ(φ(x+e)) Π_W W0 + W0 Π_W ρ(φ(x))ᵀ] b(x) is rank 3 only because Y is global. It pairs L at one end
(contracted with the Higgs there) with R at the other end, so it moves a hypercharge Y(R) across the link:
- ν_R has Y = 0. That half needs no link and stays rank 3.
- e_R has Y = −1, two doublet units. That half needs a charge-2 link factor, B or det V, which makes it rank 4: not an
  OD4 spring, so the manager's rank-4 ruling forbids it.
- The other order, V(x,e) φ(x+e), is also rank 4.

Rank-3 escape: auxiliary hybrid link gears Ξ(x,e) ~ V(x,e) φ(x+e) and Ξ′(x,e) ~ φ(x) B(x,e). Each would be locked by a
rank-3 covariant term ⟨Ξ, V φ′⟩ (resp. ⟨Ξ′, φ B⟩) with its own inertia, and its vacuum would need a tuned integer
value. The alternatives are: drop the charged Wilson–Yukawa (the charged doublers turn light, an explicit
Nielsen–Ninomiya cost), or get an owner ruling for a rank-4 element that is not a spring.

Full exact list for local SU(2)_L × U(1)_Y with the doublers lifted:
- U(2) links V (8 gears) + U(2) 2-paths;
- the φ̃-column Higgs hop (link vacuum diag(A, A₁));
- B locked to det V (the e_R hop);
- Ξ and Ξ′ (the charged Wilson–Yukawa);
- matter's free hop split into L (through V), e_R (through B) and ν_R (free). This means filtered copies of the
  approved matter blocks, which are not edited.

Estimate: 3–4 h build + tests. NOT BUILT.

(2) Integer vacuum example for the distorted link: A = v = 2^16, λ = 4, A₁ = A + 2^10 gives
A₁(A₁² − A²) = 2^30·8385 = κH v²/λ with κH = 8385, exactly (checked by integer arithmetic). This is the balance without
2-paths. With U(2) 2-paths the 2-path vacuum becomes diag(P0, P0′), and its unequal pull adds 4κ_P(P0′ − P0)A₁ to the
right-hand side (retune).

No code was changed by either addendum; the files and results above are unchanged.
