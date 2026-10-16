# Two bodies at rest fall together

A world of the matter family alone, read on the lattice through its look page, `two_bodies.html`. The page steps nothing: every number on it is an integer the engine wrote, recorded every third interval and embedded in the page. Open the page, press the start button, drag the slider. The page needs no server and reads no external resource; it is set in the system fonts, and its record is gzip-compressed and inflated in the page.

## The world

A board of 49 x 17 x 17 Nodes, every face open, 900 intervals, on the shipped universe `examples/events/rule.json` (Gamma = 6,000, T = 32,768, G = 16; gravity [6000, 6000] held at the level weight 1,000 with the rest 60, the second content holder [2400, 2401] at 1, matter [4000, 6000]) with `examples/events/engine_start.json`. Two copies of the same pixel of `examples/events/matter_alone/pixel.json`, the standing record of `pixel.mode.json` cropped alike at eight Links about its centre, are laid at rest at x = 12 and x = 36, 24 Links apart, each its own record of the matter family, nothing laid but the lay; the wells are laid by the engine's own start (`Lattice.start`). The control is the same body alone at x = 12 on the same board, 300 intervals, its centroid the dashed trace. No NodeDetector, no click, no blind row; every reading is a lattice reading.

## What one sees

The two records flip sign each in its own rotation; the content strip, the vacuum content 62 light and the wells dark, shows the two wells and the bridge between them. For about 300 intervals little moves; then the records fall toward each other, their distance falling under a third of its start at the interval 578, the meeting, and, from the interval 620, one record in one written well cut at x = 24 into the two halves the page reads, breathing: the mid-plane content reaches 1,385 against 367 at the start, the two half-centroids 3.2 to 6.3 Links apart (3.2 to 8.0 from the meeting at 578), the smallest distance 3.16 at 838, the rms radius of A's half 3.0 to 5.1 from 620, and the shares read at the paces 9,188 and 12,195 for the two halves at the end. The separation trace shows the fall; the trace of A's centroid against the dashed control parts the mutual pull from the push of the near face (the Node beside an open face reads 0).

## The one fact

Two laid records of one family move toward each other under Rule3 with no velocity declared and fall into one written well, where they breathe as one record: the separation 24.0 (0) -> 21.3 (300) -> 14.3 (500) -> 5.7 (600) -> 3.4 (640); the accelerations at the start, by a quadratic fit over the intervals 0 to 300, A +3.72e-5 and B -3.79e-5 Links per interval squared, the alone control +1.14e-5 (the wall's push), A less the control +2.57e-5, the mutual share.

The run is mirror-exact to the bit under x -> 48 - x at every interval to 900, on every line of every family (the levels now and before, the remainders and the writes' remainders): the cube's symmetry theorem (ALGEBRA.md, The cube's symmetry) holds on a 10,000-quantum lay with the held writes on. The readout n_B - n_A (5 at the interval 275, 24 at 300, 358 at 500, 3,861 at 600, 8,339 at 650) is the middle layer x = 24, counted with B by the scripts' split of the board into the halves [0, 24) and [24, 49), and is no asymmetry; it is first nonzero at the interval 89, when the tails reach the middle layer.

The fall's coefficient is measured on the engine in a hand-held linear ramp (`ramp_pass.py`, its record `ramp_pass.json`): the bound body falls at 0.96 to 1.06 of the law's coefficient 2 (1 - nu) N^2 (R / w) / sin^2 omega_0 over 120 intervals at two slopes (the shorter windows wobbling with the breathing between 0.19 and 0.39 of it), a free packet at 0.99 to 1.01 of it; the coefficient is the band's (ALGEBRA.md, The band at a pace; the free packet's fall a / g = (1 - eps) / (3 (1 - eps / 2)), 0.2667 at [4000, 6000], row (i) of the rows against nature; Newton's 0.2667 grad U at [2, 3], (d) of what a body is), and the law's The three masses of a body, row (u), gives the cloud's 0.92 to 0.98 of it, the comparison. The "1.8" read from this run by a quadratic fit over 300 intervals is a wobbling centroid in a growing field, 0.93 of the law's coefficient over the intervals 0 to 50, and is no coefficient.

The share read at the paces: the per-period mean of the total 20,463 -> 20,743 from the start to the interval 290, 1.4 percent up; the one-interval reading 23,109 at the interval 647 is not a count.

## What a reader must not conclude

- Nothing about nature's numbers: Gamma = 6,000 and T = 32,768 are this universe's, each body is 4.6 Links wide, and the accelerations are lattice accelerations.
- The share is not a count: the count is read once per period on the record's own clock (ALGEBRA.md, The count is the record's form over its period), and the share moves with the paces as the well deepens; the law says a body's count falls in a well, and whether the reading at the paces agrees with the count per period is open.
- No static two-body solution is claimed, and the law has none to compare; the two "bodies" from the interval 620 are the two halves of one symmetric record cut at x = 24, and the distance of their two half-centroids, 3.2 to 6.3 Links from 620 (3.2 to 8.0 from the meeting at 578) with the smallest 3.16 at 838, is the cut's reading; the two shares read at the paces, 9,188 and 12,195 at the end, are the cut's two pieces of one share.
- The accelerations are exactly mirror; the 2 percent between A's and B's is the layer x = 24 in B's centroid.
- The page steps nothing; the engine's run stands in the scripts beside it.

## Files

- `two_bodies.html`: the look page with the 900-interval run embedded, every third interval, 655,009 bytes, the record gzip-compressed and inflated in the page; `build_page.py` builds it from the run's record.
- `run_fall_long.py`: the page's run, `run_fall_long.py 900 49 17`, the two bodies to 900 intervals with the mid-plane slices every third interval.
- `run_fall2.py`: the two bodies and the alone control to 300 intervals, `run_fall2.py 300 49 17`, the rows of `fall_results_49x17.json`; the page's first 301 rows equal its pair rows and the control equals its alone rows.
- `gradient_check.py`, `wall_check.py`, `tension_check.py`: the force against the content gradient, the same on the wall's field, and the Link tensions, at the start (`gradient_check.json`, `wall_check.json`, `tension_check.json`); they read the world files `fall_pair_49x17.json` and `fall_alone_49x17.json` that `run_fall2.py` writes under `runs/two_bodies/`; `wall_check.py` carries the measured accelerations as literals and `gradient_check.py` the mode's clock pair 1646 / 1202.
- `ramp_pass.py`, its record `ramp_pass.json`: the ramp pass, the pixel and a free rotating packet in a linear content ramp held on gravity's time line, the body's own well free, 120 intervals, the body at the board's centre so the walls' pushes cancel; the coefficients of "The one fact".
- All scripts import the engine from `src/event_universe` with the repository root found from their own path, write their world files (`fall_*.json` with their mode files) and their records under `runs/two_bodies/` at the repository root, and need the engine's start, about two and a half minutes for this world.

## Provenance

The page's run is reproduced bit for bit on main at 2c81ba66f: `run_fall_long.py 900 49 17` re-run with `tools/look/record.py`'s `Lattice`, the shipped `rule.json`, `engine_start.json` and `matter_alone/pixel.mode.json`; every row and every slice differs by 0 from the page's embedded data. The hands' reading of 2026-10-16 on the same engine: the mirror test on every line of every family to 900 intervals, 0 unequal entries at every interval; the ramp pass (the ramp on gravity's time line held, the body's own well free, 120 intervals, the body at the board's centre so the walls' pushes cancel) giving the coefficients above; the count per period from the 300-interval rows. The page is 655,009 bytes.
