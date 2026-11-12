# Central source integration

One supported runtime executes immutable prepared bundles through fixed Rule3.
The one saved-run geodesic board is produced with:

```bash
python -m validation.geodesic_board --out runs/geodesic-board
python -m universe24 verify --run runs/geodesic-board/runtime
```

Open `runs/geodesic-board/board.html`. Its trajectories are passive geodesics of
the reconstructed homogeneous metric. They are not measured material packets.
Source integration does not grant a physical certificate or change a default.

## Exact source ledger

| Source | Exact imported head | Role |
| --- | --- | --- |
| #51 | `ff21c878cc2e6e9d0969c3538e0c676fcdab616f` | Shared massive45 saved run and board; merged on main at `b10af568ec98cbca07524f915ca15f9e0a8b438d` |
| #52 | `8c53e69f4b466dcbd2da7dab7e3c365bd9731766` | Nine completion audits, native compiler, temporal counterexamples |
| #53 | `73b24b788d5d3aa3c969a08ca5af16bfe532c4a4` | Node algebra, common clock/cone controls, load invariance |
| #55 | `f83924d69367641751ee4815cefaf97996748774` | Guarded exact45→6 sector, native identities and saved full-state/click reconstruction |
| #54 | `d4f281c0839887ac7af8c050c406b2081f7c9baf` | Reciprocal homogeneous apparatus47, record48 and preparation-measure controls |
| #57 | `a3140de58c5359d0d0ab074eab1f6d1fa277aefb` | Interaction-to-native composition, complete-state certificates and scoped packet controls |

The new cross-team gate runs in normal unittest discovery and CI:

```bash
python -m validation.integration_contract.massive45
python -m validation.integration_contract.sector_handoff
python -m unittest universe24.tests.test_integration_contract -v
python -m unittest universe24.tests.test_sector_handoff -v
```

It compares both massive45 builders at `dt=1/64` and `1/32`, `dx=1/4`,
`mass_squared=1`: identical 889-term tensors and complete `(a,b,r)` states,
27 nodes, three updates, all six carry classes, independent scalar oracle,
per-step inverse and full rewind. The seed is independently constructed.
Tensor identities alone are insufficient: runtime state and source identities
are also checked. No second engine or observation feedback is introduced.

The independent sector implementations in #55 and #57 agree on the full
tensor and the index-mapped six-channel evolution polynomials. Their default
complete-state domains are **different**: #55 fixes omitted carries to zero,
while #57 fixes them to the full channel index modulo six. Their reduced
`d`/`dust` names and `official`/`audit` labels also differ, so reduced tensor
fingerprints and readout authority must not be equated.

The sector handoff test rejects both cross-default projections. An explicitly
prepared new zero-carry embedding for #57 then agrees exactly with #55 for
three Engine updates, 27 nodes, signed nonzero histories and all six carry
classes, including inverse and rewind. Neither original state is reset or
discarded. Default runs keep equal a/b but different r throughout. This is an
explicit preparation contract, not an observer correction or runtime adapter.

## What connects, and what remains missing

| Interface | Verified scope | Remaining acceptance gate |
| --- | --- | --- |
| Geometry45 ↔ board/completion | Same tensor and complete state at matched parameters | First-step H is `-403/40960000` at h=1/64, not zero |
| Rational invariant target ↔ Rule3 history lift | First tick preserves the homogeneous constraint | Second tick fails; target invariance is not complete-state invariance |
| Geometry45 ↔ homogeneous q,p apparatus47 | Reciprocal homogeneous exchange identities | Bounded energy and inhomogeneous momentum/source closure |
| Apparatus47 ↔ record48 | Exact retained history changes later raw feedback | Record stress and continuum scaling of that feedback |
| Local interaction ↔ native compiler | One potential generates the forces executed in a counted six-channel composition | This primitive is not a sourced Einstein macro map |
| Metric ↔ clocks/signals | Shared principal cones; separate linear massive-packet control | Same-law material-clock convergence; the packet control has a proper-time mismatch |
| Retained selector ↔ probabilities | Exact reversible routing and complete trial records | A uniquely justified preparation measure; Born and physical Bell evidence |

The standalone native three- and seven-channel controls are separate laws.
Their channels, stability results and invariants cannot be added to massive45
as if they already shared one physical construction. A direct spatial scalar
extension of apparatus47 needs three gradients: 50 channels, or 51 with record.
Any proposed compression must prove closure for both histories and all carries.

The immediate solution-search target is a complete-state temporal construction
for the small homogeneous sector, with explicit workspace and a preserved
constraint. It must retain the tick-two negative as a regression control.
Only then can it support a broader coupled-model claim. See the
[temporal handoff](temporal_handoff.md) for the restricted obstruction and
acceptance sequence.

## Reproduce the imported research

Prepare a clean detached checkout of PR50 commit
`62202fdccdd9a40d5dbbec104de6f97d9587a999` as `$REFERENCE50`; both source-import
audits require that exact historical source, not an arbitrary current checkout.

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/system-smoke
python -m universe24 verify --run runs/system-smoke/run
python -m validation.completion.run_all
python -m validation.generic_structure.run_all
python -m validation.generic_couplings --out runs/generic-couplings
python -m validation.einstein_node_audit.node_algebra
python -m validation.einstein_node_audit.clock_geometry
python -m validation.einstein_node_audit.load_invariance
python -m validation.einstein_node_audit.principal_cones --source "$REFERENCE50"
python -m validation.einstein_node_audit.independent_review
python -m validation.selection.run_audits --reference "$REFERENCE50" --out runs/retained-selection
```

The selection output directory must be fresh. Research command success means
the stated positive results **and negative controls** reproduced. Historical
evidence stays pinned; new evidence is written under `runs/`. Remote CI status
belongs to its exact commit and must be read from GitHub, not inferred from this
ledger. Other active teams' unpublished working trees are not integrated source.
