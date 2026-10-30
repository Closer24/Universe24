# Notes 02: what the three drafts and the G2 physicist say, and my first reactions

## EDGE.md (revised 16:1x): harness now reads examples/tensor24/universe.json (light A1 x2, metric square), cube 3,
12 rows x 27 sites = 324 gears. Lays in grips (1 grip = den Gamma^2 = 1.5e22 counts = 1/6 of the rest teeth!). The
lays move W by whole grips a round: W 10 -> 50 grips in 40 rounds (x5 in 40 rounds). Violently non-adiabatic; fine for
exact-arithmetic claims (24, mirror, books), useless as a physical regime for redshift ratios.

Claims measured (their probe_edge.txt, to be rerun): 24 of 24 on all 7 lays; mirror involution 41/41; untick 40/40
rising and falling; P = SUM(2 D v + s) exact (P_40 - P_0 = 0 every row); still clock state-for-state; fixed point
formula; even-rule cost (620 ties of 4812); click books 0 misses keys 1..40.

New: the floor's pump (probe_pump.py, on the G2 physicist's one-site replica). A: at rest, push k: as built (tooth 0)
answers -1 for every k in [-W, -1]; edge answers 0 for |k| <= W/2, +-1 beyond, symmetric. B: a free gear with
momentum m: as built/p-form moves floor(m/W) a round (-1 for m = -1!), edge round-to-nearest (ties to even = banker's
rounding). C: hand on spring at rest with |m0| <= W/2: p-form swings on the floor (mean p ~ W/2, strides' squares
18..105 million over 12000 rounds), edge stands still (source 0). D: readers' check F on the edge: W stays 3000 for
p0 = -1, -300 (p-form wound to 19010 and 31877); from one notch up both wind W without bound (one-site replica, no
Laplacian: the zero mode). Named remainder: between half and one notch the strides' squares over-count 1441 permille.

My reaction: the pump's removal is right (round-to-nearest is the unbiased discretization; floor is one-signed and
gives a whole-notch stride to a 1/3000 velocity). "Sources nothing" holds for the strides-squared source only; the
exact source (p^2) still reads the frozen hand's energy, as it should. Under the exact source + edge, the p0 = -3000
hand drives W 3000 -> 155094 doubling every 2000 rounds: a frozen displaced hand (a = -1) whose spring pumps its tooth
linearly while the dial outgrows it. To trace (probe E).

## CLOCKCLICK.md + MEASURED.md: Forms 1-4 refused by their own numbers; the edge and the order both 24 of 24 on all
lays; the order's 00 row: tooth kept on 4W(a), read on 4W(a+): clicks (whole count leaves, booked) on a falling clock,
2-4 gears a round at W ~ 10, |dW| = 1 (rate ~ |dW|/W); run back 10/10 only with the line, 5/10 without. The 00 row's
P grows by 4 dW SUM v (the as-built law for the 00 row: velocity not redshifted). The other reading (00 row as built)
breaks its promise. Form 3 "holds the 24 by stopping the clock" (a good catch by that deriver).

## CLICK25.md s.1 (half-tooth): u in [0, 2W(b)), shifted by W(a) - W(b), the act as built at doubled teeth. 24 of 24
rising; mirror involution; drift bounded like the standing control (-62 vs control -81 vs built -371); keeps
W d_t v = F ("the momentum form is not time-symmetric ... what the metric's motion does to a wave's momentum is G2's").
Falling clock: promise breaks at the lay (178 of 486 gears below the zero mark). Its own words: not mended.

## G2 physicist (g2_phys/READER_PHYS.md), items I lean on
- T13 item 1 BLOCKING: the floor pump (uncentred tooth, floor(p/W) = -1 for -W < p < 0): hand with p = -1 winds W to
  19010 by round 12000 (f_results). The edge answers exactly this. Good.
- T13 item 3 MINOR: "in the clicks a uniform W is unobservable (every proper-time ratio unchanged); the observable is
  the grips' mean". EXACTLY my point about the moving clock: a uniform W(t) is a change of time coordinate. Any form
  that makes a uniform W(t) do observable work on free gears or hairsprings is against nature. All three do; the
  edge by W^(-1/2) in proper velocity, the others by W^(+1/2).
- e_adiabatic: on the p-form (as built), with large strides, E^2 W kept within 5 percent while W grows 24-fold, i.e.
  E ~ W^(-1/2) under the as-built act WITH the hand winding its own clock. Hmm: that is the as-built with a self-sourced
  W (the hand's energy drains into W: not a free uniform lapse but a back-reaction). Not the same test as mine (mine:
  an externally driven uniform W, no back-reaction). Keep apart.
- c_lump_well: the lump's energy leaves the centre in tens of rounds (nothing binds a hand in space) and the floor
  pump inflates it 100-fold. The edge removes the inflation, not the dispersal.

## The plan of my probes (whole numbers; tensor24.algebra.carry.carry and edge_lib.split as the only divisions)
A. Two clocks at one site on a uniformly, slowly deepening clock: a free gear (v) and a hairspring (period T). Nature:
   notches per beat v*T constant (all clocks slow alike). Edge: ~ W^(-1/2). As built / half-tooth: ~ W^(+1/2).
   Also: S^2 W (proper-momentum squared) and the hairspring amplitude A (A^4 W const under the edge).
   Check the single-gear harness against the real act on edge_lib's board for the first rounds (uniform row, spring).
B. The cut: the 00 row's standing-wave period against the light row's at uniform c0: period^2 ratio = W/rest
   (2.0, 4.0); under the order (00 row reads itself) ~ 1.
C. The order's 00 click rate ~ |dW|/W; the 00 row's velocity not redshifted (P_00 grows).
D. Half-tooth on a falling clock without the promise: untick(tick s) fails (where).
E. The pump's exact-source feedback trace (frozen displaced hand).
F. Term 9's notch: one full uniform swing W0 -> 2W0 -> W0 under the edge and the as-built: do v and A return?
