# One joint law: no-change sensor, retained memory and scattering

Baseline: `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`. This new toy
composition was declared after the separate experiments in the
[integration assignment](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802247405).
It does not modify production dynamics or replace earlier evidence.

## Result

The bounded joint tensor realizes the narrow chain
**local source history → retained Boolean alarm → memory-dependent routing →
changed retained density**. Equal-amplitude static versus alternating source
preparations first change messages at update2 and density at update3, only
when the alarm is connected. The matched disconnected rotor is unaffected by
the source choice. Complete-state changes stay within the intervention cone.

This closes a small composition obligation that separate successful examples
could not close. It does **not** show structural-stagnation detection, sustained
complexity growth, an independent reference-board burst, Born sampling or a
physical cosmological bounce. All registered growth tests remain false.

## Law and proof of the prepared domain

The existing `local_stagnation.build(connected=False)` supplies seven gears.
Its old scalar message wire is retained, undriven and identically zero. Its
Boolean source and alarm are independent of the rotor. The existing
`reassembly_feedback.build(connected=True)` supplies24 rotor gears; its
memory routing remains enabled even in the **alarm-disconnected** control.
Thus the joint tensor has31 actual retained gears, not30 hidden behind a
pruned interface.

For one local collision let incoming bits be p,n, memory be m and the
retained alarm be s. Define

```
h = m XOR s = m+s-2*m*s
p' = p+h*(n-p)
n' = n+h*(p-n)
m' = m XOR p XOR n
   = m+p+n-2*p*n-2*m*p-2*m*n+4*m*p*n.
```

The inverse uses the complement of `m' XOR s` as its swap selector; parity
recovers the old m. All16 local Boolean cases are checked. Streaming remains
linear and translates opposite lanes by one face edge. The two-bank map is
`F_s(X,Y)=(C_s(Y),S(X))` with inverse
`F_s^-1(X,Y)=(S^-1(Y),C_s^-1(X))`.

The actual Rule3 inputs are

```
u_rotor = 3*(F_(b_alarm)(b_rotor) + F^-1_(a_alarm)(b_rotor)).
```

Prepare `a_rotor=F^-1_(a_alarm)(b_rotor)`. Since all inputs are multiples of
three, division by six leaves every remainder unchanged, and the two inverse
terms cancel to give `b_rotor_next=F_(b_alarm)(b_rotor)` exactly. At the next
step, `a_alarm_next=b_alarm` and `a_rotor_next=b_rotor`, so the prepared
relation is maintained. This proof does not require the alarm to be constant;
it requires both retained alarm values to stay Boolean.

The source's independent Boolean domain supplies that requirement. Reading
the retained alarm, rather than substituting its quadratic history predicate
into the rotor product, keeps degree at most three. New factors are on-site;
streaming has one-face support. The only old-a chain is
`source.x → sensor.alarm → rotor messages`, so staged inversion is acyclic.
The actual expanded tensors have183 monomials connected and135 disconnected,
degree3 and zero support violations. The Engine accepts their old-a DAG.

The sensor reviewer independently checked16 collision inverses and32
previous/current-alarm handoffs; incorrectly using the current alarm in both
terms failed8 of32 cases. See the
[algebra review](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802295636).

## Frozen execution protocol

Before execution, `protocol.json` freezes L=3/5 × static/alternating local
source × alarm connected/disconnected × one-site memory intervention on/off:
16 runs,80 updates each,128-bit full-step limit.

The marked sensor is at cube center. The rotor packet origin is one negative-x
edge from that node; the optional memory intervention is at the sensor. This
fixed geometry was chosen before running so a single incoming packet can
encounter the controlled swap, rather than observing only p=n at a symmetric
focus. The complete rotor history is recalculated using the previous-alarm
inverse. No state is edited after preparation.

All source preparations have exactly equal source and control L1 amplitudes
at each tick. Only the local static/alternating control changes. The source
history is bitwise identical between connected/disconnected runs and under
the separate rotor memory intervention. The source thus does not receive
implicit feedback from the rotor.

## Actual results

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python experiments/complexity/sensor_rotor.py --out runs/complexity-research/07-sensor-rotor
```

- All16×80 Engine updates preserve Boolean messages/memory, the retained
  density identity `R=p+n`, total message occupancy12 and every remainder.
- Every rotor step matches a separate array specification implemented with
  explicit Boolean conditional swaps/XOR, not the tensor polynomial evaluator.
- All16 complete seeds rewind exactly. Every transition also passes its
  one-step inverse check. All1280 updated complete states are retained.
- There are648 matched complete-state cone comparisons, including the seeds.
- Peak retained integer size is3 bits including remainders; messages and
  memory are bits, density is0/1/2. No resource stop occurs.
- The runs record153,786 C0 events and zero C1/C2. No C2-dependent assertion
  is used to manufacture success.

| Comparison | First message difference | First density difference |
| --- | ---: | ---: |
| Static vs alternating, connected, each L and memory setting | 2 | 3 |
| Static vs alternating, alarm disconnected | None | None |

The L=3 density never meets the registered dispersion/reassembly cycle
criterion. On L=5, eight toy-density reassembly episodes occur. Without the
memory intervention, both connected source preparations have the same episode
times `10,14,30,34,50,54,70,74`, despite different message/density fields.
With the memory intervention, the connected static case ends at74 while the
alternating case ends at75. Both disconnected cases end at75. Thus the alarm
changes this late concentration timing in the declared combined control, but
we do not claim a universal timing effect in every case.

Changing the retained memory alone changes messages at update2 in every
matched setting, while the source stays identical. The control called
disconnected removes only alarm influence; it deliberately retains the
underlying memory-dependent rotor. This prevents confusing the two distinct
causal links.

Full-state returns are reported, not filtered. Examples include L=3 static
connected with unperturbed memory returning at48, and several L=5 cases
returning every20 updates. All16 runs fail the progressive structural-proxy
test. A repeated complete state cannot represent continued strict increase
of a single-valued structural score.

## Remaining obligations

The density is a retained occupancy record of toy messages, not independent
48-channel reference matter. The source detector senses one-update equality
on its proved Boolean domain. A period-two source produces no ongoing new
structure yet always appears changing; that counterexample is not removed by
the successful coupling. There is no accumulated pattern archive deciding
when structural progress has stopped, nor feedback from the rotor into the
sensor's independent source sector.

The next interface must preserve the full inverse while allowing an actual
retained novelty/memory criterion to affect scattering. It should keep the
matched source-amplitude, alarm-disconnection, memory-intervention and
complete-state recurrence controls. It must also be evaluated against the
unchanged original reference-board, persistence and growth gates. Closing a
finite causal loop is a subgoal; it is not a derivation of Born probabilities
or an open-ended complexity principle.

## Evidence

Each case saves actual `tensor.json`, complete `seed.json`, `final.json`,
every `(a,b,r)` snapshot in `full_trace.jsonl.gz`, parameters and hashes.
The aggregate report includes all observations, failed growth gates, full
returns, source-history and memory comparisons, complete-state cone counts,
and hashes of the helper, both peer builders, the observer and the Engine.
The previous organization experiment is unchanged.
