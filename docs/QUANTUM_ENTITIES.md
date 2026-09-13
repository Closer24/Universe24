# Finite quantum registers, channels and entity profiles

## Scope and ownership

`local-quantum-events-v2` extends the selected native event program. The same
`Simulation`, causal ledger, quantum owner, local resolver and classical planner
execute it. It adds no physical-name dispatch or second simulator. The binary
`local-quantum-events-v1` input and existing pure-state APIs remain compatible.

`quantum/event_rules.py` owns finite bases and complete local maps;
`quantum/mixed.py` owns exact density-operator arithmetic. `event_network.py`
retains deferred dependencies, conditional constraints and checkpoints.
`integration/event_program.py` validates serialized definitions.
`integration/quantum_entities.py` compiles explicit catalog profiles; `entities.py`
selects the representation without interpreting physical species. Definitions
belong to the shared owner, not to individual physical nodes.

## Register definition

A register has an in-domain address, dimension 2, 3 or 4, and an initial basis
level. Optional `register_names` distinguish multiple degrees of freedom at one
node; names select no update law. With repeated addresses, every register must
have a distinct bounded name. A binding there must specify its `register_index` index.
Different registers at the same node are different degrees of freedom, not cloned
copies of a particle. Operations between colocated registers are local and do not
pay a fictitious neighbor transit. Actual neighbor operations still respect link
travel time. Distant operations are rejected.

`dimensions` defaults to binary. `initial_levels` and nonempty `occupied` are
mutually exclusive. Basis keys use little-endian mixed radix; binary defaults keep
all existing keys. The product of dimensions must fit the existing signed integer
register, and there are at most 30 registers. These limits do not promise that the
full joint state is affordable. Sparse-state and density-entry limits still apply.

Coherent matrices act on one or two registers (dimension at most 16) and satisfy
`U* U = s I` for a positive common integer scale. A complex coefficient remains a
pair of bounded signed integers. The scale is implicit, not rounded by a root.

## Unobserved operations and grouped measurement

A local operation supplies exactly one `matrix` or `channel`. A `channel` is one
to four same-size Kraus matrices on one register, satisfying
`sum(K* K) = s I`. It appends a recipe and does not sample any result. Its update
is the incoherent sum `sum(K rho K*)`, not a coherent sum of amplitude vectors.
This distinction preserves interference within a term without inventing
interference between inaccessible environment records.

A binding supplies either the existing `instrument` (one Kraus matrix per
outcome) or `grouped_instrument` (one to four observable outcomes, each with one
to four indistinguishable Kraus terms). Completeness is checked across ALL terms.
Only the observable outcome is sampled. Its continuation retains the density sum
for its full group. A one-outcome instrument needs no RNG even if it has several
Kraus terms. Do not select a hidden term and present it as a measured event.

Pure states retain the sparse amplitude fast path. A channel or grouped outcome
can promote a component to an unnormalized sparse density numerator. Normalize
only implicitly by its common trace. Remove only a single common integer factor
from the WHOLE state. Never independently normalize terms before adding them.
Trace, intermediate coefficients and term capacities remain checked.

`joint_density()` is a read-only host diagnostic. Passing selected register indices
computes their partial trace; it is not a physical remote read or a sufficient
checkpoint of an entangled component. `joint_state()` does not invent a wave for
a density representation and fails explicitly instead. An exact checkpoint stores
the complete live connected component, including mixed-state information.

A discarded environment cannot later be coherently recovered with an inverse
system operation. Retain its explicit quantum register when reversal or a later
return matters. No universal interaction-to-record trigger follows from this API.

## Entities: explicit finite preparations

Each of the original 35 particle/multiplet entries and 11 field families has a
`quantum_profile` in the explicitly supplied
[representation-probes.json](../examples/known-entities/representation-probes.json).
The physical reference catalog contains no executable profiles. Its additional
disturbance families have no default preparations. Every supplied profile declares
`finite_mode_representation`, mode names, basis labels, initial levels,
assumptions and missing dynamics.

- Fermion modes have occupation 0 or 1. Charged leptons and nucleons select two
  spin modes; quarks select two spin modes for each of three color labels.
  Neutrino entries select one helicity mode, not a complete massive-neutrino theory.
- Bosonic modes are truncated at occupation 2. Photon entries select two transverse
  modes; massive vector entries select three spin modes. The gluon multiplet
  selects sixteen adjoint/polarization modes without implementing gauge dynamics.
- Scalar and representative field-family profiles select finite modes. Hypothetical
  metric, computational and dark-sector entries use abstract two-level registers
  without assigning particle statistics and explicitly retain hypothesis status.
  The whole field family is not represented by one selected mode.

The compiler never infers a Hamiltonian, interaction coefficient, dispersion law
or gauge constraint from these names. Fermion occupancy alone does not implement
antisymmetry or parity superselection; a declared exchange-sign operation can be
represented, but parity, charge and number conservation must be specified by the
selected laws and reservoirs. Bosonic truncation is not a physical upper bound;
no exact canonical infinite-oscillator commutator or ladder law is claimed.

The generic `operations.py` builders provide basis projectors, dephasing, signed
permutations and directed level-transition instruments. A level transition is NOT
an automatically energy-balanced particle-creation process. Its no-transition
branch is included. All builders produce the same checked matrix data.

```sh
python -m event_universe.entities --catalog examples/known-entities/catalog.json --profiles examples/known-entities/representation-probes.json --entity electron --entity positron --entity electromagnetic_field --representation quantum --output-init artifacts/quantum-preparation.json
python -m event_universe --init artifacts/quantum-preparation.json --output artifacts/quantum-preparation
```

The preparation is held and unmeasured until explicit operations are supplied.
There are no phantom classical bodies; its required placeholder carrier type is
unoccupied. Compatible selected modes compose within fixed bounds. Requesting
all entries in one finite world fails instead of silently increasing capacity.
The default `--representation classical` preserves the previous compiler behavior.

## Costs and the classical comparison

The native classical path is still charged once per begun cycle, including the
selected branch and resolver overhead. Waiting does not resample or charge twice.
The oracle remains one modeled operation with zero direct added world ticks.

Deferred channel evaluation and density storage are additional host work, not
free computation. Density entries can grow quadratically relative to a sparse
pure state; an over-budget calculation fails. Query node counts do not count CPU
instructions or full diagnostic/checkpoint work. Scheduled channels, like earlier
coherent recipes, do not introduce a new physical propagation-cost law. The
classical path ledger does not model quantum-environment energy or workload.

Independent `spatial_fields` clocks remain incompatible with this event program.
No rejection guard was removed to suggest that every field is now quantum.

## Experiments and independent checks

```sh
python examples/quantum/run_physics_checks.py --output artifacts/quantum-physics --visualize
python tools/check.py --base origin/main
```

Use fresh output paths. Omit `--visualize` for headless results. The harness uses
the canonical runner and existing HTML player, no GIF or independent trajectory
renderer. Inputs and complete event/cost/state evidence remain in the output.

Expected finite predictions are separate from update data:

| Experiment | Independent target |
| --- | --- |
| Coherent split and recombination | Transmission 1, reflection 0 |
| Relative phase reversal before recombination | Transmission 0, reflection 1 |
| Complete discarded basis record | Transmission 1/2, reflection 1/2 |
| Channel `[3I,4P0,4P1]` before recombination | Transmission 17/25, reflection 8/25 |
| Bell pair with rational measurement settings | CHSH 14/5; both unconditional marginals 1/2 |
| Rotation with a discarded basis record each step | Exact two-state classical Markov probabilities |
| Native classical endpoint and cost-limited run | Existing paths, costs and local delays retained |

The tests also compare 72 successive states to a separate dense rational evaluator,
check mixed checkpoints, complex phases, qutrits, grouped outcomes, local support,
capacity failures, catalog coverage, and an observable signed-exchange difference.
A simulated CHSH violation is not a loophole-free experiment on nature. Finite
classical compatibility is not a derivation of Newton's laws. These outcomes
support the declared finite quantum mechanics and software composition only.

Primary physical acceptance references:
[IBM channel representations](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels),
[IBM general measurement formulations](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/formulations-of-measurements),
[IBM CHSH tutorial](https://quantum.cloud.ibm.com/docs/en/tutorials/chsh-inequality),
and [Tong on fermions](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S5.html).
Species metadata retains the catalog's existing primary sources.
