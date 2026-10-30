# rd_phys notes 01: first read (engine, EDGE2, ROOT, mc_phys REPORT)

## The act as built (step.py)
q, r+ = carry(W (a - b) + push, W, r); a+ = a + q; b+ = a.  W = rest + read(clock, a) at the NOW slot.
W = W+ within a round: the (d_t W)(d_t a) term is dropped (the comment in step.py says so).
Mirror: swap slots, flip r in W(b). untick = mirror . tick . mirror.
Static clock: c^2 = grip / W, omega^2 = D / W  -> N = sqrt(rest / W) is what the static act fixes.

## mc_phys REPORT (the earlier physicist)
Item 1: edge keeps W v (wrong), as-built keeps v (wrong), nature keeps sqrt(W) v.
Proposed fix: the root dial. W = L^2, L = L_rest + c00, D = L(b) + L(a), push divided once at L(now).
probe_g: L v within 4 permille, A within 1 permille, T^2/W 999-1000 (adiabatic, W 10^4 -> 4 10^4, one gear).
Item 2: the cut puts the 00 mode on a second cone (c_00^2 = grip/rest vs grip/W).

## EDGE2 section 3 table (one gear, adiabatic course):
form        v^2 W at Wx4   A/A0 at Wx1.86   A^4 W   T^2/W
as built    3999           1166             3433    988
edge        249            857              1003    988
root dial   1000-1008      999              1957    1000

## ROOT.md claims (to check)
- q_F = odd rounding of F / L (rule (iv), half away from zero), remainder dropped (rule (ii)).
- N = 2 (D_in (a-b) + 2 q_F) + s, split half-open at 2 D_out, D_out = L(now) + L(next).
- Mirror (b, a, -1 - s).
- dropped force 1-6 permille at L 9..73; < 1e-11 at the calibre (L ~ 3e11 vs pushes 1.5e22 per notch).
- rest a square only if den = 6 k^2 (even seed).
- "In the clicks N = L_rest / L, linear".
- kept push tooth fails on falling clock (run back 2 of 40).

## First suspicions (to probe)
S1. "D_out = L(now) + L(next)": L(next) depends on the 00 row's NEXT count. For a non-00 row the 00 row's
    a+ is computed in the same pass -> known only if the 00 row is computed first or because 00 row is on the
    cut (standing, loader's). On the cut the 00 slot never moves from the act, so "L(next)" is only known
    because the clock course is GIVEN from outside. In a real run with term 5 the 00 row moves by the act and
    the next L is unknown at the pivot -> is the dial law well-defined on the real act? EDGE2 sec 4 admits:
    "the neighbours' next counts are unknown at the pivot".
S2. W = L^2 with L = L_rest + c00: then W = L_rest^2 + 2 L_rest c00 + c00^2. The law says W = rest + c00
    (linear, Postulate 6, decision 41). So the 00 slot's meaning changes: a depth c00 in the root dial is a
    depth 2 L_rest c00 + c00^2 in the old W. Light's c^2 = grip / W: grip is NOT squared. So c^2 = grip / L^2
    -> c ~ 1/L. And omega^2 = D/W... but in the root dial the equation is L d_t (L d_t a) = F: omega_coord =
    omega_proper / L... check what the hairspring beat is in the root dial: with D the spring and the
    dial... need to derive.
S3. The dropped remainder of the push: q_F = round(F / L). F is a sum over 6 spokes of grip (nb - own).
    With F < L/2 the push is ZERO. In the regime "below one notch" the force never acts: a floor. The
    floor on the FORCE (not on the velocity) is a new floor: a hairspring with amplitude A such that
    D A < L / 2 does not swing at all. Compare: the as-built act keeps the push remainder in r, so a small
    push accumulates. The root dial drops it: small forces vanish. That is a physical bias: a dead zone
    around equilibrium -> the ground state of a hairspring is a band, not a point; the zero-point swing is
    lost; in a long wave with small gradients (k/W small!) the force is small -> waves below the dead zone
    do not propagate at all. THIS is where nature's hands sit (long waves, small k). Must measure.
    Also: rounding half away from zero is unbiased for symmetric distributions but is it unbiased when F
    is correlated with position (a spring)? Energy leak: round-off in the push with the remainder dropped
    is like a dither-free quantizer -> limit cycles.
S4. "the 00 row's standing L is the loader's (the cut)": the whole generic claim leans on the cut, which
    mc_phys item 2 calls BLOCKING (second cone). Does root dial help or hurt the cut? In the root dial
    c_00^2 = grip / L_rest^2 vs light's grip / L^2: the ratio is (L / L_rest)^2 = W / W_rest, SAME ratio as
    before in terms of W. But in terms of the 00 slot c00: L = L_rest + c00 -> the gap is bigger per unit
    of c00. Neither helps nor hurts in W; hurts in the slot.
S5. den = 6 k^2: the seed. What is den in the example universe? What else uses den (grip = den Gamma^2)?
    Changing den changes grip too; c^2 = grip / W = den Gamma^2 / (6 den Gamma^2) = 1/6 at rest regardless.
    So c^2 = 1/6 at rest in either. But L_rest = 6 k Gamma. Need to see load.py and the universe file.
S6. A^4 W = 1957 under the root dial vs nature: the adiabatic invariant for nature. Under nature's equation
    L d_t(L d_t a) = -D a with D constant: in proper time tau (d tau = dt / L), d^2 a / d tau^2 = -D a:
    omega_proper^2 = D, constant! So the amplitude is constant exactly (not adiabatic: nothing changes in
    proper time). A^4 W = A0^4 W: grows as W: at Wx1.86, 1860; at W x 1.957... they quote 1957 at some W.
    Fine, consistent with A constant.
    BUT: in the root dial is the spring's strength D constant or does it read the slot? Unchanged.
    So nature's test as they run it is: a hairspring in proper time sees NOTHING. Good. v^2 W constant
    for the free gear: v = da/dt coordinate; L v = da/dtau constant. OK.
S7. Many notches per stride & k/W small: the coordinate velocity v = q per round. In the root dial
    q = carry of (D_in (a-b) + 2 q_F)... with D = 2L: the effective "teeth" is 2 D_out = 2(L + L') ~ 4 L.
    Hmm, the velocity is stored as the quotient q with the tooth s in [-D, D-1]. Need to look at the exact
    form in probe_root.py / edge_lib.py.
