# Universe24 ONE

ONE is the sole active implementation in this repository. It is a research candidate for constructing observable events from exact, local, reversible integer dynamics. Its current default is **ONE v1**, built by `one_system()`.

Every gear uses the same scalar Rule3 recurrence. A fixed polynomial tensor supplies the input; the complete initial state supplies the seed. The forward loop never changes the tensor, injects a signal, selects a branch, or applies a click callback.

```python
ell, r_next = divmod(2 * u + r, D)
a_next, b_next = b, ell - a
```

This is an executable mathematical model, **not a demonstrated derivation of quantum mechanics or general relativity**. See [the algebra and limits](docs/MODEL.md) and [research status](docs/RESEARCH_STATUS.md).

## Install and run

Python 3.11 or newer:

```bash
git clone https://github.com/Closer24/Universe24.git
cd Universe24
python -m pip install '.[validation]'
python -m universe24 --L 3 --tmax 20 --budget 120 --out runs/demo --tag demo --rewind
```

`--out` is required. The run writes diagnostics and hashes there. `--rewind` checks recovery of the complete seed after the forward run; it is an audit, not a stage of forward dynamics. Larger boards and longer runs can be expensive. `--budget` may stop a run early; inspect the reported completed horizon.

## What is fixed, and what is chosen?

| Item | Current default |
|---|---|
| Space | Periodic cube of side `L >= 3`; six face neighbors |
| Elementary state | Exact integer triple `(a, b, r)` per gear and node |
| Gear types per node | **382**; the 48-gear `2O` block is one part |
| Shared scale | `Q = 2**33 + 1`; divisor `D = 6*Q` |
| Input | One fixed integer polynomial tensor; degree at most 3 |
| Tensor census | 18,592 live monomials; 736 designated one-way terms |
| Default cosmic coupling | Block diagonal: package and cosmic block do not read one another |
| Dynamics fingerprint | `77f6d251a8adfb2e4727bd2bd5ffeaa0e2ae3538aac393fe95c497fce754acf6` |

Choose the tensor configuration, board size and seed **before** a run. The seed then evolves deterministically. Reversibility retains the information underlying a coarse observed outcome; it does not erase alternate full states or prove a maximum-complexity selection law.

Optional builders are experiments within the same ONE engine. The coupled-doublet option is rejected because of observed runaway and is **off by default**. Einstein and CG2 constructions are also optional, not established properties of default ONE. The old standalone 48-channel implementation and its experiment trees are no longer present on the active branch; they remain in Git history.

## Code map

| Location | Responsibility |
|---|---|
| [`core/engine.py`](universe24/core/engine.py) | One exact forward engine and staged inverse |
| [`core/tensor.py`](universe24/core/tensor.py) | Polynomial input, locality and inverse-dependency validation |
| [`algebra/`](universe24/algebra) | Cube rotations, binary-octahedral group and fixed L0 matrices |
| [`layers/one.py`](universe24/layers/one.py) | Default complete ONE construction |
| [`prepare/one.py`](universe24/prepare/one.py) | Initial data only |
| [`observe/`](universe24/observe) | Passive measurements and audit identities |
| [`demos/one/run_one.py`](universe24/demos/one/run_one.py) | Reproducible run and reporting |
| [`tests/`](universe24/tests) | Exact arithmetic, locality, reversibility and scoped research tests |

## Verification

```bash
# Quick checks of the default construction and preserved state traces
python -m unittest universe24.tests.test_one universe24.tests.test_migration -v

# Complete suite, with package context for relative imports
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v
```

Tests write fresh evidence to ignored `runs/tests/`. Checked-in `universe24/results/` and research notes are historical ONE experiment records, not a declaration that all physical targets passed. Some tests deliberately verify negative findings or failure of a physical hypothesis. A green suite means the stated assertions passed.

See [validation scope](docs/VALIDATION.md), [contribution rules](CONTRIBUTING.md), and [the research proposal](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit).

## Tensor and click audit

See [the audit and measured limitations](docs/CLICK_CONTRACT_AUDIT.md). Export a complete tensor, seed and official event stream, then replay the saved inputs:

```bash
python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
python -m universe24.tools.audit_contract --replay runs/contract
```

All register reads are on-site or at a face neighbor. Including both endpoints of link gears, some terms span two lattice edges; the stricter single-physical-link condition is not satisfied. Official event counts are distinct from signed quotient weights.
