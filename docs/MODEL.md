# The single signal/clock coupling

`universe24/model.py` defines the fixed built-in tensor. This document states
its exact invariant domain and does not interpret a successful simulation as
a solution of Einstein's equations.

## Boolean reversible transmission

For one orientation g, let n=R_g e_x. Signal p streams by one face along n;
local memory m and clock phase c remain onsite. All three are Boolean. The
collision is

\[
 C(p,m,c)=(p+mc-pm,\quad c+pm-pc,\quad m+pc-mc).
\]

| Before p,m,c | After p,m,c |
| --- | --- |
| 000 | 000 |
| 001 | 010 |
| 010 | 001 |
| 011 | 110 |
| 100 | 100 |
| 101 | 101 |
| 110 | 011 |
| 111 | 111 |

C is an involution on all eight Boolean inputs and preserves p+m+c. Set
F=C S, with S the signal stream; then F inverse is S inverse C. The second-order
Rule3 law implements F on histories initialized with a=F inverse(b).

Relative group labels are signal=0, memory=2, clock=6, selector=1, counter=4;
left multiplication by g gives the selected orientation. The selector is a
retained constant bit, not an external runtime switch. The full polynomial is
the left-equivariant sum of all 48 role assignments. On the selector-separated
domain it reduces exactly to u=3(F(b)+F inverse(b)). Affine conjugation to
b=1+bit fixes the positive baseline at one and yields 1,968 monomials of degree
at most three. Every monomial obeys the one-face support rule.

The isolated counter obeys u_counter=6*b_counter. With a=K-1,b=K and K>=2,
its future values are a(t)=K+t-1,b(t)=K+t. It occupies one of the same 48 rows;
there is no extra bank. The counter is not the Boolean clock phase and does not
change signal transmission. Spatially differing counter offsets remain
isolated in this domain.

Preparation supplies every row and all carries. The Engine alone evolves it;
`sector_map` is an independent truth-table oracle and is never an evolution
callback. There is no projection back into the prepared domain. Future-positive
histories can be rewound exactly to their seed; positivity is not asserted for
arbitrary continuations before the specified preparation.

## Exact accounts and what can slow down

Let M=m+c-mc and K=p+mc. Streaming followed by collision gives

\[
 M_{t+1}(x)=M_t(x),\qquad
 K_{t+1}(x)-K_t(x)=p_t(x-n)-p_t(x).
\]

Thus M is a pointwise frozen clock-site indicator and total K is conserved.
The two clock phases are not separate matter species. The stored signal is mc.
A site with m=c=1 retains this stored unit while incoming p=1 continues;
it releases on incoming p=0. This is state-dependent residence, with finite
storage and no externally managed queue. With the same initial m=1,c=0 at x=3, incoming runs of 1, 2 and 3 ones
capture at update 1 and release at updates 2, 3 and 4: stored occupancy lasts
1, 2 and 3 updates. This is checked against the actual production Engine.
Further ones pass while occupancy remains stored, so this does not identify
individual photons or establish FIFO delay. A collision phase can also delay an
isolated pulse by one update. There is no independent, evolving edge-length
variable in this implementation.

These identities hold for arbitrary spatial Boolean profiles in a single
selected orientation. Simultaneously populating independent rotated sectors
can activate overlapping selectors. Closure and positivity for that combined
preparation are not established; the API does not silently construct it.

## Transverse signal readout

For deviations x=b-1 and selector relative label s=1,

\[
 E=\sum_g (R_g e_y)x_g x_{gs},\qquad
 B=\sum_g (R_g e_z)x_g x_{gs}.
\]

This is a root-independent covariant passive readout. In the declared sector
it gives E=(R_g e_y)p and B=(R_g e_z)p. With no clock sites, a transverse plane
profile moves one face per Engine update, with B=n cross E, E dot B=0 and
E squared=B squared, in lattice units c=1. This is a restricted light-like
transport sector. Arbitrary Maxwell superposition, general directions,
Lorentz invariance and physical photon calibration do not follow from it.

All tensor coefficients are divisible by three, so carries remain fixed.
Arithmetic event emission still depends on the changed full triple and
nonzero quotient. The model emits only C0, not C1 or C2.
