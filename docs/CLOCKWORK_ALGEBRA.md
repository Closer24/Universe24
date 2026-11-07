# Exact clock and gear readouts

The clocks and gears are a visual reading of the counter state. They do not
supply an extra physical mechanism, update stage, force, or external timekeeper.
Only the unchanged synchronous Rule3 engine advances a state. A replay control
changes which saved state is displayed, not the automaton trajectory.

## P1 — the exact gear identity

For one channel, let `u` be its signed sum of six neighbor counters from the
same old snapshot. The retained state and next state satisfy

```text
2*u + r = 6*ell + r_next,       0 <= r_next < 6
a_next = b,                    b_next = ell - a
```

A six-position wheel can therefore display the retained remainder `r`. Advancing
its unwrapped index by `2*u` produces the next remainder and signed carry `ell`.
The two other displays must retain the exact signed counter values `a,b`;
reducing a counter to a clock angle would lose information.

This is Euclidean division, including negative input. For example, `u=-1,r=0`
gives `ell=-1,r_next=4`, not a truncation-toward-zero quotient. A gear animation
must preserve this distinction. Carries are arithmetic, not physical energy.

**Proof of parity conservation.** Reduce the identity modulo two to obtain
`r_next mod 2 = r mod 2`. Write `r=2*theta+epsilon`, where `theta` is one of
`0,1,2` and `epsilon` is zero or one. Then exactly

```text
u + theta = 3*ell + theta_next
```

A three-tooth phase wheel with a separately displayed invariant parity is an
alternative lossless remainder display. The wheel alone is not the full state.
A signed input arrow, the quotient carry, the two exact counters and the
remainder are sufficient to make each scalar update inspectable.

## P2 — what a local clock means

If a channel's actual input sum is zero for an interval, its remainder is
constant, `ell=0`, and the counter pair undergoes

```text
(a,b) -> (b,-a) -> (-a,-b) -> (-b,a) -> (a,b).
```

This proves an exact period dividing four over that interval. For any nonzero
integer pair the period is exactly four: a two-step return would require
`(a,b)=(-a,-b)`, hence both counters zero. The zero pair is static.

For the signal-started unit-amplitude clock, the fixed four-phase readout is:

| Counter pair `(a,b)` | Displayed phase |
|---|---|
| `(0,1)` | 0 |
| `(1,0)` | 1 |
| `(0,-1)` | 2 |
| `(-1,0)` | 3 |

Other pairs must be shown as exact counters or explicitly marked outside this
particular four-phase alphabet. Phase must be inferred from the observed pair,
not assigned from the global step index. Four sampled phases are evidence about
a local projection; they do not assert that the whole board repeats.

The condition `u=0` refers to the **net signed input**. Individual incoming
counters can cancel. A clock face therefore cannot by itself establish absence
of neighboring activity, energy transfer, or interaction.

## P3 — source-absent quiescence

Any complete configuration with `a=b=0` at every address is exactly fixed under
Rule3, for **any** allowed remainder pattern and fixed coupling. Every input
sum is zero; because `0 <= r < 6`, `divmod(r,6)` is `(0,r)`. The next state is
therefore the same at every address. Induction gives stationarity for all steps.

This proves a useful component contract: apparatus prepared with zero counters
and information stored only in remainders cannot start on its own. A source
counter disturbance must reach it before its state can change. It does not show
that every nonzero preparation produces a useful signal or that the signal is
physical light. If a candidate apparatus includes initial nonzero counters, its
source-absent behavior needs its own control; P3 no longer applies.

## C1 — reproduced full-state clock certificates

[algebra_checks.py](../research/building_blocks/algebra_checks.py) starts one pair
at the cube center with channel 0 `(-1,-1,0)` and channel 14 `(1,1,4)`, on
background `(0,0,2)`. The adjacent-pair case adds an identical pair one site in
`+x`. These are initial preparations only.

The [retained result](../research/building_blocks/algebra_results.json) records
all complete initial/final checkpoints, full-state hashes at every sample,
observed channel triples, actual input sums and carries. Its engine files are
hashed against the unchanged baseline
`ed1556e202eb0f3cc60342c75d44012c2eeb71c3`.

| Preparation | Tested domain | First exact whole-state return |
|---|---|---|
| One preloaded pair | L=5,7,11; signs `+++` and `+-+`; 20 updates per case | 4 |
| Two adjacent preloaded pairs | Same domain | 5 |

Every forward transition has an exact full-state inverse, and every final state
rewinds all the way to its initial state. The adjacent pair's period change is
a finite interaction result. It does not establish a mechanical gear ratio,
physical binding, or an effective coefficient family. Full-state return under
a deterministic fixed update implies continuing recurrence for that exact
preparation, conditional on correct evaluation of the recorded cycle.

The one-pair example has only two explicitly nonbackground channels at some
phases and fourteen at others. The other channels retain remainder changes;
they cannot be deleted just because a clock drawing focuses on two channels.

## C2 — signal-triggered clock, not continuous pumping

A separately reproduced guide has N=24, L=151, positive signs and target j=6.
Its receiver channels 0/14 start `(0,0,4)` / `(0,0,0)`; its source pair starts
`(0,1,2)` / `(0,-1,2)`. Exact coordinates and all prepared receivers are in the
retained initial checkpoint. The same apparatus with the source omitted is
stationary in every sampled full state, agreeing with P3.

At the target's channel 0, the outgoing transition from t=5 has `u=1,ell=1`:

```text
(0,0,4) -> (0,1,0).
```

The target then follows the four-phase alphabet for t=6,...,43. For the
transitions t=6,...,42 its measured net input sum is zero. Thus the incoming
front **starts** a clock that continues by its own reversible counter evolution;
it is not continuously pumped by a nonzero input. The record predicate
`(r0,r14)=(0,4)` is a readout of the same retained state. A readout rising edge
is a passive record event, distinct from the engine's arithmetic event classes.
The 38-update first window does not establish permanent storage.

These two guide controls add 120 updates to the 240 clock-certificate updates:
14 cases and 360 forward updates total, with 360 one-step inverse checks and
360 rewind updates. All passed. The fixed CPU budget is 60 seconds; budget
exhaustion would be inconclusive. Results contain no random sampling and do not
claim a broad basin of spontaneous formation.

## Boundary of the light-driven interpretation

The universal statement “a clock can only run after receiving light” is not a
property of this model: the preloaded period-four configuration is a concrete
counterexample to a requirement for a separate incoming source. No physical
identification of its activity as light is established either.

The experimentally meaningful target is narrower: a specified source-free
apparatus remains quiescent, and adding only a specified initial source launches
a propagating influence that changes the apparatus readout after a finite delay.
The prepared guide satisfies this source dependence in the tested cases. To
make a stronger continuously driven device, preregister a readout that follows
or requires continued autonomous arrivals and compare runs with differing
initial source trains; do not remove a source or inject pulses during execution.

## Reproduction

From the repository root, choose a new output filename:

```bash
python -m research.building_blocks.algebra_checks --output runs/clockwork-algebra-new.json
```

Create `runs/` first if it does not exist. Existing results are never overwritten.
The exact script and core source hashes identify the tested computation; checkout
metadata records the execution context separately. No core files were changed.
