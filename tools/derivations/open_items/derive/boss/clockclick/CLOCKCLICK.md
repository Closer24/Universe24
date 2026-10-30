# The clock click: the owner's idea on the Node-clock's act, in whole numbers (2026-10-30, the Boss's deriver)

The defect (SYM24 v2, READER_PHYS 1): the fine tooth r is kept at round t in the teeth W_t = W(a_t) and read at round
t + 1 in W_(t+1); where the 00 slot moves, the tooth's meaning (r / W of a notch) changes between the rounds. Four faces:
the forward drift SUM r_t (1/W_t - 1/W_(t-1)), one-signed; the uniform vector along (1, 1, 1); the 24 departing by
whole notches from round 2; the mirror not its own inverse (mirror twice moves r by W(a) - W(b)).

The owner's words: "The moving clock: there is a click there. Maybe that is exactly the matter of the click. In the 00
slot there is usually a click too, no?" And: "In the clicks, think clocks, do not think quantum: clocks, hands, chains.
The whole system as clicks: clocks connect and come apart, and the aim of the system is that clocks connect."

Probes beside this page: `cc_lib.py` (the forms, each a wrapper on step.tick or on the engine's carry and sources; no
src file edited), `probe_cc.py` (its output `probe_cc.txt`). Run with `<t24b>/.venv/bin/python -I probe_cc.py`. The
edge act is imported read-only from `scratchpad/edge/edge_lib.py` (another agent's derivation). Whole numbers only; the
engine's carry (and the edge's split, two carries and lit()) the only divisions.

## Clock

- The Node-clock is double: it holds now (a) and before (b), so it holds two teeth counts, W(a) and W(b), per gear. The
  tooth r stands between them: it was kept by the round that made the velocity a - b, at W(b), and it is read by the
  round that makes the next velocity, at W(a).
- The 00 slot's gear is the clock's hand: its count sets every gear's teeth at the Node-clock, its own included (the
  loader's lay: every row reads the 00 slot, load.geared). Its notch each round (q_00 = a+_00 - a_00) is the click the
  owner points at: the hand moving the teeth of every gear it is chained to.
- A "clock click" in the owner's reading: at the moment the hand moves the teeth (W(b) to W(a)), the tooth is carried
  from the old teeth into the new by Rule3's carry; what does not fit leaves as a whole count, the remainder stays, and
  the tooth is then never read in teeth other than its own.

## Algebra: the forms

Per gear the act as built: n = W(a) (a - b) + push; q, r+ = carry(n, W(a), r); a+ = a + q; b+ = a. The momentum in
the round's teeth is U = W v + r: at standing W, U+ = U + push exactly (the books W_t (S_(t+1) - S_t) = R_t - R_(t+1)).

**Form 1, the literal click (the tooth as a count re-carried into the new teeth).** q_c, r' = carry(r, W(a), 0); q_c
into the gear's step, r' stays. Rising or standing (W(a) >= W(b) > r): q_c = 0, r' = r, nothing happens. Falling: a
tooth at or above the new teeth sheds whole notches. Identity: carry(n, W, r) = carry(n, W, r') + (q_c, 0) because
n + r = n + q_c W + r'. So Form 1 is the act as built with the promise (r within [0, W(a)), read from outside by the
runner) dropped. It mends nothing of the four faces: the drift, the 24 and the mirror are the act's. Its one gain is
the falling clock: the act runs on; but the run back by the same act fails wherever q_c is not 0 (the mirror flips r+ in
W(a) and cannot see q_c), so each such click needs a line (gear, round, q_c) for the rewind.

**Form 2, the scaled click (the tooth's fraction carried).** r' , e = carry(r W(a), W(b), 0): r / W(b) = r' / W(a) +
e / (W(a) W(b)). The new tooth r' in [0, W(a)); e in [0, W(b)) is what does not fit, a sub-tooth, no whole count. Not
a bijection on the tooth ([0, W(b)) and [0, W(a)) differ in size): e must be booked in a line at every gear at every
moving click, rising too, or the rewind cannot run. And the 24 still fail: the flip r -> W - 1 - r is the reflection
about the centre (W - 1) / 2 of the dial, which moves with W; f(W(b) - 1 - r) = W(a) - 1 - f(r) fails by about
W(a) / W(b) at most r (W(b) = 10, W(a) = 11: f(9 - r) = 9 - r against 10 - r at every r). Its drift: the floor loses
on average half a new tooth per gear per click, N / (2 W) a round, the same order as the act's N dW / (2 W) at dW = 1.

**Form 3, the momentum carried (U = W(b) v + r re-split at W(a)).** q, r+ = carry(W(b) (a - b) + push, W(a), r):
the quotient of U at the new teeth, into the step; U+ = U + push exactly, whatever W does; no promise needed (the carry
takes any r). This restores the term (d_t W)(d_t a) that step.py's comment names as dropped: W(a) v+ - W(b) v = push.
Two breaks, both exact: (i) the 24 and the mirror: the tooth's flip must be read in the divisor's teeth W(a) at the
input and in W(a+) at the output of the same round, so it fails from round 2 as the act does; (ii) the run back is not
the same act on the mirrored state: the time reverse of W(a) v+ - W(b) v = push weighs the velocities on the other
ends (W(a+) and W(a)), and at the 00 row, whose teeth read its own count, the map b -> (rest + b)(a - b) is not
monotone, so the act is not even injective: rest 6, a = 10, the sum 15 comes from (b, r) = (-5, 0), (9, 0) and
(10, 15); 27 such collisions on b in [-5, 15]. Form 3 crosses Postulate 2 (every act a bijection).

**Form 4, the centred click (withdrawn: it leans on the teeth's parity, law line 100).** With W odd and the tooth kept
centred, c = r - (W - 1) / 2, the flip is c -> -c and the carry of c into any new teeth commutes with it (0 misses over
W, W_old odd in [1, 40], c, n in a span); the one carry q, r+ = carry(W(a) v + push, W(a), c + (W(a) - 1) / 2) does the
click and the round at once: on a rising clock nothing leaves, on a falling clock c outside the new dial sheds q_c =
(c + (W(a) - 1) / 2) div W(a) whole notches into the step, and the rewind needs that q_c in a line (the mirror negates c
and cannot see it). It is candidate.py's act with the promise dropped. Measured below for the comparison asked, and set
aside: W = 6 den Gamma^2 + the 00 slot is even at rest, and an odd W needs a number in the act (a doubled 00 slot, an
odd rest).

**The edge (another agent's derivation, scratchpad/edge, measured here beside the forms).** The velocity's tooth sits on
the edge between the two slots in one dial D = W(b) + W(a), counted from its middle: the round splits N = 2 (D_in (a -
b) + 2 push) + s at 2 D_out, D_in = W(b) + W(a), D_out = W(a) + W(a+), a remainder on the dial's edge taking the count
even (edge_lib.split: two carries and lit()). The tooth written at the edge (a, a+) is read by the next round on the same
edge, so it is never read in a foreign dial, with no promise and no line: the flip is the negation, the mirror (b, a, -s)
is its own inverse, and the run back is the same act. The momentum in half-teeth P = SUM (2 D_in v + s) moves by exactly
4 SUM push. What the growing dial takes from the velocity's whole count is the redshift, in whole counts, and the books
hold it: 2 D_out S+ + T+ = 2 D_in S + T + 4 SUM push. It needs W(a+), the 00 slot's next count: the edge agent cuts the
00 row's self-read (its teeth stand at rest), since a dial that depends on its own quotient covers the integers neither
once nor fully (its section 6).

**The order of the round (Big Pic's word, tested here): the 00 slot's click first.** The 00 row's notch is the one
count no edge dial can wait for. Read it first, at its own teeth: the 00 row splits on its own now dial, both ends W(a),
N_00 = 2 (2 W(a) v + 2 push) + s split at 4 W(a) (or, the other reading, by the act as built at W(a)); every other gear
then carries its velocity, count and tooth from the old edge into the new at that click, D_out = W(a) + W(a+_00). The
00 row's own tooth is then kept on 4 W(a) and read on 4 W(a+): the hand's own gear reads its tooth in the dial it was
kept in only where the 00 slot stands or rises (the tooth fits); where it falls past the tooth, a whole count leaves
(the 00 slot's own click) and the rewind needs its line. Every other gear is exact on every clock.

## Where each quotient goes, and what the mirror does

- Form 1 and Form 4: into the gear's step by the one carry, and into a line for the rewind; the mirror negates the
  line's count (carry's sign law: (q_c, r') -> (-q_c, flip r')).
- Form 2: a sub-tooth residue, into a line at every click; the mirror does not commute with the floor.
- Form 3: into the step; the books of U close; the mirror is not the inverse.
- The edge: nothing leaves; the velocity's whole count is re-split at the new dial (the redshift) and the books of P
  close; the mirror negates the tooth and is its own inverse. The 00 row under the order "its click first": exact where
  its tooth fits its own now dial; a line where the 00 slot falls past it.
- Into the metric's own books: no form puts a gear's remainder into the 00 slot's gear: it would move W by the click it
  is settling (a fixed point, the same obstacle as the 00 row's self-read), and mix a sub-tooth into a count.

## Measured

In MEASURED.md (the tables) and probe_cc.txt (the numbers). In one line each:

- The act as built, Form 1 and Form 2 depart on every moving clock from round 2 (Form 2 from round 1 under its own
  convention): 3 of 24, the gears departing 28 at round 2 and 216 by round 9, |delta a| to 12 by round 16; the 14 free
  rows fall alike, -371 over 40 rounds against -81 standing. Form 1 runs on through a falling clock (the act's promise
  breaks before round 2) and runs back exactly only with its line (690 lines over 40 falling rounds). Form 2 needs a line
  at nearly every gear every round (14509 over 40 rising rounds).
- Form 3 holds the 24 on the lay rising by 1 only because it stops the clock: the 00 slot's momentum 9 x 1 re-split at
  10 teeth gives no notch, so W stands at 10 from round 1. Where the clock keeps moving it departs from round 2 as the
  act does; its U books close (0 misses) and its run back fails (0 of 40 on the falling and per-site lays; the 00 row's
  collisions).
- Form 4 (withdrawn) holds the 24 on its odd lays, keeps the drift within 7, runs back 12 of 12 with its line on a
  falling clock (23 to 35 clicks a round) and 1 of 12 without.
- The edge (the cut): 24 of 24 on every lay, standing, rising by 1, 2, per site and falling, over 16 rounds; mirror twice
  0 of 19926; run back 40 of 40 and the whole rewind exact on every lay with nothing booked; P closes to the bit; the
  rows move both ways (the redshift), no uniform vector.
- The order, the 00 slot's click first on its own dial: every number the edge's, on every lay; and where the 00 slot
  falls past its own tooth (section 4: W_00 from 14 to 9 at the lowest site) it clicks, 2 to 4 gears a round, one whole
  count each, booked; the 24 still 10 of 10 (the 00 slot is A1 and clicks alike at the turned site); the run back 10 of
  10 with the line, 5 of 10 without. The other reading (the 00 row by the act as built) breaks before round 2 on that
  lay and before round 4 on the per-site lay, and its mirror twice moves the 00 row's tooth.

## The owner's words on clocks, hands and chains

"Clocks connect and come apart; the aim is that clocks connect; that is what clicks show." Read on the forms: the 00
slot's gear is the hand that sets the teeth of every gear at the Node-clock; the edge chains a gear's velocity to that
hand at both ends of its interval (D = W(b) + W(a)), so the gear and the hand never come apart: nothing leaves, the
velocity's whole counts are re-split at the new chain (the redshift, in whole counts), the books close. Forms 1 to 3
read as arithmetic on a tooth, not as clocks connecting: Form 1 lets the gear come apart from a falling hand by a
whole notch (its line), Form 2 by a sub-tooth, Form 3 by changing the hand's own motion. The one place a clock comes
apart in the exact forms is the hand's own gear under the order "its click first": where the 00 slot falls past its own
tooth, one whole count leaves and is booked; the edge agent's cut avoids it by chaining the hand's gear to its rest
alone. That is the owner's "click in the 00 slot": the hand's gear, and only it, clicks, and only on a falling clock.

## Which form mends the defect, and what it costs

- Forms 1, 2 and 3: none mends the defect. Form 1 is the act. Form 2 crosses Postulate 2 without a line at every
  click and still fails the 24. Form 3 closes the momentum's books and restores the dropped term, but it is not a
  bijection and it stops a rising clock. Form 4 mends the 24, the drift and the mirror and is withdrawn (parity, law
  line 100); its falling-clock click is the same as the edge's would be with a single dial.
- The edge mends all four faces exactly (the 24 on every clock, the drift's bias and the uniform vector, the mirror an
  involution, the run back by the same act) with no promise and no line. It crosses: term 2's act (the carry split at a
  dial of two slots' teeth, the push doubled, the tooth signed; every gear's state keeps a signed tooth of twice the
  width), and either the loader's lay (the 00 row's self-read cut: the hand's gear not slowed by its own depth) or the
  one-act law (the 00 row's notch read first, a second split for the others: two carries in one round) together with
  a click of the hand's gear on a falling clock (a line, booked and undone by the rewind: "the beat and the time gear's
  turn are no clicks" is crossed there, and the metric clicks). The even-tie rule is a number (2) in the act and loses
  the shift covariance of a count's velocity (edge probe section 7), which no law asks. It adds to the record: a signed
  tooth per gear; under the order, the 00 slot's click lines (here 11 over 10 rounds at 27 sites, none on a rising or
  standing clock).
- The order "the 00 slot's click first" is exact on the act: on standing and rising clocks with nothing booked; on
  falling clocks with the hand's own click booked. What leaves is whole counts of motion handed to the clock: on the 17
  rows the velocity's count re-split at the new dial (the books 2 D_out S+ + T+ = 2 D_in S + T + 4 SUM push, 0 misses);
  on the hand's own row, where it falls past its tooth, a whole count into its own step and its line.

## Ready for a hostile pair?

The edge, yes, on its own page (scratchpad/edge), with two items to settle first that this probe names: which of the
two resolutions of the 00 row's self-read is the law's (the cut, or the order with the hand's click), and the even-tie
rule's number and its lost covariance. The forms of this page are measured, not candidates: Forms 1 to 3 are refused by
their numbers and Form 4 by law line 100; the order is a measured property of the edge (exact, with its one line), to be
read by the pair with the edge.

## Solution24

Step 5, add: "a gear's tooth is kept and read in one dial; a dial that two rounds read differently is a defect, not a
click; a click is where a whole count leaves and is booked." Step 8, add: "a probe that moves a clock prints the clock's
own course under each form beside the measure (Form 3 held the 24 by stopping the clock)."
