# Validation evidence

Each record applies to its identified source and configuration, not all future
checkouts. Original paths and hashes in historical results are retained. Use
[the migration map](MIGRATION.md#explicit-historical-component-names) after a rename
and [project status](PROJECT_STATUS.md) for the current source map.

## Physical inventory and elementary probes — 2026-09-12

Base: main `09464b41b2c44a191aa2fcbdf4b036680bd646a5`. The sourced
[entity catalog](../examples/known-entities/catalog.json) contains 11 field
categories and 35 particle/multiplet entries. These are inventory entries,
not a count of implemented physical fields. Its definitions and support
assessment are explained in [PHYSICAL_ENTITIES.md](PHYSICAL_ENTITIES.md).
Highlights was retrieved on 2026-09-12, including its implemented-entities
section; the user's elementary-vector-operation restriction is binding.

No engine code changes. The two new configurations produce updates only by
copying, swapping or clearing vector values; guards and dot-product invariants
validate those proposals. The old unequal-mass formula remains a clearly labeled
comparison benchmark. No new configuration derives its state from that formula.

The new focused suite passed eight checks: catalog/source/conjugate consistency,
elementary update assignments, equal-mass contact on 9-cubed/X and 15-cubed/Y
domains, outgoing/rest/unequal-mass exclusions, and causal two-vector transport.
The same-local-mechanism checks are not a continuum-limit proof. The final PR
records the mandatory affected gate and exact submitted tree.

Both new inputs were run with the existing CLI and `--visualize`. The pair
completed 16 ticks and 17 recorded frames: contact at tick 4, reversed momentum
in the next sample, final X positions 1 and 7, positive mass 2 in total and zero
net charge/momentum throughout. Its summed raw squared momentum remains 2.
The field probe completed six ticks and seven frames, with exactly three
nearest-neighbor transfers taking two ticks each. Its isolated E/B pulse retains
raw squared amplitude 18 and has no source or dissipation. Both runs report
balanced accounting and use unchanged runtime fingerprint
`b8b0db5aba5c8ee14cfb87be318471f3e1352d0e83b5afb5640e3d49903c37a2`.
Recorded data and metadata were inspected; no graphical-browser validation is
claimed. Generated HTML stays outside the source commit.

This verifies restricted classical proxies and a vector transport mechanism,
not Maxwell dynamics, a photon, gravity or annihilation. Boss and specialist
Skills already route to the updated postulates and owner contracts; no duplicate
Skill rule or new agent role is needed.

## Generic local field rules — 2026-09-12

The extension starts from main `12c85316f011d0601adcd0f4a31f0f52e59eaa27`.
Its authoritative scope is [LOCAL_FIELD_RULES.md](LOCAL_FIELD_RULES.md): retained
field stock, six delivered/outgoing ports, multiple scalar/vector components,
explicit invariants and joint carrier/field transactions. It introduces no
electromagnetic law or quantum-photon result. Highlights was read on 2026-09-12;
the user's node-with-six-ports clarification governs the interface.

The necessary checks exercise simultaneous vector updates, exact six-port
inventory and link delay, independent counterflow samples, integer bounds,
immutable baselines, delayed arrival preservation and stale-invariant rejection.
Active rules retain their results after renaming and declaration permutation.
A zero-net joint chain retains both commit guards and prices their work. Existing
exchange into a local field retains its reaction instead of forwarding it outward.
Unsupported carrier-only joint rules without spatial owners fail initialization.

Independent architecture and physics-rule reviews checked local ownership,
frozen proposals, fixed field timing, bounded arithmetic and commit-cost
reservation. The implementation keeps generic calculations under `fields/`;
engine code schedules them and commits validated ownership changes.

The affected gate uses CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1.
Only changed files and their affected consumers are selected. No full audit,
older-Python compatibility suite or unrelated parameter sweep is part of this
acceptance. Exact final check counts and submitted source identity are attached
to the PR; the gate saves its commands in `artifacts/check-scope.json`.

The explicit visual run uses `examples/local_field_rules.json` with the existing
CLI and `--visualize`: a 9 by 9 by 9 lattice, eight transitions, and nine recorded
frames. Starting at `a=(3,4,0), b=(0,0,0)`, the configured rule applies
`a'=b, b'=-a`; the combined squared amplitude is 25 in every recorded frame.
All eight cycles contain component transformations, with no external sources
and balanced spatial ledgers. This quantity is a declared mathematical
invariant, not an established physical energy. The standalone HTML uses recorded
node values and port packets; directional samples are not counted as extra stock.

Boss, field, architecture, test, physics-review, run and PR Skills were reviewed.
Their existing links already route to the updated owner contracts, so no
duplicated procedural rules were added to Skills. Generated run files remain
outside source commits and follow the existing output-retention policy.

## Merge follow-up: affected checks — 2026-09-12

While combined feature head `4dfc1df7543aa7e7568f5112e2e2eb879e464714` passed
GitHub Actions run `34678735217`, main advanced to
`64d26a89842637ab71517ec45aebfa7c3deae331` through PR #29. That change affects
validation selection and contributor guidance, not simulation code. The merge
preserves its default affected-code checks, full-history checkout and explicit
base selection, together with one-day CI artifact retention. Unconditional
example runs and package builds are removed from CI as required by current main.

The new check-scope report uses the existing exact-file retention lease; it does
not claim the whole artifacts directory. Explicit selector edges retain the
generic identity suite's dynamically selected examples and the historical
runpy tool's application consumer. Dry-run selection creates no output.
Current contributor and specialist guidance already defer to the check command
and affected dependencies; no additional Skill change is required.

`python tools/check.py --base 4dfc1df7543aa7e7568f5112e2e2eb879e464714` selected
the selector, language and navigation suites: 29 tests passed in 4.57 seconds,
with Ruff lint/format passing for both affected Python files. Seven selector and
report regressions failed before the integration corrections; all 15 selector
tests now pass, including active writer protection and failed-command expiry.
No `src/event_universe` file changed: runtime fingerprint `cf684492a86605a68c29aba0a169a6e992478b2f7f7b3d70804e8fce7f2d4f4a`
and the preceding simulation, full-gate and packaging evidence remain applicable.
The exact selected commands are recorded in the leased `artifacts/check-scope.json`.

## Merge with atomic interactions — 2026-09-12

The authorized PR #27 merge found that main had advanced through PR #28 to
`15029ba8d02bd7f1bb1dd1148fe55405ec1536b1`. The integration combines that exact
main tree with tested feature head `137830fd621b9522598e0719e7bd2055ead595a9`.
Signed commit, tree and blob hashes were verified through the GitHub connection
before the local merge. The previous head's CI pass alone was not reused as
evidence for the combined source.

Conflict resolutions preserve recursive spatial flux when adding integer
dot/matrix/comparison operators, all optional initial-state fields, both spatial
schemas and boundaries, spatial work scheduling and atomic pair rules. API
assembly retains spatial planner/coupler/decayer injection. Replacements preserve
carried residuals and finite allowances. Atomic interactions follow proposed
spatial response and ordinary exchange, before routing; invalid carrier proposals
do not roll back earlier independent field transport or emission.

The initial independent conflict-resolution review passed 301 focused cases.
Four new combined numerical tests and the original atomic/language cases passed
26 focused checks. A spatial Z turn followed by an atomic swap yields carrier
vectors `(0,-1,0)` and `(0,5,0)` with opposite recoil `(4,-4,0)`; first-link half
retention accounts for survivors `(2,-2,0)` and equal signed loss. Raising the
coupling price by six increases local cost by 18 across the three responses.
Delayed commits retain the frozen response while emission exhausts its allowance;
nested transform/dot/comparison expressions retain delivered flux context. A
rejected atomic proposal leaves earlier independent emission accounted.

Independent physics-rule review found no additional ownership, locality, timing
or conservation blocker. The first full-gate attempt stopped at mixed line
endings in two resolved files; Ruff normalized those endings without a semantic
change. The final runtime fingerprint is
`cf684492a86605a68c29aba0a169a6e992478b2f7f7b3d70804e8fce7f2d4f4a`.
Wheel and sdist build and asset/source equality checks passed in the leased
`../runs/merge27-packaging/` directory. The packaged source precedes this
evidence-only documentation addition. No visualization was requested or generated.

The unchanged full gate passed: 1,093 tests, 30 explicitly visual skips, Ruff
lint/format (169 files) and strict mypy (66 source modules), in 120.05 seconds.
Independent headless comparisons against archived feature `137830f` retained
byte-identical initialization, ordered events and final state for `open_world`
(12 ticks), `three_mass_finite` (120) and `spatial_turning` (12), with equal
per-tick snapshots and ledgers. Metadata excludes only source identity and host
elapsed time. The new collision separately passed 360 ticks with mass 5,
momentum `(5,0,0)` and kinetic diagnostic `35/2` throughout; contact is at tick
120, reversal at 121, final X positions 3 and 13 and every link takes one tick.
No old-source equivalence is claimed for that new example.

The comparison archives identify Python fingerprints `df6553380020d5c6ccebc2f4b2f64687141c66938ac9e08528a5792dc795f812`
(baseline) and `f6d202ba997eaf4bf35ad3c63f0aa37680926aae50be676dd68a8edb32c49d25`
(combined snapshot). Only verified CRLF/LF normalization in two files separates
that snapshot from final `cf684492`; the final source passes the full gate.
Temporary run, comparison and source-normalization records live under
`../runs/merge27-regression/`, with the same 24-hour artifact policy.

The workspace includes all 11 packaged templates. Shared workflow, Boss and
PR-review Skills were reviewed; their existing rules already require refreshed
main, coordinated provider/consumer reconciliation and current-tree validation,
so no additional procedural rule was needed for this merge.

## Genericity audit — 2026-09-12

The audit continues published feature head `188e3d3` on main base `c252254`.
It covers the active initialization-to-law-to-engine path, spatial responses,
costs, timing, ledgers and workspace adapters. No physical engine, parser or
arithmetic implementation changed. Historical named research APIs remain
explicit model selections, not the primary generic Simulation.

| Check | Result |
| --- | --- |
| Active engine/field review | No physical-name or model-ID dispatch; 233 focused existing tests passed |
| Durable identity regressions | 18 cases compare six scenarios across six transitions after renaming labels/units, reordering declarations, or both; snapshots, complete ordered events, costs, timing and ledgers agree |
| Executed behaviors | Source updates, splitting, delayed commits, cost reporting, paired exchange, finite emission/decay, norm-preserving rotation, delivered flux and open exits are required to occur |
| Independent composite audit | 744 snapshot/event/accounting comparisons passed across eight boundary/transit/budget combinations; low budgets actually reduced committed cycles |
| Editor fixes | Draft storage retains arbitrary template keys, including `__proto__`; generated field/type names skip existing declarations without changing defaults |
| Failure-before evidence | Eight new editor cases failed before the fix; the historical diagonal tool separately failed to import its obsolete Simulation name |
| Focused verification | 60 workspace tests and 9 historical application tests passed; one explicitly visual application case skipped |
| Independent diff review | No blocking finding; all 30 selected new regressions passed |
| Unchanged full gate | Ruff lint/format and strict mypy passed; 1,075 tests passed, 30 explicitly visual cases skipped in 118.03 seconds |
| Static scope | 167 formatted Python files; 66 typed package modules |
| Packaging | Wheel and sdist built in a leased temporary source copy; packaged editor bytes match source and sdist includes the new identity suite and explicit historical tool |

The Python runtime fingerprint remains
`f2cfc31cb5d85bd3dc414d871c36bde17453b0773e9bc51505b2424474a7893d`.
Temporary build/equality evidence is under `../runs/genericity-packaging/`;
the full gate report is `artifacts/junit.xml`. Both follow the 24-hour output
retention policy. Package source checks preceded this evidence-only addition.

The historical diagonal tool now imports `ScalarSimulation` explicitly; its
regression checks importability without rendering. The editor fixes affect
configuration handling only. Identity comparisons normalize semantic labels,
preserve ordered rules/axes/seeds and require nonzero activity. They establish
the tested scenarios and duration, not equivalence of every private register or
arbitrary user-defined algorithms.

The movie currently omits spatial populations and spatial transfers, although
those remain in saved state/recording data. Spatial extension settings remain
editable through complete JSON. This capability limit is documented in
[WORKSPACE.md](WORKSPACE.md); no visualization was requested or generated.
The architecture-review Skill now requires role-aware renaming, declaration
permutations and observed activity. Shared workflow and Boss guidance were
reviewed and already cover integration ownership and the required full gate.

## Generated-output retention — 2026-09-12

This host-only update continues published feature head `45da520` on main base
`c252254`. The policy and ownership rules are in [RETENTION.md](RETENTION.md).
Physical laws, costs and simulated time are unchanged.

| Check | Result |
| --- | --- |
| Unchanged full gate | Ruff lint/format and strict mypy passed; 1,045 tests passed, 30 explicitly visual cases skipped |
| Static scope | 166 formatted Python files; 66 typed package modules |
| Expiry and safety | Exact 24-hour boundaries, latest-write extension, active writers, orphan-child dependencies, source/link rejection, generation replacement, interrupted quarantine/reuse, verified adoption and singleton watcher covered |
| Runner/UI integration | Successful, failed and cancelled jobs, real HTTP/CLI equality, expired links and fresh/empty/sibling-relative output paths covered |
| Independent review | Filesystem replacement, interrupted cleanup and orphan-parent probes passed; existing artifact inventory excludes source and original example/configuration directories |
| Headless regression | Final 12-tick open run has byte-identical initialization, events and state to the prior published run |
| Packaging | Wheel and sdist built; four changed package modules match final source bytes, and sdist includes the retention contract |
| Local operation | 192 reviewed generated files enrolled with expected filesystem identities; no historical file was over 24 hours old, so initial cleanup removed none |
| Scheduling | Hidden singleton watcher started for five reviewed local output roots; a second start confirmed it already running; hourly thread automation `universe24` maintains it and catches up after interruption |
| Automatic deletion | The running watcher removed a newly registered, deliberately expired generated probe without a manual cleanup invocation |

The five operational roots are this workspace's `runs/` and the `artifacts/`
directories in `Universe24`, `Universe24-fields`, `Universe24-init` and
`Universe24-output`. A separate older UI reports outputs under a sibling
`con/outputs/movie-workspace/` directory. That directory is outside this session's
writable roots, so this deployment does not claim retention coverage there.

The final runtime fingerprint is
`f2cfc31cb5d85bd3dc414d871c36bde17453b0773e9bc51505b2424474a7893d`.
The open-run event hash remains
`42376d9d97516e7d5667d35489e06f7e4db1426666e3e4a0fa359920554273bd`;
the final state hash remains
`7a8f082a80c77a1218bfba678bd8fcf249e531926e08814b1306476b66388320`.
Temporary evidence is in `../runs/retention-open-final/`,
`../runs/retention-validation.json`, `../runs/retention-packaging/` and
`artifacts/junit.xml`; those paths follow the same expiry policy.

The first real sibling-relative CLI invocation exposed an unnormalized `..` in
its lease target. Both runners now validate the original lexical path before
passing its resolved path to retention; dedicated regressions cover that case.
The unchanged full gate was repeated after this correction. No visualization
was requested or generated. Workflow and simulation-runner guidance now require
temporary-evidence handling and explicit ownership for custom diagnostics.

## Publication integration with the configuration workspace — 2026-09-12

The publication candidate combines local field head `d3bb0ce` with exact remote
main `c252254eecb5e3b090f9ae40667c383db11a14fc`. Remote Git objects were obtained
through the authorized GitHub connection and their content hashes verified before
integration; the local Git HTTPS client could not authenticate. Main's workspace,
movie assets, presets and parser interface are preserved.

The integration fixes three consumers: terminal movie transfers accept a missing
destination and retain outward coordinates in open worlds; results distinguish
balanced loss/escape from failed accounting; renaming fields also updates nested
flux expressions. These changes do not modify physical engine calculations.

| Check | Result |
| --- | --- |
| Unchanged full gate | Ruff lint/format, strict mypy, 970 passed; 30 explicitly visual cases skipped |
| Static scope | 161 formatted Python files; 65 typed package modules |
| UI regressions | 13 headless JavaScript cases passed, after 10 failed before the fixes; existing periodic/accounting controls retained |
| Workspace regressions | 19 passed, including real HTTP submission of the finite open example and exact signed escape/loss totals |
| CLI/workspace equality | All input, state and event bytes remain exact; metadata equality excludes only the validated host elapsed timer |
| Integrated periodic run | 5,000 ticks in 10.481 host seconds; event and state files byte-identical to the verified pre-integration run |
| Integrated open run | 12 ticks; event and state files byte-identical, carried escape 72 and spatial escape 20 plus loss 52 |
| Packaging | Wheel and sdist built; packaged topology and changed UI assets match current source bytes |
| Visual inspection | Not requested; no visualization generated |

Both integrated runs balanced every completed tick. Their runtime fingerprint is
`26d7ad18f8eef8581168a6e926d7266605bc286d199437207763a54eb6a67e42`.
Canonical evidence is in `../runs/publish-periodic-5000/` and
`../runs/publish-open-12/`. The earlier benchmark still identifies its own source
and does not imply a new timing comparison. The full gate writes
`artifacts/junit.xml`; package evidence is outside the checkout in
`../runs/publish-final-packaging/` and `../runs/publish-final-build.log`.

The first merged gate exposed two obsolete test expectations: the template list
omitted five new examples and metadata byte equality included elapsed host time.
The final tests enumerate all intended examples, validate the timer and preserve
all physical equality checks. No failed physical requirement was removed.
The publication PR records remote commit and CI status; integration into this
feature branch is not a claim that the feature is merged into main. Existing
workflow and specialist guidance already require consumer validation and exact
source identity, so this integration needed no further Skill change.

## Configured boundaries and spatial scheduling — 2026-09-12

This change continues local `4a976f827ae62e16e5d23e319b1d2ce963227d9e`.
The user selected opposite-face reentry for a closed world and removal with
escaped-quantity accounting for an open world. Both schemas default to periodic
boundaries; the chosen configuration applies to carriers and spatial fields.
See [the boundary contract](DISTURBANCES.md#domain-boundary).

| Check | Result |
| --- | --- |
| Unchanged `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 935 passed and 28 explicitly visual cases skipped |
| Static scope | 156 formatted Python files; 64 typed package modules |
| New tests | 121 cases across configuration/topology, open ownership/escape, dormant scheduling and headless boundary output |
| Independent physics review | 264 affected/regression cases passed; 12 additional open/periodic, transit 1/2/3 and ordinary/delayed-budget runs matched full-sweep snapshots, events and accounting over 90 ticks each |
| Independent inventory audit | Full cell/link inventory equals indexed totals after every reviewed tick; skipped cells have no populations, pending receive cost or reported local cost |
| Periodic faces | All six positive/negative faces of a 3x4x5 domain wrap without changing the carried vector; arrivals at ticks 3 and 6 retain the full transit time |
| Terminal field exit | Original signed payload escapes after full transit; no outside cell, attenuation, merge, receive event or receiver cost |
| Open CLI example | 12 ticks, carried escape 72; spatial injection 72 = escape 20 + dissipation 52; no remaining carrier, dynamic stock or packet, and no outside address |
| Three-carrier CLI | 5,000 ticks completed in 10.356 host seconds; three records and mass 10 retained; every completed tick balances |
| Canonical periodic regression | Full ordered event file is byte-identical to the prior verified finite run; final state matches after removing only new boundary and escaped-ledger metadata |
| Package build | `python -m build --no-isolation` built wheel and sdist |
| Visualization | Not requested or generated |

The performance comparison used exactly the same initialization bytes, 5,000
ticks and per-tick accounting plus three-record checks. The baseline was a
verified archive of commit `4a976f8`; the candidate was an identified source
snapshot. Each source was run once for this comparison. Host times were:

| Measured work | Baseline seconds | Candidate seconds |
| --- | ---: | ---: |
| Simulation stepping | 34.105 | 9.159 |
| Separate accounting and record checks | 40.177 | 1.653 |
| Complete measured loop | 74.393 | 10.920 |

This is approximately 6.8 times faster for that scenario and machine. All nine
saved checkpoints have equal physical values, event counts and modeled costs;
the full final state is equal after removing new boundary metadata. The benchmark
observer did not save an ordered event digest; the separate canonical CLI
comparison above did compare the complete event files. The optimization skips
dormant spatial cell planning and resident-population summation. Empty link
buffers can still be scanned; it does not remove every historical host traversal
or alter the model's local computation charges.

Runtime fingerprint, unchanged across the final runs and independent review:
`dd4ac82debd3fb0e28b33ea4a26297930e42c53d627ca2a69d60c8c934dc56b4`.
The benchmark input fingerprint is
`a89397e6b87f9605c2e7dcc128925f22da23e26e450ccc6f17136c1e102cc74f`.
The canonical periodic example now explicitly includes the default boundary key,
so its input fingerprint is
`2d0742951aa49cbe88e6ae87ffff74859031ffbde301c4e9ade4bed7b4b540cf`.
The open example fingerprint is
`b4e3038d3b0539a7dabc11afd1dd346a272ee51af73c2c81dafd4a65b870d76f`.
Runtime/tools remain CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1.

Saved evidence is outside the checkout: `../runs/boundary-periodic-5000/`,
`../runs/boundary-open-12/`, `../runs/boundary-verification.json`,
`../runs/boundary-performance/baseline-4a976f8-verified/` and
`../runs/boundary-performance/optimized-working-4a976f8/`. Run directories
contain exact inputs, metadata, events and final state. Benchmark directories
contain timing, source identity, checkpoints and comparison reports.

Closed topology does not disable configured decay: combined momentum plus signed
loss balances, while physical momentum alone is not conserved by that law. Open
accounting additionally includes escaped quantities. General self-field
attribution, energy conservation and carrier stopping remain unestablished.
The existing isolated field branch has not been published or integrated into
remote main `c252254eecb5e3b090f9ae40667c383db11a14fc`, which was read with no
open PRs; local fetching remains unavailable. No external Highlights edit is
implied. Boss and affected Skills were reviewed; the shared workflow now requires
import-path and source-fingerprint verification when reusing an editable
environment across worktrees, following a detected wrong-checkout import.

## Finite integer fields and allowances — 2026-09-12

This change continues local `e8e5c4cd59ec3ddd8c191e0faac4468acd0a5d71`.
Schema 2 selects `finite-dissipative-v1`; schema 1 keeps its separately named
conservative law. See [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md) for the law and
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) for independent acceptance inputs.

| Check | Result |
| --- | --- |
| Unchanged `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy, 814 passed and 28 explicitly visual cases skipped |
| Static scope | 152 formatted Python files; 63 typed package modules |
| New tests | 108 cases across schema validation, integer decay, finite source integration and finite coupling allowances |
| Independent physics review | 219 affected/new and retained regression cases passed; separate periodic signed-rotation and single-charge decay-cost checks passed |
| Finite moving source | 40 headless ticks; lifetime injection 720 and dissipation 720; final dynamic field zero and carried strength 72 |
| Three carriers with computation field | 5,000 headless ticks in the original 65x65x65 domain; initial rate c/10 and all three first arrivals at tick 10 |
| Three-carrier balances | Mass 10 throughout; final combined vector `(-1,7,0)` plus signed dissipation `(-1,3,0)` equals initial `(-2,10,0)`; every completed tick balances |
| Spatial extinction | All 2,160 computation units injected by the three sources dissipated; dynamic computation and reaction populations vanish by tick 12; computation baseline remains 1 |
| Rotation | Affordable turns retain carrier norm and commit exact opposite reaction; insufficient allowance rejects both sides without changing fractional state |
| Legacy regression | Existing conservative spatial, movement, coupling, integer, locality, architecture and headless application contracts remain in the full gate |
| Visualization | Not requested or generated |

Final runtime source fingerprint:
`faa5de68bdfb0ceb77ddaa8a75d1bdce18333ef5c019d3c8b7572e4e78d268f3`.
The independent review first recorded fingerprint
`65782ddf166c906c53f0df2dc6e76fb1491a5163c54e3ff2c3aabd1b3f768659`;
the subsequent runtime change was Ruff normalization of mixed line endings in
`initialization.py`, with no arithmetic or scheduling change. The final full
gate passed after normalization. Saved final-source runs reside outside the
checkout in `../runs/finite-fields-v2-verified/` and
`../runs/three-mass-finite-v2-verified/`, with input, metadata, events and state.
The three-carrier initialization fingerprint is
`a89397e6b87f9605c2e7dcc128925f22da23e26e450ccc6f17136c1e102cc74f`.

Decay loss is explicitly nonconservative. The runner reports physical conservation
as false for these dissipative examples while its separate loss-accounting check
passes. No energy law, general self-field attribution or automatic carrier rest is
claimed. The old no-decay 5,000-tick experiment remains paused at tick 140 and is
not resumed under the changed law.

Remote main was read at `c252254eecb5e3b090f9ae40667c383db11a14fc`, with no open
pull requests. Local fetching was unavailable; this evidence does not claim the
candidate has been integrated with that main or published to GitHub. The code
remains on the existing isolated field branch. Boss, field development and physics
review Skills were reviewed; their existing candidate, locality, ownership and
independent-validation instructions already cover this change, so no Skill edit
is needed. The latest user request is the authority for the new law; no external
Highlights document was modified in this implementation task.

## Generic spatial exchange and rotation — 2026-09-12

The response extension continues local commit `5ff53888413afd421d129ffacb0d749ca0be8f08`
on base main `a53e1a2f83d4dca898ed827b2f6e4d101932be95`.
[SPATIAL_COUPLINGS.md](SPATIAL_COUPLINGS.md) defines the selected integer law,
local sampling, atomic recoil, timing and fixed preparation tariff. This section
supersedes the earlier outward-only candidate's missing-turning limitation;
general source attribution is still a separate unimplemented capability.

| Check | Result |
| --- | --- |
| Unchanged `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 706 passed and 28 visualization cases skipped |
| Static scope | 147 formatted Python files; 62 typed package modules |
| New response suite | 53 passed: signed axes, axis order, zero/invariant axes, carried fractions, scalar flux, routing, frozen samples, exact reaction arrival and atomic overflow |
| Independent physics review | Scoped pass on final runtime fingerprint; 157 relevant cases and nine additional signed-rotation/transit examples passed |
| Three-turn CLI example | Completed ticks 1, 2 and 3 at `(15,16,15)`, `(14,16,15)` and `(14,15,15)`; vectors `(0,5,0)`, `(-5,0,0)` and `(0,-5,0)` |
| Rotation accounting | Carrier squared norm stays 25; total carrier plus field vector stays `(5,0,0)` at every completed tick; source vector remains zero |
| Moving-source regression | Five ticks; source strength 72, spatial stock and injected amount both 360; all completed ticks conserve |
| Basic/exchange regression | Saved state and event files remain byte-identical to unmodified-base runs |
| Visualization | No visualization requested or generated |

Runtime source fingerprint:
`d06be12cd1a88df93b2cd9f8523344ddce2bc18827ce2839beb147f607056505`.
The turning initialization fingerprint is
`6cf38af8b1078cbfb53c9085ead7062c0c338cce97f028f10465645b2a32561f`.
Saved runs are outside the checkout in `../runs/spatial-coupling-validation/`:
`spatial_turning/`, `moving_source/`, `basic/` and `exchange/`, each with input,
metadata, events and final state. The full gate writes `artifacts/junit.xml`.
Runtime/tool versions remain CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7 and
mypy 2.3.1. Source fingerprints depend on exact file bytes, including line endings.

The three field reactions are `(5,-5,0)`, `(5,5,0)` and `(-5,5,0)` at their
respective local commits. Immediate and delayed cases verify first field arrival
at `commit_tick + link_ticks`, including transit times one and two. The independent
review also checked transit time three with a non-cardinal `(2,3,4)` vector.

Straight cardinal scalar-flux rotation passes an isolated-source control without
changing its vector or fractional state, while an external transverse pulse acts.
This is a geometric property, not a general self-filter. A separate diagnostic
in `../runs/spatial-coupling-review/` confirms a bounded own-front estimate for ten
straight steps and a straight/wait sequence. An unpaused turn has actual own stock
48 but a one-path estimate 42 at tick two; periodic return has actual 24 versus
estimate zero. These diagnostic references never feed the simulator's physics.
Continuous-angle rotation, general self attribution and general energy or angular
momentum conservation are not claimed by the discrete response law.

The field-development Skill now distinguishes combined vector conservation from
carrier norm and requires an external transverse control, causal reaction packets
and accurate cost-tariff wording. Shared, Boss, architecture, test and physics
Skills were reviewed; their existing instructions needed no additional change.
Highlights was read on 2026-09-12 at the same revision as the preceding integration;
the new executable contract is persisted here, without modifying that document.

## Configured outward spatial fields — 2026-09-11

This optional candidate is based on main
`a53e1a2f83d4dca898ed827b2f6e4d101932be95`. Its transport, timing and remaining
model gaps are defined in [SPATIAL_FIELDS.md](SPATIAL_FIELDS.md). The implementation
separates a continuously emitting carrier from its spatial stock and selects the
new law explicitly through initialization. This section records local evidence;
the submitted PR records its exact commit and remote CI result.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 653 passed and 28 visualization cases skipped |
| Static scope | 144 formatted Python files, 61 typed source modules |
| Independent physics review | Scoped pass on the final source fingerprint; 104 relevant cases passed, including fixed transit, signed conservation, delayed proposals and carried fractions |
| Moving source example | Five completed ticks; carrier advances one cell on each tick, from `(15,15,15)` to `(20,15,15)` |
| Source accounting | Carried strength stays 72; initial spatial stock 0, committed emission 360 and final spatial stock 360; balance checked after every completed tick |
| Existing basic/exchange examples | Final state and event files are byte-identical to runs from the unmodified base tree |
| Paired vector rotation | 16 additional numerical cases passed across eight rotations/sign cases and two computation budgets; component-wise recoil balance preserved |
| Package build | Wheel and sdist built successfully with `python -m build --no-isolation` |
| Visualization | No visualization requested or generated; rendering-only tests were skipped |

The moving-source run and independent review identify the runtime source as
`b1a958835fc92efe8f6a584dfa4c3fae4abd5427d47b77e8664a131185e09c81`.
The saved initialization fingerprint is
`3f9fcee4b315698e31794d9eedbcf1ce954010a85b41484f3719f3f70c41a862`.
Local evidence is preserved outside the source checkout in
`../runs/spatial-validation/`, including `current-moving_source/`, the two
baseline/current comparisons, package outputs and the build log. Each run has
its initialization bytes, events, final state and `run.json`. Additional rotation
evidence is in `../runs/rotation-conservation/`. The full gate writes
`artifacts/junit.xml`. Source fingerprints depend on runtime file bytes and may
differ across platform line endings.

Runtime and tools: CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7, mypy 2.3.1,
build 1.6.1 and setuptools 84.0.0. The shared, Boss, architecture, test and physics
Skills were reviewed; their existing rules were sufficient. The field-development
Skill now requires coarrival, turning and periodic-return checks before claiming
self attribution, and distinguishes illustrative shells from executable rules.

Automatic self-field subtraction and spatial-field-driven turning are **not
implemented**. Equal-speed coarrival and alternate field paths invalidate the
proposed first-arrival proof; merged integer rounding also prevents inferring an
exact self contribution from a single tracked path. The existing paired-record
rotation checks do not establish that missing law. The new field clock is fixed
at one link per `link_ticks`; priced spatial work can delay a new carrier cycle
but does not throttle spatial forwarding. This timing choice is explicit in the
candidate contract, not evidence that the earlier uniform-delay law is unchanged.

## Initialization-defined disturbances — 2026-09-11

The generic implementation was integrated with main
`ec0826b20286a166498beacd6cb68002624826eb`, including its historical renderer
performance and concurrent-preview changes. The active CLI requires `--init`;
historical scenarios use `event_universe.legacy_runner`. Both paths are headless
unless visualization is explicitly selected. This section records local
verification; the submitted PR records the remote commit and CI result.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 569 passed and 28 visualization cases skipped |
| Static scope | 133 formatted files, 57 typed source modules |
| Initialization | 42 checks cover schema bounds, expressions, arbitrary names and invalid input |
| Generic ownership and arithmetic | 23 checks cover signed scalar/vector conservation, whole-record movement, coupling, exact delay, frozen proposals, capacity and failure atomicity |
| Generic application | 12 checks cover required input, headless imports/output, input-byte identity, failed-tick reporting and renamed simulation equivalence |
| Independent physics review | Six reproduced defects corrected and covered; scoped review passed, including pair-remainder lifetime and counterflow channels |
| Basic example | 8 completed ticks; initial/final totals mass 2, charge -1, signal 12; conservation checked after every completed tick |
| Exchange example | 8 completed ticks; initial/final balance 8; conservation checked after every completed tick |
| Visualization | No world visualization generated; rendering-only cases require `--visualize-runs` |

Both final example runs have local source fingerprint
`3f26ce8cb69c01368f4b04166c82bdaafe2a2db4b6d6381ea5215f1e6f2ebe6b`.
Their preserved outputs are `artifacts/basic-final/` and
`artifacts/exchange-final/`, each containing the exact initialization bytes,
events, final state and `run.json` metadata. The full gate writes
`artifacts/junit.xml`. Source fingerprints identify runtime file bytes and may
differ across platform line-ending conventions.

Runtime: CPython 3.14.7. Tools: pytest 9.1.1, Ruff 0.16.7, mypy 2.3.1,
build 1.6.1 and setuptools 84.0.0. Historical fixed-physics regression contracts
remain active under their named APIs. The new framework supports same-field
paired exchange, fixed capacity and bounded integer laws; it does not establish
gravity, wave equations, relativity or arbitrary energy conservation.

The agreed high-level specification was reconciled with Universe 24 Highlights
on 2026-09-11. Detailed executable requirements are in
[DISTURBANCES.md](DISTURBANCES.md), with inputs and acceptance cases in
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md). Earlier evidence below describes
historical candidates and earlier output defaults.

## Python 3.14 and necessary tests — 2026-09-11

Validated locally with CPython 3.14.7 in the project virtual environment, based on
main `7e517afb7a274821de05bf247ece91827c1b030b`. The runtime selection, CI and
agent workflow now use Python 3.14. Older-Python, archived-v10 equality and
historical facade API tests are no longer gates, as requested by the user.
Current physical contracts and known failure evidence remain covered.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint/format, strict mypy and 461 pytest cases |
| Static scope | 114 Python files formatted; 48 package modules type checked |
| Test reduction | Four fewer collected cases, six fewer worlds and 447 fewer simulation ticks |
| Test visualization | All 94 current-engine worlds rendered through the existing HTML/GIF pipeline |
| Contact CLI | Completed 48 ticks; momentum equal at every completed tick; all state audits passed |
| Visual inspection | Contact frame at tick 24 shows both particles, field, axes and total momentum (0,0,0) |
| Package build | Wheel and sdist built; minimum Python is 3.14 and sdist includes `.python-version` |
| Agent Skills | Boss, architecture, regression and necessary-tests Skills validated; shared workflow updated |

Installed project tools: pytest 9.1.1, Ruff 0.16.7, mypy 2.3.1, Matplotlib 3.11.1,
Pillow 12.3.0, NumPy 2.5.3 and build 1.6.1. Isolated package build used
setuptools 84.0.0. Contact source fingerprint:
`c7696ccccad62080363a35673f9e6be053c3f5461909160de8792abc8b621256`.

The remaining suite is defined in [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md).
Local outputs are `artifacts/junit.xml`, `artifacts/test-runs.html` and
`artifacts/contact/run.html` with run metadata. The integration PR and its Actions
run record the remote result for the submitted commit. No old-Python or archived
engine compatibility run was performed. Earlier evidence below is historical.

## Historical validation — 2026-09-10

The required checks were executed locally on Python 3.12. GitHub Actions is
configured but was not executed on a remote repository in this task.

| Check | Result |
| --- | --- |
| Ruff lint | Passed |
| Ruff format | 52 Python files already formatted |
| mypy strict | Passed, 26 package modules |
| pytest | 206 passed, 0 failures, 0 errors, 0 skipped |
| Frozen-reference comparison | Exact after all 278 compared ticks |
| Contact application run | Completed 48 ticks; total momentum equal at every tick |
| Turning application run | Completed 110 ticks; total momentum equal at every tick |
| Generic field/turning | Signed and weighted fields, exact residues, direction policies and bounds passed |
| Current model | Exact field sample, source mapping, clipping and transverse response passed |
| Public component replacement | Field/turning/activity injection, remainder-only evolution and invalid-result rejection passed |
| Calculation boundaries | Absolute/relative imports and formula-free assembly checked, including forbidden-example tests |
| Dedicated expectations | Lattice, movement, source/range/activity policies and all diagnostic projections passed |
| Test visualization | 41 engine/reference runs rendered through the shared GIF/HTML pipeline |
| Full XYZ display | 48-tick contact run completed with total momentum preserved; shared GIF/HTML pipeline |
| Display equivalence | Plane and volume runs produced identical physical events and final reports |
| Visual inspection | Final frames of contact and turning checked; plane labels visible |

The full-state comparison checks every materialized cell, particle register,
occupancy slot, active-frontier member, force record, blocked move and path entry
after each step. It covers 120 stationary-source steps, 48 contact steps and 110
turning steps. This is evidence for those scenarios, not a proof over all inputs.

The contact event first has transverse impulse `(0,1,0)` at event tick 15, visible
in the completed frame labelled tick 16. Event records use the tick being
processed; completed frames use the count of finished ticks. This is the
preserved v10 convention.

Source fingerprint used by the preserved plane application runs:
`66855a6339d5ef4448c94ed8e47db7366a7387ea2d816aab7bedb1821d5494df`.

The full XYZ contact visualization uses source fingerprint
`47b24f3f6c8446a39c93e8badcb3baa305b4454e66ddc29fd76accd671914349`.
Its midpoint was visually inspected. After the suite, only display color,
marker size and opacity were adjusted; the XYZ demonstration was regenerated.

The source-only scalar field and full-vector turning variant are test fixtures.
They demonstrate component replacement through `Simulation`; the production
default model and its identifier remain unchanged.
An additional local-retention fixture verifies the expected sample sequence
`(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0)`, ensuring a replacement
field is not stopped while only its remainder changes. Calculation inputs,
expected outputs and ownership are documented in `TEST_EXPECTATIONS.md`.

| Tool | Version |
| --- | --- |
| pytest | 9.1.1 |
| Ruff | 0.16.6 |
| mypy | 2.3.1 |
| Matplotlib | 3.10.8 |
| Pillow | 12.3.0 |
| build | 1.6.0 |
| setuptools | 84.0.0 |

Detailed outputs are in `artifacts/checks.log`, `artifacts/junit.xml`,
`artifacts/test-runs.html`, and each scenario's `run.json` and `run.html`.
Known model assumptions and limits remain in `SIMULATOR_DEFINITIONS.md`.


## v11 local-link candidate validation — this change

- Required `python tools/check.py` completed: Ruff lint/format passed (60 Python
  files), strict mypy passed (31 source modules), **222 pytest tests passed**.
- All original frozen-v10 comparisons passed without changing expected traces.
- Eighteen new tests cover geometry, transport and the linked engine. The
  stationary-source regression initially exposed an owner-only directional
  artifact; the symmetric two-endpoint proposal protocol now passes it.
- 46 engine/reference test runs were captured using the existing renderer.
- The linked application completed 360 elementary ticks on a 32×24×12 lattice,
  with two particles and base link length 10. Total momentum matched the initial
  value at every completed tick. All runtime state audits passed.
- The final rendered frame was inspected: XY slice z=6 and tick=360 are visible.
  Arrows are scaled direction indicators; the drawing remains an address-grid
  view, not a geometrically stretched embedding.
- These tests establish the enumerated locality and numerical properties in
  tested cases; they do not establish Einstein geodesics or gravity. The example
  particles crossed the region on straight tracks; no attraction is claimed.

Current outputs: `artifacts/local-links-check.log`, `artifacts/junit.xml`,
`artifacts/test-runs.html`, `artifacts/local-links/run.json`, `.html`, `.gif`,
`.mp4` and `events.jsonl`. The video is a conversion of the existing GIF replay,
not a separately simulated trajectory.

Source fingerprint for the linked application: `53786817fe9f2c9a089a875894523229b6eb02d52bc077095fea2cc482693875`.


## Concurrent update reconciliation

The archive advanced from version 3 to version 4 while this change was being
implemented. The guarded write rejected replacement of that newer archive.
The full-XYZ renderer, `--view-3d`, its independent frame capture and both new
diagnostic tests were preserved. Link changes were reapplied to version 4.
The required gates were repeated on this merged tree: **224 tests passed**,
Ruff lint/format passed and strict mypy passed. The test renderer captured
48 engine/reference runs. The linked application was rerun from the merged
source; its current fingerprint is recorded in `artifacts/local-links/run.json`.
Earlier evidence is preserved under `artifacts/local-links-before-merge` and
`artifacts/local-links-check-before-merge.log`.
## Executable catalog and bounded conversions, 2026-09-12

Base: `d1d7251ba739fb7231eff0d41037744456297ddd`. Python 3.14.7.
The affected gate selected 764 passing cases and five explicitly optional visual
skips; Ruff and mypy passed. Selection includes consumers of the shared
initialization, record schema and local interaction law, not a full-suite switch.
All 46 catalog entries compile through the canonical validator. Representative
active worlds cover shared carrier, scalar and vector behavior without repeating
the same dynamics for every particle name.

Independent architecture/physics review found and resolved strict catalog input
validation and a conversion restriction on nonzero arrival channel tags. A real
incoming-pair regression now verifies conversion after neighbor arrival; channel
provenance is preserved while actual carried fractional progress remains rejected.
Boss, architecture, fields, physics, tests and simulation Skills were reviewed;
their existing workflow covers this change, so no Skill edit was necessary.
Highlights was read on 2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
No change to that Google document is implied.

Three CLI runs generated recorded HTML with source fingerprint
`1695a4c8757b6493e5bf58613a6b6cd97e533df81d1f17f58723c9a9354d4fce`:

| Probe | Evidence |
| --- | --- |
| Catalog electron/positron/EM registers | Four ticks; inventory 2, charge 0, momentum (2,0,0), E/B component stock (0,1,0); causal carrier and field transfers |
| `conversion.json` | Six ticks; two held records become outgoing types, stock 5 and momentum zero remain |
| Incoming variant from `test_incoming_carriers_convert_after_real_neighbor_arrival_and_reverse` | Six ticks; seeds at x=3/5 meet at x=4, convert and reverse to x=2/6; stock 5 and momentum zero remain; link time 2 |

Metadata, final states, event traces and HTML data were inspected. Browser visual
inspection was not performed; the existing renderer is unchanged. These are
representation/conversion tests, not physical annihilation, Maxwell, mass,
spinor, gauge, metric or general energy derivations. Git PR/CI evidence identifies
the final integrated tree; generated output follows finite retention.


## Repository consistency baseline — 2026-09-12

The whole-repository audit starts from main
`2e753fed1f6922d9d2082d6d43c9e150f237bdd6` (228 tracked project files).
[Baseline run 34693224761](https://github.com/Closer24/Universe24/actions/runs/34693224761)
executed `python tools/check.py --full` using Python 3.14.7, Ruff 0.16.7,
mypy 2.3.1 and pytest 9.1.1: Ruff check/format passed, strict mypy passed
73 source files, and pytest passed 1,249 cases with 30 explicit visualization skips.
The temporary read-only audit workflow was the only addition in that run;
its source tree was otherwise the recorded main revision.

The inventory found one byte-identical collision configuration pair and no exact
production function-body copies at the inspected threshold of 12 source lines.
This is a duplication heuristic, not proof of absence of semantic overlap.
The cleanup consolidates that input, explicitly names historical scalar owners,
extends source-language/navigation/hygiene coverage and preserves reference files.
Final submitted-tree validation is recorded in its PR/CI, not inferred from this
baseline result. No visual inspection or newly derived physical law is claimed.
