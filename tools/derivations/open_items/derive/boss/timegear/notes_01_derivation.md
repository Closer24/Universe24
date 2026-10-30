# Notes 01: the derivation before the probes (the Boss's deriver, 2026-10-30)

## The two conditions on a dial, read off the edge

State per gear (b, a, s): before, now, the tooth. The edge act: N = 2 (D_in (a - b) + 2 push(a)) + s, split at 2 D_out
into (q, s+), a+ = a + q. The mirror (b, a, -1 - s). Writing D_in(S) and D_out(S) for the two dials as functions of
the state S, the run back M(tick(M(S_(t+1)))) = S_t needs exactly:

  (C1) the tooth's home modulus is the velocity's weight: s_t was split at 2 D_out(S_(t-1)) and is weighted by
       2 D_in(S_t) in N, so (v, s_t) -> N is injective iff D_out(S_(t-1)) = D_in(S_t);
  (C2) the mirror swaps the roles: D_out(S_t) = D_in(M(S_(t+1))) and D_in(S_t) = D_out(M(S_(t+1))).

The edge meets both with D(edge) = W(one end) + W(other end): symmetric in the edge's ends, so the mirror cannot tell
the two readings apart; but the out dial then needs W(a+), the next count of the 00 slot.

## The fixed point is a theorem (the centre is forced)

Let the 00 row's out dial depend on its own next count, D_out(q) = W(a) + W(a + q), and let the split put the
quotient q's cell at any centre C(q): N = C(q) + s+, s+ in [-D_out(q), D_out(q) - 1]. The run back identity, with
D_in = W(b) + W(a) = D_out(-v) (the same function of the quotient, since the pivot a is the same both ways), reads

  C(q) - 2 q D_out(q) = C(-v) - 2 (-v) D_out(-v)   for every pair (q, v) that occurs.

q and v are independent (any push gives any q at any v), so e(q) = C(q) - 2 q D_out(q) is one constant: the centre is
2 q D_out(q) + e, and then the cells' gap is (2q + 1) (D_out(q + 1) - D_out(q)), zero for every q only if D_out does
not move with q. So: in a two-slot state, no dial of the out edge may depend on the row's own next count. (EDGE2 s.4
had the gaps; this shows no other centre escapes them.)

## What is left for the 00 row

Its out dial must be an explicit function of the current state. By (C1) and (C2):
 - the cut: D = 2 rest, constant. Meets (C1), (C2); fails the cone (the 00 row's teeth do not read the clock).
 - the order: D_in(b, a) = 2 W(a), D_out(b, a) = 2 W(a). Meets (C2) (the pivot's own teeth are mirror-symmetric);
   fails (C1): the tooth was split at 2 W(b) and is weighted by 2 W(a): collisions where W falls.
 - the lag: D_in(b, a) = 2 W(b), D_out(b, a) = 2 W(a). Meets (C1); fails (C2): the mirrored state reads the tooth
   at 2 W(a+).
 - option (a), other rows' two slots: D_out needs those rows' next counts, which need the 00 row's next count for
   their own out dial: a deadlock in one pass. The only way out, the read rows' teeth cut from the clock, puts
   those rows on their own cone (the cut's fault moved to another row).
 - option (b), one more register: carry the dial itself. The state (b, a, s, D), D the dial of the edge (b, a).
   D_in = D (C1 by construction: the tooth is stored with its own modulus). The out dial D_out = f(a, D) must be
   an explicit function; (C2) says the backward step, from (a+, a, -1 - s+, D_out) with the same pivot a, must give
   back D: f(a, f(a, D)) = D, an involution of the integers at each a. The affine involutions are D -> g(a) - D
   (the identity being the cut again, D constant). On a standing clock the dial must be the edge's 2 W, so
   g(a) = 4 W(a): D_out = 4 W(a) - D, the dial reflected in the now slot's teeth, the mirror's own shape w - 1 - r.

## What the carried dial is

E_t = D_t - (W(b_t) + W(a_t)), the departure from the edge's dial, obeys E_(t+1) = -E_t - (W(a_(t+1)) - 2 W(a_t)
+ W(b_t)): the alternating sum of the clock's second differences. On a standing or uniformly moving clock E = 0 at
every round: the carried dial IS the edge's dial, and the carried act is the edge act state for state, with no read
of any next count. Reversibility forbids damping (an involution has no contraction), so the deviation is not pulled
back; it is bounded by the clock's second differences as long as they do not alternate in sign every round (a
Nyquist drive of the 00 slot pumps it linearly: the hostile case to measure).

## The two forms to measure

 - the carried 00: the 00 row alone carries its dial; every other row on the edge, its out dial W(a) + W(a+) read
   from the 00 row's new count (the 00 row first, as the edge already has it);
 - the carried board: every gear carries its dial, D_out = 4 W(a) - D for every row alike: one pass, no row first,
   no cut, no next count read by anyone. Generic: one act for every gear.
Both with the loader's lay (every row reads the 00 slot, the 00 row included).

## The root dial beside

W = L^2, L the clock's count; the carried dial on the 00 row is ~ 2 L; the push at the pivot's root. Same algebra
(the involution is D -> 4 L(a) - D). On the example universe 6 den Gamma^2 is no square, so the root form stands on
one gear with the clock its own, not on the board (a law change, EDGE2 s.3).

## Sharpened after probe_tg1's first run (the lag and the tiling centre collide forward)

For the 00 gear the in dial itself may not depend on the before slot: with D_in = D_in(b) the blocks
2 D_in(v) v + [-D_in(v), D_in(v)) over the velocities v = a - b have widths that move with v, and the union of blocks
over v is no tiling (gap -(2v + 1) for D_in = w(a) + w(b); -(4v + 2) for 2 w(b)): the forward map is not injective
for every row whose own count is the clock, whatever the out dial. So the 00 row's in dial is a function of the now
slot alone, phi(a), or a register of the state. phi(a) alone fails (C1) across rounds (the home modulus was phi(b))
unless phi is constant: the cut. Hence: the cut, or a carried dial. The carried dial's update must be injective in D
at the pivot (forward) and an involution there (the run back): D -> g(a) - D; one cone on a standing clock fixes
g = 4 W(a). The carried dial is forced, not chosen.
