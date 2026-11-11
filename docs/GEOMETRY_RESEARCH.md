# From local clocks and links to a shared metric

## Integrated Einstein event board

The default is now `python -m universe24`: nonlinear ADM, complex scalar matter with opposite U(1) charges and geodesic dark dust. All updates use the fixed-six Engine; the metric, stress and event records come from the same retained state. See [equations](INTEGER_ADM.md), [events and matter conventions](UNIVERSE24_EVENTS.md), and [commands](../README.md).

The reference baseline and fixed-six research results below remain controls; they no longer describe the CLI default. Retired variable-divisor calibrations stay retired.


The scalar rule now has a fixed divisor of six. This arithmetic decision
removes a construction parameter; it does not by itself produce a physical
metric. A rank-four polynomial coupling tensor is not the spacetime metric
or the Riemann curvature tensor.

## Operational geometry

A candidate metric must make consistent predictions for independently
constructed clocks, signal travel and test-body trajectories. A local clock
readout defines a candidate proper-time interval only after its calibration
and robustness are established. A link delay or directional propagation speed
must be measured under a declared protocol, not inferred solely from a gear
name or a selected coefficient.

In an ordinary spacetime description,

    ds^2 = g_(mu,nu) dx^mu dx^nu.

Timelike curves and null curves must be identified by the same Lorentzian
metric. A positive spatial tensor alone does not supply lapse, shift, the
light cone or a four-dimensional causal structure. Fixed graph adjacency is
compatible with changing effective geometry, but the connection between link
states, clock behavior and geometry must be demonstrated.

Different clock species must agree without separately fitted scale factors.
The declared decoder must retain enough information to distinguish a stored
coordinate from an observable event and an algorithmic update count from
physical proper time.

## Field equations and constraints

Geodesic motion in a chosen metric does not prove that the metric has the
right dynamics. A gravitational construction must specify its source, show
local balance, preserve its constraints and recover the appropriate Einstein
limit under stated assumptions. A symmetric tensor or a reciprocal potential
is not enough to establish those properties.

Discretization requires particular care. Ordinary finite differences do not
obey every continuum product identity, and a local continuum action cannot
simply be copied into a tensor without checking locality and constraints.
See [the Palatini target](PALATINI_TARGET.md) and the
[constraint audit](DYNAMICAL_GEOMETRY_CONSTRAINTS.md).

## Current constructive examples

The [integer curl-wave example](LINEAR_SPIN2.md) supplies exact constrained
travelling sectors and a separate general instability control. It is a wave
building block, not an operational Einstein metric.

The [local pp-wave construction](PPWAVE_PALATINI_LOCAL.md) embeds a known
vacuum family as integer coframe and connection registers. Its centered
interior residuals vanish, but periodic transverse seams fail. Its original
uncoupled clocks do not respond to the assigned metric.

The [geodesic extension](PPWAVE_OPERATIONAL_ROUTE.md) couples four worldline
registers to that geometry. A prepared one-axis trajectory has exact continuum
geodesic and normalization identities, and a calibrated decoder uses actual
records. The trajectory stays inside one computational node. Its null/timelike
interpretation requires retained initial data that the official event stream
alone does not identify. It supplies neither moving board packets nor matter
backreaction.

The next useful test is therefore joint: an actual locally transported probe,
a clock built independently of that probe, and a geometry that predicts both
under one decoder and responds to a consistent source.

## Retired experiments

The former conformal-clock, phase-metric, link-probe and carry-lock presets
used the removed variable-divisor assembly. Their numerical ratios and
large-divisor stability estimates are archived with their original
assumptions. They are not silently converted to fixed-six claims. See
[the earlier geometry review](archive/pre-fixed-six/docs/GEOMETRY_RESEARCH.md)
for historical details and [the current experiment index](../experiments/geometry/README.md)
for executable work.

## Primary mathematical context

Palatini/coframe formulations motivate polynomial geometric variables;
[Derek K. Wise, *MacDowell–Mansouri Gravity and Cartan Geometry*](https://arxiv.org/pdf/gr-qc/0611154)
describes the continuum relationship. Constraint preservation after
discretization is a separate issue, discussed by
[Bahr and Dittrich](https://arxiv.org/pdf/0909.5688).
[Harte's plane-wave analysis](https://arxiv.org/pdf/1309.5020) provides the
known restricted continuum family used by the local examples. These sources
motivate targets; they do not establish the automaton's physical claims.
