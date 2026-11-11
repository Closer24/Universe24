# Universe24

Universe24 runs discretized Einstein gravity, complex scalar matter with opposite U(1) charges, and cold pressureless dark matter on one event board. The default command prepares constraint-compatible data, compiles one fixed local integer tensor, evolves it through Rule3, and exports the evolving geometry and matter together.

The same tensor now also contains local message transport and its reference receiver. Components have disjoint named channel ranges, so their state cannot overlap. The default one-step model has 21 physical fields and 4,825 integer channels per node: 4,771 for Einstein arithmetic and 54 for communication. An explicitly selected 26-channel probe experiment has its own test chart and retains its failed general common-metric result. It never replaces the physical ADM metric or adds a gravitational source. See [system integration and channel ownership](docs/UNIFIED_SYSTEM.md).

The fundamental update remains exact and reversible:

```text
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

All updates read the same old state. Physical rational fields are retained integer numerator/denominator expressions. No external solver supplies future states during the run.

The compact route now has an **eight-channel sourced FLRW experiment**: a
homogeneous expanding geometry, three pressureless species and radiation,
with proper-time and null affine counters in the same fixed tensor. The
number of channels stays eight for any run length; integers can grow. It is
an exact prepared symmetry sector, **not a 48-channel replacement for general
ADM**. Run `python experiments/geometry/compact_flrw.py` and see
[the recurrence, clock meaning and limits](docs/COMPACT_FLRW_CLOCKS.md).
PR #34's separate [two-channel null-wave](docs/COMPACT_NULL_WAVE.md) compresses
another restricted geometry. These experiments do not become extra metrics
or matter sources in the default board.

A separate [compact sourced investigation](docs/TEAM48_RESEARCH.md) now fits
charged classical scalar matter, Maxwell fields and nonnegative normal dust
with one geometric frame into **41 integer channels**. The exact sign encoding
also compresses PR #39's 70-channel physical trajectory into 36. A separately
compiled **44-channel variant** preserves a nondegenerate frame on its stated
prepared domain, with an explicit temporal-mode limitation. These are
research candidates: constraint errors, metric validity and a general integer
refinement family remain explicit gates. Run
`python -m experiments.geometry.team48.candidate` for the actual allocation;
the default event board and its channel count are unchanged.
These encodings are proposals under the
[one-system, total-48-channel acceptance contract](https://github.com/Closer24/Universe24/issues/40),
not additional supported physical runtimes. The existing oversized default
also fails that new architecture's budget.

## Run the event board

```bash
python -m pip install .
python -m universe24 --steps 1 --out runs/universe24
# Open runs/universe24/board.html in a browser.

# Two physical steps at the same final time as the default one-step run:
python -m universe24 --steps 2 --dt 1/128 --out runs/universe24-fine

# Inspect allocation, or enforce a construction-time channel budget:
python -m universe24 --plan --max-channels 5000 --out runs/channel-plan
```

The default `--case universe` places both signs of scalar charge and positive dark density on a periodic 3×3×3 board, with a general non-diagonal metric. Initial constraints are solved before integer quantization. The Engine performs every evolution update; complete rewind and all arithmetic registers are verified automatically. Two steps retain much larger intermediate integers and take substantially more time and memory.

The board lets you select time, spatial slice and displayed field, then inspect any node's spacetime metric, stress-energy tensor and constraints. Every physical field links to the retained integer registers and microticks that computed it. The geometric lengths and angles follow from the same evolved metric. The drawing's pixel spacing is a layout, not a claim about curved physical distance.

Each selected event also displays the instantaneous proper-clock rate derived
from that same metric, for the hypersurface-normal observer and a stationary
grid observer. A null/spacelike grid tangent is identified explicitly. These
rates are chart dependent; they are not accumulated clock readings or a
gravitational-redshift calculation. In the default unit-lapse
chart, normal clocks tick at one even when curvature and matter are nonzero.
The default shift is nonzero, so fixed-grid clock rates differ from normal rates.

Other preparations: `--case matter`, `antimatter`, `dark`, `inhomogeneous`, `scalar`, `massless`, or `gauge`. `matter` and `antimatter` are charge-conjugate classical scalar preparations. `--method midpoint` selects the second-order time integrator. `--L` selects an odd periodic side length, at least three for constrained nonuniform data.

Add `--causal-wave` to see a local packet reach a detector, create an actual
C2 memory transition and drive a response field. The board includes a separate
microtick slider, causal-cone shading and retained triples on node selection.
This is an optional probe on the same Engine board, with no coupling to
Einstein stress-energy. Its computational cone is not the metric light cone;
the Einstein compiler's existing clocks remain. See [law, exact replay and
scope](docs/CAUSAL_WAVE.md).

## What is coupled

| Field | Dynamics and gravitational source |
| --- | --- |
| Spatial metric and extrinsic curvature | Full nonlinear ADM evolution, including all six independent components of each |
| Four Einstein constraints | Hamiltonian and three momentum constraints calculated at each physical snapshot |
| Complex scalar matter | Both real components obey curved-spacetime Klein–Gordon equations and contribute to the same stress-energy tensor |
| Opposite charge / antimatter sector | Complex conjugation reverses the U(1) current and preserves energy and gravitational coupling |
| Dark matter | Evolving, pressureless, normal-comoving dust in geodesic slicing |
| Cosmological constant | Supported by the construction API as a separate source parameter |

This is a classical Einstein–Klein–Gordon–dust model. It does not implement the quantum Standard Model, electromagnetic interactions or particle-antiparticle annihilation. Dark dust is single-stream and is valid before caustics. The fixed-six migration and its archived evidence are preserved. Retired Dirac/gauge calibrations remain unavailable; their names are not used to claim additional coupled matter.

All ten Einstein equations are represented in ADM form: six curvature evolution equations and four constraints; metric evolution defines extrinsic curvature. Constraint errors and charge-balance errors are measured. They are not silently projected to zero. Finite space/time discretization and seed quantization remain, even though integer evaluation of each chosen update is exact.

The current circuit has a finite horizon fixed at construction. It retains its workspace and past states; increasing `--steps` grows memory and integer sizes. Long-time and strong-field stability are not established. Exact computational rewind is not a claim of a time-symmetric numerical integrator.

## Output

- `board.html` and `event_board.json`: interactive physical-event board and register provenance.
- `official_events.jsonl.gz`: actual Engine official changed-triple clicks of physical numerator/denominator registers; computational workspace and clocks are audit records.
- `physical_N.json.gz`, `event_tensors_N.json.gz`: exact integer-pair fields, metric, independently computed stress and current at each physical snapshot.
- `geometry_N.json.gz`: shared spatial squared lengths and local angle data.
- `tensor.json`, `full_trace.jsonl.gz`, `report.json`: fixed law, lossless complete-state trace, errors and source hashes.
- `channels.json`: every channel's owner and each physical field's retained-register address.
- `component_events.jsonl.gz`: passive local message records and computational C0/C1/C2 counts, separate from physical readouts.

A physical mesh event and an individual integer arithmetic click are explicitly different levels of the same retained computation. A click is not a particle count. [Event mapping and matter conventions](docs/UNIVERSE24_EVENTS.md) and [all Einstein equations](docs/INTEGER_ADM.md) define the correspondence.

## Code map

| Path | Responsibility |
| --- | --- |
| `universe24/core/` | Unchanged Rule3 Engine, retained state and fixed local tensor |
| `universe24/core/channels.py` | Disjoint component allocation, complete seed assembly and read-only ports |
| `universe24/layers/universe.py` | Construct the single combined tensor and its explicit research components |
| `universe24/algebra/integer_circuit.py` | Compile rational arithmetic into clocked degree-three integer gates |
| `universe24/layers/adm.py` | Einstein, scalar, dust and gauge equations; fixed tensor construction |
| `universe24/prepare/einstein.py` | Initial data and constraint solve, before evolution |
| `universe24/runtime.py` | Main run, exact audit and trace export |
| `universe24/observe/event_board.py` | Passive event, matter and geometry display |
| `universe24/layers/reference_model.py` | Explicit 48-channel fixed-six reference control |
| `experiments/geometry/` | Benchmarks and compatibility entry points; production evolution lives in the package |

## Verification

```bash
python -m unittest universe24.tests.test_universe universe24.tests.test_adm_integer universe24.tests.test_migration -v
GAUGE_LONG=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v
python -m universe24 --L 3 --steps 1 --out runs/smoke --rewind
python -m universe24.tools.system_inventory --out runs/system-inventory.json
```

See [recorded integration checks](docs/evidence/universe24_integration.json) for the 0.4.0 fixed-six physical baseline.

The 0.5.0 consolidation of PRs #29–#31 is documented in [UNIFIED_SYSTEM.md](docs/UNIFIED_SYSTEM.md), with [fresh evidence](docs/evidence/universe24_unification.json). The earlier 0.4.0 record remains historical evidence for its pinned source. `--no-communication` selects the Einstein-only control; `--probe-experiment --L 5` includes the independent probe test in the same Engine.

The fixed-six 48-channel reference control remains independently reproducible:

```bash
python -m universe24.demos.reference_model.run_reference --L 3 --tmax 20 --budget 120 --out runs/reference-regression --tag smoke --rewind
```

Historical records retain their original names and timestamps where these are evidence metadata. Current code and entry points use Universe24. See [research status](docs/RESEARCH_STATUS.md), [model](docs/MODEL.md), [contribution rules](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).
