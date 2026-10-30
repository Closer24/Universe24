# Analysis before my own probes (hostile mathematician), 2026-10-30

## A. Algebra of the edge's split (centre 0, tie taken even) -- checked by hand
- m = 2D; n + D = q0 m + r0; s0 = r0 - D in [-D, D). Tie r0 = 0: q = q0 - odd(q0), s = s0 + odd(q0) m.
  At a tie with q0 odd: s = -D + 2D = +D, q = q0 - 1 (even). With q0 even: s = -D, q = q0 (even).
  So s in [-D, D], |s| = D only at even q. Bijection: n = 2Dq + s; the tie integer n = 2Dq0 - D has two
  representations (q0, -D) and (q0 - 1, +D); the rule picks the even quotient. OK.
- Odd law split(-n) = -split(n): at a tie, -n + D = (1 - q0) m, q0' = 1 - q0 (opposite parity); the even one of
  {1 - q0, -q0} is -(the even one of {q0, q0 - 1}). OK, exact.
- ANY odd tie rule f(q0) in {first, second} needs f(1 - q0) = not f(q0); no such f is shift-invariant under
  q0 -> q0 + k for all k (take k = 1 - 2 q0). So the loss of shift covariance (probe section 7) is a theorem of
  the centre-0 convention, not a cost of the particular choice "even".
- The sign law of the plain carry carry(-n, m, m-1-r) = (-q, m-1-r') holds at every m (the law's (iii)).

## B. THE FINDING: the tie rule is unnecessary. The half-open convention (centre -1/2) is exact with ONE carry.
Define split_half(n, m): q0, r0 = carry(n + D, m, 0); s = r0 - D in [-D, D - 1]   (this is edge_lib.split_up!)
Flip on this dial: s -> -1 - s (an involution of [-D, D-1]; in floor coordinates it is the law's r -> m - 1 - r).
Laws:
  (1) bijection n <-> (q, s), trivially (one residue system), no ties, no lit().
  (2) negation law: split_half(-n - 1, m) = (-q, -1 - s)  [proof: -n - 1 + D = -(q0 m + r0) + m - 1 = -q0 m + (m-1-r0)].
  (3) shift covariance: split_half(n + m k) = (q + k, s) for EVERY k.
  (4) The 24: a flipped row has (-v, -push, -1 - s): N' = -N - 1, split at 2 D_out gives (-q, -1 - s+) = the flipped output. Exact at every D_in, D_out.
  (5) Run back: mirror (a, b, s) -> (b, a, -1 - s). From (a+, a, s+): N' = -2 D_out q + 4 push - 1 - s+ = -(2 D_in v + s) - 1,
      split at 2 D_in gives (-v, -1 - s) by (2); state (b, a, -1 - s); mirror -> (a, b, s). Exact, rising or falling.
  (6) Momentum: (2 D_out v+ + s+) - (2 D_in v + s) = 4 push, exact (same as centre 0).
  (7) Still clock: s = 4 r - D (the probe's "mutant, the cell's lower edge") gives the built act's a, b exactly
      (N + D = 4 (W v + push + r), floor at 4W = v + (push + r) div W); the flip -1 - s maps the cell of r
      ({4r - D, ..., 4r - D + 3}) onto the cell of W - 1 - r (offset k -> 3 - k): the built mirror cell for cell.
  (8) It IS the law's (i) (born at m div 2 = D, i.e. s = 0) and (iii) (r -> m - 1 - r) on the edge dial m = 2D, unchanged.
So the text's "the centring is load-bearing, not a convention" is half right: RE-CENTRING the tooth from D_in to
D_out is load-bearing; the centre at an INTEGER (0) with a tie rule is not needed. The probe's mutant "the tie taken
upward: 3 of 24" fails only because it was paired with the wrong mirror (s -> -s instead of s -> -1 - s).
TO MEASURE: edge act with split_up + mirror (b, a, -1 - s) on all lays: the 24, the run back, the books, shift covariance.

## C. The run back proof of EDGE.md (centre 0): correct given the promise and the cut (my derivation in 00_notes).
Structural reason: the input tooth's range is one residue system mod the dial that weights the input velocity
(2 D_in), so (v, s) -> N is injective; split at any dial >= 1 is a bijection. The half-tooth act weights v by
2 W(a) but the tooth was kept in [0, 2 W(b)): one residue system only when W(b) <= W(a). So the half-tooth act is
NON-INJECTIVE on a falling clock ((b, u) and (b + 1, u - 2 W(a)) collide), not merely "promise-broken".
Same for the act as built and for the order's 00 row (dial 4 W(a), tooth kept at 4 W(b)).

## D. The promise as stated is insufficient
"W >= 1 at both slots and |s| <= D_in" is read on the current state, but the round splits at 2 D_out, which needs
W(a) + W(a+) >= 1 -- a condition on the NEXT 00 count. Construct: W(a) = 3 (rest 6, a00 = -3), v_00 = -10:
W(a+) = -7, D_out = -4, split at a negative dial. The promise holds, the round is garbage. Fix: the promise must
include D_out >= 1 (computable before the round from the 00 row's standing split).

## E. Section 6's gap formula is off by one
"exactly (2q + 1)(D(q+1) - D(q)) integers each": the difference next-floor less this-ceiling is g = (2q+1) dD;
the integers MISSED are g - 1 (g >= 1), the integers SHARED are 1 - g (g <= 1). The probe's own 1560 = sum_{q=1}^{39} 2q
confirms the count 2q (= g - 1 with dD = 1), not 2q + 1 (which would give 1600). For q <= -1 the cells are not even
in order (2 D(q) q is non-monotone), so "overlap by exactly ..." is not what happens. The conclusion (no bijection) stands.

## F. EDGE.md's numbers are not probe_edge.txt's (the text says "every number below is theirs")
- "486 gears", "18 rows x 40 rounds", "19,926 gear-states": the probe has 324 gears, 12 rows, 13,284 gear-states.
- "P_40 - P_0 up to -12,941": the probe's are ~1e26 (grips of 1.5e22).
- "rising by 3 ... D 17 to 257": not in the probe (lays are rising 1, 1+1, 2; falling 1, 1+1, 3).
- "ties 10, 7, 13, ... of 486": the probe's standing lay [6, 5, 7, 3, ...] of 324.
- "the tie taken upward, 3": on the falling lay [24, 24, 24, 24, 24, 12, 12, 12, 6, 3, ...].
- Measured 4: "departs at 22 and 20 gears of 486": probe 14 and 11 of 324.
- Measured 5: "untick(tick s) = s in 10 of 12 rounds rising, and the 00 slot stalls at 13": probe 0 of 12, no stall.
- "S_40 - S_0 from -23 to -29 rising, +11 to +18 falling": probe -23..-28 and +11..+17.
These are from an earlier run on the other board (486 gears), not re-read after the move to the example universe.

## G. "acyclic" is implemented as "self-loop cut"
edge_lib.acyclic keeps first != target: it cuts self-reads only. Two square trains would give a 2-cycle 00_A <-> 00_B,
uncut; a depth-2 read chain needs a second provisional split. Measured and true only for one square train.

## H. The two conflicts
(1) Momentum form's time symmetry: CLICK25 says "W(before)(a - b) + push is not time-symmetric" -- true of Form 3
(one-slot weights W(b) in, W(a) out), false as a general statement: the edge weights each velocity by its own
edge's D (symmetric), and its run back is the same act. CLICK25's "the second-difference form ... is forced" is wrong.
(2) The key's parity: with the floor carry (tie upward in centred terms) the giver/taker books miss at even keys
once per key of area (CLICK25 right for its convention); with the centre-0 tie-even split, 0 misses at every key
(EDGE right for its convention) -- but then adding one whole winding at a tie clicks 0 or 2 times (no odd tie rule
is shift covariant, A above), so "one winding, one click" fails at the ties. Neither text says this.
Under the -1/2 convention (B): books need q(A) + q(-A - 1)... the natural pair is A and -A - 1 (a half-tooth apart),
not A and -A; with areas A and -A the books miss at the ties exactly as the floor does. So for the CLICK, the
negation-exact tie-even rule and shift covariance are in genuine tension; the key's parity is the floor's way out.

## I. Half-tooth vs edge: one tooth convention, two dial laws
Half-tooth: offset c = u - W(b) kept, re-expressed at 2 W(a), flip -1 - c; momentum weighted by W(a) both ends:
W d_t v = F (free gear keeps v). Edge: offset s kept, dial 2 D_in in and 2 D_out out: d_t (W d_t a) = F (free gear
keeps D v, velocities redshift). Different equations of motion; same tooth device. NOT one law.
