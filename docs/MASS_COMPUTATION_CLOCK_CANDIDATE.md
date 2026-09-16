# Mass, computation rays and six output clocks: finite candidate

## Status and scope

Model identity: `mass-clock-ray-v1`. This is an explicitly proposed engineering
and physics-research profile, not an established mass-to-gravity law. Its integer
parameters below are selected fixtures; none is a measured universal constant.
The central project schema owns adopted model principles. This annex freezes a
minimal executable candidate and independent expectations before implementation.

Scope: stationary mass sources retained by an explicitly configured local
interaction/hold, nonemitting probe rays, and computation-field rays emitted by
those sources. A propagating computation ray is a field payload; it does not
itself emit a second self-field. No action in this candidate draws randomness.
Only an actual Detector may sample under the canonical Detector contract.

Preserve the existing free-emitter self-exclusion implementation and its tests.
The new delayed-output profile must reject moving emitters requiring
self-exclusion before initialization; it must not switch off exclusion silently.
Existing one-link subtraction depends on emitter/own-field co-arrival, which
independent output delays do not generally preserve. This first slice does not
claim to solve that unsupported composition or accelerated/returning self-fields.
It introduces no momentum kick or force. Source stationarity is explicit model
configuration, never a wait caused by insufficient capacity.

The [directional-response design](DIRECTIONAL_OUTPUT_RESPONSE.md) records why
this scalar timing profile does not test the intended directional bending
mechanism, the unselected numerical alternatives and the required bounded
moving-emitter self-exclusion contract. It does not change the frozen law below.

## Exact frozen candidate law

All values and intermediates are bounded integers. Inputs belong to the current
Node or were delivered by its six adjacent Links. Immutable family/profile data
select the operations and coefficients; the engine must not branch on proton,
neutron, mass-source or other physical species names.

| Quantity | Frozen candidate meaning |
| --- | --- |
| m | Nonnegative source mass-property integer; fixture values 1, 2, 3 |
| B | Finite source-owned computation-token reserve; distinct from mass and physical energy |
| T | Positive source emission interval in model ticks, independent of output holds; fixture 8 |
| t0 | First emission tick; fixture 0 |
| q | Requested emission amount m at each eligible t0+nT; zero mass emits nothing |
| g | Nonnegative integer clock coupling; fixtures 0, 1, 2 |
| H | Fixed adjacent-Link transit, fixture 1; never changed by computation field |
| C(t) | Sum of computation units actually received at this Node during tick t, plus newly emitted here during t |
| W | Additional output wait g*C(t), frozen when a specific Port's output batch is prepared |

A source with B >= m and m > 0 emits q=m and debits B by m atomically.
B=0 emits nothing. If 0<B<m, retain the unused reserve exactly and emit no
partial pulse; report it as unspent, not lost. No clamp, rounding, fractional
loss, mass consumption or hidden external source is permitted. The emission
Port comes from explicit immutable directional data; the minimal fixture is +X.
A configured source hold does not stop its independent emission timer. Because
mass stays unchanged during that hold, reading it does not alter a frozen
material proposal. Budget debit belongs to the separate actual source reserve.

C(t) is a transient local response sample, not another owner of the emitted
stock. It resets to zero next tick unless another actual receipt/emission occurs.
Packets whose output is held are not counted again on later ticks. Overlapping
arrivals add exactly; the same delivered/emitted unit contributes once to that
tick's sample. The source Node uses the same sampling and clock operator as
other Nodes, including its own fresh local emission. This is the selected
stationary-source clock response; it does not generalize to moving-emitter
self-exclusion or treat a ray's own content as a separately emitted self-field.

Tick order is deterministic:

1. Admit every due adjacent-Link input with ownership at its scheduled arrival.
2. Prepare eligible source emissions and exact source debits.
3. Form C(t) from this tick's actual input and fresh local emission.
4. Prepare batches for idle output Ports using W=g*C(t).
5. Publish due held batches and zero-wait new batches; each enters a Link with
   arrival tick equal to actual departure tick + H.

Each of six Ports has its own bounded pending batch and due time. Input delivery
has no clock delay, and another Port's hold cannot block sampling or an idle
Port's preparation. A batch prepared at t departs at t+W. Later input affects
new batches only; it cannot retime an already held batch or an in-flight Link.
The receiving Node can prepare its next output in the same arrival tick, but
H>=1 prevents same-tick multi-Link traversal. Computation-field payloads follow
the same selected output timing and propagate only through adjacent Links.

This minimal profile admits at most one unresolved batch per Port. Fixtures
space same-Port emissions so that no new batch targets a busy Port. A proposed
unsupported overlapping batch must produce an explicit pre-commit failure,
not capacity waiting, silent loss or an invented displacement law. This is a
finite candidate admission limit, not a replacement for the canonical moving-
event push/overlap design. The source debit and output publication must fail
atomically together. Extend that composition only under its own closed contract.

Proposed engineering bounds: m<=8, g<=4, 0<=C<=64, 0<=B<=128, W<=256,
1<=T<=256; all are manifest parameters with fixed upper bounds for the run.
Validate tick-plus-wait-plus-H and every sum/product against the project's
bounded integer limit. Overflow fails before any affected mutation. Capacity is
fixed per Node and six Ports; no per-source history, recursive push or global
physical lookup is introduced. Host audit storage is separate.

## Ownership and physical conservation scope

The exact computational-token ledger is source reserves plus actual held,
resident and in-flight field tokens, plus explicitly escaped tokens for open
boundaries. C(t), pending preview copies and diagnostic snapshots are excluded.
No decaying or absorbed-token channel is part of these fixtures. Field packets
carry their own actual stock exactly once when ownership changes.

This ledger is not automatically energy, momentum or mass. Physical E/P
readouts remain explicit family data and must not be supplied by invented engine
formulas. Source mass and existing carried E/P properties do not change under
this clock-only operator. The candidate does not claim a physically complete
energy-momentum budget for the computation field, a dispersion relation, recoil
or nuclear binding. If a family assigns nonzero E/P to the emitted field, it must
provide and pass the matching source debit/recoil operator before admission;
this annex does not authorize an unfunded physical emission.

## Independent fixtures fixed before the runs

Use at least three consecutive Nodes on an open +X line, far enough from the
boundary for the cited events. Sources are retained explicitly, and probe
payloads do not emit fields. Expected times below follow the declared integer
law, not implementation-generated expectations.

| ID | Input | Independent required outcome |
| --- | --- | --- |
| M1 | m=1, g=1, B=1, source pulse at t=0, H=1 | Source C(0)=1; departure 1; next Node arrival 2, departure 3; second Node arrival 4 |
| M2 | Change only m=2 and B=2 | Source wait 2; successive arrivals 3 and 6 |
| M3 | m=3, g=1, B=3 | Successive arrivals 4 and 8; unchanged ray amount 3 |
| Z1 | m=2, g=0, B=2 | Same emitted token total 2; departures 0,1 and arrivals 1,2 |
| Z2 | m=0, B arbitrary, no other field | No computation emission or field-induced delay; unspent B retained |
| G2 | m=1, g=2, B=1 | Same tokens as M1; arrivals 3,6 |
| C1 | M1 and a nonemitting probe ready at receiving Node exactly t=2 | Input admitted at 2; new probe output due 3, adjacent reception 4; no earlier remote response |
| C2 | M1, probe output prepared at receiving Node t=1 with C(1)=0 | Departure 1 and Link arrival 2 stay unchanged by later field arrival 2 |
| P6 | A local pulse sample C(0)=2; one nonemitting batch ready on each of six Ports at t=0 | Six independent due times 2, six adjacent receptions 3, no serialized sixfold delay |
| P2 | At one Node C(0)=2, +Y batch prepared 0; no new field at t=1, -Y batch prepared 1 | +Y departs 2; -Y departs 1 and arrives 2 despite +Y hold; no input-side delay or global Node lock |
| L1 | Source explicit hold through tick20, m=1, g=1, B=3, T=8, t0=0 | Emit at0,8,16 while source held; source field departures1,9,17; B becomes2,1,0; no fourth pulse |
| A1 | First field pulse held then injected failure before source-debit/output commit | Original B and all packet owners unchanged; no partial emission |
| X1 | Newly delayed moving-emitter/self-exclusion composition | Reject initialization, preserving old supported exclusion configurations and regression expectations |

P6 must seed a declared actual local field receipt/emission, not inject a global
sample into the physical engine. Keep field stock distinct from six probe
payloads. If one Port's batch contains the field and a probe, use the declared
fixed batch capacity; do not duplicate that field into all six outputs.

Add integer-limit, invalid-H and same-Port overlap rejection controls. Audit
ownership and RNG draws on every fixture. Required random-draw count is zero.
Every actual run must save the existing HTML visualization and structured event
trace. Arrival times, not animation speed, decide acceptance.

## Comparison with established physics

This first experiment tests a specified monotonic mass -> field -> output-delay
mechanism. It does not yet map an output cycle to proper time, tokens to potential,
a Link to metres or a tick to seconds. It cannot claim quantitative agreement
with gravitational redshift, lensing, Shapiro delay or nuclear binding.

A future independently calibrated clock comparison can test rate ratios versus
potential difference. Existing atomic-clock measurements show a real height-
dependent clock-rate shift; see [NIST/JILA's experiment](https://www.nist.gov/news-events/news/2022/02/jila-atomic-clocks-measure-einsteins-general-relativity-millimeter-scale).
The candidate must establish its calibration and predicted rate ratio before
comparing with those measurements. Merely choosing positive g and observing a
slower configured output is agreement with the supplied rule, not empirical
validation. Its directional pulsed field and frozen per-output waits may fail
continuum/relativistic tests; retain such failures rather than fit them away.

## Final acceptance boundary

Pass means the exact fixtures, ownership, bounded work, fixed Link timing,
Detector-only randomness and untouched supported self-exclusion regressions
hold for the tested implementation revision. Report unsupported moving emitters,
clock calibration and physical E/P completion separately. No passing fixture
closes strong/weak interactions, general moving-event push/crossing, or a universal
mass/computation law.
