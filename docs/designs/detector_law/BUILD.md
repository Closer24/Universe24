# The build plan of the massive record kind (`massive-record-v1`): the algebraic map of everything on the board, every sentence of the design mapped to a generic component, a world-file key and a verb, the tests' integers written before the code

The Massive Record Builder's plan of 2026-09-23 on the Boss's order (the
model owner's words of records 1381, 1414, 1418, 1421, 1423 and 1425: the
board is algebraic, the whole algebra implemented on the GameBoard,
everything generic; "we do everything by the algebra, not the reverse";
"the whole board is an implementation of the algebra; all the engine's code
is algebraic code; detector, emitter, whatever you want, are algebraic
creatures on the board that we declare, under the algebraic laws"). The
design built is [MASSIVE_RECORD.md](MASSIVE_RECORD.md) (sections 0 to 13;
its section 11 the build's order) at the design branch's head
7a82c155d6966b088cb0369963631dddec1d3d0e (its seven first scripts last
changed at 5efd67c413b83c151c99d23ce7ee7d348f8d329c, its eighth and ninth,
`massive_light_clock_relay.py` and `massive_moving_index.py`, at 7a82c155),
with Reviewer 3's gate, [PUSH_BALANCE.md](PUSH_BALANCE.md) sections 12.5
to 12.7 (03a2ba665b6df033ee5d14452ff96a4a6bb6b1a8). The module extended is
`src/event_universe/events/detector_law.py` at the build branch's head
f4a3971a6a410b8834bbdbc1d67e3d8a8bf2d0ca (the light record under the key
`detector_law`). This file is the plan, docs only; the code follows it in
the order of section 9, one pushed commit per step, on the Boss's word
"the rows are pinned: build" (the owner's word of about 14:42Z: the two
NATURE rows of section 9 verified before the engine is implemented; those
rows are the physicist's and Reviewer 3's, not this plan's). Nothing here
moves a rule of the design: where the plan reads two sentences of the
design differently, section 10 names both and the reading built, for the
Boss and the chief physicist.

Every symbol at its first use: a_now, a_before, r the record's row at a
Node (its amplitude now, one interval ago, and the remainder of the
division); S_6 the sum of the six neighbours' a_now (verb G); [num, den]
a record kind's pair on the six-neighbour term; mu the medium's gap
(cos omega_0 = num / den, omega_0 the rest frequency in radians per
interval); s the block's side in Links; g the well's depth to first order
(g = 2 (num' / den' - num / den)) and [G, g] the dielectric coupling's
two rationals; W the wheel (the rung's height 1 / W); K the drive's count
of intervals per Link; gamma_m the medium's Lorentz factor,
1 / sqrt(1 - 3 v^2) at the pace v Links per interval (the thing compared
with, never formed at run time); kappa the mode's decay rate in the medium
and 1 / kappa its extent; eps the binding depth 1 - omega_b^2 / omega_0^2
with omega_b the bound mode's frequency; I the conserved form of section
3; Q = 64 the label's scale, S the push's width, M the block's content;
L the distance between two blocks' facing cells; N_0 the light clock's
cycle in intervals.

## 0. THE ALGEBRAIC MAP: everything that can be on the board, the group object it lives in, the data the world file declares for it, the verbs that act on it, and the one generic component that implements each verb

Nothing on the board is outside this table (the owner's word of record
1425). Every verb is one of the six of [ALGEBRA.md](../../ALGEBRA.md)
chapter 2: (T) the translation of an accumulator, (B) the bilinear form
with a declared matrix, (G) the group-ring addition, (P) the permutation,
(E) the evaluation, (D) the division with the remainder kept and the
comparison. Every component is in `src/event_universe/events/detector_law.py`
unless named otherwise; a row that needs code outside the six verbs is a
FINDING (the last rows), reported and not written as a component.

| The thing on the board | The group object (ALGEBRA.md chapter 1) | The data the world file declares | The verbs that act on it | The one generic component per verb |
| --- | --- | --- | --- | --- |
| The light record (the massless kind) | one element of the group algebra Z[Z^3] of the torus's translations (its rows over the Nodes, MASSIVE_RECORD.md section 1: the interval's map the multiplication by h = (1 / 3) SUM over the six Ports [e]); its clock a character of Z_N (the family's pair on the circle of N steps) | the family: `quantum` h, `phase_per_link` [n, d] (its clock), no `pair` (the value [1, 1]); the lamp: `rate`, `wheel` [r, W], `train`; the world's `boundary` for its faces | (G) S_6; (D) the division by 3 den (den = 1) with the remainder kept; (T) the row's two columns advanced; (E) and (D) at the click (the pointer against the rung) | `_advance` (G, D, T, one vectorised step with the kind's pair arrays); `_click` with `amplitude.cell_of` (E, D) |
| The massive record kind | the same element of Z[Z^3] under the same map with the pair [num, den] on h (a gap cos omega_0 = num / den); its rest frequency a character of the time translation at k = 0 | the family: `quantum` h (the content one unit), `pair` [num, den] with den > num, `faces` (periodic by default: the torus's) | (G), (D) by 3 den, (T): the same step | `_advance` with the family's pair arrays `num_at`, `den_at` (formed once at load, section 1) |
| The foreign object as the well of the pair (the block's cells) | a finite G_48-set R of Nodes (a cube; a scalar on Nodes on which the 48 act trivially, world data like a wall's placement); the lowered pair on R | on a measured event of the massive kind: `position` (the cube's lower corner), `side` s, `pair` [num', den'] (the well) | none of its own (a declaration); the kind's (G), (D), (T) run on R with the lowered pair | `Block` (the cells; the pair arrays written on R) |
| The block's own record (its clock: the bound mode) | one element of Z[Z_N] carried by all its cells in step (the bound mode of the map at k = 0); on the board one massive record of the kind | `seed` (the record's amplitude on the cells at interval 0), `wheel` W | (G) the sum across R; (D) the comparison that counts a cycle (the sum's crossing of 0 upward) and the rung; (E) the evaluation across R at W | `Block.clock` (G, D); `Block.first_rung` (E, D) |
| The detector-emitter (a clock body: the block coupled to light) | the coupling matrix's one entry over the other record's two columns (now, before) at a cell; the response of the block's kind to a light record another element of Z[Z^3] of the massive kind | `coupling` {`G`: [n, d], `g`: [n, d]}; `emits` (the light family the block's own record sources, paid from its `held`) | (B) the entry g (a_l,now - a_l,before) on the massive row and -G (a_m,now - a_m,before) on light's row, then (D) each rational's division with the remainder kept; in motion (D) the pair [W_d^2, W_d^2 - 3 P . P] on g; the birth of the emitted record as the lamp's (T) | `couple` (B, D); `Block.motion_pair` (D); `_births` for the emitted record (T) |
| The block's momentum and step | p in Z^3 (label units), the translation group of the torus acting on R | `momentum` [P_x, P_y, P_z]; `ramp` (the pushing agent's declaration, 0 by default) | (T) the accumulator per axis gains P_a against the wall 3 Q S M; (D) the count with the remainder kept, at most one Link per interval, the tie x before y before z; the comparison 3 (P . P) < (3 Q S M)^2 | `Block.step` (T, D); the pair arrays and the cells translated by `np.roll` (T) |
| The absorbing object (the sink, POSTULATES 10 as settled by record 1421: a light record ends where a take is declared) | a declared loss on light's row at the cells: the Port's take (DESIGN.md section 5, the pair [-15, 56]) | `absorbing` true on the block (false by default, a clock body) | (T) the Port's amplitude follows the free neighbour's; (D) the pair's division with the remainder on the Port; the offer booked to the block's cell as today | the first build's receivers (`take_masks`, `_advance`), unchanged |
| The wall (the (M) mirror for light: the pair on LIGHT's record at declared cells, a gapped lump in the massless surround, evanescent inside, MASSIVE_RECORD.md section 4 and PUSH_BALANCE.md 12.7 (c)) | the same G_48-set R with a pair on light's kind's rows there | a measured event of the LIGHT family with `side` and `pair` [num', den'] (den' > num': a gap on light's record at R; no clock, no coupling) | the light kind's (G), (D), (T) with the pair on R | `Block` on the light family (the pair arrays of light's kind, the same component) |
| The lamp's insertion | the driven row at the lamp's Nodes: the clock's cosine table (a rounding declared at load) | the lamp as built | (T) the record's clock advanced, the table read; the record's norm (B) | `_drive`, `_births` (as built) |
| The board's faces | the torus Z_X x Z_Y x Z_Z per kind: a periodic axis the algebra's own; an open face a declared deviation per world: for light a sponge (the face cells with the take, as built), for the massive kind a zero face (a wall for the massive record, section 11 item 4) | the world's `boundary` (light); the massive family's `faces` | (T) the wrap on a periodic axis; the take's (T), (D) at light's open face; nothing at a zero face (the neighbour beyond reads 0) | `_shift` with the kind's wrap flags; the face cells as built |
| The books' conserved form I (a diagnostic of the board) | the leapfrog's quadratic form on the record's two columns, positive definite for den > num (section 3) | none | (B) with the declared matrix (den per Node on the squares, num on the Links), (G) the sums | `record_form` (GAMEBOARD, written under the key alone) |
| FINDING 1: the margin rule's extent | the bound mode's frequency omega_b (the largest eigenvalue of D^-1/2 (L / 3) D^-1/2 on the world's board) and cosh kappa = 3 D_out cos omega_b - 2: a transcendental of the declaration, not a verb on the state | the block's `margin` (`"pin"` or `"control"`) | none (a check of the declaration before the world runs, like MUST I's floor) | a HOST module outside the integer audit, `diagnostics/massive_record_margin.py` (a Lanczos in numpy), called by the runner before the simulation is built; the state never reads it |
| FINDING 2: the frequency and the extent read from the rows | a spectral peak (an FFT) and an envelope's 1 / e fall are readings of the board, HOST arithmetic on a record | none | none | `examples/events/massive_record/read_runs.py`, a tool, GAMEBOARD by label |
| FINDING 3: world (iv)'s N_0 as the script defines it | "A's received part" is A's record with B present less A's record alone (`massive_light_clock_relay.py`): a subtraction of two runs, a counterfactual, not a local click | none | none | reproduced as GAMEBOARD by the reading tool from two runs; the engine's DETECTOR reading of the light clock on two bodies is A's click on B's OWN emitted record (a foreign record at A, its response's rung, section 5), stated beside the script's number, never equated with it |

## 1. The rules of the build

- The key `massive_record` (true or false, false by default; the identity
  `massive-record-v1` under `hypotheses` when true). NAMING: the design
  writes "the key `massive-record-v1`"; the repository's world keys are
  `snake_case` and the identities carry the `-v1` suffix (`detector_law`
  and `detector-law-v1`, `massive_rows` and `massive-rows-v1`), so the
  key is `massive_record` and the identity `massive-record-v1`.
- OFF by default: without the key the ray law and the light record are
  unchanged byte for byte (a dedicated test pins the digests of the chain
  world of `tests/test_detector_law.py` at f4a3971a: `events` sha256
  f6b6f273d08c0a2d278fff1b2f4967ceb48e8d5b7a906d7351f86d142080372d, the
  snapshot 9787e732df52846928e55c7466f979bfbf119b40f5e1f62db0b1269f24f7e962,
  the books 1000ac3f0b5d84f26958d70cc75e9c2484ff697e45418a7a83720689fe48535a
  over 600 intervals; read at head before any line of the build was
  written, by the observer's lines, the snapshot stream and the books).
- Generic throughout: the engine implements the verbs on the group
  objects; the world file declares the kinds, their pairs, the cells, the
  couplings, the wheel and the faces; the engine never branches on a
  physical name, keeps nothing at a Node beyond the events there, and
  reintroduces no implicit default (every default is a declared value
  named in section 3).
- Integers only in `events/` (the integer audit of
  `tests/test_integer_algebra.py`; `detector_law.py` is already in its
  list); the two findings of section 0 live outside it.
- Every reading labelled by kind: a click is DETECTOR; a reading of the
  board is GAMEBOARD; the algebra's numbers are COMPUTATION; the machine's
  cost HOST. "Matches the algebra's number", never "is nature": these
  worlds check the engine against the algebra.
- The physicist's and the reviewer's files (MASSIVE_RECORD.md, DESIGN.md,
  PINS.md, PUSH_BALANCE.md) are not edited; a contradiction goes to the
  Boss (section 10).

## 2. The map: every item of the order to its component, its keys and its verbs

| The sentence (MASSIVE_RECORD.md) | The generic component | The world-file keys | The verbs | The test |
| --- | --- | --- | --- | --- |
| 1. The rule with a pair per record KIND on the six-neighbour term (section 1): `3 den a_next + r' = num S_6 - 3 den a_before + r`, `0 <= r' < 3 den` | `_advance` takes the kind's pair as two dense int64 arrays over the board, `num_at` and `den_at` (formed once at load from the family's pair and the blocks' pairs on their cells; translated with a block's step); light's kind is the value `[1, 1]`, under which the step is today's bit for bit | the family key `pair` `[num, den]` (light: absent, the value `[1, 1]`; a massive kind: `den > num`; refused without `massive_record`) | G, then D (by `3 den`, the remainder kept in `[0, 3 den)`), then T | (a), (b), (c) of section 6 |
| 1. The rule runs at every Node the kind's rows reach | the record's rows are dense arrays over the board (the first build's form); a massive record spreads as light's does | none | as above | (a), (b) |
| 1. The conserved form I read by the books, GAMEBOARD (section 3) | `record_form(live)`: the rule's invariant a_next . D a_next + a_now . D a_now - a_next . (S_6 / 3) a_now with D_x = den_x / num_x, scaled by 3 L to integers: `3 den_x (L / num_x) (a_now^2 + a_before^2)` summed over the Nodes less `L (a_now,i a_before,j + a_now,j a_before,i)` summed over the Links, L the least common multiple of the distinct numerators (at one numerator L = num and the form is section 3's line); per family in `books()` under `form` only under the key | none | B, G | (d) |
| 2. The foreign object: a declared set of cells R, a cube of side s at a position, a G_48-set (section 4) | `Block`: R the cube `position + [0, s)^3` cut to the board (the lower corner at `position`, as `_span_nodes` places a body today); the block's pair written into the pair arrays on R; every block a measured event of the massive kind (or, for the (M) wall, of the light family) with these keys | `side`, `pair` (the well: `num' / den' > num / den` on the massive kind, refused otherwise; the reversed window `num' > den'` admitted as section 4 allows, named in the record; on the light family a gap, `den' > num'`, the mirror) | none (a declaration, kind 1) | (e) |
| 2. One momentum integer per axis with its remainder, a declared tie; the step of the whole block by verb T (section 5) | `Block.step`: per axis the accumulator gains P_a per interval against the wall `3 Q S M` (the pace v_a = P_a / (3 Q S M), DESIGN.md 5.1 (a); k = 3 is P = Q S M on one axis), at most one Link per interval, the remainder kept, the sign of P_a the side; the whole block steps together: its cells and its pair region translate by T; the record's rows are NOT carried: they live on the Nodes and re-form behind the stepped cells by the rule (PUSH_BALANCE.md 12.7 (d); section 8's chain; section 10 (a)); the bound `3 (P . P) < (3 Q S M)^2` checked at load and at every change, a crossing the world's stop with a diagnostic (no clamp); the tie: x before y before z, a coincident second Link in one interval lost to the earlier axis as the frame loses it today | `momentum` (the existing key); `ramp` (an integer of intervals, 0 by default: the momentum reached from 0 by the whole part `P x t // ramp` over the ramp; the pushing agent's declaration, the design's own chain device, section 10 (e)) | T, D, the comparison | (f) |
| 2. The coupling at its cells only: the dielectric in the first-difference form both ways, one declared g with G (section 7) | at a block's cells a light record k reaching the block owns a RESPONSE record r_k of the block's massive kind (dense arrays; the massive rule at every Node they reach); per interval at the cells the massive row gains `g (a_l,now - a_l,before)` and light's row gains `-G (r_next - r_now)`, each rational FOLDED into the row's one division (section 7, MUST A at 4ef195a: the massive wall `3 den g_d` with the term `3 den g_n P delta`, light's wall `3 L` with the term `-3 G_n (L / G_d) P delta`, L the least common multiple of the blocks' G_d, one D per row per interval, the remainder in [0, wall); in motion g's denominator times the drive's pair's, the remainder rescaled `r x new // old` when a ramp changes it); the order within the interval (MUST B): the massive step reading light's `a_now - a_before` as they stand, then light's step reading the massive `a_next - a_now` just written, then both shift; the block's total record at a Node is the sum (G) of its own record and the responses; the block's own record is driven by the light records the block itself emitted (below) and by no other | `coupling` `{"G": [n, d], "g": [n, d]}` (both `[0, 1]` by default: a block that neither drives nor is driven) | B then D | (g) |
| 2. The source term the current entry (section 7): the block emits at its mode | a block that declares `emits` births one light record per cycle of its own clock, paying the light family's quantum h from its held content as a lamp does; the record's rows at the cells gain `-G (m_now - m_before)` of the block's OWN record during that cycle (the same entry); the block's own record gains `+g` of every light record it emitted (its own light's field, the radiation reaction); no train declared: the record ends as every record ends; its norm the sum over the cycle and the cells of the sourced amount squared (the first build's form of a lamp's norm) | `emits` (a light family's name; absent, no emission; refused unless the block holds that family) | B then D; the birth as the lamp's (T) | (h) |
| 2. The click of section 6: the evaluation E of the object's own record across R at the declared wheel W in the object's own count | the block's cell `measured:<number>`; per light record k the block's pointer accumulates the response's motion across R, `sum over R of (r_now - r_before)^2` per interval, the first build's raw units (section 10 (d)); the FIRST RUNG when `pointer x W >= norm_k`, the interval and the block's own count stamped on the click; the cell chosen at the record's completion by `cell_of` over the cells' pointers as today; the block's OWN COUNT its clock: one count per cycle of its total record summed across R (the sum's crossing from at most 0 to above 0), a `click` line per cycle of its own (the self-click of row (g)); the `gather` line of a light record clicked at the block carries `clock`, the block's count | `wheel` W on the block (the world's wheel by default); `seed` (an integer from 0; the amplitude unit 2^20 by default; 0 a block whose own record is silent) | E, D, G | (i), (j) |
| 2. The take on light's row only for an object declared ABSORBING (the existing Port's take, DESIGN.md section 5); no take for a clock body | an absorbing block's cells join the `absorbing` mask (the first build's receivers: light's amplitude taken at the cells, the one-way Port take with the pair `[-15, 56]`, the offer the Ports' motion booked to the block's cell); a clock body takes nothing: light's rows pass through its cells with the coupling alone; an absorbing block's coupling reads the Ports' amplitudes (the field the cells read) and emits nothing (its light rows are taken) | `absorbing` (false by default) | the take's T and D as built | (k) |
| 2. The index in motion a COMPUTATION from the drive's own count K, the pair `[K^2, K^2 - 3]` (section 7, record 1418) | the coupling's `g` carried in motion as `g x [W_d^2, W_d^2 - 3 P . P]` with W_d = 3 Q S M the drive's wall and P the block's momentum, integers the stepping cell has (on one axis with K = W_d / abs(P_a) whole exactly `[K^2, K^2 - 3]`; at rest `[1, 1]`), reduced by the gcd and applied by D; nothing declared in motion; the reading is a PREDICTION of the model as built (7a82c155: the chain read 0.63 and 0.83 of the covariant slab with the pair) | none | D | (l) |
| 3. The massive kind's faces PERIODIC by default; light's faces per the experiment (section 11 item 4) | `_shift` and `_neighbours` take the kind's own wrap flags: the massive family's from `faces`, light's from the world's `boundary` as today; the massive kind's open face is the ZERO face (the neighbour beyond reads 0, nothing booked) | the family key `faces` (`x`, `y`, `z` to `"periodic"` or `"open"`, every axis periodic by default; refused on a family without a massive pair) | none (the torus is the algebra's, ALGEBRA.md 1.6) | (m) |
| 3. The margin rule, a LOAD-TIME check (section 11 item 4, Reviewer 3's two lines) | `diagnostics/massive_record_margin.py` (FINDING 1): for every block of the massive kind the bound mode's `2 cos omega_b` as the largest eigenvalue of `D^-1/2 (L / 3) D^-1/2` on the world's own board and faces (a Lanczos in numpy, the largest Ritz value to 1e-9), then `cosh kappa = 3 D_out cos omega_b - 2`, the extent `1 / kappa`, eps, printed before the world runs; the rule: a CONTROL world's cells at least ONE extent from any non-periodic face of the massive kind and a periodic axis's side at least the block's side plus TWO extents; a PIN world's cells at least TWO extents from a non-periodic face and a periodic side at least the side plus FOUR extents; a declaration below the margin refused naming the block, the axis, the extent and the distance; an unbound block (omega_b at the gap) refused; a SILENT block (seed 0, no own record: a take line of item 6b, an absorbing block with the kind's own pair) skipped, nothing to bind; called by `events/run.py` before the simulation is built and by the preflight | `margin` on the block (`"pin"` by default; `"control"`) | none (a check of the declaration) | (n) |
| 3. The cavity of form (I), the control (section 4) | a block declared `cavity` holds its own record at 0 outside R (the mirror faces: the row beyond R read as 0 and written 0), the record inside the cells alone; moved, the faces move with the cells and the record re-forms | `cavity` (false by default) | none (a declared mirror, DESIGN.md section 5) | (o) |
| 4. The check worlds (section 11 item 3 at 7a82c155) | `examples/events/massive_record/`: the world files, `make_worlds.py`, `pins.py` (the pins before the run, printed to `pins.out`), `expectations.json` (the pins with the design script's name and SHA), `read_runs.py` (the readings by kind), README.md; the readings in `BUILD_READINGS.md` (written at step 5) | as section 5 | none | the runs are research runs, once, dated, fingerprinted; no test pins a world's number (CONTRIBUTING.md) |

## 3. The world file under the key: every declaration, its default and its refusal

- `massive_record`: true or false, false by default; any other type refused.
  Under it the loader admits the family keys `pair` and `faces` and the
  block keys below; without it each is refused as unknown.
- The amplitude bound A = 2^40 of a record's row (MUST 3, Reviewer 3): the
  rule's total at a Node, num x 6 x A + 3 x den x (A + 1), and for a
  block's rows the same with the coupling's denominator g_d folded into
  the wall, must stay below 2^63 for every declared pair, checked at load
  and refused naming the bound and the pair (the rows' amplitudes stay at
  the seed's order 2^20; the pointers alone square them, as Python
  integers).
- A family with `pair` `[num, den]`: two integers from 1, `den > num`
  (light's kind declares none and reads `[1, 1]`); such a family is the
  massive kind and needs no `phase_per_link` (its clock is its gap; the
  first build's check "every paid family needs the pair form of its clock"
  reads "every paid family without a massive pair", section 10 (f)); a
  family with `pair` and a `lamp` was refused at step 2 and is admitted
  since build 2 with the pair form of its clock, the matter lamp of
  section 11 (a massive record was born of no
  lamp: it is a block's own record or a block's response).
- A family's `faces`: `x`, `y`, `z` each `"periodic"` or `"open"`, periodic
  by default; on a family without a massive pair refused.
- A measured event with `side` is a BLOCK: `position` (the cube's lower
  corner), `family` (the massive kind: a clock body or a well; the light
  family: the (M) wall), `amount` (its content M), `momentum`, and the
  block keys: `side` (required), `pair` (required), `coupling` (`{"G":
  [n, d], "g": [n, d]}`, `[0, 1]` each by default), `wheel` (the world's
  wheel by default), `seed` (2^20 by default; 0 admitted; or, with `margin`
  declared, a list of one integer per Node of the board in x-major order,
  the bound mode's integer profile the generator writes into the file at
  the world's amplitude, the same at both levels: the pin worlds' seed of
  MASSIVE_RECORD.md section 11 item 7, the load-time check against the
  margin module's mode printed as GAMEBOARD; a profile without `margin`,
  of the wrong length or all zero refused), `absorbing`
  (false), `cavity` (false), `ramp` (0), `margin` (`"pin"`), `emits`
  (absent). Refused: `span` other than `[1, 1, 1]` with `side`; a `lamp`
  on a block; a momentum past the pace bound; `coupling`, `seed`, `emits`,
  `cavity`, `margin` or `wheel` on a block of the light family (the wall
  has no clock and no coupling); every block key on a measured event
  without `side`.
- The light family: as the first build (a paid family with the pair form
  of `phase_per_link`, its lamps with `rate`, `wheel`, `train`).
- The record: `run.json` carries `massive_record` as declared and the
  identity `massive-record-v1` under `hypotheses` when true; per family
  `pair` and `faces` only then; per block its keys only then; the books
  gain `form` per family (GAMEBOARD) only then; `events.jsonl` gains the
  block's `click` lines, a `block` line per interval per block (its total
  record's sum across R and its cells' amplitudes, GAMEBOARD, under the
  key alone) and, where a world declares `probes`, a `probe` line per
  interval (a declared Node's light amplitude, GAMEBOARD); without the key
  no line changes.

## 4. The interval's steps under the key, in the engine's order

1. The births (the lamps' as built; a block's emission at the start of a
   cycle of its own clock).
2. For every live record, light or massive, the rule's step with its
   kind's pair arrays: G, D, T (`_advance`); light's receivers and Ports
   as built; a massive record's zero faces where its family declares an
   axis open; a cavity's faces.
3. The coupling at every block's cells: the responses and the light
   records both ways; the block's own record and its emitted records both
   ways; the offers booked (the responses' motion across R into the light
   records' pointers at the block's cell; an absorbing block's Ports as
   built); the first rungs stamped with the block's count.
4. The block's clock: the total record summed across R, the cycle
   counted, the self-click line; the block's step by its drive (the cells
   and the pair arrays moved, the bound checked).
5. The completions and the clicks as built (`cell_of` over the cells).
6. The books: the lines as built and the form I per family (GAMEBOARD).
7. In every moving world the two readings of the pump's signature (the
   Boss's 16:13Z, records 1444 and 1445), GAMEBOARD diagnostics labelled
   so: light's total energy drift per interval (the light family's `form`
   in the books, its first difference), and the content of the mode
   k = 2 pi / 3 along the motion's axis (the `mode` line per interval: the
   three sums of light's total field over the Nodes of each residue class
   of the axis coordinate modulo 3, integers by verb G, under the world
   key `mode_axis` of step 5; the reading tool forms
   abs(S_0 + w S_1 + w^2 S_2)^2 with w the cube root of unity).

## 5. The check worlds at 7a82c155, in section 11's order, each a CONTROL, a PIN or a PREDICTION world, with the pins declared before any run

Every pin below is a COMPUTATION copied from a script beside the design
(its name and the SHA of its `.out`: 5efd67c413b83c151c99d23ce7ee7d348f8d329c
for the first seven, 7a82c155d6966b088cb0369963631dddec1d3d0e for the
relay and the moving index) or from the closed form the design states;
`pins.py` of the series recomputes each on the world's own board with the
margin module and prints both numbers, the world's own being the pin
(section 10 (b)); the pins file `expectations.json` is written before its
world runs. The pairs: at mu = 0.15 the medium `D_out = 1 + mu^2 / 2 =
809 / 800`, the kind `[800, 809]`; the well at full depth g = mu^2 is
`D_in = 1`, the pair `[800, 800]`; at half depth g = mu^2 / 2, `D_in =
1609 / 1600`, the kind written `[1600, 1618]` and the well `[1600, 1609]`.
At mu = 0.05: the kind `[800, 801]` (full depth `[800, 800]`) or `[1600,
1602]` (half depth `[1600, 1601]`). On the chains of (iv) and (v-m) the
design's medium `[156, 157]` (omega_0 = 0.1129, lambda_0 = 32.1 Links)
and its well `mu_in^2 = mu^2 / 2`, `den' / num' = 1 + mu^2 / 4 =
1.0031855`, the pair `[314, 315]` (1.0031847). The margin of section 2's
rule decides each world's kind: on a periodic 48^3 board the s = 20 block
(the extent 5.7) fits a pin's four extents (42.9) and the s = 28 block
(the extent 8.2) does not (60.8), so both prediction worlds declare
`margin: "control"` and say so; the pin worlds of five are (i-c) alone.

| World | Kind | The declaration | The pin (COMPUTATION) and its source | The reading, by kind |
| --- | --- | --- | --- | --- |
| (i-a) `rest_20.json`: one block at rest, mu = 0.15, s = 20, g = mu^2, a periodic 48^3 board, seed 2^20, no light, 3000 intervals (53 periods) | CONTROL (the cavity-leaning control, section 11 item 4) | `[800, 809]`, the well `[800, 800]`, `coupling` `[0, 1]`, `margin` `"control"` | `massive_board_margin.out` (96^3): omega_b 0.11066, omega_0 0.14930, eps 0.4507, kappa 0.17410, the extent 5.7 Links, the side by the rule 31; on the world's 48^3 box the module's own (the float scratch of this plan read 0.11046 and 5.73: the periodic image's shift, 0.2 percent) | GAMEBOARD: the frequency from the self-click count over the run and the spectral peak of the block line; the extent from the envelope in `state.json`; HOST separate |
| (i-b) `rest_28.json`: s = 28, g = mu^2 / 2, the same board | CONTROL | `[1600, 1618]`, the well `[1600, 1609]`, `margin` `"control"` | `massive_board_margin.out`: omega_b 0.13184, eps 0.2202, kappa 0.12175, the extent 8.2, the side 44; on 48^3 the module's own (the scratch 0.13053 and 7.94: the image's shift 1 percent) | the same |
| (i-c) the four smallest binding sides, if afforded: mu = 0.15 at s = 10 (g = mu^2) and 14 (g = mu^2 / 2); mu = 0.05 at s = 30 (g = mu^2) and 42 (g = mu^2 / 2); the side s + 4 / kappa | PIN worlds of five (at rest their clocks; in motion (ii-c)) | the pairs above; the sides 191, 206, 274, 288 (from the 96^3 and 128^3 extents 45.3, 48.0, 60.9, 61.5); `margin` `"pin"` | `massive_board_margin.out`: omega_b 0.14876, 0.14882, 0.04907, 0.04908; eps 0.0072, 0.0064, 0.0360, 0.0353; the extents beyond those boxes, the module's own on the world's box the pin | the same; the HOST cost of section 7 decides with the Boss |
| (ii-a) `moving_20.json`: the s = 20 block pushed to k = 3 (P = Q S M on x) over a ramp of 1500 intervals and a hold of 8000, a periodic 64^3 board | PREDICTION (the block form's residual: eps 0.45, cavity-leaning) | as (i-a) with `momentum` `[64 M, 0, 0]`, `ramp` 1500, `margin` `"control"` | section 8's one formula `f / f_0 = omega_b(gamma_m s, g) / (gamma_m omega_b(s, g))` on the world's own 64^3 box: 0.7831 (`massive_moving_pins.out` at 4ef195a; `pins.py` recomputes it with the margin module at the widths 24 and 25, interpolated at 24.49, to four places: 0.78314); the first-order residual `eps (gamma_m^2 - 1) / 2` = 0.113 (11 percent) on 1 / gamma_m = 0.8165, 0.7245 at first order, the band's second term only; NOT five's pin | GAMEBOARD: the block's count per interval over the hold against its rest count; the spectral peak at the co-moving centre cell |
| (ii-b) `moving_28.json`: the s = 28 block the same way | PREDICTION (eps 0.22, between the regimes) | as (i-b) with the momentum and the ramp | the formula on the world's own box: 0.8048 (`pins.py` 0.80477); the residual 0.055 (5.5 percent), 0.7712 at first order; the design's mu = 0.05 chain numbers (0.8065 the well regime at s = 12, g = mu^2 / 2; 0.7128 the cavity regime at s = 48; `massive_block_clock_motion.out`) quoted beside as the formula's own checks, not read by these worlds | the same |
| (ii-c) the four pin worlds of (i-c) pushed to k = 3, if afforded | PIN (five: 1 and 1 to the residual under one percent) | as (i-c) with the momentum and the ramp | 1 / gamma_m = 0.8165 with the residual 0.0009 to 0.0045 (eps 0.0072 to 0.036); the one formula by `pins.py` | the same |
| (iii-a) `cavity_24.json`: the rest cavity of form (I), s = 24, `cavity` true, the kind `[800, 809]`, a periodic 48^3 board | CONTROL | the block's pair the kind's own (no well; the faces are the mirror) | section 4's table at `[1, 1]`: omega 0.1257, N = 50.0 for the 24-cube; with the pair the exact separable form on the lattice `cos omega = (num / den) cos(pi / (s + 1))`: omega 0.19503, N = 32.2 (the design's "quadrature" 0.19515 to the lattice's residual) | GAMEBOARD: the count and the spectral peak |
| (iii-b) `cavity_24_moving.json`: the cavity pushed to k = 3 | CONTROL (the medium's clock) | the momentum and the ramp as (ii) | `1 / gamma_m^2 = 0.6667` (section 8's cavity limit; `massive_block_clock_motion.out`) | the same |
| (iv-a) `two_bodies.json`: the light clock on two bodies at rest, the design's chain (1400 x 1 x 1, y and z periodic, x open for light; the massive kind `[156, 157]`, its faces open on x, the wells `[314, 315]` of s = 12 at x = 500 and at L = 60 between the facing cells; A seeded at 2^20, B seeded 0; both `coupling` G `[1, 1]`, g `[1, 5]` (0.2); W 64; A `emits` light, B `emits` light; 700 intervals); and the same world without B (`two_bodies_alone.json`) | PIN of row (d) per declaration (the script's number) | as stated; A holds light content for its births | `massive_light_clock_relay.py` under the engine's seed (a flat A_0 on the emitter's cells at both levels; 5735ace, 39603502): N_0 = 235 at G g = 0.2 and 310 at G g = 0.05 (the receiver's rung crossed 11 and 13 intervals after the front), 247 with an (M) mirror partner; the design's 258 under the eigenvector seed is history; the register's 206 +- 2 NOT MET by two bodies (the design's line); section 10 (h) | GAMEBOARD: the received part by the subtraction of the two runs' block lines (FINDING 3); DETECTOR: A's click on B's emitted record (its `gather` line's `click` and `clock`), stated beside the script's 235 and never equated with it; B's first rung on A's record against the script's 11 |
| (iv-c) the two-arm relay after (iv): the CONTROL world at k = 3 with declared rigid arms (expected the theorem's gamma_m ratio between the arms times the ring-ups' ratio) and five's PIN world at k = 4 with the arms held by light's force at section 10's equilibrium and pushed over the morning's ramp, each declared as which it is in the world file (Reviewer 3 AGREED, the Boss's 15:40Z; the physicist's declarations in section 11 at 5735ace) | CONTROL; PIN | as section 11 declares | the physicist's numbers per world | DETECTOR: the arms' counts; GAMEBOARD: the pump's signature |
| (iv-b) `take_world.json`: the take world beside it, an (M) mirror (a block of the light family with `pair` `[21, 22]`, the gap 0.3: cos 0.3 = 0.9553, 21 / 22 = 0.9545) at L = 60 from a detector declared `absorbing` with a lamp (the register's light clock of DESIGN.md 6.4 under the rule) | the register's 206 +- 2 reproduced | the first build's chain of `tests/test_detector_law.py` with the mirror block in place of the far receiver | DESIGN.md 6.8 as computed: the first rung on the Port's motion 207 to 208 at 12 to 24 Links (the pin (d) 206 +- 2 as declared, inside at its edge); `massive_light_clock_relay.out` for the mirror with a body: N_0 = 238 and 236 (a body's counting form, not the take's) | DETECTOR: the lamp's click on its returned record (the `gather` line's `click` less `birth`) |
| (v) `index.json` (three worlds at g = 1 / 50, 1 / 20, 1 / 10): a chain 1400 x 1 x 1, x open (light's faces receive), the massive kind `[7, 8]` (omega_0 = 0.50536; below the honest floor N >= 21, named: a check of the coupling's algebra, `massive_dielectric_index.py`'s own choice omega_0 = 0.5), a block of side 12 at x = 900 with `seed` 0 and G `[1, 1]`, a CAVITY with the kind's own pair (the script's oscillator is held at 0 outside its cells at omega_0: a finding of step 5), the light clock `[153, 100]` on N = 64 (omega = 0.150214, lambda 24.2 Links), a lamp at x = 600, a probe at x = 1100; `index_reference.json` without the block | CONTROL of the coupling | `faces` of the massive kind open on x | the closed form `n^2 = 1 + G g / (omega_0^2 - omega^2)` with the declared integers: n = 1.0420, 1.1021, 1.1954 (the design's 1.0430, 1.1044, 1.1998 at its omega_0 = 0.5000); the design's chain read 1.034, 1.083, 1.159, 0.8 to 3.4 percent below the closed form (the faces' steps), named beside. EXPLORATORY, the 4 percent gap (the Boss's 18:08Z): the engine reads the excess n - 1 at 0.871, 0.868, 0.870 of the closed form's at the three couplings, the physicist's float scratch of the same exact form 0.830 at s = 12; the gap is NOT the window's or the probe's (the engine's window and probe are the script's, [1000, 1800] at x = 1100 from the lamp at 600; over the windows [1000, 1400], [1400, 1800] and [1200, 1600] the ratio moves by 0.5 percent at most, 0.866 to 0.874) and not the lamp's train (a train of 64 periods, the transmitted amplitude 0.989 to 0.994 of the reference over every window); what differs from the script is the SOURCE (the engine's lamp a driven Node emitting a record with a train, phase 0 at its Node, the script's a hard sine written every interval) and the integer rows (the remainders' grain at the amplitude 2^20, below 10^-6 of the rows); the candidate left is the source's form at the block's faces, to be read against the mode sum the physicist writes as (v)'s CONTROL. The pin stays the closed form | GAMEBOARD: light's transmitted phase delay at the probe over 12 cells against the reference |
| (v-m) `index_moving.json`: the moving index, the design's chain (2200 x 1 x 1, the source at 300, the probe at 1500, s = 24, `[156, 157]`, the well `[314, 315]`, g `[1, 200]`, G `[1, 1]`, light at omega = 0.035, the block at K = 3 toward the source from x = 1300 and away from x = 700, the window [3400, 4300]) | PREDICTION of the model as built | as stated; `momentum` `[Q S M / 1, 0, 0]` for K = 3, no ramp (the script steps from t = 2600 at once) | `massive_moving_index.out` at 696bab86, the same-Node form (the rows re-forming, the design's reading): the stepped well reads 0.40 (G g unchanged) and 0.50 (the drive's pair) of the covariant dielectric's phase delay head-on at K = 3, and 4.3 and 6.8 times it from behind; the engine carries the drive's pair, so its pins are the ratios 0.500 head-on on this chain and, from behind, 2.569 on this chain of 2200 (the window's halves unequal there, the script's own lines) and 6.74 on the design's longer chain of 4000 (the source at 300, the probe at 2500, the block from 1500, the window [5000, 6000]: the Boss's 6.8), a PREDICTION of the model as built, never Fizeau's; one more world at K = 4 (the momentum 48; K = 5 is no integer of the drive), no number declared for it; the block's drive begins at interval 2600 by the block key `start` (the pushing agent's declaration, as the script steps it); the engine's own ratios reported against these, never adjusted | GAMEBOARD: the lab phase delay at the probe; for every moving world the two readings of the pump's signature (section 4, step 7) |

## 6. The tests (`tests/test_massive_record.py`), one behaviour each, with the inputs and the expected integers written here before the code, and an edge case

- (a) The rule on a chain (y and z periodic of one layer, x open on 5
  Nodes, so S_6 = a_W + a_E + 4 a_now with 0 beyond the ends), the kind
  `[2, 3]` (3 den = 9): a_now = [0, 5, -7, 3, 0], a_before = [1, 0, 2, -1,
  0], r = [0, 1, 2, 0, 1]. The totals num S_6 - 9 a_before + r are [1, 27,
  -56, 19, 7]; a_next = [0, 3, -7, 2, 0] (the floor division: -56 // 9 =
  -7) and r' = [1, 0, 7, 1, 7], every r' in [0, 9). The edge case: the
  same chain at the kind `[1, 1]` gives the head's integers (3 a_next +
  r' = S_6 - 3 a_before + r) bit for bit, the existing test's random chain
  unchanged.
- (b) At a corner of an open 2 x 2 x 2 board (three neighbours, three
  zero faces), the kind `[1, 2]` (3 den = 6): at (0, 0, 0) a_now = 4 with
  the neighbours (1, 0, 0) = 3, (0, 1, 0) = -2, (0, 0, 1) = 5, a_before = 1,
  r = 5: S_6 = 6, the total 1 x 6 - 6 x 1 + 5 = 5, a_next = 0, r' = 5.
  With a_before = -2 the total is 23, a_next = 3, r' = 5.
- (c) Light's pair `[1, 1]` on the first build's random chain: the total,
  the quotient and the remainder equal to the existing test's, and the
  chain world's digests of section 1 unchanged with the key declared on a
  world that has no massive family.
- (d) The conserved form I on a periodic 6^3 board at `[128, 129]` and
  at `[1600, 1618]` with the checkerboard seed of
  `massive_corner_stability.py` (a smooth 2^20 cosine plus one unit of
  checkerboard): I at interval 0 computed by the test from the definition;
  over 200 intervals abs(I(t) - I(0)) below 10^-3 I(0) at every interval
  (the design's chain read 2 x 10^-4; the engine's step 2 read 3 x 10^-6),
  the peak amplitude below 2 x 2^20 and the checkerboard component below
  40 units (measured 11 and 18). The edge case as first written (light's pair growing on this
  seed) was WRONG and is corrected before the code: the seed's
  checkerboard carries no velocity (now = -before on it), so at the double
  root light's alternation is stationary, the component one unit at every
  interval; the growing form is the withdrawn self-term form (A), not
  built. The books read `form` under the key.
- (e) A block of side 3 at (2, 2, 2) on an open 8^3 board of the kind
  `[800, 809]` with the well `[800, 800]`: the pair arrays read 809 on
  every Node but the 27 cells, 800 there, num 800 everywhere; the cells'
  list is the cube. The edge case: a cube of side 4 at (6, 6, 6) cut by the
  board is refused by the margin rule (its cells nearer than one extent to
  the open face), not silently truncated.
- (f) A block of content M = 1 with P = Q S M = 64 on x (S = 1): the
  accumulator gains 64 per interval against the wall 192; it steps at the
  intervals 3, 6, 9, ... (the remainder 0 each time); with P = 70 it steps
  at 3, 6, 9 with the remainders 18, 36, 54 and at the interval 11 (the
  fourth Link) with the remainder 2 (770 - 4 x 192 = 2); the cells and the
  pair arrays move with it; a row of the block's own record at a cell
  stays on its Node after the step. The edge case: P = [112, 112, 112]
  (3 P . P = 112896 >= 192^2 = 36864) is refused at load naming the bound;
  P = [64, 64, 64] (3 x 12288 = 36864, not below 36864) refused too; P =
  [64, 64, 0] admitted (24576 < 36864).
- (g) The coupling both ways on a periodic chain of 400 Nodes (the kind
  `[156, 157]`, a block of side 12 with the well `[314, 315]` at x = 200,
  G = `[1, 1]`, g = `[1, 20]` and `[1, 5]`), a planted light packet (the
  design's script's, amplitude 2^16) and the block's response to it over
  400 intervals: the EXACT identity of section 7 (MUSTs A and B at
  4ef195a) on every interval, `J(t) - J(t - 1) = SUM_i (x_next -
  x_before)_i (r - r')_i / (3 num_i g_d) + alpha SUM_i (y_next -
  y_before)_i (r - r')_i / (3 G_d)` with `J = I_m + alpha I_l + (g_n /
  g_d) SUM_cells w_i dx_i dy_i`, `alpha = g W_in / G`, the forms in exact
  rationals, no tolerance; the cross term nonzero on some interval; light's
  own form moved by more than 10 percent between the packet's arrival and
  the end. The edge case: g = `[0, 1]` leaves the response's rows 0 and
  light's form its own identity `I_l(t) - I_l(t - 1) = SUM (y_next -
  y_before) (r - r') / 3`. (As first written the test asserted the
  continuum's sum within 3 percent; the design's J replaced it, section 10
  (j).)
- (h) A seeded block (seed 2^20, the kind `[156, 157]`, the well `[314,
  315]`, G `[1, 1]`, g `[1, 500]`) that `emits` light holding 3 units of the
  light family (quantum 1): three births, one at each of the first three
  cycles of its count (the clicks at 45, 107, 167, 227, 287 on the chain,
  measured), each paying 1, the books balanced at every tick; the fourth
  and fifth cycles birth nothing (the held 0). The coupling as first
  written, g `[1, 5]` (G g = 0.2), breaks the mode's cycles within one
  period on the chain (the emitted light's back-drive; the relay script's
  e-fold of 0.8 to 3 periods), a FINDING named, so the test's coupling is
  the weak one. The edge case: a block
  with `emits` and no held content of that family is refused at load.
- (i) The click at W: the chain of (g) with W = 64 on the block and the
  lamp at x = 40, the train's front reaching the block's near face at x =
  200 after about (200 - 40) / c = 277 intervals: the block's first rung
  on that record is crossed between 10 and 60 intervals after the front
  (the relay script's 20 to 46 at g = 0.02 to 0.2 on the design's chain),
  the rung `pointer x 64 >= norm` read as the comparison, the crossing
  stamped with the block's count; the record's gather line, when the block
  is the chosen cell, carries `clock` equal to that count. The edge case as
  first written (W = 1 stamping the first motion) read the wheel backwards:
  W = 1 is the whole norm; the edge case built: W = 4096 crosses no later
  than W = 64 and after the first motion.
- (j) A seeded block at rest (the kind `[800, 809]`, the well `[800,
  800]`, s = 10, the smallest binding side of `massive_cube_threshold.out`
  at mu = 0.15, on a periodic 32^3 board, no light): its count over 500
  intervals equals the number of upward zero crossings of its summed
  record read from the `block` lines, one `click` line per count, and the
  mean period lies between 30 and 80 intervals (the gap's period 42.1;
  the board's wrap at 32 admitted, the test a consistency of the count
  and not a pin of the mode). The edge case: seed 0 counts nothing.
- (k) The take: the chain of (g) with the block declared `absorbing`:
  light's row at every cell is 0 after every step, its Ports book an offer
  into the block's cell and nothing reaches the far face; a click at the
  block carries `clock` the block's count (on a chain the ladder may give
  the click to the lamp's own cell, the afterglow of one dimension the
  first build named, so the test reads the pointers); the same chain with
  `absorbing` false: light's row at the cells is nonzero after the front
  and the record's pointer at the far face is nonzero (light passed). The
  edge case: an absorbing block with `emits` is refused at load (its light
  rows are taken; it cannot source).
- (l) The motion's pair: a block with P = 64 on x and M = 1 (K = 3) has
  the effective pair `[36864, 36864 - 3 x 4096] = [36864, 24576] = [3,
  2]` (`[K^2, K^2 - 3] = [9, 6]` reduced); at rest `[1, 1]`; with P = [64,
  64, 0] the pair `[36864, 36864 - 24576] = [3, 1]`. The edge case: K = 1
  (P = 192) is refused by the pace bound before the pair is formed.
- (m) The kind's faces: a massive record on a 5 x 1 x 1 board whose world
  `boundary` is open on x and whose family declares no `faces` wraps on x
  (the neighbour of Node 0 on the -x side is Node 4); with `faces` `{"x":
  "open"}` the neighbour reads 0 (the zero face) and nothing is booked
  (the faces' pointers of the light record unchanged). The edge case:
  `faces` on the light family refused.
- (n) The margin rule: (1) the s = 28 block of (i-b) on the periodic 48^3
  board is refused as a pin world naming x, the extent (about 7.9 Links)
  and the side needed (about 60 > 48), and admitted as a control (44 < 48);
  (2) a block of s = 20 (`[800, 809]`, the well `[800, 800]`) whose cells
  lie 3 Links from an open massive face is refused as a control (3 < 5.7)
  naming the axis and the distance; (3) the kind `[800, 809]` with the
  well `[800, 808]` at s = 3 (g = 2 (800 / 808 - 800 / 809) = 0.0031 far
  below g_c(3) = 0.2245 of `massive_cube_threshold.out`) is refused as
  unbound (omega_b at the gap); (4) the extent printed for (i-a) on 48^3
  agrees with the float scratch's 5.73 to 0.05 Links.
- (o) The cavity on a 5-cube of the kind `[800, 809]` on a periodic 24^3
  board: the exact separable form `cos omega = (800 / 809) cos(pi / 6)`,
  omega = 0.5423, the period 11.59 intervals: the block's count over 1159
  intervals between 99 and 101 (one interval's grain); the rows outside
  the cube 0 at every interval.
- (p) The byte identity without the key: the digests of section 1 on the
  first build's chain world over 600 intervals, exact.
- (q) The loader's refusals, one per key of section 3, each naming the
  key (`pair` without the key; den <= num on a massive kind; `faces` on
  light; `side` with `span`; a lamp on a block; a block key on a
  measured event without `side`; `coupling` on a wall; `emits` unheld;
  `absorbing` with `emits`; a momentum past the bound).
- (r) The record's keys under `massive_record` (`hypotheses` carrying
  `massive-record-v1`, the families' `pair` and `faces`, the blocks'
  keys, the books' `form`) and none without it.
- (s) The block key `start` (step 5): a block of side 3 with the momentum
  64 on x and `start` 30 has not moved by interval 30, has stepped once by
  33 and ten times by 60; with `ramp` 30 as well no step before 30 and the
  momentum reached at 60. The edge case: `start` below 0 refused.
- (t) The `mode` line under `mode_axis` "x" (step 5): its three sums equal
  the sums of light's total field over the residue classes of x modulo 3
  formed from the rows. The edge cases: an axis not x, y or z refused; the
  key refused without `massive_record`.
- (u) MUST 2 (Reviewer 3, the Boss's 16:42Z): a planted massive record
  with zero motion after its train plus two intervals does not complete
  (`_complete` False for a massive kind); a light record with the same
  rows does.
- (v) MUST 3: the load bound of a pair, num x 6 x A + 3 x den x (A + 1)
  below 2^63 at the amplitude bound A = 2^40 (section 3): `[2^20, 2^20 +
  1]` refused naming the bound and the pair, `[800, 809]` admitted; a
  block's pair with its g_d folded into the wall checked with that scale
  (`[800, 800]` at g = `[1, 2^20]` refused, at `[1, 20]` admitted).
- (w) MUST 1's test: on the chain 6 x 1 x 1 at `[2, 3]` (y and z folded,
  each read twice as the Node itself) the form I as the books read it
  changes by the remainders' term EXACTLY on every one of 60 intervals
  from random rows, num (I(t) - I(t - 1)) = L SUM (a_next - a_before)(r -
  r'), on an open and on a periodic x.
- (x) Reviewer 3's layer line (18:12Z): on a periodic 256 x 256 x 1 layer
  the margin module's operator keeps the folded axis's two self-reads, so
  the item 7 row mu = 0.15, s = 14, g = mu^2 / 4 (the kind `[3200,
  3236]`, the well `[3200, 3227]`) reads omega_b 0.14846 within 0.0002 and
  the extent 36.2 within 1 Link (`massive_layer_pins.out`), the rule
  comparing x and y alone.
- (g), continued: the identity asserted at G = `[2, 3]` as well as
  `[1, 1]` (alpha carrying G_d / G_n, light's wall 3 G_d: the scale 3 L
  g_d G_n, Reviewer 3's token).
- (y) The seed as the bound mode's integer profile (MASSIVE_RECORD.md
  section 11 item 7, the reader of record and the seed): on the 128^2
  layer of the exploratory world the flat-seeded block's clicks beat
  (39.3 against the period 42.32) and the mode-seeded block's (the margin
  module's mode as integers at 2^20 over the whole layer, the same at
  both levels) read the period within 0.5 percent over [200, 1500]; the
  load-time check of the file's integers against the module's mode reads
  0 units. The edge cases: a profile without `margin`, of the wrong
  length, or all zero, each refused naming the key.

## 7. The HOST estimate (this machine, numpy int64; the engine's cost, measured at step 5)

- The rule: a float scratch of this plan read 1.6 ms per interval per
  record on a 48^3 periodic box (110,592 Nodes); the integer form with the
  remainder about twice that, 3 to 4 ms; the block's own record with the
  pair arrays 10 ms.
- HOST, measured at step 5 (the five cuts' first act, the Boss's 17:10Z): the
  engine's own cost is 13.6 ms per interval on a periodic 200^2 layer
  (40,000 Nodes; a block s = 14 at g = mu^2 / 4, 60 intervals, run.json's
  elapsed seconds; `artifacts/EXPLORATORY_layer_cost_200`), 17 times the
  design's numpy script's 0.80 ms on the same layer, beside this plan's
  scratch of 1.6 ms per record on 48^3: the books' exact Python-integer
  sums per interval are the cost. A moving layer pin world of 9500
  intervals is about 2 minutes; the 64^3 moving worlds of (ii) took 47
  and 49 minutes each (0.24 s per interval); no vectorisation (the Boss's
  word of 19:50Z: the cost is acceptable).
- (i-a), (i-b): 3000 intervals, under a minute each; the Lanczos of the
  margin module 75 to 85 iterations on 48^3 (the scratch), seconds.
- (ii-a), (ii-b): 64^3 (262,144 Nodes), 9500 intervals at about 10 ms: 2
  minutes each, the design's 2 minutes (`massive_board_margin.out`, HOST).
- (iii): as (i) and (ii).
- (iv), (v), (v-m): chains of 1400 to 2200 Nodes, a few light records
  live with their responses, 700 to 4400 intervals: seconds to a minute.
- (i-c), (ii-c): 191^3 to 288^3 (7 to 24 million Nodes), 0.3 to 0.9 s per
  interval for the massive arrays alone (the design's 0.3 s at 200^3),
  0.5 to 0.6 GB of int64 arrays per record; a rest reading of the
  frequency to 0.36 percent (omega_b against omega_0 at eps 0.007) needs
  about 300 cycles, 12,000 intervals at N_0 = 42: one to three hours per
  rest world, the moving worlds 9500 intervals, one to two hours each,
  and the Lanczos minutes (the gap ratio 2.5 x 10^-5 needs several hundred
  iterations on three vectors); to be decided with the Boss after (i-a)
  and (i-b) read.
- The memory of a light record: three int64 arrays over the board and one
  response record per block it reaches (three more), the first build's
  cost doubled at a block.

## 8. What is not built, and said so

- The amplitude coupling `[[0, g], [g, 0]]`: withdrawn (the tachyon).
- A damping on the mode (the sink's form (b)): not built; the take (a)
  alone, on an absorbing block.
- The pace coupling kappa: withdrawn (MUST 4).
- A boost among the 48, a root at run time, a declared contraction: none.
- Fizeau's drag: not computed by the design; no world.
- The two NATURE rows of section 9: the physicist's and Reviewer 3's,
  verified before the build; no world of this plan reads them.

## 9. The order of the work, one pushed commit per step, on the Boss's word

1. This plan and the index row (STEP 1; pushed).
2. The rule with a pair per kind, the pair arrays, the form I, the tests
   (a) to (d), (p), (q) in part, (r) (STEP 2).
3. The block: the cells, the well, the drive and the step, the coupling
   both ways with the response records, the source term and the emission,
   the click at W and the self-click, the take for an absorbing block, the
   index in motion; the tests (e) to (l) (STEP 3).
4. The faces of the kind, the cavity, the margin module and its call in
   the runner; the tests (m) to (o) (STEP 4).
5. The series `examples/events/massive_record/`, its pins before each run,
   the runs in the order (i), (ii), (iii), (iv), (v), the readings by kind
   in BUILD_READINGS.md, a report after each world (STEP 5).

## 10. The two readings of a sentence, where the plan had to choose; for the Boss and the chief physicist

- (a) SETTLED by the design's head (4f74bf2a section 5, Reviewer 3's MUST
  of record 1431; the Boss's word of 15:30Z): the step translates the cells
  and the pair region only; the massive rows stay on their Nodes and
  re-form by the rule. BUILT so. The coupling's difference in motion,
  SETTLED by the design's word of records 1444 and 1445 (696bab86 section
  7; the Boss's 16:13Z): the SAME-NODE first differences on every interval,
  a hop interval included, light's row stepped after the massive step; an
  along-path difference (either adjoint pair) is pumped parametrically by
  the hop's pair resonance with light's band (exact at K = 3) and is NOT
  built; the same-Node form is the one coupling (`_difference`). The
  moving-index world's pins are the same-Node numbers (section 5, (v-m)).
- (b) The margin table's numbers were computed on 96^3 and 128^3 boxes;
  the first check worlds are 48^3 by the design's own line. The periodic
  image shifts omega_b by 0.2 percent (s = 20) and 1 percent (s = 28).
  BUILT: the pin is the algebra's number on the world's own board (the
  same operator, the same method); the design's box number beside it,
  the difference named as the image's.
- (c) Whose cycles are the block's clock: its own record's, or its total
  record's (own plus the responses light drives). BUILT: the total across
  R, the block's record as the algebra sees it; a block with seed 0 driven
  by light counts the driven cycles.
- (d) The units of the block's pointer: the first build books a Port's
  motion squared raw and its norm the lamp's squared steps, and Reviewer
  3's Port factor `[97, 28]` (DESIGN.md 2.1) is not applied there; the
  relay script books 3 x the motion squared against light's E with the
  strain. BUILT: the response's motion squared raw against the light
  record's norm as built, the same declared scale as the first build; the
  factor is a design question for both pointers together, not one.
- (e) A ramp of the momentum is not a rule; it is the pushing agent's
  declaration the design's own chain used. BUILT as the block key `ramp`,
  0 by default, named a declaration of the world.
- (f) The first build requires the pair form of the clock on every paid
  family; the massive kind's clock is its gap. BUILT: the requirement
  reads "every paid family without a massive pair".
- (g) The merges of `origin/detector-law-design` (75ccec3e, then
  7a82c155; docs only) into this branch so that this plan sits beside the
  design it cites and its links resolve; the first merge commit carries
  git's default message.
- (h) ANSWERED by the physicist through the Boss (15:57Z; 5735ace and
  39603502): under the engine's seed (a flat A_0 on the emitter's cells at
  both levels) the relay script reads N_0 = 235 at G g = 0.2 and 310 at
  0.05 (the receiver's rung crossed 11 and 13 intervals after the front),
  247 with an (M) mirror partner; world (iv)'s pin is the script's number
  under the seed the world declares, never 258. The engine's local
  DETECTOR reading (A's click on B's emitted record) stays a different
  quantity, stated beside it.
- (i) A block of the light family with a pair (the (M) wall) shares the
  block's component with no clock and no coupling; its keys are refused
  so that a wall declares nothing a wall has not.
- (j) FINDING of step 3, ANSWERED by the design (4ef195a section 7,
  `massive_conserved_form.py`; Reviewer 3's MUSTs A and B through the Boss,
  17:00Z): the coupled energy E_light + (G / g) I_m is the continuum's
  invariant; the discrete same-Node scheme is symplectic and its EXACT
  quadratic invariant is J = I_m + alpha I_l + g SUM_cells W_i dx_i dy_i,
  the continuum's sum plus the cross term of the two first differences on
  the cells (the 1.3 to 1.6 percent the float scratch read). BUILT to the
  two sentences: (A) the coupling folded into the rule's one division (the
  massive wall `3 den g_d`, light's `3 L`; `_coupled_term` adds the
  undivided term, `_advance` divides once, the row's `scale` the folded
  denominator), so the remainders' term per row is the whole correction;
  (B) the columns as section 7 states them (the massive step first reading
  light's `a_now - a_before`, light's step reading the massive `a_next -
  a_now` just written). Test (g) asserts the identity exactly. One default
  of the build, named: light's wall is `3 L` for EVERY light row while a
  block is on the board (L the least common multiple of the blocks' G_d,
  one number for the kind; the rows' values unchanged, the remainders
  scaled by L), and a massive row's `3 den g_d pair_d` with the drive's
  pair; when a ramp changes the pair the remainder is rescaled to the new
  wall (`r x new // old`, verbs G and D), the identity exact on every
  interval of a constant wall.
- (k) FINDING of step 2, corrected in step 3: the form I written at step 2
  skipped an axis of extent 1 in its Link sum; on a one-layer board the
  rule reads the row itself as its two neighbours on that axis (DESIGN.md
  section 2, `a_U = a_D = a_now`), which are two self-Links the form must
  carry (the diagonal 4 / 3 of the chain's operator). Step 2's tests ran
  on 6^3 boards, where nothing was skipped; step 3's chain tests found it.
  Corrected: an axis of extent 1 counts its two self-Links.
- (l) The test (g) of section 6 as first written named the light clock
  `[1, 5]` (0.2 phase steps per interval, a period of 320 intervals, too
  long for the chain); the test uses the chain test's clock `[77, 25]`
  (the period 20.8 intervals, lambda 12 Links) and reads light's energy
  before the train reaches the block and at the end.
- (m) FINDING of step 5: world (v)'s block is the design script's confined
  oscillator (`massive_dielectric_index.py` holds the massive row at 0
  outside the block's cells, at the kind's omega_0 on them), so the
  engine's world declares it as a CAVITY with the kind's own pair `[7, 8]`
  and not as a well; the closed form's omega_0 is then the kind's gap
  0.50536, as section 5 states.
- (n) The margin rule on a folded axis (step 5): a periodic axis whose
  extent is below the block's side (the y and z of a chain, the z of a
  layer; MASSIVE_RECORD.md section 11 item 7: the rule reads the Node
  itself across it) has no face and no tail for the rule to compare, and
  the module skips it; before this the chain worlds were refused on y.
- (o) The moving index's pin from behind (step 5): the design's 4.3 and
  6.8 (the Boss's 16:13Z) are the SAME-NODE script's numbers for its
  receding case on the LONGER chain (n = 4000, the source at 300, the
  probe at 2500, the block from 1500, the window [5000, 6000]); on the
  chain of 2200 with the window [3400, 4300] the same script reads 1.582
  and 2.569 with the window's two halves unequal (+0.227 and +0.973 rad).
  Both chains are built and both numbers are the pins of their worlds.
  Light's faces on the chains are open on x as declared (a zero face, a
  mirror): the reflection from x = 0 reaches the probe inside the windows
  (at about 3118 on the chain of 2200, 4850 on the chain of 4000), named
  with the readings; a trial with light's faces periodic on x (the
  script's np.roll) moved the rest readings away from the script's own
  numbers by the wrapped wave and was not kept (BUILD_READINGS.md).
- (p) The pump's two readings in worlds (ii) and (iii-b) (the Boss's
  16:13Z) read 0 identically: those worlds declare no light and no
  coupling (the pump acts on light through the coupling on a hop); the
  readings are made and recorded as ordered, and are meaningful in (v-m),
  where light's energy drift per interval and the mode's content over the
  window are reported.
- (q) The block key `start` (the interval the drive begins, the ramp
  counted from it) and the world key `mode_axis` with the `mode` line are
  the two additions of step 5, each a declaration; tests (s) and (t).

## 11. The quantum rows' three components (build 2, the Boss's order of 2026-09-23 22:25Z; `detector-law-build-2`; `tests/test_detector_law_tables.py`)

The three components the six quantum rows lack in the engine (the
declarations page `declarations/DECLARATIONS.md`, "what the engine
lacks"; PLAN.md 3.1 item 7), each a generic component under the local
integer operation contract (ARCHITECTURE.md): world-defined, no branch on
a physical name, integer intermediates, fixed local work for fixed N,
with one test (the inputs, the expected integers, an edge case).

| Component | The declaration it is built against | Where | The verbs and the integers | The test |
| --- | --- | --- | --- | --- |
| 1. The phase reading of a record at a table Node | DECLARATIONS.md's head: the angle phi on Z_N nearest to the pair (a_before, a_now) = A (cos(phi - k), cos phi) at the record's clock [n, d] (k the clock's whole step of the interval, floor(n / d) or one more), read by the phase table at load (cos x 256, `core.phase.phase_cosines`), the nearest entry by an integer comparison, no root and no float at run time; the amplitude A the third input the declaration names (the lamp's UNIT on a bar; a table's peak register where the wave spreads) | `core.phase.nearest_phase(before, now, amplitude, clock, N)` -> (phi, residual) or None for the zero pair; `DetectorLawSimulation.read_phase(record, node, amplitude)` | the residual abs(256 now - A C[phi]) + abs(256 before - A C[phi - k]) minimised over 2 N entries (verbs B and the comparison of D), the residual the reading's grain (0 for a pair the clock drove) | (a): N = 64 with [77, 25] and [1, 1] exact at every age at two amplitudes; N = 128 exact 16 units from the extrema; N = 2048 with [3, 1] within one step 32 units from them; the chain world's reading advancing by the clock's step; the zero pair None; a zero circle, clock or amplitude refused |
| 2. The pair's two arms | DECLARATIONS.md rows 1a and 1d, DESIGN.md 6.3: a pair record is two records with one birth stamp and opposite trains, each arm's row on its own line with nothing of one arm written on the other (B1); the rule's part only that both trains reach their bars; the joint labels psi = (00) + (11) carried unchanged (the rotation at the bars and the one gather are the table rows', later) | `_births`: the lamp's `arms` and `branches` (the amplitude series' keys, admitted under the key) birth one record per arm on one stamp (the same ordinal, u and interval; the arm's identity the birth's plus arm x 2^24), each arm's row confined to the half-space of its first direction from the lamp's Node (`_half_space`, verb D's comparison at every interval in `_advance`), the labels on every arm; the pair's one quantum on arm 0, the other arms 0 (a default, named: the joint click books it once); the birth line's `arms`, `labels` and `arm_records` | (b): on the bar of 21 two records per birth on one stamp, the +x arm 0 for x < 10 and the -x arm 0 for x > 10 at every interval, the two rows mirror images, both trains at the bars x = 7 and 17 within 12 intervals, the books balanced; a lamp of one arm as it was (byte for byte, test (p)); arms 2 on three directions refused |
| 3. The splitter's table | DECLARATIONS.md row 2b, DESIGN.md's fourth receiver form ("a partial re-emission with a phase"), ALGEBRA.md 4.6 (the split (w, m, p) -> ((w a_i, m A, p + t_i)) an isometry); SINCE SECTION 14 (the physicist's line on Reviewer 3's read, 2026-09-24): the table acts on the record's PAIR by the linear form, the re-emission additive, the remainder carried, one table Node per Node of the line | `Splitter` in the engine from a measured event's `table` `{"rule": "rerelease", "inputs", "weights", "turns"}` with its `directions` the outputs (the amplitude series' keys, admitted under the key when `inputs` is declared; a fan without inputs stays refused): the Node held at 0 and taking the arriving wave, booking no offer (no click at a splitter); per interval, per light record, the LINEAR FORM on the pair (a_before, a_now) at each input Node, A cos(phi + t) = (a_now S[k + t] - a_before S[t]) / S[k] (S the sine table, cos x 256's companion, immutable law data; k the interval's own whole step of the clock by `core.integer.by_clock`, floor(n / d) or one more), and each output's term SUM_i w_ij (a_now,i S[k + t_ij] - a_before,i S[t_ij]) / (S[k] R_i), R_i the root of the row's norm (exact at load: 21^2 + 20^2 = 29^2; a norm that is no square refused naming it), ADDED to what the rule gave the output Node; verbs B (the matrix on the two columns), D (one division per output per interval by the wall S[k] x L, L the least common multiple of the rows' roots, the remainder carried per output as the rule's) and G (the term added); no reading, no register (the first fold's peak register and hard level, Reviewer 3's (a) and (b), are gone); a family whose clock's step has a sine of 0 refused at load | (c): the integers of the linear form on a planted pair at every one of the 64 phases (the outputs from 0 exactly floor(w_j (a_now S[k + t_j] - a_before S[t_j]) / (S[k] 29)) with the remainder kept, each term w_j UNIT cos(phi + t_j) / 29 within UNIT / 64), the isometry (the two outputs' squares over the 64 phases summing to the input's within 2 percent), the additive re-emission (a second call adds the same term), the run of 90 intervals with the books balanced, the splitter's Node 0, no click and no offer there, the wave beyond both outputs nonzero, every remainder inside its wall (GAMEBOARD readings of the rows; the ratios 21 : 20 and 21 / 29 of the first fold no longer read, since the outputs carry the rule's value too); a fan without inputs, a row of norm 2 and the clocks [32, 1] and [1, 2] (a step with sin 0) refused |

FINDING of build 2 (component 1), for the physicist through the Boss: the
reading's grain is the phase table's scale 1 / 256, not 1 / N. Where the
clock's step k moves the cosine by less than one table unit (256 x 2 pi
k / N x abs(sin) below 1: near the zero crossings for N above about
1600 k, and in the flat runs at the extrema on every circle above 64)
consecutive entries repeat and one pair (a_before, a_now) recurs at
several phases of the wave, so the nearest entry is a tie and the
reading is off by the tie's span: at N = 2048 with the clock [1, 1] one
third of the driven pairs read wrong, some by a half turn (the other zero
crossing); with [3, 1] the reading is within one step 32 units from the
extrema and off by up to 253 steps near them; at N = 256 with [1, 1]
16 of 512 pairs read wrong by up to 7 steps at the extrema; at N = 64
every pair reads exactly. The Bell row (1a) declares N = 2048 with the
wheel [1, N]: its clock's pair must give the reading a step of at least
3 per interval, or the row's table needs a finer scale than the law's
immutable 1 / 256 (a declaration outside this build), or the rotation
reads the phase only where the levels are away from the extrema; the
physicist's line, not the builder's.

### 11.1 The matter lamp (the Boss's 23:32Z: the lamp verb on a massive kind)

The check: does the lamp verb accept a family whose pair is not light's
[1, 1], with no branch on a physical name? The verb itself did (`_births`
and `_drive` read the family's clock `phase_per_age` and the lamp's
Nodes, nothing of the pair), and the rule already ran with the family's
pair; but the kind (den > num, `massive_kind`) was light-only by four
lines, each a branch on the kind, not on a name: the loader refused any
`phase_per_link` on a massive kind ("its clock is its gap") and a lamp on
it ("born of no lamp"); the engine's interval skipped every massive record
in the records' loop (a block's records are advanced with their block)
and returned from the rule before the drive on a record the take does not
read; `read_phase` read no massive record. The one generic line, BUILT:

- The loader admits the pair form of `phase_per_link` on a massive kind
  (the family's clock; the integer form, a turn per Link, stays refused:
  a massive kind's phase per Link is its band's at its clock) and a lamp
  on a massive kind that declares its clock (a lamp on one without it is
  refused naming the pair form).
- The engine advances a lamp's record of a massive kind (the record has
  `driven`, a block's has not) by the rule with the family's pair alone,
  its faces the kind's (a zero face a mirror), coupled to no block (the
  coupling is declared on light's row, MASSIVE_RECORD.md section 7; a
  default, named); the drive at the lamp's Nodes for the train is the
  same verb as light's (a block's record has no train and is not driven);
  `read_phase` reads it at the family's clock. SINCE Reviewer 3's line on
  f5aba037 (the Boss's 01:10Z): the lamp's record goes through the SAME
  TAKE AND POINTER PATH as light's (the receivers' Ports, the faces'
  sponge, the detector sets' pointers, the click at W once per record at
  its completion, POSTULATES 10: the click is the law's one action on any
  record); a block's massive record keeps MUST 2 (taken by nothing, never
  completing). The first fold had the lamp's record taken by nothing and
  never completing, MUST 2 read on the wrong record; test (aa) reads the
  click: on the chain of 200 without light's lamp, two births of the
  matter lamp (u = 0 and 1 on the wheel [1, 64]), a receiver body of the
  matter family at x = 184 read as `screen`: each record clicks once, its
  stamp the first interval its pointer at the chosen cell reached 1 / 64
  of the norm, more than 100 intervals after its birth and before its
  completion; the screen's pointer reaches nine tenths of each norm; the
  second record (u = 1) chosen at the screen (the ladder's u = 0 falls on
  the first cell with a rung, the lamp's own body, which takes the train's
  reflections off the screen's Ports after its grace: the take's pair
  [-15, 56] is light's impedance, so a matter train is partly reflected
  by a receiver, a reading for the physicist); the books balanced.
- Light's [1, 1] unchanged: a block's records take the same path as
  before (no `driven`), and the light record's rows are identical beside
  a matter lamp (test (z)); the first build's digests stand (test (p)).
- Test (z), `tests/test_massive_record.py`: the kind [156, 157] at the
  clock [77, 25] on N = 64 (omega = 0.302 above the gap omega_0 = 0.113),
  one lamp on a chain of 200; the band on a chain from the rule's plane
  wave, cos k = 3 den cos omega / num - 2, k = 4.99 steps of 64; the
  record's phase at the interval 100 read at each Node's peak register
  over 4 Links on both sides of the lamp: 22 steps on each side beside
  4 k = 19.97 (21 before the record went through the take; the reading's
  grain of section 11's FINDING and the train's dispersive front; the
  test's bound 3 steps); the books
  balanced at every interval; light's rows identical with and without
  the matter lamp; the lamp without the clock refused.
- Not in this line: the probes and the `mode` line sum light's rows
  only, as before (a matter lamp's train is not probed); a splitter's
  table reads light's records only. Both are the physicist's to ask
  for, not the builder's to widen.

## 12. The launch list's worlds and readers (the Boss's order of 2026-09-23 23:40Z; RUN_LIST.md on `detector-law-design` at c0e88709, DECLARATIONS.md sections 7 to 12; `detector-law-build-2`)

Every world generated from its declaration, no number of the builder's
own; where a declaration lacks a line, the line is named here and the
world is not written (the Boss's rule). No pin world was run.

- (a) The two layer pin files of row 4a regenerated by `make_worlds.py`
  with the two declared keys of DECLARATIONS.md section 8: `ramp` 10000
  and `ticks` 18500 on `layer_pin_k3_14.json`, `ticks` 18500 on
  `layer_pin_rest_14.json` (the same hold [10200, 18200] read at rest, as
  the RUN_LIST reads the k = 3 clicks "over the rest world's"); the seed
  profile and every other key byte for byte as before; `read_runs.py`
  reads the pair over that hold; `pins.py`'s `reads` lines name it.
- (b) The two readers of clicks: written here (4520641b) and DROPPED at
  the merge of main 0a5ea8be (the Boss's 01:20Z: Builder 2's readers of
  the same names, `clicks_of`, `screen_clicks`, `light_clicks` in
  `read_runs.py`, reviewed and merged by PRs #1073 and #1076, stand; no
  second reader of the same thing; this branch's tracked copy
  `EXPLORATORY_chain_screen/` and `tests/test_read_runs_clicks.py` went
  with them). The same merge keeps main's `layer_pin_rest_14.json` at
  3500 intervals (this branch's 9302f513 had set 18500; the physicist
  says which is declared). A reading made on the engine's counting form: a
  record clicks ONCE, at its completion, stamped with the first rung of
  its chosen cell; a detector's "train of clicks" is one click per
  record, and a screen's counts per Node need as many births as clicks.
- (c) The world files marked "to write: the builder":
  - WRITTEN: `deep_well_rest_40.json` and `deep_well_k3_40.json` (the
    cavity row's control on a 128^2 layer, s = 40 at full depth, the
    flat seed, the ramp 1500 and the hold 8000; the block centred and the
    rest world's 3500 intervals the series' own conventions, named); the
    one formula at the exact cone on the layer's own mode 0.75306
    (`expectations.json`) beside the RUN_LIST's 0.7531.
  - REGENERATED: the long chains of (v-m) on section 11's geometry (the
    source at 800, the probe at 2400, the block from x = 1500 stepping
    away from interval 3000, the window [3800, 5400]; the train of 200
    periods, the rest block at x = 2100 and the 6000 intervals as before);
    the pin entries carry section 11's numbers (+1.0144 rad, the halves
    +0.5539 and +1.5234, the drift 1.2 x 10^-3 per interval, the bands).
  - REFUSED AT LOAD, not committed (a world that does not load fails the
    gate): 4b's `redshift_k3.json` and `redshift_control.json` (section
    4, the second draft) and the light clock's world (section 10, as an
    exploratory world read by probes): their declared coupling
    g = [1, 50000] fails Reviewer 3's MUST 3, the load bound of the pair
    with its g_d at the amplitude bound A = 2^40 (num x 6 x A x g_d +
    3 x den x g_d x (A + 1) below 2^63): on [314, 315] it admits g_d up
    to about 4450, on [800, 800] about 1750; the refusal reads
    "measured[0].pair [314, 315] with the coupling's denominator 50000:
    the rule's total ... at the amplitude bound A = 2^40 is
    155525919748962450000, not below 2^63". The generator carries both
    worlds behind `launch_list_worlds(include_refused=True)` exactly as
    declared (the emitter's stock of light one unit per interval of the
    run, an inert bound on the births; B a receiver body at x = 1900
    with a probe at the free Node it faces); the conflict of the
    declaration with the bound is the physicist's and Reviewer 3's to
    settle (a smaller g_d, or the bound declared per world at the seed's
    own amplitude). Two more lines of the light clock, for the physicist:
    on a chain a receiver body at A's face cell x = 612 TAKES the whole
    line (the Port's take, one way, no reflection), so nothing returns
    from the mirror at 672 through it; and a lamp-less world has no key
    for the detector's rung W (the wheel is the lamps'), so W = 10000 and
    a second detector at W = 64 cannot be declared; the return is readable
    by a probe's amplitude at 612 (GAMEBOARD), which is how e2 would be
    read once the world loads.
  - NOT WRITTEN, the missing line named: R2's `sagnac_k3.json` (the
    positions of A and B and their separation, the chain's faces, and
    the emission's direction are not declared; a block emits from its
    cells in every direction; PINS_R2.md is the previous engine's
    arrangement); M1 and M2's `matter_waves_{12,16}.json` (section 12:
    the lamp's stock and rate, the number of births, are not declared,
    and the engine holds no zero line for the matter kind and takes no
    matter record at a screen, MUST 2's "taken by nothing" being the
    block's record's line and the matter lamp's record's alike in
    section 11.1: two engine lines the physicist must ask for); the ray
    law's `two_slits.json`, `three_openings_*.json`, `pace_fan_*.json`,
    `one_opening_far.json` (the lamp's stock and rate, the openings'
    widths and separation and the screen's distance at 128^2 are not in
    RUN_LIST.md or DESIGN.md 6.2 as integers of the world; the mirror
    line is not an engine form, the engine's wall is a receiver body that
    takes; the clock pair at 24 Links is not declared); the tables'
    `bell_*.json` (section 1: the clock pair on N = 2048 is not declared,
    and 300 intervals cannot hold a train of 128 periods of any pair on
    that circle), `malus_*.json` (sections 5 and 6: the clock pair on
    N = 256 and the train are not declared) and `mach_zehnder.json`
    (section 3: L = 10 lambda = 120 Links on a 33 x 33 layer, the
    corridors' walls and the mirror form, which the engine lacks). The
    polariser's rotation on the read phase (the table's action of the
    declaration's head) is not among build 2's three components; named
    for the Boss as the fourth line the tables' rows need.
- e2 (the light clock) could not run: its world is refused (above). e3
  (the receding index on the regenerated long chain) runs once as
  EXPLORATORY after this section's commits land, its readings in
  BUILD_READINGS.md beside section 11's numbers.

## 13. The fold of DECLARATIONS.md section 14 and the night's lines (the Boss's 00:20Z, 00:40Z, 00:50Z, 01:00Z, 01:10Z, 01:20Z; main 0a5ea8be merged by one merge commit)

- The splitter under section 14: section 11's row 3 as it now reads
  (the linear form on the pair, additive, the remainder carried, no
  register; test (c) rewritten). The three tokens of 00:20Z: (1) arms
  whose first direction has a component on a periodic axis are refused
  at load naming the axis (no half-space there; test (b)); (2) the
  output division's remainder is carried per output (the rounded
  division not taken: the remainder is the rule's own form); (3) row 3's
  test column names its ratios GAMEBOARD (and no longer reads them).
- The world key `wheel` (an integer from 1, 1 by default, admitted under
  `detector_law` alone): the detector sets' rung W where no lamp declares
  a larger birth wheel, for the worlds whose records a block emits (4b's
  B, the light clock's face detector, R2's) and have no lamp: the
  engine's wheel is the largest of the lamps' and the key's (test (ab)).
  One W per world: two detectors at different rungs in one world (the
  light clock's W = 10000 beside W = 64) are not declarable.
- The matter lamp's record through the take (section 11.1, test (aa)).
- The World Generator's list (the Boss's 01:00Z), the engine's side:
  (1) THE g BOUND: MUST 3 guards the rule's int64 total on the rows
  (numpy int64, not Python ints): num x g_d x S_6 + 3 den g_d a_before +
  the coupling's term + r must fit 2^63 at the largest amplitude any
  row may reach, taken as A = 2^40 (`AMPLITUDE_BOUND`, a constant). The
  arithmetic: with g = [1, 50000] the bound needs A below about 2^37 on
  [314, 315] and 2^36 on [800, 800]; the seed is 2^20 and a pumped row
  grows by the coupling's gain (1.04 per window on the receding index).
  A per-world amplitude bound (a declared key, checked at load in MUST
  3's line and asserted on the rows at run time, the run refused when a
  row exceeds it) admits the declared g at A = 2^32 with a margin of
  2^12 over the seed; the number is the physicist's, the key an hour's
  build with its test. NOT built tonight without his word.
  (2) A detector's own rung W as a world key: BUILT (`wheel`, above).
  (3) A detector set that steps with its block: NOT FOR THE GO (the
  cells and the take masks are re-formed at a step for the block's
  cells only; a body that steps is a new form).
  (4) A lamp on the massive kind: EXISTS (section 11.1; the lamp's
  `wheel` key as light's; the kind's omega is the pair form of
  `phase_per_link` on the family, a clock, not a turn).
  (5) A zero line for the matter kind: with the take path a receiver
  body's Nodes hold the matter row at 0 and TAKE it one way (a sponge
  line; the reflection off it is the take's imperfect impedance, not a
  mirror's); the mirror form as a key: NOT FOR THE GO (the kind's open
  faces are the only mirrors). The (M) wall as a block of light's kind
  with the pair [21, 22] (BUILD.md (iv-b)): the loader admits it (no
  `seed`, no `margin`, no coupling on a light-kind block) but the engine
  has no path for it and stops at the first interval ("list index out of
  range" in the blocks' loop): NOT FOR THE GO; the take world (iv-b) was
  never run.
  (6) The splitter's fan: the fold above; a fan without inputs stays
  refused (a splitter declares its inputs).
  (7) The tables' clock pairs [2464, 25] on N = 2048 and [308, 25] on
  N = 256: the splitter's division uses the world's own step k by
  `by_clock` at every interval (the record's clock, not a ratio); a step
  with S[k] = 0 is refused at load. The polariser's rotation on the pair
  (the same linear form with U_s) is NOT built: the tables of Bell and
  Malus are unchanged from the amplitude law in form (DESIGN.md's
  sentence); the fourth line the tables' rows need.
  (8) The emitter's held light: WITHDRAWN by the declarations' sixth
  commit (section 14 below): the emission consumes no stock.
  (9) The screen as one detector set per Node: LOADS (121 one-Node sets
  with their 121 bodies on a 128^2 layer), and main's `screen_clicks`
  places them by the sets' Nodes; HOST on 128^2 with 19 records in
  flight and the screen's 121 bodies: 21.5 ms per interval.
- LINE B (the grace for a block's emitted records): it does NOT hold. A
  lamp's record has `driven` (the lamp's Nodes) and a grace of its train
  plus two periods, during which its own Nodes take nothing of it and
  the offer at the lamp's own cell is dropped; a block's emitted record
  is born with no train, no period and no `driven` (`_block_births`), so
  its grace is 0 and a receiver at the block's face takes its emission
  from the first interval. One change gives it: in `_advance`, a record
  with an `emitter` takes its `driven` set from the block's cells while
  `sourcing` and for two of the block's periods after the cycle's end
  (the block's period the cycle's length, known at the cycle's end), and
  the dropped offer's cell is the block's cell; then the first rung after
  the grace is the receive, as the cycle sentence reads. About twenty
  lines and one test; not built tonight without the Boss's word.
- LINE C (the cost per record per interval, this host, the head of this
  section): 128^2, light's lamp, no body: 0.9 ms with one record in
  flight, 1.1 ms per record per interval at 20 in flight (21 ms per
  interval); 256^2: 4.1 ms with one, 5.2 ms per record per interval at
  20 (104 ms per interval). Section 12's 19 records in flight on 128^2
  with the screen's 121 bodies: 21.5 ms per interval, a minute per 3000
  intervals; the first-draft 280 records in flight would be 300 ms per
  interval, ten minutes per 2000. Reviewer 3's 1.6 s per interval is
  not this engine's number.

## 14. The GO's keys (the Boss's orders of 01:40Z to 02:15Z on DECLARATIONS.md section 15; `detector-law-build-2`)

Each a generic line under the contract, one test each in
`tests/test_massive_record.py`; no pinned run.

- LINE B, the block's grace (tests (ac), (h)): a block's emitted record has
  the grace a lamp's record has: while the block sources it (its cycle)
  and for the block's `own_grace` after the cycle's end (the declared N_s
  of DECLARATIONS.md section 10 item 1, an integer of intervals REQUIRED
  on every emitting body, refused absent naming it and refused on a body
  that emits nothing; the grace = the train + own_grace; no default),
  its driven set is the block's CURRENT cells (a stepping block's follow
  it), the offer at the block's own cell is dropped and the block's own
  response to it books nothing. A LAMP may declare `own_grace` too (the
  Boss's line (A) of 04:40Z; the matter lamp's whole hold, M1-6): its
  records' grace is then the train + own_grace, and a light lamp without
  the key keeps the module's constant two periods. `held` on an emitter
  is refused (line (E): the declarations' sixth commit withdrew the
  stock; the record is born at content 0).
- LINE 7, A SET BOUND TO A BLOCK IS A RECEIVER (the Boss's 03:56Z, 04:14Z
  and 04:40Z on DECLARATIONS.md section 10 item 9 and section 13; tests
  (ac), (ah)): a detector set declared by `"block": <measured number>`
  with its own `wheel` is a take line, as a receiver body's set is: its
  Nodes are absorbing (the row held at 0 there, the Ports' one-way take
  with light's pair, the record's `absorbed` moved, so the record
  completes as at any receiver), its pointer the Ports' motion squared,
  the first rung at pointer x W at or above the norm on the set's own
  wheel, stamped with the block's own count as the interval begins
  (`rung_counts`) and named on the gather line by `clock_source`
  ("measured:<n>"; "interval" for a receiver as built). Two forms: (a)
  `block` alone, the set's Nodes the block's own cells at every interval
  (R2's form, section 13 item 1: the block is then absorbing, its cells
  taking), and (b) `block` with ONE `positions` entry, a free Node (the
  light clock's x = 612, item 9; a Node of a measured event or of another
  set refused). A set on a BODY (4b's B at [1900, 0, 0]) is `positions`
  on the body's Node with its own `wheel`, and `block` naming a body is
  refused naming that form. The set is FREE for the emitting block's own
  record during that record's grace (the per-record exemption, by
  emitter and age: no take, no zero, the row evolving there; its Ports'
  ghosts follow the free neighbours' levels and book nothing, so the take
  at the grace's end starts at those levels with no jump booked; the set
  Node's own content at the grace's end is booked as section 17 says). A
  stepping block's take masks are re-formed at each step, and (f) THE HOP
  RULE (section 13 item 4, declared at go-lines-2 0bc5cc0f): at a hop the
  face's Port is a NEW Port whose ghost starts at the entered Node's own
  level (no jump booked, no stale ghost carried); the content of the Node
  the set steps into is taken that interval, its motion squared booked to
  the set's pointer and to `absorbed`, the row then held at 0 there.
  READINGS (EXPLORATORY, test (ac), the light clock's chain of section
  10 with the set at the free Node x = 112 beside A's face, W = 64,
  own_grace 70): the record passes the set freely during its grace of
  140 (the train 70 and the 70 after), the mirror's neighbour x = 171 is
  reached before 208, and the FIRST RUNG comes at 141 after the birth,
  AT THE GRACE'S END, not in the ordered band near 218: it is booked from
  the record's own RINGING inside A's twelve cells after the train (the
  lattice's alternating mode at about 5 x 10^5 against the front's 10^7,
  its motion per interval large because it flips sign each interval),
  leaking through the face; the set's pointer reaches 2.1 x 10^12 (half
  the norm 4.3 x 10^12) by 208 before the return arrives, and the return
  is visible after 208 only as the pointer's rise (2.8 x 10^12 from 208 to
  240 against 2.1 x 10^12 from 141 to 208); with the faces open the same
  rung at 141 and no rise (the record ends at the sponge at 220). A
  FINDING FOR THE OWNER: under this form the light clock's set clicks on
  the emitter's ringing, not on the return; the candidates (a longer
  own_grace, the emitter's cells taking their own record's remnant at the
  train's end, a softer turn-off of the drive, a probe of the level) are
  the physicist's, none built. Test (ah) reads form (a) on a chain of
  300: a light lamp's record taken at the block's cells clicks once at
  the set at rest (stamped with the block's count 4 at 324) and with the
  block pushed toward the lamp at k = 3 (the click at 203, the count 2),
  the books balanced at every interval through the hops.
- THE CLOSED FACE (test (ac)): the boundary value `"closed"` per axis,
  under `detector_law` alone: a zero face for light without the open
  face's take (no face cell, no sponge; the level 0 beyond it as
  `_shift` fills), the mirror B of section 10 at x = 672. On the light
  clock's chain the level at x = 160 after the return is 7.0 x 10^6 with
  the face closed against 1.7 x 10^5 with it open (the peak 1.6 x 10^7),
  a GAMEBOARD reading of the first form's run.
- THE CLICK'S KIND (test (ac), every gather line): `click_at` is "rung"
  where the chosen cell crossed its first rung (the `click` field that
  rung's interval) and "completion" where none was crossed (a screen
  row's Node at 1e-4 of the norm: the `click` field is then the
  completion interval, never to be read as a rung; Reviewer 3's line 2).
  Test (p)'s events digest moved once by these two fields (the state and
  audit digests unchanged, the witness that the rows are byte for byte).
- THE AMPLITUDE BOUND (test (v); issue #1085): the world key
  `amplitude_bound`, required on every world that declares a massive
  FAMILY (den > num; the Boss's line 6 of 03:44Z: a light-only world
  under `massive_record` loads without it, and the key is refused on a
  world without the flag; no default; the physicist's A = 2^32 in every
  world of the GO, section 15 M1-10): MUST
  3's load bound at that A, the scalar seed and a profile's largest
  magnitude refused above it naming the bound and the pair, every row
  asserted below it at every interval (the run refused at the interval
  it is crossed, naming the record, the level and the bound). The
  series' generator writes it; the tracked copies carry it.
- THE (M) WALL'S PATH (test (ad); section 15 L-1): a block of light's
  kind is a mirror line: its `seed` is 0 at load (no own record, no
  clock, no coupling; the keys refused as before), its cells carry the
  gap's pair on light's kind ([1, 2] two Nodes deep: the declaration's
  wall transmits 1.9 percent of the amplitude two deep (section 15 M1-6's
  decay 1.97 per Link); the engine reads 1.45 percent of the level beyond
  the wall over 200 intervals, a transient below that figure, the front's
  precursor included; line (F) of the Boss's 04:40Z); the
  margin rule skips light's kind. And M1-6's BARRIER (test (e)): a
  raised pair on a block of the matter kind is admitted (no own record,
  its seed and clock keys refused, the margin rule skipping it); the
  kind's own pair without `cavity` stays refused.
- THE TABLE'S READING (test (af); section 15 T-1, the fourth component's
  first line): `read_pair(record, node, turn)`, the polariser's rotation
  on the record's two columns by the linear form of section 14 item 1,
  the level A cos(phi + t) at the turn t from the pair at the Node (one
  division by S[k], k the interval's own step); a record of declared A
  and phi reads A cos(phi + t) at t in {0, N / 8, N / 4, 3 N / 8} within
  UNIT / 64 at every phi. NOT wired: the click's channels (+ and -, the
  weights of ALGEBRA.md 4.12) are the amplitude law's cells, which the
  detector-law engine's cells (bodies, sets, faces) do not carry; the
  Bell and Malus rows read no channel here until that line is declared
  for this engine (the physicist's, after the GO).
- THE TAKE ON THE MASSIVE KIND (the Boss's item 6b; section 15 M1-6; test
  (ag)): an absorbing block of the matter kind is a take line (the kind's
  own pair admitted on an absorbing block; a well's or a barrier's pair
  as before), its Ports taking a matter lamp's record as light's, the
  record completing with one click; the take's pair is a DECLARATION of
  kind 2 per block, the key `take` [n, d] on an absorbing block (light's
  [-15, 56] where none is declared; k = n / d in (-1, 0]; refused on a
  block that is not absorbing), kept per Node in the take arrays and
  moved with the block. Read on the chain of test (aa) at the interval
  300: the declared [-19, 86] takes 7.08 x 10^12 of the record's offer
  against light's 6.48 x 10^12 and the group-pace pair's [-33, 100]
  5.73 x 10^12, and leaves the smallest level between the lamp and the
  screen (945542 against light's 951825): the phase-pace pair leaves
  least, as the declaration expected; [-5, 27] (lambda_dB = 16's pair)
  takes 7.54 x 10^12 on this world, for the physicist.
- ISSUE #1086 (test (ae)): the books' `momentum` carries `held` as the
  sum of the blocks' declared momentum vectors, `transit` and `escaped`
  null with the note that they are not accounted (the massive kind's
  momentum books are ALGEBRA.md 8.11's, the physicist's), and
  `balanced_scope` names content alone, in the books and in run.json;
  the audit's digest of test (p) moved once by it.
- THE EMISSION WITHOUT A STOCK (M1-2, the sixth commit of the
  declarations, Reviewer 3 confirmed; test (h)): `_block_births` births
  the record at content 0 and consumes nothing; no `held` on an emitter
  (the refusal "holds none of it" is gone; a `held` book stays inert and
  undeclared). The amplitude bound's CEILING (the Boss's 02:33Z): a
  declared `amplitude_bound` above 2^40 is refused at load, MUST 3's
  proof standing at 2^40 (2^32 inside it). The splitter's remainders are
  cleared at the record's completion (Reviewer 3's HOST token). The
  registered worlds of `examples/events/massive_record/` (35 files and
  the two tracked EXPLORATORY copies,
  `EXPLORATORY_layer_rest_14/world.json` and
  `EXPLORATORY_layer_k3_14/world.json`) gained the key `amplitude_bound`
  2^32, which
  the required key demands: named for the owner (Highlights 5.4 item
  10). The matter lamp's clock stays the family's
  `phase_per_link` in the pair form (item 0). The stepping detector as a
  body, the mirror form as a key, the gather line's Nodes: NOT FOR THE
  GO (the Boss's 01:55Z item 7).

## 15. Line 8, the order channel's two keys (DECLARATIONS.md section 2 item 8 as DECLARED on order-channel-attacks, PR 1106; Reviewer 3's line of 04:38Z, no default; the Boss's 04:55Z, 05:30Z and 05:45Z; `detector-law-build-2`)

Two keys on a PAIR lamp's entry (a lamp with `arms` above 1) under
`detector_law`, one test (`tests/test_detector_law.py` (d)); no run of
any world (the owner's rule; no Bell run before the attacks page is on
main under Reviewer 3's read and the seed-set order is built).

- `residue_order`, a string, REQUIRED on a pair lamp with NO DEFAULT
  (absent there the loader refuses it naming the key: an implicit
  default to the open-channel form is against AGENTS.md); not admitted
  on a lamp without arms or outside the local detector law. "ordinal" is
  the counter form as built, u = (ordinal - 1) r mod W from `wheel`
  [r, W] (declared where a diagnostic wants the open channel); "seed" is
  the seed-set order declared wherever the Bell rows run, u =
  order[(ordinal - 1) mod W], where order = `core.integer.keyed_permutation`
  (W, residue_seed) is the Fisher-Yates shuffle of range(W) driven by
  `core.integer.mix64`, the SplitMix64 mixing hash copied from
  `docs/designs/detector_law/order_channel_hidden_pins.py`'s `mix64` and
  `permutation` verbatim (the constants 0x9E3779B97F4A7C15,
  0xBF58476D1CE4E5B9 and 0x94D049BB133111EB, the shifts 30, 27 and 31,
  plain integers masked to 64 bits, the same order on every host; the
  lamp's number is NOT mixed in: the seed is per world and one lamp
  births the pairs). The stride r must be 1 under "seed" (refused
  otherwise), so W births take every residue once; the order repeats
  from the first residue beyond W births, so a Bell world counts exactly
  W births.
- `residue_seed`, an integer in [0, 2^64) (an input of kind 1, the width
  declared), required under "seed" and refused under "ordinal" (a key
  that does nothing is refused); the World Generator draws one per world
  from the host's entropy, independent per world and never written into
  `expectations.json` or the paper; the engine forms the order once at
  its construction and writes the seed to no line.
- THE STAMP'S FIELDS, none new: the gather line's `click` (the chosen
  cell's first rung, the detector's count in its own clock), `birth` (the
  record's birth interval) and `chosen` are the reader of record's three;
  the gather line's `u` and the `records` reading's `u` are HOST, the
  input of the diagnostic E_N, never a reader-of-record field (ENGINE.md
  says so). The ladder, `cell_of`, the tables and the pins do not move.
- THE PREFLIGHT (Reviewer 3's CHECKs 1 and 2): `tools/preflight_worlds.py`
  refuses a world with a pair lamp under "ordinal" and one short of W
  births within its ticks at the lamp's rate or within its stock (the
  shipped Bell worlds' ticks 300 give about 300 births and not 2048; the
  World Generator regenerates them).
- The test: `keyed_permutation` a bijection on Z_W at W = 16, 256 and
  2048 for four keys, the same key the same order, two keys two orders,
  no key the counter's order; a pair lamp without the key refused; on a
  chain of 80 with a two-arm lamp at x = 40 (the wheel [1, 64], 64 births
  held, receivers at x = 60 and 20) "ordinal" gives today's u, 0 to 63 in
  order, and "seed" every residue once in the permutation's order (the
  engine's `birth_orders`), two seeds two orders, the same seed the same
  order; the 128 arm records click once each and the four cells' counts
  (the two receivers, the two sponge faces) are the same under either
  order (the derivation's claim; a GAMEBOARD reading, no pin); the gather
  line keeps `u`; the refusals (the stride 2 under "seed", the seed absent
  under "seed" or present under "ordinal", a value that is neither, either
  key on a lamp without arms or outside the local detector law). The
  bar world of `tests/test_detector_law_tables.py` declares "ordinal" and
  reads as before.

## 16. Reviewer 3's two lines on item 6b (the Boss's 04:55Z)

- LINE 1 (built, test (ag) and the coupled chain of (k)): `take` is
  REQUIRED on an absorbing block of a massive kind, refused absent
  naming it: light's pair [-15, 56] on a massive kind's take line would be
  an implicit default of a physical rate; light's kind alone keeps the
  law's [-15, 56] (a light-kind mirror line has no take).
- LINE 2 (NAMED for 09:00, not built; on the Boss's word): the take's
  pair is declared per KIND (the family's table, kind 2) while the build
  keeps it per NODE (`take_num`, `take_den` written at the block's cells
  and moved with it), so in a mixed world a LIGHT record crossing a
  matter take line is taken with the matter pair; the pair belongs to
  the record's family. The line: the take arrays per family (one pair
  per kind per Node), the ghost's pair read by the record's family; a
  world of one taking kind per line reads the same.

## 17. The grace's end at a set bound to its emitter (Reviewer 3's nit on 906d3635)

At the grace's end the set Node's own row, which evolved freely during
the record's grace, is taken as the hop rule takes an entered Node's
content: the interval's motion there (the rule's next level less the
current) squared is booked to the set's pointer and to `absorbed` before
the row is held at 0 (`LiveRecord.was_exempt`, `_advance`); the ledger
stays balanced (test (ac)'s assertion at every interval) and the
booking is one Node's content, below the ringing's per-interval booking
on the light clock's chain.

## 18. Item 10, THE RULE: every emitter takes its own record's remnant from the first interval after its train (DECLARATIONS.md section 10 item 10 and section 15 M1-4 at remnant-rule e6b4ec3d; the model owner's word of 06:42Z, record 1694, and his word of 07:27Z, record 1711, the timing integer withdrawn; Reviewer 3 and the physicist's recommendation T = 0 of 07:18Z and 07:22Z; the Boss's 07:45Z; `detector-law-build-3`)

- THE LINE (`_own_take`, `_advance`, `_form_take_masks`): from the first
  interval after its train (a lamp's record at age > train; an emitting
  block's after its sourcing cycle) the record's own emitter's Nodes (a
  lamp's Nodes; the block's CURRENT cells) are a taking set for THAT
  record alone in the receiver form: the row held at 0 there, one ghost
  per Port in the record's OWN KIND'S pair (the family key `take` [n, d]
  on a MASSIVE kind, refused on light's kind, required where a lamp of
  the kind exists, Reviewer 3's line 2 on item 6b; light's kind the
  law's [-15, 56]), the Ports of the record's taking set (the receivers
  and its emitter together) formed per record with one slot per (axis,
  sign) so a record's Port arrays keep their index, a Port new this
  interval (the first, a hop) starting at its free neighbour's level
  with no jump booked. The tail of the train still inside the cells at
  the train's end (at most 12 percent of the record's motion on the
  light clock's chain, the reading below) is taken with the remnant.
  What the emitter takes is booked NOWHERE as motion (the ledger books
  content): onto no pointer and not into the record's `absorbed`, so
  the ladder never sees it (the grace's `keep` exclusion made permanent)
  and the record's completion comes from what the sets and faces took;
  a record its emitter took wholly has energy 0 and completes with no
  cell chosen, its content booked to the ledger's HOST row
  `taken_by_emitter` (not to `escaped`: the remnant never left the board
  and is not received back), the books balanced with the new row
  (`transit.taken_by_emitter` in the books and run.json); the gather
  line carries `taken_by_emitter` (the content so booked, 0 where a cell
  was chosen) and the records reading `emitter_taking` (whether the
  emitter's take has acted), both HOST. The emitter never clicks on its
  own record; the block's own massive record is untouched; during the
  train the cells insert as built; the sets' `own_grace` stands. NO KEY
  and no load-time integer: the earlier forms (a per-world key
  `remnant_take`; T = ceil(extent / v_g) + 2 computed at load in the
  tables' fixed point, 24 for a side-12 block at the 12-Link clock, 4
  for a one-Node lamp, 23 for the light clock's A at its clock [1, 1])
  are HISTORY of 2026-09-24's morning, withdrawn by record 1711; a
  `remnant_take` key written into a world is refused as unknown. THE
  WORLD KEY `wheel` (the Boss's line (5)): a detector-law world with a
  set, no lamp and no `wheel` is refused at load naming the key (the
  guard that would have caught the sagnac files' ladder at W = 1).
- THE TAKE'S START: the interval whose start is the record's age `train`
  is the first after the train (a lamp's drive writes last at the age
  train - 1; a block's record is sourced last in the interval before the
  next record's birth, its `train` that age), so the take acts from
  `age >= train` and the row is 0 from the age train + 1 on (test (e);
  the light clock's cells the drive's at 69, 0 from 70, test (ac)).
- THE SET THAT IS THE EMITTER'S CELLS (the form without positions, R2's
  and the sagnac worlds', `block` alone): line 7's exemption (the set
  free for the block's own record during train + own_grace) and item
  10's take name the same Nodes there; the take wins at the emitter's
  own cells from the train's end and the exemption keeps only a set's
  Nodes beyond them (the positions form's free Node). Before this line
  a cell both exempt and taking was neither held at 0 nor free (the
  row evolving while the rule read the Ports' ghosts as its neighbours),
  stable at rest and growing without bound on a stepping block: the
  World Generator's sagnac_k3 (k = 3, own_grace 3000) was refused by the
  amplitude bound at interval 1357, its records' levels tripling every
  50 intervals at A's trailing cells from about 1100 (EXPLORATORY, on
  this branch before the line; at 36fd5235 the same intervals read
  levels of 1.2 x 10^7, stable). Test (ai) pins the form at rest and at
  k = 3: the own record's row 0 at the current cells from the first
  interval after its train at every interval, the set booking nothing
  of it, the books balanced, every level below four times the seed.
- THE HOP'S TAKE OF THE BLOCK'S OWN RECORD AT EVERY AGE (the physicist's
  finding on the Preliminary Runner's sagnac_k3 at 540456da, 09:12Z; the
  Boss's 09:30Z): `_move_block`'s hop rule exempted the block's own
  emitted records only during the hold of train + own_grace, so once the
  hold had ended a step onto an own record's remnant booked that Node's
  content onto the block's own pointer (at_a's pointers on 37 of A's 69
  open records, first rungs on 16 of them at about 3500 after the birth,
  a self-click one record away at 0.14 percent of the absorbed against
  the click's 1 / (2 W) = 0.195). Item 10 has the emitter's take of its
  own record on no pointer and not into `absorbed` at ANY age, so the
  hop now holds the entered Node at 0 for the block's own record and
  books nothing, from the first interval after the train on (during the
  train the row evolves, line B); a foreign record's entered content
  books as before. Test (ak) pins it on a stepping block with own_grace
  70 and a lamp behind it.
- A BLOCK THAT STEPS OFF THE BOARD REFUSES THE INTERVAL (Reviewer 3's
  line from the Preliminary Runner's redshift dry run, the Boss's 09:45Z:
  the receding block ran off the board at tick 9722, its sum 0 from
  9756, the run going on to 14686 with the books balanced): at a hop
  whose cube is cut by a zero face (`_cube` on a non-periodic axis, the
  count of cells below the count before the hop) `_move_block` raises,
  naming the block, the interval, the corner and the cells left; a
  periodic axis wraps as before. The margin rule refuses such a block
  at load; this is the run's own check (the cheaper of Reviewer 3's two
  forms, the margin's distance the load-time rule's). Test (al): a
  block pushed toward the open face refuses at the interval its cells
  would leave, having stepped before; on a periodic chain it wraps on.
- THE GUARD (Reviewer 3, 07:43Z, on the sagnac_k3 phantom): before the
  booking loop an absorbing Node whose cell is the sentinel refuses the
  interval naming the Node (a Python list's index -1 would otherwise
  book it to the last cell, the +x face); test (e) trips it by hand.
- WHAT MOVED: every lamp's record is taken at its lamp's Nodes from the
  train's end (before: after the grace of two periods, onto the lamp's
  own cell, the first build's afterglow, which could win the ladder), so
  test (p)'s three digests moved once more (the state digest by the
  take's start at the age `train`, the record alive at 600 carrying
  its pointers); an absorbing block's own cell now stamps its first rung
  with the block's count in the generic offer loop (key (i); before,
  only the clock body's path stamped it, a gap the afterglow had
  hidden); no world file changes.
- READINGS (EXPLORATORY, before the GO, none pinned; test (ac) on the
  light clock's chain of 173, the world's `wheel` 64, the set at x =
  112, own_grace 70, W = 64): the level at A's cells is the drive's
  millions at 69 and 0 from 70 (GAMEBOARD); the set books less than one
  rung of A's own record between the grace's end and the return (5.4 x
  10^10 at 208 against the rung 6.7 x 10^10); the set's first rung reads
  214 after the birth on this chain (the declaration's pin run reads it
  beside 218 +- 2; the map's transit 207.85), the return's rise 2.7 x
  10^12 from 208 to 240. THE SWEEP over a delay after the train, the
  reading that withdrew the timing integer (the first rung; the pointer
  at 208): 0: 214 (5.4 x 10^10); 4: 174 (8.5 x 10^10); 8: 157 (1.2 x
  10^11); 12: 152 (1.4 x 10^11); 16: 151 (1.5 x 10^11); 24: 147 (2.1 x
  10^11): every interval of delay lets the remnant's alternating mode
  (the band's edge, group pace 0) spill onto the free Nodes beside the
  face, which the emitter's cells do not take. THE CELLS' SHARE of the
  record's motion energy with no take (the Boss's line (6)): 12.3
  percent at 70, 6.2 at 80, 16.3 at 90, 20.5 at 94, 21.5 at 100, 19.2 at
  110, 13.7 at 120 (the largest level inside 5.6 x 10^6, 2.0 x 10^6, 1.4
  x 10^6, 4.2 x 10^5, 1.2 x 10^6 at 70 to 100; the twelve free Nodes
  beside the face 27, 25, 21, 23, 17, 18 and 22 percent): the tail has
  left by about 94 while the remnant's motion share rises, its level
  about 10^6 alternating each interval. Test (k)'s clock-body case: the
  record's click went to the lamp's own cell at 981 (the afterglow);
  under the rule the lamp takes it and the record lives on past 1200
  with the clock body radiating into it (pinned as a reading; it
  completes at the clock body's cell at 2437, EXPLORATORY).
- THE COMPLETION AT W = 1 (Reviewer 3's second point, 07:43Z): the
  record completes when the motion left on the board is below one rung
  (norm / W) of what the receivers hold, so at W = 1 a record closes as
  soon as the board's motion is below the whole of the absorbed; the
  sagnac runs of 906d3635 ran on files without a world `wheel` (W = 1),
  so their completions are that file's, not the law's; the `wheel`
  refusal above stops such a file at load.
- THE PREFLIGHT (Reviewer 3's nit): CHECK 2 prints the interval of the
  W-th birth and the margin the ticks leave for the arm's transit and
  the completion, which the tool does not check (the world's geometry,
  the World Generator's line).
- THE THREE TESTS: generic (the take primitive as built, no family
  name), vector (the receiver form's verbs, no root, no float), local
  (the emitter's own Nodes, its own record).

## 19. The joint gather: the polariser's two cells and the pair's one ladder (DECLARATIONS.md section 1 item 3, section 14 item 6, section 15 T-1; the model owner's word of 2026-09-24, about 09:48Z, "go with the recommendations", the Boss's order of 10:00Z; `detector-law-joint-gather` off `detector-law-build-3` at 1529d20)

The finding it answers (the Preliminary Runner, records 1770 to 1779): on
every engine every gather's ladder held one cell, the arm's own table's
cell "0", no joint cell and no channel; the Bell and Malus pins were
unbuilt. Three commits, one per component; the first builder's take and
click lines untouched (the ladder's head of `_click`, the completion loop
of `step` and one call after the booking loop of `_advance` are this
build's, as named to the Boss at 10:32Z).

| Component | The declaration | The code | The test |
| --- | --- | --- | --- |
| 1. The table body of two cells | Section 14 item 6: a polariser is a TABLE BODY of two cells on the arm's line; the entry cell its Node, the exit cell the next Node beyond it; the record's offer at the entry's Ports split by [C'[s]^2, S'[s]^2] over n_s with the remainder kept, the + share to the exit, the - share to the entry; the click's interval the first rung of the whole offer at the body over W, its cell by u on the ladder of the two weights; the three tests held (one primitive, verbs B, D and E, the entry's own record and its one Link to the exit) | `TableBody`, `_polarisers` (a measured event whose table entry carries an integer `phase_window` on a family; its arm the one of the family's ONE lamp whose direction points from the lamp to the body, the exit Node body + direction, on the board and free; a reading of the window's centre, a body on no arm, two lamps, an exit off the board or taken, or no set of one Node naming the body: refused at construction), `_table_body` (the cells `<set>+` at the exit and `<set>-` at the entry, in that order on the ladder, both take Nodes booking to the body, on the set's wheel; the pair from `amplitude.half_angle`, the amplitude law's own integers), `_split_table_offers` (called once per interval after the booking loop: the entry pointer's gain since the last split times C'^2 over n_s, the remainder per record, moved to the + cell; the whole offer's rung stamped on both cells; `absorbed`, the norm and every other cell untouched), the gather's cell triples [set, channel, label] from `cell_set` and `cell_channel` (every cell as built [name, 0, "0"], so the lamp worlds' lines are byte for byte: test (p)'s digests unchanged). The rotation U_s enters through the split's weights and the joint weights; the rows are taken at the entry. THE READING NOT TAKEN: the `directions` of a measured event default to the six headings and cannot name the arm; the arm is the lamp's | `tests/test_detector_law_tables.py` (d): two cells, the shares within a unit of the declared share, one rung for both cells, the gather's triples, 64 / 32 / 0 of 64 at s = 0, N / 4 and N / 2 over the full wheel (the pin's form, 128 of 256 at 45 degrees), the books balanced; the four refusals |
| 2. The pair's one gather | Section 1 item 3: the pair's record gathers ONCE, its ladder the four joint cells (++, +-, -+, --) with the weights R = J^2, J(o_A, o_B) = SUM over the labels l of U_a[o_A][l] U_b[o_B][l] over both arms' tables (the declared integer pairs, no root, no float), the birth's one u choosing one cell, each arm's table counting its own channel of it; an arm's own two-cell ladder is NOT the Bell reading (Reviewer 3's withdrawn line); Malus the one-table case of the same ladder | `joint_weights` (per body its half-angle pair and its arm; U_s the row the channel, the column the label's bit on the body's arm, as `amplitude.rotation`; J over the birth's joint labels with their weights; R = J^2; the cells in the lexicographic order of the bodies' channels; one primitive for two bodies or one), `pair_bodies` (a lamp of several arms needs ONE table body of its family on each arm, in the sets' order; refused otherwise), `LiveRecord.arm_done` and the completion loop of `step` (an arm that completes waits, its rows still; the pair gathers when every arm has), `_click_pair` (the ladder over the four weights where every arm's offer reached its body, else no cell; the content, the arms' contents summed, one quantum, handed once to the body on the arm it was born on, arm 0; `chosen` the joint cell, one triple per body; `arm_records`; `arm_offers` HOST; `click` the later of the arms' first rungs at their bodies, `click_at` "rung" where both have one, the stamp the interval) | (e): 64 gathers of 64 births, the four cells' order, the counts 16 each at (0, N / 4), 32 and 32 on ++ and -- at (0, 0), on +- and -+ at (0, N / 2), u once each, the content one; (f): Alice's marginal exactly 32 of 64 at four settings pairs, Bob's within one (his cells not adjacent on the ladder); (g): the declared J^2 integers from planted tables, E = 46565 / 65773 at (256, 0) against (237, 98) (COMPUTATION, the form's own number for the generator's `bell.py`), the singlet's zero cells, the one-table case; (b) with the two table bodies and the refusal of a pair lamp without them; the order channel's test on 64 pair gathers |
| 3. The reader | RUN_LIST.md rows 1a to 1d and 9: the four cells' counts per setting, S from the four correlations, the marginals per side; Malus the + channel's share; read from the gather lines, never a pin moved | `tools/click_readings/detector_law_bell.py` (`read_run`, `counts_of`, `chsh`, `report`; integers and Fractions, no float in a number) | (h): the reader on a run folder written by the runner from the bar worlds |

THE BOOKS LINE, named (the Boss's item (1), the preliminary's Alice [0, 1]
against Bob [2048, 1]): in the engine as built the pair's one quantum rode
arm 0, the lamp's first direction (+x, Bob's arm on the GO bar), and Alice's
arm carried 0 (`_births`: "the pair's one quantum on arm 0, a default,
named"), so the asymmetry was the arm-per-record form's, not a physical
reading. Under the one gather the quantum lands once, at the joint click,
on the body of the arm it was born on (arm 0, the lamp's first direction:
bob on the GO bar), the first builder's word of 10:57Z: the quantum lands
where it is born and closes in the joint gather; the gather names the
joint cell, both channels.

THE WORLD FILES (a finding for the World Generator, not this build's):
`malus_45.json` and its three settings at `detector-law-worlds` 0fd1156 put
the polariser at x = 6 on a chain of 7, so its exit cell x = 7 is off the
board and the world is refused at construction naming it; the chain of 8
(or the polariser at x = 5) admits it. Their `read` counter at x = 4 stays
Reviewer 3's named defect of 08:52Z. The Bell four load unchanged (alice at
x = 7 with the exit x = 6 on the -x arm, bob at x = 17 with the exit x = 18).

## 20. The lamp record's ladder by name and the cell over the ladder's own sum (SIZING.md, 2026-09-24; DECLARATIONS.md section 13 item 7, the click line and the receiver by name; the model owner's word of 12:57Z; `engine-fix-3`)

The finding it answers (the Preliminary Runner's two_slits run of 10:45Z):
every one of 1024 clicks at the open face behind the lamp and none on the
screen, because the faces were cells on the record's ladder and held 97
percent of every record, and because the cell of u was taken over the
record's whole `absorbed`, so that with the faces sunk every u above 0.03 W
would have found no cell.

- THE KEY (`world.py`, `LAMP_KEYS`, `LampDefinition.receiver`,
  `_receiver_names`): `receiver` on a LAMP, a detector set's name or a list
  of distinct names, the record's LADDER BY NAME; refused outside the local
  detector law, on an empty list, on a repeated name and on a name no set
  declares (a face is never on it). Absent, the ladder is every cell as
  built: the table rows' lamp worlds are untouched and their gather lines
  byte for byte (the two HOST fields `ladder` and `sunk` appear on a lamp
  with the key alone; the chain world's digests of test (p) unmoved). The
  same word as the block's `receiver` of line (1): a record's ladder is what
  the world names, one set for a block's record, the named sets for a
  lamp's.
- THE LINE (`detector_law.py`, `LiveRecord.ladder`, `_births`, `_click`):
  at birth the record's ladder is the named sets' cells; at the click the
  ladder's weights are the named cells' pointers with every other cell at
  0, so `cell_of` and `rungs` take the cell of u over the LADDER'S OWN SUM
  (the cumulative rule, the first named cell whose rung exceeds u), and a
  sink (a face, an unnamed set) is never chosen. A sink takes and books as
  every cell does (the pointer, `absorbed`, its rung): the record's
  completion (`_complete`, the motion left against `absorbed` over the
  world's wheel) and the record's norm are untouched; the click's time
  stays the chosen cell's first rung against the norm on the set's own
  `wheel`. The gather line carries `ladder` (the named sets) and `sunk`
  (HOST: the pointers' sum at the sinks). The content goes with the chosen
  cell as before; a record whose named cells hold nothing escapes.
- THE THREE TESTS: generic (one primitive, the ladder's weights, no kind,
  no family name); vector (the rung on the pointer, integers, no root, no
  float); local (the record's own pointers, nothing kept at a Node).
- THE TEST (`tests/test_detector_law.py` (f)): the layer of 24 x 7 with the
  lamp two Links from the -x face and three one-Node sets at x = 18:
  under `receiver` [s0, s1, s2] every one of 8 clicks at a named set, the
  chosen cell the first named cell whose rung exceeds u on the gather's own
  rungs, the counts over the wheel of 8 the rungs' differences (3, 2, 3),
  the sinks' share printed and below the whole, the books balanced at
  every tick; without the key the same world clicks at face:-x (the
  control); the string form names one set; the four refusals.

## 26. The emitter as a clicking body: the excited records in turn, the birth written once (ALGEBRA.md 9.17 (4), the mathematician's integers of 2026-09-24 on the physicist's five questions; LAB_TOOLS.md A.1; the model owner's word of 22:30Z, "we cannot do any operation on the cells except to produce a click"; `emitter-click`; sections 24 and 25 are the material mirror's and the crystal's on their own branches)

1. THE FORM. Neither emitter on main was the algebra's: the lamp births
   from a rate accumulator with no record behind it and drives its cells
   with the cosine table every interval of the train (an overwrite); the
   block emitter "clicks" on a count of the sum of its own record that
   deletes nothing, and fills its light record every interval of the cycle
   by the coupling's source term. The form (9.17 (4)): the emitter is a
   BODY OF A MASSIVE KIND with its seed (the bound mode) and a stock
   `amount` = M, the number of its excitations. At interval 0 its first
   excited record is on the board (the seed at both levels, the body's own
   record as before), its residue u_1 from the emitter's wheel [step, W] in
   its residue order. Excited record k clicks at ITS OWN RUNG on its own
   cells: E is its own motion (now - before)^2 summed over its cells and
   booked to its offer C interval by interval (read-through, no take; the
   massive advance as before, the coupling's receive term included); D is
   the rung 2 T u_k + T <= 2 W C with T its norm. At that click X ends the
   excited record (deleted from the records) and E^T births the photon and,
   while the stock lasts, excited record k + 1 (the seed again, the next
   residue, its offer from 0). The emission times are the rungs, spread by
   the residues over the wheel. No rate, no train, no drive, no source
   term (`block.current` and the emission by the cycle stay unused by this
   form; they retire with `emits` in the next push).
2. THE INTEGERS AS BUILT, and the two read by the physicist, named for the
   gate: (i) T, "its norm", is the excited record's seed squared and summed
   over the body's cells (the record as written at both levels; nothing
   else on main is a norm for a massive record); (ii) the born values,
   written ONCE at the click's interval on every cell of the body at both
   levels: now = A C[phase(0)] and before = A C[phase(-1)], phase(age) =
   (3 N / 4 + floor(age n / d)) mod N (main's `_phase`) on the born clock
   n / d, A the lamp's unit (the cosine table on UNIT); the norm T of the
   born record the motion the write inserts, SUM over the cells of (now -
   before)^2; the residue the excitation's; the content one quantum moved
   from the body's stock (the body's family spent, the born family
   released; the books balance per family). A LINE'S travelling character
   (item 2's now = A C[phase(0) - floor(x p / q)] along the line) is OWED:
   it needs the per-Link pair [p, q], which no world file declares (the
   clock per interval n / d is another number); until it is, every cell of
   the body is written at the vertex's phase, the one-cell broadband birth.
   The one-cell write carries a STATIC LEVEL (the mean of the two levels,
   C[3N/4] = 0 and C[3N/4 - floor(n/d)] != 0), which the sponge faces
   drain slowly: under main's completion a record on a one-cell chain
   lingers about 1200 intervals after its click at the screen; under the
   end at the click (9.12) it does not matter; no count and no rung moves.
3. THE LOADER (`_emitter`, the key `emitter` on a block): {"family": the
   born family (a paid family with the pair form of its clock, not the
   body's own), "wheel": [step, W] (the step coprime to W), "residue_order":
   "ordinal" or "seed" with "residue_seed", "branches": the born labels
   (optional, [[0, 1]]), "receiver": the born records' ladder by name
   (optional, a list; the block's own `receiver`, one name, is the line at
   the rung; not both)}; refused on a body of light's kind, on a silent
   body (seed 0), with `amount` below 1, beside `emits` or `own_grace`, on
   an absorbing block. The refusals name their keys.
4. THE ENGINE (`_excite`, `_excitation_rung`, `_emit`): the birth orders
   for emitter bodies as the lamps' (`keyed_permutation` under "seed");
   the first excitation at construction; the rung checked after each
   interval's massive advance; the emission fired once the interval's
   records are advanced (the born record's first advance is the next
   interval, its age 0 at the birth); the own take is none for a record
   born of an emitter body (its cells are cells like every other after
   the birth), the grace none (no `own_grace`, the train 0), the exemption
   none. The birth line: `excitation` (k), `excitation_norm` (T),
   `excitation_offer` (C at the click), `norm`, `cells`, `u`, `train` 0,
   and the block's clock count under `clock_stamp`.
5. THE SMOKE RUN (a chain of 80, x open; the body of the matter kind
   [800, 809] with the well pair [800, 800] of side 12 at x = 5 seeded on
   its mode at 100 by the generator's `seed_on_the_mode`, the stock 4, the
   wheel [1, 4], the light [77, 25] on N = 64, the receiver at 70): the
   births at 24, 111, 253 and 447 with the residues 0, 1, 2, 3 (the offers
   at the click 11840, 35106, 57472, 81154 against the thresholds T (2 u +
   1) / 8 = 11484, 34451, 57418, 80385 with T = 91868), the four records'
   first rungs at the screen 120, 207, 349, 543, the books balanced at
   every interval, the stock 4 spent and 4 released, no record left.
6. THE TESTS: `tests/test_emitter.py` (a: M excitations give M births at
   the first interval where the offer crosses the rung, tracked interval
   by interval; the residues in the wheel's order and under "seed" the
   keyed permutation; the quanta conserved; the excited record ended and
   the next seeded; a stock below and above the wheel; b: the born values
   equal the cosine table at phase(0) and phase(-1) on the body's cells
   and 0 elsewhere, the norm the squared steps, no drive and no own take
   afterwards, nothing beyond Manhattan distance m before age m; c: the
   loader's refusals). NEXT on this branch (the Boss's order of 23:30Z,
   item 2 with 9.12 folded): the lamp's `rate`, `train` and `_drive` and
   the block's `emits`, `own_grace` and cycle births retired under the
   detector law; every listed world regenerated onto emitter bodies seeded
   on their modes; the tests rewritten; the light clock's, Sagnac's and
   the redshift's readings re-derived blind before any run.
7. THE RETIREMENTS (the second push of this branch, 2026-09-24): under
   the detector law the lamp is refused at load ("lamp is refused under
   detector-law-v1": a birth has a clicking record behind it), and with it
   `emits`, `own_grace`, the cycle births and the coupling's source term
   on a block (`block.current`), the lamp's `_births` and `_drive`, the
   grace (`_in_grace`), the exemption (`_exempt`), the emitter's own take
   (`_own_take`, item 10 of DECLARATIONS.md section 10), the fresh Port
   and the fields `was_exempt`, `own_previous`, `emitter_took` and
   `sourcing`; `_advance` reads every record with the world's take masks
   and nothing else; the ledger's HOST row `taken_by_emitter` stays at 0
   for the readers. The simulation's wheel is the largest of the emitter
   bodies' W and the world key `wheel`; a world with a detector set and no
   emitter body declares `wheel`. The table bodies read the records of the
   family's ONE emitter body (`_table_settings`; the exit cell away from
   the body's centre). The lamp's forms stay in the amplitude law.
8. THE RUNAWAY WELL (a finding of this push, COMPUTATION): the wells of
   the smoke runs, [800, 700], [800, 500] and [800, 400] on the kind
   [800, 809] and [157, 137] on [156, 157] on a chain or a layer, have
   their largest eigenvalue AT OR ABOVE 2 (2 cos omega_b = 2.03, 2.47,
   2.95 and 2.04): no oscillation but a level growing by 1.2 or more per
   interval (a one-cell well on a chain runs away at a depth that binds on
   a cube, the folded axes' self-reads counting fully). Their "cadences"
   were the runaway's and are withdrawn; the coupled chain's own record
   reached the amplitude bound at interval 362 through such a well beside
   it. The margin module refuses a runaway naming it (`MarginReading
   .runaway`, `check_margins`; test (n)'s fifth case) as it refuses an
   unbound mode. THE ONE WELL for every one-cell emitter body of both
   generators and the tests: [8, 7] on the kind [7, 8] (the index worlds'
   kind, omega_0 = 0.505): bound on a chain (2 cos omega_b = 1.90, omega_b
   = 0.32, the extent 1.4 Links, the period P = 20 intervals) and on a
   layer (1.75, 0.50, the extent 15 Links, P = 12); the massive worlds
   carry it as the family `source` beside their matter kind. THE CADENCE
   (the rung of item 1 with the norm of item 13, the mathematician's 9.17
   (5) item 1: the seed's squares made the wait scale as 1 / omega_b^2, a
   unit accident, withdrawn): the u-th residue clicks about (2 u + 1) P /
   (2 W) intervals after its excitation, the whole wheel of W in about W
   P / 2 whatever the well's depth (the Malus bar's 256 in about 2560,
   the engine reading 239 births within 3200, MALUS_TICKS 3800,
   COMPUTATION); a world whose ticks hold a part of its wheel births that
   part, the regeneration of the fifteen reads it. The
   margin rule skips an axis the body spans (`shape[axis] <= side`, an
   emitter of side 1 on a chain or a layer).
9. THE ONE-CELL BIRTH'S CHARACTER (COMPUTATION, on the write of item 2):
   the write now = C[phase(0)] = 0, before = C[phase(-1)] on one cell (or
   on cells in phase) is a velocity impulse. For light's kind it leaves a
   STATIC LEVEL between two fronts (the rule's zero-frequency mode: A's
   twelve cells of the light clock hold 1.06 x 10^6 unmoving after the
   fronts leave), the fronts alone carrying the motion the sets take; a
   front's edge disperses on its way, so a set fifty Links off crosses
   its rung (the coupled chain's block at 21 to 24 intervals after the
   front's first motion) and one 180 Links off does not, the record
   completing on the fronts' motion (energy x W below what is taken)
   with the level left; the mirror wall of test (ad) leaks 3.1 percent of
   it (1.45 of the train). A one-Node take set on a chain takes the whole
   half arriving at it (its row held at 0, nothing passes): the light
   clock's set at x = 112 takes the +x half, its rung two intervals after
   the birth, and x = 171 stays 0 with the faces closed and open alike;
   the return through the closed face, read under the exemption of old,
   is re-derived in the mirror item with a geometry the set does not
   block. For a massive kind the impulse has a STANDING PART at the gap's
   frequency (no group pace) that oscillates at the emitter and keeps
   the record from completing (test (aa): the travelling part's rung at
   the screen 158 intervals after the birth, the line at the rung, the
   record alive at 1000). THE REMEDY is item 2's line with the per-Link
   pair (a written travelling character), owed to the mathematician's
   gate; every DETECTOR reading pinned on the lamp's train stands as
   written until re-derived on the emitter before its run (the Boss's
   order of 23:30Z).
10. CONTENT FOUND ON A TAKE NODE: a record written on a set's own cells
   (an emitter whose set IS its cells, the form without positions of R2
   and the Sagnac worlds) is taken as the hop rule takes an entered
   Node's content (DECLARATIONS.md section 13 item 4): its motion squared
   booked to the cell at the interval's end and its rows held at 0 from
   there, so that the set reads the write itself, the whole norm at once,
   the SELF-CLICK of that form (E E^T = T; the click line at the birth's
   next interval stamped with the block's count, the record then complete
   and closed after its click) and nothing of a record vanishes unbooked
   (before this line the born record was zeroed at the cells with nothing
   booked and closed without a click); the rule's step of that interval
   reads the content as it stood (a planted row's integers unchanged,
   tests (a), (b), (m), (w)). A usable receiver stands at a free Node
   beside the body (the positions form); the Sagnac worlds' form is read
   at their regeneration. Named for the gate.
11. THE WORLDS: both generators write emitter bodies (`emitter_body` in
   the detector-law generator with EMITTER_KIND [7, 8] and EMITTER_WELL
   [8, 7]; `emitter_at` in the massive generator, the family `source`
   added by `world` where a body names it), every bound body seeded on
   its mode by `seed_on_the_mode` over every massive family; the four
   Bell worlds held in `docs/designs/detector_law/held_worlds/` until the
   crystal (HELD_NAMES; the lamp's arms have no emitter form yet); the
   preflight loads 29, refuses 0, misses the held 4. The Malus bar of 8
   keeps its emitter at its cell (the extent 1.4 Links within the bar).
12. THE TESTS: `tests/test_detector_law.py` on `chain_world` with the
   emitter body at x = 2 (six births on the wheel [1, 6], the order
   channel on the body, the cells like every other: no own take, the
   ledger row 0, the world key `wheel`, the guard; the lamp, `emits` and
   `own_grace` refused); `tests/test_detector_law_tables.py` on that chain
   (the splitter and the polariser; the bar and the pair worlds retired
   with the lamp, returning with the crystal); `tests/test_massive_record.py`
   rewritten test by test onto emitter bodies (the block world's source,
   the coupled chain's emitter fifty Links before the block, the matter
   emitter world of (z), (aa), (ab), (af) and (ag), the light clock of
   (ac) as item 9 reads it, (ah) with the line at the set's rung, (ai)
   and (ak) the self-click of item 10, (ad)'s leak, (n)'s runaway, (p)'s
   digests moved once more); `tests/test_body_conditions.py` (g) with
   the emitter bodies read clean; `tests/test_preflight_worlds.py` without
   the pair lamp's CHECKs (held with Bell); `tests/test_receiver_by_name.py`
   on emitter bodies (the line at the rung on the chain of 200, the
   self-click of the form without positions, the light clock's set beside
   A, two bodies naming the free Node between them, the close without a
   click at a receiver of wheel 1, `sagnac_rest.json` loaded and stepped
   with no line under item 10). Every number in them is the engine's
   reading on this head, COMPUTATION; no pin.
13. THE MATHEMATICIAN'S FIRST HEAD READ AND THE FLUX (ALGEBRA.md 9.17 (5)
   and (6), 9.19 (2) and (3), his heads 5028b92f and d58ab749; the owner's
   "plant board values and check everything works as expected"; the
   Boss's GO of 22:22Z), the third push of this branch:
   (a) THE EXCITED RECORD'S NORM T is the offer its own mode books over
   ONE PERIOD P of its clock (P the nearest integer to 2 pi / omega_b),
   in the flux's units of 9.19 (3): the one-way inward flux into the
   body's CENTRE CELL (the lower corner plus side // 2 on each axis, one
   Node; the cell itself for a body of side 1) summed over P intervals
   of the body advanced ALONE. The generator writes it as the emitter's
   integers `period` and `norm` (`excite_on_the_mode`); the loader
   recomputes it by the same advance and refuses a mismatch (a load
   check in `check_body_conditions`, not the law); the rung 2 T u + T <=
   2 W C unchanged, C the one-way flux into the centre cell interval by
   interval (`_excitation_rung`). Read on the board (tests/test_emitter.py
   (a)): the body alone, the flux into x = 11 over P = 70, bit for bit
   the declared norm.
   (b) THE WRITE ON THE CIRCLE OF 2 N (9.17 (6)): now = A C_2N[3 N / 2 +
   s] with s = floor(n / d) the born clock's step and before = -now
   exactly (the character half a step either side of its zero, no static
   part; for even s the pair C_N[3 N / 4 + s / 2] of 9.17 (5) item 2); on
   [77, 25] at N = 64 the entry 99 of the 128-step table, 38 of 256, the
   level 155648; an odd s where 2 N exceeds the tables' bound (65536) is
   refused at load, none of the fifteen has one; the light clock's [1, 1]
   writes 13 of 256, never 0. The static level of item 9 is gone from the
   write.
   (c) THE BORN PROFILE `born` (9.17 (5) item 3): the born record's two
   levels over the whole board as material ({"now", "before"}, one
   integer per Node), copied at the click; the loader refuses a wrong
   count or a profile that writes no motion; the line's travelling
   character is written this way when a world declares it (none yet).
   (d) THE DRIVEN MASK (9.17 (5) item 4): every born record's `driven`
   set is empty, its own datum, no branch on the family's kind.
   (e) THE COMPOSED OPERATOR (9.19 (2)): the stability condition read on
   the whole board, every body's well of a family in one read matrix,
   the largest eigenvalue below 2 or the world refused naming the family
   and the value (`composed_largest_eigenvalues`, printed as COMPUTATION
   with the body conditions); the per-body reading of item 8 stays for
   the margin.
   (f) THE FLUX READING BUILT AS THE ENGINE'S INTEGERS AND CHECKED ON THE
   BOARD (9.19 (3); tests/test_flux_reading.py): the local identity
   e_i(t) - e_i(t - 1) = SUM_j G_ij with G_ij = (1 / 3) A_ij (now_i
   before_j - before_i now_j) holds on the rule's integers EXACTLY up to
   the per-Node remainder term of 8.2, (a_next,i - a_before,i) (r_i -
   r'_i) / (3 num_i), on random rows for light and the matter kind (a
   periodic chain of 60, five intervals); a Gaussian packet of 40 Links
   at k = 0.3024 gives a one-way inward flux into one cell of 0.9865 of
   its I over its passage (the backward part of the planted packet the
   rest), the signed sum 7 x 10^4 against 6 x 10^11; `inward_flux` (the
   one-way flux into a mask through its outer Links), `flux_offer` (per
   cell) and `conserved_form` (3 I x the family's wall, wall the least
   common multiple of the pairs' numerators; the [8, 7] well on [7, 8]
   gives 56) are the engine's, exact against the Fraction forms on
   planted rows. The engine's open face is a take (the sponge), not the
   rule: on an open chain the identity breaks at the face cells only.
   (g) OWED IN THIS LINE, on the mathematician's answers to the three
   questions of 22:17Z (the open face under the flux; the deletion of
   the whole record at the rung and the ladder; the centre cell): the
   receivers' reading E as the one-way flux through their Ports with T
   the record's I, the take retired from the engine (the rows no longer
   held at 0 at a set, the sponge per his answer), the worlds and tests
   re-read, the first-rung pins of M2, Sagnac and the light clock
   re-derived blind; and the owner's decision of 22:20Z, the residue from
   the law's remainder at the birth cell (no declared residue or wheel),
   as he specifies it.
14. THE PROPERTY TEST ON THE ENGINE AND E AS THE FLUX (ALGEBRA.md 9.19 (3)
   with the mathematician's answers of 22:28Z, 9.20 (B), 9.21 (3); the
   owner's adoption, record 1875; the Boss's order of 22:39Z and the
   mathematician's cleanup order of 22:50Z, steps 0 and 1; the fourth
   push of this branch). THE GATE FIRST: tests/test_board_properties.py
   runs 9.20 (B)'s six properties on the engine's small world (a cube of
   12 x 12 x 12 periodic on every axis; light [77, 25] and the massive
   family [800, 809]; one well of side 2 at the vertex (3, 4, 5) with the
   pair [800, 801] seeded on its composed mode; one light record planted as
   its birth writes it on the cell (8, 2, 7); one receiver of one cell at
   (9, 9, 2), bound to the well in this head's loader form; W = 8; 90
   intervals): (1) 48 of 48 transformed worlds give the transformed states
   bit for bit, remainders included, and the same click at the same
   interval; (2) 7 of 7 translations; (3) the light's quantum constant
   until the click and gone with the deleted record, and per record the
   form I less 8.2's accumulated remainder term the same rational at every
   interval, exact; (4) 90 intervals and 90 of 8.8's inverse (`step_inverse`,
   the reverse column order, `_advance_inverse` the rule backwards with
   the ceiling) return the initial element bit for bit, and with the
   receiver named the inverse from 90 returns the state at the click's
   interval with every remaining summand bit for bit, the deleted one in
   neither; (5) a one-unit change at one Node stays inside the Manhattan
   ball of radius m at interval m and is nonzero for every m <= 12; (6)
   200 random elements with two Nodes of equal seven inputs give equal
   outputs, and two runs differing only in their residues are identical
   until the first click; (7) the scaling check the owner asked (the
   Boss's 22:55Z; HOST): the host time per Node per interval 15, 5.0 and
   1.1 microseconds and the peak memory per Node 426, 317 and 187 bytes at
   12^3, 24^3 and 48^3 (the small board's fixed costs dominate it, every
   step linear or bilinear in the levels), the generator's composed mode
   0.01, 1.4 and 2.4 seconds. The reference record clicks at 81 with u =
   0 (9.20's "60 intervals" reads on the prototype's flux, three times
   the engine's, item 13's finding to the mathematician). THE FLUX AT
   EVERY SET: after each interval's step the one-way inward flux into
   every cell (`flux_offer`, the two levels after the step, the
   prototype's reading) is booked to the record's pointer C at that cell;
   the ladder of a record is its emitter's named sets in their declared
   order, or its block's one receiver, or every detector set as declared,
   the face receiver last (`_ladder_of`); at every interval the cumulative
   sums L_k are read in that order and the click fires at the first k
   with 2 W L_k >= (2 u + 1) T (`_ladder_click`; T the record's conserved
   form at its birth, W the set's wheel on this head, the record's own
   from step 2), the line written with `click` that interval, the content
   handed to the set's body (a set without a body, the face included,
   consumes the quantum as any click does), and the record deleted whole
   after the interval's advances (`self.dead`, 8.8's one deletion). THE
   FACE RECEIVER: an open axis carries the set `face` on its border layer,
   last on every ladder (record 15 kept); a periodic axis has none; a
   `closed` face is a zero row with no receiver. RETIRED IN THIS PUSH: the
   take (no Node absorbs: the rows evolve at every cell, the Ports' ghosts
   read by nothing, the masks empty), the sponge, the completion
   (`_complete`), the close (`_close_clicked`, `_close_without_click`,
   `_click` at the close), the pair's click at the close (`_click_pair`,
   the crystal's rework), the clock body's booking (`_book_response`), the
   hop's booking of an entered Node's content, the line at the rung
   (`_line_at_rung`), `escaped` on a record and on the click line (the
   ledger's row stays at 0 until the books' rewrite), `earlier`; every
   test of those forms rewritten or removed in the same push (the Boss's
   rule of 22:55Z): tests i, k, u, ai, ak and ag of
   tests/test_massive_record.py (the take at a clock body's cell, the
   absorbing block, the completion, the self-click of a set at its own
   body's cells, the take's pair on a massive kind) removed; aa, ac and
   ah rewritten; tests/test_receiver_by_name.py rewritten (the cells off
   the ladder book and are never chosen, the line's `T` counts them, a
   block's own cell on no ladder, sagnac_rest's records clicking at the
   other body's set); the chain digests of test (p) moved. THE TAKE'S
   DATA (the `absorbing` and `take` keys, the take masks, a record's
   Ports and `driven`, a block's `taking`) is switched off here (the
   masks empty at every construction and hop) and is REMOVED with the
   loader's rewrite of step 2, where its refusals are rewritten. THE
   LADDER BY NAME in the NAMED order (9.19 (3) (b), "its declared
   order"): `live.ladder` follows the emitter's `receiver` list, a set's
   cells in the cells' order within it; the click line's `ladder` and
   `sunk` read `_ladder_of` (the face last). THE WORLDS: every emitter
   body's `norm` regenerated (the flux read from the two levels after the
   step, item 13's reading before the step withdrawn); the four Malus
   worlds moved to held_worlds/ with the Bell four (below). THE TEST
   WORLDS' FACES: the chain of 80, the layer of 24 x 7, the emitter's
   unit chain, the chain of 200 and the splitter's layer are CLOSED
   (mirrors) since the flux reading: an open face two Links behind an
   emitter body is the receiver `face`, last on every ladder, and the
   half that leaves through it reaches (2 u + 1) T / (2 W) before
   anything reaches a screen, so every record clicked at the face
   (test_detector_law.py test (a) reads that on the open chain: the first
   record's click at `face` within twelve intervals of its birth). THE
   FINDING FOR THE MATHEMATICIAN (the owner's method, values on the
   board; tests/test_detector_law.py, the layer test): under the
   cumulative rule AS WRITTEN, "the first interval at which some L_k
   reaches (2 u + 1) T / (2 W), at the first such k", the LAST sum L_K
   is the first to reach the rung whenever the cells receive together,
   and at that interval only the tail sums exceed it: on the layer's
   three sets all eight residues click at s2 under [s0, s1, s2] and all
   eight at s0 under [s2, s1, s0], no distribution over the cells; the
   same for a screen and for the polariser's two cells at one Node
   (the entry's whole offer reaches the rung no later than the + share
   of it), so Malus's counts cannot come from the table body under this
   rule and the four Malus worlds and tests d, d2 and d3 of
   tests/test_detector_law_tables.py are HELD until the polariser body
   with an axis (the mathematician's step 3). 9.22 (3) (b)'s derivation,
   "for offers in fixed proportions the crossing cell is the final
   ladder's", holds if the click's INTERVAL is read on the ladder's total
   L_K against T and the CELL on the ladder's proportions at that
   interval (main's `cell_of` with the total the ladder's own sum), two
   comparisons; the mathematician's word is owed and the engine carries
   the rule as written until it comes (no silent law change). The line's
   suites re-read on this engine: their numbers are the engine's,
   COMPUTATION; the property test green at every push of this item.

15. THE RESIDUE FROM THE LAW AND THE TAKE'S DATA GONE (ALGEBRA.md 9.22
   (4), 9.19 (4a) and 9.21 (8b) with the mathematician's answers of
   23:13Z; the cleanup order's step 2, its first push; the property test
   green). THE RESIDUE: no world declares a residue. At an excitation and
   at the click that births a record, the engine reads the clicking record's
   rule remainder r at the body's centre cell (`residue_of`): u = r / g in
   the remainder's step g = gcd(num x scale, wall), and the record's own
   wheel W = wall / g = 3 den / gcd(num, 3 den) values of the pair at that
   cell; the born record carries u and W (the birth line's `u` and `W`),
   the rung 2 W L_k >= (2 u + 1) T is read on the record's W everywhere
   (the ladder click, the excited record's rung, the gather line's rungs,
   the table body's split), and no set, block, world or emitter declares a
   wheel. THE RICHNESS: the loader refuses an emitter whose body's pair
   gives fewer than 500 remainder values, naming the count; every one-cell
   emitter moves to the well [801, 700] on the kind [7, 8] (700 values,
   the mathematician's confirmation: bound on a chain at 1.90193 and on a
   layer at 1.75218; on a cube a one-cell body does not bind and the
   emitter is a body of side 3, 9.21 (8b)), every emitting body of side 12
   to [800, 801] on [800, 809] (2403 values; [800, 800] gives 3 and is
   refused); the non-emitting wells keep [800, 800] until step 6. THE
   TAKE'S DATA REMOVED: `absorbing`, `take` (a block's and a family's),
   the take masks and their Ports, a record's `driven` and `port_motion`,
   a block's `taking`, `_form_take_masks`, the take's pair arrays; the
   loader refuses `absorbing`, `take`, `emits`, `own_grace`, `wheel`,
   `residue_order` and `residue_seed` BY NAME with the successor in the
   message (`RETIRED_KEYS`, `_refuse_retired`) on the world, a family, a
   measured event, an emitter and a detector set; `_neighbours` reads the
   six neighbours and nothing through a Port; a born record of a massive
   kind is told from a block's own record by its `emitter` (the `driven`
   mask retired). THE WORLDS regenerated on the rich wells without the
   keys (the two matter layer worlds lose their take lines at x = 0 and
   127: the open faces there are the receiver `face`); the Malus and Bell
   worlds held as before. TWO FINDINGS FOR THE MATHEMATICIAN (values on
   the board): (a) an excited record is the seed again after every click
   (9.17 (4)), so on a body WITHOUT a coupling to the light on the board
   its remainder at the centre cell repeats and every birth carries the
   same residue (the chain of 240: 214, 214, 214 on W = 700; the emitter's
   unit chain: one value over four births on W = 2403): a distribution of
   residues needs the body's coupling (the registered emitters carry G
   [1, 50], g [1, 1000]) or another body's field; (b) the excited record's
   own residue is 0 on a fresh seed (its remainder 0), so its rung is
   T / (2 W) and it clicks at the first interval with flux into the centre
   cell: the births come one per interval while the stock lasts. Retired
   tests: the order channel (test_detector_law.py), the world key `wheel`
   (test_massive_record.py ab, rewritten as the refusals by name), the
   silent take line (aj); the chain digests of (p) moved; every other
   suite rewritten onto the record's W (BUILD.md item 14's spy reads it).
   Left for the next push of step 2: no table in the engine (`born: [now,
   before]` from the generator, the cosine and sine tables and the phase
   imports retired with step 3's tables), `_source` and `_receive` (not in
   the order's list: the coupling stays until the mathematician's word),
   record 1886's LAWFUL / REFUSED input check and record 1887's one
   command (queued after the emitter line).

16. THE INCREMENT LADDER AND THE SAME INPUT (ALGEBRA.md 9.25, the
   mathematician's word of 2026-09-25 00:25Z on item 14's finding, at once
   on the Boss's order; the model owner's word through the Boss of 23:51Z
   and his proposal "a Node shouts by itself"; the property test green,
   10 of 10). THE RULE WITHDRAWN AND THE RULE IN FORCE: the cumulative
   sums of 9.19 (3) (b) are withdrawn ("your finding is right and the
   sentence was mine"); the click is THE INCREMENT LADDER (9.25 (2)): the
   record's threshold (2 u + 1) T / (2 W) is fixed at its birth; at every
   interval its running total C (`LiveRecord.total`) gains this interval's
   one-way flux into the cells of its ladder in the ladder's declared
   order (the named sets in the named order, the face last); the click
   fires at the first interval at which C crosses the threshold, at the
   cell whose segment of that interval's increment holds it (the walk of
   `_ladder_click`: the first cell k at which 2 W (C + f_1 + ... + f_k)
   >= (2 u + 1) T); the record deleted whole at that interval (record
   1888). Born's rule is its theorem (9.25 (3): a cell's share of the
   record's total inward flux, whatever the time profile); the owner's
   form, a Node shouting by itself, is exact only when the Node holds the
   record's two integers, the threshold and the running total, which is
   this walk read cell by cell (9.25 (3), the mathematician). THE DETECTOR
   IS ONE CONNECTED REGION (9.25 (7), the owner's word): the loader
   refuses a receiver on disconnected pieces naming their number
   (`_connected_pieces`, the Links across a periodic seam counted). THE
   TESTS: tests/test_detector_law.py plants 128 light records with every
   residue of the wheel 128 once on the layer and reads every click
   against the walk on the click's own numbers (a spy on
   `_ladder_click`), the counts per cell under [s0, s1, s2] against
   [s2, s1, s0] within the sampling and s0 against s2 alike (COMPUTATION:
   on eight residues the exact counts are (4, 2, 2) against (2, 2, 4), the
   first cell of the ladder holding more of the eight thresholds, so the
   mathematician's "the counts EQUAL" of 9.25 (8) holds in distribution,
   not per residue); the emitter's own births, all of one residue (item
   15), click at one cell under either order, the cell itself the
   order's; the connected-region refusals. THE SAME INPUT, THE SAME OUTPUT
   (the owner's word): test 8 of the property test runs the small world's
   input text twice and in two separate processes at once, byte-identical
   outputs (the input's hash, the click lines, the final state's digest);
   a one-unit change in the seed profile or in the planted row changes
   the output, never silently the same. The Malus and Bell worlds stay
   HELD: the increment ladder gives their counts once the residues are
   spread, and a one-cell emitter without a coupling births one residue
   (item 15's finding (a)), so their unhold waits on the mathematician's
   word on the excited record's residue. Also taken from the notices of
   this hour: record 1884 (no ramp; the `ramp` key's refusal goes to the
   loader's checks of step 5 with record 1886's LAWFUL / REFUSED), record
   1885 (every entry carries its K; a region does not move), record 1889
   (the moving name, for the line after the cleanup), record 1890 (the
   joint body dropped: the sixteenth's circuit is the generator's), the
   seventeenth (Mach-Zehnder, after the mathematician's pin and the
   generator). THE GATE'S READING OF 2bd20b8c (the mathematician, 00:31Z:
   NOT YET, two lines blocking, the rest CONFIRMED in form) folded here:
   item 1, the withdrawn ladder, is the increment ladder above; item 2,
   `_flux_ports` forms a Port only where the neighbour is a Node of no set
   or of ANOTHER set (a Link between two cells of one set, a table body's
   two cells, is no Port: the energy that entered the set at one cell is
   not offered again at its neighbour; one-cell sets unchanged); item 3,
   the two docstrings that said "the levels that enter the step" now say
   after the step; item 8, the next excitation's flat-seed fallback is
   gone and a body that births needs its seed as the composed mode's
   profile (refused at the engine's construction, where `_excite` runs,
   since the generator parses the world with the scalar seed to compute
   the profile; the line's test worlds declare `margin` so the generator
   writes their profiles); item 10's note on INTERVALS' comment (the
   prototype's factor of 3 fixed: the two agree). Items 5 and 9 (the
   branch on the kind, `live.mask`, `arm_done`, the cavity's zeroing, the
   tables) are the later steps'.

17. NO TABLE IN THE ENGINE AND THE TABLES RETIRED (the cleanup order's
   step 2, second push, and step 3; ALGEBRA.md 9.17 (6), 9.21, 9.22 (2);
   the property test green, 10 of 10). THE BORN PAIR: the emitter's
   `born` is the world's two integers [now, before] on every cell of the
   body, the generator's (now = A C_2N[3 N / 2 + s] on the host's table
   cos x 256, s the born clock's step, before = -now), checked at load in
   integers (two integers, before = -now, a motion) and required at the
   engine's construction where a body births; `_emit` writes them, no
   cosine or sine table in the engine (`_cosine_table`, `_sine_table` and
   the phase imports gone), the loader's S[k] check gone with the
   splitter. THE TABLES RETIRED: `TableBody`, `Splitter`,
   `_table_settings`, `_table_body`, `channel_weights`,
   `_split_table_offers`, `read_pair`, `_split`, `joint_weights`, the pair
   bodies, the splitter mask and the record's table shares removed; a
   measured event with a table entry (a polariser's window, a splitter's
   rows) is refused at the engine's construction naming the successor (a
   polariser is a body with an axis and two receivers named, a splitter a
   region of the one operator; the loader still parses the ray law's
   tables). THE PHASE READING is a host reader (core.phase.nearest_phase;
   the engine's `read_phase` gone), its test in tests/test_detector_law_tables.py
   alone: the splitter's (c), the joint weights' (g, d4) and the tables'
   rotation (test_massive_record.py af) retired with the code. The worlds
   regenerated with `born`. THE FINDING ON THE WRITE (for the
   mathematician): 9.17 (6)'s whole step s = floor(n / d) is 0 for a born
   clock below one step per interval (the index rows' light [3565, 10000],
   [1846, 10000], [2243, 10000] on N = 64), so the write's pair was A
   C_2N[3 N / 2] = 0 at both levels and those worlds' births wrote NO
   MOTION since item 13 (the loader's new check exposed it: "born writes
   no motion"); the generator now writes the character half a step either
   side of its zero on the clock's own advance, now = round(A sin(pi n /
   (d N))), before = -now (157930 on [77, 25] at N = 64 against the
   table's 155648 of the whole step 3; a HOST computation, the integer in
   the file the input), and the engine reads the integers alone; his
   word on the form is owed, the file's integer carries it either way.
   The Malus and Bell worlds stay held (the polariser body and the
   crystal, and the excited record's residue).
18. THE DETECTOR CUBE (the model owner's decisions of 2026-09-25, record
   1899, through the Boss; ALGEBRA.md 9.25; the property test green). THE
   RULE: a detector is one region, a cube of side 3 or more; its
   sensitivity is its whole cube, read as the one-way flux into the cube
   through its Ports from outside (9.25 (2); a Link inside the cube is no
   Port, item 16); the click is the detector's, reported by its name on
   the click line and never placed at a Node (the detector does not know
   which Node inside it clicked); the ladder lays the detectors'
   increments in the declared order. THE ENGINE AS BUILT already reads a
   set as ONE cell over all its Nodes (`cell_index` maps every Node of
   the set to the set's cell, `flux_offer` books the set's Ports to that
   cell, `_ladder_click` walks the cells, the line's `chosen` names the
   set and `node` is empty), so nothing moved in the click's code; the
   docstrings say it. THE LOADER (`_detector_region` in world.py, with
   `_box_sides`): a detector's Nodes must be one connected piece (9.25
   (7)), fill one box (per axis one run of coordinates, across a periodic
   seam too, the count the runs' product), and the box's sides must be
   `DETECTOR_SIDE` = 3 or more, cut by the GameBoard on an axis whose
   extent is below 3 (a chain's or a layer's thin axis: the cube of side
   3 on a chain is three Nodes in a row, as a block's cube is cut by an
   open face; the thin-axis reading is Nature's, the chain and layer
   reading being with the mathematician); the refusals name the sides,
   the Node count that fills no box, or the pieces. A set bound to a block
   is the block's cells (its side 3 or more, refused below) or a cube of
   free Nodes beside it under `positions` (the one-Node form retired).
   THE TESTS (test_detector_law.py, the cube test): a 2 x 2 box on the
   layer REFUSED naming its sides [2, 2, 1]; a 3 x 3 box LAWFUL (the
   layer's thin z cuts it to one deep), also wrapped across the periodic
   seam; two bodies three Links apart REFUSED naming 2 pieces; the 3 x 3
   box less its centre REFUSED as filling no box; a block of side 1 as a
   bound set REFUSED, of side 3 admitted; the engine's cell over the
   cube's Nodes exactly. THE WORLDS AND THE LINE'S TEST WORLDS on cube
   detectors: the two slits' screen a row of 67 cubes of side 3 (x in
   [153, 155], y in [28, 228]); the matter waves' screen 41 cubes over y
   in [3, 125]; the matter front, the redshift's light detector (the cube
   at [4092, 4094], the +x face at 4095 beyond it) and the light clock's
   `at_a` (the cube of free Nodes at [612, 614] bound to A) cubes cut by
   the chain; the Sagnac sets the blocks' cells of side 12 unchanged;
   every test world's one-Node receiver a cube of three on its chain, the
   layer test on 24 x 9 with three 3 x 3 cubes at x in [18, 20] on the
   rows [0, 2], [3, 5], [6, 8] (s1 centred on the emitter's row y = 4);
   the property test's receiver the cube of side 3 at (9, 9, 2), rotated
   as the well is. THE MALUS FOUR stand held as written at ead580df (the
   generator no longer rewrites them: their one-Node set `second` on the
   bar of 8 is refused by the cube, and the polariser returns as a body
   with an axis and two cube receivers at the worlds' rebuild, step 6);
   the Bell four held as before. The chain digests of test p moved by the
   cube at x in [70, 72] (COMPUTATION, read on this head).
19. THE EMITTER'S COUPLING AND THE RESIDUE'S READ POINT (the mathematician's
   answers of 2026-09-25, ALGEBRA.md 9.19 (4e), to item 15's two findings;
   the property test green). (a) EVERY EMITTING BODY DECLARES (g, G) FOR
   ITS BORN FAMILY, both nonzero, refused absent at load naming the key
   (the one-cell emitters [801, 700] included, the registered form G [1,
   50], g [1, 1000]): the born records act back on the excited record's
   rows through g (`step` drives a body's own record by its emitted
   records' first differences; a one-unit change of a row moves the next
   remainder by num mod 3 den), so the remainder at the centre cell moves
   between births and the residues spread; a body that births and is not
   coupled is a write and no source. The body's G acts on every other
   record's light and not on the light it births ("a body answers no
   record of its own", as built): whether G must act on its own born
   light too is asked of the mathematician; g alone is built. (b) THE
   EXCITED RECORD'S RESIDUE IS READ AFTER ITS FIRST ADVANCE: `_excite`
   marks the residue pending (`Block.residue_pending`), and the first
   `_excitation_rung` after the (re)seed reads u and W from the record's
   own remainder at the centre cell (nonzero after one step of the rule;
   0 at the write) and counts the offer C from that interval; the born
   photon's residue stays the excited record's remainder at the click.
   The first excitation of a run then carries the residue the generator's
   seed gives after one step, the same in every run of that world; every
   later one differs by the back-action of (a). THE TESTS: test_emitter's
   (a) reads the residues of four births no longer one (item 15's finding
   resolved) and the loader's refusal of an emitter without its coupling;
   the layer test reads eight births' residues spread and the same eight
   under the reversed order (the residues the excited record's, the
   ladder's order no input to them), an emitter without coupling and one
   with g = 0 refused; the chain world's flight bound widened to 200 (a
   residue near W waits for the whole front). The worlds regenerated with
   the coupling on every emitting body (the index rows, the pace fans, the
   two slits, the matter rows). THE 100-BIRTH READING owed to the
   mathematician (COMPUTATION on this head, the emitter world of
   test_emitter [800, 801] with the seed 100 and the stock 100, and the
   chain world of test_detector_law [801, 700] with the stock 100): the
   residues SPREAD, 97 distinct of 100 on W = 2403 with the ten-bin counts
   [6, 7, 8, 9, 12, 9, 11, 11, 14, 13] (chi-square 6.20 on 9 degrees of
   freedom), 93 distinct of 100 on W = 700 with [12, 10, 9, 16, 9, 14, 4,
   6, 11, 9] (11.20); the first excitation's residue the same in every
   run (1165 on the emitter world, 360 on the chain). TWO READINGS FOR
   HIM: (i) THE CADENCE is a few intervals, not (2 u + 1) P / (2 W): the
   flux into the centre cell after the standing start (now = before =
   the profile) is front-loaded, 0.2 to 0.4 of the norm T in the first
   interval on the seed 50 x 2^20 body of the chain of 200, so most
   residues click within one to ten intervals of their read (the gaps 1 to
   10, the mean about 4); (ii) on the test worlds seeded at the amplitude
   100 the born light (the world's `born` about 1.6 x 10^5 on the body's
   cells) times g = 1 / 1000 is about 158 per cell per interval, above the
   excited record's own amplitude, so the back-action swamps the excited
   record (the offer at the click up to 230 times the norm, the births
   one per interval on the chain world): the spread is the coupling's,
   the cadence the amplitude ratio's; the registered bodies at 50 x 2^20
   are not swamped (the offer at the click 0.2 to 0.7 of the norm). The
   pins are not moved; the rule stands as written until his word.
20. THE INPUT CHECKED LAWFUL OR REFUSED, IN INTEGERS (the model owner's
   record 1886 of 2026-09-25; ALGEBRA.md 9.22 (3) and (7); the property
   test green). THE FORM: the initial state is stored once in the world
   file, every seeded body's integer profile at both levels (`seed` as the
   list, as before) and NOW ITS MODE'S CLOCK `clock` [a, b], the
   generator's rational for 2 cos omega (b a power of two at least twice
   the amplitude and at least 2^20, so that a shallow mode's binding above
   the band's top is resolved; a the nearest integer to lambda b),
   required beside a profile and refused beside a scalar seed. THE LOADER
   (`_initial_state_checks` in world.py, after the measured events are
   parsed, in Python integers with no float and no numpy: the loader
   carries none): (a) every block's cells disjoint from every other
   block's (9.9 (4); a cube beyond a face or wrapped onto itself stays the
   fit check's refusal, naming the axis and the vertex); (b) the clock
   a / b strictly above the family's band top 2
   num / den (else "no bound mode") and below 2 (else "a runaway"), the
   rational comparisons a den > 2 num b and a < 2 b; (c) THE
   EIGEN-EQUATION'S RESIDUAL at every Node, abs(b num_i (S_6 p)_i - 3
   den_i a p_i) <= b (3 num_i + 6 den_i), the mathematician's proved bound
   for the rounded profile of an exact mode (`mode_residual`,
   `six_neighbours_flat`, `block_cell_indices`; the one copy of the cube's
   rule, the margin module's array form built from it), on the COMPOSED
   operator of the body's family (every body of the family in place),
   read at every Node outside the OTHER bodies of the family: NATURE'S
   READING, for the mathematician's word: at another body's cells the
   composed operator carries that body's summand, so those Nodes are its
   check and not this one's (a body's own mode in place); with every Node
   counted the two Sagnac wells' profiles (each the mode of its body alone
   in the medium, as the generator writes them) fail the bound at the
   other well's cells by about three times (the tunnel tail 10^-5 of the
   amplitude there), and the composed operator's exact top mode is the
   symmetric hybrid of both wells, which is no summand of one body (9.9
   (3)); (d) at most three families (record 1875), the fourth refused
   naming the count. What the check does not do: single out the mode among
   near-degenerate ones (the hybrid share stays the generator's), check a
   moving body's summand (the moving rows return as packets with the
   generator, record 1884), read a file's hash or the law it was made
   under (the input file's form of the integer generator, next); the
   `ramp` key's refusal waits for the moving rows' regeneration, by record
   1884's own words ("retires with the rows' regeneration"). THE FINDING
   THE CHECK MADE AT ONCE (COMPUTATION on the registered worlds at
   fd1734c2): the profiles the generator had written were NOT the modes to
   within their rounding: the three-term Lanczos recurrence without
   reorthogonalisation (`lanczos`, RITZ_TOLERANCE 10^-9) gave the vector to
   about 3 x 10^-4 relative, so the residual exceeded the bound by 6 to 12
   times on the 2^20 worlds (the boxes, the deep well, the layer pin,
   14758 Nodes above the bound on the layer) and by 640 to 860 times on
   the 50 x 2^20 chains (the light clock, Sagnac, the redshift), the
   stored integers off the accurate mode by up to 16349 units at 50 x
   2^20 and 888 at 2^20; the small worlds at the amplitude 100 and 4096
   passed. THE GENERATOR NOW (`accurate_mode` in the margin module): the
   largest eigenpair of the symmetric operator A = D^-1/2 (S_6 / 3)
   D^-1/2 by the implicitly restarted Lanczos method, ARPACK through
   scipy's `eigsh` at the machine's tolerance (scipy a declared
   dependency since this item, used by the diagnostics and the generator
   alone, never by the engine), the start the cells' indicator plus a flat
   10^-3; the profile rounded at the amplitude passes the bound with
   margin (the worst residual 0.18 to 0.53 of the bound on the four large
   worlds probed); `mode_profile` checks its own output through the
   loader's `mode_residual` before writing (a failing mode is raised, never
   written) and writes the clock; every world regenerated (the profiles
   moved by the accuracy). The integer power iteration of record 1898
   (3 den v' = num S_6(v) + 6 den v, the remainder kept, the power-of-two
   shift) is the generator's reproducible form owed with the input file;
   its cost per e-fold is (lambda + 2) / gap board steps (the
   mathematician's 15700 for the muon's form), so the float ARPACK start
   stays the host shortcut and the integer check the gate. A ONE-UNIT
   CHANGE at one Node is within the bound (the rounding it allows) and is
   ADMITTED: the check refuses a profile off the mode by the amplitude's
   order (the peak doubled or zeroed), not a unit; the same input then
   gives another output (the property test's test 8). THE TESTS
   (tests/test_initial_state.py): a generated world lawful with its
   clock; the peak doubled and the peak zeroed refused naming the Node,
   the residual and the bound, one unit off admitted; the clock's
   refusals by name (absent, malformed, b below the amplitude, at the
   band's top, at 2, beside a scalar seed); three families admitted and a
   fourth refused; two bodies overlapping refused, a cube beyond a face
   refused by the fit check, a whole one admitted; the six-neighbour read
   on a chain of three, open and folded. THE CART HELD: the cart worlds
   of the moving detector carry four families (post, source, cart, mass)
   and are refused by the count; RUN_LIST.md row 4c holds the cart until
   its rebuild as a transponder with three families (step 6), the file
   kept on disk as history.
21. THE INPUT STAMP, THE INTEGER GENERATOR AND THE ONE COMMAND (the model
   owner's records 1886, 1898 and 1887; ALGEBRA.md 9.22 (7); the property
   test green). THE STAMP (9.22 (7) (i)): every world with a seeded body
   carries `input` {law, hash}: the law identifier this loader runs under
   (`LAW_IDENTIFIER`, moved by a change of the laws that moves the
   initial state, forcing the files' regeneration) and the SHA-256 of the
   canonical JSON of the shape and, per seeded body, its number, its
   profile, its clock and its born pair (`input_stamp` on the raw
   document, the same digest from the parsed integers at load); the loader
   refuses a seeded world without the stamp naming the key, a stamp under
   another law naming both, and a hash that is not the digest of the
   integers loaded ("not the ones the generator wrote"); a world with no
   profile needs none. The generator writes the stamp last of all and
   before every parse of a document under construction (`stamped`); the
   tests' builders and refusal tests restamp a changed document so that
   the named refusal speaks and not the hash's. THE INTEGER GENERATOR
   (record 1898; `integer_mode_iteration` in the margin module): the power
   iteration 3 den v' = num S_6(v) + 6 den v + r with the remainder kept,
   renormalised by an exact power-of-two shift when the levels pass twice
   the amplitude, the remainder shifted with the levels (nothing of the
   fraction dropped but the bits below the wall); bit for bit reproducible
   (test h: two runs the same integers). ITS FLOOR (COMPUTATION on the
   emitter world's chain of 80, the well [800, 801] in [800, 809], the
   amplitude 2^20): from the cells' indicator it reaches ARPACK's mode
   within 78 units and stays there from 4000 to 16000 iterations: every
   step's rounding feeds the next mode and is damped only by the gap
   (0.0105 in lambda here), so the iterate carries an admixture of about
   1 / gap units at the amplitude; the float power iteration agrees with
   ARPACK to the unit, and the loader's bound accepts both (an admixture
   of the next mode moves the residual by the gap times the admixture,
   within the bound; the mathematician's own note that (ii) does not
   single out near-degenerate modes). So the ARPACK profile is what the
   generator writes and the integer iteration is the reproducible check
   of the same law, not the writer; the mathematician has the numbers.
   THE ONE COMMAND (record 1887; tools/run_inputs.py; tests/test_run_inputs.py):
   input files in, one output file per experiment out, each input in its
   own process (a spawned process pool, at most `--jobs` at once), each
   first LAWFUL or REFUSED at load with the reason (the loader's checks),
   the lawful one run under the law for its ticks, headless, and
   `<name>.output.json` written with the input's name and stamp, the
   verdict, the ticks, the click lines (DETECTOR: the detector's name and
   the interval), the count per detector, the records alive at the end
   and, where `--pins` registers a blind pin for the input before the run
   ({name: [{detector, count, band}]}), MATCH within the band or MISS
   with the count read; no time in the output, so two inputs run together
   give the files of each alone byte for byte (test a); a refused input's
   output carries the reason and the command exits 1 (test b). The pins
   of the seventeen enter that file as the mathematician's table completes
   per experiment; the short experiment file of 9.22 (5), the generator
   reading it and deriving the rest, is the next form, with his table.
22. THE FIRST INPUT FILE OF THE TABLE RUN BY THE ONE COMMAND, AND ITS
   FINDING (the mathematician's table of the eighteen, ALGEBRA.md 9.22
   (8), row 13; the owner's record 1887). THE LIGHT CLOCK IN THE TABLE'S
   FORM: the chain [674, 1, 1] with the face receivers, the well A [800,
   801] of side 12 at [600, 612) with its coupling and its stock, the
   MIRROR the gap [1, 2] of depth 2 at [672, 674) as a material of light's
   kind (A.3; the closed face of the chain of 673 HISTORY), the receiving
   set at_a the cube [612, 614] beside A; its blind pin registered in
   examples/events/pins.json (the one command's pins file, a pin on the
   COUNT of clicks or on the interval of a detector's FIRST CLICK,
   `first_click`, written before the run): at_a's first click 214 +- 1
   (the table's 211.98 plus the rung's offset). THE RUN (COMPUTATION,
   `tools/run_inputs.py --pins examples/events/pins.json`, 0.4 s): LAWFUL;
   64 births, 64 clicks at at_a, the first at interval 76, 21 intervals
   after the first birth: MISS. No pin moved. THE FAULT FOUND, for the
   mathematician: every one of the 64 records clicks within 150 intervals
   of its birth, whatever its residue (u / W from 0.01 to 0.98), on the
   OUTGOING pass and never on the return from the mirror, because the
   one-way flux the receiver books is not bounded by the record's energy
   for the born pulse as written. Measured on one born record kept from
   clicking (its norm set beyond reach): the adjacent cube [612, 614]
   books 1.31 I within 50 intervals of the birth, 2.57 I by 100, 4.65 I by
   400 and then nothing more; A's own cell 4.23 I; a cube placed 30 Links
   away, [640, 642], books 2.61 I over the outgoing pass and the return
   (two passages of the +x half, whose energy is I / 2 each: the booking
   2.6 times the energy passing); the record's conserved form I unchanged
   throughout; a SMOOTH planted packet (test b of the flux reading) books
   1.0017 of its I on a passage. So the born pair's form of 9.17 (6), one
   pair [now, before] on every cell of the body (a flat box of 12 cells
   with the slow clock's half step), is a broadband DISPERSIVE pulse: its
   components run at every pace of the band and interfere, the local
   current changes sign, and the positive part the ladder books (9.19
   (3)) exceeds the energy several times, most at the emitter's own face
   (the standing components' sloshing across the Link 611 | 612). The
   increment ladder is then met by sloshing, not by the record's passage,
   and no rung read at a receiver beside an emitter, nor a first rung on
   a chain, means what the table's pins mean (the light clock's 214,
   Sagnac's 108 and its ratio, the redshift's ratio, the moving mass's
   169). THE REMEDY IS THE MATHEMATICIAN'S OWN FOR THE LAYERS, now for
   every emitting row: the born profile as a TRAVELLING character over
   several periods with an envelope (the travelling born profile of the build order, 9.22 (3):
   the profile times the character of K at the two levels), for which the
   one-way flux is the energy passing to a part in a thousand; the
   one-pair form stays as the write of a body that births nothing lawful
   to read. Nothing in the engine changed here; his word on the form and
   the pins before the rest rows' files are written.
23. BODIES WITH EXTENTS AND THE FACE SLAB (two items of the build order
   the Boss approved on 03:18Z; ALGEBRA.md 9.22 (8) and 9.25 (10); the
   property test green). BODIES WITH EXTENTS: a block is the box of `extents` [x, y, z]
   per axis; `side` stays the cube's shorthand (the extents three times;
   one of the two keys, both refused); the loader's fit check reads the
   side per axis, the bound set's cube check the extents against min(3,
   the extent) per axis; the engine's `_box` (the `_cube` renamed) forms
   the cells and the centre cell from the extents (the corner plus the
   extent // 2 per axis), the readings carry `extents` beside `side`; the
   margin module's per-axis margins read the extent on that axis, the
   accurate mode and the profile check the box's cells; the generator's
   seeding admits `extents`; `block_cell_indices` and `block_cells` take
   a side or the extents (the one copy of the box's rule). THE FACE SLAB: the world
   key `face_depth` (1 by default): the face receiver at every open
   border is the slab of that many free Nodes nearest the border, ONE
   cell `face`, last on every ladder, its Ports toward the interior alone
   (a Link inside the slab no offer, no Node beyond the border); a depth
   above one whose two slabs leave no interior on an open axis is refused
   (the depth of one is the law before the slab, lawful on a board of
   extent 2, whose two Nodes are both face). THE
   TESTS (tests/test_extents_and_face_slab.py): a wall slab [4, 3, 1] on
   the layer placed whole with its 12 cells, the indices of a side and of
   equal extents the same; both keys refused, malformed extents refused,
   a box beyond a face refused per axis naming its side there, a box
   wider than a periodic axis refused, a bound slab [12, 1, 1] on a chain
   admitted as a cut cube and [2, 1, 1] refused naming the extents; a
   slab well [12, 5, 1] seeded on its composed mode with its clock and
   stamp LAWFUL, its peak on the slab, its centre cell the box's; the face
   slab's Nodes at depth 4 on the chain of 80 (0 to 3 and 76 to 79), the
   default's 2, a depth of 40 refused, none on a periodic axis; the
   mathematician's reading of 9.25 (10) read on the board (COMPUTATION):
   a Gaussian packet of width 14 at k = 0.3 leaving light's open chain of
   300 books more than 0.9 of its I into a face slab of depth 40 and less
   than 0.5 into a face one Node deep (the rest reflected). No world
   changed; the travelling born profile waits for the mathematician's form.

24. THE CLICK RULE OF ALGEBRA.md 9.17 (7) (f) IN THE ENGINE (the model
   owner's word, record 1918, through the Boss's closing list of 03:38Z,
   step 2). ONE FORM, ONE RUNG, TWO READINGS: every record clicks once,
   at the first interval at which its running total C reaches (2 u + 1)
   T / (2 W), and C accrues each interval the share of the record's
   conserved form its named set acquires: through the set's Ports from
   outside where the record moves (the one-way flux, the detector's pace,
   unchanged), and at the set's own cell where the record stands (its
   share e_c, the record's own tick, the emitter's pace). THE ENGINE:
   `form_share(live, mask)` the Nodes' share e_i = 3 wall (den_i / num_i)
   (now_i^2 + before_i^2) - wall now_i (A before)_i in the flux's units
   (`conserved_form` its sum over the board); `_excitation_rung` accrues
   the share at the body's centre cell in place of the one-way flux there
   (a bound mode has no flux to read, 9.17 (7) (a)); the rung, the
   residue's read point after the first advance and the coupling of 9.19
   (4e) unchanged. THE NORM T is one period's action P e_c: the emitter's
   `norm`, the generator's integer (`excitation_norm`: the share at the
   centre cell summed over `period` intervals of the mode advanced alone),
   under the input stamp; quadratic in the levels times the wall, it
   passes 2^62 at 50 x 2^20, so the loader admits it up to 2^126
   (`NORM_BOUND`; the engine's form and running total are exact Python
   integers). THE SEEDS: the born light's back-action at g = 1 / 1000 on
   the amplitude unit 2^20 swamps an excited record seeded at 100 (9.17
   (7) (c): 158 per cell per interval against 100; the seed-100 test
   bodies and the generators' emitter bodies of the index rows, the pace
   fans, the two slits and the matter rows), so every emitter body is
   seeded at 2^20 (the light clock, Sagnac and the redshift stay at 50 x
   2^20); the load condition of 9.17 (7) (c) is NOT a refusal here (the
   owner's word adopted (f); (c) stays derived). THE READINGS
   (COMPUTATION, on the emitter world of test_emitter at 2^20, the well
   [800, 801], P = 63, W = 2403): the share at the centre cell of the
   mode alone is constant within 4 x 10^-4 (26508721610111 to
   26519140807927 over a period), one period's sum the next period's
   within 7 x 10^-6; the six births' waits after their reads 22, 15, 29,
   10, 29, 21 intervals against (2 u + 1) P / (2 W) = 23.95, 15.11,
   29.74, 10.08, 29.04, 22.11 (the residues 913, 576, 1134, 384, 1107,
   843): the uniform waiting time in [0, P) of 9.17 (7) (b), within two
   intervals; at the seed 100 the same world births at 6, 7, 8, 9, 10, 11
   with the share wobbling from -18961 to 555039 (the rounding of a
   profile of 100 against a share of 3 percent of its square) and the
   offers growing a hundredfold at every reseed (the swamping). THE TESTS:
   test_emitter's births test reads the norm as the share's sum bit for bit, the
   board's shares summing to the conserved form, the share's wobble below
   one part in a thousand, and every birth's wait within two intervals of
   (2 u + 1) P / (2 W); test_massive_record's matter emitter test admits the two matter
   records' clicks in either order (the second born (2 u + 1) P / (2 W)
   after the first's click); the chain digests' events and audit moved
   once (the state at 600 unchanged). THE LIGHT CLOCK by the one command
   on this head (DETECTOR, examples/events/massive_record/light_clock_60
   .json against pins.json): LAWFUL, 64 clicks at `at_a` over 2600
   intervals, the first at 51 against the pin 214 +- 1: MISS, a fault to
   find, the pin unmoved (the born pulse is still the one-cell broadband
   birth of item 17; the travelling born profile is the remedy in
   the build order). Every world with an emitter regenerated (the norm
   and the seeds); the Malus four held as written.

25. THE GENERATOR AS THE BOARD'S OWN OPERATOR ITERATED, WITH THE STOP (the
   model owner's word of 2026-09-25, 04:10Z, in Nature's session, closing
   record 1898: "the iterated operator must become the generator itself,
   with the stop"; and his rule of the same minute: no more letter-and-
   number codes in any artifact or message, every thing named by what it
   is, the Boss to review the code's names). THE GENERATOR
   (`iterated_mode` in the margin module, called by the massive record
   generator's `mode_profile` and by every seeded test world): the block
   alone in its medium on the world's own board, from the cells'
   indicator at the amplitude; every iteration one step of the law's own
   operator 3 den v' = num S_6(v) + 6 den v + r with the remainder
   carried and the levels renormalised by an exact power-of-two shift
   (`_operator_step`, the one copy of the step; the fixed-count
   `integer_mode_iteration` is its diagnostic); the levels scaled to the
   amplitude at the peak; the clock a / b read from the scaled profile p
   as the operator's quotient over the whole board, a = round(b SUM_i p_i
   num_i (S_6 p)_i / SUM_i 3 den_i p_i^2), b the power of two at least
   twice the amplitude and at least 2^20 (`clock_denominator`; exact for
   the mode, second order in the rounding, every Node weighing in; the
   growth at the peak cell alone READ AND REJECTED: its remainder's noise
   at the amplitude 4096 moved the read by 2 x 10^-4, more than the
   property test's shallow well is bound above the band's top, 9 x 10^-5,
   and the loader refused the clock as no bound mode); THE STOP the first
   iteration at which
   that scaled profile with that clock passes the loader's own residual
   bound (`mode_residual`, the same function the loader runs on the
   file): the next step changes the board no more than the rounding
   floor, the board only rotating. Reproducible bit for bit; a limit
   (2^20 iterations) past which the generator refuses naming the last
   residual against the bound (the iteration's floor or a fault, never a
   bound moved). The host's eigensolver (`accurate_mode`, ARPACK) is no
   longer the generator: it stays a diagnostic (the margin readings'
   extent, and the cross-check of test_initial_state's generator test); `mode_clock`
   retired. THE READINGS (COMPUTATION, the emitter world's chain of 80,
   the well [800, 801]): the stop after 1817 iterations at 2^20 and 3204
   at 50 x 2^20 (0.1 and 0.2 seconds); the clock 8346518 / 2^22 and
   267088580 / 2^27, the same integers as ARPACK's rounded 2 cos omega
   (the peak's read gave 8346516 and 267088578); the profile
   within 193 and 215 units of ARPACK's rounded mode (the iteration's
   floor near 1 / gap units); the same integers on a second run; the
   128 x 128 layer pin world stops after 33822 iterations (21 seconds; a
   small gap) with its profile 3497 units from ARPACK's, within the
   loader's bound, which admits about 3 / gap units of the neighbouring
   mode (the bound is the law's check; the deviation a diagnostic). A stop by "the scaled
   profile changes by at most one unit for two successive iterations"
   was READ AND REJECTED: it fires at 1544 iterations with the residual
   twice the bound and the profile 370 units off (the creep below one
   unit per iteration accumulates; the rounding floor is the loader's
   bound, not a unit). THE WORKING AMPLITUDE: the iteration runs at 2^20
   or the declared amplitude, whichever is larger, and writes the
   rounding of the converged profile at the declared amplitude: the
   loader's bound is the bound for ONE rounding of an exact mode, while
   the iteration's own noise (a unit per Node per step through the six
   reads) sits below it only when the working amplitude is large against
   the bound's relative width 1.5 / p (READ: a side-4 well of [850, 800]
   on the 24-cube iterated at 4096 hovered at 1.2 to 1.7 times the bound
   at the well's cells for 20000 iterations, its clock converged; at the
   working amplitude 2^20 it stops). AMENDED AT THE NAMES' REGENERATION
   (2026-09-25, 06:50Z): the muon layer's well [3200, 3227] of side 14 on
   the 200 x 200 layer hovered at 1.5 times the bound at 2^20 for 2^20
   iterations (30 minutes, nothing written: the committed generator could
   not reproduce the muon files it had written from an earlier state of
   the iteration, a defect of this item's commit found by the
   regeneration under the names), and stops at 36694 iterations
   at 2^28 (COMPUTATION, the probe of the residual against the bound at
   both amplitudes); THE WORKING AMPLITUDE IS 2^28 SINCE (the same rule,
   one number moved; the deep well's layer, 50003 iterations at 2^20 by
   the noise's dip, stops at 2746 there), every seeded world regenerated
   again under it (the
   emitter chain's profile 204 units from the eigensolver's and its clock
   exact at 1653 iterations; the chain digests moved with the profiles;
   the HOST cost of the regeneration about four minutes for both
   generators, against the 31 of the hovering muon; the profiles moved by
   the floor, COMPUTATION: the muon's by 1650 units and its clock by 16
   units of 2^22, the redshift's chain by 380, the fringe layers' by 303
   to 313, the light clock's by 90, Sagnac's by 87, the boxed and the deep
   wells' by at most 49 and their clocks by at most 9 units, the index
   chains' by at most 5). TWO FINDINGS ON THE 3D WELLS
   (COMPUTATION): (i) the property test's small world's body, the side-2
   cube [800, 801] in [800, 809], is bound by its torus, not by its well:
   2 cos omega above the band's top by 9.4 x 10^-5 on the 12-cube, 4.7 x
   10^-5 on the 24-cube and 1.5 x 10^-6 on the 48-cube (the eigensolver's
   readings; a side-2 well of any of the pairs [800, 800] to [900, 800]
   binds by less than 4 x 10^-5 on the 48-cube: a shallow cube in three
   dimensions binds only above a critical depth); on the 48-cube the
   iteration stops on a mixture of the band's modes whose quotient reads
   below the top and the loader refuses the world as no bound mode (the
   eigensolver passed it by 1.6 units of 2^20 before); so the host-cost
   scaling worlds of the property test (12, 24, 48) take a side-4 well of
   [850, 800], bound by 2.9 x 10^-3 on the 24-cube; the gate's 12-cube
   world itself is unchanged (a finding for the mathematician, not a
   change of his world). (ii) The loader's residual bound admits about
   3 / gap units of the neighbouring mode, so on a small gap the
   generator's profile can sit thousands of units from the eigensolver's
   while lawful (the layer's 3497). Every seeded world regenerated (the
   profiles and clocks move by the floor; the digests of
   the chain digests test of test_massive_record with them); no registered world sits below
   2^20 (the four held Malus worlds at 100 stay held as written). HOST
   cost of the regeneration: about 31 minutes for the massive record
   generator's eight chain worlds at 50 x 2^20 and one minute for the
   detector-law generator's thirty-six. THE TESTS: test_initial_state's generator test the stop, the reproduction,
   the residual passed, the agreement with ARPACK within 300 units and 4
   clock units, the fixed-count iteration within the same, and a limit
   below the stop refused by name; test_body_conditions seeds by the
   generator.

26. THE CLICK'S COST: THE DETECTORS' INFLOW READ AT THE PORTS ALONE (the
   model owner's record 1934, through the Boss's 05:32Z: "how we do it
   without starting to count all the shapes on the board"; no new law).
   THE RULE, unchanged: per record and per interval the click reads only
   the one-way flux through the detectors' Ports, sums it per cell in
   the ladder's declared order onto the record's own tally and compares
   once with its threshold; nothing of the board's shapes is counted.
   THE CODE BEFORE: the flux was computed by whole-board array shifts
   per record per interval (six shifted copies of the record's two
   levels over every Node, object arrays), so the HOST cost was the
   board's Nodes times the records. NOW: `_inflow_ports(family)` lists
   the Port pairs ONCE per family on first use (the flat index of every
   Port Node, of its neighbour across the Link on the family's faces,
   and the cell of the Port), and `detector_inflow_tally(live)` reads
   the record's two levels at those pairs alone, one gather per pair in
   exact Python integers, the positive part per Port summed per cell
   times the wall: the same integers as the board-wide reading bit for
   bit (`inward_flux` per cell stays as the board-wide reference of the
   tests). The board-wide `flux_offer` is retired. WHAT IS NOT CLAIMED:
   the record's two levels are still board arrays and the advance is the
   board's cost; reading only the Ports a record's rows currently touch
   needs the record's bounding box, which the advance does not keep. THE
   READING (HOST, tests/test_flux_reading.py): on the emitter chain of 80
   with the cube screen 4 Ports against 80 Nodes (the screen cube's two
   and the emitter body's two); on the detector-law layer of 24 x 9 with
   three cubes 40 Ports against 216 Nodes; the two
   slits' restated placement (about 1800 Ports of 97600 Nodes) reported
   when the born train lands. THE TEST: after every interval of a run on
   both worlds the tally per cell equals the board-wide reading for every
   live record, the pairs are listed once, the cost printed.

27. THE BORN TRAIN, THE ONE FORM OF A BIRTH (ALGEBRA.md 9.17 (6a), 9.25
   (11), 9.22 (7a) (iv), the mathematician's 85780fba and 9ffc0fb2 on the
   physicist's finding at f0d2d745; the Boss's closing list item 3; the
   model owner's word that the rows come as names with meaning). THE LAW:
   every birth is a travelling train, the character of one **K** over
   n >= 8 periods under an envelope, written on the body's cells at both
   levels; the two-integer `born` [now, before] (the one-cell birth, a
   flat pulse of the body's length, broadband: its standing components
   book the ladder by sloshing, not by a passage) is refused by name. THE
   INPUT: the emitter's `train` {direction: one signed unit axis vector,
   periods: n >= 8} and its `born` {now, before, norm}, the profile over
   the body's cells in the box's x-major order (`block_cell_indices`, the
   one convention of the loader, the generator and the engine) and the
   norm T on the born family's VACUUM; the born clock is the born family's
   declared clock [p, q] (one clock per row, the table's family column):
   k = 2 pi p / (2 N q), the wavelength 2 N q / p a whole number of Links,
   the body's extent along the direction n wavelengths ([512, 1] on
   N = 1024: the wavelength 4, the train 32 cells). THE LOADER
   (`TrainDefinition`, `BornTrain`, `_train`, `_born_train`,
   `born_train_norm`, `born_train_flux_sign`), in integers: the direction,
   the periods, the wavelength whole, the extent the train's length, the
   profile's count, a motion, THE FLUX SIGN along the way positive (the
   sum over the body's Links of the engine's flux into the ahead cell from
   its neighbour, now_j before_i - before_j now_i), THE NORM the conserved
   form of the two levels on the vacuum (3 den (now^2 + before^2) - num
   now S_6 before summed over the cells, the profile embedded in zeros on
   the world's faces), the stamp over the profile and its norm. THE
   GENERATOR (`born_train` of the massive record generator, replacing
   `excite_on_the_mode`): now = round(A e h h cos(k i)), before = round(A
   e h h cos(k i + omega)) at A = 2^16, i the cell's index from the tail
   along the way, 3 cos omega = (num / den) (cos k + 2) on the born
   family's vacuum pair, e the taper sin^2(pi (i + 1 / 2) / (2 tau)) over
   tau = X / 4 cells at each end, h the Hann window sin^2(pi (y + 1 / 2) /
   Y) across a transverse extent Y the body does not span and 1 ACROSS AN
   AXIS THE BODY SPANS ON A PERIODIC FACE (a chain, and the extruded axes
   of the one table's boards, whose seed is uniform across the added
   axes: the extrusion rule of 9.30 read on the mode, A's [32, 3, 3] on
   [760, 3, 3] at 2 cos omega = 1.995488, the same as [32, 1, 1] on the
   chain to six figures); its checks, HOST, on its own check board (the
   world's transverse shape and faces, the axis along **K** open and long:
   a margin of one train behind the tail, the train, the body where one is
   run through, the plane one Node deep 40 Links beyond, a far margin of
   twelve trains so that the far face's reflection returns after the window
   of (40 + the body + six trains) / v_g intervals, v_g the dispersion's
   group pace; a narrow train's oblique parts pass more slowly, an 8-wide
   train on a layer 0.9972 in three trains and 1.0000 in six): THE PASSAGE (9.25 (11) (a)) the train alone books its
   one-way flux through the plane within 2 x 10^-3 of T (the light clock
   1.0002; a train of 3 periods 1.0052 on this window, the mathematician's
   1.0285 on his longer one, refused); THE TRANSPARENCY (9.22 (7a) (iv)) every body coupled to the
   born family passes the train run through it with 0.99 of T or more
   booked beyond it (A 1.0002 on the light clock); THE PLACEMENT (9.25
   (11) (b)) every emitter and every receiver at least one train's length
   from every face slab's front, refused naming the tool and the slab. THE
   ENGINE: `_emit` writes the train's two levels on the body's cells
   (`write_levels`, the block's current corner, its family's faces) and
   the norm T the written one; `planted_record` gives a record's levels
   to the rule directly (the generator's checks and the tests' device).
   THE LIGHT CLOCK RESTATED in the one table's form (ALGEBRA.md 9.22 (8),
   its row; 9.30's table with the extrusion rule): [760, 3, 3] periodic on
   y and z, x open with the face slabs 32 deep (`face_depth`), N = 1024,
   light [1, 1] with the born clock [512, 1], matter [800, 809]; A
   [800, 801] of the extents [32, 3, 3] at [600, 632) with the coupling,
   the seed 50 x 2^20 on its mode and a stock of 64, its train along +x;
   the mirror the gap [1, 2] of light's kind over [4, 3, 3] at [690, 694)
   (`mirror_slab`; the holder body's name waits on the cleanup's step 6);
   the set at_well A's own cells (bound to the block, no positions; the
   outgoing train leaves through their Ports, negative and not booked,
   the return enters them); 4800 intervals (COMPUTATION: 64 births at the
   mean cadence P / 2 = 47 on A's mode, P = 94, about 3000 intervals, the
   last return 300, a margin). THE BLIND PINS (examples/events/pins.json,
   written before any run against them; the engine is stabilising, the
   owner's record 1924): the mean click interval after the birth 300 +- 9
   at 64 records (the passage's mean (2 x 58 + 16 + 2) / 0.44721 = 299.7,
   the rms 24.8, the band 3 rms / sqrt 64) and the stock's first click
   250 +- 8 (the least interval since the birth among the records'
   clicks, the fastest passage); the 214 +- 1 of the chain of 674 with the
   cube beside A HISTORY (item 22). THE ONE COMMAND: the kind
   `mean_interval` (the mean over the detector's clicks of the interval
   since the record's birth, rounded), `first_click` the least such
   interval (for one record born at interval 0 the click's own interval,
   as before), every click line carrying its record's `birth`. THE
   DIAGNOSTIC RUN (the one command without pins, no verdict counted, HOST
   9 seconds): LAWFUL, 64 births, 64 clicks all at at_well, none at the
   faces, no record alive at the end; the mean interval 300.3 with the
   rms 25.9, the least 252 (GAMEBOARD readings of the restated file,
   reported to the mathematician for 9.25 (11) (d) and (7a) (iv); no pin
   moved, no verdict). THE ROWS HELD UNDER THE TRAIN: the 26 other
   emitting worlds (the two slits, the pace fans, Sagnac's two, the
   redshift's two, de Broglie's two, the moving mass, the four medium
   index and the twenty-one receding index worlds, the eight short rest
   and reference worlds without an emitter held with their row) cannot
   load under the law
   (the two-integer born refused) and their restated forms are the
   table's: their files moved as written to
   docs/designs/detector_law/held_worlds (HISTORY, the one-cell birth),
   their builders retired, RUN_LIST's rows marked HELD, to be rebuilt from
   the table through the generator (the Boss's item 7). A FINDING FOR THE
   TABLE (COMPUTATION with the eigensolver): the holder family's 32-cell
   well [801, 700] on [7, 8] is a RUNAWAY (2 cos omega = 2.285 over 32
   cells, its interior above 1; the one-cell well 1.902 and bound), so the
   matter-train rows' holder emitters want a well below 1 and near it
   ([699, 700] over 32 cells: 1.9944, W = 700), sent to the mathematician
   for (7a) (iii); the tests' holder emitters use [699, 700]. A SECOND
   FINDING: a narrow train's oblique parts pass the plane more slowly (a
   5-wide Hann train on a 9-periodic layer 0.9905 and an 8-wide one 0.9972
   in a window of three trains, 1.0000 in six), so the check's window is six
   trains and the far margin twelve. THE TESTS: tests/test_born_train.py
   (the profile the formula at every cell, the flux sign both ways, the
   norm against the engine's conserved form of the planted train bit for
   bit, the window across a transverse extent and the uniform profile
   across a spanned periodic axis, the passage within 2 x 10^-3 and the
   3-period train outside it, the engine's write and the passage read by
   the screen with the pointer at the click between the rung and 1.02 T,
   the light clock's file in the table's form with the generator's
   readings and the placement rule's refusals); the emitter, detector-law,
   massive-record, receiver-by-name, initial-state, flux-reading and
   one-command suites on the train (the emitter bodies 32 cells with
   their trains, the born clock [512, 1] on N = 1024, the loader's
   refusals by name, the stamp moving with the profile, the chain digests
   read again); the property test unchanged. THE BIRTH'S FORM HELD (the
   model owner's word of record 1950, through the Boss at 06:50Z: "the
   born train is not generic enough; a world is content written into the
   Nodes at once"): the built form stands on the branch as the record of
   its build and is NOT adopted; the owner's form, a birth as the
   emitter's own mode (the generic generator's profile, already in the
   file) times its momentum's character with no window, no taper and no
   period count, MEASURED on this head with the generator's passage check
   (COMPUTATION): the mode truncated at A's 32 cells reads 1.0047 of the
   norm (its edge 0.357 of the peak, a hard edge, refused), the mode
   written where it lives over 72 cells around A (the edge 0.0035 of the
   peak) reads 1.00002, over 52 cells 1.00005, against the train's 1.0002;
   so the owner's form holds when the birth is written on every Node the
   mode occupies, the tails included; and read as the mathematician's
   9.35 (the born family's lowest mode on the body's cells alone, the box
   with zero beyond it: a half sine along **K**, uniform across a spanned
   periodic axis) times the character, it reads 1.00023 over 32 cells,
   1.00047 over 33, 1.00014 over 24 and 1.00011 over 48, A's transparency
   1.00003, within the tolerance with no constant at all; every check of this item
   (the flux sign, the norm on the vacuum, the count, the stamp, the
   passage, the transparency, the placement) applies to it unchanged; the
   generator loses its three constants and the periods key. The
   mathematician answers on the form and on his passage pin's rms (the
   born record as long as the mode's tails). THE CARRIES (records 1951
   and 1955, a GameBoard diagnostic read on the engine's advance by a
   probe, nothing built): a carry at a Node is the old remainder pushing
   the quotient up (the remainder decreasing); the rate per occupied Node
   per interval is (1 - 1 / W) / 2 with W the remainder's wheel (3 den
   over the gcd of num and 3 den), not the wall: the boxed clock's well
   [800, 800] (W = 3) 0.3229 and its vacuum [800, 809] (W = 2427) 0.49; the
   emitter chain's A [800, 801] (W = 2403) 0.5025, its vacuum 0.4934 with
   the born light and 0.4969 with the body alone; light [1, 1] (W = 3)
   0.32 to 0.30; zero on the empty board. The engine keeps now, before and
   the remainder PER RECORD over the whole board and never a Node's total
   per family with one remainder (the sum of two records' steps differs
   from the step of their sum by the carries; for the mathematician).

28. THE TIGHTENINGS OF THE INPUT (the model owner's rules through the Boss on
   the born train's commit, 2026-09-25; the mathematician's 86e1df43 on
   ALGEBRA.md 9.35 for the tail; built on `emitter-click`). (a) ONE BORDER
   FOR EVERY FAMILY: every family's rows read the world's `boundary`; the
   family key `faces` (a massive kind's own border per axis, periodic by
   default, `massive-record-v1`) is refused by name on light's kind and on a
   massive kind alike; `kind_periodic` returns the world's periodic,
   `FamilyDefinition.faces` is gone, the run record's `families[].faces`
   carries the world's border. The light clock's file loses `matter.faces`
   (the world's x was open for matter already: the profile unchanged, the
   stamp moved); the emitter chain of the tests, closed on x, now bounds
   matter too (a zero face five Links from the well: the iterated mode's
   readings move to 2487 iterations and 467 units from the eigensolver's
   mode, COMPUTATION; 1805 and 276 with the matter border periodic,
   HISTORY). (b) THE CAVITY REFUSED BY NAME: the block key `cavity` (form
   (I), a record held by mirror faces of its own) joins the retired keys;
   the engine's zeroing outside the cells and the margin module's skip are
   gone; the kind's own pair stays no body; `cavity_24` and
   `cavity_24_moving` are CANCELLED with it, their files as written in
   `docs/designs/detector_law/held_worlds/`, their pins the record, their
   builders retired (the massive folder's `pins.py` and `read_runs.py` keep
   their rows as HISTORY, neither under the gate). (c) THE STAMP OVER THE
   WHOLE FILE: `input.hash` is the SHA-256 of the canonical JSON of the
   document without `input` (`input_digest`; was: of the profiles, clocks
   and born trains alone), so that a file changed by hand in any key is
   refused ("not the digest of the file"); a world with no profile still
   needs no stamp; every seeded file regenerated (the same integers, the
   stamp moved, read again file by file); every test that changes a seeded
   document after its stamp restamps it. (d) NO IMPLICIT SEED: a well
   declares `seed` (its amplitude, 0 silent, or its profile); the loader's
   `BLOCK_SEED` 2^20 is gone and `BlockDefinition.seed` has no default; the
   massive generator declares `SEED_AMPLITUDE` 2^20 on every well it builds
   and refuses a well without one; the transparency reading's check board
   takes the body's declared amplitude (the profile's peak). (e) NO DEFAULT
   FOR N AND face_depth: `N` is a required world key (every registered file
   declares it; the 64 of the first worlds written in each); `face_depth`
   is required on a GameBoard with an open face under `detector_law`,
   refused without that law (the slab is its receiver), 0 on a board with
   no open face (no slab); the generator's check board declares 1. (f) THE
   TAIL: a seeded body's profile must be 0 at every Node of every other
   body of its family (a body's mode ends before another body of its family
   begins; the mathematician's "below one unit", in integers 0), refused
   naming both bodies, the Node and the value; the receiver-by-name test's
   two bodies moved from three Links apart to a hundred (A's mode at
   50 x 2^20 on the closed chain ends 63 Links beyond its head, HOST). The
   files of the tightened keys are regenerated, never edited; nothing
   physical moves (the rule, the wall and the click unchanged; every
   reading here COMPUTATION). The retirement of "closed" boards (ALGEBRA.md
   9.30 (2) (f)) is not in this item: it changes every test world and is
   raised separately.

29. THE REMAINDER IS THE CELL'S (the model owner's decision (1) of record
   1962, "this closes everything", and his order of record 1968 that the
   engine change at the single Node, the remainder kept first; ALGEBRA.md
   9.34 (A), 9.35 (6) and (7); built on `emitter-click`). THE LAW: a
   record's division remainder at a Node is one of the law's own numbers
   (record 1966, the owner's "a Node does not keep a remainder" withdrawn)
   and is never reset by the engine: at an emitter's click the ended
   excited record's remainder stays at the body's cells and the fresh
   excited record (the seed again at both levels) takes it over the whole
   board, bit for bit and in its scale (the coupling's scale folded into
   the wall), so the residues of the stock's births spread from the kept
   remainder with no coupling and no draw (9.34 (A)'s computation, 532
   residues in 600 cycles); the load's seed alone starts at 0, the file's
   integers (9.35 (6)), and the residue is read after the first advance as
   before (the born record's u and W at the click from the ended record's
   remainder at the centre cell, unchanged). THE ENGINE: one place, the
   reseed in `_emit` (the fresh record's remainder and scale the ended
   record's); nothing else moves (the rule, the wall, the click, the
   born record's write unchanged). THE TESTS: test_emitter reads at every
   birth of a stock of four that the fresh record's remainder is the ended
   record's at every Node and nonzero on the body's cells (three
   reseeds), and the four residues not all equal; the chain digests of
   test_massive_record moved once more, all three (the residues moved),
   read again at this head; the light clock's diagnostic run without pins
   read again: LAWFUL, 64 births and 64 clicks at at_well alone, the mean
   click interval 302.2 with the rms 26.0 and the least wait 249 (300.3,
   25.9 and 252 at item 27's head; GAMEBOARD readings for the
   mathematician, no verdict, no pin moved). Decision
   (5), the Node clock, follows as item 30; (2), (3) and (6) after it; (4),
   the birth's form, held on record 1963.

## 23. The polariser splits by the record's own state (Reviewer 3's bug line of 2026-09-24, 15:15Z; DECLARATIONS.md section 14 item 6; `polariser-fix`)

1. THE BUG: `_split_table_offers` took the weights C'[s]^2 and S'[s]^2
   from the setting alone and never read the record's label state, so a
   record born on label 1, or on a superposition through joint labels, was
   split as if on label 0: the polariser assigned the outcome instead of
   acting on the state. It lived because the polariser's one test (d)
   drove label 0 alone.
2. THE FIX, with the primitive already on main: the table body keeps its
   half-angle pair (C'[s], S'[s]); per record the channel pointers J(o) =
   SUM over the labels l of U_s[o][bit of l on the arm] x a_l are formed by
   `joint_weights` with this one body (verb B on the record's label
   weights, then the square), the split by [J(+)^2, J(-)^2] over their sum
   with the remainder kept; the label-0 weights `plus`, `minus`, `norm`
   stay on the body as the declared integers. THE GATE (the mathematician's
   line-by-line read, ALGEBRA.md 9.11, 2026-09-24): (a) the bodies acting
   on a record's family are read as the material's own declaration
   (`table_bodies_by_family`), no branch on a family; (b) the weights' sum
   is n_s times the state's norm and never 0, so no guard; (d) for an arm
   of a rank-2 record the weights are the partial trace over the other
   arm's bit (`channel_weights`: the labels grouped by the other arm's bit,
   the pointer coherent within a group, the weight the sum of the groups'
   squares), an arm of HV + VH half on each channel at every setting; the
   joint counts unchanged (test d4).
3. THE TESTS (tests/test_detector_law_tables.py): (d) label 0 unchanged
   (64, 32, 0 of 64 in + at s = 0, N / 4, N / 2); (d2) label 1 swaps (0,
   32, 64) and the equal superposition gives (32, 64, 32) with J(+) = C' +
   S' and J(-) = C' - S', the expected counts the algebra's; (d3) Malus's
   four worlds keep 128, 246, 199 and 177 of 256. The three tests hold: one
   primitive on declared integers, no family name; verb B and one
   division, no root, no float; the entry cell reads its own record's
   labels and pair.

## 22. The body's conditions exact in the initial state, checked at load (SIMULATOR_DEFINITIONS.md, the four building blocks (history since record 1875), the body's conditions 1, 5 and 7; the model owner's words of 2026-09-24, 16:35Z and 16:48Z, through the Boss; `body-check`)

1. THE SHAPE WHOLE ON THE BOARD (`_body_fit_check`, world.py, the loader's
   last check): a body's cube from its lower vertex `position` with the
   edge `side` lies whole on the board on every axis its kind does not
   fold; an open or closed face it would pass, or a periodic axis shorter
   than its edge, refuses the world naming the body, the axis and the
   vertex; the folded axis of extent 1 (a layer, a chain) is the one
   exception; a cube across a periodic seam is whole. Before this line the
   engine's `_cube` and the margin module's `block_cells` cut the cube to
   the board silently (the defect under the owner's word of 16:35Z, "the
   experimenter must be able to put the cube exactly where he wants it").
2. THE SEED ON THE MODE (`check_body_conditions`, the margin module,
   called by run.py and `tools/preflight_worlds.py` after `check_margins`
   on the engine as constructed, before the first interval): for every
   bound body the module's own mode (`bound_mode`, the Lanczos vector)
   rounded at the seed's largest magnitude is the expected initial state
   over the whole board; the body's own record at both levels, `now` and
   `before`, must equal it bit for bit; the first Node that differs refuses
   the world, named with both values. A flat seed (the first builds' form,
   the value on the cells) is refused by it.
3. THE RAMP (the same call): a body with a momentum declares `ramp` at
   least ten relaxation times 1 / (omega_0 - omega_b) of its own well
   (DECLARATIONS.md section 8), or is refused naming the ramp and the
   relaxation time; the ramp's ratio is printed as COMPUTATION. A silent
   body (seed 0, no own record: the receding index's medium body with a
   momentum and no ramp) has no reading and no ramp check, as the margin
   module skips it (Reviewer 3's line F; test g on that world).
4. The three tests hold: the check is host-side at load, outside the
   integer path; no rule of the law moves; nothing is kept at a Node.
   Conditions 2 (the lowered pair) and 6 (the amplitude bound) stay the
   loader's own refusals; 3 and 4 (the bound mode, the margin) stay
   `check_margins`.
5. THE RUN LIST'S WORLDS UNDER IT (tests/test_body_conditions.py, test g):
   as the files stood, the muon's layer pin world alone passed (its seed
   the generator's `mode_profile`); the deep well (and its rest world),
   the boxes, the light clock, sagnac (two) and redshift (two) carried a
   flat seed and were refused. THE WORLD LINE (DECLARATIONS.md section 15
   M1-11, on the owner's word): the massive generator's `seed_on_the_mode`
   seeds every bound body on its mode at the declared amplitude (the
   detector-law generator calls it once its emitter documents are
   complete, `seed_profile=False` on its `world` calls); the layer pin
   worlds' ramp 12000 and ticks 20500 (section 8: ten relaxation times by
   the module's own 1164.6 intervals); every listed massive world loads
   clean under the check; the index's silent body and the light-kind walls
   have no reading. The preliminaries of the regenerated worlds re-run.

## 21. The receiver by name and the click line at the rung (DECLARATIONS.md section 13 item 7, the owner's word of 2026-09-24, 09:50Z; section 10 items 9 and 10; Nature24's eight decisions of 12:40Z through the Boss, the declaration built to; the former build-4 of record 1800, never pushed; the Engine Fixer's line 1 on `engine-fix-1`, 2026-09-24)

- THE LINE (`world.py`: `BlockDefinition.receiver`, the block key
  `receiver`; `detector_law.py`: `receiver_cell`, `_receiver_of`,
  `_line_at_rung`, `_gather_line`, `_release`, `_click`, `_close_clicked`,
  `_close_without_click`): every emitting block declares `receiver`, the
  name of a declared detector set (REQUIRED, refused absent with no
  default; refused on a block that emits nothing; refused naming no
  declared set, the names listed; a set bound to the block itself
  admitted), and that set's one cell is the LADDER of every record the
  block emits, one cell whatever the set's Node count, its rung the set's
  own `wheel` (pointer x wheel at or above the record's norm, the rung as
  today), the record's u 0 choosing nothing. The faces and every other
  set are SINKS for such a record: what they take enters `absorbed` (the
  completion's measure) and the record's HOST `escaped` (the pointer's
  unit) and no pointer, in the offer loop of `_advance`, at the hop's
  entered content in `_move_block` and at a clock body's response in
  `_book_response` alike. The gather line is written by `_line_at_rung`
  at the first interval after the record's train (not sourcing, age at
  or above the train, item 10's own condition) at which the receiver's
  first rung is stamped: `click` the rung's interval, `tick` the line's
  (equal to `click`; the birth plus the train where the rung fell inside
  the train, Reviewer 3's precondition of record 1800), `click_at`
  "rung", `clock` the receiving block's count as the interval began,
  `escaped` the sinks' take by the line. The content moves with the line
  to the receiver's body (`held`, `held_measured`, `transit_absorbed`; 0
  for a block's record, born at content 0), the record's content is 0
  from then and it lives on (field energy the sinks absorb) to close by
  `_complete` as before with NO second line: `_close_clicked` books its
  content (0) to the escaped row, releases its rows and counts it on the
  ledger's HOST row `closed_after_click` (`transit.closed_after_click` in
  the books; the records reading's `clicked` and `escaped`), written on
  a world with a receiver alone. A record whose receiver crosses no rung
  within the ticks writes NO line (`_close_without_click`): its content
  goes to the row of the take that ended it, `taken_by_emitter` where its
  own emitter took it and the escaped row where a face or a set did (0
  for a block's record), or it stays open at the run's end. The emitter's
  own cells take on no pointer at every age (section 18, PR 1115 as
  merged: `_move_block` holds the entered Node at 0 for the block's own
  record from the train's end and books nothing, the row evolving during
  the train, line B; nothing added), so a block naming the set at its own
  cells never clicks (test (b)). A lamp's record keeps the close and the
  cell by u (line (iii), the lamp's ladder by name, is a later order).
- THE FIVE REGISTERED FILES (the Boss's addition): `sagnac_k3.json` and
  `sagnac_rest.json` (block 0 `receiver` "at_b", block 1 "at_a"),
  `light_clock_60.json` (A "at_a"), `redshift_k3.json` and
  `redshift_control.json` (A "light_detector") receive the key by the
  minimal edit of that one key after `own_grace` (their last commits
  are hand edits, no generator in tools/ names them; the files' own form
  `json.dumps(indent=1)` kept, nothing else in the file moved). The test
  worlds of `tests/test_massive_record.py` with an emitting block name a
  receiver ((h) a body at x = 230 read as `screen`; (ac) `A_face`; (ai)
  and (ak) `at_a`), and (ac)'s far body is read as a sink (no rung, its
  take on `escaped`).
- WHERE THE ENGINE FIXER'S READING AND THE SPECIFICATION DIFFER, said
  here as ordered: (1) "the sinks book to the HOST row `escaped`": the
  ledger's escaped row counts CONTENT and balances the books in content,
  and a block's record carries 0, so the sinks' take (motion, the
  pointer's unit) is booked to the record's HOST `escaped` (the gather
  line and the records reading) and the content, 0, to the escaped row at
  the close; (2) "the hop take's fix: the exemption becomes `emitter ==
  block`": PR 1115 as merged already books nothing of the block's own
  record at any age; its form holds the entered Node at 0 after the
  train (the own take's own state) instead of leaving it to evolve, and
  is kept, Reviewer 3 having CONFIRMED it (record 1800); the behaviour
  named, nothing on the own pointer at any age, is pinned by test (b).
- THE READINGS (EXPLORATORY, no pin run; `tests/test_receiver_by_name.py`
  reads the form, not the numbers): sagnac_rest as registered reads every
  hold record's line at the other's set 108 intervals after its birth at
  rest, both directions alike (DETECTOR); the light clock's chain of 173
  closed with A naming `A_face` reads the first record's line 214 after
  the birth (DETECTOR; the T = 0 preliminary's number of record 1800), no
  rung during the grace of 140; two blocks one Link apart cross the rung
  inside the train on some records, the line then at the birth plus the
  train. HOST: sagnac_rest 420 intervals in 1.4 s, the light clock 600 in
  0.4 s (this machine).
- THE THREE TESTS: generic (one sentence, the ladder's size the only
  case; the receiver's name a world declaration as a set's position is;
  no kind, no family name, no branch on a physical name), vector (the
  rung (E) on the pointer, verb T on `absorbed` and `escaped`; integers
  only, no root, no float), local (the cell's own pointer on the record;
  nothing kept at a Node; the sinks' take a per-record integer).
