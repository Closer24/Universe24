# Notes 06: the control (P4) and the verdict's items

## P4, the push-parity control (probe_p4_push_control.txt)
Odd periods (F = 1/5, 1/15, 1/63) and aperiodic pushes (a linear congruence, mean 1/4 and 1/16) give the same picture as
P1 D: symmetric = order, v = 1 locked (v^2 / 2F = 2500, 7500, 31500 permille; 2000, 8000 aperiodic); the carried dial's
velocity runs away (225,627 permille at F = 1/5: v = 9.5 a round; 283,220 aperiodic 1/4: v = 11.9, the same digits as
the periodic case); the twin twice that. The runaway is generic, not a resonance with my push's period.

## Files
tgp_lib.py; probe_p1_lockin.py/.txt; probe_p2_cone.py/.txt; probe_p3_swing.py/.txt; probe_p4_push_control.py/.txt;
rerun_tg9_live.txt (identical to the text's), rerun_tg7_live.txt/.err (board parts fail on node-live: KeyError 'chosen');
notes_01..06. All probes run with live/.venv/bin/python -I; whole numbers; carry the one division; the root the text's own
nearest_root.

## Verdict: NOT PASSED
BLOCKING 1: nature's form is claimed where the clock does not sit; at |v| <= 1 (the text's own calibre words) the root
  form's clock course is the as-built course at every mark (P1 A, C, D; P4; P3 A = 20, 5): v = 1 locked, 1.4-5.7 x
  nature's under pushes of 1/4 .. 1/64 a round, 2 x from a sub-notch kick, W 3.56 x nature's at 100 W0 free (t^(1/3)).
BLOCKING 2: "nature's" for the lapse itself is a choice of the v^2 coefficient (0, 1/4 covariant, 1/2 the text's, 1 the
  edge); nature gives a uniform lapse no equation; the test-field derivation (mc_phys item 1) is misattributed to the lapse.
MINOR 3: the cone 1008/1006 is a baseline artefact (drift-free 1000, 997-1000; 1000 at A/10); the mean's drift is the
  zero-mode pump, upward, quadratic, A^2: +0.5 percent of W in 6000 rounds at A = grip/1000, +42 percent at grip/100.
MINOR 4: the books: the identity is the law; no integer invariant (proof); by windows v^2 W 537-1852 permille at v0 = 3.
MINOR 5: "about 26,600" is 31,15x (the probe's own 2115 permille).
MINOR 6: provenance: t24b; the board probes cannot run on node-live.
MINOR 7: the alternatives' costs under-measured: the push runaway (carried, twin), the twin's parting under its own swing
  (975 at 5 percent x 500 swings; chaotic at 20 percent, |A - B| 2.6 A); the register NOT pumped by the swing (|E| <= 466
  of 2 x 10^6); at v0 = 1 free the carried W is closer to nature's than the symmetric (1.8 x against 3.6 x at 100 W0).
MINOR 8: the symmetric form's promise is unstated (M >= 0, u >= W(a) + 1; 96 of 300 states at rest 6 without an image).
MINOR 9: the sub-notch swing's period is wrong in every form (130 and 220 against 140), the forms coinciding.
MINOR 10: the measured board mixes the 00 row's c = 1/2 with the edge's c = 1 on every other row; its "books" are the edge's.
