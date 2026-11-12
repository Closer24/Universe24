# One bounded local carrier–record law

This package follows issue #63 on consolidated source `f4f64e0`. It replaces
the proposed unbounded recoil counter with a collision whose recoil is carried
by an actual record packet. It does not alter the fixed-six Engine, runtime or
canonical decoder. The eight channel types are on the ordinary one board at
each node; the two four-channel groups below are counted explicitly. They are
not extra history arrays outside the Engine's retained `(a,b,r)` triples.

## The collision

Write an input as `(p,q,x,y)`: record moving along `+e`, record along `-e`,
carrier along `+e`, carrier along `-e`. Each rail is Boolean. The collision
exchanges `1001` and `0110` and fixes all other fourteen Boolean inputs. Thus
one incoming record and one oppositely moving carrier exchange their
propagation directions. The record carries the equal and opposite recoil.

The exact integer polynomial is

\[
\delta=py(1-q-x)-qx(1-p-y),\qquad
G(p,q,x,y)=(p-\delta,q+\delta,x+\delta,y-\delta).
\]

The two quartic terms of the Boolean minterm difference cancel. This leaves
degree three on the full integer polynomial, without clipping or modulo-two
operations at runtime. The proof that `G` is an involution and preserves the
Boolean set is the exhaustive sixteen-state table, also independently checked
against this polynomial. Outside the declared Boolean domain the Engine still
rewinds, but the Boolean collision interpretation does not apply.

On a ready record input `10` and exactly one carrier, the carrier output is
always `10`. The outgoing record is `10` or `01` according to the incoming
carrier direction. This is an actual preferred-port response with retained
origin information. Absent records, double records, absent carriers and
double carriers remain in the trial accounting. A prepared packet train is a
finite resource; there is no claim of an indefinitely fresh record reservoir.

The collision preserves separately

\[
n_+=p+x,\qquad n_-=q+y,\qquad n_R=p+q,\qquad n_C=x+y.
\]

Consequently the positive packet energy account `E=n_++n_-` and signed
propagation momentum `P=n_+-n_-` are conserved locally. These agree with the
declared unit-energy, unit-speed packet directions. A conversion to measured
physical units, a common operational metric and a general Einstein source
interpretation are separate obligations. In particular, the collision changes
the species carrying a directional packet; total directional occupancy does
not change. A change of species route need not change the metric's stress
source when those species are degenerate.

## A native lift without multi-edge inverse products

Let `A` and `B` each contain the four rails. Let `S` stream their plus rails by
one node along `e` and minus rails along `-e`. Define

\[
F(A,B)=(G(B),S(A)),\qquad
F^{-1}(A,B)=(S^{-1}(B),G(A)).
\]

There are eight channels, 24 retained integers per node. All forward and
inverse tensor polynomials are either onsite degree-three collision terms or
linear terms on one face. There are no old-`a` dependencies. Both groups are
part of one fixed tensor and one synchronous old snapshot.

Compile componentwise `u=3(F(b)+F^-1(b))`. Prepare all complete older histories
as `a=F^-1(b)` and retain any legal remainder `0<=r<6`. Then

\[
\ell=F(b)+F^{-1}(b),\quad r'=r,\quad
b'=\ell-a=F(b),\quad a'=b=F^{-1}(b').
\]

This proves the entire prepared sector invariant for all integer update counts,
not merely the first step. The first-order map is a permutation of the Boolean
board; the original Engine's inverse additionally holds outside this sector.
All rails stay zero or one and carries retain at most three bits. There is no
projective growth or scheduler workspace. The operator squares to

\[
F^2(A,B)=(G S(A), S G(B)).
\]

Each cohort therefore undergoes one collision and one spatial transport per
two native ticks, with opposite ordering. A two-tick phase is computational
ordering, not a derived proper-time clock. Physical comparisons must account
for the two cohorts' staggered phases.

## Repeated actual encounters

The default finite fixture has `L=7`, receiver at the origin, and two cohorts
of packets. In current `B`, record+ is placed at distances `0,-2` along the
chosen axis and carrier- at `0,+2`. Current `A` has record+ at `-1,-3` and
carrier- at `+1,+3`. Other rails are zero. Every carry is supplied by
`(channel+node) mod6`; all previous histories are calculated once before the
run using the inverse preparation.

The same receiver selects at native ticks `1,2,5,6`. The first cohort thus
selects at `1,5` and the second at `2,6`: this is not just observing each cohort
once. Records leave on the minus rail and carriers on the plus rail. No value
is injected, reset or read from the observer during evolution. Collision-off
gives no selections. Record-transport-off fails the repeated sequence and has
a separately identified tensor. Longer-time recurrence and source exhaustion
remain visible; two successful encounters do not prove structural growth.

## Verification

```
python -m validation.local_unification.native
python -m unittest universe24.tests.test_local_unification_native -v
```

The audit independently checks the sixteen-state collision, all six spatial
orientations, eighteen random Boolean complete histories, all legal carry
classes, 216 actual Engine transitions and 139,968 retained integer
comparisons. Every transition is inverted, each twelve-tick run is completely
rewound, and the four packet accounts remain constant. Native events are C0,
providing another direct counterexample to the claim that C2 is required for
route selection. Tests retain a mismatched-history negative that leaves the
Boolean sector while still rewinding exactly.

Twelve complete-carrier-matched interventions cover both the connected and
disconnected laws in all six orientations. Swapping a present record's initial
direction leaves every carrier `a,b,r` equal and preserves total initial packet
energy, but changes two future carrier components only under the coupled law.
The initial record momentum differs. These are causal record controls, not
same-stress or same-metric comparisons.

No claim of Born probabilities, autonomous physical time, growing structural
complexity, massive matter or general Einstein evolution follows from these
native algebra results. The other lanes must test any shared physical reading
on this exact law and seed domain.
