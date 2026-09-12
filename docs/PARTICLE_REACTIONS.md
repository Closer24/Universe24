# Generic particle reaction contract

Universe24 may use established particle identity as **data** without adding a
species branch to the engine. `event_universe.particle_reactions` is a host-side
authoring adapter that reads the existing entity catalog, validates a bounded
reaction description and compiles it into the ordinary initialization-defined
local conversion path.

The engine still sees only four role types, three integer fields and one generic
pair transaction. Renaming `electron`, `positron` or `photon` while preserving
their catalog properties produces the same compiled physical initialization.
Adding another established particle with the same catalog identity contract does
not require engine code.

## Physical source boundary

Particle identities are checked against the catalog metadata, whose established
particle classifications are sourced from the Particle Data Group and CERN. For
this contract the current external references are:

- [Particle Data Group 2026 particle properties](https://pdg.lbl.gov/2026/listings/particle_properties.html)
  and [2026 summary tables](https://pdg.lbl.gov/2026/tables/contents_tables.html);
- [CERN Standard Model overview](https://home.cern/science/physics/standard-model/);
- [CERN antimatter overview](https://home.cern/science/physics/antimatter/);
- [PDG tests of conservation laws](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-conservation-laws.pdf),
  revised October 2025 and carried in the current PDG review index.

The adapter uses these **known identity facts already represented by the catalog**:

- reciprocal particle/antiparticle identity;
- electric charge in integer thirds of the elementary charge;
- doubled spin as integer identity metadata;
- self-conjugate versus distinct-antiparticle status;
- the catalog rest-mass relation tag, such as `massless` or
  `equal_positive_pair`.

Odd `twice_spin` is reported as the fermion statistics class and even
`twice_spin` as the boson class. This is an identity classification only. The
adapter does not implement antisymmetric fermion exchange, bosonic
symmetrization, Pauli blocking, polarization dynamics or a species Hamiltonian.
Those remain quantum-dynamics work.

## What is conserved

Every compiled reaction owns exactly these runtime fields:

| Field | Shape | Meaning | Runtime rule |
| --- | --- | --- | --- |
| `charge` | scalar | electric charge in units of one third of `e` | exact conserved sum |
| `energy` | scalar | explicitly configured integer reaction-energy inventory | exact conserved sum |
| `momentum` | three-vector | explicitly configured integer momentum inventory | exact component sums |

The authoring adapter checks the same three totals before it emits an
initialization. The ordinary local interaction then marks all three fields
`conserved: true` and repeats them as pair invariants. A tampered or otherwise
imbalanced runtime proposal is rejected atomically; no partial type replacement
may commit.

`energy` is deliberately an explicit inventory. This contract does **not** derive
`E(p,m)`, use a square root, infer rest energy from a particle name or insert a
continuum kinematic formula. A future derived dispersion law must be a separate
candidate that obeys the integer-operation contract.

Electric charge is always enforced by this particle-reaction contract. Baryon
and lepton numbers are **not** silently promoted to universal exact invariants:
the PDG conservation review distinguishes gauge-rooted charge conservation from
baryon/lepton symmetries that can be violated in extensions and, for lepton
number, depend on unresolved neutrino physics. A future reaction family may add
explicit bounded quantum-number data and an interaction-specific conservation
policy, but it must not pretend those open questions are settled.

## Current reaction shape

The current runtime conversion owner supports exactly two local input records and
two local output records. Therefore this adapter accepts exactly `2 -> 2` species-
changing reactions. The two output roles may describe the same catalog particle,
so the contract can represent the ownership pattern

```text
electron + positron -> photon + photon
```

without any `if electron` or `if photon` code. It does **not** yet support `1 -> 2`,
`2 -> 3`, arbitrary particle multiplicity or an unbounded Fock-space population.
Those require a separate bounded product-ownership extension.

## Electron/positron to two photons probe

[`electron-positron-to-two-photons.json`](../examples/known-entities/electron-positron-to-two-photons.json)
uses the established catalog identities and an explicitly supplied symmetric
integer energy/momentum example. The input electric charges are `-3` and `+3`;
the two photon outputs have charge zero. Configured total energy is 10 on both
sides and total momentum is `(0,0,0)` on both sides.

This demonstrates that known particle identity can select data and that a local
species-changing transaction preserves the declared laws. It is **not** a claim
that Universe24 has derived QED annihilation, its cross section, its angular
distribution, the electron dispersion relation or photon creation from a deeper
field law.

Compile it with:

```bash
python -m event_universe.particle_reactions \
  --catalog examples/known-entities/catalog.json \
  --reaction examples/known-entities/electron-positron-to-two-photons.json \
  --output-init artifacts/electron-positron-reaction/init.json \
  --output-manifest artifacts/electron-positron-reaction/manifest.json

python -m event_universe \
  --init artifacts/electron-positron-reaction/init.json \
  --output artifacts/electron-positron-reaction/run
```

Both outputs are ordinary validated files. Generated artifacts remain outside the
repository under the retention policy.

## Acceptance

The focused tests require:

- catalog charge/spin/antiparticle relations to be internally consistent for every
  selected participant;
- electron and positron to classify as fermions and photon as a boson from their
  integer spin metadata;
- charge, configured energy and momentum to match before and after compilation;
- the runtime conversion to keep those totals exact while the output records move;
- compile-time rejection of a nonconserving charge, energy or momentum proposal;
- runtime rejection of a compiled initialization that is deliberately tampered
  after authoring validation;
- identical compiled physics after arbitrary species renaming; and
- successful compilation of a new catalog particle added as data only, without a
  new engine branch.

Passing these tests establishes a generic bounded conservation/ownership
interface. It does not establish the physical interaction law that determines
which reaction occurs or with what probability.
