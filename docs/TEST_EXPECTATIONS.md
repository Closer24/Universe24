# Test inputs and expected results

## Active generic disturbance contracts

The primary Simulation follows [DISTURBANCES.md](DISTURBANCES.md). Schema and
engine tests must use independent examples for the contracts below. These are
acceptance requirements, not a statement that a particular source tree passed.

| Input or boundary | Required outcome |
| --- | --- |
| Complete JSON initialization; renamed field/type labels | Equivalent declared behavior with no physical-name branches |
| Unknown/duplicate names or keys, wrong components, floats, unsupported expressions | Validation error before simulation |
| Whole-record move with scalar amounts and a vector attribute | One owner and unchanged carried values in free transport |
| 12 units, weights `[2,0,1,0,0,0]` | 8 through +X, 4 through +Y |
| Signed vector splitting and indivisible amounts | Component totals exact; bounded retained allocation state |
| Conserved-field assignment without source flag | Rejection; explicit source change included only when committed |
| Local exchange from donor to receiver | Equal-and-opposite component changes; both sides commit together |
| Exchange drives unsigned field negative | Failure before either proposed record is committed |
| `B=10`, costs 10, 11, 21 | Total earliest arrival after cycle start is `tau`, `2*tau`, `3*tau` |
| Delayed local cycle with later arrivals | Frozen original proposal; arrivals cannot overwrite locked records |
| Waiting originals and in-flight packets | Each conserved amount counted exactly once at every completed tick |
| Receiving/outgoing capacity or arithmetic bound exceeded | Explicit stopped run with retained ownership, no hidden queue or dropped record |
| Missing CLI `--init` | Error without implicit built-in physics |
| Ordinary headless run | Input, event, metadata and final-state files; no frame capture/render import |

`test_initialization.py` covers the parser and examples;
`test_disturbance_engine.py` covers generic ownership, timing and arithmetic;
`test_disturbance_application.py` covers required initialization, headless output
and run metadata. Standard checks are headless. Only
`pytest --visualize-runs` enables rendered run reports and presentation-only
checks; physical invariants remain active without it.

The remaining scalar, source, stream, collision, link and turning expectations
are retained for explicitly selected historical research APIs. Their results do
not establish those laws for arbitrary configured disturbances.

## Causal-stream candidate

`test_causal_stream.py` checks exact conservative six-port branching; rejection
of a negative old population even when a positive source would mask it; explicit
rejection of scalar seeding without mutation; isolated axis and diagonal momenta
with zero impulse residues at every tick; a Manhattan-distance-nine source pair
with zero response through tick eight and opposite (2,0,1) impulses at tick nine;
and an offset moving pair with opposite transverse responses at tick twenty-six.
The free-space cases do not reach periodic return. These are candidate acceptance
checks, not a claim of isotropic propagation or an established force law.

Shared calculations live in generic components. The model selects weights,
sources, response and activity policies and maps results to fixed records.
Scenarios provide initial conditions; the engine manages time, neighbors and
occupancy; measurements read the result.

## Tests by responsibility

| Test file | Responsibility | Expected outcome |
| --- | --- | --- |
| `test_integer_contract.py` | Integer arithmetic and bounds | Exact quotient and remainder for either sign; reject overflow before use |
| `test_lattice.py` | Periodic geometry | Same six-neighbor ordering for reads and moves, including boundaries |
| `test_scalar_field.py` | Generic field | Known numerical results for weights, signed values and remainders |
| `test_field_policies.py` | Source, range and activity | Derive source from count; test clipping and activity separately |
| `test_turning.py` | Generic vector response | Shared impulse arithmetic for each direction policy; opposite field impulse |
| `test_movement.py` | Movement budget and axis selection | Preserve momentum without field influence; budget schedules one step |
| `test_current_field.py` | Current-model assembly | Occupancy source, nonnegative field, transverse response and legacy activity |
| `test_field_composition.py` | Replacement in the engine | Alternative laws change the expected outcome; remainder-only activity persists |
| `test_engine.py` | Causality, occupancy and scheduling | One-edge propagation and movement; one particle update per tick |
| `test_diagnostics.py` | Measurement and display | Exact XY/XZ/YZ slices; full XYZ and off-plane records; source state untouched |
| `test_application.py` | Historical runner output | Headless metadata/events and lazy imports; explicit visualization preserves slice/volume event identity |
| `test_regressions.py` | Physical behavior | Prompt contact, reflection symmetry, three-plane turning, momentum, isolated motion and the original 180-tick result |
| `test_architecture.py` | Layer separation | Reject forbidden imports and adapter formulas; audit integer physics |
| `test_repository_language.py` | English repository text | Reject legacy non-English scripts in project prose; preserve mathematical notation |

Paths are relative to `tests/`. The dependency rules live in
`tests/architecture_rules.py`. Allowed and rejected examples test the rules
including relative imports and aliases.

## Exact numerical examples

| Calculation | Input | Expected result |
| --- | --- | --- |
| Uniform source | 3 sources, strength 64 | 192; no accumulated emission history |
| Current field | Neighbors `(1,2,3,4,5,6)`, two strength-64 sources, remainder 3, denominator 7 | Value 21, remainder 5 |
| Signed generic field | First-neighbor weight -1, neighbor value 10, denominator 3 | Value -3, remainder -1 |
| Range policy | Sample value -3, remainder -1 | Current policy returns value 0, remainder 0 |
| Gradient | Neighbors `(9,4,2,10,6,6)` | `(5,-8,0)` |
| Current turning | Momentum `(3,0,0)`, gradient `(128,64,0)`, denominator 64 | Impulse `(0,1,0)`, new momentum `(3,1,0)`, field momentum `(0,-1,0)` |
| Small impulse | Vector `(0,1,0)` each tick, numerator 1, denominator 64 | After 64 ticks: one y momentum unit, zero remainder |
| Quarter-rate movement | Momentum `(3,0,0)`, cap 12, initial budget 0 | Budgets 3, 6, 9; fourth tick moves +x with budget 0 |
| Diagonal direction | Momentum `(3,-2,1)`, initial phase 0 | Cycle: +x, +x, +x, -y, -y, +z |
| Periodic boundary | Shape `(4,5,6)`, address `(-1,12,13)` | `(3,2,1)` |
| Alternative field remainder | Initial value 1, local weight 8, neighbor weights 0, denominator 7 | Value 1 with remainders 1 through 6; seventh tick value 2, remainder 0 |
| Intermediate overflow | Product exceeds 64-bit work bound, even with a cancelling remainder | OverflowError at multiplication |

These are independently fixed expectations. Conservation tests also use identities
such as the sum of particle and field momentum before and after exchange.
Regression assertions use independently specified physical outcomes rather than
copying the tested formula. Historical engine/API and old-Python compatibility
are not acceptance targets.

## Calculation ownership

Source multiplication and nonnegative clipping live in `fields/policies.py`.
Field arithmetic lives in `fields/scalar.py`; turning and movement in `dynamics/`.
`core/lattice.py` centralizes addresses and neighbors. Bounded multiplication,
remainder accumulation and division live in `core/state.py` and serve all three
turning components.

Cell activity is an injected decision. The original model explicitly keeps its
old value-based activity. Supplying `ScalarSimulation(field=...)` tracks remainder
changes by default; `field_activity=` selects another policy.

Model, API and compatibility assembly contain no independent arithmetic.
Architecture checks reject runtime formulas in these modules. Configuration and
initial conditions are intentionally specific and tested through the behavior
they produce. The framework remains constrained to 3D, six neighbors and the
declared fixed cell schema.

## Running and validating changes

The suite reuses world runs when their inputs and required observations coincide.
The existing 24-tick contact/reflection experiment also checks the first transverse
response, per-tick momentum and final remainders. The 110-tick turning experiment
covers XY, XZ and YZ with momentum and remainder checks. Stationary-source symmetry
and persistence remain in `test_engine.py`. The shared
plane/volume application test checks metadata, traces and standalone HTML together.
The independent eight-case stream/free-control comparison covers the ordinary
isolated-rate cases; the original sampler retains only the additional 1/100 and
18/20 rate regimes. Bounds and known physical failure evidence remain covered.
The frozen engine is no longer imported or simulated, and the old facade API
comparison is removed. This reduction removes four collected cases, six worlds
and 447 simulation ticks without removing the physical regimes above.

Run `python tools/check.py` from the installed project. It checks style, types and
behavior and creates `artifacts/test-runs.html` for all captured world runs.
Pure-function unit tests do not run a world. See `VALIDATION.md` for recorded
validation and tool versions.

A new law requires inputs, expected outputs and edge cases before implementation.
Test its generic calculation and engine integration independently. Static checks
enforce known boundaries; they do not replace behavioral tests.

## Local links: candidate v11

| Test | Input | Expected outcome or boundary |
| --- | --- | --- |
| Generic stretch | Base 100, endpoint values 10 and 10 | Length 110; swapping endpoints changes nothing |
| Transit time | Length 110, rate c or c/2 | 110 or 220 ticks; no credit from a previous link |
| Numerical limits | Negative, floating-point or overflowing input | Explicit error before commit |
| Ownership | All six directions, including periodic seams | Both endpoints identify the same owner |
| Geometry message | Old length 100, proposed 110 | Both endpoints stay at 100 until delivery at tick 100 |
| Busy channel | Hundreds of updates during transit | One packet, three integers; zero is delivered and clears state |
| Simultaneous proposals | Lengths 13 and 7 arrive together | Both sides select 13 regardless of processing order |
| Replace merge policy | Same inputs with min | Both sides select 7; policy is injectable |
| Causality | Source two length-3 links away | No target influence before t=6 |
| Read boundary | Direct remote scalar read raises | Run succeeds through delivered mailboxes only |
| Rest and c | Stationary particle and fast particle on length-5 link | Rest stays fixed; fast particle arrives at t=5 |
| Locked transit | Departure length 3, field grows en route | Arrival time remains fixed at departure |
| Symmetry | Stationary source, coupling 1, 80 ticks | Six directions equal; zero momentum |
| Three particles | Moving sources, coupling 1, 50 ticks | Total momentum conserved each tick; valid occupancy |

Historical baseline expectations remain unchanged. World tests use the existing
HTML pipeline only when `--visualize-runs` is explicitly requested.
The stretch law and proposal merge are tested as separate hypotheses.

## Repository navigation

`test_repository_navigation.py` checks local Markdown destinations in root
documents, docs and Skills against the actual tree. It also checks that every
specialist is reachable from Boss and references the shared workflow. Synthetic
valid and missing file/heading links exercise rejection independently. No world
runs are added. External URL reachability and instruction quality still require
review; this check does not certify physical acceptance.

## Shared instructions and architecture boundaries

- Repository input: AGENTS.md must exist, be linked by README, contribution and
  architecture documents, and be included in MANIFEST.in. Referenced documents
  must exist. CI runs the same validation command used locally.
- A model importing an engine through `from ..core import engine` or
  `linked_engine` must be rejected, including that indirect form.
- A new or nested model containing `x + 1` or `source * count` must fail the
  assembly gate. Every file under `models/` is covered rather than a fixed list
  of existing model names.
- A model selecting `MeanStretch(100, 1, 2)` must pass: selecting parameters is
  composition, while the reusable component owns the formula.
- These tests do not run worlds and do not prove that an agent in another
  conversation has read the instructions.

## Quantum detector trial — opt-in only

The feature contract is in [QUANTUM_DETECTOR_TRIAL.md](QUANTUM_DETECTOR_TRIAL.md).
For a prescribed two-output interferometer, phase counts 0, 1, 2, 3 must yield
weights (4,0), (2,2), (0,4), (2,2). Enumerating tickets 0 through 3 verifies the
exact categorical selection; it does not test empirical randomness.

At world tick 8, the test controller commits exactly one detector record while
Engine state and time remain unchanged. Four repeated readouts, including a
changed ticket, return the same record without extra evaluation. Two bridges
share the result. Continued physical evolution must match the unqueried baseline
through tick 12. The detector record is not an Engine-native physical event.

Bad tickets, early or late first-readout timestamps, overflowing amplitudes or
weights, a zero total weight and exhausted combined work budgets must fail
without creating a terminal record. Pure queries never sample; repeated queries
preserve history and report cache hits. Different query depths retain model cost
1 and world time cost 0 while reporting distinct host work under Q-ORACLE-1.

Quantum boundary tests reuse the project's import resolver. Relative Engine
imports, importing engine from core and importing quantum from diagnostics must
be rejected even with aliases. Bounded arithmetic from core.state, imports within
quantum and the integration adapter are allowed. These are static checks, not a
proof against arbitrary dynamic Python or a proof of physical locality.

## Locality and bounded local work

`test_locality.py` supplies a read spy at (3,3,3) in extents 8 and 1,000,000.
Both calls must read the same six cardinal neighbors once each and return the
six supplied values in order. This test creates no world and advances no time.
Negative source examples in fields, dynamics and models must reject global cell
or particle access, occupancy/history reads and shadow step/run calls. The
normal architecture test scans all production modules with the same guard.
LOCALITY-1 also requires manual end-to-end provenance and loop-bound review;
passing these finite checks alone does not establish general O(1) complexity.

## Repository language

The English-only rule is authoritative in AGENTS.md and linked from the
architecture guide. The language test scans project source, tests (including
frozen references), tools, docs, root text files and workflow configuration.
Generated artifacts, installed dependencies and Git history are outside its scope.

Examples contain escaped test data: a Hebrew comment, docstring or heading must
be rejected; English prose and mathematical notation must pass. The script check
also rejects Arabic, Cyrillic, CJK, Hiragana, Katakana and Hangul letters. It is a
guard against non-English scripts, not a language classifier: Latin-script prose
still requires review. No physical calculation changes as part of translation.

## Motion display and playback

- `test_render_motion.py`: momentum (3,0,0) at c_units=12 produces an arrow
  of length 2.7; (12,0,0) produces 10.8. Momentum (3,4,0) at c_units=14
  produces (3.24,4.32,0), length 5.4. Rest or a missing scale shows no arrow;
  invalid scales are rejected. These are display-only numerical calculations.
- Periodic display fixtures cover both directions and every axis. The move
  x=63 to x=0 in a 64-cell axis is a boundary crossing, not a multi-cell jump.
  The move x=63 to x=1 is both a boundary crossing and a two-cell jump;
  the renderer must preserve both indicators. Two simultaneous seam crossings
  likewise cannot hide a two-cardinal-step displacement.
- `test_playback.py`: two distinct synthetic snapshots are rendered in both
  slice and 3D modes. Expect two distinct GIF frames with positive duration,
  no repeat extension, and an HTML note that playback stops at the end.
- `test_three_particle_continuity.py`: replay the reported 64-tick experiment
  in a 64x48x32 world with its original three seeds. Every particle ID persists;
  each particle stays put or moves to one periodic neighbor at each tick.
  Expect no boundary crossings in this exact experiment. When visualization is
  requested, save every tick in HTML without interpolating or smoothing positions.
- Continuity is not an isolated-motion or self-force test. A trajectory may
  obey the one-hop bound and still contain an incorrect self-induced turn.


## Run rejection for isolated momentum changes

`test_run_invariants.py` requires rejection of even a one-unit isolated momentum
change and acceptance of unchanged momentum. A real diagonal self-field run with
initial momentum (1,1,0), force denominator 12 and 72 requested ticks must stop at
tick 45 with actual momentum (1,0,0), even with frame_stride=64. Metadata must say
failed and the trace must survive. When visualization is requested, HTML must
say FAILED RUN and include the failure frame.
Total momentum conservation does not excuse the particle's self-impulse. A stationary
isolated run passes; a two-particle contact run is not subject to isolated classification.
These tests verify the detector, not success of the physical inertial-motion gate.

## Mass and elastic same-cell contact

`test_collisions.py` independently evaluates total momentum and classical kinetic
energy with diagnostic Fraction arithmetic, never using those values in physics.

| Input | Required outcome |
| --- | --- |
| Masses 1,1; momenta +3,-3 | Momenta -3,+3 |
| Masses 1,2; momenta +3,0 | Momenta -1,+4 |
| Masses 1,2; momenta +1,0 | Exact momenta -1/3,+4/3; no integer truncation |
| Opposite 3D momenta (3,2,-1),(-3,-2,1) | Every component reverses |
| Oblique equal-mass momenta (3,0,0),(0,3,0) | Momentum vectors exchange |
| 54 rational input pairs across unequal masses | Exact energy/momentum, reversibility and input-exchange symmetry |
| Momentum 1, mass 2, cap 12 | Half-unit budget credit, first hop after 24 ticks |
| Length 5, momentum numerator 1, denominator 3, mass 2, cap 12 | Transit 360 ticks |
| Same-cell head-on arrival at completed tick 4 | One collision, no extra hop; separation at tick 8 |
| Heavy stationary target | Fractional outgoing momenta persist and the target eventually moves |
| Local links of length 2 at half c | No collision in flight; one on arrival at event tick 4 |
| One-cell periodic self-loop | One contact, stable slot identity across four ticks |
| Independent transparent contact callable | Replacement preserves momentum instead of backscattering |
| Periodic four-cell axis | Contact at x=0, then another at x=2 after separation |
| Different simultaneous addresses | No collision despite visiting the same address at different times |
| Four co-residents | Fixed 16 flags, conserved totals and at most one collision per particle per tick |
| Invalid mass or bound overflow | Failure before insertion or atomic pair commit; faulted world rejects continuation |

Integration worlds are headless unless visualization is requested. Historical
fixed-schema, numeric and collision checks cover those research records and defaults.

## Balanced movement and twelve-cell halo candidate

`test_balanced_movement.py` checks all 342 signed nonzero directions in [-3,3]^3
for exact cycle counts, bounded prefix error, scaling, rate, invalid inputs and
register limits. `test_balanced_halo.py` runs six isolated signed 3D momenta for
200 ticks, checks the exact old/new six-neighbor target set, verifies an external
seed still creates momentum, verifies equal-and-opposite contact response, and
shows the same balanced movement without the halo fails the p=(1,1,0) input.
`tools/check_diagonal_motion.py` renders five engine runs and accepts only the new
candidate cases. See [BALANCED_MOTION.md](BALANCED_MOTION.md).

- Historical candidate composition: `BalancedSimulation(collisions=True)` handles
  two diagonal particles of masses 1 and 2, conserves pair invariants in a
  source-free run and separates them after one contact. All existing balanced
  movement and self-halo expectations remain unchanged.

## Run capture and export performance

These contracts belong to the historical runner and optional renderer. Tests that
generate visual artifacts require `pytest --visualize-runs`; ordinary tests stay
headless and retain physical assertions.

- `test_run_capture.py` checks selected-view snapshots against independent state
  expectations, including zero ticks, an unsampled final tick, invalid slices,
  complete event records and a partially committed failed tick. Failure metadata
  and its final frame must reflect the changed state, including exact fractions.
- `test_render_export.py` checks saved pixels and frame durations against the
  previous export path for synthetic figures, full 3D dimensions, non-repeating
  playback and figure cleanup on failure.
- Performance measurements use identical scenario inputs, tick counts, display
  sampling, image dimensions and dependencies. Timing comparisons are recorded
  separately from functional tests; CI does not assert machine-dependent seconds.

## Live display during execution

- `test_live_display.py` exercises a real spawned consumer: a copied snapshot
  appears before completion, later producer mutation stays isolated, and queued
  large snapshots can be cancelled without a feeder shutdown deadlock. Startup,
  publication and unexpected worker-exit errors remain diagnostic. Failed runs
  preserve their reason and link only a newly registered artifact.
- `test_render_live.py` compares preview PNGs with the actual canonical last
  raster for volume and slice views, including transparent and tight-crop export
  settings. Callbacks arrive before final GIF/HTML completion and cannot mutate
  the canonical images. Empty histories and failed writes close figures.
- `test_run_live.py` checks live/nonlive event and metadata parity, early page
  availability, headless defaults and explicit opt-in, cleanup, and preservation
  of physical errors even when final rendering also fails.
- Manual run evidence records page/image availability before final output,
  observed phases and saved image changes. First-image latency and whole-run
  duration are distinct measurements; browser refresh and recorded-frame
  equivalence are separate checks. Never infer concurrency from a callback name.

## Local configuration workspace

`test_workspace.py` drives a real loopback HTTP server and isolated runner children.
Edited tick counts, model labels and initial amounts must reach saved metadata;
two configurations must use distinct outputs and match direct CLI input, events,
state and metadata byte for byte without changing source files. Invalid inputs
and duplicate keys, including nested editor fragments, fail before execution.
Tests cover cross-origin/token/Host rejection, restricted artifact paths, active
job conflicts, explicit cancellation, shutdown cleanup and physical failure data.
The browser workflow additionally checks forms, JSON editing, draft persistence,
selection, validation after editing, imports/exports and optional recorded results.
Inspect the actual UI; a passing HTTP test is not proof of correct controls.
For phone layout changes, inspect narrow portrait and landscape viewports, all
configuration tabs, numeric and JSON editing, shortcuts and completed results.
Check document overflow, readable input text and touch target size. Record the
actual browser and dimensions; viewport emulation does not verify native iOS
keyboard, Safari or safe-area behavior on a physical device.
