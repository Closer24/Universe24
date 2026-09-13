# Causal outward-stream field candidate

Model id: `causal-octant-stream-v1`.

Integration retains this identity and its transport law. Invalid negative old
populations are rejected before any positive source can mask them. The inherited
scalar `seed_field` API is explicitly unsupported; it cannot silently create a
scalar record that the stream evolution never reads. No scalar-to-stream initial
condition rule is invented by this integration.

This candidate tests one binding acceptance target: an isolated particle must not
receive momentum or carried impulse residue from the field it generated itself.
The result must emerge from causal field transport. The particle law may not use
source identity, a remote lookup, a per-source map, a growing history, a global
subtraction, or a particle-count special case.

## Local law

Each materialized stream node has a fixed 14-integer stream record:

- eight nonnegative octant populations;
- six directional amounts delivered in the current tick.

The eight octants are the fixed sign triples `(+++), (++-), (+-+), (+--),
(-++), (-+-), (--+), (---)`. A population can move only along one of the three
cardinal directions whose sign belongs to its octant. Therefore every hop
increases Manhattan distance from the emission point by exactly one. No source
identity is stored.

At each tick the field phase happens before particle response and movement. Every
old population plus the local occupancy source is split over its three allowed
cardinal directions. Integer division by three is exact in total: indivisible
units rotate between axes using `tick mod 3`. All emitted amounts move exactly one
nearest-neighbor link in that field phase. The source emits the same configured
integer amount into each octant; `source_per_octant` is an explicit model choice,
not a calibrated physical constant.

The particle reads only the six amounts delivered to its current node in that
field phase. For the attractive candidate, opposite ports are swapped before the
existing central-difference response. The response then uses the existing bounded
integer impulse/remainder exchange and movement code.

## Why the isolated self stream cannot catch the particle before wraparound

A stream emitted at a particle position is already one link away before the
particle response and movement of that tick. After another field phase it is two
links from that emission point while the particle has completed at most one hop,
and so on. Because every stream path is monotone in Manhattan distance and matter
is limited to one hop per tick, the stream remains at least one link ahead of the
particle at every force read. This argument does not use particle identity.

Periodic wraparound is a boundary return and is excluded from the isolated
acceptance interval. Tests use domains large enough that no emitted stream can
wrap to the particle during the measured run.

## Acceptance tests

The candidate must preserve both particle momentum and all three impulse
remainders at every tick for isolated particles moving along axes and diagonals
at several legal rates. It must also demonstrate that this is not a force-off
model: a second source outside the particle must enter the Manhattan causal cone
at one link per tick and produce an equal-and-opposite interaction in a symmetric
pair test. An offset moving pair must show transverse attraction after causal
contact.

## Read-only display

Diagnostics may display the sum of the eight populations as stream magnitude.
This read-only host projection is not scalar phi and never feeds physical state.

## What this candidate does not establish

The eight-octant branching is a discrete transport hypothesis, not Maxwell's
equations, Newtonian gravity or general relativity. It has cubic/Manhattan lattice
anisotropy. Integer branch allocation produces a three-tick microcycle when an
amount is not divisible by three. The average radial falloff, energy accounting,
field-momentum transport, continuum limit and rotational convergence remain open
validation tasks. Passing the isolated self-force gate is necessary but not
sufficient to promote this candidate to the default model.
