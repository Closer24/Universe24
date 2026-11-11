# Universe24 ONE

ONE is the sole active implementation in this repository. It is a research candidate for constructing observable events from exact, local, reversible integer dynamics. Its current default is **ONE v1**, built by `one_system()`.

Every gear uses the same scalar Rule3 recurrence. A fixed polynomial tensor supplies the input; the complete initial state supplies the seed. The forward loop never changes the tensor, injects a signal, selects a branch, or applies a click callback.

```python
ell, r_next = divmod(2 * u + r, D)
a_next, b_next = b, ell - a
```

This is an executable mathematical model, **not a demonstrated derivation of quantum mechanics or general relativity**. See [the algebra and limits](docs/MODEL.md) and [research status](docs/RESEARCH_STATUS.md).

The [system map and claim audit](docs/SYSTEM_MAP.md) explain the generic node, prove the inverse under its assumptions, list every module's role and show what actually communicates. The default tensor has six independent namespace groups; its present cosmic detector choices do not select different future clock trajectories under the declared preparation.

The optional [connected-clock research](docs/CLOCK_RESEARCH.md) adds reciprocal clock and record couplings as fixed tensor entries, with exact resolution lifting and unchanged Rule3. These are experimental builders, not the default law or established gravity/entanglement. Long runs also expose instability in the original default preparation; bounded shorter runs must not be extrapolated to arbitrary times or seeds.

A separate [bounded-circuit example](docs/BOUNDED_CIRCUITS.md) proves exact routing and periodic clocks for all time on a prepared Boolean invariant sector. It uses the same engine, but a different fixed tensor; its proof is not a stability theorem for the default field model.

The [geometry research](docs/GEOMETRY_RESEARCH.md) derives the clock/link reconstruction requirements and the missing Einstein constraints. Isolated [geometry experiments](experiments/geometry/README.md) include a restricted conformal clock construction, an invariant linear tensor-wave sector and exact counterexamples. They are research examples, kept outside the default runtime.

The optional [integer ADM implementation](docs/INTEGER_ADM.md) now computes the **full nonlinear 3+1 Einstein evolution equations**, a real scalar field, optional pressureless dark matter, and all four Einstein constraint readouts. General spatial variation and off-diagonal metric components are supported. The complete numerical trajectory is compiled before the run into a fixed rank-four integer tensor; the unchanged Rule3 Engine performs every update. The evolving metric determines the event-chart geometry, shared spatial links and local angles.

This is a numerical implementation with measured discretization/constraint errors and a finite compiled horizon. It does not assert exact equality to continuous spacetime, replace default ONE, couple all existing particle sectors, or identify every arithmetic click with an Einstein event. Dark matter here is an explicit pressureless, single-stream fluid in geodesic slicing, not an assumed particle discovery or a multistream halo simulation.

```bash
# Automatically prepare constrained scalar + dark-matter data, compile, run and rewind
python experiments/geometry/adm_integer.py --case dark --steps 2 --dt 1/128 --out runs/geometry/adm/dark

# General scalar geometry with a harmonic lapse; optional midpoint time integration
python experiments/geometry/adm_integer.py --case inhomogeneous --steps 1 --out runs/geometry/adm/scalar
python experiments/geometry/adm_integer.py --case massless --method midpoint --dt 1/16 --out runs/geometry/adm/midpoint

# Exact compilation, independent Einstein solutions, source feedback and constraint tests
python -m unittest universe24.tests.test_adm_integer -v
```

The automatic runner saves the tensor, a lossless journal of every retained `(a,b,r)` state, exact physical snapshots, geometry and error reports under `runs/`. This experimental compiler can use thousands of registers and large integers; the selected horizon and source assumptions are part of the configuration.

## Install and run

Python 3.11 or newer:

```bash
git clone https://github.com/Closer24/Universe24.git
cd Universe24
python -m pip install '.[validation]'
python -m universe24 --L 3 --tmax 20 --budget 120 --out runs/demo --tag demo --rewind
```

`--out` is required. The run writes diagnostics and hashes there. `--rewind` checks recovery of the complete seed after the forward run; it is an audit, not a stage of forward dynamics. Larger boards and longer runs can be expensive. `--budget` may stop a run early; inspect the reported completed horizon.

## What is fixed, and what is chosen?

| Item | Current default |
|---|---|
| Space | Periodic cube of side `L >= 3`; six face neighbors |
| Elementary state | Exact integer triple `(a, b, r)` per gear and node |
| Gear types per node | **382**; the 48-gear `2O` block is one part |
| Shared scale | `Q = 2**33 + 1`; divisor `D = 6*Q` |
| Input | One fixed integer polynomial tensor; degree at most 3 |
| Tensor census | 18,592 live monomials; 736 designated one-way terms |
| Default cosmic coupling | Block diagonal: package and cosmic block do not read one another |
| Dynamics fingerprint | `77f6d251a8adfb2e4727bd2bd5ffeaa0e2ae3538aac393fe95c497fce754acf6` |

The compatibility name `dynamics_fingerprint` hashes the indexed coefficient template, excluding Q. Identify the complete update law by this hash **together with Q**, or use the full tensor fingerprint for the default tensor, which records Q.

Choose the tensor configuration, board size and seed **before** a run. The seed then evolves deterministically. Reversibility retains the information underlying a coarse observed outcome; it does not erase alternate full states or prove a maximum-complexity selection law.

Optional builders are experiments within the same ONE engine. The coupled-doublet option is rejected because of observed runaway and is **off by default**. Einstein and CG2 constructions are also optional, not established properties of default ONE. The old standalone 48-channel implementation and its experiment trees are no longer present on the active branch; they remain in Git history.

## Code map

| Location | Responsibility |
|---|---|
| [`core/engine.py`](universe24/core/engine.py) | One exact forward engine and staged inverse |
| [`core/tensor.py`](universe24/core/tensor.py) | Polynomial input, locality and inverse-dependency validation |
| [`algebra/`](universe24/algebra) | Cube rotations, binary-octahedral group and fixed L0 matrices |
| [`layers/one.py`](universe24/layers/one.py) | Default complete ONE construction |
| [`layers/clock_network.py`](universe24/layers/clock_network.py), [`clock_bridge.py`](universe24/layers/clock_bridge.py) | Optional fixed reciprocal interactions and record feedback |
| [`layers/involution_clock.py`](universe24/layers/involution_clock.py) | Exact prepared-sector routing experiment |
| [`prepare/one.py`](universe24/prepare/one.py) | Initial data only |
| [`observe/`](universe24/observe) | Passive measurements and audit identities |
| [`demos/one/run_one.py`](universe24/demos/one/run_one.py) | Reproducible run and reporting |
| [`experiments/geometry/adm_integer.py`](experiments/geometry/adm_integer.py) | Optional complete ADM/scalar/dark-dust circuit, automatic preparation, geometry and full-state audit |
| [`tests/`](universe24/tests) | Exact arithmetic, locality, reversibility and scoped research tests |

## Verification

```bash
# Quick checks of the default construction and preserved state traces
python -m unittest universe24.tests.test_one universe24.tests.test_migration -v

# Complete suite, with package context for relative imports
GAUGE_LONG=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v

# Connectivity and block inventory derived from live tensor entries
python -m universe24.tools.system_inventory --out runs/system-inventory.json
```

Tests write fresh evidence to ignored `runs/tests/`. Checked-in `universe24/results/` and research notes are historical ONE experiment records, not a declaration that all physical targets passed. Some tests deliberately verify negative findings or failure of a physical hypothesis. A green suite means the stated assertions passed.

See [validation scope](docs/VALIDATION.md), [contribution rules](CONTRIBUTING.md), and [the research proposal](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit).

## Reproduce the optional clock research

```bash
# Autonomous candidate, explicit initial state, exact rewind
python -m universe24.tools.connected_clocks --L 3 --steps 1000 --out runs/connected/report.json

# Paired controls change only a declared initial source; the tensor stays fixed
python -m universe24.tools.connected_clocks --control forward --L 4 --steps 300 --out runs/connected/forward.json
python -m universe24.tools.connected_clocks --control reverse --L 3 --steps 1200 --out runs/connected/reverse.json
python -m universe24.tools.connected_clocks --control off --L 3 --steps 300 --out runs/connected/off.json

# Distinguish hand crossings, reader echoes and complete-state recurrence
python -m universe24.tools.clock_epochs --L 3 --steps 1000 --matter-divisor 16 --out runs/epochs/report.json

# Raw official-click clock ratios in prescribed backgrounds; includes failed physical criteria
python -m universe24.tools.metric_clock_gate --out runs/metric-clock-gate/report.json

# Exact finite-sector proof fixtures and replay of committed evidence
python -m unittest universe24.tests.test_involution_clock -v
```

Inspect the actual completed horizon, per-sector bounds, inverse result and physical acceptance fields. A successful command means the experiment ran; it does not turn a failed physical criterion into a pass. The metric-clock gate's faster clocks fail its declared universal-dilation tolerance even though all histories rewind exactly. The reference packet and long field runs also expose growing metric amplitudes.

## Tensor and click audit

See [the audit and measured limitations](docs/CLICK_CONTRACT_AUDIT.md). Export a complete tensor, seed and official event stream, then replay the saved inputs:

```bash
python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
python -m universe24.tools.audit_contract --replay runs/contract
```

All register reads are on-site or at a face neighbor. Including both endpoints of link gears, some terms span two lattice edges; the stricter single-physical-link condition is not satisfied. Official event counts are distinct from signed quotient weights.

An explicit [single-edge experiment](docs/SINGLE_EDGE_IMPLEMENTATION.md) adds 90 node mediators and meets the stronger condition with the same engine. It changes dynamics and requires a declared observation map; physical equivalence is unproved, so it is not the default. Run `python -m universe24.tools.physics_gate` to reproduce the electromagnetic readout comparison and the gravity-independent cosmic-clock control. Neither construction establishes Einstein spacetime; the board is the proposed substrate and clicks are its observable records.
