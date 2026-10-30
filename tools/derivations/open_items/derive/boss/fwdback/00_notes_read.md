# Notes 00: what the drafts say (the Boss's deriver on "time forward and backward", 2026-10-30)

## The act as built (carry.py, ARCHITECTURE term table)
q, r+ = carry(W (a - b) + s (F + T_k q_d), W, r); a+ = a + q; b+ = a. carry(n, d, r): n + r = q d + r', 0 <= r' < d.
flip(r, w) = w - 1 - r. lit(x) by one carry. W = rest + 00 slot (linear, decision 41).

## The edge (EDGE2/EDGE3)
tooth s in [-D, D-1], D = W(b) + W(a); N = 2 (D_in (a-b) + 2 push) + s split half-open at 2 D_out, D_out = W(a) + W(a+).
Mirror (b, a, -1 - s). Keeps P = 2 D v + s to the bit. Price: d_t(W d_t a) = F, keeps W v (nature keeps sqrt(W) v),
A ~ W^(-1/4), parametric pump under swing at half a beat.

## The root dial (ROOT.md)
W = L^2, L = L_rest + c00. D = L(b) + L(a). push q_F = odd-round(F / L(now)) remainder DROPPED. N = 2 (D_in v + 2 q_F) + s
split at 2 D_out. Nature's L d_t (L d_t a) = F. Prices: floor on force (L/2), board momentum drift, den = 6 k^2 typed,
signed rounding, quaternion renaming.

## The physicist's theorem (rd_phys item 1)
"no bounded-state whole-number form of nature's equation exists on a moving L: the push's share 4 F / L(now) has a
remainder at the dial L(now) that no bijection carries to L(next)". Kept push tooth at the pivot dial 2 L(now) flipped
by (iii): 24 ok, run back fails on falling clock (2 of 40), and A/A0 939 (not exact physics).
ROOT.md: "the push's quotient enters the momentum with the same sign in both time directions (the pivot's push), so the
mirrored round must compute the same q_F from pivot data alone and a tooth flipped in the pivot's dial; a tooth re-split
between the two edge dials changes the quotient with the direction".

HYPOTHESES of the theorem as I read them:
 H1. the state is bounded: two slots (b, a) + one tooth s per gear (+ drive tooth), nothing more;
 H2. the push is divided at ONE dial, the pivot's L(now), in both time directions;
 H3. the equation is nature's: L d_t (L d_t a) = F (weight sqrt(W) on velocity, push divided by L once);
 H4. the run back is the same act on the mirrored (b, a) with the tooth flipped in ITS dial;
 H5. W = L^2 with L whole (den = 6 k^2).

## c4_math item 1 (the lesson of time forward and backward)
Term 11's click tooth runs back as the same act only when it carries X(S) + X(S+): the state read and the state
produced together. "of the increments linear in X only X(S) + X(S+) is odd across the swap" (b,a)->(a,b).
LESSON: a quantity entering the act must be read SYMMETRICALLY in the two slots (or in read+produced state) for the
mirror to invert it with the same act.

## timegear (another deriver; the 00 row's own law)
Carried dial: state (b, a, s, D), D_out = 4 W(a) - D, an involution; E_t = departure from edge dial obeys alternating
sum of second differences. Their theorem: in a two-slot state, no dial of the out edge may depend on the row's own
next count. Do not duplicate.

## The owner's lead
"No price. Solve it with time forward and backward." "The return in time is simply more gears, and there are differences
between them." Reading: the backward act is realised by MORE GEARS (extra registers/gears that run backward beside the
forward ones), and the physics is read from the differences between the forward and the backward gears.
