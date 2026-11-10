# AGREE_M2_column — S2-M2's verdict column for AGREE_M.md (for S2-M to merge; S2-M2 does not edit AGREE_M.md)

Written at 03:45 UTC (`date -u`). Every verdict is backed by S2-M2's own derivation or code in s2/M2_*. "Re-derived"
means S2-M2 reproduced the claim independently. The numbering follows AGREE_M.md.

| # | M2 verdict | M2 evidence |
|---|---|---|
| C1 | AGREED (re-derived) | M2_FINDINGS C6. Same proof via z_i = ⟨ψ,U_iψ⟩. Grid max 0.577350 (M2_vg.log) |
| C2 | AGREED (re-derived) | M2 C4. Massless ⇔ common eigenvector, and then exactly the SC scalar band |
| C3 | AGREED (EXHAUSTIVE re-derived) | M2_spec0.log, joint eigenspaces of all eigenvalue triples |
| C4 | AGREED (re-derived) | M2_scalar_exact.py: engine == 6-face scalar Rule3, bit for bit |
| C5 | AGREED (re-derived) | M2_spec0.log, M2_vg2.log (non-scalar range ±(1+√17)), M2_massive2.log |
| C6 | AGREED (re-derived) | M2 C6 |
| C7 | AGREED (re-derived; exact rationals) | M2_stencil.log. The sextic agrees with the H6 form (M2_decisive1.log) |
| C8 | AGREED. Exact-CA front checked; the [111] hard-edge constant was not re-derived | M2_front_scaling.json, M2_static_green.log |
| C9, C10, C11 | AGREED (re-derived) | M2 C7, C9–C11 |
| C13, C14, C15, C16 | AGREED (re-derived; C15 from the repo theorem) | M2 C9–C11 |
| C17 | AGREED (proof read and accepted) | — |
| C18 | AGREED. Gram eigenvalues (2, ½, ½) checked | — |
| C19, C21 | AGREED (re-derived, identical weights 2:1, 8:1, 16:4:1, 16:8:2:1) | M2_stencil.log |
| C20 | AGREED. The mod-4 argument was re-derived; the box search was not re-run | — |
| C22 | AGREED. Superseded by M2 C14 (no band constant on any sphere) | M2 C14 proof |
| C23 | AGREED (CONJECTURE) | M2 C8 |
| C24 | AGREED after re-check (M2's correction adopted) | M2_decisive1.log |
| C25 | AGREED with the support-function wording | M2_vg2.log |
| C26, C27, C28, C29 | AGREED. C27's proof was checked | M2 C15–C17 |
| C30 | AGREED. M2 yields: 12 ports for any vacuum, 14 with the reference vacuum | — |
| **C31** | **AGREED in substance.** Routing makes the k⁴ coefficient non-universal: my EFF axial scan gives a K4 coefficient range of [−0.0185, +0.0556]. The toy value −1/24 was not re-derived | M2_routing_check.log |
| C32, C33 | AGREED (re-derived; shear census checked) | M2 C18, M2_shear_check.log |
| C34 | AGREED (re-derived independently) | M2_routing_check.log, M2_routing_doublers.log |
| **Q1–Q4** | **AGREED explicitly.** Same answers as M2_FINDINGS §6b | — |
| C35 | AGREED (re-derived: √3 for w = 1, √2 for w = 2, 3) | M2_c35c36_check.log |
| C36 | AGREED (own instance: Floquet radius 1+√2) | M2_c35c36_check.log |
| C36b | Not re-derived and not disputed; moot under ADDENDUM 4 | — |
| C37 | AGREED (from C27; scope: large-amplitude free light) | — |
| C38 | AGREED (all four valleys reproduced), plus M2's addition on the Compton length (~1 node) | M2_massive2.log |
| **C39** | **AGREED.** M = 6I − L with 0 ≤ L ≤ 12 (Gershgorin), so the spectrum lies in [−6, 6] and the constant vector sits at 6. Numerically, for 20 random weight fields on L=6, the spectrum lies in [−1.40, 6.00]. Isotropy: leading order only if w_xy is direction-blind (e.g. N_xN_y). Departures: on-site entries (AGENTS item 8), non-unit weights (a divisor or channel census), and a bilinear coupling for sourcing. These are NOT tensor-only, so they are outside ADDENDUM 4. The roundness of the light cone (C1) is not covered, because the hops are not unitary; I mark it "not re-proved". | M2_c39_eff4.log |
| REV | AGREED (union with s0/REVIEW_S2M2.md) | — |
| M2-C12, M2-C13b-check, M2-C20-shear | (M2's own claims) holds | — |
| C40 | holds (M2's proposal). EXHAUSTIVE context, see the row below | M2_Wscan.log |
| **C40b (new, EXHAUSTIVE)** | Over all 61,440 covariant tables, dim W (massless space) is: 0 for 30,480 tables; 1 for 19,200; 2 for 2,304; 4 for 768; 6 for 3,072; 8 for 608; 12 for 2,304; 16 for 48; 24 for 1,792; 48 for 864. Tables with dim W > 1 do exist. By C4 every massless state is an exact SC scalar wave, and by C27/C37 it is inert to load. So a larger W gives more copies of light, not a dynamical metric. The irrep content of W > 1 is not yet classified | M2_Wscan.py / .log / .json |
| **C40c (new, EXHAUSTIVE)** | massless multiplets at Γ/R over all 61,440 tables (`M2_Wirrep.py`): E, T1, T2 occur (A1+E 288, T1 288, T2 288, A1+T2 192, A1+E+T1+2T2 48, whole non-spinorial regular rep 6); +++ only A1. By C2/C4 they are exact SC scalar waves, and by C27/C37 they are inert, so they are tensor-labelled light copies, not a metric | M2_Wirrep.log/.json |
| ADD4 | AGREED. D3Q19 with divisor 24 is non-compliant with ADDENDUM 4 (it stays compliant with ADDENDUM 2) | — |
| X-S1 | No verdict from S2-M2 (cross-study; not checked) | — |
| **DEMO** | **AGREED, with one number to reconcile.** In my own EFF executor (M2_eff_demo.py, 24 channels = z=+1 sector, the light eigenvector as initial data), reciprocity, the vacuum fixed point and the exact inverse over 25 steps all hold bit for bit. The equal-\|k\| = π/4 splitting is **8.776e-4 (EFF) against 1.573e-2 (reference): 17.9×**. The linear Bloch prediction is also 8.7760e-4, for all four K4-free axial choices. S2-M's 8.6e-4 differs by 2%. My guess is that channel-uniform initial data mix in massive components; please quote the exact value | M2_eff_demo.json, M2_c39_eff4.log |
| **REC** | **REC: AGREED (J1–J5)**, S2-M's joint proposal of 03:46, with two notes. (J2) The demo number: my exact executor and the linear Bloch prediction both give 8.776e-4 against 1.573e-2 (**17.9×**); S2-M's "8.6e-4 (18×)" agrees to 2%, and the linear value should be quoted. (J4) S1-M's T18 and the "two bilinear blocks" refinement were not checked by M2; C37, C39 and C40 were. J3 replaces M2's R4 claim of compatibility with the clutch and face waits: M2 confirms by its own check that waits and holds acting on free waves are unstable (C35, C36), and they are gates (ADDENDUM 4). | RECOMMENDATION_M2.md (v2), M2_c35c36_check.log |
| D3Q19 assessment | AGREED with S2-M: non-compliant with ADDENDUM 4 | — |
