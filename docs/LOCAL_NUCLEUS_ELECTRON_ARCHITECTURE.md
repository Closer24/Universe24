# Local nucleus and electron candidate: component interfaces

Updated scope: the user subsequently required trapped rays under the same
generic coupling. The contact-gap builder described here is a comparison
fixture, not that target. Its movement and diagnostic interfaces remain reusable;
see [the corrected target](TRAPPED_RAY_NUCLEUS_RECONCILIATION.md).

## Authority and scope

This is the engineering contract for a named deterministic candidate containing
two separate neutron/proton property records bound at one physical Node and an
electron response outside that Node. Numerical laws belong to the separately
published physics profile. Both documents must identify the same profile before
implementation or execution. A configuration-defined law is a supplied candidate,
not evidence that real nuclear binding or an atomic orbit has emerged.

The independently implementable movement slice below is
`signed-displacement-drift-v1`. Publication of this document authorizes its
configuration builder and free-motion checks. Strong capture/release, field
coefficients and combined-world execution additionally require the published
`docs/PROTON_NEUTRON_ELECTRON_CANDIDATE.md` numerical profile; they are not chosen
by this movement contract.

The 2026-09-16 central specification snapshot, paragraphs P00004, P00013 and
P00325, supersedes the earlier 36-private-register architecture. Use bounded
NodeState and Scalar/Vector properties; no private-register count, new wiring or
register scheduler is required. The central document is
[the register-theory specification](https://docs.google.com/document/d/1jPBMb-1BoCH8Qo6y5E-j0H0ANWzbHmkO9l-9t2pxSOQ/edit).
The latest request fixes the nucleus to one Node, with two actual participant
owners; display offsets do not create two physical positions.

Source prerequisite: the nuclear acceptance and ray/output-Port corrections in
`c10af8ff92d4f9db2d8562bbffb2b2974188999b`. This candidate does not depend on the
unmerged Detector admission branch: no instrument, lottery, bond sampler or
random ticket is configured. Its deterministic scope does not claim an actual
external Detector implementation.

## Minimal existing components

| Need | Reused implementation | Admission limit |
| --- | --- | --- |
| Two local material participants | Property-selected atomic pair interactions in `fields/disturbances.py` | Two retained whole records; no output-type conversion, duplicate inventory or species-name engine branch |
| Binding and breakup | Simultaneous local assignments, explicit activation and independent invariants | Physics must supply a gap, capture/release operation and separated control; `hold` transport or a waiting timer is not the binding law |
| Momentum and fractional movement | Configured direction/rate expressions and adjacent whole-record transport | At most one adjacent Link per tick; preserve all existing fractional state |
| Source and field | Existing scalar signed ray transport and configured emission | Actual causal emission/receipt only; no distance formula, global source lookup or prefilled analytic potential |
| Electron response | Existing local spatial coupling primitives, with opposite configured field reaction | No automatic physical energy or angular-momentum closure; rays do not admit joint `spatial_interactions` or `field_rules` |
| Record/field inventory | Existing conserved component ledgers and configured invariant checks | A measured residual must never be fed back to repair state |
| Evidence | Existing runner, structured events/state and canonical HTML | Renderers and observers read saved state only |

The initial timing slice selects zero additional output wait on every face,
`W_d=0`, with fixed `H=1`. The ordinary ray/coupling profile may implement this
slice only while every prepared cycle has zero extra budget delay. Declare a
normal budget above a justified bounded worst-case cost and verify the observed
cycle costs/times. Any unexpected delayed cycle fails this timing acceptance.
Do not present this as support for nonzero computation-field delays: the newer
output-clock profile still rejects the required coupled ray/reaction owners.
The ordinary budget path also does not use an interaction's `k` as its duration;
no preparation or strong-binding timer may rely on that unsupported combination.

## Material and transport ownership

The nuclear operation retains the proton and neutron as separate whole records.
Their tags and complete properties survive capture and release. The binding
state, internal/reservoir values and any emitted energy belong to actual records
or ray/Link owners selected in the numerical profile. A bound flag alone is not
an energy reservoir. Both nucleons use ordinary movement; their retention must
follow the local binding operation, not a permanent `hold` transport setting.

The minimal center-of-mass fixture starts with both transport histories zero at
the same Node. If a moving bound control is selected, require exact integral
partition `p_i=m_i*P/(m_p+m_n)` and identical reduced velocity/routing histories,
then verify that both records use the same Port and reach the same next Node.
Zeroing unequal accumulated movement fractions is forbidden. General capture
with different preexisting transport histories remains outside this first
fixture until its remainder transfer is explicitly defined and tested.

For the electron, existing balanced routing resets quotas when the reduced
momentum weights change. Fixed-direction quota tests therefore do not establish
accuracy under repeated forces. A separately named integer displacement
candidate may instead keep a fixed owned three-component remainder `r`, compute
one signed unit-axis hop `d` from `r+p`, then retain `r'=r+p-D*d`, with fixed
positive scale `D` and at most one hop. The physics profile must select the exact
threshold/tie policy and admissible momentum range. It is not an implicit change
to cyclic or balanced routing.

This can be configuration-only: local spatial response precedes record updates,
which precede pair interactions and final routing. Updates evaluate sequentially,
but each property may be an update target only once. Use a single final remainder
assignment, optionally with separately declared bounded trial/selection fields.
The final `hop_direction` drives existing movement. The nuclear records must not
use a stale electron-style hop computed before their binding interaction.

For an admitted largest-remainder policy with `sum(abs(p))<=D`, initially zero
remainders can satisfy `sum(abs(r))<3D` and each `abs(r_i)<2D` after each update.
Verify these bounds and exact component identity `D*displacement+r=sum(p)` from
the declared initial state; this is a diagnostic identity, not a repair rule.
All comparisons and intermediates remain bounded integers. Fixed-axis ties must
be disclosed and tested for orientation bias, not described as exact isotropy.

The shared initialization has at most 16 fields, 32 configured rules and fixed
record/ray capacities. Expressions retain the 64-node/depth-16 limit. Share
`mass`, `charge` and the three-component `momentum` definitions; the numerical
profile owns exact remaining names, scales, bounds and conserved readouts.
Helper variables for routing are bounded nonextensive carried data, never new
copies of material or field inventory. A changing denominator requires an exact
remainder transformation; the first displacement candidate keeps it fixed.

## Frozen signed-displacement operation

The time unit is one model tick and `H=1`. A moving particle's momentum has the
declared candidate units; `D=mass*S` converts it into displacement numerator per
tick. `mass` and positive integer `S` are immutable during an admitted run, and
the builder freezes their positive integer product `D`. A physical change in
momentum does not reset any displacement remainder. Every active local step
requires `sum(abs(momentum))<=D`; failure rejects the proposal, never clips it.

Retain `motion_remainder` and `hop_direction` as nonextensive signed Vectors.
Add only two helper Vectors: `motion_trial` and `motion_choice`. Combined with
the numerical profile's 14 properties this reaches the existing 16-field limit;
do not raise it. All four are single-carrier local data, and each update target
occurs exactly once. Freeze the following update order:

1. `motion_trial = motion_remainder + active*momentum`.
2. For its components `(x,y,z)`, set
   `motion_choice = (abs(y)>abs(x), abs(z)>abs(x), abs(z)>abs(y))`.
   Comparisons are integer 0/1 values.
3. For `(a,b,c)=motion_choice`, define selected-axis mask
   `((1-a)*(1-b), a*(1-c), b*c)`. Multiply it componentwise by
   `(sign(x),sign(y),sign(z))` and the scalar condition
   `max(abs(x),abs(y),abs(z))>=D` to obtain `hop_direction`.
4. `motion_remainder = motion_trial - D*hop_direction`.
5. If preparation uses `age`, update it last, bounded by its declared cap.

Here `sign(v)=exact_div(v,max(1,abs(v)))` is exact for every integer, including
zero. Equality ties choose X before Y before Z, an explicit lattice discretization
choice. The longest hop expression fits the existing 64-node limit when `D` is
a frozen literal; the developer must verify the parsed tree rather than assume
that prose or a helper function bypasses validation.

Ordinary movement uses `direction_field: "hop_direction"`, rate one and
denominator one. A zero direction stays; a signed unit axis dispatches exactly
one whole record through that Port. Its adjacent arrival is dispatch tick plus
one. Do not apply the old speed gate again, multiply the momentum by an extra
tick, or insert a hidden input wait. Carry the already updated remainder with the
record on the Link. A departure in the cycle labeled `t` arrives when that step
closes at `t+1`; it is eligible for the ordinary local cycle labeled `t+1` at the
next step. There is no extra post-arrival wait and no additional drift callback
at departure or delivery. Thus an admitted, isolated, zero-wait electron has one
active drift update per world tick. Verify this from the trace rather than
assuming that preparation, an unexpected budget delay or another interaction
cannot skip an update. Report world-tick periods and active-cycle periods
separately; the numerical continuum comparison uses world ticks.

For an explicitly prepared electron, `active` is zero until the declared local
launch age and one afterward. Both the field response and drift read the same
old age, because age updates last. With seed age zero, threshold 64 and cap 65,
ticks 0 through 63 retain zero remainder/hop and consume no force response;
tick 64 applies its first local response and drift. This externally prepared
initial hold is excluded from bound-state evidence. It does not pin the nucleus.

Independent movement expectations, using a free particle with `active=1`:

| Input | Required dispatches and retained remainder |
| --- | --- |
| `D=10`, initial remainder zero, `p=(3,4,0)` for five updates | No hop, no hop, +Y, +X, +Y; final `r=(5,0,0)` and dispatched displacement `(1,2,0)` |
| `D=10`, momenta `(6,0,0)`, `(0,6,0)`, `(4,0,0)` | No hop, no hop, +X; final `r=(0,6,0)`, proving a changed momentum did not erase previous displacement |
| `D=10`, `r=(6,6,0)`, `p=(4,4,0)` | +X wins the equal-magnitude tie; final `r=(0,10,0)` |
| Previous tie result followed by `p=0` | The deferred +Y hop completes the already accumulated displacement; `r=0`. This is bounded discretization lag, not newly created momentum |
| `p=0`, `r=0` repeatedly | No drift and no hop |
| Negate all momenta and initial remainders | Negate every selected hop and remainder with the same timing |
| `sum(abs(p))>D` or overflowing intermediate | Reject before physical publication; no momentum clamp or lost remainder |

For each axis, compare `D*N+r` with the accumulated admitted momentum, including
the declared initial remainder. `N` counts dispatched hops; an in-flight hop is
a Link owner and must not be misreported as an already occupied receiving Node.
Verify arrivals separately. A free-motion world must retain the canonical HTML;
unit tests of local arithmetic are not a second simulator.

## Independent implementation owners

All files below are under `examples/local-nucleus-electron/`. The shared active
engine remains the only simulator; these builders supply validated initialization
data to it. No parallel engine or new plug-in registry is needed.

| Owner | Files and public boundary |
| --- | --- |
| Strong-interaction developer | `strong_configuration.py`: `build_strong_document(*, parameters: dict[str, int], shape: tuple[int, int, int], ticks: int) -> dict[str, object]`; produces a valid standalone neutron/proton initialization |
| Electron developer | `electron_configuration.py`: `add_electron(document: dict[str, object], *, parameters: dict[str, int]) -> dict[str, object]`; returns a deep-copy extension adding electron/EM definitions, preserving all strong rules and seeds |
| Strong/integration owner | `joint_configuration.py`, `measurements.py`, `run_experiments.py` and `render_gif.py`; composes builders, executes preregistered cases and reads the resulting evidence |
| Independent acceptance owner | `acceptance.py` and `tests/test_local_nucleus_electron_acceptance.py`; read-only scoring and independent synthetic fixtures; no competing writer |
| Physics reviewer | The numerical profile and independent expected values/controls; these are not copied implementations of either builder |

The electron builder rejects incompatible shared field definitions instead of
overwriting them. It may read the nucleus's published source/binding properties
through configured local expressions, but may not rewrite the binding law or
inject a force using the nuclear coordinates. The builders must agree on the
full field-count budget before adding helper state. Any needed core/schema change
returns to the architecture owner with a minimal failing fixture and precise
extension contract before two developers touch the same interface.

## Recorded evidence interface

Every measured world uses the canonical runner with visualization enabled. It
writes `initialization.json`, `events.jsonl`, `state.json`, `run.json` and
`run.html`. The following diagnostic extension adds a compact raw sidecar for
independent physics scoring without retaining a full field map every tick.
This supersedes the initial HTML-only extraction interface; it changes no
physical update, scheduler, law or existing default behavior.

- `Simulation.snapshot(*, include_spatial: bool = True)` returns the existing
  exact snapshot. False omits only the spatial map/packet expansion. It retains
  every carrier Node, held output, Link record, owned value and bookkeeping
  field, plus tick, boundary and escaped totals. Missing spatial detail means
  unavailable, never measured zero.
- `run_initialization` adds `frame_content="all" | "carriers"`, default `"all"`,
  and `state_trace=None | "all" | "carriers"`, default `None`. These select only
  recorded content. Reject invalid values before a run. Ordinary callers and
  the full final `state.json` remain unchanged.
- When enabled, `states.jsonl` streams a direct snapshot object at tick zero and
  after every completed step, independently of HTML `frame_stride`. Each line
  also has `accounting`, containing exact `totals`, `source_totals`,
  `dissipation_totals`, `escaped_totals` and `spatial_accounting` from the same
  world at that tick. Reuse already computed accounting where possible. Never
  rerun a world to manufacture a different trace format.
- `run.json` identifies the sidecar content, stride one, row count, source and
  initialization hashes. A failure preserves its complete recorded prefix and
  the separately labeled final failed state; it must not invent a successful
  completion or an unrecorded intermediate state.

For the long combined runs, select carrier-complete raw sidecars and carrier
HTML frames. Source-field validation reads actual field receipt events and
accounting; where a detailed field map is needed, its separately preregistered
run records that detail explicitly. The HTML's `script` element with
`id="recording"` and `type="application/json"` contains copied snapshot data in
`frames`, with `metadata` and optional `observation`. That exact unrounded JSON
may cross-check the raw sidecar where ticks overlap. Rendered images, glyph
coordinates, interpolated paths or downsampled display frames never determine
physical pass/fail. The GIF is a downstream view of already recorded evidence.

The integration owner's `measurements.py` exports
`load_run(run_dir: Path) -> dict[str, object]`, returning the keys
`initialization`, `metadata`, `events`, `frames` and `final_state`. They contain,
respectively, the decoded initialization, `run.json`, decoded event lines, raw
sidecar records and `state.json`. Independent acceptance may parse the same raw
sources itself and should stream long traces. A valid complete raw recording
has contiguous ticks and a final recorded projection equal to that projection
of the final state, excluding the added accounting wrapper. Any display sampling
is explicit metadata and does not relax raw trace completeness.

A frame's `nodes` expose `position` and `disturbances`, each with `type` and
`values`; values map field names to scalar/vector component lists. `transfers`
expose `origin`, `target`, `port`, `arrival_tick`, `type` and `values`. Preserve
these ownership distinctions. Two bound constituents share one exact Node
position; visual glyph offsets never become separate physical coordinates.
Use event dispatch ticks and actual arrival records to count Link displacement.
Do not count a transfer as simultaneous occupancy of both endpoints. Saved run
metadata retains the source and initialization hashes and the model identity;
derived acceptance and GIF metadata must cite those inputs.

## Required integrated evidence

- **Strong local dynamics:** show capture and persistent co-residence of both
  complete participants, a zero-coupling separated control, the declared
  below/above-threshold perturbations, reversible release where claimed, and
  exact declared local energy/funding/momentum accounting. Compare any imposed
  residence duration with a matching nonbinding delay control.
- **Causal field:** verify all six signed axes, `H=1`, no response before receipt,
  actual source/held/Link accounting and zero ordinary draws. State the field
  preparation/launch schedule explicitly; no pre-existing analytic field may
  be silently substituted for causal preparation.
- **Electron motion:** verify the vector-displacement arithmetic independently,
  a free control, reflected/rotated cases and a larger-domain common causal
  prefix. The measured radius is separation from the actual two-record nucleus,
  never distance from a hardcoded attractor used by the law.
- **Specific radius/frequency:** preregister the initial-condition perturbations,
  localization envelope, full-state or section recurrence criterion, observation
  horizon and boundary guard. Report no recurrence as unavailable frequency.
  Distinguish trajectory recurrence, internal phase and a measured spectral
  frequency; frame count/playback speed supplies none of them. One finite
  trajectory cannot establish a unique atomic radius or frequency.
- **Conservation scope:** nuclear gap/funding and configured total momentum may
  be exact while complete electromagnetic energy, angular momentum and source
  backreaction remain unclosed. Report those limitations; do not call an open
  causal-field experiment a closed atom.
- **Visualization:** each delivered world has canonical HTML. The requested GIF
  is generated from recorded Node/Link state with integer ticks and model identity.
  Proton and neutron appear as two glyphs inside one actual Node cube, with offsets
  labeled display-only. Show the electron's actual path, velocity and trail;
  no preset circle, fitted orbit or interpolation may disguise lattice hops.

A read-only renderer may use another installed runtime with image libraries; it
must not import a second simulator, evolve missing frames or modify the recorded
trace. Physical stepping uses the project Python 3.14 runtime and identified
source. A dimensionless pilot is not an atomic prediction; any later physical
comparison needs the separately declared scale and slow-motion control.
