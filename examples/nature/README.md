# Two events of nature in the engine's language

Nine world files that show, on the one generic engine and with the rules
that exist today, (A) a photon absorbed by an electron at rest, (B) a nucleus
split by a high-energy photon, with a low-energy photon that does not split
it as the control, (C) the photon of (A) carried in the group while its
clock runs and then emitted on a new heading, the group back in its ground
state, (D) the helium ion, a nucleus of charge +2 with one electron,
[below](#the-helium-ion-one-electron-at-a-nucleus-of-charge-2), (F) the
ring, an electron at rest as a loop of rays on a unit square, with the
control that disperses, the demonstration of feature 14,
[below](#the-ring-an-electron-at-rest-as-a-loop), (G) the worlds of
experiment A5, two charged rays passing each other through their spreading
fields, in `a5_coulomb/`,
[below](#a5-coulombs-law-through-the-spreading-field), and (H) the helium
ion again, on the engine with the field spreading and the momentum turn, with
the axis-only control,
[below](#the-helium-ion-with-the-field-spreading-and-the-momentum-turn),
and (I) the screen of (E) with the ring of (F) as its source, rays of amount
4 radiating their light on seven marks,
[below](#the-screen-with-a-loop-the-ring-radiating-on-seven-marks),
and (J) the worlds of experiment A5s, two charges at rest as external
bodies, the force between them through their spreading fields, in
`a5_static/`,
[below](#a5s-coulombs-force-law-between-two-charges-at-rest),
and (K) the worlds of experiment A12, Malus's law and the three-polarizer
chain, a polarized beam through polarizer bodies, in `a12_malus/`,
[below](#a12-maluss-law-and-the-three-polarizer-chain).
(E), the field of an electron at rest on a screen of seven Detector marks,
the eye view's first picture, ran under the interim held form and is retired
with its records kept,
[below](#the-screen-the-field-of-an-electron-at-rest-on-seven-marks).
(A) to (F), (H) and (I) are demonstrations under
[Highlights](../../docs/HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions)
5.5: research runs made once, recorded with their fingerprint in the
[experiments register](../../docs/EXPERIMENTS.md#e-demonstrations-of-events)
((E) in its section here), never repeated as tests, and (G), (J) and (K) are
confrontation runs of section A of the register. Nothing here is a law of
nature; every number is a declaration written before the run.

Since 2026-09-17 (feature 14, binding as a loop, `loop-binding-v1`;
[binding as a loop](../../docs/SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1),
[loop binding](../../docs/LOOP_BINDING.md)) matter is a loop: a bound group
is rays in motion on a ring of Nodes whose corner meetings, under an
ordinary outputs rule, reproduce the rays that entered them, and nothing
holds. (A), (B) and (C) were first written under the interim held form of
feature 8 (a rule without outputs holding its rays at one Node with a
`ray_delay` wait) and rewritten the same day as loops on the unit square of
(F); their first records stay in the register as the records of that form.

The rays are selected from the [catalog of nature](../../docs/CATALOG.md)
(`light`, `electron`, `proton`, `neutron`, with the catalog's charge unit e/3
and the electron's rest rate 1); the couplings that make the events of (A),
(B) and (C) are the worlds' own declarations, since the catalog holds no
photon-absorption and no photofission coupling yet, and the rest rates of the
proton and the neutron, undecided in the catalog (A10, hypothesis 12), are set
to 1 there for the picture only. In (D) light is the field of the nucleus and
of the electron (Highlights 3.5: light and the field of a charge are one
family), declared once per releaser as the catalog says, and the attraction
is the world's own rule standing in for the catalog's open sign rule
(`opposite_charge`, A5).

## Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| A photon of energy a | A ray of the family `light`, amount a (`emissions[].amount`), rest rate 0 (`kerengonen.phase_advance` 0), charge 0, one Link per interval; its phase is the emitter's clock at emission and never advances | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1); Highlights 3.3 |
| An electron at rest | The ring of (F): eight `electron` rays (rest rate 1, charge -3) of amount 1 on the unit square P0 = (5,5,5), P1 = (6,5,5), P2 = (6,6,5), P3 = (5,6,5), one of each sense at every corner in every interval, turned at every corner by the outputs rule `corner` (each input's amount and phase through the Port the other came in by); its content is the sum of the amounts, 8, and its clock is each phase advancing by the rest rate at every Link; nothing is held | [Binding as a loop](../../docs/SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1); Highlights 3.4, 3.28 |
| The photon arrives | The light ray reaches a corner in an interval in which the corner's two electron rays are there (every interval on the eight-ray ring) and is met by the table declared for the three families present | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1); Highlights 3.4 |
| Absorption | The corner table `absorb` over `[electron, electron, light]`, declared before `corner`: the two electron rays turn as at every corner and the light leaves through the same Port as one of them, so the photon joins the loop. The literal conversion of the light's amount into electron content is refused by two generic rules (see Limits) | [Binding as a loop](../../docs/SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1); Highlights 3.4 ("its outputs leave the ring or join it") |
| The excited electron | The ring with the photon in it: content 8 + 3 (the record's reading of the group: content 11, electron 8 and light 3), the photon walking one edge of the square with the ring's rays and meeting the corner's pair at both ends every interval, its phase constant while the electron phases keep advancing | [Binding as a loop](../../docs/SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1); Highlights 3.28 (mass is content) |
| Emission | The corner table `emit` over `[electron, electron, light]`, declared before `absorb` (rules fire in declared order and a ray one rule used is not available to the next in that interval), fired by the ring's clock: its guard `"when": {"op": "eq", "args": [{"field": "phase", "participant": 0}, 1]}` is true in the interval the electron phase reads 1 at the corner where the light is. Its outputs are the electrons' turns and the light leaving through Port 4 (+Z, off the square, so it reads as emission) with the group's phase at emission (`"phase": {"of": 0}`, Highlights 3.3: the frequency of light is the rate of its emitter's clock) | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1); Highlights 3.4 |
| Lifetime of the excited state | Declared and deterministic: the intervals until the electron phase reaches the guard's value (five here, from the absorption at phase 4 through 5, 6, 7, 0 to 1). The half-life draw of Highlights 3.26, a decaying group as a source and a source as a Detector drawing at each tick, is not in the engine: a Detector mark draws on arrivals through Ports only; under the loop the draw would be at the corner meeting of the group's rays. That draw is the missing rule for a random lifetime | Highlights 3.26; [Detector mark](../../docs/SPATIAL_FIELDS.md#detector-mark-detector-mark-v1) |
| Recoil of the absorption and the emission | Momentum by heading: the photon arrives with (0, 0, a) and leaves the corner along the ring, so the corner books the difference as its source of the momentum field, as it books the quarter turns of the electrons every interval (the recoil these bookings stand for belongs to the group's own field, open); at the emission the light leaves with (0, 0, a) again and the sources return to zero. The world's momentum line is exact at every tick | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) ("Momentum of a split"); Highlights 3.14, 3.16 |
| A two-body nucleus | The four-ray ring of the design: a `proton` ray (charge +3) circulating one way from two opposite corners and a `neutron` ray (charge 0) the other, amount 6 each, meeting at two corners in every interval under the corner table `strong` over `[proton, neutron]`; content 24, period 8 at rest rate 1 | [Loop binding](../../docs/LOOP_BINDING.md#2-the-smallest-loop-the-unit-square); Highlights 3.4 |
| Photofission | The outputs rule `photofission` over `[proton, neutron, light]`, declared before `strong`: each of the three leaves on its own heading (`"same"`), so the photon above the threshold stops the corner's turn and the pair flies apart, momentum exact by heading; the other pair, its partners gone, reaches its next corners alone and crosses off the ring: the group disperses | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1), [dispersal](../../docs/LOOP_BINDING.md#4-when-it-does-not-close); Highlights 3.4 |
| The fragments | The rule's outputs: each a fresh trajectory with `steps` 0, stamped with the event's Ports and shares | [Ray state](../../docs/SPATIAL_FIELDS.md#ray-state-ray-event-state-v1) |
| The threshold | The rule's guard, `"when": {"op": "gt", "args": [{"field": "amount", "participant": 2}, 3]}`: the rule fires only when the light's amount exceeds 3, that is, is at least 4. The schema already has this amount condition, read at the meeting and nowhere else, so no new key was added. A false guard is no interaction: `strong` turns the pair and the light crosses | [Local updates and expressions](../../docs/DISTURBANCES.md#local-updates-and-expressions) (`gt`); [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) ("A false guard leaves the group untouched") |
| The control photon | A second light lamp of amount 2, below the threshold, arriving first: it meets the pair at two corners, crosses both unchanged and walks on; the ring stays | [Layers](../../docs/SPATIAL_FIELDS.md#layers-ray-layers-v1), Highlights 5.1 |
| Energy | The amount; the declared invariant `energy` (`{"field": "amount"}`), exact as a sum over inputs and outputs | Highlights 3.15 |
| Momentum | Amount times heading, the declared invariant `momentum` of `photofission`, exact component by component; every lamp keeps its recoil in its `momentum` register (`recoil_field`); the corner turns are booked as each corner's source, so the world's momentum equals its sources at every tick and the runner's `conserved_at_every_completed_tick` is true | Highlights 3.14, 3.16 |
| Charge | The family's charge per quantum in thirds of e; `charge x amount` summed over a meeting's rays is appended by the engine to every rule's invariants | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1) |
| Speed | One Link per interval for every ray, light and matter alike; matter at rest is a loop whose corners stay put, and a slower group would be one whose corner table declares a `delay` output, an output-clock wait per corner | Highlights 3.28 |
| An event | A change of trajectory leaving a meeting; in the viewer a marker at the Node. A crossing is no event | [Ray-event model](../../docs/RAY_EVENT_MODEL.md#1-definitions) |
| The group in the record | Nothing at a Node names a group: the ray viewer's extractor reads the rays that keep meeting each other at their corners, and when their states recur with a period it reports the group's ring, content, period and clock (`groups` in the run document) | [Ray viewer](../../tools/ray_viewer/README.md); Highlights 3.4 |

## absorption.json, tick by tick

Board 12 x 12 x 11, open, `link_ticks` 1, `phase_bits` 3 (N = 8), 24 ticks.
Lamps: the eight corner lamps of `ring.json` (amount 1, phase 0, rest rate 1
here, the catalog's); one light lamp at (5, 5, 0) heading +Z, amount 3.
Rules in order: `absorb` (the corner table over `[electron, electron,
light]`), then `corner`. The ticks below are the state after the tick; a
ray is (heading, amount, phase, steps).

| Tick | What is on the board |
| --- | --- |
| 1 to 4 | The ring as in `ring.json` with phase t mod 8: every corner holds one ray of each sense and `corner` fires at all four every interval; the light walks (5, 5, t) |
| 5 | The light (+Z, 3, 0, steps 5) at P0 with the corner's two rays (phase 5); in the cycle that follows `absorb` fires: the L ray leaves through +Y with the light, the R ray through +X, the event's Ports +X and +Y with shares 1 and 4 |
| 6 | The light at P3 (heading +Y, steps 1, phase 0) with the corner's pair; `absorb` fires there, sending it back through -Y with the R ray |
| 7 to 24 | The photon walks the edge P0-P3, at P0 after the odd ticks and at P3 after the even ones, met at both ends every interval; the six other rays turn as before; the ring's phases t mod 8 |

At every tick: totals electron 8, light 3, the charge ledger electron -24
(= -3 x 8), every line of the audit balanced,
`conserved_at_every_completed_tick` true; the momentum the photon's turns
move is booked at the corner as the electrons' turns are, (0, 3, -3) in the
world and its sources after the odd ticks from 5 and (0, -3, -3) after the
even ones. The record reads one group: ring P0, P1, P2, P3, content 11
(electron 8, light 3), period 8, clock electron 1 and light 0, from tick 5
to tick 23.

## absorption_emission.json, tick by tick

The board and lamps of `absorption.json` with the light lamp at (5, 5, 1)
and amount 4, 32 ticks. Rules in order: `emit` (the corner table with the
guard on the electron phase and the light through +Z), `absorb`, `corner`.

| Tick | What is on the board |
| --- | --- |
| 1 to 3 | The ring; the light walks (5, 5, 1 + t) |
| 4 | The light (amount 4) at P0 with the pair, the electron phase 4; the guard of `emit` reads 4 as false and `absorb` fires: the photon joins the ring through +Y |
| 5 to 9 | The photon walks the edge P0-P3 (P3 after the odd ticks, P0 after the even), the electron phases 5, 6, 7, 0, 1: the group's content 11 while its clock runs |
| 9 | In the cycle that follows, at P3, the electron phase reads 1: `emit` fires; the electrons turn as at every corner and the light leaves through +Z with phase 1, the event's Ports +X, -Y and +Z with shares 1, 1 and 4 |
| 10 | The light at (5, 6, 6) heading +Z, phase 1, steps 1; the ring in its ground state, content 8, its phases 2 |
| 11 to 14 | The light walks to (5, 6, 10); the ring turns on |
| 15 to 32 | The light has left the board (escaped 4); the ground ring, which the record reads as one group of content 8, period 8, clock 1, from tick 10 |

At every tick: totals electron 8, light 4 in the world with the escaped, the
charge ledger electron -24, every audit line balanced,
`conserved_at_every_completed_tick` true; the momentum the photon brought
in, (0, 0, 4), is booked at the corners while it is in the ring and leaves
with it, the world's sources reading (0, 4, -4) from tick 5 and (0, 0, 0)
from tick 10. Photon in, carried five intervals, photon out on a new heading
with the group's phase, the ring back in its ground state.

## photofission.json, tick by tick

Board 26 x 26 x 11, open, `link_ticks` 1, `phase_bits` 3, 32 ticks. Lamps:
a proton lamp and a neutron lamp at P0 = (20, 20, 5) emitting +X and +Y,
and one of each at P2 = (21, 21, 5) emitting -X and -Y, amount 6 each, phase
0 (the four-ray ring, two per sense at opposite corners); the low light lamp
at (0, 20, 5) heading +X, amount 2; the high light lamp at (20, 0, 5)
heading +Y, amount 6. Rules in order: `photofission` (the outputs rule with
the guard, threshold 4), then `strong` (the corner table over `[proton,
neutron]`).

| Tick | What is on the board |
| --- | --- |
| 1 | The proton and the neutron of P0 have reached P1 = (21, 20, 5) and P3 = (20, 21, 5), each with the other lamp's ray coming the other way: two pairs, `strong` fires at both corners |
| 2 to 19 | The pairs at P0 and P2 after the even ticks, at P1 and P3 after the odd, turned at every corner they reach; the phases t mod 8; the record reads one group, ring P0, P1, P2, P3, content 24 (proton 12, neutron 12), period 8, clock 1 and 1, from tick 1 to 19 |
| 20 | The low light (amount 2, steps 20) at P0 with the pair; the guard reads 2 > 3 as 0: `strong` turns the pair and the light crosses |
| 21 | The low light at P1 with the other pair, crossing it too; the high light (amount 6, +Y, steps 21) at P3 with the pair, the proton heading -X from P2 and the neutron +Y from P0; in the cycle that follows the guard reads 6 > 3 as 1: `photofission` fires, the three inputs replaced by three new event rays on their own headings (`steps` 0, the event's Ports -X and +Y with shares 6 and 12) |
| 22 | The proton of the split at (19, 21, 5) heading -X, the neutron at (20, 22, 5) heading +Y with the light; the other pair, turned at P1 in the same cycle, at P2 (the proton, heading +Y) and at P0 (the neutron, heading -X), each alone |
| 23 | No partner, no rule: the lone proton crosses off the ring to (21, 22, 5) and the lone neutron to (19, 20, 5); no group from here |
| 26 to 27 | The low light (at x = 25 at tick 25), the neutron and the light of the split (at y = 25) leave the board at tick 26, the lone proton at tick 27 |
| 32 | The proton of the split at (9, 21, 5) and the lone neutron at (10, 20, 5), walking -X |

Momentum at the split, amount times heading: inputs (-6, 0, 0) + (0, 6, 0)
+ (0, 6, 0) = (-6, 12, 0); outputs the same headings, (-6, 12, 0): exact,
the photon's included, nothing booked. At every tick: totals proton 12,
neutron 12, light 8 in the world with the escaped, momentum equal to its
sources (the corner turns, (-12, 12, 0) or (12, -12, 0) per corner per
interval, the two corners of an interval cancelling until the split, after
which the last turn at P1 stands); the charge ledger proton +36; every line
of the audit balanced; `conserved_at_every_completed_tick` true.

## Limits: what the engine refuses, and the rule that is missing

**The literal absorption is refused.** The translation "inputs light a +
electron m, outputs electron rays only, content m + a" is the outputs rule
below in place of `absorb` (its third output turns the light ray into an
electron ray of amount 3 on the light's heading, so energy and momentum are
exact):

```json
{"name": "absorb",
 "participants": [{"type": "electron"}, {"type": "electron"}, {"type": "light"}],
 "outputs": [
   {"field": "electron", "amount": {"of": 0}, "heading": "reversed", "input": 1, "phase": {"of": 0}},
   {"field": "electron", "amount": {"of": 1}, "heading": "reversed", "input": 0, "phase": {"of": 1}},
   {"field": "electron", "amount": {"of": 2}, "heading": "reversed", "input": 1, "phase": {"of": 2}}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}}]}
```

Two generic rules refuse it, and neither is a defect: with the catalog's
electron charge -3 the initialization stops with `ray meeting output 2 of
family electron (charge -3) would change the total charge: its amount comes
from inputs of another charge` (charge is per quantum, so content added to an
electron ray is charge added); with the electron's charge set to 0 the world
starts and the meeting stops it with `ray meeting absorb changes the stock
of a family` (a meeting with outputs keeps every family's stock exact,
[meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1)).
So in today's tables energy stored in a group is the sum of its rays' amounts
across families, and the excited electron is expressible as the ring with
the light ray in it, which is what `absorption.json` shows.

**The missing rule.** A meeting whose outputs change the stock of a family
under declared invariants: the change of family that Highlights 3.26 names
for the weak interaction (the catalog's `weak_conversion`, status open) and
that a photon absorbed into content would need too. The smallest generic
addition is one key on a `ray_interactions` rule with outputs, for example
`"stock": "converted"`, under which the engine (i) drops the per-family stock
equality of the meeting while keeping the total amount, the declared
invariants and the appended charge invariant exact, and (ii) books the
per-family difference on a `converted` line of the audit so that initial +
sourced + converted in = current + escaped + annulled + absorbed + converted
out holds per family at every tick. For absorption into a charged family a
second, larger decision is also needed: charge as a property of the ray
rather than of each quantum, since today an electron ray of amount 11
carries charge -33. Neither is added here; the register's B8 and the weak
interaction of the catalog will need the first. (On 2026-09-17 feature 13,
`decay-draw-v1`, added the first for a decaying conversion only: a rule with
outputs that declares `draw` may change family stock, the total amount and
the invariants exact, the change booked as each family's source at the
meeting; the generic key for a rule without `draw` stays open, [a decaying
group draws](../../docs/SPATIAL_FIELDS.md#a-decaying-group-draws-decay-draw-v1).)

**A random lifetime is not expressible.** The emission of
`absorption_emission.json` fires at a declared phase, so the excited state's
lifetime is one integer. Highlights 3.26 gives the decaying group its
half-life through the Detector draw at the group's tick (1 = the conversion
fires, 0 = the group ticks on); under the loop the group's tick is its
corner meeting, and the engine's Detector mark draws on arrivals through
Ports only, at a marked Node, never inside a rule. The missing rule is that
draw, the mark's setting applied at the corner meeting of the group's rays,
with the conversion as the outputs rule fired on 1; the catalog's
`weak_conversion` waits for the same rule. (Added on 2026-09-17 as feature
13, `decay-draw-v1`: the conversion's rule declares `draw: [n, d]` and
`seed`, and its meeting draws once, per meeting, from the Node's stream,
the Node marked by the declaration for that draw; a random lifetime is one
world key now, [a decaying group
draws](../../docs/SPATIAL_FIELDS.md#a-decaying-group-draws-decay-draw-v1).)

**The photon in the ring walks one edge.** The light output of `absorb`
leaves through input 1's entry Port, and at every corner input 0 is the
resident ray with the lower heading index, which alternates between the
senses around the square, so the photon is sent back along the edge it
came by and shuttles between P0 and P3 rather than circulating; a table
that read the sense would send it round. It is bound either way: a periodic
orbit with the ring's rays, read by the record as part of the group.

**Not shown.** No released field is declared: the world's light carries no
`field_of`, although light is the electron's own field in the catalog since
2026-09-17 (Highlights 3.5), and the `mass_field` of the catalog is absent;
a ring ray in motion would release five headings per Node departed, one of
them along the ring, and the closure of a ring with its own field is the
open point of the design ([loop binding](../../docs/LOOP_BINDING.md#6-the-field-of-a-loop)),
so the groups radiate nothing here. All matter rest rates are 1 at N = 8, a
resolution choice for the picture, not a mass, at which the unit square
closes in two circuits (period 8). The momentum of the corner turns is
booked as each corner's source, exact in the world's total, until the
group's field carries it.

## Run and render

The record of each run lives outside the tree (Highlights 5.5; the register
holds the fingerprint). With the project environment active:

```bash
PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/absorption.json'), Path('runs/absorption'))"
PYTHONPATH=src python tools/ray_viewer/record_sidecar.py runs/absorption
python tools/ray_viewer/extract.py runs/absorption --sidecar runs/absorption/ray-recording.json --label absorption --out runs/absorption/runs.json
python tools/ray_viewer/render_gif.py runs/absorption/runs.json --output runs/absorption.gif --contact-sheet runs/absorption-contact.png
```

The same four lines with `absorption_emission` and with `photofission`
render the other two runs. The
[ray viewer](../../tools/ray_viewer/README.md) draws the light ray arriving,
the meeting markers at the corners, the rays of the ring as matter and the
fragments leaving, and its document lists the groups it read from the record
(`groups`); a GIF is a rendering of a fingerprinted record, not evidence by
itself.

## The helium ion: one electron at a nucleus of charge +2

`helium_ion.json` is the model owner's request of 2026-09-17: to see a helium
nucleus with one electron around it (He+, hydrogen-like), and to compute the
orbit and the frequency a stable, closed orbit needs. The run is honest about
what the engine on `main` holds: the nucleus radiates its field on the six
axis lines through it and nowhere else, and the one landed turn of a matter
ray at a field ray is whole, so there is no closed orbit around the nucleus in
this engine; the run shows what happens instead, and the orbit is computed
beside it. The record is registered as
[E4](../../docs/EXPERIMENTS.md#e4-the-helium-ion-one-electron-at-a-nucleus-of-charge-2).

### Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| The helium nucleus, charge +2 e, mass about 7300 electron masses | An external body (`external_bodies[0]`) of the catalog's `proton` family at the centre (20, 20, 20), `charge` 6 in thirds of e (two protons' charge) and `amount` 2^20: the approximation of infinite mass, its whole content at one Node, never split, never pushed by matter, moved by fields only. The proton family's rest rate is set to 0 in this world, because a coupled body's token must return with the body's phase (external-body-v1); no proton ray exists on the board, so nothing else reads it | [External body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1); Highlights 3.19 |
| The Coulomb field of the nucleus | Light: the catalog's `light` is the field of every charge (Highlights 3.5, 2026-09-17), and the engine names one family per releaser, so this world declares it twice, `light_of_nucleus` (`field_of` `proton`, `release` [1, 4096]) for the nucleus and `light_of_electron` for the electron. The nucleus's: every interval the body releases one ray per Port heading of amount floor(2^20 / 4096) = 256, phase 0, booked as a source; each ray walks straight along its axis line at one Link per interval and releases nothing (a field has no field), so the field exists on the six axis lines through the nucleus only and its amount on a line does not fall with distance | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1); Highlights 3.5 |
| The electron, charge -1 e | One `electron` ray (rest rate 1, `charge` -3) of amount 4, emitted from the lamp at (28, 12, 20) heading +Y at tick 1: one Link per interval, the only speed in the engine. An electron at speed 1/k would be a bound group with `ray_delay` k (Highlights 3.28); a bound group is rays held at one Node by a delay-1 rule and does not move, and a ray field that meets anything must be unpaced, so the electron here is at c, k = 1 | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.4, 3.28 |
| The electron's own field | `light_of_electron`, the catalog's `light` released by the electron, `field_of` `electron`, `release` [1, 4]: five rays of amount 1 at every Node the electron departs, faint in the picture; those that reach the nucleus end in its sink and pull it by its `momentum_table` (-1: toward the source) | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1) |
| Coulomb attraction | The rule `nucleus_turn` over `[electron, light_of_nucleus]`, this world's own declaration: where the electron and a ray of the nucleus's light share a Node, the electron leaves on the negation of the field ray's heading (`"heading": "reversed", "input": 1`), toward the nucleus, with its amount and phase, and the field ray returns reversed as the recoil. It stands in for the catalog's open `opposite_charge` entry of `electron_field_turn` (the heading rule when the charges differ in sign, A5's to write), with the sign the model owner's words give ("an electron near a large charge"); the turn is whole at every meeting for any field amount from 1 up, the table that would make it partial (`strength_table`) being undecided too (A5) | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1), [the recoil](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1); Highlights 3.5, 3.14 |
| Coulomb repulsion of the electron by its own kind | The catalog's `electron_field_turn`, declared over `[electron, light_of_electron]` and never met: a straight ray never meets its own field, and after each turn the electron's earlier field rays are on other lines | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1); Highlights 3.5 |
| The recoil of the nucleus | The returned ray of the nucleus's light, amount 256, walking back along its axis to the body, where it ends in the sink and changes the body's momentum by 256 toward the electron (`momentum_table` -1); its velocity, momentum over 2^20, completes no Link in the run | [External body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1) ("motion by fields only") |
| The electron reaching the nucleus | The body's coupling `phase_plate` at setting 0 (catalog, decided): the arriving electron continues on its heading with its phase, the body's token returned unchanged; the nucleus is transparent to the electron. Under the default sink the electron would be absorbed at its first fall and the board would be empty of matter for the rest of the run | [External body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1) ("a declared coupling") |
| Energy | The amount; the invariant `energy` of every rule, exact over inputs and outputs | Highlights 3.15 |
| Momentum | Amount times heading. The electron's is bound to the vector `momentum` (`recoil_field` on its emission, the lamp keeping the recoil), so the audit carries a momentum line; the momentum a turn moves has no ray to carry its transverse part and is booked as the meeting's source of that line, exact at every tick; the recoil's own momentum is on the field ray, read on the bodies' line when absorbed | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) ("Momentum of a split"); Highlights 3.14, 3.16 |
| Charge | -3 per electron quantum, +3 per proton quantum, 0 on every field family; `charge x amount` appended to every meeting; the body's declared charge 6 on the audit's bodies line | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1) |
| Gravity | Not declared: the catalog's `mass_field` and `mass_field_delay` are left out, gravity being 10^-39 of the Coulomb force at this scale, and the `release` and the delay table are undecided (A6) | [Catalog](../../docs/CATALOG.md) |
| The orbit | The closed square of side 2r with the nucleus at its centre, four turns of a quarter turn each per circuit, period T = 8 r k intervals, frequency 1/T; computed below, not held by the engine | Highlights 3.4 |

### The orbit computed: what a stable, closed orbit needs

The nucleus is at the origin O. The electron of content m at speed 1/k Links
per interval runs the square with corners (r, r), (-r, r), (-r, -r), (r, -r)
in the plane z = 0: sides of 2r Links, 8r Links per circuit,

```text
T = 8 r k intervals,  f = 1 / T per interval;  here r = 8, k = 1: T = 64, f = 1/64.
```

At each corner the heading turns a quarter turn: from (0, m, 0) to
(-m, 0, 0), a momentum change of (-m, -m, 0), and the nucleus must receive
(m, m, 0) back through the recoil. The conditions for the orbit to close on
itself, as integer equalities that must hold at every turn:

1. **The turn is where the field is.** The four turns are at the corners
   (±r, ±r, 0). The body's field is on the six axis lines, which meet the
   square at the midpoints of its sides, (±r, 0, 0) and (0, ±r, 0), never at
   a corner; and a quarter turn at a midpoint sends the electron along the
   axis, into the nucleus (attraction) or away from it (repulsion). So with
   the field on the axes no closed orbit around the nucleus exists, for any
   r, m, k or field amount: every closed path of axial segments whose turns
   all lie on the axis lines runs along the axes themselves. This is the
   condition that fails today, and it fails by geometry, not by a number.
2. **A whole quarter turn per turn.** With a Port-table output (the landed
   form, `heading` a Port or `"reversed"` of the field ray) the whole
   electron turns whenever the field ray's amount A = floor(M n / d) is at
   least 1 (here A = 256): one quantum too low, A = 0, is no field ray and no
   turn, and no amount is too high. With a delay table instead (feature 8,
   `delay: {"of": 1, "table": [t0, ..., t5], "per": u}`) the lag laid at the
   crossing is floor(A t_p / u) phase steps and a full Link toward the
   lagging side needs exactly floor(A t_p / u) = N = 2^`phase_bits` (256
   here): one quantum too low leaves a lag below N that is never spent (the
   electron misses the turn and goes straight on), one quantum too high
   leaves a remainder of one step that accumulates to an extra Link after N
   turns (the orbit overturns by one Link every N circuits); and a lag turns
   the line by one Link with the heading unchanged, never by a quarter turn,
   so a lag on the axes gives no closed orbit either.
3. **The recoil closes the momentum.** At each turn the field ray returns
   reversed with amount A, carrying 2A along its own axis, and the transverse
   m has no ray to carry it (booked as the meeting's source); at the nucleus
   each recoil adds A toward the electron, so a closed circuit hands the
   nucleus four recoils of A on +x, +y, -x, -y whose sum is exactly zero, and
   the body steps only when an axis accumulator reaches 2^20, never here.
4. **The clock closes on the phase circle.** The electron's phase advances 1
   per interval, so one circuit advances it 8 r k steps; a meeting reads
   phases only as a difference through a table, and no table in this world
   reads one, so the orbit needs 8 r k = j N for no integer j today. Once a
   turn table reads the phase difference between the electron and the field
   (the body's phase, constant), closure needs 8 r k to be a multiple of N:
   at N = 256 and k = 1 the smallest square has r = 32 (T = 256), the model's
   form of the standing-wave condition on an orbit.

### helium_ion.json, tick by tick

Board 41 x 41 x 41, open, `link_ticks` 1, `phase_bits` 8 (N = 256), 128
ticks, two computed periods. The nucleus at (20, 20, 20); the electron lamp
at (28, 12, 20), the lower end of the square's right side x = 28, heading +Y,
amount 4. Rules in order: `nucleus_turn`, `electron_field_turn`,
`phase_plate`. The ticks are the state after the tick.

| Tick | What is on the board |
| --- | --- |
| 1 | Six `light_of_nucleus` rays of 256 leave the nucleus, one per axis, and six more every tick after; the electron is at (28, 13, 20) heading +Y, releasing five `light_of_electron` rays of 1 at every Node it departs |
| 8 | The electron reaches (28, 20, 20), the midpoint of the side, where the field ray released at tick 1 arrives in the same interval |
| 9 | The turn: the electron leaves (28, 20, 20) heading -X, toward the nucleus (`steps` 0, a new event), the field ray reversed behind it as the recoil; the square's next side is not where it goes |
| 9 to 15 | The fall along the axis: at every Node from x = 27 to 21 the electron meets the next field ray, is left inward by the same rule (a new event and a recoil at each Node) and walks one Link per interval |
| 16 | The electron is at the nucleus and passes it (`phase_plate`); the eight recoils of 256 arrive at the body in this one interval (each left one Link nearer and one tick later): the sink takes 2048 and the body's momentum becomes (2048, 0, 0), toward where the electron came from |
| 17 | The electron is at (19, 20, 20), heading -X, past the nucleus |
| 18 | Turned back by the -X field ray at (19, 20, 20): heading +X, at the nucleus again; the recoil of 256 arrives from the far side, momentum (1792, 0, 0) |
| 19 | (21, 20, 20) heading +X; turned back there by the +X field ray |
| 20 to 128 | The cage: the electron runs 21, 20, 19, 20, 21, ... through the nucleus, one recoil of 256 every second interval alternating in sign, the body's momentum between 2048 and 1792 and its accumulator far below the 2^20 of one Link; the phase advances 1 per interval throughout |

Observed period: 4 intervals (the cage), amplitude 1 Link on each side of the
nucleus. Computed period of the square orbit: 64 intervals. The two stand side
by side in the register entry. At every one of the 128 ticks: electron 4 in
the world, none escaped; `light_of_nucleus` sourced 1536 per tick, in the world
28160 or 28416 from tick 20 on, once the six axis lines are full, the rest
escaped at the open boundary or in the sink (16384 by tick 128, 64 recoils);
the momentum line initial (0, 0, 0), sourced (-4, -4, 0) at the first turn
and then (4, -4, 0) or (-4, -4, 0) as each reversal in the cage is booked,
current equal to it at every tick (the lamp holds (0, -4, 0), the electron
(-4, 0, 0) or (4, 0, 0)) and balanced;
the charge line electron -12; the bodies' line count 1, charge 6; every audit
line balanced, `conserved_at_every_completed_tick` true.

### Limits: what the run shows instead of an orbit, and the rules that are missing

**Why the fall.** The two facts that decide it: the body's field lives on its
six axis lines only, and the landed turn is whole. An electron that crosses
an axis line is sent down the axis, meets a field ray at every Node there,
and is turned back at the first Node past the nucleus whichever side it
leaves on: the engine's bound state of He+ is a two-Link cage through the
nucleus, period 4, for every r, m and field amount, since nothing in the
turn reads the amount. A partial turn from the delay table would not close
an orbit either: it shifts the line one Link with the heading unchanged, and
on the axis the next Node lays the next lag, a runaway into the nucleus once
the lag per crossing reaches N and nothing at all below it. A bound group
cannot be the electron at 1/k: it is held at its Node and does not move.
(Closed later on 2026-09-17 by feature 8c, `bound-group-motion-v1`: a bound
group carries a momentum register and steps one Link when a whole content
has accumulated on an axis, and the field rays a binding rule's
`momentum_table` names push it; see [bound group
motion](../../docs/SPATIAL_FIELDS.md#bound-group-motion-bound-group-motion-v1).
This run was made before it and is not re-made here.)

**The missing rules, smallest generic additions.** (i) The field off the
axes: a ray of the nucleus's light at a Node re-releasing its information on
the five headings other than its own in shares by a declared table, the path
counting of Highlights 3.5 ("as a diamond at the scale of Links and as a
sphere at large scale") that today's "a field has no field" excludes; this is
the catalog's open `spread` entry of `light` (feature 12), booked as a source
like every release. (ii) A turn proportional to the field: the delay table of feature 8
already lays a lag proportional to the field amount, but a lag is spent as a
sideways Link with the heading unchanged, so the most it can do is a
staircase of one part in two and it can never reverse the forward motion; the
generic addition is to spend a transverse lag that reaches N as a quarter
turn of the heading toward the lagging side when the sideways Links owed
exceed the forward ones, that is, to let the lag register be the transverse
momentum the audit reads, as Highlights 3.28 already states for feature 8b.
With (i) and (ii) the closed orbit is a staircase circle whose period is
8 r k and whose stability is the integer equalities above. Neither is added
here.

**Not shown.** The nucleus's picture is the viewer's default body (a star);
gravity is not declared; the proton's rest rate is 0 in this world for the
token's sake; no lamp emits light, so every light ray on the board is a
field ray of one of the two charges.

### Run and render

```bash
PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/helium_ion.json'), Path('runs/helium-ion'))"
PYTHONPATH=src python tools/ray_viewer/record_sidecar.py runs/helium-ion
python tools/ray_viewer/extract.py runs/helium-ion --sidecar runs/helium-ion/ray-recording.json --label "The helium ion" --out runs/helium-ion/runs.json
python tools/ray_viewer/render_gif.py runs/helium-ion/runs.json --output runs/helium-ion.gif --contact-sheet runs/helium-ion-contact.png
```

The record stays outside the tree; the register holds its fingerprint.

## The helium ion with the field spreading and the momentum turn

`helium_orbit.json` repeats the model owner's request of 2026-09-17 (the
helium nucleus with one electron around it; the orbit and the frequency a
stable, closed orbit needs) on the engine that holds the two rules
[E4](../../docs/EXPERIMENTS.md#e4-the-helium-ion-one-electron-at-a-nucleus-of-charge-2)
found missing: the field spreads off the axes (feature 12,
`field-spreading-v1`, with the Node-owned remainder of feature 12b,
`field-remainder-v1`) and a free ray turns gradually by the momentum of the
field rays it meets (feature 8b, `ray-momentum-turn-v1`). The orbit is
computed before the run, in the rule's own terms and on this lattice, and
the record is registered as
[E8](../../docs/EXPERIMENTS.md#e8-the-helium-ion-with-the-field-spreading-and-the-momentum-turn).
`helium_orbit_axes.json` is the same world with the field not spreading,
E4's axis-only field under the momentum turn, the control that shows what
feature 12 adds.

### Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| The helium nucleus, charge +2 e | An external body (`external_bodies[0]`) of the catalog's `proton` family at the centre (7, 7, 7) of a 15^3 board, `charge` 6 in thirds of e and `amount` 2^20, as in E4: infinite mass, never split, moved by fields only; the proton's rest rate 0 for the token's sake | [External body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1); Highlights 3.19 |
| The Coulomb field of the nucleus | `light_of_nucleus`, the catalog's `light` released by the proton family (`field_of` `proton`), `release` [1, 749]: every interval the body releases one ray of amount A = floor(2^20 / 749) = 1399 per Port heading, phase 0, `source_sign` +1 from its charge, booked as a source; and, new since E4, `spread` [6, 1, 1, 1, 1, 1], the catalog's table: every Node the field reaches releases it again, six of eleven parts forward, one back, one on each transverse heading, the shares below one quantum owned by the Node per family, sign and Port and released whole when they fill (feature 12b), so the field reaches every Node and its average intensities follow the table exactly | [Field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1); Highlights 3.5 |
| The electron, charge -1 e, mass m | One `electron` ray (rest rate 1, `charge` -3) of amount m = 256, its momentum register m along its line at the launch; one Link per interval, the one speed of the engine (Highlights 3.28: the register sets the direction and never the speed) | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2) |
| Coulomb attraction | The rule `nucleus_turn` over `[electron, light_of_nucleus]` without outputs, `momentum_table` `{"light_of_nucleus": -1}`: at every Node the electron shares with field content its register moves by -1 x amount x heading of every field ray there (toward the source of each), the accumulators reset, and each field ray returns reversed as the recoil; the DDA then walks the register. It is the catalog's `electron_field_turn` in the momentum-table form with the sign of opposite charges, standing in for the open `opposite_charge` entry (A5): the field ray carries `source_sign` +1, which no guard reads today (a coupling's view is amount, heading, phase, rate, delay, family, charge and bit), so the sign is the table's declaration, as in E4 | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2); Highlights 3.5, 3.14 |
| The launch, at rest in an established field | A second external body, `launcher`, of an apparatus family (rest rate 0, charge 0, no field) at (13, 6, 7), one Link before the orbit's tangent point (13, 7, 7), with the coupling `launch` over `[electron, launcher]`: the electron arrives from its lamp at (13, 5, 7) at tick 1 with phase 1, the guard `eq(phase, 1)` holds, and the output returns it on its heading with `delay` 40, so it waits forty intervals while the nucleus's field fills the board, and leaves on +Y with phase 41; the guard is false on every later pass (the phase advances while it waits and walks). The launcher's Node sinks every field ray that reaches it (its coupling does not name the field), a hole of one Node in the field on the orbit, counted in the computation below; nothing else in the engine delays an emission | [External body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1) ("a declared coupling"); [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) (`delay` on an output) |
| The electron's own field | Not declared in this world. A turning electron's transverse Links carry its own released rays along with it (the release skips the dominant axis of the register only), so the catalog's `electron_field_turn` would fire on its own field at the next Node; the self-field of a turning charge is a question of its own (A5) and is left out so that the nucleus's pull alone acts. E4 declared it and never met it | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1) |
| The recoil of the nucleus | Every field ray the electron meets returns reversed as a new event ray and, since the family spreads, is spread from the next Node like any content; what reaches the nucleus's sink pushes the body by its `momentum_table` (-1, toward where the content came from), together with all of its own field that diffuses back into it; the body's momentum is the running asymmetry of its sink, and a Link needs 2^20 on one axis, which no run of this length reaches | [External body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1) ("motion by fields only") |
| The electron reaching the nucleus | The body's `phase_plate` at setting 0, as in E4: the nucleus is transparent to the electron | [External body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1) |
| Energy, momentum, charge | The amount; the register read by the ledger's momentum line, the push and the reversal booked as the meeting's source; -3 per electron quantum, 0 on the field, the bodies' line charge 6 | [Audits](../../docs/SPATIAL_FIELDS.md#audits-ray-event-audit-v1); Highlights 3.14 to 3.16 |
| The orbit | The digital circle of radius R = 6 the DDA traces for a register turning uniformly, 8R = 48 Links per revolution, period T = 48 intervals, frequency 1/48; computed below | Highlights 3.4, 3.28 |

### The orbit computed: what a stable, closed orbit needs

**The rule's own dynamics.** Write P for the length of the electron's
register, r for its distance from the nucleus and a for the angle between the
register and the tangent of the circle through it (a > 0 pointing outward).
The net field flux through the electron's Node is the current of the
spreading field, on the isotropic average k / r^2 toward the nucleus, so the
register turns by the push and the ray walks one Link along it:

```text
dr/dt = sin a,   dP/dt = -(k / r^2) sin a,   da/dt = cos a (1 / r - k / (r^2 P)).
```

A circular orbit is a = 0 and P = k / r, one for every radius r, with the
period 8 r in the lattice's L1 metric (the DDA walks one axis Link per
interval; the L1 length of a circle of radius r is 8 r). Linearized about it,
d(da)/dt = dr / r^2 + dP / (r P) and its second derivative is zero, so a
radial displacement d grows as d (1 + t^2 / (2 r^2)) with nothing to restore
it: the orbit is a neutral equilibrium. Kepler's stability comes from the
speed falling as the body climbs; here the speed is the one speed of the
board (Highlights 3.28), the register changes only the direction, and the
curvature k / (r^2 P) falls faster than 1 / r when the electron drifts out.
So the answer to "the frequency a stable, closed orbit needs" in this rule
is: every radius has a closed orbit, of frequency 1 / (8 r) at register
k / r, and none is stable; the run shows how the first perturbation resolves
it, a fall or an escape.

**The lattice.** The push per interval that turns a register of length m by
one step of the circle is p = m tan(pi / (4 R)); for m = 256 and R = 6,
p = 256 x 0.1317 = 33.7, about 34 quanta per interval. Every push is an
integer vector added to the register, so a push perpendicular to it lengthens
it by about p^2 / (2 m) = 2.3 per interval, a second-order term the
continuum map does not have (there a perpendicular push leaves P unchanged);
over a revolution the length would grow by 40 percent and the turn per
interval fall with it, unless the path's opening turns the pushes backward.

**The flux on this lattice.** The isotropic average gives a net push of
S / (4 pi R^2) per Node at distance R, S the effective source. The exact
mean field of the split table on the 15^3 board (a linear map; the
Node-owned remainders make the integer field equal it on average) with the
body releasing A per heading per interval, the nucleus's sink taking back
what diffuses into it and the launcher's sink at (13, 6, 7), open faces,
iterated to its steady state, gives per unit A:

- the nucleus's sink takes 1.014 A per interval of the 6 A released, the
  backward share of its six neighbours (6 A / 11 = 0.545 A) and the rest
  diffusion; the effective source is S = 4.986 A;
- the digital circle of radius 6 from (6, 0) has 48 Nodes at Euclidean
  distances 5 to 7.07 (the DDA rounds the circle one Link off centre, through
  (0, 7) and (0, -5)); the mean inward push over them is 0.0241 A per
  interval, 2.2 times the isotropic S / (4 pi 36) = 0.0110 A, because the
  forward weight keeps a beam on each axis: 0.065 A at the axis crossing
  (6, 0), 0.105 A at (0, -5), 0.011 A on the diagonals such as (5, 5); the
  L1 shell of radius 6 has 4 x 36 + 2 = 146 Nodes; the mean gross flux is
  0.069 A per interval, so the net is about a third of what arrives;
- the transient: the mean push on the circle is 82 percent of its steady
  value at tick 26, 90 percent at tick 40, 94 percent at tick 50, 96 percent
  at tick 60.

**The integers.** m = 256, R = 6, T = 48; the push wanted is 34 per
interval, so A = 34 / 0.0241 = 1399, that is `release` [1, 749]
(floor(2^20 / 749) = 1399) and 6 A = 8394 quanta released per interval; the
electron is held 40 intervals and leaves the launcher at tick 42 into a field
at 90 percent of its steady flux; the run is 152 ticks, the hold, two periods
and a margin of 16. Expected before the run, from the neutral equilibrium and
the perturbations above (the lattice's anisotropy of 0.47 to 4.3 times the
mean push along the circle, the lengthening of the register, the transient,
the integer flux exact only on average): the electron circulates for part of
a period and then falls in or escapes, the sign set by its first pushes; no
closed orbit, and none stable at any radius.

**The recoil.** Each met field ray returns reversed and spreads from the
next Node; the nucleus's sink takes about 1.014 A = 1419 quanta per interval
in all and its momentum is the running asymmetry of what it takes; at
2^20 per Link the body completes no Link in 152 intervals whatever the
asymmetry (at most 1419 x 152 = 215,688 < 1,048,576 on one axis).

**The recoil walks with the electron.** Added after the control's record was
read and before the orbit's (2026-09-17), from the rules and the mean field
above, no integer changed: the recoil of a push is a new outbound event ray on
the negated heading, and the coupling pushes by every outbound ray of the
family at the Node, so the recoil of field content that met the electron
head-on (walking against its step) leaves on the electron's own step, reaches
the next Node with it and pushes it back by the same amount one interval
later: the head-on content's push is cancelled, while content walking with
the electron (from behind) pushes it backward once and its recoil leaves it
for good. On the circle the mean field gives per unit A and interval 0.0113
head-on (cancelled), 0.0114 from behind (a drag of 16 at A = 1399, along the
step and against it) and 0.0177 transverse in the plane (an inward push of
25), the z content cancelling in pairs. So the register's component along the
motion falls by about 16 per interval from 256 while the inward pushes turn
it: the electron turns inward faster than the mean push alone gives, and the
likelier sign of the first perturbation is the fall, within a fraction of a
period. The control shows the same mechanism on the axis: during the fall two
pushes per Node, the +X ray's and its recoil's, summing to zero.

**The control.** `helium_orbit_axes.json` declares no `spread`: the field
lives on the six axis lines, A = 1399 on each, and the electron leaving the
launcher meets the +X line at (13, 7, 7) with the whole ray: its register
becomes (-1399, 256, 0), the fall of E4 in the register's language.

### helium_orbit.json, tick by tick

Board 15^3, open, `link_ticks` 1, `phase_bits` 8 (N = 256), 152 ticks. The
nucleus at (7, 7, 7); the launcher at (13, 6, 7); the electron lamp at
(13, 5, 7), heading +Y, amount 256. Rules in order: `launch`, `nucleus_turn`,
`phase_plate`. The ticks are the state after the tick; the pushes are the
`ray_push` records of the electron's Node in slot order, each -1 x amount x
heading of one field ray, and the register is the electron's after them.

| Tick | What is on the board |
| --- | --- |
| 1 | Six `light_of_nucleus` rays of 1399 leave the nucleus, one per axis, and six more every tick after; each spreads at the next Node by [6, 1, 1, 1, 1, 1], the shares below one quantum into the Node's registers; the electron arrives at the launcher with phase 1 and is held |
| 2 to 41 | The electron waits; the field fills the board (a spread has happened at 825 Nodes by tick 8, 1757 of the 3375 by tick 12, 2925 by tick 22 and at every Node but the two bodies' by tick 40, the corners last), escapes at the open faces from tick 8 and returns into the nucleus's sink from tick 2, the sink's rate rising toward 1399 per interval, one sixth of the release, as computed |
| 42 | The electron arrives at the tangent point (13, 7, 7), the +X axis crossing at distance 6, and meets five field rays: +X 94 (the axis beam; the mean field gave 91), -X 7, -Y 11, +Z 11, -Z 11; pushes (-94, 0, 0), (7, 0, 0), (0, 11, 0), (0, 0, -11), (0, 0, 11); the register (0, 256, 0) becomes (-87, 267, 0) and the five recoils leave reversed |
| 43 | (13, 8, 7): six field rays, the recoil of the -Y push among them, walking +Y with the electron and pushing it back (0, -11, 0): +X 35 (the mean field 34), -X 4, +Y 11, -Y 8, +Z 8, -Z 8; the register (-118, 264, 0). The accumulators reset at every push (`ray-momentum-turn-v1`, the engine of this record; v2 keeps them), so the DDA steps along the register's dominant axis, +Y, and nothing else |
| 44 to 49 | Straight up the line x = 13, one Link per interval, six field rays at every Node, the +X push falling with the distance, 25, 18, 11, 8, 5, 3, the head-on -Y content cancelled by its recoil a tick later and the +Y content dragging: the register (-139, 262, 0), (-154, 262, 0), (-165, 259, 0), (-173, 258, 0), (-178, 257, 0), (-181, 256, 0) at (13, 9, 7) to (13, 14, 7); the distance from the nucleus 6.32, 6.71, 7.21, 7.81, 8.49, 9.22 |
| 50 | The electron leaves the board through the +Y face at (13, 14, 7), 7 Links from the nucleus, with its register (-181, 256, 0): `escaped` electron 256, momentum (-181, 256, 0); no push moves it again |
| 51 to 152 | The field alone: released 8394 per interval, escaping at the faces and returning into the sink; the launcher's sink takes what reaches it; the body's momentum stays the running asymmetry of its sink |

Observed: no circuit, no period; the radial distance rises monotonically from
6.00 to 9.22 over the eight moving Links; 8 ticks with pushes, 46 pushes in
all, their sum (-181, 0, 0) on the register (the y and z pushes cancelling
exactly, 0 and 0). The register's x component at the face, -181, against the
mean field's -190 for a straight walk to the same Node and its limit -214 on
an unbounded board: the dominant axis never flips. Ledger: light released 8394 per interval, 1275888 by tick 152, of which 258398 in the world (the registers included), 798078 escaped and 219412 in the sinks (208309 the nucleus's, 11103 the launcher's), the identity exact at every tick; the momentum line initial (0, 0, 0), sourced (-181, 0, 0) (the pushes, the field binding no momentum field), current (0, -256, 0) (the lamp's recoil), escaped (-181, 256, 0) (the electron's register), balanced; the charge line electron -768 until the escape; the bodies' line count 2, charge 6, momentum (-29, 12, 0), no Link stepped; every audit line balanced at all 152 ticks, `conserved_at_every_completed_tick` true; 1589 s of wall time.

### helium_orbit_axes.json, the control, tick by tick

Board 15^3, open, N = 256, 152 ticks; the same world without `spread`. The
ticks are the state after the tick.

| Tick | What is on the board |
| --- | --- |
| 1 | Six `light_of_nucleus` rays of 1399 leave the nucleus, one per axis, and six more every tick after, on the six axis lines only; the electron arrives at the launcher (13, 6, 7) with phase 1 and is held |
| 2 to 41 | The electron waits at the launcher (no push: the launcher's sink takes what reaches it); the field escapes at the open faces from tick 8 |
| 42 | The electron arrives at (13, 7, 7) on the +X line and meets the whole axis ray: one push (-1399, 0, 0), the register (-1399, 256, 0), the recoil reversed behind it; toward the nucleus in one step |
| 43 to 47 | The fall down the axis, one Link per interval: at every Node two pushes, the next axis ray (-1399, 0, 0) and the recoil of the previous push walking with the electron (+1399, 0, 0), summing to zero, the register unchanged |
| 48 | The electron at the nucleus, transparent (`phase_plate`); its output assigns the heading and clears the register to (0, 256, 0); the sink takes the first recoil, 1399, the body's momentum (1399, 0, 0) |
| 49 to 103 | The cage of E4: at (7, 8, 7) the +Y ray pushes (0, -1399, 0), the register (0, -1143, 0), back to the nucleus, reset, out again; period 2, one recoil of 1399 into the sink every second interval, the body's momentum (1399, 1399 k, 0) |
| 104 to 152 | The cage steps outward along +Y by one Link about every twenty intervals as the recoils it leaves on the line return through it: (7, 8, 7) and (7, 9, 7) from tick 106, (7, 10, 7) and (7, 11, 7) at the end; the body's momentum (1399, 37773, 0), no Link stepped (2^20 needed) |

Verdict: fall at tick 48 and a cage, no circuit; `light_of_nucleus` released
8394 per interval, 1144382 escaped and 71349 in the sink by tick 152, 55960 in
the world; electron 256 at every tick; every ledger line balanced,
`conserved_at_every_completed_tick` true. What feature 12 adds is everything
off the axes: in the control the field is six lines and the fall is the only
motion.

### Limits: what the run shows and what is open

**Why the escape.** Three facts of the rules, each computable, decide it.
(i) The DDA's accumulators reset at every push under `ray-momentum-turn-v1`,
the engine of this record (`pushed_ray`, "as at a change of line"), so a ray
pushed in every interval steps along its register's dominant axis and
nothing else: the gradual line of `ray-momentum-turn-v1` needs Links without
a push to show, and a field that reaches every Node leaves none. Since
`ray-momentum-turn-v2` (2026-09-17, [a push keeps the
walk](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2))
a push keeps the accumulators and the DDA walks the line of the running
register under a push every interval, so the engine on `main` does not
reproduce this record; the rerun is not part of the fix. The path is therefore axis runs with whole quarter turns where
the dominant axis flips, E4's whole turn by another road. (ii) The transverse
impulse a straight half-line gathers from a 1/r^2 flux is finite, k / R with
k the field's strength: at A = 1399 and R = 6 it is about 204 by the isotropic
average and 214 by the mean field of this lattice, below the register's 256,
so from the tangent point the x component can never exceed the y component
and the electron walks straight off the board, on a board of any size; the
face at 7 Links only ends the record early. A flip needs k / R > m, that is,
the field delivering more than the electron's whole momentum on the half
line, and a flip at the crossing sends the electron down the axis into the
nucleus, the fall of the control. (iii) Between these two, the neutral
equilibrium of the computation: nothing restores a radius. So the engine of
this record (v1) gives the helium ion no circulating electron at any m, R or A:
the electron passes straight (escape) or is turned onto an axis and falls
(the control, E4's cage), and the answer to the model owner's question is
the computed one, a closed orbit at every radius, none stable, and on the
lattice none at all while every interval carries a push.

**What is open.** The reset of the accumulators at a push was the point of
decision, and it is decided: since `ray-momentum-turn-v2` (2026-09-17) a
push keeps them, the push changing the register alone, and the DDA walks a
curved line under a push every interval; this record, made under v1, was
repeated with the fix on 2026-09-17 (E8's Status): on the 15-cube the
electron curves half way around the nucleus at distance 5 to 8 and leaves
through the x = 0 face, the far side of its arc one Node outside the board;
on `helium_orbit_21.json`, the same world on 21 x 21 x 21 (nucleus at (10,
10, 10), launch at (16, 10, 10), 200 ticks), it turns a quarter turn to
distance 7, then runs straight where the field is weak and leaves at
distance 11.66: an escape on either board, the arc where the field is strong
and the straight line where the impulse of (ii) is below the register. The neutral equilibrium would still make the circle
unstable, a spiral in or out at the rate of the first perturbation, and a
stable orbit would further need the speed to depend on the register, which
Highlights 3.28 excludes: both are the model owner's to decide. The recoil's `source_sign` 0 and
the slot budget are engine facts stated above.

Two facts of the engine met on the way, stated here because a world must
declare around them: (i) the recoil of a push carries `source_sign` 0, not the
field's sign (the momentum-turn rule copies no sign, unlike an outputs
meeting's recoil), so after the launch the field near the electron is content
of two signs, +1 from the nucleus and 0 from the recoils, which spread as
separate rays; (ii) a Node then holds up to twelve plain rays of the family
and the recoils beside them, more than E4's eight `ray_slots`, and the
families of one layer share 32, so this world gives the light 24 slots and the
three one-ray families 4, 2 and 2 (a first world with eight slots failed at
the first pushes with `ray slot budget exceeded` and was replaced before its
record was read).

### Run and render

```bash
PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/helium_orbit.json'), Path('runs/helium-orbit'))"
python examples/nature/helium_orbit_table.py runs/helium-orbit
python tools/ray_viewer/extract.py runs/helium-orbit --label "The helium ion: the orbit" --out runs/helium-orbit/runs.json
```

The same lines with `helium_orbit_axes` and the label "The helium ion: the
axis-only control" read and render the control. `helium_orbit_table.py` reads
the record alone (`run.json`, `initialization.json`, `events.jsonl`) and prints
the electron's Node, offset, distances, register, pushes, the nucleus's sink
and momentum per tick, and the verdict (launch, fall, escape, closure, the
observed period, the radial range, the ledger); no sidecar is made for these
records, whose event streams run to hundreds of megabytes, so the viewer draws
the paths from the transits and no register arrow. The records stay outside
the tree; the register holds their fingerprints.

## The screen: the field of an electron at rest on seven marks

**Retired on 2026-09-17 with feature 14 (`loop-binding-v1`).** The three
records below ran under the interim held form (an electron at rest as two
rays held at one Node by `bind`, `delay` 1, `ray_delay` 1), the last of them
at commit `6f35705`; `screen.json` and `screen_spread.json` are removed
from the tree with that form, and their fingerprints and findings stay here
and in the register ([E6](../../docs/EXPERIMENTS.md#e6-the-screen-the-field-of-an-electron-at-rest-on-seven-marks)).
A loop of content 8 releases nothing at the catalog's ratio `[1, 4]` (a ray
of amount 1 releases floor(1 / 4) = 0), and a radiating loop needs rays of
amount 4, content 32 at least, a different demonstration to be written and
pinned anew after A1's table and width, not a silent rerun with another
source. The text below describes the retired worlds as they were; the
demonstration with the loop source is
[below](#the-screen-with-a-loop-the-ring-radiating-on-seven-marks)
(`screen_loop.json`, E9).

`screen.json` was the model owner's request of 2026-09-17 to see the eye view
([Highlights](../../docs/HIGHLIGHTS.md) 5.4, "everything begins and is
realized at a marked Node"; the [ray viewer](../../tools/ray_viewer/README.md#the-eye-view))
with clicks in it: an electron at rest releasing its field `light` in front
of a screen of seven Detector marks. Board 12 x 11 x 11, open, `link_ticks`
1, `phase_bits` 3, 24 ticks. The electron at rest is the bound group of the
dictionary above: two `electron` lamps at (0, 5, 5) heading +X and (2, 5, 5)
heading -X, amount 4 each, meet at (1, 5, 5) at tick 1 and `bind` (`delay`
1, `ray_delay` 1) holds them there, content 8. `light` is the electron's
field (`field_of` `electron`, `release` [1, 4], the catalog's ratio): a held
ray releases on all six headings every interval, so from the cycle at tick
1, in which `bind` fires, the group releases 2 on each of its six axis lines
every interval (1 per ray, the two merged into one ray with the group's
phase). The screen is seven marks at (7, 2, 5) through (7, 8, 5), setting
[1, 1] (every arrival clicks, none is returned), at distance 6 along +X.

**Before feature 12 (2026-09-17): one mark clicks; after: the whole
screen.** The field lives on the six axis lines of the group only (a field
has no field until light's `spread` table, feature 12), so the +X line
reaches the on-axis mark (7, 5, 5) alone: the first release leaves (1, 5, 5)
in the interval after `bind` fires and arrives at tick 7, and one click of
amount 2 follows every tick from 7 to 24, eighteen clicks at one mark and
none at the six others. The eye panel shows one spot at that mark, growing
with its hits. With the split table of feature 12 the released light can
reach every Node of the screen; a world declares it with `spread` on
`light`, `screen_spread.json` below. The
record, made once: `source_sha256`
`5f89c465b235083ebb2e9284db1f172a094cefa8003b94ea38a04003a10d23cc`,
`initialization_sha256`
`35dde6ad84145b5042285baadbb27810b5d30527554646cc67f5a69eac941cff`; at
every tick electron 8 in the world and none escaped, light released 12 per
interval (276 by tick 24, 214 escaped at the open boundary, 62 in the
world), momentum (0, 0, 0), the charge ledger electron -24, every audit line
balanced, `conserved_at_every_completed_tick` true.

**After feature 12 (2026-09-17, `field-spreading-v1`): one of the seven
marks clicks, the on-axis one, twelve times.** `screen_spread.json` is
`screen.json` with `spread` `[6, 1, 1, 1, 1, 1]` declared on `light` (the
catalog's table) and nothing else changed, run once for 24 ticks
(`initialization_sha256`
`34ce343eeb204d9a8b7b1b0c6e6b5c79a21eeb799f717b76d13514a18718fa2d`, `source_sha256`
`3426aa1ddf25f30348d6238edb66b0454e484a237f40fcf9367bdb948d99c2c9`). The released rays of 2 spread at the
first Node they reach: 2 gives 1 forward by the table and the remainder 1
through the entry the group's phase selects, forward at phases 0 to 4,
backward at 5, transverse at 6 and 7, and a single quantum then turns the
same way at every Node, so in 24 ticks the +X line still feeds the on-axis
mark alone, with less: (7, 5, 5) clicks 12 times, amount 24 in
all, from tick 7, the six other marks never; light released 276, 207
escaped, 69 in the world at tick 24, electron 8, momentum (0, 0, 0), every
ledger line balanced. The whole screen clicking waits for a table and a
phase width in which the turned quanta reach it, which experiment A1
confronts; the model owner replaced the phase-selected remainder the same
day (feature 12b, below).

**After feature 12b (2026-09-17, `field-remainder-v1`): in 48 ticks the
on-axis mark clicks four times and the six others not yet; in 240 the whole
screen clicks, the on-axis mark most.** `screen_spread.json` now runs 48
ticks (`ticks` raised from 24 on 2026-09-17, because 24 ticks show nothing
off the axis: one click at (7, 5, 5) at tick 19), run once
(`initialization_sha256`
`9b0473248483faf4e0bcc97100e40e411674c5846df130973ac503338c3983b8`,
`source_sha256`
`4c6e313ce9f0b14be95ce85b3c4f256d4072f2e81715ddf1f1071b44c11d33bb`). The
Node owns the sub-quantum remainder ([the split and the
remainder](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)):
a released ray of 2 gives 1 forward by the table and leaves 1/11 in the
forward register and 2/11 in each other register of the first Node, and
every Node on fills the same way, six of eleven parts forward per arrival,
so the field is whole quanta released where registers fill and nothing turns
by phase: at distance 6 the on-axis mark (7, 5, 5) clicks at ticks 19, 30,
39 and 48, amount 1 each, four clicks, and the six other marks, which need a
transverse release (1/11 per arrival) and then five forward ones, are still
dark at tick 48; light released 564, 112 escaped, 452 in the world (376 of
them in the registers of 153 Node-and-sign blocks, 76 on rays), electron 8,
momentum (0, 0, 0), every ledger line balanced,
`conserved_at_every_completed_tick` true. The same world run for 240 ticks
(the runner's `ticks` override, the same two fingerprints, registered in E6
at commit `6f357052b6c18ab186e67d0113a0c82ff8b5a99d`, 33 s)
clicks all seven marks, symmetric about the axis and the on-axis mark most:
(7, 5, 5) 27 times from tick 19, (7, 4, 5) and (7, 6, 5) 6 each from tick
82, (7, 3, 5) and (7, 7, 5) 3 each from tick 122, (7, 2, 5) and (7, 8, 5)
once each at tick 193, light 1710 in the world and 1158 escaped, the ledger
exact at every tick: the whole screen lit by the field of a charge at rest,
which A1 confronts with a source, two slits and the Born table. The phone
GIF of the 48-tick record (`render_gif.py --preset phone --side-by-side`,
15 frames) is 896,163 bytes.

**Resident content.** The simpler form, one lamp holding 8 as resident
content and releasing from its stock ([released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1),
"Resident content"), released nothing before feature 12: `SpatialEngine.begin`
scheduled a Node whose record holds stock of a source family, but
`SpatialNode.plan_cycle` returned before planning at a Node with no active
source, no field content and nothing received. Fixed on 2026-09-17 with
`field-spreading-v1` (the `resident` case of `test_field_spreading.py`); the
bound group is kept here, the electron at rest of this README's dictionary.

### Run and render

Side by side, the board on the left and the eye on the right:

```bash
PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/screen.json'), Path('runs/screen'))"
PYTHONPATH=src python tools/ray_viewer/record_sidecar.py runs/screen
python tools/ray_viewer/extract.py runs/screen --sidecar runs/screen/ray-recording.json --label "The screen: an electron at rest and seven marks" --out runs/screen/runs.json
python tools/ray_viewer/render_gif.py runs/screen/runs.json --output runs/screen.gif --contact-sheet runs/screen-contact.png --side-by-side
```

The record stays outside the tree; the fingerprints above are its register
line. A GIF is a rendering of a fingerprinted record, not evidence by
itself.

## The ring: an electron at rest as a loop

`ring.json` and `ring_open.json` are the design worlds of feature 14,
binding as a loop (`loop-binding-v1`, 2026-09-17; the rule and its
derivation in [loop binding](../../docs/LOOP_BINDING.md), the model owner's
decision in [Highlights](../../docs/HIGHLIGHTS.md#34-matter-is-emergent)
3.4). A ray never stops: an electron at rest is not rays held at a Node but
rays circulating on the smallest closed path of the lattice, a unit square,
whose corner meetings reproduce them every interval. The two files were
written before the feature and registered as
[E5](../../docs/EXPERIMENTS.md#e5-the-ring-an-electron-at-rest-as-a-loop);
their tick-by-tick states were computed by hand and pinned in
[test expectations](../../docs/TEST_EXPECTATIONS.md#loop-binding) as
`tests/test_loop_binding.py`, the engine of `main` was run once on them to
check whether it already held the ring (it did, line for line,
[loop binding](../../docs/LOOP_BINDING.md#10-what-todays-engine-does-with-the-ring)),
and the demonstration was made on 2026-09-17 when the feature landed. The
record's reading of the group, by the ray viewer's extractor
([ray viewer](../../tools/ray_viewer/README.md)): one group whose ring is
P0, P1, P2, P3, content 8, period 4, clock 2 per interval on the 8-step
circle, read from tick 1; the control reads none.

### Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| An electron at rest | Eight `electron` rays (charge -3) of amount 1 on the unit square P0 = (5,5,5), P1 = (6,5,5), P2 = (6,6,5), P3 = (5,6,5) in the plane z = 5, four circulating one way (P0 -> P1 -> P2 -> P3) and four the other, one of each sense at every corner in every interval; content 8, ring 4; nothing is held and no register exists | [Loop binding](../../docs/LOOP_BINDING.md#2-the-smallest-loop-the-unit-square); Highlights 3.4 |
| The binding | No rule of its own: the ordinary meeting of two electron rays at a corner, the outputs rule `corner`, each input's amount and phase leaving through the Port the other came in by (`"heading": "reversed"` of the other `input`), so each ray turns a quarter turn and stays on the ring; the ring is a fixed point of that table over one circuit | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1); [loop binding](../../docs/LOOP_BINDING.md#2-the-smallest-loop-the-unit-square) |
| The preparation | Eight lamps, two at each corner, each holding 1 quantum and emitting it once in the cycle of tick 0 on its sense's heading out of that corner (`corner_k_r`, `corner_k_l`), at phase 0, keeping the recoil in its `momentum` register; after tick 1 every corner holds one ray of each sense | [Funded emission](../../docs/SPATIAL_FIELDS.md#funded-emission-and-absorption) |
| Mass | The content, 8; the sum of the amounts is exact at every tick, since a meeting keeps every family's stock | Highlights 3.4, 3.28 |
| The clock | Every ray's phase advancing by the rest rate at every Link, `kerengonen.phase_advance` 2 at `phase_bits` 3 (N = 8), so that one circuit of four Links advances every phase by 8 = 0 (mod 8) and the state repeats after one circuit; at the catalog's rate 1 the state repeats after two circuits, nothing lost | [Loop binding](../../docs/LOOP_BINDING.md#3-closure-as-integer-equalities); Highlights 3.3 |
| The closure condition | Integer equalities: a partner at every corner (presence), the headings by the square's geometry, the amounts by the table, and 4 r = 0 (mod N) for the phase; under the Port form every amount and every rate closes, so the ladder needs a table that reads content, which is open | [Loop binding](../../docs/LOOP_BINDING.md#3-closure-as-integer-equalities) |
| Dispersal (the control) | `ring_open.json`: the same eight rays and lamps under the catalog's Born table at the corner (`born_steering`, the shared content steered by the phase difference between the two entry Ports) with the senses in phase, d = 0: every corner sends its whole content one way, the next corner holds one ray, no rule fires for one ray and it crosses off the square; the eight quanta leave the open board by tick 8 | [Loop binding](../../docs/LOOP_BINDING.md#4-when-it-does-not-close) |
| Momentum | Amount times heading; the two quarter turns at a corner move (2, 2, 0) at P0 and the like at the other corners, booked as that corner's source of the momentum field (`source_delta` of its cycle record), the four corners summing to zero every interval, so the world's momentum stays (0, 0, 0) exact; the recoil these bookings stand for belongs to the group's own field, which the worlds do not declare (open) | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) ("Momentum of a split"); Highlights 3.14 |
| Charge | -3 per quantum, the ledger's electron line -24; `charge x amount` is appended to the corner rule by the engine | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1) |
| The field of the electron | Not declared here: a ring ray in motion would release five headings per Node departed, one of them along the ring to the next corner, and the catalog's electron x light turn would take the ring's ray off the ring; the closure of a ring with its own field is the open point of the design | [Loop binding](../../docs/LOOP_BINDING.md#6-the-field-of-a-loop); Highlights 3.5 |

### ring.json, tick by tick

Board 12 x 12 x 11, open, `link_ticks` 1, `phase_bits` 3, rest rate 2, 16
ticks. The ticks below are the state after the tick; a ray is (heading,
amount, phase, steps, event mask, event shares).

| Tick | What is on the board |
| --- | --- |
| 1 | Every corner holds two rays of amount 1, phase 2, steps 1, each stamped by its lamp's emission (mask `1 << heading`, share 1 on that Port): at P0 headings -X and -Y, at P1 +X and -Y, at P2 +X and +Y, at P3 -X and +Y; in the cycle that follows `corner` fires at all four corners |
| 2 to 16 | The same picture at every tick: at P0 headings -X (mask 6, shares (0,1,1,0,0,0)) and -Y (mask 9, (1,0,0,1,0,0)), at P1 +X (mask 5, (1,0,1,0,0,0)) and -Y (mask 10, (0,1,0,1,0,0)), at P2 +X (mask 9) and +Y (mask 6), at P3 -X (mask 10) and +Y (mask 5), each ray amount 1, steps 1, phase 2t mod 8 (4, 6, 0, 2, ...), stamped by the corner it last left; the state after tick t + 4 is the state after tick t: the loop closes in one circuit |

At every tick: electron 8 in the world, none escaped, momentum (0, 0, 0) in
the world and in the sources (each corner books (2, 2, 0), (-2, 2, 0),
(-2, -2, 0) or (2, -2, 0) per interval and the four cancel), the charge
ledger electron -24, every audit line balanced,
`conserved_at_every_completed_tick` true; no `bound_groups` in the snapshot
and no `bound_tick`, since nothing is held and nothing names a group. The
demonstration of 2026-09-17, on the landed feature (commit
`e3f5182ea614f84ffd6eee3a0343885800cc0ce0`): `initialization_sha256`
`7908d327bd9163414cf3c019aec9919c2a0cbdb79c086b6fd081e52b69f83fa8`,
`source_sha256`
`693ba4693afc98315b18cb616f3a2a35ce272573ada7b9beb52be6bf54b71077`, every
line as pinned, the group read as content 8, period 4, clock 2 (the check
run of the same day on `main` at `c21e03e`, before the feature, had source
`5abd76ae78b2274d52679fbdbaaf1832e4af33278ef9d36e34120038240dbff6` and the
same lines).

### ring_open.json, tick by tick

The same board, lamps and rays; the rule `corner` is the catalog's Born
table on the sum of the two inputs at their phase difference, the table
output through the Port input 1 came in by and the rest output through the
Port input 0 came in by. Input 0 at a corner is the resident ray with the
lower heading index.

| Tick | What is on the board |
| --- | --- |
| 1 | As `ring.json` |
| 2 | In the cycle of tick 1 every corner read d = 0 and sent its whole content, 2, through one Port (floor(2 x 8 / 8) = 2, the rest output no ray): P0 and P1 on +Y, P2 and P3 on -Y; each corner now holds one ray of amount 2, phase 4, steps 1, and no rule fires for one ray |
| 3 to 7 | The four rays walk off the square, (5, 7 - t, 5) and (6, 7 - t, 5) on -Y, (5, 4 + t, 5) and (6, 4 + t, 5) on +Y, amount 2, phase 2t mod 8, steps t - 1 |
| 8 to 16 | The board is empty: electron 0 in the world, 8 escaped |

At every tick momentum (0, 0, 0) (the corners booked (1, 3, 0), (-1, 3, 0),
(-1, -3, 0) and (1, -3, 0) in the cycle of tick 1), every audit line
balanced, `conserved_at_every_completed_tick` true; no group read. The demonstration:
`initialization_sha256`
`deeae3635bb5924ff90f36e9996f4acd7c7b6e235a5c6315630c62a5e442e539`, the
same `source_sha256`. With the four L lamps at phase 2 instead (the senses
a quarter turn apart, d = 2, the `quadrature` case of the expectations) the
same Born table closes the ring with the Nodes, headings and amounts of
`ring.json`.

### Limits: what the worlds show and what is open

The ring held under the engine before the feature because a meeting with
outputs is already the ordinary event of Highlights 5.2 and needs no hold;
what the feature changed is the removal of the held form and its register
(the list in [loop binding](../../docs/LOOP_BINDING.md#9-the-interim-forms-and-what-feature-14-removes)),
the reading of a group from the record, and the catalog's binding entries
as corner tables. The Port form closes for every content and every rate,
so it gives no ladder; under the catalog's Born table the ring closes only
with the senses in quadrature and equal amounts, no content ladder either;
the ladder of hypothesis 12 needs the ring's turn to be produced by its own
field, which is open. The turns' momentum is booked as a source at the
corners, exact in the world's total, until the group's field carries it.
The unit-square electron with the catalog's rate 1 closes in two circuits;
whether the electron is this loop or a longer ring is A10's.

### Run and render

```bash
PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/ring.json'), Path('runs/ring'))"
PYTHONPATH=src python tools/ray_viewer/record_sidecar.py runs/ring
python tools/ray_viewer/extract.py runs/ring --sidecar runs/ring/ray-recording.json --label "The ring: an electron at rest as a loop" --out runs/ring/runs.json
python tools/ray_viewer/render_gif.py runs/ring/runs.json --output runs/ring.gif --contact-sheet runs/ring-contact.png
```

The same four lines with `ring_open` render the control. The record stays
outside the tree; the register entry E5 carries the fingerprints.

## The screen with a loop: the ring radiating on seven marks

`screen_loop.json` is the retired screen of (E) with its source in the loop
form of binding (feature 14, `loop-binding-v1`): the same board, the same
seven Detector marks and the same declaration of `light` as
`screen_spread.json` had, the source the ring of (F) with rays of amount 4,
content 32, at the catalog's rest rate 1. It is registered as
[E9](../../docs/EXPERIMENTS.md#e9-the-screen-with-a-loop-source-the-ring-radiating-on-seven-marks),
its criterion written there before the run, and pinned in isolation by
`tests/test_screen_loop.py`
([expectations](../../docs/TEST_EXPECTATIONS.md#the-screen-with-a-loop)).
Board 12 x 11 x 11, open, `link_ticks` 1, `phase_bits` 3 (N = 8), 240 ticks
in the file (E6's registered length). The marks: (7, 2, 5) through
(7, 8, 5), setting [1, 1] (every arrival clicks, none is returned), at
distance 6 along +X from P0 = (1, 5, 5) and 5 from P1 = (2, 5, 5). The
ring: the unit square P0 = (1,5,5), P1 = (2,5,5), P2 = (2,5,6),
P3 = (1,5,6) in the plane y = 5, eight `electron` lamps of amount 4 at its
corners as `ring.json` declares them with Y read as Z (the R lamps on +X at
P0, +Z at P1, -X at P2, -Z at P3, the L lamps on +Z at P0, -X at P1, -Z at
P2, +X at P3), the one rule `corner`. `light`: `field_of` `electron`,
`release` [1, 4], `spread` [6, 1, 1, 1, 1, 1], rest rate 0, charge 0, 24 ray
slots. No rule names `light`.

### Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| An electron at rest, radiating | The ring of (F) with `emissions[].amount` 4 and the lamps' `defaults.electron` 4: eight `electron` rays (charge -3) of amount 4 circulating both ways on the unit square P0, P1, P2, P3 in the plane y = 5, one of each sense at every corner in every interval, turned by `corner`; content 32; nothing is held, and the ring's meetings change nothing about the field | [Binding as a loop](../../docs/SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1); Highlights 3.4, 3.28 |
| Why content 32 | At the catalog's ratio `[1, 4]` a ray of amount a releases floor(a / 4) per heading, 0 for a < 4, so 4 is the least amount that radiates, and the electron of `ring.json` has eight rays (one of each sense at every corner): 8 x 4 = 32 is its least radiating content; the four-ray loop of E5's `half` case would radiate at 16 but is not that electron | [Loop binding](../../docs/LOOP_BINDING.md#6-the-field-of-a-loop); [E6](../../docs/EXPERIMENTS.md#e6-the-screen-the-field-of-an-electron-at-rest-on-seven-marks) (retired) |
| The clock | `kerengonen.phase_advance` 1 on `electron`, the catalog's rest rate (not `ring.json`'s 2, chosen there so that the hand table closes in one circuit): every ray at phase t mod 8 after tick t, the ring closing in two circuits (4 x 1 = 4 is not 0 mod 8), period 8, nothing lost (E5's `slow` case); the light carries this clock, so the source that lights the screen has a frequency | [Loop binding](../../docs/LOOP_BINDING.md#3-closure-as-integer-equalities); Highlights 3.3 |
| Its field, light | `light` declared `field_of` `electron` with `release` [1, 4]: every ring ray, at every corner it departs from, releases one `light` ray of amount floor(4 / 4) = 1 on each of the five Port headings other than the one it leaves on (the release is taken from the trajectory that leaves the corner meeting), with its own phase and the sign of its family's charge (`source_sign` -1), booked as a source of `light`; the ray pays nothing and the ring's content stays 32 | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1); Highlights 3.5, 3.15 |
| The radiated power | 40 quanta per interval (eight rays, five headings, 1 each) from the cycle of tick 1 (the lamps' rays are fresh at tick 0 and release nothing), 40 (t - 1) sourced by tick t, 9560 by tick 240; against E6's 12 per interval | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1) |
| The spreading | `spread` [6, 1, 1, 1, 1, 1] on `light`, the catalog's table: at every Node the arrived content is shared six of eleven forward, one backward, one to each transverse heading, the whole quanta leaving and the shares below one quantum kept in the Node's registers per sign and Port until a register reaches eleven, so the field is whole quanta released where registers fill; the amounts are exact and the phase of the departures is the coherent sum's | [Field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1); Highlights 3.5, 3.17 |
| The screen | `detectors`: seven marks at (7, y, 5), y = 2 to 8, `setting` [1, 1], `seed` 0: every arriving ray clicks (`detector_click`, the ray's family and amount, bit 1) and walks on with its bit; a ray whose bit was read at an earlier mark passes a later one without a draw (`detector_pass`) | [Detector mark](../../docs/SPATIAL_FIELDS.md#detector-mark-detector-mark-v1), [the bit as a property](../../docs/SPATIAL_FIELDS.md#the-detectors-bit-as-a-property-detector-bit-property-v1); Highlights 5.4 |
| No coupling of light with the ring | Nothing: no `ray_interactions` rule names `light`, and layers are derived, so `light` is a layer of its own and crosses the ring's Nodes unmet, spreading there like at any Node (the edge light of a corner arrives at the next corner and fills its registers). Where E1's world declares `absorb` over `[electron, electron, light]` to make the photon join the ring, this world declares no rule over `light` at all; the runner's `ray_layer_families` records the two layers | [Layers](../../docs/SPATIAL_FIELDS.md#layers-ray-layers-v1); Highlights 5.1 |
| The square edge-on to the screen | The ring in the plane y = 5, which contains the axis (1, 5, 5) to (7, 5, 5) and is perpendicular to the marks' line, rather than in the marks' plane z = 5: a unit square in z = 5 would have two Nodes at y = 6 (or 4), one of them sending an axis beam of its own along the line of the mark (7, 6, 5), and the pairs of marks could not be equal; in y = 5 the source, the marks and the split table are symmetric under y -> 10 - y exactly, so the pairs click alike, tick for tick | [Field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1) (the four transverse weights equal); Highlights 3.23 |
| Momentum | Amount times heading; the two quarter turns of a corner move (8, 0, 8) at P0, (-8, 0, 8) at P1, (-8, 0, -8) at P2, (8, 0, -8) at P3 per interval, booked as that corner's source, the four summing to zero; `light` binds no momentum field (no `recoil_field` releases it), so neither a release nor a spread books momentum, as in E6, and the world's momentum stays (0, 0, 0) exact | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) ("Momentum of a split"); Highlights 3.14 |
| Charge | -3 per electron quantum, the ledger's electron line -96; light 0; the sign travels on every field ray as `source_sign` -1 | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1); [field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1) ("The sign of the source") |
| Capacity | `ray_slots` 24 on `light` (E8's field family; the retired screen had 8 for one source Node): a corner receives field content on six Ports with up to three phases per Port (the split's, a register's, a ring ray's release) and a full slot budget aborts a run; a capacity, not a law | [Straight-ray transport](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1) |
| The group in the record | Nothing at a Node names it: the ray viewer's extractor reads the electron rays that keep meeting at the corners and reports one group, ring P0, P1, P2, P3, content 32, period 8, clock 1, over the window in which their states recur; the light that spreads at a corner is a field family and enters no group. The extractor cannot tell a spread at a corner from a meeting with the matter there (a field ray that leaves a Node changed is drawn as meeting it), so its markers at the corners are a rendering, and the engine's record is the evidence that nothing met: the derived layers, the electron line without a source, the ring's states recurring | [Ray viewer](../../tools/ray_viewer/README.md#what-the-record-must-contain); Highlights 3.4 |

### Computed before the run

The release per corner and per interval, from the two rays that leave it
(the R ray on the R sense's edge, the L ray on the L sense's edge), each
releasing 1 on the five headings other than its own, the two releases on one
heading merging into one ray (one phase, one sign, no event):

| Corner | Departing | +X | -X | +Y | -Y | +Z | -Z |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 = (1,5,5) | R +X to P1, L +Z to P3 | 1 (edge to P1) | 2 | 2 | 2 | 1 (edge to P3) | 2 |
| P1 = (2,5,5) | R +Z to P2, L -X to P0 | 2 (the axis line to (7,5,5)) | 1 (edge to P0) | 2 | 2 | 1 (edge to P2) | 2 |
| P2 = (2,5,6) | R -X to P3, L -Z to P1 | 2 (the line y = 5, z = 6) | 1 (edge to P3) | 2 | 2 | 2 | 1 (edge to P1) |
| P3 = (1,5,6) | R -Z to P0, L +X to P2 | 1 (edge to P2) | 2 | 2 | 2 | 2 | 1 (edge to P0) |

Forty per interval: 6 on each of +X, -X, +Z, -Z and 8 on each of +Y, -Y, of
which 8 run along the four edges and reach the neighbouring corners in the
next interval, where no rule meets them and they spread as at any Node, so
the corners' registers are sources of spread content too. From the cycle of
tick 1 (the lamps' rays are fresh at tick 0 and release nothing) the light
sourced by tick t is 40 (t - 1), 9560 by tick 240. The ring's period is 8
at rate 1 and every release of the cycle of tick t carries the phase t mod
8, which light's rate 0 keeps: a quantum that reaches a mark on
whole-quantum steps carries the phase of its release tick, and a quantum a
register releases carries the phase of the coherent sum of the shares that
filled it (over eight consecutive intervals of this clock the sum cancels to
step 0, and otherwise it is the phase of the shares beyond whole circles);
the phases the marks see are read from the recording below. The order of
the first clicks: the on-axis mark (7, 5, 5) first, fed by the axis line
from P1, two fresh quanta per interval plus P1's register releases (the
edge light of P0 arrives at P1 on +X and fills its +X register by 6/11 per
interval, the edge light of P2 arrives on -Z and adds 1/11), a stronger beam
than E6's 2 starting one Node nearer the screen, so before E6's tick 19;
then (7, 4, 5) and (7, 6, 5) in one tick, then (7, 3, 5) and (7, 7, 5), then
(7, 2, 5) and (7, 8, 5), each pair in the same tick with the same amount by
the mirror, the counts falling outward as E6's 27, 6, 6, 3, 3, 1, 1; the
ticks are the run's to give. Momentum (0, 0, 0), electron 32 and the charge
line -96 at every tick; light current (rays and registers) plus escaped
equal to sourced.

### screen_loop.json, tick by tick: the first clicks

Run once, 240 ticks, at commit `ed2078f` (92 s; `source_sha256`
`693ba4693afc98315b18cb616f3a2a35ce272573ada7b9beb52be6bf54b71077`,
`initialization_sha256`
`e1984daf7ff47f2cc243a8fed7d60a3717da1b7c150af49a79656150b1640ac9`), the
record read with the extractor and the recording as the lines under "Run
and render" say. Every click is of family `light`, bit 1, 28 of amount 1
and one of amount 2 (tick 63, two whole quanta merged on one Port in one
interval), 29 in all; every mark clicks, the pairs tick for tick with the
same amount (the world's mirror y -> 10 - y), the on-axis mark most:

| Mark | Clicks | Ticks | First light received |
| --- | --- | --- | --- |
| (7, 5, 5) | 17 (amount 18) | 11, 15, 18, 22, 27, 27, 31, 34, 37, 41, 42, 43, 51, 59, 63, 67, 69 | 11 (the first click) |
| (7, 4, 5) and (7, 6, 5) | 4 each | 34, 46, 54, 72 | 34 (the first click) |
| (7, 3, 5) and (7, 7, 5) | 1 each | 71 | 50 (a pass, bit 1 already) |
| (7, 2, 5) and (7, 8, 5) | 1 each | 70 | 70 (the first click) |

Tick 11: the on-axis mark clicks, through its -X face, the axis line from
P1, eight ticks before E6's held source (tick 19), as computed. The axis
line's arrivals at (7, 5, 5) follow at 15, 18, 22, 27 (two quanta, two
clicks), 31, 34, 37, 41, 42, 46, 48, 51, 52, 56, 59, 63 (amount 2), 67, 69,
71, 73, 76, 80 and on, 91 arrivals carrying 95 quanta by tick 240. Tick 34:
the first pair, (7, 4, 5) and (7, 6, 5), through their -X faces, in the same
interval as an on-axis click; they click again at 46, 54 and 72. Tick 43:
the one click not through a -X face, at (7, 5, 5) through its +Z face from
(7, 5, 6): the line y = 5, z = 6 that P2 feeds with 2 per interval, whose
-Z share at (7, 5, 6) left whole at tick 42. Ticks 70 and 71: the two outer
pairs, the outermost (7, 2, 5) and (7, 8, 5) first and (7, 3, 5) and (7, 7,
5) one interval later, once each. Tick 72: the last click of the run. From
tick 73 to 240 no mark clicks: every arrival carries bit 1 and passes (the
eye view below). The phase pattern, read from the `field_spread` record of
the mark at each click (the phase of the arrived whole, which for a single
arrival is the quantum's): on the axis 3, 1, 2, 1, 2, 2, 0 for the first
seven clicks (ticks 11 to 31), 1, 1, 1 at 34, 37 and 41, and step 2 at every
click from tick 42; off the axis step 2 at every click but the outermost
pair's (step 3); over the run 102 of the 113 spreads at the on-axis mark
record step 2 (9 step 1, one each of 0 and 3). The ring's clock t mod 8 is
not read at the marks as a rotation: the released quanta spread at every
Node on the way and reach the screen mostly as the registers' releases,
whose phase is the coherent sum's, and the sum settles at one step.

### The eye view

The extractor's eye document (`runs.json`, `eye.hits`): (7, 5, 5) 17,
(7, 4, 5) 4, (7, 6, 5) 4, (7, 3, 5) 1, (7, 7, 5) 1, (7, 2, 5) 1, (7, 8, 5)
1: seven spots, the on-axis one brightest, the pairs equal, E6's picture
with the loop as the source (E6's 240 ticks: 27, 6, 6, 3, 3, 1, 1). Beside
the 29 clicks the record holds 378 `detector_pass` events (376 of amount 1,
2 of amount 2, all bit 1): 120 at (7, 5, 5) from tick 46, 61 each at
(7, 4, 5) and (7, 6, 5) from tick 43, 42 each at (7, 3, 5) and (7, 7, 5)
from tick 50, 26 each at (7, 2, 5) and (7, 8, 5) from tick 95, mirrored
tick for tick; E6's 240-tick record had 47 clicks and 10 passes. The reason
is in the rules, not in the source: a mark is a Node that spreads, so the
clicked quantum spreads at the mark itself, and every departure of a spread
carries the combined bit of that interval's arrivals, 1 outranking 0
outranking none ([field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1),
"The combination"; [the bit as a
property](../../docs/SPATIAL_FIELDS.md#the-detectors-bit-as-a-property-detector-bit-property-v1);
Highlights 5.4), so the read bit leaves the mark on all six headings: along
the screen to the neighbouring marks (the first light to reach (7, 3, 5)
and (7, 7, 5), at tick 50, carries it already) and back toward the source,
where a Node of the axis line that receives read content in an interval
sends that interval's forward quantum on with the bit; from tick 71 every
axis-line arrival at (7, 5, 5) passes. What the eye shows is the 29 clicks;
the 378 passes are arrivals the screen had realized already, and a screen
under a dense field stops clicking, by this catalog default, once its own
read light fills the field in front of it. A finding of the record, stated
and not tuned; whether the combined bit should outrank at a spread is the
model owner's.

### The ledger

After tick 240: light sourced 9560 (40 per interval from the cycle of tick
1), current 3680 (620 on 594 rays, 3060 in the registers of 1177
Node-and-sign blocks, all of sign -1), escaped 5880; electron initial 32,
sourced 0, current 32, escaped 0, annulled 0, absorbed 0, the same at every
tick; momentum (0, 0, 0) sourced and current at every tick; the charge
line electron -96, light 0; every line balanced at every completed tick,
`conserved_at_every_completed_tick` true. On the way (sourced, current,
escaped): tick 8: 280, 264, 16; 16: 600, 530, 70; 32: 1240, 1016, 224; 48:
1880, 1406, 474; 96: 3800, 2350, 1450; 192: 7640, 3315, 4325. The record's
events: 181351 `spatial_cycle` (the corners' among them, each booking its
two quarter turns and `light` 10 in every cycle from tick 1), 98825
`spatial_sent`, 62808 `spatial_received`, 62403 `field_spread`, 5444
`spatial_escaped`, 29 `detector_click`, 378 `detector_pass`, and the host's
960 `cycle_started` and 960 `cycle_committed`; no other kind.

### The group reading

The extractor with the recording (`ray_layer_families` `[["electron"],
["light"]]` in `run.json`) reports exactly one group: ring (1, 5, 5),
(2, 5, 5), (2, 5, 6), (1, 5, 6), size 4, content 32, families `{"electron":
32}`, period 8, clock `{"electron": 1}` on 8 phase steps, from tick 1 to
tick 239, over 1912 electron chains (the eight rays, one chain per interval,
239 intervals), the light entering none; every tick row from 1 to 239
carries `bound` `{"electron": [32]}`; after tick 240 the eight electron
rays sit at the four corners, amount 4 each, phase 0 (240 = 0 mod 8), as
after tick 8. The source stayed bound and unchanged for 240 ticks while
sourcing 9560 quanta of light. The viewer's counts: 38338 rays, 960
meetings (the corners, 4 x 240), 16879 release markers, 9481 deflection
markers (field rays leaving a Node changed, the spreads), 5444 escapes, 29
clicks, 378 passes, no unknown event kind. Against the computation: the
clicks' order was the on-axis mark, then the first pair, then the outermost
pair one interval before the next (computed: the pairs from the axis
outward), and the counts 17, 4, 4, 1, 1, 1, 1 fall from the axis but the two
outer pairs are equal (computed: falling as E6's 27, 6, 6, 3, 3, 1, 1); one
click carried 2 (computed: whole quanta of 1); the passes were not
computed. The criterion of E9, written before the run, holds in every
clause; the register carries the verdict.

### Run and render

```bash
PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/screen_loop.json'), Path('runs/screen_loop'))"
PYTHONPATH=src python tools/ray_viewer/record_sidecar.py runs/screen_loop
python tools/ray_viewer/extract.py runs/screen_loop --sidecar runs/screen_loop/ray-recording.json --label "E9: the screen with a loop source" --out runs/screen_loop/runs.json
```

The record stays outside the tree; the register entry E9 carries the
fingerprints. No GIF was rendered for this record.

## A5: Coulomb's law through the spreading field

`a5_coulomb/` holds the worlds of experiment
[A5](../../docs/EXPERIMENTS.md#a5-electron-electron-repulsion-through-released-fields)
of the register, run on 2026-09-17 on `main` with feature 12b
(`field-remainder-v1`): two charged rays on antiparallel lines along x at
impact parameter b = 4, 6, 8, 12 and 16, each releasing its field `light`,
which spreads by the catalog's table, and each turned by the other's field
through the catalog's `electron_field_turn` as a momentum table
([a free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2)).
Thirteen world files, written by `make_worlds.py` beside them and never by
hand: `ee_b{4,6,8,12,16}.json` (electron-electron), `ep_b{4,6,8,12,16}.json`
(electron-positron), `nn_b4.json` (the neutral control) and
`ee_b{4,16}_nospread.json` (the check without `spread`, the E6 geometry).
`analyze.py` reads the records and evaluates the criterion clause by clause;
`record.json` is its small committed record, which `tests/test_a5_coulomb.py`
reads. The measured outcome is in the register's entry and summarized
[below](#what-the-runs-show).

### Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| An electron at speed c, momentum p along x | A ray of the family `electron_a` (or `electron_b`), rest rate 1 (`kerengonen.phase_advance` 1), charge -3 (thirds of e), amount 64, emitted once by a lamp at the board's edge along +X (or -X); its momentum is amount x heading, (64, 0, 0), the default of its momentum register | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1); [a free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2); Highlights 3.28 |
| A positron | The same ray with `charge` 3 (`electron_b` in `ep_*.json`) | catalog, `positron` |
| The neutral control | The same rays with `charge` 0 (`neutral_a`, `neutral_b`) and no coupling declared; they still release their field, so the only difference from `ee_b4.json` is the charge and the coupling | A5, "a control with a neutral family of the same rate and content" |
| Impact parameter b | The two lines are y = 24 - b/2 and y = 24 + b/2 at z = 24; the rays start at x = 0 and x = 96 and pass each other at x = 48 at tick 48 (closest approach); the transfer is read 3b later, at tick 48 + 3b | A5, "Run" |
| The field of the charge | `light_a`, `field_of` `electron_a`, `release` [1, 4]: at every Node the electron departs it releases 16 quanta on each heading but its own line, carrying its phase and its `source_sign` (-1 for the electron, +1 for the positron), set by the engine from the releaser's charge; `light_b` the same for `electron_b`, the engine naming one light family per releaser | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1); catalog, `light` |
| The field spreading in all directions | `spread` [6, 1, 1, 1, 1, 1] on both light families: every Node that light reaches releases it again on the six headings by the table, forward 6, backward 1, transverse 1 each over 11; the share below one quantum is the Node's remainder register per family, sign and Port and leaves whole when it reaches one | [Field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1), `field-remainder-v1`; Highlights 3.5, 3.17 |
| The Coulomb force, repulsion of like charges | The coupling `electron_field_turn_a` over `[electron_a, light_b]` with `"momentum_table": {"light_b": 1}` (and `_b` the mirror): every light ray of the other charge the electron meets pushes its register by +1 x amount x heading of the field ray, away from the source, and returns reversed as the recoil; no event is stamped and the amount, phase and bit are untouched | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2); catalog, `electron_field_turn` |
| Attraction of opposite charges | The same coupling with sign -1 (`ep_*.json`): the push is toward the source. The sign is read from the field ray, never from its phase: the engine gives a `when` guard no view of `source_sign` (`RAY_PROPERTIES` holds amount, heading, phase, advance, delay, family, charge and detector), so the table names the light family that carries it, one family per releaser, and the sign of the table is the sign of the charge product written before the run | catalog, `electron_field_turn`, `opposite_charge`; [field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1), "the sign of the source" |
| The momentum transfer dp(b) | The change of the ray's momentum register, read from the `ray_push` records (before and after per push), at the read-off tick; its y component is the transverse transfer along the impact axis | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2); Highlights 3.14, 3.16 |
| The deflection | The DDA walks the register: with (64, -1, 0) the ray takes one -Y Link per 64 +X Links | the same |
| The recoil | The field ray returned reversed at the push, a new event ray on the negated heading with its amount, which spreads from the next Node like every field content | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1), "the recoil" |
| Momentum, exact | The world ledger's momentum line, initial + sourced = current + escaped at every tick: the release, every spread and every push are explicitly accounted sources | [Audits](../../docs/SPATIAL_FIELDS.md#audits-ray-event-audit-v1); Highlights 3.15 |
| No self-interaction | Read from the record, not declared: a ray arriving at a Node together with content of its own light family (`spatial_received`) is a self-meeting; the coupling names the other ray's field only, so such a co-arrival is a crossing in these worlds | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1), "the heading the ray travels on" |
| The board | 97 x 49 x 49, open boundary, `phase_bits` 12 (N = 4096), `link_ticks` 1; A5 names 49^3, and the x extent is 97 so that both rays are on the board 3b past closest approach at b = 16 | A5, "Run" |

The electron amount is 64, the smallest at which the release [1, 4] gives
16 per heading and the register resolves one quantum in 64: with 256 the
same 24 ticks of `ee_b4.json` cost 130 s against 27 s (the cost grows with
the volume the field has reached, since a Node holding a remainder register
cycles every interval), so the full runs would have taken far more than the
ten minutes each allowed.

### What the runs show

Made once on 2026-09-17 (`main` at `6f35705`, feature 12b in it; the
fingerprints are in the register's entry). The transfer, the change of
each ray's momentum register in quanta on the impact axis, at the read-off
tick 48 + 3b and at the end alike:

| b | electron-electron, ray a / ray b | electron-positron, ray a / ray b | pushes | first push |
| --- | --- | --- | --- | --- |
| 4 | −3 / +3 (apart) | +3 / −3 (together) | 2 per ray: 2 quanta at tick 50, 1 at tick 53 | 50 |
| 6 | 0 / 0 | 0 / 0 | none | none |
| 8 | 0 / 0 | 0 / 0 | none | none |
| 12 | 0 / 0 | 0 / 0 | none | none |
| 16 | 0 / 0 | 0 / 0 | none | none |

Without `spread` (the check) the transfer is one whole meeting of 16 at
tick 48 + b/2 for b = 4 and for b = 16 alike, the field on the six axis
lines of its source (E6). The control's rays go straight, no push. So the
exponent of |dp(b)| over b has no value (four zeros give no logarithm),
and the fail is the outward dilution of the declared table: the field in
flight of a ray at c is a steady wake moving with it (on the line at
transverse distance 4, 2 quanta of ray a's light at x = t − 4 and 1 at
x = t − 10 at every tick t, which ray b sweeps through once, so dp(4) = 3),
thinned by floor(A × 6/11) at every Link (16, 8, 4, 2, 1, 0) with the
rest owned by the Nodes: in the control's record the +y quanta of ray a
over ticks 40 to 68 are 667, 464, 290, 87 and 29 at distances 1 to 5 and
none beyond, and at tick 96 of the b = 16 world 7572 quanta of `light_a`
are in the world, 310 in flight (the same 310 at every tick from tick 16)
and 7262 in remainder registers, which fill by 1/11 or 6/11 per arrival
and do not release during a pass. No recoil ever reaches a releaser: a
ray at one Link per interval outruns it, and the reversed field rays walk
back to the line the ray left 2b intervals earlier. A turned ray does
share Nodes with its own field: at b = 4 the first −y Link of ray a, at
tick 65, arrives with 18 quanta of `light_a` (its own release of 16 on
that heading from the Node it left, which skips the dominant-axis line
only, plus 2), then 2 and 1 at ticks 66 and 67 (its earlier transverse
releases spread forward on the new line); six co-arrivals per b = 4
world, none where nothing turned, crossings here since the coupling names
the other ray's field, pushes by the ray's own field under the catalog's
single `light` family. The momentum sum over every ray is (0, 0, 0) at
every tick of every world (the pair's release and spread sources cancel),
every ledger line balanced, `conserved_at_every_completed_tick` true. The
criterion's clauses as written: momentum sum pass; equal and opposite
pass; recoil timing fail (no return); exponent fail; signs of the
deflection fail (right at b = 4, no deflection at b ≥ 6); neutral control
pass; no self-meeting fail for a turned ray. Run times with two to four
runs in parallel on four cores: 176, 167, 183, 266 and 255 s for b = 4 to
16 (the electron-positron worlds the same within two seconds), 143 s for
the control, 21 and 35 s without spread; each viewer document
(`runs.json`) is 4 to 8 MB.

### Run and render

```bash
PYTHONPATH=src python examples/nature/a5_coulomb/make_worlds.py
for w in ee_b4 ee_b6 ee_b8 ee_b12 ee_b16 ep_b4 ep_b6 ep_b8 ep_b12 ep_b16 nn_b4 ee_b4_nospread ee_b16_nospread; do
  PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/a5_coulomb/$w.json'), Path('runs/a5/$w'))"
  python tools/ray_viewer/extract.py runs/a5/$w --label "$w" --out runs/a5/$w/runs.json
done
python examples/nature/a5_coulomb/analyze.py runs/a5/ee_b* runs/a5/ep_b* runs/a5/nn_b4 --out runs/a5/summary.json --record examples/nature/a5_coulomb/record.json
```

The records stay outside the tree (one directory per world, siblings, since
the retention registry refuses a record nested under another); the
fingerprints in the register's entry are their register line, and
`record.json` holds the integers the test pins.

## A5s: Coulomb's force law between two charges at rest

`a5_static/` holds the worlds of experiment
[A5s](../../docs/EXPERIMENTS.md#a5s-coulombs-force-law-between-two-charges-at-rest)
of the register, run on 2026-09-17 on `main` after PR #239 (features 12,
12b, 7b and 8b in it): two external bodies at rest, each radiating its light,
which spreads by the catalog's table with the Node-owned remainder, and each
absorbing the other's light in its sink with a `momentum_table` whose sign
is the charge product, so that the force is the change of a body's momentum
register per interval. A5 (the section above) ran two free rays passing each
other and found that a ray at one Link per interval outruns its own field;
Coulomb's law is a statement about charges at rest, and this run measures
the force between two static sources directly. Fifteen world files, written
by `make_worlds.py` beside them and never by hand: `pp_r{4,6,8,12,16}.json`
(two bodies of the proton's charge on the +X axis at distance r),
`pe_r{4,6,8,12,16}.json` (a proton's charge and an electron's),
`pp_d{3,4,6,8}.json` (like charges on the diagonal, B at (d, d, 0) from A)
and `p_alone.json` (the control, one body). `analyze.py` reads the records
and evaluates the criterion clause by clause; `record.json` is its small
committed record, which `tests/test_a5_static.py` reads;
`mean_field_gauss.py` is the computation made after the run, the table's
mean field at large distance ([below](#computed-after-the-run-the-split-tables-mean-field-at-large-distance)),
whose kernel `tests/test_mean_field_gauss.py` pins. The measured
outcome is in the register's entry and summarized
[below](#what-the-static-runs-show).

### Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| A charge at rest, +e (a proton) | An external body (`external_bodies`) of the family `proton_a` (or `proton_b`), `charge` 3 (thirds of e), `amount` 2^28, at rest (no `initial_momentum`), at its Node for the whole run; a declaration, not physics, with no rays of its own at its Node | [The external body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1); Highlights 3.19 |
| A charge at rest, −e (an electron's charge) | The same body of the family `electron_b`, `charge` −3 (`pe_*.json`); the body stands for the charge only, its amount is not the electron's mass | catalog, `electron`; A5s, "Run" |
| The field of the charge | `light_a`, `field_of` `proton_a`, `release` [1, 65536]: every interval the body releases one ray per Port heading of floor(2^28 / 65536) = 4096 quanta, booked as a source, carrying its `source_sign` (+1 for the proton's charge, −1 for the electron's), set by the engine from the body's declared charge; `light_b` the same for B's family, the engine naming one light family per releaser | [The external body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1), "the release"; catalog, `light` |
| The field filling space | `spread` [6, 1, 1, 1, 1, 1] on both light families: every Node that light reaches releases it again on the six headings by the table, forward 6, backward 1, transverse 1 each over 11; the share below one quantum is the Node's remainder register per family, sign and Port and leaves whole when it reaches one (`field-remainder-v1`) | [Field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1); Highlights 3.5, 3.17 |
| The Coulomb force on a charge | The body's `momentum_table`: `{"light_b": 1}` on A and `{"light_a": 1}` on B in the like-charge worlds; every ray of the other body's light that ends in the body's sink changes its momentum register by +1 × amount × heading of the arriving ray, away from the source; the push per interval is the register's change per interval, and F(r) its mean over the last 32 ticks | [The external body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1), "motion by fields only"; Highlights 3.14 |
| Attraction of opposite charges | The same tables with sign −1 (`pe_*.json`): the push is toward the source. The table names the family that carries the sign (a body's table reads no `source_sign`), and its sign is the charge product written before the run | catalog, `electron_field_turn`, `opposite_charge`; [field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1), "the sign of the source" |
| The charge absorbing the field | The body's coupling, the default `"sink"`: whatever arrives at its Node ends in its exact sink counter per family, its own returning light and the other body's alike; a perfect absorber one Node wide | [The external body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1), "the sink" |
| The charge staying at rest | The body's velocity is its momentum over its amount, an exact accumulator per axis that steps one Link at a whole amount: with 2^28 no Link completes in these runs (`positions` per tick in `run.json`) | the same, "motion by fields only" |
| Newton's third law | The bodies' momentum line of the ledger, the sum of the two registers, and the two registers read per tick from the `external_body_absorbed` records | [Audits](../../docs/SPATIAL_FIELDS.md#audits-ray-event-audit-v1) |
| Momentum, exact | The world ledger's momentum line, initial + sourced = current + escaped + absorbed at every tick: the release, every spread and every absorption are explicitly accounted; the momentum field is bound to the light by one unseeded lamp per light family (`idle_light_a`, an emission of amount 1 with `recoil_field` that is never seeded), the engine's one way to bind it; every value of the line is zero by the mirror symmetry of each world | [Field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1), "the booking"; Highlights 3.15 |
| The control | `p_alone.json`: one body, its table naming its own light `{"light_a": 1}`; its backward-spread light returns to it from all sides and the register must stay (0, 0, 0) by symmetry | A5s, "Run" |
| The lattice's anisotropy | The diagonal worlds `pp_d{d}.json`, B at (5 + d, 5 + d, 5): the push along the diagonal (F_x = F_y by symmetry) against the axis fit at the same Euclidean distance d√2 | Highlights 3.5, 3.23; A6 |
| The board | [r + 11, 11, 11] Nodes (the diagonal [d + 11, d + 11, 11], the control [11, 11, 11]), open boundary, a margin of 5 empty Nodes beyond each body on every side, `phase_bits` 3 (no phase is read), `link_ticks` 1; the far field escapes at the boundary | A5s, "Run" and its deviations |

The release, the amount, the margin, the ticks and the phase width differ
from the run the register planned, each for a stated reason (the body's
accumulator, the engine's cost of 2.3 ms per Node cycle with the whole board
cycling): the register's entry states every deviation before the run, with
a mean-field estimate of what each costs.

### What the static runs show

Made on 2026-09-17 on the branch at `b701ea7` (`main` at `1868324` with the
planned entry; the source fingerprint and the fifteen initialization
fingerprints are in the register's entry). The push per interval on B, the
change of its momentum register per tick averaged over the last 32 ticks,
F(r) in quanta per interval (the window sum is the record's integer, F its
32nd part):

| r | F(r), like charges (`pp_r`) | opposite charges (`pe_r`) | r² F | window sum | first push at tick | B's register at the end |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | +742.81 | −742.81 | 11885 | 23770 | 4 | 27214 |
| 6 | +252.81 | −252.81 | 9101 | 8090 | 6 | 9608 |
| 8 | +89.75 | −89.75 | 5744 | 2872 | 8 | 3501 |
| 12 | +13.19 | −13.19 | 1899 | 422 | 12 | 522 |
| 16 | +2.41 | −2.41 | 616 | 77 | 18 | 91 |

A's register is the negative of B's at every tick of every world, and the
opposite-charge series is the exact negation of the like-charge series, tick
by tick (the two light fields are the same in both, only the tables' sign
differs). The log-log least-squares exponent of F over r is −4.14 ± 0.37
(standard error from the five points), against the criterion's −2.0 ± 0.2:
the exponent clause fails; the ledger, the control, the equal and opposite
registers and the signs pass. The diagonal series, B at (d, d, 0):

| d | distance d√2 | F on B | \|F\| | axis fit at d√2 | ratio | first push at tick |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 4.24 | (94.34, 94.34, 0) | 133.42 | 849.2 | 0.157 | 6 |
| 4 | 5.66 | (47.16, 47.16, 0) | 66.69 | 257.9 | 0.259 | 8 |
| 6 | 8.49 | (13.97, 13.97, 0) | 19.75 | 48.09 | 0.411 | 12 |
| 8 | 11.31 | (4.94, 4.94, 0) | 6.98 | 14.61 | 0.478 | 19 |

The push is along the diagonal exactly (F_x = F_y, F_z = 0; the window sums
3019, 1509, 447 and 158 on both axes) and a small fraction of the axis fit
at the same Euclidean distance, rising with d: the lattice's anisotropy of
the split table at short range, where the field on an axis is mostly the
forward share that never scatters.

What the integers say (a reading, not a clause): the mean-field transport of
the split table, run before the run to size it (the register's entry),
predicted F = 742, 252, 89, 13.1 and 2.4, the exponent −4.2 ± 0.4 and the
diagonal ratios 0.16, 0.26, 0.41 and 0.47 at these settings; the engine
gives the same to within a quantum per interval. The forward share that
never scatters, 4096 × (6/11)^(r−1) on the axis, is 665, 198, 59, 5.2 and
0.46 quanta per interval at r = 4 to 16: the first push at r = 4 is 664 at
tick 4, then 665, and the pushes rise to 750 by tick 40 as the scattered
part builds up; at r = 16 the forward share is below one quantum, so the
first quantum reaches B at tick 18, through the remainder registers, and
the push is 1 to 4 per tick to the end, still rising. The rest of F, 78,
55, 31, 8.0 and 1.9, is the scattered field, which the open boundary at the
margin of 5 drains and which has not reached its steady state at the far r
in 2r + 32 ticks (the mean field at the plan's settings gives −3.7 ± 0.3 and
in free space at its steady state −3.2 ± 0.1). So the fail is the short
range of the declared table: at these r the force falls like the forward
share, e^(−r/1.65), and the 1/r² flux of Gauss is the small diffusive
remainder. The control's body absorbs its own returning light (378
absorptions in 64 ticks) with its register at (0, 0, 0) at every tick. The
ledger at the end of `pp_r4`, `light_a`: sourced 983040 (6 × 4096 × 40) =
current 421226 + escaped 383590 + absorbed 178224, and the same for
`light_b`; at the end of `pp_r16`: 1572864 = 492494 + 837246 + 243124; the
momentum line and the bodies' momentum line (0, 0, 0) throughout; every
line balanced, `conserved_at_every_completed_tick` true in every world;
both bodies at their Nodes at every tick, no step. Run times with two runs
in parallel on four cores shared with other work: 156, 197, 239, 341 and
448 s for `pp_r4` to `pp_r16`, 154, 328, 247, 342 and 443 s for `pe_r4` to
`pe_r16`, 209, 264, 396 and 570 s for the diagonal d = 3 to 8, 111 s for
the control; each viewer document (`runs.json`) is 136 MB (the control) to
582 MB (d = 8), the field's rays being the record.

### Computed after the run: the split table's mean field at large distance

`mean_field_gauss.py` (2026-09-17, a computation and not an engine run)
settles what the table gives beyond the run's reach: the catalog's split as
the linear map it is on average (the remainder rule realizes it exactly on
average, so this is the expectation of the engine's integers), per-heading
amounts on the cubic lattice in floating point, the source releasing 4096 on
each heading every interval and absorbing what returns to it, a sink
absorbing everything that arrives and booking amount × heading, the open
faces absorbing; the steady states are the fixed points of the linear map
(BiCGSTAB to a residual of 10^−10) and the transients are stepped. Four
computations: the source alone in an octant of the cube of half-width 96
(193³, the boundary 2r beyond r = 48), with the simple walk [1, 1, 1, 1, 1,
1] in the same box for the Green's function of the lattice Laplacian; the
sink at r = 4 to 32 with the boundary 2r from both bodies; the time to 90 %
of the steady push; and the split of every push into the beam
4096 × (6/11)^(r−1) and the rest. The verdict: the table gives Gauss's
law, exactly for the Link current through every closed surface and as 1/r²
on the axis from r ≈ 21 on, reached after about 1.5 r² intervals; the run's
window r = 4 to 16 is the beam's and shows −2 at no box size and no
duration. CPU 607 s for the four computations on one core (and 244 s for the
free-space part alone with its Link-current column, added after).

Free space (the source alone; S = 20132 per interval is the effective
source, 24576 released less 4444 returning to the source's sink; the outflow
through the cube of half-width r equals S to 10^−7 at r = 2 to 64). J is the
net momentum arriving at the Node on the axis (amount × heading of the
arrivals, what a sink absorbs and a met ray feels); Φ is the Link current
through it, exactly 8/11 of J at every Node (on an axis the two Links'
currents sum to J + (g₊ − g₋) = J (1 + 5/11), the transverse shares
cancelling; in general J = 2 Φ / (1 + c) for the table's persistence cosine
c = 5/11, and 2 Φ for the simple walk), so Gauss's S/(4π r²) is the Link
current; n is the density and n_simple the simple walk's, scaled by
D_simple / D = 3/8 (D = 4/9 Link² per interval):

| r | J | J / Gauss | Φ / Gauss | beam / J | n / (3/8 n_simple) | local exponent of J |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 701.30 | 7.00 | 5.09 | 0.948 | 1.804 | −2.33 |
| 6 | 252.37 | 5.67 | 4.12 | 0.784 | 1.463 | −3.09 |
| 8 | 100.09 | 4.00 | 2.91 | 0.588 | 1.242 | −3.51 |
| 12 | 24.18 | 2.17 | 1.58 | 0.215 | 1.072 | −3.23 |
| 16 | 10.276 | 1.64 | 1.19 | 0.045 | 1.031 | −2.56 |
| 24 | 4.024 | 1.45 | 1.05 | 0.0009 | 1.013 | −2.12 |
| 32 | 2.211 | 1.41 | 1.03 | 0.0000 | 1.010 | −2.05 |
| 48 | 0.979 | 1.41 | 1.02 | 0.0000 | 1.010 | — |

The scattered part exceeds the beam from r = 9. The log-log exponent of J
over windows of r: 2..4 −1.55, 3..6 −2.24, 4..8 −2.81, 6..12 −3.41, 8..16
−3.31, 12..24 −2.55, 16..32 −2.19, 24..48 −2.04 ± 0.004; the local exponent
stays within −2.0 ± 0.2 from r = 21 on and within ± 0.1 from r = 26 on; over
the run's r = 4, 6, 8, 12, 16 it is −3.11 ± 0.11. Off the axis, Φ / Gauss is
1.01, 0.99, 0.99 on the (1, 1, 0) diagonal at r = 11.3, 22.6, 33.9 and 0.93,
0.97, 0.98 on the (1, 1, 1) diagonal at r = 13.9, 20.8, 27.7: the current is
isotropic to 5 % from r ≈ 24 and to 3 % from r ≈ 30, the axis above and the
diagonals below. The axis flux in the cube of half-width 64 is within 0.1 %
of the half-width 96 value at r ≤ 16 and 1.1 % at r = 32.

The point sink at r (the boundary 2r from both bodies; F the net momentum
absorbed per interval at steady state; t50, t90 and t99 the first tick at
which the push reaches that fraction of it, t99 beyond 3 r² + 64 ticks from
r = 12; the last two columns the push at the run's 2r + 32 and the plan's
2r + 64 ticks as a fraction of the steady state):

| r | F | r² F | beam / F | (F − beam) r² | F / J | local exponent | t50 | t90 | t99 | t90 / r² | at 2r + 32 | at 2r + 64 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 753.10 | 12050 | 0.883 | 1414 | 1.074 | −2.54 | 4 | 6 | 22 | 0.38 | 99.8 % | 100 % |
| 6 | 269.09 | 9687 | 0.735 | 2568 | 1.066 | −3.24 | 6 | 16 | 74 | 0.44 | 97.5 % | 99.1 % |
| 8 | 106.11 | 6791 | 0.555 | 3025 | 1.060 | −3.53 | 8 | 44 | 170 | 0.69 | 91.5 % | 95.8 % |
| 12 | 25.32 | 3647 | 0.206 | 2897 | 1.047 | −3.01 | 34 | 164 | — | 1.14 | 65.2 % | 77.8 % |
| 16 | 10.667 | 2731 | 0.043 | 2613 | 1.038 | −2.33 | 94 | 354 | — | 1.38 | 35.3 % | 51.4 % |
| 24 | 4.149 | 2390 | 0.0009 | 2388 | 1.031 | −2.09 | 246 | 866 | — | 1.50 | 7.8 % | 16.8 % |
| 32 | 2.272 | 2327 | 0.0000 | 2327 | 1.028 | — | 450 | 1564 | — | 1.53 | 1.5 % | 4.4 % |

The exponent of F over r ≥ 12 is −2.44 ± 0.13, over r ≥ 16 −2.24 ± 0.07,
and over the run's r = 4 to 16 at steady state −3.14 ± 0.11: the run's window
shows the beam at any box size and any duration (the boundary at 3r and 4r
raises F by 0.4 and 0.5 % at r = 8, 1.2 and 1.5 % at r = 12, 1.7 and 2.2 % at
r = 16). The rest, (F − beam) r², is the diffusive field, converging from
above to about 11/8 × 1.03 × S/(4π) ≈ 2300. The time to 90 % scales as
t90 ∝ r^2.29 ± 0.09 over r ≥ 12 (r^2.76 ± 0.10 over all r, the near r being
the beam's at tick r + 2), t90 / r² rising to 1.53 at r = 32 against the
continuum's 1.93 r² for D = 4/9: the field is diffusive, not ballistic. At
the engine's measured 2.3 ms per Node cycle, a world with the boundary 2r
away run to t90 costs 342 k Nodes × 354 ticks ≈ 78 hours at r = 16, 1.14 M
× 866 ≈ 26 days at r = 24 and 2.68 M × 1564 ≈ 110 days at r = 32: the
field of a charge at rest is established, in this table's sense, at no r
the engine reaches today, and the exponent clause can be met only from r ≈
24 up.

### Run and render

```bash
PYTHONPATH=src python examples/nature/a5_static/make_worlds.py
for w in pp_r4 pp_r6 pp_r8 pp_r12 pp_r16 pe_r4 pe_r6 pe_r8 pe_r12 pe_r16 pp_d3 pp_d4 pp_d6 pp_d8 p_alone; do
  PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/a5_static/$w.json'), Path('runs/a5s/$w'))"
  python tools/ray_viewer/extract.py runs/a5s/$w --label "$w" --out runs/a5s/$w/runs.json
done
python examples/nature/a5_static/analyze.py runs/a5s/pp_r* runs/a5s/pe_r* runs/a5s/pp_d* runs/a5s/p_alone --out runs/a5s/summary.json --record examples/nature/a5_static/record.json
```

The computation after the run (about ten minutes on one core; `--only-free`
for the free-space part alone, `--out` for the tables as JSON):

```bash
OPENBLAS_NUM_THREADS=1 python examples/nature/a5_static/mean_field_gauss.py
```

The records stay outside the tree (one directory per world, siblings, since
the retention registry refuses a record nested under another); the
fingerprints in the register's entry are their register line, and
`record.json` holds the integers the test pins.

## A12: Malus's law and the three-polarizer chain

`a12_malus/` holds the worlds of experiment
[A12](../../docs/EXPERIMENTS.md#a12-maluss-law-and-the-three-polarizer-chain-after-feature-11)
of the register, run on 2026-09-17 on the branch of feature 11
(`ray-polarization-v1`, [polarization](../../docs/SPATIAL_FIELDS.md#polarization-ray-polarization-v1))
merged with `main` after PR #248: a marked source sends a beam of light
polarized along +Y through one polarizer, or a chain of them, to a marked
Node behind the last one; every polarizer is an external body under the
polarizer coupling, which splits each arriving ray by the declared table at
the difference between the body's angle and the ray's polarization, the pass
share leaving with the body's angle as its polarization, the rest ending in
the body's sink and the shares below one quantum owned by the body's
registers until they reach one. Eight world files, written by
`make_worlds.py` beside them and never by hand: `single_{0,22,45,67,90}.json`
(one polarizer at 0°, 22.5°, 45°, 67.5°, 90°), `chain_90.json` (y, 90°),
`chain_45_90.json` (y, 45°, 90°) and `chain_22_45_67_90.json` (y, 22.5°,
45°, 67.5°, 90°). `analyze.py` reads the records and evaluates the
criterion clause by clause; `record.json` is its small committed record.
The measured outcome is in the register's entry and summarized
[below](#what-the-malus-runs-show).

### Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| A polarized beam of light | A lamp (`source`, holding 2048 quanta) on a marked Node (`detectors`, setting [1, 1], a source is a Detector) at (2, 4, 4), emitting 256 quanta per interval along +X for eight intervals at phase 0, `polarization` 0 on the emission; `light` declares no `spread`, so the beam stays on its line | [Polarization](../../docs/SPATIAL_FIELDS.md#polarization-ray-polarization-v1), "where it comes from"; A12, "Run" and deviation (v) |
| Polarization along y | The step 0 of light's polarization circle: the first transverse lattice axis of the heading +X in Port order, +Y; the circle has 2^`phase_bits` = 256 steps per half turn (the default, no `polarization_bits` written), 180/256 degrees each, so 22.5°, 45°, 67.5°, 90° are the steps 32, 64, 96, 128 | the same, "the property"; catalog, `light.polarization` |
| A polarizer at angle theta | An external body (`external_bodies`) of the family `apparatus`, amount 1, `coupling` `"polarizer"`, `polarizer` {`family` light, `angle` theta in steps, `pass` [1, 0, 0], `table`}; a declaration, not physics; at x = 12, 22, 32, 42 on the beam's line | [The external body](../../docs/SPATIAL_FIELDS.md#the-external-body-external-body-v1); [polarization](../../docs/SPATIAL_FIELDS.md#polarization-ray-polarization-v1), "the polarizer"; Highlights 3.19 |
| Malus's law, I = I₀ cos²(theta − theta_ray) | The body's `table`: entry d is round(256 cos²(d × 180 / 256 degrees)), the pass share in 256-ths at the difference d = (angle − polarization) mod 256; the engine only splits by the table, floor(amount × T[d] / 256) passing | catalog, `polarizer`; A12, deviation (ii) |
| The transmitted beam | The pass ray: a fresh event of the body's Node on +X with the passed amount, the ray's phase and the body's angle as its polarization, one Link on with the residents | the same, "the polarizer" |
| The absorbed part | The rest, floor(amount × (256 − T[d]) / 256), in the body's sink counter for `light`, the audit's `absorbed_by_bodies` line, one `external_body_absorbed` record per arrival | the same; [audits](../../docs/SPATIAL_FIELDS.md#audits-ray-event-audit-v1) |
| The fraction below one photon | The two shares below one quantum, in 256-ths, in the body's registers (`held`, pass and sink per source sign), one quantum in total, released whole to the pass Port or the sink when a register reaches 256; counted as current content by the ledger | the same; Highlights 3.17; feature 12b's rule |
| The photodetector behind the polarizer | The marked Node at (52, 4, 4), setting [1, 1]: every arrival passes and clicks (`detector_click`), the content that clicks is the transmitted intensity; what passes escapes through the open face at x = 64 | [Detector mark](../../docs/DETECTOR_SAMPLING.md); A12, "Recorded" |
| The chain | Two or four polarizer bodies ten Links apart on the beam, each reading the polarization the previous one set | A12, "Run" |
| Intensity exact | The world ledger: initial + sourced = current + escaped + absorbed at every tick, the registers on the `current` line; every `polarizer` record: amount = passed + sunk + the whole quantum its two fractions make | [Audits](../../docs/SPATIAL_FIELDS.md#audits-ray-event-audit-v1); Highlights 3.15 |
| The board | [65, 9, 9] Nodes, open boundary, the beam on the axis y = 4, z = 4, `phase_bits` 8 (the phase is read nowhere), `link_ticks` 1, 72 ticks | A12, "Run" and deviation (vi) |

### What the Malus runs show

Made on 2026-09-17 at commit `54d1593` (the feature's `cd4d971` merged with
`main` at `b64de24`; the source fingerprint and the eight initialization
fingerprints are in the register's entry). The content that clicked behind
the polarizer of 2048 emitted, against the table's exact integer rule
(computed by `analyze.py` from the world file alone) and Malus's cos² in
floating point:

| World | Angles | Clicked | Fraction | Table rule | Malus | Sunk | Held at the end |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `single_0` | 0° | 2048 | 1.0000 | 2048 | 2048.0 | 0 | 0 |
| `single_22` | 22.5° | 1752 | 0.8555 | 1752 | 1748.1 | 296 | 0 |
| `single_45` | 45° | 1024 | 0.5000 | 1024 | 1024.0 | 1024 | 0 |
| `single_67` | 67.5° | 296 | 0.1445 | 296 | 299.9 | 1752 | 0 |
| `single_90` | 90° | 0 | 0.0000 | 0 | 0.0 | 2048 | 0 |
| `chain_90` | y, 90° | 0 | 0.0000 | 0 | 0.0 | 2048 | 0 |
| `chain_45_90` | y, 45°, 90° | 512 | 0.2500 | 512 | 512.0 | 1536 | 0 |
| `chain_22_45_67_90` | y, 22.5°, 45°, 67.5°, 90° | 1095 | 0.5347 | 1095 | 1087.1 | 950 | 3 |

The table's entries at 22.5°, 45°, 67.5° and 90° are 219, 128, 37 and 0 in
256-ths (0.8555, 0.5, 0.1445, 0 against cos² 0.8536, 0.5, 0.1464, 0: the
rounding of the declared table, of a quantum in 256, is the whole distance
between the singles and Malus). Every pulse is 256 quanta, a multiple of the
table's denominator, so a single polarizer splits exactly and its registers
stay empty; from the second polarizer of a chain on, the amounts are not
multiples and the remainder rule works: in the chain of four the polarizers
passed 1752, 1498, 1281 and 1095 and sank 296, 253, 216 and 185, their
registers releasing 2 + 5, 7 + 0 and 5 + 2 whole quanta to the pass Port and
the sink over the eight pulses and holding, at the end, 200 + 56, 126 + 130
and 219 + 37 in 256-ths, one quantum each, so 1095 + 950 + 3 = 2048. The
chain's fraction 0.5347 lies between cos⁸(22.5°) = 0.5308 and the table's
compounded (219/256)⁴ = 0.5356, the floors withholding the difference: it is
the table's value to the quantum, and the rounding of cos² to 219/256,
compounded four times, is the whole distance from Malus. The chain y, 45°,
90° passes a quarter exactly, neither 0 nor a half: the polarization a ray
carries is the direction the last polarizer set, and the intermediate
polarizer's angle is carried through the chain. Every ledger line balances
at every tick of every world and every `polarizer` record is exact. The
polarization of every ray leaving each polarizer is the body's angle, on
every segment of the viewer documents. Run times 0.08 to 0.34 s per world.

### Run and render

```bash
PYTHONPATH=src python examples/nature/a12_malus/make_worlds.py
for w in single_0 single_22 single_45 single_67 single_90 chain_90 chain_45_90 chain_22_45_67_90; do
  PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/a12_malus/$w.json'), Path('runs/a12/$w'))"
  PYTHONPATH=src python tools/ray_viewer/record_sidecar.py runs/a12/$w
  python tools/ray_viewer/extract.py runs/a12/$w --label "$w" --out runs/a12/$w/viewer/runs.json
done
python examples/nature/a12_malus/analyze.py runs/a12/single_* runs/a12/chain_* --out runs/a12/summary.json --record examples/nature/a12_malus/record.json
```

The sidecar (`ray-recording.json`) gives the viewer each ray's polarization;
the records stay outside the tree, the fingerprints in the register's entry
are their register line, and `record.json` holds the integers.
