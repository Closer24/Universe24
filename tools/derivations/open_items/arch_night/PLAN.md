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
   keys, each a whole number of at least 0, 0 on the three shipped worlds: `"hold"` (the held hand's tie), `"tie"`
   (the hands' tie at the Node-clock), `"mesh"` (the gradient vertex through the Mesh). FRAMES.md has each form.
5. **The run tool and the decode tool** keep their command lines.
6. **Term 5 tonight** (the final physicist's two blocking items, t5f_phys/REPORT.md): the push's plan in the law's
   form (B2b, ready to build now), and its strength fixed by the books through the drive's dial on the square's rows
   (B6, as soon as the fifth text g2_t5/TERM5_FIFTH.md names the dial). The universe's "push" stays a whole number
   read by the loader: 1 the law's push at the books' dial, 0 no gravity; the well world is re-laid under it.

## The order (dependencies first), with each commit's change, test and probe

### Commit 0 (A, first, the critical path; ~1 h): the merge of origin/main 2bcf315b6 into node-live

DONE at 19:1x UTC: pushed as f5e6486c8 (frame 237, engine 251, load 137). The Boss's decisions: the night's ROOM
ceilings stand (frame 240, engine 300, load 140, run 300, files 310, decoder 600), each file's room set to its lines
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

### Commit B2b (B; after B1, before B3): term 5's push in the law's form

- plans.pushing: the blocks become the law's 2T - eta T on the matter's own stress, v (x) v for the scalar: the 00
  slot takes the momenta planes squared at the factor senses x scale x scale x f (+S 2K: the two momenta in and out,
  so `spread(so, sw, senses * whole, q00)` and `spread(to, tw, senses * whole, q00)`), each ii slot its own axis's
  difference squared at -senses x f (`spread(go, gw, senses * back, qii)`); the gradients' block on the 00 slot
  (`half`), the momenta's blocks on the ii slots (`less`) and the other axes' block (`other`) leave; the jk and 0i
  blocks stay as built. The docstring: the law's form on rho and p (00 <- rho + sum p = 2K, ii <- 2 G_i, the
  pressure read), the built -eta (v.v) gone, gamma unmeasurable until a slow source exists.
- Test (load, plain assertions on the plan contracted on a laid state): a hand at rest with a slope along z (the
  tent) pushes the 00 slot by 0, the zz slot by -senses f (D_z a)^2 and xx, yy, jk, 0i by 0; a hand gliding alike at
  every site (no gradient) pushes the 00 slot by senses S^2 f (si^2 + so^2) and every ii slot by 0; the mirror
  theorem's hypothesis (e) still holds (the plan reads the momenta as a swap-symmetric pair), so the run back 12 of
  12 (A's engine test covers the act; here one round back on a cube of 3).
- Probe (B, derive/boss/term5_law/probe.py): the physicist's probe_l and probe_s rerun on the built plan: the two
  forms agree on null matter (the travelling pulse within 6 percent) and differ on dust and the tent as his report
  says; light against the clock at u = 1/50: clock 1040, light 1040.

### Commit B6 (B; when g2_t5/TERM5_FIFTH.md names the dial; else by 01:00 UTC with the physicist's model as the
### price, NOT_CLOSED 18): term 5's strength fixed by the books through the drive's dial

- load.geared: the drive's teeth T_d on the square's rows the dial the fifth text derives, written as a product of
  the star's counts and nothing typed (the physicist's model on the law's form: 8 S^2 = senses^3 x scale^2 = 1152,
  scale = Spokes x senses), 1 on every other row: per row `1 + square_row * (dial - 1)`, the same form as the
  mirror's parity line `rd + even * (flip(rd, teeth) - rd)`, no branch, the square rows' flag the one load.geared
  already spreads over a train's rows for the parity. The remainder r_d kept within [0, T_d),
  flipped on an even row and kept on an odd one (built at 9868ae570, measured at T_d = 7 on the square's ten rows).
  universe "push" = 1 means the law's push at the dial; 0 none.
- Test (load): the drive's teeth on the square's rows equal the dial and 1 elsewhere, on the example universe and
  with the trains' order swapped; the run back with the drive's tooth moving (the engine test's own, A).
- Probe (B, derive/boss/term5_books/probe.py, whole numbers): the physicist's energy per gear 16H summed over the
  metric's rows and the matter's over windows on the gliding hand and the bump: the metric's gain over the matter's
  loss at the dial 1000 permille within the remainder's share, against 588 f and 1152 f at T_d = 1; the run back.
- The well world re-laid (lay.py rerun with push 1 at the dial, the metric at the first run's mean), the README's
  numbers moved; the live and the example worlds unchanged (push 0).

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

### Commit B3 (B; after B2 and B4): the click world, examples/tensor24-click/

- The generator tools/derivations/open_items/derive/boss/click_lay/lay.py (whole numbers, Rule3, joinpath, no train
  declared in code; its account lay.txt), reading universe.json and piece.json and writing setting.json: a cube of 3,
  den 1, full_rate 10000 (rest 6 10^8, f = 60000, the tied beat 2 pi sqrt(Gamma / 2) about 444 rounds), five trains:
  light (A1, part 2) at 0, the metric at 0, the held hand (A1, A2, part 1) at (1, 0) at every site (Mesh-less, B2),
  two tied hands (T1, T2, part 1): the giver laid as a line hand at its turning point, a = b = (A, 0, 0) on T1 at
  every site, the taker at 0; every edge tooth at the dial's middle, which on the edge form is s = 0, the format's
  default (the old act's r = W div 2 is s = 0 on a still clock, EDGE2's s = 4 r - D; the coupling family's
  mathematician's 3b: the room exists only for a held tooth born there, and the probe runs the no at s = -D, where
  the turn is off at round 1 for any tied matter); A within the room the physicist measured (hold A^2 at most 0.45 quantum at peak, two
  trains sharing it: 2 hold A^2 below Gamma div 4), A = 32 at Gamma 10,000 (1024 of 1250; 0.2 quantum at peak);
  "chosen": key K, push 0, notch 0, hold 1, tie 12000 (a tenth of the tied spring 2 hold f = 120000: the pair's
  stiffness positive), mesh 0; ticks 5000, past ten tied beats (the physicist's rule). The key CHOSEN as the nearest
  odd whole to twice the one-round key the probe measures (the giver's two-round energy change per round over its
  first beat, divided so that about seven keys pass in a beat: a chosen unit of wind below the quantum, Planck's key
  being NOT_CLOSED 3), written in lay.txt with its window.
- Measured on the runner's record and ledger (B's scratch measure, the runaway read from outside): the largest count
  over the run (no runaway); the click lines appear; at every round and site the sum of q over the trains is 0 (the
  pair's books); the taker's course in keys; the held hand's |k|^2 = 1 at every site and round; the tied hands'
  envelope constant (inside the room); the run back exact; the 24 (the turned files run alike). examples/README.md
  gains the section with how each number is made and the frame's prices (FRAMES.md 6).
- Test: the files test loads the fourth folder (the examples' loop already walks examples/*).

### Commit A2 (A; after A1): the engine's tests complete, and the frame's own no

- The engine test's remaining yes and no in main's style: the act against its naive model with the held hand's
  turn and the tie (the naive model lays the monomials as the test does today), J1 + J5 + the mesh plan's
  contraction in the drive, locality (the passing reads the Node-clock's own produced counts and its six Meshes'
  before and now slots and nothing else: frame.local with three trains), purity, rename, the 24's images. One line
  per law, within the ROOM the Boss set.
- frame.turned carries the twisted action (term 5's final mathematician, item 8; the coupling family's mathematician,
  item 6; the Boss's reading of law line 94): a turn that negates a row carries its teeth with it, the edge tooth
  s -> -1 - s and the drive tooth r_d -> T_d - 1 - r_d, the click tooth kept; today the helper permutes sites only
  and the test then holds the identity alone. The yes: the turned run equals the run turned 24 of 24 under the push
  with the clock moving and T_d above 1 on the square's rows; the no: with the teeth kept 21 of 24 fail at round 1.

### Commit B5 (B; after A1 and B3): the gradient vertex and the mesh world (the Mesh-leg frame)

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
- Measured: light's squares summed stand (no tachyon: within a few percent over the run), the tied hand's rows move
  where the pulse passes, the run back exact; the click lines: none from the Mesh leg (its wind is the Mesh flux,
  counted by no click tonight: NOT_CLOSED 4), said in the README section.
- Test (load): the mesh plan on a two-train universe: the two pushes of one potential, -mesh on M's row from L's
  difference and +mesh on L's row from M's, per axis; light with no vector hand lays nothing.

### Commit A3 (A; if time): term 13 measured on the edge (a probe, no code)

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
- C walks the hostile reader's list (ARCHITECTURE section 4) over the whole diff origin/main..node-live: a test bent
  or of nothing; a number behind a name or a count typed; a gate or a list edited; an if, a loop or a mask in the
  Node-clock; code the document does not name (listed for the writer's mends); a docstring off the four layers.
  Findings to the Boss with file and line; the writer whose file it is folds them.

## The road to main at the end

- The candidate: node-live's head after the merge of origin/main (commit 0) and the commits above; main has not
  moved since 2bcf315b6 unless the Boss says so, so the candidate fast-forwards. The Boss pushes it to tensor24-review;
  the writer reads the sha for faking and posts the approval; main moves, no force.
- The full check: `CHECK_BASE=origin/main python tools/check.py --full` exit 0 at the head; the hook's gate 0
  refusals and the KEYS notes (key, push, notch, hold, tie, mesh) for Sofer.
- The hostile reader needs: the diff against the laws and section 4; the five worlds' records; the probes'
  outputs (term11_pass, g3_frame, term5_edge, term9_edge, drive_mirror, well_lay, click_lay, mesh_lay); FRAMES.md
  and NOT_CLOSED.md beside the candidate, so that every CHOSEN strength and every price is read as named, not hidden.
- The writer's mends to docs/ARCHITECTURE.md (the Boss sends them): the Home, Test and Status lines of terms 1 to 4
  and 7 on the edge; term 5 DRAFTED with the final pair; term 6's frame (plans.holding, tying, meshing; the flags by
  character); term 9; term 11 in the S form with the kept tooth and the click line; the record at 1.3; the decoder's
  basic part (clicks.py); runner/plans.py and the five worlds; the before slot read across the Mesh named in the
  Node-clock's reads (COUNT4 N6); section 6 from NOT_CLOSED.md.

## Timeline (UTC)

| Hour | A | B | C |
|---|---|---|---|
| 19-20 | commit 0, the merge | B1 plans.py, B2 the frame's plans, B2b the law's push | C1 schema 1.3 |
| 20-22 | A1 the passing S, Layout.mesh, the kept tooth; the probe | B4 click lines and header; rebase on 0 | C2 clicks.py and the tool; the tests |
| 22-00 | A2 the engine's tests complete | B3 the click world, its generator and README | the first end-to-end run of the four worlds |
| 00-02 | A3 term 13's probe; folds | B6 the books' dial and the well re-laid; B5 meshing and the mesh world | the five worlds, the gate, the full check |
| 02-04 | folds from the hostile reader | folds; README | the hostile reader's list over the whole diff |
| 04-05 | the candidate's sha to the Boss; NOT_CLOSED.md current | | the report |
