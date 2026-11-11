# A local no-change sensor with causal messages

Baseline production code: main `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.
This is a new, standalone toy tensor. It changes neither production dynamics
nor the recurrent-burst acceptance protocol.

**Positive result:** a retained local alarm distinguishes an unchanged binary
payload from an alternating payload with identical total amplitude, and causes
messages to spread locally. A disconnected control preserves the alarm but
removes its messages. No update counter, observer callback, reset or global
state read drives the effect.

**Negative result:** this is a one-update equality sensor, not yet a detector
of stagnating structural complexity. Its period-two control has no continuing
structural novelty, but is always classified as changing. The message field
eventually grows numerically; that growth does not count as organization.

## Declared model and bounded input domain

Seven retained gears per node:

| Gears | Role |
| --- | --- |
| `source.c`, `source.d` | Complementary binary controls, c+d=1 |
| `source.x`, `source.y` | One-hot binary payload, x+y=1 |
| `source.marker` | Retained detector location, 0 or 1 |
| `sensor.alarm` | Actual reversible local response |
| `message.x` | Message field propagating along the x-axis |

Use the controlled-swap involution

```
R_c(x,y) = (x+c(y-x), y+c(x-y)),    c in {0,1}.
```

The controls and marker have u=6b and a=b. For the payload choose
`u_(x,y)=6 R_c(b_x,b_y)` and prepare `a_(x,y)=R_c(b_x,b_y)`.
Because `R_c^2=I`, fixed-six Rule3 gives `b_next=R_c(b)` and
`a_next=b=R_c(b_next)`. Boolean one-hot histories are therefore invariant
forward and backward. This proof is local at each node and permits different
controls at different nodes. It requires the stated complete history and
Boolean controls; it is not a claim about arbitrary integer preparations.

Define the polynomial

```
S = 1 - a_x - b_x + 2*a_x*b_x.
```

Its full truth table is `(a_x,b_x,S) = (0,0,1), (0,1,0), (1,0,0), (1,1,1)`.
Thus S is exactly the last-update no-change predicate on this domain.
In the chosen one-hot sector S=1 for a static payload and S=0 for an
alternating payload. S is constant along either prepared source orbit.

This is not an arbitrary-integer equality detector: `(2,2)` gives S=5 and
`(2,1)` gives S=2. More generally a finite polynomial cannot equal one at
`a=b=0` and zero for all pairs `(a,0)` with nonzero integer a: its restriction
to b=0 would have infinitely many roots and hence vanish identically. An
unbounded board needs a different mechanism or a proved finite coding domain.

The actual alarm input is

```
u_alarm = 3 * b_marker * S
```

with initial alarm a=b=0. Put s=b_marker*S, which is a fixed Boolean on this
prepared source family. Rule3 gives `b_alarm_next=s-a_alarm`. Its complete
history cycles

```
(a_alarm,b_alarm): (0,0) -> (0,s) -> (s,s) -> (s,0) -> (0,0).
```

Thus source, marker and alarm remain bounded for all time by this exact
invariant-sector argument. The alarm records and responds to the no-change
condition; it is not an accumulating novelty archive.

The downstream input is

```
u_message(n) = 3*[b_message(n-ex)+b_message(n+ex)] + 3*b_alarm(n).
```

Only the last term is removed in the disconnected control. All monomials have
degree at most three and support on the target and at most one face neighbor.
The old-a read is `source.x -> sensor.alarm`; there is no old-a dependency
cycle. The Engine's staged inverse recovers the complete state. All input
coefficients are multiples of three, so every legal remainder is retained;
all recorded clicks in these runs are C0. This construction establishes no
C2-selection mechanism, physical energy conservation or Born probabilities.

## Frozen experiment and controls

The command writes `protocol.json` before any candidate is evolved. Default:
L=5, 40 updates, 128-bit cap checked after each complete step. No fitting or
search follows the outcome. The CLI permits only L=3 or 5, 1–160 updates,
and a 128- or 256-bit cap; a resource stop preserves and rewinds the completed
state and limits comparisons to the shared completed horizon.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.complexity.local_stagnation --out runs/complexity-research/01-stagnation
```

All noncentral source nodes alternate continuously. Only the central marker
is enabled. Static versus alternating central preparations change the local
control and complete payload history, with `c+d=1` and `x+y=1` in every
current and previous source snapshot. Therefore the comparison has identical
source/control L1 amplitudes at every observation time. This does not assert
that L1 amplitude is physical energy.

| Preparation/control | Alarm | Message result | Maximum bits | Full rewind |
| --- | --- | --- | ---: | --- |
| Static central payload | Period-four response | Emits locally and spreads | 7 | Exact |
| Alternating central payload | Zero | No messages | 2 | Exact |
| Static, payload labels exchanged | Same response | Identical message trace | 7 | Exact |
| Alarm-to-message edge disconnected | Identical alarm | No messages | 2 | Exact |
| Marker disabled | Zero | No messages | 2 | Exact |

All five cases complete 40 updates without a resource stop. First nonzero
message is at the source at update 2, at its two face neighbors at update 3,
and at distance two at update 4. The complete-state difference between the
static and alternating interventions stays within the one-edge-per-update
cone from their single changed initial site. The test compares a, b and r,
not just the visible message support.

An additional 48 cases exhaust `(c,x,marker,r)` in `{0,1}^3 x {0,...,5}`
for 12 updates each on L=3. Every source/alarm invariant and full rewind passes.
Together with the local proof this validates the stated alphabet; finite
enumeration alone would not establish arbitrary-time invariance.

At update 40 the connected L=5 message wire has value 82 at each of its five
sites. This is a simple repeated-source accumulation, not a successful
complexity-growth result. The connected case records 5,182 C0 events and
zero C1/C2 events; changing input records 5,000 C0 events and no message.
Click counts alone consequently do not identify the desired organization.

The output includes each exact tensor, complete seed, full a/b/r trace,
initial/final state hashes, source hashes, per-step passive measurements,
resource-stop status and complete inverse checks.

## Smallest missing coupling

The alarm can now be attached, as a separately declared model change, to a
local transport/restoring rule and tested against its disconnected control.
This supplies the causal-actuation interface requested by the recurrent-burst
protocol. It does not yet supply that protocol's reference-board reassembly
or growing structure.

The input to the sensor must next represent retained **structural novelty**:
for example, a finite pattern-memory construction that recognizes an already
visited local configuration. It must recognize the period-two source as
stagnant after learning its cycle, preserve the overwritten/history information,
and remain an allowed fixed polynomial on a proved coding domain. The parity
memory prototype is relevant but repeated visits can erase parity, so it is
not by itself a novelty archive. Finally, changing that retained novelty must
change later reassembly at equal amplitude in matched controls. Until then
the supported claim is local no-change sensing and causal message emission.
