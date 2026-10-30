# Paper re-derivation of TIMEGEAR's two theorems (tg_math, hostile mathematician)

Notation: pivot a, before b, v = a - b, W(x) = rest + x (linear), D_in = W(b) + W(a) = 2W - v (W := W(a)),
D_out = W(a) + W(a+) = 2W + q, half-open tooth s in [-D_in, D_in - 1], s+ in [-D_out, D_out - 1].
N = 2 (D_in v + 2P) + s = 4Wv - 2v^2 + 4P + s.

## 1. The structure of every reversible two-slot law (my general form)
Mirror M(b, a, s) = (a, b, -1 - s). Run back exact <=> (M tick)^2 = id <=> I := M tick is an involution.
I keeps the pivot a and maps the pair (b, s) -> (a+, -1 - s+). So EVERY reversible law is
   tick = M o phi^-1 o R o phi
with phi_a any bijection from pairs (x, s) (s in the tooth range of the edge (x, a)) onto a range of Z and R an
involution of Z (push-dependent). The text's choice: phi_a(x, s) = 4W^2 - D(x)^2 + s (cells ordered by the other
slot x, widths 2 D(x)), R(X) = -1 - 4P - X. Then phi(a+, -1 - s+) = -1 - 4P - phi(b, s) gives
   D_in^2 + D_out^2 = 8W^2 + 4P + s - s+.            (checked: identical to the text's law)
Run back checked by hand: the backward round at pivot a, velocity -q, push P(a) (same pivot) gives N' = -1 - 4Wv + v^2
- q^2 - s + c and splits at D_out'(-v) = D_in into (q' = -v, s' = -1 - s). EXACT. (notes_02's (R) identity is right.)

## 2. Uniqueness (Theorem 2 / notes_02) -- right under FOUR hypotheses the text does not list as hypotheses
 (H1) the tooth's range is [-D, D - 1] with D = W(x) + W(y), the edge's own dial (both ends' weights);
 (H2) the round has the shape N = C(q, v, a) + s+ (the push enters N whole; C may depend on q, v, a, not on s);
 (H3) the cells are laid in the ORDER of q (monotone tiling), adjacent: C(q+1) - C(q) = D_out(q) + D_out(q+1);
 (H4) W is linear in the count (D_out(q+1) - D_out(q) = 1); the text uses this silently in "gap (2q+1) dD".
Under (H1)-(H4): e(q, v) := C - 2 q D_out(q) obeys e(q+1, v) - e(q, v) = -(2q+1), so e = -q^2 + k(v); the run back
needs e(q, v) = e(-v, -q), so k(v) + v^2 = const: C = 2 q D_out - q^2 - v^2 + c. FORCED. I agree.
General dial h(y) := D'(a, a + y) (any symmetric D'): the law is G(q) + G(-v) = 4P + s - s+ - c with
G(q+1) - G(q) = h(q) + h(q+1): G is the cumulative sum of the cell widths. A carry inverts G only if h is constant
(the cut). One cone forces h(0) = 2W(a); symmetry D'(x, y) = D'(y, x) with D'(x, x) = 2W(x) forbids h constant.
So: within (H1)-(H3), NO single carry; the quotient is the inverse of a cumulative sum (quadratic at (H4): a root).
With 2 min(W(x), W(y)) or 2 max: linear on one side of q = 0 and quadratic on the other: the mirror swaps the sides,
so the root reappears in the backward round. No escape by the dial function.

## 3. Where the text's statements are wrong or loose (paper)
 (a) "the quotient is the integer nearest sqrt(M)" is FALSE at M = u(u+1): the cell [u(u-1), u(u+1)-1] gives u+1
     there while the nearest integer to sqrt(M) is u ((2u+1)^2 = 4M + 1 > 4M). The cells are right (the only ones
     whose s+ range [-u, u-1] is mirror-symmetric); the WORDS of the law line are wrong. u = nearest integer to
     sqrt(M + 1/4), the tie at M = u(u+1) taken upward (the half-open convention).
 (b) Theorem 1 as worded ("an in dial that moves with its before slot ... so the forward map collides") is refuted
     by the text's own Theorem 2: the symmetric form's in dial moves with the before slot and its forward map is
     injective. Theorem 1 holds only for cells of ONE length (the standard centre 2 q D_out). State the hypothesis.
 (c) "Any other centre ... keeps the forward bijection and loses the run back (probe_tg1: 95 misses of 176)":
     probe_tg1 itself prints 36 collisions and 70 no-split for that centre. It does NOT keep the forward bijection.
 (d) "a bijection on the state": the forward map is injective where defined but NOT total: no image where
     W(a+) = u - W(a) < 1, i.e. M < W(W+1), i.e. roughly v < -0.646 W (a clock losing 65 percent of its weight in
     one round) -- 96 of 300 states at rest 6 (the text's own probe_tg7 A). The image set is not the domain either
     (a state's image need not have an image). Partial injection with exact inverse; say so. Same for every W-form.
 (e) The theorem is "forced" only within (H1)-(H4); the general form in section 1 shows the freedom is exactly
     phi and R; (H3) (monotone order) is physics (velocities ordered), not algebra. Name it.

## 4. Inverting the quadratic WITHOUT a root: one carry at the carried estimate plus one sign-carry
c := 4W(a) - D_in = 2W(a) + v (the carried dial's estimate, from the two slots); R := M - c^2 = 4P - 2v^2 + s.
u = c + k with k the cell of R among [k(2c + k - 1) - c, k(2c + k + 1) + c - 1] (the text's own line).
Half-open carry: k0, r0 = split(R, 2c) (R = 2c k0 + r0, r0 in [-c, c-1]). Then k0 = k + floor((k^2 + s+ + c)/(2c))
with k^2 + s+ + c in [k^2 - k, k^2 + k + 2c - 1] (s+ in [-u, u-1]). The floor is 0 or 1 for EVERY s+ iff
k^2 + k + 2c - 1 < 4c iff k(k+1) <= 2c; then k = k0 where R >= low(k0) and k = k0 - 1 where R < low(k0),
low(k0) := k0(2c + k0 - 1) - c. The test "R < low" is one carry: neg(d) = -(d // (d^2 + 1)) (1 iff d < 0; the
same formula for every integer, as lit() in tensor24.algebra.carry). So within the PROMISE k(k+1) <= 2c (the
velocity's change in one round, k = q - v, against the dial 2c = 4W(a) + 2v) the root form's act is two Rule3
carries and products; outside it the one-step rule is wrong (necessary: at s+ = u - 1 the floor is >= 2).
The runner can verify u(u-1) <= M < u(u+1) with two products and refuse the state otherwise.
To be measured in probe tgm1 (exhaustive by construction: pick (c, k, s+), no search anywhere).

## 5. The |v| <= 1 freeze (paper)
At v = 1: M = 4W^2 + 4W - 1 + s; the cell of u = 2W + 1 is s in [-2W + 1, 2W + 2], which CONTAINS the whole tooth
range [-(2W - 1), 2W - 2]: q = 1 for every tooth, s+ = s - 2. The tooth's distance from its lower bound,
s + 2W - 1, is invariant: it never overflows. A rising clock at one count a round NEVER slows (v kept, W linear).
At v = 0: q = 0 for every tooth (frozen, the text says so). At v = -1: q = -1 for all but the 4 lowest teeth, which
give q <= -2 (the fall quickens, as nature's sqrt(W) v would). At |v| >= 2 the tooth drifts 2v^2 a round against
the dial's 2|v|: overflows happen and the quotient moves.
Consequence: every free rising clock decelerates only down to v = 1 and then runs linearly for ever; nature
(sqrt(W) v kept) has v -> 0. The text's probe_tg9 C shows it (2115 permille off nature at round 30,000 from v0 = 1);
the text calls it "one quirk". By the text's own standard (the carried dial's 612 permille at v0 = 100 is "a price")
this is a price, at the one velocity scale (counts a round, order 1) where a time gear lives.
To be measured in probe tgm2 from v0 = 2, 3, 5, 10, 30 (long runs).

## 6. CORRECTION to section 4's weighing (after the first board run of tgm3)
The one-step rule is exact iff k (k + 1) <= 2 c, i.e. |k| below about 2 sqrt(W(a)) COUNTS a round squared. In the
engine's units a notch of the 00 slot is a grip = den full_rate^2 = 1.5 x 10^22 counts, and W = 12 grips = 1.8 x 10^23
counts, so 2 sqrt(W) ~ 8.5 x 10^11 counts: 6 x 10^-11 of a notch. The text's board lays (the mode A = grip / 1000,
period ~22 rounds) accelerate the 00 count by ~10^17 counts a round squared: 10^5 times the bound; a swing of one
notch with term 9's period of 140 rounds, ~3 x 10^19: 10^7 times. So on the boards and at notch-scale motion the root
IS needed (the carry's estimate is off by ~k^2 / 2c ~ 10^10 cells; Newton closes it in 2 or 3 steps, a search). The
no-root regime k (k + 1) <= 2 c holds exactly where the text measures its physics on one gear (probe_tg7 B, probe_tg9:
k in {0, -1}, v <= 100 counts a round) -- there the "root" is Rule3's carry at 2 c plus one sign-carry. F1 is a
precision about WHEN the root is needed, not a change of the owner's question: MINOR, not BLOCKING. The symmetric
form's cone must be measured, with no root, at amplitudes where the promise holds (A <= grip / 10^9 on the line of 6).
