# Highlights implementation coverage

## Highlights as the edited specification and the ray-event decisions - 2026-09-17

Reviewed `docs/HIGHLIGHTS.md` as revised on 2026-09-17 on branch
`design/ray-event-model`.

By the model owner's decision of 2026-09-17, [docs/HIGHLIGHTS.md](HIGHLIGHTS.md)
became the Highlights specification and the only copy that is edited; the
Google Doc is its historical source up to the revision of 2026-09-16 and is
neither edited nor resynced. The 2026-09-17 revision restates sections 3.3,
3.4, 3.5, 3.15, 3.19, 3.20, 5.1 and 5.4 (exactly two definitions, event and
ray; every ray a wave ray carrying a phase, its step count and the information
of its last event, with the bit if that event was at a Detector; the Detector
as a marked Node that draws once per arriving transfer and returns the ray
unchanged by its step count; the return as the inverse split of that ray's
share at its event Node, with no register at the origin, no occupied channel
and no capacity rule (the displacement rule of 5.1 deleted); a field ray as
the ray's own information in ray form, making no event unless it meets
something it changes, and returning
reversed as the emitter's recoil; a bound group with no lifetime of its own)
and deletes section 3.18, the shared quantum resource.
[POSTULATES.md](../POSTULATES.md) (sections 1, 4, 22, 23 and 24, with a note
on section 14), [the ray-event model](RAY_EVENT_MODEL.md), the
[documentation index](README.md), the [README](../README.md) and
[project status](PROJECT_STATUS.md) were synchronized to it.

This is documentation only: no implementation, runtime behavior, test or
configuration changed. The implementation contracts (the Detector-owned
sampling, quantum, spatial-fields and local-conversion contracts, with the
definitions, architecture, terminology and test-expectation sections that cite
them) describe the current code until the ray-event migration in
[RAY_EVENT_MODEL.md](RAY_EVENT_MODEL.md#6-migration-in-order) updates them.
Bell results recorded with the former shared resource remain historical
evidence about that profile, not evidence for the current model.

## Conservation as local accounting - 2026-09-17 (`ray-event-audit-v1`)

Issue #169, feature 10, implements the audit of section 3.15
([audits](SPATIAL_FIELDS.md#audits-ray-event-audit-v1), [the world
ledger](LOCAL_CONSERVATION.md#the-world-ledger-ray-event-audit-v1)):

| Highlights | Implementation |
| --- | --- |
| 3.15, exact accounting across all actual owners: retained participants, products, recoil, fields, apparatus, in-flight values and remainders | One ledger per completed tick per conserved readout (amount per family, momentum, charge), each line initial, sourced, current, escaped, annulled, absorbed with initial + sourced = current + escaped + annulled + absorbed exact; `current` reads rays, records and their stock, populations and in-flight packets |
| 3.15, a gain requires a loss, a transfer or an explicitly accounted source | `sourced` names the releases, sourced emissions and split bookings; `escaped`, `annulled` and `absorbed` name the sinks; dissipation is no line and does not balance |
| 3.15, reconstruction: a returning ray holds its event to undo it exactly | A returning ray reads its momentum as its share on the event's heading and its charge as charge x amount, in the world ledger and in the local audit alike, so the return and the inverse split leave every line exact |
| 3.19, the external body's sinks and momentum | The `absorbed` line is what the bodies' sinks took (`external_body_totals`); the bodies' count, momentum, charge and sinks are their own lines beside the identity |
| 3.26, the engine validates without inventing | A meeting whose outputs would change the total charge is rejected at validation; the runner's `conserved_at_every_completed_tick` is the ledger's identity re-checked from the recorded integers, and a record altered by hand is reported by tick and line |

## Binding and gravity by delay - 2026-09-17 (`ray-binding-v1`)

Issue #169, feature 8, implements the bound group of section 3.4 and gravity
as bending by delay of section 3.28
([binding](SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1)):

| Highlights | Implementation |
| --- | --- |
| 3.4, matter is a bound group; binding is the interaction whose result is zero events, the rays stay at the Node and interact again every interval | A `ray_interactions` rule without outputs assigning `delay` 1 holds its participants; the rule fires again every interval, the group's tick, stamped as one event and published as `bound_tick`; `bound_group` reads the group from the Node's rays and the snapshot lists `bound_groups` |
| 3.4, mass is the retained energy of a bound group; the group's phase advance is its clock | The held rays keep their amounts; each phase advances once per interval by its family's rest rate; the group's mass in phase units is the sum of the rates |
| 3.4, the binding may be a very large output-clock delay; a large mass makes the Node very slow | `ray_delay` on the binding rule: every arrival at the group's Node waits the declared intervals, one Node-wide wait approximating the six per-face clocks of 3.28 |
| 3.4, unbound the same way anything else happens: a ray arrives and the declared coupling produces events that leave | An earlier declared outputs rule naming a bound participant and an arriving ray fires; its outputs leave as new event rays; the binding rule no longer fires |
| 3.5, a bound group releases its field | A held ray releases on all six headings once per interval, booked as a source |
| 3.28, the met ray is delayed, its output clock grows, more on the side nearer the heavy Node | A meeting output's `delay` by a declared table per the Port the field ray came through, in phase steps of the face clock on that side, carried as the ray's `lag`; feature 8b planned (2026-09-17, Highlights 3.28): lag modulus decoupled from `phase_bits`, the lag counted in its own modulus declared per family, after feature 10 |
| 3.28, the ray bends toward the heavy Node; bending is a change of momentum | A transverse lag that reaches the phase modulus (the lag's own modulus after feature 8b) is spent as one Link toward the lagging side at a later departure; the field ray returns reversed as the recoil; the momentum the turn moves is booked at the meeting as the meeting's source, the recoil's coupling to the group being open |
| 3.17, remainders | The lag below the modulus stays on the ray as its owner; the floor of the delay is of a clock count, not of content |
| Hypothesis 14, G = hbar c / (N m_0)^2 | `test_ray_binding.py` pins G_eff x N^2 = 64 over N = 2^8, 2^10, 2^12, 2^16 with the mass N / 4 phase steps per interval and b = 4 |

## The field as the ray's information - 2026-09-17 (`released-field-v1`)

Issue #169, feature 7, implements the one field rule of sections 3.5 and 3.28
([released field](SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1)):

| Highlights | Implementation |
| --- | --- |
| 3.5, a ray has a field, the ray's own information in ray form, released in all directions without an event | A ray field with `field_of` and `release`; `release_field` releases one G ray per Port heading except the source's own at every Node the source departs, with the source's phase and no event stamp |
| 3.5, the free ray pays nothing until its field meets something; 3.15 | The released amount is booked as an explicitly accounted source of G; the source ray's amount, phase and heading are untouched |
| 3.5, a straight ray never meets its own field, no exclusion rule | The ray's own line ahead of it is the ray at link speed, so that heading is not released; the other five leave behind or away from the line; the test asserts no shared Node over the run |
| 3.5 and 3.14, the field ray returns reversed as the recoil, at finite speed | A `ray_interactions` rule with an output of heading `"reversed"`; the test pins the recoil walking back one Link per tick |
| 3.3, the field acts at the crossing | The meeting fires in the interval the G ray and the responding ray share a Node, like every meeting |
| 3.17, remainders | The fraction the floor leaves is not released; a description booked as a source destroys nothing |
| 3.28, gravity is bending by delay | The delay and the turn are outputs of the declared rule (heading, delay or phase); the delay by a table per Port and the turn it produces are feature 8 (`ray-binding-v1`, above); the recoil's coupling to its source and to bound groups is open |
| 3.19, the external body (`external-body-v1`) | Feature 7b (done 2026-09-17) releases the body's field on six headings by the same rule (`body_release`), booked as a source, with the sink it declares |
| 3.5, light is the field, and the field spreads (model owner, 2026-09-17) | The catalog's `light` family is the field of the electron and the positron (`field_of`, released by `release_field` as any field) and the family every source emits, `electron_field` and `positron_field` removed; its `spread` entry, the six-heading split table by which every Node the field reaches releases it again, the backward heading included and a quantum never waiting, is feature 12, field spreading (next row), declared `[6, 1, 1, 1, 1, 1]`, its cost measured before adoption in the [performance record](PERFORMANCE.md#plan-compiling-the-catalog-into-transition-tables); a family that declares no `spread` keeps its field on the six axis lines of its source, and its light goes straight; a field ray is a ray with an empty event record, rest rate 0 and charge 0, and nothing else (3.5, the field is matter's message about itself, 2026-09-17), and the sign of the source's charge as a visible property on the field ray, `source_sign`, the light family's `releaser`, is set by feature 12 at the release, never the phase, with which `electron_field_turn.opposite_charge` closes (A5) |
| 3.5, light is the field and the field spreads (`field-spreading-v1`) | Feature 12 (done 2026-09-17): a family's `spread` table makes every Node its content reaches release it again in all six headings, amounts adding per arriving heading, the phase of the coherent sum, whole quanta by the table and the remainder through the entry the phase selects; the momentum difference booked as a source ([field spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)) |

## Ray integration and local Focus - 2026-09-14

The repository now distinguishes the optional [local Focus scheduler](LOCAL_FOCUS.md)
from quantum Focus. It skips certified empty carrier Nodes while retaining exact
local transitions, clocks and model cost. A sparse 256-tick carrier probe measured
2.32x host speed with matching inventory; this is not a universal speed claim.
Integrated ray policies now validate retained owners, preserve funded stock during
load waits, prepare bounded immutable pace tables and reject unproved self-exclusion
combinations. The bond registry is bounded and idempotent and remains the
declared nonlocal exception of postulate 4 in ordinary Simulation. Q-ORACLE
remains an independent option.
See [validation](VALIDATION.md) for scope and evidence. This entry updates the Git
companion only; it does not claim a live Google Docs revision was changed.

## General research scope and effective formulas - 2026-09-14

Reviewed main: `18bc9eef361f1199e198aa13901a5a67f29c5ed8`.

Universe24 is intended as a general-purpose experimental model for investigating
physical phenomena throughout the universe, from individual disturbances and
light to matter, fields and large-scale systems. Any physical phenomenon can be
a research target; each experiment requires an explicit representation, supported
local rules and independent validation. The aim is broad scientific testing, with
demonstrated coverage growing as experiments are added. This research scope does
not imply that every phenomenon is already represented or computationally feasible.

The model may also help discover and derive effective mathematical relations from
its discrete local rules. Measure patterns and scaling, propose a candidate
formula, and test it on new configurations and scales. A derivation must explain
why the relation follows from the rules and identify its domain of validity and
approximation errors; curve fitting alone is not a derivation. An input formula,
a fitted observation and a relation derived from local dynamics remain distinct.
Comparison with independent physical evidence is needed before identifying a
candidate relation with a law of nature.

This extends the research purpose of live Highlights section **1.2.8** while
preserving the preceding experiment evidence and its stated limitations.
Connector readback verified both new paragraphs, inherited typography and the
unchanged surrounding text and source link at revision
`ANLCKQmjYawB_yYVKG1SxUrPM1Db4J80QFFRHMgHtFeUKkhQBL2qH9no65jFVVJ3A5H72BkF5xM0moWk87qw3ghhpfuSYLKR2WiWLthjl1o`.
It adds no simulator capability, physical law or new run result. The existing
postulates and validation workflow already require the distinction between
research goals, configured assumptions and demonstrated behavior.

## Discrete space, classical mechanics and light - 2026-09-14

Reviewed main: `0299cb98bf07f00dc10bad858b674ded449be03e`.

Live [Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
now includes section **1.2.8, Discrete space as a bridge between mechanics and
light**. The targeted addition preserves the original tab and adjacent sections.
A trusted file-backed read found no protected controls; connector readback
verified the text, heading, six native bullets and eight source links, including
their inherited typography. The verified revision is
`ANLCKQnABgyxqtiJn8wArsNKkX0YrpvZ_aAX8xLsUDpWQSK7uhoaEdZbA6M8rFZXGZEzbdH1ZT3XyE9L35kbJyOz9lwDerOKvQfnxSVCd8k`.

Universe24 provides a common discrete setting for classical mechanical records,
finite quantum states and ray-like radiation: Nodes hold state, Links carry
arrivals, and Events change the participating owners. The current experiments
connect wave interference, individual detections and effective classical behavior
within this setting. This makes a light-beam model a useful meeting point between
wave behavior and mechanical exchange. The ray and quantum-register candidates
remain distinct representations; a shared setting is not yet a single derived
theory of matter and light.

The role of discreteness is concrete: geometry determines available paths,
neighboring encounters and integer transit times. Given a configured phase
advance per Link, different path lengths produce different phases at a detector.
The fringe is measured after local propagation and capture; no screen pattern is
prescribed. Discrete geometry alone does not supply the phase/coherence rule,
quantization of the carried amount or the capture instrument. Those are explicit
model choices whose consequences can be tested.

| Connection demonstrated | Recorded evidence | Necessary qualification |
| --- | --- | --- |
| Optical wave behavior from local ray transport | [Kerengonen double slit](../examples/kerengonen-double-slit/README.md): one lamp illuminates two absorbing/re-emitting slits; phase changes the screen pattern, while the plain field gives the sum of the two single-slit controls | Carried phase, coherent capture and the slit re-emission rule are configured |
| Where the classical wave stops and the quantum owner begins | Bell test on the phased-ray field (`examples/kerengonen-bell/`, deleted on 2026-09-17): the same CHSH settings give 1.40 on the classical candidate and 2 on the plain field, against 14/5 from the finite quantum owner | The phase is the only hidden variable and local absorption the only instrument; the classical value is the model's prediction, not a loss of visibility |
| Whole detections and a classical mean flux | Counting probe (`examples/quantum-classical/README.md`, deleted on 2026-09-17): one-quantum arrivals are 0 or 1; their average approaches the measured inverse-square profile in the tested geometry | Integer quanta and the heading distribution are supplied; this does not identify physical photons |
| Radiation and mechanical exchange | [Local conservation contract](LOCAL_CONSERVATION.md) and [runner validation](VALIDATION.md#kerengonen-guards-reconciled-with-current-main---2026-09-14): funded emission, recoil, absorption and escaped rays close the declared energy/momentum accounting | The quantity definitions and exchange laws are explicit; this is not complete electromagnetic dynamics |
| Coherent evolution and classical probability | Quantum-to-classical probes (`examples/quantum-classical/README.md`, deleted on 2026-09-17) and claim check (`examples/quantum/quantum_classical_check.md`, deleted on 2026-09-17): configured dephasing removes interference and reproduces the finite classical probability control | Classical probability evolution does not by itself derive a Newtonian trajectory or explain a unique measurement outcome |
| Matter-wave wavelength and momentum | De Broglie probe (`examples/de-broglie/`, deleted on 2026-09-17): momenta 16, 32 and 64 move the first dark fringe to 4, 2 and 1 | The phase advance `abs(p) / 4` is supplied; the inverse relation is propagated and measured, not derived from spatial discreteness |
| Quantum contact and later ordinary motion | Recurrent contacts (`docs/RECURRENT_QUANTUM_CONTACT.md`, deleted on 2026-09-17) and local moment response (`examples/quantum/local_moment_exchange.md`, deleted on 2026-09-17): local encounters can continue a wave, create a new one or localize a record; a later local exchange can produce slow motion | Finite instruments and the response law are supplied; complete field/matter closure and an emergent classical trajectory remain open |

The supported highlight is therefore a tested bridge between selected classical,
quantum and optical behaviors on discrete space, with a clear route for stronger
tests. Deriving their common microscopic law, physical constants and full
matter/field dynamics from discreteness remains a research goal. The linked
reports retain their own tested source identities; this documentation update
does not represent them as fresh executions on the reviewed main commit.

## Signed relative field phase - 2026-09-14

The field-phase contract (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17)
now explicitly preserves `(unit / vacuum)^n` for negative field exponents by
conjugating both coefficients. Equivalent complex representations produce the
same quantum capture probabilities and ordinary envelope weights. This repairs
the existing configured law; it adds no field back-reaction or conservation
claim. The one-shot phase and null-notice options remain separate from recurrent
generations, whose unsupported combinations fail at initialization. The live
Highlights document was not edited; numerical regressions and source evidence
are linked in [validation](VALIDATION.md).

## Wave moments and position output - 2026-09-14

Live Highlights was reconciled read-only at the time of this entry.
Section 4.7.5 requires position and momentum to describe the same wave without
assigning both sharply. The position-output experiment (`examples/quantum/position_moment_response.md`, deleted on 2026-09-17)
derives a finite derivative observable from actual spatial density and output
moments from a local operator row. Its Fourier eigenvalue `2 sin(k)` gives
partial coverage of the Fourier-momentum target, not canonical momentum or a
free-particle law. The readout is diagnostic; Nodes receive only bounded
prepared values at capture. The report exposes unclosed gate/measurement energy
and distinguishes output re-encoding from vacuum. This is a candidate under
existing contracts. The live Highlights document was not edited.

## Local response candidate - 2026-09-14

The local moment-response experiment (`examples/quantum/local_moment_exchange.md`, deleted on 2026-09-17)
now composes quantum capture with an explicitly supplied ordinary local law.
Mean momentum and its variance swap with a colocated equal-mass reservoir;
the one-shot detector records completion locally. The resulting carrier moves,
while the reservoir retains unresolved momentum. This is an expectation-level
moment closure and a tested candidate, not a derived classical limit or full
field/matter quantum dynamics. Its independent exact quantum SWAP control retains
phase and branch balances; those capabilities do not transfer to the ordinary
moment-only state. No binding postulate was changed. The live Highlights
document was not edited for this experimental candidate.

## Quantum-to-classical claim check - 2026-09-14

The bounded investigation (`examples/quantum/quantum_classical_check.md`, deleted on 2026-09-17) verifies
configured dephasing, coherent recovery and classical probability evolution.
Spatial localization produces a held record with unknown momentum; an emerging
Newtonian trajectory remains unestablished. This adds measured evidence, not a
new physical rule or entity. The live Highlights document was not edited.

## Recurrent local contact outcomes - 2026-09-14

Live Highlights section **4.7.8, Configured recurrent local outcomes**, now records
the complete configured instrument, local/new-wave/continuing outcomes, single
inventory ownership, atomic new origins, finite ordinary source generations and
causal cancellation. It retains the finite-candidate and physical-closure limits.
The new section was verified in the live document without changing adjacent sections.

| Highlights rule | Authoritative owner | Acceptance |
| --- | --- | --- |
| Complete local outcomes with no separate random switch | Recurrent contract (`docs/RECURRENT_QUANTUM_CONTACT.md`, deleted on 2026-09-17), postulate 21 and Q-RECURRENT-1 | Exact source 9/16 and capture 9/16/144 ticket counts |
| Fresh origin without duplicate inventory or replay | Quantum event network (`src/event_universe/quantum/event_network.py`, deleted on 2026-09-17) | Occupied-domain rejection, atomic result and same-tick replay tests |
| Local ordinary source banks and causal cancellation | Recurrent resolver (`src/event_universe/integration/recurrent_contact_runtime.py`, deleted on 2026-09-17) | Remote-prefix equality, finite allowances and signed vector inventory |
| Repeated encounters followed by localization | Initialization and recorded expectations (`examples/quantum/repeated_contacts.md`, deleted on 2026-09-17) | Fresh-wave ticks 3/9/21, localization 24, balanced field decay |

The [validation record](VALIDATION.md) binds these results to the exact tested
source. This is not a general many-body Hamiltonian, physical energy closure or
a completed derivation of the classical limit. Older dated rows below retain
their own source revisions and do not describe this addition.
## The ray: one object for wave and particle - 2026-09-14

This entry maps the straight-ray field and its Kerengonen extension to the
Highlights sections on fields, quanta and the classical limit (1.2, 4.7, 10.3).
It reconciles the repository at main `c3c39d0` after
[PR #98](https://github.com/Closer24/Universe24/pull/98) plus the eight later
commits on the working branch; the live document was not edited.

A ray is a whole amount of one scalar field with a fixed integer heading and
three routing accumulators that keep it on one lattice line, one link per tick.
With the `kerengonen` key it also carries a phase that advances per link, and
each ray may carry its own advance, stamped at emission from an expression over
the emitter's fields (`|p| / D` is the de Broglie rule). Rays that meet at a
Node combine by phase; the coherence of what met, from a fixed-point integer
cosine table, gates the value a reader samples and the share an absorber
takes. Amounts are never changed by phase: the audit sums quanta. Absorption
is a run-time choice, the coherent share or a whole-ray lottery drawn by a
record-row ticket. A record that absorbs keeps the phase, advance and heading
of what it took: an emission may carry that phase on (a Huygens slit), send
the amount back along the mirrored heading (a mirror), or pay a record out on
a schedule (`dissolve`: a particle becoming its own wave train).

| Highlights sections | Implemented contract and limits | Repository owner |
| --- | --- | --- |
| 10.3.2 | Straight rays: isotropic inverse square, shell conservation, a small stock sweeping the heading sequence in turn. | [Straight-ray contract](SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1) |
| 4.7, 10.3 | Energy closure: funded emission with recoil, absorption with momentum, signed quanta paid by the absorber, rays measured as quanta by the event audit. Attraction that the pulled body pays for. | [Funded emission and absorption](SPATIAL_FIELDS.md#funded-emission-and-absorption), gravity probe (`examples/gravity-probe/`, deleted on 2026-09-17) |
| 1.2, 4.7 | Kerengonen phased rays: coherence-gated sampling and absorption, share or lottery capture, Huygens slits, mirrors, per-ray de Broglie advance, dissolution. Identity `kerengonen-ray-field-v1`. | [Kerengonen contract](SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1) |
| 3.3, 3.19, 3.20, 5.1, 5.4 | Ray hidden state (2026-09-17, issue #169 feature 1): every ray carries its steps since its event, whether it is outbound, the Ports and shares of its event and the Detector bit; emissions and ray interactions stamp them, rays of different events never merge, a returning ray counts steps and phase down, and no rule reads them. Identity `ray-event-state-v1`. | [Ray state](SPATIAL_FIELDS.md#ray-state-ray-event-state-v1), [expectations](TEST_EXPECTATIONS.md#ray-hidden-state) |
| 3.19, 3.20, 5.4 | Node Detector bit (2026-09-17, issue #169 feature 2): a Node marked in the initialization (`detectors`: position, setting, ticket seed, no default rate) draws one unsalted bit per arriving ray from its own ticket stream, independently for up to six arrivals in one interval, in Port then merge-key order, reading nothing from the ray; on 1 the ray passes as at an unmarked Node with its Detector bit set to 1 and a `detector_click` recorded, the only measurement; on 0 the ray records bit 0 and no click and is returned (next row); a replay redraws nothing and an unmarked Node never draws; since feature 2b (two rows down, `detector-bit-property-v1`, landed 2026-09-17) the draw is for a ray carrying no bit, a ray carrying a bit being read by the mark's declared coupling (`apparatus.detector.couplings`, `on_bit_1` and `on_bit_0`, decided: `pass` by default, `draw` the alternative). Everything begins and is realized at a marked Node (5.4, model owner, 2026-09-17): a source is a Detector, so every ray's history begins at a marked Node, a marked Node that draws 1 realizes one path of events and its return cancels the others through their event, and the physical picture is the list of PASS clicks in the observer's frame, the rendering of the board being the record's view that no observer inside the world has. Identity `detector-mark-v1`. | [Detector mark](DETECTOR_SAMPLING.md#the-detector-mark-detector-mark-v1), [schema](SPATIAL_FIELDS.md#detector-mark-detector-mark-v1), [expectations](TEST_EXPECTATIONS.md#node-detector-bit) |
| 3.19, 3.20, 5.4 | Detector return (2026-09-17, issue #169 feature 3): on a draw of 0 the marked Node returns the arriving ray in the same interval, the same wave ray reversed on its line with its amount, phase and event record unchanged and `outbound` 0, leaving through the Port it came in through one Link per tick; on the walk back it enters no coupling and no absorption, is sampled by nothing, merges with nothing and is drawn for by no mark, its steps and phase count down, and at steps 0 it rests at its event Node, inert, with the phase it left with, until the inverse split (feature 4); a return records a `detector_return` event and no click, its momentum reads as its share on the event's heading so the audits stay exact, and a world without a mark is unchanged. Identity `detector-return-v1`. | [The return](DETECTOR_SAMPLING.md#the-return-detector-return-v1), [transport](SPATIAL_FIELDS.md#detector-return-detector-return-v1), [expectations](TEST_EXPECTATIONS.md#detector-return) |
| 3.20, 3.26, 5.4 | The Detector's bit as a property (2026-09-17, issue #169 feature 2b): the bit a marked Node set travels with the ray as a property like charge. The outputs of every ray interaction that fires inherit it, the highest bit of the inputs by the order 1 over 0 over none unless the rule declares `bit` (`"highest"`, `"none"`, `{"of": i}`); a coupling reads it at a meeting as the read-only ray property `detector` (0 none, 1 a draw of 0, 2 a draw of 1) in a `when` guard or an invariant; and a marked Node reads it before it draws, by its declared couplings `on_bit_1` and `on_bit_0` (`"pass"`, the default, or `"draw"`): a ray carrying 1 passes without a draw, a ray carrying 0 is a transmission and is never drawn, each recorded as a `detector_pass` event, and only a ray carrying no bit is drawn. The runner records the identity when a world declares a key of the rule; the viewer draws the pass and carries each ray's bit; the catalog's two couplings are decided. The price of 5.4 is to be re-derived under this rule by hypothesis 11 and experiment A13. Identity `detector-bit-property-v1`. | [The bit read](DETECTOR_SAMPLING.md#the-bit-read-detector-bit-property-v1), [schema](SPATIAL_FIELDS.md#the-detectors-bit-as-a-property-detector-bit-property-v1), [expectations](TEST_EXPECTATIONS.md#detector-bit-as-a-property) |
| 3.17, 3.20, 5.4 | Inverse split (2026-09-17, issue #169 feature 4): a returned ray at its event Node performs the inverse split of its own share in the next cycle by the world's `return_mode`: `siblings` (default) transmits its amount, phase and bit to every line the event sent to except its own as new event rays, the amount shared exactly with the remainder by 3.17; `straight` continues it on the one line opposite its own; `annul` ends it into an explicitly accounted sink, initial + sources = current + dissipated + escaped + annulled at every completed tick. If the event's input is at the Node the share is first restored to it exactly and the transmission funded from it in the same interval; a returned ray meets what else is at the Node by the declared couplings before the split (none in this slice); an `inverse_split` record per split. Identity `inverse-split-v1`. | [The inverse split](DETECTOR_SAMPLING.md#the-inverse-split-inverse-split-v1), [transport and bookkeeping](SPATIAL_FIELDS.md#inverse-split-inverse-split-v1), [expectations](TEST_EXPECTATIONS.md#inverse-split) |
| 5.1 | Layers (2026-09-17, issue #169 feature 5): the layers of event spacetime are derived, never declared, as the connected components of the ray fields over the participants of the declared `ray_interactions`, a field no rule selects being its own layer; at a Node in one interval the rays are met layer by layer, rules of different layers fire independently with their own participants, invariants and events, an unruled ray crosses unchanged, and the runner records the derived layers. A single-layer world runs as before. Identity `ray-layers-v1`. | [Layers](SPATIAL_FIELDS.md#layers-ray-layers-v1), [expectations](TEST_EXPECTATIONS.md#ray-layers) |
| 3.15, 3.17, 3.26, 5.1 | Meeting of rays with N-to-M outputs (2026-09-17, issue #169 feature 6): a rule with declared outputs replaces its participants by one to six new event rays at the meeting Node, each stamped `steps 0` with the mask and shares of the meeting; every family's stock and the declared readout invariants are exact as sums over inputs and outputs; an amount may be split by a declared table indexed by the phase difference of two inputs, the rest output owning the remainder (3.17), the engine only splitting by the table (3.26); the momentum a split moves is booked as an accounted source until the field ray of feature 7 owns it (3.15); no draw. Identity `ray-meeting-conversion-v1`. | [Meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1), [expectations](TEST_EXPECTATIONS.md#ray-meetings-with-outputs) |
| 3.3, 5.1 | Wave-ray families (2026-09-17, issue #169 feature 9): every ray is a wave ray, a plain ray the special case with rest rate 0; each family's catalog entry declares its phase width `phase_bits` (a mask, never a division, no bound in the model), its rest rate (`kerengonen.phase_advance`, 0 for light, whose rays carry the emitter's phase unchanged) and its charge per quantum; `RAY_PROPERTIES` gains read-only `family` and `charge`, and `charge x amount` summed over rays is an invariant of every declared ray interaction and a world readout. Identity `wave-ray-family-v1`. | [Wave-ray families](SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1), [expectations](TEST_EXPECTATIONS.md#wave-ray-families) |
| 3.5, 3.19, 3.28 | External body (2026-09-17, issue #169 feature 7b): the world key `external_bodies` declares a Node holding a family with an amount of any width, a charge, an initial momentum (heading and pace), a coupling and a momentum table; it radiates the released field of its family on all six headings every interval, `floor(amount x n / d)` per heading, booked as a source; it never spreads and no ray of its family exists at its Node; whatever arrives is met by its coupling, the explicitly accounted sink by default (`external_body_totals()`, the conservation line initial + sources = current + dissipated + escaped + annulled + absorbed_by_bodies) or a declared meeting with outputs in which the body is the participant that never changes (a mirror, a splitter, a phase plate); only field rays its table names move it, sign x amount x heading, and its velocity is an exact accumulator per axis that steps one Link when a whole amount has accumulated, the bodies' momentum an audit line of its own; the runner records `external_body: "external-body-v1"` and `external_bodies` with positions per tick. Identity `external-body-v1`. | [External body](SPATIAL_FIELDS.md#the-external-body-external-body-v1), [expectations](TEST_EXPECTATIONS.md#external-body) |
| 3.5, 3.17, 3.20, 3.23 | Field spreading (2026-09-17, issue #169 feature 12): a ray family's catalog entry `spread`, six weights in Port order relative to the arriving heading (forward, backward, four equal transverse, the backward one positive), makes every Node its content reaches release it again in all six headings, after the marks and the meetings and before the departures: the outbound content that arrived is taken off the Node, amounts add per arriving heading, the phase is the phase of the coherent sum, each heading's content is shared in whole quanta by the table and the remainder leaves whole through the entry the phase selects, so a quantum never waits; the departures are fresh field rays with no event; the total is exact, the momentum difference is an accounted source of the bound momentum field, the local audit reads the `field_spread` record; the runner records `field_spreading: "field-spreading-v1"` and `spreading_fields` only when a family declares `spread`, and a world without one is byte-identical. The sign of the source's charge travels on the field ray as `source_sign`, a visible property like the Detector bit and never in the phase (3.5, the field is matter's message about itself); a returned field quantum walks back along its line, with no inverse split, until its emitter, its source, coupled content, a body or the boundary takes it (the `field_returned` record): the orchestrator's proposal of 5.5, implemented exactly and pending the model owner's decision. Identity `field-spreading-v1`. | [Field spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1), [expectations](TEST_EXPECTATIONS.md#field-spreading) |
| 1.2, 4.7 | Measured: two-lamp and single-lamp double slits with exact additivity without phase, single quanta building the fringe, fringe period inverse to momentum for beams and for a dissolving particle, standing waves with period `phase_steps / (2 x advance)`, a thick screen absorbing what a thin one lets pass, a round front and a Euclidean fringe on the Euclidean pace, a whole particle gathered to one screen Node with the probability of its wave. | [Double slit](../examples/kerengonen-double-slit/README.md), de Broglie (`examples/de-broglie/`, deleted on 2026-09-17), matter wave (`examples/matter-wave/`, deleted on 2026-09-17), mirror (`examples/kerengonen-mirror/`, deleted on 2026-09-17), Euclidean pace (`examples/euclidean-pace/`, deleted on 2026-09-17), claim and gather (`examples/claim-gather/`, deleted on 2026-09-17), [validation](VALIDATION.md) |
| 1.2, 10.6 | Quantum-to-classical seams on existing rules: a dephased walk equals the classical chain, quanta click whole and average to the inverse square, repeated captures follow the geometric decay law. | Quantum-to-classical probes (`examples/quantum-classical/README.md`, deleted on 2026-09-17) |

What the ray is not, recorded rather than claimed: a single particle's matter
lands spread as its wave unless the field has claims, because rays carry
conserved stock and no local rule can retire the rest of a wave when one Node
captures without a faster signal; with [claim and gather](SPATIAL_FIELDS.md#claim-and-gather-claim-gather-ray-field-v1)
(`claim-gather-ray-field-v1`) a slower matter wave is gathered whole to the
capturing Node by a claim that floods at link speed, so the landing is whole
but takes time, and the earlier of two captures wins; a mirror reflects across a lattice axis or a
lattice diagonal, whole or by a fraction, not at an arbitrary angle; fringes
follow Manhattan path difference on the links metric and Euclidean path
difference on the [Euclidean pace](SPATIAL_FIELDS.md#euclidean-pace-metric-euclidean)
(`euclidean-ray-pace-v1`), where rays wait at Nodes and are slower, never
faster, than one link per tick; the lottery ticket is a configured local
sequence, not physical randomness; the event audit re-measures every owner per
event, so audited worlds stay small; and the ray is a local model, so
Bell's test (`examples/bell-chsh/`, deleted on 2026-09-17) on it stays below the CHSH
bound 2, where the quantum value is 2 sqrt 2: shared origin and no-signaling
it gives in the stated probes, and the excess correlation it cannot derive,
unless the field is bonded (`bonded-ray-field-v1`, the split of postulate 4:
a bounded registry answers the pair's joint outcome for both ends from one
number, with nothing physical in it, and S reaches the quantum value);
gathering a gravity train to
its catcher (gathered gravity, `examples/gathered-gravity/`, deleted on 2026-09-17)
focuses quanta, not a force law, so no flat rotation curve comes from it.
The `|p| / D` rule and every mixer are configured laws, measured to hold, not
derived. Exact sources and completed checks are in
[validation evidence](VALIDATION.md).

## Causal quantum source envelopes - 2026-09-13

The user's latest selection extends the preceding localized-source choice:
each wave mode may source an ordinary field with its local squared weight, and
weight changes or cancellation must travel through Nodes and Links with delay.
This maps Highlights sections 1.2.7, 4.7.1-4.7.7 and 10.3/10.6 to the explicit
causal source candidate (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17). The live document remains read-only.

`causal-contact-fields-v1` retains a bounded complex source envelope at each
participating ordinary Node, immutable definitions outside NodeState, finite
allowances and fixed packet/proposal slots. Actual contact creates the source;
successful local absorption creates one full-strength ordinary output and sends
terminal notices over physical Links. Existing field stock continues. Shared
origin status remains quantum bookkeeping and never controls remote ordinary
emission, response or delay. The older localized-only profile is unchanged.

After measurement the local source weights are retarded and may be unnormalized;
their sum is not conserved charge or proof of field/matter energy closure. The
candidate preserves one inventory owner and specifies separate source accounting,
phase-sensitive propagation, causal termination and unsupported combinations.
Its implementation owners and numerical acceptance expectations are linked from
the contract. Exact source, completed runs and review outcomes belong in
[validation evidence](VALIDATION.md); no pending test is represented here as a
passed result. This extension does not complete the broader unified-dynamics goal.

## Localized quantum contacts - 2026-09-13

Live Highlights was reconciled read-only. Its sections 1.2.7, 4.7.1-4.7.7 and
10.3/10.6 map to the localized contact candidate (`docs/LOCALIZED_QUANTUM_CONTACT.md`, deleted on 2026-09-17).
The later user selection explicitly chooses ordinary fields only at localized
events. This finite hybrid is an additional configured candidate, not a claim
that the project's separate goal of emergent unified dynamics is complete.

Actual local source contact creates an origin only at committed event time.
Finite coherent domains retain one configured inventory through number-preserving
operations; a complete local absorption instrument transfers it into one ordinary
record. Existing classical fields evolve causally. Quantum probabilities never
reconstruct or erase remote ordinary field stock. Definitions, implementation
owners, tests and configuration are linked in the candidate contract.

The separate predecessor list remains absent. Node state adds only a bounded
reservation token; six-entry origin banks and immutable event history retain their
owners. Common local field reactions preserve every coupled resident, including
third participants, and all alternatives validate before sampling. Unknown
momentum is explicit; no sharp momentum or physical energy is inferred from a
position record. Public snapshots serialize with event-backed commits and expose
possible support separately from localized charge.

The focused acceptance suite covers fifty-one numerical and failure cases, including
3:4 interference, exhaustive Born tickets, delayed ownership, external-field
exchange, finite emission, six periodic directions and unchanged unconditional
receiver statistics. The authoritative run/gate evidence belongs in
[validation](VALIDATION.md). Full quantum fields, unrestricted no-signalling,
exterior quantum escape and shared Node clock composition remain outside scope.
The live Google Doc was not changed. Its section 11 reports other unmerged
branch candidates; those results are not imported or claimed by this change.

## Quantum origin cells and event spacetime - 2026-09-13

Live Highlights was reread. Implementation
starts from `fb54f3306ce8172f5ed3f2d3a65eb03cb021a6b7`, integrating current main
`2c20d00094639263fbe387c0a62420dcef108285` with the prior Node-event work.

The user's later explicit contract replaces the separate per-stream predecessor
list. Sections 1.2.7 and 4.7.1-4.7.6 now map to
event spacetime (`docs/QUANTUM_EVENTS.md`, deleted on 2026-09-17) and
origin cells (`docs/WAVE_ORIGINS.md`, deleted on 2026-09-17): immutable events are the sole history, each
participating Node stores up to six origin IDs, and a direct origin status check
does not traverse a history. Current virtual-register heads remain separate
bounded state. One conditional terminal decision atomically resolves its selected
origins; peers prune their local references on their next native tick. Every v3
gate declares participating origins. Unarrived support cannot execute the gate;
suppression after resolution requires unchanged complete correlated density.
A retired instrument also needs an explicit `null_outcome` that is certain and
preserves that density. Unsafe suppression fails. One origin may describe several
disturbances; interaction lists accept one to six names, not a particle count.
Untagged gates and the older carrier bindings are rejected in
this profile. Continuing outcomes retain the conditional state and do not assign
sharp momentum after a position record. Origin bookkeeping does not grant an
ordinary remote field read.

Explicit matrices and exact joint state retain interference and correlation.
Component checkpoints preserve phases, origin identity and individual Link
readiness. `examples/quantum/event_paths.json` retains the four-Node coherent,
phase, record and checkpoint cases; the v3 origin contract specifies the new
local-capacity, contention, conditional-sampling and pruning acceptance checks.
The terminal policy stops future operations requiring its named origins; it does
so only through the guarded contract. The example instrument explicitly resets
occupation on its terminal branch; this is not a derived absorption or energy law.
Direct origin lookup is O(1); cancellation certification is separately counted
quantum-owner work, without an added physical observer or carrier-delay channel.
Check results require the exact tested tree and completed validation evidence.

This is a finite configured candidate. It does not establish spontaneous free
dynamics, a universal trigger or conservation law, general field composition,
full Focus, host O(1) evaluation or bounded total memory for infinite spacetime.
The live Google document was read only; its text was not changed by this
repository reconciliation.

## Quantum time-direction clarification - 2026-09-13

Highlights sections 1.2.7 and 4.7 distinguish direct origin relevance lookup
from deferred quantum evaluation. Neither is reverse physical-time computation.
Required stored dependencies and recorded constraints are collected as bounded
host work; their recipes evaluate forward from sources or exact checkpoints.
Earlier events and outcomes are not rewritten or resampled.

This terminology review uses merged main
`63983788140bc06d5e8f581e3609c0520c00f43b` and the then-reported
`Quantom -> Classic` run in [PR #91](https://github.com/Closer24/Universe24/pull/91),
head `49bcbc74c69a47814945efce8600edbc824ee04f`. PR #91 was open and unmerged
at review. Its `local-quantum-events-v3` candidate removes separate chronological
predecessor lists and `history(register)` traversal, while retaining immutable
events and quantum dependencies. Direct event-ID/status lookup is O(1); full
retained-state evaluation and cancellation certification are separate host work.
Source resolution adds a later write-once status without rewriting the source.

The PR reports `wave_origins.json` completing 5/5 ticks in 0.0123118 seconds:
one outcome draw, origin 3 resolved at tick 2 to record 13, peer references retired
at tick 3, and origin 4 still active. Three oracle calls include two cancellation
certifications. These are branch-reported results, not a new experiment in this
documentation task or proof of a universal quantum-to-classical limit.
See the quantum contract (`docs/QUANTUM_EVENTS.md`, deleted on 2026-09-17).
The Google Doc receives the same clarification in sections 1.2.7, 4.7.2 and 4.7.7.
No reaction law or evaluation algorithm changes in this correction.

## Latest synchronized snapshot - 2026-09-13

This is the repository implementation map for
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit),
not a second specification or an automatic live mirror. Both this map and the
Google Doc were reconciled against main
`cc042ce6c51a34775c292371538c5cd6acd4e423`, including merged
[PR #89](https://github.com/Closer24/Universe24/pull/89),
[PR #90](https://github.com/Closer24/Universe24/pull/90) and
[PR #92](https://github.com/Closer24/Universe24/pull/92).
The older entries below retain their historical source and validation scope;
their statements that the live document was not edited refer to those earlier tasks.

### Current implementation coverage

| Highlights sections | Implemented contract and limits | Repository owner |
| --- | --- | --- |
| 2.2.1-2.2.2 | Bounded integer physical inputs and intermediates; shared SI unit/constant registry prepares Scalar/Vector values outside physical stepping. Explicit conversion errors are separate from measurement uncertainty. Model time h is not Planck action. | [Reference units](REFERENCE_UNITS.md), [architecture](ARCHITECTURE.md) |
| 3.3.4, 3.5.5, 4.3.1 | Declared aggregation, indexed local participants, joint carrier/field proposals and complete-owner conserved readouts. Nonlinear balances use actual before/after state; labels do not supply physical laws. | [Node processor](NODE_VECTOR_PROCESSOR.md) |
| 4.4.1-4.4.2 | Explicit k*h Node execution and optional shared field/carrier cost-budget timing remain separate, incompatible modes. Waiting input has bounded destination ownership. | [Node processor](NODE_VECTOR_PROCESSOR.md), [shared clock](SPATIAL_COMPUTATION_DELAY.md) |
| 4.4.3 | Emission can read the Node's last committed work. Configured received-Port response exchanges momentum with a local field register; this is not derived gravity or physical energy. | [Computational response](COMPUTATIONAL_RESPONSE.md) |
| 6.5-6.7, 10.10 | Node-owned commits, immutable worker planning, deterministic barriers and bounded physical-owner memory have scoped tests. Total host memory and full-world work are separate costs. | [Architecture](ARCHITECTURE.md), [validation](VALIDATION.md) |
| 10.3.1 | Schema 2 localizes attenuation residue by default. Explicit dissipate retains the earlier loss policy. Stationary deposits remain owned inventory and are not sampled by local rules. | [Spatial fields](SPATIAL_FIELDS.md) |
| 10.3.2 | Scalar straight-ray transport retains heading and integer routing phase; ray_slots bounds resident capacity. Unsupported vector, octant-seed, field-rule, joint-interaction and alternative-clock combinations are rejected. | [Straight-ray contract](SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1), [ray tests](../tests/test_ray_field.py) |
| 10.9, 10.11 | Sourced particle reference data, explicit representation profiles, preflight, finite quantum events and read-only observers remain distinct from verified species dynamics. | [Entity catalog](ENTITY_CATALOG.md), [project status](PROJECT_STATUS.md) |

### Merged field changes and evidence

PR #90 adds `residue: localize`, selected when a schema 2 decay definition omits
the key. At completed interior arrival, the removed fraction becomes bounded
stationary stock at the receiving Node. It is included in inventory, not
dissipation; moving flux still diminishes. Explicit `residue: dissipate` selects
the earlier loss law. Open exit, signed components, source allowances and in-flight
ownership retain their separate accounting. The 40-tick finite-source run
accounted for 720 emitted units as deposits, with zero dissipation. Tests include
signed vectors, mixed residue policies and overflow rejection without partial
receipt. Neither a component ledger nor a stationary deposit establishes physical
field energy or a gravitational law.

PR #92 adds `transport: ray` under `isotropic-ray-field-v1`. A source sweeps
configured integer headings using its emission cursor. Each ray retains its
heading index, three integer routing accumulators and amount while moving over
adjacent Links. Matching heading and phase may merge; capacity exhaustion fails.
Ray fields currently reject vector payloads, octant seeds/weights, field rules,
spatial interactions, `node_execution` and `spatial_computation_delay`.

The published inverse-square probe (`examples/inverse-square/`, deleted on 2026-09-17) reports
a 41-cubed open world with 4,096 headings, 64 rays per tick and a 64-tick measurement
sweep. Finite fitted slopes are -2.25, -2.05 and -1.92 on the axis, face diagonal
and body diagonal. Angular-patch coefficients of variation are 6-8 percent over
72 patches at tested radii. This statistic is not a maximum error bound or exact
isotropy; individual nodes show greater variation. These are reported world/event
audit measurements of stock, not operational observer records or an independent
rerun in this documentation task. Scalar shell stock is not oriented surface
flux, and finite fits do not establish asymptotic scaling, mass coupling,
attraction, Newton's law or physical energy conservation.

### Unmerged amendments remain separate

The live document's section 11 contains branch-reported self-field policies,
carried allocation phase, scattering and collision results. Its cited
[PR #93](https://github.com/Closer24/Universe24/pull/93), head
`7149ec961df330b460dd3dc7262c4a98c5c17221`, was open and unmerged when checked
against the main commit above. The live section now states that scope explicitly.
Its findings are retained without being promoted to merged-main capabilities or
independently revalidated physical results. This sync does not merge PR #93.

The Google Doc update adds sections 6.7 and 10.3.1-10.3.2, reconciles the prior
decay accounting bullets, and labels section 11's branch scope. Existing Node,
unit, quantum and pending-hypothesis content is retained. Documentation-only
validation applies here; no simulator behavior or experiment input changes.

## Joint local reaction contract - 2026-09-13

The live source was reread.
Implementation base: `a7a0000e3005ae41b37639f5dcf76e56532be69f`.
Sections 3.1, 3.3 and 4.3 motivate the bounded property-selected
[joint Node reaction](NODE_VECTOR_PROCESSOR.md#local-rules). The user's explicit
reaction contract refines delayed execution: one group reads several carriers
and fields from one snapshot, and each frozen substep must still pass its
declared invariants and optional persistent condition before atomic commit.
Start triggers remain separate. The supplied register-rotation example checks
externally defined readouts; it does not derive physical species, energy laws or
quantum behavior. No live Highlights text was edited.

## Integer Node timing reconciliation - 2026-09-13

The live Highlights source was read again with modification timestamp
`2026-09-13T05:10:29.655Z`; integration started from main
`bb177121ec2efdc6c998a8290b9e7b09c7706c62`.
Sections 3.2, 3.3 and 4.3 motivate bounded generic local properties and rules.
The user's subsequent explicit h/k clarification selects the new
[Node profile](NODE_VECTOR_PROCESSOR.md): h is one hop; k is configured per
interaction, independently of operation cost. This supersedes the cost-derived
k description in section 10.6 for the opt-in profile only. Node vector width is
also explicitly generalized while world topology remains the current six-port
lattice. Section 1.3's distinction between assumptions, tested consequences and
emergence claims remains binding. The live document was not edited.

## Shared field computation cycle reconciliation - 2026-09-13

The live Highlights document was read against source base `1784acdd140f260c0fb5e568b2e28241df573fa2`.
Section 4.4 maps to the opt-in
[shared field/carrier cycle](SPATIAL_COMPUTATION_DELAY.md): C counts combined
local work once, one integer ceiling sets the entire cycle, proposals stay
frozen and later input belongs to the next cycle. Section 3.5.3 maps to
distinct waiting, input-buffer and transit owners in inventory.
The empty-input stream is implicit zero and allocates no event history.
This timing candidate does not establish nonlinear energy conservation,
gravity or quantum/spatial composition. The live document was not edited.

## Property coupling and local conservation reconciliation - 2026-09-13

The live Highlights document was read.
Source base: `ed65f829a6ddc797cafec1bf34156ca59bdcb7dd`. Sections 10.2, 10.5,
10.6 and 10.7 map to [property selection](PROPERTY_COUPLINGS.md), shared explicit
entity profiles and [passive local conservation](LOCAL_CONSERVATION.md).
The clarified user rule requires joint energy/momentum and actual boundary flux;
internal transfer is not an external source and checking cannot repair a law.
The audit detects violations after committed owner changes. Per-rule validation
no longer sets computation delay. Catalog metadata remains formula-free;
experiment profiles define their own quantities and elementary assignments.
No physical species law or universal proof follows. The live document was not edited.

## Coupled excitation candidate reconciliation - 2026-09-13

The [unit-excitation probe](COUPLED_EXCITATIONS.md) applies Highlights sections
3.2, 3.3, 3.5 and 4.3: independently owned field/internal states exchange through
local generic operations and a coordinated commit. A local capture gate retains
the input while a carrier computation is pending. This is a configured mechanism
under the unverified emergence hypothesis in sections 1.1.3 and 1.3.3, not a new
claim that electron/photon dynamics or quantum occupation have emerged.

The live document was read on 2026-09-13.
Source base: `6a2816526083c23069bf3b0f3fcb6a9dc5b17944`. The finite unit-state,
single-packet and held-receiver restrictions belong to this experiment. No core
law, catalog measurement or live Highlights text changes in this work.

## Configuration validation reconciliation - 2026-09-13

The [read-only preflight](CONFIGURATION_VALIDATION.md) implements explicit input
rejection and shared ownership under Highlights sections 4.5 and 10.7. It validates
configuration data without generating a physical state or inferring a law from
catalog measurements. Passing preflight remains distinct from the verified
behavior and physical hypotheses in sections 1.3 and 6.3. The live document was read on 2026-09-13.
Source base: `521b63567d186bab2fac982a1e1f9d0a592a73a5`. This is a host validation
and Skill workflow change; it adds no physical law and does not edit Highlights.


## Physical reference catalog reconciliation — 2026-09-12

The version 2 [entity catalog](ENTITY_CATALOG.md) expands descriptive coverage
without supplying physical evolution laws. Sourced measured properties remain
external comparison targets. Possible interactions describe channels and their
conditions; the simulator still needs explicit elementary operations and evidence
of emergence. The original 46 experiment profiles move to a separate file.

This implements the Highlights goals of deriving effective laws from local
operations, preserving generic field/type definitions and separating established
physics from hypotheses and verified results. The live document was read on 2026-09-12.
This repository update does not modify that document or claim additional derived
physics. Source base: `98b774ac3b02aa5cd350d5513b1e1fddbe3a2c81`.

## Historical implementation inventory

This versioned companion records the implementation inventory added to
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit).
Scope: main `09464b41b2c44a191aa2fcbdf4b036680bd646a5`.
The live document was updated on 2026-09-12 with section 10 below, preserving
all earlier paragraphs.
Highlights is the high-level specification; linked contracts define exact schemas
and rejection cases. Neither a prose document nor Git restores credentials or
expired outputs. Together, this map, the contracts and versioned initialization
files allow reconstruction without chat history.

This is a dated inventory for the revision above. Later native event programs,
local probes and internal path changes are described in [project status](PROJECT_STATUS.md),
[the documentation index](README.md) and [migration](MIGRATION.md). Preserve this
record as historical evidence rather than treating its omissions as current gaps.

This is a dated inventory for the revision recorded above. Later native event programs,
quantum entity support, Maxwell research examples, local probes and internal path changes
are described in [project status](PROJECT_STATUS.md), [the documentation index](README.md)
and [migration](MIGRATION.md). Preserve this record as historical evidence rather than
treating its omissions as current gaps.

## 10. Implemented entities and rules

### 10.1 World, nodes and links

- The active world is a bounded three-dimensional lattice with six directed
  neighbor ports: +X, -X, +Y, -Y, +Z, -Z.
- A node owns bounded resident records, field stock, residuals and pending local
  proposals. A link owns dispatched payloads until their fixed arrival tick.
- Periodic boundaries wrap all three coordinates. Open boundaries remove outgoing
  contents and record their escaped quantities; they do not reflect or reinsert them.
- Integer value, field, type, slot, expression and rule limits are validated.
  Exhaustion or overflow is an error, never silent deletion or unlimited allocation.
- Addresses route events; ordinary local laws cannot query distant state.

### 10.2 Field definitions and disturbance records

- A field declares its label, one or three components, units, scale, signedness,
  extensivity and whether its quantity is conserved. Labels select no physical law.
- Signed values and zero use positive integer payload codes internally. External
  JSON and diagnostics expose decoded values, including negative vector components.
- A disturbance type selects fields, defaults, local updates and transport policy.
  Seeds instantiate typed records at configured nodes.
- Transport may hold a record, move a whole record or distribute declared contents
  according to its policy. Direction, six routing weights and a scalar/vector
  payload are different concepts. No floating-point normalized vector is required.
- Rate accumulators and integer residuals preserve discrete allocations over time.
  They are physical bookkeeping, not accumulated computation debt.
- Mass, charge, momentum and emission in examples are configured quantities.
  The engine does not recognize electrons, protons or physical material classes.

### 10.3 Spatial fields and finite propagation

- Spatial fields separate immutable background from dynamic contributions.
  Background is observable locally and excluded from dynamic decay.
- Outward propagation uses bounded directional populations, including eight octant
  channels, and routes allocated amounts through six links. Six ports do not mean
  every field must contain six vector components.
- Scalar/vector payload sign is preserved on receipt; the receiving face does not
  automatically reverse it. Opposing directional populations can coexist.
- Emissions add configured field amounts. In schema 2, finite emission and reaction
  allowances prevent an inexhaustible source; dynamic fields have declared decay.
- Unsigned dynamic stock cannot decay below zero. Signed components retain their
  declared sign semantics; dissipation is tracked component by component.
- Conservation includes resident and in-transit stock, configured sources, recorded
  dissipation and escaped quantities. A balanced decay ledger does not mean the
  remaining physical inventory is conserved indefinitely.
- Self-field attribution is not implemented as a general source-identity filter.
  Arrival order is not a general proof of ownership after turning or periodic return.
  A ray field's `self_exclusion` subtracts a departing emitter's own one-link rays
  on arrival, from its own registers only.
- A ray is a whole amount on one lattice line; with `kerengonen` it carries a
  phase and its own advance, combines by phase where rays meet, and is absorbed
  whole or by its coherent share. Slits, mirrors and dissolving particles are
  emissions that carry the absorbed phase, heading or schedule on.

### 10.4 Local field rules and field groups

- Schema 1 optionally supports retained local fields alongside outward fields.
  Schema 2 rejects local field rules and joint spatial interactions; policies are
  distinct candidates and cannot be silently mixed.
- Field groups give related scalar/vector fields a logical label. Groups neither
  duplicate stock nor implement an electromagnetic law.
- Local rules read retained values and completed incoming values independently
  for all six travel channels. They may also read outgoing proposals from earlier
  rules in the same phase.
- Assignments replace retained dynamic stock or an explicitly selected outgoing
  payload. Background is not an assignable stock.
- Expressions, conditions, ordering and invariants are bounded configuration data.
  No arbitrary Python or hidden neighboring-node read is accepted.

### 10.5 Couplings, interactions and rotation

- Local updates and pair exchanges use generic integer expressions, coefficients
  and retained remainders. Sources must be declared.
- Atomic pair interactions evaluate coordinated assignments from a frozen pair and
  validate configured invariants before commit. A failed transaction cannot apply
  only one participant's change.
- Spatial exchange and exact quarter-turn response change a carried vector and
  account for the corresponding field reaction within the selected policy.
- Joint carrier/field interactions can assign carried and local/outgoing field
  quantities with declared invariants and guards. Validation and commit cover the
  participating state together, including delayed proposals and competing inputs.
- Momentum conservation requires the configured component balance across all
  participants. Preserving vector magnitude alone does not conserve momentum.
- The unequal-mass collision example supplies its elastic law and energy invariant
  in JSON; its successful outcome is not evidence that collision laws emerged.

### 10.6 Cost, timing and ownership

- Each declared model primitive has a configured positive cost. A local carrier
  cycle sums its work C and compares it with budget B.
- With link time tau, k = max(1, ceil(C/B)); additional wait is (k-1) tau and the
  subsequent link transit remains tau. Already dispatched arrivals never slow down.
- Pending proposals remain fixed while waiting; newly received inputs are handled
  according to the scheduling and transaction contract, never read from the future.
- Carrier and field phases have separate clocks and recorded costs. Do not infer
  that a spatial field named computation automatically measures all engine work.
- The optional cost-reporting field belongs to a held nonconserved scalar record.
  A separately emitted computation field requires an explicit configured law.
- Host elapsed time, visualization work and global diagnostics are not model costs.

### 10.7 Initialization, results and display

- Initialization selects model identity, schema, boundaries, capacities, timing,
  costs, field/type definitions, seeds, transport, emissions and applicable rules.
- The prepared simulator reads new JSON without compilation. Unknown definitions
  and incompatible policies fail explicitly.
- Normal runs save the input, event trace, final state and run metadata. They check
  combined quantity accounting at each completed tick and retain failure evidence.
- The runner can submit each active Node's immutable disturbance and spatial-field
  plan to isolated Python interpreters. A tick barrier and address-ordered commit
  preserve the serial result. Shared delayed field/carrier cycles use two planning
  barriers before their joint commit. Host worker counts never change modeled local cost.
- Visualization is opt-in. Playback and workspace consumers read recorded labels,
  values, groups, positions and transfers without changing physical state.
- Views distinguish resident records from fields and in-transit payloads, and
  display signed loss/escape accounting without confusing dissipation with failure.
- Saved configuration editing must preserve references when fields are renamed.
  Arbitrary labels and declaration order must not select hidden behavior.

### 10.8 Research scope and reproducibility

- Historical scalar, linked, balanced and causal-stream APIs remain explicitly
  named comparisons, not default laws of the generic Simulation.
- Quantum and Focus modules have separate research contracts. They do not authorize
  nonlocal ordinary fields or establish real quantum input, Maxwell equations,
  emergent gravity or a complete physical theory.
- Reproducible examples include approaching/parallel motion, spreading, configured
  elastic collision, three carriers with finite fields, and both boundary modes.
- Check renamed and reordered configurations, integer limits, residuals, local
  transaction failure, rotation, signed balances and generic result consumers.
- Run the recurring genericity procedure from the repository skill. Report exact
  source identity and coverage; finite passing tests do not prove universal behavior.
- Preserve source, specifications, skills and original configurations in Git.
  Generated results expire under the 24-hour policy; idle cleanup needs a scheduler.

## Relativity probes of 2026-09-14

Configuration-only probes in examples/relativity-probes (`examples/relativity-probes/`, deleted on 2026-09-17)
test what section 4.4's computational field yields when a mass emits it and
bodies exchange momentum with its delivered flux (the sign is supplied, as for
charge). The supplied couplings and transport/phase policies produce finite
attraction, velocity-scaling, lensing-like and delay observations. They do not
derive Newtonian gravity, relativity or dark matter. The open-3D control remains
pending. Forward replay and one configured collision restart are reproducible;
they do not prove reversal of arbitrary state. Lorentz dilation, accelerated
expansion and gravitating quantum matter have not emerged in these probes.
Findings, each a branch result and not a law:

- Under 4.4 and 7.2: the momentum coupling reproduces the Newtonian velocity law
  exactly (a body at c/2 deflects four times more than light at the same impact
  parameter) but not the 1/b law: the lattice far field along an axis column
  falls faster than 1/r² under `"straight"` allocation phases (b = 3/7 ratio 18
  instead of 2.33). With the mass emitting straight rays
  (`isotropic-ray-field-v1`, headings spread over the sphere every tick) the
  ratio falls to 5.6 for light and 4.7 for the slow body, symmetric on both
  sides; the remainder is ray quantization, not axis structure.
- Under 4.4: with the load defined as the stock present at a node, the source
  node's own emission is its own load, so a strong source throttles itself and
  the far field never forms under the shared clock. The directional delay does
  not have this problem. A load definition that excludes a node's own emission
  is an open design choice.
- Under 5 and the local observer: no kinematic time dilation. Twin clocks agree
  at every speed under any budget above the moving cycle's cost; a tighter
  budget slows the traveller linearly in moves, not as √(1−v²).
- Under 7.2 (cosmology): four masses launched outward under the momentum
  coupling recollapse at every speed up to c at emission 24000 — the escape
  speed of the configuration exceeds the link speed — so expansion is only an
  initial condition and no repulsive term exists. A light train past a mass
  whose emission grows each cycle arrives late and stretched (mean spacing 2.7
  per link-tick, z ≈ 1.7) under the directional delay: a distance-redshift
  relation from delay growth without recession, quantized in bunches. In a
  closed (periodic) universe the field never leaves, so a constant source
  makes the load grow with the age of the universe: with a ray computation
  field a unit-spaced light train stretches to z ≈ 9 within one lap (first
  seven bodies unshifted, then 6, 60, 12, 26-tick gaps) — a distance-
  proportional redshift from closure alone, whose lattice form is stepwise.
  Under `straight` phases the mass's axis ray stalls the train at one column
  and under `rotate` the wrapped Manhattan field piles up at the antipode;
  neither is a uniform load.
- Under 4.4 and the Kerengonen field: a two-lamp interferometer beside a mass
  is unchanged at every screen Node under the fixed field clock (gravity
  invisible to interference); with the opt-in `ray_delay` the delayed rows
  gain quanta (decoherence, 6176 → 6404); with `ray_phase_per_tick` as well
  they darken (6176 → 5636, y = 10 from 552 to 211): the waits carry phase and
  the fringe shifts in whole steps — the gravitational-phase (COW) signature,
  present only when a waiting interval counts as phase.
- Under 7 (postulates) and 4.7: the eight-tick seeded quantum example replays
  the same exposed snapshots from its logged ticket or original seed. Earlier
  snapshots are reached by executing forward from the original configuration.
  The equal-mass collision example, restarted after 12 ticks with negated
  momenta, returns the initial positions and reversed momenta after 12 more
  ticks. This does not prove inversion of retained queues, counters or arbitrary
  fields. Outward transport and truncated absorption have no tested inverse.
- Under 4.7 and 10.6: a localized quantum domain hops one Link per world tick
  regardless of the local computation load, while a classical carrier on the
  same path is delayed 6 → 13 ticks. The quantum gate clock does not read the
  node's delay; this is an equivalence-principle gap of the profile, not
  configurable.

## Proposed amendments of 2026-09-13

Status: applied to the live Google document on 2026-09-13 as an appended
section 11 with subsections 11.1 to 11.7, each naming the section it amends;
earlier paragraphs were preserved. Section 10 above is unchanged so that it
remains the recorded snapshot. Each bullet below is written in the document's style and names the
heading it belongs under. Evidence: `examples/collisions`, `examples/charged-pair`,
`tests/test_field_phase_first.py` (deleted on 2026-09-17), `tests/test_arrival_port_blind.py` (deleted on 2026-09-17) and
`tests/test_rotation_self_interaction.py` (deleted on 2026-09-17).

Under 3.3.1 Discrete directional-flux conservation:

- An indivisible unit must carry its own allocation phase; a node-owned phase
  decides its direction by lattice axis order.
- Observed: without decay, every far-field unit follows the first axis weight,
  so the far field is rays, not a shell. Status: open defect, not a law.
- Repository status after the live edit: `allocation_phase` carries each
  portion's phase and merges phases on arrival. `"straight"` (default) keeps
  a lone unit on its axis so rays move at link speed while the axes share
  the units; `"rotate"` cycles the axes and is Manhattan-isotropic but slows
  axial propagation to a third; `"node"` retains the legacy behavior.
  See [spatial fields](SPATIAL_FIELDS.md#carried-allocation-phases).
  Reported to the live document on 2026-09-14 as two bullets under 11.8
  (the `allocation_phase` modes and PR #93 head `8f04758`).

Under 3.5.2 Local collisions:

- Status: the configured elastic, inelastic, three-body and rotated-axis
  examples pass the momentum, mass and energy checks; a nonintegral outcome
  faults instead of rounding. This verifies the supplied law, not emergence.

Under 4.2 Update cycle:

- The order of the field phase relative to the carrier sample within one
  interval is a declared model choice; see 10.3.

Under 5.2 Fixed link travel:

- Matter and field share the link time; whether the field phase precedes the
  carrier sample inside an interval is declared, not implied by c.

Under 7.2 Attraction between masses:

- Verified for charge, not mass: a configured charge-times-flux exchange gives
  attraction of unlike and repulsion of like charges for held and free pairs.
  The sign is supplied in initialization, so this tests the mechanism, not
  emergence.

Under 10.3 Spatial fields and finite propagation, replacing the self-field
bullet:

- Self-field attribution is not implemented as a source-identity filter.
- Under one shared clock a source and its departure-interval emission cross
  one link together; a value-driven response therefore reads its own field
  after every hop and an isolated charge accelerates itself.
- Two declared policies remove this without identity: field-phase-first
  delivery keeps own field one link ahead on every free-space path;
  arrival-port-blind sampling keeps the default clock and ignores the entry
  travel port for the arrival interval, so straight paths are self-blind
  while maximum-speed turns still coarrive.
- The flux-driven rotation law is self-blind on straight paths by geometry and
  turns at maximum-speed corners.
- Periodic return remains outside every guarantee. None of these is a derived
  self-force law.

Under 10.5 Couplings, interactions and rotation:

- The generic value exchange was observed to accelerate an isolated straight
  emitter by its own coarriving packet; that baseline is retained as a test.

## Coverage map

### Local observer reconciliation

For the [local reception observer](LOCAL_OBSERVER.md), Highlights was reread on 2026-09-12.
Sections 2.1, 4.6, 5.1-5.2 and 10.7 require discrete connected nodes, causal
delivery and read-only output. The probe records completed local inputs and
preserves exact playback prefixes. The user's event-time interpretation
motivates a local cycle counter; perceived time and a derived spacetime remain
hypotheses. The live document itself was not edited by this implementation.

### Directional-wave candidate reconciliation

The live Highlights document was read on 2026-09-12.
The [directional-wave contract](DIRECTIONAL_WAVE.md) is a new explicit candidate
under sections 3.3, 3.3.2, 3.5, 10.4 and 10.5. Six transverse directional modes,
bounded vector operations and local encounter guards preserve the declared
U=sum of squared mode amplitudes and P=sum of their direction-weighted energies,
with resident and in-flight ownership counted once. Same-law cubic rotations and
periodic return are tested. E/B are derived readouts, not duplicated stock.

The candidate demonstrates conditional polarization interaction and declared
balances. It does not promote the emergence hypothesis to a verified physical
law, or claim Maxwell dynamics, charge response or trajectory scattering.
The [configuration Skill](../skills/simulation-configuration/SKILL.md) supports
section 10.7 with reusable input definitions and separate recording/display controls.
Its commands and template are executable evidence; technical workflow remains in
the repository. This reconciliation does not edit the live Google document.

### Local Maxwell research reconciliation

For the configuration-only Maxwell experiment (`examples/maxwell/`, deleted on 2026-09-17),
Highlights was reread on 2026-09-12.
Sections 1.3.3, 1.3.4 and 10.4 are reconciled as follows: the existing generic
local field interface can express a transverse reflection and one-link
streaming hypothesis without adding an engine field equation. Conditional
leading vacuum dynamics and small-space mode frequencies agree with the
independent forecast. Exact centered Gauss conservation, complete macroscopic
energy, physical light speed and indefinite bounded-integer mixing remain gaps.
The experiment does not promote full electromagnetic emergence to a verified
result. This entry records repository coverage; it does not claim a live
Highlights edit or replace the earlier revision record above.

### Self-field ordering reconciliation

Highlights was read again on 2026-09-13 through the Drive connector for
sections 1.1.1, 3.3.1, 3.5.2, 3.5.4, 4.2, 5.2, 10.3 and 10.5. Section 10.3
states that self-field attribution is not implemented as a general
source-identity filter; that remains true. The generic engine's default clock
delivers a carrier and its departure-interval emission through the same link
together, so a value-driven exchange read one own packet after every hop and
an isolated moving charge violated POSTULATES section 7. Two opt-in policies
now exist without source identity: `field_phase_first` orders the field phase
before carrier sampling, matching the causal stream candidate, so own field is
at least one link ahead on every free-space path; `arrival_port_blind` keeps
the default clock and excludes the arrival travel port from an arriving
carrier's single sample, so straight paths are self-blind while maximum-speed
corners still coarrive. Both pass isolated-source and external-source controls
in `tests/test_field_phase_first.py` (deleted on 2026-09-17), `tests/test_arrival_port_blind.py` (deleted on 2026-09-17) and
`tests/test_rotation_self_interaction.py` (deleted on 2026-09-17). The same probes recorded that a
decay-free schema 1 pulse keeps every unit on the Manhattan shell but that
indivisible far-field units all follow the first axis weight, which is a
separate open finding. This reconciliation edits repository contracts only;
the live Google document was not edited.

### Source contracts and evidence

| Highlights section | Authoritative contract / implementation owner | Evidence owner |
| --- | --- | --- |
| 10.1 | [Disturbances](DISTURBANCES.md), core/topology.py | test_boundary_configuration.py and architecture tests (test_open_boundaries.py deleted on 2026-09-17) |
| 10.2 | [Disturbances](DISTURBANCES.md), core/disturbance_state.py | test_initialization.py and test_disturbance_engine.py (test_generic_identity.py deleted on 2026-09-17) |
| 10.3 | [Spatial fields](SPATIAL_FIELDS.md), fields/spatial.py, fields/spatial_decay.py | finite-field and spatial transport tests |
| 10.4 | [Local field rules](LOCAL_FIELD_RULES.md), fields/local_field_rules.py | test_local_field_rules.py |
| 10.5 | [Spatial couplings](SPATIAL_COUPLINGS.md), fields/spatial_interactions.py | test_spatial_interactions.py (test_atomic_interactions.py deleted on 2026-09-17) |
| 10.6 | [Definitions](../SIMULATOR_DEFINITIONS.md), core/disturbance_engine.py, core/spatial_engine.py | disturbance and spatial scheduling tests |
| 10.7 | [Workspace](WORKSPACE.md), runner.py, diagnostics/disturbance_render.py, ui_assets | test_disturbance_application.py (test_workspace_integration.py and test_recorded_movie.py deleted on 2026-09-17) |
| 10.8 | [Architecture](ARCHITECTURE.md), [recovery](RECOVERY.md), [regression skill](../skills/regression-check/SKILL.md) | [test expectations](TEST_EXPECTATIONS.md), [validation](VALIDATION.md) |
