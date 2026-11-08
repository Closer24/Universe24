# Internal clock trials and conditional registration

Base model: `ff89e2ff661c8b60af84aff738f9040ad7f15bcc`.
This note changes no engine, coupling, preparation, observer or acceptance rule.
Every claimed mechanism must be realized by a complete initial board state,
fixed coupling and ordinary synchronous Rule3 evolution.

## Exact obstruction: four quotient-free updates close the whole orbit

Let `S_t` be the complete board state, and let `ell_i(t)` be the Rule3 quotient
for channel/address `i` during the transition from `S_t` to `S_(t+1)`.
Suppose `ell_i(t)=0` for **every** channel and for `t=0,1,2,3`.
Then `S_4=S_0`, and determinism implies `S_(t+4)=S_t` for every later time.
Thus this board cannot discover a new event merely by running longer.

Proof: zero quotient gives `(a,b)->(b,-a)`. Each address therefore has the
four successive old `b` values `b_0,-a_0,-b_0,a_0`. Their sum is zero and
the counter pair returns after four transitions. Coupling is a fixed linear
sum of neighboring old `b` values, so `sum_(t=0..3) u_i(t)=0` at every address.
The exact remainder balance is

```text
r_i(t+1)-r_i(t) = 2*u_i(t)-6*ell_i(t).
```

Summing it over the four transitions returns every remainder as well. Hence
the full state, including all halos, is restored. Applying the same
deterministic map to equal states proves the all-time recurrence. No finite
experimental result is needed for this implication. The argument works for
every permitted fixed sign triple and every permitted board size.

The premise is **zero quotients everywhere**, not merely zero observed C.
The existing C guard suppresses an event when the complete local triple is
unchanged, even if its quotient is nonzero. For example, with +++ coupling,
the explicit complete field `a=b=k` at every channel has `u=6k`, `ell=2k`
and unchanged arbitrary valid remainders; it is stationary and has no C.
No-C and zero-quotient tests must therefore remain separate in an audit.

Consequently an autonomous search lasting beyond four updates needs ongoing
nonzero quotients somewhere. The proposed detector may remain quiet while
other board regions perform those transitions. A prepared isolated four-cycle
alone supplies no expanding set of trials.

## WRITE then PROBE: a conditional internal interface

The existing phase study gives a finite, prepared carrier that changes a
local clock's retained phase. The existing transmission study gives a finite
clock/guide preparation whose state controls exact outgoing transport.
Combining those two interfaces is a new claim, not an automatic consequence.

Prepare a writer packet, a later probe packet and the target apparatus once.
Keep the probe preparation and timing identical across writer-present and
writer-absent controls. Keep the target clock present in all four writer/probe
controls. Remove only designated source counters; retain all initial
remainders and the common tensor. A changed probe outcome can then depend on
the internal state produced by the first encounter, rather than merely on the
arrival of a separately scheduled release train.

In the original phase convention, a first packet with delay `d1` writes an
effective clock offset `p_eff=-d1 (mod 4)`. A later probe with delay `d2`
would therefore encounter offset `p_eff+d2=d2-d1 (mod 4)`.
The existing isolated transmission domains suggest the prospective predictions

```text
gap = d2-d1 = 2 mod 4: enabling state;
gap = d2-d1 = 0 mod 4: aligned suppression state.
```

These predictions require equality of the **complete** prepared clock/guide
interface, including all retained halo remainders. Equality of one clock
phase or a passive D/X readout is insufficient. They also require suitable
separation from the first encounter's outgoing information.

For a strong enabling comparison, choose initial offset `p=-d2`: probe-only
starts aligned, while the writer is predicted to put the apparatus in the
enabling state when `gap=2 mod 4`. For the converse comparison choose
`p=2-d2` with `gap=0 mod 4`. In both cases the writer itself encounters
initial offset two and may transmit, so a later output window must not count
that first packet as the probe.

Preregister a complete quiet interval before the probe: the full protected
region follows its lag-four orbit, and every individual external input term
is zero throughout that interval. Preserve writer-only and probe-only output
controls, all raw C classes, exact output-template matches, complete-state
inverses and actual input terms. A quiet interval alone does not prove that
residual waves cannot return later. Causal margins or a separately declared
offline state-mediation control are needed for the stronger causal claim.

This is a candidate internal conditional gate. Even a successful result would
not establish a preference for complexity, a single selected route, indefinite
waiting, autonomous trial generation or quantum measurement.

## Exact downstream event word for the existing positive carrier

Let `T` be the board time when the translating packet's origin reaches a
fixed primary-guide node. The existing cumulative profile `(1,1)` gives the
following local states without using an observed encounter outcome:

| Time | Primary-channel triple |
| --- | --- |
| `T-4` | `(0,0,0)` |
| `T-3` | `(0,-1,4)` |
| `T-2` | `(-1,0,4)` |
| `T-1` | `(0,1,4)` |
| `T` | `(1,0,4)` |
| `T+1` | `(0,0,0)` |
| `T+2` | `(0,0,0)` |

The quotient recovered by `ell=b_next+a_old` is -1 at `T-3`, +1 at
`T+1`, and zero on the other displayed transitions. The remainder change
therefore gives the unchanged arithmetic classification C2 at `T-3` and
C1 at `T+1`. There are no further primary-channel events through `T+4`
when the surrounding guide remains the pristine carrier environment.

In the proposed geometry the origin reaches the fixed downstream node at
`T=25+gap`, predicting C2 at `22+gap` and C1 at `26+gap`. Register this
before encounter simulations. Matching two event labels alone does not
certify a carrier: retain the full spatial template, its halo and these
temporal margins. Other channels and other board events remain observable.

## A minimal scalar coincidence condition

At a resting target `(a,b,r)=(0,0,2)`, two actual unit positive inputs at the
same update yield `u=2`, `ell=1`, and target `(0,1,0)`. The existing arithmetic
event is C2. Each input alone gives `u=1`, `ell=0`, target `(0,0,4)` and no C;
neither input gives the unchanged target. This is exact one-step Rule3
arithmetic and a candidate cooperative threshold.

It is not a runtime input-injection recipe. A full realization must prepare
the contributing channels and their halos before the run, check the entire
six-input sum, and audit subsequent feedback. A coincidence event alone is
neither an approval message nor selection of one among competing outputs.

## Repeated trials and a return loop

Several initially prepared probes can test repeated conditional responses.
They remain a finite supplied sequence. Calling their arrivals autonomous
trial generation would require an additional mechanism that produces or
recirculates the trial signals through Rule3.

A return-loop candidate must expose an actual outgoing carrier, a propagation
path back to an interaction site, and a new input there after a measured
latency. Periodic wrapping is an available board effect, but a wrapped carrier
also revisits guides and all prior disturbances. It is a separate experiment,
not proof that an isolated component composes. Compare different loop lengths,
phases, source masks and board sizes, retaining every returning disturbance.

For a pristine carrier whose **complete** state obeys `S_t=T_x^t S_0`,
periodicity gives `S_L=S_0` on a side-L board. This proves recurrence of
that carrier/environment, not recurrence of an attached apparatus. Combining
the phase-write formula with an undisturbed return after L updates gives
the conditional next-encounter phase `(-d)+(d+L)=L (mod 4)`. Thus `L=2 mod 4`
is a prospective enabling-loop family and `L=0 mod 4` a prospective suppressed
family. Both need full interface and incoming-template checks on each lap;
other disturbances can return on different paths and invalidate the premise.

For initial packet origin `c-16`, the first outlet window is states24..27,
with packet origins `c+8..c+11`. Pristine later laps add `n*L` to those
times. An upstream sample at states4..7 likewise repeats at `4..7+n*L`.
These are predictions for a preserved carrier, not post-hoc output windows.

The all-state dynamics is invertible. Distinct complete states cannot merge
into one absorbing winner or enter the same complete periodic orbit. Local
selection-like behavior remains possible only with the distinguishing
information retained elsewhere in the full state. A late retained local
record and an ongoing global exploration must therefore be specified and
tested separately.
