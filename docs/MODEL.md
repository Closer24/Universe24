# The single signal/clock coupling

`universe24/model.py` defines the fixed built-in tensor. This document states
its exact invariant domain and does not interpret a successful simulation as
a solution of Einstein's equations.

## Boolean reversible transmission

For each directional face, let n=R_g e_x. Signal p streams by one face along n;
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

C is an involution and preserves p+m+c. Each face has F=C S, with S the
signal stream; F inverse is S inverse C. All six face maps act simultaneously
on disjoint sets of retained channels. They do not scatter into other faces.

The eight labels of a face are g h^k, k=0..7, where h is the order-eight
stabilizer generator (group label 1) of e_x. Positions 0,1,2 retain p,m,c;
positions 3..7 retain marker bits 0,0,0,1,1. The eight cyclic orientations
and eight live triples give 64 distinct eight-bit words, so the marker phase
is uniquely decodable. Each direction may select its own phase, spatially
uniform across the lattice. Markers are counted state, not an external
selector, hidden clock or runtime setting.

The fixed cubic prototypes FORWARD3 and INVERSE3 evaluate 3F and 3F inverse
for a target row. Their exact identities cover all 512 local/neighbor/phase
cases each (8 local triples times 8 neighbor triples times 8 phases).
They are fixed integer coefficients in the source; no interpolation solver
runs during preparation or evolution. Applying the prototypes at all 48
labels gives exact left 2O covariance and one-face support.

With deviations x=b-1 the raw tensor is

\[
 u(b)=6+3F(x)+3F^{-1}(x).
\]

Affine expansion gives 2,400 monomials of degree at most three. Initialize
b=1+x and a=1+F inverse(x). Rule3 then advances b to 1+F(x) exactly.
All six faces can have arbitrary spatial Boolean p,m,c simultaneously.
All future a,b are in {1,2}; arbitrary explicitly supplied carries in 1..5
remain fixed. Thus the complete prepared state stays positive indefinitely.

Every face uses eight retained integers per bank; six faces use all 48 rows,
or 144 integers across a,b,r. There is no separate unbounded counter. The
Engine index orders execution, while physical time must eventually be
calibrated using retained phase clocks and observable exchanges.

Preparation supplies every row and carry. The Engine alone evolves it;
`sector_map` is an independent truth-table oracle, never an evolution callback.
There is no projection back into the prepared domain. An arbitrary raw state
outside the domain still has the exact Engine inverse, but positivity and
Boolean transmission are not claimed there.

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
individual photons or establish FIFO delay. A permanently occupied input can
keep stored occupancy indefinitely; finite latency for every identifiable
message is not guaranteed. A collision phase can also delay an
isolated pulse by one update. There is no independent, evolving edge-length
variable in this implementation.

These identities hold independently in all six directional circuits. The
busy-input contract tests also activate all six directions together. Their
independence is a limitation: there is no cross-face recoil or scattering,
no movable massive body and no universal gravitational source coupling.

## Transverse signal readout

Decode the retained marker phase of each face to obtain its root g and signal
p. The passive field readout sums

\[
 E=\sum_{faces}(R_g e_y)p,\qquad
 B=\sum_{faces}(R_g e_z)p.
\]

This full-state audit reads the counted markers rather than a root parameter.
It is separate from the click-only observer, which needs public calibration. It transforms covariantly under the joint 2O action.
With no clock sites, an individual transverse plane profile moves one face
per Engine update, with B=n cross E, E dot B=0 and E squared=B squared,
in lattice units c=1. These null identities apply to each single plane mode;
multiple crossing modes need not have zero field invariants. This is a
restricted light-like transport sector. General Maxwell evolution, continuous
rotations, Lorentz invariance and photon calibration remain unproved.

All tensor coefficients are divisible by three, so carries remain fixed.
Arithmetic event emission still depends on the changed full triple and
nonzero quotient. The model emits only C0, not C1 or C2.
