# Universe24 — a three-dimensional event simulator

Universe24 implements **Reality Theory (Universe24)**: one discrete world of
Nodes and Links, bounded integer arithmetic and local rules; the Detector is a
marked Node and a pair's outcome travels on the returning ray
([Highlights](docs/HIGHLIGHTS.md) sections 3.19 and 3.20); since 2026-09-18
the law of the bit (section 5.4) is the model: every ray is a thing or its
shadow, a mark absorbs things and returns shadows, and nothing draws. The
name of the
framework is Reality Theory; the simulator that realizes it is Universe24.

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
The shared quantum resource and its integration layer were deleted on
2026-09-17 ([migration](docs/MIGRATION.md#shared-quantum-resource-and-integration-layer-deleted-on-2026-09-17)).
The named-particle gallery (`examples/gallery/`, deleted on 2026-09-17) renders recorded
electron and positron runs as three-dimensional animations.

For a complete authoring walkthrough, use the
[simulation configuration Skill](skills/simulation-configuration/SKILL.md):
space, reusable entities, field laws, encounters, run commands and display options,
with a runnable two-stream template.

The optional [local reception observer](docs/LOCAL_OBSERVER.md) shows only
signals received at one selected node, with a local cycle counter and six
arrival directions, separately from the global world audit.

Explicitly named scalar, stretched-link, balanced-motion and causal-stream
research APIs remain available with their own historical laws and tests.
Their five-register node and sixteen-register particle schemas are not the
generic disturbance schema.

## Project specification (Google Docs)

[docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) is the Universe 24 Highlights
specification, the high-level project specification, edited directly since
2026-09-17 by the model owner's decision. The Google Doc
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is its historical source up to the revision of 2026-09-16 and is neither
edited nor resynced. Opening it requires a Google account with document
access; repository access does not grant Google Docs access.

The specification contains goals as well as requirements. Keep proposed behavior,
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

[Local Focus](docs/LOCAL_FOCUS.md) is enabled by default: identical pure local
planning inputs share their calculated result, and certified empty carrier Nodes
sleep until needed. Set `"focus": false` for uncached ordinary carrier scheduling.
Host reuse never reduces modeled operation cost or changes world time.

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

For the schema 2 finite attenuation candidate, with bounded source allowances and
explicitly configured decay on each completed field link, where removed fractions
come to rest at the receiving node instead of being lost:

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
Compare selected behavior using the small-space physics suite (`examples/small-space/`, deleted on 2026-09-17),
or probe the outward field from outside the event space with the
inverse-square experiment (`examples/inverse-square/`, deleted on 2026-09-17).
The local Maxwell experiment (`examples/maxwell/`, deleted on 2026-09-17) tests a configured
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
For CPU-parallel active-Node planning, pass `--node-workers N` with `N` from 2
through 64. Each tick commits the isolated worker proposals in deterministic Node
order. The default is one worker. The
worker setting affects host execution only and is recorded in `run.json`.
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

## Run performance

Reuse the installed environment for later runs; dependency installation is a
one-time setup step. Ordinary runs capture no animation frames. Only an explicit
`--visualize` request records the generic disturbance view, and `--frame-stride`
samples the recorded frames without changing the physical update interval or
the event trace. See [performance measurements](docs/PERFORMANCE.md) for the
measured cases and their limits.

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

That option enables the presentation-only checks that render run reports. Do not enable it merely because a simulation test runs.
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
| `src/event_universe/dense_field.py` | The dense mode: a board's pure-field Nodes cycled as one vectorized integer step (`dense-field-v1`, off by default) |
| `src/event_universe/fields/` | Generic field arithmetic, rays, spatial couplings and local rules |
| `src/event_universe/diagnostics/` | Read-only observers, conservation audits and the optional disturbance renderer |
| `src/event_universe/runner.py` | Initialization-based execution and optional visualization |
| `src/event_universe/ui.py`, `ui_assets/` | Local configuration workspace, templates and isolated CLI jobs |
| `src/event_universe/retention.py`, `docs/RETENTION.md` | Registered output ownership, active writer protection and 24-hour cleanup |
| `examples/basic.json` | Complete example initialization; physical names occur only as data |
| `examples/finite_fields.json` | Schema 2 finite emission, completed-link decay and explicit background |
| `tests/` | Generic contracts, schema checks and explicit research regressions |
| `docs/DISTURBANCES.md` | Authoritative generic schema, laws, timing and failure contract |
| `docs/LOCAL_FIELD_RULES.md` | Local retained/output rules, component groups and joint field/carrier transactions |
| `POSTULATES.md`, `SIMULATOR_DEFINITIONS.md` | Shared principles and scoped candidate requirements |
| `docs/ARCHITECTURE.md` | Ownership and dependency boundaries |
| `docs/PHYSICAL_FEATURES.md` | Procedure for a new physical hypothesis |
| `docs/TEST_EXPECTATIONS.md` | Independent test inputs and expected outcomes |
| `docs/MIGRATION.md` | Transition from implicit scalar defaults |

## Generic field, specific use

Each configured disturbance type carries named scalar/vector fields together.
Choose whole-record movement for coupled attributes or extensive splitting for
divisible quantities. Conservation is a declared component-wise local balance,
including explicit sources and in-flight amounts. Schema 2 counts localized
deposits as inventory and subtracts committed dissipation only under the explicit
`"residue": "dissipate"` option; its finite allowances are separate from inventory.
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

## Standalone generic vector lab

The opt-in [vector lab](tools/generic_vector_lab/README.md) contains externally
configured N-to-M node reactions, bounded rational vector arithmetic and exact
conservation tests. It is an independent experiment, not the active simulator.
Run `python -m tools.generic_vector_lab.run_demo` from this repository.

## License and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen.
Every version is archived on Zenodo; the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746) resolves
to the latest version, and each version's own DOI is listed on that record
(0.3.0: [10.5281/zenodo.22749342](https://doi.org/10.5281/zenodo.22749342);
see [CHANGELOG.md](CHANGELOG.md)).
Cite the software using [CITATION.cff](CITATION.cff); GitHub renders it as a
citation entry on the repository page. Reference form:

> Gonen, A. (2026). Universe24: a discrete simulator of local physical laws
> (Reality Theory) (Version 0.3.1) [Computer software]. Zenodo.
> https://doi.org/10.5281/zenodo.22738746
