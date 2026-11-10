# AGREE_P — Study 5 twin physicists: S5-P (local) | S5-P2R (remote, relayed by the manager)
FINAL v7 by S5-P, 07:12–07:43 UTC 2026-11-10 (`date -u`). S5-P2R's columns are quoted from s5/P2R_INTERIM.md (relayed 06:48,
06:52, 07:03, 07:04) the manager's relays of 07:11, 07:21 and 07:28 (F7), and P2R's sections of 07:30–07:31. Codes: S5-P = s5/P_*.py, pre-registered in s5/P_NOTES.md. S5-P2R = /tmp/u24_s5/*.py (remote).
Verdicts:
- AGREE: same claim, same numbers or the same exact fractions.
- AGREE (geometry): same claim, with numbers that differ only by a declared setup difference.
- SINGLE: one twin only; needs a twin run or is accepted on one code.
- DIFFER: with a diagnosis.

## A. M2-1 — shared-token |ψ|² router (MECHANISM TEST; both EXHAUSTIVE over the token)
| claim | S5-P | S5-P2R | verdict | diagnosis |
|---|---|---|---|---|
| P(d+) = 1, 3/4, 1/4, 0, 1/4, 3/4 for s = 0..5; P(both) = P(none) = 0; A = 1, 2, 3, 10 | PASS, exact | PASS, exact (A = 10: 600/800, 200/800) | AGREE | — |
| I± static, I+ + I− = D = 8A², I± = (8,0),(6,2),(2,6),(0,8),(2,6),(6,2)·A² | PASS (implied exactly by E4's count formula over 24 updates) | PASS (12 updates) | AGREE | — |
| E1 independent tokens: α = P(both)/(P+P−) = 1; shared token α = 0 | α = 1 exactly (P(both) = P(none) = 3/16, A = 1, 2, 3) | α = 1 exactly; shared 0 | AGREE | the board's Grangier–Roger–Aspect test: α = 0 needs the SHARED (mirror) token |
| E2 global lag t0: counts unchanged | PASS | PASS | AGREE | — |
| E3 rank-2 homodyne fails E2 | FAILS E2 (A = 1, s = 0: P+ = 1, 1, 1/2, 0, 0, 1/2; s = 3: 1/2 each) | FAILS E2 (A = 1, s = 0: 8, 8, 4, 0, 0, 4 of 8; s = 3: 4 each) | AGREE, identical fractions | different scalings of the same rank-2 form |
| E4 long exposure: first click exclusive + Born; then BOTH keep clicking at I±/D | PASS (A = 1, 3, T = 24; N± = ⌊(r± + T·I±)/D⌋ exact) | PASS (A = 2, T = 60) | AGREE | the board does not use the wave up: no collapse |
| E5 exact rewind (every λ) | PASS | PASS | AGREE | — |
| E6 what the choice click records | kind = handedness of δ = I_own mod D: C0 at the certain outcomes (s = 0, 3), C2 for the LIKELY detector, C1 for the unlikely one | clicking detector Δr = I_own − D = −I_other; silent detector Δr = +I_own | AGREE (the same Δr) | δ = −I_other lies in (−D/2, 0) iff I_own > D/2 (C2), and maps to I_own ∈ (0, D/2) iff I_own < D/2 (C1); δ = 0 at I_own = D (C0). P2R left kinds "undefined" for D = 8A²; the taxonomy's handedness kind is defined for every D |
| E6 time mirror of the router | JR = (−b,−a,r) is NOT a reversor (quadratic K), 0/12; M = (b,a,D−1−r) and J_arm∘M ARE, 12/12; the mirrored log = reversed, with the SAME detector sizes and kinds | (c3, reference board) the repo's time_reverse returns exactly and PRESERVES kinds (Φ_JR = +Φ) | AGREE | manager's derivation (07:10): R-type reversals keep δ (kinds R-even); JR swaps them only where K is odd in b (linear board). With rank-3 detectors only R-type reversals exist, so the choice kinds are mirror-EVEN. K2's "C1 ↔ C2" is a J-property, not a time-arrow property |
| E7 three exits: no local token rule is exclusive + exhaustive + Born | best ONE fixed offset fails 5/27 of (phase cell, token) pairs (A = 1, D = 18, 36 cells); zero failures need c2 = I3 (non-local) | EXHAUSTIVE: 0 solutions for D = 2, 3, 4 (64 / 19,683 / 65,536 maps); two-exit control D! | AGREE | S5-M2's measure theorem confirmed two ways |
| board-made token T4 (staged DC gear): λ uniform over birth times, one click, P(+) = I+/D | PASS (D = 8, 72; even form K → 2K, D → 2D) | not run | SINGLE (S5-P) | S5-M2's m2_token.py uses ODD K (5, 27, 9); the even form gives the same fractions |
| unstaged token: born at vacuum, exposed from t = 0 | exactly ONE click at EVERY update; P(+) = I+/D over readout times; r+ = r− always; rewind exact | not run | SINGLE (S5-P) | a sigma-delta (time-ensemble) Born rule; the token is the detectors' own remainder phase |
| token kinds (opposite-sign form, equal remainders) | BOTH updates share one kind: (C2,C2) for I+ > D/2, (C1,C1) for I+ < D/2, (C0,C0) at D/2. The manager's (C2,C1) holds only for the MIRROR form (confirmed there) | not run | SINGLE (S5-P); corrects the manager's prediction for this form | K+ − K− = D with r+ = r−, so δ+ ≡ δ− (mod D) |
| T5 tuning S ≠ D | P(both) = max(0,S−D)/D, P(none) = max(0,D−S)/D, exact in 6/6 rows; Born conditional on detection iff S ≤ D ((27,9): 3/4; (54,30): 7/10 vs 9/14) | not run | SINGLE (S5-P) | — |

## B. Demo (a) — two-path interference, which-path clocks
| claim | S5-P | S5-P2R | verdict | diagnosis |
|---|---|---|---|---|
| no detector, A = 1e4: V_event = V_click(ℓ²) | 0.964 / 0.964 (Fourier 0.827 / 0.822) | 0.951 / 0.950 (Fourier 0.785) | AGREE (geometry) | the same identity ℓ = b(t+1) + b(t−1). My board is the 256² z-uniform cube (one side length); P2R's is 256 × 128 (packets 15 sites from the y-boundary) |
| click counts flat at large A; kinds show no fringes | V_count 0.03; kinds ≈ 1/3 each | flat; no fringes in kinds | AGREE | every node clicks every update |
| small A (≤ 3): no fringes even without a detector | Fourier event 0.09 / 0.11 / 0.03 at A = 1 / 2 / 3 | Fourier ≈ 0.06 at A = 3, 1.5 | AGREE | quantization: the joint − p1 − p2 deviation is ≈ 6 units rms at EVERY A (√T/3) |
| amplitude window (S5-M a1) | A* ≈ 12; 1 − F/F∞ ≈ 6/A for A ≥ 30 | — | SINGLE (S5-P) | — |
| linear (spring, rank-2) detector: deterministic loss, ensemble = single run, record independent of the microstate | twin run (P_spring.log): single-run V the same for 7 microstates (spread ≤ 0.0007), ensemble = single, V_click(ℓ²) = V_event, rewind exact; V = 0.527 / 0.687 / 0.617 for 125 / 1025 / 2025 nodes (path-2 energy 0.991 / 0.843 / 0.818) | 0.966 / 0.504 / 0.354 for 125 / 1025 / 3025 nodes, same in every single run | AGREE (claims); DIFFER (numbers, geometry) | linearity (S5-M): ensemble = single. The V numbers depend on the patch shape: my thin 5×25 strip spans the beam and acts as a phase-step plate (V 0.53 at 99 % energy). Not monotonic in size |
| rank-3 couplings at the reference light's zero headroom blow up | rank-3 parametric 2g·b_W·b_S: max\|b\| 1.4e8 (g = 1), 7e12 (g = 2), int64 guard (g = g' = 1) | plain / asymmetric couplings blew up | AGREE | k = 0 band edge cos ω = 1 has no headroom (G6 family); a stable detector needs a sign-definite modulation (rank 4, D4) or a symmetric spring |
| ensemble decoherence needs a hidden-phase-dependent SHIFT; sorting by the detector restores it | rank-4 parametric: single F 0.756, ensemble 0.652 = F_single·\|⟨e^{iβ}⟩\| (0.654); sorting by W's 8 click logs restores 0.756 exactly; g = 2: 0.620 → 0.298 → 0.620 | M2-2 (Q_W = 5, A = 1, N = 6): V_single 0.903, V_ens 0.262, V_eraser(ALL W) 0.911, one W 0.575 | AGREE (different mechanisms, same law) | classical dephasing; information is MOVED into the detector clocks (rewind exact in both) |
| record and back-action are independent knobs; Englert V² + D² ≤ 1 fails | (g,g') = (0,1): V unchanged, D = 1; (1,0): dephasing, D = 0; (1,1): both | — | SINGLE (S5-P) | deterministic integer records are perfectly distinguishable |
| ALL-OR-NOTHING at amplitude ~1 (S5-M a2: exact light + primed nonlinear detector) | CONFIRMED exactly: 80/120 hidden r_W never fire, light bit-identical; 40/120 fire (all C1) and change the light by ≥ 4 units | EXHAUSTIVE in P2R's router detector (A = 1, 2; N = 1, 2): R = 0 ⇒ bit-identical (108/108, 1944/1944, 36/36, 216/216); R = 1 ⇒ changed by ≥ 2 units | AGREE | r26 T8: in the reference alone exact light is transparent (unmarkable); my M2-2c twin shows it again (silent W: undisturbed fringe) |
| small-A detector: counts lose more than the board | V_count 0.57–0.97 vs V_event 0.87–1.00 (disturbed runs); shift ≤ 0.017 rad; eraser only back to the single-run level | — | SINGLE (S5-P) | dark sites click with \|ℓ\| = 1: a readout weighting, not dephasing |
| N_c ∝ A² (W gears needed for decoherence grow with A) | — | V_ens(N = 6) = 0.262 / 0.921 / 1.00 at A = 1 / 2 / 3 | SINGLE (S5-P2R) | — |
| M2-2c conditional exits (A = 1, Q_W = 5, τ = 6, N = 1): unconditioned 9/10, 3/4, 7/20, 1/10, 1/4, 13/20; on record (0,1,0,0,0,−1): 1/2, 3/4, 3/4, 1/2, 1/4, 1/4 (QM 1/2) | EXACT the same fractions, with s → 6−s (my arm 2 is advanced, P2R's lagged; W on arm-1 gear 0); the silent-W record (864/1440) keeps the undisturbed fringe 1, 3/4, 1/4, 0, 1/4, 3/4 | as stated | AGREE (two codes; lag sign convention) | another board-vs-QM signature: conditioning on the which-path record keeps s-dependent fringes |

## C. Demos (b) and (c)
| claim | S5-P | S5-P2R | verdict | diagnosis |
|---|---|---|---|---|
| b1 independent board-clock settings: max\|S\| = 2 | 2 exactly (12⁴ quadruples; standing pulse split into conjugate halves; passive click-size homodyne) | 2.000 exactly (12⁴) | AGREE | K1 |
| b E(δ): cusp at 0 (sawtooth), not cos | near-linear steps, L∞ 0.111 to the triangle vs 0.311 to cos; E depends on θa + θb (conjugate halves) | cusp; constant offset from φ alone | AGREE | different outcome maps, same family; the board's affine clock readouts give sawtooth E |
| b2 common past: \|S\| > 2, beyond Tsirelson | max 97/30 = 3.233, counts (2,15,15,4), ΣTV = 3.0, I = 1.64 bits | 2.67 / 3.50 / 3.67 (AMP A / 2A / 4A), unequal counts | AGREE (in substance) | measurement dependence; the value is tuned by the mechanism, with no preference for 2√2 |
| b3 every \|S\| > 2 has TV > 0; S ≤ 2 + 2ΣTV | 64/120 offset cells \|S\| > 2, all TV > 0, bound holds in all | 3328 / 3112 violating mechanisms, all TV > 0, bound holds | AGREE | — |
| b4 / T14 settings independent of the token ⇒ \|S\| ≤ 2 | T14 with remainder clocks: max\|S\| = 2 iff gcd(lcm(Pa,Pb), D) = 1, else 4 (20/20 rows) | b4 fresh settings TV = 0: max 2.000 | AGREE | CRT: coprime periods = measurement independence on the board |
| M2-3 S tuned, not produced (fixed marginals, mechanism changed) | — | S = 1.33–4.00 | SINGLE (S5-P2R) | — |
| c handshake: no emitter-C1 ↔ absorber-C2 pairing | twin run (P_hand.log): H = −144 of 16,750 pairs (z ≈ −1.6) at A_E = 1e4; +80 of 9,392 (z ≈ +1.2) at A_E = 20; per-seed max \|z\| 2.6 / 2.1 over 32 cells; the mirror identity N_JR(A→E; k̄) = N(E→A; k) EXACT 16/16, H_JR = H | \|z\| ≤ 1.2, asymmetry ≈ 0 | AGREE | the kind classes 'C1 then C2' and 'C2 then C1' are each mirror-invariant (THEOREM E25); no handshake selection |
| c3 the repo's time_reverse R keeps kinds and quotients; JR flips them; Φ is no arrow | official engine, 3 cases: R and JR return exactly; R-log reversed with the SAME kinds/q; JR-log with C1 ↔ C2, q → −q; Φ (fwd, R, JR) = (0,0,0), (−15,−15,+15), (−33,−33,+33) | Φ_JR(repo R) = +Φ: 0/0, −109/−109, +46/+46 | AGREE | manager 07:10: kinds R-even, J-odd; K2's swap is a JR (J) property |
| c3 the arrow is in the record footprint | random seed: F_fwd 119 → 296 vs F_R 182 → 296 (forward activity grows); a small impulse that goes dark reverses the order | spreading impulse 6 → 14311 vs 9604 → 14311 | AGREE (case-dependent) | the footprint arrow follows spreading; it is not a kind statistic |

## D. Twin checks of the mathematicians' reference codes (two codes)
| claim | S5-P (own code) | reference | verdict |
|---|---|---|---|
| D12b decisive toy: c = 1 gives P(+\|s) = 1/2 flat, P(+\|s, W1) = 1,1,1,0, I(s; exit) 0.5 → 0, I(s; exit, record) = 0.8113 | EXACT, A = 1, 2, 3, as Rule3 gears with a shared token and even K (P_dec.py); the literal 90° kick is possible because my arms are period-4 clocks | S5-M2 m2_dec_toy.py; P2R could NOT do 90° (period-6 arms: a 60° quantum) and did M2-2c instead | AGREE with S5-M2 (two codes); P2R's M2-2c is the 60° analogue (section B) |
| travelling router (m2_fibre): one click per pulse for every λ, P(+) = 1, 3/4, 17/64, 1/32, 17/64, 23/32 (ncyc 8) | EXACT, same fractions; rewind exact; d+ C1 / d− C2 | S5-M2 m2_fibre.py | AGREE (two codes) |
| D3 reciprocal back-action (m2_fibre_recip_diag): w = 2 gives 3 clicks at (s,λ) = (3,40); w = 6 gives 30–40 clicks, \|b\| ≤ 6 | EXACT on those trajectories (P_fibre_recip.py); ensemble: exactly-one only 1/24–23/48, and some tokens BLOW UP (up to 7/48 per phase at w = 2) | S5-M2 | AGREE (two codes) + S5-P adds the instability |
| T14 CRT measurement independence | 20/20 rows (remainder clocks) | S5-M2 m2_crt_bell.py | AGREE (two codes) |
| T4 board-made token; T5 tuning | EXACT (even form) | S5-M2 m2_token.py (odd K; rewritten in the even form 07:17) | AGREE (two codes, even form) |

## E. F7 — the owner's light-cone choice (TOP PRIORITY, 07:28)
| claim | S5-P (genuine C0 fibres, P_f7.py / P_f7b.py) | S5-P2R (f7.py buffer; f7b.py genuine fibres, 07:30; f7c.py readers, 07:31) | verdict | diagnosis |
|---|---|---|---|---|
| TIMELIKE: E(δ) = cos(a − b) exactly on the 60° grid | EXACT: 1, 1/2, −1/2, −1, −1/2, 1/2 (d = 6); at d = 5 the same law with the fixed light-travel phase 300° (a relabeling of Bob's setting) | EXACT: 1, 1/2, −1/2, −1, −1/2, 1/2 | AGREE | the buffer and the genuine fibre give the same law; the fibre adds only the transport phase d × 60° |
| timelike max S on the 60° grid = 5/2 | 5/2 | 5/2 at (0°, 60°, 0°, 120°) | AGREE | the cos-CHSH grid maximum |
| SPACELIKE, front-only reader | E = 0, S = 0 | E = 0, S = 0 | AGREE | — |
| SPACELIKE, photon-copy reader (S5-M2) | E = cos/2, S = 5/4 | E = cos/2, S = 5/4 exactly (f7c.py, exhaustive) | AGREE (three codes, with S5-M2) | a local hidden-variable reader |
| Bob's wait | 6 updates = 1 period of his clock (d = 5, staged imprint: 0 set-up updates); 7 at d = 6 | 6 (buffer, d = 5); 9 with genuine fibres = 1 (click) + 2 (two-update front set-up) + 6 (transit, d = 6) | AGREE | wait = click + front set-up + d/c in both codes; P2R's window statement: S = 5/2 iff W ≥ 9, else 0 |
| a designed (bit-gate) reader of the same front: S = 4 | 4 (decodes (o_A, a) within a setting pair not 180° apart) | 4 | AGREE | the quantum cap comes from the Born reader, not the cone |
| 90° grid | timelike E = cos exactly (1, 0, −1, 0); max S = 2; R1 0, R2 1, bit gate 4 | (P2R: 60° only) | SINGLE (S5-P) | no 45° clock exists (2cos 45° is irrational), so no exact grid violates on 90° |
| transport by a genuine Rule3 fibre | exact, all C0, rewind exact; open ends reflect after 2 updates, so lines are extended | f7b.py: 3 exact C0 fibres of length 30, reflection after Bob's readout; cos exact, 5/2, spacelike 0 | AGREE (both genuine) | the buffer simplification is removed in both codes |
| Alice's exposure without staging (photon-gated rank-3 input 2Σ b_ph(b_ph ± b_a)) | 0 clicks before arrival; first click exclusive; timelike cos exact, S = 5/2; spacelike 0 (P_f7b.py) | one-update exposure | S5-P adds | — |
| front creation on the board | staged bilinear imprint (declared) | declared two-update bilinear kick k0 = 6q·c_j(t+1), k1 = 6q·(c_j(t+2) − c_j(t+1)) from the OLD (a,b) of Alice's setting gear (exactly reversible) | COMPLEMENTARY | between the two codes every F7 step now has a Rule3 realisation: S5-P's photon-gated exposure plus P2R's front kick. P2R's kick reads an a (two-time), which is allowed by the staged inverse (acyclic a-reads) |

## F. M2-2 twin (P_m22.py)
| claim | S5-P | S5-P2R | verdict | diagnosis |
|---|---|---|---|---|
| N = 1 (A = 1, Q_W = 5, τ = 6): V_ens / V_single / V_eraser | 0.808 / 0.915 / 0.915 (exhaustive) | 0.808 / 0.915 / 0.915 | AGREE (two codes) | — |
| N = 2 / 3 / 6 V_ens | with P2R's exact definitions (P_m22_p2r.py: '+' = d+ alone with ℓ == 1; arm 2 lagged; seed-1 sampling for N ≥ 3): 0.833 / 0.650 / 0.262; my first definitions gave 0.678 / 0.547 / 0.331 | 0.833 / 0.650 / 0.262 | AGREE (two codes, exact) | the earlier DIFFER was definitional only; V_single at N = 6 = 0.903 when undefined per-configuration V's (c0 = 0, 169/2000) count as 0 (P2R's convention), 0.986 when skipped |
| decoherence fades with A (N = 6) | V_ens 0.33 / 0.78 / 0.91 / 0.97 / 0.98 for A = 1 / 2 / 3 / 5 / 10 | 0.262 / 0.921 / 1.00 / 1.04 / 1.02 | AGREE (trend) | N_c grows with A |

## Decisive tests (S5-P's reading, 07:40)
1. Choice with Born frequencies on TWO exits needs one of three things:
   - a shared mirror token (λ, D−1−λ);
   - equal remainders with opposite inputs;
   - or the detectors' own remainder phase in time (unstaged).
   It is local, exact and reversible, and the token decides (hidden variable). AGREE (A, E1, E7).
2. Three or more exits: no local token rule (AGREE: exhaustive D ≤ 4, numeric 5/27).
3. Apparent collapse = classical dephasing by hidden detector phases.
   - It is the same in click space and on the board, and sorting by the detector's clicks undoes it.
   - Single runs keep (shifted) fringes.
   - Linear detectors cannot dephase (ensemble = single).
   - AGREE (rank-4 parametric for S5-P, M2-2 nonlinear W for P2R, spring for both).
4. At amplitude ~1 a detector acts all-or-nothing, decided by its hidden remainder. AGREE (S5-P exact light 80/120 vs 40/120;
   P2R exhaustive in the router; S5-P's M2-2c twin: the silent-W record keeps the undisturbed fringe).
5. BOARD vs QM: conditioned on the which-path record, the board's exit still depends on the phase s. QM gives 1/2 flat and
   0 bits.
   - D12b 90°: P(+|s, W1) = 1, 1, 1, 0 and 0.8113 bits; S5-P and S5-M2 in two codes.
   - The 60° analogue M2-2c: P2R and S5-P in two codes, the same fractions.
   - With no kick, fringes survive a perfect record (V = D = 1).
   - AGREE.
6. Bell: |S| ≤ 2 whenever the settings are independent of the token (CRT-coprime clocks). Beyond 2 only with measurement
   dependence (TV > 0), tuned up to 4, with a sawtooth E (cusp), not cos. AGREE.
7. Time mirror: the repo's R keeps kinds and JR flips them, so kinds carry no arrow. No handshake pairing; the mirror
   identity is exact. AGREE.
8. F7 (the owner's light-cone choice): a Born reader of the choice front gives cos(a − b) EXACTLY for timelike readout
   (S = 5/2 on the 60° grid). Spacelike readers get 0 or 5/4; a bit gate on the same front gets 4. AGREE (S5-P with
   genuine C0 fibres, P2R with a buffer, S5-M2's theorem).

## Open (not twinned)
- S5-P only:
  - T5 tuning;
  - the token kinds in the opposite-sign form;
  - the a2 count-vs-board readout split;
  - the rank-3 parametric blow-up magnitudes;
  - c2 influence fractions.
- P2R only:
  - N_c ∝ A²;
  - M2-3 mechanism invariance;
  - the product law (PARTIAL).
- RESOLVED at 07:41: M2-2 at N ≥ 2 now agrees exactly with P2R's definitions (V_ens 0.833 / 0.650 / 0.262; V_single 0.903
  at N = 6). The difference was definitional.
- S5-P only, newest:
  - F7 with Alice de-staged (photon-gated router);
  - the D3 ensemble instability (blow-ups);
  - the 90° F7 grid.
- Numbers that differ by geometry (claims agree): the spring-detector V's (mine 0.53 / 0.69 / 0.62, P2R 0.97 / 0.50 / 0.35);
  V at A = 1e4 (0.964 vs 0.951).
