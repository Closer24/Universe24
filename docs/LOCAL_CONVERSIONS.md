# Bounded local record conversion

> **History (2026-09-19).** The engine this document describes was deleted on
> 2026-09-19 with the old engine ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
> the one engine is the field-only engine of the law of the shadow
> ([SPATIAL_FIELDS.md](SPATIAL_FIELDS.md#the-law-of-the-shadow-field-only-v1)).
> The text below is kept as the record of what was built and measured; its
> links to code, worlds and tests name files that no longer exist.

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

## N-to-M family conversion

Deleted on 2026-09-17 (issue #164, bucket B.6). `family-conversion-n-to-m-v1`
generalized the two-to-two rule above over families and arity: an
`interactions` entry with `participants` and `outputs` replaced one to six
resident records by one to six declared output families in one frozen local
plan, each product leaving on its own Port. Under [Highlights](HIGHLIGHTS.md)
3.20 and 5.1 and row R1 of the
[ray-event model](RAY_EVENT_MODEL.md#5-what-the-current-engine-does-differently)
an interaction is a property of the meeting of rays, not of a resident record,
so the N-to-M conversion lives only at a meeting of rays
([meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1),
`ray-meeting-conversion-v1`), whose arithmetic `convert_values`
(`fields/disturbances.py`) the record rule had shared. An `interactions` entry
with `outputs` is now rejected at initialization with a dated message;
`outputs` in `ray_interactions` is unchanged. The compiler
`_conversion_interaction` (`initialization.py`), the record path
`_convert_group` with the `outputs` branch of `DisturbanceLaw.__call__`
(`fields/disturbances.py`) and the one-role admission of
`core/coupling_selectors.py` are gone; see the
[migration note](MIGRATION.md#records-as-owners-deleted-on-2026-09-17). The
family-conversion candidates (`examples/family-conversion/`) and their test
module went earlier the same day with the test-suite reduction; their dated
results stay in [validation](VALIDATION.md). The two-to-two `output_types`
rule above is unchanged and stays covered by `tests/test_local_conversions.py`,
which also checks the rejection of `outputs`.

Limits found while building the deleted candidates, kept as history:

- A converting record must arrive with zero carried routing state. Cyclic
  weighted movement advances its phase once per hop, so momentum components
  used directly as port weights were rejected at the meeting; the fixtures
  moved along the reduced direction `rational_direction(momentum)`, whose unit
  weights keep the phase at zero. Fractional `rate` credit and balanced-routing
  counters were rejected for the same reason.
- Every stored component is bounded by `MAX_VALUE = 1_073_741_823`; products in
  guards and assignments use the 64-bit working register. Annihilation and pair
  production ran at exactly `MAX_VALUE` per record.
- Rational projections charge 65536 `evaluate` operations per node; the
  configuration's `normal_budget` had to cover a conversion cycle or the
  ordinary timing law delayed it.
- Three axis-aligned photons with zero total momentum always share a Port on
  the cubic lattice, so the 2 -> 3 candidate required a net momentum.
