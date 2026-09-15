# Stationary source and delivered response probes

This historical source convention is retained for the charged-pair example.
The original inputs are in the [retired package](README.md).

These two schema 1 configurations use the existing generic field engine. They
are candidates for a small-space audit, not established physical field models.
The contracts are [spatial fields](../../docs/SPATIAL_FIELDS.md) and
[spatial response](../../docs/SPATIAL_COUPLINGS.md).

| Contract | Configuration |
| --- | --- |
| Domain and timing | Open 9 by 9 by 9 nodes, one tick per link, three ticks |
| Capacity and work | Two disturbance slots per node, at most four fields and two types, one emission and one response rule, fixed six-port state |
| Source | Held at (4, 4, 4), strength 216, equal octant and axis weights |
| Emission | Explicit `source: true` injects 216 scalar units per field interval while preserving carried strength |
| Receiver | Held at (5, 4, 4), initially zero vector stock, signed polarity 1 |
| Response | Negate the delivered scalar-flux vector after multiplying by receiver polarity; exchange this amount between carrier and same-named local vector stock |
| Reaction | Equal and opposite vector change retained at the receiver node; zero immutable baseline |

## Independent expectations

The source configuration emits repeated pulses; the filename `source-pulse.json`
does not mean the source shuts off after its first pulse. Each pulse has 216 units,
27 in each octant. Its first hop delivers 36 units to each of the six axial
neighbors. A front crosses one link per interval and cannot visit the source
again on these open monotone paths. Every isolated cohort retains 216 scalar
units until an open boundary is reached. Total scalar inventory grows by the
explicitly recorded 216-unit injection each interval; it is not constant.

After two completed hops, the first cohort gives 12 units to each of six axial
Nodes at Manhattan radius two and 12 units to each of twelve edge Nodes at that
radius. It has 216 units in 18 Nodes. Those two sets have different Euclidean
distances despite equal node intensity. This is an explicit lattice-anisotropy
control, not an inverse-square or spherical-isotropy claim.

The receiver has no delivered signal in its initial cycle. At tick 1 the first
scalar pulse has completed its +X link, delivering the vector projection
(36, 0, 0). The next receiver cycle exchanges this vector: its carrier gains
(36, 0, 0) and the local momentum field gains (-36, 0, 0). With the ample normal
budget this is the cycle starting at tick 1, visible after the second step.
Subsequent completed samples repeat that increment. Reversing polarity reverses
both changes. Polarity zero or source strength zero gives zero vector change.
Combined carrier-plus-field vector stock remains exactly zero in every case.

The runner's event timestamps and snapshots must verify those timing expectations;
schema acceptance alone is not run evidence. Every actual run uses the existing
HTML recorder when visualization is requested; these configurations request no GIF.

## Physical gaps exposed by this probe

The source is externally supplied, not funded by a debited energy reservoir.
The receiver is held deliberately to isolate its local response; this does not
demonstrate acceleration, free motion, a mass-dependent response, or source recoil.
The retained vector reaction balances the receiver locally but has no configured
propagation rule. The scalar driver is not depleted by its use in the response.
Consequently these checks establish causal scalar transport and exact vector
bookkeeping, not an energy-conserving radiation-pressure, Coulomb or gravity law.

The receiver's polarity-dependent action is a supplied generic arithmetic rule;
its sign is not an emergent attraction or repulsion. A physical replacement needs
a defined energy owner and local conservative transfer, independently validated
motion and field dynamics, and evidence for angular and distance behavior. No
source identifier, self-field estimator, direct neighbor-state read, remote
source search or global correction is used. The source has no response rule, so
its immobility is not evidence of a general self-force solution.

No specialist skill update is needed: the existing field-development skill already
requires explicit source accounting, external-source controls and separation of
local conservation from unestablished physical laws.
