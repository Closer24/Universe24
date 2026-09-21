# The worlds of the Beam Law

Four world files of the one engine (`beam-v1`, [the Beam Law](../../docs/BEAM_LAW.md),
[the engine](../../docs/ENGINE.md); [Highlights 5.4](../../docs/HIGHLIGHTS.md#54-the-detector),
"DECIDED: the law of the ray", the model owner, 2026-09-19). Each is a JSON
object with `"law": "beam"`: the GameBoard, K and N (`K` the clock's rate:
an integer K, the content per phase step per self-creation, read as the
pair `[1, K]`, or since 2026-09-20 a pair `[n, d]` of phase steps per unit
of content per self-creation like `release`, the turn `by_clock(age,
content x n, d)`; every world here declares the integer, and the record
carries the key as declared), the release, the
suspension, the declared directions, the families (each by its `quantum`:
0 a free family, 1 or more a paid one; the kind is never declared), the
measured events at the start (their tables generated from the families'
keys, a free family read and a paid one measured; a world declares only
the entries that differ, `tools/migrate_nature_beam_worlds.py` having rewritten
these) and, where wanted, the detectors. The engine recognizes nothing by
physical name; a run is headless and its readings are made from the record
(`run.json`, `events.jsonl`, `state.json`). The GameBoard is open on every face
unless the world declares an axis periodic (`"boundary": {"z": "periodic"}`).
A beam (the record of an event in transit; "ray" is its informal name) flies
at 1 / sqrt 3 on the digital line of its direction (the flight
table: at most one Link per interval); rays of one number and content that
meet at a Node are permuted by the collision table; a release costs the
emitter by its phase rate (E = h f) and a click measures that content.

| World | What it declares | What its record reads |
| --- | --- | --- |
| `one_content.json` | One measured event of the free family `m` (`quantum` 0; `"phase": false`: its rays carry phase 0 and it never turns), content 2^24, held in place at the centre of an open 25^3 GameBoard; K 2^22, N 64, release 1/128 per heading per unit per self-creation on the six headings, `suspension` 1; 200 intervals | The books close at every tick and the content stays constant (what comes home is created again); six ballistic beams of 2^17 per interval, Gauss's flux through every cube equal to the emission once the front has passed; the count on the axes constant with r (a beam does not spread) |
| `two_contents.json` | Two such measured events of `m` 8 Links apart on the x axis of an open 21^3 GameBoard, no suspension; 200 intervals | Equal and opposite pushes along the line, toward each other, each the content times the flow of the other's beam at its Node: the third law read on lone beams (read on 2026-09-19: the books close at every tick, the pushes +/-411217348788224 = 2^24 x 187 x 2^17 along x after 200 intervals; its faces click two beams of 2^17 in one interval and their records pass 2^63, exact, [validation](../../docs/VALIDATION.md)) |
| `two_slits.json` | A lamp of the paid family `light` (`quantum` 1; K 2^30, turn 8, 64 rays per self-creation on five directions toward the wall), a wall at x = 8 of the paid family `wall` measuring light (the rule the keys give; no table declared) with two openings at y = 55 and 65 that declare `rerelease` on a fan of 91 primitive directions, a screen at x = 52 of measured events declared as 121 one-Node detectors `screen_<y>` (the screen's pixels) under the reading `wave` (since 2026-09-19 a detector is a set with one record: one detector of 121 Nodes would read one record with no resolution in y); 60 x 121 x 1 with z periodic, no suspension; 500 intervals | The screen's plain count is additive to the unit (no interference in the count); its squared record fringes at lambda = period / sqrt 3, the interference term correlating with the two-source cosine above 0.85 (`tests/test_nature_beam_worlds.py` (a)) |
| `one_slit.json` | The same with one opening | The control: the record without the two-source term |

The four are written by `make_worlds.py` beside them; since 2026-09-20
they take their families from `entities/families.json` (the world's
`entity_definitions` and `entities` in place of `families`). Since
2026-09-21 (the trimming's part 2: a test holds no literal of a world's
number) `expectations.json` beside them registers what a test reads of a
root world (`two_contents`'s face records at its 20th interval,
`tests/test_nature_beam_worlds.py` (e)), and `gate_set.json` carries each
lamp-free gate world's `digests` at its cap (the sha256 of its state, its
books and its events; `tests/test_amplitude_click.py` (d)).

Run one:

```bash
python -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

## The Bell run

The folder [bell/](bell/README.md) holds the ten worlds of the Bell run A2
under the Beam Law, written by `bell/make_worlds.py`: one bar of
21 x 1 x 1, a lamp of `light` at the centre releasing one ray per
self-creation on +X and on -X, and four counters with phase windows, Alice's
pair at x = 2 and 1 and Bob's at x = 18 and 19, the settings the only
difference between the files. `tools/bell_chsh.py` reads their records and
prints the counts, E, S and every criterion; the register entry is
[A2, under the Beam Law (2026-09-19)](../../docs/EXPERIMENTS.md#a2-under-the-beam-law-2026-09-19):
S = 2 exactly, the model's limit, unchanged from the law of events.

The same folder holds the seven worlds of the run with the choosers on the
GameBoard (issue #363), written by `bell/make_chooser_worlds.py`: the same
bar and pair lamp, and four counters whose windows are not written in the
file but read from the phase of a stream arriving from a third lamp
(`sa`, at x = 0, Alice's) and a fourth (`sb`, at x = 20, Bob's), the key
`phase_window` `{"reads": "<family>", "offset": s}`; the streams have odd
periods (5 and 3) coprime to each other and to the circle, so every
combination of settings meets every phase of the pair; `read.json` is the
run, `written_a<a>_b<b>.json`, `fixed.json` and `one_clock.json` its
three controls. `tools/bell_choosers.py` bins the clicks by the window
they carry and prints every E, S on the quadruple, the largest S over
every quadruple that occurred and the marginals; the register entry is
[A2 with the choosers on the GameBoard (2026-09-20)](../../docs/EXPERIMENTS.md#a2-with-the-choosers-on-the-gameboard-2026-09-20):
S = 2 exactly with every E on the triangle, the law found not to
correlate what never met.

## The coupling series

The folder [coupling/](coupling/README.md) holds the twenty-one worlds of
the coupling series C under the Beam Law, written by
`coupling/make_worlds.py` from one base: a GameBoard of 121 x 121 x 1 with the z
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
[BEAM_LAW section 8](../../docs/BEAM_LAW.md#8-independent-expectations-for-the-re-registered-readings);
the register entry is
[C, the couplings under the Beam Law, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#c-the-couplings-under-the-beam-law-on-the-plane-2026-09-19).

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
under the step drive (2026-09-20) the reference orbit closes four times
and stays on the GameBoard for the run, the coherence at the closing
radius outside (C(4) = 1.01 against 2.0, the phase's turn per orbit 0.75
to 0.83 against 0): the orbit closes and Bohr's condition is not met,
registered as the finding and not tuned.

## The nucleus series

The folder [nucleus/](nucleus/README.md) holds the eight worlds of series
I, written by `nucleus/make_worlds.py`: an open 21^3 cube, three free
families without a phase circle (`p` with `charge` 4, `n`, and `nuclear`
with the column `strong` of value 10000 and sign minus and the `lifetime`
3), nucleons that are free bodies of 1836 or 1839 units holding one unit
of `nuclear` (`held`) and releasing one row per direction of the 290
primitive directions with |a| + |b| + |c| <= 6 per interval, `width` 2^28:
the deuteron at one and at three Links (kicked), two protons at one Link
(G = 10000 and 7000) and at three, the square p n / n p and the line p n
n p. `tools/nucleus_readings.py` reads the bodies' own `read` and
`contact` records and the border's clicks (DETECTOR) and their steps and
separations (GAMEBOARD), every line labelled by its kind; the register
entry is
[I, the nucleus (2026-09-20)](../../docs/EXPERIMENTS.md#i-the-nucleus-2026-09-20):
the deuteron bound at one Link and free at three, two protons bound or
repelled by the sign of Q^2 - G^2 - M^2, the square sheared apart and the
line held, 29 readings inside and 1 outside, registered and not tuned.

## The binding series

The folder [binding/](binding/README.md) holds the three worlds of series
N, the binding that costs content (`binding-v1`,
[BEAM_LAW note 40](../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
written by `binding/make_worlds.py` on series I's base: the nucleons carry
the paid family `bond` (quantum 1, lifetime 3) held 2 each with their free
totals kept (1837, 1840), and give it at their first contact under
`measure` to the flight away from the occupant, the border `lifetime`
clicking it two Links away: the deuteron with the bond (B1, the defect 4
as two border clicks, the mass read 3673 of 3677), one proton alone beside
the I7 lamp (B2, the control: no give, the lamp blind to the held content)
and the square p n / n p with the bond (B3, 8 units, the ratio 2.0 to the
deuteron against nature's 12.7, the law's failure stated before the run).
The pins were written before the run and the readings beside them; the
register entry is
[N, the binding that costs content (2026-09-20)](../../docs/EXPERIMENTS.md#n-the-binding-that-costs-content-2026-09-20).

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
[D, the orbit under the Beam Law, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19):
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
[A10, the width of an opening and the spread behind it](../../docs/EXPERIMENTS.md#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-beam-law-2026-09-20):
the `wave` record narrows with w and the count does not; the product
w x FWHM reaches 0.886 lambda within 22 % at w = 27 and is not read at
the smaller widths on the sparse fan.

## The A10 low-rate run

The folder [buildup/](buildup/README.md) holds the three worlds of A10 at
a low rate, written by `buildup/make_worlds.py` from the A10 generator:
the registered `w27_wave` world with the lamps' `rate` 47, 8 and 1 units
per interval (about 6, 1 and 0.14 rays per pixel per interval at the
screen) and the runs lengthened so that the late window holds the same
172 000 clicks. `tools/buildup_readings.py` reads, per pixel over the
window, the plain count, the coherent record and the incoherent sum of
every unit's own square (the cross term between them), the narrowing of
the record's spread against the count's, and the (pixel, interval) cells
that held two or more rays; the register entry is
[A10 at a low rate, the single-click build-up (2026-09-20)](../../docs/EXPERIMENTS.md#a10-at-a-low-rate-the-single-click-build-up-2026-09-20):
the lobe of the coherent record (the narrowing 0.31 at six rays per
pixel per interval) is a sixth of itself at about one ray and gone at
0.14, where nature builds the same fringes one click at a time; the
law's limit, registered and not tuned.

## The light-beside-a-mass series

The folder [lensing/](lensing/README.md) holds the four worlds of series
K, written by `lensing/make_worlds.py`: an open 57 x 41 x 41 box, a lamp
of the paid family `light` sending a narrow beam (five directions within
5 degrees of the heading) past a fixed mass of the free phase-less
family `m` at the centre (series E's fan of 290 directions, one or two
rays per direction per interval) at the impact distance b = 6 or 3,
toward a screen of 1681 one-Node `wave` pixels with the age moment on the
click record, and a control without the mass. `tools/lensing_readings.py`
reads the deflection of the arrival's centroid, its width, the mean age
of the arrivals (the delay), the count and the phase rate against the
control (DETECTOR) and replays the world for the beam's rows, the rays a
collision would have turned and the Nodes shared with the crowd
(GAMEBOARD); the register entry is
[K, light beside a mass (2026-09-20)](../../docs/EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20):
the deflection 0.000 pixel and the delay 0.00 interval at a crowd where
nature would capture the beam, the derivation of the physicist's entry 2
held: light is neither bent nor delayed in this law, a plain
disagreement with nature, registered and not tuned. Since the meeting
(2026-09-20, the world key `meeting`, [BEAM_LAW note 35](../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
the folder also holds the four worlds under the key
(`<name>_meeting.json`) and `lens_meeting.json`, two beams at +-b on a
longer box; the register entry
[K under the meeting (2026-09-20)](../../docs/EXPERIMENTS.md#k-under-the-meeting-2026-09-20):
light bent toward the mass with the sign of gravity, the M / b form and
the grain of the fan (-1.8 to -4.4 pixels; the lens crossing 71 Links
past the mass), not delayed in time, the mass measuring the light turned
into it; registered, 14 readings inside and 9 outside, not tuned.
## The Hubble series with stars

The folder [hubble_stars/](hubble_stars/README.md) holds the nine worlds of
series G2, the Hubble diagram with stars behind the detector, written by
`hubble_stars/make_worlds.py` with their expectations
(`hubble_stars/expectations.json`, written before the runs) for the model
owner's question of 2026-09-20, whether dark energy is needed: twenty-four
stars of the catalog's kind, each ONE measured event that holds a mass
(`held`, the universal gravity column) and is a lamp (its light released on
its clock at the cost E = h f), thrown from the centre of an open 301^3
cube along the six axes with a Hubble-flow initial condition (the speed
proportional to the distance, as if from one point 90 intervals before the
run), the model's own gravity between them (the mass rows on the axes, the
push through the detector to the opposite chain), a detector of one Node at
the centre reading `wave` with `reads: "age"`; three crowds (the coupling
off, on, doubled) and three clocks (none, the presence, the age moment).
`tools/hubble_stars_readings.py` reads, per star, the redshift from the
pointer's turn, the distance from the arrivals' ages and the luminosity from
the click rate, fits the deceleration q with H free (the power-law family
and the three exact forms), validates the criterion on the exact coasting
form first, and labels every line a detector or a GameBoard reading; the
register entry is drafted in the folder's README and not registered until
the model owner says so: the clock-free coasting control reads the Milne
form to the grain (q = -0.11, H (t_0 + T_0) = 1.03), every star's momentum
decelerates under the law's gravity and none accelerates, and the detector
cannot read that deceleration as a q because the step rule stalls and
bursts under a changing momentum (the README's findings for the law, among
them that a body's own motion does not Doppler what it reads). The
physicist's design is `docs/designs/hubble_stars/DESIGN.md`; the same
worlds under the record click (`make_worlds.py --record`, the key
`amplitude`, the branch `claude/amplitude-impl`) read the same list of
clicks and the same numbers to the last digit.

## The weak-force series

The folder [weak/](weak/README.md) holds the worlds of series J, the weak
force, written by `weak/make_worlds.py`: J2, the neutrino's passage through
a filled bar (the neutrino first, no change of law: a bar of 200 x 1 x 1, a
fixed source of the free family `nu` releasing one ray per self-creation
with the stride 1 or 2 over the circle, 128 fixed readers of a paid family
measuring `nu` under a window of `phase_width` 1 or the default half
circle, their centres all 0, all 1 or a ladder x mod 64, and a far
detector counting every ray that reaches it). `tools/weak_readings.py`
reads the readers' clicks and passes and the far detector's clicks
(DETECTOR) against the counts computed before the run from the engine's
flight table (GAMEBOARD), every line labelled by its kind; the register
entry is
[J, the weak force (2026-09-20)](../../docs/EXPERIMENTS.md#j-the-weak-force-2026-09-20):
the first reader takes exactly 1 / 64 of a stride-1 source's arrivals and
the 127 behind it nothing (a filter, not an attenuation), the ladder
exhausts the beam after 64 readers, the stride 2 gives 1 / 32 at the centre
0 and nothing at the centre 1; 13 readings inside, 0 outside, registered
and not tuned. J1, the free neutron's decay count against its clock (the
transformation `become`, `weak-v1`, [BEAM_LAW note 36](../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
(iii)): 64 neutrons of the register's `n` on a lattice of pitch 4 in an
open 41^3 GameBoard, each with `become` at 512 into `p` with the products
`beta` and `nu`, a shell of readers at r = 18 declared as one `beam`
detector measuring `beta` with `reads` `age`; alone (`j1_lattice`) and
with a fixed source at the centre (`j1_source`). J3, the bound neutron:
the deuteron of series I with `become` at 512 on the neutron
(`j3_deuteron`), the same with the gate `crowd` 65536
(`j3_deuteron_crowd`) and the neutron alone (`j3_neutron_free`). The tool
reads each neutron's `become` line (its tick and the count its clock read,
GAMEBOARD) and the shell's clicks per interval with their contents and
ages (DETECTOR) against the ticks computed before the runs from the
clock's rule and the counts a warm run read (`expectations.json`). The W
world (`w_exchange`, no key added): the W a paid family with a whole
charge per unit of amount and `lifetime` 1, thrown by a neutron's
`become` and measured by the proton one Link away one interval later,
which then has a neutron's charge and content.

## The hand series

The folder [hand/](hand/README.md) holds the worlds of series P, the hand
(`hand-v1`, the model owner's decision of 2026-09-20, record 128 of the
log; [BEAM_LAW note 39](../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
written by `hand/make_worlds.py`: `w_hand`, the W world with a second
proton, the W family left-handed and the neutron given an axis (the W
leaves against the axis to the proton on one side; the mirror image of the
world sends it to the other: the parity test); `w_two_sides`, the control
without a hand or an axis (mirror-equal); `wu`, Wu's experiment on a bar of
17 (the left-handed beta against the nuclear axis to the reader at x = 0,
the right-handed antineutrino along it out of the face); and `nu_hand`,
J2's bar with the neutrino left-handed and two readers admitting one hand
each (0 and 1022 clicks; mirror-equal, a hand without an axis being a
datum a mirror cannot see). The register entry is
[P, the hand (2026-09-20)](../../docs/EXPERIMENTS.md#p-the-hand-2026-09-20);
the parity test itself is `tests/test_hand.py` (d).

## The amplitude series

The folder [amplitude/](amplitude/README.md) holds the worlds of series L,
the amplitude law (`amplitude-v1`, the record form of every lamp since
stage (vii) step 4, the world key `amplitude` deleted,
[BEAM_LAW note 37](../../docs/BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
written by `amplitude/make_worlds.py` with `expectations.json` pinned
before the runs: L1, the Mach-Zehnder interferometer of the design's
section 3.4 (a 5 x 5 plane, a source releasing one record per
self-creation on two arms, two mirrors, a splitter whose split table is
selected by the arrival, the ports D1 and D2 reading `sum`) with equal
arms, a half and a quarter turn on one arm, the balanced (1, 1) split, the
(3, 4) split, arms unequal by two intervals at three phases per interval,
and Elitzur-Vaidman's absorber on one arm; L2, the two slits at a low
rate (the shipped two-slit world under the key with the wall freed beside
the openings, and its one-birth reference; L2b, the two slits with the
fan by angle, the Huygens fan of width 48 with the angle weights, whose
weights carry Young's fringes); L3, the pair on the A2 world
with the choosers, at the CHSH labels, with a which-path read and with
Bob's counters far; L4, GHZ; L5, the gate between records (the CNOT
pair, CNOT twice, GHZ by one gate, the register's ceiling); L6, the pair
at N = 1024 and 4096. The register entry is
[L, the amplitude law (2026-09-20)](../../docs/EXPERIMENTS.md#l-the-amplitude-law-2026-09-20).

## The entity catalog

The folder [catalog/](catalog/README.md) holds the four worlds of
[the catalog of the entities](../../docs/ENTITY_CATALOG.md) (the model
owner, 2026-09-20: "that we can also support external ones such as the
sun, a planet, a neutron star, so that they can be placed on the GameBoard
and things tested"), written by `catalog/make_worlds.py`: `sun_planet.json`
(a star as a mass and a lamp at adjacent Nodes, each on a set of three
Nodes, a planet as a free body on a set of nine Nodes with the tangential
momentum of a circular orbit that reflects the star's light, and a screen
that is one `wave` detector set),
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

The isolated tests of the engine are the ten `tests/test_nature_beam_*.py` modules
([expectations](../../docs/TEST_EXPECTATIONS.md)); `tests/test_nature_beam_worlds.py`
runs these worlds' designs on smaller GameBoards and pins their readings as a
check that the engine does what the law says, not as a result.
