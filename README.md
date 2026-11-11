# Universe24

Universe24 is a research project for testing whether exact local integer
dynamics can generate useful physical descriptions. Its active runtime uses
one scalar Rule3 operation with the **fixed divisor six**:

```python
quotient, remainder = divmod(2 * input_sum + remainder, 6)
previous, current = current, quotient - previous
```

A fixed local integer tensor supplies each input. A complete initial state
supplies both retained histories and every remainder. The forward loop never
replaces the tensor, injects signals, selects an outcome, or invokes an
observer to change a state.

The default `one_system()` is the **48-channel cube-group reference
construction**. The former 382-channel variable-divisor assembly has been
retired. This is a deliberate change of model; its old physical calibrations,
state hashes and long-run results are not claims about the new default.

This repository does **not** demonstrate general relativity, quantum
mechanics, particle physics or a law selecting maximum-complexity paths.
See [the algebra](docs/MODEL.md), [research status](docs/RESEARCH_STATUS.md)
and [the migration note](docs/DIVISOR_AUDIT.md).

## Install and run

Python 3.11 or newer:

```bash
git clone https://github.com/Closer24/Universe24.git
cd Universe24
python -m pip install '.[validation]'
python -m universe24 --L 3 --tmax 20 --budget 120 --out runs/demo --tag demo --rewind
```

The default seed is a declared local pulse of integer amplitude three. The CLI also supports a standing
preparation and the empty preparation. `--rewind` checks recovery of the
complete initial state; it is an audit, not part of the forward dynamics.
`--budget` may stop a run early, so inspect the completed horizon.

## What defines a run?

| Item | Current contract |
|---|---|
| Storage graph | Periodic cube with six face neighbors |
| Local state | Integer `(a,b,r)` per gear, with `0 <= r < 6` |
| Default gear types | 48 group-labelled reference channels |
| Default coupling | 288 linear terms; actual tensor order two |
| Scalar divisor | Constant six; no scale argument |
| Input law | Fixed integer polynomial of degree at most three |
| Tensor order | At most four, including the output index |
| Forward reads | One complete old snapshot |
| Inverse | Exact, with acyclic old-history dependencies |
| Observation | Passive official clicks and explicitly declared decoders |

The matrices and polynomial tensor entries define the couplings; they remain
fixed during a run. An effective link response can change through products
of evolving registers. That does not make the graph, metric interpretation
or quantum measurement behavior automatic.

## Code and research examples

| Location | Responsibility |
|---|---|
| [`core/engine.py`](universe24/core/engine.py) | Shared scalar evolution and exact inverse |
| [`core/tensor.py`](universe24/core/tensor.py) | Integer tensor, locality and dependency validation |
| [`algebra/`](universe24/algebra) | Cube rotations, quaternions and fixed group matrices |
| [`layers/one.py`](universe24/layers/one.py) | Fixed-six reference construction |
| [`prepare/`](universe24/prepare) | Complete initial states only |
| [`observe/`](universe24/observe) | Passive diagnostics and records |
| [`experiments/geometry/`](experiments/geometry/README.md) | Optional, separately declared constructions |

The [bounded-circuit example](docs/BOUNDED_CIRCUITS.md) proves routing and
periodic clocks on a prepared finite sector. The [integer reciprocal
examples](docs/INTEGER_RECIPROCAL_GEOMETRY.md) show exact coupled cycles and
explicit unbounded controls. Neither is a generic stability theorem.

The [local pp-wave experiment](docs/PPWAVE_PALATINI_LOCAL.md) embeds a chosen
vacuum geometry and records its boundary failures. Its [geodesic extension](docs/PPWAVE_OPERATIONAL_ROUTE.md)
encodes selected one-axis worldlines and calibrated time readouts. Those
coordinates stay inside a carrier node; no general packet propagation,
backreaction or universal operational metric has been established.

The separate [transported-probe experiment](docs/TRANSPORTED_PROBE_CLOCK.md)
uses 26 channels and one order-four tensor to carry a marker and two clocks
between board nodes. It passes a restricted axial comparison but explicitly
fails off-axis geodesic and proper-time tests; its common-metric gate is false.

## Verification

```bash
# Default construction and fixed-six regression fixtures
python -m unittest universe24.tests.test_one universe24.tests.test_migration -v

# Complete discovery, with package context
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v

# Live tensor connectivity and support
python -m universe24.tools.system_inventory --out runs/system-inventory.json

# Export and replay the actual tensor, seed and event stream
python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
python -m universe24.tools.audit_contract --replay runs/contract
```

The migrated full suite passes 118 tests. A size-three, 20-update default
run emits 75 official records and rewinds exactly; [validation](docs/VALIDATION.md)
records the scope and current tensor fingerprint.

A passing negative-control test records the failure of the associated
physical claim. It does not turn that claim into a successful result.
Fresh runs belong under `runs/`; [validation scope](docs/VALIDATION.md)
describes what the checks can establish.

## Historical results

The [pre-migration archive](docs/archive/pre-fixed-six/README.md) preserves
superseded notes, configurations and evidence. Their large-divisor presets
are unavailable in the active engine. They must be interpreted with the
corresponding version of the source, available in Git history, and must not
be silently replayed as fixed-six laws.

See [contribution rules](CONTRIBUTING.md) and the [research proposal](docs/RESEARCH_PROPOSAL.md).
