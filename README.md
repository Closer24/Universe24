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

The default `one_system()` has **48 cube-group reference channels and six
local message lanes**. An initial pulse travels between neighboring nodes and
drives a local receiver; nodes carry no shared cosmic clock. See the
[transport proof and protocol](docs/LOCAL_COMMUNICATION.md).
The previous 48-channel law remains available with `--model reference`. The former 382-channel variable-divisor assembly has been
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

The default seed declares six outgoing integer messages of payload three at
one origin, including their complete previous snapshots. The CLI also supports
the empty preparation; standing preparation requires `--model reference`.
Each run saves separate message and official-click logs. `--rewind` checks recovery of the
complete initial state; it is an audit, not part of the forward dynamics.
`--budget` may stop a run early, so inspect the completed horizon.

## What defines a run?

| Item | Current contract |
|---|---|
| Storage graph | Periodic cube with six face neighbors |
| Local state | Integer `(a,b,r)` per gear, with `0 <= r < 6` |
| Default gear types | 48 reference channels + 6 message lanes |
| Default coupling | 306 linear terms; actual tensor order two |
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
| [`layers/one.py`](universe24/layers/one.py) | Reference dynamics with local message reception |
| [`layers/communication.py`](universe24/layers/communication.py) | Six directed transport lanes and receiver wiring |
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

The [recurrent-burst audit](docs/RECURRENT_BURSTS.md) separates message
refocusing, reference-board reassembly and retained structural growth. Its
25 cases do not demonstrate stagnation-driven bursts with increasing
complexity. An exact periodic control reassembles ten times but repeats the
same structure; all tested histories rewind without information loss.
The [joint C2/cone audit](docs/CLICK_CAUSALITY.md) follows local messages into
later click classes and tests their relation to the measured structural growth.

## Verification

```bash
# Default construction and fixed-six regression fixtures
python -m unittest universe24.tests.test_communication universe24.tests.test_one universe24.tests.test_migration -v

# Complete discovery, with package context
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v

# Live tensor connectivity and support
python -m universe24.tools.system_inventory --out runs/system-inventory.json

# Export and replay the actual tensor, seed and event stream
python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
python -m universe24.tools.audit_contract --replay runs/contract
```

The previous 48-channel reference fixture still emits 75 official records in
20 updates and rewinds exactly. The communication default has a new tensor
and seed; [validation](docs/VALIDATION.md) records its separate results and
source provenance.

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
