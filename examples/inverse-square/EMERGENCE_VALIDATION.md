# Derivation and falsification of radial dilution

This experiment uses unchanged `src/event_universe` from main base
`d66b43e`. It extends the [original probe](README.md) with exact path counts,
world-size and translation controls, source scaling, indivisible units, and an
intentionally biased transport control. This is a world/event audit, not a
local observer's image. No particle acceleration or force is configured.

## Prediction from the selected local rule

The existing conservative outward candidate distributes a constant source `S`
among eight octants. Each octant sends one third along each of its three
outward Links. Link travel takes one tick. These are selected microscopic
assumptions; locality and conservation alone do not uniquely choose them.

Every hop increases the unwrapped Manhattan radius
`R = abs(x) + abs(y) + abs(z)` by one. Before a boundary influences a measured
region, each reached shell therefore contains one emission interval's stock:

```
shell_stock(R) = S
shell_nodes(R) = 4 R^2 + 2
mean_stock_per_node(R) = S / (4 R^2 + 2)
```

Consequently `R^2 * mean / S` approaches `1/4`. This inverse-square asymptote
is a derived shell-count identity. Neither the physical configuration nor
the transport implementation reads a source distance or multiplies by `1/R^2`.
It is not yet a Euclidean pointwise law or a gravitational force.

For exact splitting, independently count all paths to one offset. Set
`a=abs(x), b=abs(y), c=abs(z)`, `R=a+b+c`, and let `z0` count zero coordinates:

```
stock(x,y,z) = S * 2^z0 / 8 * R! / (a! b! c!) / 3^R
```

The multinomial counts orderings of the local hops. The factor `2^z0` counts
octants sharing the coordinate planes. Integer path counting is an analysis
tool only; it does not update the simulation. With `S=8*3^9`, the prediction
is exact through radius nine. For smaller indivisible sources, rotating integer
allocation preserves the shell total but need not reproduce that point formula.

## Rejection criterion

A direction-independent scalar law at Euclidean radius five must give equal
values at `(5,0,0)` and `(3,4,0)`. The path prediction instead gives `324` and
`630`, a ratio of `35/18`. This is a counterexample to exact pointwise isotropy,
regardless of a fitted mean slope. Both points have the same geometric radius,
not merely the same number of lattice hops.

The eight configurations preserve both successful and unsuccessful physical
claims. Biased axis weights deliberately break local rotational symmetry;
their shell total should still pass. Straight-ray transport is an existing
alternative with explicitly supplied heading directions, not a consequence of
the equal octant split. Its finite-sweep readings are comparative evidence,
not proof of an isotropic continuum limit. Scalar resident stock and oriented
surface flux are different observables, especially for direction-dependent
lattice residence time.

## Reproduce

Use Python 3.14 with `PYTHONPATH` pointing to this checkout's `src`:

```sh
python examples/inverse-square/validate_emergence.py --output /new/evidence/path
```

The script preflights each initialization before constructing `Simulation`.
It records self-contained inputs, SHA-256 identities, actual integer inventory,
source/escape ledgers and causal-front checks at every completed step, plus
measurements and two saved field sequences. Completed-step count means the
number of `Simulation.step()` calls; the first completed step may hold stock
one Link from the source. Nothing beyond that causal radius may be populated.

The primary octant controls use eleven completed steps, radius nine and open
25-cubed or 31-cubed worlds. The shifted source is eleven or more Links from
each closest face. Ray controls use 512 or 2,048 headings, 32 emitted rays per
tick, heading scale 96, and a complete heading sweep after the measured shells
have filled. The source is declared external injection: the ledger proves
transported scalar-stock accounting, not closed physical energy conservation.

No simulator code, physical law, catalog or default is changed. This is a
configuration/API research harness, not a canonical runner export. Full event
graphs and local observer records are not enabled. A GIF reads the saved field
sequence; it must not change the physical states or interpolate their timing.

## Measured results on 2026-09-14

All eight configurations completed on Python 3.14.7. Across 226 completed
steps, injected stock equaled resident/in-flight plus escaped stock with zero
integer residual, and no measured stock preceded its causal front. All 72
measured shells contained exactly one source interval's stock. In the four
exact-split controls, all 1,158 measured Nodes per case matched the independent
multinomial prediction: 4,632 exact comparisons, zero mismatches. World-size
and translated-source maps matched point by point; doubling the source doubled
every measured value. The small indivisible source retained shell balance.

| Configuration | Stock at (5,0,0) | Stock at (3,4,0) | Ratio |
| --- | ---: | ---: | ---: |
| Equal octant split | 324 | 630 | 1.944444 |
| Larger world | 324 | 630 | 1.944444 |
| Translated source | 324 | 630 | 1.944444 |
| Double source | 648 | 1260 | 1.944444 |
| Axis weights 4:1:1 | 10372 | 314 | 0.030274 |
| 512 straight-ray headings, full sweep | 307.5625 | 615.0625 | 1.999797 |
| 2048 straight-ray headings, full sweep | 307.53125 | 691.984375 | 2.250127 |

The indivisible-source snapshot has zero stock at both selected points, so its
point ratio is undefined, not evidence for isotropy. More ray headings did not
make these two resident-stock readings equal. This narrow observation does not
test a properly defined oriented-flux continuum limit. No positive-only fitted
slope is used as the acceptance criterion.

Runtime source SHA-256, unchanged before and after the eight cases:
`f1899620d69425423e0d42868cbcae77b67a6d5835b93d8e5cd9e30952cc97bd`.
The first harness attempt used the wrong completed-step origin in its causal
assertion (`R >= steps`). It stopped at step one. Aligning the audit to actual
completed-step semantics (`R > steps`) fixed that measurement error; no engine
rule was changed. The reported eight runs are the subsequent complete run.

The saved-state GIF has eleven actual frames, 700 by 800 pixels, a fixed log
stock scale, a rotating camera and no automatic replay. Every frame decoded;
the first and last were inspected. Its camera motion is presentation only.

The affected `tools/check.py` gate passed 144 tests with two opt-in visualization
skips; Ruff lint and format passed. Windows checks used UTF-8 and a fresh explicit
pytest temporary directory after the default temporary directory rejected access.

## Interpretation of the results

The useful outcome is conditional: conservative outward transport plus shell
growth derives a mean radial dilution law. The same microscopic assumptions
also derive anisotropy. Larger worlds cannot remove an angular bias that is
already present in the local rule. A claim of gravity would additionally need
a justified observable, interaction, acceleration, energy/momentum closure and
an independently tested continuum regime.

The existing Skills already require independent expectations and separation
of host audits from physical inputs. No Skill change is needed for this study.
