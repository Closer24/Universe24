# Four phase-relation records on the same board

This first construction attaches a finite test apparatus to the saved 44-channel
proposal through the existing bundle interface. It adds no second Engine, metric,
global age, random ticket or runtime callback. All 48 channels retain `(a,b,r)`.
It leaves every original tensor term and the entire 44-channel trajectory
unchanged. That is an explicit **one-way apparatus approximation**, not a proof
that physical apparatus can have zero stress or no reaction on the carrier.

## Fixed construction and allocation

Let `z(x)=b[field.phi,x]+i b[field.chi,x]` be the existing raw carrier. The four
appended node channels are:

| Index for the 44-channel source | Name | Driving integer |
| --- | --- | --- |
| 44 | `observer.local_intensity` | `I0(x)=|z(x)|²` |
| 45 | `observer.link_x` | `Ix(x)=|z(x)+z(x+ex)|²` |
| 46 | `observer.link_y` | `Iy(x)=|z(x)+z(x+ey)|²` |
| 47 | `observer.link_z` | `Iz(x)=|z(x)+z(x+ez)|²` |

Each input is `u=3I`. The unchanged integer rule therefore gives

```text
ell, r_next = divmod(6*I+r, 6) = I, r
a_next = b
b_next = I-a
```

This identity holds for every signed apparatus history and every carry `0..5`.
The carrier squares and cross terms have degree two and use at most the target
and one face neighbor. Every new `a` dependence is absent, so staged inversion of
the base remains valid. The source scalar oracle still checks complete state;
the displayed identity is not substituted for Engine evolution.

The three positive axes enumerate all undirected face edges on the periodic
board. Opposite direction and seam cases are checked independently. The record
names are not independent clock fields: they observe carrier relations, while
their retained histories follow a driven second-order recurrence. The assembly
has 48 channels, 144 retained integers per node, plus external audit files which
are never read by evolution. Bit growth is reported separately.

## Phase, time and gauge scope

The two existing carrier components share the staggered encoding sign on the
pinned source's prepared uniform phase sector, so its common sign cancels from
the quadratic records. For a generic bundle the formula is only a raw integer
relation. The projective proposal in PR #47 uses a different denominator; this
construction does not silently reuse the old source's physical calibration.

A common quarter-turn `z -> i*z` preserves every driving integer. Changing only
one endpoint changes coherent intensity: aligned unit carriers give 4, opposed
carriers give 0, and a quarter-turn gives 2. This is exact algebraic interference.
It is **not invariant under independent local gauge rotations**: a physical
charged-carrier link would need a specified parallel transporter and gauge law.
No such law is added here. Nor is an independently ticking proper-time apparatus
established by these records. The complete board remains the dynamical system;
the numerical update index is only external audit ordering.

## What observer memory can and cannot do

The exact quotient is independent of apparatus history. Nevertheless the
canonical arithmetic event also requires a changed retained triple. At `I=2`,
an initially empty record changes and emits quotient 2, while `a=b=1` with the
same carry remains unchanged and emits nothing. Both source states and driving
intensities agree. This is a concrete effect of retained apparatus preparation
on a later recorded event.

It is not structural selection. The new fields never drive the source, so
different apparatus histories cannot change future carrier links, geometry or
matter. The triangular dependency proves this obstruction for this construction,
independently of finite simulation length. The saved record can lose information
about a complete reversible state: an empty bin does not imply zero intensity.
All emitted apparatus records are C0 because their remainders are unchanged.
Selecting C2 would discard all apparatus events.

## Next interaction port, before another law is proposed

To make a history-dependent observer alter future carrier structure, an explicit
term must connect its retained state back to a declared source equation. That
would change the 44-channel law and require a new model version, complete degree
and locality checks, source/stress accounting, a gauge-compatible coupling, and
revalidation of constraints and conservation. A global complexity score cannot
select this term during execution. A proposed local comparison must have a
specified invariant domain and retain the losing alternative or otherwise prove
its inverse. No unreviewed feedback term is introduced in this first slice.

The immediate falsifying next experiment is a matched-history intervention on
that proposed feedback law: identical carrier inputs but different retained
apparatus histories must alter a predefined future structural motif statistic;
disconnecting the feedback must remove the effect. A finite burst-growth test
then needs separately declared bursts, persistence, periodic/noise controls and
held-out preparations. An intensity quotient by itself is not a single-outcome
measurement law or a Born derivation.

## Reproduction

`append_phase_observers(base_bundle)` in `validation/clock_links/model.py` returns
ordinary immutable inputs for `system.runtime.run_bundle`. All optional
apparatus seed arrays are complete exact integers; invalid types, carries or
budget fail through the ordinary bundle contract.

```bash
python -m validation.clock_links.phase_audit --base-bundle PATH --out runs/clock_links/phase
```

The report includes the base and extended bundle/tensor hashes, exact quotient
comparisons, unchanged-base checks, phase/seam controls, matched apparatus
history, integer bit lengths and saved full-state replay. Reports retain explicit
open status for physical clocks, gauge transport, apparatus backreaction,
complexity selection, Born probabilities and Bell violation.

## Actual pinned-source result

The first integration run uses source commit
`49b896c795203914a939e465d6d39e5b99343259`, exported by the current main
`validation.team48_contract` adapter. It preserves that original unconstrained
audit seed; modified local phase/history controls are labelled separately.
The final strengthened audit in `runs/clock_links/phase-complete/phase.json`
records:

- 48 retained channels, 27 nodes, three complete updates;
- all 324 apparatus quotient comparisons exact, with all 44 source channels
  unchanged relative to the original source execution;
- all 18 phase and seam cases exact: 4, 0, and 2 for the three unit-phase cases;
- 314 emitted apparatus events, all C0;
- peak retained integer lengths 6, 12, and 25 bits after successive updates;
- full generic runtime verification and complete rewind;
- all 20 phase/history control runs saved with complete seed/final state and
  common tensor, then reloaded, replayed and rewound independently of summaries;
- matched-history local event counts `[1,1,1]` versus `[0,0,1]`, despite identical
  quotients `[2,2,530]` and identical source states.

The extended tensor hash is
`094bb4edbe243e4f7654073e64688ebc7b56d951724a21a0f3af1526153df611`.
The final bundle hash is
`f15c3c342d4a9ee807640fcd6357996a1c878cb43e448f8371e3a6b6b662fad9`;
it includes complete seed, ownership and passive model metadata. The earlier
independent-review bundle `4559fcbf...` omitted each apparatus channel from its
readout-dependency metadata. Its tensor/trajectory were identical, but the final
metadata has been revalidated and replayed as a new bundle. These finite results establish the stated construction and
counterexample; they do not change the open physical gates above.
