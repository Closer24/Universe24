# Candidate couplings (explicitly separate variant)

This package lets a study choose a **different fixed coupling tensor before a
run**. The reference engine in [`universe24/`](../../universe24/) and its eight
sign triples stay the default and are not modified. After t = 0 the coupling is
constant, and every channel is updated by the reference Rule3 primitive. That
primitive is imported from [`universe24/core/rule3.py`](../../universe24/core/rule3.py),
and every update reads the same complete previous snapshot. There are no
runtime hooks, observers in the loop, gates or injections.

A table other than the eight reference tables is a **candidate variant** in the
sense of [AGENTS.md](../../AGENTS.md). It is not the reference model and has no
established physical meaning. Every result obtained with it must quote its
`label` and full `fingerprint` beside the corresponding reference result.

## What is fixed and what is chosen

Fixed, as in the reference engine:
* one board of 48 channels labelled by 2O on the periodic cube `L >= 3`;
* exactly six spatial ports per channel, one per face neighbour, and no on-site term;
* the per-channel law `ell, r' = divmod(2u + r, 6)`, `a' = b`, `b' = ell - a`;
* exact integers, the complete retained state, and an exact inverse.

Chosen once, before the run: one `VariantCoupling` and the initial data.

## The validated family

`VariantCoupling(name, ports, weights)` holds `ports[d][g]` and `weights[d][g]`
for the directions `(+x,-x,+y,-y,+z,-z)`. These have the meaning of
`Coupling.ports` and `Coupling.weights`: sender `(x,g)` adds `weights[d][g]*b`
to receiver `(x+e_d, ports[d][g])`. Validation requires the following.

| Rule | Check |
| --- | --- |
| Six signed ports | every `ports[d]` is a permutation of 0..47; every weight is `+1` or `-1` |
| Reciprocity (as `Coupling.validate`) | `ports[d^1][ports[d][g]] == g`, with an equal weight |
| 2O covariance (the owner's constraint) | `ports[R(h)d][h*g] == h*ports[d][g]`, with an equal weight, for all 48 `h` |

A zero weight would delete a port, and a larger magnitude would rescale
Rule3's input. Neither is allowed in this version.

Covariance is equivalent to the 2O body-action form of the reference
construction: `ports[d][g] = g*B_u` and `weights[d][g] = w_u`, with
`u = R(g)^-1 d`. A table is therefore fixed by its identity column,
`B_u = ports[u][e]` and `w_u = weights[u][e]` (`body_actions`, `body_weights`).

Reciprocity then pairs each body direction `u` with
`v = -R(B_u)^-1 u`. It requires `v != u`, `B_v = B_u^-1` and `w_v = w_u`
(`pairs`). For each pair there are 4 rotations, 2 lifts and 2 signs; the two
lifts differ by the central element `z`.

**[EXHAUSTIVE]** The family `covariant_family()` therefore has 15 pairings ×
16³ = **61,440** labelled tables. All of them are distinct and pass full
validation (`python -m research.coupling_variants_v1.audit --family`).

* The axial pairing {±x}, {±y}, {±z} gives the 4,096 tables of
  [docs/COUPLING_FAMILIES.md](../../docs/COUPLING_FAMILIES.md).
* Its member `m = (0,1,3)` gives the eight reference tables.
* The other 14 pairings answer a port through a perpendicular body direction.

These counts are of labelled tables, not of inequivalent models.

**[THEOREM + test] Character gauge.** 2O has one nontrivial one-dimensional
character `χ`, which is `-1` outside the commutator subgroup 2T. The map `J` on
the 24 channels with `χ(g) = -1` conjugates a coupling with body weights `w_u`
to the coupling with body weights `χ(B_u)·w_u` (`chi_gauged`,
`gauge.chi_gauge_state`). This holds on every side `L`, for backgrounds
`r ∈ {2,3}`. For the reference tables it sends `(sx,sy,sz)` to `(sx,-sy,-sz)`,
the gauge that r03 and r05 of the matter/light program used. On an even side,
`J` on every channel of the odd-parity sites likewise conjugates `w_u` to
`-w_u` (`gauge.staggered_state`). Such pairs give no new dynamics.

## Constructors (all inside the algebra)

```python
from research.coupling_variants_v1 import VariantCoupling, VariantEngine, covariant_family

VariantCoupling.reference((1, -1, 1))                  # a reference table (label reference:+-+)
VariantCoupling.axial("axial-017", m=(0, 1, 7))        # other body actions in place of (0,1,3)
VariantCoupling.from_body_actions("c1", actions, w)    # any family member: six 2O labels, six signs
base = VariantCoupling.reference((1, 1, 1))
base.with_body_weights("signs-1", (1, 1, -1, -1, 1, 1))  # another sign pattern
base.z_twisted("twist-x", (1, 1, 0, 0, 0, 0))            # B_u -> B_u*z on both members of a pair
base.chi_gauged("gauge")                                 # the character-gauge image
for actions, weights in covariant_family(): ...          # enumerate all 61,440
```

Under covariance the weights are functions of the body direction only.
"Group-derived weights" therefore means a choice of `w_u` per pair, or `χ(B_u)`
via `chi_gauged`. An explicit table is accepted only if it passes all checks.
The optional `construction` record is re-derived and must match the tables.

## Labels and identity

* `fingerprint`: SHA-256 of the tables, tagged `universe24-variant-coupling-v1`.
  The name is not part of it.
* `label`: `reference:+-+` if the tables equal a reference table, otherwise
  `variant:<name>@<fingerprint[:12]>`.
* `reference_signs` and `reference_fingerprint`: the matching reference
  triple and its engine fingerprint, or `None`.

## Executor and band analysis

`VariantEngine(coupling)` provides `input_sums`, `advance`, `rewind` (the exact
inverse, for audit only) and `evolve`, with the same sparse-state semantics as
`Engine`. The read-only diagnostics in `universe24.observation`
(`balance_residuals`, `signed_account`, `expected_account_change`, `clicks`)
accept it unchanged. `Q` remains a signed algebraic account, not energy.

`coupling.matrix(d)` is the signed matrix `P[d][g][h]` (receiver `g`, sender
channel `h` at `x+e_d`). `coupling.bloch_matrix(k)` is
`A(k) = Σ_d exp(i k·e_d) P[d]`, Hermitian by reciprocity: a plane wave
`b(x,h) = c_h exp(i k·x)` receives `exp(i k·x)(A(k)c)_g`. In the
large-amplitude regime an eigenvalue `λ` gives `cos ω ≈ λ/6`. For `+++` the
matrix reproduces r02's spinor-sector maximum `λ = 5.0355` near
`k = 0.494(1,1,1)`. Eigen-solvers are left to the study (the package uses
only the standard library).

## Init files and the runner

A variant init file is the official init format plus the complete coupling:

```json
{
 "format": "universe24-variant-init-v1",
 "side": 9, "background": [0,0,2], "steps": 12,
 "coupling": {"format": "universe24-variant-coupling-v1", "name": "axial-m017-ppp",
              "construction": {"kind":"axial","m":[0,1,7],"signs":[1,1,1]},
              "fingerprint": "fc4d2d79…", "ports": [[48 ints] x 6], "weights": [[48 ints] x 6]},
 "seed_changes": [{"position":[4,4,4],"channel":0,"state":[0,2,2]}]
}
```

`load` parses the cube and cells with the official `universe24.experiments.from_dict`.
It rebuilds and validates the coupling and requires the recorded fingerprint.
The reference loader rejects these files, so a variant cannot run as a
reference experiment by mistake. `write_init` never overwrites and
reload-checks. See [`examples/`](examples/): the impulse with the `+++` table,
and with the axial `m=(0,1,7)` variant (a format example, no claim).

```sh
python -m research.coupling_variants_v1 --config research/coupling_variants_v1/examples/impulse_axial_m017.json \
    --events runs/axial.jsonl --summary runs/axial.summary.json --audit
```

The runner mirrors `python -m universe24`. Its event log is the official
passive JSONL, so a click decoder reads it unchanged. The summary records
`model` (`variant` or `reference-equivalent`), `coupling_label`, both
fingerprints and the executor. Keep the summary beside every log.
`--output` and `--resume` use `universe24-variant-checkpoint-v1`.

## Evidence

* `tests/test_coupling_variants_v1.py` (13 tests, about 4 s) covers:
  * reference tables and labels;
  * bit-for-bit equality with `Engine` on random states, including `10^30`
    counters, for all eight triples;
  * validator rejections and the family counts;
  * the constructors, and character-gauge and staggered-gauge conjugacy;
  * the exact inverse and balance identities for random family members;
  * scatter versus an independent dense gather;
  * Bloch conventions against the engine's impulse responses;
  * init files and runner output, byte-identical to the official CLI;
  * imports (`universe24` and the standard library only).
* `python -m research.coupling_variants_v1.audit` covers 350 recorded cases:
  the three engine examples and the 347 reference-coupling blocks of
  [matter_light_blocks_v1](../matter_light_blocks_v1/README.md) (a variant block
  has no reference Engine to be compared with and is skipped).
  * All eight triples are covered.
  * Every complete state is compared with `Engine` at every update.
  * The variant inverse is checked at every update.
  * Each final state hash is compared with the catalog.
  * Result: 17,385 transitions, 0 differences.

## Per-site tensors are not supported

**[THEOREM + check]** Suppose every site carries its own covariant table and
every bond is reciprocal. Then one bond already fixes the neighbour's table:
`B'_{v} = B_u^-1` and `w'_v = w_u`, with `v = -R(B_u)^-1 u`, for all six
`u`. This is because `R(g)^-1 d` meets every body direction as `g` runs over
2O. The resulting map `T` is an involution.

A connected board therefore carries at most two tables, `D` and `T(D)`, on
the two parity sublattices; on odd `L` it carries one table. Two different
sign triples can never be neighbours. For example, `+++` next to `+-+` fails
reciprocity on every bond direction.

A "coupling patch" between blocks of different triples would therefore break
either covariance or reciprocity at the interface. That is outside the owner's
constraint, so it is not implemented. The exact inverse alone would survive,
because it needs only a fixed input map of the old `b`
(docs/COUPLING_FAMILIES.md). What would be lost is `P[-d] = P[d]^T`, the
symmetric operator `A` and the scatter/gather equivalence.

Blocks with different triples can share a board only by transporting a
preparation through an exact gauge into the common triple (data only). Two
cases are known:
* the character gauge, for `(sx,sy,sz) ~ (sx,-sy,-sz)`;
* the staggered sign gauge on even `L`, for `w_u ~ -w_u`.

Otherwise they need separate boards. A two-sublattice tensor `(D, T(D))` with
`D != T(D)` exists for even `L`. It would be a separate, explicitly reviewed
extension.

## Limits

* One table on the whole board (translation invariant), 48 channels, unit weights.
* A variant result is a statement about that variant only. No variant is
  claimed to be physically preferred, Lorentz-invariant or reference-equivalent
  unless its label says `reference:`.
