# Universe24 fixed-divisor development contract

The default `python -m universe24` constructs Einstein ADM, complex scalar matter and dark dust through `universe24.layers.adm`. It uses the unchanged fixed-six Rule3 Engine. The 48-channel reference baseline is explicitly selected through `universe24.layers.reference_model.reference_system()`.

1. Preserve exactly `ell,r_next = divmod(2*u+r,6); a_next=b; b_next=ell-a`. The divisor is fixed at six. Do not add a divisor-scale parameter, per-gear divisor, or hidden normalization to this recurrence. Physical rational readouts may use two ordinary retained integer registers only through the proved finite-horizon arithmetic construction in docs/INTEGER_ADM.md; this never changes an Engine denominator.
2. Every forward output reads the same complete old snapshot. Never insert runtime injections, vetoes, branch selectors, detector callbacks, or unrecorded state.
3. The fixed integer polynomial tensor has input degree at most three. Every monomial is supported on the target node and at most one face neighbor, including the endpoints of physical link gears. Old-`a` dependencies must be acyclic for staged inversion.
4. `layers/` constructs fixed law data before a run; `prepare/` constructs complete initial data; `observe/` reads snapshots. Keep these responsibilities separate.
5. Use arbitrary-precision integers when validated int64 bounds fail. No floating arithmetic in fundamental states, input evaluation or evolution.
6. Preserve complete `(a,b,r)` histories for behavior-preserving refactors. A changed tensor, seed law or divisor convention is a model change: update its algebra and evidence, and do not claim equivalence to superseded runs.
7. Cube and `2O` algebra belongs in `algebra/`. The 48-channel reference block is a construction within the same engine. The independent scalar oracle stays test-only and must not call production `Engine.step` to produce its expected result.
8. Keep optional or rejected constructions explicitly separate from the default. A retired variable-divisor construction must fail clearly or be removed from the active API, not silently rerun with changed coefficients.
9. Distinguish identities, numerical evidence and physical hypotheses. Reversibility is not boundedness, energy conservation, universal clock behavior, a Born-rule derivation or Einstein dynamics.
10. Put fresh runs under `runs/`. Do not relabel historical evidence as current. Regenerated evidence needs source provenance and a stated comparison with the previous construction.

Run the quick suite and appropriate affected checks. For common-engine or
structural migrations, run the full discovery and the CLI forward/rewind smoke
run documented in README. Review the diff and update the mathematical contract
before publishing. Effective `num/den` families remain hypotheses until an
explicit invariant or retimed encoding is proved.
