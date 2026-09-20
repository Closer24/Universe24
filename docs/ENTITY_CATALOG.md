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
written in is [the Beam Law](BEAM_LAW.md) (the owner's name of 2026-09-20
for the law of the ray of 2026-09-19: the identity `beam-v1`, the world key
`"law": "beam"`; the quotations of the day keep their wording) with
[the engine's bookkeeping](ENGINE.md); the register that tests things on
these placements is [the experiments register](EXPERIMENTS.md). Nothing here
is a result: a row says what a thing is on the GameBoard and what a detector
reads of it, never what a reading measured. What a row calls a ray is the
informal name of a beam, `NatureBeam`, the record of an event in transit;
the catalog's generator and test read the law's value from `world.py` and
not from a literal.

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
[BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file);
the refusals in [the engine](ENGINE.md)):

- a **family**: `name`; `quantum` (h, required: 0 a free family, matter,
  whose rays carry no content and are read for gravity and electricity; 1
  or more a paid family, light, released only by a lamp at the cost h x s
  content per unit at a self-creation whose turn is s, E = h f); `charge`
  (rho, the charge per unit of content, an integer or a pair `[n, d]`; 0
  by default; on a paid family since 2026-09-20 a whole charge per unit of
  amount on the charge line only, D-1); `phase` (true by default; false:
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
  record), `threshold` (today the amount arriving over the set in one
  interval; under `wave` the pointer's square in units of one ray by the
  decision of 2026-09-20 on issue #359, in the next engine change),
  `reading` (`wave`, the square of the coherent pointer over the set, or
  `beam`, the count after the pairing by opposite phase); an open face of
  the GameBoard is a detector named
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
not have yet, the row's "Waits for" column names it in bold. The changes in
flight on 2026-09-20 (Highlights 5.4: "one mechanism for all the laws on the
GameBoard"; the physicist's designs of the strong and the weak force; the
mathematician's verdict on the columns; the owner's "go on everything"),
each by the name its design gives it:

| Waits for | What it is | Its state on 2026-09-20 |
| --- | --- | --- |
| **the strong column** | the one coupling as a signed inner product over the columns a family declares per unit of content, `push = M_A x (sum over the columns c of epsilon_c x c_A x c_B) x flow`, each column floored separately off the reader's clock: gravity the built-in column of value 1 and sign minus (a declared gravity refused), `charge` the shorthand for the electric column of sign plus, and a declared column with its sign, in the world file per family `"columns": {"strong": {"value": [n, d], "sign": -1}}`; no code path for any force | decided (the owner: "as long as it enters the whole of the laws"; then "go"); the mathematician's verdict: correct and working, the form equal to today's push integer by integer on 11,945 pushes of 46 registered worlds; in implementation |
| **`lifetime`** | a family key, L: the event in transit whose age reaches L makes no next event but an escape click on the border `lifetime`, the range of a force; its reach on the flight table: L = 1 the six neighbours, L = 2 also the face diagonals, L = 3 the cube diagonals and two Links; absent for ever-living families | decided (the owner: "excellent, go for it"); in implementation |
| **the held content** | a measured event holding content of several families, its charge the rational sum over what it holds (the register's proton: 1836 of a charged family and one unit of the strong family `nuclear`, strong 10000, lifetime 3), since a lifetime is a key of a family of rays and the electric rays live forever | decided with the strong force's "go"; in implementation |
| **the contact** | the refused step made generic through the table: a body that steps into a Node held by another measured event is an arrival at the occupant, and the occupant's entry for the body's family decides as for any arrival, `measure` handing the body's momentum component on that axis to the occupant (the pair's sum unchanged, each label bounded by one interval's push, a `contact` record), `rerelease` returning it (the body bounces); until it lands the momentum grows at the refused step | decided (the owner: "go"); in implementation |
| **`become`** | the transformation, a fifth table rule beside `read`, `measure`, `rerelease` and `pass`: a measured event becomes another family's event and releases the rest as rows born as a re-release is, the content exact, the charge conserved, a `became` line per family in the books; two triggers, the clock (`become: {at, into, products, crowd}`, fired at the self-creation whose clock reaches `at`, `crowd` a gate that fires only while the count the clock read is below it) and the click (a table entry with a phase window: the capture); the identity `weak-v1` | admissible (the physicist's design); the owner's "go" in the recommended order, after the neutrino (series J1, J3) |
| **`phase_width`** | a table-entry key, N / 2 by default (bit-identical to today's half circle whatever its centre): the admitted fraction of a window w / N exactly when the source's stride is coprime to N; a narrow window for a neutrino, nature's cross-section needing about three such gates compounded | landed on 2026-09-20 ([BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) (i); on a table entry and on a lamp); series J2 registered: 1 / 64 at the first reader, nothing behind it |
| **D-1** | a paid family may declare a whole charge per unit of amount, read on the charge line of the books only, the push untouched (without it a neutron's products are refused) | landed on 2026-09-20 ([BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) (ii)): the charge line conserved through a charged paid row's click, home and escape; a lamp on a charged paid family refused |
| **a hand** | `hand-v1`: an axial record and a right-hand rule in `become`, that family restricted to the 24 proper rotations of the GameBoard; parity is exact on the GameBoard today, the one thing the law lacks for the weak force | admissible; only if wanted later |
| **the `wave` threshold** | issue #359, step A: under the reading `wave` a detector set's `threshold` reads what the reading is, the square of the coherent pointer of the interval's arrivals in units of one ray (one ray 1, two in phase 4, two opposite 0), and under `beam` the amount as today; no memory between intervals (step B, the pointer kept on the detector, is refused: "a detector parameter that is not known to work in the real world") | decided (the owner: step A yes, step B no); the next engine change |

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
| The electron | a free family; its measured event a body | `quantum` 0; `charge` the electron's rho, negative, an integer or `[n, d]` (series H declares -15 against the proton's `[1, 1]`: the scale of the charge is a declared number, the three ratios of electric to gravity coming out in the proportions 1836^2 : 1836 : 1 from the form of the coupling alone); `phase` true; `phase_per_link` 0. The measured event: `amount` its content (1836 in series H, the proton's, so that both release at the world's one `release`), `momentum` (tangential for an orbit), `fixed` false, `span` `[1, 1, 3]` (the owner's "electron of width 3"), `phase_by_momentum` true with the world's `action` (Bohr's turn), `directions` the four in-plane headings; its table the keys' (`read` of the proton's rays: the push; `measure` of light: absorption, with a `phase_window` for a line) | nothing, to be placed; **`become`** and **a hand** for what the weak force does with it | its released rays (free: its phase, no content) clicked by a `wave` detector, the open faces of series H; a probe's `read` of its field; a set covering its body reads "one electron, in one of these" | [`bohr/r8.json`](../examples/events/bohr/README.md) |
| The muon, the tau | free families with the electron's keys and a content 207 and 3477 times the electron's per measured event; the charge -e on the larger content is a smaller charge per unit of content, so each is a family of its own (one rho per family) | `quantum` 0; `charge` `[n_e, 207 d_e]` and `[n_e, 3477 d_e]` in the pair form, to the pair's grain; `phase` true; the measured event's `amount` the content | **`become`** at the clock (`{"at": ..., "into": ..., "products": ...}`, fired at the self-creation whose clock reaches `at`): the decay at rest, the muon into an electron and two neutrinos; a moving muon's clock ticks in every interval in which its body steps (the owner, 2026-09-20: the engine stands, nature's gamma a limit of the law, not tuned in) | as the electron's while it lives; its decay nothing today | none placed (placeable as the electron is) |
| The three neutrinos | a free family of `charge` 0 with a phase circle that every table passes and that a detector measures only within a narrow window (the weak design: a cross-section without a draw); one family per flavour | `quantum` 0; `charge` 0; `phase` true; on every other measured event the declared entry `{"nu": "pass"}` (a free family is read by default, gravity: the neutrino gravitates and carries no content), on the detector `{"nu": {"rule": "measure", "phase_window": s, "phase_width": w}}` (since 2026-09-20 the window's width w, N / 2 by default: the admitted fraction w / N when the source's stride is coprime to N); a source a measured event of the family releasing at the world's `release` | **`become`** (its birth in a decay); **a hand**; a change of family in flight (oscillation) has no key and is not in design; the cross-section flat in energy, a plain disagreement with nature's linear rise, registered as the law's own prediction (series J2, measured: 1 / 64 at w = 1 whatever the emitter's rate) | a click within the window at a set; nothing else | [`weak/j2_filter.json`](../examples/events/weak/README.md) (a source of `nu` and 128 windowed readers) |
| The six quarks | not modelled: the nucleon is a family (the owner, 2026-09-20); if wanted, families `u`, `d` and the rest with the rational charges `[2, 3]` and `[-1, 3]`, ordinary values of the pair form, three measured events bound at adjacent Nodes by the strong column | `quantum` 0; `charge` `[2, 3]`, `[-1, 3]`; `phase` true | **the strong column** and **`lifetime`** (the binding); colour has no key (the gap list); confinement a statement of the detector's world (no set at the nucleon's scale resolves one of the three) | a set covering the three reads the sum of their columns (the proton 2/3 + 2/3 - 1/3 = 1) | none |
| The photon | a paid family: a unit released by a lamp at a self-creation whose turn is s costs the emitter h x s content, carries it and the momentum h s u_d (E = h f); a click measures it | `quantum` h from 1; `charge` 0 (refused otherwise); `phase` true; `phase_per_link` its declared rate in transit (0 in the shipped worlds: the phase is the lamp's clock at birth); ever-living; released by a `lamp`; met by `measure` (the click), `rerelease` (a mirror, an opening), `pass` (glass) or `read` (a report of its label, the ray going on); its push on a reader its label alone, +V (radiation pressure) | nothing, to be placed; a paid ray is pulled by nothing and bent by nothing, the law's own prediction (2), to be run as series K after series I (the gap list) | the click's amount, content and phase; a set's `wave` record (the fringes; A10's spread) or its `beam` count; a face's record of what left | [`two_slits.json`](../examples/events/README.md), [`bell/`](../examples/events/bell/README.md), [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md), [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| The W and the Z | the weak design: the W a paid family with `lifetime` 1 and no column (it holds nothing; measured, its push is its label), a family of events in transit that end after one Link, whose click on a measured event's table transforms it; L = 0 is no family at all, Fermi's contact form; no Z family, the neutral current a windowed re-release | `quantum` from 1; `charge` 1 and -1 for the W under D-1 (landed: a whole charge per unit of amount); `lifetime` 1 (landed) | **`become`**; **a hand** only if wanted; the electroweak scale and its broken symmetry, the W and Z masses fixing the scale, the propagator's rise and V-A have no counterpart (the physicist's design, registered as limits) | nothing today | none (the W world after series J1 to J3) |
| The gluon | the strong family's rays: a family of rays of its own carrying the strong column with a `lifetime`, the range (the register's strong family `nuclear`, strong 10000, lifetime 3, is its place; the strong reading a square well, not Yukawa's exponential, a stated difference from nature) | none today | **the strong column**, **`lifetime`**; colour has no key | nothing today | none (series I) |
| The Higgs | not in the law: the content of a measured event is its declared `amount`, and no mechanism gives it | none | not in design (the gap list) | nothing | none |
| The graviton | what the law has instead: gravity is the -1 of the one coupling, `M_A x (rho_A rho_B - 1) x V_B`, read off every free family's rays by every measured event whose table reads them; in the columns form the built-in column of value 1 and sign minus, verified bit for bit against every registered push (the mathematician, 2026-09-20); no family is the mediator, no ray carries content for it and no thing is placed for it | the free family's `quantum` 0; the world's `release`; the reader's `read` entry (the default of a free family) | nothing: the column exists | a probe's `read` records (the push; series C), a clock's owed count (the presence, M / r^2, or the age moment, M / r; series E); the field of a moving body points to its retarded position (the push along the arriving u_d), the law's own prediction (3) | [`one_content.json`](../examples/events/README.md), [`coupling/`](../examples/events/coupling/README.md), [`redshift/`](../examples/events/redshift/README.md), [`catalog/clock_near_mass.json`](../examples/events/catalog/README.md) |

## The composites

| Entity | What it is on the GameBoard | Its keys today | Waits for | What a detector reads of it | World file that places it |
| --- | --- | --- | --- | --- | --- |
| The proton | a family today (the nucleon is a family): free, `charge` `[1, 1]` in the atom's units; for the register of the nucleus a measured event holding 1836 of a charged family and one unit of the strong family `nuclear`; as three quarks a bound set (above) | `quantum` 0; `charge` `[1, 1]`; the measured event `amount` 1836, `fixed` in series H, `directions` a fan of 2616 primitive directions | for the nucleus: **the held content**, **the strong column** and **`lifetime`** 3 | its field by a probe or a clock; the atom's lines at the faces (series H) | [`bohr/r8.json`](../examples/events/bohr/README.md) |
| The neutron | a free family of `charge` 0 (content 1839 in the atom's units); beside a proton it binds today by the -1 alone at one Link, each pulling the other and a step onto an occupied Node refused (the contact) | `quantum` 0; `charge` 0; the measured event's `amount` | **the held content** and **the strong column** (nuclear binding at nature's scale of rho, where the -1 is negligible); **`become`** at the clock with the `crowd` gate (beta decay, fired only while the count its clock reads is below the gate: the bound neutron stable); **D-1** for its products | its field by a probe or a clock | [`catalog/neutron_star.json`](../examples/events/catalog/README.md) |
| The deuteron | a bound set of a proton and a neutron at adjacent Nodes, held today by the -1 column and the refused step, its content 1836 + 1839 exact (no mass defect in the content: a free ray carries no content); seen as one by a detector whose set covers both; the design: it binds at one Link and no strong ray reaches three | two measured events of the families `p` and `n` at adjacent Nodes | **the strong column**, **`lifetime`**, **the held content**; **the contact** (decided: through the table; until it lands the momentum grows at the refused step) | one click of a set covering both; its field; its binding energy as the clock's count (the bound clock slower at one Link, the one reading of a binding energy the law has) | none in the catalog (series I registers it; `catalog/neutron_star.json` places eight nucleons the same way) |
| The alpha | the 2 x 2 square p n / n p on the GameBoard (the owner's "explain alpha", 2026-09-20): four strong bonds at one Link, the two protons on the diagonal at sqrt 2 where the electric push is half its one-Link value; the physicist's design finds the square sheared (the p-p diagonal bond weaker than the n-n one) and ejecting a proton under the contact rule, while the line p n n p holds: on the lattice the alpha candidate is the line, and series I decides | four measured events at four adjacent Nodes | **the strong column** with **`lifetime`** at least 2 (the diagonal; a bond of tensile strength needs 3), **the held content**, **the contact**; today the two protons at rho 1 read zero between them (rho^2 - 1 = 0) | one click of a set covering the four; alpha decay the push of the other protons of a nucleus exceeding the hold, the cluster pushed out as one | none (series I) |
| The light nuclei | sets of nucleons at adjacent Nodes; the range `lifetime` on the flight table (L = 1 the six neighbours, L = 2 also the face diagonals, L = 3 the cube diagonals and two Links); the design finds He-5 and Li-5 bound at L >= 2: the law has no exclusion principle, a known difference from nature; a decay deterministic, one interval per world, no spread across the 48 orientations | measured events at adjacent Nodes | **the strong column**, **`lifetime`**, **the held content**, **the contact** | as the alpha's | none (series I) |
| The hydrogen atom | a proton fixed at the centre and an electron body with a tangential momentum, the world's `action` and the body's `phase_by_momentum` giving Bohr's turn, de Broglie's closure 4 p r = j h on the lattice; its detector the open faces (`wave`) receiving the electron's rays, or a lamp's beam shot at the atom and read behind it (absorption: the electron's entry with a `phase_window`) | `action`; the electron's `span`, `phase_by_momentum`, `momentum`; the proton's `directions` (the fan) | nothing to place; a closed orbit is the register's open finding (series H: no orbit closed on the lattice's whole kicks, nothing tuned) | the faces' coherent record per turn and cumulatively; the lines | [`bohr/r8.json`](../examples/events/bohr/README.md) |
| Helium | an alpha nucleus and two electrons of one family at two Nodes (their mutual push M (rho_e^2 - 1): repulsion) | the alpha's and the electron's | **the strong column** (the bound nucleus, series I) and quantization (the owner's record: "helium waits on a bound nucleus and on quantization") | as hydrogen's | none |
| A molecule | two atoms bound through their electrons | the atoms' | the bound atom first; no key for a bond beyond the columns (the gap list) | as the atoms' | none |

## The external things

Every external thing brought from the real world into the GameBoard (a
lamp, a source, a star, a mass, a mirror, a wall, a probe, a detector)
carries its uncertainty on the world's side exactly as the detector does,
and on the GameBoard it is certain (the model owner, 2026-09-20). Two
columns say it per row: **its widths on the world's side**, the set it is
declared on (`span` for a measured event, `positions` for a detector set)
and its phase window (`phase_window` on a lamp or on a table entry); and
**on the GameBoard**, the definite events it makes (a release at a Node, in
an interval, on a direction, with a phase, by the clock and the fan, no
draw; a click; a re-release). Which Node of an emitter's set released, like
which Node of a detector's set clicked, is not information the world has;
the GameBoard has both. Verified on the engine: a lamp of `span` `[1, 1, 3]`
releases over its three Nodes, 262146 + 262146 + 262140 = the one-Node
release 786432, apportioned whole by its age.

| Entity | What it is on the GameBoard | Its keys today | Its widths on the world's side | On the GameBoard | Waits for | What a detector reads of it | World file that places it |
| --- | --- | --- | --- | --- | --- | --- | --- |
| The sun, a star of content M | a composite of two measured events at adjacent Nodes, since a measured event has one family: its mass (a free family, `fixed`, content M, releasing on a fan: gravity, read as the push) and its lamp (a paid family with a `lamp` on a fan: light) | the mass: `family` free, `amount` M, `fixed` true, `span`, `directions` the fan, the world's `release`; the lamp: `family` paid, `amount` below K x N / 2, `fixed` true, `span`, `lamp` `{"rate": [n, d], "directions": [...]}` | the set each of its two events is declared on, `span` `[1, 3, 1]` in `catalog/sun_planet.json` (a star of width three; a measured event on one Node is `[1, 1, 1]`); a `phase_window` on the lamp for a star that shines in one phase range | at every self-creation of the mass a release of one row per direction of the fan at one Node of its set, in that interval, with the clock's phase, apportioned whole over the set by its age; at every self-creation of the lamp a release of `rate` units per direction at one Node of its set, each costing h x s; no draw | one measured event that both pulls and shines: **the held content** (a measured event holding the content of a free family and of a paid one) with a lamp on the paid part, or the built-in gravity column read off a paid family's rays, whichever the design says; today a paid family carries no charge and a lamp is of a paid family | its light as clicks and the `wave` record of a screen; its gravity as a probe's `read` or a clock's owed count | [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| A planet | a free body: `fixed` false, `momentum` tangential (the circular orbit's, derived by the generator from the fan's flux on the body along the engine's flight lines), `span` `[3, 3, 1]` over the fan's grain, a content far above h x s so that gravity's push, proportional to the reader's content, is far above the light's, the unit's label alone; it reflects light by `rerelease` on its `directions` | `amount`, `momentum`, `span`, `fixed` false, `table` `{"light": "rerelease"}`, `directions` | `span` `[3, 3, 1]`; a `phase_window` on its light entry for a planet that reflects one phase range | a step of the whole set by one Link in an interval where nothing is owed, by the step rule off its clock; a `read` of every arriving row at the Node it reached (the push); a re-release of a light row at one Node of the set on one of its directions at the next self-creation | nothing | the light it reflects at a screen (a click's `number` the planet's: its transit across the screen); its gravity by a probe | [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| A moon | a planet's planet: a free body of smaller content with a momentum about the planet, which is free and takes the moon's push | as the planet's | as the planet's | as the planet's | nothing | as the planet's | none placed (as `catalog/sun_planet.json` with a third body) |
| A neutron star | a bound set of neutron measured events at adjacent Nodes of large content, free, held at one Link by the gravity column alone (each pulls its neighbours; a step onto an occupied Node is refused; in nature too a neutron star is bound by gravity); the content the largest a run's pushes allow, M_A x (the row's amount) x Q per arriving row within 2^62 - 1 | measured events of a free family at adjacent Nodes, `amount` 2^26 each, `fixed` false, the six headings; probes of content 1 with `pass`, one with `reads: "age"`; `suspension` `[1, d]` | each neutron on one Node (`span` `[1, 1, 1]`; a neutron on a set would be one record on its Nodes) and the star the set of the eight; the probes one Node each; no window | at every self-creation of a neutron a release of one row per heading at its Node with no phase (the family has no circle); a step attempted and refused at every interval it owes nothing; at a probe a pass of every arriving row and the count off its clock | **the contact** (decided, generic through the table: the occupant's entry for the body's family takes the axis component or bounces it; until it lands the momentum grows at the refused step, within the bound for a short run); degeneracy pressure is not in the law (a body's size is its declared set) | the presence and the age moment on the clocks of probes at a radius (M / r^2 and M / r from the same rays); the crowd slowing the star's own clocks and with them its releases | [`catalog/neutron_star.json`](../examples/events/catalog/README.md) |
| A white dwarf | a star, a mass and a lamp, with a white dwarf's numbers; no key distinguishes it from the sun but its content and its lamp's rate | as the sun's | as the sun's | as the sun's | nothing (as the sun's) | as the sun's | none placed (as `catalog/sun_planet.json` with other numbers) |
| A black hole | not placeable as itself (the gap list): the law offers two readings, (i) the content bound, a body whose pushes pass 2^62 - 1 refuses the run, and (ii) a body whose clock the crowd slows without bound, never to zero (the rate 1 / (1 + k); no horizon, the law's own prediction (1)), releasing ever more rarely: dark and weightless in the limit, since its pull is its releases | none | none | none | a field that is not paid by the emitter's clock; not in design (the owner's item) | see the gap list: the clicks of its light thin out and a probe's clock returns toward its free rate, the opposite of a horizon | none |
| A galaxy | many stars: many mass measured events, each a star composite, placed up to the host's cost (series E placed 6985 measured events); series G threw twenty-four sources from a centre, a family each, chains on the six axes, with a detector of one Node at the centre | many measured events, each a star's; a thrown source a free measured event with a `momentum` releasing toward the detector | each star's set; series G's sources one Node each and its detector one Node, no window | each source's step by its momentum and its release toward the centre at its Node with its clock's phase; the detector's click of each arriving row | nothing; what series G found the law lacked is registered (a straight throw off the axes, a three-dimensional gravity of a crowd of points, a source releasing along its own motion without taking its row home) | the sum of the stars' light at a set; per source the redshift (the rate of the pointer's turn in the record) and the distance (the age of the arriving rays): the linear Hubble law by itself, z = v / c | [`hubble/`](../examples/events/hubble/README.md) ([G](EXPERIMENTS.md#g-the-hubble-diagram-behind-the-detector-2026-09-20)) |
| A comet | a free body of small content on an eccentric path (a momentum off the circular orbit's at a large radius), shining by reflected light | as the planet's | as the planet's | as the planet's | its tail: `become` releases its products as rows (rays), never as bodies, so a body that sheds bodies has no key (the gap list) | as the planet's | none placed |
| A lamp | a measured event of a paid family that releases it: `lamp` `{"rate": [n, d], "directions": [...], "phase_window": s}`, `rate` units per self-creation per direction, the release at a self-creation whose turn is s costing h x s content per unit, the recoil taken | `lamp`; the family's `quantum` from 1; `span` | `span` (verified on the engine: a lamp of `span` `[1, 1, 3]` releases over its three Nodes, 262146 + 262146 + 262140 = the one-Node release 786432, apportioned whole by its age) and its `phase_window` | a release at one Node of its set, in an interval, on each of its directions, of whole units with its clock's phase, by the clock and the fan, no draw | nothing | nothing of its own: what it lights | [`two_slits.json`](../examples/events/README.md), [`catalog/sun_planet.json`](../examples/events/catalog/README.md) |
| A laser | a lamp with one direction and a `phase_window`: a release only at the self-creations whose clock phase falls in the half circle centred on the setting, so it releases in pulses of one phase range on one line | `lamp` `{"rate", "directions": [one], "phase_window": s}`; `span` | `span`; its `phase_window` (the pulses) | a release on its one direction at the self-creations whose clock phase falls in the window, none at the others | nothing | as the lamp's | [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) |
| A mirror | a `rerelease` entry: what arrives is created again at the next self-creation on the measured event's `directions`, the amount apportioned whole, the phase and the content kept, the number the mirror's, the age 0, the recoil -(out) + (in); one direction a plane mirror turning the beam, a fan a diffuser or an opening | `table` `{"light": "rerelease"}`, `directions`; `span` | its set (`span`, or a row of Nodes); a `phase_window` on its entry for a mirror that returns one phase range | a re-release at the Node the row reached, at the next self-creation, on its directions, the phase and the content kept, the number the mirror's | nothing | what it returns, read at a set: the age the flight time since the mirror, the phase the mirror's (the owner's "a ray the detector sends, which returns to it") | [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md), [`two_slits.json`](../examples/events/README.md) (the openings) |
| A wall | `measure` with no release: a measured event of a paid family, content 1, `fixed`, with no `lamp`, whose entry for light is the one the keys give (the click: the content joins, the momentum pushes it, nothing leaves); a `measure` entry declared on a free family is a wall for gravity (the rays absorbed, no content joining) | a measured event of a paid family, `fixed` true, no `lamp`; on a free family `table` `{"m": "measure"}` | its Nodes (a row of measured events, or a `span`); a `phase_window` on its entry for a wall that absorbs one phase range and passes the rest | a click at the Node the row reached, in that interval, the content joining | nothing | its own record as a detector of one Node (`wave` by default): what it absorbed | [`two_slits.json`](../examples/events/README.md), [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) |
| A slit | a wall with one or more Nodes whose entry is `rerelease` on a fan of `directions`; the opening's width the number of such Nodes (A10: 1, 3, 9, 27 Nodes) and, declared as a detector, its set | `table` `{"light": "rerelease"}`, `directions` the fan; `detectors[]` for the opening as a set | its Nodes (the opening's width w); a `phase_window` on its entry | a re-release at each Node of the opening of what that Node took, on the fan, whole units per direction by the age | nothing | the spread behind it at a screen (the `wave` record narrowing with the width, the count never; A10) | [`one_slit.json`](../examples/events/README.md), [`heisenberg/`](../examples/events/heisenberg/README.md), [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) |
| A screen and a detector | `DetectorSet`: `detectors[]` `{"name", "positions", "threshold", "reading"}`, a set of measured events with ONE record (a click says "here, in one of these" and not which; the set's width is the position's uncertainty); a screen resolved in y is one-Node detectors, the pixels; a screen that is one set is one record; an open face is a detector named `face:+x` and the five others; a measured event outside every set is a detector of one Node | `positions`, `threshold`, `reading` `wave` or `beam`; a `phase_window` on the set's entries | `positions` (the set); the `phase_window` on the set's entries and its `phase_width` (a narrower window, since 2026-09-20) | a click at one Node of the set of one row in one interval, with its phase, content and number; the record's sum over the set is the world's | **the `wave` threshold** (step A of issue #359, decided: the threshold under `wave` reading the pointer's square in units of one ray; no memory between intervals, step B refused); nothing to place | the record: under `wave` the square of the coherent pointer and the set's phase (returned to its events after a click); under `beam` the count after the pairing; the clicks with their amount, content, phase and number | [`two_slits.json`](../examples/events/README.md) (pixels), [`catalog/sun_planet.json`](../examples/events/catalog/README.md) (one set), [`detector/`](../examples/events/detector/README.md) (placed from a definitions file) |
| A clock | a measured event whose owed count is read: with `suspension` `[n, d]` it owes `by_clock(age, k x n, d)` intervals after each self-creation, k what its clock counted over every ray of another number at its Nodes (the presence, or the age moment on an entry that reads `age`); its rate `age / (age + waited)` in the record; a moving body's clock ticks in every interval in which it steps (the engine stands, the owner, 2026-09-20) | `suspension`; the entry's `reads` (`scalar`, or `age` for M / r); `span` for a body that averages the fan's grain | `span` (`[3, 3, 3]` in `catalog/clock_near_mass.json`); no window | at every interval a self-creation (its age one more) or a wait (its owed count one less), the count owed off its clock from what it counted over its set | nothing | its `age` and `waited` in `run.json` (the redshift between two clocks: series E; an emitter's clock in the Hubble reading: series G) | [`catalog/clock_near_mass.json`](../examples/events/catalog/README.md), [`redshift/`](../examples/events/redshift/README.md) |
| A probe | a measured event of content 1 with `pass` (no push, no record; the clock counts all the same) or `read` (the push taken and recorded: the `read` lines carry it) | `amount` 1, `fixed` true, `table` `{"m": "pass"}` or the default `read` | `span`; a `phase_window` on its entry | at its Node a `read` (the push) or a `pass` of every arriving row, in the interval it arrived | nothing | its `read` records (the field; series C) or its clock (above) | [`coupling/`](../examples/events/coupling/README.md), [`redshift/`](../examples/events/redshift/README.md), [`catalog/`](../examples/events/catalog/README.md) |
| Dark matter | a free family with no columns but gravity's: `charge` 0, its measured events declaring `pass` for every paid family (transparent to light); placeable today, distinguished from a neutron by its table alone | `quantum` 0, `charge` 0, `table` `{"light": "pass"}` | as the neutron's | as the neutron's | nothing | its gravity by a probe or a clock; no light | none placed (as `catalog/neutron_star.json` with `pass` for a light family) |

## The gap list

Every entity or property the law cannot yet place, with what the law has,
the key it would need and whether it is in design. The law's own
predictions against nature, listed by the physicist on 2026-09-20 (23
entries), are the register's; the ones that name a thing this catalog
cannot place are here.

| Gap | What the law has today | The key it would need | In design? |
| --- | --- | --- | --- |
| Colour and confinement | the columns are rational pairs, so a quark's charge is an ordinary value; a nucleon of three measured events bound by the strong column at adjacent Nodes; confinement a statement of the detector's world (no set at the nucleon's scale resolves one of the three) | the strong column first; a colour column with a neutral sum of three has no form yet | the strong column in implementation; colour recorded as a series after it lands, if the owner wants it |
| The Higgs and mass generation | the content of a measured event is its declared `amount` | a mechanism that gives a content; none named | not in design |
| A black hole | (i) the bound: an `amount` at most 2^62 - 1 and every push M_A x V within it; a body beyond it refuses the run at the first push past the bound (an `OverflowError` naming it), the law's statement that it cannot be placed; (ii) a body whose clock the crowd slows without bound: with `suspension` on, a member of a dense set owes ever more intervals per self-creation, its rate 1 / (1 + k) falling toward zero and never reaching it (no horizon: the law's own prediction (1)), so it releases ever more rarely, and its gravity, which is its releases, thins with its light. The reading a black hole would give under (ii): the clicks of the set's light thin out at every detector, a probe's `read` count falls toward nothing and its clock returns toward its free rate, the opposite of a horizon; under (i) there is no reading, the run is refused | a field that is not paid by the emitter's clock, so that a slowed clock keeps pulling | not in design; the owner's item in the catalog decision |
| Antimatter | the sign of the columns: a positron is a family with `charge` +rho_e, placeable today; the electric push between it and the electron attractive; nothing happens when they meet but the refused step (the contact, when it lands) | **`become`** on the click trigger (the capture form) for annihilation, and at the clock for pair creation: the content moved between the families' lines and light released | the weak design's entry |
| Spin and polarization | the record carries a direction and a phase; nothing on it turns with a hand under the 48 symmetries; a phase window reads the phase, not a polarization | a hand (`hand-v1`); "polarization as worlds and tables" is the owner's open item | admissible, only if wanted |
| Molecules and chemistry | the atom (series H open), helium (the strong column) | a bond: nothing beyond the columns; no key | not in design |
| Dark energy | nothing: the GameBoard's shape is fixed and no term pushes everything apart; series G read the Hubble law from a throw, linear by itself, and the far part falling below the coasting form by the throw's start and the emitters' clocks, nothing accelerating on the GameBoard | none named | not in the law |
| Light bent, slowed or redshifted by a mass in flight | a ray in transit is moved by the flight table and turned by the collision table only, and no rule lets it read the crowd; gravity acts on measured events; a paid ray pushes its reader by its label alone; the law's redshift is the clock's (series E), not the ray's; the law's own prediction (2), a plain disagreement with nature's 1.75 arcseconds and Shapiro's delay | what happens to the ray in flight has no key | not in design; to be run as series K after series I and registered as the limit |
| Decays and lifetimes at rest (the muon, the tau, the neutron) | the clock of a measured event counts; a count of it "will trigger a decay in time" (the owner, 2026-09-20) | **`become`** at the clock (`at`, with the `crowd` gate for the bound neutron) | the weak design, the owner's "go" |
| The W and Z, the gluon | nothing | **`lifetime`**, **the strong column**, **`become`**, **D-1**; **a hand** if wanted | in implementation (the strong force) and in the owner's order (the weak force) |
| Neutrino oscillation | three families; an event in transit changes family by nothing | a change of family in flight | not in design |
| Mass defect, binding energy | absent in the content: a free ray carries no content, so the alpha's content is 2 x 1836 + 2 x 1839 exact; the one reading of a binding energy is the clock's count (the bound clock slower at one Link) | a binding that costs content | not in design |
| The exclusion principle | none: the design finds He-5 and Li-5 bound at L >= 2, a known difference from nature | none named | not in design |
| Tunnelling | absent: the GameBoard is deterministic, a nucleus holds or decays, one interval per world, no spread across the 48 orientations | none | not in the law (the owner's record on alpha; the design's finding) |
| A moving clock's dilation | a body's clock ticks in every interval in which it steps: no slowing against 1 - v at first order, nature's gamma absent (the muon in flight) | none: the owner decided the engine stands and TERMINOLOGY is corrected; a limit of the law, not tuned in | not in design |
| A body that sheds matter (a comet's tail, fission) | a measured event releases rays, never a measured event; `become` releases products as rows | a decay that leaves a body | the owner's open item |
| A star that pulls and shines as one measured event | two measured events at adjacent Nodes (`catalog/sun_planet.json`) | **the held content** with a lamp on the paid part, or the gravity column read off a paid family's rays; the design's to say | the held content in implementation |
| The properties the law's own predictions name as disagreements | a moving body's field pointing to its retarded position (an aberration at order v / c), a bound body's active flux slowed by its count while its inertia is not, no radiation from accelerated charges, bodies that can outrun light, a step survival and a line beta spectrum | none named; each a reading to register, never tuned | the register's (PREDICTIONS.md, 2026-09-20) |

## What could not be placed, and why

The judgements of the architect for the model owner, from the worlds of the
catalog ([their page](../examples/events/catalog/README.md)):

1. **A black hole cannot be placed, and the law's dense body is dark and
   weightless in the limit.** A measured event's field is its releases and
   its releases come at its self-creations, which the crowd's count
   postpones (`suspension`): a body whose clock the crowd slows without
   bound releases ever more rarely, so a detector reads ever less light
   from it and a probe ever less pull; the rate 1 / (1 + k) never reaches
   zero, so there is no horizon (the law's own prediction (1)). The
   neutron star of the catalog shows the beginning of it: the eight
   neutrons count each other's rays and their clocks slow, and with them
   their releases. In nature a black hole keeps its gravity; here a slowed
   clock is a slowed field. The other reading, the integer bound, is a
   refusal and not a thing on the GameBoard.
2. **A star is two measured events.** A measured event has one family; a
   paid family carries no charge and a lamp is of a paid family, so what
   pulls (a free family releasing at the world's rate) and what shines (a
   lamp) are two events at adjacent Nodes, each on a set of three in the
   catalog's world. The held content of several families, decided with
   the strong force, may let one measured event hold both once a lamp can
   release from the paid part; until the design says so, the sun is a
   composite.
3. **Light is pulled by nothing and bent by nothing.** A paid ray pushes
   its reader by its label alone (radiation pressure) and takes no push in
   flight; no rule lets an event in transit read the crowd. The redshift
   the law reads is the clock's, series E; the run that measures the
   disagreement is series K, after series I.
4. **The nucleus, the quarks, the gluon, the W and Z, the decays wait**
   for the strong column, `lifetime`, the held content, the contact,
   `become`, `phase_width` and D-1, all decided or in the owner's order
   (the strong column, `lifetime`, the held content, the contact and
   `phase_width` landed on 2026-09-20); colour has no key and the hand is
   only if wanted.
5. **The contact at one Link is decided and not yet landed.** Two bodies
   held at one Link by the gravity column keep pushing each other; today
   the refused step keeps the momentum, which grows every interval until
   the integer bound refuses the run. The catalog's neutron star is sized
   so that a run of forty intervals stays within the bound (a push of 2^50
   per arriving row); when the contact through the table lands, the
   occupant's `measure` takes the body's axis component and the momenta
   stop growing, and the world reads differently there, its books still
   balanced.
6. **The width of a body is a width of its push.** A body on a set of w
   Nodes reads about w times one Node's flux at the same content (BEAM_LAW
   note 30), so the planet's circular orbit on nine Nodes needs the
   world's `width` of the push large (512) to be slow; the generator
   derives the momentum from the engine's own flight lines and prints it
   as a GameBoard reading of the design. Whether an orbit closes is the
   register's question (series D and H).
7. **An emitter on a set has a width the world cannot see through.** The
   star's mass and lamp are each on a set of three Nodes: every release is
   apportioned whole over the set by the age, so the fan's lines and the
   lamp's beam leave from one of the three Nodes at a time, and a detector
   reading the star reads the set's width as a source's size, as a
   detector's set is a position's uncertainty; which Node released is on
   the GameBoard only.
8. **Dark matter is placeable and dark energy is not.** A free family of
   charge 0 whose measured events pass light is dark matter to every
   detector; nothing in the law pushes everything apart, and series G
   read an accelerating signature without an acceleration.

## The worlds of the catalog

| World | Places | Read by |
| --- | --- | --- |
| [`catalog/sun_planet.json`](../examples/events/catalog/README.md) | the sun (a mass and a lamp, each on a set of three), a planet (a free body on a set of nine, reflecting), a screen (one set) | the screen's `wave` record and its clicks by number; the planet's `read` records |
| [`catalog/neutron_star.json`](../examples/events/catalog/README.md) | a neutron star (eight neutrons bound at one Link), six probes | the probes' clocks: the presence on five, the age moment on one |
| [`catalog/lamp_mirror_screen.json`](../examples/events/catalog/README.md) | a laser, a mirror, a wall with a slit, a screen as pixels | the pixels' `wave` records |
| [`catalog/clock_near_mass.json`](../examples/events/catalog/README.md) | a mass on a fan, two clocks (bodies on sets) at two radii | the clocks' owed counts |

`tests/test_entity_catalog.py` checks that each world is what its page says
(it parses, declares its keys, runs with the books balanced, and its
readings exist) and pins no number
([expectations](TEST_EXPECTATIONS.md#the-entity-catalog)). The register
tests things on them later.
