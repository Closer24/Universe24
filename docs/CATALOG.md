# Catalog of nature

> **History (2026-09-19).** The engine this document describes was deleted on
> 2026-09-19 with the old engine ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
> the one engine is the field-only engine of the law of the shadow
> ([SPATIAL_FIELDS.md](SPATIAL_FIELDS.md#the-law-of-the-shadow-field-only-v1)).
> The text below is kept as the record of what was built and measured; its
> links to code, worlds and tests name files that no longer exist.

`catalog/nature.json` is the catalog of nature: the
data file that declares what exists on the board of the one generic engine, by
the model owner's decision of 2026-09-17 ([Highlights](HIGHLIGHTS.md) 3.26 and
3.30). It is exactly two things:

- the **rays** of nature: every family as a ray record (content and clock,
  charge, the size of its shadow set, polarization since feature 11, later
  colour; a rest rate, a phase width per family and a field family until
  2026-09-18); matter, light and the gluon are all families of things, and a
  family's field is its own shadows (Highlights 5.4, point 12); beneath them
  the **couplings**, what happens when ray A meets ray B, one table each;
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
sum, and the one draw at a marked Node (no draw since 2026-09-18, Highlights
5.4, point 14). Anything that does not change how a
ray moves between events is a family property in the catalog or a coupling
table, read only at a meeting, exactly as charge is. Forces and polarization
are catalog entries, not engine mechanisms; the strong interaction is quark
families, colour, the gluon as the quark's own field and binding couplings;
the weak interaction is an N-to-M conversion at the tick of a bound group that
draws as a Detector (since 2026-09-18 by a decay table, point 20). The
catalog therefore adds no rule to the engine: a
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
| m₀, the content | One quantum of content, the electron's rung; a thing's content is its mass and its clock, content / K phase steps per interval with one K for the world, and light has no clock (Highlights 5.4, point 19; `clock-readings-v1`, 2026-09-18); until that date the rest rate, one phase step per interval for the electron, every rate an integer multiple of it ([hypothesis 12](HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding), hypothesis 14) | `content` and `clock` on the family, `K` on the world; `kerengonen.phase_advance` refused |
| e/3, the charge unit 3 | Every charge is an integer number of thirds of the elementary charge e, so that quarks are integers: up +2, down −1, electron −3, positron +3, proton +3, neutron 0; the charge of the things summed over a meeting's rays is the invariant the engine appends to every coupling | `charge`, the charge of one thing of the family, whole, whatever its content (charge-per-thing-v1, 2026-09-18) |
| N, the phase circle | The number of steps of the phase circle, one for the world like K (Highlights 5.4, the definitions of the law, the model owner, 2026-09-18): declared once, 64 by default, a power of two from 2 through 4096; a phase is an integer from 0 below N, an advance or a difference a mask with N − 1. A phase difference between any two rays, of one family or of two, is read on the one circle, so a width per family means nothing, and the per-family `phase_bits` is retired in the cleanup of 2026-09-18; the steering table of two things of one family is computed from N (point 17) and the Node's mixing reads N (point 24). The register's boards ran at 256 steps and the reference Born table is written at 8 | `N`, one for the world |
| The lag width | Deleted on 2026-09-18 with the delay, the lag register and the word register (Highlights 5.4, points 16, 21 and 22; the cleanup of that day): gravity is the push of the shadows read times the content of what is pushed, and every ray moves one Link per interval. What fixes the strength of gravity remains hypothesis 16's question | none |
| The quantum | The content of a ray, a bounded integer; the energy of the invariants is the amount, the momentum is amount × heading | `amount` |

## The records

**A ray** (`rays.<id>`; the id is the world's field name): `kind` (`ray` or
`bound_group`), `content` (in m₀, or `"undecided"`; since clock-readings-v1,
2026-09-18, the rung is the content, a thing's mass and its clock) and
`clock` (whether the family's things have one), `charge` (in thirds of e),
`release` (`[n, d]`, the size of the family's shadow set, `floor(content × n
/ d)` per Port heading, or `"undecided"`) and `note`. Under the law of the bit
(Highlights 5.4, point 12; `bit-law-v1`, 2026-09-18; the cleanup of the same
day) there is no field family and no `field` key: a shadow is a ray of its
owner's family with the bit 0, carrying the owner's identity, charge sign
and content as its message, given with the board (`initial_field`) and
circulating, and gravity and electricity are the one shadow set read twice
(points 16 and 18). `light` is a family of things, the electromagnetic
quantum: a photon is one quantum of it, emitted at an event by any source
and absorbed at a meeting or a mark; it has no content on the ladder, no
clock and no charge, and carries the phase of what emitted it; whether its
content casts a shadow of its own is undecided (hypothesis 17). `gluon` is
likewise a family of real rays with colour charge, emitted at events as
light is, differing from light in that it carries colour and so is itself
pushed (Highlights 3.26 as amended on 2026-09-18); the strong field of a
quark is the quark's own shadows. The families `electron_field`,
`positron_field`, `mass_field`, `light` and `gluon` as field families
(`kind: field`, `field_of`, `source_sign`, a `spread` table) are retired: a
family's `spread` is the Node's mixing (point 24, `node-mixing-v1`), the
sign a shadow carries is set by the engine, and no record declares a phase
width (one `N` for the world, above). Light's `polarization` key,
`transverse`, and `polarization_bits`, `"default"` (feature 11,
`ray-polarization-v1`, 2026-09-17; decided by A12): every light ray carries
a transverse direction modulo a half turn, an integer step of a circle of
2^`polarization_bits` steps per half turn (the world key `polarization_bits`
on the family, the world's phase circle by default), or none; 0 and half
the circle are the two lattice axes of Highlights 3.26 and the steps between
them the direction of the circular case without its handedness bit; a lamp
declares it on its emission (`polarization`), rays merge only at equal
polarization, a meeting's outputs carry their source input's unless they
declare one, and the polarizer reads it
([polarization](SPATIAL_FIELDS.md#polarization-ray-polarization-v1)). The
electron's and the positron's `polarization_bits` 1 is spin as the same
property at one bit; what `spin` stands undecided for is the table of
`pauli_exclusion` (hypothesis 12).
A `bound_group` adds `members` (ray id to count), `binding` (the corner table
whose loop its rays close, loop-binding-v1, 2026-09-17) and, if it can decay,
`decay` (the conversion and the setting its rule draws with: the `draw` of
the conversion's `ray_interactions` rule since 2026-09-17, `decay-draw-v1`,
[a decaying group draws](SPATIAL_FIELDS.md#a-decaying-group-draws-decay-draw-v1)).
A property read only at a meeting (`colour`, `spin`,
`polarization`) sits on the ray record; `reference` holds a measured number
the register quotes for comparison, never a lattice value.

**A coupling** (`couplings.<id>`): `status` (`decided`: everything needed to
run it is fixed; `open`: a value needed to run it is not), `engine` (the
identity that runs it, and `landed`: true when every mechanism it needs is on
`main`, false when a feature or a property it needs, colour, spin, is not),
`participants` (the ray ids that meet, `"any"` for every ray, or
`{"apparatus": "external_body"}`), one of `outputs` (the event rays, in the
format of a `ray_interactions` rule when decided, or `"undecided"` when
not), `momentum_table` with `reads` (a thing pushed by the shadows of the
named families, `bit-law-v1` points 15 and 16: `electron_field_turn` is the
electron pushed by its own family's shadows, read by charge; the recoil is
the return of the law, point 3, and `recoil_return` is no coupling since the
cleanup of 2026-09-18) or `sink` (absorption into the accounted sink),
`invariants` (the exact sums
over inputs and outputs; `charge × amount` is appended by the engine) and
`note`. In an external-body coupling `"any"` and `"same"` stand for the met
family, `"body"` for the body's family and `"setting"` for the body's
offset; a world writes the names. The `polarizer` (decided 2026-09-17,
`external-body-v1` with `ray-polarization-v1`) is declared on the body,
not as a rule over a token: its `outputs` state the split by the declared
table at the difference between the body's angle and the ray's
polarization, the pass share on the pass Port with the body's angle, the
rest into the body's sink counter and the remainder below one quantum in
the body's registers; its `table` is the reference table at three bits,
`[8, 7, 4, 1, 0, 1, 4, 7]`, cos^2 in eighths rounded, and a world writes its
own D entries for its circle (`rule`); `unpolarized` is the table's mean. A binding coupling
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
`note`. Both are landed and both are things since node-is-ports-v1
(Highlights 5.4, point 22; feature 17, 2026-09-18): the Detector
(`detector-mark-v1`, `detector-return-v1`, `inverse-split-v1`,
`detector-absorb-v1`, `bit-law-v1`, `node-is-ports-v1`), a Node whose bit is
set with a thing resident at it, what the mark has absorbed per bit and per
family with its momentum and the identities it is made of, no seed and no
counter; and the external body (`external-body-v1`, feature 7b), a thing with
declared tables, whose record also states the coupling form (the body is the
participant that never changes, its token returned once among the outputs)
and the `apparatus_family` a world gives a mirror, a splitter, a plate, a
wall, a screen or a beam stop under a declared table: rest rate 0, since the
token must come back with the body's phase, no charge, no shadows. A body
radiates nothing: its shadows are given with the board (`initial_field`).
The Detector's record lists its one coupling, `on_click` (Highlights 5.4 "A
click is an absorption", model owner, 2026-09-18; feature 2c,
`detector-absorb-v1`, landed 2026-09-18), the declared table of the resident
thing: what the mark does with a thing it catches by its `setting`, the k-th
arrival when k mod d < n, `"absorb"`, the thing ending in the resident on its
things line with its momentum, booked as absorbed by marks, nothing of it
spreading on; or `"pass"`, the thing continuing with its bit 1. Absorb is the
default for every family, and the world key takes one value for every ray
family or a mapping of family name to one, so a counter that lets light
through is an entry ([a click is an absorption](SPATIAL_FIELDS.md#a-click-is-an-absorption-detector-absorb-v1)).
A shadow is returned without a draw and never counted, unless the resident
is its home, when it is absorbed on the resident's shadows line without an
event ([a Node is its six Ports](SPATIAL_FIELDS.md#a-node-is-its-six-ports-node-is-ports-v1)).
The couplings on the bit a ray carries (`on_bit_1`, `on_bit_0`,
`detector-bit-property-v1`) went with the law of the bit: the bit never
changes at a meeting, and a mark reads it, never a coupling on it.

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
| `rays.light.release` | The size of light's own shadow set, whether a photon's content casts a shadow read by gravity; what fixes a shadow set's size is hypothesis 17 | hypothesis 17 |
| `rays.electron.spin` | The two-state property of the electron family (feature 11) | hypothesis 12 |
| `rays.positron.spin` | As for the electron | hypothesis 12 |
| `rays.muon.content` | The muon's rung on the ladder, k × 206.768 28 | A10 |
| `rays.muon.release` | The size of the muon's shadow set | hypothesis 17 |
| `rays.neutrino.content` | The neutrino's rung | hypothesis 12 |
| `rays.neutrino.release` | The size of the neutrino's shadow set (read by gravity alone: charge 0) | hypothesis 17 |
| `rays.antineutrino.content` | The antineutrino's rung | hypothesis 12 |
| `rays.antineutrino.release` | As for the neutrino | hypothesis 17 |
| `rays.up.content` | The up quark's rung | hypothesis 12 |
| `rays.up.release` | The size of the up quark's shadow set, its strong field (Highlights 5.4, point 12) | hypothesis 17 |
| `rays.down.content` | The down quark's rung | hypothesis 12 |
| `rays.down.release` | As for the up quark | hypothesis 17 |
| `rays.gluon.release` | The size of the gluon's own shadow set, a real family with colour charge (Highlights 3.26 as amended, 2026-09-18); what fixes a shadow set's size is hypothesis 17 | hypothesis 13, hypothesis 17 |
| `rays.gluon.colour` | How a gluon ray carries its colour | hypothesis 13 |
| `rays.proton.content` | The proton's rung, k × 1836.152 67 | A10 |
| `rays.neutron.content` | The neutron's retained content | hypothesis 12 |
| `rays.neutron.release` | The size of the neutron's shadow set (read by gravity alone: charge 0) | hypothesis 17 |
| `couplings.electron_field_turn.strength_table` | The integer table over the shadow's message and the charge product; under the law of the bit the push is sign x amount x heading read times the owner's charge over its content times the charge of what is pushed (point 16), so the table's role is the size of the shadow set, `release` on the family | A5 |
| `couplings.electron_proton_binding.binding_energy_ladder` | Whether bound trajectories have discrete retained energies, and their ladder | A8 |
| `couplings.quark_binding.outputs` | The three-quark corner table (an outputs rule whose loop closes, loop-binding-v1) | hypothesis 12 |
| `couplings.gluon_gluon_binding.outputs` | The corner table of two gluon rays, real rays with colour charge, the one catalog line by which gluon rays close into a string between quarks (Highlights 3.26 as amended on 2026-09-18; an outputs rule whose loop closes, loop-binding-v1) | hypothesis 13 |
| `couplings.weak_conversion.decay.after_periods` | The meeting under the rule at which the neutron breaks, its decay table (Highlights 5.4 point 20, clock-readings-v1) | A9 |
| `couplings.weak_conversion.shares` | The neutron's content shared among proton, electron and antineutrino | A9 |
| `couplings.weak_conversion.headings` | The headings of the three products | A9 |
| `couplings.pauli_exclusion.outputs` | What two electrons of opposite spin bind to (feature 11): the Born-form corner table with the guard on spin, loop-binding-v1 | hypothesis 12 |
| `couplings.transmission_meets_held_share.outputs` | The table between the transmission and the share waiting under its delay output, and where the two meet (a ray waiting at its event Node is met by nothing there since loop-binding-v1) | A3 |
| `couplings.beam_splitter.outputs.table` | The split ratio of the splitter | A2 |
| `couplings.slit.outputs.shares` | The share per forward heading of a slit | A1 |

## How a world selects rays from the catalog

There is no loader: a world file is written from the catalog, one
`spatial_fields` entry per selected ray and one `ray_interactions` rule per
selected coupling, and the test shows the mapping by building its worlds from
the file. A world names only the rays it holds and declares only the couplings
it uses; the layers follow.

| Catalog | World file |
| --- | --- |
| The ray id | `fields[].name` and `spatial_fields[].field` |
| `content`, `clock` | the thing's amount; `spatial_fields[].clock` with the world's `K` (clock-readings-v1; `kerengonen.phase_advance` is refused) |
| `charge` | `spatial_fields[].charge` |
| N | `N` on the world, once, 64 by default (`phase_bits` on a family is refused since the cleanup of 2026-09-18) |
| `polarization` and `polarization_bits` | `spatial_fields[].polarization_bits` (the world's N when absent), `emissions[].polarization` on a lamp, `polarization` on a meeting's output; the electron's `polarization_bits` 1 is spin |
| `release`, the size of the shadow set | `spatial_fields[].release` on the family itself and `initial_field`, the prefill (`bit-law-v1`): a shadow is a ray of the same family with the bit 0; `field_of` and `kind: field` are refused since 2026-09-18 (no field family, Highlights 5.4, point 12) and the mass field is retired (point 18) |
| A coupling's `participants`, `outputs` or `momentum_table` with `reads`, `invariants` | One `ray_interactions` rule |
| `apparatus.detector` | `detectors[]` with `position`, `setting` (the mark's table `[n, d]`, no seed: there is no lottery) and the optional `on_click` (`"absorb"`, the default for every family, or `"pass"`, for every ray family or per family, the resident thing's table, `detector-absorb-v1`); the couplings on the bit, a rule's `bit` key and the world's `return_mode` are retired (`bit-law-v1`, the cleanup of 2026-09-18) |
| `apparatus.external_body` | `external_bodies[]` with `position`, `family`, `amount` (the body's content) and the optional `charge`, `phase`, `initial_momentum`, `coupling` (`"sink"`, `"polarizer"` or a declared rule's name), `momentum_table` with its `reads` (`"content"` or `"charge"`, what the body multiplies the shadows' message by, `bit-law-v1` point 16) and `thing` (its identity, the owner its shadows carry) ([external body](SPATIAL_FIELDS.md#the-external-body-external-body-v1)); a coupled body's rule names the body's family for the apparatus role and returns its token once; a polarizer body writes `polarizer` (`family`, `angle`, `pass`, `table`, `unpolarized`) beside `coupling` ([polarization](SPATIAL_FIELDS.md#polarization-ray-polarization-v1)); a body radiates nothing, its shadows are given with the board (`initial_field`, `bit-law-v1`) |
| A bound group | A loop: rays circulating on a ring of Nodes under the corner table, one `ray_interactions` rule with outputs per binding coupling, as `examples/nature/ring.json` declares the unit-square electron ([binding as a loop](SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1), [loop binding](LOOP_BINDING.md); Highlights 3.4, 2026-09-17); nothing holds and no key names the group, which a reader finds in the record. The held form (a rule without outputs assigning `delay` 1, `ray_delay`) was removed by feature 14 on 2026-09-17 |
| A source | A marked Node that emits the family: a lamp on a Node with a mark of setting 1 |
| A bound group's decay | `decay: {"after_periods": n}` or `{"content_at_most": c}` on the conversion's `ray_interactions` rule, declared before the group's corner table: the group breaks at the meeting where the condition on its own state is met, nothing drawn (Highlights 5.4, point 20; `clock-readings-v1`, 2026-09-18); `draw` and `seed` are refused (the `decay-draw-v1` of 2026-09-17, [a decaying group draws](SPATIAL_FIELDS.md#a-decaying-group-draws-decay-draw-v1)) |

A bound group's decay has its world key since 2026-09-18 (`decay` on the
conversion's rule, the table of `clock-readings-v1`; the neutron's ring under
`quark_binding` is not yet declared, so `weak_conversion` stays open);
colour has no world key yet; its catalog records wait for it, and no
engine rule is added for it
([ray-event model, after feature 10](RAY_EVENT_MODEL.md#6-migration-in-order)).
Polarization has its keys since feature 11 (2026-09-17, above).
The split table of feature 12 (`spread` on a ray spatial field,
`field-spreading-v1`, 2026-09-17) is retired since 2026-09-18 by the Node's
mixing (`node-mixing-v1`, Highlights 5.4, point 24), which declares
nothing; the sign a shadow carries is its owner's charge sign, set by the
engine and declared by no one.

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
today (light, the electron, the positron and the gluon), for every shadow set
a world can declare today (the electron's and the positron's, one shadow of
the thing given with the board and mixed by the Node) and for every decided
coupling the engine runs today (the Born steering, the electron pushed by
its own family's shadows, and an external body under the absorber, the
mirror, the phase plate and the polarizer), runs each for two ticks against
pinned integers, and checks that a Detector mark parses. `tools/check.py` selects it when the catalog, this
document, the register or the hypotheses change. Passing it establishes the
file's contract, not any agreement with nature: that is the register's.
