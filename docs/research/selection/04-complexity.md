# Retained local preference now changes the transported carrier

This source-only native control advances the previous two specific failures:
PR #48 compared prepared score bits without routing their carrier, and PR #49
had no apparatus-to-carrier terms. Here three retained Boolean channels carry
two actual lanes and the origin of the locally preferred output. The same
immutable fixed-six tensor transports these lanes; retained memory changes
their later routes. No click or external observer selects an update.

The result is a **finite local sorting and causal-response mechanism**. It is
not yet the non-Boolean charged carrier of the corrected 45-channel geometry,
and it does not demonstrate growing complexity between physical bursts.

## Local structural feature and reversible preference

At a collision site let `(m,x,y)` be exact bits. The carrier feature is the
directed inversion `s=y(1-x)`: the lower-priority lane is occupied while the
preferred lane is empty. Compute `m'=m XOR s`, then swap the two lanes when
`m'=1`. This gives the following complete permutation:

| Input `(m,x,y)` | Output `(m',x',y')` |
| --- | --- |
| 000 | 000 |
| 001 | 110 |
| 010 | 010 |
| 011 | 011 |
| 100 | 100 |
| 101 | 001 |
| 110 | 101 |
| 111 | 111 |

When current `m=0`, the output is
`(y(1-x), x OR y, x AND y)`. The two unequal carrier inputs both become
`(x',y')=(1,0)`, while distinct `m'` values preserve their origin. No losing
branch or original order is erased. `x+y` is exactly conserved. The preferred
lane is part of the fixed local law; it is not a runtime global maximizer.

The Boolean polynomial form is explicitly cubic:

```text
m' = m + y - xy - 2my + 2mxy
x' = x + y - xy - mx - my + 2mxy
y' = xy + mx + my - 2mxy.
```

The inverse, evaluated on the collision output `(m,x,y)`, is also cubic:

```text
m_old = m + y - mx - my - xy + 2mxy
x_old = x - mx + my
y_old = y + mx - my.
```

These are exact only on the declared Boolean sector. The underlying integer
Rule3 tensor remains reversible outside it, but those values do not implement
a Boolean sorter and are rejected as structural evidence.

## One streamed lane makes the invariant sector local

Let `C` denote this collision, `S_x` transport only `x` one face, and `F=S_x C`.
Its inverse is `C^-1 S_x^-1`. In each inverse monomial, transported `x` comes
from one face neighbor and `m,y` come from the target. Forward monomials are
entirely local or at one incoming neighbor. No monomial touches two distinct
neighbors. The direction is static law data; all six directions are tested.

The shared compiler in `validation/selection/clocks.py` produces

```text
u = 3 [F(b) + F^-1(b)]
a = F^-1(b)                 # complete prepared initial history
```

For every retained remainder `0<=r<6`, unchanged Rule3 gives
`ell=F(b)+F^-1(b)`, `r'=r`, `a'=b`, `b'=F(b)`.
Thus `a'=F^-1(b')` holds inductively. Every `a,b` remains Boolean without
clipping/reset; the three remainders remain retained. Each tensor has three
channels, 22 monomials, degree at most three, and zero support violations.
This proof requires the prepared sector; simply setting both history slices
equal would not establish it.

The generic bridge, this gate, the Born audit and the quantum-permutation
audit share one table and tensor family. It is a research control through the
existing runtime, not a new installed runtime mode.
The three-channel pulse-pointer control is a different law, with its own
retained-state budget and finite memory/feedback claim.

## Preregistered finite tests and actual results

The mechanism and checks were declared in
[issue #45](https://github.com/Closer24/Universe24/issues/45#issuecomment-6810761836)
before the runs. Each of 36 configurations uses a 3- or 5-cube, one of all six
face directions, and seed 101, 509 or 2027. Each runs 24 complete updates with
all remainder classes represented. A matched identity-collision control
streams the same carrier but removes the memory-controlled routing.

| Gate | Result |
| --- | --- |
| First collision, ready current memory | All 36 remove every directed inversion at the declared output ports |
| Independent first-order table/transport versus Engine | All 1,728 transitions across 36 coupled and 36 disconnected runs agree |
| Bounds and occupancy | Every carrier/history bit stays Boolean; total `x+y` is constant |
| Complete inverse and rewind | All 72 runs pass |
| Matched retained-memory interventions | All 24 change later carrier components; disconnected controls remove every difference |
| Full-state causal support | Every retained `a,b,r` outside the computational cone agrees |
| Persistent structural growth at episodes | **0 pass, 30 fail, 6 blocked** |

The intervention is stronger than equal current amplitudes: both experiments
have the **same complete initial carrier `a,b,r`**. Prepare an `x` pulse one
face from the intervention and set `y_n=x_(n+e)`. The inverse collision then
sees equal lanes and gives the same carrier history for either value of local
`m`. Changing only memory produces two differing future carrier components
at each of four checked updates; deleting the memory interaction produces
zero. Origins include zero and the opposite periodic corner on both cubes.

One complete representative 24-step run is saved through `run_bundle`:

- Tensor: `e198bd03db97d7bf55396c6db07c4926d6a161783f399caaccd48ebbbc2858da`.
- Bundle: `5375b2fa1a5ed05fb47cfca07ea2b64f45a1fa0df745c4583054765181820845`.
- 898 canonical arithmetic records; complete saved replay passes.
- Maximum retained size is three bits throughout, including remainders.

Ten focused tests pass independently of the wider shared-clock audit.

## What did not grow, and why ready memory matters

The passive structural proxy counts distinct nonuniform axial triples of the
actual `(x,y)` carrier pattern that recur at at least two sites and persist at
the same sites across adjacent checkpoints. It contains neither memory bits,
elapsed time, an accumulated novelty counter nor numeric amplitude. An
episode is a strict interior local maximum of **all** memory-channel
arithmetic-event counts. Empty windows and all trials are kept. Four separated
episodes and strictly increasing current score are required.

Some native runs reach score eight, but none passes the complete growth gate.
The 30 failed runs have enough episodes; six lack four episodes. Fresh random
occupancies score zero in the control; a frozen random carrier scores
38 and the periodic event control fails growth. Thus this proxy still cannot
identify meaningful organization universally. It is not retuned after the
failure, and arithmetic episodes are not physical cosmological bursts.

Ready memory is a resource. A local gate already has the explicit cycle
`001 -> 110 -> 101 -> 001`; after using `m=0`, a later collision can undo the
sorting. Current memory is never reset. The report records available ready
sites and output-port inversions at **every** step, exposing this effect.
Finite Boolean boards necessarily recur. Bounded local preference and
retained-history response do not imply indefinite monotone complexity.

The original PR #43 growth failures remain unchanged and are not rerun here.
Mapping this native mechanism into the corrected physical tensor requires a
declared carrier encoding, complete same-metric source/stress accounting and
shared apparatus ownership. Merely writing `45+3=48` proves none of those.
Born probabilities and physical Bell outcomes are not derived.

## Separate physical-carrier response controls

The reciprocal source lane supplied four-step 47-field texture controls, with
opposite initial apparatus momentum at one site and otherwise matched carrier
data. This is a different, explicitly typed projective model. A supplementary
protocol was declared in
[issue #45](https://github.com/Closer24/Universe24/issues/45#issuecomment-6810892674)
before comparison. Every supplied complete state is replayed and rewound.

The original coarse `(sign dot,sign cross)` bins do not change. To report phase
response finer than one bin, the supplementary reader also divides the integer
`(dot,cross)` pair by its gcd, correcting both projective denominator signs.
This primitive direction is invariant under positive endpoint amplitude
scaling. It uses saved state, not click-only data. Its implementation rejects
zero current denominators, and tests include negative projective rescalings.
The bare charged-carrier link is a **fixed-gauge diagnostic**, not an invariant
under independent local gauge rotations; no gauge transporter is supplied by
this readout.

| Control | Raw carrier component differences | Exact normalized directed phase-link differences |
| --- | --- | --- |
| Reciprocal47 texture, updates0–2 | 0 | 0 |
| Reciprocal47 texture, updates3–4 | 2 | 12 |
| Matched47 disconnected interaction, all updates | 0 | 0 |

The connected tensor is
`53e16d2f6ec111b43c968d507be4f954decaf93d78a5ff73c6b6de7dabefe243`.
This demonstrates an amplitude-independent phase response in that finite
source fixture. It does not establish preference for a more complex pattern,
Einstein constraint acceptance or a physical clock.

The separate actual48 retained-pointer comparison is weaker: tensor
`f981af820395eb1d00d323f39f3607acc759b2159ccf35d06f6a661cf00b4959`
compares identical original47 complete fields with different old pointer
memory. Raw carrier position components differ at update4 (and the explicitly
exploratory fifth update), but **both coarse and exact normalized phase-link
differences remain zero**. This homogeneous fixture therefore shows a matter
amplitude response, not the phase-structure response seen in the47 texture.
Its initial `chi=Pi_chi=0` is a purely real carrier; changing its real amplitude
alone cannot change a normalized complex phase while the sign is maintained.
This is a limitation of this fixture, not a theorem excluding phase response
from every48-channel pointer preparation.
The raw pointer feedback also lacks reciprocal source/stress accounting. The
two outcomes must not be conflated with the native sorting mechanism or with
completed physical complexity selection.

A further **exploratory** test was declared before running in
[issue #45](https://github.com/Closer24/Universe24/issues/45#issuecomment-6810942417):
use the existing `connected-texture-+1` source preparation unchanged, append
the identical pointer law, and compare only old pointer memory through exactly
five updates. No seed, score or horizon was chosen after reading the result.
The tensor is the same `f981af8...` as the homogeneous negative. All original47
initial complete fields agree. At updates0–3 both raw positions and exact
phase directions agree. At updates4–5, two carrier position components and
**12 directed normalized phase links differ**, while coarse sign bins still
agree. All three48 variants pass independent scalar comparisons, complete
saved replay and rewind. The compared bundle IDs are
`5c2d16779e61de72cc3daf6c1382208e7b8c5fb40e4cdd087036a9b5fd2512ea`
and `681c1db751c9d78fa1599ee42f1a75759cbad58d8b6d72424cf32d7c81590b28`.

This supplies the narrower positive chain **retained pointer history → later
apparatus → actual carrier phase structure on the same48-channel tensor**.
It still establishes neither preference for a higher structural score,
complete reciprocal pointer stress nor physical measurement. The homogeneous
negative and the coarse-bin zeros are retained beside the positive texture.

Evidence is produced by `audit_physical_response(raw_source,out)` and
`audit_pointer_response(reference_run,history_run,out)` in the same module.
Both reports bind source/tensor identities and preserve every zero/failing
response. The48 reader verifies both complete saved runs first.
The combined audit reproduces the fixed five-step exploratory run by passing
the exact saved `connected-texture-+1/bundle` to `pointer.audit_appended` and
then passing its two saved history runs to `audit_pointer_response`.

## Research source and reproduction

Margolus's [Partitioning Cellular Automata](https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TM-317.pdf)
and [Universal Cellular Automata Based on the Collisions of Soft Spheres](https://arxiv.org/abs/0806.0127)
provide primary examples of reversible local collision/transport computation.
They motivate retaining all collision information and separating local
scattering from transport. The exact three-bit sorting table, single-stream
Rule3 embedding, preparation proof and evidence above are this investigation's
construction; the cited work does not establish its physical identification,
complexity growth or Born statistics.

```bash
python -m unittest universe24.tests.test_selection_complexity -v
python -m validation.selection.complexity --out runs/selection/complexity
```

Use a fresh output directory. `complexity.json` records the complete
preregistered protocol, all held-out runs, detached controls, causal
interventions, event windows, negative outcomes and source hash. The
representative bundle, full trace and clicks are in `representative-run/`.
All24 native memory-intervention records also retain their complete initial
and final states, tensor identities and the shared compiler's source hash for
independent replay.
