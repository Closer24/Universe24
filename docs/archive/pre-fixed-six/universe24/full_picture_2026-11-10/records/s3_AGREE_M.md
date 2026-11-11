# AGREE_M — Study 3 mathematicians S3-M and S3-M2: the new matter, and what matter IS in clocks and clicks

Drafted by S3-M2 at 04:12–04:14 UTC 2026-11-10 (`date -u`) from M2_FINDINGS.md (v1, 04:05) and M_FINDINGS.md
(v1, 04:05), after direct exchange (S3-M2 -> S3-M 04:08; S3-M -> S3-M2 received ~04:12, self-stamped 04:15, "I agree with nearly everything ...
I'll review and co-sign"). STATUS: items below are AGREED by message; S3-M confirms the file by co-signing at the end.
Binding rules applied: ADDENDUM 2 (no calculations on the board), ADDENDUM 4 (tensor only), ADDENDUM 5/5b
(ALGEBRA <-> CLOCKS <-> EINSTEIN), owner DEADLINE. Labels: THEOREM, EXHAUSTIVE, DERIVED, CONJECTURE, SIMULATION.
Cross-study results used, not re-derived: S1 T18 = S2 C37 (no fixed tensor gives a load-sourced or universal lapse),
S2 C1, C27, C36, C38, C39, C40.

---------------------------------------------------------------------------------------------------------------
## 1. The agreed answer in plain words
* **A clock IS a tensor eigenvalue.** Every Bloch mode of a fixed tensor turns by w per update, `cos w = mu/6`
  (`mu/6Q` for a 6Q-tooth gear); the carry adds a bounded force, so a large clock keeps this rate to O(1/amplitude)
  (S3-1; S3-P 2.5e-10). Exactly periodic single-frequency (rational cos w, remainder-free) integer clocks have periods
  1, 2, 3, 4, 6 only (Niven; S3-2 = K5); multi-frequency integer blocks (e.g. weight-3 "magic" rings, S1-P's ring(n,k))
  can be exactly periodic with other periods [wording qualified by S3-M2 at 04:17 after signing; no conclusion changed].
* **Matter = a massive band = a clock whose rest rate is its gap** (de Broglie: rest frequency = rest energy = mass;
  wave number = momentum; a moving packet = a moving clock, its phase spread over space = the de Broglie wave).
  **Light = the band with zero rest rate** (the A1 band of +++). **Antimatter = the time mirror JR of matter.**
  **A clock that never overflows (dark) is frozen.**
* **The reference +++ bands are not Einstein matter** (lattice-scale masses, anisotropic, valleys, dilation with
  their own c_m: C38, S3-P R2), and with divisor 6 no ONE-channel isotropic massive band is stable (S3-3). Light,
  relativistic matter needs an effective coefficient below 1: either a CENSUS over channels (KK-H, tensor-only) or a
  BIGGER GEAR (the KG gear, divisor 6Q, departure).
* **New matter, agreed ranking:** (1) **KK-H with odd n** = THE tensor-only new matter: n copies of the 48 channels,
  the two plain body-x ports of +++ (body action = identity) step the copy index j±1. Matter is light circulating
  round this internal ring (Kaluza–Klein). (2) **KG gear** ("light one tooth short", u = (Q−1) Σ6 b, divisor 6Q) as a
  labelled DEPARTURE. It is the leaner option once gravity is accepted: one channel per node instead of 48n, no copy
  index, `c_m^2/c^2 = w0 cot w0 ≈ 1 − w0^2/3` (KK-H ≈ 1 − 1.3 w0^2). The lapse departure itself already needs
  rational coefficients N = n/P, hence a bigger divisor (6P^2, S2 C39 iii). Once gravity is accepted, the KG gear's 6Q
  therefore adds no new KIND of departure (they combine to 6QP^2).
* **Gravity is impossible tensor-only for every matter design** (T18/C37). Both designs are Einstein-READY under the
  agreed minimal departure (C39: bilinear, conservative, prescribed or sourced lapse): one half-angle law
  `sin(w/2) = N sin(w_vac/2)` for every mode (S3-6); mass clocked by N, transport by N/H; self-sizing.

---------------------------------------------------------------------------------------------------------------
## 2. The dictionary (ADDENDUM 5) — agreed
| object | ALGEBRA | CLOCKS (board time, full state, clicks) | EINSTEIN | basis |
|---|---|---|---|---|
| clock | Bloch eigenvalue mu of A(k) | turns by w per update, cos w = mu/6 | normal mode of frequency w | S3-1 THEOREM; S3-P |
| exact integer clock | rational cos w, remainder-free | periods 1, 2, 3, 4, 6 only (KK-H n = 3: exactly 6) | — | S3-2 = K5 THEOREM |
| light | A1 band, mu = 6 at Γ; in KK-H the j-uniform sector = the reference bit for bit | open gear train, w ≈ c|k|, c = 1/sqrt3; clicks wherever it changes a vacuum channel | massless field | C1–C6, K1 |
| matter (KK-H) | Z_n character q: top band of `A_q(k) = A_yz(k) + diag 2cos(k.R(g)e_x + q)`, mu0 = 4 + 2cos q | closed internal gear cycle (light round the copy ring), rest rate w0 = arccos((4+2cos q)/6) | Klein–Gordon, m = w0, c_m -> c from below | K1, §3 numbers |
| matter (KG gear) | `cos w = cos w0 cos wL`, cos w0 = (Q−1)/Q | rest period 2 pi/w0 (31.68 for Q = 51) | Klein–Gordon with the light's c to O(w0^2, k^2) | S3-4 |
| moving clock | Legendre/Clairaut `w − k.grad w` | comoving phase rate | dtau/dt = 1/gamma; exact iff KG | K3 (THEOREM carrier, DERIVED packets), S3-5 |
| speed limit | |grad w| <= 1/sqrt3 every band | no packet outruns the light front | light cone | C1; S3-4 iii (KG gear every k); KK-H c_m < c (§3) |
| one c for matter and light | impossible exactly for any massive band of any integer tensor | — | Lorentz only in the continuum limit | K4 THEOREM (Lindemann) |
| antimatter | JR(a,b,r) = (−b,−a,r), F JR F = JR for ANY divisor; KK-H: character −q | counter-rotating clock, same rate; clicks reversed in order, quotients negated, C1 <-> C2 | CPT image, same mass, opposite charge | K9, S3-9 |
| charge | KK-H: internal circulation sense (built in); KG pair: Wronskian q = Σ(X_t Y_{t+1} − Y_t X_{t+1}) (flips under JR, kept under J) | sense of rotation | U(1)-like charge (KK charge) | K2, S3-9 iv |
| dark (never overflows) | quotient ≡ 0 <=> b(t+1) = −b(t−1); kernel states (mu = 0); +++ dark level at rest E + 2·T2 | quarter-turn rotor, every channel's a^2 + b^2 constant: FROZEN; in the quiet vacuum exactly invisible and exactly non-interacting | non-interacting, motionless energy: not cosmological dark matter | K6 = S3-7 (corrected), S3-8 |
| gravitating load | must be J-even, hence quadratic (energy); linear sources: antimatter would anti-gravitate, dark weightless | not a click count | T00 | S3-10, K8, K9 |
| lapse | tensor-only: none ((6 − W)<b> = 0); departure: bonds N_x N_y, on-site N_x^2 | sin(w/2) = N sin(w_vac/2) for every clock | g00 = −N^2 | T18/C37, K8; S3-6 (departure) |
| constraints (5b) | fixed connection: no local gauge symmetry, no Gauss law; gauging the KK internal translation (a Z_n link register) gives an exact Gauss law for KK charge | — | Gauss law of a KK photon; Einstein's constraints not reached | K10, S3 §6 (departure) |

---------------------------------------------------------------------------------------------------------------
## 3. KK-H (rank 1, tensor-only): agreed facts
* Layout: 48n channels (j, g); 4 reference body-y/z ports (same j, label g·B_u); 2 plain body-x ports step j±1
  (`B_{±x} = 1`). Weights +1, one input per face neighbour, 2O-covariant, reciprocal, stable (|mu| <= 6), Rule3 with
  divisor 6, no gates, tables or on-site entries, zero new executor rules. n = 1 is the reference.
* **K1 [THEOREM + SIMULATION]**: the j-uniform set U is invariant under F^{±1} and is the reference bit for bit (runs:
  official VariantEngine == dense reference; j-uniform KK-H == reference every copy, n = 3, 12; rewind exact; S3-P
  replicated independently, P_kkh_tests.json).
* **K2 [THEOREM, Curie]**: every Fix(T^d) is invariant under F^{±1}: light alone never creates KK matter, at any
  amplitude; matter never annihilates completely into light. (Agrees with S3-11, which covers any band at large
  amplitude.)
* Numbers (exact Bloch; M2_scan_n.py, M2_rtower.py, M2_restframe.py): c_m^2/c^2 = 0.885, 0.934, 0.970, 0.992 for n = 12,
  16, 24, 48 (w0 = 0.300, 0.226, 0.151, 0.0755), isotropic to 5 digits. **Use odd n**: for even n the q = pi sector
  holds an exactly massless second light at R (exact sign-symmetry image of the light). For odd n the light part of the
  tower lives at Γ (small q, uniform rest pattern) and at R (q near pi, staggered rest pattern), all Klein–Gordon
  (n = 25: R level w0 = 0.0725, c_m^2/c^2 = 0.993; Γ level w0 = 0.145, 0.972). **Rest frame (answer to S3-M's
  question, scan of every sector, odd n = 5..25):** Γ for the light Γ levels (n = 25: j = 1..4), R for q near pi
  (j = 8..13), and the P points (pi/2)(±1,±1,±1) for the heavy middle levels (q ≈ pi/2, mu0 ≈ 4.8, w0 ≈ 0.64:
  lattice-scale valley matter). n = 5 already puts j = 1 in a P valley; for n >= 7 the lightest Γ level is at k = 0.
  So the CONTINUUM part of the spectrum (w0 << 1) always has its rest frame at Γ or R.
* Demo (exact integers, M2_kkh_sim.py, M2_run5b.py): n = 3 rest clock exactly period 6 for A = 1, 7, 1e12 (remainders
  never change); n = 12 rest frequency = Bloch to 4e-12; JR image counter-rotates at −w0; n = 24 moving clock: proper
  rate within 1 % of Bloch, Bloch within 4e-5 / 6e-4 / 8e-3 of SR(c_m) at k0 = 0.1 / 0.2 / 0.4; S3-P: dilation vs
  SR(1/sqrt3, v_meas) 0.0517/0.0516 at k0 = 0.4.
* Under the departure (M2_gr_ready.py, Bloch, two link classes w_h = N^2, w_p = N^2(3/H^2 − 1)/2): rest clock
  sin(w0/2)/sin(w0_vac/2) = N exactly for every H; light speed ratio N/H exactly; Compton length in nodes ∝ 1/H to
  0.2–0.8 % (fixed proper size). This is S3-12's "mass clocked by N, transport by N/H" realised with INTERNAL links.
  Not yet run in a gradient (DERIVED: symmetric static coefficients, as S3-14).

## 4. KG gear (rank 2, departure: divisor 6Q): agreed facts (S3-M's results, co-signed)
S3-3 CFL rigidity [THEOREM]; S3-4 dispersion `cos w = cos w0 cos wL`, subluminal at every k, isotropic like light,
zone-corner copy = the same particle, reversible [THEOREM + SIMULATION: plane waves to 1e-15, 3-D along [100]/[110]/
[111] to 1e-9]; S3-5 comoving clock vs SR with c = 1/sqrt3 within 0.2 % up to v = 0.5c [SIMULATION]; S3-6 half-angle
law [THEOREM, departure]; S3-14 [SIMULATION, prescribed lapse, mechanism unit test, P = 200]: stable through a step
1 -> 1/2 with exact rewind; reflection falls with ramp width like WKB (matter 1.4e-2, 1.3e-2, 1.8e-3, 1.8e-4 for step,
W = 25, 100, 400; light 1.1e-1, 2.9e-3, 1.5e-4, 2.9e-5); free fall: lab frequency conserved, speed in the slow region
0.24060 vs 0.24066 predicted; random |b| <= 3 bounded (34 -> 60 in 4000 updates). S3-P replicated B0/B2/B3
(P_NOTES 03:55–04:06: half-angle law to 8 digits; reflections 3.3 %, 1.6 %, 0.62 %, 0.077 % for W = 25–1600).

## 5. Ranked list (agreed)
| rank | candidate | ADDENDUM 4 | key property | key defect |
|---|---|---|---|---|
| 1 | KK-H, odd n | compliant (0 new rules) | j-uniform = reference; KG, c_m -> c from below; exact n = 3 period-6 clock; built-in charge (circulation) | 48n channels; middle levels lattice-scale; c_m deficit ≈ 1.3 w0^2 |
| 2 | KG gear (+ complex pair for charge) | departure (divisor 6Q) | cleanest KG (`w0 cot w0`), 1 channel/node, no doubler; tested in lapse gradients | needs the bigger gear |
| 3 | +++ massive bands (manager's hypothesis) | compliant | the reference itself | not KG with c; anisotropic; valleys; masses at the cutoff (C38, K3b, K10 Landau reading) |
| 4 | on-site gear cycles (hexa, ring, rotor) | on-site entries | exact standard clocks | do not move |
| 5 | frozen dark states (kernel / sub-threshold rotors) | compliant | exactly invisible and sterile in the quiet vacuum | frozen: cannot fall or cluster |
| 6 | V5 exact translators (speed 3/5) | compliant | exact compact movers | fragile; gamma = 5/4 is numerology (r55) |

---------------------------------------------------------------------------------------------------------------
## 6. Theorems co-signed (numbering of both drafts)
S3-M2: **K1** KK-H structure (THEOREM). **K2** Curie superselection (THEOREM). **K3** Clairaut: comoving dilation <=> KG;
a valley k_v != 0 gives a first-order `−k_v.v` shift (THEOREM for the carrier statement, DERIVED for finite packets).
**K4** Lindemann: no massive band of any integer tensor has exactly c_m = c (THEOREM; holds for the KG gear too:
cos w0 = (Q−1)/Q rational, so w0 is transcendental). **K5** = S3-2 (THEOREM). **K6** = S3-7 corrected: never
overflowing => frozen (every channel's a^2 + b^2 constant); kernel states superpose exactly with any state, quotients
unchanged (THEOREM; run M2_dark.py on +++: True). **K7** no silent propagation through the quiet vacuum: a vacuum
channel that does not click keeps a = b = 0 and sends nothing (THEOREM). **K8** = T18/C37 + torus Gauss law (THEOREM).
**K9** antimatter = JR, plus S3-M's J_D(a,b,r) = (−a,−b, D−2−r for even r, D−r for odd r), which commutes with F for any
divisor D, and the Wronskian charge (flips under JR, kept under J), so the antiparticle map is JR, not J (THEOREM;
J_D/JR checked 50/50 by S3-M). **K10** a fixed tensor cannot make the link group dynamical; no local constraints
tensor-only (THEOREM).
S3-M: **S3-1** clock = eigenvalue (THEOREM). **S3-2** (THEOREM). **S3-3** scalar CFL rigidity (THEOREM; KK-H escapes by
its 48n-channel census). **S3-4** (THEOREM + SIM). **S3-5** (DERIVED + SIM). **S3-6** (THEOREM, departure).
**S3-7** as K6. **S3-8** +++ dark level at rest E + 2·T2 (EXHAUSTIVE; the 8-fold multiplicity checked by S3-M2; the
spin-2 reading is CONJECTURE/interpretation; class B T1 + T2; −++/+−− E + 2·T1). **S3-9** (THEOREM). **S3-10** the
gravitating load must be J-even, i.e. quadratic (THEOREM). **S3-11** no pair creation at large amplitude (THEOREM).
**S3-12** (DERIVED), refined: a mass made of SPATIAL links reads N/H like light (gamma = 0); KK-H's mass is made of
INTERNAL (helical) links and reads N exactly with two link classes. **S3-13** self-sizing (DERIVED). **S3-14** (SIM).

---------------------------------------------------------------------------------------------------------------
## 7. Light, dark matter, antimatter, creation — agreed readings
* LIGHT: an open gear train at speed c, no rest clock. In the quiet vacuum every channel it changes clicks (K7).
* MATTER: a closed internal gear cycle (KK-H: circulation round the copy ring; KG gear: the missing tooth). It ticks
  at w0 at rest and is a de Broglie wave in motion (phase speed > c > group speed, `v_ph v_g = c_m^2`).
* ANTIMATTER: the same clock run backwards (JR): same mass, opposite charge (circulation), clicks mirrored. Under the
  quadratic source it falls like matter (ALPHA-g); a linear source would make it anti-gravitate (S3-10).
* DARK MATTER: a never-overflowing clock is a frozen quarter-turn rotor (K6). It is invisible and non-interacting in
  the quiet vacuum, and weightless under any linear or click load. Since it cannot fall or cluster, it is NOT
  cosmological dark matter. Under the lapse departure a kernel state in a well leaves the kernel (effective operator
  6 + N^2(W − 6)) and starts to evolve and click (DERIVED). **Corrected claim (S3-M withdrew its B4(a)/§0.6):** a
  dark-shell PACKET (frequency spread around pi/2) does move at the shell group velocity, but it is not dark. Run
  M2_darkpacket.py (scalar +++ sector, L = 48, A = 1e6, sigma = 4): centroid moves 13.0 nodes per axis in 40 updates
  (13.3 predicted) while 20k–47k of 37k–77k active sites click EVERY update. So no click-free moving carrier or
  "dark detector" exists in this form.
* CREATION / ANNIHILATION / CONSERVATION: at large amplitude bands never mix (S3-11). In KK-H light alone never
  creates matter and matter never fully annihilates into light, at any amplitude (K2). Creation needs a carry vertex
  (CT5) with symmetry-breaking initial data, or a bilinear vertex. Exactly conserved IN KK-H (and the reference, since
  every channel sends six unit outputs): the A1 account Q = 6Σ(b − a) + Σr (KK matter carries 0) and the Z_n symmetry
  classes (K2); NOT in the KG gear (note n2: ΔQ = −12Σb per update, the missing tooth); in both: remainder parity per
  channel. Conserved by
  the linear part only: the energy E = |a|^2 + |b|^2 − b.Wa/3 (= A^2 sin^2 w per channel for a mode), the q content,
  and the Wronskian charge.

## 8. QM — agreed
Superposition and interference are exact at large amplitude up to K(t) units. Clicks are passive and MAP the wave
(bright fringes click, dark fringes do not); a click does not choose a path. Silent propagation through the quiet
vacuum is impossible (K7). Single outcomes need amplitude ~1, the carry regime: OPEN. The Bell bound |S| <= 2 holds
for both designs (local deterministic rule).

## 9. GR — agreed
Tensor-only: no load sources a static field and no load changes a large-amplitude clock (T18/C37, K8): no gravity for
any matter. The minimal departure (C39 + quadratic source: S1's part): every clock obeys sin(w/2) = N sin(w_vac/2).
Both new matters carry their mass separately from spatial transport, so gamma = 1 and fixed proper size follow once
link lengths act (DERIVED; KK-H Bloch-checked, KG gear gradient-tested). Prepared rigid rings remain "strained"
clocks (S1 T13).

## 10. Fit to today's way of working — agreed
KK-H: a VariantCoupling-type table over 48n labels, `ports[d][(j,g)] = (j + s(d,g), ports_ref[d][g])`, the existing
validation (permutation, ±1, reciprocity, 2O covariance with j fixed), the VariantEngine logic unchanged, exact
Rule3 inverse, vacuum = reference bit for bit (K1), passive observers with a Z_n Fourier decoder, full-state
checkpoints. KG gear: JSON block with one divisor parameter (6Q), separate block, its own vacuum fixed point
(r_vac = 3Q − 1, Q odd), rewind exact. Gravity (both): the one generic bilinear rule, pending the owner.

## 11. Open
KK-H in a lapse gradient (only Bloch-level so far); KK-H carry-regime interactions (creation with symmetry-breaking
seeds); single-outcome QM; the quadratic source (S1); the spin-2 reading of the dark level (interpretation only).

## Signatures
S3-M2: agreed, 04:14 UTC (`date -u`). S3-M: AGREED and co-signed, 04:15 UTC (`date -u` read 04:14:37 just before
signing), with three notes that change no conclusion:
(n1) Stamp: my reply went out about 04:10–04:12 by `date -u`; "04:15" in it was a self-stamp ahead of the clock.
(n2) Conservation for the KG gear: the A1 signed account is NOT conserved there. Summing 6Q(b' + a) = 2(Q−1)Σ6 b + r − r'
     gives Δ[6QΣ(b − a) + Σr] = −12Σb per update (the missing tooth = the mass, so Σb oscillates). Exactly conserved:
     remainder parity per channel (2u and 6Q are even). Conserved by the linear part: the energy
     E = |a|² + |b|² − a·Wb/(3Q) and the Wronskian charge of a complex pair.
(n3) §9: the KG gear was gradient-tested in the LAPSE N only (H = 1, prescribed profiles, P = 20 and 200); the link-length
     part (H ≠ 1) is DERIVED for both designs (KK-H Bloch-checked by S3-M2, M2_gr_ready.py).
Demo for the 06:30 integration: s3/M_demo.py → M_demo.log (11/11 PASS in ~1 min: native-engine equivalence, vacuum = reference
bit for bit, light = weight-Q gear, KG rewind, clock = eigenvalue in 3-D, SR dilation, lapse law, lapse step, both mirrors,
frozen dark, charge under JR/J) plus S3-M2's M2_work/M2_kkh_sim.py for KK-H.

---------------------------------------------------------------------------------------------------------------
## 12. ADDENDUM 7 — EVENT space vs CLICK space for the matter claims (agreed by message 04:38; S3-M2 wrote it 04:44)
| claim | EVENT space (full state, board time) | CLICK space (observer, own ticks) | agree? |
|---|---|---|---|
| clock = eigenvalue / rest clock | full-state (quasi)period, cos w = mu/6 | size series ell_t = b(t+1)+b(t−1) is the sampled oscillation: w from ell_{t+1}+ell_{t−1} = 2cos(w) ell_t; tick = one size sign-cycle; only RATIOS to a declared clock are physical | yes: size-cycle rate = full-state rate to 1e-7–7e-6 (S3-M), 1e-5 (S1-M); exact for the n = 3 period-6 clock (pattern period 6) |
| light = reference A1 | j-uniform KK-H = reference bit for bit | the reference click log, identical | yes (exact) |
| moving matter / de Broglie / free fall | centroid of the local rest energy | centroid of the click energy from two consecutive sizes (ell_t² + ell_{t−1}² − 2c ell_t ell_{t−1}) | yes: fall identical to 1e-6 (M2_wep.py); single-size ell² weight is phase-biased: not used |
| time dilation | comoving phase rate w − k v (S3-5, M2_run5b) | reunion test: moving and resting clock meet at one station; size-cycle count ratio = 1/γ | DERIVED (not run) |
| gravitational slowing (departure (B)) | sin(w/2) = N sin(w_vac/2) per board update (coordinate fact) | redshift N_e/N_o by received ticks per own tick (static field keeps signal periods); locally: two co-located species keep sin(W_A/2)/sin(W_B/2) constant | yes: W(r)/W(32) 0.98112/0.99507/0.99861 vs N ratios 0.98155/0.99514/0.99877; two-species ratio constant to ~1e-4 (S3-M) |
| WEP (departure, prescribed gradient) | a = cos(w0)/(6cos²(w/2)) dphi/dx | the same fall in clicks | yes: 0.13 %/0.25 %/1.1 % vs law; Eötvös a(5)/a(51) 0.90175 both spaces (pred 0.8933) |
| antimatter | JR image | log reversed, C1 <-> C2, ell -> −ell; charge = size-Wronskian / KK-H ring phase sense | yes (exact; M_demo D9) |
| dark (frozen) | ell ≡ 0, a² + b² per channel constant | NO clicks: event-space only, except indirectly through gravity under the quadratic source | DIFFER by construction |
| matter clicks under (B) | every channel clicks almost every update | counts carry nothing; clocks are read from SIZES | yes (sizes), no (counts) |

## 13. ADDENDA 6 and 8, P2R questions, demos — agreed (S3-M co-signed (a), (b) and additions 04:38–04:41)
* **Primary design under ADDENDUM 6** (bilinear rank-3, on-site entries, 6Q gears for new channels): the **KG gear** is
  the PRIMARY matter. It needs one new channel per node; the 48 reference channels stay divisor 6 and untouched; it takes
  the (B) lapse directly. **KK-H** stays the strict tensor-only (ADDENDUM 4) design and the Kaluza–Klein reading, with
  built-in charge. Under (B) it would be a new 48n-channel block beside the untouched 48. KK-H through a prescribed lapse
  step 1 -> 1/2 (P = 20, n = 25, 1-D plane reduction, M2_kkh_lapse.py): reflection 1.1 %, bounded, rewind exact.
* **(a) WEP [THEOREM + NUMERIC].** A resting packet falls with g = (c_m²/w0)(dw/dN)|grad N|; the half-angle law gives
  dw/dN = 2tan(w0/2). For the KG gear this is g = c²|grad N|(1 − tan²(w0/2)). The Eötvös residual between species is
  (w0B² − w0A²)/4 + O(w0⁴), so c_m -> c restores WEP to O(m²a²). P2R's x1.5 comes from bands with different c_eff at the
  cutoff. The RATE law is exactly universal in the half-angle variable: sin(w/2)/sin(w0/2) = N for every species
  (S3-M: two species constant to ~1e-4). Prescribed-gradient run: §12.
* **(b) Conserved mobile positive load [NUMERIC + DERIVED].**
  - The leapfrog energy E_f = |a|² + |b|² − a·(M_f b) is conserved to rounding (3e-9; 6.6e-9 while crossing a static
    lapse step). Σb² is not (0.5 %, 37 %, 200 %). The on-site e is only approximate (3e-4, 2.7 %, 5e-4).
  - E_f is positive-definite for massive matter, JR/J-even and local. As a rank-3 SOURCE only its vacuum part or e is
    allowed.
  - S3-M's additions: (1) a reciprocal source dE_f/df makes the coupled map symplectic (Störmer–Verlet), so a modified
    total energy is conserved for exponentially long times (DERIVED). (2) Whatever the source, the Gauss law holds
    EXACTLY for its time-averaged actual value (period-mean identity of the F gear). (3) Clocks are read from sizes
    (§12).
* **Time mirror in (B) (S3-M, exact checks)**:
  - a source reading only current b's (κ b²) keeps an exact reversor: F∘M∘F = M (20/20), with J on matter only;
  - the rest-energy source e (reads previous a) breaks it (0/20) while staying bijective;
  - so an exact time mirror (C1 <-> C2 under reversal) needs a b-only source;
  - the conserved E_f load shares the trade-off (CLICK_TAXONOMY §1);
  - CORRECTION (S3-M 04:45): for REAL (standing) clocks a b² source is 100 % modulated at 2w0 and parametrically pumps
    same-species clocks (rates faster near the lump, non-monotonic: M_gravity_mirror.py);
  - RESOLUTION (S3-M 04:45, M_gravity_mirror2.log): circulating (complex) matter with J = 2(b_X² + b_Y²) = |ψ|² (KG pair or
    KK-H ring circulation) is static, positive, J/JR-even and reads current b only. Clocks then slow monotonically
    (W(r)/W(24) = 0.97911 at r = 3 ... 0.99940 at r = 16; event = click to ~2e-5), the full-run time mirror is exact, and
    all 16,000 matter clicks mirror with ell -> −ell and C1 <-> C2. Antimatter has the same |ψ|², so it gravitates the
    same. RECOMMENDED (B) source: |ψ|² of circulating matter; E_f and e are the static but mirror-breaking
    alternative.
* **Sourced-gravity demo (i) [NUMERIC, two independent codes].** Shared geometry: L = 64, 33-site atom lump, Q_F = 3751,
  S = P = 1e4, T = 600, mean over [200, 600]. The time-averaged F(r) − F(ref) equals the exact lattice prediction from
  the time-averaged source: S3-M 364.4/364.6 (r = 3), 96.7/96.5 (8), 24.5/24.2 (16); S3-M2 (corner reference) ratios
  1.003–1.015 for r <= 8, 1.047 at 16, 1.074 at 24 (low-k ringing). The two codes agree to ~0.2 units after the
  constant reference shift 12.2 ± 0.2. Lump source drift in its own well: −10 % (S3-M2 time-mean) / 17 % (S3-M), a
  post-Newtonian O(phi) effect. Rewind exact in both.
* **Sourced free fall (iii)**: INCONCLUSIVE in the sourced run (the b² + a² centroid jumps when the switch-on front
  arrives; S3-M2's control without a source shows no drift). Replaced by the prescribed-gradient WEP test (§12), a
  labelled mechanism test.
* **ADDENDUM 8**: the click taxonomy is s3/CLICK_TAXONOMY.md, merged by S3-M2 (single editor) and co-signed there.
  Decisions: kind = handedness of the gear's turn (= today's for D = 6; scale-free); tick = size sign-cycle; front
  arrival = fraction-of-peak f = 1/10; delay = size-weighted centroid; antimatter = size-Wronskian sign; C0 = no turn;
  dark = no clicks; metric-gear clicks HIDDEN (audit log).

* **Manager's 04:48 items (merged into CLICK_TAXONOMY §1–§2):**
  - (A) kind statistics do NOT label matter vs antimatter (S3-P v2: C1 = C2 = 1,965,623); only time order or the
    circulation sense does.
  - (B) for CIRCULATING matter the b-only source Σ_j b_j² is static: exact for the n = 3 KK-H clock (ripple 0.0), O(1/A)
    otherwise (5.6e-9 at A = 1e9); standing modes are 100 % modulated. So matter = circulation gives a static source and
    the exact time mirror together, and antimatter gravitates the same. Light's 2w ripple is bounded off the
    phase-matching surface and grows linearly (never exponentially from the source alone) on it. Remedies: circulating
    light, or screening that moves k_res out of band.
  - (C) the staged inverse needs an acyclic a-read graph.

## Signatures for §12–§13 (added after the first signatures)
S3-M2: agreed, 04:44 UTC (`date -u`). S3-M: "co-signed AGREE §12–13 and CLICK_TAXONOMY, 04:45 UTC (date -u), with the
04:45 correction/addition" (by message; recorded by S3-M2 at 04:46, correction and addition included above).

S3-M: "co-signs the 04:48 merge (CLICK_TAXONOMY + AGREE §13 pointer), 04:49 UTC (date -u)" (by message; recorded by S3-M2 at 04:49).

=====================================================================================================================
## ADDENDUM 10 — WS-C: matter for the full metric (S3-M2 wrote these rows 05:29–05:31 UTC from S3-M's rows in
## M_FINDINGS.md "## ADDENDUM 10" and S3-M2's work; to be co-signed by S3-M)
Labels: THEOREM / NUMERIC (exact integers) / DERIVED / CONJECTURE / MECHANISM TEST (prescribed metric, labelled, not
evidence of gravity). Scripts: s3/M2_work/M2_tmunu.py, M2_dirac_shift.py, M2_circsource.py; S3-M's M_tmunu_identities.py,
M_dirac_shift.py; S3-P's P_tmunu2.py, P_shift.py, P_shear.py, P_wsc.py (P_FINDINGS §11). The spec is M2_SPEC_ADD10.md.

| # | claim | S3-M | S3-M2 | verdict |
|---|---|---|---|---|
| A10-1 | **Exact local T^{μν} identities with the rounding remainder** (KG gear, any symmetric fixed linear part). ENERGY: D[e_x(t+1) − e_x(t)] + Σ_i D[J^i_x(t) − J^i_{x−e_i}(t)] = (b_x(t+1) − b_x(t−1))(r_x(t) − r_x(t+1)), with D e = D(b² + a²) − 2(Q−1) a Σ6 b and D J^i_x = 2(Q−1)[b_x(t) b_{x+e_i}(t+1) − b_x(t+1) b_{x+e_i}(t)] on link (x, x+e_i). MOMENTUM: D²[J^i(t+1) − J^i(t)] = 4(Q−1)²{[S^i(x+e_i) − S^i(x)] + Σ_{j≠i}[H^{ij}(x) − H^{ij}(x−e_j)]} + R^i, with node stress S^i = b_{y−e}b_{y+e} − b_y², plaquette stress H^{ij} = b_x b_{x+e_i+e_j} − b_{x+e_i} b_{x+e_j} (symmetric), and R^i = 2(Q−1)[b_x Δr_{x+e_i} − b_{x+e_i} Δr_x] at t+1. CHARGE (pair): the Wronskian with the remainder (S3-P2R C-a). These match WS-B's convention (D_t forward, D_i backward, T^{0i} on links). | THEOREM; 60/60 exact (energy, quasi-momentum, charge) | THEOREM; 0 failures in 39,000 energy and 117,000 momentum checks (Q = 50, 11) | **AGREED, THEOREM + NUMERIC**. S3-P: 0 failures in 4,096,000 node-updates; totals drift 5.6e-9 (A = 1e9) and 1.2e-3 (A = 1e4), below sqrt(T)/A. Remainder-free matter (KK-H n = 3): exactly conservative. Sent to WS-B (S2-M) 05:29; WS-B accepted it as its row W8 (Yee positions; a breathing source's exterior is pure gauge to round-off, R = 4e-16). |
| A10-2 | **No exactly conserved b-only quadratic** for general states (b(t+1) is free given b(t)); b-only proxies (|ψ|², X∇Y − Y∇X) are conserved to O(Δw/w) | agrees (packet Σ|ψ|² moves 4 %) | THEOREM | **AGREED**. S3-P: continuity residual 3.8e-2 (sigma 15) and 4.1e-3 (sigma 60), ∝ 1/sigma². Exact for pure circulating modes (Σ(X² + Y²) = Q_charge/sin w; KK-H n = 3 ripple 0.0). |
| A10-3 | **Trade-off** (single-snapshot update): exact conservation (sources read a) and an exact time mirror are mutually exclusive for general matter. The staged inverse is an exact bijection whenever the a-read graph is ACYCLIC (matter reads only b's; the field may read matter's a); then there is no mirror. A "field-centred" source cannot centre the matter's force at the same time. | THEOREM (Fredkin condition + A10-2) | agrees | **AGREED**. Both at once: exactly for pure circulating matter; for general states only with an implicit or split-step schedule (departs from AGENTS 7: owner decision; its reversor is unproved, CONJECTURE). For WS-B: with A10-1 sources the Lorenz constraints hold up to rounding (R^ν zero-mean); with b-only sources, to O(Δw/w). |
| A10-4 | **Shift, second-order (KG-type) matter: no charge-blind coupling with single-time inputs.** Each Bloch eigenvector of b(t+1) + b(t−1) = M b(t) has the roots ±w (2cos w = mu). The physical spectrum is therefore symmetric, while GR needs N·k ± E for every internal state. R5's partner coupling is CHARGE-ODD (a KK-photon-like gauge field). | THEOREM; co-signed | THEOREM | **AGREED, THEOREM**. MECHANISM TEST (S3-P a1): sense + = Bloch to 10 digits; sense − exactly opposite (w_−(k) = w_+(−k)); a real wave splits into both lines and is unshifted at first order; real light has no coupling. A light PAIR with the ports exceeds the CFL edge (max|λ|/6Q = 1.00006) and blows up. |
| A10-5 | **Shift, FIRST-order (Dirac-type) matter: charge-blind and reversible** (S2-M2's conjecture). With b = i^t ψ the first-order leapfrog ψ(t+1) − ψ(t−1) = −2iHψ(t) IS Rule3: b(t+1) + b(t−1) = 2H b(t). Each eigenvector has roots Ω = arcsin(λ/2) and π − Ω (a time doubler), not ±Ω, so A10-4 does not apply. Advection N·∇ enters as the real-symmetric partner block via the complex structure J, b-only and rank 3 (N from G0i). Every physical mode, of both energy signs, shifts by +2N sin k: the GR form (Ω − β·k)² = E0², including the β² term the KG partner coupling missed, with sin k for k on the lattice. | REFUTES the no-go for Dirac matter; Bloch: 0.108852 = 0.108852 at N = 0.05; exact-integer demo running | CONFIRMS at Bloch level (M2_dirac_shift.py: k = 0.3, N = 0.01, both branches +0.00591); S2-M2 confirms independently (C-test difference 0.0) | **AGREED, THEOREM (Bloch, linear part) + NUMERIC (exact integers, mechanism tests)**. S3-M2's integer board (M2_dirac_board.py, 1-D, D = 300, c_w = 30, s = 20, n = 0, ±3, prescribed uniform shift): board = Bloch to 8 digits for all 24 cases; in the physical sector both energy branches shift by +N_k (+0.003913/+0.003914 vs N_k = 0.003902, i.e. ×1/cos Ω); exact rewind; random |b| <= 3 bounded (max 147 in 1e4 updates). S3-P2R (cbshift.py, own 3-D sin-Dirac construction): particle and antiparticle shifts equal to <= 6.7e-14 in 9/9 cases; board = Bloch to 2.4e-14; linear in β; stable 1e4 updates; exact rewind. RANK-3 form (S3-M2, M2_dirac_rank3.py): the shift taken from a G0i array n(x) on BONDS, K += 2[(n_x + n_{x+e}) J b_{x+e} − (n_{x−e} + n_x) J b_{x−e}], reciprocal. With a NON-uniform static bump: exact rewind over 3000 updates, bounded. A dynamically evolving G0i gear (WS-B coupling) is not yet run. The i^t staggering is a READING convention: the board runs plain Rule3 with b-only inputs, so bijectivity and the mirror are kept. Universal: matter, antimatter (negative-energy branch) and light, if light is a massless first-order (Weyl) gear. CAVEAT (manager 05:31, (1)): on the lattice the GR form holds at FIRST order. λ shifts exactly by 2N sin k, but Ω = arcsin(E0 + N_k): the effective speed is N/cos Ω, and sin k ≠ k at O(k³). In the CONTINUUM LIMIT (spacing h -> 0 at fixed physical k, E and β) the corrections are O(E²h², k²h²) -> 0, so E = E0(k) + β·k and (E − β·k)² = m² + c²k² become exact (DERIVED). |
| A10-6 | **Costs and caveats of first-order matter** | listed | adds the doubler analysis | **AGREED**. (i) Needs 2 entries per row per face (M_d and J) for new channels: an OWNER DECISION (AGENTS 4). (ii) Spatial (naive) doublers at k = π keep the SAME mass and get the same dE as the physical mode at +q, i.e. the OPPOSITE sign relative to their own momentum (the naive-fermion problem; manager 05:31 (2)). A WILSON term w_r(2b_x − b_{x+e} − b_{x−e})G is rank-2 data, b-only, symmetric and commutes with J. It therefore keeps the coupling reversible and charge-blind, and makes the doublers heavy. NUMERIC (M2_dirac_rank3.py, w_r = 10): physical rest mass 0.03334 unchanged, doubler mass 0.03334 -> 0.10017; shifts unchanged; max|λ|/2 = 0.142. In physical units the Wilson mass ∝ 1/h, so doublers are absent in the continuum (DERIVED). On the board they are excited only by lattice-scale data or O(1/A) rounding. (iii) The time doubler π − Ω decouples for smooth initial data; rounding excites it at O(1/A). (iv) Stability needs |E0| + |N_k| < 1 (sub-CFL by construction, unlike the second-order light pair of A10-4). (v) Small click sizes near the π/2 carrier: read via the i^t demodulation (taxonomy). (vi) Its own cone c_D unless weights are tuned to the light's. |
| A10-7 | **Off-diagonal h^{ij} with face ports**. A single input per face per channel gives a DIAGONAL census (S2 C28/C33 + S3-M), so a linearly controllable mixed term needs >= 2 entries per row per face (or edge ports). Realisations: (a) the AUXILIARY gradient gear (adiabatic elimination): g^{ij} = c²δ^{ij} − (4/(9Q²(M² − w0²))) n^i n^j, n = (G, E, 0); (b) S3-P2R's sin-type Dirac gear, M'_x = M_x + εM_y: λ² = s² + 4 sin k·g·sin k. | THEOREM (census) + agrees | DERIVED (a); spec (a2) | **AGREED**. MECHANISM TEST (S3-P a2, 2-D slab L = 128, G = 10): board = Bloch to <= 4e-12; split w²[110] − w²[1−10] = −1.068e-4·E (matter), −1.033e-4·E (light), linear and odd in E; the adiabatic formula predicts −1.056e-4·E and −1.028e-4·E (1.1 %, 0.45 %). Matter and light differ by 3.4 % = O(w0²/M²); stable (max|λ| = 1.96 and 2); random data bounded; exact rewind. Owner decision as in A10-6(i). |
| A10-8 | **Equivalence principle in the full metric** | DERIVED (her rows) | agrees, and adds that the shift becomes universal with A10-5 | **AGREED, DERIVED**. h^00 and h^ii: geodesics of g^{μν}k_μk_ν + m² = 0 to O(w0², k²a²) (WEP deficit 1 − tan²(w0/2), measured 0.90175/0.96805 vs 0.8933/0.9601). h^{ij} off-diagonal: to O(w²/M²) if every species uses the same construction. h^{0i}: universal ONLY for first-order matter (A10-5); KG matter feels a charge-odd force (A10-4), so no universal frame dragging for KG. Light: null geodesics in static metrics (S1: γ = 1); frame dragging of light only for first-order (Weyl) light. Continuum limit: every residual → 0; with first-order matter and light the full 10-component sector converges, under the A10-6 owner decision. |
| A10-9 | **Gauge consistency (S2-M2)**: slow test particles accelerate as a^i = −∂_t h^{0i} + ½∂_i h^{00}, so matter MUST feel h^{0i}, or Lorenz-gauge exterior waves of a breathing source act on it as a 1/R force | agrees | agrees | **AGREED, DERIVED**. This makes A10-5 (first-order matter) necessary for test bodies in WS-B's harmonic gauge, not optional. |
| A10-10 | **Manager's 05:13 points**. (1) c_m/c of the KG gear: PRIMARY form (cos w = cos w0 cos wL): Q = 50 w0 = 0.200335, c_m/c = 0.99327 (= S3-P2R's 0.9932). ALTERNATIVE on-site(−6) half-angle form: 0.99663. 0.9966² ≈ 0.9932 is a coincidence; quote the primary. (2) Comoving click readout: CLICK_TAXONOMY §2.1 (added 05:31). (3) The periodic-universe growth = S1's Z1. (4) Integer-noise pumping: same exposure; relative growth ~ w0² t²/(16 P²); negligible at P = 1e4, T <= 600; use P >= 2^16 for long runs; the circulating source pumps nothing coherently. | rows (1)–(4) | agrees | **AGREED** (point 4 DERIVED, not run). |

**Owner decisions needed (WS-C):**
- D10-a: 2 entries per row per face for NEW channels (the off-diagonal metric and the first-order Dirac structure). With it,
  "10 components sourced (A10-1), propagated (WS-B) AND felt (A10-5, A10-7)" exists at linear order, with exact
  reversibility.
- D10-b (optional): an implicit or split-step schedule, only if the exact mirror AND exact conservation are both wanted
  for general matter (A10-3).
- No own-a port is needed: A10-5 supersedes S3-M2's earlier "κ = D" suggestion.

**ADDENDUM 10 — additions from S3-M (05:33), recorded by S3-M2:**
- A10-5 NUMERIC, S3-M's own exact-integer run (s3/M_dirac_shift_run.py: 1-D ring L = 200, 8 real channels, divisor 6P,
  P = 1000, transport ±P, mass S = 600, Wilson R = 1000, advection n = 50 so N = 0.05, k = 2π·6/L).
  - Frequencies equal Bloch to 9 digits.
  - Particle (+k, positive branch) and antiparticle of the same momentum (negative branch at −k):
    dE_p = dE_a = +0.00314752, ratio 1.000000. CHARGE-BLIND on the integer board.
  - Exact rewind in all 4 runs.
  - The first-order value 2N sin k/6 = 0.00312302 differs by 0.8 %: the arcsin/sin-k lattice correction of caveat (1).
- RANK-3, S3-M (M_dirac_shift_rank3.py): static varying shift h_x = 40 + 30 sin(2πx/L), symmetrised advection (h d + d h)
  with J. The operator is exactly symmetric; exact rewind after 1e4 updates; bounded with no trend. This agrees with
  S3-M2's M2_dirac_rank3.py.
- The DYNAMICAL G0i gear is not run. Matter reads its b (b-only), so the read graph stays acyclic.
- Caveats (1)–(3): the answers in A10-5/A10-6 are AGREED by both twins. The Wilson term was included in S3-M's Bloch check
  and integer run (r = 1) and in S3-M2's M2_dirac_rank3.py (w_r = 10).

**Signatures ADDENDUM 10.** S3-M2: compiled and agreed, 05:33 UTC (`date -u`). S3-M: "co-signs ADDENDUM 10 (A10-1 …
A10-10, D10-a/b), 05:33 UTC (date -u), with the A10-5 NUMERIC addition and the caveat answers (1)–(3)" (by message;
recorded by S3-M2).
- S3-P's (a3) run, read by S3-M2 at 05:33 (s3/P_dirac_shift.json, partial): the 1-D Dirac gear of M2_SPEC (D = 300, c_w = 30,
  s = 20) gives Omega_board = Omega_Bloch to ~1e-11, with exact rewind AND an exact time mirror ("mirror": true) in every
  listed case. This is the fourth independent integer-board confirmation of A10-5 (after S3-M2, S3-M and S3-P2R).
- S3-P's (a3) FINAL (05:35; P_dirac_shift.py, P_FINDINGS §12), recorded by S3-M2 at 05:36:
  - PART 1 (the M2_SPEC gear):
    - board = Bloch to 6.5e-12; every rewind and every time mirror exact;
    - within each J-sector the + and − energy branches shift IDENTICALLY: +0.001965/+0.001965 at k = +0.098 (N_k = 0.001960;
      the 0.25 % excess is the arcsin) and +0.003914/+0.003913 at k = 0.196, linear in n;
    - the C-test {Ω(k)} = {−Ω(−k)} holds EXACTLY (C-even = charge-blind; the KG partner is C-odd);
    - Dirac LIGHT (s = 0) gets the same advection (+0.001961);
    - the doublers get the opposite shift relative to their own Dirac point (A10-6 ii);
    - bounded (47 -> 99 over 1e4 updates).
  - PART 2 (an independent 8-channel quaternion block, J = right multiplication by i, 2 entries per row per face):
    board = Bloch to 2.3e-12; exact rewinds and mirrors; charge-blind.
  - This is the fifth independent confirmation of A10-5.
