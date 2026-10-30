# The clock click, measured (probe_cc.txt, 2026-10-30; the engine's own load and act, 486 gears, whole numbers)

The lays: standing W = 10; rising by 1 from 10; rising by 2 from 11 (odd, Form 4's); per site (the 00 slot in [20, 24]
with its velocity in [-1, 1], so W rises at some sites and falls at others, the 00 row pulled by its neighbours); falling
by 1 from 46. The teeth drawn in [0, 5]; the centred and edge forms negate a flipped tooth, the act as built flips it in
the teeth that kept it. Counts within 10 bits everywhere.

## 1. The 24 (16 rounds, of the 24 turns; the departing gears over the 21 sign-flipping turns)

| form | standing | rising 1 | rising 2 (odd) | per site | falling 1 |
|---|---|---|---|---|---|
| the act as built | 24 all | 24, then 3 (28 gears at round 2, 216 at 16, delta a to 12) | 24, then 3 (34; 216, to 16) | promise breaks before round 2 | promise breaks before round 2 |
| Form 1, literal | 24 all | as the act (same arithmetic) | as the act | 24, then 3; 85 lines | 24, then 3; 136 lines |
| Form 2, scaled | 24 all | 3 at every round; 5650 lines | 3 all; 5801 lines | 3 all; 3351 lines | 3 all; 5867 lines |
| Form 3, momentum | 24 all | 24 all, but the clock stopped (below) | 24, then 3 (24; 216, to 8) | 24, then 3 (8; 202, to 6) | 24, then 3 (16; 216, to 15) |
| Form 4, centred (withdrawn) | - | - (W even) | 24 all | - | - |
| the edge (cut) | 24 all | 24 all | 24 all | 24 all | 24 all |
| the order: 00 click first | 24 all | 24 all | 24 all | 24 all; 4 lines (the 00 slot's) | 24 all |
| the order, 00 row as built | 24 all | 24 all | 24 all | 24 for 3 rounds, then its promise breaks | 24 all |

Form 3 on the lay rising by 1: the 00 slot's own momentum U = W(b) v + r = 9 x 1 + 0, re-split at W(a) = 10, gives q = 0
and the tooth 9: the 00 slot stands at 4 for ever (its count by round 4, 4, 4, ...; the act's 4, 5, 6, ...), so W
stands at 10 and the 24 hold on a clock that no longer moves. Rising by 2: the 00 slot climbs 5, 6, 7, ... 13 and
stops at 13 (the act's 5, 7, 9, ...). Form 3 changes the clock's own motion; the edge and the order keep it as laid.

## 2. The forward drift, 40 rounds, the 14 free rows' S = SUM (a - b): S_40 - S_0 summed, fell / rose, largest |S_t - S_0|

| form | rising 1 | standing 10 | rising 2 (odd) | standing 11 | books (misses over rows x rounds) |
|---|---|---|---|---|---|
| the act as built | -371, 14 / 0, 29 | -81, 14 / 0, 11 | -470, 14 / 0, 37 | -89, 14 / 0, 11 | W_t dS = R_t - R_t+1 + SUM push: 0 |
| Form 1 | as the act | as the act | as the act | as the act | the act's: 0 |
| Form 2 | -371, 14 / 0, 29 | -81, 14 / 0, 11 | -288, 14 / 0, 24 | -89, 14 / 0, 11 | none closed (the residue leaves the state) |
| Form 3 | -67, 8 / 6, 51 (clock stopped at round 1) | -81, 14 / 0, 11 | -78, 6 / 8, 232 | -89, 14 / 0, 11 | U_t+1 - U_t = SUM push: 0 |
| Form 4 | - | - | +17, 2 / 11, 7 | +17, 2 / 10, 5 | W_t dS = C_t - C_t+1 + SUM push: 0 |
| the edge (cut) | +88, 5 / 9, 338 | -5, 6 / 5, 5 | +83, 5 / 9, 374 | +4, 3 / 9, 4 | P_t+1 - P_t = 4 SUM push: 0 |
| the order (00 first) | +88, 5 / 9, 338 | -5, 6 / 5, 5 | +83, 5 / 9, 374 | +4, 3 / 9, 4 | the 17 edge rows as the edge, 0; the 00 row P_00 grows by 4 dW SUM v: 0 |

The act's one-signed fall (14 of 14 rows, -24 to -29 each, the uniform vector along (1, 1, 1)) is gone on the edge
and on the order: the rows move both ways, by their own momentum re-split at the growing dial (the redshift: t1 x,
S -15 -> -10 -> -4 -> -5 -> -3 at D 19 -> 99, P -607 kept at every round; a1, S -72 -> -11, P -2743 kept; the act's
t1 x S -15 -> -43 with P = W S + R -101 -> -1509). The large |S_t - S_0| on the edge (338) is the redshift of a row
laid with |S_0| = 334 (0z), not a drift: P closes to the bit. Standing, the edge's S moves within 5 against the act's 11.

## 3. The mirror twice and the run back, 40 rounds (gear-states of 19926; untick(tick s) = s per round)

| form | rising 1 | falling 1 from 46 | per site |
|---|---|---|---|
| the act as built | mirror twice moves 19926 of 19926; back 40 of 40 | promise before round 2 | promise before round 2 |
| Form 1 | 19926; 40 of 40 (no line needed) | 19926; 40 of 40 with the line, 1 without; 690 lines | 9036; 40 of 40 with, 3 without; 144 lines |
| Form 2 | 0; 40 of 40 with the line, 0 without; 14509 lines | 0; 40 with, 0 without; 14344 lines | 0; 40 with, 0 without; 8460 lines |
| Form 3 | 486; 39 of 40 (no line exists); rewind False | 19926; 0 of 40; False | 11610; 0 of 40; False |
| Form 4 (12 rounds) | rising 2: 0; 12 of 12; no clicks | falling 2 from 41: 0; 12 of 12 with the line, 1 without; 23 to 35 clicks a round | - |
| the edge (cut) | 0; 40 of 40; rewind True | 0; 40 of 40; True | 0; 40 of 40; True |
| the order (00 first) | 0; 40 of 40; True | 0; 40 of 40; True | 0; 40 of 40 with the line, 33 without; 7 lines (the 00 slot's) |
| the order, 00 row as built | 1107 (the 00 row's 27 gears x 41); 40 of 40 | 1107; 40 of 40 | promise before round 4 |

## 4. The 00 slot's own click (the order), a lay where the 00 slot falls past its tooth

The 00 slot per site in [8, 11], its velocity in [-1, 0], its tooth drawn in [-24, 24]; 10 rounds; W_00's least by round
14, 14, 13, 12, 12, 11, 10, 10, 9, 9, 9. The order: the 24 hold 10 of 10; mirror twice 0; the 00 slot clicks at 2, 4,
0, 0, 0, 1, 0, 2, 2 gears in rounds 2 to 10 (each sheds one whole count: at round 2 the sites 1 and 19); untick(tick s)
= s in 10 of 10 with the line and 5 of 10 without; rewound to the start with the line. The edge (cut) on the same lay:
the 00 row's teeth at rest 6, no click, exact 10 of 10 with nothing booked. The other reading (the 00 row by the act as
built) breaks its promise after round 1.

## 5. Small facts

Form 1 is the act: carry(n, W, r) = carry(n, W, r mod W) + (r div W, 0), 0 misses over W in [1, 14], r in [0, 59], n
in [-40, 40]. Form 2's flip: at W(b) = 10 to W(a) = 11 the scaled tooth misses the flip at 10 of 10 teeth. Form 3 at
the 00 row (rest 6, a = 10): 27 sums U reached from two or more (b, r), U = 15 from (-5, 0), (9, 0) and (10, 15).
The even-tie rule of the split is not shift-covariant (edge probe section 7), so the 00 slot's booked count is read from
the whole re-split, k = split(4 W v + t, 4 W).q - v, not from the tooth alone: with the tooth alone the run back held 7
of 10 in section 4; with k, 10 of 10.
