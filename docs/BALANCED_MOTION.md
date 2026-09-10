# Balanced motion and twelve-cell local halo candidate

Base: upstream `76676d48ffbe7fc53913f4d26464921cb20f72df`.
Candidate: `scalar-field-v12-balanced-halo`, exposed as `BalancedSimulation`
in `event_universe.api`. Baseline `Simulation` and the frozen v10 reference retain
their existing behavior.

## Feature contract

| Part | Contract |
| --- | --- |
| Motion law | Interleave cardinal steps using integer prefix counts; retain the shared speed budget |
| Halo law | After every particle has responded and moved, cancel scalar value and residue in the six neighbors of its old position and the six neighbors of its current position |
| Local inputs | Momentum, budget and phase for motion; one local cell record for each scheduled halo operation |
| Evolving state | Existing particle, cell, budget and phase records; no source identity map or history |
| Parameters | Existing positive `c_units`; no angle-specific or speed-specific branch |
| Outputs | Zero or one hop, updated phase and budget; up to twelve validated local cell proposals per particle |
| Bounds | Momentum L1 sum fits one 32-bit register; products use checked 64-bit work registers |
| Timing | Every particle reads the same post-field state before the halo phase; all halo proposals validate before commit |
| Tests | 342 signed directions, six 200-tick isolated runs, exact halo cells, external seed response, two-source response, momentum and baseline comparison |

The halo phase runs after the particle phase. Clearing before particle response
would remove every gradient, including an external one. Clearing immediately
after each particle would make later particles see a different state. The
synchronous phase avoids both errors: all particles respond first, then the
engine schedules the union of the old and current six-neighbor halos. A cardinal
move has twelve distinct target cells in a normal-sized lattice. Rest or periodic
small dimensions can make targets overlap; each address receives one proposal.

This scheduling has host work proportional to the number of particles, just as
the existing particle phase does. Each particle contributes at most twelve local
targets, every local transformation takes one fixed cell record, and the state
stored per cell and particle is unchanged. It therefore preserves the fixed
local O(1) physical bound for fixed K. No world object, remote search, shadow
simulation, source history or per-source field map enters the halo calculation.

## Balanced integer movement

For hop index n and weights a,b,c with total T, the x count is floor(n*a/T).
The other n-floor(n*a/T) hops are distributed between y and z using the same
integer construction. Three absolute values, fixed arithmetic and at most two
axis decisions are needed. The existing phase stores n modulo T.

For constant momentum and phase initially zero, x error is less than one lattice
cell and y/z error is less than two cells on an unwrapped chart without blocked
moves. This is a bounded digital staircase rather than exact rotational
invariance. Coordinate priority remains explicit. Momentum changes reuse phase
modulo the new total.

## Reproduction and measured results

Run `PYTHONPATH=src python tools/check_diagonal_motion.py`. It uses the existing
full 3D GIF/HTML renderer, writes JSON measurements, and exits nonzero if any new
candidate case changes isolated momentum or exceeds the digital-line bound.

| Run | Measured result |
| --- | --- |
| Legacy, source off, p=(600,400,0), cap=1000, 30 ticks | Displacement (30,0,0); grouped-axis control fails the line bound |
| Candidate, source off, same momentum | Displacement (18,12,0); unchanged momentum |
| Candidate, source=64, same momentum | Same displacement and unchanged momentum |
| Candidate, source=64, p=(6,4,0), cap=12, 72 ticks | Unchanged particle momentum; test passes |
| Candidate, source=64, p=(1,1,0), cap=12, 72 ticks | Unchanged particle momentum; test passes |

The focused suite additionally runs six signed 3D directions for 200 ticks.
The previous balanced-motion implementation without the halo changes p=(1,1,0)
to (1,-1,0) by tick 8 under the same strong-coupling input; the candidate keeps
(1,1,0). A seeded external field still changes a resting particle to momentum
(101,0,0) within two ticks. The contact pair first responds at tick 18 with
momenta (3,1,0) and (-3,-1,0), so the local cancellation does not remove all
external interaction. Total particle-plus-field momentum remains exact in the
tested runs.

## Scope of the result

The rule implements the proposed moving local exclusion zone. It cancels the
combined scalar value in those cells rather than identifying a source-specific
component, because the five-register scalar cell contains no source identity.
Consequently it changes how external scalar fields propagate through a
particle's immediate halo. The tests establish that an adjacent seeded field
and the contact scenario still act; they do not establish an unchanged force
law at every distance, density or boundary.

The candidate preserves integer arithmetic, local bounds and tested momentum.
Energy conservation, continuum rotational invariance and equivalence to a known
physical self-field regularization remain unestablished. These are model limits,
not exceptions to the passing isolated-motion contract.
