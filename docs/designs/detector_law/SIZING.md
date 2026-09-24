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
   record per cell), not a Poisson error. A lamp under `residue_order`
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
| light_clock_60 | 213 +- 1 at W = 64 (section 10 item 9, 09:55Z) | the first cycle's record's first rung at the set, DETECTOR; the later cycles beside | 3 (the pin's record and two later cycles) | chain 173 (A at [100, 112), the set 112, the mirror 172; the -x face 100 from A: its half returns at 346, after the rung) | 460 (the first rung at 267, the third cycle's at 407, margin 50) | 37 / 673 / 2600 | 12 / 3.9 / 5.7 | 8 s / 0.3 s |
| redshift_k3 | 1 + z = 1.9889, the band 0.3 percent | f_B over the hold's clicks, a ratio of differences, DETECTOR; the grain 1 / span | 13 hold clicks (a hold of 1000; the grain 0.1 percent) | chain 1420 (the block from 1217 receding 1117 Links by the run's end, the detector 200 Links beyond its start, a margin 100) | 4000 (ramp 1500 as section 8 keeps it, hold 1000, the last hold record's transit 1356 plus its rung and margin) | 38 / 4096 / 9600 | 2.9 / 2.9 / 2.4 | 3.3 min / 9 s |
| redshift_control | the control's f_B (the ratio's denominator) | the same at rest | 13 | chain 1420 (the pair alike) | 4000 (the pair alike; 1450 would do at rest) | 38 / 4096 / 9600 | 2.9 / 2.9 / 2.4 | 3.3 min / 9 s |
| bell_a0b0, a0b1, a1b0, a1b1 | S = 181 / 64 exactly at N = 2048 (the finite-N value, W = N); the band the ladder's grain 1 / 2048 | the joint cells' counts per setting, DETECTOR; S from the four correlations; the seed permutation gives each u once, the counts exact | 2048 (one wheel; the pin's own N) | the bar of 21 (the tables at 3 and 7 Links, the sponges) | 5500 (2048 births, the train 3200, the close 250) | 2048 / 21 / 5500 | 1 / 1 / 1 | 19 min each / 19 min (the train is the cost: 128 periods, DESIGN.md 6.2's coherence line; a 16-period train would read 1.5 min, a re-derivation of that line, not made here) |
| malus_45, 11.25, 28.125, 33.75 | 128, 246, 199, 177 of 256 (cos^2 s x 256), the band one count (the wheel [159, 256] a permutation, exact) | the + cell's count, DETECTOR | 256 (one wheel) | the bar of 9 (section 14 item 6) | 1200 (256 births, the train 800, margin) | 256 / 7 to 9 / 1200 | 1 / 1 / 1 | seconds / seconds |
| two_slits | the visibility 0.959 at 32 periods; the band +- 0.02 was declared as Poisson over about 1000 clicks: RE-DERIVED as the ladder's grain at W = 64 (a blind computation on the same geometry, before the pin run) | the screen's clicks per Node, DETECTOR; (max - min) / (max + min) | 64 (one wheel [1, 64]; 1024 is 16 copies of it) | the 128 x 128 layer (d = 32, L = 64, the fringes over y in [4, 124]: the pin's geometry) | 2000 (64 births at one per 16 = 1024, the train 665, the transit 146, margin) | 1024 / 128^2 / 17300 | 16 / 1 / 8.7 | 24 min / 3 min |
| pace_fan_12, 16, 24 | the phase pace by direction, 0.8 / 0.4 / 0.2 percent on the axis, a quarter on the diagonal (GAMEBOARD); the band the reader's spread (L-6, 10:15Z) | the two probes' phase difference per ray at one interval, GAMEBOARD | 1 | the 128 x 128 layer (the probes at 40 Links plus the sponge; 96 x 96 would do) | 830 / 1110 / 1500 (the train, the train's end past the inner probe, margin 100) | 1 / 128^2 / 1000, 1400, 1900 | 1 / 1.8 / 1.2 | seconds / seconds |
| layer_pin_rest_14, layer_pin_k3_14 (4a) | f / f_0 = 0.8116, the band 0.3 percent | the block's clicks' mean interval over the hold, at k = 3 over the rest's | 24 clicks at k = 3 (a hold of 1000), 28 at rest (1200) | the 200 x 200 layer: set by the shallow well's mode extent (section 8, eps 0.013), NOT re-derived here | k = 3: 11100 (ramp 10000 by section 8's rule, hold 1000, margin); rest 1200 | 150 clicks / 200^2 / 18500; rest 80 / 200^2 / 3500 | 6 / 1 / 1.7; rest 2.9 / 1 / 2.9 | 4.2 min / 2.5 min; rest 0.8 / 0.3 min |
| cart_k3 (4c) | (1 + beta) / (1 - beta) = 3.732 | the cart's received line over the sent (a frequency ratio) | as built (the lamps' 8192 records are 128 wheels of [1, 64]; the ratio needs one) | 240 x 3 x 3 as built | 600 as built | 8192 x 2 / 240 x 3 x 3 / 600 | 128 / 1 / 1 | seconds / seconds |
| matter_front_12 (M2) | 169 +- 2 at W = 64 | the first click's interval from the birth, DETECTOR | 1 | the chain of 200 (the set at 84 Links) | 420 (the rung 169, the train 150, margin 100) | 1 / 200 / 600 | 1 / 1 / 1.4 | seconds / seconds |
| matter_waves_12 (M1; the file not yet written) | the centroid y = 64 + 27.79, the band one Node; declared as a 4.4-sigma Poisson statistic at 2048: RE-DERIVED as the ladder's grain if the matter lamp's wheel is a stride (section 12 names no wheel; it must) | the screen's counts per Node, the side lobe's centroid, DETECTOR | 64 (one wheel) if a stride wheel; 2048 stands only under a drawn residue per birth | the 128 x 128 layer (d = 32, L = 64) | 930 (64 births at one per 8, the train 150, the transit 167, margin 100) | 2048 / 128^2 / 16700 | 32 / 1 / 18 | 30 min / 1.7 min |
| moving_20, moving_28 ((ii-a), (ii-b)) | 0.7814 and 0.8032, the band 0.3 percent | the block's clicks' mean interval at k = 3 over the rest's | 19 clicks (a hold of 1000 at the moving period about 52) | the 64^3 box: set by the well's mode extent, NOT re-derived here | 2600 (ramp 1500 as section 8 keeps it, hold 1000, margin 100) | 150 / 64^3 / 9500 | 8 / 1 / 3.7 | 38 min each / 10 min |
| rest_20, rest_28 | the rest clocks (the denominators) | the same at rest | 28 clicks (1200) | the 48^3 box, as above | 1200 | 70 / 48^3 / 3000 | 2.5 / 1 / 2.5 | 12 min each / 5 min |
| deep_well_k3_40, deep_well_rest_40 | 0.7531 (the cavity's control), the band 0.3 percent | the block's clicks' mean interval | 19 clicks at k = 3 (1000); 28 at rest (1200) | the 128 x 128 layer for s = 40: the well's extent, NOT re-derived here | k = 3: 2600 (ramp 1500, hold 1000, margin); rest 1200 | 150 / 128^2 / 9500; rest 80 / 128^2 / 3500 | 8 / 1 / 3.7; rest 2.9 / 1 / 2.9 | 3 min / 0.8 min; rest 1.1 / 0.4 min |
| index_moving_long_k3_away, its rest and reference worlds ((v-m)) | the lab phase +1.0144 rad, +- 0.04; the drift 1.2e-3 rad per interval, +- 10 percent (P, GAMEBOARD) | the probe's phase over the window [3800, 5400] against the reference, and its drift | 1 (one train, one block) | chain 3400 (the far end 1000 beyond the probe returns its reflection at 6230, after the window; the -x return at 5543 sets the window's end and stands) | 5500 (the window's end 5400, margin 100) | 1 / 4000 / 6000 | 1 / 1.2 / 1.1 | 2 min each / 1.5 min |

The totals, HOST on one core, the worlds one after another: DECLARED
about 260 minutes (Bell 76, the boxes and their rest worlds 100, M1 30,
two_slits 24, the sagnac and redshift chains 16, 4a 5, the deep well 4,
the index 6, the rest seconds); MINIMAL about 120 minutes with Bell's
train as declared (Bell 76, the boxes 30, the index 4.5, 4a 2.8, two_slits
3, M1 1.7, the deep well 1.2, the chains under a minute), about 50 minutes
if Bell's train is re-derived to 16 periods.

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

two_slits (16 in records, 8.7 in ticks): the stock 1024 was sized as
Poisson statistics (L-3: "about 1000 clicks over five fringes; the dark
pixels' Poisson error") which the counting form with the stride wheel
[1, 64] does not produce; the cadence one per 16 was chosen for the HOST
per interval and stretched the ticks to 17300. It SHRINKS to one wheel,
64 records, 2000 ticks; the pin's band is re-derived as the ladder's grain
at W = 64 on the same geometry (blind: the count visibility of the
64-pattern, in which a dark fringe below 1 / 128 of the record reads no
click), before its pin run.

matter_waves_12 (32 in records, 18 in ticks): the same sizing by Poisson
(section 12: "the Poisson sd 0.23 at the stock of 2048") for a stock of
2048 at one per 8; section 12 names no wheel for the matter lamp. If the
wheel is a stride, it SHRINKS to one wheel and 930 ticks with the band
re-derived as the ladder's grain; if the row wants drawn residues (a
seed order per birth, as Bell's), the declaration must say so and the
stock stands. The declaration decides before the file is written.

4a, the boxes (ii-a), (ii-b) and the deep well (1.7 to 3.7 in ticks): the
holds of 8000 were carried from the exploration's runs, whose reader was a
spectral PEAK needing a long series; the reader of record is now the
clicks' mean interval, whose grain is 1 / span, and a hold of 1000 gives
a third of the band. The ramps stand where section 8 derived them (4a's
10000, ten relaxation times) or keeps them (1500 on the boxes and the
deep well, above the rule's ten). The boards (200^2, 64^3, 48^3, 128^2)
are set by each well's mode extent and are not re-derived here. They
SHRINK in the hold only: the ticks 11100 / 2600 / 2600 and the rest
worlds 1200. The pins are the one formula per well and do not move.

pace fans, M2, the cart, the index (1 to 1.4): derived today (the fans),
minimal as built (M2, the cart), or derived in section 11 with the two
faces' returns placed around the window (the index, whose chain could
shorten to 3400 for a saving of a minute). They STAY.

## Which pins move with the geometry

None of the pins' numbers move with a shrink except as stated: the light
clock's 213 +- 1 is re-derived on the 173 chain and reads 213 there (the
same map, blind); two_slits' and M1's BANDS change form, from a Poisson
error to the ladder's grain, a re-derivation on the same geometry, blind.
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
built, minimal. Two slits and M1: sized by Poisson statistics the
counting form does not have. 4a, the boxes, the deep well: the holds
carried from a peak reader that no longer reads them; the ramps derived
or kept above the rule.
