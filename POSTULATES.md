# Simulator postulates in plain language

This document explains the ideas underlying the simulator without programming
details. Consult it before any change. A change contradicting a binding principle
requires an explicit decision to change the model.

Distinguish three categories:

- **Binding principle:** a rule the simulator must satisfy.
- **Candidate law:** a specific hypothesis under evaluation, not a proven law of nature.
- **Open question:** an idea that has not been implemented or established.

## 1. The world consists of locations and events

Space is divided into three-dimensional cells. Each cell has six nearest neighbors:
right, left, forward, backward, up and down.

An event is a local change in a cell at a particular time: a field update, a particle
momentum change, a move to a neighbor or a blocked move attempt.

The simulator does not assume every familiar physical phenomenon is fundamental.
Mass, gravity, curvature or a known particle can count as an emergent result only
if they arise from local events and laws, rather than being inserted under another name.

## 2. Every location has only bounded local information

A cell does not store a picture of the entire universe. It stores a fixed amount
of information and reads only its own state and information received from its six neighbors.

Cell particle capacity is fixed in advance. A cell has no list that grows with the
number of sources in the universe and does not retain its entire history.

Physical work per local update is therefore bounded and constant. Total host
runtime for a large world is not constant: all active locations still require updates.

## 3. Consistency is maintained locally and causally

Each location must be consistent with all information that could already have
reached it. It need not know about a distant event before information arrives.

There is no instantaneous update of the whole universe or central repair of all
space. An event first changes its own location. Its influence travels from neighbor
to neighbor, and each location updates upon receipt under the same local law.

Global consistency emerges from consistent local updates. New information does
not rewrite completed events; it becomes causal input to future events.

**Implemented:** a field change travels at most one link per tick; a field update
reads six neighbors. There is no global correction at the end of a tick.

**Not established:** that these local laws suffice for every kind of physical
consistency, particularly quantum consistency and entanglement.

## 4. There is a maximum causal speed

Information and influence cannot skip cells. They travel at most one neighboring
cell per elementary step. This is the role of c: the maximum propagation speed of
causal influence in the simulator.

A particle can also move at most one neighbor per step. The same movement law
applies at all speeds; there are no separate low-speed and high-speed laws.

## 5. Physical calculations use integers only

Every value affecting simulation evolution is an integer: position, time, field,
momentum, counter and remainder.

Core calculations contain no floating-point values, trigonometry, roots or vector
normalization. Nonintegral division retains the missing fraction as an integer
remainder carried into the next calculation.

Numbers have fixed bounds. An out-of-range calculation stops the run with an error
rather than hiding overflow or distorting the result.

Display and measurement code may use floating-point values, provided none of its
results feed back into the simulation.

## 6. A resident source remains a source

A particle occupying a cell remains a source every tick even without moving.
Its presence in that cell represents the source.

The simulator does not repeatedly add a source's own new emission to itself.
A stationary source should form a persistent surrounding state, rather than grow
without bound or disappear because there was no movement event.

## 7. An isolated particle cannot deflect or accelerate itself

In the absence of external fields and other particles, a particle must retain
its initial momentum and inertial trajectory even while its own field is active.
This applies to moving particles as well as stationary ones, at low and high
rates and along cardinal and diagonal directions. Switching on its own source
must not change its trajectory relative to the same source-free experiment.

A straight trajectory on the cardinal lattice is the corresponding digital
staircase, not a diagonal hop through several cells. Compare complete digital
cycles and each tick with the source-free control; do not smooth displayed
coordinates to hide a physical deflection.

For a stationary isolated source, opposite field values must remain symmetric
and its momentum must remain zero. This is the existing stationary special case.
The moving-particle requirement extends it by explicit user instruction. The
historical baseline remains a reference, not proof that it meets this requirement.
A failure of the mandatory isolated-motion test blocks acceptance of the model.

## 8. Momentum is exchanged at the event location

When a particle receives a momentum change, the field receives an equal and
opposite change in the same event. Both sides are validated before committing.

Never calculate missing momentum at the end of a run and distribute a correction
throughout the universe. Total momentum is a measurement for validation only.

**Open:** energy conservation has not been established, and there is no complete
law for transporting field momentum between locations.

## 9. Field and turning laws are hypotheses under test

The current local field law uses six neighbors, the local source and a retained
remainder. A turning law lets transverse field imbalance change motion direction.

These are **candidate laws**. They are not called gravity and do not establish
Newton's or Einstein's equations. A successful experiment describes the tested
conditions only.

Introduce another law as a separate candidate and compare results. Do not change
old tests merely to make a new law appear successful.

## 10. Measurement and display are outside the physics

Trajectories, reports, images and HTML only read run results. They neither direct
particle motion nor repair the field.

Every application run saves initial conditions, parameters, code identity and an
HTML view identifying its displayed geometry. A view may be a 2D slice while the
underlying calculation remains 3D.

## 11. A result must pass tests to be considered reliable

A phenomenon seen once in an animation is not a general model result. Check that it:

- is not a bug, an accidental update-order effect or a display artifact;
- persists under the translations, reflections and coordinate-plane changes tested;
- obeys local rules and numerical bounds;
- repeats from documented initial conditions;
- passes checks that were not used to construct the law.

Failure is information about the model. Do not add a special correction just to hide it.

## 12. Quantum behavior and entanglement remain open

The present core describes discrete fields and particles. It does not yet implement
quantum state, amplitudes, interference, measurement or entanglement.

A future quantum layer must preserve both consistent joint results and the
inability to use those correlations to send information faster than c.

Until a precise local law satisfies these requirements, do not claim that the
simulator solves quantum collapse or entanglement consistency.

## Overall principle

The simulated universe is not kept consistent by instantly knowing everything.
Each location stores little information, responds only to what has arrived, and
exchanges information with neighbors under a fixed law. Spatial consistency is
intended to emerge from the consistency of each local event.

`SIMULATOR_DEFINITIONS.md` contains the exact executable requirements.
`docs/ARCHITECTURE.md` separates the engine, laws and measurements.

## 13. Experimental extension: variable-length links

In this candidate, each cell also stores fixed information about its six links.
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
