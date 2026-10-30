# Notes 03: the hostile self-check (the law of findings), 2026-10-30

- Every probe rerun from scratch into rerun/: five of five byte-identical (probe_fb1 .. probe_fb5).
- No float, true division, root, round, math, random, fractions or decimal in fb_lib or the probes; the floor divisions
  that had crept into three print lines were replaced by the carry and the outputs re-diffed (identical).
- Theorem 2 (c), re-derived: a release needs tau >= D_in - 2 L_0, so D_in - 1 - tau <= 2 L_0 - 1 < 2 L_0 <= D_out;
  (b): tau+ = tau + 2 L_0 - D_in < 2 L_0 since tau < D_in. Both need D >= 2 L_0 at every slot (the domain).
- Cases built to pass my stated rules and break the form (probe_fb5): the clock halving over five steps, doubling,
  reaching L_0 exactly at one slot with 4 L_0 at the other, swinging between 0 and 10 L_0 by its own spring, a step
  every 21st round, tau laid at 0 and at D - 1, a ring of 32, two clocks on one Mesh for 400 rounds: the run back
  exact in every one; outside the domain (c = -L_0 / 2) the escapement turns 2 and the run back fails 20 of 20, as
  the theorem says, named by the promise.
- The first form (the escapement at the now slot's dial alone, the mirror a plain swap) FAILED the run back on every
  stood round (10,000 of 30,000 rising): kept in 02_mirror_finding with the five dead ends; the symmetric dial and the
  escapement's own quotient in the mirror are what fixed it; then the two-site Mesh case (probe_fb5 H) failed 50 of
  400 under the plain swap and passed 400 of 400 once the stood Node-clock was no longer swapped.
- What a hostile reader will still press: the law's line 35 (W linear at the now slot) becomes L linear at both slots
  with W a second-order reading; the domain c >= 0; the mirror not an involution on a moving clock (Theorem 3); the
  half-step reading of the clock in the escapement's dial; term 5 and term 9 untested with it. All named in FWDBACK.md
  section 6, none hidden, none written CHOSEN.
