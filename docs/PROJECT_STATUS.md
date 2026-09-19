# Project status and restart guide

## Where the project stands on 2026-09-19 (read this first)

**Two laws are recorded, two engines are in the code, one is the working one.**
Everything below is on `main`; nothing is in a branch or a machine.

1. **The law of the bit** ([Highlights](HIGHLIGHTS.md) section 5.4, points 1 to 25 with
   their glossary): every ray is a thing (1) or its shadow (0), a thing walks one path,
   a shadow is the thing's field and spreads by the Node's mixing (point 24), a shadow
   meeting a thing pushes it and is turned back (point 3), a thing at rest reads the
   count for its push and the size for its wait (points 16 and 23), the charge is per
   thing (point 16 as amended), a thing emits its shadows every interval and a shadow
   never disappears, and the board of a run is open (the evening's paragraphs of
   2026-09-18). Its engine is the old one: `src/event_universe/core/`, `fields/`,
   `dense_field.py`, `prefill.py`, every world under `examples/nature/` and the
   catalog, about 700 tests, all green. Its confrontation runs of 2026-09-18 (E11,
   A5s, E9, A1, A6 on closed boards, before the emission was decided) are registered in
   [EXPERIMENTS.md](EXPERIMENTS.md) as measurements on a field that never settles:
   the count-reading and the closed board give no static force (DERIVATIONS.md round 7,
   Theorem 1), which is what forced the emission and the open board.
2. **The law of the shadow** (Highlights 5.4, the paragraph "The law of the shadow: only
   shadows and events", the model owner's words of the evening of 2026-09-18; the
   whole document annotated to it on the same day, the consistency table at the end of
   5.4): "No real and shadow. There is only shadow. There are events, which are a whole
   quantum. That is all. The shadow spreads like a ray from the event." Matter is
   content held at Nodes; every ray in flight is a shadow; an event is a whole quantum
   at held content. It is derived in [DERIVATIONS.md](DERIVATIONS.md) round 8 (sections
   51 to 56: the law in points S1 to S10 as a draft for the owner, stability, the step
   and the speed, inertia, the tests one by one, the verdict table, the Node rule in
   pseudo-code) on round 7's fixed point (sections 45 to 50). Its engine is the new one,
   `src/event_universe/shadow/` (feature 20, `field-only-v1`, PR #327), selected by a
   world's `"law": "shadow"`, with `tests/test_field_only.py` and the worlds under
   `examples/shadow/`. **It is under test and not the working law** (the model owner,
   2026-09-19): it becomes the law only after it has repeated every confrontation on
   open boards (E11, A5s, A6, A1, E9) and the readings were registered. Until then the
   old engine stays; when it passes, the old engine is retired in a cleanup and this
   becomes one engine. The gate of the morning (feature 20b, `shadow-gate-v1`: a world
   refused unless it declared `transmitted_number`, `wait_per_quantum` and `epsilon_g`)
   was withdrawn by the model owner later the same day ("We do not need these three
   things at all", Highlights 5.4, the status line): it is not written, the keys are
   not added, and the engine runs as it stands. PR #331, which made the gate the first
   task, is superseded.

**What the new engine already gave on its first worlds** (test_field_only, pinned before
the runs): Gauss's flux through every shell equal to the emission within 2 %, the count
falling as r^-2.00 and the size as r^-1.05, the third law within 2.1 %, the product law,
two slits giving fringes in the counts event by event (ratio 3.2, the one-slit control
monotone), the wait falling as r^-0.9.

**What is open, by whose hand:**

- The model owner's decisions (round 8's verdict table, PR #327's "Needs a decision",
  Highlights 5.4's status line): the law in points S1 to S10 point by point; T2 (an
  event takes its interval); what a matter shadow rotates by;
  hypothesis 19 or a per-family w (the bending of light: half of Einstein with one w,
  whole if light pays twice); the Compton table; the parked share's phase (1.5 % of the
  emission stands still); a lamp's recoil; the plain or matched edge. Settled on
  2026-09-19 ("We do not need these three things at all"): the number a transmitted
  quantum carries is the last emitter's, the wait's unit is the size read, one interval
  per whole unit, and there is no gravity multiplier ε_g; the hierarchy of section 55
  (x) stays an open question of the model, not a parameter.
- Derived and not solved by either law: no inertia for a co-moving pair at first order
  in v (section 54: the lattice's preferred frame for composite matter); no mass ladder
  under the law of the shadow (bound contents give Kepler's continuum; the law of the
  bit had one from loop-binding, hypothesis 12); Bell at most 2 (both laws, section 55
  (ix)); the field of a small content is a haze, not a wave (sections 47 (iii), 52 (v)).
- Runs to make on the new engine, in this order, each with a page and a GIF: E11 (one
  held content), A5s (two), A6 (the four tests on an open 33³ board), A1 (a lamp with
  q_γ ≥ 2·10⁶ per quantum), E9. DERIVATIONS.md section 56 gives the worlds and the
  numbers that decide.

**How the work is done** ([AGENTS.md](../AGENTS.md)): every model decision is recorded in
Highlights the same day in the owner's words, elaborations flagged; one feature per
branch and PR with one isolated test module; `PYTHONPATH=src python tools/check.py
--base origin/main` locally (the whole suite in CI); merge commits, never a rebase;
experiments registered in EXPERIMENTS.md with their digests; hypotheses numbered in
HYPOTHESES.md; the engine documented in SPATIAL_FIELDS.md (both engines) and its
features in HIGHLIGHTS_IMPLEMENTATION.md; every deletion in MIGRATION.md.

**Everything is in git.** The history is merge commits only; `git log --first-parent
main` reads the day by PRs (#278 to #329 on 2026-09-18 and 19). Any earlier state can be
checked out; the old engine needs no checkout, it runs today.

[Local Focus](LOCAL_FOCUS.md) defaults on: certified empty carrier Nodes sleep,
and equal complete local planning inputs reuse immutable pure transition results.
Host transport indexes active output banks in their original creation order.
Shared field clocks retain the ordinary carrier scheduler. Model operation costs,
local commit timing, events and physical owners are unchanged. Measured savings
and the low-repetition case without a benefit are in [performance](PERFORMANCE.md).
The integrated ray policies validate retained rays and incoming ray bundles,
retain funded emissions during load delay, and prepare bounded immutable pace
tables. Exact share capture and whole-ray threshold funding have regression
coverage. Unsupported self-exclusion compositions fail preflight. The bond
registry, claim-gather, the lottery capture and the occupied-links guard were
deleted on 2026-09-17 (issue #164, bucket B.5) under
[Highlights](HIGHLIGHTS.md) 3.18 (deleted), 3.19, 3.20, 5.1 and 5.4, after the
explicit Q-ORACLE option went the same day with buckets B.1 and B.2; see the
[migration note](MIGRATION.md#bond-registry-claim-gather-lottery-capture-and-occupied-links-guard-deleted-on-2026-09-17).
See the exact submitted source and check results in the integration PR.

The shared quantum resource and its integration layer, with the position-output
and local moment-response experiments, the recurrent, causal-source and
localized-contact profiles, the quantum origin cells and the native event
programs, were deleted on 2026-09-17 under Highlights sections 3.18 (deleted),
3.19, 3.20 and 5.4; see the
[migration note](MIGRATION.md#shared-quantum-resource-and-integration-layer-deleted-on-2026-09-17).
Their dated evidence stays in [validation](VALIDATION.md). The source-envelope
modules were deleted on 2026-09-17 under Highlights section 3.5 (bucket B.3;
see the [migration note](MIGRATION.md#source-envelopes-deleted-on-2026-09-17)),
the causal event ledger under Highlights section 3.20 (bucket B.4; see the
[migration note](MIGRATION.md#causal-event-ledger-deleted-on-2026-09-17)) and
the bond registry and claim/gather the same day with bucket B.5, and the record
operations (records as owners, the N-to-M conversion of records) the same day
with bucket B.6, the last (see the
[migration note](MIGRATION.md#records-as-owners-deleted-on-2026-09-17)); every
deletion bucket of issue #164 is done.


The test suite was reduced on 2026-09-17 by decision of the model owner: the
engine is generic, so one module isolates each generic rule on a minimal board
and one module covers each feature of the ray-event model; world-specific
pins, duplicates, experiment-like suites and the dated research studies under
`examples/` were deleted. The kept modules and the rule each one isolates are
listed in [test expectations](TEST_EXPECTATIONS.md#suite-inventory-of-2026-09-17);
the deleted modules and studies are named in the
[migration note](MIGRATION.md#test-suite-reduced-on-2026-09-17-one-test-per-rule).

[Computational response](COMPUTATIONAL_RESPONSE.md) adds an emission-only readout
of the colocated Node's last committed carrier-cycle cost. A moving-pair candidate
uses existing received-port interactions and paired momentum updates. The impulse
law is explicitly configured; gravitational attraction and physical energy are
not established by this mechanism.

The [integer Node profile](NODE_VECTOR_PROCESSOR.md) adds bounded indexed rules,
explicit k*h local duration, declared aggregation and complete-owner pre-commit
readouts. Indexed spatial rules now read several carriers and fields from one
snapshot. Delayed field phases recheck each rule's invariants, and optional
`commit_when` is separate from the consumed `when` trigger. Nodes own their
physical transitions and fixed output banks. Example
configurations demonstrate register permutations and local field exchange;
they do not establish physical species laws or quantum emergence. General graph
topology and interacting coarse-graining remain outside this profile.

The [shared field computation delay](SPATIAL_COMPUTATION_DELAY.md) candidate
adds an explicit configuration switch and bounded later-input ownership.
Existing inputs keep fixed-clock spatial transport. See its contract and
focused tests for supported timing and conservation limits.

The [property coupling extension](PROPERTY_COUPLINGS.md) selects compatible
disturbances by owned properties, retaining explicit types for existing inputs.
Entity probes share two local energy/momentum reservoirs. The optional
[local conservation audit](LOCAL_CONSERVATION.md) measures node changes and
actual link transfers after commits, including merging and later updates.
Checks do not repair state or contribute modeled delay. Quantity definitions
and discrete laws still require independent physical proof.

The optional [coupled unit-excitation probe](COUPLED_EXCITATIONS.md) uses existing
configuration operations for a held internal state and one traveling field mode.
A local gate retains the input during an atomic exchange and releases it afterward.
Its finite occupation and recoil inventory are declared assumptions; massive
motion, photon quantization and QED are not established. The catalog profiles
and simulator code are unchanged.

[Configuration preflight](CONFIGURATION_VALIDATION.md) checks initialization,
physical reference catalogs, all supplied representation profiles and observer
sidecars without running a world. It shares parsing and preparation with runtime
entry points. Configuration validity is separate from run and physics acceptance.

The optional [local reception observer](LOCAL_OBSERVER.md) records arrivals at
one node configured in the ordinary initialization JSON, using a completed local-cycle counter and the existing HTML player.
Global state remains available as an explicit audit view. Optical images, radar
geometry, proper time and Maxwell laws in an emergent spacetime remain open.

An optional [directional-wave candidate](DIRECTIONAL_WAVE.md) supplies six modes
and a configured polarization encounter with exact normalized energy/momentum
guards. It uses the existing local field engine and does not replace the catalog
probes or establish Maxwell dynamics. Verify the current Git tree and PR status
before using historical validation evidence.

For a clean machine or deleted conversation, follow
[recovery without chat history](RECOVERY.md), including the versioned daily
genericity skill and local retention setup.
The [Highlights implementation map](HIGHLIGHTS_IMPLEMENTATION.md) records the
dated Highlights reconciliations, entity coverage and exact source contracts.

The quantum and classical coupling summary, its two-arm interference and
two-wing Bell experiments and the finite quantum-register extension were
deleted on 2026-09-17 with the shared quantum resource.


The local Maxwell experiment (`examples/maxwell/`, deleted on 2026-09-17) selects a
six-population reflection and causal streaming through configuration only.
Its conditional long-wavelength vacuum generator and eleven small-world runs
give two transverse modes with leading speed one half link per tick. Centered
Gauss conservation, exact macro electromagnetic energy and indefinite integer
mixing remain explicit blockers; this is not a complete electromagnetic law.

The small-space comparisons (`examples/small-space/`, deleted on 2026-09-17) record 24
9-cubed/15-cubed entity, source and response experiments. Local accounting and
selected mechanisms pass; field/particle physical laws remain incomplete.
Finite owned-reservoir transfer, a ray-speed parameter and a restricted
zero-total-momentum unequal-mass candidate are explicit configuration solutions,
not replacements for the default entity profiles or derived universal laws.
The inverse-square probe (`examples/inverse-square/`, deleted on 2026-09-17) measures the
outward field from outside the event space: every Manhattan shell carries exactly
one tick of emission, so the shell mean is `emission / (4R^2 + 2)`, while node
values are anisotropic (geometric on axes, about `1/r` on body diagonals). The
straight-ray candidate `isotropic-ray-field-v1` (`"transport": "ray"`) removes that
anisotropy: rays carry their heading and phase, and the time-averaged flux per
node follows solid angle. The gravity probe (`examples/gravity-probe/`, deleted on 2026-09-17)
composes existing rules only: an `exchange` coupling with amount `mass x flux / D`
gives held bodies momentum toward the ray source in proportion to mass, and a
moving body falls inward. The reaction stays in the local momentum field at the
body's Node; no reaction reaches the source, and no gravitational constant is
identified beyond the configured `1 / D`. The
particle interaction probes (`examples/particle-interactions/`, deleted on 2026-09-17) give
all charged bodies one signed ray field with the local one-link `self_exclusion`
rule: like charges repel head-on, opposite charges attract, neutral bodies
cross, and a timed two-record conversion emits a proton with a recoiling core.
Energy has no representation in the exchange rules, so kicks near a source are
unbounded. The [conservation audit](LOCAL_CONSERVATION.md) now measures rays as
quanta, funded emission with recoil and the `absorb` coupling move energy and
momentum only between records and rays; signed quanta with a mass-proportional
absorbed share give attraction that the pulled body pays for, and the
radiation-pressure probe runs
with that audit closed. The quantum-to-classical probes
(`examples/quantum-classical`) were deleted on 2026-09-17.
The [Kerengonen candidate](SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1)
(`kerengonen-ray-field-v1`) gives rays a phase: rays that meet combine by phase,
coherence gates absorption and sampling, and two sources in phase give a fringe
in Manhattan path difference; the plain ray field is unchanged without the key.
The deterministic threshold capture and carried-phase re-emission also run through
the same local ray owners; the whole-ray lottery capture was deleted on 2026-09-17. Prepared immutable phase tables and explicit ray
momentum inventory support ordinary headless runs. Delayed funded/absorbed carrier
plans and phased/attenuating self-exclusion with response couplings are explicitly unsupported;
see the candidate contract rather than treating a passing probe as complete quantum
or gravitational dynamics.

A Huygens slit re-emits the phase and advance it absorbed, so one lamp behind
two slits gives the fringe, and rays may carry their own advance from the
emitter's momentum: the de Broglie probe (`examples/de-broglie/`, deleted on 2026-09-17)
halves the fringe period each time the beam's momentum doubles in its measured
range. The momentum-to-advance relation is supplied by configuration, not derived.
The Bell test on the phased-ray field (`examples/kerengonen-bell/`, deleted on
2026-09-17 with bucket B.5; its numbers stay in [validation](VALIDATION.md))
placed the candidate: with the four CHSH settings of the former quantum owner
(deleted the same day) it measured 1.40 exactly, one half of that owner's
recorded 14/5 in every correlation, and the plain field 2, so the classical
candidate stayed inside the local bound.
halves the fringe period each time the beam's momentum doubles, and the
matter-wave probe (`examples/matter-wave/`, deleted on 2026-09-17) stops a moving particle,
pays its matter out as a wave train and lands it on the screen with the fringe
of the momentum it flew with. A mirror emission re-emits along the reflected
absorbed heading, and the mirror probe (`examples/kerengonen-mirror/`, deleted on 2026-09-17)
reads the standing wave between a lamp and a mirror with period
`phase_steps / (2 x advance)`. A ray field may set `"metric": "euclidean"`
(`euclidean-ray-pace-v1`): rays wait at Nodes by their heading's pace so every
heading covers equal Euclidean distance per tick, and the
Euclidean pace probe (`examples/euclidean-pace/`, deleted on 2026-09-17) reads a round
front and a fringe in Euclidean path difference. The claim-and-gather rule
(`claim-gather-ray-field-v1`, a claim flooding the world at link speed to
gather a captured train), the Bell probe (`examples/bell-chsh/`, CHSH
detectors built from the coherence with the lottery, threshold and bonded
captures) and the gathered-gravity probe were deleted on 2026-09-17 with the
bond registry (issue #164, bucket B.5): under [Highlights](HIGHLIGHTS.md)
3.19, 3.20 and 5.4 the only draw is at a Node whose Detector bit is set, no
registry answers at a distance, and pair identity is the trajectory. Their
recorded results (S = 1.48 for the lottery, 2.00 for deterministic hidden
variables and the quantum value with the registry; a gathered pull that
focused quanta, not a force law) stay in [validation](VALIDATION.md) as
evidence about the deleted rules.

The [physical reference catalog](ENTITY_CATALOG.md) separates sourced properties
and possible interactions from explicitly supplied representation experiments.
It covers 11 field families, 35 particle records and 14 disturbance families, with
17 interaction families and 33 representative channels. No catalog formula,
measured mass or interaction label becomes a simulation law. The original 46
bounded probes live in a separate file and compile into ordinary run inputs.
The [local conversion interface](LOCAL_CONVERSIONS.md) supports explicit atomic
two-to-two type replacement with declared balances. These additions do not
establish physical annihilation, general particle production or physical field
dynamics. Consult current PR/CI evidence for the exact integrated tree.

The [physical entity inventory](PHYSICAL_ENTITIES.md), based on main
`09464b41b2c44a191aa2fcbdf4b036680bd646a5`, separates descriptive entities from
executable mechanics and unestablished emergence. New equal-mass charged-pair
and two-vector port probes use elementary operations only. They do not provide
Maxwell dynamics, gravity or matter/antimatter creation and annihilation.
Use the linked catalog and exact PR evidence instead of treating physical labels
as implemented laws.

Relativity probes, 2026-09-14, branch `feat/self-field-policies-and-carried-phase`
(bottom line of 2026-09-14; `examples/relativity-probes/` deleted on 2026-09-17):
the supplied JSON couplings and declared transport/phase policies produce
finite attraction, velocity-scaling, lensing-like and delay observations.
These are configured candidates, not a derivation of Newtonian gravity or
relativity. Forward replay matched the quantum example's exposed snapshots
(that probe was deleted on 2026-09-17), and the equal-mass collision example returned positions and reversed momenta
after restarting with negated momenta. Neither establishes reversal of arbitrary
hidden state. The radius-independent loss observations remain inconclusive
until the same-metric open-3D control is completed; they do not establish dark
matter. Lorentz dilation, accelerated expansion and gravitating quantum matter
have not emerged in these probes. `ray_delay` and `ray_phase_per_tick` are
supplied engine rules, and physical collision laws are supplied in JSON.

Local field-rule extension base: 2026-09-12, main
`12c85316f011d0601adcd0f4a31f0f52e59eaa27`. The opt-in
[local rule contract](LOCAL_FIELD_RULES.md) adds logical field groups, independent
six-port reads, retained/outgoing field assignments and guarded joint
field/carrier transactions. This is a bounded generic research interface, not
an implemented electromagnetic law. Integration and validation status require
the current PR and its exact tested tree; this paragraph does not certify a run.

Integration reference: 2026-09-12. [PR #27](https://github.com/Closer24/Universe24/pull/27)
combines reviewed spatial-field feature head
`137830fd621b9522598e0719e7bd2055ead595a9` with main
`15029ba8d02bd7f1bb1dd1148fe55405ec1536b1`, which adds atomic generic interactions
and the configured unequal-mass elastic example through PR #28, followed by
main `64d26a89842637ab71517ec45aebfa7c3deae331` and its affected-check selection
through PR #29. Validation selects changed code and reviewed consumers by default;
complete audits require explicit `--full`. See [CONTRIBUTING.md](../CONTRIBUTING.md).
Spatial fields,
finite budgets, boundaries, output retention and arbitrary-name handling remain
included. GitHub-supplied blob, tree and commit hashes were verified before local
integration. Verify live checkout, remote and PR state before continuing; this
reference is not a claim about the version in another checkout. Identified checks
and run evidence belong in [VALIDATION.md](VALIDATION.md).

Registered run outputs,
workspace copies/logs/exports and test reports expire after 24 hours, with live
writer protection; see [RETENTION.md](RETENTION.md). Idle cleanup requires the
watcher or a scheduled invocation. Generated evidence paths in older validation
records are temporary, while their recorded conclusions remain in the repository.

## What this checkout contains

| Scope | Implemented owner | Contract and limits |
| --- | --- | --- |
| Active generic simulator | [disturbance_api.py](../src/event_universe/disturbance_api.py), [disturbance_engine.py](../src/event_universe/core/disturbance_engine.py) | `Simulation(InitialState)`; laws and fields come from explicit initialization, not physical names |
| Carrier Node activity and cost reporting | [disturbance_node.py](../src/event_universe/core/disturbance_node.py) | `carrier_work` and `report_cost`, pure functions over the immutable run definition; an arrival takes a spare slot and nothing merges (the record operation policy was deleted on 2026-09-17, bucket B.6) |
| Rational particle candidates | [rational contract](RATIONAL_PARTICLES.md) | Explicit bounded rational regions, balanced routes, fractional movement credit and local checks; supplied reference laws |
| Local expressions and transactions | [disturbances.py](../src/event_universe/fields/disturbances.py) | Bounded integer operations, declared balances, fixed local capacities and explicit rejection |
| Spatial fields | [spatial_engine.py](../src/event_universe/core/spatial_engine.py) | Fixed neighbor transit, baselines, schema 1 transport and opt-in schema 2 finite budgets/decay |
| Local field read/response rules | [local_field_rules.py](../src/event_universe/fields/local_field_rules.py) | Six-port reads and guarded local field/carrier proposals; no implied Maxwell law |
| Entity reference and representation | [entity_catalog.py](../src/event_universe/entity_catalog.py), [entities.py](../src/event_universe/entities.py), [catalog.json](../examples/known-entities/catalog.json) | Sourced properties and interactions are validated separately; 46 explicitly supplied experiment profiles compile without deriving laws from labels |
| Shared integer arithmetic | [integer.py](../src/event_universe/core/integer.py) | Shared bounded integer primitives; expression evaluation retains its separate owner |
| Local E/B pulse candidate | [local impulse contract](LOCAL_LORENTZ_FIELD.md) | Held one-shot probes, finite pulse transport and an opposite local reservoir; not derived Maxwell dynamics |
| Formula-free state diagnostic | [node_contract.py](../src/event_universe/diagnostics/node_contract.py) | Read-only structural guard for state ownership; host diagnostics are not physical updates |
| Standalone vector laboratory | [laboratory guide](../tools/generic_vector_lab/README.md) | Separate research/reference process, not the active generic Simulation |
| Application and output | [runner.py](../src/event_universe/runner.py), [ui.py](../src/event_universe/ui.py) | Headless runs by default; optional read-only recording and workspace playback |

The active package lives only in `src/event_universe/`, and the active
`Simulation` resolves to `disturbance_api.py`. The historical scalar scheduler,
its named research APIs, notebook facade and frozen archive were deleted on
2026-09-17; see [migration](MIGRATION.md#historical-particle-candidates-deleted-on-2026-09-17).

The unequal-mass collision configuration has one canonical file:
[04-unequal-mass-collision.json](../examples/04-unequal-mass-collision.json).
Both the workspace and [reference checks](../examples/known-entities/run_reference_checks.py)
consume it. The reference runner does not maintain a second copy of the law.
Its three-mass case likewise uses [three_mass_finite.json](../examples/three_mass_finite.json)
with a 120-tick override instead of a duration-only copy of the initialization.

## Specifications and gaps

[docs/HIGHLIGHTS.md](HIGHLIGHTS.md) is the high-level specification, edited
directly since 2026-09-17 by the model owner's decision; it is not automatic
evidence of implementation. The Google Doc
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
is its historical source up to the revision of 2026-09-16 and is neither
edited nor resynced. Read the current file when working on specification
changes and correct the documents that restate a changed rule to it. The
[ray-event model](RAY_EVENT_MODEL.md) (postulate 23) is the adopted target
direction of 2026-09-17; the implementation contracts below describe the
current code until its migration is published.

The active [disturbance contract](DISTURBANCES.md) supports named scalar/vector
fields, whole-record movement, extensive splitting, atomic interactions, explicit
sources and computation-dependent local waits. Physical work/storage per fixed
local configuration is distinct from total host scheduling and history costs.
Capacity exhaustion rejects a run rather than silently losing state.

[Spatial fields](SPATIAL_FIELDS.md) and [couplings](SPATIAL_COUPLINGS.md) retain
candidate-specific behavior. Schema 2 (`finite-localizing-v1` by default) attenuates
moving stock on each completed link and deposits the removed fraction as stationary
stock at the receiving Node, so total inventory is preserved; the explicit
`"residue": "dissipate"` option (`finite-dissipative-v1`) records completed-link
loss instead. Finite source/response allowances apply to both. Accounting through
attenuation is not physical energy or momentum conservation. Periodic and open boundaries have
separate explicit contracts. General automatic self-field attribution after turns
or periodic return remains unsupported. Two opt-in ordering policies,
[`field_phase_first`](SPATIAL_COUPLINGS.md#field-phase-first-ordering) and
[`arrival_port_blind`](SPATIAL_COUPLINGS.md#arrival-port-blind-sampling), keep an
isolated straight emitter's momentum unchanged without source identity; the default
clock is unchanged and still shows the coarrival self push for value-driven exchange.
A passing isolated-motion rejection test identifies invalid behavior; it does not
repair the underlying candidate law.

The quantum events, focus, native event programs, classical causal-graph
configuration and contact trial were deleted on 2026-09-17 (issue #164,
buckets B.1 and B.2) under Highlights 3.18 (deleted), 3.19, 3.20 and 5.4: no
owner answers at a distance, the Detector is a marked Node and every
alternative is an event on the board. The [ray-event model](RAY_EVENT_MODEL.md)
section 6 lists the remaining migration steps.


The [entity inventory](PHYSICAL_ENTITIES.md), [catalog](ENTITY_CATALOG.md) and
[conversion interface](LOCAL_CONVERSIONS.md) separate representation from physical
acceptance. Maxwell dynamics, gravity, general physical creation/annihilation,
relativity and universal energy conservation are not established merely by these
interfaces or by successful software tests.

The small-space comparisons (`examples/small-space/`, deleted on 2026-09-17), integrated through
PR #40, record 24 experiments in 9-cubed/15-cubed worlds. Finite reservoir transfer,
a ray-speed parameter and a restricted zero-total-momentum unequal-mass candidate
are explicit configuration solutions, not changed entity defaults or derived
universal laws. Their limitations and revision-specific results remain in the
experiment README.

The audit reference now includes the standalone vector laboratory, shared bounded
arithmetic, the local E/B pulse and formula-free node-state guard, and the
Highlights/recovery documentation. Their appearance in the checkout does not
promote reference experiments into the active physical engine. The
[Highlights coverage record](HIGHLIGHTS_IMPLEMENTATION.md) preserves its stated
historical revision; use this map and current contracts for later additions.
Consult [live PRs](https://github.com/Closer24/Universe24/pulls) for any subsequent
work rather than inferring integration from a branch description.
Historical integration chronology remains in Git and [validation records](VALIDATION.md),
not a competing current-status list.

## Resume without a conversation

1. Read [AGENTS.md](../AGENTS.md), inspect local changes, fetch main and record the
   actual base. Use a separate branch/worktree for the task.
2. Use [README installation instructions](../README.md#install-and-run) and the
   interpreter in [.python-version](../.python-version). The minimum package version
   in [pyproject.toml](../pyproject.toml) does not select the shell interpreter.
3. Select an explicit initialization and an unused output directory. The
   [workspace](WORKSPACE.md) changes runtime JSON without rebuilding the engine.
   Visualization is opt-in. Registered outputs expire under [retention](RETENTION.md);
   idle cleanup needs the existing watcher or a scheduled invocation.
4. Follow [CONTRIBUTING.md](../CONTRIBUTING.md), inspect the affected selection from
   `python tools/check.py`, and attach actual results for the submitted tree.
   Use `--full` only for an explicitly justified complete audit.
5. Hand off the scope, validation, limits and integration state through the PR and
   [shared workflow](../skills/workflow.md). A Git rename changes the source fingerprint;
   retain older fingerprints as historical evidence rather than relabeling old runs.

## Repository naming and ownership audit

The repository-wide naming/ownership audit is reconciled against main
`8ceb1fd00e9f23020965d8c2873caf0eff384f92`. It preserved the integrated
native quantum, quantum-entity and Maxwell research additions, of which the
quantum ones were deleted on 2026-09-17, while keeping
one active implementation owner per documented responsibility. Historical
research APIs and standalone laboratories remain explicitly labeled.
