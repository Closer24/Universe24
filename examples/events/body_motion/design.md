# A bound body pushed along x

A world of the matter family alone, read on the lattice through its look page, `body_motion.html`. The page steps nothing: every number on it is an integer the engine wrote, recorded interval by interval and embedded in the page. Open the page, press the start button, drag the slider. The page needs no server and reads no external resource; it is set in the system fonts, and its record is gzip-compressed and inflated in the page.

## The world

A board of 61 x 17 x 17 Nodes, every face open, 200 intervals, on the shipped universe `examples/events/rule.json` (Gamma = 6,000, T = 32,768, G = 16; gravity [6000, 6000] held at the level weight 1,000 with the rest 60, the second content holder [2400, 2401] at 1, matter [4000, 6000]) with `examples/events/engine_start.json`. The body is the generator's pixel of `examples/events/matter_alone/pixel.json`, the standing record of `pixel.mode.json` (10,007 quanta declared on 1,965 Nodes), cropped to 17 x 17 in y and z with every one of its 1,965 Nodes kept, and laid at x = 14 with a velocity: `now` is the record times cos(k x'), k = pi / 8 along +x; `before` is the same with the envelope shifted back by v and the phase advanced by omega, both from the band at the body's own reaches (R / w weighted by the record squared, 0.1876). On this board the lay is rescaled by 1.06 percent to pass the body gate. The wells are laid by the engine's own start (`Lattice.start`). After the start nothing acts but Rule3 with the held writes on: no NodeDetector, no click, no blind row; every reading is a lattice reading.

## What one sees

The top strip is the record's level on the mid-plane z = 8, red positive and blue negative: the level at the centre column of the mid-plane changes sign 52 times in 200 intervals (a level exactly 0 counted as a sign of its own), once every 3.85 intervals, the half period of its rest rotation, about 7.7 (2 pi / omega_0 = 7.69 at the mode's clock pair), while it slides to the right. The second strip is the content every family reads, the vacuum content 61 light and the well dark: the well moves with the body. The bars are the share per x-layer read at the paces, the marker the centroid the band predicts. The traces: the centroid against the band's straight line; the level at the centroid, the rotation; the rms radius; the share read at the paces.

## The one fact

The centroid moves 13.93 -> 32.89 Links in 200 intervals, a speed of 0.0948 Links per interval against the band's 0.0968, 2.0 percent under it; at most one quantum stands beyond a sphere of radius 9 about the centroid at any interval (two intervals show one); the share read at the paces stays within 10,334 and 10,747; the rms radius goes 4.61 -> 4.03.

The same body on the wider board, 61 x 25 x 25, the run of `run_moving.py` whose rows are `results.json`: the centroid 13.93 -> 32.96, the speed 0.0952 against the band's 0.0968, 1.6 percent under it; no quantum beyond radius 9 at any interval; the share read at the paces within 10,258 and 10,698; the content at the centroid 396 -> 481; its gate rescale 1.9 percent. The two runs are two boards and are not one set of numbers.

## What a reader must not conclude

- Nothing about nature's numbers: Gamma = 6,000 and T = 32,768 are this universe's, the body is 4.6 Links wide, and the speeds are lattice speeds.
- The velocity was put in by hand at the lay; only the motion after the start is the rule's.
- The bars and the trace are the share read at the paces and not the count: the count is read once per period on the record's own clock (ALGEBRA.md, The count is the record's form over its period), and the share moves with the paces as the well moves.
- The breathing of the laid body, the rms radius falling and the content at the centroid rising, is the lay's and the writes', not a decay.
- The page steps nothing; the engine's run stands in the scripts beside it.

## Files

- `body_motion.html`: the look page with the 61 x 17 x 17 run embedded, 571,107 bytes, the record gzip-compressed and inflated in the page; `build_page.py` builds it from the run's record.
- `run_viz.py`: the page's run, `run_viz.py 200`, the pushed body on 61 x 17 x 17 with the mid-plane slices recorded every interval.
- `run_moving.py`: the pushed body against the body at rest on 61 x 25 x 25, `run_moving.py 200`, the aggregate rows of `results.json`.
- Both scripts import the engine from `src/event_universe` with the repository root found from their own path, write their world files (`viz_*.json` with their mode files) and their records under `runs/body_motion/` at the repository root, and need the engine's start, about two and a half minutes for this world.

## Provenance

The page's run is reproduced bit for bit on main at 2c81ba66f: `run_viz.py 200` re-run with `tools/look/record.py`'s `Lattice`, the shipped `rule.json`, `engine_start.json` and `matter_alone/pixel.mode.json`; every row (the centroid, the share, the rms radius, the shed count) and every slice (the levels, the content, the share per layer) differs by 0 from the page's embedded data; the gate refused 10,223 against 10,007 and passed after the rescale by 0.9894. The hands' reading of 2026-10-16: the numbers of "The one fact" are the page's own for the page's board and `results.json`'s for the 61 x 25 x 25 board. The page is 571,107 bytes.
