# The engine

The one engine of Universe24 is the field-only engine of the law of the shadow
(`field-only-v1`, feature 20; [Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
the model owner's decisions of 2026-09-18 and 2026-09-19). This document is
its contract as implemented: the world file, the interval's steps, the wait,
the events, the books and the record. It was the last section of the old
engine's document `SPATIAL_FIELDS.md` until 2026-09-19, when that document was
deleted with the engine it described ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
names of the old candidates that appear below (the dense layer, the readings
R and points of the law of the bit) are the road to this law, recorded in
Highlights 5.4 and in git.

The code: `src/event_universe/shadow/` (`world.py` the world file and its
refusals, `layer.py` the arrays of one family and the walk, `mixing.py` the
Node's mixing kernels, `engine.py` the interval and the books, `run.py` the
artifacts of a run) on `src/event_universe/core/` (`integer.py`, `lattice.py`,
`phase.py`). The tests: `tests/test_field_only.py`, `tests/test_node_mixing.py`,
`tests/test_family_turns.py`, `tests/test_family_quantum.py`
([expectations](TEST_EXPECTATIONS.md)). The worlds: [examples/shadow/](../examples/shadow/README.md).

## The law of the shadow (`field-only-v1`)

Feature 20, the model owner's decision of 2026-09-18, the evening
([Highlights 5.4](HIGHLIGHTS.md#54-the-detector), "The law of the shadow:
only shadows and events"): "No real and shadow. There is only shadow. There
are events, which are a whole quantum. That is all. The shadow spreads like a
ray from the event." A new engine mode beside the old one
(`event_universe/shadow/`), selected by a world's `"law": "shadow"` key; the
old engine and its worlds are untouched, each refuses the other's worlds by
name (`parse_shadow_world` refuses every key of the old schema, the old
parser refuses `law`), and the runner (`run_initialization`,
`python -m event_universe`) dispatches on the key, refusing its old switches
(`--observer`, `--visualize`, `--dense-field`, `--standing-field`,
`--node-workers` above 1) for a world of this law. Derived first in
DERIVATIONS.md round 7 (sections 45 to 50), whose numbers the worlds and the
test take, and the Node rule of round 8 (branch `docs/derivations-8`,
sections 51 to 56) the interval follows.

**The board.** Open (a closed board is refused: the edge is infinity, what
leaves is booked as escaped). Per Node and family: the twelve lanes' shadow
slots, one per number (the content whose field a shadow is), an amount, a
phase, a heading, a momentum carried; the remainder registers of point 22
(per number and Port, in ninths); and, at a Node with content, the held
content (`Holder`: an amount per family, a momentum, a phase, a number, a
whole charge, a table). The layer of one family is the dense layer's arrays
(`ShadowLayer`, the axes x, y, z, number, Port, layer; perf-arrays-v1), and
the mixing, the parked releases and the departure layers are the dense
layer's kernels by import
(`dense_field.mix_arrivals`, `apportion_carried`, `release_parked`,
`merge_departures`, `place_departures`, moved to module level over a
`MixingArrays` protocol on 2026-09-18; the old engine's results are byte for
byte the same). The nearest phase step of a sum is computed exactly over a
bounded window of candidates (`layer.nearest_step`, `step_window`: the tables'
rounding to 1/256 bounds how far from the nearest step the greatest rounded
projection can lie).

**The interval** (`ShadowSimulation.step`, round 8's S2, in this order):
(1) every shadow in flight moves one Link, a paid family's phase turning by
its amount over K (a cell below K does not turn; a matter shadow does not
turn, round 8 section 52 (iv)), the escapes booked; (2) at every Node the
size of the coherent sum of each number's arrivals is formed
(`ShadowLayer.sizes`, the amplitude the mixing forms, in 32nds of one
quantum's, `arrival_amplitude`'s integers); a held content reads the sizes of
the other numbers at its Node, and the quanta of a paid family in flight
read the free families' sizes at the Node they cross, each owing one
interval per whole unit at the world's `wait_per_quantum` n / d, a remainder
carried (on the holder, or per Node and number, in 1 / (32 d)); a holder
that owes neither releases, turns its phase nor steps that interval;
arrivals that owe neither mix nor move (a frozen cell, later arrivals of the
number joining them as one amplitude per Port, the countdown theirs); (3) a
held content meets the whole quanta that arrive at its Node: its own
number's are home, sunk for their amount alone and pooled to leave again
with its release, pushing nothing (R13; round 8 sections 52 (i) and 54 (i):
the only reading that keeps a content constant, gives the flux of the
emission and Newton's first law); another number's are met by its table,
`read` (the default for a free family: the push taken and the units left to
mix on as at an empty Node; round 8 section 54 (ii): a sink reads the
gradient of the intensity, 1/r^3, the pass reads the flux, 1/r^2), `keep`
(the default for a paid family, the click: the push taken and the amount
joining the holder's content), `rerelease` (the push taken, the amount
pooled to leave again with the holder's release and number) or `pass` (no
push, the units mix on); (4) at every Node the shadows of one number mix
(node-mixing-v1), the remainders park and release, the departures go into
flight; (5) a held content releases: per free family it holds, content x
the world's `release` n / d per Port with a remainder per Port; the pooled
amount six-fold with a remainder; a lamp its declared rate on its headings,
spending its content; every release stamped with the holder's number and
current phase; nothing in an interval it owes or in the interval after a
step; (6) the holder's phase turns by its content over K with a remainder
(refused when a step would reach half the circle); each accumulator adds
its component of the momentum, held at the content while a step is not
allowed, and the first axis (x before y before z) whose accumulator has
reached the content steps the content one Link that way, the accumulator
giving back the content and the momentum untouched (round 8 section 53:
v = p / M, Newton's first law by bookkeeping), at most once per interval and
never in the interval after a step (T2, an event takes the interval: the
speed bound a half Link per interval on an axis, below the field's 1 / sqrt
3), `fixed` never; a step onto a held content merges the two into the
resident (amounts, momentum and charge added, the resident's number, phase
and table kept), a step off the board escapes with its content.

**The push** (point 16 as amended, charge per thing;
round 8 S3): a unit of a free family with heading h pushes by -M a h (the
gravity reading, toward the emitter, the holder's content M the
cross-section) and by +(q_A / M_A) q a h (the electric reading, the owner's
whole charge over its declared content times the holder's whole charge q,
kept exactly in units of 1 / D on the holder, `push_remainder`, D the least
common multiple of the charged contents' declared amounts, the whole units
into the momentum); a unit of a paid family pushes by +a h, its own
momentum. The holder's own number pushes nothing. A shadow carries no
momentum and there is no ledger of the field's momentum (S8): the momentum
lives on held content and changes only by the pushes, and the third law is
the symmetry of the two fields, exact at rest for a symmetric pair (round 8
section 55 (ii)).

**The books** (`ShadowSimulation.books`, the runner's `audit` per tick),
exact at every interval: per family the held line, initial + absorbed (the
clicks) = current + spent (the lamps) + escaped (contents off the board);
the shadows' line, initial (the declared `initial_shadows`) + released (the
fresh emission, the lamps, the pooled releases) = current (the arrivals, the
departures in flight, the parked ninths' whole quanta) + escaped + absorbed
(home, the clicks, the re-releases; what is pooled is on the absorbed line
until its release); the momentum line reports the held momentum, the sum of
the pushes; the charge, the sum over the holders. At the fixed point of a
content at rest, released - absorbed = escaped = the emission (round 7
section 49 (i)).

**The world.** `law` "shadow"; `model_id`; `shape`; `boundary` "open";
`ticks`; `K`; `N` (64 by default, a power of two from 2 through 4096);
`release` `[n, d]` per Port heading per interval per quantum of held content
of a free family; `wait_per_quantum` (1 by default; an integer or `[n, d]`;
0 for no wait); `families` (`name`, `kind` `free` or `paid`, `charge` of a
held content of a free family, `turns_in_flight` whether the family's quanta
turn their phase in flight by their amount over K on every Link, true by
default for a paid family and false for a free one, a declared width since
2026-09-19, `quantum` the units of the family that make one event at a
holder that absorbs them, 1 by default); `contents` (`position`, `family`, `amount`
with 2 x amount < K x N, `phase`, `charge`, `momentum`, `fixed`, `table`
family name to `read` | `keep` | `rerelease` | `pass` with `read` the
default for a free family and `keep` for a paid one, `lamp` `{rate: [n, d],
headings}` on a content of a paid family); `initial_shadows` (optional,
a declared profile booked as initial content; the default is an empty board
that the emission fills). Every content is numbered at parsing in declaration
order; the numbers whose quanta a family can carry are the contents that
hold it free, the lamps of it and the contents whose table re-releases it. Refused, naming the law: any old key, a closed board, a lamp
on a free family, a charge on a paid family, two contents at one Node, a
table naming an unknown family or rule, a content at or past K x N / 2, N
not a power of two, a repeated lamp heading. `event_universe.configuration_validation`
reports a world of the law as kind `shadow`.

**The quantum of a family (2026-09-19).** `families[i].quantum`, 1 by default:
at a holder whose table absorbs the family (`keep`, the click; `rerelease`),
the units of one number arriving in an interval are taken from flight, their
push entering the holder as before, and wait in the holder's register for
that number until a whole quantum is there; then one event of the whole: one
click counted (`events` per family in the content's state, `absorbed` the
units that made events) with the whole joining the holder's content, or the
whole pooled to leave again. Nothing changes in flight, and `read` and `pass`
are unchanged. The units waiting are on the shadows' absorbed line and on the
held line's `pending`, not yet on its absorbed; a content's state lists its
`pending` per family and number. With the default every unit is its own
event, byte for byte as before. The derivation's q_γ (round 8, S5 and S6: a
whole q_γ assembled at a holder by the remainder rule, per number, one
absorption per quantum) as a declared width; whether light's phase in flight
turns by its message q/K rather than by the cell's amount, as S5 reads, is
not decided (`tests/test_family_quantum.py`).

**The record.** `run.json` carries `law` "field-only-v1", the world's keys,
`numbers` (the contents' numbers, positions and families), the books per
completed tick (`audit`) with `conserved_at_every_completed_tick`, the
per-tick `held_content`, `shadow_content` and `momentum` lines, the
contents' final states (`contents`: position, held per family, content,
phase, charge, momentum and accumulators, intervals waited, phase steps,
steps, what each met per family by rule, the push taken) and the escapes;
`events.jsonl` one record per event (`home`, `read`, `click`, `rerelease`,
`step`, `merged`, `escaped`) with the tick, the Node, the holder, the
family, the number, the amount and the push; `state.json`, through
`snapshot_writer.write_snapshot` (its source a `SnapshotSource` since this
feature), the contents and every Node with content (arrivals, departures and
parked shares per number and heading, with their phases and the intervals a
cell waits). `tools/run_series.py` runs these worlds as any. The
readings the tests make are the engine's (`shell_readings`: the shell mean
of the count, the radial flow and the size; `cube_flux`: Gauss's flux through
a closed surface), read-only.

**What does not exist here**: no thing ray, no bit, no return, no momentum
on a shadow, no home other than the pooled re-release of the own number, no
chase, no trace, no per-quantum charge, no closed board, no prefilled field
by a fill (a profile only), no `wait_reads` or `shadow_wait` option (the
size is the reading), no draw. The
example worlds are `examples/shadow/` ([README](../examples/shadow/README.md));
the isolated test is `tests/test_field_only.py`
([expectations](TEST_EXPECTATIONS.md#the-law-of-the-shadow)).

**Choices where the text was open, flagged for the model owner** (the PR's
"Needs a decision"; the readings of round 8 sections 51 to 56 taken where
they decide): the free families are read at a holder and pass on, only a
table keeps or re-releases (section 54 (ii)); a held content's own quanta
are sunk for their amount and push nothing (sections 52 (i), 54 (i)); the
step is the accumulator's with T2 (section 53), the holder object moving to
the neighbour at the end of the interval and merging with what it finds;
`fixed` declares an apparatus held in place; a paid family's push is its
unit's own momentum, a lamp does not recoil (the momentum changes only by
the pushes, S8); the electric quotient reads the owner's declared content;
a re-emitting slit stamps its own number on the light, and two numbers
never interfere (point 24), so the two-slit worlds use openings in the wall
(measured both ways on 2026-09-18: re-emitting slits give two humps and no
fringes); the wait of light in flight is charged once, at its arrival, from
the free families' sizes at the Node, and quanta that join a waiting cell
wait its countdown; the phase circle N is the world's (round 7 section 47
(ii); this engine's remainder rule sheds about 1.5 % of the emission per
interval into standing content at N = 64 and at N = 256 alike, the parked
release at the register's combined phase being the source); the gravity
reading's multiplier epsilon_g of section 55 (x) is not declared (1).

### Funded emission and absorption

A field whose emitting type also carries a scalar field of the same name may
emit with `"source": false`: the emitted amount is paid from the record's own
stock, clipped to what it holds, and no external source is recorded. Ray fields
require schema 1 for this; octant fields accept it under both schemas. The
causal source envelope's extension to a delocalized wave was deleted on
2026-09-17 with the shared quantum resource. An optional
`"recoil_field"` names an owned signed vector that loses `amount x heading` for
every emitted ray. The reverse is the `absorb` coupling mode: a record of the
absorbing type takes a share of every ray resident at its Node on the cycle
after arrival (`amount x fraction / fraction_denominator`, or the whole ray),
adds it to its own field of the same name and, with `momentum_field`,
`share x heading` to that vector; the rest of the ray is forwarded. Absorption
happens before forwarding and before this cycle's emission joins the residents,
so a record never swallows its fresh rays. Absorbers act in slot order.

A funded emission may carry a `"dissolve": {"after_ticks": N, "over_ticks": K}`
schedule instead of an amount: the record emits nothing for its first `N`
cycles, then the stock it held when the rule first saw it, divided over `K`
cycles and never more than is left. The count and the initial stock are a
record row (`dissolve_clocks`), so the schedule follows the record wherever it
moves. A particle that pays itself out as rays this way is a matter wave in
flight; the matter-wave probe (`examples/matter-wave/`, deleted on 2026-09-17) lands one
on a screen as the fringe of its momentum.

Quanta are signed when the field is. A funded emission of a negative amount
credits the emitter with what it emits, and the ray's momentum `amount x heading`
points back at the emitter; a record that absorbs a share of such a ray pays it
from its own stock, never beyond what it holds, and gains momentum toward the
source. That is attraction with the ledger closed: the pulled body pays for its
pull, and a body with nothing left is not pulled.

```json
"emissions": [{"type": "lamp", "field": "quanta", "amount": 2048, "source": false,
               "recoil_field": "momentum"}],
"spatial_couplings": [{"name": "sail_absorbs", "type": "sail", "field": "quanta",
                       "mode": "absorb", "momentum_field": "momentum"}]
```

Together with the conservation audit, which measures
rays as quanta, this closes the ledger: energy is the amount, momentum is amount
times heading, and both move only between records and rays. Positive quanta
give radiation pressure; negative quanta give attraction paid by the absorber.
Schema 2 attenuation of such fields is not supported.

### Kerengonen: phased rays (`kerengonen-ray-field-v1`)

The candidate uses immutable cosine/sine tables prepared with the field definition,
before physical stepping. Each table has at most 4096 bounded entries; the two
host preparation caches retain at most 16 tables each. A bounded integer series
uses fixed-point scale 1,000,000,000, checked 64-bit intermediates and at most 32
terms. Physical events read the prepared tuples and never construct trigonometric
tables. Preparation and cache storage are host costs outside NodeState.

A ray field may add `"kerengonen": {"phase_steps": P, "phase_advance": k}`,
with `P` a power of two from 2 to 4096 (the phase width `phase_bits` is log2 `P`;
wave-ray families) and `0 <= k < P`,
the family's rest rate. Every ray carries a phase step in any case, since every
ray is a wave ray, starting at the emission rule's `kerengonen_phase` (default
0) and advancing by `k` on every link, masked to the width; the key adds the
rate and the coherence table below. Rays merge only when heading, lattice phase
and wave phase all agree. Nothing else about transport changes: a ray still follows one
integer line, keeps its amount, and is counted whole by the ledger and the
audit.

Phase acts where rays meet. The coherence of the rays resident at one Node is
`|sum a e^(i phi)|^2 / (sum |a|)^2`, computed in bounded integers from a fixed
cosine table over phase differences (scale 256), so equal phases give exactly
one and opposite phases of equal amounts exactly zero. It gates two things:
the value a reader samples at the Node (couplings and `spatial_values` see the
ray total times the coherence, toward zero), and the share an `absorb` coupling
takes of each ray. Quanta that cancel are not absorbed and not seen; they
continue along their lines and are absorbed or escape elsewhere. The total is
never changed by phase: the audit measures amounts, not coherence.

How an absorber takes a ray is a run-time choice, `"capture"`. The default
`"share"` takes the coherent share of each ray's amount, truncated toward
zero, and forwards the rest: a single quantum at a half-coherent Node is never
taken. The other choice, `"threshold"`, is the deterministic hidden-variable
rule: the whole ray is taken when its coherent share reaches one half and left
otherwise, so the outcome is fixed by the phases alone. A threshold capture of
a negative ray is left whole when the absorber cannot pay its complete amount;
only the share mode may take a smaller stock-limited amount. Neither capture
draws: an ordinary absorber has no ticket and no seed. The whole-or-nothing
`"lottery"` capture, its `capture_seed`, the absorb rule's `capture_salt` and
the record row `absorb_tickets` were deleted on 2026-09-17 (issue #164, bucket
B.5) under [Highlights](HIGHLIGHTS.md) 3.19: the only draw in the model is at
a Node whose Detector bit is set. The bounded ticket sequence
(`TICKET_MODULUS`, `next_ticket`, `ticket_draw`) stays in
`core/spatial_state.py` as the local draw the
Detector mark owns.

Two sources in phase therefore give a fringe in Manhattan path difference:
`k x (d_a - d_b)` steps. One source alone never interferes with itself, because
rays that meet at one Node on one tick have traveled the same number of links;
it does through a Huygens source. A record that absorbs on the field keeps, per
absorb rule, the phase step nearest the direction of the coherent sum of what
it took (`absorbed_phases`, a record row), and an emission with
`"kerengonen_phase": "carried"` starts its rays at that phase plus one advance,
the emitter's own tick. A slit that absorbs and re-emits its stock every cycle
therefore continues the wave that reached it, and two slits lit by one lamp are
two sources in the lamp's phase. A carried phase requires an absorb rule on the
same field for the emitting type.

A ray may also carry its own advance per link. An emission with
`"kerengonen_advance": {"amount": <expression>, "denominator": D}` evaluates the
expression over the emitter's own fields, divides by `D`, takes the result
modulo the phase steps, and stamps it on every ray it emits; rays merge only
with equal advance, and a Huygens re-emission carries the advance of the
largest share it absorbed with the phase. An advance from the emitter's
momentum, `|p| / D`, supplies a candidate de Broglie relation: a faster beam has a
shorter wavelength within the probe's configured range. The
de Broglie probe (`examples/de-broglie/`, deleted on 2026-09-17) measures the fringe spacing
it gives; this relation is configured, not derived. A ray without its own advance uses the
field's rate. Without the key the field is the plain `isotropic-ray-field-v1`,
a wave-ray family with rest rate 0 and no coherence table, which still admits
a `kerengonen_phase` below its declared width; a `kerengonen_advance` on an
emission requires the key. The runner records the identity
`kerengonen-ray-field-v1`. The double-slit probe (`examples/kerengonen-double-slit/`, deleted on 2026-09-18)
measures the fringe on a line of absorbers.

Self-exclusion carries `(amount, cursor, wave phase, advance)` for the actual
departure cycle and compares heading, lattice accumulators, wave phase and advance.
A distinguishable external phase or advance is not excluded, even if the emitter's
properties have changed since departure. A cycle without emission clears the
previous emission row to four zeros, so the fallback advance sentinel cannot keep
an exhausted source active. A foreign ray never merges with the own key, since
its event differs (ray state); the own ray
of the departure cycle is the only one excluded. Phased or attenuating
self-exclusion alongside response couplings is rejected: subtracting a raw own
amount from a coherent or decayed sample is not the corresponding local
subtraction; the supported combination is absorption. Coherence evaluation is
quadratic in the configured local phase count, bounded relative to world size.

Funded emission and absorption currently require an immediate carrier commit on
the independent fixed field clock. If the local carrier cost requires a delayed
plan, the Node rejects it before publishing that plan. This prevents a later
carrier commit from restoring stock changed by intervening field cycles. The
candidate does not yet arbitrate these two clocks for delayed shared ownership.

Declared component accounting associates ray momentum with the vector explicitly
named by `recoil_field` or absorption's `momentum_field`. All declarations for one
ray field must agree; that vector cannot also own spatial populations. Actual
resident rays, in-flight rays, external injection and completed escape contribute
`amount x heading` to that vector's read-only totals. No field name supplies a
binding, and this accounting never repairs state or replaces the separate local
energy/momentum audit.
momentum, `|p| / D`, is the de Broglie rule: a faster beam has a shorter
wavelength, and the de Broglie probe (`examples/de-broglie/`, deleted on 2026-09-17)
measures the fringe spacing it gives. A ray without its own advance uses the
field's.

The mirror of the record form, `kerengonen_mirror`, is retired with the
record-as-owner field program (the settled rule (v); the cleanup of
2026-09-18, part 2) and refused naming the rule; a mirror is an external body
with a table since `node-is-ports-v1`. Until then a mirror was the same rule
turned around: the absorbed row also kept the heading of the largest share,
and an emission with `"kerengonen_mirror": "x"` (or `"y"`, `"z"`) sent its whole amount back as
one ray along the mirror image of that heading across the named axis, at the
carried phase and advance when `"kerengonen_phase": "carried"` is set. A
diagonal mirror, `"xy"`, `"xz"` or `"yz"`, swaps the two named components
instead, so a ray along `+x` returns along `+y`. The heading sequence must
contain every mirror image, the emission must name a `recoil_field` (the
mirror takes the momentum it reverses), and the emitting type must absorb on
the field. A mirror whose absorb rule carries a `fraction` is partial: it
returns the fraction it takes and lets the rest pass. A lamp facing a mirror
then holds a standing wave: the reading along the line repeats every
`phase_steps / (2 x advance)` links, as the
mirror probe (`examples/kerengonen-mirror/`, deleted on 2026-09-17) measures.
Without the key the field is the plain `isotropic-ray-field-v1`; a
`kerengonen_advance` on an emission requires the key, and a carried phase
requires its coherence table. The runner records the
identity `kerengonen-ray-field-v1`. The double-slit probe of the record form
(`examples/kerengonen-double-slit/`, deleted on 2026-09-18 with the program)
measured the fringe on a line of absorbers.

### Euclidean pace (`"metric": "euclidean"`)

A ray field moves every ray one link per tick, so a wave front reaches the
same Manhattan distance in every heading and the fringe of two sources follows
Manhattan path difference. A ray field may instead set `"metric": "euclidean"`
(identity `euclidean-ray-pace-v1` in the run metadata, beside the field's
policy). Every heading then has a pace, the ratio of its Euclidean length to
its Manhattan length scaled by 4096 and computed by integer square root; the
slowest heading (the one nearest a body diagonal) hops every tick, and every
other ray adds that slowest pace to a per-ray `wait` on every tick and hops
only when the wait passes its own pace, carrying the remainder. A ray that
waits stays resident at its Node, counted by the ledger, sampled by readers
and open to absorption like any other, and its phase still advances by one
step for the tick. No ray ever moves faster than one link per tick; the
Euclidean metric only makes rays slower, so that every heading covers the same
Euclidean distance per tick and the front is round to within one link. Rays
merge only with equal wait. Two sources in phase then give a fringe in
Euclidean path difference, and the
Euclidean pace probe (`examples/euclidean-pace/`, deleted on 2026-09-17) measures both.

A ray field may also set `"pace": [n, d]` with `n <= d`: the fastest heading
then hops `n` links every `d` ticks, on either metric, by the same wait. A
pace is never faster than one link per tick; it exists so that a matter wave
can be slower than the signals that chase it.

A funded ray emission may also name `"heading": [x, y, z]`, one of the
field's headings: every ray it emits leaves on that heading instead of
sweeping the sequence, a directed emitter. It cannot be combined with a
mirror, which chooses its heading from what it absorbed.

## Preflight

`python -m event_universe.configuration_validation WORLD [--json]` checks a
world file without running it: the strict decoder (`json_documents`, no
duplicate keys, no non-finite numbers), then the world parser above, whose
refusals name the key at fault. The report's `summary` is the world's model,
law, shape, ticks, families and contents; an issue carries a code (`syntax`,
`validation`, `io`), the document and the message. The workspace
(`python -m event_universe.ui`, [WORKSPACE.md](WORKSPACE.md)) uses the same
check. A valid configuration, a run that completes and a physically accepted
hypothesis are three separate results (`tests/test_configuration_validation.py`).
