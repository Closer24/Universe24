# Six inputs, division with remainder and effective ratios

Status: exact current-model algebra and an unexecuted small-family proposal.
No runtime coefficient, core rule or coupling is changed.

The current scalar update has the exact Euclidean decomposition

```text
2*u+r = 6*ell+r_next,       0 <= r_next < 6,
a_next=b,                  b_next=ell-a.
```

The integer quotient ell and retained remainder jointly encode the division.
Every channel uses the same fixed formula with num=den=1. Its counters do
not choose new numerical coefficients during evolution. A rule allowing such
choices would be a separately specified candidate, not a discovered behavior
of the present engine.

The six spatial ports define the old input `u=sum_d w_d*b_d`. The divisor6
belongs to the scalar arithmetic. Six neighbors do not mean that a packet
budget is divided into six conserved equal pieces. Each recipient reads the
old donor counter with its fixed signed weight, while all updates use the same
previous snapshot. For example, an initial donor b3 on an otherwise quiet +++
board supplies u3 to each of six recipients; it is not read as six inputs of
one half. The recipient quotient, counters and remainder then evolve normally.
The complete algebraic balance, not an assumed conserved packet amplitude,
accounts for the update.

## Exact unit-source threshold family

For a target initially `(a,b,r)=(0,0,2)`, let k of its six actual input channels
have initial b1, with the others b0, under +++ coupling. Thus u=k at the first
transition. Every source counter is part of the initial board preparation;
there is no time-dependent injected u.

| k=u | ell | r_next | New target `(a,b,r)` | Guarded class |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | `(0,0,2)` | None |
| 1 | 0 | 4 | `(0,0,4)` | None |
| 2 | 1 | 0 | `(0,1,0)` | C2 |
| 3 | 1 | 2 | `(0,1,2)` | C0 |
| 4 | 1 | 4 | `(0,1,4)` | C1 |
| 5 | 2 | 0 | `(0,2,0)` | C2 |
| 6 | 2 | 2 | `(0,2,2)` | C0 |

The class cycles modulo three; it is not an ordering of source number,
cooperation or complexity. In particular C0 occurs for both three and six
unit inputs, whereas four inputs produce C1. C1/C2/C0 are passive labels of
already determined updates, not choice instructions. Larger input may change
the quotient while preserving the class. Signed input cancellation introduces
further distinctions between source count, actual u and event class.

A future registered family could use all64 source-presence masks around one
target on side9, with unchanged target/halo remainders, initial-only source
counters and the fixed +++ tensor. Retain the complete one-step states, all
world C events, the six individual target terms and exact inverses. Compare
all masks of equal k, and retain counterexamples outside the target instead
of recording only its predicted table. This is a proposed finite check of
parallel local input summation, not an executed experiment, a route selector
or evidence of evolving preference for complexity.

## Effective ratios need a behavioral family

State-dependent response can yield different measured ratios without changing
any coefficient. For the table above, ell/u is respectively zero, one half,
one third, one quarter, two fifths and one third for u1..6. These are outcomes
of a fixed quotient/remainder rule, not six chosen num/den values.

An effective rational frequency or transport ratio would require a declared
family of preparations, response windows and perturbations, a stable fit
across that family and an explicit error bound. One matched frequency or one
instantaneous ell/u ratio is insufficient. Retained remainder and prior
counter state must be included when testing whether a reduced effective law
actually predicts subsequent behavior.

There is also an exact constraint on the same channel's signed accumulated
input and quotient. Telescoping the retained-remainder identity over T updates
gives

```text
6*sum ell = 2*sum u + r_initial-r_final,
|sum ell - (sum u)/3| <= 2/3.
```

The bound uses fixed parity: the two endpoint remainders differ by at most4.
If `sum u` is nonzero, the accumulated ratio differs from one third by at
most `2/(3*|sum u|)`. Convergence requires unbounded absolute accumulated
signed input, not merely a long run: canceling inputs can keep `sum u` zero
or bounded. The ratio is undefined when that denominator is zero. Per-update
averages differ by at most `2/(3*T)`. Thus the current law cannot freely
choose a new long-run signed quotient/input gain for these same observables.
Counts of guarded C, ratios between component cycles and other coarse-grained
readouts are different quantities and need their own derivations.

Parallel board activity is one determined reversible trajectory. A claim that
it represents multiple competing alternatives requires explicit simultaneous
board patterns and fixed readouts; it does not follow merely from synchronous
updates or Euclidean division. No external complexity score may choose which
of those patterns continues.
