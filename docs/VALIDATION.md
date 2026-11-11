# Implementation validation

## Connected clocks and geometric requirements

The core Rule3 engine, default tensor and default seed builder are unchanged. Optional builders compile new clock interactions into fixed tensor data; isolated geometric experiments live under `experiments/geometry/`. The [clock research record](CLOCK_RESEARCH.md) and [geometry audit](GEOMETRY_RESEARCH.md) distinguish exact identities, measured finite histories and physical requirements.

| Check actually run | Outcome |
|---|---|
| Complete suite with `GAUGE_LONG=1`, before the final metric-gate guard correction | 236 tests in 938.499 seconds; one existing expected failure, no unexpected failures |
| Complete suite after the guard correction | 237 tests in 881.613 seconds; one existing expected failure, no unexpected failures or skips |
| Final complete suite after flat-control validation | 238 tests in 870.617 seconds; one existing expected failure, no unexpected failures or skips |
| Default `L=3` CLI, 20 updates | Exact rewind; unchanged dynamics fingerprint; zero sampled ledger, Lorenz and dressed-continuity residuals |
| Default `L=4` saved-input audit, 120 updates | Exact rewind and replay; 152,616 official records; independent scalar oracle has zero mismatches |
| Wheel installed outside checkout | Saved 120-update audit replays exactly; optional connected-clock paired control also runs and rewinds |
| Resolution lift, clock ports, bridge and bounded routing | Exact algebra, support and inverse regressions pass; no default-law changes |
| Public connected-clock controls | Forward and reverse official-record influence, zero-bridge negative control, exact rewinds and no violations of the tested storage cone |
| Held-out clock preparations | Three additional seeds, a phase-decorrelated preparation and a reference packet each complete 5000 updates and exactly rewind; phase alignment is not created spontaneously and metric growth remains |
| Long baseline preparation control | Retained 46,000 updates on L=4 plus complete exact inverse; 29 peak counter bits, 58,603,903 official records and no full-seed recurrence; requested 100,000 horizon not reached |
| Raw relational metric-clock gate | Four 32,768-update preparations exactly rewind; slow pair passes tolerance, faster pairs fail; corrected resource-guard and insufficient-data statuses remain distinct from physical acceptance |
| Strict local clock composition | Rank four and zero physical-support violations; finite runs rewind, but the physical-link Lorenz constraint remains failed in the wave-margin experiment |
| Isolated conformal geometry experiments | Sixteen exact Engine histories and reversals; restricted clock-rate and nonlinear-history convergence, not a derivation of general Einstein dynamics |
| Planar vacuum tensor-wave sector | Exact invariant linear trace/divergence sector; 256 actual updates and rewind pass; 32,224 audit records and no official detector records |
| Separate integer curl waves | Exact all-time travelling-profile proof; 18 gears, two polarizations, 24 proper rotations, fixed remainders and exact rewinds; general oblique instability retained as a negative control |
| Separate two-bank retiming | Six 56-update Engine histories on three chosen axes and two divisors; exact half-speed translation, period 14 and rewinds; an unprepared linear-growth control prevents an all-seed claim |
| Local travelling metric and test probes | Exact declared linearized lattice Ricci/constraint identities; two 84-update rank-four probe histories reverse exactly and show different official records; one-way coupling and unequal speeds remain explicit |
| Metric carry-lock control | Four million-update forward/inverse reduced histories; each has a 32-update actual-Engine prefix check; a proved finite drift interval differs from the remainder-free spectrum |

The expected failure is the previously recorded TC.15 Bell-style experiment. No physical acceptance tolerance was relaxed. The new metric tool originally could accept a run whose growth guard was reached on its final requested update; the corrected tool records the guard explicitly and rejects that acceptance. A second review found that a completed comparison could use a guard-failed flat control: the tool now requires a valid reference trajectory and rates for acceptance, while retaining numerical ratios as diagnostics. Both failures have actual-Engine regression fixtures. Insufficient clock crossings are inconclusive, not a measured agreement or disagreement. The published long clock trajectories had a valid completed flat control and did not reach the guard; their original execution hashes and both validation-only patches are separately recorded.

The [long-run manifest](evidence/clock_long_runs.json) gives actual completed horizons, exact states' hashes, resource stops and inverse results. [Connected-clock evidence](evidence/connected_clocks.json), [raw metric-clock evidence](evidence/metric_clock_gate.json), [the metric-source audit](METRIC_SOURCE_AUDIT.md) and the [geometry experiment index](../experiments/geometry/README.md) provide the individual reproduction commands. A successful command or test suite includes verified negative physical findings; it does not assert gravity, quantum entanglement, cosmological bounces or complexity maximization.

The compact [integration validation record](evidence/clock_integration_validation.json) records the final suite, default-law preservation, installed-wheel replay and source hashes. The wheel's flat-control regression was also executed outside the checkout: an invalid 22-update reference correctly blocks acceptance of its otherwise completed 128-update comparison.

## Integrated algebra and repository audit

The [system map](SYSTEM_MAP.md) ties current claims to their assumptions and code. The default recurrence, coefficients, seed construction and both tensor fingerprints are unchanged. Corrections cover exact large-divisor readout/mirror arithmetic, invalid rewind horizons, misleading metadata and portable demo output paths.

| Check actually run | Outcome |
|---|---|
| Complete pre-correction suite with GAUGE_LONG=1 | 184 tests in 812.300 seconds; 183 passed, one expected failure, none skipped |
| Complete corrected suite with GAUGE_LONG=1 | 193 tests in 788.486 seconds; 192 passed, 1 expected failure, none skipped |
| Focused final regressions and complete-state migration fixture | 18 passed in 5.334 seconds |
| Default L=4, 120 updates | Exact rewind and saved-input replay; 152,616 official records; online and exported-event decoders agree |
| Optional single-edge L=4, 120 updates | Exact rewind and replay; 152,617 official records; online and exported-event decoders agree |
| Independent scalar receiver oracle | 2,292 default and 2,832 mediator gear transitions; zero mismatches, including beyond-int64 states |
| Local perturbation controls | Zero changed sites outside the storage cone over the tested three updates |
| Default matched-choice control, 12 updates, preparation RNG 13 vs 17 | 275 differing dp quotient site-updates and different official records on all 12 updates; identical full hand/reader and pair-difference histories |
| Metric/clock negative control, 40 updates | 9,605 paired cosmic records unchanged; no dependency path in either construction |
| Electromagnetic state diagnostic, 40 updates | Baseline passes; unadapted mediator readout fails from update 2; explicit passive source-coordinate map passes |
| Default CLI smoke | All 20 requested updates; exact rewind; zero sampled ledger, Lorenz and dressed-continuity residuals |
| Installed wheel outside checkout | Exact 120-update replay from saved tensor and seed |
| Genericity control | Metadata/name changes preserve complete forward/inverse histories for the same indexed polynomial and Q |
| Group/coupling enumeration | 110,592 associativity cases, 24 proper cube rotations and 110,592 equivariance cases across eight sign choices passed |
| Repository-wide static checks | All 168 previously tracked Python files and all new sources parse; 286 tracked JSON records parse; internal imports and current documentation links resolve |
| Demo portability checks | EM census module/direct modes, O6 one-step module/direct modes and historical-input post-hoc reader passed |
| Canonical tensor inventory | 22 builder blocks, 382 types, rank four, 18,592 live monomials; six independent namespace groups and 15 gear components |

The full-suite expected failure is TC.15, the already recorded negative Bell-style router experiment. No assertion thresholds were loosened. The default complete-state migration traces remain identical. The new inventory records absent interactions rather than adding unproved physical couplings; the matched cosmic preparation still cannot select different future hand/reader trajectories by changing detector load/token data.

All production library/tool modules import, but this is not a blanket import of research demos: several execute expensive experiments at import. Two demos use test helpers and require a checkout. The review covers code structure, documented proofs and scoped numerical tests, not an independent proof of every claim in every historical research record. The historical notes are explicitly separated from the current specification; original numerical evidence is retained.

Reproduce the final checks with the commands in the repository README, plus:

```bash
python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
python -m universe24.tools.audit_contract --single-edge --stiffness 33554432 --L 4 --steps 120 --out runs/single-edge
python -m universe24.tools.physics_gate --steps 40 --out runs/physics-gate/report.json
```

The compact [integration evidence](evidence/integrated_validation.json) records exact hashes and outcomes. These checks do not derive GR, general quantum statistics, an atom, or a maximum-complexity selection law.

## Single-edge experiment

The optional construction and its exact equations are in [SINGLE_EDGE_IMPLEMENTATION](SINGLE_EDGE_IMPLEMENTATION.md). It is not the default. Core Rule3 and default tensor coefficients are unchanged.

| Check actually run | Outcome |
|---|---|
| Affected core, ONE, migration and audit suite with the first six new strict-edge tests | 38 passed in 48.661 seconds |
| Final strict-edge and audit suite, including passive mapping and physical controls | 17 passed in 6.845 seconds |
| Full 472-type tensor physical-support check | Zero violations; rank four; maximum support diameter one edge |
| Independent original-polynomial and endpoint-force comparison | Every row at all 27 sites agrees |
| Arbitrary extended-state inverse, including large integers | Exact; does not assume H=U |
| L=4, 120 updates at k=33,554,432 | Exact rewind/replay; 152,617 official records decoded consistently; peak state length 36 bits |
| k=Q strong-coupling control | Growth limit exceeded at update 38; the recorded prefix remains exactly invertible |
| Inherited electromagnetic identity, 40 updates | Baseline passes; unadapted new readout fails from update 2; explicit source-coordinate view passes |
| Metric perturbation / clock control, 40 updates | 9,605 cosmic records identical in each paired comparison; no tensor dependency path from metric sector to cosmic clocks |

The readout mismatch is repaired by an explicit passive map, not by changing the evolution. The gravity-independent cosmic clock remains a physical obstruction if interpreted as a universal proper-time clock. The complete prior suite was not rerun locally because the common engine, default builders and default seed are unchanged; affected checks include the full-state default migration fixture. CI also runs the full discovery and short baseline/strict audits. No physical-equivalence or Einstein-spacetime certificate is implied.

## Tensor, seed and click audit

The [contract audit](CLICK_CONTRACT_AUDIT.md) records the current numerical results and physical limitations. The scalar recurrence and default polynomial coefficients were not changed.

| Check actually run | Outcome |
|---|---|
| Full suite with `GAUGE_LONG=1` | 173 tests in 804.005 seconds: 172 passed, one pre-existing expected failure; none skipped |
| Final affected suite: core, ONE, migration fixture and all eight new audit regressions | 32 passed in 47.079 seconds |
| Independent scalar receiver-loop check | 2,292 sampled gear transitions, including integers beyond int64; exact agreement |
| Default audit, L=4, 120 updates, preparation RNG 13 | Exact rewind, fixed tensor, passive observers and exact saved-input replay |
| Official event-only decoder | 152,616 records; counts, classes, signed quotient sums and selected clock sequence match online readout |
| Preparation control, RNG 17 | Same record counts and selected clock sequence, different C1/C2 counts; not a Born-rule derivation |
| Local perturbation on L=7 | No influence outside the one-edge-per-update storage cone over three updates |
| Short CI audit, L=3, 12 updates | Passed, including exported-event decoder and saved-input replay |
| Installed wheel outside the checkout | Saved-input replay passed |
| CLI forward/rewind | Seven-update run and final two-update report check passed; partial reporting windows retained |
| Source syntax, report JSON and diff whitespace | Passed |

The full-suite discovery preceded the addition of two final regression tests and the final engine-law immutability guard. The final 32-test affected suite covers all eight regressions and the final core changes. The short CI audit and wheel replay also exercised the final execution path. These are actual executions, not a claim that the full discovery ran twice.

The expected failure remains TC.15 below. Passing long regressions preserves their documented negative physical findings. The audit verifies storage locality; including both geometric endpoints of link gears, some terms span two edges and fail the stronger single-physical-link condition. No claim of complete quantum mechanics or general relativity follows from these checks.

## ONE migration validation

The repository was reorganized from the ONE implementation at commit `d73f78e827e3d7b15c06f729c52fa3c2cc241ed2`. ONE is now the only active runtime under `universe24/`. The cube algebra moved into `universe24/algebra/`; the former standalone engine and unrelated experiments were removed from the current tree, remaining in Git history.

### Checks actually run

Environment: Python 3.12, NumPy 2.3.5, SymPy 1.14.0.

| Check | Outcome |
|---|---|
| Original ONE tests before restructuring | 12 passed |
| Complete migrated ONE suite | 166 tests; 163 passed, 2 opt-in long tests skipped, 1 pre-existing expected failure |
| Both skipped long gauge experiments, explicitly enabled | Reproduced the two documented failed stability criteria |
| Baseline strong-drive test before migration | Reproduced the same failure at update 6 |
| Revised explicit negative-result regressions for both long experiments | 2 passed; physical stability criteria remain failed |
| Final quick suite, including migration fixtures | 13 passed |
| Complete-state comparison against the original code | Two preparations, L=3 and L=4, initial state plus six updates each; all a,b,r hashes identical; exact rewind |
| Default CLI run | 20 updates on L=3; exact rewind; zero sampled quotient-ledger and other reported balance failures |
| Built wheel and installed away from checkout | Successful; installed CLI completed a separate forward/rewind run |
| Python source compilation and diff whitespace checks | Passed |

The long-test changes do not loosen a physical acceptance threshold or alter the tensor. They explicitly test the already documented negative behavior: strong-drive G6 runaway and G6b SU(2) relay cases at lam=1,2 exceeding the original 0.5 deviation bound. Positive calibrated arms retain their original threshold. The reports continue to state the original failed criterion.

The remaining expected failure is TC.15, the odd-Q continuously exposed Bell-style router. Its coincidence-conditioned result does not satisfy the proposed quantum correlation claim. It is a recorded negative experiment, not an unexplained software exception or a derived Bell violation.

The updated CI enables the long regressions and discovers all ONE tests with package context. The local full run predates the addition of the migration fixture test; that test was run separately and again in the final quick suite. These numbers describe actual executions, not a claim that every possible seed, parameter choice, horizon or physical interpretation was verified.

### Reproduction

```bash
python -m pip install '.[validation]'
GAUGE_LONG=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v
python -m universe24 --L 3 --tmax 20 --budget 120 --out runs/demo --tag demo --rewind
```

Tests write fresh records under `runs/tests/`. The pre-migration trace fixture is checked in at `universe24/tests/fixtures/one_before_migration.json`; it covers the full state, not just visible events. A default trace fingerprint unchanged by the migration is necessary for behavior preservation, not sufficient evidence for a physical theory.
