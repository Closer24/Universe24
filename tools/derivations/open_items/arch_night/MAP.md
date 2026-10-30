# Tensor24: the map of the whole system for the night of 2026-10-30 (stage 1)

The architect, 2026-10-30, 18:5x UTC, for the Boss. The owner's words of tonight frame it: standing code of the whole
system by morning; what is not sure goes in as a FRAME, the Boss approving after the fact; the laws of locality,
whole numbers and no fakes are not broken; only generic laws, one rule for every family, read from the kinds and the
tables; the decoder only in its basic part until the clicks are closed; the Node-clock's initialization in scope; where
a part is stuck, a direction is CHOSEN and implemented completely, its strengths in the universe file, and the side
list NOT_CLOSED.md says what is not closed and who is needed.

Statuses: BUILT/main (main 2bcf315b6), BUILT/live (node-live 9868ae570, worktree scratchpad/live), DERIVED (both
readers passed; to build), DRAFTED (readers in work), FRAME (a lawful placeholder with its CHOSEN strengths), OPEN
(no lawful form tonight; the price taken is named in NOT_CLOSED.md). Paths are the worktree's. "Decoder reads"
says what the record and the ledger carry of the part, which is all the decoder may read.

## 0. The two heads and the road

- main 2bcf315b6 = 9067de20d + three commits: contract.contract zeros_like (Python integers on any gears), load.lay
  fields from GEAR, and the tests CUT to one plain test per generic part (engine 570 -> 202 lines, kinds 330 -> 80,
  load 185 -> 113, frame 265 -> 230, algebra 80 -> 34; tests_shape ROOM lowered to those). The run, files and decoder
  tests unchanged.
- node-live 9868ae570 = 9067de20d + 11 commits (the edge form, terms 5, 9, 11 drafted, the window, the live and the well
  worlds, the files' tooth range, the drive tooth's mirror by parity). Its tests are the OLD files adapted (engine 570,
  frame 264, load 184, run 285, files 310). So the first commit of the night is the merge of origin/main into
  node-live, taking main's cut tests and re-laying the edge's and the terms' yes and no on them (PLAN.md, commit 0).
  DONE at 19:1x UTC: f5e6486c8 (frame 237, engine 251, load 137); the Boss set the night's ROOM ceilings (frame
  240, engine 300, load 140, run 300, files 310, decoder 600), each file's room its lines with no slack at every
  commit, Sofer reading them before main.
- The gate: the pre-push hook runs scratchpad/t24b/tools/derivations/open_items/scribe_scan.py --hook with
  venv314; every commit is checked by the hook's gate against origin/main and by `python tools/check.py --full`
  with CHECK_BASE=origin/main. The ratchets: record_code_shape (400 lines, docstrings' four layers), tests_shape
  (ROOM), documents_gates, scribe_scan and its selftest. scribe_law_check --arch is not a ratchet (the mirror of
  docs/ARCHITECTURE.md is the writer's; the Boss sends him the Home/Test/Status mends at the end).

## 1. The parts (ARCHITECTURE section 1), each in one row

| Part | Status | Files | What it does | Decoder reads |
|---|---|---|---|---|
| World, the three files | BUILT/main (examples/tensor24), BUILT/live (tensor24-live, tensor24-well) | examples/*/universe.json, piece.json, setting.json; examples/README.md | whole numbers lay a world: the integers, the trains (name, kinds, part, pinion = den), the CHOSEN strengths, the sides, the gears | the header carries the files verbatim with digests |
| Loader (the Node-clock's initialization) | BUILT/live; two lays FRAME tonight (the held hand's tie, the hands' tie) | runner/files.py, board.py, load.py, main.py; tools/tensor24_files.py | lays every Node-clock alike from the files and the star: section 2 below | the header's train cards (kinds, part, key, square flag) |
| Node-clock (the act) | BUILT/live on the edge; terms by status in section 3 | engine/step.py, mesh.py, contract.py, kinds.py, state.py; algebra/carry.py | one act per gear per round: the pull, the drive, the kick, the momentum carried on the edge and split at the next edge, the metric's push, the notch, the click | nothing directly: the ledger's counts and the record's click lines |
| Runner | BUILT/live (promise on the edge, the window) ; click lines FRAME tonight | runner/run.py, rounds.py, rewind.py; tools/tensor24_run.py | counts the rounds from outside, reads the promise and the window before each round, writes the record and the ledger, runs back | the record (header, click lines, end) and the ledger |
| Record | BUILT at schema 1.2; schema 1.3 DERIVED-by-plan tonight | record/schema.py | the boundary: header, click lines, end; the ledger beside it | everything it reads |
| Decoder | built on records made in memory; BASIC part only tonight (the owner's word) | decoder/records.py, books.py, bangs.py, measure.py; tools/tensor24_decode.py | reads the record and the ledger from outside; tonight: reads schema 1.3's click lines and lists them, no verdict | n/a |
| Visualizer | owed (Animate's) | none | draws what the decoder reads | n/a |
| Guards | BUILT | docs/ALGEBRA.md, tools/check.py, tests_shape.py, record_code_shape.py, documents_gates.py, the gate scribe_scan.py (+ selftest), scribe_law_check.py | refuse a push that breaks a law; the tests, one per generic part and the whole once; tests/frame.turned permutes sites only today and gains the 24's twisted action (a negated row's teeth flipped) in A2 | n/a |

## 2. The initialization, part by part (the owner's word: in scope)

| Init part | Status | Files | What it does | Generic? |
|---|---|---|---|---|
| The star and the board | BUILT/main | load.star, load.geometry, board.board | the six Spokes as the + and - of each axis; the six neighbours by the wrap (Rule3); each Spoke's Mesh paired from both ends | yes: one formula per site |
| The 24 and the kinds | BUILT/main | kinds.turns, kinds.kinds, kinds.weighed, kinds.square | every matrix of three Spokes weighed by Rule3 (24 of 216); A1, A2, E, T1, T2 from the turn itself; the four-vector's square as a signed permutation | yes: from the star alone, no table typed |
| The tables C[i x k -> m] | BUILT/main | load.tables (one einsum), main.made | a channel's group sum c u u^T; u the primitive row, read where the diagonal entry divides every other, sign by Rule3's sign test; 125 channels, no seed, no search | yes |
| The kinds found by character | BUILT/main (square, matter); FRAME tonight (held, tied) | load.trains_of, files.vocabulary, files.held_departures | each train's character summed over its kinds times its part, against the square's: square = 1 where the gap is 0 (Rule3's quotient of 1 by gap^2 + 1), matter = lit(gap); tonight the same test against the held hand's character (A1 + A2) and the tied test (the character kept under A2's twist); the loader refuses a second square train by name, one metric family (t5f_math item 1: two make the clock's reads cyclic and the run back fails unseen) | yes: a character test, no name |
| The gearing (rest, s, T_k, T_d, parity) | BUILT/live | load.geared | rest = 6 den Gamma^2 (6 the Spokes); s = T_k = T_d = 1 (the force's path); parity 0 on the square's 0i rows (one time index), 1 elsewhere, by the square flag and the slot's place after the 00 slot | yes |
| The clocks' read and the grips' read | BUILT/live (the cut) | load.geared (clock, stretch) | every row reads every square train's 00 slot at factor 1 into its teeth, less its own row (lit of the rows' difference: the acyclic cut); each Spoke reads the square's ii slot of its axis at both ends of its Mesh | yes; the cut is a CHOSEN form (NOT_CLOSED 2) |
| J's plan (the potential) | BUILT/main (the vertex law); the monomials laid: term 9 BUILT/live; terms 6's ties FRAME tonight | contract.pushes, load.notching; tonight load.holding, load.tying, load.meshing | each monomial f x_a x_b x_c x_d pushes each leg by -f times the other three; the loader lays the monomials from the kinds' tables at the CHOSEN strengths | yes, when laid from the tables |
| Term 5's plan | BUILT/live in the refused form; the law's form to build (PLAN B2b) | load.pairs_of, load.spread, load.pushing (tonight plans.pushing) | the matter's stress through K x K -> A1 onto the square's slots: tonight the law's form, +S 2K on the 00 slot, -2 G_i on each ii slot, jk and 0i as built; S = Spokes x senses from the star | yes |
| The drive's dial on the square's pushed rows (term 5's books) | to build in B2b; the mirror by parity at T_d > 1 BUILT/live | load.geared (drive), step.drive, step.mirror | T_d = senses (2) on the square's 00 and ii rows, the half that -dH/d slot carries, 1 elsewhere; the remainder kept, flipped on an even row and kept on an odd one | n/a |
| The click's cross / passing | BUILT/live (the area form); DERIVED to build tonight (the passing S) | load.clicking (today), tonight load.passing | the form of each train through K x K -> A1 (pairs_of), one carry per train and Node-clock at the key | yes |
| The lay of the gears | BUILT/live | load.lay | a, b, r (the edge tooth) from the setting; r_d at 0; the click tooth k born at (key - 1) div senses | yes |
| The key, push, notch (and tonight hold, tie, mesh) | CHOSEN in the universe file | files.UNIVERSE["chosen"], load.load | the strengths the law leaves free, read by the loader, no number in the code | yes |
| The promises | BUILT/live | run.promises, run.window, step.dials, step.grips, mesh.held | before each round, read from outside: both slots' teeth at least 1 and every edge tooth within [-D, D), D = W(b) + W(a); the six Spokes' grips summed within [0, senses W] | yes |
| The files' format | BUILT/live | files.py | every rule refuses by name; the tooth's range is the runner's promise, not the format's; pinion = den; RETIRED couplings | yes |

## 3. The thirteen terms of the act (ARCHITECTURE's own list; nothing invented)

| # | Term | Status tonight | Where | One line | Decoder reads |
|---|---|---|---|---|---|
| 1 | The readings | BUILT/live | step.readings | the value, the three centred differences, the pull, the unit, at the now slot; term 5 adds the momenta in and out as two planes | the ledger's counts |
| 2 | The teeth W | BUILT/live | step.weight, step.dials, load.geared | W = rest + the 00 slot landed by the clocks' read; on the edge the dial is W(b) + W(a) in and W(a) + W(a+) out, W(a+) the 00 row's own carry first (its teeth at rest, the cut) | the 00 slot in the ledger (proper time's rate) |
| 3 | The grips | BUILT/live | mesh.held, mesh.gripped | grip = den Gamma^2 + the axis's ii slot at both ends of the Mesh, alike from both ends | the ii slots in the ledger |
| 4 | The pull F | BUILT/live | mesh.pull | the sum over the Spokes of grip (neighbour - own) at the now slot | the light's travel in the ledger |
| 5 | The metric's push | FRAME (the Boss's, 19:2x UTC): the books' form at dial 2, derived from the act's own energy by the deriver (TERM5_FIFTH.md in writing); the fourth text NOT PASSED by the final physicist (t5f_phys), PASSED by the final mathematician with eight minors (t5f_math) | step.stress (A1b: the stretches, the momenta, the unit), mesh.stretches, plans.pushing (B2b), load.geared (the dial 2 on the pushed rows) | every slot pushed by -dH/d slot of the act's energy H = (1/2) W v_in v_out + (1/2) SUM grip Delta^2: the 00 slot by k0 SUM over the rows but the 00 of sigma_in sigma_out, each ii slot by minus its two Meshes' stretches squared over every row, both at the drive's dial 2 with the remainder kept, jk and 0i by nothing; no strength ("push" 1 or 0); the books 1000 permille on dust and held sources, 1133 / 1041 on free fast matter (OPEN); the read factor k0 = 1 as built (12 for light's gamma = 1: NOT_CLOSED 26) | the wells in the ledger (the 00 and ii slots) |
| 6 | The vertex and the spring (the coupling family, G3) | the contraction BUILT/main; the ties FRAME tonight (G3.md's whole-speed part NOT PASSED by both readers: the physicist's six blocking items, g3_phys/03_report.md, and the mathematician's four, g3_math/REPORT.md: the plan laid by hand and its J telling no kind, the held hand a unit spring in substance within the room, decision 40 (g) unmet, the two ties sharing k; the frame answers the physicist's item 1 by the Mesh-less held train and the mathematician's item 1 by the flags by character, names the unit spring as its first price, and names the rest, FRAMES.md 6) | contract.pushes; tonight plans.holding (the held hand's own spring 2 rest, its rows' grips 0 at rest, and the tie hold f C x x k.k), plans.tying (the hands' tie tie C x y) | the held hand (A1, A2) turns a quarter a round at every Node-clock with no Mesh (a site-local oscillator, exact at every site, stable at every wavevector); a train whose kinds hold the pair (K, A2 K) ties to its square and beats; two tied trains exchange through the hands' tie; light (A1, A1) is untied by character; the keys 0 on the shipped worlds | the beats in the ledger; the clicks in the record |
| 7 | The drive | BUILT/live with its mirror by parity; T_d = 2 (senses) on the square's pushed rows from B2b, 1 elsewhere; at T_d = 1 the drive is the identity (q_d = J, r_d = 0 always), so its DERIVED rested on a no-op (g3_math item 13) until the dial gives it content | step.drive, step.mirror, load.geared (T_d) | q_d, r_d+ = carry(J, T_d, r_d); the tooth flipped on an even row, kept on an odd one; the dial 2 on the 00 and ii rows halves their push exactly with the remainder kept (term 5's books) | none |
| 8 | The kick | BUILT/live at T_k = 1 | step.kick, step.driven | K = s T_k q_d; the push on every gear s F + K | none |
| 9 | The volume's notch | DRAFTED (David's page); strength "notch" CHOSEN | load.notching | V9 = 2 h c00^2 + h tr^2 as monomials of J's potential on every square train; -4 h c00 on the 00 slot, -2 h tr on each ii slot | the board's mean swing in the ledger |
| 10 | The shift and the shears | OPEN (G4): the 0i and jk slots are pushed by term 5 and carried exactly, read by no gear | state (the square's rows), load.geared (the 0i parity) | no reader tonight; the price and the alternatives in NOT_CLOSED 6 | the 0i and jk slots in the ledger |
| 11 | The whole click | DERIVED for the pair at one Node-clock at the rest teeth (COUNT5.md); to build tonight in the S form; the key CHOSEN | step.act (today the area tau), tonight step.passing; load.passing; run (the click lines) | the passing S = X(S) + X(S+), X = the train's form over a J(b) - b J(a), carried at the odd key with the tooth KEPT under the mirror; the record's line carries q, and -q on the run back | the click lines: round, site, train, q, tooth before and after |
| 12 | The split click | OPEN (David's draft, both readers NOT AGREED) | none | no draw is written tonight: a share below half a key moves a tooth and clicks nowhere (the spread take is not made whole) | none |
| 13 | The frozen clock | OPEN (G2): a reading of the act, N^2 = rest / W | none of its own | where W grows without bound a clock stops; to be measured again on the edge (TERM5_FOURTH sec. 6) | the 00 slot in the ledger |

**The metric family**: the reads BUILT/live (the clock's and the grips' read), its push a FRAME tonight (term 5 in
the law's form with the books' dial, the fifth text in writing), its notch DRAFTED (term 9), its 0i and jk slots OPEN
(term 10), its own law on the 00 row OPEN under the cut (NOT_CLOSED 2). gamma is not measurable until a slow source
exists (term 6's spring: the click world has one), so "gamma = 1" is struck from every status line.

**The mass** (term 6): FRAME tonight = G3's whole-speed part: the held hand's turn (derived: the theorem of the turn,
K = 2 W), the tie through its square (the tables' row C of K x K -> A1), f = rest / Gamma CHOSEN with its reason, g
("hold") CHOSEN at 1; one beat per tied train; the half-speed tie OPEN (the spinor gear, another agent's).

**The families and the three hands**: the quaternion's settled findings are the frame (FAMILIES4.md, RECHECK.md):
the eight kinds from the 48 units of one ring (A1 the real part, T1 the sandwich, A2 = sigma(g)/g, T2, E, and the
half-speed kinds); spin 1/2's phase U(1)_I, the one charge; the contraction's group the 48 times the family's own
turn I, with the I-averaged table standing and the generic table refused; the norm tells no kind; Pauli is not in the
act (a theorem: no click refuses a second half-speed quantum without a second hand per quantum over the board or a
declared cap). No code of their own tonight: the loader's five kinds stand; the half-speed kinds are OPEN (NOT_CLOSED 8). Pauli's direction for the night is Big Pic's hand per quantum (FRAMES.md 12): one train per quantum, the family's hand their sum, the like clicks weighed by the determinant or the permanent in term 12's draw, not built while the clicks are not closed; a probe on whole-speed hands tonight (PLAN, the whole).

## 4. The record and the decoder (ARCHITECTURE section 3)

| Part | Status | What tonight | Decoder reads |
|---|---|---|---|
| Schema 1.3 | to build (DERIVED by the plan: ARCHITECTURE names it the writer's first task) | the header: each train card gains "key" and "square"; each kind its "characters" on the 24; "couplings", "classes" and "draw" retired; the click line: {"kind": "whole", "round", "site", "train", "q", "tooth": [k, k+]} | all |
| The ledger | BUILT/live | Count lines, one per round, Node-clock and train | all |
| Decoder, the basic part | to build tonight (the owner's word: only something basic) | records.read accepts 1.3 (a click's q may be below 0: a give); the tool lists the click lines and counts them per train and per round, with no verdict; the old rows (15, 46, D6 to D8) stay as they are and read NOT READ by name on a 1.3 record | the click lines |
| Decoder, the readings 1 to 10 | out of tonight's build (the clicks are not closed) | nothing | n/a |

## 5. The worlds (examples/)

| World | Status | What it shows |
|---|---|---|
| tensor24 | BUILT/main | the one bang: light (A1, part 2) and the metric at rest; push 0, notch 0, key 1; no vertex, no click |
| tensor24-live | BUILT/live | the light pulse along z at 2^40 counts, c = 1 / sqrt 6 Meshes a round, the run back exact |
| tensor24-well | BUILT/live | the held lump in whole numbers (lay.py): the well 350866 / 258119 in the 00 slot, N^2 944 / 958 permille, the pulse lagging 1.59 Meshes; the second cone named OPEN |
| tensor24-click | FRAME tonight (PLAN B3) | the pair world: the held hand (A1, A2) at (1, 0) everywhere, two tied hands (T1, T2) beating, the hands' tie between them, a line hand laid as the giver: clicks appear in the record, the books close per round and site |
| tensor24-mesh | FRAME tonight if time (PLAN B5) | light (A1) on a tied hand through the gradient vertex (the Mesh leg), stable by g^2 < grip spring / 2; its exchange is booked by no click tonight (NOT_CLOSED 4) |

## 6. Where a part works for one family only (the owner's word), and its generic frame

- The held hand and the tie: G3's probes lay the tie by hand (its Open 1). The frame: the held train found by its
  character (A1 + A2 at part 1), the tied trains by the character kept under A2's twist (chi times chi_A2 = chi: (T1,
  T2), (A1, A2), (E, E)), light (A1, A1) and the square refused by the same test; the monomials from the tables' row of
  K x K -> A1. No name, no place, no complement: lit of a character gap, as the square and the matter flags are.
- The hands' tie: every pair of distinct tied trains through K x K -> A1 at the one CHOSEN strength "tie"; a pair with
  no channel takes the factor 0.
- The gradient vertex (the Mesh leg): every pair of a scalar train (kind A1) and a vector hand (kind T1 among its
  kinds) through A1 x (T1 . T1) -> A1 at the CHOSEN strength "mesh": the tables select light to matter through the
  Mesh, since A1 x T1 has no A1 channel at the value legs.
- Term 11's form: the train's pairs through K x K -> A1 (load.pairs_of), the same form term 5 reads: one form for the
  push, the passing and the area.
- The mirror's parity: the 0i rows by the square flag and the slot's place, no name.
- Everything else already reads the kinds and the star.

## 7. What the decoder may read of each part, in one list

The header (the files, the sides, the order, the kinds with their characters, the train cards with kinds, part, key,
square flag); the click lines (round, site, train, q, tooth before and after; -q on the run back, which the record
does not write: only the forward run writes lines); the end (rounds, digest, undone, exact); the ledger's Count lines
(every train's now counts per round and Node-clock: the 00 slot for the clock's rate, the ii slots for the grips, the
0i and jk slots carried, the hands' counts for the beats and the travel). Nothing else crosses.
