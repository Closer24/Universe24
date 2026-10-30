# Reading the fifth text (TERM5_FIFTH.md, head 6b77872dc; the act's gear part unchanged from 9868ae570 by the diff:
# step.py changes are the click's passing, the Layout's mesh plan, contract's zeros_like; gear(), split(), stress() as before)

## Item 1 (the form), as answered
P_slot = -dH/d slot with H the leapfrog invariant on the kept momenta (my 16H):
  P_00 = +k0 (1/2) sum_{rows != 00} v_in v_out   -> plan: k0 x si so at the drive's dial T_d = 2
  P_ii = -k1 (1/2) sum_rows [(Delta+_i)^2 + (Delta-_i)^2] -> plan: the two Meshes' stretches squared at the now slot, dial 2
  P_jk = P_0i = 0 (no reader)
Sign check: H as a function of (M, slots): dH_matter/dc00 = -(1/2) v^2 (E = M^2/2W falls as W rises: measured in my probe_b),
so P_00 = +(1/2) v^2 > 0 (clocks slow) and the 00 gear takes what the matter gives up. The ii: dV/d(ii) = +(1/2) k1 Delta^2
-> P_ii < 0 (grips fall). Both signs right, the magnitudes fixed, no eta L term: this IS v (x) v on the read slots, the law's
form for the scalar as I derived it. "gamma = 1 on dust" struck, the tent's 48 g^2 struck. ACCEPTED in form.

## Item 2 (the books), as answered
The strength is the dial 2 (the quadratic form's half) with the plan at factor 1 (k0 on the 00 terms): no number chosen.
Measured (out_f): dust 1000 permille; held tent 1000 to 8 digits; held bump 1000; free tent 1133; free bump 1041.
Their cause: the exact invariant pairs stretch_now x stretch_next (non-local, the neighbour's next); the local mirror-exact
reading now^2 is first order in the stride per stretch per round. For light v = c delta, so the residual should go as
c x (curvature/stretch) ~ c / width: TEST: does it halve when the bump's width doubles? If yes: discretization, OPEN
with its cause is fair. If no: a form error.

## The new consequence: gamma for light is set by the READ factor k0, not by the books
h_ii/h_00 = 24 (k1/k0)^2 delta^2/v^2 = 144 (k1/k0)^2 for light (delta^2 = 6 v^2). As loaded k0 = k1 = 1: 144 (measured
131837 permille on their not-quite-null bump); at k0 = 12 = Spokes x senses: 1 (measured 915). The fourth text's S on the
push (which broke the books by S^2) was the 12 that belongs on the read: one unit (the half grip) for every slot.
The Boss keeps k0 = 1 for the night (NOT_CLOSED). As built, light's gamma = 144: bending 72x Einstein's for the clock's well.
This is the one remaining blocking point; the text has the fix in hand (k0 = S, "one unit for all ten slots", read from the star).

## Checks to run
R1 rerun probe_f, probe_f7 (copies in t5f_phys/rerun5/, so their out_*.txt are not overwritten), diff.
R2 probe_n: (a) gamma on a near-null TRAVELLING pulse under the books' form at k0 = 1 and 12 (expect ~144000 and ~1000 x G/K);
   (b) the books at k0 = 12 on dust, the held tent, the travelling pulse; (c) the residual against the width: bumps of
   half-width 4, 8, 16 (boards 12, 24, 48 x 3 x 3), standing and travelling, at k0 = 1.
