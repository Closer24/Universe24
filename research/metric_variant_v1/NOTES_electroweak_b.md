# NOTES_electroweak_b — ROUTE B: exact LOCAL SU(2)_L × U(1)_Y (EW-BUILDER = HAND-M1). DECLARED CANDIDATE, DEFAULT OFF

The owner chose route B at 13:2x (E1 retired as a separate photon; the photon is the W3/B mix). Every stamp below is from
`date -u`.

NEW FILES ONLY:
- layers/electroweak_b.py
- observe/electroweak_b.py
- tests/test_electroweak_b.py
- results/electroweak_b/
- this file

No existing package file is modified. core/ and universe24/ are untouched. No git.

## Design (Tue Nov 10 14:47:41 UTC 2026; full account in the layers/electroweak_b.py docstring)
The rank-3 route of NOTES_electroweak (12:39 / 12:47 addenda), with one change that removes the cubic tuning.
- **ONE U(2) link per face** (8 gears), V = Σ v_μ E_μ with E = (1, EPS, iSX, iSZ, i, iEPS, −SX, −SZ).
  - Its doublet representation is R(M) = Re M ⊗ 1 + Im M ⊗ J′, so t_a = R(EPS, iSX, iSZ) and J′ = R(i).
  - The L doublet hops through V; e_R and ν_R do not.
- **Higgs.** The quaternion's column col2 has Y = +1 and hops through V: kH Re(col2† V col2′). col1 has Y = −1.
- **The charge-2 link B** is locked to det V by kB Re(B̄ det V) (rank 3). It carries the e_R hop. It is the "det-shadow" link.
- **Hybrids.** Xi ~ V†col1(x) and Xi′ ~ V col1(x+e), each with a rank-3 lock. They carry the charged Wilson–Yukawa at rank 3.
- **NEW: an isotropic vacuum.**
  - The hybrid locks pull the charged slot (col1 vev) by 2 kXi v xi0. The Higgs hop pulls the neutral slot (col2 vev) by kH v².
  - With 2 kXi xi0 = kH v the −SZ pull cancels exactly, so V0 = A·1. There is no diag(A, A₁) distortion and no cubic integer
    tuning.
  - The vacuum identities are checked in ewb_params; deviation_terms asserts that no linear term remains.
- **Gauge sector.**
  - B1-GAUGE-type U(2) 2-paths: kappa_P = 256, c_P = 0, beta = D − 2^33 (the frozen-photon regime).
  - OPTION plaquette=True: the approved plaquette kind (owner 14:37), built B3-locally with relays R(x;a,b) ~ V(x+e_a,b) and
    the split plaquette −w‖V_a R_ab − V_b R_ba‖² (on site).
- **No graviweak.** This is FIX-i, owner decision 1. In the composed system the doublet has no lapse coupling (OPEN).
- **Composer.** compose_electroweak_b(base) works on the hands-OFF base: it retires "em" (E1), removes "mlapse"/"mbeta", and adds
  matter2 + ewb.
  - This is ONE-A's hook one_system(route_b=True) (agreed 14:51).

## PRE-REGISTRATION (Tue Nov 10 14:47:41 UTC 2026; tests/test_electroweak_b.py implements EWB1–EWB6; L = 3 unless stated)
- **EWB1 — exactness, EWB-ALONE (matter + matter2 + ewb, default regime).**
  - compose (B3) and check_reciprocity pass, with 0 designated terms.
  - Rank ≤ 4, where the rank-4 terms are the two OD4 springs only.
  - The vacuum stays fixed for 20 updates; rewind over T = 6 is exact; int64 headroom.
- **EWB2 — the core claim.** On a random fully excited state:
  - the Lie derivative ⟨∇Ψ_phys, X_y B⟩ is 0 at EVERY node for t1, t2, t3 and Y;
  - the discrete Noether identity over T = 6 has 0 failures for each generator;
  - the size of the remainder term (the "continuous Gauss jitter") is reported;
  - three negative controls must FAIL: e_R charge 1, B not rotated, Xi phase omitted.
- **EWB3 — the photon Q = (t3 + Y)/2.**
  - X_Q annihilates the vacuum (every field).
  - The global Q charge changes exactly by the global remainder term.
  - The Q Gauss law is the half-sum of the t3 and Y laws.
- **EWB4 — composed.** compose_electroweak_b(default_system(chiral=False, electroweak=False)):
  - compose OK, with em/mlapse/mbeta removed and the designations counted;
  - the vacuum stays fixed for 3 updates; rewind over T = 2 is exact;
  - the local Gauss laws have 0 failures over T = 2.
- **EWB5 — linear spectrum** (exact coefficients, Bloch; boson sector; L = 8 k-set incl. the corner, and k = 2π/64).
  - Pass: every V_eff eigenvalue is in [0, 2D] up to 1e−9 D, and there are 4 gauge zero modes per k.
  - Reported: the photon branch (massless) and its v/c_Q; h_W/D and h_Z/D; m_Z/m_W; sin²θ_W(on-shell).
- **EWB6 — the plaquette option** (relays, diff lock, M_R = 2^33, w = 1).
  - Pass: exactness (Lie, Gauss, vacuum, rewind) and the band check.
  - Reported: v_γ/c_Q.
  - PREDICTION (from 14:46 probes): exact and band-legal, with v_γ well below c_Q, because relays and the det-shadow B add
    inertia. Reported honestly.

## RESULTS (written Tue Nov 10 14:51:03 UTC 2026; FINAL SUITE on the final code: 7 tests OK in 5.2 s, 1 thread)
Post-registration addition (declared): EWB6b, the plaquette option plus the det-shadow kinetic term (w_B = 1).

| test | result | file |
|---|---|---|
| EWB1 exactness (EWB-ALONE) | reciprocal, 0 designated; rank 4 = 280 OD4 spring terms only; G 138; 13,529 monomials; vacuum 20/20; rewind T = 6 exact; int64 only | EWB1_exactness.json |
| EWB2 LOCAL GAUSS (core claim) | Lie derivative 0 at all 27 nodes for t1, t2, t3, Y. Discrete Noether 0 failures (T = 6) for each. All three negative controls FAIL (27/27 nodes): e_R charge 1, B not rotated, Xi phase omitted. Continuous (remainder-free) Gauss jitters: \|remainder term\|/\|J2\| = 1.7e−3 to 4.1e−3 per update on a random state | EWB2_local_gauss.json |
| EWB3 photon Q | X_Q annihilates the vacuum. t3 alone does not (it moves H_k and the Xi/Xi′ phases); Y cancels it. Global 2Q changes by exactly the remainder term | EWB3_photon_charge.json |
| EWB4 composed (hands-OFF base) | em (E1), mlapse, mbeta removed; designations 1202 → 44; G 437; vacuum 3/3; rewind T = 2; local Gauss 0 failures | EWB4_composed.json |
| EWB5 spectrum (default kappa_P = 256) | Band OK; 4 gauge zero modes per k. Photon massless: h/D = 9.23e−10 at k = 2π/64 (∝ k²), v = 7.6e−4 c_Q (FROZEN). W: h/D = 1.2919e−3 (ω 0.0508). Z: h/D = 1.5401e−3 (ω 0.0555). m_Z/m_W = 1.0919, so sin²θ_W(on-shell) = 0.161 (the det-shadow B's inertia, not 1/2) | EWB5_spectrum_default.json |
| EWB6 plaquette option (relays, M_R = 2^33, w = 1) | exact (Lie 0, Noether 0, vacuum, rewind); band OK; photon v = 0.253 c_Q | EWB6_plaquette_option.json |
| EWB6b + det-shadow kinetic (w_B = 1) | exact; band OK; photon v = 0.333 c_Q | EWB6b_plaquette_det_shadow.json |

Probes (scratch, not registered; s7/HAND-M1_work/ewb/):
- U(2) 2-paths at kappa_P = 2^17 are linearly UNSTABLE: the 2-path Hermitian sector has h ≈ −0.1 D.
- Plaquette w = 2–3 (with λ = 1) breaks the band edge: h_max 2.4–3.2 D, from the split plaquette's radial (corner-trace) stiffness.
- Relay M_R = 2^34 also breaks it (2.34 D).

**ONE LIGHT: NOT reached (DERIVED + NUMERIC).** The chain of reasons:
- B3 (one node or one face link) rejects a direct four-link plaquette monomial, which touches three nodes, so the plaquette
  must be carried by relays.
- Each relay is a full Rule3 gear with inertia D (one divisor), so the photon's inertia is multiplied by
  (1 + number of relay copies) = 3. Hence v_γ ≤ c_Q/√3 at w = 1, and 0.33 c_Q is measured once the det-shadow B shares the
  photon.
- Raising w (and w_B) to 3 to compensate needs a corner counter-term to keep the band edge (OPEN; ONE-LIGHT-A's construction is
  not available as a file).
- One light on c_Q is NOT claimed. The missing law is a B3-legal plaquette without relay inertia, or a counter-term that
  restores the band at w = 3.

## SWITCH LINES (integrator; DEFAULT OFF; no existing file edited)
In layers/system.default_system, add `route_b: bool = False` and, before the electroweak/chiral lines (it needs chiral=False and
electroweak=False):
`if route_b: from .electroweak_b import compose_electroweak_b; return compose_electroweak_b(System(Q, tuple(blocks), info), on=True)`

ONE-A's hook (agreed 14:51): one_system(route_b=True) applies compose_electroweak_b to default_system(Q, chiral=False,
electroweak=False). A callable is also accepted.
Plaquette variant: compose_electroweak_b(base, on=True, plaquette=True, M_R=2**33, w_B=1).

## FILES (sha256, Tue Nov 10 14:51:03 UTC 2026)
| file | sha256 |
|---|---|
| layers/electroweak_b.py | 67b45d219a95d1b5057f1603cfef0fdf1a6b9a657d8f16b0540ff33a7d7eee86 |
| observe/electroweak_b.py | bab4772fb875d43976ebf0790489e4b3025b34d5418b73290513a1c526885939 |
| tests/test_electroweak_b.py | 2b83fb6e574897fb62ffcf231a51d684dff676c654a022d821bb76664d4e9555 |
| results/electroweak_b/EWB1_exactness.json | b77b892e13c77e1dcf1070a69b6d16051549e7990ae83d28656f8b417762829f |
| results/electroweak_b/EWB2_local_gauss.json | 41a59501013ce7d5c7ae65a82220f6c605189db3b775e67abee24500816cbd45 |
| results/electroweak_b/EWB3_photon_charge.json | 7d9cee7829f59dbd65e1d251f0aa70c3d51c8d18eb12e93039180706712eb1c4 |
| results/electroweak_b/EWB4_composed.json | d10b85ed250d0ddfc3c3815f78573cc9544673b05367031c445429604363fbac |
| results/electroweak_b/EWB5_spectrum_default.json | 187eedbed1576f2330de487cd1110b43aa1c6293cd905fa05eca1655f6d5c102 |
| results/electroweak_b/EWB6_plaquette_option.json | 95d0bbc3fecee2c1785a7f3509aa6fe9256ce3433d3601b8f6264a87fe4dc272 |
| results/electroweak_b/EWB6b_plaquette_det_shadow.json | 15f833a20fcbcb1913015624a6e4160e2fe98cca83de83f5e70c200bb5a946d5 |
Package files modified: NONE (new files only); core/, universe24/ untouched; no git.

## ADDENDUM — ONE-LIGHT scan (Tue Nov 10 14:56:55 UTC 2026; manager 14:56: B3 has NO exception, relays are the legal route, TUNED must be labelled)
I scanned the relay-carried approved plaquette (exact-coefficient Bloch spectra; band legality checked at 15 L = 8 k
including the corner; photon speed at k = 2π/64). Grid:
- relay scale s ∈ {1, 3/2, 2, 3}; plaquette w = w_B ∈ {1, 2, 3}; spring λ ∈ {1, 2}; relay lock M_R ∈ {2^30 … 2^34};
- two corner forms:
  - "split": −w‖V_aR_ab − V_bR_ba‖²;
  - ONE-LIGHT-A's symmetric "sym4" (the manager's text of s19): (w/2)·(four corners) − 2w⟨V_aR_ab, V_bR_ba⟩, all on site
    through relays.

Files: SCAN_relay_split.json, SCAN_relay_sym4.json, DISPERSION_sym4_best.json.
- **Split form.** The best band-legal point is v_γ = 0.333 c_Q (s = 1, w = 1, M_R = 2^33). w ≥ 2 or M_R = 2^34 leave the band.
  - s = 3/2 cannot be built: its vacuum is not static.
  - s = 2 and s = 3 break the band (h_max up to 18 D), because the V lock stiffness grows as s².
- **sym4 form (EWB6c).** The best band-legal point is v_γ = 0.408 c_Q (s = 1, w = w_B = 1, λ = 1, M_R = 2^34).
  - The speed has converged at small k: 0.4079 / 0.4079 / 0.4078 at k = 2π/256, 2π/128, 2π/64.
  - The covariance is exact: Lie 0, Noether 0, vacuum, rewind.
  - The photon is about 89 % det-shadow sector (B and its relays S).
- **v_γ is governed by the relay lock, not by w.**
  - At w = 1: v_γ = 0.26 / 0.33 / 0.41 c_Q for M_R = 2^32 / 2^33 / 2^34.
  - Raising w helps little: 0.408 → 0.471 → 0.499 at M_R = 2^34, and those points leave the band.
- **W/Z in this configuration.** ω_W = 0.0294–0.0300 and ω_Z = 0.0321–0.0326 (k = 2π/256). Against the 2-path build (ω_W = 0.0508), ω_W is
  reduced by about √3: the relay copies triple the link inertia. m_Z/m_W ≈ 1.09.

**CONCLUSION (DERIVED + NUMERIC; declared OPEN limitation).** Under one divisor (every gear has inertia D) and B3 (six face
neighbours; the plaquette must be relayed), the photon is slower than gravity:
- each physical link is carried by itself and two relay copies, so its inertia is ×3 and v_γ ≤ c_Q/√3 = 0.577 c_Q even with
  ideal relays;
- a faithful copy needs M_R ≫ (the plaquette's stiffness on the relay), while Rule3's band needs M_R + that stiffness ≤ 2D;
- the best band-legal photon measured is 0.408 c_Q.

ONE light on c_Q is NOT reached and NOT claimed. A photon slower than gravity is contradicted by GW timing, so this is OPEN. The
missing law is a plaquette without relay inertia; the owner keeps B3, and the divisor is ONE.

Nothing here is a tuned counter-term. The sym4 corner weights are ONE-LIGHT-A's construction, not fitted. M_R and w are scan
parameters (TUNED-free).

Default for ONE v2 (manager 14:56: integrate the exact-Gauss build as it is): compose_electroweak_b(base, on=True), i.e. U(2)
2-paths with a frozen photon. The best light-carrying variant is compose_electroweak_b(base, on=True, plaquette=True,
corner_form="sym4", M_R=2**34, w_B=1, lam=1).

### FILES after this addendum (sha256, Tue Nov 10 14:56:55 UTC 2026)
| file | sha256 |
|---|---|
| layers/electroweak_b.py | b69c73d58c8d64ed36b7ceb871c740a7b70016b7544d11fdffb917d560285894 |
| observe/electroweak_b.py | bab4772fb875d43976ebf0790489e4b3025b34d5418b73290513a1c526885939 |
| tests/test_electroweak_b.py | 4d8c2dbcab55c0743ae1a5d1da1d1f70f96132cf9718926df8181a31d3dec8a4 |
| results/electroweak_b/DISPERSION_sym4_best.json | 63c3c3145ebf9e4e22646045b17efd36237381181fda1c15ce5b2c358770b815 |
| results/electroweak_b/EWB1_exactness.json | bfbd0690b4c8febe8e3419046341321afe7281cb886092cdb3da7516238f7363 |
| results/electroweak_b/EWB2_local_gauss.json | 78dc1cb8e6ff937b436be4f172c401e8326aeeeef3805011656448d573046c73 |
| results/electroweak_b/EWB3_photon_charge.json | 94b3b6c3b6669fcfdcbfc4ae3dc05623a01b6a1864ffe32a006bb33c328dc6a5 |
| results/electroweak_b/EWB4_composed.json | 05497804ccdfaa7b107b2835d9766de0d8ee1e9e4bd313e4543b35a873ef7c44 |
| results/electroweak_b/EWB5_spectrum_default.json | 0ee32d8e2a81edeb4dd21e1644aefe2dfd03ec15f68d3dc1da990cffc7c4617d |
| results/electroweak_b/EWB6_plaquette_option.json | 11afd87f04fe5a60e9f744f7b555625fb21691adaf7e1fef1ec6c883e18c1ff8 |
| results/electroweak_b/EWB6b_plaquette_det_shadow.json | 25bbc4242f06cb2fc1cdf6c8d0dac345eb80d33687e5c20e6bd138cc0967ed45 |
| results/electroweak_b/EWB6c_plaquette_sym4_best.json | 700ae8a2dd9869a1d30a68191b430d5e2fec148e7149dfe97a83efa9756e52a4 |
| results/electroweak_b/SCAN_relay_split.json | b424098beb6f5aa124a3d6834c9410b2140a00d00df69e47926a5224d911915d |
| results/electroweak_b/SCAN_relay_sym4.json | 33709b8cb917229b53fa84df646b40633f571b92dd18182075b6ada8e86b93dd |

## OWNER TRADE-OFF (written Tue Nov 10 15:02:25 UTC 2026, at the manager's request 15:03)
**(A) E1 photon on the cone** (route A: the hands-ON default with FIX-i).
- Gives: one light on c_Q, with E1's exact Gauss law for the photon charge.
- Costs: hypercharge is only GLOBAL. Composed with E1, the local t1/t2 Gauss laws fail (NOTES_electroweak EW5b: 54/81),
  because E1 couples only the charged pair. So local Gauss fails in weak (charged-W) processes.

**(B) Route B (this build).**
- Gives: exact LOCAL SU(2)_L × U(1)_Y. All four discrete Gauss laws are exact (EWB2/EWB4), Q is conserved (EWB3), and E1 is
  retired.
- Costs: the photon (the W3/B mix) is either frozen (2-path build) or at most 0.408 c_Q (relayed approved plaquette, sym4,
  best band-legal point, EWB6c). The ceiling is c_Q/√3 even for ideal relays.
- So light is slower than gravity, which GW/light timing (~1e−15) contradicts.

**(C) A NEW LAW "plaquette without relay inertia".** It needs either:
- a B3 exception: a three-node plaquette monomial, against the fixed rule of six face neighbours; or
- a second divisor: relays lighter than D, against ONE divisor.

Both are against fixed rules. The owner chooses; this build is opt-in (EWB_DEFAULT_ON = False) and changes nothing by default.

## L = 8 EXACT-DYNAMICS CONFIRMATION (written Tue Nov 10 15:06:33 UTC 2026; run in scratch per the manager, not in results/)
Scratch: s7/HAND-M1_work/ewb/dyn8.py; output dyn8_sym4.json, dyn8_2path.json.
- Method: T = 1000 updates at L = 8, one thread. Each mode is prepared as its exact Bloch eigenvector (integer-rounded, at rest),
  and the frequency is read by a least-squares fit of the projected series.

| build | mode | measured ω | linear ω | difference / speed |
|---|---|---|---|---|
| sym4 | W, lowest massive mode carrying the EPS direction, k = 0 | 0.02945 | 0.02941 | +0.14 % |
| 2-path | W, k = 0 | 0.05098 | 0.05084 | +0.28 % |
| sym4 | transverse neutral branch at k = 2π/8 | 0.18365 | 0.18365 | 0.405 c_Q |

- At k = 2π/8 the photon and the transverse Z are within 3 % of each other, because the mass is negligible at that k.
- The 2-path build's "photon" pick at k = 2π/8 selected the Z (the frozen photon is far lower), so it is discarded.
- The small-k photon speed 0.408 c_Q (k ≤ 2π/64) would need L ≥ 64 for a direct run. It rests on the exact-coefficient linear
  analysis, which these runs reproduce to ≤ 0.3 %.

## FINAL FREEZE LIST (sha256, Tue Nov 10 15:06:51 UTC 2026). Final suite on these files: 8 tests OK, 9.9 s (one thread).
- Route B is OPT-IN only: EWB_DEFAULT_ON = False, and layers/system.py contains no route-B line.
- After this list, NONE of the files below will be edited (manager 15:09 freeze rule).

| file | sha256 |
|---|---|
| layers/electroweak_b.py | 2315ecedfd828f31a456be0807757ef8f9a83441fa428a0d0930f7c3a600c5c1 |
| observe/electroweak_b.py | bab4772fb875d43976ebf0790489e4b3025b34d5418b73290513a1c526885939 |
| tests/test_electroweak_b.py | 4d8c2dbcab55c0743ae1a5d1da1d1f70f96132cf9718926df8181a31d3dec8a4 |
| results/electroweak_b/DISPERSION_sym4_best.json | 63c3c3145ebf9e4e22646045b17efd36237381181fda1c15ce5b2c358770b815 |
| results/electroweak_b/EWB1_exactness.json | 26b4042304bb185f3543a212dbf372834c2c4b6ea5155b8c498575bf76c67548 |
| results/electroweak_b/EWB2_local_gauss.json | 77160cc76de7fc69aeba96911f2bb56b9c4c75abe064825dde566c2d3cd42ffd |
| results/electroweak_b/EWB3_photon_charge.json | 635f4ec294a7479f854314cd59c905d21a7e34e8f7d676f56de6446afad0c199 |
| results/electroweak_b/EWB4_composed.json | 3309b64b2eb8cf5567eab839ecab9af84ee40d1793469f3551e8c64249b37ef4 |
| results/electroweak_b/EWB5_spectrum_default.json | 3f52bf79ed65eb301b03ac5a922636d63bf51746947e2dbf7e867fc0611fc6e8 |
| results/electroweak_b/EWB6_plaquette_option.json | 84332c816ffbc5e1c0a48f4b96d7aff372039ddd412f1c7586c9aa5f54609b2d |
| results/electroweak_b/EWB6b_plaquette_det_shadow.json | 215fe51c935d4f31f1f1e09e9ec5cfdc56b8f0ce684c507e1faff9c3e0efbf86 |
| results/electroweak_b/EWB6c_plaquette_sym4_best.json | 16a57e63fa5bce739465f65c93190a4e081b6cb6a1c92da7b8889c6ae95de3ce |
| results/electroweak_b/SCAN_relay_split.json | b424098beb6f5aa124a3d6834c9410b2140a00d00df69e47926a5224d911915d |
| results/electroweak_b/SCAN_relay_sym4.json | 33709b8cb917229b53fa84df646b40633f571b92dd18182075b6ada8e86b93dd |
NOTES_electroweak_b.md itself is hashed at hand-off (message to REV-ARCH / manager), since this line is its last edit.
