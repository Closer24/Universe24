# The lean Node toy (tools/derivations/toys/lean), David's report of 2026-10-25

A generic Node of 94 integers, every integer within 128 bits, the same acts at every Node, built from the engine's exact primitives (core.rule3, core.paces, features.phase, loader.circle, features.volume) with the architecture the toy's; its decoder reads the run's log alone, in integers; the run back is exact. The toy is a derivation tool, not the engine: it names what the law does on a lean Node and what it does not do, with numbers.

Files: `lean_full.py` (the Node and the board, built from the two files and nothing else), `decoder_full.py` (the gates read from the record alone, every verdict from the record's numbers), `runback_test.py`, `cube48_test.py` (the 48 images), `mirror_diag.py` (where one mirror breaks), `residuals.py` (the one-click floor), `freeze_diag.py`, `records/` (the gates' tables), `universe_toy.json` (the integers den, node_clock, quantum_action, link_unit; the rows by shape and pair: the light at (den, den) and the three lifts) and `world_toy.json` (the shape, the intervals, the seed as lays: the sea with its hole, one quantum more at (1,0,0)). No number of a universe stands in the toy's code: the two held rows are the law's (the volume at (den - den div Gamma, den), the sign at (den, den)), the phase pair's amplitude is derived from half the law's width 128 less one, every root is the law's search `largest_below`. The probes that read the 4.0 record are under `../probes`.

Run: `PYTHONPATH=src python tools/derivations/toys/lean/lean_full.py <world.json> <out.json> [current|link|node] [back N]` (the mode `current` the law's Link close; `link` and `node` the toy's controls; `back N` runs N intervals back at the end and writes the result on the record), then `python tools/derivations/toys/lean/decoder_full.py <out.json>`. The runs below are at the den 15162856759112389 (54 bits, three lifts), the cube 5, Gamma 1000, T 36000, G 16, as `universe_toy.json` has them; the runs before the rebuild took the same numbers on the command line.

## The state at every Node (94 integers, fixed)

- the volume row: the time line (now, before, remainder) carrying X, three axis lines (the tensions), four write remainders: 16
- the light row: 3
- the sign row: the time line, three odd lines, four write remainders: 16; its phase row (wall 2): 3
- the three lifts' planes, two senses each, re and im lines: 36
- the records' counters (standing, crossed, beats) per plane record: 18; proper, closes: 2

## The acts in the two shapes (the owner's law of 2026-10-25)

act(row), atomic to the row (one function, applied to every row by one loop over the list):

1. Rule3's step of a line: inputs the line's three integers at the Node, the same line's now at the six neighbours, the row's pair, the Node's paces, the six Link factors; one carried division at the wall w. For a plane the arrival is read in the Node's frame (im negated where the two ends' frame bits differ), turned by the Link's pair (cos, sin) over X with one rounding and by the odd line's tangent triple (W^2 - n^2, 2 W n, W^2 + n^2), W = 4 Gamma, with one rounding (`step_line`, `step_plane`).
2. The share of a row at a Node: the frame's term 2 [w (now^2 + before^2) - S now before - now SUM_j R_j before_j] - SUM_j R_j (before - b_j)(now + n_j), one division by 4 p^2 G^2 (`share`, the engine's share.share with the halves).
3. The standing and the beat of a record: the share at or above the row's unit over one period of the re line's upward crossings (`close`, the bodies' part).
4. The tension's part of a row on each axis: weight x (now(i+a) - now(i-a))^2 (The stress is the Links'); the former -weight h_a kept by name under the switch LEAN_FORMER_TENSION (`tensions`).

act(rows), atomic to the Node (one sum or one exchange over the list):

5. The held write of the volume: the time line gets 4 X (3 den SUM forms - trace) p0^4 over 3 den Gamma^5 T, the axis lines (3 part_a - trace) p0^4 over 2 Gamma^4 3 den T, one carried division per line (`step`).
6. The held write of the sign: the time line 2 SUM W over T (W the Wronskian of every plane), the odd lines SUM J_a over T (J from the start's levels in the Node's frame), the phase row 2 Phi_now - Phi_before + c with c = rounded(L p0 / Gamma) (`step`).
7. The Link's count: K = Phi_next - Phi_before = 2 (Phi_now - Phi_before) + c at each end, n_ij = K_i - f_ij K_j, f the frame sign (`centred_count`, `link_phases`, `frames`).
8. The swap at the top: the weak maximum X0 <= X1 >= X2 with one strict on the volume's time line (the held before, the held now, the now after the writes), or the floor X0 < X_f or X2 < X_f with X_f = volume_of(Gamma, -Gamma); the turned Node ends the interval at the state it started from with every line's two levels exchanged and every remainder complemented at its wall, the im lines conjugated, the write remainders complemented from the held ones, the step's output discarded (`swap`, `exchange`).
9. The Link close: at a Node whose light share holds two whole quanta (or one and a whether), the one-Link read of every row's remainders on the digit lattices F = gcd(w, D, R) composed modulo 3 W_c, the lift by the quotient, the lay refused where the child's family stands above one quantum at its Node, the exact take from the light by the quadratic root on the Node's own term, the lay of one quantum of the child (the least A with (2 D + SUM R_j) A^2 >= unit x 4 p^2 G^2); with the switch `link` the + child at the +x end (the label; see below) (`close`, `read_number`, `take`, `lay_amplitude`).
10. The click of a bound body: the take from the light at the Node, the credit with its frame (the start's levels, the neighbours' start, the phases, the odd counts, the frames, the factors, the stepped level, the beat, the proper count).
11. The run back: every act inverted in the reverse order; at a turned Node the same act again on the kept post-state; the lays and takes from the log (`step_back`).

Where the eight approved sentences sit: 2 (the sign one row read whole) in act 6 and act 1 (every plane reads the one row, its own write among it); 4 (the click lays nothing into a bound body) in act 10 (the take moves the light alone; a body's count stands at its lay); 5 (every row's form at one weight) in act 5. Sentences 1, 3, 7 are NOT in the toy; see below.

## What the runs show (the records in `records/`)

Both run backs exact: 40 of 40 intervals bit for bit without Link births (1,492 turns, 243 births, 610 clicks) and with them (1,225 turns, 168 births, 490 clicks).

Run A, no Link birth, 600 intervals (`records/gates_u24_node7.jsonl`): births 379 (stop by 100); credits 6,086 and continuing; the mean volume 1,000 -> 94,101 (200) -> 63,929 (300) -> 59,398 (400) -> 36,351 (600): the top and the contraction (gates 1/3/6 SHOWN at the board); dilation SHOWN (proper per thousand intervals shallow 797,387 against deep 514,279); the Links lengthening in the clicks SHOWN (spacing in hundredths 804 shallow against 3,753 deep); charge SHOWN (the senses' sum 0); era of matter SHOWN; horizon NOT REACHED (max content 1,232 against frozen 3,793); the one-click floor SHOWN (6,086 of 6,086 credits within it); species over the track 632 of 744; the three constants SHOWN (94 integers, max state bits 121, max transient 102).

Run A to 2,400 intervals (`u24_node8`): the mean volume 94,101 (200) -> 36,351 (600) -> 148,062 (1000) -> 120,991 (1200) -> 2.5e6 (1600) -> 2.7e8 (2400): two returns, then a slow pump (the planes' energy 25 -> 37 bits, the light's velocity 190 -> 5,350), the clicks stopping at 6,908 after 1600; 128 bits held.

Run B, Link births, 300 intervals (`records/gates_u24_link9.jsonl`): births 200 (stop by 150); credits 5,438; the mean volume 3,337 (50) -> 8,802 (150) -> 5,602 (200) -> 7,281 (300), a return; dilation SHOWN; the one-click floor SHOWN (5,438 of 5,438); species over the track 643 of 724; 128 bits held (max transient 99).

## What was found on the way (each against the law's text or the 4.0 record)

1. The swap of the post-state locked the board in a two-cycle at its top (every Node turning every interval, no click), as ALGEBRA.md's The swap at the top says by name ("refuted and shown"); the act is the pre-state exchanged and complemented, the step's output discarded. Moved to it.
2. The 4.0 record births 54 pairs at intervals 12 to 17 and none after: the probe `probes/refusals_probe.py` on the record's own world reproduces 6 + 39 + 1 + 8 = 54, then every meeting refused by the cause "lay" (take.below_quantum: a child is not laid where its family stands above one quantum). The toy lacked that comparison and birthed 26,934 pairs; with it 200 to 380.
3. The fold pumped: with the phase pair alone the planes exploded (15,853 bits at 150), with the odd tangent alone they held. The toy read the Link's count as Phi_i - Phi_j; the law (M23) reads K = Phi_next - Phi_before, one integration less. With K the Link run holds 300 intervals.
4. The species misreads were the turn: at a turned Node the credit's now was the start's; the stepped level is named on the credit, and every credit then reads within the one-click floor, the two remainders' bound w sqrt(2) / |denom| (2,488 of 2,488 and 5,617 of 5,617 in the earlier runs).
5. The lay at a fixed amplitude the root of T / 2 left the heavies below one quantum under the frame share (the clicks stopped); the lay of one quantum of the child's unit at the Node's paces restores the clicks.
6. The remaining pump is the Link factor Q = G^2 (Gamma - t)^2 / Gamma^2 above G^2 under negative tension: the toy's tension lines reach thousands where the 4.0 record's means stay within 10 (the eras' tension_means), so the toy's axis write scale is not the engine's (records.scaled_sum, the walls of loader.held_write_of); under the decided square tension at the toy's scale the tensions pass Gamma by interval 300. Open: the port of the engine's write scales.

## What the toy does not do (by name, against the eight sentences and the two laws)

- Sentence 1, the orientation by the light's current F_ij: BUILT (the mode `current` of `lean_full.py`, the Link close: every Link once, a meeting where both ends hold a whole quantum of light, F_ij = num (now_i before_j - before_i now_j) at the start, F = 0 refused by the name `orientation`, the + child at the end the current flows into, the Link's one number read at that end and the take there; the label `link` kept as the negative control). Measured by `cube48_test.py` on the 3-cube at the 54-bit den, 30 intervals, the births (interval, the take's Node, the lift, the two children's Nodes) and the volume and light rows compared through every image: the hole seed 48 of 48 (84 births, 318 refused at F = 0, 113 turns); the hole seed plus one quantum at (1,0,0) 48 of 48 (66 births, 227 refused at F = 0, 129 turns); the label 8 of 48 (60 births). Three labels had to leave first, each found by `mirror_diag.py` (the first interval and quantity where one mirror breaks): the Link's number read at the +a end (6 of 48; read at the current's end instead), the births' takes in the x-major order (one take per Node of the children's walls summed, the start's light paying, as meeting_board.closed has it), and the odd line on the Link read as the floored mean (every odd sum broke the mirror by one unit; the engine's V_ij = V_a(i) + V_a(j) is the sum, no division). The run back exact 25 of 25 in this mode (549 turns, 338 births, 159 clicks).
- Sentence 3, a bound body's write lighting the massless line: not in the toy; no light click with a beat is credited (gates 7, 11, 12 NOT SHOWN).
- Sentence 7, the threshold at the vacuum's weight: the toy reads the share at the frame's weight (4 p^2 G^2 at the Node's pace); the births stop by the lay's refusal, not by the vacuum's weight.
- Sentence 6 (the gap of the middle) is a derivation the toy did not run; sentence 8 waits by the owner's word.
- The law "one act on every row alike": the toy's volume write sums the forms of the light and the planes (not the held rows); the births read the light row as the seed; the swap's trigger reads the volume row (the law's own). The toy's probes name these; none is a species name.
- The law "no number in the code": the toy holds Gamma 1000, T 36000, G 16, the phase width 63, the orbit cap 65,536 and the seed's drift the root of T in the code and takes den on the command line; `universe_toy.json` and `world_toy.json` give the same universe in the generic form, and the toy does not read them. Universe24's seed with one quantum more off the origin is not in the toy.
- The body test of the W hands (a one-quantum body in a hand-laid well with the sea emptied) is not run in this toy; the toy's bodies are records credited at one Node (no track moves; gates 9 and 13 NOT SHOWN).
- Exact conservation at the click (gate 15): the identity taken >= booked holds on every birth; the excess below one level of light is the known item.
