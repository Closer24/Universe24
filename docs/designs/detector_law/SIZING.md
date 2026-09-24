# Sizing every GO world by the algebra (2026-09-24, 10:50Z, the model owner's order of 10:33Z, record 1793)

The owner's question: why are the GO worlds so large; by the algebra, how
large must each be. This page sizes every world of the GO list
(RUN_LIST.md) from its pin and its band alone. Every number is labelled by
kind: DECLARATION (a value in DECLARATIONS.md or a world file), COMPUTATION
(derived here from the declared integers), HOST (a cost). No pin moves on
this page; a world that shrinks is a NEW declaration whose pin is
re-derived from the new geometry alone, blind of every preliminary reading
(Reviewer 3 confirms that no reading enters), and the World Generator
regenerates its file from the line here. Nothing runs by this page.

## The three rules used

1. THE RECORD COUNT (column c). A reading is one of three kinds. A
   first-rung interval per record (sagnac, the light clock, M2): the rise
   is deterministic on the rule, so one record reads the pin and the
   records beyond it are controls of the spread; five hold records per
   direction are taken as the minimum where a mean is read, three where
   one record is the pin. A ratio of click intervals (redshift, 4a, the
   boxes, the deep well): the mean interval over a span S of intervals has
   the grain 1 / S, so the band b needs S > 1 / b; the band 0.3 percent
   needs S > 333, and a hold of 1000 gives the grain 0.1 percent, a third
   of the band. A click count per cell (Bell, Malus, two slits, M1): under
   the counting form (DESIGN.md section 5, the cell of u on the ladder)
   the clicks are NOT Poisson. A lamp with a stride wheel [1, W] and a fixed
   world births identical records (the rule is linear, every record has
   its own rows, the bodies are fixed), so every record's ladder is the
   same and the cell of u repeats after W births: a stock of k W records
   gives exactly k times the counts of one wheel. The minimal stock is
   ONE WHEEL, and the band is the ladder's grain (one rung, 1 / W of the
   record per cell), not a Poisson error. THE WHEEL IS SIZED TO THE BAND
   (corrected 11:20Z, on the Preliminary Runner's two_slits reading of
   10:45Z, 1024 records with the wheel [1, 64] choosing one cell 16 times
   over): a count row's band b needs the grain 1 / W below b, so W is the
   stock and the stock is W, each u once: two_slits W = 1024 (the dark
   fringe about 2 percent of the screen's total, 20 counts of 1024, the
   visibility's grain 0.002 against the band 0.02), M1 W = 2048 (the
   lobe's centroid at the grain of one count in 610, a tenth of a Node).
   The stocks declared for 2a and M1 were therefore the right size by a
   wrong statistic; what was wrong is the wheel of 64 beside them, which
   repeats one coarse pattern 16 and 32 times. Their HOST does not
   shrink; their reading becomes exact. A lamp under `residue_order`
   "seed" (Bell) draws one permutation of 0 .. W - 1 per world, again each
   u once: one wheel, the counts exact. THIS IS A FINDING of this page for
   Reviewer 3's read: rows 2a and M1 declared Poisson bands (0.02 over
   about 1000 clicks; the sd 0.23 over 610 clicks) that this engine does
   not produce; their bands are re-derived as the ladder's grain on the
   same geometry, a blind computation, before their pin runs.
2. THE BOARD (column d). A chain needs the pin's geometry (the gap, the
   distance to the detector), the bodies' travel over the run, and, per
   record, room for that record's own backward and forward shares so that
   their reflections from the faces return after the record's own rung
   (a record's rung is on its own pointer; other records' reflections do
   not enter it): a face at d Links returns a share after 2 d / c = 3.46 d
   intervals, so a rung within 250 of the birth needs d > 73, taken 100.
   A layer needs the pin's geometry (the slits' d and L, the fan's 40
   Links) plus the sponge; the layer lemma of section 7 fixes nothing
   about the size beyond that. Where a size is set by a bound mode's
   extent (4a's 200 x 200, the boxes, the deep well) it is not re-derived
   here and is said so.
3. THE TICKS (column e). The ramp (section 8: at least ten relaxation
   times of the block's own well), the hold or the births' span, the
   transit to the farthest reading, the last record's line, one named
   margin. Under the click line at the rung (the owner's word of 09:50Z,
   section 13 item 7) no world waits for a record's close, which is what
   the largest tick counts were set for.

THE HOST RATE (column h): the Preliminary Runner's in-process rate on
ENGINE C 540456da, one core: 640 intervals a minute on a 128 x 128 layer
with about 50 live records (0.094 s per interval); the Bell bar of 21
with up to 3200 live arms 0.21 s per interval; sagnac_k3 on the chain of
3000 with about 70 live records 0.046 s; the light clock on 673 with
about 20 live 0.003 s. One model fits them within a factor 2: the time
per interval is L x (6e-5 s + 1.1e-7 s x Nodes), L the live records.
Block-only worlds (no light records) are costed at their measured rates:
the 64^3 box 0.24 s per interval (the builder's runs), the 200^2 layer
13.6 ms (section 8), the 128^2 deep well about 19 ms (3 minutes over
9500). Every HOST number is that model or that rate, one core.

## The table

Columns: (a) the pin and its band (DECLARATION); (b) the reading's kind
and statistic; (c) the minimal record count; (d) the minimal board; (e)
the minimal ticks; (f) the declared values (records / board / ticks); (g)
the ratio declared / minimal on records, board, ticks; (h) HOST at the
declared size and at the minimal size (one core).

| World | (a) pin, band | (b) reading, statistic | (c) records min | (d) board min | (e) ticks min | (f) declared | (g) ratios | (h) HOST declared / minimal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sagnac_k3 | 247 and 72, +- 2 each (first rungs at at_b and at_a); the ratio 0.5774 +- 0.01 beside | first-rung interval per hold record, DETECTOR; the mean over the hold's records by birth | 5 per direction | chain 800 (the gap 60; 100 beyond each block; the travel 417) | 1050 (ramp 200, hold 500, the last rung 250, margin 100) | 31 per direction / 3000 / 6400 | 6 / 3.8 / 6.1 | 4.9 min / 2 s |
| sagnac_rest | 108 +- 2 | the same, at rest | 5 per direction | chain 300 | 560 (5 cycles of 70, the rung 108, margin 100) | 43 per direction / 3000 / 8450 | 8.6 / 10 / 15 | 4.3 min / 1 s |
| light_clock_60 | 213 +- 1 at W = 64 (section 10 item 9, 09:55Z) | the first cycle's record's first rung at the set, DETECTOR; the later cycles beside | 3 (the pin's record and two later cycles) | chain 173 (A at [100, 112), the set 112, the mirror 172; the -x face 100 from A: its half returns at 346, after the rung; THE PIN ON THIS CHAIN by the same map, `light_clock_60_receiver_173.py` and `.out` beside this page, run 2026-09-24 12:05Z before the World Generator regenerates the file: the first rung at 213 at W = 64, 211 at 256, 209 at 1024, the no-take control 213, the -x return 346, the same integers as the 673 chain's; the builder's (ac) test on this chain in section 10 item 10 is an ENGINE reading, not the pin's provenance) | 460 (the first rung at 267, the third cycle's at 407, margin 50) | 37 / 673 / 2600 | 12 / 3.9 / 5.7 | 8 s / 0.3 s |
| redshift_k3 | 1 + z = 1.9889, the band 0.3 percent | f_B over the hold's clicks, a ratio of differences, DETECTOR; the grain 1 / span | 13 hold clicks (a hold of 1000; the grain 0.1 percent) | chain 1420 (the block from 1217 receding 1117 Links by the run's end, the detector 200 Links beyond its start, a margin 100) | 4000 (ramp 1500 as section 8 keeps it, hold 1000, the last hold record's transit 1356 plus its rung and margin) | 38 / 4096 / 9600 | 2.9 / 2.9 / 2.4 | 3.3 min / 9 s |
| redshift_control | the control's f_B (the ratio's denominator) | the same at rest | 13 | chain 1420 (the pair alike) | 4000 (the pair alike; 1450 would do at rest) | 38 / 4096 / 9600 | 2.9 / 2.9 / 2.4 | 3.3 min / 9 s |
| bell_a0b0, a0b1, a1b0, a1b1 | S = 181 / 64 exactly at N = 2048 (the finite-N value, W = N); the band the ladder's grain 1 / 2048 | the joint cells' counts per setting, DETECTOR; S from the four correlations; the seed permutation gives each u once, the counts exact | 2048 (one wheel; the pin's own N) | the bar of 21 (the tables at 3 and 7 Links, the sponges) | 5500 (2048 births, the train 3200, the close 250) | 2048 / 21 / 5500 | 1 / 1 / 1 | 19 min each / 19 min (the train is the cost: 128 periods, DESIGN.md 6.2's coherence line; a 16-period train would read 1.5 min, a re-derivation of that line, not made here) |
| malus_45, 11.25, 28.125, 33.75 | 128, 246, 199, 177 of 256 (cos^2 s x 256), the band one count (the wheel [159, 256] a permutation, exact) | the + cell's count, DETECTOR | 256 (one wheel) | the bar of 9 (section 14 item 6) | 1200 (256 births, the train 800, margin) | 256 / 7 to 9 / 1200 | 1 / 1 / 1 | seconds / seconds |
| two_slits | the visibility of the CLICK COUNTS 0.96 at 32 periods, the band +- 0.02 (the map's count visibility 0.961 on the world's own geometry, `two_slits_1024.py` and `.out`, blind, 2026-09-24 12:10Z; 6.2's 0.959 is the offer's on the pilot's scaled board; the falsifier 0.93 unchanged); THE WORLD RE-DECLARED (section 15 L-3, the second draft): 6.2's own two-slit geometry, d = 26, L = 113, the openings of WIDTH 3, on a 160 x 256 layer with x and y OPEN (the faces sponges), the lamp at [20, 128], the screen's 201 sets over y in [28, 228] (one per Node, the ladder), the window y in [40, 216]. WHY (the map, the first draft's geometry): the width-1 openings scatter into the lattice's short-wavelength modes, a floor of 9 percent of the centre at the dark pixels (the visibility 0.81 on 6.2's own boundary form), and the y-periodic layer folds the openings' images onto the screen (0.39): the first draft's 0.959 was 6.2's number on 6.2's geometry, not the world's. The band: the grain 0.019 (one count moved) and the faces' residual reflection; the map's crude sponge form reads 0.79, the engine's open face reflects less (sagnac: 0.4 to 3.5 percent of the absorbed), read at the preliminary as GAMEBOARD; if it costs more than the band the layer is regenerated taller before the pin run, the pin unmoved. THE CRITERION OF THAT CONTINGENCY, NAMED (Reviewer 3's lines of 16:15Z and 14:45Z): the pin's 0.9608 is the map's margin form, nothing returning from the y ends, while the world is y open with the face as the sponge; the reading that decides it is the y faces' RETURNED SHARE at the preliminary, PER FACE: the cells `face:-y` and `face:+y` of the run's books (the `cells` entries of state.json, the take booked at each face over the run; NOT `sunk`, which sums every sink and is 97 percent the x face behind the lamp), each face's take against the ideal sponge's take of the map at that face (the map's margin form absorbs the whole arriving amplitude; the engine's open face reflects a share of it, read on sagnac as 0.4 to 3.5 percent), the returned share = 1 - (the face's take / the map's take at that face); THE THRESHOLD, declared before the run: a returned share above 4 percent at either y face (the band's 0.02 on the visibility at the dark pixels' 9 percent floor) regenerates the layer taller; below it the layer stands; GAMEBOARD, never the screen's visibility, which is the pin's own statistic and decides nothing before the pin run | THE COUNTS' VISIBILITY: the screen's clicks per Node, DETECTOR; the MEAN count per pixel over the two-source cosine's bright pixels (19) and over its dark pixels (10) of the window, (B - D) / (B + D) on the two means (6.2's statistic; L-3's first draft summed the counts, which on unequal pixel numbers reads 0.98 for the same pattern, withdrawn); the pixels listed in the .out. THE SCREEN IS THE LADDER: the faces and the mirror line SINKS (the record's 97 percent to the escaped row at its close), the 201 sets the ladder, each with its own rung wheel 2^20 (the dimmest cell a u chooses holds 1.8e-4 of the screen, 5.5e-6 of the norm at the screen's 3 percent; the wheel must exceed 1.8e5, with a margin of 4: 2^20; the first draft's 65536 withdrawn, Reviewer 3's line (c)); THE TWO BUILDS the row needs, named: a lamp record's ladder by name (build-4's key `receiver` is on emitting blocks; the lamp's ladder is its sets less the declared sinks) and the cell of u taken over the LADDER'S OWN SUM (`cell_of` divides by the record's whole `absorbed`, amplitude.py 275 to 293; with 97 percent in the sinks every u above 0.03 W would find no cell); BOTH BUILDS ARE ON MAIN (the lamp's ladder by name and the cell over the ladder's sum, 567cd1b7) | 1024 = one wheel [1, 1024] (the same stock as declared, each u once) | the 160 x 256 layer (x and y open): d = 26, L = 113, the openings of width 3 at y = 115 and 141, the screen at x = 153 | 5500 (1024 births at one per 4, the last birth 4096, the train 665, the transit 231 to the farthest set, the close of the last record within about 500 of its train's end, the margin 100; Reviewer 3's 5010 on the first draft's transit) | 1024 / 128^2 / 17300 | 1 / 2.5 / 3.1 | 94 min / 94 min (the stock times a record's life of about 1200 intervals on 40960 Nodes at 4.6 ms per record-interval; the taller layer's cost) |
| pace_fan_12, 16, 24 | the phase pace by direction, 0.8 / 0.4 / 0.2 percent on the axis, a quarter on the diagonal (GAMEBOARD); the band the reader's spread (L-6, 10:15Z) | the two probes' phase difference per ray, GAMEBOARD, read at every period after the front from the second to the train's end and printed as a series; THE READING OF RECORD is the settled value: the first period after which the eight rays' values change by less than 0.05 percent between consecutive periods (the World Generator's rerun without rings, 10:55Z: at two periods the eight rays spread 2.3 percent, the front's own transient; at four 0.32 percent, the axes settled at 0.5268 and the diagonals still moving at 0.5260; the criterion, not a chosen period, is the declaration) | 1 | the 128 x 128 layer (the probes at 40 Links plus the sponge; 96 x 96 would do) | 830 / 1110 / 1500 (the train of 32 periods, the train's end past the inner probe, margin 100: the settling may need many periods, so the window runs to the train's end) | 1 / 128^2 / 1000, 1400, 1900 | 1 / 1.8 / 1.2 | seconds / seconds |
| layer_pin_rest_14, layer_pin_k3_14 (4a) | f / f_0 = 0.8116, the band 0.3 percent | the block's clicks' mean interval over the hold, at k = 3 over the rest's | 24 clicks at k = 3 (a hold of 1000), 28 at rest (1200) | the 200 x 200 layer: set by the shallow well's mode extent (section 8, eps 0.013), NOT re-derived here | k = 3: 13100 (ramp 12000 by section 8's rule since body-check, ten relaxation times by the margin module's own number, hold 1000, margin; 11100 on the ramp 10000 HISTORY); rest 1200 | 150 clicks / 200^2 / 20500; rest 80 / 200^2 / 20500 (both 18500 and 3500 HISTORY, M1-8) | 6 / 1 / 1.7; rest 2.9 / 1 / 2.9 | 4.2 min / 2.5 min; rest 0.8 / 0.3 min |
| cart_k3 (4c) | (1 + beta) / (1 - beta) = 3.732 | the cart's received line over the sent (a frequency ratio) | as built (the lamps' 8192 records are 128 wheels of [1, 64]; the ratio needs one) | 240 x 3 x 3 as built | 600 as built | 8192 x 2 / 240 x 3 x 3 / 600 | 128 / 1 / 1 | seconds / seconds |
| three_openings_{abc,ab,ac,bc,a,b,c} (2c; the one list, the owner's word of 11:29Z) | the Sorkin sum of the CLICK COUNTS per Node over the seven worlds, |S| at most 13 on every cell of the 201 and the bright pixels' mean count 8 (the map on the declared world's geometry, `two_slits_1024.py`: the seven count patterns of one wheel each, each normalised to its own ladder, so the sum over all cells is 1024 by construction and the statement is per cell); the theorem the row's statement (the click a quadratic form, the exponent 2 exactly; the offers' Sorkin sum 0 to the remainders' grain, 3.9e-2 of the centre on the map, GAMEBOARD when run) | the seven screens' clicks per Node, DETECTOR; S per Node = N_abc - N_ab - N_ac - N_bc + N_a + N_b + N_c; the same ladder, sinks and builds as two_slits | 1024 per world = one wheel each | two_slits' layer with the openings a, b, c at y = 115, 128, 141 (width 3), the unnamed openings closed | 5500 each | none declared | new | 7 x 94 min (the seven worlds; the rows cost is the stock's, not the cadence's) |
| one_opening_near (10 (a); the one list) | w x FWHM / lambda = 0.842, the band 0.03 (DESIGN.md 6.1, the wave's own sum through an opening in a mirror at w = 2 lambda, F = 0.16; a COMPUTATION check, PINS.md row 10) | the screen's clicks per Node, DETECTOR, summed in bins of 8 Nodes declared before the run; the half-maximum crossings of the binned counts by linear interpolation, FWHM in sin theta; at W = 1024 the peak bin holds about 30 counts, the crossing's grain about a Node in a width of about 240, 0.5 percent of the pin, inside the band; the same ladder, sinks and builds as two_slits | 1024 = one wheel | 6.1's scaled board: w = 23 Nodes at L = 275, the screen 895 tall, 522 x 895 (x and y open) | 17400 (1024 births at one per 16 to keep about 80 records live, the train 665, the transit 500, margin) | none | new | 18 hours (1024 records of about 1240 intervals on 467k Nodes at 51 ms per record-interval): the costliest row of the list; at W = 256 (the crossing's grain 4 Nodes, 2 percent) 4.5 hours, the owner's choice |
| one_opening_far (10 (b); the one list) | 0.886 (Fraunhofer's sinc), the band 0.03 (PINS.md row 10; F = 0.16 at w = 8 lambda needs L = 4800 Links) | as 10 (a) | 1024 | at w = 96, L = 4800 the screen about 3000 tall: a 4830 x 3000 layer, 14.5 million Nodes | about 27000 | none | new | about 600 hours at W = 1024 (1.6 s per record-interval, records of about 10000 intervals): NOT RUNNABLE as declared; the row waits on a cheaper form (PINS.md row 10 (c), w = 4 lambda at L = 100 lambda: 1230 x 900, 1.1 million Nodes, 97 hours at 1024, 24 at 256), the owner's word |
| two_slits at the 128-period train (2a's coherence line; the one list) | the counts' visibility 0.96 at 128 periods, the band +- 0.02 (the map on the declared world: 0.961 on the counts, 0.970 on the offer; L-3's 0.99 was 6.2's expectation, not computed there); the rule adds no loss below the train's coherence (the 32-period and the 128-period counts agree within the grain) | as two_slits | 1024 | two_slits' layer | 7500 (4096 births, the train 2660, the transit 231, the close, margin) | none | new | 6 hours (records of about 3200 intervals): the train is the cost |
| matter_front_12 (M2) | 169 +- 2 at W = 64 | the first click's interval from the birth, DETECTOR | 1 | the chain of 200 (the set at 84 Links) | 420 (the rung 169, the train 150, margin 100) | 1 / 200 / 600 | 1 / 1 / 1.4 | seconds / seconds |
| matter_waves_12 (M1; the file not yet written) | the side lobe's count centroid y = 64 + 27.4, the band one Node (the lattice map `matter_waves_2048.py` and `.out` on the declared layer itself, y periodic, with the matter kind's rule and the 8-period train, blind, 2026-09-24 12:10Z: 27.43 on the counts, 27.41 on the offer; the two-source formula's 27.79 of `matter_wave_pins.py` beside, the statistic's earlier derivation, inside the band; the map's open-boundary forms 27.2 and 27.4, so the periodic layer's images move the lobe's centroid by less than 0.3 Node and the layer stays as declared, unlike two_slits whose visibility the images destroy); section 12's Poisson sd 0.23 was the wrong statistic: the count centroid's grain at W = 2048 is 0.016 Node (one wheel, each u once) | the screen's counts per Node, the side lobe's count centroid over y in [64 + 14, 64 + 40], DETECTOR; as for two_slits the take lines at x = 0 and 127 are SINKS outside the ladder and the screen's 121 sets are the ladder, each with its own rung wheel 65536, which HOLDS here (the dimmest cell a u chooses holds 3.2e-3 of the screen, 9.7e-5 of the norm at the light row's 3 percent; the matter world's own share read at its preliminary, GAMEBOARD; above 1e4 needed, 65536 the margin of 6); the same two builds as two_slits (the lamp's ladder by name, the cell over the ladder's sum) | 2048 = one wheel [1, 2048] (the same stock as declared, each u once) | the 128 x 128 layer (d = 32, L = 64, the openings of width 1, y periodic: as declared) | 4700 (2048 births at one per 2, the train 150, the transit 167, margin) | 2048 / 128^2 / 16700 | 1 / 1 / 3.6 | 30 min / 30 min (the stock times a record's life) |
| moving_20, moving_28 ((ii-a), (ii-b)) | 0.7814 and 0.8032, the band 0.3 percent | the block's clicks' mean interval at k = 3 over the rest's | 19 clicks (a hold of 1000 at the moving period about 52) | the 64^3 box: set by the well's mode extent, NOT re-derived here | 2600 (ramp 1500 as section 8 keeps it, hold 1000, margin 100) | 150 / 64^3 / 9500 | 8 / 1 / 3.7 | 38 min each / 10 min |
| rest_20, rest_28 | the rest clocks (the denominators) | the same at rest | 28 clicks (1200) | the 48^3 box, as above | 1200 | 70 / 48^3 / 3000 | 2.5 / 1 / 2.5 | 12 min each / 5 min |
| deep_well_k3_40, deep_well_rest_40 | 0.7531 (the cavity's control), the band 0.3 percent | the block's clicks' mean interval | 19 clicks at k = 3 (1000); 28 at rest (1200) | the 128 x 128 layer for s = 40: the well's extent, NOT re-derived here | k = 3: 2600 (ramp 1500, hold 1000, margin); rest 1200 | 150 / 128^2 / 9500; rest 80 / 128^2 / 3500 | 8 / 1 / 3.7; rest 2.9 / 1 / 2.9 | 3 min / 0.8 min; rest 1.1 / 0.4 min |
| index_moving_long_k3_away, its rest and reference worlds ((v-m)) | the lab phase +1.0144 rad, +- 0.04; the drift 1.2e-3 rad per interval, +- 10 percent (P, GAMEBOARD) | the probe's phase over the window [3800, 5400] against the reference, and its drift | 1 (one train, one block) | chain 3400 (the far end 1000 beyond the probe returns its reflection at 6230, after the window; the -x return at 5543 sets the window's end and stands) | 5500 (the window's end 5400, margin 100) | 1 / 4000 / 6000 | 1 / 1.2 / 1.1 | 2 min each / 1.5 min |

The totals, HOST on one core, the worlds one after another: DECLARED
about 260 minutes (Bell 76, the boxes and their rest worlds 100, M1 30,
two_slits 24, the sagnac and redshift chains 16, 4a 5, the deep well 4,
the index 6, the rest seconds); MINIMAL about 240 minutes with Bell's
train as declared (two_slits 94 on its re-declared 160 x 256 layer, Bell
76, M1 30, the boxes 30, the index 4.5, 4a 2.8, the deep well 1.2, the
chains under a minute), about 170 minutes if Bell's train is re-derived
to 16 periods. The count rows keep their cost: a click row's cost is its
wheel times a record's life on the board, and the wheel is the band's.
THE ONE LIST beyond the GO list (the owner's word of 11:29Z, one list of
all the experiments): 2c's seven worlds 11 hours, two_slits at the
128-period train 6 hours, 10 (a) 18 hours at W = 1024 (4.5 at 256), 10
(b) not runnable as declared (its rows below); 2b, the atom's lines and the
index at k = 4 wait on their builds and are not sized here.

## Which worlds are larger than their derivation needs, and why they were sized so

sagnac_k3 and sagnac_rest (6 to 15 times in ticks, 4 to 10 in board): the
chain of 2200 then 3000 and the ticks 6400 / 8450 were set on 2026-09-24,
08:06Z for the CLOSE as built, so that the sponges' tails would die and
every hold record complete within the run (section 13 item 2); the click
line at the rung (the owner's word of 09:50Z) removes that need, and the
pins are first rungs within 250 of the birth, set by the gap of 60 Links
and the speed alone. The hold 3000 was carried from the matter lamp's
hold, not derived from the band; the ramp 1500 was carried from the 64^3
boxes (section 8 names it 26 to 140 relaxation times there, the rule
needing ten). They SHRINK: the chain 800 / 300, the hold 500 (five
records per direction), the ramp 200, the ticks 1050 / 560. The pins do
not move with the chain or the hold (geometry-free beyond the gap and the
speed); the maps that gave 108 / 247 / 72 ran on a chain long enough for
the transit and nothing else.

light_clock_60 (5.7 in ticks, 3.9 in board): the chain of 673 kept the
-x face 600 Links from A so that its reflection returned after 2000, and
the 2000 came from reading many cycles; the pin is one record's first
rung at 213 after its birth, the -x half's reflection cannot reach the set
(A's cells held at 0 pass nothing), and only A's own train must be clear
of it. It SHRINKS to the builder's own test chain of 173 (A at [100,
112), the set 112, the mirror 172) and 460 ticks. The pin on that chain:
213 at W = 64 by the same map (the sweep of 07:24Z on the 173 chain,
computed before any T = 0 reading: 213 for every grace from 88 up, with
or without A's take), to be committed beside the map if the world is
regenerated.

redshift_k3 and redshift_control (2.4 to 2.9): the chain 4096 is the
loader's cap, carried, not derived; the hold 8000 was the light lamp's
hold and the ticks were set for the close. They SHRINK to the chain of
1420, the hold 1000 (13 clicks, the grain 0.1 percent), the ticks 4000;
the ramp 1500 stays as section 8 keeps it (the emitter's relaxation 90,
ten needed, 1500 declared). The pin is the one formula at k = 3 on the
well pair and does not move with the chain, the detector's distance or
the hold.

Bell (1 / 1 / 1): N = 2048 is the pin's own integer (181 / 64 is the
finite-N value with W = N); the bar and the ticks are minimal for the
declared train; the train of 128 periods is DESIGN.md 6.2's coherence line
and is the whole cost (3200 of the 5500 ticks, up to 3200 live arms, 19
minutes per world). A shorter train needs that line re-derived (what the
tables read of the chirped front), not made on this page; Bell STAYS.

Malus (1 / 1 / 1): sized by its wheel; STAYS.

two_slits (the records stay; the layer grows): the stock 1024 was sized as
Poisson statistics (L-3: "about 1000 clicks over five fringes; the dark
pixels' Poisson error") which the counting form does not produce; the
wheel [1, 64] beside it repeats one coarse pattern 16 times; the cadence
one per 16 stretched the ticks to 17300. The Runner's preliminary of
10:45Z on the declared file read every click at the open face behind the
lamp and none on the screen (the faces hold 97 percent of every record, the
mirror line reflecting all but two openings of width 1). It is
RE-DECLARED twice over: (1) the faces and the mirror line sinks outside
the ladder, the screen's sets the ladder with their own rung wheel (2^20,
from the dimmest cell a u chooses on the map), the lamp's wheel [1, 1024]
with the stock 1024 (one wheel, each u once), the cadence one per 4; (2)
THE GEOMETRY, on the blind map of the world itself (`two_slits_1024.py`,
12:10Z): the first draft's layer (128 x 128, y periodic, d = 32, L = 64,
the openings of width 1) reads 0.81 on 6.2's own boundary form and 0.39
with its y-periodic images, so its 0.959 was 6.2's number on 6.2's
geometry and not the world's; the world takes 6.2's geometry (d = 26, L =
113, the openings of width 3) on a 160 x 256 layer with x and y open,
where the same map reads 0.961 on the counts (0.950 on the offer, 6.2's
0.959 on the pilot's scaled board), 5500 ticks. The pin's number is
unmoved in substance (0.96 +- 0.02), its statistic is the counts' and its
world is the map's; the HOST grows to 94 minutes (the taller layer), the
largest of the GO list after Bell; the reading becomes exact. THE TWO
BUILDS it needs are named in the row (the lamp's ladder by name; the cell
of u over the ladder's own sum). The 128-period train (6 hours) is a
second world on the one list.

matter_waves_12 (3.6 in ticks; the records stay): the same sizing by
Poisson (section 12: "the Poisson sd 0.23 at the stock of 2048") for a
stock of 2048 at one per 8; section 12 names no wheel for the matter lamp.
It is RE-DECLARED as two_slits is in its ladder: the take lines sinks
outside the ladder, the screen's sets the ladder with their own rung wheel
65536 (which holds on the map: the dimmest chosen cell 9.7e-5 of the
norm), the lamp's wheel [1, 2048] with the stock 2048 (one wheel), the
cadence one per 2, 4700 ticks; the band the ladder's grain (0.016 Node on
the count centroid). Its GEOMETRY STAYS: the lattice map of the world
itself (`matter_waves_2048.py`, the matter kind's rule, 12:10Z) reads the
side lobe's count centroid 64 + 27.43 on the declared y-periodic layer
and 27.2 to 27.4 with open boundaries, so the images cost the statistic
less than 0.3 Node, inside the band of one Node; the pin is restated as
the lattice map's 27.4 with the two-source formula's 27.79 beside (the
statistic's earlier derivation, inside the band; both blind of any run).
Its HOST does not shrink.

4a, the boxes (ii-a), (ii-b) and the deep well (1.7 to 3.7 in ticks): the
holds of 8000 were carried from the exploration's runs, whose reader was a
spectral PEAK needing a long series; the reader of record is now the
clicks' mean interval, whose grain is 1 / span, and a hold of 1000 gives
a third of the band. The ramps stand where section 8 derived them (4a's
10000, ten relaxation times) or keeps them (1500 on the boxes and the
deep well, above the rule's ten). The boards (200^2, 64^3, 48^3, 128^2)
are set by each well's mode extent and are not re-derived here. They
SHRINK in the hold only: the ticks 13100 (11100 before the ramp 12000) / 2600 / 2600 and the rest
worlds 1200. The pins are the one formula per well and do not move.

pace fans, M2, the cart, the index (1 to 1.4): derived today (the fans),
minimal as built (M2, the cart), or derived in section 11 with the two
faces' returns placed around the window (the index, whose chain could
shorten to 3400 for a saving of a minute). They STAY.

## Which pins move with the geometry

None of the pins' numbers move with a shrink except as stated: the light
clock's 213 +- 1 is re-derived on the 173 chain and reads 213 there (the
same map, blind, `light_clock_60_receiver_173.out`); two_slits' and M1's
BANDS change form, from a Poisson error to the ladder's grain, and their
worlds change form (the faces and the wall sinks, the screen the ladder,
the wheel the stock); two_slits' GEOMETRY changes to 6.2's own on a taller
open layer and its pin is re-derived there (0.96 on the counts, the same
number), M1's pin is restated by the lattice map of its own layer (27.4
for the formula's 27.79, inside the band): every re-derivation blind, no
screen reading of either world existing (the Runner's 10:45Z run read the
face alone).
Geometry-free: sagnac (the gap and the speed), redshift (the formula on
the well pair at k = 3), Bell and Malus (the tables), 4a, the boxes and
the deep well (the well's formula), M2, the cart, the fans and the index
(unchanged geometry).

## What the owner asked, in one line per world

Sagnac: sized for the close, which the click line at the rung made
unnecessary; the hold and the ramp carried over. The light clock: sized
to keep one reflection out of a run made long for the later cycles; the
pin needs one record. Redshift: the loader's cap and the lamp's hold,
carried. Bell: sized by its pin's own N and by a declared coherence line.
Malus, M2, the cart, the fans, the index: sized by derivation or as
built, minimal. Two slits and M1: their stocks sized by Poisson
statistics the counting form does not have, the right size by a wrong
statistic, with a wheel of 64 that repeated one coarse pattern, and with
the open faces on the ladder, where the mirror line sends 97 percent of
every record. 4a, the boxes, the deep well: the holds
carried from a peak reader that no longer reads them; the ramps derived
or kept above the rule.
