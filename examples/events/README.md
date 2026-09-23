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
(`run.json`, `events.jsonl`, `state.json`). A pin of the register is a
detector reading (a click, a record line); a reading of the GameBoard
itself (`shell_readings`, the cube flux, the probes' counts, a replay) is a
host reading, labelled GAMEBOARD by every tool that prints one (the model
owner's record 163 of 2026-09-20). The GameBoard is open on every face
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
books and its events; `tests/test_amplitude_click.py` (d)). Every
`expectations.json` names each entry's source in its `derivations` map
and, since 2026-09-21 (the owner's rule, record 353), its second runner's
check in its `replicated` map, one entry per run block pointing at the
run's line in `docs/REPLICATIONS.md`; an entry absent there is a run
measured once, awaiting replication
([TEST_EXPECTATIONS](../../docs/TEST_EXPECTATIONS.md)).

Run one:

```bash
python -m event_universe --init examples/events/one_content.json --output artifacts/one_content
```

## Writing and running a new series: what the experimenter of 2026-09-21 had to find out by refusals

The rules below are the engine's (docs/ENGINE.md and the refusals of
`events/world.py`); they are gathered here because each cost a run or a
refusal to learn while series O and P were built.

1. **A body's oblique directions are the world's table.** A body's
   `directions` (its releases and re-emissions) and a lamp's `directions`
   name vectors; a vector beyond the six headings must be declared once in
   the world's `directions` table, in primitive form (components coprime:
   `(3, -3, 0)` is refused, write `(1, -1, 0)`), and the table must not
   repeat a heading (`(0, -1, 0)` is refused there; a body still names it).
   A row flies on the digital line of its vector (`nature_beam._bresenham`:
   at each Link the axis furthest behind, the lowest axis first), so which
   Nodes a fan visits is that line's: `(-4, -3, 0)` from `(x, y + 3)` visits
   `x - 3`, `x - 4` and `x - 5` on the plane `y`, not `x - 4` alone. Print
   the store's rows for a few intervals before pinning a geometry.
2. **A free family's release goes whole on every direction.** A `mass`
   body of `amount` A releases `release x A` units per self-creation on
   each of its directions (nine directions, nine rows of the whole
   release; the release costs a free family nothing); the presence a
   neighbour counts is per row at its Node, "outside and here", about two
   per unit of a heading row's flux at c = 0.58 Links per interval. A paid
   family's release is apportioned whole over the directions.
3. **A lamp spends.** Its wheel turns by its content over K, and its
   content falls by one unit per birth: a lamp of 8192 units is 6 % slow
   after 500 births, which a clock experiment reads as a false k. Give a
   clock experiment's lamp a reservoir far beyond the run's births
   (2^20 units for 500 births: 0.05 %).
4. **Load a world as the tests do.** `load_world(path.read_bytes(),
   base_dir=path.parent, root=<the examples/events folder>)` returns a
   `LoadedWorld`; its `.world` is what `NatureBeamSimulation` takes. A
   world's `..` references climb one level only.
5. **Run a series headless and read the record.**
   `PYTHONPATH=src python tools/run_series.py --jobs 3 --out <dir> <worlds...>`
   writes `<dir>/<world>/run/{run.json, initialization.json, events.jsonl,
   state.json}` and a `summary.md`. The lines to read: `birth` (a lamp's
   self-creation, `measured` the lamp's number, `record` its record), `click`
   (`measured` the reader, `record & 0xFFFFFFFF` the birth ordinal, so the
   slope of ordinal against tick is 1 / (1 + z); `age` the flight when the
   reader's entry `reads: "age"`), `step` (`number`, `node`, `to`), `contact`
   (`number`, `occupant`, `given`), `home`. `state.json` carries per measured
   event `waited`, `owed`, `presence`, `age`, `content`, `position`. Write
   the reading script before the run and keep it beside the design.
6. **Before `python tools/check.py`**, format and lint the changed Python
   files: `python -m ruff format <files>` and `python -m ruff check <files>`;
   the gate fails on an unformatted file before it runs a test. Regenerate
   the worlds after formatting the generator and confirm the shipped JSON
   is unchanged (the tests compare document for document).

## The Bell run

The folder [bell/](bell/README.md) holds the ten worlds of the Bell run A2
under the Beam Law, written by `bell/make_worlds.py`: one bar of
21 x 1 x 1, a lamp of `light` at the centre releasing one ray per
self-creation on +X and on -X, and four counters with phase windows, Alice's
pair at x = 2 and 1 and Bob's at x = 18 and 19, the settings the only
difference between the files. `tools/click_readings/bell.py` reads their records and
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
three controls. `tools/click_readings/bell_choosers.py` bins the clicks by the window
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
from the presence read) and the electric reading. `tools/click_readings/coupling.py`
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
the record since 2026-09-20). `tools/click_readings/redshift.py` reads the shell
means of the owed count per self-creation, k x r^2 and k x r, the single
probes on the axis and the diagonals and the redshift ratios of the age
clocks; the register entry is
[E, the clock's redshift in space under the age reading (2026-09-20)](../../docs/EXPERIMENTS.md#e-the-clocks-redshift-in-space-under-the-age-reading-2026-09-20):
the presence falls as M / r^2 and the age moment as M / r from the same
rays, their ratio the flight's sqrt 3 / 2. Those are GameBoard readings of
probes in a world with no detector; the detector reading of the same field
is series T (outside a source) and series X below (its source term).

## The shell series: Poisson after a detector

The folder [shell_clock/](shell_clock/README.md) holds the nine worlds of
series X, written by `shell_clock/make_worlds.py` (series T's generator
imported for the speeds, series E's for the one copy of the fan of 290):
series T's lamp and detector 100 Links apart, and a shell of 450 fixed
`mass` sources of radius 6 (the Nodes at |distance - R| < 1/2, series E's
selection) centred 2, 4 or 12 Links from the lamp, each source releasing
21.8444 units per direction per interval on the full fan (series T's crowd's
total release pair spread over the shell's Nodes). The lamp's entry for the
crowd declares the age word or the presence word, and each world has its
control, the lamp alone on the same GameBoard. `tools/click_readings/shell_clock.py`
reads the detector's click lines and nothing else: 1 + z per window, the
count k = 1 + z - 1 and the three ratios the map pinned before the run. The
register entry is
[X, Poisson after a detector (2026-09-22)](../../docs/EXPERIMENTS.md#x-poisson-after-a-detector-2026-09-22):
inside a shell the potential is flat and the flux is not, so the interior
tells the clock's two words apart at a source term.

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
(`scalar`) or the age moment (`age`). `tools/click_readings/hubble.py` reads,
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
`tools/click_readings/bohr.py` reads the orbit (GAMEBOARD) and the faces'
coherent record per turn and cumulatively (DETECTOR), every line
labelled by its kind; the register entry is
[H, Bohr's lines behind the detector (2026-09-20)](../../docs/EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20):
under the step drive (2026-09-20) the reference orbit closes four times
and stays on the GameBoard for the run, the coherence at the closing
radius outside (C(4) = 1.01 against 2.0, the phase's turn per orbit 0.75
to 0.83 against 0): the orbit closes and Bohr's condition is not met,
registered as the finding and not tuned.

## The atoms series

The folder [atoms/](atoms/README.md) holds the two worlds of the atoms
series under form B, written by `atoms/make_worlds.py` on series H's base:
`hydrogen_r12`, the one registered radius with a whole closure, with the
momentum derived under form B's drive, the action re-fixed by series H's
rule and a `wave` detector on the proton's Node; and `helium_r12`,
binding-v1's square fixed as the nucleus with two electrons of the
register's electron point-symmetric about it, each releasing on the fan's
band so that the partner's rays push it. The pins before the runs are
[docs/designs/atoms/PINS.md](../../docs/designs/atoms/PINS.md); the runs
come after form B lands.

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
n p. `tools/click_readings/nucleus.py` reads the bodies' own `read` and
`contact` records and the border's clicks (DETECTOR) and their steps and
separations (GAMEBOARD), every line labelled by its kind; the register
entry is
[I, the nucleus (2026-09-20)](../../docs/EXPERIMENTS.md#i-the-nucleus-2026-09-20):
the deuteron bound at one Link and free at three, two protons bound or
repelled by the sign of Q^2 - G^2 - M^2, the square sheared apart and the
line held, 29 readings inside and 1 outside, registered and not tuned.

## The quarks series

The folder [quarks/](quarks/README.md) holds the seven worlds of series
R, written by `quarks/make_worlds.py`: series I's base with the up and the
down quarks as free families (4 and 9 units of content, the charges 1224
and -272 per unit: the whole charges 2/3 and -1/3 of the register's proton
7344) each holding one unit of the strong family `glue` (sigma 10000,
lifetime 3), three bodies in a line, a triangle, two triples side by side
and end to end, a kicked quark and a dressed line whose glue makes the
read mass 1836; the pins derived by the design's `quark_numbers.py` in
`quarks/expectations.json` and compared by `tests/test_quarks_expectations.py`;
`tools/click_readings/quarks.py` reads the bodies' `read`, `contact` and step
records and the border's clicks. The register entry is
[R, the quarks (2026-09-21)](../../docs/EXPERIMENTS.md#r-the-quarks-2026-09-21);
the design is [the quarks as families of the family table](../../docs/designs/quarks/QUARKS.md).

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
`width` 1, 8 and 32. `tools/click_readings/orbit.py` reads the probe's steps and
pushes and prints whether the orbit closed, its period, its mean radius,
its drift and the period ratio against the plane's k = 2; the register
entry is
[D, the orbit under the Beam Law, on the plane (2026-09-19)](../../docs/EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19):
one orbit closes by the criterion (S = 32, r = 12, an eccentric loop), the
mean push reads as derived, the grain of the push breaks the rest.

## The orbit read by a lamp on the probe (series D3, Newton after a detector)

The folder [orbit_lamp/](orbit_lamp/README.md) holds the five worlds of
series D3, written by `orbit_lamp/make_worlds.py` with their expectations
before the runs (`orbit_lamp/expectations.json`), the chief physicist's
design of 2026-09-22 (records 574 and 594) on the owner's word: series
D's plane and fan source, the probe a body of a paid family `probe` of
amount 2^12 (the lamp's reservoir) holding the free mass 2^20 the fan
pushes, at r = 12 and 24 with the circular momentum at n = 10, carrying a
lamp of rate [1, 8] on +y and -y (the recoil cancelling by the pair), and
a line of 121 one-Node `wave` detectors at y = 20 reading the rows' age,
so every click is the probe's x at the row's birth and the birth's tick;
two controls without the source and the equivalence world holding four
times the mass. `tools/click_readings/orbit_lamp.py` reads the click lines alone
(the period as the recurrence of x, the lagged second difference, the
ratio, the equivalence, the controls) and labels the probe's end state
and the homes GAMEBOARD; the register entry is
[D3, Newton after a detector (2026-09-22)](../../docs/EXPERIMENTS.md#d3-newton-after-a-detector-2026-09-22):
registered twice on 2026-09-22, no number moved: the first run at n = 10
(its pins form B's pace, which the engine does not run: the cause read
off the controls' pace and named, the rows kept as history) and the
re-run at n = 9 on the owner's word (the per-axis drive's circle, series
D's p = 576): the equivalence principle after a detector (to the Node
on every click) and the controls' pace to the tick closed; the ratio of
the two radii's recurrences 1.997 against 2.00 consistent with the 1 / r
force's scale symmetry, from one recurrence per radius on loops that are
not similar figures, not closed; a circle's period, amplitude and omega^2
outside, the grain of the push and the per-axis drive's anisotropy both
named, as series D registered the loops.

## The Heisenberg run

The folder [heisenberg/](heisenberg/README.md) holds the eight worlds of
the run A10, written by `heisenberg/make_worlds.py`: the plane stretched
to 120 x 161, a plane wave from a row of lamps on one heading, a wall
with ONE opening of width w (1, 3, 9, 27 Nodes) declared as one detector
that re-emits on a forward fan of 47 directions, and a screen 108 Links
behind it read as 161 one-Node detectors, every detector under the
world's `reading` (`wave` or `beam`). `tools/click_readings/heisenberg.py` reads
the spread of the screen's record and of its count against the
wavelength lambda = 8 / sqrt 3; the register entry is
[A10, the width of an opening and the spread behind it](../../docs/EXPERIMENTS.md#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-beam-law-2026-09-20):
the `wave` record narrows with w and the count does not; the product
w x FWHM reaches 0.886 lambda within 22 % at w = 27 and is not read at
the smaller widths on the sparse fan.

## The light-beside-a-mass series

The folder [lensing/](lensing/README.md) holds the four worlds of series
K, written by `lensing/make_worlds.py`: an open 57 x 41 x 41 box, a lamp
of the paid family `light` sending a narrow beam (five directions within
5 degrees of the heading) past a fixed mass of the free phase-less
family `m` at the centre (series E's fan of 290 directions, one or two
rays per direction per interval) at the impact distance b = 6 or 3,
toward a screen of 1681 one-Node `wave` pixels with the age moment on the
click record, and a control without the mass. `tools/click_readings/lensing.py`
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
`tools/click_readings/hubble_stars.py` reads, per star, the redshift from the
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
detector counting every ray that reaches it). `tools/click_readings/weak.py`
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

## The covariant series

The folder [covariant/](covariant/README.md) holds the four worlds of
series S, the covariant readings (`covariant-readings-v1`, the world key
`covariant_readings`; the model owner's decision of 2026-09-21, record 270
of the log of 2026-09-20, on DERIVATIONS_BEAM section 17 as amended in
17.6), written by `covariant/make_worlds.py` with their expectations before
the runs (`covariant/expectations.json`): the muon of J4 (the catalog's
`mu`, content 207, `become` at 64 into `e` with the products `beta` and
`nu`) at rest, at p = 3640 and at p = 12 856 label units on an open bar of
201 x 1 x 1 with the +x face at x = 200, and series G2's `coasting_none` in
its record form under the key at the grain 2^18. `tools/click_readings/covariant.py`
reads the products' clicks on the +x face and the centre's pointer
(DETECTOR) and the `become` lines, the `energy` lines with their
invariant and the intervals owed to proper time (GAMEBOARD) against the
pins; the register entry is
[S, the covariant readings (2026-09-21)](../../docs/EXPERIMENTS.md#s-the-covariant-readings-2026-09-21).

## The drive-b series

The folder [drive_b/](drive_b/README.md) holds the six worlds of series X,
the directional drive of a body (`drive-b-v1`, the world key `drive_b`, off
by default; the model owner's approval of form B, 2026-09-22, record 652 of
the log of 2026-09-20; the design [docs/designs/drive_b/DESIGN.md](../../docs/designs/drive_b/DESIGN.md)),
written by `drive_b/make_worlds.py` with their expectations before the runs
(`drive_b/expectations.json`): one body of content 64 at |**p**|_1 = 6000
on the axis, the plane diagonal and the cube diagonal from the centre of an
open 41^3 box, under the key and, as the controls, without it.
`tools/click_readings/drive_b.py` reads the body's click on a face (DETECTOR) and
the `step` lines against the line of the momentum and the accumulators'
bound (GAMEBOARD) against the pins; the register entry is
[X, the directional drive (2026-09-22)](../../docs/EXPERIMENTS.md#x-the-directional-drive-2026-09-22).

## The flow-link series

The folder [flow_link/](flow_link/README.md) holds the ring worlds of
`flow-link-v1` (the world key `flow_link`, off by default; the model
owner's decision of 2026-09-22, record 915 of the log of 2026-09-20; the
design [docs/designs/flow_weight/DESIGN.md](../../docs/designs/flow_weight/DESIGN.md)
section 4 with its algebra), written by `flow_link/make_worlds.py` with
their expectations before the run (`flow_link/expectations.json`): series
K's box with the mass 2^16 at the pin n S = d and a ring of lamps on the
heading at the impact distance b = 6, 3 and 8 (40, 16 and 48 starts) under
`optical: 0` and `optical: 1`, each with its control, and the registered
optical mass worlds under the key as the calibration.
`tools/click_readings/flow_link.py` reads every start's arrival Node and age at
the screen (DETECTOR), the ring's mean radial shift against the design's
pin (0.731 +- 0.025 Links at b = 6, gamma 1) and the conversions
`C_nodes` and `C_ring` through the stated lever-arm factor against
`2 c_f x 0.990 x L / sqrt(L^2 + b^2)` on the one constant, labelled so; the
verdict by the pins is in the folder's README.

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

## The c series

The folder [c_measured/](c_measured/README.md) holds the one world of
series Q, c measured behind a detector, written by `c_measured/make_world.py`
with its register (`expectations.json` and `derived.csv`: the closed form's
escape of every direction, DERIVATIONS_BEAM.md section 11.1, written before
the run): an open cube of 65^3 whose six faces are the detectors, one lamp
of `light` at the centre holding exactly one birth's content (one record
of 290 rows on the fan of 290 primitive directions with |a| + |b| + |c| <=
6 at tick 1, then nothing), 100 intervals. `tools/click_readings/c_measured.py`
reads the faces' clicks (the tick, the Node, the face; the direction off
the engine's label table) against the derived tick, Node and face of
every direction and the escapes' pace against c = 1 / sqrt 3; the
register entry is
[Q, c measured behind a detector (2026-09-21)](../../docs/EXPERIMENTS.md#q-c-measured-behind-a-detector-2026-09-21):
290 of 290 clicks at the derived tick, Node and face, the pace 0.5718 to
0.5893 (the mean 0.5810) over the fan at this GameBoard, 0.5774 to
0.5818 in the limit, against c = 0.5774.

## The massive rows

The folder [massive_rows/](massive_rows/README.md) holds the worlds of the
massive rows (`massive-rows-v1`, the model owner's yes of 2026-09-21,
record 332; the design docs/designs/massive_rows/DESIGN.md), written by
`massive_rows/make_worlds.py` from series L's generator beside
`slits_huygens` with `expectations.json` pinned before the run: the pin
`slits_matter` (the two slits with the massive family `matter`, M 64 and
p 220 at S 1 and h 1024, 4096 births over 5750 intervals), the 1024-birth
run `slits_matter_1024` (the wheel [633, 1024], 2700 intervals) and the
small replay world `slits_matter_small` (8 births read over 48 intervals,
its record registered by `tools/click_readings/massive_rows_replay.py`); `tools/click_readings/massive_rows.py` reads a run
against the pin, every number labelled DETECTOR (the screen's gathers,
the first `click` lines) or GAMEBOARD (the faces' and the wall's
completions, the books). The register entry is
[W, the massive rows (2026-09-21)](../../docs/EXPERIMENTS.md#w-the-massive-rows-2026-09-21).

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
