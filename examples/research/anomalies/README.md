# Anomalies: four lattice measurements against published numbers

Exploration evidence of 2026-09-16 at commit `e5b5911`, source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`
(Python 3.14.0rc2, headless). Every world is a supplied configuration on the
generic engine; every number is a read-only inventory audit at host lattice
coordinates; no unit, constant or calibration is identified. The four
experiments reuse the configurations of the
[relativity probes](../../relativity-probes/README.md) (closed loaded row) and
the [gravity probe](../../gravity-probe/README.md) (held bodies in a ray field)
without changing them, and each has an `expectations.json` written before the
run under `results/<experiment>/`.

The questions, in the words of hypotheses
[6](../../../docs/HYPOTHESES.md#6-dark-matter-is-a-closed-dimension-not-extra-mass),
[7](../../../docs/HYPOTHESES.md#7-redshift-without-recession-and-no-dark-energy)
and [9](../../../docs/HYPOTHESES.md#9-a-candidate-law-stated-so-that-it-can-fail):
(E1) what Tolman surface-brightness exponent the loaded closed row implies;
(E2) what redshift-distance relation, effective Hubble rate and deceleration
the linear and quadratic loads give; (E3) what force-law exponent a `1/r^2` ray
source has when one dimension is closed and short; (E4) whether a clock built
from the model's own rays and mirrors keeps the bare rate under load.

## Files and commands

| script | recorded runs (host time) | re-run at packaging |
| --- | --- | --- |
| `e1_rows.py` | `--rule link` (rows 24, 48, 96 plus the zero-emission control: 41 + 180 + 650 s), `--rule interval` (same) | no |
| `e1_geometry.py` | `--baseline 0` (1019 s), `--baseline 3000` (1002 s) | no |
| `e2_hubble.py` | `--load linear` (rows 16-96, 549 s), `--load quadratic` (rows 16-64, 1188 s) | `--load linear --rows 16` (8 s, identical to the recorded row) |
| `e2_refit.py` | not run on 2026-09-16; run at packaging on the two recorded summaries, output committed as `refit.json` | yes |
| `e3_rotation.py` | `--box periodic-slab --depth 3` (722 s), `--depth 9` (573 s), `--box open-cube --side 61` (540 s), `--box open-slab --depth 3` (51 s) | `--box open-slab` (35 s, identical fits) |
| `e4_light_clock.py` | defaults with `--length 48` (`along`, emission 16: 684 s), `--emission 0` (112 s), `--direction none` (fails, see E4) | `--length 16 --ticks 300` (19 s) |

```sh
export PYTHONPATH=src
OUT=artifacts/research/anomalies
python examples/research/anomalies/e1_rows.py --output $OUT/e1-rows-link --rule link
python examples/research/anomalies/e1_rows.py --output $OUT/e1-rows-interval --rule interval
python examples/research/anomalies/e1_geometry.py --output $OUT/e1-geometry-k1 --baseline 0
python examples/research/anomalies/e1_geometry.py --output $OUT/e1-geometry-k3 --baseline 3000
python examples/research/anomalies/e2_hubble.py --output $OUT/e2-linear --load linear
python examples/research/anomalies/e2_hubble.py --output $OUT/e2-quadratic --load quadratic
python examples/research/anomalies/e2_refit.py $OUT/e2-linear/summary.json --output $OUT/e2-linear
python examples/research/anomalies/e3_rotation.py --output $OUT/e3-slab3 --box periodic-slab --depth 3
python examples/research/anomalies/e3_rotation.py --output $OUT/e3-slab9 --box periodic-slab --depth 9
python examples/research/anomalies/e3_rotation.py --output $OUT/e3-cube --box open-cube --side 61
python examples/research/anomalies/e3_rotation.py --output $OUT/e3-open-slab --box open-slab --depth 3
python examples/research/anomalies/e4_light_clock.py --output $OUT/e4-along --length 48
python examples/research/anomalies/e4_light_clock.py --output $OUT/e4-control --length 48 --emission 0
```

`results/baseline-row48/summary.json` is the redshift sweep's own row 48 at
this fingerprint (`examples/relativity-probes/redshift_sweep.py`), kept as the
reference the E1 and E2 rows extend: z = 0.7727 at D = 41.5, control at zero
emission z = 0, single source z = 1.0682. The committed E2 summaries omit the
per-hop `schedule` lists (a `packaging_note` says so); `e2_hubble.py` writes
them again. `e4_light_clock.py` also writes `initialization.json` and
`raw_observation.json` per run; only `summary.json` is committed.

## E1: the Tolman exponent of the lattice

Reading of the documents: surface brightness scales as `(1 + z)^-n` with
`n = a + b`, `a` the exponent of the count rate and `b` of the per-photon energy
read as the phase rate; the geometric factors (`1/D^2` dilution, `s/D` angular
size) are measured separately and must not depend on the load. Rows: the closed
loaded row (baseline 7000, emission 16 per Node per tick, budget 1000) at
lengths 24, 48 and 96 with the light carrying a Kerengonen phase.

| row (rule `link`) | D | z (eye counter) | span stretch | frequency ratio measured / predicted | gaps on the eye clock |
| --- | --- | --- | --- | --- | --- |
| 24 | 17.5 | 0.2159 | 1.1758 | 0.8515 / 0.8505 | 9 9 9 9 10 10 10 10 10 10 11 |
| 48 | 41.5 | 0.7727 | 1.7143 | 0.5832 / 0.5833 | 13 13 14 14 14 14 14 15 15 15 15 |
| 96 | 89.5 | 2.8068 | 3.6813 | 0.2715 / 0.2716 | 28 29 29 30 30 30 31 31 32 32 33 |
| 48, zero emission (control) | 41.5 | 0.0 | 1.0 | 1.0 | 7 x 11 |

| exponent (3 rows, stretch 1.18 to 3.68) | rule `link` | rule `interval` |
| --- | --- | --- |
| a (rate) | 1.0 (by construction of the gaps) | 1.0 |
| b (phase rate) | 1.0013 +/- 0.0008 | -0.006 +/- 1.46 (the phase-rate ratio changes sign: -0.9394 -> -0.6514, -0.1311, +0.4735; the fit of its magnitude is not a measurement) |
| n = a + b | **2.0013 +/- 0.0008** | 0.99 +/- 1.46 |

Geometry (`e1_geometry.py`): periodic cube of side 141, two lamps 4 links
apart, 4,096 golden-spiral headings, eight eyes at in-plane distances 3.2 to
18.0, one 64-tick sweep after the front has passed, with no load (k = 1) and
with a uniform static load (baseline 3000, k = 3).

| measurement | k = 1 | k = 3 |
| --- | --- | --- |
| dilution exponent, count against distance (8 eyes) | -2.171 +/- 0.194 | -2.171 +/- 0.194 |
| angle-size exponent, angle between the lamps against D | -1.063 +/- 0.061 | -1.063 +/- 0.061 |
| measured / static angle at the 8 eyes | 1.03, 1.03, 1.01, 1.01, 0.99, 1.00, 0.96, 0.74 (1 count each at the last eye) | identical |
| quanta closed, window free of images | yes, yes | yes, yes |

The two geometry tables are identical count for count: the load delays every
ray equally and changes neither the dilution nor the angular size.

Against the pre-fixed conditions: code pass (all rays absorbed, quanta
conserved, eye clock = ticks, zero-load control a = b = 0, dilution -2 +/- 0.3
with and without load) **yes**; "falsified if the lattice n differs from 2 by
more than its fit error under reading B": n - 2 = 0.0013 +/- 0.0008, 1.6 fit
errors, so that clause is **not met as literally written**, while the
pre-fixed verdict rule ("compare to 4 and to the 2.59-3.37 band; if lattice
n < 2.59 - 2 sigma the data favour theory over the candidate") gives: lattice
n = 2.001 lies below 2.25, so the raw Lubin and Sandage exponents
(2.59 +/- 0.17 in R, 3.37 +/- 0.13 in I, reduced under an expanding geometry
before any luminosity-evolution correction) favour the expansion value 4 over
the lattice value 2, with the pre-registered caveat that the data reduction
assumes expansion and was not redone under a static-lattice metric.

## E2: the redshift-distance relation and the effective Hubble rate

Linear load (constant emission 16, hop time k = 8 at launch) and quadratic load
(each mass body's emission proportional to its own bare-rate counter,
launch at counter 1500, k = 30 at launch). Twelve rays per row; z from the mean
absorption gap over the launch hop time on the eye's counter.

| load, row | D | absorbed | z +/- gap scatter | k_o / k_e | H at observation (1/k dk/dt) | q at observation |
| --- | --- | --- | --- | --- | --- | --- |
| linear, 16 | 9.5 | 12 | 0.0682 +/- 0.0197 | 1.0625 | 0.00195 | 0 |
| linear, 24 | 17.5 | 12 | 0.2159 +/- 0.0244 | 1.2083 | 0.00171 | 0 |
| linear, 32 | 25.5 | 12 | 0.3864 +/- 0.0264 | 1.375 | 0.00149 | 0 |
| linear, 48 | 41.5 | 12 | 0.7727 +/- 0.0283 | 1.7604 | 0.00114 | 0 |
| linear, 64 | 57.5 | 12 | 1.2955 +/- 0.0422 | 2.2812 | 0.00088 | 0 |
| linear, 96 | 89.5 | 12 | 2.8068 +/- 0.0568 | 3.7812 | 0.00053 | 0 |
| quadratic, 16 | 9.5 | 12 | 0.3061 +/- 0.0467 | 1.2861 | 0.00091 | -0.607 |
| quadratic, 24 | 17.5 | 12 | 0.7788 +/- 0.0759 | 1.7472 | 0.00080 | -0.574 |
| quadratic, 32 | 25.5 | 12 | 1.5848 +/- 0.1315 | 2.5278 | 0.00068 | -0.548 |
| quadratic, 48 | 41.5 | 8 of 12 | not formed | - | - | - |
| quadratic, 64 | 57.5 | 4 of 12 | not formed | - | - | - |

H at launch is 0.00228 (linear) and 0.00102 (quadratic); in every row H at
observation is lower: **H falls with age** in both histories. The configured
load law reproduces every measured hop (maximum deviation 0 ticks linear, 1
tick quadratic). Light is conserved and the field total grows linearly
(linear) or not linearly (quadratic) with age in every row.

FRW-correspondence fit `D = (1/H) n [(1 + z)^((n-1)/n) - 1] / (n - 1)` with a
launch-offset nuisance, `n` on a grid 0.50 to 4.00:

| fit | linear (6 points) | quadratic (3 points) |
| --- | --- | --- |
| recorded run, sigma_z = gap scatter | n = 1.00 at the grid edge, chi2 = 254: the gap scatter understates sigma_z | n = 1.00 at the grid edge, chi2 = 211 |
| `e2_refit.py`, sigma_z = gap scatter and half-step 0.5/k_e in quadrature (packaging) | n = 1.00, 1-sigma interval [0.84, 1.23], **q0 = 0.00** [-0.19, +0.19], chi2/dof = 0.007 | 0 degrees of freedom: n = 0.64 with interval [0.5, 1.61]; not a measurement |
| residual-scaled (sigma so that chi2/dof = 1) | n [0.99, 1.01], q0 [-0.01, +0.01] | 0 degrees of freedom |

Against the pre-fixed conditions: linear n within 2 sigma of 1 **yes**; H
decreasing with age **yes** (both); quadratic n within 2 sigma of 2: **not
evaluable** (rows 48 and 64 did not absorb all twelve rays within their tick
budgets, leaving three points for a three-parameter fit); the kinematic q read
off the hop schedule is -0.55 to -0.61 for the quadratic load and 0 for the
linear load, which is the "-> -0.5" of the summary line. The distance-ladder
bias quoted in `expectations.json` (below 1 % at q0 = -0.29, about +1.5 % at
q0 = 0 for z = 0.02-0.15) is the pre-registered estimate; no lattice run
measured it, and the lattice carries no absolute calibration, so only the sign
and shape of H(t) and q are results.

## E3: the force-law exponent with a short closed dimension

The gravity probe's held-body configuration: a source at the centre emits
`radiation` rays over 4,096 golden-spiral headings (64 per tick), and a held
body of mass 1 gains momentum toward the source for every ray crossing its
Node (exchange coupling, momentum += mass x flux / D; rays pass through, so
bodies do not shadow each other). Bodies in the source's plane at r = 3 to 24
on the four axes and r = 2.8 to 24.0 on the four diagonals (28 bodies); pull
per tick over one full sweep after the front has passed every body; error =
standard error over the four directions at each radius; fit `pull ~ r^p`.

| box | shape | axis p (7 radii) | diagonal p (7 radii) | pooled r >= 4 (12 radii) | momentum closed / all pulls inward / no laps |
| --- | --- | --- | --- | --- | --- |
| periodic slab, depth 3 | 201 x 201 x 3 | -0.838 +/- 0.120 | -1.153 +/- 0.041 | **-0.974 +/- 0.104** | yes / yes / yes |
| periodic slab, depth 9 | 201 x 201 x 9 | -1.044 +/- 0.159 | -1.455 +/- 0.084 | -1.134 +/- 0.130 | yes / yes / yes |
| open cube (control) | 61 x 61 x 61 | -1.985 +/- 0.160 | -2.140 +/- 0.091 | **-2.044 +/- 0.121** | yes / yes / yes |
| open slab, depth 3 (leak control) | 201 x 201 x 3 | -1.985 +/- 0.160 | -2.140 +/- 0.091 | -2.044 +/- 0.121 | yes / yes / yes |

Period-9 slab split at the period: r < 9 (8 radii) **-1.47 +/- 0.19**;
r > 9 (6 radii) **-0.70 +/- 0.45**.

Against the pre-fixed conditions: closed slab within 2 sigma of -1 **yes**;
open cube within 2 sigma of -2 **yes**; a transition in the period-9 slab
between r = 5 and r = 12: the exponent changes from -1.47 inside to -0.70
outside, though the inside value is not the -2 the plan expected; the open
slab was expected to be steeper than -2 and is instead identical to the open
cube body for body (an in-plane body receives the same rays in both open
boxes). The pre-registered discriminating observable stands as stated: the
lattice's transition is set by a length (the period), nature's by an
acceleration (the radial acceleration relation), and the lattice cannot decide
between them without a calibration of the period.

## E4: a light clock under a growing load

A [L, 5, 1] periodic lattice whose load grows uniformly (a mass body at every
Node emits `computation` 16 per tick; baseline 3000; budget 1000; `ray_delay`
with `delay_direction: along`). A `light` ray bounces along y between a bottom
mirror at y = 0 and a top mirror at y = 4 (mirror records: absorb and re-emit
along the reversed heading), one clock in the source column and one in the
eye column 47 links away. Every catch at the source's bottom mirror fires one
`signal` quantum toward the eye; the eye absorbs the signals and runs the
bare-rate counter of the redshift sweep in the same record.

| run | periods | k over the run | log-log slope of P against k | least-squares line (packaging) | z by bare counter | z by light clock |
| --- | --- | --- | --- | --- | --- | --- |
| `along`, emission 16 | 28 | 4 -> 62 | 0.956 +/- 0.006 | P = 5.96 (+/- 0.02) k + 3.6 | **0.608 +/- 0.042** (24 signal pairs) | **0.022 +/- 0.022** |
| `along`, emission 0 (control) | 67 | 3 | undefined (k constant) | P = 22 in 67 of 67 (= 6 x 3 + 4) | 0.0 +/- 0.0 (64 pairs) | 0.0 +/- 0.0 |
| default (isotropic) delay direction (control) | run rejected by the engine: `funded ray emission or absorption does not support a delayed carrier cycle` | | | | | |

The source and eye clocks show the same 28 periods. Signals were conserved,
the two clock rays were never lost, and the eye's counter equalled the tick
count throughout. The pre-registered period law was `P = 8k + 2`; the
measured law is close to `P = 6k + 4` (residuals P - 6k between 0 and 6 ticks
over the 28 periods, whose k changes within a period).

Against the pre-fixed conditions: code pass **yes**; "falsified if the light
clock's log-log slope against k is within 2 sigma of 1": the slope is
0.956 +/- 0.006, seven standard errors below 1 and far from 0, which the
pre-fixed classification calls "between"; the pre-fixed verdict rule ("slope
near 0 keeps the candidate; slope near 1 retires it unless a bound-pair clock
behaves differently") is left to the owner with the two readings side by side:
the bare counter reads 1 + z = 1.61 where a clock made from the model's own
moving parts reads 1.02.

## Not representable at this revision

No lattice experiment was configured for the muon g-2 or the neutron
lifetime: the [entity audit](../entity-audit/README.md) records no magnetic-moment
dynamics (the property is absent for 29 of 35 particle records, the muon among
them) and no decay law (all 17 interaction families are `descriptive_only`),
so neither anomaly has a representation to measure.

## Controls

E1 zero emission (a = b = 0, z = 0) and the static load that leaves the geometry
unchanged; E2 the configured law checked against every hop; E3 the open cube
and the open slab; E4 zero emission (P constant, z = 0) and the isotropic
delay, which the engine refuses explicitly instead of running silently.

## Limits

- Rows of 12 rays, three to six row lengths, one seed each; errors are the
  scatter of the eleven integer gaps, and z is quantized in steps of 1/k_e.
- E1 fits three points; E2's quadratic family fit has zero degrees of freedom;
  E3 averages four directions per radius on a lattice whose axes and diagonals
  differ (axis and diagonal exponents are reported separately).
- The light clock's period is read against the hop time at the period's
  midpoint while k changes during a period; the mirror is a hold record, not a
  ray, because the engine has no rule by which two rays reflect each other
  (see [ray form](../ray-form/README.md)).
- No absolute calibration: no unit of length, time or mass is identified, so no
  H0, no galaxy radius and no clock rate in physical units follow.

## What is not established

- No physical law is derived: the load law, the delay direction, the mirror
  rule and the coupling are supplied in JSON.
- Whether the published Tolman exponents, rotation curves or Hubble diagram
  are explained is not decided here; the lattice numbers are placed beside the
  published ones with the reduction assumptions the published numbers carry.
- Whether a bound ray pair (rather than a mirror cavity) would clock
  differently is untested; that is the first item of the third manuscript in
  hypothesis 8.
