# Highlights implementation coverage

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

### 10.1 World, cells and links

- The active world is a bounded three-dimensional lattice with six directed
  neighbor ports: +X, -X, +Y, -Y, +Z, -Z.
- A cell owns bounded resident records, field stock, residuals and pending local
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
  No arbitrary Python or hidden neighboring-cell read is accepted.

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
