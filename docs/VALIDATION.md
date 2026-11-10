# ONE migration validation

The repository was reorganized from the ONE implementation at commit `d73f78e827e3d7b15c06f729c52fa3c2cc241ed2`. ONE is now the only active runtime under `universe24/`. The cube algebra moved into `universe24/algebra/`; the former standalone engine and unrelated experiments were removed from the current tree, remaining in Git history.

## Checks actually run

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

## Reproduction

```bash
python -m pip install '.[validation]'
GAUGE_LONG=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v
python -m universe24 --L 3 --tmax 20 --budget 120 --out runs/demo --tag demo --rewind
```

Tests write fresh records under `runs/tests/`. The pre-migration trace fixture is checked in at `universe24/tests/fixtures/one_before_migration.json`; it covers the full state, not just visible events. A default trace fingerprint unchanged by the migration is necessary for behavior preservation, not sufficient evidence for a physical theory.
