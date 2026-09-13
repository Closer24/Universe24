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
| Consistency | Validate bounded inputs and proposals before publication; preserve signed fractional emission residue across changing denominators; keep previously emitted field stock and its source accounting. |
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

## Configuration, implementation and acceptance

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
