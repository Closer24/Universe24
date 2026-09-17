# Catalog of nature

[`catalog/nature.json`](../catalog/nature.json) is the catalog of nature: the
data file that declares what exists on the board of the one generic engine, by
the model owner's decision of 2026-09-17 ([Highlights](HIGHLIGHTS.md) 3.26 and
3.30). It is exactly two things:

- the **rays** of nature: every family as a ray record (rest rate, charge,
  phase width, its field family and release, later colour and polarization);
  matter, light and fields are all ray records; beneath them the
  **couplings**, what happens when ray A meets ray B, one table each;
- the **apparatus**: the Detector and the external body, the declarations an
  experimenter places on the board, which obey no table.

The engine only reads this file. A world file selects rays from it and places
apparatus, and nothing else exists on the board. Every number in the file is a
declaration to be tested by the [experiments register](EXPERIMENTS.md); none is
derived by the engine and none is a law of nature. Where the model owner has
not decided a value, the file says so: the string `"undecided"`, beside a
`decided_by` that names the experiment or the [hypothesis](HYPOTHESES.md) that
decides it. Nothing is invented in its place.

## The rule: the engine reads the catalog as data

Highlights 3.26 (approved 2026-09-17): the engine performs only the simple
operations, a step on a Link, a phase advance, a split by a declared table, a
sum, and the one draw at a marked Node. Anything that does not change how a
ray moves between events is a family property in the catalog or a coupling
table, read only at a meeting, exactly as charge is. Forces and polarization
are catalog entries, not engine mechanisms; the strong interaction is quark
families, colour, the gluon as the quark's own field and binding couplings;
the weak interaction is an N-to-M conversion at the tick of a bound group that
draws as a Detector. The catalog therefore adds no rule to the engine: a
family the engine cannot run yet is data waiting for its feature (issue #169,
[ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order)), and no engine
rule is named after a family. Highlights 3.30: one property engine, families
distinguished by property content and permitted interactions, not by separate
engines.

The file is data in the sense of the
[local integer operation contract](ARCHITECTURE.md#local-integer-operation-contract):
exact integers and ratios `[n, d]`, no floats, no formulas, and no executable
expression beyond the declared `outputs` and `invariants` a `ray_interactions`
rule already takes. A test pins the file's contract
(`tests/test_nature_catalog.py`, below); an experiment confronts its numbers.

## Units

| Unit | Declaration | World key |
| --- | --- | --- |
| m₀, the rest rate | One phase step per interval, the rest rate of the electron ([hypothesis 12](HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding), hypothesis 14); every rest rate is an integer multiple of it and light is 0; a rest rate is the ray's mass as a clock (Highlights 3.3) | `kerengonen.phase_advance` |
| e/3, the charge unit 3 | Every charge is an integer number of thirds of the elementary charge e, so that quarks are integers: up +2, down −1, electron −3, positron +3, proton +3, neutron 0; `charge × amount` summed over a meeting's rays is the invariant the engine appends to every coupling | `charge`, per quantum |
| The phase width | 2^`phase_bits` steps per turn; a phase is an integer from 0 below that, an advance or a difference a mask with it less one. A phase is read only at a meeting and only as a difference, so the width is the family's choice of the resolution its couplings need (Highlights 3.28, 2026-09-17): eight steps resolve the Born table, the register's boards use 8 (256 steps), the reference table is written at 3 (8 steps), and a wider circle is allowed but never required; A11's 75-bit phase is a check that a wide width leaks into no coupling | `phase_bits`, one width per world |
| The lag width | The modulus of the lag register in which a field ray's delay is carried and spent as one interval of wait when it reaches that modulus; declared per family, of any width because it enters no phase sum; it, not the phase circle, is the N of hypothesis 14 on the delay. Open under feature 8b: the turn, the transverse part of the lag, landed on 2026-09-17 as the momentum register of a free ray (`ray-momentum-turn-v1`, a resolution of one part in the ray's amount, no modulus), and the delay is counted in phase steps until a run needs its own modulus; what fixes N is hypothesis 16 (Highlights 5.5, 2026-09-17), until which N is an input | the `lag_bits` entry: world key open |
| The quantum | The content of a ray, a bounded integer; the energy of the invariants is the amount, the momentum is amount × heading | `amount` |

## The records

**A ray** (`rays.<id>`; the id is the world's field name): `kind` (`ray`,
`field` or `bound_group`), `rest_rate` (in m₀, or `"undecided"`), `charge`
(in thirds of e), `phase_bits` (`"default"`: the world's one width), `field`
(the ids of its field rays: its own field and, if massive, the mass field)
and `note`. A `field` ray adds `field_of` (the rays that release it) and
`release` (`[n, d]`: each departure releases `floor(amount × n / d)` per Port
heading except the ray's own,
[released field](SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1)).
`light` is a `field` ray, the electromagnetic field in ray form (Highlights
3.5, model owner, 2026-09-17): released by the electron and the positron as
their field (the families `electron_field` and `positron_field` until that
date) and emitted at an event by any source, a photon one quantum of it. Its
`spread` key is the six-heading split table by which every Node that light
reaches releases it again, the backward heading included, the remainder
below a quantum owned by the Node per family and heading and leaving whole
when it reaches one (Highlights 3.5, model owner, 2026-09-17, feature 12b,
`field-remainder-v1`; `field-spreading-v1` selected the remainder's heading
by phase until then)
(feature 12, `field-spreading-v1`, 2026-09-17, [field
spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)): `[6, 1,
1, 1, 1, 1]`, the first declared table, which A1 and A6 confront.
Its `source_sign` key, `releaser`, is the sign of the releasing charge
carried on the field ray as a visible property, like the Detector's bit
(Highlights 3.5, "the field is matter's message about itself", 2026-09-17),
set by the engine at the release, read by couplings and never the phase;
feature 12 carries it, and `electron_field_turn.opposite_charge` closes with
it (A5). A field ray is a ray with an empty event record, rest rate 0 and
charge 0, and nothing else.
A `bound_group` adds `members` (ray id to count), `binding` (the corner table
whose loop its rays close, loop-binding-v1, 2026-09-17) and, if it can decay,
`decay` (the conversion and the mark's setting). A property read only at a meeting (`colour`, `spin`,
`polarization`) sits on the ray record; `reference` holds a measured number
the register quotes for comparison, never a lattice value.

**A coupling** (`couplings.<id>`): `status` (`decided`: everything needed to
run it is fixed; `open`: a value needed to run it is not), `engine` (the
identity that runs it, and `landed`: true when every mechanism it needs is on
`main`, false when a feature or a property it needs, colour, spin, the
group's draw, is not), `participants` (the ray ids that meet, `"any"` for
every ray, or `{"apparatus": "external_body"}`), one of `outputs` (the event
rays, in the format of a `ray_interactions` rule when decided, or
`"undecided"` when not) or `sink` (absorption into the accounted sink),
`invariants` (the exact sums
over inputs and outputs; `charge × amount` is appended by the engine) and
`note`. In an external-body coupling `"any"` and `"same"` stand for the met
family, `"body"` for the body's family and `"setting"` for the body's
offset; a world writes the names. A binding coupling
(`electron_proton_binding`, `quark_binding`, `gluon_gluon_binding`,
`pauli_exclusion`) is a **corner table** since 2026-09-17 (feature 14,
[loop binding](LOOP_BINDING.md), `loop-binding-v1`): an ordinary outputs
rule whose loop closes, with a `closes` note saying what closes under it;
the Port form of the ring's `corner` rule where the design gives it, the Born
form where the design names it, `"undecided"` where the model owner has not
decided. The held form of feature 8 (`binds`, `delay` 1, `ray_delay`) is gone
from the engine and from the file.

**The apparatus** (`apparatus.detector`, `apparatus.external_body`):
`world_key`, `engine`, `declaration` (the keys a world writes), `does` and
`note`. Both are landed: the Detector (`detector-mark-v1`,
`detector-return-v1`, `inverse-split-v1`) and the external body
(`external-body-v1`, feature 7b), whose record also states the coupling form
(the body is the participant that never changes, its token returned once
among the outputs) and the `apparatus_family` a world gives a mirror, a
splitter or a plate under a declared coupling: rest rate 0, since the token
must come back with the body's phase, no charge, no field.
The Detector's record also lists its `couplings` on the bit a ray already
carries (Highlights 5.4, model owner, 2026-09-17; feature 2b,
`detector-bit-property-v1`, landed 2026-09-17), two decided entries with
their world keys on the mark's `detectors[]` entry: `on_bit_1`, a ray
carrying 1 passes without a draw; `on_bit_0`, a ray carrying 0 is a
transmission and is never drawn; only a ray carrying no bit is drawn. Each
key takes `"pass"` (the default) or `"draw"`, the draw of `detector-mark-v1`
on that arrival ([the bit as a property](SPATIAL_FIELDS.md#the-detectors-bit-as-a-property-detector-bit-property-v1)).

`layers` is a note only: layers are derived from the couplings
([layers](SPATIAL_FIELDS.md#layers-ray-layers-v1)), never declared.
`experiments` lists, per entry A1 to A14 of the register, the ids it uses, so
that the register and the catalog agree; the test holds the two together.

## Undecided entries and what decides each

The test reads this table and holds it equal to the `"undecided"` values of
the file, path for path and decider for decider. A decider is an entry of the
[register](EXPERIMENTS.md), a numbered hypothesis of the
[hypotheses page](HYPOTHESES.md), or a feature of the
[ray-event model's migration list](RAY_EVENT_MODEL.md#6-migration-in-order).

| Entry | What is undecided | Decided by |
| --- | --- | --- |
| `lag_bits.world_key` | The key that declares the lag modulus per family for the delay on the ray's own axis, the N of hypothesis 14 on the lag register and not on the phase; the turn is the momentum register of feature 8b since 2026-09-17; what fixes N is hypothesis 16 (Highlights 5.5, 2026-09-17) | feature 8b, hypothesis 16 |
| `rays.light.polarization` | The two-state transverse property of light (feature 11) | A12 |
| `rays.electron.spin` | The two-state property of the electron family (feature 11) | hypothesis 12 |
| `rays.positron.spin` | As for the electron | hypothesis 12 |
| `rays.muon.rest_rate` | The muon's rung on the ladder, k × 206.768 28 | A10 |
| `rays.neutrino.rest_rate` | The neutrino's rung | hypothesis 12 |
| `rays.antineutrino.rest_rate` | The antineutrino's rung | hypothesis 12 |
| `rays.up.rest_rate` | The up quark's rung | hypothesis 12 |
| `rays.down.rest_rate` | The down quark's rung | hypothesis 12 |
| `rays.gluon.release` | The release ratio of the quark's field; what fixes a release ratio is hypothesis 17 | hypothesis 13, hypothesis 17 |
| `rays.gluon.colour` | How a gluon ray carries its releaser's colour | hypothesis 13 |
| `rays.proton.rest_rate` | The proton's rung, k × 1836.152 67 | A10 |
| `rays.neutron.rest_rate` | The neutron's retained content | hypothesis 12 |
| `rays.mass_field.release` | The release ratio of the computation field; what fixes a release ratio is hypothesis 17 (Highlights 5.5, 2026-09-17) | A6, hypothesis 17 |
| `couplings.electron_field_turn.strength_table` | The integer table over field content and charge product; with a `momentum_table` in place of the outputs (`ray-momentum-turn-v1`, feature 8b) the turn is gradual, sign x amount x heading of every field ray met, and the table's role is the field's amount | A5 |
| `couplings.electron_field_turn.opposite_charge` | The heading rule when the charges differ in sign; closes with `rays.light.source_sign`, the sign carried on the field ray (feature 12) | A5 |
| `couplings.recoil_return.outputs` | What the returning field ray does at its releaser | A5 |
| `couplings.mass_field_delay.outputs[0].delay.table` | The delay table, six entries per Port, per unit of field amount | A6 |
| `couplings.electron_proton_binding.binding_energy_ladder` | Whether bound trajectories have discrete retained energies, and their ladder | A8 |
| `couplings.quark_binding.outputs` | The three-quark corner table (an outputs rule whose loop closes, loop-binding-v1) | hypothesis 12 |
| `couplings.gluon_gluon_binding.outputs` | The field-to-field corner table, the one catalog line by which gluon rays close into a string between quarks (Highlights 3.26, 2026-09-17; an outputs rule whose loop closes, loop-binding-v1) | hypothesis 13 |
| `couplings.weak_conversion.shares` | The neutron's content shared among proton, electron and antineutrino | A9 |
| `couplings.weak_conversion.headings` | The headings of the three products | A9 |
| `couplings.pauli_exclusion.outputs` | What two electrons of opposite spin bind to (feature 11): the Born-form corner table with the guard on spin, loop-binding-v1 | hypothesis 12 |
| `couplings.transmission_meets_held_share.outputs` | The table between the transmission and the share waiting under its delay output, and where the two meet (a ray waiting at its event Node is met by nothing there since loop-binding-v1) | A3 |
| `couplings.beam_splitter.outputs.table` | The split ratio of the splitter | A2 |
| `couplings.slit.outputs.shares` | The share per forward heading of a slit | A1 |
| `couplings.polarizer.outputs.table` | The polarizer's cos² table in N-ths (feature 11) | A12 |

## How a world selects rays from the catalog

There is no loader: a world file is written from the catalog, one
`spatial_fields` entry per selected ray and one `ray_interactions` rule per
selected coupling, and the test shows the mapping by building its worlds from
the file. A world names only the rays it holds and declares only the couplings
it uses; the layers follow.

| Catalog | World file |
| --- | --- |
| The ray id | `fields[].name` and `spatial_fields[].field` |
| `rest_rate` | `spatial_fields[].kerengonen.phase_advance` |
| `charge` | `spatial_fields[].charge` |
| `phase_bits` | `spatial_fields[].phase_bits`, the same for every ray of the world |
| A field ray's `field_of` and `release` | `spatial_fields[].field_of` (one family per field today) and `spatial_fields[].release`; a world that holds both charged families declares the light family once per releaser, as it does the mass field, and a world whose light no charge releases writes neither key |
| A coupling's `participants`, `outputs`, `invariants` | One `ray_interactions` rule |
| `apparatus.detector` | `detectors[]` with `position`, `setting`, `seed`, the optional `on_bit_1` and `on_bit_0` (`"pass"` or `"draw"`, the couplings on the bit a ray carries, `detector-bit-property-v1`), and the world's `return_mode`; a coupling's `bit` (`"highest"`, `"none"`, `{"of": i}`) is the `bit` key of its `ray_interactions` rule |
| `apparatus.external_body` | `external_bodies[]` with `position`, `family`, `amount` and the optional `charge`, `phase`, `initial_momentum`, `coupling` (`"sink"` or a declared rule's name) and `momentum_table` ([external body](SPATIAL_FIELDS.md#the-external-body-external-body-v1)); a coupled body's rule names the body's family for the apparatus role and returns its token once |
| A bound group | A loop: rays circulating on a ring of Nodes under the corner table, one `ray_interactions` rule with outputs per binding coupling, as `examples/nature/ring.json` declares the unit-square electron ([binding as a loop](SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1), [loop binding](LOOP_BINDING.md); Highlights 3.4, 2026-09-17); nothing holds and no key names the group, which a reader finds in the record. The held form (a rule without outputs assigning `delay` 1, `ray_delay`) was removed by feature 14 on 2026-09-17 |
| A source | A marked Node that emits the family: a lamp on a Node with a mark of setting 1 |

A bound group's decay draw (the mark drawing at the group's tick), colour
and the properties of feature 11 have no world key yet; their catalog
records wait for them, and no engine rule is added for them
([ray-event model, after feature 10](RAY_EVENT_MODEL.md#6-migration-in-order)).
The split table of feature 12 has its world key, `spread` on a ray spatial
field, and the light family declares it (`field-spreading-v1`,
2026-09-17), with `source_sign` the sign the engine puts on every released
ray.

## What the catalog is not

The [entity catalog](ENTITY_CATALOG.md)
(`examples/known-entities/catalog.json`) is the sourced physical reference:
measured values with citations and no executable content, validated by
`event_universe.entity_catalog`, which rejects `outputs`. The catalog of
nature is the other side, what the engine reads, and is made of outputs; the
two formats differ because their responsibilities do. A measured number the
register quotes (the keV masses of A9) appears here under `reference`, for
comparison only. The register decides which experiment runs and pins its
criterion; this file only lists, per entry, the ids it uses.

## Evidence

`tests/test_nature_catalog.py`
([expectations](TEST_EXPECTATIONS.md#catalog-of-nature)) parses the file
under the strict decoder, checks every record and reference, holds the
undecided table above equal to the file, holds the experiment ids equal to
the register's, builds a world from the file for every ray a world can select
today, for every release a world can declare today (light by the electron
and by the positron) and for every decided coupling the engine runs today
(the Born steering, the electron's turn at a field ray, and an external body
under the absorber, the mirror and the phase plate), runs each for two ticks against
pinned integers, and checks that a Detector mark parses. `tools/check.py` selects it when the catalog, this
document, the register or the hypotheses change. Passing it establishes the
file's contract, not any agreement with nature: that is the register's.
