# Universe24 ONE development contract

ONE is the sole active runtime. The default is `universe24.layers.one.one_system()`.

1. Preserve the exact scalar recurrence `ell,r_next = divmod(2*u+r,D); a_next=b; b_next=ell-a`, with one common positive integer `Q` and `D=6Q`.
2. All forward outputs read the same complete old snapshot. Never insert runtime injections, vetoes, branch selectors, detector callbacks, or unrecorded state.
3. The fixed integer polynomial tensor has input degree at most three. Every monomial is supported on the target node and at most one face neighbor. Cycles in old-`a` dependencies are rejected so staged inversion is valid.
4. `layers/` constructs the law before a run; `prepare/` constructs initial data; `observe/` reads snapshots. Keep these roles separate.
5. Use arbitrary-precision integers when the validated int64 bounds fail. Never introduce float arithmetic into the fundamental state update.
6. Preserve complete `(a,b,r)` traces when refactoring. The default tensor census, fingerprint and migration fixtures are regression contracts, not proof of physical correctness.
7. Cube and `2O` algebra belongs in `algebra/`. The 48-gear L0 block is part of ONE, not a second runtime. The test-only Q=1 oracle must stay independent of `Engine.step` and must never be imported by production code.
8. Keep rejected and optional constructions clearly marked and off by default. Do not promote them by changing README language alone.
9. Distinguish mathematical identities, numerical evidence and physical hypotheses. Reversibility is not boundedness, physical energy conservation, time-reversal symmetry or a Born-rule derivation.
10. Put new run output under `runs/`. Preserve checked-in historical evidence unless explicitly regenerating it with recorded provenance.

Run the quick suite and appropriate affected checks. For a structural migration or change to the common engine, run the complete suite and the CLI forward/rewind smoke run from README. Review the diff before publishing. Update the algebra whenever the law or construction changes.
