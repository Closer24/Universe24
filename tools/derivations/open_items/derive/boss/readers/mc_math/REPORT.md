# The hostile mathematician on the moving clock's three drafts (the edge, the clock click, the half-tooth act)

The report as the reader gave it, 2026-10-30, filed by the Boss (the reader's harness refused to write this file).
Probes and outputs beside this file: mc_lib.py, probe_mc1_half.py, probe_mc2_promise_gap.py, probe_mc3_collisions.py,
probe_mc4_symmetry.py, probe_mc5_key.py, probe_mc6_pump.py, probe_mc7_plan_twosquares.py (each -> .txt), rerun/ (the
three drafts' own probes rerun), and the notes 00 to 02. Whole numbers only; tensor24.algebra.carry.carry the one
division; src untouched.

VERDICT on the edge: NOT PASSED

Read: scratchpad/edge (EDGE.md revised 16:1x, edge_lib.py, probe_edge/record/pump), scratchpad/clockclick
(CLOCKCLICK.md, MEASURED.md, cc_lib.py, probe_cc), scratchpad/click25 section 1 (halftooth.py, probe_clock/drift/48).
Every stored probe output of the three drafts reruns byte for byte (warnings aside), and every number on the revised
EDGE.md is its probe's. The act itself is sound: a bijection on every clock, the 24 and the run back bit for bit, the
books exact. What fails is the derivation's one CHOSEN point and the law text built on it: the tie rule is not
load-bearing, the text's own mutant was refuted with the wrong mirror, and the proposed case (vi) adds a rule the law's
(i) and (iii) already supply. Rewriting, not new physics, is owed.

## Items, most serious first

1. BLOCKING. The tie rule ("where the remainder lands on the dial's edge the count is taken even") is presented as
   forced; it is not, and case (vi) rests on that.
   - Place: Algebra "The split"; "The 24" ("the centring is load-bearing, not a convention"); "The even-count rule's
     cost"; Measured 1 and 6; line 122 (vi) and the touch on line 100; OPEN item 3; Solution24 item 3; Clock bullet
     "the tooth 0, the middle, is what the forward and the backward Node-clock share".
   - Measurement (probe_mc1_half.txt): the half-open convention s in [-D, D-1], which is edge_lib.split_up itself
     (the text's mutant), with the mirror s -> -1 - s (the law's (iii) r -> m - 1 - r on the dial m = 2D): one
     carry, no lit(), no tie. Algebra: bijection 0 misses of 7,212; split(-n - 1) = (-q, -1 - s) 0 misses;
     split(n + 2Dk) = (q + k, s) 0 misses for k = 1, 2, 3, -1, -5. On the edge agent's own board, six lays (standing;
     rising 1 grip; rising 1 grip + 1, D odd; falling 1; falling 1 grip + 1; falling 3), 40 rounds: the 24 24 of 24 at
     every round, mirror twice = s 41 of 41, untick(tick s) = s 40 of 40, rewound True, P books 0 misses, 78 to 82
     bits. Shift covariance on the board: 0 departures for k = 1, 2, 3 even with all 27 carries of the row laid on the
     centre-0 split's tie (the centre-0 act departs at 27 of 27 for k = 1 and 3). Still clock, W = 9 and 10 grips: a
     and b equal to the act as built 40 of 40 with s = 4r - D; the cell (s + D) div 4 is the built tooth at every
     gear; the mirror -1 - s lands in the cell of the built mirror W - 1 - r, 0 misses of 41 x 324. The text's "3 of
     24" is the half-open act judged with the negation s -> -s: the two mismatched pairings each give 3 of 24 on the
     lays with ties and 24 of 24 on the tie-free D-odd lays. Under J laid through the tables the half-open holds
     alike (item 6).
   - True in the text: the tooth must be RE-CENTRED from D_in to D_out (kept as its offset from the dial's half); the
     plain carry in the floor coordinate fails because its flip's centre moves with the dial. False: that the centre
     must be the integer 0 with a tie rule. The real content of the centre-0 choice is line 100's wish that the
     rounding be odd under p -> -p at every p, including the exact half notch. Its real cost is a theorem: any tie
     rule odd under negation obeys f(1 - q0) = not f(q0), which forbids f(q0 + k) = f(q0), so no odd tie rule is
     shift covariant. The half-open keeps covariance and (i), (iii) unchanged; its oddness fails only at p = D mod 2D,
     where the rest state is the conjugate pair {0, -1}.
   - Fix: (a) write (vi) minimally: "a kept remainder belongs to the edge between the gear's two slots and is counted
     from the half of that edge's dial m = 2 (W(before) + W(now)); the round adds the half of the dial it splits at
     and carries there, keeping the offset; (i) is the offset 0 and (iii) is r -> m - 1 - r as written; a change of
     the teeth moves no tooth"; (b) put the tie-even rule to the owner as a separate decision with both sides
     measured (oddness at the exact half notch and one rest tooth, against shift covariance, one carry against two and
     lit(), and the click's count at the ties, item 2); (c) strike "load-bearing", the 934-of-934 and 3-of-24 lines as
     evidence, and "the one CHOSEN point ... with its measured cost"; (d) note that under the half-open the drive's
     remainder r_d already obeys the same (iii): the text's OPEN item 2 ("one split for every carry") closes by
     itself.
2. BLOCKING. "That retires term 11's 'the key odd' item" is overstated and hides a cost.
   - Place: Physics bullet 5; Algebra "The click's books"; Measured 8; Solution24 items 5 and 12.
   - Measurement (probe_mc5_key.txt, keys 1 to 40, areas within 3 keys, 4,960 cases): the floor born at (key - 1) div
     2 and CLICK25's half-tooth born at u = key: books q(A) + q(-A) = 0 miss 0 at odd keys, 120 at even keys; one key
     added is one more count, 0 misses. The centre-0 tie-even: books 0 misses at every key; one key added is one more
     count misses 120, every one a tie; a hand fed exactly one key a round from a tooth on its edge clicks [2, 0, 2,
     0, ...]. The half-open: as the floor. Giver/taker at key 12: the floor forms 900 of 6,000 not opposite, the
     centre-0 0; key 13: all four 0 of 6,000. At an odd key the centre-0 split has no tie: it coincides with the floor
     and has both properties.
   - So the tie-even rule buys the books at an even key with the count's covariance ("one winding, one click"); the
     odd key is the one case where nothing is traded. Fix: "under the tie-even split the books close at every key, at
     the price that a whole key added at a tie counts 0 or 2; the odd key keeps both and stays CHOSEN unless the owner
     takes the trade".
3. MINOR. The promise is stated on the state the round starts from, but the round splits at a dial read from the next
   00 count (probe_mc2 A: W(a) = 3 grips, W(b) = 13, v_00 = -10 grips gives D_out = -4 grips). Fix: the runner's
   promise reads D_out >= 1 through the 00 row's standing split, one carry before the round.
4. MINOR. Section 6's count is off by one and its picture is wrong for q <= -1 (probe_mc2 B: the formula sums to
   1,600, the probe counts 1,560). The conclusion (no bijection) stands. Fix: "the next cell's floor less this cell's
   ceiling is (2q + 1) dD; one fewer integer is missed, and for q <= -1 the cells fall back over one another".
5. MINOR. "The clocks' read acyclic" is implemented and measured as "the 00 row's self-read cut" (probe_mc7 B: with
   two four-vector squares both moving, 2 reads between the 00 rows remain and the run back fails; with every read
   onto a 00 row cut, 12 of 12). Fix: state the generic rule "a row whose count the clocks read reads no clock", and
   say the probes measure one square.
6. MINOR (a point for the edge). The 24's hypothesis "J laid through the tables" is not measured by the text, and the
   probe's turned state would fail it (turned_edge moves the drive's tooth unflipped). Measurement (probe_mc7 A,
   SYM24's plan 1, s = 3, T_k = 2, T_d = 5, 4 rounds, standing, rising, falling): both conventions 24 of 24 at every
   round with r_d flipped in T_d on a flipped row, run back exact; with the probe's own turned state 3 of 24; the act
   as built 24 standing, [24, 3, 3, 3] rising, breaks falling. Fix: flip r_d on flipped rows in turned_edge and add
   the measurement.
7. MINOR. probe_pump's reading. The (i)-born act at k = -1500 moves 0, not -1. probe_mc6 A: the p-form hand born at
   the law's (i) stands as the edge's for |m0| <= 1500 with the floor source 0: the pump is the birth at 0, which (i)
   removes too; what only the edge has is 0 energy at rest under the exact source. probe_mc6 B: under the exact
   source the 00 gear's momentum crosses half a notch near round 12,500 (W = 6,492 at 16,000 and 10,492 at 20,000).
   Fix: "removed by centring, which the edge has by construction; under the exact source the zero mode returns after
   about 12,500 rounds".
8. MINOR. The record check is a one-gear world (examples/tensor24/setting.json lays one light gear): "a and b equal at
   every one of the 1,280 count lines" measures the world, not the acts. Fix: say so, or lay pushes near half a notch.

## The cut against the order

The cut is the exact one; the order is not an act on the state. On a falling clock the order's 00 row (tooth kept at
4 W(b), split at 4 W(a)) maps 625 valid states onto 529 images, 96 collisions (probe_mc3): no mirror or promise can
run it back, the "booked line" is a hold outside the state, Postulate 2 fails on the state alone, and it crosses "the
time gear's turn is no click". The edge with the cut: 0 collisions of 573 on the same clock; untick(tick s) = s at 0
failures of about 2,000 exhaustive two-gear states on four clocks (probe_mc4 A); 40 of 40 and rewound on every lay.
Notes: (a) both resolutions compute the 00 row's count before the others' D_out; what differs is the 00 row's dial, 2
rest (cut) against 2 W_00(now) (order), and the order's 00 row is exactly the half-tooth act's situation; (b) the
cut's lawfulness is the owner's: a change of load.geared for one row, generic in the form of item 5, with a reading
under Postulate 6 ("no coupling of the time gear with itself"). Only the cut is exact and lawful in form.

## The half-tooth act against the edge

One tooth device, two laws of the dial; not one law in two conventions. Both keep the tooth as its offset from the
dial's middle with the flip -1 - c, but the half-tooth weighs the velocity by W(now) at both ends and the edge by D_in
in and D_out out. probe_mc4 B, a free gear, W rising 10 -> 30: the half-tooth keeps v = 6; the edge keeps 2Dv + s =
228 and v falls 5 -> 2 (W d_t v = F against d_t (W d_t a) = F). Time symmetry (probe_mc4 A, exhaustive): half-tooth 0
failures standing and rising, 196 of 1,176 falling, 490 of 1,274 falling fast; edge 0 on every clock in both
conventions; Form 3 112 of 539 rising, 220 of 490 falling. Injectivity (probe_mc3, W 12 -> 10 -> 8): half-tooth 48
collisions of 312, act as built 24 of 156, edge 0. Conflict 1 settled: CLICK25's "the momentum form is not
time-symmetric ... so the second-difference form is forced" holds for Form 3's one-slot weights and fails for the
edge's two-slot weights; "forced" is wrong. Conflict 2 is item 2. Mathematically only the edge is a bijection on every
clock.

## Sound, with numbers

- The split's algebra, both conventions: bijection and odd law 0 misses of 7,212; the tie-even rule's cost 620 of
  4,812, every one a tie, explained as a theorem.
- The run back: 40 of 40 and rewound on six lays rising and falling, D odd and even, both conventions; 0 failures on
  exhaustive two-gear states on four clocks, including W 13 -> 8 -> 3.
- The 24: 24 of 24 on every lay, 40 rounds, both conventions; with J through the tables and T_d = 5, 24 of 24
  standing, rising and falling (new).
- The books: P_(t+1) - P_t = 4 SUM push 0 misses over 12 rows x 40 rounds; exact per gear by construction.
- The structural reason (probe_mc3): the tooth ranges over one residue system of the modulus that weights its own
  velocity, so every split at any D_out >= 1 is a bijection; the one-dial acts (built, half-tooth, the order's 00 row)
  lose injectivity when W falls (24, 48, 96 collisions).
- The still clock: the edge is the act as built state for state, 40 of 40 at W = 9 and 10 grips.
- The fixed point's conclusion: a dial moved by its own quotient covers the integers neither once nor fully; the
  loader's lay 0 of 12 run back, the cut 12 of 12.
- The pump: a gear at rest with the tooth at the middle answers |k| <= W/2 with no notch, either sign alike.
- All stored outputs of edge, clockclick and click25 rerun identically.

## Solution24

Step 8 let a convention's mutant be refuted with another convention's mirror: a mutant of the tooth's form is judged
with its own flip and mirror, or the refutation says nothing.
