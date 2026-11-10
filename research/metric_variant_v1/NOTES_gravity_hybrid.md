# NOTES_gravity_hybrid — HYBRID gravity source (Study 10 port, ST-2). NEW FILES ONLY; DEFAULT OFF.
All stamps `date -u`. Every test is pre-registered here BEFORE it runs; results are appended below, never edited in.
Files (new): layers/gravity_hybrid.py, prepare/gravity_hybrid.py, tests/test_gravity_hybrid.py,
demos/gravity/hybrid_long.py, results/gravity_hybrid/, this file. No existing package file is edited; universe24/ untouched;
no git. One core, nice 19.
Law (OWNER decision 2, 13:09 UTC: approved NEW LAW, designated one-way; final adoption after (a) the reversor test and
(b) a long run): u_F += e_L0 + rho on F = metric.h00, see the module docstring. Study 10 evidence: s10/ST-2_FINDINGS.md,
s10/AGREE_ST.md (S1-S23, both twins), scratch prototype s10/ST-2_work/tts_candidate.py (HYBRID mode, same algebra).
Composition: apply_hybrid(default_system()) = the v2 default with mlapse and lapseL0 replaced by their ONE-WAY actions
(same form-C/R1 coefficients, b-only source dropped), + block "hsrc" (the hybrid source), + GRAV-FIX (A) beta
(build_beta_detuned, w_G = (Q-1)/2) by default; detune_h00 = False by default (AGREE_ST S21 option).
Integrator switch (one line, not applied): default_system(..., gravity_source="lapse"); if gravity_source == "hybrid":
return apply_hybrid(System(Q, tuple(blocks), info)).

## PRE-REGISTRATION (written Tue Nov 10 13:17:24 UTC 2026, before any test or demo of these files runs)
H1 EXACTNESS (tests/test_gravity_hybrid.py, L = 3):
 (a) integers: compose succeeds (the Tensor rejects non-integers; hybrid_source_terms raises on a fractional coefficient);
 (b) designations counted: every hsrc monomial and every one-way lapse-action monomial carries a designation; report the
     counts and the total designated monomials of the composed system vs the default (1202);
 (c) rank <= 4 (max monomial degree <= 3) and B3 (the Tensor's locality check at construction); hsrc monomials have
     degree 2 (rank 3), one node / one link, a-reads acyclic (inverse stages reported);
 (d) vacuum bit-exact for 20 updates: (i) hsrc ALONE with its inputs (ref + matter + metric, no other block), (ii) the
     composed hybrid system; PASS iff the state is unchanged;
 (e) rewind: a random small state (matter |v| <= 2^10, ref |v| <= 20, other gears at the vacuum) of the composed system,
     20 forward + 20 staged-inverse updates: bit-exact.
H2 THE REVERSOR TEST (pre-registered prediction: FAIL, DERIVED in Study 10 / ST-2: R* reverses the matter pair (m(t-1),
 m(t)) -> (K m(t), K m(t-1)), so in R* F R* the lapse reads the two-time source at the pair (m(t), m(t+1)) instead of
 (m(t-1), m(t)): the source is evaluated one step late; R* can be exact only where that local density does not change):
 full hybrid system, L = 6, seeds as tests/test_seed.py SD6 (A = 2^12, x0 = (2,2,2)): S2* and the two S-symmetrised L0 dark
 seeds (L0_rstar_e0, L0_rstar_band); check F^-t(s0) == r_star(F^t(s0)) (observe/seed.py r_star WITH the L0 relabelling)
 for t = 1..6; also R*(s0) == s0. Controls: the same on the plain v2 default (expected PASS, = SD6). Report per t the
 number of mismatching (gear, node) entries and which gear types mismatch. If it fails: test the candidate reversors
 X_k = r_star o F^k (trivially equivalent) is NOT a fix; report the obstruction (no single-time-centred reversor can match
 a source centred at t - 1/2 while the matter reads F at t), and name the structural way out (an OD2-type rounding-free
 accumulator for the source, ST-1's design III mass gear mu, so that the staggered OD2 reversor applies) as OPEN.
H3 LONG RUN (demos/gravity/hybrid_long.py; results/gravity_hybrid/LONG_*.json): hybrid + GRAV-FIX (A), L = 4, data = S2*
 (A = 2^16, x0 = (1,1,1)) + the S-symmetrised L0 dark seed band vector (amplitude 64 x 2^6, x0' = (3,3,3)), exact hybrid
 R-a datum (prepare/gravity_hybrid.with_hybrid_datum), T = 2e4 (as far as time allows; checkpoint every 500 updates).
 Readouts every 100 updates: U_mean = Sum F/(2PN), U_pi = |Sum (-1)^(x+y+z) F|/(2PN), max |G|, max bits. RUNAWAY := any
 value > 2^60 (bits > 60) or |U_mean| > 0.25 or U_pi > 0.25; BOUNDED := no runaway to the end. Reported: the horizon and
 the U_mean / U_pi histories. If U_pi grows steadily (h00's own corner, AGREE_ST S21), a second run with detune_h00=True
 is made (pre-registered here) and reported separately.

## AMENDMENT (written Tue Nov 10 13:19:00 UTC 2026, before any registered run): the live default changed under me (RC2 BATCH 3, 13:17: hands ON =
chiral + electroweak by default; EW removes "matter"'s mlapse; beta_form "detuned" by default). A first H1 call at 13:17:58
on the hands-ON default composed an INCORRECT hybrid (the Dirac pair kept its reciprocal source inside the EW/"lapse"
blocks; recorded as invalid, not a result). The port now REQUIRES the hands-OFF composition (default_system(chiral=False,
electroweak=False), the system Study 10 analysed; apply_hybrid raises otherwise) and skips the beta replacement when the
default is already detuned. H1-H3 run on the hands-OFF system; the hands-ON port is OPEN (EW-BUILDER's lapse x |Phi|^2).

## RESULTS H1 + H2 (written Tue Nov 10 13:20:25 UTC 2026; runs 13:19:00-13:19:01 (H1) and 13:19:09-13:19:13 (H2); results/gravity_hybrid/H1.json, H2.json)
System: apply_hybrid(default_system(chiral=False, electroweak=False)) at Q = 2^33+1 (layers/system.py as of 13:18, sha256
806a6061...; beta_form "detuned" already in the default, so the beta block is kept as built).
H1 PASS: compose OK (integers, B3, acyclic); G = 319 (= the hands-OFF v2 default); hsrc = 688 monomials, all degree 2
(rank 3), 640 with an a-read, offsets <= 1 (on-site / one link); inverse stages [301, 1, 16, 1] (one more stage: F after
L0/Dirac); designations: composed 3490 = default 1202 + hsrc 688 + one-way lapse actions 1600 (formerly reciprocal);
max rank 4 (other blocks); vacuum bit-exact 20 updates ALONE (ref + matter + metric + hsrc) and COMPOSED; random-state
rewind 20 + 20 bit-exact.
H2 (reversor) as PREDICTED: FAIL for the hybrid, PASS for the control.
| seed | control default: F^-t = R* F^t, t = 1..6 | hybrid: mismatching entries at t = 1..6 | first mismatching gear |
|---|---|---|---|
| S2* (A = 2^12) | exact 6/6 (R*-fixed) | 0, 2, 12, 36, 52, 54 | metric.h00 only (t = 2) |
| L0_rstar_e0 | exact 6/6 | 14, 474, 1771, 3911, 6818, 8863 | metric.h00 only (t = 1) |
| L0_rstar_band | exact 6/6 | 8, 370, 398, 453, 494, 536 | metric.h00 only (t = 1) |
R*(s0) = s0 holds for every seed in both systems (the data are R*-fixed); the bounce fails first in the lapse field
exactly as DERIVED: under R*, the lapse's two-time source is evaluated on the pair (m(t), m(t+1)) instead of
(m(t-1), m(t)); the mismatch then spreads to the clocks through the lapse action.
OBSTRUCTION (DERIVED): reversing matter about t and the lapse field about t + 1/2 (F~(s) = F(1 - s)) would repair F's
own equation, but the matter reads F at the matter's own centre t (b-only), which needs F~(s) = F(-s): no time-shift
reversor exists for "two-time source centred at t - 1/2 + one-time action at t". An exact CPT bounce needs the source
moved into a rounding-free accumulator (ST-1's design III mass gear mu, AGREE_ST S22), for which an OD2-type staggered
reversor may exist (B1-GRAV G10): OPEN, not built here.

## RESULT H3 first run (written Tue Nov 10 13:21:15 UTC 2026; run 13:19:52-13:20:17; results/gravity_hybrid/LONG_T20000_detune0.json)
RUNAWAY (registered criterion |U_mean| > 0.25) at t = 500: U_mean 1.5e-3 (100), 2.0e-2 (200), 6.5e-2 (300), 0.14 (400),
0.29 (500), accelerating; U_pi stays small (9e-4 .. 4.7e-3); max |G| 8871 (detuned beta, no corner mode); bits 40 (int64).
The datum total (5.7e13) is ALL L0 (S2* has N_J = 0): the k = 0 imbalance comes from the L0 two-time energy, which is
exact only for a STATIC lapse (G2): as the lapse builds up, the free-H energy of L0 changes at O(U) and feeds the uniform
mode (positive feedback). The registered detune_h00 second run is NOT the relevant one (U_pi is small).
## PRE-REGISTRATION H3 controls (written Tue Nov 10 13:21:15 UTC 2026, before running; same L = 4, same readouts and criteria, T = 2000)
 C1 the plain hands-OFF default with the SAME data (S2* + L0 band seed x 2^6), R-a datum = two-time snapshot mean of its
    b-only source: does the default also run away (then it is the strong dark seed's self-gravity, not the hybrid)?
 C2 hybrid, S2* only (no L0 seed): expected bounded (Dirac part exact; N_J = 0).
 C3 hybrid, L0 seed x 2^4 (16x less energy): if the runaway is the O(U) feedback, its onset moves much later.
- ADDENDUM (written Tue Nov 10 13:25:50 UTC 2026): the first C1 call (13:21:15-13:25:40) gave no output in 4 min (no progressive print; the bit check only every 100 updates let a runaway enter the slow Python-int path); killed; controls re-run with a check every 10 updates (rows every 100), criteria unchanged.

## RESULTS H3 controls (written Tue Nov 10 13:29:58 UTC 2026; runs 13:25:50-13:29:27; results/gravity_hybrid/LONG_control_C*_T2000.json)
| case | data | source | runaway (|U_mean| > 0.25) | U_mean t = 100 / 1000 / 2000 | U_pi at the end |
|---|---|---|---|---|---|
| H3 (registered) | S2* + L0 band seed x 2^6 | hybrid | t = 500 | 1.5e-3 / - / - | 4.7e-3 |
| C1 | same | plain hands-OFF default (two-time snapshot datum) | t = 150 | 0.123 / - / - | 4.7e-2 |
| C2 | S2* only | hybrid | NONE to 2000 | ~0 / -9.3e-5 / -3.5e-4 (rounding floor, sign random) | 1.8e-3 (grows ~linearly) |
| C3 | S2* + L0 band seed x 2^4 (energy / 16) | hybrid | t = 1970 | ~0 / 3.9e-2 / - | 2.7e-3 |
Reading: (1) a strong DARK (L0) seed makes the uniform lapse run away in BOTH laws; the hybrid delays it x3.3 (500 vs 150)
and at t = 100 its U_mean is x80 smaller. (2) The onset scales like 1/sqrt(dark energy) (x16 less energy -> x3.9 later):
a k = 0 positive feedback at O(U): the L0 part is the FREE-H two-time energy, which GROWS as the uniform lapse slows the
L0 clocks (adiabatic |x|^2 ~ 1/sin w), whereas the exactly conserved (lapse-dressed) energy would DECREASE (redshift,
negative feedback); the dressed form is not integer at the 2^-22 scale (its F-terms need 3/2^8; Study 10 §4), and P is
pinned to 2^20 by the Dirac mass granularity (m/4P integer). (3) The Dirac part (rest-mass Wronskian) alone (C2) is
bounded to 2000 with only the rounding-floor drift, while h00's own corner grows ~linearly (AGREE_ST S21).
## PRE-REGISTRATION H3b (written Tue Nov 10 13:29:58 UTC 2026, before running): the long run proper on the bounded case: hybrid, S2* only
(C2 setting), L = 4, T = 2e4, same readouts and criteria (check every 10 updates). Reported: bounded or the runaway time;
U_mean and U_pi histories. (The detune_h00 run is pre-registered as H3c, same setting, T as time allows after H3b.)
- AMENDMENT to the H2 obstruction (written Tue Nov 10 13:31:30 UTC 2026): the named way out (ST-1's mass gear mu with an OD2-type staggered
  reversor) is CLOSED-NEGATIVE at today's integers (AGREE_ST S22 amendment (b), DERIVED by ST-1, confirmed by ST-2): a
  rounding-free accumulator works in units of D x N^, so its source would be ~6e6 x too strong. No exact reversor for the
  hybrid is known at today's integers.
- ADDENDUM H3c (written Tue Nov 10 13:31:50 UTC 2026, before running): case C2D in hybrid_long_controls.py = C2 with hybrid_system(detune_h00=True) (h00 face weight (Q-1)/2, Laplacian form); T = 5000 after H3b; compare U_pi growth with C2/H3b.

## RESULT H3b (written Tue Nov 10 13:42:37 UTC 2026; run 13:30:00-13:41:4x; ST-2_work log H3b.log; no JSON: the run crashed)
Hybrid, S2* only, L = 4: bounded readouts to t = 6300: U_mean -2e-6 (200), -9.3e-5 (1000), -3.5e-4 (2000), -7.6e-4 (2600),
-1.18e-2 (5600), -1.47e-2 (6300) (NEGATIVE: N > 1); U_pi 1.8e-3 (2000), 3.8e-3 (2600), 2.5e-2 (5600), 3.0e-2 (6300);
max |G| 1986; 38 bits at t = 6300. Between t = 6300 and 6310 the run ended with "OverflowError: Python int too large to
convert to C long" (the traceback's line text is from the file as edited later; the failing call is the step or the
readout, not yet separated). Reading (DERIVED, to be checked): with no k = 0 offset datum the uniform lapse drifted
NEGATIVE (rounding walk, here negative) and h00's corner adds +-U_pi, so U ~ -0.045 at some nodes: link factor
1 - 4U ~ 1.18 > 1 violates the CFL bound of the one headroom stencil (B1-GRAV F2) -> sudden runaway.
## PRE-REGISTRATION H3c / H3d (written Tue Nov 10 13:42:37 UTC 2026, before running; controls script now records an engine OverflowError and
checks every update after FINE_AFTER)
 H3c: case C2D (detuned h00), T = 7000: does the corner growth (U_pi) stop, and does the run pass t = 6310?
 H3d: case C2 rerun T = 6400 with FINE_AFTER = 6250: locate the failure update and whether the engine or the readout fails;
      report min U over the nodes at the last good update.

## RESULT H3c (written Tue Nov 10 13:50:30 UTC 2026; run 13:42:37-13:49:5x; ST-2_work log H3c.log; no JSON: the readout overflowed)
Detuned h00 (face weight (Q-1)/2), S2* only, L = 4: h00's corner SUPPRESSED (U_pi <= 1.5e-6 at every sample, vs 3.0e-2 at
t = 6300 in H3b) - AGREE_ST S21 confirmed in the second code. But the uniform lapse still wanders: U_mean -1.7e-4 (1500),
+1.3e-3 (3500), -1.4e-3 (5000), -9.6e-3 (6000), -1.6e-2 (6500), -2.3e-2 (6900); between t = 6900 and 7000 the values ran
away (the readout's float conversion of Sum F overflowed). Horizon ~6900-7000 (H3b without detuning: 6300-6310).
Reading (DERIVED, order of magnitude checked): the Dirac part is exact up to the remainder kicks, and the massless k = 0
lapse integrates that walk twice (ST-1's rounding floor G4): ~1e-2 .. 1e-1 in U by t ~ 7000 at A = 2^16, L = 4; once the
uniform lapse is NEGATIVE (N > 1) the one headroom stencil violates CFL (B1-GRAV F2) and the run explodes. A k = 0 offset
datum (N <= 1 margin) delays it; reaching 2e4 updates would need a margin ~0.2 in U (light speed factor ~0.2): not run.
H3d (pre-registered above) launched now to locate the H3b failure step (engine vs readout).

## RESULT H3d (written Tue Nov 10 13:55:08 UTC 2026; run 13:50:30-13:54:3x; results/gravity_hybrid/LONG_control_C2_T6400.json)
Same trajectory as H3b, bit-identical readouts (U_mean -1.9968e-6 at t = 200 in both). Smooth to t = 6328
(U_mean -0.01484, U_pi 0.0292, U_min = min over nodes of F/2P = -0.0458, i.e. N_max = 1.046), then a CFL-type explosion
in five updates: U_min -0.055 (6329), -0.061 (6330), -0.057 (6331), -1.44 (6332), -55.2 (6333); bits 38 -> 59; RUNAWAY by
the registered criterion at t = 6333 (U_pi 1.81). The exception of the 13:30 run came after this runaway (values >= 2^59);
it is not an exactness failure (whether numpy inside the step or my readout raised it was not separated).
H3 SUMMARY: hybrid + GRAV-FIX (A), L = 4: strong dark seed -> runaway t = 500 (default 150); S2* alone -> t = 6333 (one
stencil) / ~6900-7000 (detuned h00, corner suppressed); 2e4 updates NOT reached. Mechanism: the uniform lapse is a massless
double integrator of the k = 0 source; any residual (dark-sector O(U) feedback; the exact charge's remainder walk) drives
it, and the first negative excursion (N > 1) breaks CFL on the one headroom stencil. Needed for adoption beyond ~6e3
updates at L = 4: a k = 0 control (offset margin, or a law that keeps N <= 1), OPEN.
New-file hashes (sha256): layers/gravity_hybrid.py 8e8aaab5..., prepare/gravity_hybrid.py dd143933...,
tests/test_gravity_hybrid.py 3ca7d611..., demos/gravity/hybrid_long.py a6534a37...,
demos/gravity/hybrid_long_controls.py a58cd1b1... (edited during the runs, as recorded above).
