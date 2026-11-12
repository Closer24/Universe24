# Published handoff inventory

This is a source inventory, not a new physics test result. It compares the
published proposal heads with main `b8a064a9b0cccb1218445578d8765642572b40a7`
and the integration history through `a94dff2fd2343c15ff2d0f7f4f7a4287fa4ff7c6`.
An ancestor check proves historical inclusion; it does not prove that every
old file remains unchanged or that a physical claim passes.

## Disposition of the twelve open handoffs inspected

| Handoff | Exact source head | Verified inclusion and disposition |
| --- | --- | --- |
| 64, anisotropic conservation | `97e3a42f31fee76826305af314540c05323edf32` | Ancestor of main. Already incorporated; close the redundant handoff. |
| 57, generic interaction construction | `455cc5f3ec4ae4a3992ddf032f95c884321ff466` | Ancestor of main. Already incorporated; close the redundant handoff. |
| 54, retained selection | `d4f281c0839887ac7af8c050c406b2081f7c9baf` | Ancestor of main. Already incorporated; close the redundant handoff. |
| 52, completion audits | `8c53e69f4b466dcbd2da7dab7e3c365bd9731766` | Ancestor of main. Already incorporated; close the redundant handoff. |
| 50, frame/algebra research | `62202fdccdd9a40d5dbbec104de6f97d9587a999` | Ancestor of main. Already incorporated; close the redundant handoff. |
| 48, integration reviews | `72a4a0f229f137c8bcc30fb390d86c764c7a1dba` | Ancestor of main. Already incorporated; close the redundant handoff. |
| 65, local carrier/record/source chart | `fb4a09b2925a876d6c92493b2784fe30c16ed2e1` | Ancestor of the integration tree, not the inspected main. Complete package and tests incorporated for final combined validation. |
| 67, gauge-loop controls | `eb90805563c203625fbafbecc8696e39cba7ea2b` | Ancestor of the integration tree, not the inspected main. Complete package and tests incorporated for final combined validation. |
| 38, six-lens audits | `e0539cc60057b4616bce95cfa0926f4a7705b58f` | Not an ancestor of main. Its new audit sources and reports are not present there. Historical counterexamples remain catalogued; preserve the exact source as history, not a production replacement. |
| 39, 70-channel coupled frame | `35344a1ba5c12c857404115e893911411ece7d35` | Not an ancestor of main. The proposed installed frame-matter modules are absent. Excluded from the supported allocation because it needs 70 channels before apparatus and retains physical defects. Preserve its source/derivation as history. |
| 42, compact coupled frame | `49b896c795203914a939e465d6d39e5b99343259` | Not an ancestor of main. Six helpers are copied exactly and one is relocated with import changes; the complete candidate is exercised by a pinned compatibility checkout. Restricted reference, not a production physical default. |
| 43, history-dependent routing | `3a02ade62f09db68e2c78d7b0eb7db8f88f81304` | Not an ancestor of main. Its new sources and reports are absent. The 31-channel construction and its failed growth panel are catalogued; appending it to the 44-channel frame would need 75 channels. Preserve as historical research rather than restore the old experiments interface. |

The head of 38 is an ancestor of 43; the head of 39 is an ancestor of 42.
Therefore preserving the full histories of 43 and 42 also preserves those
two earlier heads. Closing these four proposals is not evidence that their
implementations were all imported or that their physical tasks were solved.

## Exact compact-frame ports

Each of the following paths in `validation/geometry/team48/` has exactly the
same Git blob as the corresponding `experiments/geometry/team48/` file at
the pinned 42 head:

- `geometry_positive_pairs.py`
- `geometry_triangular.py`
- `integer_sign_lift.py`
- `matter_charged.py`
- `matter_dust_square.py`
- `matter_equations.py`

`numerical_sign_validation.py` is also present. Its differences are the
`experiments` → `validation` import and source-manifest paths. The historical
`candidate.py`, staggered builder/audit, complete report, several independent
audits and frame-matter modules are not present as current files.

`validation/team48_contract.py` explicitly checks out/accepts only the pinned
42 source, imports it in an isolated subprocess, exports complete inputs,
then executes and verifies those inputs through the current single runtime.
It compares all saved histories and carries; its report explicitly declines
physical promotion. The CI workflow has a separate checkout step for this
pin. This dependency must remain reproducible when cleaning branch names.

## Six-lens and complexity source boundary

The following historical trees are absent from the current checkout, including
after a search for their exact Git blobs under other paths:

| Historical source | Absent source/report group |
| --- | --- |
| 38 | `experiments/research/six_lens_*.py`; `docs/research/six-lens/`; `docs/PHYSICS_GAP_SYNTHESIS.md`; `docs/evidence/six_lens_physics.json` |
| 39 | `universe24/{algebra,layers,observe,prepare}/frame_matter.py`; frame-matter test/audit/report and evidence |
| 43 | `experiments/complexity/`; `docs/research/complexity/`; `docs/COMPLEXITY_MECHANISMS.md`; `docs/evidence/complexity_mechanisms.json` |

Their findings are summarized in `docs/ONE_SYSTEM.md` and
`docs/proposals/INDEX.md`, and newer `validation/synthesis/`, selection and
local-unification work addresses related questions. Related newer work is
not a byte-for-byte preservation or a replay of every historical experiment.

## Cube/clock checkpoint

The published checkpoint is
`228ba23171ec600820b24fd9341ab1f9608bf371`. It contains the recovery report,
recovery metadata and compressed evidence at 19 changed paths, including 17
compressed-file paths with duplicated content. It does not contain the new
Python implementation, its tests, or all normal bundle metadata. Its recovery
report explicitly says the final integrated test outcome is unknown.

The archived findings describe two-channel spatial transport, complete cube
covariance and recurrent cluster formation, with failed structural-growth
criteria. They cannot be promoted to current executable evidence from this
checkpoint alone. Preserve the checkpoint as incomplete historical evidence;
recover or reconstruct the missing implementation and rerun the full joined
experiment before admitting it to the runnable source inventory.

## Cleanup requirements

There is no missing published implementation in the six ancestor handoffs or
the two newly integrated packages. There is a genuine source-availability
boundary for the cube work and an intentional exclusion boundary for the four
older proposals.

Before removing proposal branch refs, preserve the exact excluded source
heads and the cube checkpoint in durable repository history or a main-owned
archive. Do not discard them on the assumption that the current source tree
contains their files. Avoid importing their old workflow, runtime entry points
or superseded defaults merely to preserve their evidence. Record closure as
incorporated, historical/rejected, or incomplete, with continuing physical
obligations in the central research plan.

This inventory was checked with ancestor tests, changed-file inventories,
whole-tree blob comparisons and direct inspection of the compatibility
adapter and recovery report. It did not execute the excluded historical
implementations or certify their old reported test counts.
