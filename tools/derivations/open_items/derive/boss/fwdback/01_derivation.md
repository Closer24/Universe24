# Notes 01: the derivation (the Boss's deriver on "time forward and backward", 2026-10-30)

## A. The no-go for every one-tooth form (the physicist's theorem, sharpened)

State per gear (now a, before b, one tooth s). A round at the pivot a carries m_in(a, b) v + s + c F(a) and splits it
at m_out, v = a - b. Three conditions:
 (C1) across rounds: s was produced in [0, m_out(prev)) and is weighted by m_in(now): injective iff m_in = m_out(prev).
 (R1) the run back within the round (the same act on the mirrored state (a, a+)): m_in(a, a+) = m_out(a, b, a+) and
      m_out(a, a+, b) = m_in(a, b): one function m(x, y) with m_in = m(a, b), m_out = m(a, a+).
 (C1)+(R1) on every course (rising and falling): m symmetric in its two slots.
Then m(b, a) ~ g(W) at the half step, and the physics is d_t (g(W) v) = F. Nature needs g = sqrt(W): no polynomial
in W(a), W(b) gives it, and no coefficient c(W) on F mends it (the integrating factor of W dv + (1/2) dW v = F is
sqrt(W) whatever multiplies F). A dial with m_in != m_out as functions (quarter-step dials (W(b) + 3 W(a)) / 4 and
(3 W(a) + W(a+)) / 4) gives nature's ratio but fails (C1) on a falling clock. A fractional momentum at dial D_in cannot
be re-expressed at dial D_out: the obstruction is a rational rescaling. The root dial escapes with L = sqrt(W) whole and
pays with the push's remainder at the pivot's L (no home across rounds). The hypothesis every form above shares:

  (H) the clock enters the act by DIVIDING THE PUSH (or the momentum) at a dial that moves with the clock.

## B. What time forward and backward removes: the clock divides TIME, not the push

Nature's equation L d_t (L d_t a) = F is autonomous in the clock's own time: d^2 a / d tau^2 = F with d tau = dt / L.
So the gear's own act is the standing act (the act as built at a STANDING dial, exact and bijective), and the clock's
depth decides WHEN the gear steps: the Node-clock has one more gear, its proper clock (the escapement), a first-order
gear like the drive:

   q_tau, tau+ = carry(L_0, L, tau),   L = L_0 + the 00 slot at the now slot,   q_tau in {0, 1} for L >= L_0.

Every gear of the Node-clock steps q_tau times, at the rest teeth:

   q, r' = carry(rest (a - b) + push, rest, r);  a+ = a + q_tau q;  b+ = b + q_tau (a - b);  r+ = r + q_tau (r' - r);

the drive, the kick and the click teeth the same way (their carries taken only when q_tau = 1), all by multiplication,
no if. The remainder carried across rounds is TIME's remainder tau, whose push L_0 never exceeds its dial L (the domain
L >= L_0, the clock at or below its rest rate): after a step tau+ = tau + L_0 - L < L_0 <= L(next), and on a round
with no step the dial does not move. So tau always stands within the dial that reads it, on every course. The force's
remainder has no such bound: that is why the theorem bites the push and not time.

## C. The run back

mirror: slots swapped, r flipped at rest (standing), r_d at T_d, tau flipped at L(before) (the dial it was kept at,
as the act as built flips r at W(b)). untick = mirror o tick o mirror. Forward at pivot a: tau + L_0 = q L(a) + tau+.
Backward at the same pivot a (the mirrored state's now): L(a) - 1 - tau+ + L_0 = q' L(a) + tau'; with tau < L(a):
q' = q and tau' = L(a) - 1 - tau; the gears' standing step runs back (the act as built at fixed teeth); the final
mirror flips tau' at L(before) = L(a): tau. Exact iff tau < L(a), which B gives on every course with L >= L_0.

## D. The physics

In proper time the gear is the standing act: a hairspring keeps its amplitude exactly, a free gear its proper velocity
u = da per proper step exactly, nothing is pumped by any swing of the clock (the swing moves only WHEN the steps fall),
two clocks at one site step together. Proper steps per round: L_0 / L. c^2 = (grip / rest) (L_0 / L)^2 = grip / W_eff
and omega^2 = D / W_eff with W_eff = rest (L / L_0)^2. For W_eff = rest + c00 to first order: L_0 = 2 rest (the
derivative of the square; no root, no square condition on den). The law's line "W = rest + c, linear" becomes
"the clock's count L = 2 rest + c, linear" with W = L^2 / (4 rest) a reading (as the root dial's readers already named
it: 1 / N linear in c, Postulate 6 at first order either way). The static relations hold with W_eff.

## E. Every push kept

The gear's carry is at the standing dial rest: every push with its remainder, the kick of 1 alive, no floor. On a
uniform clock every site steps together, so SUM_sites P changes by SUM push = 0: the row's momentum exact.

## F. The 00 row

It is a row like every other: it steps at rest with the proper clock; its new count makes L(next), read by the NEXT
round's proper carry. No dial is moved by its own quotient: the proper carry reads L at the now slot before the step,
and the 00 row's own carry is at the standing dial rest. Its wave runs on the same proper steps as light: one cone.
(The timegear deriver's carried dial is for the edge form; here the question does not arise.)

## G. To measure (whole numbers, the engine's carry)

1. One gear, the course given: free gear and hairspring on the adiabatic course (probe_root's lay), rising and falling;
   the fast swing at half the beat (probe_fp_swing's lay). 2. The board (edge_lib's cube of 3, the example universe),
   the 00 row moving: run back, the 24, books, on standing / rising / falling / varying. 3. J through the tables.
4. Hostile: a clock halving in one step; the kick of 1; sub-L pushes; the 00 wave's cone against light's; L = L_0
   exactly; the boundary L < L_0 named as the domain's edge.
