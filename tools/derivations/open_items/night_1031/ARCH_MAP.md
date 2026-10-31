# ARCH_MAP: every part of the architecture with its derivation, for Sofer (the architect, 2026-10-31, 06:2x UTC)

The owner's word (06:2x UTC): "Verify with Sofer that the architecture is synced to where we stand, and that every
part of the architecture has its derivation. The derivation means: how it is explained in the clock, how it is
explained in the algebra, and how it is in the click world." This map is read only: no repository file was edited.

S below is /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad.

## What was read

- docs/ARCHITECTURE.md on origin/scribe-5 5c65e7ab9 (06:06 UTC, 417 lines), copied whole to S/arch_map/src/. Every
  "line N" below is a line of that file. docs/ENGINE.md is not on scribe-5 (it left the tree on 2026-10-30, line 403).
- The night's map: S/arch_night/ (FULLPIC, MAP, NOT_CLOSED, PLAN, STRENGTHS, TEXTS_INDEX, MAIN, BUILD, FRAMES) and
  origin/boss-derive 19963dd97 night_1031/ (FULLPIC.md, MAIN.md, texts/INDEX.md, byte for byte the scratchpad's).
- The owner's words and rulings: S/BRIEF_PAIRS.md whole (to the owner's words of 06:1x UTC), S/onelaw/KEY2.md,
  S/third/THIRD6_mode4.md.
- The texts and their readers' reports in S/ (folders named in each block), with their verdict lines.
- The code, by git show only: node-live 1794d474b; node-half 0893f2f28; node-onelaw 08c66fd40; node-edge 88b4d281c;
  node-third d9ad5f6aa; node-third-readings 3a446e77a (06:02, on top of node-third); bigpic-3clicks 9c78397e5 (a probe
  beside the act, nothing in src). node-all is not on origin: writer G's local tree S/nodeall stands at c78b202e9 with
  two of four merges (node-half, node-onelaw), unpushed.

## How to read a block

- **Part:** the module and its functions on the branch where built, or "not built".
- **Texts:** each derivation text, its status and its readers. DERIVED or PASSED means both hostile readers passed it;
  NOT PASSED means its pair refused it; DRAFTED or OPEN means no pair has passed it. Paths are given.
- **Clock / Algebra / Click world:** the three views, a few sentences each, or OWED where no text gives the view.
  "n/a (stated)" means a text says the part has no click of its own; it counts as given. "A board check" means the
  reading is read against board fields. A click-world view counts as given only where the decoder shows something of
  the part from the record of the act as built; where the only reading waits on a missing part (a clock's own count,
  light's click lines, a mass reading), the view is OWED and the missing part is named.
- **Synced?** whether docs/ARCHITECTURE.md says it as the code and the texts now have it, with each stale line.
- On the board there are only clocks. Light and matter are what the decoder shows in the click world; every mention
  of them below is a click-world reading, owed or shown, or a document's quoted name.

## Verdict

- **68 parts mapped. 49 have all three views; 19 OWE at least one.** Of the 49, 11 stand on a click view of n/a
  stated by its text and 3 on a board check (measure.py, D8's cone, the passings and weights). Of the 19, 18 owe the click-world view alone and one, the empty readings
  package, owes all three.
- **The click world is where the derivations stop.** Only the first click (its books edge by edge), the split's
  structure at a place, the third click's necessary readings (R2 within one record, the swap, two records compared)
  and the decoder's own readings show anything from the record alone. Every reading that needs a clock's own count
  (FACE2, not built), light's click lines (no echo rule) or a mass reading is owed, so terms 2 to 6, 9, 10 and 13 owe
  their click-world view.
- **64 lines of docs/ARCHITECTURE.md are out of date** (list K at the end). The largest gaps: term 11 on the edges and
  schema 1.4 (node-edge), ONELAW3's three built pieces (node-onelaw), the decoder's sides guard and three-click
  readings (node-third, node-third-readings), the strengths rule against lines 177 to 189, G2's, G3's and terms 6, 12
  and 13's statuses in lines 108, 163, 164, 334, 395 and 397, and the night's last texts in line 359 (KEY2, HAT4,
  DECODE3d, VARY1, SPLIT2b, mode 11). The law of the path, in docs/ALGEBRA.md at line 1964, is not in
  ARCHITECTURE.md.
- **Code built on branches but not in ARCHITECTURE.md:** decoder/sides.py and decoder/three.py; term 11 on the edges
  and the Mesh's edges; schema 1.4; ONELAW3's (b), (c) and (d); node-half's lifts, spun trains and kept forms named only
  in passing; five test files (list at the end).
- **What no text has passed yet and is built:** decoder/three.py stands on DECODE3 to DECODE3d, each NOT PASSED by
  both readers, folded by the Boss's rulings; the across guard and the Mesh's edges are unread by a code reader.

## A. The modules of src/tensor24

### M1. algebra/carry.py
- **Part:** carry, flip, lit; node-live 1794d474b, the same on every branch.
- **Texts:** the law's own (docs/ALGEBRA.md lines 46 and 100 to 102); no pair is asked of it. The audit of main
  (boss-derive night_1031/audit/) NOT PASSED, its fixes on node-live.
- **Clock:** a dial counts a push in whole turns of its teeth; what it cannot hold stays at the gear as its fine tooth.
- **Algebra:** n + r = q d + r' with 0 <= r' < d, the one division; flip is the mirror's w - 1 - r; lit is the zero
  test by one carry.
- **Click world:** the click is this quotient: every q on a click line is a carry's quotient, read as it stands (a
  give below 0, a take above). Reading the carry's law back from schema 1.4's sides, x = D q + k_after - k_before
  (decoder/three.py's passing), is a board check, since D and the teeth are board fields.
- **Synced?** yes (lines 244 to 250). The docstring's "a click will be such a quotient ... (G5)" is the code's tense,
  not the document's.

### M2. engine/step.py
- **Part:** node-live: split, gear, drive, readings, sources, stress, kick, driven, valued, passing, weight, halves,
  dials, grips, act, tick, mirror, untick. node-edge 88b4d281c: passing rewritten on the edges between trains, and
  crossing (the Mesh's edges). node-onelaw 08c66fd40: weight contracts the clocks' Plan of any number of legs.
- **Texts:** EDGE2.md and EDGE3.md (boss-derive derive/boss/edge/; DERIVED by its first and final pair); COUNT5.md
  (boss-derive derive/boss/click25/; DERIVED for the pair at one Node-clock); DAVID-TENSOR24-TERM7-DRIVE.md (toys-5;
  DERIVED by both end readers); NC29b.md (S/nc29/; PASSED by both, S/hf_math/REPORT_NC29b.md and
  S/hf_phys/nc29/REPORT_NC29b.md); ONELAW3.md (boss-derive night_1031/onelaw/; PASSED by both as a reading, its (b)
  built); LIGHT1.md (S/onelaw/; NOT PASSED by both, S/light1_math/ and S/light1_phys/REPORT.md, its sections 1 and 3
  found sound, the ground of crossing); EDGE1.md (S/onelaw/; DRAFTED, no reader). Code readers: S/hcr8/REPORT3.md
  PASSED 1794d474b..50af24bde; 88b4d281c and 08c66fd40 sit with the ninth reader (S/hcr9/), no report yet.
- **Clock:** every round every gear moves once: its six neighbours pull it, the coupling pushes it, its momentum is
  carried to the next edge and split there in one dial of both slots' teeth; the drive carries the push the same way.
  On node-edge every edge between two clocks holds one pair of teeth born complementary, so what leaves one side
  enters the other in the same round; the Mesh's edges do the same for two trains across one Mesh.
- **Algebra:** D_in = W(b) + W(a); N = 2 (D_in (a - b) + 2 (s F + K)) + s; q, s+ = split(N, 2 D_out) with
  D_out = W(a) + W(a+); a+ = a + q, b+ = a. Term 11 on node-live: S = X(a, b) + X(a+, a), q, k+ = carry(S, key, k)
  per train. On node-edge: W_i = J_i(a) (a+ - b) scattered onto each partner, P(t, u) the given less the taken, so
  P(u, t) = -P(t, u), one carry per side at the edge key, the teeth born at (key - 1) div senses, so
  q_tu + q_ut = 0; across a Mesh P(x, y) = c (x_r y_p - y_r x_p). The passing reads the gears and moves none.
- **Click world:** the act leaves a q on every side that carried and a line's q is the sum of its sides'. The decoder
  reads each edge's books at its place (decoder/sides.py) and each place's books (shadow.books): closed at every place
  on NC29b's three worlds; one quantum per meeting NOT SHOWN (|q| reaches 5 a round, 80,000 on the mesh world).
- **Synced?** no. Line 117 (the click as "a train's own click tooth"); line 126 ("q_c, k+ = carry(S, key, k)" per
  train, and "On main the plan is empty, so J = 0", false since B2, B2b and B3); line 127 ("k0 c00" as the clocks'
  read, and "the Mesh flux ... booked by no click this night", which node-edge's Mesh edges now book); line 128 (the
  per-train click line); line 129 (its Test line names no test_the_tensor24_edges.py).

### M3. engine/mesh.py
- **Part:** seen, gripped, held, stretches, pull; node-live, unchanged on every branch. Terms 3 and 4.
- **Texts:** EDGE2.md, EDGE3.md (DERIVED). ONELAW3.md gives the grips as gg^ij = gt^ij - W b^i b^j (PASSED as a
  reading; not built).
- **Clock:** each neighbour tugs a gear toward its own count through their Mesh, alike from both ends.
- **Algebra:** F = the sum over the six Spokes of grip (neighbour - own); a Mesh's grip is its rest plus the ii slots
  read at both its ends.
- **Click world:** OWED. Its docstring's "as the clicks will read them" names no reading. The board's wave's travel
  (about 0.41 Mesh a round per axis) is a clock fact; reading it as light needs light's echo (reading 7, NOT READ).
- **Synced?** partly. Lines 145 and 146 say "lengths and the speed of light, as the clicks read them" and "read in the
  clicks as light" as if read; under line 40 these are owed.

### M4. engine/contract.py
- **Part:** pushes, contract, read. node-onelaw f494b0aa6: pushes lays a monomial of any number k of legs as their
  circulant, Plan(legs, factor, target) in state.py.
- **Texts:** DAVID-TENSOR24-G3.md (toys-5; G3's page DERIVED by both end readers at its fifteenth text); ONELAW3 3.7
  (PASSED by both; (c) built). Code reader: S/hcr8/REPORT4.md PASSED 1794d474b..e871dfb75.
- **Clock:** a vertex couples a Node-clock's gears: each term of one potential pushes every one of its legs by the
  others.
- **Algebra:** each monomial f x_1 ... x_k pushes each leg by -f times the other k - 1 legs, the unit standing for a
  leg it lacks; J1 is their sum (k at most four on node-live, any k on node-onelaw).
- **Click world:** OWED. The rest beat a spring gives would be read as a mass (reading 8), which no text gives.
- **Synced?** no. Line 148's algebra column ("pushes each leg by -f times the other three") and line 126 ("up to three
  readings") predate node-onelaw's k legs.

### M5. engine/kinds.py
- **Part:** node-live: Kinds, det, axes, inverse, turns, kinds, weighed, beside, square, placed, stacked. node-half
  0893f2f28 adds Halves, Lifts, conjugate, hamilton, lifts, listed, on_cosets, pair, product, spread, times, turned:
  the 48 lifts as words u w^k z^m from the star; E1/2, E5/2 and G3/2; the 8-gear train on the cosets of C6; the
  24-gear train laid as one half-speed hand on the three axes (Lifts.axes).
- **Texts:** the law's theorems of the 24 (line 94); HALF2.md (boss-derive night_1031/half/; PASSED by both:
  S/hf_math/REPORT.md on HALF, S/hf_phys/REREAD.md on HALF2); GEN4c.md and GEN5b.md (PASSED by both:
  S/hf_math/REPORT_GEN4c_GEN5b.md, S/hf_phys/gen5/REPORT_GEN4c_GEN5b.md); GEN3 NOT PASSED by both; GEN4 and GEN4b
  PASSED by the mathematician, NOT PASSED by the physicist; GEN5 NOT PASSED by both (all in S/half/). Code readers:
  S/hcr8/REPORT.md and REPORT2.md PASSED; S/hcr7/REPORT6.md and REPORT7.md PASSED (to 0893f2f28).
- **Clock:** every Node-clock is made alike from its star of six Spokes: the 24 turns, the five kinds, and on
  node-half the 48 lifts, each of the 24 twice, which give the half-speed gear: two half-speed trains, and one
  half-speed hand on the three axes.
- **Algebra:** the 24 are the matrices of three Spokes that Rule3's weight keeps, 24 of 216; the kinds have 1, 1, 2, 3
  and 3 rows. The full turn is -1 on the three half-speed kinds. On the 24 whole units the hand gives 2 + 2' + 2'',
  four of each, whole projectors, a third on each axis row; a real coupling never parts 2' from 2'' (line 173 calls it
  DERIVED; GEN4, which states it, is PASSED by its mathematician only); the parting term is OPEN.
- **Click world:** n/a (stated) for the kinds: a kind is no observable and a click names a train, never a row (line
  188). OWED for the doublets: the share 1/3 per axis row needs a click that names the row, and three species' own
  clocks, Koide's Q and the Michelson reading wait on a world, on a clock's own count and on light's click lines (NOT_CLOSED 34, 42).
- **Synced?** no. Line 173 ("its code reader owed" for 0893f2f28: PASSED, S/hcr7/REPORT7.md, 05:59); line 343 ("on
  node-half a18901454 ... its code reader reading"); line 189 (Home gives engine/kinds.py as "the 24 and the kinds"
  only).

### M6. engine/state.py
- **Part:** State, Plan, Read, Click, Gearing, Layout. node-edge: k becomes the click tooth of every edge side,
  ((1 + Spokes) x trains x trains, sites) teeth at 88b4d281c. node-onelaw: Plan(legs, factor, target).
- **Texts:** the law's own; NC29b.md (PASSED); ONELAW3 3.7 (PASSED).
- **Clock:** what a Node-clock holds: each gear's count now and before, the tooth between them, the drive's fine
  tooth, the click teeth, and term 10's 0i and jk rows, carried and read by no gear.
- **Algebra:** whole-number arrays a, b, r, r_d and k, and the layout's coefficients and plans, read once at load.
- **Click world:** n/a (stated): it holds the board, not its shadow.
- **Synced?** partly. Glossary lines 409 and 412 know a gear's fine tooth and "a train's click tooth", not the edge
  sides' teeth.

### M7. runner/files.py
- **Part:** whole, Rule, star, axial, once, read, numbers, rows, checked, seed_departures, universe_departures,
  sites_of, setting_departures, departures, vocabulary, held_departures, entries. node-half adds Spun, spun,
  halved_departures: the files' eight kinds and the two half-speed trains, admitted and refused in a file run.
- **Texts:** the law (decision 35; lines 35 and 106); HALF2 items 4 and 5 (PASSED by both); the strengths rule
  (S/arch_night/STRENGTHS.md section 3: Big Pic's rule, ruled by the Boss at 04:24 UTC; a ruling, not a derivation);
  VARY1.md (S/vary/; NOT PASSED by both, S/vary1_math/ and S/vary1_phys/REPORT.md: a varied lay lives in
  setting.json, written by a world lay tool).
- **Clock:** before the first round the files say which trains every Node-clock carries, how many stand on each axis
  and which gears are laid where.
- **Algebra:** whole numbers only; every side, part and integer at least 1; each departure refused by name.
- **Click world:** n/a (stated): nothing the clicks show comes from the files.
- **Synced?** no. Line 177 ("its kinds among the 24's five"; "the free strengths CHOSEN by name") and line 179 ("the
  only strengths are the universe file's own CHOSEN integers ... so that they can be played with by the files")
  stand against the owner's "Choosing a strength is forbidden" and the Boss's ruling of 04:24 UTC, already entered at
  line 148.

### M8. runner/board.py
- **Part:** site, wrap, board; node-live, unchanged.
- **Texts:** the law (line 92, locality).
- **Clock:** each Node-clock's six neighbours, one through each Spoke.
- **Algebra:** a site's index from its three coordinates; the wrap on each axis by Rule3's carry.
- **Click world:** n/a (stated): a label crosses as a place and never as a length (line 46).
- **Synced?** yes (line 187).

### M9. runner/load.py
- **Part:** node-live: Train, Trains, first, tables, trains_of, lay, Loaded, load, teeth, geared, geometry,
  laid_out. node-half: kept_forms. node-onelaw: scaled (the whole action times one whole factor), geared laying the
  clocks' read as one-leg terms. node-edge: laid_out lays the edges and the Mesh's edges, every side's tooth born at
  (key - 1) div senses.
- **Texts:** the law; ONELAW3 4A (PASSED by both; (d) built, S/hcr8/REPORT4.md PASSED); NC29b.md (PASSED); HALF2.md
  (PASSED); KEY2.md (NOT PASSED by both; not built); the strengths rule (a ruling).
- **Clock:** the Node-clock's initialization: every Node-clock made alike, the 24's tables, each train's rows, every
  gear's teeth and grips, the held hand found by character, the ties, every edge side's click tooth at its birth.
- **Algebra:** a channel's table is the primitive row u of its group sum c u u^T; the teeth at rest 6 den Gamma^2,
  the grips den Gamma^2, k0 = Spokes x senses = 12; births (key - 1) div senses; scaled: split(lam n, lam D) =
  (q, lam r) on every carry, so a scaled world moves bit for bit as at lam 1 (4A.1), and no file names a unit.
- **Click world:** n/a (stated): no number of the load reaches the clicks except through the act.
- **Synced?** no. Line 189: its Home lists plans' "rows_of, holding, tying, joined and meshing" and no scaled,
  kept_forms or edge births; its Status says "hold, tie, mesh and push are CHOSEN in the universe file".

### M10. runner/plans.py
- **Part:** node-live: pairs_of, passing, rows_of, holding, tying, joined, spread, pushing, meshing, notching.
  node-edge: edging (the edges from J's potential, each monomial weighed onto its trains by kappa (L - l) / L, kappa
  read from the structure) and crossing (the Mesh's edges); passing gone. node-half: selves, widening.
- **Texts:** TERM5_FIFTH.md (boss-derive derive/boss/g2/term5_third/; DERIVED by its final pair at k0 = 12);
  DAVID-TENSOR24-TERM9-NOTCH.md (toys-5; DERIVED by both pairs); DAVID-TENSOR24-G3.md (DERIVED); NC29b.md (PASSED);
  LIGHT1 sections 1 and 3 (sound by both; the text NOT PASSED); FRAMES.md frame 7 (the gradient vertex, a frame).
  Code readers: edging in S/hcr8/REPORT3.md PASSED; crossing unread.
- **Clock:** the plans every Node-clock reads, laid once from the star, the tables and the files: term 5's push, term
  9's notch, term 6's holding and tying, the gradient vertex, and on node-edge the edges between trains and across
  Meshes.
- **Algebra:** whole factors on rows of the readings: term 5 in the books' form at dial 2; V9 = 2 h c00^2 + h tr^2;
  the edges' weights kappa (L - l) / L, a hands' tie weighing 3 on both legs at kappa 6.
- **Click world:** OWED for the beat: its docstring's "what the clicks read as its mass" names no reading. For the
  edges the decoder reads their books (decoder/sides.py).
- **Synced?** no. Line 148 ("a writer builds it in plans.holding and term 11's passing once its text passes": built as
  plans.edging on node-edge f71c19390; "the Mesh leg's wind counted by no click, NOT_CLOSED 4": plans.crossing counts
  it at 88b4d281c); line 189 (Home's list).

### M11. runner/rounds.py
- **Part:** rounds; node-live, unchanged.
- **Texts:** the law (line 35: no loop in the act; the rounds counted from outside).
- **Clock:** the rounds, counted from outside, since no Node-clock holds a count.
- **Algebra:** the engine's act iterated.
- **Click world:** each round's quotients are handed beside its state to the record; a round crosses as order only.
- **Synced?** yes (lines 193 to 197). Line 399's merge of rounds and rewind still waits.

### M12. runner/rewind.py
- **Part:** rewind; node-live, unchanged.
- **Texts:** the law (Postulate 4; lines 31 and 35).
- **Clock:** all the rounds run back, to see the start return.
- **Algebra:** the engine's untick iterated, no log read.
- **Click world:** n/a (stated); the record's end line says whether the run back was exact.
- **Synced?** partly. On node-edge the edge teeth run back only from the forward run's end teeth (the end line's
  "teeth"); lines 117 and 195 do not say it.

### M13. runner/run.py
- **Part:** node-live: Engine, promises, window, wide, promised, digest, stated, ledger_of, counts, clicked,
  characters, header, run. node-edge adds joined, meeting, teeth_of, crossed: a line for every clock joined to a side
  that carried, listing every edge side of its clock, q 0 included; the header's dial and birth; the end's teeth.
- **Texts:** NC29b.md (PASSED); DECODE3.md (S/split/; NOT PASSED by both; its four fields taken by the Boss's ruling of
  04:5x UTC); the runaway named where a count passes the width (node-live a66674061). Code reader: S/hcr8/REPORT3.md
  PASSED to 50af24bde.
- **Clock:** the run from the three files to the record; before each round the promise is read from outside.
- **Algebra:** the act iterated; the promise: teeth at least 1, every tooth within its edge's dial, the wave's
  window, every count within the width; a departure named at its round and nothing written.
- **Click world:** it writes what the decoder reads: the header, the click lines, the end, the ledger beside them.
- **Synced?** no. Line 196 ("the click lines of schema 1.3 (one per round, Node-clock and train whose click tooth
  carried").

### M14. record/schema.py
- **Part:** node-live schema 1.3 (File, Kind, Train, Header, Click, End, Count, Ledger, with 1.2's classes kept for old
  records). node-edge schema 1.4: Click's sides [u, q_tu, k_before, k_after] and across [[u, place, q_tu, k_before,
  k_after]], Header's dial and birth, End's teeth and across, one ADDED entry (MINOR 4). node-third-readings: ACROSS,
  the across field list.
- **Texts:** the schema's own; NC29b.md; DECODE3.md's fields (NOT PASSED; taken by ruling); the Boss's ruling of 04:4x
  UTC: one click line for the three clicks, the Third record withdrawn.
- **Clock:** the boundary between the board and the clicks; only the readers read it.
- **Algebra:** JSON Lines of whole numbers of any width and labels; MINOR = len(ADDED).
- **Click world:** its click line is the click world's event: a round, a site, a train and q, the sum of its sides'
  carries; nothing is computed in it.
- **Synced?** no. Lines 110, 203, 204, 205 and 345 (schema 1.2 and 1.3; "to build: 1.4 only with the face").

### M15. decoder/records.py
- **Part:** Record, whole, keyed, parsed, schema_shapes ... guarded, read, read_ledger. node-third: GUARDS gains
  records.paired, the sides guard; q 0 is refused only on a line holding no sides.
- **Texts:** the decoder's basic part (C2 6b77872dc, C4 9ccbc6481; their code readers in the ledger); DECODE3 rule (a)
  (NOT PASSED by both).
- **Clock:** the decoder is the watchmaker outside the case (line 209); this module's docstring has no four layers.
- **Algebra:** read a line against the schema and the train cards, and refuse a bad one by name.
- **Click world:** the record read alone, every refusal named.
- **Synced?** partly. Line 304 ("the decoder's four modules are owed them"): there are six modules; clicks, shadow,
  sides and three carry the four layers; records.py and measure.py lack them, and records.py's docstring still says
  schema 1.3. Line 215 reads "its click lines of schema 1.3".

### M16. decoder/clicks.py
- **Part:** Tally, Counted, listed, tallied, by, summed, counted; node-live.
- **Texts:** C2 (the basic part).
- **Clock:** the click lines listed and counted, nothing read into them.
- **Algebra:** whole counts and sums per train and Node-clock: given, taken, net.
- **Click world:** the list and the counts, no verdict.
- **Synced?** yes (line 213).

### M17. decoder/measure.py
- **Part:** verdict, meshes, past; node-live.
- **Texts:** C5 and C6 (boss-derive night_1031/code_readers/hcr4_REPORT.md and hcr5_REPORT.md NOT PASSED and folded;
  the seventh code reader PASSED 0456fa478..86ec0e348, per line 355);
  DECODE3d.md (S/split/; NOT PASSED by both: R4's causal and locality checks named on the board's cone).
- **Clock:** no four-layer docstring; the cone is one Mesh a round.
- **Algebra:** a verdict with its cause; the Meshes between two sites the shorter way round each side; the lay's past
  cone.
- **Click world:** a board check: the cone is the board's, named a check until light's echo cone exists.
- **Synced?** yes (line 213), with line 304's owed layers still true of it.

### M18. decoder/shadow.py
- **Part:** lacking, placed, met, spread, books, meetings, clock_lines, not_read, duration, twins, echo, laid, cone,
  shadow, click_board; node-live.
- **Texts:** SHADOW.md (boss-derive night_1031/shadow/; NOT PASSED by both); SHADOW2.md (DRAFTED for the same pair);
  C5 and C6 (code readers as M17).
- **Clock:** the click board as the clocks' meetings: each event one quantum passing from one clock to another at one
  place, the order of events and each clock's own count, no time axis.
- **Algebra:** at every place, the sum of q over the trains and each line's q; a meeting is one give of -1 and one
  take of +1.
- **Click world:** seven readings, each SHOWN, NOT SHOWN, NOT READ or NO CLICK with its cause (readings D1, D3 to D7,
  D11 and D12 below).
- **Synced?** partly. Line 213's status reads node-live's per-train worlds only; on the edge form NC29b reads the books
  closed at every place and the meetings and each clock's line NOT SHOWN.

### M19. decoder/sides.py
- **Part:** edged, formed, mirrored, paired, sided, whole; node-third d9ad5f6aa; node-third-readings 3a446e77a adds
  the across guard.
- **Texts:** NC29b.md (PASSED); DECODE3 rule (a) (NOT PASSED by both); the Boss's rulings of 04:3x and 04:4x UTC. Code
  readers: S/hcr7/REPORT5.md NOT PASSED f87a93f8a (three BLOCKING); S/hcr7/REPORT8.md PASSED c01db8f90..d9ad5f6aa;
  the across guard unread.
- **Clock:** n/a (stated): the decoder's guard on the edges between clocks, read from the record alone.
- **Algebra:** per line, its sides' q summed to its q; per edge at its place, in the site or across a Mesh, the two q
  summing to 0 and the two teeth to the key less 1, before and after.
- **Click world:** each edge's books at its place, the first click's books edge by edge, refused by name where an edge
  does not close.
- **Synced?** no: not named in ARCHITECTURE.md.

### M20. decoder/three.py
- **Part:** structure, joined, edges_of, lands, passing, readings, compared, twice, apart, swapped, within, ends, named,
  omitted, q_lines, ambiguous, unread; node-third-readings 3a446e77a; tools/tensor24_decode.py gains --readings,
  --twin, --apart, --swap.
- **Texts:** DECODE3.md, DECODE3b.md, DECODE3c.md, DECODE3d.md (S/split/; each NOT PASSED by both, reports in
  S/decode3*_math/ and S/decode3*_phys/); the Boss's rulings of 05:1x to 05:4x UTC. No code reader yet.
- **Clock:** n/a (stated): the decoder's readings of the three clicks, by each place's structure, never by a label.
- **Algebra:** whole counts alone; x = D q + k_after - k_before; the split's weights kept as pairs (x_tu, X_t); R2's
  past ladder cut into parts by Rule3's carry.
- **Click world:** the structure per place tells the three clicks apart; which side lands; R2 within one record; the
  passings and weights as a board check; R1, R2's two-record form and the swap on two records (readings D14 to D19).
  (3a) to (3d) and CHSH are named owed in its docstring.
- **Synced?** no: not named in ARCHITECTURE.md.

### M21. main.py
- **Part:** made, layout, ran; node-onelaw adds typed; node-half's made passes the 48 lifts.
- **Texts:** the law (line 99: the one joint).
- **Clock:** the one joint: the Node-clock's act handed to the runner that turns it.
- **Algebra:** n/a (stated): it computes nothing.
- **Click world:** n/a (stated).
- **Synced?** yes (lines 99, 117, 129).

### M22. readings/__init__.py (with the six package __init__.py files, one line each)
- **Part:** one docstring, imported by nothing.
- **Texts:** none.
- **Clock, Algebra, Click world:** OWED, all three: no text gives it a role.
- **Synced?** yes: line 399 says it stands in no part of section 3, with its row in section 5.

## B. The thirteen terms of the act

### T1. The readings
- **Part:** engine/step.py readings; node-live.
- **Texts:** EDGE2.md (DERIVED).
- **Clock:** a gear looks at itself and at its six neighbours.
- **Algebra:** the readings' rows at the now slot: the value, three gradients, the force, then the unit.
- **Click world:** n/a (stated, line 143: none of their own).
- **Synced?** yes (line 143).

### T2. The teeth W
- **Part:** engine/step.py weight and dials; runner/load.py geared. node-onelaw 08c66fd40: weight contracts the
  clocks' Plan, monomials of any number of legs read on the counts given first, the round's two stages kept.
- **Texts:** EDGE2.md (DERIVED); ONELAW3.md (PASSED by both as a reading: W = det(gt) L^4, a product of the 3+1
  gears; (b) built, the product terms not laid until the flat and the units are ruled); FWDBACK3.md (boss-derive
  night_1031/fwdback3/; NOT PASSED by both: the 00 row's own law OPEN, NOT_CLOSED 2).
- **Clock:** how much a gear carries in one turn; a deeper clock turns slower.
- **Algebra:** W = rest + k0 c00, linear (node-live); on node-onelaw W = rest + the clocks' plan, today its one-leg
  terms, so no motion moves.
- **Click world:** OWED. "Proper time" needs a clock's own count between two meetings (D6, NOT READ; FACE2 not built).
- **Synced?** no. Line 127 ("the clocks' read of the metric family's 00 slot, k0 c00"), line 144 ("W = rest + the
  sum of the 00 slots, linear"; its click cell "proper time" as if read) and line 341 (the widened given-first step
  "named and not built": built on node-onelaw).

### T3. The grips
- **Part:** engine/mesh.py gripped, engine/step.py grips; node-live.
- **Texts:** EDGE2.md (DERIVED); ONELAW3.md (gg^ij; not built).
- **Clock:** how hard a Mesh holds its two gears, alike from both ends.
- **Algebra:** grip = den Gamma^2 + the ii slots at both ends.
- **Click world:** OWED. Lengths are read only by light's echo between clocks (reading 7, NOT READ).
- **Synced?** no. Line 145 ("lengths and the speed of light, as the clicks read them").

### T4. The pull F
- **Part:** engine/mesh.py pull; node-live. On node-edge the board's wave's exchange with a tied train clicks on the
  Mesh's edges (plans.crossing, step.crossing).
- **Texts:** EDGE2.md (DERIVED); LIGHT1.md (NOT PASSED by both; sections 1 and 3 sound); EDGE1.md (DRAFTED, no reader).
- **Clock:** each neighbour tugs a gear toward its own count through their Mesh.
- **Algebra:** F = the sum over the Spokes of grip (neighbour - own).
- **Click world:** OWED. The decoder reads the books of the Mesh's edges, but no text tells those lines as light's;
  the echo rule is owed.
- **Synced?** no. Line 146 ("waves, the board's wave travelling, read in the clicks as light").

### T5. The metric's push
- **Part:** engine/step.py sources and stress (J5); runner/plans.py pushing; node-live.
- **Texts:** TERM5_FIFTH.md (DERIVED by its final pair at k0 = 12); DAVID-TENSOR24-G2-STATIC.md (toys-5; DERIVED by
  both end readers at its thirteenth text); ONELAW3.md (the 3+1 dial, PASSED as a reading).
- **Clock:** the clocks' motion winds the clock's own train, and every clock reads its 00 slot.
- **Algebra:** each square slot is pushed by minus the derivative of the act's own energy by it, the books' form at
  dial 2, k0 = Spokes x senses = 12; its price, the metric's self-stress unpaid (NOT_CLOSED 30).
- **Click world:** OWED. Gravity as the clocks' rates needs D6 and light's echo; gamma as echo delay over clock
  deficit is Big Pic's post 6538018966, no text.
- **Synced?** no. Line 147 (opens "David's static-field text (G2) stands at its twelfth text"; the push kept as a
  world's switch, where Big Pic's rule leaves the push field to term 5's factors); line 395 ("the thirteenth
  follows").

### T6. The vertex and the spring
- **Part:** engine/contract.py; runner/plans.py holding, tying, joined, meshing; runner/load.py's held spring;
  node-edge's edging books the tie's passing on edges.
- **Texts:** DAVID-TENSOR24-G3.md (DERIVED by both end readers, fifteenth text); DAVID-TENSOR24-PASSING4.md (toys-5;
  NOT_CLOSED 29's split at the rest, DERIVED by both end readers); NC29b.md (PASSED); HAT1.md to HAT4.md (S/nc29/; no
  reader); the strengths rule (a ruling).
- **Clock:** a hairspring ties a hand to a held hand in its own clock, and a vertex couples trains.
- **Algebra:** each monomial pushes each leg by -f times the others; the tie through the held hand's square; the
  held spring K = W / 3 at spring 10^8 in the click and mesh worlds.
- **Click world:** OWED for the rest beat as a mass (reading 8). The exchange's books edge by edge are given (C1).
- **Synced?** no. Line 148 ("a writer builds it in plans.holding and term 11's passing once its text passes"; the
  gradient vertex "counted by no click"); line 163 ("no spring is laid in any world file yet; the strengths OPEN at
  G3"); line 164 ("G3's line, NOT AGREED ... the seventh text is in work"); line 334 ("both of G3's readers not
  passed"); line 397 ("stands at its fourteenth text").

### T7. The drive
- **Part:** engine/step.py drive and driven; node-live.
- **Texts:** DAVID-TENSOR24-TERM7-DRIVE.md (toys-5; DERIVED by both end readers, fifth text).
- **Clock:** one wheel carries the coupling's push for every row.
- **Algebra:** q_d, r_d+ = carry(J, T_d, r_d), J = J1 + J5; K = s T_k q_d.
- **Click world:** n/a (stated: the clicks do not come from the drive).
- **Synced?** yes (line 149).

### T8. The kick
- **Part:** engine/step.py kick; node-live. node-onelaw's scaled multiplies T_k by the units' factor.
- **Texts:** EDGE2.md and the drive's text (K = T_k s q_d).
- **Clock:** the drive's whole turns pushed into the gear.
- **Algebra:** K = T_k s q_d, at T_k = 1.
- **Click world:** n/a (stated, line 150).
- **Synced?** yes (line 150).

### T9. The volume's notch
- **Part:** runner/plans.py notching; node-live.
- **Texts:** DAVID-TENSOR24-TERM9-NOTCH.md (toys-5; DERIVED by both pairs).
- **Clock:** the board's mean count swings about its rest and returns.
- **Algebra:** V9 = f9 c00^2 + (f9 / 2) tr^2; the mean's beat 4 sin^2 (omega / 2) = 2 f9 / W as a reading of the act.
- **Click world:** OWED (FULLPIC's row: no click reading this night).
- **Synced?** no. Line 151 ("h CHOSEN as chosen.notch ... 120000 in the well world": Big Pic's rule gives rest div
  Gamma, 6000 in the well; its click cell states the universe's swing and massless polarizations with no click
  reading); line 336 (FULLPIC's row, "'notch' CHOSEN").

### T10. The shift and the shears
- **Part:** not built as a term: the 0i and jk rows are carried in state.py and read by no gear.
- **Texts:** ONELAW3.md (PASSED by both as a reading: the shift b^i on the 0i gears; not built, BUILD.md 3 (a): its
  run back with the kept momentum W (v - b . D a) unmeasured, the step's bound with the shift failing 11 of 12 runs);
  no G4 text.
- **Clock:** the now leans toward a neighbour, the shift, and stretches by direction, the shears.
- **Algebra:** gg^0i = W b^i, gg^ij = gt^ij - W b^i b^j; the joined act reads d_t(W b^i d_i a) + d_i(W b^i d_t a).
- **Click world:** OWED (frame dragging and shear read in the clicks).
- **Synced?** no. Line 152 ("owed after G2"; "no draft yet": ONELAW3 gives the form, named and not built) and line
  337 (FULLPIC's row, "OPEN: no reader").

### T11. The whole click
- **Part:** node-live: step.passing per train, carried at the key by the train's own tooth. node-edge f71c19390,
  50af24bde: per edge side, plans.edging, step.passing, load's births, run.clicked, schema 1.4.
- **Texts:** COUNT5.md (DERIVED for the pair at one Node-clock); NC29b.md (PASSED by both); DAVID-TENSOR24-PASSING4.md
  (DERIVED); SCALE1.md (S/scale/; no reader); KEY1.md (S/onelaw/; no reader); KEY2.md (NOT PASSED by both).
- **Clock:** when a passing between two clocks completes a whole key, the edge's pair of teeth carries it once: what
  leaves one side enters the other in the same round.
- **Algebra:** node-live S = X(a, b) + X(a+, a), q, k+ = carry(S, key, k); node-edge: P(t, u) the given less the taken,
  one carry per side at the edge key (the file's key times kappa over senses), teeth born at (key - 1) div senses,
  so q_tu + q_ut = 0 by the carry's law.
- **Click world:** the books at every place edge by edge (sides guard; shadow.books), SHOWN on NC29b's worlds and on
  Big Pic's stage 1 records; one quantum per meeting NOT SHOWN.
- **Synced?** no. Lines 117, 128 and 153 (the train's own tooth, "born at half the key"); line 338 ("to build: the
  four-leg passing"); line 380 (frame 4's "a passing for monomials of four value legs"); line 412 (the key as "a
  train's click tooth").

### T12. The split click
- **Part:** not built as a draw. Built as the split over the triangle: node-edge's edging lays a monomial with value
  legs in three trains on the triangle's three edges, each passing its share. G5's draw on form B is not built (its
  pointer reads two Meshes).
- **Texts:** DAVID-TENSOR24-G5-DRAW.md (toys-5; DERIVED by both end readers; its law-of-the-choice texts PASSED by
  both); SPLIT1.md (S/split/; DRAFTED, no reader); SPLIT2.md (NOT PASSED by both, S/split2_*/REPORT.md); SPLIT2b.md
  (PASSED by both, S/split2_math/REPORT2.md, S/split2_phys/REPORT2.md: the shares follow the passing, the law gives
  frequencies, not weights); SPLIT3.md (read by SPLIT2b's readers in their second read, minors folded, no verdict of
  its own; P2 DERIVED).
- **Clock:** where three clocks meet at one place, the passing splits over the triangle's three edges, each edge on its
  own pair of teeth.
- **Algebra:** each monomial weighed onto its trains, kappa (L - l) / L; each side's passing x = D q + k_after -
  k_before, so the split's weights are read from the sides with no new field.
- **Click world:** the place's structure (three clocks all pairwise joined) tells where it splits (decoder/three.py
  structure), which side lands names the taker, the weights are read as a board check; Born's shares (3a) are owed.
- **Synced?** no. Line 25 ("the split, where a draw by the sizes chooses, the one choice built"); line 154 ("SPLIT2b,
  PASSED by its mathematician": PASSED by both); line 339 ("to build: its pick, on the owner's law question": answered
  at 03:37 UTC); line 359 ("SPLIT2, the weights, is NOT PASSED" with no word of SPLIT2b).

### T13. The frozen clock
- **Part:** no code of its own; measured on the edge by a probe (A3 36effecd5).
- **Texts:** DAVID-TENSOR24-TERM13-FROZEN.md (toys-5; DERIVED by both end readers; the Boss's to confirm).
- **Clock:** a clock's beat goes as the root of its spring over its teeth, so it stops only where its teeth grow
  without bound.
- **Algebra:** N^2 = rest / W, within 0.7 ppm on the edge far above a notch.
- **Click world:** OWED (two clicking clocks at two depths, D6).
- **Synced?** no. Line 108 ("terms 6, 12 and 13 DRAFTED"); the row at line 155 is current.

## C. The three clicks

### C1. The first click (two clocks alone)
- **Part:** node-edge f71c19390, 50af24bde, 88b4d281c (term 11 on the edges, schema 1.4, the Mesh's edges);
  decoder/sides.py and three.py read it. Big Pic's stage 1 (bigpic-3clicks edgeclick.py) is its probe.
- **Texts:** NC29b.md (PASSED by both); COUNT5.md (DERIVED); the owner's words of 03:4x UTC (a shared tooth for every
  pair of clocks) and 04:1x UTC ("Check with the first click without a draw"); the Boss's ruling of 04:2x UTC.
- **Clock:** two clocks alone meet on one edge; no draw and no turn; the edge's two teeth, born complementary, carry
  the passing.
- **Algebra:** K q = r_before + x - r_after, the carry's own law ("past meets future"); q_tu + q_ut = 0 at every place.
- **Click world:** the books edge by edge SHOWN (stage 1: 0 of 4,212 places open on the click world, 0 of 4,442 on the
  mesh world); R2 NOT SHOWN for it, 0 of 54 sides, its landing fixed by its past as the law expects; the swap SHOWN,
  10,827 of 10,827 lines.
- **Synced?** no. Lines 117, 128, 153; line 359 ("Writer B's node-edge 50af24bde (05:05Z, unmerged, its code reader
  owed)": S/hcr8/REPORT3.md PASSED it; the head is 88b4d281c).

### C2. The split click (three clocks at one place)
- **Part:** as T12: the split by the structure on node-edge's edges; no draw built.
- **Texts:** as T12; and the owner's word of 04:1x UTC ("The split click chooses between the first and the third").
- **Clock:** a passing shared over a triangle's three edges where three clocks meet.
- **Algebra:** the weights from the sides, x = D q + k_after - k_before; the label rule: P2, a lay and its swap giving
  exactly swapped takes, DERIVED on the act (SPLIT3).
- **Click world:** the structure per place (stage 1: 2,295 places not all joined and 108 all pairwise joined, a lower
  bound where lines leave out sides); which side lands; the shares against the weights (3a) owed.
- **Synced?** no. Lines 25, 154 and 339, as T12.

### C3. The third click (the circulation per triangle)
- **Part:** not built in src. On Big Pic's bench (bigpic-3clicks derive/bigpic/three_clicks/): mode 4, mode 4c, modes 7
  to 10, and mode 11, the triangle's own tooth, one whole circulation per quantum (8a718332f), the 24 on it 24 of 24
  (9c78397e5). The interim and the Third record are on the local node-third-interim 216cc7b03, unpushed.
- **Texts:** THIRD.md NOT PASSED by both; THIRD2.md PASSED by both (the direction with its tooth r3, q from a+ - a0,
  the 24, the run back at J5 = 0); THIRD3.md and THIRD4.md NOT PASSED by both; THIRD5.md PASSED by its mathematician,
  NOT PASSED by its physicist (S/third/, S/th_math/, S/th_phys/); THIRD6.md NOT PASSED by both (S/third6_frozen/,
  S/third6_math/ and S/third6_phys/REPORT.md, 05:3x: each clock's books, and a member picked among ties);
  THIRD6_mode4.md (S/third/; DRAFTED note); THIRD7 not written (its probe S/third7/tri7.py); SPLIT3.md (PASSED);
  VARY1.md and VARY2.md (NOT PASSED by both); KEY2.md (NOT PASSED by both). The owner's law of the choice (03:37), Bell's
  test (03:4x), the law of the path (05:56, docs/ALGEBRA.md line 1964), "never seen alone" (06:0x), the hidden tooth
  approved on condition that every clock's books close (05:5x).
- **Clock:** three clocks at a triangle's vertices; besides each edge's pair of teeth the triangle holds its own tooth
  and a twin, which turn by a palindrome of shears; each quantum the triangle's tooth lands goes around all three edges
  at once, so no clock's own line carries it alone.
- **Algebra:** 3 x = (3 x - c y) + c y with y = c . x; each edge tooth carries 3 x_e - c_e y at the dial 3D, unturned;
  the triangle's tooth carries y, its twin turned at K = C^T C = 3, each landing booked +1, +1 and -1 along the
  boundary; B c = 0, so each clock's line is its own passing's carry. THIRD6's lemma (DERIVED inside a NOT PASSED
  text): a turn that moves flow only along the boundary keeps the two clock-total directions, det(L - I) = 0, so the
  choice lives in the circulation alone.
- **Click world:** given in part. R2 within one record is a necessary reading only (SHOWN, 54 of 54, on stage 1's
  third click); the swap holds for mode 4 and mode 11 on the bench and fails for stage 1's turn M (apart at round 9);
  two records compared show the clicks differing (the seed test). The choice is read only by Bell's test across a pair
  (R4, owed in the decoder; Big Pic's stage 4 toy: 40,000 pairs, CHSH 2,490 per mille from the record's paired
  lines). "Never seen alone" is a property of the form (it shows only in the sides); no decoder reading is built that
  would fail if it were absent.
- **Synced?** no. Line 25 (its weights "OPEN until its derivation, THIRD"; still OPEN, but "the one choice built" names
  the split); line 344 (FULLPIC's row: "the owner is asked the law question (NOT_CLOSED 41)"; "writer C's build on
  node-third waits": node-third now holds the decoder's sides guard); line 359 ("Big Pic builds the
  one-quantum-around-the-triangle member next": built as mode 11, 8a718332f; the law of the path absent); line 40 (the
  law of the choice entered, the law of the path not).

## D. The initialization

### I1. The world's three files
- **Part:** examples/tensor24 (the bang), tensor24-live, -well, -click and -mesh, each laid by a generator kept in the
  repo (derive/boss/), read by runner/files.py; node-half's half-speed worlds are laid in memory by its tests; Big
  Pic's bench lays click-k1601-laid by laywrite.py (a probe).
- **Texts:** the law (decision 35; lines 35 and 106); the strengths rule (S/arch_night/STRENGTHS.md section 3, a
  ruling); VARY1.md and VARY2.md (S/vary/, S/vary2/; NOT PASSED by both); SCALE1.md (no reader); KEY2.md (NOT PASSED
  by both).
- **Clock:** before round 0 the files say which trains each Node-clock carries, how many Node-clocks stand on each
  axis, which gears are laid where and how many rounds run.
- **Algebra:** whole numbers only; under Big Pic's rule a world is its lay alone: every coupling at its table's entry
  1, every scale in the initialization, a runaway or a still hand the lay's reading and never a reason to re-pick.
- **Click world:** n/a (stated): nothing the clicks show comes from the files.
- **Synced?** no. Lines 177 and 179 (strengths CHOSEN, "so that they can be played with by the files"); line 189
  (each world's CHOSEN values). The click and mesh worlds' re-lay on Big Pic's rule is still owed.

### I2. The loader, the Node-clock's initialization
- **Part:** runner/load.py (with files.py, board.py, plans.py, engine/kinds.py and main.made), as M9.
- **Texts:** the law; ONELAW3 4A (PASSED by both); NC29b.md (PASSED); HALF2.md (PASSED); KEY2.md (NOT PASSED).
- **Clock:** it makes every Node-clock alike from its star, sets every tooth, grip and birth, then lays the setting's
  gears.
- **Algebra:** rest 6 den Gamma^2, grip den Gamma^2, k0 = 12, f = rest div Gamma; births (key - 1) div senses; the
  units' factor exact on every carry.
- **Click world:** n/a (stated): no number of the load reaches the clicks except through the act.
- **Synced?** no. Lines 185 to 189 (line 189 above all: Home, Status, the strengths).

### I3. The key as laid birth
- **Part:** not built. Today the key is chosen.key in universe.json (50,811,429 in the click world, 1 elsewhere), one
  key for the board (runner/load.py); on node-edge each side's key is that key times kappa over senses.
- **Texts:** KEY1.md (S/onelaw/; DRAFTED, no reader); KEY2.md (S/onelaw/; NOT PASSED by both, 06:1x UTC:
  S/key2_math/REPORT.md, the probe's identity check cannot fail, though the claim holds by the reader's own per-tooth
  check, 0 of 4,347 lines differing on a uniform field and 104 with an even key at one tooth; S/key2_phys/REPORT.md, a
  key laid per tooth lets one world carry several keys, which opens a place's books where keys mix, gives a triangle
  three dials, lays a rate field and gives one number two roles, and the one measured reading cannot fail); SCALE1.md
  (no reader); STRENGTHS.md 3.3. The owner's answer C of 05:5x UTC: the key enters the initialization tensor, or the
  node computes it at initialization; until then the file's key stands.
- **Clock:** each click tooth's laid birth k0 is laid in the setting like any count; the node computes its dial at
  initialization, K = senses k0 + 1.
- **Algebra:** K is odd by construction and the birth is its own complement, k0 = K - 1 - k0; a scalar under the 24;
  the books and the run back hold for any K.
- **Click world:** OWED. The key is the unit the click counts are read in, a setting of the board; no text gives what
  the decoder shows of it (KEY2's physicist reads a varied key as a laid rate field, the mark of a deeper clock laid
  and not shown).
- **Synced?** no. Line 359 ("KEY2 derives which": KEY2 is written and NOT PASSED by both); line 412 (the key as "the
  swept area at which a train's click tooth carries").

## E. The record

### R. The record and its schema
- **Part:** record/schema.py (1.3 on node-live, 1.4 on node-edge, ACROSS on node-third-readings); runner/run.py writes
  it; decoder/records.py reads it.
- **Texts:** as M14.
- **Clock:** the boundary between the board and the clicks; nothing of the board crosses but what its lines name.
- **Algebra:** the header (the files verbatim, the kinds with their characters, each train's kinds, part, key and
  square flag; on 1.4 the dial and every birth), the click lines, the end (rounds, rounds run back, the digest,
  exact or not; on 1.4 every edge side's teeth), the ledger's count lines beside it.
- **Click world:** the click line is the event the click world is made of; the decoder reads the record alone, and
  because the header names each train's kinds a click names a train, never a row.
- **Synced?** no. Lines 110, 203, 204, 205, 215 and 345.

## F. The decoder's readings

### D1. The books at each click (row 15)
- **Part:** decoder/shadow.py books (node-live); decoder/sides.py paired, per edge (node-third).
- **Texts:** SHADOW.md (NOT PASSED by both); NC29b.md (PASSED); DECODE3.md section 1 (NOT PASSED).
- **Clock:** a click moves whole turns from a giver's dial to a taker's, each remainder staying at its dial.
- **Algebra:** the sum of q over the trains at each place; per edge q_tu + q_ut = 0.
- **Click world:** conservation at every click: SHOWN on the edge form at every place of NC29b's worlds and of Big Pic's
  stage 1 records (0 of 4,212 and 0 of 4,158 places open); NOT SHOWN on node-live's per-train click world (123,066 of
  123,795 places); NO CLICK where no line stands.
- **Synced?** no. Line 221 reads the per-train form only.

### D2. Row 46, each later bang shows more
- **Part:** not built (its reader, decoder/bangs.py, cut with its tests).
- **Texts:** none tonight.
- **Clock:** the clocks' rate gears wind up and run down together.
- **Algebra:** the clock family's 00 slot summed over the board, round by round.
- **Click world:** OWED (line 35 item 9's clocks of clocks wait on a world that lays one).
- **Synced?** yes (line 222).

### D3. D6, proper time
- **Part:** decoder/shadow.py duration; NOT READ.
- **Texts:** SHADOW.md (NOT PASSED); FACE.md (NOT PASSED by both); FACE2.md (boss-derive night_1031/face/; DRAFTED: its
  mathematician PASSED it, its physicist's one item folded).
- **Clock:** a clock counts its own ticks between two of its clicks.
- **Algebra:** FACE2: each clock's own count of its half beats per train and Node-clock by Rule3's carries (not built;
  a schema 1.4 field would write it).
- **Click world:** a clock's own count between two of its meetings; NOT READ, as the act holds no clock's own count.
- **Synced?** yes (line 223).

### D4. No duration from rounds
- **Part:** decoder/measure.py's rules and shadow.not_read.
- **Texts:** the law (line 35 item 18: a round crosses as order only).
- **Clock:** the runner's pass is no tick of any clock.
- **Algebra:** a round is an index from outside.
- **Click world:** a difference of rounds is refused by name; only the order is counted.
- **Synced?** yes (line 224).

### D5. D8, the cone
- **Part:** decoder/shadow.py cone; decoder/measure.py past.
- **Texts:** C5 and C6 (code readers as M17); NOT_CLOSED 40 (the board wave's cone, OPEN); DECODE3d.md (NOT PASSED).
- **Clock:** a click's past is what could reach it, one Mesh a round.
- **Algebra:** measure.past, the lay's cone round each click.
- **Click world:** a board check on the board's cone: no click outside the lay's cone; NOT READ on the five worlds;
  light's cone owed.
- **Synced?** yes (line 225).

### D6. D7, the twins
- **Part:** decoder/shadow.py twins; NOT READ.
- **Texts:** SHADOW.md (NOT PASSED).
- **Clock:** two clocks part and meet again.
- **Algebra:** the two paths between the meetings, each with its winding round the board.
- **Click world:** the free path counts more; NOT READ, since every clock stands at its Node-clock (owed with a moving
  clock, a bound pair whose ticks are clicks).
- **Synced?** yes (line 226).

### D7. Light's echo (reading 7)
- **Part:** decoder/shadow.py echo, NOT READ; light.py not built. node-edge writes the Mesh's edges' click sides
  (across) from the wave's coupling, with no echo rule.
- **Texts:** LIGHT1.md (NOT PASSED by both); EDGE1.md (DRAFTED, no reader); KEY1.md (DRAFTED).
- **Clock:** one clock lays a quantum and another takes it.
- **Algebra:** the lay's and the take's Node-clocks and rounds.
- **Click world:** OWED: no rule tells light's click lines from the others (Big Pic's front on the cone's edge, one
  Mesh a round, is a post, not a text).
- **Synced?** no. Line 227 ("no world writes them"; node-edge's Mesh edges now write click lines from the wave's
  exchange, 21,589 on the mesh world at key 1, which no rule yet reads as light's); lines 234, 349, 381 and 383.

### D8. Mass
- **Part:** not built (mass.py owed).
- **Texts:** none tonight.
- **Clock:** a clock's own beat counted in its own ticks.
- **Algebra:** the held hand's rest beat (term 6).
- **Click world:** OWED.
- **Synced?** yes (line 228).

### D9. A probability, Born's rule: (3a), the shares against the weights
- **Part:** not built (decoder/three.py names (3a) owed); the weights themselves are read (D16).
- **Texts:** DECODE3.md section 3 (3a) and its later texts (NOT PASSED by both); SPLIT2b.md (PASSED: the shares follow
  the passing).
- **Clock:** many landings at one giver, each by its passing.
- **Algebra:** the shares against (x_tu, X_t) in blocks of one record, under Pearson's rule.
- **Click world:** given by text, owed in code.
- **Synced?** no. Line 229 ("at G5").

### D10. A correlation at a distance, Bell: R4, CHSH and no signal
- **Part:** not built in the decoder; Big Pic's stage 4 toy (pairwhole.py) writes one line per landing naming its pair.
- **Texts:** DECODE3.md section 4 and DECODE3d.md (R4 the conjunction of S, measurement independence and no signal,
  Bonferroni's cut; NOT PASSED by both); the owner's word of 03:4x UTC.
- **Clock:** one birth's two clicks at two clocks far apart, each with its setting.
- **Algebra:** CHSH from the click counts, the local bound 2 against the pair's 2 r2; no signal: one place's counts
  unmoved by the far setting.
- **Click world:** given by text, owed in code: the record must name the pair event (40,000 pairs, CHSH 2,490 per mille
  on the toy).
- **Synced?** no. Line 230 ("at G5").

### D11. The meetings
- **Part:** decoder/shadow.py meetings.
- **Texts:** SHADOW.md (NOT PASSED); NC29b.md (PASSED).
- **Clock:** one quantum passes from one clock to another at one place.
- **Algebra:** at a place one give of -1 and one take of +1.
- **Click world:** NOT SHOWN on the spring and on every edge-form world (|q| reaches 5 a round on the pair and click
  worlds, 80,000 on the mesh world); its one SHOWN reading went with the exact quarter turn.
- **Synced?** no. Line 231 has the per-train worlds only.

### D12. Each clock's line of meetings
- **Part:** decoder/shadow.py clock_lines.
- **Texts:** SHADOW.md; NC29b.md.
- **Clock:** a clock counts its own meetings in the order of the rounds.
- **Algebra:** its click lines in round order.
- **Click world:** NOT SHOWN on the spring and on every edge-form world.
- **Synced?** no. Line 232, as D11.

### D13. The sides guard, each edge's books
- **Part:** decoder/sides.py paired (node-third d9ad5f6aa; the across guard at 3a446e77a).
- **Texts:** as M19.
- **Clock:** each edge between two clocks holds one pair of teeth.
- **Algebra:** the two q of an edge sum to 0 and its two teeth to the key less 1, before and after.
- **Click world:** an edge that does not close is refused by name; Big Pic's stage 1 records read with no cause.
- **Synced?** no: not in ARCHITECTURE.md.

### D14. The place's structure, which click it is
- **Part:** decoder/three.py structure, joined, edges_of.
- **Texts:** DECODE3.md to DECODE3d.md (NOT PASSED by both); the Boss's ruling of 04:2x UTC.
- **Clock:** which clocks meet at the place.
- **Algebra:** the distinct pairs, each seen from both ends; two clocks alone, not all joined, or all pairwise joined;
  per site the union of its places.
- **Click world:** the three clicks told apart by structure, never by a label (stage 1: 1,809 places two clocks alone,
  2,295 not all joined, 108 all pairwise joined).
- **Synced?** no: not in section 3 (line 359 has the ruling only).

### D15. Which side lands
- **Part:** decoder/three.py lands.
- **Texts:** DECODE3.md section 3 (NOT PASSED).
- **Clock:** a giving clock joined to two or more lands its quanta on the taker its side names.
- **Algebra:** the in-site giving sides with q not 0.
- **Click world:** each landing names its taker.
- **Synced?** no: not in ARCHITECTURE.md.

### D16. The passings and the split's weights
- **Part:** decoder/three.py passing.
- **Texts:** DECODE3.md section 2 (NOT PASSED); the Boss's ruling: x = 3 K q + k_after - k_before, no weight field.
- **Clock:** each side's passing read back from its carry and its teeth.
- **Algebra:** x = D q + k_after - k_before; the weights kept as pairs (x_tu, X_t).
- **Click world:** a board check (the dial and the teeth are board fields); NOT READ with no dial or where a line
  leaves out a side.
- **Synced?** no: not in section 3 (line 359 gives the formula).

### D17. R2 within one record
- **Part:** decoder/three.py readings.
- **Texts:** DECODE3b.md (NOT PASSED by both: R2 per single one-way side, since per clock it reads the passing's back
  and forth as ambiguity); the Boss's ruling of 05:3x UTC (a necessary reading only, gated, never evidence for a
  turn).
- **Clock:** a clock's own click past does not fix its landing.
- **Algebra:** per single, one-way side, its pasts on the readings' ladder that recur and are followed by two
  different q, counted in parts by Rule3's carry.
- **Click world:** SHOWN on stage 1's third click (54 of 54), NOT SHOWN on its first (0 of 54), as the law expects; NOT
  READ with no readings file.
- **Synced?** no. Line 359 ("passes the first click at 81 of 81 clocks" is the per-clock form; the built form reads
  per side).

### D18. R1 and R2's two-record form (the seed test's reading)
- **Part:** decoder/three.py compared, twice, apart.
- **Texts:** DECODE3.md (3f) and (3g) (NOT PASSED); DECODE3d's physicist's seed-test item (NOT PASSED); the owner's seed
  test (05:5x UTC).
- **Clock:** two lays alike but for one hidden unit in one tooth.
- **Algebra:** two records' lines compared on their q alone, line for line in the schema's order.
- **Click world:** where the clicks differ and where they first part.
- **Synced?** no: not in section 3.

### D19. The swap, the label rule
- **Part:** decoder/three.py swapped.
- **Texts:** SPLIT3.md (PASSED; P2 DERIVED on the act); DECODE3.md (3e) (NOT PASSED); the Boss's label rule.
- **Clock:** two alike takers swapped in the files together with their teeth.
- **Algebra:** the second record's trains named back, lines compared on q.
- **Click world:** SHOWN for the first click (10,827 of 10,827 lines), NOT SHOWN for stage 1's turn M (apart at round
  9).
- **Synced?** no: not in section 3 (line 359 has the rule).

### D20. (3b), the Fano factor
- **Part:** not built.
- **Texts:** DECODE3b.md, DECODE3c.md, DECODE3d.md (NOT PASSED by both; DECODE3d's mathematician's B6: Pearson's rule
  needs five in both cells, landings and misses).
- **Clock:** a steady side's landings counted in windows.
- **Algebra:** variance over mean against the window's length; NOT READ below five expected in a cell.
- **Click world:** given by text, not built.
- **Synced?** no. Line 359 ("DECODE3d is being written": NOT PASSED by both at 06:0x UTC).

### D21. (3c), the takers' correlation
- **Part:** not built.
- **Texts:** DECODE3.md (3c) (NOT PASSED).
- **Clock:** two takers of one giver.
- **Algebra:** the correlation of their landings in one record.
- **Click world:** given by text, not built.
- **Synced?** no: not in ARCHITECTURE.md.

### D22. (3d), the lives
- **Part:** not built.
- **Texts:** DECODE3.md (3d) and DECODE3b's lives() (NOT PASSED).
- **Clock:** the rounds between two landings of one side.
- **Algebra:** the lives against the exponential law.
- **Click world:** given by text, not built.
- **Synced?** yes in substance (line 359: "breakup lives spread by the exponential law", owed in the clicks).

## G. The run back and the seed test

### B1. The run back
- **Part:** engine/step.py mirror and untick; runner/rewind.py; the end line's "exact". On node-edge the edge teeth run
  back from the forward run's end teeth (the end's "teeth"); restarted at their birth they miss (its test's no).
- **Texts:** the law (Postulate 4; lines 31 and 35); EDGE2.md (the run back exact on every lay); THIRD2.md (exact at
  J5 = 0); NC29b.md (the mirror keeps every tooth, the quotients negated); HAT3.md (S/nc29/; no reader: a palindromic
  round that runs back needs a new state element).
- **Clock:** the Node-clock going backward: the same act on the mirrored state, mirrored, n rounds by n unticks.
- **Algebra:** the mirror (b, a, -1 - s) on an even row and (-b, -a, s) on an odd one, a tooth flipped to w - 1 - r;
  exact where every tooth stands within its edge's dial and the push reads no row it lands on (hypothesis (d)).
- **Click world:** the end line says whether the run back was exact, and the decoder reads it; the rounds run back
  write no click lines, only the forward run's.
- **Synced?** partly. Lines 117 and 195 do not say that the edge teeth need the end's teeth.

### B2. The seed test (the owner's acceptance test)
- **Part:** not in src. Big Pic's seeds.py on bigpic-3clicks (mode 4 at 60e00972f and 04b89d07b; mode 11 at
  8a718332f); the decoder's two-record readings (D18) on node-third-readings.
- **Texts:** the owner's word of 05:5x UTC and the Boss's reading of 06:0x UTC (S/BRIEF_PAIRS.md); the law of the path
  (docs/ALGEBRA.md line 1964: "the board is deterministic but the clicks' path is not"); DECODE3d's physicist's
  seed-test item (NOT PASSED). No derivation text of the test has passed a pair.
- **Clock:** the start seed is the board with every tooth and twin at its birth; the act runs forward and the clicks
  fall as they fall; from the end seed alone, nothing kept, the board runs back by its untick and the teeth by the
  same act on the mirrored state, and reach the start seed exactly. Two lays one hidden unit apart write different
  clicks, only at that clock, and reach the same end board; so does the first click, with no draw.
- **Algebra:** the click pushes nothing into the gears (the passing is a record), so the board's run back does not
  hang on the clicks; the teeth run back by the carry's sign law. Measured on the bench: mode 4, the click world over
  500 rounds, one hidden unit moving 418, 459 and 434 click sides, all at Node-clock 0, one end board; mode 11, 300
  rounds, 397 sides, one end board.
- **Click world:** two records compared on their q (R1, R2's two-record form) show the clicks differing and where they
  part; "the same end" is a board check (the end digest).
- **Synced?** partly. Line 359 gives the test on mode 4; mode 11's run, the decoder's two-record readings and the law
  of the path are not there.

## H. The 24

### X. The 24
- **Part:** engine/kinds.py turns and kinds (node-live); the 48 lifts (node-half); tests/frame.py's images of the 24
  and A2 f72067cdf's twisted 24 on the act; node-edge: 24 of 24 on the click world's cube for state, teeth and every
  side's clicks, the Mesh teeth on turned Spokes (8 of 8 on the line, 24 on a cube in memory).
- **Texts:** the law (line 94) and its theorems; HALF2.md (the 48); SPLIT3.md (P2); KEY2.md 2.2 (the key a scalar
  under the 24; NOT PASSED); THIRD6_mode4.md (24 of 24 for mode 4, mode 4c and the five blocks); Big Pic's check24 on
  mode 11 (24 of 24 over 20 rounds, 9c78397e5).
- **Clock:** the cube's 24 turns leave a Node-clock's star the same, and every train turns by its kinds.
- **Algebra:** 24 of 216 matrices kept by Rule3's weight; the five kinds; the 48 cover each turn twice and add the
  three half-speed kinds; an edge's flow is an A1 invariant, so the 24 keep one scalar tooth per edge.
- **Click world:** OWED. Isotropy and the shadow's three dimensions read in the meetings are owed (FULLPIC's row 2);
  check24 compares turned runs' click lines on the bench, a check of the act on two records, not a decoder reading.
- **Synced?** partly. Line 331 stands; the edges' 24 and the 48 are not in section 3.

## I. The runaway's step

### W. The runaway's step (NOT_CLOSED 37)
- **Part:** not built as a step. Built: the runner names the round where a count first passes the width and writes
  nothing (node-live a66674061), and reads the wave's window from outside (runner/run.py window, wide, promised).
- **Texts:** HAT1.md, HAT2.md, HAT3.md, HAT4.md (S/nc29/; no hostile reader); STEADY1.md (S/nc29/; no reader: term 11's
  push-back has no lawful exact form); the nc29 measurer's acyclic read (the Boss's 6539314043; no text). The owner's
  answer D (05:5x: is there a mathematical miracle) and his word of 06:1x on the square-2 lay (check whether
  entanglement, the clicks and the clocks being connected, solve it).
- **Clock:** the held hand at rest swings its square, a parametric drive; the step's multiplier is m = 2 - K / W and
  its window 0 < 2 spring < 4 W; the click world's counts pass the width at round 3,752, the pair world leaves its
  window at round 740 (the run tool names 766).
- **Algebra:** HAT3: a palindromic round on a centred triple of counts, with one more count and one more tooth per gear
  of the half-stepped family, runs back exactly (pair world 1,260 rounds, click world 500) and forward past 3,752
  (3,900 of 3,900), its energy OPEN. HAT4 (06:03): the polarized discrete gradient is HAT2's form and does not close the
  run back on two slots (the pair world from round 188); the energy is not kept in whole numbers; on whole counts with
  one tooth per edge an exact run back by the same act, a dial that is the edge's own and an acyclic read cannot all
  be had. The square-2 lay: the hands' tie is indefinite where |k|^2 is below 0.8, with no lower bound.
- **Click world:** OWED. A runaway is a clock fact; the click world sees only that no record is written. Whether a tied
  pair's fall is paid through its shared teeth or the clicks has no text yet.
- **Synced?** no. Line 359 ("HAT4 looks for an exact, time-symmetric, energy-keeping step": HAT4 now reports the
  candidate is HAT2's form, not closed, and no two-slot miracle); line 335 (FULLPIC's row: "his road a finer notch,
  then the held pair above it with the hat's spring", before HAT1 to HAT4).

## J. The parts with a view OWED (19)

The click-world view alone (18):
1. M3 engine/mesh.py: the board's wave read as light (reading 7's rule).
2. M4 engine/contract.py: the rest beat as a mass (reading 8).
3. M5 engine/kinds.py: the doublets in the clicks (a click that names the row; three species' clocks).
4. M10 runner/plans.py: the tied hand's beat read as a mass.
5. T2 the teeth W: proper time (D6 needs a clock's own count; FACE2 not built).
6. T3 the grips: lengths by light's echo.
7. T4 the pull: the wave's clicks read as light (EDGE1 unread).
8. T5 the metric's push: gravity by the clocks' rates; gamma by echo delay over clock deficit.
9. T6 the vertex and the spring: the rest beat as a mass.
10. T9 the notch: no click reading at all.
11. T10 the shift and the shears: dragging and shear in the clicks.
12. T13 the frozen clock: two clicking clocks at two depths.
13. I3 the key as laid birth: what the decoder shows of the key.
14. D2 row 46: its reader cut.
15. D7 light's echo: no rule tells light's lines.
16. D8 mass: no reading.
17. X the 24: isotropy in the meetings.
18. W the runaway's step: the confinement in the clicks.

All three views (1):
19. M22 readings/__init__.py: an empty package with no role.

## K. The lines of docs/ARCHITECTURE.md to change (64)

Each line of origin/scribe-5 5c65e7ab9, with the stale words and what now stands.
1. Line 25: "the split, where a draw by the sizes chooses, the one choice built": the split is read by the structure
   (three clocks at one place, the Boss's ruling of 04:2x), and no choice is built in src.
2. Line 40: "the architect's FULLPIC, 19 parts": 22 rows (line 326). The law of the path (docs/ALGEBRA.md line 1964) is
   not entered beside the law of the choice.
3. Line 65: "built one draft branch, node-live": node-live 1794d474b plus node-half, node-onelaw, node-edge, node-third
   and node-third-readings; writer G's node-all local and unpushed.
4. Line 108: "terms 6, 12 and 13 DRAFTED, term 10 OPEN": 6, 12 and 13 DERIVED by both end readers (lines 148, 154,
   155); term 10's form in ONELAW3, not built.
5. Line 110: "BUILT at schema 1.3": 1.4 on node-edge.
6. Line 111: "the click world's block of seven readings (C5, C6)": also decoder/sides.py and decoder/three.py.
7. Line 117: "a train's own click tooth ... a click line of schema 1.3, one per round, Node-clock and train": an edge
   side's tooth at the edge key; schema 1.4's lines with sides.
8. Line 126: "q_c, k+ = carry(S, key, k)" per train; "up to three readings"; "On main the plan is empty, so J = 0": per
   edge side; monomials of any number of legs (node-onelaw); the plans read the tables since B2.
9. Line 127: "k0 c00" as the clocks' read; "the Mesh flux ... booked by no click this night": the clocks' Plan
   (node-onelaw); the Mesh's edges book it (node-edge 88b4d281c).
10. Line 128: the per-train click line; "a split click will be the draw over the parts' sizes": schema 1.4's sides; the
    three clicks by the structure.
11. Line 129: the Test line lacks test_the_tensor24_edges.py, test_the_tensor24_half.py and test_the_tensor24_lifts.py.
12. Line 144: term 2's "W = rest + the sum of the 00 slots, linear" and "proper time": the clocks' Plan; owed in the
    click world.
13. Line 145: term 3's "as the clicks read them": owed.
14. Line 146: term 4's "read in the clicks as light": owed; the Mesh's edges built.
15. Line 147: term 5 opening "stands at its twelfth text"; the push as a world switch.
16. Line 148: term 6's "a writer builds it in plans.holding"; the gradient vertex "counted by no click"; "the other
    three": built as plans.edging; counted by plans.crossing; k legs.
17. Line 151: term 9's "h CHOSEN as chosen.notch ... 120000"; its click cell's physics: Big Pic's rule (rest div
    Gamma); owed.
18. Line 152: term 10's "owed after G2" and "no draft yet": ONELAW3's form, named and not built.
19. Line 153: term 11's train tooth "born at half the key": the edge sides' teeth.
20. Line 154: "SPLIT2b, PASSED by its mathematician": PASSED by both, with SPLIT3.
21. Line 163: "no spring is laid in any world file yet; the strengths OPEN at G3": spring 10^8 laid (36fbfbbde); G3
    DERIVED.
22. Line 164: "G3's line, NOT AGREED ... the seventh text is in work": DERIVED at its fifteenth text.
23. Line 173: "its code reader owed" (node-half 0893f2f28): PASSED, S/hcr7/REPORT7.md.
24. Line 177: "its kinds among the 24's five"; "the free strengths CHOSEN by name": eight kinds on node-half; the
    strengths rule.
25. Line 179: the strengths "so that they can be played with by the files": choosing a strength is forbidden.
26. Line 189: the plans list "rows_of, holding, tying, joined and meshing" and the CHOSEN strengths: edging, crossing,
    selves, widening, load.scaled, load.kept_forms, the edge births; the strengths rule.
27. Line 196: "the click lines of schema 1.3": 1.4.
28. Line 203: "three fields no reader reads ... until schema 1.3 retires them": retired; 1.4 adds dial and birth, and
    the end's teeth.
29. Line 204: "its click lines, from G5, name a train, a Node-clock and a round": and their sides and across.
30. Line 205: "BUILT at schema 1.2 ... schema 1.3 is laid in main": 1.4 on node-edge.
31. Line 213: the decoder's Home and Test lack sides.py, three.py and their two test files.
32. Line 215: "its click lines of schema 1.3": 1.4's sides and across.
33. Line 221: reading 1's status, per-train only: the edge form closes every place.
34. Line 227: reading 7's "no world writes them": the Mesh's edges write click lines, no echo rule reads them.
35. Line 229: reading 9 "at G5": DECODE3's (3a), owed.
36. Line 230: reading 10 "at G5": R4, CHSH and no signal.
37. Line 231: reading 11, per-train only: NOT SHOWN on the edge form.
38. Line 232: reading 12, per-train only: NOT SHOWN on the edge form.
39. Line 234: "G5's clicks, each take's lay and each setting's frames": the three clicks by the structure, the pair
    event for R4.
40. Line 258: the visualizer "waits for the click lines (G5)": the lines exist; it waits on the Node-clock standing.
41. Line 304: "the decoder's four modules are owed them": six modules; records.py and measure.py lack the four layers.
42. Line 328: "On node-live 0456fa478": 1794d474b and the branches.
43. Line 334: term 6's row "both of G3's readers not passed": DERIVED.
44. Line 335: the held and tied hands' row: Big Pic's road "a finer notch, then the held pair above it": HAT1 to HAT4
    since.
45. Line 336: term 9's row "'notch' CHOSEN": Big Pic's rule.
46. Line 337: term 10's row "OPEN: no reader": ONELAW3's form.
47. Line 338: term 11's row "OPEN for four", "to build: the four-leg passing": built on node-edge.
48. Line 339: term 12's row "to build: its pick, on the owner's law question": answered at 03:37 UTC.
49. Line 341: the dial and slots' row "the act change named and not built: ... the widened given-first step ..., k-leg
    monomials ..., the units re-laid": (b), (c) and (d) built on node-onelaw; (a) and the product terms not.
50. Line 343: the families' row "node-half a18901454 ... its code reader reading": 0893f2f28, PASSED.
51. Line 344: the third click's row (THIRD2 and THIRD3; "the owner is asked the law question"; "writer C's build on
    node-third waits"): THIRD5, THIRD6 NOT PASSED, THIRD7's road, the owner's answers; node-third holds the sides guard.
52. Line 345: the record's row "to build: 1.4 only with the face": 1.4 built for the sides.
53. Line 346: the decoder's row "the fifth code reader not passed ..., writer C folding": PASSED by the seventh; sides
    and three built.
54. Line 349: light's clicks' row "to build: a lawful vertex": the Mesh's edges built; the echo owed.
55. Line 355: "node-third c01db8f90": d9ad5f6aa (S/hcr7/REPORT8.md PASSED), node-third-readings 3a446e77a, node-all
    local at c78b202e9.
56. Line 359: "Big Pic builds the one-quantum-around-the-triangle member next" (built, mode 11); "KEY2 derives which"
    (NOT PASSED by both); "HAT4 looks for" (HAT4's verdict in); "SPLIT2, the weights, is NOT PASSED" (SPLIT2b PASSED by
    both); "VARY1 is NOT PASSED by its hostile physicist (the mathematician's report owed)" (NOT PASSED by both);
    "DECODE3d is being written" (NOT PASSED by both); "node-edge 50af24bde (05:05Z, unmerged, its code reader owed)"
    (PASSED; head 88b4d281c); "the seventh code reader reads ... and the eighth's reads extend" (done, PASSED); "passes
    the first click at 81 of 81 clocks" (the built R2 reads per side); "seeds.py ... in mode 4" (mode 11 too).
57. Line 380: frame 4's "a passing for monomials of four value legs": built.
58. Line 381: frame 5's "the Mesh leg's wind uncounted": counted on node-edge.
59. Line 383: frame 7's "Replaced by: the Mesh-leg count (frame 5)": built on node-edge.
60. Line 386: frame 10's "Replaced by: Animate's readings with G5": the decoder's three-click readings.
61. Line 393: the side list's titles 4 and 29 (built) and 41 (answered).
62. Line 395: G2 "stands at its twelfth text ... the thirteenth follows": DERIVED.
63. Line 397: G3 "stands at its fourteenth text": DERIVED at its fifteenth.
64. Line 412: "Click: ... whole or split" and "Key: ... a train's click tooth": three kinds of click; the edge sides'
    teeth.

## L. Parts built but not in docs/ARCHITECTURE.md

1. decoder/sides.py, the sides guard records.paired (node-third d9ad5f6aa; the across guard at node-third-readings
   3a446e77a), with tests/test_the_tensor24_decoder_sides.py.
2. decoder/three.py, the three clicks' readings (node-third-readings 3a446e77a), with
   tests/test_the_tensor24_decoder_three.py and tools/tensor24_decode.py's --readings, --twin, --apart and --swap.
3. Term 11 on the edges (node-edge f71c19390, 50af24bde): runner/plans.py edging, the edge form of engine/step.py
   passing, the per-side teeth in engine/state.py, runner/run.py joined, meeting, teeth_of; named in section 3 nowhere
   (line 359 names the branch only).
4. The Mesh's edges (node-edge 88b4d281c): runner/plans.py crossing, engine/step.py crossing, runner/run.py crossed,
   schema 1.4's across; with tests/test_the_tensor24_edges.py. Not named anywhere.
5. Schema 1.4 (record/schema.py on node-edge): sides, across, the header's dial and birth, the end's teeth and across.
6. ONELAW3 (c), the k-leg monomials (node-onelaw f494b0aa6): engine/contract.py pushes, engine/state.py
   Plan(legs, factor, target).
7. ONELAW3 (d), the units' machinery (node-onelaw e871dfb75): runner/load.py scaled, main.py typed.
8. ONELAW3 (b), the widened given-first step (node-onelaw 08c66fd40): engine/step.py weight on the clocks' Plan.
9. node-half's pieces named only in passing (lines 173, 343 and 359), in no Home line: engine/kinds.py lifts, Halves,
   Lifts.axes, on_cosets, hamilton, turned; runner/files.py spun, halved_departures; runner/load.py kept_forms;
   runner/plans.py selves, widening; with tests/test_the_tensor24_half.py and tests/test_the_tensor24_lifts.py.
10. Big Pic's mode 11, the triangle's own tooth (bigpic-3clicks 8a718332f, 9c78397e5): a probe beside the act, not src;
    line 359 announces it as next.
