# Fixed-six geometry experiments and controls

These optional constructions use the shared scalar engine with the fixed
divisor six. Each run declares a fixed integer tensor and complete seed before
its first update. Observations are passive. They are separate mathematical
examples, not assertions that the default reference tensor already produces
physical gravity.

## Active experiments

Run from the repository root:

| Command | What it tests | Derivation |
|---|---|---|
| `python experiments/geometry/reciprocal_metric_candidate.py` | Prepared coupled integer clock cycles and unbounded controls | [Integer reciprocal examples](../../docs/INTEGER_RECIPROCAL_GEOMETRY.md) |
| `python experiments/geometry/metric_transport_candidate.py` | Local tensor/flux response and explicit failed geometric criteria | [Integer reciprocal examples](../../docs/INTEGER_RECIPROCAL_GEOMETRY.md) |
| `python experiments/geometry/exact_constraint_audit.py` | Exact source and constraint obstructions | [Constraint analysis](../../docs/DYNAMICAL_GEOMETRY_CONSTRAINTS.md) |
| `python experiments/geometry/linear_spin2_check.py` | Prepared constrained travelling waves and general instability | [Integer curl waves](../../docs/LINEAR_SPIN2.md) |
| `python experiments/geometry/retimed_tensor_wave.py` | Two-bank half-speed translation and off-preparation growth | [Retiming proof](../../docs/LINEAR_SPIN2.md#8-separate-exact-retiming-control) |
| `python experiments/geometry/palatini_constraint_checks.py` | Palatini polynomial targets and exact failure controls | [Palatini target](../../docs/PALATINI_TARGET.md) |
| `python experiments/geometry/ppwave_palatini_local.py` | Known vacuum coframe/connection family, interior success and seam failure | [Local pp-wave algebra](../../docs/PPWAVE_PALATINI_LOCAL.md) |
| `python experiments/geometry/ppwave_geodesic_clock.py` | A chosen one-axis worldline with a calibrated event decoder | [Geodesic proof](../../docs/PPWAVE_OPERATIONAL_ROUTE.md) |
| `python experiments/geometry/ppwave_geodesic_audit.py` | Independent symbolic metric/geodesic audit; requires SymPy | [Geodesic proof](../../docs/PPWAVE_OPERATIONAL_ROUTE.md) |

The passive `linear_metric_reconstruction.py` checks a declared linearized
geometry; it does not advance a new runtime law. The optional
`plot_geodesic_clock.py` displays checked records using Matplotlib. Floating
arithmetic in a plot is separate from the exact integer evolution.

Fresh output goes under ignored `runs/` by default. Checked evidence is under
[`docs/evidence`](../../docs/evidence); use the records associated with the
current source, not old files with a different divisor or tensor. The migration
comparison is [fixed_six_experiment_migration.json](../../docs/evidence/fixed_six_experiment_migration.json).

## Scope of the pp-wave examples

The local Palatini example has 48 integer registers. Actual Rule3 steps
transport its prepared coframe and connection, and the declared interior
residuals vanish. The transverse periodic seams fail. Its uncoupled clocks
do not respond to the metric.

The follow-up keeps 48 registers and uses an order-four tensor to drive four
worldline registers from the geometric state. Its selected trajectory has an
exact continuum geodesic interpretation and a prepared-sector decoder from
actual official records. Those coordinates remain inside one carrier node.
There is no transported board packet, universal clock apparatus or matter
backreaction, and different norm sectors can share the same official records.

## Retired presets

The former `conformal_metric_probe`, `conformal_nonlinear_clock`,
`phase_metric_probe`, `link_metric_check`, `carry_locked_metric`,
`planar_tt_sector`, and `metric_obstruction_check` runners depended on the
removed variable-divisor field assembly. Their entrypoints now state that
retirement instead of silently running an altered model. Old convergence,
clock-rate and long-run evidence stays in the
[historical archive](../../docs/archive/pre-fixed-six/README.md).

A replacement needs an explicit fixed-six integer tensor, complete seed and
new validation. Renaming a scale, rounding a coefficient or preserving a plot
does not establish that replacement. The [geometry requirements](../../docs/GEOMETRY_RESEARCH.md)
state the physical targets still to be met.
