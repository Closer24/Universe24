# The runs toward nature, without pins (rows 1 to 3)

The diagnostic rows of ALGEBRA.md 9.59 (0) to (3) (the model owner's question of
2026-09-25 through the Boss, record 2030: "when will experiments start, to see
that there is a direction toward nature, without pins?"), on today's law (the
first-order rule of 9.50 (13)). No `expectations.json` is written here: no pin,
no verdict (9.59 (6)). Every reading below is labelled by its kind (DETECTOR a
click, GAMEBOARD a diagnostic of the rows, COMPUTATION a number of the
declaration or of the reader's arithmetic, HOST the machine's cost) and is set
beside nature's value only to see the direction. A reading outside the
mathematician's band goes to him before any word (9.59 (6)).

Files: `make_worlds.py` writes the four worlds of rows (1) and (2) from the
light clock's own form (`../detector_law/make_worlds.py::light_clock`, the one
table of 9.30) under Gamma = 10^4 (9.57 (2), 9.59 (0)); `read_runs.py` reads
the one command's outputs (`tools/run_inputs.py`). Row (3) runs the dark body's
two worlds (`../dark_body/`) as they stand. The unit test is
`tests/test_toward_nature.py`.

    PYTHONPATH=src python examples/events/toward_nature/make_worlds.py
    PYTHONPATH=src python tools/run_inputs.py --out RUNS --jobs 4 examples/events/toward_nature/*.json
    PYTHONPATH=src python examples/events/toward_nature/read_runs.py RUNS

## Row (1): the redshift

Two light clocks on the chain [760, 3, 3], the arm 558 Links (the emitter A at
[100, 132) with its train along +x, the mirror at [690, 694), the set `at_well`
A's own Nodes): `redshift_top.json` with the arm at the level 0 and
`redshift_bottom.json` with the arm's free Nodes [132, 690) held at the uniform
level c_1 = 2000 by a holder body of a fifth family (`well`, the matter kind's
pair; the hold of 9.45 (2): the level at a body's Nodes is its content), so
U_1 = c_1 / (2 Gamma) = 0.1. The emitter's own Nodes read its one own quantum
plus its stock (the given family's content held at the body, BUILD.md section 26
item 47) and the mirror's its content in both worlds alike. 6000 intervals each.

The reading is the wait from a record's giving click to its click at `at_well`
(the light clock's tick, 9.24 (6)), run 2026-09-25:

| Reading | Kind | Top (the arm at 0) | Bottom (the arm at 2000) |
| --- | --- | --- | --- |
| Clicks at `at_well` | DETECTOR | 59 | 48 (2 early, 46 the mirror's) |
| Mean wait, rms, standard error | DETECTOR | 2445.6, 82.6, 10.7 | the mirror's cluster 3137.5, 133.9, 19.7 |
| Clicks at the faces | DETECTOR | 5 | 15 |
| Ratio bottom / top of the means | COMPUTATION | 1.283 +- 0.010 (the mirror's cluster); 1.242 +- 0.030 with the two early clicks | |

The two early clicks of the bottom world (waits 657 and 871, below the top
world's least 2158) are records turned back at the well's edge before the
mirror; they are stated and the mirror's cluster is read alone.

Set beside: the mathematician's continuum form 1 / sqrt(1 - 2 U_1) = 1.118
(9.59 (1)); nature 1 + U_1 = 1.100 at first order. THE DIRECTION HOLDS: the
clock in the well is slower. THE SIZE IS THE LATTICE'S OWN, not the continuum's:
the given train has wavelength 4, k = pi / 2, the band's middle, where the
rule's dispersion 6 Gamma cos omega = (Gamma - c) (2 cos k + 4) + 6 c (the
chain's cross-section [3, 3] periodic) is far from the continuum. With the
frequency conserved across the well's edge (cos omega_0 = 2 / 3 at c = 0) the
wave number refracts to cos k' = -0.25 in the well and the group velocity
(Gamma - c) sin k / (3 Gamma sin omega) falls from 0.447 to 0.346: the flight
ratio 1.291 (COMPUTATION, `read_runs.py`; a scratch run of the exact rule on a
chain reads 1.26 to 1.29). Read 1.283 +- 0.010. So on today's law at k = pi / 2
the light clock in a well reads nearer 1 / (1 - c / Gamma) than 1 / sqrt(1 - c
/ Gamma); the row's expectation at the lattice's wave number, or the
wavelength the rows should use, is the mathematician's to state (his finding
1 of 2026-09-25).

### The long-wave pair for the check-mode runs

`redshift_top_long.json` and `redshift_bottom_long.json`: the same two clocks
with the given clock near k = 0.302, the mathematician's rule for the rows
toward nature (ALGEBRA.md 9.62 (1): at the band's middle the row reads the
lattice's grain; at k = 0.3 the lattice's term is 0.3 percent). The light
[4096, 21] on the circle N = 2048 gives the whole wavelength 21 Links (k = 2 pi
/ 21 = 0.299; the light clock row's own [2464, 25] gives 20.8, not whole, and a
train needs a whole wavelength, 9.17 (6a)); the train 8 periods over 168 Nodes;
the emitter A at [200, 368) (one train beyond the low face slab, 9.25 (11) (b)),
the mirror at [690, 694), the arm 322 Links; the bottom's holder over [368, 690)
at 2000. On the Einstein form (9.62 (2)) a light clock with a declared arm reads
the coordinate speed of light, 1 / (1 - 2 U_1) = 1.250 (1.258 at k = 0.302),
the Shapiro reading in another dress; a clock body reads the redshift, 1 /
sqrt(1 - 2 U_1 + 2 U_1^2) = 1.104; both are set beside nature's, each against
its own. These two worlds are the check-mode rows of 9.61. THE FIRST CHECK-MODE
TABLE (2026-09-25, the law as built, ALGEBRA.md 9.57 (1) at Gamma 10^4; no pin, no
verdict; DETECTOR unless marked):

| Row | Expected (blind, the mathematician's) | Read | Direction |
| --- | --- | --- | --- |
| The light clock (`../massive_record/light_clock.json`, k = pi / 2), the mean wait giving to click | 300 +- 9 (9.24 (6), 9.46 (10) (a)) times the self-level 1 + 64 / (2 Gamma) = 1.0032 (9.61 (1) (b)): 301 | 301.8, rms 20.3, standard error 2.5, 64 clicks | holds |
| The redshift, long wave, the ratio bottom over top of the mean waits | a light clock with a declared arm reads 1 / (1 - 2 U_1) = 1.250 on the arm's share of the tick (9.62 (2); 1.258 at k = 0.302); the arm's share here 1120 of 1283 intervals (COMPUTATION: 2 x 322 / 0.575), so 1.218 to 1.225 on the whole tick; a clock body would read 1.104; today's law 1.118 on the share, 1.103 on the tick | 1.205 +- 0.011 (64 and 64 clicks; the top 1283.2 +- 6.8, the bottom 1546.6 +- 10.7) | holds: the well slows the clock by the coordinate speed of light's factor, not the redshift's; 1.2 to 1.8 standard errors below the Einstein form's line, 9 above today's law's |

The host: 8, 26 and 32 seconds for the three runs with the support-only step.

THE SAME TWO ROWS ON THE HEAD OF ITEM 47 (the stock as the given family's content held at
the body, ALGEBRA.md 9.51 (8); the emitter's level 65, its one own quantum beside the
stock; DETECTOR; no pin):

| Row | Expected | Read | Direction |
| --- | --- | --- | --- |
| The light clock, the mean wait giving to click | 300 +- 9 times 1 + 65 / (2 Gamma) = 1.00325: 301 | 301.9, rms 17.8, standard error 1.9, 85 clicks | holds |
| The redshift, long wave, the ratio bottom over top | 1.218 to 1.225 (the Einstein form on the arm's share); 1.104 a clock body; 1.103 today's law | 1.201 +- 0.010 (62 and 72 clicks; the top 1294.0 +- 7.2, the bottom 1553.8 +- 10.1) | holds as before |

THE FINDING OF THIS HEAD (a consequence of the two rules as written, for the
mathematician's line): the emitter's own set takes its light back (`at_well` is bound to
the emitter's Nodes), the taken quantum is held light again, and the rung gives it again
while the run lasts: 85 givings on a stock of 64 in 4800 intervals, 62 and 72 on 64 in
6000 (before item 47 the stock was spent once, 64 givings). The reading per record, the
wait from the giving to the click, is unchanged in kind; the clocks run while the run
lasts, as an atom re-emits the light it absorbs.

## Row (2): Lorentz

The light clock at rest (`lorentz_rest.json`) and the same clock carried along
its arm (`lorentz_moving.json`, the longitudinal clock of 9.24 (6)): the
emitter, its mirror and its set hop together one Link every 4 intervals, v = 1
/ 4, by the declared momentum of each block at one quarter of its own drive
wall 3 Q width amount (`drive_wall`), so that both accumulators carry at the
same intervals (checked, GAMEBOARD: 25 hops each per 100 intervals, the gap
constant). The chain [1500, 3, 3], the clock at [100, 194), 3600 intervals.
The board's light at k = pi / 2 runs at c_l = 0.447 Links per interval (the
plain rule's group velocity, 9.24 (6) at this wave number), so v / c_l =
0.559: nature's gamma 1.206, the longitudinal form's gamma^2 = 1.455 (9.24
(6): the board's material does not contract, a PREDICTION against nature's
gamma). The transverse clock (gamma alone) needs a layer and an isotropic
emitter and is not built here.

| Reading | Kind | Rest | Moving |
| --- | --- | --- | --- |
| Clicks at `at_well` | DETECTOR | 64 | 25 (9 at the faces) |
| Mean wait, rms, standard error | DETECTOR | 303.1, 18.7, 2.3 | 1352.6, 440.8, 88.2; the waits grow from 631 to 2636 over the run |
| The same under `body_record` | DETECTOR | 303.9 (62 clicks) | 1444.3 (31 clicks) |

NOT A READING OF THE TICK. A trace of one record (GAMEBOARD) shows the light
leaving the emitter at 0.447, meeting the receding mirror, turning, coming
back at 0.40, entering the moving set and passing through it without a click,
then wandering behind it; a part left on the block clicks hundreds of
intervals later. Two findings for the mathematician (2026-09-25): (2) the
set's ladder books the plain inward flux at its Ports (9.25 (2)); a hop covers
the rows in front of the block without a Port crossing, so nothing is booked
for them, and at v = 1 / 4 against light at 0.4 most of a record enters by
hops: the moving detector does not take on the first pass (the proposal put to
him: at a hop the rows on the Nodes the detector newly covers are booked as
inward flux, their share of the norm, as 9.52 (4) (i) moves the field face to
face); (3) the moving emitter gives its train at rest in the board's frame,
the same k as the resting one, where nature's moving source gives
Doppler-shifted light. The row has no reading until both are ruled; the files
stand.

THE ROW ON THE HEAD OF ITEM 48 (the taking at a hop, ALGEBRA.md 9.62 (3), built; the
detectors' Ports re-read at every hop, the host bug behind finding 2; DETECTOR unless
marked; no pin), the same two worlds rerun in check mode:

| Reading | Rest | Moving |
| --- | --- | --- |
| Clicks at `at_well` | 80 (1 at a face) | 69 |
| Mean wait, rms, standard error | 294.7, 20.8, 2.3 | 513.3, 144.2, 17.4 |
| Waits by 50-interval bins | 200: 1, 250: 46, 300: 33 | 50: 1, 150: 1, 200: 3, 250: 2, 300: 1, 350: 5, 400: 8, 450: 8, 500: 5, 550: 13, 600: 10, 650: 10, 700: 2 |
| Ratio moving / rest of the means (COMPUTATION) | | 1.742 +- 0.060; the longitudinal form's gamma^2 = 1.455 on the flight (9.24 (6)), 1.40 on the whole tick with the rung's wait |

The moving clock ticks now (finding 2 closed: the light returning from the mirror is
booked at the hops it is overtaken by and at the Ports). The spread is the row's own,
for the mathematician (GAMEBOARD trace of one late record): the light returning from the
receding mirror carries 0.735 of its given norm (the form is not conserved under a
hopping pair region, Doppler's loss at the mirror), the ladder's threshold stands on the
given norm, so a record whose residue asks more than the returned norm cannot click on
the first pass (the cluster at 350 to 500) and clicks late on what lingers (550 to 700);
the few early clicks (below 300) are the outgoing train's rows at the hops' grain.
Finding 3 (the moving emitter gives its train at rest) stands for 9.62 (4).

THE LONG-WAVE PAIR WITH DOPPLER (ALGEBRA.md 9.62 (1) and (4); BUILD.md section 26 item
49; `lorentz_rest_long.json`, `lorentz_moving_long.json`): the light [4096, 21] on N =
2048 (k = 0.299, c_l = 0.573), the emitter at 200, the mirror 90 Links beyond the train's
head; the moving emitter's train at the boosted wave number k gamma (1 + v / c_l), the
wavelength 13 (the body 104 Nodes in place of 168), hopping with its mirror one Link every
4 intervals; 3600 intervals; the reading in check mode on the head of item 49 (DETECTOR; no
pin):

| Reading | Rest | Moving |
| --- | --- | --- |
| Clicks at `at_well` | 51 | 52 |
| Mean wait, rms, standard error | 459.0, 58.2, 8.1 | 569.6, 59.6, 8.3 |
| Ratio moving / rest of the means (COMPUTATION) | | 1.241 +- 0.028; the longitudinal form's gamma^2 = 1.235 on the flight at v / c_l = 0.436 (9.24 (6)); nature's gamma 1.111 |

The rest tick reads the round trip 2 x 90 / 0.573 = 314 plus the returning train's passage
into its own body (168 Nodes at 0.573, the click at the residue's rung within it, about 146
on average): 460 (COMPUTATION), read 459. The moving clock's spread is the rest clock's
(rms 60 against 58): with the boosted train the clusters of the k = pi / 2 world are gone.
The blind numbers for this pair are asked of the mathematician; the ratio stands beside the
longitudinal form's gamma^2 as a check-mode reading, no verdict.

## Row (3): the bending on today's law

Two forms. FIRST, the dark body's two worlds (`../dark_body/dark.json` and
`bright.json`, ALGEBRA.md 9.54 (4); BUILD.md section 26 item 39) run as they
stand (Gamma 10^6, the body's content 10^5, the beam 5 wide, 30 records, the
beam's line 45 Links from the body's centre, the screen 180 Links beyond, 2400
intervals; `read_bending.py`). SECOND, `bending.json`, the same layout under
row (3)'s numbers (`make_worlds.py::bending`, the dark body's generator with
its constants set: Gamma 10^4; the body's content 4812 so that the static
level on the beam's line under the body is c_b = 2000, U_b = 0.1; the beam 20
wide; 100 records; 5600 intervals; the body dark), read with `read_bending.py
RUNS --bending`. The reading is the centroid of the emitter's records' clicks
over the screen's cubes less the beam's line (toward the body positive),
DETECTOR, set beside the closed form 2 U_b L of 9.59 (3) and the ray through
the static field (COMPUTATION, `../dark_body/make_worlds.py::ray_bend`). The
dark body row's own pins are not read: this is the one command without pins.

Read 2026-09-25 (PRE-CHANGE CONTROLS on today's law, the Boss's record 2038):

| Reading | Kind | The dark body's `dark.json` (Gamma 10^6, the beam 5 wide, 30 records) | Its `bright.json` (the body an emitter too, the shadow control) | `bending.json` (Gamma 10^4, the beam 20 wide, 100 records) |
| --- | --- | --- | --- | --- |
| The emitter's records' clicks at the screen (at the faces; at the body's set) | DETECTOR | 25 (5; no set) | 21 (5; 4 at `at_body`, the shadow) | 95 (5; no set) |
| The body's own records' clicks | DETECTOR | 0 (dark) | 83 (74 at the screen, 9 at the faces) | 0 (dark) |
| Centroid of the emitter's clicks less the beam's line, toward the body positive; rms; standard error | DETECTOR | +5.68 Links; 37.07; 7.41 | +4.00 Links; 34.59; 7.55 | +11.96 Links; 31.19; 3.20 |
| The level on the beam's line under the body, c_b, from the declared content | COMPUTATION | 41561 (U_b = 0.021) | 41561 | 2000 (U_b = 0.1) |
| 2 U_b L (the cube's 1 / r form, which does not hold on this layer, 9.61 (2) (c)) | COMPUTATION | 7.5 | 7.5 | 36.0 |
| The ray through the static field (`ray_bend`, the beam's centre line at k = pi / 2) | COMPUTATION | 13.7 | 13.7 | 76.3 |
| Host seconds, the one command, before the support-only step | HOST | 933 | 3673 | 1032 |

The dark and the bright worlds read the same centroid within their errors (5.7
and 4.0 against 7.4 and 7.6), the dark body's row's own "the same in both within
one cube" (9.54 (4)); the bright body's shadow takes 4 of the 30 records at
`at_body` and its own 83 given records reach the screen. The redshift's two
worlds took 58 and 73 host seconds, Lorentz's 17 and 57, before the support-only
step.

THE DIRECTION HOLDS in both: the centroid moves toward the body, in the second
world by 3.7 standard errors. THE SIZE is far below the ray's number: the beam
at k = pi / 2 is not a ray; it spreads to an rms of 31 to 37 Links at the
screen (wider than the body's distance from the line), so the clicks are the
whole spread beam's, with its part near the body bent most and its far part
hardly; the ray through the static field traces the centre line alone. The
dark body's world with 30 records cannot read its 7 to 14 Links at all (the
standard error 7.4). Both are PRE-CHANGE CONTROLS; the row toward nature moves
to the given clock at k = 0.302 (9.62 (1)), where the lattice's term is 0.3
percent and the beam spreads less, and is read again after the change of
9.60 and the Einstein form (the check-mode runs of 9.61). 