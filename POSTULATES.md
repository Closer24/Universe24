# Simulator postulates in plain language

This document explains the ideas underlying the simulator without programming
details. Consult it before any change. A change contradicting a binding principle
requires an explicit decision to change the model.

The user-authorized [Node execution profile](docs/NODE_VECTOR_PROCESSOR.md)
declares h as one adjacent-node transit step and each interaction's k as an
explicit positive integer duration in h units. Sequential fired interactions add
their durations; link transit follows local completion. Operation cost is measured
separately. The earlier cost-budget delay contract below still describes profiles
without `node_execution: true`. Conserved readouts remain selected assumptions
until independently derived physical behavior is demonstrated.
Its generic reaction contract admits several local disturbances and fields in
one frozen proposal. Declared invariants and persistent validity conditions must
hold at actual commit, including after a local arrival during the wait. A consumed
start trigger is not a persistent condition. Every affected owner commits together
or remains unchanged; a failed check reports an error without repairing the law.

Distinguish three categories:

- **Binding principle:** a rule the simulator must satisfy.
- **Candidate law:** a specific hypothesis under evaluation, not a proven law of nature.
- **Open question:** an idea that has not been implemented or established.

## Active initialization-defined model

The opt-in [bounded rational candidate](docs/RATIONAL_PARTICLES.md) preserves
finite integer state while representing fractional quantities in explicitly
configured whole/remainder/denominator fields. Its larger finite intermediate
registers, balanced neighbor selection and exact fractional clock are named
choices. They do not establish isotropic light propagation or electromagnetic
energy. The six-neighbor causal boundary remains binding.

The active model treats physical content as configured disturbances carrying
named fields. The engine supplies integer local updates, causal transport,
conservation enforcement and scheduling; initialization supplies identities and
candidate laws. It does not infer familiar physics from names.

All interactions use generic definitions. A configured local pair transaction
may transform several fields together only when its declared invariants and
conserved pair totals hold exactly. Existing elastic-collision formulas remain
explicit reference benchmarks; reproducing them does not mean they emerged from
a computational field. New emergence experiments must use simple local vector
operations to produce states, not supplied continuum force or collision formulas.
Guards and conservation diagnostics validate proposals without replacing this
elementary rule. See [physical entities](docs/PHYSICAL_ENTITIES.md) and the example in
[DISTURBANCES.md](docs/DISTURBANCES.md).

The optional [bounded conversion](docs/LOCAL_CONVERSIONS.md) also permits two
local records to become two explicitly configured output types under the same
atomic conservation checks. This is a supplied transformation, not evidence of
emergent annihilation. [Executable entity profiles](docs/ENTITY_CATALOG.md)
describe bounded representations; physical identity and dynamics cannot be
inferred solely from the ability to store or transport their registers.

The user-defined cost of a local cycle sets a general node delay above the
normal cost. Neighbor transit is fixed, and no computation debt accumulates
between cycles. The exact schema, exchange, timing and source rules are in
[the disturbance contract](docs/DISTURBANCES.md).

The optional [outward spatial-field candidate](docs/SPATIAL_FIELDS.md) separates
source records from the fields they emit. By default its field transport uses a fixed
clock; priced field work contributes to new local carrier cycles while field
forwarding continues at causal link speed. Schema 1 preserves conservative
transport. Schema 2 explicitly selects finite attenuation, `finite-localizing-v1` by default: finite source
and response allowances bound dynamic input, and declared integer attenuation
removes magnitude at interior arrivals while exempting immutable background.
This candidate tracks signed dissipation rather than promising conserved physical
momentum through decay. Self-field exclusion by arrival order remains an unverified
hypothesis and is not enabled by this extension.

The opt-in [shared computation cycle](docs/SPATIAL_COMPUTATION_DELAY.md) applies
the same budget delay to all local fields and carriers. It freezes updates and
directional departures together; later input belongs to the next cycle.
The integer link transit remains fixed. This alternative timing candidate is
selected with `spatial_computation_delay`; existing inputs keep the default.

The optional [spatial response candidate](docs/SPATIAL_COUPLINGS.md) can turn a
configured vector while preserving its length exactly, transferring the opposite
vector change to the same spatial field. This is an integer quarter-turn law;
it does not infer physical names, continuous angles or energy conservation.
Straight cardinal self flux is parallel to its carrier and cannot turn that
vector under the flux-driven law. Turns, periodic return and other coupling
laws require separate self-interaction analysis.

The optional [local field-rule framework](docs/LOCAL_FIELD_RULES.md) treats a
location as a node with six directional connections. Several scalar/vector
components can evolve together from local state and received information, with
explicit retained and outgoing amounts. Joint field/carrier transactions must
pass declared balances before both owners commit; delayed transactions cannot
overwrite intervening field evolution. A logical group of two vectors does not
itself identify an electromagnetic field or supply a photon. Known physical laws
remain independent acceptance targets. A historical benchmark that explicitly
inserts them is not an emergence experiment. This extension is a research
interface, not evidence of their emergence.

Initialization independently chooses periodic or open boundaries. Periodic space
connects opposite faces on each of X, Y and Z without changing a carried direction.
An open terminal link instead removes the original packet after its full transit
time and records the escaped quantities. No exterior node or exterior decay is
simulated. Being spatially closed does not cancel a separately configured decay.

Sections 1–5 and 10–11 state shared locality, arithmetic and evidence principles.
Sections 6–9 document the source, self-force, momentum and turning requirements
of the explicitly selected historical research models; they are not implicit
laws of every configured disturbance. Sections 13 and 15 likewise belong to
named historical candidates. Section 14 defines the optional quantum assumption. Section 16 explicitly
selects its native local-cycle integration without changing unselected worlds.

For a configured law claiming energy and momentum conservation, account for the
fields and disturbances together at every local event. The combined node change
must match actual incoming and outgoing flux. An internal exchange must balance the
participants' energy changes and all three momentum changes at that node;
external sources and losses must be distinguished from closed transfers.
The [local conservation contract](docs/LOCAL_CONSERVATION.md) defines the optional
read-only audit and its supported ownership boundaries. It measures declared
quantities without repairing state, choosing laws or adding model-time cost.
Locality, a passing component ledger and catalog properties alone do not establish
physical energy, momentum or an emergent field law.

## 1. The world consists of locations and events

Space is divided into three-dimensional nodes with six directional connections:
right, left, forward, backward, up and down. A connection reaches one nearest
neighbor, or exits the simulated domain at an explicitly open boundary.

An event is a local change in a node at a particular time: a field update, a particle
momentum change, a move to a neighbor or a blocked move attempt.

The simulator does not assume every familiar physical phenomenon is fundamental.
Mass, gravity, curvature or a known particle can count as an emergent result only
if they arise from local events and laws, rather than being inserted under another name.

## 2. Every location has only bounded local information

A physical node does not store a picture of the entire universe. It stores a fixed
amount of information and reads its own state and information already delivered
by its six neighbors. Section 14
explicitly adds an optional shared quantum query primitive, not a neighbor read.

Local disturbance capacity is fixed in advance. A node has no list that grows with the
number of sources in the universe and does not retain its entire history.

Physical work per local update is therefore bounded and constant. Total host
runtime for a large world is not constant: all active locations still require updates.

This includes estimating or subtracting a particle's own field. A second simulated
world or a search through source histories cannot supply a physical input merely
because its final subtraction happens in one node. LOCALITY-1 in the definitions
document specifies this end-to-end rule and its test/reference boundary.

## 3. Consistency is maintained locally and causally

Each location must be consistent with all information that could already have
reached it. It need not know about a distant event before information arrives.

There is no instantaneous update of the whole universe or central repair of all
space. An event first changes its own location. Its influence travels from neighbor
to neighbor, and each location updates upon receipt under the same local law.
The optional oracle in section 14 is a host-computation exception, not permission
to rewrite physical records or send instantaneous physical messages.

Global consistency emerges from consistent local updates. New information does
not rewrite completed events; it becomes causal input to future events.

**Active contract:** disturbance transfers cross one neighbor link after its
fixed transit time; updates use already available local records. Extra node delay
can make propagation slower. There is no global correction at the end of a tick.

**Not established:** that these local laws suffice for every kind of physical
consistency, particularly quantum consistency and entanglement.

## 4. There is a maximum causal speed

Physical influence cannot skip nodes. It travels at most one neighboring node per
elementary step. This is the role of c: the maximum propagation speed of causal
influence in the simulator. Oracle evaluation is not physical propagation.

A particle can also move at most one neighbor per step. The same movement law
applies at all speeds; there are no separate low-speed and high-speed laws.

## 5. Physical calculations use integers only

Every value affecting simulation evolution is an integer: position, time, field,
momentum, counter and remainder.

Core calculations contain no floating-point values, trigonometry, roots or vector
normalization. Conservation-preserving division retains the missing fraction as
an integer remainder carried into the next calculation.

Schema 2 finite attenuation changes each packet/octant/component reaching an
interior receiver from `v` to `sign(v) * floor(abs(v) * p / q)`, with integer
`0 <= p < q`. A wave never loses flux: by default the removed signed quantity is
deposited as stationary stock at the receiving node, so total inventory is
preserved and a thinning wave ends as whole units at known nodes rather than
fading to nothing. The explicitly selected `"residue": "dissipate"` candidate is
the historical exception: it records the removed quantity as loss, not saved in
a remainder, and makes integer dynamic fields vanish after their last input. The
immutable background is exempt in both cases. It can change a vector's direction and does not
preserve momentum or energy. It does not alter conservative splitting, fractional
source requests or the historical models' remainder rules. See
[the finite field contract](docs/SPATIAL_FIELDS.md#finite-completed-link-decay).

Numbers have fixed bounds. An out-of-range calculation stops the run with an error
rather than hiding overflow or distorting the result.

Display and measurement code may use floating-point values, provided none of its
results feed back into the simulation.

## 6. A resident source remains a source

A particle occupying a node remains a source every tick even without moving.
Its presence in that node represents the source.

The simulator does not repeatedly add a source's own new emission to itself.
A stationary source should form a persistent surrounding state, rather than grow
without bound or disappear because there was no movement event.

## 7. An isolated symmetric source does not push itself

For a single stationary source in symmetric space, field values on opposite sides
of every axis must be equal. Opposite influences cancel, leaving its momentum unchanged.

This is a fundamental local-consistency test: a particle must not start moving
solely because of its own symmetric field.

For an accepted free-motion candidate, this requirement also applies to moving
isolated particles: their momentum and impulse remainders must not change due
to their own field. Baseline failures remain evidence, not approved corrections.
The opt-in `causal-octant-stream-v1` candidate tests this through outward one-link
transport before the particle response, with no source identity or subtraction.
Its free-space guarantee ends at periodic return, which is a boundary effect
requiring separate evidence. The fixed state and limits are specified in
`SIMULATOR_DEFINITIONS.md` and `docs/CAUSAL_STREAM_FIELD.md`.

## 8. Momentum is exchanged at the event location

When a particle receives a momentum change, the field receives an equal and
opposite change in the same event. Both sides are validated before committing.

Never calculate missing momentum at the end of a run and distribute a correction
throughout the universe. Total momentum is a measurement for validation only.

**Open:** energy conservation has not been established, and there is no complete
law for transporting field momentum between locations.

## 9. Field and turning laws are hypotheses under test

The historical scalar field law uses six neighbors, the local source and a retained
remainder. A turning law lets transverse field imbalance change motion direction.

These are **candidate laws**. They are not called gravity and do not establish
Newton's or Einstein's equations. A successful experiment describes the tested
conditions only.

Introduce another law as a separate candidate and compare results. Do not change
old tests merely to make a new law appear successful.

## 10. Measurement and display are outside the physics

Trajectories, reports, images and HTML only read run results. They neither direct
particle motion nor repair the field. Here measurement means diagnostics, not a
quantum interaction that creates a new physical record.

Every application run saves initial conditions, parameters, code identity and
completion or failure evidence. Runs and ordinary tests are headless. Only an
explicit visualization request adds frame capture and a visual artifact identifying
its displayed quantity and geometry. A slice does not change the underlying 3D world.

## 11. A result must pass tests to be considered reliable

A phenomenon seen once in an animation is not a general model result. Check that it:

- is not a bug, an accidental update-order effect or a display artifact;
- persists under the translations, reflections and coordinate-plane changes tested;
- obeys local rules and numerical bounds;
- repeats from documented initial conditions;
- passes checks that were not used to construct the law.

Failure is information about the model. Do not add a special correction just to hide it.

## 12. Quantum behavior and entanglement remain open

The physical core describes discrete fields and particles. The selected quantum
candidate is a deferred event network: a saved joint state plus local operations
and immutable outcome records defines the wave without evaluating it every tick.
An explicit query follows the required past dependencies and evaluates forward.
This is a bounded finite-state model, not a derived electron/photon field law.
The previous scalar-amplitude and terminal-trial interfaces remain available as
separate, explicitly selected historical contracts.

A future full quantum layer must preserve both consistent joint results and the
inability to use those correlations to send information faster than c.

Until these requirements have been tested for the proposed laws, do not claim that
the simulator solves quantum collapse or entanglement consistency.

## Overall principle

Physical nodes keep bounded local state and exchange influence with neighbors.
Section 14 adds an explicitly authorized shared computation primitive alongside
that local world. It does not turn host evaluation into physical communication.

`SIMULATOR_DEFINITIONS.md` contains the exact executable requirements.
`docs/ARCHITECTURE.md` separates the engine, laws and measurements.

## 13. Experimental extension: variable-length links

This historical candidate is selected explicitly through LinkedSimulation. It
does not replace the active disturbance model's fixed neighbor transit time.
In this candidate, each node also stores fixed information about its six links.
It owns the three positive-direction links and keeps local copies of the other
three. Ownership organizes storage; it must not privilege a physical direction.

Both endpoints can propose a length from their local field and information
already delivered by their neighbor. A proposal travels along the old length.
Both endpoints activate it only on arrival. Simultaneous proposals use the larger
length. This is an explicit experimental choice, not a consequence of Einstein's
work. Length changes do not alter a transit already in progress.

The default address spacing is 100 elementary length units; length 110 represents
a tenth of the default spacing added. Light travels one elementary length unit
per elementary tick, so its speed is 1. Each link has at most one packet traveling
in each direction. There are no per-source lists.

A moving particle remains a source at its origin until arrival. Direction and
length are locked at departure; interaction with the field resumes on arrival.
A nonintegral arrival time rounds up to the next tick. Unlike field and momentum
remainders, excess travel time cannot shorten the next transit: crossing a link
faster than c to repair an average is forbidden.

Tests verify stationary-source symmetry, neighbor-only influence and fixed local
storage capacity. They do not establish gravity or geodesics.

## 14. Shared quantum query postulate — Q-ORACLE-1

The user explicitly authorized `deferred-unit-cost-oracle-v1`: one successful
query to the shared quantum space counts as one elementary model operation and
consumes zero world ticks. This is a model assumption, not an established physical
fact or a claim that host computation takes constant time.

The quantum owner may evaluate a long deferred history outside the physical
six-neighbor computation. Its work and resource budgets are measured separately.
Bounded integer arithmetic still applies. Exhaustion and overflow are errors,
not absence of a particle, collapse or a new physical event.

Pure queries do not sample outcomes or change past records. Repeated queries are
consistent. The optional `terminal-two-output-trial-v1` test chooses one complete,
absorbing output using a supplied uniform integer ticket; repeated readout returns
the same shared record. This does not implement general measurement or establish
no-signalling. The test controller's record is not an Engine-native event.

Only the main engine may eventually commit physical events through an explicit
interface. That interface, automatic node polling and quantum-field feedback are
not implemented by this addition. Exact contracts and ownership are specified in
`SIMULATOR_DEFINITIONS.md` and `docs/ARCHITECTURE.md`.

## 15. Supplied mass and local elastic collisions

The historical scalar/contact candidate explicitly adds a positive integer inertial
mass per particle, default
one. This mass is a model input; it has not emerged from events. At the same
momentum a heavier particle moves more slowly, subject to the existing causal
speed limit. Mass does not silently replace the source-strength or field laws.

In the opt-in collision candidate, particles meeting at the same node and tick
undergo elastic backscattering. For equal and opposite momenta both return in the
opposite direction. With unequal masses the result is calculated in the pair's
center-of-mass frame, preserving the pair's total momentum and classical kinetic
energy. Fractions are kept exactly using bounded integer numerators and
denominators. No global correction supplies missing momentum or energy.

A contact occurs once per encounter, without an extra position jump. Link transit
particles can collide only after arrival. Fixed local flags distinguish a new
encounter from particles still occupying the same node. The exact two-body law,
multiparticle ordering, schema extension and limits are in the v13 section of
SIMULATOR_DEFINITIONS.md. This classical lattice hypothesis does not establish
relativistic physics or energy conservation of the existing field law.


### Selected event-network method

`deferred-event-network-v1` extends the existing quantum owner, not the ordinary
physical nodes. Its detailed contract is [QUANTUM_EVENTS.md](docs/QUANTUM_EVENTS.md).
Queries compute possibilities without choosing historical paths. Only an explicit
instrument request can select a result; it retains the conditional joint state,
including a no-event branch. No universal interaction-to-collapse trigger is claimed.

A known event location does not supply a simultaneous sharp momentum. Position
and lattice-momentum diagnostics use the same state. Exact host checkpoints may
replace complete correlated histories without sampling. Unused branches remain
available until an exact sufficient replacement is saved. These choices neither
make host computation O(1) nor establish a Newtonian or continuum field limit.

## 16. Selected native event-program extension

An explicitly selected initialization program may connect the shared quantum
owner to ordinary local cycles through a generic event resolver. A local result
can select a configured mechanical continuation; it is not a free remote state
read. Every executed physical path retains its local operation costs. A query
is one additional model operation, with zero direct world ticks; total local
cycle cost may still produce the ordinary computation delay. No cost is erased
to manufacture the classical endpoint. See [the native contract](docs/NATIVE_QUANTUM_EVENTS.md).
This extends section 14 only for the declared candidate, not all interactions.

## 17. Explicit finite-register and unobserved-channel extension

The selected native v2 candidate permits finite local registers, complete
unobserved channels and grouped measurement outcomes. An unobserved Kraus label
is not a classical record and is not sampled. Preserve its density sum and all
remaining coherent information. Mixed checkpoints represent the complete live
component. Local supports, integer bounds, classical cycle charges and zero
direct oracle ticks remain unchanged. This is a representation/channel extension,
not a new collapse law or a derived physical species Hamiltonian. See
[QUANTUM_ENTITIES.md](docs/QUANTUM_ENTITIES.md).
