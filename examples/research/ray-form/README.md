# Ray form: what is a ray, and can two rays bind?

Exploration evidence of 2026-09-16 at commit `e5b5911`, source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`
(Python 3.14.0rc2, headless). Read-only audit; no engine change. The question
is the first check of
[hypothesis 8](../../../docs/HYPOTHESES.md#8-everything-that-moves-is-a-ray-records-only-hold):
which forms of the engine are rays, and can a pair of counter-heading rays
stay bound at a Node so that its phase is a clock.

## Inventory of forms (owner audit, read from the source)

| form | ray-form? | why |
| --- | --- | --- |
| carrier (disturbance) records | no | hold, move, read and emit; a moving record waits under load and stalls the Node's clock |
| local fields (`transport: local`) | no | Node-resident stock |
| localized residue, claims | no | stock and bookkeeping left at Nodes |
| source envelopes, the quantum owner | no | retained complex sources and the deferred joint-state backend |
| `BondRegistry` | no | the declared registry, not a spatial object |
| outward fields (`transport: outward`) | yes | integer units crossing one link per interval along Ports |
| ray fields (`transport: ray`, Kerengonen phase) | yes | headed parcels crossing one link per interval |

A bound ray pair cannot be built from rays alone: rays merge, are absorbed by
records, gathered by claims or answered by the registry; there is no rule by
which two rays reflect each other at a Node. The closest legal configuration
is a cavity of two mirror **records** (`transport: hold`, absorb plus
`kerengonen_mirror` re-emission), so the pair measured below is bound by a
configured record rule, and every reflection passes through a record for one
tick.

## Files and commands

`bound_pair_proxy.py` builds and runs every case; `expectations.json` was
fixed before the first run; `summary.json` is the recorded full run (600
ticks); `control-k4-200.json` is the no-mirror control extended to 200 ticks.

```sh
export PYTHONPATH=src
python examples/research/ray-form/bound_pair_proxy.py --output artifacts/research/ray-form              # 600 ticks, 45 s
python examples/research/ray-form/bound_pair_proxy.py --output artifacts/research/ray-form-smoke --ticks 40
```

Re-run at packaging with `--ticks 40` (3 s): every case bound, closed and
symmetric as recorded; the expected failure fails as recorded.

## Method

Phase steps 64, advance 4 per link, 8 quanta per ray, budget 1000. Geometries:
`adjacent` (mirrors at x = 0 and 1; every Node holds an absorber) and `cavity`
(mirrors at x = 0 and 2, lamp at x = 1; the centre Node has no absorber, so a
load there delays the rays under `ray_delay`). Loads: none; fixed k = 1, 2, 4,
8 through the `computation` baseline; the redshift sweep's growing profile
(baseline 7000, emission 16, budget 1000). `ray_phase_per_tick` off and on.
Read per tick: located parcels (resident rays or mirror stock), their phases,
the load at the centre. Clock rate = ticks per 64 phase steps.

## Results (600 ticks per run)

| case | bound (max separation <= d every tick) | ticks per cycle +/- sem (cycles) | k at the centre | quanta closed | phases symmetric |
| --- | --- | --- | --- | --- | --- |
| adjacent, no field | yes (1) | 16.0 +/- 0.0 (37) | - | yes | yes |
| adjacent, k = 1, 2, 4, 8, growing; `ppt` off and on (10 runs) | yes (1) | 16.0 +/- 0.0 (37) in all ten | as configured; growing 8 -> 17 | yes | yes |
| cavity, no field | yes (2) | 16.03 +/- 0.14 (37) | - | yes | yes |
| cavity, k = 1, `ppt` off / on | yes (2) | 16.03 +/- 0.14 (37) / 16.03 +/- 0.14 (37) | 1 | yes | yes |
| cavity, k = 2, `ppt` off / on | yes (2) | **21.36 +/- 0.18** (28) / 16.0 +/- 0.0 (37) | 2 | yes | yes |
| cavity, k = 4, `ppt` off / on | yes (2) | **32.0 +/- 0.40** (18) / 16.0 +/- 0.0 (37) | 4 | yes | yes |
| cavity, k = 8, `ppt` off / on | yes (2) | **52.9 +/- 1.0** (11) / 16.0 +/- 0.0 (37) | 8 | yes | yes |
| cavity, growing load, `ppt` off / on | yes (2) | 71.1 +/- 5.1 (8) / 16.0 +/- 0.06 (37) | 8 -> 17 | yes | yes |

The cavity law without `ray_phase_per_tick` is `T(k) = 16 (k + 2) / 3`: 16,
21.33, 32, 53.33 for k = 1, 2, 4, 8, matched within 3 %, and the growing-load
run tracks it cycle by cycle within one k step; the +2 is the mirror turnaround
(one tick on the bare clock) plus the second link of each half-cycle. With
`ray_phase_per_tick` the held ray's phase advances every waiting interval by
configuration and the period is 16.0 at every k. The adjacent geometry reads
"constant" trivially: every Node holds an absorber and the mirror record
commits on the bare carrier clock, so it says nothing about the hypothesis.

Classification by the pre-fixed rule (ratio T(k)/T(1): constant if within
5 %, ~1/k if T(k)/(k T(1)) within 5 %, else between): `ppt` off **between**
(r proportional to 3/(k + 2), tending to 1/k for large k); `ppt` on
**constant**.

| control | result |
| --- | --- |
| no mirrors, open row of 65, no load (120 ticks) | separation grows 2.0 links per tick; both parcels escape; escaped quanta 16 = all |
| no mirrors, k = 4 (120 and 200 ticks) | separation grows 0.487 links per tick (2 links per k ticks); escaped 0 within 120 ticks, 16 within 200; closed |
| cavity, k = 4, `computation_field` set with **no** `delay_direction` (40 ticks) | fails as expected: `ValueError: funded ray emission or absorption does not support a delayed carrier cycle` |

## Pass and fail against `expectations.json`

| item | pre-fixed | outcome |
| --- | --- | --- |
| E1 bound | separation <= d at every observation; 16 quanta in records + in flight + escaped | pass, 22 of 22 mirror runs |
| E2 adjacent | 16.0 +/- 2 % at every load, trivially | pass (and recorded as not evidence) |
| E3 cavity, `ppt` off | 16 (k + 2) / 3 within 3 %, "between" | pass |
| E4 cavity, `ppt` on | 16.0 +/- 2 %, "constant" | pass |
| E5 negative control | 2 links per tick at zero load, 2 per k ticks at k = 4, all quanta escape | pass |
| E6 isotropic delay | explicit failure, not a silent run | pass |
| E7 growing load | k 7 -> 15 over 500 ticks (measured 8 -> 17 over 600), period tracks the law within one k step (`ppt` off), stays 16 (`ppt` on) | pass |

## Candidate rule `bound-ray-pair-v1` (stated, not implemented)

Two counter-heading rays of equal amount arriving through opposite Ports of
one Node in one interval are retained at that Node with their headings
exchanged; the retained pair's phase advances once per interval; nothing
crosses a Link while the pair is bound; an absorber at the Node takes the pair
as it would take any ray; an unequal pair forwards as ordinary rays. Open
questions: how the rule composes with the same-heading merge rule and with
`ray_delay` when the two arrivals are staggered by a wait; whether the
exchanged headings keep the recoil accounting exact; how a bound pair
moves (both rays sharing a velocity component, the fourth step of the third
manuscript); and whether its phase rate under load is the mirror cavity's
`16 (k + 2) / 3`, the constant 16, or neither. The rule is written on the
[hypotheses page](../../../docs/HYPOTHESES.md#8-everything-that-moves-is-a-ray-records-only-hold)
as a candidate for the owner to accept or retire.

## Limits and what is not established

- The pair is bound by two mirror records, a configured rule; the engine has
  no two-ray reflection, so the proxy cannot say what a bound ray pair does.
- Every reflection spends one tick in a record on the bare clock, which is the
  "+2" of the measured law; a rule without records could have another law.
- One row, one parcel size, one phase advance; nothing about motion of the
  pair or about a detector response.
- No claim that everything that moves is a ray follows; the inventory says
  which existing forms are ray-form and which are not.
