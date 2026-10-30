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
6. **Term 5 tonight** (the final physicist's two blocking items answered by the deriver's derivation from the act's
   own energy, the Boss's frame of 19:2x UTC): the push in the books' form at dial 2 (A1b the readings, B2b the plan
   and the dial, one merged commit replacing the earlier "2K at the factor / 2 G_i centred / 1152" plan). The
   universe's "push" is 1 where the books close and 0 where there is no gravity; the well world is re-laid under it.

## The order (dependencies first), with each commit's change, test and probe

State at 21:2x UTC (the architect who took over): pushed on origin/node-live e88150989, in order: 0 (f5e6486c8), C1
(b10d7d008), C2 (6b77872dc), B1 (c967980d0), A1 (d6ec46ff0), C3 (ac3085db4, the hand-per-quantum probe), A1b
(939fa65a7), B2 (c853dee00), B4 (a9f8a440a), A2 (f72067cdf), B2b (df4fa644c), then A's docstring commit (e88150989:
term 5 in the books' form in the engine's docstrings, no behaviour change). The load test's ceiling is 155 from 20:4x
UTC, raised by the Boss for B2b's and B5's tests alone. No B2c: David's hat does not replace the own spring tonight
(B2c below; FRAMES.md 6). Next: B3, then B5 (writer B); writer C the hostile reader's checklist and the five worlds'
runs.

The first hostile code reader read origin/main..f72067cdf (scratchpad/hcr1/REPORT.md: one BLOCKING, thirteen MINOR);
its items go to their writers as folds, each with its test in the file's room:
- A: B1's engine test, the run back under the push on pushed() with the K1 read as its no, and the mirror theorem's
  hypothesis (d) (no plan reads a pushed row's momenta) in the docstrings of step.stress, act and untick
  (FRAMES.md 3; NOT_CLOSED 30); M2, the one-line no of the flipped click tooth restored and A1's note corrected
  (FRAMES.md 4); M12, J5 in no train's passing named in the act's docstring (FRAMES.md 5; NOT_CLOSED 31).
- B: M1, the square's pairs at the factor 0 by its square flag in plans.passing, as pushing has them (FRAMES.md 4);
  M3, the run test's pair world laid inside the room for its whole run (the taker at rest) or its window stated (its
  world bends at round 57: NOT_CLOSED 29; at its key 76801 a taker at rest clicks nowhere over 2,000 rounds, the
  architect's check, so the taker at rest goes with a smaller odd key or the test shows no click); M4, the run test's pins spelt as sums (read the 2 from the structure, or
  let the PIN notes show); M5, "mesh" refused by name above 0 until B5 lays the Mesh plan; M6, an even key refused by
  name; M7, the docstrings and the README that claim gamma = 1, a resting hand sourcing nothing, the old push
  readings, the window as SUM grip / W <= 1, and the dial printed below 0.
- C: M10, the decoder refusing by name a click line of a train with no card, of q 0, doubled (round, site, train),
  with a tooth past the key or below 0; M11, MINOR = len(ADDED) at 3 named; M4, the decoder test's pins spelt as sums.

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

### Commit B2b (B; after B1 and A1b, before B3; the one commit that replaces the earlier B2b and B6): term 5 in the
### books' form at dial 2 (the deriver's derivation from the act's own energy, the Boss's frame of 19:2x UTC)

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

### B2c (the hat in place of the own spring): judged at 20:3x UTC, NOT TONIGHT; writer B goes from B2b to B3

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

- The candidate: node-live's head after the merge of origin/main (commit 0) and the commits above; main has not
  moved since 2bcf315b6 unless the Boss says so, so the candidate fast-forwards. The Boss pushes it to tensor24-review;
  the writer reads the sha for faking and posts the approval; main moves, no force.
- The full check: `CHECK_BASE=origin/main python tools/check.py --full` exit 0 at the head; the hook's gate 0
  refusals and the KEYS notes (key, push, notch, hold, tie, mesh) for Sofer.
- For the owner's word before main (the first hostile code reader's M8): tests_shape's ROOM rises against main,
  frame 230 -> 237, engine 202 -> 299, load 113 -> 147 (its ceiling 155), run 285 -> 291, and the decoder lowered
  600 -> 572. ARCHITECTURE section 4 says a ROOM is not raised with a code change; these stand under the Boss's
  ceilings of the night, named and read by Sofer, not hidden, and main takes them only on the owner's word (or the
  writer's and Sofer's, as section 4 names them). The Boss lists them with the candidate's sha.
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
| 19-20 | commit 0, the merge (done) | B1 plans.py, B2 the frame's plans | C1 schema 1.3 |
| 20-22 | A1 the passing S, Layout.mesh, the kept tooth; A1b the push's readings; the probe | B4 click lines and header; B2b the books' form at dial 2 | C2 clicks.py and the tool; the tests |
| 22-00 | A2 the engine's tests complete | B3 the click world, its generator and README | the first end-to-end run of the four worlds |
| 00-02 | A3 term 13's probe; folds | the well re-laid under the books' form; B5 meshing and the mesh world | the five worlds, the gate, the full check |
| 02-04 | folds from the hostile reader | folds; README | the hostile reader's list over the whole diff |
| 04-05 | the candidate's sha to the Boss; NOT_CLOSED.md current | | the report |
