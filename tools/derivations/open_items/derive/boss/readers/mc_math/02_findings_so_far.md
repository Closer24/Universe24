# Findings so far (after probes mc1 to mc6), 2026-10-30

All stored outputs rerun byte-identical: edge/probe_edge.txt, probe_pump.txt, probe_record.txt; click25/probe_clock,
probe_drift, probe_48 (warnings aside). EDGE.md's numbers now match probe_edge.txt (the revision of 16:1x fixed the
earlier mismatches I had listed from the 486-gear board).

## F1 (BLOCKING for the law wording): the tie rule is not load-bearing; one carry does it
probe_mc1_half.txt. The half-open convention s in [-D, D-1] (edge_lib.split_up, i.e. the text's own mutant "the tie
taken upward") with the mirror s -> -1 - s (the law's (iii) r -> m - 1 - r on the dial m = 2D):
- algebra: bijection 0 misses (7212), split(-n - 1) = (-q, -1 - s) 0 misses, shift covariance 0 misses for k = 1, 2, 3, -1, -5;
- the edge agent's board, 6 lays, 40 rounds: the 24 24 of 24 at every round (standing, rising 1, rising 1+1 (D odd),
  falling 1, falling 1+1, falling 3); mirror twice = s 41/41; untick(tick s) = s 40/40; rewound True; P books 0 misses;
- shift covariance on the board: 0 departures for k = 1, 2, 3 even with every carry on the centre-0 split's tie (the
  centre-0 act departs at 27 of 27 for k = 1, 3);
- still clock: a, b equal to the act as built 40/40 at W = 9 and 10 grips with s = 4 r - D; the cell (s + D) div 4 is
  the built tooth at every gear; the mirror -1 - s lands in the built mirror's cell W - 1 - r: 0 misses of 41 x 324.
The text's mutant "the tie taken upward: 3 of 24" fails only because it was paired with the negation s -> -s; the
mismatched pairs (half-open act + negation, centre-0 act + flip -1 - s) each give 3 of 24 on the lays with ties and
24 on the tie-free (D odd) lays. So "the centring is load-bearing" is right only as "the tooth is re-centred from D_in
to D_out"; the integer centre 0 with a tie rule, two carries and lit() is not needed, and neither is (vi)'s edge case,
nor the OPEN item about a named edge case, nor the "even-count rule's cost".

## F2 (MINOR): the stated promise is on the wrong state
probe_mc2 A. "W >= 1 at both slots and |s| <= D_in" holds on states whose round splits at D_out = -4 grips (W(a) = 3,
W(b) = 13, v_00 = -10 grips). The act stays a bijection even there (Python's carry at a negative dial is still a
bijection; untick(tick s) = s: True), but a negative dial is not teeth. Also D_out = 2 grips with W(a+) = -1 grip is
exact: "W >= 1 at both slots" is neither necessary nor sufficient for the round; the condition is D_in, D_out >= 1,
which the Algebra sentence names and the Board's promise does not. Fix: the promise reads D_out through the 00 row's
standing split.

## F3 (MINOR): section 6's gap formula is off by one and its picture is wrong for q <= -1
probe_mc2 B. The text's formula summed gives 1600; the probe's own count is 1560 = sum (g - 1). For q <= -1 the cells
are out of order (W_a = 5: 4 of 49 pairs). The conclusion (no bijection) stands.

## F4 (SOUND, strengthened): the structural reason the edge is a bijection and the one-dial acts are not
probe_mc3. Falling clock W(b) 12 -> W(a) 10 -> W(a+) 8, a = 0, b in [-6, 6], no push: collisions: the act as built 24
of 156 states, the half-tooth act 48 of 312, the order's 00 row 96 of 625, the edge 0 of 573/572 (both conventions).
Standing and rising: 0 everywhere. The tooth must range over one residue system of the modulus that weights its own
velocity; the edge's does (2 D_in); a tooth kept at 2 W(b) and read at 2 W(a) does not when W falls.

## F5 (settles conflict 1): the momentum form IS time-symmetric when both ends weigh it
probe_mc4 A. Two-gear Node-clock, exhaustive: Form 3 (W(b) v + push re-split at W(a)) fails untick(tick s) = s at 112
of 539 rising, 220 of 490 falling; the half-tooth act 0 standing and rising, 196 of 1176 falling, 490 of 1274 falling
fast; the edge 0 of ~2000 on every clock, both conventions. CLICK25's "the momentum form ... is not time-symmetric ...
so the second-difference form is forced" is true of Form 3 and false in general; "forced" is wrong.

## F6 (settles "one law?"): one tooth device, two dial laws
probe_mc4 B. Free gear, W rising 10 -> 30: the half-tooth keeps v = 6; the edge keeps 2 D v + s = 228 (v 5 -> 2).
Different equations of motion (W d_t v = F against d_t (W d_t a) = F). Not one law in two conventions.

## F7 (settles conflict 2): the key's parity is a trade, and the odd key is where no trade is needed
probe_mc5. Keys 1-40: floor born (key-1) div 2 and CLICK25's half-tooth born u = key: books miss 120 at even keys,
one key = one click exact; the centre-0 tie-even: books 0 misses, one key = one click misses 120 (at ties a whole key
is 0 or 2 clicks: [2, 0, 2, 0, ...] from a tooth on the edge); half-open: as the floor. No odd tie rule is shift
covariant (theorem). At an ODD key the centre-0 split has no ties (2A + key is odd), so it coincides with the floor
and has both. The edge's "retires the odd-key item" is overstated: the tie-even rule buys the books at an even key
with the count's covariance; the odd key needs no rule at all.

## F8 (MINOR): the pump is the birth's, and the exact-source claim is run-length-limited
probe_mc6. The p-form hand born at the law's (i) (p = W div 2 + m0) stands as the edge's for |m0| <= 1500, floor
source 0: the pump is the birth at 0. What only the edge has: 0 energy at rest for the exact source (the (i)-born
p-form carries 2 p^2 / W = W/2 a round at rest). The edge's exact-source run at p0 = -300: W = 3000 through 12,000
rounds, then the 00 gear's momentum crosses half a notch (~12,500) and W = 6492 at 16,000, 10,492 at 20,000.

## F9 (MINOR): probe_record's world is one gear
examples/tensor24/setting.json lays one light gear with v = 1; pushes are -W or W/6: floor and nearest agree.

## F10 (SOUND, new): the 24 and the run back hold on the edge with J laid through the tables
probe_mc7 A. Plan 1 (s = 3, T_k = 2, T_d = 5), 486 gears, J not 0 at 326, 4 rounds, standing, rising AND falling:
both conventions 24 of 24 at every round, untick(tick s) = s 4 of 4, rewound True (90 to 103 bits), with the drive's
tooth flipped in T_d on a flipped row. The edge probe's own turned_edge moves r_d unflipped: 3 of 24 at T_d = 5
(harmless at T_d = 1). The act as built: [24, 24, 24, 24] standing, [24, 3, 3, 3] rising, breaks falling.

## F11 (MINOR): "acyclic" is the self-read cut; two squares break it
probe_mc7 B. Two squares, both 00 slots moving: the cut leaves 2 cross reads, promise broke at 1, run back 0 of 1;
with every read onto a 00 row cut: 12 of 12, rewound. One moving and one standing: 12 of 12 either way.

## Reruns: probe_cc.txt identical to stored (warnings aside).
