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

The canonical [Detector-owned sampling contract](docs/DETECTOR_SAMPLING.md)
allows draws only at an actual external Detector encounter. Ordinary evolution
is deterministic. Earlier autonomous lottery, bond and contact descriptions
below apply only to the explicitly selected `historical-autonomous-v1` research
profile; they do not establish canonical Detector compliance.

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
The explicit dissipate option tracks signed loss; neither option establishes physical
momentum through decay. Self-field exclusion by arrival order remains an unverified
hypothesis and is not enabled by this extension. For straight-ray fields an
optional local one-link exclusion exists: a departing emitter subtracts the rays
of its own departure cycle from the flux it samples on arrival, using only its
own registers; returning self-field at any other distance is not excluded.

Two explicit opt-in policies now
exist for the generic engine, described in [spatial couplings](docs/SPATIAL_COUPLINGS.md#field-phase-first-ordering):
`field_phase_first` completes every field link before carriers sample, so an
emitter's own field is one link ahead on every free-space path; `arrival_port_blind`
keeps the default clock and lets an arriving carrier ignore, for that one sample,
the travel port it came in on, so straight paths are self-blind while maximum-speed
corners still coarrive. Both pass isolated-source and external-source controls;
neither uses source identity, and neither is a derived physical law.

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
named historical candidates. Section 14 defines the optional quantum
assumption of the current implementation; as a model law it lapsed with
Highlights section 3.18, deleted on 2026-09-17 (section 23). Section 23 states the
ray-event model adopted as the target direction on 2026-09-17, with
implementation pending. Section 16 explicitly
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

Adopted direction (model owner, 2026-09-17; implementation pending, see
[section 23](#23-the-ray-event-model)): an event is a change of trajectory
leaving an interaction, a new straight line through one Port. A ray is the
trajectory of one event between two interactions, and a node that a ray
merely crosses hosts no event. The definition above
describes the current implementation; the ray-event definition is the target
every future profile is measured against.

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

Adopted direction (model owner, 2026-09-17): the bound has no exception. The
joint outcome of a pair travels on the returning ray itself, one Link per
step, back to the birth event and on to the partner ray
([section 23](#23-the-ray-event-model)). The registry exception described in
the next paragraph is withdrawn as a model law and retained only as the
historical `bonded-ray-field-v1` profile; its measurements stand as evidence
about that profile, not for the current model. Highlights section 3.18,
which described the shared resource, was deleted on 2026-09-17.

Historical (withdrawn 2026-09-17): the bound was split in two, as the
experiments split it. Energy, momentum,
matter and every message that a record can control move at most one Node per
step, without exception. The joint outcome of a bonded pair, two rays emitted
together, is the one thing that does not: each ray carries the Node and tick
of its birth through the lattice at link speed, and when either end is
measured, the bond registry answers for both ends at once, at any distance (the
[bonded ray field](docs/SPATIAL_FIELDS.md#bonded-rays-bonded-ray-field-v1)).
That answer carries no energy, no momentum and no message: each end alone sees
an even coin whatever the other end does, which the Bell probe measures as
plus rates that do not move with the other side's setting, not a consequence
of the answer carrying no energy. It is the correlation Bell's test measures
beyond the local bound, and nothing else. In Bell's terms the registry is a
deterministic, measurement-independent, parameter-dependent model: the end
that answers second reads the first end's setting, which the
[causal probe](examples/bell-chsh/README.md#which-assumption-of-bells-theorem-each-candidate-breaks)
measures as an outcome that moves with the other end's setting at fixed
hidden variable. It is a nonlocal resource, not a local explanation of the
Bell value, and the unmoved plus rates are no-signalling, not locality. The
registry keeps a bounded bank of
open pairs, one identity per pair from its birth Node and tick, releases a
pair at its second answer, and answers a repeated question the same way, so
it is bounded and idempotent like every other owner. A world with no bonded
field has no exception at all.

A particle can also move at most one neighbor per step. The same movement law
applies at all speeds; there are no separate low-speed and high-speed laws.

A ray on the Euclidean pace waits at a Node for part of its journey so that
every heading covers the same Euclidean distance per step. Waiting is slower,
never faster: the bound holds for every heading, and the lattice metric is a
configured choice, not a derivation.

## 5. Physical calculations use integers only

Every value affecting simulation evolution is an integer: position, time, field,
momentum, counter and remainder.

Core calculations contain no floating-point values, trigonometry, roots or vector
normalization. Conservation-preserving division retains the missing fraction as
an integer remainder carried into the next calculation.

Schema 2 finite attenuation changes each packet/octant/component reaching an
interior receiver from `v` to `sign(v) * floor(abs(v) * p / q)`, with integer
`0 <= p < q`. Signed inventory is preserved: by default the removed signed quantity is
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
The generic engine's default clock fails this requirement for a value-driven
exchange response: a carrier and the field it emits in its departure interval
cross one link together, and `tests/test_field_phase_first.py` records that
baseline. The opt-in `field_phase_first` and `arrival_port_blind` policies in
[spatial couplings](docs/SPATIAL_COUPLINGS.md#field-phase-first-ordering) satisfy
it for straight motion by ordering alone; the flux-driven rotation law satisfies
it under the default clock by geometry, as `tests/test_rotation_self_interaction.py`
shows. None of these selects a self-force law under acceleration.
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

The outward octant candidate conserves flux through every closed shell but
concentrates it near body diagonals. The straight-ray candidate keeps the same
shell conservation and makes the time-averaged flux follow solid angle in every
direction, because each ray carries its own heading and phase and never spreads.
Signed quanta are the attraction hypothesis under test: a source emits negative
quanta paid into its own stock, a body absorbs a share proportional to its mass
and pays for the momentum it gains toward the source. Energy and momentum stay
exact at every event; no gravitational constant is derived, and a source's stock
rises by what it emits. Kerengonen phased rays are the interference hypothesis:
a ray carries a phase that advances per link, rays that meet combine by phase,
and the coherence gates what is absorbed and sampled while every quantum stays
whole and accounted for. Quanta that cancel continue; whether that is the right
place for them is the question the candidate is meant to test. A ray's advance
per link may come from its emitter's momentum, `|p| / D`, the de Broglie
hypothesis: measured as a fringe period inverse to momentum, not derived.

Three limits of the ray were tested rather than assumed. A single particle
dissolved into rays lands where its wave is absorbed, spread over the screen;
it cannot land whole at one Node, because each ray carries conserved stock at
link speed and no local rule can retire the other rays when one is captured
without a signal faster than the rays themselves, which postulate 4 forbids.
Whole landing needs either inventory that a domain owns rather than rays
carry, as the quantum layer keeps it, or matter rays slower than the causal
speed with a retirement that travels at that speed. A mirror can reflect
across a lattice axis or a lattice diagonal, and a fraction makes it partial;
an arbitrary angle needs a heading map beyond a signed permutation. The
fringe follows Manhattan path difference on the links metric and Euclidean
path difference on the Euclidean pace: the metric is a configured choice
under test, with every quantum still counted whole.

The whole landing was then built by the second route, claim and gather: a
matter wave slower than link speed, and a claim that spreads from the
capturing Node at link speed, Node to Node, each Node remembering the port it
came from. Rays of the claimed train that meet the claim turn homeward along
those ports, and the capturing record takes them whole. The wave becomes one
particle at one known place, but not at once: the rest arrives over the ticks
the claim and the return take, and until it does the particle is a claim plus
matter in transit, all counted. Where two captures race, the earlier one wins
when their claims meet and the later keeps only what it took first. This is
the hypothesis under test for postulate 12's open question: a local,
causal, exactly counted collapse, whose measured signature is a landing that
takes time.

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

The ray was put to Bell's test. Two rays from one Node share a hidden phase,
each side's detector takes its ray with the coherence of that phase against a
local reference (Malus's law on the Kerengonen coherence), and the
[CHSH probe](examples/bell-chsh/README.md) measures the correlations. The
result is what a local model must give: S near the value the two independent
lotteries predict, below the local bound 2, and far from the quantum 2 sqrt 2.
The ray explains the shared origin, the no-signaling and the collapse's
timing; it cannot explain the correlations beyond the bound, and no local
rule on this lattice can. Replacing the lottery by deterministic hidden
variables (the `threshold` capture) raises S to exactly 2 and no further, as
the theorem says. The excess is reached only by the bonded ray field, which
takes the split of postulate 4: the pair's joint outcome is answered for both
ends at once by the bond registry, with no energy, momentum or message in it,
and S rises to the quantum value. The ray then carries everything physical at
link speed and the bond carries the one thing the experiments say is not
carried: the correlation. It is not a local derivation of the quantum
correlations, and it does not claim to be. What remains open is what the
registry is.

The dark-matter question was put to the same rule. Gathering a gravity train
to whoever catches a ray of it does focus the pull, but into the momentum of
the part of the train the flood can reach: it falls slowly while the catch
is partial and cancels when the catch is complete, and a rotation curve from
it would rise, not stay flat. The plain ray gravity stays inverse square. The
[gathered gravity probe](examples/gathered-gravity/README.md) records it: the
lattice has no focusing that mimics unseen mass.

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

Only the main engine may commit physical events through an explicit interface.
The later native extensions in sections 16 and 18 define their limited interface
and origin polling; quantum-field feedback is not supplied by this original
terminal-trial addition. Exact contracts and ownership are specified in
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

## 18. Event-spacetime origin cells - Q-ORIGINS-3

The user-selected origin-cell candidate keeps history solely in immutable event
spacetime, with no separate linked list per Node or wave. A participating Node
holds at most six origin IDs. Configured local operations propagate possible
causal support; they do not sample a hidden particle path. Current virtual
register heads and exact joint quantum state retain their existing owners.

At an explicit local wave interaction, the owner calculates every instrument
outcome from the current conditional state. A configured terminal outcome marks
its selected origins resolved once, atomically with the result. Other Nodes
check their local references each native tick and discard resolved origins;
commit never sweeps all wave fragments. A later gate executes only if every
declared participating origin remains active and has arrived at a local endpoint.
Suppressing a retired-origin gate requires unchanged complete correlated density.
Suppressing a retired instrument additionally requires its sole possible outcome
to be the declared no-event result with unchanged density. Otherwise reject the
cancellation; a remote flag cannot remove observable dynamics arbitrarily.
These certificates are separately priced quantum-owner work, not O(1) status
lookups or physical observer signals. One origin may encode several disturbances;
the interaction definition names one to six origins without inferring particle
count. A continuing outcome
preserves the conditional state. A position record does not assign sharp momentum,
and a coherent interaction need not sample at all.

Resolution status is quantum-owner bookkeeping associated with the source event,
not a mutation of its historical physical data or an ordinary remote field read.
The finite candidate, initialization requirements, cost distinctions and open
physical questions are defined in [WAVE_ORIGINS.md](docs/WAVE_ORIGINS.md).
Bounded local lookup does not make total host evaluation or memory constant.

## 19. Localized quantum contact candidate

The explicitly selected [localized contact hybrid](docs/LOCALIZED_QUANTUM_CONTACT.md)
transfers one configured ordinary inventory into a finite coherent domain only
when an actual local contact commits. Undefined momentum is explicit information
state, not a zero vector or a derivation of propagation amplitudes. A complete
local absorption instrument restores one localized record and leaves quantum
vacuum. Number-preserving propagation and origin retirement keep one inventory.

Ordinary fields are emitted only by localized records under their finite configured
allowances. Existing field stock continues causally. Neither conditioned
probabilities nor shared origin flags drive a remote ordinary field update.
This is the user-selected approximation, not a derivation of quantum fields,
physical momentum or the general classical limit. Its clock and representation
limits are explicit and do not silently extend the older native profiles.

## 20. Causal local quantum source candidate

The explicit [causal source extension](docs/CAUSAL_QUANTUM_SOURCES.md) permits
ordinary emission weighted by a bounded complex envelope retained at the same
Node. Phase evolution uses frozen local and causally received neighbor inputs.
Only an actual local contact can prepare or localize the configured inventory.
A successful capture creates one full-strength localized source and sends
termination through Links with local delay. Shared quantum origin retirement
never controls remote ordinary fields or their clocks.

After measurement these are retarded, potentially unnormalized source weights;
the candidate does not silently substitute global conditional probabilities.
Previously emitted fields remain causal, finite source allowances do not refill,
and charge inventory is counted separately from field-source weights. This
extends section 19 only for `causal-contact-fields-v1`, preserving its older
localized-only selection and making no new quantum-field or energy-closure claim.

The optional [null notice extension](docs/CAUSAL_QUANTUM_SOURCES.md#opt-in-causal-null-notices)
lets a Node that records a null result send its own renormalization factor
`1/(1-p)` through Links. Receiving Nodes multiply a local weight scale after
their control delay and forward the notice. The factor is computed from local
state only and travels at Link speed; for one excitation it equals the exact
conditional renormalization once delivered. Between decision and arrival the
remote weights remain stale. This is a candidate rule that closes a measured
gap in the single-excitation sector; it is not a general Born-rule mechanism
for entangled registers and it never reads the shared quantum state.

The optional [field-dependent phase](docs/CAUSAL_QUANTUM_SOURCES.md#opt-in-field-dependent-phase)
lets a configured one-mode gate choose its exact integer phase from the Node's
own classical field value at the schedule tick. The classical field then acts
on the wave, locally and causally, as a phase only. Its `unit / vacuum` ratio
is configured data, not a derived coupling constant, and no field-plus-matter
conservation follows from it. Negative field exponents invert that relative
phase by conjugating both coefficients; a common phase on the coefficient pair
does not change observable probabilities.

The optional [funded envelope emission](docs/CAUSAL_QUANTUM_SOURCES.md#opt-in-funded-envelope-emission)
pays the wave's classical field from the wave's own conserved stock instead of
an external source, so the field and the wave close together: totals stay
constant, the localized winner inherits the unspent stock, and the only
external term is the retarded emission committed after a remote localization,
which is reported. The stock is held by the quantum owner like charge and mass;
it is not transported between modes, and the field still exerts no force on it.

## 21. Configured recurrent contact outcomes

The explicit [recurrent contact candidate](docs/RECURRENT_QUANTUM_CONTACT.md),
`recurrent-contact-fields-v1`, extends section 20 with complete configured local
outcome instruments. A source encounter can retain its localized record or
transfer it into a vacuum domain. A capture can leave vacuum, localize the
inventory, continue the conditional wave, or resolve its origin and begin a new
local continuation. Only the instrument and current conditional state determine
the lottery; a certain result consumes no random ticket.

One inventory owner survives each transfer. New-wave creation and old-origin
resolution are atomic, with immutable event history and bounded current references.
At most six explicitly preallocated source generations retain separate causal
packets and finite allowances. A local vacuum result clears every nonretired
local envelope; remote quantum generation changes cannot choose an ordinary
source bank. Existing field stock follows its configured transport and decay.
This is a finite configured hypothesis, preserving the older profiles and their
limits; it does not derive the matrices or establish physical energy closure.

## 22. Historical autonomous sampling candidates

Adopted direction (model owner, 2026-09-17): the only draw in the model is the
Detector interaction, 1 or 0 for each transfer arriving at a marked node,
every ray being a wave ray, 1 ordinary behavior and 0 return, one bit per
arriving transfer, and the bit is all the Detector adds
(the [Detector-only contract](docs/DETECTOR_SAMPLING.md) made concrete in
[section 23](#23-the-ray-event-model)). A pair's bit is drawn at the first
Detector and carried by the returning ray, which walks back the same number
of steps it has made since its event and transmits it by the inverse split
at the birth event to the partner ray's line, and the second Detector
receives it on the ray that reaches it and draws its own bit on that
arrival like on any other; a Detector sees nothing of the ray, only its own
value, the received value is information on the ray, not an input to the
draw, and no owner answers at a distance. The information of the last event
and the Detector's bit stay on the ray as hidden variables: no Detector and
no ordinary coupling reads them today, they come from no ordinary physics,
and for now they affect no one; nothing on the board feels them. With two Detectors,
Alice's and Bob's, whichever returns first sends its value through the birth
event and the other receives it; sometimes it is Alice's information,
sometimes Bob's. To Alice and Bob the correlation feels as if it were decided
at time zero, but nothing happened at time zero: the value was carried
through the birth event in event spacetime, one Link per interval.
For two Detectors at equal distance from the birth the CHSH value is at most 2,
and the joint law's value appears only when the second ray's path exceeds the
round trip through the first Detector. This price is accepted. The text below
describes the historical candidates, including the shared registry, and their
measurements.

Every interaction whose outcome is not certain consumes exactly one bounded
integer from a configured sequence, and nothing else decides it: the record's
own ticket for a lottery capture on a ray field, the quantum owner's ticket at
a contact, and the bond registry's number for a bonded pair. The world's
history is fixed by its rules, its initial state and this sequence of integers,
one per interaction, and the same sequence replays the same history. Replay
establishes reproducibility, not reversibility, and no physical origin for
the probabilities.

A bonded pair is one interaction and draws one number, whichever end asks
first, Alice's or Bob's. The number is a fixed function of the registry seed
and the pair's birth code. Its upper half is the first end's even coin; its
lower half, read against the difference of the two settings, decides whether
the second end agrees, with the singlet's probability
`(1 - cos(difference)) / 2`. Neither end can read the number: each sees an even
coin whatever the other end's setting, so the number carries no message and
postulate 4 holds for everything physical. The number is a hidden variable in
Bell's sense, local for a lottery capture, where it lives in the detector's
record row and `S` stays at or below 2, and shared for a bonded pair, where
one number answers both ends and `S` reaches the quantum value. The
[bonded ray field](docs/SPATIAL_FIELDS.md#bonded-rays-bonded-ray-field-v1)
implements the pair's single number; the [Bell probe](examples/bell-chsh/README.md)
measures it. What the sequence is, beyond a configured seed, is the open
question of postulate 12 in another form.

Three things follow from this postulate without a further assumption. The
sequence is the only place where information not already in the world's
state enters the world, because everything else is fixed by the rules and the
initial state. The model does not fix the generator of the sequence: a
seed, a file or a source outside the world give the same physics as long as
the numbers are used the same way. It does fix how a number is read, and that
decides which of Bell's assumptions is at stake: a number chosen before the
settings and read by one end only is a local hidden variable and keeps `S` at
or below 2 (the lottery); a number chosen before the settings and read by
both ends keeps measurement independence and breaks parameter independence
(the registry); a number correlated with the settings would relax measurement
independence, and no rule in the model does that. And the two halves of a bonded pair's number are bound
differently: a supply biased in the coin half moves one end's plus rate
with the other end's setting, a signal faster than the causal speed,
measured as such; a supply biased in the agreement half moves no marginal
and is not a signal, and it is not held to the quantum value either, since a
fixed lower half gives the Popescu-Rohrlich box, `S = 4`, with even
marginals. No-signalling bounds the coin, not the correlation; what bounds
the correlation at the quantum value is the singlet law in the lower half,
and that law is configured. The [hypotheses page](docs/HYPOTHESES.md) states the tests.

## 23. The ray-event model

Adopted as the target direction by the model owner on 2026-09-17 and recorded
in [docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) (sections 3.3, 3.4, 3.5, 3.15,
3.19, 3.20, 5.1 and 5.4), the Highlights specification edited directly since
that date. The design candidate `ray-event-model-v1` in
[docs/RAY_EVENT_MODEL.md](docs/RAY_EVENT_MODEL.md) holds the complete
statement, the migration order and the acceptance criteria.
Nothing in this section is implemented yet; every implementation step is a
separate published change measured against that document.

The model has exactly two definitions, event and ray: a ray carries
information, an event is where that information splits, and a ray is what
was split off from an event. An interaction is a meeting of rays at a node in
one interval, decided by the coupling declared between the families present;
it is the only place where anything is decided, and its result is at most six
events, one per Port. Event spacetime has layers: a layer is a set of
families that couple, and a meeting exists only inside a layer; rays whose
families have no declared coupling never meet and cross as if the other were
not there, so two events can happen at the same node in the same interval in
layers that do not communicate. An event is a change of trajectory: a new straight line
leaving the interaction through one Port. A ray is not an object; it is the
trajectory of one event between two interactions, the same event with the
same family properties, one node per Link interval, one heading. From its
event, every ray carries the number of steps it has made, and every ray
carries the information of the last event it was involved in; if that event
was at a Detector, the ray records that it was a Detector event and the bit
drawn, 1 or 0, and the bit is all the Detector adds. A ray trajectory is
reversible: run backward it returns exactly to the interaction
that created it, because nothing was added or lost along the line. A node
that a ray merely crosses hosts no event.

Outside a Detector every trajectory an interaction permits actually happens:
the up-to-six events all propagate, each as a straight ray with its share of
the conserved quantities and its phase. Alternatives are created only at
interactions, never at the empty nodes a ray crosses. Every ray is a wave ray
and carries a phase; a plain ray is a special case of the wave ray, not a
second kind. Light is a wave ray with no mass and no charge, an event moving
in time. Three things change a phase and nothing else: each interval advances
it at the rest rate its family declares, which is the ray's mass as a clock,
and that rate is zero for light, whose phase does not advance along its own
line; an interaction changes it as the declared coupling says; a bound group
advances it once per interval it is held. A light ray carries the phase of
the clock that emitted it at the moment of emission and delivers it
unchanged, so the frequency of light is the rate of its emitter's clock.
Interference of light follows from this alone: two paths of different length
reach one place at one time only if their rays were emitted at different
times, so they carry different emission phases, and the difference is the
emitter's rate times the difference in path length; nothing is accumulated
on the way. There is no amplitude as a number and no probability field: the
phase and the ray's conserved content together are the discrete stand-in for
the quantum amplitude, the phase as its angle and the conserved content as
its size. Because every permitted trajectory happens, the intensity at a
place is how much content arrived there, and interference is steering:
where rays meet in one layer, the declared coupling reads their phase
difference and decides through which Port the shared content leaves, with
every invariant exact; nothing is erased. The Detector reads none of this;
the probability of a click is already in how much content reached it.

At a node where rays meet, the declared coupling decides one of three things:
no interaction, and the rays cross as if the other were not there; a
deterministic interaction, up to six
events computed from the frozen inputs with every declared invariant exact
over all inputs and outputs; or a Detector interaction, at a node whose Detector
bit is set, which draws 1 or 0 for each arriving transfer, independently,
up to six in one interval: 1 ordinary behavior together with the other
arrivals that drew 1, 0 return of that arrival on its own line. A ray alone
at a node never interacts.
Binding is the interaction whose result is zero events: the rays stay at the
node, interact again every interval, and their phase advances once per
interval.

Every node carries one bit, Detector or not; the mark is bounded node
metadata (bit, setting, ticket seed), not a record and not an external
device, and Detector behavior is how a node behaves when the bit is set. A
marked node does one very simple thing. What arrives is a wave ray carrying
information; every ray is a wave ray, so the kind makes no difference. For
each transfer that arrives, whatever it is, it draws 1 or 0. On 1 it behaves
as an ordinary node for that arrival and the transfer continues or interacts.
On 0 it returns that wave ray on the same line in the opposite direction,
unchanged, back the same number of steps it has made since its event, so that
it arrives at the node it left from with exactly the information it left
with. Up to six transfers can arrive in one interval, one per Port, and
the node draws once for each, independently: the arrivals that drew 1 enter
the ordinary interaction together, each arrival that drew 0 is returned on
its own line. The Detector reads, changes,
absorbs and adds nothing; the click is the record of the bit drawn. A
Detector sees nothing of the ray, on 1 or on 0: it sees only its own value.
When it returned a ray with 0, that value travels with the ray, and the
second Detector of the pair receives it on the ray that reaches it.
A returning ray retraces its own trajectory by its step count, reaches its
birth interaction with certainty and there performs the inverse split of its
share: it transmits what happened at the event, with its bit, to the same
places the event sent to, the partner ray's line among them, so the
partner's Detector is not missing it: it receives that value on the ray
that reaches it. Pair identity is the trajectory, not the birth node and
tick.

A ray has a field: the field is the ray's own information spreading in ray
form to the nodes around it, without an event; a field ray is not a second
kind and is not born at an event. The field's presence at a node is an
interaction that makes no event. A field never makes an event unless it
meets something it changes; the first event a field is involved in is that
meeting, and the returning ray that carries the recoil is split off from
it, like every ray from its event. Where a field ray meets a ray whose declared
coupling responds, the meeting is an ordinary interaction and its events
change that ray's trajectory; everywhere else the field crosses without an
event. One of those events is the field ray itself returning reversed: the
return is the opposite momentum of the field, carried back along the field
ray's line to the ray that released it, which recoils when the return
arrives, at finite speed. That is how postulate 7 and Highlights 3.14 are
satisfied: the recoil is a ray. Until its field meets something, a
traveling ray pays nothing for it. The field is released in all directions.
A ray traveling straight never meets its own field: the field is born where
the ray is and leaves at the causal speed, ahead of the ray or away from it,
and the ray is never faster than its field, at any output-clock delay; no
exclusion rule is needed. Only after a change of trajectory can a ray cross
field it released earlier, and that is a meeting like any other. A ray's
phase per interval comes from its family's rest rate alone, not from its
own field.
There is no
matter in the model at this stage: matter is the name for rays bound in one
node by a declared binding coupling, a neutron ray and a proton ray held
together by the strong binding, an electron ray around them whose trajectory
is changed at every step by the field rays the bound pair releases. Mass is
the retained energy of a bound group, and the group's phase advance is its
clock. A bound group has no lifetime of its own: it lasts as long as the
binding interaction repeats at that node without releasing an event. The
binding may be nothing more than a very large output-clock delay (Highlights
3.28) that the bound rays create together, a large mass making the node very
slow, so that the rays do not leave. It is unbound the same way anything
else happens on the board: a ray arrives (a high-energy light ray, for
instance; there is no photon, only a ray) and the coupling declared for the
families present produces events that leave. Nothing else creates or
destroys matter. Held source records remain an explicitly labeled interim
device until the binding couplings exist.

Postulates 1 to 4 hold under this model without exception; the registry
exception of postulate 4 and the shared query of section 14 lapsed with
Highlights section 3.18, deleted on 2026-09-17, and the price stated in
postulate 22 is accepted.

## 24. Everything is information transfer; a return is the inverse split at the event

Adopted as the target direction by the model owner on 2026-09-17, together
with section 23, and restated by him the same day (Highlights 3.3, 3.20 and
5.4); implementation pending.

Everything on the board is a transfer of information. The model has exactly
two definitions, event and ray: a ray carries information, an event is where
that information splits, and a ray is what was split off from an event. An
event is a splitting of information: the interaction splits what arrived
into the rays that leave, at most six, and each ray carries its own share of
what happened at the event away from it, along its line, one node per
interval. All the information is on the rays; the origin node keeps nothing,
and there is no register of any kind at the origin, no occupied channel and
no capacity rule: rays cross, meet or bind by their declared couplings, and
nothing is pushed back or made to wait for room. Every ray carries the
information of the last event it was involved in; if that event was at a
Detector, the ray records that it was a Detector event and the bit drawn,
1 or 0, and the bit is all the Detector adds. An event cannot be moved;
there is no such thing. It happened at its node, and a returning ray walks
back exactly the number of steps it has made to reach it.

A Detector that returns a ray is not sending a message to anyone. The
returning ray carries what happened at the event, its own share only, with
its bit and nothing larger, and at the event node it performs the inverse
split with its information, transmitting it to the same places the event
sent to, so that it cancels what was already there and the momentum and
energy of that share are restored exactly. This turns time back for that
ray's share only; the other shares are untouched until their own rays
return. A ray that passes the Detector is realized. For a pair, the
partner ray's line is among the same places, so the partner's Detector is
not missing the bit; that is the same inverse split, not a second mechanism.
The transmission is a ray like any other, with a field like any other: it
cancels the share only where it meets it, and where it meets nothing it makes
no event, by the same definitions. A share that left the event earlier on a
straight line at the same speed is met only where it was delayed: bound at a
node, slowed by an output clock, changed by an interaction or standing at a
Detector; for a pair this is the condition of Highlights 5.4. Even when it
is never caught, the event as it was has changed: the returned ray reversed
its share, so the event lost that share, and the information is never lost,
it chases the share it cancels. If the share is delayed and caught, momentum
and everything else are conserved at the node where they meet.

What a returning ray does at its event node when nothing is there is a
configured mode of the world, three of which are defined and tested:
siblings, the default and the rule above (it transmits its share and bit to
every line the event sent to, which needs at most six records on the ray,
one per Port); straight (it continues straight through the node on the one
line opposite its own, enough for a pair, with no records); and annul (it
ends there, its content leaves the world into an explicitly accounted sink,
initial equals current plus escaped plus annulled at every tick, and its
information survives only in the record). If something is at the node, a
bound group or other rays, the returning ray meets it by the declared
coupling in every mode. For a ray-interaction event whose inputs were
consumed, the returning ray cancels its own share only and continues along
the event's output lines; nothing is left at the node.

Each ray meets its own fate. Sibling events of one interaction are
independent rays; nothing cancels a sibling's share except its own return.
The once-only requirement of the central specification is therefore a
property of the returns, not of a shared owner, and it is accepted that a
sibling can be realized at a second Detector before a return from the first
arrives.

The conservation laws exist for this. Energy, momentum component by
component, charge and every other declared invariant are conserved exactly
across an interaction so that the event can be rebuilt from its pieces when
they return: the pieces are the information, and the conserved totals are
the check that nothing was added or lost when they split and when a share is
returned. A Detector that returns a ray is therefore returning an event in
time: the share walks its line backward and the event is undone by exactly
the amount that share carried, and only that. Exact integer conservation on
the lattice is what makes this undoing exact rather than approximate.

The design candidate in [docs/RAY_EVENT_MODEL.md](docs/RAY_EVENT_MODEL.md)
carries this section's consequences for ray state and for the acceptance
criteria.
