# Universe24 detector requirements

Date: 2026-09-19. Status: consolidated requirements and published implementation contract for the explicitly selected `reversible-detector-v1` candidate. Code and physical validation are separate evidence. Tracked in [issue 342](https://github.com/Closer24/Universe24/issues/342).

Source baseline: `events-v1`, commit `bfb463be6313ae226aa0a192d11036ead63dd0f1`. This document owns the detector requirements and the scoped candidate contract below. The default `events-v1` measurement and mixing rules remain as documented in ENGINE.md. The candidate deliberately does not call their lossy transitions.

## Definition and adopted requirements

**A detector is a physical arrangement of ordinary Nodes and Events within the event board. Its interactions produce a physical output record. An observer can read that record with a declared resolution; the complete underlying physical state remains definite.**

| ID | Requirement |
| --- | --- |
| D1 — Definite state | The complete board, apparatus, environment and settings have definite bounded-integer states. Repeating the identical complete initial state and settings produces the identical outcome. This is a model postulate, not an established description of nature. |
| D2 — Ordinary physics | Detector behavior uses the same generic LocalRules as other matter, without branches on a physical entity's name. Physical memory consists of Events on Nodes, including measured Events; no special detector register, unbounded history or off-board hidden state is introduced. |
| D3 — Causal locality | Every physical input arrives through the six neighboring Links, with the declared transit time. Work and storage per local update remain bounded for fixed declared capacities. A large detector combines signals through local interactions; its size does not grant instantaneous access to all its Nodes. |
| D4 — Physical result | A shared result must exist as an output state produced within the detector. A diagnostic sum over the board does not create that result. The observer reads an existing record; observer callbacks, rendering and audit totals cannot determine an outcome or modify physical state. |
| D5 — Preserve information | Different permitted complete physical inputs, including the previous apparatus state, must remain distinguishable in the complete physical output: detector, environment and outgoing Events together. The local transition must have an explicit inverse on its allowed domain, or equivalent injectivity evidence. A many-to-one visible result is allowed; a many-to-one complete physical transition is not. |
| D6 — Exact accounting | Every interaction preserves the quantities declared invariant by its model, with their units and owners explicit. Include recoil, outgoing content and supporting apparatus where relevant. Do not silently identify information, Event count, photon number and energy as the same invariant. |

For a closed physical system with state `S`, the information requirement is `F(S1) = F(S2) => S1 = S2`. Its visible readout `R(S)` may map several states to the same result. Audit records are not a substitute for `S`. Current boards have open edges: a closed-region claim requires a trial with no escapes; a wider-system claim must include the full escaping physical state, not only escaped totals.

## Generic sensitivity and distinguishable results

**D10 — Generic configuration.** Coverage may contain any declared finite number `n_nodes >= 1`, subject to explicit world and resource bounds. No rule is specialized to three Nodes, another coverage size or a physical entity name. Specify the Node geometry, readout grouping, thresholds and output locations as data. Local work and storage remain bounded for the declared per-Node capacity; total apparatus resources and causal aggregation time may grow with coverage. A configuration is supported only when its physical interactions and bounds are defined and validated.

Configure these separately:

| Property | Meaning |
| --- | --- |
| Coverage | Which Nodes participate, for any supported finite size. Their geometry and causal signal paths are declared. |
| Spatial readout resolution | Which locations yield distinguishable output records. Three Nodes may yield one common result meaning “an event was detected somewhere in this group.” |
| Quantum threshold and trigger | The amount and timing needed to produce a result under the local interaction law. Coverage of three Nodes does **not** require three quanta, or one quantum at every Node. |
| Observable and setting | Which physical quantity the apparatus couples to, and its physical reference, orientation or other setting. |
| Timing and capacity | Propagation delay, record capacity, readiness and the physical behavior on saturation or reset. |

The following are illustrative configurations, not hardcoded physics or claims of current implementation. Every common output must arise from physical local signal collection. A group threshold counts eligible quanta under a declared accumulation/timing rule; it does not require one quantum per covered Node.

| Covered Nodes | Readout grouping | Quantum trigger | Spatial meaning of a result |
| --- | --- | --- | --- |
| 1 | One output | 1 quantum | The single Node detected an event. |
| 3 | One shared output | 1 quantum anywhere in the group | An event occurred somewhere among these three Nodes. |
| 100 | One shared output | 1 quantum anywhere in the group | An event occurred somewhere among these 100 Nodes. |
| 100 | 100 distinguishable outputs | 1 quantum at a responding Node | The output identifies which Node detected the event. |
| 12 | Four distinguishable groups of three | 2 quanta per responding group, under its declared timing rule | The output identifies a group, without identifying an individual Node. |

These examples show independent choices: the same coverage can provide different spatial resolution, and a three-Node group can have a threshold other than three. Group/output labels do not authorize instantaneous global processing.

**D7 — Shared output without erasure.** One quantum arriving at any of three covered Nodes may produce the same spatial output category. The distinguishing information must survive elsewhere in the full physical state. The example does not require identical timing or other output channels unless the readout contract says so. Any claim that the observer cannot resolve the input Node must be tested against the full declared accessible record, including timing and other channels. A three-Node footprint is not itself a standard deviation or a Heisenberg relation.

**D8 — Capacity and reset.** Declare finite encoding, integer bounds and saturation behavior before implementation. Previous detector information cannot be overwritten by incoming phase. Full capacity must invoke a specified physical process or an explicit unsupported-state refusal; no silent overflow, rounding loss or arbitrary deletion. Reset must transfer information through physical interactions. Repeated unlimited recording into a fixed finite detector is not permitted.

An incoming phase record is distinct from the detector's own clock phase. Mandatory backward emission and mandatory multi-Node coincidence are not requirements of this design. If reflection is later specified, its outgoing information, amount and momentum need a local conservation contract; reflection alone does not establish information preservation.

## Accessible measurements and quantum targets

**D9 — Physical observable contract.** A reported quantity must come from a specified coupling and output encoding. Position/time use local detection and clock records; momentum must be inferred from a physical momentum-sensitive interaction, such as transfer or recoil, rather than reading a hidden engine variable. Counts and energy require their own declared conversion. Phase, if measured, needs a physical reference. The design does not grant simultaneous exact access to every internal variable.

**Q1 — Position–momentum target.** The requested principle is that preparing a sharply defined momentum requires position spread, and preparing a sharply localized state requires momentum spread. In an appropriate continuum regime, repeated operationally identical preparations must reproduce the preparation uncertainty relation

\[
\sigma_x\sigma_p \geq \hbar/2.
\]

For the finite discrete board, first define the appropriate observables and valid discrete counterpart or continuum regime. Fix length, time, momentum and action scales independently of the validation results. Device resolution, state preparation spread, measurement error and disturbance are different quantities; a universal measurement-error-times-disturbance bound is not assumed. [Ozawa's distinction](https://arxiv.org/abs/quant-ph/0207121)

Operationally identical preparation may admit a declared ensemble of different complete microstates; identical complete microstates remain deterministic. Compare independently calibrated position and momentum measurements on separate ensembles prepared by the same procedure. The relation is a lower bound: it does not say that every decrease of actual position spread must increase actual momentum spread.

The preparation and microscopic interaction laws must produce the restriction. Artificial noise, clipping results to a bound, hiding an otherwise physically accessible joint sharp measurement, or refitting calibration after a failure does not satisfy Q1. Three-Node readout resolution alone does not satisfy it either.

**Q2 — Other quantum behavior.** Born statistics, backaction and measurement-sequence behavior are separate research targets, with independent expected results. A supplied probability or response table must be labeled as an assumed law, not a derived prediction.

**Q3 — Bell limitation.** A local deterministic board, including the source and both detectors, with measurement choices independent of its shared state remains subject to Bell constraints, including `|CHSH| <= 2` for the standard complete-trial setting. This architecture does not establish quantum entanglement or a Bell violation. Postselection, setting-dependent omission of events, or later communication between detectors cannot be presented as a loophole-free violation. [Shalm et al.'s experimental benchmark](https://arxiv.org/abs/1511.03189)

## Current implementation gap and ownership

The baseline [engine contract](https://github.com/Closer24/Universe24/blob/bfb463be6313ae226aa0a192d11036ead63dd0f1/docs/ENGINE.md) explicitly treats a click as a one-way boundary: incoming phase is recorded externally to the live board, while amount and momentum enter the measured Event. That contract is incompatible with D5's full on-board information goal and must be reconciled explicitly before implementation.

| Existing owner | Required design work |
| --- | --- |
| `events/world.py` | Separate coverage, resolution, trigger and physical output layout in the world contract. Existing `positions` and per-Node `threshold` do not define a causal shared output. |
| `events/engine.py`: `Measured`, `_meet` | Specify a local reversible interaction and physical record encoding, preserving incoming distinctions and prior apparatus information without overwriting its clock. |
| `events/transit.py` | Carry all required physical information through local propagation; examine combination/take operations for lost distinctions. |
| `events/engine.py`: `detectors()`, `_event` | Keep diagnostic aggregation and exported records separate from the physical result they describe. Neither supplies missing physical memory. |

This is an ownership map, not a new API. Before coding, publish the local operator, its input/output domain, Event encoding and capacities, timing, saturation/reset behavior, invariant accounting, allowed preparations and observable/unit mapping. Missing physics must remain an open design decision. Full-board information preservation also requires examining other merges and mixing operations.

## Acceptance checklist for later work

- **A1 — Determinism and locality:** identical complete inputs replay identically; audit integer intermediates, bounded storage and causal input provenance. Enabling diagnostics cannot change the trajectory.
- **A2 — Information:** test incoming phase 0 versus 16, distinct prior detector states and full-capacity/reset cases. Their complete physical states remain distinguishable and reconstructable without history logs. This witness alone is not a proof for all states or all rules.
- **A3 — Generic grouping:** cover one Node and several configured sizes, including three and a larger group, and separate shared from individually distinguishable outputs. Under a one-quantum trigger, arrival at any covered Node can give the contracted common spatial category while retaining distinct complete physical states. Vary the trigger independently of group size; reject unsupported bounds. Output cannot depend on information that has not yet arrived.
- **A4 — Conservation:** verify the model's exact invariants across input, detector, supporting environment and output, with explicit edge handling.
- **A5 — Quantum research:** freeze preparations, calibration, reference expectations and discrepancy criteria before uncertainty/Born/sequence comparisons. Record failures and finite-board limits. These are research runs, distinct from isolated generic-rule unit tests.

The owner proposes that finite cell sensitivity together with information preservation on the board will produce the Heisenberg relation. This is the research hypothesis to investigate, not a rule inserted into the output. The following candidate supplies a concrete reversible interaction for D5 on its declared domain; whether any such mechanism supplies Q1 remains open.

## Implementation contract: reversible-detector-v1

### Identity, scope and ownership

This is an explicitly assumed, nondestructive transduction candidate, selected by the new world key `dynamics: "reversible-detector-v1"`. Omission selects `events-v1` and preserves its existing behavior and serialized output. `law` remains `"events"`; `model_id` is a user label and never selects behavior. Candidate output identifies its dynamics separately.

The candidate represents the detector as ordinary fixed measured Events, routes original incoming Events through local contact scattering, and changes a measured Event's phase as a physical pointer. It does not absorb a carrier, invent a second signal, retain packet history, or insert a detector register. Every configured contact obeys the same generic rule; a detector or family name has no physical meaning. This is not a replacement for the default world's interference law, an assertion that default `measure` is reversible, or a derivation of laboratory quantum measurement.

| Owner | Contract |
| --- | --- |
| `events/world.py` | Strict immutable schema and candidate domain validation; provider of definitions to all consumers |
| `events/reversible.py` | One owner of the pure bounded integer contact, inverse, clock reference and physical readout decoding; no output libraries |
| `events/engine.py` | Candidate scheduling, fixed Event ownership, atomic preflight and commit, serialization; no duplicated contact formula |
| `events/transit.py` | Existing fixed arrays and ordinary nearest-neighbor transfer; candidate must bypass combining/mixing methods |
| `events/run.py` | Existing runner artifacts; identifies candidate and exposes its read-only result without creating it |
| `examples/events/detector/` | Data-only configurations and a short usage/limits guide; no independent simulator |

World/schema and physical-engine developers work in separate files. The world/schema developer is the only writer of `world.py` and its public dataclasses. The engine developer is the only writer of `reversible.py`, `engine.py`, transport integration and runner integration. Architecture owns this document and its canonical cross-links. Test owners write focused tests of the generic rule and schema, not expected numerical outputs of example worlds.

The pure public API in `events/reversible.py` is fixed for independent consumers:

```
CarrierState(family: int, number: int, amount: int, phase: int,
             port: int, momentum: tuple[int, int, int])
ContactState(phase: int, momentum: tuple[int, int, int])
transduce(carrier: CarrierState, material: ContactState,
          port_map: tuple[int, ...], phase_steps: int, quantum: int)
    -> tuple[CarrierState, ContactState]
inverse_transduce(carrier: CarrierState, material: ContactState,
                  port_map: tuple[int, ...], phase_steps: int, quantum: int)
    -> tuple[CarrierState, ContactState]
clock_step(age: int, content: int, clock: int,
           phase_steps: int, phase: int) -> tuple[int, int]  # age, phase
pointer_displacement(phase: int, age: int, content: int,
                     reference_phase: int, clock: int, phase_steps: int) -> int
```

Both state records are immutable dataclasses and are only local input/output values, never additional persistent Node memory. Validation errors use `ValueError`; working-range errors use `OverflowError`. Engine runtime output is available through `EventSimulation.detector_readouts() -> list[dict[str, object]]`; this is read-only. Snapshots for the candidate add `dynamics` and `detector_readouts`; old `detectors` remains audit data and cannot drive the new physical output. Candidate-only audit records use `kind: "transduction"` and expose local input/output payloads without being needed for replay. The test owner exclusively writes `tests/test_reversible_detector.py` and `tests/test_physical_detector.py`; the schema developer owns `tests/test_reversible_detector_world.py`.

### Exact schema additions

The following definitions are candidate-only; ordinary worlds reject candidate-only fields and rules rather than silently ignoring them.

* `dynamics`: `"events-v1"` or `"reversible-detector-v1"`, default `"events-v1"`.
* `max_active_owners`: required for the candidate, integer 1 through 16. Each family's actual active transit owner count must not exceed it. At most 8 families are accepted by the candidate. Each Node therefore has at most `8 * 16 * 6` fixed transit channels, independent of detector coverage. Ordinary paid, nonemitting material Events do not add transit owner channels; only identities actually present in `in_transit` do. Thus 100 or more material Nodes with one active incoming owner are supported by a bound of 1.
* A measured Event may declare `port_map`: a required permutation of integers 0 through 5 when any table entry is `"transduce"`. Port order is the existing `PORT_HEADINGS` order. No missing route is inferred for a transducer. The table entry `"pass"` is the explicitly selected identity transfer and does not change the pointer. Every candidate measured Event explicitly declares its table entry for every family; no absent entry defaults to another rule. Other table entries are refused by the candidate. A `"transduce"` rule applies to all eligible arriving Events, including an Event with the same number: there is no lossy `home` override.
* A candidate detector declares `name`, `positions`, and `groups`. `positions` are the nonempty unique coverage Nodes, each with an ordinary measured Event. Every group declares `name`, nonempty unique `positions` drawn from that coverage, `output` (one measured Event's Node), `threshold`, `capacity`, and `reference_phase`. Group positions partition the detector coverage exactly; output Nodes are unique across groups and detectors. Outputs may also be covered Nodes. The candidate does not accept the legacy top-level detector `threshold`; the default detector schema remains unchanged.
* A group `threshold` is an integer from 1 through `capacity`; `capacity` is from 1 through `N - 1`; `reference_phase` is from 0 through `N - 1`. All are explicit, without defaults. The reference is frozen configuration, not recalibrated from each trial's initial pointer.

Keep `DetectorDefinition` backward compatible with existing positional constructor consumers by adding `groups=()` as a trailing field; its old `threshold` field is set to 1 and unused for the candidate. Introduce immutable `DetectorGroupDefinition(name, positions, output, threshold, capacity, reference_phase)`. Add trailing defaults to `MeasuredDefinition` for `port_map=()` and to `EventWorld` for `dynamics="events-v1"` and `max_active_owners=0`. Existing table-window structures remain intact; candidate rules use no `phase_window`. Preflight also rejects duplicate initial slots, initial `q * quantum` or per-Node amount sums outside the stated bounds, and output initial displacement greater than capacity.

Coverage is an apparatus layout, not an instantaneous input list. It may contain 1, 3, 100 or another finite number of Nodes. Group names and membership label the claimed response region; they cannot make a signal arrive at the output. The input author must arrange actual local transport routes. The first examples use a nonbranching chain or serpentine chain of ordinary transducers so arrivals at any covered Node reach one output without a many-to-one port mapping. At a corner a permutation changes direction; outside contact, heading and phase are unchanged. Arbitrary many-to-one merging is unsupported. A configuration with a declared group but no physical path does not produce a result by assertion.

### Allowed physical state and capacity

All candidate families are `paid`. All measured Events are fixed, carry zero charge, have no lamps, and use only `pass` or `transduce`. World `release` is zero and `suspension` is zero. There is no emission, absorption, merge, coherent mixing, field push, suspended queue, measured movement or reset in this candidate. Their introduction requires another contract revision, not a fallback into a default rule.

Each occupied transit slot holds exactly the existing Event record: family, number, amount `q > 0`, phase, heading and momentum. Momentum is canonical on the allowed domain: `p = q * family.quantum * heading`. Transduction updates it to the new heading and takes the balancing recoil. No original phase, identity or amount is discarded. Fixed material Events keep their existing content and encode memory only in their phase, momentum and age; there is no extra dynamic detector state.

Storage bounds use the existing amount/component bound `B = 2^62 - 1`; every arithmetic intermediate uses signed `W = 2^63 - 1` through the generic integer checker, including products before cancellation. Explicitly check the total local amount, recoil sums, `age + 1`, `age * content`, `(age + 1) * content`, and pointer sums. Each occupied channel is unique. Empty channel numeric payload is canonical zero. Candidate diagnostics cannot enter physical formulas and may not grow beyond declared bounds.

Snapshot-derived host audit totals use exact Python integer sums rather than overflow-prone fixed-width NumPy reductions. Their finite bounds follow from the validated board size, channel/material counts and component bound, and can exceed the physical working-register width. They are not physical state or cumulative memory, never feed a local operator, and do not impose a global 64-bit admission limit on otherwise valid local states. Their computation and storage are host costs reported separately.

The only normalized physical boundaries are the initial state (seeded arrivals, no flights) and completed steps (flights, no arrivals). Complete-state reversibility is asserted on those timed boundaries. Refuse arbitrary mixed arrival/flight input, slot overwrite, nonzero suspension/home content and noncanonical momentum. Physical inverse/replay never consults diagnostic counters or callbacks.

### Local operator and explicit inverse

At one measured Event, for a declared permutation `pi`, an incoming carrier on port `h` has amount `q`, phase `phi`, momentum `p`; the measured Event has phase `a`, momentum `P`, fixed content `M`, age `t`. The generic contact does:

```
h_out = pi[h]
p_out = q * family.quantum * PORT_HEADINGS[h_out]
a_contact = (a + q) mod N
P_out = P + p - p_out
```

The phase coupling is an assumed one phase step per amount unit; it does not define an action scale or `hbar`. The carrier's amount, phase `phi`, family and number do not change. For `pass`, `h_out = h`, `p_out = p`, `a_contact = a`, `P_out = P`. For several occupied local channels, apply the same operator in fixed family/owner/port order and use checked sums; a port permutation is injective within each family and owner and never combines packets. Different family/owner channels remain physically distinct. The output's capacity check sees only arrivals already at that output Node.

Next the material clock advances exactly once, with fixed content:

```
clock_turn = ((t + 1) * M) // K - (t * M) // K
a_next = (a_contact + clock_turn) mod N
t_next = t + 1
```

The contact inverse reads the outgoing carrier once: recover `h = pi_inverse[h_out]`, `p = q * family.quantum * PORT_HEADINGS[h]`, subtract the same `q` modulo `N` from the material phase, and recover `P = P_out - p + p_out`. To invert the completed local step, first decrement age and undo its known clock turn, then undo contacts in reverse order. Local rule definitions are immutable inputs to the inverse. A contact is a new configured scattering interaction, not a change of phase during free flight.

Thus previous material phase is preserved as well as incoming phase. There are no collision-prone sums of phases, no source tag rewritten to the detector number, and no external record needed. Modular addition is a permutation, including at the phase boundary; capacity is a separate finite-readout constraint.

### Interval, causality and failure

Reuse `EventSimulation` and its artifacts. Candidate scheduling bypasses `sizes`, `suspend`, `mix_arrivals`, `receive` combination, lossy `_meet`, release and movement; it dispatches the declared generic contact and exact clock operator instead. Transit construction may accept an `exact_transport=True` initialization option for this path, avoiding unused trigonometric tables while retaining the same owned arrays; it changes no default behavior. A first step handles the declared initial arrivals; subsequent steps transfer each prior flight through one Link, then perform the contact at that receiving Node, then place its intact outgoing record into flight. Material clocks advance once at every step. There is no additional cross-board access by a physical rule.

Build bounded local proposals from the current immutable step state and validate before committing any physical owner, diagnostic counter, tick or callback. The host scheduler may hold proposals for the board; that host cost scales with board size, while each proposal reads one Node's arrivals and one resident. If any required proposal has a slot conflict, range violation, unsupported state, output capacity overflow or outward open-edge transfer, refuse the entire step with the original state and tick unchanged. This is an unsupported-state refusal, not a new remote physical reaction. No partially advanced board may be returned as a successful step.

The physical board remains open. Candidate runs are finite no-escape trials: reaching an outer edge without a next Node is refused before information can leave. No periodic topology is inserted. The unaffected default model retains its ordinary escaped totals and makes no full-state closed-system information claim. Trial length and routes must keep all Events within the board.

### Output record, sensitivity and read-only observer

At a group's output Event the physical clock supplies the local reference. Its calibrated displacement is

```
d = (phase - reference_phase - ((age * content) // K)) mod N
```

Only that one output Event's current phase, age and fixed content enter this expression. No input position, source phase, global sum, saved earlier state or inferred travel history is read. The local clock reference and calibration are an explicitly assumed readout encoding, not a derived laboratory phase measurement. Initial `d` must be at most `capacity`; it is not silently zeroed. At each contact an output must satisfy `d + sum(q_transduced_here) <= capacity` before commit. Thus `d` is an unambiguous finite count of transduced units within the trial. A trajectory crossing twice counts twice; examples route each input through the output once.

The group readout is `{"name": group_name, "value": d, "triggered": d >= threshold}`. The exact detector object is `{"name": detector_name, "positions": [[x, y, z], ...], "groups": [group_readout, ...]}`, in declaration order. A shared group yields one category regardless of which covered Node the input used, but only after transport reaches its output. Multiple groups produce distinguishable output categories. Threshold is a read-only classification of a physically changed pointer and never creates, absorbs or suppresses an Event. For example, a threshold of 2 does not demand two input Nodes: one bundle of amount 2 or two amount-1 crossings can give `value: 2`.

Timing and any other exposed readout fields belong to the observer's accessible record. Different path lengths can reveal which input was used; this candidate makes no perfect spatial-anonymity claim. Full physical snapshots deliberately reveal more than the observer view and label transit, apparatus and audit data separately. The read-only output API must have no physical side effects; enabling, disabling or changing the diagnostic callback cannot change a trajectory.

Finite capacity has no silent saturation. When full, the next otherwise incrementing contact is outside the accepted state domain and refuses the step. There is no runtime reset operation in this milestone. Loading a new experiment is a new preparation, not a physical erasure. Inverse functions are mathematical validation tools, not a claim that a reverse-scheduled laboratory reset has been implemented.

### Invariants, examples and independent checks

For every accepted contact and complete no-escape interval: per-family transit amount and each carrier's family/number/phase remain exact, material content is unchanged, and total material-plus-transit momentum remains exact. Carrier count is also preserved on this restricted no-split domain. No energy relation for the fixed supporting apparatus is supplied; do not claim energy conservation merely from momentum and amount. Fixed support retains recoil in its measured Event's momentum under the existing `fixed` convention.

Independent local checks fixed before implementation:

| Input | Exact expected result |
| --- | --- |
| `N=32`, `q=2`, family quantum `3`, incoming `+x`, phase `16`, material phase `5`, material momentum `(7,-4,2)`; permutation swaps `+x` and `+y` | Outgoing `+y`, phase `16`, momentum `(0,6,0)`; material phase `7`, momentum `(13,-10,2)`; total momentum `(13,-4,2)` before and after |
| Same incoming phase `0` instead of `16` | Same visible pointer, different complete outgoing physical phase; inverse restores either input without history |
| Same material phase `6` instead of `5` | Material phase `8`; previous apparatus information remains distinguishable |
| Local primitive `q=1`, material phase `31`, `N=32` | Material phase `0`; inverse returns `31`; carrier phase is unchanged (modular phase wrap itself is valid) |
| Clock `t=2`, `M=3`, `K=4` | Turn `1`, next age `3`; inverse subtracts `1` |
| Pointer reference `4`, phase `9`, age `3`, content `3`, `K=4` | Baseline `6`, displacement `3`; threshold `2` gives true |
| Output displacement `3`, capacity `3`, next increment `1` | Refusal before any physical state, tick or record changes |
| Duplicate/nonpermutation route, noncanonical momentum, unknown key, bool count, owner bound, output edge escape | Explicit refusal by the responsible boundary; no clipping, merging or fallback |

Schema checks include one, three and at least 100 coverage Nodes, one shared output versus separately grouped outputs, and thresholds independent of coverage. Causality tests isolate one Link transfer and one local readout: the pointer stays unchanged before arrival and changes exactly on the receiving interaction. Test physical-domain round-trip on bounded enumerated phases, ports and prior material phases, and integer limits separately. These are generic-rule tests; the 9-by-9 demonstration is a dated research run with source/configuration fingerprints and HTML, not an example-output unit test.

The independent finite inverse enumeration is fixed at `N=4`, `q` in `{1,2}`, incoming phase `0..3`, six input Ports, prior pointer phase `a` with `a+q<4`, and prior material momentum components each in `{-1,0,1}`, with family quantum 1 and a fixed bijective port map. There are exactly `(3+2)*4*6*27 = 3240` permitted complete inputs, requiring 3240 distinct complete outputs and exact inverse recovery. This count excludes the separately tested raw modular wrap case.

Example plans: a 9-by-9-by-1 board with a three-Node route to one output and one phase-varied carrier; a serpentine layout with at least 100 coverage Nodes feeding one output on a sufficiently large board; four separate chains of three Nodes with separate outputs and threshold 2. Preserve their finite capacities, time horizon and no-escape conditions. Do not claim that three or 100 covered Nodes impose that many quanta per measurement.

### Remaining physical questions

This candidate is classical, local and reversible on its admitted domain. It demonstrates a concrete mechanism for physical finite-memory readout and preservation of carrier/apparatus distinctions. It does not provide the full requirements for arbitrary default-world interactions, lossy merges, absorption, saturating/resetting apparatus, a momentum-sensitive quantum measurement, Born probabilities or an uncertainty relation. The owner's cell-sensitivity hypothesis remains falsifiable: this reversible routing/counter alone admits sharply specified position and momentum, so a universal positive Heisenberg lower bound does not follow merely from these two ingredients. Future preparation/interaction laws must supply and test the missing restriction; do not invent `hbar`, noise or an output clamp to make it pass.
