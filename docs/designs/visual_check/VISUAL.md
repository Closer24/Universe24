# The visual check of the paper's findings: what a picture shows, with the new code (the owner's word, record 929 of 2026-09-22)

The Visual Checker, 2026-09-22, on the Boss's bounded order: go over the
findings of the paper (the manuscript of `paper/general_formula/` on the
branch `claude/paper-owner-review-five` at 9d1eeaf8) that a picture can
show, render each from ONE re-run of its registered world with the code on
`origin/main` at 20d3a45afcd0498b4cae97d0858bfd27f246498c, and say whether
what the paper claims is seen. Nothing here changes a law, a pin or a
verdict; nothing new is declared and no world is edited; a NOT SEEN goes
to the Boss and the reviewer, not into the paper.

**What a picture is.** A figure here is a diagnostic, never a measurement
and never compared with nature (the model owner, record 281 of
[the log of 2026-09-20](../../LOG_2026-09-20.md)). Each figure names the
kind of what it draws: DETECTOR, the click and gather lines of the run's
`events.jsonl` (the only kind reality has); GAMEBOARD, the host's view of
the board (a body's `step` lines), drawn beside as a diagnostic. Every
number in the table is read from the record by the script named in the
row; the scripts of this folder read events only, count clicks and read
ticks and Nodes, and their only arithmetic on a physical number is exact
(integers and reduced pairs); no float enters a physical number. The runs
are the registered worlds of `examples/events/`, run headless by the
register's runner (`event-universe --init <world> --output <folder>`),
every one `completed` and conserved at every tick, the engine's source
fingerprint `d537d4435b92` (the sha256 of the source at 20d3a45a).

**Where the figures are.** No PNG is committed: CONTRIBUTING.md keeps
generated outputs outside source commits. The eleven figures are
published as one private page, "Visual check 2026-09-22":
https://claude.ai/artifact/KVCpQxkhGwTsHdx9yTYkoA (private; the owner shares it from the page). Each figure is captioned with its kind and its
run's SHA. To remake them:

    PYTHONPATH=src:docs/designs/visual_check .venv/bin/python docs/designs/visual_check/fig_<name>.py <runs dir> <out dir>

where `<runs dir>` holds the runner's folders named `<series>__<world>`.
The printout of every script, the readings of the table, is
[visual_check.out](visual_check.out) beside them.

## The table: one row per finding

The claim is quoted with the paper's row or table (NATURE rows are the
paper's Table `tab:nature`; the conversion table is `tab:conversion`; "the
seven confirmations" is the paper's paragraph of that name). The verdict
is one of three: SEEN (the figure shows what the claim says, in the
claim's own numbers), NOT SEEN (the figure shows something else, stated
without interpretation), NOT RENDERABLE (no cheap registered run gives the
picture; the cost is said).

| # | The paper's finding | The figure (its script) | What the figure shows | Kind | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | The two-slit fringes in the clicks of `slits_huygens` (NATURE row 2a; the conversion table): the dark pixels 0 to 3 clicks, the bright about 40 to 51, the bands 23.5 pixels apart, over 4096 births; `slits_low` the same geometry at 64 births (L2) | `fig_two_slits.png` (fig_two_slits.py (`docs/designs/visual_check/fig_two_slits.py`, deleted 2026-09-26)) | `slits_huygens`: 4096 records read, screen 1711 clicks on 107 pixels, wall 882, faces 1503 (the register's numbers exactly); the counts y = 40 .. 80 are 29 41 28 27 19 15 8 6 3 0 1 5 7 15 18 20 36 45 51 51 49 51 51 45 36 20 18 15 7 5 1 0 3 6 9 14 19 26 29 42 28, the register's row to the click; three bright bands (the middle 45 to 51 clicks at y = 57 to 63, the sides 38 to 42) with the dark runs of at most 3 clicks at y = 23, 48 to 50, 70 to 72 and 97, whose centres are 26, 22 and 26 pixels apart (the mean 74/3 = 24.7) for the paper's 23.5; every pixel's count within 2 of the first record's rung width x 4096. `slits_low`: 64 records, screen 15 clicks on 14 pixels (y = 60 twice), wall 34, faces 15, the register's numbers; no band is visible at 64 births | DETECTOR (the pixel chosen per record; the first record's rungs as the expected counts) | SEEN (the fringes and the dark pixels 0 to 3 as claimed; the band spacing read as 22 and 26 pixels between the dark centres around the paper's 23.5, which is the paper's own reading of the bright centres and not remade here) |
| 2 | The single opening (NATURE row 10, the spread 0.886): the paper's status NOT YET, no completed registered run under the click; the register's one-opening reference `slits_one` (L2's control, one birth, "the record without the two-source term") | `fig_one_slit.png` (fig_one_slit.py (`docs/designs/visual_check/fig_one_slit.py`, deleted 2026-09-26)) | `slits_one`: 108 screen clicks on 75 pixels from y = 0 to 120, at most 4 on a pixel, no fringe; the age at the click 75 to 152 intervals (mean 1705/18); the clicks per set equal the register's (wall 34 (11, 12, 11), screen 15 on 14 pixels and faces 15 in `slits_low`'s 64 births, read by fig_two_slits) | DETECTOR (the screen's click lines) | NOT RENDERABLE for row 10 (no registered run of the one-opening spread under the click; the reference is drawn as the two-slit control, not as row 10) |
| 3 | Mach-Zehnder (NATURE row 2b; the seven confirmations): 64 / 0 with equal arms, 0 / 64 at a half turn, 32 / 32 at a quarter, over 64 births | `fig_mach_zehnder.png` (fig_mach_zehnder.py (`docs/designs/visual_check/fig_mach_zehnder.py`, deleted 2026-09-26)) | `mz_equal` D1 64, D2 0; `mz_half` D1 0, D2 64; `mz_quarter` D1 32, D2 32, over the first 64 births by ordinal | DETECTOR (the set chosen per gather) | SEEN |
| 4 | Bell's cells and the plateau (NATURE row 1a; the CHSH theorem; the paper's Figure S(N)): the cells 27, 5, 5, 27 per setting pair over 64 births, S = 2.75 = 176 / 64 at N = 64; S = 181 / 64 at N = 512, 2048, 4096 and 8192 and 5793 / 2048 at 16384 | `fig_bell_cells.png` (fig_bell_cells.py (`docs/designs/visual_check/fig_bell_cells.py`, deleted 2026-09-26)) | N = 64: `bell_0_8` 27, 5, 5, 27 (E 44); `bell_0_24` 5, 27, 27, 5 (E -44); `bell_16_8` 27, 5, 5, 27; `bell_16_24` 27, 5, 5, 27; S = 176 / 64. N = 512: 219, 37, 37, 219 and 218, 38, 38, 218, S N = 1448 = 181 / 64 x 512; N = 2048: 874, 150 and S = 181 / 64; N = 4096: 1749, 299 and 1747, 301, S = 181 / 64; N = 8192: 3498, 598 and 3494, 602, S = 181 / 64; N = 16384: 6996, 1196 and 6989, 1203, S = 5793 / 2048 | DETECTOR (the two outcomes per gather) | SEEN |
| 5 | Malus (NATURE row 9; A12 under the click): 128 of 256 at 45 degrees, 0 of 256 at 90 degrees, 219 of 256 at 22.5 degrees | `fig_malus.png` (fig_malus.py (`docs/designs/visual_check/fig_malus.py`, deleted 2026-09-26)) | `malus_a` 128 transmitted, 128 absorbed; `malus_b` 0 transmitted, 256 absorbed; `malus_22_5` 219 transmitted, 37 absorbed, of 256 births each | DETECTOR (the second polariser's outcome per gather) | SEEN |
| 6a | The orbit's period ratio (the conversion table, "Kepler's period, T(24) / T(12) = 2 on the plane"; D3): 1.997 in [1.82, 2.18] | `fig_orbit.png` (fig_orbit.py (`docs/designs/visual_check/fig_orbit.py`, deleted 2026-09-26)) | `r12`: the centre column x = 60 crossed downward at the birth ticks 124 and 1592/3 = 530.7, one recurrence 1220/3 = 406.7; `r24`: downward at 1152/5 = 230.4 and 3128/3 = 1042.7, one recurrence 12184/15 = 812.3; the ratio 3046/1525 = 1.997 | DETECTOR (the line's clicks: x at the birth tick) | SEEN (as the ratio of two single recurrences) |
| 6b | The orbit's loop at the pinned period (the same row; the pins T = 343 at r = 12 and 687 at r = 24 within 9 percent, the amplitude r - 1 to r + 2) | the same figure | No closed loop is seen: `r12`'s clicks run from x = 18 to 86 (the amplitude 34 Links for the pin 12 in [11, 14]) and the probe leaves through `face:+y` at tick 698; `r24`'s from x = 1 to 103 (the amplitude 51 for the pin 24 in [23, 26]), the escape through `face:-x` at 1239; each single recurrence is outside its pin's bracket (406.7 for 343, [312.6, 374.4]; 812.3 for 687, [625.1, 748.8]). The GAMEBOARD panel shows the probe's steps: one turn about the source, then away. The register's own D3 table registers the same (outside, outside, outside) | DETECTOR (the clicks); GAMEBOARD (the probe's steps, a diagnostic) | NOT SEEN (the picture shows one turn and an escape, not a loop at the pinned period; the ratio of row 6a is a ratio of two open arcs) |
| 7 | The clock's k inside a shell (the conversion table: "series X k = 0.9089 at r = 4 for the pin 0.9108") | none; fig_clock_k.py (`docs/designs/visual_check/fig_clock_k.py`, deleted 2026-09-26) is written and reads the click lines as the register's `read_runs.py` does | Not rendered: the registered world `shell_clock/age_4` (114 x 15 x 15 Nodes, 450 sources, 500 intervals) is not a cheap world on this host: stopped at interval 236 of 500 after about 14 minutes of one core with 5.9 GB of `events.jsonl` written (the sources' rows click on the faces); the record deleted. Its control `control_4` ran in 1.3 s | DETECTOR (would be: the birth ordinal against the click's tick) | NOT RENDERABLE within the cheap bound (the host cost above) |
| 8 | The far pair (the seven confirmations: "the far pair's cells 27, 5, 5, 27"; L3, `bell_16_24_far`, Bob's counters 116 Links farther, no maintenance) | `fig_far_pair.png` (fig_far_pair.py (`docs/designs/visual_check/fig_far_pair.py`, deleted 2026-09-26)) | `bell_16_24` 27, 5, 5, 27 with the completions at ticks 13 to 77; `bell_16_24_far` 27, 5, 5, 27 with the completions at ticks 212 to 276 (the record's one click at the far arm's arrival) | DETECTOR (the two outcomes and the tick per gather) | SEEN |
| 9 | The redshift ladder: the Hubble diagram behind the detector, z against distance for the 24 stars (NATURE rows 3 and 4b; series G2, `examples/events/hubble_stars/`) | none | Not rendered: every G2 world is 301^3 Nodes over 400 intervals; the register itself does not re-run them ("not re-run here (301^3 Nodes over 400 intervals)", the G2 entry). The nearest cheap registered redshift reading, the two lamps of series T, is row 13 | DETECTOR (would be: the pointer's turn per star) | NOT RENDERABLE within the cheap bound |
| 10 | GHZ (the seven confirmations): the four allowed triples 16 each, the products +1 (xxx) and -1 (xyy, yxy, yyx), the others 0; yyy every triple 8 | `fig_ghz.png` (fig_ghz.py (`docs/designs/visual_check/fig_ghz.py`, deleted 2026-09-26)) | `ghz_xxx` +++ 16, +-- 16, -+- 16, --+ 16, the others 0, the product +1; `ghz_xyy`, `ghz_yxy`, `ghz_yyx` ++- 16, +-+ 16, -++ 16, --- 16, the product -1; `ghz_yyy` 8 on each of the eight triples | DETECTOR (the three outcomes per gather) | SEEN |
| 11 | The bending's arrival Nodes (the seven confirmations: "light beside a mass, series K, three worlds, the deflection 0.000 pixel, the delay 0.00 interval"; the paper's row 13 ground) | `fig_bending.png` (fig_bending.py (`docs/designs/visual_check/fig_bending.py`, deleted 2026-09-26)) | `control`, `mass`, `heavy`: 1553 light clicks each on the same 5 pixels of the screen, the centroid y = 26, z = 20 exactly (the lamp's line), the mean age 138837/1553 = 89.399 intervals in all three: against the control 0 pixel in y and z, 0 interval, 0 clicks of difference; `near` (the lamp at y = 23): 1553 clicks, the centroid y = 23, z = 20, on its own lamp's line, the same mean age | DETECTOR (the screen's click lines: pixel, age) | SEEN |
| 12 | The atom's baseline loop widening (branch `atom-baseline-run` at 01e86183, RUN.md section 4): the electron widens every quarter turn (the crossings at 13, 13, 17 and 26 Links) and leaves through `face:+y` at count 3407; the faces' clicks of `e` 342, 337, 342, 339 | `fig_atom.png` (fig_atom.py (`docs/designs/visual_check/fig_atom.py`, deleted 2026-09-26)) | The side faces' clicks of `e`: `face:+x` 342, `face:-x` 337, `face:+y` 342, `face:-y` 339, the coordinate they carry from 12 Links off the proton's Node at the start to 26 at the last quarter (the picture: an amplitude growing turn by turn); the electron's own escape click on `face:+y` at tick 3407 at Node (29, 52, 26); the same counts and escape as the baseline's | DETECTOR (the faces' clicks); GAMEBOARD (the electron's 173 steps, a diagnostic) | SEEN |
| 13 | The clock's form at two distances (NATURE row 12; the conversion table): the ratio of the two lamps' shifts 1.907 for the pin 1.909 +- 0.05 under the age word (series T, read before the generic entry of 2026-09-22) | `fig_clock_form.png` (fig_clock_form.py (`docs/designs/visual_check/fig_clock_form.py`, deleted 2026-09-26)) | `clock_word/age_3`: 1 + z = 2.6517 and 2.6514 in the two windows (k = 1.6517, 1.6514); `age_6`: 4.1500 and 4.1506 (k = 3.1500, 3.1506); k(6) / k(3) = 1.907 and 1.908, the register's 1.907 | DETECTOR (the detector's click lines: the birth ordinal against the tick, the inverse slope exact) | SEEN |

**The counts.** 14 rows: SEEN 10 (rows 1, 3, 4, 5, 6a, 8, 10, 11, 12, 13); NOT SEEN 1 (row 6b); NOT RENDERABLE 3 (rows 2, 7, 9). Every SEEN row reproduces the register's registered numbers exactly on the re-run at 20d3a45a; no reading moved.

**What the pictures contradict, stated without interpretation.** Row 6b:
the paper's row "Kepler's period, T(24) / T(12) = 2 on the plane ... D3:
1.997 in [1.82, 2.18] (DETECTOR)" is a ratio of two single recurrences of
open arcs; the picture of the clicks shows each probe crossing the centre
column twice in one direction and then leaving the GameBoard (`face:+y`
at 698, `face:-x` at 1239), with amplitudes 34 and 51 Links for the pins
12 and 24 and each recurrence outside its bracket. The register's D3
entry says the same in its table ("outside, outside, outside"; "1.997 is
consistent with the 1 / r form and not decisive"); the paper's sentence
carries the ratio without the escape. This goes to the Boss and the
reviewer; the paper is not edited here.

**The host cost.** One core per run, Python 3.14 (`.venv`, uv-installed),
the runner headless, no frames. The cheap worlds: the amplitude worlds
0.2 to 1.3 s each at N <= 512 (thirty-one worlds), 5 s at N = 2048, 10 s
at 4096, 21 s at 8192, 57 s at 16384 (four each); `slits_low` 4 s,
`slits_one` 1 s; the four lensing worlds 12 to 17 s; the orbit's four
worlds 9 to 18 s; `clock_word` 1.4 s each; `atoms/hydrogen_r12` 75 s
(369 MB of `events.jsonl`); `slits_huygens` 869 s (14.5 min; the register's own run took 1334 s), the one run beyond the minute, kept because the paper's row 2a rests on it. Not cheap and
stopped: `shell_clock/age_4` (row 7). Not run: series G2 (row 9). The
total of the completed runs about 25 min of one core; the
records about 12 GB on disk, kept outside the repository.

## Links

- The order and the record: record 929 of the day's log (the owner's word), the Boss's bounded order of 2026-09-22.
- [docs/EXPERIMENTS.md](../../EXPERIMENTS.md): the register's entries L, D3, K, T, X, G2, whose pins and readings the table quotes.
- [docs/ENGINE.md, the detector's readings by type](../../ENGINE.md#the-output): the kinds.
- [docs/NATURE.md](../../NATURE.md): the rows the paper's Table `tab:nature` carries.
- The atom's baseline: `docs/designs/atom_baseline/RUN.md` on the branch `atom-baseline-run` at 01e86183.

> The scripts of this folder (`clock_reading.py`, `common.py`, `fig_atom.py`, `fig_bell_cells.py`, `fig_bending.py`, `fig_clock_form.py`, `fig_clock_k.py`, `fig_far_pair.py`, `fig_ghz.py`, `fig_mach_zehnder.py`, `fig_malus.py`, `fig_one_slit.py`, `fig_orbit.py`, `fig_two_slits.py`, `gathers.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/visual_check/<script>`).
