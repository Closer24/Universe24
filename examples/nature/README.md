# Two events of nature in the engine's language

Five world files that show, on the one generic engine and with the rules
that exist today, (A) a photon absorbed by an electron at rest, (B) a nucleus
split by a high-energy photon, with a low-energy photon that does not split it
as the control, (C) the photon of (A) held inside the group while its
clock runs and then emitted on a new heading, the group back in its ground
state, (D) the helium ion, a nucleus of charge +2 with one electron,
[below](#the-helium-ion-one-electron-at-a-nucleus-of-charge-2), and (E) the
field of an electron at rest on a screen of seven Detector marks, the eye
view's first picture,
[below](#the-screen-the-field-of-an-electron-at-rest-on-seven-marks). They are demonstrations under
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
with its hits. With the split table of feature 12 the released light reaches
every Node of the screen and the whole screen clicks; the world file does
not change for that, only the catalog's `spread` entry and the engine. The
record, made once: `source_sha256`
`5f89c465b235083ebb2e9284db1f172a094cefa8003b94ea38a04003a10d23cc`,
`initialization_sha256`
`35dde6ad84145b5042285baadbb27810b5d30527554646cc67f5a69eac941cff`; at
every tick electron 8 in the world and none escaped, light released 12 per
interval (276 by tick 24, 214 escaped at the open boundary, 62 in the
world), momentum (0, 0, 0), the charge ledger electron -24, every audit line
balanced, `conserved_at_every_completed_tick` true.

**Not shown.** The simpler form, one lamp holding 8 as resident content and
releasing from its stock ([released field](../../docs/SPATIAL_FIELDS.md#field-as-the-rays-information-released-field-v1),
"Resident content"), releases nothing on `main` today: `SpatialEngine.begin`
schedules a Node whose record holds stock of a source family, but
`SpatialNode.plan_cycle` returns before planning at a Node with no active
source, no field content and nothing received, and no test covers
`release_stock`. The bound group is used instead, the electron at rest of
this README's dictionary.

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
