# Recurrent local quantum contact candidate

`recurrent-contact-fields-v1` extends the causal contact profile explicitly.
Existing profiles keep their one-shot contracts. Names remain configuration data.

| Part | Contract |
| --- | --- |
| Law | A complete configured local instrument selects an outcome and its conditional state. A certain outcome consumes no random ticket. |
| Inputs | Resident source/partner or detector, explicit validity scalar, configured matrices and the quantum owner's current conditional state. Ordinary sources use only their retained envelopes and delivered packets. |
| State | At most six preallocated envelope generations per participating Node, each with its own fixed pending and Port banks. Ordinary records, reserved slots and immutable event-space origins retain their existing owners. |
| Parameters | Explicit `max_generations` in 1..6; finite disjoint mode domains; outcome objects containing `effect`, `matrix` and optional localized `output`; finite per-generation emission allowances. |
| Outputs | Source `localized` retains its existing ordinary record; source `new_wave` transfers it into quantum occupation. Capture `null` observes vacuum; `continue` retains the origin; `localized` transfers occupation to a held record; `new_wave` resolves the old origin and creates a fresh origin at the same local event. |
| Consistency | The semantic quantum owner enforces matrix occupation support, complete instruments, domain vacuum before source preparation and single inventory ownership. Capacity and ordinary alternatives are checked before drawing. |
| Acceptance | Exact branch weights, deterministic no-draw cases, repeated local origins, delayed ownership, stale-generation isolation, finite emission, renamed fields and explicit exhaustion. |

Source outcomes replace `preparation`; capture outcomes replace `instrument`.
Source `register_indices` optionally extends the declared source contact locations.
Each outcome's matrix and effect are inseparable. A source localized outcome does
not replace its original record or refill its emission bookkeeping. Capture
localized output defaults to the domain's existing output template; every output
must preserve all declared conserved components and unknown momentum.

Source instruments act on a vacuum mode: localized branches are diagonal;
new-wave branches exchange vacuum and occupation. Capture null has support only
on `|0><0|`; continue/new-wave only on `|1><1|`; localized only on `|0><1|`.
Capture requires its explicit null outcome at index zero. No arbitrary overlap,
zero momentum or missing data generates an additional unconfigured lottery.

New-wave outcomes are local records followed by coherent continuation; they do
not install a duplicate ordinary carrier or assign sharp momentum. Source
preparation requires a local encounter and a fully vacuum domain. The old origin
remains immutable and resolved in event spacetime. Generation exhaustion is an
explicit error before sampling an applicable new-wave result, never a replacement
outcome or silent loss. A possible new-wave branch requires capacity even if a
different result would be selected; a certain vacuum null does not consume it.
New origin creation is atomic with the quantum result and old-origin resolution.
Reading or recommitting that result returns its original identity, even after
later absorption; it cannot create another wave. Event, decision and amplitude
budgets remain finite. A retained source pair may encounter again on a later
local cycle; each attempt uses the current complete instrument without refilling
the original record's allowance or fractional residue.

Each generation owns separate ordinary envelopes. Old cancellation continues
through its old generation's Links while a fresh unit envelope begins only at
the actual local new-wave event. All generation gate clocks run from configured
time, including vacuum; remote quantum status never starts or stops them.
Previously emitted field stock continues under its existing decay/escape law.

For emission, every Node selects generation `tick modulo max_generations`.
Selection is independent of activity and outcome. A ready pending emission waits
at most G-1 further ticks for its turn; this queue delay does not change Link
transit time. Pending amounts stay frozen and are deposited into current local
field stock. A local null cancels pending emission in every nonretired local bank;
a local terminal result cancels its old bank. A received terminal immediately
makes that bank's pending emission ineligible; the pending object may be discarded
at its next scheduled emission turn.
Each bank's allowance is consumed once and never refilled. The finite lifetime
envelope allowance is at most G times the sum of configured per-mode allowances;
ordinary localized source allowances are separately finite and accounted.

A continue result updates the exact conditional quantum state but leaves the
ordinary retarded envelope unchanged. A null clears all nonretired envelopes at
that local Node, without selecting a bank from shared quantum progress.
Localized/new-wave results terminate the old local envelope and send causal
notices. New-wave additionally starts a distinct local unit envelope. Retarded
weights need not equal globally conditioned Born probabilities. Inventory,
ordinary field injection and source weights remain separate quantities.

This extension supplies configured finite outcome/lifecycle mechanics, not a
derived Hamiltonian, reciprocal field action on amplitudes, physical energy
closure, unrestricted many-body collisions or parallel Node execution.

## Implementation and evidence

The one-shot causal profile's `null_notices: true` and `field_phase` operations
are not composed with recurrent generation banks. Selecting either in this
profile is rejected during preflight; an explicit `null_notices: false` retains
the existing behavior. Generation-specific renormalization and dynamic gate
selection require separate ownership and timing evidence before admission.

[Contact parsing](../src/event_universe/integration/contact_program.py) owns the
strict schema. [Quantum support checks](../src/event_universe/quantum/contact_outcomes.py)
and the [event network](../src/event_universe/quantum/event_network.py) own complete
instruments and atomic conditional results. The
[recurrent resolver](../src/event_universe/integration/recurrent_contact_runtime.py)
composes ordinary inventory with preallocated causal source banks.

[Outcome acceptance](../tests/test_recurrent_quantum_contact.py) enumerates exact
ticket weights and tests finite inventory, generic labels, output templates and
the headless runner. [Locality regressions](../tests/test_recurrent_contact_locality.py)
compare remote prefixes, reject duplicate occupied-domain preparation and prevent
replay after same-tick absorption. The
[reproducible input and event sequence](../examples/quantum/repeated_contacts.md)
exercise repeated results and ordinary field decay. Actual checks and source
identity are recorded in [validation evidence](VALIDATION.md).
