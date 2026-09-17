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

## N-to-M family conversion

`family-conversion-n-to-m-v1` generalizes the two-to-two rule above over
families and arity. An interaction that declares `participants` and `outputs`
is a conversion rule on the indexed-participants mechanism of the
[Node execution profile](NODE_VECTOR_PROCESSOR.md#local-rules): the same role
selection (one `type` or `requires` per role, earliest unused compatible slot
in declaration order, disjoint groups, no search), the same frozen snapshot and
the same atomic commit. It is available in the ordinary cost-budget profile as
well as under `node_execution: true` (where `k` is required like any rule); the
plain indexed interaction without `outputs` still requires `node_execution`.

```json
{"name": "decay", "participants": [{"type": "parent"}],
 "outputs": [{"type": "child"}, {"type": "child"}],
 "when": {"op": "gt", "args": [{"field": "energy", "participant": 0}, 1021]},
 "assignments": [{"output": 0, "field": "energy", "expression": {"op": "rational_floor", "args": [{"op": "ratio", "args": [{"field": "energy", "participant": 0}, 2]}]}}, "..."],
 "invariants": [{"name": "energy", "expression": {"field": "energy"}}]}
```

| Part | Contract |
| --- | --- |
| Inputs | 1 through 6 roles; six is a declared bound of this contract (six roles, six outputs, one product departure per Port), not `slots_per_node`; the engine's transport itself admits several packets per Port |
| Outputs | 1 through 6 entries, each an explicit `type` (a declared family); property selection describes inputs only |
| Assignments | `output`, `field`, `expression`; every field owned by every output is assigned exactly once from the frozen inputs (`participant: i` references); a field the output family does not own stays zero |
| Guard | Optional scalar `when` over the frozen inputs, as in indexed rules; a zero guard leaves every input untouched |
| Invariants | Per-record readouts (`{"field": ...}` or any owned-field expression, absent fields reading zero) summed over all N inputs and compared with the sum over all M outputs, component by component; every `conserved` field is compared the same way without a declaration |
| Slots | Outputs `0..N-1` replace the input slots in role order; inputs beyond M are consumed and their slots emptied; outputs beyond N take free slots in the frozen snapshot, and when none is free the cycle fails before commit (no waiting, no silent drop) |
| Ports | Products route in the same cycle under their own family transport. Every product departure uses a distinct Port; a second product on one Port fails before commit. Non-participant records leaving in the same cycle keep the ordinary transport, which admits several packets per Port, so a spectator on a product's Port does not fail the cycle. Products with a zero direction are retained instead |
| Ownership | Reserved slots, including newly claimed free ones, are locked against arrivals during the computation wait; originals own all inventory until the single commit |
| State boundary | No new pending, packet or Node state: the plan reuses `LocalPlan.replacements`, recording consumed inputs as `(slot, None)` and claimed free slots as replacements, which the existing pending lock protects during the wait |
| Bounded arithmetic | Every stored component is bounded by `MAX_VALUE`; guards and assignments use the 64-bit working register; rational projections carry their fixed 65536-`evaluate` tariff. These are design bounds of the contract, and a configuration's `normal_budget` must cover a conversion cycle or the ordinary timing law delays it |
| Carried state | Every input must carry zero routing, rate, allowance and exchange state, as for the two-to-two rule; outputs that reuse an input slot keep its arrival channel tag, new ones start local |
| Cost | One `couple`, one `update` per assignment and one `update` per output replacement; rational projections carry their fixed tariff |
| Failure | Guard, arithmetic, bound, conservation, invariant, slot or Port failure installs no replacement and no pending plan |

Excluded and rejected at initialization: pair selectors or `output_types` together
with `outputs`, `outputs` without `participants`, more than six roles or outputs,
split or cost-reporting families, schema 2, and families that also join exchange
couplings, spatial responses or emission. Output families may repeat input
families (an exchange that keeps both families is a 2-to-2 conversion); a rule
never re-selects its own products in the same pass, and later rules or later
cycles act on products under their own guards, as configured.

The family-conversion candidates (`examples/family-conversion/`, deleted on 2026-09-17)
are declared on this contract between catalog families, with values derived
from the [entity catalog](ENTITY_CATALOG.md) through the reference-unit
authoring adapter and recorded in `bindings.json`:

- `family-conversion-annihilation-v1` (2 -> 2), `family-conversion-pair-production-v1`
  (2 -> 2 with the 1022 keV threshold in `when`), `family-conversion-compton-v1`
  (2 -> 2 keeping both families), `family-conversion-three-photon-v1` (2 -> 3)
  and `family-conversion-four-body-v1` (4 -> 4, four rays through four Ports in
  one joint transaction whose every output reads all four inputs), each with a
  stated discrete kinematics and an explicit owner for every indivisible unit.
- The catalog photon has no energy property; the shared `energy`, `momentum`,
  `charge` layout with `energy == |momentum|` for a photon is the representation
  the entity audit found missing, supplied here as configuration data.
- Rest energy is a coupling parameter, not a stored field, because the ordinary
  runner accounts every field total.

Limits found while building them:

- A converting record must arrive with zero carried routing state. Cyclic
  weighted movement advances its phase once per hop, so momentum components
  used directly as port weights are rejected at the meeting; the fixtures move
  along the reduced direction `rational_direction(momentum)`, whose unit
  weights keep the phase at zero. Fractional `rate` credit and balanced-routing
  counters are rejected for the same reason; a physical pace `|p| / E` for a
  converting record needs an explicit rule for the credit's owner.
- Every stored component is bounded by `MAX_VALUE = 1_073_741_823`; products in
  guards and assignments use the 64-bit working register. Annihilation and pair
  production run at exactly `MAX_VALUE` per record; the Compton recoil electron
  carries one unit more than the photon and is rejected explicitly at that bound.
- Rational projections charge 65536 `evaluate` operations per node; the
  configuration's `normal_budget` must cover a conversion cycle (about eleven
  million for the annihilation rule) or the cycle is delayed by the ordinary
  timing law.
- The runner's `conserved_at_every_completed_tick` excludes escaped quantity and
  is false after the first escape in an open world; the balanced flag and the
  audit include escapes.
- Three axis-aligned photons with zero total momentum always share a Port on the
  cubic lattice, so the 2 -> 3 candidate requires a net momentum.

Acceptance. The independent acceptance criteria are the `contract` and
`generic_arity` entries of
expectations.json (`examples/family-conversion/expectations.json`, deleted on 2026-09-17), written
before the first run, and the family-conversion entry of
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md): arity 1 -> 6 with one record per
Port, 6 -> 1, arity outside one to six rejected, two products on one Port,
missing free slots, a broken readout invariant and a conserved-field mismatch
each leaving every owner unchanged with no pending plan, property-selected
inputs converting, reserved slots surviving an arrival during the wait, and the
same conversion under `node_execution` firing at `ready_tick = k`.

The owners are `core/disturbance_state.py`, `core/coupling_selectors.py`,
`initialization.py` (`_conversion_interaction`) and `fields/disturbances.py`
(`_convert_group`). Evidence: `tests/test_family_conversion.py` (deleted on 2026-09-17); the two-to-two
suite `tests/test_local_conversions.py` is unchanged.
