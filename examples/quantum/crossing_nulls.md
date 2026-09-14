# Crossing null notices: two nulls before either notice arrives

This experiment measures the one residual the opt-in
[null notice](../../docs/CAUSAL_QUANTUM_SOURCES.md#opt-in-causal-null-notices)
left open for a single excitation, and the local correction that removes it.
A null notice carries the deciding Node's factor `1 / (1 - p)`, with `p` its own
scaled weight. When two Nodes record nulls before either notice has crossed the
Link between them, the second factor is computed from a stale scale, and the
product delivered to the rest of the domain is not the conditional scale. The
correction rule lets the Node whose null is ordered later, by tick and then by
position, answer the earlier notice with the exact quotient it should have sent.
Every number below is a read-only audit of the runtime report; the analytic
targets are computed independently of the update code.

## Layout

[crossing_nulls.py](crossing_nulls.py) derives every input from the checked-in
[causal_charge.json](causal_charge.json): registers S, M and D at (1,1,1),
(2,1,1) and (3,1,1) with `"null_notices": true`. Two 3:4 mixers, on (S, M) and
then on (M, D), leave the weights `225/625`, `144/625` and `256/625` by tick 3.
The contact probe type moves; two probes start four Links above M and D and
reach them at tick 4, when both record a null with tickets that select it. A
second variant starts the D probe one or two ticks later.

The exact conditional scale at S after both nulls is
`1 / (1 - 144/625 - 256/625) = 25/9`, whichever null is taken first. M's
factor `625/481` is exact. D's factor sent at the same tick is `625/369`,
computed from the stale weight `256/625` instead of the conditional
`256/481`; the stale product is `390625/177489 = 2.2008`, and S would emit
`9/25 x 2.2008 = 0.79` of its full strength instead of one. The correction is
`(1 - w s_old) / (1 - w s_new)` with `w = 256/625`, `s_old = 1` and
`s_new = 625/481`: `19721/15625`, and `625/481 x 625/369 x 19721/15625 = 25/9`.

## Reproduce

```sh
PYTHONPATH=src python examples/quantum/crossing_nulls.py --output artifacts/crossing-nulls
```

`tests/test_null_notices.py` runs the same worlds in the fast gate and checks
the correction arithmetic, the ordering key on notice packets, the correction
bank and its bound.

## Observed results, 2026-09-14

Python 3.14.0rc2, runtime source fingerprint
`6c5eb5f5151944a865ec91d2b7ffb786d7c56a898a02446733dc6bd78a2c4fdf`.

| Variant | Tick 4 | Tick 5 | Tick 6 | Tick 7 onward | Corrections |
| --- | --- | --- | --- | --- | --- |
| Crossing: both nulls at tick 4 | M and D null; M sends 625/481, D sends 625/369 | D receives M's notice, corrects itself to 25/9 and queues 19721/15625; M holds the stale product 390625/177489; S holds 625/481 | the correction reaches M: 25/9; S holds the stale product | S at 25/9 | 1, at D |
| Sequential: D one tick later | M nulls, sends 625/481 | D receives it, then nulls with the scaled weight 256/481 and sends 481/225 | S at 25/9 | S at 25/9 | 0 |
| Sequential: D two ticks later | M nulls | S at 625/481 | D nulls exactly | S at 25/9 | 0 |

The quantum owner decides both nulls at tick 4 with the exact conditional
weights, `[481, 144]` at M and then `[225, 256]` at D; the envelope side is
what lags. With the correction every Node reaches the conditional scale 25/9
once every notice and the one correction have crossed their Links: S two ticks
after D's correction leaves. Spatial accounting is balanced at every tick.

## What this does and does not show

- It shows that, for one excitation, crossing nulls are corrected locally: the
  correcting Node uses only its own null record and the factor delivered to
  it, and the ordering by (tick, position) makes exactly one of two crossing
  Nodes correct. The conditional scale is reached by every Node after Link
  transit, with no global renormalization.
- It shows the price: the stale product is emitted by S for two ticks, which is
  the causal residual of this candidate, now bounded by Link transit rather
  than permanent.
- It does not extend the candidate to several excitations in one domain. That
  case is outside the candidate's configuration space, not a numerical gap: the
  envelope per Node is a one-excitation amplitude, and a domain holds one
  conserved carrier.
