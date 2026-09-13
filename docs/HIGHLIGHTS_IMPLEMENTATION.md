# Highlights implementation coverage

## Quantum time-direction clarification - 2026-09-13

Highlights sections 1.2.7 and 4.7 distinguish direct origin relevance lookup
from deferred quantum evaluation. Neither is reverse physical-time computation.
Required stored dependencies and recorded constraints are collected as bounded
host work; their recipes evaluate forward from sources or exact checkpoints.
Earlier events and outcomes are not rewritten or resampled.

This terminology review uses merged main
`63983788140bc06d5e8f581e3609c0520c00f43b` and the latest reported
`Quantom -> Classic` run in [PR #91](https://github.com/Closer24/Universe24/pull/91),
head `49bcbc74c69a47814945efce8600edbc824ee04f`. PR #91 was open and unmerged
at review. Its `local-quantum-events-v3` candidate removes separate chronological
predecessor lists and `history(register)` traversal, while retaining immutable
events and quantum dependencies. Direct event-ID/status lookup is O(1); full
retained-state evaluation and cancellation certification are separate host work.
Source resolution adds a later write-once status without rewriting the source.

The PR reports `wave_origins.json` completing 5/5 ticks in 0.0123118 seconds:
one outcome draw, origin 3 resolved at tick 2 to record 13, peer references retired
at tick 3, and origin 4 still active. Three oracle calls include two cancellation
certifications. These are branch-reported results, not a new experiment in this
documentation task or proof of a universal quantum-to-classical limit.
See [the quantum contract](QUANTUM_EVENTS.md#time-direction-and-origin-lookup).
The Google Doc receives the same clarification in sections 1.2.7, 4.7.2 and 4.7.7.
No reaction law or evaluation algorithm changes in this correction.

## Latest synchronized snapshot - 2026-09-13

This is the repository implementation map for
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit),
not a second specification or an automatic live mirror. Both this map and the
Google Doc were reconciled against main
`cc042ce6c51a34775c292371538c5cd6acd4e423`, including merged
[PR #89](https://github.com/Closer24/Universe24/pull/89),
[PR #90](https://github.com/Closer24/Universe24/pull/90) and
[PR #92](https://github.com/Closer24/Universe24/pull/92).
The older entries below retain their historical source and validation scope;
their statements that the live document was not edited refer to those earlier tasks.

### Current implementation coverage

| Highlights sections | Implemented contract and limits | Repository owner |
| --- | --- | --- |
| 2.2.1-2.2.2 | Bounded integer physical inputs and intermediates; shared SI unit/constant registry prepares Scalar/Vector values outside physical stepping. Explicit conversion errors are separate from measurement uncertainty. Model time h is not Planck action. | [Reference units](REFERENCE_UNITS.md), [architecture](ARCHITECTURE.md) |
| 3.3.4, 3.5.5, 4.3.1 | Declared aggregation, indexed local participants, joint carrier/field proposals and complete-owner conserved readouts. Nonlinear balances use actual before/after state; labels do not supply physical laws. | [Node processor](NODE_VECTOR_PROCESSOR.md) |
| 4.4.1-4.4.2 | Explicit k*h Node execution and optional shared field/carrier cost-budget timing remain separate, incompatible modes. Waiting input has bounded destination ownership. | [Node processor](NODE_VECTOR_PROCESSOR.md), [shared clock](SPATIAL_COMPUTATION_DELAY.md) |
| 4.4.3 | Emission can read the Node's last committed work. Configured received-Port response exchanges momentum with a local field register; this is not derived gravity or physical energy. | [Computational response](COMPUTATIONAL_RESPONSE.md) |
| 6.5-6.7, 10.10 | Node-owned commits, immutable worker planning, deterministic barriers and bounded physical-owner memory have scoped tests. Total host memory and full-world work are separate costs. | [Architecture](ARCHITECTURE.md), [validation](VALIDATION.md) |
| 10.3.1 | Schema 2 localizes attenuation residue by default. Explicit dissipate retains the earlier loss policy. Stationary deposits remain owned inventory and are not sampled by local rules. | [Spatial fields](SPATIAL_FIELDS.md) |
| 10.3.2 | Scalar straight-ray transport retains heading and integer routing phase; ray_slots bounds resident capacity. Unsupported vector, octant-seed, field-rule, joint-interaction and alternative-clock combinations are rejected. | [Straight-ray contract](SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1), [ray tests](../tests/test_ray_field.py) |
| 10.9, 10.11 | Sourced particle reference data, explicit representation profiles, preflight, finite quantum events and read-only observers remain distinct from verified species dynamics. | [Entity catalog](ENTITY_CATALOG.md), [project status](PROJECT_STATUS.md) |

### Merged field changes and evidence

PR #90 adds `residue: localize`, selected when a schema 2 decay definition omits
the key. At completed interior arrival, the removed fraction becomes bounded
stationary stock at the receiving Node. It is included in inventory, not
dissipation; moving flux still diminishes. Explicit `residue: dissipate` selects
the earlier loss law. Open exit, signed components, source allowances and in-flight
ownership retain their separate accounting. The 40-tick finite-source run
accounted for 720 emitted units as deposits, with zero dissipation. Tests include
signed vectors, mixed residue policies and overflow rejection without partial
receipt. Neither a component ledger nor a stationary deposit establishes physical
field energy or a gravitational law.

PR #92 adds `transport: ray` under `isotropic-ray-field-v1`. A source sweeps
configured integer headings using its emission cursor. Each ray retains its
heading index, three integer routing accumulators and amount while moving over
adjacent Links. Matching heading and phase may merge; capacity exhaustion fails.
Ray fields currently reject vector payloads, octant seeds/weights, field rules,
spatial interactions, `node_execution` and `spatial_computation_delay`.

The published [inverse-square probe](../examples/inverse-square/README.md) reports
a 41-cubed open world with 4,096 headings, 64 rays per tick and a 64-tick measurement
sweep. Finite fitted slopes are -2.25, -2.05 and -1.92 on the axis, face diagonal
and body diagonal. Angular-patch coefficients of variation are 6-8 percent over
72 patches at tested radii. This statistic is not a maximum error bound or exact
isotropy; individual nodes show greater variation. These are reported world/event
audit measurements of stock, not operational observer records or an independent
rerun in this documentation task. Scalar shell stock is not oriented surface
flux, and finite fits do not establish asymptotic scaling, mass coupling,
attraction, Newton's law or physical energy conservation.

### Unmerged amendments remain separate

The live document's section 11 contains branch-reported self-field policies,
carried allocation phase, scattering and collision results. Its cited
[PR #93](https://github.com/Closer24/Universe24/pull/93), head
`7149ec961df330b460dd3dc7262c4a98c5c17221`, was open and unmerged when checked
against the main commit above. The live section now states that scope explicitly.
Its findings are retained without being promoted to merged-main capabilities or
independently revalidated physical results. This sync does not merge PR #93.

The Google Doc update adds sections 6.7 and 10.3.1-10.3.2, reconciles the prior
decay accounting bullets, and labels section 11's branch scope. Existing Node,
unit, quantum and pending-hypothesis content is retained. Documentation-only
validation applies here; no simulator behavior or experiment input changes.

## Joint local reaction contract - 2026-09-13

The live source was reread at revision
`ANLCKQluUGX_afG63QQM9IQBX-qmjBbhP-b8UVvMJ-mCjZQ30ZYQ_Kkyk4MKp-O_P1PvMixFu3_pO-w-dDxrnekqUXbwar_XXVKECHy5vBA`.
Implementation base: `a7a0000e3005ae41b37639f5dcf76e56532be69f`.
Sections 3.1, 3.3 and 4.3 motivate the bounded property-selected
[joint Node reaction](NODE_VECTOR_PROCESSOR.md#local-rules). The user's explicit
reaction contract refines delayed execution: one group reads several carriers
and fields from one snapshot, and each frozen substep must still pass its
declared invariants and optional persistent condition before atomic commit.
Start triggers remain separate. The supplied register-rotation example checks
externally defined readouts; it does not derive physical species, energy laws or
quantum behavior. No live Highlights text was edited.

## Integer Node timing reconciliation - 2026-09-13

The live Highlights source was read again with modification timestamp
`2026-09-13T05:10:29.655Z`; integration started from main
`bb177121ec2efdc6c998a8290b9e7b09c7706c62`.
Sections 3.2, 3.3 and 4.3 motivate bounded generic local properties and rules.
The user's subsequent explicit h/k clarification selects the new
[Node profile](NODE_VECTOR_PROCESSOR.md): h is one hop; k is configured per
interaction, independently of operation cost. This supersedes the cost-derived
k description in section 10.6 for the opt-in profile only. Node vector width is
also explicitly generalized while world topology remains the current six-port
lattice. Section 1.3's distinction between assumptions, tested consequences and
emergence claims remains binding. The live document was not edited.

## Shared field computation cycle reconciliation - 2026-09-13

The live Highlights revision
`ANLCKQluUGX_afG63QQM9IQBX-qmjBbhP-b8UVvMJ-mCjZQ30ZYQ_Kkyk4MKp-O_P1PvMixFu3_pO-w-dDxrnekqUXbwar_XXVKECHy5vBA`
was read against source base `1784acdd140f260c0fb5e568b2e28241df573fa2`.
Section 4.4 maps to the opt-in
[shared field/carrier cycle](SPATIAL_COMPUTATION_DELAY.md): C counts combined
local work once, one integer ceiling sets the entire cycle, proposals stay
frozen and later input belongs to the next cycle. Section 3.5.3 maps to
distinct waiting, input-buffer and transit owners in inventory.
The empty-input stream is implicit zero and allocates no event history.
This timing candidate does not establish nonlinear energy conservation,
gravity or quantum/spatial composition. The live document was not edited.

## Property coupling and local conservation reconciliation - 2026-09-13

The live Highlights document was read at revision
`ANLCKQluUGX_afG63QQM9IQBX-qmjBbhP-b8UVvMJ-mCjZQ30ZYQ_Kkyk4MKp-O_P1PvMixFu3_pO-w-dDxrnekqUXbwar_XXVKECHy5vBA`.
Source base: `ed65f829a6ddc797cafec1bf34156ca59bdcb7dd`. Sections 10.2, 10.5,
10.6 and 10.7 map to [property selection](PROPERTY_COUPLINGS.md), shared explicit
entity profiles and [passive local conservation](LOCAL_CONSERVATION.md).
The clarified user rule requires joint energy/momentum and actual boundary flux;
internal transfer is not an external source and checking cannot repair a law.
The audit detects violations after committed owner changes. Per-rule validation
no longer sets computation delay. Catalog metadata remains formula-free;
experiment profiles define their own quantities and elementary assignments.
No physical species law or universal proof follows. The live document was not edited.

## Coupled excitation candidate reconciliation - 2026-09-13

The [unit-excitation probe](COUPLED_EXCITATIONS.md) applies Highlights sections
3.2, 3.3, 3.5 and 4.3: independently owned field/internal states exchange through
local generic operations and a coordinated commit. A local capture gate retains
the input while a carrier computation is pending. This is a configured mechanism
under the unverified emergence hypothesis in sections 1.1.3 and 1.3.3, not a new
claim that electron/photon dynamics or quantum occupation have emerged.

The live document was read on 2026-09-13 at revision
`ANLCKQmE1CS353UW3vWf9cdweVRw0CiohpQ85_euvi1zz8TP_ijhldHMIs45KNJzO19_xt67LnVLnj03t2IyvWRQ8kS8TCH8jcFGKfmj3UE`.
Source base: `6a2816526083c23069bf3b0f3fcb6a9dc5b17944`. The finite unit-state,
single-packet and held-receiver restrictions belong to this experiment. No core
law, catalog measurement or live Highlights text changes in this work.

## Configuration validation reconciliation - 2026-09-13

The [read-only preflight](CONFIGURATION_VALIDATION.md) implements explicit input
rejection and shared ownership under Highlights sections 4.5 and 10.7. It validates
configuration data without generating a physical state or inferring a law from
catalog measurements. Passing preflight remains distinct from the verified
behavior and physical hypotheses in sections 1.3 and 6.3. The live document was
read on 2026-09-13 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Source base: `521b63567d186bab2fac982a1e1f9d0a592a73a5`. This is a host validation
and Skill workflow change; it adds no physical law and does not edit Highlights.


## Physical reference catalog reconciliation — 2026-09-12

The version 2 [entity catalog](ENTITY_CATALOG.md) expands descriptive coverage
without supplying physical evolution laws. Sourced measured properties remain
external comparison targets. Possible interactions describe channels and their
conditions; the simulator still needs explicit elementary operations and evidence
of emergence. The original 46 experiment profiles move to a separate file.

This implements the Highlights goals of deriving effective laws from local
operations, preserving generic field/type definitions and separating established
physics from hypotheses and verified results. The live document was read on
2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
This repository update does not modify that document or claim additional derived
physics. Source base: `98b774ac3b02aa5cd350d5513b1e1fddbe3a2c81`.

## Historical implementation inventory

This versioned companion records the implementation inventory added to
[Universe 24 Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit).
Scope: main `09464b41b2c44a191aa2fcbdf4b036680bd646a5`.
The live document was updated on 2026-09-12 with section 10 below, preserving
all earlier paragraphs. Verified revision:
`ANLCKQkcdo3E9Q9qA92kvEzUjmFE9kJmMiJsmZQ8jTo0wroDlz5YbBRcKpGlvLu6PDzqvRncp0x2R4ecCgECBJFygKGssxx8uQW2M6WYTQg`.
Highlights is the high-level specification; linked contracts define exact schemas
and rejection cases. Neither a prose document nor Git restores credentials or
expired outputs. Together, this map, the contracts and versioned initialization
files allow reconstruction without chat history.

This is a dated inventory for the revision above. Later native event programs,
local probes and internal path changes are described in [project status](PROJECT_STATUS.md),
[the documentation index](README.md) and [migration](MIGRATION.md). Preserve this
record as historical evidence rather than treating its omissions as current gaps.

This is a dated inventory for the revision recorded above. Later native event programs,
quantum entity support, Maxwell research examples, local probes and internal path changes
are described in [project status](PROJECT_STATUS.md), [the documentation index](README.md)
and [migration](MIGRATION.md). Preserve this record as historical evidence rather than
treating its omissions as current gaps.

## 10. Implemented entities and rules

### 10.1 World, nodes and links

- The active world is a bounded three-dimensional lattice with six directed
  neighbor ports: +X, -X, +Y, -Y, +Z, -Z.
- A node owns bounded resident records, field stock, residuals and pending local
  proposals. A link owns dispatched payloads until their fixed arrival tick.
- Periodic boundaries wrap all three coordinates. Open boundaries remove outgoing
  contents and record their escaped quantities; they do not reflect or reinsert them.
- Integer value, field, type, slot, expression and rule limits are validated.
  Exhaustion or overflow is an error, never silent deletion or unlimited allocation.
- Addresses route events; ordinary local laws cannot query distant state.

### 10.2 Field definitions and disturbance records

- A field declares its label, one or three components, units, scale, signedness,
  extensivity and whether its quantity is conserved. Labels select no physical law.
- Signed values and zero use positive integer payload codes internally. External
  JSON and diagnostics expose decoded values, including negative vector components.
- A disturbance type selects fields, defaults, local updates and transport policy.
  Seeds instantiate typed records at configured nodes.
- Transport may hold a record, move a whole record or distribute declared contents
  according to its policy. Direction, six routing weights and a scalar/vector
  payload are different concepts. No floating-point normalized vector is required.
- Rate accumulators and integer residuals preserve discrete allocations over time.
  They are physical bookkeeping, not accumulated computation debt.
- Mass, charge, momentum and emission in examples are configured quantities.
  The engine does not recognize electrons, protons or physical material classes.

### 10.3 Spatial fields and finite propagation

- Spatial fields separate immutable background from dynamic contributions.
  Background is observable locally and excluded from dynamic decay.
- Outward propagation uses bounded directional populations, including eight octant
  channels, and routes allocated amounts through six links. Six ports do not mean
  every field must contain six vector components.
- Scalar/vector payload sign is preserved on receipt; the receiving face does not
  automatically reverse it. Opposing directional populations can coexist.
- Emissions add configured field amounts. In schema 2, finite emission and reaction
  allowances prevent an inexhaustible source; dynamic fields have declared decay.
- Unsigned dynamic stock cannot decay below zero. Signed components retain their
  declared sign semantics; dissipation is tracked component by component.
- Conservation includes resident and in-transit stock, configured sources, recorded
  dissipation and escaped quantities. A balanced decay ledger does not mean the
  remaining physical inventory is conserved indefinitely.
- Self-field attribution is not implemented as a general source-identity filter.
  Arrival order is not a general proof of ownership after turning or periodic return.

### 10.4 Local field rules and field groups

- Schema 1 optionally supports retained local fields alongside outward fields.
  Schema 2 rejects local field rules and joint spatial interactions; policies are
  distinct candidates and cannot be silently mixed.
- Field groups give related scalar/vector fields a logical label. Groups neither
  duplicate stock nor implement an electromagnetic law.
- Local rules read retained values and completed incoming values independently
  for all six travel channels. They may also read outgoing proposals from earlier
  rules in the same phase.
- Assignments replace retained dynamic stock or an explicitly selected outgoing
  payload. Background is not an assignable stock.
- Expressions, conditions, ordering and invariants are bounded configuration data.
  No arbitrary Python or hidden neighboring-node read is accepted.

### 10.5 Couplings, interactions and rotation

- Local updates and pair exchanges use generic integer expressions, coefficients
  and retained remainders. Sources must be declared.
- Atomic pair interactions evaluate coordinated assignments from a frozen pair and
  validate configured invariants before commit. A failed transaction cannot apply
  only one participant's change.
- Spatial exchange and exact quarter-turn response change a carried vector and
  account for the corresponding field reaction within the selected policy.
- Joint carrier/field interactions can assign carried and local/outgoing field
  quantities with declared invariants and guards. Validation and commit cover the
  participating state together, including delayed proposals and competing inputs.
- Momentum conservation requires the configured component balance across all
  participants. Preserving vector magnitude alone does not conserve momentum.
- The unequal-mass collision example supplies its elastic law and energy invariant
  in JSON; its successful outcome is not evidence that collision laws emerged.

### 10.6 Cost, timing and ownership

- Each declared model primitive has a configured positive cost. A local carrier
  cycle sums its work C and compares it with budget B.
- With link time tau, k = max(1, ceil(C/B)); additional wait is (k-1) tau and the
  subsequent link transit remains tau. Already dispatched arrivals never slow down.
- Pending proposals remain fixed while waiting; newly received inputs are handled
  according to the scheduling and transaction contract, never read from the future.
- Carrier and field phases have separate clocks and recorded costs. Do not infer
  that a spatial field named computation automatically measures all engine work.
- The optional cost-reporting field belongs to a held nonconserved scalar record.
  A separately emitted computation field requires an explicit configured law.
- Host elapsed time, visualization work and global diagnostics are not model costs.

### 10.7 Initialization, results and display

- Initialization selects model identity, schema, boundaries, capacities, timing,
  costs, field/type definitions, seeds, transport, emissions and applicable rules.
- The prepared simulator reads new JSON without compilation. Unknown definitions
  and incompatible policies fail explicitly.
- Normal runs save the input, event trace, final state and run metadata. They check
  combined quantity accounting at each completed tick and retain failure evidence.
- The runner can submit each active Node's immutable disturbance and spatial-field
  plan to isolated Python interpreters. A tick barrier and address-ordered commit
  preserve the serial result. Shared delayed field/carrier cycles use two planning
  barriers before their joint commit. Host worker counts never change modeled local cost.
- Visualization is opt-in. Playback and workspace consumers read recorded labels,
  values, groups, positions and transfers without changing physical state.
- Views distinguish resident records from fields and in-transit payloads, and
  display signed loss/escape accounting without confusing dissipation with failure.
- Saved configuration editing must preserve references when fields are renamed.
  Arbitrary labels and declaration order must not select hidden behavior.

### 10.8 Research scope and reproducibility

- Historical scalar, linked, balanced and causal-stream APIs remain explicitly
  named comparisons, not default laws of the generic Simulation.
- Quantum and Focus modules have separate research contracts. They do not authorize
  nonlocal ordinary fields or establish real quantum input, Maxwell equations,
  emergent gravity or a complete physical theory.
- Reproducible examples include approaching/parallel motion, spreading, configured
  elastic collision, three carriers with finite fields, and both boundary modes.
- Check renamed and reordered configurations, integer limits, residuals, local
  transaction failure, rotation, signed balances and generic result consumers.
- Run the recurring genericity procedure from the repository skill. Report exact
  source identity and coverage; finite passing tests do not prove universal behavior.
- Preserve source, specifications, skills and original configurations in Git.
  Generated results expire under the 24-hour policy; idle cleanup needs a scheduler.

## Coverage map

### Local observer reconciliation

For the [local reception observer](LOCAL_OBSERVER.md), Highlights was reread on
2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Sections 2.1, 4.6, 5.1-5.2 and 10.7 require discrete connected nodes, causal
delivery and read-only output. The probe records completed local inputs and
preserves exact playback prefixes. The user's event-time interpretation
motivates a local cycle counter; perceived time and a derived spacetime remain
hypotheses. The live document itself was not edited by this implementation.

### Directional-wave candidate reconciliation

Read the live Highlights on 2026-09-12 at revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
The [directional-wave contract](DIRECTIONAL_WAVE.md) is a new explicit candidate
under sections 3.3, 3.3.2, 3.5, 10.4 and 10.5. Six transverse directional modes,
bounded vector operations and local encounter guards preserve the declared
U=sum of squared mode amplitudes and P=sum of their direction-weighted energies,
with resident and in-flight ownership counted once. Same-law cubic rotations and
periodic return are tested. E/B are derived readouts, not duplicated stock.

The candidate demonstrates conditional polarization interaction and declared
balances. It does not promote the emergence hypothesis to a verified physical
law, or claim Maxwell dynamics, charge response or trajectory scattering.
The [configuration Skill](../skills/simulation-configuration/SKILL.md) supports
section 10.7 with reusable input definitions and separate recording/display controls.
Its commands and template are executable evidence; technical workflow remains in
the repository. This reconciliation does not edit the live Google document.

### Local Maxwell research reconciliation

For the [configuration-only Maxwell experiment](../examples/maxwell/README.md),
Highlights was reread on 2026-09-12 at live revision
`ANLCKQnu00jY0NhSjcfyTkt2A8oPZs3_d4dpkEsZ7TI37moZ-eXNntyf4MfeRPttXmu_vnMlIlwe1xt0qmZsn1KXkJoxrMoESFC4_eG9MWA`.
Sections 1.3.3, 1.3.4 and 10.4 are reconciled as follows: the existing generic
local field interface can express a transverse reflection and one-link
streaming hypothesis without adding an engine field equation. Conditional
leading vacuum dynamics and small-space mode frequencies agree with the
independent forecast. Exact centered Gauss conservation, complete macroscopic
energy, physical light speed and indefinite bounded-integer mixing remain gaps.
The experiment does not promote full electromagnetic emergence to a verified
result. This entry records repository coverage; it does not claim a live
Highlights edit or replace the earlier revision record above.

### Source contracts and evidence

| Highlights section | Authoritative contract / implementation owner | Evidence owner |
| --- | --- | --- |
| 10.1 | [Disturbances](DISTURBANCES.md), core/topology.py | test_open_boundaries.py, test_boundary_configuration.py and architecture tests |
| 10.2 | [Disturbances](DISTURBANCES.md), core/disturbance_state.py | test_generic_identity.py |
| 10.3 | [Spatial fields](SPATIAL_FIELDS.md), fields/spatial.py, fields/spatial_decay.py | finite-field and spatial transport tests |
| 10.4 | [Local field rules](LOCAL_FIELD_RULES.md), fields/local_field_rules.py | test_local_field_rules.py |
| 10.5 | [Spatial couplings](SPATIAL_COUPLINGS.md), fields/spatial_interactions.py | test_spatial_interactions.py, test_atomic_interactions.py |
| 10.6 | [Definitions](../SIMULATOR_DEFINITIONS.md), core/disturbance_engine.py, core/spatial_engine.py | disturbance and spatial scheduling tests |
| 10.7 | [Workspace](WORKSPACE.md), runner.py, diagnostics/disturbance_render.py, ui_assets | test_workspace_integration.py, test_recorded_movie.py |
| 10.8 | [Architecture](ARCHITECTURE.md), [recovery](RECOVERY.md), [regression skill](../skills/regression-check/SKILL.md) | [test expectations](TEST_EXPECTATIONS.md), [validation](VALIDATION.md) |
