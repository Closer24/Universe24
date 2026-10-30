# The double Node-clock's tooth on the edge

The Boss's deriver, 2026-10-30, 15:3x UTC, revised 16:1x UTC (the gate's mends and the floor's pump), on the piece
placed from above (Big Pic, #2187 6525478254) on the owner's pointer "The double Node-clock's tooth on the edge", by
Solution24. Nothing here is engine code; the probes beside this page wrap the engine's own load and act (t24b, src
untouched) in whole numbers with the engine's carry as the one division: `edge_lib.py` (the harness), `probe_edge.py`
-> `probe_edge.txt` (sections 1 to 8), `probe_record.py` -> `probe_record.txt` (the example world's record),
`probe_pump.py` -> `probe_pump.txt` (the floor's pump, the G2 readers' finding). Run each with
`<t24b>/.venv/bin/python -I`. Every number below is theirs. Status proposed: DRAFTED, for a hostile mathematician and a
hostile physicist; it hangs on one decision, named first.

**The board the probes run on.** The example world's universe as it stands on main (examples/tensor24/universe.json,
read through the loader: the light train, A1 of two parts, and the metric family, the four-vector's square; den,
full_rate and width the file's; nothing declared), on the probe's own piece, a cube of side 3, and the probe's own
settings: 12 rows at 27 sites, 324 gears. The grip at rest, den Gamma^2 = 15,162,856,759,112,389,000,000, is the Mesh
unit and, with J = 0, the pitch every fine tooth moves by (load.geared; David's draw page); the 00 slot's counts and
the drawn fine teeth are laid in grips, the rest teeth are 6 grips, and a count that is not whole in grips is written
"n grips + m". The counts reach 78 to 82 bits of the law's 128. The 00 slot is laid uniform so that W moves by whole
counts a round; the square's ii slots at 0, every grip at its rest. D = W(b) + W(a) is odd exactly where the 00 slot
moves by an odd count (1 grip + 1), even where it stands or moves by whole grips.

## The defect, and the piece in one paragraph

The act as built keeps a gear's fine tooth at the now slot's teeth W(a) and the next round reads it at W(a+): on a
moving clock the tooth is kept in one dial and read in another. From that the SYM24 readers derived the 24's loss from
the second round (24, 3, 3, ...), the one-signed drift of about N dW / 2W a round, the mirror not its own inverse and a
falling clock's broken promise, and the physicist named the equation the board obeys, W d_t v = F, with (d_t W)(d_t a)
dropped (step.py lines 44 to 49). The piece: the velocity a - b lies on the edge between the two slots, so its tooth is
given to that edge, in one dial of both slots' teeth, D = W(b) + W(a), counted from the dial's middle. The round carries
2 (D_in (a - b) + 2 push) + s and splits it at 2 D_out, with D_in = W(b) + W(a) and D_out = W(a) + W(a+); where the
remainder lands exactly on its dial's edge the new count is taken even. The next round reads the tooth on the same edge
it was kept on, so the teeth's change moves no tooth; a sign flip is a negation; the run back reads the same two dials
in the other order. It is d_t (W d_t a) = F with W on the edge, and it completes the law's line 122 with a sixth case.

**The one decision it hangs on (section 6).** The split at 2 D_out needs W(a+), the 00 slot's next count. A dial that
depends on its own quotient has no lawful split (the cells of consecutive quotients overlap for q <= -1 and leave gaps
for q >= 1, exactly (2q + 1) (D(q+1) - D(q)) integers each); so the 00 row's own teeth cannot read the 00 slot. The
lawful way is the one N2's second text already asks for its p-form (M4): the clocks' read acyclic, the 00 row's teeth
at rest, every other row reading the 00 slot. That is a change of term 2's law for one row and of the loader's clock
read, and it is the owner's and Big Pic's word; everything below is measured with that cut.

## Clock

- A gear has two counts, now and before; its velocity is the stride between them, and so is what its carry could not
  make whole. Both belong to the edge between the two slots, not to either slot. The edge's dial has the teeth of both
  slots together, D = W(before) + W(now), and its tooth is read from the dial's middle, so a tooth is a step short or
  a step over, never a place on a dial that one slot owns.
- Every round the gear reads its push at the now slot (the pivot), carries its edge's momentum, 2 D_in (a - b) + s plus
  four times the push, to the next edge, whose dial is D_out = W(now) + W(next), and splits it there: the whole turns
  are the new velocity, the rest stays as the new edge's tooth. The dial it splits at is the dial the next round reads
  it on: one dial per tooth.
- Going backward, the gear sees the same two slots, the same push at the same pivot, the two dials in the other order
  and every edge quantity negated: velocity, momentum and tooth. The tooth 0, the middle, is what the forward and the
  backward Node-clock share, at every dial, odd or even.
- A gear whose momentum is below half a notch stands still and keeps the momentum as its tooth; a push smaller than
  half a notch moves no whole notch, either way; one above half a notch moves one, either way alike (the floor's pump
  below).
- The 00 slot is every row's teeth here. Its own gear cannot read its own next count as its dial; its own teeth stand at
  rest, so the 00 gear is a standing clock and every other gear's D_out is a reading of the 00 slot's next count, which
  the 00 gear's own carry gives in the same round (the engine's lit() and two carries, no if, no loop).

## Algebra

- **The split** (probe 1): for a dial m = 2 D, n + D = q0 m + r0 by Rule3, s0 = r0 - D in [-D, D); where r0 = 0 the
  tooth stands on the edge, and the count is taken even: q = q0 - tie x odd(q0), s = s0 + tie x odd(q0) x m. So
  n = q 2D + s with |s| <= D, |s| = D only at an even q, each integer n one pair and each pair one n (7,212 cases, 0
  misses), and split(-n) = (-q, -s) (0 misses). The tie taken upward misses the negation at exactly the ties (934 of
  934); the plain carry at 6,276 of 7,212.
- **The round.** D_in = W(b) + W(a); N = 2 (D_in (a - b) + 2 push) + s; q_00 from the split at 2 D_in (exact for the 00
  row, whose D_out is its D_in); D_out = W(a) + W(a + q_00) through the clocks' read; (q, s+) = split(N, 2 D_out);
  a+ = a + q, b+ = a. Divided by four: W_in v + push + s / 4 = W_out v+ + s+ / 4 with W_in = D_in / 2 and
  W_out = D_out / 2 the mean teeth of the two edges, |s / 4| <= W / 2: the leapfrog of d_t (W d_t a) = F with W on the
  half-steps, the remainder kept within half a tooth of the momentum's own dial.
- **The mirror:** (a, b, s, r_d) -> (b, a, -s, T_d - 1 - r_d), read in no teeth; twice the identity by inspection.
  **The run back:** from (a+, a, s+) the mirrored state (a, a+, -s+) reads D_in' = W(a+) + W(a) = D_out, the same push
  at the pivot a, N' = 2 D_out (-q) + 4 push - s+ = -(2 D_in v + s); its 00 row's provisional count is -v_00, so
  D_out' = W(a) + W(b) = D_in, and the split at 2 D_in of 2 D_in (-v) + (-s) is (-v, -s), the negation of a valid pair
  being valid; the state (b, a, -s) mirrored is (a, b, s). Exact at every D_in, D_out >= 1 (W >= 1 at both slots is
  more than enough), rising or falling, with no promise beyond the tooth within its own dial.
- **The 24** (the hypotheses of the SYM24 one-round identity: equal sides, rests alike within an orbit of rows, the 00
  slot read at the own site, J either 0 or laid through the tables; and the acyclic cut alike at every Node-clock):
  every turn fixes the 00 slot at both slots, so D_in and D_out at the image are the site's; the push turns by P; so
  N turns by P, and on a flipped row N -> -N gives (q, s+) -> (-q, -s+) by the split's negation law. The turned state
  is P a, P b, P s with the sites moved and no dial read, so it is the same in every round: tick(T s) = T(tick s)
  wherever the tooth lives, moving or standing. The plain carry at the edge's dial has the sign law
  carry(-n, m, m - 1 - r) = (-q, m - 1 - r') at its own dial m = 2 D_out, which is not the dial 2 D_in the tooth
  lives on where the clock moves: the centring is load-bearing, not a convention (probe 2, and the run back in 3).
- **The still clock:** at D = 2 W, s = 4 r + 2 - D maps the act as built's tooth to the centre of its cell;
  N = 4 (W v + push + r) + 2 - D = 2 D q + (4 r' + 2 - D) with |4 r' + 2 - D| <= D - 2: the same q, the corresponding
  tooth, never a tie; and -s = 4 (W - 1 - r) + 2 - D is (iii)'s flip. State for state (probe 5).
- **The momentum:** per gear (2 D_out v+ + s+) - (2 D_in v + s) = 4 push exactly; summed over a row on the torus, where
  the Meshes' pull sums to 0, P = SUM (2 D_in v + s) is kept to the bit under any motion of W (probe 4).
- **The fixed point:** cells [2 D(q) q - D(q), 2 D(q) q + D(q)] tile the integers iff D(q + 1) = D(q); the next cell's
  floor less this cell's ceiling is (2q + 1) (D(q+1) - D(q)) (0 misses), so a dial moved by its own quotient leaves
  gaps (q >= 1) and overlaps (q <= -1): no bijection, for any W_a (probe 6).
- **The even-count rule's cost:** split(n + 2 D k) = (q + k, s) for every even k and every n, and for an odd k at every
  n but the ties, where q + k is odd and the tie goes the other way (620 misses of 4,812, every one a tie). The act as
  built has q - v = (push + r) div W, covariant under v -> v + k for every k (probe 7).
- **The click's books:** the same split on an area A at a key with the tooth born at 0 gives q(A) + q(-A) = 0 at every
  key, odd or even (4,960 cases, 0 misses; the plain carry born at (key - 1) div 2: 0 at odd keys, 120 at even ones,
  term 11's measure 4); a giver and a taker born at 0 keep opposite clicks and opposite teeth in 6,000 of 6,000 rounds
  at the keys 12 and 13 (probe 8).
- **The floor and the middle** (probe_pump A, B): at rest with the tooth 0, the act as built answers a push k with
  k div W: a backward notch for every k in [-W, -1] and a forward one at W alone; born at W div 2 (the law's (i)) it
  answers (k + W div 2) div W: -1 for k <= -W/2 - 1 and +1 for k >= W/2, the tie at -W/2 going down and at +W/2 going
  up. The edge answers split(4 k, 4 W): 0 for |k| <= W/2 (the tie taken even), -1 and +1 alike beyond. A free gear
  carrying a sub-notch momentum m: the act as built and the p-form move floor(m / W) a round, -1 for every m in
  [-W, -1], 0 for m in [0, W - 1] (a whole notch a round from a momentum of -1); the edge moves 0 for |m| <= W/2 and
  +-1 alike beyond, the momentum kept as the tooth.

## Board

- **What stands and moves.** At every Node-clock the state is (a, b, s, r_d) per gear, s the tooth of the edge (b, a)
  in half-teeth of its dial D = W(b) + W(a). The readings, the pull and the clocks' read are at the now slot, as built.
  The 00 row's teeth read no row (W_00 = rest); every other row's read the 00 slot at both slots and at the next
  count through the 00 row's own carry; the grips as built. The drive as built (T_d standing, its tooth flipped in
  T_d by the mirror; on main T_d = 1 and r_d = 0).
- **The promise** the runner reads from outside: W >= 1 at both slots and |s| <= D_in, the edge |s| = D_in only at an
  even velocity. The tooth is kept on the edge the next round reads, so no motion of the clock, rising or falling, can
  break it: on the lay falling from W = 46 to 6 grips the edge's promise held at all 40 rounds where the act as
  built's broke before round 2.
- **The width:** the carried N is about 4 W v, two bits over the act as built's W v: 78 to 82 bits on the probe's
  board, 78 against 77 on the example world's own run (the law's 128).
- **The ties** fall at about one gear in 2 D / grip a round on the lays whose teeth and clocks are whole in grips
  (6, 5, 7, ... of 324 standing); from the act as built's own states on a still even dial they never fall (0 in 40
  rounds), the quarter-tooth lattice 4 r + 2 - D being kept; where the clock moves by a count that is not whole in
  grips they are rarer than one in 10^22 and none fell.

## Physics behind the clicks

- The board obeys d_t (W d_t a) = F with W the mean of the two slots' teeth on each half-step: the momentum W v is what
  the clock keeps, not the velocity. On a rising clock the row sums S of a - b fall as 1 / D (from -172 to -33, from 240
  to 45, from 325 to 62 as D goes 19 to 99 grips) and on a falling one they rise (from -172 to -1,230 as D goes 93 to
  13 grips), with P = SUM (2 D v + s) kept to the bit in every row: the velocities redshift with the clock and no row
  drifts. The act as built, on the same lays, keeps W S + R only across a standing W (P_(t+1) - P_t = dW x S_(t+1), 0
  misses; P_40 - P_0 up to -12,941 grips) and drifts one-signed (S_40 - S_0 from -23 to -28 rising, +11 to +17
  falling).
- **The floor's pump, removed at its root** (the G2 readers' blocking item on term 13 and N2: "a gear's rest is p of
  about W/2, because the tooth is uncentred, counted from 0; a+ = a + floor(p / W) answers any small negative push with
  a whole notch"; probe_pump, on the physicist's own one-site replica, REST 3000, G 210, T_d 1000). On the edge a
  slow hand at rest stays at rest, and a push below half a notch moves no whole notch, either sign alike (Algebra). The
  hand on its spring with no 00 push (C, 12,000 rounds): laid with a momentum of -1, -300, -1,499 or -1,500 (below
  half a notch of 3,000) the p-form's hand swings on the floor, its strides' squares summing to 18 to 105 million with
  500 permille of that from a -1 stride at -W < p < 0, its mean p 1,440 to 1,589, about W/2; the edge's hand does not
  move at all: strides 0, source 0, its momentum kept as its tooth. Laid with one notch (-3,000) the p-form's floor
  source is 644 permille of the exact 2 p^2 / W (399 permille of it from the sub-notch -1), the edge's 1,441 permille
  (437 permille of it from strides of one notch out of a momentum below one), both without drift; laid with ten
  notches both are the exact source within 7 permille. The readers' check F replicated (D): with the strides squared
  as the source, the p-form winds W from 3,000 to 19,010 from a hand laid with p = -1 (2E0 = 0) and to 31,877 from
  p = -300, 654 to 657 permille of the push from the sub-notch -1 strides (their numbers, reproduced); the edge keeps
  W at 3,000 through 12,000 rounds in both, with no push at all. From one notch up both wind W without bound (edge
  50,911 against 87,299 at p = -3,000; 1,475,288 against 1,119,051 at 30,000), in the edge form ordered by the energy
  laid and with no share from below half a notch; that growth is term 5's and 13's zero mode, not the tooth's. So the
  pump the readers found is the uncentred tooth's and the edge removes it; what the edge does not remove is the whole
  notch itself: between half a notch and one notch of momentum the strides' squares over-count the energy (1,441
  permille), symmetric in sign.
- The 00 gear is a standing clock at its rest: the clock's rate is a count every other gear reads, not a gear that reads
  itself; where the metric's push (term 5) moves it, it moves by its own carry at rest teeth. This is N2's M4 read
  again from the edge: a gear reading its own count has no inverse in the p-form and no dial on the edge.
- A falling clock runs back: a metric wave's falling edges no longer block the rewind (the SYM24 physicist's item 4).
- The owner's word, the Node-clock forward and backward: the two dials read in the two orders are one bijection and its
  inverse. What they give the click: the quotient of every carry negates exactly between the two readings at every
  dial, so a give and a take, a click and its undoing, are opposite at every key, odd or even, once the click tooth
  takes the edge's rule, born at the middle and mirrored by negation (probe 8). That retires term 11's "the key odd"
  item and the declaration it needed at an even key (the giver's and the taker's births apart). The birth and the
  mirror's fixed point are one, 0, at every dial; the physicist's "its half-tooth is the 24's (W - 1)/2" is this
  middle, which on the edge is 0 at every D with no parity. Nothing more comes from the two dials: no key, no size of
  a quantum, no selection; on a moving clock the momentum is re-split and the velocity's whole count is not kept, only
  the momentum's; the key stays G3's.
- Term 12's draw, re-read: David's pointer V, the A1 rows' fine teeth at the Node-clock and its six neighbours folded
  at the Node-clock's own teeth, becomes the A1 rows' edge teeth s (each in its own edge's half-teeth) folded by the
  same split at the drawing Node-clock's own dial 2 D, its tooth d in [-D, D]; the A1 rows' teeth are unchanged under
  the 24 and the 48's g lift, so the turned board draws alike. Under time's reversal s -> -s and d -> -d, so a draw
  read the same both ways reads |d|: the law's (v), min(r, w - 1 - r) over (w + 1) div 2 classes with a case for an
  even w, becomes |d| over D + 1 classes at every D with no case. The pitch lemma stands with the pitch and the dial
  both in half-teeth; on a moving clock the quarter-tooth lattice is lost and the pointer is finer, not coarser. Not
  probed here; David's probe is his to re-run on the new tooth.
- The record, re-read: the record writes no tooth; the end's digest is of (a, b, tooth, r_d). On the example world (a
  still clock, the metric at 0) the runner's record gives exact 1 and the digest cb361775...; the act as built stepped
  here gives the same digest; the edge act gives a and b equal to it at every one of the 1,280 count lines, exact 1,
  and the digest cf711d50... from the built lay's tooth read on the edge (s = 4 r + 2 - D) or 59148d53... from the
  edge's own birth (s = 0). So the ledger is byte for byte the same and the digest is not: schema 1.3 should name the
  tooth's form beside the digest, and the runner's promise reads the edge's.

## Measured (probe_edge.txt, probe_record.txt, probe_pump.txt), each with its "no"

1. **The 24 on any moving clock, no parity condition** (2). Seven lays, 324 gears, 40 rounds: standing at W = 9 grips
   (D = 18 grips); rising by 1 grip, by 1 grip + 1 (D odd) and by 2 grips from W = 10 grips (D 19 to 99, 18 to 178);
   falling by 1 grip and by 1 grip + 1 (D odd) from W = 46 grips (D 93 to 13) and by 3 grips from W = 126 grips (D 255
   to 15): the edge act 24 of 24 at every one of the 40 rounds on every lay, D odd and even. The act as built: 24
   standing; 24, 3, 3, ... rising by 1 grip; falling, the promise breaks before round 2. Mutants: the tooth moved and
   not negated, 3 of 24 at every round; the plain carry at the edge's dial with the negation, 3; the same with the flip
   2D - 1 - s in the tooth's dial, 24 standing and 3 at every round moving; the tie taken upward, 3 at every round
   standing and rising (ties at 6, 5, 7, ... and 9, 3, 5, ... gears a round) and 24 for five rounds then 12, 12, 12, 6,
   3, ... falling (its first ties at rounds 3 and 5).
2. **The mirror its own inverse; the run back rising and falling** (3). mirror(mirror s) = s at 41 of 41 states on
   every lay; untick(tick s) = s in 40 of 40 rounds rising by 1 grip and by 1 grip + 1, falling by 1 grip, by 1 grip + 1
   and by 3 grips, standing; the 40 rounds rewound to the start bit for bit on every lay. The act as built, no promise
   asked: 40 of 40 rising, 1 of 40 falling (its promise broken from round 1); its mirror twice moves the tooth at all
   13,284 gear-states on every moving lay and at 0 standing. Mutants: the mirror with the tooth kept, 0 of 40; the
   plain carry on the edge with its flip, 0 of 40 moving and 40 of 40 standing.
3. **The momentum kept exactly where the pushes sum to zero** (4). P_(t+1) - P_t = 4 SUM push: 0 misses over 12 rows x
   40 rounds on the rising, falling and standing lays; SUM push = 0 (grips alike at both ends, J = 0): 0 misses;
   P_40 - P_0 = 0 in every row; the row sums S re-split with the dial (above); the 00 row's own S, 27 grips, stands.
   The act as built: P = W S + R moves by dW x S_(t+1) (0 misses), by -7,583 to -12,941 grips and 1,080 grips^2 on the
   00 row over 40 rounds. Mutant: a spring on the light train's first row (push -2 a, not summing to 0): the books
   still close, P moves by exactly 4 x the pushes' sum (0 misses, 12 row-rounds not 0), run back 12 of 12.
4. **The still clock, state for state** (5). At W = 9 and W = 10 grips, 40 rounds: a and b equal and s = 4 r + 2 - D at
   40 of 40 rounds, 0 ties; (iii)'s flip maps to the negation at 41 of 41 states; the 00 row's cut changes no a or b
   of the act as built here (41 of 41). Mutant: the tooth laid at the cell's lower edge, s = 4 r - D, departs at 14 and
   11 gears of 324 after one round.
5. **How the split learns W(a+)** (6). The formula for the gap or overlap, 0 misses; a self-read dial (D(q) = 2 W_a + q)
   leaves 1,560 integers of the hull under no q and 2 to 194 under two or more, for W_a from 1 to 13; a dial the
   quotient does not move leaves 0 and 70 shared edges, which the even rule gives to one q. On the act, the loader's
   lay (the 00 row reading itself) under the edge's two carries: untick(tick s) = s in 0 of 12 rounds rising and 0 of
   12 falling, and the 00 slot's own count leaves the grips (4 grips, 5 grips - 95 permille, 6 grips - 262 permille,
   7 grips - 486 permille, ...: its own dial re-splits its own velocity); the acyclic cut: 12 of 12, the slot 4 to 16
   grips by whole grips.
   What is missing is thus named: a teeth law for the 00 row that does not read the 00 row.
6. **The even-count rule's cost** (7). Adding a whole count k to every velocity of a row on a still clock: k even, 0
   misses of 4,812; k odd, 620 misses, every one a tie and none else; on the board with the light row's 27 carries laid
   on the dial's edge, k = 1 and 3 depart at 27 of 27, k = 2 at 0; the act as built departs at 0 for every k. No law
   asks a boost of a count's velocity (the law's symmetries are the cube's 24, time's reversal and locality).
7. **Term 12's draw and the record's digest, re-read** (probe_record.txt and Physics above): the digest changes, the
   1,280 count lines do not, exact stays 1, 78 bits; the draw's fold becomes the split at the own dial, its even read
   |d|, D + 1 classes at every D.
8. **The owner's word** (8): the click's books on the centred split, 0 misses at every key 1 to 40, 0 of 6,000 rounds at
   the keys 12 and 13; the plain carry's birth, 120 misses at even keys.
9. **The floor's pump** (probe_pump A to D, above): removed below half a notch (W constant at 3,000 through 12,000
   rounds for p = -1 and -300, against 19,010 and 31,877), symmetric above it, the over-count of one notch named.

## The law's line 122, case (vi): old -> new

- Old (line 122): "every division of the Node-clock is the carry u = q w + r with the remainder r in [0, w), and the
  remainder obeys one rule in five cases. (i) It is born at the half teeth count ... r = w div 2. (ii) It is kept where
  what is divided is a notch of the state and dropped where it is a coefficient ... (iii) It is mirrored, r -> w - 1 -
  r, once per reversal of the gear it belongs to, two mirrors the identity ... (iv) ... the odd rounding ... (v) The
  digit is read even under the mirror, min(r, w - 1 - r) over (w + 1) div 2 classes, w div 2 at an even w."
- New, proposed (vi): "A kept remainder belongs to the edge of the division that kept it, between the gear's two slots,
  in one dial of both slots' teeth, D = W(before) + W(now), counted from the dial's middle in half-teeth, s in
  [-D, D]: the round carries 2 (D_in (a - b) + 2 push) + s and splits it at 2 D_out, n = q 2D + s with |s| <= D, and
  where s lands on the dial's edge the count q is taken even; the next round reads the tooth on the edge it was kept
  on, so a change of the teeth moves no tooth. On the edge (i) is the middle, s = 0, at every D with no parity; (iii)
  is the negation, s -> -s, read in no teeth; (v) is |s|, D + 1 classes at every D. On a still clock it is (iii)'s
  w - 1 - r state for state, by s = 4 r + 2 - 2 w. A dial is never moved by its own quotient: a gear whose teeth would
  read its own count has no edge dial, so the 00 row's teeth read no row. A momentum below half a notch is a tooth and
  moves no notch; one above it moves one, either sign alike."
- The touch on line 100: the sentence "the carry's rounding at the mid tooth ... ties at every p = w / 2 mod w at an
  even w and never at an odd one, where it is odd under p to -p" gains its even case: with the tie taken even the
  rounding is odd under p -> -p at every w.

## What stays OPEN

- The 00 row's own teeth at rest (the acyclic cut): term 2's law for one row and the loader's clock read; the owner's
  and Big Pic's word. It is also N2's M4; the two texts ask one change.
- The drive's tooth and the click tooth under the same rule (Solution24, step 10: one split for every carry of the
  Node-clock): the drive not measured (J = 0, T_d = 1 on main); the click's books measured in the algebra alone (G5).
- Whether a rule with a named edge case ("where the remainder lands on the edge") is a case the owner allows in the
  law's words; in the act it is two carries and lit(), no if.
- The energy with a moving W: not checked here.
- Term 5's push on the edge form: N2's theorem (its strides sigma_b, sigma_a and its mirror R_P) is written for the
  p-form and must be derived again with the edge's mirror, the negation; the stride out of a round is known only after
  the 00 slot's next count, so a source reading it reads it at the in-dial (probe_pump's replica) or not at all, and
  which, if either, keeps the run back exact is not derived here. The strides' squares as a source over-count a
  momentum between half a notch and one notch (1,441 permille) in the edge form, symmetric in sign; and the zero
  mode's growth without bound from a hand of one notch or more is term 5's and 13's question, not the tooth's.
- Term 12's draw on the new tooth: re-read here, not probed; David's probe to re-run.
- The record's schema 1.3: the tooth's form named beside the digest; the runner's promise is the edge's.
- The hypotheses of the 24 as SYM24 states them (equal sides, rests alike within an orbit, J through the tables).
- The relation to N2's p-form: two spellings of one momentum (p = W v + r at the now slot; 2 D v + s on the edge);
  which the law writes is Big Pic's.

## Ready for a hostile pair?

Yes, with the one decision named at the head. Points 1 to 6 and 9 are measured on the real act or on the readers'
own replica with their "no" mutants; the fixed point is derived as an impossibility with its formula and the lawful
way measured; point 7 is a re-reading with the record measured and the draw stated, not probed. The mathematician
will want the one-round identity's hypotheses restated for the cut, the physicist the energy and term 5 on the edge.

## The gate

Sofer's scan refused the first probes on six lines: five trains declared in the harness's code with a pinion, and a
path built with pathlib's "/". Mended: the harness reads the example universe's trains and integers through the
loader and declares nothing; every path is built with joinpath; every floor division and remainder in the probes goes
through Rule3's carry (the note DIVIDE). The scan's rules PROBE, DIVIDE and DECLARE find nothing in the four files
(self-checked with the gate's own scan; the Boss re-runs it). Every number on this page is the rerun's.

## Solution24, addressed

1. It does not follow by itself: the act as built keeps and reads one tooth in two dials; the mend adds no number and
no rule for a phenomenon, it names where the remainder belongs. 2. The picture: a slot's quantities (a count, the
teeth, the pull) are the reversal's pivots; an edge's (a velocity, a momentum, a kept remainder) are negated by it.
3. From the big things: Rule3's carry twice and lit(), the 24, time's reversal; the one CHOSEN point is the tie taken
even, with its measured cost. 4. Four layers above. 5. The click: the carry's quotient at the edge's rule negates
exactly between the two readings, every key. 6. The books: P = SUM (2 D v + s) to the bit under a moving W, the run
back to the bit rising and falling, the 24 to the bit. 7. Both ways: W v kept and the velocities redshifting with the
clock is nature's; a hand below half a notch at rest is nature's rest; what does not follow is the 00 row's own teeth,
named. 8. Run locally, on the real act, wrapped, and on the readers' replica. 9. For the pair. 10. Unify: one split
for every carry of the Node-clock, the gear's, the drive's and the click's, is proposed. 11. Into the document when
the pair passes it. 12. Which gear: every gear's tooth; the 00 gear's own teeth; what the clicks show: W v kept, a give
and a take opposite at every key, no notch below half a notch. 13. Toward the Node-clock working well under a moving
clock, the step term 5 waits on.

**One line to add to Solution24, step 2:** a count, the teeth and the pull belong to a slot and are the reversal's
pivots; a velocity, a momentum and a kept remainder belong to an edge and are negated by it; every remainder is kept
and read on one edge, in one dial.
