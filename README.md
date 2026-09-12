# Universe24 — a three-dimensional event simulator

Canonical source: [Closer24/Universe24](https://github.com/Closer24/Universe24),
branch `main`. The Python package remains `event_universe`.

**Start here:** [AGENTS.md](AGENTS.md) contains the shared instructions and
English-only repository language rule. The active implementation lives in
`src/event_universe/`; [Boss and specialist skills](skills/boss-orchestrator/SKILL.md)
define coordinated work and independent checks.

The active simulator runs **initialization-defined disturbances**. A JSON file
defines field names and values, disturbance types, local updates, couplings,
transport, operation costs, normal cost and initial placements. The engine does
not recognize mass, charge or velocity by name or supply a hidden physical model.
Read [the disturbance contract](docs/DISTURBANCES.md) before defining a run.
Optional [native event programs](docs/NATIVE_QUANTUM_EVENTS.md) bind repeated
local quantum decisions to that same engine and charge the executed mechanical
path. They currently cannot be combined with spatial fields.

For a complete authoring walkthrough, use the
[simulation configuration Skill](skills/simulation-configuration/SKILL.md):
space, reusable entities, field laws, encounters, run commands and display options,
with a runnable two-stream template.

The optional [local reception observer](docs/LOCAL_OBSERVER.md) shows only
signals received at one selected node, with a local cycle counter and six
arrival directions, separately from the global world audit.

Explicitly named scalar, stretched-link, balanced-motion and causal-stream
research APIs remain available with their own historical laws and tests.
Their five-register cell and sixteen-register particle schemas are not the
generic disturbance schema.

## Project specification (Google Docs)

[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is the high-level project specification. Open it using a Google account with
document access. Repository access does not grant Google Docs access, and a clone
contains this link rather than a copy of the live document.

The document contains goals as well as requirements. Keep proposed behavior,
implemented contracts and tested results distinct. Consult
[project status](docs/PROJECT_STATUS.md#specifications-and-gaps),
[POSTULATES.md](POSTULATES.md) and
[SIMULATOR_DEFINITIONS.md](SIMULATOR_DEFINITIONS.md).

## AI-ready monorepo

Start with [AGENTS.md](AGENTS.md), the [status guide](docs/PROJECT_STATUS.md) and
[monorepo ownership](docs/ARCHITECTURE.md#monorepo-ownership). Load only the
contracts and skills needed for the task. Verify actual source and GitHub state
before integration; documentation is not evidence of the latest remote head.

## Install and run

Python 3.14 is the development and minimum runtime, recorded in
[.python-version](.python-version). Use a project environment. For headless runs
the package has no rendering dependency:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m event_universe --init examples/basic.json --output artifacts/basic
```

On Windows:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m event_universe --init examples/basic.json --output artifacts/basic
```

Select the environment's interpreter explicitly if activation is unavailable.
For development, install `python -m pip install -e '.[render,dev]'`; renderer
helper tests use the optional libraries even when no animation is generated.

Check a configuration without running a world:

```bash
python -m event_universe.configuration_validation examples/basic.json --json
```

See [configuration validation](docs/CONFIGURATION_VALIDATION.md) for catalog,
profile and observer files, explicit dependencies and the limits of a valid report.

The initialization file is required. It supplies `ticks`; `--ticks` can override
duration. Missing input is an error, not a request to load a built-in universe.
Field definitions, disturbance types, seeds, formulas and cost settings are
documented with examples in [DISTURBANCES.md](docs/DISTURBANCES.md).

Set the top-level initialization member `"boundary": "periodic"` for a closed
periodic domain: a transfer leaving one side arrives at the opposite side.
This is the default. Set `"boundary": "open"` for an absorbing edge: departing
disturbances and field packets leave the simulated world, with their escaped
quantities recorded separately. Both settings work with schema versions 1 and 2.
See [the boundary contract](docs/DISTURBANCES.md#domain-boundary) for geometry and
accounting. This setting is shared by carriers and fields.

For a moving source that continuously emits a separate conserved outward field:

```bash
python -m event_universe --init examples/moving_source.json --output artifacts/moving-source
```

For the schema 2 finite dissipative candidate, with bounded source allowances
and explicitly configured decay on each completed field link:

```bash
python -m event_universe --init examples/finite_fields.json --output artifacts/finite-fields
```

The [finite field contract](docs/SPATIAL_FIELDS.md#finite-completed-link-decay)
defines integer loss, immutable background and the extinction guarantee. Schema 1
keeps the conservative behavior. Neither schema is selected by physical names.

For configured field-driven rotation with an equal-and-opposite spatial reaction:

```bash
python -m event_universe --init examples/spatial_turning.json --output artifacts/spatial-turning
```

See [the coupling contract](docs/SPATIAL_COUPLINGS.md) for exact integer rotation,
fractional requests, value/flux sampling, timing and conservation limits.

For generic retained fields, coupled scalar/vector components and explicit
six-port outputs, use [LOCAL_FIELD_RULES.md](docs/LOCAL_FIELD_RULES.md) and
[local_field_rules.json](examples/local_field_rules.json). Schema 1 can combine
this opt-in local transport with existing outward fields. The same contract
defines atomic field/carrier transactions and guarded delayed commits. These
are configurable building blocks; the example does not claim electromagnetic
or quantum behavior.

For the physical field/particle inventory, matter and antimatter, and the exact
limits of classical support, see [PHYSICAL_ENTITIES.md](docs/PHYSICAL_ENTITIES.md)
and [the entity catalog](examples/known-entities/catalog.json). Compile selected
experiments using [the catalog and explicit profile guide](docs/ENTITY_CATALOG.md); generic
two-record conversion is described in [local conversions](docs/LOCAL_CONVERSIONS.md).
Compare selected behavior using the [small-space physics suite](examples/small-space/README.md).
The [local Maxwell experiment](examples/maxwell/README.md) tests a configured
reflection/streaming vacuum limit and records its Gauss and integer-lifetime gaps.
Emergence probes use elementary local vector operations; known continuum equations remain
external validation targets rather than supplied update formulas.

For opt-in exact fractional representation, balanced routing, massless transport
and joint-energy reference benchmarks, see [RATIONAL_PARTICLES.md](docs/RATIONAL_PARTICLES.md).
These examples test supplied mechanical contracts, not emergent physical laws.

Read [SPATIAL_FIELDS.md](docs/SPATIAL_FIELDS.md) for the baseline, eight-octant
transport through six faces, source cadence, cost accounting and self-field
limitations. The source moves every link interval while within its normal budget;
no two-tick movement interval is inserted automatically.

| Output | When written |
| --- | --- |
| `initialization.json` | Exact input file copied for reproducibility |
| `run.json` | Source identity, boundary, elapsed time, completion and quantity accounting |
| `state.json` | Final resident state and in-flight transfers |
| `events.jsonl` | Streamed local-cycle and transfer events |
| Visual artifacts | Only when explicitly requested with `--visualize` |

Normal runs do not capture animation frames or import rendering libraries.
Visualization is read-only and does not change the physical update interval.
Both active and historical runners require a new or empty output directory.
Generated output expires 24 hours after writing finishes; active writers remain
protected. Original initialization files and templates are preserved. See
[output retention](docs/RETENTION.md) for ownership and interrupted runs.
The reported `elapsed_seconds` includes world construction, simulation steps,
per-tick accounting, event writing and the final snapshot. Input parsing and final
artifact serialization are outside that timer. For a small open-boundary run, use
`--init examples/open_world.json`; its departing carrier is accounted as escaped.
The display contract is in [definitions](SIMULATOR_DEFINITIONS.md#default-run-display).

## Simulation configuration UI

Start the local workspace with the same installed Python environment:

```bash
python -m event_universe.ui
```

Open the printed local URL, normally `http://127.0.0.1:8765`. Choose a template,
edit the configuration, check it, and select **Run simulation**. Forms cover world
dimensions, duration, fields, disturbance types, seeds, rules and operation costs;
a complete JSON editor and import/export cover every initialization member.
Each run reads a saved JSON snapshot at runtime. Configuration changes require
no compilation, package rebuild, dependency installation or server restart.

The interface stays responsive while the runner executes in another process.
**Run & watch** records a movie with play/pause, timeline, speed and plane controls.
Prepared examples show approaching particles, parallel beams, a spreading
pulse and an unequal-mass elastic collision using configured laws. The collision
example uses generic atomic interactions and checks momentum and kinetic energy;
see [its contract](docs/DISTURBANCES.md#configured-unequal-mass-elastic-example).
Advanced settings start folded; the Names
tab updates particle/type and field references together. Disable recording for
a headless UI run; the CLI remains headless by default. Results include
conservation checks and links to the input, state and events. Use `--configs`
to select your own template folder, or `--port 0` to choose an available port.
See the [workspace guide](docs/WORKSPACE.md) for drafts, files and interruption.

The running workspace cleans expired outputs periodically and removes expired
result links. CLI runs also check for expired output at startup. To keep cleanup
running while both are idle, use a watcher or schedule the cleanup command:

```bash
python -m event_universe.retention --root artifacts --root runs --watch
```

Use `--dry-run` to inspect candidates without deletion. A stopped watcher or an
offline computer catches up on the next cleanup; see [retention](docs/RETENTION.md).

## Optional historical live display

The historical scalar/particle renderer supports an explicitly requested live
preview. This is separate from the active initialization-based runner's generic
disturbance view. Install the `render` extra before requesting historical output:

```bash
python -m pip install -e '.[render]'
python -m event_universe.legacy_runner --scenario contact --visualize --live --output artifacts/contact-live
```

This command prints the absolute `live.html` path at startup. Open that file in
a browser while the command is running; the page updates automatically each
second. It shows copied simulation snapshots as computation proceeds, then
updates from the frames being rendered for the recorded replay. At completion,
the page redirects to the standalone `run.html` animation. The final historical
output also includes `run.gif`. No web server or browser extension is required.

The live preview may skip intermediate snapshots and adjust its framing and color
scale as new data arrives. The final replay retains every frame selected by
`--frame-stride`, with the same fixed scale, quality and physics as before.
For short simulations, the first image may appear during replay export because
the physical calculation can finish before preview startup.

Omit `--live` for final visualization without a live preview; omit visualization
options for a headless run. Both features default off. Python callers opt in with
`legacy_runner.run_scenario(scenario, output, visualize=True, live=True)`.
Requesting `--live` or `live=True` also enables the recorded visualization.
Scripts that start live runs must call them inside an `if __name__ == "__main__":`
guard so the preview process can start safely on Windows. A preview fault is
reported and does not cancel the physical calculation or its recorded output.

## Run performance

Reuse the installed environment for later runs; dependency installation is a
one-time setup step. Ordinary runs capture no animation frames. When historical
visualization is explicitly requested, stride 1 captures every tick and the 3D
renderer exports enhanced 1500x1275 HTML and GIF. It draws each default frame once
and encodes the stopped GIF once; the runner captures only the selected view.

For a quicker, explicitly sampled preview of a long run, use the existing option:

```bash
python -m event_universe.legacy_runner --scenario contact --visualize --frame-stride 4 --output artifacts/contact-preview
```

This still computes and checks every physical tick and records every event.
It saves fewer display frames, so intermediate movement is visible in the event
trace rather than in the animation. Use stride 1 for consecutive-tick inspection.
See [performance measurements](docs/PERFORMANCE.md) for the measured case and limits.

## Check the project with one command

```bash
python tools/check.py
```

This runs lint, formatting, strict types and behavioral tests. Standard tests are
headless. Physical assertions remain active; presentation-only tests are skipped
unless visual checks are explicitly requested:

```bash
python -m pytest --visualize-runs
```

That option enables frame capture, the historical HTML renderer and relevant
presentation checks. Do not enable it merely because a simulation test runs.
On Windows, `PYTHONUTF8=1` provides consistent UTF-8 handling for the check tools.
Current results belong in identified validation evidence, not an assumed pass
from this README.

## Project map

The [documentation index](docs/README.md) assigns one owner per topic and separates
active contracts, explicit experiments and revision-specific evidence.


| Path | Responsibility |
| --- | --- |
| `src/event_universe/initialization.py` | Strict JSON schema and typed expression parsing |
| `src/event_universe/core/disturbance_state.py` | Fixed generic definitions, records and positive payload codes |
| `src/event_universe/core/disturbance_engine.py` | Local scheduling, fixed transit, ownership and capacity |
| `src/event_universe/core/topology.py` | Shared six-port periodic/open neighbor geometry for the generic simulator |
| `src/event_universe/fields/disturbances.py` | Generic updates, paired exchange and transport proposals |
| `src/event_universe/disturbance_api.py` | Active generic Simulation assembly |
| `src/event_universe/particle_api.py` | Explicitly named historical research APIs |
| `src/event_universe/core/scalar_engine.py` | Historical scalar-engine scheduling and occupancy |
| `src/event_universe/fields/`, `dynamics/`, `models/` | Generic arithmetic and retained candidate implementations |
| `src/event_universe/diagnostics/` | Read-only measurements, recording and optional output |
| `src/event_universe/particle_scenarios.py` | Explicit historical research scenarios |
| `src/event_universe/runner.py` | Initialization-based execution and optional visualization |
| `src/event_universe/ui.py`, `ui_assets/` | Local configuration workspace, templates and isolated CLI jobs |
| `src/event_universe/legacy_runner.py` | Explicit historical scenarios and optional recorded/live visualization |
| `src/event_universe/retention.py`, `docs/RETENTION.md` | Registered output ownership, active writer protection and 24-hour cleanup |
| `examples/basic.json` | Complete example initialization; physical names occur only as data |
| `examples/finite_fields.json` | Schema 2 finite emission, completed-link decay and explicit background |
| `tests/` | Generic contracts, schema checks and retained research regressions |
| `tests/reference/` | Historical source archive, not an active engine |
| `docs/DISTURBANCES.md` | Authoritative generic schema, laws, timing and failure contract |
| `docs/LOCAL_FIELD_RULES.md` | Local retained/output rules, component groups and joint field/carrier transactions |
| `POSTULATES.md`, `SIMULATOR_DEFINITIONS.md` | Shared principles and scoped candidate requirements |
| `docs/ARCHITECTURE.md` | Ownership and dependency boundaries |
| `docs/SCALAR_FIELDS.md` | Historical scalar field composition and turning |
| `docs/PHYSICAL_FEATURES.md` | Procedure for a new physical hypothesis |
| `docs/TEST_EXPECTATIONS.md` | Independent test inputs and expected outcomes |
| `docs/MIGRATION.md` | Transition from implicit scalar defaults |

## Generic field, specific use

Each configured disturbance type carries named scalar/vector fields together.
Choose whole-record movement for coupled attributes or extensive splitting for
divisible quantities. Conservation is a declared component-wise local balance,
including explicit sources and in-flight amounts. Schema 2 explicitly subtracts
committed dissipation; its finite allowances are separate from inventory.
Coupling rules exchange a shared field between local records atomically. See
[DISTURBANCES.md](docs/DISTURBANCES.md).

Local operation costs set a uniform delay before transfer. Ordinary cost adds no
extra wait; excess cost stretches the local cycle. Neighbor transit time remains
fixed, and no computation debt accumulates between cycles.

## Preserved rules

- Three dimensions and six causal neighbor links.
- Bounded integer payloads, arithmetic and fixed local storage.
- Explicit ownership during local waits and transit.
- Local conservation checks, with no global physical correction.
- Read-only measurements and visualization.
- Named hypotheses and independent tests; no claim that a successful run proves
  gravity, waves, energy conservation or other emergent physics.

## Local stretched-link candidate

`LinkedSimulation` is a historical research API with variable link lengths.
It does not supply the active disturbance engine's timing law.
An explicitly selected historical CLI example is:

```bash
python -m event_universe.legacy_runner --scenario links --output artifacts/local-links
```

This remains headless unless visualization is requested. Its model laws are
scoped in [definitions](SIMULATOR_DEFINITIONS.md) and the architecture guide.

## Particle mass and elastic collisions

Hardcoded mass and elastic-contact behavior belongs to `ScalarSimulation`,
not the generic `Simulation`:

```python
from event_universe import Config, ScalarSimulation

world = ScalarSimulation(Config(source_strength=0), collisions=True)
world.add_particle(0, 14, 6, 6, px=6, mass=1)
world.add_particle(1, 18, 6, 6, px=-6, mass=2)
```

`BalancedSimulation` and `CausalStreamSimulation` likewise select explicit
research laws. See [migration](docs/MIGRATION.md) and their candidate contracts.

## Standalone generic vector lab

The opt-in [vector lab](tools/generic_vector_lab/README.md) contains externally
configured N-to-M node reactions, bounded rational vector arithmetic and exact
conservation tests. It is an independent experiment, not the active simulator.
Run `python -m tools.generic_vector_lab.run_demo` from this repository.
