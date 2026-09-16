# Private 36-register contact candidate

This is the implementation contract for `private-register-bond-v1`, selected
after the user requested cubic 36-register execution and correction of the
separate two-detector experiment. It extends the private identity candidate in
PR141. The existing 24-register input remains an explicitly selected historical
fixture. This contract reuses the authorized shared-pair law in
[postulate 22](../POSTULATES.md#22-the-lottery-is-the-reality-one-integer-per-interaction)
and [BondRegistry](../src/event_universe/fields/bonds.py); it does not derive
Bell correlations from local hidden variables.

## Topology and transport

Each cubic Node is a container of 36 independent Registers, indexed by all
ordered pairs of the six Ports. A Register has private bounded state, one
input and at most one output. The Node adds no mixer, action or delay. Ordinary
channels span exactly one cardinal neighbor and take one tick. Six distinct
neighbors require all periodic extents to be at least three in this example.

The new input supplies all 36 routes, never an inferred universal routing law.
For source `(p,q)`, its offset is `direction[q]` and target entrance is `q^1`.
The target exit is `p` for perpendicular ports, `q` for straight travel
(`p == q^1`), and `q^1` for return (`p == q`). This is a permutation of all
target Registers. The twelve added routes therefore allow straight and return
traffic while preserving the older perpendicular square loops.

The core supports explicit immutable port-pair sets. The 24-pair fixture uses
its original set; this profile uses all 36. Host keys validate port ranges;
each Node, selector and wiring validates membership in its chosen set.

## Private local contact and the quantum boundary

An input token has exactly two positive-encoded bounded integer components:
`(pair_id, end)`, with end 1 or 2. These are configured ownership identifiers,
not energy or momentum. Initial input supplies two tokens at the same source,
one per end. No pair creation, beam splitting or species coupling is inferred.

An immutable detector binding selects one Register, one end and a setting in
the 64-step phase table. A pure local request function reads only the selected
Register's private state, its actually due input and that detector definition.
It receives no Node, peer reference, address, clock or registry callback.
An empty Register requests capture; an occupied detector rejects another token.
Empty inputs do not request an oracle call or change private state.

The integration owner handles the resulting request through BondRegistry during
the same step, before publication of any state. Each terminal capture retains
`(pair_id,end,outcome)` in that Register's bounded private state and consumes
its actual input. It emits no outgoing beam. The retained state is the token's
sole physical owner; the outcome is metadata about it. Other Registers apply
the unchanged identity operation and transfer their actual input object.

Capture is an explicitly configured terminal contact, not an automatic rule
for every Event. The detector is drawn at its Node and its retained state is
shown by the existing renderer. A shared-pair answer is the explicit quantum
exception: it does not access an ordinary neighboring Register's private state.

## One number and finite lifecycle

The shared quantum owner contains a fixed declared set of at most 4096 pair IDs,
the existing bounded registry, and two answer/setting slots for each pair.
First access obtains the pair's number through the existing law; the other end
uses the same number. Both answers remain cached after registry release.
Replaying the same pair/end/setting returns its cached answer without drawing;
changing a previously used setting or requesting an undeclared pair fails.
The cache is quantum bookkeeping and does not duplicate token inventory.

Settings live at detector bindings; transported tokens carry no remote setting
or predicted outcome. Each real detector request has model oracle cost one and
zero additional model-time delay. Count requests, newly drawn numbers and host
bookkeeping separately. This is a finite experiment; it does not claim an
unbounded completed-pair history or constant total host work.

## Scheduler integration and atomicity

The scheduler first validates the complete due cohort and reads immutable due
data without consuming it. It prepares local results, then the contact owner
stages its quantum results on a private copy. No lookup before the due tick
may trigger a contact. The quantum adapter receives only immutable local input
records, never the world or a live Node/Registry reference for the local law.

All result shapes, input capacity, channel readiness, clock bounds and contact
requests must validate before commit. On success the quantum stage commits,
due ownership is received, each result replaces only its own private state,
and each datum is either sent once or retained once. The existing identity
emission object-ownership guard remains intact. Failure leaves inputs, channels,
due index, private states, quantum state/counters, events, transitions and tick
unchanged. Expected preflight failures must not consume scheduler work counters.
Out-of-memory and externally mutated runtime internals are outside this contract.

Dense and sparse execution share the same preparation and commit implementation.
The audit compares complete private states, inputs, channels, due times, ordered
transport/capture events and complete quantum lifecycle state after every tick.
Host-only history/recording may grow; physical Register memory remains fixed.

## Acceptance and scope

- Validate all 36 routes and six neighbors; explicitly test straight and return.
- Preserve the original 24-register timing/ownership regression fixture.
- Compare dense/sparse execution with simultaneous inputs and terminal captures.
- Two tokens travel from a common source to distinct detectors. No capture
  precedes arrival, and after capture there is no propagating copy of that token.
- Exactly one number and two distinct answers per pair; both arrival orders,
  cached replay, conflicting settings, unknown IDs and capacity/overflow errors.
- Compare lattice outcomes to the existing registry and independent endpoint
  controls; retain a local CHSH control at or below 2 and report sampling error.
- Every explicit run produces existing-generator HTML and quantitative evidence.

This integrates the chosen shared-pair resource with private36. It does not
migrate the complete entity catalog, add all physical couplings, supply a
generic splitting rule, establish isotropic relativity, or replace the native
two-draw quantum program. Fixed settings are not a loophole-free experimental
choice procedure. A shared registry is nonlocal in Bell's factorization sense.
