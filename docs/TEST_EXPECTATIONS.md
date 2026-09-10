# Test inputs and expected results

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
| `test_application.py` | Execution and compatibility | Metadata, events and standalone HTML; same events for slice and volume; old API preserved |
| `test_regressions.py` | Established behavior | All state and events match the frozen version across 278 comparison ticks |
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
Regressions compare against a separate frozen source instead of copying the tested
formula to calculate expectations.

## Calculation ownership

Source multiplication and nonnegative clipping live in `fields/policies.py`.
Field arithmetic lives in `fields/scalar.py`; turning and movement in `dynamics/`.
`core/lattice.py` centralizes addresses and neighbors. Bounded multiplication,
remainder accumulation and division live in `core/state.py` and serve all three
turning components.

Cell activity is an injected decision. The original model explicitly keeps its
old value-based activity. Supplying `Simulation(field=...)` tracks remainder
changes by default; `field_activity=` selects another policy.

Model, API and compatibility assembly contain no independent arithmetic.
Architecture checks reject runtime formulas in these modules. Configuration and
initial conditions are intentionally specific and tested through the behavior
they produce. The framework remains constrained to 3D, six neighbors and the
declared fixed cell schema.

## Running and validating changes

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

Baseline expectations remain unchanged. World tests use the existing HTML pipeline.
The stretch law and proposal merge are tested as separate hypotheses.

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

## Mandatory isolated straight motion

`test_isolated_motion.py` compares a single particle in its own active field
with an otherwise identical source-free control, for baseline and unit-link
transport. Inputs: source strengths 64/0, force denominator 12, speed cap 12,
257×257×257 cells, origin (128,128,128), 72 ticks. Momenta are (1,0,0), (3,0,0),
(12,0,0), (0,-3,0), (0,0,12), (1,1,0), (3,-2,1), and (6,4,-2).

Expected: unchanged particle momentum and matching position at every tick;
the self-field becomes nonzero while the control field stays zero. For baseline
full 12-tick cycles, displacement is the initial momentum times the cycle count.
An example is (3,-2,1) after 12 ticks: position (131,126,129). Digital cardinal
steps are allowed between cycle endpoints. A self-induced momentum change or
trajectory drift fails the ordinary suite, even if total matter-field momentum
is conserved. The test has no xfail or skip exemption. All world runs are captured
in the existing HTML test report, including the frame where an assertion fails.
