# Physical scenario coverage

This map distinguishes executable representations, acceptance of a supplied
candidate law, and agreement with an independent physical target. A green test
suite is not a statement that every catalog entity has physical dynamics.
The source audit began at main `992e0006469bb1156f517ae8273a80a980df7c57`.
The test extensions in this change leave all runtime laws and initializations
unchanged. See [test expectations](TEST_EXPECTATIONS.md) for numerical contracts.

## Model and scenario matrix

| Family | Distinct scenarios and evidence | Physical interpretation and remaining gap |
| --- | --- | --- |
| Catalog: 11 fields and 35 particle/multiplet entries | [Classical profiles](../tests/test_entity_compiler.py) compile all 46; composed charged carriers/vector fields and a four-scalar field actually run. [Quantum profiles](../tests/test_quantum_entities.py) run all 46 finite preparations, including different dimensions and occupations. | Representation coverage. Most classical profiles are copy/transport probes; finite quantum preparation does not supply a species Hamiltonian, statistics or interactions. There is no all-species interaction matrix. |
| Massive rational carriers | [Rational tests](../tests/test_rational_particles.py): seven distinct mass/charge pairs, rest and all six signed directions, fractional p/m, every-tick resident positions, periodic seams and unequal domain extents. | Supplied nonrelativistic free-motion benchmark. With p/m = +/-1/3 and twelve ticks per time unit, each completed hop takes 36 ticks. This does not derive relativistic dispersion or interactions for seven species. |
| Massless rational carrier | Same suite: axis and 3:4 directions in all signed coordinate planes, actual receive events and final resident positions, mass-shell rejection. | At the selected c=1/2, 100 ticks give 50 Euclidean cells. This covers selected representable directions; it does not establish isotropy at the six-port causal maximum or a quantum photon law. |
| Two-body contacts | [Physical entities](../tests/test_physical_entities.py), [rational tests](../tests/test_rational_particles.py), [small-space cases](../tests/test_small_space_experiments.py): equal/unequal masses, independent center-of-mass prediction, rest, separated/outgoing controls, size/axis changes and rejection outside a restricted candidate. | Supplied classical elastic contacts preserve decoded p and p-squared/(2m) in their accepted regimes. No general impact-parameter scattering, cross section, annihilation or relativistic collision law follows. |
| Particle with local E/B pulse | [Local response](../tests/test_local_lorentz_field.py): negative, positive and zero charge; rest, no field, parallel velocity/B, electric only, six signed transverse directions, oblique mixed fields, one/two-tick links and low budget. All three probes and opposite field reactions are checked each tick. | One-shot held probes verify the configured impulse q(E+v cross B), causal arrival and paired momentum. They do not test moving magnetic orbits or physical field energy. The magnetic energy counterexample below remains a failure of that stronger target. |
| Generic field/carrier turning | [Spatial coupling](../tests/test_spatial_coupling.py), [joint interactions](../tests/test_spatial_interactions.py), [budget](../tests/test_spatial_coupling_budget.py): signed axes, ordered noncommuting turns, residuals, local reaction, delayed atomic commits, overflow and renamed quantities. | Exact quarter-turn candidate and configured conservation. Norm preservation alone is not total momentum conservation; periodic/turning self-field identification remains open. |
| Finite emission and decay | [Decay](../tests/test_spatial_decay.py), [finite engine](../tests/test_finite_spatial_engine.py), [open boundaries](../tests/test_open_boundaries.py): signed/unsigned stock, smallest quantum, exhausted source, all six exits, in-flight ownership and recorded losses. | Accounting includes sources, dissipation and escape. Remaining physical inventory is not conserved in a dissipative model; these tests do not establish vacuum field decay. |
| Transverse directional wave | [Directional waves](../tests/test_directional_wave.py): unequal/equal, solitary, coincident electric/magnetic, dark aggregate, six-way encounter, 24 proper cubic rotations, periodic return and two transit times. | Configured polarization rotation preserves mode energy U and directional P. It is nonlinear and is not Maxwell propagation, matter coupling or a photon interaction law. |
| Six-population Maxwell candidate | [Reflection tests](../tests/test_maxwell_configuration.py): exact reflection/involution, integer failure, one-link ownership, frequency estimator and a compact divergence-free curl counterexample. [Separate experiments](../examples/maxwell/README.md) compare axial/oblique wavelengths, polarizations, no-scattering and longitudinal controls. | Conditional long-wavelength agreement was reported by that experiment. Exact centered Gauss conservation and instantaneous macroscopic EM energy fail. Historical frequency measurements retain their recorded source identity; this audit does not relabel them as new runs. |
| Finite quantum evolution | [Channels](../tests/test_quantum_channels.py), [event network](../tests/test_quantum_event_network.py), [native channels](../tests/test_native_quantum_channels.py): coherent/phase-reversed/dephased/partially dephased controls, dense exact reference, grouped outcomes, CHSH and unchanged unconditional marginals, local priced execution. | Finite quantum information identities and a supplied classical Markov limit are tested. No species-specific scattering, full QFT, gravity or Newtonian trajectory emergence is established. |
| Native contact and detectors | [Native runtime](../tests/test_native_event_runtime.py), [contact](../tests/test_quantum_contact_trial.py), [detectors](../tests/test_quantum_detector_trial.py): deterministic and probabilistic branches, repeated encounters, no-transfer outcomes, local trigger, cost and invalid-input controls. | Configured instruments and trajectories. A definite recorded branch does not itself derive the quantum-to-classical transition. Native event programs cannot be combined with ordinary spatial fields in the current schema. |
| Observation, locality and genericity | [Observer](../tests/test_local_observer.py), [cell contract](../tests/test_cell_state_contract.py), [identity](../tests/test_generic_identity.py), [locality](../tests/test_locality.py): delayed receptions, unchanged state/cost, renamed/reordered scalar/vector fields and formula-free payloads. | Software and model constraints. Passive playback, labels or balanced counters cannot certify physical laws. |

Historical scalar, linked, balanced and causal-stream candidates remain separate
owners. Their [regressions](../tests/test_regressions.py),
[collision](../tests/test_collisions.py),
[balanced-motion](../tests/test_balanced_movement.py) and
[causal-stream](../tests/test_causal_stream.py) results do not certify the active
initialization-defined model.

## Reproduced physical counterexamples

For the held electron probe with m=100000, initial p=(100000,0,0), E=0 and
B=(0,0,300000), the configured one-shot impulse gives p=(100000,300000,0).
Classical kinetic energy rises from 50000 to 500000 while joint momentum remains
exact. A purely magnetic Lorentz force does no work on a moving charge; this
finite impulse is therefore insufficient as an energy-preserving magnetic
orbit integrator. See the [MIT electromagnetism notes](https://web.mit.edu/8.02t/www/802TEAL3D/visualizations/coursenotes/modules/guide08.pdf)
and the narrower [local pulse contract](LOCAL_LORENTZ_FIELD.md).

The Maxwell test seeds the centered curl of a compact integer Z potential.
Its initial centered electric divergence is exactly zero. One field tick makes
it nonzero while population norm stays fixed. A test that reproduces this
counterexample guards the evidence; its passing status is **not physical
acceptance of Gauss conservation**. Do not replace a required physical acceptance
test with a counterexample test or mark the physical target passed.

## Review protocol for every contributor

For an affected family, record model identity, source revision, units, initial
conditions, independent target and the exact tests that exercise it. Cover
physically distinct regimes that matter to the claim: isolated versus interacting,
zero versus nonzero field, charge/sign, orientation/polarization, rest versus
motion, contact versus no contact, transit, budget, boundary and finite capacity.
An axis irrelevant to a model may be explicitly inapplicable; unsupported physics
is a gap, not an inapplicable or passing case.

Choose representative distinct laws and parameter regimes, rather than a full
Cartesian product of labels. Compilation or a renamed repeat cannot replace a
missing field/particle interaction test. Check actual received/resident motion
as well as outgoing routing. Check total physical ownership across participants,
fields and links, with explicit source/loss/escape terms when applicable.

Establish expectations outside the engine evaluator: analytic examples, exact
host references or a justified experimental target with units and tolerance.
Relativistic particle claims require a declared dispersion relation and
four-momentum consistency, not only balanced arbitrary registers; see
[PDG kinematics](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf).
Quantum channels require complete maps, normalization and appropriate retained
correlations; see [IBM channel representations](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels).
Agreement with such a supplied law is still distinct from emergence of that law.

Use `python tools/check.py --tests` with the affected suites above for a cross-family
audit. Normal development keeps the default affected selection. Inspect dynamic
JSON and experiment-script consumers: static import analysis alone cannot select
all their tests. Report code checks, physical target outcomes and not-run gaps
separately. Record runtime fingerprints before/after, keep runs headless, and
lease generated evidence under the existing [retention policy](RETENTION.md).
Recheck changed open PR heads independently; their results are not main results.
