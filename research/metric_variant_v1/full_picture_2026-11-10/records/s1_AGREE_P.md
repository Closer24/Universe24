# AGREE_P — twin agreement S1-P (local) <-> S1-P2R (remote; draft relayed by the manager in s1/P2R_FINDINGS.md)

Protocol: every measured claim, both numbers, AGREED / DISAGREE + diagnosis / re-run. Twin numbers are taken ONLY from
the relayed s1/P2R_FINDINGS.md (local s1/P2_* files are NOT used). Stamps from `date -u`. ADDENDUM 7: each claim
carries an EVENT-space reading (full state, board updates) and a CLICK-space reading (clicks-only observer, own ticks).
Labels: G = gated design (DIAGNOSTIC under ADDENDA 4/6); B = bilinear design (primary under ADDENDUM 6).
Abbreviations used in the table:
- PRIMARY: board-time measure read from the full state (clock-state re-entry; first change of state).
- U = f/Phi0: the lapse field in dimensionless units; at large r it falls as U = M/r.
- c_L: the light-wait factor (light time per link = 1 + c_L U).
- lam_act: a load counted as the number of clicking channels at a node.
- V-B: S1-M's scalar test bed with weights modulated by the field (prescribed U).
- H: link-lengthening factor; m/l: the ratio of an on-site clock to a lattice light-cavity clock.
- C37: S2-M's draft theorem that no fixed tensor gives an amplitude-independent lapse.

| id | claim | S1-P event space | S1-P click space | S1-P2R | status | diagnosis |
|---|---|---|---|---|---|---|
| A1 | broadcast field is a 1/r potential (3-D) | k_phi = 1.003 +- 0.003; f/[(J/2)G] = 1.000 +- 0.001 (r 4..32), vacuum (0,0,0) at J = 6*2^24 | not observable in clicks (field gear is new; its clicks are not an observer's clock) | 0.984-1.000 to r = 20 with vacuum (0,0,2) | AGREED | both ~1 where amplitude/vacuum allow |
| A2 | F vacuum (0,0,0) depletes the far field at SMALL amplitude | D-a re-run (t-avg 60..100, shells): J=6000 (0,0,0): 0.888/0.781/0.563/0.455 (R=4/8/16/20); (0,0,2): 0.999/0.997/0.995/0.994; J=6*2^24: 1.000 both | — | (0,0,0): 0.86/0.71/0.42/0.25; (0,0,2): 0.984-1.000 | AGREED | remainder-filling sink ~2.5 per wake node (Gauss identity term); negligible at large J; RECOMMEND vacuum (0,0,2) |
| A3 | 1-D/2-D: no static potential | f ~ t (gradient J/4 exact), f ~ ln t ((J/4pi) ln2 per octave) | — | not run | NOT MEASURED BY TWIN | |
| B1 | H-0, non-radiating lump: no slowing at a distance | all clocks/rings/arms/Shapiro BIT-IDENTICAL to twin (n=160) | clicks identical (bit-identical states) | 12/12 probes identical to the kappa=0 control | AGREED | |
| B2 | H-0, radiating lump (counting content) | k = 0.961 (hexa) / 0.966 (rotor); <abs(ell)> ~ r^-1.014; click count: k = 0 (saturated); <psi^2> r^-2.03 (passive) | hexa clocks: clicks-only periods = event periods (shown in P_sec); rotor invisible | P1 (lamp) not run | NOT MEASURED BY TWIN | |
| B3 | click-free (dark) lump with click-count load | weightless: load 0, field exactly 0 | dark matter invisible in clicks too | dark (-1,-1,0) all-48: ell == 0, period 4 | AGREED | |
| C1 | G: uniform lapse re-times EXACTLY | fibre24 48/36/32/30, ring16 32/24/21.33/20, all-48 probe 8/6/5.33/5 for N = 1/2..4/5 | fibre/ring click counts scale with firings; all-48 probe never clicks | ring16 32/24/21.333/20, all-48 8/6/5.33/5, pair 10/7.5/6.67/6.25; clicks-only ring16 31.86, 21.23 | AGREED | identical numbers |
| C2 | G: non-uniform lapse destroys structured reference matter | ramps, 60|59 step, phase offset: ignition 634k-645k/663k; ring16 straddling a step breaks; fibre ALONE at a sharp 1|1/2 step (D-b, 04:31): first lap nearly clean (0 or 4 created at t=40 for the two schedules), then ignition (647k at t=240) | — | split test destroys orbits (g >= 3); sharp step clean in 2/4 runs; ramps ignite 3/3 | AGREED | twin's "clean" = single crossing; my closed loop crosses twice per lap: first crossing clean, later laps ignite |
| C3 | G: sourced physics run with reference probes | P4: probe rings break from their own self-sourced field; ~900 created; board freezes (zero mode) | — | P4b: all 12 probes destroyed at t = 73-137 before measurable slowing | AGREED | slowing at a distance NOT SHOWN on reference matter |
| C4 | G: gates pump free/smooth waves | private-gear smooth 48-uniform packet x1.5e4 in 160 updates | — | shared gate x1.0026/update, private x1e5 (L=48, T=3000) | AGREED | both unstable (private faster) |
| C5 | lam_act (click-count) load self-acts | clicking probes break from own field (P4) | — | light packet self-freezes at kappa = 2 | AGREED | |
| D1 | G: on-site clock slowing = U, k ~ 1 | delta = U +- 0.003 (X = 3..40); k = 0.991 | hexa clicks-only periods == event periods (same cycle sets) | not run (twin used reference-sector probes) | NOT MEASURED BY TWIN | |
| D2 | gamma: light/clock slowing 1 (1911) vs 2 (GR) | G relay: c_L=1 -> 1.00, c_L=2 -> 2.0 (rings); B (P_Bdemo1, prescribed uniform F): s=1 -> 1.01, s=2 -> 2.03 | (see E1-E3: (B) click readings) | V-B: H-A locked 0.9989-0.9998; H-B gamma = 1 | AGREED | same physics, different setups |
| D3 | Shapiro ratio GR/1911 | G: 2.000 +- 0.004 (b = 3.5..31.5) (identity of c_L); A1 = 2M asinh(Y/b) within 0.03 | first-arrival time is a token hop (click) == event time | V-B Shapiro lag ratio 1.94-2.16 (pred 2) | AGREED | 2 within the twin's wave-packet spread |
| D4 | bending ratio GR/1911 | G eikonal from relay delays: 2.00 +- 0.03 (1.96-2.04) | — | V-B wave bending 1.81-1.91 | AGREED (method differs) | eikonal (front delays) vs wave-packet centroid (finite size, lattice dispersion); both ~2 within the twin's stated spread; decisive test if needed: twin's packet at larger b / longer path |
| D5 | lattice-rigid clock vs on-site clock = H (universality break) | G ring/on-site 1.099 = (1+2U)(1-U) at X=8 (c_L=2); 0.983 = 1-U^2 (c_L=1) | — | V-B m/l = 1.0507/1.1055/1.2203 at U = 0.05/0.1/0.2 (H = 1.0513/1.1052/1.2214) | AGREED | |
| D6 | on-site clock kinds universal under one clutch | hexa vs rotor equal +- 0.001 | rotor invisible to clicks | V-B m-clock at N to 4e-4 | AGREED | |
| E1 | B: clock universality only for slow clocks | uniform: 1.0034 (w0=0.1) ... 1.1042 (w0=1.05); SOURCED atoms: 1.016/1.015/1.010 (w0=0.3) vs 1.104/1.092/1.109 (w0=pi/3) | quotient periods == event periods (20.942072 both) | not run | NOT MEASURED BY TWIN | |
| E2 | B: first change of state is a quantization front | d=20: t = 21/22/26/53 for w/P = 1/.8/.5/.1 (pulse 1e9) | first click == first change | not run | NOT MEASURED BY TWIN | |
| E3 | B: sourced demo (light gamma; redshift) | through-lump excess s2/s1 = 2.01/2.01/2.04/1.98/1.70/2.02/2.08; P_near/P_far = 1.0105 | redshift received/own = 1.0102 (GR 1.0102); Shapiro change in own ticks ratio 1.987 | not run | NOT MEASURED BY TWIN | |
| F1 | ADD5: cos w = mu/6 | k=0 modes of reference M(0): board w = arccos(mu/6) to 1e-4/1e-8/<=1e-7 (A = 2^10/2^20/2^30) | — | free packets follow cos w = (sum cos k)/3 (centroid 0.527 vs v_g 0.547 at k = pi/4) | AGREED | |
| F2 | reference clocks: ring16 = guide transit; all-48 period 4 | ring16, fibre: node counts (carry objects); probe mu = 0 -> 4 | probe never clicks | ring16 16 = guide transit; dark (-1,-1,0) period 4 (THEOREM) | AGREED | |
| F3 | massive bands not relativistic moving clocks | singlet packet: v -0.0389 (alg -0.0392), worldline rate x1.0036 vs SR 0.998 | — | not run | NOT MEASURED BY TWIN | |
| G1 | tensor only: no amplitude-independent lapse | THEOREM (linear part); EXHAUSTIVE small clusters: 0 universal slowings; carry error ~1/A | — | C37 test: A*dev = 37-149 ~ const (A = 1e2..1e6), centroid shift -> 0 | AGREED | |
| G2 | static input acts on rates only mod 3 | rotor full-state period 4 (s = 0 mod 3) / 12 otherwise, any amplitude | — | (S1-M T18c) | AGREED (cross-team) | |
| H1 | PRIMARY vs clicks for on-site clocks | identical cycle lengths | clicks-only == event | clicks-only ring16 31.86 (f=30) over finite windows | AGREED | twin's finite-window value ~ 32 |
| H2 | counting-linear responses give beta = 1/2 | N = 1 - U exactly | — | not stated | NOT MEASURED BY TWIN | |
| H3 | per-direction link lengths (diagonal g_ij) | kappa 2:1:1 -> x/y excess 2.17 | — | not run | NOT MEASURED BY TWIN | |

## Cross-team checks (not the twin)
* 03:54 UTC field law: my code reproduces S1-M's published f/((J/2)G) on L=96 (15/15 values, 3 dp).
* 04:07 UTC S1-M2's decisive heating test reproduced exactly (L=45, K=1: 0.263/1.938/2.937/9.792; 25.3% clutch domain;
  even-L doubler RMS 283 at t=600). Calm at large amplitude.

* 04:47 UTC S1-M EVENT_vs_CLICK_M.md: same click-space principle (click SIZES carry (B) clocks; counts saturate; first
  clicks are quantization fronts); their atom clock ratios from click sizes agree with the full state within 2.3e-4,
  mine within 1e-8 (20.942072 both). Their open item "emitter-to-light coupling not built": built in P_Bdemo3b (near
  atom drives a light gear through one on-site port): received/own 1.0102 (click) vs P_near/P_far 1.0105 (event) vs
  GR 1.0102. AGREED (cross-team).

## Log of disagreements and resolutions
* 04:29-04:31 UTC A2 (F vacuum): twin found depletion with (0,0,0). My headline used (0,0,0) at LARGE J. Decisive
  re-run (P_decisive_vac2.py): small J depletes with (0,0,0) (0.455 at R=20), not with (0,0,2) (0.994); large J: 1.000
  both. -> AGREED; recommendation: vacuum (0,0,2) for the lapse gear.
* 04:31 UTC C2 (sharp step): twin "clean in 2/4"; my P3 step board had a ring16 straddling the step. Decisive re-run
  (fibre alone, 4 gear phases; P_decisive.py step): first crossing of both interfaces nearly clean (0/4 created at
  t=40), ignition on later laps (647k at t=240). -> AGREED (single crossing can be clean; repeated crossing ignites).


## Replies to S1-P2R's open points (P2R_AGREE.md, relayed 04:56 UTC) — signed S1-P, 04:56 UTC (date -u)
* ROW 1 (F vacuum). My headline k_phi = 1.003 / ratio 1.000 +- 0.001 used vacuum (0,0,0) at LARGE load (J = 6*2^24 per
  site per update; f(32) ~ 1e6). Decisive re-run D-a (my code, t-avg 60..100, shells): J=6000 (0,0,0) 0.888/0.781/
  0.563/0.455 at R=4/8/16/20 (depleted, as yours); (0,0,2) 0.999/0.997/0.995/0.994; J=6*2^24: 1.000 for both. AGREED.
  My (B) runs: P_Bdemo1-3b F vacuum (0,0,0) with J = 2^20 per update (depletion negligible at that load);
  P_proto/bilinear default (0,0,2); P_closed/P_yukawa r = 3Q (mid-range, as yours). Recommendation: centred remainder.
* ROW 7 (gate with on-site clock). NOT COMPARABLE: AGREED with your verdict. Consistent extra: my reference all-48
  probe under the clutch in a weak SOURCED gradient breaks after 2-5 cycles and the 40^3 x 48 board ignites (P_probe4),
  matching your P4b for reference-type probes. delta = U (k = 0.991) holds only for on-site clocks (hexa/rotor).
* ROW 10 ((B) clock dependence). AGREED; sharpened by my multi-w tests:
  - uniform-F unit test: 1.0034 / 1.0059 / 1.0240 / 1.1042 for w0 = 0.1 / 0.2 / 0.5 / 1.05;
  - sourced on-site atoms: 1.016 / 1.015 / 1.010 (w0 = 0.3) vs 1.104 / 1.092 / 1.109 (w0 = pi/3), predicted 1.008-1.013 / 1.103;
  - board check of the weak-field slope delta/U = 2tan(w/2)/w on the reference bands: 1.057-1.467.
  Your 1.034 +- 0.023 at pi/4 (pred 1.055) fits. My w0 = 0.3 (near your pi/8) gives 1.01 (pred 1.008), so your pi/8
  value (0.89) is a short-window artefact.
* ROW 16 (beta). My B6 statement "beta = 1/2" is for the GATED counting clutch (N = 1 - U exactly). For design (B) as
  built (mass factor 1 - F/P), N^2 = 1 - 2U EXACTLY, so beta = 0. This is confirmed numerically by the second-order
  term: delta/U = 1 + U/2 (1.0034 / 1.0059 / 1.0110 at U = 0.005 / 0.01 / 0.02). GR's beta = 1 needs
  N^2 = 1 - 2U + 2U^2 (field self-source or a non-linear map). Proposed status: AGREED-pending-your-check (derivation in
  P_NOTES 04:56).
* ROW 17 (click-count load self-freezes). AGREED qualitatively:
  - my P4 (prototype, clutch, click-count source): clicking probe rings source their own lapse and break; on the
    closed L=32 board the zero mode drives the clutch increment to 0 by t ~ 20, so the board freezes;
  - this matches your frozen packet at t = 45 (kappa = 2).

## Replies to the manager's 04:56 items (1)-(3) — S1-P
(1) My (B) run lengths:
  - octant n = 112 / 128 (== periodic 224^3 / 256^3), T = 240-360; demo Part 4 n = 96, T = 240.
  - Total source 8P per update. Zero mode F0 = J_tot t^2/(12 V) grows (THEOREM) but is negligible in my windows:
    F0/P ~ 5e-6 (U0 ~ 3e-6) at t = 300 vs U = 0.004-0.014 at my clocks. Measurements are inside the causal window
    (before images return).
(2) Blow-up REPRODUCED (P_closed, independent code, periodic L=32, J = 2P per update):
  - F0 = J t^2/(12V) exactly (0.2518 P at t=222; formula 0.2507 P);
  - light bounded (1.5-4e5) until t ~ 262; blow-up at t = 284 (|light| > 1e8), with F0 = 0.41 P and F_max = 0.65 P;
  - F_max had crossed the link-weight zero P/2 at t ~ 230.
  - Note: my first run had int64 overflow beyond the onset; that run is discarded and the guard re-run is used.
(3) Screening, KG-gear form (face weight Q - mq, Q = 6000, mq = 1, lambda ~ 31.6; a plain on-site -m is unstable at
  (pi,pi,pi), as you warned, and my first such run was stopped):
  - no blow-up to T=800; exact inverse;
  - (i) F0 oscillates undamped 0.0021-0.061 P (period ~340; predicted max 0.061 P, period 343), far from the link zero;
    F_max 0.23-0.31 P < P/2; light bounded;
  - (ii) pumping near w_F0/2 = 0.009 not tested (no clock that slow); my atoms at w0 = 0.3 and 1.05 stayed bounded;
  - (iii) near-zone 1/r shape kept (screened/unscreened profile ratio 1.00-1.04 at r = 2-16 on L=64); the
    e^{-r/lambda} factor is not resolved on that board, so redshift and Shapiro inside lambda change only at
    O(r/lambda) (DERIVED).

## ADDENDUM 10 / WS-A — S1-P rows next to S1-P2R's rows (P2R_AGREE.md "ADDENDUM 10" + "(B2) convergence"), signed S1-P, 05:48 UTC (date -u)
All S1-P numbers: own code (s1/P_beta.py, P_conv.py = spec v1 = the twin's geometry, P_conv2.py = spec v2, P_conv3.py = spec v3,
P_noise.py, P_strong.py; read-outs P_conv_analyse.py, P_light_phase*.py), pre-registered in P_NOTES.md (18-23), exact inverse in
every run, board sum of the G source = 0 at every check, H identity (H = 2PG - F^2) exact at all sites. E = event space (atom
phase winding, exact N^2 = (2 - 2cos w)/m2); C = click space (not re-measured for B2; on-site atoms click every update, so the
quotient stream gives the same w as in FINDINGS 10). Atoms ON-SITE (no hopping) in all my runs.

| # | S1-P2R row | S1-P (own runs) | verdict |
|---|---|---|---|
| R1 | G = U^2 at field level: 0.94-1.09 (mechanism), 1.11-1.13 (physics) | static-form source FAILS (G P/F^2 = 0.91 ... -4.9, uniform deficit -0.019P; pre-reg 18 failed) — same as your amendment. Leibniz source: G 2P/F^2 = 1.027-1.029 at r = 2.8-3M (window means, v1/v2, all M/h), rising with r because of a near-uniform offset (G - F^2/2P)/P = +0.004 ... +0.007 (window) and +0.001 at t = T (v2; decays like (M/ct)^2). v3 (KG-difference): 1.00-1.02 at <= 6M at t = T | AGREED (size of the deviation depends on window/time, both see the offset) |
| R2 | atom-level beta -> 1 with eps <= 0.002: 1.2 +- 0.25; eps = 0.02 deficit 58-91% | on-site atoms (eps = 0): beta = 1.010/1.010/1.009 (M/h 2/3/4, offset free), readout |N^2 - f_local| <= 1.3e-5 (control), <= 2.5e-3 (B2; G changes in the window) | AGREED (on-site case; your hopping diagnosis not re-tested by me) |
| R3 | beta = 0 blows up where 1 - 2U < 0; beta = 1 stable to U ~ 0.92; remaining breakdown = link zero at U = 1/s | control atoms blow up at every node with U > 1/2 (t = 24-194), bounded at U = 0.46; B2 atoms bounded up to U = 1.58 (T = 200, R_b = 1.5M); link zero at U = 1/4 (my s = 2 == your s = 4) blows up the plain light (t = 38-48) | AGREED (extended to U = 1.58) |
| R4 | light ratio s4/s2 = 2.00-2.11; absolute 0.75-0.81 of the ray estimate | ratio s2/s1 (my convention) 2.0x in the (B) demos (FINDINGS 10); radial TOF (B2): carrier-phase delays 0.5 (6M) -> 0.83 (16M) of the continuum ray estimate EVEN for the prescribed exact-GR reference => finite-beam systematic of the read-out | AGREED |
| R5 | noise: x1.028/update at P = 1000; (superseded:) reference-stencil doubler grows at P = 16000 (x1.0076) | EDGE (1/3) light: x1.0206 at P = 1000 (t_x10 = 520), x1.0056 at P = 16000 (t_x10 = 2640, T = 3000), bounded at 2^20 to T = 3000; stencil B (1/6) bounded at all three P to T = 3000 | AGREED (with S1-M2 and your corrected row) |
| R6 | atom readout = local factor within 0.01 (eps = 0.002); deficit 40% (eps = 0.02) | not measured (no hopping atoms) | — |
| C1 | beta (B2, offset free): 1.007 / 1.009 (M/h 2/3) | v1 (your geometry): 1.010 / 1.010 / 1.009 (M/h 2/3/4); v2 (spec v2, T = 100M): 1.011 / 1.012 / 1.011; v2 LATE half-window: 1.000 / 0.9997 / 0.9998 | AGREED |
| C1b | plus free U^3: 1.022/-0.08, 1.030/-0.12 | v1: 1.026/-0.090, 1.028/-0.106, 1.030/-0.121 | AGREED |
| C1c | a = 1 fixed: 1.032 / 1.036; plus U^3: 1.131/-0.61, 1.142/-0.71 | v1: 1.036 / 1.038 / 1.036; plus U^3: 1.134/-0.64, 1.147/-0.73, 1.145/-0.70 | AGREED |
| C2 | control beta: -0.002 / 0.000 | v1: -0.0002 / 0.000 / 0.000; v2: 0.000 / 0.000 / 0.000 | AGREED |
| C3 | c3 ~ 0 | see C1b; v2 late half: c3 = -0.003 / +0.007 / +0.008 | AGREED |
| C4 | axis = diagonal, delta beta <= 0.006 | offset-free fit: 1.0088/1.0123, 1.0086/1.0119, 1.0091/1.0085 (delta <= 0.0035); a = 1 + U^3 fit: delta <= 0.029 | AGREED |
| C5 | constant N^2 offset +0.004 (half from G) | a = 1.0038 / 1.0040 / 1.0041; in my runs the whole offset is accounted for by the window-mean G offset (control offset 0.0000) | AGREED (size); attribution differs (mine: all of it from G) |
| C6 | G/U^2 = 1.01-1.02 at 3M, offset +0.002P | see R1 | AGREED |
| C7 | light first-order delay within 5-13% at 12-16M | 0.80-0.83 of the ray estimate at 12-16M for both lit and the exact-GR reference (phase read-out) | AGREED in kind (beam systematic ~0.8) |
| C8 | kappa2 not resolvable | not resolvable: the carrier-phase fit of the PRESCRIBED exact-GR reference returns kappa2 = -2.0 / -2.6 instead of 1.75 (M/h 2/3) | AGREED |
| C9 | reference-stencil doubler grows at P = 16000 (x1.0076) | x1.0056 (last 600 of 3000 updates) | AGREED |
| C10 | rewind exact | exact in every run (two-stage light preparation included) | AGREED |

New S1-P rows for S1-P2R / S1-M2 to check:
- N1 (h/M)^2 convergence: visible in the FIELD (U r/M - 1 at 2.9M: 1.0e-3 / 5e-4 / 3e-4, v2) and in the LATE-window r-space fit
  (beta = 1.022 / 1.011 / 1.004, c3 = -0.10 / -0.04 / -0.01, M = 2.007 / 3.003 / 3.996 vs M_load 2.000 / 3.000 / 4.000), NOT in the
  full-window fits (transient-limited) — agrees with your "not visible" for the full windows.
- N2 G6 P-scaling: ln(growth) ratio EDGE P=1000 / P=16000 = 3.6 (yours 3.9) ~ sqrt(16): growth ~ sqrt(w - 1) => headroom loss at the CFL edge,
  not parametric pumping (which would scale ~ depth or depth^2 = 16 or 256). Remedy = stencil B; large P only delays (noise rms
  keeps growing, 4.1 -> 21.6 from t = 220 to 3000).
- N3 G in the link weight (manager): the U = 1/4 link zero disappears (Lgr bounded at U(0) = 0.63-0.72 where Lplain blows up), but
  lambda = 1 - 4U + 8.5U^2 is unbounded: stencil-B ceiling lambda = 2 at U = 0.651 (blew up once the over-ceiling core grew);
  face coefficient 1/12 moves it to U = 0.862 (bounded to T at U_max 0.91 briefly); at U ~ 1.4-1.6 every truncated weight fails.
  => strong fields need the bounded all-orders weight N^2(1+N)^4/16 (S1-M phase 2).
- N4 spec v3 (KG-difference G, l = 3): no uniform offset (a = 1 fixed: beta = 0.992 / 1.003, M/h 2/3), BUT G rings with ~100%
  amplitude at w ~ 0.136 after the switch-on step (G 2P/F^2 = 0.41-2.08 at t = T beyond 12M); r-space fits with free U^3 unstable
  (beta 0.87 / 1.09). For T = 100M windows the plain Laplacian form (v2) is the better choice.

## Rank-3 all-orders checks for S1-M (X11 follow-up; S1-M's s1/M_Binf_split.py run unchanged, plus my P_Binf_adiab.py), S1-P 06:03 UTC
| # | claim (S1-M X11: rank 3 marginal at N ~ 0.5) | S1-P | verdict |
|---|---|---|---|
| X11a | strong case: core lambda dips below 0 in the build-up, light x25 | my parameters (L 64, R0 8, Arot 102, ks 8): -0.08 / -0.19 (t = 10/20), +0.01 ... +0.15 (30-80), -0.30 (90), light x14 | AGREED |
| X11b | (your question a) finer lattice, same compactness | R0 = 8 / 12 / 16 (L = 8 R0): dip -0.19 / -0.41 / -0.46, light x14 / x55 / x300, N_min 0.50-0.56 | the dip is NOT a lattice artefact; it deepens |
| X11c | (your question b) adiabatic switch-on, non-circular | beat-pair load (dark rotor -> bright rotor, on-site rank-2 coupling, t_build = 120 = 6 x crossing; only matter prepared): lambda_min > 0 through the whole build-up (min +0.036 at full load, N_min 0.587), light bounded (x1.8); but lambda sits ~0.1 below its static target 0.14 (conserved-total offset of the massless remainder gear) and turns negative once the load beats back (-0.06 / -0.15 / -0.41 at t = 130/140/150) | adiabaticity removes the build-up dip; rank 3 still MARGINAL at N ~ 0.6 because of the remainder offset |
- 06:06 UTC: S1-M's strong-field reconciliation text (X13): AGREED with three precisions (wording of the refinement dip,
  offset attribution marked as presumed, "about 75 % below target"); see P_NOTES 06:06.
| X11d | (S1-M2 Y15) detuned remainder gears (w = 1 / 0.7 / 0.5) + adiabatic beat-pair load: lambda > 0, light bounded | my re-run (P_Binf_adiab_detune.py, 06:19 UTC): lambda_min/P > 0 at every read-out (min 0.095 at t = 110; 0.12-0.15 at t = 120-150 vs target 0.13-0.14), light x1.87 max then falling, rewind and vacuum exact | AGREED (bit-identical light maxima) |
