# Architecture and change boundaries

The one engine is the engine of the Beam Law ([BEAM_LAW.md](BEAM_LAW.md),
its bookkeeping [ENGINE.md](ENGINE.md)):
`src/event_universe/events/` on the substrate of `src/event_universe/core/`,
with the host modules (the runner, the preflight, the workspace, retention,
the snapshot writer) around them. This document owns the repository policy:
the local integer operation contract every physical change obeys, who owns
generated output, the monorepo's single owners, the dependency direction the
gate enforces, and how a physical feature is added. The boundaries of the
engines before it, deleted on 2026-09-19, are in git
([migration](MIGRATION.md)).

## The API of the GameBoard: an emitter in, a detector out

The model owner, 2026-09-20: "when you intervene in the GameBoard it requires
a detector on the GameBoard or an emitter; that is the API." Every way the
world touches the GameBoard is one of its external things, both of them
measured events with declared widths ([the entity catalog](ENTITY_CATALOG.md)):
input goes in through an emitter, a measured event that releases events by
its clock and its table (a lamp, a source, a star, a mirror that re-releases);
output comes out through a detector, a set of Nodes with one record whose
clicks are the only reading reality has. The world file's declarations are
the state at interval 0. Nothing else writes to or reads from the GameBoard
as physics: a host reading of the dense arrays (`GameBoardDiagnostics`, the
shell means, the books) is a diagnostic or a picture, labelled a GameBoard
reading and never registered as a measurement
([the two kinds of readings](EXPERIMENTS.md)), and no tool, test or agent
sets an event at a Node during a run. A rule that acts on an event in transit
(the collision, the generalized collision in design) is a meeting of events
on the GameBoard, not an intervention.

## Entity authoring boundary

[Reusable entity definitions](ENTITY_DEFINITIONS.md) owns separate definitions,
placement, strict dependency resolution, portable bundles and input provenance.
The host loader expands data before the canonical world parser; physical modules
receive immutable ordinary Events and never load a file or branch on an entity
label. All runner, preflight and workspace paths use that one loading boundary.

## Local integer operation contract

This contract applies to all new and changed physical code, world definitions
and prototypes intended for the engine ([ENGINE.md](ENGINE.md)). LOCALITY-1
and the numeric bounds in SIMULATOR_DEFINITIONS.md remain authoritative.

### Generic operations and law ownership

Express active laws as initialization-defined compositions of supported scalar
and vector operations. Particle names, charges, masses, couplings, thresholds,
interaction eligibility and participant limits are data; names must not select
hidden physical equations. Reuse generic operators instead of adding a special
electron, proton, electromagnetic or computation-load branch to the engine.

The engine owns scheduling, addresses, capacities, transport timing, validation
and atomic commits. It must not own a model-specific force, energy, momentum or
field equation. Generic arithmetic belongs to its documented reusable owner;
model/API assembly only composes it. Scheduler indexing and timing arithmetic
are necessary bookkeeping, not permission to hide physical laws in the scheduler.
An externally configured equation is still a chosen law, not evidence that it
emerged from the GameBoard.

Keep immutable parsed law definitions outside dynamic node, disturbance,
pending-proposal and packet payloads. Payloads carry bounded state values and
declared identifiers, never copied expression trees, formula strings, Python
callbacks or executable code. Read-only diagnostics may calculate global
measurements but cannot supply a physical update or repair conservation.

### The operations of the law

Since the model owner's statement of 2026-09-21 (record 167 of
[the log of 2026-09-20](LOG_2026-09-20.md); the derivation mathematician's
inventory, record 168), every rule of the Beam Law is one of six operations on
bounded integers, or a declared rounding at load or at the click:

1. A translation by a rate with a threshold: `core.integer.by_clock` and
   `by_drive` (the flight, the phase per interval, every count of a clock).
2. A bilinear form, an inner product with a declared matrix:
   `core.integer.signed_inner`, a vector, a diagonal matrix of +1 and -1, a
   vector. The click's weight sits here: for one arm the form **f**^T **G**
   **f** of the record's phase-count vector **f** with the Gram matrix
   **G** = **E**^T **E** of the tables (`amplitude.Layer.gram_form`,
   `core.phase.phase_gram`, no pointer formed), for several arms the same
   form on the tensor product of the arms' vectors through its rank-2
   factorisation, the pointers' product taken with itself,
   `signed_inner((X, Y), (X, Y), (1, 1))` in `amplitude.cells`; nothing
   squared as a step of its own (records 173 and 188 of the same log;
   [BEAM_LAW note 37 (xi) and (xii)](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)).
   The coupling, `nature_beam.push_form`, is the signed sum over the columns
   of the columns' whole parts, each floored off the reader's clock between
   its product and the sum, and keeps its own loop; note 37 (xi) states why
   it is not the primitive's call.
3. The group-ring addition: the merge's signed sum by magnitude with its
   cancel (`nature_beam`), the counts' accumulation (`amplitude.add_counts`);
   and the ring's multiplication within an arm (`amplitude.ring_product`, a
   read's factor a multiple of the identity).
4. A permutation: the collision's six-heading table, the meeting's arc, the
   gate's relabelling of a record's rows.
5. The evaluation: the pointer over the tables of the circle
   (`coherent_pointer`; `amplitude.Layer.evaluate`, the report's pointer and
   the several-arm form's factor).
6. The Euclidean division: the ladder's rungs, `apportion_whole`, the
   reduced pairs and every whole part.

A new physical rule is written as one of these six, composed from the world's
tables, or as a declared rounding named where it is taken; a square, a root or
a float is not an operation of the law.

### Integers, vectors and tensors

All physical numeric inputs, registers, intermediate results and transmitted
components use the declared bounded integer domains. Reject booleans and
floating-point inputs rather than coercing them. Python's arbitrary-precision
integers do not remove the model's working-register bounds: check intermediates
before cancellation, scaling or assignment. Never add float, complex, NumPy,
Decimal or Fraction arithmetic as a physical fallback.

Represent scales and ratios with explicit bounded integer numerators and
denominators. Exact-division operators must reject a zero divisor or a nonexact
result. A rule that permits division with remainder must declare the existing
bounded remainder owner, update and lifetime; do not silently discard a remainder,
round through floating point, wrap overflow or clamp a failed calculation.
In the Beam Law the owner of every count's remainder is the accumulator on
the body's own record ([BEAM_LAW note 41](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation), the
fraction-free law of 2026-09-20; `core.integer.by_drive`): a whole part
off the clock at the current rate discards the remainder of a changing
rate, so it is admitted only as the constant-rate identity of a count, or
as a comparison of an age against a key.
Keep documented integer split/quantization policies explicit and test their
accounting. Arithmetic failure must not leave a partially committed transaction.

The active field schema currently supports scalars and three-component vectors.
Its constant 3-by-3 integer matrix transform is not general tensor-valued state.
Do not claim arbitrary tensor support or silently flatten an unsupported shape.
A future tensor extension must declare fixed rank and dimensions, component
bounds, generic operators, transport coding and all state/diagnostic consumers,
with shape, overflow and locality tests before use. Tensor notation alone does
not make a calculation generic, integer or local.

### Local inputs and bounded work

A physical rule may read its own fixed local records and information already
delivered through the six neighbor ports under the transport contract. Neighbor
coordinates do not authorize instantaneous reads of remote physical state.
Trace every input to its causal owner, including self-field subtraction,
computation-load fields, energy bookkeeping and collision eligibility.

Fix local record, field, rule and participant capacities in validated definitions.
Only supported configured participant limits may be used; a larger value does
not create an unsupported many-body operator. Bound local loops and storage by
those capacities, independently of world size. Never compute responses from an
all-particle scan, global field reconstruction, growing per-source history or a
host-side correction. Charge, momentum and declared energy balances need explicit
local owners and transaction checks; a diagnostic total alone is not a law.

### Review evidence and scope

For each affected operator or rule, identify its owner, scalar/vector shape,
integer input/intermediate/output bounds, causal input path and failure behavior.
Run the affected checks selected by tools/check.py, including related integer,
initialization, architecture and locality gates when those contracts change.
The existing entry points are tests/test_integer_arithmetic.py,
tests/test_architecture.py and tests/test_locality.py.
Review gaps in scanner coverage explicitly; passing static checks is not a proof
about arbitrary Python or every possible configuration.

Read-only rendering and host timing may use noninteger arithmetic outside the
physical path; their results must never feed physical state. Historical named
models retain their explicit contracts and must not be copied into the active
generic engine. External floating-point or globally coupled reference prototypes
are not compliant active-engine implementations, even if their GIFs look useful.

Q-ORACLE-1, the explicitly scoped opt-in quantum exception, was deleted on
2026-09-17 with Highlights section 3.18 (issue #164, buckets B.1 and B.2), the
source envelopes on the same day under Highlights section 3.5 (bucket B.3),
the causal event ledger under Highlights section 3.20 (bucket B.4) and the
bond registry, claim-gather and the lottery capture the same day under
Highlights sections 3.19, 3.20, 5.1 and 5.4 (bucket B.5), and the record
operations (records as owners and the N-to-M conversion of records) the same
day under Highlights sections 3.20 and 5.1 (bucket B.6, the last). No path in
the package answers at a distance, and no Node folds an arrival into a
resident. That every bucket of issue #164 is deleted is not evidence that every
repository path already satisfies the active local integer contract.

## Generated output ownership

`retention.py` owns host-only artifact registration, writer leases and expiry.
Runners own complete fresh output directories; the workspace owns exact input,
log and export files and declares the child-output dependency for companions.
Cleanup uses recorded filesystem generations and operating-system locks, with
recoverable quarantine before removal. The module never imports or changes
physical engine state. Its one-shot and singleton watcher interfaces share the
[same retention contract](RETENTION.md).

## Monorepo ownership

Universe24 is one versioned repository, not a requirement that every component
run in one process. Keep the current package layout until an actual independently
built component justifies another package; do not create empty apps/packages trees.
The [README project map](../README.md#project-map) is the path index; the dependency
table below defines code boundaries. Architecture owns this repository policy.

| Information | Single owner | Update rule |
| --- | --- | --- |
| Executable code and law selection | [src/event_universe](../src/event_universe/) | Keep shared formulas generic; the world file selects them |
| The world file, the interval's steps and the record | [The Beam Law](BEAM_LAW.md) and [the engine's bookkeeping](ENGINE.md) | Keep the live contract in one document; the engines before it are in git |
| Physical contracts | [POSTULATES.md](../POSTULATES.md), [SIMULATOR_DEFINITIONS.md](../SIMULATOR_DEFINITIONS.md) | Plain-language principles and exact contracts have distinct roles |
| Test expectations | [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) | Link the responsible tests, inputs and outcomes without copying laws |
| Installation and execution | [README.md](../README.md) | Reuse the package CLI and [tools/check.py](../tools/check.py) |
| Contribution and integration | [CONTRIBUTING.md](../CONTRIBUTING.md) | One coordinated change includes affected providers and consumers |
| Durable agent procedures | [skills/workflow.md](../skills/workflow.md) and specialist Skills | Shared rules live once; specialist Skills reference them |
| Current task, owner and evidence | Repository Issues and PRs | Record head/base, acceptance target, blockers and next action |
| Checkout orientation | [PROJECT_STATUS.md](PROJECT_STATUS.md) | A dated, commit-pinned snapshot links to live work; no duplicate task ledger |

Use existing definition headings or stable rule IDs when mapping a change to code
and tests. Record the exact contract, implementation path and test path in the PR;
extend the responsible test-expectation entry if coverage changes. Never treat a
test's existence as proof it passed. Architectural decisions belong here or in a
linked focused decision document; physics decisions belong in their contracts.

Store reproducible scenario inputs, configuration and test fixtures with the code.
Keep generated videos, HTML, traces and large outputs outside source commits.
Link them from the PR with the code identity, command and relevant parameters;
artifact retention is finite, so preserve required evidence before it expires.
There is no automatic chat-to-repository or Google-Doc-to-code synchronization.

## Dependency direction

| Module | Allowed dependencies |
| --- | --- |
| `core/integer` | Standard-library types; owns the working-register bound (`checked_work`) and the Beam Law's integer primitives (`bounded_gcd`, `integer_root`, `by_clock`, `by_drive`, `signed_inner`, `apportion_whole`); the array forms of the two counts over rows (`by_clock_rows`, `by_drive_rows`) live in `events/nature_beam` with numpy |
| `core/game_board` | `core/integer` (`checked_work`); the GameBoard's addresses, the six Port headings in Port order (`PORT_HEADINGS`, `adjacent_node`), the cube's group of 48 with its hand (`cube_symmetries`, `compose_symmetries`, `inverse_symmetry`, `symmetry_hand`; named 2026-09-21) and the bound of a declared charge and quantum (`MAX_VALUE`) |
| `core/phase` | `core/integer`; the phase circle's cosine and sine tables from fixed-point series, cached per N, and the circle itself as the cyclic group of N steps with its unit vectors (`PhaseCircle`, `phase_circle`; named 2026-09-21), and their Gram matrix (`phase_gram`, stored through `GRAM_STORED_STEPS`) |
| `events/world` | `core/integer`, `core/game_board`; the world file of the Beam Law, its keys, defaults, bounds and refusals (`parse_nature_beam_world`, `NatureBeamWorld`), the constants `Q`, `LABEL_SCALE`, `FACE_NAMES`; no execution |
| `events/measured` | `core/integer`, `core/game_board`, `events/world`; the records the engine keeps beside the rays (`Measured`, `DetectorSet`, `Ledger`, the reduced rational pairs); no law |
| `events/nature_beam` | `core/integer`, `core/game_board`, `core/phase`, `events/amplitude`, `events/measured`, `events/meeting`, `events/world` and numpy; the Beam Law, one function over the whole GameBoard (the flight table, the one reading, the collision table, the push, the detector's record, the releases, the store) |
| `events/amplitude` | `core/integer` (`signed_inner`), `core/phase` (the tables, `phase_gram`), `events/measured`; the apparatus's layer of the amplitude law (`Layer`: the records' phase-count vectors, the ladder, the gathers), host integers, no GameBoard state |
| `events/meeting` | `core/integer`, `events/world` and numpy; the meeting of a paid unit with the free crowd (`meet`, the arc table), the turn read off the phase register |
| `events/engine` | `core/integer`, `core/game_board`, `events/amplitude`, `events/measured`, `events/nature_beam`, `events/world` and numpy; the interval's frame, the clocks, the steps, the books and the snapshot (`NatureBeamSimulation`); no output or storage |
| `events/run` | `events/engine`, `events/world`, the package version, `snapshot_writer` and the standard library; the artifacts of a run (the one physical module allowed to write files) |
| `events/__init__` | `events/world`; `events/engine` lazily (`Measured`, `NatureBeamSimulation`), so importing the package loads no numpy |
| `json_documents`, `snapshot_writer`, `retention` | Standard library; host modules with no physics |
| `world_loading` | `events/world`, `json_documents`; the entity definitions loader and the portable bundle |
| `configuration_validation` | `events/world`, `world_loading`; read-only |
| `runner` | `events/run`, `retention`, `world_loading` |
| `ui` | `configuration_validation`, `json_documents`, `retention`, `world_loading`; local HTTP and isolated CLI process ownership |
| `diagnostics/numeric_audit` | Standard library; the two static audits, `core/` integers only and `events/` integer numpy and nothing that leaves the integers (`run.py`, the artifacts' writer, outside it) |
| `diagnostics/shell_readings` | `events/engine`, `core/game_board`, numpy; the shell means of the engine's readings, read-only, the one floating-point calculation of the package (a host diagnostic, outside the engine since 2026-09-21) |
| `tools/` | Readers of the record, loaded by their path and never imported by the package (the architecture review of 2026-09-20: a tool calls the engine's functions, it owns no rule): `coupling_readings` imports `core/integer`, `core/game_board`, `events`, `events/nature_beam`, `events/world`, `json_documents` and numpy; `orbit_readings` `core/integer`, `events`, `events/nature_beam`, `events/world`, `json_documents`; `heisenberg_readings` `core/integer`, `events`, `json_documents`; `redshift_readings` `events`; `migrate_nature_beam_worlds` `events/world`; `bell_chsh`, `run_series` and `check` the standard library; the `derivations_round*` scripts numpy |
| `tests/` | The package's modules under test, the tools by their path (`importlib`), the gates (`tests/architecture_rules.py`, the repository scanners) the standard library; `tools/check.py` selects a test by its imports and by the files it names |

The gate (`tests/architecture_rules.py`, `tests/test_architecture.py`): `core`
imports only `core`; `events` imports only `core` and `events`, except
`events/run`, which writes the artifacts; no physical module imports an output
or storage library; and every module of `core/` passes the integer audit.

## Verification scope

LOCALITY-1 in SIMULATOR_DEFINITIONS.md governs the complete dependency path of
every physical update, including self-field inputs. Shadow/reference
computations cannot be hidden behind a local adapter. `test_locality.py` rejects
known world access and replay in generic field modules. Code review
must still check causal input provenance and bounded loops; static checks do
not prove arbitrary Python is O(1). Global scheduling and diagnostics retain
their explicitly separate host costs.

| Reviewed path | Local bound | Separate host cost |
| --- | --- | --- |
| Generic disturbance local cycle | Fixed fields/types/rules and resident slots; up to six outgoing channels per record | Sparse scheduler and diagnostic totals grow with materialized nodes and packets |
| Diagnostics and rendering | Not a physical update; cannot feed state repairs | Full-state audits, histories and rendering are not O(1) |

The implementation therefore supports bounded local model work, not a claim that
the entire Python program or a full simulation tick is O(1).

The import-boundary audit resolves absolute and relative imports and rejects
runtime arithmetic in API assembly while allowing type annotations and literal
configuration; it is tested with both allowed and forbidden examples. Inputs and
expected outcomes are listed in `TEST_EXPECTATIONS.md`.

## Adding physical features

Follow [the physical-feature procedure](PHYSICAL_FEATURES.md) before adding a
law or state contract. It separates explicit local inputs, evolving state,
immutable parameters, derived values and model assembly. Dependencies between
physical inputs remain explicit; code separation does not imply statistical
independence. Formula-free assembly is checked for the public API assembly.

## Repository language

English is required for all repository comments, docstrings, documentation,
instructions, diagnostic messages and new identifiers. The authoritative rule
is [Repository language: English](../AGENTS.md#repository-language-english).
`tests/test_repository_language.py` guards against legacy non-English scripts;
review checks the actual language. Older branches must follow this rule when
merged. Mathematical notation remains valid. This affects documentation and
review, not physical laws.

## Standalone vector-lab experiment

The user-requested [tools/generic_vector_lab](../tools/generic_vector_lab/README.md)
is an opt-in mechanism experiment with its own explicit JSON laws. It does not
import, replace or extend the active engine or its schema. The lab runtime owns
its local transactions; its separate movie tool reads saved states. Generated
outputs go under artifacts and remain outside source commits. Its local quantum
coupling is a toy experiment of the lab alone; the repository's shared quantum
resource was deleted on 2026-09-17. The active source-of-truth boundaries above
remain unchanged.

