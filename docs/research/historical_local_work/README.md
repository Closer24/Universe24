# Preserved local node, link and face research

This is an archive of the earlier local work based on commit
`e582960f6c9d2d134d3d6b28c08494e8bfafa86a`. It preserves the work when current
main moves to the exact 48-channel `2O-left-regular-cube/1` admission contract.
It does not install the older models, pad their channel budgets, rewrite their
historical evidence, or waive current bundle validation.

The archive contains every changed or new source/document/test file from the
older worktree: five modified tracked files, sixteen untracked files, and
four research programs found under the ignored `runs/` directory. The
complete **25-file** snapshot is byte-preserved. Python snapshots use the
`.py.txt` extension and are not imported or discovered as active tests.

## Contents

| Earlier work | Preserved source and scope |
| --- | --- |
| Shared node/link topology | `core/network.py`, `observe/network.py`, topology tests and smoke; six views of three canonical undirected interfaces per cell |
| Frozen propagation delays | 31-channel lengths 1/2/4 construction, tests and geometry/clock countercontrols |
| Coupled natural scatterer | Separate 10-channel law, tests, positive-domain proof and failed length-to-arrival interpretation |
| Coupled face processor | 25-channel law, tests, two-endpoint phase feedback, one/two-update mode-dependent passage and counted transit memory |
| Passage-ticks-first control | Positive affine encoding of the frozen-delay law; native delays remain static |
| Spring and metric controls | Restoring-motion positivity failure, six-length/shear counterexample, tangent-interval metric reconstruction and saved-state natural-number audit |
| Documentation | All six new documents and complete modified README, system, agenda and proposal-index snapshots |

The older face-processor report records 29 runs and 1,056 updates with exact
replay/oracles, 33,065 upward and 33,059 downward canonical delay changes,
and 64,942 checked occupied-stage releases. These are historical results of
that 25-channel law. They are not evidence that the current 48-channel
component inherits its traffic feedback, memory stages, or positive domain.
The preserved general physical acceptance status remains blocked.

## Exact source and evidence

- [Applyable source patch](../../../validation/archive/local_20261113/changes-from-e582960.patch)
- [Full provenance and per-file SHA-256 inventory](../../../validation/archive/local_20261113/manifest.json)
- [Compressed non-trace evidence](../../../validation/archive/local_20261113/evidence-nontrace.tar.gz)
- [Readable selected gate summary](evidence-summary.json)
- [Source snapshot root](../../../validation/archive/local_20261113/source/)

The patch includes all 25 files, including the four originally ignored
programs. It was applied to a private temporary Git index initialized at the
exact historical base; every restored file was compared byte-for-byte with
the old worktree. The old worktree and its real index were not changed.

The evidence archive contains **1,455 original files**, including saved input
bundles, tensor/seed/protocol records, validation receipts, reports, logs and
the four research programs. Every archive member was checked against its
original SHA-256. The 16,632,672 original bytes compress to 1,469,659 bytes.

For reviewability, **349 bulk streams** are not included in the Git archive:
`full_trace.jsonl.gz`, `clicks.jsonl.gz` and `complete_panel.jsonl.gz`.
Their 61,857,182 bytes remain untouched in the older local worktree. Every
omitted stream has an exact original path, size and SHA-256 in the manifest.
This is a compact evidence archive, not a claim that the published archive
alone contains every byte required to replay an old saved run. Fresh runs
can be generated from the restored historical source and complete inputs.

The workspace-root `current-unittest.log` and `phase-cli-verify.json` belong
to the later 48-channel audit; copies already live with that audit's
`runs/light-link-resonance-20261113-v2/` evidence. They are not mislabeled as
results of the older models here.

## Restore only in a historical checkout

Start a separate worktree at the pinned historical base, then apply the
archive patch there. Substitute the real absolute path of the patch:

```bash
git worktree add --detach ../Universe24-historical e582960f6c9d2d134d3d6b28c08494e8bfafa86a
cd ../Universe24-historical
git apply --check /absolute/path/to/changes-from-e582960.patch
git apply /absolute/path/to/changes-from-e582960.patch
python -m validation.face_transport --out runs/new-face-transport
```

The archived documents give the other historical reproduction commands.
The four restored `runs/dynamic-link-review-20261113/*.py` programs require
the historical repository on the Python import path, for example
`PYTHONPATH=. python runs/dynamic-link-review-20261113/time_link_naturals.py`.
Their output directories must be fresh; extracting the evidence archive into
that same worktree would populate those original output locations.

Do not apply this patch to current main or import the `.py.txt` snapshots as
an alternate current runtime. A new admitted representation requires its own
48-channel tensor, covariance proof, preparation and fresh evidence.
