# The HALF mathematician on GEN3, 2026-10-31

(Written by the Boss from the reader's hand-back; the text is the reader's, shortened in layout. Evidence:
hf_math/probe_hm5.py and probe_hm5.txt, run twice identical; exact integer elimination, Rule3's carry the one
division, no float, root or math module.)

VERDICT on GEN3: NOT PASSED (one BLOCKING item, three MINOR)

## BLOCKING

B1. The theorem "a real spring gives at most two rates ... never three" (section 1, last bullets) is false as stated,
and every later use inherits it (section 3's reading 1, "two rates at most without it"; section 4's "a third rate").
- What is true, and what GEN3 derives: no real spring parts 2' from 2''. A real C kept by the 24 commutes with every
  L(g), hence with Q; its restrictions to 2' and 2'' are complex conjugates. A C kept by all 48 is also conjugated
  onto itself by the r2 lifts, which swap 2' and 2''. Either way every rate of 2' is a rate of 2'' with the same
  multiplicity.
- The count of distinct rates is not two. On the 24-gear train's real form the commutant has a quaternion block for
  E1/2, a quaternion block for E5/2 (which also restricts to the doublet 2 under the 24) and a 2 x 2 quaternionic
  block for the two G3/2 copies (which carry 2' + 2'').
- Measured (Krylov rank of a symmetric spring, two draws each): a symmetric spring kept by all 48 gives 4 distinct
  rates; one kept by the 24 alone, GEN3's own part-5 setting, gives 6. Species 2 alone already splits in two (E1/2
  against E5/2). What no real spring can give is three different rates to 2, 2' and 2''.
- Fix: "a real spring never parts 2' from 2''"; the third species-rate, not a third rate, needs a term odd in Q;
  re-read section 3's reading 1, since a species may not carry one rate.

## MINOR

1. "The half-speed hand on the three axes is HALF2's 24-gear train": the hand E1/2 x T1 (12 real dimensions) is not
   the train; the train holds the hand's real form with its Galois partner E5/2 x T1 (twice the hand's real form
   under the 24). "Is" should read "holds, with its Galois partner". "No new train is needed" stands.
2. The leak "under one per cent": the ratios are right (800 / 119,104, 1,000 / 149,158, 800 / 107,712, 916 / 130,032,
   0.67 to 0.74 per cent), but the carry's rounding is O(1) per gear per round, so the percentage depends on the drawn
   amplitude and the 400 rounds. Report it absolute, or show how it scales.
3. "C commutes with Q (measured: Q is central)": C commutes with Q because it commutes with every L(g) and Q is a sum
   of L(g); Q's centrality is a separate fact. Reword.

## SOUND (on paper and against the probe)

- The 24 are Q8, w Q8 and w^2 Q8 (w^3 = 1, Q8 normal, w's turn i -> k, j -> i, k -> j).
- The seven kinds of 2T (degrees 1, 1, 1, 3, 2, 2, 2; squares sum 24) orthonormal exactly; the inner product
  conjugates right, conj(p + q w) = (p - q) - q w.
- The restrictions: 2 x 3 = 2 + 2' + 2''; G3/2 to the 24 is 2' + 2'', so the 8-gear train gives 2 2' + 2 2''; the
  24-gear train 4 of each; T1 x 2 G3/2 has the 24-gear train's character, one 24-gear orbit by HALF2's classification.
- Pi = 12 P: Pi_2 + Pi_c = 12 I, each squares to 12 times itself, they annihilate each other, ranks 8 and 16, both
  whole. Q antisymmetric (inversion swaps w's class and w^2's), 0 on 2 and -+2 sqrt(3) i on 2' and 2'', so
  Q Q = -12 P_c = -Pi_c; the r2 lifts send Q to -Q.
- The share 1/3 per axis row DERIVED soundly: every irreducible subspace is invariant under L(w), which cycles the
  axis blocks.
- Section 2's analysis right: a push odd in Q on the now slot gives complex rates; a gyroscopic Q (a - b) gives real
  split rates but breaks hypothesis (d); a reversible midpoint form needs a matrix inverse, not Rule3's carry.
- Z[w] lawful under ruling 4 a fortiori (Z[x] / (x^2 + x + 1); conjugation x -> -1 - x; only equality tested); the
  src plan can avoid Z[w], needing only chi_2, chi_2' + chi_2'' and Q.
- No construction is a root, search, sign test or table; the src plan states honestly that Q's orientation is a
  choice equal to the sign of its strength.

## DERIVED / MEASURED / OVERCLAIMED

DERIVED: the share 1/3; 2' and 2'' never parted by a real spring; section 2's shape and three causes. MEASURED: parts
1 to 6, the leak for the drawn amplitude. OVERCLAIMED: "at most two rates, never three" (B1); "is HALF2's 24-gear
train" (minor 1).

## The reader's question, and the Boss's ruling (03:0x UTC)

Q: do the generations need three species-rates (2, 2', 2'' each apart), or three rates of any kind?
Ruling: not ours to choose on the board. GEN4 states both clock facts exactly (the count of rates; 2' = 2'' at every
rate without a parting coupling) and puts the question to Big Pic as his reading; it chooses nothing.
