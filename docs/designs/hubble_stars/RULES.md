# Two rule changes for a readable Hubble diagram of gravitating stars: the physicist's design

The model owner, 2026-09-20, on the two findings of series G2
([DESIGN.md](DESIGN.md) section 5, the worlds' [README](../../../examples/events/hubble_stars/README.md)
"What the law lacked"): "1 and 2 are very important for a solution and a
new run." This is the read-only design of the two rule changes, for the
engine's implementation under [physics-rule validation](../../../skills/physics-rule-validation/SKILL.md)
with the mathematician's check of the integer forms; the experimenter
changes no law. Each change is stated with its finding, its rule as it is,
the rule proposed, its integer form and bounds, what it leaves bit-identical,
what it re-registers, and the tests the implementation must add. The new run
of series G2 follows the landing of change 1 at least; change 2 is the
owner's to weigh, since it moves registered integers of every pushed body.

## 1. The step rule under a changing momentum

**The finding (measured on the engine, `gravity_none`).** The step of a
free measured event on an axis fires when `by_clock(age - 1, |p|, D)` = 1,
D = Q S M + |p| (BEAM_LAW section 3 step 5, note 17: "no remainder is kept;
the count is the whole part off the clock"), that is when
`floor(age |p| / D) - floor((age - 1) |p| / D) = 1` at the CURRENT |p|. Under
a momentum that falls steadily the argument age x |p| / D barely moves
(age grows while |p| falls), so the count `floor(age |p| / D)` stands still
for tens of intervals and the body stalls; when the argument then sits just
above an integer the difference is 1 at every interval and the body steps
at every interval: `s_px1` stepped at the ticks 321, 322, 323, 325, 326 at a
momentum that says 0.019 Links per interval (its own record); the longest
stall of a late window 85 intervals, the longest burst 12 Links on
consecutive intervals. Two contradictions with the law's own principles:
(i) one Link per interval is faster than the ray (c = 32 / 55), against
"one speed" (Highlights 5.4, 2026-09-19); (ii) the Links a body has made
equal age x v_now, as if it had always moved at its present speed: a
deceleration erases distance already made, an acceleration creates it, and
neither is a motion. A body's Doppler as read at a detector is the Doppler
of these stalls and bursts, which is why series G2 cannot read q.

**The rule proposed: the count is the whole part of the distance the
momentum has driven.** The measured event's record (where `age`, `waited`,
`owed`, `steps` and `pending` already live: the external thing's own
record, not a Node's register) carries per axis one integer `drive_a`, 0
at the start, and at every self-creation in which the body may step (it
owes nothing):

    drive_a <- drive_a + |p_a|
    if drive_a >= D_a:  step one Link on axis a (the sign of p_a), drive_a <- drive_a - D_a
    with D_a = Q S M + |p_a| read at that self-creation

- **Bit-identical where the momentum is constant.** With |p| constant,
  after n self-creations `drive = n |p| - k D` with k the steps made, and
  the step fires exactly when `floor(n |p| / D)` increments: the same ticks
  as `by_clock(n - 1, |p|, D)` for every n (the accumulator is the remainder
  of that very division). Every world whose bodies never take a push (the
  coasting crowds, the catalog's fixed things, the Bell and slit worlds,
  series C's fixed probes) replays byte-identical; the implementation's
  test (a) proves it on a bar for |p| / D over a grid of fractions and 10^4
  self-creations.
- **At most one Link per self-creation, always**: `drive < D` before the
  addition and `|p| < D`, so `drive + |p| < 2 D` and one subtraction
  suffices; no burst can exist. Under a falling momentum the next step
  comes later (the accumulator grows slower), under a rising one sooner:
  the motion follows the momentum at every self-creation, and the Links
  made are `floor(sum |p| / D)` to within one, the distance the momentum
  drove (test (b): a body whose momentum is halved at every 50th
  self-creation makes the Links its integrated speed says, within 1).
- **Bounds.** `drive_a < D_a <= Q S M + |p_a| < 2^62` by the label bound;
  `drive_a + |p_a| < 2^63`, formed in Python integers or checked by
  `bounded` before the addition; nothing else grows.
- **What "no remainder" meant, and what changes.** Note 17's "no remainder
  is kept" was decided for a constant momentum, where the whole part off
  the clock IS the remainder-free form of the same count. Under a push the
  count needs the momentum's history, and the only local place for it is
  the body's own record, beside its age: one integer per axis, a report of
  the body and not a Node's state (LOCALITY-1 untouched: the Node holds
  only the events there; the body reads only its own record). The owner's
  decision of 2026-09-19 is superseded for the moving body only; nothing
  changes for the clock, the release, the lamp or the owed count, which
  read a rate against an age that no push changes.
- **The turn by momentum** (Bohr, note 30 (ii)): the phase turn at a step
  read `k0 = floor((age - 1) |p| / D)` and `k1 = k0 + 1`; with the drive,
  k0 is the body's `steps` count on the axis before the step and k1 = k0 +
  1, the same numbers where the momentum is constant.
- **The frame's order** is unchanged (`nature_beam`, then `_move` in number
  order); the contact rule reads the same refused step; a body on a set
  steps as one; the escape on a face is unchanged.
- **Record and refusals.** `run.json` and `state.json` carry `drive` per
  measured event (three integers); the `step` line carries the drive after
  the step; a declared `drive` in a world file is refused (the start is 0).
- **Re-registration.** Every registered world in which a body steps while
  its momentum changes reads differently from the first push on: the
  coupling `1b_m1`, `1b_m4`, `1b_m16` (the probe's steps from tick 21),
  the orbit series D (all six), Bohr's H (the electron under the turn), the
  catalog's `sun_planet` (the planet), series G's pushing worlds and G2's
  gravity and double crowds; the neutron star's neutrons (refused steps, a
  contact) and the deuteron by the contact's hand-over. Each is re-run and
  its entry gets a dated line; nothing else moves.
- **Tests the implementation adds.** (a) the identity at constant momentum
  above; (b) the integrated distance under a halving momentum; (c) never two
  Links in one interval on any axis under any push sequence (a random push
  sequence within the bound, 10^4 intervals); (d) the drive bounded and
  `state.json` carrying it; (e) the turn by momentum unchanged at constant
  momentum.

**Why this and not the alternatives weighed.** "The count since the last
step" (`by_clock(age - age_last_step, |p|, D)`) needs no remainder but
gives the rate `1 / ceil(D / |p|)` in place of `|p| / D` (a body at v = 0.3
would move at 0.25): not bit-identical and wrong. A distance label
`sum |p|` on the record is the same rule with an unbounded integer. Reading
the count off the momentum's history is what the drive does with one
bounded integer.

## 2. A body's own motion and what it reads

**The finding (measured on a bar, 700 intervals).** A fixed source
releases one row of 64 per interval toward a free body of content 2^20;
the body reads (`read`, the push taken) exactly 1.000 row per interval at
rest, receding at 0.30 and at 0.45 Links per interval, and approaching at
0.30 (200 rows in 200 intervals in every case), where the rows crossing a
body's world-line are (c - v) / c = 0.48 and 0.23 of the beam's rate
receding and (c + v) / c = 1.52 approaching. The rule as it is reads "the
rays that arrived this interval at its Node" (BEAM_LAW step 4): a row
stepping into the body's Node. On a lattice where a ray dwells (c = 32 / 55:
it steps in 32 of 55 intervals) that counts a co-moving row every time it
re-enters the body's Node after the body stepped ahead of it (a leapfrog:
at v = 0.45 each row is read about four times), and misses a head-on row
whose Node the body steps onto, since it then steps into the Node the body
left. The two errors make the reading independent of the body's motion. In
series G2 this over-counts the pull of the inner stars on the outer ones
(co-moving rows) and under-counts the pull of the opposite chain (head-on
rows); the measured momenta match a derivation with the emitter's Doppler
alone within 10 %.

**What an exact rule needs, and why it is not memoryless.** A crossing is
a change of the order of a row and a body along the axis. With a dwelling
row and a stepping body the same pair coincides several times (row ahead
and dwelling, body onto it, row ahead again), and telling a crossing from a
leapfrog needs one interval of history per row and body (whether the row
was strictly behind before the coincidence). The rows carry no such bit and
a bit per (row, body) is neither bounded nor local; the alternatives that
read the destination's dwelling rows at the body's step, or skip the rows
arriving from the Node the body just left, each fix one case and double or
miss the other (the physicist's count of the cases, kept in the worlds'
README of the next run). So an exact crossing count is not admissible under
the law's principles.

**The rule proposed: the push reads the crowd the body is in, at the
relative speed.** The one reading already takes the presence at the
body's Node (the zeroth moment of every row of another number, rest and
moving alike: what the clock counts, series E). Let the push read the same
rows, each weighted by the relative speed of the row's flight and the body:
for the group of a family B's rows PRESENT at the body's Node this
interval (arrived or dwelling, the rows the clock counts), with the label
flow `V_B = sum amount x u_d` and per row the flight's speed along its
direction, c on every direction (the flight table's one speed), and the
body's speed along that direction `v_d = (p . u_d) / (Q D_a)` in Links per
interval,

    push_A = sum over the columns of epsilon_c x sign(V E_c n_c) x by_clock(age_A, |V E_c n_c| x (C_num - (p . u_d) rounding), D_c d_c x C_den)

in the form the mathematician fixes: the flux through the body is the
presence times |c_d - v_d| per interval, `c_d = 32 / 55` on a heading (the
period's Links over the period, `flight_table`) and `v_d` the body's own
speed on the row's direction read off its record (`p`, the step rule's
`|p| / D` per axis, signed), so that a body at rest reads the presence
times c, a receding body less, an approaching one more, and a body moving
with the beam at c reads nothing. In integers: the relative speed as a pair
`(32 x D_a - 55 x s p_a, 55 x D_a)` on a heading (s the sign of the row's
heading against the axis), the product with the presence floored off the
reader's clock by `by_clock` as every column is, every product tested by
division before it is formed (the mathematician's R1, R2), the partial sums
bounded after each column.

- **Where it is bit-identical.** Nowhere per interval: a body at rest reads
  the presence times c in place of the arrivals, the same rows summed over
  a period (the presence of a beam is its arrivals times the dwell: on a
  heading 55 arrivals become 55 x 55 / 32 row-intervals of presence, and
  the flux c x presence returns the 55) but distributed over the intervals
  differently. Every registered push (series C, 7, D, E's probes with
  `pass` are unaffected, G, H, K's mass, the catalog) changes per tick and
  agrees in the sum over a period within the grain of the floor: series C's
  identities (the third law, the equivalence, superposition) hold on the
  new integers as on the old, and the mathematician re-verifies them as the
  columns were (record 35).
- **Bounds.** The presence at a Node is bounded by the store; the product
  presence x |E n| x (32 D_a + 55 |p_a|) is tested by division before it is
  formed and refused naming the body and the column, as the columns are.
- **Locality.** The body reads the rows at its Node and its own record;
  nothing of another Node, no history, no register.
- **What it does to G2.** The pull of the inner stars on the outer ones
  falls by (c - v) / c and the pull of the opposite chain rises by (c + v)
  / c: the acoustic derivation pinned before the first run
  (`throw_derivation`, the rule "acoustic") becomes the law's, and the
  inner stars of the fast lines are expected to GAIN speed as it derived
  (|p(end)| / p(0) up to 1.11 in `gravity`): the model's own line gravity
  under a retarded, rate-read pull, to be read at the detector after
  change 1.
- **Tests the implementation adds.** (a) the bar of the finding: a body at
  rest reads presence x c = the beam's rate over a period; receding at 0.30
  reads 0.48 of it and approaching 1.52, within the floor's grain over 200
  intervals; (b) a body moving with a beam at the beam's own speed reads
  nothing; (c) the third law on two fixed bodies (series C item 2)
  unchanged in the sum over a period; (d) every column floored on its own,
  the bounds refused loudly.

**The owner's decision needed.** Change 1 is a repair of the step rule
under its own principles and re-registers the moving-body worlds; change 2
is a new form of the push (the crowd at the relative speed in place of the
arrivals) that moves every registered push integer and needs the
mathematician's verified form first. The physicist's recommendation: land
change 1 now and re-run series G2 under the record click with the
expectations of DESIGN.md section 4 re-derived by the emitter-only rule
(the law as it is until change 2); then decide change 2 on its own design
and re-run G2 once more with the acoustic expectations. Two runs, each with
a stated expectation and a decision it serves.
