# Exact sourced evolution with a complete native history

This is the construction tracked in [issue #58](https://github.com/Closer24/Universe24/issues/58),
following the complete-state proof obligations of #57 and the central #56 integration.
The starting integration commit is `f4f64e062f07b3ca119eccf655df746be206908b`.

The positive construction addresses a **spatially flat, homogeneous, isotropic,
expanding universe with a massless scalar and pressureless dust**. It changes
the retained coordinates and the research tensor. It is not an exact rewrite
of the failing massive45 discrete trajectory, and it does not implement the
massive scalar, spatial interactions, apparatus or general Einstein dynamics.

## The physical coordinate change

In the repository's convention, the inverse spatial frame is `B`, the diagonal
extrinsic-curvature variable is `k`, scalar velocity is `p`, and dust density
is `d²`. Proper time has unit lapse. Introduce

\[
V=B^{-3},\quad U=-3kV,\quad P=pV,\quad D=d^2V.
\]

For zero scalar mass, the constraint is

\[
Q=U^2-3DV-\tfrac32P^2=0.
\]

On this constraint surface, the sourced equations reduce to

\[
\dot V=U,\qquad \dot U=\tfrac32D,\qquad \dot P=\dot D=0.
\]

Thus the exact proper-time step of size `h` is

\[
V'=V+hU+\tfrac34Dh^2,\qquad U'=U+\tfrac32Dh.
\]

Direct expansion gives `Q'=Q`. The reverse step is obtained by replacing `h`
with `-h`; physical validity additionally requires staying on the same positive-
volume branch. The native integer dynamics can remain invertible beyond a
physical singularity, which is not a continuation of this physical solution.

The scalar is not discarded: its momentum `P` and a retained integration
constant determine its evolving value through an explicit passive logarithmic
coordinate map. The scale factor and dust amplitude use passive real roots.
These are full-state diagnostics, not the canonical arithmetic click decoder
or a retained operational clock. No diagnostic feeds the Engine.

## The native history is the missing momentum

For `h=1/N`, retain `W=4N²V` and infer `J=4NU` from **both** volume histories:

\[
J=b_W-a_W+3D.
\]

The fixed input `u_W=6b_W+18D` gives, with every legal carry retained,

\[
W'=W+J+3D,\qquad J'=J+6D.
\]

The integer constraint

\[
I=J^2-12DW-24N^2P^2
\]

is therefore preserved exactly. This is a constraint of the complete native
history, rather than a constraint separately imposed on each time slice.
The original first-step and cross-history failure controls remain valid for
their original tensors.

Six channels retain volume, dust charge, scalar charge, reference velocity,
scalar offset and a proper-time coordinate counter. Every channel keeps all
three integers `(a,b,r)`. The time counter is a coordinate label; it does not
establish a material clock. The changing volume comes from the Engine's
retained volume histories and source, not from looking up a precomputed
trajectory at that counter.

## Evidence and boundaries

| Work package | Executed proof or check |
| --- | --- |
| [Physical map](01_physical_map.md) | Exact flow, scalar phase, stress balance and all Einstein components |
| [Integer chart](02_projective.md) | Exact scaling, history-to-velocity bijection and integer invariant |
| [Native implementation](03_native.md) | Actual Engine, all carry classes, scalar oracle, source removal and rewind |
| [Massive alternatives](04_variational.md) | Correct massive equations and explicit failures of candidate integrators |
| [Independent physical oracle](05_oracle.md) | Original field equations, source interventions and same-time resolution comparisons |
| [Domain and bit cost](06_domain.md) | Entire physical intervals, singularity controls and logarithmic bit bound |
| [Runtime integration](07_runtime.md) | Verified saved bundles, canonical clicks and declared full-state observations |
| [Independent review](08_review.md) | Metric derivation, adversarial native/readout/runtime controls and fixes |

The native audit includes eleven cases and 26,244 scalar integer comparisons.
The independent oracle executes twelve source/resolution runs, including
stronger scalar and dust sources. At proper time `1/8`, the main case reaches
exactly `V=355/256` and `U=51/16` for `N=24,48,96`. These are exact samples of
the restricted flow; no infinite convergence order is inferred. Independent
high-precision integration of the original physical equations supplies an
additional numerical comparison. Counts in joined audits overlap and must not
be summed as independent experiments.

The time counter is not consulted to reconstruct the physical fields. The
decoder reads the current volume, its previous history, retained source charges
and phase anchors. Numerical root/log evaluation is explicitly distinguished
from the exact rational identities. Review found and fixed loss of precision
in scalar reconstruction near the branch boundary and a runtime reader's
assumption that every valid time counter starts at zero.

The accepted initial-data chart must be stated explicitly: finite integer
charges and exactly representable rational volume/velocity are not every real
FLRW initial datum. The expanding mixed-source branch is the initial target;
pure scalar and other singular coordinate limits need separate encodings.

For nonzero mass, `P` ceases to be constant and the volume acceleration depends
on the scalar potential. Relabelling this tensor as massive cannot repair that.
The massive-method audit supplies explicit positive identities and rejection
controls, rather than transferring this restricted success to that problem.

No production Engine, public runtime, canonical decoder, default tensor or
general physical acceptance gate is changed by this source-only package.

## Reproduce

```bash
python -m validation.sourced_map.run_all
python -m unittest discover -s universe24/tests -t .
python -m validation.system_smoke --out runs/sourced-map/recheck-smoke
python -m universe24 verify --run runs/sourced-map/recheck-smoke/run
```

Use a fresh smoke output directory for each run. The eight-audit collector
records exact source and evidence hashes in `runs/sourced-map/collection.json`.
Large complete traces are archived as deterministic `.json.gz` files; the
collector records both raw and archived hashes, and each audit regenerates its
plain JSON. The runtime audit uses fresh saved-run directories and reports the
five exact directories to inspect. See [VALIDATION.md](VALIDATION.md) for the
final execution ledger.

The underlying stiff-matter/dust cosmology is a known exact solution; see
[Chavanis, section V.B, equation 39](https://arxiv.org/pdf/1412.0743).
The contribution here is its explicit complete-history integer encoding,
source-bound runtime evidence and the boundaries for extending it.
