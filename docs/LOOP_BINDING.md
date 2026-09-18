# Binding as a loop (`loop-binding-v1`)

The design of feature 14 of the [ray-event model](RAY_EVENT_MODEL.md#6-migration-in-order),
written on 2026-09-17 from the model owner's decision in
[Highlights](HIGHLIGHTS.md#34-matter-is-emergent) 3.4 ("Binding is a periodic
orbit of the meeting rule"), with 3.3, 3.5, 3.17, 3.19, 3.20, 3.28 and 5.2.
This page states the rule in the model's language, derives the closure
condition by following the declared tables, defines the smallest loop, the
unit-square electron, as a world file (`examples/nature/ring.json`, with its
dispersing control `ring_open.json`), and names what the feature removes.
Design only: no engine code changes with it. The expected integers of the
future `tests/test_loop_binding.py` are pinned in
[test expectations](TEST_EXPECTATIONS.md#loop-binding) before any run, as
Highlights 5.5 requires; the engine of `main` was run once on the two worlds
only to check whether it already holds the ring
([section 10](#10-what-todays-engine-does-with-the-ring)). The
implementation follows feature 8b (features 12, 8c and 2b landed on
2026-09-17).

## 1. The rule

A ray never stops. Every ray moves one Link per interval, and a Node it
merely crosses hosts no event (Highlights 3.3). "Bound" therefore does not
mean "resident"; it means "back at the same place in the same state".

A **bound group** is a set of rays that is a periodic orbit of the Node's
law of Highlights 5.2: there is a period T such that running the law for T
intervals maps the set to itself, every ray again at the same Node with the
same heading, the same amount and the same phase modulo the circle, so that
the same meetings happen again and the pattern repeats forever. Nothing
holds the rays: at every meeting the ordinary coupling table of the
families present gives the outputs, the outputs leave, walk their Links,
meet again, and the table reproduces the rays that entered. A set of rays
whose meetings do not reproduce them is not bound: some output leaves the
pattern and does not come back, which is dispersal.

There is no binding rule and no register. The only declared thing is the
table (Highlights 3.26): a binding coupling of the
[catalog](CATALOG.md) is an ordinary `ray_interactions` rule with outputs
([meetings with outputs](SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1))
whose loop closes, and whether a given content closes under it is a
computation, not a declaration. A group lives on a **ring** of Nodes, the
closed path its rays walk; its size is the ring, its content is the sum of
its rays' amounts, and that content is its mass (Highlights 3.4, 3.28).

## 2. The smallest loop: the unit square

On the cubic lattice a closed path of Links has an even number of Links and
the shortest is the unit square, four Nodes and four Links. Take the
corners in the plane z = 5

```text
P0 = (5, 5, 5)   P1 = (6, 5, 5)   P2 = (6, 6, 5)   P3 = (5, 6, 5)
```

and two senses of circulation: the **R** sense P0 -> P1 -> P2 -> P3 -> P0
(headings +X, +Y, -X, -Y, Ports 0, 2, 1, 3) and the **L** sense
P0 -> P3 -> P2 -> P1 -> P0 (headings +Y, -X, -Y, +X, Ports 2, 1, 3, 0).

**Timing.** A ray of the R sense that is at a corner at tick t is at the
next corner at tick t + 1. Two rays of the same sense never meet; a meeting
is one R ray and one L ray at one corner in one interval. With one ray per
sense the two meet only every other interval, at opposite corners
(P0 -> tick 2 at P2 -> tick 4 at P0), and in between each is alone at a
corner where, with no partner, no rule fires and it crosses straight out of
the square. So the smallest closed set is **four rays**: two of each sense
starting at opposite corners (R and L at P0, R and L at P2), which meet at
two corners in every interval (P1 and P3 at odd ticks, P0 and P2 at even
ticks). The picture of Highlights 3.4, every corner meeting every interval,
is **eight rays**, one of each sense at every corner: two four-ray rings
interleaved, the even one and the odd one, whose meetings never mix. The
world file has the eight; the four-ray ring is pinned as its own case.

**The corner coupling.** At a corner the R ray arrived along one edge and
the L ray along the other. The table of Highlights 3.4, "two rays that leave
through each other's Ports", is: each input's content leaves through the
Port the other input came in by, with its own amount and phase. The Port a
ray came in by is the Port opposite its heading, so this is an outputs rule
in today's schema, with exactly these keys:

```json
{"name": "corner", "participants": [{"type": "electron"}, {"type": "electron"}],
 "outputs": [
   {"field": "electron", "amount": {"of": 0}, "heading": "reversed", "input": 1, "phase": {"of": 0}},
   {"field": "electron", "amount": {"of": 1}, "heading": "reversed", "input": 0, "phase": {"of": 1}}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}}]}
```

`"heading": "reversed"` with `"input": 1` is the negation of input 1's
heading, the Port input 1 came in by; `"amount": {"of": 0}` and
`"phase": {"of": 0}` are input 0's amount and phase, read modulo the phase
steps; every output carries its source input's advance (the family's rate).
Output 1 is the same with the roles exchanged, so the rule is symmetric under
the exchange of its inputs and it does not matter which resident ray the
engine takes as input 0 (the resident rays of a Node are in merge-key order,
heading index first). Geometrically, at every corner of the square the
other's entry Port is the next edge of one's own sense: the R ray turns a
quarter turn one way and the L ray a quarter turn the other, each staying on
the ring. At a head-on meeting on a longer ring's side (feature 14's
general ring, section 3) "the other's entry Port" is one's own heading, so
there the rule lets the rays through unturned, a new event with the same
lines. The charge invariant `charge x amount` is appended by the engine; the
declared invariant is the amount. Momentum is not declared as an invariant,
and cannot be: a quarter turn of each ray changes their momentum by
`(2a, 2a, 0)` at P0 and by the same magnitude at every corner (section 8),
which today the spatial law books as the meeting's source of the momentum
field, as it books the momentum a steering split moves. This is the
**Port form** of the corner table, `port` in the pinned cases.

**The world.** `examples/nature/ring.json`: board 12 x 12 x 11, open,
`link_ticks` 1, `phase_bits` 3 (N = 8), 16 ticks; the `electron` family of
the catalog (charge -3) with rest rate 2 (section 3 says why); eight lamps,
two at each corner, one per sense, each holding 1 quantum and emitting it
once, funded, on its sense's heading out of that corner at phase 0, keeping
the recoil (`recoil_field` `momentum`); the one rule `corner` above. The
emissions happen in the cycle of tick 0, so after tick 1 every corner holds
an R ray and an L ray, and from the cycle of tick 1 every corner meets every
interval. Content 8, ring 4.

## 3. Closure as integer equalities

Follow the tables. The state of a ray is (Node, heading, amount, phase),
and the loop closes in one circuit when every ray, after walking the L
Links of the ring and passing its corners, is back with the same four. Each
condition is an equality of bounded integers.

1. **Presence.** Whenever a ray reaches a corner, a ray of the other sense
   is there: on the unit square, two rays per sense at opposite corners, or
   four per sense, one at each corner (section 2). A corner with one ray
   fires no rule and that ray leaves the ring.
2. **Headings.** The corner table sends each output through the other's
   entry Port; on the unit square that is the next edge of its own sense at
   every corner, so the headings are reproduced by geometry, for every
   amount and every phase.
3. **Amounts.** Under the Port form each output carries its own input's
   amount: reproduced for every amount. Under a table that splits by the
   phase difference the amounts must satisfy the split, item 6.
4. **Phase.** A ray's phase advances by its family's rest rate r at every
   Link and nowhere else: a meeting output takes its input's phase
   (`{"of": i}`, offset 0), and the meeting takes no interval of its own,
   since the outputs depart in the cycle in which the inputs arrived. After
   one circuit of L Links the phase is `phi + L r` modulo `N = 2^phase_bits`.
   Closure in one circuit is therefore

   ```text
   L r = 0  (mod N)          unit square, L = 4:   4 r = 0  (mod N),  r = 0 (mod N / 4)
   ```

   At N = 8 the rates that close the unit square in one circuit are r = 0,
   2, 4, 6. The catalog's electron, r = 1, does not: its phase returns after
   two circuits. That is not dispersal. Nothing at a corner reads the
   absolute phase, so the orbit is still periodic, with the state period

   ```text
   T = L x N / gcd(L r, N)   intervals      (r = 1, N = 8, L = 4:  T = 8;  r = 2:  T = 4)
   ```

   and the pattern of Nodes, headings, amounts and phase differences has
   period L in every case. `ring.json` declares r = 2 so that the pinned
   state repeats after one circuit; the r = 1 ring is pinned as the `slow`
   case, period 8, nothing lost.
5. **The phase difference at a corner is a constant of the motion.** Every
   ray of one family advances by the same r per Link, so the difference
   between any two rays of the ring never changes: the difference d the
   corner table reads is set by the emission phases and is the same at every
   later meeting of the same pair. On the eight-ray ring corner k at tick t
   meets R ray k - t with L ray k + t (indices modulo 4), so with all R rays
   at one phase and all L rays at one phase, d is the same at every corner
   at every tick. "The difference at every corner must return to itself"
   holds by itself for one family. A rest rate can be read at a meeting
   only against a ray that did not walk the loop with the group: a ray of
   another family in a composite, or the group's own field, whose rays have
   rate 0 and carry the phase at their release (section 6). In a ring of
   one family under a Port-form or a steering corner, the rate sets the
   clock (item 4) and nothing else.
6. **The steering form.** With the catalog's `born_steering` at the corner,
   the ordinary table of two rays of one family meeting (Highlights 3.3, the
   shared content steered between two candidate Ports by the phase
   difference), the two candidate Ports being the two entry Ports:

   ```json
   {"field": "electron", "amount": {"of": "sum", "index": "phase_difference"},
    "heading": "reversed", "input": 1, "phase": {"of": 0}},
   {"field": "electron", "amount": {"rest_of": 0}, "heading": "reversed", "input": 0, "phase": {"of": 1}}
   ```

   the table output takes `floor((a_0 + a_1) x T[d] / N)` of the shared
   content through input 0's turning Port and the rest output the rest
   through input 1's. Input 0 is the resident ray with the lower heading
   index, which on the square is the L ray at P0 and P2 and the R ray at P1
   and P3, so the sense that takes the table's share alternates around the
   ring. The amounts are reproduced at every corner only if
   `floor((a_R + a_L) T[d] / N) = a_R = a_L`, that is `a_R = a_L` and
   `T[d] = N / 2`: **d = N/4 or 3N/4**, the two senses a quarter turn apart
   (d = 2 or 6 at N = 8), any equal amounts. At d = 0 one output takes the
   whole content and the other is no ray; at d = N/2 the other; either way
   the next corner has one ray and the ring disperses (section 4). At the
   other d the content moves between the senses from corner to corner and
   the pattern re-closes with alternating amounts or disperses by the
   floor; the reference table gives no further closing d at equal amounts.
   This is the **Born form**, `born` in the pinned cases: `ring_open.json`
   declares it with the senses in phase (d = 0) and disperses;
   `quadrature`, the same with the L lamps at phase 2, closes with the same
   Nodes, headings and amounts as `ring.json`.

**A general ring.** A rectangle of a by b Links has L = 2 (a + b) and four
corners at arc lengths 0, a, a + b, 2a + b along the ring. A ray of one
sense reaches corner c at the ticks when its arc position is that of c, and
a ray of the other sense must be there: the set of arc positions of the L
sense must contain `2 s_c - s` for every corner c and every R position s,
and symmetrically. The set closed under these reflections through the
corners is the set of multiples of `2 g`, g = gcd(a, b): the ring closes
with `(a + b) / g` rays per sense, spaced 2g Links apart, every one of
them at a corner whenever any is (for the unit square, 2 per sense; for the
2 x 2 square, also 2 per sense, meeting at two corners in every second
interval and crossing the side Nodes alone in between). Between two corners
the rays of the two senses pass each other on the Links and never share a
Node when 2g divides the spacing, so no side meeting occurs. The phase
closure is `L r = 0 (mod N)`: at the catalog's r = 1 and N = 8 the smallest
rectangles that close in one circuit have L = 8 (the 2 x 2 square, the
1 x 3 rectangle), which is the loop form of the standing-wave condition
that the helium-ion computation stated for an orbit
(`8 r k = j N`, [README](../examples/nature/README.md#the-orbit-computed-what-a-stable-closed-orbit-needs)).
Loops with more than four corners obey the same reflection condition
corner by corner.

## 4. When it does not close

Dispersal is not a rule; it is what a ray does with no partner. A corner at
which only one ray of the layer is resident fires no rule, and the ray
crosses on its heading, off the ring, and walks to the boundary (an open
world books it as escaped; a periodic one lets it wander). The ways a ring
fails to close under today's tables:

- **Presence.** Fewer rays than the ring needs (seven on the unit square,
  say): the corner with one ray lets it through, its downstream partners
  then arrive alone, and within L intervals every ray has left.
- **The steering table at a difference that does not close.** Under the
  Born form at d = 0 the whole shared content of every corner leaves
  through one Port: after the first meeting each corner sends 2a one way,
  the other sense is empty, the next corner holds one ray of 2a, and it
  crosses. `ring_open.json` is this control: the same eight rays, the same
  lamps and phases, the corner table the catalog's Born table; after tick
  2 four rays of amount 2 walk +Y and -Y out of the square and by tick 8
  all eight quanta have left the open board.
- **A rate or an amount, under the Port form: never.** The Port form
  reproduces every amount and reads no phase, so a ring under it holds any
  content at any rate, with a longer clock when `L r` is not 0 modulo N.
  This is the loop counterpart of the held-ray rule of feature 8, which
  holds any content: the Port form alone gives no ladder. The pinned `slow`
  case (r = 1) states it as integers, and the implementation must not read
  the Port form as the whole of feature 14.

## 5. Mass and clock

- **Content.** The mass of a bound group is its content, the sum of the
  amounts of its rays (Highlights 3.4, 3.28): 8 for `ring.json`, 4 for the
  four-ray ring. It is exact at every tick, since a corner meeting keeps
  every family's stock.
- **The ring and its period.** The ring is the closed path, L Links; one
  circuit takes L intervals, and the state repeats after
  `T = L N / gcd(L r, N)` intervals (section 3, item 4), which is L when
  the loop closes in one circuit.
- **The clock.** Every ray's phase advances r per interval, on the ring as
  on a straight line (Highlights 3.3: the rest rate is the mass as a clock),
  so the group's clock is the phase of its rays, and light the group emits
  carries that phase. The interim held group advanced its phases once per
  interval while resident; the loop advances them once per Link, which is
  the same count, because a ray walks one Link per interval.
- **Content per period.** The content passing a corner per interval,
  `rho = C / L` (2 for `ring.json`: two rays of 1 at every corner every
  interval; 1 for the four-ray ring, two rays every second interval), is
  the group's rate in the sense of Highlights 3.28: it is what a ray that
  crosses the ring meets, and the delay such a ray suffers is the `delay`
  output of its meeting with the ring's rays, at most one meeting per corner
  it crosses, its size the table's product of the content met and the
  declared entry. Under the interim form the same thing was one declared
  number, `ray_delay` k, a Node-wide wait for every matter ray arriving at
  the group's Node; under the loop there is no such number: k is what the
  visitor's table gives per corner, and a group of larger content delays
  more because its corners carry more content, not because a register says
  so.
- **Speed.** A group at rest has fixed corners; Highlights 3.28's speed 1/k
  is corners shifting one Link per k intervals, section 8.

## 6. The field of a loop

Every ray of the ring releases its field at every Node it departs from, as
any ray in motion does (Highlights 3.5;
[released field](SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1)):
one field ray per Port heading except its own, five, each of amount
`floor(a x n / d)` with the ray's phase, booked as a source. Per corner per
interval that is ten releases on the eight-ray ring, forty per interval for
the group; at the catalog's ratio `[1, 4]` an amount of 1 releases nothing
(the floor is 0), an amount of 4 releases 1 per heading. Of each ray's five
headings one lies along the ring: the R ray leaving P0 on +X releases on
+Y, the edge to P3, and the L ray leaving P0 on +Y releases on +X, the edge
to P1; so two field rays per corner per interval run along the edges and
reach the neighbouring corners in the next interval, where the ring's rays
are. Only after a change of trajectory can a ray cross field it released
earlier (Highlights 3.5), and on a ring every corner is one: the ring meets
its own field. With feature 12 the released rays spread from the next Node
and the field fills the board around the ring, falling with distance by the
lattice's path counting. The six-heading release of a held ray, which
existed only because a held ray occupied no line ahead of it, goes with the
held form. What the ring does when it meets its own field is the coupling
of the electron with light (the catalog's `electron_field_turn`, whose
strength table experiment A5 writes): under today's whole turn the ring's
ray would leave on the field ray's heading, off the ring; the ring worlds
therefore declare no released field, and the closure of a ring with its
own field is the open point that the ladder needs (section 7). The
field-and-recoil bookkeeping of the corners is the same statement from the
other side: the momentum the quarter turns move, `(2a, 2a, 0)` per corner
per interval on the unit square, is what the group's field would carry and
return, and today it is booked as the meeting's source of the momentum
field (its four corners summing to zero, so the world's momentum stays
exact).

## 7. The ladder, and how A10 counts it

Hypothesis 12's ladder is, under feature 14, the set of (content, phases,
L) that close a loop under the catalog's binding table
([HYPOTHESES.md](HYPOTHESES.md#12-one-mass-ladder-and-the-composite-spectrum-from-binding)).
The counting procedure of experiment A10, a catalog fit with no board:

1. Enumerate the rings: rectangles a x b (and longer lattice loops corner
   by corner), L = 2 (a + b), with the ray placement of section 3
   (`(a + b) / gcd(a, b)` rays per sense, spaced 2 gcd(a, b)).
2. For each ring and each family, enumerate the amounts of the rays (up to
   a declared bound) and the phase differences between the senses (N
   values), the emission phases being the free initial data.
3. Apply the corner table to one circuit: the outputs at every corner by
   `convert_values`, exactly as the engine does, and keep the sets for
   which every corner reproduces its inputs (headings, amounts, phases
   modulo N).
4. A kept set is a rung: content C, clock L, rate r, difference d. Record
   the contents that occur, per L, as the ladder; the ratios of the
   contents of the kept sets are the mass ratios the ladder predicts, to
   be set against the measured ratios as A10 states.

What the count gives under today's tables, by section 3: under the Port
form every (C, r, L) with the presence condition is kept, no ladder; under
the Born form every even C at d = N/4 or 3N/4 with equal senses, no ladder
in content either; the only integer conditions are the presence condition
on the number of rays and `L r = 0 (mod N)` on the ring's length. A content
ladder appears only when the turn at a corner is not declared whole by a
Port but produced by content: the ring's rays meeting the group's own field
rays (section 6), whose amount is a floor of the content times the release
ratio, under a table whose turn is proportional to what is met (the delay
table of feature 8, spent as a Link per modulus, or the quarter turn of
feature 8b), so that a circuit closes only for the contents whose field
gives exactly one quarter turn per corner; the helium-ion computation
states that condition for an orbit around a proton (`floor(A t_p / u) =
N` under a delay table). A10's procedure is written to run over any corner
table, and the model owner's binding entries of the catalog
(`electron_proton_binding`, `quark_binding`, `pauli_exclusion`) are the
tables it will read once they are written as corner tables.

## 8. Motion of a loop as a whole

Highlights 3.28: a group that moves one Link every k intervals has speed
1/k, and under feature 14 that motion must be its corners shifting, not a
register on a Node. What a shift of the unit square by one Link along +X
takes, in the language of the corner table: in the shift interval the R ray
at P1 must go straight (+X, to the new corner) instead of turning, the L ray
at P1 must return the way it came (+Y, since the old P1 is the new P0 and
the L sense leaves it on +Y), the rays at P0, which drops out of the
square, must both head +X, and the rays at P2 and P3 correspondingly; and
after the shift the new corners P1' = (7, 5, 5) and P2' = (7, 6, 5) receive
rays from one side only, so a complete ring cannot re-form in one interval
and a moving loop is not the resting loop plus a step. A moving loop is a
different periodic orbit: a pattern of rays that repeats after k intervals
one Link further on. Three things would have to hold, none of them
established here:

- the corner table must be able to select the shift outputs (straight on,
  or back the way one came) and the turn outputs at the same table, so it
  must read something that differs between the front and the back of the
  moving loop; in the model that can only be the phase difference, so a
  moving loop carries a phase pattern around its ring, the model's form of
  the de Broglie wave, and the table entries for that pattern are catalog
  declarations to be written;
- the momentum of the pattern, amount x heading summed over its rays, must
  equal the group's momentum, the corner bookings of section 6 no longer
  summing to zero in the shift interval, and the balance must be carried
  by the group's field rays (the recoil of Highlights 3.14), which is the
  same open closure as the ladder's;
- the count of rays and the timing must close at the shifted square, which
  section 3's reflection condition states for a resting ring and nobody has
  stated for a moving one.

Until then the register-driven motion of feature 8c is the interim form,
and experiment A14 (time dilation from transit) waits: whether a moving
loop's rays spend more intervals between meetings than a resting loop's is
exactly what its orbit will show.

## 9. The interim forms, and what feature 14 removes

| Interim form (features 8, 8c) | Loop form (feature 14) |
| --- | --- |
| A bound group is rays held at one Node by a `ray_interactions` rule without outputs whose assignments set `delay` 1 ([binding](SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1)); the rule fires again every interval, the group's tick, an event with no departure | A bound group is rays in motion on a ring whose corner meetings, by an ordinary outputs rule, reproduce them; every meeting is an ordinary event with departures; a held group is the loop of length 0, which the rule "a ray never stops" excludes |
| Content: the held amounts; clock: each phase advanced once per interval while held | Content: the ring's amounts; clock: each phase advanced once per Link, the same count |
| `ray_delay` k on the binding rule: every matter ray arriving at the group's Node waits k intervals, one Node-wide register `bound_delay` | No register: a visitor meets the ring's rays at a corner and its delay is the `delay` output of that meeting, per corner crossed (section 5) |
| A held ray releases its field on all six headings (it occupies no line ahead of it) | Every ring ray releases on five headings at every Node it departs, as any ray in motion (section 6) |
| `bound_group` reads the group from the Node's rays; the snapshot lists `bound_groups`; the Node publishes `bound_tick` | Nothing at a Node names the group; a group is a set of rays that repeat, read from the record by a reader (a Renderer) that looks for the repetition, which is tooling to be written with the feature |
| Motion (feature 8c): a momentum register with three accumulators on the group, `group_step` one Link when a whole content has accumulated, `bound_group_step`, `momentum_table` on the binding rule pushing the register, `carry_rays` | Motion is the corners shifting, a different periodic orbit (section 8); a field ray that meets a ring ray is met by the ordinary table at that corner and returned as the recoil, and its momentum enters the pattern, not a register |
| Unbinding: an earlier outputs rule naming a bound participant and an arriving ray | The same: an arriving ray meets a ring ray at a corner by the table declared for the families present, and its outputs leave the ring or join it; nothing else creates or destroys a group |

When feature 14 lands, the following are removed from the engine and the
schema, with a dated migration note: the binding form of a rule without
outputs (assignments of `delay` 1 as a hold), `ray_delay`, `bound_delay`,
`bound_group`, `bound_groups`, `bound_tick`, the six-heading release of a
held ray in `release_field`, and all of `bound-group-motion-v1` (the
register, `group_step`, `carry_rays`, `bound_group_step`,
`momentum_table` on binding rules, the ledger's reading of a group by its
register, `SpatialPacket.group`). What stays: the outputs rule and its
`delay` output as an output-clock wait (Highlights 3.28), the delay table
and the lag register (feature 8b), the released field with its spreading,
the external body with its own register (a declaration, not matter,
Highlights 3.19), and the Node's five-step law, which the loop uses
unchanged. The catalog's `binds` entries become corner tables, and the
nature examples that use the held form (E1 to E3, the screen) are rewritten
as loops or retired with their dated records kept.

## 10. What today's engine does with the ring

The two worlds were run once on `main` at `c21e03e` (2026-09-17), after the
expectations were pinned, to learn where the implementation starts. The
engine holds the ring: under the Port form every corner meets every
interval from the cycle of tick 1, the outputs leave on the ring, and the
state after tick t + 4 is the state after tick t for every t from 2, the
phases 2t modulo 8, the event stamps those of the corner each ray last
left, content 8, momentum (0, 0, 0), every ledger line balanced and
`conserved_at_every_completed_tick` true; the record's `bound_groups` is
empty and no `bound_tick` is written, since nothing is held. The control
disperses as computed: four rays of 2 leave the square after tick 2 and the
open board by tick 8, escaped 8. The rate-1 ring, the four-ray ring and the
quadrature ring agree with the hand computation line for line as well (the
[expectations](TEST_EXPECTATIONS.md#loop-binding) carry the engine's column
beside the hand column; the two are identical). So no step of the Node's
law fails on a loop today, and the implementation's starting point is not a
repair but the removal of section 9 with the record's reading of a group,
the catalog's binding entries as corner tables, and the closure of a ring
with its own field (sections 6 and 7).

## 11. Open points

- The self-field closure: the coupling of a ring's rays with the group's
  own field rays, from which alone a content ladder can come (section 7),
  and the momentum of the quarter turns, booked as a source today, carried
  by those field rays instead. A5's strength table and 8b's quarter turn
  are the declarations it waits for.
- A moving loop: the phase pattern that selects a shift and the corner
  entries that read it (section 8); until then feature 8c is the interim
  form of motion and A14 waits.
- The reading of a group from the record: what a Renderer draws as matter
  once nothing at a Node names a group.
- Two loops that share a corner, and a ring ray meeting an arriving ray of
  another family: the ordinary layers and declared order decide, but no
  world has been written.
- The catalog's binding entries (`electron_proton_binding`,
  `quark_binding`, `pauli_exclusion`) as corner tables, and the nature
  examples E1 to E3 in loop form.
- The rate of the world's electron: the catalog's r = 1 closes the unit
  square in two circuits at N = 8; whether the electron is the unit-square
  loop at all, or a longer ring, is A10's to decide with the ladder.
