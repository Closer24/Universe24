# Reading log (hostile mathematician, tg_math)

## Read so far
- TIMEGEAR.md, notes_01_derivation.md, notes_02_forward_backward.md, tg_lib.py.

## Claims to check (as stated)
U. Uniqueness: with D_in = W(b)+W(a), D_out = W(a)+W(a+), (T) tiling at fixed D_in and (R) run back
   force C(q) = 2 q D_out(q) - q^2 - v^2 + c. Law: D_in^2 + D_out^2 = 8 W(a)^2 + 4 push + s - s+.
N. No carry meets one cone + bijection + nothing written + no price.

## First suspicions (to verify)
1. In the derivation of (T): "C(q+1) - C(q) = D_out(q) + D_out(q+1)" assumes the cells for q and q+1 are
   adjacent with widths 2 D_out(q) and 2 D_out(q+1). Fine. But (R) as written: e(q, D_out(-v)) = e(-v, D_out(q)).
   The symmetry argument "g(q,y) = -q^2 + k(y), symmetry makes k(y) = -y^2 + c" needs g defined on a product set
   where both q and -v range over ALL integers independently, and D_in = D_out(-v) must be the same FUNCTION.
   D_out(y) = W(a) + W(a + y) depends on a (the pivot); fine since a fixed per round.
   But: W(x) = rest + x is linear, so D_out(y) = 2 W(a) + y. Then D_out(-v) = 2W(a) - v = W(a) + W(b). OK.
2. The law needs s+ in [-D_out, D_out - 1] with D_out = u; cells [u(u-1), u(u+1)-1] have width 2u. OK, tile
   the non-negative integers from u=1: [0,1], [2,5], [6,11], ... Yes: u(u+1)-1 +1 = u(u+1) = (u+1)u. Tiles N>=0.
   BUT: M can be NEGATIVE? M = 8W(a)^2 - D_in^2 + s + 4 push. With D_in ~ 2W(a), 8W^2 - 4W^2 = 4W^2 > 0, so M>0
   typically; but the formula uses u >= 1 requires M >= 0. For u = 0 cell is [0, -1] = empty. So M < 0 has no cell:
   NOT a bijection on all states. Need to check what the probe does when M < 0 (promise?).
3. "s - s+" sign: the law D_in^2 + D_out^2 = 8W(a)^2 + 4 push + s - s+. Check: N = 2(D_in v + 2 push) + s where
   v = a - b. D_in = 2W(a) - v (since W(b) = W(a) - v). So N = 2((2W(a) - v) v + 2 push) + s = 4W(a)v - 2v^2 + 4push + s.
   Centre C(q) = 2 q D_out(q) - q^2 - v^2 with D_out(q) = 2W(a) + q: C(q) = 4W(a) q + 2q^2 - q^2 - v^2 = 4W(a)q + q^2 - v^2.
   N = C(q) + s+ : 4W(a)v - 2v^2 + 4push + s = 4W(a) q + q^2 - v^2 + s+
   => 4W(a)(q - v) + q^2 + v^2 = 4 push + s - s+. Matches text's physics line.
   Now D_in^2 + D_out^2 = (2W-v)^2 + (2W+q)^2 = 8W^2 - 4Wv + v^2 + 4Wq + q^2 = 8W^2 + 4W(q-v) + q^2 + v^2. So the law
   reads D_in^2 + D_out^2 = 8W^2 + 4push + s - s+. OK consistent.
   M = 8W^2 - D_in^2 + s + 4push = D_out^2 - s+ ... wait: D_in^2 + D_out^2 - 8W^2 - 4push - s = -s+, so
   D_out^2 - s+ = 8W^2 - D_in^2 + 4push + s = M. So M = u^2 - s+ with s+ in [-u, u-1] => M in [u^2 - u + 1, u^2 + u].
   TEXT SAYS cells [u(u-1), u(u+1)-1] and s+ = M - u^2. That gives M in [u^2-u, u^2+u-1], s+ = M - u^2 in [-u, u-1]. OK
   so the text uses s+ = M - u^2, i.e. M = u^2 + s+, meaning D_in^2 + D_out^2 = 8W^2 + 4push + s + s+ ??? Let me recheck.
   M := 8W^2 - D_in^2 + s + 4 push. Text: s+ = M - u^2 => M = u^2 + s+ => 8W^2 - D_in^2 + s + 4push = D_out^2 + s+
   => D_in^2 + D_out^2 = 8W^2 + 4push + s - s+. OK consistent. Good. So s+ = M - u^2, and the centre formula gives
   N = C(q) + s+... let me recheck: N = 4Wv - 2v^2 + 4push + s and C(q) = 4Wq + q^2 - v^2: N - C(q) = 4W(v-q) - v^2 - q^2 + 4push + s.
   And M - u^2 = 8W^2 - (2W-v)^2 + s + 4push - (2W+q)^2 = 8W^2 - 4W^2 + 4Wv - v^2 + s + 4push - 4W^2 - 4Wq - q^2
   = 4W(v - q) - v^2 - q^2 + s + 4push. Same. Good, consistent.
4. KEY: is the uniqueness hypothesis "D_out depends on q only through W(a)+W(a+q)" plus "(T) at fixed v" plus "(R)"
   really forcing k(y) = -y^2 + c? g(q,y) = -q^2 + k(y) and g symmetric: g(q,y) = g(y,q) => -q^2 + k(y) = -y^2 + k(q)
   => k(y) + y^2 = k(q) + q^2 = const. Yes forced, IF symmetry holds for all pairs (q, y) in Z^2. The text says
   "q and v are independent (any push gives any q at any v)". Need to check: is the domain really all of Z^2? Push is
   bounded by the state; but as a law for all states, fine.
   HOWEVER: the (R) condition as stated, C(q) - 2 q D_out(q) = C(-v) - 2(-v) D_out(-v), where does it come from?
   Need to re-derive the run-back identity myself. The notes_01 derivation: "The run back identity, with D_in = D_out(-v)".
   Let me derive: forward: N = 2(D_in v + 2P) + s = C(q) + s+, with s+ in [-D_out(q), D_out(q)-1].
   Backward: state (a+, a, -1-s+), v' = a - a+ = -q, D_in' = W(a+) + W(a) = D_out(q) (same number). Push P' = push(a) = P
   (the pivot's push). N' = 2(D_in' v' + 2P) + (-1 - s+) = 2(-q D_out(q) + 2P) - 1 - s+.
   Need: N' splits into (q' = -v, s+' = -1 - s) with D_out'(q') = W(a) + W(a - v) = W(a) + W(b) = D_in = D_out(-v).
   So N' = C'(-v) + (-1 - s) where C' is the centre function in the backward round. Centres are the same function of
   (q, pivot) in both directions if the act is the same. But C depends on v too (C(q) = 2qD_out(q) - q^2 - v^2 + c)!
   In backward round v' = -q, so C'(-v) = 2(-v) D_out(-v) - v^2 - q^2 + c. 
   Check: N' = -2q D_out(q) + 4P - 1 - s+. And s+ = N - C(q) = 4Wv - 2v^2 + 4P + s - C(q).
   N' = -2qD_out(q) + 4P - 1 - 4Wv + 2v^2 - 4P - s + C(q) = -2qD_out(q) - 1 - 4Wv + 2v^2 - s + C(q).
   Want N' = C'(-v) - 1 - s = -2v D_out(-v) - v^2 - q^2 + c - 1 - s = -2v(2W - v) - v^2 - q^2 + c - 1 - s
   = -4Wv + 2v^2 - v^2 - q^2 + c - 1 - s = -4Wv + v^2 - q^2 + c - 1 - s.
   And with C(q) = 2q(2W+q) - q^2 - v^2 + c = 4Wq + q^2 - v^2 + c: N' = -2q(2W+q) - 1 - 4Wv + 2v^2 - s + 4Wq + q^2 - v^2 + c
   = -4Wq - 2q^2 - 1 - 4Wv + 2v^2 - s + 4Wq + q^2 - v^2 + c = -q^2 - 1 - 4Wv + v^2 - s + c. MATCHES. Good.
   Also need -1 - s in [-D_out'(-v), D_out'(-v) - 1] = [-D_in, D_in - 1]: s in [-D_in, D_in-1] => -1-s in [-D_in, D_in-1]. OK.
   So the run back is exact given the forward split put s+ in the right range. Good; the run back is correct.
5. WHERE the uniqueness may fail: the text assumes the centre function depends on (q, v, a) only; general law could
   depend on s too, or on push... Also the text assumes the cells for consecutive q are adjacent (T). Does tiling need
   consecutive q adjacent in order? Cells could be arranged in a different order (e.g. q -> permuted). Hmm, but
   monotonic in q is natural; the text says "(T) the cells tile the integers at fixed D_in: C(q+1) - C(q) = D_out(q) + D_out(q+1)".
   That's a hypothesis (order-preserving tiling), not derived. A tiling with cells in another order could exist?
   Cells of widths 2 D_out(q) = 4W + 2q for q in Z... widths grow with q; negative q: for q <= -2W widths become <= 0 -> no cell.
   So the domain of q is q > -2W (D_out >= 1 i.e. q >= 1 - 2W). The cells tile [some lower bound, infinity)? Sum of widths
   from q = 1-2W upward: the half-line. So the tiling covers a half-line: N must be >= lower bound. That's the M >= 0 condition.
   Check bijection: for N below the lower bound, NO cell => not a bijection on all states! The text says "the lawful states (W(b) >= 1)".
   Hmm, with u = D_out >= 1 and M in [u(u-1), u(u+1)-1] >= 0. M < 0 happens when 8W^2 - D_in^2 + s + 4push < 0,
   i.e. (2W - v)^2 > 8W^2 + s + 4 push, i.e. |2W - v| > ~2.83 W: v < -0.83 W or v > 4.83 W. With D_in = 2W - v >= 1 needed,
   so v <= 2W - 1. v < -0.83W: a fall of the clock faster than 0.83 W per round: W(b) > 1.83 W(a). A falling clock
   losing nearly half its count in one round. Hmm, "the falling clock" the Boss asked about. Under the engine, is such
   a state lawful? W(b) >= 1, W(a) >= 1. e.g., W(b) = 10, W(a) = 5: v = -5, D_in = 15, 8*25 = 200 - 225 = -25 + s + 4push.
   M < 0 unless s + 4 push >= 25. So the state (W(b)=10, W(a)=5, s=0, push=0) has NO image: the forward map is not total.
   That is a counterexample to "bijection on the state" unless such states are excluded by a promise. Measure it.
6. Second: injectivity. Given N, (u, s+) determined uniquely from M (cells tile) PROVIDED we know D_in, s... wait the
   forward map is (b, a, s) -> (a, a+, s+). Given the output (a, a+, s+) can we recover (b, s)? Output gives u = W(a)+W(a+),
   s+. M = u^2 + s+. M = 8W^2 - D_in^2 + s + 4push(a). So D_in^2 - s = 8W^2 + 4push - M =: K known. D_in = 2W - v, s in
   [-D_in, D_in - 1]. (2W-v)^2 - s = K. Different (v, s) pairs: D^2 - s with s in [-D, D-1] gives range [D^2 - D + 1, D^2 + D] 
   = [(D-1)D + 1, D(D+1)]. For D and D+1: [D(D-1)+1, D(D+1)] and [D(D+1)+1, (D+1)(D+2)]. Disjoint and adjacent! Tiles
   integers >= 1 (D=1: [1, 2]). So injective. Good  -  so the forward map is injective, and the issue is only totality
   (M >= 0) and whether the output's s+ range makes the back map total too.
7. Third concern: s+ = M - u^2 in [-u, u-1]; but ALSO the "mirror" -1 - s+ must be in the same range: yes symmetric.
8. The no-carry theorem: hypotheses: 'two slots + one carry' and 'register' forms. The text's Theorem 1 says in dial
   must be a function of the now slot alone or a register. Claim "the forward map collides" when D_in depends on b.
   But wait  -  the symmetric form itself HAS D_in = W(b) + W(a) depending on b! And it is injective (shown above) because
   the centre includes -v^2 which compensates. So Theorem 1's "an in dial that moves with its before slot makes blocks
   of unequal width so the forward map collides" is only true when the centre is 2 q D_out (the standard carry)  -  i.e.
   Theorem 1's hypothesis is "one carry with the standard centre". The symmetric form escapes by using a non-standard
   centre. So the question "is there an integer form with no root" = "is there a centre C(q) with (T) and (R) whose
   inverse (finding q from N) is a carry (one division)". The text's uniqueness says C is forced => q = nearest-integer sqrt.
   But: uniqueness was derived under D_out(q) = W(a) + W(a+q). Other choices of D_out: e.g. D_out = 2 W(a) (the order's
   out dial) with D_in = W(b)+W(a)? Then (C1) must hold across rounds: D_out(S_t) = D_in(S_{t+1}): 2W(a) vs W(a)+W(a+).
   Fails unless q = 0. Hmm. But (C1) was derived assuming the standard centre! With a general centre, (C1) is not needed
   per se; what is needed is the full injectivity + run-back. Let me think again more generally.

GENERAL SETTING: state (b, a, s). Law: given (b, a, s) produce (a, a+, s+). Requirements:
   (i) bijection on lawful states (define lawful!);
   (ii) run back: M tick M tick = id, where M(b,a,s) = (a, b, -1-s);
   (iii) one cone: the 00 wave's speed equal to light's (dial 2W).
   (iv) nothing written; (v) integers only with one carry; (vi) "no price": the physics is nature's?? (vague).
   The text's (vi)/no price is judged by "the clock's own course"  -  that's a physics choice, not a theorem.

I should test: the 'frozen hand' and |v|=1 quirk: in the symmetric form at |v| = 1, "the quotient never falls, W linear".
   That's physically wrong vs nature (sqrt(W) v kept means v should decay). So the symmetric form ALSO pays a price at
   |v| = 1: it does not follow nature. The text admits this as "one quirk". With v0 = 1 and rest 10,000 the clock runs
   linearly for ever. That is a price. Hmm, is it "a second cone"? No. But it's a mis-physics at the smallest velocity,
   which for the real clock (v tiny vs W) is THE regime! At the real calibre the clock's own velocity in counts per round is
   ... W ~ 10^23 and the velocity is small in counts per round? Depends. If |v| <= 1 in units typical, then the symmetric
   form's physics = v kept = the act as built's. So "nature's form" claim is only for |v| >= 2. That is a significant
   hole: the sub-count regime is exactly where the engine lives (teeth carry the fraction).

Let me now read the probes.
