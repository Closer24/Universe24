# The catalog of the entities

The model owner's decision of 2026-09-20 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
"DECIDED: the catalog of the entities"), in the owner's words, translated:
"Make sure that every entity the world of physics knows exists in our
entity definitions, and that we can also support external ones such as the
sun, a planet, a neutron star, so that they can be placed on the GameBoard
and things tested." This document is that catalog: every entity physics
knows as one row of the law's keys, the external things beside them, each
with the world file that places it on the GameBoard, and the honest list of
what the law cannot yet place. The definitions layer, how a reusable entity
is authored in a file and placed by a world, is owned by
[entity definitions](ENTITY_DEFINITIONS.md); the law whose keys the rows are
written in is [the law of the ray](RAY_LAW.md) with
[the engine's bookkeeping](ENGINE.md); the register that tests things on
these placements is [the experiments register](EXPERIMENTS.md). Nothing here
is a result: a row says what a thing is on the GameBoard and what a detector
reads of it, never what a reading measured.

The principles the rows follow, all of 2026-09-20 (Highlights 5.4): on the
GameBoard an entity is a family, one row of keys, and the engine does not
know which is which; a composite is a set of measured events bound by a
column and seen as one by a detector whose set covers it; an external thing
is a measured event with a table, a lamp, or a detector's set; our laws are
on the GameBoard and in the detector one sees other laws, so the name of an
entity is the detector's world's and the row is the GameBoard's; and on the
GameBoard there are only events, what a row calls a ray being the record of
an event in transit (`NatureBeam`).

## How to read a row

The keys of a row are the keys of the world file as
`src/event_universe/events/world.py` accepts them on 2026-09-20 (its
`WORLD_KEYS`, `FAMILY_KEYS`, `MEASURED_KEYS`, `LAMP_KEYS`,
`TABLE_ENTRY_KEYS`, `TRANSIT_KEYS` and `DETECTOR_KEYS`;
[RAY_LAW section 2](RAY_LAW.md#2-the-record-of-a-ray-and-the-world-file);
the refusals in [the engine](ENGINE.md)):

- a **family**: `name`; `quantum` (h, required: 0 a free family, matter,
  whose rays carry no content and are read for gravity and electricity; 1
  or more a paid family, light, released only by a lamp at the cost h x s
  content per unit at a self-creation whose turn is s, E = h f); `charge`
  (rho, the charge per unit of content, an integer or a pair `[n, d]`; 0
  by default; refused on a paid family); `phase` (true by default; false:
  no phase circle); `phase_per_link` (0 .. N - 1, the steps a ray of the
  family turns at every Link). The content of a thing is not a family key:
  it is its measured event's `amount`;
- a **measured event**: `position`, `family`, `amount` (its content),
  `phase`, `momentum` (three integers in label units, Q = 64 per unit of
  amount along a heading), `fixed` (held in place: pushes taken into its
  momentum, never a step), `span` (three odd integers: a body on a set of
  Nodes with one record), `phase_by_momentum` (with the world's `action`:
  the turn by momentum), `directions` (what it releases and re-emits on),
  `table` (per family `read`, `measure`, `rerelease` or `pass`, or
  `{"rule": ..., "phase_window": s, "reads": component}`; the table is
  generated from the families' keys, a free family read and a paid one
  measured, and a world declares only what differs), `lamp` (`rate`,
  `directions`, `phase_window`: a measured event of a paid family that
  releases it);
- a **detector**: `name`, `positions` (a set of measured events with ONE
  record), `threshold`, `reading` (`wave`, the square of the coherent
  pointer over the set, or `beam`, the count after the pairing by
  opposite phase); an open face of the GameBoard is a detector named
  `face:+x` and the five others; a measured event outside every declared
  set is a detector of one Node;
- a **ray at the start** (`in_transit`): `position`, `family`, `number`,
  `direction`, `amount`, `phase`, `age`;
- the **world's** keys a row leans on: `release` (a free family's rate,
  per direction per self-creation per unit of content), `suspension`
  (the width of the clock's count), `width` (S, the width of the push),
  `action` (h, the quantum of action of the turn by momentum),
  `age_bound`, `directions` (the fan a lamp or an emitter may name),
  `boundary`, `K`, `N`.

A row names only keys that exist. Where a thing needs a key the law does
not have yet, the row's "Waits for" column names it in bold. Four changes
are in flight on 2026-09-20 (Highlights 5.4: "one mechanism for all the laws
on the GameBoard", the decisions on the strong force's column and range and
on the weak force arranged in the world's terms), and the rows wait for them
by these names:

| Waits for | What it is | Its state |
| --- | --- | --- |
| **sigma** | the strong column: the one coupling as a signed inner product over the columns a family declares per unit of content, `push = M_A x (sum over the columns c of epsilon_c x c_A x c_B) x flow`, gravity the column every family has with the value 1 and the sign minus, the electric column rho with the sign plus, and a third column sigma with the sign minus; a column's sign a key and not a formula | decided (the owner: "as long as it enters the whole of the laws"); the mathematician verifies the form before the implementation |
| **L** | the lifetime, a family key: the event in transit whose age reaches L makes no next event but an escape click in the ledger, the range of a force; absent for ever-living families | decided (the owner: "excellent, go for it") |
| **the transformation** | a fifth table entry beside `read`, `measure`, `rerelease` and `pass`: a measured event turned into another family and the rest released, the books moving the content between the families' lines, the charge conserved | sent to the physicist as a read-only design (the weak force in the world's terms) |
| **a hand** | a family with a handedness under the 48 signed axis permutations of the GameBoard: parity violation, the one thing the law lacks for the weak force | named, not designed |

"What a detector reads of it" is always a detector reading, the only kind
reality has ([the experimenter's rule](../skills/experimenter/SKILL.md)): a
click at a set with its amount, content, phase and number; a set's `wave`
record or `beam` count; a probe's `read` records (the push taken); a clock's
owed count (`waited` against `age`). A GameBoard reading (a body's Node, its
steps, the books, the dense count at a Node) describes the mechanism and is
never the measurement.

## The fundamental things

| Entity | What it is on the GameBoard | Its keys today | Waits for | What a detector reads of it | World file that places it |
| --- | --- | --- | --- | --- | --- |
| The electron | a free family; its measured event a body | `quantum` 0; `charge` the electron's rho, negative, an integer or `[n, d]` (series H declares -15 against the proton's `[1, 1]`: the scale of the charge is a declared number, the three ratios of electric to gravity coming out in the proportions 1836^2 : 1836 : 1 from the form of the coupling alone); `phase` true; `phase_per_link` 0. The measured event: `amount` its content (1836 in series H, the proton's, so that both release at the world's one `release`), `momentum` (tangential for an orbit), `fixed` false, `span` `[1, 1, 3]` (the owner's "electron of width 3"), `phase_by_momentum` true with the world's `action` (Bohr's turn), `directions` the four in-plane headings; its table the keys' (`read` of the proton's rays: the push; `measure` of light: absorption, with a `phase_window` for a line) | nothing, to be placed; **the transformation** and **a hand** for what the weak force does with it | its released rays (free: its phase, no content) clicked by a `wave` detector, the open faces of series H; a probe's `read` of its field; a set covering its body reads "one electron, in one of these" | [`bohr/r8.json`](../examples/events/bohr/README.md) |
| The muon, the tau | free families with the electron's keys and a content 207 and 3477 times the electron's per measured event; the charge -e on the larger content is a smaller charge per unit of content, so each is a family of its own (one rho per family) | `quantum` 0; `charge` `[n_e, 207 d_e]` and `[n_e, 3477 d_e]` in the pair form, to the pair's grain; `phase` true; the measured event's `amount` the content | **the transformation** (the decay at rest, triggered by a count of its clock: the muon into an electron and two neutrinos) | as the electron's while it lives; its decay nothing today | none placed (placeable as the electron is) |
| The three neutrinos | a free family of `charge` 0 with a phase circle that every table passes and that a detector measures only within a narrow window (the weak design: a cross-section without a draw); one family per flavour | `quantum` 0; `charge` 0; `phase` true; on every other measured event the declared entry `{"nu": "pass"}` (a free family is read by default, gravity), on the detector `{"nu": {"rule": "measure", "phase_window": s}}`; a source a measured event of the family releasing at the world's `release` | **the transformation** (its birth in a decay); **a hand**; a change of family in flight (oscillation) has no key and is not in design | a click within the window at a set; nothing else | none placed (a source of a free family is placeable today) |
| The six quarks | not modelled: the nucleon is a family (the owner, 2026-09-20); if wanted, families `u`, `d` and the rest with the rational charges `[2, 3]` and `[-1, 3]`, ordinary values of the pair form, three measured events bound at adjacent Nodes by sigma | `quantum` 0; `charge` `[2, 3]`, `[-1, 3]`; `phase` true | **sigma** (the binding); colour has no key (the gap list); confinement a statement of the detector's world (no set at the nucleon's scale resolves one of the three) | a set covering the three reads the sum of their columns (the proton 2/3 + 2/3 - 1/3 = 1) | none |
| The photon | a paid family: a unit released by a lamp at a self-creation whose turn is s costs the emitter h x s content, carries it and the momentum h s u_d (E = h f); a click measures it | `quantum` h from 1; `charge` 0 (refused otherwise); `phase` true; `phase_per_link` its declared rate in transit (0 in the shipped worlds: the phase is the lamp's clock at birth); ever-living; released by a `lamp`; met by `measure` (the click), `rerelease` (a mirror, an opening), `pass` (glass) or `read` (a report of its label, the ray going on); its push on a reader its label alone, +V (radiation pressure) | the universal column on a paid family is the design's to state: today a paid ray is pulled by nothing and bent by nothing (the gap list) | the click's amount, content and phase; a set's `wave` record (the fringes; A10's spread) or its `beam` count; a face's record of what left | [`two_slits.json`](../examples/events/README.md), [`bell/`](../examples/events/bell/README.md), [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md), [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| The W and the Z | a weak family with the lifetime L of 1 or 0 (the weak design): a family of events in transit that end after L Links, whose click on a measured event's table transforms it | `quantum` (paid or free, the design's to say); `charge` `[1, 1]` and `[-1, 1]` for the W, 0 for the Z | **L**, **the transformation**, **a hand**; the electroweak scale and its broken symmetry are the detector's world's, for the physicist to state | nothing today | none |
| The gluon | the strong family's rays: a family of rays of its own carrying the sigma column with a lifetime L, the range | none today | **sigma**, **L**; colour has no key | nothing today | none |
| The Higgs | not in the law: the content of a measured event is its declared `amount`, and no mechanism gives it | none | not in design (the gap list) | nothing | none |
| The graviton | what the law has instead: gravity is the -1 of the one coupling, `M_A x (rho_A rho_B - 1) x V_B`, read off every free family's rays by every measured event whose table reads them, in the design the universal column with the value 1 and the sign minus; no family is the mediator, no ray carries content for it and no thing is placed for it | the free family's `quantum` 0; the world's `release`; the reader's `read` entry (the default of a free family) | nothing: the column exists | a probe's `read` records (the push; series C), a clock's owed count (the presence, M / r^2, or the age moment, M / r; series E) | [`one_content.json`](../examples/events/README.md), [`coupling/`](../examples/events/coupling/README.md), [`redshift/`](../examples/events/redshift/README.md), [`catalog/clock_near_mass.json`](../examples/events/catalog/README.md) |

## The composites

| Entity | What it is on the GameBoard | Its keys today | Waits for | What a detector reads of it | World file that places it |
| --- | --- | --- | --- | --- | --- |
| The proton | a family today (the nucleon is a family): free, `charge` `[1, 1]` in the atom's units; as three quarks a bound set (above) | `quantum` 0; `charge` `[1, 1]`; the measured event `amount` 1836, `fixed` in series H, `directions` a fan of 2616 primitive directions | **sigma** for the nucleus | its field by a probe or a clock; the atom's lines at the faces (series H) | [`bohr/r8.json`](../examples/events/bohr/README.md) |
| The neutron | a free family of `charge` 0 (content 1839 in the atom's units); beside a proton it binds today by the -1 alone at one Link, each pulling the other and a step onto an occupied Node refused (the contact) | `quantum` 0; `charge` 0; the measured event's `amount` | **sigma** (nuclear binding at nature's scale of rho, where the -1 is negligible); **the transformation** (beta decay, triggered by its clock) | its field by a probe or a clock | [`catalog/neutron_star.json`](../examples/events/catalog/README.md) |
| The deuteron | a bound set of a proton and a neutron at adjacent Nodes, held today by the -1 column and the refused step, its content 1836 + 1839 exact (no mass defect: a free ray carries no content); seen as one by a detector whose set covers both | two measured events of the families `p` and `n` at adjacent Nodes | **sigma** (the binding beyond the declared small rho); the contact rule (the momentum grows at the refused step, a recorded defect for the strong-force design) | one click of a set covering both; its field | none in the catalog (series I registers it; `catalog/neutron_star.json` places eight nucleons the same way) |
| The alpha | the 2 x 2 square p n / n p on the GameBoard (the owner's "explain alpha", 2026-09-20): four sigma bonds at one Link, the two protons on the diagonal at sqrt 2 where the electric push is half its one-Link value | four measured events at the four Nodes of a square | **sigma** with **L** at least 2 (the diagonal); today the two protons at rho 1 read zero between them (rho^2 - 1 = 0) | one click of a set covering the four; alpha decay the push of the other protons of a nucleus exceeding the hold, the cluster pushed out as one | none (series I) |
| The light nuclei | sets of nucleons at adjacent Nodes; saturation from the range L (a fifth nucleon on the square's side finds one or two bonds against the push of two protons: He-5 and Li-5 unbound in the model as in nature) | measured events at adjacent Nodes | **sigma**, **L** | as the alpha's | none (series I) |
| The hydrogen atom | a proton fixed at the centre and an electron body with a tangential momentum, the world's `action` and the body's `phase_by_momentum` giving Bohr's turn, de Broglie's closure 4 p r = j h on the lattice; its detector the open faces (`wave`) receiving the electron's rays, or a lamp's beam shot at the atom and read behind it (absorption: the electron's entry with a `phase_window`) | `action`; the electron's `span`, `phase_by_momentum`, `momentum`; the proton's `directions` (the fan) | nothing to place; a closed orbit is the register's open finding (series H: no orbit closed on the lattice's whole kicks, nothing tuned) | the faces' coherent record per turn and cumulatively; the lines | [`bohr/r8.json`](../examples/events/bohr/README.md) |
| Helium | an alpha nucleus and two electrons of one family at two Nodes (their mutual push M (rho_e^2 - 1): repulsion) | the alpha's and the electron's | **sigma** (the bound nucleus) and quantization (the owner's record: "helium waits on a bound nucleus and on quantization") | as hydrogen's | none |
| A molecule | two atoms bound through their electrons | the atoms' | the bound atom first; no key for a bond beyond the columns (the gap list) | as the atoms' | none |

## The external things

| Entity | What it is on the GameBoard | Its keys today | Waits for | What a detector reads of it | World file that places it |
| --- | --- | --- | --- | --- | --- |
| The sun, a star of content M | a composite of two measured events at adjacent Nodes, since a measured event has one family: its mass (a free family, `fixed`, content M, releasing on a fan: gravity, read as the push) and its lamp (a paid family with a `lamp` on a fan: light) | the mass: `family` free, `amount` M, `fixed` true, `directions` the fan, the world's `release`; the lamp: `family` paid, `amount` below K x N / 2, `fixed` true, `lamp` `{"rate": [n, d], "directions": [...]}` | one measured event that both pulls and shines: the design of the universal column (today a paid family carries no charge and a lamp is of a paid family) | its light as clicks and the `wave` record of a screen; its gravity as a probe's `read` or a clock's owed count | [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| A planet | a free body: `fixed` false, `momentum` tangential (the circular orbit's, derived by the generator from the fan's flux on the body along the engine's flight lines), `span` `[3, 3, 1]` over the fan's grain, a content far above h x s so that gravity's push, proportional to the reader's content, is far above the light's, the unit's label alone; it reflects light by `rerelease` on its `directions` | `amount`, `momentum`, `span`, `fixed` false, `table` `{"light": "rerelease"}`, `directions` | nothing | the light it reflects at a screen (a click's `number` the planet's: its transit across the screen); its gravity by a probe | [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| A moon | a planet's planet: a free body of smaller content with a momentum about the planet, which is free and takes the moon's push | as the planet's | nothing | as the planet's | none placed (as `catalog/sun_planet.json` with a third body) |
| A neutron star | a bound set of neutron measured events at adjacent Nodes of large content, free, held at one Link by the gravity column alone (each pulls its neighbours; a step onto an occupied Node is refused; in nature too a neutron star is bound by gravity); the content the largest a run's pushes allow, M_A x (the row's amount) x Q per arriving row within 2^62 - 1 | measured events of a free family at adjacent Nodes, `amount` 2^26 each, `fixed` false, the six headings; probes of content 1 with `pass`, one with `reads: "age"`; `suspension` `[1, d]` | the contact rule (the momentum grows at the refused step, within the bound for a short run); degeneracy pressure is not in the law (a body's size is its declared set) | the presence and the age moment on the clocks of probes at a radius (M / r^2 and M / r from the same rays); the crowd slowing the star's own clocks and with them its releases | [`catalog/neutron_star.json`](../examples/events/catalog/README.md) |
| A white dwarf | a star, a mass and a lamp, with a white dwarf's numbers; no key distinguishes it from the sun but its content and its lamp's rate | as the sun's | nothing (as the sun's) | as the sun's | none placed (as `catalog/sun_planet.json` with other numbers) |
| A black hole | not placeable as itself (the gap list): the law offers two readings, (i) the content bound, a body whose pushes pass 2^62 - 1 refuses the run, and (ii) a body whose clock the crowd stops, which then releases nothing, dark, its pull ending with its last rays | none | a field that is not paid by the emitter's clock; not in design (the owner's item) | see the gap list: the clicks of its light end and a probe's clock resumes its free rate, the opposite of a horizon | none |
| A galaxy | many stars: many mass measured events, each a star composite, placed up to the host's cost (series E placed 6985 measured events); series G throws sources from a centre for the Hubble diagram | many measured events, each a star's | nothing | the sum of the stars' light at a set; per source the redshift (the rate of the pointer's turn in the record) and the distance (the age of the arriving rays; series G) | none in the catalog (series G's worlds when registered) |
| A comet | a free body of small content on an eccentric path (a momentum off the circular orbit's at a large radius), shining by reflected light | as the planet's | its tail: a body that sheds matter has no key (a decay as a table on a measured event is the owner's open item; the gap list) | as the planet's | none placed |
| A lamp | a measured event of a paid family that releases it: `lamp` `{"rate": [n, d], "directions": [...], "phase_window": s}`, `rate` units per self-creation per direction, the release at a self-creation whose turn is s costing h x s content per unit, the recoil taken | `lamp`; the family's `quantum` from 1 | nothing | nothing of its own: what it lights | [`two_slits.json`](../examples/events/README.md), [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| A laser | a lamp with one direction and a `phase_window`: a release only at the self-creations whose clock phase falls in the half circle centred on the setting, so it releases in pulses of one phase range on one line | `lamp` `{"rate", "directions": [one], "phase_window": s}` | nothing | as the lamp's | [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) |
| A mirror | a `rerelease` entry: what arrives is created again at the next self-creation on the measured event's `directions`, the amount apportioned whole, the phase and the content kept, the number the mirror's, the age 0, the recoil -(out) + (in); one direction a plane mirror turning the beam, a fan a diffuser or an opening | `table` `{"light": "rerelease"}`, `directions` | nothing | what it returns, read at a set: the age the flight time since the mirror, the phase the mirror's (the owner's "a ray the detector sends, which returns to it") | [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md), [`two_slits.json`](../examples/events/README.md) (the openings) |
| A wall | `measure` with no release: a measured event of a paid family, content 1, `fixed`, with no `lamp`, whose entry for light is the one the keys give (the click: the content joins, the momentum pushes it, nothing leaves); a `measure` entry declared on a free family is a wall for gravity (the rays absorbed, no content joining) | a measured event of a paid family, `fixed` true, no `lamp`; on a free family `table` `{"m": "measure"}` | nothing | its own record as a detector of one Node (`wave` by default): what it absorbed | [`two_slits.json`](../examples/events/README.md), [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) |
| A slit | a wall with one or more Nodes whose entry is `rerelease` on a fan of `directions`; the opening's width the number of such Nodes (A10: 1, 3, 9, 27 Nodes) and, declared as a detector, its set | `table` `{"light": "rerelease"}`, `directions` the fan; `detectors[]` for the opening as a set | nothing | the spread behind it at a screen (the `wave` record narrowing with the width, the count never; A10) | [`one_slit.json`](../examples/events/README.md), [`heisenberg/`](../examples/events/heisenberg/README.md), [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) |
| A screen and a detector | `DetectorSet`: `detectors[]` `{"name", "positions", "threshold", "reading"}`, a set of measured events with ONE record (a click says "here, in one of these" and not which; the set's width is the position's uncertainty); a screen resolved in y is one-Node detectors, the pixels; a screen that is one set is one record; an open face is a detector named `face:+x` and the five others; a measured event outside every set is a detector of one Node | `positions`, `threshold`, `reading` `wave` or `beam`; a `phase_window` on the set's entries | nothing | the record: under `wave` the square of the coherent pointer and the set's phase (returned to its events after a click); under `beam` the count after the pairing; the clicks with their amount, content, phase and number | [`two_slits.json`](../examples/events/README.md) (pixels), [`catalog/sun_planet.json`](../examples/events/catalog/README.md) (one set), [`detector/`](../examples/events/detector/README.md) (placed from a definitions file) |
| A clock | a measured event whose owed count is read: with `suspension` `[n, d]` it owes `by_clock(age, k x n, d)` intervals after each self-creation, k what its clock counted over every ray of another number at its Nodes (the presence, or the age moment on an entry that reads `age`); its rate `age / (age + waited)` in the record | `suspension`; the entry's `reads` (`scalar`, or `age` for M / r); `span` for a body that averages the fan's grain | nothing | its `age` and `waited` in `run.json` (the redshift between two clocks: series E) | [`catalog/clock_near_mass.json`](../examples/events/catalog/README.md), [`redshift/`](../examples/events/redshift/README.md) |
| A probe | a measured event of content 1 with `pass` (no push, no record; the clock counts all the same) or `read` (the push taken and recorded: the `read` lines carry it) | `amount` 1, `fixed` true, `table` `{"m": "pass"}` or the default `read` | nothing | its `read` records (the field; series C) or its clock (above) | [`coupling/`](../examples/events/coupling/README.md), [`redshift/`](../examples/events/redshift/README.md), [`catalog/`](../examples/events/catalog/README.md) |
| Dark matter | a free family with no columns but gravity's: `charge` 0, its measured events declaring `pass` for every paid family (transparent to light); placeable today, distinguished from a neutron by its table alone | `quantum` 0, `charge` 0, `table` `{"light": "pass"}` | nothing | its gravity by a probe or a clock; no light | none placed (as `catalog/neutron_star.json` with `pass` for a light family) |

## The gap list

Every entity or property the law cannot yet place, with what the law has,
the key it would need and whether it is in design.

| Gap | What the law has today | The key it would need | In design? |
| --- | --- | --- | --- |
| Colour and confinement | the columns are rational pairs, so a quark's charge is an ordinary value; a nucleon of three measured events bound by sigma at adjacent Nodes; confinement a statement of the detector's world (no set at the nucleon's scale resolves one of the three) | sigma first; a colour column with a neutral sum of three has no form yet | sigma decided; colour recorded as a series after the strong force lands, if the owner wants it |
| The Higgs and mass generation | the content of a measured event is its declared `amount` | a mechanism that gives a content; none named | not in design |
| A black hole | (i) the bound: an `amount` at most 2^62 - 1 and every push M_A x V within it; a body beyond it refuses the run at the first push past the bound (an `OverflowError` naming it), the law's statement that it cannot be placed; (ii) a body whose clock the crowd stops: with `suspension` on, a member of a dense enough set owes so many intervals that it never self-creates again, so it releases nothing and steps nowhere, and its gravity, which is its releases, ends when its last rays in flight have left. The reading a black hole would give under (ii): the clicks of the set's light end at every detector, a probe's `read` count falls to nothing and its clock returns to its free rate, the opposite of a horizon; under (i) there is no reading, the run is refused | a field that is not paid by the emitter's clock, so that a stopped clock keeps pulling | not in design; the owner's item in the catalog decision |
| Antimatter | the sign of the columns: a positron is a family with `charge` +rho_e, placeable today; the electric push between it and the electron attractive; nothing happens when they meet but the refused step | **the transformation** for annihilation and pair creation (the content moved between the families' lines and light released) | the weak design's entry |
| Spin and polarization | the record carries a direction and a phase; nothing on it turns with a hand under the 48 symmetries; a phase window reads the phase, not a polarization | a hand; "polarization as worlds and tables" is the owner's open item | named, not designed |
| Molecules and chemistry | the atom (series H open), helium (sigma) | a bond: nothing beyond the columns; no key | not in design |
| Dark energy | nothing: the GameBoard's shape is fixed and no term pushes everything apart; the Hubble diagram is read from a throw (series G: a coasting or a decelerating recession, whichever the detector reads) | none named | not in the law |
| Light bent, slowed or redshifted by a mass in flight | a ray in transit is moved by the flight table and turned by the collision table only; gravity acts on measured events; a paid ray pushes its reader by its label alone; the law's redshift is the clock's (series E), not the ray's | the universal column on a paid family says what a reader takes from it; what happens to the ray in flight has no key | not in design |
| Decays and lifetimes at rest (the muon, the tau, the neutron) | the clock of a measured event counts; a count of it "will trigger a decay in time" (the owner, 2026-09-20) | **the transformation** triggered by the clock's count | the weak design |
| The W and Z, the gluon | nothing | **L**, **sigma**, **the transformation**, **a hand** | decided and in design |
| Neutrino oscillation | three families; an event in transit changes family by nothing | a change of family in flight | not in design |
| Mass defect, binding energy | absent: a free ray carries no content, so the alpha's content is 2 x 1836 + 2 x 1839 exact | a binding that costs content | not in design |
| Tunnelling | absent: the GameBoard is deterministic, a nucleus holds or decays, and the only spread of decay times is the fan's grain | none | not in the law (the owner's record on alpha) |
| A body that sheds matter (a comet's tail, fission) | a measured event releases rays, never a measured event | a decay as a table on a measured event | the owner's open item |
| A star that pulls and shines as one measured event | two measured events at adjacent Nodes (`catalog/sun_planet.json`) | a paid family with the gravity column: the universal column of the design | the design of the one coupling |

## What could not be placed, and why

The judgements of the architect for the model owner, from the worlds of the
catalog ([their page](../examples/events/catalog/README.md)):

1. **A black hole cannot be placed, and the law's dense body is dark and
   weightless.** A measured event's field is its releases and its releases
   come at its self-creations, which the crowd's count postpones
   (`suspension`): a body whose clock the crowd stops releases nothing,
   so a detector reads no light from it and, once its rays in flight have
   left, a probe reads no pull either. The neutron star of the catalog
   shows the beginning of it: the eight neutrons count each other's rays
   and their clocks slow, and with them their releases. In nature a black
   hole keeps its gravity; here a stopped clock is a stopped field. The
   other reading, the integer bound, is a refusal and not a thing on the
   GameBoard.
2. **A star is two measured events.** A measured event has one family; a
   paid family carries no charge and a lamp is of a paid family, so what
   pulls (a free family releasing at the world's rate) and what shines (a
   lamp) are two events at adjacent Nodes. The design of the universal
   column may or may not give a paid family the gravity column; until it
   says, the sun is a composite.
3. **Light is pulled by nothing and bent by nothing.** A paid ray pushes
   its reader by its label alone (radiation pressure) and takes no push
   in flight. The redshift the law reads is the clock's, series E.
4. **The nucleus, the quarks, the gluon, the W and Z, the decays wait**
   for sigma, L and the transformation entry, all decided or in design;
   colour and the hand have no key.
5. **The contact at one Link is a recorded defect.** Two bodies held at
   one Link by the gravity column keep pushing each other; the refused
   step keeps the momentum, which grows every interval until the integer
   bound refuses the run. The catalog's neutron star is sized so that a
   run of forty intervals stays within the bound (a push of 2^50 per
   arriving row); a heavier star, a faster release or a longer run needs
   the contact rule sent to the strong-force design.
6. **The width of a body is a width of its push.** A body on a set of w
   Nodes reads about w times one Node's flux at the same content (RAY_LAW
   note 30), so the planet's circular orbit on nine Nodes needs the
   world's `width` of the push large (512) to be slow; the generator
   derives the momentum from the engine's own flight lines and prints it
   as a GameBoard reading of the design. Whether an orbit closes is the
   register's question (series D and H).
7. **Dark matter is placeable and dark energy is not.** A free family of
   charge 0 whose measured events pass light is dark matter to every
   detector; nothing in the law pushes everything apart.

## The worlds of the catalog

| World | Places | Read by |
| --- | --- | --- |
| [`catalog/sun_planet.json`](../examples/events/catalog/README.md) | the sun (a mass and a lamp), a planet (a free body on a set, reflecting), a screen (one set) | the screen's `wave` record and its clicks by number; the planet's `read` records |
| [`catalog/neutron_star.json`](../examples/events/catalog/README.md) | a neutron star (eight neutrons bound at one Link), six probes | the probes' clocks: the presence on five, the age moment on one |
| [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) | a laser, a mirror, a wall with a slit, a screen as pixels | the pixels' `wave` records |
| [`catalog/clock_near_mass.json`](../examples/events/catalog/README.md) | a mass on a fan, two clocks (bodies on sets) at two radii | the clocks' owed counts |

`tests/test_entity_catalog.py` checks that each world is what its page says
(it parses, declares its keys, runs with the books balanced, and its
readings exist) and pins no number
([expectations](TEST_EXPECTATIONS.md#the-entity-catalog)). The register
tests things on them later.
