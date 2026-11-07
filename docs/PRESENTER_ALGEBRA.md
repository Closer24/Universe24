# The Presenter: clocks, gears and exact algebra

The Presenter uses one visual language for complete recorded experiments of the
current Universe24 reference model. The pictures are functions of the recorded
state and fixed tensor. An experiment name, a guide shape, a particular channel
or an expected outcome does not define a drawing rule.

A clock hand helps a reader see how two counters change together. A remainder
gear helps a reader see division and retained information. Neither picture
introduces a mechanical law or proves that a physical clock, gear, photon or
particle exists. The forward dynamics remain the Rule3 law in [MODEL.md](MODEL.md).

## Three scales of inspection

| View | What is represented | What must remain accessible |
|---|---|---|
| Space | Positions in the periodic cube, with counter activity and remainder-only changes distinguished | Any valid position, including a position whose channels all equal the background; the number of nodes hidden by the chosen filter or slice |
| Node | All 48 channel states at the selected position | Every channel index 0 through 47, including channels equal to the background |
| Channel | The selected exact `(a,b,r)` and, when history exists, its completed scalar transition | All six signed neighboring contributions from the previous snapshot, their spatial addresses and channel indices, the quotient and the next triple |

The background is part of the full representation. A missing sparse entry means
exactly that background triple; it does not mean an unknown value, a removed
channel or a missing spatial port. In particular, `(a,b)=(0,0)` can coexist with
a nonbackground remainder. Such a channel has no moving counter hand but still
retains microscopic information. Hiding it in a counter-only view must not
remove it from transition checks, recorded readouts or saved states.

Spatial projection, camera orientation, slicing and channel selection change
what the reader inspects. They do not change the preparation, tensor, recorded
trajectory or experiment-defined observers. Periodic wrapping remains part of
the algebra even when the visual camera shows a flat slice.

## What a counter dial means

For an exact pair `(a,b)`, the dial points in the direction of that vector:
`a` points right and `b` points up. For `(0,0)` it is marked at rest and has no
inferred direction. The step index must never be substituted for the observed
counter phase.

Normalizing the hand length deliberately removes amplitude from the picture:
`(1,1)` and `(1000,1000)` point the same way. The exact signed values must
therefore remain available alongside the dial. A displayed revolution is not a
unit of physical time or a proof of periodicity. A nonperiodic trajectory can
also be drawn as successive counter directions.

The portable representation stores counters as canonical decimal strings. The
browser performs arithmetic with `BigInt`, preserving negative and arbitrarily
large integer values within its explicit resource limits. Conversion to a
finite graphical direction is an approximation used only for drawing. It must
not feed into sums, quotients, state comparisons, hashes or readouts. This
separation prevents a large integer from becoming `Infinity`, a rounded
counter or a false equality during scientific inspection.

## Six neighboring contributions, one old snapshot

Let the selected receiver have address `(x,g)`. For direction `d`, the recorded
fixed tensor specifies a sender channel `h=P[d,g]` and sign `w[d,g]`. Its input is

```text
u[x,g] = sum over the six directions d of
         w[d,g] * b_old[(x+d) mod L, P[d,g]].
```

All six values are read from the same complete old frame. They are not taken
from whichever neighbor happens to be selected in the interface or from a
partially updated board. Clicking an input neighbor may navigate to that
address, but cannot change the original recorded connection.

A negative sign reverses that contribution to the sum. It does not delete a
port. Likewise, `u=0` does not imply that all neighbors are inactive: positive
and negative contributions can cancel. Showing the six signed products makes
that distinction inspectable.

When the selected saved frame is at step `t`, its incoming transition is from
`t-1` to `t`. The current triple belongs to `t`; the displayed old triple and
all input counters belong to `t-1`. A first loaded frame, even a checkpoint
labelled step 100, has no observed predecessor in that loaded record. It is a
snapshot, not an audited incoming transition.

## The six-position remainder gear

For the selected old triple and exact input sum, Rule3 is

```text
n = 2*u + r
ell = floor(n / 6)
r_next = n - 6*ell,       with 0 <= r_next < 6

a_next = b
b_next = ell - a.
```

Equivalently, the gear identity is

```text
2*u + r = 6*ell + r_next.
```

A six-position wheel displays `r`. The unwrapped arithmetic displacement `2u`
produces signed whole turns `ell` and the new remainder. The quotient can be
much larger than one, and a wheel position alone cannot show it. The exact
quotient, counter transfer `a_next=b`, and subtraction `b_next=ell-a` therefore
belong in the selected-channel explanation.

Negative input requires Euclidean division, not truncation toward zero. For
example, old `(a,b,r)=(3,2,0)` and `u=-1` give

```text
n = -2 = 6*(-1) + 4
ell = -1, r_next = 4
(a_next,b_next,r_next) = (2,-4,4).
```

In JavaScript, integer `/` truncates toward zero and `%` can return a negative
remainder. The arithmetic implementation must correct those operations to
match the displayed floor and the range `0..5`. The visual representation does
not supply an alternative rounding rule.

## The three-position gear and retained parity

Reduce `2u+r=6ell+r_next` modulo two. It follows exactly that

```text
epsilon_next = epsilon,       epsilon = r mod 2.
```

Writing `r=2theta+epsilon`, with `theta` in `0,1,2`, gives

```text
u + theta = 3*ell + theta_next.
```

Thus a three-position `theta` wheel plus the invariant bit `epsilon` is a
lossless alternative representation of the six-position remainder. Neither
part can be discarded: a phase wheel without the parity bit is an incomplete
state description. This identity holds for every valid scalar transition; it
is independent of the example being displayed.

## A dial is not a universal oscillator

If the actual net input remains zero, then `ell=0`, the remainder stays fixed,
and the counter pair follows

```text
(a,b) -> (b,-a) -> (-a,-b) -> (-b,a) -> (a,b).
```

This is an exact conditional period-four identity. A nonzero integer pair has
period exactly four under that zero-input map; the zero pair is fixed. Incoming
nonzero sums can change this behavior. A four-step local projection also does
not prove recurrence of the whole board, whose other counters and remainders
remain part of its state.

If **every** counter in a complete preparation is zero, all input sums are zero
and `divmod(r,6)=(0,r)`. The whole preparation is therefore fixed for any allowed
remainder field and fixed tensor. This proves a useful source-free control
condition. It does not prove that every nonzero preparation needs an external
source, that a propagated influence is physical light, or that a clock receives
continuous power after it starts.

## Arithmetic events and experiment readouts

The existing arithmetic event classification is a passive function of a
completed transition. It records a class only when `ell != 0` and the local
triple changed. The class index is the Euclidean residue `u mod 3`, giving
`C0`, `C1` or `C2`. A negative JavaScript remainder must again be normalized.
The absence of an arithmetic event does not imply an unchanged full state.

An optional experiment readout is separately declared in the imported data.
For example, an `all_equal` readout is a conjunction of exact values of named
counter or remainder components at specified addresses. The Presenter applies
that same predicate at each recorded step. A rising edge requires a false
value in the preceding loaded frame and a true value in the current one. A
readout already true in the first frame has a value, but no observed incoming
edge.

These readouts are data, not viewer-specific detector code. Moving the camera
or selecting another channel must not relocate a readout, change its predicate
or choose a more favorable event definition. A readout imported after a run can
be evaluated reproducibly, but the viewer cannot establish that it was
preregistered before the experiment. That timing belongs to the research
protocol and provenance, not to the rendering software.

A readout becoming false is not information erasure. Hidden remainders and
other channels remain in the full state. No arithmetic class or recorded edge
by itself establishes quantum collapse, an exclusive detector outcome or a
physical measurement law.

## State identity, history and scope

`state_sha256` identifies the canonical complete sparse representation
`{side,background,cells}`. It excludes the update index, camera, selection,
readout labels and view filters. Within a fixed representation convention, a
stationary configuration therefore has the same state digest at different
recorded steps. Hashes are useful identity checks; full-state transition
validation checks the actual retained values.

The coupling has a separate fingerprint. The same state data can be prepared
under different tensors, so its state digest alone does not identify the
experiment or the dynamical candidate. Record the fixed coupling, source code,
preparation and time range as well. Different sparse background conventions
also require explicit normalization before comparing representations across
experiments.

A complete sequence of consecutive frames can be checked against the exact
law and its inverse. A single full checkpoint can be displayed and inspected,
but supplies no transition history or period certificate. The Presenter must
not fabricate intermediate states when only a snapshot was supplied.

Generic means that every valid experiment using the current reference
geometry, channel state and supported fixed tensor format uses the same
rendering code. It does not mean unlimited memory, unlimited file size or
support for an undeclared model revision. Geometry and step indices must be
representable exactly in the browser; counter sizes, frame counts and retained
support are subject to explicit resource limits. Exceeding a limit must produce
an error rather than silently omitting channels or accepting an incomplete
trajectory. The current reference catalog contains all eight body-sign choices
of its fixed six-port coupling construction.

Exact algebra and faithful visualization establish what the recorded model
did. They do not establish that the model describes nature. The viewer is a
research instrument for making that distinction easier to inspect.
