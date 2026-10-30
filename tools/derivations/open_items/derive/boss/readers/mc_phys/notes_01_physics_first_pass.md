# Notes 01: first physics pass (before any probe)

## The lapse the engine already fixes
- Static: W d_t^2 a = grip Lap a - D a. Light c^2 = grip/W, hairspring omega^2 = D/W.
- Both go as W^(-1/2), so the clock rate is N = sqrt(rest/W) (law: N^2 = rest/W). W <-> rest/N^2 = -rest/g_00.
- Proper time per round: dtau = N dt. A round is coordinate time t (D7: a round is no clock's time).

## What nature does when W moves in time at a site
- A scalar field in ds^2 = -N^2 dt^2 + dx^2 (lapse only, flat slices, no shift):
    d_t ( (1/N) d_t phi ) = div ( N grad phi ) - N m^2 phi      (exact, any N(x,t))
- With 1/N = sqrt(W/rest):  sqrt(W) d_t ( sqrt(W) d_t a ) = F,  i.e.
    W d_t v + (1/2) (d_t W) v = F
- Compare:
    as built / half-tooth :  W d_t v              = F   (no (d_t W) v term)
    edge                  :  W d_t v + (d_t W) v  = F   (the whole term)
    nature                :  W d_t v + (1/2)(d_t W) v = F  (half of it)
- Free zero mode on a torus (push sums to 0), uniform W(t):
    as built/half-tooth: v const            -> v/N = proper velocity ~ W^(+1/2)
    edge               : W v const          -> proper velocity ~ W^(-1/2)
    nature             : sqrt(W) v const    -> proper velocity const (a uniform lapse is a change of time coordinate; nothing a clock can read changes)
- Hairspring amplitude A under a slow uniform change of W (adiabatic invariant E/omega):
    as built : A ~ W^(+1/4);  edge : A ~ W^(-1/4);  nature : A const.
- So the edge's "W v is what the clock keeps ... nature's" is a claim against nature by a factor sqrt(W_out/W_in) in v
  and W^(1/4) in a hairspring's amplitude; the act as built errs by the same factor the other way.
- Static wells: all three forms are the same act (W does not move at a site), so the static redshift of light and of a
  climbing particle cannot tell them apart. Only a clock moving in time at a site does: term 9's notch, term 5's push,
  a passing mass.

## Owner's rule
- "energy and momentum are conserved in the clicks, in the clicks' spacetime, not as board invariants."
- The edge's P = SUM (2 D v + s) is a board invariant. In the clicks' spacetime the proper momentum of a free gear is
  m v / N = m v sqrt(W/rest); under the edge it falls as W^(-1/2). Under nature it is kept. The edge conserves the
  wrong thing by exactly sqrt(W).

## Cut vs order (preliminary)
- Cut: 00 row's teeth = rest -> c_00^2 = grip/rest while light's c^2 = grip/W: in a well (W > rest) the 00 wave outruns
  light by sqrt(W/rest), in proper units too (local clocks slow by the same N). A signal outside light's cone (D8).
  GW170817 bounds the tensor modes at ~1e-15; the 00 mode is a scalar, but any metric disturbance that outruns light in
  the galactic well (Phi ~ 1e-6) is excluded by the same logic (the cone is one).
- Order: 00 row reads itself, split first on its own now dial (4 W(a)); every other row uses D_out = W(a) + W(a+_00).
  c_00 = c (good). But the 00 row's own tooth is kept at 4W(a) and read at 4W(a+): the as-built defect kept for the
  metric's own gear (its velocity not redshifted, one-signed drift on an A1 row), and on a falling clock a whole count
  leaves (the "00 click"), booked outside the Node-clock for the rewind: not a bijection of the act alone.
- Neither is GR: GR has no propagating 00 mode at all (the lapse is a constraint, not a wave).

## Half-tooth (CLICK25 s.1)
- Keeps W d_t v = F (no redshift; proper velocity grows as sqrt W). Does not run on a falling clock. Term 9's notch has
  the clock falling half of every beat: the half-tooth cannot run the notch at all.

## To measure (whole numbers, real act)
1. Rerun the three drafts' probes as given.
2. Edge, free row, uniform rising W: S vs D; S^2 * W (nature's invariant) falls ~ 1/W under the edge.
3. Edge, hairspring on a rising clock: amplitude envelope; A^4 * W ~ const under the edge (nature: A const).
4. Cut: the 00 wave's speed against light's on the real act (a 00 pulse vs a t1 pulse in a uniform well).
5. Order: count the 00 clicks on a falling clock; the 00 row's drift.
6. Half-tooth on a falling clock: confirm the promise breaks.
