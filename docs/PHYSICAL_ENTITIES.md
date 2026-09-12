# Physical entities and discrete support

The [quantum-mode definitions](QUANTUM_ENTITIES.md) give every current entry a
finite quantum preparation. The inventory's missing physical dynamics remain
missing: register dimensions and working quantum channels are not a Standard
Model field theory or a derivation of particle properties.


The entity inventory is [catalog.json](../examples/known-entities/catalog.json).
It contains descriptive metadata and explicit executable representation profiles,
not a raw simulator initialization file. The [catalog adapter](ENTITY_CATALOG.md)
compiles selected profiles into ordinary initialization JSON. No catalog label
selects a hidden engine law. All 46 entries have bounded representation probes;
their actual physical dynamics and emergence remain separately unestablished.

The scope is the established particle/field families and selected useful
composites, together with explicitly unresolved or hypothetical entries. It is
not an assertion that every entity in nature is known or implemented.

## Elementary rules first

For new emergence experiments, generate the next state using simple local vector
operations: copy, transfer, add, exchange and reverse components. Read only the
node's owned state and completed inputs on its six ports. Do not insert a known
force equation, Maxwell update or elastic-collision formula and then claim that
it emerged. Fixed integer timing and rational allocation parameters define the
experiment; they do not constitute a derived physical law.

Local guards and invariant checks can compare values and use vector dot products.
They reject invalid proposals; they do not calculate a replacement state from a
target continuum equation. Physical equations may be independent external
validation targets. A successful finite example establishes only its stated
local mechanism and measured outcome.

The older [unequal-mass collision](../examples/known-entities/collision.json)
contains a configured elastic formula. It remains a reference benchmark, not
evidence that the new elementary rules derived that formula. The new examples
below do not use it to generate their updates.

## What can currently be represented

| Physical entity | Discrete representation available | Dynamics still required |
| --- | --- | --- |
| Electromagnetic field | One logical group containing signed electric and magnetic three-vectors | Compatible local electric/magnetic evolution, Gauss constraints, charge/current coupling and field energy/momentum exchange |
| Photon | A directed packet can be a ray proxy | A quantum excitation, quantized emission/absorption, polarization statistics and matter coupling |
| Strong gauge field and gluons | Internal components can be cataloged | Gauge transport, color transformations, non-Abelian interactions and confinement |
| Weak fields and W/Z particles | Scalar/vector placeholders can be stored | Electroweak structure, chirality and species-changing interactions |
| Higgs field | A scalar fluctuation can be represented | The full Higgs field structure, symmetry breaking and mass-generation mechanism |
| Quark and lepton fields | Classical records can carry selected charges and momentum | Spinors, quantum statistics, internal symmetries and their dynamics |
| Classical gravity | Scalar candidate data or grouped components can be stored | A derived Newtonian limit or a metric-based gravitational law and matter response |
| Computational Field | The project's scalar field/cost interfaces | Its proposed connection to gravity and physical time remains a hypothesis |
| Composite matter | Whole records can represent bodies | Binding, internal structure and effective behavior from constituents |

The physical classification follows the [CERN Standard Model overview](https://home.cern/science/physics/standard-model/)
and the field descriptions in [Tong's QFT lectures](https://davidtong.org/pdfs/teaching/quantum-field-theory/qft.pdf).
Gravity uses a distinct geometric description in
[Tong's GR lectures](https://davidtong.org/pdfs/teaching/general-relativity/gr.pdf).
The electromagnetic split is observer-dependent; it does not create two
independent fundamental fields. An electric-only configuration is a valid
special regime, not another field family.

The current runtime admits at most 16 configured fields and 16 disturbance
types per experiment. Each field has one or three components. Listing spin,
color or tensor components in a catalog does not implement their transformation
laws or enlarge the engine's bounded schema. A full particle inventory need not
be instantiated in every node or every run.

## Matter and antimatter

Corresponding massive particles and antiparticles have equal positive mass.
Their additive charges are conjugated; antimatter is not negative mass.
The catalog encodes electric charge in thirds of the elementary charge and spin
in doubled units, so metadata can remain integer-valued. These identifiers do
not supply spin dynamics. See [CERN's antimatter overview](https://home.cern/science/physics/antimatter/).

Neutral does not imply self-conjugate: neutron and antineutron remain distinct.
The neutrino/antineutrino entries describe the observed sectors without deciding
the unresolved Dirac/Majorana question; see the
[PDG neutrino review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-neutrino-mixing.pdf).

The engine can store positive masses and opposite charges. The optional
[local conversion interface](LOCAL_CONVERSIONS.md) can now replace two record
types with two configured output types, with full assignments and exact declared
balances. Arbitrary product counts and physical annihilation are unsupported.
Removing opposite charges is not annihilation:
products must carry the full applicable energy, momentum and charges. Rest mass
is conserved in the restricted mechanical examples, not a universal invariant
for matter/radiation reactions.

## New executable probes

| Input | Elementary operation | What its result can establish |
| --- | --- | --- |
| [discrete-pair.json](../examples/known-entities/discrete-pair.json) | Two equal-mass classical charged proxies exchange their momentum vectors at a selected head-on contact | Positive masses and opposite charges persist; the vectors reverse for the symmetric input while their total and squared-norm sum remain unchanged |
| [field-channel.json](../examples/known-entities/field-channel.json) | A node moves two transverse vector payloads into one chosen outgoing port, retaining zero | Each payload has one owner and arrives only after the full link time; two-component representation works without a neighboring-state read |

The pair is a restricted non-annihilating classical model, not an electron/positron
scattering prediction. Its fixed approach direction and equal masses are explicit
assumptions. Its rate is selected as a rational transport parameter; general
mass-dependent motion has not been derived from this example.

The field probe selects a direction. It does not establish isotropic light
propagation, Maxwell waves or quantum photons. An isolated packet may preserve
its squared amplitude under translation; this does not prove conservation of
physical field energy when packets overlap. Field component sums and physical
energy/momentum are different quantities.

Run with the existing CLI, using a new output directory each time:

```bash
python -m event_universe --init examples/known-entities/discrete-pair.json --output artifacts/discrete-pair --visualize
python -m event_universe --init examples/known-entities/field-channel.json --output artifacts/field-channel --visualize
```

The old `known-entities/run.py` wrapper runs its original five benchmarks only.
It does not consume the catalog or these two inputs. Use the explicit commands
above to obtain the recorded HTML for the new probes.

## Conditions for claiming classical physics

| Target | Necessary evidence beyond storing its variables |
| --- | --- |
| Free mechanics | Rest stability, retained momentum, causal motion and independently measured displacement versus mass and momentum |
| Elastic interaction | Energy and momentum balance for different masses and geometries, with outcomes generated by elementary local operations |
| Charge continuity | Each node's charge change matches actual incoming/outgoing charge transport, including link ownership |
| Electromagnetism | Preserved electric/magnetic constraints, transverse modes, dispersion and orientation tests, consistent matter exchange |
| Gravity | A measured distance dependence, source response and appropriate limiting behavior from the chosen local field rule |
| Fluids and composite bodies | Effective stress, transport and thermodynamics from actual local interactions, not labels |
| Emergence | A derivation from the discrete rule plus independent experiments across initial conditions, orientations and scales |

Charge-preserving discrete coupling is a substantive structural requirement;
see this [primary geometric particle/grid method](https://arxiv.org/abs/1409.0854).
It is a reference for acceptance criteria, not a bounded-integer implementation
already present in Universe24.

Comparing matching local experiments on 9-cubed and 15-cubed lattices tests
independence from the total domain before boundaries can influence the result.
It does not prove a continuum limit. Increasing domain size at fixed cell size
and decreasing cell size at fixed physical scales are different experiments.
Large-scale emergence requires a defined mapping of lattice units and additional
long-wavelength evidence; no dimension-dependent repair is permitted.

The necessary automated checks are in `tests/test_physical_entities.py`.
Status fields distinguish representation, configured dynamics and emergence.
No new catalog entry is marked as a completed derivation of a physical field.
