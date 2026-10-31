# The third click as the triangle's one tooth (Big Pic's bench)

Wanted, in the owner's words: the third click with at most one new number per triangle. The owner's answers of 09:30
UTC say "two new numbers per triangle are not approved", "there is surely a mathematical miracle here that solves this
cleanly" and "check what an equilateral triangle gives". The owner's word of 09:35 says to derive what is open from
ALG2's coupling complex.

Every probe here uses whole numbers, with Rule3's carry as the one division, and picks nothing. Each runs with
python3 -I on node-all 9d75a4904's carry, with the click world's spring, hands' tie, rest teeth and key.

## The form: ALG2's 2-cochain (THIRD7's member, with no twin and no turn)

- In ALG2, a tooth is a cochain: one whole number per oriented cell. A triangle's wraps are written as +w, +w, -w on
  its edges' sides by C, and never in a line, because B C = 0.
- **The triangle's one tooth tau**, born at the middle of G D, carries the circulation y = C^T x of its edges'
  passings.
- **Each edge** carries G x_e - c_e y at G D, its curl-free part scaled by G = C^T C. No division enters:
  G I = (G I - C C^T) + C C^T.
- **Each quantum that tau lands** is booked as c_e w on the triangle's edges.
- This is tri7.Member with turned=False, the unturned member that THIRD7 kept as its reading's control. It is
  THIRD9's member with its twin and its turn left out.

## What the equilateral triangle gives: the circulation is Noether's charge of the triangle's turn (DERIVED)

tooth.py checks each identity below at every round.

- **The side passing is the pair's angular momentum.** On a two-leg edge f x_u x_v, the act's own side passing is
  x_e = (kappa / 2) f (l_uv(a, a+) + l_uv(b, a)), with l_uv(p, r) = p_u r_v - p_v r_u. This is the wedge of the
  pair's two counts, taken at the round's two windows. node-all's step.passing and crossing have the same form,
  P(a, b) + P(a+, a).
- **Summed around the triangle:** y = (kappa / 2) f (L(a, a+) + L(b, a)), where L is the triple's angular momentum
  about the triangle's axis (1, 1, 1).
- **The torque identity.** The gear gives 2 D (a+ - 2a + b) = 4 F(a) + s - s', with D the gear's dial 2 W. So
  2 D (L(a, a+) - L(b, a)) = 4 a^T J F(a) + a^T J (s - s'): the force's torque plus the teeth's torque.
- **The force's torque is 0.** The equilateral potential of two-leg edges, S |x|^2 + f SUM x_u x_v, is turned into
  itself about the axis, so a^T J F(a) = 0 at every state. L moves by the teeth's torque alone: it is booked to the
  unit, as road B's energy is.
- **So the third click lands the triangle's angular momentum** in whole quanta of G D: W = (SUM y + born) div (G D).
  The landings tick at the charge's rate.
- **The lines read the components across the axis.** Each clock's net passing is (kappa / 2) f times the triple's
  angular momentum across the axis, which has two components. The circulation reads the one component along the axis.
  So the Hodge split of the edges' flows is the split of the triple's angular momentum along and across the axis.
- **In the board's continuum** the three edges' wedges close under the bracket as the turning group's:
  {l_01, l_12} = l_20, and its turns.

## MEASURED (tooth_5000.txt, 5,000 rounds each)

Every identity above held at every round on every lay: y, the lines, the torque, the zero force torque, tau's books,
and the sides' books per clock on both forms, a check by construction read through the teeth (15,000 of 15,000
clock-rounds each; first named "the books in the clicks"). On every lay the run back
from the end state alone is exact on both forms, and S_3 holds in 6 of 6. An odd turn reads each edge's tooth from its
other end, and tau as G D - 1 - tau.

| lay (now; before) | L at the lay, at the end, its range | landings over the run | the largest line, against y |
|---|---|---|---|
| turning: (40, -20, -20); (20, -40, 20), a test's lay in the triangle's own plane | 3,600; 355; [336, 3,810] | 15,009 | 1.7e9 against 0.19e9 to 2.2e9 |
| at rest: (40, 20, 1) | 0; -471; [-524, 524] | -127 | 3.0e8 against -3.0e8 to 3.0e8 |
| turning the other way (the slots swapped) | -3,600; -355; [-3,810, -336] | -15,009 | the mirror image |
| turning at ten times the counts | 360,000; 385,231; [349,434, 386,434] | 2,315,503 | 2.0e10 against 2.0e11 to 2.2e11 |
| at rest at ten times the counts | 0; 27,003; [-264, 27,003] | 83,501 | 6.0e10 against -1e8 to 1.6e10 |
| two clocks in one state: (40, 40, 7); (25, 25, 3) | 0 at every round | 0 | (the exchange, below) |

- **The charge is kept up to the teeth's torque.** At the shipped grain the teeth's torque wears it away, from 3,600 to
  355 over 5,000 rounds. At ten times the counts it stays within 7 percent. From rest, the teeth's torque builds it,
  to 27,003 at ten times the counts. This is the walk of miracle/README.md, read in the angular momentum.
- **The control:** the equilateral triangle of four-leg edges, c x_u^2 x_v^2, under the present act, laid turning. Its
  potential is turned into itself only by S_3, not about the axis.
  - The torque identity holds at every round, but the force's torque is 0 in only 96 of 2,914 rounds.
  - A count passes 64 bits at round 2,914, where the reading stops: the present act's residual heats it past its
    potential's floor (miracle/README.md).
  - Under road B, laid at rest, the same triangle stays within 6 bits over 5,000 rounds (miracle/equil.py).
- **The record (Q11: the teeth out).** c . q on the sides reads the circulation on both forms. Its running sum stays
  within 1 of 3 W under the triangle's tooth, and within 2 under the first click, at every lay. So the triangle's
  charge is in the sides on either form, as the Boss's ruling says. A click reading that tells the two forms apart
  with the teeth out is OPEN.

## The owner's guiding line (10:37 UTC), read on four starts: the board's end against the tooth's births

Four starts, by the THIRD pair's ruling (one start is one start seed): the turning lay, with the triangle's tooth
born at four places on its dial, the birth, 0, a third and two thirds. Over 5,000 rounds (tooth_5000.txt, the reading
before the exchange's):
- the board's end is one for every birth;
- every clock's line is one at every round, since B C = 0 keeps the landings out of the lines;
- the landings differ from the first birth's in 2,773, 1,384 and 1,470 rounds;
- each run back from its own end reaches its own start, the lay and its own birth, 4 of 4.

So the board's end is one against the four births. That holds by construction, since the board reads no tooth
(B C = 0). The freedom is in the member's births.

The THIRD pair's ruling (the Boss's 6542866096 item 2): one start is one start seed. So the four births are four starts,
and the board's end fixed against them holds by construction. The guiding line's second half stays OWED until a run
with one start seed shows the clicks choosing the path to one end. Its law, (C), stays OPEN.

## Clock facts: the charge is odd under exchange (the owner's Pauli lead of 10:15 UTC stays OPEN)

Renamed on the THIRD pair's physicist (B1, the Boss's 6542866096 item 2). The determinant is an exchange-odd reading,
not exclusion: two equal clocks are allowed and stay so. The owner's lead, "the reversal of the clocks by family", stays
OPEN.

- **The charge is a determinant.** L(b, a) = det(1, b, a), the three clocks' counts at the two slots under a row of ones.
- **So it is odd under the exchange of any two clocks.** The exchange is the 2-cell's orientation, the sign character
  of ALG2's complex, which ALG3 reads too. Under an odd turn the landings reverse, w -> -w, and tau is read as
  G D - 1 - tau, in 6 of 6 turns.
- **And it is 0 when two clocks share their state:** two equal columns.
- **On any triangle whose law is turned into itself by the exchange of two clocks,** a state that is its own swap stays
  its own swap. Its circulation then equals its own negative, so it is 0, and the triangle lands no third click
  (DERIVED).
- **MEASURED** (the last reading but one of tooth_5000.txt): clocks 0 and 1 laid in one state, (40, 40, 7) now and
  (25, 25, 3) before. Over 5,000 rounds they stay in one state, counts and teeth. L and y are 0 at every round, and
  the triangle lands no third click. The state is allowed and kept, so this is no exclusion.
- **The click world's open direction** (miracle/README.md) is the exchange-odd mode of its two like hands, the giver
  and the taker. Their pair form [[c h^2, t/2], [t/2, c h^2]] has its lower value, c h^2 - t/2, on (1, -1) (DERIVED).

## Three like hands: the floor by itself (the owner's words of 10:11 to 11:10 UTC; FLOOR1's pairs; David's Harary rule)

- **node-all's own rule** (plans.tying): the hands' tie bands every two distinct tied trains of one part. A train is tied
  when its character is kept under the sign kind's twist and it is not the held hand, as the giver and the taker
  (T1, T2) are.
- **So the click world's two tied hands make one band.** Under the square form that is an even structure, at the
  floor's edge, with one free swing (FLOOR1).
- **Three tied hands of one part would be banded pairwise by the same rule:** a plain triangle of bands, a frustrated
  loop. Under the square form every swing then holds a spring: each hand gets t, the two swings that sum to 0 hold t/2
  each, and the common swing 2t (DERIVED; Harary's balance).
- **MEASURED** (frustration.py, frustration_20000.txt; a test's lay in a stand-alone model, the MIRACLE pair's
  mathematician): the click world's band as its own square, no own spring laid and no held hand (FLOOR1's clean test of
  the edge), the hands' difference moving, 20,000 rounds:
  - two hands on one band: the free swing drifts linearly, the largest count 4,040 at round 4,000 and 20,040 at round
    20,000;
  - three hands on a plain triangle: the largest count at most 88 over the run;
  - the identity and the run back exact in both.
- **The mathematician's reading:** "three like hands are the fewest that hold by themselves" is a theorem under the square
  form with bands alone, and David's 2 : 1 : 1, the swings' frequency ratio, is whole only at n = 3.
- **So three like hands are the fewest whose floor holds by itself,** and their bands are the equilateral triangle of
  two-leg edges, on which the third click's charge is kept (above). Whether the structure lays a third tied hand is
  OPEN: the click world as laid has two.

## The twin and the turn, read against the one tooth

- With one tooth, every check that THIRD9 read with its pair holds on the equilateral triangle:
  - the sides' books per clock, by construction;
  - the triangle's own books, tau' + G D w = tau + y;
  - the run back from the end state alone, with tau kept by the carry's sign law;
  - the whole of S_3.
- The turn makes the landings' timing follow the pair's hidden digits. Under Q10, a clock reads only its own clicks,
  and no landing ever enters a clock's line (B C = 0). So the turn hides nothing that a clock reads. The member is
  never "the choice" (the Boss's 08:1x ruling).
- **No new number at all (ALG3's count, MEASURED here).** The edges carry curl-free passings, c . (G x - c y) = 0, so
  their teeth's circulation c . f stays at its birth's value mod G D at every round (5,000 of 5,000 on every lay). One
  edge tooth is then the other two's double, and tau takes its place. So the third click is the first click's three
  numbers, re-routed: the circulation moves out of the edges' teeth and into the triangle's one tooth.
- **The choice (ALG3's Q1).** The tooth does not turn: the path is a plain carry of the circulation. Any choice in it
  sits in the births, by road (C)'s seeds' law. A turned tooth would force the twin (ALG3 5.4).
- So no check here needs the twin. The third click is one number per triangle, the 2-cochain's. It is set by the
  board's own flows, and on the equilateral triangle by its conserved charge, not by a hidden pair.

## OPEN

- **The third click is not seen in the clicks** (the THIRD pair's B2). With the teeth out of the record, no click
  reading tells it from the first click. A click reading that the first click's record fails is a condition of the
  closed picture. Which edge tooth is read back is this form's to name, with no pick by order.
- **The count, read by the THIRD pair's mathematician:** no new number, but (3 D)^3 states against D^3, a factor 27.
  The charge needs equal springs, equal ties and one gear dial.
- **The click world's own triangle** has four-leg giver-held and taker-held edges and a two-leg giver-taker edge. Its
  potential is not turned into itself about any axis, so its circulation is no conserved charge. Its landings follow
  the flows.
- **The uncertainty relation among the click readings.** The lines and the third click read the components of one
  angular momentum, across and along the axis, and their brackets are the turning group's. A relation between the
  click readings themselves is OPEN. UNC2 keeps the name "uncertainty principle" for place and motion, read by light's
  echo.
- **Road (C)'s births on the one tooth:** tau's birth, read from the seeds' law.

Usage: python3 -I tooth.py <node-all src> <the click world's universe.json> [rounds]

## The third click that writes and chooses, a first stand-alone model (turns.py, turns_5000.txt)

- **The owner's words of 12:23 to 12:28 UTC** (the Boss's 6543327690, 6543337835 and 6543366692): "Only the third click
  writes to the board and chooses... it is the important one"; "The clicks' floor, from their structure alone..."; "the
  first 2 clicks represent the initial conditions of the universe; the third, the choices that change the universe
  from the path without the choices".
- **The model** (a test's lay in a stand-alone model, not the engine's board):
  - three like hands on one triangle of bands, each band its own square at the click world's hands' tie, with no own
    spring and no held hand: the frustrated loop that holds a floor by itself;
  - the engine's gear form, whole numbers and Rule3's carry only;
  - the triangle's one tooth tau carries the bands' circulation, as tooth.py's member does.
- **The write:** at each landing w, the third click turns the three hands' whole state, with the triangle's edge
  teeth, by the cycle (0 1 2) taken w times.
  - The turn is a symmetry of the triangle's law, so the round commutes with it.
  - The circulation is kept by it, and so are every clock's books and the energy.
  - B C = 0 leaves no other write that keeps a clock's books (third/README.md, OPEN above).
- **MEASURED, 5,000 rounds, two lays, tau born at four places:**
  - E32's change equals the teeth's share in 5,000 of 5,000 rounds, the turns included.
  - **The floor holds by the structure alone:** the widest count is 12 bits laid turning and 7 bits laid with the
    hands' difference moving.
  - **The three states, taken as a set, are the unwritten path's at every round**, for every birth. So the end is
    fixed as the like hands' state, and the writes change only which hand holds which state.
  - **The writes are seen in the lines:** laid turning, a clock's own count differs from the unwritten path in 3,327
    to 3,384 of 5,000 rounds, by birth. So the births choose the path.
  - **The labelled end** is the unwritten end turned by the net landings modulo 3. Laid turning, the net is 17,575
    at every birth, so the net turn is 1: the end as labelled differs from the unwritten end, and no birth here keeps
    it. It equals the unwritten end only where the net is a multiple of 3, a condition the start and the end fix
    together.
  - **The run back from the end state alone is exact,** the writes part of the state, at every birth on both lays.
  - **Laid with the hands' difference moving,** the circulation is 0: no landing, no write, the path the unwritten one.
- **So, as first read** (withdrawn in part on the THIRD pair's verdict below):
  - the third click writes by turning its triangle of like hands;
  - the floor is the triangle's own, from the structure;
  - the end stays fixed as a state of like hands, with the choices in the labels along the path.
- **The THIRD pair's verdict: NOT PASSED by both** (the Boss's 6543768769 item 3 and 6543794891; their reports at
  S/bp_turns_phys and S/bp_turns_math). Taken whole:
  - **The write is a relabelling** (the physicist's B1). Every label-free reading equals the unwritten path's: the set
    of states, the energy, the circulation and so the landings, in 5,000 of 5,000. The end is fixed only as a set; by
    label it moves, and no birth fixes it. So "the writes are seen in the lines" is withdrawn: they are seen by label
    alone, against a run no clock holds, and by the Boss's ruling a relabelling of like hands is a choice of names,
    not the owner's write.
  - **Each clock's books break at every write** (the mathematician's B1, the physicist's B2). Read per clock on
    tooth.py's form, each clock misses its books at every write round, three misses per write (7,170 of 15,000 rounds
    at 2,390 writes; with no write, 0). A write moves each clock's whole state and its energy to the next clock, and no
    side carries it. The total is kept by construction alone. turns.py's docstring is mended.
  - **The net turn** (the mathematician's B2): "the net is 17,575 at every birth" holds for the four births tried
    alone. On this lay a birth gives a net turn of 1, or of 2 from birth 404,748,936 on (11.5 percent of the dial), and
    never 0, so the unwritten end is not reached on this lay.
  - **The floor is the bands' own form** (the physicist's m2): V = (t/2)(|x|^2 + (SUM x)^2), springs t/2, t/2 and 2t,
    held over 10^6 rounds with no write. It is a board structure, not the clicks'.
  - **SOUND, both readers:** the turn is an exact symmetry of the isolated round in whole numbers, carry and teeth
    included (5,000 of 5,000 rounds on all eight runs); the run back from the end state alone is exact at every birth.
  - **On a joined board a turn is no symmetry** (the physicist's m1): E32's change parts from the teeth's share at
    every write. write.py reads the same on two joined triangles (below).
- **Not shown:**
  - the click world's own triangle, which is no triangle of like hands;
  - a swap, the odd move, which reverses the circulation and the owner's Pauli lead would ask;
  - the lines read as clicks, not as counts;
  - whether a turn of like hands is the write the owner means;
  - the engine's act;
  - any physics.

Usage: python3 -I turns.py <node-all src> <the click world's universe.json> [rounds]

## The third click's cone, a first stand-alone model (cone.py, cone_5000.txt)

- **The owner's word of 12:4x UTC to Big Pic** (in Hebrew; in my translation): "... and check whether the cone is
  needed on the board... of the third click... is it a cone to the past and to the future?"
- **The model** (a test's lay in a stand-alone model, not the engine's board):
  - turns.py's three like hands on a triangle of bands, laid turning, with its write at tau's landings;
  - each hand also banded to one hub clock, and the hub at the end of a chain of 6 bands, each band its own square at
    the click world's hands' tie, with no own spring laid;
  - the rest of the board reads the three hands only through the hub, alike, so the turn is a symmetry of the whole
    round;
  - the far clock laid apart by amplitudes.py's top swing, 163,840.
- **By construction:** the round reads a clock's own state and its neighbours' counts alone. So nothing reaches farther
  than one edge per round, and the run back is the same round, so the same holds in the other sense of time.
- **MEASURED, 5,000 rounds, tau born at two places:**
  - E32's change equals the teeth's share in 5,000 of 5,000 rounds, the turns included; the widest count is 12 bits.
  - **The past cone.** Two starts apart at the far clock alone. No clock's count comes apart sooner than its
    distance: the chain at rounds 1, 9, 40, 84 and 135 (distances 1 to 5), the hub at 190 (distance 6), and the
    hands at 208 to 213 (distance 7). Tau's landings first come apart at round 216 and 219.
  - **The future cone.** Two ends apart at the far clock alone, each run back from its end state alone (the run back
    exact). Counted back from the end, the same holds: 1, 9, 40, 84, 135 and 190, and the hands at 193 to 198.
  - The reach is far inside the cone: the cone is a bound, and the bands' own speed is far below it.
  - **The write's own reach.** With the writes and without, the hub's and the chain's lines are the unwritten path's
    at every round. The hands' own lines come apart at round 1, tau's first landing.
- **So, as a reading:**
  - no cone needs laying on the board: the round's own reach is the cone, one edge per round, the same both ways in
    time;
  - the third click's write is local to its triangle, and, with the rest reading its like hands alike, nothing
    outside sees it: here the write's future cone outside the triangle is empty;
  - the choice at the triangle at round n is fixed by the start within its past cone (the start's clocks within n
    edges) and, the run back exact, by the end within its future cone (the end's clocks within N - n edges): a double
    cone, to the past and to the future;
  - for a pair (bellend.py), the two wings' past cones meet at the source, and their future cones meet where the two
    readings are joined. That is where the 11:52 law's connection, from the start and from the end, can run with no
    reach beyond the cones. CANDIDATE, not run.
- **Not shown:**
  - a write that others read: it must tell the like hands apart, and then the turn is no symmetry of the round, so
    the energy is not kept under it (OPEN, for 12:28);
  - the cone on the engine's act and on the click world's own triangle;
  - the pair run with the double cone;
  - any physics.

Usage: python3 -I cone.py <node-all src> <the click world's universe.json> [rounds] [chain]

## The write the rest read: the condition and two writes on two joined triangles (write.py, write_2000.txt)

- **The owner's word of 13:0x UTC** (the Boss's 6543746068 item 1): "There is a connection between click 3 and click 3
  and the rest, because the universe must return to what the future fixed... and it changes its path only through
  click 3... Is the coupling family inside?"
- **The ask** (the Boss's 6543746068 item 3 and 6543794891 item 4): a write that the rest read, that keeps each clock's
  books by a passing, that stands on a meshed board, and whose sum over every triangle meets the fixed end, read by
  label.
- **DERIVED, the condition on a write between rounds.**
  - Let R be the round, M the mirror (the run back is M R M = R^-1), and W(w) the write at a landing w, so a step is
    F = W(w(X)) R.
  - The same act runs back exactly when M F M = F^-1, that is when R^-1 W(w) R = M W(w')^-1 M, with w' the landing the
    run back reads (-w).
  - The left side moves the write one round back, which the round spreads to the write's neighbours. The right side
    is a write at the same place. So a local write is undone by the same act only when it commutes with the round: a
    symmetry of the whole round.
  - On a board that reads the hands apart, such a write fixes all that the rest reads.
  - **So the rest reading the write, each clock's books, and the same act's run back cannot all hold for any write
    between rounds.** turns.py's turn keeps the run back because it is a symmetry, and so nothing label-blind reads it.
- **The model** (a test's lay in a stand-alone model, not the engine's board):
  - two triangles of like hands, A and B, each a triangle of bands at the click world's hands' tie, joined by one band
    between a hand of each, so the rest reads each triangle's hands apart;
  - this is a stand-in for a meshed board: the Mesh's own crossing is not built here;
  - A is laid as turns.py's turning lay, and B as that lay turned once; each triangle's tau carries its own
    circulation.
- **Two writes at each landing w,** against no write:
  - **the whole turn**, turns.py's write;
  - **the momenta turn**, new. The hands' exact momenta P = 2 G (a - b) + s are turned by the cycle, w times (mod 3).
    The counts are kept, so the teeth alone move: no clock's count or energy moves at the write, and the momentum moved
    enters each hand through its own tooth at the next round.
- **MEASURED, 2,000 rounds:**
  - **No write:** each clock's books hold in 12,000 of 12,000; E32's narrowest is 956 per mille of its widest; the run
    back is exact.
  - **The whole turn on the joined board:**
    - each clock's books hold, read across the write as the THIRD pair read them, in 3,082 of 12,000;
    - E32 moves at 2,677 of 3,951 writes, and its narrowest is 390 per mille of its widest;
    - the rest read it: B's clock 3 is apart from the unwritten path in 1,999 rounds;
    - the run back by the same act is not exact.
  - **The momenta turn:**
    - each clock's books hold across the write in 12,000 of 12,000, by the round's own identity, since no count moves
      at the write;
    - E32 moves at 0 of 3,980 writes;
    - the rest read it: B's clock 3 is apart in 1,999 rounds, and A's clock 0 in 1,990;
    - the run back by the same act is not exact, as the condition says;
    - its cost: the momentum moved is booked through each hand's own tooth, not by a side, and E32's narrowest over
      the run is 757 per mille of its widest, against 956 with no write.
  - **The ends over a grid of 12 x 12 births of the two taus, 1,000 rounds:**
    - with no write, the 144 pairs of births give one end;
    - under the momenta turn they give 144 distinct ends, one pair of births for each;
    - each triangle's own part of the end takes 144 values, so each hangs on the other triangle's birth too.
- **So, as a reading:**
  - a write the rest read is in reach: the momenta turn is read by the rest, keeps each clock's books at every round
    and E32 at every write, and stands on a joined board;
  - under it, the end fixes both triangles' choices together. Each triangle's end hangs on the other's choice through
    the band between them, within the cone: the 13:0x connection between click 3 and click 3, here through the board
    and the end;
  - what it does not keep is the same act's run back, and the condition shows that no write between rounds that the
    rest read can keep it.
- **The way left open by the condition, DERIVED and not built:** the third click inside the round, not between rounds.
  - tau's record is split into its two half-windows, the half before the round and the half after;
  - the round reads the triangle's landed count at the round's centre, which is the same count both ways in time;
  - so the act's run back is exact by construction, and the write is a term of the round that the rest read;
  - its energy would be booked as a passing from the triangle's tooth (named), and its choice is tau's birth.
- **Not shown:**
  - the Mesh's own crossing;
  - the third click inside the round;
  - the energy kept to the board's own band under a write;
  - the sum over many triangles meeting a fixed end that is laid in advance;
  - any physics.

Usage: python3 -I write.py <node-all src> <the click world's universe.json> [rounds] [grid] [grid rounds]
