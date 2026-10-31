# Tensor24: the build plan to morning (stage 2), node-live, three writers on disjoint files

The architect, 2026-10-30, 19:0x UTC. Morning is 05:00 UTC. Every commit: its own worktree off node-live, one step, a
plain-assertion test in main's cut style (one yes and one no per generic part, no mutant tables), the hook's gate at
0 refusals (`venv314/bin/python scratchpad/t24b/tools/derivations/open_items/scribe_scan.py --base origin/main
<worktree>`), `python tools/check.py --full` with CHECK_BASE=origin/main exit 0, the two attribution lines last,
nothing in docs/ (the Boss sends the writer the ARCHITECTURE mends at the end). Numbers in the code: 0 and 1 only;
the 2 is `senses` from the star (carry(spokes.shape[0], spokes.shape[1], 0)); the half is carry(x, senses, 0); no
two spelt as a sum; no if, loop, mask or bound in engine/; load.py may branch and loop (the gate's lists); the runner
may branch outside the act. Every strength the law leaves free is a key of the universe file's "chosen" block, read
by the loader, so the owner plays with the files in the morning, not the code.

## The writers and their files (disjoint)

| Writer | Files (nobody else touches them) |
|---|---|
| A, the engine | src/tensor24/engine/step.py, state.py, contract.py, mesh.py, kinds.py; algebra/carry.py; tests/test_the_tensor24_engine.py, tests/frame.py, tests/test_the_tensor24_algebra.py, tests/test_the_tensor24_kinds.py; tools/derivations/open_items/derive/boss/term11_pass/ (the probe) |
| B, the loader, the runner and the worlds | src/tensor24/runner/load.py, plans.py (new), files.py, board.py, run.py, rounds.py, rewind.py; src/tensor24/main.py; tools/tensor24_run.py, tools/tensor24_files.py; examples/**; tools/derivations/open_items/derive/boss/click_lay/, mesh_lay/; tests/test_the_tensor24_load.py, test_the_tensor24_files.py, test_the_tensor24_run.py |
| C, the record and the decoder's basic part | src/tensor24/record/schema.py; src/tensor24/decoder/** (records.py, a new clicks.py); tools/tensor24_decode.py; tests/test_the_tensor24_decoder*.py; the night's end-to-end run script in the scratchpad and the hostile reader's checklist |

## The interfaces, fixed now so the three work in parallel

1. **The act.** `step.act(layout, s) -> (State, clicks)`, clicks an array (trains, sites) of Python integers, as today.
   `State = (a, b, r, rd, k)` as today; k the click tooth (trains, sites), KEPT by the mirror from A1 on.
2. **Layout** gains one field after `push`: `mesh: Plan`, the plan's terms with a Mesh leg (the gradient vertex of
   B5), on the same readings as `plan` (the value, the d differences, the force, the unit); J = J1 + J5 + contract(mesh).
   `Layout.click: Click(first, second, factor, target, key)` keeps its shape and becomes the passing's pairs: `first`
   and `second` the two rows of a pair of each train through K x K -> A1 (load.pairs_of's `one`, `two`), `factor` the
   form's entry (Python integers), `target` the train, `key` (trains, 1). Until B1 lands, A tests with pairs it lays.
3. **The record, schema 1.3** (C1; B4 writes it): the header's train card gains `"key"` (the train's key) and
   `"square"` (its square flag), each kind card gains `"characters"` (its trace on each of the 24 turns, in the
   turns' order) and loses `"tt"`; `"couplings"`, `"classes"` and `"draw"` leave the header; a new line kind
   `"click"` after the header, one per round, Node-clock and train with q not 0, in the order (round, site, train):
   `{"kind": "click", "round": t, "site": x, "train": n, "q": q, "tooth": [k, k_after]}`. The old "whole", "split",
   "rate" and "books" lines stay what the records read before (no run writes them), so the old readers read NOT READ
   by name on a 1.3 record and nothing of theirs is edited tonight.
4. **The loader's new plans** (B2, B5), laid from the kinds' tables and the universe's "chosen" block, three new
   keys, each a whole number of at least 0, 0 on the three worlds shipped then (the click and mesh worlds later ship
   their frames' strengths as showcases, the owner's list): `"hold"` (the held hand's tie), `"tie"`
   (the hands' tie at the Node-clock), `"mesh"` (the gradient vertex through the Mesh). FRAMES.md has each form.
5. **The run tool and the decode tool** keep their command lines.
6. **Term 5 tonight** (the final physicist's two blocking items answered by the deriver's derivation from the act's
   own energy, the Boss's frame of 19:2x UTC): the push in the books' form at dial 2 (A1b the readings, B2b the plan
   and the dial, one merged commit replacing the earlier "2K at the factor / 2 G_i centred / 1152" plan). The
   universe's "push" is 1 where the books close and 0 where there is no gravity; the well world is re-laid under it.

## The order (dependencies first), with each commit's change, test and probe

State at 00:2x UTC (the architect who took over): main moved at 00:10 UTC from 2bcf315b6 to b1a50bb33, a fast-forward
with no force, on the owner's explicit word ("yes, push now") after Sofer's APPROVED of b1a50bb33 (#2187 6536221372).
Pushed on origin/node-live b1a50bb33, the head, in order: 0 (f5e6486c8), C1 (b10d7d008), C2 (6b77872dc), B1
(c967980d0), A1 (d6ec46ff0), C3 (ac3085db4, the hand-per-quantum probe), A1b (939fa65a7), B2 (c853dee00), B4
(a9f8a440a), A2 (f72067cdf), B2b (df4fa644c), A's docstring commit (e88150989), A's folds of B1, M2 and M12
(575973a20), B3 (e8161f301, the click world), A3 (36effecd5, term 13 on the edge), C's folds (9ccbc6481: M10, M11,
M4), A's Algebra line (214739ddf: term 5's half stated once), B's folds (484fb8d72: M1 and M3, M4 and M6, M7, Sofer's
measure.py seam and the square card's winding), B5 (87f88322d, the gradient vertex and the mesh world, which closes
M5), A's docstrings (7dcb31607: state.py's Plan, Layout.mesh, the Board line and Click, the second reader's 6, A's
part) B's folds (996df846f: the second reader's 1, 2, 3, 5 and 6, B's part) and B's fold of the third reader's minors
(b1a50bb33: hcr3/REPORT.md 1, 2 and 3). Every commit of the order below is DONE but the whole; no B2c (David's hat is
not tonight's: B2c below; FRAMES.md 6). The load test stands at 155, its ceiling. The checks at 996df846f: gate5 0
refusals with the same 6 notes; the full check exit 0, 27 passed; tensor24 10 of 10, live 100 of 100, well 128 of 128
and mesh 125 of 125, each exact, digests 540e503cad44, cfef203d5dd5, 05586b5db17f and 00fd62494c9a, every record and
ledger byte-identical to 87f88322d's; the click world exact at 996df846f (rerun after the container restart): 5,000 of
5,000 rounds undone, 4,212 click lines at 2,106 places, the books 0 (the sum of q over the trains not 0 at 0 places),
the held train (2) with 0 lines, the giver (3) at (2106, 1107, 999, -108) and the taker (4) at (2106, 999, 1107, 108),
digest f351582ede39, its record and ledger byte-identical to the earlier run's; so all five worlds are measured at the
candidate's sha. Now: the audit of main for the owner (his ask of 00:3x UTC; Sofer and an independent hostile auditor;
the owner's list, first); C5, the basic click decoder (writer C, the owner's build order of 23:5x UTC; FRAMES.md 13;
built as 49e97c992), its reader NOT PASSED (the fourth hostile code reader, scratchpad/hcr4/REPORT.md: one BLOCKING,
D8 on the click world, and five MINOR), all folded in C6 on the Boss's rulings of 00:5x UTC; C6 at the top of the
road, top priority, the decoder built accordingly with the fold (FRAMES.md 13b); C5 with C6 as one small candidate
after C6's reader; then Sofer's road, the gate's own files, law line 102 and the documents, for the owner's separate
word; Big Pic's road beyond (its section below).

The second hostile code reader read f72067cdf..87f88322d (scratchpad/hcr2/REPORT.md: no BLOCKING, seven MINOR). DONE:
- A (7dcb31607): his 6, A's part, state.py's docstrings saying what the loader lays.
- B (996df846f): his 1, the vertex's load test asserting each term's second and third readings the unit (his two
  mutants, a cubic vertex and the third reading set to the first, now fail it); his 2, files.SWITCH (a whole number
  that is its own square) refusing by name any push other than 0 or 1, "0 or 1, the metric's push off or on: term 5
  claims no strength"; his 3, the odd key's reason stated as the pair's two teeth summing to key - 1 in files.py, ODD's
  message and load.py; his 5, the unit laid as -1, the readings' last row, in plans.pushing and plans.meshing, the same
  row, no record moving; his 6, B's part, files.py's Board line naming the six CHOSEN strengths and examples/README
  the five worlds.
- The architect: his 4, light's second part taking no gradient vertex, named as a price (FRAMES.md 7; NOT_CLOSED 4);
  his 7, the documents' numbers given as they stand and the two showcases put on the owner's list.

The first hostile code reader read origin/main..f72067cdf (scratchpad/hcr1/REPORT.md: one BLOCKING, thirteen MINOR).
DONE, every item folded by its writer, each with its test in the file's room:
- A (575973a20, 214739ddf): B1's engine test, the run back under the push on pushed() with the K1 read as its no, and
  the mirror theorem's hypothesis (d) (no plan reads a pushed row's momenta) in the docstrings of step.stress, act and
  untick (FRAMES.md 3; NOT_CLOSED 30); M2, the one-line no of the flipped click tooth restored (FRAMES.md 4); M12, J5
  in no train's passing named in the act's docstring (FRAMES.md 5; NOT_CLOSED 31); step.py's Algebra line stating the
  half once (Sofer's reading).
- B (484fb8d72, 87f88322d): M1, the square's pairs at the factor 0 by its square flag in plans.passing, as pushing has
  them (FRAMES.md 4); M3 and M4, the run test's pair world laid inside the room for ten beats with the taker at rest
  and keys passing, chosen by the act (Gamma 1000, the giver at its turning point at 14, the hands' tie 9600, 800
  permille of the tied spring 12000, the key 614401, 1260 rounds), no sums in its asserts; M5, closed by B5 (plans.
  meshing reads "mesh"); M6, an even key refused by name, its parity read by Rule3's carry at the senses (the star
  moved to files.py); M7, run.promises naming teeth below 1 as teeth, and the docstrings and the README mended;
  Sofer's notes on B2b (well_lay/measure.py's seam, the square card's winding).
- C (9ccbc6481): M10, the decoder refusing by name the click lines schema 1.3 rules out; M11, MINOR = len(ADDED) at 3
  named open in schema.py's Algebra line (on the owner's list, below); M4, the decoder test's twos read from the
  structure.

### Commit 0 (A, first, the critical path; ~1 h): the merge of origin/main 2bcf315b6 into node-live

DONE at 19:1x UTC: pushed as f5e6486c8 (frame 237, engine 251, load 137). The Boss's decisions: the night's ROOM
ceilings stand (frame 240, engine 300, load 140, run 300, files 310, decoder 600; load raised to 155 at 20:4x UTC for
B2b's and B5's tests alone), each file's room set to its lines
with no slack at every commit, Sofer reading them before main; the held hand (A1, A2) at part 1 approved; B6 at 01:00
without the fifth text's dial takes the model's 1152 as the named price; no clicks from the Mesh leg tonight.

- `git merge origin/main` in A's worktree. src conflicts: contract.contract (take main's zeros_like), load.lay (take
  main's GEAR-headed array AND node-live's birth/k: `return (a, b, r, rd, k), []`). Tests: take main's cut files whole
  (engine 202, frame 230, kinds 80, load 113, algebra 34) and re-lay node-live's yes and no on them in main's style:
  the engine's naive model on the edge (the 00 count first, the half-open split, the mirror by parity), the state
  with k, the click of no term (k unmoved, clicks 0), the run back where every tooth stands within its edge's dial.
  The load test: the promise on the edge, the square's parity rows, the chosen keys read. tests_shape ROOM: the Boss
  sets the budgets at the merge (proposed: frame 240, engine 300, load 140, run 300, files 310, decoder 600); the
  writer never raises one himself.
- Test: the merged suite passes; the full check exit 0; the gate 0 refusals. No new behaviour.
- B and C start now from node-live's head in their own worktrees and rebase their unpushed commits onto commit 0 when
  it lands (their files are disjoint from A's; load.py's merge conflict is one function, lay).

### Commit A1 (A; after 0): term 11's passing S, the tooth kept, Layout.mesh

- step.py: `passing(click, x, y, jx, jy)`: every train's X in the trains' shape, a gather, a product, a scattered
  sum: `np.add.at(moved, target, factor[:, None] * (x[first] * jy[second] - y[first] * jx[second]))`, the form over
  a J(b) - b J(a). The passing's J is the value-leg plan (`layout.plan`: the springs, the held hand's tie, the hands'
  tie, the notch) contracted on the Node-clock's OWN counts with the unit, `valued(x) = np.concatenate((x,
  np.ones_like(x[:1], dtype=object)))` and `contract(plan, valued(x), x)`: pushes() lays every leg as a value row or
  -1, the readings' last row, so the plan reads the same on this flat as on the act's, and the passing reads no Mesh
  at all (manifestly local; the Mesh plan is not in X: FRAMES.md 5). In `act`: `jb = contract(plan, valued(b), b)`,
  `ja = contract(plan, valued(a), a)`, `ja1 = contract(plan, valued(a1), a1)`, `s = passing(click, a, b, ja, jb) +
  passing(click, a1, a, ja1, ja)`, `clicks, k1 = carry(s, key, k)`. The kick's `area` leaves. The drive's J stays
  j1 + stress(...) + contract(mesh, flat, a), j1 the plan on the full readings as today.
- step.mirror: the click tooth KEPT (`k`, not `flip(k, key)`); the docstring says why (the passing is odd under the
  reversal of the round's window, so the kept tooth returns and the quotient negates: COUNT5 M1).
- state.py: Layout gains `mesh: Plan`; the docstrings of State, Click and Layout say the passing.
- Test (engine, plain assertions): one Node-clock (its own neighbour through every Spoke), two trains of a T1 hand of
  two parts, each with a spring laid as monomials in the test's own plan, a value vertex between them, the giver laid
  as a line hand: over 400 rounds (i) the two trains' q sum to 0 in every round and k_L + k_M = key - 1 is kept, (ii)
  untick(tick(s)) == s with the teeth returned, and the backward act's quotients are the negatives of the forward
  ones, (iii) a lone hand with its own spring clicks nowhere (X = 0 to the bit), (iv) the no: the click tooth flipped
  instead of kept breaks (ii) at round back 1. Budget: within the engine file's ROOM.
- Probe (A, tools/derivations/open_items/derive/boss/term11_pass/probe.py, whole numbers, on the engine's act):
  the same world for 6,000 rounds: the books 0 misses, the run back 6,000 of 6,000 with -q, the taker's course,
  and the 24 on a cube of 3 with the plan laid (the turned run equals the run turned). Output probe.txt beside it.

### Commit B1 (B; from node-live's head, rebased after 0): the plans' home and the passing's pairs

- `runner/plans.py` (new; load.py is at 376 of 400 lines): pairs_of, spread, pushing, notching move there unchanged,
  and `passing(trains, c, traces, key)` replaces `clicking`: `(one, two, entry, train) = pairs_of(...)`, returned as
  `(one, two, entry, train, key)`. load.load imports them. A pure move plus one function.
- Test (load): the passing's pairs on the example universe: every pair of a train's rows through its form once, the
  factor the table's entry (1 on the dot product), the target its train; the key the universe's.

### Commit B2 (B; after B1): term 6's frame, the coupling family, generic by character

- files.UNIVERSE["chosen"] gains "hold", "tie", "mesh" (NONE_BELOW); the three shipped universes gain them at 0 (the
  gate notes KEYS for Sofer, no refusal).
- The loader refuses a second square train by name (term 5's final mathematician, item 1: with two square trains the
  clock's reads are cyclic, neither 00 row's dial stands at rest, the run back fails at round back 1 and the promise
  never fires): files.held_departures names "universe.trains: two trains of the four-vector's square's character, one
  metric family" where the square flag stands on more than one train; the test's no: a universe of light, the metric
  and a second metric is refused by that line, one metric loads.
- load.trains_of gains two flags by character, as `square` and `matter` are: `held` = 1 where the train's character
  is the held hand's (chi_A1 + chi_A2 at part 1: `carry(1, gap_held^2 + 1)`), `tied` = 1 where the character is kept
  under A2's twist (chi x chi_A2 == chi on every turn) and differs from the held hand's (lit of the gap, no complement).
- plans.holding(trains, c, traces, spokes, rest, hold, gamma): the monomials of J's potential: for every held row
  (rest; rho, rho, 1, 1), the own spring 2 rest as the theorem of the turn gives it (the leg stands twice, so the
  factor is rest); for every tied train X and held train K, (hold x f x C_yz; x_y, x_z, k_rho, k_rho) with f =
  rest div Gamma (one carry) and C the form of K x K -> A1 (pairs_of's entry); a train that is neither takes the
  factor 0. plans.tying(trains, c, traces, tie): for every pair of distinct tied trains X, Y through K x K -> A1,
  (tie x C_yz; x_y, y_z, 1, 1), a pair with no channel at the factor 0. load.load: potential = notching + holding +
  tying concatenated (factor and legs).
- **The held train holds no grip at rest** (G3's hostile physicist, item 1, g3_phys/03_report.md: with its grip the
  held hand's own spring 2 W plus the Meshes' 2 W on a checkerboard reach 4 W, the window's top, and the vacuum runs
  away on every board; FRAMES.md 6): load.laid_out lays the grips per row, shape (rows, Meshes), `np.repeat(unheld,
  trains.size)[:, None] * grip` with `unheld = lit(gap_held)` per train (1 where the character is not the held hand's,
  by the same test that gives `held`; no complement), so the held rows' Meshes hold 0 and every other row's den
  Gamma^2; mesh.held already takes a (rows, Meshes) grip. The docstring says the held train is a site-local
  oscillator, exact at every Node-clock, and names the limit: the ii slots' read still lands on its Spokes, so a world
  with the held hand keeps the push at 0 or its summed grips within the window (the runner refuses the rest by name).
- Test (load): on a universe of five trains (light (A1) x 2, the square, the held (A1, A2) x 1, two tied (T1, T2) x
  1): the flags by character (held at the held train alone, tied at the two (T1, T2) trains alone, light and the
  square 0), the held rows' own monomial at the factor rest, the tie's factor hold x f x 1 on the dot product's
  diagonal and 0 off it, light's rows in no monomial, the held rows' grips 0 at rest and den Gamma^2 on every other
  row; the no: the two (T1, T2) trains swapped in the file lay the same plan and grips.
- Probe (B, derive/boss/g3_frame/probe.py, the physicist's bench pattern, the runaway read from outside at 10^9):
  on the engine's act, a cube of 3 with Meshes (not one Node-clock), ten tied beats: the held hand's quarter turn
  exact and |k|^2 = 1 at every site; a checkerboard seed of a tied hand at A = 2 bounded past ten beats (its own
  spring plus its Meshes' 2 W below 4 W); the tied hand's period 4 sin^2(omega/2) = 2 hold f / W by zero crossings
  within the room (hold A^2 at most 0.45 quantum at peak: A = 15 at Gamma 1,000); light untied standing; the run
  back exact; the largest count over the run. G3.md's p1, p2, p6 reproduced on the loader's plan, and the
  physicist's q6b and q11 rerun on the Mesh-less held train (no runaway where his found them at 196 to 510).

### Commit A1b (A; after A1, small): the push's readings for the books' form

- step.stress reads, for the push's plan, the Node-clock's six stretches per row at the now slot (each Spoke's
  neighbour less own: `mesh.stretches(layout, a)` = seen(a, nb) - a[:, None, :], the same read the pull makes, and
  pull now uses it), the two momenta in rest-dial turns (sigma_in, sigma_out as built) and the unit:
  `flat = concatenate((stretches(layout, a).reshape(-1, sites), sigma_in, sigma_out, ones))`, the planes in that
  order: Spoke s, row r at s x rows + r; sigma_in at Spokes x rows + r; sigma_out at (Spokes + 1) x rows + r; the
  unit last. The value, difference and force planes leave the push's readings (nothing of the push reads them).
- Test (engine): stress on a laid state against its closed sums: a hand at rest with a slope g along z (the tent)
  pushes the zz slot by -(the two z-Meshes' stretches squared, 2 g^2) per row and the 00, xx, yy, jk and 0i slots
  by 0; a hand gliding alike at every site pushes the 00 slot by the read's factor times the sum over the rows but
  the 00 of sigma_in sigma_out and every ii slot by 0.

### Commit B2b (B; after B1 and A1b, before B3; the one commit that replaces the earlier B2b and B6): term 5 in the books' form at dial 2 (the deriver's derivation from the act's own energy, the Boss's frame of 19:2x UTC)

DONE at 21:00 UTC: pushed as df4fa644c, with one change from the text below by the Boss's ruling of 20:4x UTC: the
00 push reads the momenta of the rows on the force's path alone (T_d = 1: the matter and the square's 0i and jk
rows), not every row but the 00, so that no plan reads a pushed row's momenta (the mirror theorem's hypothesis (d);
the first hostile code reader's B1): the well world runs back 128 of 128; the price, the metric's self-stress not paid
into the 00 slot, 1 ppm of the matter's on the well world (NOT_CLOSED 30; FRAMES.md 3, with the two-plan road as its
alternative). Measured by its probe on the built loader at k0 = 12: dust 999999 ppm, the held tent and bump 1000000,
the free tent 1063599 and bump 1019889, the run back 12 of 12 with r_d moving, light's h_xx / h_00 1043 permille,
the clock deeper where the matter is.

- The derivation, in one line: the act's energy is H = (1/2) W v_in v_out + (1/2) SUM_Mesh grip Delta^2 with the
  reads W = rest + k0 c00 into every row but the 00 and grip = grip_rest + ii at both ends; the books close iff each
  slot is pushed by -dH/d slot: the 00 slot by the sum over every row but the 00 of sigma_in x sigma_out (the
  momenta in and out in rest-dial turns, swap-symmetric) times the read's factor k0, each ii slot by minus the sum
  over every row of its two Meshes' stretches squared at the now slot, (a(x + e_i) - a(x))^2 + (a(x) - a(x - e_i))^2
  (not the centred (D_i a)^2, which misses the Meshes at a crest or a foot: 757 permille on the tent), both halved
  by the dial 2 with the remainder kept; the jk and 0i slots by nothing, since nothing reads them (a push there is
  energy from nothing: a finding for the owner against line 35's "ten slots each pushed", NOT_CLOSED 6). Measured by
  the deriver on the live act (probe_f): the matter's loss against the metric's gain, dust 1000 permille (the built
  form 588000, the 2K-plan 1151999), a held tent and bump 1000 to eight digits, free fast matter 1133 and 1041 (the
  pairing now x next, not local in one Mesh: OPEN), the run back 12 of 12. No strength anywhere: the factor is 1.
- plans.pushing on A1b's readings: for every square train, for every row r but its 00 row, one term (sigma_in[r],
  sigma_out[r], unit) at the factor k0 x push landing on the 00 slot (k0 the clock read's factor, 1 as built: the
  chain rule carries the read's factor into the push, so one number serves both); for every row r and every Spoke
  s, one term (stretch[s, r], stretch[s, r], unit) at the factor -push landing on the ii slot of the Spoke's axis
  (the axis from the star, `along = (spokes * spokes) @ axis`, as geared reads it for the grips); no term on the jk
  and 0i slots. "push" in the universe file is 1 where the books close (gravity on) and 0 where there is none; it
  multiplies the factor and nothing else, and the docstring says a value other than 1 opens the books by that
  factor. The old blocks (whole, half, less, back, other, the jk and 0i blocks) leave.
- load.geared: the drive's teeth on the pushed rows of the square, its 00 and ii rows, are senses: per row
  `1 + pushed_row * (senses - 1)`, pushed_row the flag of those rows spread as the parity's is, 1 on every other
  row; the remainder r_d kept within [0, T_d), flipped on an even row (built at 9868ae570). The notch's monomials on
  those rows are carried by the same dial (h is CHOSEN and re-chosen with it).
- Test (load, plain assertions on the plan contracted on a laid state): the tent along z pushes the zz slot by
  -(Delta_+^2 + Delta_-^2) summed over the rows (-2 g^2 for a slope g on one row), xx and yy by 0, the 00 slot by 0,
  jk and 0i by 0 (no term lands there); the gliding hand pushes the 00 slot by k0 x the sum over the rows but the 00
  of sigma_in sigma_out and every ii slot by 0; the drive's teeth senses on the 00 and ii rows and 1 elsewhere, the
  same with the trains' order swapped; push 0 lays every factor 0.
- Probe (B, derive/boss/term5_books/probe.py: the deriver's probe_f rerun on the built loader, whole numbers): the
  matter's energy loss against the metric's gain by windows at dial 2 on dust, the held tent, the held bump and
  free fast matter (1000, 1000, 1000, 1133 / 1041 permille as he found), the run back 12 of 12 with r_d moving on
  the pushed rows; and the sign read on the well world: the 00 slot deepens where the matter is (a slower clock,
  gravity's sign) or the finding goes to the owner at once.
- The well world re-laid under the books' form (lay.py rerun with push 1 at dial 2, the notch h re-chosen so that
  the board's mean is held, written with its window, the metric at the first run's mean), the README's numbers
  moved; the live and the example worlds unchanged (push 0).
- The Boss's yes (19:2x UTC), built in this commit as a frame, the owner to confirm: the clock's read at k0 = Spokes x
  senses from the star (load.geared's clock factor),
  which GR's gamma = 1 for light needs (the deriver: light's h_ii / h_00 is 144 at k0 = 1, measured 132, and 1 at
  k0 = 12, measured 0.92; the dial 2 stands either way). It moves load.geared's one factor, the load test's pin of
  that factor, and the well world's lay and README (regenerated anyway); nothing in the act (NOT_CLOSED 26). The
  load test pins the clock's factor at Spokes x senses, from the star.

### B2c (the hat in place of the own spring): judged at 20:3x UTC: not tonight; writer B goes from B2b to B3

- David's hat (G3's eighth text, toys-5 7791470d1) stays the named next direction (FRAMES.md 6). Not tonight because,
  with the hand still, the tie's four legs open term 11's books: on B4's own pair world with the hat swapped in, 29 of
  30 rounds open and the held train clicks in 29 where the frame has 0 (the architect's check,
  arch_night/hat_check/books.txt; NOT_CLOSED 29), so B4's landed test and B3's books would fail; and f = rest div
  (Gamma R^2) is 0 once R^2 > 6 den Gamma, so the click world's integers would be re-laid. Nothing changes in B2's
  code tonight; the one fold for writer B is a docstring line in plans.holding (NOT_CLOSED 29: the tie is a monomial
  of four value legs, invisible to the passing only while the turn is exact), at his next fold.

### Commit C1 (C; from node-live's head): schema 1.3

- schema.py: `Click` dataclass (round, site, train, q, tooth: tuple[int, int]); `Kind` gains `characters:
  tuple[int, ...]` and loses `tt`; `Train` gains `key` and `square`; `Header` loses classes, couplings, draw; ADDED
  gains its third line (the click line, the key, the square flag and the characters, the couplings, classes and draw
  retired); MINOR = 3. The retired dataclasses that no run writes (Whole, Split, Rate, Books and their parts) stay
  for the records read before, as the docstring says today.
- records.py: KINDS gains "click" (after "whole", before "split": the order within a round is the schema's); `off`
  reads a click's q as any whole number (a give is below 0) and keeps the old whole click's q >= 1 rule for "whole".
- Test (decoder): a 1.3 record built in memory with two click lines reads; a click line with a tooth of three
  entries, or at a site off the board, is refused by name.

### Commit B4 (B; after B1, independent of A1): the record's click lines and the 1.3 header

- rounds.rounds yields `(state, clicks)` from `engine.act`; run.Engine gains `act` (main passes step.act);
  run.run writes, per round, `clicks(round, s, s1, out)`: one Click line per `(n, x)` in `np.argwhere(out)` with
  q = out[n, x], tooth = [s.k[n, x], s1.k[n, x]], in the order (site, train) (`np.argwhere(out.T)` walks sites
  first; records.ordered sorts by (round, kind, site, train)); the record file holds the header, the click lines in
  round order, the end; the ledger's lines unchanged. The header's train card gains `"key": layout.click.key[at, 0]` and
  `"square": train.square`; the kind cards `"characters"` (the trace of each kind on the 24 turns, the weight 1
  candidates in order: from `kinds` and `made`'s weight; B reads them off `vocabulary`'s traces); couplings, classes,
  draw leave. The ledger unchanged.
- Test (run): the example bang writes no click line (no vertex: J = 0); a tiny click world laid in the test (one
  Node-clock, two (T1, T2) hands, the held hand, hold = tie = 1 in a universe written to tmp_path) writes click lines
  whose q sum to 0 at every round and site, each line's kind, round, site, train, q and tooth whole, and the run
  back exact; the header carries key, square and characters. records.read reads it (after C1 lands; until then the
  assertion reads the lines as JSON).

### Commit C2 (C; after C1): the decoder's basic part

- decoder/clicks.py: `listed(record)`: the click lines counted: per train (its index, lines, the sum of q), per round
  and site the sum of q over the trains, the rounds where that sum is not 0 counted; plain counts, no verdict (the
  owner's word: nothing that interprets until the clicks are closed). tools/tensor24_decode.py prints it after the
  rows (which read NOT READ by name on a 1.3 record, their causes the cause lines they already have).
- Test (decoder): the counts on the in-memory record; the tool prints them and raises nothing.

### Commit C6 (C; top priority, on C5's 49e97c992, with its reader's fold): the decoder built accordingly, the click board read as meetings (FRAMES.md 13b)

- The owner's word (00:3x UTC, the Boss's translation, whole): "The board is clocks that mesh with each other. The
  click board is the clocks' meetings: each event is one quantum passing from one clock to another clock, at one
  place. There is no time axis in it; there is only the order of the events and each clock's count. Space is read in
  it only through an echo of light between clocks. To mend clocks, that is on the board. To mend a meeting of clocks,
  you look in the clicks. The decoder needs to be built accordingly. Top priority to put this in ... according to
  everything Big Pic wrote."
- The writer: C. The change, as FRAMES.md 13b has it on SHADOW's answer (a clock is the record's (site, train); the
  act holds no clock's own count): decoder/shadow.py keeps C5's shadow(record) and its four, their keys and their
  order, and grows by click_board(record), three readings on the 1.3 record, each by its own function: (a) the
  meetings (meetings), beside reading 1 and not in its place, SHOWN where every place holds one give and one take of
  one quantum, the two clocks named, the round its order alone; (b) each clock's line of meetings (clock_lines), its
  meetings counted and labelled "the order counted, no duration", its books beside it (given, taken, net); (e) space
  by light's echo between clocks (echo, reading 7), computed (the Boss's overrule: no typed verdict): NO CLICK on a
  record with no click line, otherwise NOT READ, its cause "light's echo is not read: no rule yet tells light's click
  lines from the others (reading 7, owed)" (the light rule, by character and not by name, named for later only). C5's
  four stand: (c) D6 reads NOT READ, its cause mended to "the act holds no clock's own count and 1.3 writes none; the
  click tooth is the books' remainder"; (d) the twins NOT READ, their own cause "every 1.3 clock stands at its
  Node-clock"; (f) the books beside the meetings; D8 and the books with the fourth code reader's fold (below). A
  record with no click line reads NO CLICK on all seven, the owner's phrase, before any other cause.
  tools/tensor24_decode.py prints the three in its click-world block after C5's four, under (b) one line per clock,
  the refusal line staying the block's last.
- The mend for writer C (the Boss's word with SHADOW's answer): "would need a root" struck from C5's cause, as from
  FRAMES.md 13: in shadow.py the constant NO_CLOCK renamed NO_COUNT, its text the mended cause, and D7's cause a
  constant of its own, AT_NODE; C5's own text that says 1.3 names no clock (shadow.py's Clicks layer, the docstrings
  of duration and twins, the test's name and docstring) says the mended causes; C5's assertion that D7's cause holds
  D6's becomes D7's own. Each a line for a line: C5's test file stays at 597, its ROOM unchanged.
- The fourth code reader's fold (his NOT PASSED on b1a50bb33..49e97c992, scratchpad/hcr4/REPORT.md; the Boss's rulings
  of 00:5x UTC), all in C6, as FRAMES.md 13b has it: BLOCKING 1, D8 reads NOT READ where no line could stand outside
  the lay's cone (a line at a laid site cannot, nor one at or past the board's diameter in rounds), on the click world
  "the lay's cone covers the board's 27 sites from round 0, before the first click line at round 91: no line could
  stand outside it", its test a ring of seven with two gears laid, neither at site 0, one line inside one cone only
  and one outside both; MINOR 1, the missing asserts; MINOR 2, the books in row 15's order (NOT SHOWN first with the
  gap named, then NOT READ, then SHOWN); MINOR 3, the check for a record of no click line inside each reading; MINOR
  4, laid() reading NOT READ for a gear off the board and finding the setting file by its name; MINOR 5, the 1.2 twins
  line labelled D7, the refusal printed only where the record holds no click of either kind, shadow.py's docstring
  naming only what it reads.
- The test: a second click-world test file, tests/test_the_tensor24_decoder_meetings.py, with its own ROOM entry and
  its reason line (FRAMES.md 13b), the Boss's decision under decision 26, on the owner's list (M8) with C6: (a) the
  yes a place of q = -1 and q = +1, the no a place of q = -2 and +2 and one of three lines (+1, +1 and -2), their
  books closing, the mutant that reads the sum alone; (b) the yes two clocks meeting at rounds 2 and 9, two meetings
  each with the label, the no a lone line, the mutants a duration by rounds (the yes fails it) and every line counted
  a meeting (the no fails it); (e) NOT READ with its cause on (a)'s yes record and NO CLICK with the owner's phrase on
  a record with no click line, the mutants that show SHOWN or read NO CLICK on a record with lines; and the fold's
  tests (FRAMES.md 13b). The mutants named in the commit message. The decoder test file stays at 597, its ROOM
  unchanged: the fold changes C5's click-world test a line for a line (its name and docstring, the four kinds with the
  cone NOT READ on its edge record, the causes' constants) and adds none.
- The measure: the tool run on the five worlds' records at the head, each output against FRAMES.md 13b's table. The
  click world: (f) the books SHOWN, 0 of 2,106 places off; (a) the meetings SHOWN, one give and one take at 2,106 of
  2,106 places (1,107 from train 3 to train 4, 999 the reverse); (b) SHOWN, 54 clocks of 78 meetings each, "the order
  counted, no duration", the giver's 27 each net -4 and the taker's 27 each net +4; (c) and (d) read NOT READ with
  their causes; D8 reads NOT READ, "the lay's cone covers the board's 27 sites from round 0, before the first click
  line at round 91: no line could stand outside it"; (e) light's echo NOT READ, no rule yet tells light's click lines
  from the others. The four worlds of no click line NO CLICK on all, the refusal line last.
- The checks: the gate at 0 refusals, the full check exit 0, record_code_shape on shadow.py. The reader after it: a
  hostile code reader on C5's head..C6, the fourth reader's six items checked closed, his folds by C. The road: C5
  does not go alone; C5 with C6 goes as one small candidate once C6's reader passes it.

### Commit C5 (C; tonight, after the code already read): the basic click decoder (FRAMES.md 13)

- The owner's word (his answer 3 of 23:5x UTC, the Boss's #2187 6536002736): "Build a basic decoder on the clicks that
  knows how to show the physics there"; under his law of 23:4x UTC (the click world the board's shadow, the physics
  checked there with the tools we know) and his answer 4 (the ban on a claim of physics standing on a board reading
  alone, and every claim checked twice in the click world, for everyone).
- The writer: C. The change, as FRAMES.md 13 has it: decoder/shadow.py, new, with four readings on the 1.3 record (the
  books at each click, row 15's first reading ported; D6 and D7, each NOT READ on 1.3 with its cause; D8, the cone
  check by click ported, the lay's cone alone), each SHOWN, or NOT SHOWN, or NOT READ, or NO CLICK (its cause "the
  record holds no click line: not in the click world"), a click line with no q NOT READ in the books (row 15's LACKS
  rule ported); tools/tensor24_decode.py printing them in a block after the basic listing, and the refusal line on a
  record with no click line; clicks.py, books.py, bangs.py and measure.py unchanged, measure.past and measure.meshes
  reused. Nothing new: every reading is a tool the decoder holds.
- The test: in tests/test_the_tensor24_decoder.py, each reading's yes and no, each mutant named in the commit message
  with the test failing on it; the decoder test stands at 597 lines, ROOM 597, a 25-line rise against main's 572, on
  the owner's list (M8) with C5.
- The measure: the tool run on the five worlds' records at 996df846f, each output against FRAMES.md 13's table, in the
  commit message: the click world's books SHOWN (0 of 2,106 places, the giver 2,106, 1,107, 999, -108, the taker
  2,106, 999, 1,107, 108, the held train 0 lines), D8 reads SHOWN, D6 and D7 each read NOT READ; the other four NO
  CLICK on every reading, with the refusal line.
- The checks: the gate at 0 refusals, the full check exit 0, record_code_shape on the new module.
- The reader after it: a hostile code reader on 996df846f..C5 (the diff, the laws, the five outputs against the
  table); his folds by C. Read: the fourth hostile code reader, NOT PASSED (scratchpad/hcr4/REPORT.md: one BLOCKING,
  D8 on the click world cannot fail, and five MINOR), all folded in C6 on the Boss's rulings of 00:5x UTC (FRAMES.md
  13b).
- The road: C5 follows main's b1a50bb33 as its own small candidate once its reader passes it (the Boss, 00:1x UTC).
  Now: not alone; C5 with C6, after C6's reader.

### Commit B3 (B; after B2 and B4): the click world, examples/tensor24-click/

DONE at 21:43 UTC: pushed as e8161f301 (FRAMES.md 6 has its numbers). As built, against the text below: the tie and A
chosen by the act, the tie 96000 (800 permille of the tied spring 120000, the pair's stiffness 24000 positive),
since the plan's 12000 gives a silent world (no count moves and no click falls in 5000 rounds); A = 40, inside the
room over the whole run (at most 1600 of Gamma div 4 = 2500; at A 46 and 48 the act leaves it and the held train
clicks); the key 50811429; the taker at rest. Measured: 4212 click lines, the books 0 everywhere, the held train
silent and |k|^2 = 1, the 24 at 24 of 24 with the clicks, the run back exact, the largest count 40. The envelope is
not constant: the strong tie beats on two normal modes, so the text's "tied hands' envelope constant" is withdrawn.

- The generator tools/derivations/open_items/derive/boss/click_lay/lay.py (whole numbers, Rule3, joinpath, no train
  declared in code; its account lay.txt), reading universe.json and piece.json and writing setting.json: a cube of 3,
  den 1, full_rate 10000 (rest 6 10^8, f = 60000, the tied beat 2 pi sqrt(Gamma / 2) about 444 rounds), five trains:
  light (A1, part 2) at 0, the metric at 0, the held hand (A1, A2, part 1) at (1, 0) at every site (Mesh-less, B2),
  two tied hands (T1, T2, part 1): the giver laid as a line hand at its turning point, a = b = (A, 0, 0) on T1 at
  every site, the taker at 0; every edge tooth at the dial's middle, which on the edge form is s = 0, the format's
  default (the old act's r = W div 2 is s = 0 on a still clock, EDGE2's s = 4 r - D; the coupling family's
  mathematician's 3b: the room exists only for a held tooth born there, and the probe runs the no at s = -D, where the
  turn is off at round 1 for any tied matter); A within the room the physicist measured (hold A^2 at most 0.45 quantum
  at peak, two trains sharing it: 2 hold A^2 below Gamma div 4), A = 32 at Gamma 10,000 (1024 of 1250; 0.2 quantum at
  peak); "chosen": key K, push 0, notch 0, hold 1, tie 12000 (a tenth of the tied spring 2 hold f = 120000: the pair's
  stiffness positive), mesh 0; ticks 5000, past ten tied beats (the physicist's rule). The key CHOSEN as the nearest
  odd whole to twice the one-round key the probe measures (the giver's two-round energy change per round over its
  first beat, divided so that about seven keys pass in a beat: a chosen unit of wind below the quantum, Planck's key
  being NOT_CLOSED 3), written in lay.txt with its window.
- The books hold only inside the room (NOT_CLOSED 29: the tie is a monomial of four value legs, invisible to the
  passing only while the held hand's quarter turn is exact; past the room the held train clicks alone and the books
  open, 149 of 300 rounds on B4's world run past its ticks): so A, the tie and the ticks are chosen so that both tied
  hands' squares summed at the held hand stay inside the room for the WHOLE run, the energy that moves from the giver
  to the taker included, and lay.txt writes that bound with its numbers.
- Measured on the runner's record and ledger (B's scratch measure, the runaway read from outside): the largest count
  over the run (no runaway); the click lines appear; at every round and site the sum of q over the trains is 0 (the
  pair's books); the held train's click lines counted with the others, 0 in every round (a round where it clicks is
  named with its |k|^2: the room's edge reached); the taker's course in keys; the held hand's |k|^2 = 1 at every site
  and round; the tied hands'
  envelope constant (inside the room); the run back exact; the 24 (the turned files run alike). examples/README.md
  gains the section with how each number is made and the frame's prices (FRAMES.md 6).
- Test: the files test loads the fourth folder (the examples' loop already walks examples/*).

### Commit A2 (A; after A1): the engine's tests complete, and the frame's own no

- The engine test's remaining yes and no in main's style: the act against its naive model with the held hand's
  turn and the tie (the naive model lays the monomials as the test does today), J1 + J5 + the mesh plan's
  contraction in the drive, locality (the passing reads the Node-clock's own produced counts and its six Meshes'
  before and now slots and nothing else: frame.local with three trains), purity, rename, the 24's images. One line
  per law, within the ROOM the Boss set.
- The twisted action (term 5's final mathematician, item 8; the coupling family's mathematician, item 6; the Boss's
  reading of law line 94): a turn that negates a row carries its teeth with it, the edge tooth s -> -1 - s and the
  drive tooth r_d -> T_d - 1 - r_d, the click tooth kept. DONE at f72067cdf in the engine test's own twisted(), not in
  tests/frame.turned, which still permutes sites only (the first hostile code reader's M9: this text had said
  frame.turned). The yes: the turned run equals the run turned 24 of 24 under the push with the clock moving and T_d
  above 1 on the square's rows; the no: with the teeth kept, the three turns that negate no row hold alone and the
  other 21 fail at round 1.

### Commit B5 (B; after A1 and B3): the gradient vertex and the mesh world (the Mesh-leg frame)

DONE at 22:22 UTC: pushed as 87f88322d (FRAMES.md 7 has its numbers). As built, against the text below: plans.meshing
lays V = mesh x SUM_i C_ji M_j D_i L as one potential's two pushes, L every A1 row (by character) of a train that is
no square and not the held hand, M_j every row of one part of a tied train, C the tied kind's table with the kind the
board's axes turn by onto A1 (the dot product for T1, nothing for T2); the held hand, Mesh-less, takes no gradient
vertex. The mesh world's integers chosen by the act: a ring of 180 Node-clocks at den 1 and Gamma 10000, light's
pulse, the held hand at (1, 0), a tied hand at rest, hold 1, mesh 200000, 125 ticks; the tied hand moves at 106
Node-clocks, hold |x|^2 at most 900 of 2500, the held hand's |k|^2 1, no click line, light ending at 944 permille of
its start (within 71 permille of the same files at mesh 0), the run back exact; the no: mesh 250000 leaves the room
at round 111. The price: the vertex's terms laid at the factor 0 in every world cost 10 to 30 per cent a round. The
load test at 155, its ceiling. The first reader's M5 closes.

- plans.meshing(trains, c, traces, spokes, mesh): for every pair of a scalar train L (kind A1 among its kinds, no
  square flag) and a vector hand M (kind T1 among its kinds, tied), per axis i and part: the two terms of V = mesh x
  SUM_i M_i D_i L on the readings' planes, (mesh; the plane of L's difference along i at L's row, unit, unit) landing
  on M_i's row with the factor -mesh, and (the plane of M_i's difference along i, unit, unit) landing on L's row with
  the factor +mesh (the push on the gradient leg is the gradient of the other leg, one potential's two pushes); a
  pair with no A1 x (T1 . T1) channel at the factor 0. laid_out returns it as the eleventh part; main.layout types
  it `state.Plan`.
- examples/tensor24-mesh/ by derive/boss/mesh_lay/lay.py: light (A1, part 2) as a pulse along x (the well world's
  pulse form), the held hand at (1, 0), one tied hand (T1, T2) at rest at every site, mesh = 3000 (mesh^2 below
  grip x 2 f / 2: the derivative vertex's ground state, COUNT5 P2), hold 1, tie 0, push 0, notch 0, ticks 400.
  These integers leave the room (the Boss, 21:5x UTC: mesh 1000 pushes the tied hand to 28 counts, mesh 3000 runs
  away): B chooses the world's integers by the act, as B3's were, inside the room for the whole run with the bound
  in lay.txt, or ships the world at mesh 0 (the vertex laid, its strength CHOSEN at 0), named in the README.
- Measured: light's squares summed stand (no tachyon: within a few percent over the run), the tied hand's rows move
  where the pulse passes, the run back exact; the click lines: none from the Mesh leg (its wind is the Mesh flux,
  counted by no click tonight: NOT_CLOSED 4), said in the README section.
- Test (load): the mesh plan on a two-train universe: the two pushes of one potential, -mesh on M's row from L's
  difference and +mesh on L's row from M's, per axis; light with no vector hand lays nothing.

### Commit A3 (A; if time): term 13 measured on the edge (a probe, no code)

DONE at 21:52 UTC: pushed as 36effecd5 (derive/boss/frozen_edge/probe.py and probe.txt); NOT_CLOSED 7 carries its
measure (N^2 = rest / W within 0.7 ppm at strides far above a notch) and item 23 the count-level lock-in (the
calibre condition).

- derive/boss/frozen_edge/probe.py: on the well world's lay, N^2 = rest / W by the hand's period at the crests
  against the void, and the ratio against W (TERM5_FOURTH sec. 6 asks it); the result goes to NOT_CLOSED 7.

### The whole (all three; from about 01:00 UTC)

- C runs the five worlds end to end (tensor24, live, well, click, mesh) with tools/tensor24_run.py and the decode
  tool, keeps the records and the measures in the scratchpad, and checks: every run back exact, the click world's
  lines with the books 0 at every round and site, the gate at 0 refusals on the final head, the full check exit 0;
  and reads each world's light size over its run from the ledger (the sum of squares and the largest count of
  light's rows, round by round): the coupling family's mathematician found a smooth light wave of amplitude 50 on a
  ring of 64 heating by the act's rounding from 80,180 to 4,035,064 in 3,000 rounds (max |x| 50 to 324) where the
  tied wave went 80,180 to 86,851 (NOT_CLOSED 23); a world whose light grows is named with its numbers.
- C also runs Pauli's probe (derive/boss/hand_per_quantum/probe.py, whole numbers, no src; FRAMES.md 12): two
  whole-speed hands of one kind on their springs with no tie, and one hand laid as their sum: after one round the
  momenta add exactly at every gear and site; over 1,000 rounds the summed counts part from the sum's counts by
  teeth alone (the largest gap per gear reported); with a tie between the two the one-round sum differs by exactly
  the tie's push. Output probe.txt beside it; NOT_CLOSED 28 cites it.
- C walks the hostile reader's list (ARCHITECTURE section 4) over the whole diff origin/main..node-live: a test bent
  or of nothing; a number behind a name or a count typed; a gate or a list edited; an if, a loop or a mask in the
  Node-clock; code the document does not name (listed for the writer's mends); a docstring off the four layers.
  Findings to the Boss with file and line; the writer whose file it is folds them.

## The road to main at the end

- The candidate: DONE. main moved at 00:10 UTC from 2bcf315b6 to b1a50bb33, a fast-forward with no force, on the
  owner's explicit word ("yes, push now") after Sofer's APPROVED of b1a50bb33 (#2187 6536221372). The owner's word
  covers M8, the ROOM at main: frame 237, engine 300, load 155, run 295, decoder 572 (files 310 unchanged). CI
  ("Python checks") is running on it; its result to follow.
- Next on the road, at its top: C6, top priority on the owner's word of 00:3x UTC ("The board is clocks that mesh with
  each other. The click board is the clocks' meetings ... The decoder needs to be built accordingly."), the decoder
  built accordingly (FRAMES.md 13b), with the fourth code reader's fold of C5 (his NOT PASSED on 49e97c992, the Boss's
  rulings of 00:5x UTC). C5, the basic click decoder (49e97c992), does not go alone: C5 with C6 goes as one small
  candidate after C6's reader; then Sofer's road, the gate's own files, law line 102 and the documents, not in main
  and still for the owner's separate word.
- The checks at the candidate's sha: `CHECK_BASE=origin/main python tools/check.py --full` exit 0; the hook's gate 0
  refusals, its notes listed (the KEYS notes for key, push, notch, hold, tie and mesh; B2's INDICATORs; the load
  test's PINs) for Sofer; the five worlds run by the run tool, each run back exact (tensor24, live, well, click,
  mesh), their digests beside the sha; the click world's books 0 at every round and site. At 996df846f: gate5 0
  refusals with the same 6 notes; the full check exit 0, 27 passed; tensor24, live, well and mesh exact at the digests
  above, every record and ledger byte-identical to 87f88322d's; the click world exact at 996df846f (rerun after the
  container restart): 5,000 of 5,000 rounds undone, 4,212 click lines at 2,106 places, the books 0 (the sum of q over
  the trains not 0 at 0 places), the held train (2) with 0 lines, the giver (3) at (2106, 1107, 999, -108) and the
  taker (4) at (2106, 999, 1107, 108), digest f351582ede39, its record and ledger byte-identical to the earlier run's;
  so all five worlds are measured at the candidate's sha.
- The owner's list (his word before main, or after it where main has moved):
  - FIRST, the night's first open item for the owner: his ask of 00:3x UTC for a confirmation that the code in main
    has no fake (numbers only in the approved files; no sine, cosine or formula; no enum hiding a count; the writer
    checking everything found before). A full-tree gate scan of main against the old engine base finds 2 refusals
    (SEARCH, a bracket halved: derive/david_open/node/g3_strengths.py:200 and :427, in main since 9067de20d, before
    the owner's 17:20 word) and 15 notes (LENGTH: len(WAYS) at decoder/records.py:171 and len(ADDED) at
    record/schema.py:25; INDICATOR in load.py and plans.py; PIN in the load test). Sofer and an independent hostile
    auditor audit main now; the result to follow. Its first result (#2187 6536864716, both readings, item 1 (c)): the
    well world's lay builds a cosine by the Chebyshev recurrence (derive/boss/well_lay/lay.py:49 to 60), forbidden as
    law line 102 is worded, and FRAMES.md 11's "no root and no sine" for it was false (mended); writer B re-lays the
    lump with no mode, light at rest, its well real but spreading (the held lump made none), the standing well OPEN
    (FRAMES.md 11, NOT_CLOSED 36), and the pulse at rest (P1, agreed by both readings); the 20 / 49 pair still lays
    the live and mesh worlds' pulses (NOT_CLOSED 35). The owner's ruling on line 102 (01:2x UTC) reaches frame 6's
    held spring (FRAMES.md 6, NOT_CLOSED 37).
  - M8 (the first hostile code reader), DONE for main: the owner's word of 00:10 UTC covers it, main at b1a50bb33.
    With C5, open: the decoder test's ROOM 572 -> 597, a 25-line rise against main's 572. With C6, open: the second
    click-world test file's own ROOM (the Boss's decision under decision 26), C6's tests and the fourth code reader's
    fold in it, the decoder test's 597 unchanged. tests_shape's ROOM rises against the old main, frame 230 -> 237,
    engine 202 -> 300, load 113 -> 155 (its ceiling, by B5), run 285 -> 295 (by B's fold 484fb8d72), and the decoder
    lowered 600 -> 572 (the files test 310 at main's 310); the figures re-read at 996df846f from tools/tests_shape.py
    against origin/main, unchanged. ARCHITECTURE section 4 says a ROOM is not raised with a code change; these stand
    under the Boss's ceilings of the night, named and read by Sofer, not hidden, and main takes them only on the
    owner's word (or the writer's and Sofer's, as section 4 names them).
  - M11: schema.MINOR = len(ADDED) at 3, a count behind a length with no cheap reading from the schema's structure
    (ARCHITECTURE section 6 tied reading it from the schema to 1.3); writer C names it open in schema.py's Algebra
    line (9ccbc6481).
  - The two showcases, named exceptions to "a frame's strengths are 0 in the shipped worlds" (the second hostile code
    reader's 7): the click world ships hold 1 and tie 96000 (frame 6), its showcase line saying "valid inside the
    room" (Big Pic, #2187 6535643629 item 3's last line), and the mesh world hold 1 and mesh 200000 (frame 7), as B3
    and B5 planned; the well world's push 1 and notch 120000 are term 5's and term 9's, not a frame's; the other two
    worlds hold every strength at 0 with key 1 (NOT_CLOSED 11).
  - The frames and prices that need his word, from NOT_CLOSED.md: k0 confirmed as the star's unit (26); the cut and
    the moving clock's road for his morning, its moving-clock part standing and its claim on gamma fallen (2); slow
    matter's gravity, in Big Pic's wording: on the board, the books' form gives slow matter the clocks' slowing and no
    stretch of space (gamma 0), not in the click world (32); a potential in the law, the hat's direction (19); the
    metric's self-stress against the two-plan road (30); the jk and 0i slots pushed by nothing (6); the key at depth
    (3).
  - G5's mathematician's M7, for the owner's ruling: probe (g)'s Pythagorean lay sets the hand's before slot at 48/50
    and 14/50, a rational point of the circle from (7, 1); whether law line 102's "any construction that finds one"
    reaches it is the owner's word (NOT_CLOSED 5). Big Pic's reading (#2187 6536112029): the lay (48, 14) over 50
    holds whole numbers and no angle; the bar reaches it only if (7, 1) was picked to land at an angle (its half
    angle's tangent 1/7).
  - Decision 40 (g), as Big Pic states it (#2187 6535643629 item 4): a hand that holds one quantum (D = 1) weighs W a
    Node-clock, and a still hand in a hat weighs 0 and holds none; no frame on this act has both (NOT_CLOSED 19).
  - The owner's own word of 23:4x UTC, for Big Pic first, not ruled: the third click, which "chooses a path that no
    one has chosen yet" (NOT_CLOSED 33), and a family with three hands (NOT_CLOSED 34); nothing in code tonight.
  - The Boss's decision on Sofer's question, for the owner's word: a term DERIVED on board readings keeps DERIVED, its
    row naming "board reading only"; Sofer's words of a measure now the files' (MEASURED on the board; MEASURED in the
    click world).
  - The owner's own question to Big Pic: "In the gravity problem, are you looking at it in the world of the clicks?
    Because in the clicks gravity looks different.. they are a three-dimensional space and not 4 like the board." Big
    Pic's answer: no, every gravity word is a board reading.
  - The owner's word of 00:0x UTC (the Boss's translation): the escapement is the road (FWDBACK, FWDBACK2: W = L^2 by
    itself, no root); FWDBACK3 works its runaway to a cure, then a hostile pair; the cut stays in the code tonight
    (NOT_CLOSED 2). And his principle, which Sofer enters in Solution24: a mathematical miracle usually fits the
    solution, so a refused text holding one goes to Big Pic first and back to its deriver for the problem it names,
    closed only by a theorem forbidding every cure. The Boss lists them with the candidate's sha.
- The hostile reader needs: the diff against the laws and section 4; the five worlds' records; the probes' outputs
  beside their probes in derive/boss/ (term11_pass, g3_frame, term5_books, term5_edge, term9_edge, drive_mirror,
  hand_per_quantum, frozen_edge, and the lays' accounts of well_lay, click_lay and mesh_lay); FRAMES.md and
  NOT_CLOSED.md beside the candidate, so that every CHOSEN strength and every price is read as named, not hidden.
- The writer's mends to docs/ARCHITECTURE.md (the Boss sends them): the Home, Test and Status lines of terms 1 to 4
  and 7 on the edge; term 5 DERIVED by the method, board reading only (the end's new pair reads it), its books' form
  at dial 2 with k0 = 12 and its price (hypothesis (d): the 00 push on the force's path alone); term 6's frame
  (plans.holding, tying; the flags by character; the held train Mesh-less); the gradient vertex (plans.meshing); term
  9; term 11 in the S form with the kept tooth and the click line, the value legs alone in its passing (no Mesh plan,
  no J5); term 13 measured on the edge; the 24's twisted action (law line 94); the record at 1.3; the decoder's basic
  part (clicks.py) and its refusals; runner/plans.py and the five worlds; the before slot read across the Mesh named
  in the Node-clock's reads (COUNT4 N6); section 6 from NOT_CLOSED.md; runner/plans.py's Home and Test lines, which no
  line of ARCHITECTURE names yet (scribe_law_check --arch: 1 departure, the first reader's M9 half and the second
  reader's note), Sofer's mend on the road to main.

## Big Pic's road beyond the night (#2187 6536273648, in his order; each step with its two click-world readings)

1. C5, the basic click decoder (FRAMES.md 13): the readings every later step is checked by.
2. The clock's cure against FWDBACK3 (NOT_CLOSED 2): the release carried in every round, every gear stepping every
   round, W = L^2 by itself; checked by two clicking clocks at two depths, each by its own count, and a wave crossing
   a still step read by clicks.
3. The third click on two places (FRAMES.md 14, NOT_CLOSED 33): one quantum with two places to land, its frequencies
   against the hand's squares at the click, the push on the before slot, the books and the run back.
4. The three-hand local choice (NOT_CLOSED 34): in one T1 train at one Node-clock a quantum leaving one row has two
   takers, the smallest place a click must choose.
5. The half-speed kinds laid, with the determinant weighing (NOT_CLOSED 8, 28): like half-speed quanta never two at
   one place, read in the click world with the fringes that flip and return after two turns.
6. Gravity's two halves (NOT_CLOSED 32): the clocks' half by two clicking clocks at two depths of a sourced well and
   the twins; the space half by light read by clicks.
## Timeline (UTC)

| Hour | A | B | C |
|---|---|---|---|
| 19-20 | commit 0, the merge (done) | B1 plans.py, B2 the frame's plans | C1 schema 1.3 |
| 20-22 | A1 the passing S, Layout.mesh, the kept tooth; A1b the push's readings; the probe | B4 click lines and header; B2b the books' form at dial 2 | C2 clicks.py and the tool; the tests |
| 22-00 | A2 the engine's tests complete | B3 the click world, its generator and README | the first end-to-end run of the four worlds |
| 00-02 | A3 term 13's probe; folds | the well re-laid under the books' form; B5 meshing and the mesh world | the five worlds, the gate, the full check |
| 02-04 | folds from the hostile reader | folds; README | the hostile reader's list over the whole diff |
| 04-05 | the candidate's sha to the Boss; NOT_CLOSED.md current | | the report |

At 00:0x UTC one commit is added to the night, C5, the basic click decoder (FRAMES.md 13), the owner's build order of
23:5x UTC, for writer C, its reader after it. At 22:2x UTC the work of the rows to 02:00 is DONE but the whole: every
commit pushed by 87f88322d, the first hostile code reader's items folded; left for 22:2x to 05:00: the second hostile
code reader's folds, writer C's whole (the five worlds' records and the checklist), NOT_CLOSED.md current, and the
candidate's sha to the Boss with the owner's list.
