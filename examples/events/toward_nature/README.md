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
U_1 = c_1 / (2 Gamma) = 0.1. The emitter's own Nodes read its stock and the
mirror's its content in both worlds alike. 6000 intervals each.

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