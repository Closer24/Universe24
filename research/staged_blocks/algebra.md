# Prepared shielded counter orbits

Base commit: `b552f90dd8e19f836424411019dccd573c10fa6c`.
The reusable `ShieldedOrbit` preparation is data only. The reference Rule3
engine, 48 channels, six spatial neighbors and the preselected tensor remain
unchanged. This is an installed mathematical clock candidate. It does not
establish that an incoming signal can write, capture, approve or release it.

## Exact construction and theorem

Choose a channel g at a site c, integers A,B with `|A|+|B|<=2`, and a center
remainder rho in `0..5`. All other counters are initially zero. For each of
the six directions d, let `h_d` be the receiving channel at `c+d` and `w_d`
its signed coupling weight from g. The tensor is a signed permutation, so
each recipient is unique; the six sites are distinct for every L>=3.

With zero actual input at the center, Rule3 has zero quotient and gives

| Phase | Center counters | Cumulative emitted b before this phase |
| --- | --- | --- |
| 0 | `(A,B)` | `0` |
| 1 | `(B,-A)` | `B` |
| 2 | `(-A,-B)` | `B-A` |
| 3 | `(-B,A)` | `-A` |
| 4 | `(A,B)` | `0` |

Let `P=(0,B,B-A,-A,0)`. Prepare recipient d at `(0,0,r_d)` such that

```text
0 <= r_d + 2*w_d*P_t <= 5       for every phase t.
```

Every recipient quotient is then zero, so its counters stay zero while its
retained remainder is exactly `r_d+2*w_d*P_t`. It sends no counter influence
onward. Every other channel remains at its stationary initial background.
In particular, the center receives zero input, closing the argument without
assuming an externally supplied waveform. Induction proves this complete
board orbit for all times in the isolated preparation.

The range of P is `|A|+|B|`. A valid integer recipient remainder exists exactly
when this range is at most two: its doubled range must fit in six successive
remainder values. The recipe uses an even remainder nearest to 2 in the
admissible interval `[-2*min(w*P), 4-2*max(w*P)]`. Optional explicitly supplied
halo remainders, including odd values, are accepted only if all phase bounds
hold. The center remainder does not change and may have either parity.

For nonzero `(A,B)` the complete state's minimal period is four: a nonzero
integer vector cannot equal its 90-degree or 180-degree rotation. For zero
counters it is stationary. Removing only the prepared center counters while
retaining every halo remainder also produces a stationary control.

All quotients in this isolated orbit are zero. Consequently it has no guarded
arithmetic C events, despite its moving counter phases and retained halo
changes. A periodic counter motion is not by itself an observed physical clock
or a derivation of physical time from clicks.

## API and assembly contract

```python
from research.components import BoardSpec, TensorSpec, finalize, place
from research.staged_blocks.orbit import ShieldedOrbit

tensor = TensorSpec.from_signs((1, 1, 1))
clock = ShieldedOrbit(channel=0, a=1, b=0, r=2, tensor=tensor)
prepared = finalize(BoardSpec(9, tensor=tensor), [
    place(clock, at=(4, 4, 4), name="clock", wrap=True)
])
states = list(prepared.engine.evolve(prepared.initial, 8))
```

`phase=0..3` shifts the complete center-and-halo preparation; it does not
rotate the center counters while leaving an inconsistent halo. `present=False`
sets only the initial center counters to zero, preserving the same apparatus
remainders. Location and orientation are handled by the existing generic
placement function. The convenience `prepare_orbit` returns the same
`PreparedBoard` type for a single clock.

The patch explicitly assigns all 48 channels on its center and six halo nodes,
336 assignments in total. It exposes `center`, `center_node`, `halo`, and
`region` ports, plus the center's `orbit` initial-source address. Structured
resource metadata records the complete tensor fingerprint, protected nodes,
base counters, actual initial phase and halo remainders. Ordinary assembly
rejects conflicting initial values and different tensors. An identical shared
assignment does not prove dynamical compatibility: simultaneous influences
from two components can add at a shared halo.

The generic Presenter phase selectors are explicitly labeled projections:
they inspect the selected center channel and six receiving halo channels.
They are not scientific acceptance predicates for an attached apparatus.
The registered assessment separately compares the **entire complete board**,
including all 336 protected channels, with the analytic formula. This avoids
exceeding the existing Presenter clause budget when composing components.

The isolated theorem assumes no additional input to its center or halo. It
does not promise immunity to an arbitrary attached signal source. A guide
sharing a halo node must preserve all its own retained channel remainders and
use an explicitly compatible joint preparation. Other zero-counter stationary
remainders can be present if no additional counter inputs occur.

For example under +++, a center `(0,+1,rho)` with a touched recipient at r=0
gives recipient remainders `0,2,2,0,0`; `(0,-1,rho)` with recipient r=4 gives
`4,2,2,4,4`. Both are exact quotient-free interfaces to suitably prepared
guide channels. This fact establishes their clock-only baseline, not their
behavior when a moving packet arrives.

## Conditional halo opening: a separate input contract

For the default center `(1,0,rho)` and a recipient of weight w, the actual
center contribution cycles `0,-w,0,+w`; recipient phases are
`2,2,2-2w,2-2w`. Suppose an additional incoming contribution `q=-w` occurs
once at that recipient, followed by zero extra contribution. The first halo C
occurs after respectively `2,1,1,3` updates for arrival phases `0,1,2,3`.
Its first nonzero quotient and new b are `-w`, with new remainder `2+2w`.
Until that first event the halo counters remain zero, so the local feedback
assumption is consistent. This is exact scalar input-contract arithmetic.

It is **not a runtime injection API** and is not an autonomous release result.
A real approval packet affects its entire neighborhood and has a complete
waveform. The bipolar additional contribution `q,0,-q` arriving at phase 3
undoes the priming before a quotient occurs. After any first halo C, its new
counter affects all six neighbors, including the center; one event does not
establish one directed outgoing carrier or continuing center stability.

A separate actual-signal study must retain null, clock-only, carrier-only
and joint preparations at all four arrival phases. These 16 controls need the
same initial apparatus remainders within each group, complete input sums,
all outgoing ports, complete-state inversion, and a prospectively registered
release window. The isolated orbit's tests are not a substitute for that study.

## Frozen validation and limits

The [protocol](orbit_protocol.json) fixes 744 eight-step complete-board runs
before observations: 384 sign/channel cases, 312 counter/remainder/phase cases,
24 stationary controls and 24 initial halo disturbances. It includes L3/L5/L9,
boundary-crossing placement, every channel and sign triple, all 13 permitted
counter pairs, every center remainder and complete orbit phase. It is a
declared finite selection, not every Cartesian combination of those parameters.

Every recorded full state is compared to the analytic orbit; all C events,
full center nodes, retained halos, noncenter counter activity, forward/inverse
steps and complete rewinds are kept. Independent matrix routing in
[`test_staged_orbit.py`](../../tests/test_staged_orbit.py) reconstructs the
halo recipient and expected complete state without the production routing
tables. The symbolic proof above supplies the all-state/domain statement;
finite checks validate its implementation. Disturbance outcomes are reported
without changing the success criterion or claiming general stability.

Reproduce the registered study into a new directory:

```bash
python -m research.staged_blocks.orbit --output research/staged_blocks/evidence/orbit
python -m unittest discover -s tests -p test_staged_orbit.py -v
```

The runner writes its protocol copy, registration and source hashes before
the first experiment. Complete compressed records include initial raw patches,
fixed tensors and full trajectories. All cases are available in paged generic
Presenter bundles; the root HTML opens four preselected unit-clock phases
and their matched absent controls. Every other case remains available in the
complete paged bundles. No selection depends on an observed outcome. The evidence
does not establish a light-written memory, approval gate, unique release,
physical photon, or quantum measurement.

## Signed tensors: exact gauges and a local obstruction

This section concerns a restricted, explicit class of state conjugacies. It
does not classify arbitrary possible conjugacies or establish different
physical theories. For a fixed sign field `sigma(x,g)` in `{+1,-1}`, transform
each local triple by the identity when sigma is positive and by

```text
K(a,b,r) = (-a,-b,4+2*(r mod 2)-r)
```

when it is negative. If every edge satisfies
`weight_new(i,j)=sigma(i)*sigma(j)*weight_old(i,j)`, the actual new input is
`sigma(i)*u_i`. The scalar K identity then proves the complete-state
conjugacy `F_new T_sigma = T_sigma F_old`. Every counter and remainder,
including the guide and its halo, must be transformed. Background remainder
2 is fixed by K. A fixed initial seed under a changed tensor is a different
comparison from this transformed-preparation conjugacy.

Let `chi(g)` be the parity sign of the proper rotation's permutation of the
four unoriented cube body diagonals. It is a group character: the identity
body action has character +1, whereas the quarter-turn Y action and the
three-quarter-turn Z action both have character -1. Define

```text
sigma(x,g) = (-1)^(k*(x+y+z)) * chi(g)^l,       k,l in {0,1}.
```

Every unwrapped nearest-neighbor step changes spatial parity. The fixed body
actions therefore give the exact sign mapping

```text
(s_x,s_y,s_z) -> ((-1)^k*s_x, (-1)^(k+l)*s_y, (-1)^(k+l)*s_z).
```

For k=0 this is valid on every periodic L. For k=1 it is globally well-defined
on even L. On odd L, a wrapping edge breaks the checkerboard relation, so
the argument applies only inside a declared unwrapped causal domain. The
odd-length ring of identity-body-action X edges is itself a global sign
obstruction when the X sign is flipped.

In contrast, changing `+++` to `+-+` has a **local** obstruction, with no
periodic seam involved. Independent exact matrix routing gives these paths
from `(0,0,0,channel 0)`; all old +++ weights equal +1:

| Path | Direction | New position and channel | +-+ edge weight |
| --- | --- | --- | --- |
| A | +Z | `(0,0,1,25)` | +1 |
| A | +X | `(1,0,1,35)` | -1 |
| A | -Y | `(1,-1,1,12)` | +1 |
| B | -Y | `(0,-1,0,45)` | -1 |
| B | +X | `(1,-1,0,18)` | +1 |
| B | +Z | `(1,-1,1,12)` | -1 |

The paths have the same endpoints but relative sign products -1 and +1.
Any diagonal sign gauge telescopes to the same endpoint sign ratio on both
paths; hence no such gauge can map these two tensors. Translating the paths
by `(1,1,1)` embeds the entire witness without wrapping already in L3.
Body-axis signs are therefore not simply independent world-axis checkerboard
signs. The regression test reconstructs this witness from the independent
matrix algebra rather than the engine's tables.

Opposite path-sign products do not themselves prove destructive interference
or signal cancellation. Intermediate Rule3 quotients, retained remainders,
feedback and other paths determine the actual amplitude history. Cancellation
still requires a complete-board experiment with functioning singleton controls.

More generally the same two paths have relative products `tau_y` and
`tau_z`, where tau is the ratio of new to old body signs. This obstruction
requires `tau_y=tau_z` for this gauge class. Together with the construction
above, on an infinite lattice or even periodic cube the eight sign triples
form two classes under these diagonal sign/K gauges, distinguished by
`s_y*s_z`. On an odd periodic cube the X ring additionally requires
`tau_x=+1`, leaving four global classes. This is a statement about these
specific gauges, not a proof about all transformations or observables.

Under a valid gauge, guarded C occurrence at each address and time is
preserved, while a negative sigma changes the quotient sign and permutes
the `u mod 3` classes. Readouts must be transformed consistently. A genuine
comparison of +++ and +-+ remains worth testing, but a missing output alone
does not establish cancellation: both singleton controls must still work,
and the complete inverse must retain the input distinction.

## A prospective relative-phase memory observable

This is algebra for a separately registered follow-up. It does not change the
original magnitude/remainder record criterion or turn its failures into passes.
Let a target counter pair be `(a,b)` and a reference clock on the **same board**
be `(c,d)`. Define the passive integer observables

```text
D = a*c + b*d
X = a*d - b*c.
```

X denotes a cross product here, avoiding confusion with arithmetic C events.
When both pairs undergo the zero-quotient rotation `(a,b)->(b,-a)`, D and X
are invariant. Also

```text
D*D + X*X = (a*a+b*b)*(c*c+d*d).
```

For two unit-magnitude clocks, the relative record has four possible values:
`(D,X)=(1,0),(0,1),(-1,0),(0,-1)`. A signal can therefore leave a persistent
relative phase difference even when the old record `(a*a+b*b,r)` is unchanged.
That would be a different prospectively declared record, not a retrospective
reinterpretation of an unsuccessful earlier test.

For arbitrary actual inputs and quotients ell at the target and m at the
reference, direct substitution gives

```text
D_next-D = ell*m - ell*c - a*m
X_next-X = b*m - ell*d.
```

The actual input first determines `ell,r_next=divmod(2*u+r,6)`. A quiet
remainder change can prime a later quotient, which then changes relative
phase. If the reference always has zero quotient, the integrated changes are

```text
D_T-D_0 = -sum(ell_t*c_t)
X_T-X_0 = -sum(ell_t*d_t).
```

This explains why balanced quotient/input words need not erase a phase record:
the contributions are weighted by the reference phase. None of these equations
injects a prescribed input or selects a trajectory. Nonzero quotient is not
automatically a guarded C event: an unchanged complete triple suppresses C.
The quiet unit-orbit proof explicitly has zero quotient, so it does not rely
on that weaker event test.

A follow-up should place the complete prepared reference sufficiently far from
all other initial disturbances that its full protected region lies outside
their toroidal causal cones throughout the declared horizon. Each Rule3 update
has spatial radius at most one. For example, on L129 a reference displaced by
64 sites in both transverse coordinates can supply a generous margin for H40,
but the actual minimum distance must be checked against every prepared source
address and all seven protected nodes. Preserve the exact same reference and
apparatus in every matched control.

During a registered eight-update retention interval, retain nine full states,
verify the target and reference regions at lag four, check zero quotients at
both clock channels, and retain every external input term. Zero total incoming
sum alone can conceal compensating influences. Check the entire protected
regions rather than only D and X, and report the original magnitude/remainder
criterion alongside the new record.

D and X are computed by a passive observer. Their persistence would establish
an internally represented relative phase under the declared preparation; it
would not establish an internal comparator, a propagating readout/approval
message, exclusive directed release, or physical photon statistics. Those
require additional ordinary Rule3 interactions and separate tests.

## Completed isolated-orbit validation

The frozen [result](evidence/orbit/result.json) records 744 runs, 6,696 complete
states and 5,952 forward/inverse transitions. All 720 unperturbed and source-off
cases meet the full-board formula, minimal-period and zero-C criteria. Every
full rewind matches. Runtime was 178.014 CPU seconds within the registered
180-second bound. The independent audit is a separate review artifact.

The 24 initial disturbances give a useful finite distinction. All six halo
changes from r=2 to r=0 generated ten world C events each over eight updates,
had no complete return within four updates, and changed the center magnitude
between zero and one. The six changes r=2 to r=4 and twelve initial halo
counter changes b=+1/-1 each returned the complete state after four updates,
with no C events over eight updates. All remained reversible. These are
specific finite preparations, not a claim of arbitrary disturbance tolerance.
Their mismatch from the unperturbed formula at state zero merely reflects the
intentional initial change; it is not itself evidence of dynamical instability.

## Remainder parity is a frozen spectator

Write each remainder as `r=2*s+p`, with `s` in `{0,1,2}` and `p` in `{0,1}`.
Euclidean division `u+s=3*q+t`, with `t` in `{0,1,2}`, gives

```text
2*u+r = 6*q+2*t+p
ell = floor((u+s)/3)
s_next = (u+s) mod 3
p_next = p.
```

This proves more than conservation of parity at each fixed address. Since
the fixed coupling reads only the neighboring b counters, the complete
counter/reduced-remainder trajectory `(a,b,s)` is independent of every initial
parity label. The existing C guard is `ell!=0` and a changed triple; because
p is fixed, the latter is equivalent to a changed `(a,b,s)`. Its kind is
`(s_next-s) mod 3`. C occurrence, kind and quotient are therefore independent
of parity when the reduced initial states match.

A passive reader of the complete state can inspect p, and complete logged
triples retain it. However, an internal Rule3 component cannot turn a difference
only in p into a different counter, reduced remainder or C response. Thus this
mathematical invariant is not already an operationally measured physical
invariant. No state reduction or change to the inverse contract is proposed.
