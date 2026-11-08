# Universe24 development contract

This file governs automated and human contributions to the **reference** Universe24 implementation. Do not silently alter its mathematics.

## Fixed model
1. One elementary node per spatial site and **one board** with 48 channels indexed by `2O`.
2. Every channel stores exactly two arbitrary-precision integer counters `a,b` and the retained remainder `r in {0,...,5}`.
3. Spatial geometry is the periodic cube `(Z/LZ)^3`, specified by **one side length** `L >= 3`.
4. Each channel receives **exactly six spatial inputs**, one from each face neighbor. Zero entries in signed matrices do not delete ports.
5. Coupling is constructed from the fixed 2O body actions `(0,1,3)` and three preselected body-axis signs in `{-1,+1}`. It remains constant during the run.
6. **Sole forward primitive:** `ell,r_next = divmod(2*u + r,6)`, `a_next=b`, `b_next=ell-a`.
7. Every next state is computed only from the **same complete previous snapshot**.
8. There is no state-changing detector/click/veto/selector code, no extra gates or clock, no internal on-site links, no second board, no erased remainder or hidden numerical state.
9. `experiments/` may only create initial preparations and serialize full-state checkpoints. No intervention after the run starts.
10. `observation/` may only read already determined states and compute derived diagnostics. `C2` is an arithmetic class, **not** a proven physical selection law.
11. `inverse` and `rewind` exist for audit and recovery; they are not stages in forward evolution.
12. The signed algebraic account `Q` is not established physical energy; do not equate them.

## Allowed changes
Tests, documentation, optimization preserving exact state traces, optional read-only observables, data-only preparations and explicitly separate candidate variants. Any optimization must show equality on *all* retained state components for declared test regimes.

## Verification

First complete the dependency and evidence setup in
[full research validation](docs/QUICKSTART.md#full-research-validation).
The core itself uses only the standard library; the full research suite does not.
```bash
python -m unittest discover -s tests -v
python -m universe24 --config examples/impulse.json --audit
python -m universe24 --config examples/signed_impulse.json --audit
```

For full model, schema, caveats, and review requirements see [docs/MODEL.md](docs/MODEL.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and [CONTRIBUTING.md](CONTRIBUTING.md).
