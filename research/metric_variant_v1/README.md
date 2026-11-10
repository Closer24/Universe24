# metric_variant_v1: candidate variant, Stage 0 (core engine)

> **Current status (2026-11-10).** The current version of this package is the **ONE version** (Study 22): one tensor,
> one odd Q, one seed and one run. `one_system()` in [layers/one.py](layers/one.py) composes the package's default
> system, `default_system()` in [layers/system.py](layers/system.py) (hands ON, FIX-i, GRAV-FIX A), with the
> cosmic-clock layer (the WIND hand). By default it is ONE v1, block-diagonal: the hand reads no matter, and no
> package gear reads the hand. The doublet-reads-the-hand coupling (Study 22) was rejected by the owner: matter must
> not read the clock; it also runs away (Study 30); it is kept as an explicit opt-in (`couple_doublet=True`) for the
> record. ONE v1 shows no runaway in what could be run (to t = 9,869 at L = 6), but it is not quiet: E1, β and the
> metric grow slowly, and its uniform lapse has no restoring force and reaches U = −0.186 by t = 9,869: the main OPEN
> stability problem of the default (Study 30); Study 34's clock law CG2 (`one_system_clock`, layers/clockgen.py) is an
> opt-in candidate fix, default OFF and valid only for L ≤ 6; it is not a size-independent law. The other owner
> decisions behind the version: rank 4 is final (rank 5 was studied and rejected in Study 23); bangs do not return to
> the seed: each turn of the cosmic clock starts a new seed, and no information is lost, because Rule3 on one tensor
> is an exact bijection; there is no freeze or hold on the board; light follows route A (E1, with hypercharge global),
> and route B is opt-in and OFF; FIX-i is the hands-ON default. The departures from AGENTS.md now cover items 1, 2, 4,
> 5, 6 and 8, all in declared layers. Start with
> [full_picture_2026-11-10/FULL_PICTURE_FINAL.md](full_picture_2026-11-10/FULL_PICTURE_FINAL.md), the final synthesis
> (Study 36); then [ONE_EXPLAINED.md](ONE_EXPLAINED.md) (the node, the algebra, the clocks, the seed and the tensor),
> [README_v1_draft.md](README_v1_draft.md), the detailed package description, [NOTES_one.md](NOTES_one.md) for the ONE
> version, and [full_picture_2026-11-10/](full_picture_2026-11-10/README.md), beginning with the signed
> THE_ALGEBRA.md. Where the full-picture documents differ from README_v1_draft.md, that README and the code govern.
> The rest of this page describes Stage 0, the core engine, and is kept as history.

This is a **separate candidate variant** of Universe24. It is not the reference model. The reference engine in
[`universe24/`](../../universe24/) is not modified. This package imports it read-only, to build the reference block
and to compare against it. Owner decision OD5 approved the package in SYSTEM_DESIGN_v5 §13. It departs from AGENTS.md
items 1, 2, 5 and 6 only inside this directory: more gear types per node than the one 48-channel board, remainders
in 0..6Q−1, couplings beyond the fixed 2O body actions, and the divisor 6Q in place of 6. The form of the primitive
is kept. Nothing here is a
physical claim. Gear names such as "light" or "gravity" are labels on tensor blocks and on states.

## The definition

**WHOLE SYSTEM = Rule3 + one divisor D = 6Q + ONE tensor T of rank ≤ 4 + the initial state.**

Every gear of every node runs the same primitive. Each input is read from the same complete previous snapshot:

```
u      = T-polynomial of the previous snapshot      (integer)
K      = 2u                                         (even, so the parity of r is a conserved bit)
ell, r' = divmod(K + r, D)                          (D = 6Q, the same for every gear)
a' = b,   b' = ell - a
```

The engine ([`core/engine.py`](core/engine.py)) sees only integer arrays and the tensor's integers. It has no branch
on gear names, readout labels, link metadata or blocks. It contains no table and no notion of light, matter, gravity
or charge.

**Homogeneous form.** With v = (1, b, a), `u_i = T_ijkl v_j v_k v_l`. Each monomial is
`coefficient × (up to three factors)`. A factor is the `b` or the `a` of one gear, at the same node or at one face
neighbour. A monomial with no factor is a constant entry. Rank ≤ 4 means degree ≤ 3, counting the constant 1.

**ONE divisor, read literally.** Every gear of a composed system has the same divisor D = 6Q. No gear type,
layer or block has a divisor of its own. `Engine(tensor, Q)` takes one Q for the whole system.

ONE Q is enforced (stage 0.2, R1):
* every block records the Q it was built with in `Block.Q` (`None` only for blocks without Q-dependent entries);
* `compose` raises when two blocks declare different Q, and the tensor records the common `Tensor.Q`;
* `Engine(tensor, Q)` and `prepare.vacuum_state` raise when a declared Q differs from the one they are given.

The 48 reference channels are not divisor-6 gears that sit beside 6Q gears. They are the Q-scaled 6Q gear, by the
**Q-scaling theorem**: a reference channel runs inside D = 6Q with its entries ×Q and its remainder ×Q, and
`divmod(2Qu + Q r, 6Q) = (ell, Q r')` holds bit for bit. The reference vacuum (0, 0, 2) becomes (0, 0, 2Q). Q = 1
is today's board itself. Tests T0.1 and T0.2 check this for Q = 1, 7 and 50.

## Tensor format (serialisable; this is what the verifier reads)

`Tensor.to_dict()` / `Tensor.from_dict()`, or JSON via `to_json()` / `from_json()`:

```json
{
  "format": "metric_variant_v1/tensor/1",
  "Q": 7,
  "gears": [ {"name": "ref.R00", "label": "official", "link": null, "sign": 1, "sign_why": ""}, ... ],
  "monomials": [
    [target_name, coefficient, [[gear_name, [dx, dy, dz], "b"], ...]],
    ...
  ],
  "designated_one_way": [ [target_name, [[gear_name, [dx, dy, dz], "b"], ...], "justification"], ... ]
}
```

The engine reads only `gears` (their number and order) and `monomials`, and it checks `Q` against its own Q
(`null` means undeclared). `label`, `link`, `sign`, `sign_why` and `designated_one_way` are metadata:

* `label` is for the click readout;
* `link` is the Yee storage axis;
* `sign` and `designated_one_way` are for the reciprocity checker.

`Tensor.dynamics_fingerprint` hashes only what the engine reads. `Tensor.fingerprint` hashes everything.

* `gears` is the unit cell, in order. Every node holds one gear of every type, which gives translation invariance.
  The position in this list is the gear index used by the state arrays.
  * `label` is `"official"` or `"audit"` (OD1). The passive click readout uses it and nothing else does.
  * `link` is `null` for a node gear, or the Yee axis `0/1/2` (+x/+y/+z) for a link gear. A link gear of the link
    (x, x + e_k) is stored at its base node x. This is metadata only.
* A monomial `[t, c, factors]` adds `c × Π factor` to `u_t(x)`, the input of the gear of type `t` at node x. The
  factor `[g, [dx, dy, dz], f]` is field `f` (`"a"` or `"b"`) of the gear of type `g` at node x + (dx, dy, dz).
  * `c` is an arbitrary-precision integer. It is a coefficient of **u**, not of K, because K = 2u.
  * There are at most 3 factors. An empty factor list is a constant.
* **Locality, B3 (enforced; illegal entries raise `LocalityError`).**
  * Each offset must be 0 or one of the six face offsets (±1, 0, 0), (0, ±1, 0), (0, 0, ±1).
  * Every offset of a monomial, together with the target node at 0, must lie in {0, e} for ONE face direction e. So
    a monomial lives on one node or on one face link.
  * Rejected: edge offsets (1,1,0), diagonal offsets (1,1,1), longer offsets (2,0,0), and monomials on three nodes,
    for example factors at +e_x and −e_x.
  * The rule uses storage offsets, with link gears counted at their base node. This is BINDING (manager ruling
    09:08 on X11).
  * The stricter physical-support rule treats a link gear as occupying both ends of its link. By default it is a
    diagnostic, `Tensor.support_violations()`, and a hit is a design fact to report. Examples are the link-field
    stencil across a plaquette and 2-path gears.
  * The strict rule is OPT-IN (stage 0.1): `Tensor(..., strict_support=True)`, `compose(..., strict_support=True)`,
    `build(..., strict_support=True)`, `TensorBuilder.build(strict_support=True)` and
    `Tensor.from_dict(..., strict_support=True)` raise `LocalityError` on such entries.
* **Two-time reads.** A factor with field `"a"` reads the gear's previous `b`.
  * The graph "the `a` of gear g is read by gear t" must be acyclic. A self-read is a cycle. A cyclic graph raises
    `AcyclicityError`.
  * `Tensor.stages` is the staged inverse order. Stage 0 holds the gear types whose input reads no `a`. Stage s holds
    the types that read `a` only from earlier stages.
* **Canonical form**, applied on construction:
  * factors are sorted;
  * monomials with the same target and the same factor multiset are merged, with coefficients added;
  * zero coefficients are dropped;
  * monomials are sorted by (target, degree, factors).

  So two tensors are equal if and only if their canonical dicts are equal. `Tensor.fingerprint` is the sha256 of
  the canonical JSON.
* The divisor is NOT part of the tensor. A system is the pair (tensor, Q): `Engine(tensor, Q)`.

**The reference block.** `reference_block(Q, body_signs=(1,1,1))` reads `ports` and `weights` from
`universe24.core.coupling.Coupling`. No constant is copied by hand. It transcribes the sender form of
`universe24.core.engine.Engine.input_sums` literally:

* the sender gear `g` at x feeds the receiver gear `ports[d][g]` at x + e_d;
* so the receiver's monomial is `[R{ports[d][g]}, Q*weights[d][g], [[R{g}, -e_d, "b"]]]`;
* gear `R{g}` carries the 2O label `g`.

The block has 288 link entries and 0 node entries. A test checks that it equals the receiver form of
`Engine.update_node`. `build(block, ...)` joins blocks into ONE tensor.

## Layer API (contract for the stage-1 builders)

Three separate packages keep AGENTS items 9 and 10 apart:

| package | may contain | must not contain |
|---|---|---|
| `layers/` | tensor blocks only: `build_<layer>(*, Q, couplings..., vacuum remainders..., name=...) -> Block` | state, runs, observation |
| `prepare/` | initial data only: `vacuum_state`, `insert_reference`, `with_gears` | anything that runs the engine or touches a running state |
| `observe/` | read-only observables of determined states: clicks, `gear_field`; `observe.audit.frozen_equivalence` compares two independent runs | anything fed back into a run |

* **Block.** `Block(gears, terms, name=<namespace>, vacuum={local: r0}, params={...}, doc=...)`.
  * Gear names are LOCAL and may not contain a dot.
  * A term is `(target, coeff, factors)`, optionally with a 4th element `{"designated_one_way": "<why>"}`.
  * `params` records the documented parameters the builder was called with: Q, the integer coupling constants and
    the vacuum remainders.
* **compose(*blocks).** Merges the blocks into ONE Tensor.
  * It qualifies every local name as `"<namespace>.<gear>"`, for example `ref.R07`, `em.A_x` or `matter.X3`.
  * Cross-layer terms name gears by their qualified name. Indices are remapped automatically.
  * Gear order is block order, then the order inside each block.
  * A dotted local name, a duplicate namespace and an unknown reference all raise.
  * `build(*blocks)` is the same function, kept for blocks without a namespace.
* **vacuum_map(*blocks).** Returns qualified name → r0. `prepare.vacuum_state(tensor, Q, L, *blocks)` builds the
  vacuum state. Each new layer is written in deviation form: its vacuum gear is (0, 0, r0), and every term that
  targets it vanishes when the layer's own gears are 0. The vacuum is then the reference board bit for bit (T0.6).
* **Reference layer.** `layers.build_reference(*, Q=1, body_signs=(1,1,1), name="ref", label="official")`.
* **Reciprocity: force blocks must be gradients.** `core.reciprocity.check_reciprocity(tensor)` checks that the
  b-only part (degree ≥ 1, every factor b) satisfies `u_t = s_t · ∂Φ/∂b_t` for ONE translation-invariant integer
  potential Φ.
  * `s_t` is the documented field sign, `GearType.sign`, default +1.
  * Equivalently, S·J is symmetric: action equals reaction.
  * The checker groups the monomials by their potential monomial (modulo translation) and demands every partner
    with the exact coefficient (exact Fractions).
  * Terms marked `designated_one_way: <justification>` are excluded and listed.
  * The check FAILS if any undesignated non-reciprocal b-only monomial remains. `report.violations` lists them and
    `report.missing_partners` names the absent partners.
  * Constants and terms with an `a` factor (two-time reads) are counted but not checked.
  * The reference block passes for all 8 body-sign choices (T0.8).
  * Field sign −1 needs a reason (R2). `GearType(..., sign=-1)` raises unless `sign_why="<justification>"` is given.
    The report lists every s = −1 gear with its justification in `report.negative_sign_gears`. Per S4-M2, all signs
    can be +1 under the first-order inversion, so each −1 must be explained.
* **LINKS FROZEN (G9-c hook).** A layer that couples to the reference board through link gears takes its link
  couplings as keyword parameters, for example `kappa`, `lam` and `beta`.
  * With all of them set to 0, the composed run must equal today's board exactly, and the link gears must stay at
    their vacuum.
  * `observe.audit.frozen_equivalence(base_blocks, extra_blocks, Q, base_state, steps)` is the check. It reports
    base-sector mismatches and extra-gear deviations, and `frozen` is True iff both are 0.
  * T0.10 checks a test stub of rank-3 link hopping: with kappa = 0 it is frozen; with kappa = 1, the control,
    the difference is detected.

## State format

`State(L, a, b, r)` holds integer arrays of shape (G, L³) in gear-type order.

* The flat node index is n = (x·L + y)·L + z, so `reshape(G, L, L, L)` gives `[gear, x, y, z]`.
* Remainders must satisfy 0 ≤ r < D.
* The arrays are numpy int64 while every |value| < 2^62. Otherwise they are numpy object arrays of Python ints.
* `State.to_dict()` gives `{"L", "a", "b", "r"}` as nested lists of ints.
* Directions use universe24's order: +x, −x, +y, −y, +z, −z.

## Exactness

There is no floating point anywhere. Before each step the engine computes an exact Python-int bound on |K + r|. It
works from per-gear maxima of |a| and |b| and the absolute coefficients, and the bound also covers every partial
product and partial sum. If 2·bound + 2D < 2^62, the step runs in vectorised int64. Otherwise the same code runs on
Python ints in object arrays, and the engine returns to int64 when the values are small again. `Engine.stats` counts
the two paths. The staged inverse decides the same way, stage by stage.

Maxima are computed exactly as `max(int(x.max()), -int(x.min()))`, never with `np.abs` on int64, because
`np.abs(int64(-2^63))` is -2^63. B0-VERIFY found this bug (X7); stage 0.1 fixed it, and T0.11 tests it. Plain-list
input is read as Python ints and is never float-inferred.

## Audit maps and the passive readout

These are never stages of the forward evolution.

* `Engine.inverse_step` is the staged exact inverse. It sets old b = new a. Then, stage by stage, it computes
  `r = (r' − K) mod D`, `ell = (K + r − r')/D` and `old a = ell − b'`.
* `Engine.mirror` applies M(a, b, r) = (b, a, D − 1 − r) to every gear. For b-only tensors, M F M = F⁻¹. M flips the
  parity of r. The other reversors and symmetries (M′ = universe24 `time_reverse` for D = 6, J, JR, spatial
  inversions, group maps) are in `core/reversors.py` (stage 0.2).
* `Engine.clicks(before, after, step, stream)` reads two snapshots. It never touches the state.
  * **OFFICIAL clicks (`stream="official"`, the default).** The rule is exactly universe24's
    `observation.clicks.classify`: a click is an update with `quotient = after.b + before.a ≠ 0` **and** a changed
    triple (a, b, r).
    * A gear whose triple did not change is not a click, even when ell ≠ 0. Example: a = b = 1, ell = 2, r' = r.
  * **kind.** Take δ = (r' − r) mod D in (−D/2, D/2]. The kind is C0 if δ ∈ {0, D/2}, C1 if 0 < δ < D/2, and C2 if
    −D/2 < δ < 0. This is the handedness of CLICK_TAXONOMY §1.
    * For D = 6 it equals universe24's `((r' − r)//2) mod 3`.
    * For Q-scaled reference gears it gives the same kinds as the Q = 1 run.
  * **Columns.** Each row has the gear type, the node, kind (0/1/2), quotient, `changed`, and the gear's readout
    label (`official`/`audit`, OD1). Rows are sorted by (x, y, z, gear), as in universe24.
    `ClickLog.select("official")` keeps the rows of official-label gears.
  * **RAW stream (`stream="raw"`): NON-OFFICIAL.** It holds every gear with ell ≠ 0, including unchanged triples,
    with the `changed` flag. Use it for audit only.

## Reversor building blocks (stage 0.2, `core/reversors.py`)

These are audit maps on complete states. They are never stages of the forward evolution. Which map acts on which
gear is DATA, and every map is exact integer arithmetic. `X @ Y` composes two maps, X∘Y with Y applied first.

**(a) Per-gear maps.** D = 6Q. `R'(r)` is D−2−r for even r and D−r for odd r.

| name | map | role |
|---|---|---|
| `M` | (b, a, D−1−r) | time mirror; flips r mod 2; reversor of every b-only tensor |
| `Mp` (M′) | (b, a, R′(r)) | parity-preserving; for D = 6 it equals universe24 `time_reverse` |
| `J` | (−a, −b, D−1−r) | negation; a symmetry of odd tensors |
| `JR` | J∘M′ = (−b, −a, r xor 1) | the manager's definition |
| `JM` | J∘M = (−b, −a, r) | CLICK_TAXONOMY's "JR" |
| `Jp` | (−a, −b, R′(r)) | CLICK_TAXONOMY's parity-preserving J_D |

| `rhoL0` | (b, a, ρ(r)), ρ(r) = 4Q + 2(r mod 2Q) − r | the Q-scaled universe24 `time_reverse`, for the L0 (reference) gears |

Use `GearwiseMap(tensor, Q, {gear: name}, default="id")` to choose a map per gear, or `uniform(tensor, Q, name)` to
use one map everywhere. On the reference sector, M and M′ keep click kinds. JR and JM swap C1 ↔ C2 and negate
quotients (T0.13).

**Choosing a mirror for L0 and for new layers (R-M2 theorem).**
* For an L0 (reference) gear, (b, a, ρ(r)) is an exact time mirror iff its K = 2u ≡ 0 (mod 2Q). That holds when
  every term targeting it has a u-coefficient ≡ 0 (mod Q). ρ fixes the L0 vacuum 2Q.
* R′ fixes the new layers' vacuum 3Q−1 (for odd Q) but sends 2Q to 4Q−2.
* So the joint mirror is "rhoL0" on L0 gears and "Mp" on the new b-only layers. It is exact and fixes the joint
  vacuum (T0.15).
* The validator `compose(..., q_lattice=("ref.*",))` raises if a term targeting a matching gear breaks the mod-Q
  rule. `Tensor.q_lattice_violations(patterns)` lists such terms. With the rule satisfied, L0 remainders that start
  on the Q-lattice stay on it.

**(b) Group linear maps.** `GroupLinearMap(tensor, Q, gears, matrix, r_rule=None, neg_r="M")` applies an integer
matrix to the (a, b) vectors of a gear group at every node. Link gears are stored at nodes, so a link's gear block is
a group like any other.
* Remainders: target i takes `rmap(r[source])`, given by `r_rule[i] = (source, "id"|"M"|"Mp")`.
* For a signed permutation, `r_rule` can be left out. A +1 entry copies r. A −1 entry applies `neg_r`.
* Layers compose staggered or Kramers-type maps from these with `@`, for example K∘M with K = [[0,−1],[1,0]].

**(c) Spatial maps.** `inversion_about_node(tensor, x0)` uses S = 2x0. `inversion_about_cube_centre(tensor, x0)`
uses S = 2x0 + (1,1,1). `inversion_about_box_centre(tensor, L)` and `identity_map(tensor)` are also provided.
* A node gear moves x → S − x.
* A link gear of axis k moves from base x to base S − x − e_k, because the link (x, x+e) maps to (S−x−e, S−x).
* Values are moved, never changed. Signs of oriented quantities are layer data, applied by composing with (b).
* Storage-legal entries whose physical support exceeds one link do not stay storage-legal under inversion.
  Inversion-symmetric layers should therefore build on physically link-local entries (T0.12 flag).
* The +++ reference board commutes with inversion composed with a channel relabeling σ, where
  σ(ports[d][h]) = ports[d^1][σ(h)]. A search over universe24's own ports finds 8 such σ for +++ (a Q8 coset) and 0
  for (1,1,−1). Plain inversion does not commute.

**(d) Reversor check.** `reversor_check(X, F, states, n, central=[(name, Z), ...])` evaluates X F^n X F^n (s). It
counts the result as identity, as a declared central map Z (for example J, when (K∘M)² = J), or as a failure.

**(e) Fixed points.** `is_fixed(X, state)`.

## Files

| file | content |
|---|---|
| `core/lattice.py` | periodic L³ indexing, the six face directions, gather maps, Yee link helpers |
| `core/tensor.py` | `GearType`, `Factor`, `Monomial`, `Tensor` (validation, B3, a-read stages, canonical form, JSON), `TensorBuilder`, `reference_block`, `build` |
| `core/engine.py` | `State`, `Engine` (step, run, inverse_step, rewind, mirror, vacuum, inputs, clicks), `ClickLog`, `handedness_kind` |
| `core/bridge.py` | read-only conversion between universe24 `State` and dense arrays, with r ×Q |
| `core/reciprocity.py` | `check_reciprocity` (gradient-of-one-potential check with field signs and one-way designations) |
| `layers/__init__.py`, `layers/reference.py` | the layer contract; `build_reference` |
| `prepare/__init__.py` | initial-data helpers (`vacuum_state`, `insert_reference`, `with_gears`) |
| `observe/__init__.py`, `observe/audit.py` | read-only observables (clicks, `gear_field`); `frozen_equivalence` |
| `tests/test_core.py` | acceptance tests T0.1–T0.7; each writes `results/<test>.json` |
| `tests/test_layers.py` | T0.8 reciprocity checker, T0.9 compose/namespaces, T0.10 links-frozen hook |
| `tests/test_stage01.py` | T0.11 int64 extremes against a pure-Python oracle; T0.12 opt-in strict physical support |
| `core/reversors.py` | stage 0.2: per-gear maps (M, M′, J, JR, JM, Jp), group linear maps, spatial inversions with link re-basing, `reversor_check`, `is_fixed` |
| `tests/test_stage02.py` | T0.13 reversor building blocks |
| `tests/test_stage02_review.py` | T0.14 ONE Q and field-sign justifications (R1, R2); T0.15 ρ_L0 and the Q-lattice validator |
| `tests/randgen.py` | seeded random B3-local tensors and states (test data only) |
| `tools/export_fixtures.py` | writes tensor + initial state + final state fixtures (JSON) for independent cross-checks |
| `NOTES.md` | pre-registrations and results, with `date -u` stamps |

## How to run

From the repository root (numpy is required):

```bash
OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_core research.metric_variant_v1.tests.test_layers research.metric_variant_v1.tests.test_stage01 research.metric_variant_v1.tests.test_stage02 research.metric_variant_v1.tests.test_stage02_review -v
python research/metric_variant_v1/tools/export_fixtures.py      # optional: fixtures for the verifier
```

The suite runs in well under a minute on 2 cores. T0.1 compares against universe24's own `Engine.advance`,
`Engine.rewind` and `observation.clicks`. T0.7 prints its throughput.

## Caveats

* This is a candidate variant: a generic engine and data. No physics block (gravity, EM, matter, links) is built
  in Stage 0.
* The `official`/`audit` label is a readout decision (OD1), not a law.
* Name clash: here **Q is the divisor scale** (D = 6Q), as in the design documents. It is unrelated to the signed
  algebraic account that AGENTS.md item 12 calls `Q`. Nothing here identifies any account with energy.
* B3 is enforced on storage offsets, which is binding. `Tensor.support_violations()` reports entries whose
  physical support, with link gears spanning their link, exceeds one link. `strict_support=True` turns that report
  into a rejection.
* The engine does not enforce reciprocity, because it is exact and reversible without it. Reciprocity is a design
  rule for force blocks, checked by `core.reciprocity` before a block is adopted.
