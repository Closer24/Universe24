# ANIMATE-SPRING: the gear's spring as one algebraic operation of the Node-clock's act

The owner's word to Animate (2026-10-30, 06:4x UTC, in Hebrew; in translation): "Did you pass to everyone which part
the Node-clock lacks? It is needed as an algebraic operation in the node." The part the hostile readers of both pages
found missing is the spring: no gear on the head holds a beat of its own (the decoder's page 1.4, git 8c4f3ff59; board2mass 3).

Run: `python -I tools/derivations/open_items/ANIMATE-SPRING/spring.py` (under a second; the output is spring.txt).
Whole numbers only, on the head's own gear step (engine/step.py, gear) at the head's teeth W from the example files.

## The operation

At every Node-clock, every round, at the now slot; x a family's gears there, k the coupling family's held count there,
here of kind A1 (the E or T2 count that three masses need has its own operation, OPEN: the decoder's page 3.8.7, git 8c4f3ff59):

1. **Contract:** c = the sum over i, j of C[i, j -> k] x_i x_j (for a T1 family and an A1 count, c = x . x).
2. **Push each gear (the spring and its bound):** P_i = -g k x_i - lam c x_i.
3. **Push the held count:** Q = -(g / 2) c - kappa (k - n).
4. **Into the act:** P and Q are sources of the drive and reach the step through the kick (TENSOR24_NODE.md, terms 7
   and 8): W (a+ - 2 a + a-) = the push, the remainder kept.

The pushes are minus the derivatives of one potential, V = (g / 2) k c + (lam / 4) c c + (kappa / 2) (k - n)^2, so the
vertex pushes all its legs. Sums and products of whole counts and table entries; each strength a quotient by the carry.

## What it shows (spring.txt)

1. **The beat is the mass:** laid at 10^5, the gear beats 64 sign changes in 4,000 rounds, a period of about 126
   rounds, as one spring at W div 400 gives, with the four-leg term at 0, at half the bound or at twice it alike.
2. **The four-leg term bounds the gear's swing, and the held count still gives way:** laid at 10^7 and 2 x 10^7, the
   gear runs away with no four-leg term (rounds 49 and 29, as David's m3 (i)) and at half the bound (rounds 205 and
   50), and stays over 4,000 rounds at twice the bound, its largest local spring 12 and 43 thousandths of W. But the
   held count is held by its own spring kappa alone (the four-leg term pushes the gears, not the count), and at these
   swings it falls below 0 (least -3,112,715 and -8,012,335; below 0 in 1,913 and 2,555 of 4,000 rounds): the gear's
   beat is then 95 and 206 sign changes, not the mass's 64. The bound, lam at least g^2 / (2 kappa), is exact: with
   the count at its minimum the potential keeps (lam / 4 - g^2 / (8 kappa)) c c.
3. **The ceiling:** the beat is the mass only for swings whose push moves the held count little, its shift at the
   swing's top, g x^2 / (2 kappa), far below n: 199 at 10^5, against 1,999,999 at 10^7 and 7,999,999 at 2 x 10^7.
4. **The step's limit:** laid at 10^8 the gear runs away even at twice the bound (round 14). The four-leg term's own
   spring is W at the lay, the held count falls to -296 n, and the local spring first passes 4 W at round 9, where a
   lone gear's step x+ - 2 x + x- = -(D / W) x beats no more (the board's top mode holds only below 2 W). The
   potential is bounded; the step holds it only while every spring stays far below W.
5. **The channel:** on a T1 family of three gears at twice the bound, laid at one length along an axis (10^7, 0, 0)
   and off it (6 x 10^6, 8 x 10^6, 0), the four-leg term through A1, (x . x)^2, beats alike both ways (95 and 95 sign
   changes of the gears' sum); the sum of x_i^4, which the 24 also allow, does not (95 and 66): it reads the board's
   axes, so the four-leg term goes through A1 alone.

## What does not follow

- **The strengths:** g, lam and kappa and the held count's steady count n are set by hand here, as in David's m3; on
  the act they are the law's (decision 35; decision 40 (g)), OPEN at G3 (TENSOR24_NODE.md 4.2, David derives).
- **The neighbours:** the probe steps one Node-clock's gears with no Mesh; on the board the pull joins them.
- **The strengths' remainders:** each strength's quotient drops its remainder here, a probe's simplification.
- **The head:** run at reader-5 after tensor24-review 68c7245ef (the Mesh unit 1, W = 6 den Gamma^2, about 9.1 x
  10^22); every strength scales with W, so the counts are the same as at the earlier W of 2.3 x 10^25.
- **The held count's own spring** kappa (k - n): a hat of the held family itself, -(mu / 2) k k + (nu / 4) k^4, would
  give n and kappa from its two strengths, as nature's held field has them, though not the spring's sign: its minima
  at plus and minus n give springs of plus and minus g n; OPEN.
