# The hostile mathematician on SPLIT2 (the weights from the law), 2026-10-31

(Written by the Boss from the reader's hand-back, 04:4x UTC; the text is the reader's, shortened in layout. Evidence in
split2_math/: rerun1.txt, rerun2.txt, split2_probe.txt (byte-identical to the frozen split2_run1.txt, run on live
7dcb31607's src, the frozen folder having no nl/src), ring_count.py and ring_count.txt (whole numbers, run twice).)

VERDICT on SPLIT2: NOT PASSED (two BLOCKING items; five MINOR)

## BLOCKING

B1. Step 4's "n equal whole parts" are equal parts in the algebra only, so step 5 does not follow from steps 2 to 4
(steps 4 and 5; the verdict's "the road goes through on three named premises"). The classes of Z[q] / q Z[q] are
residues of an abstract ring: nothing in the act divides a take into them, carries them or draws among them. P2 is a
premise about takers (two trains alike but for their labels); step 5 applies it to these classes as if each were a
label-alike sub-taker, which needs a fourth premise, P4: the draw treats the n classes of the hand's ring as n
label-alike sub-takers (Zurek gets it from a physical fine-graining, an ancilla splitting a branch into equal ones).
Unnamed, P4 is Born's rule restated. The measured agreements (802 and 809 against 800; 359 against 360) do not test
step 4: the toys' passing is k times the square by construction (turnteeth.py: xa, xb = 9 k, 16 k; THIRD5's k a s_i),
and in the carried form the takes are the passing over D within one click by the carry's identity, whatever the passing
is; so they test the carry's additivity and the turned tooth's fidelity in frequency. What the road derives: a share
proportional to the passing's measure, from additivity plus P2; the square itself comes from THIRD5's bilinear passing
(Euclid's leg theorem), a form taken, not derived from the law. Fix: name P4, or show an operation of the act carrying
a hand of norm n onto n equal unit passings with the draw commuting with their swaps; otherwise restate step 5 as "share
proportional to the passing; the passing's square from THIRD5's form".

B2. The count's exponent is the choice of ring: step 4 picks no basis but picks the measure (ring_count.txt):

| ring | rank | the count | example |
|---|---|---|---|
| Z, the hand's own ring when it is scalar | 1 | abs(a) | the scalar hand 3: 3 |
| Z[q], the hand's own ring | 2 | N(q) | 7 hands, from 2 to 25 |
| L, the board's whole quaternions Z<1, i, j, k> | 4 | det(left multiplication) = N(q)^2 | 4, 25, 16, 121, 81, 81, 625 at the same 7 hands |
| Z[i], fixed, at a scalar hand | 2 | a^2 | 4, 9, 25 |

So "the square comes from step 4's count, the board's own quaternion algebra" is not right as stated: the board's own
algebra gives the fourth power of the rows; the square comes from choosing the rank-2 subring the hand generates. The
text is inconsistent with itself: probe part (d) counts two-row hands in the fixed ring Z[i], step 4 counts four-row
hands in the hand's own Z[q]; with a fixed ring throughout the four-row count would be N^2. The scalar exception (P3)
is a symptom of the choice: Z[q] collapses to Z whenever the vector part is 0 at the reading (a held hand whose A2 row
stands at 0 counts abs(a); q = 0 has infinitely many classes), so the count jumps where the square is continuous; Z[i]
fixed has no such exception. Fix: name the ring as a premise (it is the measure), or derive why the hand's own rank-2
ring, not the board's quaternion order, is the one the draw counts.

## MINOR

1. The turned tooth reads a label each round: its shear cycle's sense follows the takers' order (ab += ga, gb -= ab,
   ga -= gb), so each round's count depends on the order in universe.json, a label behind a count draw by draw under
   the owner's rule, not only "P2 failing draw by draw"; "in frequency" saves the shares, not the clicks. Section 4's
   sense-free turn is the remedy; say why it is required.
2. The yardstick: the 20 lays' z^2 sum to 8.089 against an expected 20, so the data reject the independence model
   (under-dispersed), as the text itself reads; the pooled equality stands (25,675 against 25,479), but the binomial is
   not the spread to quote it against.
3. "The hand counts their sum" for a T1 + T2 taker adds class counts from two rings, Z[q1] and Z[q2]; six rows are not
   one quaternion; the commensurability of the two rings' classes is a further identification. Name it.
4. "834 millionths against k / D, 799" for two takers: a 4.4 per cent excess, about 1.9 sigma on about 2,000 takes,
   unremarked; say whether it is the turned tooth's correlation.
5. The probe's tree: it imports node-live's nl/src, which the frozen folder lacks; on live 7dcb31607 it reproduces byte
   for byte. Name the tree it ran on.

## The four points pressed

- The class count: the algebra is right (q q = t q - n is q's characteristic polynomial; Z[q] = Z + Z q has rank 2 when
  the vector part is not 0; the index of (q) in that quadratic order is abs(N(q)) by the norm formula); but the classes
  are equal parts only in the algebra (B1), and their number depends on the ring chosen (B2).
- P2 is a premise, honestly named: with Big Pic's turned tooth, S D S = D' is the reverse-sense dynamics, so the swap
  gives nothing about D's own frequencies; P2 would follow from the act's relabelling symmetry only with a sense-free
  turn and a lay the swap keeps (section 4's road, not built).
- The scalar exception: the collapse of Z[q] to Z; a fixed ring has none (B2).
- Basis, number, label: no basis picked (Z + Z q is basis-free), but a ring picked (B2); the numbers are named
  stand-ins (dial 50,811,429, divisor 1,250, the 64-bit generator's constants, the squares); the one label is the
  turned tooth's sense (MINOR 1).

## SOUND

The quaternion identity at 1,000 of 1,000 hands (alpha = -n, beta = t by Rule3's carry); the Gaussian class counts at
all seven hands; Legendre's misses among 1 to 64 exactly 4^a (8 b + 7), Lagrange none; "the 24 alone cannot pick the
square" (both measures kept, 96 of 96); T's determinant 1 (checked by hand) and P T P = [[1, 1, -1], [0, 1, -1],
[-1, -1, 2]], neither T nor T^-1; the carried form commuting with P exactly (500,000 of 500,000 rounds, the totals 10 of
10); P1 and P2 named and come back in section 4; no float or root.

## DERIVED / MEASURED / OVERCLAIMED

- DERIVED: shares as frequencies (on P1); equal shares for parts a turn relates (on P1); the act's commuting with the
  relabelling; P T P != T; index = norm in Z[q]; the 24 keep both measures.
- MEASURED (a board stand-in): the frequencies, the swap's parting and its exactness without the turn, the identity,
  the class counts.
- OVERCLAIMED: "three named premises" (B1 needs a fourth); "the square ... the board's own quaternion algebra" (B2);
  "the road from the law fixes which measure the passing must carry" (it fixes share proportional to passing).

## The reader's question for the Boss

Which ring does the law's count read: the hand's own Z[q] (the square), or the board's whole quaternions (the fourth
power)? Is the coincidence index = norm the miracle principle's road, to be made operational by an act that fine-grains
a passing?

## Solution24 (the reader's line)

From the law, the shares follow the passing. The square in the passing stands on THIRD5's bilinear form until a
fine-graining in the act, or a named ring, carries it.
