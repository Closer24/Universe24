# Changelog

All notable changes to Universe24, the reference implementation of Reality
Theory (Universe24). Versions are tags on `main`; each is archived on Zenodo.

## Unreleased

### The engine of the law of events (2026-09-19)

- The engine of the law of events (`events-v1`, `src/event_universe/events/`)
  is the one engine: one thing, the event, created at every interval at its
  next place from its record, at a neighbour or here; a measured event's clock
  the count of its self-creations and every rate read off it (`by_clock`); the
  suspension a count the event carries; the sides from the vectors in whole
  units, a single quantum whole by its momentum; no turn in transit; no
  register, remainder, parked share or draw; detectors by sensitivity
  ([the engine](docs/ENGINE.md), [migration](docs/MIGRATION.md)). The engine of
  the law of the shadow (`field-only-v1`) is deleted with its tests and worlds;
  the world file's keys are renamed (`measured`, `in_transit`, `suspension`,
  `detectors`; `phase_turn` gone). Tests: `test_node_mixing` (node-mixing-v2),
  `test_event_transit`, `test_event_suspension`, `test_event_clock`,
  `test_event_worlds` ([expectations](docs/TEST_EXPECTATIONS.md)).
- A detector's threshold gates every response of a detector's Node (`read`,
  `measure`, `rerelease`), receivers and re-emitters alike, by the model
  owner's instruction of 2026-09-19 that every kind of external apparatus
  works with the sensitivity: a bundle of one number below the threshold
  passes with no push and mixes on; a release reads no threshold
  (`EventSimulation._meet`, [the engine](docs/ENGINE.md)). Test:
  `test_detector_sensitivity` ([expectations](docs/TEST_EXPECTATIONS.md#a-detectors-sensitivity)).
- The phase window, `phase_window`, by the model owner's decision of
  2026-09-19 ("Approve the phase window as a declared width of a detector,
  and of the emitter too"; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)):
  a setting on the circle of N steps and the half circle centred on it. On a
  table entry (`{"rule": ..., "phase_window": s}`, any rule but `pass`; the
  string form still accepted) the response, after the threshold, only to a
  bundle whose phase at the Node falls in the window, a bundle outside it
  passing with a `pass` record; on a lamp a release only at the
  self-creations whose clock phase falls in it, the clock and the phase
  turning regardless; the phase read on every measurement record
  (`Transit.phase_at`, `engine.in_window`, [the engine](docs/ENGINE.md),
  [migration](docs/MIGRATION.md#the-phase-window-on-2026-09-19-phase_window)).
  Test: `test_phase_window` ([expectations](docs/TEST_EXPECTATIONS.md#the-phase-window)).

### The law of events recorded (2026-09-19)

- The model owner's law of events, after the one engine and `phase_turn`
  ("there are no registers"; "there are no fields; a field is an event";
  "there is no matter either; matter is a measured event"; "a single quantum
  does not split; in the space of events the quantum leaves in one
  direction"; "there is no shadow and no real; on the board there are only
  events"), is recorded in [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)
  after "One speed, and what is seen", in the owner's words with the
  orchestrator's readings flagged, and the paragraphs it changes carry a dated
  sentence. Nothing of it is implemented: [Highlights coverage](docs/HIGHLIGHTS_IMPLEMENTATION.md),
  [ENGINE.md](docs/ENGINE.md), [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) and the
  README say so. No code changes. The same day: every event carries momentum
  from birth ("By the momentum"); no return to the source; the suspension is a
  count the event carries; fifteen principles recorded after the law with the
  owner's decision on each, the fixing mechanism of their points 8 to 12 not
  adopted; what follows for Highlights and the engine, and the tests of the
  engine of events in 5.5.

### One engine (2026-09-19)

- The engine of the law of the shadow (`field-only-v1`, feature 20) is the one
  engine, by the model owner's decision of 2026-09-19 ("The field is, in fact,
  a field of events. No confrontations are needed. Only tests that everything
  is as designed."; [Highlights 5.4](docs/HIGHLIGHTS.md#54-the-detector)). The
  old engine of the law of the bit, its worlds, catalog, tools and tests are
  deleted ([migration](docs/MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted)).
  The substrate the new engine took from the old one moved to
  `core/lattice.py`, `core/phase.py` and `shadow/mixing.py`, byte-identical in
  what it does; the Node's mixing has its own isolated test again,
  `tests/test_node_mixing.py`, on one Node of the engine's layer.
- The runner takes `--init`, `--output` and `--ticks` only; the preflight
  checks world files only; the workspace lists the worlds of `examples/shadow/`
  and runs headless.
- The same day, earlier: the three pending decisions of the morning's status
  line (`transmitted_number`, the wait's unit, ε_g) were withdrawn ("We do not
  need these three things at all"), so the gate of feature 20b is not written;
  the wait is the delayed clock and `wait_per_quantum` stays a declared width
  of the world; and the owner's reading "A quantum passes, like everything, at
  the speed of light between Nodes" is recorded in 5.4 ("One speed, and what
  is seen").

- `families[i].phase_turn` (features 21 and 23; the owner's "what can be put
  as a parameter, put" and "constant frequency for light? Yes, make it the
  default for light. That is, per family."): how a family's quanta turn their
  phase per Link walked. `"quantum"`, the default for a paid family: by the
  family's quantum over K, the same for every quantum of the family wherever it
  is, the remainder carried per family, so light keeps the frequency it was
  born with (round 8, S5); `"none"`, the default for a free family; `"amount"`,
  the old rule by the amount in the cell, which slowed as the field thinned and
  stopped a few Links from a lamp, kept as a choice. Replaces the key
  `turns_in_flight` of the same morning ([migration](docs/MIGRATION.md#the-phase-turn-in-flight-per-family-on-2026-09-19-phase_turn));
  `tests/test_family_turns.py`.

- `families[i].quantum` (the owner's "put it in, without an experiment"): the
  units of a family that make one event at a holder that absorbs them (`keep`,
  the click; `rerelease`), per number, the rest waiting in the holder's
  register (`pending` in the content's state and on the held line of the
  books, `events` per family); 1 by default, every unit its own event as
  before; the derivation's q_γ as a declared width; `tests/test_family_quantum.py`.

### The law of the shadow, the field-only engine (`field-only-v1`, feature 20, 2026-09-18)

- A new engine mode beside the old one, `event_universe/shadow/`, selected by
  a world's `"law": "shadow"` key ([the law of the shadow](docs/MIGRATION.md)):
  only shadows and events. Matter is content held at Nodes; every ray is a
  shadow, a whole quantum in flight that moves one Link per interval and
  spreads by the Node's mixing, the dense layer's kernels by import; an event
  is a whole quantum at a Node with content, absorbed, held or released again
  by the holder's table (the free families read at a holder and passed on,
  the push by the holder's content and charge; light kept, the click, or
  re-released; the own number sunk for its amount and pushing nothing); a
  held content releases its field at the world's rate, a lamp spends its
  light; the wait reads the size; the step is the accumulator's, at most
  once in two intervals (round 8's Node rule, DERIVATIONS.md sections 51 to
  56); the books per family close at every tick. The old engine, its worlds and its
  tests are untouched ([migration](docs/MIGRATION.md#the-law-of-the-shadow-a-new-engine-mode-on-2026-09-18-field-only-v1)).
- The worlds `examples/shadow/` (one content, two contents, two slits and
  the one-slit control) and the isolated test `tests/test_field_only.py`
  ([expectations](docs/MIGRATION.md)), the
  numbers from DERIVATIONS.md round 7.

### Charge per thing (`charge-per-thing-v1`, feature 16g, 2026-09-18)

- The charge of a thing is one declared number of its family, whatever its
  content (the model owner, Highlights 5.4 point 16 as amended): a family's
  `charge` and a body's are the charge of one thing, whole, never a charge
  per quantum. The electricity reading multiplies the shadow's message (its
  owner's charge over its content, unchanged) by the whole charge of what is
  pushed; the worked example of point 16 holds exactly, a body of 1000 quanta
  with charge 1 is pushed by nine units and not nine thousand, and the
  catalog's electron of 20 does not turn at its first push.
- The charge readout, the ledger's charge line and the local audit count the
  whole charge of things: a merged ray of k things carries k times the
  family's charge (the identities a merge keeps), a record's stock the things
  it has not yet emitted, a shadow none; every table conserves it (the
  appended invariant sums the things' charges; a join keeps every identity).
- `run.json` records `charge_per_thing`; the refusal of a pushed body whose
  charge was not a multiple of its amount is gone. No example world's
  declaration changes; the tests whose bodies declared `-amount` to mean -1
  per quantum re-declare it ([migration](docs/MIGRATION.md#charge-per-thing-on-2026-09-18-charge-per-thing-v1)).

## 0.3.1 - 2026-09-15

Concept DOI 10.5281/zenodo.22738746 (the version DOI is listed on the Zenodo
record).

### Redshift from delay growth (second manuscript)

- `redshift_sweep.py`: a train of twelve rays crosses closed rows of 16 to 96
  Nodes under `ray_delay` to an absorbing eye that counts its own cycles;
  `1 + z = k_o / k_e` on the eye's clock, durations stretch by the same
  ratio, `z` from 0.07 to 2.81 with the distance, the slope scaling with the
  emission; the wave's frequency follows the gaps under the default phase
  rule by construction (the phase difference between rays is conserved along
  the path), read over the span it is measured on and converging with the
  tick resolution; a single source emitting at a fixed interval of its own
  clock (`--labels "single source"`) gives the same law. Moving bodies stall the
  clocks of the Nodes they wait at and are
  not used (report (`examples/relativity-probes/`, deleted on 2026-09-17)).
- `redshift_hubble.py`: the law's shapes against the Pantheon+ Hubble-flow
  sample, with the diagonal errors and (`--covariance`) the release's full
  covariance, the exponent fitted under each error model with its interval
  (refined in steps of 0.001 around the minimum) and the reading-A family
  bounded by its `n -> infinity` limit; the model's own load histories are
  behind LambdaCDM, and the best power law by nine units of chi-square with
  one fitted parameter each, as preferences between models (the shapes pass
  a goodness-of-fit test on their own); the Tolman exponent is the
  discriminating test, an indication against the lattice until the data
  are reduced under its own distance relations. Manuscript in `paper/redshift/` ([hypotheses](docs/HYPOTHESES.md)).


A review pass on the paper's Bell narrative. No engine change; the Bell probe
gains two modes and the framework's claims are narrowed to what is measured.

### Bell's test

- The bonded value carries its statistics: `--sweep` re-measures the bonded
  CHSH value with fresh pairs for every setting pair, 64 to 4096 pairs per
  correlation on the lattice with four replicas each and the registry alone
  to a million pairs, with binomial standard errors; every lattice outcome
  equals the registry's answer from the same seed, and `S` converges to the
  table expectation `724/256 = 2.828125`. The first run's 2.889 was sampling
  spread on correlated samples (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17).
- Which assumption of Bell's theorem each candidate breaks is measured at
  fixed hidden variable by `--causal`: the lottery and the threshold are
  parameter independent; the bonded pair is deterministic and
  measurement-independent and breaks parameter independence (Bob's answer
  moves with Alice's setting for 0.72 of the hidden variables at
  `b'`); the quantum owner breaks outcome independence
  (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17;
  coupling (`docs/QUANTUM_CLASSICAL_COUPLING.md`, deleted on 2026-09-17)).
- The door of postulate 22 is measured half by half: `--source agreement`
  keeps the coin even and fixes the agreement half, giving S = 4 (the
  Popescu-Rohrlich box) with even marginals and no signal; no-signalling
  bounds the coin, not the correlation (report: `examples/bell-chsh/README.md`, deleted on 2026-09-17).
- Postulates 4 and 22 name the broken assumption: the registry is a nonlocal
  resource in Bell's sense, its unmoved plus rates are no-signalling and not
  locality, and how a number is read (one end, both ends, or correlated with
  the settings) decides which assumption is at stake ([POSTULATES](POSTULATES.md)).

### Paper

- The manuscript is reframed as a finite-integer causal-lattice testbed: the
  configured laws are named as inputs, the Bell section carries errors and the
  causal analysis, "what is new" and "what is not claimed" are explicit, and
  the bonded pair is stated not to be a local explanation of the Bell value
  ([paper](paper/main.tex)).

## 0.3.0 - 2026-09-14

153 commits since 0.2.0. Zenodo DOI 10.5281/zenodo.22749342. Every number
below is recorded with its source fingerprint in [validation](docs/VALIDATION.md).

### Framework

- The framework is named Reality Theory (Universe24); the simulator stays
  Universe24 ([README](README.md)).
- Postulate 4 is split: energy, momentum, matter and every controllable
  message move at most one Node per step; the joint outcome of a bonded pair is
  the one declared exception, answered by a bounded registry that carries
  nothing physical ([POSTULATES](POSTULATES.md)).
- Postulate 22: every uncertain interaction consumes exactly one bounded
  integer; a bonded pair draws one number, whichever end asks first; the
  sequence is the only door for outside information and is bound by
  no-signalling.
- A [hypotheses page](docs/HYPOTHESES.md) keeps the questions the framework
  raises apart from measured results.

### Quantum and classical coupling (causal source candidate)

- Two-arm interference on the canonical runner: exact capture weights, a
  balanced Hadamard splitter, which-path decoherence, causal termination
  (report (`examples/quantum/causal_interference.md`, deleted on 2026-09-17)).
- Opt-in null notices restore the exact conditional Born weights after Link
  transit; crossing nulls are corrected locally by the later Node
  (crossing nulls (`examples/quantum/crossing_nulls.md`, deleted on 2026-09-17)).
- Opt-in field-dependent phase: an external classical field on one arm shifts
  the fringe by an exact configured phase per field unit.
- Opt-in funded emission: the wave pays for its own field from its conserved
  stock; totals constant; the retarded emission after a capture is the measured
  residual.
- Emission-scale sweep: the integer field follows `amount x |psi|^2` within one
  unit per tick at every scale.
- Two-wing Bell CHSH on the finite quantum owner: 14/5 exact, no-signalling
  marginals, dephased control 6/5 (report (`examples/quantum/bell_chsh.md`, deleted on 2026-09-17)).

### Straight and phased rays (Kerengonen candidate)

- Kerengonen phased rays with a fixed-point cosine table: double slit, Huygens
  slits, single-quantum lottery, de Broglie advance from momentum, mirror
  standing waves, matter-wave dissolution, Euclidean pace, claim and gather,
  bonded pairs.
- Bell's test on the ray with five captures on one scale: share 1.40 exact,
  lottery 1.48 and 1.38, threshold 2.00 exactly, bonded 2.89 against the
  quantum 2.83, plain field 2 (`examples/kerengonen-bell/` and `examples/bell-chsh/`,
  both deleted on 2026-09-17).
- An outside number source for bonded pairs: uniform is invisible, biased is
  a measured signal.
- Signed-quanta gravity with a closed ledger, gathered gravity (no dark-matter
  substitute from focusing), isotropy probe, relativity probes (lensing,
  redshift without recession, flat curves from a compressed closed dimension,
  gravitational phase in an interferometer, replay).

### Engine

- Local Focus scheduling (opt-in), ray ownership guards, carried allocation
  phases, ray delay and ray phase per tick, bounded prepared tables, 24-slot
  envelope output banks.

### Repository

- MIT license, `CITATION.cff`, Zenodo DOI 10.5281/zenodo.22738746 (0.2.0);
  named-particle gallery; documentation cleaned of process noise.

## 0.2.0 - 2026-09-14

First archived version: the integer lattice simulator with configured
disturbances, spatial fields, the finite quantum owner and the causal source
candidate. Zenodo DOI 10.5281/zenodo.22738746.
