# Two events of nature in the engine's language

Eight world files that show, on the one generic engine and with the rules
that exist today, (A) a photon absorbed by an electron at rest, (B) a nucleus
split by a high-energy photon, with a low-energy photon that does not split it
as the control, (C) the photon of (A) held inside the group while its
clock runs and then emitted on a new heading, the group back in its ground
state, (D) the helium ion, a nucleus of charge +2 with one electron,
[below](#the-helium-ion-one-electron-at-a-nucleus-of-charge-2), (E) the
field of an electron at rest on a screen of seven Detector marks, the eye
view's first picture,
[below](#the-screen-the-field-of-an-electron-at-rest-on-seven-marks), and
(F) the ring, an electron at rest as a loop of rays on a unit square, with
the control that disperses, the design world of feature 14,
[below](#the-ring-an-electron-at-rest-as-a-loop), and (G) the worlds of
experiment A5, two charged rays passing each other through their spreading
fields, in `a5_coulomb/`,
[below](#a5-coulombs-law-through-the-spreading-field). (A) to (F) are demonstrations under
[Highlights](../../docs/HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions)
5.5: research runs made once, recorded with their fingerprint in the
[experiments register](../../docs/EXPERIMENTS.md#e-demonstrations-of-events)
((E) in its section here), never repeated as tests, and (G) is a confrontation
run of section A of the register. Nothing here is a law of nature; every number is a
declaration written before the run.

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
| An electron at rest | A bound group: two `electron` rays (rest rate 1, charge -3) held at one Node by the binding rule `bind`, a rule without outputs whose assignments set `delay` 1 on both; its content is the sum of their amounts (4 + 4 = 8), its clock is each phase advancing by the rest rate once per interval, and its mass as an output-clock delay is the rule's `ray_delay` 1 | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.4, 3.28 |
| The photon arrives | The light ray reaches the group's Node and waits the group's `ray_delay` (one interval) before it meets anything: the group's output clock, not a kinematic rule | [Mass as output-clock delay](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.28 |
| Absorption | The coupling declared for the families present when the light arrives: the rule `excite`, a binding rule over `[electron, electron, light]` declared before `bind`; it fires with zero events, so the light ray ends at the Node and stays in the group. The literal conversion of the light's amount into electron content is refused by two generic rules (see Limits) | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.4 ("Binding is the interaction whose result is zero events") |
| The excited electron | The bound group `[electron, electron, light]`: content 8 to 11 (the `bound_tick` record's `amounts`), the Node's output clock `ray_delay` 1 to 3 (a slower clock: every ray of matter that arrives now waits three intervals), the light's phase held at 0 while the electron phases keep advancing | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.28 ("Speed is a clock slowing") |
| Emission | The outputs rule `emit` over the bound `[electron, electron, light]`, declared before `excite` (rules fire in declared order and a ray one rule used is not available to the next in that interval, so `emit` must come first; while its guard is false `excite` holds the group), fired by the group's clock: its guard `"when": {"op": "eq", "args": [{"field": "phase", "participant": 0}, 1]}` is true in the interval the electron phase reads 1. Its outputs are the light ray leaving through Port 0 (+X, a new heading, so it reads as emission) with the group's phase at emission (`"phase": {"of": 0}`, Highlights 3.3: the frequency of light is the rate of its emitter's clock), and the two electron rays with `delay` 1, which stay at the Node one interval and are re-bound by `bind` in the next; "outputs where two participants stay bound" is this one rule plus the existing binding rule, with `ray_delay` reading 0 for the one tick in between | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) (`delay` on an output); Highlights 3.4 |
| Lifetime of the excited state | Declared and deterministic: the intervals until the electron phase reaches the guard's value (five here, from the excitation at phase 4 through 5, 6, 7, 0 to 1). The half-life draw of Highlights 3.26, a decaying group as a source and a source as a Detector drawing at each tick, is not in the engine: a Detector mark draws on arrivals through Ports only, never at a resident group's tick. That draw is the missing rule for a random lifetime | Highlights 3.26; [Detector mark](../../docs/SPATIAL_FIELDS.md#detector-mark-detector-mark-v1) |
| Recoil of the emission | Momentum exact by heading: the light leaves with (4, 0, 0) and one electron's heading turns from +X to +Y, so the group holds (-4, 4, 0) in its rays' headings, the photon's original (0, 4, 0) less what left; a bound group does not move (hypothesis 15 is open), so the recoil is bookkeeping in the group. This is why the light's amount is 4 in `absorption_emission.json` (3 in `absorption.json`): equal to an electron's amount, so that one heading carries it | Highlights 3.14, 3.16 |
| A two-body nucleus | A bound group of one `proton` ray (charge +3) and one `neutron` ray (charge 0) held by the binding rule `strong` (`delay` 1, `ray_delay` 1) | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.4 |
| Photofission | The outputs rule `photofission` naming the bound proton, the bound neutron and the arriving light ray, declared before `strong`: three new event rays leave the Node, the proton through Port 2 (+Y) and the neutron through Port 3 (-Y), on opposite headings by the Port table, the light continuing on its heading (`"same"`); nothing is left at the Node and `strong` no longer fires | [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1), [unbinding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.4 |
| The fragments | The rule's outputs: each a fresh trajectory with `steps` 0, stamped with the event's Ports and shares | [Ray state](../../docs/SPATIAL_FIELDS.md#ray-state-ray-event-state-v1) |
| The threshold | The rule's guard, `"when": {"op": "gt", "args": [{"field": "amount", "participant": 2}, 3]}`: the rule fires only when the light's amount exceeds 3, that is, is at least 4. The schema already has this amount condition, read at the meeting and nowhere else, so no new key was added. A false guard is no interaction: the light crosses | [Local updates and expressions](../../docs/DISTURBANCES.md#local-updates-and-expressions) (`gt`); [Meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1) ("A false guard leaves the group untouched") |
| The control photon | A second light lamp of amount 2, below the threshold, arriving first: it waits the nucleus's clock, crosses the Node unchanged and walks on; the group stays and ticks | [Layers](../../docs/SPATIAL_FIELDS.md#layers-ray-layers-v1), Highlights 5.1 |
| Energy | The amount; the declared invariant `energy` (`{"field": "amount"}`), exact as a sum over inputs and outputs | Highlights 3.15 |
| Momentum | Amount times heading, the declared invariant `momentum`, exact component by component; every lamp keeps its recoil in its `momentum` register (`recoil_field`), so the world's total is (0, 0, 0) at every tick and the runner's `conserved_at_every_completed_tick` is true | Highlights 3.14, 3.16 |
| Charge | The family's charge per quantum in thirds of e; `charge x amount` summed over a meeting's rays is appended by the engine to every rule's invariants | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1) |
| Speed | One Link per interval for every ray, light and matter alike; matter is slower only by an output-clock delay (`ray_delay`) | Highlights 3.28 |
| An event | A change of trajectory leaving a meeting; in the viewer a marker at the Node. A crossing is no event | [Ray-event model](../../docs/RAY_EVENT_MODEL.md#1-definitions) |

## absorption.json, tick by tick

Board 21 x 21 x 21, open, `link_ticks` 1, `phase_bits` 3 (N = 8), 12 ticks.
Lamps: two electron lamps at (9, 10, 10) heading +X and (11, 10, 10) heading
-X, amount 4 each; one light lamp at (10, 4, 10) heading +Y, amount 3. Rules
in order: `excite` (binds `[electron, electron, light]`, `ray_delay` 3), then
`bind` (binds `[electron, electron]`, `ray_delay` 1). The ticks below are the
state after the tick; the event stream stamps each Node cycle with the tick it
started at, so the `bound_tick` that shows the state of tick t carries tick
t - 1.

| Tick | What is on the board |
| --- | --- |
| 1 | The two electron rays have crossed their one Link and are both at (10, 10, 10) (`steps` 1); the light ray is at (10, 5, 10) |
| 2 | `bind` has fired: the group `[electron, electron]`, amounts [4, 4], phases [2, 2], `ray_delay` 1; from here it ticks every interval, each phase +1 |
| 6 | The light ray arrives at (10, 10, 10) with amount 3 and `delay` 1, the group's clock; the group ticks on (phases [6, 6]) |
| 7 | The light's wait is over (`delay` 0, phase 0, `steps` 6); in the cycle that follows, `excite` fires over the three rays with zero events |
| 8 | The group is `[electron, electron, light]`, amounts [4, 4, 3] (content 11), phases [0, 0, 0], `ray_delay` 3; the light ray has `steps` 0 and its trajectory has ended at the Node |
| 9 to 12 | The excited group ticks every interval: the electron phases advance to 1, 2, 3, 4, the light's stays 0, `ray_delay` stays 3 |

At every tick: totals electron 8, light 3, momentum (0, 0, 0); the charge
ledger electron -24 (= -3 x 8); every line of the audit balanced;
`conserved_at_every_completed_tick` true. The light lamp keeps the recoil
(0, -3, 0) and the held light ray reads (0, 3, 0): the photon's momentum is
in the group.

## absorption_emission.json, tick by tick

Board 11 x 11 x 11, open, `link_ticks` 1, `phase_bits` 3, 14 ticks. Lamps:
two electron lamps at (4, 5, 5) heading +X and (6, 5, 5) heading -X, amount 4
each; one light lamp at (5, 2, 5) heading +Y, amount 4. Rules in order:
`emit` (the outputs rule with the guard on the electron phase), `excite`
(binds `[electron, electron, light]`, `ray_delay` 3), `bind` (binds
`[electron, electron]`, `ray_delay` 1).

| Tick | What is on the board |
| --- | --- |
| 1 | The two electron rays are at (5, 5, 5); the light ray is at (5, 3, 5) |
| 2 | `bind` has fired: the group `[electron, electron]`, amounts [4, 4], `ray_delay` 1 |
| 3 | The light ray (amount 4) arrives at (5, 5, 5) and waits the group's clock (`delay` 1) |
| 4 | Its wait is over; in the cycle that follows the guard of `emit` reads phase 4 as false and `excite` fires with zero events |
| 5 to 9 | The group `[electron, electron, light]`, amounts [4, 4, 4], `ray_delay` 3; the electron phases 5, 6, 7, 0, 1, the light's 0: the photon sits inside while the group ticks |
| 9 | In the cycle that follows, the electron phase reads 1: `emit` fires; the light leaves through +X with phase 1, the electrons stay with `delay` 1, one of them now on +Y |
| 10 | The light is at (6, 5, 5) heading +X, phase 1, `steps` 1; the two electrons are at (5, 5, 5), `ray_delay` 0 for this one tick, since no binding rule fired in the cycle before |
| 11 | `bind` has re-formed the ground group: amounts [4, 4], `ray_delay` 1, phases [3, 3], headings -X and +Y; the light is at (7, 5, 5) |
| 12 to 14 | The ground group ticks; the light walks to (10, 5, 5) at tick 14 |

At every tick: totals electron 8, light 4, momentum (0, 0, 0), the charge
ledger electron -24, every audit line balanced,
`conserved_at_every_completed_tick` true. Photon in, held five intervals,
photon out on a new heading, the group back in its ground state.

## photofission.json, tick by tick

Board 21 x 21 x 21, open, `link_ticks` 1, `phase_bits` 3, 16 ticks. Lamps: a
proton lamp at (9, 10, 10) heading +X, amount 6; a neutron lamp at
(11, 10, 10) heading -X, amount 6; the low light lamp at (10, 10, 4) heading
+Z, amount 2; the high light lamp at (10, 10, 19) heading -Z, amount 6.
Rules in order: `photofission` (the outputs rule with the guard, threshold 4),
then `strong` (binds `[proton, neutron]`, `ray_delay` 1).

| Tick | What is on the board |
| --- | --- |
| 1 | The proton and the neutron rays are at (10, 10, 10) (`steps` 1); the low light is at (10, 10, 5), the high light at (10, 10, 18) |
| 2 | `strong` has fired: the group `[proton, neutron]`, amounts [6, 6], `ray_delay` 1, ticking every interval |
| 6 | The low light (amount 2) arrives at the group's Node and waits its clock (`delay` 1) |
| 7 | Its wait is over; in the cycle that follows the guard reads 2 > 3 as 0: no interaction, the light crosses |
| 8 | The low light is at (10, 10, 11), still heading +Z with amount 2 and phase 0; the group is intact and ticks (phases [0, 0]) |
| 9 | The high light (amount 6) arrives at the group's Node and waits its clock |
| 10 | Its wait is over; in the cycle that follows the guard reads 6 > 3 as 1: `photofission` fires, the three inputs are replaced by three new event rays (`steps` 0, the event's Ports +Y, -Y, -Z with shares 6, 6, 6) |
| 11 | The proton is at (10, 11, 10) heading +Y, the neutron at (10, 9, 10) heading -Y, the high light at (10, 10, 9) heading -Z; there is no bound group |
| 12 to 16 | Each walks one Link per interval; at tick 16 the proton is at (10, 16, 10), the neutron at (10, 4, 10), the high light at (10, 10, 4) and the low light at (10, 10, 19) |

Momentum at the split, amount times heading: inputs (6, 0, 0) + (-6, 0, 0) +
(0, 0, -6) = (0, 0, -6); outputs (0, 6, 0) + (0, -6, 0) + (0, 0, -6) =
(0, 0, -6): exact, the photon's included. At every tick: totals proton 6,
neutron 6, light 8, momentum (0, 0, 0); the charge ledger proton +18; every
line of the audit balanced; `conserved_at_every_completed_tick` true.

## Limits: what the engine refuses, and the rule that is missing

**The literal absorption is refused.** The translation "inputs light a +
electron m, outputs electron rays only, content m + a" is the outputs rule
below in place of `excite` (its third output turns the light ray into an
electron ray of amount 3 on the light's heading, so energy and momentum are
exact):

```json
{"name": "absorb",
 "participants": [{"type": "electron"}, {"type": "electron"}, {"type": "light"}],
 "outputs": [
   {"field": "electron", "amount": {"of": 0}, "heading": "same", "input": 0, "delay": 1},
   {"field": "electron", "amount": {"of": 1}, "heading": "same", "input": 1, "delay": 1},
   {"field": "electron", "amount": {"of": 2}, "heading": "same", "input": 2, "delay": 1}],
 "invariants": [{"name": "energy", "expression": {"field": "amount"}},
                {"name": "momentum", "expression": {"op": "mul", "args": [{"field": "amount"}, {"field": "heading"}]}}]}
```

Two generic rules refuse it, and neither is a defect: with the catalog's
electron charge -3 the initialization stops with `ray meeting output 2 of
family electron (charge -3) would change the total charge: its amount comes
from inputs of another charge` (charge is per quantum, so content added to an
electron ray is charge added); with the electron's charge set to 0 the world
starts and the meeting at tick 8 stops it with `ray meeting absorb changes
the stock of a family` (a meeting with outputs keeps every family's stock
exact, [meetings with outputs](../../docs/SPATIAL_FIELDS.md#meetings-with-outputs-ray-meeting-conversion-v1)).
So in today's tables energy stored in a group is the sum of its rays' amounts
across families, and the excited electron is expressible as the bound
`[electron, electron, light]` group, which is what `absorption.json` shows.

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
interaction of the catalog will need the first.

**A random lifetime is not expressible.** The emission of
`absorption_emission.json` fires at a declared phase, so the excited state's
lifetime is one integer. Highlights 3.26 gives the decaying group its
half-life through the Detector draw at the group's tick (1 = the conversion
fires, 0 = the group ticks on); the engine's Detector mark draws on arrivals
through Ports only, so a resident group's tick draws nothing today. The
missing rule is that draw, the mark's setting applied once per `bound_tick`,
with the conversion as the outputs rule fired on 1; the catalog's
`weak_conversion` waits for the same rule.

**Not shown.** No released field is declared: the world's light carries no
`field_of`, although light is the electron's own field in the catalog since
2026-09-17 (Highlights 3.5; the family `electron_field` until that date), and
the `mass_field` of the catalog is absent; no event of these runs needs a
release, and the faint rays would fill the picture; the groups therefore
radiate nothing. All
matter rest rates are 1 at N = 8, a resolution choice for the picture, not a
mass. The one-interval pause of each photon at the group's Node is the
group's declared `ray_delay`, the only clock slowing in the engine.

## Run and render

The record of each run lives outside the tree (Highlights 5.5; the register
holds the fingerprint). With the project environment active:

```bash
PYTHONPATH=src python -c "from pathlib import Path; from event_universe.runner import run_initialization; run_initialization(Path('examples/nature/absorption.json'), Path('runs/absorption'))"
PYTHONPATH=src python tools/ray_viewer/record_sidecar.py runs/absorption
python tools/ray_viewer/extract.py runs/absorption --label absorption --out runs/absorption/runs.json
python tools/ray_viewer/render_gif.py runs/absorption/runs.json --output runs/absorption.gif --contact-sheet runs/absorption-contact.png
```

The same four lines with `absorption_emission` and with `photofission`
render the other two runs. The
[ray viewer](../../tools/ray_viewer/README.md) draws the light ray arriving,
the meeting marker at the group's Node, the `bound_tick` records as generic
markers at that Node and the fragments leaving; a GIF is a rendering of a
fingerprinted record, not evidence by itself.

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

## The screen: the field of an electron at rest on seven marks

`screen.json` is the model owner's request of 2026-09-17 to see the eye view
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
outside the record (`ticks` 240, exploratory, not fingerprinted here)
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
whose corner meetings reproduce them every interval. The two files are
written before the feature and registered as
[E5](../../docs/EXPERIMENTS.md#e5-the-ring-an-electron-at-rest-as-a-loop)
(planned); their tick-by-tick states were computed by hand and pinned in
[test expectations](../../docs/TEST_EXPECTATIONS.md#loop-binding) as the
future `tests/test_loop_binding.py`, and the engine of `main` was then run
once on them to check whether it already holds the ring: it does, line for
line ([loop binding](../../docs/LOOP_BINDING.md#10-what-todays-engine-does-with-the-ring)).

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
`conserved_at_every_completed_tick` true; `bound_groups` empty and no
`bound_tick`, since nothing is held. The check run of 2026-09-17 on `main`
at `c21e03e` (not the registered demonstration, which waits for the
feature): `initialization_sha256`
`7908d327bd9163414cf3c019aec9919c2a0cbdb79c086b6fd081e52b69f83fa8`,
`source_sha256`
`5abd76ae78b2274d52679fbdbaaf1832e4af33278ef9d36e34120038240dbff6`, every
line as pinned.

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
balanced, `conserved_at_every_completed_tick` true. Check run:
`initialization_sha256`
`deeae3635bb5924ff90f36e9996f4acd7c7b6e235a5c6315630c62a5e442e539`, the
same `source_sha256`. With the four L lamps at phase 2 instead (the senses
a quarter turn apart, d = 2, the `quadrature` case of the expectations) the
same Born table closes the ring with the Nodes, headings and amounts of
`ring.json`.

### Limits: what the worlds show and what is open

The ring holds under today's engine because a meeting with outputs is
already the ordinary event of Highlights 5.2 and needs no hold; what the
feature changes is the removal of the held form and its register (the list
in [loop binding](../../docs/LOOP_BINDING.md#9-the-interim-forms-and-what-feature-14-removes)),
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
outside the tree; the register entry E5 is planned and carries no
fingerprint until the feature lands.

## A5: Coulomb's law through the spreading field

`a5_coulomb/` holds the worlds of experiment
[A5](../../docs/EXPERIMENTS.md#a5-electron-electron-repulsion-through-released-fields)
of the register, run on 2026-09-17 on `main` with feature 12b
(`field-remainder-v1`): two charged rays on antiparallel lines along x at
impact parameter b = 4, 6, 8, 12 and 16, each releasing its field `light`,
which spreads by the catalog's table, and each turned by the other's field
through the catalog's `electron_field_turn` as a momentum table
([a free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v1)).
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
| An electron at speed c, momentum p along x | A ray of the family `electron_a` (or `electron_b`), rest rate 1 (`kerengonen.phase_advance` 1), charge -3 (thirds of e), amount 64, emitted once by a lamp at the board's edge along +X (or -X); its momentum is amount x heading, (64, 0, 0), the default of its momentum register | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1); [a free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v1); Highlights 3.28 |
| A positron | The same ray with `charge` 3 (`electron_b` in `ep_*.json`) | catalog, `positron` |
| The neutral control | The same rays with `charge` 0 (`neutral_a`, `neutral_b`) and no coupling declared; they still release their field, so the only difference from `ee_b4.json` is the charge and the coupling | A5, "a control with a neutral family of the same rate and content" |
| Impact parameter b | The two lines are y = 24 - b/2 and y = 24 + b/2 at z = 24; the rays start at x = 0 and x = 96 and pass each other at x = 48 at tick 48 (closest approach); the transfer is read 3b later, at tick 48 + 3b | A5, "Run" |
| The field of the charge | `light_a`, `field_of` `electron_a`, `release` [1, 4]: at every Node the electron departs it releases 16 quanta on each heading but its own line, carrying its phase and its `source_sign` (-1 for the electron, +1 for the positron), set by the engine from the releaser's charge; `light_b` the same for `electron_b`, the engine naming one light family per releaser | [Released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1); catalog, `light` |
| The field spreading in all directions | `spread` [6, 1, 1, 1, 1, 1] on both light families: every Node that light reaches releases it again on the six headings by the table, forward 6, backward 1, transverse 1 each over 11; the share below one quantum is the Node's remainder register per family, sign and Port and leaves whole when it reaches one | [Field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1), `field-remainder-v1`; Highlights 3.5, 3.17 |
| The Coulomb force, repulsion of like charges | The coupling `electron_field_turn_a` over `[electron_a, light_b]` with `"momentum_table": {"light_b": 1}` (and `_b` the mirror): every light ray of the other charge the electron meets pushes its register by +1 x amount x heading of the field ray, away from the source, and returns reversed as the recoil; no event is stamped and the amount, phase and bit are untouched | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v1); catalog, `electron_field_turn` |
| Attraction of opposite charges | The same coupling with sign -1 (`ep_*.json`): the push is toward the source. The sign is read from the field ray, never from its phase: the engine gives a `when` guard no view of `source_sign` (`RAY_PROPERTIES` holds amount, heading, phase, advance, delay, family, charge and detector), so the table names the light family that carries it, one family per releaser, and the sign of the table is the sign of the charge product written before the run | catalog, `electron_field_turn`, `opposite_charge`; [field spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1), "the sign of the source" |
| The momentum transfer dp(b) | The change of the ray's momentum register, read from the `ray_push` records (before and after per push), at the read-off tick; its y component is the transverse transfer along the impact axis | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v1); Highlights 3.14, 3.16 |
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
