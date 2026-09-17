# Two events of nature in the engine's language

Ten world files that show, on the one generic engine and with the rules
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
[below](#the-ring-an-electron-at-rest-as-a-loop), and (G) the helium ion
again, on the engine with the field spreading and the momentum turn, with
the axis-only control,
[below](#the-helium-ion-with-the-field-spreading-and-the-momentum-turn).
They are demonstrations under
[Highlights](../../docs/HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions)
5.5: research runs made once, recorded with their fingerprint in the
[experiments register](../../docs/EXPERIMENTS.md#e-demonstrations-of-events)
((E) in its section here), never repeated as tests. Nothing here is a law of nature; every number is a
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
| The electron, charge -1 e, mass m | One `electron` ray (rest rate 1, `charge` -3) of amount m = 256, its momentum register m along its line at the launch; one Link per interval, the one speed of the engine (Highlights 3.28: the register sets the direction and never the speed) | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v1) |
| Coulomb attraction | The rule `nucleus_turn` over `[electron, light_of_nucleus]` without outputs, `momentum_table` `{"light_of_nucleus": -1}`: at every Node the electron shares with field content its register moves by -1 x amount x heading of every field ray there (toward the source of each), the accumulators reset, and each field ray returns reversed as the recoil; the DDA then walks the register. It is the catalog's `electron_field_turn` in the momentum-table form with the sign of opposite charges, standing in for the open `opposite_charge` entry (A5): the field ray carries `source_sign` +1, which no guard reads today (a coupling's view is amount, heading, phase, rate, delay, family, charge and bit), so the sign is the table's declaration, as in E4 | [A free ray turns by momentum](../../docs/SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v1); Highlights 3.5, 3.14 |
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
| 43 | (13, 8, 7): six field rays, the recoil of the -Y push among them, walking +Y with the electron and pushing it back (0, -11, 0): +X 35 (the mean field 34), -X 4, +Y 11, -Y 8, +Z 8, -Z 8; the register (-118, 264, 0). The accumulators reset at every push, so the DDA steps along the register's dominant axis, +Y, and nothing else |
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
(i) The DDA's accumulators reset at every push (`pushed_ray`, "as at a change
of line"), so a ray pushed in every interval steps along its register's
dominant axis and nothing else: the gradual line of `ray-momentum-turn-v1`
needs Links without a push to show, and a field that reaches every Node
leaves none. The path is therefore axis runs with whole quarter turns where
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
equilibrium of the computation: nothing restores a radius. So the engine on
`main` today gives the helium ion no circulating electron at any m, R or A:
the electron passes straight (escape) or is turned onto an axis and falls
(the control, E4's cage), and the answer to the model owner's question is
the computed one, a closed orbit at every radius, none stable, and on the
lattice none at all while every interval carries a push.

**What is open.** The reset of the accumulators at a push is the point of
decision: a rule that kept them (the push changing the register alone) would
let the DDA walk a curved line under a push every interval, and the neutral
equilibrium would still make the circle unstable, a spiral in or out at the
rate of the first perturbation; a stable orbit would further need the speed
to depend on the register, which Highlights 3.28 excludes. Both are the model
owner's to decide; nothing is changed here. The recoil's `source_sign` 0 and
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
