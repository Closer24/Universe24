# Universe24 — a three-dimensional event simulator

The simulator's field is named **Computational Field**; see the
[field naming contract](docs/FIELDS.md#field-name).

Canonical source: [Closer24/Universe24](https://github.com/Closer24/Universe24),
branch `main`. The Python package remains `event_universe`.

**Start here:** [AGENTS.md](AGENTS.md) contains the shared instructions, source of
truth and rule map, including the English-only repository language rule. This is
one project; active implementation lives only in `src/event_universe/`.

Agent workflow: [Boss and specialist skills](skills/boss-orchestrator/SKILL.md)
define task routing, independent checks and handoffs using the same project rules.

The package supports research into local fields and events, separating the engine,
candidate laws, measurements and tests. The baseline model is
`scalar-field-v10-contact`. It preserves the field and turning laws tested before
modularization. Start with `POSTULATES.md` for a plain-language explanation of
binding principles, candidate laws and open questions.

## Install and run

Python 3.11 or later is required. From the project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[render,dev]'
python -m event_universe --scenario contact --output artifacts/contact
```

On Windows, activate with `.venv\Scripts\activate`. Each application run creates:

| File | Contents |
| --- | --- |
| `run.html` | Standalone animation, view description and parameters |
| `run.gif` | Animation embedded in the HTML |
| `run.json` | Completion status, initial conditions, code identity and run checks |
| `events.jsonl` | Streamed movement, momentum-exchange and blocked-move events |

Other examples:

```bash
python -m event_universe --scenario turning --output artifacts/turning
python -m event_universe --scenario contact --view-3d --output artifacts/contact-3d
python -m event_universe --scenario stationary --frame-stride 4 --output artifacts/stationary
```

`--ticks` sets run duration. `--plane XY|XZ|YZ` and `--slice` select a displayed
slice; they do not change 3D physics. `--frame-stride` samples images without
skipping physical ticks.

Enhanced 1500×1275 3D is the default for every run, including test reports.
Use `--view-2d --plane XY --slice 12` for a slice. The full rule is in the
[definitions](SIMULATOR_DEFINITIONS.md#default-run-display).
Running into the same output directory replaces its results. Use separate
output directories to compare experiments.

## Check the project with one command

```bash
python tools/check.py
```

This checks lint, formatting, types and behavior and generates
`artifacts/test-runs.html` with every test world, including the frozen comparison.
Individual commands are also available:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pytest --junitxml=artifacts/junit.xml
```

Prefer `tools/check.py` for the full gate: it passes the current Python version
to mypy. GitHub Actions is configured in `.github/workflows/check.yml` for pushes
and pull requests. Local execution and testing do not require GitHub.

## Project map

| Path | Responsibility |
| --- | --- |
| `src/event_universe/core/state.py` | Fixed records, parameters and bounded integer arithmetic |
| `src/event_universe/core/contracts.py` | Local law and event interfaces |
| `src/event_universe/core/lattice.py` | Shared periodic addresses and neighbors for reading and moving |
| `src/event_universe/core/engine.py` | Sparse storage, time, neighbors, occupancy and cell movement |
| `src/event_universe/fields/scalar.py` | Generic scalar field and gradient |
| `src/event_universe/fields/policies.py` | Source, range and activity calculations selected by models |
| `src/event_universe/dynamics/turning.py` | Generic direction selection, remainders and momentum exchange |
| `src/event_universe/dynamics/movement.py` | Movement budget and neighbor-step selection |
| `src/event_universe/models/current_field.py` | Model choices and record adaptation |
| `src/event_universe/models/local_field.py` | Import compatibility without duplicated logic |
| `src/event_universe/diagnostics/` | Measurements, state audits, recording and HTML |
| `src/event_universe/scenarios.py` | Explicit initial conditions |
| `src/event_universe/runner.py` | Connect execution, recording and visualization |
| `tests/` | Unit, contract, regression and full-state comparison tests |
| `tests/reference/` | Frozen source used only for comparison |
| `POSTULATES.md` | Binding ideas in plain language |
| `SIMULATOR_DEFINITIONS.md` | Current precise requirements |
| `docs/ARCHITECTURE.md` | Responsibilities and update order |
| `docs/FIELDS.md` | How to replace a field or turning policy |
| `docs/PHYSICAL_FEATURES.md` | Required contract for a new physical feature |
| `docs/TEST_EXPECTATIONS.md` | Test responsibilities, inputs and exact expectations |
| `docs/MIGRATION.md` | Migrating older code and notebooks |

## Generic field, specific use

`ScalarField` calculates from six neighbor weights, a local weight and a supplied
source. `FieldTurning` receives a local vector and a response-selection function,
centralizing impulse arithmetic, remainders and momentum exchange. Neither
component knows a world or particle record.

`CurrentFieldModel` assembles the current occupancy source, nonnegative field and
dominant-axis transverse response. Replace components independently through
`Simulation(field=..., turning=...)`; see `docs/FIELDS.md`. The specific model is
tested in `tests/test_current_field.py`, alongside separate generic and integration tests.

## Preserved rules

- 3D physics with six cardinal neighbors.
- Integer physical state: five cell registers and twelve particle registers.
- Bounded registers and intermediate calculations; overflow raises an error.
- Bounded local work over six neighbors and K fixed cell slots.
- Persistent sources represented by occupancy; integer division residues retained.
- Local matter-field momentum exchange, without global correction.
- One speed law and at most one neighbor hop per tick.
- Measurements and animation do not feed back into the engine.

This is a discrete-model research framework. Field and turning laws are explicit
candidates. Software tests do not establish energy conservation or general physical
validity. Assumptions such as movement order and axis tie-breaking are documented
in the architecture guide.

## Local stretched-link candidate

```bash
PYTHONPATH=src python -m event_universe --scenario links --output artifacts/local-links --frame-stride 12
```

This selects `scalar-field-v11-local-links`: local six-port mailboxes, integer
lengths, symmetric edge proposals and frozen travel times. Dedicated tests are
`test_link_geometry.py`, `test_link_transport.py` and `test_linked_engine.py`.
The example uses base length 10 for a shorter replay; `LinkConfig()` defaults to
100. See `POSTULATES.md`, `SIMULATOR_DEFINITIONS.md` and `docs/ARCHITECTURE.md`.
Existing baseline scenarios keep their old behavior.

## Particle mass and elastic collisions

```python
from event_universe import Config, Simulation

world = Simulation(Config(source_strength=0), collisions=True)
world.add_particle(0, 14, 6, 6, px=6, mass=1)
world.add_particle(1, 18, 6, 6, px=-6, mass=2)
```

Run `python -m event_universe --scenario collision-masses --output artifacts/collision-masses`
for a saved 3D replay. `collision` demonstrates equal masses; `collision-links`
uses delayed local links. Mass defaults to 1; collisions are explicit opt-in to
preserve baseline comparisons. Momentum components have the integer denominator
`particle.momentum_den`. The exact law, timing and classical-model limits are in
the v13 section of SIMULATOR_DEFINITIONS.md.

The same option works with `event_universe.api.BalancedSimulation(collisions=True)`
to combine mass and contact handling with the current balanced movement and local
scalar halo. Existing balanced-halo tests remain part of the required gate.
