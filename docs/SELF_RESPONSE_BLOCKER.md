# Moving self-response investigation

Status: blocked; no physical correction is established by this investigation.
Reviewed source: `f25262e0ef0fa7212acab9e60448d6e151baff32`.
The ordinary isolated-motion acceptance tests remain unchanged and required.

Follow-up: the user's [matter-state transfer hypothesis](MATTER_STATE_TRANSFER_HYPOTHESIS.md)
has passed six exact local arithmetic checks. It establishes conditions for
state restoration without an extra impulse, while leaving the replacement
long-range interaction and the existing self-response failures unresolved.

## Contract and observed cause

The [current Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
sections 3.3.2 and 3.3.3 distinguish transported vector components from the face
used to cross a link. Section 3.5 requires balances for each declared conserved
quantity/component, including retained remainders. None supplies an attribution
rule for separating one emitter's contribution after integer redistribution.

The delivered-face candidate responds to its old local inbox. A moving emitter
can occupy the same cell as its previously emitted outward field. Its nonzero
arrival imbalance then changes its force remainder or momentum. Existing tests
require zero self-response and unchanged free motion at every tested tick,
alongside nonzero emitted fields and an external response.

In `core/streams.py`, `direction ^ 1` selects the receiving face. The eight
population components themselves retain their indices and signs. These are
scalar arrival totals with a separately defined attractive response, not an
accidental reversal of a transported vector. Reversing the response sign changes
the sign of a nonzero self-response; it does not make it zero.

## Rejected correction: a predictor following only the particle's route

Consider one emission with nine units per octant, first phase zero, then phase
one. A particle takes the two hops `+x, +y`. Its own field can also reach that
destination by `+y, +x`. Pure calls to the current stream law give:

| Contribution | Eight octant components |
| --- | --- |
| Along the particle route | `(1, 1, 0, 0, 0, 0, 0, 0)` |
| Along the other route | `(1, 1, 0, 0, 0, 0, 0, 0)` |
| Total from the same emission | `(2, 2, 0, 0, 0, 0, 0, 0)` |

A predictor carrying only the packet on the particle's successive links misses
half this contribution. This rejects that particular fixed eight-component
predictor. It does not prove that every bounded local representation is impossible.

## Rejected correction: subtract an independently propagated self copy

The generic octant definition emits whole three-way bundles and retains leftover
units locally. For one sector and no new source, one unit alone emits nothing;
two units alone also emit nothing. Their merged three units emit one unit on
each of the three allowed faces.

| Inventory | Outgoing six-face sector amounts | Retained sector amount |
| --- | --- | --- |
| One unit | `(0, 0, 0, 0, 0, 0)` | `1` |
| Two units | `(0, 0, 0, 0, 0, 0)` | `2` |
| Three units | `(1, 0, 1, 0, 1, 0)` | `0` |

All three cases conserve inventory. However, redistribution of a sum differs
from the sum of independent redistributions. Labeling one input as self and the
other as external does not define ownership of the merged outgoing units.
An independently propagated self copy therefore does not provide an exact
decomposition of this merged update without an additional attribution rule.

## Reproduction

Run from the reviewed repository root. These are pure law calls; no simulation
world is executed or physical state corrected by the diagnostic.

```sh
PYTHONPATH=src python - <<'PY'
from event_universe.fields.streaming import CausalOctantStream, ZERO_OCTANTS
from event_universe.fields.definitions import octant_definition
from event_universe.fields.encoding import encode_values, decode_values

rule = CausalOctantStream()
first = rule.emit(ZERO_OCTANTS, 1, 9, 0)
xy = rule.emit(first[0], 0, 9, 1)[2]
yx = rule.emit(first[2], 0, 9, 1)[0]
print(xy, yx, tuple(a + b for a, b in zip(xy, yx)))

definition = octant_definition(source_per_octant=0)
for amount in (1, 2, 3):
    state = encode_values((amount,) + (0,) * 15)
    packets, retained = definition.publish(state, 0, 0)
    print(amount, tuple(decode_values(p)[0] for p in packets),
          decode_values(retained)[8])
PY
```

## Next bounded decisions

These are investigation directions, not an exhaustive list or a demonstrated
contradiction in the project's requirements. No admissible implementation fix
was found in this bounded investigation. A different bounded local state or
timing design may still satisfy the existing requirements.

1. A decomposition approach needs an explicit rule for attributing merged units
   and residuals, plus a bounded local representation that also covers alternate
   propagation routes. Per-source histories, global estimators and arbitrary
   suppression of motion-axis fields remain prohibited. No such representation
   has been established here.
2. A changed local interaction or emission rule could avoid generating or
   responding to the problematic co-arrival state. It is a new model assumption,
   not a vector-encoding repair. Its exact local inputs and timing must be defined
   before implementation. It must retain external longitudinal response, free
   motion, conservative transport and the whole-tick causal bound.

Neither option authorizes relaxing the current zero-self acceptance tests.
The test and physics-rule owners must independently accept any future candidate.
The contention/sender-locality defect is a separate scheduling problem; fixing
it alone does not establish a self-response correction.
