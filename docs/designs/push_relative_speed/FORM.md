# Change 2, "the push reads the crowd the body is in, at the relative speed": the integer form and the verdict (read-only, the mathematician, 2026-09-20)

The proposal: the G2 physicist's [RULES.md section 2](https://github.com/Closer24/Universe24/blob/5322dc4/docs/designs/hubble_stars/RULES.md)
on `claude/series-g2-stars` at `5322dc4`, from the finding of
[DESIGN.md section 5](https://github.com/Closer24/Universe24/blob/5322dc4/docs/designs/hubble_stars/DESIGN.md)
and the worlds' README "What the law lacked": a body reads exactly 1.000
row per interval from a fixed beam at rest, receding at 0.30 and 0.45 and
approaching at 0.30, so its own motion never Dopplers what it reads, and
an exact crossing count needs one interval of memory per (row, body),
which is not admissible. The change is not being built; this is the
referee's reading of its integer form, asked by the Boss, for the owner.
The law read: [BEAM_LAW](../../BEAM_LAW.md) section 3 (steps 2, 4, 5), the
flight table, notes 17, 23, 31 and 33; the
[local integer operation contract](../../ARCHITECTURE.md#local-integer-operation-contract);
series C's identities ([the register](../../EXPERIMENTS.md#c-the-couplings-under-the-beam-law-on-the-plane-2026-09-19));
record 35 (the columns' verification). Every integer below is from
`relative_speed_map.py` beside this file (its output
`relative_speed_map.out`; standalone, the flight table's pace taken from
the engine's own `flight_table`), nothing from an engine run: none was
needed to state a number, and none is made before the owner's word.

## 1. The exact integer form under the contract

Per body A, per axis a, per arriving family B, per column c, the proposal
replaces the arrivals' flow by the presence at the relative speed. The
intermediates, each with its bound and where it is refused:

| Intermediate | Definition | Bound | Refused |
| --- | --- | --- | --- |
| `p_a` | the body's momentum component on the axis, signed, label units (the record) | within 2^62 - 1 (`MOMENTUM_BOUND`) | as today, at the push that would pass it |
| `D_a` | `Q S M + \|p_a\|`, the step rule's divisor (`_move`), M the content the frame read | `Q S M < 2^62` by the label bound; `D_a < 2^63` | the parser's static budget as today; `bounded` |
| `(N_d, T_d)`, the pace of a direction d along the axis | on a heading `(32, 55)`: the period's Links over the period; on a direction `(a, b, c)` the pair `(a Q, T_d)`, `T_d = isqrt(3 \|D\|^2 Q^2)` (the x-Links per interval, `a / S_1` of `S_1 Q / T_d`), one world constant per direction beside `u_d` | `a Q <= 64^2`, `T_d <= isqrt(3 x 3 x 64^2 x 64^2) = 12 288` | never (a table) |
| `s` | the sign of `u_{d,a}` against the axis | +-1 | never |
| the relative speed of the row against the body, as a pair | `(N_d D_a - T_d s p_a, T_d D_a)`; on a heading `(32 D_a - 55 s p_a, 55 D_a)`; its absolute value the weight | `\|N_d D_a - T_d s p_a\| <= (N_d + T_d) D_a`, on a heading `87 D_a`; the denominator `55 D_a` | **new refusal needed**: `87 D_a` must fit the register, so `D_a < 2^62 / 87` at load; the pair does not reduce for `p_a` not 0 (gcd(32 D - 55 p, 55 D) is 1 in general) |
| `V_{B,d}` | the presence of the rows of direction d at the body's Node this interval, arrived or dwelling (`read_arrivals` order 0 outside + here, per direction), times the label `amount x u_{d,a}` | as the flow today, `Q x amount` per row | the store's bound |
| the product per direction | `\|V_{B,d}\| x \|E_c n_c\| x \|N_d D_a - T_d s p_a\|` | must fit 2^62 - 1 before it is formed: tested by division twice, `\|V E n\| <= (2^62 - 1) // \|num\|` | refused naming the body, the column and the direction (the mathematician's R1) |
| the whole part | `by_clock(age_A, \|V E n num\|, D_c d_c x T_d D_a)` per direction, sign `sign(V E n num)`, summed over the directions and then over the columns, the partial sum bounded after each term | `(age_A + 1) x product < 2^63` in the int64 register, else Python integers as `push_form` does | `bounded` after each term (R2) |

Two things the proposal leaves open, fixed here so that the form is exact:
(i) the pace is per direction, not one number: on a fan (series I's 290,
Bohr's 2616) the rows reaching a Node come on many directions with
different paces along the axis and different dwells, so the sum is per
(direction, column), not per column: the host cost rises from k products
per arriving group to k x (directions present); (ii) the floor is per
(direction, column), never summed before the floor, as record 35 fixed
for the columns; summing first and flooring once differs by up to the
number of terms minus one per interval.

**The bound problem is real on the register's worlds.** With the width
S = 2^28 (series I, series J, the gate set's `weak/j3_deuteron.json`),
`D_a = 64 x 2^28 x 1837 = 3.2 x 10^13`; the nuclear column's product
`|V E n|` is 3.0 x 10^11 (the registered push), times `32 D_a = 1.0 x 10^15`
gives 3.1 x 10^26, far past 2^62 - 1 = 4.6 x 10^18: the form as written
refuses the deuteron at its first push after the first (for a body at
rest, p = 0, the pair reduces to (32, 55) and fits; the moment the body
holds any momentum it does not). The only bounded form is a speed at a
declared grain: `w_a = (T_d Q x |p_a|) // D_a`, a whole number below
`T_d Q = 3520` on a heading, and the pair `(N_d Q - s w_a, T_d Q)` at most
`(5568, 3520)`; that is a new quantisation of the body's speed to
1 / 3520 Links per interval, floored (a bias below 1 / 3520 per interval,
not exact on average: the floor of a value, not of a rate off a clock),
whose remainder has no owner: the contract's "a rule that permits
division with remainder must declare the remainder owner" is not met by
the proposal and is met by this grain only if the owner accepts the bias
as a declared width, like S and Q.

## 2. The period-sum identity: refuted at a Node, exact over a spatial period

A row on a heading is at the x-th Node for `d(x)` ages, the number of
`tau` with `m(tau) = x`, `m(tau) = (2 tau Q + 110) // 220`: `d(x)` is 1 or
2 and a function of x alone (`relative_speed_map.out` A: over one spatial
period of 32 Nodes, 23 Nodes of dwell 2 and 9 of dwell 1, the sum 55). A
fixed beam's rows all reach the x-th Node at the same age, so **the
presence at a fixed Node is `d(x)` rows per interval, constantly**, and the
proposal's reading at a body at rest is `d(x) x 32 / 55` of the beam's
rate: 32 / 55 (-41.8 %) on a dwell-1 Node, 64 / 55 (+16.4 %) on a dwell-2
Node, never 1. The claim "55 arrivals become 55 x 55 / 32 row-intervals of
presence and c x presence returns the 55" mixes the average over Nodes
with the count at a Node: at one Node over 55 intervals the presence is
55 x d(x) = 55 or 110 row-intervals, not 3025 / 32 = 94.53. The identity
is exact **over the 32 Nodes of one spatial period in one interval**
(presence 55 rows, times 32 / 55, 32 = the 32 arrivals, remainder 0), that
is for a body that traverses whole periods, and only there. The remainder
of `by_clock` over the reader's clock is bounded by one unit per interval
and exact on average as always; the dwell factor is not a remainder but a
systematic factor that depends on which Node the body sits on, and it
never averages out for a body at rest.

## 3. Series C's identities on the new integers, and the gate set

- **The equivalence** (item 1, `push_m = m x push_1` record by record):
  fails record by record by the floor (with the divisor `55 D_a` in place
  of 1 for gravity, `by_clock(age, m X, den) - m by_clock(age, X, den)` is
  within 2 (m - 1)), holds exactly in the sum over a clock period of
  `den` ages. Today it is exact record by record because gravity's divisor
  is 1.
- **The third law on two fixed bodies** (item 2): holds as today (to the
  apportioning's grain): the dwell of B's rows at A's Node is `d(r)` of
  the distance r, symmetric, so both read the same factor `d(r) x 32 / 55`
  and the two pushes stay opposite and equal in the sum; per tick the
  same grain as today.
- **Superposition** (item 3 and the reading's linearity): holds exactly
  per row (the reading is a sum over rows), the floor's grain per
  (direction, column) as today per column.
- **Coulomb's exponent and the far field** (items 5 and 7): a single
  fixed probe at distance r reads `d(r) x 32 / 55` of today's push, so the
  registered `read` records of every fixed probe on a heading move by
  x 0.582 or x 1.164 by their Node; ring means keep the exponents (the
  average dwell 55 / 32 over a period), single-probe series (C's item 4
  fronts, E's shells with `read`, the coupling `1b` probes) become a comb
  of two values along the line. Item 7's electric / gravity ratio is
  unchanged (the same factor on every column).

The gate set (`examples/events/gate_set.json`), which worlds move and by
how much, from the map and the flight table (no run):

| World | Moves? | By how much |
| --- | --- | --- |
| `weak/j3_deuteron.json`, `weak/j3_deuteron_crowd.json`, `nucleus/alpha_square.json` | yes, every push from the first | the first read of a body at one Link on the 284 fan: the 57 directions whose first step is +x, each with its dwell (1 or 2) at the first Node and its pace `(a Q, T_d)`: the proposal reads 1921.006 per unit against today's 3008 (`relative_speed_map.out` C), the ratio **0.6386**; the deuteron's 310 967 280 640 becomes about 198 593 779 901 per interval; the same factor on every column, so the binding condition `G^2 + M^2 > Q^2` keeps its sign, every hand-over and step tick moves; and with p not 0 the unreduced pair refuses the run (section 1) |
| `bohr/r2.json` | yes | the electron (a body of three Nodes at r = 2) reads the proton's 2616-direction fan at the dwell and pace of each direction at its Nodes: the same kind of factor, not computed here (a fan of 2616 with a body on a set; the map's method applies) |
| `coupling/1b_m16.json` | yes | the fixed probe at 12 Links on -x reads d(12) = 2: x 64 / 55 = 1.164 of every registered push; the free probes' steps move with it |
| `hubble/pushing_age.json`, `catalog/sun_planet.json` | yes | every pushed body; the planet on a set of nine Nodes averages the dwell over its Nodes (a body on a set reads the sum over its Nodes) |
| `bell/*`, `catalog/lamp_mirror_screen.json`, `lensing/heavy_meeting.json`, `detector/grouped_12_nodes.json`, `weak/j2_ladder.json`, `heisenberg/*` | no | paid rays push by their label at the click, unchanged by the proposal; the meeting is the light's own rule, untouched |

So the change moves eight of the fifteen gate worlds and every registered
push of a free family (series C, 7, D, E's `read` probes, G, G2, H, I, J,
the catalog), by a factor between 0.58 and 1.16 per fixed reader and by
the crossing factor per moving one, plus the refusals of section 1.

## 4. The bar of the finding under the proposed form: the expected integers

From the map (`relative_speed_map.out` B), a fixed source releasing one
row per interval on +x, a free body of `(p, D)` stepping by the step rule,
200 intervals after the beam's front is past every Node the body visits;
the law's arrivals (today), the proposal (presence x the pair
`(|32 D - 55 p|, 55 D)` off the clock), the smallest alternative of section
6 (the arrivals x the pair `(|32 D - 55 p|, 32 D)`), and the host's
crossing count (a control with memory, never a rule):

| Case | The law today | The proposal | The alternative | Crossings | (c - v) / c x 200 |
| --- | --- | --- | --- | --- | --- |
| at rest, a dwell-1 Node | 200 | **116** | 200 | 200 | 200 |
| at rest, a dwell-2 Node | 200 | **232** | 200 | 200 | 200 |
| receding at 0.30 | 200 | 96 | 97 | 97 | 96.9 |
| receding at 0.45 | 200 | 44 | 45 | 46 | 45.3 |
| approaching at 0.30 | 200 | 305 | 303 | 304 | 303.1 |
| co-moving at c = 32 / 55 | 200 | 0 | 0 | 2 | 0 |
| outrunning at 0.75 | 200 | 56 | 58 | 58 | 57.8 |

The proposal passes the bar's moving cases (its test (a) receding 0.48
and approaching 1.52, its test (b) nothing at c) and fails the bar's first
line: **a body at rest does not read the beam's rate**; it reads 116 or
232 of 200 by the Node it sits on, and the physicist's test (a) as written
("presence x c = the beam's rate over a period") would fail on the engine
at every fixed body. The alternative passes every line, and at rest it is
today's integers exactly (the pair is `(32 D, 32 D)` = 1 for p = 0).

## 5. Locality

Confirmed local, both the proposal and the alternative: the body reads the
rows at its own Node (the presence or the arrivals the one reading already
takes, with their directions on their records) and its own record (`p_a`,
M through `D_a`); the pace `(N_d, T_d)` and `u_d` are world constants of
the direction table, as `u_d` is today; no history, no register, nothing
of another Node. The only new state is none; the only new table is one
pair per direction. (The crossing count of the map is the host's control
and is not local: it needs the order of the pair one interval earlier, as
RULES.md says.)

## 6. Verdict

**Not admissible as a repair of the one reading.** The reading it replaces
is exactly right where it is exact today, at rest: a fixed body reads the
beam's rate at every interval, and every registered push of series C
rests on that. The proposal moves the rest reading by the dwell of the
Node the body sits on (x 0.582 or x 1.164 on a heading, x 0.639 on the
register's deuteron fan), a factor that no period averages out for a body
at rest, and it does not fit the register on the register's own worlds
(section 1: the unreduced pair `55 D_a` at S = 2^28 overflows at the first
nonzero momentum), so it needs a quantised speed with an unowned remainder
besides. Its period-sum identity holds over 32 Nodes of space, not over
55 intervals at a Node (section 2).

**Admissible as a hypothesis with its own identity only in the smallest
alternative form**, which keeps everything the law does at rest and adds
the Doppler for a moving body: **the arrivals at the relative speed**. The
push reads the arrivals as today, each row weighted by the pair
`(|N_d D_a - T_d s p_a|, N_d D_a)` (on a heading `(|32 D_a - 55 s p_a|,
32 D_a)`), floored off the reader's clock per (direction, column), the
sign of the push flipped where `N_d D_a - T_d s p_a` is negative (a body
outrunning a row is hit from behind). At p = 0 the pair is 1 and every
registered push of a fixed body is bit-identical (series C's identities,
record 35's 11 945 pushes, the third law, item 7); for a moving body it
reads the crossing rate (section 4: 97, 45, 303, 0, 58 against the control's
97, 46, 304, 2, 58), which is the flux (c - v) / c the finding asked for.
Its price is the same bound question: the pair must fit, so either the
width is bounded at load (`D_a < 2^62 / 87`, which the S = 2^28 worlds
fail) or the speed is read at the grain `1 / (T_d Q)` = 1 / 3520 with the
bias declared (a new width of the world, the owner's). It changes the
integers of every moving pushed body (the orbit series D, Bohr's H, the
planet, G, G2's stars, the contact worlds once a body holds momentum) and
none of a fixed one; it needs its own identity (say `doppler-v1` under a
world key, absent by default, every registered world byte-identical
without it), the physics-rule review, tests (a) the identity at p = 0 on
every gate world, (b) the bar's six lines from section 4 as the pinned
integers, (c) the refusal at the bound, and the re-registration of the
moving-body worlds. What it does not give: an exact crossing count (the
leapfrog and the miss stay, only their mean is corrected), and nothing
for a body on a set beyond the sum over its Nodes.

A referee's last line: change 2 as proposed trades an exact rest reading
for an approximate moving one; the alternative keeps the first and adds
the second at the same locality and the same cost, and is the form to
decide on, not the presence.
