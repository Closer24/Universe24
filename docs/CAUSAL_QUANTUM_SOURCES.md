# Causal quantum source candidate

`causal-contact-fields-v1` is an explicit finite extension of the
[localized contact candidate](LOCALIZED_QUANTUM_CONTACT.md). A delocalized mode
can emit an ordinary field from its locally retained complex source envelope.
Weight changes and cancellation reach another Node only through physical Links
and its local computation delay. The older `localized-contact-quantum-v1`
selection continues to emit ordinary fields only at localized events.

## Local law and ownership

This page specifies the one-shot profile. The separately selected
[recurrent extension](RECURRENT_QUANTUM_CONTACT.md) adds outcome effects and
finite isolated envelope generations, preserving the original selection.

| Part | Contract |
| --- | --- |
| Law | Multiply the configured full emission by the squared magnitude of the local source envelope. Evolve its complex amplitude through configured number-preserving neighbor operations. |
| Inputs | The Node's retained amplitude, frozen neighbor amplitudes actually received through Links, local source allowances and the immutable initialization definitions. Neither conditional quantum queries nor shared origin status supply ordinary source inputs. |
| Evolving state | One envelope per participating Node: bounded complex numerator and positive denominator, origin identity, generation, terminal marker, one pending gate, one received gate input, one pending terminal notice and one pending emission. Twelve fixed output slots hold six amplitude packets and six terminal packets. |
| Parameters | The contact profile's disjoint finite mode domains, source/capture definitions and phases; generic field emission rules, finite budgets, operation tariffs, normal budget and Link transit. |
| Derived values | The local squared weight and proposed field injection. They are neither copied charge inventory nor a query of the globally conditioned Born distribution. |
| Outputs | Delayed local amplitude commits, finite ordinary field deposits and causal terminal packets. Localized capture installs one full-strength ordinary source and terminates only the colocated envelope immediately. |
| Consistency | Validate bounded inputs and proposals before publication; preserve signed fractional emission residue across changing denominators; keep previously emitted field stock and its source accounting. The optional [null notices](#opt-in-causal-null-notices) add one rational weight scale per Node. |
| Acceptance | Phase-sensitive splitting/recombination, real Link fronts, delayed terminal propagation, remote-prefix equality, single inventory ownership, finite allowances, stale-output rejection and explicit unsupported-input rejection. |

The source envelope is actual locally evolved state in this candidate. It is
attached to the ordinary Node; it is not a replay, a per-source reconstruction of
the entire field or a cached global quantum query. Ordinary response reads only
the local field stock already produced or delivered through the existing spatial
owner. Event identities establish provenance without granting ancestor reads.

The exact finite quantum owner still supplies the configured local absorption
lottery and counts one coherent inventory until a successful capture. Its origin
retirement and conditional state are separate from the locally propagated source
envelopes. Globally retired quantum support cannot turn off a remote ordinary
emitter or select that emitter's clock.

## Amplitudes and delayed operations

An amplitude is `(real + i*imag)/denominator`, using bounded integer registers
and bounded intermediates. Its local weight is
`(real*real + imag*imag)/(denominator*denominator)`. Phase is retained even though
the emission rate depends on the squared magnitude.

For a number-preserving one-mode or two-mode matrix, divide its one-excitation
block by its nonzero complex vacuum coefficient. This removes the common vacuum
phase and scale; rational complex arithmetic suffices even when the matrix's
implicit normalization scale has no integer square root. No global norm or
remote amplitude sum is needed. Invalid dimensions, occupation changes, numeric
overflow and local weights above one are rejected, not normalized away.

Each phase freezes the endpoint inputs. A two-mode endpoint sends its frozen
amplitude through one Link and computes its output only after receiving the
neighbor's matching epoch. The one-shot origin identity must agree. A local
preparation or capture invalidates an older frozen local gate output. A null
result clears the current source amplitude but retains the complete snapshot of
an already started gate. Rewriting just one endpoint's frozen operand could
increase the source norm. A retired Node cannot be reactivated by a stale packet.

Let `L` be the configured Link time. The existing integer cycle rule derives
`send_delay` and `compute_delay` from the selected tariffs and normal budget.
The common phase commit offset is `send_delay + L + compute_delay`; its repeating
period adds one further `L`. A one-mode operation waits for this same phase
boundary. The finite quantum gate schedule is padded to these boundaries as
well. Physical Link transit remains `L`; the phase period is not a changed value
of the propagation speed. Receive, evaluate, update, send and commit work is
charged separately from the quantum owner's host evaluation.
Gate, contact and source-emission cycles retain their declared separate clocks.
Their reported operation costs do not model shared aggregate CPU contention or
prove that concurrent components exhaust one common Node execution budget.

## Actual interaction and causal termination

An actual local source contact prepares a unit envelope at the same delayed
commit that transfers the ordinary record into the quantum domain. Merely
planning that contact does not move its inventory or create its envelope.

A successful configured local absorption produces one held ordinary output at
full strength. At that same commit the local envelope becomes zero and ends;
its pending emission is canceled. A terminal notice leaves through the declared
neighbor Ports. Each receiving Node waits its local control delay, terminates
its own envelope, and forwards the notice through its own Links. A terminal
notice can arrive before an amplitude and still prevents later resurrection.
Duplicate notices are inspected and charged without restarting termination.

A null outcome zeros only the local envelope and cancels its pending emission.
It does not terminate the origin or remotely renormalize the other envelopes.
An already started gate can subsequently repopulate that Node from its frozen
inputs, including the old local input; the null result does not rewrite a packet
or calculation already in flight. This is delayed ordinary source evolution,
not the quantum owner's conditioned probability after the null result.
Coherent gates, probability inspection and ordinary overlap alone are not
automatic absorption instruments. Other interaction laws require explicit
configuration and their own physical contract.

After measurement these source weights are a **retarded, unnormalized local
approximation**. They need not equal globally conditioned Born probabilities,
and their sum need not be one while cancellation propagates or after a null
result. After a null result the local source approximation can remain unnormalized
until later localization; there is no deferred global normalization operation. The
localized winner has full strength because it is an actual ordinary output,
while remote envelope sources can continue until their causal notices commit.

The conserved configured charge or mass retains exactly one ordinary/quantum
owner under the contact contract. Summing source weights is not a charge audit.
Ordinary injection, remaining field stock, dissipation and escape retain their
separate spatial accounting. Previously emitted packets are never swept or
erased by origin retirement. This hybrid does not establish field/matter energy
closure, quantum electromagnetism or a universal classical limit.

## Opt-in causal null notices

`"null_notices": true` on the contact program object selects an explicit
extension of the null rule above. It requires `causal-contact-fields-v1` and
changes nothing when absent.

| Part | Contract |
| --- | --- |
| Law | At a null result on a Node whose scaled local weight is `p < 1`, the Node multiplies its own weight scale by `1/(1-p)` and sends that rational factor through its domain Ports as a null notice. A receiving Node waits its local control delay, multiplies its own scale by the delivered factor, and forwards the notice through its other Ports. |
| Inputs | Only the deciding Node's own amplitude and scale, and factors actually delivered through Links. No Node reads the conditional quantum state or another Node's weight. |
| State | One `EnvelopeScale` per Node, a rational of at least one; six pending-notice slots, one per Port; a fixed bank of the six most recently applied notice identities; six additional output slots for notices. |
| Effect | Ordinary emission is full strength times the local squared weight times the scale, clipped at one. Amplitudes, gates and the quantum owner are unchanged. |
| Limits | A vacuum null (`p = 0`) and a certain occupation (`p = 1`) send nothing. A notice identity already in the bank is ignored; a Node that has retired ignores notices. A Node holds at most one pending notice per Port. |
| Acceptance | Factor 25/9 after a 16/25 null; one-Link and two-Link arrival ticks; forwarding away from the arrival Port; duplicate and retired rejection; the fixed bank; exact 9/16 emission after the next gate; unchanged behavior without the option. |

For one excitation in the domain the delivered factor equals the exact
conditional renormalization: after all notices have arrived, every scaled
weight equals the quantum owner's conditional Born weight for that Node. The
[two-arm experiment](../examples/quantum/causal_interference.md) records this:
the source recovers to 25 of 25 units one Link after an arm null, and the next
gate emits 9 and 16, the conditional weights, instead of 3 and 5.

The approximation remains causal. Between the null and the notice's arrival a
remote Node still emits its stale weight, and a second null decided before an
earlier notice reached the deciding Node computes its factor from a stale
scale. The scale is a multiplier of squared weights, so no square root enters;
two-mode gates combine amplitudes, not scales, and a gate between a Node that
has received a notice and one that has not is the residual error of this
candidate. For several excitations or entangled registers the local factor is
the marginal renormalization only, and the departure from conditional weights
is not removed. The clip at one and the fixed notice bank are explicit bounds,
not physical claims.

## Opt-in field-dependent phase

A one-mode propagation operation may declare `"field_phase"` instead of
`"matrix"`. It requires `causal-contact-fields-v1` and changes nothing when
absent. This is the candidate's only action of the classical field on the
wave: a local phase, no amplitude change and no transfer to the field.

| Part | Contract |
| --- | --- |
| Law | At the gate's schedule tick the Node reads its own value of one configured spatial field component, present at the start of that cycle. The exponent is that value divided by `divisor` toward zero. The gate is `diag(vacuum^n, unit^n)` for `n >= 0`; for `n < 0`, both coefficients are conjugated and raised to `|n|`. Thus the relative phase is `(unit / vacuum)^n` for either sign. |
| Inputs | The Node's own local field readout, the configured `vacuum` and `unit` Gaussian integers of equal nonzero norm, `divisor`, `component` and `max_exponent` (at most twelve). No remote value and no quantum query. |
| State | Nothing evolving is added to NodeState. The `2 * max_exponent + 1` matrices are fixed at initialization; the chosen matrix index enters the ordinary pending gate, and the same unitary is recorded for the quantum owner's recipe of that epoch. |
| Effect | Both owners apply the identical matrix: the envelope through its delayed one-mode gate, the quantum owner in the propagation phase of the same epoch. A phase read is charged one `read` tariff on the gate start. |
| Limits | An exponent beyond `max_exponent` stops the run. A field phase requires the spatial owner at schedule time. The field is read, never changed, by the gate. Rational phase angles only: `unit / vacuum` such as `(3 + 4i) / 5`. |
| Acceptance | Identity at exponent zero, conjugate for negative values, exact table; parser rejections; exponent 0, 1 and 2 from coil fields 0/200, 400 and 800 with recorded output weights `[12745, 2880]` and `[160225, 230400]`; a coil on the far side of the source selects no phase; the envelope port weight `2549/3125` after the shifted recombination. |

The [two-arm experiment](../examples/quantum/causal_interference.md) records the
fringe shift: an external `vector_potential` field next to the M arm moves the
output capture probability from 0 to `576/3125` and `9216/15625` for exponents
one and two, while the same field placed beside the source arm's other side
leaves the fringe unchanged. This is an Aharonov-Bohm-like local coupling in
integer form. It does not make the field react to the wave, does not conserve
a field-plus-matter quantity and does not select the coupling constant; the
`unit / vacuum` ratio is configured data.

Negative values preserve the inverse of the relative phase even when `vacuum`
is complex. Multiplying both coefficients by the same phase cannot change
interference probabilities. Regression controls exercise exponents -3 through 3,
positive/negative inverse composition in both orders, and a native negative-coil
run. The equivalent pairs `(5, 3+4i)` and `(5i, -4+3i)` both give capture
probability `576/3125` and source envelope weight `2549/3125` at exponent -1.

## Opt-in funded envelope emission

An emission rule selecting the source type may declare `"source": false`. The
emitted field is then paid from the wave's own conserved stock of the field
with the same name, and the runner records no external injection for it. It
requires `causal-contact-fields-v1`, the emitting and output types must own the
field, and the source stock must cover every mode's finite `budget`, so that no
local cap can overdraw the wave. Nothing changes when `source` stays true.

| Part | Contract |
| --- | --- |
| Law | Each envelope emission is booked as an internal transfer from the wave's stock into the field. The stock is the conserved value the source record carried into the quantum domain; the quantum owner holds it as it holds charge and mass, less what the modes have paid. Per-mode budgets remain the only local bound on emission. |
| Inputs | The local envelope weight and allowance as before. No mode reads the remaining stock; the parse-time cap `modes x budget <= stock` guarantees it is never exceeded. |
| Effect | `totals()` stays constant and `source_totals()` stays zero while the wave is live. At localization the output record receives the unspent stock and continues paying its own ordinary funded emission from it. Stock the ordinary record spent before delocalizing counts as already paid. |
| Residual | An envelope emission committed after the domain localized elsewhere has no payer left: it is booked as an explicit external source and reported as `after_capture`. It is the causal residual of the terminal notice's Link transit. |
| Report | `funded_emission` per domain: `paid` and `after_capture` per field; `quantum_inventory` shows the stock less what was paid. |
| Acceptance | Parser: ownership, causal model, budget coverage. Runtime: constant totals with zero sources, inventory equal to stock minus paid, the localized winner holding stock minus paid and paying 25 per tick afterwards, the post-capture residual equal to the recorded sources, balanced spatial accounting, unchanged default profile. |

For the [two-arm experiment](../examples/quantum/causal_interference.md) at
`phi = pi` with stock 3000 and budget 1000 per mode, the wave pays 211 units
into the field over fourteen ticks with no capture, the totals stay at 3000 and
the runner's strict conservation flag holds. With a capture at tick 7 the
localized record receives the unspent stock, keeps paying 25 per tick, and the
source Node's one retarded emission after the capture is the entire external
residual. This is energy closure between the wave and its classical field under
a bookkeeping that the quantum owner holds centrally, as it does the charge; it
is not a local transport of stock between modes, and the field still does not
act back on the stock.

## Configuration, implementation and acceptance

The [two-arm interference experiment](../examples/quantum/causal_interference.md)
measures phase-dependent capture, classical emission after recombination,
which-path decoherence and the size of the retarded-source approximation.
The [coupling summary](QUANTUM_CLASSICAL_COUPLING.md) places these results
against the literature.

Select `event_program.model: "causal-contact-fields-v1"` with the existing contact
schema. [causal_charge.json](../examples/quantum/causal_charge.json) is the complete
runner example:

```sh
python -m event_universe --init examples/quantum/causal_charge.json --output artifacts/causal-charge
```

Each of the at most thirty distinct mode addresses belongs to one finite,
connected, disjoint domain. Connectivity follows the configured six-Port topology,
including periodic seams in all axes. Terminal messages travel that domain graph;
there are no implicit exterior quantum modes. Ordinary open-boundary field and
carrier exit accounting remains unchanged.

Spatial emission definitions are required. Each mode owns the selected output
type's finite configured emission allowances; these never refill on propagation,
null results or repeated visits. Fractional residue stays local until used,
exhausted or canceled under the local source lifecycle. The total allowed source
injection across modes is distinct from the single conserved carrier inventory.
Ray transport, shared field-delay clocks, Node execution and the passive
classical-only conservation audit are outside this profile. It does not add
reciprocal field action on coherent amplitudes.

`integration/contact_program.py` validates the selection and
`integration/causal_contact_runtime.py` composes the owners. Formula-free state,
packets, local transitions and source proposals belong to the `core/source_*`
modules. `fields/source_envelope.py` owns bounded amplitude and weighted-emission
arithmetic; `fields/source_emission.py` composes the existing generic spatial
source primitives. Immutable laws remain outside NodeState. Source events use
the write-only `NodeEvents` interface; saved reports and playback are read-only.
Ordinary runs remain headless unless visualization is explicitly requested.

The arithmetic acceptance uses a 3:4 mixer: a unit input gives weights `9/25`
and `16/25`, and the inverse recombines it to one. A configured signed full
source of `-25` therefore requests `-9` and `-16`. Integration must compare
ordinary source, field and cost prefixes with and without a distant detector
before causal delivery, and exercise delayed capture, finite allowances,
six-axis periodic Links and no resurrection. These are required numerical
expectations; completed checks and the exact tested source belong in
[validation evidence](VALIDATION.md). `test_source_envelope.py` owns arithmetic
acceptance and `test_causal_contact_fields.py` owns the integrated candidate,
with coverage in
[test expectations](TEST_EXPECTATIONS.md#causal-quantum-sources).

The [many-contact experiment](../examples/quantum/many_contacts.md) exercises six
simultaneous one-shot domains and 1,200 captures across 200 independent trials.
It records the distinction between local captures, retarded ordinary fields and
the unsupported next step of repeated hopping after capture.
