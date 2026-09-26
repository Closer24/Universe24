# The board and the one algebra: a correspondence audit (2026-09-25, read-only)

The owner's request (record 1937): check that the algebra takes in everything on the board: how a beam splits, the small laws found on the board, and how mass affects the computation and so the times.

## Sources, exactly as read

- **The engine.** `origin/emitter-click` at `a9ab486f` ("The generator as the operator iterated with the stop", BUILD.md section 26 item 25). Files: `src/event_universe/events/detector_law.py` (1836 lines), `events/world.py`, `events/run.py`, `diagnostics/massive_record_margin.py`, `tools/run_inputs.py`, `docs/designs/detector_law/BUILD.md` section 26 (items 1 to 25), `docs/ENGINE.md`. Line numbers below refer to this head.
- **The algebra.** `docs/ALGEBRA.md` on `origin/lab-tools-unification` at `0240ab0b` (PR 1150): chapter 8 and sections 9.12 to 9.27. The tool cards are `docs/designs/lab_tools/LAB_TOOLS.md` part A.
- **The small laws.**
  - `docs/HIGHLIGHTS.md` 5.4 and `docs/LOG_2026-09-20.md`, both on `origin/claude/new-boss-skills-file-4d1svd` at `1445dc55`.
  - `docs/DERIVATIONS_BEAM.md`.
  - `docs/designs/paper_verification/NEW_ENGINE_AUDIT.md`.
  - `docs/designs/detector_law/DESIGN.md` 4.1.
  - ALGEBRA.md chapters 1 to 7.
- **The tests run.** A fresh worktree at `a9ab486f`, run with the repository's `.venv` (Python 3.14.0rc2, numpy 2.5.3).
  - The first attempt failed at import with `ModuleNotFoundError: No module named 'scipy'`. `pyproject.toml` declares `scipy>=1.14,<2`, but the `.venv` does not have it. `test_board_properties.py` imports `massive_record_margin.py`, which imports scipy.
  - I installed scipy 1.18.1 into a scratch directory outside the repository (`uv pip --target`). The `.venv` was not touched. I then re-ran with `PYTHONPATH` pointing at that directory.
  - `tests/test_board_properties.py`, `tests/test_detector_law.py`, `tests/test_emitter.py` and `tests/test_extents_and_face_slab.py`: **24 passed in 32.4 s**.
  - That is the 10 board properties: 48 of 48 transforms, 7 translations, conservation, the inverse, locality, only the click reads, host cost at 12, 24 and 48, and same input gives the same output. It also covers 6 detector-law tests, 3 emitter tests and 5 extent and face-slab tests.

Marks used: MATCHES, DIFFERS (said how), MISSING IN ALGEBRA; BUILT, NOT YET BUILT, CONTRADICTED; REFLECTS, RETIRES, DOES NOT MENTION.

**Counts (primary verdict per row):**

| Table | Rows | Verdicts |
| --- | --- | --- |
| 1 | 50 | MATCHES 25, DIFFERS 12, MISSING IN ALGEBRA 6, CONTRADICTED 6, not in the engine 1 |
| 2 | 54 | BUILT 27, NOT YET BUILT 21, CONTRADICTED 6 |
| 3 | 36 | REFLECTS 23, RETIRES 12, DOES NOT MENTION 1 |

"The one algebra" means ALGEBRA.md chapter 8 together with 9.12 to 9.27. Chapters 1 to 7 of the same file are the ray law's (`beam-v1`) algebra. They are marked as history only locally (for example at line 584). They still state the crowd, the age wall and the shell mean as SHOWN; see table 3.

---

## Table 1. CODE -> ALGEBRA: every mechanism the engine performs in a run

### 1a. The path selection

| # | Mechanism | Where | ALGEBRA.md | Verdict |
| --- | --- | --- | --- | --- |
| 1 | Which engine runs | `run.py:102-106`: `DetectorLawSimulation` if the world declares `detector_law`, else `NatureBeamSimulation` (the ray law `beam-v1`: flights, the collision table, the crowd, the push, the drive, tables) | 9.19 (5), 9.21 (3): "one step of one operator ... plus the click" | **MISSING IN ALGEBRA.** Chapter 9 has no ray-law path. Yet the ray law is still the engine's default. about 300 of the 347 world JSON files on the branch (a heuristic count) lack `detector_law: true`, and `docs/ENGINE.md` line 3 still says "The one engine ... is the engine of the Beam Law (`beam-v1`)". Its mechanisms are in table 1d. |

### 1b. The interval of the detector law, in the engine's order (`step`, `detector_law.py:1573-1672`)

| # | Mechanism | Where | ALGEBRA.md | Verdict |
| --- | --- | --- | --- | --- |
| 2 | The interval's column order | `step` 1573-1672. The order is: the blocks' hops; each block's own record advanced with its emitted light's receive; the excited record's rung; per light record, each block's response then light with the sources; the births; the block clocks; the deletions; the probes | 8.5 (massive step first, then light with the massive forward difference); 9.19 (5); 9.17 (1) (E^T at the click's interval) | **MATCHES** in column order and in the birth after the advances. The hop at the head of the interval is covered in row 18. |
| 3 | The rule, one division with the remainder kept | `_advance` 1266-1331: `total = num*scale*S_6 - wall*before + r + extra`, `nxt = floor(total / wall)`, `r' = total - wall*nxt`, `wall = 3 den scale` | 8.1 (the rule); 8.5 (the one division, walls 3 den g_d and 3 G_d); 8.8 (bijection) | **MATCHES.** |
| 4 | Pairs per Node per family | `kind_num` and `kind_den` arrays (`__init__` about 401-409); `_write_pair` 559-573 writes a block's pair on its cells, the vacuum's elsewhere | 8.1, 8.3, 9.19 (2): one pair per family per Node, a body's region its pair | **MATCHES.** |
| 5 | The six reads and the faces | `_neighbours` 1118-1141: wrap on a periodic axis; 0 beyond an open face; the row itself twice on an axis of extent 1. `_shift` 1092 | 8.2 lemma (the self-reads); 1.6 | **MATCHES.** |
| 6 | Per-family faces | `kind_wrap` from the family key `faces` (`world.py` `_kind_faces` 2295-2322; light uses the world's `boundary`) | 9.18 (2) and 9.21 (7) (b): "ONE BORDER FOR EVERY FAMILY", DECIDED by record 1875 | **DIFFERS.** The engine still gives each massive family its own faces (periodic by default). |
| 7 | The remainder rescaled when the wall's scale changes | `_advance` 1285-1290: `r = r * new // old` when the motion pair changes (only under a ramp) | 8.8 assumes a fixed wall per row | **MISSING IN ALGEBRA.** It is a lossy floor that breaks 8.8's bijection. It occurs only with the ramp, which the algebra retires (row 18). |
| 8 | The amplitude bound | `_advance` 1303-1310 raises above the world's `amplitude_bound` | 9.26 (4) (b): "bounded by refusal, never by overflow" | **MATCHES.** |
| 9 | Branches on the family's kind in the law's path | `_advance` 1276: `booked = not massive_kind or live.emitter is not None`. `step` 1601: a massive record is advanced only if born of an emitter. `step_inverse` 1060 | 9.18 (5) and 9.21 (3): "no place in it for ... the `massive_kind` branches in the law's path"; 9.20 (A) 6: "no branch on a name or a value" | **CONTRADICTED.** A block's own record and its responses book no flux and sit on no ladder, and that is chosen by kind, not by the named set. The algebra's one click rule (9.17 (7) (f)) is built as two machineries selected by this branch. |

### 1c. Materials, bodies and tools

| # | Mechanism | Where | ALGEBRA.md | Verdict |
| --- | --- | --- | --- | --- |
| 10 | Mirror and splitter material | A block of light's family with a pair den > num, no seed, no coupling (`world.py` 3486-3500; "the (M) wall"). Its cells carry the gap and nothing else | 9.18 (1) table (a light pair: the mirror, the splitter, an index slab); A.3, A.4 (the gap [1, 2]; the splitter [2, 3] at k = pi / 2) | **MATCHES** as an operator region. **DIFFERS** in its carrier: 9.18 (1)-(2), A.10 and A.12 ADOPT tool bodies that are bound bodies of the holder family carrying light's pair on the same cells, and retire the silent body. The engine's mirror is a silent block of light's own family. |
| 11 | Massive barrier (raised pair) | `world.py` 3478-3486 (seed forced to 0) | 9.18 (1); the holder-family barrier of de Broglie's fringes, 9.22 (8) | **MATCHES** as a region. Same carrier difference as row 10. |
| 12 | Cavity | `step` 1591-1593: the own record is set to 0 outside the cells every interval (`cavity: true`, used by `index_10/20/50.json` and `cavity_24*.json`) | 9.10 item 4: the cavity's read is replaced by "a DECLARED ZERO FACE made material: a gap pair". 9.12: a projection is "not admitted into the law" | **CONTRADICTED.** This is a per-interval projection, the kind of act 9.12 removed with the take. |
| 13 | Splitter and slit behaviour | No engine code: a splitter is a region of light's pair, a slit an opening in a gap wall. The table splitter and polariser are refused at construction, 333-349 | A.4 (the reflection share formula); 9.25 (10) (the fringe spacing); 9.21 | **MATCHES** (data only; the split is the rule's own). |
| 14 | Coupling: receive and source in the one division | `_difference` 680, `_coupled_term` 693, `receive_scale` 704, `_receive` 710, `_source` 719; `light_scale` is the least common multiple of the G denominators (about 455-463). The massive row gains `3 den g_n (a_l,now - a_l,before)`; light gains `-3 G_n (L / G_d)(a_m,next - a_m,now)` | 8.5 (the form, the Euler-Lagrange scheme, J, the one division) | **MATCHES.** |
| 15 | The coupling split into one response record per light record | `step` 1614-1632: every block creates `block.responses[identity]`, a massive summand of content 0 per light record, advanced by the receive and feeding light's source | 8.5 and 9.19 (1): one massive record per body, the coupling bilinear in the two records | **MISSING IN ALGEBRA.** It is equal in total by linearity, but it has a consequence. Light from other bodies never reaches the excited record's rows, so it cannot spread that record's residues. **DIFFERS** from 9.19 (4e) (i): "a distribution of residues needs the body's coupling ... or another body's field". |
| 16 | An emitter's own light: back-action by g only | `step` 1582-1590: the own record gains g times its emitted light's difference. `step` 1617: "a body answers no record of its own", so there is no G source from the own record into its own light (BUILD.md 26 item 19 (a): "g alone is built") | 8.5: J is conserved only with both entries. 9.19 (4e) states only the g side | **DIFFERS.** The pair on the emitter's own light is one-sided, so 8.5's variational scheme and its invariant J do not hold for it. The question is open to the mathematician (BUILD item 19 (a)). |
| 17 | Coupling in motion | `motion_pair` 609: `[W_d^2, W_d^2 - 3 P . P]` scales g | 8.5, last paragraph ("the one pair the engine forms in motion", CARRIED) | **MATCHES** 8.5. But 9.24 (3) retires moving material and with it this pair (see row 18). |
| 18 | The block's hop by a declared momentum with a ramp | `_momentum_now` 597 (ramp), `_move_block` 622 (`by_drive` against `wall = 3 LABEL_SCALE width amount`, one Link at most, x before y before z). `check_body_conditions` REQUIRES a ramp of at least RELAXATION_TIMES relaxation times on a moving body (`massive_record_margin.py` 780-799) | 8.11 (the step, CARRIED). 9.22 (2): "no ramp (DECIDED, record 1884 ...)", refused at load. 9.24 (3): "THE REGION OF MATERIAL DOES NOT MOVE (PROVED)"; (b) the push "RETIRING with the moving wells"; (5) "no `ramp` key; a world with one is refused" | **CONTRADICTED.** The engine moves material and requires a ramp. The algebra forbids both. The replacement (packets with **K** and the moving name) is not built (table 2). |
| 19 | The push by light's stress at the outer Ports | absent | 8.11, 9.15 (ii), 9.18 (4) item 7 | No engine mechanism (table 2). |

### 1d. The emitter and the birth

| # | Mechanism | Where | ALGEBRA.md | Verdict |
| --- | --- | --- | --- | --- |
| 20 | The excitation | `_excite` 744-786. It requires the seed as a profile, `born` and `norm`, sets `residue_pending`, and sets the offer to 0. The first excitation is made at construction (about 440) | 9.17 (4) item 1 (the excited records in turn); 9.9 (the composed mode); 9.19 (4e) (ii) (the residue read after the first advance) | **MATCHES.** |
| 21 | The emitter's own-tick rung | `_excitation_rung` 799-824. At the first call it reads u and W from the record's remainder at the centre cell. Then `offer += form_share(own, centre)`, and the rung is `2 T u + T <= 2 W C` | 9.17 (7) (e) and (f): C accrues e_c at the set's own cell; T = P e_c | **MATCHES.** The six births wait within two intervals of (2 u + 1) P / (2 W) (BUILD item 24). |
| 22 | The excited record's norm T | `massive_record_margin.excitation_norm` 616-649: the sum of `form_share` at the centre over `period` intervals of the body advanced alone. The loader recomputes it and refuses a mismatch (714-732) | 9.17 (7) (e): T = P e_c; 9.18 (4) item 9 (the loader's check) | **MATCHES.** The refusal text at 725-730 still says "the one-way flux into the body's centre cell", which is the retired reading; the code computes the share. |
| 23 | The birth (X, then E^T) | `_emit` 826-956. `del self.records[own]` (X). The born record is written ONCE: `live.now[mask] = born[0]`, `live.before[mask] = born[1]` on every cell of the body. `live.norm = conserved_form(live)`; u and W from the clicking record's remainder at the centre; content one quantum from the stock; the next excitation is the profile again | 9.13, 9.17 (4) items 1 to 3, 9.17 (6) (the two-integer form) | **MATCHES** 9.17 (4) and (6). **CONTRADICTED** by 9.17 (6a): "THE BORN TRAIN, THE ONE FORM OF A BIRTH ... the two-integer form is refused with this reason". The engine accepts only that refused form (`world.py` 3736-3757, two integers with before = -now). |
| 24 | The born record's ladder by name | `_emit` 900-908: the emitter's `receiver` list in the named order | 9.19 (3) (b), 9.25 (4) | **MATCHES.** |
| 25 | The residue from the law | `residue_of` 730-742: u = r // g and W = wall / g at the centre cell, with g = gcd(num x scale, wall) | 9.19 (4), (4a), (4e); 9.22 (4) | **MATCHES** (W = 3 den / gcd(num, 3 den), the same as 3 den / gcd(num, 3) in lowest terms). |
| 26 | The loader for emitters | `world.py`: the coupling is required with both g and G nonzero (3638); the richness is at least 500 remainder values (3648-3660); the emitter is refused on light's kind or on a silent body; `lamp` is refused (4021); `RETIRED_KEYS` refuses by name `absorbing`, `take`, `emits`, `own_grace`, `wheel`, `residue_order` and `residue_seed` (1885-1909) | 9.19 (4a), (4d), (4e); 9.21 (1); 9.17 (3) | **MATCHES.** The 9.17 (7) (c) load condition (back-action <= seed / 1000, "refused above") is not built; BUILD item 24 says "NOT a refusal here". See table 2. |

### 1e. The reading, the click and the deletion

| # | Mechanism | Where | ALGEBRA.md | Verdict |
| --- | --- | --- | --- | --- |
| 27 | The flux (the one reading) | `flux_offer` 1179-1199 and `_flux_ports` 1153-1177: a Port is a Link to a Node of no set or of another set; no flux across a folded axis. `inward_flux` 1201. `kind_wall` 1143 (the least common multiple of the numerators). The levels are read after the step | 9.19 (3) (G_ij = (1/3) A_ij (now_i before_j - before_i now_j), the positive part); 9.25 (2) and (10) (a Link inside a detector is no Port) | **MATCHES** (the engine's units are 3 G x wall, consistent with 3 I x wall). |
| 28 | The conserved form and the Node's share | `conserved_form` 1230, `form_share` 1238-1253; `record_form` 1387 is the books' GAMEBOARD form | 8.2 (I and its remainder identity); 9.19 (3) (e_i); 9.17 (7) (e) | **MATCHES.** |
| 29 | The increment ladder | `_ladder_click` 1347-1385; `_ladder_of` 1333: the named sets in order, or the block's one receiver, or every detector set as declared, with `face` last. The click is at the first cell k where 2 W (C + f_1 + ... + f_k) >= (2 u + 1) T | 9.25 (2) and (3) (Born's rule a theorem); 9.19 (3) (b) as corrected | **MATCHES.** |
| 30 | The deletion | `_ladder_click` appends to `self.dead`; `step` 1641-1644 pops the record whole after the interval's advances; `_release` 1436 | 8.8 (the one deletion), 9.19 (3) (b), record 1888 | **MATCHES.** |
| 31 | The click line and the content handover | `_gather_line` 1447-1571: the content goes to the set's measured event, or is consumed at a set without a body or at the face. The HOST fields `taken_by_emitter` (0), `escaped`, and `click_at` "completion" are kept | 9.18 (4) item 5; 9.18 (5) and 9.21 (3) ("no place for ... `_complete`, the close, `escaped`"); 9.19 (3) (a) ("`escaped` is the face receiver's count") | **MATCHES** in act. **DIFFERS** in residue fields: the retired `taken_by_emitter`, `escaped` and "completion" labels remain as HOST fields, and a face click is booked as absorbed, not counted as the escaped row. |
| 32 | The face receiver as a slab | `__init__` 376-395: every open axis's border slab of `face_depth` free Nodes is ONE cell `face`, last on every ladder; `face_depth` defaults to 1 (`world.py` 1604, 5562) | 9.19 (3) (a); 9.25 (10): "every open face is a receiver slab of depth at least the record's length"; 9.25 (11) (b) | **MATCHES** in form. **DIFFERS** in the rule: the depth is not tied to the record's length (the default of 1 books about 0.15 of a packet, 9.25 (10)), and the placement rule (one train's length from every slab) is not checked. |
| 33 | Closed faces | Under `detector_law` a face may be declared `closed` (a zero row, no receiver). A board with no periodic axis and no face receiver is admitted; `world.py` 5586 refuses `closed` only without `detector_law` | 9.19 (3) (a): "A board with neither a periodic axis nor a face receiver stays refused" (record 15); 9.22 (3) | **DIFFERS.** The test worlds of BUILD item 14 are closed boards. |
| 34 | The detector as one connected cube | `world.py` `_detector_region` 5212, `_connected_pieces` 5149, `DETECTOR_SIDE` = 3 (5187); the engine maps a set to one cell over all its Nodes (`__init__` 350-373) | 9.25 (7) and (10) | **MATCHES.** |
| 35 | A set bound to a block (its cells or a cube beside it) | `__init__` 352-363 and 470-478; the stamp is the block's count (`rung_counts`) | 9.25 (10), 9.25 (11) (d) ("the detector is the source's own cells") | **MATCHES** as a set. The stamp uses row 37's count. |
| 36 | A block's cells booked to its own cell, never chosen | `__init__` 466-474 | none | **MISSING IN ALGEBRA** (a HOST sink of the bookkeeping; harmless). |
| 37 | The block clock | `_block_clock` 958-1011: a count when the sum of the block's records over its cells crosses from <= 0 to > 0; it writes a `click` line that deletes nothing and a `block` line, and gives the `clock` stamp | 9.17 (4): "Its 'click' is a count on the sum of its record (a crossing from at most 0 to above 0) that deletes nothing", named NOT the form; the algebra's clock of a body is its record's click at its rung (9.17 (7) (f), 9.26 (1a) (b)); 8.7 reads the clock by clicks at W | **DIFFERS / MISSING IN ALGEBRA.** The engine still writes a sign-crossing count named `click` for every block and stamps bound sets' lines with it. The algebra has no such clock. A non-emitting well (a clock row) has no rung-click at all in the engine. |

### 1f. Books, inverse, load checks, generator and command

| # | Mechanism | Where | ALGEBRA.md | Verdict |
| --- | --- | --- | --- | --- |
| 38 | Books | `books` 1674-1747: content per family balanced; the form is GAMEBOARD; momentum is "not accounted" | 9.20 (A) 3 (a) (content), 3 (b) (I); 9.15, 8.11 (momentum through the push) | **MATCHES** for content and form. Momentum books are missing (the push is not built). |
| 39 | The inverse step | `_advance_inverse` 1022 (the ceiling), `step_inverse` 1046: the reverse column order; refused if any block moves; no click and no birth | 8.8; 9.20 (A) 4; 9.26 (3) (a) | **MATCHES.** |
| 40 | The integer load checks | `world.py` `_initial_state_checks` 5061-5148: cells disjoint; the clock a / b above the band top and below 2; the residual `mode_residual` 4932 on the composed operator outside the other bodies' cells. `MOST_FAMILIES` = 3 (856, 2334). The input stamp `input_stamp` 4984 and `_input_stamp_check` 5013 with `LAW_IDENTIFIER` (861). `NORM_BOUND` 2^126 (359). The pace bound 3 P . P < (3 Q S M)^2 (3590) | 9.22 (3) and (7) (i) to (iv); 9.22 (7a) (i); 9.21 (8) (d) | **MATCHES.** Missing: the hybrid share, transparency, the holder-family rule, the born train's checks, the face depth and the refusal of `ramp` (table 2). |
| 41 | The spectral and margin checks | `massive_record_margin.check_margins` 543 (per body: runaway or not bound, the margin rule) and `check_body_conditions` 680 (the composed largest eigenvalue < 2 by float ARPACK via scipy; the seed equals the file's profile at both levels; the norm recomputed; the ramp required). Called from `run.py` 64-84 at run start, not by `load_world` | 9.19 (2): "THE LOADER'S CHECK is the spectral one"; 9.22 (7): load checks in integers; 9.21 (7) (d): float is HOST | **MATCHES** in content. **DIFFERS** in place and kind: a float check at run start, not an integer load check. The ramp requirement contradicts record 1884 (row 18). |
| 42 | The generator | `iterated_mode` 360, `_operator_step` 294: 3 den v' = num S_6(v) + 6 den v + r, with power-of-two renormalisation. The clock a / b is the Rayleigh quotient. The STOP is the first iteration whose scaled profile passes the loader's residual bound. ARPACK (`accurate_mode`) is only a diagnostic (BUILD item 25) | 9.22 (7): "the generator is the board's own operator, iterated"; 9.22 (7a) (ii): "DECIDED: the generator writes the accurate float mode and the integer iteration is the reproducible CHECK ... not the writer"; 9.27 (A) row 36: "the stop the shape unchanged within one unit at the peak's amplitude (the cross product with the peak)" | **MATCHES** 9.22 (7) and record 1924. **DIFFERS** from 9.22 (7a) (ii), which is not updated: it says the float writes. **DIFFERS** from 9.27 (A) row 36's stop: the engine's stop is the residual bound, and a one-unit stop was "READ AND REJECTED" (BUILD item 25). |
| 43 | The one command and the pins | `tools/run_inputs.py`: LAWFUL or REFUSED, one output per input, pins `count` and `first_click` only (96-101) | 9.22 (7); the pins' file form of 9.22 (8): count, first_click, mean_interval, cadence, ratio, sum, fringe, centroid | **MATCHES** in form. Six pin forms are missing (table 2). |
| 44 | GAMEBOARD readings | `step` 1645-1672: `probe` lines (the sum of light's `now` at declared Nodes); `mode` lines (the k = 2 pi / 3 sums under `mode_axis`) | 9.21 (4): a GameBoard reading is a diagnostic; 9.22 (8) (the pace fans' probe); 8.5 (the hop pump's signature) | **MATCHES** as diagnostics. The pump's `mode_axis` reads a moving-material effect the algebra retires. |
| 45 | Remnants of retired forms | `LiveRecord` `mask`, `arms`, `arm_done`, `labels` (`mask` is still applied at `_advance` 1315; `arm_done` is still checked at `step` 1598); the unused `_phase` 1014; `DEFAULT_TRAIN`; `Block.current`, `births`, `new_cycle`, `cycle_*`; the header docstring (1-51) still describes lamps, the take and `cell_of` at the close | 9.18 (5), 9.21 (3), 9.25 (5) item 5 ("the arm's half-space cut dies with the two-arm emitter") | **MISSING IN ALGEBRA** (dead code: no effect today, but not removed). |
| 46 | A dense array per record over the whole board | `LiveRecord.now`, `before` and `remainder` over the full shape | 9.21 (8) (e) (i): a host matter, OPEN | **MATCHES** (stated as a host cost). |

### 1g. The ray-law path (`NatureBeamSimulation`, `nature_beam.py`, `meeting.py`, `measured.py`), run by every world without `detector_law`

| # | Mechanism | Where | ALGEBRA.md | Verdict |
| --- | --- | --- | --- | --- |
| 47 | The flight and walk (the digital line, T_D, `_walk_rows`) and the collision or meeting table | `nature_beam.py` 911 (`direction_flight`), 1404, 1295 (`collision_table`); `meeting.py` | chapters 1 to 7 only; DESIGN.md 4.1 "not relevant"; 9.21 (2) "Retire: ... the headings" | **MISSING IN ALGEBRA** (the one algebra). Still live code. |
| 48 | The crowd and the age wall (the owed count at d against d + a_tau n) | `engine.py` 157 `count_owed`, `measured.py` 370-430 (`age_wall_set`, `age_wall_coefficient`); `suspension` | ALGEBRA 5.4 "the clock in a crowd" (chapter 5); the one algebra: none (see table 3, rows 7 and 8) | **MISSING IN ALGEBRA** (chapter 9). Contradicted by 9.22 (8a) and 9.27 (C) (ii). |
| 49 | The push and the drive, the optical turn and the flow label | `nature_beam.py` 3037 (`push_form`), 3828-3946 (`optical_*`); `engine.py` 122 (`step_axis`) | 8.11 (CARRIED); 9.21 (7) (a) (the push outside the one algebra); 9.21 (3) (no `_drive`) | **MISSING IN / CONTRADICTED BY** the one algebra. Live code. |
| 50 | The amplitude-v1 click (pointers on the cosine and sine tables, `cell_of` at the completion) and the half-angle rotations | `amplitude.py`, `nature_beam.py` 1860-1943, 2870 | 9.14, 9.18 (5), 9.21 (3): tables and `half_angle` retire | **CONTRADICTED** (retired by the algebra, still run by ray-law worlds). |

---

## Table 2. ALGEBRA -> CODE: every rule or tool the one algebra says the engine must have

The build steps are named as the build order names them (record 1924). They are:
- the travelling born profile;
- the packets with momentum and the moving name, with the ramp refused;
- the polariser's axis and the crystal;
- the cleanup order's step 5 (the loader's checks) and step 6 (the worlds rebuilt on bound tool bodies).

| # | Rule or tool (ALGEBRA.md) | Code | Verdict |
| --- | --- | --- | --- |
| 1 | The rule with a pair per record kind per Node (8.1, 9.18 (4) item 1) | `_advance` | **BUILT** |
| 2 | The conserved form I and its remainder identity (8.2) | `conserved_form`, `form_share`; property test 3 (b) | **BUILT** |
| 3 | A well: a lowered pair on declared cells, its clock the bound mode (8.3) | `_write_pair`, the loader, the margin module | **BUILT** |
| 4 | The coupling, first difference both ways, in the one division (8.5, 9.18 (4) item 2) | `_receive`, `_source` | **BUILT**, except the emitter's own born light (g only, table 1 row 16) |
| 5 | The invariant J with the cross term (8.5) | `tests/test_massive_record.py` (about 741); the property test world is uncoupled | **BUILT** (test), not in the property test |
| 6 | The inverse, the bijection except the click (8.8, 9.20 (A) 4, 9.26 (3) (a)) | `step_inverse` | **BUILT** (at rest) |
| 7 | The seed as the composed mode's integer profile at both levels, remainders 0 (8.7, 9.9, 9.22 (3)) | the loader, `_initial_state_checks`, `check_body_conditions` | **BUILT** |
| 8 | The stability (spectral) check, the largest eigenvalue < 2 (9.19 (2)) | `composed_largest_eigenvalues` (float, at run start) | **BUILT** (as a host float check, not in the integer loader) |
| 9 | The flux as the one reading; T = I (9.19 (3)) | `flux_offer`, `_flux_ports`, `conserved_form` | **BUILT** |
| 10 | The face receiver last on every ladder (9.19 (3) (a)) | `__init__` 376-395 | **BUILT** |
| 11 | A board with neither a periodic axis nor a face receiver refused (9.19 (3) (a), 9.22 (3)) | closed boards admitted under `detector_law` | **CONTRADICTED** (the cleanup's step 5) |
| 12 | The deletion whole at the click, at that interval (9.19 (3) (b), record 1888) | `self.dead` | **BUILT** |
| 13 | The increment ladder in the declared order (9.25 (2)-(4)) | `_ladder_click` | **BUILT** (tests: 128 planted residues, both orders) |
| 14 | The detector as one connected cube of side 3 or more (9.25 (7), (10)) | `_detector_region`, `_connected_pieces` | **BUILT** |
| 15 | The face slab (9.25 (10)) | `face_depth` | **BUILT** as a key |
| 16 | The face slab as deep as the record, one train's length from every tool (9.25 (10), (11) (b)) | not checked; default depth 1 | **NOT YET BUILT** (the worlds' rebuild on the eighteen's placements, step 6) |
| 17 | The residue from the law; W from the birth cell's pair; refuse declared residues and wheels (9.19 (4), (4d)) | `residue_of`, `RETIRED_KEYS` | **BUILT** |
| 18 | The richness of a birth cell, at least 500 (9.19 (4a)) | `world.py` 3648 | **BUILT** (emitters). The crystal's light pair is not built with the crystal |
| 19 | Every emitting body declares (g, G) for its born family (9.19 (4e) (i)) | `world.py` 3638 | **BUILT** |
| 20 | The excited record's residue read after its first advance (9.19 (4e) (ii)) | `residue_pending` | **BUILT** |
| 21 | The emitter as a clicking body: X then E^T, the stock in turn, no rate, no drive, no source term (9.13, 9.17 (2)-(4)) | `_excite`, `_emit`; `lamp` refused | **BUILT** |
| 22 | The excited record's rung by its own tick: C += e_c, T = P e_c (9.17 (7) (e), (f)) | `_excitation_rung`, `excitation_norm` | **BUILT** |
| 23 | Loader refusal: 6 g A sin(pi n / (d N)) <= seed amplitude / 1000 (9.17 (7) (c)) | not refused (BUILD item 24: "NOT a refusal here", held for the owner) | **NOT YET BUILT** (held for the owner's word, record 1923) |
| 24 | No table in the engine; born values are the world's integers (9.17 (6), 9.18 (5), 9.21 (7) (c)) | `_emit` writes `born`; no cosine or sine table in `detector_law.py` | **BUILT** (the detector-law path; the ray-law path still carries tables, table 1 row 50) |
| 25 | THE BORN TRAIN, the one form of a birth: a travelling character over at least 8 periods under the Hann window and tapers, K = pi / 2 ([512, 1]), `born` a profile at both levels; the two-integer form refused; at load the form, the flux sign along **K** and the hash (9.17 (6a), 9.25 (11) (a)) | only the two-integer uniform form is accepted | **CONTRADICTED** (the travelling born profile, awaiting the mathematician's integer form, records 1919 and 1923) |
| 26 | The born record's norm written beside the profile and checked at load (9.17 (6a)) | the engine computes `conserved_form` at the birth | **NOT YET BUILT** as a load check (same step) |
| 27 | Transparency of an emitting or receiving body to its born family at the born **K**, at least 0.99 (9.22 (7a) (iv)) | none | **NOT YET BUILT** (the travelling born profile and the cleanup's step 5) |
| 28 | The integer load checks: the stamp, the residual, the band, the remainders 0, disjoint cells (9.22 (7)) | `_initial_state_checks`, `input_stamp` | **BUILT** |
| 29 | The hybrid share of near-degenerate wells within the band (9.9 (3), 9.22 (3)) | printed nowhere as a refusal | **NOT YET BUILT** (step 5) |
| 30 | At most three families (9.18 (2), record 1875) | `MOST_FAMILIES` | **BUILT** |
| 31 | The holder family: a tool body's family differs from every family the tool acts on or reads; refused otherwise (9.18 (2), 9.22 (3)) | not checked | **NOT YET BUILT** (step 5) |
| 32 | One border for every family (9.18 (2), 9.21 (7) (b)) | the per-family `faces` key | **CONTRADICTED** (step 6) |
| 33 | Tool bodies BOUND, of the holder family, carrying a light pair on the same cells; the silent body retired (9.18 (1), A.10, A.12) | a block has one family; the mirror is a silent light-kind block | **NOT YET BUILT** (step 6); the silent form still used |
| 34 | A body carrying a pair for each of two families on the same cells (9.18 (7), A.8 the transponder) | no | **NOT YET BUILT** (step 6) |
| 35 | The polariser: an integer axis (a, b), **M**_u on the label rows, two receivers (9.14 (b), 9.16 (2), A.5) | tables refused; no label rows | **NOT YET BUILT** (the polariser's axis and the crystal); Malus worlds held |
| 36 | One amplitude per label on every record, the label rows (9.16 (2)) | one row per record | **NOT YET BUILT** (same step) |
| 37 | The crystal: E, m^T, E^T; the pair born by an arriving record's click; the rich light pair at its cells (9.13, 9.16 (5), 9.19 (4a), A.6, A.11) | none | **NOT YET BUILT** (same step); Bell worlds held |
| 38 | The pair of rank 2: one residue, per-arm time, the joint ladder R = J^2, o_A outer (9.23 (1), 9.25 (6)) | `arms` and `labels` remnants only | **NOT YET BUILT** (same step) |
| 39 | The joint body, optional (A.13, 9.23 (3)) | none | **NOT YET BUILT** (optional, record 1890) |
| 40 | The push: the stress at the outer Ports into the body's vector, then (D), then (T) (8.11, 9.15 (ii), 9.18 (4) item 7) | none; momentum books "not accounted" | **NOT YET BUILT** (CARRIED and "retiring" in 9.24 (3) (b); outside the one algebra per 9.21 (7) (a)) |
| 41 | No ramp; material does not move (9.22 (2), 9.24 (3), (5)) | `ramp` admitted and required on moving bodies; `_move_block` hops | **CONTRADICTED** (the packets with momentum and the moving name, with the ramp refused) |
| 42 | Every entry carries **K**; a packet written at interval 0 as the profile times the character of **K** (9.22 (2)-(3), 9.24 (2), record 1885) | a seed has equal levels (`now = before = profile`); no packet key | **NOT YET BUILT** (same step) |
| 43 | The moving name: a set S(t) translating at v_g(**K**) by an accumulator (9.24 (4), A.14, record 1889) | none | **NOT YET BUILT** (same step) |
| 44 | Property test (B) 1, 2, 3 (a) (b), 4, 5, 6 (9.20) | `tests/test_board_properties.py` 1 to 6 (plus 7 host cost and 8 same input) | **BUILT**; 24 of 24 pass here |
| 45 | Property test (B) 3 (c): a plane wave's **K** constant on a homogeneous board (9.20) | not in the test | **NOT YET BUILT** |
| 46 | Property test (B) 7: no signalling, Alice identical under Bob's two axes (9.20, 9.25 (6), (8)) | no crystal or polariser | **NOT YET BUILT** (the polariser's axis and the crystal) |
| 47 | Property tests "per family and together" (9.20 (B), (C) coupled) | the property world has no coupling | **NOT YET BUILT** for the coupled families (the J test exists elsewhere) |
| 48 | The retirements of 9.18 (5) and 9.21 (3): `_drive`, the lamp, `_source` as a birth, the grace, the exemption, the own take, the take masks, `_complete`, the close, `TableBody`, `read_pair`, `half_angle`, `Splitter`, the residue orders | removed from `detector_law.py` | **BUILT** (detector-law path). Remnants: `escaped` and `taken_by_emitter` (HOST 0), `arms`, `mask`, `arm_done` (table 1 rows 31 and 45) |
| 49 | No `massive_kind` branch in the law's path (9.18 (5), 9.21 (3)) | `_advance` 1276, `step` 1601, `step_inverse` 1060 | **CONTRADICTED** |
| 50 | No projection in the law (9.12); the cavity replaced by a gap (9.10 item 4) | the cavity zeroing in `step` 1591-1593 | **CONTRADICTED** |
| 51 | The pins' forms: mean_interval, cadence, ratio, sum, fringe, centroid (9.22 (8)) | `run_inputs.py` has count and first_click only | **NOT YET BUILT** (the eighteen's input files with their pins) |
| 52 | The generator is the operator iterated, with the stop (9.22 (7), record 1924) | `iterated_mode` | **BUILT** (with the stop stated differently from 9.27 (A) row 36; table 1 row 42) |
| 53 | Arbitrary-precision ladder integers (9.21 (8) (d)) | object arrays, `NORM_BOUND` 2^126 | **BUILT** |
| 54 | The exchange hypothesis, the key `hypotheses: {"exchange": true}`, off by default (9.27 (D)) | none | **NOT YET BUILT** (a hypothesis outside the law, stated after `a9ab486f`) |

---

## Table 3. The small laws found on the board, against the one algebra

Legend: **(a) REFLECTS** (section and formula), **(b) RETIRES** (by which record or section, and why), **(c) DOES NOT MENTION**.

### 3a. How a beam splits

| # | Law found on the board | Source | Verdict |
| --- | --- | --- | --- |
| 1 | **The split at a Node.** A record's amplitude spreads to the six neighbours every interval. In the ray law a row splits through the collision or Grover coin (record 1298); in the detector law "the ray splits at every free Node" (DESIGN.md) | DESIGN.md 1-2; record 1298; `nature_beam` collision table | **(a) REFLECTS** as the rule itself: 8.1 "3 den a_next + r' = num S_6 - 3 den a_before + r"; A.0 "**R**, THE RULE: the split at every Node". The ray law's coin and digital line are **(b) RETIRED** (DESIGN.md 4.1 "not relevant"; 9.21 (2) the headings). |
| 2 | **The split at a splitter.** A one-Node layer of light's pair. The first draft's [91, 107] split 3 : 1 at the true clock | LAB_TOOLS.md A.4; records 1531, 1903 | **(a) REFLECTS**, A.4: "abs(r)^2 = delta^2 / (delta^2 + (2 h sin q)^2)", "delta = 6 cos(omega) (d / p - 1) divided by h". The exact half is "abs(r)^2 = 1 / 2 EXACTLY for d / p = 3 / 2, the pair [2, 3]" at k = pi / 2. At 45 degrees the share equals normal incidence "for every k and every pair". The splitter's table and linear form are **(b) RETIRED** (9.18 (5)). |
| 3 | **The split at a slit or opening; the fringe spacing** | 9.25 (10); records 1356, 1894, 1903 | **(a) REFLECTS**, 9.25 (10): "DELTA y = 2 pi L / (d sin k_x)", which at k = pi / 2 is 1.571 times the continuum's lambda L / d (53.2 cells), "a grain term named". The ray law's fan by angle (Huygens on the lattice, records 160 and 163) is **(b) RETIRED** (DESIGN.md 4.2: "the opening's fan by nothing (an opening is a hole)"). |
| 4 | **The mirror's reflection and delay.** The gap [1, 2] transmits 1.006 x 10^-2 at depth 1; the delay is +0.516 intervals over the zero row's 3.491 (2 / v_g) | A.3, A.9 | **(a) REFLECTS** (A.3's COMPUTATION; the faces' "2 / v_g referred to the last free Node"). |
| 5 | **A flat born pulse sloshes: its one-way flux exceeds its norm, 4.65 T beside the emitter** | BUILD.md 26 items 9 and 22; record 1919 | **(a) REFLECTS**, 9.17 (6a) and 9.25 (11) (a): "the positive part of an alternating current grows without bound ... the click of (2) is Born's rule for a record that PASSES its detectors, and only for it". The algebra's remedy (the born train) is not built (table 2 row 25). |
| 6 | **A face one Node deep books about 0.15 of a packet and reflects the rest** | BUILD item 23 (the board reading: over 0.9 into a slab 40 deep, under 0.5 into one Node) | **(a) REFLECTS**, 9.25 (10): "a slab of depth D books 0.15 at D = 1, 0.29 at 4, 0.52 at 8, 0.83 at 16, 0.96 at 32 and 0.995 at 64". |

### 3b. The pace: band, cone, direction and mass

| # | Law found on the board | Source | Verdict |
| --- | --- | --- | --- |
| 7 | **The pace by direction: the axis above the diagonal by k^2 / 48 at a fixed omega** | records 1597, 1618, 1903; the pace fans (5a) | **(a) REFLECTS.** 9.17 (4) item 5: "k(axis) - k(diagonal) = k^2 / 48 at fixed omega is a property of the band that holds per character". 9.22 (8a): "omega = (k / sqrt 3) (1 - (k^2 / 72) (3 sum n_i^4 - 1))"; the group pace is "(1 / sqrt 3) (1 - (k^2 / 24) (3 sum n_i^4 - 1))". 9.22 (8) pace fans: the diagonal's 1.4810 per Link and the group pace 0.5477 against 0.4472 at k = pi / 2. 9.25 (9): "the pace fans read k^2 / 48, the lattice's own anisotropy, a diagnostic by construction". The flight table's direction paces (c_D, 32 / 55 on a heading) are **(b) RETIRED** (AUDIT F91, F112). |
| 8 | **The band and the cone** | 8.1; records 1405, 1410 | **(a) REFLECTS**, 8.1: "2 cos omega = (2 num / (3 den)) (cos k_x + cos k_y + cos k_z)", "cos omega = cos omega_0 cos omega_l(k)"; c = 1 / sqrt 3; "c_m^2 = cos omega_0 c^2", "c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2". The ray law's cone test (record 144, the flight) is **(b) RETIRED**. |
| 9 | **The massive family's slower pace and its group velocity** | 8.1, 9.24 (2); records 1889, 1903 | **(a) REFLECTS.** 9.24 (2): "the group velocity per axis v_i = (numerator / denominator) sin k_i / (3 sin omega)"; "The effective mass 1 / omega'' at rest is 3 sin omega_0 (denominator / numerator)". The limiting pace deficit is omega_0^2 / 6 (c_eff) to omega_0^2 / 4 (c_m) (9.22 (8a)). v_g is 0.4384 for matter at K = pi / 2 against 0.44721 for light (9.22 (8)). |
| 10 | **A moving body's tick: 0.8146 at k = 3 (v = 1 / 3)** | records 1889, 1895, 1920; 9.24 | **(a) REFLECTS.** 9.24 (2): "the packet's own tick is slower than the rest tick by (omega(**K**) - **K** . **v**) / omega_0. TIME DILATION ARISES FROM THE DISPERSION"; "0.81457 against 1 / gamma = 0.81650". 9.26 (1): "omega - K d omega / d K = omega_0^2 / omega on the cone". 9.22 (8a): gamma at the kind's own cone c_eff, and a lattice term 0.41 K^4. **(b) RETIRED** by 9.24 (5), (2) and AUDIT F69: the older well form 0.8116, where 8.4's "f / f_0 = omega_b(gamma_m s, g_w) / (gamma_m omega_b(s, g_w))" is "HISTORY for a moving well"; also the ray law's "r = 1 at every speed". |
| 11 | **The bound clock's second term, eps (gamma_m^2 - 1) / 2 below 1 / gamma_m** | 8.4, 8.9 prediction 2 | **(b) RETIRED** as the well form (9.24 (5)) and replaced. 9.22 (8a) re-derives the "bound clock's second term" as the cone's beta^2 gamma^2 omega_0^2 / 6 plus the lattice's 0.41 (K a)^4. 8.9 still lists the old term as prediction 2, uncorrected. |
| 12 | **The moving light clock: gamma across the arm, gamma^2 along it** | records 1889, 1895 | **(a) REFLECTS** gamma across (9.24 (6)). The longitudinal gamma^2 is **(b) RETIRED** as a prediction (record 1895; 9.24 (7) (iii): "the model has clocks and no rods"). |

### 3c. Doppler, redshift and the index

| # | Law found on the board | Source | Verdict |
| --- | --- | --- | --- |
| 13 | **Doppler 1 +- v / c from the crossing rule; the receding emitter's redshift; the round trip** | DERIVATIONS_BEAM 2; records 153, 158 | **(a) REFLECTS** in a new form. 9.22 (8): "1 + z = (1 + v / c_l) / (the tick ratio) = ... 2.141 at v = 1 / 3"; the round trip is "(1 + beta) / (1 - beta) = 6.856 at beta = v / c_l". Both run with the moving name, which is not built. The crossing rule itself is **(b) RETIRED** (flights; AUDIT F172, F173). |
| 14 | **The index of a medium** | 8.5; records 1338, 1400, 1405 | **(a) REFLECTS** at a coupled body's cells only. 8.5: "n^2 = 1 + G g / (omega_0^2 - omega^2), the classical dielectric" (COMPUTED, NOT PROVED); in motion G g is carried as [K^2, K^2 - 3]. The pinned rows are OPEN: 9.22 (8) receding index, "at the train's omega = 0.841 ... the coupled index lies below 1 ... the row is re-derived". The ray law's "light in a crowd" (the index as the crowd's age, the optical turn) is **(b) RETIRED**. DESIGN.md 4.1's crowd index n_c = (d + f n A) / d is **(c) NOT MENTIONED** (see row 15). |

### 3d. Mass, the crowd, fields and gravity

| # | Law found on the board | Source | Verdict |
| --- | --- | --- | --- |
| 15 | **The crowd at a Node stretching a clock (the old age wall).** The owed count at d against d + a_tau n; the tick outside per tick inside r_D = d / (d + A n) | Highlights 5.4 "The one wall"; record 1248; ALGEBRA 5.4 ("its rate is 1 / (1 + k_crowd), k_crowd = a_tau n / d (SHOWN ...)"); DESIGN.md 4.1 (the coefficient form q = [d^2, (d + f n A)^2] under the detector law, never built) | **(b) RETIRED** in the one algebra, without naming the age wall. 9.27 (C) (ii): "the law is linear: two records on one board never act on each other, the only nonlinearity being the click". 9.24 (3) (a): a pair following a record "would have to be a function of the holder record's amplitude there, a term of degree two ... REFUSED by the three tests (PROVED)". 9.22 (8a): "the vacuum around a body carries the vacuum's pair". The equivalent rule is named only as a hypothesis outside the law: "the pair-field hypothesis" (9.22 (8a), 9.27 (C)) and 8.5's "`gravity-index-hypothesis`, with no number". **Conflicts to resolve:** Highlights 5.4 still carries "The one wall" row ("the one wall stretches the local pace at a Node (the design's 4.1)"). Its observed-values table still reads "a mass ... the clock's slowing near it (series E)". ALGEBRA chapter 5.4 still states the crowd clock as SHOWN. The engine still runs `count_owed` on every ray-law world. |
| 16 | **The delay field and the retarded potential** | DERIVATIONS_BEAM 5.1-5.3; records 168, 213, 1580 | **(b) RETIRED.** 9.22 (8a): "no field stands in the vacuum around a body". AUDIT: "No longer in the list: ... the delay". Record 1580 moved them to records.tex as history. The one algebra keeps retardation only as the rule's own locality ("a change at one Node reaches Manhattan distance m at interval m and no further", 9.20 (A) 5), not as a potential of mass. |
| 17 | **Gravity's forms under a shell average (Newton, Poisson, Coulomb's inverse square)** | ALGEBRA 5.6; DERIVATIONS_BEAM 3; record 1915 (the sixth computed experiment) | **(b) RETIRED** explicitly. 9.22 (8a): "gravity's forms are NOT the algebra's ... in its place the UNIVERSALITY OF THE TICK"; "Newton's inverse square under a shell average and Poisson's equation are therefore not limits of the algebra". 9.27 (A) row 32: "DIFFERS ON THE SIXTH", with the owner's yes owed. |
| 18 | **The gravitational redshift: a clock near a mass runs slow (series E)** | log record 07; DERIVATIONS_BEAM 5.2; ALGEBRA 5.1 and 5.4 | **(b) RETIRED** by 9.22 (8a), "the algebra has no gravitational field". It is replaced by the universality of the tick (constitution term (omega_0a^2 - omega_0b^2) beta^2 gamma^2 / 6 plus a direction term of order (K a)^4). |
| 19 | **Light bending 2 (1 + gamma_PPN) and the Shapiro delay** | ALGEBRA 5.9 | **(b) RETIRED.** 9.22 (8a): "light passing beside a body is not bent". AUDIT F101, F115. |
| 20 | **A heavier block steps slower for the same momentum (the drive's wall 3 Q S M)** | 8.11; `_move_block` | **(b) RETIRED** by 9.24 (3) and 9.22 (2) (material does not move; no ramp). It is still in the engine (table 1 row 18). |
| 21 | **The force between two blocks through light, 2 A^2 cos(k_0 L)** | 8.11; PUSH_BALANCE.md | **(b) RETIRED** as law. The push is "not in the one algebra" (9.24 (3) (b)). 9.27 (D) restates a momentum exchange as a hypothesis outside the law ("WHAT IT DOES NOT GIVE: attraction, gravity or binding"). |

### 3e. Other laws found on the board

| # | Law found on the board | Source | Verdict |
| --- | --- | --- | --- |
| 22 | **The hop's parametric pump at K = 3** | 8.5, 8.9 prediction 4 | **(b) RETIRED** implicitly, with moving material (9.24 (3); AUDIT F73 "out"). 8.9 still lists it as a prediction, uncorrected. |
| 23 | **E = h f from the release** | DERIVATIONS_BEAM 6.4 | **(b) RETIRED.** 9.26 (1): "The algebra has no E = h f: nothing in the law ties a record's form to its rotation"; 9.27 (A) row 38 "DIFFERS". |
| 24 | **Born's rule and the click's square (a lattice Gleason argument)** | DERIVATIONS_BEAM 6.5; record 185 | **(a) REFLECTS** in a new form. 9.25 (3): "P(cell i) = C_i(infinity) / T ... THE DETECTOR'S SHARE OF THE RECORD'S TOTAL INWARD FLUX". 9.22 (8a): "the exponent is 2 because the conserved form is of degree 2". |
| 25 | **Malus a^2 / (a^2 + b^2); Bell's S = 14 / 5 on integer axes; Tsirelson's limit** | 9.14 (b), 9.16 (4); records 1853, 1858 | **(a) REFLECTS** (9.16 (4), 9.19 (4b), 9.22 (8a)). It is not runnable on the engine (table 2 rows 35-38). The earlier 181 / 64 is **(b) RETIRED** (9.21 (9)). |
| 26 | **Bohr's levels, and atomic lines at mode differences** | DERIVATIONS_BEAM 7.2 | **(b) RETIRED** and contradicted. 9.22 (8a): "the algebra's atom emits at its modes' own rotations, nature's at their differences" (DISAGREE, stated). |
| 27 | **Light cannot be a body** | 8.3 | **(a) REFLECTS** (8.3, PROVED: the norm bound "<= 1 x 6 / 3 = 2"). |
| 28 | **The cube's binding threshold g_c(s) s^2 -> 2.190; the smallest binding cube** | record 1410; 8.3 | **(a) REFLECTS** (8.3, COMPUTED, NOT PROVED). 9.22 (9): "a side of 16 is bound ... sides 2 to 10 are not bound in the large-board limit". |
| 29 | **The runaway well (2 cos omega_b >= 2)** | BUILD item 8 | **(a) REFLECTS**, 9.19 (2): "a mode with 2 cos omega >= 2 grows without bound (the physicist's 'runaway well' ...)". |
| 30 | **The remainder's range and one residue per reseed without back-action** | BUILD items 15 and 19 | **(a) REFLECTS**, 9.19 (4): "AT MOST 3 x denominator / gcd(numerator, 3) values"; 9.19 (4e) (i): "a deterministic law with an identical start gives an identical cycle". |
| 31 | **A standing mode has no flux (the Wronskian)** | BUILD item 19 (the front-loaded cadence) | **(a) REFLECTS**, 9.17 (7) (a): "the flux G_ij ... VANISHES IDENTICALLY for a bound standing mode"; its share "e_i = D_i p_i^2 sin^2 omega" is constant. |
| 32 | **Two wells on one board split exactly; the beat period** | record 1929; 9.22 (7a) (v) | **(a) REFLECTS**, 9.22 (7a) (v): "lambda_+ - lambda_- = 2 lambda_0 t_12 / M_11". |
| 33 | **The Inside cycles exactly; the exact-return periods 3, 4 and 6** | records 1922, 1932 | **(a) REFLECTS** (9.26 (4) (b), (4a)). |
| 34 | **The Mach-Zehnder dark port and the Sorkin sum** | records 1891, 1911 | **(a) REFLECTS** (9.22 (8): the dark share 0.0054; Sorkin S = 0 +- 284). |
| 35 | **The Hubble deceleration and cosmology rows (q, the law's own crowd)** | ALGEBRA chapter 6; `hubble*` worlds | **(c) DOES NOT MENTION** (chapter 9 is silent; chapter 6 stays as FAIL-row text). |
| 36 | **The quarks and the nucleus as family-table rows, binding through the table** | 9.27 (C) | **(b) RETIRED**, 9.27 (C): "HISTORY with the tables and the take"; "a bag with no colour, no confinement and no mass of its own". |

### 3f. Special care: does mass change the local pace, and so the times?

1. **What "mass" is in the one algebra.** A family's mass is its pair: "cos omega_0 = num / den ... nothing else names the mass" (8.1). A body's mass is the lowered pair declared on its cells (8.3). The number of quanta changes nothing in the step. The law is linear (9.24 (1)), and "the same rotation at twice the amplitude is one record still, with four times the form" (9.26 (1)). "The quantum is counted, not weighed" (9.17 (7) (c)).

2. **Where the pair does change the pace and the times (REFLECTED).**
   - (i) A record of a massive family travels more slowly: "v_i = (numerator / denominator) sin k_i / (3 sin omega)" (9.24 (2)). Its limiting pace is c_m or c_eff below c (8.1). So first-click and passage times depend on the family's pair: "(41 + 16 + 2) / 0.4384 = 135 +- 5" (9.22 (8), the moving mass's energy).
   - (ii) A body's own clock is set by its pair and extents: "a body's frequency is its bound mode's own rotation, set by the body's pair and extents and by nothing outside it" (9.26 (1)). The emitter's births come one per half period of that rotation (9.17 (7) (b)). A heavier family has the FASTER rest rotation omega_0 = arccos(num / den), the Compton sense. A well lowers omega_b below omega_0.
   - (iii) At a coupled body's cells the medium has an index for light: "n^2 = 1 + G g / (omega_0^2 - omega^2)" (8.5). Light is delayed there only.
   - (iv) A moving packet's tick slows by its own dispersion (0.81457 at v = 1 / 3, 9.24 (2)).

3. **What does NOT exist in the one algebra: gravitational time dilation.** A clock does not run slow near a mass.
   - 9.22 (8a): "GRAVITY, for the record: the algebra has no gravitational field. A body's coupling (g, G) acts at its own cells on the families it is coupled to (the index of a medium, the back-action of an emitter, 9.19 item (4e)); the vacuum around a body carries the vacuum's pair; light passing beside a body is not bent and a second body is not drawn."
   - 9.22 (8a): "no field stands in the vacuum around a body, so an inverse square or Poisson's equation would need the pair-field hypothesis, which spreads a body's pair into its neighbourhood, a hypothesis under its own identity and no computation of the algebra".
   - 9.27 (B): "the law has no force of one body on another (the coupling of 9.19 (4e) is a body's to light alone)".
   - 9.17 (7) (b): "the light on the board neither hastens nor delays it (no stimulated emission in the law ...)".
   - 8.5: "Gravity as an index of the crowd's massive records is a hypothesis outside the law under its own name, `gravity-index-hypothesis`, with no number".
   - So the only time effects are those in point 2: the index of a medium at its own cells, the massive family's own band and group velocity, a body's own clock, and motion's dispersion. The "universality of the tick" replaces gravity's row (9.22 (8a)).

4. **In the engine today (emitter-click).** A Node's pair enters the step (`kind_num` and `kind_den` in `_advance`) exactly as above. No quantity at a Node depends on how many records or quanta are there. The content M (`amount`) enters the physics only through the block's drive wall 3 Q S M (the hop cadence of a moving block, `_move_block`) and the coupling-in-motion pair (`motion_pair`). Both are mechanisms the one algebra retires (table 1 rows 17 and 18).
   - The only clock-near-mass mechanism in the code is the ray law's `count_owed` (the age wall at `suspension` [n, d]). It still runs in every world without `detector_law`. It is stated in ALGEBRA chapter 5.4 and Highlights 5.4 "The one wall", and absent from the one algebra.
   - DESIGN.md 4.1's detector-law form of the wall (the pair [d^2, (d + f n A)^2] at a crowded Node) was never built and is not named in chapter 9.

---

## Gaps for the mathematician and Nature24, in one list

1. **The born train.** The engine's only birth form is the one 9.17 (6a) refuses.
2. **Moving material and the ramp** are live in the engine and required by `check_body_conditions`; the algebra forbids both. The packets with **K** and the moving name are not built.
3. **Kind branches** on `massive_kind` remain in `_advance`, `step` and `step_inverse`.
4. **The cavity's per-interval projection** remains.
5. **Closed boards** are admitted.
6. **Faces per family** remain.
7. **Mirrors are silent light-kind blocks**, not bound holder bodies.
8. **The coupling to the emitter's own light is g only**, so there is no J for that pair. Other bodies' light never reaches an excited record (it drives separate response records), so it cannot spread that record's residues.
9. **`_block_clock`'s sign-crossing `click`** still stamps bound sets. It is not in the algebra, and a non-emitting clock well has no rung-click.
10. **Loader checks not built:** the 9.17 (7) (c) back-action refusal (held for the owner), transparency, the hybrid share, the holder-family rule, and the face depth against the train's length.
11. **Not built:** the polariser's axis, the label rows, the crystal, the pair of rank 2, the push and momentum books; property tests (B) 3 (c), (B) 7 and the coupled "together" case; six pin forms.
12. **Algebra text not updated:**
    - 9.19 (3) (c) and its bullet (the excited record's T as the flux into the centre cell) contradict 9.17 (7) (a) and (e).
    - 8.6 still describes the take, the motion-squared pointer and the emitter's own take.
    - 8.9 still lists the pump and the old second term.
    - 9.22 (7a) (ii) says the float writes the seed.
    - 9.27 (A) row 36's stop differs from the engine's.
    - Chapters 1 to 7 (the crowd clock, the shell mean, the delay) are not marked as retired by 9.22 (8a).
13. **Documents and environment:**
    - Highlights 5.4 still carries "The one wall" and "a mass ... the clock's slowing near it".
    - `docs/ENGINE.md` still calls `beam-v1` the one engine and describes the retired take, grace and line-at-the-rung as current.
    - The repository `.venv` lacks the declared dependency `scipy`, so `tests/test_board_properties.py` fails at import without it.
