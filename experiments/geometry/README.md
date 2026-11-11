# Geometry experiments and controls

These are optional, reproducible experiments. They do not modify the default
ONE tensor, `Engine.step`, the click definition, or a running state. A declared
tensor and complete integer seed are fixed before each run; observations are
passive. Outputs go under ignored `runs/` by default.

## Restricted conformal construction

The two conformal scripts choose a **new** four-gear reciprocal rank-four
tensor. They are not tests asserting that the default tensor already realizes
a spacetime metric. The scalar conformal factor is updated through the same
Rule3 as the matter and signal gears, including its reciprocal source.

From the repository root:

```bash
PYTHONPATH=. python experiments/geometry/conformal_metric_probe.py
PYTHONPATH=. python experiments/geometry/conformal_nonlinear_clock.py
```

Each command runs two initial backgrounds at each declared refinement
`N=8,16,32,64`: eight forward histories and eight complete inverse histories.
Use `--refinements 8 16` for a subset, or `--out runs/geometry/custom.json` for
a different report path. Refinements define separate fixed preparations;
coefficients and normalization never change during a run.

The independent-clock experiment measures signed **official quotient**
crossings for two scalar clocks. It checks the complete massless canonical
signal history across backgrounds, positive conformal factor at every update,
strict local support, reciprocity, and exact rewind. The nonlinear experiment
adds a reciprocal quartic interaction and compares the same fixed official
readout at the analytically determined update pairing `n` and `2n-1`.
It reports exact error fractions and a bound on the mismatch from nominal
constant-background proper time. Neither decoder fits a time shift or uses
board values as replacement samples; raw quotient equality is a separate
audit. Missing click rows retain their zero-valued time slots.

Results include source, tensor, seed, final-state and trace hashes. Published
evidence is [conformal_metric.json](../../docs/evidence/conformal_metric.json)
and [conformal_nonlinear_clock.json](../../docs/evidence/conformal_nonlinear_clock.json).
The [algebra and finite-time proof](../../docs/CONFORMAL_METRIC_EXPERIMENT.md)
explain the normalization, positive scalar kinetic sign, rounding bounds and
second-order clock comparison.

The interpretation is restricted to conformally coupled scalars in a
controlled temporal-continuum and weak-probe limit. `L=3` is fixed: this is
not a spatial continuum convergence test. Canonical signal equality is not
an executed emitter-to-receiver redshift experiment. The conformal ansatz is
not general Einstein geometry, cannot produce generic Weyl curvature, and
does not derive particles or quantum statistics. Finite histories and the
conditional finite-time estimate do not prove all-seed, all-time stability.

## Independent checks and obstructions

The separate [integer curl-wave experiment](../../docs/LINEAR_SPIN2.md) uses
18 gears and a reciprocal linear tensor. It proves bounded propagation and
exact constraints for prepared travelling profiles and checks all 24 proper
cube rotations. Its general three-dimensional instability control remains
explicit. Run `python experiments/geometry/linear_spin2_check.py`; the checked
record is [linear_spin2.json](../../docs/evidence/linear_spin2.json). It supplies
a linear tensor-wave building block, not a measured Einstein metric.

These scripts test narrower existing or proposed algebraic claims. Their
definitions and limitations are recorded in the linked research notes.

| Script | What it checks | Explanation |
|---|---|---|
| `linear_spin2_check.py` | Exact bounded integer travelling profiles, TT constraints, cube rotations and a separate three-dimensional instability control | [Integer curl waves](../../docs/LINEAR_SPIN2.md) |
| `retimed_tensor_wave.py` | Exact bounded two-bank translation at half a coarse site per update; a separate unprepared growth control | [Retiming control](../../docs/LINEAR_SPIN2.md#8-separate-exact-retiming-control) |
| `link_metric_check.py` | Local reciprocal clock/link coefficients and operational metric conditions | [Geometry research](../../docs/GEOMETRY_RESEARCH.md) |
| `metric_obstruction_check.py` | An exact invisibility control and source defect for a proposed Einstein extension | [Geometry research](../../docs/GEOMETRY_RESEARCH.md) |
| `planar_tt_sector.py` | Preserved linear trace/divergence constraints on a prepared planar vacuum sector; audit-only activity | [Geometry research](../../docs/GEOMETRY_RESEARCH.md) |
| `phase_metric_probe.py` | Local metric polynomial and actual official one-way probe response; unequal speeds retained | [Local metric experiment](../../docs/PHASE_METRIC_EXPERIMENT.md) |
| `linear_metric_reconstruction.py` | Exact linearized lattice Ricci tensor and constraints for the prepared travelling metric | [Local metric experiment](../../docs/PHASE_METRIC_EXPERIMENT.md) |
| `carry_locked_metric.py` | Exact two-sublattice reduction, long finite carry-locked drift and complete reversal | [Metric-source audit](../../docs/METRIC_SOURCE_AUDIT.md) |
| `palatini_constraint_checks.py` | Declared Palatini constraint targets and explicit algebraic controls | [Palatini target](../../docs/PALATINI_TARGET.md) |

```bash
python experiments/geometry/linear_spin2_check.py
python experiments/geometry/retimed_tensor_wave.py
python experiments/geometry/link_metric_check.py
python experiments/geometry/metric_obstruction_check.py
python experiments/geometry/planar_tt_sector.py
python experiments/geometry/phase_metric_probe.py
python experiments/geometry/linear_metric_reconstruction.py
python experiments/geometry/carry_locked_metric.py --steps 1000000
python experiments/geometry/palatini_constraint_checks.py
```

The carry-locked example is a fast checkerboard preparation of a different
stencil. It exposes a limit of a remainder-free stability inference; it is
not a no-go theorem for the separately controlled smooth conformal limit.
Constraint checks define research targets and counterexamples, not a
completed derivation of the Einstein equations.
