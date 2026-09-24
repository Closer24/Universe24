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
| 3. The margin rule, a LOAD-TIME check (section 11 item 4, Reviewer 3's two lines) | `diagnostics/massive_record_margin.py` (FINDING 1): for every block of the massive kind the bound mode's `2 cos omega_b` as the largest eigenvalue of `D^-1/2 (L / 3) D^-1/2` on the world's own board and faces (a Lanczos in numpy, the largest Ritz value to 1e-9), then `cosh kappa = 3 D_out cos omega_b - 2`, the extent `1 / kappa`, eps, printed before the world runs; the rule: a CONTROL world's cells at least ONE extent from any non-periodic face of the massive kind and a periodic axis's side at least the block's side plus TWO extents; a PIN world's cells at least TWO extents from a non-periodic face and a periodic side at least the side plus FOUR extents; a declaration below the margin refused naming the block, the axis, the extent and the distance; an unbound block (omega_b at the gap) refused; called by `events/run.py` before the simulation is built and by the preflight | `margin` on the block (`"pin"` by default; `"control"`) | none (a check of the declaration) | (n) |
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
| 3. The splitter's table | DECLARATIONS.md row 2b, DESIGN.md's fourth receiver form ("a partial re-emission with a phase"), ALGEBRA.md 4.6 (the split (w, m, p) -> ((w a_i, m A, p + t_i)) an isometry): the split's integer matrix acting on the record's read phase, the two outputs re-emitted by the table form | `Splitter` in the engine from a measured event's `table` `{"rule": "rerelease", "inputs", "weights", "turns"}` with its `directions` the outputs (the amplitude series' keys, admitted under the key when `inputs` is declared; a fan without inputs stays refused): the Node held at 0 and taking the arriving wave, booking no offer (no click at a splitter); per interval, per light record, the phase and amplitude at each input Node (the Node the input direction arrives from) read by component 1 with the amplitude the largest level the input has shown to that record (an integer register of the table, a default named), and each output Node driven at SUM_i w_ij A_i C[phi_i + t_ij] / (256 R_i), R_i the root of the row's norm, exact (checked at load: 21^2 + 20^2 = 29^2; a norm that is no square refused naming it); verbs B, D (one division per output per interval, no remainder carried: the level is the read phase's function, not an accumulation, a default named) and T (the output's drive, as the lamp's) | (c): on a layer the lamp's train through the splitter's weights [21, 20] and turns [0, 16]: the driven output peaks in the ratio 21 : 20 within 3 percent, the +x peak 21 / 29 of the input's read amplitude within 3 percent, the phase read at the two outputs a quarter turn apart (16 steps within 2) on three quarters of the intervals, the splitter's Node 0, no click and no offer there, the books balanced, the wave beyond the outputs nonzero; a fan without inputs refused; a row of norm 2 refused |

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
  its faces the kind's, taken by nothing (MUST 2), coupled to no block
  (the coupling is declared on light's row, MASSIVE_RECORD.md section 7;
  a default, named), never completing (MUST 2; its content stays in
  transit, the books balanced); the drive at the lamp's Nodes for the
  train is the same verb as light's (a block's record has no train and is
  not driven); `read_phase` reads it at the family's clock.
- Light's [1, 1] unchanged: a block's records take the same path as
  before (no `driven`), and the light record's rows are identical beside
  a matter lamp (test (z)); the first build's digests stand (test (p)).
- Test (z), `tests/test_massive_record.py`: the kind [156, 157] at the
  clock [77, 25] on N = 64 (omega = 0.302 above the gap omega_0 = 0.113),
  one lamp on a chain of 200; the band on a chain from the rule's plane
  wave, cos k = 3 den cos omega / num - 2, k = 4.99 steps of 64; the
  record's phase at the interval 100 read at each Node's peak register
  over 4 Links on both sides of the lamp: 21 steps on each side beside
  4 k = 19.97 (the reading's grain of section 11's FINDING and the
  train's dispersive front; the test's bound 2 steps); the books
  balanced at every interval; light's rows identical with and without
  the matter lamp; the lamp without the clock refused.
- Not in this line: the probes and the `mode` line sum light's rows
  only, as before (a matter lamp's train is not probed); a splitter's
  table reads light's records only. Both are the physicist's to ask
  for, not the builder's to widen.
