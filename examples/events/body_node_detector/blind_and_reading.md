# The two-level body's one-Node detector: the blind and the reading

Line 1 of the generic emitter/detector (ALGEBRA.md, The emitter/detector is one declaration kind for
every experiment; the mathematician's 235, #1572 comment 5966769056, with the advisor's seconds,
5966657866 and 5966780505, two hands): a detector of one Node on a bound body of two levels reads the
Node's level sequence over its window and solves exactly for the four quadrature amplitudes of the
reference sequences at omega_g and omega_e through their Gram matrix by Cramer's rule, the determinants
integers of Python's, and draws once at the window's close by the levels' shares Q_n = (a_n^2 + b_n^2)
sin^2(omega_n) / weight_n, p_n = Q_n / SUM Q (`src/event_universe/body_node.py`, `credit.read_levels`).
The toy body: a periodic chain of 48 Nodes of one family of quanta at the pair [5, 6] reading no holder
(`two_levels.json`), the level g the wave at k = pi / 3 and the level e the wave at k = 2 pi / 3, each a
message over the whole chain with no envelope, so that every Node carries both rotations in time,
cos omega_g = 25 / 36 and cos omega_e = 5 / 12 by the chain's band at the vacuum's paces,
cos omega = (num / den) (2 + cos k) / 3, the amplitudes 300 and 540; the detector `reader` on the Node
12 declares the two levels by their labels, pairs and weights at the Node (1 / 48 each), the world's
instrument the window 32 at the seed 24, 100 windows over 3200 intervals. The blind `expectation.json`
was written by `build_world.py` from `design.json` before any lay and never touched after; the readings
are `read_world.py`'s, the clicks labelled DETECTOR and the solve on the arrays labelled GAMEBOARD; a
miss is a finding by name and never an adjustment of the blind.

## The blind (expectation.json), written before the run

1. The clicks: over the 100 windows the detector's credit lines name the level realised; p_e =
   Q_e / (Q_g + Q_e) with Q_n = a_n^2 sin^2(omega_n) / weight_n, sin^2(omega_g) = 671 / 1296 and
   sin^2(omega_e) = 119 / 144, so p_e = 0.8380 (the amplitudes chosen so that the number is the
   mathematician's own for his 21-Node well, 0.8378): 83.8 +/- 3.7 of the 100 windows realise e and
   16.2 +/- 3.7 realise g.
2. The window: 2 pi / (omega_e - omega_g) = 2 pi / 0.3371 = 18.6 intervals, so the window 18 is refused
   at the loader by name, "the window does not resolve the beat", and 32 resolves it.
3. The clocks: the detector's proper time equals the board's tick at every close (the family reads no
   holder, p_0 = Gamma) and the window index counts the closes 1, 2, 3, ...; the count moved is 0 (the
   body's record stands, its re-lay in the realised level by name).
4. The reference check, a GameBoard reading: the solve on the first window's level sequence at the Node
   reads p_e within 0.002 of the blind, as 235 reads 0.838 flat at W = 32 for his well.

## The reading (branch body-node-detector, 2026-10-03, about 09:20 UTC)

`PYTHONPATH=src python examples/events/body_node_detector/read_world.py --seeds 24 25 26 27`:

1. The clicks at the seed 24: e 80, g 20 of 100 windows (DETECTOR), against 83.8 +/- 3.7: within 1.1
   deviations, PASS; at the seeds 25, 26 and 27: e 78, 86 and 78.
2. The window: `two_level_body.json` with the window 18 is refused at load by name, "detector 'reader':
   the window does not resolve the beat of the levels 'g' at [25, 36] and 'e' at [5, 12] within 18
   intervals" (the test asserts it); at 32 the world runs LAWFUL over 3200 intervals. PASS.
3. The clocks: `proper` equals `tick` on every one of the 100 credit lines, `windows` 1 to 100, `count`
   0, `left` 452 (the record's count, unmoved), no Node in any line. PASS.
4. The reference check (GAMEBOARD): the solve's p_e over the 100 windows reads 0.8263 to 0.8354, the
   mean 0.8321, against the blind 0.8380 within 0.002: a MISS by 0.006, a FINDING by name of the lay and
   not of the solve: the generator lays each wave at its declared amplitude with its level one interval
   earlier rounded to integers, and the integer step's rounding walk (about 0.16 levels per Node per
   interval) moves the levels at the Node by a few units per window, so the ratio of the two amplitudes
   squared read at the Node is the lay's within about 4 percent (the exact solve on the exact
   combination of the references returns the amplitudes exactly, the test's first assertion); the
   clicks follow the solve's number, 83.2 expected from the read shares, and the blind's 83.8 within it.

## The findings by name

- The advisor's toy at [2, 3] against [1, 3] was tried first and replaced: two messages at those
  rotations stand only on the massless pair [1, 1] (the band gives cos omega_g = 2 / 3 at k = pi / 2 and
  cos omega_e = 1 / 3 at k = pi for no other pair), whose uniform mode is a repeated root of the line
  and collects the rounding's walk linearly, the levels at a Node wandering by hundreds over 3200
  intervals (the g wave alone 300 to 799 in its largest level, the e wave alone 539 to 1074, the books'
  share drifting 2 percent), the solve's p_e then swinging 0.71 to 0.96 window by window; at the pair
  [5, 6] the levels stand and the solve reads 0.826 to 0.835.
- The levels' pairs and weights are declared on the detector (`levels`) by name: the body's mode file
  holds one laid mode and no second, and the engine reads no mode of a well at the start, so neither
  the hands' "the start's own readings" nor a mode file's frequencies had a file to come from; the
  declaration is the file's and the engine holds no number.
- The draw writes nothing on the GameBoard: the record stands after the click, its re-lay in the
  realised level (the body's collapse to one mode) by name, not built.
- The one-Node detector reads the record's first line at its Node (light the sum of its rows); a plane's
  second line is not read.
