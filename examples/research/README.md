# Research explorations of 2026-09-16

Five exploration studies run on 2026-09-16 against commit `e5b5911` (merge of
PR #135) of this repository. Every study here is **exploration evidence**: a
read-only audit of what the engine does under a supplied configuration. None of
it is integrated behavior, none of it changes an engine rule, and none of it is
proof of a physical law. A number below moves a hypothesis on the
[hypotheses page](../../docs/HYPOTHESES.md) only as a measured result with its
fingerprint; deciding what the result means is left to the owner.

Provenance shared by all five studies:

| item | value |
| --- | --- |
| date | 2026-09-16 |
| commit | `e5b5911` (`Merge pull request #135 from Closer24/perf/focus-reuse-active-links`) |
| source fingerprint | `4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36` (`event_universe.runner.source_fingerprint()`, SHA-256 over `src/event_universe/**/*.py`; recorded as `source_sha256` in every result file) |
| interpreter | Python 3.14.0rc2, headless, no visualization except where the study says so |
| packaging | scripts re-run at commit `d5d2427` (fingerprint `39a611ddd1df3f549566a233417c3cb2c28cb953fc52cd388b96f5cbde04a516`) on the cheap modes listed in each README; the recorded numbers were reproduced where the mode allowed a comparison |

What is committed for each study: the scripts (fixed so that they run from the
repository root with `PYTHONPATH=src` and an `--output` directory), the
`expectations.json` written before the runs, the small recorded result files,
and a README with the question, method, exact commands, result tables with
sample sizes and errors, controls, pass/fail against the pre-fixed conditions,
limits and what is **not** established. Run directories, HTML views, GIFs,
event traces and state dumps are not committed; every README says how to
regenerate them.

## The five studies

| study | one paragraph |
| --- | --- |
| [Bell and postulate 22](bell-postulate-22/README.md) | Four experiments on the bonded Bell world of the [Bell probe](../bell-chsh/README.md): E1 changes one pair's registry number and finds every differing Node inside the forward cone of the end whose answer changed (144 world pairs, 0 violations, the front exactly on the cone edge); E2 finds the product of the two outcomes independent of which end asks first (4096 of 4096 pairs identical) and, in a flagged private-state variant, dependent only on the setting present at the asking tick; E3 finds no dependence between the world's own number and settings chosen from the world's own generator (pooled p = 0.44 over 2^20 pairs; the raw affine ticket state is a degenerate chooser); E4 finds that two pairs born at one Node and tick share one bond (an implementation limit), that a replayed detector encounter draws nothing, and that a missing end leaves the other end's marginal even. One E2 rate at z = 3.59 and one E3 p = 0.002 are traced to block fluctuations of consecutive seeds. |
| [Anomalies](anomalies/README.md) | Four lattice measurements against published anomalies: the Tolman surface-brightness exponent of the closed loaded row (n = 2.0013 +/- 0.0008 under the per-link phase rule, against 2.59 +/- 0.17 and 3.37 +/- 0.13 in the raw data and 4 for expansion); the force-law exponent of a 1/r^2 ray source (-0.97 +/- 0.10 in a closed period-3 slab, -2.04 +/- 0.12 in an open cube, -1.47 +/- 0.19 inside and -0.70 +/- 0.45 outside the period in a period-9 slab); the redshift-distance relation of the linear and quadratic loads (H falls with age; q = 0 for the linear load and -0.55 to -0.61 for the quadratic load read from the hop schedule); and a light clock built from the model's rays and mirrors, whose period grows as about 6k + 4 with the hop time k and which reads z = 0.022 +/- 0.022 where the bare counter reads 0.608 +/- 0.042. The muon g-2 and the neutron lifetime have no representation at this revision. |
| [Ray form](ray-form/README.md) | An inventory of which engine forms are rays and which are not, the finding that a bound pair of counter-heading rays cannot be built from rays alone, and a proxy cavity of two mirror records with one Kerengonen ray bouncing each way: bound for 600 ticks in all 22 mirror runs, ticks per cycle 16(k + 2)/3 under a load k without `ray_phase_per_tick` and 16.0 with it, separation growing 2 links per tick in the no-mirror control. A candidate rule `bound-ray-pair-v1` is stated, not implemented. |
| [Entity audit](entity-audit/README.md) | A read-only audit of the entity catalog and its consumers: 35 particles, 11 fields, 14 disturbance families, 17 interaction families and 33 channels; all validators pass; 287 tests pass; every channel balances charge, baryon number and lepton sector; 56 headless runs complete with balanced accounting, each a labeled configuration probe rather than a physical law; all 17 interaction families are `descriptive_only`; no nucleus, atom or meson record exists. |
| [Electron-photon scatter](electron-photon-scatter/README.md) | A catalog-bound electron (charge -3 thirds, mass 511 keV/c^2) meeting six pulses of directional quanta under the declared radiation-scattering coupling, recorded and rendered: 60 quanta and total momentum (60, 0, 0) exact at every tick, six scatters of 2 quanta, two held quanta left at the old Node when the electron hops (a two-phase hold/scatter defect), and a configured outward halo that never decays because schema 1 dilutes only by redistribution. |

## Running the studies

```sh
export PYTHONPATH=src
python examples/research/bell-postulate-22/e1_lightcone.py --output artifacts/research/bell-postulate-22
python examples/research/anomalies/e2_hubble.py --output artifacts/research/anomalies/e2-linear --load linear
python examples/research/ray-form/bound_pair_proxy.py --output artifacts/research/ray-form
python examples/research/entity-audit/cross_checks.py
python examples/research/electron-photon-scatter/build_viz_config.py --output artifacts/research/electron-photon-scatter
```

Each README lists the full command set, the host time of the recorded runs and
which commands were re-run at packaging. Outputs belong under `artifacts/`
(ignored by Git); the committed `results/` folders are the recorded evidence
and are read, not written, by the analysis scripts unless `--output` points at
them.

## Reading the numbers

- "Pass" and "fail" in the READMEs refer to the conditions fixed in each
  `expectations.json` before the runs, and to nothing else.
- A recorded deviation is reported as recorded; where a follow-up run explains
  it, the follow-up is reported next to it with its own sample size.
- The statistical errors are standard errors of the recorded samples; the
  systematic limits are listed under "Limits" in each README.
- The [hypotheses page](../../docs/HYPOTHESES.md) carries a dated "Measured on
  2026-09-16" note per affected section that points back here.
