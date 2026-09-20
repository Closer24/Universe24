# The worlds of the law of the ray

Four world files of the one engine (`rays-v1`, [the law of the ray](../../docs/RAY_LAW.md),
[the engine](../../docs/ENGINE.md); [Highlights 5.4](../../docs/HIGHLIGHTS.md#54-the-detector),
"DECIDED: the law of the ray", the model owner, 2026-09-19). Each is a JSON
object with `"law": "rays"`: the board, K and N, the release, the
suspension, the declared directions, the families (each by its `quantum`:
0 a free family, 1 or more a paid one; the kind is never declared), the
measured events at the start (their tables generated from the families'
keys, a free family read and a paid one measured; a world declares only
the entries that differ, `tools/migrate_ray_worlds.py` having rewritten
these) and, where wanted, the detectors. The engine recognizes nothing by
physical name; a run is headless and its readings are made from the record
(`run.json`, `events.jsonl`, `state.json`). The board is open on every face
unless the world declares an axis periodic (`"boundary": {"z": "periodic"}`).
A ray flies at 1 / sqrt 3 on the digital line of its direction (the flight
table: at most one Link per interval); rays of one number and content that
meet at a Node are permuted by the collision table; a release costs the
emitter by its phase rate (E = h f) and a click measures that content.

| World | What it declares | What its record reads |
| --- | --- | --- |
| `one_content.json` | One measured event of the free family `m` (`quantum` 0; `"phase": false`: its rays carry phase 0 and it never turns), content 2^24, held in place at the centre of an open 25^3 board; K 2^22, N 64, release 1/128 per heading per unit per self-creation on the six headings, `suspension` 1; 200 intervals | The books close at every tick and the content stays constant (what comes home is created again); six ballistic beams of 2^17 per interval, Gauss's flux through every cube equal to the emission once the front has passed; the count on the axes constant with r (a beam does not spread) |
| `two_contents.json` | Two such measured events of `m` 8 Links apart on the x axis of an open 21^3 board, no suspension; 200 intervals | Equal and opposite pushes along the line, toward each other, each the content times the flow of the other's beam at its Node: the third law read on lone beams (read on 2026-09-19: the books close at every tick, the pushes +/-411217348788224 = 2^24 x 187 x 2^17 along x after 200 intervals; its faces click two beams of 2^17 in one interval and their records pass 2^63, exact, [validation](../../docs/VALIDATION.md)) |
| `two_slits.json` | A lamp of the paid family `light` (`quantum` 1; K 2^30, turn 8, 64 rays per self-creation on five directions toward the wall), a wall at x = 8 of the paid family `wall` measuring light (the rule the keys give; no table declared) with two openings at y = 55 and 65 that declare `rerelease` on a fan of 91 primitive directions, a screen at x = 52 of measured events declared as 121 one-Node detectors `screen_<y>` (the screen's pixels) under the reading `wave` (since 2026-09-19 a detector is a set with one record: one detector of 121 Nodes would read one record with no resolution in y); 60 x 121 x 1 with z periodic, no suspension; 500 intervals | The screen's plain count is additive to the unit (no interference in the count); its squared record fringes at lambda = period / sqrt 3, the interference term correlating with the two-source cosine above 0.85 (`tests/test_ray_worlds.py` (a)) |
| `one_slit.json` | The same with one opening | The control: the record without the two-source term |

Run one:

```bash
python -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

## The Bell run

The folder [bell/](bell/README.md) holds the ten worlds of the Bell run A2
under the law of the ray, written by `bell/make_worlds.py`: one bar of
21 x 1 x 1, a lamp of `light` at the centre releasing one ray per
self-creation on +X and on -X, and four counters with phase windows, Alice's
pair at x = 2 and 1 and Bob's at x = 18 and 19, the settings the only
difference between the files. `tools/bell_chsh.py` reads their records and
prints the counts, E, S and every criterion; the register entry is
[A2, under the law of the ray (2026-09-19)](../../docs/EXPERIMENTS.md#a2-under-the-law-of-the-ray-2026-09-19):
S = 2 exactly, the model's limit, unchanged from the law of events.

## The coupling series

The folder [coupling/](coupling/README.md) holds the twenty-one worlds of
the coupling series C under the law of the ray, written by
`coupling/make_worlds.py` from one base: a board of 121 x 121 x 1 with the z
axis periodic, a source of content 2^24 at the centre releasing six beams on
the six headings, and probes of content 1 that read (the push taken, the
rays go on). The items: the equivalence, the third law with unequal contents
(to the grain of the whole apportioning), superposition, retardation (the
front from the flight table), the far field (the ring means of the count,
the presence and the flow, the flux through the square, the escape; the
axis pattern at the probes), the clock (`suspension` 1: the ages replayed
from the presence read) and the electric reading. `tools/coupling_readings.py`
reads their records, replays the source-alone worlds through the API and
prints every criterion and every reading against the expectations of
[RAY_LAW section 8](../../docs/RAY_LAW.md#8-independent-expectations-for-the-re-registered-readings);
the register entry is
[C, the couplings under the law of the ray, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#c-the-couplings-under-the-law-of-the-ray-on-the-plane-2026-09-19).

## The redshift series

The folder [redshift/](redshift/README.md) holds the two worlds of the
redshift series E, written by `redshift/make_worlds.py`: an open 31^3 cube,
a fixed source of content 2^12 at the centre releasing one ray per
self-creation on the 290 primitive directions with |a| + |b| + |c| <= 6,
and probes of content 1 at every Node of the shells r = 4 to 14 that
`pass` the rays and count, in the `scalar` world the presence and in the
`age` world the age moment (`reads: "age"`, the ray's age kept whole on
the record since 2026-09-20). `tools/redshift_readings.py` reads the shell
means of the owed count per self-creation, k x r^2 and k x r, the single
probes on the axis and the diagonals and the redshift ratios of the age
clocks; the register entry is
[E, the clock's redshift in space under the age reading (2026-09-20)](../../docs/EXPERIMENTS.md#e-the-clocks-redshift-in-space-under-the-age-reading-2026-09-20):
the presence falls as M / r^2 and the age moment as M / r from the same
rays, their ratio the flight's sqrt 3 / 2.

## The Hubble series

The folder [hubble/](hubble/README.md) holds the four worlds of series G,
the Hubble diagram behind the detector, written by `hubble/make_worlds.py`:
an open 301^3 cube, twenty-four free sources (a family each) thrown from
the centre along the six axes at 0.05 c to 0.6 c (c = 32 / 55 Links per
interval read off the flight table), each releasing one row per
self-creation toward the centre with its clock's phase, a detector of one
Node at the centre reading `wave` with `reads: "age"` (the arrival's age
on the click record) and six masses inside at one Link (the crowd's mass
inside every source), in a coasting crowd (rows of one ray, the masses of
content 1) and a pushing crowd (rows of sixteen, the masses releasing 64
per self-creation), each with the emitters' clocks counting the presence
(`scalar`) or the age moment (`age`). `tools/hubble_readings.py` reads,
per source, the redshift from the rate at which the pointer of the
detector's record turns against the emitter's declared turn and the
distance from the ages of the arriving rays, fits the linear law on the
near part and compares the far part with the coasting (q = 0),
decelerating (q = +0.5) and accelerating (q = -0.55, what is observed
today) forms, every line labelled a detector or a GameBoard reading; the
register entry is
[G, the Hubble diagram behind the detector (2026-09-20)](../../docs/EXPERIMENTS.md#g-the-hubble-diagram-behind-the-detector-2026-09-20):
the linear law comes out by itself (z = v / c to 0.003, H t_0 = 1.03 at
t_0 = 350) and the far part falls below the coasting form of the near fit
in every run, the signature of the accelerating form, by the throw's
initial distances and the emitters' clocks and not by an acceleration
(on the GameBoard the pushing sources lose 4 to 32 % of their momentum).

## The Bohr series

The folder [bohr/](bohr/README.md) holds the seven worlds of series H,
written by `bohr/make_worlds.py`: an open cube sized to the orbit, a fixed
proton (`p`, content 1836, `charge` [1, 1]) at the centre releasing one
ray per direction of a shell of 2616 primitive directions every 10
intervals, and an electron (`e`, content 1836, `charge` -15) that is a
body on a set of three Nodes (`span` [1, 1, 3]) at r = 2, 4, 6, 8, 12, 15
or 16 with the tangential momentum the README derives from the engine's
own flight lines, turning its phase by its momentum at every Link it steps
(`phase_by_momentum` under the world's `action`, h = 16 p(8) so that
4 p r = 2 h at r = 8) and releasing rays that carry that phase to the
open faces, the `wave` detectors of what comes out of the atom.
`tools/bohr_readings.py` reads the orbit (GAMEBOARD) and the faces'
coherent record per turn and cumulatively (DETECTOR), every line
labelled by its kind; the register entry is
[H, Bohr's lines behind the detector (2026-09-20)](../../docs/EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20):
no orbit closed well enough for the coherence reading (the reference
orbit held its mean radius for two eccentric turns and was thrown out at
a close pass), registered as the finding and not tuned.

## The orbit series

The folder [orbit/](orbit/README.md) holds the six worlds of the orbit
series D, written by `orbit/make_worlds.py`: the same plane, a fixed source
of content 2^10 releasing one shell every 10 intervals on a fan of 120
primitive in-plane directions (q = 12 units per interval), and a free probe
of content 1 at r = 12 or 24 with the tangential momentum the README derives
for a circular orbit under the measured push law, at the widths of the push
`width` 1, 8 and 32. `tools/orbit_readings.py` reads the probe's steps and
pushes and prints whether the orbit closed, its period, its mean radius,
its drift and the period ratio against the plane's k = 2; the register
entry is
[D, the orbit under the law of the ray, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#d-the-orbit-under-the-law-of-the-ray-on-the-plane-2026-09-19):
one orbit closes by the criterion (S = 32, r = 12, an eccentric loop), the
mean push reads as derived, the grain of the push breaks the rest.

## The Heisenberg run

The folder [heisenberg/](heisenberg/README.md) holds the eight worlds of
the run A10, written by `heisenberg/make_worlds.py`: the plane stretched
to 120 x 161, a plane wave from a row of lamps on one heading, a wall
with ONE opening of width w (1, 3, 9, 27 Nodes) declared as one detector
that re-emits on a forward fan of 47 directions, and a screen 108 Links
behind it read as 161 one-Node detectors, every detector under the
world's `reading` (`wave` or `beam`). `tools/heisenberg_readings.py` reads
the spread of the screen's record and of its count against the
wavelength lambda = 8 / sqrt 3; the register entry is
[A10, the width of an opening and the spread behind it](../../docs/EXPERIMENTS.md#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-law-of-the-ray-2026-09-20):
the `wave` record narrows with w and the count does not; the product
w x FWHM reaches 0.886 lambda within 22 % at w = 27 and is not read at
the smaller widths on the sparse fan.

## The entity catalog

The folder [catalog/](catalog/README.md) holds the four worlds of
[the catalog of the entities](../../docs/ENTITY_CATALOG.md) (the model
owner, 2026-09-20: "that we can also support external ones such as the
sun, a planet, a neutron star, so that they can be placed on the GameBoard
and things tested"), written by `catalog/make_worlds.py`: `sun_planet.json`
(a star as a mass and a lamp at adjacent Nodes, a planet as a free body on
a set of nine Nodes with the tangential momentum of a circular orbit that
reflects the star's light, and a screen that is one `wave` detector set),
`neutron_star.json` (eight neutrons of content 2^26 bound at one Link by
the gravity column alone, six probes on the axes counting the presence and
one the age moment), `lamp_mirror_screen.json` (a laser with a phase
window, a mirror that re-releases on one direction, a wall with a slit and
a screen read as pixels) and `clock_near_mass.json` (a mass on a fan of
122 directions and two clocks, bodies on sets, at two radii). Placements,
not experiments: each parses and runs its intervals with the books
balanced, `tests/test_entity_catalog.py` pins no number, and the register
tests things on them later.

## The detector definitions

The folder [detector/](detector/README.md) holds four worlds that place
reusable apparatus from `detector/entities/detectors.json` through the
[entity definitions loader](../../docs/ENTITY_DEFINITIONS.md): chains of
measured events measuring a carrier, declared as detectors with thresholds,
one of them reading the tensor component of the one reading.

The isolated tests of the engine are the ten `tests/test_ray_*.py` modules
([expectations](../../docs/TEST_EXPECTATIONS.md)); `tests/test_ray_worlds.py`
runs these worlds' designs on smaller boards and pins their readings as a
check that the engine does what the law says, not as a result.
