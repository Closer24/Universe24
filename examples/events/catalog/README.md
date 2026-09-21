# The worlds of the entity catalog

Four small worlds written by `make_worlds.py`, one per external thing the
Beam Law can place on the GameBoard today, for the model owner's
decision of 2026-09-20 ([Highlights 5.4](../../../docs/HIGHLIGHTS.md#54-the-detector),
"DECIDED: the catalog of the entities": "that we can also support external
ones such as the sun, a planet, a neutron star, so that they can be placed
on the GameBoard and things tested"). The catalog they belong to is
[the catalog of the entities](../../../docs/ENTITY_CATALOG.md); the law
whose keys they declare is [the Beam Law](../../../docs/BEAM_LAW.md)
with [the engine's bookkeeping](../../../docs/ENGINE.md).

These are placements, not experiments. Each world parses through the
canonical loader, runs its declared intervals headless with the books
balanced at every interval, and shows what a detector or a clock reads of
the thing placed; the four together run in well under a minute. No number
is registered here and no test pins one (`tests/test_entity_catalog.py`
checks only that each world is what this page says it is, [the
expectations](../../../docs/TEST_EXPECTATIONS.md#the-entity-catalog)); the
[experiments register](../../../docs/EXPERIMENTS.md) tests things on these
placements later, under [the experimenter's rule](../../../skills/experimenter/SKILL.md):
every reading below is a detector reading, the record of a set or of a
measured event in the world; a body's steps and the books are GameBoard
readings, the host's view of the mechanism.

Every family declares its `quantum`, every detector its `reading`, and a
measured event declares only the table entries that differ from the ones
its families' keys give (the world rewrite of 2026-09-20 put the register in
this form; its tool is deleted, in git before e4b649a0). The worlds declare `"law":
"beam"`, the Beam Law (`beam-v1`, the owner's name of 2026-09-20); the
generator and the test read that value from `world.py`, not from a
literal.

## The worlds

| World | What it places | What a detector or a clock reads of it |
| --- | --- | --- |
| `sun_planet.json` | The plane, 41 x 41 x 1 with z periodic, `width` 512, `suspension` 0. **The sun** at the centre is a composite of two measured events at adjacent Nodes, since a measured event has one family, each a body on a set of three Nodes along y (`span` [1, 3, 1]: an emitter on a set, its releases apportioned whole over its Nodes by its age, so which of the three Nodes released is not information the world has): its mass (the free family `mass`, content 2^16, `fixed`, releasing one shell of the 120 primitive in-plane directions with a^2 + b^2 <= 64 every 10 intervals: its gravity) and its lamp (the paid family `light`, content 2^25, `fixed`, a `lamp` of rate 1 per self-creation on a fan of nine directions toward +x: its light, each unit costing and carrying the lamp's turn of 8 content, E = h f). **The planet** is a free body of `mass` of content 2^10 at radius 8 on the +x axis, a body on a set of 3 x 3 Nodes (`span`) so that it reads the fan's grain averaged, with the tangential `momentum` of a circular orbit that the generator derives from the engine's own flight lines (the entries per shell on the body's set, the width of the push and the step rule; printed when the worlds are written, a GameBoard reading of the design), and `rerelease` for `light` on the four in-plane headings: it shines by reflected light. Its content keeps gravity's push, proportional to the reader's content, far above the light's, which is the unit's label alone. **The screen** is one detector set `screen` of 25 Nodes of the paid family `screen` at x = 38, `threshold` 1, `reading` `wave`: one record for the whole set. | The screen's `wave` record accumulates the lamp's light that reaches it directly on the fan's inner directions, and the light the planet reflects toward +x from the planet's rows: a click of the screen names the emitter's `number`, the lamp's or the planet's, so the planet's transit across the screen is read in the clicks. The open faces are detectors too and record the fan's outer directions and the mass's rays. The planet reads the sun's gravity as `read` records (the push taken, one per arriving row) and turns on its arc; whether the orbit closes is the register's question (series D and H), not the catalog's. A body's re-emissions born inside its own set come home and are created again, the law of a body on a set. |
| `neutron_star.json` | An open cube of 25^3. **The neutron star** is a bound set of eight measured events of the free family `neutron` (`charge` 0, no phase circle) at the adjacent Nodes of a 2 x 2 x 2 cube, each of content 2^26 releasing 2^18 units per heading per self-creation on the six headings, free (not `fixed`): each pulls its neighbours by the gravity column alone (the coupling's -1) and a step onto a Node that holds a measured event is refused, so the set holds together at one Link, as a neutron star in nature is bound by gravity. The content is the largest a short run allows: a push is M_A x (the row's amount) x Q per arriving row and every momentum must stay within 2^62 - 1. **Six probes** of the free family `probe`, content 1, `fixed`, `pass` for `neutron` (no push, no record; the clock counts all the same), on the six axes at radius 8 from the star's centre (between Nodes: 8 Links from the cube's corner on a +axis, 7 on a -axis); the -x probe's entry is `{"rule": "pass", "reads": "age"}`, so its clock counts the age moment, sum amount x age, in place of the presence. `suspension` [1, 2^22]. | Each probe's clock: the count it owes off its clock per self-creation (`waited` against `age` in `run.json`), the presence on five probes (M / r^2 in a fan; on the six headings a beam does not spread, series C) and the age moment on the sixth (M / r, the flight time on the record; series E). The star's own clocks count each other's rays and slow, and with them their releases: the crowd slows the splitting, the law's statement of a dense body (the gap list of the catalog on a black hole; the rate never reaches zero, no horizon). The momentum of each neutron grows inward at every refused step, within the bound for these intervals; the contact rule decided on 2026-09-20 (generic through the table: the occupant's entry for the body's family takes the axis component) is in implementation, and when it lands the momenta stop growing and this world reads differently there, its books still balanced. The faces record what leaves. |
| `lamp_mirror_screen.json` | The plane, 21 x 21 x 1 with z periodic, `suspension` 0. An optical bench of the paid families `light` and `apparatus` (content 1, `fixed`). **The laser** at (3, 10) is a lamp of `light` (content 2^25, turn 8) with one direction, +x, and a `phase_window` of 16: it releases 4 units per self-creation only at the self-creations whose clock phase falls in the half circle centred on 16, so it releases in pulses of four intervals out of eight. **The mirror** at (11, 10) is a measured event of `apparatus` with `rerelease` for `light` on the one direction +y: the beam turned by a right angle, the phase and the content kept, the number the mirror's, the age started again. **The wall** is a row of `apparatus` at y = 13 from x = 5 to 17 measuring light (the click, nothing leaves: the rule the keys give a paid family); **the slit** at (11, 13) is the one Node of the wall whose entry is `rerelease` on a fan of the eleven primitive forward directions (a, b, 0) with b >= 1 and abs(a) + b <= 4. **The screen** is a row of `apparatus` at y = 17 from x = 1 to 19 declared as nineteen one-Node detectors `screen_<x>`, the pixels, `reading` `wave`. | The screen's pixels record the light the slit spreads behind the wall: per pixel the square of the coherent pointer of what clicked there and its phase, per interval on the `record` line and cumulatively in the report; the wall and the mirror, outside every declared detector, are detectors of one Node and record what they absorb or return. The faces record the fan's outer directions. A pulse's phases are the laser's clock at the release; a pixel's pointer sums them. |
| `clock_near_mass.json` | An open cube of 21^3, `suspension` [1, 4]. **The mass** at the centre is a measured event of the free family `mass`, content 2^12, `fixed`, releasing one ray per direction per self-creation on the 122 primitive directions with abs(a) + abs(b) + abs(c) <= 4 (the fan of series E's kind, every direction of the lattice within that bound). **Two clocks** are measured events of the free family `probe`, content 1, `fixed`, bodies on sets of 3 x 3 x 3 Nodes (`span`) centred on the +x axis at radius 5 and 9, `pass` for `mass`: a body reads the presence summed over its 27 Nodes, the shell-like mean of the fan's grain at one Node. | Each clock's owed count per self-creation (`waited` against `age`): the count the nearer clock owes is larger than the farther one's, the clock beside a mass; the ratio of the two rates is the redshift between the two heights (series E reads it on whole shells with an expectation written first). The mass owes nothing (nothing of another number reaches it within the run) and the faces record what leaves. |

Write the worlds again (the generator prints the planet's derived orbit):

```bash
python examples/events/catalog/make_worlds.py
```

Run one headless into a new output directory and read its record
(`run.json`: the books per tick, the measured events' states with `age`,
`waited` and `owed`, the detectors with their `record`; `events.jsonl`: the
clicks with their `number`, the `record` lines, the `read` lines with the
push, the `step` lines of the planet):

```bash
python -m event_universe --init examples/events/catalog/sun_planet.json --output artifacts/catalog_sun_planet
```

## What is placed here and what is not

Placed: a star (a mass and a lamp), a planet (a free body with a momentum,
reflecting light), a neutron star (a bound set of neutrons), a lamp, a
laser, a mirror, a wall, a slit, a screen as one set and as pixels, a
clock, a probe. Not placed, with the reason in [the catalog's gap
list](../../../docs/ENTITY_CATALOG.md#the-gap-list): a black hole (the
content bound, or a body whose clock the crowd stops, which then releases
nothing), a star that pulls and shines as one measured event (a paid
family has no charge and a lamp is of a paid family), a nucleus bound by
the strong force (the strong column, the lifetime, the held content and
the contact are in implementation), and everything the weak force does
(the table rule `become`, `phase_width`, in the owner's order). A moon, a
white dwarf, a comet and dark matter are placeable with these worlds' keys
and other numbers, and no world of the catalog places them; a galaxy's
throw is placed by series G (`examples/events/hubble/`).

## Re-read under the Nodes' claims (2026-09-20)

By the model owner's record 155 ("no remainder discarded") a body on a
set of Nodes places every released row over its Nodes by the Nodes'
claims (`place_over_nodes`, the `place` rows of its table of counts;
[BEAM_LAW note 41](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(viii)) in place of the leftover unit to the Node `age mod w`: the sun of
`sun_planet` (two bodies on sets of three Nodes) moves, the planet
standing at (22, 25, 0) after 50 intervals with 11 steps ((23, 25, 0)
with 10), the screen's 152 light clicks (147), the faces' `mass` 19, 19,
7, 7 (19, 19, 0, 21) and `light` 6, 0, 28, 5 (6, 0, 22, 6), the escaped
light 39 units of content 304 (34 of 263), the books balanced at every
tick; `clock_near_mass` is unchanged in its events and books (its bodies
release nothing; the claims 0 in its `state.json`); `lamp_mirror_screen`
and `neutron_star` are identical. The old integers are history
([migration](../../../docs/MIGRATION.md#no-registers-at-nodes-no-tables-on-2026-09-20-the-last-counts-join-the-table-the-flight-as-the-positions-accumulator-no-remainder-discarded)).

## Re-read under the directional drive (2026-09-21)

Under the directional drive ([BEAM_LAW note 49](../../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
the model owner's records 191 and 301) a body walks the line of its
momentum at the pace |p|_1 S_1 Q / (Q S M S_1 Q + |p|_1 T_D), the rows'
pace the cap, and its drive's wall must stay within 2^62 - 1.
`neutron_star` no longer runs its 40 intervals: its eight neutrons of
content 2^26 take the gravity column's push of 3 x 2^50 label units per
interval (the placement's "the largest a short run allows" was set by the
per-axis rule's bound on a component, which the new bound undercuts by
the direction's resolution T_D), so by tick 6 a neutron's |p|_1 is 5 x
2^51 on the direction (3, 2, 5), T_D = 683, and the run is refused at tick
7 with the books balanced through tick 6 (`tests/test_entity_catalog.py`
(b)); its re-placement at a content within the bound is a catalog change
for the physicist, not this rule's. `sun_planet` moves (the planet at
0.1648 Links per interval for the derived 0.1869 at its momentum 7713621;
the branch's VALIDATION table has its digests), `lamp_mirror_screen` and
`clock_near_mass` read the same records (no moving body), their
`state.json` differing by the record's new fields alone.

