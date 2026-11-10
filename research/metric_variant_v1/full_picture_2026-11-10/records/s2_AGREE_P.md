# AGREE_P — twin agreement S2-P (local) ↔ S2-P2R (remote, relayed by the manager)

Written by S2-P at 04:31 UTC (`date -u`) from s2/P2R_FINDINGS.md (S2-P2R interim, received by the manager 03:57) and
s2/P_FINDINGS.md. Never edits the twin's files. Verdicts: **AGREED** (same number within the stated tolerance or after
an identified convention), **AGREED-QUAL** (same verdict, numbers differ by an identified set-up difference),
**OPEN** (needs the twin's confirmation of a definition; decisive test named). Nothing is left "unresolved".
STATUS 04:44 UTC: all 23 rows AGREED or AGREED-QUAL; no OPEN items (twin's table s2/P2R_AGREE.md: C1–C23 AGREED,
C24 not checked; no DISAGREE).

## 0. Conventions reconciled
- **Offset convention.** S2-P2R uses offset = t + 1 − r√3 (τ = t+1); S2-P uses t − r√3. Removing the +1:
  [100] peak offsets are IDENTICAL at r = 50/100/200/400 (S2-P2R 2.51/3.35/4.31/5.55 − 1 = 1.51/2.35/3.31/4.55 =
  S2-P 1.51/2.35/3.31/4.55). Threshold offsets differ by 0.03–0.31 update, shrinking with r (interpolation of the
  threshold crossing on the parity grid; S2-P interpolates linearly between allowed steps).
- **Front read-out.** S2-P: first local maximum of |b| (channel norm) on the site's parity steps that is ≥ 25% of the
  site's global maximum; thresholds = fractions of that peak. Global-max read-outs differ on [110] (late ringing peak;
  P_alt_readout.json lists both); all comparisons below use the first-peak convention.

## 1. Claim table
| # | claim | S2-P | S2-P2R | verdict | note / resolution |
|---|---|---|---|---|---|
| 1 | [100] offsets r = 50/100/200/400, peak/10%/1% (t − r√3) | +1.51/−6.13/−9.96; +2.35/−7.17/−12.15; +3.31/−8.75/−14.88; +4.55/−10.67/−18.46 | (−1 applied) +1.51/−5.96/−9.65; +2.35/−7.14/−11.90; +3.31/−8.68/−14.75; +4.55/−10.62/−18.34 | AGREED | peak exact; thresholds ≤ 0.31 (r = 50) → ≤ 0.12 (r = 400): interpolation convention |
| 2 | [110] offsets r = 200/400 | +1.80/−5.74/−9.49; +2.49/−6.96/−11.90 | +1.83/−5.57/−9.34; +2.48/−6.86/−11.68 | AGREED | ≤ 0.22 update |
| 3 | equal-s(n) fronts [110]/[211]/[321] | 1% at r = 200: −9.49/−9.52/−9.49 | coincide to ≤ 0.17 at r = 400 | AGREED | |
| 4 | [111] hard edge at t = r√3 = |x|₁ | yes, every threshold | yes | AGREED | |
| 5 | relative anisotropy ∝ r^(−2/3) | local exponent r = 300→400: −0.70 (10%), −0.70 (1%); −0.54 (peak) | −0.70/−0.69/−0.69; peak value at r = 400 +0.656% | AGREED (closed 04:44: same peak value, +0.657% mine) | if S2-P2R's three numbers include the peak, the peak differs by definition: S2-P's peak offset has a constant term (a ≈ −1.1…−1.4 in t − r√3 = a + b r^(1/3)) that makes the local exponent −0.54 at r ≤ 400; decisive test: δ_peak(r) = (t_pk,100 − r√3)/(r√3) at r = 200/300/400 — S2-P: 0.00955/0.00768/0.00657 |
| 6 | S2 exact normal modes (10 periods, L = 60) | all = cos ω = (1/3)Σcos k_j to ≤ 1.1e-11 | all identical to the prediction (< 1e-10) | AGREED | |
| 7 | S3 largest r within 10%, [100]/[110]/[111] | 1e2: 3.0/5.7/10.4; 1e3: 11/12.7/36.4; 1e4: 36/49.5/123; 1e6: ≥ 239 (run end) | 1e2: 3/5/10; 1e3: 11/13/36; 1e4: 36/49/123; 1e6: ≥ 400 | AGREED | site discretisation; longer run on the remote side |
| 8 | S4 class B Bloch front speeds / ratio | radial 0.3647/0.4643/0.5248, support 0.3647/0.4706/0.5248; ratio 1.439 (radial), 1.441 (plane) | support 0.3628/0.4671/0.5231; ratio 1.442 | AGREED | sampled maxima (S2-P 200k k, slightly higher); ratio within 0.3% |
| 9 | S4 class B simulation | plane pulses (48-ch, exact 1-D reduction): 1.44 at r = 50…1600 (main peak); point pulses r ≤ 60: 1.2–1.28 (finite-r read-out) | 1%-arrival ratio 1.31 (r = 12–30), 1.45 (r = 30–48) | AGREED | both: does NOT decay, asymptote 1.44; finite-r point-pulse values read-out dependent |
| 10 | +++ control of S4 | → 1 (plane: 1.006 at r = 2000; point 0.84 → 0.91) | 0.96–0.99 | AGREED | |
| 11 | S7 parallelogram defect, axis pair, 1% | t-convention: +0.340/+0.152/+0.0935/+0.0659 (m = 20/40/80/120); τ = t+1 convention: +0.303/+0.139/+0.088/+0.0624 | +0.264/+0.145/+0.085/+0.062 (m = 20/40/80/120) | AGREED | with S2-P2R's τ = t+1: ≤ 0.006 at m ≥ 40 (m = 120: 0.0624 vs 0.062); m = 20 differs by 0.04 (threshold interpolation at small m); both decay ~m^(−2/3) |
| 12 | S7 fibres | +1.000 / −0.500 exactly (Engine fibre runs, m = 20, 40) | +1.000 (exact causal-cone proxy) | AGREED | |
| 13 | S8 inertness: light not affected by matter, independent of A | max |S_lit − S_dark − S_vac| ≤ 580 units (48-ch light field, L = 40, t ≤ 40; A = 1e9, 1e12; matter ≤ 1e3, 1e6) | max |D| 6–11 over 30 steps, A = 1e3…1e12 | AGREED-QUAL | both bounded and A-independent; absolute numbers depend on the set-up (field = 48-channel sum, dense matter ball, wrap) |
| 14 | S8 caveat: light scrambles low-amplitude matter | P_S8b: up to 7–9 units beyond superposition in 52–77% of matter channels, same for A = 1e9/1e12 and matter amplitude 3 or 1000 | "O(1) level" | AGREED | inert light ≠ matter left intact |
| 15 | global cube rotation | 48/48 (+++ and ++-) | 48/48 | AGREED | |
| 16 | uniform relabelling g → p·g WITHOUT rotating space | (R1 always includes R(p)); a relabelling alone is a symmetry only for R(p) = 1 | symmetry only for p ∈ {1, z} | AGREED | same statement (covariance pairs h with R(h)) |
| 17 | per-node frame field | R2 = TRANSPORTED tensor (coupling rewritten in the new labels, per-site table): pure gauge, identical states and click logs; untransported: not a symmetry; on +++ even untransported rotated tables leave the LIGHT sector identical (R5, 5/5) | fixed tensor: changes everything; transported: pure gauge but 79 distinct +x tables (not one global tensor) | AGREED | both: gauge only with transport; transport ⇒ no longer one global tensor; R5 adds: light is blind to any wiring when all weights are +1 |
| 18 | frame-rotated tables without transport break reciprocity | 49,888/62,208 (+++), 46,432/62,208 (++-) entries (P_x[d] = P[R(h_x)d], L = 6) | 35,104/36,000 | AGREED-QUAL | both inadmissible; fractions depend on the construction (S2-P rotates direction labels; counts differ) |
| 19 | toy exponents | SC −0.73…−0.75, square −0.72…−0.75, BCC −0.77…−0.79, FCC −0.93…−1.10 (r ≤ 100 nn, range-limited) | ~ −2/3 for SC6/FCC12/BCC8/square | AGREED (SC, square, BCC); AGREED-QUAL (FCC) | FCC: my fit range r ≤ 100 nn is contaminated by the constant offset; both consistent with −2/3 asymptotically (S2-M: K4 ≠ 0 for FCC) |
| 20 | toys below resolution | triangular, ISO19, ISO27 at the noise level (≤ 0.05% at r = 100) | below its resolution floor (upper bound) | AGREED | |
| 21 | max group speed over all 48 bands | 0.577338 (sampled; = 1/√3 only for the light band) | 0.577356 (light only, k → 0) | AGREED | |
| 22 | massive bands not Klein–Gordon with c = 1/√3 | massive speed limits 0.4957 (z-even), 0.4614 (spinor); Γ multiplets split linearly; singlet μ0 = −2 isotropic-quadratic, |ω0ω''| = 0.225 | X singlet ω0 0.5475, c_m 0.5051/0.567/0.567; [111] valley ω0 0.5749, c_m 0.5377/0.3348/0.3348; Γ multiplets linear, anisotropic slopes | AGREED | complementary: no common speed limit, anisotropic masses |
| 23 | linear stability needs spec A(k) ⊂ [−6, 6]; extra unit links unstable | (toys normalised Σw = 6; link WAITS ignite: ×1.29/update, exact) | THEOREM; λ(0) = 18 for unit face-diagonal links | AGREED | |

## 2. EVENT space vs CLICK space (owner ADDENDUM 7) — S2-P
| quantity | EVENT space (full state, board update count) | CLICK space (official clicks only: step, address, kind, quotient) | agree? |
|---|---|---|---|
| round free-light front | |b| fronts: sphere; rel. anisotropy [100]v[111] (10%) −4.1% (r = 100), −2.5% (200), −1.5% (400) | the click QUOTIENT ell = b' + a (logged with every click) read with the same fraction-of-peak rule: −3.8% (r = 100), −2.8% (150), −2.3% (200) (P_impl large; P_demo D3) | YES: the observer reads the round front from quotients; the official CLI log's quotients equal the full-state ell integer for integer (L = 21) |
| FIRST click at a station | (not a front: the earliest nonzero change) | quantization front: A = 1e15: speeds 1.000/0.707/0.577 on [100]/[110]/[111] at r ≤ 20 = the strict cone |x|₁ = t (TAXICAB octahedron); −13% at r = 200; A = 1e6: −3.6% at r = 200; A = 1e4: axis lags +13% at r = 200 (sub-quantum) | DIFFER: first clicks are NOT the light front; an observer must weight by the quotient |
| fibres | transit = node count | the same: one click per node per update; taxicab | YES |
| normal-mode periods (clocks) | cos ω = μ/6 on the exact board (measured on b: ≤ 1.1e-11; 97 light + massive projections ≤ 9.6e-11) | THEOREM: the logged quotient is ell_t = b_t + b_{t−2} exactly, so every mode projection of the click quotients oscillates at the same frequency (not separately run) | YES |
| time base | update count | station clocks (any identical clicking clocks) tick at equal rates on the homogeneous board, so arrival-time RATIOS are unchanged; resolution = clock period (needs ≤ ~4 updates to resolve 1% at r = 200); free-light radar echoes are impossible (inertness: nothing reflects large-amplitude light), so stations need a prepared common start; large-amplitude light disturbs low-amplitude station clocks (row 14) — the arrival is read at the onset | QUALIFIED |

## 2b. S2-P local exponents of |rel. anisotropy| [100]v[111] (W500; intervals r = 100–200, 200–300, 300–400)
peak −0.508/−0.536/−0.547; 50% −0.863/−0.812/−0.799; 10% −0.713/−0.721/−0.704; 1% −0.708/−0.683/−0.697.
(The peak approaches −2/3 from above, the 50% read-out from below — both carry a constant offset term; 10% and 1% sit
at ≈ −0.70 already.)

## 3. Remaining action
- None. Row 5 was closed at 04:44 (see §4: the twin's peak anisotropy at r = 400, +0.656%, equals mine).

## 4. Twin's AGREE table (s2/P2R_AGREE.md, relayed 04:39): C1–C23 AGREED (4 qualified), C24 not checked, no DISAGREE.
S2-P replies to its three open questions (signed S2-P, 04:44 UTC):
- **S2-P reply, C15 (inertness normalisation):** YES — my 23–51 (t = 5) … 412–580 (t = 40) are max over sites of
  |S_lit − S_dark − S_vac| with S = Σ_g b_g, the SIGNED sum over the 48 channels (the light field), not Σ|Δb|. Per
  channel (P_S8b.py: matter channels, b_lit − b_vac − b_dark) the maxima are 7–9 units at t = 20–30, i.e. the twin's
  per-channel 6–11 (t = 30) / ≤ 12 (t = 40). AGREED after normalisation (factor ≤ 48). I agree with the caveat: the
  deviation exceeds O(1) matter counters (52–77% of matter channels changed by up to 7–9 units, independent of A).
- **S2-P reply, C23 (EFF splitting):** the "8.776e-4 vs 1.573e-2 (18×)" is S2-M/S2-M2's definition, which I quoted;
  my own EFF numbers were the fitted coefficients (c2 = 0.444444, c4 = −0.03909 in 6 directions) and front
  anisotropies. Table: s2/M_routing_EFF.json as given by S2-M ("routing-EFF-lift000", body lines (−1,−1,0), (0,−1,0),
  (0,0,−1), body_actions_2O [9, 2, 28]; sha256 b84ea465950f5e81…), my own executor (P_eff.py). Re-computed now
  (P_eff_splitting.json), light band at |k| = π/4: (i) pair (3,0,0) vs (2,2,1): EFF 8.77e-4, SC 1.561e-2 relative to
  the mean (1.5735e-2 relative to ω_100, = S2-M2's number): ratio 17.8; (ii) 71 Fibonacci directions on the sphere,
  (max − min)/mean: EFF 2.83e-3, SC 1.53e-2: ratio 5.4 — the twin's 1.68e-3 vs 7.89e-3 (4.7) is the same picture with
  its own direction set/metric. AGREED after definition: the pair sits near a node of EFF's 6th-order term, the sphere
  spread is ~5× below SC at |k| = π/4 and falls ∝ |k|² faster than SC's.
- **S2-P reply, C17 (hard-edge convention):** at a hard edge I take the FIRST SAMPLE, not an interpolation into the
  zero sample (rule in P_front.front_times: if the previous allowed sample is < 1% of the threshold, the arrival is
  the step itself). The FCC/BCC magnitude gap is a UNIT convention: my §4 table quotes r in shortest-link units
  (FCC nn = √2, BCC nn = √3 grid units). At r = 100 GRID units my values are FCC +0.88% (= the twin's 0.88%) and BCC
  +5.93% (twin 5.3%); the remaining BCC 0.6-point gap matches the r-matching convention (I interpolate in r between
  lattice points; the twin uses nominal/nearest-point r: ≈ 0.5 update at t ≈ 100). AGREED.
- **Row 5 closed:** the twin's C3 gives the peak anisotropy at r = 400 as +0.656%, mine +0.657% → identical data;
  its "−0.70/−0.69/−0.69" are threshold read-outs (mine −0.70/−0.70 at 10%/1%). AGREED. No OPEN items remain.
- C24 (ignition by link waits / clutch holds): mine only (P_wait.py ×1.29/update; P_hold.py ×1.019, ×1.017;
  P_hold_noise.py ×1.009); not checked by the twin.

## 5. ADDENDUM 10 (WS-B) — S2-P vs S2-P2R (twin interim s2/P2R_WSB.md, 05:24), rows written 05:55 UTC
**Conventions.**
- P: S2-M's spec. Site gears u = Σ₆b + s; BACKWARD D_t, D_i, which equal central half-step differences in the staggered reading (b^{0i} at (t−½, x+e_i/2), b^{ij} at (t−1, x+(e_i+e_j)/2)); η = diag(−1,3,3,3).
- P2R: gears u = 2Σ₆b + J; CENTRAL full-step D; η = diag(−1/3,1,1,1).

All sources are labelled mechanism tests (prescribed conserved T).
The status column is PROPOSED by S2-P (06:04 UTC). The twin must confirm it via the manager.
Two checks for the twin:
- W11: its central-difference leak should show the ℓ=4 pattern ∝ Σn_i⁴ − 1/3, zero along [111].
- W2: its central differences annihilate the staggered mode (−1)^{x+y+z}, which explains why it sees only √t.

| row | claim | S2-P (backward / staggered) | S2-P2R (central full-step) | status |
|---|---|---|---|---|
| W1 | (a) linear Lorenz C ≡ 0 | float: max\|C\| ≤ 1.5e-7 at field 1e9 (round-off) | rational: exactly 0 | AGREED (THEOREM) |
| W2 | (a) integer C = P-independent carry noise, no exponential growth | L=48, T=2000: max\|C^0\| 37–57 (t=101) → 226–1180 (t=2000), C^x 415–1827, same order for P = 1e6–1e12 (rel ∝ 1/P: 1e-2 → 5e-9); rms outside the Nyquist corner ∝ t^0.54 (ν = 0 and x); total C^x super-diffusive (96–99% in the staggered mode (−1)^{x+y+z}, a double root of the leapfrog) | max\|L\| 31→360 (osc), 24→299 (move), L=40, T=3000; rms ∝ t^0.52; relative ≤ 3e-6 | AGREED-QUAL: same magnitudes (≈ 40 → 400 units) and the same √t law for the long-wavelength part. My extra staggered-mode growth is a backward-difference artefact (central differences annihilate (−1)^x) |
| W3 | (a) S2-M2's identity 6(C₊+C₋) − 2ΣC + 𝓛[Δr] = 2𝓛[s] = 0, bit for bit | 0 violations in every update of every exact run (int64) | not reported | P only |
| W4 | (a) non-conserving control → constraint violation | +1 on S^00 once at t = 50: max\|C^0\| ≤ 0.026 (free wave), Σ_x C^0 = 1/3 exactly; permanent: Σ_x C^0 = (t−50)/3 exactly, local max bounded | T0j dropped → 25% of h within 50 updates | AGREED-QUAL (different controls) |
| W5 | (b) two TT polarizations, GR patterns | point source: h+, h× rms 0.3–0.7%, max ≤ 2.7% (146 dirs, R = 24–40) | blob: within 5–7% (near zone, blob) | AGREED |
| W6 | (b) normalisation = quadrupole formula × source form factor | 1.028 (ω=0.3), 1.007 (ω=0.15) of point formula (lattice +O(ω²)) | 0.71–0.75 = blob form factor 0.74 | AGREED |
| W7 | (b) rotating source circular on axis | \|h×\|/\|h+\| = 1.001–1.010, −90.25° | 0.999 (r=20), 0.973 (r=30) | AGREED |
| W8 | (b) 1/R | amplitude·r constant to 0.03% (R = 24/32/40) | r = 20/30 | AGREED |
| W9 | (b) non-TT parts of b^{ij} are pure gauge (curvature check) | R's non-TT part ≈ 4/R relative while b's non-TT part is 0.78 at all R; R^TT = −½δ_t²h^TT within 4.2/R | not done | P only |
| W10 | (c) TT = 0 | bit for bit (literal: b^xx=b^yy=b^zz; co-located: shifted equality incl. r) | TT = 0 | AGREED |
| W11 | (c) exterior R_{0i0j} full/(B) → no radiation outside (Birkhoff) | co-located: EXACT 0 (lin 4e-16–6e-15 at ω = 0.15/0.3/0.6; int 3–6e-7); spec-literal: 0.13–0.14 (O(ka) placement artefact) | 0.016–0.055 at period 20, ∝ ω² | AGREED-QUAL: no radiation in the continuum limit. The residual is a placement/read-out artefact whose ORDER depends on the convention: 0 (staggered), O(k²) (central full-step; my prediction: ℓ=4 pattern ∝ Σn_i⁴ − 1/3, zero along [111]), O(k) (backward with literal placement) |
| W12 | (c) design (B) radiates a 1/R monopole | R·r = 1.066e8 / 1.063e8 (R = 16/24) | yes | AGREED |
| W13 | (d) GR frame-dragging sign | b^{0y}(+x) = −b^{0x}(+y) > 0 | h̄^{0y}(+x) = −h̄^{0x}(+y) > 0 | AGREED |
| W14 | (d) 1/r² dipole amplitude vs continuum | 1.011/0.995/0.988 at r = 8/10/12 (1.04–1.12 at r ≤ 6, point plaquette dipole) | 1.013/0.996/0.978 at r = 8/10/12 (0.997/1.031 at 4/6, blob) | AGREED at r ≥ 8 (≤ 1%) |
| W15 | exact rewind of all gears | True in every exact run (a, b, c, d) | True (10 × (a,b,r)) | AGREED |
| W16 | THEOREM: Rule3 leapfrog with c² = 1/3 is stable only for m = 0 | at k = (π,π,π): 2cos ω = −2 − m² < −2 for any m² > 0 | 12c² + m² ≤ 4 | AGREED (THEOREM) |
