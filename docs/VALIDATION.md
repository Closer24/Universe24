# Implementation validation

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
