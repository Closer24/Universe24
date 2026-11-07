# Reviewed algebra for the component README

This note describes the current reference model and the preparation boundary.
It does not add a rule or establish a physical interpretation.

## Complete state and fixed coupling

The board is the periodic cube `x in (Z/LZ)^3`, with `L >= 3`. At each site,
`g in 2O` indexes 48 channels. The group label chooses a channel and its
connection geometry; it does not choose among 48 update rules. Each channel
stores exactly

```text
S[x,g] = (a[x,g], b[x,g], r[x,g])
a,b are arbitrary-precision integers; r is one of 0,1,2,3,4,5.
```

For each of the six spatial directions `d`, the fixed tensor supplies one
sender channel `P[d,g]` and one sign `w[d,g]`. Every receiver uses

```text
u_t[x,g] = sum_d w[d,g] * b_t[(x+d) mod L, P[d,g]].
T[d,g,h] = w[d,g] if h=P[d,g], otherwise 0.
```

All six inputs come from the same complete old snapshot. A negative sign
changes a contribution, and a zero matrix entry is not a deleted spatial port.

The current body actions are `B[+x]=B[-x]=identity`, `B[+y]=q_y`,
`B[-y]=q_y^-1`, `B[+z]=q_z^3`, and `B[-z]=q_z^-3`. If `R(g)` is the spatial
rotation of channel `g`, the body direction is `e=R(g)^-1 d`, the port is
`P[d,g]=g B[e]`, and `w[d,g]` is the preselected sign of the body axis of `e`.
Thus three global signs `(s_x,s_y,s_z)` supply the eight currently implemented
couplings. They are not eight independent choices at every channel. The
coupling is chosen before execution and is constant throughout the run.

## Rule3 and its inverse

For every channel, the only forward update is

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

`divmod` is Euclidean division: `2*u+r = 6*ell+r_next` and
`0 <= r_next < 6`, including when `u` is negative. This is the existing
`num=den=1` rule. Every next value is calculated from the same old state;
there is no runtime source insertion, gate, selector, detector reset or
coupling change.

Let `F(b)` denote the complete fixed six-neighbor input map. The exact inverse
of a complete next snapshot `(a_next,b_next,r_next)` is

```text
b = a_next
u = F(a_next)
r = (r_next - 2*u) mod 6
a = (2*u + r - r_next)/6 - b_next
```

The recovered remainder makes the division exact. Since the old `b` field is
the known next `a` field, every old input is available before inversion.
This proves bijectivity on the full integer state for the fixed tensor.
Rewind is used for audit, not as a second forward operation. Finite inverse
tests check the implementation; they are separate from this algebraic proof.

## Clocks, gears, memory and C events

The counter dial displays the direction of `(a,b)`; `(0,0)` has no direction.
Its normalized hand does not display magnitude, so the exact integers remain
available. The remainder gear displays `r`. An equivalent lossless form is

```text
r = 2*theta + epsilon, with theta in {0,1,2}, epsilon in {0,1}
epsilon_next = epsilon
u + theta = 3*ell + theta_next.
```

Both the phase and parity bit belong to the full state. The drawings and
camera are passive readings of saved states, not additional mechanical laws.

If the actual net input remains zero, `ell=0` and
`(a,b,r) -> (b,-a,r)`. A nonzero counter pair then rotates with period four;
the zero pair is fixed. Thus hands can move between signal arrivals. Their
motion is not automatically a click or a unit of physical time.

The existing arithmetic readout records `C` only when `ell != 0` **and** the
full channel triple changes. Its class is `u mod 3`, equivalently
`((r_next-r)/2) mod 3`. A remainder change `R` is a separate observation:
it can occur with `ell=0` and therefore without C. These observations do not
alter evolution or select a path.

The counter quantity used by the finite memory example is `I=a*a+b*b`, with
the exact identity `I_next-I = ell*ell - 2*a*ell`. It is not generally
conserved and has not been identified as physical energy. The demonstrated
levels `0 -> 1 -> 4` are a scoped response of the declared preparation.

## What separate and composed runs mean

A component recipe supplies initial triples, named existing addresses and
passive readouts. It has no private clock or runtime updater. The composer
places the recipes on one board and takes a **consistent union** of their
assignments. Identical shared triples are allowed with provenance;
different triples at the same address are rejected. It never adds counter
states or lets a later component overwrite an earlier one. Explicit sockets
reserve unassigned locations for compatible initial preparations. Named
ports do not add connections to the lattice. All components must use the
same complete tensor and background.

An isolated component run evolves its entire declared board and environment.
A composed run evolves one jointly prepared board. Saved isolated runs
cannot generally be combined afterward: the six-input sum is linear in old
`b`, but the quotient/remainder update is not linear. For example, at the
same initial remainder `r=2`, a unit input gives `ell=0`, whereas two unit
contributions arriving together give total `u=2` and `ell=1`. This is a
statement about incoming contributions to one update, not permission to add
two independently prepared full states.

Locality gives a precise sufficient condition for limited independence.
Agreement of the complete initial states on a region's backward dependence
cone of radius `T`, using periodic lattice distance, guarantees identical
observed trajectories in that region through `T` updates. This is sufficient,
not necessary for coincident outputs. The agreement includes all 48 channels,
remainders and the full declared background or shared guide. With a common stationary
reference preparation, disjoint disturbance cones give the corresponding
isolated behavior until the cones meet. Once signals can interact, the joint
trajectory must be checked directly; initial compatibility is not a proof
of functional compatibility.

The four-placement example is two `SignalSource` instances, one `GuideSegment`
and one `Receiver`: three recipe types and four initial placements. The
receiver's clock and memory are two readings of the same counters. Its source
controls establish a finite source-driven response, not an autonomous
uniqueness approval, a general preference for complexity or physical light.
