# The massive rows: the two slits of matter

The worlds of `massive-rows-v1` (the model owner's yes of 2026-09-21,
[record 332](../../../docs/LOG_2026-09-20.md); the mathematician's design
[docs/designs/massive_rows/DESIGN.md](../../../docs/designs/massive_rows/DESIGN.md),
ADMISSIBLE in the physics-rule review's three rounds; the identity in
[BEAM_LAW section 2](../../../docs/BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
and [HYPOTHESES section 26](../../../docs/HYPOTHESES.md#26-the-free-particle-as-a-record-of-massive-rows-de-broglies-fringes-from-h--p-stated-so-that-it-can-fail);
the register entry [W, the massive rows](../../../docs/EXPERIMENTS.md#w-the-massive-rows-2026-09-21)).
A free quantum of matter flies as a photon does: a paid family declared
`massive` births records of rows over its lamp's fan, each row carrying
the momentum label p_D at the scale p (the lamp's `momentum_magnitude`)
and the content M (the family's `quantum`), flying by the flight's one
accumulator at the rate 2 abs(p_D)_1 against the wall 2 E'_D (E'_D =
isqrt((Q S M)^2 + 3 p_D . p_D) at load), turning de Broglie's abs(p_a) N
/ h at every axis Link, and at the record's completion handing ONE
quantum, M and the one label, to the chosen set. Every number here is a
DETECTOR reading (a gather, a `click` line) or a GAMEBOARD reading (a
completion at a face or at the wall, the books, a row), labelled so.

The worlds are written by `make_worlds.py` from series L's generator
beside `slits_huygens` (`../amplitude/make_worlds.py`); `expectations.json`
beside them holds the pin, written before the run, with the line each
number is read on, the byte-identity digests of the amplitude worlds
registered from the base tree, and the small world's replay written by
`tools/click_readings/massive_rows_replay.py`; `tools/click_readings/massive_rows.py` reads a run against the pin. The
`age_bound` of every world is declared (a massive row's pace is its
family's, below the flight's).

## The pin: `slits_matter` (the design's section 4)

`slits_huygens`' plane and apparatus (the GameBoard of 60 x 121 x 1 with
z periodic, K 2^30, N 64, `suspension` 0, the stops at x = 7 and the wall
at x = 8 with the openings at y = 55 and 65, s = 10, re-releasing on the
Farey fan by angle of 1326 directions and the heading with the angle
weights, the screen at x = 52 read by 121 `sum` detectors on the wall's
own Nodes), the world key `massive_rows`, `width` 1, `action` 1024,
`age_bound` 2048, the family `matter` (`quantum` 64, a phase circle,
`massive`, no `phase_per_link`) in place of `light` in `families`, on the
lamp and in the openings' table key (the screen's events carry no table),
the lamp at (2, 60, 0) with `rate` [1, 1], the wheel [2531, 4096], its
five directions, `momentum_magnitude` 220, held 2^30 (the turn 1), 4096
births; 5750 intervals. The integers: E'_0 = 4096, E' = 4113 on every
direction (gamma = 1.0042), the pace 220 / 4113 = 0.05349 Links per
interval (0.0926 c), the turn 55 / 4 steps per axis Link, the wavelength
h / p = 256 / 55 = 4.6545 Links (the photon world's 4.654); the diagonal
(1, 1, 0)'s table entry (624, 8226, 4113) with the label (156, 156, 0) and
the turn (9984, 9984, 0) over 1024.

**Pinned before the run, each number with its line** (`expectations.json`
under `slits_matter`; the design's section 4, re-derived by the
accumulator rule on the engine's own Bresenham lines by
`docs/designs/massive_rows/massive_rows_round2_map.py` and again by
`tests/test_massive_rows.py` (g)):

- the lamp leg 139 intervals (the 11th Link of the diagonals (1, +-1, 0),
  the photon's 13): the first birth at tick 1, the first `rerelease` line
  at an opening at tick 140 (GAMEBOARD);
- the first `click` line of `matter` at the detector `screen_60` about
  the tick 955 within 5 (a row's arrival, the group pace: 815 after the
  re-release), at `screen_37` and `screen_83` about 1016 (DETECTOR);
- the longest row of a record 1468 intervals after its re-release ((17,
  26, 0) to the y face), so every record of 4096 births gathers within
  about 5753: the run 5750 (GAMEBOARD);
- the bright bands centred at the pixels 36.5, 60 and 83.5 within one,
  read on the gathers' chosen `screen_<y>` (DETECTOR);
- Pearson of the gathers' counts per pixel with the two-source cosine
  0.89 +- 0.03 on the declared Farey fan (the map's 0.886; the registered
  photon's 0.891 by the same walk), the visibility 0.95 +- 0.03 over the
  cosine's bright and dark pixels, the dark pixels 0 to 3 (DETECTOR);
- what refutes: a band off by more than one pixel (the wavelength not h /
  p), the centre's first `click` line off by more than 5 intervals of 955
  (the pace not p / E'), or no fringes (the phase not p . x);
- the records whose completion the ladder places at a face (about a
  third on the photon's lines and amounts) or at the wall's own sets (x =
  7 and 8) are a GAMEBOARD diagnostic reported beside the pin, not a
  reading of it; the screen's gathers are the detector reading.

**The 1024-birth run** `slits_matter_1024` (the design's section 7, the
Boss's order: the run made first): the same world at the wheel [633,
1024] (the golden rate at W = 1024) and 2700 intervals; the same pin read
on the gathers of the records 1 .. 1024, the cells' widths a quarter of
the pin's. The 4096-birth pin is run when the host allows (the design's
host cost: about 5.3 hours on the host that ran `slits_huygens` in 1334
s, the rows in flight about 11 times the photon's; the record about 4.6
GB of `click` lines).

**Run.** The 1024-birth run completed on 2026-09-21 (through the
runner, `python -m event_universe --init
examples/events/massive_rows/slits_matter_1024.json --output <dir>
--ticks 2700`): run by N check on the branch's heads 70df6514 and
e6de713d and by the architect on 40faf848 (the same engine sources), the
same `events.jsonl` and `state.json` byte for byte on all three (sha256
f561aedb... and afe643aa...), 2700 intervals completed, the books
balanced at every interval. Its reading by `tools/click_readings/massive_rows.py` is registered
under `slits_matter_1024.run` in `expectations.json`, every number
labelled; the pin's numbers are not moved. DETECTOR (the screen's
gathers and the first `click` lines): the first `click` line at
`screen_60` at tick 955 and at `screen_37` and `screen_83` at tick 1016
(the pin 955 and 1016 within 5: inside); the bands' centres 37.06,
59.99 and 83.02 (the pin 36.5, 60 and 83.5 within 1: inside); Pearson
of the 121 pixels' counts with the two-source cosine 0.88 (the pin 0.89
within 0.03: inside); the visibility 0.964 (0.95 within 0.03: inside);
the dark maximum 1 (the pin 0 to 3: inside); 433 clicks over the 121
pixels, the bright counts 10, 5, 10, 9, 14, 13, 14, 10, 10, 5, 10; every
pinned number inside its bracket, the run PASSES. GAMEBOARD (a
diagnostic beside the pin): 1024 births read, 2698 records born, 1092
gathered and 1606 open at the end; the wall's completions 215, the two
faces' 188 and 188; the transit and content lines balanced at the end
(the waiting lines of the open records beside them).

## The small world of the replay: `slits_matter_small`

A plane of 12 x 21 x 1 with z periodic, K 2^20, N 64, the world key,
`width` 1, `action` 1024, `age_bound` 256; a lamp of `matter` (`quantum`
4, `momentum_magnitude` 400: E'_0 = 256, E' = 738 on a heading, the pace
400 / 738 Links per interval) at (1, 10, 0) with `rate` [1, 1] on the five
directions of the pin's lamp and the wheel [5, 8]; a wall at x = 4 of the
paid family `wall` with the openings at y = 8 and 12 (where the lamp's
diagonals land after five Links) re-releasing on a fan of five directions
((1, 0, 0), (2, +-1, 0), (1, +-1, 0)) with equal weights; a screen at x =
10 of 21 `sum` pixels; 48 intervals. The register (`expectations.json`
under `slits_matter_small.replay`, written by `tools/click_readings/massive_rows_replay.py` from
the engine as shipped, no number typed by hand) holds the run's digests
(state, books, events), the gathers of the records 1 .. 8 (the tick, the
chosen set, the Node, the content 4 and the one label 4 p_D), the books
and the momentum block at the end and the layer's line;
`tests/test_massive_rows.py` (f) replays it bit-exact. What the world
shows (GAMEBOARD: the record; DETECTOR: the gathers): the first record's
diagonals reach the openings at tick 10 and its fan rows the screen from
tick 20, its completion at tick 21; every gather places one quantum of
content 4 with the label of one direction of the table at one Node, the
rest of the record cancelled; the books balanced at every tick.

## The byte identity

`expectations.json` under `byte_identity` holds the digests of `mz_345`,
`bell_0_8` and `slits_low` (series L's generator) at their ticks, written
from the base tree before the build (the design's head b1248102, main
65b65f45): `tests/test_massive_rows.py` (a) reads them after it, with the
gate set's lamp-free digests, and shows every world without the key byte
identical (the pair (f_F, q_F) = (1, 0) on every family, `acc_turn`
omitted from the rows' record, no `waiting` line).

## Re-read in the row's own clock (2026-09-22)

The model owner's word of records 678, 707 and 709 of docs/LOG_2026-09-20.md:
the GameBoard holds the clock of every experiment read through a
detector. The group pace is pinned as the row's `age` on its first
`click` line at `screen_60`, `screen_37` and `screen_83` (the row's own
clock since its re-release at the opening: 815 and 876 within 5,
`first_click_age` of `expectations.json`; DETECTOR), the line's tick the
record's ordering (the re-release tick 140 plus the age; GAMEBOARD, the
lattice's clock); `tools/click_readings/massive_rows.py` reads both so. The 1024-birth run's
record replayed on main's engine reads 815 and 876 exactly; the reading
and the verdict are in
[the register's entry](../../../docs/EXPERIMENTS.md#w-the-massive-rows-2026-09-21),
"Re-read in the row's own clock (2026-09-22)".
