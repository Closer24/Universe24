# Universe24 detector requirements

Date: 2026-09-19. Status: consolidated requirements; the implementation contract of the explicitly selected `reversible-detector-v1` candidate was deleted the same day, absorbed into [the law of the ray](RAY_LAW.md) (history marker in its section below). Code and physical validation are separate evidence. Tracked in [issue 342](https://github.com/Closer24/Universe24/issues/342).

Source baseline of the candidate: `events-v1`, commit `bfb463be6313ae226aa0a192d11036ead63dd0f1` (history: `events-v1` was deleted on 2026-09-19 with the candidate; the active engine is the law of the ray). This document owns the detector requirements and the record of the scoped candidate contract below. The default `events-v1` measurement and mixing rules remained as documented in ENGINE.md until that deletion. The candidate deliberately did not call their lossy transitions.

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

The baseline [engine contract](https://github.com/Closer24/Universe24/blob/bfb463be6313ae226aa0a192d11036ead63dd0f1/docs/ENGINE.md) of the law of events treated a click as a one-way boundary with the phase recorded externally; the law of the ray of 2026-09-19 keeps the click as the one one-way border and reads the phase on the board as the detector's coherent record ([the law of the ray](RAY_LAW.md), section 5). The ownership map below is the one under which the candidate was designed; the modules it names are `nature_beam.py` (the interval) and `engine.py` (the frame) since that day.

| Existing owner | Required design work |
| --- | --- |
| `events/world.py` | Separate coverage, resolution, trigger and physical output layout in the world contract. Existing `positions` and per-Node `threshold` do not define a causal shared output. |
| `events/engine.py`: `Measured`, `_meet` | Specify a local reversible interaction and physical record encoding, preserving incoming distinctions and prior apparatus information without overwriting its clock. |
| `events/nature_beam.py` (the walk and the collision, since 2026-09-19) | Carry all required physical information through local propagation; the flight and the collision are bijections and lose no distinction. |
| `events/engine.py`: `detectors()`, `_event` | Keep diagnostic aggregation and exported records separate from the physical result they describe. Neither supplies missing physical memory. |

This is an ownership map, not a new API. Before coding, publish the local operator, its input/output domain, Event encoding and capacities, timing, saturation/reset behavior, invariant accounting, allowed preparations and observable/unit mapping. Missing physics must remain an open design decision. Full-board information preservation also requires examining other merges and mixing operations.

## Acceptance checklist for later work

- **A1 — Determinism and locality:** identical complete inputs replay identically; audit integer intermediates, bounded storage and causal input provenance. Enabling diagnostics cannot change the trajectory.
- **A2 — Information:** test incoming phase 0 versus 16, distinct prior detector states and full-capacity/reset cases. Their complete physical states remain distinguishable and reconstructable without history logs. This witness alone is not a proof for all states or all rules.
- **A3 — Generic grouping:** cover one Node and several configured sizes, including three and a larger group, and separate shared from individually distinguishable outputs. Under a one-quantum trigger, arrival at any covered Node can give the contracted common spatial category while retaining distinct complete physical states. Vary the trigger independently of group size; reject unsupported bounds. Output cannot depend on information that has not yet arrived.
- **A4 — Conservation:** verify the model's exact invariants across input, detector, supporting environment and output, with explicit edge handling.
- **A5 — Quantum research:** freeze preparations, calibration, reference expectations and discrepancy criteria before uncertainty/Born/sequence comparisons. Record failures and finite-board limits. These are research runs, distinct from isolated generic-rule unit tests.

The owner proposes that finite cell sensitivity together with information preservation on the board will produce the Heisenberg relation. This is the research hypothesis to investigate, not a rule inserted into the output. The reversible detector candidate of 2026-09-19 supplied a concrete reversible interaction for D5 on a declared domain; the law of the ray absorbed it the same day (below); whether any such mechanism supplies Q1 remains open.

## Implementation contract: reversible-detector-v1

Deleted on 2026-09-19 with the law of the ray (the model owner, Highlights
5.4; [the law of the ray](RAY_LAW.md), section 1): the candidate's pointer is
the detector's squared coherent record, its `transduce` and `port_map` are
the re-emission on declared directions (`rerelease` with `directions`), its
refusal of an open face is the face detector, and its `dynamics` key,
schema, operator, inverse, capacity and readout are gone. The contract's
text is in git at any commit before the deletion (`ce0b22af` the last);
its two example runs keep their scope in [validation](VALIDATION.md). The
requirements above stay; the reversibility they asked for is the ray law's
bijection of the interval (`tests/test_ray_bijection.py`).

## Remaining physical questions

The ray law is classical, local and reversible on the board without a
measured event; the click is its one one-way border. It demonstrates a
concrete mechanism for a physical readout (the squared coherent record of a
crowd of rays) and preserves the record of every ray in flight. It does not
provide the full requirements for lossy merges, absorption, saturating or
resetting apparatus, a momentum-sensitive quantum measurement, Born
probabilities or an uncertainty relation. The owner's cell-sensitivity
hypothesis remains falsifiable: a reversible routing alone admits sharply
specified position and momentum, so a universal positive Heisenberg lower
bound does not follow merely from these ingredients. Future preparation and
interaction laws must supply and test the missing restriction; do not invent
`hbar`, noise or an output clamp to make it pass.
