# Two events of nature in the engine's language

Two world files that show, on the one generic engine and with the rules that
exist today, (A) a photon absorbed by an electron at rest and (B) a nucleus
split by a high-energy photon, with a low-energy photon that does not split it
as the control. They are demonstrations under
[Highlights](../../docs/HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions)
5.5: research runs made once, recorded with their fingerprint in the
[experiments register](../../docs/EXPERIMENTS.md#e-demonstrations-of-events),
never repeated as tests. Nothing here is a law of nature; every number is a
declaration written before the run.

The rays are selected from the [catalog of nature](../../docs/CATALOG.md)
(`light`, `electron`, `proton`, `neutron`, with the catalog's charge unit e/3
and the electron's rest rate 1); the two couplings that make the events are
the worlds' own declarations, since the catalog holds no photon-absorption and
no photofission coupling yet, and the rest rates of the proton and the
neutron, undecided in the catalog (A10, hypothesis 12), are set to 1 here for
the picture only.

## Dictionary: each physical word next to the engine word

| Physics | Engine (the key in the world file) | Where the rule is stated |
| --- | --- | --- |
| A photon of energy a | A ray of the family `light`, amount a (`emissions[].amount`), rest rate 0 (`kerengonen.phase_advance` 0), charge 0, one Link per interval; its phase is the emitter's clock at emission and never advances | [Wave-ray families](../../docs/SPATIAL_FIELDS.md#wave-ray-families-wave-ray-family-v1); Highlights 3.3 |
| An electron at rest | A bound group: two `electron` rays (rest rate 1, charge -3) held at one Node by the binding rule `bind`, a rule without outputs whose assignments set `delay` 1 on both; its content is the sum of their amounts (4 + 4 = 8), its clock is each phase advancing by the rest rate once per interval, and its mass as an output-clock delay is the rule's `ray_delay` 1 | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.4, 3.28 |
| The photon arrives | The light ray reaches the group's Node and waits the group's `ray_delay` (one interval) before it meets anything: the group's output clock, not a kinematic rule | [Mass as output-clock delay](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.28 |
| Absorption | The coupling declared for the families present when the light arrives: the rule `excite`, a binding rule over `[electron, electron, light]` declared before `bind`; it fires with zero events, so the light ray ends at the Node and stays in the group. The literal conversion of the light's amount into electron content is refused by two generic rules (see Limits) | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.4 ("Binding is the interaction whose result is zero events") |
| The excited electron | The bound group `[electron, electron, light]`: content 8 to 11 (the `bound_tick` record's `amounts`), the Node's output clock `ray_delay` 1 to 3 (a slower clock: every ray of matter that arrives now waits three intervals), the light's phase held at 0 while the electron phases keep advancing | [Binding](../../docs/SPATIAL_FIELDS.md#binding-and-gravity-by-delay-ray-binding-v1); Highlights 3.28 ("Speed is a clock slowing") |
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

**Not shown.** No released field is declared: the world's light carries no
`field_of`, although light is the electron's own field in the catalog since
2026-09-17 (Highlights 3.5; the family `electron_field` until that date), and
the `mass_field` of the catalog is absent; neither event needs a release, and
the faint rays would fill the picture; the groups therefore radiate nothing. All
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

The same four lines with `photofission` render the second run. The
[ray viewer](../../tools/ray_viewer/README.md) draws the light ray arriving,
the meeting marker at the group's Node, the `bound_tick` records as generic
markers at that Node and the fragments leaving; a GIF is a rendering of a
fingerprinted record, not evidence by itself.
