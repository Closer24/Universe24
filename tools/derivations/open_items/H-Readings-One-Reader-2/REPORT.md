# H-Readings-One-Reader-2 (ro2): the readings as one reader. Report (2026-10-26, toys-5 at 853582d7b, the worktree's head: 3dc12e307 plus TW-S1; the committed records of this head)

## The verdict line

Every reading of a Link is one read of the pair (x_i, x_j) at a Port, linear x_i + s x_j or bilinear x_i y_j - y_i x_j, and every reading of a row is one bilinear x.M.y with M one of the row's four matrices named once (G, GJ, G Gamma_a, K): TWO readers (the row's gram is not a reading of the Link's record, the quartet's G being the file's trace form; the cross is the one bilinear they share), link_reader.py 80 function lines and row_reader.py 71 against the 379 lines of the engine that read the Link's record and the row's gram, bit for bit on the hole 60 and the chiral 60 with the run back 20 of 20: every call of twenty engine reading functions compared with the reader's value at the same arguments, 2,006,974 calls on the hole and 2,078,329 on the chiral, 0 apart on either; the readings' 1,443 lines do not become 151, because 1,042 of them read other objects (the file, the carrier, the seed, the click, quartet's derivation) and are not a reading of the Link or the row.

## The inventory's groups and sums (the lines def-to-end on this head; the table with lines, reads, returns and consumers in DERIVATION.md section 2)

- The Link's record (F_ij and its parts: the factor, the frame, the count and phase pair, the odd part, the fold, the current, the net current, the twist, the gradient, the turn): links.py 74, readings.py 35, metric.py 16, node.py and interval.readings 54: 179.
- The row's gram (the charge, the current, the density, the curl, the term, the share, the period; the stress, shear and flux parts; the force and the emission): gram.py 146, metric.py and interval.py and node.is_im 76: 222; quartet.py's derivation of the four matrices 348.
- The file's constants (the wall, the mass, the reaches, the factor's form, the units, the walls): core/rule3.py 110, node.py and rows.py 37: 147.
- The carrier's lines (the clock's table, the paces, the content, the frozen mask, the orbit's pair, the floor, the mean wall): core/paces.py 118, readings.py, node.py and interval.py 38: 156.
- The seed's envelopes: seed.py 110, wave.py 14, gram.moving/rest/levels 29: 153.
- The click's readings (the fall, the draw, the walls and shares, the meeting, the credit's frame): take.py 43, draw.py 27, merger.py 74, close.py 48, bodies.py 46: 238.
- The sum 1,443 (the Node pair: 1,359 and 1,458). The two readers address 401 of them (179 + 222); the proven replacement 379 to 151.

## The record module's lines and proof

one_record.py: the log's three lines spelt once each through one head `entry(event, i, node)` (refused with its count, birth, credit), the frame of the close, COUNTS, the census (arrays, census, state_bytes, state_hash, bits_of) and the writer (run.py's eight functions): 278 function lines, 18 names (361 with the docstrings; 298 code lines) against the 293 engine lines it replaces (run.py 164, close.refused 6, the dict of close.children 30, bodies.credit 42, interval.close 13, node's census 20, COUNTS 16, merger.read_ends' stop line 2): one home and the head spelt once, no cut in count; the Node pair's 366 to 518 counted the state's classes too, which stay. Proved by replacing the engine's spellings in-process (prove_record.py) and running the writer: the hole 60 against examples/records/hole.json every key equal, the log 21,699 of 21,699 entries equal (19,394 refusals, 2,288 credits, 17 births; the brief's 16,903 is 3dc12e307's count, before TW-S1's regeneration), the counts equal, the run back 20 of 20, 15 s; the chiral 60 against examples/records/chiral.json every key equal, 23,519 of 23,519 entries equal, the run back 20 of 20.

## The map's estimate against the 70 percent

Strokes 8 to 12 after the Node pair's seven (DERIVATION.md section 5): 8 the Link reader (160 to 80), 9 the row reader (77 to 71 proved; metric's three bilinears, 24 lines, to follow), 10 the record module (293 to 294), 11 quartet.py to the loader (348 out of the engine), 12 the dead readings struck (about 60). The lines after: the acts 150, the readings 925, the record 294, the refusals 123, the wrappers about 100, the second roads 0: about 1,592 of 2,959 function lines, 46 percent out. The owner's 70 percent (to 890) is NOT reached by the readers: the 700 lines above the mark are the readings of the other objects (the paces' table 118, the file's constants 147, the seed's envelopes 153, the click's readings 238, the metric lines 28) and the refusals 123, each one spelling already; a cut there is a cut of what the law reads, not of its spelling.

## Bugs (toys-5 853582d7b, by file and line; the list with the measured counts in DERIVATION.md section 6)

1. interval.py:135 the curl computed at every interval and read by gram.term (gram.py:128) only where a row has axis matrices: 80 curl and 400 term calls with no quartet on each record (dead work on every record without one).
2. interval.py:123 and :126-134 the Link phases computed twice per interval (self.phases and links_at[1]: 240 link_phases calls on 80 intervals); node.start_phases read by bodies.frame_of:103 alone.
3. interval.py:126-134 links_at[0], the coupling-0 record (frames**0, count*0, odd*0): six board-wide vectorised pair_angle calls for the constant pair per interval, where turn None at node.turned_arrival:165 is the identity in one line.
4. node.py:235 node.act's `levels` returned and read by no caller (interval.py:116 `_levels`, :213 `[-1]`): a reading computed and discarded on every act of the carrier and the walled row.
5. node.py:311 read_lines' plane_starts read nowhere; node.py:318 digit_of returns its inputs; links.py:87 wronskian and node.py:264 is_im with no caller in src (tests alone).
6. merger.py:58 share_at, gram.share re-spelt at one Node (callers merger.py:51, 102, 105; the audit's item 8, still live); gram.py:138 the local import inside share.
7. close.py:74-76 the currents, twists and charges of every record computed over the whole board at every click and read at the few standing Nodes alone.

## Cut short (by name)

- The metric's three bilinears (metric.stress_parts, shear_parts, net_flux) as readings of the row reader: named in the map, not written or proved.
- The 48 (the kit's clicks_48.py) and the kit's flagged copy (make_flagged_copy.py) not run: the readers were proved by in-process wrappers on the engine's own run, forward and back, and not by a copy of src with the reader in the engine's path.
- The record module's proof on the bodies' record (examples/records/bodies.json, 120 intervals): not run.
- The interval's readings block itself (interval.py:86-166, 81 lines) was read through the readers' values but not re-cut as one function of the two readers.

Files: tools/derivations/open_items/H-Readings-One-Reader-2/{DERIVATION.md, REPORT.md, link_reader.py, row_reader.py, one_record.py, prove_readers.py, prove_record.py, out/readers_hole_60.json, out/readers_chiral_60.json, out/record_hole_60.json, out/record_chiral_60.json}. Nothing under src/ or tests/ edited; no commit, no push.
