<!-- Dated record copied into the package on 2026-11-10 by the manager (Study 25 should-fix S-1). Source: scratchpad s18/AGREE_STAB.md.
     It is the signed evidence for FIX-i (graviweak lam_H = lam_L = 0), the hands-ON default adopted by the owner (decision v8-1, 14:37 UTC).
     Paths of the form s<N>/... refer to the research scratchpad records, not to files in this repository. -->

# AGREE_STAB — Study 18 (hands-ON runaway)
Created by STAB-B 14:00:31 UTC. Rows rewritten by STAB-B at the stamp below, before any append.
EW-BUILDER: APPEND only (do not rewrite). Add a section "EW-BUILDER marks" at the end, one line per row:
R# | AGREE / DISAGREE / CAN'T-CHECK | note | your evidence. Then sign with a date -u stamp.
Paths are relative to s18/STAB-B_work/. pin and pin2 are sha256-verified copies (68/68 OK) of the EMERGE-N pins.
ARM B = default_system() of the pin (chiral = electroweak = True, beta_form detuned), fingerprint 473b7b9f… (= EMERGE-N's).

## Rows
| R# | claim (STAB-B) | label | evidence | EW-BUILDER mark |
|----|----------------|-------|----------|-----------------|
| R1 | Repro at L=4: ARM B with S2* 2^16 runs away at t* = 121. wsu2 is first above 2^34 (64 bits at t=119, metric 43). | NUMERIC | runs/L4_B_S2_16.json | |
| R2 | The ARM B VACUUM is linearly unstable in two lapse modes: k=0 with lambda = +1.138057 (eigenvector 99% metric.h00), and the corner (pi,pi,pi) with lambda = -1.025995 (period 2, 100% metric.h00). All other L=6 k checked: 1.00000003. Bc, Bng and "gwb removed" are marginal (1.0000001). | DERIVED (exact integer tensor; float eigenvalues are analysis only) | a3_linear.py, a4_thresh.py, a5_corner.py; NOTES §2, §4 | |
| R3 | Matter-free check: vacuum plus a uniform lapse offset of 1 gives U_mean x1.138 per update and a runaway at t* = 138 (L=4). | NUMERIC | runs/L4_B_K0_1.json | |
| R4 | Cause. The metric.h00 k=0 row sum is exactly D (top band edge) and its corner value is -1+2/Q (bottom edge). gwb's F(abs(Phi)^2 - v^2) and (F_x+F_y)(abs(U)^2 - A^2), expanded at Phi=v, U=A, give bilinears F.phi_1 = -D/48 (on-site) and F.u_1 = -D/24 per link (link form). Level repulsion then: k=0 from links + Higgs; corner from the on-site Higgs bilinear only. Removing only gwb's degree-1 entries restores 1.0000001 at k=0. | DERIVED | a2_hess.py; a4 k0 B_nobil | |
| R5 | Edge-mode lemma: in a symmetric linear Rule3 system, a mode at a band edge (m = +1 or -1) with any nonzero coupling to other modes produces an eigenvalue outside [-1, 1], hence abs(lambda) > 1. Every SU(2)-covariant rank<=4 coupling of F to abs(Phi)^2 or abs(U)^2 contains such a bilinear (v, A nonzero). | THEOREM (Rayleigh quotient) | PROPOSAL §2 | |
| R6 | Thresholds after the lapse grows (adiabatic, relaxed radius): U < -0.4985 (the relaxed radial link clock leaves the band, period 2), U = +1/4 (the link radius collapses: the (1-4U) flip, as in L0), U = 1/2 (the vev collapses). Then the F <- abs(U)^2 loop gives a finite-time blow-up (bits x2.4-2.8 per update). RETRACTED: my 14:01 "gauge links tachyonic for every U<0". That came from linearising at the unrelaxed radius and holds only in the non-covariant truncation without the bilinears (t* = 92). EW-BUILDER's relaxed-radius argument is accepted. | DERIVED | NOTES §2; runs/L4_B_nobil_S2_16.json | |
| R7 | Bisection at L=4, S2* 2^16 (t*): B 121; Bnh 114; gwb minus Higgs-lapse group 135; minus link-factor group 334; minus singlet hop 117; link group only 126; Higgs group only 318; hop only, Bng, Bc and gwb removed bounded 1000. Agrees with EMERGE-N at L=6 (137 / 380 / stable). | NUMERIC | runs/L4_*_S2_16.json | |
| R8 | The manager's hypothesis ("form C replaced") is half right. compose_electroweak removes mlapse/mbeta (744+496 terms) and adds no mlapse2/mbeta2. But the runaway comes from what gwb ADDS (the edge-mode bilinears), not from losing form C. Bc (form C) also drifts at L=4 (U_mean -0.36 at t=1000) but has no gwb, so it does not run away. | DERIVED + NUMERIC | a1_static.py; runs/L4_Bc_S2_16.json | |
| R9 | FIX-i = build_graviweak_b(lam_H=0, lam_L=0), keeping the singlet-half hop. It uses existing parameters, is coefficient-level, SU(2)-covariant, rank 3, and is NOT a new law. Fingerprint b51d3f2c… (= gwb filtered to its hop terms). Marginal at k=0 and at all L=6 k checked, corner included. | DERIVED | a4/a5 outputs | |
| R10 | FIX-i at L=6: vacuum fixed for 10 updates; rewind10 exact (S2* 2^16 and J-pure 2^12); R* via r_star_hands_on gives X(s0)=s0 and X(F^t s0)=F^-t s0 for t=1..10 with 0 mismatches, both seeds. | NUMERIC | runs/vf_FIX_S_built_L6.json | |
| R11 | FIX-i bang seeds at L=6: S2* 2^16 bounded to t=1196 (max 29 bits, em; U_mean -0.036). J-pure 2^12 and S2* 2^12: see the addendum below. Caveat: the uniform-lapse drift accelerates slowly (as in the form-C control); behaviour beyond about 1200 updates is OPEN. | NUMERIC | runs/L6_FIX_S_built_*.json | |
| R12 | FIX-C (EW-BUILDER: Psi -= sum (c/2)(F_x+F_{x+e})^2, c = 36417963) fixes k=0 (1.000000038) but leaves the corner at 1.025995. At L=4 it runs away: S2* 2^16 at t* = 573 (chiral leads) and the corner datum at t* = 837 (both inside the pre-registered windows). K0:1 stays bounded to 1500. | DERIVED + NUMERIC | a5 FIX_C; runs/L4_FIX_C_*.json | |
| R13 | FIX-C+ = FIX-C plus Psi += sum (c'/2)(F_x - F_{x+e})^2 with c' = 1,500,000 (threshold between 1.4e6 and 1.5e6). Marginal at k=0 and at the corner (1.00000003); full L=6 k scan and L=4 dynamics: see the addendum. | DERIVED (+ NUMERIC pending) | a5 FIX_CP; runs/L4_FIX_CP_*.json | |
| R14 | On-site k=0 margin (the manager's fix ii): epsilon = 0.0084 D is not enough (k=0 1.0126); 0.009 D works at k=0. But it pushes the corner further out (EW-BUILDER: 1.142) and gives the bare lapse a Yukawa range of 1/sqrt(6 eps) = 4.3 sites. Rejected. | DERIVED | a4 k0 B_det84/90/100 | |

## Side by side (what the fixed hands-ON default keeps)
| | FIX-i (lam_H = lam_L = 0) | FIX-C (EW-BUILDER) | FIX-C+ (FIX-C + corner term) |
|---|---|---|---|
| vacuum linear stability | marginal at all k checked | k=0 fixed, corner 1.026 UNSTABLE | marginal at all k checked |
| bang seeds | bounded >= 1196 (L=6 S2* 2^16); others: addendum | runs away (L=4: 573) | pending (addendum) |
| new law? | no (existing parameters) | yes: lapse counter-term, tuned to chi (owner decision) | yes: two tuned lapse counter-terms (owner decision) |
| tuning | none | c = ceil(chi/12), must be re-tuned if v, A, lam, P or kH change | c and c' both tied to chi |
| "Higgs sets the clocks" | OFF | ON | ON |
| EP for the doublet | NOT exact: the doublet's mass and the doublet half of the transport have no lapse factor (OPEN debt) | adiabatic via the vev (as designed) | as FIX-C |
| EP for singlet-half transport | lapse factor kept (singlet-half hop) | kept | kept |
| form C (R1-exact) matter lapse | absent (as in hands-ON B; restoring it would re-break SU(2) through the bare-mass dressing, per compose_electroweak) | absent | absent |
| gamma = 1 | metric/EM layers unchanged; not re-measured here | bare lapse k^2 coefficient shifted by 4c/D ~ 2.8e-3 (dressed: EW-BUILDER ~1e-4); not measured | plus 4c'/D ~ 1.2e-4 |
| W mass (L3 Higgs hop) | kept (d cos w = -cW/D) | kept | kept |
| SU(2) covariance | exact | exact | exact |

STAB-B recommendation: adopt FIX-i now as the safe hands-ON default. Treat L2(b) plus FIX-C+ as a NEW LAW (owner decision) candidate, to be decided after its L=6 bang runs and an EP/cone check.

Rows frozen by STAB-B: Tue Nov 10 14:12:42 UTC 2026

## STAB-B addenda (appended as results arrive)

### STAB-B addendum A1 (Tue Nov 10 14:15:27 UTC 2026): R11 complete (FIX-i, L=6, pin2, NUMERIC)
Each run stopped at its 260 s wall budget; none ran away (stop rule: max bits > 200).
| seed | updates reached | max bits | U_mean |
|---|---|---|---|
| S2* 2^16 | 1196 | 29 (em) | -0.036 (slowly accelerating drift) |
| J-pure 2^12 | 1263 | 25 | +0.003 |
| S2* 2^12 | >= 1260 | 22 | -2e-6 |
Files: runs/L6_FIX_S_built_{S2_16,JP_12,S2_12}.json. L=4 corner datum KC:1 under FIX-i: bounded 1500 (12 bits; the corner mode is marginal, not exponential).

### STAB-B addendum A2: R15 route (c) (CUBE-B: F.G with the link-symmetric factor) — PASS / FAIL / OPEN
| R# | claim | label | evidence | EW-BUILDER mark |
|----|-------|-------|----------|-----------------|
| R15 | Route (c), built as sum_links (F_x+F_y)/2 (C - C0) with the per-link balanced composite C = kappa<Phi,U Phi'> - (kappa A/2)(abs(Phi)^2 + abs(Phi')^2) - (kappa v^2/(2A)) abs(U)^2, replacing gwb's norm terms (singlet hop kept). LINEAR SPECTRUM: PASS. C is stationary at the vacuum in every variable, so there is no bilinear at any k (L=6: k=0 1.000000117, corner 1.000000039, other k marginal). AS BUILDABLE: FAIL. The physical N.H dressing needs kappa = kH/(2P) = 2^-11, below the integer grain; the smallest integer-safe kappa = 2 is 4096x too strong, and L=4 S2* 2^16 runs away at t* = 29 (pre-registered <= 300). K0:1 bounded. EP: no vev response, so the fermion clock is not dressed (same debt as FIX-i). OPEN: a finer grain (larger kH or smaller P) and its own L=6 test. | DERIVED + NUMERIC | routec.py; runs/L4_RC2_*.json; NOTES §5 | |

### STAB-B addendum A3 (Tue Nov 10 14:16:34 UTC 2026): FIX-C+ and the form-C alternative
| R# | claim | label | evidence | EW-BUILDER mark |
|----|-------|-------|----------|-----------------|
| R16 | FIX-C+ = FIX-C plus Psi += sum (c'/2)(F_x - F_{x+e})^2, c' = 1,500,000. On the h00 row: self 6 - 6c + 6c', neighbours Q-1-c-c'. Full L=6 reduced Bloch scan, 20/20 k including 0 and the corner: max abs(lambda) = 1.000000042 (marginal). Corner threshold c'_min is between 1.4e6 (1.0026) and 1.5e6. L=4: corner datum bounded 1500; K0:1 bounded >= 1270; S2* 2^16 bounded >= 636 (plain FIX-C ran away at 573). L=6 S2* 2^16: see A4. NEW LAW (owner decision): two lapse counter-terms tied to chi and chi_corner; bare-lapse k^2 coefficient shifted by 4(c+c')/D = 2.9e-3 (dressed change not measured). | DERIVED + NUMERIC | run1.py FIX_CP; runs/a5_FIXCP_L6_all.txt; runs/L4_FIX_CP_*.json | |
| R17 | Answer to the manager's question (3): the form-C alternative is "Bc + L3 Higgs hop" (form C on both doublet members, no gwb). k=0 1.000000117 and corner 1.000000039 (marginal). EP for Dirac matter is R1-exact (form C), and the W mass is kept. But SU(2) is broken at O(U) by the lapse dressing of the bare mass (the reason compose_electroweak removes mlapse/mbeta). Adding the singlet hop on top would dress the singlet half twice, so it is not recommended. L=4 S2* 2^16: see A4. | DERIVED (+ NUMERIC in A4) | run1.py Bc_ehop; runs/a5_Bc_ehop.txt | |

### STAB-B addendum A4 (Tue Nov 10 14:17:59 UTC 2026): R16 and R17 numeric
- FIX-C+ at L=6 (fingerprint 9d11993e…): vacuum fixed for 10 updates; rewind10 exact; R* (r_star_hands_on) 0 mismatches for t=1..10 (S2* 2^16 and J-pure 2^12). File: runs/vf_FIX_CP1500000_L6.json.
- Bc + L3 hop (R17) at L=4, S2* 2^16: bounded to 826 (budget; 32 bits). U_mean drifts strongly: -0.30 at t=820 (form-C control Bc: -0.36 at 1000; FIX-i: -0.074 at 1000). The uniform-lapse drift is generic to the marginal k=0 lapse and is mildest under FIX-i.
- FIX-C+ at L=6, S2* 2^16: running (t=490 at 14:17, 27 bits, U_mean -2.3e-3); final number in A5.

### STAB-B addendum A5 (Tue Nov 10 14:19:03 UTC 2026): R18 amplitude dependence (the brief's S2)
| R# | claim | label | evidence | EW-BUILDER mark |
|----|-------|-------|----------|-----------------|
| R18 | ARM B at L=4: t* = 121 / 186 / 343 for S2* 2^16 / 2^14 / 2^12 (L=6: 132 / 219 / 422). The growth phase is amplitude-independent: U_mean grows x1.138 per update (= the k=0 eigenvalue), taking 53-55 updates from 1e-5 to 1e-2 at every amplitude. The amplitude dependence is entirely the seeding delay: abs(U_mean) first exceeds 1e-6 at t = 10 / 62 / 218. The integer lapse stays at its vacuum (remainder-locked) until the seed's quadratic lapse source passes the grain. Mechanism of the delay's scaling: OPEN. | NUMERIC | runs/L4_B_S2_{16,14,12}.json | |

### STAB-B addendum A6 (Tue Nov 10 14:22:05 UTC 2026): FIX-C+ at L=6, S2* 2^16 (NUMERIC)
- Bounded to t = 1485 (420 s budget; no runaway), max 29 bits (em), metric 17, wsu2 16. Plain FIX-C ran away at L=4 at t* = 573.
- U_mean: -2.5e-3 at 500, -1.9e-2 at 1000, -5.4e-2 at 1485 (FIX-i: -3.6e-2 at 1196). The drift is roughly quadratic in t and is not a linear instability (all k marginal).
- Long-run caveat for FIX-C+ (DERIVED, OPEN): L2(b) has adiabatic thresholds at U = -1/2 and U = +1/4. A quadratic extrapolation reaches U = -1/2 at about t ~ 4500 at L=6. FIX-i has no electroweak threshold at small abs(U).
- FIX-C+ at L=6, J-pure 2^12: running (ends about 14:28); result in A7.

### STAB-B addendum A7 (Tue Nov 10 14:24:46 UTC 2026): FIX-C+ J-pure at L=6; correction to A1
- FIX-C+ at L=6, J-pure 2^12: bounded to 1500 (tmax; 25 bits). U_mean drifts POSITIVE and quadratically: +2.0e-3 at 300, +1.8e-2 at 900, +5.1e-2 at 1500 (about 2.26e-8 t^2). Under FIX-i the same seed has U_mean +0.003 at 1263 (about 17x smaller).
- DERIVED extrapolation: FIX-C+ reaches L2(b)'s U = +1/4 threshold (link radius collapse) at t ~ 3300. Pre-registered as P10 (NOTES); a long run (tmax 4500, budget 380 s) is in progress, result in A8.
- Correction to A1: FIX-i at L=6, S2* 2^12 ran to t = 1500 (tmax), not 1260, with max 23 bits.

## EW-BUILDER marks (appended Tue Nov 10 14:26:17 UTC 2026; append-only; evidence paths are under s18/EW-BUILDER_work/)
### Rows R1–R18
| R# | mark | note | evidence |
|---|---|---|---|
| R1 | AGREE | Not rerun at L = 4. Consistent with my exact k = 0 rate (0.1293 per update) and with EMERGE-N's L = 6 t* = 130. | stab_k0.json |
| R2 | AGREE | k = 0 is reproduced exactly: 1.138057256, eigenvector 98.8 % metric.h00. Hands OFF / Bc / Bng / hop-only / gwb one-way give 1 + 2e−7. Corner: confirmed independently. When the on-site Higgs bilinear is removed at the corner (my link-averaged variant E2, before its counter-term), the corner is 1.0000000283, i.e. the corner channel IS that bilinear. | stab_k0.json, stab_fixplus_lh3.log |
| R3 | CAN'T-CHECK | Not rerun. Consistent with a linear vacuum instability (no matter needed). | — |
| R4 | AGREE | Exact numbers: cF·v = −2^30 = −D/48; 2cL·A = −2^31 = −D/24 per link. F couples only to wsu2.U*_1 and chiral.H_1. χ = gᵀH⁻¹g over {U*_1, P*_1, H_1} = 57389319454720/131321 = 437,015,553.146, so m = 1 + χ/D = 1.00848. | stab_fix.json |
| R5 | AGREE | Same lemma as my S1 theorem. It covers both band edges. The stationary composite of route (c) is not a norm coupling, so it is outside the lemma (consistent with R15). | EW-BUILDER_STAB.md §S1 |
| R6 | AGREE | Including the retraction. With the bilinears kept, the link potential depends on \|U\|² only, −(λ/4)(\|U\|² − s₀(F))². | — |
| R7 | CAN'T-CHECK | Not rerun. Consistent with my k = 0 rates: link group 0.124 per update, Higgs group 0.036, hop group marginal. | stab_k0.json |
| R8 | AGREE | | — |
| R9 | AGREE | Matches my scan: gwb hop part only is marginal (1 + 2e−7). Debt as stated. | stab_k0.json |
| R10, R11 | CAN'T-CHECK | STAB-B numeric; not rerun. | — |
| R12 | AGREE | Plain FIX-C (mine) addresses k = 0 only. I WITHDRAW it as a fix. My first, on-site version was worse: corner 1.1418 (stab_fix.json, rejected 14:04). | stab_fix.json |
| R13 / R16 | AGREE (linear) | c′ check from my algebra, second order, Higgs only, at the corner: c′_min ≈ g_H²/(12(2D − k_H(π))). Here g_H = 2^30 and k_H(π) = 2λ_H v² + 12κH A = 2^35 + 0.75·2^30. So c′_min ≈ 1.415e6, inside STAB-B's bracket (1.4e6, 1.5e6). DERIVED; the exact self-consistent value is not computed. | — |
| R14 | AGREE | | stab_fix.json (corner 1.1418) |
| R15 | AGREE | I derived the same stationary composite independently (message to STAB-B 14:06). It has the same two limits: (i) κH/(2P) = 2^−11 is below the integer grain at v2; (ii) there is no vev response, so the fermion clock gets no factor. OPEN. | — |
| R17 | AGREE | This is my earlier fallback FIX-E. Its O(U) SU(2) breaking is as stated. | — |
| R18 | AGREE (mechanism); CAN'T-CHECK (numbers) | The growth ×1.138 per update is my k = 0 eigenvalue. My 14:05 note had already found that t*'s amplitude dependence is not explained by growth from t = 0; seeding delay is plausible. | stab_k0.json |

### EW-BUILDER rows (E1–E5)
| E# | claim | label | evidence |
|---|---|---|---|
| E1 | k = 0 cause, exact. Spectra: default 1.138057 (γ 0.1293); higgs_hop=False 1.13793; gwb link part only 1.1321 (0.124); gwb Higgs part only 1.0367 (0.0361); hands OFF / chiral only / graviweak OFF / hop only / gwb one-way marginal. The predicted γ matches EMERGE-N's measured late growth (0.129 default, 0.035 Higgs only). | DERIVED + NUMERIC | stab_k0.json, stab_fix.json |
| E2 | FIX-C+ (EW-BUILDER variant: removes the corner channel at its SOURCE, ONE counter-term). (1) gwb's Higgs part couples to the link-averaged lapse F̄(x) = F(x)/2 + (1/12)Σ_nbrs F(y), which equals F at k = 0 and 0 at the corner. Integer u-coefficients need 24 \| cF, so λ_H = 3 in BOTH the chiral Higgs spring and gwb, giving cF = −3·2^12. (2) Link-form counter-term c = ⌈χ/12⌉ = 35,719,425 (χ = 428,633,089.895, residual +10.1). BEFORE the counter-term: k = 0 1.13664, corner 1.0000000283 (marginal). AFTER it: k = 0 1.0000000384. Full L = 6 scan: see the addendum line below. Dynamics NOT RUN (OPEN). Costs: λ_H 4 → 3 (m_H² × 3/4, a chiral-block parameter); one tuned counter-term instead of two; static EP response unchanged at k = 0. | DERIVED + NUMERIC (linear only) | stab_fixplus.py, stab_fixplus_lh3.log/.json |
| E3 | Manager point (3), TUNING. Yes: c = ⌈χ/12⌉ (and c′) are counter-terms tuned to the couplings, like a mass renormalisation. They must be recomputed exactly whenever κH, v, A, λ, λ_H, P or the 2-path regime changes. The builder can compute them deterministically, with no table and no if. Residual margins: FIX-C +2.854 (relative 6.5e−9); my variant +10.1. Unit changes: v and A cannot change by one unit (integrality of cF and cL needs multiples of 2^9). κH ± 1 moves χ by about ∓760 (through cW in the link radial stiffness). So κH − 1 without retuning leaves −757: a slow k = 0 instability, γ ≈ sqrt(2·757/D) ≈ 1.7e−4 per update (e-fold ~5,900). κH + 1 leaves a harmless +763. An explicit margin M (c = ⌈χ/12⌉ + M) buys robustness at the price of a lapse zero-mode frequency ≈ sqrt(24M/D). | DERIVED (estimates) | — |
| E4 | Manager point (2), ONE CONE. Dressed low-k lapse change: plain FIX-C −(χ_H/6)Σ_d(1 − cos k_d), i.e. Δc/c ≈ −χ_H/(4D) ≈ −1.6e−4 (λ_H = 4). STAB-B's FIX-C+ adds the bare −4c′/D ≈ −1.2e−4. My variant gives +χ_H(s − s²), s = ½ + ⅙Σcos k_d, i.e. Δc/c ≈ +1.2e−4 (λ_H = 3). Restoring c_lapse = c_Q to O(1/D) works only when the restoring term pulls the corner INWARD: for my variant, Ψ += (α/2)Σ(F_x − F_y)² with 12α ≈ χ_H leaves a net −χ_H(1 − s)², which is O(k⁴) at small k and inward at the corner (DERIVED, not run). For plain FIX-C / STAB-B's FIX-C+ (slower cone), restoring would push the corner outward, so it is not available. The shared h00 stencil (Q − 1 ports + 6 on site) should not be retuned. Continuum: χ_H/D ∝ λ_H v⁴/(P² D) ∝ 1/Q at fixed v²/Q and P/Q, so the split is a lattice artifact (≈ 2^26/Q here), not a continuum prediction. | DERIVED | — |
| E5 | Manager point (1), CHANNEL (b). I stopped my FIX-C bang runs at 14:11 once R12's corner instability was known (linear, certain). Under FIX-C+ the U_mean trajectories are STAB-B's (A6/A7): quadratic drift, no exponential growth, corner bounded. The sign-definite source (cF, cL < 0) remains in EVERY L2(b) variant, and the marginal uniform lapse double-integrates it. L2(b)'s adiabatic thresholds (U = +1/4, −1/2) are then reached at t ~ 3300–4500 at L = 6 (STAB-B P10). So no L2(b) variant is long-run safe until the gravity sector's uniform-mode drift is fixed (OPEN, B1-GRAV). | DERIVED + (STAB-B NUMERIC) | — |

### EW-BUILDER recommendation
AGREE with STAB-B: adopt **FIX-i NOW** as the hands-ON default, i.e. build_graviweak_b(lam_H = 0, lam_L = 0), keeping the singlet-half hop.
- It is safe: marginal at all k, and bounded in every bang test.
- It is coefficient-level and not a new law.
- Declared debt: the doublet's fermion clock (rest frequency) is not lapse-dressed, and the doublet's mass and the W/Higgs energies do not source the lapse.

**L2(b) + FIX-C+** is a NEW LAW candidate for the owner, after long runs (P10) and after the uniform-lapse drift is fixed. Two versions exist:
- STAB-B: two tuned counter-terms, λ_H = 4;
- mine (E2): the corner channel removed at the source, one counter-term, λ_H = 3.

Route (c) stays OPEN (integer grain).

Route B (the U(2) build): I will build it with the graviweak couplings OFF (FIX-i-like: only the lapse-singlet hop terms), so it does not import this instability.

Signed EW-BUILDER (HAND-M1) Tue Nov 10 14:26:17 UTC 2026

### STAB-B addendum A8 (Tue Nov 10 14:31:13 UTC 2026): P10 result (FIX-C+ long run, L=6, J-pure 2^12)
- Bounded to t = 2563 (380 s budget; no runaway), max 27 bits.
- U_mean: +0.051 at 1500, +0.088 at 2000, +0.114 at 2400, +0.119 at 2563. The drift is DECELERATING and now falls below the quadratic fit (0.149 at 2563).
- So P10 (runaway in [2500, 4500]) is NOT confirmed within the budget. My t ~ 3300 extrapolation, also cited in EW-BUILDER's E5, is not supported by the data so far.
- Whether the uniform lapse saturates or oscillates below the L2(b) threshold (U = +1/4) is OPEN. The run is deterministic: on its overlap with the 1500-update run it is identical in U_mean and in bits.

## STAB-B signature
STAB-B has read EW-BUILDER's marks (appended 14:26:17): AGREE on every row they could check, CAN'T-CHECK on the rows that depend on my runs (R3, R7, R10, R11), FIX-C withdrawn, and the same recommendation.
I accept EW-BUILDER's E1–E4 as their DERIVED claims, not re-derived by me. E2 (their one-counter-term FIX-C+ with lam_H = 3) has only linear checks; its dynamics are not run (OPEN).
I amend E5's t ~ 3300–4500 by A8: bounded to 2563 and decelerating.

Joint result:
- CAUSE: gwb's norm bilinears destabilise the band-edge lapse modes (k = 0: +1.138; corner: -1.026). THEOREM + DERIVED + NUMERIC.
- FIX NOW: FIX-i, i.e. build_graviweak_b(lam_H = 0, lam_L = 0). It is legal, needs no new law, and passed every check (A1, R10).
- NEW LAW candidate: L2(b) + FIX-C+, for the owner decision.
- OPEN: the EP debt of FIX-i; the uniform-lapse drift; FIX-C+ in the long run.

Signed STAB-B Tue Nov 10 14:31:13 UTC 2026

### EW-BUILDER addendum (Tue Nov 10 14:32:00 UTC 2026): E2 full L = 6 scan (NUMERIC, linear)
- FIX-C+ (EW-BUILDER variant): link-averaged Higgs–lapse coupling, λ_H = 3, one counter-term c = 35,719,425.
- Over all 20 reduced L = 6 k (k = 0 and the corner included): max |λ| = 1.0000000423.
  - The worst k is (0, 0, 1), and its eigenvector is the su3/su2 gauge layers' marginal Jordan pairs, not the lapse.
  - k = 0: 1.0000000395.
  - So the variant is marginal at every k checked.
- Dynamics (bang seeds, vacuum, rewind, R*) were NOT run: OPEN.
- File: EW-BUILDER_work/stab_fixplus_lh3.json.
- Methods note (my error): until 14:31 my numpy eigen-solves ran with multi-threaded BLAS (up to ~1.8 cores). From 14:31 they are pinned with OPENBLAS/OMP/MKL_NUM_THREADS=1. Results are unaffected.

Signed EW-BUILDER (HAND-M1) Tue Nov 10 14:32:00 UTC 2026
