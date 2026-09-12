# Bounded local record conversion

An atomic pair interaction may declare `output_types` with exactly `left` and
`right` type names. The existing assignments then supply the complete payloads
of two replacement records. Every expression reads the frozen input pair.
The type labels select configured behavior; the engine does not interpret them.

This first extension is exactly two inputs to two outputs, in the same two
reserved slots before routing. It does not implement variable product counts,
record deletion, photon production or a derived matter/antimatter law.
`examples/known-entities/conversion.json` is the explicitly named
`generic-two-record-conversion-probe-v1`: two held records with positive scalar
inventories 2 and 3 and opposite unit momenta become two moving record types.
All output values are copied. Inventory 5 and total momentum zero persist;
neither output type's defaults supplies reaction content. This is a software
ownership demonstration, not a physical annihilation model.

## Preconditions and semantics

- Both output types differ from both input types. A rule therefore cannot
  immediately repeat on its own products. Other explicitly declared rules may
  act later in the fixed rule order; cyclic networks are configuration choices.
- All four types own the same field set and use whole-record hold or move
  transport, without a `cost_field`. Every owned output field has an explicit
  assignment. Different field schemas and missing output assignments fail loading.
- Schema 1 is required. Involved types cannot have exchange couplings, spatial
  emission, spatial couplings or joint spatial interactions. Those combinations
  need an explicit transfer contract for carried fractions, allowances and
  frozen opposite reactions. Unrelated spatial fields remain allowed.
- At conversion, routing phases, rate remainders and carried
  metadata must all be at their zero/default coded state. Nonzero fractional
  progress is rejected, never erased or borrowed by a different transport law.
  Outputs start with zero routing bookkeeping. A valid channel tag (seed or one
  of six neighbor ports) is preserved: for whole records this is arrival provenance,
  not fractional progress or conserved inventory. The next departure replaces it
  with its actual outgoing port. Configurations that convert a
  moving fractional-rate carrier must reach this state before activation.
- Every field marked conserved retains its component sum. Every declared pair
  invariant also retains its exact pre/post value. Unsigned payloads remain
  nonnegative; expression and payload bounds remain enforced. These assertions
  do not infer the physical meaning of a named quantity.
- Output assignment, type replacement and routing share the existing frozen local
  plan and commit. Each type replacement charges one additional `update`.
  Original records own all inventory while computation waits. Conversion never
  creates a second owner in the pending proposal. Invalid proposals install no
  partial replacement or pending plan. Neighbor transit retains `link_ticks`.
- Conversion allocates no extra slot. Existing resident and outgoing capacity
  checks remain active and stop a run on exhaustion. Work remains bounded by
  fixed rule, field, expression and slot limits, independently of world size.

A conversion can prescribe a hypothesis using these generic operations. Such a
configured reaction is still an input law: supporting its definition does not
show that annihilation, Maxwell dynamics or particle species emerged from more
basic rules. Energy must have a defined representation and conservation check
before any example can claim physical energy preservation.

The owners are `core/disturbance_state.py`, `initialization.py` and
`fields/disturbances.py`. Focused evidence is in `tests/test_local_conversions.py`;
the existing atomic interaction and engine suites cover their shared commit,
capacity, arithmetic and transit contracts.


## Bounded variable-multiplicity reactions

The separate `reactions` initialization key generalizes local product ownership to
one through eight input records and one through eight output records. It does not
change the legacy pair `interactions` schema. Reaction assignments read the frozen
input tuple by `participant` index and fully define every output-owned field. All
inputs and output capacity are local to one cell; work and storage remain bounded
by fixed rule, slot, field and arity limits. Conserved fields are checked across the
whole selected input/output transaction before commit. Invalid proposals, missing
capacity or nonzero carried routing/allowance state fail without partial mutation.
See [particle reactions](PARTICLE_REACTIONS.md) and `tests/test_nary_reactions.py`.
