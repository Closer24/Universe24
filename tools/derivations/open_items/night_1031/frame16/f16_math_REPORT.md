# FRAME16, the hostile mathematician's report, 2026-10-31

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's, shortened in layout. In f16_math/: the four frozen probes copied with only their import paths changed, each
rerun identical (p_*.rerun.txt); the reader's m_check.py, m_check2.py, m_check3.py with their .txt. Whole numbers;
the one division the engine's carry; Bareiss's exact divisions checked to leave remainder 0; each window stated.)

VERDICT on FRAME16: NOT PASSED

Most of the algebra is right: Sylvester, S C S = E C E^T, conjugation, the a p b theorem and section 4. It buys less
than 0.3 claims: the (1, 3) "held" is a property of the reading S -> S C S, not of the act; the candidate's own law
W = Re(s0 s0) gives zero or negative teeth at most invertible rounds of the text's own runs; the gauge is not
transversal at the flat point the text names; the tie holds only because of the probe dial's residue.

## BLOCKING

B1. The candidate's W fails on its own runs (0.3 lines 31-34; 2.3).
- Reading p_gauge2's two runs with the text's law (W = S00^2 - S01^2 - S02^2 - S03^2 as the clock's teeth): W <= 0
  at 835 of 1100 and 807 of 1101 invertible Node-clock-rounds (m_check2.txt). On p_slots' starts read as S: W <= 0 at
  964 of 1101 (large) and 260 of 1107 (small, base 16).
- Exact, on the act's own free motion: S = 4C with a uniform stride +1 on S01: W = 16 - t^2 reaches 0 at round 4
  (det S = -512) and -9 at round 5; the signature stays (1, 3) throughout. At W = 0 the dial is 0 and carry(5, 0, 0)
  raises ZeroDivisionError.
- 2.3 measures the tip only for the untied frame (81, 871, 1004), never for the candidate.
- Fix: do not call 0.3 HELD; measure the tip on the candidate's own runs; state W >= 1 and 3 grip <= W as laws still
  owed (Sylvester does not give them).

B2. Sylvester holds for every S, so measuring it on the act tests nothing; and the act does reach det S = 0 (0.3, 2.2,
1.4).
- (1, 3) at every invertible S is a theorem about the reading: over all 3^10 symmetric S with entries in {-1, 0, 1},
  44,868 of 44,868 invertible S read (1, 3). So "MEASURED (1, 3) at 1100 and 1101" cannot fail; "cannot turn over" is
  unconditional too (no singular S reads two positive squares).
- The real question is det S, and the act reaches 0 exactly: from S = 4I with stride -1 on S33, det S runs 256, 192,
  128, 64, then 0 (reading (1, 2, 1)), then -64 and back to (1, 3). In p_gauge2's own runs det S changes sign between
  rounds without a zero 261 and 189 times (only 7 and 6 rounds land on 0); in the reader's runs 286 crossings against
  6 landings (large start), 858 against 6 (200 rounds).
- Nothing holds det S off zero: on a uniform board the stride is kept exactly (Newton's first law); at the text's flat,
  det(L I + t V) = prod (L + t lam_i(V)) has only real roots, so a zero comes forward or on the run back.
- Fix: the signature DERIVED only; count crossings, not only landings, as singular passages.

B3. The gauge is not transversal at the text's own flat (3.3 against 0.3's "Flat: S = I").
- "so(1, 3) meets {X : X C symmetric} only in 0" is true only at E = I, that is S = C. At E = S C the gauge is
  transversal iff no two eigenvalues of S C sum to 0. The determinant of Y -> A Y + Y A^T on antisymmetric Y: 0 at
  S = I and at 2I, 64 at S = C, -64 at diag(3, 1, 1, 1).
- At S = I the boosts lie inside the gauge. Whole example: Lam = [[3,2,2,0],[2,2,1,0],[2,1,2,0],[0,0,0,1]] (gamma 3)
  gives S' = C Lam C = [[3,-2,-2,0],[-2,2,1,0],[-2,1,2,0],[0,0,0,1]], symmetric and reading exactly C, as S = I does.
- "E symmetric" and "E C symmetric" turn into each other under the internal parity C (in O(1, 3)), so the text's "E
  symmetric is not a gauge, the boosts lie in it" condemns its own gauge at S = I.
- At S = L I the ten gears do not chart the ten slots; the reading has rank 7 there (S = 4I with S01 = S10 = 1 reads
  diag(15, -15, -16, -16), g01 = 0). The act crosses this locus 183 and 112 times in p_gauge2's runs, 368 and 413 in
  the reader's.
- Fix: the flat S = C (E = (1, i, j, k)), or diag(L, l, l, l) with L /= l, with the condition stated. The reading's
  singular set is prod_{i<=j} (lam_i + lam_j) = 0; det S = 0 is only its i = j part.

B4. The tie is held only by the dial's residue (3.3 "The tie that holds"; 0.3 "which the act holds").
- On p_gauge's start over 60 rounds the tie never breaks at D = 18 or 22 (D = 2 mod 4). At D = 16, 20 and 24 it
  breaks at round 1, in 60 of 60 rounds for both seeds, with teeth on the edge -D between 2,114 and 3,291 times. So
  the text's OPEN case comes out negative; in the engine D = W(a) + W(a+) is not fixed.
- For the ten-gear candidate the tie does not matter (S symmetric by construction); it hits the 16-gear alternative
  and 0.3's appeal to 3.3.
- Fix: "kept on D = 2 mod 4 with constant teeth"; do not support 0.3 with it.

## MINOR

- M1. Line 25 "with no law and no gear added" against line 33 "a law change": say no gear added, the reading law
  changed (W and the grips quadratic; the term-5 push through the chain rule).
- M2. p_slots' large start is out of (1, 3) at round 0 at 20 of 27 sites. The claim is true (from diag(4,-4,-4,-4) a
  stride +1 on G11 gives (2, 2) at round 5, a stride -1 on G00 gives (0, 4); from an all-(1, 3) start only 270 of 5,400
  rounds stay (1, 3) over 200 rounds); replace the start.
- M3. 0.2 and 0.3 are measured on different starts; on the same start (base 4, amp 6) the S reading gives (1, 3) at
  1,101 of 1,101 invertible rounds, with W <= 0 at 964 of them.
- M4. The "boost" p -> p + Re(p v) v, v = 1 + i + j + k, is a Lorentz reflection (matrix
  [[2,-1,-1,-1],[1,0,-1,-1],[1,-1,0,-1],[1,-1,-1,0]], M^T C M = C, det -1, M M = I, M00 = 2); composed with z -> -z a
  proper map with gamma = 2; no whole boost has gamma < 2. Lawful as a derivation; as code a typed group element, which
  the owner's ruling forbids.
- M5. The "48" in 1.3 are the lifts w and -w of the 24, not O_h; parity derived, not measured (the reader: parity keeps
  the tie in 300 of 300).
- M6. The 12,005 in 2.1 covers diagonal F only and checks an identity; the general identity holds for every S:
  adj(S C S) = -adj(S) C adj(S).
- M7. "The cone can close for a round at det S = 0" is wrong for the displacement cone: at S = diag(3, 1, 1, 0), which
  the act reaches, Re(Z Z) = 0 for V = (1, 100, 0, 0), so any speed in the plane z = 0 counts as on the cone while the
  slots read c = 1/3 there (m_check3.txt). The order in 5.1 needs a rule at singular rounds.
- M8. sqrt(-g) = |det E| needs a sign (an if or a carry construction), and det E flips sign by jumps (1.4).
- M9. The tie survives the 24 only if the quaternion index turns with the legs (legs alone keep it 600 of 14,400;
  legs plus conjugation 14,400 of 14,400): a choice, to be stated.

## SOUND

- All four frozen probes reproduce exactly; the run back exact, 0 misses of 1,296 in all five runs.
- Re(e_m e_n) = (E C E^T)_mn, and S C S = E C E^T with E = S C. (1, 3) at every invertible S, 44,868 of 44,868 over
  3^10; never a second positive square, singular or not.
- Item 3: conjugation (carry remainders 0, g unchanged in every case); legs turned plus conjugation give R g R^T (0
  misses); a p b keeps Re(p q) up to a positive scale iff b a is real (6,400 of 6,400 pairs over a, b in
  {-1, 0, 1}^4; the scale (b a)^2, exactly 1 iff b a = +-1); one side keeps it only for real w (33,000 of 33,000
  non-real cases changed g).
- The tie kept by the 24 with conjugation (14,400 of 14,400), by parity (300 of 300), by the mirror T E T (300 of
  300). Section 4: S = diag(L, l, l, l) gives W = L^2 and grip = l^2. The plain slots do lose (1, 3) on the act's own
  steps (M2's exact strides).

## Item 4, the law

W = S00^2 - S01^2 - S02^2 - S03^2 is whole, with no root, no number beyond 0 and 1 (the signs from Hamilton's
i^2 = -1) and no table; it comes out of the state, so it meets the owner's ruling; but it is not a teeth count (B1). The
reflection in v is lawful as a derivation; in code it would be a typed group element aimed at integrality
(Re(v v) = -2 makes the map whole). The probes aim at no angle and no root.

## DERIVED / MEASURED / OVERCLAIMED

- DERIVED and correct: Sylvester as applied, Re(p q) = p^T C q, the a p b theorem, the parities in 1.1, section 4, the
  octahedron in 5.3.
- MEASURED and reproduced: 1.2, 1.3, 1.4, 2.3, p_slots and p_gauge2. MEASURED but cannot fail: the signature counts in
  0.3 and 2.2, the 12,005 in 2.1.
- OVERCLAIMED: "HELD" and "no law added" (0.3); "the act holds" the tie (3.3, dial residue only); "transversal" (3.3,
  false at S = I); "the cone can close" (0.3); "boost" for a reflection (3.1).

## Questions for the Boss

1. Should W >= 1 (with 3 grip <= W) be a law of the candidate or a window of the run? Without it the candidate cannot
   run from its own start.
2. Is the flat S = I, where the gauge is degenerate, or S = C?
3. Does the owner accept a quadratic reading law as "no added gear"?

## Solution24

Record the quadratic re-reading as the Lorentzian form of W = L^2. It gives (1, 3) by construction of the reading; its
folds are at det S = 0 and at lam_i + lam_j = 0, and the act crosses both freely. Do not record the cone as held by the
act. Still open: det S, W > 0, 3 grip <= W, and the tie, which holds only on the dial residue.
