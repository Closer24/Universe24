# The hostile physicist on the moving clock's three drafts (the edge, the clock click, the half-tooth act)

The report as the reader gave it, 2026-10-30, filed by the Boss (the reader's harness refused to write this file).
Files beside it: notes_01..04, probe_a_two_clocks.py, probe_b_cut_speed.py, probe_c_order_clicks.py,
probe_d_half_falling.py, probe_e_pump_trace.py, probe_f_lump_energy.py, probe_g_root_dial.py with their .txt outputs,
and rerun/ (the three drafts' probes rerun: every output identical to the stored one). Whole numbers on the real act or
on the drafts' own harnesses; the only divisions are tensor24.algebra.carry.carry and edge_lib.split.

VERDICT on the edge: NOT PASSED

## Items, most serious first

1. BLOCKING. The edge's equation of motion is not nature's, and the text says it is.
   - Place: EDGE.md, Physics behind the clicks, first bullet ("the momentum W v is what the clock keeps ... the
     velocities redshift with the clock"); Clock bullet 2; Solution24 addressed, step 7; the head paragraph ("It is
     d_t (W d_t a) = F").
   - Physics: the static act already fixes the clock rate: light's c^2 = grip/W and the hairspring's omega^2 = D/W
     both go as W^(-1/2), so N = sqrt(rest/W). A uniform change of every clock's rate in time is, in nature, a change
     of time coordinate: nothing two clocks at one site show each other can change. The scalar field under a lapse N(t)
     with flat slices obeys d_t((1/N) d_t a) = N (Lap a - m^2 a); with 1/N = sqrt(W/rest) that is
     sqrt(W) d_t(sqrt(W) d_t a) = F, i.e. W d_t v + (1/2)(d_t W) v = F. The act as built and the half-tooth drop the
     (d_t W) v term; the edge keeps all of it; nature keeps half. On a free row nature conserves sqrt(W) v (the proper
     velocity), the edge conserves W v, the others v.
   - Measured (probe_a_two_clocks.txt; one gear with the clock's course given, checked bit for bit against the
     engine's own load and act through edge_lib's board: 0 misses in 400 rounds for the edge and for the act as built):
     the 00 slot rising 1 count a round from W = 10,000 to 40,000 (adiabatic), a free gear v0 = 10^6 and a hairspring
     (push -100 a, A0 = 10^7) at one site.
     - Notches per beat v T against the start (nature 1000): the edge 508 at W x3.8 (3.8^(-1/2) = 0.513); the act as
       built and the half-tooth 1932 (3.8^(+1/2) = 1.949).
     - v^2 W (nature 1000): edge 249 at W x4; as built 4000. The edge's P = 2 D v + s is kept to the bit: it is the
       wrong invariant.
     - The hairspring's amplitude (nature constant): edge A/A0 = 824 at W x2.17 (2.17^(-1/4) = 0.824); as built 1212.
       The beat T^2/W is 989-1000 in every form: the frequency is right everywhere, the amplitude and the velocity are
       not.
     - In proper units a hairspring's quanta fall as W^(-1/2) under the edge and rise as W^(+1/2) under the act as
       built; nature keeps them.
   - Fix: strike "nature's" and name d_t(W d_t a) = F as a CHOSEN form; or build nature's form, which exists on the
     edge's own pattern in whole numbers (probe_g_root_dial.txt): the teeth a square, W = L^2 with L the clock's count,
     the dial given to the roots, D = L(b) + L(a), the push divided once at the pivot's root (its centred quotient, the
     remainder dropped as a coefficient's by rule (ii), or kept on a second edge tooth). Measured on the same course: L
     v within 4 permille, A within 1 permille, T^2/W 999-1000, untick(tick s) = s in 30,000 of 30,000 rounds, the books
     P_(t+1) - P_t = 4 q_F exact; the edge form on the same course gives v^2 W 252 and A/A0 848. The price is a law
     change: the 00 slot enters the root L, not W (Postulate 6's linearity holds for L at first order as it did for W).
     The other route, N = rest/W with the grips and springs reading the 00 slot as rest/W, changes terms 3 and 6 and is
     heavier. The fixed point of item 2 stands in either.
2. BLOCKING. The cut puts the metric's own 00 mode on a second cone.
   - Place: EDGE.md "The one decision it hangs on"; Clock bullet 5; Board bullet 1 ("W_00 = rest"); Physics bullet 3;
     case (vi)'s last sentence; What stays OPEN, first bullet.
   - With the 00 row's teeth at rest a disturbance of the 00 slot travels at c_00^2 = grip/rest while light travels at
     grip/W: in every well the metric's scalar mode outruns light by sqrt(W/rest), in proper units too. Measured
     (probe_b_cut_speed.txt; the example universe through edge_lib's board, a line of 6): at W = 2 rest, T^2 ratio 2012
     permille; at W = 4 rest, 4039 permille. Under the order (the 00 row reads the 00 slot) 1012 and 1009: one cone. A
     signal outside light's cone breaks the law's own reading 5 (D8) and the equivalence principle for the metric's
     own field. GW170817 bounds the tensor modes, which the cut leaves on light's cone, so it does not reach the 00
     mode directly; but no reading of nature gives a metric mode a cone of its own, and the galactic well alone makes
     the gap about 2 x 10^-6.
   - Fix: not the cut. The 00 row must read the 00 slot (one cone); its own tooth cannot be on the edge (the fixed
     point is a theorem: no dial can be moved by its own quotient), so the metric's own gear needs a law of its own,
     named OPEN, derived before term 5.
3. MINOR. "The energy with a moving W: not checked here" is checked here: the edge's adiabatic invariant is E/omega
   (A^4 W = 1002, 1003 permille over W x2.17; after one full swing the amplitude returns to 998 permille and a free
   velocity to 999,900 of 10^6). The act as built is adiabatically clean the other way (A ~ W^(+1/4)). Within every
   swing both breathe, oppositely; nature does not breathe. For term 9: a uniform notch of the 00 slot is in nature
   unobservable, and under the edge every amplitude breathes by W^(-1/4) and every free velocity by 1/W within each
   beat of the notch.
4. MINOR. The floor's pump: the removal is right, the words overreach. Right: the centred split is round-to-nearest with
   ties to even, the unbiased discretisation of a velocity (probe_f_lump_energy.txt: at strides 1 to 10 the act as
   built's energy grows to 2162 permille by round 3000, the edge's stays within 837-1217; at strides 100 and 3000 the
   acts agree). Overreach: "sources nothing" holds for the strides-squared source alone; the exact source still reads
   the frozen hand's energy (probe_e_pump_trace.txt: the hand freezes at a = 0 holding half a notch of momentum and
   sources p^2/(4D) for ever; one site has no Laplacian, so the 00 gear accelerates: the zero mode). Fix: write the
   removal as a statement about the floor; retire the strides-squared source for the kept momentum squared in term 5;
   rerun G2's lump on a board of the edge form. The edge does not bind a hand in space (term 6's and G3's).
5. MINOR. The lays are no physical regime: W moves by whole grips a round, W x5 in 40 rounds. Fix: one adiabatic lay
   (the 00 slot moving by a count a round at W of 10^4 counts), the physics sentences measured there.
6. MINOR. Term 11 on the edge: the negation law of the centred split is exact (7212 cases 0 misses; keys 1 to 40, 4960
   cases 0; 6000 rounds 0). One line for G5: a key in board units counts a different number of quanta at two depths of
   the clock; the proper wind is D W/rest.
7. MINOR. The tie taken even and the lost shift covariance: the tie rule is the unbiased one, the 2 is the doubled dial
   and not a strength, no law asks a boost of a count's velocity. Agreed; the gate's reading is Sofer's.

## The cut against the order

Neither is physically right; the order is the admissible one. The cut gives the metric's 00 mode its own cone (2012
and 4039 permille in speed squared at W = 2 and 4 rest) and makes the clock's own gear the one gear no depth slows; the
order keeps one cone (1012, 1009). The order's price, measured (probe_c_order_clicks.txt): the 00 row keeps the
as-built law (velocity not redshifted, P_00 -4640 -> -908 while every edge row keeps P to the bit); on a uniformly
falling clock its teeth overflow, 29, 64 and 65 clicks of 27 gears in 36 rounds falling by 1, 2 and 3, each click
moving the clock's own count by a whole notch at one site; the round runs back only with the booked line (15, 8 and 9
of 36 without). In the clicks' spacetime the order's 00 click is a jump of the local clock rate by a whole count with
no partner clock and no source: not two clocks connecting or coming apart; its time reverse exists only in the
runner's record, so the act alone is no bijection there. At the real calibre the overflow is rare; term 9's notch is
where it lives. Verdict: the order's one cone, with the 00 row's own law OPEN by name.

## The half-tooth act against the edge

The half-tooth keeps the act as built's physics (v T 1932 permille, A ~ W^(+1/4)) and does not run on a falling clock
(probe_d_half_falling.txt: 0 of 24 rounds falling, 24 of 24 rising). Its merits are real: the 24 and the 48 on a rising
clock with no change to term 2, the drift bounded, the proof that the flip must be read in the reading round's teeth.
The edge runs both ways exactly with no promise and no line, keeps P to the bit, holds the 24 at every D and removes the
pump; its physics is wrong by the same factor the other way. As algebra the edge beats the half-tooth; as physics
neither is nature; the root dial (probe G) has the edge's algebra with nature's physics, fixed point and law change
included. W d_t v = F is a choice, not a consequence of the exact run back.

## Sound, with numbers

- The 24 on the edge: 24 of 24 at every one of 40 rounds on all seven lays (rerun identical); the mutants 3 of 24.
- The mirror its own inverse 41 of 41; untick(tick s) = s 40 of 40 on every lay; the act as built 1 of 40 falling.
- P kept to the bit on every lay; with a spring P moves by exactly 4 x the pushes' sum; on an adiabatic course P is
  constant over 30,000 rounds.
- The still clock state for state; the fixed point's formula and cover count; the split's negation law; the click's
  books.
- The floor's pump removed below half a notch; the drift's uniform vector gone.
- The edge's adiabatic invariant E/omega; T^2/W = 989-1000 in every form.
- CLOCKCLICK's and CLICK25 section 1's numbers reproduced to the bit.

## For Solution24

Step 7 should say that a moving clock is tested first on the uniform case, adiabatically: a uniform change of every
clock's rate must change nothing two clocks at one site show each other (notches per beat, a hairspring's amplitude),
and no form is written "nature's" before that measurement.
