# Generic particle reaction contract

Universe24 uses established particle identity as **data** while the active engine
owns one bounded local reaction mechanism. `event_universe.particle_reactions`
validates catalog facts and compiles reaction-version 1 or 2 descriptions into
ordinary initialization. No species name selects a runtime equation.

## Bounded n-to-m configuration

Initialization may contain `reactions`. Each rule declares `input_types`,
`output_types`, complete output `assignments`, optional scalar `invariants` and an
optional `when` expression. Input field expressions use an integer `participant`
index. A reaction supports one through eight local input records and one through
eight local output records, subject also to `slots_per_cell`. Eight is a software
capacity bound, not a proposed law of nature.

All selected inputs are already resident at one event location. A rule consumes a
disjoint set of matching records once per local cycle. Outputs reuse consumed
slots first and then empty local slots. If output capacity is unavailable, or an
assignment, invariant, integer bound or conservation check fails, the transaction
fails before commit and no input is discarded. Outputs from one rule may enter a
later explicitly configured rule in the same local cycle; they cannot recursively
re-enter the same rule during that cycle.

The existing pair `interactions` interface remains unchanged for legacy paired
assignments. `reactions` is the bounded variable-multiplicity owner.

The native quantum event binding accepts the same bounded physical participant
count for a trigger. The quantum instrument remains explicitly configured; adding
more physical participants does not by itself define a new Hamiltonian or a
many-register quantum operation.

## Particle facts and conserved fields

The catalog supplies reciprocal particle/antiparticle identity, electric charge
in integer thirds of the elementary charge, doubled spin, conjugacy status and a
rest-mass relation tag. Odd doubled spin is reported as fermion identity metadata
and even doubled spin as boson identity metadata. This classification does not
implement exchange antisymmetry, Pauli blocking or bosonic symmetrization.

The particle adapter compiles three exact conserved runtime inventories:

| Field | Shape | Runtime meaning |
| --- | --- | --- |
| `charge` | scalar | electric charge in thirds of the elementary charge |
| `energy` | scalar | explicitly configured integer reaction-energy inventory |
| `momentum` | three-vector | explicitly configured integer momentum inventory |

The adapter checks these totals before compilation and the generic engine checks
them again at the local transaction. `energy` is not a derived relativistic
`E(p,m)` relation. Baryon and lepton numbers are not silently made universal exact
invariants; a reaction family can add explicit bounded invariant data when that
physical claim is justified.

## Physical probes

`electron-positron-to-two-photons.json` remains the version-1 two-to-two ownership
probe. `electron-electron-scattering.json` uses the same generic engine for the
known electron-electron elastic-scattering topology: two fermionic electron inputs
remain two electron outputs while charge, configured energy and momentum are exact.
The integer momenta are a symmetric conservation example, not a QED cross section,
angular distribution or derived dispersion relation.

`muon-decay.json` is a version-2 one-to-three topology probe for the known weak
decay `mu- -> e- + anti-nu_e + nu_mu`. It validates the catalog identities and
local ownership of three products while preserving the represented charge,
configured energy and momentum. The chosen integer energy/momentum partition is a
software test point, not the physical decay spectrum or lifetime.

A separate generic test exercises `3 -> 2` with anonymous disturbance types. It
exists to validate the engine contract rather than assert a new physical process.

## Acceptance limits

The focused tests require exact compile-time and runtime conservation, atomic
failure, species-name independence, same-species electron inputs, one-to-three
product ownership, a generic three-input transaction and explicit capacity
failure. Passing them establishes bounded local reaction plumbing only. It does
not derive which reaction occurs, its probability, its interaction strength, its
angular distribution, a species Hamiltonian, or quantum field creation operators.
