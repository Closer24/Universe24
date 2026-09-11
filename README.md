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

The initialization file is required. It supplies `ticks`; `--ticks` can override
duration. Missing input is an error, not a request to load a built-in universe.
Field definitions, disturbance types, seeds, formulas and cost settings are
documented with examples in [DISTURBANCES.md](docs/DISTURBANCES.md).

| Output | When written |
| --- | --- |
| `initialization.json` | Exact input file copied for reproducibility |
| `run.json` | Source identity, completion status and conservation diagnostics |
| `state.json` | Final resident state and in-flight transfers |
| `events.jsonl` | Streamed local-cycle and transfer events |
| Visual artifacts | Only when explicitly requested with `--visualize` |

Normal runs do not capture animation frames or import rendering libraries.
Visualization is read-only and does not change the physical update interval.
The active runner requires an empty output directory to preserve earlier evidence.
The display contract is in [definitions](SIMULATOR_DEFINITIONS.md#default-run-display).

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

| Path | Responsibility |
| --- | --- |
| `src/event_universe/initialization.py` | Strict JSON schema and typed expression compilation |
| `src/event_universe/core/disturbance_state.py` | Fixed generic definitions, records and positive payload codes |
| `src/event_universe/core/disturbance_engine.py` | Local scheduling, fixed transit, ownership and capacity |
| `src/event_universe/fields/disturbances.py` | Generic updates, paired exchange and transport proposals |
| `src/event_universe/disturbance_api.py` | Active generic Simulation assembly |
| `src/event_universe/api.py` | Explicitly named historical research APIs |
| `src/event_universe/core/engine.py` | Historical scalar-engine scheduling and occupancy |
| `src/event_universe/fields/`, `dynamics/`, `models/` | Generic arithmetic and retained candidate implementations |
| `src/event_universe/diagnostics/` | Read-only measurements, recording and optional output |
| `src/event_universe/scenarios.py` | Explicit historical research scenarios |
| `src/event_universe/runner.py` | Initialization-based execution and optional visualization |
| `src/event_universe/legacy_runner.py` | Explicit historical scenarios and optional recorded/live visualization |
| `examples/basic.json` | Complete example initialization; physical names occur only as data |
| `tests/` | Generic contracts, schema checks and retained research regressions |
| `tests/reference/` | Historical source archive, not an active engine |
| `docs/DISTURBANCES.md` | Authoritative generic schema, laws, timing and failure contract |
| `POSTULATES.md`, `SIMULATOR_DEFINITIONS.md` | Shared principles and scoped candidate requirements |
| `docs/ARCHITECTURE.md` | Ownership and dependency boundaries |
| `docs/FIELDS.md` | Active field definition and historical component extension |
| `docs/PHYSICAL_FEATURES.md` | Procedure for a new physical hypothesis |
| `docs/TEST_EXPECTATIONS.md` | Independent test inputs and expected outcomes |
| `docs/MIGRATION.md` | Transition from implicit scalar defaults |

## Generic field, specific use

Each configured disturbance type carries named scalar/vector fields together.
Choose whole-record movement for coupled attributes or extensive splitting for
divisible quantities. Conservation is a declared component-wise local balance,
including explicit sources and in-flight amounts. Coupling rules exchange a
shared field between local records atomically. See
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
